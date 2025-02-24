---
title: Linking Tables in OneLake to Azure Machine Learning Through UI
titleSuffix: Azure Machine Learning
description: Learn how to link a Table in OneLake Lakeshouse to Azure ML and create datastore through UI.
author: helenzusa1 
ms.author: helenzeng
ms.reviewer:  franksolomon
ms.service: azure-machine-learning
ms.subservice: mldata
ms.topic: how-to
ms.date: 02/14/2025
#Customer intent: Existing solutions help link Files in Lakehouse to Azure ML and create datastore through SDK, but some customers have Tables in Lakehouse, and they want to create datastore in Azure ML through UI.
---

# Quickstart: Create a datastore in Azure Maching Learning to link a Table in Lakehouse through UI

There were some existing solutions which can build a link in Azure Machine Learning to OneLake, get the data, and create a datastore in AML. However, in those solutions, the data in OneLake is of type "Files". Refer to the reference section. Some customers have data in OneLake as type "Tables." The existing solutions creating datastore in AML don’t work.

:::image type="content" source="media/create-datastore-with-UI/table-in-fabric.png" alt-text="Screenshot that shows how the table looks like in Microsoft Fabric." lightbox="./media/create-datastore-with-UI/table-in-fabric.png":::

Also some customers prefer doing in UI. Therefore, a new solution is needed to link AML to Tables in OneLake using UI.

In this article, you will learn how to link tables in OneLake to Azure Machine Learning studio through UI.

## Prerequisites
- An Azure subscription; if you don't have an Azure subscription, [create a free account](https://azure.microsoft.com/free) before you start.
- An Azure Machine Learning workspace. Visit [Create workspace resources](./quickstart-create-resources.md).
- An Azure Data Lake Storage (ADLS) storage account. Visit [Create an Azure Data Lake Storage (ADLS) storage account](/azure/storage/blobs/create-data-lake-storage-account).
- Knowledge of assigning roles in Azure storage account. 

## Overall idea

Overall there are three stages in this solution, first to create and setup a Data Lake Storage account in Azure portal, next to copy the data from OneLake to Azure Data Lake Storage, then bring it to Azure ML and create datastore.

:::image type="content" source="media/create-datastore-with-UI/overall-idea.png" alt-text="Screenshot that shows overall idea." lightbox="./media/create-datastore-with-UI/overall-idea.png":::

## Setup Data Lake Storage account in Azure portal 

This includes assigning **Storage Blob Data Contributor** and **Storage File Data Privileged Contributor** roles to the user identity or service principal, enabling key access and creating container. 

To assign appropriate roles to the user identity:

1. Open the [Microsoft Azure portal](https://portal.azure.com)
1. Search and select the **Storage accounts** service 

    :::image type="content" source="media/apache-spark-environment-configuration/find-storage-accounts-service.png" lightbox="media/apache-spark-environment-configuration/find-storage-accounts-service.png" alt-text="Expandable screenshot that shows Storage accounts service search and selection in Microsoft Azure portal.":::

1. On the **Storage accounts** page, select the Data Lake Storage account you have created in the prerequisite step. A page showing the storage account **Overview** opens

     :::image type="content" source="media/create-datastore-with-UI/create-storage-account.png" alt-text="Screenshot that shows an example of data lake storage account in Azure portal." lightbox="./media/create-datastore-with-UI/create-storage-account.png":::

1. Click the  **Access keys** from the left panel and record the key, it will be used in later step.
1. Click **Storage account key access** and enable it

    :::image type="content" source="media/create-datastore-with-UI/enable-key-access.png" alt-text="Screenshot that shows how to enable key access of data lake storage account in Azure portal." lightbox="./media/create-datastore-with-UI/enable-key-access.png":::

1. Select **Access Control (IAM)** from left panel, assign **Storage Blob Data Contributor** and **Storage File Data Privileged Contributor** to the service principal 

    :::image type="content" source="media/create-datastore-with-UI/assign-roles.png" alt-text="Screenshot that shows how to assign roles of data lake storage account in Azure portal." lightbox="./media/create-datastore-with-UI/assign-roles.png":::

1. Create a container **onelake-table** in the storage account 
    :::image type="content" source="media/create-datastore-with-UI/create-container.png" alt-text="Screenshot that shows how to create a container of data lake storage account in Azure portal." lightbox="./media/create-datastore-with-UI/create-container.png":::

## Use Data pipeline in Fabric to copy data to Azure Data Lake Storage account

1. In Fabric, create a **Data pipeline**

    :::image type="content" source="media/create-datastore-with-UI/create-pipeline.png" alt-text="Screenshot that shows how to create a data pipeline in Fabric." lightbox="./media/create-datastore-with-UI/create-pipeline.png":::

1. Use pipeline, start **Copy data assistant**

    :::image type="content" source="media/create-datastore-with-UI/copy-data-assistant.png" alt-text="Screenshot that shows how to start Copy data assistant in Fabric." lightbox="./media/create-datastore-with-UI/copy-data-assistant.png":::

1. In  **Copy data assistant**, select **Azure Blobs**

    :::image type="content" source="media/create-datastore-with-UI/select-azure-blob.png" alt-text="Screenshot that shows how to select Azure blobs in Copy data assistant in Fabric." lightbox="./media/create-datastore-with-UI/select-azure-blob.png":::

1. Create connection to the Azure Data Lake Storage account

    :::image type="content" source="media/create-datastore-with-UI/create-connection.png" alt-text="Screenshot that shows how to create connection in Fabric data pipeline." lightbox="./media/create-datastore-with-UI/create-connection.png":::

1. Select data destination

    :::image type="content" source="media/create-datastore-with-UI/select-destination-folder.png" alt-text="Screenshot that shows how to select destination folder." lightbox="./media/create-datastore-with-UI/select-destination-folder.png":::

1. Connect to data destination

    :::image type="content" source="media/create-datastore-with-UI/connect-data-destination.png" alt-text="Screenshot that shows how to connect to data destination." lightbox="./media/create-datastore-with-UI/connect-data-destination.png":::

1. Start data copy job

    :::image type="content" source="media/create-datastore-with-UI/copy-activity-scheduled.png" alt-text="Screenshot that shows the copy activity is scheduled." lightbox="./media/create-datastore-with-UI/copy-activity-scheduled.png":::

1. Check the data copy job finished successfully

    :::image type="content" source="media/create-datastore-with-UI/copy-activity-success.png" alt-text="Screenshot that shows the copy is successful." lightbox="./media/create-datastore-with-UI/copy-activity-success.png":::

## Create datastore in Azure ML linking to Azure Data Lake Storage container

Now the data is in Azure Data Lake storage, ready to create datastore in Azure ML.

1. In Azure storage account, check the data is in the designated **container**

    :::image type="content" source="media/create-datastore-with-UI/check-container.png" alt-text="Screenshot that shows how to verify the data in Azure storage account container." lightbox="./media/create-datastore-with-UI/check-container.png":::

1. In ML studio create data asset, select type **File**

    :::image type="content" source="media/create-datastore-with-UI/create-data-asset.png" alt-text="Screenshot that shows how to create a data asset in Azure Machine Learning studio." lightbox="./media/create-datastore-with-UI/create-data-asset.png":::

1. Select **From Azure storage**
    
    :::image type="content" source="media/create-datastore-with-UI/select-azure-storage.png" alt-text="Screenshot that shows how to select Azure storage." lightbox="./media/create-datastore-with-UI/select-azure-storage.png":::

1. Create a **New datastore**

    :::image type="content" source="media/create-datastore-with-UI/new-datastore.png" alt-text="Screenshot that shows how to create new datastore in Azure Machine Learning." lightbox="./media/create-datastore-with-UI/new-datastore.png":::

1. Or directly **Create datastore** from the beginning

    :::image type="content" source="media/create-datastore-with-UI/create-datastore.png" alt-text="Screenshot that shows how to create a datastore in Azure Machine Learning." lightbox="./media/create-datastore-with-UI/create-datastore.png":::

1. **Datastore** is created

:::image type="content" source="media/create-datastore-with-UI/datastore-created.png" alt-text="Screenshot that shows the datastore looks like after creation." lightbox="./media/create-datastore-with-UI/datastore-created.png":::

1. Access the **Datastore** 

:::image type="content" source="media/create-datastore-with-UI/access-datastore.png" alt-text="Screenshot that shows how to access a datastore in Azure Machine Learning." lightbox="./media/create-datastore-with-UI/access-datastore.png":::

Now the datastore is created successfully in Azure ML. It's ready for use in ML exercises.

## References

- https://community.fabric.microsoft.com/t5/Data-Engineering/Read-from-a-specified-table-from-lakehouse-in-One-workspace/m-p/4234885  
- https://fabric.guru/delta-lake-tables-for-optimal-direct-lake-performance-in-fabric-python-notebook 
- https://learn.microsoft.com/en-us/azure/machine-learning/how-to-datastore?view=azureml-api-2&tabs=sdk-identity-based-access%2Csdk-adls-identity-access%2Csdk-azfiles-accountkey%2Csdk-adlsgen1-identity-access%2Csdk-onelake-identity-access#create-a-onelake-microsoft-fabric-datastore-preview 
- https://learn.microsoft.com/en-us/fabric/data-engineering/spark-data-warehouse-connector
- https://learn.microsoft.com/en-us/azure/storage/blobs/data-lake-storage-abfs-driver   
- https://github.com/azeltov/aml_one_lake 