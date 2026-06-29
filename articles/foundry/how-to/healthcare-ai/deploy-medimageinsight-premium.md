---
title: Deploy and use MedImageInsight Premium in Foundry
titleSuffix: Microsoft Foundry
description: Deploy MedImageInsight Premium in Microsoft Foundry and send a test request to generate medical image and text embeddings for evaluation workflows.
ms.service: microsoft-foundry
ms.subservice: foundry-model-inference
ms.topic: how-to
ms.date: 06/29/2026
ms.reviewer: mehmetoez
reviewer: mertoezdev
ms.author: mopeakande
author: msakande
ms.custom: dev-focus
ai-usage: ai-assisted

#customer intent: As a data scientist or developer, I want to deploy MedImageInsight Premium and send a test request so that I can validate image embedding generation for search, retrieval, and downstream evaluation.

---

# Deploy and use MedImageInsight Premium (preview)

[!INCLUDE [health-ai-models-meddev-disclaimer-preview](includes/health-ai-models-meddev-disclaimer-preview.md)]

In this article, you deploy MedImageInsight Premium (preview) and send a test request to generate medical image and text embeddings. MedImageInsight Premium generates rich, semantically meaningful embeddings of medical images across nine imaging modalities, including X-ray, CT, MRI, ultrasound, dermatology, ophthalmology, pathology, mammography.

MedImageInsight Premium provides assistive model output for medical imaging workflows. Treat embeddings, similarity scores, classifications, and retrieval results as workflow inputs that still require appropriate testing, validation, monitoring, and human governance before use in clinical contexts. For more details about the model, see [Learn more about the model](#learn-more-about-the-model).

> [!NOTE]
> Registration is required to use [MedImageInsight Premium](https://aka.ms/MI2Premium). Access will be granted according to Microsoft's eligibility criteria. To request access, submit [this form](https://aka.ms/microsoft/medimageinsight-premium).

## Prerequisites

- An Azure subscription with access to Microsoft Foundry. If you don't have one, [create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- A Foundry project. If you don't have one, [create a project](../create-projects.md).
- Permission to view models and create or use deployments in your project.
- Access to deploy MedImageInsight Premium in the model catalog for your project. To request access, submit [this form](https://aka.ms/microsoft/medimageinsight-premium).
- Required role-based access control for model deployment and endpoint use. For details, see [Role-based access control in Foundry portal](../../concepts/rbac-foundry.md).
- A test image or small test set for evaluation.
- A client for test calls, such as REST tooling or an SDK-capable app environment.

## Deploy MedImageInsight Premium in Foundry

Deploy the model from the Foundry model catalog so that you can invoke it from
your application or test client.

1. [!INCLUDE [foundry-sign-in](../../includes/foundry-sign-in.md)]
1. Select your subscription and Foundry resource.
1. Select **Discover** > **Models**.
1. Search for **MedImageInsight Premium** and open the model card.
1. Select **Deploy**.
1. Review the available terms and deployment settings in your tenant.
1. Enter a deployment name and create the deployment.
1. Wait for deployment status to show **Succeeded**.
1. Copy the endpoint URL, deployment identifier, and authentication settings.

> [!NOTE]
> If deployment fails, check [Known issues in Microsoft Foundry](../../reference/foundry-known-issues.md) for current limitations and workarounds. Common causes include missing role assignments, region mismatch, and offer access that isn't enabled for your tenant.

## Test the deployment

After deployment succeeds, you can validate the endpoint by sending test requests with text or image inputs to generate embeddings.

### Sample request payload

Send a `POST` to `/providers/microsoft/v2/embed` on your deployment URL. Use the `texts` field for text inputs or the `images` field for images encoded as base64 data URIs.

# [REST](#tab/rest)

```http
POST https://<your-endpoint>/providers/microsoft/v2/embed
Authorization: Bearer <your-api-key>
Content-Type: application/json

{
  "model": "MedImageInsight-Premium",
  "texts": ["x-ray chest anteroposterior Atelectasis."]
}
```

# [Python](#tab/python)

```python
import requests

url = "https://<your-endpoint>/providers/microsoft/v2/embed"
headers = {"Authorization": "Bearer <your-api-key>"}

resp = requests.post(
    url,
    json={
        "model": "MedImageInsight-Premium",
        "texts": ["x-ray chest anteroposterior Atelectasis."],
    },
    headers=headers,
    timeout=60,
)
resp.raise_for_status()
embeddings = resp.json()["embeddings"]["float"]
```

---

## Reference for REST API

[!INCLUDE [MedImageInsight Premium API reference](includes/mi2-api-reference.md)]

## Learn more about the model

MedImageInsight Premium (preview) generates rich, semantically meaningful embeddings of medical images across nine imaging modalities, including X-ray, CT, MRI, ultrasound, dermatology, ophthalmology, pathology, mammography. These embeddings power downstream workflows: similarity search, classification, outlier detection, drift monitoring, dataset curation, and multimodal retrieval-augmented generation. Outputs are intermediate signals that feed into a customer-built application; they are never a clinical determination on their own.

The premium model is a closed-weight, [serverless](../../concepts/foundry-models-overview.md#serverless-deployments) offering with expanded capabilities and improved performance. For more information about differences between legacy and Premium models, see [Legacy and Premium healthcare models](https://aka.ms/HLSPremiumModels).

For license, transparency, and intended-use details, see the [MedImageInsight Premium model card](https://aka.ms/MI2Premium).

## Common use cases

Each of the following use cases assumes qualified human review as part of the workflow before any approval or action occurs
- Image similarity search across hospital PACS archives
- Dataset curation and triage for AI/ML pipelines
- Outlier detection and study-level QA
- Drift monitoring for deployed imaging models
- Embedding-based classification for narrow downstream tasks (fracture detection, lesion characterization, modality routing)

:::image type="content" source="../../media/how-to/healthcare-ai/healthcare-embedding-capabilities.gif" alt-text="Animated diagram that shows an embedding model supporting similarity search and quality control scenarios." lightbox="../../media/how-to/healthcare-ai/healthcare-embedding-capabilities.gif":::

> [!TIP]
> For runnable code examples covering zero-shot classification, adapter training, outlier detection, and more, see the [Healthcare AI Examples](https://aka.ms/HealthcareAIExamples) repository on GitHub.

## Review safety requirements

MedImageInsight Premium (preview) generates embeddings for medical images and text in a shared latent space, suitable for similarity search, retrieval, and downstream classification workflows.

MedImageInsight Premium is a model service, not a standalone clinical
application. It's intended for organizations and developers building
healthcare imaging solutions, including healthcare providers, independent
software vendors, systems integrators, partners, enterprise AI teams, and data
science teams. The service is hosted and accessed by authenticated endpoints;
customers don't receive raw model weights.

Embedding outputs can support powerful workflows, but they don't provide
definitive clinical truth. Model performance can vary based on data
representativeness, modality, acquisition parameters, workflow design,
site-specific practice, prompt wording, preprocessing, image quality, and
distribution shift.

Before implementation, define your workflow controls:

1. Validate that the model is fit for your intended use, modalities, and data sources.
1. Keep appropriate human governance and review in workflows where outputs inform decisions.
1. Evaluate performance on representative data before use and after material workflow changes.
1. Monitor data drift, out-of-distribution behavior, quality, fairness, and operational performance over time.
1. Confirm privacy, security, retention, logging, and access controls for sensitive healthcare data.

Use MedImageInsight Premium only in assistive workflows with appropriate human
oversight. It isn't intended for:

- Out-of-the-box clinical use
- Autonomous clinical decision-making.
- Use without qualified human oversight where outputs inform health or medical decisions.
- Treating similarity scores, embeddings, classifications, or search results as definitive clinical truth without validation.
- Use cases that require guarantees of perfect accuracy, completeness, fairness, or stability across all populations, devices, sites, or imaging protocols.
- Emergency, triage, or time-critical workflows unless your organization has independently validated the complete workflow and implemented appropriate controls.
- Any workflow where model output could be acted on without mitigation for performance variability, drift, or data quality issues.

## Data, privacy, and security considerations

MedImageInsight Premium might be used in workflows that involve sensitive
healthcare data, including medical images and associated text. You are
responsible for configuring and operating your applications to meet privacy,
security, compliance, and data governance obligations.

Use of MedImageInsight Premium is subject to the preview license and might
also be subject to other terms and conditions. For licensing information, see
the [MedImageInsight Premium model card](https://aka.ms/MI2Premium).

## Related content

- [Healthcare AI examples (GitHub)](https://aka.ms/HealthcareAIExamples)
- [How to use MedImageInsight healthcare AI model for medical image embedding generation (classic)](../../../foundry-classic/how-to/healthcare-ai/deploy-medimageinsight.md)
- [Customize a premium healthcare AI model with fine-tuning](fine-tune-premium-healthcare-models.md)
- [Model catalog and collections in Foundry portal](../../concepts/foundry-models-overview.md)
- [Authentication and authorization options in Foundry](../../concepts/rbac-foundry.md)
- [Integrate Microsoft Foundry with your applications](../integrate-with-other-apps.md)
