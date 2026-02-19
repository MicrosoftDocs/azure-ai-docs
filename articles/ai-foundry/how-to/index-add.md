---
title: Build and Consume Vector Indexes
titleSuffix: Microsoft Foundry
description: Learn how to create and use a vector index for performing retrieval-augmented generation (RAG) by using Microsoft Foundry portal.
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.custom:
  - ignite-2023
  - build-2024
  - ignite-2024
ms.topic: how-to
ms.date: 11/21/2025
ms.reviewer: estraight
ms.author: ssalgado
manager: nitinme
author: ssalgadodev
---

# Build and consume vector indexes in Microsoft Foundry portal

[!INCLUDE [classic-banner](../includes/classic-banner.md)]

[!INCLUDE [feature-preview](../includes/feature-preview.md)]

In this article, you learn how to create and use a vector index for performing [retrieval-augmented generation (RAG)](../concepts/retrieval-augmented-generation.md) in the Microsoft Foundry portal.

A vector index isn't required for RAG, but a vector query can match on semantically similar content, which is useful for RAG workloads.

## Prerequisites

- A [Foundry project](create-projects.md).

- An [Azure AI Search resource](/azure/search/search-create-service-portal).

- You should have content in a supported format that provides sufficient information for a chat experience. It can be an existing index on Azure AI Search, or you can create a new index using content files in Azure Blob Storage, your local system, or data in Foundry.

- You should have content in a supported format that provides sufficient information for a chat experience. It can be an existing index on Azure AI Search, or you can create a new index using content files in Azure Blob Storage, your local system, or data in Foundry.

## Create an index from the Chat playground

[!INCLUDE [tip-left-pane](../includes/tip-left-pane.md)]

1. Sign in to the [Foundry portal](https://ai.azure.com/?cid=learnDocs).

1. Go to your project or [create a new project](../how-to/create-projects.md) in your Foundry resource.

1. From the sidebar menu, select **Playgrounds**. Select **Try the Chat playground**.

    :::image type="content" source="../media/index-retrieve/project-left-menu.png" alt-text="Screenshot of Project Left Menu." lightbox="../media/index-retrieve/project-left-menu.png":::

1. Select a deployed chat completion model. If you don't have one, deploy a model by selecting **Create new deployment**, then choose a model.

   :::image type="content" source="../media/index-retrieve/create-deployment.png" alt-text="Screenshot of create a deployment button." lightbox="../media/index-retrieve/create-deployment.png":::

1. Scroll to the bottom of the model window. Select **+ Add a new data source**.

   :::image type="content" source="../media/index-retrieve/add-your-data.png" alt-text="Screenshot of the add your data section." lightbox="../media/index-retrieve/add-your-data.png":::

1. Choose your **Source data**. You can choose source data from a list of your recent data sources, a storage URL on the cloud, or upload files and folders from the local machine. You can also add a connection to another data source such as Azure Blob Storage.

   If you don't have sample data, you can [download these PDFs](https://github.com/Azure-Samples/azure-search-sample-data/tree/main/health-plan) to your local system, and then upload them as your source data.

    :::image type="content" source="../media/index-retrieve/select-source-data.png" alt-text="Screenshot of select source data." lightbox="../media/index-retrieve/select-source-data.png":::

1. Select **Next** after choosing source data.

1. In the **Index configuration** tab, choose the **Index storage** location where you want your index to be stored.

1. If you already have an Azure AI Search resource, you can browse the list of search service resources for your subscription and then select **Connect** for the one you want to use. If you're connecting with API keys, confirm your search service [uses API keys](/azure/search/search-security-api-keys).

    :::image type="content" source="../media/index-retrieve/index-storage.png" alt-text="Screenshot of select index store." lightbox="../media/index-retrieve/index-storage.png":::

    If you don't have an existing resource, choose **Create a new Azure AI Search resource**. Select **Next**.
  
1. Select the Azure OpenAI connection you want to use. Select **Next**.

1. Review the details you entered and select **Create vector index**.

1. You're taken to the index details page where you can see the status of your index creation.

## Use an index in prompt flow

1. Under **Build and customize** in the sidebar menu, select **Prompt flow**.

1. Open an existing prompt flow or select **+ Create** to create a new flow.

1. Select **Create** in the **Chat flow** tile, then select **Create** again.

1. Select **Start compute session**, and wait a few minutes for the compute session to begin.

1. Select **More tools**, and then select **Index Lookup**.

    :::image type="content" source="../media/index-retrieve/index-lookup-tool.png" alt-text="Screenshot of Vector index Lookup from More Tools." lightbox="../media/index-retrieve/index-lookup-tool.png":::

1. Provide a node name for your Index Lookup Tool and select **Add**.

1. Select the **mlindex_content** value box, and select your index from the value section. After completing this step, enter the queries and **query_types** to be performed against the index.

   :::image type="content" source="../media/index-retrieve/configure-index-lookup-tool.png" alt-text="Screenshot of the prompt flow node to configure index lookup." lightbox="../media/index-retrieve/configure-index-lookup-tool.png":::


## Related content

- [Retrieval augmented generation and indexes](../concepts/retrieval-augmented-generation.md)
- [Build and consume an index using code](../tutorials/copilot-sdk-create-resources.md)
