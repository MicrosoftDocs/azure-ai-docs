---
title: Add and configure models to Microsoft Foundry using code
titleSuffix: Microsoft Foundry
description: Learn how to add and configure Microsoft Foundry Models in your Foundry resource for use in inferencing applications.
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: how-to
ms.date: 01/20/2026
ms.custom: ignite-2024, github-universe-2024
author: msakande   
ms.author: mopeakande
recommendations: false
zone_pivot_groups: azure-ai-create-deployment
monikerRange: 'foundry-classic || foundry'
ai.usage: ai-assisted

#CustomerIntent: As a developer or AI practitioner, I want to deploy Microsoft Foundry Models using code, so that I can integrate these AI models into my applications and perform inference tasks for my business needs.
---

# Deploy Microsoft Foundry Models using code

[!INCLUDE [version-banner](../../includes/version-banner.md)]

[!INCLUDE [migrate-model-inference-to-v1-openai](../../includes/migrate-model-inference-to-v1-openai.md)]

You can decide and configure which models are available for inference in your Microsoft Foundry resource. When you configure a model, you can generate predictions from it by specifying its model name or deployment name in your requests. You don't need to make any other changes in your code to use the model.

In this article, you learn how to add a new model to a Foundry Models endpoint.

## Prerequisites

To complete this article, you need:

* An Azure subscription. If you're using [GitHub Models](https://docs.github.com/en/github-models/), you can upgrade your experience and create an Azure subscription in the process. Read [Upgrade from GitHub Models to Microsoft Foundry Models](quickstart-github-models.md) if that's your case.

* A Foundry project. This kind of project is managed under a Foundry resource (formerly known as Azure AI Services resource). If you don't have a Foundry project, see [Create a project for Microsoft Foundry](../../how-to/create-projects.md).


* [Foundry Models from partners and community](../concepts/models-from-partners.md) require access to **Azure Marketplace**. Ensure you have the [permissions required to subscribe to model offerings](../how-to/configure-marketplace.md). [Foundry Models sold directly by Azure](../concepts/models-sold-directly-by-azure.md) don't have this requirement.

::: zone pivot="programming-language-cli"

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

1. Check which models are available to you and under which SKU. SKUs, also known as [deployment types](../concepts/deployment-types.md), define how Azure infrastructure is used to process requests. Models might offer different deployment types. The following command lists all the model definitions available:
    
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

Deployed models can be consumed using the [Endpoints for Microsoft Foundry Models](../concepts/endpoints.md) for the resource. When constructing your request, indicate the parameter `model` and insert the model deployment name you have created. You can programmatically get the URI for the inference endpoint using the following code:

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

::: zone-end

::: zone pivot="programming-language-bicep"

* Install the [Azure CLI](/cli/azure/).

* Identify the following information:

  * Your Azure subscription ID.

  * Your Foundry resource (formerly known as Azure AI Services resource) name.

  * The resource group where the Foundry resource is deployed.

  * The model name, provider, version, and SKU you want to deploy. You can use the Foundry portal or the Azure CLI to find this information. In this example, you deploy the following model:

    * **Model name:**: `Phi-3.5-vision-instruct`
    * **Provider**: `Microsoft`
    * **Version**: `2`
    * **Deployment type**: Global standard

## About this tutorial

The example in this article is based on code samples contained in the [Azure-Samples/azureai-model-inference-bicep](https://github.com/Azure-Samples/azureai-model-inference-bicep) repository. To run the commands locally without having to copy or paste file content, use the following commands to clone the repository and go to the folder for your coding language:

```azurecli
git clone https://github.com/Azure-Samples/azureai-model-inference-bicep
```

The files for this example are in:

```azurecli
cd azureai-model-inference-bicep/infra
```

[!INCLUDE [rbac](../includes/configure-marketplace/rbac.md)]
## Add the model

1. Use the template `ai-services-deployment-template.bicep` to describe model deployments:

    __ai-services-deployment-template.bicep__

    :::code language="bicep" source="~/azureai-model-inference-bicep/infra/modules/ai-services-deployment-template.bicep":::

1. Run the deployment:

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

Deployed models can be consumed using the [Endpoints for Microsoft Foundry Models](../concepts/endpoints.md) for the resource. When constructing your request, indicate the parameter `model` and insert the model deployment name you have created. You can programmatically get the URI for the inference endpoint using the following code:

__Inference endpoint__

```azurecli
az cognitiveservices account show  -n $accountName -g $resourceGroupName | jq '.properties.endpoints["Azure AI Model Inference API"]'
```

To make requests to the Foundry Models endpoint, append the route `models`, for example `https://<resource>.services.ai.azure.com/models`. You can see the API reference for the endpoint at [Azure AI Model Inference API reference page](https://aka.ms/azureai/modelinference).

__Inference keys__

```azurecli
az cognitiveservices account keys list  -n $accountName -g $resourceGroupName
```


::: zone-end

## Next step

- [How to generate text responses with Microsoft Foundry Models](generate-responses.md)