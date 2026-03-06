---
title: Import custom models into Microsoft Foundry (preview)
description: Learn how to import, register, and deploy your own custom model weights in Microsoft Foundry using the Fireworks inference runtime.
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: how-to
ms.date: 03/04/2026
author: laujan
ms.author: davevoutila
ai-usage: ai-assisted
---

<!-- markdownlint-disable MD025 -->
# Import custom models with Fireworks (preview)

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

In this article, you learn how to import, register, and deploy your own custom model weights in Microsoft Foundry. Custom model import (also known as *bring your own model*) lets you run your proprietary or fine-tuned open-weight models within the Foundry ecosystem. [Fireworks AI](https://fireworks.ai/) handles inference on on-demand GPU-backed infrastructure, while Foundry provides governance, project management, and access controls.

> [!NOTE]
> This custom model import guide uses the Fireworks in Foundry integration. For an overview of available catalog models, supported architectures, data privacy, and limitations, see [Use Fireworks models in Foundry](use-fireworks-models.md).

The import workflow has four steps:

1. [**Prepare**](#model-requirements) your model files in a supported architecture.
1. [**Register**](#import-a-custom-model) the model in the Foundry portal.
1. [**Upload**](#verify-model-registration) model weights using the Azure Developer CLI.
1. [**Deploy**](#deploy-the-imported-model) the model to Fireworks inference infrastructure.

## Prerequisites

Before you begin, make sure your Azure environment is set up and that you have the required tools installed. To complete the steps in this article, you need the following resources and permissions:

* An Azure subscription. If you don't have one, create a [free account](https://azure.microsoft.com/free/).
* A [Foundry resource](/azure/ai-foundry/how-to/create-azure-ai-resource) with a [Foundry project](../../how-to/create-projects.md).
* The **Fireworks AI on Foundry** preview feature enabled in your subscription. For setup steps, see [Enable Fireworks on Foundry](use-fireworks-models.md#enable-fireworks-on-foundry).
* The **Cognitive Services Contributor** role (or equivalent) on the Foundry resource to create and manage deployments. For more information, see [Azure role based access control](/azure/role-based-access-control/built-in-roles).
* [Azure Developer CLI](/azure/developer/azure-developer-cli/install-azd) (`azd`) installed locally. The import workflow uses `azd` to upload model weights.

## Region availability

Fireworks on Foundry is available in the following [Azure regions](/azure/reliability/regions-list):

* **East US** (eastus)
* **East US 2** (eastus2)
* **Central US** (centralus)
* **North Central US** (northcentralus)
* **West US** (westus)
* **West US 3** (westus3)

## Model requirements

Custom models must match a supported architecture and include specific files for Foundry to register and deploy them. Review both requirements before starting the import process.

### Supported architectures

Custom models must be based on one of the following model architectures:
| **DeepSeek** | V3.1, V3.2 |
| **Kimi** | K2, K2.5 |
| **GLM** | 4.7, 4.8 |
| **OpenAI** | gpt-oss-120b |

### Required model files

Your model directory must include the following files:

| File | Description |
| --- | --- |
| `config.json` | Model configuration (architecture, hyperparameters). |
| `*.safetensors` or `*.bin` | One or more model weight files. |
| `*.index.json` | At least one weights index file that maps weight shards. |
| `tokenizer.model`, `tokenizer.json`, or `tokenizer_config.json` | Tokenizer files required for the model. |

> [!IMPORTANT]
> Only **full-weight models** with original quantization are supported. LoRA adapters or custom quantized models aren't currently supported in this preview.

## Import a custom model

The import process starts in the Foundry portal, where you register your model, and then uses the Azure Developer CLI to upload the model weights from your local machine.

1. Sign in to the [Foundry portal](https://ai.azure.com).

1. From the Foundry portal homepage, select **Build** in the upper-right navigation, then select **Models** in the left pane.

1. Select the **Custom Models** tab.

1. Select **Add a custom model**.

1. Configure the following settings:

* **Name**: Enter a descriptive name for your custom model.
* **Architecture**: Select the model architecture that matches your model (for example, `DeepSeek V3.2` or `Llama 4`).

1. The portal generates an `azd` command. Copy the command and paste it into a local terminal. Update the `--source` parameter to point to the directory that contains your model weight files.

   > [!TIP]
   > Make sure the directory you specify contains all the [required model files](#required-model-files). Missing files cause the import to fail.

1. Wait for the upload to complete. Upload time depends on the model size and your network bandwidth.

## Verify model registration

Once the upload finishes, confirm that Foundry successfully registered the model before proceeding to deployment.

1. Return to the Foundry portal and refresh the **Custom Models** page.

1. Confirm that your imported custom model appears in the list with a **Registered** status.

1. Select your model to review its details, including the architecture and file manifest.

## Deploy the imported model

With the model registered, you can deploy it to Fireworks' cloud for inference.

1. From the **Custom Models** list, select your custom model.

1. Select **Deploy**.

1. Configure the deployment:

   - **Deployment name** — Provide a deployment name. During inference, this name is used in the `model` parameter to route requests to this deployment.
   - **Provisioned throughput units** — Allocate the number of provisioned throughput units (PTUs) for the deployment. For more information, see [Provisioned throughput concepts](../../openai/concepts/provisioned-throughput.md).

1. Review and acknowledge the pricing terms.

1. Select **Deploy**.

When the deployment completes, the status shows **Succeeded** in your deployment list. You can test the deployment in the [Foundry Playground](../../concepts/concept-playgrounds.md) by sending prompts and reviewing responses.

## Troubleshooting

If you encounter issues during import or deployment, use the following table to identify common problems and resolutions.

| Issue | Resolution |
| --- | --- |
| Import fails with missing files | Verify your model directory contains all [required model files](#required-model-files), including `config.json`, weight files, an index file, and tokenizer files. |
| Architecture mismatch | Confirm the architecture you selected matches your model. See [supported architectures](#supported-architectures). |
| Upload times out or stalls | Check your network connection and retry. For large models, use a stable high-bandwidth connection. |
| Deployment fails | Confirm you have sufficient quota and that the [Fireworks preview feature](use-fireworks-models.md#enable-fireworks-on-foundry) is enabled and registered in your subscription. |
| Quota exceeded | [Request more quota](https://aka.ms/oai/stuquotarequest) or reallocate provisioned throughput units from existing deployments. |

## Related content

Explore the following resources to learn more about Fireworks models, deployment options, and authentication in Foundry.

* [Fireworks models in Foundry](use-fireworks-models.md)
* [Deploy Foundry Models in the portal](../../foundry-models/how-to/deploy-foundry-models.md)
* [Deploy models using Azure CLI and Bicep](../../foundry-models/how-to/create-model-deployments.md)
* [Deployment types](../../foundry-models/concepts/deployment-types.md)
* [Provisioned throughput concepts](../../openai/concepts/provisioned-throughput.md)
* [Configure keyless authentication with Microsoft Entra ID](../../foundry-models/how-to/configure-entra-id.md)
