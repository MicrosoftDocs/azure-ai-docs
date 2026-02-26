---
title: Identify and extract Personally Identifying Information (PII) from text
titleSuffix: Foundry Tools
description: This article shows you how to identify, extract, and redact Personally Identifying Information (PII) from text.
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: how-to
ms.date: 11/18/2025
ms.author: lajanuar
ms.custom: language-service-pii
---
<!-- markdownlint-disable MD025 -->
# Detect and redact Personally Identifying Information in text

Azure Language in Foundry Tools is a cloud-based service that applies Natural Language Processing (NLP) features to text-based data. The PII feature can evaluate unstructured text, extract, and redact sensitive information (PII) and health information (PHI) in text across several [predefined categories](../concepts/entity-categories.md).

## Development options

[!INCLUDE [development options](../includes/development-options.md)]

## Specify the PII detection model

By default, this feature uses the latest available AI model on your text. You can also configure your API requests to use a specific [model version](../../concepts/model-lifecycle.md).

## Input languages

When you submit input text to be processed, you can specify which of [the supported languages](../language-support.md) they're written in. If you don't specify a language, extraction defaults to English. The API may return offsets in the response to support different [multilingual and emoji encodings](../../concepts/multilingual-emoji-support.md).

##  Additional configuration parameters (2025-11-15-preview)

> [!IMPORTANT]
>
> * Azure Language in Foundry Tools public preview releases provide early access to features that are in active development.
> * Features, approaches, and processes may change, before General Availability (GA), based on user feedback.
> * Preview features are subject to the terms applicable to **Previews** as described in the [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms) and the [Microsoft Products and Services Data Protection Addendum (DPA)](https://www.microsoft.com/licensing/docs/view/microsoft-products-and-services-data-protection-addendum-dpa).

### Redaction policies

Starting with version `2025-11-15-preview` and onward, you can specify the `redactionPolicies` parameter to define which redaction policies are applied when processing text. You can include more than one policy in a single request, with one policy specified as the `defaultRedactionPolicy` and additional policy overrides for specified entities.

The policy field accepts four policy types:

> [!div class="checklist"]
>
> * [`SyntheticReplacement 🆕`](#syntheticreplacement-policy-type-)
> * [`CharacterMask` (default)](#charactermask-policy-type)
> * [`NoMask`](#nomask-policy-type)
> * [`EntityMask`](#entitymask-policy-type)

For more information, *see* [REST API PII task parameters](/rest/api/language/analyze-text/analyze-text/analyze-text?view=rest-language-analyze-text-2025-11-15-preview&preserve-view=true&tabs=HTTP#piitaskparameters).

<!-- markdownlint-disable MD001 -->
##### syntheticReplacement policy type 🆕

> [!IMPORTANT]
> The Azure Language in Foundry Tools Text Personally Identifiable Information (PII) detection **anonymization feature** (synthetic replacement) is currently available in `preview` and licensed to you as part of your Azure subscription. Your use of this feature is subject to the terms applicable to **Previews** as described in the [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms) and the [Microsoft Products and Services Data Protection Addendum (DPA)](https://www.microsoft.com/licensing/docs/view/microsoft-products-and-services-data-protection-addendum-dpa).

The **syntheticReplacement** policy type replaces a detected PII entity with a replacement value. For instance, an input like "John Doe received a call from 424-878-9193." can be transformed into "Sam Johnson received a call from 401-255-6901." These substitutes are randomly selected from a predefined set of alternative values.

   ```bash

   POST {Endpoint}/language/:analyze-text?api-version=2025-11-15-preview

         {
        "kind": "PiiEntityRecognition",
        "parameters": {
          "modelVersion": "latest",
          "redactionPolicies": [
            {
              "policyKind": "syntheticReplacement",
              "entityTypes": [
                       "Person",
                       "PhoneNumber"
              ]
            }
          ]
        }
      }
   ```

##### characterMask policy type

The **characterMask** policy type** enables you to mask **redactedText** using a specified character (for example, "*****") while preserving the length and offset of the original text. For instance, "******** received a call from ************"

> Additionally, there's also an optional field named `redactionCharacter` that allows you to specify the character used for redaction when applying the `characterMask` policy.

   ***Sample request***

   ```bash
      POST {Endpoint}/language/:analyze-text?api-version=2025-11-15-preview
              {
          "kind": "PiiEntityRecognition",
          "parameters": {
          "modelVersion": "latest",
              "redactionPolicies": [
                {
                  "policyKind": "characterMask",
                  "redactionCharacter": "-"
                }
              ]
            }
        }

   ```


##### noMask policy type

**noMask** policy type** enables you to return the response without including the `redactedText` field. For example, "John Doe received a call from 424-878-919."


   ***Sample request***

   ```bash
      POST {Endpoint}/language/:analyze-text?api-version=2025-11-15-preview

        {
       "kind": "PiiEntityRecognition",
       "parameters": {
         "modelVersion": "latest",
         "redactionPolicies": [
           {
             "policyKind": "noMask"
           }
         ]
       }
     }

   ```


##### entityMask policy type

The **entityMask** policy type** enables you to mask the detected PII entity text its corresponding entity type. For example, "[PERSON_1] received a call from [PHONENUMBER_1]."

   ```bash

      POST {Endpoint}/language/:analyze-text?api-version=2025-11-15-preview

         {
        "kind": "PiiEntityRecognition",
        "parameters": {
          "modelVersion": "latest",
          "redactionPolicies": [
            {
              "policyKind": "entityMask"
            }
          ]
        }
      }

   ```




To learn more, *see* [Transparency Note for Personally Identifiable Information (PII)](/azure/ai-foundry/responsible-ai/language-service/transparency-note-personally-identifiable-information).

### ConfidenceScoreThreshold 🆕

The PII feature currently redacts all detected entities, regardless of their confidence scores. Thus, entities with low confidence scores are also removed, even if retaining them is preferred. To enhance flexibility, you can configure a confidence threshold that determines the minimum confidence score an entity must have to remain in the output.


***Sample request***

```bash

    POST {Endpoint}/language/:analyze-text?api-version=2025-11-15-preview

         {
           "kind":"PiiEntityRecognition",
           "parameters":{
              "modelVersion":"latest",
              "confidenceScoreThreshold":{
                 "default":0.9,
                 "overrides":[
                    {
                       "value":0.8,
                       "entity":"USSocialSecurityNumber"
                    },
                    {
                       "value":0.6,
                       "entity":"Person",
                       "language":"en"
                    }
                 ]
              }
           }
        }
   ```
To learn more, *see* [REST API reference: ConfidenceScoreThreshold](/rest/api/language/analyze-text/analyze-text/analyze-text?view=rest-language-analyze-text-2025-11-15-preview&preserve-view=true&tabs=HTTP#confidencescorethreshold)

### DisableEntityValidation

When you use the PII service, it validates multiple entity types to ensure data integrity and minimize false positives. However, this strict validation can sometimes slow down workflows where validation isn't necessary. To give you more flexibility, we're introducing a parameter that lets you disable entity validation if you choose. By default, this parameter is set to false, which means strict entity validation remains in place. If you want to bypass entity validation for your requests, you can set the parameter to true.

***Sample request***

```bash


 POST {Endpoint}/language/:analyze-text?api-version=2025-11-15-preview

     {
        "kind":"PiiEntityRecognition",
        "parameters":{
           "modelVersion":"latest",
           "disableEntityValidation":"true | false"
        },
        "analysisInput":{
           "documents":[
              {
                 "id":"id01",
                 "text":"blah"
              }
           ]
        }
     }
```
To learn more, *see* [REST API reference: PiiTaskParameters](/rest/api/language/analyze-text/analyze-text/analyze-text?view=rest-language-analyze-text-2025-11-15-preview&preserve-view=true&tabs=HTTP#piitaskparameters)

## Select which entities to be returned

The API attempts to detect the [defined entity categories](../concepts/entity-categories.md) for a given input text language. If you want to specify which entities are detected and returned, use the optional `piiCategories` parameter with the appropriate entity categories. This parameter can also let you detect entities that aren't enabled by default for your input text language. The following example would detect only `Person`. You can specify one or more [entity types](../concepts/entity-categories.md) to be returned.

> [!TIP]
> If you don't include `default` when specifying entity categories, The API only returns the entity categories you specify.

**Input:**

> [!NOTE]
> In this example, it returns only the **person** entity type:

`https://<your-language-resource-endpoint>/language/:analyze-text?api-version=2022-05-01`

```bash
{
  "kind": "PiiEntityRecognition",
  "parameters": {
    "modelVersion": "latest",
    "piiCategories": [
      "Person"
    ],
    "redactionPolicies": {
      "policyKind": "characterMask",
      "redactionCharacter": "*"
       # MaskWithCharacter|MaskWithEntityType|DoNotRedact
    }
  },
  "analysisInput": {
    "documents": [
      {
        "id": "1",
        "language": "en",
        "text": "We went to Contoso foodplace located at downtown Seattle last week for a dinner party, and we adore the spot! They provide marvelous food and they have a great menu. The chief cook happens to be the owner (I think his name is John Doe) and he is super nice, coming out of the kitchen and greeted us all. We enjoyed very much dining in the place! The pasta I ordered was tender and juicy, and the place was impeccably clean. You can even pre-order from their online menu at www.contosofoodplace.com, call 112-555-0176 or send email to order@contosofoodplace.com! The only complaint I have is the food didn't come fast enough. Overall I highly recommend it!"
      }
    ]
  }
}
```

**Output:**

```bash

{
    "kind": "PiiEntityRecognitionResults",
    "results": {
        "documents": [
            {
                "redactedText": "We went to Contoso foodplace located at downtown Seattle last week for a dinner party, and we adore the spot! They provide marvelous food and they have a great menu. The chief cook happens to be the owner (I think his name is ********) and he is super nice, coming out of the kitchen and greeted us all. We enjoyed very much dining in the place! The pasta I ordered was tender and juicy, and the place was impeccably clean. You can even pre-order from their online menu at www.contosofoodplace.com, call 112-555-0176 or send email to order@contosofoodplace.com! The only complaint I have is the food didn't come fast enough. Overall I highly recommend it!",
                "id": "1",
                "entities": [
                    {
                        "text": "John Doe",
                        "category": "Person",
                        "offset": 226,
                        "length": 8,
                        "confidenceScore": 0.98
                    }
                ],
                "warnings": []
            }
        ],
        "errors": [],
        "modelVersion": "2021-01-15"
    }
}
```

## Adapting PII to your domain

To accommodate and adapt to a customer's custom vocabulary used to identify entities (also known as the "context"), the `entitySynonyms` feature allows customers to define their own synonyms for specific entity types.

This feature is designed to identify entities within contexts that may be unfamiliar to the model, especially terms specific to the customer's input. By doing so, it ensures that the customer's unique terminology is accurately recognized and properly linked during the detection process.

The `valueExclusionPolicy` option allows customers to adapt the PII service for scenarios where customers prefer certain terms not to be detected and redacted even if those terms fall into a PII category they're interested in detected. For example, a police department might want personal identifiers redacted in most cases except for terms like "police officer," "suspect," and "witness."

Customers can now adapt the PII service's detecting by specifying their own regex using a regex recognition configuration file. See our [container how-to guides](use-containers.md) for a tutorial on how to install and run Personally Identifiable Information (PII) Detection containers.

A more detailed tutorial can be found in the "[Adapting PII to your domain](adapt-to-domain-pii.md)" how-to guide.


## Submitting data

Analysis is performed upon receipt of the request. Using the PII detection feature synchronously is stateless. No data is stored in your account, and results are returned immediately in the response.

[!INCLUDE [asynchronous-result-availability](../../includes/async-result-availability.md)]

## Getting PII results

When you get results from PII detection, you can stream the results to an application or save the output to a file on the local system. The API response includes [recognized entities](../concepts/entity-categories.md), including their categories and subcategories, and confidence scores. The text string with the PII entities redacted is also returned.

## Service and data limits

[!INCLUDE [service limits article](../../includes/service-limits-link.md)]

## Next steps

[Personally Identifying Information (PII) overview](../overview.md)
