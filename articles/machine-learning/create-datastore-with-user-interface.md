---
title: Linking Tables in OneLake to Azure Machine Learning Through UI
titleSuffix: Azure Machine Learning
description: Learn how to link a Table in OneLake Lakehouse to Azure Machine Learning and create datastore through UI.
ms.author: scottpolly
author: s-polly
ms.reviewer: soumyapatro 
ms.service: azure-machine-learning
ms.subservice: mldata
ms.topic: how-to
ms.date: 03/03/2025
#Customer intent: Existing solutions help link lakehouse files to Azure Machine Learning resources, and create a datastore through the SDK. However, some customers have lakehouse tables, and they want to create a datastore in Azure Machine Learning through the UI.
---

# Quickstart: Create a datastore in Azure Machine Learning through the UI to link a lakehouse table

Existing solutions can link an Azure Machine Learning resource to OneLake, extract the data, and create a datastore in Azure Machine Learning. However, [in those solutions](#references), the OneLake data is of type "Files." Those solutions don't work for OneLake table-type data, as shown in the following screenshot:

:::image type="content" source="media/create-datastore-with-user-interface/show-fabric-table.png" alt-text="Screenshot showing a table in Microsoft Fabric." lightbox="./media/create-datastore-with-user-interface/show-fabric-table.png":::

Additionally, some customers might prefer to build the link in the UI. A solution that links Azure Machine Learning resources to OneLake tables is needed.
In this article, you learn how to link OneLake tables to Azure Machine Learning studio resources through the UI.

## Prerequisites

- An Azure subscription; if you don't have an Azure subscription, [create a free account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn) before you start.
- An Azure Machine Learning workspace. Visit [Create workspace resources](./quickstart-create-resources.md).
- An Azure Data Lake Storage (ADLS) storage account. Visit [Create an Azure Data Lake Storage (ADLS) storage account](/azure/storage/blobs/create-data-lake-storage-account).
- Knowledge of assigning roles in Azure storage account.

## Solution structure

This solution has three parts. First, create and set up a Data Lake Storage account in the Azure portal. Next, copy the data from OneLake to Azure Data Lake Storage. Bring the data to the Azure Machine Learning resource, and lastly, create the datastore. The following screenshot shows the overall flow of the solution:

:::image type="content" source="media/create-datastore-with-user-interface/overall-idea.png" alt-text="Screenshot showing the overall flow of the solution." lightbox="./media/create-datastore-with-user-interface/overall-idea.png":::

## Set up the Data Lake storage account in the Azure portal

Assign the **Storage Blob Data Contributor** and **Storage File Data Privileged Contributor** roles to the user identity or service principal, to enable key access and **creating container** permissions. To assign appropriate roles to the user identity:

1. Open the [Microsoft Azure portal](https://portal.azure.com)
1. Select the **Storage accounts** service.

    :::image type="content" source="media/apache-spark-environment-configuration/find-storage-accounts-service.png" lightbox="media/apache-spark-environment-configuration/find-storage-accounts-service.png" alt-text="Screenshot showing selection of Storage Accounts service.":::

1. On the **Storage accounts** page, select the Data Lake Storage account you created in the prerequisite step. A page showing the storage account properties opens.

     :::image type="content" source="media/create-datastore-with-user-interface/create-storage-account.png" alt-text="Screenshot showing the properties page of the data lake storage account." lightbox="./media/create-datastore-with-user-interface/create-storage-account.png":::

1. Select the  **Access keys** from the left panel and record the key. This value is required in a later step.

1. Select and enable **Allow storage account key access** as shown in the following screenshot:

    :::image type="content" source="media/create-datastore-with-user-interface/enable-key-access.png" alt-text="Screenshot showing how to enable key access of data lake storage account in Azure portal." lightbox="./media/create-datastore-with-user-interface/enable-key-access.png":::

1. Select **Access Control (IAM)** from left panel, and assign the **Storage Blob Data Contributor** and **Storage File Data Privileged Contributor** roles to the service principal.

    :::image type="content" source="media/create-datastore-with-user-interface/assign-roles.png" alt-text="Screenshot showing how to assign roles of data lake storage account in Azure portal." lightbox="./media/create-datastore-with-user-interface/assign-roles.png":::

1. Create a container in the storage account. Name it **onelake-table**.

    :::image type="content" source="media/create-datastore-with-user-interface/create-container.png" alt-text="Screenshot showing creation of a data lake storage account container in the Azure portal." lightbox="./media/create-datastore-with-user-interface/create-container.png":::

## Use a Fabric data pipeline to copy data to an Azure Data Lake Storage account

1. At the Fabric portal, select **Data pipeline** at the New item page.

    :::image type="content" source="media/create-datastore-with-user-interface/create-pipeline.png" alt-text="Screenshot showing selection of data pipeline at the Fabric New item page." lightbox="./media/create-datastore-with-user-interface/create-pipeline.png":::

1. Select **Copy data assistant**.

    :::image type="content" source="media/create-datastore-with-user-interface/copy-data-assistant.png" alt-text="Screenshot showing selection of Copy data assistant." lightbox="./media/create-datastore-with-user-interface/copy-data-assistant.png":::

1. In  **Copy data assistant**, select **Azure Blobs**:

    :::image type="content" source="media/create-datastore-with-user-interface/select-azure-blob.png" alt-text="Screenshot showing selection of Select Azure blobs in the Fabric Copy data assistant." lightbox="./media/create-datastore-with-user-interface/select-azure-blob.png":::

1. To create a connection to the Azure Data Lake storage account, select **Authentication kind: Account key** and then **Next**:

    <!-- Maybe place a red highlight box around "Authentication kind: Account key" -->

    :::image type="content" source="media/create-datastore-with-user-interface/create-connection.png" alt-text="Screenshot that shows how to create a connection in a Fabric data pipeline." lightbox="./media/create-datastore-with-user-interface/create-connection.png":::

1. Select the data destination, and select Next:

    <!-- Maybe place red highlight boxes around "OK" and "Next" -->

    :::image type="content" source="media/create-datastore-with-user-interface/select-destination-folder.png" alt-text="Screenshot that shows selection of the data destination." lightbox="./media/create-datastore-with-user-interface/select-destination-folder.png":::

1. Connect to the data destination, and select Next:

    :::image type="content" source="media/create-datastore-with-user-interface/connect-data-destination.png" alt-text="Screenshot that shows connection to the data destination." lightbox="./media/create-datastore-with-user-interface/connect-data-destination.png":::

1. That step automatically starts the data copy job:

    <!-- This image does not seem to highlight how to start the data copy job - it does not seem to highlight a control that actually starts the data copy job -->

    :::image type="content" source="media/create-datastore-with-user-interface/copy-activity-scheduled.png" alt-text="Screenshot that shows the copy activity is scheduled." lightbox="./media/create-datastore-with-user-interface/copy-activity-scheduled.png":::

    This step might take a while. It directly leads to the next step.

1. Check that the data copy job finished successfully:

    :::image type="content" source="media/create-datastore-with-user-interface/copy-activity-success.png" alt-text="Screenshot showing that the copy operation succeeded." lightbox="./media/create-datastore-with-user-interface/copy-activity-success.png":::

## Create datastore in Azure Machine Learning linking to Azure Data Lake Storage container

Now that your data is in the Azure Data Lake storage resource, you can create an Azure Machine Learning datastore.

1. In Azure storage account, the **container** as shown on the left has data, as shown on the right:

    <!-- This image does not seem to highlight how to verify that the container has the actual data. Also,
         did the earlier steps show that we gave the container the name "onelake-table"? 
    
         The create-container.png image step created the **onelake-table** container.-->

    :::image type="content" source="media/create-datastore-with-user-interface/check-container.png" alt-text="Screenshot that shows how to verify the data in Azure storage account container." lightbox="./media/create-datastore-with-user-interface/check-container.png":::

1. In Machine Learning studio create data asset, select the **File (uri_file)** type:

    :::image type="content" source="media/create-datastore-with-user-interface/create-data-asset.png" alt-text="Screenshot showing selection of the File (uri_file) type." lightbox="./media/create-datastore-with-user-interface/create-data-asset.png":::

1. Select **From Azure storage**:

    :::image type="content" source="media/create-datastore-with-user-interface/select-azure-storage.png" alt-text="Screenshot that shows how to select Azure storage." lightbox="./media/create-datastore-with-user-interface/select-azure-storage.png":::

1. Using the **Account key** value from the earlier **Create a connection to the Azure Data Lake storage account** step, create a **New datastore**:

    :::image type="content" source="media/create-datastore-with-user-interface/new-datastore.png" alt-text="Screenshot that shows how to create new datastore in Azure Machine Learning." lightbox="./media/create-datastore-with-user-interface/new-datastore.png":::

1. You can also directly create a datastore in the Azure Machine Learning Studio:

    :::image type="content" source="media/create-datastore-with-user-interface/create-datastore.png" alt-text="Screenshot that shows how to create a datastore in Azure Machine Learning." lightbox="./media/create-datastore-with-user-interface/create-datastore.png":::

1. You can review details of the datastore you created:

    :::image type="content" source="media/create-datastore-with-user-interface/datastore-created.png" alt-text="Screenshot that shows details of the datastore you created." lightbox="./media/create-datastore-with-user-interface/datastore-created.png":::

1. Review the data in the datastore

    <!-- The data in the access-datastore.png image came from this

            https://microsoftlearning.github.io/mslearn-fabric/Instructions/Labs/01-lakehouse.html

        resource.  -->

    :::image type="content" source="media/create-datastore-with-user-interface/access-datastore.png" alt-text="Screenshot that shows how to access a datastore in Azure Machine Learning." lightbox="./media/create-datastore-with-user-interface/access-datastore.png":::

Now that you successfully created the datastore in Azure Machine Learning, you can use it in machine learning exercises.

## References

+ [Read from a specified table from lakehouse in One workspace using Notebook in other workspace](https://community.fabric.microsoft.com/t5/Data-Engineering/Read-from-a-specified-table-from-lakehouse-in-One-workspace/m-p/4234885)
+ [Delta Lake Tables For Optimal Direct Lake Performance In Fabric Python Notebook](https://fabric.guru/delta-lake-tables-for-optimal-direct-lake-performance-in-fabric-python-notebook)
+ [Create a OneLake (Microsoft Fabric) datastore (preview)](./how-to-datastore.md#create-a-onelake-microsoft-fabric-datastore-preview)
+ [Spark connector for Microsoft Fabric Data Warehouse](/fabric/data-engineering/spark-data-warehouse-connector)
+ [AML and OneLake and Fabric Better Together Demo](https://github.com/azeltov/aml_one_lake)