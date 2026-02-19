---
title: Entity categories recognized by Named Entity Recognition in Azure Language in Foundry Tools
titleSuffix: Foundry Tools
description: Learn about the entities the NER feature can recognize from unstructured text.
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: concept-article
ms.date: 11/18/2025
ms.author: lajanuar
ms.custom: language-service-ner
---
# Named entity categories and types

Named Entity Recognition (NER) is a computational linguistic process within natural language processing (NLP) that uses predictive models to detect and identify entities within unstructured text. After entities are detected, each entity receives a semantic label and is organized into predefined categories and types:

* **Entity Categories** refer to main classifications of named entities such as Location, Organization, Date, or Quantity.

* **Entity Types** provide more detailed distinctions within the broader categories, allowing for more granularity and flexibility.

This article provides a list of entity categories identified and returned by the Named Entity Recognition (NER) process.

## Language Support

The [NER language support](../language-support.md) page lists all languages available for the named entities in this article. Any exceptions are noted for specific named entities.

## Supported API versions:

* [**Stable: Generally Available (GA)**](/rest/api/language/analyze-text/analyze-text/analyze-text?view=rest-language-analyze-text-2025-11-01&preserve-view=true&tabs=HTTP#definitions)
* [**Preview: 2025-05-15-preview**](/rest/api/language/analyze-text/analyze-text/analyze-text?view=rest-language-analyze-text-2025-11-01&preserve-view=true&tabs=HTTP#definitions)

> [!NOTE]
> Beginning with the GA API (released 2024-11-01), the **Subcategory** field is no longer supported. All entity classifications now use the **type** field.

## NER named entity types

|Entities|Entities|Entities|Entities|Entities|Entities|
|:---:|:---:|:---:|:---:|:---:|:---:|
|[Address](#type-address)|[Age](#type-age)|[Airport](#type-airport)|[Area](#type-area)|[City](#type-city)|[ComputingProduct](#type-computingproduct)|
|[Continent](#type-continent)|[CountryRegion](#type-countryregion)|[CulturalEvent](#type-culturalevent)|[Currency](#type-currency)|[Date](#type-date)|[DateRange](#type-daterange)|
|[DateTime](#type-datetime)|[DateTimeRange](#type-datetimerange)|[Dimension](#type-dimension)|[Duration](#type-duration)|[Email](#type-email)|[Event](#type-event)|
|[Geological](#type-geographical)|[GPE](#type-gpe)|[Height](#type-height)|[Information](#type-information)|[IpAddress](#type-ipaddress)|[Length](#type-length)|
|[Location](#type-location)|[NaturalEvent](#type-naturalevent)|[Number](#type-number)|[NumberRange](#type-numberrange)|[Ordinal](#type-ordinal)|[Organization](#type-organization)|
|[OrganizationMedical](#type-organizationmedical)|[OrganizationSports](#type-organizationsports)|[OrganizationStockExchange](#type-organizationstockexchange)|[Percentage](#type-percentage)|[Person](#type-person)|[PersonType](#type-persontype)|
|[PhoneNumber](#type-phonenumber)|[Product](#type-product)|[SetTemporal](#type-settemporal)|[Skill](#type-skill)|[Speed](#type-speed)|[SportsEvent](#type-sportsevent)|
|[State](#type-state)|[Structural](#type-structural)|[Temporal](#type-temporal)|[Temperature](#type-temperature)|[Time](#type-time)|[TimeRange](#type-timerange)|
|[URL](#type-url)|[Volume](#type-volume)|[Weight](#type-weight)||

### Type: Address
##### Category: Address

|Entity|Tags|Detail|
|---|---|---|
|**Address**|Address|A distinct identifier assigned to a physical or geographic location, utilized for navigation, delivery services, and formal administrative purposes.|

### Type: Age
##### Category: Quantity


|Entity|Tags|Detail|Metadata|
|---|---|---|---|
|**Age**|Numeric, Quantity, Age|A quantitative measure representing the length of time from an individual's birth to a specific reference date.|[Age metadata](entity-metadata.md#age)|


### Type: Airport
##### Category: Location

|Entity|Tags|Detail|
|---|---|---|
|**Airport**|Location, Airport|A designated location equipped with facilities for the landing, takeoff, and maintenance of aircraft.  |

### Type: Area
##### Category: Quantity

|Entity|Tags|Detail|MetaData|
|---|---|---|---|
|**Area**|Numeric, Quantity, Dimension, Area|The measurement of a surface or region expressed in square units.|[Area metadata](entity-metadata.md#area)|

### Type: City
##### Category: Location

|Entity|Tags|Detail|
|---|---|---|
|**City**|Location,GPE,City|A settlement characterized by a dense population and infrastructure. |

### Type: ComputingProduct
##### Category: Product

|Entity|Tags|Detail|
|---|---|---|
|**ComputingProduct**|Product, ComputingProduct|A hardware or software item designed for computational tasks or digital processing.|


### Type: Continent
##### Category: Location


|Entity|Tags|Detail|
|---|---|---|
|**Continent**|Location,GPE,Continent|A vast, continuous landmass on the Earth's surface. | 


### Type: CountryRegion
##### Category: Location

|Entity|Tags|Detail|
|---|---|---|
|**CountryRegion**|Location,GPE,CountryRegion|A distinct territorial entity recognized as a nation or administrative area.|

### Type: CulturalEvent
##### Category: Event

|Entity|Tags|Detail|Language support|
|---|---|---|---|
|**CulturalEvent**|Event, EventCultural|An organized activity or gathering that reflects or celebrates cultural practices or traditions| `en`|


### Type: Currency
##### Category: Quantity


|Entity|Tags|Detail|MetaData|
|---|---|---|---|
|**Currency**|Numeric, Quantity, Currency|A system of money in common use, typically issued by a government and used as a medium of exchange.|[Currency metadata](entity-metadata.md#currency)|


### Type: Date
##### Category: DateTime


|Entity|Tags|Detail|MetaData|
|---|---|---|
|**Date**|DateTime, Date|A specific calendar day expressed in terms of day, month, and year.|[Date metadata](entity-metadata.md#date)|


### Type: DateRange
##### Category: DateTime


|Entity|Tags|Detail|
|---|---|---|
|**DateRange**|DateTime, DateRange|A span of time defined by a start and end date.|


### Type: DateTime
##### Category: DateTime


|Entity|Tags|Detail|MetaData|
|---|---|---|---|
|**DateTime**|DateTime|A data type encompassing date and time components used in scheduling or logging events.|[DateTime metadata](entity-metadata.md#datetime)|


### Type: DateTimeRange
##### Category: DateTime


|Entity|Tags|Detail|
|---|---|---|
|**DateTimeRange**|DateTime, DateTimeRange|A period defined by a starting and ending date and time.|


### Type: Dimension
##### Category: Quantity


|Entity|Tags|Detail|
|---|---|---|
|**Dimension**|Numeric, Quantity, Dimension|The measurable size or extent of an object or area, commonly expressed in terms of length, width, height, or depth.|


### Type: Duration
##### Category: DateTime


|Entity|Tags|Detail|
|---|---|---|
|**Duration**|DateTime, Duration|The total time interval during which an event occurs or continues.|


### Type: Email
##### Category: Email

|Entity|Tags|Detail|
|---|---|---|
|**Email**|Email|An electronic message sent and received via digital mail systems.|


### Type: Event
##### Category: Event


|Entity|Tags|Detail|
|---|---|---|
|**Event**|Event|A specific or noteworthy instance, or activity occurring within a defined context.|


### Type: Geographical
##### Category: Location

|Entity|Tags|Detail|
|---|---|---|
|**Geographical**|Location, Geographical|Earth's physical geography and natural features, including landforms like rivers, mountains, and valleys.|

### Type: GPE
##### Category: Location

|Entity|Tags|Detail|
|---|---|---|
|**GPE**|Location, GPE|Geo political entity (GPE) is a region or area defined by political boundaries or governance. |


### Type: Height
##### Category: Quantity

|Entity|Tags|Detail|
|---|---|---|
|**Height**|Numeric, Quantity, Dimension, Height|The measurement of vertical distance.|


### Type: Information
##### Category: Information

|Entity|Tags|Detail|MetaData|
|---|---|---|---|
|**Information**|Information|Structured data or processed knowledge transmitted or acquired about a specific entity, event, or condition.|[Information metadata](entity-metadata.md#information)|


### Type: IpAddress
##### Category:IpAddress

|Entity|Tags|Detail|
|---|---|---|
|**IpAddress**|IpAddress|A unique numerical label assigned a device connected to a computer network using Internet Protocol.|


### Type: Length
##### Category: Quantity

|Entity|Tags|Detail|MetaData|
|---|---|---|---|
|**Length**|Numeric, Quantity, Dimension, Length|The measurement of an object or distance between two points.|[Length metadata](entity-metadata.md#length)|


### Type: Location
##### Category: Location

|Entity|Tags|Detail|
|---|---|---|
|**Location**|Location|A specific point or area in physical or virtual space defined by exact coordinates, metadata, or unique identifiers that can be referenced, queried, or accessed.|

### Type: NaturalEvent
##### Category: Event

|Entity|Tags|Detail|Language support|
|---|---|---|---|
|**NaturalEvent**|Event, EventNatural|An occurrence or phenomenon that takes place in a physical environment as a result of natural processes, without direct human intervention.|`en`|


### Type: Number
##### Category: Quantity

|Entity|Tags|Detail|MetaData|
|---|---|---|---|
|**Number**|Numeric, Quantity, Number|A mathematical value used for counting, measuring, or labeling.|[Number metadata](entity-metadata.md#number)|


### Type: NumberRange
##### Category: Quantity

|Entity|Tags|Detail|MetaData|
|---|---|---|---|
|**NumberRange**|Numeric, Quantity, NumberRange|A set of numbers that includes all values between a specified minimum and maximum boundary.|[NumberRange metadata](entity-metadata.md#numericrange)


### Type: Ordinal
##### Category: Quantity

|Entity|Tags|Detail|MetaData|
|---|---|---|---|
|**Ordinal**|Numeric, Ordinal|A number indicating position or order in a sequence, such as first, second, or third.|[Ordinal metadata](entity-metadata.md#ordinal)|


### Type: Organization
##### Category: Organization

|Entity|Tags|Detail|
|---|---|---|
|**Organization**|Organization|A company, institution, or group formed for a specific purpose.|


### Type: OrganizationMedical
##### Category: Organization

|Entity|Tags|Detail|Language support|
|---|---|---|---|
|**OrganizationMedical**|Organization, OrganizationMedical|An entity that delivers or facilitates healthcare or medical services.|`en`|

### Type: OrganizationSports

|Entity|Tags|Detail|Language support|
|---|---|---|---|
|**OrganizationSports**|Organization, OrganizationSports|An entity that manages or promotes sports activities or teams (**Organization**).|`en`|

### Type: OrganizationStockExchange
##### Category: Organization

|Entity|Tags|Detail|Language support|
|---|---|---|---|
|**OrganizationStockExchange**|Organization, OrganizationStockExchange|An institution that manages or facilitates the trading of stocks and securities.|`en`|

### Type: Percentage
##### Category: Quantity

|Entity|Tags|Detail|
|---|---|---|
|**Percentage**|Numeric, Quantity, Percentage|A value expressed as a fraction of 100, representing a proportion or share.|


### Type: Person
##### Category: Person

|Entity|Tags|Detail|
|---|---|---|
|**Person**|Person|An individual human being or a legal entity with rights and responsibilities.|


### Type: PersonType
##### Category: PersonType

|Entity|Tags|Detail|
|---|---|---|
|**PersonType**|PersonType|A classification describing the role or category of a person, such as employee or customer.|


### Type: PhoneNumber
##### Category: PhoneNumber

|Entity|Tags|Detail|
|---|---|---|
|**PhoneNumber**|PhoneNumber|A unique sequence of digits assigned to a telephone line or mobile device that serves as an identifier within a communication network.|


### Type: Product
##### Category: Product

|Entity|Tags|Detail|
|---|---|---|
|**Product**|Product|An item or service offering value and created for sale or use.|


### Type: SetTemporal
##### Category: DateTime


|Entity|Tags|Detail|MetaData|
|---|---|---|---|
|**Set**|DateTime, Set|A sequence of sets, where each individual set is associated with a timestamp.|[Set metadata](entity-metadata.md#set)|

### Type: Skill
##### Category: Skill

|Entity|Tags|Detail|
|---|---|---|
|**Skill**|Skill|The ability to perform a task or activity, acquired through training or experience.|

### Type: Speed
##### Category: Quantity

|Entity|Tags|Detail|MetaData|
|---|---|---|---|
|**Speed**|Numeric, Quantity, Dimension, Speed|The rate at which something moves or operates, typically measured in units per time.|[Speed metadata](entity-metadata.md#speed)|

### Type: SportsEvent
##### Category: Event


|Entity|Tags|Detail|Language support|
|---|---|---|---|
|**SportsEvent**|Event, EventSports|An organized competition or exhibition that involves skill or strategy typically governed by a set of rules.|`en`|


### Type: State
##### Category: Location

|Entity|Tags|Detail|
|---|---|---|
|**State**|Location,GPE,State|The institutional framework and governing apparatus for a defined geographical area or political entity.|


### Type: Structural
##### Category: Location

|Entity|Tags|Detail|
|---|---|---|
|**Structural**|Location, Structural|The configuration or organizational schema of components within a system or object that define the overall architecture.|

### Type: Temporal
##### Category: DateTime

|Entity|Tags|Detail|
|---|---|---|
|**Temporal**|Related to time or time-based changes, such as data, events, or processes that vary over time.|


### Type: Temperature
##### Category: Quantity

|Entity|Tags|Detail|MetaData|
|---|---|---|---|
|**Temperature**|Numeric, Quantity, Temperature|A quantitative expression that indicates the measure of heat or cold present in an object or environment, commonly expressed in units such as degrees.|[Temperature metadata](entity-metadata.md#temperature)|


### Type: Time
##### Category: DateTime

|Entity|Tags|Detail|MetaData|
|---|---|---|---|
|**Time**|DateTime, Time|A quantifiable interval during which an event occurs, a process unfolds, or a condition persists.|[Time metadata](entity-metadata.md#time)|


### Type: TimeRange
##### Category: DateTime


|Entity|Tags|Detail|
|---|---|---|
|**TimeRange**|DateTime, TimeRange|An interval period defined by specific start and designated end times. |


### Type: URL
##### Category: URL


|Entity|Tags|Detail|
|---|---|---|
|**Skill**|URL|A Uniform Resource Identifier is a string of characters that uniquely identifies a resource on the internet.|


### Type: Volume
##### Category: Quantity


|Entity|Tags|Detail|MetaData|
|---|---|---|---|
|**Volume**|Numeric, Quantity, Dimension, Volume|The measure of three-dimensional space taken up by a substance or object, typically expressed in cubic units.|[Volume metadata](entity-metadata.md#volume)|


### Type: Weight
##### Category: Quantity

|Entity|Tags|Detail|MetaData|
|---|---|---|---|
|**Weight**|Numeric, Quantity, Dimension, Weight|The measure of the force exerted on an object due to gravity typically expressed in units like kilograms or pounds.|[Weight metadata](entity-metadata.md#weight)|



## Next steps

[NER overview](../overview.md)
