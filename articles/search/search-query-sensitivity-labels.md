---
title: Query-Time Microsoft Purview Sensitivity Label Enforcement
description: Learn how query-time enforcement of Microsoft Purview sensitivity labels ensures secure document retrieval in Azure AI Search for indexes containing label metadata.
ms.reviewer: gimondra
ms.service: azure-ai-search
ms.topic: concept-article
ms.date: 06/02/2026
ai-usage: ai-assisted
---

# Query-time enforcement of Microsoft Purview sensitivity labels in Azure AI Search (preview)

<!-- preserve -->
<!-- LEGAL/CELA NOTICE — DO NOT MODIFY. This wording is mandated by Microsoft Legal (CELA) and must remain verbatim in every Azure AI Search article that discusses ACLs or document-level permissions. The ONLY permitted change is updating the API version placeholder when the documented API version changes. Do not rewrite, paraphrase, shorten, or remove. -->

> [!IMPORTANT]
> These features and functionality are part of the 2026-05-01-preview REST API. The 2026-05-01-preview is licensed to you as part of your Azure subscription and is subject to the terms applicable to "Previews" in the [Microsoft Product Terms](https://www.microsoft.com/licensing/terms/welcome/welcomepage), the [Microsoft Products and Services Data Protection Addendum](https://www.microsoft.com/licensing/docs/view/Microsoft-Products-and-Services-Data-Protection-Addendum-DPA) ("DPA"), and the [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).
>
> The 2026-05-01-preview can't modify access permissions that were set outside of the 2026-05-01-preview. If you use the 2026-05-01-preview with access- or permission-restricted content, a timing lag will occur before the 2026-05-01-preview recognizes changes to those access or permission restrictions.

At query time, Azure AI Search can enforce sensitivity label policies defined in [Microsoft Purview](/purview/create-sensitivity-labels). These policies include the evaluation of [`EXTRACT` usage rights](/purview/rights-management-usage-rights) associated with each document, ensuring users can only retrieve documents they're permitted to access.

This capability extends [document-level access control](search-document-level-access-overview.md) to align with your organization's [information protection and compliance requirements](/purview/create-sensitivity-labels) managed in Microsoft Purview.

When Purview sensitivity label indexing is enabled, Azure AI Search checks each document's label metadata during query time. It applies access filters based on Purview policies to return only results the requesting user is allowed to access.

This article explains how query-time sensitivity label enforcement works and how to issue secure search queries.

> [!TIP]
> If you consume labeled content through a knowledge base (retrieve action or MCP endpoint) instead of calling Azure AI Search directly, see [Inspect sensitivity label metadata in retrieve responses](agentic-retrieval-how-to-retrieve.md#inspect-sensitivity-label-metadata-in-the-response-preview) for the equivalent response fields. Elevated read and Microsoft Purview audit logging documented in this article apply to both paths.

## Prerequisites

- Complete all steps in [Use Azure AI Search indexers to ingest Microsoft Purview sensitivity labels](search-indexer-sensitivity-labels.md).

- Both the Azure AI Search service and the user issuing the query must be in the same Microsoft Entra tenant.

- REST API version 2025-11-01-preview or an equivalent preview SDK package to query the index. The [elevated read](#elevated-read-for-administrative-investigations-preview) capability and Purview audit logging require [2026-05-01-preview](/rest/api/searchservice/operation-groups?view=rest-searchservice-2026-05-01-preview&preserve-view=true) or later.

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
- The calling application's RBAC role, provided in the `Authorization` header.  The minimum required role is `Search Index Data Reader`. For more details, review the [Azure AI Search RBAC guide](search-security-rbac.md).
- The user identity via token, provided in the `x-ms-query-source-authorization` header.  

Both are required to authorize label-based visibility.

| Input type | Description | Example source |
|-------------|--------------|----------------|
| Application role | Determines whether the calling app has permission to execute queries on the index. | `Authorization: Bearer <app-token>` |
| User identity | Determines which sensitivity labels the end user is allowed to access. | `x-ms-query-source-authorization: <user-token>` |



### 2. Sensitivity label evaluation

When a query request is received, Azure AI Search evaluates:
1. The `sensitivityLabel` field in each indexed document (extracted from Microsoft Purview during ingestion).  
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

To query Azure AI Search using user context, you must acquire an access token that represents the signed-in user. The approach you use depends on whether you're testing locally with your own token, if you have access to the source document, or implementing the application flow that requires passing the end-user token.

### For testing scenarios

For local testing, you can retrieve a user access token using Azure CLI:

```powershell
$token = az account get-access-token `
  --resource https://search.azure.com `
  --query accessToken `
  --output tsv
```

This approach uses your current Azure CLI login session, so you can use the context over documents you have `EXTRACT` permissions assigned via sensitivity labels. This method is intended for development and validation scenarios only.

### Token acquisition for OBO scenarios

Applications that implement the on-behalf-of (OBO) flow must acquire tokens through Microsoft Entra ID using a supported authentication library, such as the [Microsoft Authentication Library](/entra/identity-platform/msal-acquire-cache-tokens) (MSAL).

In OBO scenarios, the token must be requested for the downstream API that the application calls. For example, when calling Azure AI Search, the resource URI is `https://search.azure.com/.default`.

The `.default` scope requests all delegated permissions that have been pre-consented for the application for the specified resource.

Sensitivity label permissions, including `EXTRACT`, aren't represented as OAuth scopes. These permissions are evaluated at runtime by the downstream service, such as Azure AI Search, based on the user identity in the token and the applied sensitivity label policy.

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

## Elevated read for administrative investigations (preview)

Elevated read lets an authorized developer return labeled documents that the calling user wouldn't normally see, while emitting a Microsoft Purview audit log entry for every document the request returns. Use it for compliance reviews, eDiscovery, incident response, and other administrative investigations where an auditable record of access is required.

Elevated read is available on Purview-enabled indexes in REST API version [2026-05-01-preview](/rest/api/searchservice/operation-groups?view=rest-searchservice-2026-05-01-preview&preserve-view=true) and later.

### How elevated read works

1. The calling application sets the `x-ms-enable-elevated-read: true` header on the search request.

1. Azure AI Search skips the per-document label-based access check and returns matching documents, regardless of the requesting user's `EXTRACT` permissions on each label.

1. For each document in the response, Azure AI Search emits one entry to the [Microsoft Purview audit log](#find-elevated-read-audit-logs-in-microsoft-purview) on behalf of the requesting tenant. A single search request that returns *N* documents produces *N* audit entries.

1. Audit entries are uploaded to Purview asynchronously after the search response is returned.

### Required role assignment

The calling developer user must hold the **Search Index Data Contributor** role on the search service or index scope. **Search Index Data Reader** isn't sufficient. Elevated read fails with `403 Forbidden` if the role isn't assigned. For more information about Azure AI Search roles, see [Connect to Azure AI Search using roles](search-security-rbac.md).

When the `x-ms-enable-elevated-read` header is set to `true`, the `x-ms-query-source-authorization` header isn't allowed to be used. 

### Elevated read example

```http
POST  {{endpoint}}/indexes/sensitivity-docs/docs/search?api-version=2026-05-01-preview
Authorization: Bearer {{contributor-token}}
x-ms-enable-elevated-read: true
Content-Type: application/json

{
    "search": "*",
    "select": "title,summary,sensitivityLabel",
    "orderby": "title asc"
}
```

### Audit fields emitted to Microsoft Purview

Each audit entry follows the [Office 365 management activity API](/office/office-365-management-api/office-365-management-activity-api-schema) schema and includes the following fields.

| Category | Field | Description |
|---|---|---|
| Standard schema | `CreationTime` | UTC timestamp of the elevated read request. |
| Standard schema | `Operation` | The operation name that identifies the elevated read action. |
| Standard schema | `OrganizationId` | The Microsoft Entra tenant ID of the search service. |
| Standard schema | `RecordType` | The Office 365 management activity record type for Azure AI Search. |
| Standard schema | `UserType` | The type of user that issued the request. |
| Standard schema | `UserId` | The unique identifier (PUID) of the requesting user. |
| Standard schema | `UserPrincipalName` | The user principal name (UPN) of the requesting user. |
| Standard schema | `ClientIP` | The IP address of the calling application. |
| Azure AI Search | `UserObjectId` | The Microsoft Entra object ID of the requesting user. |
| Azure AI Search | `DocumentDataSourceType` | The type of source for the accessed document, such as `azureblob`, `sharepoint`, `onelake`, or `searchIndex`. |
| Azure AI Search | `DocumentDataSourceId` | The source-specific identifier of the accessed document, such as the blob URL or SharePoint item ID. |
| Azure AI Search | `SensitivityLabelName` | The display name of the sensitivity label applied to the accessed document. |

### Graceful degradation

If Azure AI Search can't reach Microsoft Purview while processing a query, such as during a transient Purview outage, label evaluation is skipped for that request. The behavior depends on whether the request includes a user identity token:

- **Elevated read requests** (`x-ms-enable-elevated-read: true`): The request fails with `5xx`. Azure AI Search doesn't return labeled documents without first being able to emit audit logs.

- **Standard label-enforced requests** (with `x-ms-query-source-authorization`): The request fails with `5xx`. Azure AI Search doesn't return partial or unfiltered results when label policies can't be evaluated.

- **Calls without `x-ms-query-source-authorization`** issued by an application with at least the **Search Index Data Reader** role: The request succeeds and returns only documents that don't have a sensitivity label. Labeled documents are omitted from the response.

This degraded path is intended only for non-user-facing workflows that explicitly accept unlabeled-only results. Don't rely on it for end-user search experiences.

### Find elevated read audit logs in Microsoft Purview

Azure AI Search uploads audit entries to the calling tenant's Microsoft Purview audit log. To investigate elevated read activity:

1. In the [Microsoft Purview portal](https://purview.microsoft.com), select **Solutions** > **Audit**.

1. Select **Audit Search**, and then filter by date range, user, or the Azure AI Search record type.

1. Open an entry to view the standard schema fields and the Azure AI Search custom fields, including `SensitivityLabelName`, `DocumentDataSourceType`, and `DocumentDataSourceId`.

For step-by-step guidance on running audit searches, retention behavior, and required Purview roles, see [Search the audit log in the Microsoft Purview portal](/purview/audit-search).

## Sensitivity label handling in Azure AI Search

When Azure AI Search indexes document content with sensitivity labels from sources like SharePoint, Azure Blob, and others, it stores both the content and the label metadata. The search query returns indexed content along with the GUID that identifies the sensitivity label applied to the document, only if the user has data `EXTRACT` access for that document assigned via the sensitivity label definition. This GUID uniquely identifies the label but doesn't include human-readable properties such as the label name or associated permissions. 

Note that the GUID alone is insufficient for scenarios that include user interface because sensitivity labels often carry other policy controls enforced by [Microsoft Purview Information Protection](/purview/sensitivity-labels), such as: print permissions or screenshot and screen capture restrictions. Azure AI Search doesn't surface these capabilities.

To display label names and/or enforce UI-specific restrictions, your application must call the Microsoft Purview Information Protection endpoint to retrieve full label metadata and associated permissions.

You can use the GUID returned by Azure AI Search to resolve the label properties and call the [Purview Labels APIs](/graph/api/sensitivitylabel-get) to fetch the label name, description, and policy settings. 


## End-to-end testing setup

To help you validate your sensitivity label configuration in Azure AI Search, here's a [reference end-to-end setup](https://aka.ms/Ignite25/aisearch-purview-sensitivity-labels-repo).

This repository demonstrates:
- How to configure sensitivity labels sync and honoring in Azure AI Search
- How to test ingestion and query-time enforcement scenarios for documents with sensitivity labels
- How to extract the label name and expose it as part of the citations used in your RAG applications or agents.

