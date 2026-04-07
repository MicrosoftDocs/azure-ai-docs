---
title: "Model benchmarks and leaderboards in Microsoft Foundry (classic)"
description: "Compare AI models using quality, safety, cost, and performance benchmarks on the model leaderboards (preview) in Microsoft Foundry portal. (classic)"
ms.service: azure-ai-foundry
ms.custom:
  - classic-and-new
  - ai-learning-hub
ms.topic: concept-article
ms.date: 02/13/2026
ms.reviewer: changliu2
ms.author: lagayhar  
author: lgayhardt
ai-usage: ai-assisted
# customer intent: As a developer or data scientist, I want to understand model leaderboards and benchmarking capabilities in Microsoft Foundry portal so I can compare and select the best models for my AI solutions.
ROBOTS: NOINDEX, NOFOLLOW
---

# Model leaderboards in Microsoft Foundry portal (preview) (classic)

**Currently viewing:** :::image type="icon" source="../../foundry/media/yes-icon.svg" border="false"::: **Foundry (classic) portal version** - [Switch to version for the new Foundry portal](../../foundry/concepts/model-benchmarks.md)

[!INCLUDE [feature-preview](../../foundry/includes/feature-preview.md)]

Model leaderboards (preview) in Microsoft Foundry portal help you compare models in the Foundry [model catalog](foundry-models-overview.md) using industry-standard benchmarks. From the model leaderboards section of the model catalog, you can [browse leaderboards](https://aka.ms/model-leaderboards) to compare available models by:

- [Quality, safety, cost, and performance leaderboards](../how-to/benchmark-model-in-catalog.md#access-model-leaderboards) to identify leading models on a single metric (quality, safety, cost, or throughput)
- [Trade-off charts](../how-to/benchmark-model-in-catalog.md#trade-off-charts) to compare performance across two metrics, such as quality versus cost
- [Leaderboards by scenario](../how-to/benchmark-model-in-catalog.md#view-leaderboards-by-scenario) to find models aligned to specific use cases

When you find a suitable model, you can open its **Detailed benchmarking results** in the model catalog. From there, you can deploy the model, try it in the playground, or evaluate it on your own data. The leaderboards support benchmarking for text language models (including large language models (LLMs) and small language models (SLMs)) and embedding models.

Model benchmarks assess LLMs and SLMs across quality, safety, cost, and throughput. Embedding models are evaluated using standard quality benchmarks. Leaderboards are updated as new models and benchmark datasets become available.

[!INCLUDE [model-benchmarks 1](../../foundry/includes/concepts-model-benchmarks-1.md)]

## Performance benchmarks of language models

Performance metrics are aggregated over 14 days using 24 trials per day, with two requests per trial sent at one-hour intervals. Unless otherwise noted, the following default parameters apply to both [serverless API deployments](./foundry-models-overview.md) and [Azure OpenAI](/azure/ai-foundry/openai/overview):

| Parameter | Value | Applicable for |
|--|--|--|
| Region | East US/East US2 | [serverless API deployments](./foundry-models-overview.md) and [Azure OpenAI](/azure/ai-foundry/openai/overview) |
| Tokens per minute (TPM) rate limit | 30k (180 RPM based on Azure OpenAI) for non-reasoning and 100k for reasoning models <br> N/A (serverless API deployments) | For Azure OpenAI models, selection is available for users with rate limit ranges based on deployment type (serverless API, global, global standard, and so on.) <br> For serverless API deployments, this setting is abstracted. |
| Number of requests | Two requests in a trial for every hour (24 trials per day) | serverless API deployments, Azure OpenAI |
| Number of trials/runs | 14 days with 24 trials per day for 336 runs | serverless API deployments, Azure OpenAI |
| Prompt/Context length | Moderate length | serverless API deployments, Azure OpenAI |
| Number of tokens processed (moderate) | 80:20 ratio for input to output tokens, that is, 800 input tokens to 200 output tokens. | serverless API deployments, Azure OpenAI |
| Number of concurrent requests | One (requests are sent sequentially one after other) | serverless API deployments, Azure OpenAI |
| Data | Synthetic (input prompts prepared from static text) | serverless API deployments, Azure OpenAI |
| Deployment type | serverless API | Applicable only for Azure OpenAI |
| Streaming | True | Applies to serverless API deployments and Azure OpenAI. For models deployed via [managed compute](./foundry-models-overview.md), or for endpoints when streaming isn't supported TTFT is represented as P50 of latency metric. |
| SKU | Standard_NC24ads_A100_v4 (24 cores, 220GB RAM, 64GB storage) | Applicable only for Managed Compute (to estimate the cost and performance metrics) |
             
The performance of LLMs and SLMs is assessed across the following metrics:

| Metric | Description |
|--|--|
| Latency mean | Average time in seconds to process a request, computed over multiple requests. A request is sent to the endpoint every hour for two weeks, and the average is computed. |
| Latency P50 | Median (50th percentile) latency. 50% of requests complete within this time. |
| Latency P90 | 90th percentile latency. 90% of requests complete within this time. |
| Latency P95 | 95th percentile latency. 95% of requests complete within this time. |
| Latency P99 | 99th percentile latency. 99% of requests complete within this time. |
| Throughput GTPS | Generated tokens per second (GTPS) is the number of output tokens that are getting generated per second from the time the request is sent to the endpoint. |
| Throughput TTPS | Total tokens per second (TTPS) is the number of total tokens processed per second including both from the input prompt and generated output tokens. For models which don't support streaming, time to first token (ttft) represents the P50 value of latency (time taken to receive the response) |
| Latency TTFT | Total time to first token (TTFT) is the time taken for the first token in the response to be returned from the endpoint when streaming is enabled. |
| Time between tokens | This metric is the time between tokens received. |

Foundry summarizes performance using:

| Metric | Description |
|-------|-------------|
| Latency | Mean time to first token. Lower is better. |
| Throughput | Mean generated tokens per second. Higher is better. |

For performance metrics like latency or throughput, the time to first token and the generated tokens per second give a better overall sense of the typical performance and behavior of the model. Performance numbers are refreshed periodically to reflect the latest deployment configurations.

[!INCLUDE [model-benchmarks 2](../../foundry/includes/concepts-model-benchmarks-2.md)]

## Related content

- [Compare and select models using the model leaderboard in Foundry portal](../how-to/benchmark-model-in-catalog.md)
- [Model catalog and collections in Foundry portal](foundry-models-overview.md)
- [Evaluate your generative AI apps](../how-to/evaluate-generative-ai-app.md)
- [Deploy models with serverless API](../how-to/deploy-models-serverless.md)
