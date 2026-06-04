---
title: Import custom models into Microsoft Foundry with Fireworks
description: Learn how to import, register, and deploy custom model weights, LoRA adapters, and speculative decoding draft models in Microsoft Foundry using the Fireworks inference runtime.
ms.service: microsoft-foundry
ms.subservice: foundry-model-inference
ms.topic: how-to
ms.date: 06/01/2026
author: ssalgadodev 
ms.author: ssalgado
ai-usage: ai-assisted
ms.custom: doc-kit-assisted, references_regions
---

<!-- markdownlint-disable MD025 -->
# Import custom models with Fireworks

Import and deploy your own model weights on Foundry using the Fireworks inference runtime.

In this article, you learn how to import, register, and deploy your own custom model weights in Microsoft Foundry. Custom model import (also known as *bring your own weights*) lets you run your proprietary or fine-tuned open-weight models within the Foundry ecosystem. You can also import LoRA adapters (preview) and draft models for speculative decoding (preview) when your base model and deployment type support those features.

LoRA adapters are lightweight fine-tuning artifacts that modify a base model without uploading a full copy of the model weights. Speculative decoding uses a smaller draft model to propose tokens that a target model verifies, which can reduce generation latency for supported workloads.

> [!NOTE]
> This custom model import guide uses the Fireworks on Foundry integration. For an overview of available catalog models, supported architectures, data privacy, and limitations, see [Use Fireworks models on Foundry](enable-fireworks-models.md).

<!-- -->

> [!IMPORTANT]
> Items marked (preview) in this article are currently in preview. This preview is provided without a service-level agreement, and we don't recommend it for production workloads. Certain features might not be supported or might have constrained capabilities. For more information, see [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).

The import workflow has five steps:

1. [**Prepare**](#model-requirements) your model, adapter, or draft model files.
1. [**Register**](#import-a-custom-model) the custom model asset in the Foundry portal.
1. [**Upload**](#verify-model-registration) the files using the generated Azure Developer CLI command.
1. [**Deploy**](#deploy-the-imported-model) the model, LoRA adapter (preview), or speculative decoding configuration (preview) to Fireworks inference infrastructure.
1. [**Test**](#test-your-deployment) the deployment in Foundry.

## Prerequisites

Before you begin, make sure your Azure environment is set up and that you have the required tools installed. To complete the steps in this article, you need the following resources and permissions:

* An Azure subscription. If you don't have one, create a [free account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
* A [Foundry resource](/azure/ai-foundry/how-to/create-azure-ai-resource) with a [Foundry project](../../how-to/create-projects.md).
* The **Cognitive Services Contributor** role or equivalent permissions on the Foundry resource to create and manage deployments. For more information, see [Azure role based access control](/azure/foundry/concepts/rbac-foundry#permissions-for-each-built-in-role).
* [Azure Developer CLI](/azure/developer/azure-developer-cli/install-azd) (`azd`) installed locally. The import workflow uses `azd` to upload model weights. To verify your installation, run `azd version` and `azd ai models create --help`.
* Azure Developer CLI authentication. Before running the generated upload command, sign in with `azd auth login`.

## Region availability

Support for deploying custom models is available in all global [Azure regions](/azure/reliability/regions-list) except for Azure Government cloud environments.

## Model requirements

Custom models must match a supported Fireworks model and include the files required for the model type you import. Review the supported models, file requirements, and preview constraints before starting the import process.

### Supported architectures

Custom models must be based on one of the following model architectures:

|Model Architecture|Versions|
|---|---|
|DeepSeek|v3.1, V4 Pro|
|Gemma|4 26B A4B IT, 4 31B IT|
|GLM|4.7, 5.1|
|Kimi|K2 Instruct 0905, K2 Thinking, K2.6|
|Llama|3.1 8B Instruct|
|Ministral|3 3B Instruct 2512|
|Qwen|3.5 9B, 3.5 35B A3B, 3.5 112B A10B, 3.5 397B|

### Required model files

Your model directory must include the files required for the model weight type you're importing.

| File | Full-weight model | LoRA adapter (preview) | Draft model for speculative decoding (preview) |
| --- | --- | --- | --- |
| `config.json` | Required | Not required; inherited from the base model | Required |
| `*.safetensors` or `*.bin` full weight files | Required | Not applicable | Required |
| `tokenizer.model`, `tokenizer.json`, or `tokenizer_config.json` | Required | Not required; inherited from the base model | Required |
| `adapter_config.json` | Not applicable | Required | Not applicable |
| `adapter_model.bin` or `adapter_model.safetensors` | Not applicable | Required | Not applicable |

## Import a custom model

The import process starts in the Foundry portal, where you register your model, and then uses the Azure Developer CLI to upload the model weights from your local machine.

1. Sign in to the [Foundry portal](https://ai.azure.com).

1. From the Foundry portal homepage, select **Build** in the upper-right navigation, then select **Models** in the left pane.

1. Select the **Models** tab.

1. Select **Generate upload command** instead.

1. Configure the following settings:

    | Setting | Description |
    | --- | --- |
    | **Base model** | Select the Fireworks base model or architecture that matches your model files. For LoRA adapters, select the base model that the adapter targets. For draft models, select the model family that matches the target model you plan to pair with the draft model. |
    | **Model details** | Enter the custom model name and version details. |
    | **Weight type** | Select **Full weight model**, **LoRA adapter** (preview), or **Draft model** (preview). The portal uses this selection to generate the appropriate CLI command and flags. |
    | **LoRA settings** | For LoRA adapters (preview), configure rank and alpha. Target modules and dropout are optional settings. |
    | **Model path** | Enter the local path to the folder that contains your model files. |

1. The portal generates an `azd` command. Copy the command and paste it into a local terminal. Update the `--source` parameter to point to the directory that contains your model weight files.

   > [!TIP]
   > Make sure the directory you specify contains all the [required model files](#required-model-files). Missing files cause the import to fail.

1. Wait for the upload to complete. Upload time depends on the model size and your network bandwidth. Large models (tens of gigabytes) can take a significant amount of time over standard connections.

## Verify model registration

After the upload finishes, confirm that Foundry successfully registered the model before proceeding to deployment.

1. Return to the Foundry portal and refresh the **Custom Models** page.

1. Confirm that your imported custom model appears in the list with a **Registered** status.

1. Select your model to review its details, including the architecture and file manifest.

## Deploy the imported model

With the model registered, you can deploy it to Fireworks' cloud for inference.

1. From the **Models** list, select your custom model.

1. Select **Deploy**.

1. Configure the deployment:

   * **Deployment name**: provide a deployment name. During inference, this name is used in the `model` parameter to route requests to this deployment.
   * **Provisioned throughput units**: allocate the number of provisioned throughput units (PTUs) for the deployment. For more information, see [Provisioned throughput concepts](../../openai/concepts/provisioned-throughput.md).

1. Review and acknowledge the pricing terms.

1. Select **Deploy**.

When the deployment completes, the status shows **Succeeded** in your deployment list.

> [!NOTE]
> You can only have one active deployment of the same imported custom model at a time in a given project.

### Deploy with speculative decoding (preview)

Speculative decoding pairs a target model with a same-family, architecture-compatible draft model to reduce token generation latency during decoding.
It does not improve context processing latency in the prefill phase, so workloads with long inputs and short outputs may see limited benefit.

To deploy a draft model, select the registered draft model, and then select **Deploy**. Configure the deployment name, select a **Target model** from **the same model family** as the draft model, set the draft token count, choose the deployment type, configure PTU capacity, review the pricing terms, and deploy.

### Deployment examples

Use the following examples to automate parts of the deployment workflow after the custom model is registered. Each example deploys the custom model with `80` units of Global Provisioned throughput. Be sure to replace any placeholders with your details.

#### [REST API](#tab/rest-api)

```http
PUT https://management.azure.com/subscriptions/{subscription-id}/resourceGroups/{resource-group}/providers/Microsoft.CognitiveServices/accounts/{foundry-account}/deployments/{deployment-name}?api-version=2025-06-01
Authorization: Bearer <access-token>
Content-Type: application/json
```

```json
{
  "sku": {
    "name": "GlobalProvisionedManaged",
    "capacity": 80
  },
  "properties": {
    "model": {
      "name": "<registered-model-name>",
      "format": "FireworksCustom",
      "version": "1",
      "source": "/subscriptions/{subscription-id}/resourceGroups/{resource-group}/providers/Microsoft.CognitiveServices/accounts/{foundry-account}/projects/{foundry-project}"
    }
  }
}
```

#### [PowerShell](#tab/powershell)

```powershell
az cognitiveservices account deployment create `
  --name "<foundry-resource-name>" `
  --resource-group "<resource-group>" `
  --deployment-name "<deployment-name>" `
  --model-name "<registered-model-name>" `
  --model-version "1" `
  --model-format "FireworksCustom" `
  --model-source "/subscriptions/{subscription-id}/resourceGroups/{resource-group}/providers/Microsoft.CognitiveServices/accounts/{foundry-account}/projects/{foundry-project}" `
  --sku-name "GlobalProvisionedManaged" `
  --sku-capacity 80
```

#### [Bash](#tab/bash)

```bash
az cognitiveservices account deployment create \
  --name "<foundry-resource-name>" \
  --resource-group "<resource-group>" \
  --deployment-name "<deployment-name>" \
  --model-name "<registered-model-name>" \
  --model-version "1" \
  --model-format "FireworksCustom" \
  --model-source "/subscriptions/{subscription-id}/resourceGroups/{resource-group}/providers/Microsoft.CognitiveServices/accounts/{foundry-account}/projects/{foundry-project}" \
  --sku-name "GlobalProvisionedManaged" \
  --sku-capacity 80
```

---

### Test your deployment

After the deployment succeeds, verify it works by sending a test request:

1. Open the [Foundry Playground](../../concepts/concept-playgrounds.md).
1. Select your custom model deployment from the model list.
1. Send a test prompt and confirm the model returns a valid response.

## Troubleshooting

If you encounter issues during import or deployment, use the following table to identify common problems and resolutions.

| Issue | Resolution |
| --- | --- |
| Import fails with missing files | Verify your model directory contains all [required model files](#required-model-files), including `config.json`, weight files, an index file, and tokenizer files. |
| Architecture mismatch | Confirm the architecture you selected matches your model. See [supported architectures](#supported-architectures). |
| Upload times out or stalls | Check your network connection and retry. For large models, use a stable high-bandwidth connection. |
| Deployment fails | Confirm you have sufficient quota and that Fireworks on Foundry is available in your [supported region](enable-fireworks-models.md#region-availability). |
| Speculative decoding draft model isn't available | Confirm that the draft model is registered in the same project and that the draft model and target model are in the same model family and architecture-compatible. |
| Quota exceeded | [Request more quota](https://aka.ms/fireworks-quota) or reallocate provisioned throughput units from existing deployments. |

For more troubleshooting guidance, see [Troubleshoot Fireworks on Foundry](enable-fireworks-models.md#troubleshoot-fireworks-on-foundry).

## Related content

Explore the following resources to learn more about Fireworks models, deployment options, and authentication on Foundry.

* [Fireworks models on Foundry](enable-fireworks-models.md)
* [Deploy Foundry Models in the portal](../../foundry-models/how-to/deploy-foundry-models.md)
* [Deploy models using Azure CLI and Bicep](../../foundry-models/how-to/create-model-deployments.md)
* [Deployment types](../../foundry-models/concepts/deployment-types.md)
* [Provisioned throughput concepts](../../openai/concepts/provisioned-throughput.md)
* [Configure keyless authentication with Microsoft Entra ID](../../foundry-models/how-to/configure-entra-id.md)
