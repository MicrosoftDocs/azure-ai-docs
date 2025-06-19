---
title: Explore model leaderboards in Azure AI Foundry portal
titleSuffix: Azure AI Foundry
description: This article introduces benchmarking capabilities and model leaderboards (preview) in Azure AI Foundry portal.
manager: scottpolly
ms.service: azure-ai-foundry
ms.custom:
  - ai-learning-hub
ms.topic: concept-article
ms.date: 04/04/2025
ms.reviewer: changliu2
ms.author: lagayhar  
author: lgayhardt
---

# Model leaderboards in Azure AI Foundry portal (preview)

[!INCLUDE [feature-preview](../includes/feature-preview.md)]


Model leaderboards (preview) in Azure AI Foundry portal allow you to streamline the model selection process in the Azure AI Foundry [model catalog](../how-to/model-catalog-overview.md). The model leaderboards, backed by industry-standard benchmarks can help you to find the best model for your custom AI solution. From the model leaderboards section of the model catalog, you can [browse leaderboards](https://aka.ms/model-leaderboards) to compare available models as follows:

- [Quality, safety, cost, and performance leaderboards](../how-to/benchmark-model-in-catalog.md#access-model-leaderboards) to quickly identify the model leaders along a single metric (quality, safety, cost, or throughput);
- [Trade-off charts](../how-to/benchmark-model-in-catalog.md#compare-models-in-the-trade-off-charts) to see how models perform on one metric versus another, such as quality versus cost;
- [Leaderboards by scenario](../how-to/benchmark-model-in-catalog.md#view-leaderboards-by-scenario) to find the best leaderboards that suite your scenario.

Whenever you find a model to your liking, you can select it and zoom into the **Detailed benchmarking results** of the model within the model catalog. If satisfied with the model, you can deploy it, try it in the playground, or evaluate it on your data. The leaderboards support benchmarking across text language models (large language models (LLMs) and small language models (SLMs)) and embedding models.


Model benchmarks assess LLMs and SLMs across the following categories: quality, safety, cost, and throughput. In addition, we assess the quality of embedding models using standard benchmarks. The leaderboards are updated regularly as better and more unsaturated benchmarks are onboarded, and as new models are added to the model catalog.


## Quality benchmarks of language models

Azure AI assesses the quality of LLMs and SLMs using accuracy scores from standard, comprehensive benchmark datasets measuring model capabilities such as reasoning, knowledge, question answering, math, and coding. 

| Index | Description                                                                                                                                                                                                                  |
|-------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Quality index | Quality index is calculated by averaging applicable accuracy scores (exact_match, pass@1, arena_hard) over comprehensive, standard benchmark datasets. | 

Quality index is provided on a scale of zero to one. Higher values of quality index are better. The datasets included in quality index are: 

| Dataset Name       | Leaderboard Scenario |
|--------------------|----------------------|
| arena_hard        | QA                   |
| bigbench_hard     | Reasoning            |
| gpqa              | QA                   |
| humanevalplus     | Coding               |
| ifeval            | Reasoning            |
| math              | Math                 |
| mbppplus          | Coding               |
| mmlu_pro          | General Knowledge    |



See more details in accuracy scores:

| Metric | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
|--------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Accuracy | Accuracy scores are available at the dataset and the model levels. At the dataset level, the score is the average value of an accuracy metric computed over all examples in the dataset. The accuracy metric used is `exact-match` in all cases, except for the _HumanEval_  and _MBPP_ datasets that use a `pass@1` metric. Exact match compares model generated text with the correct answer according to the dataset, reporting one if the generated text matches the answer exactly and zero otherwise. The `pass@1` metric measures the proportion of model solutions that pass a set of unit tests in a code generation task. At the model level, the accuracy score is the average of the dataset-level accuracies for each model. |

Accuracy scores are provided on a scale of zero to one. Higher values are better.


## Safety benchmarks of language models

To guide the selection of safety benchmarks for evaluation, we apply a structured filtering and validation process designed to ensure both relevance and rigor. A benchmark qualifies for onboarding if it addresses high-priority risks. For safety leaderboards, we look at different benchmarks that can be considered reliable enough to provide some signals on certain topics of interest as they relate to safety. We select [HarmBench](https://github.com/centerforaisafety/HarmBench) to proxy model safety, and organize scenario leaderboards as follows: 

| Dataset Name       | Leaderboard Scenario |    Metric   | Interpretation   |
|--------------------|----------------------|----------------------|----------------------|
| HarmBench (standard)        | Standard harmful behaviors                   |  Attack Success Rate | Lower values means better robustness against attacks designed to illicit standard harmful content   |
| HarmBench (contextual)    | Contextually harmful behaviors            | Attack Success Rate | Lower values means better robustness against attacks designed to illicit contextually harmful content |
| HarmBench (copyright violations)             | Copyright violations                   | Attack Success Rate |  Lower values means better robustness against attacks designed to illicit copyright violations|
| WMDP     | Knowledge in sensitive domains               | Accuracy |  Higher values denotes more knowledge in sensitive domains (cybersecurity, biosecurity, and chemical security) |
| Toxigen            | Ability to detect toxic content            | F1 Score |  Higher values means better ability to detect toxic content |

### Model harmful behaviors 
The [HarmBench](https://github.com/centerforaisafety/HarmBench) benchmark measures model harmful behaviors and includes prompts to illicit harmful behavior from model. As it relates to safety, the benchmark covers 7 semantic categories of behavior: 
- Cybercrime & Unauthorized Intrusion
- Chemical & Biological Weapons/Drugs
- Copyright Violations
- Misinformation & Disinformation
- Harassment & Bullying
- Illegal Activities
- General Harm
  
These 7 categories can be summarized into 3 functional categories
- standard harmful behaviors
- contextually harmful behaviors
- copyright violations

Each functional category is featured in a separate scenario leaderboard. We use direct prompts from HarmBench (no attacks) and HarmBench evaluators to calculate Attack Success Rate (ASR). Lower ASR values means safer models. We do not explore any attack strategy for evaluation, and model benchmarking is performed with Azure AI Content Safety Filter turned off. 


### Model ability to detect toxic content
[Toxigen](https://github.com/microsoft/TOXIGEN) is a large-scale machine-generated dataset for adversarial and implicit hate speech detection. It contains implicitly toxic and benign sentences mentioning 13 minority groups. We use the annotated samples from Toxigen for evaluation and calculate F1 scores to measure classification performance. Scoring higher on this dataset means that a model is better at detecting toxic content. Model benchmarking is performed with Azure AI Content Safety Filter turned off.

### Model knowledge in sensitive domains
The [Weapons of Mass Destruction Proxy](https://github.com/centerforaisafety/wmdp) (WMDP) benchmark measures model knowledge of in sensitive domains including biosecurity, cybersecurity, and chemical security. The leaderboard uses average accuracy scores across cybersecurity, biosecurity, and chemical security. A higher WMDP accuracy score denotes more knowledge of dangerous capabilities (worse behavior from a safety standpoint). Model benchmarking is performed with the default Azure AI Content Safety filters on. These safety filters detect and block content harm in violence, self-harm, sexual, hate and unfairness, but don't target categories in cybersecurity, biosecurity, and chemical security.

### Limitations of safety benchmarks
We understand and acknowledge that safety is a complex topic and has several dimensions. No single current open-source benchmarks can test or represent the full safety of a system in different scenarios. Additionally, most of these benchmarks suffer from saturation, or misalignment between benchmark design and the risk definition, can lack clear documentation on how the target risks are conceptualized and operationalized, making it difficult to assess whether the benchmark accurately captures the nuances of the risks. This limitation can lead to either overestimating or underestimating model performance in real-world safety scenarios. 

## Performance benchmarks of language models

Performance metrics are calculated as an aggregate over 14 days, based on 24 trails (two requests per trail) sent daily with a one-hour interval between every trail. The following default parameters are used for each request to the model endpoint:

| Parameter                             | Value                                                                                              | Applicable For                                                                                                                                                                                                                              |
|---------------------------------------|----------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Region                                | East US/East US2                                                                                   | [Standard deployments](../how-to/model-catalog-overview.md#standard-deployment-pay-per-token-offer-billing) and [Azure OpenAI](/azure/ai-services/openai/overview)                                                                                          |
| Tokens per minute (TPM) rate limit    | 30k (180 RPM based on Azure OpenAI) for non-reasoning and 100k for reasoning models <br> N/A (standard deployments) | For Azure OpenAI models, selection is available for users with rate limit ranges based on deployment type (standard, global, global standard, and so on.) <br> For standard deployments, this setting is abstracted.                             |
| Number of requests                    | Two requests in a trail for every hour (24 trails per day)                                         | Standard deployments, Azure OpenAI                                                                                                                                                                                                               |
| Number of trails/runs                 | 14 days with 24 trails per day for 336 runs                                                        | Standard deployments, Azure OpenAI                                                                                                                                                                                                               |
| Prompt/Context length                 | Moderate length                                                                                    | Standard deployments, Azure OpenAI                                                                                                                                                                                                               |
| Number of tokens processed (moderate) | 80:20 ratio for input to output tokens, that is, 800 input tokens to 200 output tokens.            | Standard deployments, Azure OpenAI                                                                                                                                                                                                               |
| Number of concurrent requests         | One (requests are sent sequentially one after other)                                               | Standard deployments, Azure OpenAI                                                                                                                                                                                                               |
| Data                                  | Synthetic (input prompts prepared from static text)                                                | Standard deployments, Azure OpenAI                                                                                                                                                                                                               |
| Region                                | East US/East US2                                                                                   | Standard deployments and Azure OpenAI                                                                                                                                                                                                            |
| Deployment type                       | Standard                                                                                           | Applicable only for Azure OpenAI                                                                                                                                                                                                            |
| Streaming                             | True                                                                                               | Applies to standard deployments and Azure OpenAI. For models deployed via [managed compute](../how-to/model-catalog-overview.md#managed-compute), or for endpoints when streaming is not supported TTFT is represented as P50 of latency metric. |
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

## Cost benchmarks of language models

Cost calculations are estimates for using an LLM or SLM model endpoint hosted on the Azure AI platform. Azure AI supports displaying the cost of standard deployments and Azure OpenAI models. Because these costs are subject to change, we refresh our cost calculations on a regular cadence.

The cost of LLMs and SLMs is assessed across the following metrics:

| Metric | Description |
|--------|-------------|
| Cost per input tokens | Cost for standard deployment for 1 million input tokens |
| Cost per output tokens | Cost for standard deployment for 1 million output tokens |
| Estimated cost | Cost for the sum of cost per input tokens and cost per output tokens, with a ratio of 3:1. |

Azure AI also displays the cost index as follows:

| Index | Description |
|-------|-------------|
| Cost index | Estimated cost. Lower values are better. |

## Quality benchmarks of embedding models

The quality index of embedding models is defined as the averaged accuracy scores of a comprehensive set of standard benchmark datasets targeting Information Retrieval, Document Clustering, and Summarization tasks.

See more details in accuracy score definitions specific to each dataset:

| Metric | Description |
|--------|-------------|
| Accuracy | Accuracy is the proportion of correct predictions among the total number of predictions processed. |
| F1 Score | F1 Score is the weighted mean of the precision and recall, where the best value is one (perfect precision and recall), and the worst is zero. |
| Mean average precision (MAP) | MAP evaluates the quality of ranking and recommender systems. It measures both the relevance of suggested items and how good the system is at placing more relevant items at the top. Values can range from zero to one, and the higher the MAP, the better the system can place relevant items high in the list. |
| Normalized discounted cumulative gain (NDCG) | NDCG evaluates a machine learning algorithm's ability to sort items based on relevance. It compares rankings to an ideal order where all relevant items are at the top of the list, where k is the list length while evaluating ranking quality. In our benchmarks, k=10, indicated by a metric of `ndcg_at_10`, meaning that we look at the top 10 items. |
| Precision | Precision measures the model's ability to identify instances of a particular class correctly. Precision shows how often a machine learning model is correct when predicting the target class. |
| Spearman correlation | Spearman correlation based on cosine similarity is calculated by first computing the cosine similarity between variables, then ranking these scores and using the ranks to compute the Spearman correlation. |
| V measure | V measure is a metric used to evaluate the quality of clustering. V measure is calculated as a harmonic mean of homogeneity and completeness, ensuring a balance between the two for a meaningful score. Possible scores lie between zero and one, with one being perfectly complete labeling. |

## Calculation of scores

### Individual scores

Benchmark results originate from public datasets that are commonly used for language model evaluation. In most cases, the data is hosted in GitHub repositories maintained by the creators or curators of the data. Azure AI evaluation pipelines download data from their original sources, extract prompts from each example row, generate model responses, and then compute relevant accuracy metrics.

Prompt construction follows best practices for each dataset, as specified by the paper introducing the dataset and industry standards. In most cases, each prompt contains several _shots_, that is, several examples of complete questions and answers to prime the model for the task. The evaluation pipelines create shots by sampling questions and answers from a portion of the data held out from evaluation.

## Related content

- [Compare and select models using the model leaderboard in Azure AI Foundry portal](../how-to/benchmark-model-in-catalog.md)
- [Model catalog and collections in Azure AI Foundry portal](../how-to/model-catalog-overview.md)
