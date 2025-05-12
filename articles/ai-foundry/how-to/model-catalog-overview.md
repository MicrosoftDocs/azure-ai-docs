---
title: Explore the model catalog in Azure AI Foundry portal
titleSuffix: Azure AI Foundry
description: This article introduces foundation model capabilities and the model catalog in Azure AI Foundry portal.
manager: scottpolly
ms.service: azure-ai-foundry
ms.custom:
  - ignite-2023
  - build-2024
  - ai-learning-hub
  - ignite-2024
ms.topic: how-to
ms.date: 03/24/2025
ms.reviewer: jcioffi
ms.author: ssalgado
author: ssalgadodev
---

# Model catalog and collections in Azure AI Foundry portal

[!INCLUDE [feature-preview](../includes/feature-preview.md)]

The model catalog in Azure AI Foundry portal is the hub to discover and use a wide range of models for building generative AI applications. The model catalog features hundreds of models across model providers such as Azure OpenAI in Azure AI Foundry Models, Mistral, Meta, Cohere, NVIDIA, and Hugging Face, including models that Microsoft trained. Models from providers other than Microsoft are Non-Microsoft Products as defined in [Microsoft Product Terms](https://www.microsoft.com/licensing/terms/welcome/welcomepage) and are subject to the terms provided with the models.

## Model collections

The model catalog organizes models into different collections:


* **Curated by Azure AI**: The most popular partner models (open-weight and proprietary) packaged and optimized to work seamlessly on the Azure AI platform. Use of these models is subject to the model providers' license terms. When you deploy these models in Azure AI Foundry portal, their availability is subject to the applicable [Azure service-level agreement (SLA)](https://www.microsoft.com/licensing/docs/view/Service-Level-Agreements-SLA-for-Online-Services), and Microsoft provides support for deployment problems.

  Models from partners such as Meta, NVIDIA, and Mistral AI are examples of models available in this collection on the catalog. You can identify these models by looking for a green checkmark on the model tiles in the catalog. Or you can filter by the **Curated by Azure AI** collection.

* **Azure OpenAI in Azure AI Foundry Models**: Flagship Azure OpenAI models available in Foundry Models. Microsoft supports these models and their use according to the product terms and [SLA for Azure OpenAI](https://www.microsoft.com/licensing/docs/view/Service-Level-Agreements-SLA-for-Online-Services).

* **Open models from the Hugging Face hub**: Hundreds of models from the Hugging Face hub for real-time inference with managed compute. Hugging Face creates and maintains models listed in this collection. For help, use the [Hugging Face forum](https://discuss.huggingface.co) or [Hugging Face support](https://huggingface.co/support). Learn more in [Deploy open models with Azure AI Foundry](deploy-models-managed.md).

You can submit a request to add a model to the model catalog by using [this form](https://forms.office.com/pages/responsepage.aspx?id=v4j5cvGGr0GRqy180BHbR_frVPkg_MhOoQxyrjmm7ZJUM09WNktBMURLSktOWEdDODBDRjg2NExKUy4u).

## Overview of model catalog capabilities

You can search and discover models that meet your need through `keyword search` and `filters`. Model catalog also offers the model performance benchmark metrics for select models. You can access the benchmark by clicking `Compare Models` or from the model card Benchmark tab.

On the model card, you'll find:

* **Quick facts**: you will see key information about the model at a quick glance.
* **Details**: this page contains the detailed information about the model, including description, version info, supported data type, etc.
* **Benchmarks**: you will find performance benchmark metrics for select models.
* **Existing deployments**: if you have already deployed the model, you can find it under Existing deployments tab.
* **Code samples**: you will find the basic code samples to get started with AI application development.
* **License**: you will find legal information related to model licensing.
* **Artifacts**: this tab will be displayed for open models only. You can see the model assets and download them via user interface.

## Model deployment: Azure OpenAI

For more information on Azure OpenAI models, see [What is Azure OpenAI](../../ai-services/openai/overview.md).

## Model deployment: Managed compute and standard deployments  

In addition to Azure OpenAI models, the model catalog offers two distinct ways to deploy models for your use: managed compute and standard deployments.

The deployment options and features available for each model vary, as described in the following tables. [Learn more about data processing with the deployment options]( concept-data-privacy.md).

### Capabilities of model deployment options
<!-- docutune:disable -->

Features | Managed compute | standard deployment
--|--|--
Deployment experience and billing | Model weights are deployed to dedicated virtual machines with managed compute. A managed compute, which can have one or more deployments, makes available a REST API for inference. You're billed for the virtual machine core hours that the deployments use. | Access to models is through a deployment that provisions an API to access the model. The API provides access to the model that Microsoft hosts and manages, for inference. You're billed for inputs and outputs to the APIs, typically in tokens. Pricing information is provided before you deploy.
API authentication | Keys and Microsoft Entra authentication. | Keys only.
Guardrails & controls | Use Azure AI Content Safety service APIs. | Azure AI Content Safety filters are available integrated with inference APIs. Azure AI Content Safety filters are billed separately.
Network isolation | [Configure managed networks for Azure AI Foundry hubs](configure-managed-network.md).  | Managed compute follow your hub's public network access (PNA) flag setting. For more information, see the [Network isolation for models deployed via standard deployments](#network-isolation-for-models-deployed-via-serverless-apis) section later in this article.


### Available models for supported deployment options

For Azure OpenAI models, see [Azure OpenAI models](../../ai-services/openai/concepts/models.md).

To view a list of supported models for standard deployment or Managed Compute, go to the home page of the model catalog in [Azure AI Foundry](https://ai.azure.com). Use the **Deployment options** filter to select either **standard deployment** or **Managed Compute**. 

:::image type="content" source="../media/how-to/model-catalog-overview/catalog-filter.png" alt-text="A screenshot showing how to filter by managed compute models in the catalog." lightbox="../media/how-to/model-catalog-overview/catalog-filter.png":::  


<!-- docutune:enable -->

:::image type="content" source="../media/explore/platform-service-cycle.png" alt-text="Diagram that shows a standard deployment model and the service cycle of managed computes." lightbox="../media/explore/platform-service-cycle.png":::

## Model lifecycle: deprecation and retirement
AI models evolve fast, and when a new version or a new model with updated capabilities in the same model family become available, older models may be retired in the AI Foundry model catalog. To allow for a smooth transition to a newer model version, some models provide users with the option to enable automatic updates. To learn more about the model lifecycle of different models, upcoming model retirement dates, and suggested replacement models and versions, see:

- [Azure OpenAI model deprecations and retirements](../../ai-services/openai/concepts/model-retirements.md?context=/azure/ai-foundry/context/context)
- [Deprecations and retirements for standard deployments](../concepts/model-lifecycle-retirement.md)

## Managed compute

The capability to deploy models as managed compute builds on platform capabilities of Azure Machine Learning to enable seamless integration of the wide collection of models in the model catalog across the entire life cycle of large language model (LLM) operations.

:::image type="content" source="../media/explore/llmops-life-cycle.png" alt-text="Diagram that shows the life cycle of large language model operations." lightbox="../media/explore/llmops-life-cycle.png":::

### Availability of models for deployment as managed compute  

The models are made available through [Azure Machine Learning registries](/azure/machine-learning/concept-machine-learning-registries-mlops). These registries enable a machine-learning-first approach to [hosting and distributing Azure Machine Learning assets](/azure/machine-learning/how-to-share-models-pipelines-across-workspaces-with-registries). These assets include model weights, container runtimes for running the models, pipelines for evaluating and fine-tuning the models, and datasets for benchmarks and samples.

The registries build on top of a highly scalable and enterprise-ready infrastructure that:

* Delivers low-latency access model artifacts to all Azure regions with built-in geo-replication.

* Supports enterprise security requirements such as limiting access to models by using Azure Policy and secure deployment by using managed virtual networks.

### Deployment of models for inference with managed compute

Models available for deployment to managed compute can be deployed to Azure Machine Learning managed compute for real-time inference. Deploying to managed compute requires you to have a virtual machine quota in your Azure subscription for the specific products that you need to optimally run the model. Some models allow you to deploy to a [temporarily shared quota for model testing](deploy-models-managed.md).

Learn more about deploying models:

* [Deploy Meta Llama models](deploy-models-llama.md)
* [Deploy Azure AI Foundry open models](deploy-models-managed.md)

### Building generative AI apps with managed compute

The *prompt flow* feature in Azure Machine Learning offers a great experience for prototyping. You can use models deployed with managed compute in prompt flow with the [Open Model LLM tool](/azure/machine-learning/prompt-flow/tools-reference/open-model-llm-tool). You can also use the REST API exposed by managed compute in popular LLM tools like LangChain with the [Azure Machine Learning extension](https://python.langchain.com/docs/integrations/chat/azureml_chat_endpoint/).  

### Guardrails & controls for models deployed as managed compute

The [Azure AI Content Safety](../../ai-services/content-safety/overview.md) service is available for use with managed compute to screen for various categories of harmful content, such as sexual content, violence, hate, and self-harm. You can also use the service to screen for advanced threats such as jailbreak risk detection and protected material text detection.

You can refer to [this notebook](https://github.com/Azure/azureml-examples/blob/main/sdk/python/foundation-models/system/inference/text-generation/llama-safe-online-deployment.ipynb) for reference integration with Azure AI Content Safety for Llama 2. Or you can use the Content Safety (Text) tool in prompt flow to pass responses from the model to Azure AI Content Safety for screening. You're billed separately for such use, as described in [Azure AI Content Safety pricing](https://azure.microsoft.com/pricing/details/cognitive-services/content-safety/).

## Standard deployment (pay per token offer) billing

You can deploy certain models in the model catalog with pay-per-token billing. This deployment method, also called *standard deployment*, provides a way to consume the models as APIs without hosting them on your subscription. Models are hosted in a Microsoft-managed infrastructure, which enables API-based access to the model provider's model. API-based access can dramatically reduce the cost of accessing a model and simplify the provisioning experience.

Models that are available for deployment as standard deployments with pay-as-you-go billing are offered by the model provider, but they're hosted in a Microsoft-managed Azure infrastructure and accessed via API. Model providers define the license terms and set the price for use of their models. The Azure Machine Learning service:

* Manages the hosting infrastructure.
* Makes the inference APIs available.
* Acts as the data processor for prompts submitted and content output by models deployed via standard deployment.

Learn more about data processing for standard deployment in the [article about data privacy](concept-data-privacy.md).

:::image type="content" source="../media/explore/model-publisher-cycle.png" alt-text="Diagram that shows the model publisher service cycle." lightbox="../media/explore/model-publisher-cycle.png":::

> [!NOTE]
> Cloud Solution Provider (CSP) subscriptions do not have the ability to purchase standard deployment models.

### Billing

The discovery, subscription, and consumption experience for models deployed via standard deployment is in Azure AI Foundry portal and Azure Machine Learning studio. Users accept license terms for use of the models. Pricing information for consumption is provided during deployment.

Models from non-Microsoft providers are billed through Azure Marketplace, in accordance with the [Microsoft Commercial Marketplace Terms of Use](/legal/marketplace/marketplace-terms).

Models from Microsoft are billed via Azure meters as First Party Consumption Services. As described in the [Product Terms](https://www.microsoft.com/licensing/terms/welcome/welcomepage), you purchase First Party Consumption Services by using Azure meters, but they aren't subject to Azure service terms. Use of these models is subject to the provided license terms.  

### Fine-tuning models

Certain models also support fine-tuning. For these models, you can take advantage of managed compute (preview) or standard deployment fine-tuning to tailor the models by using data that you provide. For more information, see the [fine-tuning overview](../concepts/fine-tuning-overview.md).

### RAG with models deployed as standard deployments

In Azure AI Foundry portal, you can use vector indexes and retrieval-augmented generation (RAG). You can use models that can be deployed via standard deployments to generate embeddings and inferencing based on custom data. These embeddings and inferencing can then generate answers specific to your use case. For more information, see [Build and consume vector indexes in Azure AI Foundry portal](index-add.md).

### Regional availability of offers and models

Pay-per-token billing is available only to users whose Azure subscription belongs to a billing account in a country/region where the model provider has made the offer available. If the offer is available in the relevant region, the user then must have a project resource in the Azure region where the model is available for deployment or fine-tuning, as applicable. See [Region availability for models in standard deployment endpoints | Azure AI Foundry](deploy-models-serverless-availability.md) for detailed information.

### Guardrails & controls for models deployed via standard deployments

[!INCLUDE [content-safety-serverless-models](../includes/content-safety-serverless-models.md)]

### Network isolation for models deployed via standard deployments

Endpoints for models deployed as standard deployments follow the public network access flag setting of the Azure AI Foundry hub that has the project in which the deployment exists. To help secure your standard deployment, disable the public network access flag on your Azure AI Foundry hub. You can help secure inbound communication from a client to your endpoint by using a private endpoint for the hub.

To set the public network access flag for the Azure AI Foundry hub:

* Go to the [Azure portal](https://ms.portal.azure.com/).
* Search for the resource group to which the hub belongs, and select your Azure AI Foundry hub from the resources listed for this resource group.
* On the hub overview page, on the left pane, go to **Settings** > **Networking**.
* On the **Public access** tab, you can configure settings for the public network access flag.
* Save your changes. Your changes might take up to five minutes to propagate.

#### Limitations

* If you have an Azure AI Foundry hub with a private endpoint created before July 11, 2024, standard deployments added to projects in this hub won't follow the networking configuration of the hub. Instead, you need to create a new private endpoint for the hub and create new standard deployments in the project so that the new deployments can follow the hub's networking configuration.

* If you have an Azure AI Foundry hub with standard deployment created before July 11, 2024, and you enable a private endpoint on this hub, the existing standard deployments won't follow the hub's networking configuration. For standard deployments in the hub to follow the hub's networking configuration, you need to create the deployments again.

* Currently, [Azure OpenAI On Your Data](/azure/ai-services/openai/concepts/use-your-data) support isn't available for standard deployments in private hubs, because private hubs have the public network access flag disabled.

* Any network configuration change (for example, enabling or disabling the public network access flag) might take up to five minutes to propagate.

## Related content

* [Explore foundation models in Azure AI Foundry portal](../../ai-services/connect-services-ai-foundry-portal.md)
* [Model deprecation and retirement in Azure AI model catalog](../concepts/model-lifecycle-retirement.md)
