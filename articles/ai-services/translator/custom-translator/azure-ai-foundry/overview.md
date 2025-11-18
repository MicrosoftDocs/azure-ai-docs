---
title: What is Foundry Tools custom translation?
titleSuffix: Foundry Tools
description: Microsoft Foundry custom translation offers similar capabilities to what Azure Translator in Foundry Tools Hub does for Statistical Machine Translation (SMT), but exclusively for Neural Machine Translation (NMT) systems.
author: laujan
manager: nitinme
ms.service: azure-ai-translator
ms.date: 11/18/2025
ms.author: lajanuar
ms.topic: overview
---

# What are Foundry Tools custom translations?

Microsoft Foundry custom translation, formerly known as Custom Translator, empowers businesses, app developers, and language service providers to craft tailored neural machine translation (NMT) systems. Integrated within the [Azure Translator in Foundry Tools](../../overview.md) service, it allows users to adapt translations to suit specific requirements and contexts. The custom translation feature provides translation solutions that effortlessly integrate with your current applications, workflows, and websites.


Foundry custom translation is built on the robust, cloud-based Translator Text API—the same secure, high-performance platform that powers billions of translations daily—Custom translation enables you to fine-tune and deploy translation systems to and from English. It supports over 100 languages, directly mapping to the extensive NMT capabilities available in the service. For a complete list of supported languages, *see* to [Translator language support](../../language-support.md).

Custom translation makes building and deploying a custom translation system effortless—even if you have no programming experience. Its intuitive user interface lets you seamlessly upload data, train and test your models, and securely deploy them to a production environment. Depending on your training data size, your translation system can be up and running at scale within a few hours.

If you prefer programmatic control, a dedicated API is available. This API enables you to manage model creation and updates directly from your own applications or web services, integrating custom translation capabilities into your existing workflows.

## Features

Custom translation provides different features to build custom translation system.

|Feature  |Description  |
|---------|---------|
|[Apply neural machine translation technology](https://www.microsoft.com/translator/blog/2016/11/15/microsoft-translator-launching-neural-network-based-translations-for-all-its-speech-languages/)     |  Improve your translation by applying neural machine translation (NMT) provided by Custom translator.       |
|[Build systems that knows your business terminology](beginners-guide.md)     |  Customize and build translation systems using parallel documents that understand the terminologies used in your own business and industry.       |
|[Use a dictionary to build your models](how-to/train-model.md#when-to-select-dictionary-only-training)     |   If you don't have training data set, you can train a model with only dictionary data.       |
|[Access your custom translation model](how-to/translate-with-model.md)     |  You can access your custom translation model anytime using your existing applications/ programs via Azure Translator Text API V3.       |

## Get better translations

Azure Translator in Foundry Tools released [Neural Machine Translation (NMT)](https://www.microsoft.com/translator/blog/2016/11/15/microsoft-translator-launching-neural-network-based-translations-for-all-its-speech-languages/) in 2016. NMT provided major advances in translation quality over the industry-standard [Statistical Machine Translation (SMT)](https://en.wikipedia.org/wiki/Statistical_machine_translation) technology. Because NMT better captures the context of full sentences before translating them, it provides higher quality, more human-sounding, and more fluent translations. [Custom translation](https://ai.azure.com/?cid=learnDocs) provides NMT for your custom models resulting in better translation quality.

Custom translation also accepts data that's parallel at the document level to make data collection and preparation more effective. If users have access to versions of the same content in multiple languages but in separate documents, custom translation is able to automatically match sentences across documents. For a list of supported document format, *see* [Custom translation document formats and naming convention](concepts/document-formats-naming-convention.md).

If the appropriate type and amount of training data is supplied, it's not uncommon to see [`BLEU` score](concepts/bleu-score.md) gains between 5 and 10 points by using custom translation.

## Build and translate with custom models

You create a custom translation model by fine tuning an Azure Translator base model with your own data and terminology. 

This article is an overview of how to use fine-tuning to create a custom translation model for your applications across all [supported languages](../../language-support.md).

The steps for creating a custom model are as follows:

1. [**Create a project**](how-to/create-project.md). A project is a work area for composing and building your custom translation system. A project can contain multiple language pairs, models, and documents. All the work you do in custom translation is done inside a specific project.

1. [**Create a language pair**](how-to/create-language-pair.md). A language pair is a wrapper for models, documents, and tests. Each language pair includes all documents that are uploaded into that project with the correct language pair. For example, if you have both an English-to-Spanish language pair and a Spanish-to-English language pair, the same documents are included in both language pairs.

1. [**Upload parallel documents**](how-to/upload-data.md). Parallel documents are pairs of texts where one document is the original language and the other is its human translation. Each sentence in the original document corresponds to a translated sentence in the paired document. Importantly, the designations "source" and "target" are interchangeable—a single pair can be used to train a translation system in either direction.

1. [**Train a model**](how-to/train-model.md). A model is the translation system built for a specific language pair, and a successful training session results in a fully functional model. To train a model, you must provide three distinct and mutually exclusive sets of documents: training, tuning, and testing data. If you supply only training data when queuing a training session, custom translation automatically extracts a random subset of sentences from your training documents to serve as the tuning and testing data—ensuring that these sentences aren't used during the actual training. 

    > [!NOTE]
    > A minimum of 10,000 parallel sentences is required to train a model effectively.

1. [**Test a model**](how-to/test-model.md). The testing set is used to compute the [**BLEU**](concepts/bleu-score.md) score. This score indicates the quality of your translation system.

1. [**Deploy a model**](how-to/deploy-model.md). Your custom model is made available for runtime translation requests in the regions you select.

1. [**Translate text**](../../text-translation/reference/v3/translate.md). Use the cloud-based, secure, high performance, highly scalable Azure Translator [Text API](../../text-translation/reference/v3/translate.md) to make translation requests.

## Next steps

> [!div class="nextstepaction"]
> [Learn how to create a project](how-to/create-project.md)
