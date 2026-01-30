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
* A [Microsoft Foundry project](../../../how-to/create-projects.md) with:
  * An Azure OpenAI model deployment (for example `gpt-4.1`)
  * (Optional) An MCP tool connection configured in the [Foundry tool catalog](https://ai.azure.com)
* [Azure Developer CLI](/azure/developer/azure-developer-cli/install-azd) version 1.23.0 or later
* [Azure CLI](/cli/azure/install-azure-cli) version 2.80 or later
* [Docker Desktop](https://docs.docker.com/get-docker/) installed and running
* [Python 3.10 or later](https://www.python.org/downloads/)

> [!NOTE]
> Hosted agents are currently in preview.

## Step 1: Set up the sample project

Initialize a new project with the Foundry starter template and configure it with the agent-with-foundry-tools sample:

1. Initialize the starter template:

    ```bash
    azd init -t https://github.com/Azure-Samples/azd-ai-starter-basic
    ```

    When prompted, enter a name for your environment (for example, `my-hosted-agent`). This name creates a resource group called `rg-my-hosted-agent`.

1. Initialize the agent sample:

    ```bash
    azd ai agent init -m https://github.com/microsoft-foundry/foundry-samples/blob/main/samples/python/hosted-agents/agent-framework/agent-with-foundry-tools/agent.yaml
    ```

    When prompted, configure the following values:
    - **AZURE_OPENAI_ENDPOINT**: Your Azure OpenAI endpoint URL
    - **AZURE_OPENAI_CHAT_DEPLOYMENT_NAME**: Your model deployment name (for example, `gpt-4.1`)
    - **AZURE_AI_PROJECT_ENDPOINT**: Your Foundry project endpoint
    - **AZURE_AI_PROJECT_TOOL_CONNECTION_ID** (optional): Your MCP tool connection ID

1. Provision the required Azure resources:

    ```bash
    azd provision
    ```

    This command creates the Foundry project, Container Registry, and Application Insights resources needed for deployment.

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
    export AZURE_OPENAI_CHAT_DEPLOYMENT_NAME="gpt-4.1"
    export AZURE_AI_PROJECT_ENDPOINT="https://your-project.services.ai.azure.com/api/projects/your-project"
    ```

    **PowerShell:**

    ```powershell
    $env:AZURE_OPENAI_ENDPOINT = "https://your-openai-resource.openai.azure.com/"
    $env:AZURE_OPENAI_CHAT_DEPLOYMENT_NAME = "gpt-4.1"
    $env:AZURE_AI_PROJECT_ENDPOINT = "https://your-project.services.ai.azure.com/api/projects/your-project"
    ```

1. Sign in to Azure:

    ```bash
    az login
    ```

1. Run the agent locally:

    ```bash
    python main.py
    ```

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

Deploy your agent with a single command:

```bash
azd up
```

This command:

1. Provisions Azure resources (Foundry project, Container Registry, Application Insights)
1. Builds your agent container image
1. Pushes the image to Azure Container Registry
1. Creates and starts your hosted agent

The deployment takes approximately 5-10 minutes.

> [!NOTE]
> You need **Contributor** access on your Azure subscription for resource provisioning.

## Step 4: Verify and test your agent

After deployment completes, verify your agent is running:

```bash
az cognitiveservices agent show \
    --account-name <your-account-name> \
    --project-name <your-project-name> \
    --name <your-agent-name>
```

Look for `status: Started` in the output.

### Test in the Foundry playground

1. Open the [Foundry portal](https://ai.azure.com).

1. Navigate to your project.

1. Select **Build** > **Agents**.

1. Find your deployed agent and select **Open in playground**.

1. Ask a question like "What is Microsoft Foundry?" to test your agent's web search capability.

## Step 5: Clean up resources

To avoid charges, delete the resources when you're finished:

```bash
azd down
```

This command removes all Azure resources created during deployment. The cleanup process takes approximately 10-20 minutes.

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

## Related content

- [What are hosted agents?](../concepts/hosted-agents.md)
- [Deploy a hosted agent](../how-to/deploy-hosted-agent.md)
- [Agent development lifecycle](../concepts/development-lifecycle.md)
- [Python hosted agent samples](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/hosted-agents)
