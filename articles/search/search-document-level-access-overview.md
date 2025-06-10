---
title: Document-level access control
titleSuffix: Azure AI Search
description: Conceptual overview of document-level permissions in Azure AI Search.
author: gmndrg
ms.author: gimondra
ms.date: 06/06/2025
ms.service: azure-ai-search
ms.topic: conceptual
ms.custom:
  - build-2025
---
  
# Document-level access control in Azure AI Search  
  
Azure AI Search supports document-level access control, enabling organizations to enforce fine-grained permissions at the document level, from data ingestion through query execution. This capability is essential for building secure AI agentic systems grounding data, Retrieval-Augmented Generation (RAG) applications, and enterprise search solutions that require authorization checks at the document level.  
  
## Approaches for document-level access control

| Approach | Description |
|----------|-------------|
| Security filters | String comparison. Your application passes in a user or group identity as a string, which populates a filter on a query, excluding any documents that don't match on the string. <br><br>Security filters are a technique for achieving document-level access control. This approach isn't bound to an API so you can use any version or package. |
| ACLs (preview) | Microsoft Entra ID security principal behind the query token is compared to the permission metadata of documents returned in search results, excluding any documents that don't match on permissions. <br><br>Built-in access control list (ACL) support for principals is in preview, available in REST APIs and prerelease Azure SDK packages that provide the feature. |

## Pattern for security trimming using filters  

For scenarios where native ACL integration isn't viable, we recommend security filters for trimming results based on exclusion criteria. The pattern includes the following components:

- Create a string field in the index to store strings of user or group identities.
- Load the index with source documents that include a field containing the identities.
- Include a filter expression in your query logic for matching on the string.
- At query time, get the identity of the caller.
- Pass in the identity of the caller as the filter string.

You can use push or pull model APIs. Because this approach is API agnostic, you just need to ensure that the index and query have valid strings (identities) for the filtration step.

This approach is useful for systems with custom access models or non-Microsoft security frameworks. For more information this approach, see [Security filters for trimming results in Azure AI Search](search-security-trimming-for-azure-search.md).

## Pattern for native support for POSIX-like ACL permissions (preview)

Native support is based on Microsoft Entra ID user and group access IDs affiliated with documents that you want to index and query. We recommend group access IDs for ease of management. The pattern includes the following components:

- Start with documents or files that have ACL assignments.
- [Enable permission filters](/rest/api/searchservice/indexes/create-or-update?view=rest-searchservice-2025-05-01-preview&preserve-view=true#searchindexpermissionfilteroption) in the index.
- [Add a permission filter](/rest/api/searchservice/indexes/create-or-update?view=rest-searchservice-2025-05-01-preview&preserve-view=true#permissionfilter) to a string field in an index.
- Load the index with source documents having associated ACLs.
- Query the index, [adding `x-ms-query-source-authorization`](/rest/api/searchservice/documents/search-post?view=rest-searchservice-2025-05-01-preview&preserve-view=true#request-headers) in the request header.

You can use the push model API, pushing any JSON documents to the search index, where the payload includes a string field providing POSIX-like ACLs for each document.

Or, use the pull model (indexer) APIs if the data source is [Azure Data Lake Storage (ADLS) Gen2](/azure/storage/blobs/data-lake-storage-introduction).  
  
### Retrieve permissions metadata during data ingestion process

How you retrieve permissions varies depending on whether you're pushing a documents payload or using the ADLS Gen2 indexer.

Start with a preview API that provides the feature:

- [2025-05-01 preview REST API](/rest/api/searchservice/documents/?view=rest-searchservice-2025-05-01-preview&preserve-view=true)
- [Azure SDK for Python prerelease package](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/search/azure-search-documents/CHANGELOG.md#1160b12-2025-05-14)
- [Azure SDK for .NET prerelease package](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/search/Azure.Search.Documents/CHANGELOG.md#1170-beta4-2025-05-14)
- [Azure SDK for Java prerelease package](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/search/azure-search-documents/CHANGELOG.md#1180-beta7-2025-05-16)

For the [push model approach](search-index-access-control-lists-and-rbac-push-api.md):

1. Ensure your index schema is also created with a preview or prerelease SDK and that the schema has permission filters.
1. Consider using the Microsoft Graph SDK to get group or user IDs.
1. Use the [Index Documents](/rest/api/searchservice/documents/?view=rest-searchservice-2025-05-01-preview&preserve-view=true#indexdocumentsresult) or equivalent Azure SDK API to push documents and their associated permission metadata into the search index. 

For the [pull model ADLS Gen2 indexer approach](search-indexer-access-control-lists-and-role-based-access.md):

1. Verify that files in the directory are secured using the [ADLS Gen2 access control model](/azure/storage/blobs/data-lake-storage-access-control-model).
1. Use the [Create Indexer](/rest/api/searchservice/indexers/create?view=rest-searchservice-2025-05-01-preview&preserve-view=true) or equivalent Azure SDK API to create the indexer, index, and data source. 

### Enforce document-level permissions at query time

With native [token-based querying](https://aka.ms/azs-query-preserving-permissions), Azure AI Search validates a user's [Microsoft Entra token](/Entra/identity/devices/concept-tokens-microsoft-Entra-id), trimming result sets to include only documents the user is authorized to access. 

You can achieve automatic trimming by attaching the user's Microsoft Entra token to your query request. For more information, see [Query-Time ACL and RBAC enforcement in Azure AI Search](search-query-access-control-rbac-enforcement.md).

## Benefits of document-level access control  
  
Document-level access control is critical for safeguarding sensitive information in AI-driven applications. It helps organizations build systems that align with their access policies, reducing the risk of exposing unauthorized or confidential data. By integrating access rules directly into the search pipeline, AI systems can provide responses grounded in secure and authorized information.  

By offloading permission enforcement to Azure AI Search, developers can focus on building high-quality retrieval and ranking systems. This approach helps reducing the need to handle nested groups, write custom filters, or manually trim search results.  

Document-level permissions in Azure AI Search provide a structured framework for enforcing access controls that align with organizational policies. By using Microsoft Entra-based ACLs and RBAC roles, organizations can create systems that support robust compliance and promote trust among users. These built-in capabilities reduce the need for custom coding, offering a standardized approach to document-level security.  

## Tutorials and samples
  
Take a closer look at document-level access control in Azure AI Search with more articles and samples.

- [Tutorial: Index ADLS Gen2 permissions metadata using an indexer](tutorial-adls-gen2-indexer-acls.md)
- [azure-search-rest-samples/Quickstart-ACL](https://github.com/Azure-Samples/azure-search-rest-samples/tree/main/Quickstart-ACL)
- [azure-search-python-samples/Quickstart-Document-Permissions-Push-API](https://github.com/Azure-Samples/azure-search-python-samples/blob/main/Quickstart-Document-Permissions-Push-API)
- [azure-search-python-samples/Quickstart-Document-Permissions-Pull-API](https://github.com/Azure-Samples/azure-search-python-samples/blob/main/Quickstart-Document-Permissions-Pull-API)

## Related content

- [How to index document-level permissions using push API](search-index-access-control-lists-and-rbac-push-api.md)
- [How to index document-level permissions using the ADLS Gen2 indexer](search-indexer-access-control-lists-and-role-based-access.md)
- [How to query using Microsoft Entra token-based permissions](https://aka.ms/azs-query-preserving-permissions)