---
title: Quickstart - Custom sentiment analysis
titleSuffix: Azure AI services
description: Quickly start building an AI model to identify the sentiment of text.
#services: cognitive-services
author: jboback
manager: nitinme
ms.service: azure-ai-language
ms.topic: quickstart
ms.date: 11/21/2024
ms.author: jboback
ms.custom: language-service-sentiment-opinion-mining
zone_pivot_groups: usage-custom-language-features
---

# Quickstart: Custom sentiment analysis (preview)

> [NOTE]
> Custom sentiment analysis (preview) will be retired on 10 January 2025, please transition to other custom model training services, such as custom text classification in Azure AI Language, by that date. From now to 10 January 2025, you can continue to use custom sentiment analysis (preview) in your existing projects without disruption. You can’t create new projects. On 10 January 2025 – workloads running on custom sentiment analysis (preview) will be deleted and associated project data will be lost. 

Use this article to get started with creating a Custom sentiment analysis project where you can train custom models for detecting the sentiment of text. A model is artificial intelligence software that's trained to do a certain task. For this system, the models classify text, and are trained by learning from tagged data.

::: zone pivot="language-studio"

[!INCLUDE [Language Studio quickstart](../includes/custom/quickstarts/language-studio.md)]

::: zone-end

::: zone pivot="rest-api"

[!INCLUDE [REST API quickstart](../includes/custom/quickstarts/rest-api.md)]

::: zone-end

## Next steps

After you've created a Custom sentiment analysis model, you can:
* [Use the runtime API to classify text](how-to/call-api.md)

When you start to create your own Custom sentiment analysis projects, use the how-to articles to learn more about developing your model in greater detail:

* [Data selection](how-to/design-schema.md)
* [Tag data](how-to/label-data.md)
* [Train a model](how-to/train-model.md)
<!--* [View the model's evaluation](how-to/view-model-evaluation.md)-->