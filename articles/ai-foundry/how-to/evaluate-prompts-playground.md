---
title: Manually Evaluate Prompts in Azure AI Foundry Portal Playground
titleSuffix: Azure AI Foundry
description: Learn how to quickly test and evaluate prompts in Azure AI Foundry portal playground.
manager: scottpolly
ms.service: azure-ai-foundry
ms.custom:
  - ignite-2023
  - build-2024
ms.topic: how-to
ms.date: 11/21/2024
ms.reviewer: mithigpe
ms.author: lagayhar
author: lgayhardt
---

# Manually evaluate prompts in Azure AI Foundry portal playground

[!INCLUDE [feature-preview](../includes/feature-preview.md)]

As you learn prompt engineering, you should test different prompts (*inputs*) one at a time to evaluate their effectiveness. This process can be very time intensive for several reasons. You need to check to make sure the content filters work appropriately, the response is accurate, and more.

To simplify this process, you can utilize manual evaluation in Azure AI Foundry portal. This evaluation tool enables you to use a single interface to continuously iterate and evaluate your prompt against your test data. You can also manually rate the model's responses (*outputs*) to help you gain confidence in your prompt.  

Manual evaluation can help you understand how your prompt is performing. You can then iterate on your prompt to ensure you reach your desired level of confidence.

In this article, you learn to:

* Generate your manual evaluation results.
* Rate your model responses.
* Iterate on your prompt and reevaluate.
* Save and compare results.
* Evaluate with built-in metrics.

## Prerequisites

* A test dataset in one of these formats: CSV or JSON Lines (JSONL). If you don't have a dataset available, you can also manually enter data from the UI.
* A deployment of one of these models: GPT 3.5, GPT 4, or Davinci. To learn more about how to create a deployment, see [Deploy models](./deploy-models-openai.md).

> [!NOTE]
> At this time, manual evaluation is only supported for Azure OpenAI models for chat and completion task types.

## Generate your manual evaluation results

From the **Playground**, select the **Manual evaluation** option to begin the process of manually reviewing the model responses based on your test data and prompt. Your prompt is automatically transitioned to your **Manual evaluation** file. You need to add test data to evaluate the prompt against. You can do this step manually by using the text boxes in the **Input** column.

You can also use the **Import Data** feature to select one of the existing datasets in your project, or upload a dataset in CSV or JSONL format. After loading your data, you'll be prompted to map the columns appropriately. After you finish and select **Import**, the data is populated in the appropriate columns.  

:::image type="content" source="../media/evaluations/prompts/generate-manual-evaluation-results.png" alt-text="Screenshot that shows how to generate manual evaluation results." lightbox= "../media/evaluations/prompts/generate-manual-evaluation-results.png":::

> [!NOTE]
> You can add as many as 50 input rows to your manual evaluation. If your test data has more than 50 input rows, only the first 50 upload to the input column.

Now that your data is added, you can select **Run** to populate the output column with the model's response.

## Rate your model's responses

You can rate the prompt's output by selecting a thumbs up or down for each response. Based on the ratings you provide, you can view these response scores in the at-a-glance summaries.  

:::image type="content" source="../media/evaluations/prompts/rate-results.png" alt-text="Screenshot that shows response scores in the at-a-glance summaries." lightbox= "../media/evaluations/prompts/rate-results.png":::

## Iterate on your prompt and reevaluate

Based on your summary, you might want to make changes to your prompt. You can edit your prompt setup by using the prompt controls mentioned previously. You can update the system message, change the model, edit the parameters, and more.

After making your edits, you can run them all again to update the entire table or run only specific rows again that didn't meet your expectations the first time.  

## Save and compare results

After populating your results, you can select **Save results**. By saving your results, you can share the progress with your team or continue your manual evaluation later.  

:::image type="content" source="../media/evaluations/prompts/save-and-compare-results.png" alt-text="Screenshot of the Save results selection." lightbox= "../media/evaluations/prompts/save-and-compare-results.png":::

You can also compare the thumbs up and down ratings across your manual evaluations. Save them, and then view them in the **Evaluation** tab under **Manual evaluation**.

## Related content

Learn more about how to evaluate your generative AI applications:

* [Evaluate your generative AI apps with the Azure AI Foundry portal or SDK](./evaluate-generative-ai-app.md)
* [View the evaluation results](./evaluate-results.md)

Learn more about [harm mitigation techniques](../concepts/evaluation-approach-gen-ai.md).
