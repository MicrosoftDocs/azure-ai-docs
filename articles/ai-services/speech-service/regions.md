---
title: Regions - Speech service
titleSuffix: Azure AI services
description: A list of available regions and endpoints for the Speech service, including speech to text, text to speech, and speech translation.
author: eric-urban
manager: nitinme
ms.service: azure-ai-speech
ms.topic: conceptual
ms.date: 1/6/2025
ms.author: eur
ms.custom: references_regions
#Customer intent: As a developer, I want to learn about the available regions and endpoints for the Speech service.
---

# Speech service supported regions

The Speech service allows your application to convert audio to text, perform speech translation, and convert text to speech. The service is available in multiple regions with unique endpoints for the Speech SDK and REST APIs. 

Keep in mind the following points:

- If your application uses a [Speech SDK](speech-sdk.md), you provide the region identifier, such as `westus`, when you create a `SpeechConfig`. Make sure the region matches the region of your subscription.
- If your application uses one of the Speech service REST APIs, the region is part of the endpoint URI you use when making requests.
- Keys created for a region are valid only in that region. If you attempt to use them with other regions, you get authentication errors.

> [!NOTE]
> Speech service doesn't store or process your data outside the region of your Speech resource. The data is only stored or processed in the region where the resource is created. For example, if you create a Speech resource in the `westus` region, the data is only in the `westus` region.

## Regions

The regions in this table support most of the core features of the Speech service, such as speech to text, text to speech, pronunciation assessment, and translation. Some features, such as fast transcription and batch synthesis API, require specific regions. For the features that require specific regions, the table indicates the regions that support them.

| **Region** | **Fast transcription** | **Batch synthesis API** | **Custom speech** | **Custom speech training with audio**<sup>1</sup> | **Custom neural voice** | **Custom neural voice training**<sup>2</sup> | **Custom neural voice high performance endpoint** | **Personal voice** | **Text to speech avatar** | **Video translation** | **Custom keyword advanced models** | **Keyword verification** | **Speaker recognition** | **Intent recognition**<sup>3</sup> | **Voice assistants**<sup>3</sup> |
|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| australiaeast      | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |  |  |  | ✅ |  | ✅ | ✅ |  |
| brazilsouth        | ✅ | ✅ | ✅ |  | ✅ |  |  |  |  |  |  |  |  | ✅ |  |
| canadacentral      |  | ✅ | ✅ | ✅ | ✅ |  |  |  |  |  |  |  | ✅ |  |  |
| centralindia       | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |  |  |  |  | ✅ | ✅ | ✅ |  | ✅ |
| centralus          |  | ✅ | ✅ |  | ✅ |  |  |  |  |  |  |  | ✅ |  |  |
| eastasia           |  | ✅ | ✅ |  | ✅ |  |  |  |  |  |  | ✅ | ✅ | ✅ | ✅ |
| eastus             | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |  | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| eastus2            | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |  |  | ✅ |  | ✅ | ✅ | ✅ | ✅ | ✅ |
| francecentral      | ✅ | ✅ | ✅ |  | ✅ |  |  |  |  |  |  |  | ✅ |  |  |
| germanywestcentral |  | ✅ | ✅ |  | ✅ |  |  |  |  |  |  |  | ✅ |  |  |
| japaneast          | ✅ | ✅ | ✅ |  | ✅ | ✅ |  |  |  |  |  | ✅ | ✅ |  |  |
| japanwest          |  |  | ✅ |  | ✅ |  |  |  |  |  |  |  | ✅ |  |  |
| koreacentral       |  | ✅ | ✅ |  | ✅ |  |  |  |  |  |  |  | ✅ |  |  |
| northcentralus     | ✅ | ✅ | ✅ |  | ✅ |  |  |  |  |  | ✅ |  |  |  |  |
| northeurope        | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |  | ✅ |  | ✅ | ✅ | ✅ | ✅ | ✅ |
| norwayeast         |  | ✅ | ✅ |  | ✅ |  |  |  |  |  |  |  | ✅ |  |  |
| qatarcentral       |  |  | ✅ |  | ✅ |  |  |  |  |  |  |  | ✅ |  |  |
| southafricanorth   |  | ✅ | ✅ |  | ✅ |  |  |  |  |  |  |  |  |  |  |
| southcentralus     | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |  | ✅ |  | ✅ | ✅ |  | ✅ | ✅ |
| southeastasia      | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |  | ✅ | ✅ | ✅ | ✅ | ✅ |
| swedencentral      | ✅ | ✅ | ✅ |  |  |  |  |  | ✅ |  |  |  | ✅ |  |  |
| switzerlandnorth   |  | ✅ | ✅ |  | ✅ |  |  |  |  |  |  |  |  |  |  |
| switzerlandwest    |  |  | ✅ |  | ✅ |  |  |  |  |  |  |  | ✅ |  |  |
| uaenorth           |  | ✅ | ✅ |  | ✅ |  |  |  |  |  |  |  |  |  |  |
| uksouth            |  | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |  |  |  | ✅ |  | ✅ |  |  |
| westcentralus      |  |  | ✅ |  | ✅ |  |  |  |  |  |  | ✅ | ✅ | ✅ | ✅ |
| westeurope         | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |  | ✅ | ✅ | ✅ | ✅ | ✅ |
| westus             | ✅ | ✅ | ✅ |  | ✅ | ✅ |  |  |  |  |  | ✅ | ✅ | ✅ | ✅ |
| westus2            | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |  | ✅ |  | ✅ | ✅ | ✅ | ✅ | ✅ |
| westus3            | ✅ |  | ✅ |  | ✅ |  |  |  |  |  |  |  | ✅ |  |  |

<sup>1</sup> The region has dedicated hardware for custom speech training. If you plan to train a custom model with audio data, you must use one of the regions with dedicated hardware. Then you can [copy the trained model](how-to-custom-speech-train-model.md#copy-a-model) to another region.

<sup>2</sup> The region is available for custom neural voice training. You can copy a trained neural voice model to other regions for deployment.

<sup>3</sup> The [Speech SDK](speech-sdk.md) supports intent recognition and voice assistant capabilities through [Direct Line Speech](./direct-line-speech.md).

## Related content

- [Language and voice support](./language-support.md)
- [Quotas and limits](./speech-services-quotas-and-limits.md)
