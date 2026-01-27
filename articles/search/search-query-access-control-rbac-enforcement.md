---  
title: Query-Time ACL and RBAC Enforcement
titleSuffix: Azure AI Search  
description: Learn how query-time ACL and RBAC enforcement ensures secure document retrieval in Azure AI Search for indexes containing permission filters from data sources such as Azure Data Lake Storage (ADLS) Gen2 and SharePoint in Microsoft 365.  
ms.service: azure-ai-search  
ms.topic: concept-article  
ms.date: 01/15/2026  
author: mattgotteiner  
ms.author: magottei 
---  

# Query-time ACL and RBAC enforcement in Azure AI Search

Query-time access control ensures that users only retrieve search results they're authorized to access, based on their identity, group memberships, roles, or attributes. This functionality is essential for secure enterprise search and compliance-driven workflows.

Authorized access depends on permission metadata that's ingested during indexing. For indexer data sources that have built-in access models, such as Azure Data Lake Storage (ADLS) Gen2 and SharePoint in Microsoft 365, an indexer can pull in the permission metadata for each document automatically. For other data sources, you must assemble the document payload yourself, and the payload must include both content and the associated permission metadata. You then use the [push APIs](search-index-access-control-lists-and-rbac-push-api.md) to load the index.

This article explains how to set up queries that use permission metadata to filter results.

## Prerequisites

- Permission metadata must be in `filterable` string fields. You won't use the filter in your queries, but the search engine builds a filter internally to exclude unauthorized content.

- Permission metadata must consist of either POSIX-style permissions that identify the level of access and the group or user ID, or the resource ID of the container in ADLS Gen2 if you're using RBAC scope.

- Depending on the data source:
  + For ADLS Gen2 data sources, you must have configured Access Control Lists (ACLs) and/or Azure role-based access control (RBAC) roles at the container level.
  + For Azure Blob data sources, you must have role assignments on the container. You can use a [built-in indexer](search-indexer-access-control-lists-and-role-based-access.md), a [knowledge source](agentic-knowledge-source-how-to-blob.md), or [Push APIs](search-index-access-control-lists-and-rbac-push-api.md) to index permission metadata in your index.
  + For SharePoint data sources, you must have configured Access Control Lists (ACLs). You can use a [built-in SharePoint indexer](search-how-to-index-sharepoint-online.md) and configure it with [ACL ingestion capabilities](search-indexer-sharepoint-access-control-lists.md). 

- Use the [latest preview REST API](/rest/api/searchservice/operation-groups?view=rest-searchservice-2025-11-01-preview&preserve-view=true) or a preview package of an Azure SDK to query the index or knowledge source. This API version supports internal queries that filter out unauthorized results.

## Limitations

- If ACL evaluation fails (for example, the Graph API is unavailable), the service returns **5xx** and does **not** return a partially filtered result set.

- Document visibility requires both:
  - the calling application’s RBAC role (Authorization header)  
  - the user identity carried by **x-ms-query-source-authorization**
 
- Initial ACL-based queries may experience higher latency compared to subsequent requests, due to caching and permission resolution overhead.

## ACL entry limits per data source

Access Control List (ACL) entry limits define how many distinct permission records can be associated with a file, folder, or item within a connected data source. Each entry represents a single user or group identity and the access rights granted to that identity (for example, Read, Write, or Execute).

The maximum number of ACL entries supported by Azure AI Search functionality varies depending on the data source type:

Azure Data Lake Storage Gen2 (ADLS Gen2):
Each file or directory can have up to [32 ACL entries permissions](/azure/storage/blobs/data-lake-storage-access-control). In this context, an entry means a single principal (user or group) with a specific permission set. Example: assigning "Everyone" read access and "Azure users" execute access would count as two ACL entries.

SharePoint in Microsoft 365:
SharePoint data source in search supports up to 1,000 permission entries per file. Each entry represents a unique user or group assignment in the item’s permission list. This is distinct from the overall [unique permission scopes limits](/office365/servicedescriptions/sharepoint-online-service-description/sharepoint-online-limits#unique-security-scopes-per-list-or-library) per list or library, which governs how many items can have unique permissions.

These limits determine how granularly Azure AI Search can honor item-level permissions when indexing or filtering search results. If an item exceeds these ACL entry limits, permissions beyond the limit may not be enforced at query time.


## How query-time enforcement works

This section lists the order of operations for ACL enforcement at query time. Operations vary depending on whether you use Azure RBAC scope or Microsoft Entra ID group or user IDs.

### 1. User permissions input

The end-user application includes a query access token as part of the search query request, and that access token is typically the identity of the user. The following table lists the source of the user permissions supported by Azure AI Search for ACL enforcement:

| Permission type | Source |
| - | - |
| userIds | `oid` from `x-ms-query-source-authorization` token |
| groupIds | Group membership fetched using the [Microsoft Graph](/graph/api/resources/groups-overview) API |
| rbacScope | Permissions the user from `x-ms-query-source-authorization` has on a storage container |

### 2. Security filter construction

Internally, Azure AI Search dynamically constructs security filters based on the user permissions provided. These security filters are automatically appended to any filters that might come in with the query if the index has the permission filter option enabled.

For Azure RBAC, permissions are lists of resource ID strings. There must be an Azure role assignment (Storage Blob Data Reader) on the data source that grants access to the security principal token in the authorization header. The filter excludes documents if there's no role assignment for the principal behind the access token on the request.

### 3. Results filtering
  
The security filter efficiently matches the userIds, groupIds, and rbacScope from the request against each list of ACLs in every document in the search index to limit the results returned to ones the user has access to. It's important to note that each filter is applied independently and a document is considered authorized if any filter succeeds. For example, if a user has access to a document through userIds but not through groupIds, the document is still considered valid and returned to the user.

## Query example

Here's an example of a query request from [sample code](https://github.com/Azure-Samples/azure-search-rest-samples/tree/main/acl). The query token is passed in the request header. The query token is the personal access token of a user or a group identity behind the request.

```http
POST  {{endpoint}}/indexes/stateparks/docs/search?api-version=2025-11-01-preview
Authorization: Bearer {{query-token}}
x-ms-query-source-authorization: {{query-token}}
Content-Type: application/json

{
    "search": "*",
    "select": "name,description,location,GroupIds",
    "orderby": "name asc"
}
```

> [!NOTE]
> If the query token is omitted, only public documents accessible to everyone are returned in the query request.

## Elevated permissions for investigating incorrect results

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

Debugging queries that include permission metadata can be problematic because search results are specific to each user. As a developer or administrator, you might need elevated permissions to return results regardless of the permission metadata so that you can investigate problems with queries returning unauthorized content.

To investigate, you must be able to: 

- View the set of documents that the end user is able to view based on that user's permissions.

- View all documents in the index to investigate why some might not be visible to the end user.

You can accomplish these tasks by adding a custom header, `x-ms-enable-elevated-read: true`, to a query.

### Permissions for elevated-read requests

You must have [Search Index Data Contributor](search-security-rbac.md#built-in-roles-used-in-search) permissions or a [custom role](search-security-rbac.md#create-a-custom-role) that includes the Elevate Read permission.

Queries are a data plane operation, so the custom role can only consist of atomic data plane permissions. For a custom role, add the `Microsoft.Search/searchServices/indexes/contentSecurity/elevatedOperations/read` permission.

### Add an elevated-read header to a query

After you set up permissions, you can run the query. The following example is a query request against a search index.

```http
POST {endpoint}/indexes('{indexName}')/search.post.search?api-version=2025-11-01-preview
Authorization: Bearer {AUTH_TOKEN} 
x-ms-query-source-authorization: Bearer {TOKEN} 
x-ms-enable-elevated-read: true

{
    "search": "prototype tests",
    "select": "filename, author, date",
    "count": true
}
```

> [!IMPORTANT]
> The `x-ms-enable-elevated-read` header only works on Search POST actions. You can't perform an elevated read query on a [knowledge base retrieve](/rest/api/searchservice/knowledge-retrieval/retrieve?view=rest-searchservice-2025-11-01-preview&preserve-view=true) action.

### Important ACL functionality behavior change in specific preview API versions

Before REST API version `2025-11-01-preview`, earlier preview versions `2025-05-01-preview` and `2025-08-01-preview` returned all documents when using a service API key or authorized Entra roles, even if no user token was provided. Applications that didn’t validate the presence of a user token could inadvertently expose results to end users if not implemented correctly or following best practices.

Starting in November 2025, this behavior changed:

- ACL permission filters now apply even when using only service API keys or Entra authentication across all versions that support ACL.
- If the user token is omitted, ACL-protected content isn't returned.
- To view all documents for troubleshooting, you must explicitly include the elevated-read header when using REST API version `2025-11-01-preview`.

This update helps keep content protected when applications don’t enforce best practices for token validation.

## See also

- [Tutorial: Index ADLS Gen2 permission metadata](tutorial-adls-gen2-indexer-acls.md) 

- [Indexing ACLs and RBAC using the push API in Azure AI Search](search-index-access-control-lists-and-rbac-push-api.md)

- [Use an ADLS Gen2 indexer to ingest permission metadata and filter search results based on user access rights](search-indexer-access-control-lists-and-role-based-access.md) 

- [Use a Blob indexer to ingest RBAC scopes metadata](search-blob-indexer-role-based-access.md)

- [Use a SharePoint indexer to ingest permission metadata and filter search results based on user access rights](search-indexer-sharepoint-access-control-lists.md)
