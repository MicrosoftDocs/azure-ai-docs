---
title: Adapt Personally Identifying Information (PII) to your domain
titleSuffix: Azure AI services
description: This article shows you how to adapt Personally Identifying Information (PII) to your domain.
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: how-to
ms.date: 04/29/2025
ms.author: lajanuar
ms.custom: language-service-pii
---

# Adapting Personally Identifying Information (PII) to your domain

## Overview

To accommodate and adapt to a customer’s custom vocabulary used to identify entities (also known as the "context"), the `entitySynonyms` feature allows customers to define their own synonyms for specific entity types. The goal of this feature is to help detect entities in contexts that the model isn't familiar with but are used in the customer’s inputs by ensuring that the customer’s unique terms are recognized and correctly associated during the detection process. 

This adapts the prebuilt PII service which is trained to detect entities based on general domain text which may not match a customer’s custom input vocabulary, such as writing "BAN" instead of "InternationalBankAccountNumber". 

This means PII detection can catch sensitive information even when it’s written in different styles, slang, or casual language. That makes the system better at protecting privacy in real-world situations. 

We strongly recommend that customers first test the quality of predictions without introducing synonyms and only use them if the model isn't performing well. For example, "Org" may be something that the model already understands as "organization" and there's no need to use the Synonym feature. 

After testing the service on their data, customers can use `entitySynonyms` to:

* Specify particular [entities within the prebuilt service](../concepts/entity-categories.md) for which there are custom synonym context words in their input vocabulary.
* List the custom synonyms.
* Specify the language of each synonym.

## API Schema for the 'entitySynoyms' parameter

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

1. Synonyms must be restricted to phrases that directly refer to the type, and preserve semantic correctness. For example, for the entity type `InternationalBankAccountNumber`, a valid synonym could be "Financial Account Number" or "FAN". But, the word "deposit" though may be associated with type, as it doesn't directly have a meaning of a bank account number and therefore shouldn't be used. 
1. Synonyms should be country agnostic. For example, "German passport" wouldn't be helpful to include.
1. Synonyms can't be reused for more than one entity type.
1. This synonym recognition feature only accepts a subset of entity types supported by the service. The supported entity types and example synonyms include:

| Supported entity type             | Entity Type                       | Example synonyms                                                                         |
|-----------------------------------|-----------------------------------|------------------------------------------------------------------------------------------|
| ABA Routing Number                | ABARoutingNumber                  | Routing transit number (RTN)                                                             |
| Address                           | Address                           | My place is                                                                              |
| Age                               | Age                               | Years old, age in years, current age, person’s age, biological age                       |
| Bank Account Number               | BankAccountNumber                 | Bank acct no., savings account number, checking account number, financial account number |
| Credit Card Number                | CreditCardNumber                  | Cc number, payment card number, credit acct no.                                          |
| Date                              | DateTime                          | Given date, specified date                                                               |
| Date of Birth                     | DateOfBirth                       | Birthday, DOB, birthdate                                                                 |
| International Bank Account Number | InternationalBankingAccountNumber | IBAN, intl bank acct no.                                                                 |
| Organization                      | Organization                      | company, business, firm, corporation, agency, group, institution, entity, legal entity, party, respondent, plaintiff, defendant, jurisdiction, partner, provider, facility, practice, network, institution, enterprise, LLC, Inc, LLP, incorporated, employer, brand, subsidiary |
| Person                            | Person                            | Name, individual, account holder |
| Person Type                       | PersonType                        | Role, title, position |
| Phone number                      | PhoneNumber                       | Landline, cell, mobile |
| Swift Code                        | SWIFTCode                         | SWIFT code, BIC (Bank Identifier Code), SWIFT Identifier |

## Customizing PII output by specifying values to exclude

The `valueExclusionPolicy` option allows customers to adapt the PII service for scenarios where customers prefer certain terms be undetected and redacted even if those terms fall into a PII category they're interested in detected. For example, a police department might want personal identifiers redacted in most cases except for terms like "police officer", "suspect", and "witness".  

In the following example, customers can use the `valueExclusionPolicy` option to specify a list of values which they wouldn't like to be detected or redacted from the input text. In the example below, if the user specifies the value "1 Microsoft Way, Redmond, WA 98052, US", even if the Address entity is turned-on, this value isn't redacted or listed in the returned API payload output. 

A subset of the specified excluded value, such as "1 Microsoft Way" isn't excluded.

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

Customers can now adapt the PII service’s detecting by specifying their own regex using a regex recognition configuration file. See our [container how-to guides](../concepts/entity-categories.md) for a tutorial on how to install and run Personally Identifiable Information (PII) Detection containers.

> [!NOTE]
> This only available for the Text PII container

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

| Parameter       | Subparameters and Descriptions                                                 |
|-----------------|-------------------------------------------------------------|
| `name`          | Category, type, and tag to return if there's a regex match. |
| `decription`    | (optional) User-readable rule description.                  |
| `regexPatterns` | List of regex patterns used to find entities.<br>- `id`: Identifier of the regex pattern.<br>- `matchScore`: Confidence score for regex matches.<br>- `locales`: Languages valid for the regex pattern.|
| `matchcontext`  | Regex patterns providing context to matched entities. Context matching is a bidirectional search from the matched entity that increases confidence score in case it's found.  If multiple hints are supporting a match the hint with the highest score is used.<br>- `hints`: List of regex patterns giving context to matched entities.<br>    - `hintText`: Regex pattern providing context to matched entities.<br>    - `boostingScore`: (optional) Score added to confidence score from a matched entity.<br>    - `locales`: Language valid for hintText.<br>- `contextLimit`: (optional) Distance from the matched entity to search for context. |

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

- Rule names must begin with "CE_"  
- Rule names must be unique. 
- Rule names may only use alphanumeric characters and underscores ("_")
- Regex patterns follow the .NET regular Expressions format. See [our documentation on .NET regular expressions](https://learn.microsoft.com/dotnet/standard/base-types/regular-expressions) for more information. 