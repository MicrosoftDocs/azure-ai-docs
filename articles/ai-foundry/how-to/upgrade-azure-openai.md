---
title: Upgrade from Azure OpenAI to Azure AI Foundry 
titleSuffix: Azure AI Foundry
description: Upgrade seamlessly from Azure OpenAI to Azure AI Foundry and unlock advanced capabilities like a broader model catalog, agents service, and evaluation tools.
ms.author: sgilley
author: sdgilley
ms.reviewer: deeikele
ms.date: 10/01/2025
ms.service: azure-ai-foundry
ms.topic: how-to
---

# Upgrade from Azure OpenAI to Azure AI Foundry

The Azure AI Foundry resource type offers a superset of capabilities compared to the Azure OpenAI resource type. It enables access to a broader model catalog, agents service, and evaluation capabilities.

An upgrade option is available to convert your Azure OpenAI resource to an Azure AI Foundry resource. You keep your existing Azure OpenAI API endpoint, state of work, and security configurations, and don't need to create a new Azure AI Foundry resource.

## Benefits of upgrading

Upgrading your Azure OpenAI resource to an Azure AI Foundry resource unlocks the following capabilities.

|Feature|Azure OpenAI|Azure AI Foundry|
|---|---|---|
| Models sold directly by Azure | Azure OpenAI only | Azure OpenAI, Black Forest Labs, DeepSeek, Meta, xAI, Mistral, Microsoft  |
| Partner & Community Models sold through Marketplace - Stability, Bria, Cohere, etc.|  | ✅ |
| Azure OpenAI API (batch, stored completions, fine-tuning, evaluation, etc.) | ✅ | ✅ |
| Agent service | | ✅ |
| Azure Foundry API |  | ✅ |
| AI Services (Speech, Vision, Language, Content Understanding) | | ✅ |

Your existing resource configurations and state remain preserved including:

* Resource name
* Azure resource tags
* Network configurations
* Access and identity configurations
* API endpoint and API key
* Custom Domain Name
* Existing state including fine-tuning jobs, batch, stored completions, etc.

## Limitations

Backend limitations:

* Azure OpenAI resources using **customer-managed keys** for encryption are available for upgrade by request only. [Fill out the request form here](https://forms.office.com/r/sKGZJ0YhDd).
* The AI Foundry resource type doesn't support configuring Weights & Biases.
* Private network setups require [reconfiguration of private link endpoints and extra DNS configurations](#private-network-configuration) before all Foundry capabilities can be used.

Foundry portal limitations:

* The evaluations view doesn't yet support all the capabilities available in the Azure OpenAI evaluations view.

## Support level post-upgrade 

The upgrade converts your Azure OpenAI resource type to Azure AI Foundry resource type. Both services are generally available and supported before and after the upgrade. Upgrading your Azure OpenAI resource is an opt-in capability. If needed, you can [roll back to your previous setup](#roll-back-to-azure-openai).

## How to upgrade

As a prerequisite to upgrade, managed identity must be enabled on your Azure OpenAI resource. Upgrade can be completed via the Azure AI Foundry portal, or using Azure Bicep or Resource Manager templates (recommended for resource configurations with custom security settings).

# [Foundry portal](#tab/portal)

**Option 1: Use Azure AI Foundry portal**

1. Sign in to [Azure AI Foundry](https://ai.azure.com/?cid=learnDocs).
1. Select your Azure OpenAI resource.
1. On the overview page, find the banner **Make the switch to AI Foundry** and select **Switch now.**
1. Provide the name for your first project. A project is a folder to organize your work in Azure AI Foundry. Your first 'default' project has backwards compatibility with your previous work in Azure OpenAI.
1. Confirm to start the upgrade. The upgrade takes up to two minutes.

# [Azure Bicep](#tab/bicep)

**Option 2: Use an Azure Bicep template**

Starting with your existing Azure OpenAI template configuration, set the following properties:

* Update kind from value 'OpenAI' => 'AIServices'
* Set allowProjectManagement: True
* Configure managed identity

Sample configuration:

```bicep
resource aiFoundry 'Microsoft.CognitiveServices/accounts@2025-06-01' = {
    name: aiFoundryName // Your existing resource name
    location: location
    identity: {
        type: 'SystemAssigned'
    }
    sku: {
        name: 'S0'
    }
    kind: 'AIServices' // Update from 'OpenAI'
    properties: {
        // required to work in AI Foundry
        allowProjectManagement: true 

        // Needed for capabilities that require EntraID authentication
        customSubDomainName: aiFoundryName
        disableLocalAuth: true
    }
}
```

Run the template using [Azure Bicep CLI](/azure/azure-resource-manager/bicep/bicep-cli) or your [Visual Studio Code extension for Bicep](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-bicep) as a patch operation on your current resource.

---

## UX navigation differences after upgrading

After upgrading from Azure OpenAI to Azure AI Foundry, you'll notice updates to the portal’s navigation and feature access:

1. **Updated left-side navigation**
   
   The left-hand menu is reorganized to consolidate playgrounds, including Assistants, under a single landing page, streamlining access to experimentation environments. You find access to new features including Agent service and Content Understanding.

   An *Azure OpenAI section* provides access to features that are exclusively used with Azure OpenAI models.

   > [!NOTE]
   > Not all Foundry tools are visible by default in the left side navigation, which is customizable. Select '... More' to locate them.

1. **Your default view is now a project**

   Projects are folders to organize your work in Foundry. They're also a container for access management and data isolation. Multiple can be created as part of your AI Foundry resource, so you can separate your work between use cases that you're working on. The first project after upgrade has access to your previous work in Azure OpenAI.

1. **Broader set of models in model catalog**
   
   Your model catalog now includes more models that can be directly deployed using your Azure AI Foundry resource. 

1. **Developer endpoints**

   Your project overview page includes your previous Azure OpenAI endpoint, and a new Azure AI Foundry endpoint. Foundry API and SDK grant access to the broader set of models and features including agent service.

## Understanding pricing

There are no pricing differences for existing Azure OpenAI functionality when upgrading to Azure AI Foundry—your current usage patterns and costs remain unchanged. However, Azure AI Foundry unlocks access to more features such as expanded model catalogs, agent services, and evaluation tools, which may have their own pricing structures depending on the models and services used.

For estimating costs of new features available in Azure AI Foundry, use the [Azure Pricing Calculator](https://azure.microsoft.com/pricing/calculator/).

## Private network configuration

AI Foundry resource is a superset of Azure OpenAI resource and its capabilities are exposed over three FQDNs:

- {custom-domain}.openai.azure.com
- {custom-domain}.services.ai.azure.com
- {custom-domain}.cognitiveservices.azure.com

Your DNS configuration must be able to resolve each of the above FQDNs in order to use the full set of Foundry capabilities. 

* If you're using Azure DNS, you need to create an [Azure DNS Zone](/azure/dns/dns-zones-records) for each of the above domains.

* If you're using a custom DNS implementation, you need to implement a conditional forwarder for each of the above configurations. 

After this, delete and [re-create a private link endpoint](configure-private-link.md) on your resource. Your private link endpoint creates an IP address in your Azure Virtual Network to map to each endpoint.

> [!IMPORTANT] 
> When upgrading to Azure AI Foundry, you must recreate your private link endpoint, for the "services.ai.azure.com" and "{custom-domain}.cognitiveservices.azure.com" IP configurations to be created.

## Roll back to Azure OpenAI

In case you run into any issues, a rollback option is available. As prerequisite to rollback, you're required to delete any of the following configurations first:

* Projects
* Connections
* Non-Azure OpenAI model deployments

Then, use either AI Foundry Portal or ARM template to roll back:

# [Foundry portal](#tab/portal)

**Option 1: Use Azure AI Foundry portal**

1. Navigate to management center in the left bottom of your screen.
1. On your resource overview page, find the rollback option.
1. Select **Rollback**.

:::image type="content" source="../media/upgrade-azure-openai/rollback.png" alt-text="Screenshot shows the roll back option in the Azure AI Foundry portal." lightbox = "../media/upgrade-azure-openai/rollback.png":::

# [Azure Bicep](#tab/bicep)

**Option 2: Use an Azure Bicep template**
  
To roll back, convert your template configuration back to 'OpenAI' as kind.

  ```bicep
  resource aiFoundry 'Microsoft.CognitiveServices/accounts@2025-06-01' = {
  name: aiFoundryName
  location: location
  identity: {
      type: 'SystemAssigned'
  }
  sku: {
      name: 'S0'
  }
  kind: 'OpenAI'
  properties: {

      // Defines developer API endpoint subdomain
      customSubDomainName: aiFoundryName
      disableLocalAuth: true
  }
  ```

  Run the template using [Azure Bicep CLI](/azure/azure-resource-manager/bicep/bicep-cli) or your [Visual Studio Code extension for Bicep](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-bicep) as a patch operation on your current resource.


---

## Troubleshooting Common Issues

Azure resource limits and organizational configurations may require extra steps to complete the upgrade. The table below outlines some of the most common issues along with recommended solutions to help troubleshooting.

|Issue|Solution/mitigation|
|---|---|
|User principal lacks account/write permissions|Obtain a privileged Azure RBAC role to manage top-level Azure resources, e.g. Owner, Contributor, Azure AI Administrator.| 
|Managed identity isn't enabled on the Azure OpenAI resource|Configure managed identity on your resource via templates or Azure portal.|
|No permissions to create agents, while you're the owner/contributor on the resource.|An EntraID data plane role is required for development actions including agents. Examples include Azure AI User or Azure AI Project Manager role. Owner and Contributor roles only grant access to management operations in Azure such as managing deployments.|
|An Azure Policy conflict occurred.|Your organization may have put constraints on resource configurations. Inspect the details of the policy violation error. Then upgrade your resource via template options for further customization. For example, network configurations for Agents can only be configured via template options such as Azure Bicep.|
|Exceeded number of Azure OpenAI instances of 30 per subscription per region when rolling back.|Delete an Azure OpenAI resource or upgrade it to the Azure AI Foundry. Then retry rolling back your current resource.|
|Exceeded number of AIServices instances of 100 per subscription per region.|Delete an Azure AI Foundry resource you may not use in this subscription. Then retry upgrading your current resource.|
|I can't access my resource over the private network|See [private networking configuration](#private-network-configuration) for the required steps.|

## How to inspect whether a resource has been upgraded

The following Azure resource property is available to inspect whether a resource was previously upgraded to AI Foundry.

```bicep
{
  {
    // Read only properties if your resource was upgraded:
    previouskind: "OpenAI"
  }
}
```

Not sure who upgraded your resource to Azure AI Foundry? You can [view the activity log in the Azure portal](/azure/azure-monitor/platform/activity-log-insights#view-the-activity-log) to understand when the upgrade operation took place and by which user:

1. Use Azure Activity Logs (under "Monitoring") to see if an upgrade operation was performed.
1. Filter by "Write" operations on the storage account.
1. Look for operations listed as `Microsoft.CognitiveServices/accounts/write`.

## Related content

* [Choose an Azure resource type for AI foundry](../concepts/resource-types.md)
* [Bicep samples for Azure AI Foundry common infrastructure configurations](https://github.com/azure-ai-foundry/foundry-samples/tree/main/samples/microsoft/infrastructure-setup)
