---
title: Azure AI Translator 2025-05-01-preview reference
titleSuffix: Azure AI services
description: Reference documentation for Azure AI Translator 2025-05-01-preview operations and capabilities.
author: laujan
manager: nitinme
ms.service: azure-ai-translator
ms.topic: reference
ms.date: 04/18/2025
ms.author: lajanuar
---

# Azure AI Translator 2025-05-01-preview 

Azure AI Translator `2025-05-01-preview` is our latest cloud-based, multilingual, neural machine translation service. The Text translation API enables robust and scalable translation capabilities suitable for diverse applications. 

The Translator service is an optimal solution for managing extensive multilingual content. It easily integrates with your applications and workflows through a single REST API call and supports multiple programming languages. Translator supports over 100 languages and dialects, making it ideal for businesses, developers, and organizations seeking to seamlessly integrate multilingual communication.  

Azure AI Translator prioritizes data security and privacy, complying with regulations like GDPR, HIPAA, and ISO/SOC, thus ensuring that it's a reliable solution for handling sensitive and confidential information.

>[!IMPORTANT]
> * Azure AI Translator REST API `2025-05-01-preview` is new version of the Azure AI Translator REST API **with breaking changes**.
> * It's essential to thoroughly test your code against the new release before migrating any production applications from Azure AI Translator v3.0.
> * Make sure to review your code and internal workflows for adherence to best practices and restrict your production code to versions that you fully test.


## What's new for 2025-05-01-preview?

* **`LLM` choice**. You can choose a large language model for translation based on factors such as quality, cost, and other considerations.

* **Adaptive custom translation**. You can provide reference translations or translation memory datasets to enable an `LLM` model to perform few-shot translations tailored to your needs. Few-shot translation is a machine translation method where the model is trained or fine-tuned with only a limited number of examples to translate between languages.

* The **Translator** resource doesn't support Neural Machine Translation (`NMT`) translations.

* You need to create an **Azure AI Foundry** resource to use an `LLM` model.

## Metrics

Metrics allow you to view the translator usage and availability information in Azure portal, under metrics section as shown in the following screenshot. For more information, see [Data and platform metrics](/azure/azure-monitor/essentials/data-platform-metrics).

:::image type="content" source="../../../media/azure-portal-metrics-v4.png" alt-text="Screenshot of HTTP request metrics in the Azure portal.":::

This table lists available metrics with description of how they're used to monitor translation API calls.

| Metrics | Description |
|:----|:-----|
| BlockCalls| Number of calls that exceed rate or quota.|
| ClientErrors| Number of calls with client-side error (HTTP response code 4xx)|
| DataIn| Size of incoming data in bytes.|
| DataOut| Size of outgoing data in bytes.|
| Latency| Duration to complete request in milliseconds.|
| RateLimit| The current rate limit of the ratelimit key.|
| ServerErrors| Number of calls with server internal error (HTTP response code 5xx).|
| SuccessfulCalls| Number of successful calls (HTTP response code 2xx).|
| TotalCalls| Total number of calls.|
| TotalErrors|Total number of calls with error response (HTTP response code 4xx or 5xx)|
| TotalTokenCalls|Total number of token calls|

## Next steps

> [!div class="nextstepaction"]
> [View 2025-05-01-preview migration guide](../../how-to/migrate-to-v4.md)



