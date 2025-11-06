---
title: Evaluation Cluster Analysis 
titleSuffix: Azure AI Foundry 
description: Learn how to run and interact with an evaluation cluster analysis. 
ms.service: azure-ai-foundry
ms.topic: how-to
ms.date: 11/18/2025
ms.reviewer: hanch
ms.author: lagayhar
author: lgayhardt
ai-usage: ai-assisted 
---

# Evaluation Cluster Analysis (preview)

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

Once you run one or evaluation runs, you can generate an evaluation cluster analysis to understand what is happening in your evaluation results and have an intuitive way to understand the top patterns / errors in your evaluation runs, with recommended next steps on improving the evaluator scores.

This article describes the user experience of how to generate an evaluation cluster analysis and interact with it.

## Prerequisites

Before you begin:

- You have access to the **Azure AI Foundry portal**.
- You have one or more deployed agents.
- You have one or more evaluation runs in one evaluation group.

## Generate an evaluation cluster analysis

In the evaluation group detail page, you can select one or more runs and select **Cluster analysis**. A window pops up and asks you to select a model to generate the cluster analysis. It also provides an estimated time and tokens based on the samples selected from the evaluation runs.  

## View cluster analysis

Cluster Analysis provides an intuitive visualization of performance by grouping evaluation result samples with similar issues or response patterns. It helps you quickly identify recurring failure types, understand distribution across error categories, and prioritize areas for improvement.

At the top of the view, there are summary statistics for the evaluation run:

- Total Samples – Total number of evaluated responses (for example, 48).
- Clusters – Number of automatically identified clusters (for example, 2).
- Passed / Failed – Breakdown of successful versus problematic samples.
- Avg Score – The overall average quality score for the run.
- Hover / Click: Hovering over a dot or cluster label reveals detailed information, including example responses and evaluator feedback.

### Visualization

Each dot represents a sample from your evaluation dataset. Dots are grouped by semantic similarity, using embedding-based clustering of model outputs and feedback signals.

- Color: Indicates the cluster assignment (for example, inadequate final answer, incorrect response).
- Position: Samples closer together share similar characteristics or issues.

### Detail Panel

#### Cluster

Selecting a cluster opens a side panel that includes:

- Selected cluster – Name of the top-level issue group.
- Entry count – Total number of samples within this cluster.
- Subclusters – Breakdown of related subcategories.
- Description – Automatically generated diagnostic summary explaining the likely cause or characteristic pattern
- Recommendations –suggested next steps for mitigation or agent improvement.

#### Sub-Cluster

Selecting a subcluster opens a side panel that includes:

- Cluster – Indicates the parent cluster this subcluster belongs to (for example, inadequate_final_answer).
- Selected Subcluster – The specific subset being examined (for example, invalid_or_missing_api_key).
- Entry Count – Number of individual samples grouped under this subcluster.
- Tabs:
  - Analysis – Provides summary statistics, score averages, and qualitative insights (when available).
  - Entries – Lists each sample (Entry ID) in the subcluster with their individual scores such as fluency, groundedness, or accuracy.

#### Entry ID

Selecting a dot / entry ID opens a side panel that includes:

- Cluster hierarchy
  - Displays the full path of where this entry belongs:
    Cluster → Subcluster → Entry ID
    For example, inadequate_final_answer → invalid_or_missing_api_key → Entry ID: 17-fluency.
- Tabs
- Conversation – Shows the full text interaction for the selected sample:
  - Context Summary (if applicable) – Any background or preceding context used in the evaluation.
  - Query – The model prompt or user question (for example, “How do I submit an FSA reimbursement claim?”).
  - Response – The model’s generated output for that query.
- Metadata – Contains additional evaluation information such as scores, evaluators, timestamps, agent IDs, and trace IDs.

### Filter Panel

The Filter Panel on the right side of the Cluster Analysis view allows users to customize how clusters are displayed and filtered for targeted inspection.

- Color By
  - Lets you adjust how the samples are color-coded on the visualization.
  - Options typically include:
    - Cluster – Colors samples by top-level issue category.
    - Subcluster – Colors samples by more granular subcategories within each cluster.
    - Or evaluation result, evaluation type, score, and agent ID.
- Advanced Filtering
  - Provides tools to focus the visualization on specific subsets of data.
  - You can define filters based on metadata or evaluation attributes.
    - Select Parameter – Choose which field to filter on (for example, score, evaluator type, timestamp).
    - Equal / Contains / Not equal – Define the condition for filtering.
    - Select Value – Choose or input the specific value to match.
    - Add Filter – Apply the condition to update the view dynamically.

## Download the analysis

If you want to view the analysis offline, you can select **download** to get a copy of the analysis in csv format and easily view it in other applications.  

> [!NOTE]
> The analysis result won't be stored. Once you leave the page, the analysis result will be gone.

## Next Steps

The Cluster Analysis view gives you a powerful way to move from surface-level evaluation metrics to actionable insights. By combining semantic grouping, diagnostic summaries, and per-sample context, it bridges the gap between quantitative scoring and qualitative understanding.

Use the insights discovered here to:

- Refine prompts or model based on recurring issue patterns.
- Validate improvements after fine-tuning or retraining and reevaluate to compare the old and new analysis results.

## Related content

- [See evaluation results in the Azure AI Foundry portal](../../ai-foundry/how-to/evaluate-results.md?view=foundry)
