---
title: Use Azure AI Search indexers to ingest Microsoft Purview sensitivity labels  
titleSuffix: Azure AI Search  
description: Learn how to configure Azure AI Search indexers to ingest Microsoft Purview sensitivity labels from supported data sources for document-level security enforcement.  
ms.service: azure-ai-search  
ms.topic: how-to  
ms.date: 10/05/2025  
author: gmndrg  
ms.author: gimondra  
---

# Use Azure AI Search indexers to ingest Microsoft Purview sensitivity labels and enforce document-level security

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

Azure AI Search now supports automatic extraction of [Microsoft Purview sensitivity labels](/purview/sensitivity-labels) at document-level during indexing, with label-based access control enforced at query time. Available in public preview, this feature enables organizations to align search experiences with existing [information protection policies](/purview/create-sensitivity-labels) defined in Microsoft Purview.

With sensitivity label indexing, Azure AI Search can extract, store, and enforce document-level sensitivity metadata and content, enabling only authorized users to view or retrieve labeled content in search results.

This functionality is available for the following data sources:

+ [Azure Blob Storage](search-how-to-index-azure-blob-storage.md)
+ [Azure Data Lake Storage Gen2](search-how-to-index-azure-data-lake-storage.md)
+ [SharePoint in Microsoft 365 (Preview)](search-how-to-index-sharepoint-online.md)
+ [Microsoft OneLake](search-how-to-index-onelake-files.md)

> [!IMPORTANT]
> The feature is available in **limited regions** and only through the [REST API version 2025-11-01-preview](/rest/api/searchservice/operation-groups?view=rest-searchservice-2025-11-01-preview&preserve-view=true) or supported beta SDKs during public preview.  
> Portal configuration and debug mode for administrators are not supported at this time.


### Policy enforcement

At query time, Azure AI Search evaluates sensitivity labels and enforces [document-level access control](search-document-level-access-overview.md) in accordance with the user’s Microsoft Entra ID token and Purview label policies.  

Only users authorized to access content with [extract usage right](/purview/rights-management-usage-rights) under a given label can retrieve corresponding documents in search results. Note that there is a delay in how often the labels are pulled from a document after changed. When configured [on a schedule](search-howto-schedule-indexers.md), the indexer will pull the new documents and associated sensitivity labels and any changes in document content and its associated sensitivity labels if changed since the last run.


## Prerequisites

+ [Microsoft Purview sensitivity label policies](/purview/create-sensitivity-labels) must be configured and [applied to documents](/purview/sensitivity-labels) before indexing.  

+ [Global Administrator](/entra/identity/role-based-access-control/permissions-reference#global-administrator) or [Privileged Role Administrator](/entra/identity/role-based-access-control/permissions-reference#privileged-role-administrator) roles in your Microsoft Entra tenant are required to grant the search service access to Purview APIs and sensitivity labels.

+ Both the Azure AI Search service and end users querying the content must belong to the same Microsoft Entra tenant. Guest users and multi-tenant scenarios are not supported.

+ File types must be included in the [Purview sensitivity labels WXP supported formats list](/purview/sensitivity-labels-sharepoint-onedrive-files#supported-file-types) and also be recognized as [Office supported file types](search-how-to-index-azure-blob-storage.md#supported-document-formats) by Azure AI Search indexers.


## Limitations

+ Initial release supports REST API version 2025-11-01-preview and associated beta SDKs only. There’s no portal experience for configuration or management.  
+ This feature is not supported when used simultaneously with [ACL-based security filters](search-query-access-control-rbac-enforcement.md) (currently also in preview). It’s advised to test each feature independently until official coexistence support is announced.  
+ [Autocomplete](/rest/api/searchservice/documents/autocomplete-post) and [Suggest](/rest/api/searchservice/documents/suggest-post) APIs are disabled for Purview-enabled indexes, as they cannot yet enforce label-based access control.  
+ Guest accounts and cross-tenant queries are not supported.
+ In the initial release, unlabeled documents are not supported in sensitivity label-enabled indexes and will not be returned in query results. Support for both labeled and unlabeled documents with the same index will be announced and documented once available.

The following steps must be followed in order to configure sensitivity label sync in Azure AI Search.

## 1 - Enable AI Search managed identity

Enable a [system-assigned managed identity for your Azure AI Search service](search-how-to-managed-identities.md).  This identity is required for the indexer to securely access Microsoft Purview and extract label metadata.

## 2 - Enable RBAC on your AI Search service

[Enable a role-based access control (RBAC)](search-security-enable-roles.md) on your Azure AI Search service. It's recommended that both, RBAC and API keys, are kept to avoid disrupting any operations using API keys. This step is required so content-related operations such as indexing content and query the index succeed. 

## 3 - Granting access to extract sensitivity labels

Accessing Microsoft Purview sensitivity label metadata involves highly privileged operations, including reading encrypted content and security classifications. To enable this capability in Azure AI Search, you must grant specific roles to the service’s managed identity—following your organization’s internal governance and approval processes.


### Identify your Global or Priviledge Role Administrators

If you need to determine who can authorize permissions for the search service, you can locate active or eligible Global Administrators in your Microsoft Entra tenant.

1. In the [Azure portal](https://portal.azure.com), search for **Microsoft Entra ID**.

   ::image type="content" source="media/search-indexer-sensitivity-labels/search-microsoft-entra-id.png" alt-text="Screenshot of the search action for Microsoft Entra product." lightbox="media/search-indexer-sensitivity-labels/search-microsoft-entra-id.png":::
   
1. In the left navigation pane, select **Manage > Roles and administrators**.

   ::image type="content" source="media/search-indexer-sensitivity-labels/entra-id-roles-and-administrators.png" alt-text="Screenshot of the Entra roles and administrators page." lightbox="media/search-indexer-sensitivity-labels/entra-id-roles-and-administrators.png":::
   
1. Search for the **Global Administrator** or **Privileged Role Administrator**  role and select it.

   ::image type="content" source="media/search-indexer-sensitivity-labels/global-administrator-role.png" alt-text="Screenshot of the selection of global administrator role." lightbox="media/search-indexer-sensitivity-labels/global-administrator-role.png":::
   
1. Under **Eligible assignments** and **Active assignments**, review the list of administrators authorized to run the permissions setup process.

   ::image type="content" source="media/search-indexer-sensitivity-labels/role-eligible-assignments-and-active-assignments.png" alt-text="Screenshot of role eligible and active assignments." lightbox="media/search-indexer-sensitivity-labels/role-eligible-assignments-and-active-assignments.png":::

### Secure Governance Approval
Engage your internal security or compliance teams to review the request. Microsoft recommends following your company’s standard governance and security review process before proceeding with any role assignments.

Once approved, a Global Administrator or Privileged Role Administrator must assign the following roles to the Azure AI Search system-assigned managed identity:
- **Content.SuperUser** – for label and content extraction
- **UnifiedPolicy.Tenant.Read** – for Purview policy and label metadata acces

  
### Assign Roles via PowerShell

Your Global Administrator or Priviledged Role Administrator should use the following PowerShell script to grant the required permissions. Replace the placeholder values with your actual subscription, resource group, and search service names.

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

The appID roles above are associated to the following Azure roles:

| AppID                                  | Service Principal                      | 
| -------------------------------------- | -------------------------------------- | 
| `870c4f2e-85b6-4d43-bdda-6ed9a579b725` | Microsoft Info Protection Sync Service | 
| `00000012-0000-0000-c000-000000000000` | Azure Resource Manager SP              | 



## 4 - Configure the index to enable Purview sensitivity label 

When sensitivity label support is required, set the purviewEnabled property to true in your index definition.
> [!IMPORTANT]
> **purviewEnabled** property must be set to true when the index is created. This setting is permanent and cannot be modified later.
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

## 5 - Configure the data source

To enable sensitivity label ingestion, configure the data source with the indexerPermissionOptions property set to ["sensitivityLabel"]. 

```
{
  "name": "purview-sensitivity-datasource",
  "type": "azureblob", // < adjust type value according to the data source you are enabling this for: sharepoint, onelake, adlsgen2.
  "indexerPermissionOptions": [ "sensitivityLabel" ],
  "credentials": {
    "connectionString": "ResourceId=/subscriptions/<subscriptionId>/resourceGroups/<resourceGroupName>/providers/Microsoft.Storage/storageAccounts/<storageAccountName>/;"
  },
  "container": {
    "name": "<container-name>"
  }
}
```

The `indexerPermissionOptions` property instructs the indexer to extract sensitivity label metadata during ingestion and attach it to the indexed document.

## 6 - Configure the indexer

- Define field mappings to route extracted label metadata to the index fields.
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

- Sensitivity label updates are indexed automatically when changes to a document’s label, content, or metadata are detected during a scheduled indexer run. [Configure the indexer on a recurring schedule](search-howto-schedule-indexers.md). The minimum supported interval is every 5 minutes. 


### Configure index projections in your skillset

If your indexer has a skillset and you're implementing data chunking through [split skill](cognitive-search-skill-textsplit.md), you must ensure you also map the property to each chunk via index projections:

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

## Next steps

[How to query a sensitivity labels-enabled index](search-query-sensitivity-labels.md)
[Document-level security in Azure AI Search](search-document-level-access-overview.md)
