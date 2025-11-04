---
title: Use Azure AI Search indexers to ingest Microsoft Purview sensitivity labels  
titleSuffix: Azure AI Search  
description: Learn how to configure Azure AI Search indexers to ingest Microsoft Purview sensitivity labels from supported data sources for document-level security enforcement.  
ms.service: azure-ai-search  
ms.topic: how-to  
ms.date: 10/04/2025  
author: gmndrg  
ms.author: gimondra  
---

# Use Azure AI Search indexers to ingest Microsoft Purview sensitivity labels and enforce document-level security

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

Starting in the **2025-11-01-preview** REST API, Azure AI Search introduces support for ingesting and enforcing Microsoft Purview sensitivity labels at the document level.  
This feature enables organizations to align search experiences with existing information protection policies defined in Microsoft Purview.

With sensitivity label indexing, Azure AI Search can extract, store, and enforce document-level sensitivity metadata and content, enabling only authorized users to view or retrieve labeled content in search results.

This functionality is available for the following data sources:

+ [Azure Blob Storage](/azure/storage/blobs/storage-blobs-introduction)
+ [Azure Data Lake Storage Gen2](/azure/storage/blobs/data-lake-storage-introduction)
+ [SharePoint Online](/sharepoint/overview)
+ [OneLake (Microsoft Fabric)](/fabric/onelake/overview)

> [!IMPORTANT]
> The feature is available in **limited regions** and **only through the REST API or supported SDKs** during public preview.  
> Portal configuration and debug mode for administrators are not supported at this time.


### Sensitivity label and document content ingestion

When enabled, Azure AI Search indexers automatically extract Microsoft Purview sensitivity labels from supported file formats (Word, Excel, PowerPoint, PDF, and others) during content ingestion.  

Extracted labels are stored as metadata fields within the search index, alongside the document content.

### Policy enforcement

At query time, Azure AI Search evaluates sensitivity labels and enforces **document-level access control** in accordance with the user’s Microsoft Entra ID token and Purview label policies.  

Only users authorized to access content under a given label can retrieve corresponding documents in search results. Note that there is a delay in how often the labels are pulled from a document after changed. When configured on a schedule, the indexer will pull the new documents and associated sensitivity labels and any changes in document content and its associated sensitivity labels if changed since the last run.


## Prerequisites

+ **Microsoft Purview sensitivity label policies** must be configured and applied to documents before indexing.  

+ **Azure AI Search service with a managed identity** must be enabled.  
  See [Configure a managed identity - Azure AI Search](search-how-to-managed-identities.md).

+ **Global Administrator permissions** in your Microsoft Entra tenant are required to grant the search service access to Purview APIs and sensitivity labels.

+ Both the **Azure AI Search service** and end users querying the content must belong to the same **Microsoft Entra tenant**.  
  Guest users and multi-tenant scenarios are not supported during preview.

+ Access to this capability is restricted to **approved preview participants**.  
  Provide your search service name to your Microsoft program contact to enable the feature for your instance.

+ File types must be included in the [Purview sensitivity labels WXP supported formats list](/purview/sensitivity-labels-sharepoint-onedrive-files#supported-file-types) and also be recognized as [Office supported file types](search-how-to-index-azure-blob-storage.md#supported-document-formats) by Azure AI Search indexers.

---

## Limitations

+ Initial release supports **REST API and SDKs only**. There’s **no portal experience** for configuration or management.  
+ May have **undesired results when used simultaneously with ACL-based security filters** (currently also in preview).  
  It’s recommended to **test each feature independently** until official coexistence support is announced.  
+ **Autocomplete** and **Suggest** APIs are disabled for Purview-enabled indexes, as they cannot yet enforce label-based access control.  
+ **Incremental indexing** of sensitivity labels occurs automatically when a document’s label or metadata changes and is detected in a subsequent indexer run.  
+ **Guest accounts and cross-tenant queries** are not supported.


## Enable AI Search managed identity

Enable a managed identity for your Azure AI Search service.  
See [Configure a managed identity in Azure AI Search](search-how-to-managed-identities.md).

This identity is required for the indexer to securely access Microsoft Purview and extract label metadata.

## Governance and permissions approval

Access to Microsoft Purview label metadata involves highly sensitive operations, including the ability to read encrypted content and security classifications.  
For this reason, elevated permissions are required and must follow your organization’s internal governance processes.

### Follow your company’s governance model

Each organization defines its own policies and role-assignment governance.  
To enable this feature:

1. Identify the **Global Administrators** or **delegated administrators** responsible for approving tenant-level role assignments.
2. Engage your internal security or compliance teams for review and clearance before granting permissions.
3. Your Global Administrator must allow the search service managed identity to access document sensitivity labels.

Microsoft recommends following your company’s standard governance and security review process before running any of the commands in the next section.  
The following steps and scripts are provided only as implementation examples for environments that do not yet have internal governance automation in place.

## Identify your Global Administrator

If you need to determine who can authorize permissions for the search service, you can locate active or eligible Global Administrators in your Microsoft Entra tenant.

1. In the [Azure portal](https://portal.azure.com), search for **Microsoft Entra ID**.  
1. In the left navigation pane, select **Manage > Roles and administrators**.  
1. Search for the **Global Administrator** role and select it.  
1. Under **Eligible assignments** and **Active assignments**, review the list of administrators authorized to run the permissions setup process.

Contact one of these administrators to initiate the approval and run the PowerShell configuration.


## Grant search service permissions to extract sensitivity labels

Once governance approval is obtained, the Global Administrator can grant the necessary permissions to the Azure AI Search managed identity.  
This step enables the indexer to extract all label and permission metadata and decrypt labeled content where authorized.

The managed identity must be granted:

- **Content.SuperUser** – for label and content extraction  
- **UnifiedPolicy.Tenant.Read** – for Purview policy and label metadata access
  
### PowerShell example

Run the following commands in an elevated administrator PowerShell session. Change the resourceIdWithManagedIdentity variable and substitute with your search service information. 

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

The appID roles above are associated to the following Azure roles:

| AppID                                  | Service Principal                      | 
| -------------------------------------- | -------------------------------------- | 
| `870c4f2e-85b6-4d43-bdda-6ed9a579b725` | Microsoft Info Protection Sync Service | 
| `00000012-0000-0000-c000-000000000000` | Azure Resource Manager SP              | 


[!NOTE]
Permissions must be granted by a Global Administrator or equivalent delegated role in your tenant.
These elevated permissions are necessary for the indexer to extract and synchronize sensitivity labels correctly.

## Configure the index to enable Purview sensitivity label 

When sensitivity label support is required, set the purviewEnabled property to true in your index definition.
This setting cannot be changed after index creation.

PUT https://{service}.search.windows.net/indexes('{indexName}')?api-version=2025-11-01-preview
{
  "purviewEnabled": true,
  "fields": [
    {
      "name": "sensitivityLabel",
      "type": "Edm.String",
      "filterable": true,
      "sensitivityLabel": true,
      "retrievable": false
    }
  ]
}


[!IMPORTANT]
When purviewEnabled is set to true, only RBAC authentication is supported for all document operations APIs.
API key access is limited to index schema retrieval (list and get).
Autocomplete and Suggest APIs are unavailable for Purview-enabled indexes.

## Configure the data source

To enable sensitivity label ingestion, configure the data source with the indexerPermissionOptions property set to ["sensitivityLabel"]. 

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


This property instructs the indexer to extract sensitivity label metadata during ingestion and attach it to the indexed document.

## Configure the indexer

Define field mappings to route extracted label metadata to the index fields.
If your data source emits label metadata under a different field name (for example, metadata_sensitivity_label), map it explicitly.

{
  "fieldMappings": [
    {
      "sourceFieldName": "metadata_sensitivity_label",
      "targetFieldName": "sensitivityLabel"
    }
  ]
}

- If your indexer has a skillset and you're implementing data chunking through split skill, you must ensure you also map the property to each chunk via index projections:

<ADD INDEX PROJECTIONS CODE>

- Put your indexer on a schedule the indexer to crawl your data source and extract labels.

- Changes to document sensitivity labels are picked up automatically by the indexer when the document’s LastModified timestamp changes due to a sensitivity label change and the next scheduled indexer run occurs.


## Recommendations and best practices

- Test the sensitivity label feature and ACL permission filters separately until coexistence support is officially announced.

- Always use managed identities for connections; API keys are not supported for Purview-enabled indexes.

- Use RBAC-based query authorization for all search operations.

- Schedule regular indexer runs to keep sensitivity label metadata synchronized with your data sources.

- Avoid enabling retrievable on the sensitivityLabel field in production environments.

## Next steps

[How to query a sensitivity labels-enabled index](Add article.md)
[Document-level security in Azure AI Search](Add article.md)
