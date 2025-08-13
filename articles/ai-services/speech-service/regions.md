---
title: Regions - Speech service
titleSuffix: Azure AI services
description: A list of available regions and endpoints for the Speech service, including speech to text, text to speech, and speech translation.
author: eric-urban
manager: nitinme
ms.service: azure-ai-speech
ms.topic: conceptual
ms.date: 7/1/2025
ms.author: eur
ms.custom: references_regions
#Customer intent: As a developer, I want to learn about the available regions and endpoints for the Speech service.
---

# Speech service supported regions

The Speech service allows your application to convert audio to text, perform speech translation, and convert text to speech. The service is available in multiple regions with unique endpoints for the Speech SDK and REST APIs.

Keep in mind the following points:

- If your application uses a [Speech SDK](speech-sdk.md), you provide the region identifier, such as `westus`, when you create a `SpeechConfig`. Make sure the region matches the region of your Speech resource.
- If your application uses one of the Speech service REST APIs, the region is part of the endpoint URI you use when making requests.
- Keys created for a region are valid only in that region. If you attempt to use them with other regions, you get authentication errors.

> [!NOTE]
> Speech service doesn't store or process your data outside the region of your Speech resource. The data is only stored or processed in the region where the resource is created. For example, if you create an AI Foundry resource for Speech in the `westus` region, the data is only in the `westus` region.

## Regions

The regions in these tables support most of the core features of the Speech service, such as speech to text, text to speech, pronunciation assessment, and translation. Some features, such as fast transcription and batch synthesis API, require specific regions. For the features that require specific regions, the table indicates the regions that support them.

# [Geographies](#tab/geographies)

| Geography | Region | Region identifier |
| ----- | ------- | ------ |
| Africa        | South Africa North   | `southafricanorth`|
| Asia Pacific  | East Asia            | `eastasia`      |
| Asia Pacific  | Southeast Asia       | `southeastasia` |
| Asia Pacific  | Australia East       | `australiaeast` |
| Asia Pacific  | Central India        | `centralindia`  |
| Asia Pacific  | Japan East           | `japaneast`     |
| Asia Pacific  | Japan West           | `japanwest`     |
| Asia Pacific  | Korea Central        | `koreacentral`  |
| Canada        | Canada Central       | `canadacentral` |
| Europe        | North Europe         | `northeurope`   |
| Europe        | West Europe          | `westeurope`    |
| Europe        | France Central       | `francecentral` |
| Europe        | Germany West Central | `germanywestcentral` |
| Europe        | Norway East          | `norwayeast`    |
| Europe        | Sweden Central       | `swedencentral` |
| Europe        | Switzerland North    | `switzerlandnorth` |
| Europe        | Switzerland West     | `switzerlandwest` |
| Europe        | UK South             | `uksouth`       |
| Middle East   | UAE North            | `uaenorth`      |
| South America | Brazil South         | `brazilsouth`   |
| Qatar         | Qatar Central        | `qatarcentral`  |
| US            | Central US           | `centralus`     |
| US            | East US              | `eastus`        |
| US            | East US 2            | `eastus2`       |
| US            | North Central US     | `northcentralus`|
| US            | South Central US     | `southcentralus`|
| US            | West Central US      | `westcentralus` |
| US            | West US              | `westus`        |
| US            | West US 2            | `westus2`       |
| US            | West US 3            | `westus3`       |


# [Speech to text](#tab/stt)

| **Region** | **Fast transcription** | **Custom speech** | **Custom speech training with audio**<sup>1</sup> |
|-----|-----|-----|-----|
| australiaeast      | ✅ | ✅ | ✅ |
| brazilsouth        | ✅ | ✅ |  |
| canadacentral      |  | ✅ | ✅ |
| centralindia       | ✅ | ✅ | ✅ |
| centralus          |  | ✅ |  |
| eastasia           |  | ✅ |  |
| eastus             | ✅ | ✅ | ✅ |
| eastus2            | ✅ | ✅ | ✅ |
| francecentral      | ✅ | ✅ |  |
| germanywestcentral |  | ✅ |  |
| japaneast          | ✅ | ✅ |  |
| japanwest          |  | ✅ |  |
| koreacentral       |  | ✅ |  |
| northcentralus     | ✅ | ✅ |  |
| northeurope        | ✅ | ✅ | ✅ |
| norwayeast         |  | ✅ |  |
| qatarcentral       |  | ✅ |  |
| southafricanorth   |  | ✅ |  |
| southcentralus     | ✅ | ✅ | ✅ |
| southeastasia      | ✅ | ✅ | ✅ |
| swedencentral      | ✅ | ✅ |  |
| switzerlandnorth   |  | ✅ |  |
| switzerlandwest    |  | ✅ |  |
| uaenorth           |  | ✅ |  |
| uksouth            | ✅ | ✅ | ✅ |
| westcentralus      |  | ✅ |  |
| westeurope         | ✅ | ✅ | ✅ |
| westus             | ✅ | ✅ |  |
| westus2            | ✅ | ✅ | ✅ |
| westus3            | ✅ | ✅ |  |

<sup>1</sup> The region has dedicated hardware for custom speech training. If you plan to train a custom model with audio data, you must use one of the regions with dedicated hardware. Then you can [copy the trained model](how-to-custom-speech-train-model.md#copy-a-model) to another region.

# [Text to speech](#tab/tts)

| **Region** | **Neural text to speech** | **Batch synthesis API** | **HD voices** | **Azure OpenAI voices**  | **Custom voice** | **Custom voice training** | **Custom voice high performance endpoint** | **Personal voice** | **Text to speech avatar** | **Custom avatar** | **Custom avatar training** |
|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| australiaeast      | ✅ | ✅ |  |  | ✅ | ✅ | ✅ |  |  |  |  |
| brazilsouth        | ✅ | ✅ |  |  | ✅ |  | ✅ |  |  |  |  |
| canadacentral      | ✅ | ✅ |  |  | ✅ |  |  |  |  |  |  |
| centralindia       | ✅ | ✅ |  |  | ✅ | ✅ | ✅ |  |  |  |  |
| centralus          | ✅ | ✅ |  |  | ✅ |  | ✅ |  |  |  |  |
| eastasia           | ✅ | ✅ |  |  | ✅ |  |  | ✅ |  |  |  |
| eastus             | ✅ | ✅ | ✅ |  | ✅ | ✅ | ✅ | ✅ |  |  |  |
| eastus2            | ✅ | ✅ |  |  | ✅ | ✅ | ✅ |  | ✅ | ✅ |  |
| francecentral      | ✅ | ✅ |  |  | ✅ |  |  |  |  |  |  |
| germanywestcentral | ✅ | ✅ |  |  | ✅ |  |  |  |  |  |  |
| japaneast          | ✅ | ✅ |  |  | ✅ | ✅ | ✅ |  |  |  |  |
| japanwest          | ✅ |  |  |  | ✅ |  |  |  |  |  |  |
| koreacentral       | ✅ | ✅ |  |  | ✅ | ✅ | ✅ |  |  |  |  |
| northcentralus     | ✅ | ✅ |  | ✅ | ✅ |  | ✅ |  |  |  |  |
| northeurope        | ✅ | ✅ |  |  | ✅ | ✅ | ✅ |  | ✅ | ✅ |  |
| norwayeast         | ✅ | ✅ |  |  | ✅ |  |  |  |  |  |  |
| qatarcentral       | ✅ |  |  |  | ✅ |  |  |  |  |  |  |
| southafricanorth   | ✅ | ✅ |  |  | ✅ |  |  |  |  |  |  |
| southcentralus     | ✅ | ✅ |  |  | ✅ | ✅ | ✅ |  | ✅ | ✅ |  |
| southeastasia      | ✅ | ✅ | ✅ |  | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| swedencentral      | ✅ | ✅ |  | ✅ |  |  |  |  | ✅ | ✅ |  |
| switzerlandnorth   | ✅ | ✅ |  |  | ✅ |  |  |  |  |  |  |
| switzerlandwest    | ✅ |  |  |  | ✅ |  |  |  |  |  |  |
| uaenorth           | ✅ | ✅ |  |  | ✅ |  |  |  |  |  |  |
| uksouth            | ✅ | ✅ |  |  | ✅ | ✅ | ✅ |  |  |  |  |
| westcentralus      | ✅ |  |  |  | ✅ |  |  |  |  |  |  |
| westeurope         | ✅ | ✅ | ✅ |  | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| westus             | ✅ | ✅ |  |  | ✅ | ✅ | ✅ |  |  |  |  |
| westus2            | ✅ | ✅ |  |  | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| westus3            | ✅ |  |  |  | ✅ |  | ✅ |  |  |  |  |

# [Speech translation](#tab/speech-translation)

| **Region** | **Video translation** |
|-----|-----|
| australiaeast      |  |
| brazilsouth        |  |
| canadacentral      |  |
| centralindia       |  |
| centralus          | ✅ |
| eastasia           |  |
| eastus             | ✅ |
| eastus2            | ✅ |
| francecentral      |  |
| germanywestcentral |  |
| japaneast          |  |
| japanwest          |  |
| koreacentral       |  |
| northcentralus     | ✅ |
| northeurope        |  |
| norwayeast         |  |
| qatarcentral       |  |
| southafricanorth   |  |
| southcentralus     | ✅ |
| southeastasia      |  |
| swedencentral      |  |
| switzerlandnorth   |  |
| switzerlandwest    |  |
| uaenorth           |  |
| uksouth            |  |
| westcentralus      | ✅ |
| westeurope         | ✅ |
| westus             | ✅ |
| westus2            | ✅ |
| westus3            | ✅ |

# [Voice live](#tab/voice-live)

| **Region** | **gpt-4o-realtime-preview** | **gpt-4o-mini-realtime-preview** | **gpt-4o** | **gpt-4o-mini**  | **gpt-4.1** | **gpt-4.1-mini** | **gpt-4.1-nano** | **phi4-mm-realtime** | **phi4-mini** | 
|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| centralindia       | Cross-region<sup>1</sup> | Cross-region<sup>1</sup> | Global standard | Global standard | - | Global standard | Global standard | - | - |
| eastus2       | Global standard | Global standard | Data zone standard | Data zone standard | Data zone standard | Data zone standard | Data zone standard | Regional | Regional |
| southeastasia       | - | - | - | - | - | Global standard | Global standard | - | - |
| swedencentral       | Global standard | Global standard | Data zone standard | Data zone standard | Data zone standard | Data zone standard | Data zone standard | Regional | Regional |
| westus2       | Cross-region<sup>2</sup> | Cross-region<sup>2</sup> | Data zone standard | Data zone standard | Data zone standard | Data zone standard | Data zone standard | Regional | Regional |

<sup>1</sup> The Azure AI Foundry resource must be in Central India. Azure AI Speech features remain in Central India. The voice live API uses Sweden Central as needed for generative AI load balancing.  

<sup>2</sup> The Azure AI Foundry resource must be in West US 2. Azure AI Speech features remain in West US 2. The voice live API uses East US 2 as needed for generative AI load balancing.

# [Intent recognition](#tab/intent-recognition)

| **Region** | **Intent recognition** |
|-----|-----|
| australiaeast      | ✅ |
| brazilsouth        | ✅ |
| canadacentral      |  |
| centralindia       |  |
| centralus          |  |
| eastasia           | ✅ |
| eastus             | ✅ |
| eastus2            | ✅ |
| francecentral      |  |
| germanywestcentral |  |
| japaneast          |  |
| japanwest          |  |
| koreacentral       |  |
| northcentralus     |  |
| northeurope        | ✅ |
| norwayeast         |  |
| qatarcentral       |  |
| southafricanorth   |  |
| southcentralus     | ✅ |
| southeastasia      | ✅ |
| swedencentral      |  |
| switzerlandnorth   |  |
| switzerlandwest    |  |
| uaenorth           |  |
| uksouth            |  |
| westcentralus      | ✅ |
| westeurope         | ✅ |
| westus             | ✅ |
| westus2            | ✅ |
| westus3            |  |

> [!NOTE]
> The [Speech SDK](speech-sdk.md) supports intent recognition through Direct Line Speech.


# [Keyword recognition](#tab/keyword-recognition)

| **Region** | **Custom keyword advanced models** | **Keyword verification** |
|-----|-----|-----|
| australiaeast      | ✅ |  |
| brazilsouth        |  |  |
| canadacentral      |  |  |
| centralindia       | ✅ | ✅ |
| centralus          |  |  |
| eastasia           |  | ✅ |
| eastus             | ✅ | ✅ |
| eastus2            | ✅ | ✅ |
| francecentral      |  |  |
| germanywestcentral |  |  |
| japaneast          |  | ✅ |
| japanwest          |  |  |
| koreacentral       |  |  |
| northcentralus     | ✅ |  |
| northeurope        | ✅ | ✅ |
| norwayeast         |  |  |
| qatarcentral       |  |  |
| southafricanorth   |  |  |
| southcentralus     | ✅ | ✅ |
| southeastasia      | ✅ | ✅ |
| swedencentral      |  |  |
| switzerlandnorth   |  |  |
| switzerlandwest    |  |  |
| uaenorth           |  |  |
| uksouth            | ✅ |  |
| westcentralus      |  | ✅ |
| westeurope         | ✅ | ✅ |
| westus             |  | ✅ |
| westus2            | ✅ | ✅ |
| westus3            |  |  |

# [Scenarios](#tab/scenarios)

| **Region** | **Pronunciation assessment** | **Speaker recognition** | **Voice assistants** | 
|-----|-----|-----|
| australiaeast      | ✅ | ✅ |  |
| brazilsouth        | ✅ |  |  |
| canadacentral      | ✅ | ✅ | ✅ |
| centralindia       | ✅ | ✅ |  |
| centralus          | ✅ | ✅ |  |
| eastasia           | ✅ | ✅ | ✅ |
| eastus             | ✅ | ✅ | ✅ |
| eastus2            | ✅ | ✅ | ✅ |
| francecentral      | ✅ | ✅ |  |
| germanywestcentral | ✅ | ✅ |  |
| japaneast          | ✅ | ✅ |  |
| japanwest          | ✅ | ✅ |  |
| koreacentral       | ✅ | ✅ |  |
| northcentralus     | ✅ |  |  |
| northeurope        | ✅ | ✅ | ✅ |
| norwayeast         | ✅ | ✅ |  |
| qatarcentral       | ✅ | ✅ |  |
| southafricanorth   | ✅ |  |  |
| southcentralus     | ✅ |  | ✅ |
| southeastasia      | ✅ | ✅ | ✅ |
| swedencentral      | ✅ | ✅ |  |
| switzerlandnorth   | ✅ |  |  |
| switzerlandwest    | ✅ | ✅ |  |
| uaenorth           | ✅ |  |  |
| uksouth            | ✅ | ✅ |  |
| westcentralus      | ✅ | ✅ | ✅ |
| westeurope         | ✅ | ✅ | ✅ |
| westus             | ✅ | ✅ | ✅ |
| westus2            | ✅ | ✅ | ✅ |
| westus3            | ✅ | ✅ |  |

> [!NOTE]
> The [Speech SDK](speech-sdk.md) supports voice assistant capabilities through Direct Line Speech.

---

## Related content

- [Language and voice support](./language-support.md)
- [Quotas and limits](./speech-services-quotas-and-limits.md)
