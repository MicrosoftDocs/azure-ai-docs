---
title: "Hugging Face models in Microsoft Foundry (preview)"
description: "Learn how to discover and deploy Hugging Face models in Microsoft Foundry (preview), including project availability filtering, managed compute behavior, and classic fallback for unavailable models."
ms.service: microsoft-foundry
ms.subservice: foundry-models
ms.topic: how-to
ms.date: 06/16/2026
author: msakande
reviewer: ositanachi
ms.author: mopeakande
ms.reviewer: osiotugo
ms.custom:
  - classic-and-new
  - doc-kit-assisted
ai-usage: ai-assisted
#customer intent: As a developer, I want to understand how Hugging Face models are discovered and deployed in Microsoft Foundry so I can choose the right deployment path for my project.
---

# Hugging Face models in Microsoft Foundry (preview)

Hugging Face-published models are available in the Foundry model catalog for deployment in Microsoft Foundry. In the current Foundry experience, these models use managed compute.

In this article, you discover deployable Hugging Face models, deploy one with managed compute, and call the endpoint from your application.

In model discovery, use the **Available in my Project** filter to find the Hugging Face models that you can deploy in your current project. To see all Hugging Face-published models, set the availability filter to **All models**. If a model isn't currently available in Foundry, a **Continue in Foundry (classic)** button appears on the model card so you can deploy in Foundry (classic).

> [!IMPORTANT]
> Foundry managed compute is currently in preview. Preview features might not be available in all regions and are subject to supplemental terms. For more information, see [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).
>
> Hugging Face models in Foundry are globally available. For general service availability information by region, see [Azure products by region](https://azure.microsoft.com/explore/global-infrastructure/products-by-region/).

## Use Hugging Face models responsibly

Models sourced from Hugging Face are Non-Microsoft Products that aren't tested or evaluated by Microsoft. Before you deploy a model, ensure it's appropriate for your specific use case, including by evaluating any legal or export-control considerations and conducting your own model risk and safety evaluations. Learn about [Foundry risk and safety evaluations](../../concepts/safety-evaluations-transparency-note.md) and [Hugging Face security measures for models offered in Foundry](https://huggingface.co/docs/microsoft-azure/security).

> [!IMPORTANT]
> Models from Hugging Face are subject to third-party license terms available on the Hugging Face model details page. It's your responsibility to comply with the model's license terms.

## Prerequisites

- A Foundry project.
- The following role assignments on the Foundry account scope:
   - **Cognitive Services Contributor** (or **Foundry Owner** / **Foundry Account Owner**) to create, update, and delete managed compute deployments.
   - **Foundry User** to call the deployment with Microsoft Entra ID from the playground, SDK, or REST.
   For role definitions, see [Role-based access control in Foundry](../../concepts/rbac-foundry.md#managed-compute-control-plane-operations).
- Available GPU managed compute quota in your Azure subscription for the selected accelerator family. Foundry managed compute quota is separate from Azure VM quota and uses a different request path. In the [Foundry portal](https://ai.azure.com/nextgen), go to **Operate** > **Quota** > **Managed compute** > **Request quota** to check your current allocation or request an increase. For detailed guidance, see [Request more quota](../../how-to/deploy-models-managed.md#request-more-quota).

## Deploy a Hugging Face model

### Find and select the model

1. In the [Foundry portal](https://ai.azure.com/nextgen), go to **Discover** in the upper navigation bar, and then select **Models** in the left pane.

1. In the **Collections** filter, select **Hugging Face** to see available Hugging Face-published models.

1. Select the **Available in my Project** filter to see only models that you can currently deploy in your project and region.

1. In the **Deployment options** filter, select **Managed compute** to show only models available for managed compute deployment.

1. Select a model tile to open the model details card.

### Configure and deploy

1. On the model details card, select **Deploy**. This action opens the deployment configuration panel with default selections.

1. Enter a **Deployment name**. You need a deployment name and it can't contain a dot (`.`). Use only alphanumeric characters, underscores, and hyphens, and use 2 to 64 characters.

1. Select the **Deployment template**.

1. Select the **Accelerator type** that matches your model size and performance requirements. The portal prefilters available options to compatible accelerators.

1. Specify the **Instance count**:
   - Use 1 instance for testing and development.
   - Use 2 or more instances for production to ensure availability and handle traffic spikes.

1. Select **Deploy**. The deployment process typically takes several minutes. When it's done, the portal displays the deployment details page with:
   - The endpoint URL for invoking the model
   - API keys for authentication
   - Deployment status and logs

### Deploy with Python SDK (alternative)

If you prefer automation, use the Python management SDK to create the same managed compute deployment. Replace placeholders with values from your subscription and selected model.

To get values for `MODEL` and `TEMPLATE`, open the model details card and deployment wizard in the Foundry portal, and then copy the fully qualified registry asset IDs.

```bash
python -m pip install --upgrade azure-identity azure-mgmt-cognitiveservices openai
```

```python
from azure.identity import DefaultAzureCredential
from azure.mgmt.cognitiveservices import CognitiveServicesManagementClient

SUBSCRIPTION_ID = "<your-subscription-id>"
RESOURCE_GROUP = "<your-resource-group>"
ACCOUNT_NAME = "<your-foundry-account>"
DEPLOYMENT_NAME = "<your-deployment-name>"

MODEL = "azureml://registries/azure-huggingface/models/<model-id>/versions/<version>"
TEMPLATE = "azureml://registries/azure-huggingface/deploymenttemplates/<template-id>/labels/<label>"

client = CognitiveServicesManagementClient(
   DefaultAzureCredential(), SUBSCRIPTION_ID
)

deployment = client.managed_compute_deployments.begin_create_or_update(
   resource_group_name=RESOURCE_GROUP,
   account_name=ACCOUNT_NAME,
   deployment_name=DEPLOYMENT_NAME,
   resource={
      "sku": {"name": "GlobalManagedCompute", "capacity": 1},
      "properties": {
         "model": MODEL,
         "deploymentTemplate": TEMPLATE,
         "acceleratorType": "<accelerator-type>",
         "versionUpgradeOption": "OnceNewDefaultVersionAvailable",
      },
   },
).result()

print(f"State: {deployment.properties.provisioning_state}")
print(f"ID: {deployment.id}")
```

## Verify and use your deployment

After the deployment finishes, validate the endpoint before you integrate it into your application:

1. Confirm the deployment status is **Succeeded** on the deployment details page.

1. Run a test inference from the deployment details page to confirm that the model returns a successful response for your task type.

1. If deployment fails, review the deployment logs. Then, verify GPU quota and regional availability for the selected model and accelerator type. Foundry managed compute quota is separate from Azure VM quota. For quota checks and increase requests, see [Request more quota](../../how-to/deploy-models-managed.md#request-more-quota).

## Invoke the endpoint from your application

After verification succeeds, invoke your deployment through the unified Foundry endpoint base URL:

`https://<account>.services.ai.azure.com/openai/v1/`

In request bodies, set the `model` field to your **deployment name**, not the model ID.

### Python OpenAI SDK with Microsoft Entra ID

```python
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import OpenAI

ACCOUNT_NAME = "<your-foundry-account>"
DEPLOYMENT_NAME = "<your-deployment-name>"

token_provider = get_bearer_token_provider(
   DefaultAzureCredential(),
   "https://cognitiveservices.azure.com/.default",
)

client = OpenAI(
   base_url=f"https://{ACCOUNT_NAME}.services.ai.azure.com/openai/v1",
   api_key=token_provider,
)

response = client.chat.completions.create(
   model=DEPLOYMENT_NAME,
   messages=[{"role": "user", "content": "What is the capital of Nigeria?"}],
)

print(response.choices[0].message.content)
```

### Python OpenAI SDK with API key

```python
from azure.identity import DefaultAzureCredential
from azure.mgmt.cognitiveservices import CognitiveServicesManagementClient
from openai import OpenAI

SUBSCRIPTION_ID = "<your-subscription-id>"
RESOURCE_GROUP = "<your-resource-group>"
ACCOUNT_NAME = "<your-foundry-account>"
DEPLOYMENT_NAME = "<your-deployment-name>"

mgmt = CognitiveServicesManagementClient(
   DefaultAzureCredential(), SUBSCRIPTION_ID
)
api_key = mgmt.accounts.list_keys(RESOURCE_GROUP, ACCOUNT_NAME).key1

client = OpenAI(
   base_url=f"https://{ACCOUNT_NAME}.services.ai.azure.com/openai/v1",
   api_key=api_key,
)

response = client.chat.completions.create(
   model=DEPLOYMENT_NAME,
   messages=[{"role": "user", "content": "What is the capital of Nigeria?"}],
)

print(response.choices[0].message.content)
```

### Test the endpoint with cURL

Use a cURL request to validate your deployment outside the portal. Replace the endpoint URL, API key, and model name with your deployment values.

```bash
curl -X POST "https://<your-foundry-account>.services.ai.azure.com/openai/v1/chat/completions" \
   -H "Content-Type: application/json" \
   -H "api-key: <your-api-key>" \
   -d '{
      "messages": [{"role": "user", "content": "What is the capital of Nigeria?"}],
      "temperature": 0.2,
      "max_tokens": 256,
      "model": "<your-deployment-name>"
   }'
```

A successful response returns HTTP `200` and includes `choices[0].message.content`.

## How Hugging Face models work in Foundry

Hugging Face models in Foundry use the managed compute deployment path, which creates a dedicated GPU-backed endpoint for inference.

At a high level:

- You discover Hugging Face models in the model catalog.
- You filter to models that are deployable in your current project.
- You deploy a supported model; Foundry provisions dedicated GPU compute instances and exposes an endpoint.
- You invoke the deployment through the endpoint by using Foundry managed compute pricing.

Managed compute provides dedicated GPU compute instances, endpoint-based inference access, and billing through the Foundry Models Managed Compute pricing model. For current rates and billing details, see [Foundry Models pricing - Managed Compute](https://azure.microsoft.com/pricing/details/ai-foundry-models/microsoft/#pricing).

For deployment concepts, see [Managed compute in Microsoft Foundry](../../concepts/managed-compute-overview.md).

## Data hosting and model weights

For Hugging Face models available through Foundry, model weights are stored on Azure. This behavior differs from Hugging Face-published models in Foundry (classic) and Azure Machine Learning where model weights are downloaded from Hugging Face Hub at deployment.

## Discover deployable Hugging Face models

In the model catalog, use model filters to narrow discovery to Hugging Face-published models. To focus on models that you can deploy now, turn on **Available in my Project**.

When you enable this filter, the catalog shows only models that are currently deployable in your selected project context. A model appears in this filtered view when all of the following conditions are true:

- The model is in the Foundry model catalog.
- Your subscription has available GPU managed compute quota for at least one compatible accelerator type.
- The model is available in your project's Azure region.

If a model you expect to see doesn't appear, verify your quota and region coverage in Foundry before switching to Foundry (classic).

## Supported models

Foundry supports Hugging Face models that meet all of the following criteria:

- Must have the `Transformers`, `Diffusers`, or `Sentence-Transformers` tag on Hugging Face Hub.
- Have a permissive license (such as Apache 2.0, MIT, or OpenRAIL-M) that permits commercial use and redistribution.
- Have a [supported task](https://huggingface.co/docs/microsoft-azure/azure-ai/tasks) such as `chat-completion`, `image-to-text`, or `embeddings`.
- The model weights are in the Safetensors format and the model doesn't require `trust_remote_code`.

### Security requirements

Before deployment, all models in the Hugging Face collection undergo mandatory security scanning:

- **Malware scanning:** The process scans models to identify embedded malware or harmful binaries.
- **Code inspection:** The process disallows models that require `trust_remote_code=True` unless Hugging Face explicitly verifies them or they come from trusted organizations.
- **Safe format enforcement:** Model weights must be in Safetensors format to eliminate risks from pickle-based formats.
- **Validation checks:** The process tests all model, runtime, and accelerator combinations for API conformance and performance before publication.

For more details, see [Hugging Face security documentation](https://huggingface.co/docs/hub/en/security).


## Choose Foundry or Foundry (classic)

Use the following table to determine which experience fits your scenario:

| Scenario | Use |
| --- | --- |
| Model is available in your current project | Foundry |
| Model weights sourced directly from Azure | Foundry |
| Model is gated on Hugging Face Hub | Foundry (classic) |
| Model doesn't appear for your current project | Foundry (classic) |
| Model weights sourced directly from Hugging Face Hub | Foundry (classic) |

## When a model isn't available in Foundry

Some Hugging Face-published models might not be currently available in Foundry. When that happens, the model card displays a **Continue in Foundry (classic)** button. Select it to open the equivalent experience in Foundry (classic).

Foundry (classic) remains the fallback path for Hugging Face-published models that aren't available in the current Foundry project experience. For more details on managed compute deployment capabilities in the current Foundry experience, see [Managed compute in Microsoft Foundry](../../concepts/managed-compute-overview.md). You can also request a model through the [Hugging Face on Microsoft Foundry feedback portal](https://feedbackportal.microsoft.com/feedback/forum/58a369c8-4c59-f111-bec7-0022482aa60e).

To understand differences between the current and classic experiences, see [Migrate from the Foundry (classic) portal](../../how-to/navigate-from-classic.md).

## FAQ

### Are gated Hugging Face models available in Foundry?

No. Gated Hugging Face models aren't available in Foundry. Gated models require authentication and approval from the model author before use. Use Foundry (classic) for gated model support. See [Deploy models from Hugging Face Hub to managed compute (classic)](../../../foundry-classic/how-to/deploy-models-managed-hugging-face.md?context=/azure/foundry/context/context).

### Can I deploy Hugging Face models using CPU compute with managed compute?

Managed compute deployments for Hugging Face models use enterprise-grade GPU accelerators. If you need a different deployment path, consider Foundry (classic).

### What should I do if the model I want isn't available in Foundry?

See [When a model isn't available in Foundry](#when-a-model-isnt-available-in-foundry).

### How do I find only models that are deployable now?

In the model catalog, set the **Collections** filter to **Hugging Face**, set the **Deployment options** to **Managed compute**, and then enable the **Available in my Project** filter to see only models that are currently deployable in your project and region.

## Related content

- [Managed compute in Microsoft Foundry](../../concepts/managed-compute-overview.md)
- [Deploy models with managed compute (classic)](../../../foundry-classic/how-to/deploy-models-managed.md?context=/azure/foundry/context/context)
- [Foundry Models from partners and community](../concepts/models-from-partners.md)
- [Deployment overview for Microsoft Foundry Models](../../concepts/deployments-overview.md)
- [Deploy models from Hugging Face Hub to managed compute (classic)](../../../foundry-classic/how-to/deploy-models-managed-hugging-face.md?context=/azure/foundry/context/context)
- [Migrate from the Foundry (classic) portal](../../how-to/navigate-from-classic.md)
