---
title: What's new in Azure Vision in Foundry Tools?
titleSuffix: Foundry Tools
description: Stay up to date on recent releases and updates to Azure Vision in Foundry Tools.
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-vision
ms.custom:
  - build-2023
  - ignite-2023
ms.topic: whats-new
ms.date: 09/26/2025
ms.author: pafarley
---

# What's new in Azure Vision in Foundry Tools

Learn what's new in Azure Vision. Check this page to stay up to date with new features, enhancements, fixes, and documentation updates. 

## August 2025


### Image Analysis 4.0 Preview API deprecation

On March 31, 2025, the Image Analysis 4.0 Preview APIs will be retired. Before that date, you need to migrate your Azure Image Analysis workloads to the [Image Analysis 4.0 GA ](/rest/api/computervision/operation-groups)API.

We encourage you to make the transition sooner to gain access to improvements such as multimodal embedding, synchronous OCR, people detection, image tagging, smart cropping, caption, dense caption, and image object detection.
These Image Analysis 4.0 preview APIs will be retired on March 31, 2025:
- `2022-07-31-preview`
- `2022-10-12-preview`
- `2023-02-01-preview`
- `2023-04-01-preview`
- `2023-07-01-preview`
- `v4.0-preview.1`

The following features will no longer be available upon retirement of the preview API versions, and they are removed from the Studio experience as of January 10, 2025:
- Model customization
- Background removal
- Product recognition

To maintain a smooth operation of your models, transition to [Azure AI Custom Vision](/azure/ai-services/Custom-Vision-Service/overview), which is now generally available. Custom Vision offers similar functionality to these retiring features.



## February 2024

#### Multimodal embeddings GA: new multi-language model

The Multimodal embeddings API has been updated and is now generally available. The new `2024-02-01` API includes a new model that supports text search in 102 languages. The original English-only model is still available, but it can't be combined with the new model in the same search index. If you vectorized text and images using the English-only model, these vectors aren't compatible with multi-lingual text and image vectors.


See the [language support](/azure/ai-services/computer-vision/language-support#multimodal-embeddings) page for the list of supported languages.

## January 2024

### New Image Analysis SDK 1.0.0-beta.1 (breaking changes)

The Image Analysis SDK was rewritten in version 1.0.0-beta.1 to better align with other Azure SDKs. All APIs have changed. See the updated [quickstarts](/azure/ai-services/computer-vision/quickstarts-sdk/image-analysis-client-library-40), [samples](/azure/ai-services/computer-vision/sdk/overview-sdk#github-samples) and [how-to-guides](/azure/ai-services/computer-vision/how-to/call-analyze-image-40) for information on how to use the new SDK.

Major changes:
- The SDK now calls the generally available [Computer Vision REST API (2023-10-01)](/rest/api/computervision/operation-groups), instead of the preview [Computer Vision REST API (2023-04-01-preview)](/rest/api/computervision/operation-groups).
- Support for JavaScript was added.
- C++ is no longer supported.
- Image Analysis with a custom model, and Image Segmentation (background removal) are no longer supported in the SDK, because the [Computer Vision REST API (2023-10-01)](/rest/api/computervision/operation-groups) doesn't yet support them. To use either feature, call the [Computer Vision REST API (2023-04-01-preview)](/rest/api/computervision/operation-groups) directly (using the `Analyze` and `Segment` operations respectively).

## November 2023

### Analyze Image 4.0 GA

The Analyze Image 4.0 REST API is now in General Availability. Follow the [Analyze Image 4.0 quickstart](./quickstarts-sdk/image-analysis-client-library-40.md) to get started.

The other features of Image Analysis, such as model customization, background removal, and multimodal embeddings, remain in public preview. 


## September 2023

### Deprecation of outdated Computer Vision API versions

Computer Vision API versions 1.0, 2.0, 3.0, and 3.1 will be retired on September 13, 2026. Developers won’t be able to make API calls to these APIs after that date.
We recommend that all affected customers migrate their workloads to the generally available Computer Vision 3.2 API by following this [QuickStart](/azure/ai-services/computer-vision/quickstarts-sdk/image-analysis-client-library?tabs=linux%2Cvisual-studio&pivots=programming-language-rest-api) at their earliest convenience. Customers should also consider migrating to [Image Analysis 4.0 API (preview)](/azure/ai-services/computer-vision/quickstarts-sdk/image-analysis-client-library-40?tabs=visual-studio%2Clinux&pivots=programming-language-python), which has our latest and greatest Image Analysis capabilities. 

Visit our [Q&A](/answers/tags/127/azure-computer-vision) for any questions.

## May 2023

### Image Analysis 4.0 Product Recognition (public preview)

The Product Recognition APIs let you analyze photos of shelves in a retail store. You can detect the presence and absence of products and get their bounding box coordinates. Use it in combination with model customization to train a model to identify your specific products. You can also compare Product Recognition results to your store's planogram document. [Product Recognition](./concept-shelf-analysis.md).



## March 2023

### Azure Vision Image Analysis 4.0 SDK public preview

The [Florence foundation model](https://www.microsoft.com/en-us/research/project/projectflorence/) is now integrated into Azure Vision. The improved Vision services enable developers to create market-ready, responsible Azure Vision applications across various industries. Customers can now seamlessly digitize, analyze, and connect their data to natural language interactions, unlocking powerful insights from their image and video content to support accessibility, drive acquisition through SEO, protect users from harmful content, enhance security, and improve incident response times. For more information, see [Announcing Microsoft's Florence foundation model](https://aka.ms/florencemodel).

### Image Analysis 4.0 SDK (public preview)

Image Analysis 4.0 is now available through client library SDKs in C#, C++, and Python. This update also includes the Florence-powered image captioning and dense captioning at human parity performance.

### Image Analysis V4.0 Captioning and Dense Captioning (public preview):

"Caption" replaces "Describe" in V4.0 as the improved image captioning feature rich with details and semantic understanding. Dense Captions provides more detail by generating one-sentence descriptions of up to 10 regions of the image in addition to describing the whole image. Dense Captions also returns bounding box coordinates of the described image regions. There's also a new gender-neutral parameter to allow customers to choose whether to enable probabilistic gender inference for alt-text and Seeing AI applications. Automatically deliver rich captions, accessible alt-text, SEO optimization, and intelligent photo curation to support digital content. [Image captions](./concept-describe-images-40.md).

### Video summary and frame locator (public preview): 
Search and interact with video content in the same intuitive way you think and write. Locate relevant content without the need for extra metadata. Available only in [Vision Studio](https://aka.ms/VisionStudio).


### Image Analysis 4.0 model customization (public preview)

You can now create and train your own [custom image classification and object detection models](./concept-model-customization.md), using Vision Studio or the v4.0 REST APIs.

### Multimodal embeddings APIs (public preview)

The [Multimodal embeddings APIs](./how-to/image-retrieval.md), part of the Image Analysis 4.0 API, enable the _vectorization_ of images and text queries. They let you convert images and text to coordinates in a multi-dimensional vector space. You can now search with natural language and find relevant images using vector similarity search.

### Background removal APIs (public preview)

As part of the Image Analysis 4.0 API, the [Background removal API](./concept-background-removal.md) lets you remove the background of an image. This operation can either output an image of the detected foreground object with a transparent background, or a grayscale alpha matte image showing the opacity of the detected foreground object.

### Azure Vision 3.0 & 3.1 previews deprecation

The preview versions of Azure Vision 3.0 and 3.1 APIs are scheduled to be retired on September 30, 2023. Customers won't be able to make any calls to these APIs past this date. Customers are encouraged to migrate their workloads to the generally available (GA) 3.2 API instead. Mind the following changes when migrating from the preview versions to the 3.2 API:
- The [Analyze Image](/rest/api/computervision/analyze-image) and [Read](/rest/api/computervision/recognize-printed-text) API calls take an optional _model-version_ parameter that you can use to specify which AI model to use. By default, they use the latest model.
- The [Analyze Image](/rest/api/computervision/analyze-image) and [Read](/rest/api/computervision/recognize-printed-text) API calls also return a `model-version` field in successful API responses. This field reports which model was used.
- Azure Vision 3.2 API uses a different error-reporting format. See the [API reference documentation](/rest/api/computervision/operation-groups) to learn how to adjust any error-handling code.

## October 2022

### Azure Vision Image Analysis 4.0 (public preview)

Image Analysis 4.0 has been released in public preview. The new API includes image captioning, image tagging, object detection, smart crops, people detection, and Read OCR functionality, all available through one Analyze Image operation. The OCR is optimized for general non-document images in a performance-enhanced synchronous API that makes it easier to embed OCR-powered experiences in your workflows.

## September 2022

### Azure Vision 3.0/3.1 Read previews deprecation

The preview versions of Azure Vision 3.0 and 3.1 Read API are scheduled to be retired on January 31, 2023. Customers are encouraged to refer to the [How-To](./how-to/call-read-api.md) and [QuickStarts](./quickstarts-sdk/client-library.md?tabs=visual-studio&pivots=programming-language-csharp) to get started with the generally available (GA) version of the Read API instead. The latest GA versions provide the following benefits:
* 2022 latest generally available OCR model
* Significant expansion of OCR language coverage including support for handwritten text
* Improved OCR quality 

## June 2022

### Vision Studio launch

Vision Studio is UI tool that lets you explore, build, and integrate features from Azure Vision into your applications.

Vision Studio provides you with a platform to try several service features, and see what they return in a visual manner. Using the Studio, you can get started without needing to write code, and then use the available client libraries and REST APIs in your application.


### Azure Vision 3.2-preview deprecation

The preview versions of the 3.2 API are scheduled to be retired in December of 2022. Customers are encouraged to use the generally available (GA) version of the API instead. Mind the following changes when migrating from the 3.2-preview versions:
1. The [Analyze Image](/rest/api/computervision/analyze-image) and [Read](/rest/api/computervision/recognize-printed-text) API calls now take an optional _model-version_ parameter that you can use to specify which AI model to use. By default, they use the latest model.
1. The [Analyze Image](/rest/api/computervision/analyze-image) and [Read](/rest/api/computervision/recognize-printed-text) API calls also return a `model-version` field in successful API responses. This field reports which model was used.
1. Image Analysis APIs now use a different error-reporting format. See the [API reference documentation](/rest/api/computervision/analyze-image) to learn how to adjust any error-handling code.

## May 2022

### OCR (Read) API model is generally available (GA)

Azure Vision's [OCR (Read) API](overview-ocr.md) latest model with [164 supported languages](language-support.md) is now generally available as a cloud service and container.

* OCR support for print text expands to 164 languages including Russian, Arabic, Hindi and other languages using Cyrillic, Arabic, and Devanagari scripts.
* OCR support for handwritten text expands to 9 languages with English, Chinese Simplified, French, German, Italian, Japanese, Korean, Portuguese, and Spanish.
* Enhanced support for single characters, handwritten dates, amounts, names, other entities commonly found in receipts and invoices.
* Improved processing of digital PDF documents.
* Input file size limit increased 10x to 500 MB.
* Performance and latency improvements.
* Available as [cloud service](overview-ocr.md) and [Docker container](computer-vision-how-to-install-containers.md).

See the [OCR how-to guide](how-to/call-read-api.md) to learn how to use the GA model.

> [!div class="nextstepaction"]
> [Get Started with the Read API](./quickstarts-sdk/client-library.md)

## February 2022

### OCR (Read) API Public Preview supports 164 languages

Azure Vision's [OCR (Read) API](overview-ocr.md) expands [supported languages](language-support.md) to 164 with its latest preview:

* OCR support for print text expands to 42 new languages including Arabic, Hindi, and other languages using Arabic and Devanagari scripts.
* OCR support for handwritten text expands to Japanese and Korean in addition to English, Chinese Simplified, French, German, Italian, Portuguese, and Spanish.
* Enhancements including better support for extracting handwritten dates, amounts, names, and single character boxes.
* General performance and AI quality improvements

See the [OCR how-to guide](how-to/call-read-api.md) to learn how to use the new preview features.

> [!div class="nextstepaction"]
> [Get Started with the Read API](./quickstarts-sdk/client-library.md)


## September 2021

### OCR (Read) API Public Preview supports 122 languages

Azure Vision's [OCR (Read) API](overview-ocr.md) expands [supported languages](language-support.md) to 122 with its latest preview:

* OCR support for print text in 49 new languages including Russian, Bulgarian, and other Cyrillic and more Latin languages.
* OCR support for handwritten text in 6 new languages that include English, Chinese Simplified, French, German, Italian, Portuguese, and Spanish.
* Enhancements for processing digital PDFs and Machine Readable Zone (MRZ) text in identity documents.
* General performance and AI quality improvements

See the [OCR how-to guide](how-to/call-read-api.md) to learn how to use the new preview features.

> [!div class="nextstepaction"]
> [Get Started with the Read API](./quickstarts-sdk/client-library.md)

## August 2021

### Image tagging language expansion

The [latest version (v3.2)](/rest/api/computervision/operation-groups) of the Image tagger now supports tags in 50 languages. See the [language support](language-support.md) page for more information.

## July 2021

### New HeadPose and Landmarks improvements for Detection_03

* The Detection_03 model has been updated to support facial landmarks.
* The landmarks feature in Detection_03 is much more precise, especially in the eyeball landmarks, which are crucial for gaze tracking.

## May 2021

### Spatial Analysis container update

A new version of the [Spatial Analysis container](spatial-analysis-container.md) has been released with a new feature set. This Docker container lets you analyze real-time streaming video to understand spatial relationships between people and their movement through physical environments.

* [Spatial Analysis operations](spatial-analysis-operations.md) can be now configured to detect the orientation that a person is facing.
  * An orientation classifier can be enabled for the `personcrossingline` and `personcrossingpolygon` operations by configuring the `enable_orientation` parameter. It is set to off by default.

* [Spatial Analysis operations](spatial-analysis-operations.md) now also offers configuration to detect a person's speed while walking/running
  * Speed can be detected for the `personcrossingline` and `personcrossingpolygon` operations by turning on the `enable_speed` classifier, which is off by default. The output is reflected in the `speed`, `avgSpeed`, and `minSpeed` outputs.

## April 2021

### Azure Vision v3.2 GA

Azure Vision API v3.2 is now generally available with the following updates:

* Improved image tagging model: analyzes visual content and generates relevant tags based on objects, actions, and content displayed in the image. This model is available through the [Tag Image API](/rest/api/computervision/operation-groups). See the Image Analysis [how-to guide](./how-to/call-analyze-image.md) and [overview](./overview-image-analysis.md) to learn more.
* Updated content moderation model: detects presence of adult content and provides flags to filter images containing adult, racy, and gory visual content. This model is available through the [Analyze API](/rest/api/computervision/analyze-image). See the Image Analysis [how-to guide](./how-to/call-analyze-image.md) and [overview](./overview-image-analysis.md) to learn more.
* [OCR (Read) available for 73 languages](./language-support.md#optical-character-recognition-ocr) including Simplified and Traditional Chinese, Japanese, Korean, and Latin languages.
* [OCR (Read)](./overview-ocr.md) also available as a [Distroless container](./computer-vision-how-to-install-containers.md?tabs=version-3-2) for on-premises deployment.

> [!div class="nextstepaction"]
> [See Azure Vision v3.2 GA](/rest/api/computervision/recognize-printed-text)


## March 2021

### Azure Vision 3.2 Public Preview update

Azure Vision API v3.2 public preview has been updated. The preview release has all Azure Vision features along with updated Read and Analyze APIs.

> [!div class="nextstepaction"]
> [See Azure Vision v3.2 public preview 3](/rest/api/computervision/operation-groups)

## February 2021

### Read API v3.2 Public Preview with OCR support for 73 languages

Azure Vision Read API v3.2 public preview, available as cloud service and Docker container, includes these updates:

* [OCR for 73 languages](./language-support.md#optical-character-recognition-ocr) including Simplified and Traditional Chinese, Japanese, Korean, and Latin languages.
* Natural reading order for the text line output (Latin languages only)
* Handwriting style classification for text lines along with a confidence score (Latin languages only).
* Extract text only for selected pages for a multi-page document.
* Available as a [Distroless container](./computer-vision-how-to-install-containers.md?tabs=version-3-2) for on-premises deployment.

See the [Read API how-to guide](how-to/call-read-api.md) to learn more.

> [!div class="nextstepaction"]
> [Use the Read API v3.2 Public Preview](/rest/api/computervision/operation-groups)



## January 2021

### Spatial Analysis container update

A new version of the [Spatial Analysis container](spatial-analysis-container.md) has been released with a new feature set. This Docker container lets you analyze real-time streaming video to understand spatial relationships between people and their movement through physical environments.

* [Spatial Analysis operations](spatial-analysis-operations.md) can be now configured to detect if a person is wearing a protective face covering such as a mask.
  * A mask classifier can be enabled for the `personcount`, `personcrossingline` and `personcrossingpolygon` operations by configuring the `ENABLE_FACE_MASK_CLASSIFIER` parameter.
  * The attributes `face_mask` and `face_noMask` will be returned as metadata with confidence score for each person detected in the video stream
* The *personcrossingpolygon* operation has been extended to allow the calculation of the dwell time a person spends in a zone. You can set the `type` parameter in the Zone configuration for the operation to `zonedwelltime` and a new event of type *personZoneDwellTimeEvent* will include the `durationMs` field populated with the number of milliseconds that the person spent in the zone.
* **Breaking change**: The *personZoneEvent* event has been renamed to *personZoneEnterExitEvent*. This event is raised by the *personcrossingpolygon* operation when a person enters or exits the zone and provides directional info with the numbered side of the zone that was crossed.
* Video URL can be provided as "Private Parameter/obfuscated" in all operations. Obfuscation is optional now and it will only work if `KEY` and `IV` are provided as environment variables.
* Calibration is enabled by default for all operations. Set the `do_calibration: false` to disable it.
* Added support for auto recalibration (by default disabled) via the `enable_recalibration` parameter, please refer to [Spatial Analysis operations](./spatial-analysis-operations.md) for details
* Camera calibration parameters to the `DETECTOR_NODE_CONFIG`. Refer to [Spatial Analysis operations](./spatial-analysis-operations.md) for details.


## October 2020

### Azure Vision API v3.1 GA

Azure Vision API in General Availability has been upgraded to v3.1.

## September 2020

### Spatial Analysis container preview

The [Spatial Analysis container](spatial-analysis-container.md) is now in preview. The Spatial Analysis feature of Azure Vision lets you analyze real-time streaming video to understand spatial relationships between people and their movement through physical environments. Spatial Analysis is a Docker container you can use on-premises.

### Read API v3.1 Public Preview adds OCR for Japanese

Azure Vision Read API v3.1 public preview adds these capabilities:

* OCR for Japanese language
* For each text line, indicate whether the appearance is Handwriting or Print style, along with a confidence score (Latin languages only).
* For a multi-page document extract text only for selected pages or page range.

* This preview version of the Read API supports English, Dutch, French, German, Italian, Japanese, Portuguese, Simplified Chinese, and Spanish languages.

See the [Read API how-to guide](how-to/call-read-api.md) to learn more.

> [!div class="nextstepaction"]
> [Learn more about Read API v3.1 Public Preview 2](/rest/api/computervision/operation-groups)



## July 2020

### Read API v3.1 Public Preview with OCR for Simplified Chinese

The Azure Vision in Foundry Tools Read API v3.1 public preview adds support for Simplified Chinese.

* This preview version of the Read API supports English, Dutch, French, German, Italian, Portuguese, Simplified Chinese, and Spanish languages.

See the [Read API how-to guide](how-to/call-read-api.md) to learn more.

> [!div class="nextstepaction"]
> [Learn more about Read API v3.1 Public Preview 1](/rest/api/computervision/operation-groups)

## May 2020

Azure Vision API v3.0 entered General Availability, with updates to the Read API:

* Support for English, Dutch, French, German, Italian, Portuguese, and Spanish
* Improved accuracy
* Confidence score for each extracted word
* New output format

See the [OCR overview](overview-ocr.md) to learn more.



## March 2020

* TLS 1.2 is now enforced for all HTTP requests to this service. For more information, see [Foundry Tools security](../security-features.md).

## January 2020

### Read API 3.0 Public Preview

You now can use version 3.0 of the Read API to extract printed or handwritten text from images. Compared to earlier versions, 3.0 provides:

* Improved accuracy
* New output format
* Confidence score for each extracted word
* Support for both Spanish and English languages with the language parameter

Follow an [Extract text quickstart](https://github.com/Azure-Samples/cognitive-services-quickstart-code/blob/master/dotnet/ComputerVision/REST/CSharp-hand-text.md?tabs=version-3) to get starting using the 3.0 API.




## Foundry Tools updates

[Azure update announcements for Foundry Tools](https://azure.microsoft.com/updates/?product=cognitive-services)
