---
title: Entity categories recognized by Personally Identifiable Information (detection) in Azure AI Language
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

# Supported Personally Identifiable Information entities

The Personally Identifiable Information (PII) detection API is a cloud-based solution that uses artificial intelligence and machine learning to help you create smart applications with advanced natural language processing. The PII API effectively detects and removes sensitive information from input data by categorizing personal details into specific, predefined entity types. This comprehensive approach not only safeguards sensitive data to ensure full compliance with privacy regulations, but also enables applications to process and utilize information with enhanced security, reliability, and efficiency.

> [!TIP]
> Try PII detection in text or conversations using the [Azure AI Foundry](https://ai.azure.com/explore/language) language playground.

## Language Support

The [PII language support page](../language-support.md) lists all languages available for the PII entities in this article. Any exceptions are noted for specific named entities.

Supported API versions:

* [**Preview: 2025-08-15-preview**](/rest/api/language/text-analysis-runtime/analyze-text?view=rest-language-2025-05-15-preview&preserve-view=true&tabs=HTTP#entitycategory)
* [**Stable: Generally Available (GA)**](/rest/api/language/text-analysis-runtime/analyze-text?view=rest-language-2024-11-01&preserve-view=truetabs=HTTP#entitycategory)

> [!NOTE]
> Beginning with the GA API (released 2024-11-01), the **Subcategory** field is no longer supported. All entity classifications now use the **type** field.


## Supported PII entity list

To review a list of all supported PII entities, *see* [PII entity list](Entity-category-list.md)

## Supported PII entities

### Type: ABA Routing Number

|Issuer|Tag|
|---|---|
|American Bankers Association (ABA)| [ABARoutingNumber]  |


### Type: Address

|Issuer|Tag|
|---|---|
|Not applicable.| [Address]  |

### Type: Age

|Issuer|Tag|
|---|---|
|Not applicable.| [Age]  |

### Type: AR National Identity Number

|Issuer|Tag|
|---|---|
|Argentina| [ARNationalIdentityNumber]  |

### Type: AT Identity Card

|Issuer|Tag|
|---|---|
|Austria| [ATIdentityCard]  |

### Type: AT Tax Identification Number

|Issuer|Tag|
|---|---|
|Austria| [ATTaxIdentificationNumber]  |

### Type: AT Value Added Tax Number

|Issuer|Tag|
|---|---|
|Austria| [ATValueAddedTaxNumber]  |

### Type: AU Bank Account Number

|Issuer|Tag|
|---|---|
|Australia| [AUBankAccountNumber]  |

### Type: AU Business Number

|Issuer|Tag|
|---|---|
|Australia| [AUBusinessNumber]  |

### Type: AU Company Number

|Issuer|Tag|
|---|---|
|Australia| [AUCompanyNumber]  |

### Type: AU Drivers License Number

|Issuer|Tag|
|---|---|
|Australia| [AUDriversLicenseNumber]  |

### Type: AU Medical Account Number

|Issuer|Tag|
|---|---|
|Australia| [AUMedicalAccountNumber]  |

### Type: AU Passport Number

|Issuer|Tag|
|---|---|
|Australia| [AUPassportNumber]  |

### Type: AU Tax File Number

|Issuer|Tag|
|---|---|
|Australia| [AUTaxFileNumber]  |

### Type: Azure Document DB Auth Key

|Issuer|Tag|
|---|---|
|Microsoft| [AzureDocumentDBAuthKey]  |

### Type: Azure IAAS Database Connection And SQL String

|Issuer|Tag|
|---|---|
|Microsoft| [AzureIAASDatabaseConnectionAndSQLString]  |

### Type: Azure IoT Connection String

|Issuer|Tag|
|---|---|
|Microsoft| [AzureIoTConnectionString]  |

### Type: Azure Publish Setting Password

|Issuer|Tag|
|---|---|
|Microsoft| [AzurePublishSettingPassword]  |

### Type: Azure Redis Cache String

|Issuer|Tag|
|---|---|
|Microsoft| [AzureRedisCacheString]  |

### Type: Azure SAS

|Issuer|Tag|
|---|---|
|Microsoft| [AzureSAS]  |

### Type: Azure Service Bus String

|Issuer|Tag|
|---|---|
|Microsoft| [AzureServiceBusString]  |

### Type: Azure Storage Account Generic

|Issuer|Tag|
|---|---|
|Microsoft| [AzureStorageAccountGeneric]  |

### Type: Azure Storage Account Key

|Issuer|Tag|
|---|---|
|Microsoft| [AzureStorageAccountKey]  |

### Type: Bank Account Number

|Issuer|Tag|
|---|---|
|Not applicable| [BankAccountNumber]  |

### Type: BE National Number

|Issuer|Tag|
|---|---|
|Belgium| [BENationalNumber]  |

### Type: BE National Number V2

|Issuer|Tag|
|---|---|
|Belgium| [BENationalNumberV2]  |

### Type: BE Value Added Tax Number

|Issuer|Tag|
|---|---|
|Belgium| [BEValueAddedTaxNumber]  |

### Type: BG Uniform Civil Number

|Issuer|Tag|
|---|---|
|Bulgaria| [BGUniformCivilNumber]  |

### Type: BR CPF Number

|Issuer|Tag|
|---|---|
|Brazil| [BRCPFNumber]  |

### Type: BR Legal Entity Number

|Issuer|Tag|
|---|---|
|Brazil| [BRLegalEntityNumber]  |

### Type: BR National IDRG

|Issuer|Tag|
|---|---|
|Brazil| [BRNationalIDRG]  |

### Type: CA Bank Account Number

|Issuer|Tag|
|---|---|
|Canada| [CABankAccountNumber]  |

### Type: CA Drivers License Number

|Issuer|Tag|
|---|---|
|Canada| [CADriversLicenseNumber]  |

### Type: CA Health Service Number

|Issuer|Tag|
|---|---|
|Canada| [CAHealthServiceNumber]  |

### Type: CA Passport Number

|Issuer|Tag|
|---|---|
|Canada| [CAPassportNumber]  |

### Type: CA Personal Health Identification

|Issuer|Tag|
|---|---|
|Canada| [CAPersonalHealthIdentification]  |

### Type: CA Social Insurance Number

|Issuer|Tag|
|---|---|
|Canada| [CASocialInsuranceNumber]  |

### Type: CH Social Security Number

|Issuer|Tag|
|---|---|
|Switzerland| [CHSocialSecurityNumber]  |

### Type: CL Identity Card Number

|Issuer|Tag|
|---|---|
|Chile| [CLIdentityCardNumber]  |

### Type: CN Resident Identity Card Number

|Issuer|Tag|
|---|---|
|China| [CNResidentIdentityCardNumber]  |

### Type: Credit Card Number

|Issuer|Tag|
|---|---|
|Not applicable| [CreditCardNumber]  |

### Type: CY Identity Card

|Issuer|Tag|
|---|---|
|Cyprus| [CYIdentityCard]  |

### Type: CY Tax Identification Number

|Issuer|Tag|
|---|---|
|Cyprus| [CYTaxIdentificationNumber]  |

### Type: CZ Personal Identity Number

|Issuer|Tag|
|---|---|
|Czech Republic| [CZPersonalIdentityNumber]  |

### Type: CZ Personal Identity V2

|Issuer|Tag|
|---|---|
|Czech Republic| [CZPersonalIdentityV2]  |

### Type: Date

|Issuer|Tag|
|---|---|
|Not applicable| [Date]  |

### Type: Date Of Birth

|Issuer|Tag|
|---|---|
|Not applicable| [DateOfBirth]  |

### Type: DE Drivers License Number

|Issuer|Tag|
|---|---|
|Germany| [DEDriversLicenseNumber]  |

### Type: DE Identity Card Number

|Issuer|Tag|
|---|---|
|Germany| [DEIdentityCardNumber]  |

### Type: DE Passport Number

|Issuer|Tag|
|---|---|
|Germany| [DEPassportNumber]  |

### Type: DE Tax Identification Number

|Issuer|Tag|
|---|---|
|Germany| [DETaxIdentificationNumber]  |

### Type: DE Value Added Number

|Issuer|Tag|
|---|---|
|Germany| [DEValueAddedNumber]  |

### Type: DK Personal Identification Number

|Issuer|Tag|
|---|---|
|Denmark| [DKPersonalIdentificationNumber]  |

### Type: DK Personal Identification V2

|Issuer|Tag|
|---|---|
|Denmark| [DKPersonalIdentificationV2]  |

### Type: Drivers License Number

|Issuer|Tag|
|---|---|
|Not applicable| [DriversLicenseNumber]  |

### Type: Drug Enforcement Agency Number

|Issuer|Tag|
|---|---|
|United States| [DrugEnforcementAgencyNumber]  |

### Type: EE Personal Identification Code

|Issuer|Tag|
|---|---|
|Estonia| [EEPersonalIdentificationCode]  |

### Type: Email

|Issuer|Tag|
|---|---|
|Not applicable| [Email]  |

### Type: ES DNI

|Issuer|Tag|
|---|---|
|Spain| [ESDNI]  |

### Type: ES Social Security Number

|Issuer|Tag|
|---|---|
|Spain| [ESSocialSecurityNumber]  |

### Type: ES Tax Identification Number

|Issuer|Tag|
|---|---|
|Spain| [ESTaxIdentificationNumber]  |

### Type: EU Debit Card Number

|Issuer|Tag|
|---|---|
|European Union| [EUDebitCardNumber]  |

### Type: EU Drivers License Number

|Issuer|Tag|
|---|---|
|European Union| [EUDriversLicenseNumber]  |

### Type: EU GPS Coordinates

|Issuer|Tag|
|---|---|
|European Union| [EUGPSCoordinates]  |

### Type: EU National Identification Number

|Issuer|Tag|
|---|---|
|European Union| [EUNationalIdentificationNumber]  |

### Type: EU Passport Number

|Issuer|Tag|
|---|---|
|European Union| [EUPassportNumber]  |

### Type: EU Social Security Number

|Issuer|Tag|
|---|---|
|European Union| [EUSocialSecurityNumber]  |

### Type: EU Tax Identification Number

|Issuer|Tag|
|---|---|
|European Union| [EUTaxIdentificationNumber]  |

### Type: FI European Health Number

|Issuer|Tag|
|---|---|
|Finland| [FIEuropeanHealthNumber]  |

### Type: FI National ID

|Issuer|Tag|
|---|---|
|Finland| [FINationalID]  |

### Type: FI National ID V2

|Issuer|Tag|
|---|---|
|Finland| [FINationalIDV2]  |

### Type: FI Passport Number

|Issuer|Tag|
|---|---|
|Finland| [FIPassportNumber]  |

### Type: FR Drivers License Number

|Issuer|Tag|
|---|---|
|France| [FRDriversLicenseNumber]  |

### Type: FR Health Insurance Number

|Issuer|Tag|
|---|---|
|France| [FRHealthInsuranceNumber]  |

### Type: FR National ID

|Issuer|Tag|
|---|---|
|France| [FRNationalID]  |

### Type: FR Passport Number

|Issuer|Tag|
|---|---|
|France| [FRPassportNumber]  |

### Type: FR Social Security Number

|Issuer|Tag|
|---|---|
|France| [FRSocialSecurityNumber]  |

### Type: FR Tax Identification Number

|Issuer|Tag|
|---|---|
|France| [FRTaxIdentificationNumber]  |

### Type: FR Value Added Tax Number

|Issuer|Tag|
|---|---|
|France| [FRValueAddedTaxNumber]  |

### Type: GR National ID Card

|Issuer|Tag|
|---|---|
|Greece| [GRNationalIDCard]  |

### Type: GR National ID V2

|Issuer|Tag|
|---|---|
|Greece| [GRNationalIDV2]  |

### Type: GR Tax Identification Number

|Issuer|Tag|
|---|---|
|Greece| [GRTaxIdentificationNumber]  |

### Type: HK Identity Card Number

|Issuer|Tag|
|---|---|
|Hong Kong| [HKIdentityCardNumber]  |

### Type: HR Identity Card Number

|Issuer|Tag|
|---|---|
|Croatia| [HRIdentityCardNumber]  |

### Type: HR National ID Number

|Issuer|Tag|
|---|---|
|Croatia| [HRNationalIDNumber]  |

### Type: HR Personal Identification Number

|Issuer|Tag|
|---|---|
|Croatia| [HRPersonalIdentificationNumber]  |

### Type: HR Personal Identification OIB Number V2

|Issuer|Tag|
|---|---|
|Croatia| [HRPersonalIdentificationOIBNumberV2]  |

### Type: HU Personal Identification Number

|Issuer|Tag|
|---|---|
|Hungary| [HUPersonalIdentificationNumber]  |

### Type: HU Tax Identification Number

|Issuer|Tag|
|---|---|
|Hungary| [HUTaxIdentificationNumber]  |

### Type: HU Value Added Number

|Issuer|Tag|
|---|---|
|Hungary| [HUValueAddedNumber]  |

### Type: ID Identity Card Number

|Issuer|Tag|
|---|---|
|Indonesia| [IDIdentityCardNumber]  |

### Type: IE Personal Public Service Number

|Issuer|Tag|
|---|---|
|Ireland| [IEPersonalPublicServiceNumber]  |

### Type: IE Personal Public Service Number V2

|Issuer|Tag|
|---|---|
|Ireland| [IEPersonalPublicServiceNumberV2]  |

### Type: IL Bank Account Number

|Issuer|Tag|
|---|---|
|Israel| [ILBankAccountNumber]  |

### Type: IL National ID

|Issuer|Tag|
|---|---|
|Israel| [ILNationalID]  |

### Type: IN Permanent Account

|Issuer|Tag|
|---|---|
|India| [INPermanentAccount]  |

### Type: IN Unique Identification Number

|Issuer|Tag|
|---|---|
|India| [INUniqueIdentificationNumber]  |

### Type: International Banking Account Number

|Issuer|Tag|
|---|---|
|Not applicable| [InternationalBankingAccountNumber]  |

### Type: IP Address

|Issuer|Tag|
|---|---|
|Not applicable| [IPAddress]  |

### Type: IT Drivers License Number

|Issuer|Tag|
|---|---|
|Italy| [ITDriversLicenseNumber]  |

### Type: IT Fiscal Code

|Issuer|Tag|
|---|---|
|Italy| [ITFiscalCode]  |

### Type: IT Value Added Tax Number

|Issuer|Tag|
|---|---|
|Italy| [ITValueAddedTaxNumber]  |

### Type: JP Bank Account Number

|Issuer|Tag|
|---|---|
|Japan| [JPBankAccountNumber]  |

### Type: JP Drivers License Number

|Issuer|Tag|
|---|---|
|Japan| [JPDriversLicenseNumber]  |

### Type: JP My Number Corporate

|Issuer|Tag|
|---|---|
|Japan| [JPMyNumberCorporate]  |

### Type: JP My Number Personal

|Issuer|Tag|
|---|---|
|Japan| [JPMyNumberPersonal]  |

### Type: JP Passport Number

|Issuer|Tag|
|---|---|
|Japan| [JPPassportNumber]  |

### Type: JP Residence Card Number

|Issuer|Tag|
|---|---|
|Japan| [JPResidenceCardNumber]  |

### Type: JP Resident Registration Number

|Issuer|Tag|
|---|---|
|Japan| [JPResidentRegistrationNumber]  |

### Type: JP Social Insurance Number

|Issuer|Tag|
|---|---|
|Japan| [JPSocialInsuranceNumber]  |

### Type: KR Resident Registration Number

|Issuer|Tag|
|---|---|
|South Korea| [KRResidentRegistrationNumber]  |

### Type: License Plate

|Issuer|Tag|
|---|---|
|Not applicable| [LicensePlate]  |

### Type: LT Personal Code

|Issuer|Tag|
|---|---|
|Lithuania| [LTPersonalCode]  |

### Type: LU National Identification Number Natural

|Issuer|Tag|
|---|---|
|Luxembourg| [LUNationalIdentificationNumberNatural]  |

### Type: LU National Identification Number Non Natural

|Issuer|Tag|
|---|---|
|Luxembourg| [LUNationalIdentificationNumberNonNatural]  |

### Type: LV Personal Code

|Issuer|Tag|
|---|---|
|Latvia| [LVPersonalCode]  |

### Type: MT Identity Card Number

|Issuer|Tag|
|---|---|
|Malta| [MTIdentityCardNumber]  |

### Type: MT Tax ID Number

|Issuer|Tag|
|---|---|
|Malta| [MTTaxIDNumber]  |

### Type: MY Identity Card Number

|Issuer|Tag|
|---|---|
|Malaysia| [MYIdentityCardNumber]  |

### Type: Neighborhood

|Issuer|Tag|
|---|---|
|Not applicable| [Neighborhood]  |

### Type: NL Citizens Service Number

|Issuer|Tag|
|---|---|
|Netherlands| [NLCitizensServiceNumber]  |

### Type: NL Citizens Service Number V2

|Issuer|Tag|
|---|---|
|Netherlands| [NLCitizensServiceNumberV2]  |

### Type: NL Tax Identification Number

|Issuer|Tag|
|---|---|
|Netherlands| [NLTaxIdentificationNumber]  |

### Type: NL Value Added Tax Number

|Issuer|Tag|
|---|---|
|Netherlands| [NLValueAddedTaxNumber]  |

### Type: NO Identity Number

|Issuer|Tag|
|---|---|
|Norway| [NOIdentityNumber]  |

### Type: NZ Bank Account Number

|Issuer|Tag|
|---|---|
|New Zealand| [NZBankAccountNumber]  |

### Type: NZ Drivers License Number

|Issuer|Tag|
|---|---|
|New Zealand| [NZDriversLicenseNumber]  |

### Type: NZ Inland Revenue Number

|Issuer|Tag|
|---|---|
|New Zealand| [NZInlandRevenueNumber]  |

### Type: NZ Ministry Of Health Number

|Issuer|Tag|
|---|---|
|New Zealand| [NZMinistryOfHealthNumber]  |

### Type: NZ Social Welfare Number

|Issuer|Tag|
|---|---|
|New Zealand| [NZSocialWelfareNumber]  |

### Type: Organization

|Issuer|Tag|
|---|---|
|Not applicable| [Organization]  |

### Type: Passport Number

|Issuer|Tag|
|---|---|
|Not applicable| [PassportNumber]  |

### Type: Person

|Issuer|Tag|
|---|---|
|Not applicable| [Person]  |

### Type: PH Unified Multi Purpose ID Number

|Issuer|Tag|
|---|---|
|Philippines| [PHUnifiedMultiPurposeIDNumber]  |

### Type: Phone Number

|Issuer|Tag|
|---|---|
|Not applicable| [PhoneNumber]  |

### Type: PIN

|Issuer|Tag|
|---|---|
|Not applicable| [PIN]  |

### Type: PL Identity Card

|Issuer|Tag|
|---|---|
|Poland| [PLIdentityCard]  |

### Type: PL National ID

|Issuer|Tag|
|---|---|
|Poland| [PLNationalID]  |

### Type: PL National ID V2

|Issuer|Tag|
|---|---|
|Poland| [PLNationalIDV2]  |

### Type: PL Passport Number

|Issuer|Tag|
|---|---|
|Poland| [PLPassportNumber]  |

### Type: PL REGON Number

|Issuer|Tag|
|---|---|
|Poland| [PLREGONNumber]  |

### Type: PL Tax Identification Number

|Issuer|Tag|
|---|---|
|Poland| [PLTaxIdentificationNumber]  |

### Type: PT Citizen Card Number

|Issuer|Tag|
|---|---|
|Portugal| [PTCitizenCardNumber]  |

### Type: PT Citizen Card Number V2

|Issuer|Tag|
|---|---|
|Portugal| [PTCitizenCardNumberV2]  |

### Type: PT Tax Identification Number

|Issuer|Tag|
|---|---|
|Portugal| [PTTaxIdentificationNumber]  |

### Type: RO Personal Numerical Code

|Issuer|Tag|
|---|---|
|Romania| [ROPersonalNumericalCode]  |

### Type: RU Passport Number Domestic

|Issuer|Tag|
|---|---|
|Russia| [RUPassportNumberDomestic]  |

### Type: RU Passport Number International

|Issuer|Tag|
|---|---|
|Russia| [RUPassportNumberInternational]  |

### Type: SA National ID

|Issuer|Tag|
|---|---|
|Saudi Arabia| [SANationalID]  |

### Type: SE National ID

|Issuer|Tag|
|---|---|
|Sweden| [SENationalID]  |

### Type: SE National ID V2

|Issuer|Tag|
|---|---|
|Sweden| [SENationalIDV2]  |

### Type: SE Passport Number

|Issuer|Tag|
|---|---|
|Sweden| [SEPassportNumber, PassportNumber]  |

### Type: SE Tax Identification Number

|Issuer|Tag|
|---|---|
|Sweden| [SETaxIdentificationNumber]  |

### Type: SG National Registration Identity Card Number

|Issuer|Tag|
|---|---|
|Singapore| [SGNationalRegistrationIdentityCardNumber]  |

### Type: SI Tax Identification Number

|Issuer|Tag|
|---|---|
|Slovenia| [SITaxIdentificationNumber]  |

### Type: SI Unique Master Citizen Number

|Issuer|Tag|
|---|---|
|Slovenia| [SIUniqueMasterCitizenNumber]  |

### Type: SK Personal Number

|Issuer|Tag|
|---|---|
|Slovakia| [SKPersonalNumber]  |

### Type: Sort Code

|Issuer|Tag|
|---|---|
|Not applicable| [SortCode]  |

### Type: SQL Server Connection String

|Issuer|Tag|
|---|---|
|Microsoft| [SQLServerConnectionString]  |

### Type: SWIFT Code

|Issuer|Tag|
|---|---|
|Not applicable| [SWIFTCode]  |

### Type: TH Population Identification Code

|Issuer|Tag|
|---|---|
|Thailand| [THPopulationIdentificationCode]  |

### Type: TR National Identification Number

|Issuer|Tag|
|---|---|
|Turkey| [TRNationalIdentificationNumber]  |

### Type: TW National ID

|Issuer|Tag|
|---|---|
|Taiwan| [TWNationalID]  |

### Type: TW Passport Number

|Issuer|Tag|
|---|---|
|Taiwan| [TWPassportNumber]  |

### Type: TW Resident Certificate

|Issuer|Tag|
|---|---|
|Taiwan| [TWResidentCertificate]  |

### Type: UA Passport Number Domestic

|Issuer|Tag|
|---|---|
|Ukraine| [UAPassportNumberDomestic]  |

### Type: UA Passport Number International

|Issuer|Tag|
|---|---|
|Ukraine| [UAPassportNumberInternational]  |

### Type: UK Drivers License Number

|Issuer|Tag|
|---|---|
|United Kingdom| [UKDriversLicenseNumber]  |

### Type: UK Electoral Roll Number

|Issuer|Tag|
|---|---|
|United Kingdom| [UKElectoralRollNumber]  |

### Type: UK National Health Number

|Issuer|Tag|
|---|---|
|United Kingdom| [UKNationalHealthNumber]  |

### Type: UK National Insurance Number

|Issuer|Tag|
|---|---|
|United Kingdom| [UKNationalInsuranceNumber]  |

### Type: UK Unique Taxpayer Number

|Issuer|Tag|
|---|---|
|United Kingdom| [UKUniqueTaxpayerNumber]  |

### Type: URL

|Issuer|Tag|
|---|---|
|Not applicable| [URL]  |

### Type: US Bank Account Number

|Issuer|Tag|
|---|---|
|United States| [USBankAccountNumber]  |

### Type: US Drivers License Number

|Issuer|Tag|
|---|---|
|United States| [USDriversLicenseNumber]  |

### Type: US Individual Taxpayer Identification

|Issuer|Tag|
|---|---|
|United States| [USIndividualTaxpayerIdentification]  |

### Type: US Social Security Number

|Issuer|Tag|
|---|---|
|United States| [USSocialSecurityNumber]  |

### Type: US UK Passport Number

|Issuer|Tag|
|---|---|
|United States/United Kingdom| [USUKPassportNumber]  |

### Type: VIN

|Issuer|Tag|
|---|---|
|Not applicable| [VIN]  |

### Type: ZA Identification Number

|Issuer|Tag|
|---|---|
|South Africa| [ZAIdentificationNumber]  |
