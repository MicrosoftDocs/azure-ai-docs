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

Model leaderboards (preview) in Microsoft Foundry portal help you compare models in the Foundry [model catalog](../how-to/model-catalog-overview.md) using industry-standard benchmarks. From the model leaderboards section of the model catalog, you can [browse leaderboards](https://aka.ms/model-leaderboards) to compare available models by:

<!-- Changed to remove duplicated marketing phrasing and consolidate into a single concise sentence. -->

- [Quality, safety, cost, and performance leaderboards](../how-to/benchmark-model-in-catalog.md#access-model-leaderboards) to identify leading models on a single metric (quality, safety, cost, or throughput)
- [Trade-off charts](../how-to/benchmark-model-in-catalog.md#trade-off-charts) to compare performance across two metrics, such as quality versus cost
- [Leaderboards by scenario](../how-to/benchmark-model-in-catalog.md#view-leaderboards-by-scenario) to find models aligned to specific use cases

::: moniker-end

::: moniker range="foundry"

Model leaderboards (preview) in Foundry portal help you compare models in the Foundry [model catalog](../how-to/model-catalog-overview.md) using industry-standard benchmarks.

<!-- Changed to remove duplicated opening sentences and retain a single authoritative description. -->

You can review detailed benchmarking methodology for each leaderboard category:

- [Quality benchmarking](#quality-benchmarks-of-language-models) to evaluate performance on core language tasks such as reasoning, knowledge, question answering, math, and coding
- [Safety benchmarking](#safety-benchmarks-of-language-models) to assess robustness against harmful behavior generation
- [Performance benchmarking](#performance-benchmarks-of-language-models) to understand latency and throughput characteristics
- [Cost benchmarking](#cost-benchmarks-of-language-models) to estimate model usage costs
- [Scenario leaderboard benchmarking](#scenario-leaderboard-benchmarking) to identify models suited to specific scenarios
- [Quality benchmarking](#quality-benchmarks-of-embedding-models) to evaluate embedding model performance on search and retrieval tasks

::: moniker-end

When you find a suitable model, you can open its **Detailed benchmarking results** in the model catalog. From there, you can deploy the model, try it in the playground, or evaluate it on your own data. The leaderboards support benchmarking for text language models (including large language models (LLMs) and small language models (SLMs)) and embedding models.

<!-- Changed to streamline repeated high-level guidance into a single concise paragraph. -->

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
| Accuracy | Accuracy scores are available at the dataset and model levels. Dataset-level accuracy is the average value computed across all examples. The `exact-match` metric is used in most cases, while _HumanEval_ and _MBPP_ use `pass@1`. Model-level accuracy is the average of dataset-level scores. |

Accuracy scores range from zero to one, where higher values are better.

## Safety benchmarks of language models

To guide safety evaluation, Foundry applies a structured filtering and validation process to select benchmarks that address high-priority risks. For safety leaderboards, Foundry uses benchmarks that provide reliable signals for specific safety-related behaviors. The primary proxy for model safety is [HarmBench](https://github.com/centerforaisafety/HarmBench), with scenario leaderboards organized as follows:

| Dataset Name | Leaderboard Scenario | Metric | Interpretation |
|--|--|--|--|
| HarmBench (standard) | Standard harmful behaviors | Attack Success Rate | Lower values indicate stronger robustness against harmful prompts |
| HarmBench (contextual) | Contextually harmful behaviors | Attack Success Rate | Lower values indicate stronger robustness against contextual harm |
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

Each functional area is represented by a separate scenario leaderboard. Evaluation uses direct prompts and HarmBench evaluators to calculate Attack Success Rate (ASR). Lower ASR values indicate safer models. No attack strategies are applied, and benchmarking is performed with the Foundry Content Safety Filter turned off.

### Model ability to detect toxic content

[Toxigen](https://github.com/microsoft/TOXIGEN) is a large-scale dataset for detecting adversarial and implicit hate speech. It includes implicitly toxic and benign sentences referencing 13 minority groups. Foundry uses annotated Toxigen samples and calculates F1 scores to measure classification performance. Higher scores indicate better toxic content detection. Benchmarking is performed with the Foundry Content Safety Filter turned off.

### Model knowledge in sensitive domains

The [Weapons of Mass Destruction Proxy](https://github.com/centerforaisafety/wmdp) (WMDP) benchmark measures knowledge in sensitive domains such as biosecurity, cybersecurity, and chemical security. The leaderboard reports average accuracy across these domains. Higher scores indicate greater knowledge of sensitive capabilities, which is considered worse from a safety perspective. Benchmarking is performed with default Foundry Content Safety filters enabled.

### Limitations of safety benchmarks

Safety is multi-dimensional, and no single benchmark captures all safety considerations. Existing benchmarks may suffer from saturation, limited documentation, or misalignment between benchmark design and real-world risks. As a result, benchmark scores can overestimate or underestimate actual safety performance in production scenarios.

## Performance benchmarks of language models

Performance metrics are aggregated over 14 days using 24 trails per day, with two requests per trail sent at one-hour intervals. The following default parameters are used:

| Parameter | Value | Applicable for |
|--|--|--|
| Region | East US/East US2 | Serverless API deployments and Azure OpenAI |
| Tokens per minute (TPM) | 30k (non-reasoning), 100k (reasoning) | Azure OpenAI |
| Number of requests | Two per trail, hourly | Serverless API deployments, Azure OpenAI |
| Number of trails | 14 days, 24 trails per day (336 runs) | Serverless API deployments, Azure OpenAI |
| Prompt length | Moderate | Serverless API deployments, Azure OpenAI |
| Token ratio | 800 input / 200 output | Serverless API deployments, Azure OpenAI |
| Concurrency | One request at a time | Serverless API deployments, Azure OpenAI |
| Data | Synthetic | Serverless API deployments, Azure OpenAI |
| Deployment type | Serverless API | Azure OpenAI |
| Streaming | True | Serverless API deployments, Azure OpenAI |
| SKU | Standard_NC24ads_A100_v4 | Managed compute only |

The following metrics are used to assess performance:

| Metric | Description |
|--|--|
| Latency mean | Average request processing time |
| Latency P50 | Median request latency |
| Latency P90 | 90th percentile latency |
| Latency P95 | 95th percentile latency |
| Latency P99 | 99th percentile latency |
| Throughput GTPS | Generated tokens per second |
| Throughput TTPS | Total tokens processed per second |
| Latency TTFT | Time to first token when streaming |
| Time between tokens | Interval between generated tokens |

Foundry summarizes performance using:

| Metric | Description |
|-------|-------------|
| Latency | Mean time to first token. Lower is better. |
| Throughput | Mean generated tokens per second. Higher is better. |

Performance metrics are refreshed on a regular cadence.

## Cost benchmarks of language models

Cost benchmarks estimate usage costs for LLM and SLM endpoints hosted on Foundry, including serverless API deployments and Azure OpenAI models. Because pricing can change, cost estimates are refreshed regularly.

The following metrics are used:

| Metric | Description |
|--------|-------------|
| Cost per input tokens | Cost per 1 million input tokens |
| Cost per output tokens | Cost per 1 million output tokens |
| Estimated cost | Combined input and output cost using a 3:1 ratio |

Foundry also displays:

| Metric | Description |
|-------|-------------|
| Cost | Estimated USD cost per 1 million tokens. Lower is better. |

## Scenario leaderboard benchmarking

Scenario leaderboards group benchmarks by common evaluation goals, helping you identify model strengths by use case.

| Scenario | Datasets | Description |
|--|--|--|
| Standard harmful behavior | HarmBench (standard) | Attack success rate on standard harmful prompts |
| Contextually harmful behavior | HarmBench (contextual) | Attack success rate on contextual harmful prompts |
| Copyright violations | HarmBench (copyright) | Attack success rate on copyright prompts |
| Knowledge in sensitive domains | WMDP | Accuracy across sensitive domains |
| Toxicity detection | ToxiGen | F1 score for toxic content detection |
| Reasoning | BIG-Bench Hard | Reasoning performance |
| Coding | BigCodeBench, HumanEvalPlus, LiveBench, MBPPPlus | Code task accuracy |
| General knowledge | MMLU-Pro | General knowledge assessment |
| Question answering | Arena-Hard, GPQA | QA performance |
| Math | MATH | Mathematical reasoning |
| Groundedness | TruthfulQA | Truthfulness assessment |

## Quality benchmarks of embedding models

The quality index for embedding models averages accuracy-based metrics across benchmarks for information retrieval, document clustering, and summarization tasks.

| Metric | Description |
|--------|-------------|
| Accuracy | Proportion of correct predictions |
| F1 score | Weighted mean of precision and recall |
| Mean average precision (MAP) | Ranking quality metric |
| Normalized discounted cumulative gain (NDCG) | Ranking quality at k=10 |
| Precision | Correct positive prediction rate |
| Spearman correlation | Rank correlation based on cosine similarity |
| V measure | Clustering quality metric |

## Calculation of scores

### Individual scores

Benchmark results are derived from public datasets hosted by their original creators. Foundry evaluation pipelines retrieve the data, generate model responses, and compute the relevant metrics.

Prompt construction follows dataset-specific best practices. Prompts typically include multiple shots—example questions and answers sampled from held-out data—to prime the model before evaluation.

## Related content

- [Compare and select models using the model leaderboard in Foundry portal](../how-to/benchmark-model-in-catalog.md)
- [Model catalog and collections in Foundry portal](../how-to/model-catalog-overview.md)