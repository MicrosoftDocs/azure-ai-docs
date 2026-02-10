---
title: "Custom categories in Azure AI Content Safety (preview)"
titleSuffix: Azure AI services
description: Learn about custom content categories and the different ways you can use Azure AI Content Safety to handle them on your platform.
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-content-safety
ms.custom: build-2024
ms.topic: concept-article
ms.date: 09/02/2025
ms.author: pafarley
---

# Custom categories (preview)

Azure AI Content Safety lets you create and manage your own content categories for enhanced moderation and filtering that matches your specific policies or use cases.

## Types of customization

You can define and use custom categories through multiple methods. This section details and compares these methods.

| API        | Functionality   |
| :--------- | :------------ |
| [Custom categories (standard) API](#custom-categories-standard-api) | Use a customizable machine learning model to create, get, query, and delete a customized category. Or, list all your customized categories for further annotation tasks. |
| [Custom categories (rapid) API](#custom-categories-rapid-api) | Use a large language model (LLM) to quickly learn specific content patterns in emerging content incidents. |

### Custom categories (standard) API

The Custom categories (standard) API enables you to define categories specific to your needs, provide sample data, train a custom machine learning model, and use it to classify new content according to the learned categories. 

This API provides the standard workflow for customization with machine learning models. Depending on the training data quality, it can reach very good performance levels, but it can take up to several hours to train the model.

This implementation works on text content, not image content.

### Custom categories (rapid) API

The Custom categories (rapid) API is quicker and more flexible than the standard method. Use it to identify, analyze, contain, eradicate, and recover from cyber incidents that involve inappropriate or harmful content on online platforms. 

An incident might involve a set of emerging content patterns (text, image, or other modalities) that violate Microsoft community guidelines or the customers' own policies and expectations. You need to mitigate these incidents quickly and accurately to avoid potential live site issues or harm to users and communities. 

This implementation works on both text content and image content.

> [!TIP]
> Another way to deal with emerging content incidents is to use [Blocklists](/azure/ai-services/content-safety/how-to/use-blocklist), but that option only allows exact text matching and no image matching. The Custom categories (rapid) API offers the following advanced capabilities:
> - semantic text matching using embedding search with a lightweight classifier
> - image matching with a lightweight object-tracking model and embedding search


## How it works

### [Custom categories (standard) API](#tab/standard)

The Azure AI Content Safety custom categories feature uses a multistep process for creating, training, and using custom content classification models. Here's the workflow:

### Step 1: Definition and setup
 
When you define a custom category, you need to teach the AI what type of content you want to identify. This step involves providing a clear **category name** and a detailed **definition** that encapsulates the content's characteristics.

Then, you collect a balanced dataset with **positive** and (optionally) **negative** examples to help the AI learn the nuances of your category. This data should represent the variety of content that the model encounters in a real-world scenario.

### Step 2: Model training
 
After you prepare your dataset and define categories, the Azure AI Content Safety service trains a new machine learning model. This model uses your definitions and uploaded dataset to perform data augmentation by using a large language model. As a result, the training dataset is larger and higher quality. During training, the AI model analyzes the data and learns to differentiate between content that aligns with the specified category and content that doesn't.

### Step 3: Model evaluation
 
After training, evaluate the model to ensure it meets your accuracy requirements. Test the model with new content that it didn't receive during training. The evaluation phase helps you identify any potential adjustments you need to make before deploying the model into a production environment.

### Step 4: Model usage

Use the **analyzeCustomCategory** API to analyze text content and determine whether it matches the custom category you defined. The service returns a Boolean indicating whether the content aligns with the specified category.

#### [Custom categories (rapid) API](#tab/rapid)

To use the custom categories (rapid) API, first create an **incident** object with a text description. Then, upload any number of image or text samples to the incident. The LLM on the backend uses these samples to evaluate future input content. No training step is needed.

You can include your defined incident in a regular text analysis or image analysis request. The service indicates whether the submitted content is an instance of your incident. The service can still do other content moderation tasks in the same API call.

---

## Limitations

### Language availability

The Custom categories APIs support all languages that Content Safety text moderation supports. See [Language support](/azure/ai-services/content-safety/language-support).

### Input limitations

#### [Custom categories (standard) API](#tab/standard)


See the following table for the input limitations of the custom categories (standard) API:

| Object           | Limitation   |
| ---------------- | ------------ |
| Supported languages | English only |
|  Number of categories per user     |         3     |
|  Number of versions per category   |        3      |
|  Number of concurrent builds (processes) per category      |       1       |
|  Inference operations per second           |    5         |
|  Number of samples in a category version          |        Positive samples(required): minimum 50, maximum 5K<br>In total (both negative and positive samples): 10K<br>No duplicate samples allowed.      |
| Sample file size       |     maximum 128000 bytes         |
| Length of a text sample           |          maximum 125K characters   |
| Length of a category definition          |       maximum 1000 chars     |
|Length of a category name           |         maximum 128 characters    |
|Length of a blob url       |          maximum 500 characters    |

#### [Custom categories (rapid) API](#tab/rapid)

See the following table for the input limitations of the custom categories (rapid) API:

| Object     | Limitation      |
| :------------ | :----------- |
| Maximum length of an incident name | 100 characters | 
| Maximum number of text/image samples per incident | 1,000 |
| Maximum size of each sample | Text: 500 characters<br>Image: 4 MB  |
| Maximum number of text or image incidents per resource| 100 |  
| Supported Image formats | BMP, GIF, JPEG, PNG, TIF, WEBP |

---

### Region availability

To use these APIs, you must create your Azure AI Content Safety resource in one of the supported regions. For more information, see [Region availability](../overview.md#region-availability).


## Next step

Follow a how-to guide to use the Azure AI Content Safety APIs to create custom categories.

* [Use custom category (standard) API](../how-to/custom-categories.md)
* [Use the custom categories (rapid) API](../how-to/custom-categories-rapid.md)



