---
title: What are Foundry Tools?
titleSuffix: Foundry Tools
description: Foundry Tools are cloud-based artificial intelligence (AI) services that help developers build cognitive intelligence into applications without having direct AI or data science skills or knowledge.
author: nitinme
manager: nitinme
keywords: Foundry Tools, cognitive
ms.service: azure-ai-services
ms.topic: overview
ms.date: 10/02/2025
ms.author: nitinme
ms.custom:
  - build-2023
  - build-2023-dataai
  - ignite-2023
---

# What are Foundry Tools?

[!INCLUDE [About Foundry Tools](./includes/ai-services-intro.md)]

## Available Foundry Tools

When building AI applications, use the following Foundry Tools:

| Service | Description |
| --- | --- |
| ![Speech icon](~/reusable-content/ce-skilling/azure/media/ai-services/speech.svg) [Speech](./speech-service/index.yml) | Speech to text, text to speech, translation, and speaker recognition. |
| ![Translator icon](~/reusable-content/ce-skilling/azure/media/ai-services/translator.svg) [Translator](./translator/index.yml) | Use AI-powered translation technology to translate more than 100 in-use, at-risk, and endangered languages and dialects. |
| ![Language icon](~/reusable-content/ce-skilling/azure/media/ai-services/language.svg) [Language](./language-service/index.yml) | Build apps with industry-leading natural language understanding capabilities. |
| ![Content Understanding icon](~/reusable-content/ce-skilling/azure/media/ai-services/document-intelligence.svg) [Content Understanding](./content-understanding/index.yml) | Analyze and comprehend various media content types. |
| ![Document Intelligence icon](~/reusable-content/ce-skilling/azure/media/ai-services/document-intelligence.svg) [Document Intelligence](./document-intelligence/index.yml) | Turn documents into intelligent data-driven solutions. |
| ![Vision icon](~/reusable-content/ce-skilling/azure/media/ai-services/vision.svg) [Vision](./computer-vision/index.yml) | Analyze content in images and videos. |
| ![Azure AI Search icon](~/reusable-content/ce-skilling/azure/media/ai-services/search.svg) [Azure AI Search](/azure/search/) | Bring AI-powered cloud search to your mobile and web apps. |
| ![Content Safety icon](~/reusable-content/ce-skilling/azure/media/ai-services/content-safety.svg) [Content Safety](./content-safety/index.yml) | An AI service that detects unwanted contents. |
| ![Custom Vision icon](~/reusable-content/ce-skilling/azure/media/ai-services/custom-vision.svg) [Custom Vision](./custom-vision-service/index.yml) | Customize image recognition for your business. |
| ![Immersive Reader icon](~/reusable-content/ce-skilling/azure/media/ai-services/immersive-reader.svg) [Immersive Reader](./immersive-reader/index.yml) | Help users read and comprehend text. |

The following Foundry Tools are scheduled for retirement. These services are still available for existing applications but don't use them for new AI applications:

| Service | Description |
| --- | --- |
| ![Anomaly Detector icon](~/reusable-content/ce-skilling/azure/media/ai-services/anomaly-detector.svg) [Anomaly Detector](./Anomaly-Detector/index.yml) (retired) | Identify potential problems early on. |
| ![Content Moderator icon](~/reusable-content/ce-skilling/azure/media/ai-services/content-moderator.svg) [Content Moderator](./content-moderator/index.yml) (retired) | Detect potentially offensive or unwanted content. |
| ![Language Understanding icon](~/reusable-content/ce-skilling/azure/media/ai-services/luis.svg) [Language understanding](./luis/index.yml) (retired) | Understand natural language in your apps. |
| ![Metrics Advisor icon](~/reusable-content/ce-skilling/azure/media/ai-services/metrics-advisor.svg) [Metrics Advisor](./metrics-advisor/index.yml) (retired) | An AI service that detects unwanted contents. 
| ![Personalizer icon](~/reusable-content/ce-skilling/azure/media/ai-services/personalizer.svg) [Personalizer](./personalizer/index.yml) (retired) | Create rich, personalized experiences for each user. |
| ![QnA Maker icon](~/reusable-content/ce-skilling/azure/media/ai-services/luis.svg) [QnA maker](./qnamaker/index.yml) (retired) | Distill information into easy-to-navigate questions and answers. |

## Pricing tiers and billing

Pricing tiers (and the amount you get billed) are based on the number of transactions you send using your authentication information. Each pricing tier specifies the:
* Maximum number of allowed transactions per second (TPS).
* Service features enabled within the pricing tier.
* Cost for a predefined number of transactions. Going above this number causes an extra charge as specified in the [pricing details](https://azure.microsoft.com/pricing/details/cognitive-services/) for your service.

> [!NOTE]
> Many of the Foundry Tools have a free tier you can use to try the service. To use the free tier, use `F0` as the SKU for your resource.

## Development options

The tools that you can use to customize and configure models are different from tools that you use to call the Foundry Tools. Out of the box, most Foundry Tools allow you to send data and receive insights without any customization. For example:

* You can send an image to the Azure Vision in Foundry Tools service to detect words and phrases or count the number of people in the frame
* You can send an audio file to the Speech service and get transcriptions and translate the speech to text at the same time

Azure offers a wide range of tools that are designed for different types of users, many of which can be used with Foundry Tools. Designer-driven tools are the easiest to use, and are quick to set up and automate, but might have limitations when it comes to customization. Our REST APIs and client libraries provide users with more control and flexibility, but require more effort, time, and expertise to build a solution. If you use REST APIs and client libraries, there's an expectation that you're comfortable working with modern programming languages like C#, Java, Python, JavaScript, or another popular programming language.

Let's take a look at the different ways that you can work with the Foundry Tools.

### Client libraries and REST APIs

Foundry Tools client libraries and REST APIs provide direct access to your service. These tools provide programmatic access to the Foundry Tools, their baseline models, and in many cases allow you to programmatically customize your models and solutions.

* **Target user(s)**: Developers and data scientists.
* **Benefits**: Provides the greatest flexibility to call the services from any language and environment.
* **Subscription(s)**: Azure account + Foundry Tools resources.

If you want to learn more about available client libraries and REST APIs, use our [Foundry Tools overview](index.yml) to pick a service and get started with one of our quickstarts.

### Continuous integration and deployment

You can use Azure DevOps and GitHub Actions to manage your deployments. In the [following section](#continuous-integration-and-delivery-with-devops-and-github-actions), we have two examples of CI/CD integrations to train and deploy custom models for Speech and Azure Language Understanding (LUIS) service.

* **Target user(s)**: Developers, data scientists, and data engineers.
* **Benefits**: Allows you to continuously adjust, update, and deploy applications and models programmatically. There's significant benefit when regularly using your data to improve and update models for Speech, Vision, Language, and Decision.
* **Subscription(s)**: Azure account + Foundry Tools resource + GitHub account.

### Continuous integration and delivery with DevOps and GitHub Actions

Language Understanding and the Speech service offer continuous integration and continuous deployment solutions that are powered by Azure DevOps and GitHub Actions. These tools are used for automated training, testing, and release management of custom models.

* [CI/CD for Custom Speech](./speech-service/how-to-custom-speech-continuous-integration-continuous-deployment.md)
* [CI/CD for LUIS](./luis/luis-concept-devops-automation.md)

### On-premises containers

Many of the Foundry Tools can be deployed in containers for on-premises access and use. Using these containers gives you the flexibility to bring Foundry Tools closer to your data for compliance, security, or other operational reasons. For a complete list of Azure AI containers, see [On-premises containers for Foundry Tools](./cognitive-services-container-support.md).

### Training models

Some services allow you to bring your own data, then train a model. Trained custom models allow you to extend the model using the service's data and algorithm with your own data. The output matches your needs. When you bring your own data, you might need to tag the data in a way specific to the service. For example, if you're training a model to identify flowers, you can provide a catalog of flower images along with the location of the flower in each image to train the model.

## Foundry Tools in the ecosystem

With Azure and Foundry Tools, you have access to a broad ecosystem, such as:

* Automation and integration tools like Logic Apps and Power Automate.
* Deployment options such as Azure Functions and the App Service.
* Foundry Tools Docker containers for secure access.
* Tools like Apache Spark, Azure Databricks, Azure Synapse Analytics, and Azure Kubernetes Service for big data scenarios.

## Regional availability

The APIs in Foundry Tools are hosted on a growing network of Microsoft-managed data centers. You can find the regional availability for each API in [Azure region list](https://azure.microsoft.com/regions "Azure region list").

## Language support

Foundry Tools support a wide range of cultural languages at the service level. You can find the language availability for each API in the [supported languages list](language-support.md "Supported languages list").

## Security

Foundry Tools provide a layered security model, including [authentication](authentication.md "Authentication") with Microsoft Entra credentials, a valid resource key, and [Azure Virtual Networks](cognitive-services-virtual-networks.md "Azure Virtual Networks").

## Certifications and compliance

Foundry Tools awarded certifications include Cloud Security Alliance STAR Certification, FedRAMP Moderate, and HIPAA BAA.

To understand privacy and data management, go to the [Trust Center](https://servicetrust.microsoft.com/ "Trust Center").

## Help and support

Foundry Tools provide several support options to help you move forward with creating intelligent applications. Foundry Tools also have a strong community of developers that can help answer your specific questions. For a full list of support options available to you, see [Foundry Tools support and help options](cognitive-services-support-options.md).

## Related content

* Learn how to [get started with Azure](https://azure.microsoft.com/get-started/)
* [Try Foundry Tools and more in the Foundry portal](../ai-foundry/what-is-foundry.md)
* [Plan and manage costs for Foundry Tools](plan-manage-costs.md)
