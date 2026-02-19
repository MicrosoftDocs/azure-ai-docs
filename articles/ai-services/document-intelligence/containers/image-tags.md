---
title: Document Intelligence container image tags and release notes
titleSuffix: Foundry Tools
description: A listing of all Document Intelligence container image tags.
author: laujan
manager: nitinme
ms.service: azure-ai-document-intelligence
ms.topic: reference
ms.date: 11/18/2025
ms.author: lajanuar
---

# Document Intelligence container tags

<!-- markdownlint-disable MD051 -->

:::moniker range="doc-intel-2.1.0"

Support for containers is currently available with Document Intelligence version `2022-08-31 (GA)` for all models, `2023-07-31 (GA)` for Read, Layout, Invoice, Receipt, and ID Document models, and `2024-11-30 (GA)` for Read and Layout model:

* [REST API `2022-08-31 (GA)`](/rest/api/aiservices/document-models/analyze-document?view=rest-aiservices-v3.0%20(2022-08-31)&preserve-view=true&tabs=HTTP)
* [REST API `2023-07-31 (GA)`](/rest/api/aiservices/document-models/analyze-document?view=rest-aiservices-v3.1%20(2023-07-31)&tabs=HTTP&preserve-view=true)
* [REST API `2024-11-30 (GA)`](/rest/api/aiservices/document-models/analyze-document?view=rest-aiservices-v4.0%20(2024-11-30)&tabs=HTTP&preserve-view=true)
* [Client libraries targeting `REST API 2022-08-31 (GA)`](../sdk-overview-v3-0.md)
* [Client libraries targeting `REST API 2023-07-31 (GA)`](../sdk-overview-v3-1.md)
* [Client libraries targeting `REST API 2024-11-30 (GA)`](../sdk-overview-v4-0.md)

✔️ See [**Document Intelligence v3.0 container image tags**](?view=doc-intel-3.0.0&preserve-view=true) or [**Document Intelligence v3.1 container image tags**](?view=doc-intel-3.1.0&preserve-view=true) or [**Document Intelligence v4.0 container image tags**](?view=doc-intel-4.0.0&preserve-view=true) for supported versions of container documentation.

:::moniker-end

::: moniker range="doc-intel-3.0.0"

**This content applies to:** ![checkmark](../media/yes-icon.png) **v3.0 (GA)**

## Microsoft container registry (MCR)

Document Intelligence container images can be found within the [**Microsoft Artifact Registry** (also know as Microsoft Container Registry(MCR))](https://mcr.microsoft.com/catalog?search=document%20intelligence), the primary registry for all Microsoft published container images.

The following containers support DocumentIntelligence v3.0 models and features:

| Container name |image |
|---|---|
|[**Document Intelligence Studio**](https://mcr.microsoft.com/product/azure-cognitive-services/form-recognizer/studio/tags)| `mcr.microsoft.com/azure-cognitive-services/form-recognizer/studio:latest`|
| [**Business Card 3.0**](https://mcr.microsoft.com/product/azure-cognitive-services/form-recognizer/businesscard-3.0/tags) | `mcr.microsoft.com/azure-cognitive-services/form-recognizer/businesscard-3.0:latest` |
| [**Custom Template 3.0**](https://mcr.microsoft.com/product/azure-cognitive-services/form-recognizer/custom-template-3.0/tags) | `mcr.microsoft.com/azure-cognitive-services/form-recognizer/custom-template-3.0:latest` |
| [**Document 3.0**](https://mcr.microsoft.com/product/azure-cognitive-services/form-recognizer/document-3.0/tags)| `mcr.microsoft.com/azure-cognitive-services/form-recognizer/document-3.0:latest`|
| [**ID Document 3.0**](https://mcr.microsoft.com/product/azure-cognitive-services/form-recognizer/id-document-3.0/tags) |  `mcr.microsoft.com/azure-cognitive-services/form-recognizer/id-document-3.0:latest` |
| [**Invoice 3.0**](https://mcr.microsoft.com/product/azure-cognitive-services/form-recognizer/invoice-3.0/tags) |`mcr.microsoft.com/azure-cognitive-services/form-recognizer/invoice-3.0:latest`|
| [**Layout 3.0**](https://mcr.microsoft.com/product/azure-cognitive-services/form-recognizer/layout/tags) |`mcr.microsoft.com/azure-cognitive-services/form-recognizer/layout-3.0:latest`|
| [**Read 3.0**](https://mcr.microsoft.com/product/azure-cognitive-services/form-recognizer/read-3.0/tags) |`mcr.microsoft.com/azure-cognitive-services/form-recognizer/read-3.0:latest`|
| [**Receipt 3.0**](https://mcr.microsoft.com/product/azure-cognitive-services/form-recognizer/receipt-3.0/tags) |`mcr.microsoft.com/azure-cognitive-services/form-recognizer/receipt-3.0:latest`|

::: moniker-end

::: moniker range="doc-intel-3.1.0"

**This content applies to:** ![checkmark](../media/yes-icon.png) **v3.1 (GA)**

## Microsoft container registry (MCR)

Document Intelligence container images can be found within the [**Microsoft Artifact Registry** (also know as Microsoft Container Registry(MCR))](https://mcr.microsoft.com/catalog?search=document%20intelligence), the primary registry for all Microsoft published container images.

The following containers support DocumentIntelligence v3.1 models and features:

| Container name |image |
|---|---|
| [**Read 3.1**](https://mcr.microsoft.com/product/azure-cognitive-services/form-recognizer/read-3.1/tags) |`mcr.microsoft.com/azure-cognitive-services/form-recognizer/read-3.1:latest`|
| [**Layout 3.1**](https://mcr.microsoft.com/en-us/product/azure-cognitive-services/form-recognizer/layout-3.1/tags) |`mcr.microsoft.com/azure-cognitive-services/form-recognizer/layout-3.1:latest`|
| [**Invoice 3.1**](https://mcr.microsoft.com/product/azure-cognitive-services/form-recognizer/invoice-3.1/tags) |`mcr.microsoft.com/azure-cognitive-services/form-recognizer/invoice-3.1:latest`|
| [**ID Document 3.1**](https://mcr.microsoft.com/product/azure-cognitive-services/form-recognizer/id-document-3.1/tags) |  `mcr.microsoft.com/azure-cognitive-services/form-recognizer/id-document-3.1:latest` |
| [**Receipt 3.1**](https://mcr.microsoft.com/product/azure-cognitive-services/form-recognizer/receipt-3.1/tags) |`mcr.microsoft.com/azure-cognitive-services/form-recognizer/receipt-3.1:latest`|
| [**Custom Template 3.1**](https://mcr.microsoft.com/en-us/artifact/mar/azure-cognitive-services/form-recognizer/custom-template-3.1/tags) |`mcr.microsoft.com/azure-cognitive-services/form-recognizer/custom-template-3.1:latest`|

::: moniker-end

::: moniker range="doc-intel-4.0.0"
**This content applies to:** ![checkmark](../media/yes-icon.png) **v4.0 (GA)**

## Microsoft container registry (MCR)

Document Intelligence container images can be found within the [**Microsoft Artifact Registry** (also know as Microsoft Container Registry(MCR))](https://mcr.microsoft.com/catalog?search=document%20intelligence), the primary registry for all Microsoft published container images.

The following containers support Document Intelligence v4.0 models and features:

| Container name |image |
|---|---|
| [**Layout 4.0**](https://mcr.microsoft.com/en-us/product/azure-cognitive-services/form-recognizer/layout-4.0/tags) |`mcr.microsoft.com/azure-cognitive-services/form-recognizer/layout-4.0:latest`|
| [**Read 4.0**](https://mcr.microsoft.com/product/azure-cognitive-services/form-recognizer/read-4.0/tags) |`mcr.microsoft.com/azure-cognitive-services/form-recognizer/read-4.0:latest`|
::: moniker-end


:::moniker range="doc-intel-2.1.0"

> [!IMPORTANT]
>
> Document Intelligence v3.0 containers are now generally available. If you're getting started with containers, consider using the v3 containers.
The following containers:

## Feature containers

Document Intelligence containers support the following features:

| Container name | Fully qualified image name |
|---|---|
| **Layout** | mcr.microsoft.com/azure-cognitive-services/form-recognizer/layout |
| **Business Card** | mcr.microsoft.com/azure-cognitive-services/form-recognizer/businesscard |
| **ID Document** | mcr.microsoft.com/azure-cognitive-services/form-recognizer/id-document |
| **Receipt** | mcr.microsoft.com/azure-cognitive-services/form-recognizer/receipt |
| **Invoice** | mcr.microsoft.com/azure-cognitive-services/form-recognizer/invoice |
| **Custom API** | mcr.microsoft.com/azure-cognitive-services/form-recognizer/custom-api |
| **Custom Supervised** | mcr.microsoft.com/azure-cognitive-services/form-recognizer/custom-supervised |

> [!IMPORTANT]
> The Document Intelligence v1.0 container is retired.

## Next steps

> [!div class="nextstepaction"]
> [Install and run Document Intelligence containers](install-run.md)
:::moniker-end
