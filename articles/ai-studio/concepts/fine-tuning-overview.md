---
title: Fine-tuning in Azure AI Studio
titleSuffix: Azure AI Studio
description: This article introduces fine-tuning of models in Azure AI Studio.
manager: scottpolly
ms.service: azure-ai-studio
ms.custom:
  - build-2024
  - code01
ms.topic: conceptual
ms.date: 10/31/2024
ms.reviewer: sgilley
ms.author: sgilley
author: sdgilley
---

# Fine-tune models with Azure AI Foundry

[!INCLUDE [feature-preview](../includes/feature-preview.md)]

Fine-tuning refers to customizing a pre-trained generative AI model with additional training on a specific task or new dataset for enhanced performance, new skills, or improved accuracy. The result is a new, custom GenAI model that's optimized based on the provided examples.

Consider fine-tuning GenAI models to:
- Scale and adapt to specific enterprise needs
- Reduce hallucinations as tailored models are less likely to produce inaccurate or irrelevant responses
- Enhance the model's accuracy for domain-specific tasks
- Save time and resources with faster and more precise results
- Get more relevant and context-aware outcomes as models are fine-tuned for specific use cases

[Azure AI Foundry](https://ai.azure.com) offers several models across model providers enabling you to get access to the latest and greatest in the market. You can discover supported models for fine-tuning through our model catalog by using the **Fine-tuning tasks** filter and clicking into the model card to learn detailed information about each model. Specific models may be subjected to regional constraints, [view this list for more details](#supported-models-for-fine-tuning). 

:::image type="content" source="../media/concepts/model-catalog-fine-tuning.png" alt-text="Screenshot of Azure AI Foundry model catalog and filtering by Fine-tuning tasks." lightbox="../media/concepts/model-catalog-fine-tuning.png":::

This article will walk you through use-cases for fine-tuning and how this can help you in your GenAI journey.

## Getting started with fine-tuning

When starting out on your generative AI journey, we recommend you begin with prompt engineering and RAG to familiarize yourself with base models and its capabilities. 
- [Prompt engineering](../../ai-services/openai/concepts/prompt-engineering.md) is a technique that involves designing prompts using tone and style details, example responses, and intent mapping for natural language processing models. This process improves accuracy and relevancy in responses, to optimize the performance of the model.
- [Retrieval-augmented generation (RAG)](../concepts/retrieval-augmented-generation.md) improves LLM performance by retrieving data from external sources and incorporating it into a prompt. RAG can help businesses achieve customized solutions while maintaining data relevance and optimizing costs.

As you get comfortable and begin building your solution, it is important to understand where prompt engineering falls short and that'll help you realize if you should try fine-tuning. 
- Is the base model failing on edge cases or exceptions? 
- Is the base model not consistently providing output in the right format?
- Is it difficult to fit enough examples in the context window to steer the model?
- Is there high latency?

Examples of failure with the base model and prompt engineering can help you identify the data to collect for fine-tuning and establish a performance baseline that you can evaluate and compare your fine-tuned model against. Having a baseline for performance without fine-tuning is essential for knowing whether or not fine-tuning improves model performance.

Here's an example: 

_A customer wants to use GPT-3.5 Turbo to turn natural language questions into queries in a specific, nonstandard query language. The customer provides guidance in the prompt ("Always return GQL") and uses RAG to retrieve the database schema. However, the syntax isn't always correct and often fails for edge cases. The customer collects thousands of examples of natural language questions and the equivalent queries for the database, including cases where the model failed before. The customer then uses that data to fine-tune the model. Combining the newly fine-tuned model with the engineered prompt and retrieval brings the accuracy of the model outputs up to acceptable standards for use._

### Use cases

Base models are already pre-trained on vast amounts of data and most times you will add instructions and examples to the prompt to get the quality responses that you're looking for - this process is called "few-shot learning". Fine-tuning allows you to train a model with many more examples that you can tailor to meet your specific use-case, thus improving on few-shot learning. This can reduce the number of tokens in the prompt leading to potential cost savings and requests with lower latency. 

Turning natural language into a query language is just one use case where you can  _show not tell_ the model how to behave. Here are some additional use cases:
- Improve the model's handling of retrieved data
- Steer model to output content in a specific style, tone, or format
- Improve the accuracy when you look up information
- Reduce the length of your prompt
- Teach new skills (i.e. natural language to code)

If you identify cost as your primary motivator, proceed with caution. Fine-tuning might reduce costs for certain use cases by shortening prompts or allowing you to use a smaller model. But there may be a higher upfront cost to training, and you have to pay for hosting your own custom model. 

### Steps to fine-tune a model
Here are the general steps to fine-tune a model:
1. Based on your use case, choose a model that supports your task
2. Prepare and upload training data
3. (Optional) Prepare and upload validation data
4. (Optional) Configure task parameters
5. Train your model. 
6. Once completed, review metrics and evaluate model. If the results don't meet your benchmark, then go back to step 2.
7. Use your fine-tuned model

It's important to call out that fine-tuning is heavily dependent on the quality of data that you can provide. It is best practice to provide hundreds, if not thousands, of training examples to be successful and get your desired results.

## Supported models for fine-tuning

Now that you know when to use fine-tuning for your use case, you can go to Azure AI Foundry to find models available to fine-tune. The following table describes models that you can fine-tune in Azure AI Foundry, along with the regions where you can fine-tune them.

| Model family | Model ID | Fine-tuning regions |
| --- | --- | --- |
| [Azure OpenAI models](../../ai-services/openai/how-to/fine-tuning.md?context=/azure/ai-studio/context/context) | Azure OpenAI Service models that you can fine-tune include among others `gpt-4` and `gpt-4o-mini`.<br/><br/>For details about Azure OpenAI models that are available for fine-tuning, see the [Azure OpenAI Service models documentation](../../ai-services/openai/concepts/models.md#fine-tuning-models) or the [Azure OpenAI models table](#fine-tuning-azure-openai-models) later in this guide. | Azure OpenAI Service models that you can fine-tune include among others North Central US and Sweden Central.<br/><br/>The supported regions might vary if you use Azure OpenAI models in an AI Studio project versus outside a project.<br/><br/>For details about fine-tuning regions, see the [Azure OpenAI Service models documentation](../../ai-services/openai/concepts/models.md#fine-tuning-models). |
| [Phi-3 family models](../how-to/fine-tune-phi-3.md)<sup>**1**</sup>| `Phi-3-mini-4k-instruct`<br/>`Phi-3-mini-128k-instruct`<br/>`Phi-3-medium-4k-instruct`<br/>`Phi-3-medium-128k-instruct` | East US2 |
| [Meta Llama 2 family models](../how-to/fine-tune-model-llama.md)<sup>**1**</sup>| `Meta-Llama-2-70b`<br/>`Meta-Llama-2-7b`<br/>`Meta-Llama-2-13b` <br/> `Llama-2-7B-chat` <br> `Llama-2-70B-chat` | West US3 |
| [Meta Llama 3.1 family models](../how-to/fine-tune-model-llama.md)<sup>**1**</sup>| `Meta-Llama-3.1-70b-Instruct`<br/>`Meta-Llama-3.1-8b-Instruct` | West US3 |

**<sup>1</sup>** Fine-tuning of these models is currently in public preview.

This table provides more details about the Azure OpenAI Service models that support fine-tuning and the regions where fine-tuning is available.

### Fine-tuning Azure OpenAI models

[!INCLUDE [Fine-tune models](../../ai-services/openai/includes/fine-tune-models.md)]

## Related content

- [Fine-tune an Azure OpenAI model in Azure AI Studio](../../ai-services/openai/how-to/fine-tuning.md?context=/azure/ai-studio/context/context)
- [Fine-tune a Llama 2 model in Azure AI Studio](../how-to/fine-tune-model-llama.md)
- [Fine-tune a Phi-3 model in Azure AI Studio](../how-to/fine-tune-phi-3.md)
- [Deploy Phi-3 family of small language models with Azure AI Studio](../how-to/deploy-models-phi-3.md)
