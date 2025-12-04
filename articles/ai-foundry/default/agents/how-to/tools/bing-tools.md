---
title: 'Grounding with Bing Search overview for the agents API'
titleSuffix: Microsoft Foundry
description: Learn about the options available to let agents search the web using standard and custom Bing Search grounding tools.
services: cognitive-services
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: article
ms.date: 12/04/2025
author: alvinashcraft
ms.author: aashcraft
ai-usage: ai-assisted
zone_pivot_groups: selection-bing-grounding-new
---

# Grounding with Bing Search tools for agents

Traditional language models operate with a knowledge cutoff. A fixed point in time beyond which they can't access new information. Grounding with Bing Search and Grounding with Bing Custom Search (preview) allows your agents to incorporate real-time public web data when generating responses, letting you ask questions such as "what is the top AI news today".

The grounding process involves several key steps:

1. **Query formulation**: The agent identifies information gaps and constructs search queries
2. **Search execution**: The grounding tool submits queries to search engines and retrieves results
3. **Information synthesis**: The agent processes search results and integrates findings into responses
4. **Source attribution**: The agent provides transparency by citing search sources

>[!IMPORTANT]
> * Grounding with Bing Search and/or Grounding with Bing Custom Search is a [First Party Consumption Service](https://www.microsoft.com/licensing/terms/product/Glossary/EAEAS#:~:text=First-Party%20Consumption%20Services) with [terms for online services](https://www.microsoft.com/licensing/terms/product/ForOnlineServices/EAEAS), governed by the [Grounding with Bing terms of use](https://www.microsoft.com/bing/apis/grounding-legal-enterprise) and the [Microsoft Privacy Statement](https://go.microsoft.com/fwlink/?LinkId=521839&clcid=0x409). 
> * The Microsoft [Data Protection Addendum](https://aka.ms/dpa) doesn't apply to data sent to Grounding with Bing Search and/or Grounding with Bing Custom Search. When Customer uses Grounding with Bing Search and/or Grounding with Bing Custom Search, Customer Data will flow outside the Azure compliance and Geo boundary. This also means use of Grounding with Bing Search and/or Grounding with Bing Custom Search waives all elevated Government Community Cloud security and compliance commitments, to include data sovereignty and screened/citizenship-based support, as applicable.  
> * Use of Grounding with Bing Search and Grounding with Bing Custom Search will incur costs. See pricing for [details](https://www.microsoft.com/en-us/bing/apis/grounding-pricing). 
> * See the [manage section](#manage-grounding-with-bing-search-and-grounding-with-bing-custom-search) for information about how Azure admins can manage access to use of Grounding with Bing Search and/or Grounding with Bing Custom Search.

## Available tools

|Tool  |Description  |Use-case  |
|---------|---------|---------|
|Grounding with Bing Search     | Gives agents standard access to Bing's search capabilities.        | Scenarios requiring broad knowledge access.        |
|Grounding with Bing Custom Search (preview)  | Allows agents to search within a configurable set of public web domains. You define the parts of the web you want to draw from so users only see relevant results from the domains and subdomains of your choosing.        | Scenarios requiring information management.        |

> [!NOTE]
> See [best practices](../../concepts/tool-best-practice.md) for information on optimizing tool usage.

## Code examples

:::zone pivot="python"
> [!NOTE]
> - You'll need the latest prerelease package. See the [quickstart](../../../../quickstarts/get-started-code.md?view=foundry&preserve-view=true#install-and-authenticate) for details.
> - Your connection ID should be in the format of `/subscriptions/{{subscriptionID}}/resourceGroups/{{resourceGroupName}}/providers/Microsoft.CognitiveServices/accounts/{{foundryAccountName}}/projects/{{foundryProjectName}}/connections/{{foundryConnectionName}}`

# [Grounding with Bing Search](#tab/grounding-with-bing)

```python
import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    PromptAgentDefinition,
    BingGroundingAgentTool,
    BingGroundingSearchToolParameters,
    BingGroundingSearchConfiguration,
)

load_dotenv()

project_client = AIProjectClient(
    endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)

openai_client = project_client.get_openai_client()

with project_client:
    agent = project_client.agents.create_version(
        agent_name="MyAgent",
        definition=PromptAgentDefinition(
            model=os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
            instructions="You are a helpful assistant.",
            tools=[
                BingGroundingAgentTool(
                    bing_grounding=BingGroundingSearchToolParameters(
                        search_configurations=[
                            BingGroundingSearchConfiguration(
                                project_connection_id=os.environ["BING_PROJECT_CONNECTION_ID"]
                            )
                        ]
                    )
                )
            ],
        ),
        description="You are a helpful agent.",
    )
    print(f"Agent created (id: {agent.id}, name: {agent.name}, version: {agent.version})")

    stream_response = openai_client.responses.create(
        stream=True,
        tool_choice="required",
        input="What is today's date and whether in Seattle?",
        extra_body={"agent": {"name": agent.name, "type": "agent_reference"}},
    )

    for event in stream_response:
        if event.type == "response.created":
            print(f"Follow-up response created with ID: {event.response.id}")
        elif event.type == "response.output_text.delta":
            print(f"Delta: {event.delta}")
        elif event.type == "response.text.done":
            print(f"\nFollow-up response done!")
        elif event.type == "response.output_item.done":
            if event.item.type == "message":
                item = event.item
                if item.content[-1].type == "output_text":
                    text_content = item.content[-1]
                    for annotation in text_content.annotations:
                        if annotation.type == "url_citation":
                            print(f"URL Citation: {annotation.url}")
        elif event.type == "response.completed":
            print(f"\nFollow-up completed!")
            print(f"Full response: {event.response.output_text}")
```

# [Grounding with Bing Custom Search (preview)](#tab/grounding-with-bing-custom)

```python
import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    PromptAgentDefinition,
    BingCustomSearchAgentTool,
    BingCustomSearchToolParameters,
    BingCustomSearchConfiguration,
)

load_dotenv()

project_client = AIProjectClient(
    endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)

# Get the OpenAI client for responses and conversations
openai_client = project_client.get_openai_client()

bing_custom_search_tool = BingCustomSearchAgentTool(
    bing_custom_search_preview=BingCustomSearchToolParameters(
        search_configurations=[
            BingCustomSearchConfiguration(
                project_connection_id=os.environ["BING_CUSTOM_SEARCH_PROJECT_CONNECTION_ID"],
                instance_name=os.environ["BING_CUSTOM_SEARCH_INSTANCE_NAME"],
            )
        ]
    )
)

with project_client:
    agent = project_client.agents.create_version(
        agent_name="MyAgent",
        definition=PromptAgentDefinition(
            model=os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
            instructions="""You are a helpful agent that can use Bing Custom Search tools to assist users. 
            Use the available Bing Custom Search tools to answer questions and perform tasks.""",
            tools=[bing_custom_search_tool],
        ),
    )
    print(f"Agent created (id: {agent.id}, name: {agent.name}, version: {agent.version})")

    user_input = input(
        "Enter your question for the Bing Custom Search agent " "(e.g., 'Tell me more about foundry agent service'): \n"
    )

    # Send initial request that will trigger the Bing Custom Search tool
    stream_response = openai_client.responses.create(
        stream=True,
        input=user_input,
        extra_body={"agent": {"name": agent.name, "type": "agent_reference"}},
    )

    for event in stream_response:
        if event.type == "response.created":
            print(f"Follow-up response created with ID: {event.response.id}")
        elif event.type == "response.output_text.delta":
            print(f"Delta: {event.delta}")
        elif event.type == "response.text.done":
            print(f"\nFollow-up response done!")
        elif event.type == "response.output_item.done":
            if event.item.type == "message":
                item = event.item
                if item.content[-1].type == "output_text":
                    text_content = item.content[-1]
                    for annotation in text_content.annotations:
                        if annotation.type == "url_citation":
                            print(
                                f"URL Citation: {annotation.url}, "
                                f"Start index: {annotation.start_index}, "
                                f"End index: {annotation.end_index}"
                            )
        elif event.type == "response.completed":
            print(f"\nFollow-up completed!")
            print(f"Full response: {event.response.output_text}")
```

---
:::zone-end

:::zone pivot="csharp"

For C# usage, see the [Sample for use of Agents with Bing grounding](https://github.com/Azure/azure-sdk-for-net/blob/feature/ai-foundry/agents-v2/sdk/ai/Azure.AI.Projects.OpenAI/samples/Sample16_Bing_Grounding.md) and [Sample for use of Agents with Bing grounding in streaming scenarios](https://github.com/Azure/azure-sdk-for-net/blob/feature/ai-foundry/agents-v2/sdk/ai/Azure.AI.Projects.OpenAI/samples/Sample17_Bing_Grounding_Streaming.md) Azure.AI.Projects.OpenAI project examples in the Azure SDK for .NET repository on GitHub.

:::zone-end

## How it works

The user query is the message that an end user sends to an agent, such as *"should I take an umbrella with me today? I'm in Seattle."* Instructions are the system message a developer can provide to share context and provide instructions to the AI model on how to use various tools or behave. 

When a user sends a query, the customer's AI model deployment first processes it (using the provided instructions) to later perform a Bing search query (which is [visible to developers](#how-to-display-search-results)). 
Grounding with Bing returns relevant search results to the customer's model deployment, which then generates the final output. 

> [!NOTE]
> When using Grounding with Bing Search or Grounding with Bing Custom Search, only the Bing search query, tool parameters, and your resource key are sent to Bing, and no end user-specific information is included. Your resource key is sent to Bing solely for billing and rate limiting purposes. 

The authorization will happen between the Grounding with Bing Search or Grounding with Bing Custom Search service and Foundry Agent Service. Any Bing search query that is generated and sent to Bing for the purposes of grounding is transferred, along with the resource key, outside of the Azure compliance boundary to the Grounding with Bing Search service. Grounding with Bing Search is subject to Bing's terms and don't have the same compliance standards and certifications as the Agent Service, as described in the [Terms of Use](https://www.microsoft.com/en-us/bing/apis/grounding-legal-enterprise). It's your responsibility to assess whether the use of Grounding with Bing Search or Grounding with Bing Custom Search in your agent meets your needs and requirements.

Transactions with your Grounding with Bing resource are counted by the number of tool calls per run. You can see how many tool calls are made from the run step.

Developers and end users don't have access to raw content returned from Grounding with Bing Search. The model response, however, includes citations with links to the websites used to generate the response, and a link to the Bing query used for the search. You can retrieve the **model response** by accessing the data in the conversation that was created. These two *references* must be retained and displayed in the exact form provided by Microsoft, as per Grounding with Bing Search's [Use and Display Requirements](https://www.microsoft.com/en-us/bing/apis/grounding-legal-enterprise#use-and-display-requirements). See the [how to display Grounding with Bing Search results](#how-to-display-search-results) section for details.

## How to display search results

According to Grounding with Bing's [terms of use and use and display requirements](https://www.microsoft.com/en-us/bing/apis/grounding-legal-enterprise#use-and-display-requirements#use-and-display-requirements), you need to display both website URLs and Bing search query URLs in your custom interface. You can find this information in the API response, in the `arguments` parameter. To render the webpage, we recommend you replace the endpoint of Bing search query URLs with `www.bing.com` and your Bing search query URL would look like `https://www.bing.com/search?q={search query}`.

:::image type="content" source="../../../../agents/media/tools/bing/website-citations.png" alt-text="A screenshot showing citations for Bing search results." lightbox="../../../../agents/media/tools/bing/website-citations.png":::

## Grounding with Bing Custom Search configuration

Grounding with Bing Custom Search is a powerful tool that allows you to select a subspace of the web to limit your Agent’s grounding knowledge. Here you can find a few tips for how to take the maximum advantage of this capability: 

- If you own a public site that you want to include in the search but Bing hasn’t indexed, see the [Bing webmaster documentation](https://www.bing.com/webmaster/help/webmaster-guidelines-30fba23a) for details about getting your site indexed. The webmaster documentation also provides details about getting Bing to crawl your site if the index is out of date. 
- You'll need at least the contributor role for the Bing Custom Search resource to create a configuration.
- You can only block certain domains and perform a search against the rest of the Web (a competitor's site, for example). 
- Grounding with Bing Custom Search only returns results for domains and webpages that are public and have been indexed by Bing. 
  - Domain (for example, `https://www.microsoft.com`) 
  - Domain and path (for example, `https://www.microsoft.com/surface`) 
  - Webpage (for example, `https://www.microsoft.com/en-us/p/surface-earbuds/8r9cpq146064`) 

## Supported capabilities and known issues

- The Grounding with Bing Search tool is designed to retrieve real-time information from the web, NOT specific web domains. For retrieving information from specific domains, use the Grounding with Bing Custom Search tool.
- It's NOT Recommended to **summarize** an entire web page.
- Within one run, the AI model will evaluate the tool outputs and may decide to invoke the tool again for more information and context. The AI model may also decide which pieces of tool outputs are used to generate the response.
- Azure AI Agent service will return **AI model generated response** as output so end-to-end latency will be impacted pre-/post-processing of LLMs.
- The Grounding with Bing Search and Grounding with Bing Custom Search tools don't return the tool output to developers and end users.
- Grounding with Bing Search and Grounding with Bing Custom Search only works with agents that aren't using VPN or Private Endpoints. The agent must have normal network access.

## Manage Grounding with Bing Search and Grounding with Bing Custom Search

Admins can leverage RBAC role assignments for enabling or disabling use of using Grounding with Bing and/or Grounding with Bing Custom Search within the subscription or resource group. 

1. The Admin needs to register `Microsoft.Bing` in the Azure Subscription. The Admin needs to have the permissions to do the `/register/action` operation for the resource provider. The permission is included in the Contributor and Owner roles. For more information about how to register, see the [Azure Resource Manager](/azure/azure-resource-manager/management/resource-providers-and-types) documentation.

1. Once the Admin has registered `Microsoft.Bing`, people with permissions can create/delete/retrieve the resource key for a Grounding with Bing and/or Grounding with Bing Custom Search resource. These people need to have the **Contributor** or **Owner** role at the subscription or resource group level. 

1. Once a Grounding with Bing and/or Grounding with Bing Custom Search resource is created, people with permissions can then create a Microsoft Foundry connection to connect to the resource and use it as a tool in Foundry Agent Service. These people need to have at least  the **Azure AI Project Manager** role. 

### Disable use of Grounding with Bing Search and Grounding with Bing Custom Search

1. The Admin needs to have "Owner" or "Contributor" role in your description.

1. The Admin can then delete all Grounding with Bing Search and/or Grounding with Bing Custom Search resources in the subscription.

1. The Admin should then unregister the `Microsoft.Bing` resource provider in your subscription (you can't unregister before deleting all resources).  See the [Azure Resource Manager documentation](/azure/azure-resource-manager/management/resource-providers-and-types) for more information about unregistering. 

1. Next, the Admin should create an Azure Policy to disallow creation of Grounding with Bing Search and/or Grounding with Bing Custom Search resources in their subscription, following the sample [here](https://github.com/azure-ai-foundry/foundry-samples/blob/main/samples/microsoft/infrastructure-setup/05-custom-policy-definitions/deny-disallowed-connections.json).
