---
title: How to deploy NVIDIA Inference Microservices
titleSuffix: Azure AI Foundry
description: Learn to deploy NVIDIA Inference Microservices, using Azure AI Foundry.
manager: scottpolly
ms.service: azure-ai-foundry
ms.topic: how-to
ms.date: 03/14/2024
ms.author: ssalgado
author: ssalgadodev
ms.reviewer: tinaem
reviewer: tinaem
ms.custom:  serverless, devx-track-azurecli
---

# How to deploy NVIDIA Inference Microservices

In this article, you learn how to deploy NVIDIA Inference Microservices (NIMs) on Managed Compute in Foundry Catalog​. NVIDIA inference microservices are containers built by NVIDIA for optimized pre-trained and customized AI models serving on NVIDIA GPUs​.

(Summary on what benefits the customers get from NIMs)

[!INCLUDE [models-preview](../includes/models-preview.md)]



## Prerequisites

- An Azure subscription with a valid payment method. Free or trial Azure subscriptions won't work. If you don't have an Azure subscription, create a [paid Azure account](https://azure.microsoft.com/pricing/purchase-options/pay-as-you-go) to begin.

- An [Azure AI Foundry hub](create-azure-ai-resource.md).

- An [Azure AI Foundry project](create-projects.md).

- Azure role-based access controls (Azure RBAC) are used to grant access to operations in Azure AI Foundry portal. To perform the steps in this article, your user account must be assigned the __Azure AI Developer role__ on the resource group. For more information on permissions, see [Role-based access control in Azure AI Foundry portal](../concepts/rbac-ai-foundry.md).

- You need to install the following software to work with Azure AI Foundry:

    # [Azure AI Foundry portal](#tab/azure-ai-studio)

    You can use any compatible web browser to navigate [Azure AI Foundry](https://ai.azure.com).

    # [Azure CLI](#tab/cli)

    The [Azure CLI](/cli/azure/) and the [ml extension for Azure Machine Learning](/azure/machine-learning/how-to-configure-cli).

    ```azurecli
    az extension add -n ml
    ```

    If you already have the extension installed, ensure the latest version is installed.

    ```azurecli
    az extension update -n ml
    ```

    Once the extension is installed, configure it:

    ```azurecli
    az account set --subscription <subscription>
    az configure --defaults workspace=<project-name> group=<resource-group> location=<location>
    ```

    # [Python SDK](#tab/python)

    Install the [Azure Machine Learning SDK for Python](https://aka.ms/sdk-v2-install).

    ```python
    pip install -U azure-ai-ml
    ```

    Once installed, import necessary namespaces and create a client connected to your project:

    ```python
    from azure.ai.ml import MLClient
    from azure.identity import InteractiveBrowserCredential
    from azure.ai.ml.entities import MarketplaceSubscription, ServerlessEndpoint

    client = MLClient(
        credential=InteractiveBrowserCredential(tenant_id="<tenant-id>"),
        subscription_id="<subscription-id>",
        resource_group_name="<resource-group>",
        workspace_name="<project-name>",
    )
    ```

    # [Bicep](#tab/bicep)

    Install the Azure CLI as described at [Azure CLI](/cli/azure/).

    Configure the following environment variables according to your settings:

    ```azurecli
    RESOURCE_GROUP="serverless-models-dev"
    LOCATION="eastus2" 
    ```  

    # [ARM](#tab/arm)

    You can use any compatible web browser to [deploy ARM templates](/azure/azure-resource-manager/templates/deploy-portal) in the Microsoft Azure portal or use any of the deployment tools. This tutorial uses the [Azure CLI](/cli/azure/).


## Subscribe your project to the model offering

(Explain how to subscribe and start using the NIMs)

## Deploy NVIDIA Inference Microservices on Managed Compute

1. Sign in to [Azure AI Foundry](https://ai.azure.com) and go to the **Home** page.
1. Select **Model catalog** from the left sidebar.
1. In the filters section, select **Collections** and select **NVIDIA**

:::image type="content" source="../media/how-to/deploy-nim/nvidia-collections.png" alt-text="A screenshot showing how to filter by NVIDIA collections models in the catalog." lightbox="../media/how-to/deploy-nim/nvidia-collections.png":::  

1. Select your desired model. In this case we will be using **Meta-Llama-3.1-70B-NIM**.
1. Select **Deploy**.
1. Select the NVIDIA GPU based VM SKU based on your intended workload. You will need to have quota in your Azure subscription.
1. You can then customize your deployment configuration such as instance count and endpoint name. For this example you will need an instance count of **2** and create a new endpoint. 
1. Select **Next**
1. You will then need to review the user payment agreement. This will tell you what the aggregated surcharge would be for the deployment, which is a function of number of NVIDIA GPUs in the VM instance selected in the previous steps.

:::image type="content" source="../media/how-to/deploy-nim/payment-description.png" alt-text="A screenshot showing the necessary user payment agreement detailing how the user will be charged for deploying the models." lightbox="../media/how-to/deploy-nim/payment-description.png":::  

1. Then, select **Deploy**.

:::image type="content" source="../media/how-to/deploy-nim/deploy-nim.png" alt-text="A screenshot showing the deploy model button in the deployment wizard." lightbox="../media/how-to/deploy-nim/deploy-nim.png"::: 


## Delete endpoints and subscriptions


## Cost and quota considerations for NVIDIA Inference Microservices


#### Cost 




## Related content

* [Region availability for models in serverless API endpoints](deploy-models-serverless-availability.md)
* [Fine-tune models using serverless API](../how-to/fine-tune-serverless.md)
