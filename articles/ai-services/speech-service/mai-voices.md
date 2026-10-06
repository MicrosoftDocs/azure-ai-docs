---
title: MAI-Voice-2.1 and MAI-Voice-2.1-Flash - Speech Service
titleSuffix: Foundry Tools
description: Learn how to use the MAI-Voice-2.1 and MAI-Voice-2.1-Flash text to speech models via Azure Speech API.
ms.service: azure-speech-foundry-tools
ms.topic: how-to
ms.date: 09/30/2026
ms.custom: references_regions
zone_pivot_groups: llm-speech-quickstart
ai-usage: ai-assisted

# Customer intent: As a developer who implements text to speech, I want to synthesize natural, expressive speech with MAI's latest MAI-Voice-2.1 and MAI-Voice-2.1-Flash models.
---

# MAI-Voice in Azure Speech

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

MAI-Voice-2.1 produces natural, expressive speech from text or a short reference clip, with built-in guardrails ensuring only authorized, consented voices can be used. It delivers stable, high-fidelity output that preserves speaker consistency across audiobooks, podcasts, and lectures in 23 different languages.

The following models are supported:

- `MAI-Voice-2.1`
- `MAI-Voice-2.1-Flash`

| Model | Voice Count | Key Characteristics | Best For |
| --- | --- | --- | --- |
| MAI-Voice-2.1-Flash | Prebuilt voices across 23 languages | Ultra-fast low-latency, emotionally rich, highly expressive, multilingual, supports 23 languages, instant voice cloning (gated), fine-grained emotion control via SSML | Real-time voice agents and assistants, low-latency call center/IVR flows, multilingual interactive experiences |
| MAI-Voice-2.1 | Prebuilt voices across 23 languages | Emotionally rich, highly expressive, high-fidelity, multilingual, supports 23 languages, instant voice cloning (gated), long-form generation with speaker consistency, fine-grained emotion control via SSML | Expressive long-form content, educational content, audiobooks/podcasts, voice overs |

## Model details

# [MAI-Voice-2.1-Flash](#tab/mai-voice-2-1-flash)

MAI‑Voice‑2.1‑Flash is a text‑to‑speech model built for fast, low‑latency generation. It produces high‑fidelity, natural, and expressive speech across 23 languages and supports gated instant voice cloning, all while being optimized for real‑time responsiveness. Its human‑like intonation, rhythm, and emotional nuance make it ideal for voice agents, assistants, and other interactive scenarios where latency and cost are critical.

You can integrate with MAI-Voice-2.1-Flash using the Azure Speech SDK via SSML, and also via [Voice Live](/azure/ai-services/speech-service/voice-live-how-to#audio-output-through-azure-text-to-speech).

### Key features

| Key features | Description |
| --- | --- |
| Ultra-fast low-latency synthesis | Built for real-time text-to-speech with very low latency, suitable for interactive voice scenarios. |
| High-fidelity natural synthesis | Produces natural, expressive, emotionally rich, and high-clarity voice output with human-like rhythm and intonation. |
| Multilingual support | Supports synthesis across 23 languages. |
| Emotion and style control | Developers can influence speaking style by using SSML with `mstts:express-as` and `style`, enabling control over emotions such as `joy`, `excitement`, `empathy`, and more. |
| Voice prompting with instant cloning (gated) | Matches a consented reference voice from a short audio clip (5-60 seconds) without additional training. |
| Voice library | Includes licensed curated voices across the supported languages that work out of the box for rapid deployment. |
| Real-time agent optimization | Optimized for voice agents, assistants, IVR, and call-center interactions where responsiveness is critical. |

### SSML example

[!INCLUDE [MAI Voice 2.1 Flash SSML](./includes/quickstarts/text-to-speech-basics/mai-voice-ssml-flash.md)]

# [MAI-Voice-2.1](#tab/mai-voice-2-1)

MAI‑Voice‑2.1 is the highest‑fidelity, most expressive text‑to‑speech model in the MAI-Voice family, delivering rich, natural speech across 23 languages. It extends the MAI‑Voice family with broad multilingual coverage, gated instant voice cloning, and strong long‑form generation capabilities. With its detailed prosody, nuanced expressiveness, and studio‑grade audio quality, MAI‑Voice‑2.1 is ideal for experiences where maximum voice quality and fidelity are required, such as long‑form narration and brand‑defining audio.

### Key features

| Key features | Description |
| --- | --- |
| High-fidelity natural synthesis | Produces natural, expressive, emotionally rich, and high-clarity voice output with human-like rhythm and intonation. |
| Multilingual support | Supports synthesis across 23 languages. |
| Emotion and style control | Developers can influence speaking style by using SSML with `mstts:express-as` and `style`, enabling control over emotions such as `joy`, `excitement`, `empathy`, and more. |
| Voice prompting with instant cloning (gated) | Matches a consented reference voice from a short audio clip (5-60 seconds) without additional training. |
| Voice library | Includes licensed curated voices across the supported languages that work out of the box for rapid deployment. |
| High fidelity audio | The model produces high-quality speech with natural prosody and clarity suitable for production-grade applications. |
| Long-form generation | Optimized for long-form narration with stable persona quality and speaker consistency across extended content. |
| Out-of-scope note | The model prioritizes naturalness and expressivity over latency-critical scenarios. |

### SSML example

[!INCLUDE [MAI Voice 2.1 SSML](./includes/quickstarts/text-to-speech-basics/mai-voice-ssml.md)]

---

## Prerequisites

> [!div class="checklist"]
> - An Azure subscription. You can [create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
> - [A Microsoft Foundry resource for Speech](https://portal.azure.com/#create/Microsoft.CognitiveServicesAIFoundry) in the Azure portal.
> - The Speech resource key and region. After your Speech resource is deployed, select **Go to resource** to view and manage keys. For the current list of supported regions, see [Speech service regions](regions.md?tabs=llmspeech).

## Availability and regions

You can access MAI-Voice-2.1 and MAI-Voice-2.1-Flash globally. Azure serves the models from the following regions, and routes requests to them:

| Region | Region identifier | Availability |
| --- | --- | --- |
| France Central | `francecentral` | Available |
| East Asia | `eastasia` | Available |
| Southeast Asia | `southeastasia` | Available |
| East US | `eastus` | Available |
| Canada Central | `canadacentral` | Available |
| East US 2 | `eastus2` | Available |
| West US | `westus` | Available |
| West Europe | `westeurope` | Available |
| North Europe | `northeurope` | Available |
| West US 2 | `westus2` | Available |
| West US 3 | `westus3` | Available |
| Central India | `centralindia` | Available |
| Sweden Central | `swedencentral` | Available |
| Japan East | `japaneast` | Available |

## Pricing

Find pricing information at [https://azure.microsoft.com/pricing/details/speech/](https://azure.microsoft.com/pricing/details/speech/).

Usage: Available for third-party developers. Microsoft holds full licensing rights for commercial use.

## Choose your preferred usage method

MAI-Voice models use the same Azure Speech API and SDK as other Azure neural and HD voices. Choose a portal, API, or SDK tab, and use a MAI-Voice name in the SSML `voice` element. For available names, see [Managed voices and styles](#managed-voices-and-styles).

::: zone pivot="ai-foundry"

# [MAI-Voice-2.1-Flash](#tab/mai-voice-2-1-flash)

[!INCLUDE [MAI Voice Foundry portal Flash](./includes/quickstarts/text-to-speech-basics/mai-voice-ai-foundry-flash.md)]

# [MAI-Voice-2.1](#tab/mai-voice-2-1)

[!INCLUDE [MAI Voice Foundry portal](./includes/quickstarts/text-to-speech-basics/mai-voice-ai-foundry.md)]

---

::: zone-end

::: zone pivot="programming-language-rest"

# [MAI-Voice-2.1-Flash](#tab/mai-voice-2-1-flash)

[!INCLUDE [MAI Voice REST API Flash](./includes/quickstarts/text-to-speech-basics/mai-voice-rest-flash.md)]

# [MAI-Voice-2.1](#tab/mai-voice-2-1)

[!INCLUDE [MAI Voice REST API](./includes/quickstarts/text-to-speech-basics/mai-voice-rest.md)]

---

::: zone-end

::: zone pivot="programming-language-python"

# [MAI-Voice-2.1-Flash](#tab/mai-voice-2-1-flash)

[!INCLUDE [MAI Voice Python SDK Flash](./includes/quickstarts/text-to-speech-basics/mai-voice-python-flash.md)]

# [MAI-Voice-2.1](#tab/mai-voice-2-1)

[!INCLUDE [MAI Voice Python SDK](./includes/quickstarts/text-to-speech-basics/mai-voice-python.md)]

---

::: zone-end

::: zone pivot="programming-language-csharp"

# [MAI-Voice-2.1-Flash](#tab/mai-voice-2-1-flash)

[!INCLUDE [MAI Voice C# SDK Flash](./includes/quickstarts/text-to-speech-basics/mai-voice-csharp-flash.md)]

# [MAI-Voice-2.1](#tab/mai-voice-2-1)

[!INCLUDE [MAI Voice C# SDK](./includes/quickstarts/text-to-speech-basics/mai-voice-csharp.md)]

---

::: zone-end

<!-- markdownlint-disable-next-line MD044 -->
::: zone pivot="programming-language-javascript"

# [MAI-Voice-2.1-Flash](#tab/mai-voice-2-1-flash)

[!INCLUDE [MAI Voice JavaScript SDK Flash](./includes/quickstarts/text-to-speech-basics/mai-voice-javascript-flash.md)]

# [MAI-Voice-2.1](#tab/mai-voice-2-1)

[!INCLUDE [MAI Voice JavaScript SDK](./includes/quickstarts/text-to-speech-basics/mai-voice-javascript.md)]

---

::: zone-end

::: zone pivot="programming-language-java"

# [MAI-Voice-2.1-Flash](#tab/mai-voice-2-1-flash)

[!INCLUDE [MAI Voice Java SDK Flash](./includes/quickstarts/text-to-speech-basics/mai-voice-java-flash.md)]

# [MAI-Voice-2.1](#tab/mai-voice-2-1)

[!INCLUDE [MAI Voice Java SDK](./includes/quickstarts/text-to-speech-basics/mai-voice-java.md)]

---

::: zone-end

## Custom voice - Personal Voice/Instant Voice Cloning (gated access)

Developers can create a custom voice in Microsoft Foundry across all supported languages by using just a short reference clip, with no retraining or fine-tuning required. By using only a few seconds of audio (recommended: 5-60 seconds), MAI-Voice models generate high-quality speech that matches the speaker's identity, making it easy for companies to bring their own brand voice into products without maintaining a separate voice model.

All MAI-Voice models support Instant Voice Cloning. Only authorized, licensed voices can be synthesized in production. No unlicensed voice cloning is possible. To gain access to this feature:

1. Apply for gated access through Azure AI Custom Neural Voice and Custom Avatar [Limited Access Review](https://aka.ms/customneural).
2. Once approved, access personal voice APIs at cognitive-services-speech-sdk/samples/custom-voice.
3. Upload audio consent and prompt to create a personal voice.
4. Synthesize text by using the created voice and a MAI-Voice model. Select a model tab for the corresponding SSML.

# [MAI-Voice-2.1-Flash](#tab/mai-voice-2-1-flash)

[!INCLUDE [MAI Voice 2.1 Flash personal voice](./includes/quickstarts/text-to-speech-basics/mai-voice-personal-voice-flash.md)]

# [MAI-Voice-2.1](#tab/mai-voice-2-1)

[!INCLUDE [MAI Voice 2.1 personal voice](./includes/quickstarts/text-to-speech-basics/mai-voice-personal-voice.md)]

---

## Prebuilt voices

### Managed voices and styles

All managed voices in the following table support both `MAI-Voice-2.1` and `MAI-Voice-2.1-Flash`. Use the complete voice ID with the selected model suffix in SSML. For example, use `en-US-Harper:MAI-Voice-2.1` or `en-US-Harper:MAI-Voice-2.1-Flash`.

| Voice ID | Locale | Language | Gender | Supported models | Supported styles |
| --- | --- | --- | --- | --- | --- |
| `cs-CZ-Grant` | `cs-CZ` | Czech | Male | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `agent`, `audiobook`, `customer_call_center`, `educational`, `narrator`, `neutral` |
| `cs-CZ-Harper` | `cs-CZ` | Czech | Female | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `agent`, `audiobook`, `customer_call_center`, `educational`, `narrator`, `neutral` |
| `da-DK-Grant` | `da-DK` | Danish | Male | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `agent`, `customer_call_center`, `educational`, `narrator`, `neutral` |
| `da-DK-Harper` | `da-DK` | Danish | Female | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `agent`, `audiobook`, `customer_call_center`, `educational`, `narrator`, `neutral` |
| `de-DE-Grant` | `de-DE` | German | Male | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `agent`, `audiobook`, `customer_call_center`, `educational`, `narrator`, `neutral` |
| `de-DE-Harper` | `de-DE` | German | Female | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `agent`, `audiobook`, `customer_call_center`, `educational`, `narrator`, `neutral` |
| `de-DE-Klaus` | `de-DE` | German (Germany) | Male | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `angry`, `confused`, `determined`, `disgusted`, `embarrassed`, `excited`, `fearful`, `happy`, `hopeful`, `jealous`, `joyful`, `neutral`, `regretful`, `relieved`, `sad`, `shouting`, `softvoice`, `surprised`, `whispering` |
| `de-DE-Mia` | `de-DE` | German (Germany) | Female | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `angry`, `confused`, `determined`, `disgusted`, `embarrassed`, `excited`, `fearful`, `happy`, `hopeful`, `jealous`, `joyful`, `neutral`, `regretful`, `relieved`, `sad`, `shouting`, `softvoice`, `surprised`, `whispering` |
| `en-AU-Isla` | `en-AU` | English (Australia) | Female | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `angry`, `confused`, `determined`, `disgusted`, `embarrassed`, `excited`, `fearful`, `happy`, `hopeful`, `jealous`, `joyful`, `neutral`, `regretful`, `relieved`, `sad`, `shouting`, `softvoice`, `surprised`, `whispering` |
| `en-GB-Emily` | `en-GB` | English (United Kingdom) | Female | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `agent`, `angry`, `audiobook`, `confused`, `customer_call_center`, `disgusted`, `educational`, `embarrassed`, `excited`, `fearful`, `happy`, `jealous`, `joyful`, `narrator`, `neutral`, `sad`, `surprised` |
| `en-GB-Harry` | `en-GB` | English (United Kingdom) | Male | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `agent`, `angry`, `audiobook`, `customer_call_center`, `disgusted`, `educational`, `fearful`, `joyful`, `narrator`, `neutral`, `sad`, `surprised` |
| `en-IN-Dhruv` | `en-IN` | English (India) | Male | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `neutral` |
| `en-IN-Priya` | `en-IN` | English (India) | Female | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `neutral` |
| `en-US-Ethan` | `en-US` | English (United States) | Male | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `angry`, `confused`, `determined`, `disgusted`, `embarrassed`, `excited`, `fearful`, `happy`, `hopeful`, `jealous`, `joyful`, `neutral`, `regretful`, `relieved`, `sad`, `shouting`, `softvoice`, `surprised`, `whispering` |
| `en-US-Grant` | `en-US` | English (United States) | Male | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `agent`, `audiobook`, `customer_call_center`, `educational`, `narrator`, `neutral` |
| `en-US-Harper` | `en-US` | English (United States) | Female | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `agent`, `angry`, `audiobook`, `confused`, `customer_call_center`, `determined`, `educational`, `embarrassed`, `excited`, `happy`, `hopeful`, `joyful`, `narrator`, `neutral`, `regretful`, `relieved`, `sad`, `shouting`, `softvoice`, `whispering` |
| `en-US-Iris` | `en-US` | English (United States) | Female | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `neutral` |
| `en-US-Jasper` | `en-US` | English (United States) | Male | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `neutral` |
| `en-US-Olivia` | `en-US` | English (United States) | Female | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `angry`, `confused`, `determined`, `disgusted`, `embarrassed`, `excited`, `fearful`, `happy`, `hopeful`, `jealous`, `joyful`, `neutral`, `regretful`, `relieved`, `sad`, `shouting`, `softvoice`, `surprised`, `whispering` |
| `en-US-Sage` | `en-US` | English (United States) | Male | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `agent`, `audiobook`, `customer_call_center`, `educational`, `narrator`, `neutral` |
| `es-ES-Marta` | `es-ES` | Spanish (Spain) | Female | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `adventurous`, `caringempathy`, `curious`, `encouraging`, `excited`, `friendlycheerful`, `neutral`, `nostalgic`, `reflective`, `saddisappointed`, `serious` |
| `es-MX-Alejo` | `es-MX` | Spanish (Mexico) | Male | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `angry`, `confused`, `determined`, `disgusted`, `embarrassed`, `excited`, `fearful`, `happy`, `hopeful`, `jealous`, `joyful`, `neutral`, `regretful`, `relieved`, `sad`, `shouting`, `softvoice`, `surprised`, `whispering` |
| `es-MX-Grant` | `es-MX` | Spanish (Mexico) | Male | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `neutral` |
| `es-MX-Harper` | `es-MX` | Spanish (Mexico) | Female | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `agent`, `audiobook`, `customer_call_center`, `educational`, `narrator`, `neutral` |
| `es-MX-Valeria` | `es-MX` | Spanish (Mexico) | Female | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `angry`, `confused`, `determined`, `disgusted`, `embarrassed`, `excited`, `fearful`, `happy`, `hopeful`, `jealous`, `joyful`, `neutral`, `regretful`, `relieved`, `sad`, `shouting`, `softvoice`, `surprised`, `whispering` |
| `fi-FI-Grant` | `fi-FI` | Finnish | Male | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `neutral` |
| `fi-FI-Harper` | `fi-FI` | Finnish | Female | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `agent`, `audiobook`, `customer_call_center`, `educational`, `narrator`, `neutral` |
| `fr-FR-Grant` | `fr-FR` | French | Male | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `neutral` |
| `fr-FR-Harper` | `fr-FR` | French | Female | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `agent`, `audiobook`, `customer_call_center`, `educational`, `narrator`, `neutral` |
| `fr-FR-Marc` | `fr-FR` | French (France) | Male | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `angry`, `confused`, `determined`, `disgusted`, `embarrassed`, `excited`, `fearful`, `happy`, `hopeful`, `jealous`, `joyful`, `neutral`, `regretful`, `relieved`, `sad`, `shouting`, `softvoice`, `surprised`, `whispering` |
| `fr-FR-Soleil` | `fr-FR` | French (France) | Female | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `angry`, `confused`, `determined`, `disgusted`, `embarrassed`, `excited`, `fearful`, `happy`, `hopeful`, `jealous`, `joyful`, `neutral`, `regretful`, `relieved`, `sad`, `shouting`, `softvoice`, `surprised`, `whispering` |
| `hi-IN-Arjun` | `hi-IN` | Hindi (India) | Male | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `angry`, `confused`, `disgusted`, `embarrassed`, `excited`, `fearful`, `happy`, `hopeful`, `jealous`, `joyful`, `neutral`, `regretful`, `sad`, `surprised` |
| `hi-IN-Dhruv` | `hi-IN` | Hindi (India) | Male | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `angry`, `confused`, `determined`, `disgusted`, `embarrassed`, `excited`, `fearful`, `happy`, `hopeful`, `jealous`, `joyful`, `neutral`, `regretful`, `relieved`, `sad`, `shouting`, `softvoice`, `surprised`, `whispering` |
| `hi-IN-Grant` | `hi-IN` | Hindi | Male | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `audiobook`, `neutral` |
| `hi-IN-Harper` | `hi-IN` | Hindi | Female | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `agent`, `customer_call_center`, `educational`, `narrator`, `neutral` |
| `hi-IN-Kavya` | `hi-IN` | Hindi (India) | Female | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `angry`, `confused`, `determined`, `disgusted`, `embarrassed`, `excited`, `fearful`, `happy`, `hopeful`, `jealous`, `joyful`, `neutral`, `regretful`, `relieved`, `sad`, `shouting`, `softvoice`, `surprised`, `whispering` |
| `hi-IN-Priya` | `hi-IN` | Hindi (India) | Female | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `angry`, `confused`, `determined`, `disgusted`, `embarrassed`, `excited`, `fearful`, `happy`, `hopeful`, `jealous`, `joyful`, `neutral`, `regretful`, `relieved`, `sad`, `shouting`, `softvoice`, `surprised`, `whispering` |
| `hu-HU-Bence` | `hu-HU` | Hungarian (Hungary) | Male | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `neutral` |
| `hu-HU-Grant` | `hu-HU` | Hungarian | Male | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `neutral` |
| `hu-HU-Harper` | `hu-HU` | Hungarian | Female | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `agent`, `audiobook`, `customer_call_center`, `educational`, `narrator`, `neutral` |
| `hu-HU-Levente` | `hu-HU` | Hungarian (Hungary) | Male | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `neutral` |
| `hu-HU-Lilla` | `hu-HU` | Hungarian (Hungary) | Female | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `neutral` |
| `hu-HU-Reka` | `hu-HU` | Hungarian (Hungary) | Female | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `neutral` |
| `id-ID-Grant` | `id-ID` | Indonesian | Male | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `agent`, `audiobook`, `customer_call_center`, `educational`, `narrator`, `neutral` |
| `id-ID-Harper` | `id-ID` | Indonesian | Female | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `neutral` |
| `it-IT-Grant` | `it-IT` | Italian | Male | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `audiobook`, `educational`, `neutral` |
| `it-IT-Harper` | `it-IT` | Italian | Female | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `agent`, `customer_call_center`, `narrator`, `neutral` |
| `it-IT-Luca` | `it-IT` | Italian (Italy) | Male | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `angry`, `confused`, `determined`, `disgusted`, `embarrassed`, `excited`, `fearful`, `happy`, `hopeful`, `jealous`, `joyful`, `neutral`, `regretful`, `relieved`, `sad`, `shouting`, `softvoice`, `surprised`, `whispering` |
| `it-IT-Rosa` | `it-IT` | Italian (Italy) | Female | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `angry`, `confused`, `determined`, `disgusted`, `embarrassed`, `excited`, `fearful`, `happy`, `hopeful`, `jealous`, `joyful`, `neutral`, `regretful`, `relieved`, `sad`, `shouting`, `softvoice`, `surprised`, `whispering` |
| `ko-KR-Grant` | `ko-KR` | Korean | Male | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `agent`, `audiobook`, `customer_call_center`, `educational`, `narrator`, `neutral` |
| `ko-KR-Haena` | `ko-KR` | Korean (Korea) | Female | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `angry`, `confused`, `determined`, `embarrassed`, `excited`, `happy`, `hopeful`, `joyful`, `neutral`, `regretful`, `relieved`, `sad`, `softvoice`, `surprised` |
| `ko-KR-Harper` | `ko-KR` | Korean | Female | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `agent`, `audiobook`, `customer_call_center`, `educational`, `narrator`, `neutral` |
| `ko-KR-Junho` | `ko-KR` | Korean (Korea) | Male | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `angry`, `confused`, `determined`, `embarrassed`, `excited`, `happy`, `hopeful`, `joyful`, `neutral`, `relieved`, `sad`, `softvoice` |
| `nb-NO-Grant` | `nb-NO` | Norwegian (Bokmål) | Male | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `educational`, `neutral` |
| `nb-NO-Harper` | `nb-NO` | Norwegian (Bokmål) | Female | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `agent`, `audiobook`, `customer_call_center`, `narrator`, `neutral` |
| `nl-NL-Grant` | `nl-NL` | Dutch | Male | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `agent`, `customer_call_center`, `educational`, `narrator`, `neutral` |
| `nl-NL-Harper` | `nl-NL` | Dutch | Female | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `agent`, `audiobook`, `customer_call_center`, `educational`, `narrator`, `neutral` |
| `nl-NL-Sander` | `nl-NL` | Dutch (Netherlands) | Male | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `adventurous`, `caringempathy`, `curious`, `encouraging`, `excited`, `friendlycheerful`, `neutral`, `nostalgic`, `reflective`, `saddisappointed`, `serious` |
| `pl-PL-Grant` | `pl-PL` | Polish | Male | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `neutral` |
| `pl-PL-Harper` | `pl-PL` | Polish | Female | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `agent`, `audiobook`, `customer_call_center`, `educational`, `narrator`, `neutral` |
| `pt-BR-Caio` | `pt-BR` | Portuguese (Brazil) | Male | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `angry`, `confused`, `determined`, `disgusted`, `embarrassed`, `excited`, `fearful`, `happy`, `hopeful`, `jealous`, `joyful`, `neutral`, `regretful`, `relieved`, `sad`, `shouting`, `softvoice`, `surprised`, `whispering` |
| `pt-BR-Grant` | `pt-BR` | Portuguese (Brazil) | Male | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `agent`, `customer_call_center`, `educational`, `neutral` |
| `pt-BR-Harper` | `pt-BR` | Portuguese (Brazil) | Female | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `audiobook`, `narrator`, `neutral` |
| `pt-BR-Luana` | `pt-BR` | Portuguese (Brazil) | Female | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `angry`, `confused`, `determined`, `disgusted`, `embarrassed`, `excited`, `fearful`, `happy`, `hopeful`, `jealous`, `joyful`, `neutral`, `regretful`, `relieved`, `sad`, `shouting`, `softvoice`, `surprised`, `whispering` |
| `pt-BR-Pedro` | `pt-BR` | Portuguese (Brazil) | Male | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `confused`, `determined`, `embarrassed`, `excited`, `happy`, `hopeful`, `joyful`, `neutral`, `regretful`, `relieved`, `sad`, `softvoice`, `surprised` |
| `pt-BR-Rafael` | `pt-BR` | Portuguese (Brazil) | Male | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `angry`, `confused`, `determined`, `embarrassed`, `excited`, `happy`, `hopeful`, `joyful`, `neutral`, `regretful`, `relieved`, `sad`, `softvoice`, `surprised` |
| `pt-PT-Grant` | `pt-PT` | Portuguese (Portugal) | Male | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `neutral` |
| `pt-PT-Harper` | `pt-PT` | Portuguese (Portugal) | Female | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `neutral` |
| `pt-PT-Rui` | `pt-PT` | Portuguese (Portugal) | Male | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `angry`, `confused`, `determined`, `embarrassed`, `excited`, `happy`, `hopeful`, `joyful`, `neutral`, `regretful`, `relieved`, `sad`, `softvoice`, `surprised` |
| `ro-RO-Andrei` | `ro-RO` | Romanian (Romania) | Male | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `neutral` |
| `ro-RO-Elena` | `ro-RO` | Romanian (Romania) | Female | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `neutral` |
| `ro-RO-Grant` | `ro-RO` | Romanian | Male | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `agent`, `customer_call_center`, `educational`, `narrator`, `neutral` |
| `ro-RO-Harper` | `ro-RO` | Romanian | Female | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `audiobook`, `neutral` |
| `ro-RO-Ioana` | `ro-RO` | Romanian (Romania) | Female | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `neutral` |
| `ro-RO-Radu` | `ro-RO` | Romanian (Romania) | Male | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `neutral` |
| `ru-RU-Grant` | `ru-RU` | Russian | Male | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `agent`, `customer_call_center`, `neutral` |
| `ru-RU-Harper` | `ru-RU` | Russian | Female | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `audiobook`, `educational`, `narrator`, `neutral` |
| `ru-RU-Lev` | `ru-RU` | Russian (Russia) | Male | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `adventurous`, `caringempathy`, `curious`, `encouraging`, `excited`, `friendlycheerful`, `neutral`, `nostalgic`, `reflective`, `saddisappointed`, `serious` |
| `ru-RU-Masha` | `ru-RU` | Russian (Russia) | Female | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `adventurous`, `caringempathy`, `curious`, `encouraging`, `excited`, `friendlycheerful`, `neutral`, `nostalgic`, `reflective`, `saddisappointed`, `serious` |
| `sv-SE-Grant` | `sv-SE` | Swedish | Male | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `neutral` |
| `sv-SE-Harper` | `sv-SE` | Swedish | Female | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `agent`, `audiobook`, `customer_call_center`, `educational`, `narrator`, `neutral` |
| `th-TH-Grant` | `th-TH` | Thai | Male | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `agent`, `audiobook`, `customer_call_center`, `educational`, `narrator`, `neutral` |
| `th-TH-Harper` | `th-TH` | Thai | Female | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `agent`, `audiobook`, `customer_call_center`, `educational`, `narrator`, `neutral` |
| `th-TH-Krit` | `th-TH` | Thai | Female | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `adventurous`, `caringempathy`, `curious`, `encouraging`, `excited`, `friendlycheerful`, `neutral`, `nostalgic`, `reflective`, `saddisappointed`, `serious` |
| `th-TH-Nattapong` | `th-TH` | Thai | Male | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `adventurous`, `caringempathy`, `curious`, `encouraging`, `excited`, `friendlycheerful`, `neutral`, `nostalgic`, `reflective`, `saddisappointed`, `serious` |
| `tr-TR-Aydin` | `tr-TR` | Turkish (Türkiye) | Male | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `adventurous`, `caringempathy`, `curious`, `encouraging`, `excited`, `friendlycheerful`, `neutral`, `nostalgic`, `reflective`, `saddisappointed`, `serious` |
| `tr-TR-Elif` | `tr-TR` | Turkish (Türkiye) | Female | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `adventurous`, `caringempathy`, `curious`, `encouraging`, `excited`, `friendlycheerful`, `neutral`, `nostalgic`, `reflective`, `saddisappointed`, `serious` |
| `tr-TR-Grant` | `tr-TR` | Turkish | Male | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `educational`, `narrator`, `neutral` |
| `tr-TR-Harper` | `tr-TR` | Turkish | Female | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `agent`, `audiobook`, `customer_call_center`, `neutral` |
| `vi-VN-Grant` | `vi-VN` | Vietnamese | Male | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `agent`, `customer_call_center`, `educational`, `narrator`, `neutral` |
| `vi-VN-Harper` | `vi-VN` | Vietnamese | Female | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `audiobook`, `neutral` |
| `zh-CN-Bo` | `zh-CN` | Chinese (Simplified) | Male | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `angry`, `confused`, `determined`, `disgusted`, `embarrassed`, `excited`, `fearful`, `happy`, `hopeful`, `jealous`, `joyful`, `neutral`, `regretful`, `relieved`, `sad`, `shouting`, `softvoice`, `surprised`, `whispering` |
| `zh-CN-Grant` | `zh-CN` | Chinese (Simplified) | Male | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `agent`, `audiobook`, `customer_call_center`, `educational`, `narrator`, `neutral` |
| `zh-CN-Harper` | `zh-CN` | Chinese (Simplified) | Female | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `agent`, `audiobook`, `customer_call_center`, `educational`, `narrator`, `neutral` |
| `zh-CN-Lan` | `zh-CN` | Chinese (Simplified) | Female | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `angry`, `confused`, `disgusted`, `embarrassed`, `excited`, `fearful`, `happy`, `joyful`, `neutral`, `sad`, `surprised` |
| `zh-CN-Mei` | `zh-CN` | Chinese (Simplified) | Female | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `angry`, `confused`, `determined`, `disgusted`, `embarrassed`, `excited`, `fearful`, `happy`, `hopeful`, `jealous`, `joyful`, `neutral`, `regretful`, `relieved`, `sad`, `shouting`, `softvoice`, `surprised`, `whispering` |
| `zh-CN-Wei` | `zh-CN` | Chinese (Simplified) | Male | `MAI-Voice-2.1`, `MAI-Voice-2.1-Flash` | `angry`, `confused`, `disgusted`, `embarrassed`, `excited`, `fearful`, `happy`, `hopeful`, `jealous`, `joyful`, `neutral`, `regretful`, `sad`, `surprised` |

> [!NOTE]
> Microsoft adds more locales and managed voices as they become available.

---

## Related content

- For more information about using LLM Speech API, see [LLM Speech API](llm-speech.md).
- [MAI-Transcribe in Azure Speech](mai-transcribe.md).
- [How to customize Voice Live input and output](./voice-live-how-to-customize.md).
