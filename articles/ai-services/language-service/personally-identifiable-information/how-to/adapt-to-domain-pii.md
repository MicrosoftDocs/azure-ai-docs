---
title: Adapt Personally Identifying Information (PII) to your domain
titleSuffix: Foundry Tools
description: This article shows you how to adapt Personally Identifying Information (PII) to your domain.
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: how-to
ms.date: 11/18/2025
ms.author: lajanuar
ms.custom: language-service-pii
---
# Adapt Personally Identifying Information (PII) to your domain

To support using your own terminology to identify entities (also known as *context*), the `entitySynonyms` feature enables you to define custom synonyms for specific entity types. This feature helps the system detect entities that appear in your inputs using terms or vocabulary that the model doesn't recognize by default. Aligning your specific terms with standard entities allows the model to accurately recognize and link these terms during entity detection.

This custom vocabulary support enhances the prebuilt PII (Personally Identifiable Information) detection service, which is originally trained on general language and may not understand specialized or informal vocabulary—such as using *BAN* instead of *InternationalBankAccountNumber*. As a result, PII detection is capable of recognizing sensitive information even when it appears in slang, abbreviations, or informal language. This detection enhancement strengthens the system's ability to safeguard privacy in everyday, real-world scenarios.

We strongly recommend that you first test the accuracy of the entity detection feature without adding synonyms. Then only introduce custom synonyms if the model doesn't perform well with the default settings. For instance, if the model already recognizes *Org* as *organization*, there's no need to add it as a synonym.

Once you test the service with your own data, you can use `entitySynonyms` to:

* Identify specific [entities within the prebuilt service](../concepts/entity-categories.md) that require custom synonym context words from your input vocabulary.
* Provide a list of custom synonyms for context entities.
* Specify the language of each synonym.

## API Schema for the 'entitySynonyms' parameter

```json
{
    "parameter":
    "entitySynonyms": [
        {
            "entityType": "InternationalBankAccountNumber",
            "synonyms": [ {"synonym": "BAN", "language": "en"} ]
        }
    ]
}
```

## Usage guidelines

1. Synonyms must be restricted to phrases that directly refer to the type, and preserve semantic correctness. For example, for the entity type `InternationalBankAccountNumber`, a valid synonym could be "Financial Account Number" or *FAN*. But, the word *deposit* though may be associated with type, as it doesn't directly have a meaning of a bank account number and therefore shouldn't be used.
1. Synonyms should be country/region agnostic. For example, *German passport* wouldn't be helpful to include.
1. Synonyms can't be reused for more than one entity type.
1. This synonym recognition feature only accepts a subset of entity types supported by the service. The supported entity types and example synonyms include:

|Supported entity type|Entity Type|Example synonyms|
|--|--|--|
|ABA Routing Number|ABARoutingNumber|Routing transit number (RTN)|
|Address|Address|My place is|
|Age|Age|Years old, age in years, current age, person's age, biological age|
|Bank Account Number|BankAccountNumber|Bank acct no., savings account number, checking account number, financial account number|
|Credit Card Number|CreditCardNumber|Cc number, payment card number, credit acct no.|
|Date|DateTime|Given date, specified date|
|Date of Birth|DateOfBirth|Birthday, DOB, birthdate|
|International Bank Account Number|InternationalBankingAccountNumber|IBAN, intl bank acct no.|
|Organization|Organization|company, business, firm, corporation, agency, group, institution, entity, legal entity, party, respondent, plaintiff, defendant, jurisdiction, partner, provider, facility, practice, network, institution, enterprise, LLC, Inc, LLP, incorporated, employer, brand, subsidiary|
|Person|Person|Name, individual, account holder|
|Person Type|PersonType|Role, title, position|
|Phone number|PhoneNumber|Landline, cell, mobile|
|Swift Code|SWIFTCode|SWIFT code, BIC (Bank Identifier Code), SWIFT Identifier|

## Customizing PII output by specifying values to exclude

The `valueExclusionPolicy` option allows you to adapt the PII service for scenarios where certain preferred terms can be undetected and redacted even if those terms fall into a PII category you're interested in detecting. For example, a police department might want personal identifiers redacted in most cases except for terms like *police officer*, *suspect*, and *witness*.

In the following example, you can use the `valueExclusionPolicy` option to specify a list of values that you wouldn't like to be detected or redacted from the input text. In the next example, if the user enters the value *1 Microsoft Way, Redmond, WA 98052, US*, this value isn't redacted. It also isn't included in the returned API payload output, even if the `Address` entity is enabled.

A subset of the specified excluded value, such as *One Microsoft Way* isn't excluded.

### Input
```json
{
  "kind": "PiiEntityRecognition",
  "parameters": {
    "modelVersion": "latest",
    "redactionPolicy": {
      "policyKind": "characterMask",
      "redactionCharacter": "-"
    },
    "valueExclusionPolicy": {
      "caseSensitive": false,
      "excludedValues": {
        "1 Microsoft Way, Redmond, WA 98052",
        "1045 La Avenida St, Mountain View, CA 94043"
      }
    }
  },
  "analysisInput": {
    "documents": [
      {
        "id": "1",
        "text": "The police and John Doe inspected the storage garages located at 123 Main St, 1 Microsoft Way, Redmond, WA 98052, 456 Washington Blvd, Portland, OR, and 1045 La Avenida St, Mountain View, CA 94043"
      }
    ]
  }
}
```

### Output
```json
{
    "kind": "PiiEntityRecognitionResults",
    "results": {
        "documents": [
            {
                "redactedText": "The police and John Doe inspected the storage garages located at **********, 1 Microsoft Way, Redmond, WA 98052, ********************************, and 1045 La Avenida St, Mountain View, CA 94043"
                "id": "1",
                "entities": [
                    {
                        "text": "John Doe",
                        "category": "Person",
                        "offset": 16,
                        "length": 5,
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
## Customizing PII detection using your own regex (only available for Text PII container)

You can now adapt the PII service's detecting by specifying your own regex using a regex recognition configuration file. See our [container how-to guides](../concepts/entity-categories.md) for a tutorial on how to install and run Personally Identifiable Information (PII) Detection containers.

> [!NOTE]
> Regex specification is only available for the Text PII container.

```bash
docker run --rm -it -p 5000:5000 --memory 8g --cpus 1 \
mcr.microsoft.com/azure-cognitive-services/textanalytics/pii:{IMAGE_TAG} \
Eula=accept \
Billing={ENDPOINT_URI} \
ApiKey={API_KEY} \
UserRegexRuleFilePath={REGEX_RULE_FILE_PATH}
```

`UserRegexRuleFilePath` is the file path of the user defined regex rules.

### Regex recognition file format
```json
[
    {
      "name": "USSocialSecurityNumber", // category, type and tag to be returned. This name must be unique
      "description": "Rule to identify USSocialSecurityNumber in text", // used to describe the category
      "regexPatterns": [ // list of regex patterns to identify the entities
        {
          "id": "StrongSSNPattern", // id for the regex pattern
          "pattern": "(?<!\\d)([0-9]{3}-[0-9]{2}-[0-9]{4}|[0-9]{3} [0-9]{2} [0-9]{4}|[0-9]{3}.[0-9]{2}.[0-9]{4})(?!\\d)", // regex pattern to provide matches
          "matchScore": 0.65, // score to assign if the regex matches
          "locales": [ // list of languages valid for this regex
            "en"
         ]
        },
        {
          "id": "WeakSSNPattern",
          "pattern": "(?<!\\d)([0-9]{9})(?!\\d)",
          "matchScore": 0.55,
          "locales": [
            "en"
          ]
        }
      ],
      "matchContext": { // patterns to give matches context
        "hints": [
          {
            "hintText": "ssa(\\s*)number", // regex pattern to find to give a match context.
            "boostingScore": 0.2, // score to boost match confidence if hint is found
            "locales": [ // list of languages valid for this context
              "en"
            ]
          },
          {
            "hintText": "social(\\s*)security(\\s*)(#*)",
            "boostingScore": 0.2,
            "locales": [
              "en"
            ]
          }
        ],
      }
    }
]
```

### Overview of each regex recognition file parameter

|Parameter      |Subparameters and Descriptions                                                |
|-----------------|-------------------------------------------------------------|
|`name`         |Category, type, and tag to return if there's a regex match.|
|`decription`   |(optional) User-readable rule description.                 |
|`regexPatterns`|List of regex patterns used to find entities.<br>* `id`: Identifier of the regex pattern.<br>- `matchScore`: Confidence score for regex matches.<br>* `locales`: Languages valid for the regex pattern.|
|`matchcontext` |Regex patterns providing context to matched entities. Context matching is a bidirectional search from the matched entity that increases confidence score in when found. If multiple hints support a match, the hint with the highest score is used.<br>* `hints`: List of regex patterns giving context to matched entities.<br>* `hintText`: Regex pattern providing context to matched entities.<br>* `boostingScore`: (optional) Score added to confidence score from a matched entity.<br>* `locales`: Language valid for hintText.<br>* `contextLimit`: (optional) Distance from the matched entity to search for context.|

### Logging

To display information about the running `regexRules`, add the following property to enable debug logging: `Logging:Console:LogLevel:Default=Debug`

```bash
docker run --rm -it -p 5000:5000 --memory 8g --cpus 1 \
mcr.microsoft.com/azure-cognitive-services/textanalytics/pii:{IMAGE_TAG} \
Eula=accept \
Billing={ENDPOINT_URI} \
ApiKey={API_KEY} \
UserRegexRuleFilePath={REGEX_RULE_FILE_PATH} \
Logging:Console:LogLevel:Default=Debug
```

### Regex rule constraints

- Rule names must begin with *CE_*
- Rule names must be unique.
- Rule names may only use alphanumeric characters and underscores (*_*)
- Regex patterns follow the .NET regular Expressions format. For more information, see [our documentation on .NET regular expressions](/dotnet/standard/base-types/regular-expressions).
