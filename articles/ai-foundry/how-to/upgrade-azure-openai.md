---
title: Upgrade from Azure OpenAI to Microsoft Foundry 
titleSuffix: Microsoft Foundry
description: Upgrade seamlessly from Azure OpenAI to Microsoft Foundry and unlock advanced capabilities like a broader model catalog, agents service, and evaluation tools.
ms.author: sgilley
author: sdgilley
ms.reviewer: deeikele
ms.date: 12/23/2025
ms.service: azure-ai-foundry
ms.topic: how-to
ms.custom: dev-focus
ai-usage: ai-assisted
---

# Upgrade from Azure OpenAI to Microsoft Foundry

[!INCLUDE [classic-banner](../includes/classic-banner.md)]

The Microsoft Foundry resource type provides a superset of capabilities compared to the Azure OpenAI resource type. It gives you access to a broader model catalog, agents service, and evaluation capabilities.

You can upgrade your Azure OpenAI resource to a Foundry resource. You keep your existing Azure OpenAI API endpoint, state of work, and security configurations, and don't need to create a new Foundry resource.

## Benefits of upgrading

When you upgrade your Azure OpenAI resource to a Foundry resource, you get access to the following capabilities.

| Feature | Azure OpenAI | Foundry |
|---|---|---|
| Models sold directly by Azure | Azure OpenAI only | Azure OpenAI, Black Forest Labs, DeepSeek, Meta, xAI, Mistral, Microsoft  |
| Partner and community models sold through Marketplace - Stability, Cohere, and others |  | ✅ |
| Azure OpenAI API - batch, stored completions, fine-tuning, evaluation, and more | ✅ | ✅ |
| Agent service | | ✅ |
| Azure Foundry API |  | ✅ |
| Foundry Tools - Speech, Vision, Language, Content Understanding | | ✅ |

Your existing resource configurations and state stay the same, including:

* Resource name
* Azure resource tags
* Network configurations
* Access and identity configurations
* API endpoint and API key
* Custom Domain Name
* Existing state including fine-tuning jobs, batch, stored completions, and more

## Limitations

### Backend limitations

* Foundry model and feature availability [differs by region](../reference/region-support.md). For example, Agent Service is [available](../agents/concepts/model-region-support.md) in select regions compared to Azure OpenAI service. **Impact**: You may not have access to all new Foundry features in your region immediately after upgrade.

* Foundry resources using **customer-managed keys** for encryption are available for upgrade by request only. [Fill out the request form here](https://forms.office.com/r/sKGZJ0YhDd). **Impact**: If you use encryption with customer-managed keys, contact Microsoft before upgrading.

* The Foundry resource type doesn't support configuring Weights & Biases. **Impact**: Existing Weights & Biases integrations won't function post-upgrade.

* Private network setups require [reconfiguration of private link endpoints and extra Domain Name Server (DNS) configurations](#private-network-configuration) before all Foundry capabilities can be used. **Impact**: You must update your network configuration to access all Foundry features over private networks.

### Foundry portal limitations

* The evaluations view doesn't yet support all the capabilities available in the Azure OpenAI evaluations view. **Impact**: Some evaluation features may be unavailable in the portal.

## Support level post-upgrade 

The upgrade converts your Azure OpenAI resource type to Foundry resource type. Both services are generally available and supported before and after the upgrade. Upgrading your Azure OpenAI resource is an opt-in capability. If needed, you can [roll back to your previous setup](#roll-back-to-azure-openai).

## How to upgrade

### Prerequisites for upgrade

Before you upgrade your Azure OpenAI resource to a Foundry resource, ensure you have:

- **Azure role requirements**: You must have one of the following Azure roles on your subscription or resource group:
  - **Owner** or **Contributor** role for resource management and configuration
  - **Azure AI Administrator** role for managing AI services
  
  These roles are needed to enable managed identity and perform the upgrade operation.

- **Managed identity**: Managed identity must be enabled on your Azure OpenAI resource. If it isn't already enabled, you can enable it via the [Azure portal](https://portal.azure.com) by navigating to your resource, selecting **Identity** from the left menu, and toggling **System assigned** to **On**.

### Upgrade your resource

As a prerequisite to upgrade, managed identity must be enabled on your Azure OpenAI resource. You can complete the upgrade via the Foundry portal, Azure portal, or by using Azure Bicep or Resource Manager templates (recommended for resource configurations with custom security settings).

# [Foundry portal](#tab/portal)

1. [!INCLUDE [classic-sign-in](../includes/classic-sign-in.md)]
1. Select your Azure OpenAI resource.
1. On the overview page, find the banner **Want to try the latest industry models and Agents?** and select **Get started**.
1. Provide the name for your first project. A project is a folder to organize your work in Foundry. Your first 'default' project has backwards compatibility with your previous work in Azure OpenAI.
1. Confirm to start the upgrade.

**Success**: After the upgrade completes, you're taken to your new Foundry project. Your resource name, API endpoint, and existing configurations remain unchanged. You now have access to the broader model catalog, agent service, and Foundry Tools.

# [Azure portal](#tab/azportal)

1. Sign in to [Azure portal](https://portal.azure.com/)
1. Select your Azure OpenAI resource
1. On the overview page, locate the banner "Want to try the latest industry models and Agents?" and select **Get Started**.
1. Confirm to start the upgrade.

:::image type="content" source="../media/upgrade-azure-openai/azure-portal-upgrade.png" alt-text="Screenshot shows how to upgrade in Azure portal." lightbox="../media/upgrade-azure-openai/azure-portal-upgrade.png":::

**Success**: The upgrade completes, and you're returned to your resource overview page. Your resource type is now **Foundry** (previously **Azure OpenAI**). All existing configurations, endpoints, and API keys remain the same.

# [Azure Bicep](#tab/bicep)

Starting with your existing Azure OpenAI template configuration, set the following properties:

* Update `kind` from value `OpenAI` to `AIServices`
* Set `allowProjectManagement` to `true`
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
        // required to work in Foundry
        allowProjectManagement: true 

        // Needed for capabilities that require EntraID authentication
        customSubDomainName: aiFoundryName
        disableLocalAuth: true
    }
}
```

Run the template using [Azure Bicep CLI](/azure/azure-resource-manager/bicep/bicep-cli) or your [Visual Studio Code extension for Bicep](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-bicep) as a patch operation on your current resource.

**References**: [`Microsoft.CognitiveServices/accounts`](/azure/templates/microsoft.cognitiveservices/accounts), [Bicep CLI documentation](/azure/azure-resource-manager/bicep/bicep-cli)

**Success**: The patch operation completes with no errors. Your resource's `kind` property changes from `OpenAI` to `AIServices`, and `allowProjectManagement` is set to `true`. Your existing endpoint, API keys, and configurations are preserved.

---

## Portal navigation differences after upgrading

After upgrading from Azure OpenAI to Foundry, you see updates to the portal's navigation and feature access:

* **Updated left-side navigation**
   
   The portal reorganizes the left-hand menu to consolidate playgrounds, including Assistants, under a single landing page. This change streamlines access to experimentation environments. You find access to new features including Agent Service and Content Understanding.

   An *Azure OpenAI section* provides access to features that you exclusively use with Azure OpenAI models.

   > [!NOTE]
   > The portal doesn't show all Foundry tools by default in the left side navigation. The navigation is customizable. Select *... More* to locate them.

* **Your default view is now a project**

   Projects are folders to organize your work in Foundry. They're also a container for access management and data isolation. You can create multiple projects as part of your Foundry resource, so you can separate your work between use cases that you're working on. Your first project after upgrade has access to your previous work in Azure OpenAI.

* **Broader set of models in model catalog**
   
   Your model catalog now includes more models that you can directly deploy by using your Foundry resource. 

* **Developer endpoints**

   Your project overview page includes your previous Azure OpenAI endpoint, and a new Foundry endpoint. Foundry API and SDK grant access to the broader set of models and features including agent service.

## Understanding pricing

There are no pricing differences for existing Azure OpenAI functionality when upgrading to Foundry—your current usage patterns and costs remain unchanged. However, Foundry unlocks access to more features such as expanded model catalogs, agent services, and evaluation tools, which may have their own pricing structures depending on the models and services used.

For estimating costs of new features available in Foundry, use the [Azure Pricing Calculator](https://azure.microsoft.com/pricing/calculator/).

## Private network configuration

Foundry resource is a superset of Azure OpenAI resource and its capabilities are exposed over three FQDNs:

- {custom-domain}.openai.azure.com
- {custom-domain}.services.ai.azure.com
- {custom-domain}.cognitiveservices.azure.com

Your DNS configuration must be able to resolve each of the FQDNs in order to use the full set of Foundry capabilities. 

* If you're using Azure DNS, you need to create an [Azure DNS Zone](/azure/dns/dns-zones-records) for each of the above domains.

* If you're using a custom DNS implementation, you need to implement a conditional forwarder for each of the above configurations. 

After this, delete and [re-create a private link endpoint](configure-private-link.md) on your resource. Your private link endpoint creates an IP address in your Azure Virtual Network to map to each endpoint.

> [!IMPORTANT] 
> When upgrading to Foundry, you must recreate your private link endpoint, for the "services.ai.azure.com" and "{custom-domain}.cognitiveservices.azure.com" IP configurations to be created.

## Roll back to Azure OpenAI

In case you run into any issues, a rollback option is available. As a prerequisite to roll back, you're required to delete any of the following configurations first:

* Projects
* Connections
* Non-Azure OpenAI model deployments

Then, use either the Foundry portal, Azure portal, or an ARM template to roll back:

# [Foundry portal](#tab/portal)

**Option 1: Use Foundry portal**

1. Navigate to management center in the left bottom of your screen.
1. On your resource overview page, find the rollback option.
1. Select **Rollback**.

:::image type="content" source="../media/upgrade-azure-openai/rollback.png" alt-text="Screenshot shows the rollback option in the Foundry portal." lightbox = "../media/upgrade-azure-openai/rollback.png":::

# [Azure portal](#tab/azportal)

1. Sign in to [Azure portal](https://portal.azure.com/)
1. Select your Foundry resource
1. On the overview page, select 'rollback upgrade'.

:::image type="content" source="../media/upgrade-azure-openai/rollback-azure-portal.png" alt-text="Screenshot shows how to roll back in Azure portal." lightbox = "../media/upgrade-azure-openai/rollback-azure-portal.png":::

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

**References**: [`Microsoft.CognitiveServices/accounts`](/azure/templates/microsoft.cognitiveservices/accounts), [Bicep CLI documentation](/azure/azure-resource-manager/bicep/bicep-cli)


---

## Troubleshooting Common Issues

Azure resource limits and organizational configurations may require extra steps to complete the upgrade. The table below outlines some of the most common issues along with recommended solutions to help troubleshooting.

|Issue|Solution/mitigation|
|---|---|
|User principal lacks account/write permissions|Obtain a privileged Azure RBAC role to manage top-level Azure resource. For example Owner, Contributor, Azure AI Administrator.| 
|Managed identity isn't enabled on the Azure OpenAI resource|Configure managed identity on your resource via templates or Azure portal.|
|No permissions to create agents, while you're the owner/contributor on the resource.|An EntraID data plane role is required for development actions including agents. Examples include Azure AI User or Azure AI Project Manager role. Owner and Contributor roles only grant access to management operations in Azure such as managing deployments.|
|An Azure Policy conflict occurred.|Your organization may put constraints on resource configurations. Inspect the details of the policy violation error. Then upgrade your resource via template options for further customization. For example, network configurations for Agents can only be configured via template options such as Azure Bicep.|
|Exceeded number of Azure OpenAI instances of 30 per subscription per region when rolling back.|Delete an Azure OpenAI resource or upgrade it to the Foundry. Then retry rolling back your current resource.|
|Exceeded number of AIServices instances of 100 per subscription per region.|Delete a Foundry resource you may not use in this subscription. Then retry upgrading your current resource.|
|I can't access my resource over the private network|See [private networking configuration](#private-network-configuration) for the required steps.|

## How to inspect whether a resource was upgraded

The following Azure resource property is available to inspect whether a resource was previously upgraded to Foundry.

```bicep
{
  {
    // Read only properties if your resource was upgraded:
    previouskind: "OpenAI"
  }
}
```

Not sure who upgraded your resource to Foundry? You can [view the activity log in the Azure portal](/azure/azure-monitor/platform/activity-log-insights#view-the-activity-log) to understand when the upgrade operation took place and by which user:

1. Use Azure Activity Logs (under "Monitoring") to see if an upgrade operation was performed.
1. Filter by "Write" operations on the storage account.
1. Look for operations listed as `Microsoft.CognitiveServices/accounts/write`.

## Related content

* [Choose an Azure resource type for AI foundry](../concepts/resource-types.md)
* [Bicep samples for Foundry common infrastructure configurations](https://github.com/azure-ai-foundry/foundry-samples/tree/main/samples/microsoft/infrastructure-setup)
