---
title: Customize a premium healthcare AI model by fine-tuning it in Microsoft Foundry
titleSuffix: Microsoft Foundry
description: Learn how to fine-tune a premium healthcare AI model in Microsoft Foundry.
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
#customer intent: As a data scientist, I want to fine-tune a premium healthcare model so that I can improve model performance for my domain-specific use case.

---

# Customize a premium healthcare AI model with fine-tuning

Fine-tuning lets you adapt a premium healthcare AI model to your data and domain tasks. This article covers prerequisites and steps to create a fine-tuning job, with links to the core fine-tuning workflow in Microsoft Foundry.

[!INCLUDE [health-ai-models-meddev-disclaimer-preview](includes/health-ai-models-meddev-disclaimer-preview.md)]

## Prerequisites

- An Azure subscription. If you don't have one, [create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- A Foundry project in a region that supports your target fine-tuning model. If you don't have one, [create a project](../create-projects.md).
- Access to a [premium healthcare model](healthcare-ai-models.md) such as [MedImageInsight Premium (preview)](deploy-medimageinsight-premium.md) or [CxrReportGen Premium (preview)](deploy-cxrreportgen-premium.md) in the model catalog for your project.
- The **Foundry Owner** role, or a custom role that includes permissions to fine-tune and deploy models.
- Training and validation files in JSONL format, encoded as UTF-8 with BOM, and less than 512 MB per file.
- A healthcare data governance process that covers de-identification, retention, auditing, and access control.
- Review the core guidance before you train:
   - [Customize a model with fine-tuning](../../openai/how-to/fine-tuning.md)
   - [Microsoft Foundry fine-tuning considerations](../../openai/concepts/fine-tuning-considerations.md)
   - [Quotas and limits for Azure OpenAI in Foundry](../../openai/quotas-limits.md)

## Fine-tune a premium healthcare AI model

To create a fine-tuning job in the Foundry portal:

1. [!INCLUDE [foundry-sign-in](../../includes/foundry-sign-in.md)]
1. Select your subscription and Foundry resource.
1. Go to **Build** > **Fine-tune**, and select **Start fine-tuning**.
1. Select the premium healthcare model you want to customize. You can also select a previously fine-tuned model.
1. Choose the customization method that your selected model supports: **Supervised** for supervised fine-tuning (SFT), or **Direct Preference Optimization** (DPO), or **Reinforcement** for reinforcement fine-tuning (RFT).
1. Select the training type: **Standard** (in-region, data residency), or **Global** (lower cost, faster queue), or **Developer (preview)** (experimentation, preemptible).
1. Upload or select your training and validation datasets.
1. Optionally, configure a suffix, seed, and hyperparameters.
1. Select **Submit** to start the job.

After the job completes:

1. Review training metrics and checkpoints on the job details page.
1. Confirm safety evaluation status before deployment.
1. Select **Deploy** on the job details page to deploy the fine-tuned model.
1. Test with a representative validation set and keep qualified human reviewers in the workflow.

For the full fine-tuning workflow, including data preparation, format requirements, hyperparameter options, monitoring, and deployment, see [Customize a model with fine-tuning](../../openai/how-to/fine-tuning.md).

For model-specific fine-tuning details, including supported methods and training parameters, see the model card for your chosen model in the Foundry model catalog.

## Related content

- [Healthcare AI examples (GitHub)](https://aka.ms/HealthcareAIExamples)
- [Customize a model with fine-tuning](../../openai/how-to/fine-tuning.md)
- [Deploy a fine-tuned model](../../openai/how-to/fine-tuning-deploy.md)
- [Fine-tuning safety evaluation](../../openai/how-to/fine-tuning-safety-evaluation.md)
- [CxrReportGen Premium healthcare AI model](./deploy-cxrreportgen-premium.md)
- [MedImageInsight Premium healthcare AI model](./deploy-medimageinsight-premium.md)
