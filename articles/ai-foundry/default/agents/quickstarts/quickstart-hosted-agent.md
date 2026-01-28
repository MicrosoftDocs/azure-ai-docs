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

In this quickstart, you deploy a containerized AI agent to Foundry Agent Service. By the end, you have a running hosted agent that you can interact with through the Foundry playground.

**In this quickstart, you:**

> [!div class="checklist"]
> * Clone a sample hosted agent project
> * Test the agent locally
> * Deploy to Foundry Agent Service
> * Interact with your agent in the playground
> * Clean up resources

## Prerequisites

Before you begin, you need:

* An Azure subscription - [Create one for free](https://azure.microsoft.com/free/)
* [Azure Developer CLI](/azure/developer/azure-developer-cli/install-azd) version 1.11.0 or later
* [Docker Desktop](https://docs.docker.com/get-docker/) installed and running
* [Python 3.9 or later](https://www.python.org/downloads/)

> [!NOTE]
> Hosted agents are currently in preview and available only in **North Central US**.

## Step 1: Clone the sample project

Clone a sample hosted agent project that's configured for deployment:

```bash
azd init -t https://github.com/Azure-Samples/azd-ai-starter-basic
```

When prompted, enter a name for your environment (for example, `my-hosted-agent`). This name creates a resource group called `rg-my-hosted-agent`.

Navigate to the project directory:

```bash
cd my-hosted-agent
```

## Step 2: Test the agent locally

Before deploying, verify the agent works locally.

1. Create and activate a Python virtual environment:

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

1. Install dependencies:

    ```bash
    pip install azure-ai-agentserver-agentframework
    ```

1. Run the agent locally:

    ```bash
    python src/agent.py
    ```

1. Test with a REST client. The agent runs on `localhost:8088`:

    ```bash
    curl -X POST http://localhost:8088/responses \
        -H "Content-Type: application/json" \
        -d '{"input": {"messages": [{"role": "user", "content": "Hello!"}]}}'
    ```

    You should see a response like:

    ```json
    {
        "id": "resp_abc123",
        "status": "completed",
        "output": [{"type": "message", "role": "assistant", "content": "Hello! How can I help you today?"}]
    }
    ```

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
azd ai agent show --name <your-agent-name>
```

Look for `status: Started` in the output.

### Test in the Foundry playground

1. Open the [Foundry portal](https://ai.azure.com).

1. Navigate to your project.

1. Select **Build** > **Agents**.

1. Find your deployed agent and select **Open in playground**.

1. Send a message to test your agent.

    :::image type="content" source="../../media/agents/hosted-agent-playground.png" alt-text="Screenshot showing a hosted agent responding in the Foundry playground." lightbox="../../media/agents/hosted-agent-playground.png":::

## Step 5: Clean up resources

To avoid charges, delete the resources when you're finished:

```bash
azd down
```

This command removes all Azure resources created during deployment. The cleanup process takes approximately 10-20 minutes.

## What you learned

In this quickstart, you:

- Cloned a sample hosted agent project
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
- [Python code samples](https://github.com/azure-ai-foundry/foundry-samples/tree/main/samples/python/hosted-agents)
