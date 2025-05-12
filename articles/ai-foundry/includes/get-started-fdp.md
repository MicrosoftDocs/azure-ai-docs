---
title: Include file
description: Include file
author: sgilley
ms.author: sgilley
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 04/30/2025
ms.custom: include file
---

[!INCLUDE [fdp-rollout](fdp-rollout.md)]

In this quickstart, you use [Azure AI Foundry](https://ai.azure.com) to:

> [!div class="checklist"]
> * Create a project
> * Deploy a model
> * Run a chat completion
> * Create and run an agent
> * Upload files to the agent

The Azure AI Foundry SDK is available in multiple languages, including Python, Java, JavaScript, and C#. This quickstart provides instructions for each of these languages.

> [!TIP]
> The rest of this article shows how to use a **[!INCLUDE [fdp](../includes/fdp-project-name.md)]**. Select **[!INCLUDE [hub](../includes/hub-project-name.md)]** at the top of this article if you want to use a [!INCLUDE [hub](../includes/hub-project-name.md)] instead.

## Prerequisites

- An [Azure subscription](https://azure.microsoft.com/free/). If you don't have an Azure subscription, create a free account before you begin.
- You must be **Owner** of the subscription to receive the appropriate access control needed to use your project.

### Set up your environment  

# [Azure AI Foundry portal](#tab/azure-ai-foundry)

No installation is necessary to use the Azure AI Foundry portal.

# [Python SDK](#tab/python)

1. [Install Python and Azure CLI](../how-to/develop/install-cli-sdk.md?pivots=programming-language-python)
1. Install these packages:

    ```
    pip install openai azure-ai-projects azure-identity
    ```

1. Make sure to sign in using the CLI `az login` (or `az login --use-device-code`) command to authenticate before running your Python scripts.

> [!TIP]
> All the code in this article is at [GitHub Quickstart](https://github.com/azure-ai-foundry/foundry-samples/tree/main/samples/microsoft/python/mslearn-resources/quickstart).

# [Java](#tab/java)

1. [Install Java and Azure CLI](../how-to/develop/install-cli-sdk.md?pivots=programming-language-java).
1. Set these environment variables to use in your scripts:

    :::code language="text" source=" source="~/foundry-samples/samples/microsoft/java/mslearn-resources/quickstart/.env.template:::

1. Make sure to sign in using the CLI `az login` (or `az login --use-device-code`) command to authenticate before running your Java scripts.

> [!TIP]
> All the code in this article is at [GitHub Quickstart](https://github.com/azure-ai-foundry/foundry-samples/blob/main/samples/microsoft/java/mslearn-resources/quickstart).

# [JavaScript](#tab/javascript)

1. [Install JavaScript and Azure CLI](../how-to/develop/install-cli-sdk.md?pivots=programming-language-javascript)
1. Make sure to sign in using the CLI `az login` (or `az login --use-device-code`) command to authenticate before running your JavaScript scripts.
1. Download [package.json](https://github.com/azure-ai-foundry/foundry-samples/blob/main/samples/microsoft/javascript/mslearn-resources/quickstart/package.json).
1. Install packages with `npm install`
1. Set these environment variables to use in your scripts:

    :::code language="text" source=" source="~/foundry-samples/samples/microsoft/javascript/mslearn-resources/quickstart/.env.template:::


> [!TIP]
> All the code in this article is at [GitHub Quickstart](https://github.com/azure-ai-foundry/foundry-samples/tree/main/samples/microsoft/javascript/mslearn-resources/quickstart).

# [C#](#tab/csharp)

1. [Install C# and Azure CLI](../how-to/develop/install-cli-sdk.md?pivots=programming-language-csharp)
1. Install packages:

    [!INCLUDE [install-csharp-packages](install-csharp-packages.md)]

1. Set these environment variables to use in your scripts:

    :::code language="text" source=" source="~/foundry-samples/samples/microsoft/csharp/mslearn-resources/quickstart/Samples/.env.example:::

1. Make sure to sign in using the CLI `az login` (or `az login --use-device-code`) command to authenticate before running your C# scripts.

> [!TIP]
> All the code in this article is at [GitHub Quickstart](https://github.com/azure-ai-foundry/foundry-samples/tree/main/samples/microsoft/csharp/mslearn-resources/quickstart).

---

## Create a [!INCLUDE [fdp-project-name](fdp-project-name.md)] 

Use either the Azure AI Foundry portal or Azure CLI to create a project.

1. Sign in to the [Azure AI Foundry portal](https://ai.azure.com).
1. On the home page, select **Create the future**. This creates a project and also include steps to start working with a basic Agent.
    
    :::image type="content" source="../media/quickstarts/start-building.png" alt-text="Screenshot shows how to start building an Agent in Azure AI Foundry portal.":::

1. Fill in a name for your project and select **Create**. 

## Deploy a model

[!INCLUDE [tip-left-pane](../includes/tip-left-pane.md)]

1. If you just used the Azure AI Foundry portal to create the project with the **Create the future** link, you're next  prompted to deploy a model.
1. Or else, sign in to the [Azure AI Foundry portal](https://ai.azure.com), select your project, and select **Model catalog**.
1. Search for the model you want to deploy. For this quickstart, select **gpt-4o**.
1. Select **Confirm**.
1. Don't change the default settings. Select **Deploy**.

## Run a chat completion

# [Azure AI Foundry portal](#tab/azure-ai-foundry)

1. If you used **Create the future** to create the project, you'll now find yourself in the Agents playground, ready to try it out. You'll come back here in a moment, but first let's play with the model.
1. In the left pane, select **Playgrounds**. 
1. Select **Try the chat playground**.
1. Fill in the prompt and select the **Send** button.
1. The model returns a response in the **Response** pane.

# [Python SDK](#tab/python)

:::code language="python" source="~/foundry-samples/samples/microsoft/python/mslearn-resources/quickstart/quickstart.py" id="chat_completion":::


# [Java](#tab/java)

:::code language="java" source="~/foundry-samples/samples/microsoft/java/mslearn-resources/quickstart/src/main/java/com/azure/ai/foundry/samples/ChatCompletionSample.java" :::

# [JavaScript](#tab/javascript)

:::code language="javascript" source="~/foundry-samples/samples/microsoft/javascript/mslearn-resources/quickstart/src/quickstart.js" id="chat_completion":::


# [C#](#tab/csharp)

:::code language="csharp" source="~/foundry-samples/samples/microsoft/csharp/mslearn-resources/quickstart/Samples/SimpleInference.cs" id="chat_completion":::

---

## Create and run an agent

# [Azure AI Foundry portal](#tab/azure-ai-foundry)

1. In your project, on the left pane, select **Agents**.
1. Select the agent created with the project. 
1. If you didn't create one with your project, select **New agent** to create an agent now.
1. On the right **Setup** pane, change the name if you'd like.
1. Add instructions, such as, "You are a helpful writing assistant."
1. At the top of the **Setup** pane, select **Try in playground**.
1. Start chatting with your agent, for example, "Write me a poem about flowers"

# [Python SDK](#tab/python)

:::code language="python" source="~/foundry-samples/samples/microsoft/python/mslearn-resources/quickstart/quickstart.py" id="create_and_run_agent":::

# [Java](#tab/java)

:::code language="java" source="~/foundry-samples/samples/microsoft/java/mslearn-resources/quickstart/src/main/java/com/azure/ai/foundry/samples/AgentSample.java" :::

# [JavaScript](#tab/javascript)

:::code language="javascript" source="~/foundry-samples/samples/microsoft/javascript/mslearn-resources/quickstart/src/quickstart.js" id="create_and_run_agent" :::

# [C#](#tab/csharp)

:::code language="csharp" source="~/foundry-samples/samples/microsoft/csharp/mslearn-resources/quickstart/Samples/AgentService.cs" id="create_and_run_agent" :::

---

## Add files to the agent


Enable your agent to search and retrieve information from a provided file. 

* Download [product_info_1.md](https://github.com/azure-ai-foundry/foundry-samples/blob/main/samples/microsoft/data/product_info_1.md) to give to your agent.


# [Azure AI Foundry portal](#tab/azure-ai-foundry)

1. In your agent's **Setup** pane, scroll down if necessary to find **Knowledge**.
1. Select **Add**.
1. Select **Files** to upload the **product_info_1.md** file.
1. Select **Select local files** under **Add files**.
1. Select **Upload and save**.
1. Change your agents instructions, such as, "You are a helpful assistant and can search information from uploaded files."
1. Ask a question, such as, "Hello, what Contoso products do you know?"
1. To add more files, select the **...** on the AgentVectorStore, then select **Manage**.

# [Python SDK](#tab/python)

:::code language="python" source="~/foundry-samples/samples/microsoft/python/mslearn-resources/quickstart/quickstart.py" id="create_filesearch_agent":::

# [Java](#tab/java)

:::code language="java" source="~/foundry-samples/samples/microsoft/java/mslearn-resources/quickstart/src/main/java/com/azure/ai/foundry/samples/FileSearchAgentSample.java" :::


# [JavaScript](#tab/javascript)

:::code language="javascript" source="~/foundry-samples/samples/microsoft/javascript/mslearn-resources/quickstart/src/quickstart.js" id="create_filesearch_agent":::

# [C#](#tab/csharp)

:::code language="csharp" source="~/foundry-samples/samples/microsoft/csharp/mslearn-resources/quickstart/Samples/AgentFileSearch.cs" id="create_filesearch_agent":::

---


## Clean up resources

If you no longer need them, delete the resource group associated with your project.

In the Azure AI Foundry portal, select your project name in the top right corner. Then select the link for the resource group to open it in the Azure portal. Select the resource group, and then select **Delete**. Confirm that you want to delete the resource group.

## Related content

[Azure AI Foundry SDK Overview](../how-to/develop/sdk-overview.md)