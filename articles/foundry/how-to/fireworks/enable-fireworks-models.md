---
title: Fireworks models on Microsoft Foundry (preview)
titleSuffix: Microsoft Foundry
description: Learn how to enable, deploy, and use Fireworks models in Microsoft Foundry, including catalog models, custom model import (BYOM), data privacy, and frequently asked questions.
author: ssalgadodev 
ms.author: ssalgado
manager: nitinme
ms.date: 03/11/2026
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: how-to
ms.custom: doc-kit-assisted
---

<!-- markdownlint-disable MD025 -->
# Fireworks models on Microsoft Foundry (preview)

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

Through integration with [Fireworks AI](https://fireworks.ai/), Microsoft Foundry customers can:

* **Experiment with the latest open-source models** often before they're available [directly from Azure](../../foundry-models/concepts/models-sold-directly-by-azure.md).
* **Import and deploy custom model weights** (bring your own model, or BYOM) onto Fireworks' on-demand GPU-backed infrastructure. For more information, see [Import custom models on Microsoft Foundry with Fireworks](import-custom-models.md).
* **Scale up** using [Provisioned throughput](../../openai/concepts/provisioned-throughput.md).

You can do all of this from your Foundry project while using Azure's governance, access controls, and project management.

## Prerequisites

* An Azure subscription. If you don't have one, create a [free account](https://azure.microsoft.com/free/).
* A [Foundry resource](/azure/ai-foundry/how-to/create-azure-ai-resource) with a [Foundry project](../../how-to/create-projects.md).
* An Azure identity with the **Subscription Owner** or **Subscription Contributor** role to enable the preview feature.
* To deploy models, you need the **Azure AI Developer** role or higher on the Foundry project. For more information, see [Azure built-in roles](/azure/role-based-access-control/built-in-roles#privileged).

## Region availability

Data Zone Standard deployments of models via Fireworks on Foundry are available in the following [Azure regions](/azure/reliability/regions-list):

* **East US** (eastus)
* **East US 2** (eastus2)
* **Central US** (centralus)
* **North Central US** (northcentralus)
* **West US** (westus)
* **West US 3** (westus3)

Global provisioned throughput deployments of base and custom models are available in all public [Azure regions](/azure/reliability/regions-list) with the exception of Azure Government cloud environments.

## Enable Fireworks on Foundry

While in preview, **Fireworks requires an administrator to enable the preview feature** within your Azure subscription.

1. Sign in to the [Azure portal](https://portal.azure.com).

1. In the search box, enter _subscriptions_ and select **Subscriptions**.

1. Select the link for your subscription's name.

1. From the left menu, under **Settings**, select **Preview features**.

1. Search for and select the **Fireworks.Enable.Deploy** preview feature.

1. Review the terms provided in the **Description** and the [data privacy](#data-privacy) section in this documentation.

1. If you don't agree to the terms, select **Close** and don't continue. Otherwise, select **Register**.

1. Select **OK**. The **Preview features** screen refreshes and the preview feature's **State** is displayed. It might take up to 30 minutes for the feature to enable for your subscription.

     > [!TIP]
     > To verify registration, refresh the **Preview features** page and confirm the **State** column shows **Registered** for the **Fireworks on Foundry** feature.


    :::image type="content" source="../media/fireworks/portal-preview-registration.png" alt-text="Screenshot of the Preview features setting in the Azure portal." lightbox="../media/fireworks/portal-preview-registration-lightbox.png":::

## Deploy Fireworks models from the Foundry portal

After the feature is enabled, you can deploy Fireworks models from the Foundry model catalog. Complete these steps to get a live endpoint for chat completions. Browse available models in the [Available catalog models](#available-catalog-models) section, or [import your own custom model](import-custom-models.md).

1. From the portal homepage, select **Discover** in the upper-right navigation.

1. In the left pane, select **Models** to open the Model catalog.

1. Select your desired Fireworks model to view its details on the model page:

   :::image type="content" source="../media/fireworks/models-homepage.png" alt-text="Screenshot of Foundry models homepage showing available Fireworks models.":::

1. On the model page, select **Deploy**. For more information on deployment options, see [Deploy Foundry Models in the portal](../../foundry-models/how-to/deploy-foundry-models.md).

1. In the deployment window, configure the following settings:

   * **Deployment name** â€” Keep the default name or enter a custom name to identify the deployment.
   * **Deployment type** â€” Select **Data Zone Standard** or **Global provisioned throughput**. For more information, see [Deployment types](../../foundry-models/concepts/deployment-types.md#deployment-type-comparison).
   * **Model version settings** â€” Select the model version for the deployment.
   * **Tokens per Minute Rate Limit** â€” Set a custom tokens-per-minute limit to manage costs and control usage. The default value is based on the model's typical performance and cost profile.
   * **Guardrails** â€” Select **DefaultV2** or **Default** guardrail configuration. By default, models are assigned the Microsoft.DefaultV2 guardrail. For more information, see [Use guardrails to set boundaries on model outputs](../../guardrails/guardrails-overview.md).

1. Select **Deploy**. The deployment process can take up to 30 minutes.

1. After deployment completes, use the provided endpoint and key to send inference requests to the model. To quickly test the deployment, use the **Playground** in your Foundry project.

   > [!TIP]
   > To verify the deployment, navigate to your project's **Deployments** page and confirm the deployment **Status** shows **Succeeded**.

## Available catalog models

The following Fireworks models are available in the Foundry model catalog:

| Model provider | Model name | Model ID | Type | Description |
| --- | --- | --- | --- | --- |
| **DeepSeek** | DeepSeek v3.2 | `FW-DeepSeek-v3.2` | Chat completions | Reasoning-optimized open-weight model for complex tasks. |
| **MiniMax** | MiniMax 2.5 | `FW-MiniMax-2.5` | Chat completions | General-purpose model for conversational and instruction-following tasks. |
| **Moonshot AI** | Kimi K2.5 | `FW-Kimi-K2.5` | Chat completions | Multimodal model with strong long-context capabilities. |
| **OpenAI** | gpt-oss-120b | `FW-gpt-oss-120b` | Chat completions | Large-scale open-weight model for broad generative tasks. |
| **Zhipu AI** | GLM-5 | `FW-GLM-5` | Chat completions | High-performance bilingual model for chat and reasoning. |

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
> Fireworks on Foundry is currently excluded from EU Data Boundary commitments.
>
> FedRAMP isn't achieved for Fireworks on Foundry. If your organization requires FedRAMP, before use, consult with your Authorization Official to determine if use of Fireworks on Foundry is allowed.
>
> Payment Card Industry (PCI) Data Security Standard (DSS) is not applicable to Fireworks on Foundry. You should not use Fireworks on Foundry to store, process, or transmit payment and cardholder data.

Consult the Fireworks AI [Trust Center](https://trust.fireworks.ai/) to review their Data Processing Addendum and certifications and their [Privacy Notice](https://fireworks.ai/privacy-policy) to understand their privacy commitment.

## Transparency note

Fireworks on Foundry allows customers to deploy and operate third-party and open-weight AI models using Microsoft Foundry platform services.

* Microsoft doesn't develop, train, fineâ€‘tune, or evaluate the safety, security, or Responsible AI characteristics of models deployed through Fireworks on Foundry.
* Microsoft makes no representations regarding the behavior, performance, or risk profile of these models.
* Customers are solely responsible for assessing the suitability of any model for their intended use, including performing any required safety, compliance, and Responsible AI evaluations, before deploying models in production or customer-facing applications.

Foundry provides the tools and best practices for performing your own [risk and safety evaluations](../../concepts/safety-evaluations-transparency-note.md) of models.

## Frequently asked questions

### Is Fireworks on Foundry available in Azure for US Government?

No, currently the Fireworks on Foundry service isn't available for Azure Government cloud users.

### How can I get quota for Fireworks model deployments?

Use the quota request [form](https://aka.ms/fireworks-quota) to request additional quota for Fireworks on Foundry.

### I have a Fireworks AI account. Can I use my existing Fireworks deployments?

No, you need to create new deployments in Foundry. If you'd like to shift consumption to Azure, contact your Fireworks account team to assist.

### Can I deploy LoRA or adapter-based models?

No, the current preview supports full-weight custom models only. LoRA and adapter-based models aren't supported at this time.

### Is the Fireworks preview suitable for production workloads?

No. As a public preview, Fireworks on Foundry doesn't include a production service-level agreement (SLA). The preview is intended for early testing, experimentation, and validation.

### How do I import and deploy a custom model?

Custom model import uses a CLI-first workflow with the [Azure Developer CLI](/azure/developer/azure-developer-cli/install-azd). For step-by-step instructions, see [Import custom models into Foundry](import-custom-models.md).

### How is Fireworks on Foundry billed?

Fireworks models deployed through Foundry support both [pay-per-token](https://aka.ms/fireworks-pricing) and [provisioned throughput](../../openai/concepts/provisioned-throughput.md) offers.

### How do I disable Fireworks in my Foundry project?

Fireworks can be disabled at the Azure subscription level. Follow the steps to [unregister preview features](/azure/azure-resource-manager/management/preview-features#unregister-preview-feature) in your Azure subscription.

## Troubleshoot Fireworks on Foundry

Use the following guidance to resolve common issues with Fireworks on Foundry.

| Issue | Resolution |
| --- | --- |
| **Preview registration stays in "Registering" state** | Registration can take up to 30 minutes. Refresh the **Preview features** page to check the current status. If the state doesn't change after 30 minutes, try unregistering and re-registering the feature. |
| **Fireworks models don't appear in the model catalog** | Confirm that the preview feature state shows **Registered** for your subscription. Verify you're working in a [supported region](#region-availability). |
| **Deployment fails with a quota error** | Use the [quota request form](https://aka.ms/fireworks-quota) to request additional capacity for Fireworks on Foundry. |
| **"Forbidden" or access denied during deployment** | Verify that your identity has the **Azure AI Developer** role or higher on the Foundry project. Subscription-level roles alone aren't sufficient for deployment. |
| **Model endpoint returns errors after deployment** | Confirm the deployment status shows **Succeeded** on the project's **Deployments** page. Verify you're using the correct **Target URI** and **Key** from the deployment details. |

For additional questions, see the [frequently asked questions](#frequently-asked-questions).

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
