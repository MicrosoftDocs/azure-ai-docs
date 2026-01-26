---
title: Overview of web grounding capabilities in Foundry
titleSuffix: Microsoft Foundry
description: Learn how to ground agent responses with web data.
services: cognitive-services
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: how-to
ms.date: 01/20/2026
author: alvinashcraft
ms.author: aashcraft
ms.custom: 
 - dev-focus
 - pilot-ai-workflow-jan-2026
ai-usage: ai-assisted
zone_pivot_groups: selection-bing-grounding-new
---
# Web Grounding Tools Overview

Large language models work with a knowledge cutoff. They can't access new information beyond a fixed point in time. By connecting with web, your agents can incorporate real-time public web data when generating responses. By using these tools, you can ask questions such as "what is the top AI news today". 

The grounding process involves several key steps: 

- Query formulation: The agent identifies information gaps and constructs search queries.
- Search execution: The grounding tool submits queries to search engines and retrieves results.
- Information synthesis: The agent processes search results and integrates findings into responses.
- Source attribution: The agent provides transparency by citing search sources. 

>[!IMPORTANT]
> - Web Search (preview) uses Grounding with Bing Search and Grounding with Bing Custom Search are [First Party Consumption Services](https://www.microsoft.com/licensing/terms/product/Glossary/EAEAS#:~:text=First-Party%20Consumption%20Services) with [terms for online services](https://www.microsoft.com/licensing/terms/product/ForOnlineServices/EAEAS). They're governed by the [Grounding with Bing terms of use](https://www.microsoft.com/bing/apis/grounding-legal-enterprise) and the [Microsoft Privacy Statement](https://go.microsoft.com/fwlink/?LinkId=521839&clcid=0x409). 
> - The Microsoft [Data Protection Addendum](https://aka.ms/dpa) doesn't apply to data sent to Grounding with Bing Search or Grounding with Bing Custom Search. When you use these services, your data flows outside the Azure compliance and Geo boundary. This also means use of these services waives all elevated Government Community Cloud security and compliance commitments, including data sovereignty and screened/citizenship-based support, as applicable.  
> - Use of Grounding with Bing Search and Grounding with Bing Custom Search incurs costs. See pricing for [details](https://www.microsoft.com/bing/apis/grounding-pricing). 
> - See the management section for information about how Azure admins can manage access to use of Grounding with Bing Search and Grounding with Bing Custom Search.

## Determine the best tool for your use cases

### Use case 1: grounding from general web indexed by Bing

|                           | [Web Search](./web-search.md) (recommended)                                                                                                                    | [Grounding with Bing Search](./bing-tools.md)                                                                                   |
|---------------------------|----------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------|
| **Stage**                 | Preview                                                                                                                                           | GA                                                                                                            |
| **Grounding with Bing resource** | Managed by Microsoft                                                                                                                           | Managed by you — requires creating a Grounding with Bing Search resource first                               |
| **Supported parameters**  | - `user_location`: Provides geo‑relevant results<br>- `search_context_size`: low/medium/high (default: medium)<br> Learn more [here](./web-search.md#options) | - `count`: the maximum of results returned by Bing <br>- `freshness`: specifies the period for the search results<br>- `market`: specifies the region for the search results <br>- `set_lang`: specifies the language for the search results <br> Learn more [here](./bing-tools.md#optional-parameters) |
| **Supported models**      | Azure OpenAI models                                                                       | Azure OpenAI models and Azure direct models                                                                          |

### Use case 2: grounding from specific domains you defined

|                               |[Grounding with Bing Custom Search](./bing-tools.md)                                                                 |
|-------------------------------|--------------------------------------------------------------------------------------------------|
| **Stage**                     | Preview                                                                                  |
| **Pre-defined domains**       | Supported — use `custom_search_configuration` to pre‑define allowed/blocked domains (requires creating a Bing Custom Search resource + instance)|
| **Other parameters**          |  - `count`: the maximum of results returned by Bing <br>- `freshness`: specifies the period for the search results<br>- `market`: specifies the region for the search results <br>- `set_lang`: specifies the language for the search results <br> Learn more [here](./bing-tools.md#optional-parameters) |
| **Supported models**          |  Azure OpenAI models and Azure direct models                                                             |
