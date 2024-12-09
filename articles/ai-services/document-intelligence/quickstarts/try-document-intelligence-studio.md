---
title: "Quickstart: Document Intelligence Studio | v3.0"
titleSuffix: Azure AI services
description: Form and document processing, data extraction, and analysis using Document Intelligence Studio
author: laujan
manager: nitinme
ms.service: azure-ai-document-intelligence
ms.custom:
  - ignite-2024
ms.topic: quickstart
ms.date: 08/07/2024
ms.author: lajanuar
monikerRange: '>=doc-intel-3.0.0'
---


<!-- markdownlint-disable MD001 -->

# Get started: Document Intelligence Studio

[!INCLUDE [applies to v4.0 v3.1 v3.0](../includes/applies-to-v40-v31-v30.md)]

[Document Intelligence Studio](https://formrecognizer.appliedai.azure.com/) is an online tool for visually exploring, understanding, and integrating features from the Document Intelligence service in your applications. You can get started by exploring the pretrained models with sample or your own documents. You can also create projects to build custom template models and reference the models in your applications using the [Python SDK](get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true) and other quickstarts.

## Prerequisites for new users

To use Document Intelligence Studio, you need the following assets and settings:

* An active [**Azure account**](https://azure.microsoft.com/free/cognitive-services/). If you don't have one, you can [**create a free account**](https://azure.microsoft.com/free/).

* A [**Document Intelligence**](https://portal.azure.com/#create/Microsoft.CognitiveServicesFormRecognizer) or [**multi-service**](https://portal.azure.com/#create/Microsoft.CognitiveServicesAIServices) resource.

> [!TIP]
> Create an Azure AI services resource if you plan to access multiple Azure AI services under a single endpoint/key. For Document Intelligence access only, create a Document Intelligence resource. Please note that you'll need a single-service resource if you intend to use [Microsoft Entra authentication](/azure/active-directory/authentication/overview-authentication).
>
> Document Intelligence now supports AAD token authentication additional to local (key-based) authentication when accessing the Document Intelligence resources and storage accounts. Be sure to follow below instructions to setup correct access roles, especially if your resources are applied with `DisableLocalAuth` policy.

* **Properly scoped Azure role assignments** For document analysis and prebuilt models, following role assignments are required for different scenarios.

  * Basic
    ✔️ **Cognitive Services User**: you need this role to Document Intelligence or Azure AI services resource to enter the analyze page.

  * Advanced
    ✔️ **Contributor**: you need this role to create resource group, Document Intelligence service, or Azure AI services resource.

    For more information on authorization, *see* [Document Intelligence Studio authorization policies](../studio-overview.md#authorization-policies).

    > [!NOTE]
    > If local (key-based) authentication is disabled for your Document Intelligence service resource, be sure to obtain **Cognitive Services User** role and your AAD token will be used to authenticate requests on Document Intelligence Studio.  The **Contributor** role only allows you to list keys but does not give you permission to use the resource when key-access is disabled.

* Once your resource is configured, you can try the different models offered by Document Intelligence Studio. From the front page, select any Document Intelligence model to try using with a no-code approach.

* To test any of the document analysis or prebuilt models, select the model and use one of the sample documents or upload your own document to analyze. The analysis result is displayed at the right in the content-result-code window.

* Custom models need to be trained on your documents. See [custom models overview](../train/custom-model.md) for an overview of custom models.

## Authentication

Navigate to the [Document Intelligence Studio](https://formrecognizer.appliedai.azure.com/). If it's your first time logging in, a popup window appears prompting you to configure your service resource. In accordance with your organization's policy, you have one or two options:

* **Microsoft Entra authentication: access by Resource (recommended)**.

  * Choose your existing subscription.
  * Select an existing resource group within your subscription or create a new one.
  * Select your existing Document Intelligence or Azure AI services resource.

    :::image type="content" source="../media/studio/configure-service-resource.png" alt-text="Screenshot of configure service resource form from the Document Intelligence Studio.":::

* **Local authentication: access by API endpoint and key**.

  * Retrieve your endpoint and key from the Azure portal.
  * Go to the overview page for your resource and select **Keys and Endpoint** from the left navigation bar.
  * Enter the values in the appropriate fields.

      :::image type="content" source="../media/studio/keys-and-endpoint.png" alt-text="Screenshot of the keys and endpoint page in the Azure portal.":::

* After validating the scenario in the Document Intelligence Studio, use the [**C#**](get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true), [**Java**](get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true), [**JavaScript**](get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true), or [**Python**](get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true) client libraries or the [**REST API**](get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true) to get started incorporating Document Intelligence models into your own applications.

To learn more about each model, *see* our concept pages.

### View resource details

 To view resource details such as name and pricing tier, select the **Settings** icon in the top-right corner of the Document Intelligence Studio home page and select the **Resource** tab. If you have access to other resources, you can switch resources as well.

## Added prerequisites for custom projects

In addition to the Azure account and a Document Intelligence or Azure AI services resource, you need:

### Azure Blob Storage container

A **standard performance** [**Azure Blob Storage account**](https://portal.azure.com/#create/Microsoft.StorageAccount-ARM). You create containers to store and organize your training documents within your storage account. If you don't know how to create an Azure storage account with a container, following these quickstarts:

* [**Create a storage account**](/azure/storage/common/storage-account-create). When creating your storage account, make sure to select **Standard** performance in the **Instance details → Performance** field.
* [**Create a container**](/azure/storage/blobs/storage-quickstart-blobs-portal#create-a-container). When creating your container, set the **Public access level** field to **Container** (anonymous read access for containers and blobs) in the **New Container** window.

### Azure role assignments

For custom projects, the following role assignments are required for different scenarios.

* Basic
  * **Cognitive Services User**: You need this role for Document Intelligence or Azure AI services resource to train the custom model or do analysis with trained models.
  * **Storage Blob Data Contributor**: You need this role for the Storage Account to create a project and label data.
* Advanced
  * **Storage Account Contributor**: You need this role for the Storage Account to set up CORS settings (this action is a one-time effort if the same storage account is reused).
  * **Contributor**: You need this role to create a resource group and resources.

  > [!NOTE]
  > If local (key-based) authentication is disabled for your Document Intelligence service resource and storage account, be sure to obtain **Cognitive Services User** and **Storage Blob Data Contributor** roles respectively, so you have enough permissions to use Document Intelligence Studio.  The **Storage Account Contributor** and **Contributor** roles only allow you to list keys but does not give you permission to use the resources when key-access is disabled.

### Configure CORS

[CORS (Cross Origin Resource Sharing)](/rest/api/storageservices/cross-origin-resource-sharing--cors--support-for-the-azure-storage-services) needs to be configured on your Azure storage account for it to be accessible from the Document Intelligence Studio. To configure CORS in the Azure portal, you need access to the CORS tab of your storage account.

1. Select the CORS tab for the storage account.

   :::image type="content" source="../media/quickstarts/cors-setting-menu.png" alt-text="Screenshot of the CORS setting menu in the Azure portal.":::

1. Start by creating a new CORS entry in the Blob service.

1. Set the **Allowed origins** to `https://documentintelligence.ai.azure.com`.

   :::image type="content" source="../media/quickstarts/cors-updated-image.png" alt-text="Screenshot that shows CORS configuration for a storage account.":::

    > [!TIP]
    > You can use the wildcard character '*' rather than a specified domain to allow all origin domains to make requests via CORS.

1. Select all the available 8 options for **Allowed methods**.

1. Approve all **Allowed headers** and **Exposed headers** by entering an * in each field.

1. Set the **Max Age** to 120 seconds or any acceptable value.

1. To save the changes, select the save button at the top of the page.

CORS should now be configured to use the storage account from Document Intelligence Studio.

### Sample documents set

1. Sign in to the [Azure portal](https://portal.azure.com) and navigate to **Your storage account** > **Data storage** > **Containers**.

   :::image border="true" type="content" source="../media/sas-tokens/data-storage-menu.png" alt-text="Screenshot of Data storage menu in the Azure portal.":::

1. Select a **container** from the list.

1. Select **Upload** from the menu at the top of the page.

    :::image border="true" type="content" source="../media/sas-tokens/container-upload-button.png" alt-text="Screenshot of container upload button in the Azure portal.":::

1. The **Upload blob** window appears.

1. Select your files to upload.

    :::image border="true" type="content" source="../media/sas-tokens/upload-blob-window.png" alt-text="Screenshot of upload blob window in the Azure portal.":::

> [!NOTE]
> By default, the Studio will use documents that are located at the root of your container. However, you can use data organized in folders by specifying the folder path in the Custom form project creation steps. *See* [**Organize your data in subfolders**](../how-to-guides/build-a-custom-model.md?view=doc-intel-2.1.0&preserve-view=true#organize-your-data-in-subfolders-optional)

## Use Document Intelligence Studio features

### Auto label documents with prebuilt models or one of your own models

* In custom extraction model labeling page, you can now auto label your documents using one of Document Intelligent Service prebuilt models or your trained models.

    :::image type="content" source="../media/studio/auto-label.gif" alt-text="Animated screenshot showing auto labeling in Studio.":::

* For some documents, duplicate labels after running autolabel are possible. Make sure to modify the labels so that there are no duplicate labels in the labeling page afterwards.

    :::image type="content" source="../media/studio/duplicate-labels.png" alt-text="Screenshot showing duplicate label warning after auto labeling.":::

### Auto label tables

* In custom extraction model labeling page, you can now auto label the tables in the document without having to label the tables manually.

    :::image type="content" source="../media/studio/auto-table-label.gif" alt-text="Animated screenshot showing auto table labeling in Studio.":::

### Add test files directly to your training dataset

* Once you train a custom extraction model, make use of the test page to improve your model quality by uploading test documents to training dataset if needed.

* If a low confidence score is returned for some labels, make sure to correctly label your content. If not, add them to the training dataset and relabel to improve the model quality.

    :::image type="content" source="../media/studio/add-from-test.gif" alt-text="Animated screenshot showing how to add test files to training dataset.":::

### Make use of the document list options and filters in custom projects

* Use the custom extraction model labeling page to navigate through your training documents with ease by making use of the search, filter, and sort by feature.

* Utilize the grid view to preview documents or use the list view to scroll through the documents more easily.

    :::image type="content" source="../media/studio/document-options.png" alt-text="Screenshot of document list view options and filters.":::

### Project sharing

Share custom extraction projects with ease. For more information, see [Project sharing with custom models](../how-to-guides/project-share-custom-models.md).

## Next steps

* Follow our [**Document Intelligence v3.1 migration guide**](../v3-1-migration-guide.md) to learn the differences from the previous version of the REST API.
* Explore our [**v4.0 SDK quickstarts**](get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true) to try the v3.0 features in your applications using the new client libraries.
* Refer to our [**v4.0 REST API quickstarts**](get-started-sdks-rest-api.md?view=doc-intel-4.0.0&preserve-view=true) to try the v3.0 features using the new REST API.

[Get started with the Document Intelligence Studio](https://formrecognizer.appliedai.azure.com).
