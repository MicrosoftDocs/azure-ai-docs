---
title: "Hosted agent runtime contract"
description: "Reference for the runtime contract a hosted agent container must fulfill in Foundry Agent Service: port, health probe, protocols, and environment variables."
author: aahill
ms.author: aahi
ms.manager: mcleans
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.topic: reference
ms.date: 06/15/2026
ms.custom: doc-kit-assisted
ai-usage: ai-assisted
---

# Hosted agent runtime contract

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

A hosted agent is a container that fulfills a specific runtime contract with the Microsoft Foundry platform. This reference describes what the platform expects from your container and how the SDK adapter packages help you meet those requirements.

The SDK adapter packages implement the entire contract for you. If you use `azure-ai-agentserver-responses` or `azure-ai-agentserver-invocations`, you implement only your handler logic.

## Contract requirements

Your container must:

| Requirement | Detail |
| ----------- | ------ |
| Listen on port 8088 | HTTP/1.1, plain HTTP. The platform terminates TLS. |
| Serve a health probe | Return `200 OK` from `GET /readiness`. |
| Implement a protocol endpoint | Serve at least one of `POST /responses` or `POST /invocations`. |
| Consume platform environment variables | Read the variables the platform injects at startup. |
| Shut down gracefully | Flush writes and close connections on `SIGTERM`. |

## Protocol endpoints

A protocol defines the HTTP contract between Foundry and your agent container. Your container implements at least one protocol endpoint.

### Responses protocol

The responses protocol implements the OpenAI Responses API. The platform sends requests to `POST /responses` and expects either a JSON response or a Server-Sent Events (SSE) stream.

| Aspect | Detail |
| ------ | ------ |
| Endpoint | `POST /responses` |
| Input | OpenAI Responses API request (`input`, `model`, `stream`, and so on) |
| Output | JSON response object or SSE stream of response events |
| Conversation history | Hydrated automatically by the SDK adapter when `conversation.id` is present |
| Streaming | SSE with the `text/event-stream` content type |

Use the responses protocol as the standard choice. It's compatible with the OpenAI API ecosystem.

### Invocations protocol

The invocations protocol is a minimal pass-through protocol. You define the payload structure, and the platform passes it through without interpretation.

| Aspect | Detail |
| ------ | ------ |
| Endpoint | `POST /invocations` |
| Input | Any JSON payload your handler expects |
| Output | Any JSON response or SSE stream |
| Conversation history | Not managed. Your code handles state if needed. |
| Streaming | Optional, through SSE |

Use the invocations protocol when you need full control over the request and response payloads.

## SDK adapter packages

The adapter packages are protocol-specific and framework-agnostic. They work with any agent framework, including Microsoft Agent Framework, LangGraph, and custom code.

| Protocol | Python package | .NET package |
| -------- | -------------- | ------------ |
| Responses | `azure-ai-agentserver-responses` | `Azure.AI.AgentServer.Responses` |
| Invocations | `azure-ai-agentserver-invocations` | `Azure.AI.AgentServer.Invocations` |

The adapter handles the following parts of the contract for you:

* HTTP server setup on port 8088.
* The health probe endpoint (`GET /readiness`).
* Protocol-specific request parsing and response formatting.
* Conversation history hydration (responses protocol).
* SSE streaming infrastructure.
* OpenTelemetry instrumentation.
* Graceful shutdown on `SIGTERM`.
* Platform environment variable consumption.

You implement a handler function that receives parsed requests and returns responses.

## Handler examples

The complete bring-your-own samples for both protocols and both languages are in the [foundry-samples](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples) repository.

### Responses protocol example

This minimal handler forwards user input to a model from the Foundry model catalog through the Responses API. The SDK adapter hydrates conversation history automatically through `context.get_history()` (Python) or `context.GetHistoryAsync()` (C#), so the agent maintains context across turns.

### [Python](#tab/python)

From [`bring-your-own/responses/hello-world/main.py`](https://github.com/microsoft-foundry/foundry-samples/blob/main/samples/python/hosted-agents/bring-your-own/responses/hello-world/main.py):

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

# FOUNDRY_PROJECT_ENDPOINT is auto-injected in hosted Foundry containers and
# set by 'azd ai agent run' for local development.
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
    history = await context.get_history()

    # Build the model input from prior conversation turns + the current message.
    input_items = []
    for item in history:
        # Map history items to {"role": ..., "content": ...} dicts; see the
        # full sample for the unpacking helper.
        ...
    input_items.append({"role": "user", "content": user_input})

    response = await asyncio.get_running_loop().run_in_executor(
        None,
        lambda: _responses_client.create(
            model=_model,
            instructions="You are a helpful AI assistant.",
            input=input_items,
            store=False,  # platform manages history; don't store at model level
        ),
    )

    return TextResponse(context, request, text=response.output_text)


app.run()
```

Reference: [ResponsesAgentServerHost](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/hosted-agents), [AIProjectClient](/python/api/azure-ai-projects/azure.ai.projects.aiprojectclient), [DefaultAzureCredential](/python/api/azure-identity/azure.identity.defaultazurecredential)

### [C#](#tab/csharp)

From [`bring-your-own/responses/HelloWorld/Program.cs`](https://github.com/microsoft-foundry/foundry-samples/blob/main/samples/csharp/hosted-agents/bring-your-own/responses/HelloWorld/Program.cs):

```csharp
using Azure.AI.AgentServer.Responses;
using Azure.AI.AgentServer.Responses.Models;
using Azure.AI.Extensions.OpenAI;
using Azure.AI.Projects;
using Azure.Identity;
using OpenAI.Responses;

ResponsesServer.Run<HelloWorldHandler>(configure: builder =>
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

public sealed class HelloWorldHandler(ProjectResponsesClient responsesClient)
    : ResponseHandler
{
    private const string SystemPrompt = "You are a helpful AI assistant.";

    public override IAsyncEnumerable<ResponseStreamEvent> CreateAsync(
        CreateResponse request,
        ResponseContext context,
        CancellationToken cancellationToken)
    {
        return new TextResponse(context, request,
            createText: ct => GenerateTextAsync(context, ct));
    }

    private async Task<string> GenerateTextAsync(
        ResponseContext context,
        CancellationToken cancellationToken)
    {
        var userInput = await context.GetInputTextAsync(
            cancellationToken: cancellationToken) ?? "Hello!";
        var history = await context.GetHistoryAsync(cancellationToken);

        var options = new CreateResponseOptions { Instructions = SystemPrompt };
        // Map history items into options.InputItems via
        // ResponseItem.Create*MessageItem(...). See the full sample.
        options.InputItems.Add(ResponseItem.CreateUserMessageItem(userInput));

        var result = await responsesClient.CreateResponseAsync(options);
        return result.Value.GetOutputText() ?? string.Empty;
    }
}
```

Reference: [Azure.AI.Projects](/dotnet/api/azure.ai.projects), [DefaultAzureCredential](/dotnet/api/azure.identity.defaultazurecredential)

---

### Invocations protocol example

With the invocations protocol, your handler receives whatever JSON the caller posts and returns whatever JSON your code chooses. There's no built-in conversation history.

### [Python](#tab/python)

Pattern from [`bring-your-own/invocations/hello-world`](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/hosted-agents/bring-your-own/invocations/hello-world):

```python
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from azure.ai.agentserver.invocations import InvocationAgentServerHost

app = InvocationAgentServerHost()


@app.invoke_handler
async def handle_invoke(request: Request) -> Response:
    data = await request.json()
    message = data.get("message", "Hello!")
    return JSONResponse({"echo": message})


if __name__ == "__main__":
    app.run()
```

### [C#](#tab/csharp)

Pattern from [`bring-your-own/invocations/HelloWorld`](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/csharp/hosted-agents/bring-your-own/invocations/HelloWorld):

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
    await httpContext.Response.WriteAsJsonAsync(new { echo = message });
});
```

---

The full samples also include conversation-history hydration, error handling, telemetry, toolbox integration, and Dockerfile and `agent.yaml` setup.

## Health probe

The platform sends `GET /readiness` to determine whether your container is ready to serve traffic. Return `200 OK` when the container is ready, or a non-200 status to signal that the platform should restart the instance. The SDK adapters register this endpoint automatically.

## Network and transport

| Property | Value |
| -------- | ----- |
| Protocol | HTTP/1.1 |
| Default port | 8088 (override with the `PORT` environment variable) |
| Bind address | `0.0.0.0` (all interfaces) |
| TLS | Terminated by the platform. Your container serves plain HTTP. |

## Graceful shutdown

When the platform sends `SIGTERM`, your container stops accepting new requests, finishes in-flight requests, flushes pending writes to `$HOME` (the session filesystem), and exits cleanly. The SDK adapters handle this sequence automatically.

## Platform environment variables

The platform injects environment variables into your container at startup. Your code can read the following key variables:

| Variable | Purpose |
| -------- | ------- |
| `FOUNDRY_PROJECT_ENDPOINT` | Foundry project endpoint for API calls |
| `FOUNDRY_AGENT_NAME` | The agent's name |
| `FOUNDRY_AGENT_VERSION` | The agent's version |
| `FOUNDRY_AGENT_SESSION_ID` | The current session ID |

## Related content

* [What are hosted agents?](hosted-agents.md)
* [Agent development lifecycle](development-lifecycle.md)
* [Python hosted agent samples](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/hosted-agents)
