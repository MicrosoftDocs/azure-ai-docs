---
title: How to use model benchmarking in Azure AI Studio
titleSuffix: Azure AI Studio
description: In this article, you learn to compare benchmarks across models and datasets, using the model benchmarks tool in Azure AI Studio.
manager: scottpolly
ms.service: azure-ai-studio
ms.custom:
  - ai-learning-hub
ms.topic: how-to
ms.date: 10/29/2024
ms.reviewer: jcioffi
ms.author: mopeakande
author: msakande
---

# How to benchmark models in Azure AI Studio

[!INCLUDE [feature-preview](../includes/feature-preview.md)]

In this article, you learn to compare benchmarks across models and datasets, using the model benchmarks tool in Azure AI Studio. You also learn to analyze benchmarking results and to perform benchmarking with your own data. Benchmarking can help you make informed decisions about which models meet the requirements for your particular use case or application.

## Prerequisites

- An Azure subscription with a valid payment method. Free or trial Azure subscriptions won't work. If you don't have an Azure subscription, create a [paid Azure account](https://azure.microsoft.com/pricing/purchase-options/pay-as-you-go) to begin.

- An [Azure AI Studio project](create-projects.md).

## Access model benchmarks through the model catalog

Azure AI supports model benchmarking for select models that are popular and most frequently used. Follow these steps to use detailed benchmarking results to compare and select models directly from the AI Studio model catalog:

[!INCLUDE [open-catalog](../includes/open-catalog.md)]

4. Select the model you're interested in. For example, select **gpt-4o**. This action opens the model's overview page.

    > [!TIP]
    > From the model catalog, you can show the models that have benchmarking available by using the **Collections** filter and selecting **Benchmark results**. These models have a _benchmarks_ icon that looks like a histogram.

1. Go to the **Benchmarks** tab to check the benchmark results for the model.
  
    <!-- gpt4o-benchmark-tab.png alt-text: benchmarks tab for gpt-4o.  -->

1. Return to the homepage of the model catalog.
1. Select **Compare models** on the model catalog's homepage to explore models with benchmark support, view their metrics, and analyze the trade-offs among different models. This analysis can inform your selection of the model that best fits your requirements.

    <!-- compare-models-model-catalog.png  alt-text: Compare model button on model catalog main page.  -->

1. Select your desired tasks and specify the dimensions of interest, such as _AI Quality_ versus _Cost_, to evaluate the trade-offs among different models.
1. You can switch to the **List view** to access more detailed results for each model.

    <!-- compare-view.png alt-text: Example of benchmark compare view.  -->

## Analyze benchmark results

When you're in the "Benchmarks" tab for a specific model, you can gather extensive information to better understand and interpret the benchmark results, including:

- **High-level aggregate scores**: These scores for AI quality, cost, latency, and throughput provide a quick overview of the model's performance.
- **Comparative charts**: These charts display the model's relative position compared to related models.
- **Metric comparison table**: This table presents detailed results for each metric.

    <!-- gpt4o-benchmark-tab-expand.png alt-text: benchmarks tab for gpt-4o -->

By default, AI Studio displays an average index across various metrics and datasets to provide a high-level overview of model performance. 

To access benchmark results for a specific metric and dataset:

1. Select the expand button on the chart. The pop-up comparison chart reveals detailed information and offers greater flexibility for comparison.

    <!-- expand-to-detailed-metric.png alt-text: click the expand button to show the detailed comparison chart  -->

1. Select the metric of interest and choose different datasets, based on your specific scenario. For more detailed definitions of the metrics and descriptions of the public datasets used to calculate results, select **Read more**.

    <!-- comparison-chart-per-metric-data.png alt-text: the comparison chart with specific metric and dataset   -->


## Evaluate benchmark results with your data

The previous sections showed the benchmark results calculated by Microsoft, using public datasets. However, you can try to regenerate the same set of metrics with your data.

1. Return to the **Benchmarks** tab in the model card.
1. Select **Try with your own data** to evaluate the model with your data. Evaluation on your data helps you see how the model performs in your particular scenarios.

    <!-- try-with-your-own-data.png alt-text: evaluate with your own data button -->

## Related content

- [Model benchmarks in Azure AI Studio](../concepts/model-benchmarks.md)
- [How to evaluate generative AI apps with Azure AI Studio](evaluate-generative-ai-app.md)
- [How to view evaluation results in Azure AI Studio](evaluate-results.md)
