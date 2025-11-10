---
title: Regional support for Azure AI Language
titleSuffix: Azure AI services
description: Learn which Azure regions support by the Language service features and capabilities.
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: conceptual
ms.date: 09/17/2025
ms.author: lajanuar
ms.custom: references_regions
---

# Language service supported regions

The Language service is available for use in several Azure regions. Use this article to learn about the regional support and limitations.

## Region support overview

Typically you can refer to the [region support](https://azure.microsoft.com/explore/global-infrastructure/products-by-region/?products=cognitive-services) for details, and most Language service capabilities are available in all supported regions. Some Language service capabilities, however, are only available in select regions.

> [!NOTE]
> Language service doesn't store or process customer data outside the region you deploy the service instance in.

## Conversational language understanding and orchestration workflow

Conversational language understanding and orchestration workflow are only available in some Azure regions. Some regions are available for **both authoring and prediction**, while other regions are **prediction only**. Language resources in authoring regions allow you to create, edit, train, and deploy your projects. Language resources in prediction regions allow you to get [predictions from a deployment](./custom-features/multi-region-deployment.md).

| Region             | Authoring | Prediction  |
|--------------------|-----------|-------------|
|AustraliaEast|✓|✓|
|BrazilSouth||✓|
|CanadaCentral|✓|✓|
|CanadaEast||✓|
|CentralIndia|✓|✓|
|CentralUS||✓|
|ChinaEast2|✓|✓|
|ChinaNorth2||✓|
|EastAsia||✓|
|EastUS|✓|✓|
|EastUS2|✓|✓|
|FranceCentral||✓|
|GermanyWestCentral||✓|
|ItalyNorth||✓|
|JapanEast||✓|
|JapanWest||✓|
|JioIndiaCentral||✓|
|JioIndiaWest||✓|
|KoreaCentral||✓|
|NorthCentralUS||✓|
|NorthEurope|✓|✓|
|NorwayEast||✓|
|QatarCentral||✓|
|SouthAfricaNorth||✓|
|SouthCentralUS|✓|✓|
|SoutheastAsia||✓|
|SwedenCentral||✓|
|SwitzerlandNorth|✓|✓|
|UAENorth||✓|
|UKSouth|✓|✓|
|UKWest||✓|
|WestCentralUS||✓|
|WestEurope|✓|✓|
|WestUS||✓|
|WestUS2|✓|✓|
|WestUS3|✓|✓|

## Custom named entity recognition

Custom named entity recognition is only available in some Azure regions. Some regions are available for **both authoring and prediction**, while other regions are **prediction only**. Language resources in authoring regions allow you to create, edit, train, and deploy your projects. Language resources in prediction regions allow you to get [predictions from a deployment](./custom-features/multi-region-deployment.md).

| Region             | Authoring | Prediction  |
|--------------------|-----------|-------------|
|AustraliaEast|✓|✓|
|BrazilSouth||✓|
|CanadaCentral|✓|✓|
|CanadaEast||✓|
|CentralIndia|✓|✓|
|CentralUS||✓|
|EastAsia||✓|
|EastUS|✓|✓|
|EastUS2|✓|✓|
|FranceCentral||✓|
|GermanyWestCentral||✓|
|JapanEast||✓|
|JapanWest||✓|
|JioIndiaCentral||✓|
|JioIndiaWest||✓|
|KoreaCentral||✓|
|NorthCentralUS||✓|
|NorthEurope|✓|✓|
|NorwayEast||✓|
|QatarCentral||✓|
|SouthAfricaNorth||✓|
|SouthCentralUS|✓|✓|
|SoutheastAsia||✓|
|SwedenCentral||✓|
|SwitzerlandNorth|✓|✓|
|UAENorth||✓|
|UKSouth|✓|✓|
|UKWest||✓|
|WestCentralUS||✓|
|WestEurope|✓|✓|
|WestUS||✓|
|WestUS2|✓|✓|
|WestUS3|✓|✓|

### Data augmentation feature in Custom Named Entity Recognition

The data augmentation capability allows users to use an Azure OpenAI model to generate supplementary training data during the creation of a custom named entity recognition model. This functionality is currently limited to select regions.

* All entity data utilized with data augmentation is required to include a description field.
* Supported Azure OpenAI model types for this feature are gpt-4o and gpt-4 32k.
* The language resource must also have the **Azure OpenAI Contributor** role assigned on the Azure OpenAI resource.


| Region | `CNER` data augmentation support|
|---|---|
|EastUS|✓|
|SwitzerlandNorth|✓|
|AustraliaEast|✓|

## Custom text classification

Custom text classification is only available in some Azure regions. Some regions are available for **both authoring and prediction**, while other regions are **prediction only**. Language resources in authoring regions allow you to create, edit, train, and deploy your projects. Language resources in prediction regions allow you to get [predictions from a deployment](./custom-features/multi-region-deployment.md).

| Region             | Authoring | Prediction  |
|--------------------|-----------|-------------|
|AustraliaEast|✓|✓|
|BrazilSouth||✓|
|CanadaCentral|✓|✓|
|CanadaEast||✓|
|CentralIndia|✓|✓|
|CentralUS||✓|
|EastAsia||✓|
|EastUS|✓|✓|
|EastUS2|✓|✓|
|FranceCentral||✓|
|GermanyWestCentral||✓|
|JapanEast||✓|
|JapanWest||✓|
|JioIndiaCentral||✓|
|JioIndiaWest||✓|
|KoreaCentral||✓|
|NorthCentralUS||✓|
|NorthEurope|✓|✓|
|NorwayEast||✓|
|QatarCentral||✓|
|SouthAfricaNorth||✓|
|SouthCentralUS|✓|✓|
|SoutheastAsia||✓|
|SwedenCentral||✓|
|SwitzerlandNorth|✓|✓|
|UAENorth||✓|
|UKSouth|✓|✓|
|UKWest||✓|
|WestCentralUS||✓|
|WestEurope|✓|✓|
|WestUS||✓|
|WestUS2|✓|✓|
|WestUS3|✓|✓|

## Summarization

|Region                |Text abstractive summarization|Conversation summarization               |
|----------------------|------------------------------|-----------------------------------------|
|AustraliaEast|✓|✓|
|CanadaCentral|✓|✓|
|CentralUS|✓|✓|
|ChinaNorth3|✓|✓|
|EastUS|✓|✓|
|EastUS2|✓|✓|
|FranceCentral|✓|✓|
|GermanyWestCentral|✓|✓|
|ItalyNorth|✓|✓|
|JapanEast|✓|✓|
|NorthCentralUS|✓|✓|
|NorthEurope|✓|✓|
|SouthCentralUS|✓|✓|
|SouthUK|✓|✓|
|SoutheastAsia|✓|✓|
|SwitzerlandNorth|✓|✓|
|USGovVirginia|✓|✓|
|USGovArizona|✓|✓|
|USNatEast|✓|✓|
|USNatWest|✓|✓|
|USSecEast|✓|✓|
|USSecWest|✓|✓|
|WestEurope|✓|✓|
|WestUS|✓|✓|
|WestUS2|✓|✓|

### Next steps

* [Language support](./language-support.md)
* [Quotas and limits](./data-limits.md)
