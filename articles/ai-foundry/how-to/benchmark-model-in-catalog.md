---
title: Benchmark models in the model leaderboard of Microsoft Foundry portal
titleSuffix: Microsoft Foundry
description: In this article, you learn to compare benchmarks across models and datasets, using the model leaderboards (preview) and the benchmarks feature in Microsoft Foundry portal.
ms.service: azure-ai-foundry
ms.custom:
  - ai-learning-hub
ms.topic: how-to
ms.date: 11/18/2025
ms.reviewer: changliu2
reviewer: changliu2
ms.author: lagayhar  
author: lgayhardt
monikerRange: 'foundry-classic || foundry'
ai-usage: ai-assisted
---

# Compare and select models using the model leaderboard in Microsoft Foundry portal (preview)

[!INCLUDE [version-banner](../includes/version-banner.md)]

::: moniker range="foundry-classic"

This article shows you how to streamline model selection in the Microsoft Foundry [model catalog](../concepts/foundry-models-overview.md) by comparing models in the model leaderboards (preview) available in Foundry portal. This comparison can help you make informed decisions about which models meet the requirements for your particular use case or application.

::: moniker-end

::: moniker range="foundry"

This article shows you how to streamline model selection in the Microsoft Foundry [model catalog](../concepts/foundry-models-overview.md) by using the model leaderboards (preview) and side-by-side comparison features in Microsoft Foundry portal. These features enable you to understand model performance through comprehensive leaderboards and direct comparisons, helping you make informed decisions about which models best meet your specific use case or application requirements. 

::: moniker-end

You can analyze and compare models using:

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

## Access model leaderboards

::: moniker range="foundry-classic"

[!INCLUDE [open-catalog](../includes/open-catalog.md)]

4. Go to the **Model leaderboards** section of the model catalog. This section displays the top three model leaders ranked along [quality](../concepts/model-benchmarks.md#quality-benchmarks-of-language-models), [safety](../concepts/model-benchmarks.md#safety-benchmarks-of-language-models), [cost](../concepts/model-benchmarks.md#cost-benchmarks-of-language-models), and [performance](../concepts/model-benchmarks.md#performance-benchmarks-of-language-models). You can select any of these models to check out more details.

    :::image type="content" source="../media/how-to/model-benchmarks/leaderboard-entry-select-model.png" alt-text="Screenshot showing the selected model from entry point of leaderboards on the model catalog homepage." lightbox="../media/how-to/model-benchmarks/leaderboard-entry-select-model.png":::

1. From the **Model leaderboards** section of the model catalog, select **Browse leaderboards**  to go to the [model leaderboards landing page](https://aka.ms/model-leaderboards) to see the full suite of leaderboards that are available.

    :::image type="content" source="../media/how-to/model-benchmarks/leaderboard-entry.png" alt-text="Screenshot showing the entry point from model catalog into model leaderboards." lightbox="../media/how-to/model-benchmarks/leaderboard-entry.png"::: 

    The homepage displays leaderboard highlights for model selection criteria. Quality is the most common criterion for model selection, followed by safety, cost, and performance.

    :::image type="content" source="../media/how-to/model-benchmarks/leaderboard-highlights.png" alt-text="Screenshot showing the highlighted leaderboards in quality, cost, and performance." lightbox="../media/how-to/model-benchmarks/leaderboard-highlights.png":::

::: moniker-end

::: moniker range="foundry"

1. If you’re not already in your project, select it.

1. Go to **Discover** from the top nav, where you can view a snapshot of the model leaderboard on the overview page. You can sort on the different metrics to view the top 6 respectively. Quality is the most common criterion for model selection, followed by safety, cost, and performance. You can select any of these models to go their respective model detail pages. To view more models beyond top 6, select **Go to leaderboard**.

1. **Model leaderboard** highlights the top 5 leaders at the top for quality, safety, throughput, and estimated cost. These charts can be expanded to visually view the top 10.

1. After the charts, you can find the full model leaderboard. Similar to the top 6, you can sort on the metrics you care most about and select model name to go to their respective detail page.

1. You can also select 2-3 models for [detailed feature comparison](#compare-models) in a side by side view. 

::: moniker-end

### Trade-off charts

This trade-off chart allows you to compare trade-offs visually based on the criteria that you care more about. 
Suppose you care more about cost than quality and you discover that the highest quality model isn't the cheapest model, you might need to make trade-offs among quality, safety, cost, and throughput criteria. In the trade-off chart, you can compare how models perform along these two metrics at a glance. 

::: moniker range="foundry-classic"

1. Select the **Models selected** dropdown menu to add or remove models from the trade-off chart.
1. Select the **Quality vs. Safety** tab, **Quality vs. Cost** tab, and **Quality vs Throughput** tab to view those charts for your selected models.
1. Select **Compare between metrics** to access comparisons between more pairs of these dimensions.

:::image type="content" source="../media/how-to/model-benchmarks/leaderboard-trade-off.png" alt-text="Screenshot showing the trade-off charts in quality, cost, and performance." lightbox="../media/how-to/model-benchmarks/leaderboard-trade-off.png":::

::: moniker-end

::: moniker range="foundry"
You can **compare quality against** estimated cost, throughput, or safety by using the dropdown to switch.

You can add or remove models from the trade-off chart using the selector on the right.
::: moniker-end

### View leaderboards by scenario

Suppose you have a scenario that requires certain model capabilities. For example, say you're building a question-and-answering chatbot that requires resistance to harmful content, good question-and-answering and reasoning capabilities. You might find it useful to compare models in these leaderboards that are backed by capability-specific benchmarks.

::: moniker range="foundry-classic"

:::image type="content" source="../media/how-to/model-benchmarks/leaderboard-by-scenario.png" alt-text="Screenshot showing the quality leaderboards by scenarios." lightbox="../media/how-to/model-benchmarks/leaderboard-by-scenario.png":::

::: moniker-end

Once you've explored the leaderboards, you can decide on a model to use. 

::: moniker range="foundry-classic"

## View benchmarks from the model card

1. Select a model to your liking and select **Model details**. You can select the model from one of the displayed leaderboards, such as the quality leaderboard at the top of the model leaderboards homepage. For this example, select **gpt-4o**. This action opens the model's overview page.

1. Go to the **Benchmarks** tab to check the benchmark results for the model.
  
    :::image type="content" source="../media/how-to/model-benchmarks/gpt4o-benchmark-tab.png" alt-text="Screenshot showing the  benchmarks tab for gpt-4o." lightbox="../media/how-to/model-benchmarks/gpt4o-benchmark-tab.png":::

1. Select **Compare with more models**.

1. Switch to the **List view** to access more detailed results for each model.

    :::image type="content" source="../media/how-to/model-benchmarks/compare-view.png" alt-text="Screenshot showing an example of benchmark comparison view." lightbox="../media/how-to/model-benchmarks/compare-view.png":::

## Analyze benchmark results

When you're in the "Benchmarks" tab for a specific model, you can gather extensive information to better understand and interpret the benchmark results, including:

- **High-level aggregate scores**: These scores for AI quality, cost, latency, and throughput provide a quick overview of the model's performance.
- **Comparative charts**: These charts display the model's relative position compared to related models.
- **Metric comparison table**: This table presents detailed results for each metric.

    :::image type="content" source="../media/how-to/model-benchmarks/gpt4o-benchmark-tab-expand.png" alt-text="Screenshot showing benchmarks tab for gpt-4o." lightbox="../media/how-to/model-benchmarks/gpt4o-benchmark-tab-expand.png":::

By default, Foundry displays an average index across various metrics and datasets to provide a high-level overview of model performance.

To access benchmark results for a specific metric and dataset:

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

This feature enables side-by-side comparison of up to three models simultaneously across multiple dimensions including performance benchmarks, model detail specifications, supported endpoints, and feature support.

Use the dropdown to select models you want to compare.

If you want to learn even more about the model, you can **View details** or if you're ready to start using the model, you can **Deploy**.

:::image type="content" source="media/observability/model-benchmarks/compare-model-overview.png" alt-text="Screenshot showing the compare model experience in Microsoft Foundry." lightbox="media/observability/model-benchmarks/compare-model-overview.png":::

## View and analyze benchmarks from the model card

Once you've selected a model you're interested in whether from leaderboard or browsing the catalog, go to the **Benchmarks** tab to check the benchmark results for the model.
  
> [!NOTE]
> Benchmarking results conducted by Microsoft are available for select models in the model catalog. Benchmarking information reported by providers is included when available.

When you're in the "Benchmarks" tab for a specific model, you can gather extensive information to better understand and interpret the benchmark results with:

- **Public data benchmark results**: These are high-level aggregate scores for AI quality, safety, estimated cost, latency, and throughput provide a quick overview of the model's performance.
- **Comparative charts**: These charts display the model's relative position compared to related models.
- **Metric comparison table**: This table presents detailed results for each metric.

    :::image type="content" source="media/observability/model-benchmarks/benchmark-overview.png" alt-text="Screenshot showing the metric comparison table on the benchmarks tab." lightbox="media/observability/model-benchmarks/benchmark-overview.png":::

By default, Microsoft Foundry displays an average index across various metrics and datasets to provide a high-level overview of model performance.

To access benchmark results for a specific metric and dataset:

1. Select the expand button on the chart. The pop-up comparison chart reveals detailed information and offers greater flexibility for comparison.

1. Select the metric of interest and choose different datasets, based on your specific scenario. For more detailed definitions of the metrics and descriptions of the public datasets used to calculate results, select **Read more**.

For side-by-side model comparisons, you can [compare models](#compare-models) to evaluate features, performance metrics, and estimated costs across multiple models.

::: moniker-end

## Related content

- [Model leaderboards in Foundry portal](../concepts/model-benchmarks.md)
- [How to evaluate generative AI apps with Foundry](evaluate-generative-ai-app.md)
- [How to view evaluation results in Foundry portal](evaluate-results.md)
