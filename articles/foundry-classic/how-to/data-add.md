---
title: How to add and manage data in your Microsoft Foundry hub-based project
titleSuffix: Microsoft Foundry
description: Learn how to add and manage data in your Microsoft Foundry hub-based project.
manager: mcleans
ms.service: azure-ai-foundry
ms.custom:
  - ignite-2023
  - build-2024
  - ignite-2024
  - hub-only
  - dev-focus
ms.topic: how-to
ms.date: 02/02/2026
ms.author: jburchel 
author: jonburchel 
ai-usage: ai-assisted
---

# How to add and manage data in your Microsoft Foundry hub-based project

[!INCLUDE [classic-banner](../includes/classic-banner.md)]

[!INCLUDE [feature-preview](../includes/feature-preview.md)]

This article describes how to create and manage data in Microsoft Foundry hub-based projects. You learn how to connect to your project, create data assets that reference files and folders in Azure Storage, and manage those assets through versioning, tagging, and archiving.

Data can help when you need these capabilities:

> [!div class="checklist"]
> - **Versioning:** Data versioning is supported.
> - **Reproducibility:** Once you create a data version, it's *immutable*. You can't modify or delete it. Therefore, you can reproduce jobs or prompt flow pipelines that consume the data.
> - **Auditability:** Because the data version is immutable, you can track the asset versions, who updated a version, and the date of each version update.
> - **Lineage:** For any given data, you can view which jobs or prompt flow pipelines consume the data.
> - **Ease-of-use:** A Foundry data resembles web browser bookmarks (favorites). Instead of remembering long storage paths that *reference* your frequently-used data on Azure Storage, you can create a data *version* and then access that version of the asset with a friendly name.


## Prerequisites

- An Azure subscription. [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- A Microsoft Foundry project. [Create a project in Microsoft Foundry portal](./create-projects.md).
- The [Azure AI Developer](/azure/role-based-access-control/built-in-roles/ai-machine-learning#azure-ai-developer) role assigned to you on the project resource. This role grants permissions to read, create, and manage data assets.
- Python 3.8 or later.
- The Microsoft ML SDK and Azure Identity package:

    ```bash
    pip install azure-ai-ml azure-identity
    ```

[!INCLUDE [hub-only-prereq](../includes/hub-only-prereq.md)]

## Connect to your project

To interact with your project programmatically, connect to it by using the `MLClient`.

```python
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential

# Authenticate using the default Azure credential
credential = DefaultAzureCredential()

# Connect to the project
# Get the subscription ID, resource group, and project name from the Microsoft Foundry portal
# or from the Overview page of your project in the Azure portal.
ml_client = MLClient(
    credential=credential,
    subscription_id="<SUBSCRIPTION_ID>",
    resource_group_name="<RESOURCE_GROUP>",
    workspace_name="<PROJECT_NAME>",
)

print(f"Connected to project: {ml_client.workspace_name}")
```

Reference: [MLClient documentation](/python/api/azure-ai-ml/azure.ai.ml.mlclient)

## Add data

You're charged for the storage used by your data. To help estimate the cost, use the [Azure Pricing Calculator](https://azure.microsoft.com/pricing/calculator/). The data is stored in a container named `workspaceblobstore` in your project's Azure Storage account. 

When you create your data, set the data type. Microsoft Foundry supports these data types:

|Type  |**Canonical Scenarios**|
|---------|---------|
|**`file`**<br>Reference a single file | Read a single file on Azure Storage (the file can have any format). |
|**`folder`**<br>Reference a folder | Read a folder of parquet/CSV files into Pandas/Spark.<br><br>Read unstructured data (for example: images, text, or audio) located in a folder. |
|**`table`**<br>Reference a table | Read a table on Azure Storage. |

### Add data by using Python SDK

You can create data assets that reference files or folders in Azure Storage.

#### Create a file data asset

To create a data asset that references a single file:

```python
from azure.ai.ml.entities import Data
from azure.ai.ml.constants import AssetTypes

# Define the data asset
my_file_data = Data(
    path="https://<storage_account>.blob.core.windows.net/<container>/<path_to_file>",
    type=AssetTypes.URI_FILE,
    description="Data asset pointing to a single file",
    name="my-file-data",
    version="1.0"
)

# Create the data asset in the project
created_data = ml_client.data.create_or_update(my_file_data)
print(f"Data asset created: {created_data.name} version {created_data.version}")
```

Reference: [Data class](/python/api/azure-ai-ml/azure.ai.ml.entities.data)

#### Create a folder data asset

To create a data asset that references a folder:

```python
from azure.ai.ml.entities import Data
from azure.ai.ml.constants import AssetTypes

# Define the data asset
my_folder_data = Data(
    path="https://<storage_account>.blob.core.windows.net/<container>/<path_to_folder>/",
    type=AssetTypes.URI_FOLDER,
    description="Data asset pointing to a folder",
    name="my-folder-data",
    version="1.0"
)

# Create the data asset in the project
created_data = ml_client.data.create_or_update(my_folder_data)
print(f"Data asset created: {created_data.name} version {created_data.version}")
```

Reference: [Data class](/python/api/azure-ai-ml/azure.ai.ml.entities.data)

### Add data by using Microsoft Foundry portal

Microsoft Foundry shows the supported source paths. You can create data from a folder or file:

- If you select **Folder** for the data source **Type**, you can choose the folder URL format. Foundry shows the supported folder URL formats. You can create a data resource as shown:
    :::image type="content" source="../media/data-add/studio-url-folder.png" alt-text="Screenshot of folder URL format.":::

- If you select **File** for the data source **Type**, you can choose the file URL format. The supported file URL formats are shown in Foundry portal. You can create a data resource as shown:
    :::image type="content" source="../media/data-add/studio-url-file.png" alt-text="Screenshot of file URL format.":::

- If you select **Table** for the data source **Type**, you can choose the table URL format. The supported file URL formats are shown in Foundry portal. You can create a data resource as shown:
    :::image type="content" source="../media/data-add/studio-url-table.png" alt-text="Screenshot of table URL format.":::

### Upload files and folders

You can upload files or folders directly to your workspace storage account by selecting **Upload files/folders** in the **Data source** field as shown:

:::image type="content" source="../media/data-add/upload-file-folder.png" alt-text="This screenshot shows how to upload a file.":::

When you upload files or folders, you upload them to the default `workspaceblobstore` connection. The files and folders go to the root of the storage container.

### Add file, folder, and table data from Azure Storage

You can add file, folder, and table data from Azure Storage to your Foundry workspace.

A file (`uri_file`) data resource type points to a *single file* on storage (for example, a CSV file).

A folder (`uri_folder`) data source type points to a *folder* on a storage resource (for example, a folder containing several subfolders of images).

A table (`uri_table`) data source type points to a *table* on a storage resource (for example, a folder that contains tabular data).

[!INCLUDE [tip-left-pane](../includes/tip-left-pane.md)]

These steps explain how to add an existing file, folder, or table data resource from Azure Storage to your hub-based project workspace in the Foundry portal:

1. Go to the [Foundry](https://ai.azure.com/?cid=learnDocs).

1. Select the hub-based project where you want to add the data.

1. From the collapsible **My assets** menu on the left, select **Data + indexes**. Then select **New data** as shown in the following screenshot:

    :::image type="content" source="../media/data-add/add-data.png" alt-text="Screenshot highlighting New Data in the Data tab.":::

1. Select **Get data with storage URL** as your **Data source**. 
1. Choose the *File*, *Folder*, or *Table* as the data **Type**. Then provide a URL based on the supported URL formats listed on that page.    

1. Select **Next** after you choose the data source.

1. Enter a custom name for your data, and then select **Create**.

:::image type="content" source="../media/data-add/data-add-finish.png" alt-text="This screenshot shows the naming step for the data source." lightbox="../media/data-connections/data-add-finish.png":::

## Manage data

After you add data to your hub-based project, you can manage it by using the Microsoft Foundry portal or the Python SDK.

### List and get data assets

To list all data assets in your project, use the following code:

```python
# List all data assets
data_assets = ml_client.data.list()
for data in data_assets:
    print(f"Name: {data.name}, Version: {data.version}")
```

Reference: [DataOperations.list](/python/api/azure-ai-ml/azure.ai.ml.operations.dataoperations#azure-ai-ml-operations-dataoperations-list)

To get details of a specific data asset, use the following code:

```python
# Get a specific data asset
data = ml_client.data.get(name="my-file-data", version="1.0")
print(f"Data name: {data.name}")
print(f"Data path: {data.path}")
```

Reference: [DataOperations.get](/python/api/azure-ai-ml/azure.ai.ml.operations.dataoperations#azure-ai-ml-operations-dataoperations-get)

### Delete data

> [!IMPORTANT]
> Data deletion isn't supported. Data is immutable in Microsoft Foundry portal. Once you create a data version, you can't modify or delete it. This immutability provides a level of protection when working in a team that creates production workloads.

If Microsoft Foundry allowed data deletion, it would have the following adverse effects:
- Production jobs that consume data that you later delete would fail.
- Machine learning experiment reproduction would become more difficult.
- Job lineage would break, because it would become impossible to view the deleted data version.
- You could no longer correctly track and audit, since versions could be missing.

When you erroneously create a data resource - for example, with an incorrect name, type, or path - Microsoft offers solutions to handle the situation without the negative consequences of deletion:

|Reason that you might want to delete data | Solution  |
|---------|---------|
|The **name** is incorrect     |  [Archive the data](#archive-data)       |
|The team **no longer uses** the data | [Archive the data](#archive-data) |
|It **clutters the data listing** | [Archive the data](#archive-data) |
|The **path** is incorrect     |  Create a *new version* of the data (same name) with the correct path. For more information, visit [Add data](#add-data).       |
|It has an incorrect **type**  |  Currently, Microsoft doesn't allow the creation of a new version with a *different* type compared to the initial version.<br>(1) [Archive the data](#archive-data)<br>(2) [Add data](#add-data) under a different name with the correct type.    |

### Archive data

By default, archiving a data resource hides it from both list queries, such as the CLI `az ml data list`, and the data listing in Microsoft Foundry portal. You can still reference and use an archived data resource in your workflows. You can either archive:

- *all versions* of the data under a given name
- a specific data version

Use the Python SDK to archive data:

```python
# Archive a specific version
ml_client.data.archive(name="my-file-data", version="1.0")

# Archive all versions (container)
ml_client.data.archive(name="my-file-data")
```

Reference: [DataOperations.archive](/python/api/azure-ai-ml/azure.ai.ml.operations.dataoperations#azure-ai-ml-operations-dataoperations-archive)

#### Archive all versions of a data

Currently, Microsoft Foundry portal doesn't support archiving *all versions* of the data resource under a given name.

#### Archive a specific data version

Currently, Microsoft Foundry portal doesn't support archiving a specific version of the data resource.

### Restore archived data

You can restore an archived data resource. If all versions of the data are archived, you can't restore individual versions of the data - you must restore all versions.

You can restore data by using the Python SDK:

```python
# Restore a specific version
ml_client.data.restore(name="my-file-data", version="1.0")

# Restore all versions (container)
ml_client.data.restore(name="my-file-data")
```

Reference: [DataOperations.restore](/python/api/azure-ai-ml/azure.ai.ml.operations.dataoperations#azure-ai-ml-operations-dataoperations-restore)

#### Restore all versions of data

Currently, the Microsoft Foundry portal doesn't support restoration of *all versions* of the data under a given name.

#### Restore a specific data version

> [!IMPORTANT]
> If all data versions are archived, you can't restore individual versions of the data - you must restore all versions.

Currently, the Microsoft Foundry portal doesn't support restoration of a specific data version.

### Data tagging

Data tagging is extra metadata you apply to the data as a key-value pair. Data tagging offers many benefits:

- Data quality description. For example, if your organization uses a *medallion lakehouse architecture*, you can tag assets with `medallion:bronze` (raw), `medallion:silver` (validated), and `medallion:gold` (enriched).
- Efficient data searching and filtering, to help with data discovery.
- Identification of sensitive personal data, to properly manage and govern data access. For example, `sensitivity:PII` and `sensitivity:nonPII`.
- Identification of whether data is approved, from a responsible AI (RAI) audit. For example, `RAI_audit:approved` and `RAI_audit:todo`.

You can add tags to existing data by using the Python SDK:

```python
# Get the data asset
my_data = ml_client.data.get(name="my-file-data", version="1.0")

# Add or update tags
my_data.tags["medallion"] = "silver"
my_data.tags["sensitivity"] = "nonPII"

# Update the data asset
ml_client.data.create_or_update(my_data)
print(f"Tags updated for: {my_data.name}")
```

Reference: [DataOperations.create_or_update](/python/api/azure-ai-ml/azure.ai.ml.operations.dataoperations#azure-ai-ml-operations-dataoperations-create-or-update)

### Data preview

In the Data details page, you can browse the folder structure and preview the file. The portal supports data preview for these types:
- Data file types that the preview API supports: `.tsv`, `.csv`, `.parquet`, `.jsonl`.
- For other file types, the Microsoft Foundry portal tries to natively preview the file in the browser. The supported file types might depend on the browser itself.
For images, the portal supports these file image types: `.png`, `.jpg`, `.gif`. For other files, the portal supports these file types: `.ipynb`, `.py`, `.yml`, `.html`.

## Next steps

- Learn how to [create a project in Microsoft Foundry portal](./create-projects.md).
