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
ms.custom:  devx-track-azurecli
---

# How to deploy NVIDIA Inference Microservices

In this article, you learn how to deploy NVIDIA Inference Microservices (NIMs) on Managed Compute in the model catalog on Foundry​. NVIDIA inference microservices are containers built by NVIDIA for optimized pre-trained and customized AI models serving on NVIDIA GPUs​. 
Get improved TCO and performance with NVIDIA NIMs offered for one-click deployment on Foundry, with enterprise production-grade software under NVIDIA AI Enterprise license. 

[!INCLUDE [models-preview](../includes/models-preview.md)]

## Prerequisites

- An Azure subscription with a valid payment method. Free or trial Azure subscriptions won't work. If you don't have an Azure subscription, create a [paid Azure account](https://azure.microsoft.com/pricing/purchase-options/pay-as-you-go) to begin.

- An [Azure AI Foundry hub](create-azure-ai-resource.md).

- An [Azure AI Foundry project](create-projects.md).

- Ensure Marketplace purcharses are enabled for your azure subscription. Learn more about it [here](https://learn.microsoft.com/en-us/azure/cost-management-billing/manage/enable-marketplace-purchases).

- Azure role-based access controls (Azure RBAC) are used to grant access to operations in Azure AI Foundry portal. To perform the steps in this article, your user account must be assigned a _custom role_ with the following permissions. User accounts assigned the _Owner_ or _Contributor_ role for the Azure subscription can also create NIM deployments. For more information on permissions, see [Role-based access control in Azure AI Foundry portal](../concepts/rbac-ai-foundry.md).

    •	On the Azure subscription—*to subscribe the workspace to the Azure Marketplace offering*, once for each workspace/project:
        o	Microsoft.MarketplaceOrdering/agreements/offers/plans/read
        o	Microsoft.MarketplaceOrdering/agreements/offers/plans/sign/action
        o	Microsoft.MarketplaceOrdering/offerTypes/publishers/offers/plans/agreements/read
        o	Microsoft.Marketplace/offerTypes/publishers/offers/plans/agreements/read
        o	Microsoft.SaaS/register/action

    •	On the resource group—*to create and use the SaaS resource*:
        o   Microsoft.SaaS/resources/read
        o	Microsoft.SaaS/resources/write

    •	On the workspace—to deploy endpoints (the Azure Machine Learning data scientist role contains these permissions already):
        o	Microsoft.MachineLearningServices/workspaces/marketplaceModelSubscriptions/*
        o	Microsoft.MachineLearningServices/workspaces/onlineEndpoints/* 


## NVIDIA NIM PayGo offer on Azure Marketplace by NVIDIA

 NVIDIA NIMs available on Azure AI Foundry model catalog can be deployed with a suscription to the [NVIDIA NIM SaaS offer](https://aka.ms/nvidia-nims-plan) on Azure Marketplace. This offer includes a 90-day trial that applies to all NIMs associated with a particular SaaS subscription scoped to a Azure AI Foundry project, and has a PayGo price of $1 per GPU hour post the trial period. 

 Azure AI Foundry enables a seamless purchase flow of the NVIDIA NIM offering on Marketplace from NVIDIA collection in the model catalog, and further deployment on Managed Compute.

## Deploy NVIDIA Inference Microservices on Managed Compute

1. Sign in to [Azure AI Foundry](https://ai.azure.com) and go to the **Home** page.
2. Select **Model catalog** from the left sidebar.
3. In the filters section, select **Collections** and select **NVIDIA**.

:::image type="content" source="../media/how-to/deploy-nim/nvidia-collections.png" alt-text="A screenshot showing how to filter by NVIDIA collections models in the catalog." lightbox="../media/how-to/deploy-nim/nvidia-collections.png":::  

1. Select the NVIDIA NIM of your choice. In this article, we will be using **Llama-3.3-70B-Instruct-NIM-microservice** as an example.
1. Select **Deploy**.
1. Select one of the NVIDIA GPU based VM SKUs supported for the NIM, based on your intended workload. You will need to have quota in your Azure subscription.
1. You can then customize your deployment configuration for the instance count, endpoint selection/creation, etc. For the example in this article, we will consider an instance count of **2** and create a new endpoint. 
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
