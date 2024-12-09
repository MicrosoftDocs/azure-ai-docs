---
title: Custom template document model - Document Intelligence 
titleSuffix: Azure AI services
description: Use the custom template document model to train a model to extract data from structured or templated forms.
author: laujan
manager: nitinme
ms.service: azure-ai-document-intelligence
ms.topic: conceptual
ms.date: 08/07/2024
ms.author: lajanuar
monikerRange: 'doc-intel-4.0.0 || <=doc-intel-3.1.0'
---


# Document Intelligence custom template model

::: moniker range="doc-intel-4.0.0"

[!INCLUDE [preview-version-notice](../includes/preview-notice.md)]

[!INCLUDE [applies to v4.0](../includes/applies-to-v40.md)]
::: moniker-end

::: moniker range="doc-intel-3.1.0"
[!INCLUDE [applies to v3.1](../includes/applies-to-v31.md)]
::: moniker-end

::: moniker range="doc-intel-3.0.0"
[!INCLUDE [applies to v3.0](../includes/applies-to-v30.md)]
::: moniker-end

::: moniker range="doc-intel-2.1.0"
[!INCLUDE [applies to v2.1](../includes/applies-to-v21.md)]
::: moniker-end

Custom template (formerly custom form) is an easy-to-train document model that accurately extracts labeled key-value pairs, selection marks, tables, regions, and signatures from documents. Template models use layout cues to extract values from documents and are suitable to extract fields from highly structured documents with defined visual templates.

::: moniker range=">=doc-intel-3.0.0"

Custom template models share the same labeling format and strategy as custom neural models, with support for more field types and languages.

::: moniker-end

## Model capabilities

Custom template models support key-value pairs, selection marks, tables, signature fields, and selected regions.

| Form fields | Selection marks | Tabular fields (Tables) | Signature | Selected regions | Overlapping fields |
|:--:|:--:|:--:|:--:|:--:|:--:|
| Supported| Supported | Supported | Supported| Supported | Not supported |

::: moniker range=">=doc-intel-3.0.0"

## Tabular fields

With the release of API versions v3.0 and  later, custom template models add support for **cross page** tabular fields (tables):  

* To label a table that spans multiple pages, label each row of the table across the different pages in a single table.
* As a best practice, ensure that your dataset contains a few samples of the expected variations. For example, include samples where the entire table is on a single page and where tables span two or more pages if you expect to see those variations in documents.

Tabular fields are also useful when extracting repeating information within a document that isn't recognized as a table. For example, a repeating section of work experiences in a resume can be labeled and extracted as a tabular field.

::: moniker-end

## Dealing with variations

Template models rely on a defined visual template, changes to the template results in lower accuracy. In those instances, split your training dataset to include at least five samples of each template and train a model for each of the variations. You can then [compose](composed-models.md) the models into a single endpoint. For subtle variations, like digital PDF documents and images, it's best to include at least five examples of each type in the same training dataset.

## Input requirements

* For best results, provide one clear photo or high-quality scan per document.

* Supported file formats:

    |Model | PDF |Image: </br>J`PEG/JPG`, `PNG`, `BMP`, `TIFF`, `HEIF` | Microsoft Office: </br> Word (DOCX), Excel (XLSX), PowerPoint (PPTX), and HTML|
    |--------|:----:|:-----:|:---------------:|
    |Read            | ✔    | ✔    | ✔  |
    |Layout          | ✔  | ✔ | ✔ (2024-02-29-preview, 2023-10-31-preview or later)  |
    |General&nbsp;Document| ✔  | ✔ |   |
    |Prebuilt        |  ✔  | ✔ |   |
    |Custom          |  ✔  | ✔ |   |

    &#x2731; Microsoft Office files are currently not supported for other models or versions.

* For PDF and TIFF, up to 2,000 pages can be processed (with a free tier subscription, only the first two pages are processed).

* The file size for analyzing documents is 500 MB for paid (S0) tier and 4 MB for free (F0) tier.

* Image dimensions must be between 50 x 50 pixels and 10,000 px x 10,000 pixels.

* If your PDFs are password-locked, you must remove the lock before submission.

* The minimum height of the text to be extracted is 12 pixels for a 1024 x 768 pixel image. This dimension corresponds to about `8`-point text at 150 dots per inch (`DPI`).

* For custom model training, the maximum number of pages for training data is 500 for the custom template model and 50,000 for the custom neural model.

* For custom extraction model training, the total size of training data is 50 MB for template model and 1G-MB for the neural model.

* For custom classification model training, the total size of training data is `1GB`  with a maximum of 10,000 pages.

## Training a model

::: moniker range="doc-intel-4.0.0"

Custom template models are generally available starting with v2.0 API and later versions. If you're starting with a new project or have an existing labeled dataset, use the v3.1 or v3.0 API with Document Intelligence Studio to train a custom template model.

| Model | REST API | SDK | Label and Test Models|
|--|--|--|--|
| Custom template  | [v3.1 API](/rest/api/aiservices/document-models/build-model?view=rest-aiservices-2024-02-29-preview&preserve-view=true&branch=docintelligence&tabs=HTTP)| [Document Intelligence SDK](../quickstarts/get-started-sdks-rest-api.md?view=doc-intel-3.1.0&preserve-view=true)| [Document Intelligence Studio](https://formrecognizer.appliedai.azure.com/studio)|

With the v3.0 and later APIs, the build operation to train model supports a new ```buildMode``` property, to train a custom template model, set the ```buildMode``` to ```template```.

```REST
https://{endpoint}/documentintelligence/documentModels:build?api-version=2024-07-31-preview


{
  "modelId": "string",
  "description": "string",
  "buildMode": "template",
  "azureBlobSource":
  {
    "containerUrl": "string",
    "prefix": "string"
  }
}
```

::: moniker-end

::: moniker range="doc-intel-3.1.0"

Custom template models are generally available with the [v3.1 API](/rest/api/aiservices/document-models/build-model?view=rest-aiservices-2023-07-31&preserve-view=true&tabs=HTTP). If you're starting with a new project or have an existing labeled dataset, use the v3.1 or v3.0 API with Document Intelligence Studio to train a custom template model.

| Model | REST API | SDK | Label and Test Models|
|--|--|--|--|
| Custom template  | [v3.1 API](/rest/api/aiservices/document-models/analyze-document?view=rest-aiservices-2023-07-31&preserve-view=true&tabs=HTTP)| [Document Intelligence SDK](../quickstarts/get-started-sdks-rest-api.md?view=doc-intel-3.0.0&preserve-view=true)| [Document Intelligence Studio](https://formrecognizer.appliedai.azure.com/studio)|

With the v3.0 and later APIs, the build operation to train model supports a new ```buildMode``` property, to train a custom template model, set the ```buildMode``` to ```template```.

```REST
https://{endpoint}/formrecognizer/documentModels:build?api-version=2023-07-31

{
  "modelId": "string",
  "description": "string",
  "buildMode": "template",
  "azureBlobSource":
  {
    "containerUrl": "string",
    "prefix": "string"
  }
}
```

::: moniker-end

## Supported languages and locales

*See* our [Language Support—custom models](../language-support/custom.md) page for a complete list of supported languages.

::: moniker range="doc-intel-2.1.0"

Custom (template) models  are generally available with the [v2.1 API](/rest/api/aiservices/analyzer?view=rest-aiservices-v2.1&preserve-view=true).

| Model | REST API | SDK | Label and Test Models|
|--|--|--|--|
| Custom model (template) | [Document Intelligence 2.1 ](/rest/api/aiservices/analyzer?view=rest-aiservices-v2.1&preserve-view=true)| [Document Intelligence SDK](../quickstarts/get-started-sdks-rest-api.md?view=doc-intel-2.1.0&preserve-view=true?pivots=programming-language-python)| [Document Intelligence Sample labeling tool](https://fott-2-1.azurewebsites.net/)|

::: moniker-end

## Next steps

Learn to create and compose custom models:

::: moniker range=">=doc-intel-3.0.0"

> [!div class="nextstepaction"]
> [**Build a custom model**](../how-to-guides/build-a-custom-model.md)
> [**Compose custom models**](../how-to-guides/compose-custom-models.md)

::: moniker-end

::: moniker range="doc-intel-2.1.0"

> [!div class="nextstepaction"]
> [**Build a custom model**](custom-model.md#build-a-custom-model)
> [**Compose custom models**](composed-models.md#development-options)

::: moniker-end
