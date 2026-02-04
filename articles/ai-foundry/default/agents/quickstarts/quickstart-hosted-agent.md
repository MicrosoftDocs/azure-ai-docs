---
title: "Quickstart: Deploy your first hosted agent"
titleSuffix: Microsoft Foundry
description: Learn how to deploy a containerized AI agent to Foundry Agent Service using the Azure Developer CLI.
author: aahill
ms.author: aahi
ms.date: 01/26/2026
ms.manager: nitinme
ms.topic: quickstart
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.custom: mode-other
ai-usage: ai-assisted
---

# Quickstart: Deploy your first hosted agent

In this quickstart, you deploy a containerized AI agent with Foundry tools to Foundry Agent Service. The sample agent uses web search and optionally MCP tools to answer questions. By the end, you have a running hosted agent that you can interact with through the Foundry playground.

**In this quickstart, you:**

> [!div class="checklist"]
> * Set up an agent sample project with Foundry tools
> * Test the agent locally
> * Deploy to Foundry Agent Service
> * Interact with your agent in the playground
> * Clean up resources

## Prerequisites

Before you begin, you need:

* An Azure subscription - [Create one for free](https://azure.microsoft.com/free/)
* A [Microsoft Foundry project](../../../default/tutorials/quickstart-create-foundry-resources.md) with:
  * An Azure OpenAI model deployment (for example `gpt-5`)
    * This example uses `gpt-5`, you may need to use another model (such as `gpt-4.1`) depending on your [quotas and limits](../../../agents/quotas-limits.md#quotas-and-limits-for-models).
  * (Optional) An [MCP tool](../how-to/tools/model-context-protocol.md), if you have one you want to use.
* An [Azure OpenAI resource](https://portal.azure.com/#create/Microsoft.CognitiveServicesOpenAI)
* [Azure Developer CLI](/azure/developer/azure-developer-cli/install-azd) version 1.23.0 or later
* [Azure CLI](/cli/azure/install-azure-cli) version 2.80 or later
* [Docker Desktop](https://docs.docker.com/get-docker/) installed and running
* [Python 3.10 or later](https://www.python.org/downloads/)

> [!NOTE]
> Hosted agents are currently in preview.

## Step 1: Set up the sample project

Initialize a new project with the Foundry starter template and configure it with the agent-with-foundry-tools sample.

1. Initialize the starter template:

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

    | Value | Description | How to find it |
    | ----- | ----------- | -------------- |
    | **AZURE_OPENAI_ENDPOINT** | Your Azure OpenAI endpoint URL | In the [Azure portal](https://portal.azure.com), go to your Azure OpenAI resource and copy the **Endpoint** from the **Keys and Endpoint** page. |
    | **AZURE_OPENAI_CHAT_DEPLOYMENT_NAME** | Your model deployment name (for example, `gpt-5`) | In the [Foundry portal](https://ai.azure.com), go to **Build** > **Deployments** and copy the deployment name. |
    | **AZURE_AI_PROJECT_ENDPOINT** | Your Foundry project endpoint | In the [Foundry portal](https://ai.azure.com), open your project, select **Overview**, and copy the **Project endpoint**. |
    | **AZURE_AI_PROJECT_TOOL_CONNECTION_ID** (optional) | Your MCP tool connection ID | In the [Foundry portal](https://ai.azure.com), go to **Management** > **Connected resources** and copy the connection ID for your MCP tool. |

    > [!IMPORTANT]
    > If you aren't using an MCP server, comment out or remove the following lines in the `agent.yaml` file:
    >
    > ```yaml
    > - name: AZURE_AI_PROJECT_TOOL_CONNECTION_ID
    >   value: <CONNECTION_ID_PLACEHOLDER>
    > ```

1. Provision the required Azure resources:

    ```bash
    azd provision
    ```

    This command takes 5-15 minutes and creates the following resources:

    | Resource | Purpose | Cost |
    | -------- | ------- | ---- |
    | Foundry project | Hosts your agent and provides AI capabilities | Consumption-based; see [Foundry pricing](https://azure.microsoft.com/pricing/details/ai-foundry/) |
    | Azure Container Registry | Stores your agent container images | Basic tier; see [ACR pricing](https://azure.microsoft.com/pricing/details/container-registry/) |
    | Application Insights | Monitors agent performance and logs | Pay-as-you-go; see [Azure Monitor pricing](https://azure.microsoft.com/pricing/details/monitor/) |

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
    pip install -r requirements.txt
    ```

1. Set the required environment variables:

    **Bash:**

    ```bash
    export AZURE_OPENAI_ENDPOINT="https://your-openai-resource.openai.azure.com/"
    export AZURE_OPENAI_CHAT_DEPLOYMENT_NAME="gpt-5"
    export AZURE_AI_PROJECT_ENDPOINT="https://your-project.services.ai.azure.com/api/projects/your-project"
    ```

    **PowerShell:**

    ```powershell
    $env:AZURE_OPENAI_ENDPOINT = "https://your-openai-resource.openai.azure.com/"
    $env:AZURE_OPENAI_CHAT_DEPLOYMENT_NAME = "gpt-5"
    $env:AZURE_AI_PROJECT_ENDPOINT = "https://your-project.services.ai.azure.com/api/projects/your-project"
    ```

1. Sign in to Azure:

    ```bash
    az login
    ```
1. Verify you’re logged in: 

    ```bash
    az account show
    ```
    > [!IMPORTANT]
    > Keep this session active while testing. The agent uses `DefaultAzureCredential`, which relies on your Azure CLI sign-in for local authentication.

1. Run the agent locally:

    ```bash
    python main.py
    ```

    If the agent fails to start, check these common issues:

    | Error | Solution |
    | ----- | -------- |
    | `AuthenticationError` or `DefaultAzureCredential` failure | Run `az login` again to refresh your session. |
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

The first deployment can take up to 15 minutes. Subsequent deployments are faster because infrastructure is already provisioned.

### What's being created

The deployment creates and configures the following Azure resources:

| Resource | Purpose |
| -------- | ------- |
| Foundry project | Hosts your agent and provides AI capabilities |
| Azure Container Registry | Stores your agent container images |
| Application Insights | Monitors agent performance and logs |
| Hosted agent endpoint | Runs your containerized agent |
| Managed identity | Authenticates your agent to Azure services |

> [!NOTE]
> You need **Contributor** access on your Azure subscription for resource provisioning.

> [!WARNING]
> Your hosted agent incurs charges while deployed. After you finish testing, complete [Step 5: Clean up resources](#step-5-clean-up-resources) to delete resources and stop charges.

## Step 4: Verify and test your agent

After deployment completes, verify your agent is running.

### Find your resource names

To use the Azure CLI verification command, you need the following values:

| Value | How to find it |
| ----- | -------------- |
| Account name | In the [Foundry portal](https://ai.azure.com), open your project and select **Overview**. The account name is the first part of your project endpoint URL (before `.services.ai.azure.com`). Alternatively, in the [Azure portal](https://portal.azure.com), go to your resource group and find the **Foundry** resource—its name is the account name. |
| Project name | In the [Foundry portal](https://ai.azure.com), open your project and copy the name from the **Overview** page. |
| Agent name | In the [Foundry portal](https://ai.azure.com), go to **Build** > **Agents**. The agent name appears in the list. |

You can also find these values in your azd output. After `azd up` completes, it displays the deployed resource names.

### Check agent status

Run the following command with your values:

```bash
az cognitiveservices agent show \
    --account-name <your-account-name> \
    --project-name <your-project-name> \
    --name <your-agent-name>
```

Look for `status: Started` in the output.

**If the status isn't "Started":**

| Status | Meaning | Action |
| ------ | ------- | ------ |
| `Provisioning` | Agent is still starting | Wait 2-3 minutes and check again. |
| `Failed` | Deployment error occurred | Run `azd deploy` to retry, or check logs in the Foundry portal. |
| `Stopped` | Agent was manually stopped | Run `az cognitiveservices agent start` to restart. |
| `Unhealthy` | Container is crashing | Check **View deployment logs** in the Foundry portal for errors. |

### Test in the Foundry playground

1. Open the [Foundry portal](https://ai.azure.com) and sign in with your Azure account.

1. Select your project from the **Recent projects** list, or select **All projects** to find it.

1. In the left navigation, select **Build** to expand the menu, then select **Agents**.

1. In the agents list, find your deployed agent (it matches the agent name from your deployment).

1. Select the agent name to open its details page, then select **Open in playground** in the top toolbar.

1. In the chat interface, type a test message like "What is Microsoft Foundry?" and press **Enter**.

1. Verify that the agent responds with information from web search results. The response might take a few seconds as the agent queries external sources.

> [!TIP]
> If the playground doesn't load or the agent doesn't respond, verify the agent status is `Started` using the CLI command above.

## Step 5: Clean up resources

To avoid charges, delete the resources when you're finished.

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

To verify resources were deleted, open the [Azure portal](https://portal.azure.com), go to your resource group (for example, `rg-my-hosted-agent`), and confirm the resources no longer appear. If the resource group is empty, you can delete it as well.

## Troubleshooting

If you encounter issues, try these solutions for common problems:

| Issue | Solution |
| ----- | -------- |
| `azd init` fails | Run `azd version` to verify version 1.23.0+. Update with `winget upgrade Microsoft.Azd` (Windows) or `brew upgrade azd` (macOS). |
| Docker build errors | Ensure Docker Desktop is running. Run `docker info` to verify. |
| `SubscriptionNotRegistered` error | Register providers: `az provider register --namespace Microsoft.CognitiveServices` |
| `AuthorizationFailed` during provisioning | Request **Contributor** role on your subscription or resource group. |
| Agent doesn't start locally | Verify environment variables are set and run `az login` to refresh credentials. |
| `AcrPullUnauthorized` error | Grant **AcrPull** role to the project's managed identity on the container registry. |

## What you learned

In this quickstart, you:

- Set up a hosted agent sample with Foundry tools (web search and MCP)
- Tested the agent locally using the hosting adapter
- Deployed to Foundry Agent Service using `azd up`
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
