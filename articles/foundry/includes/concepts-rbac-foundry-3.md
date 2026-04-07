---
title: Include file
description: Include file
author: sdgilley
ms.reviewer: meerakurup
ms.author: sgilley
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 03/20/2026
ms.custom: include
---

## Create custom roles for projects

If the built-in roles don't meet your enterprise requirements, create a custom role that allows for precise control over allowed actions and scopes. Here's an example subscription-level custom role definition:

```json
{
  "properties": {
    "roleName": "My Enterprise Foundry User",
    "description": "Custom role for Foundry at my enterprise to only allow building Agents. Assign at subscription level.",
    "assignableScopes": ["/subscriptions/<your-subscription-id>"],
    "permissions": [ { 
        "actions": ["Microsoft.CognitiveServices/*/read", "Microsoft.Authorization/*/read", "Microsoft.CognitiveServices/accounts/listkeys/action","Microsoft.Resources/deployments/*"], 
        "notActions": [], 
        "dataActions": ["Microsoft.CognitiveServices/accounts/AIServices/agents/*"], 
        "notDataActions": []     
    } ]
  }
}
```

For more information on creating a custom role, see the following articles. 

- [Azure portal](/azure/role-based-access-control/custom-roles-portal)
- [Azure CLI](/azure/role-based-access-control/custom-roles-cli)
- [Azure PowerShell](/azure/role-based-access-control/custom-roles-powershell)
- [Disable preview features in Microsoft Foundry](../how-to/disable-preview-features.md). This article provides more details on specific permissions in Foundry across control and data plane which you can utilize when building custom roles.

## Notes and limitations

* To view and purge deleted Foundry accounts, you must have the Contributor role assigned at the subscription scope.
* Users with the Contributor role can deploy models in Foundry.
* You need the Owner role on a resource's scope to create custom roles in the resource.
* If you have permissions to role assign in Azure (for example, the Owner role assigned on the account scope) to your user principal, and you deploy a Foundry resource from the Azure portal or Foundry portal UI, then the Azure AI User role gets automatically assigned to your user principal. This assignment doesn't apply when deploying Foundry from SDK or CLI. 
* When you create a Foundry resource, the built-in role-based access control (RBAC) permissions give you access to the resource. To use resources created outside Foundry, ensure the resource has permissions that let you access it. Here are some examples: 
    * To use a new Azure Blob Storage account, add the Foundry account resource's managed identity to the Storage Blob Data Reader role on that storage account. 
    * To use a new Azure AI Search source, add Foundry to the Azure AI Search role assignments.
* To fine-tune a model in Foundry, you need both data plane and control plane permissions. Deploying a fine-tuned model is a control plane permission. Therefore, the only built-in role with both data plane and control plane permissions is the **Azure AI Owner** role. Or, if you prefer, you can also assign the **Azure AI User** role for data plane permissions and the **Azure AI Account Owner** role for control plane permissions.
