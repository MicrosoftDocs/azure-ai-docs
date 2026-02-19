---
title: Sovereign Clouds - Speech service
titleSuffix: Foundry Tools
description: Learn how to use Sovereign Clouds
author: PatrickFarley
ms.author: pafarley
manager: nitinme
ms.service: azure-ai-speech
ms.topic: how-to
ms.custom: references_regions
ms.date: 08/07/2025
ms.reviewer: jagoerge
#Customer intent: As a developer, I want to learn how to use Speech service in sovereign clouds.
---

# Speech service in sovereign clouds

## Azure Government (United States)

Available to US government entities and their partners only. See more information about Azure Government [here](/azure/azure-government/documentation-government-welcome) and [here.](/azure/azure-government/compare-azure-government-global-azure)

- **Azure portal:**
  - [https://portal.azure.us/](https://portal.azure.us/)
- **Regions:**
  - US Gov Arizona
  - US Gov Virginia
- **Available pricing tiers:**
  - Free (F0) and Standard (S0). See more details [here](https://azure.microsoft.com/pricing/details/cognitive-services/speech-services/)
- **Supported features:**
  - [Speech Studio](https://speech.azure.us/)
  - Speech to text
    - Real-time transcription
    - Batch transcription
    - Language ID
    - Speaker diarization
    - Custom speech
  - Text to speech
    - Standard voice
    - Neural voice
  - Speech translation
    - Real-time speech translation
  - Keyword recognition
- **Unsupported features:**
    - Custom voice
    - Personal voice
    - Text to speech avatar
    - Fast transcription
    - Pronunciation assessment
    - Custom keyword
    - Voice Live
    - Live interpreter
    - Video translation
    - LLM speech
- **Supported languages:**
  - Same as public clouds. See the list of supported languages [here](language-support.md)

### Endpoint information

This section contains Speech service endpoint information for the usage with [Speech SDK](speech-sdk.md), [Speech to text REST API](rest-speech-to-text.md), and [Text to speech REST API](rest-text-to-speech.md).

#### Speech service REST API

Speech service REST API endpoints in Azure Government have the following format:

|  REST API type / operation | Endpoint format |
|--|--|
| Access token | `https://<REGION_IDENTIFIER>.api.cognitive.microsoft.us/sts/v1.0/issueToken`
| [Speech to text REST API](rest-speech-to-text.md) | `https://<REGION_IDENTIFIER>.api.cognitive.microsoft.us/<URL_PATH>` |
| [Speech to text REST API for short audio](rest-speech-to-text-short.md) | `https://<REGION_IDENTIFIER>.stt.speech.azure.us/<URL_PATH>` |
| [Text to speech REST API](rest-text-to-speech.md) | `https://<REGION_IDENTIFIER>.tts.speech.azure.us/<URL_PATH>` |

Replace `<REGION_IDENTIFIER>` with the identifier matching the region of your Speech resource from this table:

|                     | Region identifier |
|--|--|
| **US Gov Arizona**  | `usgovarizona` |
| **US Gov Virginia** | `usgovvirginia` |

#### Speech SDK

For [Speech SDK](speech-sdk.md) in sovereign clouds, you need to use "from endpoint / with endpoint" instantiation of `SpeechConfig` class or `--endpoint` option of [Speech CLI](spx-overview.md). 

`SpeechConfig` class should be instantiated like this:

# [C#](#tab/c-sharp)
```csharp
var config = SpeechConfig.Endpoint(new Uri(usGovEndpoint), subscriptionKey);
```
# [C++](#tab/cpp)
```cpp
auto config = SpeechConfig::FromEndpoint(usGovEndpoint, subscriptionKey);
```
# [Java](#tab/java)
```java
SpeechConfig config = SpeechConfig.fromEndpoint(new java.net.URI(usGovEndpoint), subscriptionKey);
```
# [Python](#tab/python)
```python
import azure.cognitiveservices.speech as speechsdk
speech_config = speechsdk.SpeechConfig(endpoint=usGovEndpoint, subscription=subscriptionKey)
```
# [Objective-C](#tab/objective-c)
```objectivec
SPXSpeechConfiguration *speechConfig = [[SPXSpeechConfiguration alloc] initWithEndpoint:usGovEndpoint subscription:subscriptionKey];
```
***

Speech CLI should be used like this (note the `--endpoint` option):
```dos
spx recognize --endpoint "usGovEndpoint" --file myaudio.wav
```

Replace `subscriptionKey` with your Speech resource key.
Replace `usGovEndpoint` with the endpoint from the Azure portal.

## Microsoft Azure operated by 21Vianet

Available to organizations with a business presence in China. See more information about Microsoft Azure operated by 21Vianet [here](/azure/china/overview-operations). 

- **Azure portal:**
  - [https://portal.azure.cn/](https://portal.azure.cn/)
- **Regions:**
  - China East 2
  - China North 2
  - China North 3
- **Available pricing tiers:**
  - Free (F0) and Standard (S0). See more details [here](https://www.azure.cn/pricing/details/cognitive-services/index.html)
- **Supported features:**
  - [Speech Studio](https://speech.azure.cn/)
  - Speech to text
    - Real-time transcription
    - Batch transcription
    - Language ID
    - Speaker diarization
    - Custom speech
  - Pronunciation assessment
  - Text to speech
    - Standard voice
    - Neural voice
  - Speech translation
    - Real-time speech translation
  - Keyword recognition
- **Unsupported features:**
    - Custom voice
    - Personal voice
    - Text to speech avatar
    - Custom keyword
    - Voice Live
    - Live interpreter
    - Video translation
    - LLM speech
- **Supported languages:**
  - Same as public clouds. See the list of supported languages [here](language-support.md)

### Endpoint information

This section contains Speech service endpoint information for the usage with [Speech SDK](speech-sdk.md), [Speech to text REST API](rest-speech-to-text.md), and [Text to speech REST API](rest-text-to-speech.md).

#### Speech service REST API

Speech service REST API endpoints in Azure operated by 21Vianet have the following format:

|  REST API type / operation | Endpoint format |
|--|--|
| Access token | `https://<REGION_IDENTIFIER>.api.cognitive.azure.cn/sts/v1.0/issueToken`
| [Speech to text REST API](rest-speech-to-text.md) | `https://<REGION_IDENTIFIER>.api.cognitive.azure.cn/<URL_PATH>` |
| [Speech to text REST API for short audio](rest-speech-to-text-short.md) | `https://<REGION_IDENTIFIER>.stt.speech.azure.cn/<URL_PATH>` |
| [Text to speech REST API](rest-text-to-speech.md) | `https://<REGION_IDENTIFIER>.tts.speech.azure.cn/<URL_PATH>` |

Replace `<REGION_IDENTIFIER>` with the identifier matching the region of your Speech resource from this table:

|                     | Region identifier |
|--|--|
| **China East 2**  | `chinaeast2` |
| **China North 2**  | `chinanorth2` |
| **China North 3**  | `chinanorth3` |

#### Speech SDK

For [Speech SDK](speech-sdk.md) in sovereign clouds, you need to use "from endpoint / with endpoint" instantiation of `SpeechConfig` class or `--endpoint` option of [Speech CLI](spx-overview.md). 

`SpeechConfig` class should be instantiated like this:

# [C#](#tab/c-sharp)
```csharp
var config = SpeechConfig.Endpoint(new Uri(azCnEndpoint), subscriptionKey);
```
# [C++](#tab/cpp)
```cpp
auto config = SpeechConfig::FromEndpoint(azCnEndpoint, subscriptionKey);
```
# [Java](#tab/java)
```java
SpeechConfig config = SpeechConfig.fromEndpoint(new java.net.URI(azCnEndpoint), subscriptionKey);
```
# [Python](#tab/python)
```python
import azure.cognitiveservices.speech as speechsdk
speech_config = speechsdk.SpeechConfig(endpoint=azCnEndpoint, subscription=subscriptionKey)
```
# [Objective-C](#tab/objective-c)
```objectivec
SPXSpeechConfiguration *speechConfig = [[SPXSpeechConfiguration alloc] initWithEndpoint:azCnEndpoint subscription:subscriptionKey];
```
***

Speech CLI should be used like this (note the `--endpoint` option):
```dos
spx recognize --endpoint "azCnEndpoint" --file myaudio.wav
```

Replace `subscriptionKey` with your Speech resource key. Replace `azCnEndpoint` with the endpoint from the Azure portal.
