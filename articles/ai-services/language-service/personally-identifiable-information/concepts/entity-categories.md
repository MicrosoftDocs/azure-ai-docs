---
title: Entity categories recognized by Personally Identifiable Information (detection) in Azure AI Language
titleSuffix: Azure AI services
description: Learn about the entities the PII feature can recognize from unstructured text.
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: conceptual
ms.date: 06/04/2025
ms.author: lajanuar
ms.custom: language-service-pii
---

# Supported Personally Identifiable Information (PII) entity categories

Use this article to find the entity categories that the [PII detection feature](../how-to-call.md) returns. This feature runs a predictive model to identify, categorize, and redact sensitive information from an input document.

The PII feature includes the ability to detect personal (`PII`) and health (`PHI`) information.

## Entity categories

> [!NOTE]
> To detect protected health information (PHI), use the `domain=phi` parameter and model version `2020-04-01` or later.
> The `Type` and Sub is a new designation we're introducing in preview

The following entity categories are returned when you're sending API requests PII feature.

# [Preview API](#tab/preview-api)

## Type: Person

This category contains the following entity:

:::row:::
    :::column span="":::
        **Entity**

        Person

    :::column-end:::
    :::column span="2":::
        **Details**

        Names of people. Returned as both PII and PHI.

        To get this entity category, add `Person` to the `piiCategories` parameter. `Person` is returned in the API response if detected.

    :::column-end:::

    :::column span="":::
      **Supported languages**

      `en`, `es`, `fr`, `de`, `it`, `pt-pt`, `pt-br`, `zh`, `ja`, `ko`, `nl`, `sv`, `tr`, `hi`, `af`, `ca`, `da`, `el`, `ga`, `gl`, `ku`, `nl`, `no`, `ss`, `ro`, `sq`, `ur`, `ar`, `bg`, `bs`, `cy`, `fa`, `hr`, `id`, `mg`, `mk`, `ms`, `ps`, `ru`, `sl`, `so`, `sr`, `sw`, `am`, `as`, `cs`, `et`, `eu`, `fi`, `he`, `hu`, `km`, `lo`, `lt`, `lv`, `mr`, `my`, `ne`, `or`, `pa`, `pl`, `sk`, `th`, `uk`, `az`, `bn`, `gu`, `hy`, `ka`, `kk`, `kn`, `ky`, `ml`, `mn`, `ta`, `te`, `ug`, `uz`, `vi`

   :::column-end:::
:::row-end:::

# [GA API](#tab/ga-api)

## Category: Person

This type contains the following entity:

:::row:::
    :::column span="":::
        **Entity**

        Person

    :::column-end:::
    :::column span="2":::
        **Details**

        Names of people. Returned as both PII and PHI.

        To get this entity type, add `Person` to the `piiCategories` parameter. `Person` is returned in the API response if detected.

    :::column-end:::

    :::column span="":::
      **Supported languages**

      `en`, `es`, `fr`, `de`, `it`, `pt-pt`, `pt-br`, `zh`, `ja`, `ko`, `nl`, `sv`, `tr`, `hi`, `af`, `ca`, `da`, `el`, `ga`, `gl`, `ku`, `nl`, `no`, `ss`, `ro`, `sq`, `ur`, `ar`, `bg`, `bs`, `cy`, `fa`, `hr`, `id`, `mg`, `mk`, `ms`, `ps`, `ru`, `sl`, `so`, `sr`, `sw`, `am`, `as`, `cs`, `et`, `eu`, `fi`, `he`, `hu`, `km`, `lo`, `lt`, `lv`, `mr`, `my`, `ne`, `or`, `pa`, `pl`, `sk`, `th`, `uk`, `az`, `bn`, `gu`, `hy`, `ka`, `kk`, `kn`, `ky`, `ml`, `mn`, `ta`, `te`, `ug`, `uz`, `vi`

   :::column-end:::
:::row-end:::
---

# [Preview API](#tab/preview-api)

## Type: PersonType

This category contains the following entity:


:::row:::
    :::column span="":::
        **Entity**

        PersonType

    :::column-end:::
    :::column span="2":::
        **Details**

        Job types or roles held by a person.

        To get this entity category, add `PersonType` to the `piiCategories` parameter. `PersonType` is returned in the API response if detected.

    :::column-end:::

    :::column span="":::
      **Supported languages**

      `en`, `es`, `fr`, `de`, `it`, `pt-pt`, `pt-br`, `zh`, `ja`, `ko`, `nl`, `sv`, `tr`, `hi`, `af`, `ca`, `da`, `el`, `ga`, `gl`, `ku`, `nl`, `no`, `ss`, `ro`, `sq`, `ur`, `ar`, `bg`, `bs`, `cy`, `fa`, `hr`, `id`, `mg`, `mk`, `ms`, `ps`, `ru`, `sl`, `so`, `sr`, `sw`, `am`, `as`, `cs`, `et`, `eu`, `fi`, `he`, `hu`, `km`, `lo`, `lt`, `lv`, `mr`, `my`, `ne`, `or`, `pa`, `pl`, `sk`, `th`, `uk`, `az`, `bn`, `gu`, `hy`, `ka`, `kk`, `kn`, `ky`, `ml`, `mn`, `ta`, `te`, `ug`, `uz`, `vi`

   :::column-end:::
:::row-end:::

# [GA API](#tab/ga-api)

## Category: PersonType

This type contains the following entity:


:::row:::
    :::column span="":::
        **Entity**

        PersonType

    :::column-end:::
    :::column span="2":::
        **Details**

        Job types or roles held by a person.

        To get this entity type, add `PersonType` to the `piiCategories` parameter. `PersonType` is returned in the API response if detected.

    :::column-end:::

    :::column span="":::
      **Supported languages**

      `en`, `es`, `fr`, `de`, `it`, `pt-pt`, `pt-br`, `zh`, `ja`, `ko`, `nl`, `sv`, `tr`, `hi`, `af`, `ca`, `da`, `el`, `ga`, `gl`, `ku`, `nl`, `no`, `ss`, `ro`, `sq`, `ur`, `ar`, `bg`, `bs`, `cy`, `fa`, `hr`, `id`, `mg`, `mk`, `ms`, `ps`, `ru`, `sl`, `so`, `sr`, `sw`, `am`, `as`, `cs`, `et`, `eu`, `fi`, `he`, `hu`, `km`, `lo`, `lt`, `lv`, `mr`, `my`, `ne`, `or`, `pa`, `pl`, `sk`, `th`, `uk`, `az`, `bn`, `gu`, `hy`, `ka`, `kk`, `kn`, `ky`, `ml`, `mn`, `ta`, `te`, `ug`, `uz`, `vi`

   :::column-end:::
:::row-end:::
---

# [Preview API](#tab/preview-api)

## Type: PhoneNumber

This category contains the following entity:

:::row:::
    :::column span="":::
        **Entity**

        PhoneNumber

    :::column-end:::
    :::column span="2":::
        **Details**

        Phone numbers (US and EU phone numbers only). Returned as both PII and PHI.

        To get this entity category, add `PhoneNumber` to the `piiCategories` parameter. `PhoneNumber` is returned in the API response if detected.

    :::column-end:::

    :::column span="":::
      **Supported languages**

      `en`, `es`, `fr`, `de`, `it`, `zh-hans`, `ja`, `ko`, `pt-pt` `pt-br`

   :::column-end:::

:::row-end:::

# [GA API](#tab/ga-api)

## Category: PhoneNumber

This type contains the following entity:

:::row:::
    :::column span="":::
        **Entity**

        PhoneNumber

    :::column-end:::
    :::column span="2":::
        **Details**

        Phone numbers (US and EU phone numbers only). Returned as both PII and PHI.

        To get this entity type, add `PhoneNumber` to the `piiCategories` parameter. `PhoneNumber` is returned in the API response if detected.

    :::column-end:::

    :::column span="":::
      **Supported languages**

      `en`, `es`, `fr`, `de`, `it`, `zh-hans`, `ja`, `ko`, `pt-pt` `pt-br`

   :::column-end:::

:::row-end:::
---

# [Preview API](#tab/preview-api)

## Type: Organization

This category contains the following entity:

:::row:::
    :::column span="":::
        **Entity**

        Organization

    :::column-end:::
    :::column span="2":::
        **Details**

        Companies, political groups, musical bands, sport clubs, government bodies, and public organizations. Nationalities and religions are not included in this entity type. Returned as both PII and PHI.

        To get this entity category, add `Organization` to the `piiCategories` parameter. `Organization` is returned in the API response if detected.

    :::column-end:::

    :::column span="":::
      **Supported languages**

      `en`, `es`, `fr`, `de`, `it`, `pt-pt`, `pt-br`, `zh`, `ja`, `ko`, `nl`, `sv`, `tr`, `hi`, `af`, `ca`, `da`, `el`, `ga`, `gl`, `ku`, `nl`, `no`, `ss`, `ro`, `sq`, `ur`, `ar`, `bg`, `bs`, `cy`, `fa`, `hr`, `id`, `mg`, `mk`, `ms`, `ps`, `ru`, `sl`, `so`, `sr`, `sw`, `am`, `as`, `cs`, `et`, `eu`, `fi`, `he`, `hu`, `km`, `lo`, `lt`, `lv`, `mr`, `my`, `ne`, `or`, `pa`, `pl`, `sk`, `th`, `uk`, `az`, `bn`, `gu`, `hy`, `ka`, `kk`, `kn`, `ky`, `ml`, `mn`, `ta`, `te`, `ug`, `uz`, `vi`

   :::column-end:::

:::row-end:::

#### Subcategories

The entity in this category can have the following subcategories.

:::row:::
    :::column span="":::
        **Entity subcategory**

        Medical

    :::column-end:::
    :::column span="2":::
        **Details**

        Medical companies and groups.

        To get this entity category, add `OrganizationMedical` to the `piiCategories` parameter. `OrganizationMedical` is returned in the API response if detected.

    :::column-end:::

    :::column span="":::
      **Supported languages**

      `en`

   :::column-end:::

:::row-end:::
:::row:::
    :::column span="":::

        Stock exchange

    :::column-end:::
    :::column span="2":::

        Stock exchange groups.

        To get this entity category, add `OrganizationStockExchange` to the `piiCategories` parameter. `OrganizationStockExchange` is returned in the API response if detected.

    :::column-end:::

    :::column span="":::

      `en`

   :::column-end:::

:::row-end:::
:::row:::
    :::column span="":::

        Sports

    :::column-end:::
    :::column span="2":::

        Sports-related organizations.

        To get this entity category, add `OrganizationSports` to the `piiCategories` parameter. `OrganizationSports` is returned in the API response if detected.

    :::column-end:::

    :::column span="":::

      `en`

   :::column-end:::

:::row-end:::

# [GA API](#tab/ga-api)

## Category: Organization

This type contains the following entity:

:::row:::
    :::column span="":::
        **Entity**

        Organization

    :::column-end:::
    :::column span="2":::
        **Details**

        Companies, political groups, musical bands, sport clubs, government bodies, and public organizations. Nationalities and religions are not included in this entity type. Returned as both PII and PHI.

        To get this entity type, add `Organization` to the `piiCategories` parameter. `Organization` is returned in the API response if detected.

    :::column-end:::

    :::column span="":::
      **Supported languages**

      `en`, `es`, `fr`, `de`, `it`, `pt-pt`, `pt-br`, `zh`, `ja`, `ko`, `nl`, `sv`, `tr`, `hi`, `af`, `ca`, `da`, `el`, `ga`, `gl`, `ku`, `nl`, `no`, `ss`, `ro`, `sq`, `ur`, `ar`, `bg`, `bs`, `cy`, `fa`, `hr`, `id`, `mg`, `mk`, `ms`, `ps`, `ru`, `sl`, `so`, `sr`, `sw`, `am`, `as`, `cs`, `et`, `eu`, `fi`, `he`, `hu`, `km`, `lo`, `lt`, `lv`, `mr`, `my`, `ne`, `or`, `pa`, `pl`, `sk`, `th`, `uk`, `az`, `bn`, `gu`, `hy`, `ka`, `kk`, `kn`, `ky`, `ml`, `mn`, `ta`, `te`, `ug`, `uz`, `vi`

   :::column-end:::

:::row-end:::

#### Subtypes

The entity in this type can have the following subtypes.

:::row:::
    :::column span="":::
        **Entity subtype**

        Medical

    :::column-end:::
    :::column span="2":::
        **Details**

        Medical companies and groups.

        To get this entity type, add `OrganizationMedical` to the `piiCategories` parameter. `OrganizationMedical` is returned in the API response if detected.

    :::column-end:::

    :::column span="":::
      **Supported languages**

      `en`

   :::column-end:::

:::row-end:::
:::row:::
    :::column span="":::

        Stock exchange

    :::column-end:::
    :::column span="2":::

        Stock exchange groups.

        To get this entity type, add `OrganizationStockExchange` to the `piiCategories` parameter. `OrganizationStockExchange` is returned in the API response if detected.

    :::column-end:::

    :::column span="":::

      `en`

   :::column-end:::

:::row-end:::
:::row:::
    :::column span="":::

        Sports

    :::column-end:::
    :::column span="2":::

        Sports-related organizations.

        To get this entity type, add `OrganizationSports` to the `piiCategories` parameter. `OrganizationSports` is returned in the API response if detected.

    :::column-end:::

    :::column span="":::

      `en`

   :::column-end:::

:::row-end:::

---


# [Preview API](#tab/preview-api)

## Type: Address


This category contains the following entity:

:::row:::
    :::column span="":::
        **Entity**

        Address

    :::column-end:::
    :::column span="2":::
        **Details**

        Full mailing address. Returned as both PII and PHI.

        To get this entity category, add `Address` to the `piiCategories` parameter. `Address` is returned in the API response if detected.

    :::column-end:::

    :::column span="":::
      **Supported languages**

      `en`, `es`, `fr`, `de`, `it`, `pt-pt`, `pt-br`, `zh`, `ja`, `ko`, `nl`, `sv`, `tr`, `hi`, `af`, `ca`, `da`, `el`, `ga`, `gl`, `ku`, `nl`, `no`, `ss`, `ro`, `sq`, `ur`, `ar`, `bg`, `bs`, `cy`, `fa`, `hr`, `id`, `mg`, `mk`, `ms`, `ps`, `ru`, `sl`, `so`, `sr`, `sw`, `am`, `as`, `cs`, `et`, `eu`, `fi`, `he`, `hu`, `km`, `lo`, `lt`, `lv`, `mr`, `my`, `ne`, `or`, `pa`, `pl`, `sk`, `th`, `uk`, `az`, `bn`, `gu`, `hy`, `ka`, `kk`, `kn`, `ky`, `ml`, `mn`, `ta`, `te`, `ug`, `uz`, `vi`

    :::column-end:::

:::row-end:::

# [GA API](#tab/ga-api)

## Category: Address

This type contains the following entity:

:::row:::
    :::column span="":::
        **Entity**

        Address

    :::column-end:::
    :::column span="2":::
        **Details**

        Full mailing address. Returned as both PII and PHI.

        To get this entity type, add `Address` to the `piiCategories` parameter. `Address` is returned in the API response if detected.

    :::column-end:::

    :::column span="":::
      **Supported languages**

      `en`, `es`, `fr`, `de`, `it`, `pt-pt`, `pt-br`, `zh`, `ja`, `ko`, `nl`, `sv`, `tr`, `hi`, `af`, `ca`, `da`, `el`, `ga`, `gl`, `ku`, `nl`, `no`, `ss`, `ro`, `sq`, `ur`, `ar`, `bg`, `bs`, `cy`, `fa`, `hr`, `id`, `mg`, `mk`, `ms`, `ps`, `ru`, `sl`, `so`, `sr`, `sw`, `am`, `as`, `cs`, `et`, `eu`, `fi`, `he`, `hu`, `km`, `lo`, `lt`, `lv`, `mr`, `my`, `ne`, `or`, `pa`, `pl`, `sk`, `th`, `uk`, `az`, `bn`, `gu`, `hy`, `ka`, `kk`, `kn`, `ky`, `ml`, `mn`, `ta`, `te`, `ug`, `uz`, `vi`

    :::column-end:::

:::row-end:::

---

# [Preview API](#tab/preview-api)

## Type: Email

This category contains the following entity:

:::row:::
    :::column span="":::
        **Entity**

        Email

    :::column-end:::
    :::column span="2":::
        **Details**

        Email addresses. Returned as both PII and PHI.

        To get this entity category, add `Email` to the `piiCategories` parameter. `Email` is returned in the API response if detected.

    :::column-end:::
    :::column span="":::
      **Supported languages**

      `en`, `es`, `fr`, `de`, `it`, `zh`, `ja`, `ko`, `pt-pt`, `pt-br`, `nl`, `sv`, `tr`, `hi`

    :::column-end:::
:::row-end:::

# [GA API](#tab/ga-api)

## Category: Email

This type contains the following entity:

:::row:::
    :::column span="":::
        **Entity**

        Email

    :::column-end:::
    :::column span="2":::
        **Details**

        Email addresses. Returned as both PII and PHI.

        To get this entity type, add `Email` to the `piiCategories` parameter. `Email` is returned in the API response if detected.

    :::column-end:::
    :::column span="":::
      **Supported languages**

      `en`, `es`, `fr`, `de`, `it`, `zh`, `ja`, `ko`, `pt-pt`, `pt-br`, `nl`, `sv`, `tr`, `hi`

    :::column-end:::
:::row-end:::

---


---

# [Preview API](#tab/preview-api)

## Type: URL

This category contains the following entity:

:::row:::
    :::column span="":::
        **Entity**

        URL

    :::column-end:::
    :::column span="2":::
        **Details**

        URLs to websites. Returned as both PII and PHI.

        To get this entity category, add `URL` to the `piiCategories` parameter. `URL` is returned in the API response if detected.

    :::column-end:::

    :::column span="":::
      **Supported languages**

      `en`, `es`, `fr`, `de`, `it`, `zh`, `ja`, `ko`, `pt-pt`, `pt-br`, `nl`, `sv`, `tr`, `hi`

    :::column-end:::

:::row-end:::

# [GA API](#tab/ga-api)

## Category: URL

This type contains the following entity:

:::row:::
    :::column span="":::
        **Entity**

        URL

    :::column-end:::
    :::column span="2":::
        **Details**

        URLs to websites. Returned as both PII and PHI.

        To get this entity type, add `URL` to the `piiCategories` parameter. `URL` is returned in the API response if detected.

    :::column-end:::

    :::column span="":::
      **Supported languages**

      `en`, `es`, `fr`, `de`, `it`, `zh`, `ja`, `ko`, `pt-pt`, `pt-br`, `nl`, `sv`, `tr`, `hi`

    :::column-end:::

:::row-end:::
---

# [Preview API](#tab/preview-api)

## Type: IP Address

This category contains the following entity:

:::row:::
    :::column span="":::
        **Entity**

        IPAddress

    :::column-end:::
    :::column span="2":::
        **Details**

        Network IP addresses. Returned as both PII and PHI.

        To get this entity category, add `IPAddress` to the `piiCategories` parameter. `IPAddress` is returned in the API response if detected.

    :::column-end:::

    :::column span="":::
      **Supported languages**

      `en`, `es`, `fr`, `de`, `it`, `zh`, `ja`, `ko`, `pt-pt`, `pt-br`, `nl`, `sv`, `tr`, `hi`

    :::column-end:::
:::row-end:::

# [GA API](#tab/ga-api)

## Category: IP Address

This type contains the following entity:

:::row:::
    :::column span="":::
        **Entity**

        IPAddress

    :::column-end:::
    :::column span="2":::
        **Details**

        Network IP addresses. Returned as both PII and PHI.

        To get this entity type, add `IPAddress` to the `piiCategories` parameter. `IPAddress` is returned in the API response if detected.

    :::column-end:::

    :::column span="":::
      **Supported languages**

      `en`, `es`, `fr`, `de`, `it`, `zh`, `ja`, `ko`, `pt-pt`, `pt-br`, `nl`, `sv`, `tr`, `hi`

    :::column-end:::
:::row-end:::


---

# [Preview API](#tab/preview-api)

## Type: DateTime

This category contains the following entities:

:::row:::
    :::column span="":::
        **Entity**

        DateTime

    :::column-end:::
    :::column span="2":::
        **Details**

        Dates and times of day.

        To get this entity category, add `DateTime` to the `piiCategories` parameter. `DateTime` is returned in the API response if detected.

    :::column-end:::
:::column span="":::
      **Supported languages**

      `en`, `es`, `fr`, `de`, `it`, `pt-pt`, `pt-br`, `zh`, `ja`, `ko`, `nl`, `sv`, `tr`, `hi`, `af`, `ca`, `da`, `el`, `ga`, `gl`, `ku`, `nl`, `no`, `ss`, `ro`, `sq`, `ur`, `ar`, `bg`, `bs`, `cy`, `fa`, `hr`, `id`, `mg`, `mk`, `ms`, `ps`, `ru`, `sl`, `so`, `sr`, `sw`, `am`, `as`, `cs`, `et`, `eu`, `fi`, `he`, `hu`, `km`, `lo`, `lt`, `lv`, `mr`, `my`, `ne`, `or`, `pa`, `pl`, `sk`, `th`, `uk`, `az`, `bn`, `gu`, `hy`, `ka`, `kk`, `kn`, `ky`, `ml`, `mn`, `ta`, `te`, `ug`, `uz`, `vi`

   :::column-end:::
:::row-end:::

### Subcategories

The entity in this category can have the following subcategories.

:::row:::
    :::column span="":::
        **Entity subcategory**

        Date

    :::column-end:::
    :::column span="2":::
        **Details**

        Calendar dates. Returned as both PII and PHI.

        To get this entity category, add `Date` to the `piiCategories` parameter. `Date` is returned in the API response if detected.

    :::column-end:::
    :::column span="2":::
      **Supported languages**

      `en`, `es`, `fr`, `de`, `it`, `pt-pt`, `pt-br`, `zh`, `ja`, `ko`, `nl`, `sv`, `tr`, `hi`, `af`, `ca`, `da`, `el`, `ga`, `gl`, `ku`, `nl`, `no`, `ss`, `ro`, `sq`, `ur`, `ar`, `bg`, `bs`, `cy`, `fa`, `hr`, `id`, `mg`, `mk`, `ms`, `ps`, `ru`, `sl`, `so`, `sr`, `sw`, `am`, `as`, `cs`, `et`, `eu`, `fi`, `he`, `hu`, `km`, `lo`, `lt`, `lv`, `mr`, `my`, `ne`, `or`, `pa`, `pl`, `sk`, `th`, `uk`, `az`, `bn`, `gu`, `hy`, `ka`, `kk`, `kn`, `ky`, `ml`, `mn`, `ta`, `te`, `ug`, `uz`, `vi`

    :::column-end:::
:::row-end:::

:::row:::
    :::column span="":::

        DateAndTime


    :::column-end:::
    :::column span="2":::

        Dates and times of day.

        To get this entity category, add `DateAndTime` to the `piiCategories` parameter. `DateAndTime` is returned in the API response if detected.


    :::column-end:::
    :::column span="2":::
      **Supported languages**

      `en`, `es`, `fr`, `de`, `it`, `pt-pt`, `pt-br`, `zh`, `ja`, `ko`, `nl`, `sv`, `tr`, `hi`, `af`, `ca`, `da`, `el`, `ga`, `gl`, `ku`, `nl`, `no`, `ss`, `ro`, `sq`, `ur`, `ar`, `bg`, `bs`, `cy`, `fa`, `hr`, `id`, `mg`, `mk`, `ms`, `ps`, `ru`, `sl`, `so`, `sr`, `sw`, `am`, `as`, `cs`, `et`, `eu`, `fi`, `he`, `hu`, `km`, `lo`, `lt`, `lv`, `mr`, `my`, `ne`, `or`, `pa`, `pl`, `sk`, `th`, `uk`, `az`, `bn`, `gu`, `hy`, `ka`, `kk`, `kn`, `ky`, `ml`, `mn`, `ta`, `te`, `ug`, `uz`, `vi`
      :::column-end:::
:::row-end:::
#### Subtype: Age

The PII service supports the Age subcategory within the broader Quantity category (since Age is the personally identifiable piece of information).

:::row:::
    :::column span="":::
        **Entity subcategory**

        Age

    :::column-end:::
    :::column span="2":::
        **Details**

        Ages.

    :::column-end:::
    :::column span="2":::
      **Supported languages**

      `en`, `es`, `fr`, `de`, `it`, `pt-pt`, `pt-br`, `zh`, `ja`, `ko`, `nl`, `sv`, `tr`, `hi`, `af`, `ca`, `da`, `el`, `ga`, `gl`, `ku`, `nl`, `no`, `ss`, `ro`, `sq`, `ur`, `ar`, `bg`, `bs`, `cy`, `fa`, `hr`, `id`, `mg`, `mk`, `ms`, `ps`, `ru`, `sl`, `so`, `sr`, `sw`, `am`, `as`, `cs`, `et`, `eu`, `fi`, `he`, `hu`, `km`, `lo`, `lt`, `lv`, `mr`, `my`, `ne`, `or`, `pa`, `pl`, `sk`, `th`, `uk`, `az`, `bn`, `gu`, `hy`, `ka`, `kk`, `kn`, `ky`, `ml`, `mn`, `ta`, `te`, `ug`, `uz`, `vi`

   :::column-end:::
:::row-end:::

#### Subtype: DateOfBirth

:::row:::
    :::column span="":::
        **Entity subcategory**

        Date of birth.

    :::column-end:::
    :::column span="2":::
        **Details**

      Date

      To get this entity category, add `DateOfBirth` to the `piiCategories` parameter. `DateOfBirth` is returned in the API response if detected. 

    :::column-end:::
    :::column span="2":::
      **Supported languages**

      `en`

   :::column-end:::
:::row-end:::

# [GA API](#tab/ga-api)

## Category: DateTime

This type contains the following entities:

:::row:::
    :::column span="":::
        **Entity**

        DateTime

    :::column-end:::
    :::column span="2":::
        **Details**

        Dates and times of day.

        To get this entity type, add `DateTime` to the `piiCategories` parameter. `DateTime` is returned in the API response if detected.

    :::column-end:::
:::column span="":::
      **Supported languages**

      `en`, `es`, `fr`, `de`, `it`, `pt-pt`, `pt-br`, `zh`, `ja`, `ko`, `nl`, `sv`, `tr`, `hi`, `af`, `ca`, `da`, `el`, `ga`, `gl`, `ku`, `nl`, `no`, `ss`, `ro`, `sq`, `ur`, `ar`, `bg`, `bs`, `cy`, `fa`, `hr`, `id`, `mg`, `mk`, `ms`, `ps`, `ru`, `sl`, `so`, `sr`, `sw`, `am`, `as`, `cs`, `et`, `eu`, `fi`, `he`, `hu`, `km`, `lo`, `lt`, `lv`, `mr`, `my`, `ne`, `or`, `pa`, `pl`, `sk`, `th`, `uk`, `az`, `bn`, `gu`, `hy`, `ka`, `kk`, `kn`, `ky`, `ml`, `mn`, `ta`, `te`, `ug`, `uz`, `vi`

   :::column-end:::
:::row-end:::

### Subtypes

The entity in this type can have the following subtypes.

:::row:::
    :::column span="":::
        **Entity subtype**

        Date

    :::column-end:::
    :::column span="2":::
        **Details**

        Calender dates. Returned as both PII and PHI.

        To get this entity type, add `Date` to the `piiCategories` parameter. `Date` is returned in the API response if detected.

    :::column-end:::
    :::column span="2":::
      **Supported languages**

      `en`, `es`, `fr`, `de`, `it`, `pt-pt`, `pt-br`, `zh`, `ja`, `ko`, `nl`, `sv`, `tr`, `hi`, `af`, `ca`, `da`, `el`, `ga`, `gl`, `ku`, `nl`, `no`, `ss`, `ro`, `sq`, `ur`, `ar`, `bg`, `bs`, `cy`, `fa`, `hr`, `id`, `mg`, `mk`, `ms`, `ps`, `ru`, `sl`, `so`, `sr`, `sw`, `am`, `as`, `cs`, `et`, `eu`, `fi`, `he`, `hu`, `km`, `lo`, `lt`, `lv`, `mr`, `my`, `ne`, `or`, `pa`, `pl`, `sk`, `th`, `uk`, `az`, `bn`, `gu`, `hy`, `ka`, `kk`, `kn`, `ky`, `ml`, `mn`, `ta`, `te`, `ug`, `uz`, `vi`

    :::column-end:::
:::row-end:::

:::row:::
    :::column span="":::

        DateAndTime


    :::column-end:::
    :::column span="2":::

        Dates and times of day.

        To get this entity type, add `DateAndTime` to the `piiCategories` parameter. `DateAndTime` is returned in the API response if detected.


    :::column-end:::
    :::column span="2":::
      **Supported languages**

      `en`, `es`, `fr`, `de`, `it`, `pt-pt`, `pt-br`, `zh`, `ja`, `ko`, `nl`, `sv`, `tr`, `hi`, `af`, `ca`, `da`, `el`, `ga`, `gl`, `ku`, `nl`, `no`, `ss`, `ro`, `sq`, `ur`, `ar`, `bg`, `bs`, `cy`, `fa`, `hr`, `id`, `mg`, `mk`, `ms`, `ps`, `ru`, `sl`, `so`, `sr`, `sw`, `am`, `as`, `cs`, `et`, `eu`, `fi`, `he`, `hu`, `km`, `lo`, `lt`, `lv`, `mr`, `my`, `ne`, `or`, `pa`, `pl`, `sk`, `th`, `uk`, `az`, `bn`, `gu`, `hy`, `ka`, `kk`, `kn`, `ky`, `ml`, `mn`, `ta`, `te`, `ug`, `uz`, `vi`
      :::column-end:::
:::row-end:::
:::row:::
    :::column span="":::

        DateOfBirth

    :::column-end:::
    :::column span="2":::

        Calendar dates in diverse formats and years associated with date of birth of an individual. Examples include "born in 1994", "born in 990101", "birth date: February 14th, 1995", "date: 1992/06/30", "DATE: 05-12-1988", "04.10.1999"

    :::column-end:::
    :::column span="":::

      `en`, `fr`, `de`, `it`, `es`, `pt-pt`, `pt-br`, `nl`, `zh-Hans`, `ja`, `ko`, `zh-Hant`

    :::column-end:::
:::row-end:::

#### Subcategory: Age

The PII service supports the Age subtype within the broader Quantity type (since Age is the personally identifiable piece of information).

:::row:::
    :::column span="":::
        **Entity subtype**

        Age

    :::column-end:::
    :::column span="2":::
        **Details**

        Numeric age.

    :::column-end:::
    :::column span="2":::
      **Supported languages**

      `en`, `es`, `fr`, `de`, `it`, `pt-pt`, `pt-br`, `zh`, `ja`, `ko`, `nl`, `sv`, `tr`, `hi`, `af`, `ca`, `da`, `el`, `ga`, `gl`, `ku`, `nl`, `no`, `ss`, `ro`, `sq`, `ur`, `ar`, `bg`, `bs`, `cy`, `fa`, `hr`, `id`, `mg`, `mk`, `ms`, `ps`, `ru`, `sl`, `so`, `sr`, `sw`, `am`, `as`, `cs`, `et`, `eu`, `fi`, `he`, `hu`, `km`, `lo`, `lt`, `lv`, `mr`, `my`, `ne`, `or`, `pa`, `pl`, `sk`, `th`, `uk`, `az`, `bn`, `gu`, `hy`, `ka`, `kk`, `kn`, `ky`, `ml`, `mn`, `ta`, `te`, `ug`, `uz`, `vi`

   :::column-end:::
:::row-end:::

---

# [Preview API](#tab/preview-api)

## Identification

## Type: BankAccountNumber

:::row:::
    :::column span="":::
        **Entity**

    :::column-end:::
    :::column span="2":::
        **Details**

        To get this entity category, add `BankAccountNumber` to the `piiCategories` parameter. `BankAccountNumber` is returned in the API response if detected.

    :::column-end:::
    :::column span="":::
      **Supported languages**

     `en`, `es`, `fr`, `de`, `it`, `pt-pt`, `pt-br`, `zh`, `ja`, `ko`, `nl`, `sv`, `tr`, `hi`, `af`, `ca`, `da`, `el`, `ga`, `gl`, `ku`, `nl`, `no`, `ss`, `ro`, `sq`, `ur`, `ar`, `bg`, `bs`, `cy`, `fa`, `hr`, `id`, `mg`, `mk`, `ms`, `ps`, `ru`, `sl`, `so`, `sr`, `sw`, `am`, `as`, `cs`, `et`, `eu`, `fi`, `he`, `hu`, `km`, `lo`, `lt`, `lv`, `mr`, `my`, `ne`, `or`, `pa`, `pl`, `sk`, `th`, `uk`, `az`, `bn`, `gu`, `hy`, `ka`, `kk`, `kn`, `ky`, `ml`, `mn`, `ta`, `te`, `ug`, `uz`, `vi`

    :::column-end:::
:::row-end:::

## Type: DriversLicenseNumber

:::row:::
    :::column span="":::
        **Entity**

    :::column-end:::
    :::column span="2":::
        **Details**

        To get this entity category, add `DriversLicenseNumber` to the `piiCategories` parameter. `DriversLicenseNumber` is returned in the API response if detected.

    :::column-end:::
    :::column span="":::
      **Supported languages**

     `en`, `es`, `fr`, `de`, `it`, `pt-pt`, `pt-br`, `zh`, `ja`, `ko`, `nl`, `sv`, `tr`, `hi`, `da`, `nl`, `no`, `ro`, `ar`, `bg`, `hr`, `ms`, `ru`, `sl`, `cs`, `et`, `fi`, `he`, `hu`, `km`, `lo`, `lt`, `lv`, `sk`, `th`, `uk`

    :::column-end:::
:::row-end:::

## Type: PassportNumber

:::row:::
    :::column span="":::
        **Entity**

    :::column-end:::
    :::column span="2":::
        **Details**

        To get this entity category, add `PassportNumber` to the `piiCategories` parameter. `PassportNumber` is returned in the API response if detected.

    :::column-end:::
    :::column span="":::
      **Supported languages**

     `en`, `es`, `fr`, `de`, `it`, `pt-pt`, `pt-br`, `zh`, `ja`, `ko`, `nl`, `sv`, `tr`, `hi`, `da`, `nl`, `no`, `ro`, `ar`, `bg`, `hr`, `ms`, `ru`, `sl`, `cs`, `et`, `fi`, `he`, `hu`, `km`, `lo`, `lt`, `lv`, `sk`, `th`, `uk`

    :::column-end:::
:::row-end:::


# [GA API](#tab/ga-api)

[!INCLUDE [supported identification entities](../includes/identification-entities.md)]

---

# [Preview API](#tab/preview-api)

## Azure information

These entity categories include identifiable Azure information like authentication information and connection strings. Not returned as PHI.

:::row:::
    :::column span="":::
        **Entity**

        Azure DocumentDB Auth Key

    :::column-end:::
    :::column span="2":::
        **Details**

        Authorization key for an Azure Cosmos DB server.

        To get this entity category, add `AzureDocumentDBAuthKey` to the `piiCategories` parameter. `AzureDocumentDBAuthKey` is returned in the API response if detected.

    :::column-end:::
    :::column span="":::
      **Supported languages**

      `en`, `es`, `fr`, `de`, `it`, `pt-pt`, `pt-br`, `zh`, `ja`, `ko`, `nl`, `sv`, `tr`, `hi`, `da`, `nl`, `no`, `ro`, `ar`, `bg`, `hr`, `ms`, `ru`, `sl`, `cs`, `et`, `fi`, `he`, `hu`, `lv`, `sk`, `th`, `uk`

    :::column-end:::
:::row-end:::
:::row:::
    :::column span="":::

        Azure IAAS Database Connection String and Azure SQL Connection String.


    :::column-end:::
    :::column span="2":::

        Connection string for an Azure infrastructure as a service (IaaS) database, and SQL connection string.

        To get this entity category, add `AzureIAASDatabaseConnectionAndSQLString` to the `piiCategories` parameter. `AzureIAASDatabaseConnectionAndSQLString` is returned in the API response if detected.

    :::column-end:::
    :::column span="":::

      `en`, `es`, `fr`, `de`, `it`, `pt-pt`, `pt-br`, `zh`, `ja`, `ko`, `nl`, `sv`, `tr`, `hi`, `da`, `nl`, `no`, `ro`, `ar`, `bg`, `hr`, `ms`, `ru`, `sl`, `cs`, `et`, `fi`, `he`, `hu`, `lv`, `sk`, `th`, `uk`

    :::column-end:::
:::row-end:::
:::row:::
    :::column span="":::

        Azure IoT Connection String

    :::column-end:::
    :::column span="2":::

        Connection string for Azure IoT.

        To get this entity category, add `AzureIoTConnectionString` to the `piiCategories` parameter. `AzureIoTConnectionString` is returned in the API response if detected.

    :::column-end:::
    :::column span="":::

      `en`, `es`, `fr`, `de`, `it`, `pt-pt`, `pt-br`, `zh`, `ja`, `ko`, `nl`, `sv`, `tr`, `hi`, `da`, `nl`, `no`, `ro`, `ar`, `bg`, `hr`, `ms`, `ru`, `sl`, `cs`, `et`, `fi`, `he`, `hu`, `lv`, `sk`, `th`, `uk`

    :::column-end:::
:::row-end:::
:::row:::
    :::column span="":::

        Azure Publish Setting Password

    :::column-end:::
    :::column span="2":::

        Password for Azure publish settings.

        To get this entity category, add `AzurePublishSettingPassword` to the `piiCategories` parameter. `AzurePublishSettingPassword` is returned in the API response if detected.

    :::column-end:::
    :::column span="":::

      `en`, `es`, `fr`, `de`, `it`, `pt-pt`, `pt-br`, `zh`, `ja`, `ko`, `nl`, `sv`, `tr`, `hi`, `da`, `nl`, `no`, `ro`, `ar`, `bg`, `hr`, `ms`, `ru`, `sl`, `cs`, `et`, `fi`, `he`, `hu`, `lv`, `sk`, `th`, `uk`

    :::column-end:::
:::row-end:::
:::row:::
    :::column span="":::

        Azure Redis Cache Connection String

    :::column-end:::
    :::column span="2":::

        Connection string for a Redis cache.

        To get this entity category, add `AzureRedisCacheString` to the `piiCategories` parameter. `AzureRedisCacheString` is returned in the API response if detected.

    :::column-end:::
    :::column span="":::

      `en`, `es`, `fr`, `de`, `it`, `pt-pt`, `pt-br`, `zh`, `ja`, `ko`, `nl`, `sv`, `tr`, `hi`, `da`, `nl`, `no`, `ro`, `ar`, `bg`, `hr`, `ms`, `ru`, `sl`, `cs`, `et`, `fi`, `he`, `hu`, `lv`, `sk`, `th`, `uk`

    :::column-end:::
:::row-end:::
:::row:::
    :::column span="":::

        Azure SAS

    :::column-end:::
    :::column span="2":::

        Connection string for Azure software as a service (SaaS).

        To get this entity category, add `AzureSAS` to the `piiCategories` parameter. `AzureSAS` is returned in the API response if detected.

    :::column-end:::
    :::column span="":::

      `en`, `es`, `fr`, `de`, `it`, `pt-pt`, `pt-br`, `zh`, `ja`, `ko`, `nl`, `sv`, `tr`, `hi`, `da`, `nl`, `no`, `ro`, `ar`, `bg`, `hr`, `ms`, `ru`, `sl`, `cs`, `et`, `fi`, `he`, `hu`, `lv`, `sk`, `th`, `uk`

    :::column-end:::
:::row-end:::
:::row:::
    :::column span="":::

        Azure Service Bus Connection String

    :::column-end:::
    :::column span="2":::

        Connection string for an Azure service bus.

        To get this entity category, add `AzureServiceBusString` to the `piiCategories` parameter. `AzureServiceBusString` is returned in the API response if detected.

    :::column-end:::
    :::column span="":::

      `en`, `es`, `fr`, `de`, `it`, `pt-pt`, `pt-br`, `zh`, `ja`, `ko`, `nl`, `sv`, `tr`, `hi`, `da`, `nl`, `no`, `ro`, `ar`, `bg`, `hr`, `ms`, `ru`, `sl`, `cs`, `et`, `fi`, `he`, `hu`, `lv`, `sk`, `th`, `uk`

    :::column-end:::
:::row-end:::
:::row:::
    :::column span="":::

        Azure Storage Account Key

    :::column-end:::
    :::column span="2":::

        Account key for an Azure storage account.

        To get this entity category, add `AzureStorageAccountKey` to the `piiCategories` parameter. `AzureStorageAccountKey` is returned in the API response if detected.

    :::column-end:::
    :::column span="":::

      `en`, `es`, `fr`, `de`, `it`, `pt-pt`, `pt-br`, `zh`, `ja`, `ko`, `nl`, `sv`, `tr`, `hi`, `da`, `nl`, `no`, `ro`, `ar`, `bg`, `hr`, `ms`, `ru`, `sl`, `cs`, `et`, `fi`, `he`, `hu`, `lv`, `sk`, `th`, `uk`

    :::column-end:::
:::row-end:::
:::row:::
    :::column span="":::

        Azure Storage Account Key (Generic)

    :::column-end:::
    :::column span="2":::

        Generic account key for an Azure storage account.

        To get this entity category, add `AzureStorageAccountGeneric` to the `piiCategories` parameter. `AzureStorageAccountGeneric` is returned in the API response if detected.

    :::column-end:::
    :::column span="":::

      `en`, `es`, `fr`, `de`, `it`, `pt-pt`, `pt-br`, `zh`, `ja`, `ko`, `nl`, `sv`, `tr`, `hi`, `da`, `nl`, `no`, `ro`, `ar`, `bg`, `hr`, `ms`, `ru`, `sl`, `cs`, `et`, `fi`, `he`, `hu`, `lv`, `sk`, `th`, `uk`

    :::column-end:::
:::row-end:::
:::row:::
    :::column span="":::

        SQL Server Connection String

    :::column-end:::
    :::column span="2":::

        Connection string for a computer running SQL Server.

        To get this entity category, add `SQLServerConnectionString` to the `piiCategories` parameter. `SQLServerConnectionString` is returned in the API response if detected.

    :::column-end:::
    :::column span="":::

      `en`

    :::column-end:::
:::row-end:::
# [GA API](#tab/ga-api)

## Azure information

These entity types include identifiable Azure information like authentication information and connection strings. Not returned as PHI.

:::row:::
    :::column span="":::
        **Entity**

        Azure DocumentDB Auth Key

    :::column-end:::
    :::column span="2":::
        **Details**

        Authorization key for an Azure Cosmos DB server.

        To get this entity type, add `AzureDocumentDBAuthKey` to the `piiCategories` parameter. `AzureDocumentDBAuthKey` is returned in the API response if detected.

    :::column-end:::
    :::column span="":::
      **Supported languages**

      `en`, `es`, `fr`, `de`, `it`, `pt-pt`, `pt-br`, `zh`, `ja`, `ko`, `nl`, `sv`, `tr`, `hi`, `da`, `nl`, `no`, `ro`, `ar`, `bg`, `hr`, `ms`, `ru`, `sl`, `cs`, `et`, `fi`, `he`, `hu`, `lv`, `sk`, `th`, `uk`

    :::column-end:::
:::row-end:::
:::row:::
    :::column span="":::

        Azure IAAS Database Connection String and Azure SQL Connection String.


    :::column-end:::
    :::column span="2":::

        Connection string for an Azure infrastructure as a service (IaaS) database, and SQL connection string.

        To get this entity type, add `AzureIAASDatabaseConnectionAndSQLString` to the `piiCategories` parameter. `AzureIAASDatabaseConnectionAndSQLString` is returned in the API response if detected.

    :::column-end:::
    :::column span="":::

      `en`, `es`, `fr`, `de`, `it`, `pt-pt`, `pt-br`, `zh`, `ja`, `ko`, `nl`, `sv`, `tr`, `hi`, `da`, `nl`, `no`, `ro`, `ar`, `bg`, `hr`, `ms`, `ru`, `sl`, `cs`, `et`, `fi`, `he`, `hu`, `lv`, `sk`, `th`, `uk`

    :::column-end:::
:::row-end:::
:::row:::
    :::column span="":::

        Azure IoT Connection String

    :::column-end:::
    :::column span="2":::

        Connection string for Azure IoT.

        To get this entity type, add `AzureIoTConnectionString` to the `piiCategories` parameter. `AzureIoTConnectionString` is returned in the API response if detected.

    :::column-end:::
    :::column span="":::

      `en`, `es`, `fr`, `de`, `it`, `pt-pt`, `pt-br`, `zh`, `ja`, `ko`, `nl`, `sv`, `tr`, `hi`, `da`, `nl`, `no`, `ro`, `ar`, `bg`, `hr`, `ms`, `ru`, `sl`, `cs`, `et`, `fi`, `he`, `hu`, `lv`, `sk`, `th`, `uk`

    :::column-end:::
:::row-end:::
:::row:::
    :::column span="":::

        Azure Publish Setting Password

    :::column-end:::
    :::column span="2":::

        Password for Azure publish settings.

        To get this entity type, add `AzurePublishSettingPassword` to the `piiCategories` parameter. `AzurePublishSettingPassword` is returned in the API response if detected.

    :::column-end:::
    :::column span="":::

      `en`, `es`, `fr`, `de`, `it`, `pt-pt`, `pt-br`, `zh`, `ja`, `ko`, `nl`, `sv`, `tr`, `hi`, `da`, `nl`, `no`, `ro`, `ar`, `bg`, `hr`, `ms`, `ru`, `sl`, `cs`, `et`, `fi`, `he`, `hu`, `lv`, `sk`, `th`, `uk`

    :::column-end:::
:::row-end:::
:::row:::
    :::column span="":::

        Azure Redis Cache Connection String

    :::column-end:::
    :::column span="2":::

        Connection string for a Redis cache.

        To get this entity type, add `AzureRedisCacheString` to the `piiCategories` parameter. `AzureRedisCacheString` is returned in the API response if detected.

    :::column-end:::
    :::column span="":::

      `en`, `es`, `fr`, `de`, `it`, `pt-pt`, `pt-br`, `zh`, `ja`, `ko`, `nl`, `sv`, `tr`, `hi`, `da`, `nl`, `no`, `ro`, `ar`, `bg`, `hr`, `ms`, `ru`, `sl`, `cs`, `et`, `fi`, `he`, `hu`, `lv`, `sk`, `th`, `uk`

    :::column-end:::
:::row-end:::
:::row:::
    :::column span="":::

        Azure SAS

    :::column-end:::
    :::column span="2":::

        Connection string for Azure software as a service (SaaS).

        To get this entity type, add `AzureSAS` to the `piiCategories` parameter. `AzureSAS` is returned in the API response if detected.

    :::column-end:::
    :::column span="":::

      `en`, `es`, `fr`, `de`, `it`, `pt-pt`, `pt-br`, `zh`, `ja`, `ko`, `nl`, `sv`, `tr`, `hi`, `da`, `nl`, `no`, `ro`, `ar`, `bg`, `hr`, `ms`, `ru`, `sl`, `cs`, `et`, `fi`, `he`, `hu`, `lv`, `sk`, `th`, `uk`

    :::column-end:::
:::row-end:::
:::row:::
    :::column span="":::

        Azure Service Bus Connection String

    :::column-end:::
    :::column span="2":::

        Connection string for an Azure service bus.

        To get this entity type, add `AzureServiceBusString` to the `piiCategories` parameter. `AzureServiceBusString` is returned in the API response if detected.

    :::column-end:::
    :::column span="":::

      `en`, `es`, `fr`, `de`, `it`, `pt-pt`, `pt-br`, `zh`, `ja`, `ko`, `nl`, `sv`, `tr`, `hi`, `da`, `nl`, `no`, `ro`, `ar`, `bg`, `hr`, `ms`, `ru`, `sl`, `cs`, `et`, `fi`, `he`, `hu`, `lv`, `sk`, `th`, `uk`

    :::column-end:::
:::row-end:::
:::row:::
    :::column span="":::

        Azure Storage Account Key

    :::column-end:::
    :::column span="2":::

        Account key for an Azure storage account.

        To get this entity type, add `AzureStorageAccountKey` to the `piiCategories` parameter. `AzureStorageAccountKey` is returned in the API response if detected.

    :::column-end:::
    :::column span="":::

      `en`, `es`, `fr`, `de`, `it`, `pt-pt`, `pt-br`, `zh`, `ja`, `ko`, `nl`, `sv`, `tr`, `hi`, `da`, `nl`, `no`, `ro`, `ar`, `bg`, `hr`, `ms`, `ru`, `sl`, `cs`, `et`, `fi`, `he`, `hu`, `lv`, `sk`, `th`, `uk`

    :::column-end:::
:::row-end:::
:::row:::
    :::column span="":::

        Azure Storage Account Key (Generic)

    :::column-end:::
    :::column span="2":::

        Generic account key for an Azure storage account.

        To get this entity type, add `AzureStorageAccountGeneric` to the `piiCategories` parameter. `AzureStorageAccountGeneric` is returned in the API response if detected.

    :::column-end:::
    :::column span="":::

      `en`, `es`, `fr`, `de`, `it`, `pt-pt`, `pt-br`, `zh`, `ja`, `ko`, `nl`, `sv`, `tr`, `hi`, `da`, `nl`, `no`, `ro`, `ar`, `bg`, `hr`, `ms`, `ru`, `sl`, `cs`, `et`, `fi`, `he`, `hu`, `lv`, `sk`, `th`, `uk`

    :::column-end:::
:::row-end:::
:::row:::
    :::column span="":::

        SQL Server Connection String

    :::column-end:::
    :::column span="2":::

        Connection string for a computer running SQL Server.

        To get this entity type, add `SQLServerConnectionString` to the `piiCategories` parameter. `SQLServerConnectionString` is returned in the API response if detected.

    :::column-end:::
    :::column span="":::

      `en`

    :::column-end:::
:::row-end:::

---

## Next steps

* [PII overview](../overview.md)
