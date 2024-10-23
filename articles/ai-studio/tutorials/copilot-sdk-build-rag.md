---
title: "Part 2: Build a custom chat app with the prompt flow SDK"
titleSuffix: Azure AI Studio
description: Learn how to build a RAG-based chat app using the prompt flow SDK. This tutorial is part 2 of a 3-part tutorial series.
manager: scottpolly
ms.service: azure-ai-studio
ms.topic: tutorial
ms.date: 08/29/2024
ms.reviewer: lebaro
ms.author: sgilley
author: sdgilley
ms.custom: [copilot-learning-hub]
#customer intent: As a developer, I want to learn how to use the prompt flow SDK so that I can build a RAG-based chat app.
---

# Tutorial: Part 2 - Build a custom chat application with the prompt flow SDK

In this tutorial, you use the prompt flow SDK (and other libraries) to build, configure, evaluate, and deploy a chat app for your retail company called Contoso Trek. Your retail company specializes in outdoor camping gear and clothing. The chat app should answer questions about your products and services. For example, the chat app can answer questions such as "which tent is the most waterproof?" or "what is the best sleeping bag for cold weather?".

This part two shows you how to enhance a basic chat application by adding [retrieval augmented generation (RAG)](../concepts/retrieval-augmented-generation.md) to ground the responses in your custom data. Retrieval Augmented Generation (RAG) is a pattern that uses your data with a large language model (LLM) to generate answers specific to your data. In this part two, you learn how to:

> [!div class="checklist"]
> - Deploy AI models in Azure AI Studio to use in your app
> - Develop custom RAG code
> - Use prompt flow to test your chat app

This tutorial is part two of a three-part tutorial.

## Prerequisites

* Complete [Tutorial: Part 1 - Create resources for building a custom chat application with the prompt flow SDK](copilot-sdk-create-resources.md).

* You need a local copy of product data. The [Azure-Samples/rag-data-openai-python-promptflow repository on GitHub](https://github.com/Azure-Samples/rag-data-openai-python-promptflow/) contains sample retail product information that's relevant for this tutorial scenario. [Download the example Contoso Trek retail product data in a ZIP file](https://github.com/Azure-Samples/rag-data-openai-python-promptflow/blob/main/tutorial/data/product-info.zip) to your local machine.

## Application code structure

Create a folder called **rag-tutorial** on your local machine. By the end of this tutorial series, **rag-tutorial** folder will provide the setup and scripts required to build, deploy, and test a Retrieval-Augmented Generation (RAG) based chat app based on the prompt flow SDK. When you complete the tutorial series, your folder structure looks like this:

```text
rag-tutorial/
│   .env
│   build_index.py
│   deploy.py
│   evaluate.py
│   eval_dataset.jsonl
|   invoke-local.py
│
├───copilot_flow
│   └─── chat.prompty
|   └─── copilot.py
|   └─── Dockerfile
│   └─── flow.flex.yaml
│   └─── input_with_chat_history.json
│   └─── queryIntent.prompty
│   └─── requirements.txt
│
├───data
|   └─── product-info/
|   └─── [Your own data or sample data as described in the prerequisites.]
```

> [!NOTE]
> You can run this Python script within the **rag-tutorial** to create all the required files for this tutorial.
```python
import os
folders = [
    "copilot_flow",
    "data",
    "data/product-info"
]
files = {
    ".env": "",
    "build_index.py": "",
    "deploy.py": "",
    "evaluate.py": "",
    "eval_dataset.jsonl": "",
    "invoke-local.py": "",
    "copilot_flow/chat.prompty": "",
    "copilot_flow/copilot.py": "",
    "copilot_flow/Dockerfile": "",
    "copilot_flow/flow.flex.yaml": "",
    "copilot_flow/input_with_chat_history.json": "",
    "copilot_flow/queryIntent.prompty": "",
    "copilot_flow/requirements.txt": ""
}
for folder in folders:
    os.makedirs(folder)
for file_path, content in files.items():
    with open(file_path, 'w') as f:
        f.write(content)
```

In this tutorial, the chat app is created using the [Prompt Flow](https://microsoft.github.io/promptflow/) suite, which simplifies building LLM-based applications. It uses a [flex flow](https://microsoft.github.io/promptflow/concepts/concept-flows.html#flex-flow) with **copilot.py** as the entry point, enabling access to Prompt Flow's testing, evaluation, and tracing features. For more details on developing a flex flow, visit the [Prompt Flow documentation on GitHub](https://microsoft.github.io/promptflow/how-to-guides/develop-a-flex-flow/index.html).

## Set initial environment variables

There's a collection of environment variables used across the different code snippets. Add them all into an **.env** file. 

> [!IMPORTANT]
> If you create this in a git repository, ensure that `.env` is in your `.gitignore` file so that you don't accidentally check it into the repository.

Start with these values. You'll add a few more values as you progress through the tutorial.

1. Create an **.env** file into your **rag-tutorial** folder. Add these variables:

    ```env
    AZURE_SUBSCRIPTION_ID=<your subscription id>
    AZURE_RESOURCE_GROUP=<your resource group>
    AZUREAI_PROJECT_NAME=<your project name>
    AZURE_OPENAI_CONNECTION_NAME=<your AIServices or Azure OpenAI connection name>
    AZURE_SEARCH_ENDPOINT=<your Azure Search endpoint>
    AZURE_SEARCH_CONNECTION_NAME=<your Azure Search connection name>
    ```
Replace the placeholders with the following values:

* Find the `<your subscription id>`, `<your resource group>`, and `<your project name>` from your project view in AI Studio:
    1. In [AI Studio](https://ai.azure.com), go to your project and select **Settings** from the left pane.
    1. In the **Project properties** section, find the **Subscription ID** and **Resource group**. The **Name** field is `<your project name>`
* Still in your project **Settings**, in the **Connected resources** section, you'll see an entry for either Azure AIServices or Azure OpenAI. Select the name to open the **Connection Details**. The connection name appears at the top of the **Connection Details** page. Copy this name to use for `<your AIServices or Azure OpenAI connection name>`.
* Go back to the project **Settings** page. In the **Connected resources** section, select the link for the Azure AI Search.
    * Copy the **Target** URL for `<your Azure Search endpoint>`.
    * Copy the name at the top for `<your Azure Search connection name>`. 

    :::image type="content" source="../media/tutorials/develop-rag-copilot-sdk/search-settings.png" alt-text="Screenshot shows endpoint and connection names.":::

## Deploy models

You need two models to build a RAG-based chat app: an Azure OpenAI chat model (`gpt-3.5-turbo`) and an Azure OpenAI embedding model (`text-embedding-ada-002`). Deploy these models in your Azure AI Studio project, using this set of steps for each model.

These steps deploy a model to a real-time endpoint from the AI Studio [model catalog](../how-to/model-catalog-overview.md):

1. Sign in to [AI Studio](https://ai.azure.com) and go to the **Home** page.
1. Select **Model catalog** from the left sidebar.
1. In the **Collections** filter, select **Azure OpenAI**.

    :::image type="content" source="../media/deploy-monitor/catalog-filter-azure-openai.png" alt-text="A screenshot showing how to filter by Azure OpenAI models in the catalog." lightbox="../media/deploy-monitor/catalog-filter-azure-openai.png"::: 

1. Select the model from the Azure OpenAI collection. The first time through, select the `gpt-3.5-turbo` model. The second time, select the `text-embedding-ada-002` model.
1. Select **Deploy** to open the deployment window. 
1. Select the hub that you want to deploy the model to. Use the same hub as your project.
1. Specify the deployment name and modify other default settings depending on your requirements.
1. Select **Deploy**.
1. You land on the deployment details page. Select **Open in playground**.
1. Select **View Code** to obtain code samples that can be used to consume the deployed model in your application.
 
When you deploy the `gpt-3.5-turbo` model, find the following values in the **View Code** section, and add them to your **.env** file:

```env
AZURE_OPENAI_ENDPOINT=<endpoint_value>
AZURE_OPENAI_CHAT_DEPLOYMENT=<chat_model_deployment_name>
AZURE_OPENAI_API_VERSION=<api_version>
```

When you deploy the `text-embedding-ada-002` model, add the name to your **.env** file:

```env
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=<embedding_model_deployment_name>
```

## Install the Azure CLI and sign in 

[!INCLUDE [Install the Azure CLI](../includes/install-cli.md)]

Now we create our app and call the Azure OpenAI Service from code.

## Create a new Python environment

[!INCLUDE [Install Python](../includes/install-python.md)]

## Upgrade pip

To make sure you have the latest version of pip, run the following command:

```bash
python -m pip install --upgrade pip
```

## Install the prompt flow SDK

[Prompt flow](https://microsoft.github.io/promptflow) is a suite of development tools designed to streamline the end-to-end development cycle of LLM-based AI applications, from ideation, prototyping, testing, evaluation to production deployment and monitoring.

[!INCLUDE [Install prompt flow](../includes/install-promptflow.md)]

## Create an Azure AI Search index

The goal with this RAG-based application is to ground the model responses in your custom data. You use an Azure AI Search index that stores vectorized data from the embeddings model. The search index is used to retrieve relevant documents based on the user's question.

If you don't have an Azure AI Search index already created, we walk through how to create one. If you already have an index to use, you can skip to the [set the search environment variable](#set-search-index) section. The search index is created on the Azure AI Search service that was either created or referenced in the previous step.

1. Use your own data or [download the example Contoso Trek retail product data in a ZIP file](https://github.com/Azure-Samples/rag-data-openai-python-promptflow/blob/main/tutorial/data/product-info.zip) to your local machine. Unzip the file into your **rag-tutorial/data** folder. This data is a collection of markdown files that represent product information. The data is structured in a way that is easy to ingest into a search index. You build a search index from this data.

1. The prompt flow RAG package allows you to ingest the markdown files, locally create a search index, and register it in the cloud project. Install the prompt flow RAG package:

    ```bash
    pip install promptflow-rag
    ```

1. Create the **build_index.py** file in your **rag-tutorial** folder. 
1. Copy and paste the following code into your **build_index.py** file.

    :::code language="python" source="~/rag-data-openai-python-promptflow-main/tutorial/build_index.py":::

    - Set the `index_name` variable to the name of the index you want. 
    - As needed, you can update the `path_to_data` variable to the path where your data files are stored.

    > [!IMPORTANT]
    > By default the code sample expects the application code structure as described [previously in this tutorial](#application-code-structure). The `data` folder should be at the same level as your **build_index.py** and the downloaded `product-info` folder with md files within it.

1. From your console, run the code to build your index locally and register it to the cloud project:

    ```bash
    python build_index.py
    ```

1. Once the script is run, you can view your newly created index in the **Indexes** page of your Azure AI Studio project. For more information, see [How to build and consume vector indexes in Azure AI Studio](../how-to/index-add.md).

1. If you run the script again with the same index name, it creates a new version of the same index.

### <a name="set-search-index"></a> Set the search index environment variable

Once you have the index name you want to use (either by creating a new one, or referencing an existing one), add it to your **.env** file, like this:

```env
AZUREAI_SEARCH_INDEX_NAME=<index-name>
```

## Develop custom RAG code

Next you create custom code to add retrieval augmented generation (RAG) capabilities to a basic chat application. In the quickstart, you created **chat.py** and **chat.prompty** files. Here you expand on that code to include RAG capabilities.

The chat app with RAG implements the following general logic:

1. Generate a search query based on user query intent and any chat history
1. Use an embedding model to embed the query
1. Retrieve relevant documents from the search index, given the query
1. Pass the relevant context to the Azure OpenAI chat completion model
1. Return the response from the Azure OpenAI model

### The chat app implementation logic

The chat app implementation logic is in the **copilot.py** file. This file contains the core logic for the RAG-based chat app.

1. Create a folder named **copilot_flow** in the **rag-tutorial** folder. 
1. Then create a file called **copilot.py** in the **copilot_flow** folder.
1. Add the following code to the **copilot.py** file:

    :::code language="python" source="~/rag-data-openai-python-promptflow-main/tutorial/copilot_flow/copilot.py":::

The **copilot.py** file contains two key functions: `get_documents()` and `get_chat_response()`.

Notice these two functions have the `@trace` decorator, which allows you to see the prompt flow tracing logs of each function call inputs and outputs. `@trace` is an alternative and extended approach to the way the [quickstart](../quickstarts/get-started-code.md) showed tracing capabilities.

The `get_documents()` function is the core of the RAG logic.
1. Takes in the search query and number of documents to retrieve.
1. Embeds the search query using an embedding model.
1. Queries the Azure Search index to retrieve the documents relevant to the query.
1. Returns the context of the documents.
    
The `get_chat_response()` function builds from the previous logic in your **chat.py** file:
1. Takes in the `chat_input` and any `chat_history`.
1. Constructs the search query based on `chat_input` intent and `chat_history`.
1. Calls `get_documents()` to retrieve the relevant docs.
1. Calls the chat completion model with context to get a grounded response to the query.
1. Returns the reply and context. We set a typed dictionary as the return object for our `get_chat_response()` function. You can choose how your code returns the response to best fit your use case.

The `get_chat_response()` function uses two `Prompty` files to make the necessary Large Language Model (LLM) calls, which we cover next.

### Prompt template for chat

The **chat.prompty** file is simple, and similar to the **chat.prompty** in the [quickstart](../quickstarts/get-started-code.md). The system prompt is updated to reflect our product and the prompt templates includes document context.

1. Add the file **chat.prompty** in the **copilot_flow** directory. The file represents the call to the chat completion model, with the system prompt, chat history, and document context provided.
1. Add this code to the **chat.prompty** file:

    :::code language="yaml" source="~/rag-data-openai-python-promptflow-main/tutorial/copilot_flow/chat.prompty":::

### Prompt template for chat history

Because we're implementing a RAG-based application, there's some extra logic required for retrieving relevant documents not only for the current user query, but also taking into account chat history. Without this extra logic, your LLM call would account for chat history. But you wouldn't retrieve the right documents for that context, so you wouldn't get the expected response.

For instance, if the user asks the question "is it waterproof?", we need the system to look at the chat history to determine what the word "it" refers to, and include that context into the search query to embed. This way, we retrieve the right documents for "it" (perhaps the Alpine Explorer Tent) and its "cost."

Instead of passing only the user's query to be embedded, we need to generate a new search query that takes into account any chat history. We use another `Prompty` (which is another LLM call) with specific prompting to interpret the user query **intent** given chat history, and construct a search query that has the necessary context.

1. Create the file **queryIntent.prompty** in the **copilot_flow** folder. 
1. Enter this code for specific details about the prompt format and few-shot examples.

    :::code language="yaml" source="~/rag-data-openai-python-promptflow-main/tutorial/copilot_flow/queryIntent.prompty":::

The simple system message in our **queryIntent.prompty** file achieves the minimum required for the RAG solution to work with chat history.

### Configure required packages

Create the file **requirements.txt** in the **copilot_flow** folder. Add this content:

:::code language="txt" source="~/rag-data-openai-python-promptflow-main/tutorial/copilot_flow/requirements.txt":::

These packages are required for the flow to run locally and in a deployed environment.

### Use flex flow

As previously mentioned, this implementation uses prompt flow's flex flow, which is the code-first approach to implementing flows. You specify an entry function (which is defined in **copilot.py**). Learn more at [Develop a flex flow](https://microsoft.github.io/promptflow/how-to-guides/develop-a-flex-flow/index.html).

This yaml specifies the entry function, which is the `get_chat_response` function defined in `copilot.py`. It also specifies the requirements the flow needs to run.

Create the file **flow.flex.yaml** in the **copilot_flow** folder. Add this content:

:::code language="yaml" source="~/rag-data-openai-python-promptflow-main/tutorial/copilot_flow/flow.flex.yaml":::

## Use prompt flow to test your chat app

Use prompt flow's testing capability to see how your chat app performs as expected on sample inputs. By using your **flow.flex.yaml** file, you can use prompt flow to test with your specified inputs.

Run the flow using this prompt flow command:

```bash
pf flow test --flow ./copilot_flow --inputs chat_input="how much do the Trailwalker shoes cost?"
```

Alternatively, you can run the flow interactively with the `--ui` flag. 

```bash
pf flow test --flow ./copilot_flow --ui
```

When you use `--ui`, the interactive sample chat experience opens a window in your local browser. 
- The first time you run with the `--ui` flag, you need to manually select your chat inputs and outputs from the options. The first time you create this session, select the **Chat input/output field config** settings, then start chatting. 
- The next time you run with the `--ui` flag, the session will remember your settings.

:::image type="content" source="../media/tutorials/develop-rag-copilot-sdk/flow-test-ui.png" alt-text="Screenshot that shows the sample chat experience." lightbox="../media/tutorials/develop-rag-copilot-sdk/flow-test-ui.png":::

When you're finished with your interactive session, enter **Ctrl + C** in the terminal window to stop the server.

### Test with chat history

In general, prompt flow and `Prompty` support chat history. If you test with the `--ui` flag in the locally served front end, prompt flow manages your chat history. If you test without the `--ui`, you can specify an inputs file that includes chat history.

Because our application implements RAG, we had to add [extra logic to handle chat history](#prompt-template-for-chat-history) in the **queryIntent.prompty** file.

To test with chat history, create a file called **input_with_chat_history.json** in the **copilot_flow** folder, and paste in this content:

:::code language="json" source="~/rag-data-openai-python-promptflow-main/tutorial/copilot_flow/input_with_chat_history.json":::

To test with this file, run:

```bash
pf flow test --flow ./copilot_flow --inputs ./copilot_flow/input_with_chat_history.json
```

The expected output is something like: "The Alpine Explorer Tent is priced at $350."

This system is able to interpret the intent of the query "how much does it cost?" to know that "it" refers to the Alpine Explorer Tent, which was the latest context in the chat history. Then the system constructs a search query for the price of the Alpine Explorer Tent to retrieve the relevant documents for the Alpine Explorer Tent's cost, and we get the response.

If you navigate to the trace from this flow run, you see the conversation in action. The local traces link shows in the console output before the result of the flow test run.

:::image type="content" source="../media/tutorials/develop-rag-copilot-sdk/trace-for-chat-history.png" alt-text="Screenshot shows the console output for the prompt flow." lightbox="../media/tutorials/develop-rag-copilot-sdk/trace-for-chat-history.png" :::

## Clean up resources

To avoid incurring unnecessary Azure costs, you should delete the resources you created in this tutorial if they're no longer needed. To manage resources, you can use the [Azure portal](https://portal.azure.com?azure-portal=true).

But don't delete them yet, if you want to deploy your chat app to Azure in [the next part of this tutorial series](copilot-sdk-evaluate-deploy.md).

## Next step

> [!div class="nextstepaction"]
> [Part 3: Evaluate and deploy your chat app to Azure](copilot-sdk-evaluate-deploy.md)
