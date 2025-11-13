---
title: Evaluation Cluster Analysis 
titleSuffix: Microsoft Foundry 
description: Learn how to run and interact with an evaluation cluster analysis. 
ms.service: azure-ai-foundry
ms.topic: how-to
ms.date: 11/18/2025
ms.reviewer: hanch
ms.author: lagayhar
author: lgayhardt
ai-usage: ai-assisted 
---

# Evaluation cluster analysis (preview)

[!INCLUDE [feature-preview](../../../includes/feature-preview.md)]

After you run one or more evaluation runs, you can generate an evaluation cluster analysis to understand your evaluation results. This analysis provides an intuitive way to identify the top patterns and errors in your evaluation runs, along with recommended next steps to improve evaluator scores.

This article explains how to generate and interact with an evaluation cluster analysis.

## Prerequisites

Before you begin:

- Make sure you have access to the **Microsoft Foundry portal**.
- Ensure you have one or more deployed agents.
- Verify that you have one or more evaluation runs in one evaluation.

## Generate an evaluation cluster analysis

On the evaluation detail page, select one or more runs and then select **Cluster analysis**. A window appears and prompts you to select a model to generate the cluster analysis. It also shows an estimated time and tokens based on the samples selected from the evaluation runs.  

:::image type="content" source="../../media/observability/cluster-analysis-set-up.png" alt-text="Screenshot of the setup cluster analysis window." lightbox="../../media/observability/cluster-analysis-set-up.png":::

## View cluster analysis

Cluster analysis provides an intuitive visualization of performance by grouping evaluation result samples with similar issues or response patterns. It helps you quickly identify recurring failure types, understand the distribution across error categories, and prioritize areas for improvement.

:::image type="content" source="../../media/observability/cluster-analysis-map.png" alt-text="Screenshot of the cluster analysis page." lightbox="../../media/observability/cluster-analysis-map.png":::

At the top of the view, summary statistics for the evaluation run are displayed:

- Total samples: Total number of evaluated responses (for example, 48).
- Clusters – Number of automatically identified clusters (for example, 2).
- Passed/failed: Breakdown of successful versus problematic samples.
- Avg Score – The overall average quality score for the run.
- Hover/click: Hovering over a dot or cluster label reveals detailed information, including example responses and evaluator feedback.

### Visualization

Each dot represents a sample from your evaluation dataset. Dots are grouped by semantic similarity, using embedding-based clustering of model outputs and feedback signals.

- Color: Indicates the cluster assignment (for example, inadequate final answer or incorrect response).
- Position: Samples closer together share similar characteristics or issues.

### Detail panel

#### Cluster

Selecting a cluster opens a side panel that includes:

- Selected cluster – Name of the top-level issue group.
- Entry count – Total number of samples within this cluster.
- Subclusters – Breakdown of related subcategories.
- Description – Automatically generated diagnostic summary explaining the likely cause or characteristic pattern
- Recommendations: Suggested next steps for mitigation or agent improvement.

:::image type="content" source="../../media/observability/cluster-analysis-side-panel.png" alt-text="Screenshot of a selected cluster with the side panel open." lightbox="../../media/observability/cluster-analysis-side-panel.png":::

#### Subcluster

Selecting a subcluster opens a side panel that includes:

- Cluster – Indicates the parent cluster this subcluster belongs to (for example, inadequate_final_answer).
- Selected subcluster – The specific subset being examined (for example, invalid_or_missing_api_key).
- Entry Count – Number of individual samples grouped under this subcluster.
- Tabs
  - Analysis – Provides summary statistics, score averages, and qualitative insights (when available).
  - Entries – Lists each sample (Entry ID) in the subcluster with their individual scores such as fluency, groundedness, or accuracy.

:::image type="content" source="../../media/observability/cluster-analysis-sub-cluster-side-panel.png" alt-text="Screenshot of a selected subcluster with the side panel open." lightbox="../../media/observability/cluster-analysis-sub-cluster-side-panel.png":::

#### Entry ID

Selecting a dot / entry ID opens a side panel that includes:

- Cluster hierarchy
  - Displays the full path of where this entry belongs:
    Cluster → Subcluster → Entry ID
    For example, inadequate_final_answer → invalid_or_missing_api_key → Entry ID: 17-fluency.
- Tabs
- Conversation – Shows the full text interaction for the selected sample:
  - Context Summary (if applicable) – Any background or preceding context used in the evaluation.
  - Query – The model prompt or user question (for example, "How do I submit an FSA reimbursement claim?").
  - Response – The model’s generated output for that query.
- Metadata – Contains additional evaluation information such as scores, evaluators, timestamps, agent IDs, and trace IDs.

:::image type="content" source="../../media/observability/cluster-analysis-entry-id.png" alt-text="Screenshot of entry ID select with side panel opened." lightbox="../../media/observability/cluster-analysis-entry-id.png":::

### Filter panel

The Filter Panel on the right side of the Cluster Analysis view allows users to customize how clusters are displayed and filtered for targeted inspection.

- Color by
  - Lets you adjust how the samples are color-coded on the visualization.
  - Options typically include:
    - Cluster – Colors samples by top-level issue category.
    - Subcluster – Colors samples by more granular subcategories within each cluster.
    - Or evaluation result, evaluation type, score, and agent ID.

:::image type="content" source="../../media/observability/cluster-analysis-filter.png" alt-text="Screenshot of the cluster analysis's filter panel." lightbox="../../media/observability/cluster-analysis-filter.png":::

- Advanced filtering
  - Provides tools to focus the visualization on specific subsets of data.
  - You can define filters based on metadata or evaluation attributes.
    - Select Parameter – Choose which field to filter on (for example, score, evaluator type, timestamp).
    - Equal / Contains / Not equal – Define the condition for filtering.
    - Select Value – Choose or input the specific value to match.
    - Add Filter – Apply the condition to update the view dynamically.

:::image type="content" source="../../media/observability/cluster-analysis-advanced-filtering.png" alt-text="Screenshot of the cluster analysis's advanced filtering." lightbox="../../media/observability/cluster-analysis-advanced-filtering.png":::

## Download the analysis

To view the analysis offline, select **download** to get a copy of the analysis in CSV format and view it in other applications.  

> [!NOTE]
> The analysis result isn't stored. If you leave the page, the analysis result is lost.

## Next steps

The cluster analysis view helps you move from surface-level evaluation metrics to actionable insights. By combining semantic grouping, diagnostic summaries, and per-sample context, it bridges the gap between quantitative scoring and qualitative understanding.

Use the insights discovered here to:

- Refine prompts or models based on recurring issue patterns.
- Validate improvements after fine-tuning or retraining, and reevaluate to compare the old and new analysis results.

## Related content

- [See evaluation results in the Foundry portal](../../../how-to/evaluate-results.md?view=foundry&preserve-view=true)
