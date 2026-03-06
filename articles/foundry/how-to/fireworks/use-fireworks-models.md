---
title: Fireworks models in Microsoft Foundry (preview)
titleSuffix: Microsoft Foundry
description: Learn about Fireworks models available in the Foundry model catalog, including catalog models, custom model import (BYOM), data privacy, and frequently asked questions.
author: laujan
ms.author: davevoutila
manager: nitinme
ms.date: 03/03/2026
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: conceptual
ai-usage: ai-assisted
---

<!-- markdownlint-disable MD025 -->
# Fireworks models in Foundry (preview)

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

Through integration with [Fireworks AI](https://fireworks.ai/), Microsoft Foundry customers can:

* **Experiment with the latest open-source models** before they're available [directly from Azure](../../foundry-models/concepts/models-sold-directly-by-azure.md).
* **Import and deploy custom model weights** (bring your own model, or BYOM) onto Fireworks' on-demand GPU-backed infrastructure. For more information, see [Import custom models into Foundry](import-custom-models.md).
* **Scale up** using [Provisioned throughput](../../openai/concepts/provisioned-throughput.md).

You can do all of this from your Foundry project while using Azure's governance, access controls, and project management.

## Prerequisites

- An Azure subscription. If you don't have one, create a [free account](https://azure.microsoft.com/free/).
- A [Foundry resource](/azure/ai-foundry/how-to/create-azure-ai-resource) with a [Foundry project](../../how-to/create-projects.md).
- An Azure identity with the **Subscription Owner** or **Subscription Contributor** role to enable the preview feature.

## Enable Fireworks on Foundry

While in preview, **Fireworks requires an administrator to enable the preview feature** within your Azure subscription.

1. Sign in to the [Azure portal](https://portal.azure.com).

1. In the search box, enter _subscriptions_ and select **Subscriptions**.

1. Select the link for your subscription's name.

1. From the left menu, under **Settings**, select **Preview features**.

1. Search for and select the **Fireworks on Foundry** preview feature.

1. Review the terms provided in the **Description** and the [data privacy](#data-privacy) section in this documentation.

1. If you don't agree to the terms, select **Close** and don't continue. Otherwise, select **Register**.

1. Select **OK**.

The **Preview features** screen refreshes and the preview feature's **State** is displayed. It might take up to 30 minutes for the feature to enable for your subscription.

> [!TIP]
> To verify registration, refresh the **Preview features** page and confirm the **State** column shows **Registered** for the **Fireworks on Foundry** feature.

After the feature is enabled, you can deploy Fireworks models from the Foundry model catalog. Browse available models in the [Available catalog models](#available-catalog-models) section, or [import your own custom model](import-custom-models.md).

## Available catalog models

The following Fireworks models are available in the Foundry model catalog:

| Model provider | Model name | Model ID | Type |
| --- | --- | --- | --- |
| **DeepSeek** | DeepSeek v3.2 | `FW-DeepSeek-v3.2` | Chat completions |
| **MiniMax** | MiniMax 2.5 | `FW-MiniMax-2.5` | Chat completions |
| **Moonshot AI** | Kimi K2.5 | `FW-Kimi-K2.5` | Chat completions |
| **OpenAI** | gpt-oss-120b | `FW-gpt-oss-120b` | Chat completions |
| **Zhipu AI** | GLM-5 | `FW-GLM-5` | Chat completions |

All catalog models support the [OpenAI/v1 API](https://aka.ms/openai/v1) for chat completions.

## Custom models (bring your own model)

In addition to the catalog models, Fireworks on Foundry supports importing and deploying your own custom model weights. This BYOM capability lets you run proprietary or fine-tuned open-weight models within the Foundry ecosystem, with inference provided by the optimized Fireworks cloud.

### Supported model architectures

Custom models must be based on one of the following supported architectures:

* **DeepSeek** (V3.1, V3.2)
* **Kimi** (K2, K2.5)
* **GLM** (4.7, 4.8)
* **OpenAI** gpt-oss-120b

### Limitations

* **Full-weight models only**. LoRA and adapter-based models aren't supported.
* **CLI-first workflow**. The import process uses the [Azure Developer CLI](/azure/developer/azure-developer-cli/install-azd) (`azd`). The Foundry portal supports registering, viewing, and deploying models after upload.
* **Fireworks Agents and Agent Builder workflows** are out of scope for this preview.

For step-by-step instructions, see [Import custom models into Foundry](import-custom-models.md).

## Data privacy

Fireworks model deployments made available via Foundry send inference traffic outside of Azure to the Fireworks AI cloud. Your Microsoft customer agreements (including the Product Terms and Microsoft's Data Protection Addendum) don't apply to your use of Fireworks services from within Microsoft Foundry.

> [!IMPORTANT]
> Because inference is performed on Fireworks infrastructure, review the Fireworks data handling policies before deploying models with sensitive data.

> [!NOTE]
> If your network restricts outbound traffic, ensure your firewall allows connectivity to the Fireworks AI inference endpoints.

Consult the Fireworks AI [Trust Center](https://trust.fireworks.ai/) to review their Data Processing Addendum and certifications and their [Privacy Notice](https://fireworks.ai/privacy-policy) to understand their privacy commitment.

## Frequently asked questions

### Is Fireworks on Foundry available in Azure for US Government?

No, currently the Fireworks service isn't available for Azure Government cloud users.

### How can I get quota for Fireworks model deployments?

We're updating the quota request [form](https://aka.ms/oai/stuquotarequest) to allow requesting quota for Fireworks on Foundry. In the meantime, contact your Azure account team.

### I have a Fireworks AI account. Can I use my existing Fireworks deployments?

No, you need to create new deployments in Foundry. If you'd like to shift consumption to Azure, contact your Fireworks account team to assist.

### Can I deploy LoRA or adapter-based models?

No, the current preview supports full-weight custom models only. LoRA and adapter-based models aren't supported at this time.

### Is the Fireworks preview suitable for production workloads?

No. As a public preview, Fireworks on Foundry doesn't include a production service-level agreement (SLA). The preview is intended for early testing, experimentation, and validation.

### How do I import and deploy a custom model?

Custom model import uses a CLI-first workflow with the [Azure Developer CLI](/azure/developer/azure-developer-cli/install-azd). For step-by-step instructions, see [Import custom models into Foundry](import-custom-models.md).

### How is Fireworks on Foundry billed?

Fireworks models deployed through Foundry support [provisioned throughput](../../openai/concepts/provisioned-throughput.md). During the preview, contact your Azure account team for specific pricing details.

### How do I disable Fireworks in my Foundry project?

Fireworks can be disabled at the Azure subscription level. Follow the steps to [unregister preview features](/azure/azure-resource-manager/management/preview-features#unregister-preview-feature) in your Azure subscription.

## Related content

* [Import custom models into Foundry](import-custom-models.md)
* [Deploy Foundry Models in the portal](../../foundry-models/how-to/deploy-foundry-models.md)
* [Foundry Models from partners and community](../../foundry-models/concepts/models-from-partners.md)
* [Foundry model catalog overview](../../foundry-models/concepts/models-sold-directly-by-azure.md)
* [Deployment types](../../foundry-models/concepts/deployment-types.md)
* [Provisioned throughput concepts](../../openai/concepts/provisioned-throughput.md)
* [Azure built-in roles](/azure/role-based-access-control/built-in-roles#privileged)
* [Azure preview features](/azure/azure-resource-manager/management/preview-features)
* [Fireworks AI Trust Center](https://trust.fireworks.ai/)
