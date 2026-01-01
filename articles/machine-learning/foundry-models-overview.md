---
title: Explore Microsoft Foundry Models in Azure Machine Learning
titleSuffix: Azure Machine Learning
description: This article introduces Microsoft Foundry Models and the model catalog in Azure Machine Learning.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: training
ms.topic: concept-article
ms.custom:
  - build-2025
ms.date: 05/12/2025
ms.reviewer: sooryar
ms.author: scottpolly
author: s-polly
---

# Explore Microsoft Foundry Models in Azure Machine Learning

Microsoft Foundry Models is your one-stop destination for discovering, evaluating, and deploying powerful AI models—whether you're building a custom copilot, building an agent, enhancing an existing application, or exploring new AI capabilities. 

With Foundry Models, you can: 

* Explore a rich catalog of cutting-edge models from Microsoft, OpenAI, DeepSeek,  Hugging Face, Meta, and more. 
* Compare and evaluate models side-by-side using real-world tasks and your own data. 
* Deploy with confidence, thanks to built-in tools for fine-tuning, observability, and responsible AI. 
* Choose your path—bring your own model, use a hosted one, or integrate seamlessly with Azure services. 
* Whether you're a developer, data scientist, or enterprise architect, Foundry Models gives you the flexibility and control to build AI solutions that scale—securely, responsibly, and fast.

Foundry offers a comprehensive catalog of AI models. There are over 1900+ models ranging from Foundation Models, Reasoning Models, Small Language Models, Multimodal Models, Domain Specific Models, Industry Models and more.

Our catalog is organized into two main categories: 

* [Models Sold Directly by Azure](#models-sold-directly-by-azure)
* [Models from Partners and Community](#models-from-partners-and-community)

Understanding the distinction between these categories helps you choose the right models based on your specific requirements and strategic goals. 
 
## Models Sold Directly by Azure  
 
These are models that are hosted and sold by Microsoft under Microsoft Product Terms. These models have undergone rigorous evaluation and are deeply integrated into Azure’s AI ecosystem. The models come from a variety of top providers and they offer enhanced integration, optimized performance, and direct Microsoft support, including enterprise-grade Service Level Agreements (SLAs).
 
Characteristics of these direct models: 

- Official first-party support from Microsoft 
- High level of integration with Azure services and infrastructure 
- Extensive performance benchmarking and validation 
- Adherence to Microsoft’s Responsible AI standards 
- Enterprise-grade scalability, reliability, and security

These Models also have the benefit of fungible Provisioned Throughput, meaning you can flexibly use your quota and reservations across any of these models.

## Models from Partners and Community

These models constitute the vast majority of the Foundry Models. These models are provided by trusted third-party organizations, partners, research labs, and community contributors. These models offer specialized and diverse AI capabilities, covering a wide array of scenarios, industries, and innovations.

Characteristics of Models from Partners and Community: 
* Developed and supported by external partners and community contributors 
* Diverse range of specialized models catering to niche or broad use cases 
* Typically validated by providers themselves, with integration guidelines provided by Azure 
* Community-driven innovation and rapid availability of cutting-edge models 
* Standard Azure AI integration, with support and maintenance managed by the respective providers 

Models are deployable as Managed Compute or Standard (pay-go) deployment options. The model provider selects how the models are deployable.   
 
## Choosing Between direct models and partner & community models 

When selecting models from Foundry Models, consider the following: 
* Use Case and Requirements: Models sold directly by Azure are ideal for scenarios requiring deep Azure integration, guaranteed support, and enterprise SLAs. Azure Ecosystem Models excel in specialized use cases and innovation-led scenarios.
* Support Expectations: Models sold directly by Azure come with robust Microsoft-provided support and maintenance. These models are supported by their providers, with varying levels of SLA and support structures.
* Innovation and Specialization: Models from Partners and Community offer rapid access to specialized innovations and niche capabilities often developed by leading research labs and emerging AI providers.

## Model collections

The model catalog organizes models into different collections:

* **Azure OpenAI models exclusively available on Azure**: Flagship Azure OpenAI models available through an integration with Azure OpenAI in Foundry Models. Microsoft supports these models and their use according to the product terms and [SLA for Azure OpenAI in Foundry Models](https://www.microsoft.com/licensing/docs/view/Service-Level-Agreements-SLA-for-Online-Services).

* **Open models from the Hugging Face hub**: Hundreds of models from the Hugging Face hub for real-time inference with managed compute. Hugging Face creates and maintains models listed in this collection. For help, use the [Hugging Face forum](https://discuss.huggingface.co) or [Hugging Face support](https://huggingface.co/support). Learn more in [Deploy open models with Foundry](../ai-foundry/how-to/deploy-models-managed.md).

You can submit a request to add a model to the model catalog by using [this form](https://forms.office.com/pages/responsepage.aspx?id=v4j5cvGGr0GRqy180BHbR_frVPkg_MhOoQxyrjmm7ZJUM09WNktBMURLSktOWEdDODBDRjg2NExKUy4u).

## Overview of Model Catalog capabilities

The model catalog in Foundry portal is the hub to discover and use a wide range of models for building generative AI applications. The model catalog features hundreds of models across model providers such as Azure OpenAI, Mistral, Meta, Cohere, NVIDIA, and Hugging Face, including models that Microsoft trained. Models from providers other tha Microsoft are Non-Microsoft Products as defined in [Microsoft Product Terms](https://www.microsoft.com/licensing/terms/welcome/welcomepage) and are subject to the terms provided with the models.

You can search and discover models that meet your need through keyword search and filters. Model catalog also offers the model performance leaderboard and benchmark metrics for select models. You can access them by selecting **Browse leaderboard** and **Compare Models**. Benchmark data is also accessible from the model card Benchmark tab.
 
On the model catalog filters, you’ll find:

* Collection: you can filter models based on the model provider collection.
* Industry: you can filter for the models that are trained on industry specific dataset.
* Capabilities: you can filter for unique model features such as reasoning and tool calling.
* Deployment options: you can filter for the models that support a specific deployment options.
  * Standard: this option allows you to pay per API call.
  * Provisioned: best suited for real-time scoring for large consistent volume.
  * Batch: best suited for cost-optimized batch jobs, and not latency. No playground support is provided for the batch deployment.
  * Managed compute: this option allows you to deploy a model on an Azure virtual machine. You will be billed for hosting and inferencing.
* Inference tasks: you can filter models based on the inference task type.
* Fine-tune tasks: you can filter models based on the fine-tune task type.
* Licenses: you can filter models based on the license type.

On the model card, you'll find:

* Quick facts: you will see key information about the model at a quick glance.
* Details: this page contains the detailed information about the model, including description, version info, supported data type, etc.
* Benchmarks: you will find performance benchmark metrics for select models.
* Existing deployments: if you have already deployed the model, you can find it under Existing deployments tab.
* License: you will find legal information related to model licensing.
* Artifacts: this tab will be displayed for open models only. You can see the model assets and download them via user interface.

## Model deployment: Managed compute and standard deployments  

In addition to Azure OpenAI models, the model catalog offers two distinct ways to deploy models for your use: managed compute and standard deployments.

The deployment options and features available for each model vary, as described in the following tables. [Learn more about data processing with the deployment options]( concept-data-privacy.md).

### Capabilities of model deployment options
<!-- docutune:disable -->

Features | Managed compute | Standard deployments
--|--|--
Deployment experience and billing | Model weights are deployed to dedicated virtual machines with managed compute. A managed compute, which can have one or more deployments, makes available a REST API for inference. You're billed for the virtual machine core hours that the deployments use. | Access to models is through a deployment that provisions an API to access the model. The API provides access to the model that Microsoft hosts and manages, for inference. You're billed for inputs and outputs to the APIs, typically in tokens. Pricing information is provided before you deploy.
API authentication | Keys and Microsoft Entra authentication. | Keys only.
Content safety | Use Azure AI Content Safety service APIs. | Azure AI Content Safety filters are available integrated with inference APIs. Azure AI Content Safety filters are billed separately.
Network isolation | [Configure managed networks for Foundry hubs](../ai-foundry/how-to/configure-managed-network.md).  | Managed compute follow your hub's public network access (PNA) flag setting. For more information, see the [Network isolation for models deployed via standard deployments](#network-isolation-for-models-deployed-via-standard-deployments) section later in this article.

### Available models for supported deployment options

Model Catalog offers two distinct ways to deploy models from the catalog for your use: managed compute and standard deployments. The deployment options available for each model vary; learn more about the features of the deployment options, and the options available for specific models, in the tables below. Learn more about [data processing](concept-data-privacy.md) with the deployment options. 

Features | Managed compute   | Standard deployments
--|--|-- 
Deployment experience and billing |  Model weights are deployed to dedicated Virtual Machines with managed online endpoints. The managed online endpoint, which can have one or more deployments, makes available a REST API for inference. You're billed for the Virtual Machine core hours used by the deployments.  | Access to models is through a deployment that provisions an API to access the model. The API provides access to the model hosted in a central GPU pool, managed by Microsoft, for inference. This mode of access is referred to as "Models as a Service".   You're billed for inputs and outputs to the APIs, typically in tokens; pricing information is provided before you deploy.  
| API authentication   | Keys and Microsoft Entra ID authentication. [Learn more.](concept-endpoints-online-auth.md) | Keys only.  
Content safety | Use Azure Content Safety service APIs.  | Azure AI Content Safety filters are available integrated with inference APIs. Azure AI Content Safety filters may be billed separately.  
Network isolation | Managed Virtual Network with Online Endpoints. [Learn more.](how-to-network-isolation-model-catalog.md)  |  

## Managed compute

The capability to deploy models with managed compute builds on platform capabilities of Azure Machine Learning to enable seamless integration, across the entire GenAIOps (sometimes called LLMOps) lifecycle, of the wide collection of models in the model catalog. 

:::image type="content" source="media/concept-model-catalog/llm-ops-life-cycle.png" alt-text="A diagram showing the LLMops life cycle." lightbox="media/concept-model-catalog/llm-ops-life-cycle.png":::


### Availability of models for deployment as managed compute  

The models are made available through [Azure Machine Learning registries](concept-machine-learning-registries-mlops.md) that enable ML first approach to [hosting and distributing Machine Learning assets](how-to-share-models-pipelines-across-workspaces-with-registries.md) such as model weights, container runtimes for running the models, pipelines for evaluating and fine-tuning the models and datasets for benchmarks and samples. These ML Registries build on top of highly scalable and enterprise ready infrastructure that: 

* Delivers low latency access model artifacts to all Azure regions with built-in geo-replication. 

* Supports enterprise security requirements as [limiting access to models with Azure Policy](how-to-regulate-registry-deployments.md) and [secure deployment with managed virtual networks](how-to-network-isolation-model-catalog.md).

### Deployment of models for inference with managed compute

Models available for deployment with managed compute can be deployed to Azure Machine Learning online endpoints for real-time inference or can be used for Azure Machine Learning batch inference to batch process your data. Deploying to managed compute requires you to have Virtual Machine quota in your Azure Subscription for the specific SKUs needed to optimally run the model.  Some models allow you to deploy to [temporarily shared quota for testing the model](how-to-use-foundation-models.md). Learn more about deploying models: 

* [Deploy Meta Llama models](how-to-deploy-models-llama.md) 
* [Deploy Open models Created by Azure AI](how-to-use-foundation-models.md)
* [Deploy Hugging Face models](how-to-deploy-models-from-huggingface.md)

### Building generative AI apps with managed compute

Prompt flow offers capabilities for prototyping, experimenting, iterating, and deploying your AI applications. You can use models deployed with managed compute in Prompt Flow with the [Open Model LLM tool](./prompt-flow/tools-reference/open-model-llm-tool.md).  You can also use the REST API exposed by the managed computes in popular LLM tools like LangChain with the [Azure Machine Learning extension](https://python.langchain.com/docs/integrations/chat/azureml_chat_endpoint/). 

### Content safety for models deployed as managed compute

[Azure AI Content Safety (AACS)](/azure/ai-services/content-safety/overview) service is available for use with models deployed to managed compute to screen for various categories of harmful content such as sexual content, violence, hate, and self-harm and advanced threats such as Jailbreak risk detection and Protected material text detection. You can refer to this notebook for reference integration with AACS for [Llama 2](https://github.com/Azure/azureml-examples/blob/main/sdk/python/foundation-models/system/inference/text-generation/llama-safe-online-deployment.ipynb) or use the [Content Safety (Text) tool in Prompt Flow](./prompt-flow/tools-reference/content-safety-text-tool.md) to pass responses from the model to AACS for screening. You'll be billed separately as per [AACS pricing](https://azure.microsoft.com/pricing/details/cognitive-services/content-safety/) for such use. 


## Standard deployments with Standard billing

Certain models in the model catalog can be deployed as standard deployments with Standard billing; this method of deployment is called standard deployments. Models available through MaaS are hosted in infrastructure managed by Microsoft, which enables API-based access to the model provider's model. API based access can dramatically reduce the cost of accessing a model and significantly simplify the provisioning experience. Most MaaS models come with token-based pricing.   

### How are third-party models made available in MaaS?   

:::image type="content" source="media/concept-model-catalog/model-publisher-cycle.png" alt-text="A diagram showing model publisher service cycle." lightbox="media/concept-model-catalog/model-publisher-cycle.png":::

Models that are available for deployment as standard deployments with Standard billing are offered by the model provider but hosted in Microsoft-managed Azure infrastructure and accessed via API. Model providers define the license terms and set the price for use of their models, while Azure Machine Learning service manages the hosting infrastructure, makes the inference APIs available, and acts as the data processor for prompts submitted and content output by models deployed via MaaS. Learn more about data processing for MaaS at the [data privacy](concept-data-privacy.md) article. 


> [!NOTE]
> Cloud Solution Provider (CSP) subscriptions do not have the ability to purchase standard deployment models.

### Billing

The discovery, subscription, and consumption experience for models deployed via MaaS is in Foundry portal and Azure Machine Learning studio. Users accept license terms for use of the models. Pricing information for consumption is provided during deployment.

Models from non-Microsoft providers are billed through Azure Marketplace, in accordance with the [Microsoft Commercial Marketplace Terms of Use](/legal/marketplace/marketplace-terms).

Models from Microsoft are billed via Azure meters as First Party Consumption Services. As described in the [Product Terms](https://www.microsoft.com/licensing/terms/welcome/welcomepage), you purchase First Party Consumption Services by using Azure meters, but they aren't subject to Azure service terms. Use of these models is subject to the provided license terms.  

### Fine-tuning models

For models that are available through MaaS and support fine-tuning, users can take advantage of hosted fine-tuning with Standard billing to tailor the models using data they provide. For more information, see [fine-tune a Llama 2 model](/azure/ai-services/openai/how-to/fine-tuning) in [Foundry portal](https://ai.azure.com/?cid=learnDocs). 

### RAG with models deployed as standard deployments

Foundry enables users to make use of Vector Indexes and Retrieval Augmented Generation. Models that can be deployed as standard deployments can be used to generate embeddings and inferencing based on custom data to generate answers specific to their use case. For more information, see [Retrieval augmented generation and indexes](concept-retrieval-augmented-generation.md). 

### Regional availability of offers and models

Standard billing is available only to users whose Azure subscription belongs to a billing account in a country/region where the model provider has made the offer available. If the offer is available in the relevant region, the user then must have a Hub/Project in the Azure region where the model is available for deployment or fine-tuning, as applicable. See [Region availability for models in standard deployments](concept-endpoint-serverless-availability.md) for detailed information.

### Content safety for models deployed via standard deployments

[!INCLUDE [machine-learning-preview-generic-disclaimer](includes/machine-learning-preview-generic-disclaimer.md)]

[!INCLUDE [content-safety-serverless-models](../ai-foundry/includes/content-safety-serverless-models.md)]

### Network isolation for models deployed via standard deployments

Endpoints for models deployed as standard deployments follow the public network access (PNA) flag setting of the workspace in which the deployment exists. To secure your MaaS endpoint, disable the PNA flag on your workspace. You can secure inbound communication from a client to your endpoint by using a private endpoint for the workspace.

To set the PNA flag for the workspace:

* Go to the [Azure portal](https://ms.portal.azure.com/).
* Search for _Azure Machine Learning_, and select your workspace from the list of workspaces.
* On the Overview page, use the left pane to go to **Settings** > **Networking**.
* Under the **Public access** tab, you can configure settings for the public network access flag.
* Save your changes. Your changes might take up to five minutes to propagate.

#### Limitations

* If you have a workspace with a private endpoint created before July 11, 2024, new MaaS endpoints added to this workspace won't follow its networking configuration. Instead, you need to create a new private endpoint for the workspace and create new standard deployments in the workspace so that the new deployments can follow the workspace's networking configuration. 
* If you have a workspace with MaaS deployments created before July 11, 2024, and you enable a private endpoint on this workspace, the existing MaaS deployments won't follow the workspace's networking configuration. For standard deployments in the workspace to follow the workspace's configuration, you need to create the deployments again.
* Currently [On Your Data](#rag-with-models-deployed-as-standard-deployments) support isn't available for MaaS deployments in private workspaces, since private workspaces have the PNA flag disabled.
* Any network configuration change (for example, enabling or disabling the PNA flag) might take up to five minutes to propagate.
  
## Related content

- [Model deprecation and retirement in Foundry model catalog](concept-model-lifecycle-and-retirement.md)
- [How to use Open Source foundation models curated by Azure Machine Learning](how-to-use-foundation-models.md)
