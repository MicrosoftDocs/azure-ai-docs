---
title: "Quickstart: Deploy your own code as a hosted agent"
description: "Take your existing Python or .NET agent code, add one hosting library, and deploy to Foundry Agent Service with the Azure Developer CLI."
author: aahill
ms.author: aahi
ms.date: 07/23/2026
ms.manager: mcleans
ms.topic: quickstart
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.custom: mode-other, dev-focus, doc-kit-assisted
ai-usage: ai-assisted
#CustomerIntent: As a developer with existing agent code, I want to deploy it to Foundry Agent Service so that I can host my agent without rewriting it for a specific framework.
---

# Quickstart: Deploy your own code as a hosted agent

In [Deploy your first hosted agent](quickstart-hosted-agent.md), you deployed a sample. In this quickstart, you deploy **your own** Python or .NET (C#) agent code to Foundry Agent Service. Your code can use any agent framework - such as Microsoft Agent Framework, LangGraph, the GitHub Copilot SDK, or the OpenAI Agents SDK - or plain code that calls a model directly.

Each code step has tabs for your language and protocol. Select the same combination, such as **C# (Responses)**, in every step.

If you use a coding agent like GitHub Copilot, the [Microsoft Foundry Skill](../../how-to/develop/use-microsoft-foundry-skill.md) can help adapt the quickstart to your own codebase and run the right `azd` deployment steps.

## Prerequisites

Before you begin, you need:

* An Azure subscription--[Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
* If you have an existing Foundry project, you need `Foundry Project Manager` at project scope. If you need to create a new Foundry project, you need `Owner` role at resource group scope. For the full role matrix, see [Hosted agent permissions reference](../concepts/hosted-agent-permissions.md).
* [Azure Developer CLI (azd) 1.27.1 or later](/azure/developer/azure-developer-cli/install-azd).
* The `azd microsoft.foundry` extension:

    ```bash
    azd ext install microsoft.foundry
    ```

* An authenticated `azd` session:

    ```bash
    azd auth login
    ```

* Your existing agent code in a local directory.
* For the Python path, [Python 3.13 or later](https://www.python.org/downloads/).
* For the C# path, the [.NET 10 SDK or later](https://dotnet.microsoft.com/download/dotnet/10.0).
* (Optional) To start from a sample in Visual Studio Code, install [Visual Studio Code](https://code.visualstudio.com/) and the [Microsoft Foundry Toolkit for Visual Studio Code](https://aka.ms/foundrytk).

Your project directory should contain at minimum, for Python:

```
my-agent/
├── main.py              # Your agent entry point
└── requirements.txt     # Python dependencies
```

Or, for C#, a .NET web project:

```
my-agent/
├── Program.cs           # Your agent entry point
└── my-agent.csproj      # Project file (web SDK)
```

## Choose your framework

The hosting library you add in [Step 1](#step-1-add-the-hosting-library) handles the protocol - the HTTP server, health checks, and request and response schemas. It doesn't depend on a specific agent framework, so your agent logic can use any packages you prefer, in Python or C#.

To use a framework, add its packages next to the hosting library, then call the framework from the handler. The following table lists common choices and a Python sample for each.

| Framework | Packages to add to `requirements.txt` | Sample |
| --------- | ------------------------------------- | ------ |
| Plain Python (call a model directly) | `azure-ai-projects` | [hello-world](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/hosted-agents/bring-your-own/responses/hello-world) |
| LangGraph | `langgraph`, `langchain-azure-ai` | [langgraph-chat](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/hosted-agents/bring-your-own/responses/langgraph-chat) |
| GitHub Copilot SDK | `github-copilot-sdk` | [github-copilot](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/hosted-agents/bring-your-own/invocations/github-copilot) |
| OpenAI Agents SDK | `openai-agents` | [openai-agents-sdk](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/hosted-agents/bring-your-own/responses/openai-agents-sdk) |

Each sample's `requirements.txt` lists the exact package versions. For the full set of bring-your-own samples, see the [Python samples folder](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/hosted-agents/bring-your-own).

For C#, add framework packages to your project file next to the hosting package, then call the framework from the handler in `Program.cs`. For the full set of C# examples, see the [C# bring-your-own samples folder](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/csharp/hosted-agents/bring-your-own).

> [!NOTE]
> Microsoft Agent Framework has a built-in hosting integration that uses its own package. To deploy a Microsoft Agent Framework agent, see [Deploy your first hosted agent](quickstart-hosted-agent.md).

## Start from a sample in Visual Studio Code

To start from a working framework template instead of your own code, use the sample gallery in the Microsoft Foundry Toolkit for Visual Studio Code:

1. In the Visual Studio Code Activity Bar, select the **Foundry Toolkit** icon.
1. Under **Developer Tools** > **Agent Dev Tools**, select **Create Agent**.
1. Under **Create in code with full control**, select **Use a sample**.
1. On **Create Hosted Agent from Sample**, use the filters to narrow the gallery:
    - For **Framework**, select **Agent Framework**, **Bring Your Own**, **LangGraph**, or **Copilot SDK**.
    - For **Protocol Type**, select **Responses API** or **Invocations API**.
1. Select a sample, and then select **Next**.
1. Enter an agent name, select your Foundry project, and then select **Create**.

The toolkit scaffolds the sample into a new workspace and sets up a one-click **F5** debug experience. To install dependencies, test locally, and deploy from Visual Studio Code, follow the Visual Studio Code steps in [Deploy your first hosted agent](quickstart-hosted-agent.md).

## Choose your protocol

Each code step has a tab for every combination of language and protocol. **Responses** manages conversation history and is OpenAI-compatible. **Invocations** gives you full control over request and response schemas. Select the same language and protocol combination in every step.

> [!TIP]
> Not sure which protocol to use? Start with **Responses**.

## Step 1: Add the hosting library

Add the protocol library to your project. The library handles the HTTP server, health checks, and protocol compliance, independent of the agent framework you use. If you use a framework, add its packages alongside the hosting library - see [Choose your framework](#choose-your-framework).

# [Python (Responses)](#tab/python-responses)

Add the protocol library to your `requirements.txt`:

```text
azure-ai-agentserver-responses>=1.0.0b7
```

# [Python (Invocations)](#tab/python-invocations)

Add the protocol library to your `requirements.txt`:

```text
azure-ai-agentserver-invocations>=1.0.0b5
```

# [C# (Responses)](#tab/csharp-responses)

Create a .NET web project and add the protocol package:

```dotnetcli
dotnet new web --name my-agent
cd my-agent
dotnet add package Azure.AI.AgentServer.Responses --prerelease
```

# [C# (Invocations)](#tab/csharp-invocations)

Create a .NET web project and add the protocol package:

```dotnetcli
dotnet new web --name my-agent
cd my-agent
dotnet add package Azure.AI.AgentServer.Invocations --prerelease
```

---

## Step 2: Add the hosting wrapper

Create or update your agent entry point with the hosting wrapper. The following examples show the minimal pattern. Replace the marked block with your existing agent logic.

# [Python (Responses)](#tab/python-responses)

Create or update `main.py`:

```python
import asyncio
from azure.ai.agentserver.responses import (
    CreateResponse,
    ResponseContext,
    ResponsesAgentServerHost,
    TextResponse,
)

app = ResponsesAgentServerHost()


@app.response_handler
async def handler(
    request: CreateResponse,
    context: ResponseContext,
    _cancellation_signal: asyncio.Event,
):
    user_input = await context.get_input_text() or ""

    # ─── YOUR AGENT LOGIC HERE ───
    reply = f"Hello! You said: {user_input}"
    # ─────────────────────────────

    return TextResponse(context, request, text=reply)


app.run()
```

# [Python (Invocations)](#tab/python-invocations)

Create or update `main.py`:

```python
import json
from starlette.requests import Request
from starlette.responses import JSONResponse
from azure.ai.agentserver.invocations import InvocationAgentServerHost

app = InvocationAgentServerHost()


@app.invoke_handler
async def handle_invoke(request: Request):
    raw = (await request.body()).decode("utf-8").strip()
    try:
        body = json.loads(raw)
        user_message = (
            body.get("message") or body.get("input") or raw
        )
    except json.JSONDecodeError:
        user_message = raw

    # ─── YOUR AGENT LOGIC HERE ───
    reply = f"Hello! You said: {user_message}"
    # ─────────────────────────────

    return JSONResponse({"reply": reply})


if __name__ == "__main__":
    app.run()
```

# [C# (Responses)](#tab/csharp-responses)

Replace `Program.cs`:

```csharp
using Azure.AI.AgentServer.Responses;
using Azure.AI.AgentServer.Responses.Models;

ResponsesServer.Run<EchoHandler>();

public sealed class EchoHandler : ResponseHandler
{
    public override IAsyncEnumerable<ResponseStreamEvent> CreateAsync(
        CreateResponse request,
        ResponseContext context,
        CancellationToken cancellationToken)
    {
        return new TextResponse(context, request, createText: async ct =>
        {
            var userInput = await context.GetInputTextAsync(cancellationToken: ct) ?? "";

            // ─── YOUR AGENT LOGIC HERE ───
            var reply = $"Hello! You said: {userInput}";
            // ──────────────────────────────

            return reply;
        });
    }
}
```

# [C# (Invocations)](#tab/csharp-invocations)

Replace `Program.cs`:

```csharp
using System.Text.Json;
using Azure.AI.AgentServer.Invocations;
using Microsoft.AspNetCore.Http;

InvocationsServer.Run<EchoHandler>();

public sealed class EchoHandler : InvocationHandler
{
    public override async Task HandleAsync(
        HttpRequest request,
        HttpResponse response,
        InvocationContext context,
        CancellationToken cancellationToken)
    {
        var raw = (await new StreamReader(request.Body).ReadToEndAsync(cancellationToken)).Trim();

        string userMessage;
        try
        {
            var body = JsonDocument.Parse(raw).RootElement;
            userMessage =
                (body.TryGetProperty("message", out var m) ? m.GetString() : null)
                ?? (body.TryGetProperty("input", out var input) ? input.GetString() : null)
                ?? raw;
        }
        catch (JsonException)
        {
            userMessage = raw;
        }

        // ─── YOUR AGENT LOGIC HERE ───
        var reply = $"Hello! You said: {userMessage}";
        // ──────────────────────────────

        await response.WriteAsJsonAsync(new { reply }, cancellationToken);
    }
}
```

---

> [!NOTE]
> These examples echo user input to demonstrate the hosting wrapper. Replace the marked block with your own agent logic - model calls, RAG, or a framework like LangGraph or the GitHub Copilot SDK. For complete examples, see the [Python samples](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/hosted-agents/bring-your-own) and [C# samples](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/csharp/hosted-agents/bring-your-own).

## Step 3: Initialize the project

Run `azd ai agent init` from your agent source directory. The Azure Developer CLI detects your language from the project files:

# [Python (Responses)](#tab/python-responses)

```bash
azd ai agent init --protocol responses --deploy-mode code
```

# [Python (Invocations)](#tab/python-invocations)

```bash
azd ai agent init --protocol invocations --deploy-mode code
```

# [C# (Responses)](#tab/csharp-responses)

```bash
azd ai agent init --protocol responses --deploy-mode code
```

# [C# (Invocations)](#tab/csharp-invocations)

```bash
azd ai agent init --protocol invocations --deploy-mode code
```

---

The interactive flow prompts for:

* **Agent name**: Customize the name or accept the default.
* **Foundry Project**: Select **Use an existing Foundry project** or **Create a new Foundry project**.
* **Subscription**: Select your Azure subscription.
* **Location**: Select an Azure region.

When complete, you see: **AI agent definition added to your azd project successfully!**

## Step 4: Provision Azure resources

```bash
azd provision
```

This creates the required Azure resources, such as Application Insights.

## Step 5: Test the agent locally

```bash
azd ai agent run
```

This command creates a virtual environment (Python) or restores and builds the project (C#), installs dependencies, and launches your agent. It also opens the agent inspector in your browser so you can chat with the agent.

You can also invoke from the CLI in a separate terminal:

```bash
azd ai agent invoke --local "Hello from my hosted agent"
```

## Step 6: Deploy to Foundry Agent Service

```bash
azd deploy
```

When the command finishes, the output shows links to the agent playground and the agent endpoint:

```output
Deploying services (azd deploy)

  Done: Deploying service my-agent
  - Agent playground (portal): https://ai.azure.com/.../build/agents/my-agent/build?version=1
  - Agent endpoint: https://ai-account-<name>.services.ai.azure.com/api/projects/<project>/agents/my-agent/versions/1
```

## Step 7: Invoke the deployed agent

```bash
azd ai agent invoke "Hello from my hosted agent"
```

You should see a response within a few seconds.

## Clean up resources

> [!WARNING]
> If the current `azd` environment created the Foundry project, `azd down` permanently deletes the project's resource group and everything in it. If you selected an existing project during initialization, `azd down` leaves the project, its resource group, the hosted agent, and other quickstart resources in place. Delete any resources you no longer need from the existing project separately.

```bash
azd down
```

## Troubleshooting

| Issue | Solution |
| ----- | -------- |
| `ModuleNotFoundError: azure.ai.agentserver` | Verify the protocol library is in `requirements.txt` and reinstall: `pip install -r requirements.txt`. |
| C#: `The type or namespace name 'AgentServer' could not be found` | Verify the protocol package is referenced (`dotnet add package Azure.AI.AgentServer.Responses --prerelease` or `Azure.AI.AgentServer.Invocations`) and that the project uses the web SDK (`dotnet new web`). |
| C#: `Cannot resolve scoped service ... Handler from root provider` on `dotnet run` | The default `dotnet new web` launch profile sets `ASPNETCORE_ENVIRONMENT=Development`, which enables strict scope validation. Use `azd ai agent run` to test (it runs in the hosted mode), or set `ASPNETCORE_ENVIRONMENT=Production` before `dotnet run`. |
| `FOUNDRY_PROJECT_ENDPOINT not set` | Use `azd ai agent run` (sets it automatically) instead of running the app directly. Or add it to your `.env` file. |
| `Connection refused` on local run | Ensure no other process is using port 8088. |
| `AuthorizationFailed` during deploy | You need `Foundry Project Manager` at project scope. |
| Agent stuck in `provisioning` | Run `azd ai agent show` to check status. First deploys can take 2–3 minutes while dependencies install. |
| `azd ai agent init` fails | Run `azd version` to verify 1.27.1 or later. Run `azd ext show azure.ai.agents` to verify 1.0.0-beta.4 or later. Upgrade with `azd ext upgrade azure.ai.agents`. |

For the full permission and role-assignment matrix, see [Hosted agent permissions reference](../concepts/hosted-agent-permissions.md).

## What you learned

In this quickstart, you:

* Added one hosting library to your existing agent code.
* Initialized an `azd` project from your source directory.
* Tested locally with `azd ai agent run` and `azd ai agent invoke --local`.
* Deployed to Foundry Agent Service with `azd deploy`.

## Next steps

> [!div class="nextstepaction"]
> [Manage hosted agent lifecycle](../how-to/manage-hosted-agent.md)

- [Build a toolbox and use it with a hosted agent](../how-to/tools/toolbox.md) to combine tools behind one managed endpoint.

## Related content

* [What are hosted agents?](../concepts/hosted-agents.md)
* [Deploy a hosted agent from source code](../how-to/deploy-hosted-agent-code.md)
* [Deploy a hosted agent from a container](../how-to/deploy-hosted-agent.md)
* [Agent development lifecycle](../concepts/development-lifecycle.md)
* [Python hosted agent samples](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/hosted-agents)
* [Bring-your-own framework samples (LangGraph, GitHub Copilot SDK, and more)](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/hosted-agents/bring-your-own)
* [C# hosted agent samples](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/csharp/hosted-agents)
