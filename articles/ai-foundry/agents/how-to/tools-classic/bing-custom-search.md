---
title: 'How to use Custom Bing Search with Foundry Agent Service'
titleSuffix: Azure OpenAI
description: Learn how to ground Azure AI Agents using Custom Bing Search results.
ai-usage: ai-assisted
services: cognitive-services
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: how-to
ms.date: 12/22/2025
author: alvinashcraft
ms.author: aashcraft
ms.custom: azure-ai-agents
---

# Grounding with Bing Custom Search (preview)

> [!NOTE]
> This article refers to the classic version of the agents API. 
>
> 🔍 [View the new Grounding with Bing Search documentation](../../../default/agents/how-to/tools/bing-tools.md).

Grounding with Bing Custom Search tool allows your Azure AI Agents to search within a configurable set of public web domains. It allows you to define the parts of the web you want to draw from so users only see relevant results from the domains and subdomains of your choosing. You need to first create a Grounding with Bing Custom Search resource in Azure portal. 

Once the resource is deployed, go to **Configurations** in the Microsoft Foundry portal, and create a configuration instance to include content only from websites that your users care about. Instructions about how to create your custom configuration can be found in the [setup section](#setup).

Once the tool is configured, you can connect it to your Azure AI Agent. When a user sends a query, the agent will decide if Grounding with Bing Custom Search should be leveraged or not. If so, it will use Bing to search over the domains you specify and return relevant chunks. Lastly, Azure AI Agents will use the returned chunks to generate a response to return to the user 

> [!IMPORTANT]
>  
> * Your usage of Grounding with Bing Custom Search can incur costs. See the pricing page for details. 
> * By creating and using a Grounding with Bing Custom Search resource through code-first experience, such as Azure CLI, or deploying through deployment template, you agree to be bound by and comply with the [terms of use](https://www.microsoft.com/bing/apis/grounding-legal), which may be updated periodically. 
> * When you use Grounding with Bing Custom Search, your customer data is transferred outside of the Azure compliance boundary to the Grounding with Bing Custom Search service. Grounding with Bing Custom Search isn't subject to the same data processing terms (including location of processing) and doesn't have the same compliance standards and certifications as the Foundry Agent Service, as described in the Grounding with Bing Custom Search Terms of Use. It's your responsibility to assess whether use of Grounding with Bing Custom Search in your agent meets your needs and requirements. 

## How Grounding with Bing Custom Search works 

The user query is the message that an end user sends to an agent, such as "what water bottle is available?" (assuming you create an instance to Contoso product websites). Instructions are the system message a developer can provide to share context and provide instructions to the AI model on how to use various tools or behave. 

When a user sends a query, the customer's AI model deployment first processes it (using the provided instructions) to later perform a Bing Custom Search query (which is visible to developers). Grounding with Bing Custom Search returns relevant search results to the customer's model deployment, which then generates the final output. 

> [!NOTE]
> When you use Grounding with Bing Custom Search, the Bing Custom Search query, the configuration instance, tool parameters, and your resource key are sent to Bing. The query doesn't include any end user-specific information. You send your resource key to Bing solely for billing and rate limiting purposes. 

The authorization will happen between Grounding with Bing Custom Search service and Foundry Agent service. Any Bing Custom Search query that is generated and sent to Bing for the purposes of grounding is transferred, along with the resource key and configuration instance, outside of the Azure compliance boundary to the Grounding with Bing Custom Search service. Grounding with Bing Custom Search is subject to Bing's terms and don't have the same compliance standards and certifications as the Agent Service, as described in the Grounding with Bing Custom Search Terms of Use. It's your responsibility to assess whether the use of Grounding with Bing Custom Search in your agent meets your needs and requirements. 

Developers and end users don't have access to raw content returned from Grounding with Bing Custom Search. The model response, however, includes citations with links to the websites used to generate the response and is allowed to be stored using the mechanisms provided by the Agents Service. You can retrieve the model response by accessing the data in the thread that was created. These references must be retained and displayed in the exact form provided by Microsoft, as per Grounding with Bing Custom Search's Use and Display Requirements. 

## Understand citations in the agent response

When Grounding with Bing Custom Search contributes to an agent response, the response can include URL citations that help users verify the answer.

In the client SDKs, URL citations are returned as annotations on the agent message. Each citation includes a title and URL that you can show to users as a list of references.

For an end-to-end example that prints citations from a thread message, see the [code samples](bing-custom-search-samples.md).

Transactions with your Grounding with Bing resource are counted by the number of tool calls per run. You can see how many tool calls are made from the run step.

## Setup 

> [!NOTE]
> Grounding with Bing Search tool works in your network secured Foundry, but the tool doesn't respect your VPN or Private Endpoints to Foundry. It acts as a public endpoint. Please make this security consideration when you use network secured Foundry with this tool.

1. Create an Azure AI Agent by following the steps in the [quickstart](../../quickstart.md). 

1. Create a Grounding with Bing Custom Search resource in the [Azure portal](https://portal.azure.com/#create/Microsoft.BingGroundingCustomSearch). You need to have **Owner** or **Contributor** role in your subscription or resource group to create it. Make sure you create this Grounding with Bing Custom Search resource in the same resource group as your Azure AI Agent, AI Project, and other resources. 


1. After you have created a Grounding with Bing Custom Search resource, you can create a configuration instance.  

    1. Go to the Grounding with Bing Custom Search resource created 

    1. Select **Resource Management** on the left panel. 

    1. Select **Configurations**. 

    1. Select **Create a new configuration**. 

When you create or update a configuration, enter the following information: 

1. The name of your configuration. You can change this name at any time. 

1. Include URLs to define your search slices in at least one of the following fields: 

    > [!NOTE]
    > Grounding with Bing Custom Search only returns results for domains and webpages that are public and indexed by Bing. 
    > * Domain (for example, `https://www.microsoft.com`) 
    > * Domain and path (for example, `https://www.microsoft.com/surface`) 
    > * Webpage (for example, `https://www.microsoft.com/en-us/p/surface-earbuds/8r9cpq146064`) 

    1. Allowed domains to search against. For allowed domains, if you want to include subpages, make sure the domains have at most two levels of subpages. 

    1. Blocked domains to exclude from the search space. 


1. Determine if you want to include subpages. A subpage slice specifies a domain path. Bing searches all content found at and below the path. You can specify a maximum of two subfolders in the path. For example, `www.microsoft.com/windows/`. 

1. Adjust ranking if needed. 


1. Navigate to the **Agents** screen for your agent in the [Foundry portal](https://ai.azure.com/?cid=learnDocs), scroll down the Setup pane on the right to **knowledge**. Then select **Add**.

    :::image type="content" source="../../media\tools\knowledge-tools.png" alt-text="A screenshot of the agents screen in the Foundry portal.":::

1. Select the **Grounding with Bing Custom Search** tool.  

1. Select to create a new connection, or use an existing connection 

    1. For a new connection, select your Grounding with Bing Custom Search resource. 

1. Once you have connected to a resource, select the configuration name. 

1. Save the tool and start chatting with your agent. 

## Custom Search configuration capabilities 

Grounding with Bing Custom Search is a powerful tool that allows you to select a subspace of the web to limit your Agent’s grounding knowledge. Here you can find a few tips for how to take the maximum advantage of this capability: 

1. If you own a public site that you want to include in the search but Bing hasn't indexed, see the [Bing webmaster documentation](https://www.bing.com/webmaster/help/webmaster-guidelines-30fba23a) for details about getting your site indexed. The webmaster documentation also provides details about getting Bing to crawl your site if the index is out of date. 

1. You can only block certain domains and perform a search against the rest of the Web (a competitor’s site, for example). 


## Optional parameters

When you add the Grounding with Bing Custom Search tool to your agent, you can pass the following parameters. These parameters will impact the Grounding with Bing Custom Search tool output, and the AI model might not fully use all of the outputs. See the [code examples](bing-custom-search-samples.md) for information on API version support and how to pass these parameters.

|Name|Value|Type|Required|
|-|-|-|-|
|`count`|The number of search results to return in the response. The default is 5 and the maximum value is 50. The actual number delivered might be less than requested. It's possible for multiple pages to include some overlap in results. This parameter affects only web page results. It's possible that AI model might not use all search results returned by Bing.|`UnsignedShort`|No |
|`freshness`|Filter search results by the following case-insensitive age values: <br/> **Day**: Return webpages that Bing discovered within the last 24 hours.<br/> **Week**: Return webpages that Bing discovered within the last 7 days.<br/> **Month**: Return webpages that Bing discovered within the last 30 days. To get articles discovered by Bing during a specific timeframe, specify a date range in the form: `YYYY-MM-DD..YYYY-MM-DD`. For example, `freshness=2019-02-01..2019-05-30`. To limit the results to a single date, set this parameter to a specific date. For example, `freshness=2019-02-04`.|String|No |
|`market`|The market where the results come from. Typically, `mkt` is the country/region where the user is making the request from. However, it could be a different country/region if the user isn't located in a country/region where Bing delivers results. The market must be in the form: `<language>-<country/region>`. For example, `en-US`. The string is case insensitive. For a list of possible market values, see [Market codes](/bing/search-apis/bing-web-search/reference/market-codes). If known, you're encouraged to always specify the market. Specifying the market helps Bing route the request and return an appropriate and optimal response. If you specify a market that is not listed in Market codes, Bing uses a best fit market code based on an internal mapping that is subject to change. |String|No |
|`set_lang`|The language to use for user interface strings. Specify the language by using either a 2-letter or 4-letter code. Using 4-letter codes is preferred.<br/> For a list of supported language codes, see [Bing supported languages](/bing/search-apis/bing-web-search/reference/market-codes#bing-supported-language-codes).<br/> Bing loads the localized strings if `setlang` contains a valid 2-letter neutral culture code (`fr`) or a valid 4-letter specific culture code (`fr-ca`). For example, for `fr-ca`, Bing loads the `fr` neutral culture code strings.<br/> If `setlang` isn't valid (for example, `zh`) or Bing doesn’t support the language (for example, `af`, `af-na`), Bing defaults to `en` (English).<br/> To specify the 2-letter code, set this parameter to an ISO 639-1 language code.<br/> To specify the 4-letter code, use the form `<language>-<country/region>` where `<language>` is an ISO 639-1 language code (neutral culture) and `<country/region>` is an ISO 3166 country or region (specific culture) code. For example, use `en-US` for United States English.<br/> Although optional, always specify the language. Typically, set `setLang` to the same language specified by `mkt` unless the user wants the user interface strings displayed in a different language.|String|No|
