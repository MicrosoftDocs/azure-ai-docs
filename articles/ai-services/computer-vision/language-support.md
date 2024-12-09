---
title: Language support - Azure AI Vision
titleSuffix: Azure AI services
description: This article provides a list of natural languages supported by Azure AI Vision features; OCR, Image analysis.
#services: cognitive-services
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-vision
ms.topic: conceptual
ms.date: 09/25/2024
ms.author: pafarley
---

# Language support for Azure AI Vision

Some capabilities of Azure AI Vision support multiple languages; any capabilities not mentioned here only support English.

## Optical Character Recognition (OCR)

The Azure AI Vision [Read API](./overview-ocr.md) supports many languages. The `Read` API can extract text from images and documents with mixed languages, including from the same text line, without requiring a language parameter. See [How to specify the `Read` model](./how-to/call-read-api.md#determine-how-to-process-the-data-optional) to use the new languages.

> [!NOTE]
> **Language code optional**
>
> `Read` OCR's deep-learning-based universal models extract all multi-lingual text in your documents, including text lines with mixed languages, and do not require specifying a language code. Do not provide the language code as the parameter unless you are sure about the language and want to force the service to apply only the relevant model. Otherwise, the service may return incomplete and incorrect text.

### Handwritten text

The following table lists the OCR supported languages for handwritten text by the most recent `Read` GA model.

|Language| Language code (optional) | Language| Language code (optional) |
|:-----|:----:|:-----|:----:|
|English|`en`|Japanese |`ja`|
|Chinese Simplified |`zh-Hans`|Korean|`ko`|
|French |`fr`|Portuguese |`pt`|
|German |`de`|Spanish |`es`|
|Italian |`it`|

### Print text

The following table lists the OCR supported languages for print text by the most recent `Read` GA model.

|Language| Code (optional) |Language| Code (optional) |
|:-----|:----:|:-----|:----:|
|Afrikaans|`af`|Khasi  | `kha` |
|Albanian |`sq`|K'iche'  | `quc` |
|Angika (Devanagiri) | `anp`| Korean | `ko` |
|Arabic | `ar` | Korku | `kfq`|
|Asturian |`ast`| Koryak | `kpy`|
|Awadhi-Hindi (Devanagiri) | `awa`| Kosraean | `kos`|
|Azerbaijani (Latin) | `az`| Kumyk (Cyrillic) | `kum`|
|Bagheli | `bfy`| Kurdish (Arabic) | `ku-arab`|
|Basque  |`eu`| Kurdish (Latin) | `ku-latn`
|Belarusian (Cyrillic)  | `be`, `be-cyrl`|Kurukh (Devanagiri) | `kru`|
|Belarusian (Latin) | `be`, `be-latn`| Kyrgyz (Cyrillic)  | `ky`
|Bhojpuri-Hindi (Devanagiri) | `bho`| Lakota | `lkt` |
|Bislama   |`bi`| Latin | `la` |
|Bodo (Devanagiri) | `brx`| Lithuanian | `lt` |
|Bosnian (Latin) | `bs`| Lower Sorbian | `dsb` |
|Brajbha | `bra`|Lule Sami | `smj`|
|Breton    |`br`|Luxembourgish  | `lb` |
|Bulgarian  | `bg`|Mahasu Pahari (Devanagiri) | `bfz`|
|Bundeli | `bns`|Malay (Latin) | `ms` |
|Buryat (Cyrillic) | `bua`|Maltese | `mt`
|Catalan    |`ca`|Malto (Devanagiri) | `kmj`
|Cebuano    |`ceb`|Manx  | `gv` |
|Chamling | `rab`|Maori | `mi`|
|Chamorro  |`ch`|Marathi | `mr`|
|Chhattisgarhi (Devanagiri)| `hne`| Mongolian (Cyrillic)  | `mn`|
|Chinese Simplified | `zh-Hans`|Montenegrin (Cyrillic)  | `cnr-cyrl`|
|Chinese Traditional | `zh-Hant`|Montenegrin (Latin) | `cnr-latn`|
|Cornish     |`kw`|Neapolitan   | `nap` |
|Corsican      |`co`|Nepali | `ne`|
|Crimean Tatar (Latin)|`crh`|Niuean | `niu`|
|Croatian | `hr`|Nogay | `nog`
|Czech | `cs` |Northern Sami (Latin) | `sme`|
|Danish | `da` |Norwegian | `no` |
|Dari | `prs`|Occitan | `oc` |
|Dhimal (Devanagiri) | `dhi`| Ossetic  | `os`|
|Dogri (Devanagiri) | `doi`|Pashto | `ps`|
|Dutch | `nl` |Persian | `fa`|
|English | `en` |Polish | `pl` |
|Erzya (Cyrillic) | `myv`|Portuguese | `pt` |
|Estonian  |`et`|Punjabi (Arabic) | `pa`|
|Faroese | `fo`|Ripuarian | `ksh`|
|Fijian |`fj`|Romanian | `ro` | 
|Filipino  |`fil`|Romansh  | `rm` |
|Finnish | `fi` | Russian | `ru` | 
|French | `fr` |Sadri  (Devanagiri) | `sck` | 
|Friulian  | `fur` | Samoan (Latin) | `sm`
|Gagauz (Latin) | `gag`|Sanskrit (Devanagari) | `sa`|
|Galician   | `gl` |Santali(Devanagiri) | `sat` | 
|German | `de` | Scots  | `sco` | 
|Gilbertese    | `gil` | Scottish Gaelic  | `gd` | 
|Gondi (Devanagiri) | `gon`| Serbian (Latin) | `sr`, `sr-latn`|
|Greenlandic   | `kl` | Sherpa (Devanagiri) | `xsr` |
|Gurung (Devanagiri) | `gvr`| Sirmauri (Devanagiri) | `srx`|
|Haitian Creole  | `ht` | Skolt Sami | `sms` | 
|Halbi (Devanagiri) | `hlb`| Slovak | `sk`|
|Hani  | `hni` | Slovenian  | `sl` | 
|Haryanvi | `bgc`|Somali (Arabic) | `so`|
|Hawaiian | `haw`|Southern Sami | `sma`
|Hindi | `hi`|Spanish | `es` |
|Hmong Daw (Latin)| `mww` | Swahili (Latin)  | `sw` |
|Ho(Devanagiri) | `hoc`|Swedish | `sv` |
|Hungarian | `hu` |Tajik (Cyrillic)  | `tg` |
|Icelandic | `is`| Tatar (Latin)  | `tt` |
|Inari Sami | `smn`|Tetum    | `tet` |
|Indonesian   | `id` | Thangmi | `thf` |
|Interlingua  | `ia` |Tongan | `to`| 
|Inuktitut (Latin) | `iu` | Turkish | `tr` | 
|Irish    | `ga` |Turkmen (Latin) | `tk`|
|Italian | `it` |Tuvan | `tyv`|
|Japanese | `ja` |Upper Sorbian  | `hsb` |
|Jaunsari (Devanagiri) | `Jns`|Urdu  | `ur`|
|Javanese | `jv` |Uyghur (Arabic) | `ug`|
|Kabuverdianu | `kea` |Uzbek (Arabic) | `uz-arab`|
|Kachin (Latin) | `kac` |Uzbek (Cyrillic)  | `uz-cyrl`|
|Kangri (Devanagiri) | `xnr`|Uzbek (Latin)     | `uz` |
|Karachay-Balkar  | `krc`|Volapük   | `vo` |
|Kara-Kalpak (Cyrillic) | `kaa-cyrl`|Walser    | `wae` |
|Kara-Kalpak (Latin) | `kaa` |Welsh | `cy` |
|Kashubian | `csb` |Western Frisian | `fy` |
|Kazakh (Cyrillic)  | `kk-cyrl`|Yucatec Maya | `yua` |
|Kazakh (Latin) | `kk-latn`|Zhuang | `za` |
|Khaling | `klr`|Zulu  | `zu` |

## Image Analysis

Some features of the [Analyze - Image](/rest/api/computervision/analyze-image?view=rest-computervision-v3.2) API can return results in other languages, specified with the `language` query parameter. Other features return results in English regardless of what language is specified, and others throw an exception for unsupported languages. Features are specified with the `visualFeatures` and `details` query parameters; see the [Overview](overview-image-analysis.md) for a list of all the actions you can do with the [Analyze - Image](/rest/api/computervision/analyze-image?view=rest-computervision-v3.2) API, or follow the [How-to guide](/azure/ai-services/computer-vision/how-to/call-analyze-image-40) to try them out.

| Language | Language code | Categories | Tags | Description | Adult, Brands, Color, Faces, ImageType, Objects | Celebrities, Landmarks | Captions, Dense captions|
|:---|:---:|:----:|:---:|:---:|:---:|:---:|:--:|
|Arabic |`ar`| | ✅| ||||
|Azerbaijani |`az`| | ✅| ||||
|Bulgarian |`bg`| | ✅| ||||
|Bosnian Latin |`bs`| | ✅| ||||
|Catalan |`ca`| | ✅| ||||
|Czech |`cs`| | ✅| ||||
|Welsh |`cy`| | ✅| ||||
|Danish |`da`| | ✅| ||||
|German |`de`| | ✅| ||||
|Greek |`el`| | ✅| ||||
|English |`en`|✅ | ✅| ✅|✅|✅|✅|
|Spanish |`es`|✅ | ✅| ✅||✅||
|Estonian |`et`| | ✅| ||||
|Basque |`eu`| | ✅| ||||
|Finnish |`fi`| | ✅| ||||
|French |`fr`| | ✅| ||||
|Irish |`ga`| | ✅| ||||
|Galician |`gl`| | ✅| ||||
|Hebrew |`he`| | ✅| ||||
|Hindi |`hi`| | ✅| ||||
|Croatian |`hr`| | ✅| ||||
|Hungarian |`hu`| | ✅| ||||
|Indonesian |`id`| | ✅| ||||
|Italian |`it`| | ✅| ||||
|Japanese  |`ja`|✅ | ✅| ✅||✅||
|Kazakh |`kk`| | ✅| ||||
|Korean |`ko`| | ✅| ||||
|Lithuanian |`lt`| | ✅| ||||
|Latvian |`lv`| | ✅| ||||
|Macedonian |`mk`| | ✅| ||||
|Malay  Malaysia |`ms`| | ✅| ||||
|Norwegian (Bokmal) |`nb`| | ✅| ||||
|Dutch |`nl`| | ✅| |||
|Polish |`pl`| | ✅| |||
|Dari |`prs`| | ✅| |||
| Portuguese-Brazil|`pt-BR`| | ✅| ||||
| Portuguese-Portugal |`pt`|✅ | ✅| ✅||✅||
| Portuguese-Portugal |`pt-PT`| | ✅| ||||
|Romanian |`ro`| | ✅| ||||
|Russian |`ru`| | ✅| ||||
|Slovak |`sk`| | ✅| ||||
|Slovenian |`sl`| | ✅| ||||
|Serbian - Cyrillic RS |`sr-Cryl`| | ✅| ||||
|Serbian - Latin RS |`sr-Latn`| | ✅| ||||
|Swedish |`sv`| | ✅| ||||
|Thai |`th`| | ✅| ||||
|Turkish |`tr`| | ✅| ||||
|Ukrainian |`uk`| | ✅| ||||
|Vietnamese |`vi`| | ✅| ||||
|Chinese Simplified |`zh`|✅ | ✅| ✅| |✅||
|Chinese Simplified |`zh-Hans`| | ✅| ||||
|Chinese Traditional |`zh-Hant`| | ✅| ||||

## Multimodal embeddings

The latest [Multimodal embeddings](./concept-image-retrieval.md) model supports vector search in many languages. The original model supports English only. Images that are vectorized in the English-only model are not compatible with text searches in the multi-lingual model.

| Language  | Language code | `2023-04-15` model | `2022-04-11` model|
|-----------------------|---------------| -- |--  |
| Akrikaans             | `af`          | ✅ |  |
| Amharic               | `am`          | ✅ |  |
| Arabic                | `ar`          | ✅ |  |
| Armenian              | `hy`          | ✅ |  |
| Assamese              | `as`          | ✅ |  |
| Asturian              | `ast`         | ✅ |  |
| Azerbaijani           | `az`          | ✅ |  |
| Belarusian            | `be`          | ✅ |  |
| Bengali               | `bn`          | ✅ |  |
| Bosnian               | `bs`          | ✅ |  |
| Bulgarian             | `bg`          | ✅ |  |
| Burmese               | `my`          | ✅ |  |
| Catalan               | `ca`          | ✅ |  |
| Cebuano               | `ceb`         | ✅ |  |
| Chinese Simpl         | `zho`         | ✅ |  |
| Chinese Trad          | `zho`         | ✅ |  |
| Croatian              | `hr`          | ✅ |  |
| Czech                 | `cs`          | ✅ |  |
| Danish                | `da`          | ✅ |  |
| Dutch                 | `nl`          | ✅ |  |
| English               | `en`          | ✅ | ✅ |
| Estonian              | `et`          | ✅ |  |
| Filipino (Tagalog)    | `tl`          | ✅ |  |
| Finnish               | `fi`          | ✅ |  |
| French                | `fr`          | ✅ |  |
| Fulah                 | `ff`          | ✅ |  |
| Galician              | `gl`          | ✅ |  |
| Ganda                 | `lg`          | ✅ |  |
| Georgian              | `ka`          | ✅ |  |
| German                | `de`          | ✅ |  |
| Greek                 | `el`          | ✅ |  |
| Gujarati              | `gu`          | ✅ |  |
| Hausa                 | `ha`          | ✅ |  |
| Hebrew                | `he`          | ✅ |  |
| Hindi                 | `hi`          | ✅ |  |
| Hungarian             | `hu`          | ✅ |  |
| Icelandic             | `is`          | ✅ |  |
| Igbo                  | `ig`          | ✅ |  |
| Indonesian            | `id`          | ✅ |  |
| Irish                 | `ga`          | ✅ |  |
| Italian               | `it`          | ✅ |  |
| Japanese              | `ja`          | ✅ |  |
| Javanese              | `jv`          | ✅ |  |
| Kabuverdianu          | `kea`         | ✅ |  |
| Kamba                 | `kam`         | ✅ |  |
| Kannada               | `kn`          | ✅ |  |
| Kazakh                | `kk`          | ✅ |  |
| Khmer                 | `km`          | ✅ |  |
| Korean                | `ko`          | ✅ |  |
| Kyrgyz                | `ky`          | ✅ |  |
| Lao                   | `lo`          | ✅ |  |
| Latvian               | `lv`          | ✅ |  |
| Lingala               | `ln`          | ✅ |  |
| Lithuanian            | `lt`          | ✅ |  |
| Luo                   | `luo`         | ✅ |  |
| Luxembourgish         | `lb`          | ✅ |  |
| Macedonian            | `mk`          | ✅ |  |
| Malay                 | `ms`          | ✅ |  |
| Malayalam             | `ml`          | ✅ |  |
| Maltese               | `mt`          | ✅ |  |
| Maori                 | `mi`          | ✅ |  |
| Marathi               | `mr`          | ✅ |  |
| Mongolian             | `mn`          | ✅ |  |
| Nepali                | `ne`          | ✅ |  |
| Northern Sotho        | `ns`          | ✅ |  |
| Norwegian             | `no`          | ✅ |  |
| Nyanja                | `ny`          | ✅ |  |
| Occitan               | `oc`          | ✅ |  |
| Odia                  | `or`          | ✅ |  |
| Oromo                 | `om`          | ✅ |  |
| Pashto                | `ps`          | ✅ |  |
| Persian               | `fa`          | ✅ |  |
| Polish                | `pl`          | ✅ |  |
| Portuguese (Brazil)   | `pt`          | ✅ |  |
| Punjabi               | `pa`          | ✅ |  |
| Romanian              | `ro`          | ✅ |  |
| Russian               | `ru`          | ✅ |  |
| Serbian               | `sr`          | ✅ |  |
| Shona                 | `sn`          | ✅ |  |
| Sindhi                | `sd`          | ✅ |  |
| Slovak                | `sk`          | ✅ |  |
| Slovenian             | `sl`          | ✅ |  |
| Somali                | `so`          | ✅ |  |
| Sorani Kurdish        | `ku`          | ✅ |  |
| Spanish (Latin American) | `es`       | ✅ |  |
| Swahili               | `sw`          | ✅ |  |
| Swedish               | `sv`          | ✅ |  |
| Tajik                 | `tg`          | ✅ |  |
| Tamil                 | `ta`          | ✅ |  |
| Telugu                | `te`          | ✅ |  |
| Thai                  | `th`          | ✅ |  |
| Turkish               | `tr`          | ✅ |  |
| Ukrainian             | `uk`          | ✅ |  |
| Umbundu               | `umb`         | ✅ |  |
| Urdu                  | `ur`          | ✅ |  |
| Uzbek                 | `uz`          | ✅ |  |
| Vietnamese            | `vi`          | ✅ |  |
| Welsh                 | `cy`          | ✅ |  |
| Wolof                 | `wo`          | ✅ |  |
| Xhosa                 | `xh`          | ✅ |  |
| Yoruba                | `yo`          | ✅ |  |
| Zulu                  | `zu`          | ✅ |  |
