---
title: Healthcare AI models in Microsoft Foundry
titleSuffix: Microsoft Foundry
description: Healthcare AI models in Microsoft Foundry for medical imaging workflows, available as pay-as-you-go serverless endpoints.
ms.service: microsoft-foundry
ms.subservice: foundry-model-inference
ms.topic: concept-article
ms.date: 06/10/2026
ms.reviewer: mehmetoez
reviewer: mertoezdev
ms.author: mopeakande
author: msakande
ms.custom: dev-focus
ai-usage: ai-assisted
---

# Foundation models for healthcare AI

[!INCLUDE [health-ai-models-meddev-disclaimer-preview](includes/health-ai-models-meddev-disclaimer-preview.md)]

[!INCLUDE [health-ai-models-intro](includes/health-ai-models-intro.md)]

## Premium healthcare AI models in Microsoft Foundry

Microsoft offers closed-weight, serverless premium models on Foundry that give healthcare organizations enterprise-grade medical imaging AI designed to support, *never replace*, qualified professionals. The models extend our open-source healthcare industry portfolio and are packaged for hospitals, ISVs, and partners who need higher-accuracy outputs, trusted Azure infrastructure, and predictable per-image economics, while keeping a human firmly in the loop on every clinically meaningful decision.

Premium healthcare AI models are **available for deployment as pay-as-you-go serverless endpoints** in Foundry. Microsoft manages the infrastructure, so you can focus on integrating models into your medical imaging workflows without provisioning or managing compute resources. The following sections cover the available premium healthcare AI models.

> [!NOTE]
> For foundation models available as managed compute deployments, see [Foundation models for healthcare AI (classic)](../../../foundry-classic/how-to/healthcare-ai/healthcare-ai-models.md).

### MedImageInsight Premium (preview)

MedImageInsight Premium (preview) is an embedding model for medical imaging that supports classification, similarity search, and image-text inference across radiology, pathology, ophthalmology, and dermatology. The model supports responsible AI (RAI) workflows, including out-of-distribution/outlier detection and drift monitoring, when you implement these controls in your application and monitoring pipeline. To learn about this model, see [Deploy and use MedImageInsight Premium (preview)](deploy-medimageinsight-premium.md).

### CxrReportGen Premium (preview)

CxrReportGen Premium (preview) is a multimodal model that generates structured draft findings from chest X-rays, incorporating current and prior images along with key patient information.  To learn about this model, see [CxrReportGen Premium (preview)](deploy-cxrreportgen-premium.md).

Both premium models are assistive only; all outputs require human review before clinical use.

## Partner models

[!INCLUDE [health-ai-models-partners](includes/health-ai-models-partners.md)]

## Related content

- [Healthcare AI examples (GitHub)](https://aka.ms/HealthcareAIExamples)
- [Model catalog and collections in Foundry portal](../../concepts/foundry-models-overview.md)
- [Deploy Microsoft Foundry Models in the Foundry portal](../../foundry-models/how-to/deploy-foundry-models.md)
- [Foundation models for healthcare AI (Open-Source)](../../../foundry-classic/how-to/healthcare-ai/healthcare-ai-models.md)
