---
title: Quickstart - Custom Text Analytics for health (Custom TA4H)
titleSuffix: Azure AI services
description: Quickly start building an AI model to categorize and extract information from healthcare unstructured text.
#services: cognitive-services
author: jboback
manager: nitinme
ms.service: azure-ai-language
ms.topic: quickstart
ms.date: 11/21/2024
ms.author: jboback
ms.custom: language-service-custom-TA4H, mode-other
zone_pivot_groups: usage-custom-language-features
---

# Quickstart: custom Text Analytics for health

> [!NOTE]
> Custom text analytics for health (preview) will be retired on 10 January 2025, please transition to other custom model training services, such as custom named entity recognition in Azure AI Language, by that date. From now to 10 January 2025, you can continue to use custom text analytics for health (preview) in your existing projects without disruption. You can’t create new projects. On 10 January 2025 – workloads running on custom text analytics for health (preview) will be deleted and associated project data will be lost.

Use this article to get started with creating a custom Text Analytics for health project where you can train custom models on top of Text Analytics for health for custom entity recognition. A model is artificial intelligence software that's trained to do a certain task. For this system, the models extract healthcare related named entities and are trained by learning from labeled data.

In this article, we use Language Studio to demonstrate key concepts of custom Text Analytics for health. As an example we’ll build a custom Text Analytics for health model to extract the Facility or treatment location from short discharge notes.

::: zone pivot="language-studio"

[!INCLUDE [Language Studio quickstart](includes/quickstarts/language-studio.md)]

::: zone-end

::: zone pivot="rest-api"

[!INCLUDE [REST API quickstart](includes/quickstarts/rest-api.md)]

::: zone-end

## Next steps

* [Text analytics for health overview](./overview.md)

After you've created entity extraction model, you can:

* [Use the runtime API to extract entities](how-to/call-api.md)

When you start to create your own custom Text Analytics for health projects, use the how-to articles to learn more about data labeling, training and consuming your model in greater detail:

* [Data selection and schema design](how-to/design-schema.md)
* [Tag data](how-to/label-data.md)
* [Train a model](how-to/train-model.md)
* [Model evaluation](how-to/view-model-evaluation.md)
