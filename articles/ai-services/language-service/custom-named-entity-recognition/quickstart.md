---
title: Quickstart - Custom named entity recognition (NER)
titleSuffix: Azure AI services
description: Quickly start building an AI model to categorize and extract information from unstructured text.
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: quickstart
ms.date: 09/18/2025
ms.author: lajanuar
ms.custom: language-service-custom-ner, mode-other
zone_pivot_groups: foundry-rest-api
---

# Quickstart: Custom named entity recognition

This guide provides step-by-step instructions for using custom named entity recognition (NER) with Azure AI Foundry or the REST API. NER lets you detect and categorize entities in unstructured text—like people, places, organizations, and numbers. With custom NER, you can train models to identify entities specific to your business and adapt them as needs evolve.

To get start, [a sample loan agreement](https://go.microsoft.com/fwlink/?linkid=2175226) is provided as a dataset to build a custom NER model and extract these key entities:

*    Date of the agreement
*    Borrower's name, address, city, and state
*    Lender's name, address, city, and state
*    Loan and interest amounts



::: zone pivot="azure-ai-foundry"

[!INCLUDE [Azure AI Foundry](includes/quickstarts/azure-ai-foundry.md)]

::: zone-end

::: zone pivot="rest-api"

[!INCLUDE [REST API quickstart](includes/quickstarts/rest-api.md)]

::: zone-end

## Related content

After you create your entity extraction model, you can [use the runtime API to extract entities](how-to/call-api.md).

As you create your own custom NER projects, use our how-to articles to learn more about tagging, training, and consuming your model in greater detail:

* [Data selection and schema design](how-to/design-schema.md)
* [Tag data](how-to/tag-data.md)
* [Train a model](how-to/train-model.md)
* [Model evaluation](how-to/view-model-evaluation.md)
