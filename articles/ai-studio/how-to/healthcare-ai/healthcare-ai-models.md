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

The healthcare industry is undergoing a revolutionary transformation driven by the power of artificial intelligence (AI). Modern medicine now encompasses various data modalities, including medical imaging, genomics, clinical records, and other structured and unstructured data sources. While existing large language models like [GPT-4](https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/models?tabs=python-secure#gpt-4o-and-gpt-4-turbo) have shown tremendous promise for clinical text-based tasks and general-purpose multimodal reasoning, they struggle to understand non-text multimodal healthcare data such as medical imaging—radiology, pathology, ophthalmology—and other specialized medical texts like longitudinal EMR data. They also find it challenging to process non-text modalities like signal data, genomic data, and protein data, much of which isn't publicly available.

As the pace of AI innovation accelerates, health and life science organizations are increasingly seeking solutions that go beyond medical text comprehension. These solutions require sophisticated AI models capable of integrating and analyzing diverse data sources across multiple modalities. Understanding the intricacies of this multimodal environment, Microsoft, alongside strategic partners, is releasing an array of foundational multimodal healthcare AI models in the Azure AI Model Catalog across modalities like dermatology, ophthalmology, radiology, pathology, and others. We strongly believe that the future of medical AI is multimodal and the key to success is ability to bring together the best of AI models from across the industry. 

:::image type="content" source="../../media/how-to/healthcare-ai/connect-modalities.gif" alt-text="Models that reason about various modalities come together to support discover, development and delivery of healthcare":::

In this article, you will learn about Microsoft's catalog of foundational multimodal healthcare AI models and how to use them. Developed in collaboration with Microsoft Research, strategic partners, and leading healthcare institutions, these AI models are specifically designed for healthcare organizations to rapidly build and deploy AI solutions tailored to their specific needs—all while minimizing the extensive compute and data requirements typically associated with building multimodal models from scratch. While these models are not intended to serve as standalone products, they are designed so developers can build on top of them. With these healthcare AI models, professionals have the tools they need to harness the full potential of AI to enhance patient care.

These models will enable the broader research and developer community to accelerate health and life sciences discovery, development, and delivery applications. This will lead to new treatments and better physician and patient care across the full lifecycle—from pharma and biotech to clinical applications.


## Microsoft First Party Models

Microsoft's first party Foundational Multimodal Healthcare AI Models include the following models:

### [MedImageInsight](./deploy-medimageinsight.md)
This embedding model enables sophisticated image analysis, including classification and similarity search in medical imaging. Researchers can use the model embeddings directly, or build adapters for their specific tasks, streamlining workflows in radiology, pathology, ophthalmology, dermatology and other modalities. For example, the model can be used to build tools to automatically route imaging scans to specialists, or flag potential abnormalities for further review, improving efficiency and patient outcomes. Furthermore, the model can be leveraged for Responsible AI (RAI) safeguards such as out-of-distribution (OOD) detection and drift monitoring, to maintain stability and reliability of AI tools and data pipelines in dynamic medical imaging environments.  

### [CXRReportGen](./deploy-cxrreportgen.md)
Chest X-rays are the most common radiology procedure globally. They’re crucial because they help doctors diagnose a wide range of conditions—from lung infections to heart problems. These images are often the first step in detecting health issues that affect millions of people. By incorporating current and prior images, along with key patient information, this multimodal AI model generates detailed, structured reports from chest X-rays, highlighting AI-generated findings directly on the images to align with human-in-the-loop workflows. This capability accelerates turnaround times while enhancing the diagnostic precision of radiologists. This model is currently state of the art on the industry standard MIMIC-CXR benchmark. 

### [MedImageParse](./deploy-medimageparse.md)
Designed for precise image segmentation, this model covers various imaging modalities, including X-Rays, CT scans, MRIs, ultrasounds, dermatology images, and pathology slides. It can be fine-tuned for specific applications such as tumor segmentation or organ delineation, allowing to build tools on top of this model that leverage AI for highly targeted cancer and other disease detection, diagnostics and treatment planning.