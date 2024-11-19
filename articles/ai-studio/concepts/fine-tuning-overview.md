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

## Getting starting with fine-tuning

When you're deciding whether or not fine-tuning is the right solution for your use case, it's helpful to be familiar with these key terms:

- [Prompt engineering](../../ai-services/openai/concepts/prompt-engineering.md) is a technique that involves designing prompts for natural language processing models. This process improves accuracy and relevancy in responses, to optimize the performance of the model.
- [Retrieval-augmented generation (RAG)](../concepts/retrieval-augmented-generation.md) improves LLM performance by retrieving data from external sources and incorporating it into a prompt. RAG can help businesses achieve customized solutions while maintaining data relevance and optimizing costs.

Fine-tuning is a great way to get higher quality results while reducing latency. The following questions can help you better understand why fine-tuning and evaluate whether you're ready for fine-tuning through the process. You can use these questions to guide your next steps.

### Why do you want to fine-tune a model?

Before you begin fine-tuning a model, consider if you've identified shortcomings when using a base model. These shortcomings can include: an inconsistent performance on edge cases, inability to fit enough prompts in the context window to steer the model, or high latency.

Base models are already pre-trained on vast amounts of data, but most times you will add instructions and examples to the prompt to get the quality responses that you're looking for. This process of "few-shot learning" can be improved with fine-tuning.

Fine-tuning allows you to train a model with many more examples. You can tailor your examples to meet your specific use-case. This can help you reduce the number of tokens in the prompt leading to potential cost savings and requests with lower latency.

Use cases for fine-tuning a model can be:
- Steering the model to output content in a specific and customized style, tone, or format.

If you identify cost as your primary motivator, proceed with caution. Fine-tuning might reduce costs for certain use cases by shortening prompts or allowing you to use a smaller model. But typically there's a higher upfront cost to training, and you have to pay for hosting your own custom model. 

### What isn't working with alternate approaches?

Understanding where prompt engineering falls short should provide guidance on approaching your fine-tuning. Is the base model failing on edge cases or exceptions? Is the base model not consistently providing output in the right format, and you can't fit enough examples in the context window to fix it?

Examples of failure with the base model and prompt engineering can help you identify the data that they need to collect for fine-tuning, and how you should be evaluating your fine-tuned model.

Here's an example: A customer wants to use GPT-3.5 Turbo to turn natural language questions into queries in a specific, nonstandard query language. The customer provides guidance in the prompt ("Always return GQL") and uses RAG to retrieve the database schema. However, the syntax isn't always correct and often fails for edge cases. The customer collects thousands of examples of natural language questions and the equivalent queries for the database, including cases where the model failed before. The customer then uses that data to fine-tune the model. Combining the newly fine-tuned model with the engineered prompt and retrieval brings the accuracy of the model outputs up to acceptable standards for use.

### What have you tried so far?

Fine-tuning is an advanced capability, not the starting point for your generative AI journey. You should already be familiar with the basics of using LLMs. You should start by evaluating the performance of a base model with prompt engineering and/or RAG to get a baseline for performance.

Having a baseline for performance without fine-tuning is essential for knowing whether or not fine-tuning improves model performance. Fine-tuning with bad data makes the base model worse, but without a baseline, it's hard to detect regressions.

Before you begin fine-tuning a model, you need to ensure:

- You can demonstrate evidence and knowledge of using prompt engineering and RAG-based approaches on your LLM.
- You can share specific experiences and challenges with techniques other than fine-tuning that you tried for your use case.
- You have quantitative assessments of baseline performance, whenever possible.
- You have a labeled dataset that corresponds with the specific usecase you want to train your LLM. 

### What data are you going to use for fine-tuning?

Even with a great use case, fine-tuning is only as good as the quality of the data that you can provide. You need to be willing to invest the time and effort to make fine-tuning work. Different models require different data volumes, but you often need to be able to provide fairly large quantities of high-quality curated data. In supervised fine-tuning, a generic moddel is trained on a topic specific labeled dataset. The model with adjust it's parameters to the new data and apply pre-existing knowledge when outputting new content. 

Another important point is that even with high-quality data, if your data isn't in the necessary format for fine-tuning, you need to commit engineering resources for the formatting. 

You might be ready for fine-tuning if:

- You identified a dataset for fine-tuning.
- Your dataset is in the appropriate format for training on your existing model.
- You employed some level of curation to ensure dataset quality.


### How will you measure the quality of your fine-tuned model?

There isn't a single right answer to this question, but you should have clearly defined goals for what success with fine-tuning looks like. Ideally, this effort shouldn't just be qualitative. It should include quantitative measures of success, like using a holdout set of data for validation, in addition to user acceptance testing or A/B testing the fine-tuned model against a base model. 

## Supported models for fine-tuning in Azure AI Studio

Now that you know when to use fine-tuning for your use case, you can go to Azure AI Studio to find models available to fine-tune. The following table describes models that you can fine-tune in Azure AI Studio, along with the regions where you can fine-tune them.

| Model family | Model ID | Fine-tuning regions |
| --- | --- | --- |
| [Azure OpenAI models](../../ai-services/openai/how-to/fine-tuning.md?context=/azure/ai-studio/context/context) | Azure OpenAI Service models that you can fine-tune include among others `gpt-4` and `gpt-4o-mini`.<br/><br/>For details about Azure OpenAI models that are available for fine-tuning, see the [Azure OpenAI Service models documentation](../../ai-services/openai/concepts/models.md#fine-tuning-models) or the [Azure OpenAI models table](#fine-tuning-azure-openai-models) later in this guide. | Azure OpenAI Service models that you can fine-tune include among others North Central US and Sweden Central.<br/><br/>The supported regions might vary if you use Azure OpenAI models in an AI Studio project versus outside a project.<br/><br/>For details about fine-tuning regions, see the [Azure OpenAI Service models documentation](../../ai-services/openai/concepts/models.md#fine-tuning-models). |
| [Phi-3 family models](../how-to/fine-tune-phi-3.md) | `Phi-3-mini-4k-instruct`<br/>`Phi-3-mini-128k-instruct`<br/>`Phi-3-medium-4k-instruct`<br/>`Phi-3-medium-128k-instruct` | East US2 |
| [Meta Llama 2 family models](../how-to/fine-tune-model-llama.md) | `Meta-Llama-2-70b`<br/>`Meta-Llama-2-7b`<br/>`Meta-Llama-2-13b` <br/> `Llama-2-7B-chat` <br> `Llama-2-70B-chat` | West US3 |
| [Meta Llama 3.1 family models](../how-to/fine-tune-model-llama.md) | `Meta-Llama-3.1-70b-Instruct`<br/>`Meta-Llama-3.1-8b-Instruct` | West US3 |

This table provides more details about the Azure OpenAI Service models that support fine-tuning and the regions where fine-tuning is available.

### Fine-tuning Azure OpenAI models

[!INCLUDE [Fine-tune models](../../ai-services/openai/includes/fine-tune-models.md)]

## Related content

- [Fine-tune an Azure OpenAI model in Azure AI Studio](../../ai-services/openai/how-to/fine-tuning.md?context=/azure/ai-studio/context/context)
- [Fine-tune a Llama 2 model in Azure AI Studio](../how-to/fine-tune-model-llama.md)
- [Fine-tune a Phi-3 model in Azure AI Studio](../how-to/fine-tune-phi-3.md)
- [Deploy Phi-3 family of small language models with Azure AI Studio](../how-to/deploy-models-phi-3.md)
