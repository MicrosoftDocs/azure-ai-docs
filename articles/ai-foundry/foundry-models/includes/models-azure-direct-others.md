---
title: Other Foundry Models sold directly by Azure
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: include
ms.date: 09/05/2025
ms.author: mopeakande
author: msakande
---

### DeepSeek models sold directly by Azure

The DeepSeek family of models includes DeepSeek-R1, which excels at reasoning tasks by using a step-by-step training process, such as language, scientific reasoning, and coding tasks.

| Model  | Type | Capabilities | Deployment type (region availability) | Project type |
| ------ | ---- | ------------ | ------------------------------------- | ------------ |
| [DeepSeek-R1-0528](https://ai.azure.com/explore/models/deepseek-r1-0528/version/1/registry/azureml-deepseek) | chat-completion <br /> [(with reasoning content)](../how-to/use-chat-reasoning.md) | - **Input:** text (163,840 tokens) <br /> - **Output:**  (163,840 tokens) <br /> - **Languages:** `en` and `zh` <br />  - **Tool calling:** No <br /> - **Response formats:** Text. | - Global standard (all regions) <br> - Global provisioned (all regions)| Foundry, Hub-based |
| [DeepSeek-V3-0324](https://ai.azure.com/explore/models/deepseek-v3-0324/version/1/registry/azureml-deepseek) | chat-completion | - **Input:** text (131,072 tokens) <br /> - **Output:**  (131,072 tokens) <br /> - **Languages:** `en` and `zh` <br />  - **Tool calling:** Yes <br /> - **Response formats:** Text, JSON | - Global standard (all regions) <br> - Global provisioned (all regions) | Foundry, Hub-based |
| [DeepSeek-R1](https://ai.azure.com/explore/models/deepseek-r1/version/1/registry/azureml-deepseek) | chat-completion <br /> [(with reasoning content)](../how-to/use-chat-reasoning.md) | - **Input:** text (163,840 tokens) <br /> - **Output:**  (163,840 tokens) <br /> - **Languages:** `en` and `zh` <br />  - **Tool calling:** No <br /> - **Response formats:** Text. | - Global standard (all regions) <br> - Global provisioned (all regions) | Foundry, Hub-based |

See [this model collection in Azure AI Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=DeepSeek).

### Meta models sold directly by Azure

Meta Llama models and tools are a collection of pretrained and fine-tuned generative AI text and image reasoning models. Meta models range in scale to include:

- Small language models (SLMs) like 1B and 3B Base and Instruct models for on-device and edge inferencing
- Mid-size large language models (LLMs) like 7B, 8B, and 70B Base and Instruct models
- High-performance models like Meta Llama 3.1-405B Instruct for synthetic data generation and distillation use cases.

| Model  | Type | Capabilities | Deployment type (region availability) | Project type |
| ------ | ---- | ------------ | ------------------------------------- | ------------ |
| [Llama-4-Maverick-17B-128E-Instruct-FP8](https://ai.azure.com/explore/models/Llama-4-Maverick-17B-128E-Instruct-FP8/version/1/registry/azureml-meta) | chat-completion | - **Input:** text and images (1M tokens) <br /> - **Output:** text (1M tokens) <br /> - **Languages:** `ar`, `en`, `fr`, `de`, `hi`, `id`, `it`, `pt`, `es`, `tl`, `th`, and `vi` <br />  - **Tool calling:** No <br /> - **Response formats:** Text | - Global standard (all regions) | Foundry, Hub-based |
| [Llama-3.3-70B-Instruct](https://ai.azure.com/explore/models/Llama-3.3-70B-Instruct/version/4/registry/azureml-meta) | chat-completion | - **Input:** text (128,000 tokens) <br /> - **Output:** text (8,192 tokens) <br /> - **Languages:** `en`, `de`, `fr`, `it`, `pt`, `hi`, `es`, and `th` <br />  - **Tool calling:** No <br /> - **Response formats:** Text | - Global standard (all regions) | Foundry, Hub-based |

See [this model collection in Azure AI Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=Meta). You can also find several Meta models available [from partners and community](#meta).

### Microsoft models sold directly by Azure

Microsoft models include various model groups such as MAI models, Phi models, healthcare AI models, and more. To see all the available Microsoft models, view [the Microsoft model collection in Azure AI Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=phi).

| Model  | Type | Capabilities | Deployment type (region availability) | Project type |
| ------ | ---- | ------------ | ------------------------------------- | ------------ |
| [MAI-DS-R1](https://ai.azure.com/explore/models/MAI-DS-R1/version/1/registry/azureml) | chat-completion <br /> [(with reasoning content)](../how-to/use-chat-reasoning.md) | - **Input:** text (163,840 tokens) <br /> - **Output:**  (163,840 tokens) <br /> - **Languages:** `en` and `zh` <br />  - **Tool calling:** No <br /> - **Response formats:** Text. |- Global standard (all regions) | Foundry, Hub-based |

See [the Microsoft model collection in Azure AI Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=Microsoft). You can also find several Microsoft models available [from partners and community](#microsoft).

### Mistral models sold directly by Azure

| Model  | Type | Capabilities | Deployment type (region availability) | Project type |
| ------ | ---- | ------------ | ------------------------------------- | ------------ |
| [mistral-document-ai-2505](https://ai.azure.com/explore/models/mistral-document-ai-2505/version/1/registry/azureml-mistral) | Image-to-Text | - **Input:** image or PDF pages (30 pages, max 30MB PDF file) <br /> - **Output:** text  <br /> - **Languages:** en <br />  - **Tool calling:** no  <br /> - **Response formats:** Text, JSON, Markdown  |- Global standard (all regions) <br> - Data zone standard (US)  | Foundry |

See [the Mistral model collection in Azure AI Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=Mistral+AI).  You can also find several Mistral models available [from partners and community](#mistral-ai).


### xAI models sold directly by Azure

xAI's Grok models in Azure AI Foundry Models include a diverse set of models designed to excel in various enterprise domains with different capabilities and price points, including: 

- Grok 3, a non-reasoning model pretrained by the Colossus datacenter, is tailored for business use cases such as data extraction, coding, and text summarization, with exceptional instruction-following capabilities. It supports a 131,072 token context window, allowing it to handle extensive inputs while maintaining coherence and depth, and is adept at drawing connections across domains and languages.
- Grok 3 Mini is a lightweight reasoning model trained to tackle agentic, coding, mathematical, and deep science problems with test-time compute. It also supports a 131,072 token context window for understanding codebases and enterprise documents, and excels at using tools to solve complex logical problems in novel environments, offering raw reasoning traces for user inspection with adjustable thinking budgets. 
- Grok Code Fast 1, a fast and efficient reasoning model designed for use in agentic coding applications. It was pre-trained on a coding-focused data mixture, then post-trained on demonstrations of various coding tasks and tool use as well as demonstrations of correct refusal behaviors based on xAI's safety policy. Learn more about Grok Code Fast 1's capabilities, risks, and limitations, in the model card [here](https://ai.azure.com/explore/models/grok-code-fast-1/version/1/registry/azureml-xa). 

| Model  | Type | Capabilities | Deployment type (region availability) | Project type |
| ------ | ---- | ------------ | ------------------------------------- | ------------ |
| [grok-code-fast-1](https://ai.azure.com/explore/models/grok-code-fast-1/version/1/registry/azureml-xa) | chat-completion | - **Input:** text (256,000 tokens) <br /> - **Output:** text (8,192 tokens) <br /> - **Languages:** `en` <br />  - **Tool calling:** yes <br /> - **Response formats:** text |- Global standard (all regions)  | Foundry, Hub-based |
| [grok-3](https://ai.azure.com/explore/models/grok-3/version/1/registry/azureml-xai) | chat-completion | - **Input:** text (131,072 tokens) <br /> - **Output:** text (131,072 tokens) <br /> - **Languages:** `en` <br />  - **Tool calling:** yes <br /> - **Response formats:** text |- Global standard (all regions) <br> - Data zone standard (US) | Foundry, Hub-based |
| [grok-3-mini](https://ai.azure.com/explore/models/grok-3-mini/version/1/registry/azureml-xai) | chat-completion | - **Input:** text (131,072 tokens) <br /> - **Output:** text (131,072 tokens) <br /> - **Languages:** `en` <br />  - **Tool calling:** yes <br /> - **Response formats:** text | - Global standard (all regions) <br> - Data zone standard (US) | Foundry, Hub-based |

See [the xAI model collection in Azure AI Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=xAI).

## Open and custom models

The model catalog offers a larger selection of models from a wider range of providers. For these models, you can't use the option for [standard deployment in Azure AI Foundry resources](../../concepts/deployments-overview.md#standard-deployment-in-azure-ai-foundry-resources), where models are provided as APIs. Instead, to deploy these models, you might need to host them on your infrastructure, create an AI hub, and provide the underlying compute quota to host the models.

Furthermore, these models can be open-access or IP protected. In both cases, you have to deploy them in managed compute offerings in Azure AI Foundry. To get started, see [How-to: Deploy to Managed compute](../../how-to/deploy-models-managed.md).


## Related content

- [Deployment overview for Azure AI Foundry Models](../../concepts/deployments-overview.md)
- [Add and configure models to Azure AI Foundry Models](../how-to/create-model-deployments.md)
- [Deployment types in Azure AI Foundry Models](deployment-types.md)
- [Serverless API inference examples for Foundry Models](../../concepts/models-inference-examples.md)