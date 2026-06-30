---
title: "Quickstart: Deploy your own code as a hosted agent"
description: "Take your existing Python agent code, add one hosting library, and deploy to Foundry Agent Service with the Azure Developer CLI."
author: aahill
ms.author: aahi
ms.date: 06/25/2026
ms.manager: mcleans
ms.topic: quickstart
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.custom: mode-other, dev-focus, doc-kit-assisted
ai-usage: ai-assisted
#CustomerIntent: As a developer with existing agent code, I want to deploy it to Foundry Agent Service so that I can host my agent without rewriting it for a specific framework.
---

# Quickstart: Deploy your own code as a hosted agent

> [!NOTE]
> Hosted agents are currently in preview.

In [Deploy your first hosted agent](quickstart-hosted-agent.md), you deployed a sample. In this quickstart, you deploy **your own** Python agent code to Foundry Agent Service. Your code can use any agent framework - such as Microsoft Agent Framework, LangGraph, the GitHub Copilot SDK, or the OpenAI Agents SDK - or plain Python that calls a model directly.

## Prerequisites

Before you begin, you need:

* An Azure subscription--[Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
* If you have an existing Foundry project, you need `Foundry Project Manager` at project scope. If you need to create a new Foundry project, you need `Owner` role at resource group scope. For the full role matrix, see [Hosted agent permissions reference](../concepts/hosted-agent-permissions.md).
* [Azure Developer CLI (AZD) 1.25.3 or later](/azure/developer/azure-developer-cli/install-azd).
* The `azd microsoft.foundry` extension:

    ```bash
    azd ext install microsoft.foundry
    ```

* Your existing agent code in a local directory.
* [Python 3.13 or later](https://www.python.org/downloads/).
* (Optional) To start from a sample in Visual Studio Code, install [Visual Studio Code](https://code.visualstudio.com/) and the [Microsoft Foundry Toolkit for Visual Studio Code](https://aka.ms/foundrytk).

Your project directory should contain at minimum:

```
my-agent/
├── main.py              # Your agent entry point
└── requirements.txt     # Python dependencies
```

## Choose your framework

The hosting library you add in [Step 1](#step-1-add-the-hosting-library) handles the protocol - the HTTP server, health checks, and request and response schemas. It doesn't depend on a specific agent framework, so your agent logic can use any Python packages you prefer.

To use a framework, add its packages to `requirements.txt` next to the hosting library, then call the framework from the handler in `main.py`. The following table lists common choices and a sample for each.

| Framework | Packages to add to `requirements.txt` | Sample |
| --------- | ------------------------------------- | ------ |
| Plain Python (call a model directly) | `azure-ai-projects` | [hello-world](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/hosted-agents/bring-your-own/responses/hello-world) |
| LangGraph | `langgraph`, `langchain-azure-ai` | [langgraph-chat](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/hosted-agents/bring-your-own/responses/langgraph-chat) |
| GitHub Copilot SDK | `github-copilot-sdk` | [github-copilot](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/hosted-agents/bring-your-own/invocations/github-copilot) |
| OpenAI Agents SDK | `openai-agents` | [openai-agents-sdk](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/hosted-agents/bring-your-own/responses/openai-agents-sdk) |

Each sample's `requirements.txt` lists the exact package versions. For the full set of bring-your-own samples, see the [samples folder](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/hosted-agents/bring-your-own).

> [!NOTE]
> Microsoft Agent Framework has a built-in hosting integration that uses its own package. To deploy a Microsoft Agent Framework agent, see [Deploy your first hosted agent](quickstart-hosted-agent.md).

## Start from a sample in Visual Studio Code

To start from a working framework template instead of your own code, use the sample gallery in the Microsoft Foundry Toolkit for Visual Studio Code:

1. In the Visual Studio Code Activity Bar, select the **Foundry Toolkit** icon.
1. Under **Developer Tools** > **Agent Dev Tools**, select **Create Agent**.
1. Under **Create in code with full control**, select **Use a sample**.
1. On **Create Hosted Agent from Sample**, use the filters to narrow the gallery:
    - For **Framework**, select **Bring Your Own**, **LangGraph**, **Copilot SDK**, or **Agent Framework**.
    - For **Protocol Type**, select **Responses API** or **Invocations API**.
1. Select a sample, and then select **Next**.
1. Enter an agent name, select your Foundry project, and then select **Create**.

The toolkit scaffolds the sample into a new workspace and sets up a one-click **F5** debug experience. To install dependencies, test locally, and deploy from Visual Studio Code, follow the Visual Studio Code steps in [Deploy your first hosted agent](quickstart-hosted-agent.md).

## Choose your protocol

Select the tab that matches your agent's interaction pattern. **Responses** manages conversation history and is OpenAI-compatible. **Invocations** gives you full control over request and response schemas.

> [!TIP]
> Not sure which protocol to use? Start with **Responses**.

## Step 1: Add the hosting library

Add the protocol library to your `requirements.txt`. The library handles the HTTP server, health checks, and protocol compliance, independent of the agent framework you use. If you use a framework, add its packages to the same file - see [Choose your framework](#choose-your-framework).

# [Responses](#tab/responses)

```text
azure-ai-agentserver-responses>=1.0.0b7
```

# [Invocations](#tab/invocations)

```text
azure-ai-agentserver-invocations>=1.0.0b5
```

---

## Step 2: Add the hosting wrapper

Create or update `main.py` with the hosting wrapper. The examples show the minimal pattern—replace the marked block with your existing agent logic.

# [Responses](#tab/responses)

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

# [Invocations](#tab/invocations)

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

---

> [!NOTE]
> These examples echo user input to demonstrate the hosting wrapper. Replace the marked block with your own agent logic - model calls, RAG, or a framework like LangGraph or the GitHub Copilot SDK. For complete examples, see the [Python samples](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/hosted-agents/bring-your-own) and [C# samples](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/csharp/hosted-agents/bring-your-own).

## Step 3: Initialize the project

Run `azd ai agent init` from your agent source directory:

# [Responses](#tab/responses)

```bash
azd ai agent init --protocol responses --deploy-mode code
```

# [Invocations](#tab/invocations)

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

This command creates a virtual environment, installs dependencies, and launches your agent. It also opens the agent inspector in your browser so you can chat with the agent.

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
> `azd down` permanently deletes every resource in the resource group, including the Foundry project and hosted agent. If the resource group contains other resources, those are also deleted.

```bash
azd down
```

## Troubleshooting

| Issue | Solution |
| ----- | -------- |
| `ModuleNotFoundError: azure.ai.agentserver` | Verify the protocol library is in `requirements.txt` and reinstall: `pip install -r requirements.txt`. |
| `FOUNDRY_PROJECT_ENDPOINT not set` | Use `azd ai agent run` (sets it automatically) instead of `python main.py`. Or add it to your `.env` file. |
| `Connection refused` on local run | Ensure no other process is using port 8088. |
| `AuthorizationFailed` during deploy | You need `Foundry Project Manager` at project scope. |
| Agent stuck in `provisioning` | Run `azd ai agent show` to check status. First deploys can take 2–3 minutes while dependencies install. |
| `azd ai agent init` fails | Run `azd version` to verify 1.25.3 or later. Update the extension: `azd ext upgrade microsoft.foundry`. |

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
