---
title: Custom text classification limits
titleSuffix: Azure AI services
description: Learn about the data and rate limits when using custom text classification.
#services: cognitive-services
author: jboback
manager: nitinme
ms.date: 11/21/2024
ms.service: azure-ai-language
ms.topic: conceptual
ms.author: jboback
ms.custom: language-service-custom-classification, references_regions
---

# Custom text classification limits

Use this article to learn about the data and service limits when using custom text classification.

## Language resource limits

* Your Language resource has to be created in one of the supported regions and pricing tiers listed below.

* You can only connect 1 storage account per resource. This process is irreversible. If you connect a storage account to your resource, you cannot unlink it later. Learn more about [connecting a storage account](how-to/create-project.md#create-language-resource-and-connect-storage-account)

* You can have up to 500 projects per resource.

* Project names have to be unique within the same resource across all custom features.

## Pricing tiers

Custom text classification is available with the following pricing tiers:

|Tier|Description|Limit|
|--|--|--|
|F0 |Free tier|You are only allowed one F0 tier Language resource per subscription.|
|S |Paid tier|You can have unlimited Language S tier resources per subscription. | 


See [pricing](https://azure.microsoft.com/pricing/details/cognitive-services/language-service/) for more information.

## Regional availability 

See [Language service regional availability](../concepts/regional-support.md#custom-text-classification).

## API limits

|Item|Request type| Maximum limit|
|:-|:-|:-|
|Authoring API|POST|10 per minute|
|Authoring API|GET|100 per minute|
|Prediction API|GET/POST|1,000 per minute|
|Document size|--|125,000 characters. You can send up to 25 documents as long as they collectively do not exceed 125,000 characters|

> [!TIP]
> If you need to send larger files than the limit allows, you can break the text into smaller chunks of text before sending them to the API. You use can the [chunk command from CLUtils](https://github.com/microsoft/CognitiveServicesLanguageUtilities/blob/main/CustomTextAnalytics.CLUtils/Solution/CogSLanguageUtilities.ViewLayer.CliCommands/Commands/ChunkCommand/README.md) for this process.

## Quota limits

|Pricing tier |Item |Limit |
| --- | --- | ---|
|F|Training time| 1 hour per month|
|S|Training time| Unlimited, Pay as you go |
|F|Prediction Calls| 5,000 text records per month  |
|S|Prediction Calls| Unlimited, Pay as you go |

## Document limits

* You can only use `.txt`. files. If your data is in another format, you can use the [CLUtils parse command](https://github.com/microsoft/CognitiveServicesLanguageUtilities/blob/main/CustomTextAnalytics.CLUtils/Solution/CogSLanguageUtilities.ViewLayer.CliCommands/Commands/ParseCommand/README.md) to open your document and extract the text.

* All files uploaded in your container must contain data. Empty files are not allowed for training.

* All files should be available at the root of your container.

## Data limits

The following limits are observed for the custom text classification.

|Item|Lower Limit| Upper Limit |
| --- | --- | --- |
|Documents count | 10 | 100,000 |
|Document length in characters | 1 | 128,000 characters; approximately 28,000 words or 56 pages. |
|Count of classes | 1 | 200 |
|Count of trained models per project| 0 | 10 |
|Count of deployments per project (paid tier) | 0 | 10 |
|Count of deployments per project (free tier) | 0 | 1 |

## Naming limits

| Item | Limits |
|--|--|
| Project name |  You can only use letters `(a-z, A-Z)`, and numbers `(0-9)` ,symbols  `_ . -`,with no spaces. Maximum allowed length is 50 characters. |
| Model name |  You can only use letters `(a-z, A-Z)`, numbers `(0-9)` and symbols `_ . -`. Maximum allowed length is 50 characters.  |
| Deployment name |  You can only use letters `(a-z, A-Z)`, numbers `(0-9)` and symbols `_ . -`. Maximum allowed length is 50 characters.  |
| Class name| You can only use letters `(a-z, A-Z)`, numbers `(0-9)` and all symbols except ":", `$ & %  * (  ) + ~ # / ?`. Maximum allowed length is 50 characters.|
| Document name | You can only use letters `(a-z, A-Z)`, and numbers `(0-9)` with no spaces. |

## Next steps

* [Custom text classification overview](overview.md)
