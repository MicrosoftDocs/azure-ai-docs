---
title: Version-based API mapping for entity types and tags
titleSuffix: Foundry Tools
description: Learn about the differences between NER API versions.
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: concept-article
ms.date: 12/05/2025
ms.author: lajanuar
ms.custom: language-service-ner, ignite-2024
---
# Entity types and tags

Use this article to get an overview of the new API changes starting from version `2024-11-01`. This API change mainly introduces two new concepts (`entity types` and `entity tags`) replacing the `category` and `subcategory` fields in the current Generally Available API. A detailed overview of each API parameter and the corresponding supported API versions are found on the [Skill Parameters][../how-to/skill-parameters.md] page.

Since an entity like "Seattle" could be classified as a City, GPE (Geo Political Entity), and a Location, the `type` attribute is used to define the most granular classification, in this case City. The `tags` attribute in the service output is a list all possible classifications (City, GPE, and Location) and their respective confidence score. A full mapping of possible tags for each are listed. The `metadata` attributes in the service output contain additional information about the entity, such as the integer value associated with the entity. 

## Entity types
Entity types represent the lowest (or finest) granularity at which the entity is detected. Types are considered to be the base class detected.

## Entity tags
Entity tags are used to further identify an entity where a detected entity is tagged to indicate the entity type. The entity tags list can include categories, subcategories, and sub-subcategories.

## Changes from versions `2022-05-01` and `2023-04-01` to version `2024-11-01` API
The changes introduce better flexibility for the named entity recognition service, including:

Updates to the structure of input formats:
*    InclusionList
*    ExclusionList
*    Overlap policy

Updates to the handling of output formats:

* More granular entity recognition outputs through introducing the tags list where an entity is tagged with more than one entity tag.
* Overlapping entities where entities could be recognized as more than one entity type and if so, this entity would be returned twice. If an entity was recognized to belong to two entity tags under the same entity type, both entity tags are returned in the tags list.
* Filtering entities using entity tags: to learn more, *see*  [Select returned entities](../how-to-call.md#select-which-entities-to-be-returned).
* Metadata Objects that contain additional information about the entity but currently only act as a wrapper for the existing entity resolution feature. You can learn more about this new feature [here](entity-metadata.md).

## Versions `2022-05-01` and `2023-04-01` to current version API entity mappings
You can see a comparison between the structure of the entity categories/types in the [Supported Named Entity Recognition (NER) entity categories and entity types article](./named-entity-categories.md). The following table presents the mappings between the results you would expect to see from versions `2022-05-01` and `2023-04-01` and the current version API.

| Type           | Tags                                   |
|----------------|----------------------------------------|
| Date           | Temporal, Date                         |
| DateRange      | Temporal, DateRange                    |
| DateTime       | Temporal, DateTime                     |
| DateTimeRange  | Temporal, DateTimeRange                |
| Duration       | Temporal, Duration                     |
| SetTemporal    | Temporal, SetTemporal                  |
| Time           | Temporal, Time                         |
| TimeRange      | Temporal, TimeRange                    |
| City           | GPE, Location, City                    |
| State          | GPE, Location, State                   |
| CountryRegion  | GPE, Location, CountryRegion           |
| Continent      | GPE, Location, Continent               |
| GPE            | Location, GPE                          |
| Location       | Location                               |
| Airport        | Structural, Location                   |
| Structural     | Location, Structural                   |
| Geological     | Location, Geological                   |
| Age            | Numeric, Age                           |
| Currency       | Numeric, Currency                      |
| Number         | Numeric, Number                        |
| PhoneNumber    | PhoneNumber                            |
| NumberRange    | Numeric, NumberRange                   |
| Percentage     | Numeric, Percentage                    |
| Ordinal        | Numeric, Ordinal                       |
| Temperature    | Numeric, Dimension, Temperature        |
| Speed          | Numeric, Dimension, Speed              |
| Weight         | Numeric, Dimension, Weight             |
| Height         | Numeric, Dimension, Height             |
| Length         | Numeric, Dimension, Length             |
| Volume         | Numeric, Dimension, Volume             |
| Area           | Numeric, Dimension, Area               |
| Information    | Numeric, Dimension, Information        |
| Address        | Address                                |
| Person         | Person                                 |
| PersonType     | PersonType                             |
| Organization   | Organization                           |
| Product        | Product                                |
| ComputingProduct | Product, ComputingProduct            |
| IP             | IP                                     |
| Email          | Email                                  |
| URL            | URL                                    |
| Skill          | Skill                                  |
| Event          | Event                                  |
| CulturalEvent  | Event, CulturalEvent                   |
| SportsEvent    | Event, SportsEvent                     |
| NaturalEvent   | Event, NaturalEvent                    |
