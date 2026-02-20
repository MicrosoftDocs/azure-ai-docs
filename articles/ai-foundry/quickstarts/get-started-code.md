---
title: Microsoft Foundry Quickstart
titleSuffix: Microsoft Foundry
description: Get started with Microsoft Foundry SDK building AI applications. 
author: sdgilley
ms.author: sgilley
ms.reviewer: dantaylo
ms.date: 12/16/2025
ms.service: azure-ai-foundry
ms.topic: quickstart
monikerRange: 'foundry-classic || foundry'
ms.custom:
  - build-2024
  - devx-track-azurecli
  - devx-track-python
  - ignite-2024
  - update-code8
  - build-aifnd
  - build-2025
  - peer-review-program
ai-usage: ai-assisted
# customer intent: As a developer, I want to start using the Microsoft Foundry portal and client libraries.
---

# Microsoft Foundry quickstart

[!INCLUDE [version-banner](../includes/version-banner.md)]

:::moniker range="foundry"

[!INCLUDE [quickstart-v2-main](../default/includes/quickstart-v2-main.md)]

:::moniker-end

:::moniker range="foundry-classic"

In this quickstart, you use [!INCLUDE [classic-link](../includes/classic-link.md)] to:

> [!div class="checklist"]
> * Create a project
> * Deploy a model
> * Run a chat completion
> * Create and run an agent
> * Upload files to the agent

The Microsoft Foundry SDK is available in multiple languages, including Python, Java, TypeScript, and C#. This quickstart provides instructions for each of these languages.

> [!TIP]
> The rest of this article shows how to create and use a **[!INCLUDE [fdp](../includes/fdp-project-name.md)]**. See [Quickstart: Get started with Microsoft Foundry (Hub projects)](hub-get-started-code.md) if you want to use a [!INCLUDE [hub](../includes/hub-project-name.md)] instead. [Which type of project do I need?](../what-is-foundry.md#which-type-of-project-do-i-need)

## Prerequisites

- [!INCLUDE [azure-subscription](../includes/azure-subscription.md)]
- [!INCLUDE [rbac-create](../includes/rbac-create.md)]
- Install the required language runtimes, global tools, and VS Code extensions as described in [Prepare your development environment](../how-to/develop/install-cli-sdk.md).

> [!IMPORTANT]
> Before starting, make sure your development environment is ready.  
> This Quickstart focuses on **scenario-specific steps** like SDK installation, authentication, and running sample code.
>

[!INCLUDE [first-run](../includes/first-run-experience-classic.md)]

## Get ready to code

[!INCLUDE [agent-v1-switch](../includes/agent-v1-switch.md)]

# [Python](#tab/python)

1. Install these packages:

    ```
    pip install openai azure-identity azure-ai-projects==1.0.0
    ```

1. [!INCLUDE [find-endpoint](../includes/find-endpoint.md)]
1. Make sure to sign in using the CLI `az login` (or `az login --use-device-code`) command to authenticate before running your Python scripts.

Follow along below or get the code:
> [!div class="nextstepaction"]
> [Get the code](https://github.com/azure-ai-foundry/foundry-samples/tree/main/samples-classic/python/quickstart)

# [C#](#tab/csharp)

1. Install packages:

    [!INCLUDE [install-csharp-packages](../includes/install-csharp-packages.md)]

1. [!INCLUDE [find-endpoint](../includes/find-endpoint.md)]

1. Set these environment variables to use in your scripts.  The `AZURE_AI_ENDPOINT` is the project endpoint you copied earlier.  Remove everything after `.com/` in that endpoint to form `AZURE_AI_INFERENCE`.

    :::code language="plaintext" source="~/foundry-samples-main/samples-classic/csharp/quickstart/Samples/.env.example":::

    > [!TIP]
    > The agent samples require the `AZURE_AI_MODEL` environment variable to be set to an OpenAI-compatible model, e.g. `gpt-4.1`, as not all models are supported for agent use cases, including tooling.

1. Make sure to sign in using the CLI `az login` (or `az login --use-device-code`) command to authenticate before running your C# scripts.

Follow along below or get the code:
> [!div class="nextstepaction"]
> [Get the code](https://github.com/azure-ai-foundry/foundry-samples/tree/main/samples-classic/csharp/quickstart)

# [TypeScript](#tab/typescript)

1. Make sure to sign in using the CLI `az login` (or `az login --use-device-code`) command to authenticate before running your TypeScript scripts.
1. Download [package.json](https://github.com/azure-ai-foundry/foundry-samples/blob/main/samples-classic/typescript/quickstart/package.json).
1. Install packages with `npm install`
1. [!INCLUDE [find-endpoint](../includes/find-endpoint.md)]
1. Set these environment variables to use in your scripts:

    :::code language="plaintext" source="~/foundry-samples-main/samples-classic/typescript/quickstart/.env.template":::
1. Start your code with these imports:
    
    :::code language="typescript" source="~/foundry-samples-main/samples-classic/typescript/quickstart/src/quickstart.ts" id="imports":::

Follow along below or get the code:
> [!div class="nextstepaction"]
> [Get the code](https://github.com/azure-ai-foundry/foundry-samples/tree/main/samples-classic/typescript/quickstart)

# [Java](#tab/java)


1. [!INCLUDE [find-endpoint](../includes/find-endpoint.md)]
1. Set these environment variables to use in your scripts:

    ```txt
    MODEL_DEPLOYMENT_NAME=gpt-4o
    PROJECT_ENDPOINT=https://<your-foundry-resource-name>.services.ai.azure.com/api/projects/<your-foundry-project-name>
    ```

1. Make sure to sign in using the CLI `az login` (or `az login --use-device-code`) command to authenticate before running your Java scripts.
1. Download [POM.XML](https://github.com/azure-ai-foundry/foundry-samples/blob/main/samples-classic/java/quickstart/pom.xml) to your Java IDE.

Follow along below or get the code:
> [!div class="nextstepaction"]
> [Get the code](https://github.com/azure-ai-foundry/foundry-samples/blob/main/samples-classic/java/quickstart)

# [REST API](#tab/rest)

1. Make sure to sign in using the CLI `az login` (or `az login --use-device-code`) command to authenticate before running the next command.
1. Get a temporary access token. It will expire in 60-90 minutes, you'll need to refresh after that.

    ```azurecli
    az account get-access-token --scope https://ai.azure.com/.default
    ```
    
1. Save the results as the environment variable `AZURE_AI_AUTH_TOKEN`.  

Follow along below or get the code:
> [!div class="nextstepaction"]
> [Get the code](https://github.com/azure-ai-foundry/foundry-samples/tree/main/samples-classic/REST/quickstart).

# [Foundry portal](#tab/portal)

No installation is necessary to use the Foundry portal.

---

## Chat with a model

Chat completions are the basic building block of AI applications. Using chat completions you can send a list of messages and get a response from the model.

[!INCLUDE [agent-v1-switch](../includes/agent-v1-switch.md)]

# [Python](#tab/python)

Substitute your endpoint for the `endpoint` in this code:

:::code language="python" source="~/foundry-samples-main/samples-classic/python/quickstart/quickstart.py" id="chat_completion":::

# [C#](#tab/csharp)

:::code language="csharp" source="~/foundry-samples-main/samples-classic/csharp/quickstart/Samples/SimpleInference.cs" id="chat_completion":::

# [TypeScript](#tab/typescript)

:::code language="typescript" source="~/foundry-samples-main/samples-classic/typescript/quickstart/src/quickstart.ts" id="chat_completion":::

# [Java (preview)](#tab/java)

:::code language="java" source="~/foundry-samples-main/samples-classic/java/quickstart/src/main/java/com/azure/ai/foundry/samples/ChatCompletionSample.java" :::

# [REST API](#tab/rest)

Replace `YOUR-FOUNDRY-RESOURCE-NAME` with your values:

:::code language="console" source="~/foundry-samples-main/samples-classic/REST/quickstart/quickstart.sh" id="chat_completion":::

# [Foundry portal](#tab/portal)

1. In the chat playground, fill in the prompt and select **Send**.
1. The model returns a response in the **Response** pane.

---

## Chat with an agent

Create an agent and chat with it.

[!INCLUDE [agent-v1-switch](../includes/agent-v1-switch.md)]

# [Python](#tab/python)

Substitute your endpoint for the `endpoint` in this code:

:::code language="python" source="~/foundry-samples-main/samples-classic/python/quickstart/quickstart.py" id="create_and_run_agent":::

# [C#](#tab/csharp)

:::code language="csharp" source="~/foundry-samples-main/samples-classic/csharp/quickstart/Samples/AgentService.cs" id="create_and_run_agent" :::

# [TypeScript](#tab/typescript)

:::code language="typescript" source="~/foundry-samples-main/samples-classic/typescript/quickstart/src/quickstart.ts" id="create_and_run_agent" :::

# [Java (preview)](#tab/java)

:::code language="java" source="~/foundry-samples-main/samples-classic/java/quickstart/src/main/java/com/azure/ai/foundry/samples/AgentSample.java" :::

# [REST API](#tab/rest)

Replace `YOUR-FOUNDRY-RESOURCE-NAME` and `YOUR-PROJECT-NAME` with your values:

:::code language="console" source="~/foundry-samples-main/samples-classic/REST/quickstart/quickstart.sh" id="create_and_run_agent":::

# [Foundry portal](#tab/portal)

When you're ready to try an agent, a default agent is created for you. To chat with this agent:

1. In the left pane, select **Playgrounds**.
1. In the **Agents playground** card, select **Let's go**.
1. Add instructions, such as, "You are a helpful writing assistant."
1. Start chatting with your agent, for example, "Write me a poem about flowers."

---

## Add files to the agent

Agents have powerful capabilities through the use of tools. Let's add a file search tool that enables us to do knowledge retrieval.

* Download [product_info_1.md](https://github.com/azure-ai-foundry/foundry-samples/blob/main/samples-classic/data/product_info_1.md) to give to your agent.

[!INCLUDE [agent-v1-switch](../includes/agent-v1-switch.md)]

# [Python](#tab/python)

Substitute your endpoint for the `endpoint` in this code:

:::code language="python" source="~/foundry-samples-main/samples-classic/python/quickstart/quickstart.py" id="create_filesearch_agent":::

# [C#](#tab/csharp)

:::code language="csharp" source="~/foundry-samples-main/samples-classic/csharp/quickstart/Samples/AgentFileSearch.cs" id="create_filesearch_agent":::

# [TypeScript](#tab/typescript)

:::code language="typescript" source="~/foundry-samples-main/samples-classic/typescript/quickstart/src/quickstart.ts" id="create_filesearch_agent":::

# [Java (preview)](#tab/java)

:::code language="java" source="~/foundry-samples-main/samples-classic/java/quickstart/src/main/java/com/azure/ai/foundry/samples/FileSearchAgentSample.java" :::

# [REST API](#tab/rest)

Replace `YOUR-FOUNDRY-RESOURCE-NAME` and `YOUR-PROJECT-NAME` with your values:

:::code language="console" source="~/foundry-samples-main/samples-classic/REST/quickstart/quickstart.sh" id="create_filesearch_agent":::

# [Foundry portal](#tab/portal)

1. In your agent's **Setup** pane, scroll down if necessary to find **Knowledge**.
1. Select **Add**.
1. Select **Files** to upload the product_info_1.md file.
1. Select **Select local files** under **Add files**.
1. Select **Upload and save**.
1. Change your agents instructions, such as, "You are a helpful assistant and can search information from uploaded files."
1. Ask a question, such as, "Hello, what Contoso products do you know?"
1. To add more files, select the **...** on the AgentVectorStore, then select **Manage**.

---

## Clean up resources

[!INCLUDE [clean-up-resources](../includes/clean-up-resources.md)]

## Related content

* [Quickstart: Create a new agent](../agents/quickstart.md)
* [Client library overview](../how-to/develop/sdk-overview.md)

:::moniker-end
