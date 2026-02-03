---
title: Supported Regions for Azure Speech
titleSuffix: Foundry Tools
description: This article provides a list of available regions and endpoints for Azure Speech, including speech to text, text to speech, and speech translation.
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-speech
ms.topic: concept-article
ms.date: 11/09/2025
ms.author: pafarley
ms.custom: references_regions
#Customer intent: As a developer, I want to learn about the available regions and endpoints for Azure Speech so that I can decide how to use the features in my application.
---

# Supported regions for Azure Speech

Azure Speech allows your application to convert audio to text, perform speech translation, and convert text to speech. Azure Speech is available in multiple regions with unique endpoints for the Speech SDK and REST APIs.

Keep in mind the following points:

- If your application uses the [Speech SDK](speech-sdk.md), you provide the region identifier (such as `westus`) when you create a `SpeechConfig` instance. Make sure that the region matches the region of your Azure Speech resource.
- If your application uses one of the Azure Speech REST APIs, the region is part of the endpoint URI that you use when making requests.
- Keys created for a region are valid only in that region. If you try to use them with other regions, you get authentication errors.

> [!NOTE]
> Azure Speech doesn't store or process your data outside the region of your Azure Speech resource. The data is stored or processed only in the region where the resource is created. For example, if you create a Foundry resource for speech in the `westus` region, the data is only in the `westus` region.

## Regions

The regions in the following tables support most of the core features of Azure Speech, such as speech to text, text to speech, and translation. Some features, such as fast transcription and batch synthesis, require specific regions. For the features that require specific regions, the tables indicate the regions that support them.

# [Geographies](#tab/geographies)

| Geography | Region | Region identifier |
| ----- | ------- | ------ |
| Africa | South Africa North | `southafricanorth` |
| Asia Pacific | East Asia | `eastasia` |
| Asia Pacific | Southeast Asia | `southeastasia` |
| Asia Pacific | Australia East | `australiaeast` |
| Asia Pacific | Central India | `centralindia` |
| Asia Pacific | Japan East | `japaneast` |
| Asia Pacific | Japan West | `japanwest` |
| Asia Pacific | Korea Central | `koreacentral` |
| Canada | Canada Central | `canadacentral` |
| Canada | Canada East | `canadaeast` |
| Europe | North Europe | `northeurope` |
| Europe | West Europe | `westeurope` |
| Europe | France Central | `francecentral` |
| Europe | Germany West Central | `germanywestcentral` |
| Europe | Italy North | `italynorth` |
| Europe | Norway East | `norwayeast` |
| Europe | Sweden Central | `swedencentral` |
| Europe | Switzerland North | `switzerlandnorth` |
| Europe | Switzerland West | `switzerlandwest` |
| Europe | UK South | `uksouth` |
| Europe | UK West | `ukwest` |
| Middle East | UAE North | `uaenorth` |
| South America | Brazil South | `brazilsouth` |
| Qatar | Qatar Central | `qatarcentral` |
| US | Central US | `centralus` |
| US | East US | `eastus` |
| US | East US 2 | `eastus2` |
| US | North Central US | `northcentralus` |
| US | South Central US | `southcentralus` |
| US | West Central US | `westcentralus` |
| US | West US | `westus` |
| US | West US 2 | `westus2` |
| US | West US 3 | `westus3` |

> [!NOTE]
> The following regions supported by an `AIServices` resource are currently not supported for speech processing: `southindia`, `spaincentral`.

# [Speech to text](#tab/stt)

| Region | Real-time transcription<sup>1</sup> | Fast transcription | Batch transcription<sup>1</sup> | Whisper via batch transcription | Whisper via Azure OpenAI | Custom speech training<sup>2</sup> |
| ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| `australiaeast` | ✅ | ✅ | ✅ | ✅ | | ✅ |
| `brazilsouth` | ✅ | ✅ | ✅ | | | |
| `canadacentral` | ✅ | ✅ | ✅ | | | ✅ |
| `canadaeast` | ✅ | | ✅ | | | |
| `centralindia` | ✅ | ✅ | ✅ | | ✅ | ✅ |
| `centralus` | ✅ | | ✅ | | | |
| `eastasia` | ✅ | | ✅ | | | ✅ |
| `eastus` | ✅ | ✅ | ✅ | ✅ | | ✅ |
| `eastus2` | ✅ | ✅ | ✅ | | ✅ | ✅ |
| `francecentral` | ✅ | ✅ | ✅ | | | ✅ |
| `germanywestcentral` | ✅ | ✅ | ✅ | | | |
| `italynorth` | ✅ | | ✅ | | | |
| `japaneast` | ✅ | ✅ | ✅ | ✅ | | ✅ |
| `japanwest` | ✅ | ✅ | ✅ | | | |
| `koreacentral` | ✅ | ✅ | ✅ | | | ✅ |
| `northcentralus` | ✅ | ✅ | ✅ | | ✅ | |
| `northeurope` | ✅ | ✅ | ✅ | | | ✅ |
| `norwayeast` | ✅ | | ✅ | | ✅ | |
| `qatarcentral` | ✅ | | ✅ | | | |
| `southafricanorth` | ✅ | | ✅ | | | |
| `southcentralus` | ✅ | ✅ | ✅ | ✅ | | ✅ |
| `southeastasia` | ✅ | ✅ | ✅ | ✅ | | ✅ |
| `swedencentral` | ✅ | ✅ | ✅ | | ✅ | |
| `switzerlandnorth` | ✅ | | ✅ | | ✅ | ✅ |
| `switzerlandwest` | ✅ | | ✅ | | | |
| `uaenorth` | ✅ | | ✅ | | | |
| `uksouth` | ✅ | ✅ | ✅ | ✅ | | ✅ |
| `ukwest` | ✅ | | ✅ | | | |
| `westcentralus` | ✅ | | ✅ | | | |
| `westeurope` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `westus` | ✅ | ✅ | ✅ | | | ✅ |
| `westus2` | ✅ | ✅ | ✅ | | | ✅ |
| `westus3` | ✅ | ✅ | ✅ | | | ✅ |

<sup>1</sup> Supports the processing of custom speech models.

<sup>2</sup> The region uses dedicated hardware for custom speech training. If you plan to train a custom model, you must use one of the regions that have dedicated hardware. Then you can [copy the trained model](how-to-custom-speech-train-model.md#copy-a-model) to another region.

# [Text to speech](#tab/tts)

| Region | Neural text to speech | Batch synthesis API | HD voices | Azure OpenAI voices | Custom voice | Custom voice training | Custom voice high-performance endpoint | Personal voice | Voice conversion | Voices and styles in preview |
| ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| `australiaeast` | ✅ | ✅ | | | ✅ | ✅ | ✅ | | | |
| `brazilsouth` | ✅ | ✅ | | | ✅ | | ✅ | | | |
| `canadacentral` | ✅ | ✅ | | | ✅ | | | | | |
| `canadaeast` | ✅ | | | | | | | | | |
| `centralindia` | ✅ | ✅ | | | ✅ | ✅ | ✅ | | | |
| `centralus` | ✅ | ✅ | | | ✅ | | ✅ | | | |
| `eastasia` | ✅ | ✅ | | | ✅ | | | ✅ | | |
| `eastus` | ✅ | ✅ | ✅ | | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `eastus2` | ✅ | ✅ | | | ✅ | ✅ | ✅ | ✅ | | |
| `francecentral` | ✅ | ✅ | | | ✅ | | | | | |
| `germanywestcentral` | ✅ | ✅ | | | ✅ | | | | | |
| `italynorth` | ✅ | | | | ✅ | | ✅ | | | |
| `japaneast` | ✅ | ✅ | | | ✅ | ✅ | ✅ | | | |
| `japanwest` | ✅ | | | | ✅ | | | | | |
| `koreacentral` | ✅ | ✅ | | | ✅ | ✅ | ✅ | | | |
| `northcentralus` | ✅ | ✅ | | ✅ | ✅ | | ✅ | | | |
| `northeurope` | ✅ | ✅ | | | ✅ | ✅ | ✅ | | | |
| `norwayeast` | ✅ | ✅ | | | ✅ | | | | | |
| `qatarcentral` | ✅ | | | | | | | | | |
| `southafricanorth` | ✅ | ✅ | | | ✅ | | | | | |
| `southcentralus` | ✅ | ✅ | | | ✅ | ✅ | ✅ | | | |
| `southeastasia` | ✅ | ✅ | ✅ | | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `swedencentral` | ✅ | ✅ | | ✅ | ✅ | | ✅ | ✅ | | |
| `switzerlandnorth` | ✅ | ✅ | | | ✅ | | | | | |
| `switzerlandwest` | ✅ | | | | ✅ | | | | | |
| `uaenorth` | ✅ | ✅ | | | ✅ | | | | | |
| `uksouth` | ✅ | ✅ | | | ✅ | ✅ | ✅ | | | |
| `ukwest` | ✅ | | | | | | | | | |
| `westcentralus` | ✅ | | | | ✅ | | | | | |
| `westeurope` | ✅ | ✅ | ✅ | | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `westus` | ✅ | ✅ | | | ✅ | ✅ | ✅ | | | |
| `westus2` | ✅ | ✅ | | | ✅ | ✅ | ✅ | ✅ | | |
| `westus3` | ✅ | | | | ✅ | | ✅ | | | |

# [Text-to-speech avatar](#tab/ttsavatar)

| Region | Real-time avatar | Batch avatar | Custom avatar | Custom avatar training<sup>1</sup> |
| ----- | ----- | ----- | ----- | ----- |
| `eastus2` | ✅ | ✅ | ✅ | |
| `northeurope` | ✅ | ✅ | ✅ | |
| `southcentralus` | ✅ | ✅ | ✅ | |
| `southeastasia` | ✅ | ✅ | ✅ | ✅ |
| `swedencentral` | ✅ | ✅ | ✅ | |
| `westeurope` | ✅ | ✅ | ✅ | ✅ |
| `westus2` | ✅ | ✅ | ✅ | ✅ |

<sup>1</sup> Voice sync for avatars is currently supported in the Southeast Asia, West Europe, and West US 2 regions.

# [Speech translation](#tab/speech-translation)

| Region | Real-time translation | Video translation | Live interpreter |
| ----- | ----- | ----- | ----- |
| `australiaeast` | ✅ | | |
| `brazilsouth` | ✅ | | |
| `canadacentral` | ✅ | | |
| `canadaeast` | ✅ | | |
| `centralindia` | ✅ | | |
| `centralus` | ✅ | ✅ | |
| `eastasia` | ✅ | | |
| `eastus` | ✅ | ✅ | ✅ |
| `eastus2` | ✅ | ✅ | |
| `francecentral` | ✅ | | |
| `germanywestcentral` | ✅ | | |
| `italynorth` | ✅ | | |
| `japaneast` | ✅ | | ✅ |
| `japanwest` | ✅ | | |
| `koreacentral` | ✅ | | |
| `northcentralus` | ✅ | ✅ | |
| `northeurope` | ✅ | | |
| `norwayeast` | ✅ | | |
| `qatarcentral` | ✅ | | |
| `southafricanorth` | ✅ | | |
| `southcentralus` | ✅ | ✅ | |
| `southeastasia` | ✅ | | ✅ |
| `swedencentral` | ✅ | | |
| `switzerlandnorth` | ✅ | | |
| `switzerlandwest` | ✅ | | |
| `uaenorth` | ✅ | | |
| `uksouth` | ✅ | | |
| `ukwest` | ✅ | | |
| `westcentralus` | ✅ | ✅ | |
| `westeurope` | ✅ | ✅ | ✅ |
| `westus` | ✅ | ✅ | |
| `westus2` | ✅ | ✅ | ✅ |
| `westus3` | ✅ | ✅ | |

# [LLM speech](#tab/llmspeech)

| Region | Transcription | Translation |
| ----- | ----- | ----- |
| `centralindia` | ✅ | ✅ |
| `eastus` | ✅ | ✅ |
| `northeurope` | ✅ | ✅ |
| `southeastasia` | ✅ | ✅ |
| `westus` | ✅ | ✅ |

# [Voice Live](#tab/voice-live)

| Region | gpt-realtime | gpt-realtime-mini | gpt-4o | gpt-4o-mini | gpt-4.1 | gpt-4.1-mini | gpt-5.2 | gpt-5.2-chat | gpt-5.1 | gpt-5.1-chat | gpt-5 | gpt-5-mini | gpt-5-nano | gpt-5-chat | phi4-mm-realtime (preview) | phi4-mini (preview) | Agent support |
| ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| `australiaeast` | - | - | Global standard | Global standard | Global standard | Global standard | - | - | Global standard | Global standard | Global standard | Global standard | Global standard | - | - | - | ✅ |
| `brazilsouth` | - | - | Global standard | Global standard | Global standard | Global standard | - | - | - | - | Global standard | Global standard | Global standard | - | - | - | ✅ |
| `canadacentral` | - | - | - | - | Global standard | Global standard | - | - | Global standard | Global standard | Global standard | Global standard | Global standard | - | - | - | - |
| `canadaeast` | - | - | - | - | Global standard | Global standard | - | - | Global standard | Global standard | Global standard | Global standard | Global standard | - | - | - | ✅ |
| `centralindia` | Cross-region<sup>1</sup> | Cross-region<sup>1</sup> | Global standard | Global standard | Global standard | Global standard | - | - | - | - | Global standard | Global standard | Global standard | - | - | - | - |
| `eastus` | - | - | Data zone standard | Data zone standard | Data zone standard | Data zone standard | - | - | Data zone standard | - | Data zone standard | Data zone standard | Data zone standard | - | - | - | ✅ |
| `eastus2` | Global standard | Global standard | Data zone standard | Data zone standard | Data zone standard | Data zone standard | Data zone standard | Global standard | Data zone standard | Global standard | Data zone standard | Data zone standard | Data zone standard | Global standard | Regional | Regional | ✅ |
| `francecentral` | - | - | Data zone standard | Data zone standard | Data zone standard | Data zone standard | - | - | Data zone standard | - | Data zone standard | Data zone standard | Data zone standard | - | - | - | ✅ |
| `germanywestcentral` | - | - | - | - | Data zone standard | Data zone standard | - | - | - | - | Data zone standard | Data zone standard | Data zone standard | - | - | - | ✅ |
| `italynorth` | - | - | Data zone standard | Data zone standard | Data zone standard | Data zone standard | - | - | - | - | Data zone standard | Data zone standard | Data zone standard | - | - | - | ✅ |
| `japaneast` | - | - | Global standard | Global standard | Global standard | Global standard | - | - | Global standard | Global standard | Global standard | Global standard | Global standard | - | Regional | Regional | ✅ |
| `koreacentral` | - | - | Global standard | Global standard | Global standard | Global standard | - | - | Global standard | Global standard | Global standard | Global standard | Global standard | - | - | - | - |
| `northcentralus` | - | - | Data zone standard | Data zone standard | Data zone standard | Data zone standard | - | - | - | - | Data zone standard | Data zone standard | Data zone standard | - | - | - | - |
| `norwayeast` | - | - | Global standard | Global standard | Global standard | Global standard | - | - | - | - | Global standard | Global standard | Global standard | - | - | - | ✅ |
| `southafricanorth` | - | - | Global standard | Global standard | Global standard | Global standard | - | - | - | - | Global standard | Global standard | Global standard | - | - | - | ✅ |
| `southcentralus` | - | - | Data zone standard | Data zone standard | Data zone standard | Data zone standard | - | - | - | - | Data zone standard | Data zone standard | Data zone standard | - | - | - | ✅ |
| `southeastasia` | - | - | - | - | Global standard | Global standard | - | - | - | - | Global standard | Global standard | Global standard | - | Regional | Regional | ✅ |
| `swedencentral` | Global standard | Global standard | Data zone standard | Data zone standard | Data zone standard | Data zone standard | Global standard | Global standard | Data zone standard | Global standard | Data zone standard | Data zone standard | Data zone standard | Global standard | Regional | Regional | ✅ |
| `switzerlandnorth` | - | - | Global standard | Global standard | Global standard | Global standard | - | - | Global standard | Global standard | Global standard | Global standard | Global standard | - | - | - | ✅ |
| `uaenorth` | - | - | Global standard | Global standard | Global standard | Global standard | - | - | - | - | Global standard | Global standard | Global standard | - | - | - | - |
| `uksouth` | - | - | Global standard | Global standard | Global standard | Global standard | - | - | Global standard | Global standard | Global standard | Global standard | Global standard | - | - | - | ✅ |
| `westeurope` | - | - | Data zone standard | Data zone standard | Data zone standard | Data zone standard | - | - | - | - | Data zone standard | Data zone standard | Data zone standard | - | - | - | ✅ |
| `westus` | - | - | Data zone standard | Data zone standard | Data zone standard | Data zone standard | - | - | - | - | Data zone standard | Data zone standard | Data zone standard | - | - | - | ✅ |
| `westus2` | Cross-region<sup>2</sup> | Cross-region<sup>2</sup> | Data zone standard | Data zone standard | Data zone standard | Data zone standard | - | - | - | - | Data zone standard | Data zone standard | Data zone standard | - | Regional | Regional | ✅ |
| `westus3` | - | - | Data zone standard | Data zone standard | Data zone standard | Data zone standard | - | - | - | - | Data zone standard | Data zone standard | Data zone standard | - | - | - | ✅ |

<sup>1</sup> The Microsoft Foundry resource must be in Central India. Azure Speech features remain in Central India. The API for Voice Live uses Sweden Central as needed for generative AI load balancing.

<sup>2</sup> The resource must be in West US 2. Azure Speech features remain in West US 2. The API for Voice Live uses East US 2 as needed for generative AI load balancing.

# [Keyword recognition](#tab/keyword-recognition)

| Region | Custom keyword advanced models | Keyword verification |
| ----- | ----- | ----- |
| `australiaeast` | ✅ | |
| `centralindia` | ✅ | ✅ |
| `eastasia` | | ✅ |
| `eastus` | ✅ | ✅ |
| `eastus2` | ✅ | ✅ |
| `japaneast` | | ✅ |
| `northcentralus` | ✅ | |
| `northeurope` | ✅ | ✅ |
| `southcentralus` | ✅ | ✅ |
| `southeastasia` | ✅ | ✅ |
| `uksouth` | ✅ | |
| `westcentralus` | | ✅ |
| `westeurope` | ✅ | ✅ |
| `westus` | | ✅ |
| `westus2` | ✅ | ✅ |

Verify and check actions taken. Computer use might make mistakes and perform unintended actions. This behavior can happen because the model doesn't fully understand the GUI, has unclear instructions, or encounters an unexpected scenario.

# [Speech MCP server](#tab/mcp)

| Region | Speech MCP server agent tool |
| ----- | ----- |
| `australiaeast` | ✅ |
| `brazilsouth` | ✅ |
| `canadacentral` | ✅ |
| `canadaeast` | ✅ |
| `centralindia` | ✅ |
| `centralus` | ✅ |
| `eastasia` | ✅ |
| `eastus` | ✅ |
| `eastus2` | ✅ |
| `francecentral` | ✅ |
| `germanywestcentral` | ✅ |
| `italynorth` | ✅ |
| `japaneast` | ✅ |
| `japanwest` | ✅ |
| `koreacentral` | ✅ |
| `northcentralus` | ✅ |
| `northeurope` | ✅ |
| `norwayeast` | ✅ |
| `qatarcentral` | ✅ |
| `southafricanorth` | ✅ |
| `southcentralus` | ✅ |
| `southeastasia` | ✅ |
| `swedencentral` | ✅ |
| `switzerlandnorth` | ✅ |
| `switzerlandwest` | ✅ |
| `uaenorth` | ✅ |
| `uksouth` | ✅ |
| `ukwest` | ✅ |
| `westcentralus` | ✅ |
| `westeurope` | ✅ |
| `westus` | ✅ |
| `westus2` | ✅ |
| `westus3` | ✅ |

---

## Related content

- [Language and voice support](./language-support.md)
- [Quotas and limits](./speech-services-quotas-and-limits.md)
