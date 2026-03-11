---
title: Import custom models into Microsoft Foundry with Fireworks (preview)
description: Learn how to import, register, and deploy your own custom model weights in Microsoft Foundry using the Fireworks inference runtime.
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: how-to
ms.date: 03/11/2026
author: ssalgadodev 
ms.author: ssalgado
ms.custom: doc-kit-assisted, references_regions
---

<!-- markdownlint-disable MD025 -->
# Import custom models with Fireworks (preview)

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

Import and deploy your own model weights on Foundry using the Fireworks inference runtime.

In this article, you learn how to import, register, and deploy your own custom model weights in Microsoft Foundry. Custom model import (also known as *bring your own weights*) lets you run your proprietary or fine-tuned open-weight models within the Foundry ecosystem.

> [!NOTE]
> This custom model import guide uses the Fireworks on Foundry integration. For an overview of available catalog models, supported architectures, data privacy, and limitations, see [Use Fireworks models on Foundry](enable-fireworks-models.md).

The import workflow has four steps:

1. [**Prepare**](#model-requirements) your model files in a supported architecture.
1. [**Register**](#import-a-custom-model) the model in the Foundry portal.
1. [**Upload**](#verify-model-registration) model weights using the Azure Developer CLI.
1. [**Deploy**](#deploy-the-imported-model) the model to Fireworks inference infrastructure.

## Prerequisites

Before you begin, make sure your Azure environment is set up and that you have the required tools installed. To complete the steps in this article, you need the following resources and permissions:

* An Azure subscription. If you don't have one, create a [free account](https://azure.microsoft.com/free/).
* A [Foundry resource](/azure/ai-foundry/how-to/create-azure-ai-resource) with a [Foundry project](../../how-to/create-projects.md).
* The **Fireworks on Foundry** preview feature enabled in your subscription. For setup steps, see [Use Fireworks models on Foundry](enable-fireworks-models.md#enable-fireworks-on-foundry).
* The **Cognitive Services Contributor** role (or equivalent) on the Foundry resource to create and manage deployments. For more information, see [Azure role based access control](/azure/role-based-access-control/built-in-roles).
* [Azure Developer CLI](/azure/developer/azure-developer-cli/install-azd) (`azd`) installed locally. The import workflow uses `azd` to upload model weights.

## Region availability

Support for deploying custom models is available in all global [Azure regions](/azure/reliability/regions-list) except for Azure Government cloud environments.

## Model requirements

Custom models must match a supported architecture and include specific files for Foundry to register and deploy them. Review both requirements before starting the import process.

### Supported architectures

Custom models must be based on one of the following model architectures:

| Model Architecture | Versions |
| --- | --- |
| **DeepSeek** | V3.1, V3.2 |
| **Kimi** | K2, K2.5 |
| **GLM** | 4.7, 4.8 |
| **OpenAI** | gpt-oss-120b |
| **Qwen** | qwen3-14b |

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

    :::image type="content" source="../media/fireworks/add-custom-model.png" alt-text="Screenshot of the add a custom model page.":::

1. Configure the following settings:

   * **Model name**: Enter a descriptive name for your custom model.
   * **Base model architecture**: Select the model architecture that matches your model (for example, `DeepSeek V3.2` or `GLM 4.7`).

      :::image type="content" source="../media/fireworks/select-model-architecture.png" alt-text="Screenshot of the select model architecture window.":::

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

1. From the **Custom Models** list, select your custom model.

1. Select **Deploy**.

1. Configure the deployment:

   * **Deployment name**: provide a deployment name. During inference, this name is used in the `model` parameter to route requests to this deployment.
   * **Provisioned throughput units**: allocate the number of provisioned throughput units (PTUs) for the deployment. For more information, see [Provisioned throughput concepts](../../openai/concepts/provisioned-throughput.md).

1. Review and acknowledge the pricing terms.

1. Select **Deploy**.

When the deployment completes, the status shows **Succeeded** in your deployment list.

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
| Deployment fails | Confirm you have sufficient quota and that the [Fireworks preview feature](enable-fireworks-models.md#enable-fireworks-on-foundry) is enabled and registered in your subscription. |
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
