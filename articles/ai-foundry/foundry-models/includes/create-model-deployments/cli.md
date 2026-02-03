---
manager: nitinme
author: santiagxf
ms.author: fasantia 
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.date: 09/29/2025
ms.topic: include
zone_pivot_groups: azure-ai-models-deployment
---

You can decide and configure which models are available for inference in your Microsoft Foundry resource. When you configure a model, you can generate predictions from it by specifying its model name or deployment name in your requests. You don't need to make any other changes in your code to use the model.

In this article, you learn how to add a new model to a Foundry Models endpoint.

## Prerequisites

To complete this article, you need:

* An Azure subscription. If you're using [GitHub Models](https://docs.github.com/en/github-models/), you can upgrade your experience and create an Azure subscription in the process. Read [Upgrade from GitHub Models to Foundry Models](../../how-to/quickstart-github-models.md) if that's your case.

* A Foundry project. This kind of project is managed under a Foundry resource (formerly known as Azure AI Services resource). If you don't have a Foundry project, see [Create a project for Microsoft Foundry](../../../how-to/create-projects.md).


* [Foundry Models from partners and community](../../concepts/models-from-partners.md) require access to **Azure Marketplace**. Ensure you have the [permissions required to subscribe to model offerings](../../how-to/configure-marketplace.md). [Foundry Models sold directly by Azure](../../concepts/models-sold-directly-by-azure.md) don't have this requirement.

* Install the [Azure CLI](/cli/azure/) and the `cognitiveservices` extension for Foundry Tools.

    ```azurecli
    az extension add -n cognitiveservices
    ```

* Some of the commands in this tutorial use the `jq` tool, which might not be installed on your system. For installation instructions, see [Download `jq`](https://stedolan.github.io/jq/download/).

* Identify the following information:

  * Your Azure subscription ID.

  * Your Foundry Tools resource name.

  * The resource group where you deployed the Foundry Tools resource.
    
    
## Add models

To add a model, first identify the model that you want to deploy. You can query the available models as follows:

1. Sign in to your Azure subscription.

    ```azurecli
    az login
    ```

1. If you have more than one subscription, select the subscription where your resource is located.

    ```azurecli
    az account set --subscription $subscriptionId
    ```

1. Set the following environment variables with the name of the Foundry Tools resource you plan to use and resource group.

    ```azurecli
    accountName="<ai-services-resource-name>"
    resourceGroupName="<resource-group>"
    location="eastus2"
    ```

1. If you didn't create a Foundry Tools account yet, create one.

    ```azurecli
    az cognitiveservices account create -n $accountName -g $resourceGroupName --custom-domain $accountName --location $location --kind AIServices --sku S0
    ```

1. Check which models are available to you and under which SKU. SKUs, also known as [deployment types](../../concepts/deployment-types.md), define how Azure infrastructure is used to process requests. Models might offer different deployment types. The following command lists all the model definitions available:
    
    ```azurecli
    az cognitiveservices account list-models \
        -n $accountName \
        -g $resourceGroupName \
    | jq '.[] | { name: .name, format: .format, version: .version, sku: .skus[0].name, capacity: .skus[0].capacity.default }'
    ```

1. Outputs look as follows:

    ```output
    {
      "name": "Phi-3.5-vision-instruct",
      "format": "Microsoft",
      "version": "2",
      "sku": "GlobalStandard",
      "capacity": 1
    }
    ```

1. Identify the model you want to deploy. You need the properties `name`, `format`, `version`, and `sku`. The property `format` indicates the provider offering the model. You might also need capacity depending on the type of deployment.

1. Add the model deployment to the resource. The following example adds `Phi-3.5-vision-instruct`:

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

1. The model is ready to use.

You can deploy the same model multiple times if needed as long as it's under a different deployment name. This capability might be useful if you want to test different configurations for a given model, including content filters.

## Use the model

Deployed models in can be consumed using the [Azure AI model's inference endpoint](../../concepts/endpoints.md) for the resource. When constructing your request, indicate the parameter `model` and insert the model deployment name you have created. You can programmatically get the URI for the inference endpoint using the following code:

__Inference endpoint__

```azurecli
az cognitiveservices account show  -n $accountName -g $resourceGroupName | jq '.properties.endpoints["Azure AI Model Inference API"]'
```

To make requests to the Microsoft Foundry Models endpoint, append the route `models`, for example `https://<resource>.services.ai.azure.com/models`. You can see the API reference for the endpoint at [Azure AI Model Inference API reference page](https://aka.ms/azureai/modelinference).

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
    
