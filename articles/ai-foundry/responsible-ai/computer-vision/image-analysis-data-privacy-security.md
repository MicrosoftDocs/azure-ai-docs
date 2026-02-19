---
title: Data and privacy for Image Analysis
titleSuffix: Foundry Tools
description: This document details issues for data, privacy, and security for Image Analysis.
ai-usage: ai-assisted
author: PatrickFarley
ms.author: pafarley
manager: nitinme
ms.service: azure-ai-vision
ms.topic: concept-article
ms.date: 10/15/2025
---

# Data and privacy for Image Analysis 

[!INCLUDE [non-english-translation](../includes/non-english-translation.md)]


This article provides high-level details regarding how Azure Vision in Foundry Tools processes data provided by customers. Image Analysis was designed with compliance, privacy, and security in mind. As an important reminder, you're responsible for the implementation of this technology. It's your responsibility to comply with all applicable laws and regulations in your jurisdiction, including ensuring you have all necessary licenses, permissions or other third-party approvals required to transfer and process your content using Image Analysis.

Image Analysis is part of the Azure Cognitive Azure Vision in Foundry Tools. To learn more about the different offerings, see [Azure Vision Overview](/azure/ai-services/computer-vision/overview).


> [!NOTE]
> This article is provided for informational purposes only and not for the purpose of providing legal advice. We strongly recommend seeking specialist legal advice when implementing Image Analysis.


## What data does Image Analysis process? 

Image Analysis processes the following types of data: 
* **Input** - Images from local storage or online can be submitted to Image Analysis. These images can contain objects, scenes, and people, and results will be returned in real time. Image formats supported include PNG, JPEG, GIF, and BMP. For more information, refer to [data input](/azure/ai-services/computer-vision/overview-image-analysis#image-requirements). 

* **Configuration data** - Additional request parameters for languages, model version and user selected operations are processed when the customer submits an image to Image Analysis. 
* **Output** - The [response output](/azure/ai-services/computer-vision/overview-image-analysis), including the extracted features in JSON format, along with confidence scores.
    * Image tagging - Detected visual content tags are returned with the confidence scores. 

    * Object, brand, face, celebrity, and landmark detection - Identified objects, brands, faces, celebrities, and landmarks in the image are returned with detected bounding box coordinates and confidence scores. 

    * Describe image - The detected content tags, image caption, and confidence score are returned by the API.

    * Adult content detection - API returns three Boolean properties (isAdultContent, isRacyContent, and isGoryContent) in its JSON response, along with a confidence score for each category.


   > [!NOTE]
   > For face detection, Image Analysis returns coordinates of the bounding box locations of the faces only. Face detection does not involve distinguishing one face from another face, or classifying facial attributes, or creating a facial template (a unique set of numbers generated from an image that represents the distinctive features of a face). 

   > For celebrity recognition, Image Analysis returns all recognized celebrities along with the coordinates of the recognized faces. Celebrity Recognition covers a finite list (about one million faces) based on commonly requested data sources, such as IMDB, Wikipedia, and top LinkedIn influencers. 


## How does Image Analysis process data? 

The following diagram shows how your data is processed.   

:::image border type="content" source="./media/image-analysis/api-working.png" alt-text="Diagram that shows how the Microsoft Image Analysis API works.":::

### Authenticate (with subscription or API keys)

The most common way to authenticate access to the Image Analysis API is by using your single-service (Vision) or multi-service (Foundry Tools) API key. Each request to the service URL must include an authentication header. This header passes along an API key (or token if applicable), which is used to validate your subscription for a service or group of services. For more information, see [Authenticate requests to Foundry Tools](/azure/ai-services/authentication?tabs=powershell).

### Secure data in transit

All Foundry Tools endpoints, including the Image Analysis API URLs, use HTTPS URLs for encrypting data during transit. The client operating system needs to support Transport Layer Security (TLS) 1.3 for calling the end points. For more information, see [Transport Layer Security](/azure/ai-services/security-features?tabs=command-line%2Ccsharp#transport-layer-security-tls). The incoming data is processed in the same region where the Azure resource was created. 

### Return the processed image results

The Image Analysis processes images in real time. The API returns the analysis and extracted results in [JSON format](/azure/ai-services/computer-vision/overview-image-analysis).


## How is data retained and what controls are available? 

The images you submit to Image Analysis are processed in real time, and the input images and results are not retained or stored after processing.  

To learn more about privacy and security commitments, see the [Microsoft Trust Center](https://www.microsoft.com/trust-center).
For additional security best practices and information, visit [Foundry Tools security baseline](/azure/ai-services/security-features).


## Next steps

* [Characteristics and limitations](/azure/ai-foundry/responsible-ai/computer-vision/image-analysis-characteristics-and-limitations)
* [Responsible deployment of Image Analysis](/azure/ai-foundry/responsible-ai/computer-vision/image-analysis-guidance-for-integration)
* [Quickstart your Image Analysis use case development](/azure/ai-services/computer-vision/quickstarts-sdk/image-analysis-client-library)
* [Transparency Note](/azure/ai-foundry/responsible-ai/computer-vision/image-analysis-transparency-note)
