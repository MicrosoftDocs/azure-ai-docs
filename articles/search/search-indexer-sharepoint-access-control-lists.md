---
title: Use a SharePoint indexer to ingest permission metadata
titleSuffix: Azure AI Search
description: Learn how to configure Azure AI Search indexers for ingesting Access Control Lists (ACLs) from SharePoint in Microsoft 365 files.
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 11/09/2025
author: gmndrg
ms.author: gimondra
---

# Use a SharePoint indexer to ingest permission metadata and filter search results based on user access rights

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

This article explains how to ingest an Access Control List (ACL) alongside other content from SharePoint in Microsoft 365 using an Azure AI Search indexer. Permissions from SharePoint are preserved as permission metadata for each indexed document. When users query an index containing content from SharePoint, their search results consist of only those documents for which they have permission to access.


> [!IMPORTANT]
> For scenarios that require the full SharePoint permissions model, sensitivity labels, and out-of-the-box security trimming, use a [remote SharePoint knowledge source](agentic-knowledge-source-how-to-sharepoint-remote.md). This approach calls SharePoint directly via the [Copilot retrieval API](/microsoft-365-copilot/extensibility/api/ai-services/retrieval/overview) so governance remains fully in SharePoint and query results automatically respect all applicable permissions and labels.


## Prerequisites

+ [Azure AI Search](search-create-service-portal.md) (Basic or higher).

+ SharePoint in Microsoft 365 sites, libraries, folders, and files with configured permissions.

+ Follow all configuration steps mentioned in the [SharePoint indexer documentation](search-how-to-index-sharepoint-online.md). Make sure that you apply the specific requirements in this document for ACL ingestion configuration.

+ Configure [Application permissions](search-how-to-index-sharepoint-online.md#step-2-decide-which-permissions-the-indexer-requires) with `Files.Read.All` and `Sites.FullControl.All` (or `Sites.Selected` instead of `Sites.FullControl.All`), to index only the content and permissions of specific sites. Then, grant the application full control permissions for just those selected sites.

  
## Limitations

- During public preview, this functionality applies to initial ingestion only: ACLs are captured on the first ingestion of each file. If permissions change in the source, you must [explicitly reindex those documents or their respective ACLs](#synchronize-permissions-between-indexed-and-source-content).
  
- Not supported in this preview:
  + [SharePoint Information Management policies](/sharepoint/intro-to-info-mgmt-policies) applicable to user access.
  + Document [shareable](/sharepoint/shareable-links-anyone-specific-people-organization) "Anyone links" or "People in your organization links". Only "specific people links" sync are supported.
  + [SharePoint groups](/sharepoint/modern-experience-sharing-permissions) that can't be resolved to Microsoft Entra groups (such as Owners, Members, Visitors groups).
  + Azure portal is out of support during preview; use REST API version 2025-11-01-preview or SDK preview packages.
  + This feature must not be tested in combination with [sensitivity labels preservation and honoring](search-indexer-sensitivity-labels.md) feature at this time. Both features must be tested on different indexers and indexes accordingly, since their coexistence is not supported currently.


## Support for the SharePoint permission model

This preview supports only basic ACLs for documents, as shown in the following table. The SharePoint indexer doesn't support lists ingestion, so it excludes lists permissions.

| SharePoint Feature | Description | Supported | Notes |
|--------------------|-------------|-----------|-------|
| Site & library inheritance | Site → library → folder → file. | ✔️ | Evaluated at ingestion; effective ACLs computed per file. |
| Folder & file unique ACLs | Item-level access. | ✔️ | Included when present at first ingestion. |
| Microsoft Entra (M365/Security) Groups | Group-based access. | ✔️ | Group IDs included when resolvable to Entra identifier (ID). |
| SharePoint site groups | Owners/Members/Visitors. | ⚠️ Partial | Included only when resolvable to Entra group ID. |
| Shareable "Anyone links" or "People in your organization links" | Org-wide or public access. | ❌ | Not supported in preview. |
| External/guest users | Access for guests. | ❌ | Not supported. | 
| Information Management policies | Policies to define specific permissions requirements. | ❌ | Not supported in preview. | 
| Purview sensitivity labels  | Document-level security for privacy, categorization, permissions, and encryption  | ❌ | Supported via a separate feature: [preserving and honoring sensitivity labels](search-indexer-sensitivity-labels.md) and not to be tested in the same indexer/index as this ACL feature at this time. | 


## How hierarchical permissions are evaluated

SharePoint permissions inherit the hierarchy of Site → Library → Folder → File, unless inheritance is broken.

During ingestion, the indexer gathers user and group identifiers (ID) at each level and computes the effective ACL for each file.

## Configure your search service for ACL ingestion and honoring at query time

These steps configure your search service for ACL ingestion and enable ACL honoring at query time.

### 1. Data source configuration 

Set `indexerPermissionOptions` in the [data source definition](search-how-to-index-sharepoint-online.md#step-4-create-data-source) to allow indexing of `userIds` and `groupIds` from SharePoint documents.

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

Add fields to your [index schema definition](search-how-to-index-sharepoint-online.md#step-5-create-an-index)  to store ACLs and support query-time filtering.
```
{
  "fields": [
    { "name": "UserIds",  "type": "Collection(Edm.String)", "permissionFilter": "userIds",  "filterable": true, "retrievable": false },
    { "name": "GroupIds", "type": "Collection(Edm.String)", "permissionFilter": "groupIds", "filterable": true, "retrievable": false }
  ],
  "permissionFilterOption": "enabled"
}
```
Set `retrievable` attribute to `true` only during development to verify values. You can change retrievable from true to false with no index rebuild requirement.

### 3. Configure index projections in your skillset (if applicable)

If your indexer uses a [skillset](cognitive-search-working-with-skillsets.md) with data chunking, such as a [split skill](cognitive-search-skill-textsplit.md) when enabling [integrated vectorization](vector-search-integrated-vectorization.md), make sure to map ACL properties to each chunk using [index projections](/rest/api/searchservice/skillsets/create-or-update?view=rest-searchservice-2025-11-01-preview&preserve-view=true).

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

Besides your required [indexer configuration](search-how-to-index-sharepoint-online.md#step-6-create-an-indexer), map raw metadata ACL fields from SharePoint to your index fields.

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
> If you change SharePoint permissions without triggering an update mechanism, the index serves stale ACL data for previously ingested files.

After indexing your data and ACLs, you can [query the index](search-query-access-control-rbac-enforcement.md). .


## See also

[Index SharePoint content in Azure AI Search (preview)](search-how-to-index-sharepoint-online.md)

[Query-Time ACL enforcement](search-query-access-control-rbac-enforcement.md)
