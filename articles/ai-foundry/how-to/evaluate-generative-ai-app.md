---
title: Evaluate Generative AI Models and Apps with Azure AI Foundry
titleSuffix: Azure AI Foundry
description: Evaluate your generative AI models and applications by using Azure AI Foundry.
manager: scottpolly
ms.service: azure-ai-foundry
ms.custom: ignite-2023, references_regions, build-2024, ignite-2024
ms.topic: how-to
ms.date: 05/19/2025
ms.reviewer: mithigpe
ms.author: lagayhar
author: lgayhardt
---

# Evaluate generative AI models and applications by using Azure AI Foundry

If you want to thoroughly assess the performance of your generative AI models and applications when applied to a substantial dataset, you can initiate an evaluation process. During this evaluation, your model or application is tested with the given dataset, and its performance is quantitatively measured with both mathematical-based metrics and AI-assisted metrics. This evaluation run provides you with comprehensive insights into the application's capabilities and limitations.

To carry out this evaluation, you can use the evaluation functionality in the Azure AI Foundry portal, a comprehensive platform that offers tools and features for assessing the performance and safety of your generative AI model. In the Azure AI Foundry portal, you're able to log, view, and analyze detailed evaluation metrics.

In this article, you learn to create an evaluation run against a model or a test dataset with built-in evaluation metrics from the Azure AI Foundry UI. For greater flexibility, you can establish a custom evaluation flow and employ the  **custom evaluation** feature. You can also use the **custom evaluation** feature to conduct a batch run without any evaluation.

## Prerequisites

- A test dataset in one of these formats: CSV or JSON Lines (JSONL).
- An Azure OpenAI connection. A deployment of one of these models: a GPT-3.5 model, a GPT-4 model, or a Davinci model. Required only when you run AI-assisted quality evaluations.

## Create an evaluation with built-in evaluation metrics

An evaluation run allows you to generate metric outputs for each data row in your test dataset. You can select one or more evaluation metrics to assess the output from different aspects. You can create an evaluation run from the evaluation or model catalog pages in the Azure AI Foundry portal. An evaluation creation wizard appears and shows you how to set up an evaluation run.

### From the evaluate page

From the collapsible left menu, select **Evaluation** > **Create a new evaluation**.

:::image type="content" source="../media/evaluations/evaluate/create-new-evaluation.png" alt-text="Screenshot of the button to create a new evaluation." lightbox="../media/evaluations/evaluate/create-new-evaluation.png":::

### From the model catalog page

1. From the collapsible left menu, select **Model catalog**.
1. Go to the model.
1. Select the **Benchmarks** tab.
1. Select **Try with your own data**. This selection opens the model evaluation panel, where you can create an evaluation run against your selected model.  

   :::image type="content" source="../media/evaluations/evaluate/try-with-your-own-data.png" alt-text="Screenshot of the Try with your own data button from the model catalog page." lightbox="../media/evaluations/evaluate/try-with-your-own-data.png":::

#### Evaluation target

When you start an evaluation from the **Evaluate** page, you first need to choose the evaluation target. By specifying the appropriate evaluation target, we can tailor the evaluation to the specific nature of your application, ensuring accurate and relevant metrics. We support two types of evaluation targets:  

- **Fine-tuned model**: This choice evaluates the output generated by your selected model and user-defined prompt.
- **Dataset**: Your model-generated outputs are already in a test dataset.

:::image type="content" source="../media/evaluations/evaluate/select-evaluation-target.png" alt-text="Screenshot of the evaluation target selection." lightbox="../media/evaluations/evaluate/select-evaluation-target.png":::

#### Configure test data

When you enter the evaluation creation wizard, you can select from preexisting datasets or upload a new dataset to evaluate. The test dataset needs to have the model-generated outputs to be used for evaluation. A preview of your test data is shown on the right pane.

- **Choose existing dataset**: You can select the test dataset from your established dataset collection.

    :::image type="content" source="../media/evaluations/evaluate/use-existing-dataset.png" alt-text="Screenshot of the option to select test data when creating a new evaluation." lightbox="../media/evaluations/evaluate/use-existing-dataset.png":::

- **Add new dataset**: Upload files from your local storage. Only CSV and JSONL file formats are supported. A preview of your test data displays on the right pane.

    :::image type="content" source="../media/evaluations/evaluate/upload-file.png" alt-text="Screenshot of the upload file option that you can use when creating a new evaluation." lightbox="../media/evaluations/evaluate/upload-file.png":::

#### Configure testing criteria

We support three types of metrics curated by Microsoft to facilitate a comprehensive evaluation of your application:  

- **AI quality (AI assisted)**: These metrics evaluate the overall quality and coherence of the generated content. You need a model deployment as judge to run these metrics.
- **AI quality (NLP)**: These natural language processing (NLP) metrics are mathematical-based, and they also evaluate the overall quality of the generated content. They often require ground truth data, but they don't require a model deployment as judge.
- **Risk and safety metrics**: These metrics focus on identifying potential content risks and ensuring the safety of the generated content.

:::image type="content" source="../media/evaluations/evaluate/testing-criteria.png" alt-text="Screenshot that shows how to add testing criteria." lightbox="../media/evaluations/evaluate/testing-criteria.png":::

As you add your testing criteria, different metrics are going to be used as part of the evaluation. You can refer to the table for the complete list of metrics we offer support for in each scenario. For more in-depth information on metric definitions and how they're calculated, see [What are evaluators?](../concepts/observability.md#what-are-evaluators).

| AI quality (AI assisted) | AI quality (NLP) | Risk and safety metrics |
|--|--|--|
| Groundedness, Relevance, Coherence, Fluency, GPT similarity | F1 score, ROUGE score, BLEU score, GLEU score, METEOR score| Self-harm-related content, Hateful and unfair content, Violent content, Sexual content, Protected material, Indirect attack  |

When you run AI-assisted quality evaluation, you must specify a GPT model for the calculation/grading process.

:::image type="content" source="../media/evaluations/evaluate/select-metrics-ai-quality-ai-assisted.png" alt-text="Screenshot that shows the Likert-scale evaluator with the AI quality (AI assisted) metrics listed in presets." lightbox="../media/evaluations/evaluate/select-metrics-ai-quality-ai-assisted.png":::

AI Quality (NLP) metrics are mathematically based measurements that assess your application's performance. They often require ground truth data for calculation. ROUGE is a family of metrics. You can select the ROUGE type to calculate the scores. Various types of ROUGE metrics offer ways to evaluate the quality of text generation. ROUGE-N measures the overlap of n-grams between the candidate and reference texts.  

:::image type="content" source="../media/evaluations/evaluate/select-metrics-ai-quality-nlp.png" alt-text="Screenshot that shows text similarity with the AI quality (NLP) metrics listed in presets." lightbox="../media/evaluations/evaluate/select-metrics-ai-quality-nlp.png":::

For risk and safety metrics, you don't need to provide a deployment. The Azure AI Foundry portal provisions a GPT-4 model that can generate content risk severity scores and reasoning to enable you to evaluate your application for content harms.

> [!NOTE]
> AI-assisted risk and safety metrics are hosted by Azure AI Foundry safety evaluations and are available only in the following regions: East US 2, France Central, UK South, Sweden Central.

:::image type="content" source="../media/evaluations/evaluate/safety-metrics.png" alt-text="Screenshot that shows the metric Violent content, which is one of the risk and safety metrics." lightbox="../media/evaluations/evaluate/safety-metrics.png":::

[!INCLUDE [FDP-backward-compatibility-azure-openai](../includes/fdp-backward-compatibility-azure-openai.md)]

#### Data mapping

Data mapping for evaluation: For each metric added, you must specify which data columns in your dataset correspond with the inputs that are needed in the evaluation. Different evaluation metrics demand distinct types of data inputs for accurate calculations.

During evaluation, the model’s response is assessed against key inputs such as:

- **Query**: Required for all metrics.
- **Context**: Optional.
- **Ground truth**: Optional, required for AI quality (NLP) metrics.

These mappings ensure accurate alignment between your data and the evaluation criteria.

:::image type="content" source="../media/evaluations/evaluate/test-criteria-data-mapping.png" alt-text="Screenshot of the query, context, and ground truth mapping to your evaluation input." lightbox="../media/evaluations/evaluate/test-criteria-data-mapping.png":::

##### Query and response metric requirements

For guidance on the specific data mapping requirements for each metric, refer to the information provided in the table:

| Metric                     | Query         | Response      | Context       | Ground truth  |
|----------------------------|---------------|---------------|---------------|---------------|
| Groundedness               | Required: Str | Required: Str | Required: Str | Doesn't apply           |
| Coherence                  | Required: Str | Required: Str | Doesn't apply          | Doesn't apply           |
| Fluency                    | Required: Str | Required: Str | Doesn't apply           | Doesn't apply           |
| Relevance                  | Required: Str | Required: Str | Required: Str | Doesn't apply           |
| GPT-similarity             | Required: Str | Required: Str | Doesn't apply           | Required: Str |
| F1 score                   | Doesn't apply           | Required: Str | Doesn't apply           | Required: Str |
| BLEU score                 | Doesn't apply           | Required: Str | Doesn't apply           | Required: Str |
| GLEU score                 | Doesn't apply           | Required: Str | Doesn't apply           | Required: Str |
| METEOR score               | Doesn't apply           | Required: Str | Doesn't apply           | Required: Str |
| ROUGE score                | Doesn't apply           | Required: Str | Doesn't apply           | Required: Str |
| Self-harm-related content  | Required: Str | Required: Str | Doesn't apply           | Doesn't apply           |
| Hateful and unfair content | Required: Str | Required: Str | Doesn't apply           | Doesn't apply           |
| Violent content            | Required: Str | Required: Str | Doesn't apply           | Doesn't apply           |
| Sexual content             | Required: Str | Required: Str | Doesn't apply           | Doesn't apply           |
| Protected material         | Required: Str | Required: Str | Doesn't apply           | Doesn't apply           |
| Indirect attack            | Required: Str | Required: Str | Doesn't apply           | Doesn't apply           |

- **Query**: A query seeking specific information.  
- **Response**: The response to a query generated by the model.
- **Context**: The source that the response is based on. (Example: grounding documents.)
- **Ground truth**: A query response generated by a human user that serves as the true answer.

#### Review and finish

After you complete all the necessary configurations, you can provide an optional name for your evaluation. Then you can review and select **Submit** to submit the evaluation run.

:::image type="content" source="../media/evaluations/evaluate/review-and-finish.png" alt-text="Screenshot that shows the review page to create a new evaluation." lightbox="../media/evaluations/evaluate/review-and-finish.png":::

### Fine-tuned model evaluation

To create a new evaluation for your selected model deployment, you can use a GPT model to generate sample questions, or you can select from your established dataset collection.

:::image type="content" source="../media/evaluations/evaluate/select-data-source.png" alt-text="Screenshot that shows how to select a data source in Create a new evaluation." lightbox="../media/evaluations/evaluate/select-data-source.png":::

#### Configure test data for a fine-tuned model

Set up the test dataset that's used for evaluation. This dataset is sent to the model to generate responses for assessment. You have two options for configuring your test data:

- Generate sample questions
- Use an existing dataset (or upload a new dataset)

##### Generate sample questions

If you don't have a dataset readily available and want to run an evaluation with a small sample, select the model deployment that you want to evaluate based on a chosen topic. Azure OpenAI models and other open models that are compatible with serverless API deployment, like Meta Llama and Phi-3 family models, are supported. 

The topic helps tailor the generated content to your area of interest. The queries and responses are generated in real time, and you can regenerate them as needed.

##### Use your dataset

You can also select from your established dataset collection or upload a new dataset.

:::image type="content" source="../media/evaluations/evaluate/create-evaluation-model-dataset.png" alt-text="Screenshot that shows Select data source and highlights using an existing dataset." lightbox="../media/evaluations/evaluate/create-evaluation-model-dataset.png":::

#### Select evaluation metrics

To configure your test criteria, select **Next**. As you select your criteria, metrics are added, and you need to map your dataset’s columns to the required fields for evaluation. These mappings ensure accurate alignment between your data and the evaluation criteria. 

After you select the test criteria you want, you can review the evaluation, optionally change the name of the evaluation, and then select **Submit**. Go to the evaluation page to see the results.

:::image type="content" source="../media/evaluations/evaluate/review-model-evaluation.png" alt-text="Screenshot that shows the Review evaluation option." lightbox="../media/evaluations/evaluate/review-model-evaluation.png":::

> [!NOTE]
> The generated dataset is saved to the project’s blob storage after the evaluation run is created.

## View and manage the evaluators in the evaluator library

You can see the details and status of your evaluators in one place in the evaluator library. You can view and manage Microsoft-curated evaluators.

The evaluator library also enables version management. You can compare different versions of your work, restore previous versions if needed, and collaborate with others more easily.

To use the evaluator library in Azure AI Foundry portal, go to your project's **Evaluation** page and select the **Evaluator library** tab.

:::image type="content" source="../media/evaluations/evaluate/evaluator-library-list.png" alt-text="Screenshot that shows the page where you select evaluators from the evaluator library." lightbox="../media/evaluations/evaluate/evaluator-library-list.png":::

You can select the evaluator name to see more details. You can see the name, description, and parameters, and check any files associated with the evaluator. Here are some examples of Microsoft-curated evaluators:

- For performance and quality evaluators curated by Microsoft, you can view the annotation prompt on the details page. You can adapt these prompts to your own use case. Change the parameters or criteria according to your data and objectives in the Azure AI Evaluation SDK. For example, you can select **Groundedness-Evaluator** and check the Prompty file that shows how we calculate the metric.
- For risk and safety evaluators curated by Microsoft, you can see the definition of the metrics. For example, you can select **Self-Harm-Related-Content-Evaluator** to learn what it means and understand how Microsoft determines severity levels.

## Related content

Learn more about how to evaluate your generative AI applications:

- [View the evaluation results](./evaluate-results.md)
- [Creating evaluations specifically with OpenAI evaluation graders in Azure OpenAI Hub](../openai/how-to/evaluations.md)
- [Transparency note for Azure AI Foundry safety evaluations](../concepts/safety-evaluations-transparency-note.md).

