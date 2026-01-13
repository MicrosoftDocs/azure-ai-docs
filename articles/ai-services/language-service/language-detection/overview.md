---
title: What is language detection in Azure Language in Foundry Tools?
titleSuffix: Foundry Tools
description: An overview of language detection in Azure Language, which helps you detect the language that text is written in by returning language codes.
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: overview
ms.date: 11/18/2025
ms.author: lajanuar
ms.custom: language-service-language-detection
---
# What is language detection in Azure Language in Foundry Tools?

Language detection is one of the features offered by [Azure Language in Foundry Tools](../overview.md), a collection of machine learning and AI algorithms in the cloud for developing intelligent applications that involve written language. Language detection is able to detect more than 100 languages in their primary script. In addition, the service offers [script detection](./how-to/call-api.md#script-name-and-script-code) for each detected language using  [ISO 15924 standard](https://wikipedia.org/wiki/ISO_15924) for a [select number of languages](./language-support.md#script-detection).
This documentation contains the following types of articles:

* [**Quickstarts**](quickstart.md) are getting-started instructions to guide you through making requests to the service.
* [**How-to guides**](how-to/call-api.md) contain instructions for using the service in more specific or customized ways.

## Language detection features

* Language detection: For each document, returns the main language, its ISO 639-1 code, readable name, confidence score, script name, and ISO 15924 script code.

* Script detection: To distinguish between multiple scripts used to write certain languages, such as Kazakh, language detection returns a script name and script code according to the ISO 15924 standard.  

* Ambiguous content handling: To help disambiguate language based on the input, you can specify an ISO 3166-1 alpha-2 country/region code. For example, the word "communication" is common to both English and French. Specifying the origin of the text as France can help the language detection model determine the correct language.

[!INCLUDE [Typical workflow for pre-configured language features](../includes/overview-typical-workflow.md)]


## Get started with language detection

[!INCLUDE [development options](./includes/development-options.md)]

## Responsible AI 

An AI system includes not only the technology, but also individuals who operate the system, people who experience its effects, and the broader environment where the system functions. Read the [transparency note for language detection](/azure/ai-foundry/responsible-ai/language-service/transparency-note-language-detection) to learn about responsible AI use and deployment in your systems. 

[!INCLUDE [Responsible AI links](../includes/overview-responsible-ai-links.md)]

## Next steps

There are two ways to get started using the entity linking feature:
* [Microsoft Foundry](../../../ai-foundry/what-is-foundry.md) is a web-based platform that lets you use several Language features without needing to write code.
* The [quickstart article](quickstart.md) for instructions on making requests to the service using the REST API and client library SDK.  
