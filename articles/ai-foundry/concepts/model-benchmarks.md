---
title: Explore model leaderboards in Microsoft Foundry portal
titleSuffix: Microsoft Foundry
description: This article introduces benchmarking capabilities and model leaderboards (preview) in Microsoft Foundry portal.
ms.service: azure-ai-foundry
ms.custom:
  - ai-learning-hub
ms.topic: concept-article
ms.date: 11/18/2025
ms.reviewer: changliu2
ms.author: lagayhar  
author: lgayhardt
monikerRange: 'foundry-classic || foundry'
ai-usage: ai-assisted
# customer intent: As a developer or data scientist, I want to understand model leaderboards and benchmarking capabilities in Microsoft Foundry portal so I can compare and select the best models for my AI solutions.
---

# Model leaderboards in Microsoft Foundry portal (preview)

[!INCLUDE [version-banner](../includes/version-banner.md)]

[!INCLUDE [feature-preview](../includes/feature-preview.md)]

::: moniker range="foundry-classic"

Model leaderboards (preview) in Microsoft Foundry portal help you compare models in the Foundry [model catalog](foundry-models-overview.md) using industry-standard benchmarks. From the model leaderboards section of the model catalog, you can [browse leaderboards](https://aka.ms/model-leaderboards) to compare available models by:

- [Quality, safety, cost, and performance leaderboards](../how-to/benchmark-model-in-catalog.md#access-model-leaderboards) to identify leading models on a single metric (quality, safety, cost, or throughput)
- [Trade-off charts](../how-to/benchmark-model-in-catalog.md#trade-off-charts) to compare performance across two metrics, such as quality versus cost
- [Leaderboards by scenario](../how-to/benchmark-model-in-catalog.md#view-leaderboards-by-scenario) to find models aligned to specific use cases

::: moniker-end

::: moniker range="foundry"

Model leaderboards (preview) in Foundry portal help you compare models in the Foundry [model catalog](foundry-models-overview.md) using industry-standard benchmarks.

You can review detailed benchmarking methodology for each leaderboard category:

- [Quality benchmarking](#quality-benchmarks-of-language-models) of language models to understand how well models perform on cores tasks including reasoning, knowledge, question answering, math, and coding;
- [Safety benchmarking](#safety-benchmarks-of-language-models) of language models to understand how safe models are against harmful behavior generation;
- [Performance benchmarking](#performance-benchmarks-of-language-models) of language models to understand how models perform in terms of latency and throughput.
- [Cost benchmarking](#cost-benchmarks-of-language-models) of language models to understand the estimated cost of using models.
- [Scenario leaderboard benchmarking](#scenario-leaderboard-benchmarking) of language models to help you find the best model for your specific use case or scenario.
- [Quality benchmarking](#quality-benchmarks-of-embedding-models) of embedding models to understand how well models perform on embedding-based tasks including search and retrieval.

::: moniker-end

When you find a suitable model, you can open its **Detailed benchmarking results** in the model catalog. From there, you can deploy the model, try it in the playground, or evaluate it on your own data. The leaderboards support benchmarking for text language models (including large language models (LLMs) and small language models (SLMs)) and embedding models.

Model benchmarks assess LLMs and SLMs across quality, safety, cost, and throughput. Embedding models are evaluated using standard quality benchmarks. Leaderboards are updated regularly as new models and benchmarks are added.

## Model benchmarking scope

The model leaderboards feature a curated selection of text-based language models from the Foundry model catalog. Models are included based on the following criteria:

- **Azure Direct Models prioritized**: Azure Direct Models are selected for relevance to common generative AI scenarios.
- **Core benchmark applicability**: Models must support general-purpose language tasks such as reasoning, knowledge, question answering, mathematical reasoning, and coding. Specialized models (for example, protein folding or domain-specific QA) and other modalities aren't supported.

This scoping ensures the leaderboards reflect current, high-quality models relevant to core AI scenarios.

## Quality benchmarks of language models

Foundry assesses the quality of LLMs and SLMs using accuracy scores from standard benchmark datasets that measure reasoning, knowledge, question answering, math, and coding capabilities.

| Index | Description |
|--|--|
| Quality index | Calculated by averaging applicable accuracy scores (`exact_match`, `pass@1`, `arena_hard`) across benchmark datasets. |

Quality index values range from zero to one, where higher values indicate better performance. The datasets included in the quality index are:

| Dataset Name | Category |
|--|--|
| [arena_hard](https://github.com/lmarena/arena-hard-auto) | QA |
| [bigbench_hard](https://github.com/suzgunmirac/BIG-Bench-Hard) (downsampled to 1,000 examples) | Reasoning |
| [gpqa](https://github.com/idavidrein/gpqa) | QA |
| [humanevalplus](https://github.com/evalplus/evalplus) | Coding |
| [ifeval](https://github.com/google-research/google-research/tree/master/instruction_following_eval) | Reasoning |
| [math](https://github.com/hendrycks/math) | Math |
| [mbppplus](https://github.com/evalplus/evalplus) | Coding |
| [mmlu_pro](https://github.com/TIGER-AI-Lab/MMLU-Pro) (downsampled to 1,000 examples) | General knowledge |

See more details in accuracy scores:

| Metric | Description |
|--|--|
| Accuracy | Accuracy scores are available at the dataset and the model levels. At the dataset level, the score is the average value of an accuracy metric computed over all examples in the dataset. The accuracy metric used is `exact-match` in all cases, except for the _HumanEval_ and _MBPP_ datasets that use a `pass@1` metric. Exact match compares model generated text with the correct answer according to the dataset, reporting one if the generated text matches the answer exactly and zero otherwise. The `pass@1` metric measures the proportion of model solutions that pass a set of unit tests in a code generation task. At the model level, the accuracy score is the average of the dataset-level accuracies for each model. |

Accuracy scores range from zero to one, where higher values are better.

## Safety benchmarks of language models

To guide the selection of safety benchmarks for evaluation, we apply a structured filtering and validation process designed to ensure both relevance and rigor. A benchmark qualifies for onboarding if it addresses high-priority risks. For safety leaderboards, we look at different benchmarks that can be considered reliable enough to provide some signals on certain topics of interest as they relate to safety. We select [HarmBench](https://github.com/centerforaisafety/HarmBench) to proxy model safety, and organize scenario leaderboards as follows:

| Dataset Name | Leaderboard Scenario | Metric | Interpretation |
|--|--|--|--|
| HarmBench (standard) | Standard harmful behaviors | Attack Success Rate | Lower values means better robustness against attacks designed to illicit standard harmful content |
| HarmBench (contextual) | Contextually harmful behaviors | Attack Success Rate | Lower values means better robustness against attacks designed to illicit contextually harmful content |
| HarmBench (copyright violations) | Copyright violations | Attack Success Rate | Lower values indicate stronger robustness against copyright violations |
| WMDP | Knowledge in sensitive domains | Accuracy | Higher values indicate greater knowledge in sensitive domains |
| Toxigen | Toxic content detection | F1 Score | Higher values indicate better detection performance |

### Model harmful behaviors

The [HarmBench](https://github.com/centerforaisafety/HarmBench) benchmark measures harmful behaviors using prompts designed to elicit unsafe responses. It covers seven semantic categories:

- Cybercrime and unauthorized intrusion
- Chemical and biological weapons or drugs
- Copyright violations
- Misinformation and disinformation
- Harassment and bullying
- Illegal activities
- General harm

These categories are grouped into three functional areas:

- Standard harmful behaviors
- Contextually harmful behaviors
- Copyright violations

Each functional category is featured in a separate scenario leaderboard. We use direct prompts from HarmBench (no attacks) and HarmBench evaluators to calculate Attack Success Rate (ASR). Lower ASR values mean safer models. We don't explore any attack strategy for evaluation, and model benchmarking is performed with Foundry Content Safety Filter turned off.

### Model ability to detect toxic content

[Toxigen](https://github.com/microsoft/TOXIGEN) is a large-scale dataset for detecting adversarial and implicit hate speech. It includes implicitly toxic and benign sentences referencing 13 minority groups. Foundry uses annotated Toxigen samples and calculates F1 scores to measure classification performance. Higher scores indicate better toxic content detection. Benchmarking is performed with the Foundry Content Safety Filter turned off.

### Model knowledge in sensitive domains

The [Weapons of Mass Destruction Proxy](https://github.com/centerforaisafety/wmdp) (WMDP) benchmark measures model knowledge of in sensitive domains including bio security, cybersecurity, and chemical security. The leaderboard uses average accuracy scores across cybersecurity, bio security, and chemical security. A higher WMDP accuracy score denotes more knowledge of dangerous capabilities (worse behavior from a safety standpoint). Model benchmarking is performed with the default Foundry Content Safety filters on. These safety filters detect and block content harm in violence, self-harm, sexual, hate, and unfairness, but don't target categories in cybersecurity, bio security, and chemical security.

### Limitations of safety benchmarks

We understand and acknowledge that safety is a complex topic and has several dimensions. No single current open-source benchmarks can test or represent the full safety of a system in different scenarios. Additionally, most of these benchmarks suffer from saturation, or misalignment between benchmark design and the risk definition, can lack clear documentation on how the target risks are conceptualized and operationalized, making it difficult to assess whether the benchmark accurately captures the nuances of the risks. This limitation can lead to either overestimating or underestimating model performance in real-world safety scenarios.

## Performance benchmarks of language models

Performance metrics are aggregated over 14 days using 24 trails per day, with two requests per trail sent at one-hour intervals. The following default parameters are used:

| Parameter | Value | Applicable for |
|--|--|--|
| Region | East US/East US2 | [serverless API deployments](./foundry-models-overview.md) and [Azure OpenAI](/azure/ai-foundry/openai/overview) |
| Tokens per minute (TPM) rate limit | 30k (180 RPM based on Azure OpenAI) for non-reasoning and 100k for reasoning models <br> N/A (serverless API deployments) | For Azure OpenAI models, selection is available for users with rate limit ranges based on deployment type (serverless API, global, global standard, and so on.) <br> For serverless API deployments, this setting is abstracted. |
| Number of requests | Two requests in a trail for every hour (24 trails per day) | serverless API deployments, Azure OpenAI |
| Number of trails/runs | 14 days with 24 trails per day for 336 runs | serverless API deployments, Azure OpenAI |
| Prompt/Context length | Moderate length | serverless API deployments, Azure OpenAI |
| Number of tokens processed (moderate) | 80:20 ratio for input to output tokens, that is, 800 input tokens to 200 output tokens. | serverless API deployments, Azure OpenAI |
| Number of concurrent requests | One (requests are sent sequentially one after other) | serverless API deployments, Azure OpenAI |
| Data | Synthetic (input prompts prepared from static text) | serverless API deployments, Azure OpenAI |
| Region | East US/East US2 | serverless API deployments and Azure OpenAI |
| Deployment type | serverless API | Applicable only for Azure OpenAI |
| Streaming | True | Applies to serverless API deployments and Azure OpenAI. For models deployed via [managed compute](./foundry-models-overview.md), or for endpoints when streaming isn't supported TTFT is represented as P50 of latency metric. |
| SKU | Standard_NC24ads_A100_v4 (24 cores, 220GB RAM, 64GB storage) | Applicable only for Managed Compute (to estimate the cost and performance metrics) |
	
The performance of LLMs and SLMs is assessed across the following metrics:

| Metric | Description |
|--|--|
| Latency mean | Average time in seconds taken for processing a request, computed over multiple requests. To compute this metric, we send a request to the endpoint every hour, for two weeks, and compute the average. |
| Latency P50 | 50th percentile value (the median) of latency (the time taken between the request and when we receive the entire response with a successful code). For example, when we send a request to the endpoint, 50% of the requests are completed in 'x' seconds, with 'x' being the latency measurement. |
| Latency P90 | 90th percentile value of latency (the time taken between the request and when we receive the entire response with a successful code). For example, when we send a request to the endpoint, 90% of the requests are completed in 'x' seconds, with 'x' being the latency measurement. |
| Latency P95 | 95th percentile value of latency (the time taken between the request and when we receive the entire response with a successful code). For example, when we send a request to the endpoint, 95% of the requests are complete in 'x' seconds, with 'x' being the latency measurement. |
| Latency P99 | 99th percentile value of latency (the time taken between the request and when we receive the entire response with a successful code). For example, when we send a request to the endpoint, 99% of the requests are complete in 'x' seconds, with 'x' being the latency measurement. |
| Throughput GTPS | Generated tokens per second (GTPS) is the number of output tokens that are getting generated per second from the time the request is sent to the endpoint. |
| Throughput TTPS | Total tokens per second (TTPS) is the number of total tokens processed per second including both from the input prompt and generated output tokens. For models which don't support streaming, time to first token (ttft) represents the P50 value of latency (time taken to receive the response) |
| Latency TTFT | Total time to first token (TTFT) is the time taken for the first token in the response to be returned from the endpoint when streaming is enabled. |
| Time between tokens | This metric is the time between tokens received. |

Foundry summarizes performance using:

| Metric | Description |
|-------|-------------|
| Latency | Mean time to first token. Lower is better. |
| Throughput | Mean generated tokens per second. Higher is better. |

For performance metrics like latency or throughput, the time to first token and the generated tokens per second give a better overall sense of the typical performance and behavior of the model. We refresh our performance numbers on regular cadence.

## Cost benchmarks of language models

Cost calculations are estimates for using an LLM or SLM model endpoint hosted on the Foundry platform. Foundry supports displaying the cost of serverless API deployments and Azure OpenAI models. Because these costs are subject to change, we refresh our cost calculations on a regular cadence.

The cost of LLMs and SLMs is assessed across the following metrics:

| Metric | Description |
|--------|-------------|
| Cost per input tokens | Cost for serverless API deployment for 1 million input tokens |
| Cost per output tokens | Cost for serverless API deployment for 1 million output tokens |
| Estimated cost | Cost for the sum of cost per input tokens and cost per output tokens, with a ratio of 3:1. |

Foundry also displays the cost as follows:
	
| Metric | Description |
|-------|-------------|
| Cost | Estimated US dollar cost per 1 million tokens. The estimated workload uses the three-to-one ratio between input and output tokens. Lower values are better. |
	
## Scenario leaderboard benchmarking
	
Scenario leaderboards group benchmark datasets by common real-world evaluation goals so you can quickly identify a model's strengths and weaknesses by use case. Each scenario aggregates one or more public benchmark datasets. The following table summarizes the available scenario leaderboards and their associated datasets and descriptions:

| Scenario | Datasets | Description |
|--|--|--|
| Standard harmful behavior | [HarmBench (standard)](https://github.com/centerforaisafety/HarmBench) | Measures attack success rate on standard harmful prompts. Lower is better. |
| Contextually harmful behavior | [HarmBench (contextual)](https://github.com/centerforaisafety/HarmBench) | Measures attack success rate on contextual harmful prompts. Lower is better. |
| Copyright violations | [HarmBench (copyright)](https://github.com/centerforaisafety/HarmBench) | Measures attack success rate for copyright violation prompts. Lower is better. |
| Knowledge in sensitive domains | [WMDP](https://github.com/centerforaisafety/wmdp) (bio security, chemical security, cybersecurity) | Accuracy across three sensitive domain subsets. Higher accuracy indicates more knowledge of sensitive capabilities for a model. |
| Toxicity detection | [ToxiGen](https://github.com/microsoft/TOXIGEN) (annotated) | F1 score for toxic content detection ability. Higher is better. |
| Reasoning | [BIG-Bench Hard](https://github.com/suzgunmirac/BIG-Bench-Hard) (1000 subsample) | Reasoning capabilities assessment. Higher values are better. |
| Coding | [BigCodeBench](https://github.com/bigcode-project/bigcodebench) (instruct), [HumanEvalPlus](https://github.com/evalplus/evalplus), [LiveBench (coding)](https://github.com/LiveBench/LiveBench), [MBPPPlus](https://github.com/evalplus/evalplus) | Measures accuracy on code-related tasks.  Higher values are better.|
| General knowledge | [MMLU-Pro](https://github.com/TIGER-AI-Lab/MMLU-Pro) (1K English subsample) | 1,000‑example English-only subsample of MMLU-Pro. |
| Question & answering | [Arena-Hard](https://github.com/lmarena/arena-hard-auto), [GPQA](https://github.com/idavidrein/gpqa) (diamond) | Adversarial human preference QA (Arena-Hard) and graduate‑level multi‑discipline QA (GPQA diamond).  Higher values are better.|
| Math | [MATH](https://github.com/hendrycks/math) (500 subsample) | Measures mathematical reasoning capabilities of language models.  Higher values are better.|
| Groundedness | [TruthfulQA](https://github.com/sylinrl/TruthfulQA) (MC1) | Multiple‑choice groundedness / truthfulness assessment of language models.  Higher values are better.|

## Quality benchmarks of embedding models

The quality index of embedding models is defined as the averaged accuracy scores of a comprehensive set of serverless API benchmark datasets targeting Information Retrieval, Document Clustering, and Summarization tasks.

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

Benchmark results originate from public datasets that are commonly used for language model evaluation. In most cases, the data is hosted in GitHub repositories maintained by the creators or curators of the data. Foundry evaluation pipelines download data from their original sources, extract prompts from each example row, generate model responses, and then compute relevant accuracy metrics.
	
Prompt construction follows best practices for each dataset, as specified by the paper introducing the dataset and industry standards. In most cases, each prompt contains several _shots_, that is, several examples of complete questions and answers to prime the model for the task. The evaluation pipelines create shots by sampling questions and answers from a portion of the data held out from evaluation.

## Related content

- [Compare and select models using the model leaderboard in Foundry portal](../how-to/benchmark-model-in-catalog.md)
- [Model catalog and collections in Foundry portal](foundry-models-overview.md)