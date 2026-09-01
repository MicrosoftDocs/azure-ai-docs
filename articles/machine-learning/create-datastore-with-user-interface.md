---
title: Copy a OneLake lakehouse table to Azure Machine Learning through the UI
titleSuffix: Azure Machine Learning
description: Copy a OneLake lakehouse table into Azure Data Lake Storage and create an Azure Machine Learning datastore over it in the studio UI.
ms.author: scottpolly
author: s-polly
ms.reviewer: soumyapatro 
ms.service: azure-machine-learning
ms.subservice: mldata
ms.topic: how-to
ms.date: 08/25/2026
ms.custom: dev-focus, doc-kit-assisted
ai-usage: ai-assisted
#Customer intent: Existing solutions help link lakehouse files to Azure Machine Learning resources, and create a datastore through the SDK. However, some customers have lakehouse tables, and they want to create a datastore in Azure Machine Learning through the UI.
---

# Copy a OneLake lakehouse table to Azure Machine Learning through the UI

This article shows how to make Microsoft Fabric OneLake **table**-type (`/Tables`) data available in Azure Machine Learning by copying it into an Azure Data Lake Storage (ADLS) account and creating a datastore over the copy. You do the whole task in the studio UI.

Azure Machine Learning can connect directly to OneLake **file**-type (`/Files`) data through a OneLake datastore, with no copy. That no-copy datastore doesn't support lakehouse tables, as shown in the following screenshot, so this article covers a UI-based workaround for table data.

:::image type="content" source="media/create-datastore-with-user-interface/show-fabric-table.png" alt-text="Screenshot showing a table in Microsoft Fabric." lightbox="./media/create-datastore-with-user-interface/show-fabric-table.png":::

> [!NOTE]
> This procedure **copies** data into Azure Data Lake Storage. The copied data is a point-in-time snapshot, not a live link, so you re-run the copy when the source table changes. If you don't need a UI-only workflow, consider the no-copy options first: a [OneLake (Microsoft Fabric) datastore](./how-to-datastore.md#create-a-onelake-microsoft-fabric-datastore-preview) for `/Files` data, or direct access from compute. For an overview of all OneLake integration options, see [Integrate OneLake with Azure Machine Learning](/fabric/onelake/onelake-azure-machine-learning).

## When to use this approach

Use the copy-based method in this article when both of these conditions are true:

- Your data is OneLake **table**-type (`/Tables`) data, which a OneLake datastore can't reference directly.
- You want to build the connection entirely in Azure Machine Learning studio, without the CLI or SDK.

If you need live, no-copy access, or your data is in the lakehouse `/Files` section, use a [OneLake datastore](./how-to-datastore.md#create-a-onelake-microsoft-fabric-datastore-preview) instead.

## Prerequisites

- An Azure subscription; if you don't have an Azure subscription, [create a free account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn) before you start.
- An Azure Machine Learning workspace. Visit [Create workspace resources](./quickstart-create-resources.md).
- An Azure Data Lake Storage (ADLS) storage account. Visit [Create an Azure Data Lake Storage (ADLS) storage account](/azure/storage/blobs/create-data-lake-storage-account).
- Knowledge of assigning roles in Azure storage account.
- Access to a [Microsoft Fabric](/fabric/get-started/microsoft-fabric-overview) workspace with a lakehouse that contains table-type data.
- Permission to create a data pipeline in the Fabric workspace, such as the **Contributor** or **Member** workspace role.

## How the copy workflow works

This workaround has three parts:

1. Create and set up a Data Lake Storage account in the Azure portal.
1. Use a Fabric data pipeline to copy the table data from OneLake to Azure Data Lake Storage.
1. Create an Azure Machine Learning datastore over the Azure Data Lake Storage container.

The following diagram shows the overall flow:

:::image type="content" source="media/create-datastore-with-user-interface/overall-idea.png" alt-text="Screenshot showing the overall flow of the solution." lightbox="./media/create-datastore-with-user-interface/overall-idea.png":::

> [!IMPORTANT]
> Because this approach copies data, the Azure Machine Learning datastore holds a point-in-time snapshot. Re-run the copy when the source lakehouse table changes. The copy also duplicates storage, which adds cost, and doesn't preserve OneLake governance or lineage.

## Set up the Data Lake storage account in the Azure portal

Assign the **Storage Blob Data Contributor** and **Storage File Data Privileged Contributor** roles to the user identity or service principal to grant data-plane access and permission to create containers. Account-key access is controlled separately by the **Allow storage account key access** setting, which you enable in a later step. To assign the roles to the user identity:

1. Open the [Microsoft Azure portal](https://portal.azure.com).
1. Select the **Storage accounts** service.

    :::image type="content" source="media/apache-spark-environment-configuration/find-storage-accounts-service.png" lightbox="media/apache-spark-environment-configuration/find-storage-accounts-service.png" alt-text="Screenshot showing selection of Storage Accounts service.":::

1. On the **Storage accounts** page, select the Data Lake Storage account you created in the prerequisite step. A page showing the storage account properties opens.

     :::image type="content" source="media/create-datastore-with-user-interface/create-storage-account.png" alt-text="Screenshot showing the properties page of the data lake storage account." lightbox="./media/create-datastore-with-user-interface/create-storage-account.png":::

1. Select **Access keys** from the left panel and record the key. You need this value in a later step.

1. Select and enable **Allow storage account key access** as shown in the following screenshot:

    > [!TIP]
    > For production workloads, use identity-based authentication (Microsoft Entra ID) instead of account keys. For more information, see [Create datastores](./how-to-datastore.md).

    :::image type="content" source="media/create-datastore-with-user-interface/enable-key-access.png" alt-text="Screenshot showing how to enable key access of data lake storage account in Azure portal." lightbox="./media/create-datastore-with-user-interface/enable-key-access.png":::

1. Select **Access Control (IAM)** from the left panel, and assign the **Storage Blob Data Contributor** and **Storage File Data Privileged Contributor** roles to the service principal.

    :::image type="content" source="media/create-datastore-with-user-interface/assign-roles.png" alt-text="Screenshot showing how to assign roles of data lake storage account in Azure portal." lightbox="./media/create-datastore-with-user-interface/assign-roles.png":::

1. Create a container in the storage account. Name it **onelake-table**.

    :::image type="content" source="media/create-datastore-with-user-interface/create-container.png" alt-text="Screenshot showing creation of a data lake storage account container in the Azure portal." lightbox="./media/create-datastore-with-user-interface/create-container.png":::

## Use a Fabric data pipeline to copy data to an Azure Data Lake Storage account

> [!TIP]
> You can also use a [Fabric Copy job](/fabric/data-factory/what-is-copy-job), which provides a simpler experience for data copy scenarios.

1. At the Fabric portal, select **Data pipeline** at the New item page.

    :::image type="content" source="media/create-datastore-with-user-interface/create-pipeline.png" alt-text="Screenshot showing selection of data pipeline at the Fabric New item page." lightbox="./media/create-datastore-with-user-interface/create-pipeline.png":::

1. Select **Copy data assistant**.

    :::image type="content" source="media/create-datastore-with-user-interface/copy-data-assistant.png" alt-text="Screenshot showing selection of Copy data assistant." lightbox="./media/create-datastore-with-user-interface/copy-data-assistant.png":::

1. In **Copy data assistant**, select **Azure Blobs**:

    :::image type="content" source="media/create-datastore-with-user-interface/select-azure-blob.png" alt-text="Screenshot showing selection of Select Azure blobs in the Fabric Copy data assistant." lightbox="./media/create-datastore-with-user-interface/select-azure-blob.png":::

1. To create a connection to the Azure Data Lake storage account, select **Authentication kind: Account key** and then **Next**:

    :::image type="content" source="media/create-datastore-with-user-interface/create-connection.png" alt-text="Screenshot that shows how to create a connection in a Fabric data pipeline." lightbox="./media/create-datastore-with-user-interface/create-connection.png":::

    > [!TIP]
    > To avoid account keys, select an identity-based **Authentication kind**, such as **Organizational account**, and create the Azure Machine Learning datastore with identity-based access. This approach uses the data-plane roles you assigned earlier and doesn't require enabling account-key access.

1. Select the data destination, and select **Next**:

    :::image type="content" source="media/create-datastore-with-user-interface/select-destination-folder.png" alt-text="Screenshot that shows selection of the data destination." lightbox="./media/create-datastore-with-user-interface/select-destination-folder.png":::

1. Connect to the data destination, and select **Next**:

    :::image type="content" source="media/create-datastore-with-user-interface/connect-data-destination.png" alt-text="Screenshot that shows connection to the data destination." lightbox="./media/create-datastore-with-user-interface/connect-data-destination.png":::

1. That step automatically starts the data copy job:

    :::image type="content" source="media/create-datastore-with-user-interface/copy-activity-scheduled.png" alt-text="Screenshot that shows the copy activity is scheduled." lightbox="./media/create-datastore-with-user-interface/copy-activity-scheduled.png":::

    This step might take a while. It directly leads to the next step.

1. Check that the data copy job finished successfully:

    :::image type="content" source="media/create-datastore-with-user-interface/copy-activity-success.png" alt-text="Screenshot showing that the copy operation succeeded." lightbox="./media/create-datastore-with-user-interface/copy-activity-success.png":::

## Create an Azure Machine Learning datastore over the Azure Data Lake Storage container

Now that your data is in the Azure Data Lake storage resource, you can create an Azure Machine Learning datastore.

1. In Azure storage account, the **container** as shown on the left has data, as shown on the right:

    :::image type="content" source="media/create-datastore-with-user-interface/check-container.png" alt-text="Screenshot that shows how to verify the data in Azure storage account container." lightbox="./media/create-datastore-with-user-interface/check-container.png":::

1. In Azure Machine Learning studio, create a data asset. To decide the type, open the **onelake-table** container and check whether the copy produced a single file or a folder of files. Select **File (uri_file)** for a single file, or **Folder (uri_folder)** for a folder of files, which is common when the table exports as multiple files:

    :::image type="content" source="media/create-datastore-with-user-interface/create-data-asset.png" alt-text="Screenshot showing selection of the data asset type." lightbox="./media/create-datastore-with-user-interface/create-data-asset.png":::

1. Select **From Azure storage**:

    :::image type="content" source="media/create-datastore-with-user-interface/select-azure-storage.png" alt-text="Screenshot that shows how to select Azure storage." lightbox="./media/create-datastore-with-user-interface/select-azure-storage.png":::

1. Using the **Account key** value from the earlier **Create a connection to the Azure Data Lake storage account** step, create a **New datastore**:

    :::image type="content" source="media/create-datastore-with-user-interface/new-datastore.png" alt-text="Screenshot that shows how to create new datastore in Azure Machine Learning." lightbox="./media/create-datastore-with-user-interface/new-datastore.png":::

1. You can also directly create a datastore in Azure Machine Learning studio:

    :::image type="content" source="media/create-datastore-with-user-interface/create-datastore.png" alt-text="Screenshot that shows how to create a datastore in Azure Machine Learning." lightbox="./media/create-datastore-with-user-interface/create-datastore.png":::

1. You can review details of the datastore you created:

    :::image type="content" source="media/create-datastore-with-user-interface/datastore-created.png" alt-text="Screenshot that shows details of the datastore you created." lightbox="./media/create-datastore-with-user-interface/datastore-created.png":::

1. Review the data in the datastore

    :::image type="content" source="media/create-datastore-with-user-interface/access-datastore.png" alt-text="Screenshot that shows how to access a datastore in Azure Machine Learning." lightbox="./media/create-datastore-with-user-interface/access-datastore.png":::

Now that you successfully created the datastore in Azure Machine Learning, you can use it in machine learning exercises.

## Troubleshooting

- **Role assignment not yet effective**: Azure role assignments can take several minutes to propagate. If the copy job or datastore creation fails with an authorization error, wait a few minutes and retry.
- **Account key access disabled**: If you can't retrieve or use the account key, confirm that **Allow storage account key access** is enabled on the storage account.
- **Fabric connection fails**: Verify the storage account name and key, and confirm that the **onelake-table** container exists.
- **Snapshot is stale**: The copy produces a point-in-time snapshot. To keep it current, schedule the Fabric data pipeline to run on a recurring cadence.

## Related content

- [Create datastores](./how-to-datastore.md)
- [Create a OneLake (Microsoft Fabric) datastore (preview)](./how-to-datastore.md#create-a-onelake-microsoft-fabric-datastore-preview)
- [Create data assets](./how-to-create-data-assets.md)
- [Integrate OneLake with Azure Machine Learning](/fabric/onelake/onelake-azure-machine-learning)

## References

+ [Read from a specified table from lakehouse in One workspace using Notebook in other workspace](https://community.fabric.microsoft.com/t5/Data-Engineering/Read-from-a-specified-table-from-lakehouse-in-One-workspace/m-p/4234885)
+ [Delta Lake Tables For Optimal Direct Lake Performance In Fabric Python Notebook](https://fabric.guru/delta-lake-tables-for-optimal-direct-lake-performance-in-fabric-python-notebook)
+ [Spark connector for Microsoft Fabric Data Warehouse](/fabric/data-engineering/spark-data-warehouse-connector)
+ [AML and OneLake and Fabric Better Together Demo](https://github.com/azeltov/aml_one_lake)