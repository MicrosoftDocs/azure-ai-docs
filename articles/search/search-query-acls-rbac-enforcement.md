---  
title: Query-Time ACL and RBAC Enforcement in ADLS Gen2 Indexes
titleSuffix: Azure AI Search  
description: Learn how query-time ACL and RBAC enforcement ensures secure document retrieval in Azure AI Search for indexes containing permission filters from Azure Data Lake Storage (ADLS) Gen2 data sources.  
ms.service: azure-ai-search  
ms.topic: conceptual  
ms.date: 04/23/2025  
author: mattgotteiner  
ms.author: magottei 
---  

# Query-Time ACL and RBAC Enforcement in Azure AI Search  

Query-time access control ensures that users only retrieve search results they are authorized to access, based on their identity, group memberships, roles, or attributes. This functionality is essential for secure enterprise search and compliance-driven workflows.  

## Requirements 
- Azure Data Lake Storage (ADLS) Gen2 data source configured ACLs and/or RBAC roles at container level, or permissions manually pushed into the index.
- Configure document ACL and RBAC role functionality as required using Azure AI Search [built-in indexers](search-indexer-acls-rbac.md) or when indexing the documents [using the API directly](search-indexing-acls-rbac-push-api.md).


## How query-time enforcement works

This section lists the order of operations for ACL enforcement at query time.

### 1. User Permissions Input  
The end-user application sends user permission as part of the search query request. The following table lists the source of the user permissions Azure AI Search uses for ACL enforcement:

| Permission Type | Source |
| - | - |
| userIds | `oid` from `x-ms-query-source-authorization` token |
| groupIds | Group membership fetched using the [Microsoft Graph](/graph/api/resources/groups-overview) API |
| rbacScope | Permissions the user from `x-ms-query-source-authorization` has on a storage container |

### 2. Security Filter Construction  
Azure AI Search dynamically constructs security filters based on the user permissions provided. These security filters are automatically appended to any filters that might come in with the query if the index has the permission filter option enabled.

### 3. Results Filtering  
The security filter efficiently matches the userIds, groupIds and rbacScope from the user against each list of ACLs in every document in the search index to limit the results returned to ones the user has access to. It's important to note that each filter is applied indepdendently and a document is considered authorized if any filter succeeds. For example, if a user has access to a document through userIds but not through groupIds, the document is still considered valid and returned to the user.

---  

## Limitations
- If ACL evaluation fails (for example, Graph API is unavailable), the service returns **5xx** and does **not** return a partially filtered result set.
- Document visibility requires both:  
  1) the calling application’s RBAC role (Authorization header), and  
  2) the user identity carried by **x-ms-query-source-authorization**.

## Next steps
* [How to Index Permission Information](tutorial-adls-gen2-indexer-acls.md) provides a detailed walkthrough of how to set up an index with ACLs using Azure Search indexers.
* [Indexing ACLs and RBAC using Push API in Azure AI Search](search-indexing-acls-rbac-push-api.md) provides a walkthrough of how to setup an index with ACLs using the push API.
