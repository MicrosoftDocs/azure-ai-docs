---
title: Explore model leaderboards in Azure AI Foundry portal
titleSuffix: Azure AI Foundry
description: This article introduces benchmarking capabilities and the model benchmarks experience in Azure AI Foundry portal.
manager: scottpolly
ms.service: azure-ai-foundry
ms.custom:
  - ai-learning-hub
  - ignite-2024
ms.topic: concept-article
ms.date: 11/11/2024
ms.reviewer: changliu2
ms.author: mopeakande
author: msakande
---

# Model leaderboards in Azure AI Foundry portal

[!INCLUDE [feature-preview](../includes/feature-preview.md)]

In Azure AI Foundry portal, we offer a wide range of models in [model catalog](../how-to
/model-catalog-overview.md) for your generative AI applications. To streamline your model selection experience, now you can leverage our model leaderboards backed by industry-standard benchmarks to find the best model for your custom AI solution. Within [model leaderboards](https://aka.ms/model-leaderboards) page, you can compare models available on Foundry using:
- [Quality, cost, and performance leaderboards](#quality-cost-and-performance-leaderboards) to quickly identify the model leaders in a single criterion;
- [Trade-off charts](#trade-off-charts) to see how models perform in quality versus cost;
- [Leaderboards by scenario](#leaderboards-by-scenario) to find the best leaderboards that suites your scenario.

Whenever you find a model to your liking, you can simply select a model and zoom into [detailed benchmarking results](../how-to
/benchmark-model-in-catalog.md) of individual models within the model catalog. Once you find a model to your liking, you can go and deploy your model, try it in playgorund, or evaluate it on your own data. Whether you already have models in mind or you're exploring models, model leaderboards in Azure AI Foundry empowers you to make data-driven decisions with a streamlined, intuitive experience for model selection.

## Quality, cost, and performance leaderboards

From model catalog landing page, you will see the top 3 model leaders in [quality](#quality), [cost](#cost), and [performance](#cost) criteria.    
:::image type="content" source="../media/how-to/model-benchmarks/leaderboard-entry.png" alt-text="Screenshot showing the entry point from model catalog into model leaderboards." lightbox="../media/how-to/model-benchmarks/leaderboard-entry.png":::

Wherever you are in your selection journey, you can select a model to you liking to check out more details:

:::image type="content" source="../media/how-to/model-benchmarks/leaderboard-entry-select-model.png" alt-text="Screenshot showing the selected model from entry point of leaderboards on model catalog." lightbox="../media/how-to/model-benchmarks/leaderboard-entry-select-model.png":::

You can select "Browse leaderboards" to see the full suite of leaderboards we offer. [Quality](#quality) is the most common criterion for model selection:  

:::image type="content" source="../media/how-to/model-benchmarks/leaderboard-quality.png" alt-text="Screenshot showing the quality leaderboards." lightbox="../media/how-to/model-benchmarks/leaderboard-quality.png":::

Then comes [cost](#cost) and [performance](#cost) leaderboards: 
:::image type="content" source="../media/how-to/model-benchmarks/leaderboard-highlights.png" alt-text="Screenshot showing the highlighted bar charts for quality, cost, and performance leaders." lightbox="../media/how-to/model-benchmarks/leaderboard-highlights.png":::


## Quality, cost, and performance trade-off charts

You may find that the most high-quality model may not be the cheapest model, and you need to make trade-offs in among quality, cost, and performance criteria, for example, you may care more about cost than quality. In the trade-off charts, you can see how models perform in these criteria among others. You can also select or deselect models, toggle between charts, and even more metrics in "Compare between metrics"    

:::image type="content" source="../media/how-to/model-benchmarks/leaderboard-trade-off.png" alt-text="Screenshot showing the trade-off charts in quality, cost, and performance." lightbox="../media/how-to/model-benchmarks/leaderboard-trade-off.png":::


## Quality leaderboards by scenario

You may have a specific scenario that require certain model capabilities. For example, you are building a question-and-answering chatbot that require good question-and-answering and reasoning capabilities. You can find it useful to compare models in these leaderboards backed by capability-specific benchmarks.
:::image type="content" source="../media/how-to/model-benchmarks/leaderboard-by-scenario.png" alt-text="Screenshot showing the quality leaderboards by scenarios." lightbox="../media/how-to/model-benchmarks/leaderboard-by-scenario.png":::

We support both text language models and embedding models.  

- Benchmarks across large language models (LLMs) and small language models (SLMs)  
- Benchmarks across embedding models

## Benchmarking of LLMs and SLMs

Model benchmarks assess LLMs and SLMs across the following categories: quality, performance, and cost. The benchmarks are updated regularly as new datasets and associated metrics are added to existing models, and as new models are added to the model catalog.

### Quality

Azure AI assesses the quality of LLMs and SLMs using accuracy scores from standard, comprehensive benchmark datasets measuring model capabilities such as reasoning, knowledge, question answering, math, and coding. 

| Index | Description                                                                                                                                                                                                                  |
|-------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Quality index | Quality index is calculated by averaging applicable accuracy scores (exact_match, pass@1, arena_hard) over 15 standard datasets of applicable accuracy scores. Datasets include BoolQ, HellaSwag, BoolQ, HellaSwag, OpenBookQA, PIQA, Social IQA, Winogrande, SQuAD v2, TruthfulQA (Gen), TruthfulQA (MC), HumanEval, GSM8K, MMLU (Humanities), MMLU (Other), MMLU (Social Sciences), MMLU (STEM). | 

Quality index is provided on a scale of zero to one. Higher values of quality index are better.

For accuracy scores:

| Metric | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
|--------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Accuracy | Accuracy scores are available at the dataset and the model levels. At the dataset level, the score is the average value of an accuracy metric computed over all examples in the dataset. The accuracy metric used is `exact-match` in all cases, except for the _HumanEval_  and _MBPP_ datasets that uses a `pass@1` metric. Exact match compares model generated text with the correct answer according to the dataset, reporting one if the generated text matches the answer exactly and zero otherwise. The `pass@1` metric measures the proportion of model solutions that pass a set of unit tests in a code generation task. At the model level, the accuracy score is the average of the dataset-level accuracies for each model. |

Accuracy scores are provided on a scale of zero to one. Higher values are better.


### Performance

Performance metrics are calculated as an aggregate over 14 days, based on 24 trails (two requests per trail) sent daily with a one-hour interval between every trail. The following default parameters are used for each request to the model endpoint:

| Parameter                             | Value                                                                                              | Applicable For                                                                                                                                                                                                                              |
|---------------------------------------|----------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Region                                | East US/East US2                                                                                   | [Serverless APIs](../how-to/model-catalog-overview.md#serverless-api-pay-per-token-billing) and [Azure OpenAI](/azure/ai-services/openai/overview)                                                                                          |
| Tokens per minute (TPM) rate limit    | 30k (180 RPM based on Azure OpenAI) for non-reasoning and 100k for reasoning models <br> N/A (serverless APIs) | For Azure OpenAI models, selection is available for users with rate limit ranges based on deployment type (standard, global, global standard, and so on.) <br> For serverless APIs, this setting is abstracted.                             |
| Number of requests                    | Two requests in a trail for every hour (24 trails per day)                                         | Serverless APIs, Azure OpenAI                                                                                                                                                                                                               |
| Number of trails/runs                 | 14 days with 24 trails per day for 336 runs                                                        | Serverless APIs, Azure OpenAI                                                                                                                                                                                                               |
| Prompt/Context length                 | Moderate length                                                                                    | Serverless APIs, Azure OpenAI                                                                                                                                                                                                               |
| Number of tokens processed (moderate) | 80:20 ratio for input to output tokens, that is, 800 input tokens to 200 output tokens.            | Serverless APIs, Azure OpenAI                                                                                                                                                                                                               |
| Number of concurrent requests         | One (requests are sent sequentially one after other)                                               | Serverless APIs, Azure OpenAI                                                                                                                                                                                                               |
| Data                                  | Synthetic (input prompts prepared from static text)                                                | Serverless APIs, Azure OpenAI                                                                                                                                                                                                               |
| Region                                | East US/East US2                                                                                   | Serverless APIs and Azure OpenAI                                                                                                                                                                                                            |
| Deployment type                       | Standard                                                                                           | Applicable only for Azure OpenAI                                                                                                                                                                                                            |
| Streaming                             | True                                                                                               | Applies to serverless APIs and Azure OpenAI. For models deployed via [managed compute](../how-to/model-catalog-overview.md#managed-compute), or for endpoints when streaming is not supported TTFT is represented as P50 of latency metric. |
| SKU                                   | Standard_NC24ads_A100_v4 (24 cores, 220GB RAM, 64GB storage)                                       | Applicable only for Managed Compute (to estimate the cost and perf metrics)                                                                                                                                                                 |

The performance of LLMs and SLMs is assessed across the following metrics:

| Metric | Description                                                                                                                                                                                                                                                                                        |
|--------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Latency mean | Average time in seconds taken for processing a request, computed over multiple requests. To compute this metric, we send a request to the endpoint every hour, for two weeks, and compute the average.                                                                                             |
| Latency P50 | 50th percentile value (the median) of latency (the time taken between the request and when we receive the entire response with a successful code). For example, when we send a request to the endpoint, 50% of the requests are completed in 'x' seconds, with 'x' being the latency measurement.  |
| Latency P90 | 90th percentile value of latency (the time taken between the request and when we receive the entire response with a successful code). For example, when we send a request to the endpoint, 90% of the requests are completed in 'x' seconds, with 'x' being the latency measurement.               |
| Latency P95 | 95th percentile value of latency (the time taken between the request and when we receive the entire response with a successful code). For example, when we send a request to the endpoint, 95% of the requests are complete in 'x' seconds, with 'x' being the latency measurement.                |
| Latency P99 | 99th percentile value of latency (the time taken between the request and when we receive the entire response with a successful code). For example, when we send a request to the endpoint, 99% of the requests are complete in 'x' seconds, with 'x' being the latency measurement.                |
| Throughput GTPS | Generated tokens per second (GTPS) is the number of output tokens that are getting generated per second from the time the request is sent to the endpoint.                                                                                                                                         |
| Throughput TTPS | Total tokens per second (TTPS) is the number of total tokens processed per second including both from the input prompt and generated output tokens. For models which do not support streaming, time to first token (ttft) represents the P50 value of latency (time taken to receive the response) |
| Latency TTFT | Total time to first token (TTFT) is the time taken for the first token in the response to be returned from the endpoint when streaming is enabled.                                                                                                                                                 |
| Time between tokens | This metric is the time between tokens received.                                                                                                                                                                                                                                                   |

Azure AI also displays performance indexes for latency and throughput as follows:

| Index | Description |
|-------|-------------|
| Latency index | Mean time to first token. Lower values are better. |
| Throughput index | Mean generated tokens per second. Higher values are better. |

For performance metrics like latency or throughput, the time to first token and the generated tokens per second give a better overall sense of the typical performance and behavior of the model. We refresh our performance numbers on regular cadence.

### Cost

Cost calculations are estimates for using an LLM or SLM model endpoint hosted on the Azure AI platform. Azure AI supports displaying the cost of serverless APIs and Azure OpenAI models. Because these costs are subject to change, we refresh our cost calculations on a regular cadence.

The cost of LLMs and SLMs is assessed across the following metrics:

| Metric | Description |
|--------|-------------|
| Cost per input tokens | Cost for serverless API deployment for 1 million input tokens |
| Cost per output tokens | Cost for serverless API deployment for 1 million output tokens |
| Estimated cost | Cost for the sum of cost per input tokens and cost per output tokens, with a ratio of 3:1. |

Azure AI also displays the cost index as follows:

| Index | Description |
|-------|-------------|
| Cost index | Estimated cost. Lower values are better. |

## Benchmarking of embedding models

Model benchmarks assess embedding models based on quality.

### Quality

The quality of embedding models is assessed across the following metrics:

| Metric | Description |
|--------|-------------|
| Accuracy | Accuracy is the proportion of correct predictions among the total number of predictions processed. |
| F1 Score | F1 Score is the weighted mean of the precision and recall, where the best value is one (perfect precision and recall), and the worst is zero. |
| Mean average precision (MAP) | MAP evaluates the quality of ranking and recommender systems. It measures both the relevance of suggested items and how good the system is at placing more relevant items at the top. Values can range from zero to one, and the higher the MAP, the better the system can place relevant items high in the list. |
| Normalized discounted cumulative gain (NDCG) | NDCG evaluates a machine learning algorithm's ability to sort items based on relevance. It compares rankings to an ideal order where all relevant items are at the top of the list, where k is the list length while evaluating ranking quality. In our benchmarks, k=10, indicated by a metric of `ndcg_at_10`, meaning that we look at the top 10 items. |
| Precision | Precision measures the model's ability to identify instances of a particular class correctly. Precision shows how often a machine learning model is correct when predicting the target class. |
| Spearman correlation | Spearman correlation based on cosine similarity is calculated by first computing the cosine similarity between variables, then ranking these scores and using the ranks to compute the Spearman correlation. |
| V measure | V measure is a metric used to evaluate the quality of clustering. V measure is calculated as a harmonic mean of homogeneity and completeness, ensuring a balance between the two for a meaningful score. Possible scores lie between zero and one, with one being perfectly complete labeling. |

### Calculation of scores

#### Individual scores

Benchmark results originate from public datasets that are commonly used for language model evaluation. In most cases, the data is hosted in GitHub repositories maintained by the creators or curators of the data. Azure AI evaluation pipelines download data from their original sources, extract prompts from each example row, generate model responses, and then compute relevant accuracy metrics.

Prompt construction follows best practices for each dataset, as specified by the paper introducing the dataset and industry standards. In most cases, each prompt contains several _shots_, that is, several examples of complete questions and answers to prime the model for the task. The evaluation pipelines create shots by sampling questions and answers from a portion of the data that's held out from evaluation.

## Related content

- [How to benchmark models in Azure AI Foundry portal](../how-to/benchmark-model-in-catalog.md)
- [Model catalog and collections in Azure AI Foundry portal](../how-to/model-catalog-overview.md)
