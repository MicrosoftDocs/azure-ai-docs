---
title: include file
description: include file
author: sgilley
ms.author: sgilley
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 04/30/2025
ms.custom: include file
---


In this quickstart, you use [Azure AI Foundry](https://ai.azure.com) to:

> [!div class="checklist"]
> * Create a project
> * Deploy a model
> * Run a chat completion
> * Create and run an agent
> * Upload files to the agent
> * Evaluate the agent run

The Azure AI Foundry SDK is available in multiple languages, including Python, Java, JavaScript, and C#. This quickstart provides instructions for each of these languages.

> [!TIP]
> The rest of this article shows how to use a **[!INCLUDE [fdp](../includes/fdp-project-name.md)]**.  Select **[!INCLUDE [hub](../includes/hub-project-name.md)]** at the top of this article if you want to use a [!INCLUDE [hub](../includes/hub-project-name.md)] instead.

## Prerequisites

- An [Azure subscription](https://azure.microsoft.com/free/). If you don't have an Azure subscription, create a free account before you begin.
- You must be **Owner** of the subscription to assign the appropriate access control needed to run these scripts.

### Set up your environment  

# [Azure AI Foundry portal](#tab/azure-ai-foundry)

No installation is necessary to use the Azure AI Foundry portal.

# [Python SDK](#tab/python)

1. [Set up your development environment](../how-to/develop/install-cli-sdk.md?tabs=python)
1. Install these packages:

    ```
    pip install openai azure-ai-projects azure-identity
    ```

# [Java](#tab/java)

1. [Set up your development environment](../how-to/develop/install-cli-sdk.md?tabs=java)

# [JavaScript](#tab/javascript)

1. [Set up your development environment](../how-to/develop/install-cli-sdk.md?tabs=javascript)

# [C#](#tab/csharp)

1. [Set up your development environment](../how-to/develop/install-cli-sdk.md?tabs=csharp)

---

## Create a [!INCLUDE [fdp-project-name](fdp-project-name.md)] 

# [Azure AI Foundry portal](#tab/azure-ai-foundry)

1. Sign in to the [Azure AI Foundry portal](https://ai.azure.com).
1. On the home page, select **Start building**. This will build a project and include steps to start working with an Agent.  
    
    :::image type="content" source="../media/quickstarts/start-building.png" alt-text="Screenshot shows how to start building an Agent in Azure AI Foundry portal.":::

1. Fill in a name for your project and select **Create**.  

# [Python SDK](#tab/python)

:::code language="python" source="~/foundry-samples/doc-samples/getting-started/python/create_project.py" id="create_project":::

# [Java](#tab/java)

Use instructions for **Azure AI Foundry portal** or **Python SDK** to create a [!INCLUDE [fdp-project-name](fdp-project-name.md)].

# [JavaScript](#tab/javascript)

Use instructions for **Azure AI Foundry portal** or **Python SDK** to to create a [!INCLUDE [fdp-project-name](fdp-project-name.md)].

# [C#](#tab/csharp)

Use instructions for **Azure AI Foundry portal** or **Python SDK** to create a [!INCLUDE [fdp-project-name](fdp-project-name.md)].


---


## Deploy a model

# [Azure AI Foundry portal](#tab/azure-ai-foundry)

[!INCLUDE [tip-left-pane](../includes/tip-left-pane.md)]

1. If you created the project with the **Start building** link, you'll next be prompted to deploy a model.
1. Or else, select **Model catalog**.
1. Search for the model you want to deploy.  For this quickstart, select **gpt-4o**.
1. Select **Confirm**.
1. Do not change the default settings.  Select **Deploy**.

### Assign role-based access control

1. At the bottom of the left pane, select **Management center**.
1. Under the resource name, select **Users**.
1. Add yourself as a user with each of the following roles: 

    * **Azure AI Project Manager** 
    * **Azure AI User** 

1. After adding these roles, on the left pane, select **Go to project** to return to your project.

# [Python SDK](#tab/python)

:::code language="python" source="~/foundry-samples/doc-samples/getting-started/python/create_project.py" id="deploy_model":::

# [Java](#tab/java)

Use instructions for **Azure AI Foundry portal** or **Python SDK** to deploy the **gpt-4o** model into your [!INCLUDE [fdp-project-name](fdp-project-name.md)].

# [JavaScript](#tab/javascript)

Use instructions for **Azure AI Foundry portal** or **Python SDK** to deploy the **gpt-4o** model into your [!INCLUDE [fdp-project-name](fdp-project-name.md)].

# [C#](#tab/csharp)

Use instructions for **Azure AI Foundry portal** or **Python SDK** to deploy the **gpt-4o** model into your [!INCLUDE [fdp-project-name](fdp-project-name.md)].

---

## Run a chat completion

# [Azure AI Foundry portal](#tab/azure-ai-foundry)

1. In the left pane, select **Playgrounds**. 
1. Select **Try the chat playground**.
1. Fill in the prompt and select the **Send** button.
1. The model returns a response in the **Response** pane.

# [Python SDK](#tab/python)

:::code language="python" source="~/foundry-samples/doc-samples/getting-started/python/quickstart.py" id="chat_completion":::


# [Java](#tab/java)
Info here.
# [JavaScript](#tab/javascript)
Info here.
# [C#](#tab/csharp)
Info here.

---

## Create and run an agent

# [Azure AI Foundry portal](#tab/azure-ai-foundry)

1. In your project, on the left pane, select **Agents**.
1. Select the agent created with the project.  
1. If you didn't create one with your project, select **New agent** to create an agent.
1. On the right **Setup** pane, change the name if you'd like.
1. Add instructions, such as, "You are a helpful writing assistant."
1. At the top of the **Setup** pane, select **Try in playground**.
1. Start chatting with your agent, fore example, "Write me a poem about flowers"

# [Python SDK](#tab/python)

:::code language="python" source="~/foundry-samples/doc-samples/getting-started/python/quickstart.py" id="create_and_run_agent":::

# [Java](#tab/java)
Info here.
# [JavaScript](#tab/javascript)
Info here.
# [C#](#tab/csharp)
Info here.

---

## Add files to the agent

Download [product_info_1.md]() to add to the agent.

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

:::code language="python" source="~/foundry-samples/doc-samples/getting-started/python/quickstart.py" id="create_filesearch_agent":::

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