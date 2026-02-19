---
title: Document-level access control
titleSuffix: Azure AI Search
description: Conceptual overview of document-level permissions in Azure AI Search.
author: gmndrg
ms.author: gimondra
ms.date: 11/18/2025
ms.service: azure-ai-search
ms.topic: concept-article
ms.custom:
  - build-2025
---
  
# Document-level access control in Azure AI Search  
  
Azure AI Search supports document-level access control, enabling organizations to enforce fine-grained permissions at the document level, from data ingestion through query execution. This capability is essential for building secure AI agentic systems grounding data, Retrieval-Augmented Generation (RAG) applications, and enterprise search solutions that require authorization checks at the document level.  
  
## Approaches for document-level access control

| Approach | Description |
|----------|-------------|
| Security filters | String comparison. Your application passes in a user or group identity as a string, which populates a filter on a query, excluding any documents that don't match on the string. <br><br>Security filters are a technique for achieving document-level access control. This approach isn't bound to an API so you can use any version or package. |
| POSIX-like ACL  / RBAC scopes (preview) | Microsoft Entra security principal behind the query token is compared to the permission metadata of documents returned in search results, excluding any documents that don't match on permissions. Access Control Lists (ACL) permissions apply to Azure Data Lake Storage (ADLS) Gen2 directories and files. Role-based access control (RBAC) scopes apply to ADLS Gen2 content and to Azure blobs. <br><br>Built-in support for identity-based access at the document level is in preview, available in REST APIs and preview Azure SDK packages that provide the feature. Be sure to check the [SDK package change log](#retrieve-acl-permissions-metadata-during-data-ingestion-process-preview) for evidence of feature support.|
| Microsoft Purview sensitivity labels (preview) | Indexer extracts sensitivity labels defined in Microsoft Purview from supported data sources (Azure Blob Storage, ADLS Gen2, SharePoint in Microsoft 365, OneLake). These labels are stored as metadata and evaluated at query time to enforce user access based on Microsoft Entra tokens and Purview policy assignments. This approach aligns Azure AI Search authorization with your enterprise's Microsoft Information Protection model.|
| SharePoint in Microsoft 365 ACLs (preview) | When configured, Azure AI Search indexers extract SharePoint document permissions directly from in Microsoft 365 ACLs during initial ingestion. Access checks use Microsoft Entra user and group memberships. Supported group types include Microsoft Entra security groups, Microsoft 365 groups, and mail-enabled security groups. SharePoint groups are not yet supported in preview. |

## Pattern for security trimming using filters  

For scenarios where native ACL/RBAC scopes integration isn't viable, we recommend security string filters for trimming results based on exclusion criteria. The pattern includes the following components:

- To store user or group identities, create a string field in the index.
- Load the index using source documents that include associated ACLs.
- Include a filter expression in your query logic for matching on the string.
- At query time, get the identity of the caller.
- Pass in the identity of the caller as the filter string.
- Results are trimmed to exclude any matches that fail to include the user or group identity string,

You can use push or pull model APIs. Because this approach is API agnostic, you just need to ensure that the index and query have valid strings (identities) for the filtration step.

This approach is useful for systems with custom access models or non-Microsoft security frameworks. For more information this approach, see [Security filters for trimming results in Azure AI Search](search-security-trimming-for-azure-search.md).

## Pattern for native support for POSIX-like ACL and RBAC scope permissions (preview)

Native support is based on Microsoft Entra users and groups affiliated with documents that you want to index and query. 

Azure Data Lake Storage (ADLS) Gen2 containers support ACLs on the container and on files. For ADLS Gen2, RBAC scope preservation at document level is natively supported when you use an [ADLS Gen2 indexer](search-how-to-index-azure-data-lake-storage.md) or a [Blob knowledge source (supports ADLS Gen2)](agentic-knowledge-source-how-to-blob.md) and a preview API to ingest content. For Azure blobs using the [Azure blob indexer](search-blob-indexer-role-based-access.md) or knowledge source, RBAC scope preservation is at the container level.

For ACL-secured content, we recommend group access over individual user access for ease of management. The pattern includes the following components:

- Start with documents or files that have ACL assignments.
- [Enable permission filters](/rest/api/searchservice/indexes/create-or-update?view=rest-searchservice-2025-11-01-preview&preserve-view=true#searchindexpermissionfilteroption) in the index.
- [Add a permission filter](/rest/api/searchservice/indexes/create-or-update?view=rest-searchservice-2025-11-01-preview&preserve-view=true#permissionfilter) to a string field in an index.
- Load the index with source documents having associated ACLs.
- Query the index, adding [`x-ms-query-source-authorization`](/rest/api/searchservice/documents/search-post?view=rest-searchservice-2025-11-01-preview&preserve-view=true#request-headers) in the request header.

Your client app receives read permissions to the index through **Search Index Data Reader** or **Search Index Data Contributor** role. Access at query time is determined by user or group permission metadata in the indexed content. Queries that include a permission filter pass a user or group token as `x-ms-query-source-authorization` in the request header. When you use permission filters at query time, Azure AI Search checks for two things:

- First, it checks for **Search Index Data Reader** permission that allows your client application to access the index.

- Second, given the extra token on the request, it checks for user or group permissions on documents that are returned in search results, excluding any that don't match.

To get permission metadata into the index, you can use the push model API, pushing any JSON documents to the search index, where the payload includes a string field providing POSIX-like ACLs for each document. The important difference between this approach and security trimming is that the permission filter metadata in the index and query is recognized as Microsoft Entra ID authentication, whereas the security trimming workaround is simple string comparison. Also, you can use the Graph SDK to retrieve the identities.

You can also use the pull model (indexer) APIs if the data source is [Azure Data Lake Storage (ADLS) Gen2](/azure/storage/blobs/data-lake-storage-introduction) and your code calls a preview API for indexing.
  
### Retrieve ACL permissions metadata during data ingestion process (preview)

How you retrieve ACL permissions varies depending on whether you're pushing a documents payload or using the ADLS Gen2 indexer.

Start with a preview API that provides the feature:

- [2025-11-01-preview REST API](/rest/api/searchservice/documents/?view=rest-searchservice-2025-11-01-preview&preserve-view=true)
- [Azure SDK for Python prerelease package](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/search/azure-search-documents/CHANGELOG.md#1160b12-2025-05-14)
- [Azure SDK for .NET prerelease package](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/search/Azure.Search.Documents/CHANGELOG.md#1170-beta4-2025-05-14)
- [Azure SDK for Java prerelease package](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/search/azure-search-documents/CHANGELOG.md#1180-beta7-2025-05-16)

For the [push model approach](search-index-access-control-lists-and-rbac-push-api.md):

1. Ensure your index schema is also created with a preview or prerelease SDK and that the schema has permission filters.
1. Consider using the Microsoft Graph SDK to get group or user identities.
1. Use the [Index Documents](/rest/api/searchservice/documents/?view=rest-searchservice-2025-11-01-preview&preserve-view=true#indexdocumentsresult) or equivalent Azure SDK API to push documents and their associated permission metadata into the search index. 

For the [pull model ADLS Gen2 indexer approach](search-indexer-access-control-lists-and-role-based-access.md) or [Blob (ADLS Gen2) knowledge source](agentic-knowledge-source-how-to-blob.md):

1. Verify that files in the directory are secured using the [ADLS Gen2 access control model](/azure/storage/blobs/data-lake-storage-access-control-model).
1. Use the [Create Indexer REST API](/rest/api/searchservice/indexers/create?view=rest-searchservice-2025-11-01-preview&preserve-view=true) or [Create Knowledge Source REST API](/rest/api/searchservice/knowledge-sources/create?view=rest-searchservice-2025-11-01-preview&preserve-view=true) or equivalent Azure SDK API to create the indexer, index, and data source.

## Pattern for SharePoint in Microsoft 365 basic ACL permissions ingestion (preview)

For SharePoint in Microsoft 365 content, Azure AI Search can apply document-level permissions based on SharePoint ACLs. This integration promotes that only users or groups with access to the source document in SharePoint can retrieve it in search results, as soon as the permissions are synchronized in the index. Permissions are applied to the index either during initial document ingestion.

SharePoint ACL support is available in preview through the SharePoint indexer using the [2025-11-01-preview REST API](/rest/api/searchservice/data-sources/create?view=rest-searchservice-2025-11-01-preview&preserve-view=true) or supported SDK. The indexer extracts file and list item permission metadata and preserves it in the search index, where it's used to enforce access control at query time.

The pattern includes the following components:

- Use the SharePoint in Microsoft 365 indexer with application permissions to read SharePoint site content and full permissions to read ACLs. Follow the [SharePoint indexer ACL setup instructions](https://aka.ms/azs-sharepoint-indexer-acls) for enablement and limitations.
- During initial indexing, SharePoint ACL entries (users and groups) are stored as permission metadata in the search index.
- For incremental indexing of ACLs, review the [SharePoint ACL resync available mechanisms](https://aka.ms/azs-sharepoint-indexer-acls) available during public preview.
- At query time, Azure AI Search checks the Microsoft Entra principal in the query token against SharePoint ACL metadata stored in the index. It excludes any documents the caller isn't authorized to access.

During preview, only the following principal types are supported in SharePoint ACLs:

- Microsoft Entra user accounts  
- Microsoft Entra security groups  
- Microsoft 365 groups  
- Mail-enabled security groups  

SharePoint groups aren't supported in the preview release. 

For configuration details and full limitations, see [How to index SharePoint in Microsoft 365 document-level permissions (preview)](https://aka.ms/azs-sharepoint-indexer-acls).


## Pattern for Microsoft Purview sensitivity labels (preview)

Azure AI Search can ingest and enforce **Microsoft Purview sensitivity labels** for document-level access control, extending information protection policies from Microsoft Purview into your search and retrieval applications.

When label ingestion is enabled, Azure AI Search extracts sensitivity metadata from supported data sources. These include: Azure Blob Storage, Azure Data Lake Storage Gen2 (ADLS Gen2), SharePoint in Microsoft 365, and Microsoft OneLake. The extracted labels are stored in the index alongside document content.

At query time, Azure AI Search checks each document's sensitivity label, the user's Microsoft Entra token, and the organization's Purview policies to determine access.  Documents are returned only if the user's identity and label-based permissions allow access under the configured Purview policies.

The pattern includes the following components:

- Configure your [index](/rest/api/searchservice/indexes/create?view=rest-searchservice-2025-11-01-preview&preserve-view=true), [data source](/rest/api/searchservice/data-sources/create?view=rest-searchservice-2025-11-01-preview&preserve-view=true) and [indexer](/rest/api/searchservice/indexers/create?view=rest-searchservice-2025-11-01-preview&preserve-view=true) (for scheduling purposes) using the 2025-11-01-preview REST API or a corresponding SDK that supports Purview label ingestion.
- Enable a [system-assigned managed identity](search-how-to-managed-identities.md) to your search service. Then ask your tenant global administrator or privileged role administrator to [grant the required access](search-indexer-sensitivity-labels.md), so the search service can securely access Microsoft Purview and extract label metadata.
- Apply sensitivity labels to documents before indexing so they can be recognized and preserved during ingestion.
- At query time, attach a valid Microsoft Entra token via the header `x-ms-query-source-authorization` to each query request. Azure AI Search evaluates the token and the associated label metadata to enforce label-based access control.

Purview sensitivity label enforcement is limited to single-tenant scenarios, requires RBAC authentication, and during public preview is supported only through REST API or SDK. Autocomplete and Suggest APIs aren't available for Purview-enabled indexes at this time.

For more information, see [Use Azure AI Search indexers to ingest Microsoft Purview sensitivity labels](search-indexer-sensitivity-labels.md).


### Enforce document-level permissions at query time

With native [token-based querying](https://aka.ms/azs-query-preserving-permissions), Azure AI Search validates a user's [Microsoft Entra token](/Entra/identity/devices/concept-tokens-microsoft-Entra-id), trimming result sets to include only documents the user is authorized to access. 

You can achieve automatic trimming by attaching the user's Microsoft Entra token to your query request. For more information, see [Query-time ACL and RBAC enforcement in Azure AI Search](search-query-access-control-rbac-enforcement.md).

## Benefits of document-level access control  
  
Document-level access control is critical for safeguarding sensitive information in AI-driven applications. It helps organizations build systems that align with their access policies, reducing the risk of exposing unauthorized or confidential data. By integrating access rules directly into the search pipeline, AI systems can provide responses grounded in secure and authorized information.  

By offloading permission enforcement to Azure AI Search, developers can focus on building high-quality retrieval and ranking systems. This approach helps reducing the need to handle nested groups, write custom filters, or manually trim search results.  

Document-level permissions in Azure AI Search provide a structured framework for enforcing access controls that align with organizational policies. By using Microsoft Entra-based ACLs and RBAC roles, organizations can create systems that support robust compliance and promote trust among users. These built-in capabilities reduce the need for custom coding, offering a standardized approach to document-level security.  

## Tutorials and samples
  
Take a closer look at document-level access control in Azure AI Search with more articles and samples.

- [Tutorial: Index ADLS Gen2 permissions metadata using an indexer](tutorial-adls-gen2-indexer-acls.md)
- [azure-search-rest-samples/acl](https://github.com/Azure-Samples/azure-search-rest-samples/tree/main/acl)
- [azure-search-python-samples/Quickstart-Document-Permissions-Push-API](https://github.com/Azure-Samples/azure-search-python-samples/blob/main/Quickstart-Document-Permissions-Push-API)
- [azure-search-python-samples/Quickstart-Document-Permissions-Pull-API](https://github.com/Azure-Samples/azure-search-python-samples/blob/main/Quickstart-Document-Permissions-Pull-API)
- [Demo app: Ingesting and honoring sensitivity labels](https://aka.ms/Ignite25/aisearch-purview-sensitivity-labels-repo)

## Related content

- [How to index document-level permissions using push API](search-index-access-control-lists-and-rbac-push-api.md)
- [How to index document-level permissions using the ADLS Gen2 indexer](search-indexer-access-control-lists-and-role-based-access.md)
- [How to index document-level permissions using the SharePoint in Microsoft 365 indexer](https://aka.ms/azs-sharepoint-indexer-acls)
- [How to index sensitivity labels using indexers](search-indexer-sensitivity-labels.md)
- [How to query using Microsoft Entra token-based permissions](https://aka.ms/azs-query-preserving-permissions)
