---
title: Foundation models for healthcare in Azure AI Foundry portal
titleSuffix: Azure AI Foundry
description: Learn about AI models that are applicable to the health and life science industry.
ms.service: azure-ai-foundry
manager: scottpolly
ms.topic: concept-article
ms.date: 04/24/2025
ms.reviewer: itarapov
reviewer: ivantarapov
ms.author: mopeakande
author: msakande

#Customer intent: As a Data Scientist I want to learn what offerings are available within Health and Life Sciences AI Model offerings so that I can use them as the basis for my own AI solutions
---

# Foundation models for healthcare AI

[!INCLUDE [health-ai-models-meddev-disclaimer](../../includes/health-ai-models-meddev-disclaimer.md)]

In this article, you learn about the Microsoft multimodal healthcare foundation model catalog. The models were jointly developed by Microsoft Research, strategic partners, and leading healthcare institutions for healthcare organizations. Healthcare organizations can use the models to rapidly build and deploy AI solutions tailored to their specific needs, while minimizing the extensive compute and data requirements typically associated with building multimodal models from scratch. The intention isn't for these models to serve as standalone products. Instead, they're designed for developers to use as a foundation to build upon. With these healthcare AI models, professionals have the tools they need to harness the full potential of AI to enhance biomedical research, clinical workflows, and ultimately care delivery.

The power of artificial intelligence (AI) is driving a revolutionary transformation in the healthcare industry. While existing large language models like GPT-4 show tremendous promise for clinical text-based tasks and general-purpose multimodal reasoning, they struggle to understand non-text multimodal healthcare data - for example, medical imaging—radiology, pathology, and ophthalmology information resources. This problem covers other specialized medical text resources - for example, longitudinal electronic medical records. It becomes challenging to process non-text modalities like signal data, genomic data, and protein data, much of which isn't publicly available.

:::image type="content" source="../../media/how-to/healthcare-ai/connect-modalities.gif" alt-text="Models that reason about various modalities come together to support discover, development and delivery of healthcare":::

The Azure AI model catalog, available in [Azure AI Foundry](../model-catalog-overview.md) and [Azure Machine Learning studio](../../../machine-learning/concept-model-catalog.md), provides healthcare foundation models that facilitate AI-powered analysis of various medical data types. These AI models expand well beyond medical text comprehension into the multimodal reasoning about medical data. They can integrate and analyze data from diverse sources that come in various modalities - for example, medical imaging, genomics, clinical records, and other structured and unstructured data sources. The models also span several healthcare fields, including dermatology, ophthalmology, radiology, pathology, and more.

## Microsoft first-party models

These models are Microsoft's first party multimodal healthcare foundation models.

#### [MedImageInsight](./deploy-medimageinsight.md)
This model is an embedding model that enables sophisticated image analysis, including classification and similarity search in medical imaging. Researchers can use the model embeddings in simple zero-shot classifiers. They can also build adapters for their specific tasks, thereby streamlining workflows in radiology, pathology, ophthalmology, dermatology, and other modalities. For example, researchers can use the model to build tools that automatically route imaging scans to specialists, or flag potential abnormalities for further review. These actions can boost efficiency and improve patient outcomes. Furthermore, the model supports Responsible AI (RAI) safeguards, such as out-of-distribution (OOD) detection and drift monitoring. These safeguards maintain the stability and reliability of AI tools and data pipelines in dynamic medical imaging environments.  

#### [CXRReportGen](./deploy-cxrreportgen.md)
Chest X-rays are the most common radiology procedure globally. They help doctors diagnose a wide range of conditions - lung infections, heart problems, and more. For millions of people, these images often become the first step in detecting health issues. This multimodal AI model incorporates current and prior images, along with key patient information, to generate detailed, structured reports from chest X-rays. The reports highlight AI-generated findings based directly on the images, to align with human-in-the-loop workflows. Researchers can test this capability and the potential to accelerate turnaround times while enhancing the diagnostic precision of radiologists.

#### [MedImageParse and MedImageParse 3D](./deploy-medimageparse.md)
These models are designed for precise image segmentation, and they cover various imaging modalities, including X-Rays, CT scans, MRIs, ultrasounds, dermatology images, and pathology slides. The models can be fine-tuned for specific applications, such as tumor segmentation or organ delineation, allowing developers to test and validate the model and the ability to build tools that leverage AI for highly sophisticated medical image analysis.

## Partner models

The Azure AI model catalog also provides a curated collection of healthcare models from Microsoft partners with capabilities such as digital pathology slide analysis, biomedical research, medical knowledge sharing capabilities, and more. Partners including Paige.AI and Providence Healthcare provide these models. For a complete list of models, visit the [model catalog page](https://aka.ms/healthcaremodelstudio) resource.

## Related content

- [Model catalog and collections in Azure AI Foundry portal](../model-catalog-overview.md)
- [How to deploy and inference a managed compute deployment with code](../deploy-models-managed.md)
- [Overview: Deploy models, flows, and web apps with Azure AI Foundry](../../concepts/deployments-overview.md)