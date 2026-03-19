---
title: "See Evaluation Results in Microsoft Foundry portal"
description: "See and analyze AI model evaluation results in Microsoft Foundry portal. Learn to view performance metrics, compare results, and interpret evaluation data for model optimization."
ms.service: azure-ai-foundry
ms.custom:
  - classic-and-new
  - ignite-2023
  - build-2024
  - ignite-2024
ms.topic: how-to
ms.date: 12/22/2025
ms.reviewer: dlozier
ms.author: lagayhar
author: lgayhardt
ai-usage: ai-assisted
---

# View evaluation results in the Microsoft Foundry portal

In this article, you learn to:

- Locate and open evaluation runs.
- View aggregate and sample-level metrics.
- Compare results across runs.
- Interpret metric categories and calculations.
- Troubleshoot missing or partial metrics.

## Prerequisites

- An evaluation run.

    - To learn how to run evaluations in the portal see, [Evaluate generative AI models and applications](evaluate-generative-ai-app.md).
    - To learn how to run evaluations from the SDK see, [Run evaluations from the SDK](./develop/cloud-evaluation.md) or [Evaluate your AI agents](../observability/how-to/evaluate-agent.md).

## See your evaluation results

After submitting an evaluation, you can track its progress on the Evaluation details page. When the evaluation completes, the page displays key information such as:

-The evaluation creator
-Evaluation token usage
-Scores for each evaluator, broken down by run

:::image type="content" source="../media/observability/evaluation-runs.png" alt-text="Screenshot of the evaluation details page showing evaluation runs." lightbox="../media/observability/evaluation-runs.png":::

Select a specific run to drill into row‑level results.

Select **Learn more about metrics** for definitions and formulas.

### Evaluation run details

To view the row level data for individual runs, select the name of the run. This provides a view that allows you to see evaluation results at the individual query level against each evaluator used. Here, you can view details like query, response, ground truth, and the evaluator score and explanation.

## Compare the evaluation results

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

## Understand the built-in evaluation metrics

Understanding the built-in metrics is essential for assessing the performance and effectiveness of your AI application. By learning about these key measurement tools, you can interpret the results, make informed decisions, and fine-tune your application to achieve optimal outcomes.

To learn more, see [Built in evaluators](../concepts/built-in-evaluators.md).

## Troubleshooting

| Symptom | Possible cause | Action |
|---------|----------------|-------|
| Run stays pending | High service load or queued jobs | Refresh, verify quota, and resubmit if prolonged |
| Metrics missing | Not selected at creation | Rerun and select required metrics |
| All safety metrics zero | Category disabled or unsupported model | Confirm model and metric support matrix |
| Groundedness unexpectedly low | Retrieval/context incomplete | Verify context construction / retrieval latency |

## Related content

- Improve low metrics with prompt iteration or [fine-tuning](../../foundry-classic/concepts/fine-tuning-overview.md).
- [How to run batch evaluation](./develop/cloud-evaluation.md).

Learn how to evaluate your generative AI applications:

- [Evaluate your generative AI apps with the Foundry portal or SDK](../how-to/evaluate-generative-ai-app.md).
