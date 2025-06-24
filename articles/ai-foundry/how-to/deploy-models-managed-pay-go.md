---
title: Deploy Azure AI Foundry Models to managed compute with pay-as-you-go billing 
titleSuffix: Azure AI Foundry
description: Learn how to deploy protected models from partners and community on Azure AI Foundry managed compute and understand how pay-as-you-go surcharge billing works.
manager: scottpolly
ms.service: azure-ai-foundry
ms.custom:
ms.topic: how-to
ms.date: 06/24/2025
ms.reviewer: tinaem
reviewer: tinaem
ms.author: mopeakande
author: msakande
---

# Deploy Azure AI Foundry Models to managed compute with pay-as-you-go billing 

Azure AI Foundry Models include a comprehensive catalog of models organized into two categories—Models sold directly by Azure, and [Models from partners and community](../concepts/foundry-models-overview.md#models-from-partners-and-community). These models from partners and community, which are available for deployment on a managed compute, are either open or protected models. In this article, you learn how to use protected models from partners and community, offered via Azure Marketplace for deployment on managed compute with pay-as-you-go billing. 


## Prerequisites

- An Azure subscription with a valid payment method. Free or trial Azure subscriptions won't work. If you don't have an Azure subscription, create a [paid Azure account](https://azure.microsoft.com/pricing/purchase-options/pay-as-you-go) to begin.

- If you don't have one, [create a [!INCLUDE [hub](../includes/hub-project-name.md)]](create-projects.md?pivots=hub-project).

- [Azure Marketplace purchases enabled](/azure/cost-management-billing/manage/enable-marketplace-purchases) for your Azure subscription.

- Azure role-based access controls (Azure RBAC) are used to grant access to operations in Azure AI Foundry portal. To perform the steps in this article, your user account must be assigned a *custom role* with the following permissions. User accounts assigned the *Owner* or *Contributor* role for the Azure subscription can also create deployments. For more information on permissions, see [Role-based access control in Azure AI Foundry portal](/azure/ai-foundry/concepts/rbac-azure-ai-foundry).


- On the Azure subscription— **to subscribe the workspace/project to the Azure Marketplace offering**:

  - Microsoft.MarketplaceOrdering/agreements/offers/plans/read
  - Microsoft.MarketplaceOrdering/agreements/offers/plans/sign/action
  - Microsoft.MarketplaceOrdering/offerTypes/publishers/offers/plans/agreements/read
  - Microsoft.Marketplace/offerTypes/publishers/offers/plans/agreements/read
  - Microsoft.SaaS/register/action

- On the resource group— **to create and use the SaaS resource**:

  - Microsoft.SaaS/resources/read
  - Microsoft.SaaS/resources/write

- On the workspace— **to deploy endpoints**:

  - Microsoft.MachineLearningServices/workspaces/marketplaceModelSubscriptions/*
  - Microsoft.MachineLearningServices/workspaces/onlineEndpoints/*

## Subscription scope and unit of measure for Azure Marketplace offer

Azure AI Foundry enables a seamless subscription and transaction experience for protected models as you create and consume your dedicated model deployments at scale. The deployment of protected models on managed compute involves pay-as-you-go billing for the customer in two dimensions: 

- Per-hour Azure Machine Learning compute billing for the virtual machines employed in the deployment.
- Surcharge billing for the model as set by the model publisher on the Azure Marketplace offer. 

Pay-as-you-go billing of Azure compute and model surcharge is pro-rated per minute based on the uptime of the managed online deployments. The surcharge for a model is a per GPU-hour price, set by the partner (or model's publisher) on Azure Marketplace, for all the supported GPUs that can be used to deploy the model on Azure AI Foundry managed compute.  

A user's subscription to Azure Marketplace offers are scoped to the project resource within Azure AI Foundry. If a subscription to the Azure Marketplace offer for a particular model already exists within the project, the user is informed in the deployment wizard that the subscription already exists for the project. 

> [!NOTE]
> For [NVIDIA inference microservices (NIM)](#nvidia), multiple models are associated with a single marketplace offer, so you have to subscribe to the NIM offer only once within a project to be able to deploy all NIMs offered by NVIDIA in the AI Foundry model catalog. If you want to deploy NIMs in a different project with no existing SaaS subscription, you need to resubscribe to the offer.  

To find all the SaaS subscriptions that exist in an Azure subscription:

1. Sign in to the [Azure portal](https://portal.azure.com) and go to your Azure subscription.

1. Select **Subscriptions** and then select your Azure subscription to open its overview page.

1. Select **Settings** > **Resources**  to see the list of resources.

1. Use the **Type** filter to select the SaaS resource type.
 
The consumption-based surcharge is accrued to the associated SaaS subscription and billed to a user via Azure Marketplace. You can view the invoice in the **Overview** tab of the respective SaaS subscription.

## Subscribe and deploy on managed compute

[!INCLUDE [tip-left-pane](../includes/tip-left-pane.md)]

1. Sign in to [Azure AI Foundry](https://ai.azure.com/?cid=learnDocs).
1. If you're not already in your project, select it. 
1. Select **Model catalog** from the left pane.
1. Select the **Deployment options** filter in the model catalog and choose **Managed compute**.
1. Filter the list further by selecting the **Collection** and model of your choice. In this article, we use **Cohere Command A** from the [list of supported models](#supported-models) for illustration.
1. From the model's page, select **Use this model** to open the deployment wizard.
1. Choose from one of the supported VM SKUs for the model. You need to have Azure Machine Learning Compute quota for that SKU in your Azure subscription.
1. Select **Customize** to specify your deployment configuration for parameters such as the instance count. You can also select an existing endpoint for the deployment or create a new one. For this example, we specify an instance count of **1** and create a new endpoint for the deployment.

    :::image type="content" source="../media/deploy-models-managed-pay-go/deployment-configuration.png" alt-text="Screenshot of the deployment configuration screen for a protected model in Azure AI Foundry." lightbox="../media/deploy-models-managed-pay-go/deployment-configuration.png":::

1. Select **Next** to proceed to the *pricing breakdown* page.
1. Review the pricing breakdown for the deployment, terms of use, and license agreement associated with the model's offer on Azure Marketplace. The pricing breakdown tells you what the aggregated pricing for the deployed model would be, where the surcharge for the model is a function of the number of GPUs in the VM instance that is selected in the previous steps. In addition to the applicable surcharge for the model, Azure compute charges also apply, based on your deployment configuration. If you have existing reservations or Azure savings plan, the invoice for the compute charges honors and reflects the discounted VM pricing.

    :::image type="content" source="../media/deploy-models-managed-pay-go/pricing-breakdown.png" alt-text="Screenshot of the pricing breakdown page for a protected model deployment in Azure AI Foundry." lightbox="../media/deploy-models-managed-pay-go/pricing-breakdown.png":::

1. Select the checkbox to acknowledge that you understand and agree to the terms of use. Then, select **Deploy**. Azure AI Foundry creates the user's subscription to the marketplace offer and then creates the deployment of the model on a managed compute. It takes about 15-20 minutes for the deployment to complete.

## Consume deployments

After your deployment is successfully created, you can follow these steps to consume it:

1. Select **Models + Endpoints** under _My assets_ in your Azure AI Foundry project.
1. Select your deployment from the **Model deployments** tab.
1. Navigate to the **Test** tab for sample inference to the endpoint.
1. Return to the **Details** tab and select **Open in Playground** to go to the chat playground and modify parameters for the inference requests.   

## Network isolation of deployments

Collections in the model catalog can be deployed within your isolated networks using workspace managed virtual network. For more information on how to configure your workspace managed networks, see [Configure a managed virtual network to allow internet outbound](../../machine-learning/how-to-managed-network.md#configure-a-managed-virtual-network-to-allow-internet-outbound).

#### Limitation

An Azure AI Foundry project with ingress Public Network Access disabled can only support a single active deployment of one of the protected models from the catalog. Attempts to create more active deployments result in deployment creation failures.

## Supported models 

The following sections list the supported models for managed compute deployment with pay-as-you-go billing, grouped by collection.

### Paige AI

| Model | Task |
|--|--|
| [Virchow2G](https://ai.azure.com/explore/models/Virchow2G/version/1/registry/azureml-paige) | Image Feature Extraction |
| [Virchow2G-Mini](https://ai.azure.com/explore/models/Virchow2G-Mini/version/1/registry/azureml-paige) | Image Feature Extraction |

### Cohere

| Model | Task |
|--|--|
| [Command A](https://ai.azure.com/explore/models/cohere-command-a/version/3/registry/azureml-cohere) | Chat completion |
| [Embed v4](https://ai.azure.com/explore/models/embed-v-4-0/version/4/registry/azureml-cohere) | Embeddings |
| [Rerank v3.5](https://ai.azure.com/explore/models/Cohere-rerank-v3.5/version/2/registry/azureml-cohere) | Text classification |

### NVIDIA

NVIDIA inference microservices (NIM) are containers built by NVIDIA for optimized pretrained and customized AI models serving on NVIDIA GPUs. NVIDIA NIMs available on Azure AI Foundry model catalog can be deployed with a Standard subscription to the [NVIDIA NIM SaaS offer](https://aka.ms/nvidia-nims-plan) on Azure Marketplace.

Some special things to note about NIMs are:

- **NIMs include a 90-day trial**. The trial applies to all NIMs associated with a particular SaaS subscription, and starts from the time the SaaS subscription is created.

- **SaaS subscriptions scope to an Azure AI Foundry project**. Because multiple models are associated with a single Azure Marketplace offer, you only need to subscribe once to the NIM offer within a project, then you're able to deploy all the NIMs offered by NVIDIA in the AI Foundry model catalog. If you want to deploy NIMs in a different project with no existing SaaS subscription, you need to resubscribe to the offer.  


| Model | Task |
|--|--|
| [Llama-3.3-Nemotron-Super-49B-v1-NIM-microservice](https://ai.azure.com/explore/models/Llama-3.3-Nemotron-Super-49B-v1-NIM-microservice/version/2/registry/azureml-nvidia) | Chat completion |
| [Llama-3.1-Nemotron-Nano-8B-v1-NIM-microservice](https://ai.azure.com/explore/models/Llama-3.1-Nemotron-Nano-8B-v1-NIM-microservice/version/2/registry/azureml-nvidia) | Chat completion |
| [Deepseek-R1-Distill-Llama-8B-NIM-microservice](https://ai.azure.com/explore/models/Deepseek-R1-Distill-Llama-8B-NIM-microservice/version/2/registry/azureml-nvidia) | Chat completion |
| [Llama-3.3-70B-Instruct-NIM-microservice](https://ai.azure.com/explore/models/Llama-3.3-70B-Instruct-NIM-microservice/version/2/registry/azureml-nvidia) | Chat completion |
| [Llama-3.1-8B-Instruct-NIM-microservice](https://ai.azure.com/explore/models/Llama-3.1-8B-Instruct-NIM-microservice/version/3/registry/azureml-nvidia) | Chat completion |
| [Mistral-7B-Instruct-v0.3-NIM-microservice](https://ai.azure.com/explore/models/Mistral-7B-Instruct-v0.3-NIM-microservice/version/2/registry/azureml-nvidia) | Chat completion |
| [Mixtral-8x7B-Instruct-v0.1-NIM-microservice](https://ai.azure.com/explore/models/Mixtral-8x7B-Instruct-v0.1-NIM-microservice/version/2/registry/azureml-nvidia) | Chat completion |
| [Llama-3.2-NV-embedqa-1b-v2-NIM-microservice](https://ai.azure.com/explore/models/Llama-3.2-NV-embedqa-1b-v2-NIM-microservice/version/2/registry/azureml-nvidia) | Embeddings |
| [Llama-3.2-NV-rerankqa-1b-v2-NIM-microservice](https://ai.azure.com/explore/models/Llama-3.2-NV-rerankqa-1b-v2-NIM-microservice/version/2/registry/azureml-nvidia) | Text classification |
| [Openfold2-NIM-microservice](https://ai.azure.com/explore/models/Openfold2-NIM-microservice/version/3/registry/azureml-nvidia) | Protein Binder |
| [ProteinMPNN-NIM-microservice](https://ai.azure.com/explore/models/ProteinMPNN-NIM-microservice/version/2/registry/azureml-nvidia) | Protein Binder |
| [MSA-search-NIM-microservice](https://ai.azure.com/explore/models/MSA-search-NIM-microservice/version/3/registry/azureml-nvidia) | Protein Binder |
| [Rfdiffusion-NIM-microservice](https://ai.azure.com/explore/models/Rfdiffusion-NIM-microservice/version/1/registry/azureml-nvidia) | Protein Binder |

### Consume NVIDIA NIM deployments

After your deployment is successfully created, you can follow the steps in [Consume deployments](#consume-deployments) to consume it.

NVIDIA NIMs on Azure AI Foundry expose an OpenAI compatible API. See the [API reference](https://docs.nvidia.com/nim/large-language-models/latest/api-reference.html#) to learn more about the payload supported. The `model` parameter for NIMs on Azure AI Foundry is set to a default value within the container and isn't required to be passed in to the request payload to your online endpoint. The **Consume** tab of the NIM deployment on Azure AI Foundry includes code samples for inference with the target URL of your deployment. 

You can also consume NIM deployments using the [Azure AI Foundry Models SDK](/python/api/overview/azure/ai-inference-readme), with limitations that include:

- No support for [creating and authenticating clients using `load_client`](/python/api/overview/azure/ai-inference-readme#create-and-authenticate-clients-using-load_client).
- You should call client method `get_model_info` to [retrieve model information](/python/api/overview/azure/ai-inference-readme#get-ai-model-information).

### Develop and run agents with NIM endpoints

The following NVIDIA NIMs of **chat completions** task type in the model catalog can be used to [create and run agents using Agent Service](/python/api/overview/azure/ai-projects-readme#agents-preview) using various supported tools, with the following two extra requirements: 

1. Create a _Serverless Connection_ to the project using the NIM endpoint and Key. The target URL for the NIM endpoint in the connection should be `https://<endpoint-name>.region.inference.ml.azure.com/v1/`. 
1. Set the _model parameter_ in the request body to be of the form, `https://<endpoint>.region.inference.ml.azure.com/v1/@<parameter value per table below>` while creating and running agents.


| NVIDIA NIM                                         | `model` parameter value           |
|----------------------------------------------------|----------------------------------|
| Llama-3.3-70B-Instruct-NIM-microservice            | meta/llama-3.3-70b-instruct      |
| Llama-3.1-8B-Instruct-NIM-microservice             | meta/llama-3.1-8b-instruct       |
| Mistral-7B-Instruct-v0.3-NIM-microservice          | mistralai/mistral-7b-instruct-v0.3 |


### Security scanning

NVIDIA ensures the security and reliability of NVIDIA NIM container images through best-in-class vulnerability scanning, rigorous patch management, and transparent processes. To learn more about security scanning, see the [security page](https://docs.nvidia.com/ai-enterprise/planning-resource/security-for-azure-ai-foundry/latest/introduction.html). Microsoft works with NVIDIA to get the latest patches of the NIMs to deliver secure, stable, and reliable production-grade software within Azure AI Foundry.

You can refer to the _last updated time_ for the NIM on the right pane of the model's overview page. You can redeploy to consume the latest version of NIM from NVIDIA on Azure AI Foundry. 



## Related content

* [How to deploy and inference a managed compute deployment](deploy-models-managed.md)
* [Explore Azure AI Foundry Models](../concepts/foundry-models-overview.md)

