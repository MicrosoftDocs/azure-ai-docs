---
title: Prerequisites and Setup for Document Translation API
titleSuffix: Foundry Tools
description: Learn about the prerequisites and setup required to use the Document Translation API, including Azure resources, authentication methods, and infrastructure requirements for different translation processes.
author: laujan
ms.author: lajanuar
manager: mcleans
ms.service: azure-ai-translator
ms.topic: checklist
ms.date: 06/02/2026
---
<!-- markdownlint-disable MD025 -->
# Prerequisites and setup

The Document Translation API lets you translate documents at scale or on demand. Before you configure your environment, choose the translation process that fits your workload. Each process has different infrastructure requirements and is optimized for different scenarios.

The API supports two translation processes:

* [Asynchronous batch translation](rest-api/translate-asynchronous.md) — Use this process to translate multiple documents or large files in parallel. You need an Azure Blob Storage account with separate containers for your source and translated documents.
* [Synchronous single file](rest-api/translate-synchronous.md) — Use this process to translate a single document without Azure Blob Storage. The API returns the translated document directly in the response.


## Azure resources

Make sure you have the following before you start:

* You need an active **Azure subscription**. If you don't have one, you can [create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

* For **NMT-based translation**, you need an **Azure Translator resource** with a custom domain endpoint:
    * Create an [Azure Translator resource](https://portal.azure.com/#create/Microsoft.CognitiveServicesTextTranslation) in the Azure portal.
    * After your resource deploys, select **Go to resource** and retrieve your key and endpoint. You use these values to connect your application to the Translator service.

* An **Azure Blob Storage account** (required for asynchronous batch translation) with the following containers:
    * A **source** container for your input documents.
    * A **target** container for your translated documents.

## Authentication

The Document Translation API uses key-based authentication for the Translator resource and separate authorization for Azure Blob Storage access. Configure both before making API requests.

### Translator API authentication

To authenticate requests to the Translator API, include your resource key in the request header. You can find your key on the **Keys and Endpoint** page of your Translator resource in the Azure portal.

Include the following header:

```bash
Ocp-Apim-Subscription-Key: <your-key>
```

If using a regional resource, include:

```bash
Ocp-Apim-Subscription-Region: <your-subscription-region>
```

### Storage authorization (choose one)

To access your source and target Blob Storage containers, the API needs authorization. Choose one of the following methods based on your security requirements.

#### Option 1: Managed identity

With a managed identity, Azure grants your Translator resource access to Blob Storage without requiring you to embed credentials in your code. This is the recommended approach because it eliminates the need to generate and manage shared access signature (SAS) tokens for your source and target URLs.

For setup instructions, see [Managed identities for Document Translation](../how-to-guides/create-use-managed-identities.md).

#### Option 2: Shared Access Signature (SAS)

A SAS token is a URL query string that grants time-limited, scoped access to a Blob Storage container or blob. Append a SAS token to each `sourceUrl` and `targetUrl` in your request. You can scope a token to an entire container or to specific blobs.

Your SAS tokens must include the following permissions:

* **Source** container or blob: **read** and **list**
* **Target** container or blob: **write** and **list**

For instructions on generating tokens, see [Create SAS tokens](../how-to-guides/create-sas-tokens.md).