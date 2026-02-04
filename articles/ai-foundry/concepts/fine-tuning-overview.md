---
title: Fine-tune models with Microsoft Foundry
titleSuffix: Microsoft Foundry
description: This article explains what fine-tuning is and under what circumstances you should consider doing it.
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.custom:
  - build-2024
  - code01
ms.topic: concept-article
ms.date: 12/03/2025
ms.reviewer: keli19
ms.author: ssalgado
manager: nitinme
author: ssalgadodev
#customer intent: As a developer, I want to learn what it means to fine-tune a model.
---

# Fine-tune models with Microsoft Foundry

[!INCLUDE [classic-banner](../includes/classic-banner.md)]

Fine-tuning customizes a pretrained AI model with additional training on a specific task or dataset to improve performance, add new skills, or enhance accuracy. The result is a new, optimized GenAI model based on the provided examples. This article walks you through key concepts and decisions to make before you fine-tune, including the type of fine-tuning that's right for your use case, and model selection criteria based on training techniques use-cases for fine-tuning and how it helps you in your GenAI journey.

If you're just getting started with fine-tuning, we recommend **GPT-4.1** for complex skills like language translation, domain adaptation, or advanced code generation. For more focused tasks (such as classification, sentiment analysis, or content moderation) or when distilling knowledge from a more sophisticated model, start with **GPT-4.1-mini** for faster iteration and lower costs.

## Top use cases for fine-tuning
Fine-tuning excels at customizing language models for specific applications and domains. Some key use cases include:
- **Domain Specialization:** Adapt a language model for a specialized field like medicine, finance, or law – where domain specific knowledge and terminology is important. Teach the model to understand technical jargon and provide more accurate responses.
- **Task Performance:** Optimize a model for a specific task like sentiment analysis, code generation, translation, or summarization. You can significantly improve the performance of a smaller model on a specific application, compared to a general purpose model.
- **Style and Tone:** Teach the model to match your preferred communication style – for example, adapt the model for formal business writing, brand-specific voice, or technical writing.
- **Instruction Following:** Improve the model's ability to follow specific formatting requirements, multi-step instructions, or structured outputs. In multi-agent frameworks, teach the model to call the right agent for the right task.
- **Compliance and Safety:** Train a fine-tuned model to adhere to organizational policies, regulatory requirements, or other guidelines unique to your application.
- **Language or Cultural Adaptation:** Tailor a language model for a specific language, dialect, or cultural context that may not be well represented in the training data.
Fine-tuning is especially valuable when a general-purpose model doesn't meet your specific requirements – but you want to avoid the cost and complexity of training a model from scratch.

## Serverless or Managed Compute?
Before picking a model, it's important to select the fine-tuning product that matches your needs. Microsoft's Foundry offers two primary modalities for fine tuning: serverless and managed compute.

- **Serverless** lets you customize models using our capacity with consumption-based pricing starting at $1.70 per million input tokens. We optimize training for speed and scalability while handling all infrastructure management. This approach requires no GPU quotas and provides exclusive access to OpenAI models, though with fewer hyperparameter options than managed compute.
- **Managed compute** offers a wider range of models and advanced customization through AzureML, but requires you to provide your own VMs for training and hosting. While this gives full control over resources, it demands high quotas that many customers lack, doesn't include OpenAI models, and can't use our multi-tenancy optimizations.

For most customers, serverless provides the best balance of ease-of-use, cost efficiency, and access to premium models. This document focuses on serverless options.

To find steps to fine-tuning a model in Foundry, see [Fine-tune Models in Foundry](../how-to/fine-tune-serverless.md) or [Fine-tune models using managed compute](../how-to/fine-tune-managed-compute.md). For detailed guidance on OpenAI fine-tuning see [Fine-tune Azure OpenAI Models](../openai/how-to/fine-tuning.md).

## Training Techniques

Once you identify a use case, you need to select the appropriate training technique - which guides the model you select for training. We offer three training techniques to optimize your models:

- **Supervised Fine-Tuning (SFT):** Foundational technique that trains your model on input-output pairs, teaching it to produce desired responses for specific inputs.
  - *Best for:* Most use cases including domain specialization, task performance, style and tone, following instructions, and language adaptation.
  - *When to use:* Start here for most projects. SFT addresses the broadest number of fine-tuning scenarios and provides reliable results with clear input-output training data.
  - *Supported Models:* GPT 4o, 4o-mini, 4.1, 4.1-mini, 4.1-nano; Llama 2 and Llama 3.1; Phi 4, Phi-4-mini-instruct; Mistral Nemo, Ministral-3B, Mistral Large (2411); NTT Tsuzumi-7b

- **Direct Preference Optimization (DPO):** Trains models to prefer certain types of responses over others by learning from comparative feedback, without requiring a separate reward model.
  - *Best for:* Improving response quality, safety, and alignment with human preferences.
  - *When to use:* When you have examples of preferred vs. non-preferred outputs, or when you need to optimize for subjective qualities like helpfulness, harmlessness, or style. Use cases include adapting models to a specific style and tone, or adapting a model to cultural preferences.
  - *Supported Models:* GPT 4o, 4.1, 4.1-mini, 4.1-nano

- **Reinforcement Fine-Tuning (RFT):** Uses reinforcement learning to optimize models based on reward signals, allowing for more complex optimization objectives.
  - *Best for:* Complex optimization scenarios where simple input-output pairs aren't sufficient.
  - *When to use:* RFT is ideal for objective domains like mathematics, chemistry, and physics where there are clear right and wrong answers and the model already shows some competency. It works best when lucky guessing is difficult and expert evaluators would consistently agree on an unambiguous, correct answer. Requires more ML expertise to implement effectively.
  - *Supported Models:* o4-mini

Most customers should start with SFT, as it addresses the broadest number of fine-tuning use cases.

Follow this link to view and download [example datasets](https://github.com/Azure-Samples/AIFoundry-Customization-Datasets) to try out fine-tuning.

## Training Modalities

- **Text-to-Text (All Models):** All our models support standard text-to-text fine-tuning for language-based tasks.
- **Vision + Text (GPT 4o, 4.1):** Some models support vision fine-tuning, accepting both image and text inputs while producing text outputs. Use cases for vision fine-tuning include interpreting charts, graphs, and visual data; content moderation; visual quality assessment; document processing with mixed text and image; and product cataloging from photographs.

## Model Comparison Table
This table provides an overview of the models available 

| Model                | Modalities    | Techniques   | Strengths                                                          | 
|----------------------|---------------|--------------|--------------------------------------------------------------------|
| GPT 4.1              | Text, Vision  | SFT, DPO     | Superior performance on sophisticated tasks, nuanced understanding |
| GPT 4.1-mini         | Text          | SFT, DPO     | Fast iteration, cost-effective, good for simple tasks              |
| GPT 4.1-nano         | Text          | SFT, DPO     | Fast, cost-effective, and minimal resource usage                   |
| GPT 4o               | Text, Vision  | SFT, DPO     | Previous generation flagship model for complex tasks               |
| GPT 4o-mini          | Text          | SFT          | Previous generation small model for simple tasks                   |
| o4-mini              | Text          | RFT          | Reasoning model suited for complex logical tasks                   |
| Phi 4                | Text          | SFT          | Cost effective option for simpler tasks                            |
| Ministral 3B         | Text          | SFT          | Low-cost option for faster iteration                               |
| Mistral Nemo         | Text          | SFT          | Balance between size and capability                                |
| Mistral Large (2411) | Text          | SFT          | Most capable Mistral model, better for complex tasks               |

## Get Started with Fine Tuning

1. **Define your use case:** Identify whether you need a highly capable general-purpose model (e.g. GPT 4.1), a smaller cost-effective model for a specific task (GPT 4.1-mini or nano), or a complex reasoning model (o4-mini).
2. **Prepare your data:** Start with 50-100 high-quality examples for initial testing, scaling to 500+ examples for production models.
3. **Choose your technique:** Begin with Supervised Fine-Tuning (SFT) unless you have specific requirements for reasoning models / RFT.
4. **Iterate and evaluate:** Fine-tuning is an iterative process—start with a baseline, measure performance, and refine your approach based on results.

To find steps to fine-tuning a model in Foundry, see [Fine-tune Models in Foundry](../how-to/fine-tune-serverless.md), [Fine-tune Azure OpenAI Models](../openai/how-to/fine-tuning.md), or [Fine-tune models using managed compute](../how-to/fine-tune-managed-compute.md).

## Fine-Tuning Availability

Now that you know when to use fine-tuning for your use case, you can go to Microsoft Foundry to find models available to fine-tune.

**To fine-tune a Foundry model using Serverless** you must have a hub/project in the region where the model is available for fine tuning. See [Region availability for models in serverless API deployment](../how-to/deploy-models-serverless-availability.md) for detailed information on model and region availability, and [How to Create a Hub-based project](../how-to/create-projects.md) to create your project.

**To fine-tune an OpenAI model** you can use an Azure OpenAI Resource, a Foundry resource or default project, or a hub/project. GPT 4.1, 4.1-mini, 4.1-nano and GPT 4o, 4omini are available in all regions with Global Training. For regional availability, see [Regional Availability and Limits for Azure OpenAI Fine Tuning](../foundry-models/concepts/models-sold-directly-by-azure.md). See [Create a project for Foundry](../how-to/create-projects.md) for instructions on creating a new project.

**To fine-tune a model using Managed Compute** you must have a hub/project and available VM quota for training and inferencing. See [Fine-tune models using managed compute (preview)](../how-to/fine-tune-managed-compute.md) for more details on how to use managed compute fine tuning, and [How to Create a Hub-based project](../how-to/create-projects.md) to create your project.


## Related content

- [Fine-tune models using managed compute (preview)](../how-to/fine-tune-managed-compute.md)
- [Fine-tune an Azure OpenAI model in Foundry portal](../openai/how-to/fine-tuning.md?context=/azure/ai-studio/context/context)
- [Fine-tune models using serverless API deployment](../how-to/fine-tune-serverless.md)
