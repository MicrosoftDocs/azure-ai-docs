---
title: Deploy and use CxrReportGen Premium in Foundry
titleSuffix: Microsoft Foundry
description: Deploy CxrReportGen Premium in Microsoft Foundry and send a test request to generate assistive draft findings from chest X-ray studies.
ms.service: microsoft-foundry
ms.subservice: foundry-model-inference
ms.topic: how-to
ms.date: 06/10/2026
ms.reviewer: mehmetoez
reviewer: mertoezdev
ms.author: mopeakande
author: msakande
ms.custom: dev-focus
ai-usage: ai-assisted
#customer intent: As a data scientist, I want to deploy CxrReportGen Premium and send a test request so that I can validate generated assistive chest X-ray findings in a human-reviewed workflow.

---

# Deploy and use CxrReportGen Premium (preview)

[!INCLUDE [health-ai-models-meddev-disclaimer-preview](includes/health-ai-models-meddev-disclaimer-preview.md)]

In this article, you deploy CxrReportGen Premium (preview) and send a test request to generate draft chest X-ray findings for qualified human review.

CxrReportGen Premium is an AI model checkpoint for building systems that draft structured radiology reports from chest X-ray inputs. The model provides assistive draft output. Treat generated findings as preliminary content that still requires appropriate testing, validation, monitoring, and human governance before use in clinical contexts. For more details about this mode, see [Learn more about the model](#learn-more-about-the-model).

> [!NOTE]
> Registration is required to use [CxrReportGen Premium](https://aka.ms/CXRRGV2Premium). Access will be granted according to Microsoft's eligibility criteria. To request access, submit [this form](https://aka.ms/microsoft/cxrreportgen-premium).

## Prerequisites

- An Azure subscription with access to Microsoft Foundry. If you don't have one, [create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- A Foundry project. If you don't have one, [create a project](../create-projects.md).
- Permission to view models and create or use deployments in your project.
- Access to deploy CxrReportGen Premium in the model catalog for your project. To request access, submit [this form](https://aka.ms/microsoft/cxrreportgen-premium).
- Required role-based access control for model deployment and endpoint use. For details, see [Role-based access control in Foundry portal](../../concepts/rbac-foundry.md).
- A test chest X-ray study and allowed metadata for evaluation.
- A client for test calls, such as REST tooling or an SDK-capable app environment.

## Deploy CxrReportGen Premium in Foundry

Deploy the model from the Foundry model catalog so that you can invoke it from
your application or test client.

1. [!INCLUDE [foundry-sign-in](../../includes/foundry-sign-in.md)]
1. Select your subscription and Foundry resource.
1. Select **Discover** > **Models**.
1. Search for **CxrReportGen Premium** and open the model card.
1. Select **Deploy**.
1. Review the available terms and deployment settings in your tenant.
1. Enter a deployment name and create the deployment.
1. Wait for deployment status to show **Succeeded**.
1. Copy the endpoint URL, deployment identifier, and authentication settings.

> [!NOTE]
> If deployment fails, check [Known issues in Microsoft Foundry](../../reference/foundry-known-issues.md) for current limitations and workarounds. Common causes include missing role assignments, region mismatch, and offer access that isn't enabled for your tenant.

## Test the deployment

After deployment succeeds, you can validate the endpoint by sending a test request with a chest X-ray image to generate draft findings.

### Sample request payload

CXRReportGen Premium exposes a `POST /v1/inference` endpoint that accepts a flat JSON body.

# [REST](#tab/rest)

```http
POST https://<your-endpoint>/v1/inference
Authorization: Bearer <your-api-key>
Content-Type: application/json

{
  "model": "CXRReportgen-Premium",
  "current_image": "<base64-encoded-image>"
}
```

# [Python](#tab/python)

```python
import base64
from pathlib import Path
import requests

url = "https://<your-endpoint>/v1/inference"
headers = {
    "Authorization": "Bearer <your-api-key>",
    "Content-Type": "application/json",
}

current_image_b64 = base64.b64encode(Path("current.png").read_bytes()).decode()

resp = requests.post(
    url,
    json={
        "model": "CXRReportgen-Premium",
        "current_image": current_image_b64,
    },
    headers=headers,
    timeout=120,
)
resp.raise_for_status()
print(resp.json()["findings"])
```

---

## Reference for REST API

[!INCLUDE [CxrReportGen Premium API reference](includes/cxr-api-reference.md)]

## Learn more about the model

CxrReportGen Premium is an AI model checkpoint for building systems that draft structured radiology reports from chest X-ray inputs. It integrates clinical context such as indication, technique, comparison study, and prior reports. It is purpose-built to slot into existing radiology workflows as a first-pass draft that a qualified clinician then reviews, corrects, and finalizes. The model is not a medical device and is not intended to deliver autonomous reports or to inform clinical decision-making on its own.

The Premium model is a closed-weight, [serverless](../../concepts/foundry-models-overview.md#serverless-deployments) offering with improved draft quality and expanded capabilities. For more information about differences between legacy and Premium models, see [Legacy and Premium healthcare models](https://aka.ms/HLSPremiumModels).

For license, transparency, and intended-use details, see the [CxrReportGen Premium model card](https://aka.ms/CXRRGV2Premium).

## Common use cases

Each of the following use cases assumes qualified human review as part of the workflow before any approval or action occurs.
- First-pass chest X-ray draft reports for a radiologist to edit and approve
- Structured findings extraction for downstream coding and reimbursement 
- Triage and prioritization signals in high-volume reading rooms 
- Resident and trainee feedback and quality review under attending supervision
- Embedding inside ISV radiology products that surface CxrReportGen drafts

:::image type="content" source="../../media/how-to/healthcare-ai/cxrreportgen-capabilities.gif" alt-text="Animated diagram that shows generations of findings from a chest x-ray." lightbox="../../media/how-to/healthcare-ai/cxrreportgen-capabilities.gif":::

> [!TIP]
> For runnable notebooks and code examples, see the [Healthcare AI Examples](https://aka.ms/HealthcareAIExamples) repository on GitHub.

## Review safety requirements

The model output is generated text findings, which can contain errors or
omissions.

CxrReportGen Premium is a model service, not a standalone clinical
application. It's intended for organizations and developers building
healthcare imaging solutions, including healthcare providers, independent
software vendors, systems integrators, partners, and enterprise AI teams. The
service is hosted and accessed by authenticated endpoints; customers don't
receive raw model weights.

Before implementation, define your workflow controls:

1. Out-of-the-box clinical use
2. Keep qualified professionals in the loop for review and sign-off.
3. Validate model and end-to-end workflow performance on representative data.
4. Require source-image review for clinically relevant decisions.
5. Maintain feedback and incident response paths for unexpected outputs.
6. Confirm privacy, security, retention, logging, and access controls for sensitive healthcare data.

Use CxrReportGen Premium only in assistive workflows with qualified human
review. It isn't intended for:

- Autonomous clinical decision-making.
- Producing final radiology reports without professional validation and sign-off.
- Use cases that require guarantees of perfect accuracy, completeness, or fairness.
- Emergency, triage, or time-critical workflows unless your organization has independently validated the complete workflow and implemented appropriate controls.
- Any workflow where errors or omissions in generated text could be acted on without mitigation.

## Data, privacy, and security considerations

CxrReportGen Premium might be used in workflows that involve sensitive
healthcare data, including medical images and associated text. You are
responsible for configuring and operating your applications to meet privacy,
security, compliance, and data governance obligations.

Use of CxrReportGen Premium is subject to the preview license and might
also be subject to other terms and conditions. For licensing information, see
the [CxrReportGen Premium model card](https://aka.ms/CXRRGV2Premium).

## Related content

- [Healthcare AI examples (GitHub)](https://aka.ms/HealthcareAIExamples)
- [How to use CxrReportGen healthcare AI model to generate grounded findings (classic)](../../../foundry-classic/how-to/healthcare-ai/deploy-CxrReportGen.md)
- [Customize a premium healthcare AI model with fine-tuning](fine-tune-premium-healthcare-models.md)
- [Model catalog and collections in Foundry portal](../../concepts/foundry-models-overview.md)
- [Authentication and authorization options in Foundry](../../concepts/rbac-foundry.md)
- [Integrate Microsoft Foundry with your applications](../integrate-with-other-apps.md)
