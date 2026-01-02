---
title: Transparency Note and use cases for Image Analysis
titleSuffix: Foundry Tools
description: This article explains Image Analysis Responsible AI basics, use cases, and terms.
ai-usage: ai-assisted
author: PatrickFarley
ms.author: pafarley
manager: nitinme
ms.service: azure-ai-vision
ms.topic: article
ms.date: 10/15/2025
---

# Transparency note: Image Analysis

[!INCLUDE [non-english-translation](../includes/non-english-translation.md)]

## What is a Transparency Note?

An AI system includes not only the technology, but also the people who use it, the people who will be affected by it, and the environment in which it's deployed. Creating a system that is fit for its intended purpose requires an understanding of how the technology works, what its capabilities and limitations are, and how to achieve the best performance. Microsoft's Transparency Notes are intended to help you understand how our AI technology works, the choices system owners can make that influence system performance and behavior, and the importance of thinking about the whole system, including the technology, the people, and the environment. You can use Transparency Notes when developing or deploying your own system, or share them with the people who will use or be affected by your system.

Microsoft's Transparency Notes are part of a broader effort at Microsoft to put our AI Principles into practice. To find out more, see the [Microsoft AI principles](https://www.microsoft.com/ai/responsible-ai).

## The basics of Image Analysis

### Introduction

Organizations are building solutions to process media assets such as digital files and images and extract actionable insights. These insights include visual features from images such as objects, people, and image descriptions that can be used to power knowledge mining, business process automation, and accessibility of content for everyone.

Accessible through Foundry Tools, Image Analysis APIs offer pretrained machine learning models to assign labels to images and classify them into thousands of predefined categories. The APIs extract many visual features from images, including objects, people, adult content, and auto-generated image captions. Using the Customization feature, customers can quickly train vision models using their own data and defining their own categories.

### Key terms

| **Term** | **Definition** |
| --- | --- |
| **prebuilt models** | Models powering features that Image Analysis offers to customers. These models do not require additional training. |
| **Base model** | Base models are a combination of model architecture and training data used to tune that architecture for a specific type of task (for example, image classification or object detection). Base models are built by Microsoft and are used as a starting point for the transfer learning process for various domains such as General, Food, Landmarks, Retail, Logos, and Products on Shelves. |
| **Model training** | This refers to the process of training a model based on customer provided labeled images when using the model customization feature. |
| **Few-shot learning** | In contrast to traditional methods of training machine learning models, where large amounts of training data are typically used, few shot learning uses a small amount of training data to train a model to learn the underlying pattern in order to recognize and classify new data provided by the customer when using the customization feature. |
| **Transfer learning** | The use of customer provided training data in the model customization feature to retrain a base model to address the specific problem the customer is trying to solve. The training data might be a combination of the classes they want to recognize or detect, and the type of images. |
| **Class** | A trained model has a set of classes it will assign when analyzing an input image. When you're building a custom image classification model through model customization, you define the set of classes you want the model to output and provide labeled training data for each of the classes. |
| **Class accuracy pair** | The class accuracy pair is a set of two values consisting of the name of the class and a float value for the confidence score associated with the class detection. For example, a class might be a type of fruit like a pineapple or pear represented in the image set. The class-accuracy pair is the specific class and the confidence score that the class is present in the image (for example, Pineapple: 93.53%). |
| **Image classification** | This feature takes an image as an input, and outputs a set of class accuracy pairs that are image level properties (they don't specify a location within the image). For example, a pair might be fruit versus non-fruit, where most of the image is occupied by the respective class. |
| **Object detection** | This feature takes an image as an input, and outputs a set of class accuracy pairs that also includes the bounding box coordinates for where in the image those classes were detected. For example, the model might detect the bounding box coordinates for where a vehicle is found in the image. |
| **Bounding box** | A set of four numerical values representing the x,y pixel coordinates of the top left corner of the detected object relative to the top left corner of the image, the width of the detected object. |
| **Confidence** | An Image Analysis operation returns confidence values in the range of 0 to 1 for all extracted output. The confidence value represents the estimate of the likelihood of a tag.|
| **Florence** | Florence is the name of a new foundation AI model, part of an Azure Vision in Foundry Tools initiative, trained with billions of text-image pairs that powers many of the quality improvements in the v4.0 release of the Vision service. It has the ability to recognize millions of object categories out of the box, and enables faster, lower-cost customization to recognize specific patterns with fewer training images in the model customization service. |
| **Planogram** | A planogram is a document or diagram that describes the placement of products on shelves or displays in a retail store. It's used to help retailers and manufacturers optimize the placement of products to increase sales. In product recognition scenarios, the planogram is represented as a JSON document.|

## Capabilities

### Features

> [!IMPORTANT]
> Except for celebrity recognition, Image Analysis does not identify or verify individual people. It does not perform facial recognition, predict or classify facial attributes such as age or gender, or create facial templates when faces are detected. Any recognition of an individual is the result of your labeling, not from facial recognition capabilities or the creation of facial templates. Celebrity recognition is a limited-access feature available only to approved customers. When celebrity recognition is in use, Image Analysis calls Face API to generate facial templates for detected faces and compare them with stored templates for celebrities (see Celebrity, landmark, and brand recognition, below).
<!-- Consolidated repeated warnings about facial recognition, age, and gender into a single targeted statement -->

You can use Image Analysis to process images:

- [**Tag visual features**](/azure/ai-services/computer-vision/concept-tagging-images): From a set of thousands of recognizable objects, living things, scenery, and actions, you can identify and tag visual features in an image. When the tags are ambiguous or the identity of the contents aren't common knowledge, the API response provides hints to clarify the context of the tag. Tagging isn't limited to the main subject of the image, such as a person in the foreground. Tagging can also include the setting (indoors or outdoors), furniture, tools, plants, animals, accessories, and gadgets.
- [**Detect objects**](/azure/ai-services/computer-vision/concept-object-detection): Object detection is similar to tagging, but the API returns the bounding box coordinates for each tag applied. For example, if an image contains a dog, a cat, and a person, the operation lists each object and its coordinates in the image. You can use this functionality to process relationships between the objects in an image. Object detection also lets you know when there are multiple instances of the same tag in an image.
- **[Generate descriptive captions](/azure/ai-services/computer-vision/concept-describing-images):** The image captioning algorithm uses celebrity recognition and landmark recognition models to generate more descriptive captions when celebrities or landmarks are present in the image. Celebrity recognition is only available to approved customers, apply [here](https://aka.ms/facerecognition) if you would like to use celebrity recognition.

   > [!NOTE]
   > "Caption" replaces "Describe" in V4.0 as the improved image captioning feature rich with details and semantic understanding. Dense Captions provides more detail by generating one sentence descriptions of up to 10 regions of the image in addition to describing the whole image. Dense Captions also returns bounding box coordinates of the described image regions.

- [**Moderate content in images**](/azure/ai-services/computer-vision/concept-detecting-adult-content): You can use Image Analysis to detect adult, racy, and gory content in an image and obtain confidence scores for these classifications. You can set the threshold for flagging content as adult, racy, or gory on a sliding scale to accommodate your preferences.
- [**Obtain an area of interest and smart crops**](/azure/ai-services/computer-vision/concept-generating-thumbnails?tabs=3-2): You can analyze the contents of an image to return the coordinates of the image's most important region or get AI-suggested crops of the image for different aspect ratios. Face detection is used to help determine important regions in the image. The detection doesn't involve distinguishing one face from another, predicting or classifying facial attributes, or creating a facial template.
- [**Extract text in images**](/azure/ai-services/computer-vision/concept-ocr): Image Analysis has optical character recognition (OCR) that you can use to detect printed or handwritten text in images and return the text and the text coordinates.
- [**Detect people and faces**](/azure/ai-services/computer-vision/concept-detecting-faces): You can use Azure Vision to detect faces and people in an image. The APIs return the rectangle coordinates for each detected face and person. Face verification and identification are offered by the [Azure AI Face service](/azure/ai-services/computer-vision/overview-identity).
- **[Celebrity, landmark, and brand recognition](/azure/ai-services/computer-vision/concept-detecting-domain-content)**: Use Image Analysis to identify commercial brands, popular landmarks, and celebrities in images or videos from a preset database of thousands of global logos, landmarks, and celebrities. Celebrity recognition is limited to approved customers.
- **[Customization](/azure/ai-services/computer-vision/concept-model-customization)**: Customization is a feature of Azure Vision that lets you build, deploy, and improve your own custom image identification system.
- **[Product understanding](/azure/ai-services/computer-vision/how-to/shelf-analyze)**: Use a specialized Image Analysis model to detect the presence of products on retail store shelves.
- **[Image stitching](/azure/ai-services/computer-vision/how-to/shelf-modify-images)**: Combine multiple images that partially overlap into a single large image.
- **[Image rectification](/azure/ai-services/computer-vision/how-to/shelf-modify-images)**: Undo the perspective distortion of an image.
- **[Planogram matching](/azure/ai-services/computer-vision/how-to/shelf-planogram)**: Compare product recognition results with a planogram document.
- [**Background Removal**](/azure/ai-services/computer-vision/concept-background-removal): Lets you remove the background of an image.
- [**Image Retrieval**](/azure/ai-services/computer-vision/how-to/image-retrieval): Image Retrieval allows users to search images using natural language queries.
- [**Video summary and frame locator**](https://aka.ms/visionstudio): Search and interact with video content. Currently available only in Vision Studio

### Use cases

#### Intended uses

Here are some examples of when you might use Image Analysis:

- **Image discoverability**: Images that are uploaded to an organization's internal share space and social media platforms contain rich information and metadata.
- **Content processing automation**: You can use Image Analysis to automate tasks such as detecting visual content in images.
- **Image content moderation**: Automatically flag inappropriate content in images.
- **Domain-specific identification**: Identify landmarks or brand logos in images.
- **Accessibility support**: Build solutions that assist people who are blind or have low vision by detecting and describing image content, with options for gender-specific or gender-neutral descriptions.
- **Image filtering for privacy purposes**: Detect faces and people in images to identify potentially sensitive content.
- **Retail inventory management**: Analyze photos of retail shelves and compare results to a planogram.

#### Considerations when choosing other use cases

- **Apply human oversight for award or denial of benefits**: Combine automation with human oversight.
- **Not suitable for identifying individuals or classifying personal attributes**: Azure Vision is not designed for face identification or verification, biometric identification, or for classifying personal attributes such as age or gender. Any identification of an individual occurs only through customer-provided labels. [Use Azure AI Face.](/azure/ai-services/computer-vision/overview-identity)
<!-- Consolidated multiple overlapping “not suitable” warnings into a single targeted statement -->
- **Account for additional measures for domain-specific recognition**: Prebuilt recognition is trained on a finite set of entities.
- **Do not use Azure Vision for medical diagnosis**: Azure Vision is not intended for medical or clinical use.
- [!INCLUDE [regulatory-considerations](../includes/regulatory-considerations.md)]

## System performance and Limitations for Image Analysis

### Accuracy for Image Analysis

[Content unchanged]

## Customization in Image Analysis

[Content unchanged until IMPORTANT block]

> [!IMPORTANT]
> Customization is not suitable for large-scale image sets with hundreds of classes, for generating human-readable image descriptions for accessibility, or for recognizing or identifying individuals. It does not support facial recognition or the creation of facial templates. Use Image Analysis for captioning and large-scale classification, and use [Azure AI Face](/azure/ai-services/computer-vision/overview-identity) for facial recognition scenarios.
<!-- Consolidated repeated “Customization not suitable for …” statements into a single targeted warning -->

[Remaining content unchanged]

## Learn more about responsible AI

- [Microsoft AI principles](https://www.microsoft.com/ai/responsible-ai)
- [Microsoft responsible AI resources](https://www.microsoft.com/ai/responsible-ai-resources)
- [Microsoft Azure Learning courses on responsible AI](/learn/paths/responsible-ai-business-principles/)

## Learn more about Image Analysis

- [Image Analysis overview](/azure/ai-services/computer-vision/overview-image-analysis?tabs=3-2)
- [Image Analysis quickstart](/azure/ai-services/computer-vision/quickstarts-sdk/image-analysis-client-library?tabs=visual-studio%2C3-2&pivots=programming-language-rest-api)
- [Image Analysis on Vision Studio](https://portal.vision.cognitive.azure.com/gallery/imageanalysis)

## Next steps

* [Responsible deployment of Image Analysis](/azure/ai-foundry/responsible-ai/computer-vision/image-analysis-guidance-for-integration)
* [Image Analysis Overview](/azure/ai-services/computer-vision/overview-image-analysis)
* [QuickStart your Image Analysis use case development](/azure/ai-services/computer-vision/quickstarts-sdk/image-analysis-client-library)
* [Data, privacy, and security for Image Analysis](/azure/ai-foundry/responsible-ai/computer-vision/image-analysis-data-privacy-security)