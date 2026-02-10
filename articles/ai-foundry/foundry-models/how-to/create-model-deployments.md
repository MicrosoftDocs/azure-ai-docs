---
title: Deploy models using Azure CLI and Bicep
titleSuffix: Microsoft Foundry
description: Learn how to add and configure Microsoft Foundry Models in your Foundry resource for use in inference applications using Azure CLI and Bicep templates.
#customer intent: As an AI practitioner, I want to configure model deployments with Azure CLI or Bicep templates so that I can automate and standardize the deployment process.
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: how-to
ms.date: 02/09/2026
ms.custom: ignite-2024, github-universe-2024, dev-focus, pilot-ai-workflow-jan-2026
author: msakande
ms.author: mopeakande
recommendations: false
zone_pivot_groups: azure-ai-create-deployment
monikerRange: 'foundry-classic || foundry'
ai-usage: ai-assisted

#CustomerIntent: As a developer or AI practitioner, I want to deploy Microsoft Foundry Models using Azure CLI and Bicep, so that I can integrate these AI models into my applications and perform inference tasks for my business needs.
---

# Deploy models using Azure CLI and Bicep

[!INCLUDE [version-banner](../../includes/version-banner.md)]

[!INCLUDE [migrate-model-inference-to-v1-openai](../../includes/migrate-model-inference-to-v1-openai.md)]

In this article, you learn how to add a new model deployment to a Foundry Models endpoint. The deployment is available for inference in your Foundry resource when you specify the deployment name in your requests.

## Prerequisites

To complete this article, you need the following:

* An Azure subscription. If you're using [GitHub Models](https://docs.github.com/en/github-models/), you can upgrade your experience and create an Azure subscription in the process. For more information, see [Upgrade from GitHub Models to Foundry Models](quickstart-github-models.md).

* A Foundry project. This project type is managed under a Foundry resource (formerly known as Azure AI Services resource). If you don't have a Foundry project, see [Create a project for Microsoft Foundry](../../how-to/create-projects.md).

* Azure role-based access control (RBAC) permissions to create and manage deployments. You need the **Cognitive Services Contributor** role or equivalent permissions for the Foundry resource.

* [Foundry Models from partners and community](../concepts/models-from-partners.md) require access to **Azure Marketplace**. Ensure you have the [permissions required to subscribe to model offerings](../how-to/configure-marketplace.md). [Foundry Models sold directly by Azure](../concepts/models-sold-directly-by-azure.md) don't have this requirement.

::: zone pivot="programming-language-cli"

* Install the [Azure CLI](/cli/azure/) (version 2.60 or later) and the `cognitiveservices` extension.

    ```azurecli
    az extension add -n cognitiveservices
    ```

* Some commands in this tutorial use the `jq` tool, which might not be installed on your system. For installation instructions, see [Download `jq`](https://stedolan.github.io/jq/download/).

* Identify the following information:

  * Your Azure subscription ID

  * Your Foundry resource name

  * The resource group where you deployed the Foundry resource
    
    
## Add models

To add a model, first identify the model that you want to deploy. Query the available models as follows:

1. Sign in to your Azure subscription.

    ```azurecli
    az login
    ```

1. If you have more than one subscription, select the subscription where your resource is located.

    ```azurecli
    az account set --subscription $subscriptionId
    ```

1. Set the following environment variables with the name of the Foundry resource you plan to use and resource group.

    ```azurecli
    accountName="<ai-services-resource-name>"
    resourceGroupName="<resource-group>"
    location="eastus2"
    ```

1. If you haven't created a Foundry resource yet, create one.

    ```azurecli
    az cognitiveservices account create -n $accountName -g $resourceGroupName --custom-domain $accountName --location $location --kind AIServices --sku S0
    ```

    Reference: [az cognitiveservices account](/cli/azure/cognitiveservices/account)

1. Check which models are available to you and under which SKU. SKUs, also known as [deployment types](../concepts/deployment-types.md), define how Azure infrastructure processes requests. Models might offer different deployment types. The following command lists all the model definitions available:
    
    ```azurecli
    az cognitiveservices account list-models \
        -n $accountName \
        -g $resourceGroupName \
    | jq '.[] | { name: .name, format: .format, version: .version, sku: .skus[0].name, capacity: .skus[0].capacity.default }'
    ```

    The output includes available models with their properties:

    ```output
    {
      "name": "Phi-3.5-vision-instruct",
      "format": "Microsoft",
      "version": "2",
      "sku": "GlobalStandard",
      "capacity": 1
    }
    ```

    Reference: [az cognitiveservices account list-models](/cli/azure/cognitiveservices/account#az-cognitiveservices-account-list-models)

1. Identify the model you want to deploy. You need the properties `name`, `format`, `version`, and `sku`. The property `format` indicates the provider offering the model. Depending on the type of deployment, you might also need capacity.

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

    Reference: [az cognitiveservices account deployment](/cli/azure/cognitiveservices/account/deployment)

1. The model is ready to use.

You can deploy the same model multiple times if needed as long as it's under a different deployment name. This capability is useful if you want to test different configurations for a given model, including content filters.

## Use the model

> [!NOTE]
> This section is identical for both the CLI and Bicep approaches.

You can consume deployed models using the [Endpoints for Foundry Models](../concepts/endpoints.md) for the resource. When you construct your request, specify the parameter `model` and insert the model deployment name you created. You can programmatically get the URI for the inference endpoint by using the following code:

**Inference endpoint**

```azurecli
az cognitiveservices account show  -n $accountName -g $resourceGroupName | jq '.properties.endpoints["Azure AI Model Inference API"]'
```

To make requests to the Foundry Models endpoint, append the route `models`. For example: `https://<resource>.services.ai.azure.com/models`. You can see the API reference for the endpoint at [Azure AI Model Inference API reference page](https://learn.microsoft.com/rest/api/aifoundry/modelinference/).

**Inference keys**

```azurecli
az cognitiveservices account keys list  -n $accountName -g $resourceGroupName
```

## Manage deployments

You can see all the deployments available using the CLI:

1. Run the following command to see all the active deployments:

    ```azurecli
    az cognitiveservices account deployment list -n $accountName -g $resourceGroupName
    ```

    Reference: [az cognitiveservices account deployment list](/cli/azure/cognitiveservices/account/deployment#az-cognitiveservices-account-deployment-list)

1. You can see the details of a given deployment:

    ```azurecli
    az cognitiveservices account deployment show \
        --deployment-name "Phi-3.5-vision-instruct" \
        -n $accountName \
        -g $resourceGroupName
    ```

    Reference: [az cognitiveservices account deployment show](/cli/azure/cognitiveservices/account/deployment#az-cognitiveservices-account-deployment-show)

1. You can delete a given deployment as follows:

    ```azurecli
    az cognitiveservices account deployment delete \
        --deployment-name "Phi-3.5-vision-instruct" \
        -n $accountName \
        -g $resourceGroupName
    ```

    Reference: [az cognitiveservices account deployment delete](/cli/azure/cognitiveservices/account/deployment#az-cognitiveservices-account-deployment-delete)

::: zone-end

::: zone pivot="programming-language-bicep"

* Install the [Azure CLI](/cli/azure/).

* Identify the following information:

  * Your Azure subscription ID

* Your Foundry resource (formerly known as Azure AI Services resource) name

* The resource group where the Foundry resource is deployed

* The model name, provider, version, and SKU you want to deploy. You can use the Foundry portal or the Azure CLI to find this information. In this example, you deploy the following model:

  * **Model name**: `Phi-3.5-vision-instruct`
  * **Provider**: `Microsoft`
  * **Version**: `2`
  * **Deployment type**: Global standard

## Set up the environment

The example in this article is based on code samples contained in the [Azure-Samples/azureai-model-inference-bicep](https://github.com/Azure-Samples/azureai-model-inference-bicep) repository. To run the commands locally without having to copy or paste file content, clone the repository:

```bash
git clone https://github.com/Azure-Samples/azureai-model-inference-bicep
```

The files for this example are in:

```bash
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

> [!NOTE]
> This section is identical for both the CLI and Bicep approaches.

You can consume deployed models using the [Endpoints for Foundry Models](../concepts/endpoints.md) for the resource. When you construct your request, specify the parameter `model` and insert the model deployment name you created. You can programmatically get the URI for the inference endpoint by using the following code:

**Inference endpoint**

```azurecli
az cognitiveservices account show  -n $accountName -g $resourceGroupName | jq '.properties.endpoints["Azure AI Model Inference API"]'
```

To make requests to the Foundry Models endpoint, append the route `models`. For example: `https://<resource>.services.ai.azure.com/models`. See the [Azure AI Model Inference API reference](/rest/api/aifoundry/modelinference/) for all supported operations.

**Inference keys**

```azurecli
az cognitiveservices account keys list  -n $accountName -g $resourceGroupName
```

::: zone-end

## Troubleshooting

| Error | Cause | Resolution |
| --- | --- | --- |
| **Quota exceeded** | Your subscription reached the deployment quota for the selected SKU or region. | Check your quota in the Foundry portal or request an increase through Azure support. |
| **Authorization failed** | The identity used doesn't have the required RBAC role. | Assign the **Cognitive Services Contributor** role on the Foundry resource. |
| **Model not available** | The model isn't available in your region or subscription. | Run `az cognitiveservices account list-models` to check available models and regions. |
| **Extension not found** | The `cognitiveservices` CLI extension isn't installed. | Run `az extension add -n cognitiveservices` to install the extension. |

## Related content

- [Generate text responses with Foundry Models](generate-responses.md)
- [Deployment types in Foundry Models](../concepts/deployment-types.md)
- [Deploy Foundry Models to managed compute](deploy-foundry-models.md)
- [Quotas and limits for Foundry Models](../quotas-limits.md)
