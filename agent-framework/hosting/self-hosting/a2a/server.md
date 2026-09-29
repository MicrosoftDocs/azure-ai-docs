---
title: Host agents with A2A
description: Expose Agent Framework agents through the Agent-to-Agent protocol with .NET, Python, or Go.
zone_pivot_groups: programming-languages
author: dmkorolev
ms.service: agent-framework
ms.topic: tutorial
ms.date: 07/23/2026
ms.author: dmkorolev
ai-usage: ai-assisted
---

# Host agents with A2A

The Agent-to-Agent (A2A) protocol enables standardized communication between agents built with different frameworks and technologies. This page covers exposing Agent Framework agents as A2A servers.

To discover and invoke a remote A2A agent, see the [A2A agent service](../../../integrations/by-component/agent-services/a2a.md).

## What is A2A?

A2A is a standardized protocol that supports:

- **Agent discovery** through agent cards
- **Message-based communication** between agents
- **Long-running agentic processes** via tasks
- **Cross-platform interoperability** between different agent frameworks

For more information, see the [A2A protocol specification](https://a2a-protocol.org/latest/).

::: zone pivot="programming-language-csharp"

The `Microsoft.Agents.AI.Hosting.A2A.AspNetCore` library provides ASP.NET Core integration for exposing your agents via the A2A protocol.

**NuGet Packages:**
- [Microsoft.Agents.AI.Hosting.A2A](https://www.nuget.org/packages/Microsoft.Agents.AI.Hosting.A2A)
- [Microsoft.Agents.AI.Hosting.A2A.AspNetCore](https://www.nuget.org/packages/Microsoft.Agents.AI.Hosting.A2A.AspNetCore)

## Example

This minimal example shows how to expose an agent via A2A. The sample includes OpenAPI and Swagger dependencies to simplify testing.

#### 1. Create an ASP.NET Core Web API project

Create a new ASP.NET Core Web API project or use an existing one.

#### 2. Install required dependencies

Install the following packages:

  ## [.NET CLI](#tab/dotnet-cli)
  
  Run the following commands in your project directory to install the required NuGet packages:
  
  ```bash
  # Hosting.A2A.AspNetCore for A2A protocol integration
  dotnet add package Microsoft.Agents.AI.Hosting.A2A.AspNetCore --prerelease

  # Library to connect to Microsoft Foundry
  dotnet add package Microsoft.Agents.AI.Foundry --prerelease

  # Swagger to test app
  dotnet add package Microsoft.AspNetCore.OpenApi
  dotnet add package Swashbuckle.AspNetCore
  ```

  ---

#### 3. Configure Microsoft Foundry connection

The application requires a Microsoft Foundry project connection. Configure the endpoint and deployment name using `dotnet user-secrets` or environment variables.
You can also simply edit the `appsettings.json`, but that's not recommended for the apps deployed in production since some of the data can be considered to be secret.

  ## [User-Secrets](#tab/user-secrets)
  ```bash
  dotnet user-secrets set "AZURE_OPENAI_ENDPOINT" "https://<your-openai-resource>.openai.azure.com/"
  dotnet user-secrets set "AZURE_OPENAI_DEPLOYMENT_NAME" "gpt-4o-mini"
  ```
  ## [ENV Windows](#tab/env-windows)
  ```powershell
  $env:AZURE_OPENAI_ENDPOINT = "https://<your-openai-resource>.openai.azure.com/"
  $env:AZURE_OPENAI_DEPLOYMENT_NAME = "gpt-4o-mini"
  ```
  ## [ENV unix](#tab/env-unix)
  ```bash
  export AZURE_OPENAI_ENDPOINT="https://<your-openai-resource>.openai.azure.com/"
  export AZURE_OPENAI_DEPLOYMENT_NAME="gpt-4o-mini"
  ```
  ## [appsettings](#tab/appsettings)
  ```json
    "AZURE_OPENAI_ENDPOINT": "https://<your-openai-resource>.openai.azure.com/",
    "AZURE_OPENAI_DEPLOYMENT_NAME": "gpt-4o-mini"
  ```

  ---


#### 4. Add the code to Program.cs

Replace the contents of `Program.cs` with the following code and run the application:
```csharp
using A2A;
using A2A.AspNetCore;
using Azure.AI.Projects;
using Azure.Identity;
using Microsoft.Agents.AI;
using Microsoft.Agents.AI.Hosting;
using Microsoft.Extensions.AI;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddOpenApi();
builder.Services.AddSwaggerGen();

string endpoint = builder.Configuration["AZURE_OPENAI_ENDPOINT"]
    ?? throw new InvalidOperationException("AZURE_OPENAI_ENDPOINT is not set.");
string deploymentName = builder.Configuration["AZURE_OPENAI_DEPLOYMENT_NAME"]
    ?? throw new InvalidOperationException("AZURE_OPENAI_DEPLOYMENT_NAME is not set.");

// Register the chat client
IChatClient chatClient = new AIProjectClient(
        new Uri(endpoint),
        new DefaultAzureCredential())
        .GetProjectOpenAIClient()
        .GetProjectResponsesClient()
        .AsIChatClient(deploymentName);

builder.Services.AddSingleton(chatClient);

// Register an agent and its A2A server
var pirateAgent = builder.AddAIAgent("pirate", instructions: "You are a pirate. Speak like a pirate.");
pirateAgent.AddA2AServer();

var app = builder.Build();

app.MapOpenApi();
app.UseSwagger();
app.UseSwaggerUI();

// Expose the agent via the A2A HTTP+JSON protocol binding
app.MapA2AHttpJson(pirateAgent, "/a2a/pirate");

// Publish the agent card for discovery
app.MapWellKnownAgentCard(new AgentCard
{
    Name = "Pirate Agent",
    Description = "An agent that speaks like a pirate.",
    Version = "1.0",
    SupportedInterfaces =
    [
        new AgentInterface
        {
            Url = "http://localhost:5000/a2a/pirate",
            ProtocolBinding = ProtocolBindingNames.HttpJson,
            ProtocolVersion = "1.0",
        }
    ]
});

app.Run();
```

> [!WARNING]
> `DefaultAzureCredential` is convenient for development but requires careful consideration in production. In production, consider using a specific credential (e.g., `ManagedIdentityCredential`) to avoid latency issues, unintended credential probing, and potential security risks from fallback mechanisms.

### Testing the Agent

Once the application is running, you can test the A2A agent using the following `.http` file or through Swagger UI.

The input format complies with the A2A specification. You can provide values for:
- `messageId` - A unique identifier for this specific message. You can create your own ID (e.g., a GUID) or set it to `null` to let the agent generate one automatically.
- `contextId` - The conversation identifier. Provide your own ID to start a new conversation or continue an existing one by reusing a previous `contextId`. The agent will maintain conversation history for the same `contextId`. Agent will generate one for you as well, if none is provided.

```http
# Send A2A request to the pirate agent
POST {{baseAddress}}/a2a/pirate/message:send
Content-Type: application/json
{
  "message": {
    "role": "ROLE_USER",
    "parts": [
      {
        "text": "Hey pirate! Tell me where have you been"
      }
    ],
    "messageId": null,
    "contextId": "foo"
  }
}
```
_Note: Replace `{{baseAddress}}` with your server endpoint. To stream the response as server-sent events, send the same request to `{{baseAddress}}/a2a/pirate/message:stream`._

This request returns the following JSON response:
```json
{
  "message": {
    "role": "ROLE_AGENT",
    "parts": [
      {
        "text": "Arrr, ye scallywag! Ye’ll have to tell me what yer after, or be I walkin’ the plank? 🏴‍☠️"
      }
    ],
    "messageId": "e20b2618a5504913815bc513ce315cd2",
    "contextId": "foo"
  }
}
```

The response includes the `contextId` (conversation identifier), `messageId` (message identifier), and the actual content from the pirate agent.

## AgentCard Configuration

The `AgentCard` provides metadata about your agent for discovery and integration. Publish it with `MapWellKnownAgentCard`, which the A2A SDK package (`A2A.AspNetCore`) provides:
```csharp
app.MapWellKnownAgentCard(new AgentCard
{
    Name = "My Agent",
    Description = "A helpful agent that assists with tasks.",
    Version = "1.0",
    SupportedInterfaces =
    [
        new AgentInterface
        {
            Url = "http://localhost:5000/a2a/my-agent",
            ProtocolBinding = ProtocolBindingNames.HttpJson,
            ProtocolVersion = "1.0",
        }
    ]
});
```

You can access the agent card by sending this request:
```http
# Get the agent card
GET {{baseAddress}}/.well-known/agent-card.json
```
_Note: Replace `{{baseAddress}}` with your server endpoint._

### AgentCard Properties

- **Name**: Display name of the agent
- **Description**: Brief description of the agent
- **Version**: Version string for the agent
- **SupportedInterfaces**: The URL, protocol binding, and protocol version of each endpoint that serves the agent
- **Capabilities**: Optional metadata about streaming, push notifications, and other features

## Exposing Multiple Agents

You can expose multiple agents in a single application, as long as their endpoints don't collide. Register an A2A server for each agent, then map each one to its own path. Here's an example:

```csharp
var mathAgent = builder.AddAIAgent("math", instructions: "You are a math expert.");
var scienceAgent = builder.AddAIAgent("science", instructions: "You are a science expert.");

mathAgent.AddA2AServer();
scienceAgent.AddA2AServer();

var app = builder.Build();

app.MapA2AHttpJson(mathAgent, "/a2a/math");
app.MapA2AHttpJson(scienceAgent, "/a2a/science");
```

::: zone-end

::: zone pivot="programming-language-python"

The `agent-framework-a2a` package exposes an Agent Framework agent over the A2A protocol.

```bash
pip install agent-framework-a2a --pre
```

### Test a secured endpoint

Use an `AuthInterceptor` in a test client to verify a secured A2A endpoint:

```python
from a2a.client.auth.interceptor import AuthInterceptor

class BearerAuth(AuthInterceptor):
    def __init__(self, token: str):
        self.token = token

    async def intercept(self, request):
        request.headers["Authorization"] = f"Bearer {self.token}"
        return request

async with A2AAgent(
    name="secure-agent",
    url="https://secure-a2a-agent.example.com",
    auth_interceptor=BearerAuth("your-token"),
) as agent:
    response = await agent.run("Hello!")
```

## Exposing an Agent Framework agent over A2A

The `agent-framework-a2a` package provides an opinionated `A2AExecutor` that adapts any Agent Framework agent to the A2A server-side protocol. It runs the agent, maps supported output content to A2A events and artifacts, and manages task status updates through the official [`a2a-sdk`](https://pypi.org/project/a2a-sdk/).

Your application assembles the surrounding A2A SDK server: the agent card, `DefaultRequestHandler`, task store, routes or application builder, authentication, and deployment. For a comparison with the app-owned adapters and standalone conversion helpers in `agent-framework-hosting-a2a`, see [Self-host A2A agents](index.md).

```python
import uvicorn
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.routes import create_agent_card_routes, create_jsonrpc_routes
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentInterface, AgentSkill
from agent_framework import Agent
from agent_framework.a2a import A2AExecutor
from agent_framework.openai import OpenAIChatClient
from starlette.applications import Starlette

flight_skill = AgentSkill(
    id="Flight_Booking",
    name="Flight Booking",
    description="Search and book flights across Europe.",
    tags=["flights", "travel", "europe"],
    examples=[],
)

public_agent_card = AgentCard(
    name="Europe Travel Agent",
    description="Helps users search and book flights and hotels across Europe.",
    version="1.0.0",
    default_input_modes=["text"],
    default_output_modes=["text"],
    capabilities=AgentCapabilities(streaming=True),
    supported_interfaces=[
        AgentInterface(url="http://localhost:9999/", protocol_binding="JSONRPC"),
    ],
    skills=[flight_skill],
)

agent = Agent(
    client=OpenAIChatClient(),
    name="Europe Travel Agent",
    instructions="You are a helpful Europe Travel Agent.",
)

request_handler = DefaultRequestHandler(
    agent_executor=A2AExecutor(agent, stream=True),
    task_store=InMemoryTaskStore(),
    agent_card=public_agent_card,
)

server = Starlette(
    routes=[
        *create_agent_card_routes(public_agent_card),
        *create_jsonrpc_routes(request_handler, "/"),
    ]
)

uvicorn.run(server, host="0.0.0.0", port=9999)
```

`A2AExecutor` streams agent updates as A2A artifacts when the underlying agent supports streaming and propagates the A2A `context_id` as the agent session's `session_id`. You can subclass `A2AExecutor` and override the `handle_events` method to implement custom transformations from your agent's output format to A2A protocol events.

::: zone-end

::: zone pivot="programming-language-go"
## A2A Protocol

The Go Agent Framework supports hosting Agent Framework agents through the Agent-to-Agent (A2A) protocol with the `provider/a2aprovider` package and the official A2A Go server handlers.

Install the Agent Framework and A2A packages in your Go module:

```bash
go get github.com/microsoft/agent-framework-go
go get github.com/a2aproject/a2a-go/v2
```

### Host an agent via A2A

Create or reuse an Agent Framework agent, describe it with an A2A agent card, and expose it through one of the A2A transport bindings. In this example, `hostAgent` is any Agent Framework `*agent.Agent`; the server hosts a JSON-RPC endpoint at `/` and serves the agent card at the well-known A2A path.

```go
import (
    "fmt"
    "net/http"

    "github.com/a2aproject/a2a-go/v2/a2a"
    "github.com/a2aproject/a2a-go/v2/a2asrv"
    "github.com/microsoft/agent-framework-go/provider/a2aprovider"
)

url := "http://localhost:5000"

card := &a2a.AgentCard{
    Name:               "InvoiceAgent",
    Description:        "Handles requests relating to invoices.",
    Version:            "1.0.0",
    DefaultInputModes:  []string{"text"},
    DefaultOutputModes: []string{"text"},
    Capabilities: a2a.AgentCapabilities{
        Streaming: false,
    },
    SupportedInterfaces: []*a2a.AgentInterface{
        a2a.NewAgentInterface(url, a2a.TransportProtocolJSONRPC),
    },
}

mux := http.NewServeMux()
requestHandler := a2asrv.NewHandler(
    a2aprovider.NewExecutor(hostAgent, a2aprovider.ExecutorConfig{}),
    a2asrv.WithExtendedAgentCard(card),
)
mux.Handle("/", a2asrv.NewJSONRPCHandler(requestHandler))
mux.Handle(a2asrv.WellKnownAgentCardPath, a2asrv.NewStaticAgentCardHandler(card))

if err := http.ListenAndServe(":5000", mux); err != nil {
    panic(fmt.Errorf("A2A server failed: %w", err))
}
```

Wrap the same request handler with `a2asrv.NewRESTHandler` when you want to expose the HTTP+JSON transport binding. Set `ExecutorConfig.AllowBackgroundResponses` to `true` if the hosted agent should be allowed to return A2A tasks for long-running work.

::: zone-end
## See Also

- [Integrations Overview](../../../integrations/index.md)
- [A2A agent service](../../../integrations/by-component/agent-services/a2a.md)
- [OpenAI Integration](../openai-endpoints.md)
- [A2A Protocol Specification](https://a2a-protocol.org/latest/)
- [Agent Discovery](https://github.com/a2aproject/A2A/blob/main/docs/topics/agent-discovery.md)

## Next steps

> [!div class="nextstepaction"]
> [AG-UI Protocol](../../../integrations/by-component/ui/ag-ui/index.md)
