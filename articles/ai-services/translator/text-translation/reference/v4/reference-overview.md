---
title: Azure AI Translator 2025-05-01-preview reference
titleSuffix: Azure AI services
description: Reference documentation for Azure AI Translator 2025-05-01-preview operations and capabilities.
author: laujan
manager: nitinme
ms.service: azure-ai-translator
ms.topic: reference
ms.date: 03/28/2025
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


## What's new?

* **LLM choice**. You can choose a large language model for translation based on quality, cost, and other factors, while avoiding costs associated with prompt engineering and quality evaluations.

* **Adaptive custom translation**. New features enable adaptive custom translations using datasets or reference pairs to ensure more accurate and contextually relevant translations.

* **Enhanced translation**. The Text translation API supports a range of parameters, including text type, language codes, and options for tone and gender, thus providing more nuanced translation outputs.

## Base URLs

Typically, The nearest datacenter to the point of origin manages requests to Translator. However, if there's a datacenter failure when utilizing the global endpoint, requests may be redirected beyond the initial geography.

To ensure that requests are handled within a specific region, utilize the designated geographical endpoint so all requests are processed within the datacenters of the chosen geography.

✔️ Feature: **Translator Text** </br>

| Service endpoint | Request processing data center |
|------------------|--------------------------|
|**Global (recommended):**</br>**`api.cognitive.microsofttranslator.com`**|Closest available data center.|
|**Americas:**</br>**`api-nam.cognitive.microsofttranslator.com`**|East US 2 &bull; West US 2|
|**Asia Pacific:**</br>**`api-apc.cognitive.microsofttranslator.com`**|Japan East &bull; Southeast Asia|
|**Europe (except Switzerland):**</br>**`api-eur.cognitive.microsofttranslator.com`**|France Central &bull; West Europe|
|**Switzerland:**</br> For more information, *see* [Switzerland service endpoints](#switzerland-service-endpoints).|Switzerland North &bull; Switzerland West|

#### Switzerland service endpoints

Customers with a resource located in Switzerland North or Switzerland West can ensure that their Text API requests are served within Switzerland. To ensure that requests are handled in Switzerland, create the Translator resource in the `Resource region` `Switzerland North` or `Switzerland West`, then use the resource`s custom endpoint in your API requests.

For example: If you create a Translator resource in Azure portal with `Resource region` as `Switzerland North` and your resource name is `my-swiss-n`, then your custom endpoint is `https&#8203;://my-swiss-n.cognitiveservices.azure.com`. And a sample request to translate is:

 ```bash
// Pass secret key and region using headers to a custom endpoint
curl -X POST "https://my-swiss-n.cognitiveservices.azure.com/translator/text/2025-05-01-preview/translate?to=fr" \
-H "Ocp-Apim-Subscription-Key: xxx" \
-H "Ocp-Apim-Subscription-Region: switzerlandnorth" \
-H "Content-Type: application/json" \
-d "[{`Text`:`Hello`}]" -v
```

> [!NOTE]
> Custom Translator is currently unavailable in Switzerland.

## Metrics

Metrics allow you to view the translator usage and availability information in Azure portal, under metrics section as shown in the following screenshot. For more information, see [Data and platform metrics](/azure/azure-monitor/essentials/data-platform-metrics).

![Screenshot of translator metrics.](../../../media/translatormetrics.png)

This table lists available metrics with description of how they're used to monitor translation API calls.

| Metrics | Description |
|:----|:-----|
| TotalCalls| Total number of API calls.|
| TotalTokenCalls| Total number of API calls via token service using authentication token.|
| SuccessfulCalls| Number of successful calls.|
| TotalErrors| Number of calls with error response.|
| BlockedCalls| Number of calls that exceeded rate or quota limit.|
| ServerErrors| Number of calls with server internal error(5XX).|
| ClientErrors| Number of calls with client-side error(4XX).|
| Latency| Duration to complete request in milliseconds.|
| CharactersTranslated| Total number of characters in incoming text request.|





