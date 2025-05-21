---
title: How to add and manage data in your Azure AI Foundry project
titleSuffix: Azure AI Foundry
description: Learn how to add and manage data in your Azure AI Foundry project.
manager: scottpolly
ms.service: azure-ai-foundry
ms.custom:
  - ignite-2023
  - build-2024
  - ignite-2024
ms.topic: how-to
ms.date: 05/21/2025
ms.author: franksolomon
author: fbsolo-ms1
---

# How to add and manage data in your Azure AI Foundry project

[!INCLUDE [feature-preview](../includes/feature-preview.md)]

This article describes how to create and manage data in Azure AI Foundry portal. Data can be used as a source for indexing in Azure AI Foundry portal.

Data can help when you need these capabilities:

> [!div class="checklist"]
> - **Versioning:** Data versioning is supported.
> - **Reproducibility:** Once you create a data version, it is *immutable*. It cannot be modified or deleted. Therefore, jobs or prompt flow pipelines that consume the data can be reproduced.
> - **Auditability:** Because the data version is immutable, you can track the asset versions, who updated a version, and the date of each version update.
> - **Lineage:** For any given data, you can view which jobs or prompt flow pipelines consume the data.
> - **Ease-of-use:** An Azure AI Foundry data resembles web browser bookmarks (favorites). Instead of remembering long storage paths that *reference* your frequently-used data on Azure Storage, you can create a data *version* and then access that version of the asset with a friendly name.


## Prerequisites

[!INCLUDE [hub-only-prereq](../includes/hub-only-prereq.md)]

## Create data

You are charged for the storage used by your data. To help estimate the cost, you can use the [Azure Pricing Calculator](https://azure.microsoft.com/pricing/calculator/). The data is stored in a container called `workspaceblobstore` in your project's Azure Storage account. 

When you create your data, you need to set the data type. Azure AI Foundry supports these data types:

|Type  |**Canonical Scenarios**|
|---------|---------|
|**`file`**<br>Reference a single file | Read a single file on Azure Storage (the file can have any format). |
|**`folder`**<br> Reference a folder |      Read a folder of parquet/CSV files into Pandas/Spark.<br><br>Read unstructured data (for example: images, text, or audio) located in a folder. |

Azure AI Foundry shows the supported source paths. You can create a data from a folder or file:

- If you select **folder type**, you can choose the folder URL format. Azure AI Foundry shows the supported folder URL formats. You can create a data resource as shown:
    :::image type="content" source="../media/data-add/studio-url-folder.png" alt-text="Screenshot of folder URL format.":::

- If you select **file type**, you can choose the file URL format. The supported file URL formats are shown in Azure AI Foundry portal. You can create a data resource as shown:
    :::image type="content" source="../media/data-add/studio-url-file.png" alt-text="Screenshot of file URL format.":::

### Create data: File type

A file (`uri_file`) data resource type points to a *single file* on storage (for example, a CSV file).

[!INCLUDE [tip-left-pane](../includes/tip-left-pane.md)]

These steps explain how to create a File typed data resource in the Azure AI Foundry portal:

1. Navigate to the [Azure AI Foundry](https://ai.azure.com/).

1. Select the project where you want to create the data.

1. From the collapsible **My assets** menu on the left, select **Data + indexes**, then select **New data** as shown in this screenshot:

    :::image type="content" source="../media/data-add/add-data.png" alt-text="Screenshot highlighting New Data in the Data tab.":::

1. Choose your **Data source**. To choose a data source, you have two options.
   - You can select **Get data with storage URL** if you have a direct URL to a storage account or a public accessible HTTPS server.
   - You can select **Upload files/folders** to upload a folder from your local drive.

     - **Get data with Storage URL**: You can choose the "File" as the **Type**, and then provide a URL based on the supported URL formats listed on that page, as shown in this screenshot:
     
     :::image type="content" source="../media/data-add/file-url.png" alt-text="This screenshot shows the provisioning of a URL that points to a file.":::

     - **Upload files/folders**: You can select **Upload files/folders**, select **Upload files**, and choose the local file to upload. The file uploads into the default "workspaceblobstore" connection.
     :::image type="content" source="../media/data-add/upload-file.png" alt-text="This screenshot shows how to upload a file.":::

    1. Select **Next** after you choose the data source.

    1. Enter a custom name for your data, and then select **Create**.

    :::image type="content" source="../media/data-add/data-add-finish.png" alt-text="This screenshot shows the naming step for the data source." lightbox="../media/data-connections/data-add-finish.png":::

### Create data: Folder type

A Folder (`uri_folder`) data source type points to a *folder* on a storage resource (for example, a folder containing several subfolders of images). Use these steps to create a Folder type data resource in Azure AI Foundry portal:

1. Navigate to [Azure AI Foundry](https://ai.azure.com/)

1. Select the project where you want to create the data.

1. From the collapsible **Components** menu on the left, select **Data**.

    :::image type="content" source="../media/data-add/add-data.png" alt-text="Screenshot highlighting New Data in the Data tab.":::

1.  Choose your **Data source**. To choose a data source, you have two options.
    1. Select **Get data with Storage URL** if you have a direct URL to a storage account or a public accessible HTTPS server
    1. Select **Upload files/folders** to upload a folder from your local drive

    - **Get data with Storage URL**: You can choose the **Type** as "Folder", and provide a URL based on the supported URL formats listed on that page.

       :::image type="content" source="../media/data-add/folder-url.png" alt-text="This screenshot shows the step to provide a URL that points to a folder.":::

    - **Upload files/folders**: You can select **Upload files/folders**, select **Upload folder**, and choose the local file to upload. The file resources upload into the default "workspaceblobstore" connection.

       :::image type="content" source="../media/data-add/upload-folder.png" alt-text="This screenshot shows how to upload a folder.":::

1. Select **Next** after you choose the data source.

1. Enter a custom name for your data, and then select **Create**.

    :::image type="content" source="../media/data-connections/data-add-finish.png" alt-text="Screenshot of naming the data." lightbox="../media/data-connections/data-add-finish.png":::

## Manage data

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
|The **path** is incorrect     |  Create a *new version* of the data (same name) with the correct path. For more information, visit [Create data](#create-data).       |
|It has an incorrect **type**  |  Currently, Azure AI doesn't allow the creation of a new version with a *different* type compared to the initial version.<br>(1) [Archive the data](#archive-data)<br>(2) [Create a new data](#create-data) under a different name with the correct type.    |

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
