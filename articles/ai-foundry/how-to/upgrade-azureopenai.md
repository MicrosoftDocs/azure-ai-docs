# Upgrade from Azure OpenAI to AI Foundry (preview)

The Azure AI Foundry resource type offers a superset of capabilities compared to the Azure OpenAI resource type. It enables access to a broader model catalog, agents service, and evaluation capabilities.

An upgrade option is available for existing customers who prefer to keep their existing Azure OpenAI API endpoint, state of work, and security configurations, without creating a new Azure AI Foundry resource.

## Benefits of Upgrading

Upgrading to Azure AI Foundry unlocks the following capabilites.

|Feature|Azure OpenAI|Azure AI Foundry|
|---|---|---|
| Models sold directly by Azure | Azure OpenAI only | Azure OpenAI, Black Forest Labs, DeepSeek, Meta, xAI, Mistral, Microsoft  |
| Partner & Community Models sold through Marketplace - Stability, Bria, Cohere, etc.|  | ✅ |
| Azure OpenAI API (batch, stored completions, fine-tuning, evaluation, ..) | ✅ | ✅ |n
| Agent service | | ✅ |
| Azure Foundry API |  | ✅ |
| AI Services (Speech, Vision, Language, Content Understanding) | | ✅ |

Existing resource configurations and state remain preserved including:

* Resource name
* Azure resource tags
* Network configurations
* Access and identity configurations
* API endpoint and API key
* Custom Domain Name
* Existing state including fine-tuning jobs, batch, stored completions, etc.

## Limitations

Backend limitations:
* Azure OpenAI resources using **customer-managed keys** for encryption are not supported for upgrade.
* AI Foundry resource type does not support configuring Weights & Biases.

Foundry UX limitations:
* Evaluations UX view does not yet support all capabilities that Azure OpenAI evaluations UX view supports.

## Support level post-upgrade 

The upgrade converts your Azure OpenAI resource type to Azure AI Foundry resource type. While both services are generally available and supported before and after the upgrade, the upgrade process itself is experimental. If needed, you can [roll back to your previous setup](#rollback-to-azure-openai).

## How to upgrade

As a pre-requisite to upgrade, managed identity must be enabled on your Azure OpenAI resource. Upgrade can be completed via Foundry Portal UX or using Azure Bicep or Resource Manager templates. 

* **Option 1: use Azure AI Foundry Portal**

  * Navigate to your Azure OpenAI resource.
  * In overview page, find the banner *'Make the switch to AI Foundry'* and select *'switch now'*.
  * Provide the name for your first project. This is a folder to organize your work in Azure AI Foundry. Your first 'default' project has backwards compatiblity with your previous work in Azure OpenAI.
  * Confirm to start the upgrade. This will take up to two minutes.
  
  > [!NOTE]
  > While the upgrade capability is rolling out to all users, you may not see the upgrade action yet in the UX for your resource.

* **Option 2: use an Azure Bicep template**

    Starting with your existing Azure Open AI template configuration, set the following properties:

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

    Run the template using Azure CLI options or your VSCode extension for Bicep as a patch operation on your current resource.

## Rollback to Azure OpenAI

In case you run into any issues, a rollback option is available. As pre-requisite to rollback, you are required to delete any of the following configurations first:

* Projects
* Connections
* Non-Azure OpenAI model deployments

Then, use either AI Foundry Portal or ARM template to rollback:

* **Option 1: use Azure AI Foundry Portal**

  * To start, navigate to management center in the left bottom of your screen.
  * On your resource overview page, find the rollback option.

* **Option 2: use an Azure Bicep template**
  
  To rollback, convert your template configuration back to 'OpenAI' as kind.
  
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

    Run the template using Azure CLI options or your VSCode extension for Bicep as a patch operation on your current resource.


## Inspect whether a resoure was upgraded before

The following Azure resource property is available to inspect whether a resource was previously upgraded to AI Foundry.

```bicep
{
  {
    // Read only properties if your resource was upgraded:
    previouskind: "OpenAI"
  }
}
```

Not sure who upgraded your resource to Azure AI Foundry? You can inspect the activity log in Azure Portal:

1. Use Azure Activity Logs (under "Monitoring") to see if an upgrade operation was performed.
1. Filter by "Write" operations on the storage account.
1. Look for operations listed as `Microsoft.CognitiveServices/accounts/write`.
