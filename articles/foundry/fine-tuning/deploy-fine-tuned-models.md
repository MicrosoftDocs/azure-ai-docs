---
title: Deploy fine-tuned models in Microsoft Foundry
titleSuffix: Microsoft Foundry
description: Deploy a fine-tuned model in the Microsoft Foundry portal with Serverless, Managed Compute, or Fireworks, then test and remove the deployment.
author: chillatom
ms.author: coreyhill
ms.reviewer: mopeakande
ms.service: microsoft-foundry
ms.subservice: foundry-model-inference
ms.topic: how-to
ms.date: 10/07/2026
ms.custom: doc-kit-assisted
ai-usage: ai-assisted
---

# Deploy fine-tuned models in Microsoft Foundry

Deploy your fine-tuned model in the Microsoft Foundry portal with Serverless, Managed Compute, or Fireworks on Foundry. Start with a fine-tuned model that's ready for deployment.

For deployment comparisons, model compatibility, and artifact requirements, see the [fine-tuning overview](overview.md#deployment-types) and its [supported models table](overview.md#supported-models).

## Prerequisites

- A fine-tuned model available in Foundry, with its model identifier and version.
- A [Foundry project](../how-to/create-projects.md) that supports the selected deployment option.
- The **Foundry Owner** role or a role with `Microsoft.CognitiveServices/accounts/deployments/write` on the target resource. Complete any additional provider setup listed in the example.
- Sufficient deployment quota or accelerator capacity in a supported region. Check [model availability](overview.md#supported-models).

## Deploy with Serverless

Deploy a compatible fine-tuned model with Serverless. Check the [fine-tuning overview](overview.md#supported-models) for the deployment types your model supports.

1. Open the [Foundry portal](https://ai.azure.com) and select your project.
1. Open the details view for your completed fine-tuning job, then select **Deploy**.
1. Choose **Serverless**.
1. Enter a name for your deployment.
1. Choose an available [deployment type](overview.md#deployment-options) based on your requirements, and configure capacity within your available quota.
1. Create the deployment, then monitor its progress on the **Models** page.

When deployment completes, open the [Foundry playground](#use-your-deployed-fine-tuned-model) and test your model.

[!INCLUDE [Managed Compute adapter procedure](../includes/fine-tuning-deploy-managed-compute.md)]

[!INCLUDE [Fireworks adapter procedure](../includes/fine-tuning-deploy-fireworks.md)]

## Use your deployed fine-tuned model

Test the deployment in the Foundry playground with a prompt representative of your task.

1. Open the **Playground** in your Foundry project.
1. Select the fine-tuned deployment you created, not the base-model deployment.
1. Send a test prompt and confirm that the model returns a response.

For repeatable evaluation, see [Run evaluations from the Foundry portal](../how-to/evaluate-generative-ai-app.md) or [Cloud evaluation with the Microsoft Foundry SDK](../observability/how-to/cloud-evaluation.md). To compare candidates, see [View evaluation results](../how-to/evaluate-results.md).

## Clean up your deployment

Remove the serving deployment when you no longer need it.

1. Open the **Models** page in the Foundry portal to find your deployment.
1. Select the deployment you created.
1. Select **Delete** and confirm the deletion.

Delete only the serving resources you created for this example.

## Related content

- [Fine-tuning overview](overview.md).
- [Run evaluations from the Foundry portal](../how-to/evaluate-generative-ai-app.md).
- [View evaluation results](../how-to/evaluate-results.md).
