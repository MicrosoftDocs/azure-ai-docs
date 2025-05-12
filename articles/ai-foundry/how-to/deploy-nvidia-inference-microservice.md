---
title: How to deploy NVIDIA Inference Microservices
titleSuffix: Azure AI Foundry
description: Learn to deploy NVIDIA Inference Microservices, using Azure AI Foundry.
manager: scottpolly
ms.service: azure-ai-foundry
ms.topic: how-to
ms.date: 03/19/2025
ms.author: ssalgado
author: ssalgadodev
ms.reviewer: tinaem
reviewer: tinaem
ms.custom:  devx-track-azurecli
---

# How to deploy NVIDIA Inference Microservices

In this article, you learn how to deploy NVIDIA Inference Microservices (NIMs) on Managed Compute in the model catalog on Foundry​. 

NVIDIA inference microservices are containers built by NVIDIA for optimized pretrained and customized AI models serving on NVIDIA GPUs​. Get increased throughput and reduced total cost of ownership with NVIDIA NIMs offered for managed compute deployment on Foundry, with enterprise production-grade software under NVIDIA AI Enterprise license. 

[!INCLUDE [models-preview](../includes/models-preview.md)]

## Prerequisites

- An Azure subscription with a valid payment method. Free or trial Azure subscriptions won't work. If you don't have an Azure subscription, create a [paid Azure account](https://azure.microsoft.com/pricing/purchase-options/pay-as-you-go) to begin.

- An [Azure AI Foundry project](create-projects.md).

- Marketplace purchases enabled for your Azure subscription. Learn more [here](/azure/cost-management-billing/manage/enable-marketplace-purchases).

- Azure role-based access controls (Azure RBAC) are used to grant access to operations in Azure AI Foundry portal. To perform the steps in this article, your user account must be assigned a _custom role_ with the following permissions. User accounts assigned the _Owner_ or _Contributor_ role for the Azure subscription can also create NIM deployments. For more information on permissions, see [Role-based access control in Azure AI Foundry portal](../concepts/rbac-azure-ai-foundry.md).

    -    On the Azure subscription—**to subscribe the workspace to the Azure Marketplace offering**, once for each workspace/project:
        -    Microsoft.MarketplaceOrdering/agreements/offers/plans/read
        -    Microsoft.MarketplaceOrdering/agreements/offers/plans/sign/action
        -    Microsoft.MarketplaceOrdering/offerTypes/publishers/offers/plans/agreements/read
        -    Microsoft.Marketplace/offerTypes/publishers/offers/plans/agreements/read
        -    Microsoft.SaaS/register/action

    -    On the resource group—**to create and use the SaaS resource**:
        -   Microsoft.SaaS/resources/read
        -    Microsoft.SaaS/resources/write

    -    On the workspace—**to deploy endpoints**:
        -    Microsoft.MachineLearningServices/workspaces/marketplaceModelSubscriptions/*
        -    Microsoft.MachineLearningServices/workspaces/onlineEndpoints/* 


## NVIDIA NIM Standard deployment on Azure Marketplace by NVIDIA

 NVIDIA NIMs available on Azure AI Foundry model catalog can be deployed with a Standard subscription to the [NVIDIA NIM SaaS offer](https://aka.ms/nvidia-nims-plan) on Azure Marketplace. This offer includes a 90-day trial and a Standard price of $1 per GPU hour post the trial period. The trial applies to all NIMs associated with a particular SaaS subscription, and starts from the time the SaaS subscription was created. SaaS subscriptions scope to an Azure AI Foundry project, so you have to subscribe to the NIM offer only once within a project, then you are able to deploy all NIMs offered by NVIDIA in the AI Foundry model catalog. If you want to deploy NIM in a different project with no existing SaaS subscription, you will have to resubscribe to the offer.  

 Azure AI Foundry enables a seamless purchase experience of the NVIDIA NIM offering on Marketplace from the NVIDIA collection in the model catalog, and further deployment on managed compute.

## Deploy NVIDIA Inference Microservices on Managed Compute

[!INCLUDE [tip-left-pane](../includes/tip-left-pane.md)]

1. Sign in to [Azure AI Foundry](https://ai.azure.com) and go to the **Home** page.
2. Select **Model catalog** from the left sidebar.
3. In the filters section, select **Collections** and select **NVIDIA**.

:::image type="content" source="../media/how-to/deploy-nvidia-inference-microservice/nvidia-collections.png" alt-text="A screenshot showing the Nvidia inference microservices available in the model catalog." lightbox="../media/how-to/deploy-nvidia-inference-microservice/nvidia-collections.png":::  

4. Select the NVIDIA NIM of your choice. In this article, we are using **Llama-3.3-70B-Instruct-NIM-microservice** as an example.
5. Select **Deploy**.
6. Select one of the NVIDIA GPUs accelerated Azure Machine Learning VM SKUs supported for the NIM, based on your intended workload. You need to have quota in your Azure subscription.
7. You can then customize your deployment configuration for the instance count and select an existing endpoint or create a new one. For the example in this article, we consider an instance count of **1** and create a new endpoint. 

:::image type="content" source="../media/how-to/deploy-nvidia-inference-microservice/project-customization.png" alt-text="A screenshot showing project customization options in the deployment wizard." lightbox="../media/how-to/deploy-nvidia-inference-microservice/project-customization.png"::: 

8. Select **Next**
9. Then, review the pricing breakdown for the NIM deployment, terms of use and license agreement associated with the NIM offer. The pricing breakdown helps inform what the aggregated pricing for the NIM software deployed would be, which is a function of the number of NVIDIA GPUs in the VM instance that is selected in the previous steps. In addition to the applicable NIM software price, Azure Compute charges also apply based on your deployment configuration.

:::image type="content" source="../media/how-to/deploy-nvidia-inference-microservice/payment-description.png" alt-text="A screenshot showing the necessary user payment agreement detailing how the user is charged for deploying the models." lightbox="../media/how-to/deploy-nvidia-inference-microservice/payment-description.png":::  

10. Select the checkbox to acknowledge understanding of pricing and terms of use, and then, click **Deploy**. 

## Consume NVIDIA NIM deployments

After your deployment is successfully created, you can go to **Models + Endpoints** under _My assets_ in your Azure AI Foundry project, select your deployment under **Model deployments** and navigate to the Test tab for sample inference to the endpoint. You can also go to the Chat Playground by selecting **Open in Playground** in Deployment Details tab, to be able to modify parameters for the inference requests.   

NVIDIA NIMs on Foundry expose an OpenAI compatible API. Learn more about the payload supported [here](https://docs.nvidia.com/nim/large-language-models/latest/api-reference.html#). The 'model' parameter for NIMs on Foundry is set to a default value within the container, and is not required to be passed in the request payload to your online endpoint. The **Consume** tab of the NIM deployment on Foundry includes code samples for inference with the target URL of your deployment. 

You can also consume NIM deployments using the [Azure AI Foundry Models SDK](/python/api/overview/azure/ai-inference-readme), with limitations such as no support for [creating and authenticating clients using `load_client`](/python/api/overview/azure/ai-inference-readme#create-and-authenticate-clients-using-load_client) and calling client method `get_model_info` to [retrieve model information](/python/api/overview/azure/ai-inference-readme#get-ai-model-information).

### Develop and run agents with NIM endpoints

The following NVIDIA NIMs of **chat completions** task type in the model catalog can be used to [create and run agents using Agent Service](/python/api/overview/azure/ai-projects-readme#agents-preview) using various supported tools, with the following two additional requirements: 

1. Create a _Serverless Connection_ to the project using the NIM endpoint and Key. Note that the target URL for NIM endpoint in the connection should be `https://<endpoint-name>.region.inference.ml.azure.com/v1/`. 
2. Set the _model parameter_ in the request body to be like, `https://<endpoint>.region.inference.ml.azure.com/v1/@<parameter value per table below>` while creating and running agents.


NVIDIA NIM | `model` parameter value 
--|--
Llama-3.3-70B-Instruct-NIM-microservice | meta/llama-3.3-70b-instruct 
Llama-3.1-8B-Instruct-NIM-microservice | meta/llama-3.1-8b-instruct 
Mistral-7B-Instruct-v0.3-NIM-microservice | mistralai/mistral-7b-instruct-v0.3 


## Security scanning

NVIDIA ensures the security and reliability of NVIDIA NIM container images through best-in-class vulnerability scanning, rigorous patch management, and transparent processes. Learn more on the details [here](https://docs.nvidia.com/ai-enterprise/planning-resource/security-for-azure-ai-foundry/latest/introduction.html). Microsoft works with NVIDIA to get the latest patches of the NIMs to deliver secure, stable, and reliable production-grade software within AI Foundry.

Users can refer to the last updated time for the NIM on the right pane in the model overview page. Redeploy to consume the latest version of NIM from NVIDIA on AI Foundry. 

## Network Isolation 

Collections in the model catalog can be deployed within your isolated networks using workspace managed virtual network. For more information on how to configure your workspace managed networks, see [here.](/azure/machine-learning/how-to-managed-network#configure-a-managed-virtual-network-to-allow-internet-outbound)

### Limitation

While NIMs are in preview on Foundry, projects with ingress Public Network Access disabled have a limitation of supporting creation of only one deployment successfully. Note that there can only be a single active deployment in a private workspace, attempts to create more active deployments result in deployment creation failures. This limitation does not exist when NIMs are generally available on AI Foundry.

## Related content

* Learn more about the [Model Catalog](./model-catalog-overview.md)
* Learn more about [built-in policies for deployment](./built-in-policy-model-deployment.md)
