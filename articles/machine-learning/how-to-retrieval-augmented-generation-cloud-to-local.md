---
title: Work with RAG prompt flows locally (preview)
titleSuffix: Azure Machine Learning
description: Learn to work with your Azure Machine Learning (RAG) prompt flows locally by using the Prompt flow extension in Visual Studio Code.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: prompt-flow
ms.topic: concept-article
author: lgayhardt
ms.author: lagayhar
ms.reviewer: chenlujiao
ms.date: 10/11/2024
ms.custom:
  - prompt-flow
  - ignite-2023
---

# Work with RAG prompt flows locally (preview)

[Retrieval Augmented Generation (RAG)](concept-retrieval-augmented-generation.md) is a pattern that works with pretrained Large Language Models (LLM) and your own data to generate responses. You can implement RAG in a prompt flow in Azure Machine Learning.

In this article, you learn how to transition RAG flows from your Azure Machine Learning cloud workspace to a local device and work with them by using the **Prompt flow** extension in Visual Studio Code.

> [!IMPORTANT]
> RAG is currently in public preview. This preview is provided without a service-level agreement, and isn't recommended for production workloads. Certain features might not be supported or might have constrained capabilities.
> For more information, see [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).

## Prerequisites

- Python installed locally

  - The **promptflow** SDK and **promptflow-tools** packages installed by running<br>`pip install promptflow promptflow-tools`
  - The **promptflow-vectordb** tool installed by running<br>`pip install promptflow-vectordb`

- Visual Studio Code with the **Python** and **Prompt flow** extensions installed

  :::image type="content" source="./media/how-to-retrieval-augmented-generation-cloud-to-local/vs-code-extension.png" alt-text="Screenshot of the prompt flow VS Code extension in the marketplace.":::

- An [Azure OpenAI account resource](/azure/ai-services/openai/how-to/create-resource#create-a-resource) that has [model deployments](/azure/ai-services/openai/how-to/create-resource#deploy-a-model) for both **chat** and **text-embedding-ada**

- A [vector index created](how-to-create-vector-index.md) in Azure Machine Learning studio for the example prompt flow to use

## Create the prompt flow

This tutorial uses the sample **Q&A on Your Data** RAG prompt flow, which contains a **lookup** node that uses the vector index lookup tool to search questions from the indexed docs stored in the workspace storage blob.

1. On the **Connections** tab of the Azure Machine Learning studio **Prompt flow** page, [set up a connection](prompt-flow/get-started-prompt-flow.md#set-up-connection) to your Azure OpenAI resource if you don't already have one. If you use an Azure AI Search index as the data source for your vector index, you must also have an Azure AI Search connection.

1. On the Azure Machine Learning studio **Prompt flow** page, select **Create**.

1. On the **Create a new flow** screen, select **Clone** on the **Q&A on Your Data** tile to clone the example prompt flow.

   The cloned flow opens in the authoring interface.

   :::image type="content" source="./media/how-to-retrieval-augmented-generation-cloud-to-local/my-flow.png" alt-text="Screenshot of bring your own data QnA in the Azure Machine Learning studio." lightbox = "./media/how-to-retrieval-augmented-generation-cloud-to-local/my-flow.png":::

1. In the **lookup** step of your cloned flow, populate the **mlindex_content** input with your vector index information.

   :::image type="content" source="./media/how-to-retrieval-augmented-generation-cloud-to-local/embed-question.png" alt-text="Screenshot of lookup node in studio showing inputs.":::

1. Populate the **answer_the_question_with_context** step with your **Connection** and **Deployment** information for the **chat** API.

   :::image type="content" source="./media/how-to-retrieval-augmented-generation-cloud-to-local/my-cloud-connection.png" alt-text="Screenshot of answer_the_question_with_context node in studio showing inputs.":::

1. Make sure the example flow runs correctly, and save it.

1. Select the **Download** icon at the upper right of the **Files** section. The flow files download as a ZIP package to your local machine.

   :::image type="content" source="./media/how-to-retrieval-augmented-generation-cloud-to-local/download.png" alt-text="Screenshot of the Files section of the authoring page with the Download icon highlighted.":::

1. Unzip the package to a folder.

## Work with the flow in VS Code

The rest of this article details how to use the VS Code Prompt flow extension to edit the flow. If you don't want to use the Prompt flow extension, you can open the unzipped folder in any integrated development environment (IDE) and use the CLI to edit the files. For more information, see [Prompt flow quick start](https://microsoft.github.io/promptflow/how-to-guides/quick-start.html#quick-start).

1. In VS Code with the Prompt flow extension enabled, open the unzipped prompt flow folder.

1. Select the **Prompt flow** icon in the left menu to open the Prompt flow management pane.

   :::image type="content" source="./media/how-to-retrieval-augmented-generation-cloud-to-local/vs-code-extension-toolbar.png" alt-text="Screenshot of the prompt flow VS Code extension icon in the VS Code left menu.":::

1. Select **Install dependencies** in the management pane and make sure the correct Python interpreter is selected, and the **promptflow** and **promptflow-tools** packages are installed.

### Create the connections

To use the vector index lookup tool locally, you need to create the same connections to the vector index service as you did in the cloud.

1. Expand the **Connections** section at the bottom of the Prompt flow management pane, and select the **+** icon next to the **AzureOpenAI** connection type.

   :::image type="content" source="./media/how-to-retrieval-augmented-generation-cloud-to-local/vs-code-connection-create.png" alt-text="Screenshot of creating the connections in VS Code." lightbox = "./media/how-to-retrieval-augmented-generation-cloud-to-local/vs-code-connection-create.png":::

1. A *new_AzureOpenAI_connection.yaml* file opens in the editing pane. Edit this file to add your Azure OpenAI connection `name` and `api_base` or endpoint. Don't enter your `api_key` information yet.

   :::image type="content" source="./media/how-to-retrieval-augmented-generation-cloud-to-local/flow-download.png" alt-text="Screenshot of the file for creating an Azure OpenAI connection." lightbox = "./media/how-to-retrieval-augmented-generation-cloud-to-local/flow-download.png":::

1. Select the **Create connection** link at the bottom of the file. The app runs to create the connection. When prompted, enter the API key for your connection in the terminal.

1. If you used an Azure AI Search index as the data source for your vector index, also create a new Azure AI Search connection for the local vector index lookup tool to use. For more information, see [Index Lookup tool for Azure Machine Learning (Preview)](prompt-flow/tools-reference/index-lookup-tool.md).

### Check the files

1. Open the *flow.dag.yaml* file and select the **Visual editor** link at the top of the file.

   :::image type="content" source="./media/how-to-retrieval-augmented-generation-cloud-to-local/visual-editor.png" alt-text="Screenshot of the flow dag yaml file with the visual editor highlighted in VS Code." lightbox = "./media/how-to-retrieval-augmented-generation-cloud-to-local/visual-editor.png":::

1. In the visual editor version of *flow.dag.yaml*, scroll to the **lookup** node, which consumes the vector index lookup tool in this flow. Under **mlindex_content**, check the paths and connections for your **embeddings** and **index**.

   :::image type="content" source="./media/how-to-retrieval-augmented-generation-cloud-to-local/search-blob.png" alt-text="Screenshot of indexed docs node in VS Code showing the inputs.":::

   > [!NOTE]
   > If your indexed docs are a data asset in your workspace, local consumption requires Azure authentication. Make sure you're signed in to the correct Azure tenant and connected to your Azure Machine Learning workspace.

1. Select the **Edit** icon in the **queries** input box, which opens the raw *flow.dag.yaml* file to the `lookup` node definition.

1. Ensure that the value of the `tool` section in this node is set to `promptflow_vectordb.tool.vector_index_lookup.VectorIndexLookup.search`, which is the local version of the vector index lookup tool.

   :::image type="content" source="./media/how-to-retrieval-augmented-generation-cloud-to-local/search-tool.png" alt-text="Screenshot of the tool section of the lookup node.":::

   >[!NOTE]
   >If you have any issues with the local `promptflow_vectordb` tool, see [Package tool isn't found error](prompt-flow/tools-reference/troubleshoot-guidance.md#package-tool-isnt-found-error-occurs-when-you-update-the-flow-for-a-code-first-experience) and [Migrate from legacy tools to the Index Lookup tool](/azure/ai-studio/how-to/prompt-flow-tools/index-lookup-tool#migrate-from-legacy-tools-to-the-index-lookup-tool) for troubleshooting.

1. Scroll to the **generate_prompt_context** node, and in the raw *flow.dag.yaml* file, select the **Open code file** link.

1. In the Python code file, make sure the package name of the vector tool is `promptflow_vectordb`.

    :::image type="content" source="./media/how-to-retrieval-augmented-generation-cloud-to-local/generate-node.png" alt-text="Screenshot of the Python code file with the vector tool package name highlighted.":::

1. Scroll to the **answer_the_question_with_context** node and make sure it uses the local connection you created. Check the **deployment_name**, which is the model you use here for the embedding.

   :::image type="content" source="./media/how-to-retrieval-augmented-generation-cloud-to-local/answer-connection.png" alt-text="Screenshot of answer the question with context node with the connection highlighted.":::

### Test and run the flow

Scroll to the top of the flow and fill in the **Inputs** value with a single question for this test run, such as **How to use SDK V2?**, and then select the **Run** icon to run the flow.

:::image type="content" source="./media/how-to-retrieval-augmented-generation-cloud-to-local/flow-run.png" alt-text="Screenshot of the flow dag YAML file showing inputs and highlighting value of the question input and run button.":::

For more information about batch run and evaluation, see [Submit flow run to Azure Machine Learning workspace](prompt-flow/how-to-integrate-with-llm-app-devops.md).

## Related content

- [Get started with prompt flow](prompt-flow/get-started-prompt-flow.md)
- [Create a vector index in an Azure Machine Learning prompt flow (preview)](how-to-create-vector-index.md)
- [Use Index Lookup tool for Azure AI Foundry](/azure/ai-studio/how-to/prompt-flow-tools/index-lookup-tool)
- [Integrate prompt flow with LLM-based application DevOps](prompt-flow/how-to-integrate-with-llm-app-devops.md)
