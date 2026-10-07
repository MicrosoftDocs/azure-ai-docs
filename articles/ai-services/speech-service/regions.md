---
title: Supported regions for Azure Speech
titleSuffix: Foundry Tools
description: Find the Azure Speech regions and region identifiers for the Speech SDK and REST APIs, including speech to text, text to speech, and translation.
author: PatrickFarley
manager: mcleans
ms.service: azure-speech-foundry-tools
ms.topic: concept-article
ms.date: 10/07/2026
ms.author: pafarley
ms.custom: references_regions, dev-focus
ai-usage: ai-assisted
#Customer intent: As a developer, I want to learn about the available regions and endpoints for Azure Speech so that I can decide how to use the features in my application.
---

# Supported regions for Azure Speech

Azure Speech allows your application to convert audio to text, perform speech translation, and convert text to speech. Azure Speech is available in multiple regions with unique endpoints for the Speech SDK and REST APIs.


## Use region identifiers

When configuring Azure Speech in your application:

- Provide the region identifier (such as `westus`) when you create a `SpeechConfig` instance with the Speech SDK. Make sure the region matches your Azure Speech resource.
- Use the region as part of the endpoint URI when making requests to the Speech REST APIs.
- Keys are region-scoped — using a key with a different region returns authentication errors.

> [!NOTE]
> Azure Speech stores and processes speech data in the region where you create your resource. For Voice Live, this region doesn't determine the model inference location. Model inference follows the selected global, data zone, or regional deployment. See [Voice Live region support](./regions.md?tabs=voice-live#regions).

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

| Region | Real-time transcription<sup>1</sup> | Fast transcription | Batch transcription<sup>1</sup> | Whisper via batch transcription | Whisper via Azure OpenAI | Custom speech training<sup>2</sup> | Monolingual post-stream refinement | Multilingual post-stream refinement (preview) |
| ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| `australiaeast` | ✅ | ✅ | ✅ | ✅ | | ✅ | ✅ | |
| `brazilsouth` | ✅ | ✅ | ✅ | | | | ✅ | |
| `canadacentral` | ✅ | ✅ | ✅ | | | ✅ | ✅ | |
| `canadaeast` | ✅ | | ✅ | | | | | |
| `centralindia` | ✅ | ✅ | ✅ | | ✅ | ✅ | ✅ | ✅ |
| `centralus` | ✅ | | ✅ | | | | | |
| `eastasia` | ✅ | | ✅ | | | ✅ | | |
| `eastus` | ✅ | ✅ | ✅ | ✅ | | ✅ | ✅ | ✅ |
| `eastus2` | ✅ | ✅ | ✅ | | ✅ | ✅ | ✅ | |
| `francecentral` | ✅ | ✅ | ✅ | | | ✅ | ✅ | |
| `germanywestcentral` | ✅ | ✅ | ✅ | | | | ✅ | |
| `italynorth` | ✅ | ✅ | ✅ | | | | ✅ | |
| `japaneast` | ✅ | ✅ | ✅ | ✅ | | ✅ | ✅ | ✅ |
| `japanwest` | ✅ | ✅ | ✅ | | | | ✅ | |
| `koreacentral` | ✅ | ✅ | ✅ | | | ✅ | ✅ | |
| `northcentralus` | ✅ | ✅ | ✅ | | ✅ | | ✅ | |
| `northeurope` | ✅ | ✅ | ✅ | | | ✅ | ✅ | ✅ |
| `norwayeast` | ✅ | | ✅ | | ✅ | | | |
| `qatarcentral` | ✅ | | ✅ | | | | | |
| `southafricanorth` | ✅ | | ✅ | | | | | |
| `southcentralus` | ✅ | ✅ | ✅ | ✅ | | ✅ | ✅ | |
| `southeastasia` | ✅ | ✅ | ✅ | ✅ | | ✅ | ✅ | ✅ |
| `swedencentral` | ✅ | ✅ | ✅ | | ✅ | | ✅ | |
| `switzerlandnorth` | ✅ | | ✅ | | ✅ | ✅ | | |
| `switzerlandwest` | ✅ | | ✅ | | | | | |
| `uaenorth` | ✅ | | ✅ | | | | | |
| `uksouth` | ✅ | ✅ | ✅ | ✅ | | ✅ | ✅ | |
| `ukwest` | ✅ | | ✅ | | | | | |
| `westcentralus` | ✅ | | ✅ | | | | | |
| `westeurope` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | | |
| `westus` | ✅ | ✅ | ✅ | | | ✅ | ✅ | ✅ |
| `westus2` | ✅ | ✅ | ✅ | | | ✅ | ✅ | |
| `westus3` | ✅ | ✅ | ✅ | | | ✅ | ✅ | |

<sup>1</sup> Supports the processing of custom speech models.

<sup>2</sup> The region uses dedicated hardware for custom speech training. If you plan to train a custom model, you must use one of the regions that have dedicated hardware. Then you can [copy the trained model](how-to-custom-speech-train-model.md#copy-a-model) to another region.

# [Text to speech](#tab/tts)

| Region | Neural text to speech | MAI voices | Batch synthesis API | HD voices | Azure OpenAI voices | Custom voice | Custom voice training | Custom voice high-performance endpoint | Custom voice HD endpoint | Personal voice | Voice conversion | Voices and styles in preview |
| ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| australiaeast | ✅ |  | ✅ |  |  | ✅ | ✅ | ✅ | ✅ |  |  |  |
| brazilsouth | ✅ |  | ✅ |  |  | ✅ |  | ✅ |  |  |  |  |
| canadacentral | ✅ | ✅ | ✅ | ✅ |  | ✅ |  |  |  |  |  |  |
| canadaeast | ✅ |  |  |  |  |  |  |  |  |  |  |  |
| centralindia | ✅ | ✅ | ✅ | ✅ |  | ✅ | ✅ | ✅ | ✅ |  |  |  |
| centralus | ✅ |  | ✅ |  |  | ✅ | ✅ | ✅ |  |  |  |  |
| eastasia | ✅ |  | ✅ |  |  | ✅ |  |  |  | ✅ |  |  |
| eastus | ✅ | ✅ | ✅ | ✅ |  | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| eastus2 | ✅ | ✅ | ✅ | ✅ |  | ✅ | ✅ | ✅ | ✅ | ✅ |  |  |
| francecentral | ✅ | ✅ | ✅ | ✅ |  | ✅ | ✅ |  |  |  |  |  |
| germanywestcentral | ✅ |  | ✅ |  |  | ✅ |  |  |  |  |  |  |
| italynorth | ✅ |  | ✅ |  |  | ✅ |  | ✅ |  |  |  |  |
| japaneast | ✅ |  | ✅ |  |  | ✅ | ✅ | ✅ | ✅ |  |  |  |
| japanwest | ✅ |  |  |  |  | ✅ |  |  |  |  |  |  |
| koreacentral | ✅ |  | ✅ |  |  | ✅ | ✅ | ✅ | ✅ |  |  |  |
| northcentralus | ✅ |  | ✅ |  | ✅ | ✅ | ✅ | ✅ |  |  |  |  |
| northeurope | ✅ |  | ✅ |  |  | ✅ | ✅ | ✅ | ✅ |  |  |  |
| norwayeast | ✅ |  | ✅ |  |  | ✅ |  |  |  |  |  |  |
| qatarcentral | ✅ |  |  |  |  |  |  |  |  |  |  |  |
| southafricanorth | ✅ |  | ✅ |  |  | ✅ |  |  |  |  |  |  |
| southcentralus | ✅ |  | ✅ |  |  | ✅ | ✅ | ✅ |  |  |  |  |
| southeastasia | ✅ | ✅ | ✅ | ✅ |  | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| swedencentral | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |  |  |
| switzerlandnorth | ✅ |  | ✅ |  |  | ✅ |  |  |  |  |  |  |
| switzerlandwest | ✅ |  |  |  |  | ✅ |  |  |  |  |  |  |
| uaenorth | ✅ |  | ✅ |  |  | ✅ |  |  |  |  |  |  |
| uksouth | ✅ |  | ✅ |  |  | ✅ | ✅ | ✅ | ✅ |  |  |  |
| ukwest | ✅ |  |  |  |  |  |  |  |  |  |  |  |
| westcentralus | ✅ |  |  |  |  | ✅ |  |  |  |  |  |  |
| westeurope | ✅ | ✅ | ✅ | ✅ |  | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| westus | ✅ |  | ✅ |  |  | ✅ | ✅ | ✅ | ✅ |  |  |  |
| westus2 | ✅ | ✅ | ✅ | ✅ |  | ✅ | ✅ | ✅ | ✅ | ✅ |  |  |
| westus3 | ✅ |  |  |  |  | ✅ | ✅ | ✅ |  |  |  |  |

# [Text-to-speech avatar](#tab/ttsavatar)

| Region | Real-time avatar | Batch avatar | Custom avatar | Custom video avatar training|Custom photo avatar creation|Voice sync for avatar|
| ----- | ----- | ----- | ----- | ----- | ----- |----- |
| `westus2` | ✅ | ✅ | ✅ | ✅ | ✅| ✅|
| `eastus` | ✅ | ✅ | ✅ |  | ✅| ✅|
| `eastus2` | ✅ | ✅ | ✅ | | ✅| ✅|
| `southcentralus` | ✅ | ✅ | ✅ | | ✅|
| `southeastasia` | ✅ | ✅ | ✅ | ✅ | ✅| ✅|
| `centralindia` | ✅ | ✅ | ✅ |  | ✅|
| `westeurope` | ✅ | ✅ | ✅ | ✅ | ✅| ✅|
| `swedencentral` | ✅ | ✅ | ✅ | | ✅| ✅|
| `northeurope` | ✅ | ✅ | ✅ | | ✅|
| `italynorth` | ✅ | ✅ | ✅ |  | ✅|
| `francecentral`<sup>1</sup> | ✅ | ✅ | ✅ |  | ✅|

<sup>1</sup> Francecentral has limited capacity.

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

| Region | Transcribe | Translate | Transcribe with MAI-Transcribe |
| ----- | ----- | ----- | ----- |
| `centralindia` | ✅ | ✅ | ✅ |
| `eastus` | ✅ | ✅ | ✅ |
| `northeurope` | ✅ | ✅ | ✅ |
| `southeastasia` | ✅ | ✅ | ✅ |
| `westus` | ✅ | ✅ | ✅ |
| `westus2` | ✅ | ✅ | ✅ |

# [Voice Live](#tab/voice-live)

The following table lists model availability by Voice Live resource region. Each model cell shows the data processing (inference) scope: Global, Data zone, or Regional. A dash (`-`) means the model isn't available in that resource region.

| Voice Live resource region | azure-realtime | gpt-realtime-2.1 | gpt-realtime-2.1-datazone | gpt-realtime-2.1-regional | gpt-realtime-2.1-mini | gpt-realtime-1.5 | gpt-realtime-1.5-datazone | gpt-realtime | gpt-realtime-datazone | gpt-realtime-regional | gpt-realtime-mini | gpt-4o | gpt-4o-mini | gpt-4.1 | gpt-4.1-mini | gpt-4.1-nano | gpt-5.6-terra | gpt-5.6-luna | gpt-5.4 | gpt-5.2 | gpt-5.1 | gpt-5 | gpt-5-mini | gpt-5-nano | phi4-mm-realtime (preview) |
| ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| `australiaeast` | Global | Global | - | - | Global | Global | - | Global | - | - | Global | Global | Global | Global | Global | Global | Global | Global | Global | Global | Global | Global | Global | Global | - |
| `brazilsouth` | - | - | - | - | - | - | - | - | - | - | - | Global | Global | Global | Global | Global | Global | Global | Global | Global | Global | Global | Global | Global | - |
| `canadacentral` | Global | Global | - | - | Global | Global | - | Global | - | - | Global | - | - | Global | Regional | Global | Global | Global | Global | Global | Global | Global | Global | Global | - |
| `canadaeast` | Global | Global | - | - | Global | Global | - | Global | - | - | - | - | - | Global | Regional | Global | Global | Global | Global | Global | Global | Global | Global | Global | - |
| `centralindia` | Global | Global | - | Regional | Global | Global | - | Global | - | Regional | Global | Regional | Global | Global | Regional | Global | Global | Global | Global | Global | Global | Global | Global | Global | - |
| `centralus` | Global | Global | Data zone | - | Global | Global | Data zone | Global | - | - | Global | Data zone | Data zone | Data zone | Data zone | Data zone | Data zone | Data zone | Data zone | Data zone | Data zone | Data zone | Data zone | Data zone | - |
| `eastus` | - | Global | Data zone | - | Global | - | Data zone | - | - | - | - | Data zone | Data zone | Data zone | Data zone | Data zone | Data zone | Data zone | Data zone | Global | Data zone | Data zone | Data zone | Data zone | - |
| `eastus2` | Global | Global | Data zone | - | Global | Global | Data zone | Global | - | - | Global | Regional | Data zone | Regional | Regional | Data zone | Data zone | Data zone | Data zone | Data zone | Data zone | Data zone | Data zone | Data zone | Regional |
| `francecentral` | Global | Global | - | - | Global | Global | Data zone | Global | Data zone | - | Global | Data zone | Data zone | Data zone | Data zone | Data zone | Data zone | Data zone | Global | Global | Data zone | Data zone | Data zone | Data zone | - |
| `germanywestcentral` | - | - | - | - | - | - | - | - | - | - | - | - | - | Data zone | Data zone | Data zone | Data zone | Data zone | Global | Global | Global | Data zone | Data zone | Data zone | - |
| `italynorth` | - | - | - | - | - | - | - | - | - | - | - | Data zone | Data zone | Data zone | Data zone | Data zone | Data zone | Data zone | Global | Global | Global | Data zone | Data zone | Data zone | - |
| `japaneast` | Global | Global | - | - | Global | - | - | - | - | - | - | Regional | Global | Global | Global | Global | Global | Global | Global | Global | Global | Global | Global | Global | Regional |
| `japanwest` | - | - | - | - | - | - | - | - | - | - | - | Regional | Global | Global | Global | Global | Global | Global | - | Global | Global | Global | Global | Global | - |
| `koreacentral` | - | - | - | - | - | - | - | - | - | - | - | Global | Global | Global | Global | Global | Global | Global | Global | Global | Global | Global | Global | Global | - |
| `northcentralus` | - | Global | Data zone | - | Global | - | Data zone | - | - | - | - | Data zone | Data zone | Data zone | Data zone | Data zone | Data zone | Data zone | Data zone | Global | Data zone | Data zone | Data zone | Data zone | - |
| `norwayeast` | - | - | - | - | - | - | - | - | - | - | - | Global | Global | Global | Global | Global | Data zone | Data zone | Global | Global | Global | Global | Global | Global | - |
| `southafricanorth` | - | - | - | - | - | - | - | - | - | - | - | Global | Global | Global | Global | Global | Global | Global | Global | Global | Global | Global | Global | Global | - |
| `southcentralus` | - | - | Data zone | - | - | - | - | - | - | - | - | Data zone | Data zone | Data zone | Data zone | Data zone | Data zone | Data zone | Data zone | Global | Data zone | Data zone | Data zone | Data zone | - |
| `southeastasia` | Global | Global | - | - | Global | Global | - | Global | - | - | Global | - | - | Global | Global | Global | Global | Global | Global | Global | Global | Global | Global | Global | Regional |
| `swedencentral` | Global | Global | Data zone | - | Global | Global | Data zone | Global | Data zone | - | Global | Data zone | Data zone | Regional | Regional | Data zone | Data zone | Data zone | Global | Global | Data zone | Data zone | Data zone | Data zone | Regional |
| `switzerlandnorth` | - | - | - | - | - | - | - | - | - | - | - | Global | Global | Regional | Global | Global | Data zone | Data zone | Global | Global | Global | Global | Global | Global | - |
| `uaenorth` | - | - | - | - | - | - | - | - | - | - | - | Global | Global | Global | Global | Global | Global | Global | Global | Global | Global | Global | Global | Global | - |
| `uksouth` | Global | Global | - | - | Global | Global | - | Global | - | - | Global | Global | Global | Global | Global | Global | Global | Global | Global | Global | Global | Global | Global | Global | - |
| `westcentralus` | - | - | Data zone | - | - | - | - | - | - | - | - | - | - | - | - | - | Data zone | Data zone | - | Global | Global | - | - | - | - |
| `westeurope` | - | - | - | - | - | - | - | - | - | - | - | Data zone | Data zone | Data zone | Data zone | Data zone | Data zone | Data zone | Global | Global | Global | Data zone | Data zone | Data zone | - |
| `westus` | - | - | Data zone | - | - | - | - | - | - | - | - | Data zone | Data zone | Data zone | Data zone | Data zone | Data zone | Data zone | Data zone | Global | Data zone | Data zone | Data zone | Data zone | - |
| `westus2` | Global | Global | Data zone | - | Global | Global | Data zone | Global | - | - | Global | Data zone | Regional | Data zone | Data zone | Data zone | Data zone | Data zone | Data zone | Global | Regional | Data zone | Data zone | Data zone | Regional |
| `westus3` | - | - | Data zone | - | - | - | - | - | - | - | - | Data zone | Data zone | Data zone | Data zone | Data zone | Data zone | Data zone | Data zone | Global | Data zone | Data zone | Data zone | Data zone | - |

> [!NOTE]
> The `gpt-realtime-datazone`, `gpt-realtime-1.5-datazone`, and `gpt-realtime-2.1-datazone` models use data zone processing. Prompts and responses are processed only within the data zone associated with your resource's region.

> [!NOTE]
> Models `gpt-5.5`, `gpt-5.4-mini` and `gpt-5.4-nano` are supported and tested with Voice Live but aren't pre-deployed. To use them, deploy them in your Foundry resource and connect via [Bring Your Own Model (BYOM)](./how-to-bring-your-own-model.md).

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
