---
title: Fine-tuning in Azure AI Foundry portal
titleSuffix: Azure AI Foundry
description: This article explains what fine-tuning is and under what circumstances you should consider doing it.
manager: scottpolly
ms.service: azure-ai-foundry
ms.custom:
  - build-2024
  - code01
ms.topic: concept-article
ms.date: 02/21/2025
ms.reviewer: keli19
ms.author: sgilley
author: sdgilley
#customer intent: As a developer, I want to learn what it means to fine-tune a model.
---

# Fine-tune models with Azure AI Foundry

Fine-tuning customizes a pretrained AI model with additional training on a specific task or dataset to improve performance, add new skills, or enhance accuracy. The result is a new, optimized GenAI model based on the provided examples.

[!INCLUDE [feature-preview](../includes/feature-preview.md)]

Consider fine-tuning GenAI models to:
- Scale and adapt to specific enterprise needs
- Reduce false positives as tailored models are less likely to produce inaccurate or irrelevant responses
- Enhance the model's accuracy for domain-specific tasks
- Save time and resources with faster and more precise results
- Get more relevant and context-aware outcomes as models are fine-tuned for specific use cases

[Azure AI Foundry](https://ai.azure.com) offers several models across model providers enabling you to get access to the latest and greatest in the market. You can discover supported models for fine-tuning through our model catalog by using the **Fine-tuning tasks** filter and selecting the model card to learn detailed information about each model. Specific models might be subjected to regional constraints. [View this list for more details](#supported-models-for-fine-tuning). 

:::image type="content" source="../media/concepts/model-catalog-fine-tuning.png" alt-text="Screenshot of Azure AI Foundry model catalog and filtering by Fine-tuning tasks." lightbox="../media/concepts/model-catalog-fine-tuning.png":::

This article walks you through use-cases for fine-tuning and how it helps you in your GenAI journey.

## Getting started with fine-tuning

When starting out on your generative AI journey, we recommend you begin with prompt engineering and RAG to familiarize yourself with base models and its capabilities. 
- [Prompt engineering](../../ai-services/openai/concepts/prompt-engineering.md) is a technique that involves designing prompts using tone and style details, example responses, and intent mapping for natural language processing models. This process improves accuracy and relevancy in responses, to optimize the performance of the model.
- [Retrieval-augmented generation (RAG)](../concepts/retrieval-augmented-generation.md) improves LLM performance by retrieving data from external sources and incorporating it into a prompt. RAG can help businesses achieve customized solutions while maintaining data relevance and optimizing costs.

As you get comfortable and begin building your solution, it's important to understand where prompt engineering falls short and when you should try fine-tuning.

- Is the base model failing on edge cases or exceptions? 
- Is the base model not consistently providing output in the right format?
- Is it difficult to fit enough examples in the context window to steer the model?
- Is there high latency?

Examples of failure with the base model and prompt engineering can help you identify the data to collect for fine-tuning and establish a performance baseline that you can evaluate and compare your fine-tuned model against. Having a baseline for performance without fine-tuning is essential for knowing whether or not fine-tuning improves model performance.

Here's an example: 

_A customer wants to use GPT-3.5 Turbo to turn natural language questions into queries in a specific, nonstandard query language. The customer provides guidance in the prompt ("Always return GQL") and uses RAG to retrieve the database schema. However, the syntax isn't always correct and often fails for edge cases. The customer collects thousands of examples of natural language questions and the equivalent queries for the database, including cases where the model failed before. The customer then uses that data to fine-tune the model. Combining the newly fine-tuned model with the engineered prompt and retrieval brings the accuracy of the model outputs up to acceptable standards for use._

### Use cases

Base models are already pretrained on vast amounts of data. Most times you add instructions and examples to the prompt to get the quality responses that you're looking for - this process is called "few-shot learning." Fine-tuning allows you to train a model with many more examples that you can tailor to meet your specific use-case, thus improving on few-shot learning. Fine-tuning can reduce the number of tokens in the prompt leading to potential cost savings and requests with lower latency. 

Turning natural language into a query language is just one use case where you can  "_show not tell_" the model how to behave. Here are some other use cases:

- Improve the model's handling of retrieved data
- Steer model to output content in a specific style, tone, or format
- Improve the accuracy when you look up information
- Reduce the length of your prompt
- Teach new skills (that is, natural language to code)

If you identify cost as your primary motivator, proceed with caution. Fine-tuning might reduce costs for certain use cases by shortening prompts or allowing you to use a smaller model. But there might be a higher upfront cost to training, and you have to pay for hosting your own custom model. 

### Steps to fine-tune a model

Here are the general steps to fine-tune a model:

1. Choose a model that supports your task.
1. Prepare and upload training data.
1. (Optional) Prepare and upload validation data.
1. (Optional) Configure task parameters.
1. Train your model. 
1. Once completed, review metrics and evaluate model. If the results don't meet your benchmark, then go back to step 2.
1. Use your fine-tuned model.

It's important to call out that fine-tuning is heavily dependent on the quality of data that you can provide. It's best practice to provide hundreds, if not thousands, of training examples to be successful and get your desired results.

## Supported models for fine-tuning

Now that you know when to use fine-tuning for your use case, you can go to Azure AI Foundry to find models available to fine-tune.
For some models in the model catalog, fine-tuning is available by using a standard deployment, or a managed compute (preview), or both.

Fine-tuning is available in specific Azure regions for some models that are deployed via standard deployments. To fine-tune such models, a user must have a hub/project in the region where the model is available for fine-tuning. See [Region availability for models in standard deployment](../how-to/deploy-models-serverless-availability.md) for detailed information.

For more information on fine-tuning using a managed compute (preview), see [Fine-tune models using managed compute (preview)](../how-to/fine-tune-managed-compute.md).

For details about Azure OpenAI in Azure AI Foundry Models that are available for fine-tuning, see the [Azure OpenAI in Foundry Models documentation](../../ai-services/openai/concepts/models.md#fine-tuning-models) or the [Azure OpenAI models table](#fine-tuning-azure-openai-models) later in this guide.

For the Azure OpenAI Service models that you can fine tune, supported regions for fine-tuning include North Central US, Sweden Central, and more.

### Fine-tuning Azure OpenAI models

[!INCLUDE [Fine-tune models](../../ai-services/openai/includes/fine-tune-models.md)]

## Related content

- [Fine-tune models using managed compute (preview)](../how-to/fine-tune-managed-compute.md)
- [Fine-tune an Azure OpenAI model in Azure AI Foundry portal](../../ai-services/openai/how-to/fine-tuning.md?context=/azure/ai-studio/context/context)
- [Fine-tune models using standard deployment](../how-to/fine-tune-serverless.md)

