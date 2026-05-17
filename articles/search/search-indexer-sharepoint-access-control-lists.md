---
title: Use a SharePoint Indexer to Ingest Permission Metadata
description: Learn how to configure Azure AI Search indexers for ingesting Access Control Lists (ACLs) from SharePoint in Microsoft 365 files.
ms.reviewer: gimondra
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 04/23/2026
---

# Use a SharePoint indexer to ingest permission metadata and filter search results based on user access rights

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

This article explains how to ingest an access control list (ACL) alongside other content from SharePoint in Microsoft 365 using an Azure AI Search indexer. Permissions from SharePoint are preserved as permission metadata for each indexed document. When users query an index containing content from SharePoint, their search results consist of only those documents for which they have permission to access.

:::image type="content" source="media/search-indexer-sharepoint-access-control-lists/security-trimmed-rag-sharepoint.png" alt-text="Architecture diagram showing a security-trimmed RAG solution where a SharePoint indexer ingests documents and ACL permission metadata from a SharePoint site, stores them in an Azure AI Search index, and a RAG orchestrator filters query results so each user retrieves only documents they're authorized to access." lightbox="media/search-indexer-sharepoint-access-control-lists/security-trimmed-rag-sharepoint.png":::

> [!IMPORTANT]
> For scenarios that require the full SharePoint permissions model, sensitivity labels, and out-of-the-box security trimming, use a [remote SharePoint knowledge source](agentic-knowledge-source-how-to-sharepoint-remote.md). This approach calls SharePoint directly via the [Copilot retrieval API](/microsoft-365-copilot/extensibility/api/ai-services/retrieval/overview). Governance remains fully in SharePoint, and query results automatically respect all applicable permissions and labels.

## Prerequisites

+ [Azure AI Search](search-create-service-portal.md) on a billable tier (Basic or higher) in any region.

+ SharePoint in Microsoft 365 sites, libraries, folders, and files with configured permissions.

+ Complete all configuration steps in the [SharePoint indexer documentation](search-how-to-index-sharepoint-online.md), applying the ACL-specific requirements described in this article.

+ Configure [application permissions](search-how-to-index-sharepoint-online.md#step-2-decide-which-permissions-the-indexer-requires) with `Files.Read.All` and `Sites.FullControl.All` (or `Sites.Selected` instead of `Sites.FullControl.All`) to index only the content and permissions of specific sites. Then, grant the application full control permissions for those selected sites.

+ REST API version 2026-05-01-preview or an equivalent preview SDK package.

## Limitations

+ Incremental ACL updates require the 2026-05-01-preview REST API or later. In earlier preview API versions, ACLs are captured only on the first ingestion of each item, and later permission changes require explicit reindexing. For migration steps, see [Synchronize permissions between indexed and source content](#synchronize-permissions-between-indexed-and-source-content).
  
+ Parent-scope permission changes aren't picked up automatically on subsequent indexer runs. If you change permissions on a site, library, list, or folder that's inherited by its child items (instead of on the items themselves), trigger a [`/resync` with `options: ["permissions"]`](#resync-acls-across-the-full-data-source) or [`/resetdocs`](#reset-specific-documents) to refresh ACLs for those items.

+ The Azure portal doesn't support this feature.

+ The following aren't supported in this preview:

  + [SharePoint Information Management policies](/sharepoint/intro-to-info-mgmt-policies) applicable to user access. These policies aren't evaluated, ingested, or honored at query time.

  + [Shareable links](/sharepoint/shareable-links-anyone-specific-people-organization) scoped to "Anyone" or "People in your organization." Only links scoped to "Specific people" are supported.

  + [SharePoint groups](/sharepoint/modern-experience-sharing-permissions) (such as Owners, Members, and Visitors groups) are supported starting in the 2026-05-01-preview REST API. See [Configure SharePoint groups support](#configure-sharepoint-groups-support). In earlier preview API versions, only SharePoint groups that resolve to Microsoft Entra groups are supported.
 
+ The following indexer features don't support permission inheritance in indexed documents originating from ADLS Gen2. If you use any of these features in a skillset or indexer, document-level permissions aren't included in the indexed content.

  + [Custom Web API skill](cognitive-search-custom-skill-web-api.md)

  + [GenAI Prompt skill](cognitive-search-skill-genai-prompt.md)

  + [Knowledge store](knowledge-store-concept-intro.md)

  + [Indexer enrichment cache](enrichment-cache-how-to-configure.md)

  + [Debug sessions](cognitive-search-debug-session.md)


## Support for the SharePoint permission model

This preview supports basic ACLs for documents, list items, and modern ASPX site pages.

| SharePoint Feature | Description | Supported | Notes |
|--------------------|-------------|-----------|-------|
| Site, library, list, and page inheritance | Site → library/list → folder → file/item/page. | ✔️ | Evaluated at ingestion; effective ACLs computed per item. |
| Folder, file, list item, and page unique ACLs | Item-level access. | ✔️ | Included when present at first ingestion and on subsequent runs that detect ACL changes for items with unique permissions. |
| SharePoint list items | Permissions on list items (`allSiteLists` and `allSiteContent` containers). | ✔️ | Preview, starting in the 2026-05-01-preview REST API. |
| ASPX site pages | Permissions on modern site pages (`allSitePages` and `allSiteContent` containers). | ✔️ | Preview, starting in the 2026-05-01-preview REST API. |
| Microsoft Entra (M365/Security) Groups | Group-based access. | ✔️ | Group IDs included when resolvable to a Microsoft Entra identifier (ID). |
| SharePoint site groups | Owners/Members/Visitors and custom site groups. | ✔️ | Preview, starting in the 2026-05-01-preview REST API. Requires the [SharePoint groups configuration](#configure-sharepoint-groups-support). Group IDs are emitted with the `spg:` prefix. |
| Shareable "Anyone links" or "People in your organization links" | Org-wide or public access. | ❌ | Not supported in preview. |
| External/guest users | Access for guests. | ❌ | Not supported. | 
| Information Management policies | Policies to define specific permissions requirements. | ❌ | Not supported in preview. | 
| Purview sensitivity labels  | Document-level security for privacy, categorization, permissions, and encryption  | ❌ | Supported via a separate feature: [preserving and honoring sensitivity labels](search-indexer-sensitivity-labels.md). | 

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

If your indexer uses a [skillset](cognitive-search-working-with-skillsets.md) with data chunking, such as a [split skill](cognitive-search-skill-textsplit.md) when enabling [integrated vectorization](vector-search-integrated-vectorization.md), make sure to map ACL properties to each chunk using [index projections](/rest/api/searchservice/skillsets/create-or-update?view=rest-searchservice-2026-05-01-preview&preserve-view=true).

```
PUT https://{service}.search.windows.net/skillsets/{skillset}?api-version=2026-05-01-preview
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
          { "name": "UserIds",  "source": "/document/metadata_user_ids" }, // <-- parent → child
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

## Configure SharePoint groups support

Starting in the 2026-05-01-preview REST API, the SharePoint indexer can ingest membership of SharePoint site groups (such as Owners, Members, Visitors, and custom site groups) and honor them at query time. SharePoint group IDs are emitted in the `metadata_group_ids` field with the `spg:` prefix to distinguish them from Microsoft Entra group object IDs.

To enable SharePoint groups support, add a `sharePointConnectorAppRegistration` property to your index that references an existing federated identity credential, and map the SharePoint site URL to an index field.

1. Add the `sharePointConnectorAppRegistration` property and a `SharePointSiteUrl` field to your index definition. Mark the field with the `sharepointSiteUrl: true` attribute.

   ```http
   PUT https://{service}.search.windows.net/indexes/{index}?api-version=2026-05-01-preview
   {
     "name": "my-sharepoint-acl-index",
     "sharePointConnectorAppRegistration": {
       "federatedCredentialId": "<federated-identity-credential-object-id>"
     },
     "fields": [
       { "name": "SharePointSiteUrl", "type": "Edm.String", "sharepointSiteUrl": true, "filterable": false, "retrievable": false }
     ],
     "permissionFilterOption": "enabled"
   }
   ```

   The `federatedCredentialId` value is the object ID of the federated identity credential previously configured on the [Microsoft Entra application registration](search-how-to-index-sharepoint-online.md#configuring-the-registered-application-with-a-managed-identity) used by the indexer.

1. Map the `metadata_sharepoint_site_url` source field to `SharePointSiteUrl` in the indexer field mappings.

   ```
   {
     "fieldMappings": [
       { "sourceFieldName": "metadata_sharepoint_site_url", "targetFieldName": "SharePointSiteUrl" }
     ]
   }
   ```

At query time, the search service uses the registered application and the `SharePointSiteUrl` field to resolve which SharePoint groups the calling user belongs to on that site, and matches them against the `spg:`-prefixed values stored in `GroupIds`.

## Synchronize permissions between indexed and source content

Starting in the 2026-05-01-preview REST API, ACL changes for items with unique permissions are detected and refreshed on each successful indexer run. The indexer uses SharePoint change tokens to pick up role assignment additions and removals incrementally, in the same way it picks up content changes.

Some scenarios still require an explicit refresh:

| Change scope | Detected automatically | Recommended action |
|--------------|------------------------|--------------------|
| Permissions on a specific item with unique permissions (file, list item, or page) | Yes | No action required. The change is picked up on the next successful indexer run. |
| Content change on a specific item (which also re-evaluates effective ACLs for that item) | Yes | No action required. |
| Permissions change on a parent scope (site, library, list, or folder) that's inherited by child items | No | Call [`/resync` with `options: ["permissions"]`](#resync-acls-across-the-full-data-source) to refresh ACLs across the data source, or call [`/resetdocs`](#reset-specific-documents) with the affected document keys to refresh both content and ACLs. |
| ACL ingestion enabled on an existing indexer | No | Call [`/resync` with `options: ["permissions"]`](#resync-acls-across-the-full-data-source) to backfill ACLs for previously indexed items. |

### Reset specific documents

You can [reset specific documents](/rest/api/searchservice/indexers/reset-docs?view=rest-searchservice-2026-05-01-preview&preserve-view=true) to fully ingest again content and ACLs.

```
POST https://{service}.search.windows.net/indexers/{indexer}/resetdocs?api-version=2026-05-01-preview
{
  "documentKeys": ["doc123", "doc456"]
}
```

### Resync ACLs across the full data source

You can [resync the full data set ACL content](/rest/api/searchservice/indexers/resync?view=rest-searchservice-2026-05-01-preview&preserve-view=true) after initial ingestion. To fully succeed, this operation requires an [indexer run](search-howto-run-reset-indexers.md) after completion. 

```
POST https://{service}.search.windows.net/indexers/{indexer}/resync?api-version=2026-05-01-preview
{
  "options": ["permissions"]
}
```

> [!IMPORTANT]
> If you change SharePoint permissions without triggering an update mechanism, the index serves stale ACL data for previously ingested files.

After indexing your data and ACLs, you can [query the index](search-query-access-control-rbac-enforcement.md).

## Related content

+ [Index SharePoint content in Azure AI Search (preview)](search-how-to-index-sharepoint-online.md)
+ [Query-time ACL enforcement](search-query-access-control-rbac-enforcement.md)
