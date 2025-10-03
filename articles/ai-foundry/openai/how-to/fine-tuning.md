---
title: 'Customize a model with Azure OpenAI in Azure AI Foundry Models'
titleSuffix: Azure OpenAI
description: Learn how to fine-tune and customize Azure OpenAI models using Python, REST APIs, or Azure AI Foundry portal. Improve model performance with LoRA adaptation and custom datasets.
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.custom: build-2023, build-2023-dataai, devx-track-python, references_regions
ms.topic: how-to
ms.date: 09/30/2025
author: mrbullwinkle
ms.author: mbullwin
zone_pivot_groups: openai-fine-tuning
ai-usage: ai-assisted
---

# Customize a model with fine-tuning

Learn how to fine-tune Azure OpenAI models in Azure AI Foundry for your datasets and use cases. Fine-tuning enables:

- Higher quality results than what you can get just from [prompt engineering](../concepts/prompt-engineering.md)
- The ability to train on more examples than can fit into a model's max request context limit.
- Token savings due to shorter prompts
- Lower-latency requests, particularly when using smaller models.

In contrast to few-shot learning, fine-tuning improves the model by training on more examples than fit in a prompt. Because weights adapt to your task, you include fewer examples or instructions, reducing tokens per call and potentially lowering cost and latency.

We use LoRA, or low rank adaptation, to fine-tune models in a way that reduces their complexity without significantly affecting their performance. This method works by approximating the original high-rank matrix with a lower rank one, thus only fine-tuning a smaller subset of *important* parameters during the supervised training phase, making the model more manageable and efficient. For users, this makes training faster and more affordable than other techniques.

In this article, you learn how to:

- Fine-tune via portal, Python SDK, and REST.
- Choose appropriate datasets and formats.
- Monitor job status and fetch results.
- Deploy and evaluate a tuned model.
- Iterate based on evaluation feedback.

::: zone pivot="programming-language-studio"

[!INCLUDE [Azure AI Foundry portal fine-tuning](../includes/fine-tuning-unified.md)]

::: zone-end

::: zone pivot="programming-language-python"

[!INCLUDE [Python SDK fine-tuning](../includes/fine-tuning-python.md)]

::: zone-end

::: zone pivot="rest-api"

[!INCLUDE [REST API fine-tuning](../includes/fine-tuning-rest.md)]

::: zone-end

## Related content

- [Fine-tuning tutorial (step-by-step)](../tutorials/fine-tune.md)
- [Model catalog & regional availability](../concepts/models.md)
- [Quotas and limits](../quotas-limits.md)
- [View and interpret evaluation results](../../how-to/evaluate-results.md)
- [Trace AI application usage (OpenAI SDK)](../../how-to/develop/trace-application.md)
