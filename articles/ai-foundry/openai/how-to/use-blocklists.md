---
title: 'How to use block lists in Microsoft Foundry models'
titleSuffix: Azure OpenAI
description: Learn how to use block lists with Azure OpenAI
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: how-to
ms.date: 02/10/2026
author: PatrickFarley
ms.author: pafarley
monikerRange: 'foundry-classic || foundry'
ai-usage: ai-assisted
---

# How to use block lists in Microsoft Foundry models

[!INCLUDE [version-banner](../../includes/version-banner.md)]

::: moniker range="foundry"

The [configurable Guardrails and controls](/azure/ai-foundry/openai/how-to/content-filters) available in Microsoft Foundry are sufficient for most content moderation needs. However, you might need to filter terms specific to your use case—such as competitor names, internal project names, or domain-specific sensitive terms. For this, you can create custom block lists that automatically filter content containing your specified terms.

In this article, you learn how to:

- Create and manage custom blocklists
- Add terms using exact match or regex patterns
- Apply blocklists to your content filters
- Test blocklist behavior with your deployments

::: moniker-end

::: moniker range="foundry-classic"

The [configurable content filters](/azure/ai-foundry/openai/how-to/content-filters) available in Azure OpenAI are sufficient for most content moderation needs. However, you might need to filter terms specific to your use case—such as competitor names, internal project names, or domain-specific sensitive terms. For this, you can create custom block lists that automatically filter content containing your specified terms.

In this article, you learn how to:

- Create and manage custom blocklists
- Add terms using exact match or regex patterns
- Apply blocklists to your content filters
- Test blocklist behavior with your deployments

::: moniker-end

## Prerequisites

- An Azure subscription. [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- Once you have your Azure subscription, create an Azure OpenAI resource in the Azure portal to get your token, key, and endpoint. Enter a unique name for your resource, select the subscription you entered on the application form, select a resource group, supported region, and supported pricing tier. Then select **Create**.
    - The resource takes a few minutes to deploy. After it finishes, select **go to resource**. In the left pane, under **Resource Management**, select **Subscription Key and Endpoint**. The endpoint and either of the keys are used to call APIs.
- [Azure CLI](/cli/azure/install-azure-cli) version 2.50 or later
- [cURL](https://curl.haxx.se/) installed

## Use block lists


#### [Azure OpenAI API](#tab/api)

You can create block lists with the Azure OpenAI API. The following steps help you get started. 

### Get your token

First, you need to get a token for accessing the APIs for creating, editing, and deleting block lists. You can get this token using the following Azure CLI command: 

```bash
az account get-access-token 
```

### Create or modify a blocklist

Copy the cURL command below to a text editor and make the following changes: 

1. Replace {subscriptionId} with your subscription ID. 
1. Replace {resourceGroupName} with your resource group name. 
1. Replace {accountName} with your resource name. 
1. Replace {raiBlocklistName} (in the URL) with a custom name for your list. Allowed characters: `0-9, A-Z, a-z, - . _ ~`. 
1. Replace {token} with the token you got from the "Get your token" step above. 
1. Optionally replace the value of the "description" field with a custom description.

```bash
curl --location --request PUT 'https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CognitiveServices/accounts/{accountName}/raiBlocklists/{raiBlocklistName}?api-version=2024-04-01-preview' \ 
--header 'Authorization: Bearer {token}' \ 
--header 'Content-Type: application/json' \ 
--data-raw '{ 
    "properties": { 
        "description": "This is a prompt blocklist"  
    } 
}' 
```

The response code should be `201` (created a new list) or `200` (updated an existing list). 

### Apply a blocklist to a content filter

If you haven't yet created a content filter, you can do so in [Foundry](https://ai.azure.com/?cid=learnDocs). See [Content filtering](/azure/ai-foundry/openai/how-to/content-filters#create-a-content-filter-in-azure-ai-foundry).

To apply a **completion** blocklist to a content filter, use the following cURL command: 

1. Replace {subscriptionId} with your sub ID. 
1. Replace {resourceGroupName} with your resource group name. 
1. Replace {accountName} with your resource name. 
1. Replace {raiPolicyName} with the name of your Content Filter 
1. Replace {token} with the token you got from the "Get your token" step above. 
1. Optionally change the `"completionBlocklists"` title to `"promptBlocklists"` if you want the blocklist to apply to user prompts instead of AI model completions.
1. Replace `"raiBlocklistName"` in the body with a custom name for your list. Allowed characters: `0-9, A-Z, a-z, - . _ ~`. 

```bash
curl --location --request PUT 'https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CognitiveServices/accounts/{accountName}/raiPolicies/{raiPolicyName}?api-version=2024-04-01-preview' \ 
--header 'Authorization: Bearer {token}' \ 
--header 'Content-Type: application/json' \ 
--data-raw '{ 
    "properties": { 
        "basePolicyName": "Microsoft.Default", 
        "completionBlocklists": [{ 
            "blocklistName": "raiBlocklistName", 
            "blocking": true 
        }], 
        "contentFilters": [ ] 
    } 
}' 
```

### Add blockItems to the list

> [!NOTE]
> There's a maximum limit of 10,000 terms allowed in one list.

Copy the cURL command below to a text editor and make the following changes:
1. Replace {subscriptionId} with your sub ID. 
1. Replace {resourceGroupName} with your resource group name. 
1. Replace {accountName} with your resource name. 
1. Replace {raiBlocklistName} (in the URL) with a custom name for your list. Allowed characters: `0-9, A-Z, a-z, - . _ ~`. 
1. Replace {raiBlocklistItemName} with a custom name for your list item. 
1. Replace {token} with the token you got from the "Get your token" step above. 
1. Replace the value of the `"pattern"` field with the item you'd like to add to your blocklist. The maximum length of a blockItem is 1,000 characters. Also specify whether the pattern is regex or exact match. 

```bash
curl --location --request PUT 'https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CognitiveServices/accounts/{accountName}/raiBlocklists/{raiBlocklistName}/raiBlocklistItems/{raiBlocklistItemName}?api-version=2024-04-01-preview' \ 
--header 'Authorization: Bearer {token}' \ 
--header 'Content-Type: application/json' \ 
--data-raw '{  
    "properties": {  
        "pattern": "blocking pattern",  
        "isRegex": false  
    }  
}' 
```

> [!NOTE]
> It can take around 5 minutes for a new term to be added to the blocklist. Test the blocklist after 5 minutes. 

The response code should be `200`. 

```json
{ 
  "name": "raiBlocklistItemName", 
  "id": "/subscriptions/subscriptionId/resourceGroups/resourceGroupName/providers/Microsoft.CognitiveServices/accounts/accountName/raiBlocklists/raiBlocklistName/raiBlocklistItems/raiBlocklistItemName", 
  "properties": { 
    "pattern": "blocking pattern", 
    "isRegex": false 
  } 
} 
```

### Analyze text with a blocklist

Now you can test out your deployment that has the blocklist. For instructions on calling the Azure OpenAI endpoints, visit the [Quickstart](/azure/ai-foundry/openai/quickstart). 

In the below example, a GPT-35-Turbo deployment with a blocklist is blocking the prompt. The response returns a `400` error. 

```json
{
  "error": {
    "message": "The response was filtered due to the prompt triggering Azure OpenAI's content management policy. Please modify your prompt and retry. To learn more about our content filtering policies please read our documentation: https://go.microsoft.com/fwlink/?linkid=2198766",
    "type": null,
    "param": "prompt",
    "code": "content_filter",
    "status": 400,
    "innererror": {
      "code": "ResponsibleAIPolicyViolation",
      "content_filter_result": {
        "custom_blocklists": {
          "details": [{ "filtered": true, "id": "pizza" }],
          "filtered": true
        }
      }
    }
  }
}
```

If the completion itself is blocked, the response returns `200`, as the completion only cuts off when the blocklist content is matched. The annotations show that a blocklist item was matched. 

```json
{ 
    "id": "chatcmpl-85NkyY0AkeBMunOjyxivQSiTaxGAl", 
    "object": "chat.completion", 
    "created": 1696293652, 
    "model": "gpt-35-turbo", 
    "prompt_filter_results": [ 
        { 
            "prompt_index": 0, 
            "content_filter_results": { 
                "hate": { 
                    "filtered": false, 
                    "severity": "safe" 
                }, 
                "self_harm": { 
                    "filtered": false, 
                    "severity": "safe" 
                }, 
                "sexual": { 
                    "filtered": false, 
                    "severity": "safe" 
                }, 
                "violence": { 
                    "filtered": false, 
                    "severity": "safe" 
                } 
            } 
        } 
    ], 
    "choices": [ 
        { 
            "index": 0, 
            "finish_reason": "content_filter", 
            "message": { 
                "role": "assistant" 
            }, 
            "content_filter_results": { 
                "custom_blocklists": [ 
                    { 
                        "filtered": true, 
                        "id": "myBlocklistName" 
                    } 
                ], 
                "hate": { 
                    "filtered": false, 
                    "severity": "safe" 
                }, 
                "self_harm": { 
                    "filtered": false, 
                    "severity": "safe" 
                }, 
                "sexual": { 
                    "filtered": false, 
                    "severity": "safe" 
                }, 
                "violence": { 
                    "filtered": false, 
                    "severity": "safe" 
                } 
            } 
        } 
    ], 
    "usage": { 
        "completion_tokens": 75, 
        "prompt_tokens": 27, 
        "total_tokens": 102 
    } 
} 
```

**Key fields in the response:**

- `finish_reason: "content_filter"` indicates the completion was stopped by a blocklist match
- `custom_blocklists[].id` shows which blocklist triggered the filter
- `custom_blocklists[].filtered: true` confirms the content was blocked

### Delete a blocklist item

To delete a blocklist item, use the following cURL command:

1. Replace {subscriptionId} with your subscription ID.
1. Replace {resourceGroupName} with your resource group name.
1. Replace {accountName} with your resource name.
1. Replace {raiBlocklistName} with the name of your blocklist.
1. Replace {raiBlocklistItemName} with the name of the item to delete.
1. Replace {token} with the token you got from the "Get your token" step above.

```bash
curl --location --request DELETE 'https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CognitiveServices/accounts/{accountName}/raiBlocklists/{raiBlocklistName}/raiBlocklistItems/{raiBlocklistItemName}?api-version=2024-10-01' \
--header 'Authorization: Bearer {token}'
```

The response code should be `200` (item deleted) or `204` (no content).

### Delete a blocklist

To delete an entire blocklist, use the following cURL command:

1. Replace {subscriptionId} with your subscription ID.
1. Replace {resourceGroupName} with your resource group name.
1. Replace {accountName} with your resource name.
1. Replace {raiBlocklistName} with the name of the blocklist to delete.
1. Replace {token} with the token you got from the "Get your token" step above.

```bash
curl --location --request DELETE 'https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CognitiveServices/accounts/{accountName}/raiBlocklists/{raiBlocklistName}?api-version=2024-10-01' \
--header 'Authorization: Bearer {token}'
```

> [!WARNING]
> Deleting a blocklist removes all items in that list and cannot be undone.


#### [Foundry](#tab/foundry)

[!INCLUDE [use-blocklists](../../../ai-foundry/includes/use-blocklists.md)]

---

## Troubleshooting

### 403 Forbidden error

Ensure your Azure AD token has the correct permissions. The account must have **Cognitive Services Contributor** or **Owner** role on the Azure OpenAI resource.

### Blocklist not taking effect

New blocklist terms can take up to 5 minutes to propagate. Wait and test again. If the issue persists, verify the blocklist is correctly applied to your content filter.

### Pattern not matching expected content

If using regex patterns, ensure the pattern syntax is valid. Test your regex pattern separately before adding it to the blocklist. Common issues include:

- Unescaped special characters
- Case sensitivity (patterns are case-sensitive by default)
- Anchors (`^` and `$`) might not behave as expected in streaming scenarios

### Quota limit reached

Each blocklist can contain a maximum of 10,000 terms. If you need more, create more blocklists and apply them to the same content filter.

## Related content

- Learn more about Responsible AI practices for Azure OpenAI: [Overview of Responsible AI practices for Azure OpenAI models](/azure/ai-foundry/responsible-ai/openai/overview). 

- Read more about [content filtering categories and severity levels](/azure/ai-foundry/openai/concepts/content-filter?tabs=python) with Azure OpenAI in Foundry models. 

- Learn more about red teaming from our: [Introduction to red teaming large language models (LLMs)](/azure/ai-foundry/openai/concepts/red-teaming) article. 
