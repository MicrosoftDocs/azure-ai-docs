---
title: Serp API tool for flows in Microsoft Foundry portal
titleSuffix: Microsoft Foundry
description: This article introduces you to the Serp API tool for flows in Microsoft Foundry portal.
ms.service: azure-ai-foundry
ms.subservice: azure-ai-prompt-flow
ms.custom:
  - ignite-2023
  - build-2024
  - hub-only
ms.topic: article
ms.date: 01/27/2026
ms.reviewer: none
ms.author: lagayhar
author: lgayhardt
ms.collection: ce-skilling-ai-copilot, ce-skilling-fresh-tier1
ms.update-cycle: 180-days
---

# Serp API tool for flows in Microsoft Foundry portal

[!INCLUDE [classic-banner](../../includes/classic-banner.md)]

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

The prompt flow Serp API tool provides a wrapper to the [Serp API Google Search Engine Results API](https://serpapi.com/search-api) and [Serp API Bing Search Engine Results API](https://serpapi.com/bing-search-api).

Use the tool to retrieve search results from many different search engines, including Google and Bing. Specify a range of search parameters, such as the search query, location, and device type.

## Prerequisites

[!INCLUDE [hub-only-prereq](../../includes/hub-only-prereq.md)]

Sign up on the [Serp API home page](https://serpapi.com/).

To create a Serp connection:

1. [!INCLUDE [classic-sign-in](../../includes/classic-sign-in.md)]
1. Go to project settings by selecting  **Management Center** > **Overview**.
1. Under *Connected resources*, select **+ New connection**.
1. Under *Other resource types*, select **Serp**.
1. Add your API key for Serp and make a connection name. Then select **Add connection**.

    :::image type="content" source="../../media/prompt-flow/serp-connection-keys.png" alt-text="Screenshot that shows adding Serp connection in Microsoft Foundry portal." lightbox="../../media/prompt-flow/serp-connection-keys.png":::

The connection is the model used to establish connections with the Serp API. Get your API key from the Serp API account dashboard.

| Type        | Name     | API key  |
|-------------|----------|----------|
| Serp        | Required | Required |

## Build with the Serp API tool

1. Create or open a flow in [Foundry](https://ai.azure.com/?cid=learnDocs). For more information, see [Create a flow](../flow-develop.md).
1. Select **+ More tools** > **Serp API** to add the Serp API tool to your flow.

    :::image type="content" source="../../media/prompt-flow/serp-api-tool.png" alt-text="Screenshot that shows the Serp API tool added to a flow in Foundry portal." lightbox="../../media/prompt-flow/serp-api-tool.png":::

1. Select the connection to one of your provisioned resources. For example, select **Serp Connection** if you created a connection with that name. For more information, see [Prerequisites](#prerequisites).
1. Enter values for the Serp API tool input parameters described in the [Inputs table](#inputs).
1. Add more tools to your flow, as needed. Or select **Run** to run the flow.
1. The outputs are described in the [Outputs table](#outputs).

## Inputs

The following input parameters are available.

| Name     | Type    | Description                                                   | Required |
|----------|---------|---------------------------------------------------------------|----------|
| query    | string  | The search query to execute.                                  | Yes      |
| engine   | string  | The search engine to use for the search. Default is `google`. | Yes      |
| num      | integer | The number of search results to return. Default is 10.         | No      |
| location | string  | The geographic location from which to execute the search.           | No       |
| safe     | string  | The safe search mode to use for the search. Default is off. | No       |

## Outputs

The JSON representation from a `serpapi` query:

| Engine   | Return type | Output                                                |
|----------|-------------|-------------------------------------------------------|
| Google   | json        | [Sample](https://serpapi.com/search-api#api-examples) |
| Bing     | json        | [Sample](https://serpapi.com/bing-search-api)         |

## Next steps

- [Learn more about how to create a flow](../flow-develop.md)
