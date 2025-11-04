---
title: "Quickstart: Azure AI Foundry"
titleSuffix: Azure AI Foundry
description: Get started with Azure AI Foundry SDK to build AI applications. Learn to interact with an agent in Python, C#, TypeScript, or Java.
author: sdgilley
ms.author: sgilley
ms.reviewer: dantaylo
ms.date: 10/07/2025
ms.service: azure-ai-foundry
ms.topic: how-to
ms.custom:
  - build-2024
  - devx-track-azurecli
  - devx-track-python
  - ignite-2024
  - update-code6
  - build-aifnd
  - build-2025
  - peer-review-program
ai-usage: ai-assisted
monikerRange: 'foundry-classic || foundry'
# customer intent: As a developer, I want to start using the Azure AI Foundry portal and client libraries.
---

# Quickstart: Azure AI Foundry

[!INCLUDE [version-banner](../includes/version-banner.md)]

::: moniker range="foundry-classic"

In this quickstart, you use [!INCLUDE [classic-link](../includes/classic-link.md)] to:

> [!div class="checklist"]
> * Create a project
> * Deploy a model
> * Run a chat completion
> * Create and run an agent
> * Upload files to the agent
::: moniker-end

::: moniker range="foundry"
In this quickstart, you use [!INCLUDE [foundry-link](../default/includes/foundry-link.md)] to:

> [!div class="checklist"]
> * Create a project
> * Deploy a model
> * Create and run an agent
> * Upload files to the agent
::: moniker-end

The Azure AI Foundry SDK is available in multiple languages, including Python, Java, TypeScript, and C#. This quickstart provides instructions for each of these languages.

::: moniker range="foundry-classic"
> [!TIP]
> The rest of this article shows how to create and use a **[!INCLUDE [fdp](../includes/fdp-project-name.md)]**. See [Quickstart: Get started with Azure AI Foundry (Hub projects)](hub-get-started-code.md) if you want to use a [!INCLUDE [hub](../includes/hub-project-name.md)] instead. [Which type of project do I need?](../what-is-azure-ai-foundry.md#which-type-of-project-do-i-need)
::: moniker-end




## Prerequisites

> [!IMPORTANT]
> Before starting, make sure your development environment is ready.  
> This Quickstart focuses on **scenario-specific steps** like SDK installation, authentication, and running sample code.
>

- [!INCLUDE [azure-subscription](../includes/azure-subscription.md)]
- You must be **Owner** of the subscription to get the appropriate access control needed to use your project.
- Install the required language runtimes, global tools, and VS Code extensions as described in [Prepare your development environment](../how-to/develop/install-cli-sdk.md).

[!INCLUDE [first-run](../includes/first-run-experience.md)]

## <a name="install"></a> Get ready to code

::: moniker range="foundry"
[!INCLUDE [code-preview](../default/includes/code-preview.md)] 

[!INCLUDE [agent-v2-switch](../default/includes/agent-v2-switch.md)]

::: moniker-end

# [Python](#tab/python)

::: moniker range="foundry-classic"

1. Install these packages:

    ```
    pip install openai azure-ai-projects azure-identity
    ```

1. [!INCLUDE [find-endpoint](../includes/find-endpoint.md)]
1. Make sure to sign in using the CLI `az login` (or `az login --use-device-code`) command to authenticate before running your Python scripts.

::: moniker-end
::: moniker range="foundry"


1. Install these packages, including the preview version of `azure-ai-projects`:

    ```
    pip install azure-identity
    pip install azure-ai-projects --pre
    ```

1. [!INCLUDE [find-endpoint](../default/includes/find-endpoint.md)]
1. Make sure to sign in using the CLI `az login` (or `az login --use-device-code`) command to authenticate before running your Python scripts.

::: moniker-end
Follow along below or get the code:
> [!div class="nextstepaction"]
> [Get the code](https://github.com/azure-ai-foundry/foundry-samples/tree/main/samples/microsoft/python/mslearn-resources/quickstart)


# [C#](#tab/csharp)

::: moniker range="foundry-classic"

1. Install packages:

    [!INCLUDE [install-csharp-packages](../includes/install-csharp-packages.md)]

1. [!INCLUDE [find-endpoint](../includes/find-endpoint.md)]

1. Set these environment variables to use in your scripts.  The `AZURE_AI_ENDPOINT` is the project endpoint you copied earlier.  Remove everything after `.com/` in that endpoint to form `AZURE_AI_INFERENCE`.

    :::code language="plaintext" source="~/foundry-samples-main/samples/microsoft/csharp/mslearn-resources/quickstart/Samples/.env.example":::

    > [!TIP]
    > The agent samples require the `AZURE_AI_MODEL` environment variable to be set to an OpenAI-compatible model, e.g. `gpt-4.1`, as not all models are supported for agent use cases, including tooling.

1. Make sure to sign in using the CLI `az login` (or `az login --use-device-code`) command to authenticate before running your C# scripts.

::: moniker-end
::: moniker range="foundry"

1. Install packages, including the preview version of `Azure.AI.Projects`:

    [!INCLUDE [install-csharp-packages](../includes/install-csharp-packages.md)]

1. [!INCLUDE [find-endpoint](../default/includes/find-endpoint.md)]

1. Set these environment variables to use in your scripts.  The `AZURE_AI_ENDPOINT` is the project endpoint you copied earlier.  Remove everything after `.com/` in that endpoint to form `AZURE_AI_INFERENCE`.

    :::code language="plaintext" source="~/foundry-samples-main/samples/microsoft/csharp/mslearn-resources/quickstart/Samples/.env.example":::

    > [!TIP]
    > The agent samples require the `AZURE_AI_MODEL` environment variable to be set to an OpenAI-compatible model, e.g. `gpt-4.1`, as not all models are supported for agent use cases, including tooling.

1. Make sure to sign in using the CLI `az login` (or `az login --use-device-code`) command to authenticate before running your C# scripts.

::: moniker-end

Follow along below or get the code:
> [!div class="nextstepaction"]
> [Get the code](https://github.com/azure-ai-foundry/foundry-samples/tree/main/samples/microsoft/csharp/mslearn-resources/quickstart)


# [TypeScript](#tab/typescript)

::: moniker range="foundry-classic"

1. Make sure to sign in using the CLI `az login` (or `az login --use-device-code`) command to authenticate before running your TypeScript scripts.
1. Download [package.json](https://github.com/azure-ai-foundry/foundry-samples/blob/main/samples/microsoft/typescript/mslearn-resources/quickstart/package.json).
1. Install packages with `npm install`
1. [!INCLUDE [find-endpoint](../includes/find-endpoint.md)]
1. Set these environment variables to use in your scripts:

    :::code language="plaintext" source="~/foundry-samples-main/samples/microsoft/typescript/mslearn-resources/quickstart/.env.template":::

::: moniker-end
::: moniker range="foundry"

1. Make sure to sign in using the CLI `az login` (or `az login --use-device-code`) command to authenticate before running your TypeScript scripts.
1. Download [package.json](https://github.com/azure-ai-foundry/foundry-samples/blob/main/samples/microsoft/typescript/mslearn-resources/quickstart/package.json).
1. Install packages with `npm install`, including the preview version of `@azure/ai-projects`.
1. [!INCLUDE [find-endpoint](../default/includes/find-endpoint.md)]
1. Set these environment variables to use in your scripts:

    :::code language="plaintext" source="~/foundry-samples-main/samples/microsoft/typescript/mslearn-resources/quickstart/.env.template":::

::: moniker-end

Follow along below or get the code:
> [!div class="nextstepaction"]
> [Get the code](https://github.com/azure-ai-foundry/foundry-samples/tree/main/samples/microsoft/typescript/mslearn-resources/quickstart)

# [Java](#tab/java)

::: moniker range="foundry-classic"
[!INCLUDE [code-preview](../default/includes/code-preview.md)]

1. [!INCLUDE [find-endpoint](../includes/find-endpoint.md)]
1. Set these environment variables to use in your scripts:

    ```txt
    MODEL_DEPLOYMENT_NAME=gpt-4o
    PROJECT_ENDPOINT=https://<your-foundry-resource-name>.services.ai.azure.com/api/projects/<your-foundry-project-name>
    ```

1. Make sure to sign in using the CLI `az login` (or `az login --use-device-code`) command to authenticate before running your Java scripts.
1. Download [POM.XML](https://github.com/azure-ai-foundry/foundry-samples/blob/main/samples/microsoft/java/mslearn-resources/quickstart/pom.xml) to your Java IDE.
::: moniker-end
::: moniker range="foundry"

1. [!INCLUDE [find-endpoint](../default/includes/find-endpoint.md)]
1. Set these environment variables to use in your scripts:

    ```txt
    MODEL_DEPLOYMENT_NAME=gpt-4o
    PROJECT_ENDPOINT=https://<your-foundry-resource-name>.services.ai.azure.com/api/projects/<your-foundry-project-name>
    ```

1. Make sure to sign in using the CLI `az login` (or `az login --use-device-code`) command to authenticate before running your Java scripts.
1. Download [POM.XML](https://github.com/azure-ai-foundry/foundry-samples/blob/main/samples/microsoft/java/mslearn-resources/quickstart/pom.xml) to your Java IDE. This includes the preview version of `azure-ai-projects`.
::: moniker-end

Follow along below or get the code:
> [!div class="nextstepaction"]
> [Get the code](https://github.com/azure-ai-foundry/foundry-samples/blob/main/samples/microsoft/java/mslearn-resources/quickstart)


# [REST API](#tab/rest)

1. Make sure to sign in using the CLI `az login` (or `az login --use-device-code`) command to authenticate before running the next command.
1. Get a temporary access token. It will expire in 60-90 minutes, you'll need to refresh after that.

    ```azurecli
    az account get-access-token --scope https://ai.azure.com/.default
    ```
    
1. Save the results as the environment variable `AZURE_AI_AUTH_TOKEN`.  

Follow along below or get the code:
> [!div class="nextstepaction"]
> [Get the code](https://github.com/azure-ai-foundry/foundry-samples/tree/main/samples/microsoft/REST/mslearn-resources/quickstart).


# [Azure AI Foundry portal](#tab/azure-ai-foundry)

No installation is necessary to use the Azure AI Foundry portal.

---

::: moniker range="foundry-classic"

## Run a chat completion

Chat completions are the basic building block of AI applications. Using chat completions you can send a list of messages and get a response from the model.


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

# [Azure AI Foundry portal](#tab/azure-ai-foundry)

1. In the chat playground, fill in the prompt and select **Send**.
1. The model returns a response in the **Response** pane.

---

::: moniker-end

## Chat with an agent

Create an agent and chat with it.
 

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

# [Azure AI Foundry portal](#tab/azure-ai-foundry)

::: moniker range="foundry-classic"

When you're ready to try an agent, a default agent is created for you. To chat with this agent:

1. In the left pane, select **Playgrounds**.
1. In the **Agents playground** card, select **Let's go**.
1. Add instructions, such as, "You are a helpful writing assistant."
1. Start chatting with your agent, for example, "Write me a poem about flowers."

::: moniker-end

::: moniker range="foundry"

After you create the agent, you're automatically moved from **Home** to the **Build** section. Your new agent is selected and ready for you to try out in the Agent pane.

1. Add instructions, such as, "You are a helpful writing assistant."
1. Start chatting with your agent, for example, "Write me a poem about flowers." 

::: moniker-end

---

::: moniker range="foundry-classic"
## Add files to the agent

Agents have powerful capabilities through the use of tools. Let's add a file search tool that enables us to do knowledge retrieval.

* Download [product_info_1.md](https://github.com/azure-ai-foundry/foundry-samples/blob/main/samples/microsoft/data/product_info_1.md) to give to your agent.

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

# [Azure AI Foundry portal](#tab/azure-ai-foundry)

1. In your agent's **Setup** pane, scroll down if necessary to find **Knowledge**.
1. Select **Add**.
1. Select **Files** to upload the product_info_1.md file.
1. Select **Select local files** under **Add files**.
1. Select **Upload and save**.
1. Change your agents instructions, such as, "You are a helpful assistant and can search information from uploaded files."
1. Ask a question, such as, "Hello, what Contoso products do you know?"
1. To add more files, select the **...** on the AgentVectorStore, then select **Manage**.

---
::: moniker-end

## Clean up resources

[!INCLUDE [clean-up-resources](../includes/clean-up-resources.md)]

## Related content

* [Quickstart: Create a new agent](../agents/quickstart.md)
* [Azure AI Foundry client library overview](../how-to/develop/sdk-overview.md)
