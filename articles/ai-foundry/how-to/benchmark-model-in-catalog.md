---
title: Compare models using the model leaderboard
titleSuffix: Microsoft Foundry
description: Compare model benchmarks across quality, safety, cost, and throughput using the model leaderboard and side-by-side comparison features in Foundry portal.
ms.service: azure-ai-foundry
ms.custom:
  - ai-learning-hub
ms.topic: how-to
ms.date: 02/13/2026
ms.reviewer: changliu2
reviewer: changliu2
ms.author: lagayhar  
author: lgayhardt
monikerRange: 'foundry-classic || foundry'
ai-usage: ai-assisted
---

# Compare models using the model leaderboard (preview)

[!INCLUDE [version-banner](../includes/version-banner.md)]

::: moniker range="foundry-classic"

This article shows you how to streamline model selection in the Foundry [model catalog](../concepts/foundry-models-overview.md) by comparing models in the model leaderboards (preview) available in Foundry portal. This comparison can help you make informed decisions about which models meet the requirements for your particular use case or application.

After reading this article, you can identify the best model for your scenario by comparing benchmark scores and viewing trade-off charts in the model leaderboard.

::: moniker-end

::: moniker range="foundry"

This article shows you how to streamline model selection in the Foundry [model catalog](../concepts/foundry-models-overview.md) by using the model leaderboards (preview) and side-by-side comparison features in Foundry portal. Evaluate model benchmark scores across quality, safety, cost, and throughput to choose the best model for your scenario.

After reading this article, you can identify the best model for your scenario by comparing benchmark scores, viewing trade-off charts, and evaluating models side by side.

::: moniker-end

Analyze and compare models using:

- [Model leaderboard](#access-model-leaderboards) to quickly identify top-performing models for quality, safety, estimated cost, and throughput leaderboards
- [Trade-off charts](#trade-off-charts) to visually compare model performance across two metrics, such as quality versus cost
- [Leaderboards by scenario](#view-leaderboards-by-scenario) to find the most relevant benchmark leaderboard for your specific scenario

::: moniker range="foundry"
- [Compare models](#compare-models) to evaluate features, performance, and estimated cost in a side-by-side view
::: moniker-end

[!INCLUDE [feature-preview](../includes/feature-preview.md)]

## Prerequisites

- An Azure subscription with a valid payment method. Free or trial Azure subscriptions won't work. If you don't have an Azure subscription, create a [paid Azure account](https://azure.microsoft.com/pricing/purchase-options/pay-as-you-go) to begin.

- A [Foundry project](create-projects.md).

- At least **Reader** role on the Foundry project. For more information, see [Role-based access control in Foundry](../concepts/rbac-foundry.md).

- Access to the [Foundry portal](https://ai.azure.com).

## Access model leaderboards

::: moniker range="foundry-classic"

[!INCLUDE [open-catalog](../includes/open-catalog.md)]

1. Go to the **Model leaderboards** section of the model catalog. This section displays the top three model leaders ranked along [quality](../concepts/model-benchmarks.md#quality-benchmarks-of-language-models), [safety](../concepts/model-benchmarks.md#safety-benchmarks-of-language-models), [cost](../concepts/model-benchmarks.md#cost-benchmarks-of-language-models), and [performance](../concepts/model-benchmarks.md#performance-benchmarks-of-language-models). Select any of these models to view more details.

    :::image type="content" source="../media/how-to/model-benchmarks/leaderboard-entry-select-model.png" alt-text="Screenshot showing the selected model from entry point of leaderboards on the model catalog homepage." lightbox="../media/how-to/model-benchmarks/leaderboard-entry-select-model.png":::

1. From the **Model leaderboards** section of the model catalog, select **Browse leaderboards**  to go to the [model leaderboards landing page](https://aka.ms/model-leaderboards) to see the full suite of leaderboards that are available.

    :::image type="content" source="../media/how-to/model-benchmarks/leaderboard-entry.png" alt-text="Screenshot showing the entry point from model catalog into model leaderboards." lightbox="../media/how-to/model-benchmarks/leaderboard-entry.png"::: 

    The homepage displays leaderboard highlights for model selection criteria. Quality is the most common criterion for model selection, followed by safety, cost, and performance.

    :::image type="content" source="../media/how-to/model-benchmarks/leaderboard-highlights.png" alt-text="Screenshot showing the highlighted leaderboards in quality, cost, and performance." lightbox="../media/how-to/model-benchmarks/leaderboard-highlights.png":::

::: moniker-end

::: moniker range="foundry"

Use the model catalog to access the leaderboard and identify top-performing models.

1. If you're not already in your project, select it.

1. Select **Discover** from the top navigation bar to browse the [model catalog](../concepts/foundry-models-overview.md). The overview page shows a snapshot of the model leaderboard at the top.

1. Sort on different metrics — [quality](../concepts/model-benchmarks.md#quality-benchmarks-of-language-models), [safety](../concepts/model-benchmarks.md#safety-benchmarks-of-language-models), [estimated cost](../concepts/model-benchmarks.md#cost-benchmarks-of-language-models), and [throughput](../concepts/model-benchmarks.md#performance-benchmarks-of-language-models) — to view the top models for each criterion. Select any model to go to its detail page, or select **Go to leaderboard** to view the full list. The model detail page shows the model's overview, benchmarks, and deployment options.

1. On the **Model leaderboard** page, view the top leaders for quality, safety, throughput, and estimated cost. Expand these charts to visually view the top 10. Each expanded chart shows a bar graph of the top 10 models for that metric.

1. Scroll past the charts to find the full model leaderboard. Sort on the metrics you care most about and select a model name to go to its detail page.

    The leaderboard table appears with sortable columns for quality, safety, throughput, and estimated cost.

1. Select two or three models for [detailed feature comparison](#compare-models) in a side-by-side view.

    The comparison view appears, showing features, performance, and estimated cost for your selected models.

::: moniker-end

### Trade-off charts

The trade-off chart allows you to compare trade-offs visually based on the criteria that matter most to you.

For example, suppose the highest-quality model isn't the cheapest. You might need to make trade-offs among quality, safety, cost, and throughput criteria. In the trade-off chart, you can compare how models perform along two metrics at a glance.

::: moniker range="foundry-classic"

1. Select the **Models selected** dropdown menu to add or remove models from the trade-off chart.
1. Select the **Quality vs. Safety** tab, **Quality vs. Cost** tab, and **Quality vs Throughput** tab to view those charts for your selected models.
1. Select **Compare between metrics** to access comparisons between more pairs of these dimensions.

:::image type="content" source="../media/how-to/model-benchmarks/leaderboard-trade-off.png" alt-text="Screenshot showing the trade-off charts in quality, cost, and performance." lightbox="../media/how-to/model-benchmarks/leaderboard-trade-off.png":::

::: moniker-end

::: moniker range="foundry"

Use the trade-off chart on the model leaderboard page to visualize how models balance competing criteria:

1. Use the **Compare quality against** dropdown to switch between estimated cost, throughput, or safety comparisons.

1. Add or remove models from the trade-off chart using the model selector on the right side of the chart.

1. Hover over a data point to view the exact scores for the selected model. Models closer to the top-right corner of the chart perform well on both axes.

::: moniker-end

### View leaderboards by scenario

Suppose you have a scenario that requires certain model capabilities. For example, if you're building a question-answering chatbot that needs strong reasoning capabilities and resistance to harmful content, compare models in capability-specific leaderboards.

::: moniker range="foundry-classic"

:::image type="content" source="../media/how-to/model-benchmarks/leaderboard-by-scenario.png" alt-text="Screenshot showing the quality leaderboards by scenarios." lightbox="../media/how-to/model-benchmarks/leaderboard-by-scenario.png":::

::: moniker-end

::: moniker range="foundry"

1. On the model leaderboard page, scroll to the **Leaderboards by scenario** section.

1. Select a scenario category, such as **Reasoning**, **Coding**, or **Question answering**.

1. Review the ranked list of models for your selected scenario. The leaderboard shows how models perform on benchmarks that are specific to that capability.

::: moniker-end

After exploring the leaderboards, decide on a model to use.

::: moniker range="foundry-classic"

## View benchmarks from the model card

> [!NOTE]
> Benchmark data isn't available for all models in the catalog. If a model doesn't have a **Benchmarks** tab, benchmark results haven't been published for that model yet.

1. Select a model to your liking and select **Model details**. You can select the model from one of the displayed leaderboards, such as the quality leaderboard at the top of the model leaderboards homepage. For this example, select **gpt-4o**. This action opens the model's overview page.

1. Go to the **Benchmarks** tab to check the benchmark results for the model.
  
    :::image type="content" source="../media/how-to/model-benchmarks/gpt4o-benchmark-tab.png" alt-text="Screenshot showing the  benchmarks tab for gpt-4o." lightbox="../media/how-to/model-benchmarks/gpt4o-benchmark-tab.png":::

1. Select **Compare with more models**.

1. Switch to the **List view** to access more detailed results for each model.

    :::image type="content" source="../media/how-to/model-benchmarks/compare-view.png" alt-text="Screenshot showing an example of benchmark comparison view." lightbox="../media/how-to/model-benchmarks/compare-view.png":::

## Analyze benchmark results

When you're in the "Benchmarks" tab for a specific model, you can gather extensive information to better understand and interpret the benchmark results, including:

- **High-level aggregate scores**: These scores for AI quality, safety, estimated cost, latency, and throughput provide a quick overview of the model's performance.
- **Comparative charts**: These charts display the model's relative position compared to related models.
- **Metric comparison table**: This table presents detailed results for each metric.

    :::image type="content" source="../media/how-to/model-benchmarks/gpt4o-benchmark-tab-expand.png" alt-text="Screenshot showing benchmarks tab for gpt-4o." lightbox="../media/how-to/model-benchmarks/gpt4o-benchmark-tab-expand.png":::

By default, Foundry displays an average index across various metrics and datasets to provide a high-level overview of model performance.

> [!TIP]
> Benchmark scores are normalized indexes. A higher score indicates better performance for quality and safety metrics. For cost and throughput, lower estimated cost and higher throughput are generally preferred. Use the [trade-off charts](#trade-off-charts) to balance these competing criteria for your scenario.

Use these views to quickly assess a model's strengths. To drill into specific metrics, follow these steps:

1. Select the expand button on the chart. The pop-up comparison chart reveals detailed information and offers greater flexibility for comparison.

    :::image type="content" source="../media/how-to/model-benchmarks/expand-to-detailed-metric.png" alt-text="Screenshot showing the expand button to select for a detailed comparison chart." lightbox="../media/how-to/model-benchmarks/expand-to-detailed-metric.png":::

1. Select the metric of interest and choose different datasets, based on your specific scenario. For more detailed definitions of the metrics and descriptions of the public datasets used to calculate results, select **Read more**.

    :::image type="content" source="../media/how-to/model-benchmarks/comparison-chart-per-metric-data.png" alt-text="Screenshot showing the comparison chart with a specific metric and dataset." lightbox="../media/how-to/model-benchmarks/comparison-chart-per-metric-data.png":::

## Evaluate benchmark results with your data

The previous sections showed the benchmark results calculated by Microsoft, using public datasets. However, you can try to regenerate the same set of metrics with your data.

1. Return to the **Benchmarks** tab in the model card.
1. Select **Try with your own data** to [evaluate the model with your data](evaluate-generative-ai-app.md#model-evaluation). Evaluation on your data helps you see how the model performs in your particular scenarios.

    :::image type="content" source="../media/how-to/model-benchmarks/try-with-your-own-data.png" alt-text="Screenshot showing the button to select for evaluating with your own data." lightbox="../media/how-to/model-benchmarks/try-with-your-own-data.png":::

::: moniker-end

::: moniker range="foundry"

## Compare models

The side-by-side comparison view lets you evaluate up to three models simultaneously across multiple dimensions.

1. From the model leaderboard, select two or three models by checking the boxes next to their names.

1. Select **Compare** to open the side-by-side comparison view.

1. Review the comparison across the following tabs:

    - **Performance benchmarks**: Quality, safety, and throughput scores from public datasets
    - **Model details**: Context window, training data, and supported languages
    - **Supported endpoints**: Deployment options such as serverless API and managed compute
    - **Feature support**: Capabilities like function calling, structured output, and vision

1. To learn more about a specific model, select **View details**. If you're ready to start using a model, select **Deploy**.

:::image type="content" source="media/observability/model-benchmarks/compare-model-overview.png" alt-text="Screenshot showing the compare model experience in Microsoft Foundry." lightbox="media/observability/model-benchmarks/compare-model-overview.png":::

## View model benchmarks

To view benchmarks for a specific model, select the model name from the leaderboard or search for it in the model catalog. On the model detail page, select the **Benchmarks** tab.

> [!NOTE]
> Benchmark data isn't available for all models in the catalog. If a model doesn't have a **Benchmarks** tab, benchmark results haven't been published for that model yet. Benchmarking results conducted by Microsoft are available for select models. Benchmarking information reported by providers is included when available.

When you're in the **Benchmarks** tab for a specific model, you can gather extensive information to better understand and interpret the benchmark results:

- **Public data benchmark results**: High-level aggregate scores for AI quality, safety, estimated cost, latency, and throughput that provide a quick overview of the model's performance.
- **Comparative charts**: These charts display the model's relative position compared to related models.
- **Metric comparison table**: This table presents detailed results for each metric.

    :::image type="content" source="media/observability/model-benchmarks/benchmark-overview.png" alt-text="Screenshot showing the metric comparison table on the benchmarks tab." lightbox="media/observability/model-benchmarks/benchmark-overview.png":::

By default, Foundry displays an average index across various metrics and datasets to provide a high-level overview of model performance.

> [!TIP]
> Benchmark scores are normalized indexes. A higher score indicates better performance for quality and safety metrics. For cost and throughput, lower estimated cost and higher throughput are generally preferred. Use the [trade-off charts](#trade-off-charts) to balance these competing criteria for your scenario.

To access benchmark results for a specific metric and dataset:

1. Select the expand button on the chart. The pop-up comparison chart reveals detailed information and offers greater flexibility for comparison.

1. Select the metric of interest and choose different datasets, based on your specific scenario. For more detailed definitions of the metrics and descriptions of the public datasets used to calculate results, select **Read more**.

For side-by-side model comparisons, [compare models](#compare-models) to evaluate features, performance metrics, and estimated costs across multiple models.

> [!NOTE]
> The **Try with your own data** option on the benchmarks tab is available only in [Foundry (classic)](?view=foundry-classic&preserve-view=true). To evaluate a model with your own data in the new portal, see [Evaluate generative AI apps](evaluate-generative-ai-app.md).

::: moniker-end

## Troubleshooting

| Issue | Resolution |
|-------|------------|
| Model doesn't appear in leaderboard | Not all models are benchmarked. Check the model catalog for availability. |
| No **Benchmarks** tab on model card | Benchmark results haven't been published for this model yet. |
| Benchmark scores differ from my results | Public benchmarks use standardized datasets and might not reflect performance on your specific data. To evaluate a model with your own data, see [Evaluate generative AI apps](evaluate-generative-ai-app.md). |
| Trade-off chart shows no data points | Ensure you have models selected in the model selector. At least two models are required for trade-off comparisons. |
| Can't compare more than three models | The side-by-side comparison view supports a maximum of three models. Deselect a model before adding another. |
| Benchmark scores seem outdated | Microsoft updates benchmark scores periodically. Check the model detail page for the benchmark evaluation date. |

## Related content

- [Model leaderboards in Foundry portal](../concepts/model-benchmarks.md) - Learn about the benchmarks, datasets, and metrics behind the leaderboard scores.
- [Evaluate generative AI apps with Foundry](evaluate-generative-ai-app.md) - Run evaluations on your own data to measure model performance for your scenario.
- [View evaluation results in Foundry portal](evaluate-results.md) - Interpret and compare evaluation results across runs.
