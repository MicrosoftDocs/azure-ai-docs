---
title: Explore the model catalog in Azure AI Foundry portal
titleSuffix: Azure AI Foundry
description: This article introduces foundation model capabilities and the model catalog in Azure AI Foundry portal.
manager: scottpolly
ms.service: azure-ai-studio
ms.custom:
  - ignite-2023
  - build-2024
  - ai-learning-hub
  - ignite-2024
ms.topic: how-to
ms.date: 5/21/2024
ms.reviewer: jcioffi
ms.author: ssalgado
author: ssalgadodev
---

# Model catalog and collections in Azure AI Foundry portal

[!INCLUDE [feature-preview](../includes/feature-preview.md)]

The model catalog in Azure AI Foundry portal is the hub to discover and use a wide range of models for building generative AI applications. The model catalog features hundreds of models across model providers such as Azure OpenAI Service, Mistral, Meta, Cohere, NVIDIA, and Hugging Face, including models that Microsoft trained. Models from providers other than Microsoft are Non-Microsoft Products as defined in [Microsoft Product Terms](https://www.microsoft.com/licensing/terms/welcome/welcomepage) and are subject to the terms provided with the models.

## Model collections

The model catalog organizes models into different collections:


* **Curated by Azure AI**: The most popular non-Microsoft open-weight and proprietary models packaged and optimized to work seamlessly on the Azure AI platform. Use of these models is subject to the model providers' license terms. When you deploy these models in Azure AI Foundry portal, their availability is subject to the applicable [Azure service-level agreement (SLA)](https://www.microsoft.com/licensing/docs/view/Service-Level-Agreements-SLA-for-Online-Services), and Microsoft provides support for deployment problems.

  Models from partners such as Meta, NVIDIA, and Mistral AI are examples of models available in this collection on the catalog. You can identify these models by looking for a green checkmark on the model tiles in the catalog. Or you can filter by the **Curated by Azure AI** collection.

* **Azure OpenAI models exclusively available on Azure**: Flagship Azure OpenAI models available through an integration with Azure OpenAI Service. Microsoft supports these models and their use according to the product terms and [SLA for Azure OpenAI Service](https://www.microsoft.com/licensing/docs/view/Service-Level-Agreements-SLA-for-Online-Services).

* **Open models from the Hugging Face hub**: Hundreds of models from the Hugging Face hub for real-time inference with managed compute. Hugging Face creates and maintains models listed in this collection. For help, use the [Hugging Face forum](https://discuss.huggingface.co) or [Hugging Face support](https://huggingface.co/support). Learn more in [Deploy open models with Azure AI Foundry](deploy-models-open.md).

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

For more information on Azure OpenAI models, see [What is Azure OpenAI Service?](../../ai-services/openai/overview.md).

## Model deployment: Managed compute and serverless APIs  

In addition to Azure OpenAI Service models, the model catalog offers two distinct ways to deploy models for your use: managed compute and serverless APIs.

The deployment options and features available for each model vary, as described in the following tables. [Learn more about data processing with the deployment options]( concept-data-privacy.md).

### Capabilities of model deployment options
<!-- docutune:disable -->

Features | Managed compute | Serverless API (pay-per-token)
--|--|--
Deployment experience and billing | Model weights are deployed to dedicated virtual machines with managed compute. A managed compute, which can have one or more deployments, makes available a REST API for inference. You're billed for the virtual machine core hours that the deployments use. | Access to models is through a deployment that provisions an API to access the model. The API provides access to the model that Microsoft hosts and manages, for inference. You're billed for inputs and outputs to the APIs, typically in tokens. Pricing information is provided before you deploy.
API authentication | Keys and Microsoft Entra authentication. | Keys only.
Content safety | Use Azure AI Content Safety service APIs. | Azure AI Content Safety filters are available integrated with inference APIs. Azure AI Content Safety filters are billed separately.
Network isolation | [Configure managed networks for Azure AI Foundry hubs](configure-managed-network.md).  | Managed compute follow your hub's public network access (PNA) flag setting. For more information, see the [Network isolation for models deployed via Serverless APIs](#network-isolation-for-models-deployed-via-serverless-apis) section later in this article.

### Available models for supported deployment options

The following list contains Serverless API models. For Azure OpenAI models, see [Azure OpenAI Service Models](../../ai-services/openai/concepts/models.md).

Model | Managed compute | Serverless API (pay-per-token)
--|--|--
Llama family models | Llama-3.2-3B-Instruct<BR>  Llama-3.2-1B-Instruct<BR>  Llama-3.2-1B<BR>  Llama-3.2-90B-Vision-Instruct<BR>  Llama-3.2-11B-Vision-Instruct<BR>  Llama-3.1-8B-Instruct<BR>  Llama-3.1-8B<BR>  Llama-3.1-70B-Instruct<BR>  Llama-3.1-70B<BR>  Llama-3-8B-Instruct<BR>  Llama-3-70B<BR>  Llama-3-8B<BR>  Llama-Guard-3-1B<BR>  Llama-Guard-3-8B<BR>  Llama-Guard-3-11B-Vision<BR>  Llama-2-7b<BR>  Llama-2-70b<BR>  Llama-2-7b-chat<BR>  Llama-2-13b-chat<BR>  CodeLlama-7b-hf<BR>  CodeLlama-7b-Instruct-hf<BR>  CodeLlama-34b-hf<BR>  CodeLlama-34b-Python-hf<BR>  CodeLlama-34b-Instruct-hf<BR>  CodeLlama-13b-Instruct-hf<BR>  CodeLlama-13b-Python-hf<BR>  Prompt-Guard-86M<BR>  CodeLlama-70b-hf<BR> | Llama-3.2-90B-Vision-Instruct<br>  Llama-3.2-11B-Vision-Instruct<br>  Llama-3.1-8B-Instruct<br>  Llama-3.1-70B-Instruct<br>  Llama-3.1-405B-Instruct<br>  Llama-3-8B-Instruct<br>  Llama-3-70B-Instruct<br>  Llama-2-7b<br>  Llama-2-7b-chat<br>  Llama-2-70b<br>  Llama-2-70b-chat<br>  Llama-2-13b<br>  Llama-2-13b-chat<br>
Mistral family models | mistralai-Mixtral-8x22B-v0-1 <br> mistralai-Mixtral-8x22B-Instruct-v0-1 <br> mistral-community-Mixtral-8x22B-v0-1 <br> mistralai-Mixtral-8x7B-v01 <br> mistralai-Mistral-7B-Instruct-v0-2 <br> mistralai-Mistral-7B-v01 <br> mistralai-Mixtral-8x7B-Instruct-v01 <br> mistralai-Mistral-7B-Instruct-v01 | Mistral-large (2402) <br> Mistral-large (2407) <br> Mistral-small <br> Ministral-3B <br> Mistral-NeMo
Cohere family models | Not available | Cohere-command-r-plus-08-2024 <br> Cohere-command-r-08-2024 <br> Cohere-command-r-plus <br> Cohere-command-r <br> Cohere-embed-v3-english <br> Cohere-embed-v3-multilingual <br> Cohere-rerank-v3-english <br> Cohere-rerank-v3-multilingual
JAIS | Not available | jais-30b-chat
AI21 family models | Not available | Jamba-1.5-Mini <br> Jamba-1.5-Large
Healthcare AI family Models | MedImageParse<BR>  MedImageInsight<BR>  CxrReportGen<BR>  Virchow<BR>  Virchow2<BR>  Prism<BR>  BiomedCLIP-PubMedBERT<BR>  microsoft-llava-med-v1.5<BR>  m42-health-llama3-med4<BR>  biomistral-biomistral-7b<BR>  microsoft-biogpt-large-pub<BR>  microsoft-biomednlp-pub<BR>  stanford-crfm-biomedlm<BR>  medicalai-clinicalbert<BR>  microsoft-biogpt<BR>  microsoft-biogpt-large<BR>  microsoft-biomednlp-pub<BR> | Not Available
Phi-3 family models | Phi-3-mini-4k-Instruct <br> Phi-3-mini-128k-Instruct <br> Phi-3-small-8k-Instruct <br> Phi-3-small-128k-Instruct <br> Phi-3-medium-4k-instruct <br> Phi-3-medium-128k-instruct <br> Phi-3-vision-128k-Instruct <br> Phi-3.5-mini-Instruct <br> Phi-3.5-vision-Instruct <br> Phi-3.5-MoE-Instruct | Phi-3-mini-4k-Instruct <br> Phi-3-mini-128k-Instruct <br> Phi-3-small-8k-Instruct <br> Phi-3-small-128k-Instruct <br> Phi-3-medium-4k-instruct <br> Phi-3-medium-128k-instruct <br> <br> Phi-3.5-mini-Instruct <br> Phi-3.5-vision-Instruct <br> Phi-3.5-MoE-Instruct
Nixtla | Not available | TimeGEN-1

<!-- docutune:enable -->

:::image type="content" source="../media/explore/platform-service-cycle.png" alt-text="Diagram that shows models as a service and the service cycle of managed computes." lightbox="../media/explore/platform-service-cycle.png":::

## Managed compute

The capability to deploy models as managed compute builds on platform capabilities of Azure Machine Learning to enable seamless integration of the wide collection of models in the model catalog across the entire life cycle of large language model (LLM) operations.

:::image type="content" source="../media/explore/llmops-life-cycle.png" alt-text="Diagram that shows the life cycle of large language model operations." lightbox="../media/explore/llmops-life-cycle.png":::

### Availability of models for deployment as managed compute  

The models are made available through [Azure Machine Learning registries](/azure/machine-learning/concept-machine-learning-registries-mlops). These registries enable a machine-learning-first approach to [hosting and distributing Azure Machine Learning assets](/azure/machine-learning/how-to-share-models-pipelines-across-workspaces-with-registries). These assets include model weights, container runtimes for running the models, pipelines for evaluating and fine-tuning the models, and datasets for benchmarks and samples.

The registries build on top of a highly scalable and enterprise-ready infrastructure that:

* Delivers low-latency access model artifacts to all Azure regions with built-in geo-replication.

* Supports enterprise security requirements such as limiting access to models by using Azure Policy and secure deployment by using managed virtual networks.

### Deployment of models for inference with managed compute

Models available for deployment to managed compute can be deployed to Azure Machine Learning managed compute for real-time inference. Deploying to managed compute requires you to have a virtual machine quota in your Azure subscription for the specific products that you need to optimally run the model. Some models allow you to deploy to a [temporarily shared quota for model testing](deploy-models-open.md).

Learn more about deploying models:

* [Deploy Meta Llama models](deploy-models-llama.md)
* [Deploy Azure AI Foundry open models](deploy-models-open.md)

### Building generative AI apps with managed compute

The *prompt flow* feature in Azure Machine Learning offers a great experience for prototyping. You can use models deployed with managed compute in prompt flow with the [Open Model LLM tool](/azure/machine-learning/prompt-flow/tools-reference/open-model-llm-tool). You can also use the REST API exposed by managed compute in popular LLM tools like LangChain with the [Azure Machine Learning extension](https://python.langchain.com/docs/integrations/chat/azureml_chat_endpoint/).  

### Content safety for models deployed as managed compute

The [Azure AI Content Safety](../../ai-services/content-safety/overview.md) service is available for use with managed compute to screen for various categories of harmful content, such as sexual content, violence, hate, and self-harm. You can also use the service to screen for advanced threats such as jailbreak risk detection and protected material text detection.

You can refer to [this notebook](https://github.com/Azure/azureml-examples/blob/main/sdk/python/foundation-models/system/inference/text-generation/llama-safe-online-deployment.ipynb) for reference integration with Azure AI Content Safety for Llama 2. Or you can use the Content Safety (Text) tool in prompt flow to pass responses from the model to Azure AI Content Safety for screening. You're billed separately for such use, as described in [Azure AI Content Safety pricing](https://azure.microsoft.com/pricing/details/cognitive-services/content-safety/).

## Serverless API (pay-per-token) billing

You can deploy certain models in the model catalog with pay-per-token billing. This deployment method, also called *Serverless API*, provides a way to consume the models as APIs without hosting them on your subscription. Models are hosted in a Microsoft-managed infrastructure, which enables API-based access to the model provider's model. API-based access can dramatically reduce the cost of accessing a model and simplify the provisioning experience.

Models that are available for deployment as serverless APIs with pay-as-you-go billing are offered by the model provider, but they're hosted in a Microsoft-managed Azure infrastructure and accessed via API. Model providers define the license terms and set the price for use of their models. The Azure Machine Learning service:

* Manages the hosting infrastructure.
* Makes the inference APIs available.
* Acts as the data processor for prompts submitted and content output by models deployed via MaaS.

Learn more about data processing for MaaS in the [article about data privacy](concept-data-privacy.md).

:::image type="content" source="../media/explore/model-publisher-cycle.png" alt-text="Diagram that shows the model publisher service cycle." lightbox="../media/explore/model-publisher-cycle.png":::

### Billing

The discovery, subscription, and consumption experience for models deployed via MaaS is in Azure AI Foundry portal and Azure Machine Learning studio. Users accept license terms for use of the models. Pricing information for consumption is provided during deployment.

Models from non-Microsoft providers are billed through Azure Marketplace, in accordance with the [Microsoft Commercial Marketplace Terms of Use](/legal/marketplace/marketplace-terms).

Models from Microsoft are billed via Azure meters as First Party Consumption Services. As described in the [Product Terms](https://www.microsoft.com/licensing/terms/welcome/welcomepage), you purchase First Party Consumption Services by using Azure meters, but they aren't subject to Azure service terms. Use of these models is subject to the provided license terms.  

### Fine-tuning models

Certain models also support fine-tuning. For these models, you can take advantage of managed compute (preview) or serverless API fine-tuning to tailor the models by using data that you provide. For more information, see the [fine-tuning overview](../concepts/fine-tuning-overview.md).

### RAG with models deployed as serverless APIs

In Azure AI Foundry portal, you can use vector indexes and retrieval-augmented generation (RAG). You can use models that can be deployed via serverless APIs to generate embeddings and inferencing based on custom data. These embeddings and inferencing can then generate answers specific to your use case. For more information, see [Build and consume vector indexes in Azure AI Foundry portal](index-add.md).

### Regional availability of offers and models

Pay-per-token billing is available only to users whose Azure subscription belongs to a billing account in a country where the model provider has made the offer available. If the offer is available in the relevant region, the user then must have a project resource in the Azure region where the model is available for deployment or fine-tuning, as applicable. See [Region availability for models in serverless API endpoints | Azure AI Foundry](deploy-models-serverless-availability.md) for detailed information.

### Content safety for models deployed via serverless APIs

[!INCLUDE [content-safety-serverless-models](../includes/content-safety-serverless-models.md)]

### Network isolation for models deployed via serverless APIs

Managed computes for models deployed as serverless APIs follow the public network access flag setting of the AI Foundry hub that has the project in which the deployment exists. To help secure your managed compute, disable the public network access flag on your AI Foundry hub. You can help secure inbound communication from a client to your managed compute by using a private endpoint for the hub.

To set the public network access flag for the AI Foundry hub:

* Go to the [Azure portal](https://ms.portal.azure.com/).
* Search for the resource group to which the hub belongs, and select your AI Foundry hub from the resources listed for this resource group.
* On the hub overview page, on the left pane, go to **Settings** > **Networking**.
* On the **Public access** tab, you can configure settings for the public network access flag.
* Save your changes. Your changes might take up to five minutes to propagate.

#### Limitations

* If you have an AI Foundry hub with a managed compute created before July 11, 2024, managed computes added to projects in this hub won't follow the networking configuration of the hub. Instead, you need to create a new managed compute for the hub and create new serverless API deployments in the project so that the new deployments can follow the hub's networking configuration.

* If you have an AI Foundry hub with MaaS deployments created before July 11, 2024, and you enable a managed compute on this hub, the existing MaaS deployments won't follow the hub's networking configuration. For serverless API deployments in the hub to follow the hub's networking configuration, you need to create the deployments again.

* Currently, [Azure OpenAI On Your Data](/azure/ai-services/openai/concepts/use-your-data) support isn't available for MaaS deployments in private hubs, because private hubs have the public network access flag disabled.

* Any network configuration change (for example, enabling or disabling the public network access flag) might take up to five minutes to propagate.

## Related content

* [Explore foundation models in Azure AI Foundry portal](models-foundation-azure-ai.md)
* [Model deprecation and retirement in Azure AI model catalog](../concepts/model-lifecycle-and-retirement.md)
