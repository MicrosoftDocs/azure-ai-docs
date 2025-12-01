---
title: Other Foundry Models sold directly by Azure
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: include
ms.date: 10/07/2025
ms.author: mopeakande
author: msakande
monikerRange: 'foundry-classic || foundry'
ai-usage: ai-assisted
---

> [!NOTE]
> Foundry Models sold directly by Azure also include all Azure OpenAI models. To learn about these models, switch to the [Azure OpenAI models](../../foundry-models/concepts/models-sold-directly-by-azure.md?pivots=azure-openai) collection at the top of this article. 

## Black Forest Labs models sold directly by Azure

The Black Forest Labs (BFL) collection of image generation models includes FLUX.1 Kontext [pro] for in-context generation and editing and FLUX1.1 [pro] for text-to-image generation.  

You can run these models through the BFL service provider API and through the [images/generations and images/edits endpoints](../../openai/reference-preview.md). 

::: moniker range="foundry-classic"

| Model  | Type & API endpoint| Capabilities | Deployment type (region availability) | Project type | 
| ------ | ------------------ | ------------ | ------------------------------------- | ------------ |
| [FLUX.1-Kontext-pro](https://ai.azure.com/explore/models/FLUX.1-Kontext-pro/version/1/registry/azureml-blackforestlabs/?cid=learnDocs) | **Image generation** <br> - [Image API](../../openai/reference-preview.md): `https://<resource-name>/openai/deployments/{deployment-id}/images/generations` <br> and <br> `https://<resource-name>/openai/deployments/{deployment-id}/images/edits` <br> <br> - [BFL service provider API](https://docs.bfl.ai/kontext/kontext_text_to_image): ` <resource-name>/providers/blackforestlabs/v1/flux-kontext-pro?api-version=preview `  | - **Input:** text and image (5,000 tokens and 1 image)  <br /> - **Output:** One Image  <br />  - **Tool calling:** No <br /> - **Response formats**: Image (PNG and JPG) <br /> - **Key features:** Character consistency, advanced editing <br /> - **Additional parameters:** *(In provider-specific API only)* `seed`, `aspect ratio`, `input_image`, `prompt_unsampling`, `safety_tolerance`, `output_format`  |- Global standard (all regions) | Foundry, Hub-based |
| [FLUX-1.1-pro](https://ai.azure.com/explore/models/FLUX-1.1-pro/version/1/registry/azureml-blackforestlabs/?cid=learnDocs) | **Image generation** <br> - [Image API](../../openai/reference-preview.md): `https://<resource-name>/openai/deployments/{deployment-id}/images/generations` <br> <br> - [BFL service provider API](https://docs.bfl.ai/flux_models/flux_1_1_pro): ` <resource-name>/providers/blackforestlabs/v1/flux-pro-1.1?api-version=preview ` | - **Input:** text (5,000 tokens and 1 image)  <br /> - **Output:** One Image  <br />  - **Tool calling:** No <br /> - **Response formats:** Image (PNG and JPG) <br /> - **Key features:** Fast inference speed, strong prompt adherence, competitive pricing, scalable generation <br /> - **Additional parameters:** *(In provider-specific API only)* `width`, `height`, `prompt_unsampling`, `seed`, `safety_tolerance`, `output_format` | - Global standard (all regions) | Foundry, Hub-based |

::: moniker-end

::: moniker range="foundry"

| Model  | Type & API endpoint| Capabilities | Deployment type (region availability) | 
| ------ | ------------------ | ------------ | ------------------------------------- |
| `FLUX.1-Kontext-pro` | **Image generation** <br> - [Image API](../../openai/reference-preview.md): `https://<resource-name>/openai/deployments/{deployment-id}/images/generations` <br> and <br> `https://<resource-name>/openai/deployments/{deployment-id}/images/edits` <br> <br> - [BFL service provider API](https://docs.bfl.ai/kontext/kontext_text_to_image): ` <resource-name>/providers/blackforestlabs/v1/flux-kontext-pro?api-version=preview `  | - **Input:** text and image (5,000 tokens and 1 image)  <br /> - **Output:** One Image  <br />  - **Tool calling:** No <br /> - **Response formats**: Image (PNG and JPG) <br /> - **Key features:** Character consistency, advanced editing <br /> - **Additional parameters:** *(In provider-specific API only)* `seed`, `aspect ratio`, `input_image`, `prompt_unsampling`, `safety_tolerance`, `output_format`  |- Global standard (all regions) |
| `FLUX-1.1-pro` | **Image generation** <br> - [Image API](../../openai/reference-preview.md): `https://<resource-name>/openai/deployments/{deployment-id}/images/generations` <br> <br> - [BFL service provider API](https://docs.bfl.ai/flux_models/flux_1_1_pro): ` <resource-name>/providers/blackforestlabs/v1/flux-pro-1.1?api-version=preview ` | - **Input:** text (5,000 tokens and 1 image)  <br /> - **Output:** One Image  <br />  - **Tool calling:** No <br /> - **Response formats:** Image (PNG and JPG) <br /> - **Key features:** Fast inference speed, strong prompt adherence, competitive pricing, scalable generation <br /> - **Additional parameters:** *(In provider-specific API only)* `width`, `height`, `prompt_unsampling`, `seed`, `safety_tolerance`, `output_format` | - Global standard (all regions) |

::: moniker-end

See [this model collection in Microsoft Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=black+forest+labs/?cid=learnDocs).

## DeepSeek models sold directly by Azure

The DeepSeek family of models includes DeepSeek-R1, which excels at reasoning tasks by using a step-by-step training process, such as language, scientific reasoning, and coding tasks.

::: moniker range="foundry-classic"

| Model  | Type | Capabilities | Deployment type (region availability) | Project type |
| ------ | ---- | ------------ | ------------------------------------- | ------------ |
| [DeepSeek-V3.1](https://ai.azure.com/resource/models/DeepSeek-V3.1/version/1/registry/azureml-deepseek?cid=learnDocs) | chat-completion <br /> [(with reasoning content)](../how-to/use-chat-reasoning.md) | - **Input:** text (131,072 tokens) <br /> - **Output:**  (131,072 tokens) <br /> - **Languages:** `en` and `zh` <br />  - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON | - Global standard (all regions) | Foundry, Hub-based |
| [DeepSeek-R1-0528](https://ai.azure.com/explore/models/deepseek-r1-0528/version/1/registry/azureml-deepseek?cid=learnDocs) | chat-completion <br /> [(with reasoning content)](../how-to/use-chat-reasoning.md) | - **Input:** text (163,840 tokens) <br /> - **Output:**  (163,840 tokens) <br /> - **Languages:** `en` and `zh` <br />  - **Tool calling:** No <br /> - **Response formats:** Text. | - Global standard (all regions) <br> - Global provisioned (all regions)| Foundry, Hub-based |
| [DeepSeek-V3-0324](https://ai.azure.com/explore/models/deepseek-v3-0324/version/1/registry/azureml-deepseek?cid=learnDocs) | chat-completion | - **Input:** text (131,072 tokens) <br /> - **Output:**  (131,072 tokens) <br /> - **Languages:** `en` and `zh` <br />  - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON | - Global standard (all regions) <br> - Global provisioned (all regions) | Foundry, Hub-based |
| [DeepSeek-R1](https://ai.azure.com/explore/models/deepseek-r1/version/1/registry/azureml-deepseek?cid=learnDocs) | chat-completion <br /> [(with reasoning content)](../how-to/use-chat-reasoning.md) | - **Input:** text (163,840 tokens) <br /> - **Output:**  (163,840 tokens) <br /> - **Languages:** `en` and `zh` <br />  - **Tool calling:** No <br /> - **Response formats:** Text. | - Global standard (all regions) <br> - Global provisioned (all regions) | Foundry, Hub-based |

::: moniker-end

::: moniker range="foundry"

| Model  | Type | Capabilities | Deployment type (region availability) |
| ------ | ---- | ------------ | ------------------------------------- |
| `DeepSeek-V3.1` | chat-completion <br /> [(with reasoning content)](../how-to/use-chat-reasoning.md) | - **Input:** text (131,072 tokens) <br /> - **Output:**  (131,072 tokens) <br /> - **Languages:** `en` and `zh` <br />  - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON | - Global standard (all regions) |
| `DeepSeek-R1-0528` | chat-completion <br /> [(with reasoning content)](../how-to/use-chat-reasoning.md) | - **Input:** text (163,840 tokens) <br /> - **Output:**  (163,840 tokens) <br /> - **Languages:** `en` and `zh` <br />  - **Tool calling:** No <br /> - **Response formats:** Text. | - Global standard (all regions) <br> - Global provisioned (all regions)|
| `DeepSeek-V3-0324` | chat-completion | - **Input:** text (131,072 tokens) <br /> - **Output:**  (131,072 tokens) <br /> - **Languages:** `en` and `zh` <br />  - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON | - Global standard (all regions) <br> - Global provisioned (all regions) |
| `DeepSeek-R1` | chat-completion <br /> [(with reasoning content)](../how-to/use-chat-reasoning.md) | - **Input:** text (163,840 tokens) <br /> - **Output:**  (163,840 tokens) <br /> - **Languages:** `en` and `zh` <br />  - **Tool calling:** No <br /> - **Response formats:** Text. | - Global standard (all regions) <br> - Global provisioned (all regions) |

::: moniker-end

See [this model collection in Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=DeepSeek/?cid=learnDocs).

## Meta models sold directly by Azure

Meta Llama models and tools are a collection of pretrained and fine-tuned generative AI text and image reasoning models. Meta models range in scale to include:

- Small language models (SLMs) like 1B and 3B Base and Instruct models for on-device and edge inferencing
- Mid-size large language models (LLMs) like 7B, 8B, and 70B Base and Instruct models
- High-performance models like Meta Llama 3.1-405B Instruct for synthetic data generation and distillation use cases.

::: moniker range="foundry-classic"

| Model  | Type | Capabilities | Deployment type (region availability) | Project type |
| ------ | ---- | ------------ | ------------------------------------- | ------------ |
| [Llama-4-Maverick-17B-128E-Instruct-FP8](https://ai.azure.com/explore/models/Llama-4-Maverick-17B-128E-Instruct-FP8/version/1/registry/azureml-meta/?cid=learnDocs) | chat-completion | - **Input:** text and images (1M tokens) <br /> - **Output:** text (1M tokens) <br /> - **Languages:** `ar`, `en`, `fr`, `de`, `hi`, `id`, `it`, `pt`, `es`, `tl`, `th`, and `vi` <br />  - **Tool calling:** No <br /> - **Response formats:** Text | - Global standard (all regions) | Foundry, Hub-based |
| [Llama-3.3-70B-Instruct](https://ai.azure.com/explore/models/Llama-3.3-70B-Instruct/version/4/registry/azureml-meta/?cid=learnDocs) | chat-completion | - **Input:** text (128,000 tokens) <br /> - **Output:** text (8,192 tokens) <br /> - **Languages:** `en`, `de`, `fr`, `it`, `pt`, `hi`, `es`, and `th` <br />  - **Tool calling:** No <br /> - **Response formats:** Text | - Global standard (all regions) | Foundry, Hub-based |

::: moniker-end

::: moniker range="foundry"

| Model  | Type | Capabilities | Deployment type (region availability) |
| ------ | ---- | ------------ | ------------------------------------- |
| `Llama-4-Maverick-17B-128E-Instruct-FP8` | chat-completion | - **Input:** text and images (1M tokens) <br /> - **Output:** text (1M tokens) <br /> - **Languages:** `ar`, `en`, `fr`, `de`, `hi`, `id`, `it`, `pt`, `es`, `tl`, `th`, and `vi` <br />  - **Tool calling:** No <br /> - **Response formats:** Text | - Global standard (all regions) |
| `Llama-3.3-70B-Instruct` | chat-completion | - **Input:** text (128,000 tokens) <br /> - **Output:** text (8,192 tokens) <br /> - **Languages:** `en`, `de`, `fr`, `it`, `pt`, `hi`, `es`, and `th` <br />  - **Tool calling:** No <br /> - **Response formats:** Text | - Global standard (all regions) |

::: moniker-end

See [this model collection in Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=Meta/?cid=learnDocs). You can also find several Meta models available [from partners and community](../concepts/models-from-partners.md#meta).

## Microsoft models sold directly by Azure

Microsoft models include various model groups such as MAI models, Phi models, healthcare AI models, and more. 

::: moniker range="foundry-classic"

| Model  | Type | Capabilities | Deployment type (region availability) | Project type |
| ------ | ---- | ------------ | ------------------------------------- | ------------ |
| [MAI-DS-R1](https://ai.azure.com/explore/models/MAI-DS-R1/version/1/registry/azureml/?cid=learnDocs) | chat-completion <br /> [(with reasoning content)](../how-to/use-chat-reasoning.md) | - **Input:** text (163,840 tokens) <br /> - **Output:**  (163,840 tokens) <br /> - **Languages:** `en` and `zh` <br />  - **Tool calling:** No <br /> - **Response formats:** Text. |- Global standard (all regions) | Foundry, Hub-based |

::: moniker-end

::: moniker range="foundry"

| Model  | Type | Capabilities | Deployment type (region availability) |
| ------ | ---- | ------------ | ------------------------------------- |
| `MAI-DS-R1` | chat-completion <br /> [(with reasoning content)](../how-to/use-chat-reasoning.md) | - **Input:** text (163,840 tokens) <br /> - **Output:**  (163,840 tokens) <br /> - **Languages:** `en` and `zh` <br />  - **Tool calling:** No <br /> - **Response formats:** Text. |- Global standard (all regions) |

::: moniker-end

See [the Microsoft model collection in Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=Microsoft/?cid=learnDocs). You can also find several Microsoft models available [from partners and community](../concepts/models-from-partners.md#microsoft).

### Model router

Model router is a large language model that intelligently selects from a set of underlying chat models to respond to a given prompt. For more information, see the [Model router overview](/azure/ai-foundry/openai/how-to/model-router).

#### Region availability

| Model | Region |
|---|---|
| `model-router` (2025-08-07) | East US 2 (Global Standard & Data Zone Standard), Sweden Central (Global Standard & Data Zone Standard) |
| `model-router` (2025-05-19) | East US 2 (Global Standard & Data Zone Standard), Sweden Central (Global Standard & Data Zone Standard) |
| `model-router` (2025-11-18) | East US 2 (Global Standard & Data Zone Standard), Sweden Central (Global Standard & Data Zone Standard) |

*Billing for Data Zone Standard model router deployments will begin no earlier than November 1, 2025.*

#### Capabilities

|  Model ID  | Description | Context window | Max output tokens | Training data (up to)  |
|  --- |  :--- |:--- |:---|:---: |
| `model-router` (2025-08-07) | A model that intelligently selects from a set of underlying models to respond to a given prompt. | 200,000 | 32,768 (`GPT-4.1 series`)</br> 100,000 (`o4-mini`)</br> 128,000 (`gpt-5 reasoning models`) </br> 16,384 (`gpt-5-chat`) | - |
| `model-router` (2025-05-19) | A model that intelligently selects from a set of underlying models to respond to a given prompt. | 200,000 | 32,768 (`GPT-4.1 series`)</br> 100,000 (`o4-mini`) | May 31, 2024 |
| `model-router` (2025-11-18) | A model that intelligently selects from a configurable set of underlying chat models to respond to a given prompt. | TBD | TBD | TBD |

Larger context windows are compatible with *some* of the underlying models. That means an API call with a larger context succeeds only if the prompt happens to be routed to the right model. Otherwise, the call fails.



## Mistral models sold directly by Azure

::: moniker range="foundry-classic"

| Model  | Type | Capabilities | Deployment type (region availability) | Project type |
| ------ | ---- | ------------ | ------------------------------------- | ------------ |
| [mistral-large-3](https://ai.azure.com/explore/models/mistral-large-3/version/1/registry/azureml-mistral/?cid=learnDocs) | chat-completion | - **Input:** text, image <br /> - **Output:** text  <br /> - **Languages:** en <br />  - **Tool calling:** no  <br /> - **Response formats:** Text, JSON, Markdown  |- Global standard (West US)  | Foundry |
| [mistral-document-ai-2505](https://ai.azure.com/explore/models/mistral-document-ai-2505/version/1/registry/azureml-mistral/?cid=learnDocs) | Image-to-Text | - **Input:** image or PDF pages (30 pages, max 30MB PDF file) <br /> - **Output:** text  <br /> - **Languages:** en <br />  - **Tool calling:** no  <br /> - **Response formats:** Text, JSON, Markdown  |- Global standard (all regions) <br /> - Data zone standard (US and EU)  | Foundry |

::: moniker-end

::: moniker range="foundry"

| Model  | Type | Capabilities | Deployment type (region availability) |
| ------ | ---- | ------------ | ------------------------------------- |
| `mistral-large-3` | chat-completion | - **Input:** text, image <br /> - **Output:** text  <br /> - **Languages:** en <br />  - **Tool calling:** no  <br /> - **Response formats:** Text, JSON, Markdown  |- Global standard (West US)  |
| `mistral-document-ai-2505` | Image-to-Text | - **Input:** image or PDF pages (30 pages, max 30MB PDF file) <br /> - **Output:** text  <br /> - **Languages:** en <br />  - **Tool calling:** no  <br /> - **Response formats:** Text, JSON, Markdown  |- Global standard (all regions) <br /> - Data zone standard (US and EU)  |

::: moniker-end

See [the Mistral model collection in Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=Mistral+AI/?cid=learnDocs).  You can also find several Mistral models available [from partners and community](../concepts/models-from-partners.md#mistral-ai).

## xAI models sold directly by Azure

xAI's Grok models in Foundry Models include a diverse set of models designed to excel in various enterprise domains with different capabilities and price points, including: 

- Grok 3, a non-reasoning model pretrained by the Colossus datacenter, is tailored for business use cases such as data extraction, coding, and text summarization, with exceptional instruction-following capabilities. It supports a 131,072 token context window, allowing it to handle extensive inputs while maintaining coherence and depth, and is adept at drawing connections across domains and languages.
 
- Grok 3 Mini is a lightweight reasoning model trained to tackle agentic, coding, mathematical, and deep science problems with test-time compute. It also supports a 131,072 token context window for understanding codebases and enterprise documents, and excels at using tools to solve complex logical problems in novel environments, offering raw reasoning traces for user inspection with adjustable thinking budgets. 

- Grok Code Fast 1, a fast and efficient reasoning model designed for use in agentic coding applications. It was pretrained on a coding-focused data mixture, then post-trained on demonstrations of various coding tasks and tool use as well as demonstrations of correct refusal behaviors based on xAI's safety policy. 
[Registration is required for access to the grok-code-fast-1 model](https://aka.ms/xai/grok-code-fast-1).

- Grok 4 Fast, an efficiency-optimized language model that delivers near-Grok 4 reasoning capabilities with significantly lower latency and cost, and can bypass reasoning entirely for ultra-fast applications. It is trained for safe and effective tool use, with built-in refusal behaviors, a fixed safety-enforcing system prompt, and input filters to prevent misuse.

- Grok 4 is the latest reasoning model from xAI with advanced reasoning and tool-use capabilities,
enabling it to achieve new state-of-the-art performance across challenging academic and industry
benchmarks. [Registration is required for access to the grok-4 model](https://aka.ms/xai/grok-4).

::: moniker range="foundry-classic"

| Model  | Type | Capabilities | Deployment type (region availability) | Project type |
| ------ | ---- | ------------ | ------------------------------------- | ------------ |
| [grok-4](https://ai.azure.com/explore/models/grok-4/version/1/registry/azureml-xai/?cid=learnDocs)  | chat-completion | - **Input:** text, image (256,000 tokens) <br /> - **Output:** text (8,192 tokens) <br /> - **Languages:** `en` <br />  - **Tool calling:** yes <br /> - **Response formats:** text |- Global standard (all regions)  | Foundry, Hub-based |
| [grok-4-fast-reasoning](https://ai.azure.com/explore/models/grok-4-fast-reasoning/version/1/registry/azureml-xai/?cid=learnDocs)  | chat-completion | - **Input:** text, image (2,000,000 tokens) <br /> - **Output:** text (2,000,000 tokens) <br /> - **Languages:** `en` <br />  - **Tool calling:** yes <br /> - **Response formats:** text |- Global standard (all regions) <br> - Data zone standard (US)  | Foundry, Hub-based |
| [grok-4-fast-non-reasoning](https://ai.azure.com/explore/models/grok-4-fast-non-reasoning/version/1/registry/azureml-xai/?cid=learnDocs)  | chat-completion | - **Input:** text, image (2,000,000 tokens) <br /> - **Output:** text (2,000,000 tokens) <br /> - **Languages:** `en` <br />  - **Tool calling:** yes <br /> - **Response formats:** text |- Global standard (all regions) <br> - Data zone standard (US)  | Foundry, Hub-based |
| [grok-code-fast-1](https://ai.azure.com/explore/models/grok-code-fast-1/version/1/registry/azureml-xa/?cid=learnDocs)  | chat-completion | - **Input:** text (256,000 tokens) <br /> - **Output:** text (8,192 tokens) <br /> - **Languages:** `en` <br />  - **Tool calling:** yes <br /> - **Response formats:** text |- Global standard (all regions)  | Foundry, Hub-based |
| [grok-3](https://ai.azure.com/explore/models/grok-3/version/1/registry/azureml-xai/?cid=learnDocs) | chat-completion | - **Input:** text (131,072 tokens) <br /> - **Output:** text (131,072 tokens) <br /> - **Languages:** `en` <br />  - **Tool calling:** yes <br /> - **Response formats:** text |- Global standard (all regions) <br> - Data zone standard (US) | Foundry, Hub-based |
| [grok-3-mini](https://ai.azure.com/explore/models/grok-3-mini/version/1/registry/azureml-xai/?cid=learnDocs) | chat-completion | - **Input:** text (131,072 tokens) <br /> - **Output:** text (131,072 tokens) <br /> - **Languages:** `en` <br />  - **Tool calling:** yes <br /> - **Response formats:** text | - Global standard (all regions) <br> - Data zone standard (US) | Foundry, Hub-based |

::: moniker-end

::: moniker range="foundry"

| Model  | Type | Capabilities | Deployment type (region availability) |
| ------ | ---- | ------------ | ------------------------------------- |
| `grok-4`  | chat-completion | - **Input:** text, image (256,000 tokens) <br /> - **Output:** text (8,192 tokens) <br /> - **Languages:** `en` <br />  - **Tool calling:** yes <br /> - **Response formats:** text |- Global standard (all regions)  |
| `grok-4-fast-reasoning`  | chat-completion | - **Input:** text, image (2,000,000 tokens) <br /> - **Output:** text (2,000,000 tokens) <br /> - **Languages:** `en` <br />  - **Tool calling:** yes <br /> - **Response formats:** text |- Global standard (all regions) <br> - Data zone standard (US)  |
| `grok-4-fast-non-reasoning`  | chat-completion | - **Input:** text, image (2,000,000 tokens) <br /> - **Output:** text (2,000,000 tokens) <br /> - **Languages:** `en` <br />  - **Tool calling:** yes <br /> - **Response formats:** text |- Global standard (all regions) <br> - Data zone standard (US)  |
| `grok-code-fast-1`  | chat-completion | - **Input:** text (256,000 tokens) <br /> - **Output:** text (8,192 tokens) <br /> - **Languages:** `en` <br />  - **Tool calling:** yes <br /> - **Response formats:** text |- Global standard (all regions)  |
| `grok-3` | chat-completion | - **Input:** text (131,072 tokens) <br /> - **Output:** text (131,072 tokens) <br /> - **Languages:** `en` <br />  - **Tool calling:** yes <br /> - **Response formats:** text |- Global standard (all regions) <br> - Data zone standard (US) |
| `grok-3-mini` | chat-completion | - **Input:** text (131,072 tokens) <br /> - **Output:** text (131,072 tokens) <br /> - **Languages:** `en` <br />  - **Tool calling:** yes <br /> - **Response formats:** text | - Global standard (all regions) <br> - Data zone standard (US) |

::: moniker-end

See [the xAI model collection in Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=xAI/?cid=learnDocs).

## Model region availability by deployment type

Foundry Models gives you choices for the hosting structure that fits your business and usage patterns. The service offers two main types of deployment:

- **Standard**: Has a global deployment option, routing traffic globally to provide higher throughput.
- **Provisioned**: Also has a global deployment option, allowing you to purchase and deploy provisioned throughput units across Azure global infrastructure.

All deployments perform the same inference operations, but the billing, scale, and performance differ. For more information about deployment types, see [Deployment types in Foundry Models](../concepts/deployment-types.md).

# [Global Standard](#tab/global-standard)

### Global Standard model availability

[!INCLUDE [global-standard](model-matrix/global-standard.md)]

# [Global Provisioned managed](#tab/global-ptum)

### Global Provisioned managed model availability

[!INCLUDE [global-provisioned-managed](model-matrix/global-provisioned-managed.md)]

# [Data Zone Standard](#tab/data-zone-standard)

### Data Zone Standard model availability

[!INCLUDE [data-zone-standard](model-matrix/data-zone-standard.md)]

---

::: moniker range="foundry-classic"

[!INCLUDE [models-open-and-custom](models-open-custom.md)]

::: moniker-end

## Related content

- [Foundry Models from partners and community](../concepts/models-from-partners.md)
- [Deployment overview for Foundry Models](../../concepts/deployments-overview.md)
- [Add and configure models to Foundry Models](../how-to/create-model-deployments.md)
- [Deployment types in Foundry Models](../concepts/deployment-types.md)

::: moniker range="foundry-classic"

- [Serverless API inference examples for Foundry Models](../../concepts/models-inference-examples.md)

::: moniker-end
