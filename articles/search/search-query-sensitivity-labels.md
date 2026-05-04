---
title: Query-Time Microsoft Purview Sensitivity Label Enforcement
description: Learn how query-time enforcement of Microsoft Purview sensitivity labels ensures secure document retrieval in Azure AI Search for indexes containing label metadata.
ms.reviewer: gimondra
ms.service: azure-ai-search
ms.topic: concept-article
ms.date: 03/05/2026
ai-usage: ai-assisted
---

# Query-time enforcement of Microsoft Purview sensitivity labels in Azure AI Search  

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

At query time, Azure AI Search can enforce sensitivity label policies defined in [Microsoft Purview](/purview/create-sensitivity-labels). These policies include the evaluation of [`EXTRACT` usage rights](/purview/rights-management-usage-rights) associated with each document, ensuring users can only retrieve documents they're permitted to access.

This capability extends [document-level access control](search-document-level-access-overview.md) to align with your organization's [information protection and compliance requirements](/purview/create-sensitivity-labels) managed in Microsoft Purview.

When Purview sensitivity label indexing is enabled, Azure AI Search checks each document's label metadata during query time. It applies access filters based on Purview policies to return only results the requesting user is allowed to access.

This article explains how query-time sensitivity label enforcement works and how to issue secure search queries.

## Prerequisites

- Complete all steps in [Use Azure AI Search indexers to ingest Microsoft Purview sensitivity labels](search-indexer-sensitivity-labels.md).

- Both the Azure AI Search service and the user issuing the query must be in the same Microsoft Entra tenant.

- REST API version 2025-11-01-preview or an equivalent preview SDK package to query the index.

- Authenticate queries using [Azure role-based access control](search-security-rbac.md) (RBAC), not API keys. When Purview sensitivity labels are enabled, API key access is restricted to index schema retrieval.

## Limitations

- [Guest accounts](/entra/external-id/b2b-quickstart-add-guest-users-portal) and cross-tenant queries aren't supported.

- [Autocomplete](/rest/api/searchservice/documents/autocomplete-post) and [Suggest](/rest/api/searchservice/documents/suggest-post) APIs aren't supported for Purview-enabled indexes.

- If label evaluation fails (for example, Purview APIs are temporarily unavailable), the service returns **5xx** and doesn't return a partial or unfiltered result set.

- The system evaluates labels only as they existed at the time of the last indexer run. Recent label changes might not be reflected until the next scheduled reindex.

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
| User identity | Determines which sensitivity labels the end user is allowed to access. | `x-ms-query-source-authorization: <user-token>` |



### 2. Sensitivity label evaluation

When a query request is received, Azure AI Search evaluates:
1. The sensitivityLabel field in each indexed document (extracted from Microsoft Purview during ingestion).  
2. The user's effective Purview permissions, as defined by Microsoft Entra ID and Purview label policy.  

If the user isn't authorized for a document's sensitivity label with `EXTRACT` permissions, that document is excluded from the query results.

> [!NOTE]
> Internally, the service builds dynamic access filters similar to RBAC enforcement.  
> These filters aren't user-visible and can't be modified in the query payload.


### 3. Secure result filtering

Azure AI Search applies the security filter after all user-defined filters and scoring steps.  
A document is included in the final result set only if:

- The calling application has a valid role assignment (via RBAC), and
- The user identity token represented by `x-ms-query-source-authorization` is valid and permitted to view content with the document's sensitivity label.

If either condition fails, the document is omitted from the results.



## Acquire a user access token

## For testing scenarios

For local testing, you can retrieve a user access token using Azure CLI:

```powershell
$token = az account get-access-token `
  --resource https://search.azure.com `
  --query accessToken `
  --output tsv
```

This approach uses your current Azure CLI login session so you can use over documents you have `EXTRACT` permissions assigned via sensitivity labels. This method is intended for development and validation scenarios only.

## Token acquisition for OBO scenarios

Applications that implement the On-Behalf-Of (OBO) flow must acquire tokens through Microsoft Entra ID using supported authentication libraries such as the [Microsoft Authentication Library (MSAL)](/entra/identity-platform/msal-acquire-cache-tokens).

In OBO scenarios, the token must be requested for the downstream API being called. For example, when calling Azure AI Search: `https://search.azure.com/.default`.

The `.default` scope requests all delegated permissions that have been pre-consented for the application for the specified resource.

Sensitivity label permissions (including `EXTRACT`) aren't represented as OAuth scopes. These permissions are evaluated at runtime by the downstream service (such as Azure AI Search) based on the user identity in the token and the applied sensitivity label policy.

## Query example

Here's an example of a query request using Microsoft Purview sensitivity label enforcement.
The application token is passed as a bearer token in the `Authorization` header. The user token is passed as the raw token value in the `x-ms-query-source-authorization` header, without the `Bearer` prefix.

```http
POST  {{endpoint}}/indexes/sensitivity-docs/docs/search?api-version=2025-11-01-preview
Authorization: Bearer {{app-query-token}}
x-ms-query-source-authorization: {{user-query-token}}
Content-Type: application/json

{
    "search": "*",
    "select": "title,summary,sensitivityLabel",
    "orderby": "title asc"
}
```

## Sensitivity label handling in Azure AI Search

When Azure AI Search indexes document content with sensitivity labels from sources like SharePoint, Azure Blob, and others, it stores both the content and the label metadata. The search query returns indexed content along with the GUID that identifies the sensitivity label applied to the document, only if the user has data `EXTRACT` access for that document assigned via the sensitivity label definition. This GUID uniquely identifies the label but doesn't include human-readable properties such as the label name or associated permissions. 

Note that the GUID alone is insufficient for scenarios that include user interface because sensitivity labels often carry other policy controls enforced by [Microsoft Purview Information Protection](/purview/sensitivity-labels), such as: print permissions or screenshot and screen capture restrictions. Azure AI Search doesn't surface these capabilities.

To display label names and/or enforce UI-specific restrictions, your application must call the Microsoft Purview Information Protection endpoint to retrieve full label metadata and associated permissions.

You can use the GUID returned by Azure AI Search to resolve the label properties and call the [Purview Labels APIs](/graph/api/sensitivitylabel-get) to fetch the label name, description, and policy settings. This [end-to-end demo sample](https://aka.ms/Ignite25/aisearch-purview-sensitivity-labels-repo) includes code that shows how to call the endpoint from a user interface. It also demonstrates how to extract the label name and expose it as part of the citations used in your RAG applications or agents.


## End-to-end testing setup

To help you validate your sensitivity label configuration in Azure AI Search, here's a [reference end-to-end setup](https://aka.ms/Ignite25/aisearch-purview-sensitivity-labels-repo).

This repository demonstrates:
- How to configure sensitivity labels and protection settings
- How to test ingestion and query-time enforcement scenarios for documents with sensitivity labels

