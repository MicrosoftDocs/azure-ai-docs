---
title: 'Use your own resources in the Azure AI Agent Service'
titleSuffix: Azure OpenAI
description: Learn how to use resources that you already have with the Azure AI Agent Service. 
services: cognitive-services
manager: nitinme
ms.service: azure-ai-agent-service
ms.topic: how-to
ms.date: 01/15/2025
author: fosteramanda
ms.author: fosteramanda
ms.custom: azure-ai-agents
---

# Use your own resources

Use this article if you want to use the Azure Agent Service with resources you already have. 

> [!NOTE]
> * If you use an existing AI Services / Azure OpenAI Service resource, no model will be deployed. You can deploy a model to the resource after the agent setup is complete. 
> * Make sure your Azure OpenAI resource and Azure AI Foundry project are in the same region. 

## Choose basic or standard agent setup

To use your own resources, you can edit the parameters in the provided deployment templates. To start, determine if you want to edit the [basic agent setup template](https://github.com/Azure-Samples/azureai-samples/tree/main/scenarios/Agents/setup/basic-agent-identity), or the [standard agent setup template](https://github.com/Azure-Samples/azureai-samples/tree/main/scenarios/Agents/setup/standard-agent).
   
**Basic Setup**:  Agents created in a basic project use multitenant search and storage resources fully managed by Microsoft. You don't have visibility or control over these underlying Azure resources. You can only use your own AI services account with this option.

**Standard Setup**: Agents created in a standard project use customer-owned, single-tenant search and storage resources. With this setup, you have full control and visibility over these resources, but you incur costs based on your usage. You can use your own AI services account, Azure Storage account, Cosmos DB for NoSQL account and/or Azure AI Search resource with this option. 

## Basic agent setup: Use an existing AI Services/Azure OpenAI resource 

Replace the parameter value for `aiServiceAccountResourceId` with the full arm resource ID of the AI Services or Azure OpenAI resource you want to use.

1. To get the AI Services account resource ID, sign in to the Azure CLI and select the subscription with your AI Services account:
       
    ```az login``` 
2. Replace `<your-resource-group>` with the resource group containing your resource and `your-ai-service-resource-name` with the name of your AI Service resource, and run:
    
    ```az cognitiveservices account show --resource-group <your-resource-group> --name <your-ai-service-resource-name> --query "id" --output tsv```

    The value returned is the `aiServiceAccountResourceId` you need to use in the template.

3. In the basic agent template file, replace the following placeholders:
    
    ```
    aiServiceAccountResourceId:/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CognitiveServices/accounts/{serviceName}

    [Azure OpenAI Only] aiServiceKind: AzureOpenAI
    ```

    If you want to use an existing Azure OpenAI resource, you will need to update the `aiServiceAccountResourceId` and the `aiServiceKind` parameters in the parameter file. The aiServiceKind parameter should be set to AzureOpenAI.


## Standard agent setup: Use an existing AI Services/Azure OpenAI, Azure Storage account, Azure Cosmos DB for NoSQL account, and/or Azure AI Search resource 

Use an existing AI Services / Azure OpenAI, Azure Storage account, Azure Cosmos DB for NoSQL account and/or Azure AI Search resource by providing the full ARM resource ID in the standard agent template file.

### Use an existing AI Services or Azure OpenAI resource

1. Follow the steps in basic agent setup to get the AI Services account resource ID.
2. In the standard agent template file, replace the following placeholders:
    
    ```
    aiServiceAccountResourceId:/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CognitiveServices/accounts/{serviceName}
    
    [Azure OpenAI Only] aiServiceKind: AzureOpenAI
    ```

### Use an existing Azure Storage account for file storage

1. To get your storage account resource ID, sign in to the Azure CLI and select the subscription with your storage account: 
    
    ```az login``` 
2. Then run the command:

    ```az storage account show --resource-group  <your-resource-group> --name <your-storage-account>  --query "id" --output tsv```
   
     The output is the `aiStorageAccountResourceID` you need to use in the template.
   
3. In the standard agent template file, replace the following placeholders:
    
    ```
    aiStorageAccountResourceId:/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Storage/storageAccounts/{storageAccountName}
    ```

### Use an existing Azure Cosmos DB for NoSQL account for thread storage

1. To get your Azure Cosmos DB account resource ID, sign in to the Azure CLI and select the subscription with your account: 
    
    ```console
    az login
    ``` 
    
2. Then run the command:

    ```console
    az cosmosdb show --resource-group  <your-resource-group> --name <your-comosdb-account>  --query "id" --output tsv
    ```
    
     The output is the `cosmosDBResourceId` you need to use in the template.
3. In the standard agent template file, replace the following placeholders:
    
    `cosmosDBResourceId:/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DocumentDB/databaseAccounts/{cosmosDbAccountName}`
    
### Use an existing Azure AI Search resource

1. To get your Azure AI Search resource ID, sign into Azure CLI and select the subscription with your search resource: 
    
    ```az login```
2. Then run the command:
    
    ```az search service show --resource-group  <your-resource-group> --name <your-search-service>  --query "id" --output tsv```
3. In the standard agent template file, replace the following placeholders:

    ```
    aiSearchServiceResourceId:/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Search/searchServices/{searchServiceName}
    ```

## See also

* Learn about the different [tools](./tools/overview.md) agents can use. 
