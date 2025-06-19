---
title: "Batch Document translation C#/.NET or Python client library"
titleSuffix: Azure AI services
description: Use the Batch Document translation C#/.NET or Python client library (SDK) for cloud-based batch document translation service and process.
author: laujan
manager: nitinme
ms.service: azure-ai-translator
ms.custom: devx-track-dotnet, devx-track-python
ms.topic: quickstart
ms.date: 04/14/2025
ms.author: lajanuar
zone_pivot_groups: programming-languages-document-sdk
---

# Get started: Document translation client libraries
<!-- markdownlint-disable MD024 -->
<!-- markdownlint-disable MD001 -->

Document translation is a cloud-based feature of the [Azure AI Translator](../../translator-overview.md) service that asynchronously translates whole documents in [supported languages](../../language-support.md) and various [file formats](../overview.md#batch-supported-document-formats). In this quickstart, learn to use Document translation with a programming language of your choice to translate a source document into a target language while preserving structure and text formatting.

> [!IMPORTANT]
>
> * Document translation is currently supported in the Azure AI Translator (single-service) resource only, and is **not** included in the Azure AI services (multi-service) resource.
> * Document translation is supported in paid tiers. The Language Studio supports the S1 or D3 instance tiers. We suggest that you select Standard S1 to try Document translation. *See* [Azure AI services pricing—Translator](https://azure.microsoft.com/pricing/details/cognitive-services/translator/).
> * Document translation public preview releases provide early access to features that are in active development. Features, approaches, and processes can change, before General Availability (GA) release, based on user feedback.
> * The public preview version of Document translation client libraries default to REST API version **2024-05-01**.

## Prerequisites

To get started, you need:

* An active [**Azure account**](https://azure.microsoft.com/free/cognitive-services/). If you don't have one, you can [**create a free account**](https://azure.microsoft.com/free/).

* A [**single-service Azure AI Translator resource**](https://portal.azure.com/#create/Microsoft.CognitiveServicesTextTranslation) (**not** a multi-service Azure AI Foundry resource). If you're planning on using the Document translation feature with [managed identity authorization](../how-to-guides/create-use-managed-identities.md), choose a geographic region such as **East US**. Select the **Standard S1 Standard Service Plan or C2, C3, C4, or D3 Volume Discount Plans**.

* An [**Azure Blob Storage account**](https://portal.azure.com/#create/Microsoft.StorageAccount-ARM). You'll [**create containers**](/azure/storage/blobs/storage-quickstart-blobs-portal#create-a-container) in your Azure Blob Storage account for your source and target files:

  * **Source container**. This container is where you upload your files for translation (required).
  * **Target container**. This container is where your translated files are stored (required).

### Storage container authorization

You can choose one of the following options to authorize access to your Azure AI Translator resource.

**✔️ Managed Identity**. A managed identity is a service principal that creates a Microsoft Entra identity and specific permissions for an Azure managed resource. Managed identities enable you to run your Azure AI Translator application without having to embed credentials in your code. Managed identities are a safer way to grant access to storage data and replace the requirement for you to include shared access signature tokens (SAS) with your source and target URLs.

To learn more, *see* [Managed identities for Document translation](../how-to-guides/create-use-managed-identities.md).

  :::image type="content" source="../media/managed-identity-rbac-flow.png" alt-text="Screenshot of managed identity flow (RBAC).":::

**✔️ Shared Access Signature (SAS)**. A shared access signature is a URL that grants restricted access for a specified period of time to your Translator service. To use this method, you need to create Shared Access Signature (SAS) tokens for your source and target containers. The `sourceUrl`  and `targetUrl` must include a Shared Access Signature (SAS) token, appended as a query string. The token can be assigned to your container or specific blobs.

* Your **source** container or blob must designate **read** and **list** access.
* Your **target** container or blob must designate **write** and **list** access.

To learn more, *see* [**Create SAS tokens**](../how-to-guides/create-sas-tokens.md).

  :::image type="content" source="../media/sas-url-token.png" alt-text="Screenshot of a resource URI with a SAS token.":::

::: zone pivot="programming-language-csharp"

[!INCLUDE [C# programming](includes/sdk/csharp.md)]
::: zone-end

::: zone pivot="programming-language-python"

[!INCLUDE [Python programming](includes/sdk/python.md)]
::: zone-end

### Next step

> [!div class="nextstepaction"]
> [**Learn more about Document translation operations**](../how-to-guides/use-rest-api-programmatically.md)
