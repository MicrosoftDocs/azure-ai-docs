---
title: Overview of web grounding capabilities in Foundry
titleSuffix: Microsoft Foundry
description: Learn how to choose the right web grounding tool for your Microsoft Foundry agents. Compare Web Search, Grounding with Bing Search, and Bing Custom Search.
services: cognitive-services
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: concept-article
ms.date: 01/20/2026
author: alvinashcraft
ms.author: aashcraft
ms.custom: 
 - dev-focus
 - pilot-ai-workflow-jan-2026
ai-usage: ai-assisted
---

# Web grounding tools overview

Large language models work with a knowledge cutoff. They can't access new information beyond a fixed point in time. By connecting with web grounding tools, your agents can incorporate real-time public web data when generating responses. For example, you can ask questions such as "what is the top AI news today" and receive current, cited answers.

## How web grounding works

The grounding process involves several key steps:

1. **Query formulation**: The agent identifies information gaps and constructs search queries based on the user's input.
1. **Search execution**: The grounding tool submits queries to Bing and retrieves results.
1. **Information synthesis**: The agent processes search results and integrates findings into responses.
1. **Source attribution**: The agent provides transparency by citing search sources with URLs.

## Prerequisites

Before using any web grounding tool, ensure you have:

- A [basic or standard agent environment](../../../../agents/environment-setup.md).
- The latest prerelease SDK package. See the [quickstart](../../../../quickstarts/get-started-code.md?view=foundry&preserve-view=true) for installation steps.
- An Azure OpenAI model deployment in your Foundry project.

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
| **Supported parameters**  | - `user_location`: Provides geo‑relevant results<br>- `search_context_size`: low/medium/high (default: medium)<br> Learn more [here](./web-search.md#optional-parameters-for-general-web-search) | - `count`: the maximum of results returned by Bing <br>- `freshness`: specifies the period for the search results<br>- `market`: specifies the region for the search results <br>- `set_lang`: specifies the language for the search results <br> Learn more [here](./bing-tools.md#optional-parameters) |
| **Supported models**      | Azure OpenAI models                                                                       | Azure OpenAI models and Azure direct models                                                                          |

### Use case 2: grounding from specific domains you defined

|                               |[Grounding with Bing Custom Search](./bing-tools.md)                                                                 |
|-------------------------------|--------------------------------------------------------------------------------------------------|
| **Stage**                     | Preview                                                                                  |
| **Pre-defined domains**       | Supported — use `custom_search_configuration` to pre‑define allowed or blocked domains (requires creating a Bing Custom Search resource + instance) |
| **Other parameters**          |  - `count`: the maximum number of results returned by Bing <br>- `freshness`: specifies the period for the search results<br>- `market`: specifies the region for the search results <br>- `set_lang`: specifies the language for the search results <br> Learn more [here](./bing-tools.md#optional-parameters) |
| **Supported models**          |  Azure OpenAI models and Azure direct models |

## Common questions

### Which tool should I use if I'm just getting started?

Use [Web Search (preview)](./web-search.md). It requires no additional Azure resources, handles Bing resource management automatically, and provides geo-relevant results with the `user_location` parameter.

### Can I use web grounding tools with network-secured Foundry projects?

Web grounding tools don't respect VPN or private endpoints. They act as public endpoints. Consider this security implication when using network-secured Foundry with these tools.

### How do I restrict search results to specific websites?

Use [Grounding with Bing Custom Search (preview)](./bing-tools.md). This tool lets you define an allow-list or block-list of domains, so search results come only from sources you approve.

### Are there additional costs for web grounding?

Yes. Web Search (preview), Grounding with Bing Search and Grounding with Bing Custom Search (preview) incur costs beyond standard Azure OpenAI usage. See [pricing details](https://www.microsoft.com/bing/apis/grounding-pricing).

## Troubleshooting

| Issue | Likely cause | Resolution |
| --- | --- | --- |
| Agent doesn't use web grounding | Tool not configured or model doesn't support the tool. | Verify the tool is added to your agent definition. Use `tool_choice="required"` to force tool use. Check that your model deployment supports the tool. |
| No citations in response | The model generated a response without using search results. | Add explicit instructions to always cite sources. Use `tool_choice="required"` to ensure tool invocation. |
| Search results aren't relevant | Query formulation didn't capture user intent. | Improve agent instructions to guide query construction. For Bing tools, adjust `market` and `set_lang` parameters. |
| Tool blocked by administrator | Your organization disabled web grounding tools. | Contact your Azure administrator to enable access. See [administrator control](./web-search.md#administrator-control-for-the-web-search-tool). |
| Unexpected costs | Web grounding tools have usage-based pricing. | Review [pricing details](https://www.microsoft.com/bing/apis/grounding-pricing) and implement rate limiting if needed. |

## Next steps

> [!div class="nextstepaction"]
> [Use Web Search tool (preview)](./web-search.md)
- [Use Grounding with Bing Search and Grounding with Bing Custom Search](./bing-tools.md)
- [Best practices for using tools in Microsoft Foundry Agent Service](../../concepts/tool-best-practice.md)
