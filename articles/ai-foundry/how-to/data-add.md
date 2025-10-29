---
title: How to add and manage data in your Azure AI Foundry hub-based project
titleSuffix: Azure AI Foundry
description: Learn how to add and manage data in your Azure AI Foundry hub-based project.
manager: mcleans
ms.service: azure-ai-foundry
ms.custom:
  - ignite-2023
  - build-2024
  - ignite-2024
  - hub-only
ms.topic: how-to
ms.date: 08/27/2025
ms.author: jburchel 
author: jonburchel 
---

# How to add and manage data in your Azure AI Foundry hub-based project

[!INCLUDE [feature-preview](../includes/feature-preview.md)]

This article describes how to create and manage data in Azure AI Foundry hub-based projects. Data can be used as a source for indexing in Azure AI Foundry portal.

Data can help when you need these capabilities:

> [!div class="checklist"]
> - **Versioning:** Data versioning is supported.
> - **Reproducibility:** Once you create a data version, it is *immutable*. It cannot be modified or deleted. Therefore, jobs or prompt flow pipelines that consume the data can be reproduced.
> - **Auditability:** Because the data version is immutable, you can track the asset versions, who updated a version, and the date of each version update.
> - **Lineage:** For any given data, you can view which jobs or prompt flow pipelines consume the data.
> - **Ease-of-use:** An Azure AI Foundry data resembles web browser bookmarks (favorites). Instead of remembering long storage paths that *reference* your frequently-used data on Azure Storage, you can create a data *version* and then access that version of the asset with a friendly name.


## Prerequisites

[!INCLUDE [hub-only-prereq](../includes/hub-only-prereq.md)]

## Add new data

You're charged for the storage used by your data. To help estimate the cost, you can use the [Azure Pricing Calculator](https://azure.microsoft.com/pricing/calculator/). The data is stored in a container called `workspaceblobstore` in your project's Azure Storage account. 

When you create your data, you need to set the data type. Azure AI Foundry supports these data types:

|Type  |**Canonical Scenarios**|
|---------|---------|
|**`file`**<br>Reference a single file | Read a single file on Azure Storage (the file can have any format). |
|**`folder`**<br>Reference a folder | Read a folder of parquet/CSV files into Pandas/Spark.<br><br>Read unstructured data (for example: images, text, or audio) located in a folder. |
|**`table`**<br>Reference a table | Read a table on Azure Storage. |

Azure AI Foundry shows the supported source paths. You can create a data from a folder or file:

- If you select **Folder** for the data source **Type**, you can choose the folder URL format. Azure AI Foundry shows the supported folder URL formats. You can create a data resource as shown:
    :::image type="content" source="../media/data-add/studio-url-folder.png" alt-text="Screenshot of folder URL format.":::

- If you select **File** for the data source **Type**, you can choose the file URL format. The supported file URL formats are shown in Azure AI Foundry portal. You can create a data resource as shown:
    :::image type="content" source="../media/data-add/studio-url-file.png" alt-text="Screenshot of file URL format.":::

- If you select **Table** for the data source **Type**, you can choose the table URL format. The supported file URL formats are shown in Azure AI Foundry portal. You can create a data resource as shown:
    :::image type="content" source="../media/data-add/studio-url-table.png" alt-text="Screenshot of table URL format.":::

### Upload files and folders

You can upload files or folders directly to your workspace storage account by selecting **Upload files/folders** in the **Data source** field as shown:

:::image type="content" source="../media/data-add/upload-file-folder.png" alt-text="This screenshot shows how to upload a file.":::

When you upload files or folders, they're uploaded to the default `workspaceblobstore` connection. The files and folders are uploaded to the root of the storage container.

### Add file, folder, and table data from Azure Storage

You can add file, folder, and table data from Azure Storage to your Azure AI Foundry workspace.

A file (`uri_file`) data resource type points to a *single file* on storage (for example, a CSV file).

A Folder (`uri_folder`) data source type points to a *folder* on a storage resource (for example, a folder containing several subfolders of images).

A Table (`uri_table`) data source type points to a *table* on a storage resource (for example, a folder that contains tabular data).

[!INCLUDE [tip-left-pane](../includes/tip-left-pane.md)]

These steps explain how to add an existing file, folder, or table data resource from Azure Storage to your hub-based project workspace in the Azure AI Foundry portal:

1. Navigate to the [Azure AI Foundry](https://ai.azure.com/?cid=learnDocs).

1. Select the hub-based project where you want to add the data.

1. From the collapsible **My assets** menu on the left, select **Data + indexes**, then select **New data** as shown in this screenshot:

    :::image type="content" source="../media/data-add/add-data.png" alt-text="Screenshot highlighting New Data in the Data tab.":::

1. Select **Get data with storage URL** as your **Data source**. 
1. Then choose the *File*, *Folder*, or *Table* as the data **Type**, and then provide a URL based on the supported URL formats listed on that page.    

1. Select **Next** after you choose the data source.

1. Enter a custom name for your data, and then select **Create**.

:::image type="content" source="../media/data-add/data-add-finish.png" alt-text="This screenshot shows the naming step for the data source." lightbox="../media/data-connections/data-add-finish.png":::

## Manage data

After you add data to your hub-based project, you can delete, archive, restore, tag, archive, and preview the data in the Azure AI Foundry.

### Delete data

> [!IMPORTANT]
> Data deletion isn't supported. Data is immutable in Azure AI Foundry portal. Once you create a data version, it can't be modified or deleted. This immutability provides a level of protection when working in a team that creates production workloads.

If Azure AI Foundry allowed data deletion, it would have the following adverse effects:
- Production jobs that consume data that is later deleted would fail
- Machine learning experiment reproduction would become more difficult
- Job lineage would break, because it would become impossible to view the deleted data version
- You could no longer correctly track and audit, since versions could be missing

When a data resource is erroneously created - for example, with an incorrect name, type or path - Azure AI offers solutions to handle the situation without the negative consequences of deletion:

|Reason that you might want to delete data | Solution  |
|---------|---------|
|The **name** is incorrect     |  [Archive the data](#archive-data)       |
|The team **no longer uses** the data | [Archive the data](#archive-data) |
|It **clutters the data listing** | [Archive the data](#archive-data) |
|The **path** is incorrect     |  Create a *new version* of the data (same name) with the correct path. For more information, visit [Add new data](#add-new-data).       |
|It has an incorrect **type**  |  Currently, Azure AI doesn't allow the creation of a new version with a *different* type compared to the initial version.<br>(1) [Archive the data](#archive-data)<br>(2) [Add new data](#add-new-data) under a different name with the correct type.    |

### Archive data

By default, archiving a data resource hides it from both list queries (for example, in the CLI `az ml data list`) and the data listing in Azure AI Foundry portal. You can still continue to reference and use an archived data resource in your workflows. You can either archive:

- *all versions* of the data under a given name
- a specific data version

#### Archive all versions of a data

At this time, Azure AI Foundry doesn't support archiving *all versions* of the data resource under a given name.

#### Archive a specific data version

At this time, Azure AI Foundry doesn't support archiving a specific version of the data resource.

### Restore an archived data

You can restore an archived data resource. If all of versions of the data are archived, you can't restore individual versions of the data - you must restore all versions.

#### Restore all versions of a data

At this time, Azure AI Foundry doesn't support restoration of *all versions* of the data under a given name.

#### Restore a specific data version

> [!IMPORTANT]
> If all data versions were archived, you can't restore individual versions of the data - you must restore all versions.

Currently, Azure AI Foundry doesn't support restoration of a specific data version.

### Data tagging

Data tagging is extra metadata applied to the data in the form of a key-value pair. Data tagging offers many benefits:

- Data quality description. For example, if your organization uses a *medallion lakehouse architecture*, you can tag assets with `medallion:bronze` (raw), `medallion:silver` (validated) and `medallion:gold` (enriched).
- It provides efficient data searching and filtering, to help data discovery.
- It helps identify sensitive personal data, to properly manage and govern data access. For example, `sensitivity:PII`/`sensitivity:nonPII`.
- It identifies whether or not data is approved, from a responsible AI (RAI) audit. For example, `RAI_audit:approved`/`RAI_audit:todo`.

You can add tags to existing data.

### Data preview

In the Data details page, you can browse the folder structure and preview the file. We support data preview for these types:
- Data file types that are supported via the preview API: ".tsv", ".csv", ".parquet", ".jsonl".
- For other file types, Azure AI Foundry portal tries to natively preview the file in the browser. The supported file types might depend on the browser itself.
Normally for images, these file image types are supported: ".png", ".jpg", ".gif". Normally, these file types are supported: ".ipynb", ".py", ".yml", ".html".

## Next steps

- Learn how to [create a project in Azure AI Foundry portal](./create-projects.md).
