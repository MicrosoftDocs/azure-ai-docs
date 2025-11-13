---
title: Migrate from Custom Vision Service
description: Guidance for migrating from Azure Custom Vision Service to alternative solutions before its retirement in September 2028.
author: PatrickFarley
ms.author: pafarley
ms.date: 09/24/2025
ms.topic: how-to
ms.service: azure-ai-custom-vision
ms.custom: ai-migration, vision
---

# Migrate from Custom Vision Service

The Custom Vision Service will be retired on September 25, 2028, after which calls made to the service will fail. Microsoft will provide full support for all existing Azure Custom Vision customers until 9/25/2028, but to ensure business continuity and minimize disruption, customers are encouraged to begin planning their migration to alternative solutions that best meet their scenario requirements. This document provides comprehensive guidance for evaluating, selecting, and transitioning to new services.

## Migration preparation checklist

1.	Assess current usage and dependencies on Custom Vision Service.
2.	Identify business scenarios and technical requirements for image classification and object detection.
3.	Evaluate alternative solutions based on capabilities, integration, cost, and support.
4.	Plan data export and model migration steps.
5.	Test new solution(s) in a staging environment.
6.	Update production workflows and retrain stakeholders.

## Alternative options based on scenario needs
There are several alternative platforms and services you can consider depending on your specific use case, technical requirements, and integration needs. We recommended the following options for common scenarios:

### Traditional machine learning options

To create both custom image classification and object detection models using traditional machine learning techniques, consider Azure Machine Learning with AutoML.

* **Best for**: Customers seeking to apply classic machine learning techniques
* **Features**: Offers a code-first experience, as well as a no-code studio web experience similar to Custom Vision. It offers the ability to easily train custom image classification and object detection models on your image data.
* **Learn more** about Azure Machine Learning AutoML:
    * [What is automated machine learning?](../../machine-learning/concept-automated-ml.md)
    * [Set up no-code Automated ML training for tabular data with the studio UI](../../machine-learning/how-to-use-automated-ml-for-ml-models.md)
    * [Set up AutoML to train computer vision models](../../machine-learning/how-to-auto-train-image-models.md) 

### Generative AI-based solutions
Microsoft is also investing in Generative AI-based solutions that increase accuracy in custom scenarios using prompt engineering and other techniques.

#### Generative AI solutions in Microsoft Foundry

* **Best for**: Customers who are flexible in their approach to creating a solution for customized vision capabilities.
*	**Features**: Flexibility to build custom solutions based on different Generative AI models.
*	**Learn more** about Generative AI models in the Foundry: 
    *	[Explore Foundry Models](../../ai-foundry/concepts/foundry-models-overview.md)
    *	[Azure OpenAI in Foundry models](/azure/ai-foundry/foundry-models/concepts/models-sold-directly-by-azure?tabs=global-standard-aoai%2Cstandard-chat-completions%2Cglobal-standard&pivots=azure-openai#azure-openai-in-azure-ai-foundry-models)

#### Azure Content Understanding in Foundry Tools (preview)
* **Best for**: Customers who want a managed generative solution for image classification
* **Features**: Content Understanding offers the ability to create custom classification workflows. It also supports processing unstructured data of any type (image, documents, audio, video) and extracting structured insights based on pre-defined or user-defined formats.
* **Learn more** about Content Understanding:
    * [What is Azure Content Understanding?](../content-understanding/overview.md)
    * [Azure Content Understanding image solutions (preview)](../content-understanding/image/overview.md)
    * [Content Understanding classifier](../content-understanding/concepts/classifier.md)

## Data migration guidance
Before you migrate services, export your labeled datasets and model metadata from Custom Vision Service. Review the data formats required by your chosen alternative and convert as needed.

## Next steps and required actions
* Make a plan to transition away from Azure Custom Vision by September 25, 2026.
* Azure Custom Vision will be retired on 25 September 2028, please transition to alternative options by that date.
