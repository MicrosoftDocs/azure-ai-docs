---
title: Azure AI Content Understanding field and content extraction
titleSuffix: Azure AI services
description: Learn about Content Understanding content extraction capabilities
author: laujan
ms.author: lajanuar
manager: nitinme
ms.service: azure
ms.topic: conceptual
ms.date: 11/19/2024
---

# Azure AI Content Understanding content extraction

The Content Understanding service can process and integrate multiple data modalities simultaneously Data modalities include mages, audio, video, and text.

## Field extraction and data types

***Content Understanding supports the following field data types:***

* **String**. Plain Text
* **Date**. Normalized to ISO 8601 (YYYY-MM-DD) format.
* **Time**. Normalized to ISO 8601 (hh:mm:ss) format.
* **Number**. Floating point number, normalized to double-precision floating point.
* **Integer**. Normalized to 64*bit signed integer.
* **Boolean**. Value normalized to `true` or `false`.
* **Array**. Data structure storing multiple items of the same type.
* **Object**. Key-value variable collection potentially of different types.

***Content Understanding supports the following field operations:***

| Operation | Description | FieldType support |
| --- | --- | --- |
| Extract | Direct extraction of field value from document content. | String, Date, Time, Number, Integer, StaticTable, DynamicTable |
| Classify | Classify parent field content (or document if top-level). | String |
| Generate | Generate field value from parent field content. | String|

### Field support for scenarios

| Modality | Field Kind supported for Ignite |
| --- | --- |
| Text | Generate |
| Document | Extract |
| Image | Generate, Classify |
| Conversation | Generate, Classify |
| ConversationAnalysis | Generate, Classify |
| CallCenterAnalysis | Generate, Classify |
| Scene | Generate, Classify |
| SceneAnalysis | Generate, Classify |


## Supported input and formats

|Content modality|File extension|
|----------------|--------------|
|Text document|.txt, .md|
|Visual document|.pdf, .tiff, .jpeg|
|Markup Document|.html, .docx|
|Image|.jpeg, .gif, .tiff|
|Audio|.wav|
|Video|.mp4|
|Structured|.json, .csv|