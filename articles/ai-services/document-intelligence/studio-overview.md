---
title: Document Intelligence Studio
titleSuffix: Azure AI services
description: Learn how to set up Document Intelligence Studio to test Azure AI Document Intelligence features.
author: laujan
manager: nitinme
ms.service: azure-ai-document-intelligence
ms.topic: overview
ms.date: 03/18/2025
ms.author: lajanuar
monikerRange: '>=doc-intel-3.0.0'
---

<!-- markdownlint-disable MD033 -->
<!-- markdownlint-disable MD051 -->

# Studio experience for Document Intelligence

[!INCLUDE [applies to v4.0 v3.1 v3.0](includes/applies-to-v40-v31-v30.md)]

The studio is an online tool to visually explore, understand, train, and integrate features from the Document Intelligence service into your applications. The studio provides a platform for you to experiment with the different Document Intelligence models and sample returned data in an interactive manner without the need to write code. You can use the studio experience to:

* Learn more about the different capabilities in Document Intelligence.
* Use your Document Intelligence resource to test models on sample documents or upload your own documents.
* Experiment with different add-on and preview features to adapt the output to your needs.
* Train custom classification models to classify documents.
* Train custom extraction models to extract fields from documents.
* Get sample code for the language specific `SDKs` to integrate into your applications.

Currently, we're undergoing the migration of features from the [Document Intelligence Studio](https://documentintelligence.ai.azure.com/studio) to the new [Azure AI Foundry portal](https://ai.azure.com/explore/aiservices/vision). There are some differences in the offerings for the two studios, which determine the correct studio for your use case.

## Choosing the correct studio experience

There are currently two studios, the [Azure AI Foundry portal](https://ai.azure.com/explore/aiservices/vision) and the [Document Intelligence Studio](https://documentintelligence.ai.azure.com/studio) for building and validating  Document Intelligence models. As the experiences migrate to the new Azure AI Foundry portal, some experiences are available in both studios, while other experiences/models are only available in only one of the studios. To follow are a few guidelines for choosing the Studio experience for your needs. All of our [prebuilt models](overview.md#prebuilt-models) and [general extraction models](overview.md#document-analysis-models) are available on both studios.

### When to use [Document Intelligence Studio](https://documentintelligence.ai.azure.com/studio)

Document Intelligence Studio contains all features released on or before November 2024. For any of the v2.1, v3.0, v3.1 features, continue to use the Document Intelligence Studio. Studios provide a visual experience for labeling, training, and validating custom models. For custom document field extraction models, use the Document Intelligence Studio for template and neural models. Custom classification models can only be trained and used on Document Intelligence Studio. Use Document Intelligence Studio if you want to try out GA versions of the models from version v3.0, v3.1, and v4.0.

### When to use [Azure AI Foundry portal](https://ai.azure.com/explore/aiservices/vision)

Start with the new Azure AI Foundry and try any of the prebuilt document models from `2024-11-30` version including general extraction models like Read or Layout.

## Learn more about Document Intelligence Studio

Select the studio experience from the following tabs to learn more about each studio and how you can get started.

### [**Document Intelligence Studio**](#tab/di-studio)

> [!IMPORTANT]
>
> * Document Intelligence Studio has distinct URLs for sovereign cloud regions.
> * Azure for US Government: [Document Intelligence Studio (`Azure Fairfax`)](https://formrecognizer.appliedai.azure.us/studio)
> * Microsoft Azure operated by 21Vianet: [Document Intelligence Studio (`Azure China`)](https://formrecognizer.appliedai.azure.cn/studio)

The studio supports Document Intelligence v3.0 and later API versions for model analysis and custom model training. Previously trained v2.1 models with labeled data are supported, but not v2.1 model training. Refer to the [REST API migration guide](v3-1-migration-guide.md) for detailed information about migrating from v2.1 to v3.0.

Use the [Document Intelligence Studio quickstart](quickstarts/try-document-intelligence-studio.md) to get started analyzing documents with document analysis or prebuilt models. Build custom models and reference the models in your applications using one of the [language specific `SDKs`](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-3.0.0&preserve-view=true). 

### Document Intelligence model support

Use the help wizard, labeling interface, training step, and interactive visualizations to understand how each feature works.

* **Read**: Try out Document Intelligence's [Studio Read feature](https://documentintelligence.ai.azure.com/studio/read) with sample documents or your own documents and extract text lines, words, detected languages, and handwritten style if detected. To learn more, *see* [Read overview](prebuilt/read.md).

* **Layout**: Try out Document Intelligence's [Studio Layout feature](https://documentintelligence.ai.azure.com/studio/layout) with sample documents or your own documents and extract text, tables, selection marks, and structure information. To learn more, *see* [Layout overview](prebuilt/layout.md).

* **Prebuilt models**: Document Intelligence's prebuilt models enable you to add intelligent document processing to your apps and flows without having to train and build your own models. As an example, start with the [Studio Invoice feature](https://documentintelligence.ai.azure.com/studio/prebuilt?formType=invoice). To learn more, *see* [Models overview](model-overview.md).

* **Custom extraction models**: Document Intelligence's [Studio Custom models feature](https://documentintelligence.ai.azure.com/studio/custommodel/projects) enables you to extract fields and values from models trained with your data, tailored to your forms and documents. To extract data from multiple form types, create standalone custom models or combine two, or more, custom models and create a composed model. Test the custom model with your sample documents and iterate to improve the model. To learn more, *see* the [Custom models overview](train/custom-model.md).

* **Custom classification models**: Document classification is a new scenario supported by Document Intelligence. The document classifier API supports classification and splitting scenarios. Train a classification model to identify the different types of documents your application supports. The input file for the classification model can contain multiple documents and classifies each document within an associated page range. To learn more, *see* [custom classification models](train/custom-classifier.md).

* **Add-on Capabilities**: Document Intelligence supports more sophisticated analysis capabilities. These optional capabilities can be enabled and disabled in the studio using the `Analyze Options` button in each model page. There are four add-on capabilities available: `highResolution`, `formula`, `font`, and `barcode extraction` capabilities. To learn more, *see* [Add-on capabilities](concept-add-on-capabilities.md).


### [**Azure AI Foundry portal**](#tab/ai-foundry)

Document Intelligence is part of the Azure AI services offerings in the [Azure AI Foundry portal](https://ai.azure.com/). Each of the Azure AI services helps developers and organizations rapidly create intelligent, cutting-edge, market-ready, and responsible applications with out-of-the-box and prebuilt and customizable APIs and models.

Learn how to [connect your AI services hub](../../ai-services/connect-services-ai-foundry-portal.md) with AI services and get started using Document Intelligence.

---

## Next steps

* Visit [Document Intelligence Studio](https://formrecognizer.appliedai.azure.com/studio).
* Visit [Azure AI Foundry portal](https://ai.azure.com/explore/aiservices/vision).
* Get started with [Document Intelligence Studio quickstart](quickstarts/get-started-studio.md).
