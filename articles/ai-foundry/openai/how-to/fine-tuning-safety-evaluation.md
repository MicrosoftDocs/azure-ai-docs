---
title: 'Safety evaluation for fine-tuning (preview)'
titleSuffix: Azure OpenAI
description: Learn how the safety evaluation works for Microsoft Foundry fine-tuning.
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.custom: build-2023, build-2023-dataai, devx-track-python, references_regions
ms.topic: how-to
ms.date: 02/11/2026
author: ssalgadodev
ms.author: ssalgado
monikerRange: 'foundry-classic || foundry'
---

# Safety evaluation for fine-tuning (preview)

The advanced capabilities of fine-tuned models come with increased responsible AI challenges related to harmful content, manipulation, human-like behavior, privacy issues, and more. Learn more about risks, capabilities, and limitations in the [Overview of Responsible AI practices](/azure/ai-foundry/responsible-ai/openai/overview) and [Transparency Note](/azure/ai-foundry/responsible-ai/openai/transparency-note). To help mitigate the risks associated with advanced fine-tuned models, we have implemented additional evaluation steps to help detect and prevent harmful content in the training and outputs of fine-tuned models. These steps are grounded in the [Microsoft Responsible AI Standard](https://www.microsoft.com/ai/responsible-ai) and [Azure Microsoft Foundry Models content filtering](/azure/ai-foundry/openai/concepts/content-filter?tabs=warning%2Cpython-new).

- Evaluations are conducted in dedicated, customer specific, private workspaces;
- Evaluation endpoints are in the same geography as the Foundry resource;
- Training data isn't stored in connection with performing evaluations; only the final model assessment (deployable or not deployable) is persisted; and

Fine-tuned model evaluation filters are set to predefined thresholds and can't be modified by customers; they aren't tied to any custom content filtering configuration you might have created.

## Data evaluation

Before training starts, the service evaluates your data for potentially harmful content across the [harm categories](../concepts/content-filter-severity-levels.md#harm-category-descriptions) listed earlier. If harmful content is detected above the specified severity level, your training job fails, and you receive a message informing you of the categories of failure.

**Sample message:**

```output
The provided training data failed RAI checks for harm types: [hate_fairness, self_harm, violence]. Please fix the data and try again.
```

Your training data is evaluated automatically within your data import job as part of providing the fine-tuning capability.

If the fine-tuning job fails due to the detection of harmful content in training data, you won't be charged.

## Model evaluation

After training completes but before the fine-tuned model is available for deployment, the service evaluates the resulting model for potentially harmful responses using Azure's built-in [risk and safety metrics](/azure/ai-foundry/concepts/evaluation-metrics-built-in?tabs=warning#risk-and-safety-metrics). Using the same approach to testing used for the base large language models, the evaluation simulates a conversation with your fine-tuned model to assess the potential to output harmful content across the [harm categories](../concepts/content-filter-severity-levels.md#harm-category-descriptions) listed earlier.

If a model is found to generate output containing content detected as harmful at above an acceptable rate, you'll be informed that your model isn't available for deployment, with information about the specific categories of harm detected:

**Sample message:**

```output
This model is unable to be deployed. Model evaluation identified that this fine tuned model scores above acceptable thresholds for [Violence, Self Harm]. Please review your training data set and resubmit the job.
```

   :::image type="content" source="../media/fine-tuning/failure.png" alt-text="Screenshot of a failed fine-tuning job due to safety evaluation." lightbox="../media/fine-tuning/failure.png":::

As with data evaluation, the model is evaluated automatically within your fine-tuning job as part of providing the fine-tuning capability. Only the resulting assessment (deployable or not deployable) is logged by the service. If deployment of the fine-tuned model fails due to the detection of harmful content in model outputs, you won't be charged for the training run.

## Next steps

- To request modified content safety thresholds for fine-tuning, submit the [request form](https://customervoice.microsoft.com/Pages/ResponsePage.aspx?id=v4j5cvGGr0GRqy180BHbR7en2Ais5pxKtso_Pz4b1_xUMlBQNkZMR0lFRldORTdVQzQ0TEI5Q1ExOSQlQCN0PWcu).
- Explore the fine-tuning capabilities in the [Foundry fine-tuning tutorial](../tutorials/fine-tune.md).
- Review fine-tuning [model regional availability](../../foundry-models/concepts/models-sold-directly-by-azure.md?pivots=azure-openai#fine-tuning-models).
- Learn more about [Foundry quotas](../quotas-limits.md).
