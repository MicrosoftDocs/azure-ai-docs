---
manager: nitinme
author: santiagxf
ms.author: fasantia 
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.date: 1/21/2025
ms.topic: include
zone_pivot_groups: azure-ai-models-deployment
---

[!INCLUDE [Header](intro.md)]

* A Foundry project with an AI Hub.

* Install the [Azure CLI](/cli/azure/).

* Identify the following information:

  * Your Azure subscription ID.

  * Your Foundry Tools resource name.
  
  * Your Foundry Tools resource ID.
  
  * The name of the Azure AI Hub where the project is deployed.

  * The resource group where the Foundry Tools resource is deployed.

## Add a connection

1. Use the template `ai-services-connection-template.bicep` to describe connection:

    __ai-services-connection-template.bicep__

    :::code language="bicep" source="~/azureai-model-inference-bicep/infra/modules/ai-services-connection-template.bicep":::

4. Run the deployment:

    ```azurecli
    RESOURCE_GROUP="<resource-group-name>"
    ACCOUNT_NAME="<azure-ai-model-inference-name>" 
    ENDPOINT_URI="https://<azure-ai-model-inference-name>.services.ai.azure.com"
    RESOURCE_ID="<resource-id>"
    HUB_NAME="<hub-name>"
    
    az deployment group create \
        --resource-group $RESOURCE_GROUP \
        --template-file ai-services-connection-template.bicep \
        --parameters accountName=$ACCOUNT_NAME hubName=$HUB_NAME endpointUri=$ENDPOINT_URI resourceId=$RESOURCE_ID
    ```
