---
title: Custom text classification data formats
titleSuffix: Foundry Tools
description: Learn about the data formats accepted by custom text classification.
#services: cognitive-services
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: concept-article
ms.date: 12/15/2025
ms.author: lajanuar
ms.custom: language-service-custom-classification
---
# Accepted data formats

If you're trying to import your data into custom text classification, it has to follow a specific format. If you don't have data to import, you can [create your project](../how-to/create-project.md) and use Microsoft Foundry to [label your documents](../how-to/tag-data.md).

## Labels file format

Your Labels file should be in the `json` format to enable you to [import](../how-to/create-project.md#import-a-custom-text-classification-project-rest-api) your labels into a project.

# [Multi label classification](#tab/multi-classification)

```json
{
    "projectFileVersion": "2022-05-01",
    "stringIndexType": "Utf16CodeUnit",
    "metadata": {
        "projectKind": "CustomMultiLabelClassification",
        "storageInputContainerName": "{CONTAINER-NAME}",
        "projectName": "{PROJECT-NAME}",
        "multilingual": false,
        "description": "Project-description",
        "language": "en-us"
    },
    "assets": {
        "projectKind": "CustomMultiLabelClassification",
        "classes": [
            {
                "category": "Class1"
            },
            {
                "category": "Class2"
            }
        ],
        "documents": [
            {
                "location": "{DOCUMENT-NAME}",
                "language": "{LANGUAGE-CODE}",
                "dataset": "{DATASET}",
                "classes": [
                    {
                        "category": "Class1"
                    },
                    {
                        "category": "Class2"
                    }
                ]
            }
        ]
    }
}
```

|Key  |Placeholder  |Value  | Example |
|---------|---------|----------|--|
| multilingual | `true`| A boolean value that enables you to have documents in multiple languages in your dataset and when your model is deployed you can query the model in any supported language (not necessarily included in your training documents). See [language support](../language-support.md#multi-lingual-option) to learn more about multilingual support. | `true`|
|projectName|`{PROJECT-NAME}`|Project name|myproject|
| storageInputContainerName|`{CONTAINER-NAME}`|Container name|`mycontainer`|
| classes | [] | Array containing all the classes you have in the project.| [] |
| documents | [] | Array containing all the documents in your project and the classes labeled for this document. | [] |
| location | `{DOCUMENT-NAME}` |  The location of the documents in the storage container. Since all the documents are in the root of the container, this value should be the document name.|`doc1.txt`|
| dataset | `{DATASET}` |  The test set to which this file goes to when split before training. See [How to train a model](../how-to/train-model.md#data-splitting). Possible values for this field are `Train` and `Test`.      |`Train`|


# [Single label classification](#tab/single-classification)

```json
{
    
    "projectFileVersion": "2022-05-01",
    "stringIndexType": "Utf16CodeUnit",
    "metadata": {
        "projectKind": "CustomSingleLabelClassification",
        "storageInputContainerName": "{CONTAINER-NAME}",
        "settings": {},
        "projectName": "{PROJECT-NAME}",
        "multilingual": false,
        "description": "Project-description",
        "language": "en-us"
    },
    "assets": {
        "projectKind": "CustomSingleLabelClassification",
        "classes": [
            {
                "category": "Class1"
            },
            {
                "category": "Class2"
            }
        ],
        "documents": [
            {
                "location": "{DOCUMENT-NAME}",
                "language": "{LANGUAGE-CODE}",
                "dataset": "{DATASET}",
                "class": {
                    "category": "Class2"
                }
            },
            {
                "location": "{DOCUMENT-NAME}",
                "language": "{LANGUAGE-CODE}",
                "dataset": "{DATASET}",
                "class": {
                    "category": "Class1"
                }
            }
        ]
    }
}
```
|Key  |Placeholder  |Value  | Example |
|---------|---------|----------|--|
|projectName|`{PROJECT-NAME}`|Project name|myproject|
| storageInputContainerName|`{CONTAINER-NAME}`|Container name|`mycontainer`|
| multilingual | `true`| A boolean value that enables you to have documents in multiple languages in your dataset and when your model is deployed you can query the model in any supported language (not necessarily included in your training documents). See [language support](../language-support.md#multi-lingual-option) to learn more about multilingual support. | `true`|
| classes | [] | Array containing all the classes you have in the project.| [] |
| documents | [] | Array containing all the documents in your project and which class this document belongs to. | [] |
| location | `{DOCUMENT-NAME}` |  The location of the documents in the storage container. Since all the documents are in the root of the container, use the document name.|`doc1.txt`|
| dataset | `{DATASET}` |  The test set to which this file goes to when split before training. See [How to train a model](../how-to/train-model.md#data-splitting). Possible values for this field are `Train` and `Test`.      |`Train`|


---

## Next steps

* You can import your labeled data into your project directly. See [How to create a project](../how-to/create-project.md#import-a-custom-text-classification-project-rest-api) to learn more about importing projects.
* See the [how-to article](../how-to/tag-data.md) more information about labeling your data. When you're done labeling your data, you can [train your model](../how-to/train-model.md).  
