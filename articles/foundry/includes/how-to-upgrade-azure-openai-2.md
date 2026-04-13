---
title: Include file
description: Include file
author: sdgilley
ms.reviewer: deeikele
ms.author: sgilley
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 03/20/2026
ms.custom: include
---

## Limitations

* Foundry model and feature availability [differs by region](../reference/region-support.md). For example, Agent service is [available](../agents/concepts/limits-quotas-regions.md) in select regions compared to Azure OpenAI service.
* Azure OpenAI resources using **customer-managed keys** for encryption are available for upgrade by request only. [Fill out the request form here](https://forms.office.com/r/sKGZJ0YhDd).
* The Foundry resource type doesn't support configuring Weights & Biases.
* Private network setups require [additional DNS zone configurations](#private-network-configuration) next to your existing Azure OpenAI DNS Zone before all Foundry capabilities can be used.

## Support level post-upgrade

The upgrade converts your Azure OpenAI resource type to Foundry resource type. Both services are generally available and supported before and after the upgrade. Upgrading your Azure OpenAI resource is an opt-in capability. If needed, you can [roll back to your previous setup](#roll-back-to-azure-openai).

## How to upgrade

### Prerequisites for upgrade

Before you upgrade your Azure OpenAI resource to a Foundry resource, ensure you have:

- **Azure role requirements**: You must have one of the following Azure roles on your subscription or resource group:
  - **Owner** role on the subscription or resource group for resource management and configuration and assign roles to the new project.
  
  You need this role to enable managed identity and perform the upgrade operation.

- **Managed identity**: You must enable managed identity on your Azure OpenAI resource. If it's not already enabled, you can enable it through the [Azure portal](https://portal.azure.com). Go to your resource, select **Identity** from the left menu, and toggle **System assigned** to **On**.

### Upgrade your resource

You can complete the upgrade through the Foundry (classic) portal, Azure portal, or by using Azure Bicep or Resource Manager templates (recommended for resource configurations with custom security settings).

# [Foundry portal](#tab/portal)

1. [!INCLUDE [classic-sign-in](classic-sign-in.md)]
1. Select your Azure OpenAI resource.
1. On the overview page, find the banner **Want to try the latest industry models and Agents?** and select **Get started**.
1. Enter a name for your first project. A project is a folder to organize your work in Foundry. Your first 'default' project is backward compatible with your previous work in Azure OpenAI.
1. Confirm to start the upgrade.

**Success**: After the upgrade completes, you're taken to your new Foundry project. Your resource name, API endpoint, and existing configurations remain unchanged. You now have access to the broader model catalog, agent service, and Foundry Tools. 

You can use this project in either the Foundry (classic) or the Foundry (new) portal. To switch to the new portal, turn **New Foundry** toggle to **on**.

# [Azure portal](#tab/azportal)

1. Sign in to [Azure portal](https://portal.azure.com/).
1. Select your Azure OpenAI resource.
1. On the overview page, locate the banner "Want to try the latest industry models and Agents?" and select **Get Started**.
1. Confirm to start the upgrade.

:::image type="content" source="../media/upgrade-azure-openai/azure-portal-upgrade.png" alt-text="Screenshot shows how to upgrade in Azure portal." lightbox="../media/upgrade-azure-openai/azure-portal-upgrade.png":::

**Success**: The upgrade completes, and you're returned to your resource overview page. Your resource type is now **Foundry** (previously **Azure OpenAI**). All existing configurations, endpoints, and API keys remain the same.

# [Azure Bicep](#tab/bicep)

Starting with your existing Azure OpenAI template configuration, set the following properties:

* Update `kind` from value `OpenAI` to `AIServices`.
* Set `allowProjectManagement` to `true`.
* Configure managed identity.

Sample configuration:

```bicep
resource foundry 'Microsoft.CognitiveServices/accounts@2025-06-01' = {
    name: foundryName // Your existing resource name
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
        customSubDomainName: foundryName
        disableLocalAuth: true
    }
}
```

Run the template by using [Azure Bicep CLI](/azure/azure-resource-manager/bicep/bicep-cli) or your [Visual Studio Code extension for Bicep](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-bicep) as a patch operation on your current resource.

**References**: [`Microsoft.CognitiveServices/accounts`](/azure/templates/microsoft.cognitiveservices/accounts), [Bicep CLI documentation](/azure/azure-resource-manager/bicep/bicep-cli).

**Success**: The patch operation completes with no errors. Your resource's `kind` property changes from `OpenAI` to `AIServices`, and `allowProjectManagement` is set to `true`. Your existing endpoint, API keys, and configurations are preserved.

# [Terraform](#tab/terraform)

You can upgrade your Azure OpenAI resource by using either the AzAPI or AzureRM Terraform providers.

> [!IMPORTANT]
> When using the [AzureRM resource provider](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/cognitive_account.html), make sure you use a version greater than 4.57.0 of your Terraform CLI client for a non-destructive resource update.

Start from your existing Azure OpenAI configuration and update the following properties:

* Update kind from value `OpenAI` to `AIServices`.
* Set `allowProjectManagement: True`.
* Configure managed identity.

Finally, run `terraform apply` to complete the upgrade.

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

    You can also use this project in the Foundry (new) portal.

* **Broader set of models in model catalog**
   
   Your model catalog now includes more models that you can directly deploy by using your Foundry resource. 

* **Developer endpoints**

   Your project overview page includes your previous Azure OpenAI endpoint, and a new Foundry endpoint. Foundry API and SDK grant access to the broader set of models and features including agent service.

## Understanding pricing

When you upgrade to Foundry, you don't pay more for existing Azure OpenAI functionality. Your current usage patterns and costs stay the same. However, Foundry provides access to more features, such as expanded model catalogs, agent services, and evaluation tools. These features might have their own pricing structures depending on the models and services you use.

To estimate the costs of new features available in Foundry, use the [Azure Pricing Calculator](https://azure.microsoft.com/pricing/calculator/).
