---
title: Quickstart - Custom named entity recognition (NER)
titleSuffix: Azure AI services
description: Quickly start building an AI model to categorize and extract information from unstructured text.
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: quickstart
ms.date: 07/22/2025
ms.author: lajanuar
ms.custom: language-service-custom-ner, mode-other
zone_pivot_groups: usage-custom-language-features
---

# Quickstart: Custom named entity recognition

Use this article to get started with creating a custom NER project where you can train custom models for custom entity recognition. A model artificial intelligence software trained to achieve a specific task. For this system, the models extract named entities and are trained by learning from tagged data.

In this article, we use Language Studio to demonstrate key concepts of custom Named Entity Recognition (NER). As an example, let's build a custom NER model to extract the following relevant entities from loan agreements:

* Date of the agreement
* Borrower's name, address, city, and state
* Lender's name, address, city, and state
* Loan and interest amounts

::: zone pivot="language-studio"

[!INCLUDE [Language Studio quickstart](includes/quickstarts/language-studio.md)]

::: zone-end

::: zone pivot="rest-api"

[!INCLUDE [REST API quickstart](includes/quickstarts/rest-api.md)]

::: zone-end

## Next steps

After you create your entity extraction model, you can [use the runtime API to extract entities](how-to/call-api.md).

As you create your own custom NER projects, use our how-to articles to learn more about tagging, training, and consuming your model in greater detail:

* [Data selection and schema design](how-to/design-schema.md)
* [Tag data](how-to/tag-data.md)
* [Train a model](how-to/train-model.md)
* [Model evaluation](how-to/view-model-evaluation.md)
