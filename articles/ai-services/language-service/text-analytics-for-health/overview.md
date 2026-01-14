---
title: What is the Text Analytics for health in Azure Language in Foundry Tools?
titleSuffix: Foundry Tools
description: An overview of Text Analytics for health in Azure Language, which helps you extract medical information from unstructured text, like clinical documents.
#services: cognitive-services
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: overview
ms.date: 12/15/2025
ms.author: lajanuar
ms.custom: language-service-health
---
# What is Text Analytics for health?

[!INCLUDE [service notice](includes/service-notice.md)]

Text Analytics for health is one of the prebuilt features offered by [Azure Language in Foundry Tools](../overview.md). Text Analytics for health uses machine learning to identify and label medical information in unstructured text such as doctor's notes, clinical documents, and electronic health records. It extracts key data from sources like discharge summaries to support healthcare analysis.

> [!TIP]
> Try out Text Analytics for health [in Microsoft Foundry portal](https://ai.azure.com/). There you can [utilize a currently existing Language Studio resource or create a new Foundry resource](../../../ai-services/connect-services-foundry-portal.md) in order to use this service.

This documentation contains the following types of articles:
* The [**quickstart article**](quickstart.md) provides a short tutorial that guides you with making your first request to the service.
* The [**how-to guides**](how-to/call-api.md) contain detailed instructions on how to make calls to the service using the hosted API or using the on-premises Docker container.
* The [**conceptual articles**](concepts/health-entity-categories.md) provide in-depth information on each of the service's features, named entity recognition, relation extraction, entity linking, and assertion detection.

## Text Analytics for health features

Text Analytics for health performs four key functions, all with a single API call:

* Named entity recognition
* Relation extraction
* Entity linking
* Assertion detection

[!INCLUDE [Text Analytics for health](includes/features.md)]

Text Analytics for health can receive unstructured text in English, German, French, Italian, Spanish, Portuguese, and Hebrew.

Additionally, Text Analytics for health can return the processed output using the Fast Healthcare Interoperability Resources (FHIR) structure that enables the service's integration with other electronic health systems.



> [!VIDEO https://learn.microsoft.com/Shows/AI-Show/Introducing-Text-Analytics-for-Health/player]

## Usage scenarios

Text Analytics for health can be used in multiple scenarios across various industries.
Some common customer motivations for using Text Analytics for health include:
* Assisting and automating the processing of medical documents by proper medical coding to ensure accurate care and billing.
* Increasing the efficiency of analyzing healthcare data to help drive the success of value-based care models similar to Medicare.
* Minimizing healthcare provider effort by automating the aggregation of key patient data for trend and pattern monitoring.
* Facilitating and supporting the adoption of HL7 standards across the healthcare industry. By doing so, we help improve the exchange, integration, sharing, retrieval, and delivery of electronic health information in all areas of healthcare services.

### Example use cases: 

|Use case|Description|
|--|--|
|Extract insights and statistics|Identify medical entities such as symptoms, medications, diagnosis from clinical and research documents in order to extract insights and statistics for different patient cohorts.|
|Develop predictive models using historic data|Power solutions for planning, decision support, risk analysis and more, based on prediction models created from historic data.|
|Annotate and curate medical information|Support solutions for clinical data annotation and curation such as automating clinical coding and digitizing manually created data.|
|Review and report medical information|Potential medical information errors found during quality assurance reviews.|
|Assist with decision support|Enable solutions that provide humans with assistive information relating to patients' medical information for faster and more reliable decisions.|

## Get started with Text Analytics for health

[!INCLUDE [Development options](./includes/development-options.md)]


## Input requirements and service limits

Text Analytics for health is designed to receive unstructured text for analysis. For more information, see [data and service limits](../concepts/data-limits.md).

Text Analytics for health works with various input languages. For more information,  see [language support](language-support.md).

[!INCLUDE [Developer reference](../includes/reference-samples-text-analytics.md)]


## Responsible use of AI

An AI system includes the technology, the individuals who operate the system, the people who experience its effects, and the broader environment where the system functions all play a role. Read the [transparency note for Text Analytics for health](/azure/ai-foundry/responsible-ai/language-service/transparency-note-health) to learn about responsible AI use and deployment in your systems. 

[!INCLUDE [Responsible AI links](../includes/overview-responsible-ai-links.md)]
