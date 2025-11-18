---
title: Content Understanding region and language support
titleSuffix: Foundry Tools
description: Azure Content Understanding in Foundry Tools region and language support
author: PatrickFarley 
ms.author: pafarley
manager: nitinme
ms.date: 05/19/2025
ms.service: azure-ai-content-understanding
ms.topic: reference
ms.custom:
  - references_regions
  - ignite-2024-understanding-release
  - build-2025
---

# Azure Content Understanding in Foundry Tools region and language support

Azure Content Understanding in Foundry Tools provides multilingual support in multiple geographic regions to enable users to communicate with Content Understanding applications in natural ways and empower global outreach. The following sections describe the available regions and supported languages/locales.

## Region support

To use Azure Content Understanding, create your Foundry Tool resource in a supported region. All data at rest is stored in the selected region. For lower latency or increased capacity, you can specify the processing location where analysis occurs. Content Understanding is available in the following regions. When the processing location is set to `geography` or `data zone`, the corresponding locations are shown.

| Identifier      | Region         | Geography       | Data Zone        |
|-----------------|----------------|-----------------|------------------|
| `australiaeast` | Australia East | Australia | Australia |
| `eastus` | East US | United States | US |
| `eastus2` | East US 2 | United States | US |
| `japaneast` | Japan East | Japan | Asia |
| `northeurope` | North Europe | Europe | Europe |
| `southcentralus` | South Central US | United States | US |
| `southeastasia` | Southeast Asia | Asia Pacific | Asia |
| `swedencentral` | Sweden Central | Sweden | Europe |
| `uksouth` | UK South | United Kingdom | UK |
| `westeurope` | West Europe | Europe | Europe |
| `westus` | West US | United States | US |
| `westus3` | West US 3 | United States | US |


> [!NOTE]
>
> [Pro mode (preview)](concepts/standard-pro-modes.md) currently only supports data zone and global as processing location.

## Language support

Azure Content Understanding enables you to process data in multiple languages simultaneously. Our language support capabilities enable users to communicate with your applications in natural ways and empower global outreach.

Content Understanding applies [Azure OpenAI models](../../ai-foundry/openai/overview.md) which support a wide array of languages. While there's no definitive list of supported languages, users can expect robust language capabilities across most common languages. For specific language support related to `OCR` and speech transcription, refer to the respective sections detailing the supported languages for these modalities.

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

Content Understanding applies Azure Speech in Foundry Tools [fast transcription](../speech-service/speech-to-text.md#fast-transcription) to transcribe spoken words in the input synchronously and faster than real-time audio. 

Content Understanding supports the full set of languages/locales supported by fast transcription. See the Fast transcription column here - [Azure Speech Regions](../speech-service/regions.md?tabs=stt).

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

## Preview API (2025-05-01-preview)

The preview API version `2025-05-01-preview` includes managed capacity for generative capabilities and has limited regional availability compared to the GA version.

### Region support

To use Azure Content Understanding in Foundry Tools with the preview API, create your Foundry Tool resource in a supported region. All data at rest is stored in the selected region. For lower latency or increased capacity, you can specify the processing location where analysis occurs. Content Understanding preview API is available in the following regions. When the processing location is set to `geography` or `data zone`, the corresponding locations are shown.

| Identifier      | Region         | Geography       | Data Zone        |
|-----------------|----------------|-----------------|------------------|
| `westus` | West US | United States | United States |
| `swedencentral` | Sweden Central | Sweden | European Union |
| `australiaeast` | Australia East | Australia | N/A<sup>†</sup> |

<sup>†</sup> Australia East doesn't support data zone as a processing location.

> [!NOTE]
>
> [Pro mode (preview)](concepts/standard-pro-modes.md) currently only supports data zone and global as processing location.
