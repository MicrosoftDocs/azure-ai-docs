---
title: Entity categories recognized by Named Entity Recognition in Azure AI Language
titleSuffix: Azure AI services
description: Learn about the entities the NER feature can recognize from unstructured text.
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: conceptual
ms.date: 08/06/2025
ms.author: lajanuar
ms.custom: language-service-ner
---

# Named entity categories and types

Named Entity Recognition (NER) is a computational linguistic process within natural language processing (NLP) that uses predictive models to detect and identify entities within unstructured text. After entities are detected, each entity receives a semantic label and is organized into predefined categories and types:

* **Entity Categories** refer to main classifications of named entities such as Location, Organization, Date, or Quantity.

* **Entity Types** provide more detailed distinctions within the broader categories, allowing for more granularity and flexibility.

This article provides a list of entity categories identified and returned by the Named Entity Recognition (NER) process.## Language Support


The [NER language support](../language-support.md) page lists all languages available for the named entities in this article. Any exceptions are noted for specific named entities.

### NER entities

# [Preview (2025-08-01-preview)](#tab/preview-api)

> [!NOTE]
> Beginning with the API preview releases, the `tags` fields replace the GA `subtype` fields, providing greater flexibility.

## Type: Address
##### Category: Address

|Entity|Tags|Detail|
|---|---|---|
|**Address**|Address|A distinct identifier assigned to a physical or geographic location, utilized for navigation, delivery services, and formal administrative purposes.|

## Type: Age
##### Category: Quantity


|Entity|Tags|Detail|
|---|---|---|---|
|**Age**|Numeric, Quantity, Age|A quantitative measure representing the length of time from an individual's birth to a specific reference date.|


## Type: Airport
##### Category: Airport

|Entity|Tags|Detail|
|---|---|---|
|**Airport**|Airport|A designated location equipped with facilities for the landing, takeoff, and maintenance of aircraft.  |

## Type: Area
##### Category: Quantity

|Entity|Tags|Detail|
|---|---|---|
|**Area**|Numeric, Quantity, Dimension, Area|The measurement of a surface or region expressed in square units. |

## Type: City
##### Category: Location

|Entity|Tags|Detail|
|---|---|---|
|**City**|Location,GPE,City|A settlement characterized by a dense population and infrastructure. |

## Type: ComputingProduct
##### Category: Product

|Entity|Tags|Detail|
|---|---|---|
|**ComputingProduct**|Product, ComputingProduct|A hardware or software item designed for computational tasks or digital processing.|


## Type: Continent
##### Category: Location


|Entity|Tags|Detail|Language support|
|---|---|---|---|
|**Continent**|Location,GPE,Continent|A vast, continuous landmass on the Earth's surface. | `en`|


## Type: CountryRegion
##### Category: Location

|Entity|Tags|Detail|
|---|---|---|
|**CountryRegion**|Location,GPE,CountryRegion|A distinct territorial entity recognized as a nation or administrative area.|

## Type: CulturalEvent
##### Category: Event

|Entity|Tags|Detail|Language support|
|---|---|---|---|
|**CulturalEvent**|Event, EventCultural|An organized activity or gathering that reflects or celebrates cultural practices or traditions| `en`|


## Type: Currency
##### Category: Quantity


|Entity|Tags|Detail|
|---|---|---|
|**Currency**|Numeric, Quantity, Currency|A system of money in common use, typically issued by a government and used as a medium of exchange.|


## Type: Date
##### Category: DateTime


|Entity|Tags|Detail|
|---|---|---|
|**Date**|DateTime, Date|A specific calendar day expressed in terms of day, month, and year.|


## Type: DateRange
##### Category: DateTime


|Entity|Tags|Detail|
|---|---|---|
|**DateRange**|DateTime, DateRange|A span of time defined by a start and end date.|


## Type: DateTime
##### Category: DateTime


|Entity|Tags|Detail|
|---|---|---|
|**DateTime**|DateTime|A data type encompassing date and time components used in scheduling or logging events.|


## Type: DateTimeRange
##### Category: DateTime


|Entity|Tags|Detail|
|---|---|---|
|**DateTimeRange**|DateTime, DateTimeRange|A period defined by a starting and ending date and time.|


## Type: Dimension
##### Category: Quantity


|Entity|Tags|Detail|
|---|---|---|
|**Dimension**|Numeric, Quantity, Dimension|The measurable size or extent of an object or area, commonly expressed in terms of length, width, height, or depth.|


## Type: Duration
##### Category: DateTime


|Entity|Tags|Detail|
|---|---|---|
|**Duration**|DateTime, Duration|The total time interval during which an event occurs or continues.|


## Type: Email
##### Category: Email

|Entity|Tags|Detail|
|---|---|---|
|**Email**|Email|An electronic message sent and received via digital mail systems.|


## Type: Event
##### Category: Event


|Entity|Tags|Detail|
|---|---|---|
|**Event**|Event|A specific or noteworthy instance, or activity occurring within a defined context.|

## Type: EventNatural
##### Category: Event

|Entity|Tags|Detail|Language support|
|---|---|---|---|
|**EventNatural**|Event, EventNatural|An occurrence or phenomenon that takes place in a physical environment as a result of natural processes, without direct human intervention.|`en`|

## Type: EventSports
##### Category: Event


|Entity|Tags|Detail|Language support|
|---|---|---|---|
|**EventSports**|Event, EventSports|An organized competition or exhibition that involves skill or strategy typically governed by a set of rules.|`en`|


## Type: Geographical
##### Category: Location

|Entity|Tags|Detail|
|---|---|---|
|**Geographical**|Location, Geographical|The science and study of the Earth's surface and features.|

## Type: GeoPoliticalEntity (GPE)
##### Category: Location

|Entity|Tags|Detail|
|---|---|---|
|**GeoPoliticalEntity**|Location, GPE|A region or area defined by political boundaries or governance. |


## Type: Height
##### Category: Quantity

|Entity|Tags|Detail|
|---|---|---|
|**Height**|Numeric, Quantity, Dimension, Height|The measurement of vertical distance.|


## Type: Information
##### Category: Information

|Entity|Tags|Detail|
|---|---|---|
|**Information**|Information|Structured data or processed knowledge transmitted or acquired about a specific entity, event, or condition.|


## Type: IpAddress
##### Category:IpAddress

|Entity|Tags|Detail|
|---|---|---|
|**IpAddress**|IpAddress|A unique numerical label assigned a device connected to a computer network using Internet Protocol.|


## Type: Length
##### Category: Quantity

|Entity|Tags|Detail|
|---|---|---|
|**Length**|Numeric, Quantity, Dimension, Length|The measurement of an object or distance between two points.|


## Type: Location
##### Category: Location

|Entity|Tags|Detail|
|---|---|---|
|**Location**|Location|A specific point or area in physical or virtual space defined by exact coordinates, metadata, or unique identifiers that can be referenced, queried, or accessed.|


## Type: Number
##### Category: Quantity

|Entity|Tags|Detail|
|---|---|---|
|**Number**|Numeric, Quantity, Number|A mathematical value used for counting, measuring, or labeling.|


## Type: NumberRange
##### Category: Quantity

|Entity|Tags|Detail|
|---|---|---|
|**NumberRange**|Numeric, Quantity, NumberRange|A set of numbers that includes all values between a specified minimum and maximum boundary.|


## Type: Numeric
##### Category: Numeric

|Entity|Tags|Detail|
|---|---|---|
|**Numeric**|Numeric|A value that can be measured, calculated, or represented as numbers, such as integers, decimals, or other number formats. |


## Type: Ordinal
##### Category: Quantity

|Entity|Tags|Detail|
|---|---|---|
|**Ordinal**|Numeric, Ordinal|A number indicating position or order in a sequence, such as first, second, or third.|


## Type: Organization
##### Category: Organization

|Entity|Tags|Detail|
|---|---|---|
|**Organization**|Organization|A company, institution, or group formed for a specific purpose.|


## Type: OrganizationMedical
##### Category: Organization

|Entity|Tags|Detail|Language support|
|---|---|---|---|
|**OrganizationMedical**|Organization, OrganizationMedical|An entity that delivers or facilitates healthcare or medical services.|`en`|

## Type: OrganizationSports

|Entity|Tags|Detail|Language support|
|---|---|---|---|
|**OrganizationSports**|Organization, OrganizationSports|An entity that manages or promotes sports activities or teams (**Organization**).|`en`|

## Type: OrganizationStockExchange
##### Category: Organization

|Entity|Tags|Detail|Language support|
|---|---|---|---|
|**OrganizationStockExchange**|Organization, OrganizationStockExchange|An institution that manages or facilitates the trading of stocks and securities.|`en`|

## Type: Percentage
##### Category: Quantity

|Entity|Tags|Detail|
|---|---|---|
|**Percentage**|Numeric, Quantity, Percentage|A value expressed as a fraction of 100, representing a proportion or share.|


## Type: Person
##### Category: Person

|Entity|Tags|Detail|
|---|---|---|
|**Person**|Person|An individual human being or a legal entity with rights and responsibilities.|


## Type: PersonType
##### Category: PersonType

|Entity|Tags|Detail|
|---|---|---|
|**PersonType**|PersonType|A classification describing the role or category of a person, such as employee or customer.|


## Type: PhoneNumber
##### Category: PhoneNumber

|Entity|Tags|Detail|
|---|---|---|
|**PhoneNumber**|PhoneNumber|A unique sequence of digits assigned to a telephone line or mobile device that serves as an identifier within a communication network.|


## Type: Product
##### Category: Product

|Entity|Tags|Detail|
|---|---|---|
|**Product**|Product|An item or service offering value and created for sale or use.|

## Type: Quantity
##### Category: Quantity
Beginning with the `2025-05-15-preview` model and in all future versions, the **Quantity** entity is replaced contextually by the following, more specific entities:

* [Age](#type-age)
* [Area](#type-age)
* [Currency](#type-currency)
* [Dimension](#type-dimension)
* [Height](#type-height)
* [Information](#type-information)
* [Length](#type-length)
* [Number](#type-number)
* [NumberRange](#type-numberrange)
* [Ordinal](#type-ordinal)
* [Percentage](#type-percentage)
* [Speed](#type-speed)
* [Temperature](#type-temperature)
* [Volume](#type-volume)
* [Weight](#type-weight)


## Type: Set
##### Category: DateTime


|Entity|Tags|Detail|
|---|---|---|
|**Set**|DateTime, Set|A sequence of sets, where each individual set is associated with a timestamp.|

## Type: Skill
##### Category: Skill

|Entity|Tags|Detail|
|---|---|---|
|**Skill**|Skill|The ability to perform a task or activity, acquired through training or experience.|

## Type: Speed
##### Category: Quantity

|Entity|Tags|Detail|
|---|---|---|
|**Speed**|Numeric, Quantity, Dimension, Speed|The rate at which something moves or operates, typically measured in units per time.|


## Type: State
##### Category: Location

|Entity|Tags|Detail|
|---|---|---|
|**State**|Location,GPE,State|The institutional framework and governing apparatus for a defined geographical area or political entity.|


## Type: Structural
##### Category: Location

|Entity|Tags|Detail|
|---|---|---|
|**Structural**|Location, Structural|The configuration or organizational schema of components within a system or object that define the overall architecture.|


## Type: Temperature
##### Category: Quantity

|Entity|Tags|Detail|
|---|---|---|
|**Temperature**|Numeric, Quantity, Temperature|A quantitative expression that indicates the measure of heat or cold present in an object or environment, commonly expressed in units such as degrees.|


## Type: Time
##### Category: DateTime

|Entity|Tags|Detail|
|---|---|---|
|**Time**|DateTime, Time|A quantifiable interval during which an event occurs, a process unfolds, or a condition persists.|


## Type: TimeRange
##### Category: DateTime


|Entity|Tags|Detail|
|---|---|---|
|**TimeRange**|DateTime, TimeRange|An interval period defined by specific start and designated end times. |


## Type: URL
##### Category: URL


|Entity|Tags|Detail|
|---|---|---|
|**Skill**|URL|A Uniform Resource Identifier is a string of characters that uniquely identifies a resource on the internet.|


## Type: Volume
##### Category: Quantity


|Entity|Tags|Detail|
|---|---|---|
|**Volume**|Numeric, Quantity, Dimension, Volume|The measure of three-dimensional space taken up by a substance or object, typically expressed in cubic units.|


## Type: Weight
##### Category: Quantity

|Entity|Tags|Detail|
|---|---|---|
|**Weight**|Numeric, Quantity, Dimension, Weight|The measure of the force exerted on an object due to gravity typically expressed in units like kilograms or pounds.|

# [GA (generally available)](#tab/ga-api)

## Type: Address
##### Category: Address

|Entity|Detail|
|---|---|
|**Address**|A distinct identifier assigned to a physical or geographic location, utilized for navigation, delivery services, and formal administrative purposes.|

## Type: Age

*See* [**Quantity**](#type-quantity) subtype (**Age**).


## Type: Currency

*See* [**Quantity**](#type-quantity) subtype (**Currency**).


## Type: Date

*See* [**DateTime**](#type-datetime) subtype (**Date**).

## Type: DateRange
*See* [**DateTime**](#type-datetime) subtype (**DateRange**).


## Type: DateTime

|Entity|Detail|
|---|---|
|**DateTime**|A data type encompassing date and time components used in scheduling or logging events.|

The **DateTime** entity can have the following subtypes:

|Subtype|Detail|
|---|---|
|**Date**|A specific calendar day expressed in terms of day, month, and year.|
|**Time**|A quantifiable interval during which an event occurs, a process unfolds, or a condition persists.|
|**DateRange**| span of time defined by a start and end date.|
|**TimeRange**|An interval period defined by specific start and designated end times.|
|**Duration**|The total time interval during which an event occurs or continues.|
|**Set**|A temporal sequence wherein each element is linked to a specific timestamp.|


## Type: Dimension

*See* [**Quantity**](#type-quantity) subtypes (**Dimension**).


## Type: Duration

*See* [**DateTime**](#type-datetime) subtype (**Duration**).


## Type: Email

|Entity|Detail|
|---|---|
|**Email**|An electronic message sent and received via digital mail systems. |


## Type: Event

|Entity|Detail|
|---|---|
|**Event**|A specific or noteworthy instance, or activity occurring within a defined context (**Event**).|

The **Event** entity can have the following subtypes:

|Subtype|Detail|Language support|
|---|---|---|
|**Cultural**|An organized activity or gathering that reflects or celebrates cultural practices or traditions.| `en`|
|**Natural**|An occurrence or phenomenon that takes place in a physical environment as a result of natural processes, without direct human intervention.|`en`|
|**Sports**|An organized competition or exhibition that involves skill or strategy typically governed by a set of rules. |`en`|

## Type: EventCultural

*See* [**Event**](#type-event) subtype (**Cultural**).


## Type: EventNatural

*See* [**Event**](#type-event) subtype (**Natural**).

## Type: EventSports

*See* [**Event**](#type-event) subtype (**Sports**).


## Type: Geographical

*See* [**Location**](#type-location) subtype (**Geographical**).


## Type: GeoPoliticalEntity

*See* [**Location**](#type-location) subtype (**Geopolitical Entity**).


## Type: IpAddress

|Entity|Detail|
|---|---|
|**IpAddress**|A unique numerical label assigned a device connected to a computer network using Internet Protocol.|


## Type: Location

|Entity|Detail|
|---|---|
|**Location**|A specific point or area in physical or virtual space defined by exact coordinates, metadata, or unique identifiers that can be referenced, queried, or accessed.|

The **Location** entity can have the following subtypes:

|Subtype|Detail|Language support|
|---|---|---|
|**GeoPolitical**|Referencing a region or area defined by political boundaries or governance.|[Language support](../language-support.md)|
|**Structural**|The configuration or organizational schema of components within a system or object that define the overall architecture.|`en`|
|**Geographical**|Referencing the study or representation of Earth's features, including natural and human-made characteristics, and their spatial relationships|`en`|


## Type: Number

*See* [**Quantity**](#type-number) subtype (**Number**).


## Type: Ordinal

*See* [**Quantity**](#type-quantity) subtype (**Ordinal**).


## Type: Organization

|Entity|Detail|
|---|---|
|**Organization**|A company, institution, or group formed for a specific purpose.|

The **Organization** entity can have the following subtypes:

|Subtype|Detail|Language support|
|---|---|---|
|**Medical**|An entity that delivers or facilitates healthcare or medical services.|`en`|
|**Sports**|An entity that manages or promotes sports activities or teams.|`en`|
|**Stock exchange**|An institution that manages or facilitates the trading of stocks and securities.|`en`|


## Type: OrganizationMedical

*See* [**Organization**](#type-organization) subtype (**Medical**).


## Type: OrganizationSports

*See* [**Organization**](#type-organization) subtype (**Sports**).


## Type: OrganizationStockExchange

*See* [**Organization**](#type-location) subtype (**StockExchange**).


## Type: Percentage

*See* [**Quantity**](#type-quantity) subtype (**Percentage**).


## Type: Person

|Entity|Detail|
|---|---|
|**Person**|An individual human being or a legal entity with rights and responsibilities.|


## Type: PersonType

|Entity|Detail|
|---|---|
|**PersonType**|A classification describing the role or category of a person, such as employee or customer.|


## Type: PhoneNumber

|Entity|Detail|
|---|---|
|**PhoneNumber**|A unique sequence of digits assigned to a telephone line or mobile device that serves as an identifier within a communication network.|


## Type: Product

|Entity|Detail|
|---|---|
|**Product**|An item or service offering value and created for sale or use.|

The **Product** entity can have the following subtypes:

|Subtype|Detail|
|---|---|
|**ComputingProduct**|A hardware or software item designed for computational tasks or digital processing.|


## Type: Quantity

|Entity|Detail|
|---|---|
|**Quantity**|A property or characteristic of a physical object, phenomenon, or concept that can be measured or quantified.|

The Quantity entity can have the following subtypes:

| Subtype | Detail |
|---|---|
| **Age**|A quantitative measure representing the length of time from an individual's birth to a specific reference date.|
| **Currency**|A system of money in common use, typically issued by a government and used as a medium of exchange.|
| **Dimension** |The measurable size or extent of an object or area, commonly expressed in terms of length, width, height, or depth.|
| **Number** |A mathematical value used for counting, measuring, or labeling.|
| **Ordinal**  |A number indicating position or order in a sequence, such as first, second, or third.|
| **Percentage** |A value expressed as a fraction of 100, representing a proportion or share|
| **Temperature** |A quantitative expression that indicates the measure of heat or cold present in an object or environment, commonly expressed in units such as degrees.|


## Type: Set

*See* [**DateTime**](#type-datetime) subtype (**Set**).


## Type: Skill

|Entity|Detail|
|---|---|
|**Skill**|The ability to perform a task or activity, acquired through training or experience.|




## Type: Structural

*See* [**Location**](#type-location) subtype (**Structural**).


## Type: Temperature

*See* [**Quantity**](#type-quantity) subtypes (**Temperature**).


## Type: Time

*See* [**DateTime**](#type-datetime) subtype (**Time**).


## Type: TimeRange

*See* [**DateTime**](#type-datetime) subtype (**TimeRange**).


## Type: URL

|Entity|Detail|
|---|---|
|**Skill**|A Uniform Resource Identifier is a string of characters that uniquely identifies a resource on the internet.|

---

## Next steps

* [NER overview](../overview.md)
