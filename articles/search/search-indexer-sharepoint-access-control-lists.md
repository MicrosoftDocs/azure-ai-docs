---
title: Use a SharePoint indexer to ingest permission metadata
titleSuffix: Azure AI Search
description: Learn how to configure Azure AI Search indexers for ingesting Access Control Lists (ACLs) from SharePoint in Microsoft 365 files.
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 11/08/2025
author: gmndrg
ms.author: gimondra
---

# Use a SharePoint indexer to ingest permission metadata and filter search results based on user access rights

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

> [!IMPORTANT]
> **Recommended first mechanism for full SharePoint governance in search results**  
> For scenarios that require the full SharePoint permissions model, sensitivity labels, and out-of-the-box security trimming, use a [remote SharePoint knowledge source](agentic-knowledge-source-how-to-sharepoint-remote.md). This approach calls SharePoint directly via the [Copilot retrieval API](/microsoft-365-copilot/extensibility/api/ai-services/retrieval/overview) so governance remains fully in SharePoint and query results automatically respect all applicable permissions and labels.

This article documents basic ACL ingestion capability for SharePoint in Microsoft 365 using an Azure AI Search indexer. Compared to the recommended Knowledge source approach above, this functionality has multiple permission model limitations (see below), including one-time ACL ingestion per file, unless additional steps are taken.


## Prerequisites

+ Azure AI Search (Basic or higher) with:
  - [Role-based access enabled](search-security-enable-roles.md)
  - [Managed identity configured](search-how-to-managed-identities.md)

+ SharePoint Online (Microsoft 365) sites, libraries, folders, and files with configured permissions.

+ Follow all configuration steps mentioned in the [SharePoint indexer documentation](search-how-to-index-sharepoint-online.md). Make sure that you apply the specific requirements in this document for ACL ingestion configuration.

+ Configure [Application permissions](search-how-to-index-sharepoint-online.md#step-2-decide-which-permissions-the-indexer-requires) with `Files.Read.All` and `Sites.FullControl.All` (or `Sites.Selected` instead of `Sites.FullControl.All`), to index only the content and permissions of specific sites. Then, grant the application full control permissions for just those selected sites.

  
## Limitations

- During preview this applies to initial ingestion only: ACLs are captured on the first ingestion of each file. Later permission changes [require explicit re-ingestion](#synchronize-permissions-between-indexed-and-source-content)
- Not supported in this preview:
  - [SharePoint Information Management policies](/office/create-and-apply-information-management-policies-eb501fe9-2ef6-4150-945a-65a6451ee9e9) propagation to index.
  - Document [shareable](/sharepoint/shareable-links-anyone-specific-people-organization) "Anyone links" or "People in your organization links". Only "specific people links" sync are supported.
  - [SharePoint groups](/sharepoint/modern-experience-sharing-permissions) that can't be resolved to Microsoft Entra groups (such as Owners, Members, Visitors groups).
  - Azure portal is out of support during preview; use REST API version 2025-11-01-preview or SDK preview packages.
  - This feature must not be tested in combination with [sensitivity labels preservation and honoring](search-indexer-sensitivity-labels.md) feature at this time. Both features must be tested on different indexers and indexes accordingly, since their coexistence is not supported at this time.


## Support for the SharePoint permission model

The following table covers basic ACLs only and specific to documents that are supported by this preview. Lists permissions aren't included, since lists ingestion isn't supported by the SharePoint indexer.

| SharePoint Feature | Description | Supported | Notes |
|--------------------|-------------|-----------|-------|
| Site & library inheritance | Site → library → folder → file | ✔️ | Evaluated at ingestion; effective ACLs computed per file. |
| Folder & file unique ACLs | Item-level access | ✔️ | Included when present at first ingestion. |
| Microsoft Entra (M365/Security) Groups | Group-based access | ✔️ | Group IDs included when resolvable to Entra identificator (ID) |
| SharePoint site groups | Owners/Members/Visitors | ⚠️ Partial | Included only when resolvable to Entra group ID. |
| Shareable "Anyone links" or "People in your organization links" | Org-wide or public access | ❌ | Not supported in preview. |
| External/guest users | Access for guests | ❌ | Not supported. | 
| Information Management policies | Policies to define specific permissions requirements. | ❌ | Not supported in preview. | 
| Purview sensitivity labels  | Document-level security for privacy, categorization, permissions and encryption  | ❌ | Supported via a separate feature: [preserving and honoring sensitivity labels](search-indexer-sensitivity-labels.md) and not to be tested in the same indexer/index as this ACL feature at this time. | 


## How hierarchical permissions are evaluated

SharePoint permissions inherit the hierarchy of Site → Library → Folder → File, unless inheritance is broken.

During ingestion, the indexer gathers user and group identificators (ID) at each level and computes the effective ACL for each file.

## Configure your search service for ACL ingestion and honoring at query time

These are the steps to configure your search service for ACL ingestion and for the index to be enabled for ACL honoring at query time.

### 1. Data source configuration 

Set `indexerPermissionOptions` in the [data source definition](search-how-to-index-sharepoint-online.md#step-4-create-data-source) to allow to index userIds and groupIds from SharePoint documents.

```
{
  "name": "my-sharepoint-acl-datasource",
  "type": "sharepoint",
  "indexerPermissionOptions": ["userIds", "groupIds"],
  "credentials": {
    "connectionString": "<connection-string>;"
  },
  "container": {
    "name": "<library-name>",
    "query": "<optional-folder-path>"
  }
}
```

### 2. Add permission fields to the index definition

Define additional fields to your required [index schema definition](search-how-to-index-sharepoint-online.md#step-5-create-an-index) to be able to store ACLs and enable query-time filtering.

```
{
  "fields": [
    { "name": "UserIds",  "type": "Collection(Edm.String)", "permissionFilter": "userIds",  "filterable": true, "retrievable": false },
    { "name": "GroupIds", "type": "Collection(Edm.String)", "permissionFilter": "groupIds", "filterable": true, "retrievable": false }
  ],
  "permissionFilterOption": "enabled"
}
```
Set `retrievable` attribute to `true` only during development to verify values.

### 3. Configure index projections in your skillset (if applicable)

If your indexer has a [skillset](cognitive-search-working-with-skillsets.md) and you're implementing data chunking through [split skill](cognitive-search-skill-textsplit.md), for example, if you have integrated vectorization, you must ensure you also map the ACL properties to each chunk via [index projections in the skillset](/rest/api/searchservice/skillsets/create-or-update?view=rest-searchservice-2025-11-01-preview&preserve-view=true).

```
PUT https://{service}.search.windows.net/skillsets/{skillset}?api-version=2025-11-01-preview
{
  "name": "my-skillset",
  "skills": [
    {
      "@odata.type": "#Microsoft.Skills.Text.SplitSkill",
      "name": "#split",
      "context": "/document",
      "inputs": [{ "name": "text", "source": "/document/content" }],
      "outputs": [{ "name": "textItems", "targetName": "chunks" }]
    }
    // ... (other skills such as embeddings, entity recognition, etc.)
  ],
  "indexProjections": {
    "selectors": [
      {
        "targetIndexName": "chunks-index",
        "parentKeyFieldName": "parentId",          // must exist in target index
        "sourceContext": "/document/chunks/*",     // match your split output path
        "mappings": [
          { "name": "chunkId",           "source": "/document/chunks/*/id" },     // if you create an id per chunk
          { "name": "content",           "source": "/document/chunks/*/text" },   // chunk text
          { "name": "parentId",          "source": "/document/id" },              // parent doc id
          { "name": "UserIds",  "source": "/document/metadata_user_ids" } // <-- parent → child
          { "name": "GroupIds",  "source": "/document/metadata_group_ids" } // <-- parent → child
        ]
      }
    ],
    "parameters": {
      "projectionMode": "skipIndexingParentDocuments"
    }
  }
}

```

### 4. Configure the indexer field mappings for ACLs

Besides your required [indexer configuration](/search-how-to-index-sharepoint-online.md#step-6-create-an-indexer) map raw metadata ACL fields from SharePoint to your index fields.

```
{
  "fieldMappings": [
    { "sourceFieldName": "metadata_user_ids",  "targetFieldName": "UserIds" },
    { "sourceFieldName": "metadata_group_ids", "targetFieldName": "GroupIds" }
  ]
}
```

## Synchronize permissions between indexed and source content

During public preview when the configuration is completed, and ACLs are captured during the first indexer run and for new files only. To pick up later changes:


| Change  Scope | 	Recommended | Trigger | What refreshes | 
|--------|-------------|---------|---------|
| Single/few files	| Update | LastModified |	Content and ACLs |
| Many items	| Update | [/resetdocs (preview)](/rest/api/searchservice/indexers/reset-docs?view=rest-searchservice-2025-11-01-preview&preserve-view=true) with document keys	| Content and ACLs |
| Entire site/library (as defined in the data source configuration) |	Update | /resync (preview) with permissions |	Only ACLs (no content refresh) |


### Reset specific documents

You can [reset specific documents](/rest/api/searchservice/indexers/reset-docs?view=rest-searchservice-2025-11-01-preview&preserve-view=true) to fully ingest again content and ACLs.

```
POST https://{service}.search.windows.net/indexers/{indexer}/resetdocs?api-version=2025-11-01-preview
{
  "documentKeys": ["doc123", "doc456"]
}
```

### Resync ACLs across the full data source

You can [resync the full data set ACL content](/rest/api/searchservice/indexers/resync?view=rest-searchservice-2025-11-01-preview&preserve-view=true) after initial ingestion.

```
POST https://{service}.search.windows.net/indexers/{indexer}/resync?api-version=2025-11-01-preview
{
  "options": ["permissions"]
}
```

> [!IMPORTANT]
> If you change SharePoint permissions and don't trigger one of the mechanisms above, the index will serve stale ACL data > for already-ingested items.

Once your data and ACLs have been indexed, you may proceed to [query the index](search-query-access-control-rbac-enforcement.md). 


## See also

[Index SharePoint content in Azure AI Search (preview)](search-how-to-index-sharepoint-online.md)

[Query-Time ACL enforcement](search-query-access-control-rbac-enforcement.md)
