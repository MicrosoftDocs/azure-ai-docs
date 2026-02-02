---  
title: Query-Time ACL and RBAC Enforcement in ADLS Gen2 Indexes
titleSuffix: Azure AI Search  
description: Learn how query-time ACL and RBAC enforcement ensures secure document retrieval in Azure AI Search for indexes containing permission filters from Azure Data Lake Storage (ADLS) Gen2 data sources.  
ms.service: azure-ai-search  
ms.topic: conceptual  
ms.date: 08/27/2025  
author: mattgotteiner  
ms.author: magottei 
---  

# Query-Time ACL and RBAC enforcement in Azure AI Search  

Query-time access control ensures that users only retrieve search results they're authorized to access, based on their identity, group memberships, roles, or attributes. This functionality is essential for secure enterprise search and compliance-driven workflows. 

Azure Data Lake Storage (ADLS) Gen2 provides an access model that makes fine-grained access control easier to implement, but you can use other data sources, providing you [use the push APIs](search-index-access-control-lists-and-rbac-push-api.md) and you send documents that include permission metadata alongside other indexable fields.

This article explains how to set up queries that use permission metadata to filter results.

## Prerequisites

- Permission metadata must be in `filterable` string fields. You won't use the filter in your queries, but the search engine builds a filter internally to exclude unauthorized content.

- Permission metadata must consist of either POSIX-style permissions that identify the level of access and the group or user ID, or the resource ID of the container in ADLS Gen2 if you're using RBAC scope.

- For ADLS Gen2 data sources, you must have configured Access Control Lists (ACLs) and/or Azure role-based access control (RBAC) roles at the container level. For blob data sources, your have role assignments on the container. You can use a [built-in indexer](search-indexer-access-control-lists-and-role-based-access.md) or [Push APIs](search-index-access-control-lists-and-rbac-push-api.md) to index permission metadata in your index.

- The latest preview REST API (2025-08-01-preview) or a preview package of an Azure SDK to query the index. This API version supports internal queries that filter out unauthorized results.

## Limitations

- If ACL evaluation fails (for example, the Graph API is unavailable), the service returns **5xx** and does **not** return a partially filtered result set.

- Document visibility requires both:
  - the calling application’s RBAC role (Authorization header)  
  - the user identity carried by **x-ms-query-source-authorization**

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

Here's an example of a query request from [sample code](https://github.com/Azure-Samples/azure-search-rest-samples/tree/main/Quickstart-ACL). The query token is passed in the request header. The query token is the personal access token of a user or a group identity behind the request.

```http
POST  {{endpoint}}/indexes/stateparks/docs/search?api-version=2025-08-01-preview
Authorization: Bearer {{query-token}}
x-ms-query-source-authorization: {{query-token}}
Content-Type: application/json

{
    "search": "*",
    "select": "name,description,location,GroupIds",
    "orderby": "name asc"
}
```

## See also

- [Tutorial: Index ADLS Gen2 permission metadata](tutorial-adls-gen2-indexer-acls.md) 

- [Indexing ACLs and RBAC using the push API in Azure AI Search](search-index-access-control-lists-and-rbac-push-api.md)

- [Use an ADLS Gen2 indexer to ingest permission metadata and filter search results based on user access rights](search-indexer-access-control-lists-and-role-based-access.md) 

- [Use a Blob indexer to ingest RBAC scopes metadata](search-blob-indexer-role-based-access.md)