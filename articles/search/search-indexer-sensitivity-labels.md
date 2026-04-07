---
title: Use Indexers to Ingest Microsoft Purview Sensitivity Labels
description: Learn how to configure Azure AI Search indexers to ingest Microsoft Purview sensitivity labels from supported data sources for document-level security enforcement.
ms.reviewer: gimondra
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 03/05/2026
---

# Use an Azure AI Search indexer to ingest Microsoft Purview sensitivity labels and enforce document-level security

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

Azure AI Search now supports automatic extraction of [Microsoft Purview sensitivity labels](/purview/sensitivity-labels) at document-level during indexing, with label-based access control enforced at query time. Available in public preview, this feature enables organizations to align search experiences with existing [information protection policies](/purview/create-sensitivity-labels) defined in Microsoft Purview.

With sensitivity label indexing, Azure AI Search extracts and stores metadata that describes each document's sensitivity level. It also enforces label-based access control, ensuring that only authorized users can view or retrieve labeled content in search results.

This functionality is available for the following data sources:

+ [Azure Blob Storage](search-how-to-index-azure-blob-storage.md)
+ [Azure Data Lake Storage Gen2](search-how-to-index-azure-data-lake-storage.md)
+ [SharePoint in Microsoft 365 (Preview)](search-how-to-index-sharepoint-online.md)
+ [Microsoft OneLake](search-how-to-index-onelake-files.md)

:::image type="content" source="media/search-indexer-sensitivity-labels/sensitivity-label-rag-architecture.png" alt-text="Architecture diagram showing a governed RAG solution where documents labeled with Microsoft Purview sensitivity labels are indexed into Azure AI Search, and a RAG orchestrator filters query results by label so junior users see only General content while executive users see General, Confidential, and Highly Confidential content." lightbox="media/search-indexer-sensitivity-labels/sensitivity-label-rag-architecture.png":::

## Prerequisites

+ [Microsoft Purview sensitivity label policies](/purview/create-sensitivity-labels) must be configured and [applied to documents](/purview/sensitivity-labels) before indexing.

+ [Global Administrator](/entra/identity/role-based-access-control/permissions-reference#global-administrator) or [Privileged Role Administrator](/entra/identity/role-based-access-control/permissions-reference#privileged-role-administrator) roles in your Microsoft Entra tenant are required to grant the search service access to Purview APIs and sensitivity labels.

+ Both the Azure AI Search service and the user issuing the query must be in the same Microsoft Entra tenant.

+ Source documents must use file types that are both [supported by Purview sensitivity labels](/purview/sensitivity-labels-sharepoint-onedrive-files#supported-file-types) and [supported by Azure AI Search indexers](search-how-to-index-azure-blob-storage.md#supported-document-formats).

+ REST API version 2025-11-01-preview or an equivalent preview SDK package.

## Limitations

+ The Azure portal doesn't support this feature.

+ [Autocomplete](/rest/api/searchservice/documents/autocomplete-post) and [Suggest](/rest/api/searchservice/documents/suggest-post) APIs aren't supported for Purview-enabled indexes, as they can't yet enforce label-based access control.

+ [Guest accounts](/entra/external-id/b2b-quickstart-add-guest-users-portal) and cross-tenant queries aren't supported.

+ The following indexer features don't support documents with sensitivity labels. If you use any of these features in a skillset or indexer, documents with sensitivity labels aren't processed.

  + [Custom Web API skill](cognitive-search-custom-skill-web-api.md)

  + [GenAI Prompt skill](cognitive-search-skill-genai-prompt.md)

  + [Knowledge store](knowledge-store-concept-intro.md)

  + [Indexer enrichment cache](enrichment-cache-how-to-configure.md)
  
  + [Debug sessions](cognitive-search-debug-session.md)

## How policy enforcement works

Sensitivity label support has two phases: indexing and query-time enforcement.

### Indexing

When configured [on a schedule](search-howto-schedule-indexers.md), the indexer pulls new documents and updates from the data source. For each document, it captures:

- Document content
- The associated sensitivity label
- Changes to content or labels since the last indexer run

> [!NOTE]
> There might be a delay between when a label changes on a document and when the indexer detects the update.

### Query-time enforcement

At query time, Azure AI Search evaluates sensitivity labels and enforces [document-level access control](search-document-level-access-overview.md) based on the user's Microsoft Entra ID token and Microsoft Purview label policies. Only users authorized to access content with [READ usage right](/purview/rights-management-usage-rights) under a given label can retrieve corresponding documents in search results.

### End-to-end example

The following images show how sensitivity labels flow from authoring to the search experience. In the first image, a user applies the **Confidential** label to a document in Microsoft Word. In the second image, an enterprise chatbot enforces that label at query time, blocking copy and share actions for confidential content.

:::image type="content" source="media/search-indexer-sensitivity-labels/word-sensitivity-label-menu.jpg" alt-text="Screenshot of the Microsoft Word Sensitivity menu showing a label hierarchy including Non-Business, Public, General, Confidential with sublabels such as Project Obsidian and Recipients Only, and Highly Confidential, with the Confidential label currently applied to the document." lightbox="media/search-indexer-sensitivity-labels/word-sensitivity-label-menu.jpg":::

:::image type="content" source="media/search-indexer-sensitivity-labels/chatbot-sensitivity-label-enforcement.png" alt-text="Screenshot of a Contoso enterprise chatbot displaying a policy-aware response with numbered citations, a Confidential Project Obsidian sensitivity label banner, blocked copy and share actions, and per-document sensitivity labels shown in the references panel." lightbox="media/search-indexer-sensitivity-labels/chatbot-sensitivity-label-enforcement.png":::

## 1. Enable AI Search managed identity

Enable a [system-assigned managed identity for your Azure AI Search service](search-how-to-managed-identities.md).  This identity is required for the indexer to securely access Microsoft Purview and extract label metadata.

## 2. Enable RBAC on your AI Search service

[Enable a role-based access control (RBAC)](search-security-enable-roles.md) on your Azure AI Search service. This step is required so content-related operations such as indexing content and querying the index succeed. Keep both RBAC and API keys to avoid disrupting operations that rely on API keys. 

## 3. Grant access to extract sensitivity labels

Accessing Microsoft Purview sensitivity label metadata involves highly privileged operations, including reading encrypted content and security classifications. To enable this capability in Azure AI Search, you must grant specific roles to the service's managed identity—following your organization's internal governance and approval processes.


### Identify your global or privileged role administrators

If you need to determine who can authorize permissions for the search service, you can locate active or eligible Global Administrators in your Microsoft Entra tenant.

1. In the [Azure portal](https://portal.azure.com), search for **Microsoft Entra ID**.

   :::image type="content" source="media/search-indexer-sensitivity-labels/search-microsoft-entra-id.png" alt-text="Screenshot of the search action for Microsoft Entra product." lightbox="media/search-indexer-sensitivity-labels/search-microsoft-entra-id.png":::
   
1. In the left navigation pane, select **Manage > Roles and administrators**.

   :::image type="content" source="media/search-indexer-sensitivity-labels/entra-id-roles-and-administrators.png" alt-text="Screenshot of the Entra roles and administrators page." lightbox="media/search-indexer-sensitivity-labels/entra-id-roles-and-administrators.png":::
   
1. Search for the **Global Administrator** or **Privileged Role Administrator**  role and select it.

   :::image type="content" source="media/search-indexer-sensitivity-labels/global-administrator-role.png" alt-text="Screenshot of the selection of global administrator role." lightbox="media/search-indexer-sensitivity-labels/global-administrator-role.png":::
   
1. Under **Eligible assignments** and **Active assignments**, review the list of administrators authorized to run the permissions setup process.

   :::image type="content" source="media/search-indexer-sensitivity-labels/role-eligible-assignments-and-active-assignments.png" alt-text="Screenshot of role eligible and active assignments." lightbox="media/search-indexer-sensitivity-labels/role-eligible-assignments-and-active-assignments.png":::

### Secure governance approval
Engage your internal security or compliance teams to review the request. Microsoft recommends following your company's standard governance and security review process before proceeding with any role assignments.

Once approved, a Global Administrator or Privileged Role Administrator must assign the following roles to the Azure AI Search system-assigned managed identity:
- **Content.SuperUser** – for label and content extraction
- **UnifiedPolicy.Tenant.Read** – for Purview policy and label metadata access

  
### Assign roles via PowerShell

Your Global Administrator or Privileged Role Administrator should use the following PowerShell script to grant the required permissions. Replace the placeholder values with your actual subscription, resource group, and search service names.

```powershell
Install-Module -Name Az -Scope CurrentUser
Install-Module -Name Microsoft.Entra -AllowClobber
Import-Module Az.Resources
Connect-Entra -Scopes 'Application.ReadWrite.All'

$resourceIdWithManagedIdentity = "subscriptions/<subscriptionId>/resourceGroups/<resourceGroup>/providers/Microsoft.Search/searchServices/<searchServiceName>"
$managedIdentityObjectId = (Get-AzResource -ResourceId $resourceIdWithManagedIdentity).Identity.PrincipalId

# Microsoft Information Protection (MIP)
$MIPResourceSP = Get-EntraServicePrincipal -Filter "appID eq '870c4f2e-85b6-4d43-bdda-6ed9a579b725'"
New-EntraServicePrincipalAppRoleAssignment -ServicePrincipalId $managedIdentityObjectId -Principal $managedIdentityObjectId -ResourceId $MIPResourceSP.Id -Id "8b2071cd-015a-4025-8052-1c0dba2d3f64"

# ARM Service Principal for policy read
$ARMSResourceSP = Get-EntraServicePrincipal -Filter "appID eq '00000012-0000-0000-c000-000000000000'"
New-EntraServicePrincipalAppRoleAssignment -ServicePrincipalId $managedIdentityObjectId -Principal $managedIdentityObjectId -ResourceId $ARMSResourceSP.Id -Id "7347eb49-7a1a-43c5-8eac-a5cd1d1c7cf0"

```

The appID roles in the provided PowerShell script are associated to the following Azure roles:

| AppID                                  | Service Principal                      | 
| -------------------------------------- | -------------------------------------- | 
| `870c4f2e-85b6-4d43-bdda-6ed9a579b725` | Microsoft Info Protection Sync Service | 
| `00000012-0000-0000-c000-000000000000` | Azure Resource Manager            | 



## 4. Configure the index to enable Purview sensitivity label 

When sensitivity label support is required, set the purviewEnabled property to true in your [index definition](/rest/api/searchservice/indexes/create-or-update?view=rest-searchservice-2025-11-01-preview&preserve-view=true).
> [!IMPORTANT]
> **purviewEnabled** property must be set to true when the index is created. This setting is permanent and can't be modified later.
> When **purviewEnabled** is set to true, only RBAC authentication is supported for all document operations APIs.
API key access is limited to index schema retrieval (list and get).

```
PUT https://{service}.search.windows.net/indexes('{indexName}')?api-version=2025-11-01-preview
{
  "purviewEnabled": true,
  "fields": [
    {
      "name": "sensitivityLabel",
      "type": "Edm.String",
      "filterable": true,
      "sensitivityLabel": true,
      "retrievable": true
    }
  ]
}
```

## 5. Configure the data source

To enable sensitivity label ingestion, configure the [data source](/rest/api/searchservice/data-sources/create-or-update?view=rest-searchservice-2025-11-01-preview&preserve-view=true) with the indexerPermissionOptions property set to ["sensitivityLabel"]. 

```
{
  "name": "purview-sensitivity-datasource",
  "type": "azureblob", // < adjust type value according to the data source you are enabling this for: sharepoint, onelake, adlsgen2.
  "indexerPermissionOptions": [ "sensitivityLabel" ],
  "credentials": {
    "connectionString": <your-connection-string>;"
  },
  "container": {
    "name": "<container-name>"
  }
}
```

The `indexerPermissionOptions` property instructs the indexer to extract sensitivity label metadata during ingestion and attach it to the indexed document.

## 6. Configure index projections in your skillset (if applicable)

If your indexer has a [skillset](cognitive-search-working-with-skillsets.md) and you're implementing data chunking through [split skill](cognitive-search-skill-textsplit.md), for example, if you have integrated vectorization, you must ensure you also map the sensitivity label to each chunk via [index projections in the skillset](/rest/api/searchservice/skillsets/create-or-update?view=rest-searchservice-2025-11-01-preview&preserve-view=true).

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
          { "name": "sensitivityLabel",  "source": "/document/metadata_sensitivity_label" } // <-- parent → child
        ]
      }
    ],
    "parameters": {
      "projectionMode": "skipIndexingParentDocuments"
    }
  }
}

```

## 7. Configure the indexer

- Define field mappings in your [indexer definition](/rest/api/searchservice/indexers/create-or-update?view=rest-searchservice-2025-11-01-preview&preserve-view=true) to route extracted label metadata to the index fields.
If your data source emits label metadata under a different field name (for example, metadata_sensitivity_label), map it explicitly.

```
{
  "fieldMappings": [
    {
      "sourceFieldName": "metadata_sensitivity_label",
      "targetFieldName": "sensitivityLabel"
    }
  ]
}
```

- Sensitivity label updates are indexed automatically when changes to a document's label, content, or metadata are detected during a scheduled indexer run. [Configure the indexer on a recurring schedule](search-howto-schedule-indexers.md). The minimum supported interval is every 5 minutes. 




## Next steps

[How to query a sensitivity labels-enabled index](search-query-sensitivity-labels.md)

[Document-level security in Azure AI Search](search-document-level-access-overview.md)
