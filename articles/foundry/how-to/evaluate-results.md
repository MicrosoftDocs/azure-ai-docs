---
title: "See Evaluation Results in Microsoft Foundry portal"
description: "See and analyze AI model evaluation results in Microsoft Foundry portal. Learn to view performance metrics, compare results, and interpret evaluation data for model optimization."
ms.service: microsoft-foundry
ms.custom:
  - classic-and-new
  - ignite-2023
  - build-2024
  - ignite-2024
ms.topic: how-to
ms.date: 04/29/2026
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

- **Azure AI User** role on the Foundry project. For more information, see [Role-based access control for Microsoft Foundry](../concepts/rbac-foundry.md).
- A completed evaluation run.
    - To run evaluations in the portal, see [Evaluate generative AI models and applications](evaluate-generative-ai-app.md).
    - To run evaluations from the SDK, see [Run evaluations from the SDK](./develop/cloud-evaluation.md) or [Evaluate your AI agents](../observability/how-to/evaluate-agent.md).

## See your evaluation results

1. In the [Foundry portal](https://ai.azure.com), go to your project and select **Evaluation** from the left pane.

1. Select an evaluation run from the list to open its details page. If the run is still in progress, the status shows **Running** and updates automatically when complete.

   The details page shows:

   | Field | Description |
   |-------|-------------|
   | Name | The name of the evaluation run. |
   | Target | The model or agent that was evaluated. |
   | Dataset | The test dataset used. Select the download icon to export it as a CSV file. |
   | Status | Current status of the run (**Running**, **Completed**, or **Failed**). |
   | Evaluation tokens | Tokens consumed by the evaluators during the run. |
   | Target tokens | Tokens consumed by the model or agent being evaluated. |
   | Scores | Aggregate score for each evaluator used. |

   :::image type="content" source="../media/observability/evaluation-runs.png" alt-text="Screenshot of the Evaluation page showing a list of runs with Name, Status, Target, Evaluation tokens, Target tokens, and Scores columns." lightbox="../media/observability/evaluation-runs.png":::

1. Hover over a score cell to see token usage details and additional context.

   :::image type="content" source="../media/observability/evaluation-runs-hover.png" alt-text="Screenshot of the Evaluation page with a score cell hovered, showing a tooltip with token usage breakdown." lightbox="../media/observability/evaluation-runs-hover.png":::

1. Select **Learn more about metrics** to see metric definitions and scoring formulas.

### Evaluation run details

Select the name of the run to view row-level results for each individual query. For each row, you can see the query, response, ground truth, evaluator score, and score explanation.

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
| All safety metrics zero | Category disabled or unsupported model | Confirm model and evaluator support in [Risk and safety evaluators](../concepts/built-in-evaluators.md#risk-and-safety-evaluators) |
| Groundedness unexpectedly low | Retrieval/context incomplete | Verify context construction / retrieval latency |

## Related content

- [Run evaluations from the Microsoft Foundry portal](./evaluate-generative-ai-app.md)
- [Run batch evaluations from the SDK](./develop/cloud-evaluation.md)
- [Built-in evaluators](../concepts/built-in-evaluators.md)
- [Improve model performance with fine-tuning](../openai/how-to/fine-tuning.md)
