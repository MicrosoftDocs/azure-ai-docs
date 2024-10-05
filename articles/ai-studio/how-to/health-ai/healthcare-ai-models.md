---
title: How do Deploy Health and Life Sciences AI Models with AI Studio
titleSuffix: Azure AI Studio
description: Learn how to use Health and Life Sciences AI Models models with Azure AI Studio.
ms.service: azure-ai-studio
manager: scottpolly
ms.topic: concept-article # Don't change
ms.date: 10/10/2024
ms.reviewer: itarapov
reviewer: fkriti
ms.author: itarapov
author: ivantarapov
ms.custom: references_regions, generated

#Customer intent: As a Data Scientist I want to learn what offerings are available within Health and Life Sciences AI Model offerings so that I can use them as the basis for my own AI solutions
---

# Health and Life Sciences AI Models

[!INCLUDE [Feature preview](~/reusable-content/ce-skilling/azure/includes/ai-studio/includes/feature-preview.md)]

[!INCLUDE [health-ai-models-meddev-disclaimer](../../includes/health-ai-models-meddev-disclaimer.md)]

In this article, you will learn about Microsoft's catalog of Foundational Multimodal Healthcare AI Models and how to use them. These models are targeting a wide variety of scenarios that AI developers for medical industry are developing for. While these models are not intended to serve as standalone products, they are designed so that developers can build on top of them. 

The healthcare industry is undergoing a revolutionary transformation, driven by the power of artificial intelligence (AI). Developed in collaboration with Microsoft Research, our strategic partners, and leading healthcare institutions, the AI models presented here are specifically designed for healthcare organizations to rapidly build and deploy AI solutions tailored to their specific needs, all while minimizing the extensive compute and data requirements typically associated with building multimodal models from scratch. With the healthcare AI models, healthcare professionals have the tools they need to harness the full potential of AI to enhance patient care.   

Modern medicine encompasses various data modalities, including medical imaging, genomics, clinical records, and other structured and unstructured data sources. Understanding the intricacies of this multimodal environment, Azure AI onboards specialized healthcare AI models that go beyond traditional text-based applications, providing robust solutions tailored to healthcare's unique challenges.


## Microsoft First Party Models

Microsoft's first party Foundational Multimodal Healthcare AI Models include the following models:

### [MedImageInsight](./deploy-medimageinsight.md)
This embedding model enables sophisticated image analysis, including classification and similarity search in medical imaging. Researchers can use the model embeddings directly, or build adapters for their specific tasks, streamlining workflows in radiology, pathology, ophthalmology, dermatology and other modalities. For example, the model can be used to build tools to automatically route imaging scans to specialists, or flag potential abnormalities for further review, improving efficiency and patient outcomes. Furthermore, the model can be leveraged for Responsible AI (RAI) safeguards such as out-of-distribution (OOD) detection and drift monitoring, to maintain stability and reliability of AI tools and data pipelines in dynamic medical imaging environments.  

### [CXRReportGen](./deploy-cxrreportgen.md)
Chest X-rays are the most common radiology procedure globally. They’re crucial because they help doctors diagnose a wide range of conditions—from lung infections to heart problems. These images are often the first step in detecting health issues that affect millions of people. By incorporating current and prior images, along with key patient information, this multimodal AI model generates detailed, structured reports from chest X-rays, highlighting AI-generated findings directly on the images to align with human-in-the-loop workflows. This capability accelerates turnaround times while enhancing the diagnostic precision of radiologists. This model is currently state of the art on the industry standard MIMIC-CXR benchmark. 

### [MedImageParse](./deploy-medimageparse.md)
Designed for precise image segmentation, this model covers various imaging modalities, including X-Rays, CT scans, MRIs, ultrasounds, dermatology images, and pathology slides. It can be fine-tuned for specific applications such as tumor segmentation or organ delineation, allowing to build tools on top of this model that leverage AI for highly targeted cancer and other disease detection, diagnostics and treatment planning.