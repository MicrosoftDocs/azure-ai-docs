---
manager: nitinme
author: mrbullwinkle
ms.author: fasantia 
ms.service: azure-ai-model-inference
ms.date: 1/21/2025
ms.topic: include
zone_pivot_groups: azure-ai-models-deployment
---

[!INCLUDE [Header](intro.md)]

* Install the [Azure CLI](/cli/azure/).

* Identify the following information:

  * Your Azure subscription ID.

  * Your Azure AI Services resource name.

  * The resource group where the Azure AI Services resource is deployed.

  * The model name, provider, version, and SKU you would like to deploy. You can use the Azure AI Foundry portal or the Azure CLI to identify it. In this example we deploy the following model:

    * **Model name:**: `Phi-3.5-vision-instruct`
    * **Provider**: `Microsoft`
    * **Version**: `2`
    * **Deployment type**: Global standard

## Add the model

1. Use the template `ai-services-deployment-template.bicep` to describe model deployments:

    __ai-services-deployment-template.bicep__

    :::code language="bicep" source="~/azureai-model-inference-bicep/infra/modules/ai-services-deployment-template.bicep":::

2. Run the deployment:

    ```azurecli
    RESOURCE_GROUP="<resource-group-name>"
    ACCOUNT_NAME="<azure-ai-model-inference-name>" 
    MODEL_NAME="Phi-3.5-vision-instruct"
    PROVIDER="Microsoft"
    VERSION=2
    
    az deployment group create \
        --resource-group $RESOURCE_GROUP \
        --template-file ai-services-deployment-template.bicep \
        --parameters accountName=$ACCOUNT_NAME modelName=$MODEL_NAME modelVersion=$VERSION modelPublisherFormat=$PROVIDER
    ```


## Use the model

Deployed models in Azure AI model inference can be consumed using the [Azure AI model's inference endpoint](../../concepts/endpoints.md) for the resource. When constructing your request, indicate the parameter `model` and insert the model deployment name you have created.
