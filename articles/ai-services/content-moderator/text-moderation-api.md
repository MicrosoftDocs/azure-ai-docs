---
title: Text Moderation - Content Moderator
titleSuffix: Azure AI services
description: Use text moderation to detect potentially unwanted text, personal data, and custom lists of terms.
#services: cognitive-services
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-content-moderator
ms.topic: conceptual
ms.date: 11/06/2024
ms.author: pafarley

---

# Text moderation concepts

[!INCLUDE [deprecation notice](includes/tool-deprecation.md)]

You can use Azure Content Moderator's text moderation models to analyze text content, such as chat rooms, discussion boards, chatbots, e-commerce catalogs, and documents.

The service response includes the following information:

- Profanity: term-based matching with built-in list of profane terms in various languages
- Classification: machine-assisted classification into three categories
- Personal data
- Autocorrected text
- Original text
- Language

## Profanity

If the API detects any profane terms in any of the [supported languages](./language-support.md), those terms are included in the response. The response also contains their location (`Index`) in the original text. The `ListId` in the following sample JSON refers to terms found in custom term lists if available.

```json
"Terms": [
    {
        "Index": 118,
        "OriginalIndex": 118,
        "ListId": 0,
        "Term": "<offensive word>"
    }
```

> [!NOTE]
> For the `language` parameter, assign `eng` or leave it empty to see the machine-assisted *classification* response (preview feature). **This feature supports English only**.
>
> For *profanity terms* detection, use the [ISO 639-3 code](http://www-01.sil.org/iso639-3/codes.asp) of the supported languages listed in this article, or leave it empty.

## Classification

Content Moderator's machine-assisted *text classification feature* supports *English only*, and helps detect potentially undesired content. The flagged content might be assessed as inappropriate depending on context. It conveys the likelihood of each category. The feature uses a trained model to identify possible abusive, derogatory, or discriminatory language. This includes slang, abbreviated words, offensive, and intentionally misspelled words.

The following extract in the JSON extract shows an example output:

```json
"Classification": {
    "ReviewRecommended": true,
    "Category1": {
        "Score": 1.5113095059859916E-06
    },
    "Category2": {
        "Score": 0.12747249007225037
    },
    "Category3": {
        "Score": 0.98799997568130493
    }
}
```

### Explanation

- `Category1` refers to the potential presence of language that might be considered sexually explicit or adult in certain situations.
- `Category2` refers to the potential presence of language that might be considered sexually suggestive or mature in certain situations.
- `Category3` refers to the potential presence of language that might be considered offensive in certain situations.
- `Score` is between 0 and 1. The higher the score, the higher the probability that the category might be applicable. This feature relies on a statistical model rather than manually coded outcomes. We recommend testing with your own content to determine how each category aligns to your requirements.
- `ReviewRecommended` is either true or false depending on the internal score thresholds. Customers should assess whether to use this value or decide on custom thresholds based on their content policies.

## Personal data

The personal data feature detects the potential presence of this information:

- Email address
- US mailing address
- IP address
- US phone number

The following example shows a sample response:

```json
"pii":{
  "email":[
      {
        "detected":"abcdef@abcd.com",
        "sub_type":"Regular",
        "text":"abcdef@abcd.com",
        "index":32
      }
  ],
  "ssn":[

  ],
  "ipa":[
      {
        "sub_type":"IPV4",
        "text":"255.255.255.255",
        "index":72
      }
  ],
  "phone":[
      {
        "country_code":"US",
        "text":"6657789887",
        "index":56
      }
  ],
  "address":[
      {
        "text":"1 Microsoft Way, Redmond, WA 98052",
        "index":89
      }
  ]
}
```

## Autocorrection

The text moderation response can optionally return the text with basic autocorrection applied. 

For example, the following input text has a misspelling.

> The quick brown fox jumps over the lazzy dog.

If you specify autocorrection, the response contains the corrected version of the text:

> The quick brown fox jumps over the lazy dog.

## Create and manage your custom lists of terms

While the default, global list of terms works great for most cases, you might want to screen against terms that are specific to your business needs. For example, you might want to filter out any competitive brand names from posts by users.

> [!NOTE]
> There is a maximum limit of *five term lists* with each list to *not exceed 10,000 terms*.
>

The following example shows the matching List ID:

```json
"Terms": [
    {
        "Index": 118,
        "OriginalIndex": 118,
        "ListId": 231.
        "Term": "<offensive word>"
    }
```

The Content Moderator provides a [Term List API](/rest/api/cognitiveservices/contentmoderator/list-management-term-lists) with operations for managing custom term lists. Check out the [Term Lists .NET quickstart](term-lists-quickstart-dotnet.md) if you're familiar with Visual Studio and C#.

## Related content

- [Quickstart: Use the Content Moderator client library](client-libraries.md)
