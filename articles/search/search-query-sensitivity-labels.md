---
title: Query-Time Microsoft Purview Sensitivity Label Enforcement in Azure AI Search  
titleSuffix: Azure AI Search  
description: Learn how query-time enforcement of Microsoft Purview sensitivity labels ensures secure document retrieval in Azure AI Search for indexes containing label metadata.  
ms.service: azure-ai-search  
ms.topic: conceptual  
ms.date: 11/04/2025  
author: gmndrg  
ms.author: gimondra  
---

# Query-Time Microsoft Purview Sensitivity Label Enforcement in Azure AI Search  

Query-time sensitivity label enforcement ensures that users only retrieve documents they're authorized to view, based on Microsoft Purview sensitivity label policies associated with each document.  
This capability extends **document-level access control** to align with your organization’s **information protection and compliance requirements** managed in Microsoft Purview.

When Purview sensitivity label indexing is enabled, Azure AI Search evaluates label metadata at query time and applies access filters to return only results that the requesting user is permitted to access under Purview policy evaluation.

This article explains how query-time sensitivity label enforcement works and how to issue secure search queries.


## Prerequisites

Before you can query a sensitivity-label-enabled index, the following conditions must be met:

- Your search index must have **Purview sensitivity label support enabled** (`purviewEnabled: true`) at creation time and a unique field for sensitivity labels with "sensitivityLabel" value of true.

- You must follow all steps for [Azure AI Search indexers to ingest Microsoft Purview sensitivity labels](search-how-to-index-purview-sensitivity-labels.md).

- Both the **Azure AI Search service** and the **user issuing the query** must belong to the **same Microsoft Entra tenant**.

- The **latest preview API (2025-11-01-preview)** or a compatible SDK must be used to query the index.  This version introduces internal evaluation of Microsoft Purview label-based access filters.

- Queries must be authenticated using **Azure RBAC**, not API keys.  API key access is restricted to index schema retrieval only when Purview is enabled.


## Limitations

- **Guest accounts** and **cross-tenant queries** are not supported.  
- **Autocomplete** and **Suggest** APIs are unavailable for Purview-enabled indexes.  
- If label evaluation fails (for example, Purview APIs are temporarily unavailable), the service returns **5xx** and does **not** return a partial or unfiltered result set.  
- **Coexistence with ACL-based filters** is currently in preview and should be tested separately.  Do **not** enable or test Access Control Lists (ACLs) together with Purview sensitivity labels in the same index.  
  Once combined usage is supported, it will be documented accordingly. 
- The system evaluates labels only as they existed at the time of the last indexer run; recent label changes may not be reflected until the next scheduled reindex.


## How query-time sensitivity label enforcement works

When you query an index that includes Microsoft Purview sensitivity label metadata, Azure AI Search performs internal policy checks to ensure that only documents the user is authorized to access are returned.

### 1. User identity and application role input

At query time, Azure AI Search validates both:
- The **calling application’s RBAC role**, provided in the **`Authorization`** header.  
- The **user identity**, provided in the **`x-ms-query-source-authorization`** header.  

Both are required to authorize label-based visibility.

| Input type | Description | Example source |
|-------------|--------------|----------------|
| Application role | Determines whether the calling app has permission to execute queries on the index. | `Authorization: Bearer <app-token>` |
| User identity | Determines which sensitivity labels the end user is allowed to access. | `x-ms-query-source-authorization: Bearer <user-token>` |



### 2. Sensitivity label evaluation

When a query request is received, Azure AI Search evaluates:
1. The **sensitivityLabel** field in each indexed document (extracted from Microsoft Purview during ingestion).  
2. The **user’s effective Purview permissions**, as defined by Microsoft Entra ID and Purview label policy.  

If the user is **not authorized** for a document’s sensitivity label, that document is excluded from the query results.

> [!NOTE]
> Internally, the service builds dynamic access filters similar to RBAC enforcement.  
> These filters are not user-visible and cannot be modified in the query payload.


### 3. Secure result filtering

Azure AI Search applies the security filter after all user-defined filters and scoring steps.  
A document is included in the final result set only if:

- The **calling application** has a valid role assignment (via RBAC), **and**  
- The **user identity** represented by `x-ms-query-source-authorization` is permitted to view content with the document’s sensitivity label.

If either condition fails, the document is omitted from the results.


## Query example

Here’s an example of a query request using Microsoft Purview sensitivity label enforcement.  
The query token is passed in the request headers. Both headers must include valid bearer tokens representing the application and the end user.

```http
POST  {{endpoint}}/indexes/sensitivity-docs/docs/search?api-version=2025-11-01-preview
Authorization: Bearer {{app-query-token}}
x-ms-query-source-authorization: Bearer {{user-query-token}}
Content-Type: application/json

{
    "search": "*",
    "select": "title,summary,sensitivityLabel",
    "orderby": "title asc"
}

Note that the service returns the sensitivity label GUID. This is because there are other properties that must be provided by the application interface and call the respective MIP endpoint to get the label name and display, printing permissions, etc.
