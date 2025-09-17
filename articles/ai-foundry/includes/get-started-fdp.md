---
title: Include file
description: Include file
author: sgilley
ms.author: sgilley
ms.date: 07/03/2025
ms.service: azure-ai-foundry
ms.topic: include
ms.custom:
  - include file
  - build-aifnd
  - build-2025
  - update-code-4
monikerRange: foundry-classic || foundry
ai-usage: ai-assisted
---

In this quickstart, you use [Azure AI Foundry](https://ai.azure.com/?cid=learnDocs) to:

> [!div class="checklist"]
> * Create a project
> * Deploy a model
> * Run a chat completion
> * Create and run an agent
> * Upload files to the agent

The Azure AI Foundry SDK is available in multiple languages, including Python, Java, TypeScript, and C#. This quickstart provides instructions for each of these languages.

::: moniker range="foundry-classic"
> [!TIP]
> The rest of this article shows how to create and use a **[!INCLUDE [fdp](../includes/fdp-project-name.md)]**. Select **[!INCLUDE [hub](../includes/hub-project-name.md)]** at the top of this article if you want to use a [!INCLUDE [hub](../includes/hub-project-name.md)] instead. [Which type of project do I need?](../what-is-azure-ai-foundry.md#which-type-of-project-do-i-need)
::: moniker-end

## Prerequisites

- [!INCLUDE [subscription](subscription.md)]

- You must be **Owner** of the subscription to receive the appropriate access control needed to use your project.

[!INCLUDE [feature-preview](feature-preview.md)]

[!INCLUDE [first-run](first-run-experience.md)]

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


# [TypeScript](#tab/typescript)

1. [Install Node.js and Azure CLI](../how-to/develop/install-cli-sdk.md?pivots=programming-language-javascript)
1. Make sure to sign in using the CLI `az login` (or `az login --use-device-code`) command to authenticate before running your TypeScript scripts.
1. Download [package.json](https://github.com/azure-ai-foundry/foundry-samples/blob/main/samples/microsoft/typescript/mslearn-resources/quickstart/package.json).
1. Install packages with `npm install`
1. [!INCLUDE [find-endpoint](find-endpoint.md)]
1. Set these environment variables to use in your scripts:

    :::code language="plaintext" source="~/foundry-samples-main/samples/microsoft/typescript/mslearn-resources/quickstart/.env.template":::


> [!NOTE]
> All the code in this article is at [GitHub Quickstart](https://github.com/azure-ai-foundry/foundry-samples/tree/main/samples/microsoft/typescript/mslearn-resources/quickstart).

# [Java (preview)](#tab/java)

1. [Install Java and Azure CLI](../how-to/develop/install-cli-sdk.md?pivots=programming-language-java).
1. [!INCLUDE [find-endpoint](find-endpoint.md)]
1. Set these environment variables to use in your scripts:

    ```txt
    MODEL_DEPLOYMENT_NAME=gpt-4o
    PROJECT_ENDPOINT=https://<your-foundry-resource-name>.services.ai.azure.com/api/projects/<your-foundry-project-name>
    ```

1. Make sure to sign in using the CLI `az login` (or `az login --use-device-code`) command to authenticate before running your Java scripts.
1. Download [POM.XML](https://github.com/azure-ai-foundry/foundry-samples/blob/main/samples/microsoft/java/mslearn-resources/quickstart/pom.xml) to your Java IDE.

> [!NOTE]
> All the code in this article is at [GitHub Quickstart](https://github.com/azure-ai-foundry/foundry-samples/blob/main/samples/microsoft/java/mslearn-resources/quickstart).


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

::: moniker range="foundry-classic"
1. In the chat playground, fill in the prompt and select the **Send** button.
1. The model returns a response in the **Response** pane.
::: moniker-end

::: moniker range="foundry"
1. On the top right, select **Build** if you're not already there.
1. On the left pane, select **Models**.
1. Select your **gpt-40** model.
1. Use the area on the right to chat with your model.  
::: moniker-end

# [Python](#tab/python)

Substitute your endpoint for the `endpoint` in this code:

:::code language="python" source="~/foundry-samples-main/samples/microsoft/python/mslearn-resources/quickstart/quickstart.py" id="chat_completion":::

# [C#](#tab/csharp)

:::code language="csharp" source="~/foundry-samples-main/samples/microsoft/csharp/mslearn-resources/quickstart/Samples/SimpleInference.cs" id="chat_completion":::

# [TypeScript](#tab/typescript)

:::code language="typescript" source="~/foundry-samples-main/samples/microsoft/typescript/mslearn-resources/quickstart/src/quickstart.ts" id="chat_completion":::

# [Java (preview)](#tab/java)

:::code language="java" source="~/foundry-samples-main/samples/microsoft/java/mslearn-resources/quickstart/src/main/java/com/azure/ai/foundry/samples/ChatCompletionSample.java" :::

# [REST API](#tab/rest)

Replace `YOUR-FOUNDRY-RESOURCE-NAME` with your values:

:::code language="console" source="~/foundry-samples-main/samples/microsoft/REST/mslearn-resources/quickstart/quickstart.sh" id="chat_completion":::

---

## Chat with an agent

Agents have powerful capabilities through the use of tools. Start by chatting with an agent.
 
# [Azure AI Foundry portal](#tab/azure-ai-foundry)

::: moniker range="foundry-classic"
When you're ready to try an agent, a default agent is created for you. To chat with this agent:

1. On the left pane, select **Playgrounds**.
1. In the **Agents playground** card, select **Let's go**.
1. Add instructions, such as, "You are a helpful writing assistant."
1. Start chatting with your agent, for example, "Write me a poem about flowers."
::: moniker-end

::: moniker range="foundry"
1. On the left pane, select **Agents**.
1. Select your agent.
1. Add instructions, such as, "You are a helpful writing assistant."
1. Start chatting with your agent, for example, "Write me a poem about flowers."
::: moniker-end

# [Python](#tab/python)

Substitute your endpoint for the `endpoint` in this code:

:::code language="python" source="~/foundry-samples-main/samples/microsoft/python/mslearn-resources/quickstart/quickstart.py" id="create_and_run_agent":::

# [C#](#tab/csharp)

:::code language="csharp" source="~/foundry-samples-main/samples/microsoft/csharp/mslearn-resources/quickstart/Samples/AgentService.cs" id="create_and_run_agent" :::

# [TypeScript](#tab/typescript)

:::code language="typescript" source="~/foundry-samples-main/samples/microsoft/typescript/mslearn-resources/quickstart/src/quickstart.ts" id="create_and_run_agent" :::

# [Java (preview)](#tab/java)

:::code language="java" source="~/foundry-samples-main/samples/microsoft/java/mslearn-resources/quickstart/src/main/java/com/azure/ai/foundry/samples/AgentSample.java" :::

# [REST API](#tab/rest)

Replace `YOUR-FOUNDRY-RESOURCE-NAME` and `YOUR-PROJECT-NAME` with your values:

:::code language="console" source="~/foundry-samples-main/samples/microsoft/REST/mslearn-resources/quickstart/quickstart.sh" id="create_and_run_agent":::

---

## Add files to the agent

Now let's add a file search tool that enables us to do knowledge retrieval.

* Download [product_info_1.md](https://github.com/azure-ai-foundry/foundry-samples/blob/main/samples/microsoft/data/product_info_1.md) to give to your agent.


# [Azure AI Foundry portal](#tab/azure-ai-foundry)

::: moniker range="foundry-classic"
1. In your agent's **Setup** pane, scroll down if necessary to find **Knowledge**.
1. Select **Add**.
1. Select **Files** to upload the **product_info_1.md** file.
1. Select **Select local files** under **Add files**.
1. Select **Upload and save**.
1. Change your agents instructions, such as, "You are a helpful assistant and can search information from uploaded files."
1. Ask a question, such as, "Hello, what Contoso products do you know?"
1. To add more files, select the **...** on the AgentVectorStore, then select **Manage**.
::: moniker-end

::: moniker range="foundry"
1. Scroll down if necessary to find **Tools**.
1. Select **Add**.
1. Select **File search**, then **Add tool**.
1. Select **Choose files** and browse to your **product_info_1.md** file. 
1. Select **Attach**.
::: moniker-end

# [Python](#tab/python)

Substitute your endpoint for the `endpoint` in this code:

:::code language="python" source="~/foundry-samples-main/samples/microsoft/python/mslearn-resources/quickstart/quickstart.py" id="create_filesearch_agent":::

# [C#](#tab/csharp)

:::code language="csharp" source="~/foundry-samples-main/samples/microsoft/csharp/mslearn-resources/quickstart/Samples/AgentFileSearch.cs" id="create_filesearch_agent":::

# [TypeScript](#tab/typescript)

:::code language="typescript" source="~/foundry-samples-main/samples/microsoft/typescript/mslearn-resources/quickstart/src/quickstart.ts" id="create_filesearch_agent":::

# [Java (preview)](#tab/java)

:::code language="java" source="~/foundry-samples-main/samples/microsoft/java/mslearn-resources/quickstart/src/main/java/com/azure/ai/foundry/samples/FileSearchAgentSample.java" :::

# [REST API](#tab/rest)

Replace `YOUR-FOUNDRY-RESOURCE-NAME` and `YOUR-PROJECT-NAME` with your values:

:::code language="console" source="~/foundry-samples-main/samples/microsoft/REST/mslearn-resources/quickstart/quickstart.sh" id="create_filesearch_agent":::

---


## Clean up resources

[!INCLUDE [clean-up-resources](clean-up-resources.md)]

## Related content

* [Quickstart: Create a new agent](../agents/quickstart.md)
* [Azure AI Foundry client library overview](../how-to/develop/sdk-overview.md)
