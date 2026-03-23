---
title: "Foundry Models from partners and community"
description: "Learn about Microsoft Foundry Models from partners and community, including their capabilities, supported input and output types, Azure Marketplace requirements, and troubleshooting."
author: msakande
ms.author: mopeakande
manager: nitinme
ms.date: 03/23/2026
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: partner-tools
ms.custom:
  - classic-and-new
  - references_regions
  - tool_generated
  - build-aifnd
  - build-2025
  - pilot-ai-workflow-jan-2026
  - doc-kit-assisted
ai-usage: ai-assisted
zone_pivot_groups: azure-ai-model-categories

#CustomerIntent: As a developer or AI practitioner, I want to explore and understand the available Microsoft Foundry Models from partners and community, including their specific capabilities, supported input and output types, and language support, so that I can select the most appropriate model for my AI application requirements.
---

# Foundry Models from partners and community
This article lists capabilities for a selection of Microsoft Foundry Models from partners and community.
Most Foundry Model providers are trusted third-party organizations, partners, research labs, and community contributors. 
The selection of models that you see in Foundry depends on the [kind of project](../../what-is-foundry.md#choosing-a-project) you use.
To learn more about attributes of Foundry Models from partners and community, see [Explore Foundry Models](../../../foundry-classic/concepts/foundry-models-overview.md#models-from-partners-and-community).

> [!NOTE]
> For a list of models sold directly by Azure, see [Foundry Models sold directly by Azure](models-sold-directly-by-azure.md).
>
> For a list of Azure OpenAI models that are supported by the Foundry Agent Service, see [Models supported by Agent Service](../../agents/concepts/limits-quotas-regions.md).

## Prerequisites

- An Azure subscription. If you don't have one, create a [free account](https://azure.microsoft.com/free/).

    > [!IMPORTANT]
    > The following Azure subscriptions can't be used to purchase software as a service (SaaS) offers in Marketplace: Student, Visual Studio Enterprise, or Free credit. For more information on purchasing SaaS offers, see [The SaaS purchase experience](/marketplace/purchase-saas-offer-in-azure-portal#the-saas-purchase-experience).

- A [Microsoft Foundry project](../../how-to/create-projects.md).

[!INCLUDE [marketplace-rbac](../includes/configure-marketplace/rbac.md)]

## Country/region availability

You can access models from partners and community with pay-as-you-go billing only if your Azure subscription belongs to a billing account in a country/region where the model offer is available. Availability varies per model provider and model SKU. For more information, see [Region availability for models](../../../foundry-classic/how-to/deploy-models-serverless-availability.md).

## Anthropic

Anthropic's flagship product is Claude, a frontier AI model trusted by leading enterprises and millions of users worldwide for complex tasks including coding, agents, financial analysis, research, and office tasks. Claude delivers exceptional performance while maintaining high safety standards.

To work with Claude models in Foundry, see [Deploy and use Claude models in Microsoft Foundry](../how-to/use-foundry-models-claude.md). 

[!INCLUDE [claude-usage-restriction](../includes/claude-usage-restriction.md)]

| Model  | Type | Capabilities |
| ------ | ---- | ------------ |
| `claude-opus-4-6` <br><br> **(Preview)** | Messages | - **Input:**  text, image, and code  <br /> - **Output:** text, image, and code (128,000 max tokens) <br /> - **Context window:** 1,000,000  <br /> - **Languages:** `en`, `fr`, `ar`, `zh`, `ja`, `ko`, `es`, `hi` <br />  - **Tool calling:** Yes (file search and code execution) <br /> - **Response formats:**  Text in various formats (e.g., prose, lists, Markdown tables, JSON, HTML, code in various programming languages)|
| `claude-opus-4-5` <br><br> **(Preview)** | Messages | - **Input:**  text, image, and code  <br /> - **Output:** text (64,000 max tokens) <br /> - **Context window:** 200,000   <br /> - **Languages:** `en`, `fr`, `ar`, `zh`, `ja`, `ko`, `es`, `hi` <br />  - **Tool calling:** Yes (file search and code execution) <br /> - **Response formats:**  Text in various formats (e.g., prose, lists, Markdown tables, JSON, HTML, code in various programming languages)|
| `claude-opus-4-1` <br><br> **(Preview)** | Messages | - **Input:**  text, image, and code  <br /> - **Output:** text (32,000 max tokens) <br /> - **Context window:** 200,000  <br /> - **Languages:** `en`, `fr`, `ar`, `zh`, `ja`, `ko`, `es`, `hi` <br />  - **Tool calling:** Yes (file search and code execution) <br /> - **Response formats:**  Text in various formats (e.g., prose, lists, Markdown tables, JSON, HTML, code in various programming languages) |
| `claude-sonnet-4-6` <br><br> **(Preview)** | Messages | - **Input:**  text, image, and code  <br /> - **Output:** text, image, and code (128,000 max tokens) <br /> - **Context window:** 1,000,000   <br /> - **Languages:** `en`, `fr`, `ar`, `zh`, `ja`, `ko`, `es`, `hi` <br />  - **Tool calling:** Yes (file search and code execution) <br /> - **Response formats:**  Text in various formats (e.g., prose, lists, Markdown tables, JSON, HTML, code in various programming languages)|
| `claude-sonnet-4-5` <br><br> **(Preview)** | Messages | - **Input:**  text, image, and code  <br /> - **Output:** text (64,000 max tokens) <br /> - **Context window:** 200,000   <br /> - **Languages:** `en`, `fr`, `ar`, `zh`, `ja`, `ko`, `es`, `hi` <br />  - **Tool calling:** Yes (file search and code execution) <br /> - **Response formats:**  Text in various formats (e.g., prose, lists, Markdown tables, JSON, HTML, code in various programming languages) |
| `claude-haiku-4-5` <br><br> **(Preview)** | Messages | - **Input:**  text and image  <br /> - **Output:** text (64,000 max tokens) <br /> - **Context window:** 200,000   <br /> - **Languages:** `en`, `fr`, `ar`, `zh`, `ja`, `ko`, `es`, `hi` <br />  - **Tool calling:** Yes (file search and code execution) <br /> - **Response formats:**  Text in various formats (e.g., prose, lists, Markdown tables, JSON, HTML, code in various programming languages) |

See [Anthropic models in the Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=anthropic/?cid=learnDocs).

## Cohere

The Cohere family of models includes various models optimized for different use cases, including chat completions and embeddings. Cohere models are optimized for various use cases that include reasoning, summarization, and question answering.

To deploy Cohere models in Foundry, see [Deploy Microsoft Foundry Models in the Foundry portal](../how-to/deploy-foundry-models.md).

| Model  | Type | Capabilities |
| ------ | ---- | ------------ |
| `Cohere-command-r-plus-08-2024` | chat-completion | - **Input:** text (131,072 tokens) <br /> - **Output:** text (4,096 tokens) <br /> - **Languages:** `en`, `fr`, `es`, `it`, `de`, `pt-br`, `ja`, `ko`, `zh-cn`, and `ar` <br />  - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON |
| `Cohere-command-r-08-2024` | chat-completion | - **Input:** text (131,072 tokens) <br /> - **Output:** text (4,096 tokens) <br /> - **Languages:** `en`, `fr`, `es`, `it`, `de`, `pt-br`, `ja`, `ko`, `zh-cn`, and `ar` <br />  - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON |
| `Cohere-embed-v3-english` | embeddings | - **Input:** text and images (512 tokens) <br /> - **Output:** Vector (1024 dim.) <br /> - **Languages:** `en` |
| `Cohere-embed-v3-multilingual` | embeddings | - **Input:** text (512 tokens) <br /> - **Output:** Vector (1024 dim.) <br /> - **Languages:** `en`, `fr`, `es`, `it`, `de`, `pt-br`, `ja`, `ko`, `zh-cn`, and `ar` |

See [Cohere models in the Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=Cohere/?cid=learnDocs).

## Meta

Meta Llama models and tools are a collection of pretrained and fine-tuned generative AI text and image reasoning models. Meta models range in scale to include:

- Small language models (SLMs) like 1B and 3B Base and Instruct models for on-device and edge inferencing
- Mid-size large language models (LLMs) like 7B, 8B, and 70B Base and Instruct models
- High-performance models like Meta Llama 3.1-405B Instruct for synthetic data generation and distillation use cases.

To deploy Meta Llama models in Foundry, see [Deploy Microsoft Foundry Models in the Foundry portal](../how-to/deploy-foundry-models.md).

| Model  | Type | Capabilities |
| ------ | ---- | ------------ |
| `Llama-3.2-11B-Vision-Instruct` | chat-completion | - **Input:** text and image (128,000 tokens) <br /> - **Output:** text (8,192 tokens) <br /> - **Languages:** `en` <br />  - **Tool calling:** No <br /> - **Response formats:** Text |
| `Llama-3.2-90B-Vision-Instruct` | chat-completion | - **Input:** text and image (128,000 tokens) <br /> - **Output:** text (8,192 tokens) <br /> - **Languages:** `en` <br />  - **Tool calling:** No <br /> - **Response formats:** Text |
| `Meta-Llama-3.1-405B-Instruct` | chat-completion | - **Input:** text (131,072 tokens) <br /> - **Output:** text (8,192 tokens) <br /> - **Languages:** `en`, `de`, `fr`, `it`, `pt`, `hi`, `es`, and `th` <br />  - **Tool calling:** No <br /> - **Response formats:** Text |
| `Meta-Llama-3.1-8B-Instruct` | chat-completion | - **Input:** text (131,072 tokens) <br /> - **Output:** text (8,192 tokens) <br /> - **Languages:** `en`, `de`, `fr`, `it`, `pt`, `hi`, `es`, and `th` <br />  - **Tool calling:** No <br /> - **Response formats:** Text |
| `Llama-4-Scout-17B-16E-Instruct` | chat-completion | - **Input:** text and image (128,000 tokens) <br /> - **Output:** text (8,192 tokens) <br /> - **Languages:** `en` <br /> - **Tool calling:** No <br /> - **Response formats:** Text |

See [Meta models in the Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=Meta/?cid=learnDocs). You can also find several Meta models available as [models sold directly by Azure](models-sold-directly-by-azure.md?pivots=azure-direct-others).

## Microsoft

Microsoft models include various model groups such as MAI models, Phi models, healthcare AI models, and more.

To deploy Microsoft models in Foundry, see [Deploy Microsoft Foundry Models in the Foundry portal](../how-to/deploy-foundry-models.md).

| Model  | Type | Capabilities |
| ------ | ---- | ------------ |
| `Phi-4-mini-instruct` | chat-completion | - **Input:** text (131,072 tokens) <br /> - **Output:** text (4,096 tokens) <br /> - **Languages:** `ar`, `zh`, `cs`, `da`, `nl`, `en`, `fi`, `fr`, `de`, `he`, `hu`, `it`, `ja`, `ko`, `no`, `pl`, `pt`, `ru`, `es`, `sv`, `th`, `tr`, and `uk` <br />  - **Tool calling:** No <br /> - **Response formats:** Text |
| `Phi-4-multimodal-instruct` | chat-completion | - **Input:** text, images, and audio (131,072 tokens) <br /> - **Output:** text (4,096 tokens) <br /> - **Languages:** `ar`, `zh`, `cs`, `da`, `nl`, `en`, `fi`, `fr`, `de`, `he`, `hu`, `it`, `ja`, `ko`, `no`, `pl`, `pt`, `ru`, `es`, `sv`, `th`, `tr`, and `uk` <br />  - **Tool calling:** No <br /> - **Response formats:** Text |
| `Phi-4` | chat-completion | - **Input:** text (16,384 tokens) <br /> - **Output:** text (16,384 tokens) <br /> - **Languages:** `en`, `ar`, `bn`, `cs`, `da`, `de`, `el`, `es`, `fa`, `fi`, `fr`, `gu`, `ha`, `he`, `hi`, `hu`, `id`, `it`, `ja`, `jv`, `kn`, `ko`, `ml`, `mr`, `nl`, `no`, `or`, `pa`, `pl`, `ps`, `pt`, `ro`, `ru`, `sv`, `sw`, `ta`, `te`, `th`, `tl`, `tr`, `uk`, `ur`, `vi`, `yo`, and `zh` <br />  - **Tool calling:** No <br /> - **Response formats:** Text |
| `Phi-4-reasoning` | chat-completion with reasoning content | - **Input:** text (32,768 tokens) <br /> - **Output:** text (32,768 tokens) <br /> - **Languages:** `en` <br /> - **Tool calling:** No <br /> - **Response formats:** Text |
| `Phi-4-mini-reasoning` | chat-completion with reasoning content | - **Input:** text (128,000 tokens) <br /> - **Output:** text (128,000 tokens) <br /> - **Languages:** `en` <br /> - **Tool calling:** No <br /> - **Response formats:** Text |

See [Microsoft models in the Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=Microsoft/?cid=learnDocs). Microsoft models are also available as [models sold directly by Azure](models-sold-directly-by-azure.md?pivots=azure-direct-others).

## Mistral AI

Mistral AI offers models for code generation, general-purpose chat, and multimodal tasks, including Codestral, Ministral, Mistral Small, and Mistral Medium.

To deploy Mistral AI models in Foundry, see [Deploy Microsoft Foundry Models in the Foundry portal](../how-to/deploy-foundry-models.md).

| Model | Type | Capabilities |
| ----- | ---- | ------------ |
| `Codestral-2501` | chat-completion | - **Input:** text (262,144 tokens) <br /> - **Output:** text (4,096 tokens) <br /> - **Languages:** en <br />  - **Tool calling:** No <br /> - **Response formats:** Text |
| `Ministral-3B` | chat-completion | - **Input:** text (131,072 tokens) <br /> - **Output:** text (4,096 tokens) <br /> - **Languages:** fr, de, es, it, and en <br />  - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON |
| `Mistral-small-2503` | chat-completion | - **Input:** text (32,768 tokens) <br /> - **Output:** text (4,096 tokens) <br /> - **Languages:** fr, de, es, it, and en <br />  - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON |
| `Mistral-medium-2505` | chat-completion |  - **Input:** text (128,000 tokens), image <br /> - **Output:** text (128,000 tokens) <br />  - **Tool calling:** No <br /> - **Response formats:** Text, JSON |

See [Mistral AI models in the Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=Mistral+AI/?cid=learnDocs). Mistral models are also available as [models sold directly by Azure](models-sold-directly-by-azure.md?pivots=azure-direct-others).

## Stability AI

The Stability AI collection of image generation models includes Stable Image Core, Stable Image Ultra, and Stable Diffusion 3.5 Large. Stable Diffusion 3.5 Large accepts both image and text input. 

To deploy Stability AI models in Foundry, see [Deploy Microsoft Foundry Models in the Foundry portal](../how-to/deploy-foundry-models.md).

| Model  | Type | Capabilities |
| ------ | ---- | ------------ |
| `Stable Diffusion 3.5 Large` | Image generation | - **Input:** text and image (1,000 tokens and 1 image)  <br /> - **Output:** One Image  <br />  - **Tool calling:** No <br /> - **Response formats**: Image (PNG and JPG) |
| `Stable Image Core` | Image generation | - **Input:** text (1,000 tokens)  <br /> - **Output:** One Image  <br />  - **Tool calling:** No <br /> - **Response formats:** Image (PNG and JPG) |
| `Stable Image Ultra` | Image generation | - **Input:** text (1,000 tokens)  <br /> - **Output:** One Image  <br />  - **Tool calling:** No <br /> - **Response formats:** Image (PNG and JPG) |

See [Stability AI models in the Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=Stability+AI/?cid=learnDocs).

## Troubleshooting

Use the following troubleshooting guide to find and solve errors when deploying third-party models in Foundry Models:

| Error | Description |
|-------|-------------|
| Offer not available in your country/region | The model provider didn't make the specific model SKU available in the country/region where you registered your subscription. Each model provider decides which countries/regions are available, and availability can vary by model SKU. Deploy the model to a subscription with billing in a supported country/region. See [Region availability for models](../../../foundry-classic/how-to/deploy-models-serverless-availability.md). |
| Marketplace purchase eligibility check failed | The model provider didn't make the specific model SKU available in your country/region, or the model isn't available in the region where you deployed the Foundry resource. See [Region availability for models](../../../foundry-classic/how-to/deploy-models-serverless-availability.md). |
| Unable to create a model deployment | Azure Marketplace rejected the request to create a model subscription. This rejection can happen for multiple reasons, including subscribing to the model offering too often or from multiple subscriptions at the same time. Contact [support](https://go.microsoft.com/fwlink/?linkid=2101400&clcid=0x409) and include your subscription ID. |
| CSP subscription not supported | Cloud Solution Provider (CSP) subscriptions can't purchase third-party model offerings. Consider using models offered as a first-party consumption service. |

## Related content

- [Deployment overview for Foundry Models](../../../foundry-classic/concepts/deployments-overview.md)
- [Deploy Microsoft Foundry Models in the Foundry portal](../how-to/deploy-foundry-models.md)
- [Deployment types in Foundry Models](deployment-types.md)
- [Region availability for Foundry Models](../../../foundry-classic/how-to/deploy-models-serverless-availability.md)
- [Explore Foundry Models](../../../foundry-classic/concepts/foundry-models-overview.md)

