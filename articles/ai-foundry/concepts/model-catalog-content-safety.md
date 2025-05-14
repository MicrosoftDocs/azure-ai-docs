---
title: Guardrails & controls for Models Sold Directly by Azure 
titleSuffix: Azure AI Foundry
description: Learn about content safety for models deployed using standard deployments, using Azure AI Foundry.
manager: scottpolly
ms.service: azure-ai-foundry
ms.topic: conceptual
ms.date: 02/04/2025
ms.author: mopeakande 
author: msakande
ms.reviewer: ositanachi
reviewer: ositanachi
ms.custom: 
---

# Guardrails & controls for Models Sold Directly by Azure 

[!INCLUDE [feature-preview](../includes/feature-preview.md)]

In this article, learn about content safety capabilities for models from the model catalog deployed using standard deployments.


## Content filter defaults

Azure AI uses a default configuration of [Azure AI Content Safety](/azure/ai-services/content-safety/overview) content filters to detect harmful content across four categories including hate and fairness, self-harm, sexual, and violence for models deployed via standard deployments. To learn more about content filtering, see [Understand harm categories](#understand-harm-categories).

The default content filtering configuration for text models is set to filter at the medium severity threshold, filtering any detected content at this level or higher. For image models, the default content filtering configuration is set at the low configuration threshold, filtering at this level or higher. For models deployed using the [Azure AI Foundry Models](../../ai-foundry/model-inference/how-to/configure-content-filters.md), you can create configurable filters by selecting the **Content filters** tab within the **Guardrails & controls** page of the Azure AI Foundry portal.

> [!TIP]
> Content filtering isn't available for certain model types that are deployed via standard deployments. These model types include embedding models and time series models.

Content filtering occurs synchronously as the service processes prompts to generate content. You might be billed separately according to [Azure AI Content Safety pricing](https://azure.microsoft.com/pricing/details/cognitive-services/content-safety/) for such use. You can disable content filtering for individual serverless endpoints either:

- When you first deploy a language model
- Later, by selecting the content filtering toggle on the deployment details page

Suppose you decide to use an API other than the [Foundry Models API](/azure/ai-studio/reference/reference-model-inference-api) to work with a model that is deployed via a standard deployment. In such a situation, content filtering (preview) isn't enabled unless you implement it separately by using Azure AI Content Safety. To get started with Azure AI Content Safety, see [Quickstart: Analyze text content](/azure/ai-services/content-safety/quickstart-text). You run a higher risk of exposing users to harmful content if you don't use content filtering (preview) when working with models that are deployed via standard deployments.

[!INCLUDE [content-safety-harm-categories](../includes/content-safety-harm-categories.md)]

## How charges are calculated

Pricing details are viewable at [Azure AI Content Safety pricing](https://azure.microsoft.com/pricing/details/cognitive-services/content-safety/). Charges are incurred when the Azure AI Content Safety validates the prompt or completion. If Azure AI Content Safety blocks the prompt or completion, you're charged for both the evaluation of the content and the inference calls.

## Related content

- [How to configure content filters for models in Azure AI services](../../ai-foundry/model-inference/how-to/configure-content-filters.md)
- [What is Azure AI Content Safety?](../../ai-services/content-safety/overview.md)
- [Model catalog and collections in Azure AI Foundry portal](../how-to/model-catalog-overview.md)
