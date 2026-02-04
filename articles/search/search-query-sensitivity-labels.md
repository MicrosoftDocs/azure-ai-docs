---
title: Query-Time Microsoft Purview Sensitivity Label Enforcement in Azure AI Search  
titleSuffix: Azure AI Search  
description: Learn how query-time enforcement of Microsoft Purview sensitivity labels ensures secure document retrieval in Azure AI Search for indexes containing label metadata.  
ms.service: azure-ai-search  
ms.topic: concept-article  
ms.date: 11/18/2025  
author: gmndrg  
ms.author: gimondra  
---

# Query-Time Microsoft Purview Sensitivity Label Enforcement in Azure AI Search  

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

At query time, Azure AI Search enforces sensitivity label policies defined in [Microsoft Purview](/purview/create-sensitivity-labels). These policies include evaluation of [READ usage rights](/purview/rights-management-usage-rights) tied to each document. As a result, users can only retrieve documents they are allowed to view.

This capability extends [document-level access control](search-document-level-access-overview.md) to align with your organization's [information protection and compliance requirements](/purview/create-sensitivity-labels) managed in Microsoft Purview.

When Purview sensitivity label indexing is enabled, Azure AI Search checks each document's label metadata during query time. It applies access filters based on Purview policies to return only results the requesting user is allowed to access.

This article explains how query-time sensitivity label enforcement works and how to issue secure search queries.


## Prerequisites

Before you can query a sensitivity-label-enabled index, the following conditions must be met:

- You must follow all steps for [Azure AI Search indexers to ingest Microsoft Purview sensitivity labels](search-indexer-sensitivity-labels.md).

- Both the Azure AI Search service and the user issuing the query must belong to the same Microsoft Entra tenant.

- The latest [preview API version 2025-11-01-preview](/rest/api/searchservice/operation-groups?view=rest-searchservice-2025-11-01-preview&preserve-view=true) or a compatible beta SDK must be used to query the index.  

- Queries must be authenticated using [Azure role-based access control (RBAC)](search-security-rbac.md), not API keys.  API key access is restricted to index schema retrieval only when Purview sensitivity labels functionality is enabled.


## Limitations

- [Microsoft Entra Guest users](/entra/external-id/b2b-quickstart-add-guest-users-portal) and cross-tenant queries aren't supported.  
- [Autocomplete](/rest/api/searchservice/documents/autocomplete-post) and [Suggest](/rest/api/searchservice/documents/suggest-post) APIs are unsupported for Purview-enabled indexes.  
- If label evaluation fails (for example, Purview APIs are temporarily unavailable), the service returns **5xx** and does **not** return a partial or unfiltered result set.  
- [ACL-based security filters](search-query-access-control-rbac-enforcement.md) aren't supported alongside sensitivity label functionality at this time. Don't enable both at the same time. Once combined usage is supported, it will be documented accordingly. 
- The system evaluates labels only as they existed at the time of the last indexer run; recent label changes may not be reflected until the next scheduled reindex.


## How query-time sensitivity label enforcement works

When you query an index that includes Microsoft Purview sensitivity labels, Azure AI Search checks the associated Purview policies before returning results. In this way, the query returns only documents that the user token is allowed to access.

### 1. User identity and application role input

At query time, Azure AI Search validates both:
- The calling application's RBAC role, provided in the `Authorization` header.  
- The user identity via token, provided in the `x-ms-query-source-authorization` header.  

Both are required to authorize label-based visibility.

| Input type | Description | Example source |
|-------------|--------------|----------------|
| Application role | Determines whether the calling app has permission to execute queries on the index. | `Authorization: Bearer <app-token>` |
| User identity | Determines which sensitivity labels the end user is allowed to access. | `x-ms-query-source-authorization: Bearer <user-token>` |



### 2. Sensitivity label evaluation

When a query request is received, Azure AI Search evaluates:
1. The sensitivityLabel field in each indexed document (extracted from Microsoft Purview during ingestion).  
2. The user's effective Purview permissions, as defined by Microsoft Entra ID and Purview label policy.  

If the user isn't authorized for a document's sensitivity label with extract permissions, that document is excluded from the query results.

> [!NOTE]
> Internally, the service builds dynamic access filters similar to RBAC enforcement.  
> These filters aren't user-visible and can't be modified in the query payload.


### 3. Secure result filtering

Azure AI Search applies the security filter after all user-defined filters and scoring steps.  
A document is included in the final result set only if:

- The calling application has a valid role assignment (via RBAC), and
- The user identity token represented by `x-ms-query-source-authorization` is valid and permitted to view content with the document's sensitivity label.

If either condition fails, the document is omitted from the results.


## Query example

Here's an example of a query request using Microsoft Purview sensitivity label enforcement.  
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
```

## Sensitivity label handling in Azure AI Search

When Azure AI Search indexes document content with sensitivity labels from sources like SharePoint, Azure Blob, and others, it stores both the content and the label metadata. The search query returns indexed content along with the GUID that identifies the sensitivity label applied to the document, only if the user has data READ access for that document. This GUID uniquely identifies the label but doesn't include human-readable properties such as the label name or associated permissions. 

Note that the GUID alone is insufficient for scenarios that include user interface because sensitivity labels often carry other policy controls enforced by [Microsoft Purview Information Protection](/purview/sensitivity-labels), such as: print permissions or screenshot and screen capture restrictions. Azure AI Search doesn't surface these capabilities.

To display label names and/or enforce UI-specific restrictions, your application must call the Microsoft Purview Information Protection endpoint to retrieve full label metadata and associated permissions.

You can use the GUID returned by Azure AI Search to resolve the label properties and call the [Purview Labels APIs](/graph/api/sensitivitylabel-get) to fetch the label name, description, and policy settings. This [end-to-end demo sample](https://aka.ms/Ignite25/aisearch-purview-sensitivity-labels-repo) includes code that shows how to call the endpoint from a user interface. It also demonstrates how to extract the label name and expose it as part of the citations used in your RAG applications or agents.
