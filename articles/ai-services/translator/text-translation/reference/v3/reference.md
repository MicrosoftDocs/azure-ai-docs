---
title: Translator V3.0 Reference
titleSuffix: Foundry Tools
description: Reference documentation for the Translator V3.0. Version 3.0 of the Translator provides a modern JSON-based Web API.
author: laujan
manager: mcleans
ms.service: azure-translator-foundry-tools
ms.topic: reference
ms.date: 06/02/2026
ms.author: lajanuar
ai-usage: ai-assisted
---

# Azure Translator in Foundry Tools v3.0

## What's new?

Version 3.0 of the Translator provides a modern JSON-based Web API. It improves usability and performance by consolidating existing features into fewer operations and it provides new features.

* Transliteration to convert text in one language from one script to another script.
* Translation to multiple languages in one request.
* Language detection, translation, and transliteration in one request.
* Dictionary to look up alternative translations of a term, to find back-translations and examples showing terms used in context.
* More informative language detection results.

## Base URLs

The global base URL is `https://api.cognitive.microsofttranslator.com`. Text translation also supports geography and resource-specific endpoints. For all endpoint URLs and their request processing locations, see [Region support for Azure Translator](../../../region-support.md).

## Virtual Network support

The Translator is now available with Virtual Network (`VNET`) capabilities in all regions of the Azure public cloud. To enable Virtual Network, *See* [Configuring Foundry Tools virtual networks](../../../../cognitive-services-virtual-networks.md?tabs=portal).

Once you turn on this capability, you must use the custom endpoint to call the Translator. You can't use the global translator endpoint ("api.cognitive.microsofttranslator.com") and you can't authenticate with an access token.

You can find the custom endpoint after you create a [translator resource](https://portal.azure.com/#create/Microsoft.CognitiveServicesTextTranslation) and allow access from selected networks and private endpoints.

1. Navigate to your Translator resource in the Azure portal.
1. Select **Networking** from the **Resource Management** section.
1. Under the **Firewalls and virtual networks** tab, choose **Selected Networks and Private Endpoints**.

   :::image type="content" source="../../../media/virtual-network-setting-azure-portal.png" alt-text="Screenshot of the virtual network setting in the Azure portal.":::

1. Select **Save** to apply your changes.
1. Select **Keys and Endpoint** from the **Resource Management** section.
1. Select the **Virtual Network** tab.
1. Listed there are the endpoints for Text translation and Document translation.

   :::image type="content" source="../../../media/virtual-network-endpoint.png" alt-text="Screenshot of the virtual network endpoint.":::

|Headers|Description|
|:-----|:----|
|Ocp-Apim-Subscription-Key| The value is the Azure secret key for your subscription to Translator.|
|Ocp-Apim-Subscription-Region| The value is the region of the translator resource. This value is optional if the resource is `global`|

Here's an example request to call the Translator using the custom endpoint

```curl
// Pass secret key and region using headers
curl -X POST "https://<your-custom-domain>.cognitiveservices.azure.com/translator/text/v3.0/translate?api-version=3.0&to=es" \
     -H "Ocp-Apim-Subscription-Key:<your-key>" \
     -H "Ocp-Apim-Subscription-Region:<your-region>" \
     -H "Content-Type: application/json" \
     -d "[{'Text':'Hello, what is your name?'}]"
```

## Metrics
Metrics allow you to view the translator usage and availability information in Azure portal. For more information, see [Data and platform metrics](/azure/azure-monitor/essentials/data-platform-metrics).

![Translator Metrics](../../../media/azure-portal-metrics-v3.png)

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
