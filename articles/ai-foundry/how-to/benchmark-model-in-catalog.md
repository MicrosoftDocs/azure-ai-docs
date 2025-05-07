---
title: Benchmark models in the model leaderboard of Azure AI Foundry portal
titleSuffix: Azure AI Foundry
description: In this article, you learn to compare benchmarks across models and datasets, using the model leaderboards (preview) and the benchmarks feature in Azure AI Foundry portal.
manager: scottpolly
ms.service: azure-ai-foundry
ms.custom:
  - ai-learning-hub
ms.topic: how-to
ms.date: 04/07/2025
ms.reviewer: changliu2
reviewer: changliu2
ms.author: lagayhar  
author: lgayhardt
---

# Compare and select models using the model leaderboard in Azure AI Foundry portal (preview)

[!INCLUDE [feature-preview](../includes/feature-preview.md)]

In this article, you learn to streamline your model selection process in the Azure AI Foundry [model catalog](../how-to/model-catalog-overview.md) by comparing models in the model leaderboards (preview) available in Azure AI Foundry portal. This comparison can help you make informed decisions about which models meet the requirements for your particular use case or application. You can compare models by viewing the following leaderboards:

- [Quality, cost, and performance leaderboards](#access-model-leaderboards) to quickly identify the model leaders along a single metric (quality, cost, or throughput);
- [Trade-off charts](#compare-models-in-the-trade-off-charts) to see how models perform on one metric versus another, such as quality versus cost;
- [Leaderboards by scenario](#view-leaderboards-by-scenario) to find the best leaderboards that suite your scenario.


## Prerequisites

- An Azure subscription with a valid payment method. Free or trial Azure subscriptions won't work. If you don't have an Azure subscription, create a [paid Azure account](https://azure.microsoft.com/pricing/purchase-options/pay-as-you-go) to begin.

- An [Azure AI Foundry project](create-projects.md).

## Access model leaderboards

[!INCLUDE [open-catalog](../includes/open-catalog.md)]

4. Go to the **Model leaderboards** section of the model catalog. This section displays the top three model leaders ranked along [quality](../concepts/model-benchmarks.md#quality-benchmarks-of-language-models), [cost](../concepts/model-benchmarks.md#cost-benchmarks-of-language-models), and [performance](../concepts/model-benchmarks.md#performance-benchmarks-of-language-models). You can select any of these models to check out more details.

    :::image type="content" source="../media/how-to/model-benchmarks/leaderboard-entry-select-model.png" alt-text="Screenshot showing the selected model from entry point of leaderboards on the model catalog homepage." lightbox="../media/how-to/model-benchmarks/leaderboard-entry-select-model.png":::

1. From the **Model leaderboards** section of the model catalog, select **Browse leaderboards**  to go to the [model leaderboards landing page](https://aka.ms/model-leaderboards) to see the full suite of leaderboards that are available.

    :::image type="content" source="../media/how-to/model-benchmarks/leaderboard-entry.png" alt-text="Screenshot showing the entry point from model catalog into model leaderboards." lightbox="../media/how-to/model-benchmarks/leaderboard-entry.png"::: 

    The homepage displays leaderboard highlights for model selection criteria. Quality is the most common criterion for model selection, followed by cost and performance.

    :::image type="content" source="../media/how-to/model-benchmarks/leaderboard-highlights.png" alt-text="Screenshot showing the highlighted leaderboards in quality, cost, and performance." lightbox="../media/how-to/model-benchmarks/leaderboard-highlights.png":::


### Compare models in the trade-off charts

Trade-off charts allow you to compare models based on the criteria that you care more about. Suppose you care more about cost than quality and you discover that the highest quality model isn't the cheapest model, you might need to make trade-offs among quality, cost, and performance criteria. In the trade-off charts, you can compare how models perform along two metrics at a glance. 

1. Select the **Models selected** dropdown menu to add or remove models from the trade-off chart.
1. Select the **Quality vs. Throughput** tab and the **Throughput vs Cost** tab to view those charts for your selected models.
1. Select **Compare between metrics** to access more detailed results for each model.

:::image type="content" source="../media/how-to/model-benchmarks/leaderboard-trade-off.png" alt-text="Screenshot showing the trade-off charts in quality, cost, and performance." lightbox="../media/how-to/model-benchmarks/leaderboard-trade-off.png":::

### View leaderboards by scenario

Suppose you have a scenario that requires certain model capabilities. For example, say you're building a question-and-answering chatbot that requires good question-and-answering and reasoning capabilities. You might find it useful to compare models in these leaderboards that are backed by capability-specific benchmarks.

:::image type="content" source="../media/how-to/model-benchmarks/leaderboard-by-scenario.png" alt-text="Screenshot showing the quality leaderboards by scenarios." lightbox="../media/how-to/model-benchmarks/leaderboard-by-scenario.png":::


Once you've explored the leaderboards, you can decide on a model to use. 

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

By default, Azure AI Foundry displays an average index across various metrics and datasets to provide a high-level overview of model performance.

To access benchmark results for a specific metric and dataset:

1. Select the expand button on the chart. The pop-up comparison chart reveals detailed information and offers greater flexibility for comparison.

    :::image type="content" source="../media/how-to/model-benchmarks/expand-to-detailed-metric.png" alt-text="Screenshot showing the expand button to select for a detailed comparison chart." lightbox="../media/how-to/model-benchmarks/expand-to-detailed-metric.png":::

1. Select the metric of interest and choose different datasets, based on your specific scenario. For more detailed definitions of the metrics and descriptions of the public datasets used to calculate results, select **Read more**.

    :::image type="content" source="../media/how-to/model-benchmarks/comparison-chart-per-metric-data.png" alt-text="Screenshot showing the comparison chart with a specific metric and dataset." lightbox="../media/how-to/model-benchmarks/comparison-chart-per-metric-data.png":::


## Evaluate benchmark results with your data

The previous sections showed the benchmark results calculated by Microsoft, using public datasets. However, you can try to regenerate the same set of metrics with your data.

1. Return to the **Benchmarks** tab in the model card.
1. Select **Try with your own data** to [evaluate the model with your data](evaluate-generative-ai-app.md#model-and-prompt-evaluation). Evaluation on your data helps you see how the model performs in your particular scenarios.

    :::image type="content" source="../media/how-to/model-benchmarks/try-with-your-own-data.png" alt-text="Screenshot showing the button to select for evaluating with your own data." lightbox="../media/how-to/model-benchmarks/try-with-your-own-data.png":::

## Related content

- [Model leaderboards in Azure AI Foundry portal](../concepts/model-benchmarks.md)
- [How to evaluate generative AI apps with Azure AI Foundry](evaluate-generative-ai-app.md)
- [How to view evaluation results in Azure AI Foundry portal](evaluate-results.md)
