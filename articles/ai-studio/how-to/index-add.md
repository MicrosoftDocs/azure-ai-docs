---
title: How to build and consume vector indexes in Azure AI Foundry portal
titleSuffix: Azure AI Foundry
description: Learn how to create and use a vector index for performing Retrieval Augmented Generation (RAG).
manager: scottpolly
ms.service: azure-ai-studio
ms.custom:
  - ignite-2023
  - build-2024
  - ignite-2024
ms.topic: how-to
ms.date: 12/11/2024
ms.reviewer: estraight
ms.author: ssalgado
author: ssalgadodev
---

# How to build and consume vector indexes in Azure AI Foundry portal

[!INCLUDE [feature-preview](../includes/feature-preview.md)]

In this article, you learn how to create and use a vector index for performing [Retrieval Augmented Generation (RAG)](../concepts/retrieval-augmented-generation.md).

## Prerequisites

You must have:
- An Azure AI Foundry project
- An Azure AI Search resource

## Create an index from the Chat playground

1. Sign in to [Azure AI Foundry](https://ai.azure.com).
1. Go to your project or [create a new project](../how-to/create-projects.md) in Azure AI Foundry portal.
1. From the menu on the left, select **Playgrounds**.


    :::image type="content" source="../media/index-retrieve/project-left-menu.png" alt-text="Screenshot of Project Left Menu." lightbox="../media/index-retrieve/project-left-menu.png":::

1. Select a deployed model. If you have not done so already, deploy a model by selecting **Create new deployment**.

   :::image type="content" source="../media/index-retrieve/create-deployment.png" alt-text="Screenshot of create a deployment button." lightbox="../media/index-retrieve/create-deployment.png":::
   
1. Scroll to the bottom of the model window. Select **+ Add a new data source**

   :::image type="content" source="../media/index-retrieve/add-your-data.png" alt-text="Screenshot of the add your data section." lightbox="../media/index-retrieve/add-your-data.png":::
   
1. Choose your **Source data**. You can choose source data from a list of your recent data sources, a storage URL on the cloud, or upload files and folders from the local machine. You can also add a connection to another data source such as Azure Blob Storage.

    :::image type="content" source="../media/index-retrieve/select-source-data.png" alt-text="Screenshot of select source data." lightbox="../media/index-retrieve/select-source-data.png":::

1. Select **Next** after choosing source data
1. Choose the **Index Storage** - the location where you want your index to be stored in the **Index configuration** tab. 
1. If you already have an Azure AI Search resource, you can choose that from the dropdown.

    :::image type="content" source="../media/index-retrieve/index-storage.png" alt-text="Screenshot of select index store." lightbox="../media/index-retrieve/index-storage.png":::

    1. If you don't have an existing resource, choose **Create a new Azure AI Search resource**. Select **Next**.
  
1. Select the Azure OpenAI connection you want to use. Select **Next**.
    
1. Enter a name you want to use for your vector index. Select **Next**.
1. Review the details you entered and select **Create**
1. You're taken to the index details page where you can see the status of your index creation.


## Use an index in prompt flow

1. Sign in to [Azure AI Foundry](https://ai.azure.com) and select your project. 
1. From the collapsible left menu, select **Prompt flow** from the **Build and customize** section.
1. Open an existing prompt flow or select **+ Create** to create a new flow.
1. On the top menu of the flow designer, select **More tools**, and then select ***Index Lookup***.

    :::image type="content" source="../media/index-retrieve/index-lookup-tool.png" alt-text="Screenshot of Vector index Lookup from More Tools." lightbox="../media/index-retrieve/index-lookup-tool.png":::

1. Provide a name for your Index Lookup Tool and select **Add**.
1. Select the **mlindex_content** value box, and select your index from the value section. After completing this step, enter the queries and **query_types** to be performed against the index.

    :::image type="content" source="../media/index-retrieve/configure-index-lookup-tool.png" alt-text="Screenshot of the prompt flow node to configure index lookup." lightbox="../media/index-retrieve/configure-index-lookup-tool.png":::

   :::image type="content" source="../media/index-retrieve/generate-index.png" alt-text="Screenshot of the prompt flow node to generate an index." lightbox="../media/index-retrieve/generate-index.png":::


## Related content

- [Learn more about RAG](../concepts/retrieval-augmented-generation.md)
- [Build and consume an index using code](./develop/index-build-consume-sdk.md)
