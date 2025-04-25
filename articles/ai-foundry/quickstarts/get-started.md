---
title: Get started using the Azure AI Foundry SDK
titleSuffix: Azure AI Foundry
description: This article provides instructions on how to get started using the Azure AI Foundry SDK.
manager: scottpolly
ms.service: azure-ai-foundry
ms.custom: build-2024, devx-track-azurecli, devx-track-python, ignite-2024
ms.topic: how-to
ms.date: 04/07/2025
ms.reviewer: dantaylo
ms.author: sgilley
author: sdgilley
# zone_pivot_groups: project-type
# customer intent: As a developer, I want to build a custom chat app using the Azure AI SDK.
---

# Get started in Azure AI Foundry

In this quickstart, you use [Azure AI Foundry](https://ai.azure.com) to:

> [!div class="checklist"]
> * Create a project
> * Deploy a model
> * Run a chat completion
> * Run an agent

. The Azure AI Foundry SDK is available in multiple languages, including Python, Java, JavaScript, and C#. This quickstart provides instructions for each of these languages.

## Prerequisites

- An [Azure subscription](https://azure.microsoft.com/free/). If you don't have an Azure subscription, create a free account before you begin.

### Set up your environment  

# [Azure AI Foundry portal](#tab/azure-ai-studio)

No further installation necessary to use the Azure AI Foundry portal.

# [Python SDK](#tab/python)

1. [Set up your development environment](../how-to/develop/install-cli-sdk.md?tab-python)
1. Install these packages:

    ```
    install openai and azure-ai-projects packages
    pip install openai azure-ai-projects azure-identity
    ```

# [Java](#tab/java)

1. [Set up your development environment](../how-to/develop/install-cli-sdk.md?tab=java)
1. ??? 

# [JavaScript](#tab/javascript)

1. [Set up your development environment](../how-to/develop/install-cli-sdk.md?tab=javascript)
1. ??? 

# [C#](#tab/csharp)

1. [Set up your development environment](../how-to/develop/install-cli-sdk.md?tab-csharp)
1. ??? 

---

## Create a project 

# [Azure AI Foundry portal](#tab/azure-ai-studio)

[!INCLUDE [tip-left-pane](../includes/tip-left-pane.md)]
1. Sign in to the [Azure AI Foundry portal](https://ai.azure.com).
1. On the home page, select **Start building**.
1. Fill in a name for your project and select **Create**.  

# [Python SDK](#tab/python)
1. Install packages:
1. Create a project
    :::code language="python" source="~/foundry-samples/doc-samples/getting-started/python/create_project.py" id="create_project":::
# [Java](#tab/java)
Info here.
# [JavaScript](#tab/javascript)
Info here.
# [C#](#tab/csharp)
Info here.

---


## Deploy a model

@@Do we have to do this in portal?  

[!INCLUDE [tip-left-pane](../includes/tip-left-pane.md)]

1. Sign in to the [Azure AI Foundry portal](https://ai.azure.com).
1. If you aren't already in the project, select the project you just created. 
1. From the left pane, select **Model catalog**.
1. Search for the model you want to deploy.  For this quickstart, select **gpt-4o**.
1. Select **Use this model**.
1. Do not change the default settings.  Select **Deploy**.

## Run a chat completion

# [Azure AI Foundry portal](#tab/azure-ai-studio)

1. From the left pane, select **Playgrounds**. 
1. Select the model?
1. Fill in the prompt and select the **Send** button.
1. The model returns a response in the **Response** pane.

# [Python SDK](#tab/python)

:::code language="python" source="~/foundry-samples/doc-samples/getting-started/python/doc-samples/getting-started/python/quickstart.py" id="chat_completion":::


# [Java](#tab/java)
Info here.
# [JavaScript](#tab/javascript)
Info here.
# [C#](#tab/csharp)
Info here.

---

## Create and run an agent

# [Azure AI Foundry portal](#tab/azure-ai-studio)
Info here.
# [Python SDK](#tab/python)

:::code language="python" source="~/foundry-samples/doc-samples/getting-started/python/doc-samples/getting-started/python/quickstart.py" id="create_and_run_agent":::

# [Java](#tab/java)
Info here.
# [JavaScript](#tab/javascript)
Info here.
# [C#](#tab/csharp)
Info here.

---

## Add files to the agent

# [Azure AI Foundry portal](#tab/azure-ai-studio)
Info here.
# [Python SDK](#tab/python)

:::code language="python" source="~/foundry-samples/doc-samples/getting-started/python/doc-samples/getting-started/python/quickstart.py" id="ccreate_filesearch_agent":::

# [Java](#tab/java)
Info here.
# [JavaScript](#tab/javascript)
Info here.
# [C#](#tab/csharp)
Info here.

---

## Evaluate the agent run

# [Azure AI Foundry portal](#tab/azure-ai-studio)
Info here.
# [Python SDK](#tab/python)

:::code language="python" source="~/foundry-samples/doc-samples/getting-started/python/doc-samples/getting-started/python/quickstart.py" id="evaluate_agent_run":::

# [Java](#tab/java)
Info here.
# [JavaScript](#tab/javascript)
Info here.
# [C#](#tab/csharp)
Info here.

---


## Clean up resources

If you no longer need them, delete the resource group associated with your project.

In the Azure AI Foundry portal, select your project name in the top right corner.  Then select the link for the resource group to open it in the Azure portal.  Select the resource group, and then select **Delete**.  Confirm that you want to delete the resource group.

## Related content

What's next: explore models, knowledge retrieval, evaluation