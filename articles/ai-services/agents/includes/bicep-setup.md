---
manager: nitinme
author: aahill
ms.author: aahi
ms.service: azure
ms.topic: include
ms.date: 11/13/2024
---

## Set up your Azure AI Hub and Agent project

The following section shows you how to set up the required resources for getting started with Azure AI Agents Service: 

1. Creating an [Azure AI Hub](../../../ai-studio/quickstarts/get-started-playground.md) to set up your app environment and Azure resources.

1. Creating an Azure AI project under your Hub creates an endpoint for your app to call, and sets up app services to access to resources in your tenant.

1. Connecting an Azure OpenAI resource or an Azure AI Services resource


## Choose Basic or Standard Agent Setup
   
**Basic Setup**:  Agents use multitenant search and storage resources fully managed by Microsoft. You don't have visibility or control over these underlying Azure resources.

**Standard Setup**: Agents use customer-owned, single-tenant search and storage resources. With this setup, you have full control and visibility over these resources, but you incur costs based on your usage.

| Description   | Resources  | Autodeploy |
| -----------------------------------------------| -----------------------|----------------------|
| Deploy a basic agent setup that uses Managed Identity authentication on the AI Services and storage account connections. | AI hub, AI project, AI Services | [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2FAzure%2Fazure-quickstart-templates%2Fmaster%2Fquickstarts%2Fmicrosoft.azure-ai-agent-service%2Fbasic-agent-identity%2Fazuredeploy.json) |
| Deploy a standard agent setup that uses Managed Identity authentication on the AI Services, storage account, and Azure AI Search connections. |AI hub, AI project, storage account, key vault, Azure AI Search, AI Services | [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2FAzure%2Fazure-quickstart-templates%2Frefs%2Fheads%2Fmaster%2Fquickstarts%2Fmicrosoft.azure-ai-agent-service%2Fstandard-agent%2Fazuredeploy.json)|

### [Optional] Model selection in autodeploy template
You can customize the model used by your agent by editing the model parameters in the autodeploy template. To deploy a different model, you need to update at least the `modelName` and `modelVersion` parameters. 

By default, the deployment template is configured with the following values:

| Model Parameter  | Default Value  |
|------------------|----------------|
| modelName        | gpt-4o-mini    |
| modelFormat      | OpenAI         |
| modelVersion     | 2024-07-18     |
| modelSkuName     | GlobalStandard |
| modelLocation    | eastus         |

> [!IMPORTANT]
> **Don't change the modelFormat parameter.** 
>
> The templates only support deployment of OpenAI models. See which OpenAI models are supported in the [Azure AI Agent Service model support](../concepts/model-region-support.md) documentation.


### [Optional] Use your own resources in agent setup

> [!NOTE]
> If you use an existing AI Services/AOAI resource, no model will be deployed. You can deploy a model to the resource after the agent setup is complete. 

#### Basic agent setup: use an existing AI Services resource 

Replace the parameter value for `aiServiceAccountResourceId` with the full arm resource ID of the AI Services account you want to use.

1. To get the AI Services account resource ID, sign in to the Azure CLI and select the subscription with your AI Services account:
       
    ```az login``` 
2. Replace `<your-resource-group>` with the resource group containing your resource and `your-ai-service-resource-name` with the name of your AI Service resource, and run:
    
    ```az cognitiveservices account show --resource-group <your-resource-group> --name <your-ai-service-resource-name> --query "id" --output tsv```

    The value returned is the `aiServiceAccountResourceId` you need to use in the template.

2. In the basic agent template file, set the parameter:
    - aiServiceAccountResourceId:/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CognitiveServices/accounts/{serviceName}

#### Standard agent setup: use an existing AI Services, storage, and/or Azure AI Search resource 

Use an existing AI Search, storage account, and/or Azure AI Search resource by providing the full arm resource ID in the standard agent template file.

Use an existing AI Services resource:
1. Follow the steps in basic agent setup to get the AI Services account resource ID.
2. In the standard agent template file, set the parameter:
    - aiServiceAccountResourceId:/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CognitiveServices/accounts/{serviceName}

Use an existing storage account:
1. To get your storage account resource ID, sign in to the Azure CLI and select the subscription with your storage account: 
    
    ```az login``` 
2. Then run the command:

    ```az search service show --resource-group  <your-resource-group> --name <your-storage-account>  --query "id" --output tsv```
    
     The output is the `aiStorageAccountResourceID` you need to use in the template.
3. In the standard agent template file, set the parameter:
    - aiStorageAccountResourceId:/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Storage/storageAccounts/{storageAccountName}

Use an existing Azure AI Search resource:
1. To get your Azure AI Search resource ID, sign into Azure CLI and select the subscription with your search resource: 
    
    ```az login```
2. Then run the command:
    
    ```az search service show --resource-group  <your-resource-group> --name <your-search-service>  --query "id" --output tsv```
3. In the standard agent template file, set the parameter:
    - aiSearchServiceResourceId:/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Search/searchServices/{searchServiceName}

## Basic agent setup resource architecture
:::image type="content" source="../media/quickstart/basic-agent-setup-resources.png" alt-text="An architecture diagram for basic agent setup." lightbox="../media/quickstart/basic-agent-setup-resources.png":::

Resources for the AI hub, AI project, and AI Services are created for you. A storage account is created because it's a required resource for hubs, but this storage account is not used by agents. The AI Services account is connected to your project/hub and a gpt-4o-mini model is deployed in the eastus region. A Microsoft-managed key vault, storage account, and search resource is used by default.

## Standard agent setup resource architecture
:::image type="content" source="../media/quickstart/standard-agent-setup-resources.png" alt-text="An architecture diagram for standard agent setup." lightbox="../media/quickstart/standard-agent-setup-resources.png":::

Resources for the AI hub, AI project, key vault, storage account, AI Services, and AI Search are created for you. The AI Services, AI Search, key vault, and storage account are connected to your project and hub. A gpt-4o-mini model is deployed in eastus region using the AI Services resource OpenAI endpoint.