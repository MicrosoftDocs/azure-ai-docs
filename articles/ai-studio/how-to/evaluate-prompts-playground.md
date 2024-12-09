---
title: How to manually evaluate prompts in Azure AI Foundry portal playground
titleSuffix: Azure AI Foundry
description: Quickly test and evaluate prompts in Azure AI Foundry portal playground.
manager: scottpolly
ms.service: azure-ai-studio
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

When you get started with prompt engineering, you should test different inputs one at a time to evaluate the effectiveness of the prompt can be very time intensive. This is because it's important to check whether the content filters are working appropriately, whether the response is accurate, and more. 

To make this process simpler, you can utilize manual evaluation in Azure AI Foundry portal, an evaluation tool enabling you to continuously iterate and evaluate your prompt against your test data in a single interface. You can also manually rate the outputs, the model's responses, to help you gain confidence in your prompt.  

Manual evaluation can help you get started to understand how well your prompt is performing and iterate on your prompt to ensure you reach your desired level of confidence. 

In this article you learn to: 
* Generate your manual evaluation results 
* Rate your model responses 
* Iterate on your prompt and reevaluate 
* Save and compare results 
* Evaluate with built-in metrics 

## Prerequisites 

To generate manual evaluation results, you need to have the following ready: 

* A test dataset in one of these formats: csv or jsonl. If you don't have a dataset available, we also allow you to input data manually from the UI.

* A deployment of one of these models: GPT 3.5 models, GPT 4 models, or Davinci models. To learn more about how to create a deployment, see [Deploy models](./deploy-models-openai.md).

> [!NOTE]
> Manual evaluation is only supported for Azure OpenAI models at this time for chat and completion task types.

## Generate your manual evaluation results 

From the **Playground**, select **Manual evaluation** to begin the process of manually reviewing the model responses based on your test data and prompt. Your prompt is automatically transitioned to your **Manual evaluation** and now you just need to add test data to evaluate the prompt against.  

This can be done manually using the text boxes in the **Input** column. 

You can also **Import Data** to choose one of your previous existing datasets in your project or upload a dataset that is in CSV or JSONL format. After loading your data, you'll be prompted to map the columns appropriately. Once you finish and select **Import**, the data is populated appropriately in the columns below.  

:::image type="content" source="../media/evaluations/prompts/generate-manual-evaluation-results.png" alt-text="Screenshot of generating manual evaluation results." lightbox= "../media/evaluations/prompts/generate-manual-evaluation-results.png":::

> [!NOTE]
> You can add as many as 50 input rows to your manual evaluation. If your test data has more than 50 input rows, we will upload the first 50 in the input column. 

Now that your data is added, you can **Run** to populate the output column with the model's response. 

## Rate your model responses 

You can provide a thumb up or down rating to each response to assess the prompt output. Based on the ratings you provided, you can view these response scores in the at-a-glance summaries.  

:::image type="content" source="../media/evaluations/prompts/rate-results.png" alt-text="Screenshot of response scores in the at-a-glance summaries." lightbox= "../media/evaluations/prompts/rate-results.png":::

## Iterate on your prompt and reevaluate 

Based on your summary, you might want to make changes to your prompt. You can use the prompt controls above to edit your prompt setup. This can be updating the system message, changing the model, or editing the parameters. 

After making your edits, you can choose to rerun all to update the entire table or focus on rerunning specific rows that didn't meet your expectations the first time.  

## Save and compare results 

After populating your results, you can **Save results** to share progress with your team or to continue your manual evaluation from where you left off later.  

:::image type="content" source="../media/evaluations/prompts/save-and-compare-results.png" alt-text="Screenshot of the save results." lightbox= "../media/evaluations/prompts/save-and-compare-results.png":::

You can also compare the thumbs up and down ratings across your different manual evaluations by saving them and viewing them in the Evaluation tab under Manual evaluation. 

## Next steps

Learn more about how to evaluate your generative AI applications:
- [Evaluate your generative AI apps with the Azure AI Foundry portal or SDK](./evaluate-generative-ai-app.md)
- [View the evaluation results](./evaluate-results.md)

Learn more about [harm mitigation techniques](../concepts/evaluation-improvement-strategies.md).
