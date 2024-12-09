---
title: Custom classification model - Document Intelligence
titleSuffix: Azure AI services
description: Use the custom classification model to train a model to identify and split the documents you process within your application.
author: vkurpad
manager: nitinme
ms.service: azure-ai-document-intelligence
ms.topic: conceptual
ms.date: 09/26/2024
ms.author: lajanuar
ms.custom:
  - references_regions
monikerRange: '>=doc-intel-3.1.0'
---


# Document Intelligence custom classification model

::: moniker range="doc-intel-4.0.0"
[!INCLUDE [preview-version-notice](../includes/preview-notice.md)]

**This content applies to:**![checkmark](../media/yes-icon.png) **v4.0 (preview)** | **Previous version:** ![blue-checkmark](../media/blue-yes-icon.png) [**v3.1 (GA)**](?view=doc-intel-3.1.0&preserve-view=tru)
:::moniker-end

:::moniker range="doc-intel-3.1.0"
**This content applies to:** ![checkmark](../media/yes-icon.png) **v3.1 (GA)** | **Latest version:** ![purple-checkmark](../media/purple-yes-icon.png) [**v4.0 (preview)**](?view=doc-intel-4.0.0&preserve-view=true)
:::moniker-end

::: moniker range=">=doc-intel-4.0.0"

> [!IMPORTANT]
>
> * The `2024-07-31-preview` API, custom classification model won't split documents by default during the analyzing process.
> * You need to explicitly set the ``splitMode`` property to auto to preserve the behavior from previous releases. The default for `splitMode` is `none`.
> * If your input file contains multiple documents, you need to enable splitting by setting the ``splitMode`` to ``auto``.

::: moniker-end

Azure AI Document Intelligence is a cloud-based Azure AI service that enables you to build intelligent document processing solutions. Document Intelligence APIs analyze images, PDFs, and other document files to extract and detect various content, layout, style, and semantic elements.

Custom classification models are deep-learning-model types that combine layout and language features to accurately detect and identify documents you process within your application. Custom classification models perform classification of an input file one page at a time to identify the documents within and can also identify multiple documents or multiple instances of a single document within an input file.

## Model capabilities

> [!NOTE]
>
> * Starting with the `2024-02-29-preview` API, custom clasification models support incremental training. You can add new samples to existing classes or add new classes by referencing an existing classifier.

Custom classification models can analyze a single- or multi-file documents to identify if any of the trained document types are contained within an input file. Here are the currently supported scenarios:

* A single file containing one document type, such as a loan application form.
* A single file containing multiple document types. For instance, a loan application package that contains a loan application form, payslip, and bank statement.

* A single file containing multiple instances of the same document. For instance, a collection of scanned invoices.

✔️ Training a custom classifier requires at least `two` distinct classes and a minimum of `five` document samples per class. The model response contains the page ranges for each of the classes of documents identified.

✔️ The maximum allowed number of classes is `500`. The maximum allowed number of document samples per class is `100`.

The model classifies each page of the input document, unless specified, to one of the classes in the labeled dataset. You can specify the page numbers to analyze in the input document as well. To set the threshold for your application, use the confidence score from the response.

### Incremental training

With custom models, you need to maintain access to the training dataset to update your classifier with new samples for an existing class, or add new classes. Classifier models now support incremental training where you can reference an existing classifier and append new samples for an existing class or add new classes with samples. Incremental training enables scenarios where data retention is a challenge and the classifier needs to be updated to align with changing business needs. Incremental training is supported with models trained with API version `2024-02-29-preview` and later.

> [!IMPORTANT]
>
> Incremental training is only supported with models trained with the same API version. If you are trying to extend a model, use the API version the original model was trained with to extend the model. Incremental training is only supported with API version **2024-07-31-preview** or later.

Incremental training requires that you provide the original model ID as the `baseClassifierId`. See [incremental training](../concept/incremental-classifier.md) to learn more about how to use incremental training.

### Office document type support

You can now train classifiers to recognize document types in various formats including PDF, images, Word, PowerPoint, and Excel. When assembling your training dataset, you can add documents of any of the supported types. The classifier doesn't require you to explicitly label specific types. As a best practice, ensure your training dataset has at least one sample of each format to improve the overall accuracy of the model.

### Compare custom classification and composed models

A custom classification model can replace [a composed model](../train/composed-models.md) in some scenarios but there are a few differences to be aware of:

| Capability | Custom classifier process | Composed model process |
|--|--|--|
|Analyze a single document of unknown type belonging to one of the types trained for extraction model processing.| &#9679; Requires multiple calls.<br> &#9679; Call the classification model based on the document class. This step allows for a confidence-based check before invoking the extraction model analysis.<br> &#9679; Invoke the extraction model. | &#9679; Requires a single call to a composed model containing the model corresponding to the input document type. |
 |Analyze a single document of unknown type belonging to several types trained for extraction model processing.| &#9679;Requires multiple calls.<br> &#9679; Make a call to the classifier that ignores documents not matching a designated type for extraction.<br> &#9679; Invoke the extraction model. | &#9679;  Requires a single call to a composed model. The service selects a custom model within the composed model with the highest match.<br> &#9679; A composed model can't ignore documents.|
|Analyze a file containing multiple documents of known or unknown type belonging to one of the types trained for extraction model processing.| &#9679; Requires multiple calls.<br> &#9679; Call the extraction model for each identified document in the input file.<br> &#9679; Invoke the extraction model. | &#9679;  Requires a single call to a composed model.<br> &#9679; The composed model invokes the component model once on the first instance of the document.<br> &#9679;The remaining documents are ignored. |

## Language support

:::moniker range="doc-intel-3.1.0"
Classification models currently only support English language documents.
:::moniker-end

::: moniker range=">=doc-intel-4.0.0"
Classification models can now be trained on documents of different languages. See [supported languages](../language-support/custom.md) for a complete list.
::: moniker-end

## Input requirements

Supported file formats:

|Model | PDF |Image:<br>`jpeg/jpg`, `png`, `bmp`, `tiff`, `heif`| Microsoft Office:<br> Word (docx), Excel (xlxs), PowerPoint (pptx)|
|--------|:----:|:-----:|:---------------:|
|Read            | ✔    | ✔    | ✔  |
|Layout          | ✔  | ✔ | ✔ (2024-02-29-preview, 2023-10-31-preview, and later)  |
|General&nbsp;Document| ✔  | ✔ |   |
|Prebuilt        |  ✔  | ✔ |   |
|Custom extraction|  ✔  | ✔ |   |
|Custom classification|  ✔  | ✔ | ✔ |

* For best results, provide five clear photos or high-quality scans per document type.

* For PDF and TIFF, up to 2,000 pages can be processed (with a free tier subscription, only the first two pages are processed).

* The file size for analyzing documents is 500 MB for paid (S0) tier and 4 MB for free (F0) tier.

* Image dimensions must be between 50 x 50 pixels and 10,000 px x 10,000 pixels.

* If your PDFs are password-locked, you must remove the lock before submission.

* The minimum height of the text to be extracted is 12 pixels for a 1024 x 768 pixel image. This dimension corresponds to about `8`-point text at 150  dots per inch (`DPI`).

* For custom model training, the maximum number of pages for training data is 500 for the custom template model and 50,000 for the custom neural model.

* For custom extraction model training, the total size of training data is 50 MB for template model and 1G-MB for the neural model.

* For custom classification model training, the total size of training data is 1 GB with a maximum of 10,000 pages.

## Document splitting

When you have more than one document in a file, the classifier can identify the different document types contained within the input file. The classifier response contains the page ranges for each of the identified document types contained within a file. This response can include multiple instances of the same document type.

::: moniker range=">=doc-intel-4.0.0"
The `analyze` operation now includes a `splitMode` property that gives you granular control over the splitting behavior.

* To treat the entire input file as a single document for classification set the splitMode to `none`. When you do so, the service returns just one class for the entire input file.
* To classify each page of the input file, set the splitMode to `perPage`. The service attempts to classify each page as an individual document.
* Set the splitMode to `auto` and the service identifies the documents and associated page ranges.

::: moniker-end

## Best practices

Custom classification models require a minimum of five samples per class to train. If the classes are similar, adding extra training samples improves model accuracy.

The classifier attempts to assign each document to one of the classes, if you expect the model to see document types not in the classes that are part of the training dataset, you should plan to set a threshold on the classification score or add a few representative samples of the document types to an `"other"` class. Adding an `"other"` class ensures that unneeded documents don't affect your classifier quality.

## Training a model

Custom classification models are supported by **v4.0: 2024-02-29-preview, 2024-07-31-preview** and **v3.1: 2023-07-31 (GA)** APIs. [Document Intelligence Studio](https://formrecognizer.appliedai.azure.com/studio) provides a no-code user interface to interactively train a custom classifier. Follow the [how to guide](../how-to-guides/build-a-custom-classifier.md) to get started.

When using the REST API, if you organize your documents by folders, you can use the `azureBlobSource` property of the request to train a classification model.

:::moniker range="doc-intel-4.0.0"

```json

https://{endpoint}/documentintelligence/documentClassifiers:build?api-version=2024-02-29-preview

{
  "classifierId": "demo2.1",
  "description": "",
  "docTypes": {
    "car-maint": {
        "azureBlobSource": {
            "containerUrl": "SAS URL to container",
            "prefix": "sample1/car-maint/"
            }
    },
    "cc-auth": {
        "azureBlobSource": {
            "containerUrl": "SAS URL to container",
            "prefix": "sample1/cc-auth/"
            }
    },
    "deed-of-trust": {
        "azureBlobSource": {
            "containerUrl": "SAS URL to container",
            "prefix": "sample1/deed-of-trust/"
            }
    }
  }
}

```

:::moniker-end

:::moniker range="doc-intel-3.1.0"

```json
https://{endpoint}/formrecognizer/documentClassifiers:build?api-version=2023-07-31

{
  "classifierId": "demo2.1",
  "description": "",
  "docTypes": {
    "car-maint": {
        "azureBlobSource": {
            "containerUrl": "SAS URL to container",
            "prefix": "{path to dataset root}/car-maint/"
            }
    },
    "cc-auth": {
        "azureBlobSource": {
            "containerUrl": "SAS URL to container",
            "prefix": "{path to dataset root}/cc-auth/"
            }
    },
    "deed-of-trust": {
        "azureBlobSource": {
            "containerUrl": "SAS URL to container",
            "prefix": "{path to dataset root}/deed-of-trust/"
            }
    }
  }
}

```

:::moniker-end

Alternatively, if you have a flat list of files or only plan to use a few select files within each folder to train the model, you can use the `azureBlobFileListSource` property to train the model. This step requires a `file list` in [JSON Lines](https://jsonlines.org/) format. For each class, add a new file with a list of files to be submitted for training.

```json
{
  "classifierId": "demo2",
  "description": "",
  "docTypes": {
    "car-maint": {
      "azureBlobFileListSource": {
        "containerUrl": "SAS URL to container",
        "fileList": "{path to dataset root}/car-maint.jsonl"
      }
    },
    "cc-auth": {
      "azureBlobFileListSource": {
        "containerUrl": "SAS URL to container",
        "fileList": "{path to dataset root}/cc-auth.jsonl"
      }
    },
    "deed-of-trust": {
      "azureBlobFileListSource": {
        "containerUrl": "SAS URL to container",
        "fileList": "{path to dataset root}/deed-of-trust.jsonl"
      }
    }
  }
}

```

As an example, the file list `car-maint.jsonl` contains the following files.

```json
{"file":"classifier/car-maint/Commercial Motor Vehicle - Adatum.pdf"}
{"file":"classifier/car-maint/Commercial Motor Vehicle - Fincher.pdf"}
{"file":"classifier/car-maint/Commercial Motor Vehicle - Lamna.pdf"}
{"file":"classifier/car-maint/Commercial Motor Vehicle - Liberty.pdf"}
{"file":"classifier/car-maint/Commercial Motor Vehicle - Trey.pdf"}
```

::: moniker range=">=doc-intel-4.0.0"
## Overwriting a model

> [!NOTE]
> Starting with the `2024-07-31-preview` API, custom classification models support overwriting a model in-place.

You can now update the custom classification in-place. Directly overwriting the model would lose you the ability to compare model quality before deciding to replace the existing model. Model overwriting is allowed when the `allowOverwrite` property is explicitly specified in the request body. It's impossible to recover the overwritten, original model once this action is performed.

```json


{
  "classifierId": "existingClassifierName",
  "allowOverwrite": true,  // Default=false
  ...
}

```

## Copy a model

> [!NOTE]
> Starting with the `2024-07-31-preview` API, custom classification models support copying a model to and from any of the following regions:
>
> * **East US**
> * **West US2**
> * **West Europe**
>
> Use the [**REST API**](/rest/api/aiservices/operation-groups?view=rest-aiservices-2024-07-31-preview&preserve-view=true) or [**Document Intelligence Studio**](https://documentintelligence.ai.azure.com/studio/document-classifier/projects) to copy a model to another region.

### Generate Copy authorization request

The following HTTP request gets copy authorization from your target resource. You need to enter the endpoint and key of your target resource as headers.

```http
POST https://myendpoint.cognitiveservices.azure.com/documentintelligence/documentClassifiers:authorizeCopy?api-version=2024-07-31-preview
Ocp-Apim-Subscription-Key: {<your-key>}
```

Request body

```json
{
  "classifierId": "targetClassifier",
  "description": "Target classifier description"
}
```

You receive a `200` response code with response body that contains the JSON payload required to initiate the copy.

```json
{
  "targetResourceId": "/subscriptions/targetSub/resourceGroups/targetRG/providers/Microsoft.CognitiveServices/accounts/targetService",
  "targetResourceRegion": "targetResourceRegion",
  "targetClassifierId": "targetClassifier",
  "targetClassifierLocation": "https://targetEndpoint.cognitiveservices.azure.com/documentintelligence/documentClassifiers/targetClassifier",
  "accessToken": "accessToken",
  "expirationDateTime": "timestamp"
}
```

### Start Copy operation

The following HTTP request starts the copy operation on the source resource. You need to enter the endpoint and key of your source resource as the url and header. Notice that the request URL contains the classifier ID of the source classifier you want to copy.

```http
POST {endpoint}/documentintelligence/documentClassifiers/{classifierId}:copyTo?api-version=2024-07-31-preview
Ocp-Apim-Subscription-Key: {<your-key>}
```

The body of your request is the response from the previous step.

```json
{
  "targetResourceId": "/subscriptions/targetSub/resourceGroups/targetRG/providers/Microsoft.CognitiveServices/accounts/targetService",
  "targetResourceRegion": "targetResourceRegion",
  "targetClassifierId": "targetClassifier",
  "targetClassifierLocation": "https://targetEndpoint.cognitiveservices.azure.com/documentintelligence/documentClassifiers/targetClassifier",
  "accessToken": "accessToken",
  "expirationDateTime": "timestamp"
}
```

:::moniker-end

## Model response

Analyze an input file with the document classification model.

:::moniker range="doc-intel-4.0.0"

```json
https://{endpoint}/documentintelligence/documentClassifiers/{classifier}:analyze?api-version=2024-02-29-preview
```

Starting with the `2024-07-31-preview` API, you can specify pages to analyze from the input document using the `pages` query parameter in the request.

:::moniker-end

:::moniker range="doc-intel-3.1.0"

```json
https://{service-endpoint}/formrecognizer/documentClassifiers/{classifier}:analyze?api-version=2023-07-31
```

:::moniker-end

The response contains the identified documents with the associated page ranges in the documents section of the response.

```json
{
  ...

    "documents": [
      {
        "docType": "formA",
        "boundingRegions": [
          { "pageNumber": 1, "polygon": [...] },
          { "pageNumber": 2, "polygon": [...] }
        ],
        "confidence": 0.97,
        "spans": []
      },
      {
        "docType": "formB",
        "boundingRegions": [
          { "pageNumber": 3, "polygon": [...] }
        ],
        "confidence": 0.97,
        "spans": []
      }, ...
    ]
  }

```

## Next steps

Learn to create custom classification models:

> [!div class="nextstepaction"]
> [**Build a custom classification model**](../how-to-guides/build-a-custom-classifier.md)
> [**Custom models overview**](../train/custom-model.md)
