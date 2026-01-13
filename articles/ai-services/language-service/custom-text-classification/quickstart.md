---
title: Quickstart - Custom text classification
titleSuffix: Foundry Tools
description: Quickly start building an AI model to identify and apply labels (classify) unstructured text.
#services: cognitive-services
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: quickstart
ms.date: 12/15/2025
ms.author: lajanuar
ms.custom: language-service-custom-classification, mode-other
---
# Quickstart: Custom text classification REST API

Use this article to get started with creating a custom text classification project where you can train custom models for text classification. A model is AI software trained to do a certain task. For this system, the models classify text, and are trained by learning from tagged data.

Custom text classification supports two types of projects: 

* **Single label classification** - you can assign a single class for each document in your dataset. For example, a movie script could only be classified as "Romance" or "Comedy." 
* **Multi label classification** - you can assign multiple classes for each document in your dataset. For example, a movie script could be classified as "Comedy" or "Romance" and "Comedy."

In this quickstart, you can use the sample datasets provided to build a multi label classification to classify movie scripts into one or more categories. Alternatively, you can use single label classification dataset to classify abstracts of scientific papers into one of the defined domains.


[!INCLUDE [REST API quickstart](includes/quickstarts/rest-api.md)]

## Next steps

After you create a custom text classification model, you can:
* [Use the runtime API to classify text](how-to/call-api.md)

When you start to create your own custom text classification projects, use the how-to articles to learn more about developing your model in greater detail:

* [Data selection and schema design](how-to/design-schema.md)
* [Tag data](how-to/tag-data.md)
* [Train a model](how-to/train-model.md)
* [View model evaluation](how-to/view-model-evaluation.md)
