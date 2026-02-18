---
title: Personally Identifiable Information (PII) Filter
description: Learn about the Personally Identifiable Information (PII) filter for identifying and flagging known personal information in large language model outputs.
author: ssalgadodev
ms.author: ssalgado
ms.date: 02/18/2026
ms.topic: concept-article
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
monikerRange: 'foundry-classic || foundry'
ai-usage: ai-assisted
---

# Personally identifiable information (PII) filter

Personally identifiable information (PII) refers to any information that can be used to identify a particular individual, such as a name, address, phone number, email address, social security number, driver's license number, passport number, or similar information.

PII detection is used to help prevent PII from being exposed or shared, protecting users from identity theft, financial fraud, or other types of privacy violations.

In the context of large language models (LLMs), PII detection involves analyzing text content in LLM completions. When PII has been identified, it can be flagged for further review, or the output can be blocked. The PII filter scans the output of LLMs to identify and flag known personal information. It's designed to help organizations prevent the generation of content that closely matches sensitive personal information.

For example, if a model generates "Contact me at john@example.com or call 555-0123", the PII filter can detect and flag the email address and phone number before the content reaches the user.

> [!TIP]
> Use PII filtering to meet compliance requirements (GDPR, HIPAA, CCPA), prevent data leaks in customer-facing applications, and audit sensitive information exposure in model outputs.


## PII types

There are many different types of PII, and you can specify which types you want to filter. Common PII categories include:

- **Personal information**: Email, PhoneNumber, Address, Person, IPAddress, Date of Birth, Drivers License Number, Passport Number
- **Financial information**: Credit Card Number, Bank Account Number, SWIFT Code, IBAN
- **Government IDs**: Social Security Number (US), National ID numbers (50+ countries), Tax IDs, Passport numbers
- **Azure-related**: Connection strings, storage account keys, authentication keys
- **Geolocation**: Airport, City, State, specific locations

For the complete list of supported PII entity types, see [PII entity categories](/azure/ai-services/language-service/personally-identifiable-information/concepts/entity-categories).

## Filtering modes

The PII filter can be configured to operate in two modes:

- **Annotate** mode flags PII that's returned in the model output.
- **Annotate and Block** mode blocks the entire output if PII is detected.

The filtering mode can be set for each PII category individually.


## Next steps

- [Content filtering overview](content-filter.md)
- [Configure content filters](../how-to/content-filters.md)
- [PII entity categories](/azure/ai-services/language-service/personally-identifiable-information/concepts/entity-categories)
- [Responsible AI practices](../../responsible-ai/overview.md)
