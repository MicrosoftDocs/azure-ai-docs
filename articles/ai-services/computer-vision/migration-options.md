---
title: Migrate from Azure Vision in Foundry Tools - Image Analysis
description: Guidance for migrating from Azure Vision - Image Analysis API to alternative solutions before its retirement in September 2028.
author: PatrickFarley
ms.author: pafarley
ms.date: 10/01/2025
ms.topic: upgrade-and-migration-article
ms.service: azure-ai-vision
ms.custom: ai-migration, vision
---

# Migrate from Azure Vision in Foundry Tools - Image Analysis

The Azure Vision in Foundry Tools - Image Analysis API will be retired on September 25, 2028. After that date, calls to the service fail. Microsoft supports all existing Image Analysis customers until the retirement date. To ensure business continuity and minimize disruption, start planning your migration to alternative solutions that best meet your scenario requirements. This article provides comprehensive guidance for evaluating, selecting, and transitioning to new services.

## Migration preparation checklist

1.	Assess current usage and dependencies on Image Analysis API.
1.	Identify business scenarios and technical requirements for your image analysis scenarios.
1.	Evaluate alternative solutions based on capabilities, integration, cost, and support.
1.	Plan model migration steps.
1.	Test new solutions in a staging environment.
1.	Update production workflows and retrain stakeholders.

## Alternative options based on scenario needs
Consider these alternative platforms and services depending on your specific use case, technical requirements, and integration needs. The following options are recommended for each set of features under Image Analysis.

### For OCR and Read capabilities, try Document Intelligence

Azure Document Intelligence  provides support for OCR text in images.

* **Features**: Azure Document Intelligence is a cloud-based Foundry tool that you can use to build intelligent document processing solutions.
* **Learn more** about Document Intelligence:
    * [What is Azure Document Intelligence?](../document-intelligence/overview.md)
    * [Document Intelligence Read model](../document-intelligence/prebuilt/read.md)

### For face scenarios, try the Face API

The Face service offers face detection capabilities, as well as a more comprehensive portfolio of face-related features. 
* **Features**: Full support for all face scenarios under the Image Analysis API, plus face recognition scenarios like person identification.
* **Learn more** about the Face API:
    * [What is the Azure AI Face Service?](./overview-identity.md)
    * [Face detection, attributes, and input data](./concept-face-detection.md)

### Image embeddings scenarios

#### Cohere Embed v3 in Microsoft Foundry
* **Best for**: Customers who need image and text embeddings supported on Azure.
* **Features**: A multilingual multimodal embedding model supported in the Microsoft Foundry portal. It transforms different modalities such as images, texts, and interleaved images and texts into a single vector representation.
* **Learn more** about Cohere Embed v4:
    * [Embed-v-4-0](https://ai.azure.com/resource/models/embed-v-4-0/version/5/registry/azureml-cohere)

#### SigLIP (Sigmoid Loss for Language Image Pre training)
* **Best for**: Customers who need strong zero shot classification and image text retrieval abilities.
* **Features**: A CLIP‐style vision‐language model from Google that replaces the standard contrastive (softmax) loss with a pairwise sigmoid loss. It trains on large scale image text pairs.
* **Learn more** about SigLIP:
    * [Sigmoid Loss for Language Image Pre-Training](https://arxiv.org/abs/2303.15343?utm_source=chatgpt.com)
    * [SigLP on Hugging Face](https://huggingface.co/docs/transformers/main/model_doc/siglip)

### Other Image Analysis scenarios

Alternative services support the remaining scenarios that the Image Analysis API supports. 

#### GPT model series in Microsoft Foundry

* **Best for**: Customers who are flexible in their approach to creating a solution for customized vision capabilities.
* **Features**: Flexibility to build custom solutions based on different Generative AI models.
* **Learn more** about Generative AI models in the Microsoft Foundry:
    *	[Explore Microsoft Foundry Models](../../ai-foundry/concepts/foundry-models-overview.md)
    *	[Azure OpenAI in Microsoft Foundry models](../../ai-foundry/foundry-models/concepts/models-sold-directly-by-azure.md)

#### Azure Content Understanding in Foundry Tools
* **Best for**: Customers who want a managed generative solution for image analysis scenarios.
* **Features**: Content Understanding supports processing unstructured image data, as well as documents, audio, and video. It enables you to extract structured insights based on pre-defined or user-defined formats.
* **Learn more** about Content Understanding:
    * [What is Azure Content Understanding in Foundry Tools?](../content-understanding/overview.md)
    * [Azure Content Understanding image solutions (preview)](../content-understanding/image/overview.md)
    * [Content Understanding classifier](../content-understanding/concepts/classifier.md)

## Next steps and required actions
* Make a plan to transition away from Azure Computer Vision – Image Analysis by September 25, 2026.
* Azure Computer Vision – Image Analysis will be retired on September 25, 2028. Transition to alternative options by that date.
