---
title: Regions - Speech service
titleSuffix: Azure AI services
description: A list of available regions and endpoints for the Speech service, including speech to text, text to speech, and speech translation.
author: eric-urban
manager: nitinme
ms.service: azure-ai-speech
ms.topic: conceptual
ms.date: 9/23/2024
ms.author: eur
ms.custom: references_regions
#Customer intent: As a developer, I want to learn about the available regions and endpoints for the Speech service.
---

# Speech service supported regions

The Speech service allows your application to convert audio to text, perform speech translation, and convert text to speech. The service is available in multiple regions with unique endpoints for the Speech SDK and REST APIs. You can perform custom configurations to your speech experience, for all regions, at the [Speech Studio](https://aka.ms/speechstudio/).

Keep in mind the following points:

- If your application uses a [Speech SDK](speech-sdk.md), you provide the region identifier, such as `westus`, when you create a `SpeechConfig`. Make sure the region matches the region of your subscription.
- If your application uses one of the Speech service REST APIs, the region is part of the endpoint URI you use when making requests.
- Keys created for a region are valid only in that region. If you attempt to use them with other regions, you get authentication errors.

> [!NOTE]
> Speech service doesn't store or process customer data outside the region the customer deploys the service instance in.

## Speech service

The following regions are supported for Speech service features such as speech to text, text to speech, pronunciation assessment, and translation. The geographies are listed in alphabetical order.

| **Region** | **Fast transcription** | **Video translation** | **Batch synthesis API** | **Custom speech** | **Custom speech training with audio**<sup>1</sup> | **Custom neural voice** | **Custom neural voice training**<sup>2</sup> | **Custom neural voice high performance endpoint** | **Personal voice** | **Text to speech avatar** | **Custom keyword advanced models** | **Keyword verification** | **Speaker recognition** | **Intent recognition**<sup>3</sup>  | **Voice assistants** |
|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| australiaeast      | ✅ |  | ✅ |  |  |  |  |  |  |  |  |  |  |  |  |
| brazilsouth        | ✅ |  | ✅ |  |  |  |  |  |  |  |  |  |  |  |  |
| canadacentral      |  |  | ✅ |  |  |  |  |  |  |  |  |  |  |  |  |
| centralindia       | ✅ |  | ✅ |  |  |  |  |  |  |  |  |  |  |  |  |
| centralus          |  |  | ✅ |  |  |  |  |  |  |  |  |  |  |  |  |
| eastasia           |  |  | ✅ |  |  |  |  |  |  |  |  |  |  |  |  |
| eastus             | ✅ |  | ✅ |  |  |  |  |  |  |  |  |  |  |  |  |
| eastus2            | ✅ |  | ✅ |  |  |  |  |  |  |  |  |  |  |  |  |
| francecentral      | ✅ |  | ✅ |  |  |  |  |  |  |  |  |  |  |  |  |
| germanywestcentral |  |  | ✅ |  |  |  |  |  |  |  |  |  |  |  |  |
| japaneast          | ✅ |  | ✅ |  |  |  |  |  |  |  |  |  |  |  |  |
| japanwest          |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| koreacentral       |  |  | ✅ |  |  |  |  |  |  |  |  |  |  |  |  |
| northcentralus     | ✅ |  | ✅ |  |  |  |  |  |  |  |  |  |  |  |  |
| northeurope        | ✅ |  | ✅ |  |  |  |  |  |  |  |  |  |  |  |  |
| norwayeast         |  |  | ✅ |  |  |  |  |  |  |  |  |  |  |  |  |
| qatarcentral       |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| southafricanorth   |  |  | ✅ |  |  |  |  |  |  |  |  |  |  |  |  |
| southcentralus     | ✅ |  | ✅ |  |  |  |  |  |  |  |  |  |  |  |  |
| southeastasia      | ✅ |  | ✅ |  |  |  |  |  |  |  |  |  |  |  |  |
| swedencentral      | ✅ |  | ✅ |  |  |  |  |  |  |  |  |  |  |  |  |
| switzerlandnorth   |  |  | ✅ |  |  |  |  |  |  |  |  |  |  |  |  |
| switzerlandwest    |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| uaenorth           |  |  | ✅ |  |  |  |  |  |  |  |  |  |  |  |  |
| uksouth            |  |  | ✅ |  |  |  |  |  |  |  |  |  |  |  |  |
| westcentralus      |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| westeurope         | ✅ |  | ✅ |  |  |  |  |  |  |  |  |  |  |  |  |
| westus             | ✅ |  | ✅ |  |  |  |  |  |  |  |  |  |  |  |  |
| westus2            | ✅ |  | ✅ |  |  |  |  |  |  |  |  |  |  |  |  |
| westus3            | ✅ |  |  |  |  |  |  |  |  |  |  |  |  |  |  |

<sup>1</sup> The region has dedicated hardware for custom speech training. If you plan to train a custom model with audio data, you must use one of the regions with dedicated hardware. Then you can [copy the trained model](how-to-custom-speech-train-model.md#copy-a-model) to another region.

<sup>2</sup> The region is available for custom neural voice training. You can copy a trained neural voice model to other regions for deployment.

<sup>3</sup> For intent recognitiion, the [Speech SDK](speech-sdk.md) supports voice assistant capabilities through [Direct Line Speech](./direct-line-speech.md) for regions in the following table.

## Intent recognition

Available regions for intent recognition via the Speech SDK are in the following table.

| Global region | Region           | Region identifier |
| ------------- | ---------------- | ----------------- |
| Asia          | East Asia        | `eastasia`        |
| Asia          | Southeast Asia   | `southeastasia`   |
| Australia     | Australia East   | `australiaeast`   |
| Europe        | North Europe     | `northeurope`     |
| Europe        | West Europe      | `westeurope`      |
| North America | East US          | `eastus`          |
| North America | East US 2        | `eastus2`         |
| North America | South Central US | `southcentralus`  |
| North America | West Central US  | `westcentralus`   |
| North America | West US          | `westus`          |
| North America | West US 2        | `westus2`         |
| South America | Brazil South     | `brazilsouth`     |

This is a subset of the publishing regions supported by the [Language Understanding service (LUIS)](../luis/luis-reference-regions.md).

## Voice assistants

The [Speech SDK](speech-sdk.md) supports voice assistant capabilities through [Direct Line Speech](./direct-line-speech.md) for regions in the following table.

| Global region | Region           | Region identifier |
| ------------- | ---------------- | ----------------- |
| North America | West US          | `westus`          |
| North America | West US 2        | `westus2`         |
| North America | East US          | `eastus`          |
| North America | East US 2        | `eastus2`         |
| North America | West Central US  | `westcentralus`   |
| North America | South Central US | `southcentralus`  |
| Europe        | West Europe      | `westeurope`      |
| Europe        | North Europe     | `northeurope`     |
| Asia          | East Asia        | `eastasia`        |
| Asia          | Southeast Asia   | `southeastasia`   |
| India         | Central India    | `centralindia`    |
