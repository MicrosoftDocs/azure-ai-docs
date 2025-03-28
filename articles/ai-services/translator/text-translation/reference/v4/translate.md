---
title: Translator Translate Method
titleSuffix: Azure AI services
description: Understand the parameters, headers, and body messages for the Azure AI Translator to translate text method.
author: laujan
manager: nitinme

ms.service: azure-ai-translator
ms.topic: reference
ms.date: 03/28/2025
ms.author: lajanuar
---

# Translator 4.0: Translate

Translates text.

## Request URL

Send a `POST` request to:

```HTTP
https://api.cognitive.microsofttranslator.com/translate?api-version=TODO
```

_See_ [**Virtual Network Support**](reference.md#virtual-network-support) for Translator service selected network and private endpoint configuration and support.

## Request headers

Request headers include:

| Headers | Description |
| --- | --- |
| **Authentication headers** | _Required request header_.<br/>See [available options for authentication](../authentication.md). |
| **Content-Type** | _Required request header_.<br/>Specifies the content type of the payload. Accepted values are: `application/json`; `charset=UTF-8`|
| **Content-Length** | _Optional_.<br/>The length of the request body. |
| **X-ClientTraceId** | _Optional_.<br/>A client-generated GUID to uniquely identify the request. You can omit this optional header if you include the trace ID in the query string using a query parameter named `ClientTraceId`. |

## Request body parameters

The body of the request is a JSON array. Each array element is a JSON object with a string property named `Text`, which represents the string to translate.

```json
[
    {"Text":"I would really like to drive your car around the block a few times."}
]
```

For information on character and array limits, _see_ [Request limits](../../../service-limits.md#character-and-array-limits-per-request).

Request parameters passed on the query string are as follows:

#### Required query parameters

| Parameter | Type | Required? | Description |
| --- | --- | --- | --- |
|**api-version**|string|True|Version of the API requested by the client.|
| **text** | string | True | Source text for translation. |

#### Required targets array parameters

| Parameter | Type | Required? | Description |
| --- | --- | --- | --- |
| **targets** | array | True | Targets for text translation. |
| **language** | string | True | The language code for the translated text. Possible values are list of language code supported by the specified model. |

#### Optional query parameters

| Parameter | Type | Required? | Description |
| --- | --- | --- | --- |
| **textType** | string | False | Defines whether the text being translated is plain text or HTML text. Any HTML needs to be a well-formed, complete element. Possible values are: plain (default) or html. |
| **language** | string | False | The language code for the source text. If not specified, the system autodetects the language of the source text. Possible values are list of language code supported by the specified model. |
| **script** | string | False | Specify the script of the source text. |

#### Optional targets array parameters

| Parameter | Type | Required? | Description |
| --- | --- | --- | --- |
| **script** | string | False | Specify the script of the translated text. |
|**deploymentName** | string | False | Default is `general`, which uses `NMT` system. `gpt-4o-mini` uses GPT-4o-mini model. `gpt-4o` uses GPT-4o model. `<custom model id>` uses the custom `NMT` model tuned by customer. |
| **allowFallback** | string | False | If the specified model isn't supported for a given source and target language pair, the service is permitted to revert to a general system. This action ensures that translations can still be provided even when the preferred model is unavailable. Default is `true`. If `false` system returns an error if language pair isn't supported. |
| **grade** | string | False | Default is `basic`. For example, translation produced by simple prompt like `translate <source text> from <source language> to <target language>`|
| **tone** | string | False | Desired tone of target translation. Enum: Formal, informal, neutral. |
| **gender** **\*** | string | False | Desired gender of target translation.|
| **adaptiveDatasetId** | string | False | Reference dataset ID having sentence pair to generate adaptive customized translation |
| **referenceTextPairs** | string | False | Reference text pairs to generate adaptive customized translation |
| **referenceTextPairs.source** | string | False | Source text in reference text pair. |
| **referenceTextPairs.target** | string | False | Target text in reference text pair. |
| **profanityAction** | string | False | Specifies how profanities should be treated in translations. Possible values are: `NoAction` (default), `Marked`, or `Deleted`. |
| **profanityMarker** | string | False | Specifies how profanities should be marked in translations. Possible values are `Asterisk` (default) or Tag. |
| **instruct** | string | False | Free flow textual instruction for `LLM` translation. This parameter negates all other key parameters within `targets`.|

##### Gender-specific translations with optional targets array gender parameter

| Source text | Target gender | Expected gender in translation |
| --- | --- | --- |
| Neutral |  | Neutral /  **Random**: if target language doesn't have a gender-neutral term. |
| Female |  | Female / **Neutral**: if target language is gender neutral. |
| Male |  | Male / **Neutral**: if target language is gender neutral. |
| Neutral | Female | Female / **Neutral**: if target language is gender neutral. |
| Female | Female |
| Male | Female |
| Neutral | Male | Male / **Neutral**: if target language is gender neutral. |
| Female | Male |
| Male | Male |

## Response body

A successful response is a JSON array with one result for each string in the input array. A result object includes the following properties:

* `detectedLanguage`: An object describing the detected language through the following properties:

  * `language`: A string representing the code of the detected language.

  * `score`: A float value indicating the confidence in the result. The score is between zero and one and a low score indicates a low confidence.

  The `detectedLanguage` property is only present in the result object when language autodetection is requested.

* `translations`: An array of translation results. The size of the array matches the number of target languages specified through the `to` query parameter. Each element in the array includes:

  * `to`: A string representing the language code of the target language.

  * `text`: A string giving the translated text.

  * `transliteration`: An object giving the translated text in the script specified by the `toScript` parameter.

    * `script`: A string specifying the target script.

    * `text`: A string giving the translated text in the target script.

    The `transliteration` object isn't included if transliteration doesn't take place.

    * `alignment`: An object with a single string property named `proj`, which maps input text to translated text. The alignment information is only provided when the request parameter `includeAlignment` is `true`. Alignment is returned as a string value of the following format: `[[SourceTextStartIndex]:[SourceTextEndIndex]–[TgtTextStartIndex]:[TgtTextEndIndex]]`. The colon separates start and end index, the dash separates the languages, and space separates the words. One word can align with zero, one, or multiple words in the other language, and the aligned words can be noncontiguous. When no alignment information is available, the alignment element is empty. See [Obtain alignment information](#obtain-alignment-information) for an example and restrictions.

  * `sentLen`: An object returning sentence boundaries in the input and output texts.

    * `srcSentLen`: An integer array representing the lengths of the sentences in the input text. The length of the array is the number of sentences, and the values are the length of each sentence.

    * `transSentLen`:  An integer array representing the lengths of the sentences in the translated text. The length of the array is the number of sentences, and the values are the length of each sentence.

    Sentence boundaries are only included when the request parameter `includeSentenceLength` is `true`.

* `sourceText`: An object with a single string property named `text`, which gives the input text in the default script of the source language. `sourceText` property is present only when the input is expressed in a script that's not the usual script for the language. For example, if the input were Arabic written in Latin script, then `sourceText.text` would be the same Arabic text converted into Arab script`.`

Examples of JSON responses are provided in the [examples](#examples) section.

## Response headers

| Headers | Description |
| --- | --- |
| X-requestid | Value generated by the service to identify the request used for troubleshooting purposes. |
| X-mt-system | Specifies the system type that was used for translation for each 'to' language requested for translation. The value is a comma-separated list of strings. Each string indicates a type:  </br></br>*Custom - Request includes a custom system and at least one custom system was used during translation.*</br> Team - All other requests |
| X-metered-usage |Specifies consumption (the number of characters for which the user is charged) for the translation job request. For example, if the word "Hello" is translated from English (en) to French (fr), this field returns the value `5`.|


## Examples

#### Translate text

***Request***

```bash
 [ { "text": "Doctor is available next Monday. Do you want to schedule an appointment?", "targets": [ {     "language": "es"} ] } ] |
```

***Response***

```bash
[ { "detectedLanguage": { "language": "en", "score": 1     }, "translations": [ { "text": "La médica estará disponible el próximo lunes. ¿Desea programar una cita?", "language": "es", "sourceCharacters": 72} ]   } ]
```

***Response Header***

```bash
"sourceCharactersCharged": 72
```

#### Translate source text into multiple languages

***Request***

```bash
[ { "text": "Doctor is available next Monday. Do you want to schedule an appointment?", "targets": [ {     "language": "es"} , {     "language": "de"} ] } ]
```

***Response***

```bash
[ { "detectedLanguage": { "language": "en", "score": 1     }, "translations": [ { "text": "La médica estará disponible el próximo lunes. ¿Desea programar una cita?", "language": "es", "sourceCharacters": 72} , { "text": "Der Arzt ist nächsten Montag verfügbar. Möchten Sie einen Termin vereinbaren?", "language": "de", "sourceCharacters": 72} ]   } ]
```

***Response Header***

```bash
"sourceCharactersCharged": 144
```

#### Translate text using `GPT-4o mini` and `NMT` deployments

Here, users request specific `GPT` models for deployment.

***Request***

```bash
 [ { "text": "Doctor is available next Monday. Do you want to schedule an appointment?", "targets": [ {     "language": "es", " deploymentName": "gpt-4o-mini"} , {     "language": "de"} ] } ]
```

***Response***

```bash
| [ { "detectedLanguage": { "language": "en", "score": 1     }, "translations": [ { "text": "La médica estará disponible el próximo lunes. ¿Desea programar una cita?", "language": "es", "instructionTokens": 12,  "sourceTokens": 14,  "targetTokens": 16} , { "text": "Der Arzt ist nächsten Montag verfügbar. Möchten Sie einen Termin vereinbaren?", "language": "de", "sourceCharacters": 72} ]   } ]
```

***Response Header***

```bash
"sourceCharactersCharged": 72 
"sourceTokensCharged": 26
"targetTokensCharged": 16
```

#### Translate specifying gender and tone using `GPT-4o mini` deployment

***Request***

```bash
[ { "text": "Doctor is available next Monday. Do you want to schedule an appointment?", "targets": [ {     "language": "es", "model": "gpt-4o-mini", "tone": "formal", "gender": "female"},  {  "language": "es", "model": "gpt-4o-mini", "tone": "formal", "gender": "male"} ] } ]
```

***Response***

```bash
[ { "detectedLanguage": { "language": "en", "score": 1     }, "translations": [ { "text": "La médica estará disponible el próximo lunes. ¿Desea programar una cita?", "language": "es", "promptTokens": 12,  "sourceTokens": 14,  "targetTokens": 16}, { "text": "El médico estará disponible el próximo lunes. ¿Desea programar una cita?", "language": "es", "instructionTokens": 12,  "sourceTokens": 14,  "targetTokens": 16} ]   } ]
```

***Response Header***

```bash
"sourceTokensCharged": 52
"targetTokensCharged": 32
```

#### Text translation request applying adaptive custom translation with dataset

Adaptive custom translation deploys on Translator service infrastructure. Charges are based on source characters.

***Request***

```bash
[ { "text": "Doctor is available next Monday. Do you want to schedule an appointment?", "targets": [ {     "language": "es", "adaptiveDatasetId": "TMS-en-es-hr-020"} ] } ]
```

***Response***

```bash
[ { "detectedLanguage": { "language": "en", "score": 1     }, "translations": [ { "text": "La médica estará disponible el próximo lunes. ¿Desea programar una cita?", "language": "es", "sourceCharacters": 72, "targetChaaracters": 72} ]   } ]
```

***Response Header***

```bash
"sourceCharactersCharged": 72 "targetChaaractersCharged": 72
```

#### Text translation request applying Adaptive custom translation with reference pairs

***Request***

```bash
[ { "text": "Doctor is available next Monday. Do you want to schedule an appointment?", "targets": [ {     "language": "es", "referenceTextPairs": [ {  "source": "text_in_en",  "target": " text_in_es"}, { "source": " text_in_en",  "target": " text_in_es" }] } ] } ]
```

***Response***

```bash
[ { "detectedLanguage": { "language": "en", "score": 1     }, "translations": [ { "text": "La médica estará disponible el próximo lunes. ¿Desea programar una cita?", "language": "es", "sourceCharacters": 72, "targetChaaracters": 72} ] } ]
```

***Response Header***

```bash
"sourceCharactersCharged": 72 
"targetCharactersCharged": 72
```

#### Text translation request using custom translation

***Request***

```bash
[ { "text": "Doctor is available next Monday. Do you want to schedule an appointment?", "targets": [ {     "language": "es", "model": "CT-model-en-es-hr-020"} ] } ]
```

***Response***

```bash
[ { "detectedLanguage": { "language": "en", "score": 1     }, "translations": [ { "text": "La médica estará disponible el próximo lunes. ¿Desea programar una cita?", "language": "es", "sourceCharacters": 72} ]   } ]
```

***Response Header***

```bash
"sourceCharactersCharged": 72
```

## Request body

The body of the request is a JSON array. Each array element is a JSON object with a string property named `Text`, which represents the string to translate.

```json
[
    {"Text":"I would really like to drive your car around the block a few times."}
]
```

For information on character and array limits, _see_ [Request limits](../../../service-limits.md#character-and-array-limits-per-request).

## Response 

A successful response is a JSON array with one result for each string in the input array. A result object includes the following properties:

* `detectedLanguage`: An object describing the detected language through the following properties:

  * `language`: A string representing the code of the detected language.

  * `score`: A float value indicating the confidence in the result. The score is between zero and one and a low score indicates a low confidence.

  The `detectedLanguage` property is only present in the result object when language autodetection is requested.

* `translations`: An array of translation results. The size of the array matches the number of target languages specified through the `to` query parameter. Each element in the array includes:

  * `to`: A string representing the language code of the target language.

  * `text`: A string giving the translated text.

  * `transliteration`: An object giving the translated text in the script specified by the `toScript` parameter.

    * `script`: A string specifying the target script.

    * `text`: A string giving the translated text in the target script.

    The `transliteration` object isn't included if transliteration doesn't take place.

    * `alignment`: An object with a single string property named `proj`, which maps input text to translated text. The alignment information is only provided when the request parameter `includeAlignment` is `true`. Alignment is returned as a string value of the following format: `[[SourceTextStartIndex]:[SourceTextEndIndex]–[TgtTextStartIndex]:[TgtTextEndIndex]]`. The colon separates start and end index, the dash separates the languages, and space separates the words. One word can align with zero, one, or multiple words in the other language, and the aligned words can be noncontiguous. When no alignment information is available, the alignment element is empty. See [Obtain alignment information](#obtain-alignment-information) for an example and restrictions.

  * `sentLen`: An object returning sentence boundaries in the input and output texts.

    * `srcSentLen`: An integer array representing the lengths of the sentences in the input text. The length of the array is the number of sentences, and the values are the length of each sentence.

    * `transSentLen`:  An integer array representing the lengths of the sentences in the translated text. The length of the array is the number of sentences, and the values are the length of each sentence.

    Sentence boundaries are only included when the request parameter `includeSentenceLength` is `true`.

* `sourceText`: An object with a single string property named `text`, which gives the input text in the default script of the source language. `sourceText` property is present only when the input is expressed in a script that's not the usual script for the language. For example, if the input were Arabic written in Latin script, then `sourceText.text` would be the same Arabic text converted into Arab script`.`

Examples of JSON responses are provided in the [examples](#examples) section.

## Response Headers

| Headers | Description |
| --- | --- |
| X-requestid | Value generated by the service to identify the request used for troubleshooting purposes. |
| X-mt-system | Specifies the system type that was used for translation for each 'to' language requested for translation. The value is a comma-separated list of strings. Each string indicates a type:  </br></br>*Custom - Request includes a custom system and at least one custom system was used during translation.*</br> Team - All other requests |
| X-metered-usage |Specifies consumption (the number of characters for which the user is charged) for the translation job request. For example, if the word "Hello" is translated from English (en) to French (fr), this field returns the value `5`.|

## Response status codes

If an error occurs, the request returns a JSON error response. The error code is a 6-digit number combining the 3-digit HTTP status code followed by a 3-digit number to further categorize the error. Common error codes can be found on the [Translator status code reference page](../status-response-codes.md).

## Translate examples

### Translate a single input

This example shows how to translate a single sentence from English to Simplified Chinese.

 ```bash
curl -X POST "https://api.cognitive.microsofttranslator.com/translate?api-version=TODO&from=en&to=zh-Hans" -H "Ocp-Apim-Subscription-Key: <client-secret>" -H "Content-Type: application/json; charset=UTF-8" -d "[{'Text':'Hello, what is your name?'}]"
```

The response body is:

```json
[
    {
        "translations":[
            {"text":"你好, 你叫什么名字？","to":"zh-Hans"}
        ]
    }
]
```

The `translations` array includes one element, which provides the translation of the single piece of text in the input.

### Translate a single input with language autodetection

This example shows how to translate a single sentence from English to Simplified Chinese. The request doesn't specify the input language. Autodetection of the source language is used instead.

 ```bash
curl -X POST "https://api.cognitive.microsofttranslator.com/translate?api-version=TODO&to=zh-Hans" -H "Ocp-Apim-Subscription-Key: <client-secret>" -H "Content-Type: application/json; charset=UTF-8" -d "[{'Text':'Hello, what is your name?'}]"
```

The response body is:

```json
[
    {
        "detectedLanguage": {"language": "en", "score": 1.0},
        "translations":[
            {"text": "你好, 你叫什么名字？", "to": "zh-Hans"}
        ]
    }
]
```
The response is similar to the response from the previous example. Since language autodetection was requested, the response also includes information about the language detected for the input text. The language autodetection works better with longer input text.

### Translate with transliteration

Let's extend the previous example by adding transliteration. The following request asks for a Chinese translation written in Latin script.

 ```bash
curl -X POST "https://api.cognitive.microsofttranslator.com/translate?api-version=TODO&to=zh-Hans&toScript=Latn" -H "Ocp-Apim-Subscription-Key: <client-secret>" -H "Content-Type: application/json; charset=UTF-8" -d "[{'Text':'Hello, what is your name?'}]"
```

The response body is:

```json
[
    {
        "detectedLanguage":{"language":"en","score":1.0},
        "translations":[
            {
                "text":"你好, 你叫什么名字？",
                "transliteration":{"script":"Latn", "text":"nǐ hǎo , nǐ jiào shén me míng zì ？"},
                "to":"zh-Hans"
            }
        ]
    }
]
```

The translation result now includes a `transliteration` property, which gives the translated text using Latin characters.

### Translate multiple pieces of text

Translating multiple strings at once is simply a matter of specifying an array of strings in the request body.

 ```bash
curl -X POST "https://api.cognitive.microsofttranslator.com/translate?api-version=TODO&from=en&to=zh-Hans" -H "Ocp-Apim-Subscription-Key: <client-secret>" -H "Content-Type: application/json; charset=UTF-8" -d "[{'Text':'Hello, what is your name?'}, {'Text':'I am fine, thank you.'}]"
```

The response contains the translation of all pieces of text in the exact same order as in the request.
The response body is:

```json
[
    {
        "translations":[
            {"text":"你好, 你叫什么名字？","to":"zh-Hans"}
        ]
    },
    {
        "translations":[
            {"text":"我很好，谢谢你。","to":"zh-Hans"}
        ]
    }
]
```

### Translate to multiple languages

This example shows how to translate the same input to several languages in one request.

 ```bash
curl -X POST "https://api.cognitive.microsofttranslator.com/translate?api-version=TODO&from=en&to=zh-Hans&to=de" -H "Ocp-Apim-Subscription-Key: <client-secret>" -H "Content-Type: application/json; charset=UTF-8" -d "[{'Text':'Hello, what is your name?'}]"
```

The response body is:

```json
[
    {
        "translations":[
            {"text":"你好, 你叫什么名字？","to":"zh-Hans"},
            {"text":"Hallo, was ist dein Name?","to":"de"}
        ]
    }
]
```

### Handle profanity

Normally, the Translator service retains profanity that is present in the source in the translation. The degree of profanity and the context that makes words profane differ between cultures, and as a result the degree of profanity in the target language can be amplified or reduced.

If you want to avoid getting profanity in the translation, regardless of the presence of profanity in the source text, you can use the profanity filtering option. The option allows you to choose whether you want to see profanity deleted, marked with appropriate tags (giving you the option to add your own post-processing), or with no action taken. The accepted values of `ProfanityAction` are `Deleted`, `Marked`, and `NoAction` (default).


| Accepted ProfanityAction value | ProfanityMarker value | Action | Example: Source - Spanish| Example: Target - English|
|:--|:--|:--|:--|:--|
| NoAction|  | Default. Same as not setting the option. Profanity passes from source to target. | `Que coche de` \<insert-profane-word> | What a \<insert-profane-word> car  |
| Marked                | Asterisk              | Asterisks replace profane words (default).                               | `Que coche de` \<insert-profane-word> | What a *** car      |
| Marked                | Tag                   | Profane words are surrounded by XML tags \<profanity\>...\</profanity>.          | `Que coche de` \<insert-profane-word> | What a \<profanity> \<insert-profane-word> \</profanity> car |
| Deleted               |                       | Profane words are removed from the output without replacement.                   | `Que coche de` \<insert-profane-word> | What a car        |

In the above examples, **\<insert-profane-word>** is a placeholder for profane words.

For example:

 ```bash
curl -X POST "https://api.cognitive.microsofttranslator.com/translate?api-version=TODO&from=en&to=de&profanityAction=Marked" -H "Ocp-Apim-Subscription-Key: <client-secret>" -H "Content-Type: application/json; charset=UTF-8" -d "[{'Text':'This is an <expletive> good idea.'}]"
```

This request returns:

```json
[
    {
        "translations":[
            {"text":"Das ist eine *** gute Idee.","to":"de"}
        ]
    }
]
```

Compare with:

 ```bash
curl -X POST "https://api.cognitive.microsofttranslator.com/translate?api-version=TODO&from=en&to=de&profanityAction=Marked&profanityMarker=Tag" -H "Ocp-Apim-Subscription-Key: <client-secret>" -H "Content-Type: application/json; charset=UTF-8" -d "[{'Text':'This is an <expletive> good idea.'}]"
```

That last request returns:

```json
[
    {
        "translations":[
            {"text":"Das ist eine <profanity>verdammt</profanity> gute Idee.","to":"de"}
        ]
    }
]
```

### Translate content that includes markup

It's common to translate content that includes markup such as content from an HTML page or content from an XML document. Include query parameter `textType=html` when translating content with tags. In addition, it's sometimes useful to exclude specific content from translation. You can use the attribute `class=notranslate` to specify content that should remain in its original language. In the following example, the content inside the first `div` element isn't translated, while the content in the second `div` element is translated.

```html
<div class="notranslate">This will not be translated.</div>
<div>This will be translated. </div>
```

Here's a sample request to illustrate.

 ```bash
curl -X POST "https://api.cognitive.microsofttranslator.com/translate?api-version=TODO&from=en&to=zh-Hans&textType=html" -H "Ocp-Apim-Subscription-Key: <client-secret>" -H "Content-Type: application/json; charset=UTF-8" -d "[{'Text':'<div class=\"notranslate\">This will not be translated.</div><div>This will be translated.</div>'}]"
```

The response is:

```json
[
    {
        "translations":[
            {"text":"<div class=\"notranslate\">This will not be translated.</div><div>这将被翻译。</div>","to":"zh-Hans"}
        ]
    }
]
```

### Obtain alignment information

Alignment is returned as a string value of the following format for every word of the source. The information for each word is separated by a space, including for non-space-separated languages (scripts) like Chinese:

[[SourceTextStartIndex]:[SourceTextEndIndex]–[TgtTextStartIndex]:[TgtTextEndIndex]] *

Example alignment string: "0:0-7:10 1:2-11:20 3:4-0:3 3:4-4:6 5:5-21:21".

In other words, the colon separates start and end index, the dash separates the languages, and space separates the words. One word can align with zero, one, or multiple words in the other language, and the aligned words can be noncontiguous. When no alignment information is available, the Alignment element is empty. The method returns no error in that case.

To receive alignment information, specify `includeAlignment=true` on the query string.

 ```bash
curl -X POST "https://api.cognitive.microsofttranslator.com/translate?api-version=TODO&from=en&to=fr&includeAlignment=true" -H "Ocp-Apim-Subscription-Key: <client-secret>" -H "Content-Type: application/json; charset=UTF-8" -d "[{'Text':'The answer lies in machine translation.'}]"
```

The response is:

```json
[
    {
        "translations":[
            {
                "text":"La réponse se trouve dans la traduction automatique.",
                "to":"fr",
                "alignment":{"proj":"0:2-0:1 4:9-3:9 11:14-11:19 16:17-21:24 19:25-40:50 27:37-29:38 38:38-51:51"}
            }
        ]
    }
]
```

The alignment information starts with `0:2-0:1`, which means that the first three characters in the source text (`The`) map to the first two characters in the translated text (`La`).

#### Limitations

Obtaining alignment information is an experimental feature that we enabled for prototyping research and experiences with potential phrase mappings. Here are some of the notable restrictions where alignments aren't supported:

* Alignment isn't available for text in HTML format that is, textType=html
* Alignment is only returned for a subset of the language pairs:
  * English to/from any other language except Chinese Traditional, Cantonese (Traditional) or Serbian (Cyrillic)
  * from Japanese to Korean or from Korean to Japanese
  * from Japanese to Chinese Simplified and Chinese Simplified to Japanese
  * from Chinese Simplified to Chinese Traditional and Chinese Traditional to Chinese Simplified
* You don't alignment if the sentence is a canned translation. Example of a canned translation is `This is a test`, `I love you`, and other high frequency sentences
* Alignment isn't available when you apply any of the approaches to prevent translation as described [here](../../how-to/prevent-translation.md)

### Obtain sentence boundaries

To receive information about sentence length in the source text and translated text, specify `includeSentenceLength=true` on the query string.

 ```bash
curl -X POST "https://api.cognitive.microsofttranslator.com/translate?api-version=TODO&from=en&to=fr&includeSentenceLength=true" -H "Ocp-Apim-Subscription-Key: <client-secret>" -H "Content-Type: application/json; charset=UTF-8" -d "[{'Text':'The answer lies in machine translation. The best machine translation technology cannot always provide translations tailored to a site or users like a human. Simply copy and paste a code snippet anywhere.'}]"
```

The response is:

```json
[
    {
        "translations":[
            {
                "text":"La réponse se trouve dans la traduction automatique. La meilleure technologie de traduction automatique ne peut pas toujours fournir des traductions adaptées à un site ou des utilisateurs comme un être humain. Il suffit de copier et coller un extrait de code n'importe où.",
                "to":"fr",
                "sentLen":{"srcSentLen":[40,117,46],"transSentLen":[53,157,62]}
            }
        ]
    }
]
```

### Translate with dynamic dictionary

If you already know the translation you want to apply to a word or a phrase, you can supply it as markup within the request. The dynamic dictionary is only safe for proper nouns such as personal names and product names. **Note**: the dynamic dictionary feature is case-sensitive.

The markup to supply uses the following syntax.

```html
<mstrans:dictionary translation="translation of phrase">phrase</mstrans:dictionary>
```

For example, consider the English sentence "The word wordomatic is a dictionary entry." To preserve the word _wordomatic_ in the translation, send the request:

```http
curl -X POST "https://api.cognitive.microsofttranslator.com/translate?api-version=TODO&from=en&to=de" -H "Ocp-Apim-Subscription-Key: <client-secret>" -H "Content-Type: application/json; charset=UTF-8" -d "[{'Text':'The word <mstrans:dictionary translation=\"wordomatic\">wordomatic</mstrans:dictionary> is a dictionary entry.'}]"
```

The result is:

```json
[
    {
        "translations":[
            {"text":"Das Wort \"wordomatic\" ist ein Wörterbucheintrag.","to":"de"}
        ]
    }
]
```

This dynamic-dictionary feature works the same way with `textType=text` or with `textType=html`. The feature should be used sparingly. The appropriate and far better way of customizing translation is by using Custom Translator. Custom Translator makes full use of context and statistical probabilities. If you can create training data that shows your work or phrase in context, you get better results. [Learn more about Custom Translator](../../../custom-translator/concepts/customization.md).

## Next steps

> [!div class="nextstepaction"]
> [Try the Translator quickstart](../../quickstart/rest-api.md)
