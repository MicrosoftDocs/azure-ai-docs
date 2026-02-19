---
title: Healthcare AI foundation models
titleSuffix: Microsoft Foundry
description: "Explore healthcare AI foundation models in Microsoft Foundry for medical imaging, genomics, and clinical data analysis. Deploy multimodal AI models to build healthcare solutions."
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: concept-article
ms.date: 01/23/2026
ms.reviewer: itarapov
reviewer: ivantarapov
ms.author: mopeakande
manager: nitinme
author: msakande

#Customer intent: As a Data Scientist I want to learn what offerings are available within Health and Life Sciences AI Model offerings so that I can use them as the basis for my own AI solutions
---

# Foundation models for healthcare AI

[!INCLUDE [classic-banner](../../includes/classic-banner.md)]

[!INCLUDE [health-ai-models-meddev-disclaimer](../../includes/health-ai-models-meddev-disclaimer.md)]

This article introduces healthcare AI foundation models available in the Microsoft multimodal model catalog. Microsoft Research, strategic partners, and leading healthcare institutions jointly developed these models to help healthcare organizations rapidly build and deploy AI solutions for medical imaging, genomics, clinical records, and biomedical research. You can use these models to quickly build and deploy AI solutions tailored to your specific needs while minimizing the extensive compute and data requirements typically associated with building multimodal models from scratch. These models aren't designed to serve as standalone products. Instead, developers can use them as a foundation to build upon. With these healthcare AI models, you have the tools you need to harness the full potential of AI to enhance biomedical research, clinical workflows, and ultimately care delivery.

The power of artificial intelligence (AI) is driving a revolutionary transformation in the healthcare industry. While existing large language models like GPT-4 show tremendous promise for clinical text-based tasks and general-purpose multimodal reasoning, they struggle to understand non-text multimodal healthcare data. For example, medical imaging (radiology, pathology, and ophthalmology information resources). This problem covers other specialized medical text resources. For example, longitudinal electronic medical records. It becomes challenging to process non-text modalities like signal data, genomic data, and protein data, much of which isn't publicly available.

:::image type="content" source="../../media/how-to/healthcare-ai/connect-modalities.gif" alt-text="Animation showing healthcare AI models connecting different data modalities including imaging, genomics, and clinical records for discovery, development, and delivery.":::

The Foundry model catalog, available in [Microsoft Foundry](../../concepts/foundry-models-overview.md) and [Azure Machine Learning studio](../../../machine-learning/concept-model-catalog.md), provides healthcare foundation models that let you analyze various medical data types with AI. These AI models expand well beyond medical text comprehension into multimodal reasoning about medical data. They can integrate and analyze data from diverse sources that come in various modalities. For example, medical imaging, genomics, clinical records, and other structured and unstructured data sources. The models also span several healthcare fields, including dermatology, ophthalmology, radiology, pathology, and more.

## Microsoft first-party models

These models are Microsoft's first-party multimodal healthcare foundation models.

#### [MedImageInsight](./deploy-medimageinsight.md)
This model is an embedding model that enables sophisticated image analysis, including classification and similarity search in medical imaging. Researchers can use the model embeddings in simple zero-shot classifiers. They can also build adapters for their specific tasks, thereby streamlining workflows in radiology, pathology, ophthalmology, dermatology, and other modalities. For example, researchers can use the model to build tools that automatically route imaging scans to specialists or flag potential abnormalities for further review. These actions boost efficiency and improve patient outcomes. The model also supports Responsible AI (RAI) safeguards, such as out-of-distribution (OOD) detection and drift monitoring. These safeguards maintain the stability and reliability of AI tools and data pipelines in dynamic medical imaging environments.  

#### [CXRReportGen](./deploy-cxrreportgen.md)
Chest X-rays are the most common radiology procedure worldwide. They help doctors diagnose a wide range of conditions—lung infections, heart problems, and more. For millions of people, these images are often the first step in detecting health issues. This multimodal AI model incorporates current and prior images, along with key patient information, to generate detailed, structured reports from chest X-rays. The reports highlight AI-generated findings based directly on the images to align with human-in-the-loop workflows. Researchers can test this capability and its potential to speed up turnaround times while enhancing the diagnostic precision of radiologists.

#### [MedImageParse and MedImageParse 3D](./deploy-medimageparse.md)
These models are designed for precise image segmentation and cover different imaging modalities, including X-rays, CT scans, MRIs, ultrasounds, dermatology images, and pathology slides. You can fine-tune the models for specific applications, such as tumor segmentation or organ delineation. This allows you to test and validate the model and build tools that use AI for highly sophisticated medical image analysis.

## Partner models

The model catalog also provides a curated collection of healthcare models from Microsoft partners with capabilities such as digital pathology slide analysis, biomedical research, and medical knowledge sharing. Partners like Paige.AI and Providence Healthcare provide these models. For a complete list of models, see the [model catalog page](https://aka.ms/healthcaremodelstudio).

## Related content

- [Model catalog and collections in Foundry portal](../../concepts/foundry-models-overview.md)
- [How to deploy and inference a managed compute deployment with code](../deploy-models-managed.md)
- [Overview: Deploy models, flows, and web apps with Foundry](../../concepts/deployments-overview.md)