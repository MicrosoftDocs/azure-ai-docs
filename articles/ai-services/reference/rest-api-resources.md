---
title: Azure AI services REST API reference
titleSuffix: Azure AI services
description: Provides an overview of available Azure AI services REST APIs with links to reference documentation.
author: eric-urban
manager: nitinme
ms.service: azure-ai-services
ms.topic: reference
ms.date: 02/07/2025
ms.author: lajanuar
---

# Azure AI services REST API reference


This article provides an overview of available Azure AI services REST APIs with links to service and feature level reference documentation.

## Available Azure AI services

Select a service from the table to learn how it can help you meet your development goals.

## Supported services

| Service documentation | Description | Reference documentation |
| :--- | :--- | :--- |
| ![Azure AI Search icon](~/reusable-content/ce-skilling/azure/media/ai-services/search.svg) [Azure AI Search](/azure/search/) | Bring AI-powered cloud search to your mobile and web apps | [Azure AI Search API](/rest/api/searchservice) |
| ![Azure OpenAI Service icon](~/reusable-content/ce-skilling/azure/media/ai-services/azure-openai.svg) [Azure OpenAI](../openai/index.yml) | Perform a wide variety of natural language tasks | **Azure OpenAI APIs**<br>&bullet; [resource creation & deployment](/rest/api/cognitiveservices/accountmanagement/deployments/create-or-update) </br>&bullet; [completions & embeddings](../openai/reference.md)</br>&bullet; [fine-tuning](/rest/api/azureopenai/fine-tuning) |
| ![Bot service icon](~/reusable-content/ce-skilling/azure/media/ai-services/bot-services.svg) [Bot Service](/composer/) | Create bots and connect them across channels | [Bot Service API](/azure/bot-service/rest-api/bot-framework-rest-connector-api-reference?view=azure-bot-service-4.0&preserve-view=true) |
| ![Content Safety icon](~/reusable-content/ce-skilling/azure/media/ai-services/content-safety.svg) [Content Safety](../content-safety/index.yml) | An AI service that detects unwanted contents | [Content Safety API](/rest/api/contentsafety/operation-groups?view=rest-contentsafety-2024-09-01&preserve-view=true) |
| ![Custom Vision icon](~/reusable-content/ce-skilling/azure/media/ai-services/custom-vision.svg) [Custom Vision](../custom-vision-service/index.yml) | Customize image recognition for your business applications. |**Custom Vision APIs**<br>&bullet; [prediction](https://westus2.dev.cognitive.microsoft.com/docs/services/Custom_Vision_Prediction_3.1/operations/5eb37d24548b571998fde5f3)<br>&bullet; [training](https://westus2.dev.cognitive.microsoft.com/docs/services/Custom_Vision_Training_3.3/operations/5eb0bcc6548b571998fddebd)|
| ![Document Intelligence icon](~/reusable-content/ce-skilling/azure/media/ai-services/document-intelligence.svg) [Document Intelligence](../document-intelligence/index.yml) | Turn documents into intelligent data-driven solutions | [Document Intelligence API](/rest/api/aiservices/document-models?view=rest-aiservices-2023-07-31&preserve-view=true) |
| ![Face icon](~/reusable-content/ce-skilling/azure/media/ai-services/face.svg) [Face](../computer-vision/overview-identity.md) | Detect and identify people and emotions in images | [Face API](../computer-vision/identity-api-reference.md) |
| ![Language icon](~/reusable-content/ce-skilling/azure/media/ai-services/language.svg) [Language](../language-service/index.yml) | Build apps with industry-leading natural language understanding capabilities | [REST API](/rest/api/language/) |
| ![Speech icon](~/reusable-content/ce-skilling/azure/media/ai-services/speech.svg) [Speech](../speech-service/index.yml) | Speech to text, text to speech, translation, and speaker recognition | **Speech APIs**<br>&bullet; [speech to text](../speech-service/rest-speech-to-text.md)<br>&bullet; [text to speech](../speech-service/rest-text-to-speech.md) |
| ![Translator icon](~/reusable-content/ce-skilling/azure/media/ai-services/translator.svg) [Translator](../translator/index.yml) | Translate more than 100 in-use, at-risk, and endangered languages and dialects | **Translator APIs**<br>&bullet; [text translation](../translator/reference/rest-api-guide.md) <br>&bullet; [document translation](../translator/document-translation/reference/rest-api-guide.md)|
| ![Video Indexer icon](~/reusable-content/ce-skilling/azure/media/ai-services/video-indexer.svg) [Video Indexer](/azure/azure-video-indexer) | Extract actionable insights from your videos | [Video Indexer API](/rest/api/videoindexer/accounts?view=rest-videoindexer-2024-01-01&preserve-view=true) |
| ![Vision icon](~/reusable-content/ce-skilling/azure/media/ai-services/vision.svg) [Vision](../computer-vision/index.yml) | Analyze content in images and videos | [Vision API](/rest/api/computervision/operation-groups?view=rest-computervision-v4.0-preview%20(2023-02-01)&preserve-view=true) |

## Deprecated services

| Service documentation | Description | Reference documentation |
| --- | --- | --- |
| ![Anomaly Detector icon](~/reusable-content/ce-skilling/azure/media/ai-services/anomaly-detector.svg) [Anomaly Detector](../Anomaly-Detector/index.yml) <br>(deprecated 2023) | Identify potential problems early on | [Anomaly Detector API](https://westus2.dev.cognitive.microsoft.com/docs/services/AnomalyDetector-v1-1/operations/CreateMultivariateModel) |
| ![Content Moderator icon](~/reusable-content/ce-skilling/azure/media/ai-services/content-moderator.svg) [Content Moderator](../content-moderator/index.yml) <br>(deprecated 2024) | Detect potentially offensive or unwanted content | [Content Moderator API](../content-moderator/api-reference.md) |
| ![Language Understanding icon](~/reusable-content/ce-skilling/azure/media/ai-services/luis.svg) [Language understanding (LUIS)](../luis/index.yml) <br>(deprecated 2023) | Understand natural language in your apps | [LUIS API](https://westus.dev.cognitive.microsoft.com/docs/services/luis-endpoint-api-v3-0/operations/5cb0a9459a1fe8fa44c28dd8) |
| ![Metrics Advisor icon](~/reusable-content/ce-skilling/azure/media/ai-services/metrics-advisor.svg) [Metrics Advisor](../metrics-advisor/index.yml) <br>(deprecated 2023) | An AI service that detects unwanted contents | [Metrics Advisor API](https://westus.dev.cognitive.microsoft.com/docs/services/MetricsAdvisor/operations/createDataFeed) |
| ![Personalizer icon](~/reusable-content/ce-skilling/azure/media/ai-services/personalizer.svg) [Personalizer](../personalizer/index.yml) <br>(deprecated 2023) | Create rich, personalized experiences for each user | [Personalizer API](https://westus2.dev.cognitive.microsoft.com/docs/services/personalizer-api/operations/Rank) |
| ![QnA Maker icon](~/reusable-content/ce-skilling/azure/media/ai-services/luis.svg) [QnA maker](../qnamaker/index.yml) <br>(deprecated 2022) | Distill information into easy-to-navigate questions and answers | [QnA Maker API](https://westus.dev.cognitive.microsoft.com/docs/services/5a93fcf85b4ccd136866eb37/operations/5ac266295b4ccd1554da75ff) |

## Next steps

- [View Azure AI SDK reference](sdk-package-resources.md)
