---
title: Labeling tips for custom models in the Document Intelligence Studio
titleSuffix: Azure AI services
description: Label tips and tricks for Document Intelligence Studio
author: laujan
manager: nitinme
ms.service: azure-ai-document-intelligence
ms.topic: conceptual
ms.date: 08/07/2024
ms.author: vikurpad
ms.custom:
  - references_regions
monikerRange: '>=doc-intel-3.0.0'
---


# Tips for building labeled datasets

::: moniker range="doc-intel-4.0.0"
**This content applies to:**![checkmark](../media/yes-icon.png) **v4.0 (preview)** | **Previous versions:** ![blue-checkmark](../media/blue-yes-icon.png) [**v3.1 (GA)**](?view=doc-intel-3.1.0&preserve-view=tru) ![blue-checkmark](../media/blue-yes-icon.png) [**v3.0 (GA)**](?view=doc-intel-3.0.0&preserve-view=tru)
::: moniker-end

::: moniker range="doc-intel-3.1.0"
**This content applies to:** ![checkmark](../media/yes-icon.png) **v3.1 (GA)** | **Latest version:** ![purple-checkmark](../media/purple-yes-icon.png) [**v4.0 (preview)**](?view=doc-intel-4.0.0&preserve-view=true) | **Previous versions:** ![blue-checkmark](../media/blue-yes-icon.png) [**v3.0**](?view=doc-intel-3.0.0&preserve-view=true)
::: moniker-end

::: moniker range="doc-intel-3.0.0"
**This content applies to:** ![checkmark](../media/yes-icon.png) **v3.0 (GA)** | **Latest versions:** ![purple-checkmark](../media/purple-yes-icon.png) [**v4.0 (preview)**](?view=doc-intel-4.0.0&preserve-view=true) ![purple-checkmark](../media/purple-yes-icon.png) [**v3.1**](?view=doc-intel-3.1.0&preserve-view=true)
::: moniker-end

> [!IMPORTANT]
> Best practices to generating labelled datasets only applies to custom template and custom neural models, for custom generative, refer to [Custom Generative](custom-generative-extraction.md)

This article highlights the best methods for labeling custom model datasets in the Document Intelligence Studio. Labeling documents can be time consuming when you have a large number of labels, long documents, or documents with varying structure. These tips should help you label documents more efficiently.

## Video: Custom labels best practices

* The following video is the second of two presentations intended to help you build custom models with higher accuracy (the first presentation explores [How to create a balanced data set](custom-labels.md#video-custom-label-tips-and-pointers)).

* We examine best practices for labeling your selected documents. With semantically relevant and consistent labeling, you should see an improvement in model performance.

> [!VIDEO https://www.microsoft.com/en-us/videoplayer/embed/RE5fZKB]

### Search

The Studio now includes a search box for instances when you know you need to find specific words to label, but just don't know where to locate them in the document. Simply search for the word or phrase and navigate to the specific section in the document to label the occurrence.

### Auto label tables

Tables can be challenging to label, when they have many rows or dense text. If the layout table extracts the result you need, you should just use that result and skip the labeling process. In instances where the layout table isn't exactly what you need, you can start with generating the table field from the values layout extracts. Start by selecting the table icon on the page and select on the auto label button. You can then edit the values as needed. Auto label currently only supports single page tables.

### Shift select

When labeling a large span of text, rather than mark each word in the span, hold down the shift key as you're selecting the words to speed up labeling and ensure you don't miss any words in the span of text.

### Region labeling

A second option for labeling larger spans of text is to use region labeling. When region labeling is used, the `OCR` results are populated in the value at training time. The difference between the shift select and region labeling is only in the visual feedback the shift labeling approach provides.

### Label overlapping fields

Overlapping fields are supported for fields and table cells. If you expect your analyze results to contain overlapping fields, you should add at least one sample to the training dataset with the specific field overlaps labeled. To label an overlapping field, use the region labeling feature to select the regions for each field. Both complete and partial overlaps are supported. Any single word in the document can only be labeled for two fields.

### Field subtypes

When creating a field, select the right subtype to minimize post processing, for instance select the ```dmy``` option for dates to extract the values in a ```dd-mm-yyyy``` format.

## Next steps

* Learn more about custom labeling:

  > [!div class="nextstepaction"]
  > [Custom labels](custom-labels.md)

* Learn more about custom template models:

  > [!div class="nextstepaction"]
  > [Custom models](custom-template.md)

