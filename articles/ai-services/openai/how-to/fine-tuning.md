---
title: 'Customize a model with Azure OpenAI in Azure AI Foundry Models'
titleSuffix: Azure OpenAI
description: Learn how to create your own customized model with Azure OpenAI by using Python, the REST APIs, or Azure AI Foundry portal.
manager: nitinme
ms.service: azure-ai-openai
ms.custom: build-2023, build-2023-dataai, devx-track-python, references_regions
ms.topic: how-to
ms.date: 03/27/2025
author: mrbullwinkle
ms.author: mbullwin
zone_pivot_groups: openai-fine-tuning
---

# Customize a model with fine-tuning

Azure OpenAI in Azure AI Foundry Models lets you tailor our models to your personal datasets by using a process known as *fine-tuning*. This customization step lets you get more out of the service by providing:

- Higher quality results than what you can get just from [prompt engineering](../concepts/prompt-engineering.md)
- The ability to train on more examples than can fit into a model's max request context limit.
- Token savings due to shorter prompts
- Lower-latency requests, particularly when using smaller models.

In contrast to few-shot learning, fine tuning improves the model by training on many more examples than can fit in a prompt, letting you achieve better results on a wide number of tasks. Because fine tuning adjusts the base model’s weights to improve performance on the specific task, you won’t have to include as many examples or instructions in your prompt. This means less text sent and fewer tokens processed on every API call, potentially saving cost, and improving request latency.

We use LoRA, or low rank adaptation, to fine-tune models in a way that reduces their complexity without significantly affecting their performance. This method works by approximating the original high-rank matrix with a lower rank one, thus only fine-tuning a smaller subset of *important* parameters during the supervised training phase, making the model more manageable and efficient. For users, this makes training faster and more affordable than other techniques.

::: zone pivot="programming-language-studio"

[!INCLUDE [Azure AI Foundry portal fine-tuning](../includes/fine-tuning-unified.md)]

::: zone-end

::: zone pivot="programming-language-python"

[!INCLUDE [Python SDK fine-tuning](../includes/fine-tuning-python.md)]

::: zone-end

::: zone pivot="rest-api"

[!INCLUDE [REST API fine-tuning](../includes/fine-tuning-rest.md)]

::: zone-end

## Next steps

- Explore the fine-tuning capabilities in the [Azure OpenAI fine-tuning tutorial](../tutorials/fine-tune.md).
- Review fine-tuning [model regional availability](../concepts/models.md#fine-tuning-models)
- Learn more about [Azure OpenAI quotas](../quotas-limits.md)
