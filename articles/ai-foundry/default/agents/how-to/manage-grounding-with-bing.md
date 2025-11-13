---
title: Disable Use of Grounding With Bing
titleSuffix: Microsoft Foundry
description: Learn how to manage Grounding With Bing in Microsoft Foundry and Azure.
author: haileytap
ms.author: haileytapia
ms.reviewer: magottei
ms.service: azure-ai-foundry
ms.topic: how-to
ms.date: 11/13/2025
---

# Manage Grounding With Bing in Microsoft Foundry and Azure

Grounding with Bing enables agents to retrieve and incorporate real-time public web data into model-generated responses. It supports summarization, question answering, conversational assistance, and other scenarios by using Grounding with Bing Search or Grounding with Bing Custom Search to fill knowledge gaps.

Grounding is available across features in Foundry Agent Service and Azure AI Search. You might need to disable access to these features to meet compliance, privacy, or data governance requirements.

As an admin, you can manage access to Grounding with Bing in the following ways:

+ [Disable Grounding with Bing Search tools](#disable-grounding-with-bing-search-tools) in Foundry Agent Service.
+ [Disable web search tool](#disable-web-search-tool) in Foundry Agent Service.
+ [Disable web knowledge](#disable-web-knowledge) in Azure AI Search.

## Disable Grounding with Bing Search tools

You can disable Grounding with Bing Search and/or Grounding with Bing Custom Search at the subscription or resource group level. For more information, see [Disable use of Grounding with Bing Search and Grounding with Bing Custom Search](./tools/bing-tools.md#disable-use-of-grounding-with-bing-search-and-grounding-with-bing-custom-search).

## Disable web search tool

You can disable the web search tool for all accounts in a subscription. For more information, see [Disable Bing Web Search](../how-to/tools/web-search.md#disable-bing-web-search).

## Disable web knowledge

You can disable Web Knowledge Source access for all search services in a subscription. For more information, see [Disable use of Web Knowledge Source](../../../../search/agentic-knowledge-source-how-to-web-manage.md#disable-use-of-web-knowledge-source).

## Related content

+ [Grounding with Bing Search tools for agents](./tools/bing-tools.md)
+ [Web search tool (preview)](../how-to/tools/web-search.md)
+ [Create a Web Knowledge Source resource](../../../../search/agentic-knowledge-source-how-to-web.md)
