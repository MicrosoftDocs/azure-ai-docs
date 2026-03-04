---
title: Import custom models into Microsoft Foundry (preview)
description: Learn how to import and register your own custom models in Microsoft Foundry for deployment and inference.
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: how-to
ms.date: 03/03/2026
author: laujan
ms.author: davevoutila
ai-usage: ai-assisted
---
<!-- markdownlint-disable MD025 -->
# Import custom models into Microsoft Foundry (preview)

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

In this article, you learn how to import and register your own custom models in Microsoft Foundry. Importing custom models lets you bring your proprietary or fine-tuned models into Foundry for deployment, inference, and management alongside models from the Foundry model catalog.

## Prerequisites

* An Azure subscription. If you don't have one, create a [free account](https://azure.microsoft.com/free/).
* A [Foundry resource](/azure/ai-foundry/how-to/create-azure-ai-resource).
* [Azure Developer CLI](/azure/developer/azure-developer-cli/install-azd) (azd)

## Model prerequisites

Custom models in Foundry must correspond to the following model architectures:

* DeepSeek V3.1, V3.2
* Qwen2.5, Qwen2.5-VL, Qwen3
* Kimi K2, K2.5
* GLM 4.7, 4.8
* Llama 3, 3.1, 4
* OpenAI gpt-oss-120b

Custom models must also include the following files:

* Model configuration in `config.json`
* Model weights in one or many `*.safetensors` or `*.bin` files
* At least one weights index in `*.index.json`
* Tokenizer files, for example `tokenizer.model`, `tokenizer.json`, or `tokenizer_config.json`

## Import a custom model

1. From the Foundry portal homepage, select **Build** in the upper-right navigation, then **Models** in the left pane.

1. Select the **Custom Models** tab.

1. Select **Add a custom model**.

1. Configure the custom model `name` and select the appropriate `architecture`.

1. Copy the provided `azd` command and paste it into a terminal. Update the `--source` path to point to your custom model weights.

## Verify model registration

1. When the import completes successfully, refresh the **Custom Models** page.

1. Your imported custom model appears in the list.

## Deploy the imported model

1. Select your custom model.

1. Select **Deploy**.

1. Provide the model deployment a `name` and allocate provisioned throughput units.

1. Acknowledge the pricing terms.

1. Select **Deploy**.

## Related content

* [Deploy Foundry Models in the portal](../how-to/deploy-foundry-models.md)
* [Deploy Foundry Models using code](create-model-deployments.md)
* [Deployment types](../concepts/deployment-types.md)