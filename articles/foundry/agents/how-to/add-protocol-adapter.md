---
title: "Add a protocol adapter to your hosted agent"
description: "Add Responses or Invocations protocol support to a hosted agent: install the SDK adapter package, wire up a handler, declare the protocol, and redeploy."
author: aahill
ms.author: aahi
ms.manager: mcleans
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.topic: how-to
ms.date: 06/15/2026
ms.custom: dev-focus, doc-kit-assisted
ai-usage: ai-assisted
---

# Add a protocol adapter to your hosted agent

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

A protocol adapter is a lightweight SDK wrapper that lets your agent code speak one of the Microsoft Foundry hosted agent protocols. In this article, you install the SDK adapter package, wire up a handler, declare the protocol in `agent.yaml`, and redeploy. Add an adapter when you bring your own code that doesn't already implement the [hosted agent runtime contract](../concepts/hosted-agent-contract.md).

## Prerequisites

* A hosted agent project. To create one, see [Initialize a hosted agent project with the Azure Developer CLI](init-agent-project.md).
* Python 3.10 or later, or .NET 8 or later.
* Your agent logic in a function you can call from a handler.

## Choose a protocol

| Protocol | When to use |
| -------- | ----------- |
| `responses` | Conversational agents. You get automatic conversation history, streaming, and OpenAI Responses API compatibility. |
| `invocations` | Non-conversational or custom-payload workloads. You define the request and response shape. |

For the full contract details, see [Hosted agent runtime contract](../concepts/hosted-agent-contract.md).

## Install the SDK package

### [Python](#tab/python)

```bash
# For the Responses protocol
pip install azure-ai-agentserver-responses

# For the Invocations protocol
pip install azure-ai-agentserver-invocations
```

### [C#](#tab/csharp)

```bash
# For the Responses protocol
dotnet add package Azure.AI.AgentServer.Responses

# For the Invocations protocol
dotnet add package Azure.AI.AgentServer.Invocations
```

---

## Implement a handler

The patterns below are abridged from the bring-your-own samples in the [foundry-samples](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples) repository. Use them as a starting point and copy the full sample for production code.

### Responses protocol

### [Python](#tab/python)

```python
import asyncio
import os

from azure.ai.agentserver.responses import (
    CreateResponse,
    ResponseContext,
    ResponsesAgentServerHost,
    ResponsesServerOptions,
    TextResponse,
)
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

_endpoint = os.environ["FOUNDRY_PROJECT_ENDPOINT"]
_model = os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"]

_project_client = AIProjectClient(
    endpoint=_endpoint, credential=DefaultAzureCredential()
)
_responses_client = _project_client.get_openai_client().responses

app = ResponsesAgentServerHost(
    options=ResponsesServerOptions(default_fetch_history_count=20),
)


@app.response_handler
async def handler(
    request: CreateResponse,
    context: ResponseContext,
    _cancellation_signal: asyncio.Event,
):
    user_input = await context.get_input_text() or "Hello!"

    # --- Your agent logic goes here ---
    response = await asyncio.get_running_loop().run_in_executor(
        None,
        lambda: _responses_client.create(
            model=_model,
            instructions="You are a helpful AI assistant.",
            input=[{"role": "user", "content": user_input}],
            store=False,
        ),
    )
    # -----------------------------------

    return TextResponse(context, request, text=response.output_text)


app.run()
```

### [C#](#tab/csharp)

```csharp
using Azure.AI.AgentServer.Responses;
using Azure.AI.AgentServer.Responses.Models;
using Azure.AI.Extensions.OpenAI;
using Azure.AI.Projects;
using Azure.Identity;
using OpenAI.Responses;

ResponsesServer.Run<MyHandler>(configure: builder =>
{
    var endpoint = Environment.GetEnvironmentVariable("FOUNDRY_PROJECT_ENDPOINT")
        ?? throw new InvalidOperationException("FOUNDRY_PROJECT_ENDPOINT is not set.");
    var model = Environment.GetEnvironmentVariable("AZURE_AI_MODEL_DEPLOYMENT_NAME")
        ?? throw new InvalidOperationException("AZURE_AI_MODEL_DEPLOYMENT_NAME is not set.");

    var projectClient = new AIProjectClient(
        new Uri(endpoint), new DefaultAzureCredential());
    var responsesClient = projectClient.ProjectOpenAIClient
        .GetProjectResponsesClientForModel(model);

    builder.Services.AddSingleton(responsesClient);
});

public sealed class MyHandler(ProjectResponsesClient responsesClient)
    : ResponseHandler
{
    public override IAsyncEnumerable<ResponseStreamEvent> CreateAsync(
        CreateResponse request,
        ResponseContext context,
        CancellationToken cancellationToken)
    {
        return new TextResponse(context, request,
            createText: async ct =>
            {
                var input = await context.GetInputTextAsync(
                    cancellationToken: ct) ?? "Hello!";

                // --- Your agent logic goes here ---
                var options = new CreateResponseOptions
                {
                    Instructions = "You are a helpful AI assistant."
                };
                options.InputItems.Add(
                    ResponseItem.CreateUserMessageItem(input));
                var result = await responsesClient.CreateResponseAsync(options);
                return result.Value.GetOutputText() ?? string.Empty;
                // -----------------------------------
            });
    }
}
```

---

### Invocations protocol

### [Python](#tab/python)

```python
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from azure.ai.agentserver.invocations import InvocationAgentServerHost

app = InvocationAgentServerHost()


@app.invoke_handler
async def handle_invoke(request: Request) -> Response:
    data = await request.json()
    # --- Your agent logic goes here ---
    # The payload shape is entirely up to you
    message = data.get("message", "Hello!")
    return JSONResponse({"reply": message})


if __name__ == "__main__":
    app.run()
```

### [C#](#tab/csharp)

```csharp
using Azure.AI.AgentServer.Invocations;
using Microsoft.AspNetCore.Http;

InvocationsServer.Run(handler: async (HttpContext httpContext) =>
{
    var data = await httpContext.Request
        .ReadFromJsonAsync<Dictionary<string, object>>();
    var message = data is { } d && d.TryGetValue("message", out var m)
        ? m?.ToString() ?? "Hello!"
        : "Hello!";

    // --- Your agent logic goes here ---
    await httpContext.Response.WriteAsJsonAsync(new { reply = message });
    // -----------------------------------
});
```

---

## Declare the protocol in agent.yaml

Add or update the `protocols` field in your `agent.yaml`:

```yaml
template:
  kind: hosted
  protocols:
    - protocol: responses
      version: 1.0.0
```

For invocations, use the following protocol:

```yaml
template:
  kind: hosted
  protocols:
    - protocol: invocations
      version: 1.0.0
```

## Update your startup command

Make sure the `startupCommand` in `azure.yaml` points to the entry point that starts the server:

```yaml
config:
    startupCommand: python main.py
```

## Test locally and redeploy

```bash
# Test locally
azd ai agent run

# In another terminal
azd ai agent invoke --local "Hello!"

# Deploy
azd deploy
```

For the `invocations` protocol, use `--input-file` to send your custom payload:

```bash
azd ai agent invoke --local -f request.json
```

## Add a second protocol

An agent can support multiple protocols. To add a second one, install the additional SDK package, register both handlers in your entry point, and add both protocols to `agent.yaml`:

```yaml
protocols:
  - protocol: responses
    version: 1.0.0
  - protocol: invocations
    version: 1.0.0
```

> [!NOTE]
> When an agent supports multiple protocols, `azd ai agent invoke` uses the `responses` protocol by default. Pass `-p`/`--protocol` to select `responses` or `invocations` explicitly.

## Related content

* [Hosted agent runtime contract](../concepts/hosted-agent-contract.md)
* [What are hosted agents?](../concepts/hosted-agents.md)
* [agent.yaml schema reference](../concepts/agent-yaml-reference.md)
