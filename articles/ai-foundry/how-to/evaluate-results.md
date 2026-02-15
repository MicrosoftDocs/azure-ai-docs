---
title: See Evaluation Results in Microsoft Foundry portal
titleSuffix: Microsoft Foundry
description: See and analyze AI model evaluation results in Microsoft Foundry portal. Learn to view performance metrics, compare results, and interpret evaluation data for model optimization.
ms.service: azure-ai-foundry
ms.custom:
  - ignite-2023
  - build-2024
  - ignite-2024
ms.topic: how-to
ms.date: 12/22/2025
ms.reviewer: dlozier
ms.author: lagayhar
author: lgayhardt
monikerRange: 'foundry-classic || foundry'
ai-usage: ai-assisted
---

# See evaluation results in the Microsoft Foundry portal

[!INCLUDE [version-banner](../includes/version-banner.md)]

In this article, you learn to:

- Locate and open evaluation runs.
- View aggregate and sample-level metrics.
- Compare results across runs.
- Interpret metric categories and calculations.
- Troubleshoot missing or partial metrics.

## Prerequisites

::: moniker range="foundry-classic"

- An evaluation run.

    - To learn how to run evaluations in the portal see, [Evaluate generative AI models and applications](evaluate-generative-ai-app.md).
    - To learn how to run evaluations from the SDK see, [Run evaluations in the cloud](./develop/cloud-evaluation.md) or [Run evaluations locally](./develop/evaluate-sdk.md).


::: moniker-end

::: moniker range="foundry"

- An evaluation run.

    - To learn how to run evaluations in the portal see, [Evaluate generative AI models and applications](evaluate-generative-ai-app.md).
    - To learn how to run evaluations from the SDK see, [Run evaluations from the SDK](./develop/cloud-evaluation.md) or [Evaluate your AI agents](../default/observability/how-to/evaluate-agent.md).

::: moniker-end

## See your evaluation results

::: moniker range="foundry-classic"

After you submit an evaluation, locate the run on the **Evaluation** page. Filter or adjust columns to focus on runs of interest. Review high-level metrics at a glance before drilling in.

> [!TIP]
> You can view an evaluation run with any version of the `promptflow-evals` SDK or `azure-ai-evaluation` versions 1.0.0b1, 1.0.0b2, 1.0.0b3. Enable the **Show all runs** toggle to locate the run.

Select **Learn more about metrics** for definitions and formulas.

:::image type="content" source="../media/evaluations/view-results/learn-more-metrics.png" alt-text="Screenshot that shows details of the evaluation metrics." lightbox="../media/evaluations/view-results/learn-more-metrics.png":::

Select a run to open details (dataset, task type, prompt, parameters) plus per-sample metrics. The metrics dashboard visualizes pass rate or aggregate score per metric.

[!INCLUDE [FDP-backward-compatibility-azure-openai](../includes/fdp-backward-compatibility-azure-openai.md)]

::: moniker-end

::: moniker range="foundry"

After submitting an evaluation, you can track its progress on the Evaluation details page. When the evaluation completes, the page displays key information such as:

-The evaluation creator
-Evaluation token usage
-Scores for each evaluator, broken down by run

:::image type="content" source="../default/media/observability/evaluation-runs.png" alt-text="Screenshot of the evaluation details page showing evaluation runs." lightbox="../default/media/observability/evaluation-runs.png":::

Select a specific run to drill into row‑level results.

Select **Learn more about metrics** for definitions and formulas.

::: moniker-end

::: moniker range="foundry-classic"

### Metric dashboard

In the **Metric dashboard** section, aggregate views are broken down by metrics that include **AI quality (AI Assisted)**, **Risk and safety (preview)**, **AI Quality (NLP)**, and **Custom** (when applicable). Results are measured as percentages of pass/fail based on the criteria selected when the evaluation was created. For more in-depth information on metric definitions and how they're calculated, see [What are evaluators?](../concepts/observability.md#what-are-evaluators).

- For **AI quality (AI Assisted)** metrics, results are aggregated by averaging all scores per metric. If you use **Groundedness Pro**, output is binary and the aggregated score is passing rate: `(#trues / #instances) × 100`.
    :::image type="content" source="../media/evaluations/view-results/ai-quality-ai-assisted-chart.png" alt-text="Screenshot that shows the AI quality (AI Assisted) metrics dashboard tab." lightbox="../media/evaluations/view-results/ai-quality-ai-assisted-chart.png":::
- For **Risk and safety (preview)** metrics, results are aggregated by defect rate.
  - Content harm: percentage of instances exceeding severity threshold (default `Medium`).
  - For protected material and indirect attack, the defect rate is calculated as the percentage of instances where the output is `true` by using the formula `(Defect Rate = (#trues / #instances) × 100)`.
    :::image type="content" source="../media/evaluations/view-results/risk-and-safety-chart.png" alt-text="Screenshot that shows the risk and safety metrics dashboard tab." lightbox="../media/evaluations/view-results/risk-and-safety-chart.png":::
- For **AI quality (NLP)** metrics, results are aggregated by averaging scores per metric.
     :::image type="content" source="../media/evaluations/view-results/ai-quality-nlp-chart.png" alt-text="Screenshot that shows the AI quality (NLP) dashboard tab." lightbox="../media/evaluations/view-results/ai-quality-nlp-chart.png":::

::: moniker-end


::: moniker range="foundry-classic"

### Detailed metrics result table

Use the table under the dashboard to inspect each data sample. Sort by a metric to surface worst‑performing samples and identify systematic gaps (incorrect results, safety failures, latency). Use search to cluster related failure topics. Apply column customization to focus on key metrics.

Typical actions:

- Filter for low scores to detect recurring patterns.
- Adjust prompts or fine-tune when systemic gaps appear.
- Export for offline analysis.

Here are some examples of the metrics results for the question-answering scenario:

:::image type="content" source="../media/evaluations/view-results/metrics-details-qa.png" alt-text="Screenshot that shows metrics results for the question-answering scenario." lightbox="../media/evaluations/view-results/metrics-details-qa.png":::

Some evaluations have subevaluators, which allow you to view the JSON of the results from the subevaluations. To view the results, select **View in JSON**.

:::image type="content" source="../media/evaluations/view-results/evaluation-view-json.png" alt-text="Screenshot that shows detailed metrics results with JSON selected." lightbox="../media/evaluations/view-results/evaluation-view-json.png":::

View the JSON in the **JSON Preview**:

:::image type="content" source="../media/evaluations/view-results/evaluation-view-sub-evaluators.png" alt-text="Screenshot that shows the JSON preview." lightbox="../media/evaluations/view-results/evaluation-view-sub-evaluators.png":::

Here are some examples of the metrics results for the conversation scenario. To review the results throughout a multi-turn conversation, select **View evaluation results per turn** in the **Conversation** column.

:::image type="content" source="../media/evaluations/view-results/evaluation-view-multi-turn-button.png" alt-text="Screenshot that shows metrics results for the conversation scenario." lightbox="../media/evaluations/view-results/evaluation-view-multi-turn-button.png":::

When you select **View evaluation results per turn**, you see the following screen:

:::image type="content" source="../media/evaluations/view-results/metric-per-turn.png" alt-text="Screenshot that shows the evaluation results per turn." lightbox="../media/evaluations/view-results/metric-per-turn.png":::

For a safety evaluation in a multi-modal scenario (text and images), you can better understand the evaluation result by reviewing the images from both the input and output in the detailed metrics result table. Because multi-modal evaluation is currently supported only for conversation scenarios, you can select **View evaluation results per turn** to examine the input and output for each turn.  

:::image type="content" source="../media/evaluations/view-results/image-per-turn-pop-up.png" alt-text="Screenshot that shows the image dialog from the conversation column." lightbox="../media/evaluations/view-results/image-per-turn-pop-up.png":::

Select the image to expand and view it. By default, all images are blurred to protect you from potentially harmful content. To view the image clearly, turn on the **Check blur image** toggle.

:::image type="content" source="../media/evaluations/view-results/image-check-blur-image.png" alt-text="Screenshot that shows a blurred image and the Check blur image toggle." lightbox="../media/evaluations/view-results/image-check-blur-image.png":::

Evaluation results might have different meanings for different audiences. For example, safety evaluations might generate a label for **Low** severity of violent content that might not align with a human reviewer's definition of how severe that specific violent content is. The passing grade set during the creation of the evaluation determines whether a pass or fail is assigned. There's a **Human feedback** column where you can select a thumbs up or thumbs down icon as you review your evaluation results. You can use this column to log which instances were approved or flagged as incorrect by a human reviewer.

:::image type="content" source="../media/evaluations/view-results/risk-safety-metric-human-feedback.png" alt-text="Screenshot that shows risk and safety metrics results with human feedback." lightbox="../media/evaluations/view-results/risk-safety-metric-human-feedback.png":::

To understand each content risk metric, view metric definitions in the **Report** section, or review the test in the **Metric dashboard** section.

If there's something wrong with the run, you can also use the logs to debug your evaluation run. Here are some examples of logs that you can use to debug your evaluation run:

:::image type="content" source="../media/evaluations/view-results/evaluation-log.png" alt-text="Screenshot that shows logs that you can use to debug your evaluation run." lightbox="../media/evaluations/view-results/evaluation-log.png":::

If you're evaluating a prompt flow, you can select the **View in flow** button to go to the evaluated flow page and update your flow. For example, you can add extra meta prompt instructions, or change some parameters and reevaluate.  

::: moniker-end

::: moniker range="foundry"

### Evaluation run details

To view the row level data for individual runs, select the name of the run. This provides a view that allows you to see evaluation results at the individual query level against each evaluator used. Here, you can view details like query, response, ground truth, and the evaluator score and explanation.
::: moniker-end

## Compare the evaluation results

::: moniker range="foundry-classic"

To compare two or more runs, select the desired runs and start the process. Select the **Compare** button or the **Switch to dashboard view** button for a detailed dashboard view. Analyze and contrast the performance and outcomes of multiple runs to make informed decisions and targeted improvements.

:::image type="content" source="../media/evaluations/view-results/evaluation-list-compare.png" alt-text="Screenshot that shows the option to compare evaluations." lightbox="../media/evaluations/view-results/evaluation-list-compare.png":::

In the dashboard view, you have access to two valuable components: the metric distribution comparison **Chart** and the comparison **Table**. You can use these tools to perform a side-by-side analysis of the selected evaluation runs. You can compare various aspects of each data sample with ease and precision.

> [!NOTE]
> By default, older evaluation runs have matching rows between columns. However, newly run evaluations have to be intentionally configured to have matching columns during evaluation creation. Ensure that the same name is used as the **Criteria Name** value across all evaluations that you want to compare.

The following screenshot shows the results when the fields are the same:  

:::image type="content" source="../media/evaluations/view-results/evaluation-criteria-name-match.png" alt-text="Screenshot that shows automated evaluations when the fields are the same." lightbox="../media/evaluations/view-results/evaluation-criteria-name-match.png":::

When a user doesn't use the same **Criteria Name** in creating the evaluation, fields don't match, which causes the platform to be unable to directly compare the results:

:::image type="content" source="../media/evaluations/view-results/evaluation-criteria-name-mismatch.png" alt-text="Screenshot that shows automated evaluations when the fields aren't the same." lightbox="../media/evaluations/view-results/evaluation-criteria-name-mismatch.png":::

In the comparison table, hover over the run you want to use as the reference point and set it as the baseline. Activate the **Show delta** toggle to visualize differences between the baseline and other runs for numerical values. Select the **Show only difference** toggle to display only rows that differ among the selected runs, helping identify variations.

By using these comparison features, you can make an informed decision to select the best version:

- **Baseline comparison**: By setting a baseline run, you can identify a reference point against which to compare the other runs. You can see how each run deviates from your chosen standard.
- **Numerical value assessment**: Enabling the **Show delta** option helps you understand the extent of the differences between the baseline and other runs. This information can help you evaluate how various runs perform in terms of specific evaluation metrics.
- **Difference isolation**: The **Show only difference** feature streamlines your analysis by highlighting only the areas where there are discrepancies between runs. This information can be instrumental in pinpointing where improvements or adjustments are needed.

Use comparison tools to choose the best-performing configuration and avoid regressions in safety or groundedness.

:::image type="content" source="../media/evaluations/view-results/comparison-table.png" alt-text="Screenshot that shows side-by-side evaluation results." lightbox="../media/evaluations/view-results/comparison-table.png":::

::: moniker-end

::: moniker range="foundry"

To facilitate a comprehensive comparison between two or more runs, you can select the desired runs and initiate the process.

1. Select two or more runs in the evaluation detail page.
1. Select **Compare**.

It generates a side-by-side comparison view for all selected runs.

The comparison is computed based on statistic t-testing, which provides more sensitive and reliable results for you to make decisions. You can use different functionalities of this feature:

- Baseline comparison: By setting a baseline run, you can identify a reference point against which to compare the other runs. You can see how each run deviates from your chosen standard.
- Statistic t-testing assessment: Each cell provides the stat-sig results with different color codes. You can also hover on the cell to get the sample size and p-value.  

|Legend | Definition|
|--|--|
| ImprovedStrong | Highly stat-sig (p<=0.001) and moved in the desired direction |
| ImprovedWeak  | Stat-sig (0.001<p<=0.05) and moved in the desired direction |
| DegradedStrong | Highly stat-sig (p<=0.001) and moved in the wrong direction |
| DegradedWeak | Stat-sig (0.001<p<=0.05) and moved in the wrong direction |
| ChangedStrong | Highly stat-sig (p<=0.001) and desired direction is neutral |
| ChangedWeak | Stat-sig (0.001<p<=0.05) and desired direction is neutral |
| Inconclusive | Too few examples, or p>=0.05 |

> [!NOTE]
> The comparison view won't be saved. If you leave the page, you can reselect the runs and select **Compare** to regenerate the view.

::: moniker-end

::: moniker range="foundry-classic"

## Measure jailbreak vulnerability

Evaluating jailbreak vulnerability is a comparative measurement, not an AI-assisted metric. Run evaluations on two different, red-teamed datasets: a baseline adversarial test dataset versus the same adversarial test dataset with jailbreak injections in the first turn. You can use the adversarial data simulator to generate the dataset with or without jailbreak injections. Ensure that the **Criteria Name** value is the same for each evaluation metric when you configure the runs.

To check if your application is vulnerable to jailbreak, specify the baseline and turn on the **Jailbreak defect rates** toggle in the comparison table. The jailbreak defect rate is the percentage of instances in your test dataset where a jailbreak injection generates a higher severity score for *any* content risk metric compared to a baseline across the entire dataset. Select multiple evaluations in your **Compare** dashboard to view the difference in defect rates.

:::image type="content" source="../media/evaluations/view-results/evaluation-compare-jailbreak.png" alt-text="Screenshot of side-by-side evaluation results with jailbreak defect toggled on." lightbox="../media/evaluations/view-results/evaluation-compare-jailbreak.png":::

> [!TIP]
> The jailbreak defect rate is calculated only for datasets of the same size and when all runs include content risk and safety metrics.

::: moniker-end

## Understand the built-in evaluation metrics

Understanding the built-in metrics is essential for assessing the performance and effectiveness of your AI application. By learning about these key measurement tools, you can interpret the results, make informed decisions, and fine-tune your application to achieve optimal outcomes.

To learn more, see [What are evaluators?](../concepts/observability.md#what-are-evaluators).

## Troubleshooting

| Symptom | Possible cause | Action |
|---------|----------------|-------|
| Run stays pending | High service load or queued jobs | Refresh, verify quota, and resubmit if prolonged |
| Metrics missing | Not selected at creation | Rerun and select required metrics |
| All safety metrics zero | Category disabled or unsupported model | Confirm model and metric support matrix |
| Groundedness unexpectedly low | Retrieval/context incomplete | Verify context construction / retrieval latency |

## Related content

- Improve low metrics with prompt iteration or [fine-tuning](../concepts/fine-tuning-overview.md).
- [Run evaluations in the cloud with the Microsoft Foundry SDK](./develop/cloud-evaluation.md).

Learn how to evaluate your generative AI applications:

- [Evaluate your generative AI apps with the Foundry portal or SDK](../how-to/evaluate-generative-ai-app.md).
- [Create evaluations with OpenAI evaluation graders in Azure OpenAI Hub](../openai/how-to/evaluations.md).
