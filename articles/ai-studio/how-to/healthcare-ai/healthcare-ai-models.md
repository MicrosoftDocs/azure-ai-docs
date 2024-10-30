---
title: Foundation models for healthcare in AI Studio
titleSuffix: Azure AI Studio
description: Learn about AI models that are applicable to the health and life science industry.
ms.service: azure-ai-studio
manager: scottpolly
ms.topic: concept-article
ms.date: 10/20/2024
ms.reviewer: itarapov
reviewer: ivantarapov
ms.author: mopeakande
author: msakande

#Customer intent: As a Data Scientist I want to learn what offerings are available within Health and Life Sciences AI Model offerings so that I can use them as the basis for my own AI solutions
---

# Foundation models for healthcare AI

[!INCLUDE [Feature preview](~/reusable-content/ce-skilling/azure/includes/ai-studio/includes/feature-preview.md)]

[!INCLUDE [health-ai-models-meddev-disclaimer](../../includes/health-ai-models-meddev-disclaimer.md)]

In this article, you learn about Microsoft's catalog of multimodal healthcare foundation models. The models were developed in collaboration with Microsoft Research, strategic partners, and leading healthcare institutions for healthcare organizations. Healthcare organizations can use the models to rapidly build and deploy AI solutions tailored to their specific needs, while minimizing the extensive compute and data requirements typically associated with building multimodal models from scratch. The intention isn't for these models to serve as standalone products; rather, they're designed for developers to use as a foundation to build upon. With these healthcare AI models, professionals have the tools they need to harness the full potential of AI to enhance biomedical research, clinical workflows, and ultimately care delivery.

The healthcare industry is undergoing a revolutionary transformation driven by the power of artificial intelligence (AI). While existing large language models like GPT-4 show tremendous promise for clinical text-based tasks and general-purpose multimodal reasoning, they struggle to understand non-text multimodal healthcare data such as medical imaging—radiology, pathology, ophthalmology—and other specialized medical text like longitudinal electronic medical records. They also find it challenging to process non-text modalities like signal data, genomic data, and protein data, much of which isn't publicly available.

:::image type="content" source="../../media/how-to/healthcare-ai/connect-modalities.gif" alt-text="Models that reason about various modalities come together to support discover, development and delivery of healthcare":::

The Azure AI model catalog available in [AI Studio](../model-catalog-overview.md) and [Azure Machine Learning studio](../../../machine-learning/concept-model-catalog.md) provides healthcare foundation models that facilitate AI-powered analysis of various medical data types and expand well beyond medical text comprehension into the multimodal reasoning about medical data. These AI models can integrate and analyze data from diverse sources that come in various modalities, such as medical imaging, genomics, clinical records, and other structured and unstructured data sources. The models also span several healthcare fields like dermatology, ophthalmology, radiology, and pathology. 

## Microsoft first-party models

The following models are Microsoft's first party multimodal healthcare foundation models.

#### [MedImageInsight](./deploy-medimageinsight.md)
This model is an embedding model that enables sophisticated image analysis, including classification and similarity search in medical imaging. Researchers can use the model embeddings in simple zero-shot classifiers or to build adapters for their specific tasks, thereby streamlining workflows in radiology, pathology, ophthalmology, dermatology, and other modalities. For example, researchers can explore how the model can be used to  build tools that automatically route imaging scans to specialists or flag potential abnormalities for further review. These actions can enable improved efficiency and patient outcomes. Furthermore, the model can be leveraged for Responsible AI (RAI) safeguards such as out-of-distribution (OOD) detection and drift monitoring, to maintain stability and reliability of AI tools and data pipelines in dynamic medical imaging environments.  

#### [CXRReportGen](./deploy-cxrreportgen.md)
Chest X-rays are the most common radiology procedure globally. They're crucial because they help doctors diagnose a wide range of conditions—from lung infections to heart problems. These images are often the first step in detecting health issues that affect millions of people. This multimodal AI model incorporates current and prior images along with key patient information to generate detailed, structured reports from chest X-rays. The reports highlight AI-generated findings directly on the images to align with human-in-the-loop workflows. Researchers can test this capability and the potential to accelerate turnaround times while enhancing the diagnostic precision of radiologists. 

#### [MedImageParse](./deploy-medimageparse.md)
This model is designed for precise image segmentation, and it covers various imaging modalities, including X-Rays, CT scans, MRIs, ultrasounds, dermatology images, and pathology slides. The model can be fine-tuned for specific applications, such as tumor segmentation or organ delineation, allowing developers to test and validate the model and the ability to build tools that leverage AI for highly sophisticated medical image analysis.

## Partner models

The Azure AI model catalog also provides a curated collection of healthcare models from Microsoft partners with capabilities such as digital pathology slide analysis, biomedical research, and medical knowledge sharing. These models come from partners that include Paige.AI and Providence Healthcare. For a complete list of models, refer to the [model catalog page](https://aka.ms/healthcaremodelstudio). 

## Related content

- [Model catalog and collections in Azure AI Studio](../model-catalog-overview.md)
- [How to deploy and inference a managed compute deployment with code](../deploy-models-managed.md)
- [Overview: Deploy models, flows, and web apps with Azure AI Studio](../../concepts/deployments-overview.md)