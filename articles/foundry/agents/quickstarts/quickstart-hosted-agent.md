---
title: "Quickstart: Deploy your first hosted agent"
description: "Learn how to deploy a containerized AI agent to Foundry Agent Service using the Azure Developer CLI or Microsoft Foundry Toolkit for Visual Studio Code extension."
author: aahill
ms.author: aahi
ms.date: 05/23/2026
ms.manager: nitinme
ms.topic: quickstart
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.custom: mode-other, dev-focus, doc-kit-assisted
ai-usage: ai-assisted
zone_pivot_groups: hosted-agent-deploy-method
---

# Quickstart: Deploy your first hosted agent

**In this quickstart, you:**

> [!div class="checklist"]
> * Scaffold a hosted agent project
> * Test the agent locally
> * Deploy to Foundry Agent Service
> * Chat with the agent in the playground
> * Clean up resources

Choose your preferred development experience to get started, VS Code or CLI.

> [!NOTE]
> This document is for Hosted Agents on the new backend and requires azd ai agent version 0.1.27-preview or later.
> For the legacy experience that uses Azure Container Apps, continue using 0.1.25-preview.
>
> Hosted agents are currently in preview.

## Prerequisites

Before you begin, you need:

* An Azure subscription--[Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
* The **Foundry Project Manager** role at project scope (or another role that grants both data-plane and role-assignment permissions). For the full role matrix, see [Hosted agent permissions reference](../concepts/hosted-agent-permissions.md).
* [Python 3.13 or later](https://www.python.org/downloads/).
* [Git](https://git-scm.com/downloads).
* (Optional) [GitHub Copilot for Azure plugin](https://github.com/microsoft/GitHub-Copilot-for-Azure) Recommended for coding agents and includes agent skills for creating, testing, and deploying hosted agents.

:::zone pivot="azd"

* [Azure Developer CLI (AZD) 1.25.3 or later](/azure/developer/azure-developer-cli/install-azd).
* The `azd ai foundry` extension. Install and verify the extension after AZD is installed:

    ```
    azd ext install azure.ai.foundry
    ```

* Sign in to Azure:

    ```
    azd auth login
    ```

:::zone-end

:::zone pivot="vscode"

* [Visual Studio Code](https://code.visualstudio.com/).
* [Microsoft Foundry Toolkit for Visual Studio Code](https://aka.ms/foundrytk).

:::zone-end

## Required permissions

You need the **Foundry Project Manager** role at project scope to create and deploy hosted agents. The Azure Developer CLI and the Visual Studio Code extension handle the remaining role assignments (project managed identity, agent identity, and Azure Container Registry (ACR) pull) automatically when you also have **Owner** or **User Access Administrator** on the subscription. If you don't have those subscription-level roles, ask an administrator to assign the roles described in [Hosted agent permissions reference](../concepts/hosted-agent-permissions.md).

[!INCLUDE [role-rename-note](../../includes/role-rename-note.md)]

:::zone pivot="azd"

## Step 1: Scaffold the sample project

Initialize a new hosted agent project using the basic Agent Framework sample manifest:

```
azd ai agent init -m "https://github.com/microsoft-foundry/foundry-samples/blob/main/samples/python/hosted-agents/agent-framework/responses/01-basic/agent.manifest.yaml"
```

The interactive flow prompts for:

* **Agent name**: Customize the name or accept the default, **agent-framework-agent-basic-responses**
* **Foundry Project**: Select **Create a new Foundry project**
* **Tenant**: Select your Azure tenant
* **Subscription**: Select your Azure subscription
* **Location**: Select an Azure region
* **Model**: Select the default, **gpt-4.1-mini**, or another model you can access.
* **Model Version**: Select the default option.
* **Model SKU**: Select an option with available quota that isn't Batch, usually **Standard** or **GlobalStandard**
* **Deployment capacity**: Select the default, **10**
* **Deployment name**: Select the default, **gpt-4.1-mini**

When complete, you should see **AI agent definition added to your azd project successfully!**.

### Non-interactive commands

You can also use the `--no-prompt` flag to run `init` in a non-interactive environment, like a coding agent:

```
azd ai agent init -m "https://github.com/microsoft-foundry/foundry-samples/blob/main/samples/python/hosted-agents/agent-framework/responses/01-basic/agent.manifest.yaml" --no-prompt
```

Before continuing, set AZURE_SUBSCRIPTION_ID and AZURE_LOCATION:

```
azd env set AZURE_SUBSCRIPTION_ID <subscription-id>
azd env set AZURE_LOCATION <region>
```

You can configure model deployments by editing the `config` section in `azure.yaml`: 

```yaml
deployments:
    - name: <deployment-name>
      model:
        name: <model-name>
        format: OpenAI
        version: <model-version>
      sku:
        name: GlobalStandard
        capacity: 1
```        


## Step 2: Provision Azure resources

Provision the resources defined in `azure.yaml`:

```
azd provision
```

This step takes a few minutes and creates the following resources. To run provision and deploy together, you can use `azd up` instead.

| Resource | Purpose | Cost |
| -------- | ------- | ---- |
| Resource group | Container for the other resources | No cost |
| Model deployment | Model used by the agent | See [Foundry pricing](https://azure.microsoft.com/pricing/details/microsoft-foundry/) |
| Foundry project | Hosts the agent | Consumption-based; see [Foundry pricing](https://azure.microsoft.com/pricing/details/ai-foundry/) |
| Azure Container Registry | Stores agent container images | Basic tier; see [ACR pricing](https://azure.microsoft.com/pricing/details/container-registry/) |
| Log Analytics workspace | Stores log data | See [Log Analytics cost](/azure/azure-monitor/logs/log-analytics-workspace-overview) |
| Application Insights | Monitors the agent | Pay-as-you-go; see [Azure Monitor pricing](https://azure.microsoft.com/pricing/details/monitor/) |
| Managed identity | Authenticates the agent to Azure services | No cost |

## Step 3: Test the agent locally

1. Start the agent:

    ```
    azd ai agent run --no-inspector
    ```

    This command creates a virtual environment, installs dependencies, and launches the agent using the `startupCommand` defined in `azure.yaml`. Preview packages can produce pip dependency version-conflict warnings during setup. These warnings are nonblocking. The agent starts and responds correctly despite them.

1. In a separate terminal, send a test prompt:

    ```
    azd ai agent invoke --local "Write a haiku about deploying cloud applications."
    ```

    You should see a haiku response from the agent.

## Step 4: Deploy to Foundry Agent Service

Build and deploy the agent container:

```
azd deploy
```

When the command finishes, the output shows links to the agent playground and the agent endpoint:

```output
Deploying services (azd deploy)

  Done: Deploying service basic-agent
  - Agent playground (portal): https://ai.azure.com/.../build/agents/basic-agent/build?version=1
  - Agent endpoint: https://ai-account-<name>.services.ai.azure.com/api/projects/<project>/agents/basic-agent/versions/1
```

:::zone-end

:::zone pivot="vscode"

## Step 1: Create a Foundry project

1. Open the Command Palette (**Ctrl+Shift+P**) and select **Foundry Toolkit: Create Project**.
1. Select your Azure subscription.
1. Create a new resource group or select an existing one.
1. Enter a name for the Foundry project.

## Step 2: Deploy a model

1. Open the Command Palette and select **Foundry Toolkit: Open Model Catalog**.
1. Search for `gpt-4.1` and select **Deploy**.
1. On the model deployment page, select **Deploy to Microsoft Foundry**.

## Step 3: Create a hosted agent project

1. Open the Command Palette and select **Foundry Toolkit: Create new Hosted Agent**.
1. Select the **Python** as the language.
1. For "Framework", select **Agent Framework**.
1. Select **Responses API** as the protocol type.
1. Select **Basic** as the sample code.
1. Select the "Next" button.
1. Choose a folder for the project files and enter a name for the agent.
1. For "Environment Setup", choose **Set up with Microsoft Foundry**, the content should auto-populate with the project and model you created in step 1 and 2.
1. Select the "Create" button.

A new VS Code window opens with the project as the active workspace.

## Step 4: Install dependencies

Create a virtual environment and install the requirements.

For macOS or Linux:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

For Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Step 5: Test the agent locally

Press **F5** to start the local HTTP server with debugging enabled. The Foundry Toolkit Agent Inspector opens for interactive testing, and you can set breakpoints in your code.

To run the server without debugging:

```bash
python main.py
```

The agent listens on `http://localhost:8088/`. Send a test prompt with curl (or any HTTP client):

```bash
curl -sS -H "Content-Type: application/json" -X POST http://localhost:8088/responses \
    -d '{"input": "Write a haiku about deploying cloud applications.", "stream": false}'
```

## Step 6: Deploy to Foundry Agent Service

1. Open the Command Palette and select **Foundry Toolkit: Deploy Hosted Agent**. A deployment webview will open.
1. For "Deployment Method", select **Code**.
1. Select **Remote** as the package mode.
1. The "Agent Name" should auto-populate.
1. Select the "Next" button.
1. This "Review and Deploy" page should all auto-populate.
1. Select the "Deploy" button.

When deployment completes, the agent appears under **Hosted Agents (Preview)** in the Foundry Toolkit explorer.

:::zone-end

## Verify and test your agent

:::zone pivot="azd"

1. Check the agent status:

    ```
    azd ai agent show
    ```

    Verify that the agent is "Active".

1. Send the same prompt to the deployed agent:

    ```
    azd ai agent invoke "Write a haiku about deploying cloud applications."
    ```

    You should see a haiku response within a few seconds.

1. (Optional) Stream container logs while you interact with the agent:

    ```
    azd ai agent monitor --follow
    ```

    The platform injects an Application Insights connection string into the container, so OpenTelemetry traces also appear in the Application Insights resource provisioned earlier. View them in the [Azure portal](https://portal.azure.com) under **Investigate** > **Transaction search** or **Performance**.

:::zone-end

:::zone pivot="vscode"

1. In the Foundry Toolkit explorer, expand **Hosted Agents (Preview)** and select your agent. The detail page shows the status under **Deployment Details**.
1. Select the **Playground** tab and send a test prompt such as `Write a haiku about deploying cloud applications.`.

:::zone-end

## Test in the Foundry playground

The Foundry portal includes a shared playground you can use to test the agent.

1. Open the [Foundry portal](https://ai.azure.com) and sign in.
1. Select your project from **Recent projects** or **All projects**.
1. In the left navigation, select **Build** > **Agents**.
1. Select your agent, then select **Open in playground**.
1. Enter a prompt such as `Write a haiku about deploying cloud applications.` and press **Enter**. If the playground doesn't load or the agent doesn't respond, verify the agent status is `Started` on the agent detail page.

## Clean up resources

Delete the resources when you're finished so you stop incurring charges.

:::zone pivot="azd"

> [!WARNING]
> `azd down` permanently deletes every resource in the resource group, including the Foundry project, model deployments, Container Registry, Application Insights, and the hosted agent. If you provisioned into a resource group that contains other resources, those resources are deleted too.

```
azd down
```

`azd` lists the resources it deletes and prompts for confirmation. Cleanup takes about 2-5 minutes.

:::zone-end

:::zone pivot="vscode"

1. Open the [Azure portal](https://portal.azure.com) and navigate to the resource group that contains your agent.
1. Select **Delete resource group**, type the resource group name to confirm, and select **Delete**.

> [!WARNING]
> Deleting the resource group permanently removes everything in it, including the Foundry project, Container Registry, Application Insights, and the hosted agent.

:::zone-end

## Troubleshooting

| Issue | Solution |
| ----- | -------- |
| `SubscriptionNotRegistered` | Register the provider: `az provider register --namespace Microsoft.CognitiveServices`. |
| `AuthorizationFailed` during provisioning | Request the **Contributor** role on the subscription or resource group. |
| `AuthenticationError` or `DefaultAzureCredential` failure | To refresh credentials, run `azd auth logout` and then `azd auth login`. |
| `ResourceNotFound` or `DeploymentNotFound` | Verify the endpoint URL and model deployment name in the Foundry portal under **Build** > **Deployments**. |
| `AcrPullUnauthorized` | Grant the **AcrPull** role to the project's managed identity on the Container Registry. |
| `Connection refused` on local run | Ensure no other process is using port 8088. |
| `azd ai agent init` fails | Run `azd version` to verify 1.25.0 or later. Update with `winget upgrade Microsoft.Azd` (Windows) or `brew upgrade azd` (macOS). Run `azd ext list` and upgrade the agent extension with `azd ext upgrade azure.ai.agents` to get 0.1.34-preview or later. |
| Microsoft Foundry Toolkit extension not found | Install the [Microsoft Foundry Toolkit for Visual Studio Code](https://aka.ms/foundrytk) from the Marketplace and switch to the prerelease channel. |
| Local run fails on Windows ARM64 with build errors for `aiohttp`, `grpcio`, `cryptography`, or `httptools` | Prebuilt arm64 wheels aren't published for these packages, and source builds require Microsoft C++ Build Tools. As a workaround, skip Step 3 and validate the agent remotely with `azd deploy` followed by `azd ai agent invoke`. |

For the full permission and role-assignment matrix, see [Hosted agent permissions reference](../concepts/hosted-agent-permissions.md).

## What you learned

In this quickstart, you:

* Scaffolded a hosted agent project from the Basic agent sample.
* Tested the agent locally.
* Deployed the agent to Foundry Agent Service.
* Sent test prompts from both the CLI (or VS Code) and the Foundry playground.

## Next steps

> [!div class="nextstepaction"]
> [Manage hosted agent lifecycle](../how-to/manage-hosted-agent.md)

Customize your agent with additional capabilities:

- [Add web search](../how-to/tools/web-search.md) to ground responses in real-time public web results.
- [Connect MCP tools](../how-to/tools/model-context-protocol.md) to extend agent functionality
- [Use function calling](../how-to/tools/function-calling.md) to integrate custom logic
- [Add file search](../how-to/tools/file-search.md) to search your documents
- [Enable code interpreter](../how-to/tools/code-interpreter.md) to run Python code
- See the [tool catalog](../concepts/tool-catalog.md) for the full list.

Use the Microsoft Foundry Skill in your coding agent to standardize deployment,
evaluation, and troubleshooting workflows.

- [Use the Microsoft Foundry Skill in coding agents](../../how-to/develop/use-microsoft-foundry-skill.md)

## Related content

* [What are hosted agents?](../concepts/hosted-agents.md)
* [Deploy a hosted agent](../how-to/deploy-hosted-agent.md)
* [Agent development lifecycle](../concepts/development-lifecycle.md)
* [Python hosted agent samples](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/hosted-agents)
