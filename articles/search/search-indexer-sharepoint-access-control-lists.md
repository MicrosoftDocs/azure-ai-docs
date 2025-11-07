---
title: Use a SharePoint indexer to ingest permission metadata
titleSuffix: Azure AI Search
description: Learn how to configure Azure AI Search indexers for ingesting Access Control Lists (ACLs) from SharePoint in Microsoft 365 files.
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 11/07/2025
author: gmndrg
ms.author: gimondra
---

# Use a SharePoint indexer to ingest permission metadata and filter search results based on user access rights

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

> [!IMPORTANT]
> **Recommended first mechanism for full SharePoint governance**  
> For scenarios that require the **full SharePoint permissions model**, **sensitivity labels**, and **out-of-the-box security trimming**, use **Knowledge source: Microsoft SharePoint (remote)** powered by **Azure AI Search**. This approach calls SharePoint directly via the retrieval API so governance remains in SharePoint and query results automatically respect all applied permissions and labels.  
> See: [Azure AI Search knowledge sources — Microsoft SharePoint (remote)](search-how-to-index-sharepoint.md).

This article documents a **basic ACL ingestion** capability for **SharePoint in Microsoft 365** using an **Azure AI Search indexer**. It is **preview**, **indexer-only** (Push API not supported), and intended **only for testing and feedback**. Compared to the recommended Knowledge source approach above, this functionality has **multiple limitations** (see below), including **one-time ACL ingestion per file** unless additional steps are taken.

> [!NOTE]
> This works **only for SharePoint in Microsoft 365**. On-premises SharePoint Server and other deployments aren’t supported.

---

## Prerequisites

+ [Microsoft Entra ID authentication and authorization](/entra/identity/authentication/overview-authentication). Services and apps must be in the same tenant. Users can be in different Microsoft Entra tenants if trust is configured.

+ Azure AI Search (Basic or higher) with:
  - [Role-based access enabled](search-security-enable-roles.md)
  - [Managed identity configured](search-how-to-managed-identities.md)

+ SharePoint Online (Microsoft 365) sites, libraries, folders, and files with configured permissions.

+ **[Placeholder: Authentication setup for SharePoint indexer]**  
  Configure credentials using Microsoft Entra ID app registration or managed identity with Microsoft Graph. _(Details to be finalized during preview.)_

---

## Limitations

- **Preview & testing only**: Recommended for **lab/test** and **feedback**, not production.
- **Initial ingestion only**: ACLs are captured on the **first ingestion** of each file. Later permission changes require explicit re-ingestion (see **Synchronize permissions**).
- **Incremental ACL refresh**: During preview, ACL “incremental” refresh enumerates the scope and **re-indexes ACLs broadly** (no true per-item ACL delta yet).
- **Not supported** in this preview:
  - SharePoint **policies** (e.g., conditional/IRM/DLP) — **not represented** in tables or metadata here.
  - **Shared links** for “All tenant users” or “Anyone/public”.
  - **SharePoint groups** that can’t be resolved to Microsoft Entra group IDs.
  - **Portal**: Not yet supported in the Azure portal; use REST or SDK preview packages.
---

## Support for the SharePoint permission model

The following table covers **basic ACLs** only.  
**SharePoint policies** are **out of scope** for this article and **not listed** here.

| SharePoint Feature | Description | Supported | Notes |
|--------------------|-------------|-----------|-------|
| Site & library inheritance | Site → library → folder → file | ✔️ | Evaluated at ingestion; effective ACLs computed per file. |
| Folder & file unique ACLs | Item-level access | ✔️ | Included when present at first ingestion. |
| Microsoft Entra (M365/Security) Groups | Group-based access | ✔️ | Group IDs included when resolvable to Entra IDs. |
| SharePoint site groups | Owners/Members/Visitors | ⚠️ Partial | Included only when resolvable to Entra group IDs. |
| “All tenant users” / shared links | Org-wide or public access | ❌ | Not supported in preview. |
| External/guest users | Access for guests | ❌ | Not supported in preview. |

---

## How hierarchical permissions are evaluated

SharePoint permissions inherit **Site → Library → Folder → File**.  
During ingestion, the indexer gathers user and group IDs at each level and computes the **effective** ACL for each file.

```txt
Site → Library → Folder → File
Final effective ACL = Inherited permissions ∪ Item-level unique permissions
Configure SharePoint
Authorization requirements
Your search service identity must have Microsoft Graph access to target SharePoint sites and content.

[Placeholder: Configure Azure AI Search identity for SharePoint access]

Grant app or managed identity permissions (e.g., Sites.Read.All, Files.Read.All)

Admin consent in Microsoft Entra ID

Scope to target sites

Content readiness
Confirm the identity can access the target site collections and libraries.

Ensure inheritance is as intended; identify locations with unique permissions.

Minimize excessive item-level breaks unless strictly required.

Configure Azure AI Search
Enable RBAC on your search service.

Configure a managed identity.

Authorization to operate
Assign:

Search Service Contributor (create indexers/data sources/indexes)

Search Index Data Contributor (data import)

Search Index Data Reader (query)

Configure indexing
To ingest SharePoint ACLs, create a SharePoint data source, index, and indexer.

Create the data source
Data source type: sharepoint

indexerPermissionOptions: include:

userIds

groupIds

Example (managed identity connection; placeholder values):

json
Copy code
{
  "name": "my-sharepoint-acl-datasource",
  "type": "sharepoint",
  "indexerPermissionOptions": ["userIds", "groupIds"],
  "credentials": {
    "connectionString": "ResourceId=/subscriptions/<subscription-ID>/resourceGroups/<resource-group>/providers/Microsoft.SharePoint/sites/<site-or-tenant-scope>/;"
  },
  "container": {
    "name": "<library-name>",
    "query": "<optional-folder-path>"
  }
}
[Placeholder: Add finalized authentication properties here when available]

Add permission fields to the index
Define fields to store ACLs and enable query-time filtering:

json
Copy code
{
  "fields": [
    { "name": "UserIds",  "type": "Collection(Edm.String)", "permissionFilter": "userIds",  "filterable": true, "retrievable": false },
    { "name": "GroupIds", "type": "Collection(Edm.String)", "permissionFilter": "groupIds", "filterable": true, "retrievable": false }
  ],
  "permissionFilterOption": "enabled"
}
Set retrievable to true only during development to verify values.

Configure the indexer
Map raw metadata fields from SharePoint to your index fields:

json
Copy code
{
  "fieldMappings": [
    { "sourceFieldName": "metadata_user_ids",  "targetFieldName": "UserIds" },
    { "sourceFieldName": "metadata_group_ids", "targetFieldName": "GroupIds" }
  ]
}
Synchronize permissions between indexed and source content
ACLs are captured at first ingestion. To pick up later changes:

Change Scope	Recommended Trigger	What Refreshes
Single/few files	Update LastModified or queue a targeted re-index	Content and ACLs
Many items	/resetdocs (preview) with document keys	Content and ACLs
Entire site/library	/resync (preview) with permissions	Only ACLs (no content refresh)

Reset specific documents:

http
Copy code
POST https://{service}.search.windows.net/indexers/{indexer}/resetdocs?api-version=2025-11-01-preview
{
  "documentKeys": ["doc123", "doc456"]
}
Resync ACLs across the data source:

http
Copy code
POST https://{service}.search.windows.net/indexers/{indexer}/resync?api-version=2025-11-01-preview
{
  "options": ["permissions"]
}
[!IMPORTANT]
If you change SharePoint permissions and don’t trigger one of the mechanisms above, the index will serve stale ACL data for already-ingested items.

Deletion tracking
Enable deletion tracking so that documents deleted in SharePoint are removed from the index.

Recommendations and best practices
Prefer Microsoft Entra (M365/Security) Groups over individual user assignments to reduce ACL churn.

Keep inheritance consistent; minimize unique permissions at item level.

For production with complete governance (including sensitivity labels and the full permissions model), use Knowledge source: Microsoft SharePoint (remote) with Azure AI Search.

See also
Azure AI Search

Index SharePoint content in Azure AI Search (preview)

Connect to Azure AI Search using roles

Query-Time ACL enforcement
