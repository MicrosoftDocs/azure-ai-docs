---
title: Document Intelligence Studio
titleSuffix: Foundry Tools
description: Learn how to set up Document Intelligence Studio to test Azure Document Intelligence in Foundry Tools features.
author: laujan
manager: nitinme
ms.service: azure-ai-document-intelligence
ms.topic: overview
ms.date: 11/18/2025
ms.author: lajanuar
monikerRange: '>=doc-intel-3.0.0'
---

<!-- markdownlint-disable MD033 -->
<!-- markdownlint-disable MD051 -->

# Studio experience for Document Intelligence

[!INCLUDE [applies to v4.0 v3.1 v3.0](includes/applies-to-v40-v31-v30.md)]

Azure Document Intelligence in Foundry Tools Studio is an online tool that you can use to visually explore, understand, train, and integrate features from Document Intelligence into your applications. The studio provides a platform for you to experiment with the different Document Intelligence models. You can also sample returned data in an interactive manner without the need to write code. You can use the studio experience to:

* Learn more about the different capabilities in Document Intelligence.
* Use your Document Intelligence resource to test models on sample documents or upload your own documents.
* Experiment with different add-on and preview features to adapt the output to your needs.
* Train custom classification models to classify documents.
* Train custom extraction models to extract fields from documents.
* Get sample code for the language-specific SDKs to integrate into your applications.

Currently, features are migrating from [Document Intelligence Studio](https://documentintelligence.ai.azure.com/studio) to the new [Foundry portal](https://ai.azure.com/explore/aiservices/vision). There are some differences in the offerings for the two studios, which determine the correct studio for your use case.

## Choose the correct studio experience

Currently, there are two studios for building and validating Document Intelligence models: the [Foundry portal](https://ai.azure.com/explore/aiservices/vision) and [Document Intelligence Studio](https://documentintelligence.ai.azure.com/studio). As the experiences migrate to the new Foundry portal, some experiences are available in both studios. Other experiences and models are available in only one of the studios.

The following guidelines help you to choose the studio experience for your needs. All the [prebuilt models](overview.md#prebuilt-models) and [general extraction models](overview.md#document-analysis-models) are available for both studios.

### When to use Document Intelligence Studio

Document Intelligence Studio contains all the features released on or before November 2024. For any of the v2.1, v3.0, v3.1 features, continue to use Document Intelligence Studio. 

Document Intelligence Studio provides a visual experience for labeling, training, and validating custom models. For custom document field-extraction models, use Document Intelligence Studio for template and neural models. You can train and use custom classification models only on Document Intelligence Studio. Use Document Intelligence Studio if you want to try out generally available versions of the models from version v3.0, v3.1, and v4.0.

### When to use the Foundry portal

Start with Foundry and try any of the prebuilt document models from the 2024-11-30 version, including general extraction models like read or layout.

## Learn more about Document Intelligence Studio

To learn more about each studio and how you can get started, use the following tabs to select the studio experience.

### [Document Intelligence Studio](#tab/di-studio)

> [!IMPORTANT]
>
> Document Intelligence Studio has distinct URLs for sovereign cloud regions:
> * Azure for US Government: [Document Intelligence Studio (Azure Fairfax)](https://formrecognizer.appliedai.azure.us/studio)
> * Azure operated by 21Vianet: [Document Intelligence Studio (Azure in China)](https://formrecognizer.appliedai.azure.cn/studio)

Document Intelligence Studio supports Document Intelligence v3.0 and later API versions for model analysis and custom model training. Previously trained v2.1 models with labeled data are supported, but not v2.1 model training. For information about migrating from v2.1 to v3.0, see the [REST API migration guide](v3-1-migration-guide.md).

Use the [Document Intelligence Studio quickstart](quickstarts/try-document-intelligence-studio.md) to start analyzing documents with document analysis or prebuilt models. Build custom models and reference the models in your applications by using one of the [language-specific SDKs](quickstarts/get-started-sdks-rest-api.md?view=doc-intel-3.0.0&preserve-view=true).

### Document Intelligence model support

Use the help wizard, labeling interface, training step, and interactive visualizations to understand how each feature works.

* **Read**: Try out the [Document Intelligence Studio read feature](https://documentintelligence.ai.azure.com/studio/read) with sample documents or your own documents. Extract text lines, words, detected languages, and handwritten style, if detected. To learn more, see [Read overview](prebuilt/read.md).
* **Layout**: Try out the [Document Intelligence layout feature](https://documentintelligence.ai.azure.com/studio/layout) with sample documents or your own documents. Extract text, tables, selection marks, and structure information. To learn more, see [Layout overview](prebuilt/layout.md).
* **Prebuilt models**: Use the Document Intelligence prebuilt models to add intelligent document processing to your apps and flows without having to train and build your own models. As an example, start with the [Document Intelligence invoice feature](https://documentintelligence.ai.azure.com/studio/prebuilt?formType=invoice). To learn more, see [Models overview](model-overview.md).
* **Custom extraction models**: Use the [Document Intelligence Studio custom models feature](https://documentintelligence.ai.azure.com/studio/custommodel/projects) to extract fields and values from models that are trained with your data and tailored to your forms and documents. To extract data from multiple form types, create standalone custom models. You can also combine two or more custom models and create a composed model. Test the custom model with your sample documents and iterate to improve the model. To learn more, see [Custom models overview](train/custom-model.md).
* **Custom classification models**: Document classification is a new scenario supported by Document Intelligence. The document classifier API supports classification and splitting scenarios. Train a classification model to identify the different types of documents that your application supports. The input file for the classification model can contain multiple documents and classifies each document within an associated page range. To learn more, see [Custom classification models](train/custom-classifier.md).
* **Add-on capabilities**: Document Intelligence supports more sophisticated analysis capabilities. You can enable and disable these optional capabilities in the studio by using **Analyze Options** on each model page. Four add-on capabilities are available: `highResolution`, `formula`, `font`, and `barcode extraction`. To learn more, see [Add-on capabilities](concept-add-on-capabilities.md).

### [Foundry portal](#tab/ai-foundry)

Document Intelligence is part of the Foundry Tools offerings in the [Foundry portal](https://ai.azure.com/?cid=learnDocs). Each of the Foundry Tools helps developers and organizations rapidly create intelligent and responsible applications. Developers can use the prebuilt and customizable APIs and models to make their applications.

Learn how to [connect your Foundry Tools hub](../../ai-services/connect-services-foundry-portal.md) with Foundry Tools and start using Document Intelligence.

---

## Related content

* See [Document Intelligence Studio](https://formrecognizer.appliedai.azure.com/studio).
* See the [Microsoft Foundry portal](https://ai.azure.com/explore/aiservices/vision).
* Get started with the [Document Intelligence Studio quickstart](quickstarts/get-started-studio.md).
