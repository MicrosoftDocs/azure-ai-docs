---
manager: nitinme
author: aahill
ms.author: aahi
ms.service: azure
ms.topic: include
ms.date: 11/13/2024
---

## Set up your Azure AI Hub and Agent project

The following section will show you how to set up an [Azure AI hub and project](../../../ai-studio/quickstarts/get-started-playground.md) by:

1. Creating an Azure AI Hub to set up your app environment and Azure resources

1. Creating an Azure AI project under your Hub creates an endpoint for your app to call, and sets up app services to access to resources in your tenant.

1. Connecting an Azure OpenAI resource or an Azure AI resource


1. Install [the Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli-windows?tabs=azure-cli). If you have the CLI already installed, make sure it is updated to the latest version.

1. Register providers.

   The following providers must be registered:

   - Microsoft.KeyVault
   - Microsoft.CognitiveServices
   - Microsoft.Storage
   - Microsoft.MachineLearningServices
   - Microsoft.Search
   - To use Bing Search tool: Microsoft.Bing

   ```console
   az provider register -–namespace  {my_resource_namespace}
                        [--accept-terms]
                        [--consent-to-permissions]
                        [--management-group-id]
                        [--wait]
   ```

1. To authenticate to your Azure subscription from the Azure CLI, use the following command:

   > [!NOTE]
   > Be sure to run these commands with the subscription that has been allowlisted for the private preview.

   ```console
   az login
   ```

1. Create a resource group:

   ```console
   az group create --name {my_resource_group} --location eastus
   ```

   Make sure you have the role **Azure AI Developer** on the resource group you created.


## Choose Basic or Standard Agent Setup
   
**Basic Setup**:  Agents use multitenant search and storage resources fully managed by Microsoft. You don't have visibility or control over these underlying Azure resources.

**Standard Setup**: Agents use customer-owned, single-tenant search and storage resources. With this setup, you have full control and visibility over these resources, but you will incur costs based on your usage.

# [Standard setup](#tab/standard-setup)

1. Download the `standard-agent.bicep` file, the `standard-agent.parameters.json` file, and the `modules-standard` folder to your project directory. Your directory should look like this

    ```console
    /my-project
        - standard-agent.bicep
        - standard-agent.parameters.json 
        /modules-standard
            - standard-ai-hub.bicep
            - standard-ai-project.bicep
            - standard-dependent-resources.bicep
    ```
1.  Using the resource group you created in the previous step, run one of the following commands:

    - To use default resource names, run:

        ```console
        az deployment group create --resource-group {my_resource_group} --template-file standard-agent.bicep
        ```

    - To customize additional parameters, including the OpenAI model, deployment or hub name, download and edit the `standard-agent.parameters.json` file, then run:

        ```console
        az deployment group create --resource-group {my_resource_group} --template-file standard-agent.bicep --parameters @standard-agent.parameters.json
        ```

    Resources for the hub, project, storage account, key vault, AI Services, and Azure AI Search will be created for you. The AI Services, AI Search, and Azure Blob Storage account will be connected to your project/hub and a gpt-4o-mini model will be deployed in the eastus region. 

# [Basic setup](#tab/basic-setup)

1. Download the `basic-agent-keys.bicep` file, `basic-agent-identity.bicep` file, and the `modules-basic` folder to your project directory. Your directory should look like this
    
    ```console
    /my-project
        - basic-agent-keys.bicep
        - basic-agent-identity.bicep
        - basic-agent.parameters.json
        /modules-basic
            - basic-ai-hub-keys.bicep
            - basic-ai-project-keys.bicep
            - basic-ai-hub-identity.bicep
            - basic-ai-project-identity.bicep
            - basic-dependent-resources.bicep
    ```

1. Before deploying resources, decide which configuration file to use:
    - `basic-agent-keys.bicep`: Use this file to use API keys for authentication.
    - `basic-agent-identity.bicep`: Use this file if you prefer Managed Identity to securely access resources without API keys.
    

1. Using the resource group you created in the previous step and one of the template files (either basic-agent-keys.bicep or basic-agent-identity.bicep), run one of the following commands:

    - To use default resource names, run:
        
        ```console
        az deployment group create --resource-group {my_resource_group} --template-file {my-template-file.bicep}
        ```
    
    - To specify custom names for the hub, project, storage account, and/or Azure AI service resources (Note: a randomly generated suffix will be added to prevent accidental duplication), run:
        
        ```console
        az deployment group create --resource-group {my_resource_group} --template-file {my-template-file.bicep} --parameters aiHubName='your-hub-name' aiProjectName='your-project-name' storageName='your-storage-name' aiServicesName='your-ai-services-name'
        ```

1. To customize additional parameters, including the OpenAI model deployment, download and edit the `basic-agent.parameters.json` file, then run:

    ```console
    az deployment group create --resource-group {my_resource_group} --template-file  {my-template-file.bicep} --parameters @basic-agent.parameters.json
    ```

Resources for the hub, project, storage account, and AI Services will be created for you. The AI Services account will be connected to your project/hub and a gpt-4o-mini model will be deployed in the eastus region. A Microsoft-managed key vault will be used by default.

---