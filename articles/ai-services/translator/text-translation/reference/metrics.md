---
title: Azure Translator in Foundry Tools usage and data metrics
titleSuffix: Foundry Tools
description: Reference documentation for Azure Translator Azure Monitor Metrics.
author: laujan
manager: nitinme
ms.service: azure-ai-translator
ms.topic: reference
ms.date: 11/18/2025
ms.author: lajanuar
---

# Azure Translator in Foundry Tools usage and data metrics

Metrics allow you to view the translator usage and availability information in Azure portal, under metrics section as shown in the following screenshot. For more information, see [Data and platform metrics](/azure/azure-monitor/essentials/data-platform-metrics).

:::image type="content" source="../../media/azure-portal-metrics-v4.png" alt-text="Screenshot of HTTP request metrics in the Azure portal.":::

#### Metrics terminology

* **PTU**: provisioned throughput units
* **TPS**: transactions per second
* **TPM**: tokens per minute

The following tables list available metrics with description of how they're used to monitor **Translator resource** API calls.

#### Azure Translator in Foundry Tools resource HTTP requests

| Metrics | Description |
|:----|:-----|
| `BlockedCalls`| Number of calls that exceeded rate or quota limit.|
| `ClientErrors`| Number of calls with client-side error(4XX).|
| `Latency`| Duration to complete request in milliseconds.|
| `Ratelimit`| The current rate limit of the rate limit key.|
| `ServerErrors`| Number of calls with server internal error(5XX).|
| `SuccessfulCalls`| Number of successful calls.|
| `TotalCalls`| Total number of API calls.|
| `TotalErrors`| Number of calls with error response.|
| `TotalTokenCalls`| Total number of API calls via token service using authentication token.|

#### Azure Translator in Foundry Tools resource usage2

| Metrics | Description |
|:----|:-----|
| `TextCharactersTranslated`|Number of characters in incoming text translation request.|
| `TextCustomCharactersTranslated`|Number of characters in incoming custom text translation request.|
| `TextTrainedCharacters`|Number of characters trained using text translation.|
| `DocumentCharactersTranslated`|Number of characters in document translation request.|
| `DocumentCustomCharactersTranslated`|Number of characters in custom document translation request.|

The following tables list available metrics with description of how they're used to monitor **Azure OpenAI** API calls.

#### Azure OpenAI HTTP requests

| Metrics | Description |
|:----|:-----|
| `AzureOpenAIAvailabilityRate`|Availability percentage with the following calculation:<br>`(Total Calls - Server Errors) / Total Calls`. Server Errors include any HTTP response >= 500.|
|`AzureOpenAIRequests`|Number of calls made to the Azure OpenAI API over a period of time. Applies to `PTU`, `PTU`-managed, and Pay-as-you-go deployments. To breakdown API requests, you can add a filter or apply splitting by the following dimensions: <br> `ModelDeploymentName`, `ModelName`, `ModelVersion`, `StatusCode` (successful, client errors, server errors), `StreamType` (streaming vs nonstreaming requests), and `Operation`.|

#### Azure OpenAI usage

| Metrics | Description |
|:----|:-----|
|`ActiveTokens`|Total tokens minus cached tokens over a period of time. Applies to `PTU` and `PTU`-managed deployments. Use this metric to understand your `TPS`- or `TPM`-based utilization for `PTU`s and compare your benchmarks for target `TPS` or `TPM` for your scenarios. <br> To breakdown API requests, you can add a filter or apply splitting by the following dimensions: `ModelDeploymentName`, `ModelName`, `ModelVersion`.|
|`GeneratedTokens`|Number of tokens generated (output) from an OpenAI model. Applies to `PTU`, `PTU`-managed, and Pay-as-you-go deployments. To analyze this metric in detail, you can add a filter or apply splitting by the following dimensions:<br>`ModelDeploymentName`or `ModelName`.|
|`FineTunedTrainingHours`|Number of training hours processed on an OpenAI fine-tuned model.|
|`TokenTransaction`|Number of inference tokens processed on an OpenAI model. Calculated as prompt tokens (input) plus generated tokens (output). Applies to `PTU`, `PTU`-managed, and Pay-as-you-go deployments. To analyze this metric in detail, you can add a filter or apply splitting by the following dimensions:<br>`ModelDeploymentName`or `ModelName`.|
|`ProcessedPromptTokens`|Number of prompt tokens processed (input) on an OpenAI model. Applies to `PTU`, `PTU`-managed, and Pay-as-you-go deployments. To analyze this metric in detail, you can add a filter or apply splitting by the following dimensions:<br>`ModelDeploymentName`or `ModelName`.|
|`AzureOpenAIContextTokensCacheMatchRate`|Percentage of prompt tokens that hit the cache. Applies to `PTU` and `PTU`-managed deployments.
|`AzureOpenAIProvisionedManagedUtilizationV2`|Utilization percentage for a provisioned-managed deployment, calculated as (`PTU`s consumed / `PTU`s deployed) x 100. When utilization is greater than or equal to 100%, calls are throttled and error code 429 is returned. To analyze this metric in detail, you can add a filter or apply splitting by the following dimensions: `ModelDeploymentName`, `ModelName`, `ModelVersion`, and `StreamType` (streaming vs nonstreaming requests).|

## Next steps

[What is text translation](../overview.md)
