---
title: Application settings - LUIS
description: Applications settings for Azure AI services language understanding apps are stored in the app and portal.
ms.service: azure-ai-language
ms.subservice: azure-ai-luis
ms.author: lajanuar
author: laujan
manager: nitinme
ms.topic: reference
ms.date: 06/12/2025
---

# App and version settings

[!INCLUDE [deprecation notice](./includes/deprecation-notice.md)]


These settings are stored in the [exported](/rest/api/luis/versions/export) app and updated with the REST APIs or LUIS portal.

Changing your app version settings resets your app training status to untrained.

[!INCLUDE [App and version settings](includes/app-version-settings.md)]


Text reference and examples include:

* [Punctuation](#punctuation-normalization)
* [Diacritics](#diacritics-normalization)

## Diacritics normalization

The following utterances show how diacritics normalization impacts utterances:

|With diacritics set to false|With diacritics set to true|
|--|--|
|`quiero tomar una piña colada`|`quiero tomar una pina colada`|
|||

### Language support for diacritics

#### Brazilian Portuguese `pt-br` diacritics

|Diacritics set to false|Diacritics set to true|
|-|-|
|`á`|`a`|
|`â`|`a`|
|`ã`|`a`|
|`à`|`a`|
|`ç`|`c`|
|`é`|`e`|
|`ê`|`e`|
|`í`|`i`|
|`ó`|`o`|
|`ô`|`o`|
|`õ`|`o`|
|`ú`|`u`|
|||

#### Dutch `nl-nl` diacritics

|Diacritics set to false|Diacritics set to true|
|-|-|
|`á`|`a`|
|`à`|`a`|
|`é`|`e`|
|`ë`|`e`|
|`è`|`e`|
|`ï`|`i`|
|`í`|`i`|
|`ó`|`o`|
|`ö`|`o`|
|`ú`|`u`|
|`ü`|`u`|
|||

#### French `fr-` diacritics

This includes both French and Canadian subcultures.

|Diacritics set to false|Diacritics set to true|
|--|--|
|`é`|`e`|
|`à`|`a`|
|`è`|`e`|
|`ù`|`u`|
|`â`|`a`|
|`ê`|`e`|
|`î`|`i`|
|`ô`|`o`|
|`û`|`u`|
|`ç`|`c`|
|`ë`|`e`|
|`ï`|`i`|
|`ü`|`u`|
|`ÿ`|`y`|

#### German `de-de` diacritics

|Diacritics set to false|Diacritics set to true|
|--|--|
|`ä`|`a`|
|`ö`|`o`|
|`ü`|`u`|

#### Italian `it-it` diacritics

|Diacritics set to false|Diacritics set to true|
|--|--|
|`à`|`a`|
|`è`|`e`|
|`é`|`e`|
|`ì`|`i`|
|`í`|`i`|
|`î`|`i`|
|`ò`|`o`|
|`ó`|`o`|
|`ù`|`u`|
|`ú`|`u`|

#### Spanish `es-` diacritics

This includes both Spanish and Canadian Mexican.

|Diacritics set to false|Diacritics set to true|
|-|-|
|`á`|`a`|
|`é`|`e`|
|`í`|`i`|
|`ó`|`o`|
|`ú`|`u`|
|`ü`|`u`|
|`ñ`|`u`|

## Punctuation normalization

The following utterances show how punctuation impacts utterances:

|With punctuation set to False|With punctuation set to True|
|--|--|
|`Hmm..... I will take the cappuccino`|`Hmm I will take the cappuccino`|
|||

### Punctuation removed

The following punctuation is removed with `NormalizePunctuation` is set to true.

|Punctuation|
|--|
|`-`|
|`.`|
|`'`|
|`"`|
|`\`|
|`/`|
|`?`|
|`!`|
|`_`|
|`,`|
|`;`|
|`:`|
|`(`|
|`)`|
|`[`|
|`]`|
|`{`|
|`}`|
|`+`|
|`¡`|

## Next steps

* Learn [concepts](concepts/utterances.md#utterance-normalization) of diacritics and punctuation.
