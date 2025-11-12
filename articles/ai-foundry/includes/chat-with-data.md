---
title: include file
description: include file
author: sdgilley
ms.reviewer: sgilley
ms.author: sgilley
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 5/21/2024
ms.custom: include, build-2024, ignite-2024
---

To complete this section, you need a local copy of product data. The [Azure-Samples/rag-data-openai-python-promptflow repository on GitHub](https://github.com/Azure-Samples/rag-data-openai-python-promptflow/) contains sample retail product information that's relevant for this tutorial scenario. Specifically, the `product_info_11.md` file contains product information about the TrailWalker hiking shoes that's relevant for this tutorial example. [Download the example Contoso Trek retail product data in a ZIP file](https://github.com/Azure-Samples/rag-data-openai-python-promptflow/raw/refs/heads/main/tutorial/data/product-info.zip) to your local machine. 

Follow these steps to add your data in the chat playground to help the assistant answer questions about your products. You're not changing the deployed model itself. Your data is stored separately and securely in your Azure subscription.

1. Go to your project in [Microsoft Foundry](https://ai.azure.com/?cid=learnDocs). 
1. Select **Playgrounds** from the left pane.
1. Select **Try the chat playground**.
1. Select your deployed chat model from the **Deployment** dropdown. 

    :::image type="content" source="../media/tutorials/chat/playground-chat.png" alt-text="Screenshot of the chat playground with the chat mode and model selected." lightbox="../media/tutorials/chat/playground-chat.png":::
 
1. On the left side of the chat playground, select **Add your data** > **+ Add a new data source**.

    :::image type="content" source="../media/tutorials/chat/add-your-data.png" alt-text="Screenshot of the chat playground with the option to add a data source visible." lightbox="../media/tutorials/chat/add-your-data.png":::

1. In the **Data source** dropdown, select **Upload files**. 

    :::image type="content" source="../media/tutorials/chat/add-your-data-source.png" alt-text="Screenshot of the data source selection options." lightbox="../media/tutorials/chat/add-your-data-source.png":::

1. Select **Upload** > **Upload files** to browse your local files. 

1. Select the files you want to upload. Select the product information files that you [downloaded](https://github.com/Azure-Samples/rag-data-openai-python-promptflow/raw/refs/heads/main/tutorial/data/product-info.zip) or created earlier. Add all of the files now. You won't be able to add more files later in the same playground session. 

1. Select **Upload** to upload the file to your Azure Blob storage account. Then select **Next**.

   :::image type="content" source="../media/tutorials/chat/add-your-data-uploaded.png" alt-text="Screenshot of the dialog to select and upload files." lightbox="../media/tutorials/chat/add-your-data-uploaded.png":::

1. Select your **Azure AI Search** service.

1. For the **Vector index name**, enter *product-info* and select **Next**.

1. On the **Search settings** page under **Vector settings**, deselect the **Add vector search to this search resource** checkbox. This setting helps determine how the model responds to requests. Then select **Next**.
    
    > [!NOTE]
    > If you add vector search, more options would be available here for an additional cost. 

1. Review your settings and select **Create vector index**.

1. In the playground, you can see that your data ingestion is in progress. This process might take several minutes. Before proceeding, wait until you see the data source and index name in place of the status. 

   :::image type="content" source="../media/tutorials/chat/add-your-data-ingestion-in-progress.png" alt-text="Screenshot of the chat playground with the status of data ingestion in view." lightbox="../media/tutorials/chat/add-your-data-ingestion-in-progress.png":::

1. You can now chat with the model asking the same question as before ("How much are the TrailWalker hiking shoes"), and this time it uses information from your data to construct the response. You can expand the **references** button to see the data that was used.
