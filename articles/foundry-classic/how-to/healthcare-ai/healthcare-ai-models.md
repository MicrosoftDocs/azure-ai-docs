---
title: "Healthcare AI foundation models (classic)"
description: "Explore healthcare AI foundation models in Microsoft Foundry for medical imaging, genomics, and clinical data analysis. Deploy multimodal AI models to build healthcare solutions. (classic)"
ms.service: microsoft-foundry
ms.subservice: foundry-models
ms.topic: concept-article
ms.date: 01/23/2026
ms.reviewer: itarapov
reviewer: ivantarapov
ms.author: mopeakande
manager: mcleans
author: msakande

#Customer intent: As a Data Scientist I want to learn what offerings are available within Health and Life Sciences AI Model offerings so that I can use them as the basis for my own AI solutions
---

# Foundation models for healthcare AI (classic)

[!INCLUDE [classic-banner](../../includes/classic-banner.md)]

[!INCLUDE [health-ai-models-meddev-disclaimer](includes/health-ai-models-meddev-disclaimer.md)]

[!INCLUDE [health-ai-models-intro](../../../foundry/how-to/healthcare-ai/includes/health-ai-models-intro.md)]

## Microsoft first-party models

These models are Microsoft's first-party multimodal healthcare foundation models.

#### [MedImageInsight](./deploy-medimageinsight.md)
This model is an embedding model that enables sophisticated image analysis, including classification and similarity search in medical imaging. Researchers can use the model embeddings in simple zero-shot classifiers. They can also build adapters for their specific tasks, thereby streamlining workflows in radiology, pathology, ophthalmology, dermatology, and other modalities. For example, researchers can use the model to build tools that automatically route imaging scans to specialists or flag potential abnormalities for further review. These actions boost efficiency and improve patient outcomes. The model also supports Responsible AI (RAI) safeguards, such as out-of-distribution (OOD) detection and drift monitoring. These safeguards maintain the stability and reliability of AI tools and data pipelines in dynamic medical imaging environments.  

#### [CXRReportGen](./deploy-cxrreportgen.md)
Chest X-rays are the most common radiology procedure worldwide. They help doctors diagnose a wide range of conditions—lung infections, heart problems, and more. For millions of people, these images are often the first step in detecting health issues. This multimodal AI model incorporates current and prior images, along with key patient information, to generate detailed, structured reports from chest X-rays. The reports highlight AI-generated findings based directly on the images to align with human-in-the-loop workflows. Researchers can test this capability and its potential to speed up turnaround times while enhancing the diagnostic precision of radiologists.

#### [MedImageParse and MedImageParse 3D](./deploy-medimageparse.md)
These models are designed for precise image segmentation and cover different imaging modalities, including X-rays, CT scans, MRIs, ultrasounds, dermatology images, and pathology slides. You can fine-tune the models for specific applications, such as tumor segmentation or organ delineation. This allows you to test and validate the model and build tools that use AI for highly sophisticated medical image analysis.

## Partner models

[!INCLUDE [health-ai-models-partners](../../../foundry/how-to/healthcare-ai/includes/health-ai-models-partners.md)]

## Related content

- [Model catalog and collections in Foundry portal](../../concepts/foundry-models-overview.md)
- [How to deploy and inference a managed compute deployment with code](../deploy-models-managed.md)
- [Overview: Deploy models, flows, and web apps with Foundry](../../concepts/deployments-overview.md)