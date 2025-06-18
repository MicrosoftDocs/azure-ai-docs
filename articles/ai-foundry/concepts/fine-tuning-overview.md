---
title: Fine-tune models with Azure AI Foundry
titleSuffix: Azure AI Foundry
description: This article explains what fine-tuning is and under what circumstances you should consider doing it.
manager: scottpolly
ms.service: azure-ai-foundry
ms.custom:
  - build-2024
  - code01
ms.topic: concept-article
ms.date: 05/14/2025
ms.reviewer: keli19
ms.author: sgilley
author: sdgilley
#customer intent: As a developer, I want to learn what it means to fine-tune a model.
---

# Fine-tune models with Azure AI Foundry

Fine-tuning customizes a pretrained AI model with additional training on a specific task or dataset to improve performance, add new skills, or enhance accuracy. The result is a new, optimized GenAI model based on the provided examples. This article walks you through use-cases for fine-tuning and how it helps you in your GenAI journey.

If you're just getting started with fine-tuning, we recommend **GPT-4.1** for complex skills like language translation, domain adaptation, or advanced code generation. For more focused tasks (such as classification, sentiment analysis, or content moderation) or when distilling knowledge from a more sophisticated model, start with **GPT-4.1-mini** for faster iteration and lower costs.

:::image type="content" source="../media/concepts/model-catalog-fine-tuning.png" alt-text="Screenshot of Azure AI Foundry model catalog and filtering by Fine-tuning tasks." lightbox="../media/concepts/model-catalog-fine-tuning.png":::

## Serverless or Managed Compute?

- **Serverless** lets you customize models using our capacity with consumption-based pricing starting at $1.70 per million input tokens. We optimize training for speed and scalability while handling all infrastructure management. This approach requires no GPU quotas and provides exclusive access to OpenAI models, though with fewer hyperparameter options than managed compute.
- **Managed compute** offers a wider range of models and advanced customization through AzureML, but requires you to provide your own VMs for training and hosting. While this gives full control over resources, it demands high quotas that many customers lack, doesn't include OpenAI models, and can't leverage our multi-tenancy optimizations.

For most customers, serverless provides the best balance of ease-of-use, cost efficiency, and access to premium models. This document focuses on serverless options.

To find steps to fine-tuning a model in AI Foundry, see [Fine-tune Models in AI Foundry](../how-to/fine-tune-serverless.md) or [Fine-tune models using managed compute](how-to/fine-tune-managed-compute.md).

## Training Techniques

We offer three training techniques to optimize your models:
- **Supervised Fine Tuning (SFT):** Foundational technique that trains your model on input-output pairs, teaching it to produce desired responses for specific inputs.
  - *Best for:* Most use cases including classification, generation, and task-specific adaptation.
  - *When to use:* Start here for most projects. SFT addresses the broadest number of fine-tuning scenarios and provides reliable results with clear input-output training data.
  - *Supported Models:* GPT 4o, 4o-mini, 4.1, 4.1-mini, 4.1-nano; Llama 2 and Llama 3.1; Phi 4, Phi-4-mini-instruct; Mistral Nemo, Ministral-3B, Mistral Large (2411); NTT Tsuzumi-7b

- **Direct Preference Optimization (DPO):** Trains models to prefer certain types of responses over others by learning from comparative feedback, without requiring a separate reward model.
  - *Best for:* Improving response quality, safety, and alignment with human preferences.
  - *When to use:* When you have examples of preferred vs. non-preferred outputs, or when you need to optimize for subjective qualities like helpfulness, harmlessness, or style.
  - *Supported Models:* GPT 4o, 4.1, 4.1-mini, 4.1-nano

- **Reinforcement Fine Tuning (RFT):** Uses reinforcement learning to optimize models based on reward signals, allowing for more complex optimization objectives.
  - *Best for:* Complex optimization scenarios where simple input-output pairs aren't sufficient.
  - *When to use:* Advanced use cases requiring optimization for metrics like user engagement, task completion rates, or other measurable outcomes. Requires more ML expertise to implement effectively.
  - *Supported Models:* o4-mini

> Most customers should start with SFT, as it addresses the broadest number of fine-tuning use cases.

Follow this link to view and download [example datasets](https://github.com/Azure-Samples/AIFoundry-Customization-Datasets) to try out fine-tuning.

## Training Modalities

- **Text-to-Text (All Models):** All our models support standard text-to-text fine-tuning for language-based tasks.
- **Vision + Text (GPT 4o, 4.1):** Some models support vision fine-tuning, accepting both image and text inputs while producing text outputs. Use cases for vision fine-tuning include interpreting charts, graphs, and visual data; content moderation; visual quality assessment; document processing with mixed text and image; and product cataloging from photographs.

## Model Comparison Table

| Model                | Modalities     | Techniques   | Strengths                        |
|----------------------|---------------|--------------|--------------------------------------|
| GPT 4.1              | Text, Vision  | SFT, DPO     | Superior performance on sophisticated tasks, nuanced understanding |
| GPT 4.1-mini         | Text          | SFT, DPO     | Fast iteration, cost-effective, good for simple tasks  |
| GPT 4.1-nano         | Text          | SFT, DPO     | Extremely fast and cheap, minimal resource usage        |
| o4-mini              | Text          | RFT          | Reasoning model suited for complex logical tasks        |
| Phi 4                | Text          | SFT          | Cost effective option for simpler tasks                |
| Ministral 3B         | Text          | SFT          | Low-cost option for faster iteration                   |
| Mistral Nemo         | Text          | SFT          | Balance between size and capability                    |
| Mistral Large (2411) | Text          | SFT          | Most capable Mistral model, better for complex tasks   |

## Model selection

1. **Define your use case:** Identify whether you need a highly capable general-purpose model (e.g. GPT 4.1), a smaller cost-effective model for a specific task (GPT 4.1-mini or nano), or a complex reasoning model (o4-mini).
2. **Prepare your data:** Start with 50-100 high-quality examples for initial testing, scaling to 500+ examples for production models.
3. **Choose your technique:** Begin with Supervised Fine Tuning (SFT) unless you have specific requirements for reasoning models / RFT.
4. **Iterate and evaluate:** Fine-tuning is an iterative process—start with a baseline, measure performance, and refine your approach based on results.

For additional guidance on data preparation, evaluation strategies, and advanced techniques, see the main documentation page.

## Supported models for fine-tuning

Now that you know when to use fine-tuning for your use case, you can go to Azure AI Foundry to find models available to fine-tune.

Fine-tuning is available in specific Azure regions for some models that are deployed via standard deployments. To fine-tune such models, a user must have a hub/project in the region where the model is available for fine-tuning. See [Region availability for models in standard deployment](../how-to/deploy-models-serverless-availability.md) for detailed information.

For more information on fine-tuning using a managed compute (preview), see [Fine-tune models using managed compute (preview)](../how-to/fine-tune-managed-compute.md).

For details about Azure OpenAI in Azure AI Foundry Models that are available for fine-tuning, see the [Azure OpenAI in Foundry Models documentation.](../../ai-services/openai/concepts/models.md#fine-tuning-models)

## Related content

- [Fine-tune models using managed compute (preview)](../how-to/fine-tune-managed-compute.md)
- [Fine-tune an Azure OpenAI model in Azure AI Foundry portal](../../ai-services/openai/how-to/fine-tuning.md?context=/azure/ai-studio/context/context)
- [Fine-tune models using standard deployment](../how-to/fine-tune-serverless.md)
