---
title: Linking Tables in OneLake to Azure ML Through UI
titleSuffix: Azure Machine Learning, Microsoft Fabric
description: Learn how to link table in Lakehouse to Azure ML studio through UI.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: mldata
ms.topic: how-to
ms.author: helenzeng
author: helenzusa1
ms.reviewer: franksolomon
ms.date: 02/10/2025
ms.custom: data4ml
# Customer intent: I have some Tables in OneLake, I want to use Azure ML studio for ML activities, so I need to link the Tables in AML, and I prefer to do it through UI.
---

# Introduction of the solution
There were some existing solutions which can build a link in Azure ML to OneLake, get the data and create datastore in AML.
However, in those solutions, the data in OneLake is of type ‘Files’. Please refer to reference section.
Some customers have data in OneLake as type ‘Tables’. The existing solutions creating datastore in AML don’t work.

:::image type="content" source="media/create-datastore-with-UI/1-table-in-fabric.png" alt-text="Screenshot that shows how the table looks like in Microsoft Fabric." lightbox="./media/create-datastore-with-UI/1-table-in-fabric.png":::

Also some customers prefer doing in UI. Therefore, a new solution is needed to link AML to Tables in OneLake using UI.

In this article, you will learn how to link tables in OneLake to Azure ML studio through UI.

## Overall idea

:::image type="content" source="media/create-datastore-with-UI/2-overall-idea.png" alt-text="Screenshot that shows overall idea." lightbox="./media/create-datastore-with-UI/2-overall-idea.png":::


## Step 1. Create data lake storage account in Azure portal

:::image type="content" source="media/create-datastore-with-UI/3-create-storage-account.png" alt-text="Screenshot that shows an example of data lake storage account in Azure portal." lightbox="./media/create-datastore-with-UI/3-create-storage-account.png":::

## Step 2. Enable storage account key access

:::image type="content" source="media/create-datastore-with-UI/4-enable-key-access.png" alt-text="Screenshot that shows how to enable key access of data lake storage account in Azure portal." lightbox="./media/create-datastore-with-UI/4-enable-key-access.png":::

## Step 3. Assign roles to the storage account

:::image type="content" source="media/create-datastore-with-UI/5-assign-roles.png" alt-text="Screenshot that shows how to assign roles of data lake storage account in Azure portal." lightbox="./media/create-datastore-with-UI/5-assign-roles.png":::

## Step 4. Create a container

:::image type="content" source="media/create-datastore-with-UI/6-create-container.png" alt-text="Screenshot that shows how to create a container of data lake storage account in Azure portal." lightbox="./media/create-datastore-with-UI/6-create-container.png":::

## Step 5. In Fabric, create a pipeline

:::image type="content" source="media/create-datastore-with-UI/7-create-pipeline.png" alt-text="Screenshot that shows how to create a data pipeline in Fabric." lightbox="./media/create-datastore-with-UI/7-create-pipeline.png":::

## Step 6. Use pipeline, start 'Copy data assistant'

:::image type="content" source="media/create-datastore-with-UI/8-copy-data-assistant.png" alt-text="Screenshot that shows how to start Copy data assistant in Fabric." lightbox="./media/create-datastore-with-UI/8-copy-data-assistant.png":::

## Step 7. In 'Copy data assistant', select Azure Blobs

:::image type="content" source="media/create-datastore-with-UI/9-select-azure-blob.png" alt-text="Screenshot that shows how to select Azure blobs in Copy data assistant in Fabric." lightbox="./media/create-datastore-with-UI/9-select-azure-blob.png":::

## Step 8. Set storage account, create connection

:::image type="content" source="media/create-datastore-with-UI/10-create-connection.png" alt-text="Screenshot that shows how to create connection in Fabric data pepiline." lightbox="./media/create-datastore-with-UI/10-create-connection.png":::

## Step 9. Select destination folder

:::image type="content" source="media/create-datastore-with-UI/11-select-destination-folder.png" alt-text="Screenshot that shows how to select destination folder." lightbox="./media/create-datastore-with-UI/11-select-destination-folder.png":::

## Step 10. Connect to data destination

:::image type="content" source="media/create-datastore-with-UI/12-connect-data-destination.png" alt-text="Screenshot that shows how to connect to data destination." lightbox="./media/create-datastore-with-UI/12-connect-data-destination.png":::

## Step 11. Copy activity is scheduled

:::image type="content" source="media/create-datastore-with-UI/13-copy-activity-scheduled.png" alt-text="Screenshot that shows the copy activity is scheduled." lightbox="./media/create-datastore-with-UI/13-copy-activity-scheduled.png":::

## Step 12. Copy success

:::image type="content" source="media/create-datastore-with-UI/14-copy-activity-success.png" alt-text="Screenshot that shows the copy is successful." lightbox="./media/create-datastore-with-UI/14-copy-activity-success.png":::

## Step 13. Check storage account, container in Azure portal

:::image type="content" source="media/create-datastore-with-UI/15-check-container.png" alt-text="Screenshot that shows how to verify the data in Azure storage account container." lightbox="./media/create-datastore-with-UI/15-check-container.png":::

## Step 14. In ML studio create data asset, type 'File'

:::image type="content" source="media/create-datastore-with-UI/16-create-data-asset.png" alt-text="Screenshot that shows how to create a data asset in Azure ML studio." lightbox="./media/create-datastore-with-UI/16-create-data-asset.png":::

## Step 15. Select 'From Azure storage'

:::image type="content" source="media/create-datastore-with-UI/17-select-azure-storage.png" alt-text="Screenshot that shows how to select Azure storage." lightbox="./media/create-datastore-with-UI/17-select-azure-storage.png":::

## Step 16. It will bring you to create 'New datastore'

:::image type="content" source="media/create-datastore-with-UI/18-new-datastore.png" alt-text="Screenshot that shows how to create new datastore in Azure ML." lightbox="./media/create-datastore-with-UI/18-new-datastore.png":::

## Step 17. Or you can directly 'Create datastore' from the beginning

:::image type="content" source="media/create-datastore-with-UI/19-create-datastore.png" alt-text="Screenshot that shows how to create a datastore in Azure ML." lightbox="./media/create-datastore-with-UI/19-create-datastore.png":::

## Step 18. Datastore is created

:::image type="content" source="media/create-datastore-with-UI/20-datastore-created.png" alt-text="Screenshot that shows the datastore looks like after creation." lightbox="./media/create-datastore-with-UI/20-datastore-created.png":::

## Step 19. Access the datastore

:::image type="content" source="media/create-datastore-with-UI/21-access-datastore.png" alt-text="Screenshot that shows how to access a datastore in Azure ML." lightbox="./media/create-datastore-with-UI/21-access-datastore.png":::

## References

- https://community.fabric.microsoft.com/t5/Data-Engineering/Read-from-a-specified-table-from-lakehouse-in-One-workspace/m-p/4234885  
- https://fabric.guru/delta-lake-tables-for-optimal-direct-lake-performance-in-fabric-python-notebook 
- https://learn.microsoft.com/en-us/azure/machine-learning/how-to-datastore?view=azureml-api-2&tabs=sdk-identity-based-access%2Csdk-adls-identity-access%2Csdk-azfiles-accountkey%2Csdk-adlsgen1-identity-access%2Csdk-onelake-identity-access#create-a-onelake-microsoft-fabric-datastore-preview 
- https://learn.microsoft.com/en-us/fabric/data-engineering/spark-data-warehouse-connector
- https://learn.microsoft.com/en-us/azure/storage/blobs/data-lake-storage-abfs-driver   
- https://github.com/azeltov/aml_one_lake 
