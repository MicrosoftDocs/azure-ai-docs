---
title: "Model deprecation and retirement for managed compute models (classic)"
description: "Learn about model lifecycle stages, deprecation timelines, replacements for models deployed via managed compute. (classic)"
ai-usage: ai-assisted
ms.service: microsoft-foundry
ms.subservice: foundry-model-inference
ms.topic: concept-article
ms.date: 04/23/2026
ms.author: mopeakande
manager: nitinme
author: msakande
ms.reviewer: rasavage
reviewer: rsavage2

#Customer intent: As a data scientist, I want to learn about the lifecycle of models that are available in the model catalog.
---

# Model deprecation and retirement for managed compute models (classic)

[!INCLUDE [classic-banner](../includes/classic-banner.md)]

Microsoft Foundry continuously refreshes its model catalog with newer, more capable models. As part of this process, model providers might deprecate and retire their older models, and you might need to update your applications to use a newer model.

## Model lifecycle stages

Models in the model catalog belong to one of these stages:

- Preview
- Generally available
- Legacy
- Deprecated
- Retired

### Preview

Models labeled _Preview_ are experimental in nature. A model's weights, runtime, and API schema can change while the model is in preview. Models in preview aren't guaranteed to become generally available. Models in preview have a _Preview_ label next to their name in the model catalog.  

### Generally available (GA)

This stage is the default model stage. Models that don't include a lifecycle label next to their name are GA and suitable for use in production environments. In this stage, model weights and APIs are fixed. However, model containers or runtimes with vulnerabilities might get patched, but patches don't affect model outputs.  
 
### Legacy

Models labeled _Legacy_ are intended for deprecation. You should plan to move to a different model, such as a new, improved model that might be available in the same model family. While a model is in the legacy stage, existing deployments of the model continue to work, and you can create new deployments of the model until the deprecation date.

### Deprecated

Models labeled _Deprecated_ are no longer available for new deployments. You can't create any new deployments for the model; however, existing deployments continue to work until the retirement date.

### Retired

Models labeled _Retired_ are no longer available for use. You can't create new deployments, and attempts to use existing deployments return `404` errors.

## Upcoming retirements for managed compute models

The following tables list the timelines for managed compute models that are on track for retirement. The lifecycle stages go into effect at 00:00:00 UTC on the specified dates.


#### Deci AI

| Model | Legacy date | Deprecation date | Retirement date | Suggested replacement model |
|-------|-------------------|------------------------|-----------------------|-----------------------------|
| [deci-decidiffusion-v1-0](https://ai.azure.com/explore/models/deci-decidiffusion-v1-0/version/7/registry/azureml/?cid=learnDocs) | March 16, 2026 | April 16, 2026 | July 31, 2026 | N/A |


#### Microsoft

| Model | Legacy date | Deprecation date | Retirement date | Suggested replacement model |
|-------|-------------------|------------------------|-----------------------|-----------------------------|
| [financial-reports-analysis](https://ai.azure.com/explore/models/financial-reports-analysis/version/2/registry/azureml/?cid=learnDocs) | March 16, 2026 | April 16, 2026 | July 31, 2026 | N/A |
| [financial-reports-analysis-v2](https://ai.azure.com/explore/models/financial-reports-analysis-v2/version/1/registry/azureml/?cid=learnDocs) | March 16, 2026 | April 16, 2026 | July 31, 2026 | N/A |
| [supply-chain-trade-regulations](https://ai.azure.com/explore/models/supply-chain-trade-regulations/version/3/registry/azureml/?cid=learnDocs) | March 16, 2026 | April 16, 2026 | July 31, 2026 | N/A |
| [supply-chain-trade-regulations-v2](https://ai.azure.com/explore/models/supply-chain-trade-regulations-v2/version/1/registry/azureml/?cid=learnDocs) | March 16, 2026 | April 16, 2026 | July 31, 2026 | N/A |


## Migrate to a replacement model

When a model you use enters the legacy or deprecated stage, follow these steps to migrate:

1. **Identify the replacement.** Check the **Suggested replacement model** column in the tables.
1. **Test the replacement.** Deploy the suggested replacement model and validate that it meets your application requirements, including output quality, latency, and cost.
1. **Update your deployments.** Create a new deployment with the replacement model and update your application code to point to the new deployment name.
1. **Delete the old deployment.** After you confirm the replacement works correctly, delete the deprecated model deployment to avoid unexpected `404` errors after retirement.

> [!TIP]
> Start migration as soon as a model enters the _Legacy_ stage. This gives you the maximum time to test and transition before the model is deprecated and new deployments are blocked.

## Related content

- [Deploy Microsoft Foundry Models to managed compute with pay-as-you-go billing (classic)](../how-to/deploy-models-managed-pay-go.md)
- [How to deploy and infer with a managed compute deployment (classic)](../how-to/deploy-models-managed.md)