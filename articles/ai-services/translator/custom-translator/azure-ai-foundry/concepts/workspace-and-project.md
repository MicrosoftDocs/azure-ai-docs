---
title: "What is a project and language pair? - Custom Translation"
titleSuffix: Azure AI services
description: In This article, learn the differences between a project and a project as well as project categories and labels for the Custom Translation service.
#services: cognitive-services
author: laujan
manager: nitinme
ms.service: azure-ai-translator
ms.date: 01/28/2025
ms.author: lajanuar
ms.topic: conceptual
ms.custom: cogserv-non-critical-translator
#Customer intent: As a Custom Translation user, I want to concept of a project, so that I can use it efficiently.
---
# What is a Custom Translation project?

A project is a work area for composing and building your custom translation system. A project can contain multiple language pairs, models, and documents. All the work you do in Custom Translation is inside a specific project.

project is private to you and the people you invite into your project. Uninvited people don't have access to the content of your project. You can invite as many people as you like into your project and modify or remove their access anytime. You can also create a new project. By default a project doesn't contain any language pairs or documents that already exist in other projects.

## What is a Custom Translation language pair?

A language pair is a wrapper for a model, documents, and tests. Each language pair automatically includes all documents that are uploaded into that project that
have the correct language pair. For example, if you have both an English-to-Spanish language pair and a Spanish-to-English language pair, the same documents are
included in both language pairs. Each project has a Category ID associated with it that is used when querying the [V3 API](../../reference/v3-0-translate.md?tabs=curl) for translations. Category ID is parameter used to get translations from a customized system built with Custom Translation.

## Language pair categories

The category identifies the domain – the area of terminology and style you want to use – for your language pair. Choose the category most relevant to your documents. 

In the same project, you can create language pairs for the same language pair in different categories. Custom Translation prevents creation of a duplicate language pair with the same language pair and category. Applying a label to your language pair allows you to avoid this restriction. Don't use labels unless you're building translation systems for multiple clients, as adding a unique label to your language pair is reflected in your language pairs Category ID.

## Language pair labels

Custom Translation allows you to assign a label to your language pair. The language pair label distinguishes between multiple language pairs with the same language
pair and category. As a best practice, avoid using language pair labels unless necessary.

The language pair label is used as part of the **Category ID**. If the language pair label is left unset or is set identically across language pairs, then language pairs with the same category and *different* language pairs share the same Category ID. This approach is advantageous because it allows you to switch between languages when using the  Translator API without worrying about a Category ID that is unique to each language pair.

For example, if I wanted to enable translations in the Technology domain from English-to-French and from French-to-English, I would create two
language pairs: one for English -\> French, and one for French -\> English. I would specify the same category (Technology) for both and leave the project label
blank. The Category ID for both language pairs would match, so I could query the API for both English and French translations without having to modify my Category ID.

If you're a language service provider and want to serve multiple customers with different models that retain the same category and language pair, use a language pair label to differentiate between customers.

## Next steps

> [!div class="nextstepaction"]
> [Learn about model training](../how-to-custom-translation-train-model.md)
