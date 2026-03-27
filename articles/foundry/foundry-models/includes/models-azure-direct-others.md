---
title: Other Foundry Models sold directly by Azure
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: include
ms.date: 03/25/2026
ms.author: mopeakande
author: msakande
ai-usage: ai-assisted
ms.custom: pilot-ai-workflow-jan-2026, classic-and-new

---

> [!NOTE]
> Foundry Models sold directly by Azure also include all Azure OpenAI models. To learn about these models, switch to the [Azure OpenAI models](../../foundry-models/concepts/models-sold-directly-by-azure.md?pivots=azure-openai) collection at the top of this article. 

## Black Forest Labs models sold directly by Azure

Black Forest Labs (BFL) FLUX models bring state-of-the-art image generation to Microsoft Foundry, enabling you to generate and edit high-quality images from text prompts and reference images. FLUX models support a range of capabilities including text-to-image generation, multi-reference image editing, and in-context generation and editing. 

You can run these models through the BFL service provider API and through the [images/generations and images/edits endpoints](../../openai/reference-preview.md). 

To work with FLUX models in Foundry, see [Deploy and use FLUX models in Microsoft Foundry](../how-to/use-foundry-models-flux.md).

- [Registration is required for access to FLUX.2 [flex]](https://customervoice.microsoft.com/Pages/ResponsePage.aspx?id=v4j5cvGGr0GRqy180BHbR7en2Ais5pxKtso_Pz4b1_xUMzM2TDBZRko3QldSSFlWREhQSEpSSEdKVyQlQCN0PWcu).

| Model  | Type & API endpoint| Capabilities | Deployment type (region availability) | 
| ------ | ------------------ | ------------ | ------------------------------------- |
| `FLUX.2-flex` | **Image generation** <br> - [BFL service provider API](https://docs.bfl.ai/flux_2/flux2_text_to_image): `<resource-name>/providers/blackforestlabs/v1/flux-2-flex` | - **Input:** text and image (32,000 tokens and up to 10 images<sup>i</sup>) <br /> - **Output:** One Image <br /> - **Tool calling:** No <br /> - **Response formats:** Image (PNG and JPG) <br /> - **Key features:** Fine-grained control; multi-reference support for up to 10 images <br /> - **Additional parameters:** <br> `guidance`: Controls how closely the output follows the prompt. Minimum: 1.5, maximum: 10, default: 4.5. Higher = closer prompt adherence. <br> `steps`: Number of inference steps. Maximum: 50, default: 50.  Higher = more detail, slower. | - Global standard (all regions) |
| `FLUX.2-pro` | **Image generation** <br> - [BFL service provider API](https://docs.bfl.ai/flux_2/flux2_text_to_image): `<resource-name>/providers/blackforestlabs/v1/flux-2-pro` | - **Input:** text and image (32,000 tokens and up to 8 images<sup>ii</sup>)  <br /> - **Output:** One Image  <br />  - **Tool calling:** No <br /> - **Response formats:** Image (PNG and JPG)  <br /> - **Key features:** Multi-reference support for up to 8 images; more grounded in real-world knowledge; greater output flexibility; enhanced performance <br /> - **Additional parameters:** *(In provider-specific API only)* Supports all parameters.  | - Global standard (all regions) |
| `FLUX.1-Kontext-pro` | **Image generation** <br> - [Image API](../../openai/reference-preview.md): `https://<resource-name>/openai/deployments/{deployment-id}/images/generations` <br> and <br> `https://<resource-name>/openai/deployments/{deployment-id}/images/edits` <br> <br> - [BFL service provider API](https://docs.bfl.ai/kontext/kontext_text_to_image): ` <resource-name>/providers/blackforestlabs/v1/flux-kontext-pro?api-version=preview `  | - **Input:** text and image (5,000 tokens and 1 image)  <br /> - **Output:** One Image  <br />  - **Tool calling:** No <br /> - **Response formats:** Image (PNG and JPG) <br /> - **Key features:** Character consistency, advanced editing <br /> - **Additional parameters:** *(In provider-specific API only)* `seed`, `aspect ratio`, `input_image`, `prompt_unsampling`, `safety_tolerance`, `output_format`  |- Global standard (all regions) |
| `FLUX-1.1-pro` | **Image generation** <br> - [Image API](../../openai/reference-preview.md): `https://<resource-name>/openai/deployments/{deployment-id}/images/generations` <br> <br> - [BFL service provider API](https://docs.bfl.ai/flux_models/flux_1_1_pro): ` <resource-name>/providers/blackforestlabs/v1/flux-pro-1.1?api-version=preview ` | - **Input:** text (5,000 tokens and 1 image)  <br /> - **Output:** One Image  <br />  - **Tool calling:** No <br /> - **Response formats:** Image (PNG and JPG) <br /> - **Key features:** Fast inference speed, strong prompt adherence, competitive pricing, scalable generation <br /> - **Additional parameters:** *(In provider-specific API only)* `width`, `height`, `prompt_unsampling`, `seed`, `safety_tolerance`, `output_format` | - Global standard (all regions) |

<sup>i,ii</sup> Support for **multiple reference images** are available for FLUX.2 [pro] and FLUX.2 [flex] by using the API, but *not* in the playground.

See [this model collection in Microsoft Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=black+forest+labs/?cid=learnDocs).

## Cohere models sold directly by Azure

The Cohere family of models includes various models optimized for different use cases, including chat completions, rerank/text classification, and embeddings. Cohere models are optimized for various use cases that include reasoning, summarization, and question answering.

| Model  | Type | Capabilities | Deployment type (region availability) |
| ------ | ---- | ------------ | ------------------------------------- |
| [Cohere-rerank-v4.0-pro](https://ai.azure.com/resource/models/Cohere-rerank-v4.0-pro/version/1/registry/azureml-cohere/?cid=learnDocs) | text classification (rerank) | - **Input:** text <br /> - **Output:** text <br /> - **Languages:** `en`, `fr`, `es`, `it`, `de`, `pt-br`, `ja`, `zh-cn`, `ar`, `vi`, `hi`, `ru`, `id`, and `nl` <br />  - **Tool calling:** No <br /> - **Response formats:** JSON | - Global standard (all regions) <br> - Managed compute |
| [Cohere-rerank-v4.0-fast](https://ai.azure.com/resource/models/Cohere-rerank-v4.0-fast/version/2/registry/azureml-cohere/?cid=learnDocs) | text classification (rerank) | - **Input:** text <br /> - **Output:** text <br /> - **Languages:** `en`, `fr`, `es`, `it`, `de`, `pt-br`, `ja`, `zh-cn`, `ar`, `vi`, `hi`, `ru`, `id`, and `nl` <br />  - **Tool calling:** No <br /> - **Response formats:** JSON | - Global standard (all regions) <br> - Managed compute |
| `Cohere-command-a` | chat-completion | - **Input:** text (131,072 tokens) <br /> - **Output:** text (8,182 tokens) <br /> - **Languages:** `en`, `fr`, `es`, `it`, `de`, `pt-br`, `ja`, `ko`, `zh-cn`, and `ar` <br />  - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON | - Global standard (all regions) |
| `embed-v-4-0` | embeddings | - **Input:** text (512 tokens) and images (2MM pixels) <br /> - **Output:** Vector (256, 512, 1024, 1536 dim.) <br /> - **Languages:** `en`, `fr`, `es`, `it`, `de`, `pt-br`, `ja`, `ko`, `zh-cn`, and `ar` | - Global standard (all regions) |

See [the Cohere model collection in the Foundry portal](https://ai.azure.com/explore/models?selectedCollection=Cohere/?cid=learnDocs,cohere).

## DeepSeek models sold directly by Azure

The DeepSeek family of models includes several reasoning models, which excel at reasoning tasks by using a step-by-step training process, such as language, scientific reasoning, and coding tasks.

| Model  | Type | Capabilities | Deployment type (region availability) |
| ------ | ---- | ------------ | ------------------------------------- |
| `DeepSeek-V3.2-Speciale` | chat-completion <br /> [(with reasoning content)](../../../foundry-classic/foundry-models/how-to/use-chat-reasoning.md) | - **Input:** text (128,000 tokens) <br /> - **Output:** text (128,000 tokens) <br /> - **Languages:** `en` and `zh` <br />  - **Tool calling:** No <br /> - **Response formats:** Text, JSON | - Global standard (all regions) |
| `DeepSeek-V3.2` | chat-completion <br /> [(with reasoning content)](../../../foundry-classic/foundry-models/how-to/use-chat-reasoning.md) | - **Input:** text (128,000 tokens) <br /> - **Output:** text (128,000 tokens) <br /> - **Languages:** `en` and `zh` <br />  - **Tool calling:** No <br /> - **Response formats:** Text, JSON | - Global standard (all regions) |
| `DeepSeek-V3.1` | chat-completion <br /> [(with reasoning content)](../../../foundry-classic/foundry-models/how-to/use-chat-reasoning.md) | - **Input:** text (131,072 tokens) <br /> - **Output:** text (131,072 tokens) <br /> - **Languages:** `en` and `zh` <br />  - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON | - Global standard (all regions) |
| `DeepSeek-R1-0528` | chat-completion <br /> [(with reasoning content)](../../../foundry-classic/foundry-models/how-to/use-chat-reasoning.md) | - **Input:** text (163,840 tokens) <br /> - **Output:** text (163,840 tokens) <br /> - **Languages:** `en` and `zh` <br />  - **Tool calling:** No <br /> - **Response formats:** Text | - Global standard (all regions) <br> - Global provisioned (all regions)|
| `DeepSeek-V3-0324` | chat-completion | - **Input:** text (131,072 tokens) <br /> - **Output:** text (131,072 tokens) <br /> - **Languages:** `en` and `zh` <br />  - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON | - Global standard (all regions) <br> - Global provisioned (all regions) |
| `DeepSeek-R1` | chat-completion <br /> [(with reasoning content)](../../../foundry-classic/foundry-models/how-to/use-chat-reasoning.md) | - **Input:** text (163,840 tokens) <br /> - **Output:** text (163,840 tokens) <br /> - **Languages:** `en` and `zh` <br />  - **Tool calling:** No <br /> - **Response formats:** Text | - Global standard (all regions) <br> - Global provisioned (all regions) |

See [this model collection in the Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=DeepSeek/?cid=learnDocs).

## Meta models sold directly by Azure

Meta Llama models and tools are a collection of pretrained and fine-tuned generative AI text and image reasoning models. Meta models range in scale to include:

- Small language models (SLMs) like 1B and 3B Base and Instruct models for on-device and edge inferencing
- Mid-size large language models (LLMs) like 7B, 8B, and 70B Base and Instruct models
- High-performance models like Meta Llama 3.1-405B Instruct for synthetic data generation and distillation use cases.

| Model  | Type | Capabilities | Deployment type (region availability) |
| ------ | ---- | ------------ | ------------------------------------- |
| `Llama-4-Maverick-17B-128E-Instruct-FP8` | chat-completion | - **Input:** text and images (1M tokens) <br /> - **Output:** text (1M tokens) <br /> - **Languages:** `ar`, `en`, `fr`, `de`, `hi`, `id`, `it`, `pt`, `es`, `tl`, `th`, and `vi` <br />  - **Tool calling:** No <br /> - **Response formats:** Text | - Global standard (all regions) |
| `Llama-3.3-70B-Instruct` | chat-completion | - **Input:** text (128,000 tokens) <br /> - **Output:** text (8,192 tokens) <br /> - **Languages:** `en`, `de`, `fr`, `it`, `pt`, `hi`, `es`, and `th` <br />  - **Tool calling:** No <br /> - **Response formats:** Text | - Global standard (all regions)  <br> - Global provisioned (all regions) |

See [this model collection in the Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=Meta/?cid=learnDocs). You can also find several Meta models available [from partners and community](../concepts/models-from-partners.md#meta).

## Microsoft models sold directly by Azure

Microsoft models include various model groups such as Model Router, MAI models, Phi models, healthcare AI models, and more. See [the Microsoft model collection in the Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=Microsoft/?cid=learnDocs). You can also find several Microsoft models available [from partners and community](../concepts/models-from-partners.md#microsoft).

MAI-Image-2 is a text-to-image generation model designed to create high-quality, visually rich images from natural language prompts. It uses a diffusion-based generative approach to progressively refine images, enabling strong alignment between the input text and the generated output. To work with MAI-Image-2 in Foundry, see [Deploy and use MAI-image-2 in Microsoft Foundry](../how-to/use-foundry-models-mai.md).

| Model  | Type | Capabilities | Deployment type (region availability) |
| ------ | ---- | ------------ | ------------------------------------- |
| `MAI-Image-2` | Text-to-Image. See [API endpoint](../how-to/use-foundry-models-mai.md#api-endpoint) for details. | - **Input:** text <br /> - **Output:** One image. Maximum 1024×1024 pixels <br /> - **Context length**: 32,000 tokens <br /> - **Tool calling:** No <br /> - **Response formats:** Image (PNG) <br /> - **Languages:** `en` <br /> - **Key features:** High-quality text-to-image generation; photorealistic image synthesis with consistent visual structure; general-purpose image generation across creative, design, and visualization workflows <br /> - **Parameters:** `width`, `height`, `prompt` <br /> Supports image resolutions ranging from 256×256 to 1024×1024 pixels, with `width` and `height` configurable within this range depending on aspect ratio | - Global standard (all regions) |
| [model-router](https://ai.azure.com/resource/models/model-router/version/2025-11-18/registry/azureml-routers/?cid=learnDocs)<sup>1</sup> | chat-completion | More details in [Model router overview](/azure/ai-foundry/openai/how-to/model-router). <br> - **Input:** text, image <br /> - **Output:** text (max output tokens varies<sup>2</sup>) <br> **Context window:** 200,000<sup>3</sup> <br /> - **Languages:** `en` |- Global standard (East US 2, Sweden Central) <br> - Data Zone standard<sup>4</sup> (East US 2, Sweden Central) |
| `MAI-DS-R1` | chat-completion <br /> [(with reasoning content)](../../../foundry-classic/foundry-models/how-to/use-chat-reasoning.md) | - **Input:** text (163,840 tokens) <br /> - **Output:** text (163,840 tokens) <br /> - **Languages:** `en` and `zh` <br />  - **Tool calling:** No <br /> - **Response formats:** Text |- Global standard (all regions) |

<sup>1</sup> **Model router version** `2025-11-18`. Earlier versions (`2025-08-07` and `2025-05-19`) are also available. 

<sup>2</sup> **Max output tokens** varies for underlying models in the model router. For example, 32,768 (`GPT-4.1 series`), 100,000 (`o4-mini`), 128,000 (`gpt-5 reasoning models`), and 16,384 (`gpt-5-chat`).

<sup>3</sup> Larger **context windows** are compatible with *some* of the underlying models of the Model Router. That means an API call with a larger context succeeds only if the prompt gets routed to one of such models. Otherwise, the call fails.

<sup>4</sup> Billing for **Data Zone Standard** model router deployments begins no earlier than November 1, 2025.

## Mistral models sold directly by Azure

| Model  | Type | Capabilities | Deployment type (region availability) |
| ------ | ---- | ------------ | ------------------------------------- |
| `mistral-document-ai-2512` | Image-to-Text | - **Input:** image or PDF pages (30 pages, max 30MB PDF file) <br /> - **Output:** text  <br /> - **Languages:** `en` <br />  - **Tool calling:** no  <br /> - **Response formats:** Text, JSON, Markdown  |- Global standard (all regions) <br /> - Data zone standard (US and EU)  |
| `mistral-document-ai-2505` | Image-to-Text | - **Input:** image or PDF pages (30 pages, max 30MB PDF file) <br /> - **Output:** text  <br /> - **Languages:** `en` <br />  - **Tool calling:** no  <br /> - **Response formats:** Text, JSON, Markdown  |- Global standard (all regions) <br /> - Data zone standard (US and EU)  |
| `Mistral-Large-3` | chat-completion | - **Input:** text, image <br /> - **Output:** text  <br /> - **Languages:** `en`, `fr`, `de`, `es`, `it`, `pt`, `nl`, `zh`, `ja`, `ko`, and `ar` <br />  - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON  |- Global standard (all regions) <br> - Data zone standard (US and EU)   |

See [the Mistral model collection in the Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=Mistral+AI/?cid=learnDocs).  You can also find several Mistral models available [from partners and community](../concepts/models-from-partners.md#mistral-ai).

## Moonshot AI models sold directly by Azure

Moonshot AI models include Kimi K2.5 and Kimi K2 Thinking. Kimi K2.5 is a multimodal reasoning model that accepts text and image input, while Kimi K2 Thinking is the latest, most capable version of open-source thinking model. 

| Model  | Type | Capabilities | Deployment type (region availability) |
| ------ | ---- | ------------ | ------------------------------------- |
| `Kimi-K2.5` | chat-completion <br /> [(with reasoning content)](../../../foundry-classic/foundry-models/how-to/use-chat-reasoning.md) | - **Input:** text and image (262,144 tokens) <br /> - **Output:** text (262,144 tokens) <br /> - **Languages:** `en` and `zh` <br />  - **Tool calling:** Yes <br /> - **Response formats:** Text | - Global standard (all regions) |
| `Kimi-K2-Thinking` | chat-completion <br /> [(with reasoning content)](../../../foundry-classic/foundry-models/how-to/use-chat-reasoning.md) | - **Input:** text (262,144 tokens) <br /> - **Output:** text (262,144 tokens) <br /> - **Languages:** `en` and `zh` <br />  - **Tool calling:** Yes <br /> - **Response formats:** Text | - Global standard (all regions) |

See [this model collection in the Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=Moonshot+ai/?cid=learnDocs).

## xAI models sold directly by Azure

xAI's Grok models in Foundry Models include a diverse set of reasoning and non-reasoning models designed for enterprise use cases such as data extraction, coding, text summarization, and agentic applications.

[Registration is required for access to](https://aka.ms/xai/grok-4) `grok-code-fast-1` and `grok-4`.

| Model  | Type | Capabilities | Deployment type (region availability) |
| ------ | ---- | ------------ | ------------------------------------- |
| `grok-4.1-fast-reasoning`  | chat-completion | - **Input:** text, image (128,000 tokens) <br /> - **Output:** text (128,000 tokens) <br /> - **Languages:** `en` <br />  - **Tool calling:** yes <br /> - **Response formats:** text |- Global standard (all regions)  |
| `grok-4.1-fast-non-reasoning`  | chat-completion | - **Input:** text, image (128,000 tokens) <br /> - **Output:** text (128,000 tokens) <br /> - **Languages:** `en` <br />  - **Tool calling:** yes <br /> - **Response formats:** text |- Global standard (all regions)  |
| `grok-4`  | chat-completion | - **Input:** text (262,000 tokens) <br /> - **Output:** text (8,192 tokens) <br /> - **Languages:** `en` <br />  - **Tool calling:** yes <br /> - **Response formats:** text |- Global standard (all regions)  |
| `grok-4-fast-reasoning`  | chat-completion | - **Input:** text, image (128,000 tokens) <br /> - **Output:** text (128,000 tokens) <br /> - **Languages:** `en` <br />  - **Tool calling:** yes <br /> - **Response formats:** text |- Global standard (all regions) <br> - Data zone standard (US)  |
| `grok-4-fast-non-reasoning`  | chat-completion | - **Input:** text, image (128,000 tokens) <br /> - **Output:** text (128,000 tokens) <br /> - **Languages:** `en` <br />  - **Tool calling:** yes <br /> - **Response formats:** text |- Global standard (all regions) <br> - Data zone standard (US)  |
| `grok-code-fast-1`  | chat-completion | - **Input:** text (256,000 tokens) <br /> - **Output:** text (8,192 tokens) <br /> - **Languages:** `en` <br />  - **Tool calling:** yes <br /> - **Response formats:** text |- Global standard (all regions)  |
| `grok-3` | chat-completion | - **Input:** text (131,072 tokens) <br /> - **Output:** text (131,072 tokens) <br /> - **Languages:** `en` <br />  - **Tool calling:** yes <br /> - **Response formats:** text |- Global standard (all regions) <br> - Data zone standard (US) |
| `grok-3-mini` | chat-completion | - **Input:** text (131,072 tokens) <br /> - **Output:** text (131,072 tokens) <br /> - **Languages:** `en` <br />  - **Tool calling:** yes <br /> - **Response formats:** text | - Global standard (all regions) <br> - Data zone standard (US) |

See [the xAI model collection in the Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=xAI/?cid=learnDocs).

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

## Related content

- [Foundry Models from partners and community](../concepts/models-from-partners.md)
- [Model deprecation and retirement for Foundry Models](../../concepts/model-lifecycle-retirement.md)
- [Deployment overview for Foundry Models](../../../foundry-classic/concepts/deployments-overview.md)
- [Add and configure models to Foundry Models](../how-to/create-model-deployments.md)
- [Deployment types in Foundry Models](../concepts/deployment-types.md)

