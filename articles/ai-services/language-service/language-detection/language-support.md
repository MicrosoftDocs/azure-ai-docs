---
title: Language Detection language support
titleSuffix: Foundry Tools
description: This article explains which natural languages are supported by Azure Language Detection API.
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: concept-article
ms.date: 11/18/2025
ms.author: lajanuar
ms.custom: language-service-language-detection, ignite-2024
---
# Language support for Language Detection

Use this article to learn which natural languages that language detection supports.

The Language Detection feature can detect a wide range of languages, variants, dialects, and some regional/cultural languages, and return detected languages with their name and code. The returned language code parameters conform to [BCP-47](https://tools.ietf.org/html/bcp47) standard with most of them conforming to [ISO-639-1](https://www.iso.org/iso-639-language-codes.html) identifiers. 

If you have content expressed in a less frequently used language, you can try Language Detection to see if it returns a code. The response for languages that can't be detected is `unknown`.

## Languages supported by Language Detection

| Language            | Language Code | Supported Script Code |
|---------------------|---------------|-----------------------|
| Afrikaans           | `af`          | `Latn`                |
| Albanian            | `sq`          | `Latn`                |
| Amharic             | `am`          | `Ethi`                |
| Arabic              | `ar`          | `Arab`                |
| Armenian            | `hy`          | `Armn`                |
| Assamese            | `as`          | `Beng`, `Latn`        |
| Azerbaijani         | `az`          | `Latn`                |
| Bashkir             | `ba`          | `Cyrl`                |
| Basque              | `eu`          | `Latn`                |
| Belarusian          | `be`          | `Cyrl`                |
| Bengali             | `bn`          | `Beng`, `Latn`        |
| Bhojpuri            | `bho`         | `Deva`                |
| Bodo                | `brx`         | `Deva`                |
| Bosnian             | `bs`          | `Latn`                |
| Bulgarian           | `bg`          | `Cyrl`                |
| Burmese             | `my`          | `Mymr`                |
| Catalan             | `ca`          | `Latn`                |
| Central Khmer       | `km`          | `Khmr`                |
| Checheni            | `ce`          | `Cyrl`                |
| Chhattisgarhi       | `hne`         | `Deva`                |
| Chinese Literal     | `lzh`         | `Hani`                |
| Chinese Simplified  | `zh_chs`      | `Hans`                |
| Chinese Traditional | `zh_cht`      | `Hant`                |
| Chuvash             | `cv`          | `Cyrl`                |
| Corsican            | `co`          | `Latn`                |
| Croatian            | `hr`          | `Latn`                |
| Czech               | `cs`          | `Latn`                |
| Danish              | `da`          | `Latn`                |
| Dari                | `prs`         | `Arab`                |
| Divehi              | `dv`          | `Thaa`                |
| Dogri               | `dgo`         | `Deva`                |
| Dutch               | `nl`          | `Latn`                |
| English             | `en`          | `Latn`                |
| Esperanto           | `eo`          | `Latn`                |
| Estonian            | `et`          | `Latn`                |
| Faroese             | `fo`          | `Latn`                |
| Fijian              | `fj`          | `Latn`                |
| Finnish             | `fi`          | `Latn`                |
| French              | `fr`          | `Latn`                |
| Galician            | `gl`          | `Latn`                |
| Georgian            | `ka`          | `Gujr`                |
| German              | `de`          | `Latn`                |
| Greek               | `el`          | `Grek`                |
| Gujarati            | `gu`          | `Gujr`, `Latn`        |
| Haitian             | `ht`          | `Latn`                |
| Hausa               | `ha`          | `Latn`                |
| Hebrew              | `he`          | `Hebr`                |
| Hindi               | `hi`          | `Deva`, `Latn`        |
| Hmong Daw           | `mww`         | `Latn`                |
| Hungarian           | `hu`          | `Latn`                |
| Icelandic           | `is`          | `Latn`                |
| Igbo                | `ig`          | `Latn`                |
| Indonesian          | `id`          | `Latn`                |
| Inuktitut           | `iu`          | `Cans`, `Latn`        |
| Inuinnaqtun         | `ikt`         | `Latn`                |
| Irish               | `ga`          | `Latn`                |
| Italian             | `it`          | `Latn`                |
| Japanese            | `ja`          | `Jpan`                |
| Javanese            | `jv`          | `Latn`                |
| Kannada             | `kn`          | `Knda`, `Latn`        |
| Kashmiri            | `ks`          | `Arab`, `Deva`, `Shrd`|
| Kazakh              | `kk`          | `Cyrl`                |
| Kinyarwanda         | `rw`          | `Latn`                |
| Kirghiz             | `ky`          | `Cyrl`                |
| Konkani             | `gom`         | `Deva`                |
| Korean              | `ko`          | `Hang`                |
| Kurdish             | `ku`          | `Arab`                |
| Kurdish (Northern)  | `kmr`         | `Latn`                |
| Lao                 | `lo`          | `Laoo`                |
| Latin               | `la`          | `Latn`                |
| Latvian             | `lv`          | `Latn`                |
| Lithuanian          | `lt`          | `Latn`                |
| Lower Siberian      | `dsb`         | `Latn`                |
| Luxembourgish       | `lb`          | `Latn`                |
| Macedonian          | `mk`          | `Cyrl`                |
| Maithili            | `mai`         | `Deva`                |
| Malagasy            | `mg`          | `Latn`                |
| Malay               | `ms`          | `Latn`                |
| Malayalam           | `ml`          | `Mlym`, `Latn`        |
| Maltese             | `mt`          | `Latn`                |
| Maori               | `mi`          | `Latn`                |
| Marathi             | `mr`          | `Deva`, `Latn`        |
| Meitei              | `mni`         | `Mtei`                |
| Mongolian           | `mn`          | `Cyrl`, `Mong`        |
| Nepali              | `ne`          | `Deva`                |
| Norwegian           | `no`          | `Latn`                |
| Norwegian Nynorsk   | `nn`          | `Latn`                |
| Odia                | `or`          | `Orya`, `Latn`        |
| Pashto              | `ps`          | `Arab`                |
| Persian             | `fa`          | `Arab`                |
| Polish              | `pl`          | `Latn`                |
| Portuguese          | `pt`          | `Latn`                |
| Punjabi             | `pa`          | `Guru`, `Latn`        |
| Queretaro Otomi     | `otq`         | `Latn`                |
| Romanian            | `ro`          | `Latn`                |
| Russian             | `ru`          | `Cyrl`                |
| Samoan              | `sm`          | `Latn`                |
| Sanscrit            | `sa`          | `Deva`                |
| Santali             | `sat`         | `Olck`                |
| Serbian             | `sr`          | `Latn`, `Cyrl`        |
| Shona               | `sn`          | `Latn`                |
| Sindhi              | `sd`          | `Arab`                |
| Sinhala             | `si`          | `Sinh`                |
| Slovak              | `sk`          | `Latn`                |
| Slovenian           | `sl`          | `Latn`                |
| Somali              | `so`          | `Latn`                |
| Spanish             | `es`          | `Latn`                |
| Sundanese           | `su`          | `Latn`                |
| Swahili             | `sw`          | `Latn`                |
| Swedish             | `sv`          | `Latn`                |
| Tagalog             | `tl`          | `Latn`                |
| Tahitian            | `ty`          | `Latn`                |
| Tajik               | `tg`          | `Cyrl`                |
| Tamil               | `ta`          | `Taml`, `Latn`        |
| Tatar               | `tt`          | `Cyrl`                |
| Telugu              | `te`          | `Telu`, `Latn`        |
| Thai                | `th`          | `Thai`                |
| Tibetan             | `bo`          | `Tibt`                |
| Tigrinya            | `ti`          | `Ethi`                |
| Tongan              | `to`          | `Latn`                |
| Turkish             | `tr`          | `Latn`                |
| Turkmen             | `tk`          | `Latn`                |
| Upper Sorbian       | `hsb`         | `Latn`                |
| Uyghur              | `ug`          | `Arab`                |
| Ukrainian           | `uk`          | `Latn`                |
| Urdu                | `ur`          | `Arab`, `Latn`        |
| Uzbek               | `uz`          | `Latn`                |
| Vietnamese          | `vi`          | `Latn`                |
| Welsh               | `cy`          | `Latn`                |
| Xhosa               | `xh`          | `Latn`                |
| Yiddish             | `yi`          | `Hebr`                |
| Yoruba              | `yo`          | `Latn`                |
| Yucatec Maya        | `yua`         | `Latn`                |
| Zulu                | `zu`          | `Latn`                |

## Romanized Indic Languages supported by Language Detection

| Language            | Language Code |
|---------------------|---------------|
| Assamese            | `as`          |
| Bengali             | `bn`          |
| Gujarati            | `gu`          |
| Hindi               | `hi`          |
| Kannada             | `kn`          |
| Malayalam           | `ml`          |
| Marathi             | `mr`          |
| Odia                | `or`          |
| Punjabi             | `pa`          |
| Tamil               | `ta`          |
| Telugu              | `te`          |
| Urdu                | `ur`          |

## Script detection

| Language                              | Script code | Scripts        |
| ------------------------------------- | ----------  | -------------- |
| Assamese                              | `as`        | `Latn`, `Beng` |
| Bengali                               | `bn`        | `Latn`, `Beng` |
| Gujarati                              | `gu`        | `Latn`, `Gujr` |
| Hindi                                 | `hi`        | `Latn`, `Deva` |
| Kannada                               | `kn`        | `Latn`, `Knda` |
| Malayalam                             | `ml`        | `Latn`, `Mlym` |
| Marathi	                            | `mr`        | `Latn`, `Deva` |
| Odia                                  | `or`        | `Latn`, `Orya` |
| Punjabi                               | `pa`        | `Latn`, `Guru` |
| Tamil                                 | `ta`        | `Latn`, `Taml` |
| Telugu                                | `te`        | `Latn`, `Telu` |
| Urdu                                  | `ur`        | `Latn`, `Arab` |
| Tatar                                 | `tt`        | `Latn`, `Cyrl` |
| Serbian                               | `sr`        | `Latn`, `Cyrl` |
| Inuktitut                         	| `iu`        | `Latn`, `Cans` |

## Next steps

[Language detection overview](overview.md)
