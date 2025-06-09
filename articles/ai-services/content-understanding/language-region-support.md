---
title: Content Understanding region and language support
titleSuffix: Azure AI services
description: Azure AI Content Understanding region and language support
author: laujan
ms.author: lajanuar
manager: nitinme
ms.date: 05/19/2025
ms.service: azure-ai-content-understanding
ms.topic: reference
ms.custom:
  - references_regions
  - ignite-2024-understanding-release
  - build-2025
---

# Azure AI Content Understanding region and language support

Azure AI Content Understanding provides multilingual support in multiple geographic regions to enable users to communicate with Content Understanding applications in natural ways and empower global outreach. The following sections describe the available regions and supported languages/locales.

## Region support

To use Azure AI Content Understanding, create your Azure AI Service resource in a supported region. All data at rest is stored in the selected region. For lower latency or increased capacity, you can specify the processing location where analysis occurs. Content Understanding is available in the following regions. When the processing location is set to `geography` or `data zone`, the corresponding locations are shown.

| Identifier      | Region         | Geography       | Data Zone        |
|-----------------|----------------|-----------------|------------------|
| `westus`        | West US        | United States   | United States    |
| `swedencentral` | Sweden Central | Sweden          | European Union   |
| `australiaeast` | Australia East | Australia       | N/A †            |

† Australia East doesn't support data zone as a processing location.

> [!NOTE]
>
> [Pro mode](concepts/standard-pro-modes.md) currently only supports data zone and global as processing location.

## Language support

Azure AI Content Understanding enables you to process data in multiple languages simultaneously. Our language support capabilities enable users to communicate with your applications in natural ways and empower global outreach.

Content Understanding applies [Azure OpenAI models](../openai/overview.md) which support a wide array of languages. While there's no definitive list of supported languages, users can expect robust language capabilities across most common languages. For specific language support related to `OCR` and speech transcription, refer to the respective sections detailing the supported languages for these modalities.

### Text optical character recognition (OCR)

> [!IMPORTANT]
>
> * The following list of supported languages have locale-aware normalization for words enabled in post-processing.
> * Content Understanding supports different languages so we encourage you to try it out and focus on the content and not the value itself.

|**Language**| **Language code**|**Language**| **Language code**|
|:-----|:-----|:-----|:-----|
|Afrikaans|`af`|Kazakh (Latin)|`kk, kk-latn`|
|Albanian|`sq`|Khaling|`klr`|
|Angika|`anp`|Khasi|`kha`|
|Arabic|`ar`|Kirghiz|`ky`|
|Asturian|`ast`|Korean|`ko`|
|Awadhi|`awa`|Korku|`kfq`|
|Azerbaijani|`az`|Koryak|`kpy`|
|Bagheli|`bfy`|Kosraean|`kos`|
|Basque|`eu`|Kurdish (Arabic)|`ku-arab`|
|Belarusian (Cyrillic)|`be, be-cyrl`|Kurdish (Latin)|`ku, ku-latn`|
|Belarusian (Latin)|`be-latn`|Kurukh|`kru`|
|Bhojpuri|`bho`|Kölsch|`ksh`|
|Bislama|`bi`|Lakota|`lkt`|
|Bodo|`brx`|Latin|`la`|
|Bosnian|`bs`|Lithuanian|`lt`|
|Braj|`bra`|Lower Sorbian|`dsb`|
|Breton|`br`|Volapük|`smj`|
|Bulgarian|`bg`|Luxembourgish|`lb`|
|Bundeli|`bns`|Mahasu Pahari|`bfz`|
|Buriat|`bua`|Malay|`ms`|
|Camling|`rab`|Malto|`kmj`|
|Catalan|`ca`|Manx|`gv`|
|Cebuano|`ceb`|Maori|`mi`|
|Chamorro|`ch`|Marathi|`mr`|
|Chhattisgarhi|`hne`|Mongolian|`mn`|
|Chinese (Simplified)|`zh, zh-hans`|Montenegrin (Cyrillic)|`cnr-cyrl`|
|Chinese (Traditional)|`zh-hant`|Montenegrin (Latin)|`cnr, cnr-latn`|
|Cornish|`kw`|Neapolitan|`nap`|
|Corsican|`co`|Nepali|`ne`|
|Crimean Tatar|`crh`|Niuean|`niu`|
|Croatian|`hr`|Nogai|`nog`|
|Czech|`cs`|Northern Sami|`sme`|
|Danish|`da`|Norwegian|`no`|
|Dari|`prs`|Occitan|`oc`|
|Dhimal|`dhi`|Ossetian|`os`|
|Dogri|`doi`|Panjabi|`pa`|
|Dutch|`nl`|Persian|`fa`|
|English|`en-US, en-AU, en-CA,en-GB, en-IN`|Polish|`pl`|
|Erzya|`myv`|Portuguese|`pt`|
|Estonian|`et`|Pushto|`ps`|
|Faroese|`fo`|Romanian|`ro`|
|Fijian|`fj`|Romansh|`rm`|
|Filipino|`fil`|Russian|`ru`|
|Finnish|`fi`|Sadri|`sck`|
|French|`fr`|Samoan|`sm`|
|Friulian|`fur`|Sanskrit|`sa`|
|Gagauz|`gag`|Santali|`sat`|
|Galician|`gl`|Scots|`sco`|
|German|`de`|Scottish Gaelic|`gd`|
|Gilbertese|`gil`|Serbian (Latin)|`sr, sr-latn`|
|Gondi|`gon`|Sirmauri|`srx`|
|Gurung|`gvr`|Skolt Sami|`sms`|
|Haitian|`ht`|Slovak|`sk`|
|Halbi|`hlb`|Slovenian|`sl`|
|Hani|`hni`|Somali|`so`|
|Haryanvi|`bgc`|Southern Sami|`sma`|
|Hawaiian|`haw`|Spanish|`es`|
|Hindi|`hi`|Swahili|`sw`|
|Hmong Daw|`mww`|Swedish|`sv`|
|Ho|`hoc`|Tajik|`tg`|
|Hungarian|`hu`|Tatar|`tt`|
|Icelandic|`is`|Tetum|`tet`|
|Inari Sami|`smn`|Thangmi|`thf`|
|Indonesian|`id`|Thai|`th`|
|Interlingua|`ia`|Tonga|`to`|
|Inuktitut|`iu`|Turkish|`tr`|
|Irish|`ga`|Tuvinian|`tyv`|
|Italian|`it`|Uighur|`ug`|
|Japanese|`ja`|Upper Sorbian|`hsb`|
|Jaunsari|`jns`|Urdu|`ur`|
|Javanese|`jv`|Uzbek (Arabic)|`uz-arab`|
|K'iche'|`quc`|Uzbek (Cyrillic)|`uz-cyrl`|
|Kabuverdianu|`kea`|Uzbek (Latin)|`uz, uz-latn`|
|Kachin|`kac`|Volapük|`vo`|
|Kalaallisut|`kl`|Walser|`wae`|
|Kangri|`xnr`|Welsh|`cy`|
|Kara-Kalpak (Cyrillic)|`kaa-cyrl`|Western Frisian|`fy`|
|Kara-Kalpak (Latin)|`kaa, kaa-latn`|Yucateco|`yua`|
|Karachay-Balkar|`krc`|Zhuang|`za`|
|Kashubian|`csb`|Zulu|`zu`|
|Kazakh (Cyrillic)|`kk-cyrl`|||

The following table lists the supported languages/locales for **handwritten** text.

|**Language**| **Language code**|**Language**| **Language code**|
|:-----|:----:|:-----|:----:|
|English|`en`|Japanese  |`ja`|
|Chinese Simplified   |`zh-Hans`|Korean |`ko`|
|French  |`fr`|Portuguese |`pt`|
|German  |`de`|Spanish  |`es`|
|Italian  |`it`| Russian  | `ru` |
|Thai  | `th` | Arabic  | `ar` |


### Speech transcription

Content Understanding applies [Azure AI speech to text](../speech-service/speech-to-text.md) to transcribe spoken words in the input. For a subset of supported languages, it uses [fast transcription](../speech-service/speech-to-text.md#fast-transcription) to reduce processing latency.

The following table lists the supported languages/locales for fast transcription.

|**Language**| **Language code**|**Language**| **Language code**|
|:-----|:----:|:-----|:----:|
| Chinese (Mandarin, Simplified) | `zh-CN` | Indonesian (Indonesia) | `id-ID` |
| Danish (Denmark) | `da-DK` | Italian (Italy) | `it-IT` |
| English (India) | `en-IN` | Japanese (Japan) | `ja-JP` |
| English (United Kingdom) | `en-GB` | Korean (Korea) | `ko-KR` |
| English (United States) | `en-US` | Polish (Poland) | `pl-PL` |
| Finnish (Finland) | `fi-FI` | Portuguese (Brazil) | `pt-BR` |
| French (France) | `fr-FR` | Portuguese (Portugal) | `pt-PT` |
| German (Germany) | `de-DE` | Spanish (Mexico) | `es-MX` |
| Hebrew (Israel) | `he-IL` | Spanish (Spain) | `es-ES` |
| Hindi (India) | `hi-IN` | Swedish (Sweden) | `sv-SE` |

The following table lists all supported languages/locales.

|**Language**| **Language code**|**Language**| **Language code**|
|:-----|:----:|:-----|:----:|
| Afrikaans (South Africa) | `af-ZA` | Hungarian (Hungary) | `hu-HU` |
| Albanian (Albania) | `sq-AL` | Icelandic (Iceland) | `is-IS` |
| Amharic (Ethiopia) | `am-ET` | Indonesian (Indonesia) | `id-ID` |
| Arabic (Algeria) | `ar-DZ` | Irish (Ireland) | `ga-IE` |
| Arabic (Bahrain) | `ar-BH` | isiZulu (South Africa) | `zu-ZA` |
| Arabic (Egypt) | `ar-EG` | Italian (Italy) | `it-IT` |
| Arabic (Iraq) | `ar-IQ` | Italian (Switzerland) | `it-CH` |
| Arabic (Israel) | `ar-IL` | Japanese (Japan) | `ja-JP` |
| Arabic (Jordan) | `ar-JO` | Javanese (Latin, Indonesia) | `jv-ID` |
| Arabic (Kuwait) | `ar-KW` | Kannada (India) | `kn-IN` |
| Arabic (Lebanon) | `ar-LB` | Kazakh (Kazakhstan) | `kk-KZ` |
| Arabic (Libya) | `ar-LY` | Khmer (Cambodia) | `km-KH` |
| Arabic (Morocco) | `ar-MA` | Kiswahili (Kenya) | `sw-KE` |
| Arabic (Oman) | `ar-OM` | Kiswahili (Tanzania) | `sw-TZ` |
| Arabic (Palestinian Authority) | `ar-PS` | Korean (Korea) | `ko-KR` |
| Arabic (Qatar) | `ar-QA` | Lao (Laos) | `lo-LA` |
| Arabic (Saudi Arabia) | `ar-SA` | Latvian (Latvia) | `lv-LV` |
| Arabic (Syria) | `ar-SY` | Lithuanian (Lithuania) | `lt-LT` |
| Arabic (Tunisia) | `ar-TN` | Macedonian (North Macedonia) | `mk-MK` |
| Arabic (United Arab Emirates) | `ar-AE` | Malay (Malaysia) | `ms-MY` |
| Arabic (Yemen) | `ar-YE` | Malayalam (India) | `ml-IN` |
| Armenian (Armenia) | `hy-AM` | Maltese (Malta) | `mt-MT` |
| Assamese (India) | `as-IN` | Marathi (India) | `mr-IN` |
| Azerbaijani (Latin, Azerbaijan) | `az-AZ` | Mongolian (Mongolia) | `mn-MN` |
| Basque | `eu-ES` | Nepali (Nepal) | `ne-NP` |
| Bengali (India) | `bn-IN` | Norwegian Bokmål (Norway) | `nb-NO` |
| Bosnian (Bosnia and Herzegovina) | `bs-BA` | Odia (India) | `or-IN` |
| Bulgarian (Bulgaria) | `bg-BG` | Pashto (Afghanistan) | `ps-AF` |
| Burmese (Myanmar) | `my-MM` | Persian (Iran) | `fa-IR` |
| Catalan | `ca-ES` | Polish (Poland) | `pl-PL` |
| Chinese (Cantonese, Simplified) | `yue-CN` | Portuguese (Brazil) | `pt-BR` |
| Chinese (Cantonese, Traditional) | `zh-HK` | Portuguese (Portugal) | `pt-PT` |
| Chinese (Jilu Mandarin, Simplified) | `zh-CN-shandong` | Punjabi (India) | `pa-IN` |
| Chinese (Mandarin, Simplified) | `zh-CN` | Romanian (Romania) | `ro-RO` |
| Chinese (Southwestern Mandarin, Simplified) | `zh-CN-sichuan` | Russian (Russia) | `ru-RU` |
| Chinese (Taiwanese Mandarin, Traditional) | `zh-TW` | Serbian (Cyrillic, Serbia) | `sr-RS` |
| Chinese (Wu, Simplified) | `wuu-CN` | Sinhala (Sri Lanka) | `si-LK` |
| Croatian (Croatia) | `hr-HR` | Slovak (Slovakia) | `sk-SK` |
| Czech (Czechia) | `cs-CZ` | Slovenian (Slovenia) | `sl-SI` |
| Danish (Denmark) | `da-DK` | Somali (Somalia) | `so-SO` |
| Dutch (Belgium) | `nl-BE` | Spanish (Argentina) | `es-AR` |
| Dutch (Netherlands) | `nl-NL` | Spanish (Bolivia) | `es-BO` |
| English (Australia) | `en-AU` | Spanish (Chile) | `es-CL` |
| English (Canada) | `en-CA` | Spanish (Colombia) | `es-CO` |
| English (Ghana) | `en-GH` | Spanish (Costa Rica) | `es-CR` |
| English (Hong Kong SAR) | `en-HK` | Spanish (Cuba) | `es-CU` |
| English (India) | `en-IN` | Spanish (Dominican Republic) | `es-DO` |
| English (Ireland) | `en-IE` | Spanish (Ecuador) | `es-EC` |
| English (Kenya) | `en-KE` | Spanish (El Salvador) | `es-SV` |
| English (New Zealand) | `en-NZ` | Spanish (Equatorial Guinea) | `es-GQ` |
| English (Nigeria) | `en-NG` | Spanish (Guatemala) | `es-GT` |
| English (Philippines) | `en-PH` | Spanish (Honduras) | `es-HN` |
| English (Singapore) | `en-SG` | Spanish (Mexico) | `es-MX` |
| English (South Africa) | `en-ZA` | Spanish (Nicaragua) | `es-NI` |
| English (Tanzania) | `en-TZ` | Spanish (Panama) | `es-PA` |
| English (United Kingdom) | `en-GB` | Spanish (Paraguay) | `es-PY` |
| English (United States) | `en-US` | Spanish (Peru) | `es-PE` |
| Estonian (Estonia) | `et-EE` | Spanish (Puerto Rico) | `es-PR` |
| Filipino (Philippines) | `fil-PH` | Spanish (Spain) | `es-ES` |
| Finnish (Finland) | `fi-FI` | Spanish (United States)<sup>1</sup> | `es-US` |
| French (Belgium) | `fr-BE` | Spanish (Uruguay) | `es-UY` |
| French (Canada)<sup>1</sup> | `fr-CA` | Spanish (Venezuela) | `es-VE` |
| French (France) | `fr-FR` | Swedish (Sweden) | `sv-SE` |
| French (Switzerland) | `fr-CH` | Tamil (India) | `ta-IN` |
| Galician | `gl-ES` | Telugu (India) | `te-IN` |
| Georgian (Georgia) | `ka-GE` | Thai (Thailand) | `th-TH` |
| German (Austria) | `de-AT` | Turkish (Türkiye) | `tr-TR` |
| German (Germany) | `de-DE` | Ukrainian (Ukraine) | `uk-UA` |
| German (Switzerland) | `de-CH` | Urdu (India) | `ur-IN` |
| Greek (Greece) | `el-GR` | Uzbek (Latin, Uzbekistan) | `uz-UZ` |
| Gujarati (India) | `gu-IN` | Vietnamese (Vietnam) | `vi-VN` |
| Hebrew (Israel) | `he-IL` | Welsh (United Kingdom) | `cy-GB` |
| Hindi (India) | `hi-IN` |||


### Field value normalization

Different locales have different ways to represent numbers, date, and time. Content Understanding supports normalizing these different representations into standardized ISO forms for the following locales.

|**Language**| **Language code**|**Language**| **Language code**|
|:-----|:----:|:-----|:----:|
|Arabic|`ar-AE`, `ar-EG`, `ar-SA`|Japanese|`ja-JP`|
|Bengla|`bn-IN`|Korean|`ko-KR`|
|Bulgarian|`bg-BG`|Latvian|`lv-LV`|
|Catalan|`ca-ES`|Lithuanian|`lt-LT`|
|Chinese (Simplified) |`zh-CN`|Malay|`ms-MY`|
|Chinese (Traditional)|`zh-TW`|Marathi|`mr-IN`|
|Croatian|`hr-HR`|Nepali|`ne-IN`|
|Czech|`cs-CZ`|Norwegian|`no-NO`|
|Danish|`da-DK`|Polish|`pl-PL`|
|Dutch|`nl-NL`|Portuguese|`pt-BR`, `pt-PT`|
|English|`en-AU`, `en-CA`, `en-GB`, `en-IL`, `en-IN`, `en-MY`, `en-US`|Romanian|`ro-RO`|
|Estonian|`et-EE`|Russian|`ru-RU`|
|Finnish|`fi-FI`|Serbian|`sr-RS`|
|French|`fr-CA`, `fr-FR`|Slovak|`sk-SK`|
|Galician|`gl-ES`|Slovenian|`sl-SI`|
|German|`de-DE`|Spanish|`es-AR`, `es-ES`, `es-MX`|
|Greek|`el-GR`|Swedish|`sv-SE`|
|Hebrew|`he-IL`|Tamil|`ta-IN`|
|Hindi|`hi-IN`|Thai|`th-TH`|
|Hungarian|`hu-HU`|Turkish|`tr-TR`|
|Icelandic|`is-IS`|Ukrainian|`uk-UA`|
|Indonesian|`id-ID`|Vietnamese|`vi-VN`|
|Italian|`it-IT`|||

