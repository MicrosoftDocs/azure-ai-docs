---
title: 'Customize a Model with Microsoft Foundry Fine-Tuning'
titleSuffix: Azure OpenAI
description: Learn how to fine-tune and customize Foundry models by using Python, REST APIs, or the Microsoft Foundry portal. Improve model performance with LoRA adaptation and custom datasets.
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.custom: build-2023, build-2023-dataai, devx-track-python, references_regions
ms.topic: how-to
ms.date: 12/01/2025
author: mrbullwinkle
ms.author: mbullwin
zone_pivot_groups: openai-fine-tuning
monikerRange: 'foundry-classic || foundry'
ai-usage: ai-assisted
---

# Customize a model with fine-tuning

Learn how to fine-tune models in Microsoft Foundry for your datasets and use cases. Fine-tuning enables:

- Higher-quality results than what you can get just from [prompt engineering](../concepts/prompt-engineering.md).
- The ability to train on more examples than what can fit into a model's request context limit.
- Token savings due to shorter prompts.
- Lower-latency requests, particularly when you're using smaller models.

In contrast to few-shot learning, fine-tuning improves the model by training on more examples than what fits in a prompt. Because weights adapt to your task, you include fewer examples or instructions. Including less reduces tokens per call and potentially lowers cost and latency.

We use low-rank adaptation (LoRA) to fine-tune models in a way that reduces their complexity without significantly affecting their performance. This method works by approximating the original high-rank matrix with a lower-rank one. Fine-tuning a smaller subset of important parameters during the supervised training phase makes the model more manageable and efficient. For users, it also makes training faster and more affordable than other techniques.

In this article, you learn how to:

- Choose appropriate datasets and formats for fine-tuning.
- Trigger a fine-tuning job, monitor the status, and fetch results.
- Deploy and evaluate a fine-tuned model.
- Iterate based on evaluation feedback.

::: moniker range="foundry"

::: zone pivot="programming-language-studio"

[!INCLUDE [Microsoft Foundry portal fine-tuning](../../includes/fine-tuning-foundry.md)]

::: zone-end

::: zone pivot="programming-language-python"

# [OpenAI SDK](#tab/oai-sdk)

[!INCLUDE [Microsoft Foundry fine-tuning OAI SDK](../includes/fine-tuning-oai-sdk.md)]

# [Foundry SDK](#tab/foundry-sdk)

[!INCLUDE [Microsoft Foundry fine-tuning Foundry SDK](../includes/fine-tuning-foundry-sdk.md)]

::: zone-end

::: zone pivot="rest-api"

[!INCLUDE [REST API fine-tuning](../includes/fine-tuning-rest.md)]

::: zone-end

::: moniker-end

::: moniker range="foundry-classic"

::: zone pivot="programming-language-studio"

[!INCLUDE [Microsoft Foundry portal fine-tuning](../includes/fine-tuning-unified.md)]

::: zone-end

::: zone pivot="programming-language-python"

[!INCLUDE [Python SDK fine-tuning](../includes/fine-tuning-oai-sdk.md)]

::: zone-end

::: zone pivot="rest-api"

[!INCLUDE [REST API fine-tuning](../includes/fine-tuning-rest.md)]

::: zone-end

::: moniker-end

## Related content

- [Fine-tuning tutorial (step-by-step)](../tutorials/fine-tune.md)
- [Model catalog and regional availability](../../foundry-models/concepts/models-sold-directly-by-azure.md)
- [Quotas and limits](../quotas-limits.md)
- [View and interpret evaluation results](../../how-to/evaluate-results.md)
- [Trace AI application usage (OpenAI SDK)](../../how-to/develop/trace-application.md)
