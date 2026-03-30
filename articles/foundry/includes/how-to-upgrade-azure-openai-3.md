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

## Private network configuration

Foundry resource is a superset of Azure OpenAI resource. It exposes its capabilities over three FQDNs:

- {custom-domain}.openai.azure.com
- {custom-domain}.services.ai.azure.com
- {custom-domain}.cognitiveservices.azure.com

Your DNS configuration must resolve each of these FQDNs to use the full set of Foundry capabilities. 

* If you're using Azure DNS, create an [Azure DNS Zone](/azure/dns/dns-zones-records) for each of the above domains.

* If you're using a custom DNS implementation, implement a conditional forwarder for each of the above configurations. 

After you configure DNS, update or alternatively [delete and re-create a private link endpoint](../how-to/configure-private-link.md) on your resource. Your private link endpoint creates an IP address in your Azure Virtual Network to map to each endpoint.

> [!IMPORTANT] 
> When upgrading to Foundry, you must recreate your private link endpoint for the "services.ai.azure.com" and "{custom-domain}.cognitiveservices.azure.com" IP configurations to be created.

## Roll back to Azure OpenAI

If you run into any problems, you can roll back. To roll back, first delete any of the following configurations:

* Projects
* Connections
* Non-Azure OpenAI model deployments

Then, use either the Foundry (classic) portal, Azure portal, or an ARM template to roll back:

# [Foundry portal](#tab/portal)

**Option 1: Use Foundry portal**

1. Select the project in the Foundry (classic) portal.
1. Select **Management Center** in the lower left of your screen.
1. On your resource overview page, find the rollback option.
1. Select **Rollback**.

:::image type="content" source="../media/upgrade-azure-openai/rollback.png" alt-text="Screenshot shows the rollback option in the Foundry portal." lightbox="../media/upgrade-azure-openai/rollback.png":::

# [Azure portal](#tab/azportal)

1. Sign in to [Azure portal](https://portal.azure.com/).
1. Select your Foundry resource.
1. On the overview page, select **rollback upgrade**.

:::image type="content" source="../media/upgrade-azure-openai/rollback-azure-portal.png" alt-text="Screenshot shows how to roll back in Azure portal." lightbox="../media/upgrade-azure-openai/rollback-azure-portal.png":::

# [Azure Bicep](#tab/bicep)

**Option 2: Use an Azure Bicep template**
  
To roll back, convert your template configuration back to `OpenAI` as kind.

  ```bicep
  resource foundry 'Microsoft.CognitiveServices/accounts@2025-06-01' = {
  name: foundryName
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
      customSubDomainName: foundryName
      disableLocalAuth: true
  }
  ```

  Run the template by using [Azure Bicep CLI](/azure/azure-resource-manager/bicep/bicep-cli) or your [Visual Studio Code extension for Bicep](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-bicep) as a patch operation on your current resource.

  **References**: [`Microsoft.CognitiveServices/accounts`](/azure/templates/microsoft.cognitiveservices/accounts), [Bicep CLI documentation](/azure/azure-resource-manager/bicep/bicep-cli).

# [Terraform](#tab/terraform)

To roll back to Azure OpenAI, use either the AzAPI or AzureRM Terraform providers.

> [!NOTE]
> When using the [AzureRM resource provider](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/cognitive_account.html), make sure you use a version greater than 4.57.0 of your Terraform CLI client for a non-destructive resource update.

* Delete any non-OpenAI model deployments.
* Delete Foundry-specific sub-resources, including projects and connections.
* In your `azurerm_cognitive_account` resource, update kind from value 'AIServices' to 'OpenAI' and set `allowProjectManagement` to False.

---
