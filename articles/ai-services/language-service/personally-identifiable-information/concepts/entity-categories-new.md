---
title: Entity categories recognized by Personally Identifiable Information (PII) and Protected Health Information (PHI) detection in Azure AI Language
titleSuffix: Azure AI services
description: Learn about the types of entities the PII feature can detect and identify within unstructured text.
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: conceptual
ms.date: 10/01/2025
ms.author: lajanuar
ms.custom:
  - language-service-pii
  - sfi-ropc-nochange
---

# Recognized **PII** and **PHI** entities

The Personally Identifiable Information (PII) and Protected Health Information (PHI) detection APIs are cloud-based solutions that use artificial intelligence (AI) and machine learning to help you create smart applications with advanced natural language processing. The **PII** and **PHI** APIs effectively detect and removes sensitive information from input data by categorizing personal details into specific, predefined entity types. This comprehensive approach not only safeguards sensitive data to ensure full compliance with privacy regulations, but also enables applications to process and utilize information with enhanced security, reliability, and efficiency.

> [!TIP]
> Try PII detection in text or conversations using the [Azure AI Foundry](https://ai.azure.com/explore/language) language playground.

## Language Support

The [PII language support page](../language-support.md) lists all languages available for the PII entities in this article. Any exceptions are noted for specific named entities.

Supported API versions:

* [**Preview: 2025-05-15-preview**](/rest/api/language/text-analysis-runtime/analyze-text?view=rest-language-2025-05-15-preview&preserve-view=true&tabs=HTTP#entitycategory)
* [**Stable: Generally Available (GA)**](/rest/api/language/text-analysis-runtime/analyze-text?view=rest-language-2024-11-01&preserve-view=truetabs=HTTP#entitycategory)

> [!NOTE]
> Beginning with the GA API (released `2024-11-01`), the **Subtype** field is no longer supported. All entity classifications now use the **type** field.

### Supported PII entity list

To examine a comprehensive list of all the types of Personally Identifiable Information (PII) entities that are currently supported, *see* the [Supported PII entity list](list-entity-categories.md)

### Supported PII extraction entities

Personally identifiable information (PII) refers to any single piece of data or combination of data that enables the unique identification, tracking, or differentiation of an individual.

The Azure Language PII extraction API uses Natural Language Processing (NLP) technology to detect, recognize, and extract PII entities from written text or spoken conversations. The following entities represent specific types of information that can reveal an individual's identity:

## Personal

Any data, collected or stored, that can be used to identify or contact a specific individual is considered personal information. This may include information that identifies someone directly, such as their name or social security number. It can also refer to data that, when linked with other information, could lead to identification—for example, an address or dates of birth.).

### Type: Address

|Details|Tag|
|---|---|
|To retrieve this entity type, specify **Address** in the **piiCategories** request parameter. If **Address** is detected, It appears in the **PII** and **PHI** response payloads. |[Address]|

### Type: Age

|Details|Tag|
|---|---|
|To retrieve this entity type, specify **Age** in the **piiCategories** request parameter. If **Age** is detected, It appears in the **PII** response payload.|[Age]|

### Type: Date Of Birth

|Details|Tag|
|---|---|
|To retrieve this entity type, specify **DateOfBirth** in the **piiCategories** request parameter. If **DateOfBirth** is detected, It appears in the **PII** response payload.|[DateOfBirth]|

### Type: Drivers License Number

|Details|Tag|
|---|---|
|To retrieve this entity type, specify **DriversLicenseNumber** in the **piiCategories** request parameter. If **DriversLicenseNumber** is detected, It appears in the **PII** response payload.|[DriversLicenseNumber]|

### Type: Email

|Details|Tag|
|---|---|
|To retrieve this entity type, specify **Email** in the **piiCategories** request parameter. If **Email** is detected, It appears in the **PII** and **PHI** response payloads.|[Email]|

### Type: IP Address

|Details|Tag|
|---|---|
|To retrieve this entity type, specify **IPAddress** in the **piiCategories** request parameter. If **IPAddress** is detected, It appears in the **PII** and **PHI** response payloads.|[IPAddress]|

### Type: License Plate

|Details|Tag|
|---|---|
|To retrieve this entity type, specify **LicensePlate** in the **piiCategories** request parameter. If **LicensePlate** is detected, It appears in the **PII** response payload.|[LicensePlate]|

### Type: Neighborhood

|Details|Tag|
|---|---|
|To retrieve this entity type, specify **Neighborhood** in the **piiCategories** request parameter. If **Neighborhood** is detected, It appears in the **PII** response payload.|[Neighborhood]|

### Type: Passport Number

|Details|Tag|
|---|---|
|To retrieve this entity type, specify **PassportNumber** in the **piiCategories** request parameter. If **PassportNumber** is detected, It appears in the **PII** response payload.|[PassportNumber]|

### Type: Person

|Details|Tag|
|---|---|
|To retrieve this entity type, specify **Person** in the **piiCategories** request parameter. If **Person** is detected, It appears in the **PII** response payloads.|[Person]|

### Type: Phone Number

|Details|Tag|
|---|---|
|To retrieve this entity type, specify **PhoneNumber** in the **piiCategories** request parameter. If **PhoneNumber** is detected, It appears in the **PII** and **PHI** response payloads.|[PhoneNumber]|

### Type: PIN

|Details|Tag|
|---|---|
|To retrieve this entity type, specify **PIN** in the **piiCategories** request parameter. If **PIN** is detected, It appears in the **PII** response payload.|[PIN]|

### Type: URL

|Details|Tag|
|---|---|
|To retrieve this entity type, specify **URL** in the **piiCategories** request parameter. If **URL** is detected, It appears in the **PII** and **PHI** response payloads.|[URL]|

### Type: VIN

|Details|Tag|
|---|---|
|To retrieve this entity type, specify **VIN** in the **piiCategories** request parameter. If **VIN** is detected, It appears in the **PII** response payload.|[VIN]|

## Financial

Any financial information is connected to a particular individual that can, through identifying details, be traced back to that person. 


### Type: ABA Routing Number

|Issuer|Details|Tag|
|---|---|---|
|American Bankers Association (ABA)|To retrieve this entity type, specify **ABARoutingNumber** in the **piiCategories** request parameter. If **ABARoutingNumber** is detected, It appears in the **PII** response payload.|[ABARoutingNumber]|

### Type: Bank Account Number

|Details|Tag|
|---|---|
|To retrieve this entity type, specify **BankAccountNumber** in the **piiCategories** request parameter. If **BankAccountNumber** is detected, It appears in the **PII** response payload.|[BankAccountNumber]|

### Type: Credit Card Number

|Details|Tag|
|---|---|
|To retrieve this entity type, specify **CreditCardNumber** in the **piiCategories** request parameter. If **CreditCardNumber** is detected, It appears in the **PII** response payload.|[CreditCardNumber]|

### Type: International Banking Account Number

|Details|Tag|
|---|---|
|To retrieve this entity type, specify **InternationalBankingAccountNumber** in the **piiCategories** request parameter. If **InternationalBankingAccountNumber** is detected, It appears in the **PII** response payload.|[InternationalBankingAccountNumber]|

### Type: Sort Code

|Details|Tag|
|---|---|
|To retrieve this entity type, specify **SortCode** in the **piiCategories** request parameter. If **SortCode** is detected, It appears in the **PII** response payload.|[SortCode]|

### Type: SWIFT Code

|Details|Tag|
|---|---|
|To retrieve this entity type, specify **SWIFTCode** in the **piiCategories** request parameter. If **SWIFTCode** is detected, It appears in the **PII** response payload.|[SWIFTCode]|

## Organization

Any data that an organization collects, stores, or processes that can be used to identify a specific individual, either directly or indirectly. 

### Type: Organization

|Details|Tag|
|---|---|
|To retrieve this entity type, specify **Organization** in the **piiCategories** request parameter. If **Organization** is detected, It appears in the **PII** and **PHI** response payloads.|[Organization]|

## DateTime

 Data that can be used to identify, distinguish, or trace an individual. While a date or time on its own is often not considered PII, it can become highly sensitive when combined with other data points.

### Type: Date

|Details|Tag|
|---|---|
|To retrieve this entity type, specify **Date** in the **piiCategories** request parameter. If **Date** is detected, It appears in the **PII** and **PHI** response payloads.|[Date]|

## Azure-related

Any identifiable Azure information like authentication information and connection strings that can be used to distinguish or trace an individual's identity.

### Type: Azure Document DB Auth Key

|Issuer|Details|Tag|
|---|---|---|
|Microsoft|To retrieve this entity type, specify **AzureDocumentDBAuthKey** in the **piiCategories** request parameter. If **AzureDocumentDBAuthKey** is detected, It appears in the **PII** response payload.|[AzureDocumentDBAuthKey]|

### Type: Azure IAAS Database Connection And SQL String

|Issuer|Details|Tag|
|---|---|---|
|Microsoft|To retrieve this entity type, specify **AzureIAASDatabaseConnectionAndSQLString** in the **piiCategories** request parameter. If **AzureIAASDatabaseConnectionAndSQLString** is detected, It appears in the **PII** response payload.|[AzureIAASDatabaseConnectionAndSQLString]|

### Type: Azure IoT Connection String

|Issuer|Details|Tag|
|---|---|---|
|Microsoft|To retrieve this entity type, specify **AzureIoTConnectionString** in the **piiCategories** request parameter. If **AzureIoTConnectionString** is detected, It appears in the **PII** response payload.|[AzureIoTConnectionString]|

### Type: Azure Publish Setting Password

|Issuer|Details|Tag|
|---|---|---|
|Microsoft|To retrieve this entity type, specify **AzurePublishSettingPassword** in the **piiCategories** request parameter. If **AzurePublishSettingPassword** is detected, It appears in the **PII** response payload.|[AzurePublishSettingPassword]|

### Type: Azure Redis Cache String

|Issuer|Details|Tag|
|---|---|---|
|Microsoft|To retrieve this entity type, specify **AzureRedisCacheString** in the **piiCategories** request parameter. If **AzureRedisCacheString** is detected, It appears in the **PII** response payload.|[AzureRedisCacheString]|

### Type: Azure SAS

|Issuer|Details|Tag|
|---|---|---|
|Microsoft|To retrieve this entity type, specify **AzureSAS** in the **piiCategories** request parameter. If **AzureSAS** is detected, It appears in the **PII** response payload.|[AzureSAS]|

### Type: Azure Service Bus String

|Issuer|Details|Tag|
|---|---|---|
|Microsoft|To retrieve this entity type, specify **AzureServiceBusString** in the **piiCategories** request parameter. If **AzureServiceBusString** is detected, It appears in the **PII** response payload.|[AzureServiceBusString]|

### Type: Azure Storage Account Generic

|Issuer|Details|Tag|
|---|---|---|
|Microsoft|To retrieve this entity type, specify **AzureStorageAccountGeneric** in the **piiCategories** request parameter. If **AzureStorageAccountGeneric** is detected, It appears in the **PII** response payload.|[AzureStorageAccountGeneric]|

### Type: Azure Storage Account Key

|Issuer|Details|Tag|
|---|---|---|
|Microsoft|To retrieve this entity type, specify **AzureStorageAccountKey** in the **piiCategories** request parameter. If **AzureStorageAccountKey** is detected, It appears in the **PII** response payload.|[AzureStorageAccountKey]|

### Type: SQL Server Connection String

|Issuer|Details|Tag|
|---|---|---|
|Microsoft|To retrieve this entity type, specify **SQLServerConnectionString** in the **piiCategories** request parameter. If **SQLServerConnectionString** is detected, It appears in the **PII** response payload.|[AzureStorageAccountKey]|


## Government-related

Any government-issued identification that can be used along or combined with other data to trace and reveal a specific person's identity.

### Type: AR National Identity Number

|Issuer|Details|Tag|
|---|---|---|
|Argentina|To retrieve this entity type, specify **ARNationalIdentityNumber** in the **piiCategories** request parameter. If **ARNationalIdentityNumber** is detected, It appears in the **PII** response payload.|[ARNationalIdentityNumber]|

### Type: AT Identity Card

|Issuer|Details|Tag|
|---|---|---|
|Austria|To retrieve this entity type, specify **ATIdentityCard** in the **piiCategories** request parameter. If **ATIdentityCard** is detected, It appears in the **PII** response payload.|[ATIdentityCard]|

### Type: AT Tax Identification Number

|Issuer|Details|Tag|
|---|---|---|
|Austria|To retrieve this entity type, specify **ATTaxIdentificationNumber** in the **piiCategories** request parameter. If **ATTaxIdentificationNumber** is detected, It appears in the **PII** response payload.|[ATTaxIdentificationNumber]|

### Type: AT Value Added Tax Number

|Issuer|Details|Tag|
|---|---|---|
|Austria|To retrieve this entity type, specify **ATValueAddedTaxNumber** in the **piiCategories** request parameter. If **ATValueAddedTaxNumber** is detected, It appears in the **PII** response payload.|[ATValueAddedTaxNumber]|

### Type: AU Bank Account Number

|Issuer|Details|Tag|
|---|---|---|
|Australia|To retrieve this entity type, specify **AUBankAccountNumber** in the **piiCategories** request parameter. If **AUBankAccountNumber** is detected, It appears in the **PII** response payload.|[AUBankAccountNumber]|

### Type: AU Business Number

|Issuer|Details|Tag|
|---|---|---|
|Australia|To retrieve this entity type, specify **AUBusinessNumber** in the **piiCategories** request parameter. If **AUBusinessNumber** is detected, It appears in the **PII** response payload.|[AUBusinessNumber]|

### Type: AU Company Number

|Issuer|Details|Tag|
|---|---|---|
|Australia|To retrieve this entity type, specify **AUCompanyNumber** in the **piiCategories** request parameter. If **AUCompanyNumber** is detected, It appears in the **PII** response payload.|[AUCompanyNumber]|

### Type: AU Drivers License Number

|Issuer|Details|Tag|
|---|---|---|
|Australia|To retrieve this entity type, specify **AUDriversLicenseNumber** in the **piiCategories** request parameter. If **AUDriversLicenseNumber** is detected, It appears in the **PII** response payload.|[AUDriversLicenseNumber]|

### Type: AU Medical Account Number

|Issuer|Details|Tag|
|---|---|---|
|Australia|To retrieve this entity type, specify **AUMedicalAccountNumber** in the **piiCategories** request parameter. If **AUMedicalAccountNumber** is detected, It appears in the **PII** response payload.|[AUMedicalAccountNumber]|

### Type: AU Passport Number

|Issuer|Details|Tag|
|---|---|---|
|Australia|To retrieve this entity type, specify **AUPassportNumber** in the **piiCategories** request parameter. If **AUPassportNumber** is detected, It appears in the **PII** response payload.|[AUPassportNumber]|

### Type: AU Tax File Number

|Issuer|Details|Tag|
|---|---|---|
|Australia|To retrieve this entity type, specify **AUTaxFileNumber** in the **piiCategories** request parameter. If **AUTaxFileNumber** is detected, It appears in the **PII** response payload.|[AUTaxFileNumber]|

### Type: BE National Number

|Issuer|Details|Tag|
|---|---|---|
|Belgium|To retrieve this entity type, specify **BENationalNumber** in the **piiCategories** request parameter. If **BENationalNumber** is detected, It appears in the **PII** response payload.|[BENationalNumber]|

### Type: BE National Number V2

|Issuer|Details|Tag|
|---|---|---|
|Belgium|To retrieve this entity type, specify **BENationalNumberV2** in the **piiCategories** request parameter. If **BENationalNumberV2** is detected, It appears in the **PII** response payload.|[BENationalNumberV2]|

### Type: BE Value Added Tax Number

|Issuer|Details|Tag|
|---|---|---|
|Belgium|To retrieve this entity type, specify **BEValueAddedTaxNumber** in the **piiCategories** request parameter. If **BEValueAddedTaxNumber** is detected, It appears in the **PII** response payload.|[BEValueAddedTaxNumber]|

### Type: BG Uniform Civil Number

|Issuer|Details|Tag|
|---|---|---|
|Bulgaria|To retrieve this entity type, specify **BGUniformCivilNumber** in the **piiCategories** request parameter. If **BGUniformCivilNumber** is detected, It appears in the **PII** response payload.|[BGUniformCivilNumber]|

### Type: BR CPF Number

|Issuer|Details|Tag|
|---|---|---|
|Brazil|To retrieve this entity type, specify **BRCPFNumber** in the **piiCategories** request parameter. If **BRCPFNumber** is detected, It appears in the **PII** response payload.|[BRCPFNumber]|

### Type: BR Legal Entity Number

|Issuer|Details|Tag|
|---|---|---|
|Brazil|To retrieve this entity type, specify **BRLegalEntityNumber** in the **piiCategories** request parameter. If **BRLegalEntityNumber** is detected, It appears in the **PII** response payload.|[BRLegalEntityNumber]|

### Type: BR National IDRG

|Issuer|Details|Tag|
|---|---|---|
|Brazil|To retrieve this entity type, specify **BRNationalIDRG** in the **piiCategories** request parameter. If **BRNationalIDRG** is detected, It appears in the **PII** response payload.|[BRNationalIDRG]|

### Type: CA Bank Account Number

|Issuer|Details|Tag|
|---|---|---|
|Canada|To retrieve this entity type, specify **CABankAccountNumber** in the **piiCategories** request parameter. If **CABankAccountNumber** is detected, It appears in the **PII** response payload.|[CABankAccountNumber]|

### Type: CA Drivers License Number

|Issuer|Details|Tag|
|---|---|---|
|Canada|To retrieve this entity type, specify **CADriversLicenseNumber** in the **piiCategories** request parameter. If **CADriversLicenseNumber** is detected, It appears in the **PII** response payload.|[CADriversLicenseNumber]|

### Type: CA Health Service Number

|Issuer|Details|Tag|
|---|---|---|
|Canada|To retrieve this entity type, specify **CAHealthServiceNumber** in the **piiCategories** request parameter. If **CAHealthServiceNumber** is detected, It appears in the **PII** response payload.|[CAHealthServiceNumber]|

### Type: CA Passport Number

|Issuer|Details|Tag|
|---|---|---|
|Canada|To retrieve this entity type, specify **CAPassportNumber** in the **piiCategories** request parameter. If **CAPassportNumber** is detected, It appears in the **PII** response payload.|[CAPassportNumber]|

### Type: CA Personal Health Identification

|Issuer|Details|Tag|
|---|---|---|
|Canada|To retrieve this entity type, specify **CAPersonalHealthIdentification** in the **piiCategories** request parameter. If **CAPersonalHealthIdentification** is detected, It appears in the **PII** and **PHI** response payload.|[CAPersonalHealthIdentification]|

### Type: CA Social Insurance Number

|Issuer|Details|Tag|
|---|---|---|
|Canada|To retrieve this entity type, specify **CASocialInsuranceNumber** in the **piiCategories** request parameter. If **CASocialInsuranceNumber** is detected, It appears in the **PII** response payload.|[CASocialInsuranceNumber]|

### Type: CH Social Security Number

|Issuer|Details|Tag|
|---|---|---|
|Switzerland|To retrieve this entity type, specify **CHSocialSecurityNumber** in the **piiCategories** request parameter. If **CHSocialSecurityNumber** is detected, It appears in the **PII** response payload.|[CHSocialSecurityNumber]|

### Type: CL Identity Card Number

|Issuer|Details|Tag|
|---|---|---|
|Chile|To retrieve this entity type, specify **CLIdentityCardNumber** in the **piiCategories** request parameter. If **CLIdentityCardNumber** is detected, It appears in the **PII** response payload.|[CLIdentityCardNumber]|

### Type: CN Resident Identity Card Number

|Issuer|Details|Tag|
|---|---|---|
|China|To retrieve this entity type, specify **CNResidentIdentityCardNumber** in the **piiCategories** request parameter. If **CNResidentIdentityCardNumber** is detected, It appears in the **PII** response payload.|[CNResidentIdentityCardNumber]|

### Type: CY Identity Card

|Issuer|Details|Tag|
|---|---|---|
|Cyprus|To retrieve this entity type, specify **CYIdentityCard** in the **piiCategories** request parameter. If **CYIdentityCard** is detected, It appears in the **PII** response payload.|[CYIdentityCard]|

### Type: CY Tax Identification Number

|Issuer|Details|Tag|
|---|---|---|
|Cyprus|To retrieve this entity type, specify **CYTaxIdentificationNumber** in the **piiCategories** request parameter. If **CYTaxIdentificationNumber** is detected, It appears in the **PII** response payload.|[CYTaxIdentificationNumber]|

### Type: CZ Personal Identity Number

|Issuer|Details|Tag|
|---|---|---|
|Czech Republic|To retrieve this entity type, specify **CZPersonalIdentityNumber** in the **piiCategories** request parameter. If **CZPersonalIdentityNumber** is detected, It appears in the **PII** response payload.|[CZPersonalIdentityNumber]|

### Type: CZ Personal Identity V2

|Issuer|Details|Tag|
|---|---|---|
|Czech Republic|To retrieve this entity type, specify **CZPersonalIdentityV2** in the **piiCategories** request parameter. If **CZPersonalIdentityV2** is detected, It appears in the **PII** response payload.|[CZPersonalIdentityV2]|

### Type: DE Drivers License Number

|Issuer|Details|Tag|
|---|---|---|
|Germany|To retrieve this entity type, specify **DEDriversLicenseNumber** in the **piiCategories** request parameter. If **DEDriversLicenseNumber** is detected, It appears in the **PII** response payload.|[DEDriversLicenseNumber]|

### Type: DE Identity Card Number

|Issuer|Details|Tag|
|---|---|---|
|Germany|To retrieve this entity type, specify **DEIdentityCardNumber** in the **piiCategories** request parameter. If **DEIdentityCardNumber** is detected, It appears in the **PII** response payload.|[DEIdentityCardNumber]|

### Type: DE Passport Number

|Issuer|Details|Tag|
|---|---|---|
|Germany|To retrieve this entity type, specify **DEPassportNumber** in the **piiCategories** request parameter. If **DEPassportNumber** is detected, It appears in the **PII** response payload.|[DEPassportNumber]|

### Type: DE Tax Identification Number

|Issuer|Details|Tag|
|---|---|---|
|Germany|To retrieve this entity type, specify **DETaxIdentificationNumber** in the **piiCategories** request parameter. If **DETaxIdentificationNumber** is detected, It appears in the **PII** response payload.|[DETaxIdentificationNumber]|

### Type: DE Value Added Number

|Issuer|Details|Tag|
|---|---|---|
|Germany|To retrieve this entity type, specify **DEValueAddedNumber** in the **piiCategories** request parameter. If **DEValueAddedNumber** is detected, It appears in the **PII** response payload.|[DEValueAddedNumber]|

### Type: DK Personal Identification Number

|Issuer|Details|Tag|
|---|---|---|
|Denmark|To retrieve this entity type, specify **DKPersonalIdentificationNumber** in the **piiCategories** request parameter. If **DKPersonalIdentificationNumber** is detected, It appears in the **PII** response payload.|[DKPersonalIdentificationNumber]|

### Type: DK Personal Identification V2

|Issuer|Details|Tag|
|---|---|---|
|Denmark|To retrieve this entity type, specify **DKPersonalIdentificationV2** in the **piiCategories** request parameter. If **DKPersonalIdentificationV2** is detected, It appears in the **PII** response payload.|[DKPersonalIdentificationV2]|

### Type: "Drug Enforcement Agency Number

|Issuer|Details|Tag|
|---|---|---|
|Denmark|To retrieve this entity type, specify **"DrugEnforcementAgencyNumber** in the **piiCategories** request parameter. If **DKPersonalIdentificationV2** is detected, It appears in the **PII** response payload.|["DrugEnforcementAgencyNumber]|

### Type: EE Personal Identification Code

|Issuer|Details|Tag|
|---|---|---|
|Estonia|To retrieve this entity type, specify **EEPersonalIdentificationCode** in the **piiCategories** request parameter. If **EEPersonalIdentificationCode** is detected, It appears in the **PII** response payload.|[EEPersonalIdentificationCode]|

### Type: ES DNI

|Issuer|Details|Tag|
|---|---|---|
|Spain|To retrieve this entity type, specify **ESDNI** in the **piiCategories** request parameter. If **ESDNI** is detected, It appears in the **PII** response payload.|[ESDNI]|

### Type: ES Social Security Number

|Issuer|Details|Tag|
|---|---|---|
|Spain|To retrieve this entity type, specify **ESSocialSecurityNumber** in the **piiCategories** request parameter. If **ESSocialSecurityNumber** is detected, It appears in the **PII** response payload.|[ESSocialSecurityNumber]|

### Type: ES Tax Identification Number

|Issuer|Details|Tag|
|---|---|---|
|Spain|To retrieve this entity type, specify **ESTaxIdentificationNumber** in the **piiCategories** request parameter. If **ESTaxIdentificationNumber** is detected, It appears in the **PII** response payload.|[ESTaxIdentificationNumber]|

### Type: EU Debit Card Number

|Issuer|Details|Tag|
|---|---|---|
|European Union|To retrieve this entity type, specify **EUDebitCardNumber** in the **piiCategories** request parameter. If **EUDebitCardNumber** is detected, It appears in the **PII** response payload.|[EUDebitCardNumber]|

### Type: EU Drivers License Number

|Issuer|Details|Tag|
|---|---|---|
|European Union|To retrieve this entity type, specify **EUDriversLicenseNumber** in the **piiCategories** request parameter. If **EUDriversLicenseNumber** is detected, It appears in the **PII** response payload.|[EUDriversLicenseNumber]|

### Type: EU GPS Coordinates

|Issuer|Details|Tag|
|---|---|---|
|European Union|To retrieve this entity type, specify **EUGPSCoordinates** in the **piiCategories** request parameter. If **EUGPSCoordinates** is detected, It appears in the **PII** response payload.|[EUGPSCoordinates]|

### Type: EU National Identification Number

|Issuer|Details|Tag|
|---|---|---|
|European Union|To retrieve this entity type, specify **EUNationalIdentificationNumber** in the **piiCategories** request parameter. If **EUNationalIdentificationNumber** is detected, It appears in the **PII** response payload.|[EUNationalIdentificationNumber]|

### Type: EU Passport Number

|Issuer|Details|Tag|
|---|---|---|
|European Union|To retrieve this entity type, specify **EUPassportNumber** in the **piiCategories** request parameter. If **EUPassportNumber** is detected, It appears in the **PII** response payload.|[EUPassportNumber]|

### Type: EU Social Security Number

|Issuer|Details|Tag|
|---|---|---|
|European Union|To retrieve this entity type, specify **EUSocialSecurityNumber** in the **piiCategories** request parameter. If **EUSocialSecurityNumber** is detected, It appears in the **PII** response payload.|[EUSocialSecurityNumber]|

### Type: EU Tax Identification Number

|Issuer|Details|Tag|
|---|---|---|
|European Union|To retrieve this entity type, specify **EUTaxIdentificationNumber** in the **piiCategories** request parameter. If **EUTaxIdentificationNumber** is detected, It appears in the **PII** response payload.|[EUTaxIdentificationNumber]|

### Type: FI European Health Number

|Issuer|Details|Tag|
|---|---|---|
|Finland|To retrieve this entity type, specify **FIEuropeanHealthNumber** in the **piiCategories** request parameter. If **FIEuropeanHealthNumber** is detected, It appears in the **PII** response payload.|[FIEuropeanHealthNumber]|

### Type: FI National ID

|Issuer|Details|Tag|
|---|---|---|
|Finland|To retrieve this entity type, specify **FINationalID** in the **piiCategories** request parameter. If **FINationalID** is detected, It appears in the **PII** response payload.|[FINationalID]|

### Type: FI National ID V2

|Issuer|Details|Tag|
|---|---|---|
|Finland|To retrieve this entity type, specify **FINationalIDV2** in the **piiCategories** request parameter. If **FINationalIDV2** is detected, It appears in the **PII** response payload.|[FINationalIDV2]|

### Type: FI Passport Number

|Issuer|Details|Tag|
|---|---|---|
|Finland|To retrieve this entity type, specify **FIPassportNumber** in the **piiCategories** request parameter. If **FIPassportNumber** is detected, It appears in the **PII** response payload.|[FIPassportNumber]|

### Type: FR Drivers License Number

|Issuer|Details|Tag|
|---|---|---|
|France|To retrieve this entity type, specify **FRDriversLicenseNumber** in the **piiCategories** request parameter. If **FRDriversLicenseNumber** is detected, It appears in the **PII** response payload.|[FRDriversLicenseNumber]|

### Type: FR Health Insurance Number

|Issuer|Details|Tag|
|---|---|---|
|France|To retrieve this entity type, specify **FRHealthInsuranceNumber** in the **piiCategories** request parameter. If **FRHealthInsuranceNumber** is detected, It appears in the **PII** response payload.|[FRHealthInsuranceNumber]|

### Type: FR National ID

|Issuer|Details|Tag|
|---|---|---|
|France|To retrieve this entity type, specify **FRNationalID** in the **piiCategories** request parameter. If **FRNationalID** is detected, It appears in the **PII** response payload.|[FRNationalID]|

### Type: FR Passport Number

|Issuer|Details|Tag|
|---|---|---|
|France|To retrieve this entity type, specify **FRPassportNumber** in the **piiCategories** request parameter. If **FRPassportNumber** is detected, It appears in the **PII** response payload.|[FRPassportNumber]|

### Type: FR Social Security Number

|Issuer|Details|Tag|
|---|---|---|
|France|To retrieve this entity type, specify **FRSocialSecurityNumber** in the **piiCategories** request parameter. If **FRSocialSecurityNumber** is detected, It appears in the **PII** response payload.|[FRSocialSecurityNumber]|

### Type: FR Tax Identification Number

|Issuer|Details|Tag|
|---|---|---|
|France|To retrieve this entity type, specify **FRTaxIdentificationNumber** in the **piiCategories** request parameter. If **FRTaxIdentificationNumber** is detected, It appears in the **PII** response payload.|[FRTaxIdentificationNumber]|

### Type: FR Value Added Tax Number

|Issuer|Details|Tag|
|---|---|---|
|France|To retrieve this entity type, specify **FRValueAddedTaxNumber** in the **piiCategories** request parameter. If **FRValueAddedTaxNumber** is detected, It appears in the **PII** response payload.|[FRValueAddedTaxNumber]|

### Type: GR National ID Card

|Issuer|Details|Tag|
|---|---|---|
|Greece|To retrieve this entity type, specify **GRNationalIDCard** in the **piiCategories** request parameter. If **GRNationalIDCard** is detected, It appears in the **PII** response payload.|[GRNationalIDCard]|

### Type: GR National ID V2

|Issuer|Details|Tag|
|---|---|---|
|Greece|To retrieve this entity type, specify **GRNationalIDV2** in the **piiCategories** request parameter. If **GRNationalIDV2** is detected, It appears in the **PII** response payload.|[GRNationalIDV2]|

### Type: GR Tax Identification Number

|Issuer|Details|Tag|
|---|---|---|
|Greece|To retrieve this entity type, specify **GRTaxIdentificationNumber** in the **piiCategories** request parameter. If **GRTaxIdentificationNumber** is detected, It appears in the **PII** response payload.|[GRTaxIdentificationNumber]|

### Type: HK Identity Card Number

|Issuer|Details|Tag|
|---|---|---|
|Hong Kong SAR|To retrieve this entity type, specify **HKIdentityCardNumber** in the **piiCategories** request parameter. If **HKIdentityCardNumber** is detected, It appears in the **PII** response payload.|[HKIdentityCardNumber]|

### Type: HR Identity Card Number

|Issuer|Details|Tag|
|---|---|---|
|Croatia|To retrieve this entity type, specify **HRIdentityCardNumber** in the **piiCategories** request parameter. If **HRIdentityCardNumber** is detected, It appears in the **PII** response payload.|[HRIdentityCardNumber]|

### Type: HR National ID Number

|Issuer|Details|Tag|
|---|---|---|
|Croatia|To retrieve this entity type, specify **HRNationalIDNumber** in the **piiCategories** request parameter. If **HRNationalIDNumber** is detected, It appears in the **PII** response payload.|[HRNationalIDNumber]|

### Type: HR Personal Identification Number

|Issuer|Details|Tag|
|---|---|---|
|Croatia|To retrieve this entity type, specify **HRPersonalIdentificationNumber** in the **piiCategories** request parameter. If **HRPersonalIdentificationNumber** is detected, It appears in the **PII** response payload.|[HRPersonalIdentificationNumber]|

### Type: HR Personal Identification OIB Number V2

|Issuer|Details|Tag|
|---|---|---|
|Croatia|To retrieve this entity type, specify **HRPersonalIdentificationOIBNumberV2** in the **piiCategories** request parameter. If **HRPersonalIdentificationOIBNumberV2** is detected, It appears in the **PII** response payload.|[HRPersonalIdentificationOIBNumberV2]|

### Type: HU Personal Identification Number

|Issuer|Details|Tag|
|---|---|---|
|Hungary|To retrieve this entity type, specify **HUPersonalIdentificationNumber** in the **piiCategories** request parameter. If **HUPersonalIdentificationNumber** is detected, It appears in the **PII** response payload.|[HUPersonalIdentificationNumber]|

### Type: HU Tax Identification Number

|Issuer|Details|Tag|
|---|---|---|
|Hungary|To retrieve this entity type, specify **HUTaxIdentificationNumber** in the **piiCategories** request parameter. If **HUTaxIdentificationNumber** is detected, It appears in the **PII** response payload.|[HUTaxIdentificationNumber]|

### Type: HU Value Added Number

|Issuer|Details|Tag|
|---|---|---|
|Hungary|To retrieve this entity type, specify **HUValueAddedNumber** in the **piiCategories** request parameter. If **HUValueAddedNumber** is detected, It appears in the **PII** response payload.|[HUValueAddedNumber]|

### Type: ID Identity Card Number

|Issuer|Details|Tag|
|---|---|---|
|Indonesia|To retrieve this entity type, specify **IDIdentityCardNumber** in the **piiCategories** request parameter. If **IDIdentityCardNumber** is detected, It appears in the **PII** response payload.|[IDIdentityCardNumber]|

### Type: IE Personal Public Service Number

|Issuer|Details|Tag|
|---|---|---|
|Ireland|To retrieve this entity type, specify **IEPersonalPublicServiceNumber** in the **piiCategories** request parameter. If **IEPersonalPublicServiceNumber** is detected, It appears in the **PII** response payload.|[IEPersonalPublicServiceNumber]|

### Type: IE Personal Public Service Number V2

|Issuer|Details|Tag|
|---|---|---|
|Ireland|To retrieve this entity type, specify **IEPersonalPublicServiceNumberV2** in the **piiCategories** request parameter. If **IEPersonalPublicServiceNumberV2** is detected, It appears in the **PII** response payload.|[IEPersonalPublicServiceNumberV2]|

### Type: IL Bank Account Number

|Issuer|Details|Tag|
|---|---|---|
|Israel|To retrieve this entity type, specify **ILBankAccountNumber** in the **piiCategories** request parameter. If **ILBankAccountNumber** is detected, It appears in the **PII** response payload.|[ILBankAccountNumber]|

### Type: IL National ID

|Issuer|Details|Tag|
|---|---|---|
|Israel|To retrieve this entity type, specify **ILNationalID** in the **piiCategories** request parameter. If **ILNationalID** is detected, It appears in the **PII** response payload.|[ILNationalID]|

### Type: IN Permanent Account

|Issuer|Details|Tag|
|---|---|---|
|India|To retrieve this entity type, specify **INPermanentAccount** in the **piiCategories** request parameter. If **INPermanentAccount** is detected, It appears in the **PII** response payload.|[INPermanentAccount]|

### Type: IN Unique Identification Number

|Issuer|Details|Tag|
|---|---|---|
|India|To retrieve this entity type, specify **INUniqueIdentificationNumber** in the **piiCategories** request parameter. If **INUniqueIdentificationNumber** is detected, It appears in the **PII** response payload.|[INUniqueIdentificationNumber]|

### Type: IT Drivers License Number

|Issuer|Details|Tag|
|---|---|---|
|Italy|To retrieve this entity type, specify **ITDriversLicenseNumber** in the **piiCategories** request parameter. If **ITDriversLicenseNumber** is detected, It appears in the **PII** response payload.|[ITDriversLicenseNumber]|

### Type: IT Fiscal Code

|Issuer|Details|Tag|
|---|---|---|
|Italy|To retrieve this entity type, specify **ITFiscalCode** in the **piiCategories** request parameter. If **ITFiscalCode** is detected, It appears in the **PII** response payload.|[ITFiscalCode]|

### Type: IT Value Added Tax Number

|Issuer|Details|Tag|
|---|---|---|
|Italy|To retrieve this entity type, specify **ITValueAddedTaxNumber** in the **piiCategories** request parameter. If **ITValueAddedTaxNumber** is detected, It appears in the **PII** response payload.|[ITValueAddedTaxNumber]|

### Type: JP Bank Account Number

|Issuer|Details|Tag|
|---|---|---|
|Japan|To retrieve this entity type, specify **JPBankAccountNumber** in the **piiCategories** request parameter. If **JPBankAccountNumber** is detected, It appears in the **PII** response payload.|[JPBankAccountNumber]|

### Type: JP Drivers License Number

|Issuer|Details|Tag|
|---|---|---|
|Japan|To retrieve this entity type, specify **JPDriversLicenseNumber** in the **piiCategories** request parameter. If **JPDriversLicenseNumber** is detected, It appears in the **PII** response payload.|[JPDriversLicenseNumber]|

### Type: JP My Number Corporate

|Issuer|Details|Tag|
|---|---|---|
|Japan|To retrieve this entity type, specify **JPMyNumberCorporate** in the **piiCategories** request parameter. If **JPMyNumberCorporate** is detected, It appears in the **PII** response payload.|[JPMyNumberCorporate]|

### Type: JP My Number Personal

|Issuer|Details|Tag|
|---|---|---|
|Japan|To retrieve this entity type, specify **JPMyNumberPersonal** in the **piiCategories** request parameter. If **JPMyNumberPersonal** is detected, It appears in the **PII** response payload.|[JPMyNumberPersonal]|

### Type: JP Passport Number

|Issuer|Details|Tag|
|---|---|---|
|Japan|To retrieve this entity type, specify **JPPassportNumber** in the **piiCategories** request parameter. If **JPPassportNumber** is detected, It appears in the **PII** response payload.|[JPPassportNumber]|

### Type: JP Residence Card Number

|Issuer|Details|Tag|
|---|---|---|
|Japan|To retrieve this entity type, specify **JPResidenceCardNumber** in the **piiCategories** request parameter. If **JPResidenceCardNumber** is detected, It appears in the **PII** response payload.|[JPResidenceCardNumber]|

### Type: JP Resident Registration Number

|Issuer|Details|Tag|
|---|---|---|
|Japan|To retrieve this entity type, specify **JPResidentRegistrationNumber** in the **piiCategories** request parameter. If **JPResidentRegistrationNumber** is detected, It appears in the **PII** response payload.|[JPResidentRegistrationNumber]|

### Type: JP Social Insurance Number

|Issuer|Details|Tag|
|---|---|---|
|Japan|To retrieve this entity type, specify **JPSocialInsuranceNumber** in the **piiCategories** request parameter. If **JPSocialInsuranceNumber** is detected, It appears in the **PII** response payload.|[JPSocialInsuranceNumber]|

### Type: KR Resident Registration Number

|Issuer|Details|Tag|
|---|---|---|
|South Korea|To retrieve this entity type, specify **KRResidentRegistrationNumber** in the **piiCategories** request parameter. If **KRResidentRegistrationNumber** is detected, It appears in the **PII** response payload.|[KRResidentRegistrationNumber]|

### Type: LT Personal Code

|Issuer|Details|Tag|
|---|---|---|
|Lithuania|To retrieve this entity type, specify **LTPersonalCode** in the **piiCategories** request parameter. If **LTPersonalCode** is detected, It appears in the **PII** response payload.|[LTPersonalCode]|

### Type: LU National Identification Number Natural

|Issuer|Details|Tag|
|---|---|---|
|Luxembourg|To retrieve this entity type, specify **LUNationalIdentificationNumberNatural** in the **piiCategories** request parameter. If **LUNationalIdentificationNumberNatural** is detected, It appears in the **PII** response payload.|[LUNationalIdentificationNumberNatural]|

### Type: LU National Identification Number Non Natural

|Issuer|Details|Tag|
|---|---|---|
|Luxembourg|To retrieve this entity type, specify **LUNationalIdentificationNumberNonNatural** in the **piiCategories** request parameter. If **LUNationalIdentificationNumberNonNatural** is detected, It appears in the **PII** response payload.|[LUNationalIdentificationNumberNonNatural]|

### Type: LV Personal Code

|Issuer|Details|Tag|
|---|---|---|
|Latvia|To retrieve this entity type, specify **LVPersonalCode** in the **piiCategories** request parameter. If **LVPersonalCode** is detected, It appears in the **PII** response payload.|[LVPersonalCode]|

### Type: MT Identity Card Number

|Issuer|Details|Tag|
|---|---|---|
|Malta|To retrieve this entity type, specify **MTIdentityCardNumber** in the **piiCategories** request parameter. If **MTIdentityCardNumber** is detected, It appears in the **PII** response payload.|[MTIdentityCardNumber]|

### Type: MT Tax ID Number

|Issuer|Details|Tag|
|---|---|---|
|Malta|To retrieve this entity type, specify **MTTaxIDNumber** in the **piiCategories** request parameter. If **MTTaxIDNumber** is detected, It appears in the **PII** response payload.|[MTTaxIDNumber]|

### Type: MY Identity Card Number

|Issuer|Details|Tag|
|---|---|---|
|Malaysia|To retrieve this entity type, specify **MYIdentityCardNumber** in the **piiCategories** request parameter. If **MYIdentityCardNumber** is detected, It appears in the **PII** response payload.|[MYIdentityCardNumber]|

### Type: NL Citizens Service Number

|Issuer|Details|Tag|
|---|---|---|
|Netherlands|To retrieve this entity type, specify **NLCitizensServiceNumber** in the **piiCategories** request parameter. If **NLCitizensServiceNumber** is detected, It appears in the **PII** response payload.|[NLCitizensServiceNumber]|

### Type: NL Citizens Service Number V2

|Issuer|Details|Tag|
|---|---|---|
|Netherlands|To retrieve this entity type, specify **NLCitizensServiceNumberV2** in the **piiCategories** request parameter. If **NLCitizensServiceNumberV2** is detected, It appears in the **PII** response payload.|[NLCitizensServiceNumberV2]|

### Type: NL Tax Identification Number

|Issuer|Details|Tag|
|---|---|---|
|Netherlands|To retrieve this entity type, specify **NLTaxIdentificationNumber** in the **piiCategories** request parameter. If **NLTaxIdentificationNumber** is detected, It appears in the **PII** response payload.|[NLTaxIdentificationNumber]|

### Type: NL Value Added Tax Number

|Issuer|Details|Tag|
|---|---|---|
|Netherlands|To retrieve this entity type, specify **NLValueAddedTaxNumber** in the **piiCategories** request parameter. If **NLValueAddedTaxNumber** is detected, It appears in the **PII** response payload.|[NLValueAddedTaxNumber]|

### Type: NO Identity Number

|Issuer|Details|Tag|
|---|---|---|
|Norway|To retrieve this entity type, specify **NOIdentityNumber** in the **piiCategories** request parameter. If **NOIdentityNumber** is detected, It appears in the **PII** response payload.|[NOIdentityNumber]|

### Type: NZ Bank Account Number

|Issuer|Details|Tag|
|---|---|---|
|New Zealand|To retrieve this entity type, specify **NZBankAccountNumber** in the **piiCategories** request parameter. If **NZBankAccountNumber** is detected, It appears in the **PII** response payload.|[NZBankAccountNumber]|

### Type: NZ Drivers License Number

|Issuer|Details|Tag|
|---|---|---|
|New Zealand|To retrieve this entity type, specify **NZDriversLicenseNumber** in the **piiCategories** request parameter. If **NZDriversLicenseNumber** is detected, It appears in the **PII** response payload.|[NZDriversLicenseNumber]|

### Type: NZ Inland Revenue Number

|Issuer|Details|Tag|
|---|---|---|
|New Zealand|To retrieve this entity type, specify **NZInlandRevenueNumber** in the **piiCategories** request parameter. If **NZInlandRevenueNumber** is detected, It appears in the **PII** response payload.|[NZInlandRevenueNumber]|

### Type: NZ Ministry Of Health Number

|Issuer|Details|Tag|
|---|---|---|
|New Zealand|To retrieve this entity type, specify **NZMinistryOfHealthNumber** in the **piiCategories** request parameter. If **NZMinistryOfHealthNumber** is detected, It appears in the **PII** response payload.|[NZMinistryOfHealthNumber]|

### Type: NZ Social Welfare Number

|Issuer|Details|Tag|
|---|---|---|
|New Zealand|To retrieve this entity type, specify **NZSocialWelfareNumber** in the **piiCategories** request parameter. If **NZSocialWelfareNumber** is detected, It appears in the **PII** response payload.|[NZSocialWelfareNumber]|

### Type: PH Unified Multi Purpose ID Number

|Issuer|Details|Tag|
|---|---|---|
|Philippines|To retrieve this entity type, specify **PHUnifiedMultiPurposeIDNumber** in the **piiCategories** request parameter. If **PHUnifiedMultiPurposeIDNumber** is detected, It appears in the **PII** response payload.|[PHUnifiedMultiPurposeIDNumber]|

### Type: PL Identity Card

|Issuer|Details|Tag|
|---|---|---|
|Poland|To retrieve this entity type, specify **PLIdentityCard** in the **piiCategories** request parameter. If **PLIdentityCard** is detected, It appears in the **PII** response payload.|[PLIdentityCard]|

### Type: PL National ID

|Issuer|Details|Tag|
|---|---|---|
|Poland|To retrieve this entity type, specify **PLNationalID** in the **piiCategories** request parameter. If **PLNationalID** is detected, It appears in the **PII** response payload.|[PLNationalID]|

### Type: PL National ID V2

|Issuer|Details|Tag|
|---|---|---|
|Poland|To retrieve this entity type, specify **PLNationalIDV2** in the **piiCategories** request parameter. If **PLNationalIDV2** is detected, It appears in the **PII** response payload.|[PLNationalIDV2]|

### Type: PL Passport Number

|Issuer|Details|Tag|
|---|---|---|
|Poland|To retrieve this entity type, specify **PLPassportNumber** in the **piiCategories** request parameter. If **PLPassportNumber** is detected, It appears in the **PII** response payload.|[PLPassportNumber]|

### Type: PL REGON Number

|Issuer|Details|Tag|
|---|---|---|
|Poland|To retrieve this entity type, specify **PLREGONNumber** in the **piiCategories** request parameter. If **PLREGONNumber** is detected, It appears in the **PII** response payload.|[PLREGONNumber]|

### Type: PL Tax Identification Number

|Issuer|Details|Tag|
|---|---|---|
|Poland|To retrieve this entity type, specify **PLTaxIdentificationNumber** in the **piiCategories** request parameter. If **PLTaxIdentificationNumber** is detected, It appears in the **PII** response payload.|[PLTaxIdentificationNumber]|

### Type: PT Citizen Card Number

|Issuer|Details|Tag|
|---|---|---|
|Portugal|To retrieve this entity type, specify **PTCitizenCardNumber** in the **piiCategories** request parameter. If **PTCitizenCardNumber** is detected, It appears in the **PII** response payload.|[PTCitizenCardNumber]|

### Type: PT Citizen Card Number V2

|Issuer|Details|Tag|
|---|---|---|
|Portugal|To retrieve this entity type, specify **PTCitizenCardNumberV2** in the **piiCategories** request parameter. If **PTCitizenCardNumberV2** is detected, It appears in the **PII** response payload.|[PTCitizenCardNumberV2]|

### Type: PT Tax Identification Number

|Issuer|Details|Tag|
|---|---|---|
|Portugal|To retrieve this entity type, specify **PTTaxIdentificationNumber** in the **piiCategories** request parameter. If **PTTaxIdentificationNumber** is detected, It appears in the **PII** response payload.|[PTTaxIdentificationNumber]|

### Type: RO Personal Numerical Code

|Issuer|Details|Tag|
|---|---|---|
|Romania|To retrieve this entity type, specify **ROPersonalNumericalCode** in the **piiCategories** request parameter. If **ROPersonalNumericalCode** is detected, It appears in the **PII** response payload.|[ROPersonalNumericalCode]|

### Type: RU Passport Number Domestic

|Issuer|Details|Tag|
|---|---|---|
|Russia|To retrieve this entity type, specify **RUPassportNumberDomestic** in the **piiCategories** request parameter. If **RUPassportNumberDomestic** is detected, It appears in the **PII** response payload.|[RUPassportNumberDomestic]|

### Type: RU Passport Number International

|Issuer|Details|Tag|
|---|---|---|
|Russia|To retrieve this entity type, specify **RUPassportNumberInternational** in the **piiCategories** request parameter. If **RUPassportNumberInternational** is detected, It appears in the **PII** response payload.|[RUPassportNumberInternational]|

### Type: SA National ID

|Issuer|Details|Tag|
|---|---|---|
|Saudi Arabia|To retrieve this entity type, specify **SANationalID** in the **piiCategories** request parameter. If **SANationalID** is detected, It appears in the **PII** response payload.|[SANationalID]|

### Type: SE National ID

|Issuer|Details|Tag|
|---|---|---|
|Sweden|To retrieve this entity type, specify **SENationalID** in the **piiCategories** request parameter. If **SENationalID** is detected, It appears in the **PII** response payload.|[SENationalID]|

### Type: SE National ID V2

|Issuer|Details|Tag|
|---|---|---|
|Sweden|To retrieve this entity type, specify **SENationalIDV2** in the **piiCategories** request parameter. If **SENationalIDV2** is detected, It appears in the **PII** response payload.|[SENationalIDV2]|

### Type: SE Passport Number

|Issuer|Details|Tag|
|---|---|---|
|Sweden|To retrieve this entity type, specify **SEPassportNumber** in the **piiCategories** request parameter. If **SEPassportNumber** is detected, It appears in the **PII** response payload.|[SEPassportNumber, PassportNumber]|

### Type: SE Tax Identification Number

|Issuer|Details|Tag|
|---|---|---|
|Sweden|To retrieve this entity type, specify **SETaxIdentificationNumber** in the **piiCategories** request parameter. If **SETaxIdentificationNumber** is detected, It appears in the **PII** response payload.|[SETaxIdentificationNumber]|

### Type: SG National Registration Identity Card Number

|Issuer|Details|Tag|
|---|---|---|
|Singapore|To retrieve this entity type, specify **SGNationalRegistrationIdentityCardNumber** in the **piiCategories** request parameter. If **SGNationalRegistrationIdentityCardNumber** is detected, It appears in the **PII** response payload.|[SGNationalRegistrationIdentityCardNumber]|

### Type: SI Tax Identification Number

|Issuer|Details|Tag|
|---|---|---|
|Slovenia|To retrieve this entity type, specify **SITaxIdentificationNumber** in the **piiCategories** request parameter. If **SITaxIdentificationNumber** is detected, It appears in the **PII** response payload.|[SITaxIdentificationNumber]|

### Type: SI Unique Master Citizen Number

|Issuer|Details|Tag|
|---|---|---|
|Slovenia|To retrieve this entity type, specify **SIUniqueMasterCitizenNumber** in the **piiCategories** request parameter. If **SIUniqueMasterCitizenNumber** is detected, It appears in the **PII** response payload.|[SIUniqueMasterCitizenNumber]|

### Type: SK Personal Number

|Issuer|Details|Tag|
|---|---|---|
|Slovakia|To retrieve this entity type, specify **SKPersonalNumber** in the **piiCategories** request parameter. If **SKPersonalNumber** is detected, It appears in the **PII** response payload.|[SKPersonalNumber]|

### Type: TH Population Identification Code

|Issuer|Details|Tag|
|---|---|---|
|Thailand|To retrieve this entity type, specify **THPopulationIdentificationCode** in the **piiCategories** request parameter. If **THPopulationIdentificationCode** is detected, It appears in the **PII** response payload.|[THPopulationIdentificationCode]|

### Type: TR National Identification Number

|Issuer|Details|Tag|
|---|---|---|
|Türkiye|To retrieve this entity type, specify **TRNationalIdentificationNumber** in the **piiCategories** request parameter. If **TRNationalIdentificationNumber** is detected, It appears in the **PII** response payload.|[TRNationalIdentificationNumber]|

### Type: TW National ID

|Issuer|Details|Tag|
|---|---|---|
|Taiwan|To retrieve this entity type, specify **TWNationalID** in the **piiCategories** request parameter. If **TWNationalID** is detected, It appears in the **PII** response payload.|[TWNationalID]|

### Type: TW Passport Number

|Issuer|Details|Tag|
|---|---|---|
|Taiwan|To retrieve this entity type, specify **TWPassportNumber** in the **piiCategories** request parameter. If **TWPassportNumber** is detected, It appears in the **PII** response payload.|[TWPassportNumber]|

### Type: TW Resident Certificate

|Issuer|Details|Tag|
|---|---|---|
|Taiwan|To retrieve this entity type, specify **TWResidentCertificate** in the **piiCategories** request parameter. If **TWResidentCertificate** is detected, It appears in the **PII** response payload.|[TWResidentCertificate]|

### Type: UA Passport Number Domestic

|Issuer|Details|Tag|
|---|---|---|
|Ukraine|To retrieve this entity type, specify **UAPassportNumberDomestic** in the **piiCategories** request parameter. If **UAPassportNumberDomestic** is detected, It appears in the **PII** response payload.|[UAPassportNumberDomestic]|

### Type: UA Passport Number International

|Issuer|Details|Tag|
|---|---|---|
|Ukraine|To retrieve this entity type, specify **UAPassportNumberInternational** in the **piiCategories** request parameter. If **UAPassportNumberInternational** is detected, It appears in the **PII** response payload.|[UAPassportNumberInternational]|

### Type: UK Drivers License Number

|Issuer|Details|Tag|
|---|---|---|
|United Kingdom|To retrieve this entity type, specify **UKDriversLicenseNumber** in the **piiCategories** request parameter. If **UKDriversLicenseNumber** is detected, It appears in the **PII** response payload.|[UKDriversLicenseNumber]|

### Type: UK Electoral Roll Number

|Issuer|Details|Tag|
|---|---|---|
|United Kingdom|To retrieve this entity type, specify **UKElectoralRollNumber** in the **piiCategories** request parameter. If **UKElectoralRollNumber** is detected, It appears in the **PII** response payload.|[UKElectoralRollNumber]|

### Type: UK National Health Number

|Issuer|Details|Tag|
|---|---|---|
|United Kingdom|To retrieve this entity type, specify **UKNationalHealthNumber** in the **piiCategories** request parameter. If **UKNationalHealthNumber** is detected, It appears in the **PII** response payload.|[UKNationalHealthNumber]|

### Type: UK National Insurance Number

|Issuer|Details|Tag|
|---|---|---|
|United Kingdom|To retrieve this entity type, specify **UKNationalInsuranceNumber** in the **piiCategories** request parameter. If **UKNationalInsuranceNumber** is detected, It appears in the **PII** response payload.|[UKNationalInsuranceNumber]|

### Type: UK Unique Taxpayer Number

|Issuer|Details|Tag|
|---|---|---|
|United Kingdom|To retrieve this entity type, specify **UKUniqueTaxpayerNumber** in the **piiCategories** request parameter. If **UKUniqueTaxpayerNumber** is detected, It appears in the **PII** response payload.|[UKUniqueTaxpayerNumber]|

### Type: US Bank Account Number

|Issuer|Details|Tag|
|---|---|---|
|United States|To retrieve this entity type, specify **USBankAccountNumber** in the **piiCategories** request parameter. If **USBankAccountNumber** is detected, It appears in the **PII** response payload.|[USBankAccountNumber]|

### Type: US Drivers License Number

|Issuer|Details|Tag|
|---|---|---|
|United States|To retrieve this entity type, specify **USDriversLicenseNumber** in the **piiCategories** request parameter. If **USDriversLicenseNumber** is detected, It appears in the **PII** response payload.|[USDriversLicenseNumber]|

### Type: US Individual Taxpayer Identification

|Issuer|Details|Tag|
|---|---|---|
|United States|To retrieve this entity type, specify **USIndividualTaxpayerIdentification** in the **piiCategories** request parameter. If **USIndividualTaxpayerIdentification** is detected, It appears in the **PII** response payload.|[USIndividualTaxpayerIdentification]|

### Type: US Social Security Number

|Issuer|Details|Tag|
|---|---|---|
|United States|To retrieve this entity type, specify **USSocialSecurityNumber** in the **piiCategories** request parameter. If **USSocialSecurityNumber** is detected, It appears in the **PII** response payload.|[USSocialSecurityNumber]|

### Type: US UK Passport Number

|Issuer|Details|Tag|
|---|---|---|
|United States/United Kingdom|To retrieve this entity type, specify **USUKPassportNumber** in the **piiCategories** request parameter. If **USUKPassportNumber** is detected, It appears in the **PII** response payload.|[USUKPassportNumber]|

### Type: ZA Identification Number

|Issuer|Details|Tag|
|---|---|---|
|South Africa|To retrieve this entity type, specify **ZAIdentificationNumber** in the **piiCategories** request parameter. If **ZAIdentificationNumber** is detected, It appears in the **PII** response payload.|[ZAIdentificationNumber]|

## Related content

[PII entity categories list](list-entity-categories.md)
