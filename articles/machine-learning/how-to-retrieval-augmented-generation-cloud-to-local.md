---
title: Retrieval Augmented Generation (RAG) cloud to local (preview)
titleSuffix: Azure Machine Learning
description: Learn to work with your Azure Machine Learning RAG prompt flows locally by using th
e prompt flow Visual Studio Code extension.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: prompt-flow
ms.topic: conceptual
author: lgayhardt
ms.author: lagayhar
ms.reviewer: chenlujiao
ms.date: 10/08/2024
ms.custom:
  - prompt-flow
  - ignite-2023
---

# RAG from cloud to local - bring your own data QnA (preview)

[Retrieval Augmented Generation (RAG)](concept-retrieval-augmented-generation.md) is a pattern that works with pretrained Large Language Models (LLM) and your own data to generate responses. You can implement RAG in a prompt flow in Azure Machine Learning.

In this article, you learn how to transition RAG flows from your Azure Machine Learning cloud workspace to a local device and work with them by using the **Prompt flow** extension in Visual Studio Code.

> [!IMPORTANT]
> RAG is currently in public preview. This preview is provided without a service-level agreement, and isn't recommended for production workloads. Certain features might not be supported or might have constrained capabilities.
> For more information, see [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).

## Prerequisites

To complete the procedures in this article, you need the following prerequisites:

- Python 3.9 or above, with the `promptflow` SDK and `promptflow-tools` installed by running `pip install promptflow promptflow-tools`, and the `promptflow-vectordb` tool installed by running `pip install promptflow-vectordb`.

- Visual Studio Code with the **Python** and **Prompt flow** extensions installed.

  :::image type="content" source="./media/how-to-retrieval-augmented-generation-cloud-to-local/vs-code-extension.png" alt-text="Screenshot of the prompt flow VS Code extension in the marketplace." lightbox = "./media/how-to-retrieval-augmented-generation-cloud-to-local/vs-code-extension.png":::

- An [Azure OpenAI account resource](/azure/ai-services/openai/how-to/create-resource#create-a-resource) that has [deployed models](/azure/ai-services/openai/how-to/create-resource#deploy-a-model) for both **chat** and **text-embedding-ada**.

- A [vector index created](how-to-create-vector-index.md) in Azure Machine Learning studio.

## Create the prompt flow

This tutorial uses the **Q&A on Your Data** RAG prompt flow, containing a **lookup** node that uses the vector index lookup tool to search questions from the indexed docs. The index docs are stored in the workspace storage blob.

1. On the **Connections** tab of the Azure Machine Learning studio **Prompt flow** page, [set up a connection](get-started-prompt-flow.md#set-up-connection) to your Azure OpenAI resource if you don't have one.

1. Select **Create** on the Azure Machine Learning studio **Prompt flow** page, and on the **Create a new flow** screen, select **Clone** on the **Q&A on Your Data** tile to clone the prompt flow.

1. In your cloned flow, populate the **answer_the_question_with_context** step with your **Connection** and **Deployment** information for the **chat** API.

   :::image type="content" source="./media/how-to-retrieval-augmented-generation-cloud-to-local/my-cloud-connection.png" alt-text="Screenshot of answer_the_question_with_context node in studio showing inputs." lightbox = "./media/how-to-retrieval-augmented-generation-cloud-to-local/my-cloud-connection.png":::

1. Populate the **mlindex_content** input in the **lookup** step with your vector index information.

   :::image type="content" source="./media/how-to-retrieval-augmented-generation-cloud-to-local/embed-question.png" alt-text="Screenshot of lookup node in studio showing inputs." lightbox = "./media/how-to-retrieval-augmented-generation-cloud-to-local/embed-question.png":::

1. Make sure the example flow runs correctly, and save it.

  :::image type="content" source="./media/how-to-retrieval-augmented-generation-cloud-to-local/my-flow.png" alt-text="Screenshot of bring your own data QnA in the Azure Machine Learning studio." lightbox = "./media/how-to-retrieval-augmented-generation-cloud-to-local/my-flow.png":::

1. Select the **Download** icon at the top of the **Files** section of the flow authoring page. The flow files download as a ZIP package to your local machine.

1. Unzip the package to a folder.

## Work with the flow in VS Code

The rest of this article details how to use the VS Code Prompt flow extension to edit the flow. If you don't want to use the Prompt flow extension, you can open the unzipped folder in any integrated development environment (IDE) and use the CLI to edit the files. For more information, see the [Prompt flow quick start](https://microsoft.github.io/promptflow/how-to-guides/quick-start.html#quick-start).

1. In VS Code with the Prompt Flow extension enabled, open the unzipped prompt flow folder.

1. Select the **Prompt flow** icon in the left menu to open the Prompt flow management pane.

### Create the connections

To use the vector index lookup tool locally, you need to create the same connections to the vector index service as you did in the cloud.

1. Expand the **Connections** section at the bottom of the Prompt flow management pane, and select the **+** icon next to the connection type **AzureOpenAI**.

   :::image type="content" source="./media/how-to-retrieval-augmented-generation-cloud-to-local/vs-code-connection-create.png" alt-text="Screenshot of creating the connections in VS Code." lightbox = "./media/how-to-retrieval-augmented-generation-cloud-to-local/vs-code-connection-create.png":::

1. A *new_AzureOpenAI_connection.yaml* file opens in the editing pane. Edit this file to add your Azure OpenAI connection `name` and `api_base` or endpoint. Note that you don't enter your `api_key` information yet.

   :::image type="content" source="./media/how-to-retrieval-augmented-generation-cloud-to-local/flow-download.png" alt-text="Screenshot of the file for creating an Azure OpenAI connection." lightbox = "./media/how-to-retrieval-augmented-generation-cloud-to-local/flow-download.png":::

1. Select the **Create connection** link at the bottom of the file. The app runs to create the connection. When prompted, enter the API key for your connection in the terminal.

> [!NOTE]
> There's a new version of the local vector index lookup tool, so you might also need to create a new Azure AI Search connection for the tool to use. For more information, see [Index Lookup tool for Azure Machine Learning (Preview)](prompt-flow/tools-reference/index-lookup-tool.md) and [Package tool isn't found error](prompt-flow/tools-reference/troubleshoot-guidance.md#package-tool-isnt-found-error-occurs-when-you-update-the-flow-for-a-code-first-experience).

### Check the files

1. Open the *flow.dag.yaml* file and select the **Visual editor** link at the top of the file.

   :::image type="content" source="./media/how-to-retrieval-augmented-generation-cloud-to-local/visual-editor.png" alt-text="Screenshot of the flow dag yaml file with the visual editor highlighted in VS Code." lightbox = "./media/how-to-retrieval-augmented-generation-cloud-to-local/visual-editor.png":::

1. In the visual editor version of *flow.dag.yaml*, scroll to the **answer_the_question_with_context** node and make sure the connection is the same as the local connection you created. Check the **deployment_name**, which is the model you use here for the embedding.

   :::image type="content" source="./media/how-to-retrieval-augmented-generation-cloud-to-local/answer-connection.png" alt-text="Screenshot of answer the question with context node with the connection highlighted." lightbox = "./media/how-to-retrieval-augmented-generation-cloud-to-local/answer-connection.png":::

1. Scroll to the **lookup** node, which consumes the vector index lookup tool in this flow. Check the path of your indexed docs you specify. All publicly accessible paths are supported, such as `https://github.com/Azure/azureml-assets/tree/main/assets/promptflow/data/faiss-index-lookup/faiss_index_sample`.

   :::image type="content" source="./media/how-to-retrieval-augmented-generation-cloud-to-local/search-blob.png" alt-text="Screenshot of search question from indexed docs node in VS Code showing the inputs." lightbox = "./media/how-to-retrieval-augmented-generation-cloud-to-local/search-blob.png":::

   > [!NOTE]
   > If your indexed docs are a data asset in your workspace, local consumption requires Azure authentication. Make sure you're signed in to Azure and connected to your Azure Machine Learning workspace.

1. Select the **Edit** icon in the **queries** input box, which opens the raw *flow.dag.yaml* file to the `lookup` node definition.

1. Ensure that the value of the `tool` section within this node is set to `promptflow_vectordb.tool.vector_index_lookup.VectorIndexLookup.search`, which is the local version of the vector index lookup tool.

   :::image type="content" source="./media/how-to-retrieval-augmented-generation-cloud-to-local/search-tool.png" alt-text="Screenshot of the tool section of the lookup node." lightbox = "./media/how-to-retrieval-augmented-generation-cloud-to-local/search-tool.png":::

1. Scroll to the **generate_prompt_context** node, and in the raw *flow.dag.yaml* file, select the **Open code file** link.

1. In the Python code file, make sure the package name of the vector tool is `promptflow_vectordb`.

    :::image type="content" source="./media/how-to-retrieval-augmented-generation-cloud-to-local/generate-node.png" alt-text="Screenshot of the generate prompt content node in VS Code highlighting the package name." lightbox = "./media/how-to-retrieval-augmented-generation-cloud-to-local/generate-node.png":::

### Test and run the flow

Scroll up to the top of the flow and fill in the **Inputs** value with a single question for this test run, for example **How to use SDK V2?**, and then select the **Run** icon to run the flow.

:::image type="content" source="./media/how-to-retrieval-augmented-generation-cloud-to-local/flow-run.png" alt-text="Screenshot of the flow dag YAML file showing inputs and highlighting value of the question input and run button." lightbox = "./media/how-to-retrieval-augmented-generation-cloud-to-local/flow-run.png":::

For more information about batch run and evaluation, see [Submit flow run to Azure Machine Learning workspace](prompt-flow/how-to-integrate-with-llm-app-devops.md)

## Related content

- [Submit runs to cloud for large scale testing and ops integration](prompt-flow/how-to-integrate-with-llm-app-devops.md#submitting-runs-to-the-cloud-from-local-repository)
