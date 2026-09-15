---
title: API Versions
description: Version policy for Azure AI Search REST APIs and the Azure SDK client libraries.
ms.service: azure-ai-search
ms.custom:
  - devx-track-dotnet
  - devx-track-extended-java
  - devx-track-js
  - devx-track-python
  - ignite-2023
ms.topic: concept-article
ms.date: 07/28/2026
ai-usage: ai-assisted
---

# API versions in Azure AI Search

[!INCLUDE [search-fiq-banner](./includes/search-fiq-banner.md)]

Azure AI Search rolls out feature updates regularly. Sometimes, but not always, these updates require a new version of the API to preserve backward compatibility. Publishing a new version allows you to control when and how you integrate search service updates in your code.

As a rule, the REST APIs and Azure SDK client libraries are versioned only when necessary, since it can involve some effort to upgrade your code to use a new API version. A new version is needed only if some aspect of the API has changed in a way that breaks backward compatibility. Such changes can happen because of fixes to existing features, or because of new features that change existing API surface area.

For more information about the deprecation path, see the [Azure SDK lifecycle and support policy](https://azure.github.io/azure-sdk/policies_support.html).

## Deprecated versions

**2023-07-01-preview** was deprecated on April 8, 2024 and is no longer supported as of July 8, 2024. This version was the first REST API that offered vector search support. Newer API versions have a different vector configuration. [Migrate to a newer API version](search-api-migration.md) or to a newer SDK version as soon as possible.

<a name="unsupported-versions"></a>

## Discontinued versions

As of October 15, 2020, the following API versions are discontinued and no longer documented or supported:

+ **2015-02-28**
+ **2015-02-28-Preview**
+ **2014-07-31-Preview**
+ **2014-10-20-Preview**

All SDKs are based on REST API versions. If a REST API version is discontinued, the SDK packages based on it are also discontinued. All Azure AI Search .NET SDKs older than [**3.0.0-rc**](https://www.nuget.org/packages/Microsoft.Azure.Search/3.0.0-rc) are now obsolete.

If you have code that uses a discontinued version, [migrate to a newer API version](search-api-migration.md) or to a newer SDK version.

## REST APIs

| REST API | Link |
|----------|------|
| Search Service (data plane) | See [API versions](/rest/api/searchservice/search-service-api-versions) in the REST API reference. |
| Search Management (control plane) | See [API versions](/rest/api/searchmanagement/management-api-versions) in the REST API reference. |

## Azure SDK for .NET

| SDK version | Status | Changelog | Description |
|-------------|--------|------------ |-----------------|
| [Azure.Search.Documents 12](/dotnet/api/overview/azure/search.documents-readme) | Active | [Changelog](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/search/Azure.Search.Documents/CHANGELOG.md) | APIs for data plane operations on a service, such as read-write operations on content and objects. |
| [Azure.ResourceManager.Search](https://www.nuget.org/packages/Microsoft.Azure.Management.Search/4.0.0) | Active | [Changelog](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/search/Azure.ResourceManager.Search/CHANGELOG.md) | APIs for control plane operations on the search service. |

## Azure SDK for Java

| SDK version | Status | Changelog | Description |
|-------------|--------|------------|-----------------|
| [azure-search-documents 12](/java/api/overview/azure/search-documents-readme) | Active | [Changelog](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | Use the `azure-search-documents` client library for data plane operations. |
| [azure-resourcemanager-search 2](/java/api/overview/azure/resourcemanager-search-readme) | Active | [Changelog](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/search/azure-resourcemanager-search/CHANGELOG.md) | Use the `azure-resourcemanager-search` client library for control plane operations. |

## Azure SDK for JavaScript

| SDK version | Status | Changelog | Description |
|-------------|--------|------------|------------------|
| [@azure/search-documents 13](/javascript/api/overview/azure/search-documents-readme) | Active | [Changelog](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/search/search-documents/CHANGELOG.md) | Use the `@azure/search-documents` client library for data plane operations. |
| [@azure/arm-search 4](/javascript/api/overview/azure/arm-search-readme) | Active | [Changelog](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/search/arm-search/CHANGELOG.md) | Use the `@azure/arm-search` package for control plane operations. |

## Azure SDK for Python

| SDK version | Status | Changelog | Description |
|-------------|--------|------------|------------------|
| [azure-search-documents 12](/python/api/overview/azure/search-documents-readme) | Active | [Changelog](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | Use the `azure-search-documents` client library for data plane operations. |
| [azure-mgmt-search 9](https://pypi.org/project/azure-mgmt-search/) | Active | [Changelog](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/search/azure-mgmt-search/CHANGELOG.md) | Use the `azure-mgmt-search` client library for control plane operations. |

## All Azure SDKs

If you're looking for beta client libraries and documentation, [this page](https://azure.github.io/azure-sdk/releases/latest/index.html) contains links to all of the Azure SDK library packages, code, and docs.
