---  
title: Query-Time ACL and RBAC Enforcement in ADLS Gen2 Indexes
titleSuffix: Azure AI Search  
description: Learn how query-time ACL and RBAC enforcement ensures secure document retrieval in Azure AI Search for indexes containing permission filters from Azure Data Lake Storage (ADLS) Gen2 data sources.  
ms.service: azure-ai-search  
ms.topic: conceptual  
ms.date: 05/15/2025  
author: mattgotteiner  
ms.author: magottei 
---  

# Query-Time ACL and RBAC enforcement in Azure AI Search  

Query-time access control ensures that users only retrieve search results they're authorized to access, based on their identity, group memberships, roles, or attributes. This functionality is essential for secure enterprise search and compliance-driven workflows. 

Azure Data Lake Storage (ADLS) Gen2 provides an access model that makes fine-grained access control easier to implement, but you can use other data sources, providing you use the push APIs and you send documents that include permission metadata alongside other indexable fields.

## Requirements

- Permission metadata must be in `filterable` string fields. You won't use the filter in your queries, but the search engine builds a filter internally to exclude unauthorized content.

- Permission metadata must consist of either POSIX-style permissions that identify the level of access and the group or user ID, or the resource ID of the container in ADLS Gen2 if you're using RBAC scope.

- For ADLS Gen2 data sources, you must have configured Access Control Lists (ACLs) and/or Azure role-based access control (RBAC) roles at the container level. You can use a [built-in indexer](search-indexer-access-control-lists-and-role-based-access.md) or [Push APIs](search-index-access-control-lists-and-rbac-push-api.md) to index permission metadata in your index.

- Use the 2025-05-01-preview REST API or a prerelease package of an Azure SDK to query the index. This API version supports internal queries that filter out unauthorized results.

## How query-time enforcement works

This section lists the order of operations for ACL enforcement at query time. Operations vary depending on whether you use Azure RBAC scope or Microsoft Entra ID group or user IDs.

### 1. User permissions input  
The end-user application sends user permission as part of the search query request. The following table lists the source of the user permissions Azure AI Search uses for ACL enforcement:

| Permission type | Source |
| - | - |
| userIds | `oid` from `x-ms-query-source-authorization` token |
| groupIds | Group membership fetched using the [Microsoft Graph](/graph/api/resources/groups-overview) API |
| rbacScope | Permissions the user from `x-ms-query-source-authorization` has on a storage container |

### 2. Security filter construction
Azure AI Search dynamically constructs security filters based on the user permissions provided. These security filters are automatically appended to any filters that might come in with the query if the index has the permission filter option enabled.

For Azure RBAC, permissions are list of resource ID strings, and there must an Azure role assignment (Storage Blob Data Reader) on the data the source that grants access to the security principal token in the authorization header. The filter excludes documents if there's no role assignment for the principal behind the access token on the request.

### 3. Results filtering
  
The security filter efficiently matches the userIds, groupIds, and rbacScope from the user against each list of ACLs in every document in the search index to limit the results returned to ones the user has access to. It's important to note that each filter is applied independently and a document is considered authorized if any filter succeeds. For example, if a user has access to a document through userIds but not through groupIds, the document is still considered valid and returned to the user.

## Limitations

- If ACL evaluation fails (for example, Graph API is unavailable), the service returns **5xx** and does **not** return a partially filtered result set.
- Document visibility requires both:
  - the calling application’s RBAC role (Authorization header), and  
  - the user identity carried by **x-ms-query-source-authorization**.

## Query example

Here's an example of a query request. The query token is passed in the request header.

```http
POST  {{endpoint}}/indexes/stateparks/docs/search?api-version=2025-05-01-preview
Authorization: Bearer {{search-token}}
x-ms-query-source-authorization: {{search-token}}
Content-Type: application/json

{
    "search": "*",
    "select": "name,description,location,GroupIds",
    "orderby": "name asc"
}
```

## Related content

- [Tutorial: Index ADLS Gen2 permission metadata](tutorial-adls-gen2-indexer-acls.md) provides a detailed walkthrough of how to set up an index with ACLs using Azure Search indexers.

- [Indexing ACLs and RBAC using Push API in Azure AI Search](search-index-access-control-lists-and-rbac-push-api.md) provides a walkthrough of how to set up an index with ACLs using the push indexing approach with the REST APIs.
