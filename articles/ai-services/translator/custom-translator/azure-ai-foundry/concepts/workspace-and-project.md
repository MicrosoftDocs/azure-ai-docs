---
title: Foundry Tools custom translation project?
titleSuffix: Foundry Tools
description: In This article, learn the differences about creating projects, project categories, and labels for the custom translation service.
#services: cognitive-services
author: laujan
manager: nitinme
ms.service: azure-ai-translator
ms.date: 11/18/2025
ms.author: lajanuar
ms.topic: concept-article
ms.custom: cogserv-non-critical-translator
#Customer intent: As a custom translation user, I want to concept of a project, so that I can use it efficiently.
---
# What are Foundry Tools custom translation projects?

A project is a work area for composing and building your custom translation system. A project can contain multiple language pairs, models, and documents. All the work you do in custom translation is inside a specific project.

A project is private to you and the people you invite into your project. Uninvited people don't have access to the content of your project. You can invite as many people as you like into your project and modify or remove their access anytime. You can also create a new project. By default a project doesn't contain any language pairs or documents that already exist in other projects.

## What is a custom translation language pair?

A language pair is a wrapper for a model, documents, and tests. Each language pair automatically includes all documents that are uploaded into that project that
have the correct language pair. For example, if you have both an English-to-Spanish language pair and a Spanish-to-English language pair, the same documents are
included in both language pairs. Each project has a Category ID associated with it used when querying the [V3 API](../../../text-translation/reference/v3/translate.md) for translations. Category ID is parameter used to get translations from a customized system built with custom translation.

## Language pair categories

The category identifies the domain – the area of terminology and style you want to use – for your language pair. Choose the category most relevant to your documents. 

In the same project, you can create language pairs for the same language pair in different categories. Custom translation prevents creation of a duplicate language pair with the same language pair and category. Applying a label to your language pair allows you to avoid this restriction. Don't use labels unless you're building translation systems for multiple clients, as adding a unique label to your language pair is reflected in your language pairs Category ID.

## Language pair labels

Custom translation allows you to assign a label to your language pair. The language pair label distinguishes between multiple language pairs with the same language pair and category. As a best practice, avoid using language pair labels unless necessary.

The language pair label is used as part of the **Category ID**. When the language pair label is either unspecified or identical for multiple language pairs, those pairs with the same category but *distinct* language combinations share the same Category ID. This method offers a significant benefit by enabling seamless transitions between languages while utilizing the Translator API. Unlike traditional systems, there's no need to manage a separate Category ID for each language pair, simplifying the process considerably and enhancing efficiency.

For example, if I wanted to enable translations in the Technology domain from English-to-French and from French-to-English, I would create two language pairs: one for English -\> French, and one for French -\> English. I would specify the same category (Technology) for both and leave the project label blank. The Category ID for both language pairs would match, so I could query the API for both English and French translations without having to modify my Category ID.

For language service providers aiming to cater to multiple customers with models that share the same category and language pair, applying a language pair label is an effective way to distinguish between different clients. This approach ensures clarity and organization when managing customer-specific models within identical language pairings.

## Next steps

> [!div class="nextstepaction"]
> [Learn about model training](../how-to/train-model.md)
