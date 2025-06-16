---
title: Include file
description: Include file
author: sgilley
ms.author: sgilley
ms.date: 05/13/2025
ms.service: azure-ai-foundry
ms.topic: include
ms.custom:
  - include file
  - build-aifnd
  - build-2025
---

In this quickstart, you use [Azure AI Foundry](https://ai.azure.com/?cid=learnDocs) to:

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

[!INCLUDE [feature-preview](feature-preview.md)]

## Start with a project and model

1. Sign in to the [Azure AI Foundry portal](https://ai.azure.com/?cid=learnDocs).
1. On the home page, search and then select the **gpt-4o** model. 
    
    :::image type="content" source="../media/quickstarts/start-building.png" alt-text="Screenshot shows how to start building an Agent in Azure AI Foundry portal.":::

1. On the model details page, select **Use this model**.
1. Fill in a name to use for your project and select **Create**. 
1. Once your resources are created, you are in the chat playground. 
    
## Set up your environment  

# [Azure AI Foundry portal](#tab/azure-ai-foundry)

No installation is necessary to use the Azure AI Foundry portal.

# [Python](#tab/python)

1. [Install Python and Azure CLI](../how-to/develop/install-cli-sdk.md?pivots=programming-language-python)
1. Install these packages:

    ```
    pip install openai azure-ai-projects azure-identity
    ```

1. [!INCLUDE [find-endpoint](find-endpoint.md)]
1. Make sure to sign in using the CLI `az login` (or `az login --use-device-code`) command to authenticate before running your Python scripts.

> [!NOTE]
> All the code in this article is at [GitHub Quickstart](https://github.com/azure-ai-foundry/foundry-samples/tree/main/samples/microsoft/python/mslearn-resources/quickstart).

# [Java (preview)](#tab/java)

1. [Install Java and Azure CLI](../how-to/develop/install-cli-sdk.md?pivots=programming-language-java).
1. [!INCLUDE [find-endpoint](find-endpoint.md)]
1. Set these environment variables to use in your scripts:

    :::code language="plaintext" source="~/foundry-samples-main/samples/microsoft/java/mslearn-resources/quickstart/.env.template":::

1. Make sure to sign in using the CLI `az login` (or `az login --use-device-code`) command to authenticate before running your Java scripts.
1. Download [POM.XML](https://github.com/azure-ai-foundry/foundry-samples/blob/main/samples/microsoft/java/mslearn-resources/quickstart/pom.xml) to your Java IDE.

> [!NOTE]
> All the code in this article is at [GitHub Quickstart](https://github.com/azure-ai-foundry/foundry-samples/blob/main/samples/microsoft/java/mslearn-resources/quickstart).

# [JavaScript (preview)](#tab/javascript)

1. [Install Node.js and Azure CLI](../how-to/develop/install-cli-sdk.md?pivots=programming-language-javascript)
1. Make sure to sign in using the CLI `az login` (or `az login --use-device-code`) command to authenticate before running your JavaScript scripts.
1. Download [package.json](https://github.com/azure-ai-foundry/foundry-samples/blob/main/samples/microsoft/javascript/mslearn-resources/quickstart/package.json).
1. Install packages with `npm install`
1. [!INCLUDE [find-endpoint](find-endpoint.md)]
1. Set these environment variables to use in your scripts:

    :::code language="plaintext" source="~/foundry-samples-main/samples/microsoft/javascript/mslearn-resources/quickstart/.env.template":::


> [!NOTE]
> All the code in this article is at [GitHub Quickstart](https://github.com/azure-ai-foundry/foundry-samples/tree/main/samples/microsoft/javascript/mslearn-resources/quickstart).

# [C#](#tab/csharp)

1. [Install C# and Azure CLI](../how-to/develop/install-cli-sdk.md?pivots=programming-language-csharp)
1. Install packages:

    [!INCLUDE [install-csharp-packages](install-csharp-packages.md)]

1. [!INCLUDE [find-endpoint](find-endpoint.md)]

1. Set these environment variables to use in your scripts:

    :::code language="plaintext" source="~/foundry-samples-main/samples/microsoft/csharp/mslearn-resources/quickstart/Samples/.env.example":::

1. Make sure to sign in using the CLI `az login` (or `az login --use-device-code`) command to authenticate before running your C# scripts.

> [!NOTE]
> All the code in this article is at [GitHub Quickstart](https://github.com/azure-ai-foundry/foundry-samples/tree/main/samples/microsoft/csharp/mslearn-resources/quickstart).

# [REST API](#tab/rest)

1. [Install Azure CLI](../how-to/develop/install-cli-sdk.md#installs)
1. Make sure to sign in using the CLI `az login` (or `az login --use-device-code`) command to authenticate before running the next command.
1. Get a temporary access token.  It will expire in 60-90 minutes, you'll need to refresh after that.

    ```azurecli
    az account get-access-token --scope https://ai.azure.com/.default
    ```
    
1. Save the results as the environment variable `AZURE_AI_AUTH_TOKEN`.  

> [!NOTE]
> All the code in this article is at [GitHub Quickstart](https://github.com/azure-ai-foundry/foundry-samples/tree/main/samples/microsoft/REST/mslearn-resources/quickstart).


---

## Run a chat completion

Chat completions are the basic building block of AI applications. Using chat completions you can send a list of messages and get a response from the model.

# [Azure AI Foundry portal](#tab/azure-ai-foundry)

1. In the chat playground, fill in the prompt and select the **Send** button.
1. The model returns a response in the **Response** pane.

# [Python](#tab/python)

Substitute your endpoint for the `endpoint` in this code:

:::code language="python" source="~/foundry-samples-main/samples/microsoft/python/mslearn-resources/quickstart/quickstart.py" id="chat_completion":::


# [Java (preview)](#tab/java)

:::code language="java" source="~/foundry-samples-main/samples/microsoft/java/mslearn-resources/quickstart/src/main/java/com/azure/ai/foundry/samples/ChatCompletionSample.java" :::

# [JavaScript (preview)](#tab/javascript)

:::code language="javascript" source="~/foundry-samples-main/samples/microsoft/javascript/mslearn-resources/quickstart/src/quickstart.js" id="chat_completion":::


# [C#](#tab/csharp)

:::code language="csharp" source="~/foundry-samples-main/samples/microsoft/csharp/mslearn-resources/quickstart/Samples/SimpleInference.cs" id="chat_completion":::

# [REST API](#tab/rest)

Replace `YOUR-FOUNDRY-RESOURCE-NAME` with your values:

:::code language="console" source="~/foundry-samples-main/samples/microsoft/REST/mslearn-resources/quickstart/quickstart.sh" id="chat_completion":::

---

## Chat with an agent

Agents have powerful capabilities through the use of tools. Start by chatting with an agent.
 
# [Azure AI Foundry portal](#tab/azure-ai-foundry)

When you create a project from the model catalog, the model is deployed and an agent is created using this model. To chat with this agent:

1. On the left pane, select **Playgrounds**.
1. In the **Agents playground** card, select **Let's go**.
1. Add instructions, such as, "You are a helpful writing assistant."
1. Start chatting with your agent, for example, "Write me a poem about flowers."

# [Python](#tab/python)

Substitute your endpoint for the `endpoint` in this code:

:::code language="python" source="~/foundry-samples-main/samples/microsoft/python/mslearn-resources/quickstart/quickstart.py" id="create_and_run_agent":::

# [Java (preview)](#tab/java)

:::code language="java" source="~/foundry-samples-main/samples/microsoft/java/mslearn-resources/quickstart/src/main/java/com/azure/ai/foundry/samples/AgentSample.java" :::

# [JavaScript (preview)](#tab/javascript)

:::code language="javascript" source="~/foundry-samples-main/samples/microsoft/javascript/mslearn-resources/quickstart/src/quickstart.js" id="create_and_run_agent" :::

# [C#](#tab/csharp)

:::code language="csharp" source="~/foundry-samples-main/samples/microsoft/csharp/mslearn-resources/quickstart/Samples/AgentService.cs" id="create_and_run_agent" :::

# [REST API](#tab/rest)

Replace `YOUR-FOUNDRY-RESOURCE-NAME` and `YOUR-PROJECT-NAME` with your values:

:::code language="console" source="~/foundry-samples-main/samples/microsoft/REST/mslearn-resources/quickstart/quickstart.sh" id="create_and_run_agent":::


---

## Add files to the agent

Now let's add a file search tool that enables us to do knowledge retrieval.

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

# [Python](#tab/python)

Substitute your endpoint for the `endpoint` in this code:

:::code language="python" source="~/foundry-samples-main/samples/microsoft/python/mslearn-resources/quickstart/quickstart.py" id="create_filesearch_agent":::

# [Java (preview)](#tab/java)

:::code language="java" source="~/foundry-samples-main/samples/microsoft/java/mslearn-resources/quickstart/src/main/java/com/azure/ai/foundry/samples/FileSearchAgentSample.java" :::


# [JavaScript (preview)](#tab/javascript)

:::code language="javascript" source="~/foundry-samples-main/samples/microsoft/javascript/mslearn-resources/quickstart/src/quickstart.js" id="create_filesearch_agent":::

# [C#](#tab/csharp)

:::code language="csharp" source="~/foundry-samples-main/samples/microsoft/csharp/mslearn-resources/quickstart/Samples/AgentFileSearch.cs" id="create_filesearch_agent":::

# [REST API](#tab/rest)

Replace `YOUR-FOUNDRY-RESOURCE-NAME` and `YOUR-PROJECT-NAME` with your values:

:::code language="console" source="~/foundry-samples-main/samples/microsoft/REST/mslearn-resources/quickstart/quickstart.sh" id="create_filesearch_agent":::

---


## Clean up resources

If you no longer need them, delete the resource group associated with your project.

In the Azure AI Foundry portal, select your project name in the top right corner. Then select the link for the resource group to open it in the Azure portal. Select the resource group, and then select **Delete**. Confirm that you want to delete the resource group.

## Related content

[Azure AI Foundry client library overview](../how-to/develop/sdk-overview.md)
