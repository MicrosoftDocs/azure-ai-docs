---
title: Explore model benchmarks in Azure AI Foundry portal
titleSuffix: Azure AI Foundry
description: This article introduces benchmarking capabilities and the model benchmarks experience in Azure AI Foundry portal.
manager: scottpolly
ms.service: azure-ai-foundry
ms.custom:
  - ai-learning-hub
  - ignite-2024
ms.topic: concept-article
ms.date: 11/11/2024
ms.reviewer: jcioffi
ms.author: mopeakande
author: msakande
---

# Model benchmarks in Azure AI Foundry portal

[!INCLUDE [feature-preview](../includes/feature-preview.md)]

In Azure AI Foundry portal, you can compare benchmarks across models and datasets available in the industry to decide which one meets your business scenario. You can directly access detailed benchmarking results within the model catalog. Whether you already have models in mind or you're exploring models, the benchmarking data in Azure AI empowers you to make informed decisions quickly and efficiently.

Azure AI supports model benchmarking for select models that are popular and most frequently used. Supported models have a _benchmarks_ icon that looks like a histogram. You can find these models in the model catalog by using the **Collections** filter and selecting **Benchmark results**. You can then use the search functionality to find specific models.

:::image type="content" source="../media/how-to/model-benchmarks/access-model-catalog-benchmark.png" alt-text="Screenshot showing how to filter for benchmark models in the model catalog homepage." lightbox="../media/how-to/model-benchmarks/access-model-catalog-benchmark.png":::

Model benchmarks help you make informed decisions about the sustainability of models and datasets before you initiate any job. The benchmarks are a curated list of the best-performing models for a task, based on a comprehensive comparison of benchmarking metrics. Azure AI Foundry provides the following benchmarks for models, based on model catalog collections:

- Benchmarks across large language models (LLMs) and small language models (SLMs)  
- Benchmarks across embedding models

## Benchmarking of LLMs and SLMs

Model benchmarks assess LLMs and SLMs across the following categories: quality, performance, and cost. The benchmarks are updated regularly as new metrics and datasets are added to existing models, and as new models are added to the model catalog.

### Quality

Azure AI assesses the quality of LLMs and SLMs across various metrics that are grouped into two main categories: accuracy, and prompt-assisted metrics:

For accuracy metric:

| Metric | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
|--------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Accuracy | Accuracy scores are available at the dataset and the model levels. At the dataset level, the score is the average value of an accuracy metric computed over all examples in the dataset. The accuracy metric used is `exact-match` in all cases, except for the _HumanEval_  and _MBPP_ datasets that uses a `pass@1` metric. Exact match compares model generated text with the correct answer according to the dataset, reporting one if the generated text matches the answer exactly and zero otherwise. The `pass@1` metric measures the proportion of model solutions that pass a set of unit tests in a code generation task. At the model level, the accuracy score is the average of the dataset-level accuracies for each model. |

For prompt-assisted metrics:

| Metric | Description |
|--------|-------------|
| Coherence | Coherence evaluates how well the language model can produce output that flows smoothly, reads naturally, and resembles human-like language. |
| Fluency | Fluency evaluates the language proficiency of a generative AI's predicted answer. It assesses how well the generated text adheres to grammatical rules, syntactic structures, and appropriate usage of vocabulary, resulting in linguistically correct and natural-sounding responses. |
| GPTSimilarity | GPTSimilarity is a measure that quantifies the similarity between a ground truth sentence (or document) and the prediction sentence generated by an AI model. The metric is calculated by first computing sentence-level embeddings, using the embeddings API for both the ground truth and the model's prediction. These embeddings represent high-dimensional vector representations of the sentences, capturing their semantic meaning and context. |
| Groundedness | Groundedness measures how well the language model's generated answers align with information from the input source. |
| Relevance | Relevance measures the extent to which the language model's generated responses are pertinent and directly related to the given questions. |

Azure AI also displays the quality index as follows:

| Index | Description                                                                                                                                                                                                                  |
|-------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Quality index | Quality index is calculated by average of applicable accuracy scores from comprehensive benchmark datasets measuring model capabilities such as reasoning, knowledge, and coding. Higher values of quality index are better. |

The quality index represents the average score of the applicable primary metric (accuracy, pass@1, arena_hard) over 15+ standard datasets and is provided on a scale of zero to one.

Quality index: 

- Accuracy (for example, exact match or `pass@k`). Ranges from zero to one.

The stability of the quality index value provides an indicator of the overall quality of the model.

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
