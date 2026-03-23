---
title: Include file
description: Include file
author: scottpolly
ms.author: scottpolly
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 03/19/2026
ms.custom: include
---

Personally identifiable information (personal data) refers to any information that can be used to identify a particular individual, such as a name, address, phone number, email address, social security number, driver's license number, passport number, or similar information.

Personal data detection is used to help prevent personal data from being exposed or shared, protecting users from identity theft, financial fraud, or other types of privacy violations.

In the context of large language models (LLMs), personal data detection involves analyzing text content in LLM completions. When personal data has been identified, it can be flagged for further review, or the output can be blocked. The personal data filter scans the output of LLMs to identify and flag known personal information. It's designed to help organizations prevent the generation of content that closely matches sensitive personal information.

For example, if a model generates "Contact me at john@example.com or call 555-0123", the personal data filter can detect and flag the email address and phone number before the content reaches the user.

> [!TIP]
> Use personal data filtering to meet compliance requirements (HIPAA, CCPA), prevent data leaks in customer-facing applications, and audit sensitive information exposure in model outputs.

## Personal data types

There are many different types of personal data, and you can specify which types you want to filter. Common personal data categories include:

- **Personal information**: Email, PhoneNumber, Address, Person, IPAddress, Date of Birth, Drivers License Number, Passport Number
- **Financial information**: Credit Card Number, Bank Account Number, SWIFT Code, IBAN
- **Government IDs**: Social Security Number (US), National ID numbers (50+ countries), Tax IDs, Passport numbers
- **Azure-related**: Connection strings, storage account keys, authentication keys
- **Geolocation**: Airport, City, State, specific locations

For the complete list of supported personal data entity types, see [personal data entity categories](/azure/ai-services/language-service/personally-identifiable-information/concepts/entity-categories).

## Filtering modes

The personal data filter can be configured to operate in two modes:

- **Annotate** mode flags personal data that's returned in the model output.
- **Annotate and Block** mode blocks the entire output if personal data is detected.

The filtering mode can be set for each personal data category individually.

## Next steps

- [Content filtering overview](../../../foundry-classic/foundry-models/concepts/content-filter.md)
- [Configure content filters](../../../foundry-classic/openai/how-to/content-filters.md)
- [Personal data entity categories](/azure/ai-services/language-service/personally-identifiable-information/concepts/entity-categories)
