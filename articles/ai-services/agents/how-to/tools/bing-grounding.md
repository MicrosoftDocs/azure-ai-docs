---
title: 'How to use Grounding with Bing Search in Azure AI Foundry Agent Service'
titleSuffix: Azure AI Foundry
description: Learn how to ground Azure AI Agents using Bing Search results.
services: cognitive-services
manager: nitinme
ms.service: azure-ai-agent-service
ms.topic: how-to
ms.date: 02/18/2025
author: aahill
ms.author: aahi
ms.custom: azure-ai-agents
---

# Grounding with Bing Search 

**Grounding with Bing Search** allows your Azure AI Agents to incorporate real-time public web data when generating responses. You need to create a Grounding with Bing Search resource, and then connect this resource to your Azure AI Agents. When a user sends a query, Azure AI Agents decide if Grounding with Bing Search should be leveraged or not. If so, it will leverage Bing to search over public web data and return relevant chunks. Lastly, Azure AI Agents will use returned chunks to generate a response.  

You can ask questions such as "*what is the top news today*" or "*what is the recent update in the retail industry in the US?*", which require real-time public data.

Developers and end users don't have access to raw content returned from Grounding with Bing Search. The model response, however, includes citations with links to the websites used to generate the response, and a link to the Bing query used for the search. You can retrieve the **model response** by accessing the data in the thread that was created. These two *references* must be retained and displayed in the exact form provided by Microsoft, as per Grounding with Bing Search's [Use and Display Requirements](https://www.microsoft.com/en-us/bing/apis/grounding-legal#use-and-display-requirements). See the [how to display Grounding with Bing Search results](#how-to-display-grounding-with-bing-search-results) section for details.

>[!IMPORTANT]
> 1. Your usage of Grounding with Bing Search can incur costs. See the [pricing page](https://www.microsoft.com/bing/apis/grounding-pricing) for details.
> 1. By creating and using a Grounding with Bing Search resource through code-first experience, such as Azure CLI, or deploying through deployment template, you agree to be bound by and comply with the terms available at https://www.microsoft.com/en-us/bing/apis/grounding-legal, which may be updated from time to time.
> 1. When you use Grounding with Bing Search, your customer data is transferred outside of the Azure compliance boundary to the Grounding with Bing Search service. Grounding with Bing Search is not subject to the same data processing terms (including location of processing) and does not have the same compliance standards and certifications as the Azure AI Foundry Agent Service, as described in the [Grounding with Bing Search Terms of Use](https://www.microsoft.com/en-us/bing/apis/grounding-legal). It is your responsibility to assess whether use of Grounding with Bing Search in your agent meets your needs and requirements.

## How Grounding with Bing Search works

The user query is the message that an end user sends to an agent, such as *"should I take an umbrella with me today? I'm in Seattle."* Instructions are the system message a developer can provide to share context and provide instructions to the AI model on how to use various tools or behave. 

When a user sends a query, the customer's AI model deployment first processes it (using the provided instructions) to later perform a Bing search query (which is [visible to developers](#how-to-display-grounding-with-bing-search-results)). 
Grounding with Bing returns relevant search results to the customer's model deployment, which then generates the final output. 

> [!NOTE]
> When using Grounding with Bing Search, only the Bing search query and your resource key are sent to Bing, and no end user-specific information is included. Your resource key is sent to Bing solely for billing and rate limiting purposes. 

The authorization will happen between Grounding with Bing Search service and Azure AI Foundry Agent Service. Any Bing search query that is generated and sent to Bing for the purposes of grounding is transferred, along with the resource key, outside of the Azure compliance boundary to the Grounding with Bing Search service. Grounding with Bing Search is subject to Bing's terms and do not have the same compliance standards and certifications as the Azure AI Foundry Agent Service, as described in the [Grounding with Bing Search Terms of Use](https://www.microsoft.com/bing/apis/grounding-legal). It is your responsibility to assess whether the use of Grounding with Bing Search in your agent meets your needs and requirements.

## Usage support

|Azure AI foundry support  | Python SDK |	C# SDK | JavaScript SDK | REST API |Basic agent setup | Standard agent setup |
|---------|---------|---------|---------|---------|---------|---------|
| ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |

## Setup  

> [!NOTE]
> 1. Grounding with Bing Search works with [all Azure OpenAI models](../../concepts/model-region-support.md) that Azure AI Foundry Agent Service supports, except `gpt-4o-mini, 2024-07-18`. 

1. Create an Azure AI Agent by following the steps in the [quickstart](../../quickstart.md).

1. Create a Grounding with Bing Search resource. You need to have `owner` or `contributor` role in your subscription or resource group to create it.

   1. You can create one in the [Azure portal](https://portal.azure.com/#create/Microsoft.BingGroundingSearch), and select the different fields in the creation form. Make sure you create this Grounding with Bing Search resource in the same resource group as your Azure AI Agent, AI Project, and other resources.

    :::image type="content" source="../../media/tools/bing/resource-selection.png" alt-text="A screenshot of the Bing resource selection in the Azure portal." lightbox="../../media/tools/bing/resource-selection.png":::
  
   1. You can also create one through code-first experience. If so, you need to manually [register](/azure/azure-resource-manager/management/resource-providers-and-types#register-resource-provider) Bing Search as an Azure resource provider. You must have permission to perform the `/register/action` operation for the resource provider. The permission is included in the **Contributor** and **Owner** roles.

   ```console
       az provider register --namespace 'Microsoft.Bing'
   ```

1. After you have created a Grounding with Bing Search resource, you can find it in [Azure portal](https://portal.azure.com/#home). Navigate to the resource group you've created the resource in, search for the Grounding with Bing Search resource you have created.

    :::image type="content" source="../../media/tools/bing/resource-azure-portal.png" alt-text="A screenshot of the Bing resource in the Azure portal." lightbox="../../media/tools/bing/resource-azure-portal.png":::



## How to display Grounding with Bing Search results

According to Grounding with Bing's [terms of use and use and display requirements](https://www.microsoft.com/en-us/bing/apis/grounding-legal#use-and-display-requirements), you need to display both website URLs and Bing search query URLs in your custom interface. You can find website URLs through `annotations` parameter in API response and Bing search query URLs through `runstep` details. To render the webpage, we recommend you replace the endpoint of Bing search query URLs with `www.bing.com` and your Bing search query URL would look like "https://www.bing.com/search?q={search query}"

```python
run_steps = project_client.agents.list_run_steps(run_id=run.id, thread_id=thread.id)
run_steps_data = run_steps['data']
print(f"Last run step detail: {run_steps_data}")
```

:::image type="content" source="../../media/tools/bing/website-citations.png" alt-text="A screenshot showing citations for Bing search results." lightbox="../../media/tools/bing/website-citations.png":::


## Next steps

See [code samples](./bing-code-samples.md) for using the Grounding with Bing tool programatically.
