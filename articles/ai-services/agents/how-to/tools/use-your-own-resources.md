---
title: 'How to use your own resources in agent setup'
titleSuffix: Azure OpenAI
description: Learn how to use your own resources in the Azure AI Agent service setup.
services: cognitive-services
manager: nitinme
ms.service: azure
ms.topic: how-to
ms.date: 12/11/2024
author: fosteramanda
ms.author: fosteramanda
ms.custom: azure-ai-agents
---
# [Optional] Use your own resources in agent setup

> [!NOTE]
> If you use an existing AI Services/AOAI resource, no model will be deployed. You can deploy a model to the resource after the agent setup is complete. 

### Basic agent setup: use an existing AI Services or Azure OpenAI resource 

Replace the parameter value for `aiServiceAccountResourceId` with the full arm resource ID of the AI Services/ Azure OpenAI resource you want to use.

1. To get the AI Services/Azure OpenAI resource ID, sign in to the Azure CLI and select the subscription with your AI Services/Azure OpenAI account:
       
    ```az login``` 
2. Replace `<your-resource-group>` with the resource group containing your resource and `your-ai-service-resource-name` with the name of your AI Service resource, and run:
    
    ```az cognitiveservices account show --resource-group <your-resource-group> --name <your-ai-service-resource-name> --query "id" --output tsv```

    The value returned is the `aiServiceAccountResourceId` you need to use in the template.

3. In the basic agent template file, set the parameter:
    - aiServiceAccountResourceId:/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CognitiveServices/accounts/{serviceName}
    - [Azure OpenAI Resource Only] aiServiceKind: AzureOpenAI


    If you want to use an existing Azure OpenAI resource, you will need to update the `aiServiceAccountResourceId` and the `aiServiceKind` parameters in the parameter file. The aiServiceKind parameter should be set to AzureOpenAI.

### Standard agent setup: use an existing AI Services, storage, and/or Azure AI Search resource 

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