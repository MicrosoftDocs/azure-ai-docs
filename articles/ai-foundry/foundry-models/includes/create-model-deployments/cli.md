---
manager: nitinme
author: santiagxf
ms.author: fasantia 
ms.service: azure-ai-model-inference
ms.date: 1/21/2025
ms.topic: include
zone_pivot_groups: azure-ai-models-deployment
---

[!INCLUDE [Header](intro.md)]

* Install the [Azure CLI](/cli/azure/) and the `cognitiveservices` extension for Azure AI Services:

    ```azurecli
    az extension add -n cognitiveservices
    ```

* Some of the commands in this tutorial use the `jq` tool, which might not be installed in your system. For installation instructions, see [Download `jq`](https://stedolan.github.io/jq/download/).

* Identify the following information:

  * Your Azure subscription ID.

  * Your Azure AI Services resource name.

  * The resource group where the Azure AI Services resource is deployed.
    
    
## Add models

To add a model, you first need to identify the model that you want to deploy. You can query the available models as follows:

1. Log in into your Azure subscription:

    ```azurecli
    az login
    ```

2. If you have more than 1 subscription, select the subscription where your resource is located:

    ```azurecli
    az account set --subscription $subscriptionId
    ```

3. Set the following environment variables with the name of the Azure AI Services resource you plan to use and resource group.

    ```azurecli
    accountName="<ai-services-resource-name>"
    resourceGroupName="<resource-group>"
    location="eastus2"
    ```

3. If you don't have an Azure AI Services account create yet, you can create one as follows:

    ```azurecli
    az cognitiveservices account create -n $accountName -g $resourceGroupName --custom-domain $accountName --location $location --kind AIServices --sku S0
    ```

4. Let's see first which models are available to you and under which SKU. SKUs, also known as [deployment types](../../concepts/deployment-types.md), define how Azure infrastructure is used to process requests. Models may offer different deployment types. The following command list all the model definitions available:
    
    ```azurecli
    az cognitiveservices account list-models \
        -n $accountName \
        -g $resourceGroupName \
    | jq '.[] | { name: .name, format: .format, version: .version, sku: .skus[0].name, capacity: .skus[0].capacity.default }'
    ```

5. Outputs look as follows:

    ```output
    {
      "name": "Phi-3.5-vision-instruct",
      "format": "Microsoft",
      "version": "2",
      "sku": "GlobalStandard",
      "capacity": 1
    }
    ```

6. Identify the model you want to deploy. You need the properties `name`, `format`, `version`, and `sku`. The property `format` indicates the provider offering the model. Capacity might also be needed depending on the type of deployment.

7. Add the model deployment to the resource. The following example adds `Phi-3.5-vision-instruct`:

    ```azurecli
    az cognitiveservices account deployment create \
        -n $accountName \
        -g $resourceGroupName \
        --deployment-name Phi-3.5-vision-instruct \
        --model-name Phi-3.5-vision-instruct \
        --model-version 2 \
        --model-format Microsoft \
        --sku-capacity 1 \
        --sku-name GlobalStandard
    ```

8. The model is ready to be consumed.

You can deploy the same model multiple times if needed as long as it's under a different deployment name. This capability might be useful in case you want to test different configurations for a given model, including content filters.

## Use the model

Deployed models in can be consumed using the [Azure AI model's inference endpoint](../../concepts/endpoints.md) for the resource. When constructing your request, indicate the parameter `model` and insert the model deployment name you have created. You can programmatically get the URI for the inference endpoint using the following code:

__Inference endpoint__

```azurecli
az cognitiveservices account show  -n $accountName -g $resourceGroupName | jq '.properties.endpoints["Azure AI Model Inference API"]'
```

To make requests to the Azure AI Foundry Models endpoint, append the route `models`, for example `https://<resource>.services.ai.azure.com/models`. You can see the API reference for the endpoint at [Azure AI Model Inference API reference page](https://aka.ms/azureai/modelinference).

__Inference keys__

```azurecli
az cognitiveservices account keys list  -n $accountName -g $resourceGroupName
```

## Manage deployments

You can see all the deployments available using the CLI:

1. Run the following command to see all the active deployments:

    ```azurecli
    az cognitiveservices account deployment list -n $accountName -g $resourceGroupName
    ```

2. You can see the details of a given deployment:

    ```azurecli
    az cognitiveservices account deployment show \
        --deployment-name "Phi-3.5-vision-instruct" \
        -n $accountName \
        -g $resourceGroupName
    ```

3. You can delete a given deployment as follows:

    ```azurecli
    az cognitiveservices account deployment delete \
        --deployment-name "Phi-3.5-vision-instruct" \
        -n $accountName \
        -g $resourceGroupName
    ```    
    
