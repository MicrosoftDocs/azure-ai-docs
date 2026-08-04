---
title: Host Microsoft Agent Framework agents as Foundry hosted agents
description: Learn how to host Microsoft Agent Framework agents on Foundry hosted agents with the Responses and Invocations protocols
ms.service: microsoft-foundry
ms.subservice: foundry-sdk
ms.topic: how-to
ms.date: 06/30/2026
ms.author: aahi
author: aahill
ms.reviewer: ctoshniwal, taochen
ms.custom:
  - dev-focus
ai-usage: ai-assisted
zone_pivot_groups: microsoft-agent-framewok
# customer intent: As a developer, I want to host a Microsoft Agent Framework agent on Foundry hosted agents service.
---

# Host Microsoft Agent Framework agents as Foundry hosted agents

Use the Microsoft Agent Framework hosting packages to expose an Agent Framework
agent through the protocols for Foundry
[hosted agents](../../agents/overview.md#hosted-agents). The hosting packages let
you keep your agent logic in code while Foundry manages the hosted runtime,
sessions, scale, identity, and protocol endpoints.

In this article, you create a minimal Agent Framework agent, expose it through
either the Responses or Invocations protocol, test it through HTTP, and deploy
it to Foundry with the Azure Developer CLI.

## Prerequisites

- An Azure subscription. [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- A [Foundry project](../create-projects.md).
- A deployed chat model, such as `gpt-4.1` or `gpt-4o`.
- The **Foundry Project Manager** role on the project to deploy a hosted agent. For details, see [Deploy a hosted agent](../../agents/how-to/deploy-hosted-agent.md#required-permissions).
- Azure CLI signed in (`az login`) so `DefaultAzureCredential` can authenticate.

::: zone pivot="programming-language-python"

- Python 3.10 or later.

::: zone-end

::: zone pivot="programming-language-csharp"

- .NET 10 SDK or later.

::: zone-end

## Install the packages

::: zone pivot="programming-language-python"

Install the Agent Framework and the Foundry hosting package:

```bash
pip install -U agent-framework agent-framework-foundry-hosting azure-identity python-dotenv
```

The `agent_framework_foundry_hosting` package provides the host servers for the
Foundry protocols:

- `ResponsesHostServer` for the OpenAI-compatible `/responses` endpoint.
- `InvocationsHostServer` for the generic `/invocations` endpoint.

::: zone-end

::: zone pivot="programming-language-csharp"

Add the Agent Framework and Foundry hosting packages to your project:

```bash
dotnet add package Microsoft.Agents.AI
dotnet add package Microsoft.Agents.AI.Foundry.Hosting
dotnet add package Azure.AI.Projects
dotnet add package Azure.Identity
```

For the Invocations protocol, also add the Invocations server package:

```bash
dotnet add package Azure.AI.AgentServer.Invocations
```

These packages provide the host extensions for the Foundry protocols:

- `AddFoundryResponses` and `MapFoundryResponses` for the OpenAI-compatible `/responses` endpoint.
- `AddInvocationsServer` and `MapInvocationsServer` for the generic `/invocations` endpoint.

::: zone-end

## Choose a hosting protocol

Hosted agents can expose one or more protocols. Start with Responses for most
conversational agents.

| Protocol    | Endpoint       | Use when                                                                                  |
| ----------- | -------------- | ----------------------------------------------------------------------------------------- |
| Responses   | `/responses`   | You want OpenAI-compatible chat, streaming, response history, and conversation threading. |
| Invocations | `/invocations` | You want a custom JSON shape, a webhook-style endpoint, or non-conversational processing. |

For background on protocol behavior and sessions, see [Hosted agents](../../agents/concepts/hosted-agents.md) and [Manage hosted agent sessions](../../agents/how-to/manage-hosted-sessions.md).

## Configure environment variables

Set the project endpoint and model deployment name for local development:

```bash
export FOUNDRY_PROJECT_ENDPOINT="https://<resource>.services.ai.azure.com/api/projects/<project>"
export AZURE_AI_MODEL_DEPLOYMENT_NAME="gpt-4.1"
```

In PowerShell:

```powershell
$env:FOUNDRY_PROJECT_ENDPOINT="https://<resource>.services.ai.azure.com/api/projects/<project>"
$env:AZURE_AI_MODEL_DEPLOYMENT_NAME="gpt-4.1"
```

When the same code runs as a hosted agent in Foundry, the platform injects
`FOUNDRY_PROJECT_ENDPOINT` and `AZURE_AI_MODEL_DEPLOYMENT_NAME` at runtime.

## Responses protocol

Use the Responses protocol when you want an OpenAI-compatible chat endpoint with
streaming, response history, and conversation threading.

### Create a Responses host

::: zone pivot="programming-language-python"

Create a file named `main.py` with a minimal Agent Framework agent that uses a
Foundry model.

```python
import os

from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient
from agent_framework_foundry_hosting import ResponsesHostServer
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

# Load environment variables from a .env file when present.
load_dotenv()


def main() -> None:
    client = FoundryChatClient(
        project_endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
        model=os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
        credential=DefaultAzureCredential(),
    )

    agent = Agent(
        client=client,
        instructions="You are a friendly assistant. Keep your answers brief.",
        # The hosting infrastructure manages conversation history, so the
        # service doesn't need to store it.
        default_options={"store": False},
    )

    server = ResponsesHostServer(agent)
    server.run()


if __name__ == "__main__":
    main()
```

**What this snippet does:** Creates an Agent Framework agent backed by a Foundry
model through `FoundryChatClient`, then passes the agent to
`ResponsesHostServer`. The host starts an HTTP server and exposes the agent
through `POST /responses`. By default, the server binds to port `8088`.

Reference: [Microsoft Agent Framework documentation](/agent-framework/)

Run the app locally:

```bash
python main.py
```

::: zone-end

::: zone pivot="programming-language-csharp"

Create a `Program.cs` file with a minimal Agent Framework agent that uses a
Foundry model through the Responses protocol.

```csharp
using Azure.AI.Projects;
using Azure.Identity;
using Microsoft.Agents.AI;
using Microsoft.Agents.AI.Foundry.Hosting;

var projectEndpoint = new Uri(
    Environment.GetEnvironmentVariable("FOUNDRY_PROJECT_ENDPOINT")
    ?? throw new InvalidOperationException("FOUNDRY_PROJECT_ENDPOINT is not set."));

var deployment =
    Environment.GetEnvironmentVariable("AZURE_AI_MODEL_DEPLOYMENT_NAME")
    ?? "gpt-4o";

// Create the agent via the AI project client using the Responses API.
AIAgent agent = new AIProjectClient(projectEndpoint, new DefaultAzureCredential())
    .AsAIAgent(
        model: deployment,
        instructions: "You are a friendly assistant. Keep your answers brief.",
        name: "assistant",
        description: "A simple general-purpose AI assistant");

// Host the agent as a Foundry hosted agent using the Responses API.
var builder = WebApplication.CreateBuilder(args);
builder.Services.AddFoundryResponses(agent);

var app = builder.Build();
app.MapFoundryResponses();
app.Run();
```

**What this snippet does:** Creates an `AIAgent` from the Foundry project client,
registers it as a Foundry Responses host with `AddFoundryResponses`, and maps
the `POST /responses` endpoint with `MapFoundryResponses`. By default, the host
serves on port `8088`.

Reference: [AIProjectClient](/dotnet/api/azure.ai.projects.aiprojectclient) | [DefaultAzureCredential](/dotnet/api/azure.identity.defaultazurecredential)

Run the app locally:

```bash
dotnet run
```

::: zone-end

### Test the Responses endpoint

Send a non-streaming Responses request to the local server.

**Bash:**

```bash
curl -sS -H "Content-Type: application/json" \
  -X POST http://localhost:8088/responses \
  -d '{"input":"Give me one practical tip for testing hosted agents.","stream":false}'
```

**PowerShell:**

```powershell
$body = @{
  input  = "Give me one practical tip for testing hosted agents."
  stream = $false
} | ConvertTo-Json

Invoke-RestMethod `
    -Uri http://localhost:8088/responses `
    -Method Post `
    -Body $body `
    -ContentType "application/json"
```

The server responds with a JSON object that contains the response text and a
response ID. For streaming responses, set `stream` to `true`. The host emits
Responses API server-sent events, such as `response.created`,
`response.output_text.delta`, and `response.completed`.

### Multi-turn conversations

To continue a conversation, pass the previous response ID in the
`previous_response_id` field of the next request:

```bash
curl -sS -H "Content-Type: application/json" \
  -X POST http://localhost:8088/responses \
  -d '{"input":"Can you make that more concise?","previous_response_id":"<previous-response-id>","stream":false}'
```

When the agent runs in Foundry, the same pattern works through the hosted agent
Responses endpoint. If later turns also need the same hosted sandbox filesystem,
include `agent_session_id` or use a `conversation` ID. For details, see
[Manage hosted agent sessions](../../agents/how-to/manage-hosted-sessions.md).

## Invocations protocol

Use the Invocations protocol when your callers can't use the Responses API
request shape or when your scenario isn't a chat conversation. The Invocations
host manages session state through an `agent_session_id` query parameter and
response header.

### Create an Invocations host

::: zone pivot="programming-language-python"

Use the same agent setup as the Responses example, but start
`InvocationsHostServer` instead of `ResponsesHostServer`.

```python
import os

from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient
from agent_framework_foundry_hosting import InvocationsHostServer
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

# Load environment variables from a .env file when present.
load_dotenv()


def main() -> None:
    client = FoundryChatClient(
        project_endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
        model=os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
        credential=DefaultAzureCredential(),
    )

    agent = Agent(
        client=client,
        instructions="You are a friendly assistant. Keep your answers brief.",
        default_options={"store": False},
    )

    server = InvocationsHostServer(agent)
    server.run()


if __name__ == "__main__":
    main()
```

**What this snippet does:** Hosts the Agent Framework agent through `POST
/invocations`. The host manages per-session state through the
`agent_session_id` query parameter and response header.

Reference: [Microsoft Agent Framework documentation](/agent-framework/)

::: zone-end

::: zone pivot="programming-language-csharp"

The Invocations protocol uses an `InvocationHandler` that you implement to
process each request. Register the Invocations server and your handler, then map
the endpoints.

```csharp
using Azure.AI.AgentServer.Invocations;
using Microsoft.Agents.AI;

var builder = WebApplication.CreateBuilder(args);

// Register your agent and the Invocations server services.
builder.Services.AddInvocationsServer();
builder.Services.AddScoped<InvocationHandler, MyInvocationHandler>();

var app = builder.Build();

// Map the Invocations protocol endpoints:
//   POST /invocations              - invoke the agent
//   GET  /invocations/{id}         - get result
//   POST /invocations/{id}/cancel  - cancel
app.MapInvocationsServer();
app.Run();
```

**What this snippet does:** Registers the Invocations server services and your
`InvocationHandler` implementation, then maps the `/invocations` endpoints. You
implement `MyInvocationHandler` to define how each request is processed. For a
complete handler example, see the [.NET Invocations sample](https://github.com/microsoft/agent-framework/tree/main/dotnet/samples/04-hosting/FoundryHostedAgents/invocations).

Reference: [AddInvocationsServer](/dotnet/api/azure.ai.agentserver.invocations)

::: zone-end

### Test the Invocations endpoint

Send a request to the local server:

```bash
curl -sS -X POST http://localhost:8088/invocations \
  -H "Content-Type: application/json" \
  -d '{"message":"My name is Alice.","stream":false}'
```

For multi-turn conversations, reuse the `agent_session_id` value from the
response header as the `agent_session_id` query parameter on the next request:

```bash
curl -sS -X POST "http://localhost:8088/invocations?agent_session_id=<session-id>" \
  -H "Content-Type: application/json" \
  -d '{"message":"What is my name?"}'
```

The platform doesn't store conversation history for the Invocations protocol.
Use the `agent_session_id` query parameter to route later calls to the same
hosted sandbox.

## Deploy

Deploy by using the Azure Developer CLI (`azd`). The flow uses sample manifests
and Docker to build the agent container image and roll it out to the Foundry
hosted agent runtime.

Hosted agent deployment requires the **Foundry Project Manager** role on the
project. For details, see [Deploy a hosted agent](../../agents/how-to/deploy-hosted-agent.md#required-permissions).

### Install the Azure Developer CLI extension

Install the AI agent extension and sign in before you initialize a sample:

```bash
azd ext install azure.ai.agents
azd auth login
```

Docker must be running locally because `azd ai agent run` builds the container
image declared in the sample's Dockerfile. For command details, see the
[Azure Developer CLI reference](/azure/developer/azure-developer-cli/reference).

### Initialize from a sample manifest

Create a new folder and initialize it from a sample manifest. Replace the
manifest URL with the sample you want to use.

::: zone pivot="programming-language-python"

```bash
mkdir my-agent-framework-agent
cd my-agent-framework-agent

azd ai agent init -m https://github.com/microsoft/agent-framework/blob/main/python/samples/04-hosting/foundry-hosted-agents/responses/01_basic/agent.manifest.yaml
```

::: zone-end

::: zone pivot="programming-language-csharp"

```bash
mkdir my-agent-framework-agent
cd my-agent-framework-agent

azd ai agent init -m https://github.com/microsoft/agent-framework/blob/main/dotnet/samples/04-hosting/FoundryHostedAgents/responses/Hosted-ChatClientAgent/agent.manifest.yaml
```

::: zone-end

Follow the prompts from `azd ai agent init`. If you don't already have a Foundry
project and model deployment, the initialization flow can guide you through
creating them.

### Provision Azure resources

If the initialized project uses a new Foundry project and model deployment,
provision the Azure resources first:

```bash
azd provision
```

This command creates a resource group that contains, among other resources, a
Foundry instance, a Foundry project with a model deployment, an Application
Insights instance, and a container registry for the hosted agent images.

### Run the container locally

Run the agent host locally through `azd`:

```bash
azd ai agent run
```

The host serves on `http://localhost:8088`. In another terminal, invoke the
local protocol endpoint:

```bash
azd ai agent invoke --local "Hello!"
```

You can also call the endpoint directly with `curl`:

```bash
curl -X POST http://localhost:8088/responses \
  -H "Content-Type: application/json" \
  -d '{"input": "Hello!"}'
```

### Deploy to Foundry

Deploy the agent:

```bash
azd deploy
```

The deployment packages the agent into a container image, pushes it to the
provisioned container registry, and rolls it out to the Foundry hosted agent
runtime.

The Foundry hosting infrastructure injects runtime environment variables into
the agent, including:

- `FOUNDRY_PROJECT_ENDPOINT`: The endpoint URL for the Foundry project where the
  agent is deployed.
- `AZURE_AI_MODEL_DEPLOYMENT_NAME`: The model deployment name selected during
  `azd ai agent init`.
- `APPLICATIONINSIGHTS_CONNECTION_STRING`: The connection string for the
  project's Application Insights instance.

For complete deployment concepts, permissions, and management details, see
[Deploy a hosted agent](../../agents/how-to/deploy-hosted-agent.md) and
[Manage hosted agent lifecycle](../../agents/how-to/manage-hosted-agent.md).

## Troubleshooting

Use this checklist to diagnose common issues while developing hosted agents with
Agent Framework.

### The model can't be reached in the hosted container

Confirm that the hosted agent version includes `AZURE_AI_MODEL_DEPLOYMENT_NAME`,
and that the agent identity has permission to call the Foundry project. The
platform sets `FOUNDRY_PROJECT_ENDPOINT`; your code should read that variable
when running in Foundry.

### Conversation state doesn't continue

For the Responses protocol, pass `previous_response_id` or a `conversation` ID
on later turns.

For the Invocations protocol, the platform doesn't store conversation history.
Use an `agent_session_id` query parameter to route later calls to the same
hosted sandbox.

### Protocol version mismatch

If requests fail after an upgrade, confirm that your manifest and hosting
package both use protocol version 2.0.0. Protocol versions 1.0.0 and 2.0.0 are
incompatible.

## Next step

> [!div class="nextstepaction"]
> [Deploy a hosted agent](../../agents/how-to/deploy-hosted-agent.md)

## Related content

- [What is Foundry Agent Service?](../../agents/overview.md)
- [Hosted agents](../../agents/concepts/hosted-agents.md)
- [Manage hosted agent sessions](../../agents/how-to/manage-hosted-sessions.md)
- [Host LangGraph agents as Foundry hosted agents](langchain-hosted-agents.md)
