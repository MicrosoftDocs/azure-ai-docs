---
title: Document-Level Access Control
description: Conceptual overview of document-level permissions in Azure AI Search.
ms.date: 05/17/2026
ms.reviewer: gimondra
ms.service: azure-ai-search
ms.topic: concept-article
ai-usage: ai-assisted
ms.custom:
  - build-2025
---

# Document-level access control in Azure AI Search

Azure AI Search supports document-level access control, enabling organizations to enforce fine-grained permissions at the document level, from data ingestion through query execution. This capability is essential for building secure agentic AI systems that ground on enterprise data, retrieval-augmented generation (RAG) applications, and enterprise search solutions that require authorization checks at the document level.

## Approaches for document-level access control

Azure AI Search provides four primary approaches to enforce document-level permissions, each suited to different data sources and identity models.

| Approach | Description |
|----------|-------------|
| Security filters | String comparison. Your application passes in a user or group identity as a string, which populates a filter on a query, excluding any documents that don't match on the string. <br><br>Security filters are a technique for achieving document-level access control. This approach isn't bound to an API so you can use any version or package. |
| POSIX-like ACL / RBAC scopes (preview) | The Microsoft Entra security principal behind the query token is compared to the permission metadata of documents returned in search results, excluding any documents that don't match on permissions. Access control lists (ACL) permissions apply to Azure Data Lake Storage (ADLS) Gen2 directories and files. Role-based access control (RBAC) scopes apply to ADLS Gen2 content and to Azure blobs. <br><br>Built-in support for identity-based access at the document level is in preview, available in REST APIs and preview Azure SDK packages that provide the feature. Be sure to check the [SDK version support details](#retrieve-acl-permissions-metadata-during-data-ingestion-process-preview) for evidence of feature support.|
| Microsoft Purview sensitivity labels (preview) | Indexer extracts sensitivity labels defined in Microsoft Purview from supported data sources (Azure Blob Storage, ADLS Gen2, SharePoint in Microsoft 365, OneLake). These labels are stored as metadata and evaluated at query time to enforce user access based on Microsoft Entra tokens and Purview policy assignments. This approach aligns Azure AI Search authorization with your enterprise's Microsoft Information Protection model.|
| SharePoint in Microsoft 365 ACLs (preview) | When configured, Azure AI Search indexers extract SharePoint document, list item, and ASPX site page permissions directly from Microsoft 365 ACLs. Starting in the 2026-05-01-preview REST API, ACL changes for items with unique permissions are also picked up incrementally on each successful indexer run. Access checks use Microsoft Entra user and group memberships, with SharePoint site groups also supported in the same preview (subject to extra configuration). |

## Choosing an approach

Use the following criteria to identify the approach that best fits your data source, identity model, and compliance requirements.

| Scenario | Recommended approach | Why |
|----------|----------------------|-----|
| Custom identity system, non-Microsoft security framework, or any push-model index | Security filters | API-agnostic, generally available, and based on simple string matching. |
| Content in ADLS Gen2 or Azure Blob Storage with existing ACL or RBAC assignments | POSIX-like ACL / RBAC scopes | Native Microsoft Entra integration; query-time enforcement uses permission metadata written to the index by the documented synchronization mechanism. |
| Enterprise content already governed by Microsoft Purview information protection policies | Microsoft Purview sensitivity labels | Reuses centralized classification and policy assignments across Azure AI Search. |
| Content sourced from SharePoint in Microsoft 365 (libraries, lists, ASPX site pages) | SharePoint in Microsoft 365 ACLs | Honors native SharePoint permissions, including SharePoint site groups. |

For a side-by-side feature comparison (supported principals, item types, sync behavior, and API surface), see the linked pattern sections later in this article and [How to index SharePoint in Microsoft 365 document-level permissions (preview)](search-indexer-sharepoint-access-control-lists.md).

## Pattern for security trimming using filters

For scenarios where native ACL/RBAC scopes integration isn't viable, security string filters are recommended for trimming results based on exclusion criteria. The pattern includes the following components:

- To store user or group identities, create a string field in the index.
- Load the index using source documents that include associated ACLs.
- Include a filter expression in your query logic for matching on the string.
- At query time, get the identity of the caller.
- Pass in the identity of the caller as the filter string.
- Results are trimmed to exclude any matches that fail to include the user or group identity string.

You can use push or pull model APIs. Because this approach is API agnostic, you just need to confirm that the index and query have valid strings (identities) for the filtration step.

This approach is useful for systems with custom access models or non-Microsoft security frameworks. For more information about this approach, see [Security filters for trimming results in Azure AI Search](search-security-trimming-for-azure-search.md).

## Pattern for native support for POSIX-like ACL and RBAC scope permissions (preview)

Native support is based on Microsoft Entra users and groups affiliated with documents that you want to index and query. 

Azure Data Lake Storage (ADLS) Gen2 containers support ACLs on the container and on files. For ADLS Gen2, RBAC scope preservation at document level is natively supported when you use an [ADLS Gen2 indexer](search-how-to-index-azure-data-lake-storage.md) or a [Blob knowledge source (supports ADLS Gen2)](agentic-knowledge-source-how-to-blob.md) and a preview API to ingest content. For Azure blobs using the [Azure blob indexer](search-blob-indexer-role-based-access.md) or knowledge source, RBAC scope preservation is at the container level.

For ACL-secured content, we recommend group access over individual user access for ease of management. The pattern includes the following components:

- Start with documents or files that have ACL assignments.
- [Enable permission filters](/rest/api/searchservice/indexes/create-or-update?view=rest-searchservice-2026-05-01-preview&preserve-view=true#searchindexpermissionfilteroption) in the index.
- [Add a permission filter](/rest/api/searchservice/indexes/create-or-update?view=rest-searchservice-2026-05-01-preview&preserve-view=true#permissionfilter) to a string field in an index.
- Load the index with source documents having associated ACLs.
- Query the index, adding [`x-ms-query-source-authorization`](/rest/api/searchservice/documents/search-post?view=rest-searchservice-2026-05-01-preview&preserve-view=true#request-headers) in the request header.

Your client app receives read permissions to the index through **Search Index Data Reader** or **Search Index Data Contributor** role. Access at query time is determined by user or group permission metadata in the indexed content. Queries that include a permission filter pass a user or group token as `x-ms-query-source-authorization` in the request header. When you use permission filters at query time, Azure AI Search checks for two things:

- First, it checks for **Search Index Data Reader** permission that allows your client application to access the index.

- Second, given the extra token on the request, it checks for user or group permissions on documents that are returned in search results, excluding any that don't match.

To get permission metadata into the index, you can use the push model API, pushing any JSON documents to the search index, where the payload includes a string field providing POSIX-like ACLs for each document. The important difference between this approach and security trimming is that the permission filter metadata in the index and query is recognized as Microsoft Entra ID authentication, whereas the security trimming workaround is simple string comparison. Also, you can use the Graph SDK to retrieve the identities.

You can also use the pull model (indexer) APIs if the data source is [Azure Data Lake Storage (ADLS) Gen2](/azure/storage/blobs/data-lake-storage-introduction) and your code calls a preview API for indexing.

### Retrieve ACL permissions metadata during data ingestion process (preview)

How you retrieve ACL permissions varies depending on whether you're pushing a documents payload or using the ADLS Gen2 indexer.

Start with a preview API that provides the feature:

- [2026-05-01-preview REST API](/rest/api/searchservice/documents/?view=rest-searchservice-2026-05-01-preview&preserve-view=true)
- [Azure SDK for Python prerelease package](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/search/azure-search-documents/CHANGELOG.md). Check the changelog for the latest preview version that supports ACL and RBAC scope ingestion.
- [Azure SDK for .NET prerelease package](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/search/Azure.Search.Documents/CHANGELOG.md). Check the changelog for the latest preview version that supports ACL and RBAC scope ingestion.
- [Azure SDK for Java prerelease package](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/search/azure-search-documents/CHANGELOG.md). Check the changelog for the latest preview version that supports ACL and RBAC scope ingestion.

For the [push model approach](search-index-access-control-lists-and-rbac-push-api.md):

1. Confirm that your index schema is created with a preview or prerelease SDK, and that the schema has permission filters.
1. Consider using the Microsoft Graph SDK to get group or user identities.
1. Use the [Index Documents](/rest/api/searchservice/documents/?view=rest-searchservice-2026-05-01-preview&preserve-view=true#indexdocumentsresult) or equivalent Azure SDK API to push documents and their associated permission metadata into the search index. 

For the [pull model ADLS Gen2 indexer approach](search-indexer-access-control-lists-and-role-based-access.md) or [Blob (ADLS Gen2) knowledge source](agentic-knowledge-source-how-to-blob.md):

1. Verify that files in the directory are secured using the [ADLS Gen2 access control model](/azure/storage/blobs/data-lake-storage-access-control-model).
1. Use the [Create Indexer REST API](/rest/api/searchservice/indexers/create?view=rest-searchservice-2026-05-01-preview&preserve-view=true) or [Create Knowledge Source REST API](/rest/api/searchservice/knowledge-sources/create?view=rest-searchservice-2026-05-01-preview&preserve-view=true) or equivalent Azure SDK API to create the indexer, index, and data source.

## Pattern for SharePoint in Microsoft 365 basic ACL permissions ingestion (preview)

For SharePoint in Microsoft 365 content, Azure AI Search can apply document-level permissions based on SharePoint ACLs. With this integration, only users or groups that have access to the source item in SharePoint can retrieve it from search results. The match takes effect after the ACL metadata is written to the index by the next successful [scheduled indexer](search-howto-schedule-indexers.md) run that follows the source change. ACL ingestion applies to documents in libraries, items in [SharePoint lists](search-how-to-index-sharepoint-online.md#index-sharepoint-lists), and [ASPX site pages](search-how-to-index-sharepoint-online.md#index-aspx-site-pages).

SharePoint ACL support is available in preview through the SharePoint indexer using the [2026-05-01-preview REST API](/rest/api/searchservice/data-sources/create?view=rest-searchservice-2026-05-01-preview&preserve-view=true) or supported SDK.

The pattern includes the following components:

- Use the SharePoint in Microsoft 365 indexer with application permissions to read SharePoint site content and full permissions to read ACLs. Follow the [SharePoint indexer ACL configuration steps](search-indexer-sharepoint-access-control-lists.md#configure-your-search-service-for-acl-ingestion-and-honoring-at-query-time) for enablement and limitations.
- During initial indexing, SharePoint ACL entries (users and groups) are stored as permission metadata in the search index.
- Starting in the 2026-05-01-preview REST API, ACL changes on items with unique permissions are detected and refreshed on each successful indexer run. Changes on parent scopes (site, library, list, or folder) that are inherited by child items still require an explicit refresh. For details, see [Synchronize permissions between indexed and source content](search-indexer-sharepoint-access-control-lists.md#synchronize-permissions-between-indexed-and-source-content).
- At query time, Azure AI Search checks the Microsoft Entra principal in the query token against SharePoint ACL metadata stored in the index. It excludes any items the caller isn't authorized to access.

During preview, the following principal types are supported in SharePoint ACLs:

- Microsoft Entra user accounts
- Microsoft Entra security groups
- Microsoft 365 groups
- Mail-enabled security groups
- SharePoint site groups (preview, starting in the 2026-05-01-preview REST API). Requires extra index configuration. For details, see [Configure SharePoint groups support](search-indexer-sharepoint-access-control-lists.md#configure-sharepoint-groups-support).

[SharePoint Information Management policies](/sharepoint/intro-to-info-mgmt-policies) that gate user access aren't evaluated, ingested, or honored at query time.

For configuration details and full limitations, see [How to index SharePoint in Microsoft 365 document-level permissions (preview)](search-indexer-sharepoint-access-control-lists.md).


## Pattern for Microsoft Purview sensitivity labels (preview)

Azure AI Search can ingest and enforce **Microsoft Purview sensitivity labels** for document-level access control, extending information protection policies from Microsoft Purview into your search and retrieval applications.

When label ingestion is enabled, Azure AI Search extracts sensitivity metadata from supported data sources. These include: Azure Blob Storage, Azure Data Lake Storage Gen2 (ADLS Gen2), SharePoint in Microsoft 365, and Microsoft OneLake. The extracted labels are stored in the index alongside document content.

At query time, Azure AI Search checks each document's sensitivity label, the user's Microsoft Entra token, and the organization's Purview policies to determine access. Documents are returned only if the user's identity and label-based permissions allow access under the configured Purview policies.

The pattern includes the following components:

- Configure your [index](/rest/api/searchservice/indexes/create?view=rest-searchservice-2026-05-01-preview&preserve-view=true), [data source](/rest/api/searchservice/data-sources/create?view=rest-searchservice-2026-05-01-preview&preserve-view=true), and [indexer](/rest/api/searchservice/indexers/create?view=rest-searchservice-2026-05-01-preview&preserve-view=true) (for scheduling purposes) using the 2026-05-01-preview REST API or a corresponding SDK that supports Purview label ingestion.
- Enable a [system-assigned managed identity](search-how-to-managed-identities.md) to your search service. Then ask your tenant global administrator or privileged role administrator to [grant the required access](search-indexer-sensitivity-labels.md), so the search service can securely access Microsoft Purview and extract label metadata.
- Apply sensitivity labels to documents before indexing so they can be recognized and preserved during ingestion.
- At query time, attach a valid Microsoft Entra token via the header `x-ms-query-source-authorization` to each query request. Azure AI Search evaluates the token and the associated label metadata to enforce label-based access control.

Purview sensitivity label enforcement is limited to single-tenant scenarios, requires RBAC authentication, and during preview is supported only through REST API or SDK. Autocomplete and Suggest APIs aren't available for Purview-enabled indexes at this time.

For more information, see [Use Azure AI Search indexers to ingest Microsoft Purview sensitivity labels](search-indexer-sensitivity-labels.md).

## Enforce document-level permissions at query time

Token-based query enforcement is a cross-cutting capability that applies to the POSIX-like ACL / RBAC scopes, Microsoft Purview sensitivity labels, and SharePoint in Microsoft 365 ACLs patterns. With [native token-based querying](search-query-access-control-rbac-enforcement.md), Azure AI Search validates the caller's [Microsoft Entra token](/entra/identity-platform/access-tokens) on each request and trims result sets to only the documents the caller is authorized to read according to the document ACLs, as long as the document ACL metadata has been synchronized to the index.

When you attach the user's token to a query request through the `x-ms-query-source-authorization` header, Azure AI Search:

1. Extracts the user, group, and scope claims from the token.
1. Compares those claims to the permission metadata stored alongside indexed documents (ACL entries, RBAC scopes, Purview label assignments, or SharePoint ACLs).
1. Returns only documents whose synchronized permission metadata grants the caller access.

Query-time enforcement evaluates the caller's Microsoft Entra claims against the permission metadata that's already stored in the index. Permission changes in the source system (Microsoft Entra group membership, ADLS Gen2 ACLs, Purview label assignments, or SharePoint ACLs) are only reflected in search results after that metadata is synchronized to the index through the source-specific mechanism, for example, a subsequent indexer run, a push-API update, or a Purview-driven refresh. For SharePoint, ACL changes on items with unique permissions are picked up incrementally on each successful indexer run starting in the 2026-05-01-preview REST API, while changes inherited from parent scopes (site, library, list, or folder) require an explicit refresh. For details, see [Synchronize permissions between indexed and source content](search-indexer-sharepoint-access-control-lists.md#synchronize-permissions-between-indexed-and-source-content).

For end-to-end query implementation steps, see [Query-time ACL and RBAC enforcement in Azure AI Search](search-query-access-control-rbac-enforcement.md).

## Benefits of document-level access control

Native document-level access control in Azure AI Search delivers concrete advantages over application-side filtering:

- **Eliminates custom permission code.** You don't need to implement nested group resolution, multi-level ACL traversal, or post-query trimming in your application. Azure AI Search handles the comparison and filtering during query execution.
- **Aligns with existing compliance controls.** Reusing Microsoft Entra, Microsoft Purview, and SharePoint permissions metadata helps keep search results aligned with the source identity system. Review the permission synchronization model for each source to understand its limitations.
- **Honors source permissions after each ACL synchronization.** For token-based approaches (ACL, RBAC scopes, Purview labels, SharePoint ACLs), query-time enforcement uses the permission metadata that the documented source-specific synchronization mechanism (indexer run, push-API update, or Purview refresh) has already written to the index.
- **Improves performance versus post-query trimming.** Filtering inside the search pipeline is faster than loading larger result sets into your application and trimming there, especially at high query volumes.
- **Reuses your existing identity infrastructure.** Microsoft Entra and SharePoint identities remain the source of truth for access decisions, which reduces identity duplication and the operational overhead of maintaining a parallel permission store.

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
- [How to index document-level permissions using the SharePoint in Microsoft 365 indexer](search-indexer-sharepoint-access-control-lists.md)
- [How to index sensitivity labels using indexers](search-indexer-sensitivity-labels.md)
- [How to query using Microsoft Entra token-based permissions](search-query-access-control-rbac-enforcement.md)
