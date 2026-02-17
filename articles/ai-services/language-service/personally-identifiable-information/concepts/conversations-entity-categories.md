---
title: Entity categories recognized by Conversational Personally Identifiable Information (PII) detection in Azure Language in Foundry Tools
titleSuffix: Foundry Tools
description: Learn about the types of entities the conversational PII feature can detect and identify within conversation inputs.
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: concept-article
ms.date: 02/17/2026
ms.author: lajanuar
---
<!-- markdownlint-disable MD025 -->
# Recognized conversational **PII** entities

The Conversational Personally Identifiable Information (PII) detection API is a cloud-based solution that uses artificial intelligence (AI) and machine learning to help you detect and redact sensitive information from conversation inputs. The conversational **PII** API effectively detects and removes sensitive information from input conversations by categorizing personal details into specific, predefined entity types. This comprehensive approach not only safeguards sensitive data to ensure full compliance with privacy regulations, but also enables applications to process and utilize information with enhanced security, reliability, and efficiency.

> [!TIP]
> Try PII detection in text or conversations using the [Microsoft Foundry](https://ai.azure.com/explore/language) language playground.

### Language Support

The [PII language support page](../language-support.md) lists all languages available for the PII entities in this article. Any exceptions are noted for specific named entities.

Supported API versions:

* [**Stable 2024-11-01: Generally Available (GA)**](/rest/api/language/analyze-conversations/operation-groups?view=rest-language-analyze-conversations-2024-11-01&preserve-view=true)
* [**Preview: 2025-11-15-preview**](/rest/api/language/analyze-conversations/operation-groups?view=rest-language-analyze-conversations-2025-11-15-preview&preserve-view=true)

The following entities are currently in preview:

* [ABARoutingNumber](#type-aba-routing-number-preview)
* [Age](#type-age-preview)
* [BankAccountNumber](#type-bank-account-number-preview)
* [CASocialInsuranceNumber](#type-canada-social-insurance-number-preview)
* [CVV (Card Verification Value)](#type-card-verification-value-cvv-preview)
* [Date](#type-date-preview)
* [DateOfBirth](#type-date-of-birth-preview)
* [DriversLicenseNumber](#type-drivers-license-number-preview)
* [GithubAccount](#type-github-account-preview)
* [GovernmentIssuedId](#type-government-issued-id-preview)
* [GPE (Geopolitical Entity)](#type-geopolitical-entity-gpe-preview)
* [HealthCardNumber](#type-health-card-number-preview)
* [InternationalBankingAccountNumber](#type-international-banking-account-number-preview)
* [Location](#type-location-preview)
* [Organization](#type-organization-preview)
* [PassportNumber](#type-passport-number-preview)
* [PersonType](#type-person-type-preview)
* [SWIFTCode](#type-swift-code-preview)
* [USMedicareBeneficiaryId](#type-united-states-medicare-beneficiary-id-preview)
* [VehicleIdentificationNumber](#type-vehicle-identification-number-preview)
* [ZipCode](#type-zipcode-preview)

### Supported conversational PII entity list

To examine a comprehensive list of all the types of conversational PII entities that are currently supported, *see* the [Supported conversational PII entity list](conversations-entity-categories-list.md)

### Supported conversational PII extraction entities

Personally identifiable information (PII) refers to any single piece of data or combination of data that enables the unique identification, tracking, or differentiation of an individual.

The Azure Language in Foundry Tools conversational PII extraction API uses Natural Language Processing (NLP) technology to detect, recognize, and extract PII entities from conversations. The following entities represent specific types of information that can reveal an individual's identity:

## Type: Geolocation

Data that details an individual's physical location that can be used to pinpoint or monitor where a person is or has been. This data is considered PII when it is linked to a specific person.

### Type: Geopolitical Entity GPE (preview)

|Details|Tag|
|---|---|
|To retrieve this entity type, specify **GPE** in the **piiCategories** request parameter. If detected, the entity appears in the **conversational PII** response payloads.|[GPE]|

### Type: Location (preview)

|Details|Tag|
|---|---|
|To retrieve this entity type, specify **Location** in the **piiCategories** request parameter. If detected, the entity appears in the **conversational PII** response payloads.|[Location]|

### Type: ZipCode (preview)

|Details|Tag|
|---|---|
|To retrieve this entity type, specify **ZipCode** in the **piiCategories** request parameter. If detected, the entity appears in the **conversational PII** response payloads.|[ZipCode]|

## Personal

Any data, collected or stored, that can be used to identify or contact a specific individual is considered personal information. This data may include information that identifies someone directly, such as their name or social security number. It can also refer to data that, when linked with other information, could lead to identification---for example, an address or dates of birth.

### Type: Address

|Details|Tag|
|---|---|
|To retrieve this entity type, specify **Address** in the **piiCategories** request parameter. If detected, the entity appears in the **conversational PII** response payloads.|[Address]|

### Type: Age (preview)

|Details|Tag|
|---|---|
|To retrieve this entity type, specify **Age** in the **piiCategories** request parameter. If detected, the entity appears in the **conversational PII** response payload.|[Age]|

### Type: Date Of Birth (preview)

|Details|Tag|
|---|---|
|To retrieve this entity type, specify **DateOfBirth** in the **piiCategories** request parameter. If detected, the entity appears in the **conversational PII** response payload.|[DateOfBirth]|

### Type: Drivers License Number (preview)

|Details|Tag|
|---|---|
|To retrieve this entity type, specify **DriversLicenseNumber** in the **piiCategories** request parameter. If detected, the entity appears in the **conversational PII** response payload.|[DriversLicenseNumber]|

### Type: Email

|Details|Tag|
|---|---|
|To retrieve this entity type, specify **Email** in the **piiCategories** request parameter. If detected, the entity appears in the **conversational PII** response payloads.|[Email]|

### Type: Passport Number (preview)

|Details|Tag|
|---|---|
|To retrieve this entity type, specify **PassportNumber** in the **piiCategories** request parameter. If detected, the entity appears in the **conversational PII** response payload.|[PassportNumber]|

### Type: Person

|Details|Tag|
|---|---|
|To retrieve this entity type, specify **Person** in the **piiCategories** request parameter. If detected, the entity appears in the **conversational PII** response payloads.|[Person]|

### Type: Person Type (preview)

|Details|Tag|
|---|---|
|To retrieve this entity type, specify **PersonType** in the **piiCategories** request parameter. If detected, the entity appears in the **conversational PII** response payload.|[PersonType]|

### Type: Phone Number

|Details|Tag|
|---|---|
|To retrieve this entity type, specify **Phone** in the **piiCategories** request parameter. If detected, the entity appears in the **conversational PII** response payloads.|[Phone]|

### Type: Vehicle Identification Number (preview)

|Details|Tag|
|---|---|
|To retrieve this entity type, specify **VehicleIdentificationNumber** in the **piiCategories** request parameter. If detected, the entity appears in the **conversational PII** response payload.|[VehicleIdentificationNumber]|

## Financial

Any financial information is connected to a particular individual that can, through identifying details, be traced back to that person.

### Type: ABA Routing Number (preview)

|Details|Tag|
|---|---|
|To retrieve this entity type, specify **ABARoutingNumber** in the **piiCategories** request parameter. If detected, the entity appears in the **conversational PII** response payload.|[ABARoutingNumber]|

### Type: Bank Account Number (preview)

|Details|Tag|
|---|---|
|To retrieve this entity type, specify **BankAccountNumber** in the **piiCategories** request parameter. If detected, the entity appears in the **conversational PII** response payload.|[BankAccountNumber]|

### Type: Card Verification Value CVV (preview)

|Details|Tag|
|---|---|
|To retrieve this entity type, specify **CVV** in the **piiCategories** request parameter. If detected, the entity appears in the **conversational PII** response payload.|[CVV]|

### Type: Credit Card

|Details|Tag|
|---|---|
|To retrieve this entity type, specify **CreditCard** in the **piiCategories** request parameter. If detected, the entity appears in the **conversational PII** response payload.|[CreditCard]|

### Type: International Banking Account Number (preview)

|Details|Tag|
|---|---|
|To retrieve this entity type, specify **InternationalBankingAccountNumber** in the **piiCategories** request parameter. If detected, the entity appears in the **conversational PII** response payload.|[InternationalBankingAccountNumber]|

### Type: SWIFT Code (preview)

|Details|Tag|
|---|---|
|To retrieve this entity type, specify **SWIFTCode** in the **piiCategories** request parameter. If detected, the entity appears in the **conversational PII** response payload.|[SWIFTCode]|

## Organization

Any data that an organization collects, stores, or processes that can be used to identify a specific individual, either directly or indirectly.

### Type: Organization (preview)

|Details|Tag|
|---|---|
|To retrieve this entity type, specify **Organization** in the **piiCategories** request parameter. If detected, the entity appears in the **conversational PII** response payloads.|[Organization]|

## DateTime

Data that can be used to identify, distinguish, or trace an individual. While a date or time on its own is often not considered PII, it can become highly sensitive when combined with other data points.

### Type: Date (preview)

|Details|Tag|
|---|---|
|To retrieve this entity type, specify **Date** in the **piiCategories** request parameter. If detected, the entity appears in the **conversational PII** response payloads.|[Date]|

## IT-related

Any identifiable IT-related information that can be used to distinguish or trace an individual's identity.

### Type: GitHub Account (preview)

|Details|Tag|
|---|---|
|To retrieve this entity type, specify **GithubAccount** in the **piiCategories** request parameter. If detected, the entity appears in the **conversational PII** response payload.|[GithubAccount]|

### Type: Numeric Identifier

|Details|Tag|
|---|---|
|To retrieve this entity type, specify **NumericIdentifier** in the **piiCategories** request parameter. If detected, the entity appears in the **conversational PII** response payload. Covers numeric or alphanumeric identifiers such as case numbers, member numbers, ticket numbers, bank account numbers, IP addresses, product keys, serial numbers, and shipping tracking numbers.|[NumericIdentifier]|

## Government

Any government-issued identification that can be used alone or combined with other data to trace and reveal a specific person's identity.

### Type: Canada Social Insurance Number (preview)

|Details|Tag|
|---|---|
|To retrieve this entity type, specify **CASocialInsuranceNumber** in the **piiCategories** request parameter. If detected, the entity appears in the **conversational PII** response payload.|[CASocialInsuranceNumber]|

### Type: Government Issued ID (preview)

|Details|Tag|
|---|---|
|To retrieve this entity type, specify **GovernmentIssuedId** in the **piiCategories** request parameter. If detected, the entity appears in the **conversational PII** response payload.|[GovernmentIssuedId]|

### Type: Health Card Number (preview)

|Details|Tag|
|---|---|
|To retrieve this entity type, specify **HealthCardNumber** in the **piiCategories** request parameter. If detected, the entity appears in the **conversational PII** response payload.|[HealthCardNumber]|

### Type: United States Medicare Beneficiary ID (preview)

|Details|Tag|
|---|---|
|To retrieve this entity type, specify **USMedicareBeneficiaryId** in the **piiCategories** request parameter. If detected, the entity appears in the **conversational PII** response payload.|[USMedicareBeneficiaryId]|

### Type: United States Social Security Number

|Details|Tag|
|---|---|
|To retrieve this entity type, specify **USSocialSecurityNumber** in the **piiCategories** request parameter. If detected, the entity appears in the **conversational PII** response payload.|[USSocialSecurityNumber]|


## Related content

[Conversational PII entity categories list](conversations-entity-categories-list.md)