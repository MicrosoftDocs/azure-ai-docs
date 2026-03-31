---
title: "Quickstart: Deploy your first hosted agent"
description: "Learn how to deploy a containerized AI agent to Foundry Agent Service using the Azure Developer CLI or Microsoft Foundry for VS Code."
author: aahill
ms.author: aahi
ms.date: 03/12/2026
ms.manager: nitinme
ms.topic: quickstart
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.custom: mode-other, dev-focus, doc-kit-assisted
ai-usage: ai-assisted
zone_pivot_groups: hosted-agent-deploy-method
---

# Quickstart: Deploy your first hosted agent

In this quickstart, you deploy a containerized AI agent with Foundry tools to Foundry Agent Service. The sample agent uses web search and optionally MCP tools to answer questions. By the end, you have a running hosted agent that you can interact with through the Foundry playground. Choose your preferred deployment method to get started.

**In this quickstart, you:**

> [!div class="checklist"]
> * Set up an agent sample project with Foundry tools
> * Test the agent locally
> * Deploy to Foundry Agent Service
> * Interact with your agent in the playground
> * Clean up resources

## Prerequisites

Before you begin, you need:

* An Azure subscription - [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn)
* (Optional) An [MCP tool](../how-to/tools/model-context-protocol.md), if you have one you want to use.
* [Python 3.10 or later](https://www.python.org/downloads/)

:::zone pivot="azd"
* [Azure Developer CLI](/azure/developer/azure-developer-cli/install-azd) version 1.23.0 or later
* [Docker Desktop](https://docs.docker.com/get-docker/) installed and running
:::zone-end

:::zone pivot="vscode"
* [Visual Studio Code](https://code.visualstudio.com/)
* [Microsoft Foundry for Visual Studio Code extension](https://marketplace.visualstudio.com/items?itemName=TeamsDevApp.vscode-ai-foundry)
:::zone-end

> [!NOTE]
> Hosted agents are currently in preview.

:::zone pivot="azd"

## Step 1: Set up the sample project

Initialize a new project with the Foundry starter template and configure it with the agent-with-foundry-tools sample.

1. Initialize the starter template in an empty directory:

    ```bash
    azd init -t https://github.com/Azure-Samples/azd-ai-starter-basic
    ```

    This interactive command prompts you for an environment name (for example, `my-hosted-agent`). The environment name determines your resource group name (`rg-my-hosted-agent`).

    > [!NOTE]
    > If a resource group with the same name already exists, `azd provision` uses the existing group. To avoid conflicts, choose a unique environment name or delete the existing resource group first.

1. Initialize the agent sample:

    ```bash
    azd ai agent init -m https://github.com/microsoft-foundry/foundry-samples/blob/main/samples/python/hosted-agents/agent-framework/agent-with-foundry-tools/agent.yaml
    ```

    This interactive command prompts you for the following configuration values:

    - **Azure subscription** - select the Azure subscription where you want the Foundry resources to be created.
    - **Location** - select a region for the resources
    - **Model SKU** - select the SKU available for your region and subscription
    - **Deployment name** - enter a name for the model deployment
    - **Container memory** - enter a value for the memory allocation of the container or accept the defaults
    - **Container CPU** - enter a value for the CPU allocation of the container or accept the defaults
    - **Minimum replicas** - enter a value for the minimum replicas of the container
    - **Max replicas** - enter a value for the maximum replicas of the container

    > [!IMPORTANT]
    > If you aren't using an MCP server, comment out or remove the following lines in the `agent.yaml` file:
    >
    > ```yaml
    > - name: AZURE_AI_PROJECT_TOOL_CONNECTION_ID
    >   value: <CONNECTION_ID_PLACEHOLDER>
    > ```

1. Provision the required Azure resources:

    > [!NOTE]
    > You need **Contributor** access on your Azure subscription for resource provisioning.

    ```bash
    azd provision
    ```

    This command takes about 5 minutes and creates the following resources:

    | Resource | Purpose | Cost |
    | -------- | ------- | ---- |
    | Resource group | Organizes all related resources in the same area | No cost |
    | Model deployment | Model used by the agent | See [Foundry pricing](https://azure.microsoft.com/pricing/details/microsoft-foundry/) |
    | Foundry project | Hosts your agent and provides AI capabilities | Consumption-based; see [Foundry pricing](https://azure.microsoft.com/pricing/details/ai-foundry/) |
    | Azure Container Registry | Stores your agent container images | Basic tier; see [ACR pricing](https://azure.microsoft.com/pricing/details/container-registry/) |
    | Log Analytics Workspace | Manage all log data in one place | No direct cost. See [Log Analytics cost](/azure/azure-monitor/logs/log-analytics-workspace-overview) |
    | Application Insights | Monitors agent performance and logs | Pay-as-you-go; see [Azure Monitor pricing](https://azure.microsoft.com/pricing/details/monitor/) |
    | Managed identity | Authenticates your agent to Azure services | No cost |

    > [!TIP]
    > Run `azd down` when you finish this quickstart to delete resources and stop incurring charges.

## Step 2: Test the agent locally

Before deploying, verify the agent works locally.

1. Create and activate a Python virtual environment:

    **Bash:**

    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```

    **PowerShell:**

    ```powershell
    python -m venv .venv
    .venv\Scripts\Activate.ps1
    ```

1. Install dependencies:

    ```bash
    pip install -r ./src/af-agent-with-foundry-tools/requirements.txt
    ```

1. Copy the required environment variables used in the agent code to a local .env file:

    **Bash:**

    ```bash
    azd env get-values > .env
    ```

    **PowerShell:**

    ```powershell
    azd env get-values > .env
    ```

1. Add the `AZURE_OPENAI_CHAT_DEPLOYMENT_NAME` variable to your `.env` file with the name of the model deployment:

    `AZURE_OPENAI_CHAT_DEPLOYMENT_NAME="gpt-4.1"`

1. Run the agent locally:

    ```bash
    python ./src/af-agent-with-foundry-tools/main.py
    ```

    If the agent fails to start, check these common issues:

    | Error | Solution |
    | ----- | -------- |
    | `AuthenticationError` or `DefaultAzureCredential` failure | Run `azd auth login` again to refresh your session. |
    | `ResourceNotFound` | Verify your endpoint URLs match the values in the Foundry portal. |
    | `DeploymentNotFound` | Check the deployment name in **Build** > **Deployments**. |
    | `Connection refused` | Ensure no other process is using port 8088. |

1. Test with a REST client. The agent runs on `localhost:8088`:

    **Bash:**

    ```bash
    curl -X POST http://localhost:8088/responses \
        -H "Content-Type: application/json" \
        -d '{"input": "What is Microsoft Foundry?"}'
    ```

    **PowerShell:**

    ```powershell
    Invoke-RestMethod -Method Post `
        -Uri "http://localhost:8088/responses" `
        -ContentType "application/json" `
        -Body '{"input":"What is Microsoft Foundry?"}'
    ```

    You should see a response with web search results about Microsoft Foundry.

1. Stop the local server with **Ctrl+C**.

## Step 3: Deploy to Foundry Agent Service

The `azd up` command combines three steps into one: provisioning infrastructure, packaging your application, and deploying it to Azure. This is equivalent to running `azd provision`, `azd package`, and `azd deploy` separately.

Before you begin, verify that Docker Desktop is running:

```bash
docker info
```

If this command fails, start Docker Desktop and wait for it to initialize before continuing.

Deploy your agent:

```bash
azd up
```

The first deployment will take longer because Docker needs to build the image.

> [!WARNING]
> Your hosted agent incurs charges while deployed. After you finish testing, complete [Clean up resources](#clean-up-resources) to delete resources and stop charges.

When finished, you will see a link to the Agent Playground and the endpoint for the agent which can be used to invoke the agent programmatically.

```bash
Deploying services (azd deploy)
                                                                                                                                                                     
  (✓) Done: Deploying service af-agent-with-foundry-tools
  - Agent playground (portal): https://ai.azure.com/nextgen/.../build/agents/af-agent-with-foundry-tools/build?version=1 
  - Agent endpoint: https://ai-account-<name>.services.ai.azure.com/api/projects/<project>/agents/af-agent-with-foundry-tools/versions/1
```

:::zone-end

:::zone pivot="vscode"

## Step 1: Create a Foundry project

Use the Microsoft Foundry extension in VS Code to create a new Microsoft Foundry Project resource.

1. Open the Command Palette (**Ctrl+Shift+P**) and select **Microsoft Foundry: Create Project**.

1. Select your Azure subscription.

1. Create a new resource group or select an existing one.

1. Enter a name for the Foundry Project resource.

Once the project creation is complete, continue to the next step and deploy a model.

## Step 2: Deploy a model

Use the Microsoft Foundry extension in VS Code to deploy a model to Foundry.

1. Open the Command Palette (**Ctrl+Shift+P**) and select **Microsoft Foundry: Open Model Catalog**.

1. Browse the model catalog or search for gpt-4.1 and select the **Deploy** button.

1. In the Model deployment page, select the **Deploy to Microsoft Foundry** button.

Once the model is deployed successfully, move on to the next step and create a Hosted Agent project

## Step 3: Create a Hosted Agent project

Use the Microsoft Foundry extension in VS Code to scaffold a new hosted agent project.

1. Open the Command Palette (**Ctrl+Shift+P**) and select **Microsoft Foundry: Create new Hosted Agent**.

1. Select either the Single Agent or Multi-Agent Workflow template

1. Select a programming language, Python or C#.

1. Choose the existing gpt-4.1 model you deployed in the previous step.

1. Choose the folder where you want your project files to be saved.

1. Enter a name for the hosted agent.

A new VS Code window will launch with the new agent project folder as the active workspace.

## Step 4: Install dependencies

It's recommended to use a virtual environment to isolate project dependencies:

**macOS/Linux:**

```bash
python -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell):**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Installing Dependencies

Install the required Python dependencies using pip:

```bash
pip install -r requirements.txt
```

The required packages are:

- `azure-ai-agentserver-agentframework` - Agent Framework and AgentServer SDK

## Step 5: Test the agent locally

Run and test your agent before deploying.

#### Option 1: Press F5 (Recommended)

Press **F5** in VS Code to start debugging. Alternatively, you can use the VS Code debug menu:

1. Open the **Run and Debug** view (Ctrl+Shift+D / Cmd+Shift+D)
2. Select **"Debug Local Workflow HTTP Server"** from the dropdown
3. Click the green **Start Debugging** button (or press F5)

This will:

1. Start the HTTP server with debugging enabled
2. Open the AI Toolkit Agent Inspector for interactive testing
3. Allow you to set breakpoints and inspect the workflow

#### Option 2: Run in Terminal

Run as HTTP server (default):

```bash
python main.py
```

This will start the hosted agent locally on `http://localhost:8088/`.

**PowerShell (Windows):**

```powershell
$body = @{
   input = "I need a hotel in Seattle from 2025-03-15 to 2025-03-18, budget under `$200 per night"
    stream = $false
} | ConvertTo-Json

Invoke-RestMethod -Uri http://localhost:8088/responses -Method Post -Body $body -ContentType "application/json"
```

**Bash/curl (Linux/macOS):**

```bash
curl -sS -H "Content-Type: application/json" -X POST http://localhost:8088/responses \
   -d '{"input": "Find me hotels in Seattle for March 20-23, 2025 under $200 per night","stream":false}'
```

The agent will use the `get_available_hotels` tool to search for available hotels matching your criteria.


## Step 6: Deploy to Foundry Agent Service

Deploy your agent directly from VS Code.

1. Open the Command Palette (**Ctrl+Shift+P**) and select **Microsoft Foundry: Deploy Hosted Agent**.

1. Select the CPU and Memory configuration for the Hosted Agent container.

1. In the dialog that appears, select the Confirm and Deploy button.

Switch to the Microsoft Foundry explorer by selecting the icon on the left. The agent appears in the **Hosted Agents (Preview)** tree view sidebar after deployment completes.

:::zone-end

## Verify and test your agent

After deployment completes, verify your agent is running.

:::zone pivot="vscode"

### Check agent status

Check the status of your agent to confirm it's running.

1. Select your hosted agent from the Hosted Agents (Preview) tree view.

1. Select a version (v1) to open the detail page. 

The detail page shows the Status under the Container Details section.

### Test in the playground using VS Code

Microsoft Foundry for VS Code includes an integrated Playground to chat and interact with your agent. 

1. Select your hosted agent from the Hosted Agents (Preview) tree view.

1. Select a version (v1) to open the detail page. 

1. Select the Playground option and type a message and send to test your agent.

:::zone-end

### Test in the Foundry playground

Navigate to the agent in the Foundry portal:

1. Open the [Foundry portal](https://ai.azure.com) and sign in with your Azure account.

1. Select your project from the **Recent projects** list, or select **All projects** to find it.

1. In the left navigation, select **Build** to expand the menu, then select **Agents**.

1. In the agents list, find your deployed agent (it matches the agent name from your deployment).

1. Select the agent name to open its details page, then select **Open in playground** in the top toolbar.

1. In the chat interface, type a test message like "What is Microsoft Foundry?" and press **Enter**.

1. Verify that the agent responds with information from web search results. The response might take a few seconds as the agent queries external sources.

  > [!TIP]
  > If the playground doesn't load or the agent doesn't respond, verify the agent status is `Started` using the Container Details page described above.

## Clean up resources

To avoid charges, delete the resources when you're finished.

:::zone pivot="azd"

> [!WARNING]
> This command permanently deletes all Azure resources created in this quickstart, including the Foundry project, Container Registry, Application Insights, and your hosted agent. This action can't be undone.

To preview what will be deleted before confirming:

```bash
azd down --preview
```

When you're ready to delete, run:

```bash
azd down
```

The cleanup process takes approximately 2-5 minutes.

:::zone-end

:::zone pivot="vscode"

> [!WARNING]
> Deleting resources permanently removes all Azure resources created in this quickstart, including the Foundry project, Container Registry, Application Insights, and your hosted agent. This action can't be undone.

To delete your resources, open the [Azure portal](https://portal.azure.com), navigate to your resource group, and delete it along with all contained resources.

<!-- [TODO: Author VS Code or portal-based cleanup steps] -->

:::zone-end

To verify resources were deleted, open the [Azure portal](https://portal.azure.com), go to your resource group, and confirm the resources no longer appear. If the resource group is empty, you can delete it as well.

## Troubleshooting

If you encounter issues, try these solutions for common problems:

| Issue | Solution |
| ----- | -------- |
| Docker build errors | Ensure Docker Desktop is running. Run `docker info` to verify. |
| `SubscriptionNotRegistered` error | Register providers: `az provider register --namespace Microsoft.CognitiveServices` |
| `AuthorizationFailed` during provisioning | Request **Contributor** role on your subscription or resource group. |
| Agent doesn't start locally | Verify environment variables are set and run `az login` to refresh credentials. |
| `AcrPullUnauthorized` error | Grant **AcrPull** role to the project's managed identity on the container registry. |

:::zone pivot="azd"

| Issue | Solution |
| ----- | -------- |
| `azd init` fails | Run `azd version` to verify version 1.23.0+. Update with `winget upgrade Microsoft.Azd` (Windows) or `brew upgrade azd` (macOS). |
| Model not found in catalog | Fork the sample agent.yaml and change the model deployment to one available in your subscription like `gpt-4.1`. Then remove the `AZURE_LOCATION` value in the `.azure/<environment name>/.env` file. Re-run the `azd ai agent init` command with your forked `agent.yaml` file. |

:::zone-end

:::zone pivot="vscode"

### View the container logs of your agent

You can check the console and system logs of the container to troubleshoot issues.

1. Select your hosted agent from the Hosted Agents (Preview) tree view.

1. Select a version (v1) to open the detail page. 

1. Select the Logs button on the right to open the log viewer.

| Issue | Solution |
| ----- | -------- |
| Extension not found | Install the [Microsoft Foundry for VS Code extension](https://marketplace.visualstudio.com/items?itemName=TeamsDevApp.vscode-ai-foundry) from the VS Code Marketplace. |

:::zone-end

## What you learned

In this quickstart, you:

- Set up a hosted agent sample with Foundry tools (web search and MCP)
- Tested the agent locally
- Deployed to Foundry Agent Service
- Verified your agent in the Foundry playground

## Next steps

Now that you've deployed your first hosted agent, learn how to:

> [!div class="nextstepaction"]
> [Manage hosted agent lifecycle](../how-to/manage-hosted-agent.md)

Customize your agent with additional capabilities:
- [Connect MCP tools](../how-to/tools/model-context-protocol.md) to extend agent functionality
- [Use function calling](../how-to/tools/function-calling.md) to integrate custom logic
- [Add file search](../how-to/tools/file-search.md) to search your documents
- [Enable code interpreter](../how-to/tools/code-interpreter.md) to run Python code

You can see a full list of available tools in the [tool catalog](../concepts/tool-catalog.md) article.

## Related content

- [What are hosted agents?](../concepts/hosted-agents.md)
- [Deploy a hosted agent](../how-to/deploy-hosted-agent.md)
- [Agent development lifecycle](../concepts/development-lifecycle.md)
- [Python hosted agent samples](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/hosted-agents)
