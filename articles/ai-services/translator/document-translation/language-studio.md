---
title: Try Document translation in Language Studio
description: "Document translation in Azure AI Language Studio."
author: laujan
manager: nitinme
ms.service: azure-ai-translator
ms.topic: quickstart
ms.date: 04/14/2025
ms.author: lajanuar
ms.custom: references_regions, build-2023
recommendations: false
---

# Document translation in Language Studio (preview)

> [!IMPORTANT]
>
> * Document translation in Language Studio is currently in Public Preview. Features, approaches, and processes can change, before General Availability (GA) release, based on user feedback.
>
> * Currently, virtual network connectivity isn't supported for the Document translation feature in the Language Studio.

 Document translation in [**Azure AI Language Studio**](https://language.cognitive.azure.com/home) is a no-code user interface that lets you interactively translate documents from local or Azure Blob Storage.

## Supported regions

The Document translation feature in the Language Studio is currently available in the following regions;

|DisplayName|Name|
|-----------|------|
|East US |`eastus`|
|East US 2 |`eastus2`|
|West US 2 | `westus2`|
|West US 3| `westus3`|
|UK South| `uksouth`|
|South Central US| `southcentralus` |
|Australia East|`australiaeast` |
|Central India| `centralindia` |
|North Europe| `northeurope` |
|West Europe|`westeurope`|
|Switzerland North| `switzerlandnorth` |

## Prerequisites

If you or an administrator have previously setup a Translator resource with a **system-assigned managed identity**, enabled a **Storage Blob Data Contributor** role assignment, and created an Azure Blob Storage account, you can skip this section and [**Get started**](#get-started) right away.

> [!NOTE]
>
> * Document translation is currently supported in the Translator (single-service) resource only, and is **not** included in the Azure AI services (multi-service) resource.
>
> * Document translation is supported in the S1 Standard Service Plan or in the D3 Volume Discount Plan. *See* [Azure AI services pricing—Translator](https://azure.microsoft.com/pricing/details/cognitive-services/translator/).
>

Document translation in Language Studio requires the following resources:

* An active [**Azure account**](https://azure.microsoft.com/free/cognitive-services/). If you don't have one, you can [**create a free account**](https://azure.microsoft.com/free/).

* A [**single-service Translator resource**](https://portal.azure.com/#create/Microsoft.CognitiveServicesTextTranslation) (**not** a multi-service Azure AI Foundry resource) with [**system-assigned managed identity**](how-to-guides/create-use-managed-identities.md#enable-a-system-assigned-managed-identity) enabled and a [**Storage Blob Data Contributor**](how-to-guides/create-use-managed-identities.md#grant-storage-account-access-for-your-translator-resource) role assigned. For more information, *see* [**Managed identities for Document translation**](how-to-guides/create-use-managed-identities.md). Also, make sure the region and pricing sections are completed as follows:

  * **Resource Region**. For this project, choose a geographic region such as **East US**. For Document translation, [system-assigned managed identity](how-to-guides/create-use-managed-identities.md) isn't supported for the **Global** region.

  * **Pricing tier**. Select Standard S1 or D3. Document translation isn't supported in the free tier.

* An [**Azure Blob Storage account**](https://portal.azure.com/#create/Microsoft.StorageAccount-ARM). An active Azure Blob Storage account is required to use Document translation in the Language Studio.

Now that you completed the prerequisites, let's start translating documents!

## Get started

At least one **source document** is required. You can download our [document translation sample document](https://raw.githubusercontent.com/Azure-Samples/cognitive-services-REST-api-samples/master/curl/Translator/document-translation-sample.docx). The source language is English.

1. Navigate to [Language Studio](https://language.cognitive.azure.com/home).

1. If you're using the Language Studio for the first time, a **Select an Azure resource** pop-up screen appears. Make the following selections:

   * **Azure directory**.
   * **Azure subscription**.
   * **Resource type**. Choose **Translator**.
   * **Resource name**. The resource you select must have [**managed identity enabled**](how-to-guides/create-use-managed-identities.md).

   :::image type="content" source="media/language-studio/choose-azure-resource.png" alt-text="Screenshot of the language studio choose your Azure resource dialog window.":::

    > [!TIP]
    > You can update your selected directory and resource by selecting the Translator settings icon located in the left navigation section.

1. Navigate to Language Studio and select the **Document translation** tile:

    :::image type="content" source="media/language-studio/welcome-home-page.png" alt-text="Screenshot of the language studio home page.":::

1. If you're using the Document translation feature for the first time, start with the **Initial Configuration** to select your **Azure AI Translator resource** and **Document storage** account:

   :::image type="content" source="media/language-studio/initial-configuration.png" alt-text="Screenshot of the initial configuration page.":::

1. In the **Job** section, choose the language to **Translate from** (source) or keep the default **Auto-detect language** and select the language to **Translate to** (target). You can select a maximum of 10 target languages. Once you select your source and target languages, select **Next**:

   :::image type="content" source="media/language-studio/basic-information.png" alt-text="Screenshot of the language studio basic information page.":::

## File location and destination

Your source and target files can be located in your local environment or your Azure Blob Storage [container](/azure/storage/blobs/storage-quickstart-blobs-portal#create-a-container). Follow the steps to select where to retrieve your source and store your target files:

### Choose a source file location

#### [**Local**](#tab/local-env)

 1. In the **files and destination** section, choose the files for translation by selecting the **Upload local files** button.

 1. Next, select **&#x2795; Add file(s)**, choose the files for translation, then select **Next**:

   :::image type="content" source="media/language-studio/upload-file.png" alt-text="Screenshot of the select files for translation page.":::

#### [**Azure Blob Storage**](#tab/blob-storage)

1. In the **files and destination** section, choose the files for translation by selecting the **Select for Blob storage** button.

1. Next, choose your *source* **Blob container**, find and select the files for translation, then select **Next**:

   :::image type="content" source="media/language-studio/select-blob-container.png" alt-text="Screenshot of select files from your blob container.":::

---

### Choose a target file destination

#### [**Local**](#tab/local-env)

While still in the **files and destination** section, select **Download translated file(s)**. Once you make your choice, select **Next**:

   :::image type="content" source="media/language-studio/target-file-upload.png" alt-text="Screenshot of the select destination for target files page.":::

#### [**Azure Blob Storage**](#tab/blob-storage)

1. While still in the **files and destination** section, select **Upload to Azure Blob Storage**.
1. Next, choose your *target* **Blob container** and select **Next**:

   :::image type="content" source="media/language-studio/target-file-upload.png" alt-text="Screenshot of target file upload drop-down menu.":::

---

### Optional selections and review

1. (Optional) You can add **additional options** for custom translation and/or a glossary file. If you don't require these options, just select **Next**.

1. On the **Review and finish** page, check to make sure that your selections are correct. If not, you can go back. If everything looks good, select the **Start translation job** button.

    :::image type="content" source="media/language-studio/start-translation.png" alt-text="Screenshot of the start translation job page.":::

1. The **Job history** page contains the **Translation job id** and job status.

    > [!NOTE]
    > The list of translation jobs on the job history page includes all the jobs that were submitted through the chosen translator resource. If your colleague used the same translator resource to submit a job, the status of that job appears on the job history page.

   :::image type="content" source="media/language-studio/job-history.png" alt-text="Screenshot of the job history page.":::

That's it! You now know how to translate documents using Azure AI Language Studio.

## Next steps

> [!div class="nextstepaction"]
>
> [Use Document translation REST APIs programmatically](how-to-guides/use-rest-api-programmatically.md)
