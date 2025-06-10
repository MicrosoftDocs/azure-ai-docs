---
title: Azure AI Translator 2025-05-01-preview reference
titleSuffix: Azure AI services
description: Reference documentation for Azure AI Translator 2025-05-01-preview operations and capabilities.
author: laujan
manager: nitinme
ms.service: azure-ai-translator
ms.topic: reference
ms.date: 06/19/2025
ms.author: lajanuar
---

# Azure AI Translator 2025-05-01-preview 

Azure AI Translator `2025-05-01-preview` is our latest cloud-based, multilingual, neural machine translation service. The Text translation API enables robust and scalable translation capabilities suitable for diverse applications. 

The Translator service is an optimal solution for managing extensive multilingual content. It easily integrates with your applications and workflows through a single REST API call and supports multiple programming languages. Translator supports over 100 languages and dialects, making it ideal for businesses, developers, and organizations seeking to seamlessly integrate multilingual communication.  


>[!IMPORTANT]
> * Azure AI Translator REST API `2025-05-01-preview` is new version of the Azure AI Translator REST API **with breaking changes**.
> * It's essential to thoroughly test your code against the new release before migrating any production applications from Azure AI Translator v3.0.
> * Make sure to review your code and internal workflows for adherence to best practices and restrict your production code to versions that you fully test.


## What's new for 2025-05-01-preview?

* **`LLM` choice**. You can choose a large language model for translation based on factors such as quality, cost, and other considerations.

* **Adaptive custom translation**. You can provide reference translations or translation memory datasets to enable an `LLM` model to perform few-shot translations tailored to your needs. 

* The **Translator** resource doesn't support Neural Machine Translation (`NMT`) translations.

* You need to create an **Azure AI Foundry** resource to use an `LLM` model.

## Metrics

Metrics allow you to view the translator usage and availability information in Azure portal, under metrics section as shown in the following screenshot. For more information, see [Data and platform metrics](/azure/azure-monitor/essentials/data-platform-metrics).

:::image type="content" source="../../../media/azure-portal-metrics-v4.png" alt-text="Screenshot of HTTP request metrics in the Azure portal.":::

#### Metrics terminology

* **PTU**: provisioned throughput units
* **TPS**: transactions per second
* **TPM**: tokens per minute

The following tables list available metrics with description of how they're used to monitor **Translator resource** API calls.

#### Translator resource HTTP requests

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

#### Translator resource usage

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

> [!div class="nextstepaction"]
> [View 2025-05-01-preview migration guide](../../how-to/migrate-to-preview.md)



