---
title: Create a Web Knowledge Source for Agentic Retrieval
titleSuffix: Azure AI Search
description: Learn how to create a web knowledge source that uses  for agentic retrieval workloads in Azure AI Search.
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.custom:
  - ignite-2025
ms.topic: how-to
ms.date: 10/17/2025
---

# Create a web knowledge source

> [!IMPORTANT]
> + Web Knowledge Source, which uses Grounding with Bing Search and/or Grounding with Bing Custom Search, is a [First Party Consumption Service](https://www.microsoft.com/licensing/terms/product/ForOnlineServices/EAEAS) governed by the [Grounding with Bing terms of use](https://www.microsoft.com/en-us/bing/apis/grounding-legal-enterprise) and the [Microsoft Privacy Statement](https://www.microsoft.com/en-us/privacy/privacystatement).
>
> + The [Microsoft Data Protection Addendum](https://www.microsoft.com/licensing/docs/view/Microsoft-Products-and-Services-Data-Protection-Addendum-DPA) doesn't apply to data sent to Web Knowledge Source. When Customer uses Web Knowledge Source, Customer Data flows outside the Azure compliance and Geo boundary.
>
> + Use of Web Knowledge Source incurs costs; learn more about [pricing](https://www.microsoft.com/en-us/bing/apis/grounding-pricing).
>
> + Learn more about how Azure admins can [manage access to use of Web Knowledge Source](agentic-knowledge-source-how-to-web-manage.md).

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

A *web knowledge source* enables retrieval of real-time web data from Microsoft Bing in an agentic retrieval pipeline. [Knowledge sources](agentic-knowledge-source-overview.md) are created independently, referenced in a [knowledge base](agentic-retrieval-how-to-create-knowledge-base.md), and used as grounding data when an agent or chatbot calls a [retrieve](/rest/api/searchservice/knowledge-retrieval/retrieve?view=rest-searchservice-2025-11-01-preview&preserve-view=true) action at query time.

Depending on its configuration, a web knowledge source either has unrestricted access to the entire public internet or is scoped to specific domains, such as https://learn.microsoft.com. This means that, unlike most knowledge sources, it doesn't target an index in Azure AI Search.

Web knowledge sources work best alongside other knowledge sources. Use them when your proprietary content doesn't provide complete, up-to-date answers or when you want to supplement results with information from a commercial search engine.

When you use web knowledge sources, keep the following in mind:

+ The response is always a single, formulated answer to the query instead of raw search results from the web.

+ Because web knowledge sources don't support extractive data, your knowledge base must use [answer synthesis](agentic-retrieval-how-to-answer-synthesis.md) and [low or medium reasoning effort](agentic-retrieval-how-to-create-knowledge-base.md#create-a-knowledge-base). You also can't define answer instructions.

## Prerequisites

+ An Azure subscription with [access to web knowledge sources](agentic-knowledge-source-how-to-web-manage.md). By default, access is enabled. Contact your admin if access is disabled.

+ An [Azure AI Search service](search-create-service-portal.md) on the Basic tier or higher with [semantic ranker enabled](semantic-how-to-enable-disable.md).

+ [Visual Studio Code](https://code.visualstudio.com/) with the [REST Client extension](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) or a preview package of an Azure SDK that provides the latest knowledge source REST APIs. Currently, there's no portal support.

## Check for existing knowledge sources

[!INCLUDE [Check for existing knowledge sources](includes/how-tos/knowledge-source-check-rest.md)]

The following JSON is an example response for a web knowledge source.

```json
{
  "name": "my-web-ks",
  "kind": "web",
  "description": "A sample web knowledge source.",
  "encryptionKey": null,
  "webParameters": {
    "domains": null
  }
}
```

## Create a knowledge source

To create a web knowledge source:

1. Set environment variables at the top of your file.

    ```http
    @search-url = <YOUR SEARCH SERVICE URL>
    @api-key = <YOUR ADMIN API KEY>
    ```

1. Use the 2025-11-01-preview of [Knowledge Sources - Create or Update (REST API)](/rest/api/searchservice/knowledge-sources/create-or-update?view=rest-searchservice-2025-11-01-preview&preserve-view=true) or an Azure SDK preview package that provides equivalent functionality to formulate the request.

    ```http
    POST {{search-url}}/knowledgesources/my-web-ks?api-version=2025-11-01-preview
    Content-Type: application/json
    api-key: {{api-key}}

    {
      "name": "my-web-ks",
      "kind": "web",
      "description": "This knowledge source pulls content from the web.",
      "encryptionKey": null,
      "webParameters": {
        "domains": {
          "allowedDomains": [ { "address": "learn.microsoft.com", "includeSubpages": true } ],
          "blockedDomains": [ { "address": "bing.com", "includeSubpages": false } ]
        }
      }
    }
    ```

1. Select **Send Request**.

### Source-specific properties

You can pass the following properties to create a web knowledge source.

| Name | Description | Type | Required |
|--|--|--|--|
| `name` | The name of the knowledge source, which must be unique within the knowledge sources collection and follow the [naming guidelines](/rest/api/searchservice/naming-rules) for objects in Azure AI Search. | String | Yes |
| `kind` | The kind of knowledge source, which is `web` in this case. | String | Yes |
| `description` | A description of the knowledge source. | String | No |
| `encryptionKey` | A [customer-managed key](search-security-manage-encryption-keys.md) to encrypt sensitive information in the knowledge source. | Object | No |
| `webParameters` | Parameters specific to web knowledge sources. Currently, this is only `domains`. | Object | No |
| `domains` | Domains to allow or block from the search space. The knowledge source uses [Grounding with Bing Search](/azure/ai-foundry/agents/how-to/tools/bing-grounding) by default. However, if you specify domains, the knowledge source uses [Grounding with Bing Custom Search](/azure/ai-foundry/agents/how-to/tools/bing-custom-search). | Object | No |
| `allowedDomains` | Domains to include in the search space. For each domain, you must specify its `address` in the `website.com` format. You can also specify whether to include the domain's subpages by setting `includeSubpages` to `true` or `false`. | Array | No |
| `blockedDomains` | Domains to exclude from the search space. For each domain, you must specify its `address` in the `website.com` format. You can also specify whether to include the domain's subpages by setting `includeSubpages` to `true` or `false`. | Array | No |

## Assign to a knowledge base

If you're satisfied with the web source, continue to the next step: specifying the knowledge source in a [knowledge base](agentic-retrieval-how-to-create-knowledge-base.md).

Within the knowledge base, there are more properties to set on the knowledge source that are specific to query operations.

## Delete a knowledge source

[!INCLUDE [Delete knowledge source](includes/how-tos/knowledge-source-delete-rest.md)]

## Related content

+ [Manage access to web knowledge sources in your Azure subscription](agentic-knowledge-source-how-to-web-manage.md)
+ [Agentic retrieval in Azure AI Search](search-agentic-retrieval-concept.md)
