---
title: Use an AI Search index with the agents API
titleSuffix: Microsoft Foundry
description: Learn how to use the Azure AI Search tool to connect agents to search indexes, retrieve indexed documents, and ground responses in your proprietary content.
services: azure-ai-agent-service
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: how-to
ms.date: 12/09/2025
author: alvinashcraft
ms.author: aashcraft
ms.custom: azure-ai-agents
zone_pivot_groups: selection-ai-search-tool
---

# Azure AI Search tool for agents 

> [!NOTE]
> - There are new ways to add knowledge to your agent. For the latest recommended approach, see [Connect a Foundry IQ knowledge base to Foundry Agent Service](./knowledge-retrieval.md).
> - See [best practices](../../concepts/tool-best-practice.md) for information on optimizing tool usage.

The [Azure AI Search](/azure/search/search-what-is-azure-search) tool in Microsoft Foundry Agent Service connects an agent to a new or existing search index. Use this tool to retrieve and summarize your indexed documents, grounding the agent's responses in your proprietary content.

## Prerequisites

+ The latest prerelease package. See the [quickstart](../../../../quickstarts/get-started-code.md?view=foundry&preserve-view=true#install-and-authenticate) for details.

+ An [Azure AI Search index configured for vector search](../../../../../search/search-get-started-portal-import-vectors.md). The index must include:

    + One or more `Edm.String` (text) fields attributed as searchable and retrievable.

    + One or more `Collection(Edm.Single)` (vector) fields attributed as searchable.

## Code example

> [!NOTE]
> - You need the latest prerelease package. See the [quickstart](../../../../quickstarts/get-started-code.md?view=foundry&preserve-view=true#install-and-authenticate) for details.
> - Your connection ID should be in the format of `/subscriptions/{{subscriptionID}}/resourceGroups/{{resourceGroupName}}/providers/Microsoft.CognitiveServices/accounts/{{foundryAccountName}}/projects/{{foundryProjectName}}/connections/{{foundryConnectionName}}`

:::zone pivot="python"
```python
import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    AzureAISearchAgentTool,
    PromptAgentDefinition,
    AzureAISearchToolResource,
    AISearchIndexResource,
    AzureAISearchQueryType,
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
            instructions="""You are a helpful assistant. You must always provide citations for
            answers using the tool and render them as: `[message_idx:search_idx†source]`.""",
            tools=[
                AzureAISearchAgentTool(
                    azure_ai_search=AzureAISearchToolResource(
                        indexes=[
                            AISearchIndexResource(
                                project_connection_id=os.environ["AI_SEARCH_PROJECT_CONNECTION_ID"],
                                index_name=os.environ["AI_SEARCH_INDEX_NAME"],
                                query_type=AzureAISearchQueryType.SIMPLE,
                            ),
                        ]
                    )
                )
            ],
        ),
        description="You are a helpful agent.",
    )
    print(f"Agent created (id: {agent.id}, name: {agent.name}, version: {agent.version})")

    user_input = input(
        """Enter your question for the AI Search agent available in the index
        (e.g., 'Tell me about the mental health services available from Premera'): \n"""
    )

    stream_response = openai_client.responses.create(
        stream=True,
        tool_choice="required",
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

    print("\nCleaning up...")
    project_client.agents.delete_version(agent_name=agent.name, agent_version=agent.version)
    print("Agent deleted")
```
:::zone-end

:::zone pivot="csharp"

The following sample code shows synchronous examples of how to use the Azure AI Search tool in [Azure.AI.Projects.OpenAI](https://github.com/Azure/azure-sdk-for-net/tree/feature/ai-foundry/agents-v2/sdk/ai/Azure.AI.Projects.OpenAI) to query an index. For asynchronous C# examples, see the [GitHub repo](https://github.com/Azure/azure-sdk-for-net/tree/feature/ai-foundry/agents-v2/sdk/ai/Azure.AI.Projects.OpenAI).

## Use agents with Azure AI Search tool

This example shows how to use the Azure AI Search tool with agents to query an index.

```csharp
// Read the environment variables to be used in the next steps.
var projectEndpoint = System.Environment.GetEnvironmentVariable("PROJECT_ENDPOINT");
var modelDeploymentName = System.Environment.GetEnvironmentVariable("MODEL_DEPLOYMENT_NAME");
var aiSearchConnectionName = System.Environment.GetEnvironmentVariable("AI_SEARCH_CONNECTION_NAME");
AIProjectClient projectClient = new(endpoint: new Uri(projectEndpoint), tokenProvider: new DefaultAzureCredential());

// Create an AzureAISearchToolIndex object that defines the index and the search parameters.
AzureAISearchToolIndex index = new()
{
    ProjectConnectionId = aiSearchConnectionName,
    IndexName = "sample_index",
    TopK = 5,
    Filter = "category eq 'sleeping bag'",
    QueryType = AzureAISearchQueryType.Simple
};

// Create the agent definition with the Azure AI Search tool.
PromptAgentDefinition agentDefinition = new(model: modelDeploymentName)
{
    Instructions = "You are a helpful assistant. You must always provide citations for answers using the tool and render them as: `\u3010message_idx:search_idx\u2020source\u3011`.",
    Tools = { new AzureAISearchAgentTool(new AzureAISearchToolOptions(indexes: [index])) }
};

// Create the agent version with the agent definition.
AgentVersion agentVersion = projectClient.Agents.CreateAgentVersion(
    agentName: "myAgent",
    options: new(agentDefinition));

// Create an OpenAIResponse object with the ProjectResponsesClient object.
ProjectResponsesClient responseClient = projectClient.OpenAI.GetProjectResponsesClientForAgent(agentVersion.Name);
OpenAIResponse response = responseClient.CreateResponse("What is the temperature rating of the cozynights sleeping bag?");

// In the search, an index containing "embedding", "token", "category", "title", and "url" fields is used.
// The last two fields are needed to get citation title and URL, which the agent retrieves.
// To get the reference, you need to parse the output items.
// You can do it in this GetFormattedAnnotation helper method.
private static string GetFormattedAnnotation(OpenAIResponse response)
{
    foreach (ResponseItem item in response.OutputItems)
    {
        if (item is MessageResponseItem messageItem)
        {
            foreach (ResponseContentPart content in messageItem.Content)
            {
                foreach (ResponseMessageAnnotation annotation in content.OutputTextAnnotations)
                {
                    if (annotation is UriCitationMessageAnnotation uriAnnotation)
                    {
                        return $" [{uriAnnotation.Title}]({uriAnnotation.Uri})";
                    }
                }
            }
        }
    }
    return "";
}

// Use the helper method to output the result.
Assert.That(response.Status, Is.EqualTo(ResponseStatus.Completed));
Console.WriteLine($"{response.GetOutputText()}{GetFormattedAnnotation(response)}");

// Finally, delete all the resources you created in this sample.
projectClient.Agents.DeleteAgentVersion(agentName: agentVersion.Name, agentVersion: agentVersion.Version);
```

## Use agents with Azure AI Search tool for streaming scenarios

This example shows how to use the Azure AI Search tool with agents to query an index in a streaming scenario.

```csharp
// Read the environment variables to be used in the next steps
var projectEndpoint = System.Environment.GetEnvironmentVariable("PROJECT_ENDPOINT");
var modelDeploymentName = System.Environment.GetEnvironmentVariable("MODEL_DEPLOYMENT_NAME");
var aiSearchConnectionName = System.Environment.GetEnvironmentVariable("AI_SEARCH_CONNECTION_NAME");
AIProjectClient projectClient = new(endpoint: new Uri(projectEndpoint), tokenProvider: new DefaultAzureCredential());

// Create an AzureAISearchToolIndex object that defines the index and the search parameters.
AzureAISearchToolIndex index = new()
{
    ProjectConnectionId = aiSearchConnectionName,
    IndexName = "sample_index",
    TopK = 5,
    Filter = "category eq 'sleeping bag'",
    QueryType = AzureAISearchQueryType.Simple
};

// Create the agent definition with the Azure AI Search tool.
PromptAgentDefinition agentDefinition = new(model: modelDeploymentName)
{
    Instructions = "You are a helpful assistant. You must always provide citations for answers using the tool and render them as: `\u3010message_idx:search_idx\u2020source\u3011`.",
    Tools = { new AzureAISearchAgentTool(new AzureAISearchToolOptions(indexes: [index])) }
};

// Create the agent version with the agent definition.
AgentVersion agentVersion = projectClient.Agents.CreateAgentVersion(
    agentName: "myAgent",
    options: new(agentDefinition));

// Use an index containing "embedding", "token", "category", "title", and "url" fields.
// The last two fields are needed to get citation title and URL, retrieved by the agent.
// To get the reference, parse the output items. Use this GetFormattedAnnotation helper method.
private static string GetFormattedAnnotation(ResponseItem item)
{
    if (item is MessageResponseItem messageItem)
    {
        foreach (ResponseContentPart content in messageItem.Content)
        {
            foreach (ResponseMessageAnnotation annotation in content.OutputTextAnnotations)
            {
                if (annotation is UriCitationMessageAnnotation uriAnnotation)
                {
                    return $" [{uriAnnotation.Title}]({uriAnnotation.Uri})";
                }
            }
        }
    }
    return "";
}

// Create an OpenAIResponse object with the ProjectResponsesClient object.
ProjectResponsesClient responseClient = projectClient.OpenAI.GetProjectResponsesClientForAgent(agentVersion.Name);

string annotation = "";
string text = "";

// Stream the response from the agent and parse the output items for citations.
foreach (StreamingResponseUpdate streamResponse in responseClient.CreateResponseStreaming("What is the temperature rating of the cozynights sleeping bag?"))
{
    if (streamResponse is StreamingResponseCreatedUpdate createUpdate)
    {
        Console.WriteLine($"Stream response created with ID: {createUpdate.Response.Id}");
    }
    else if (streamResponse is StreamingResponseOutputTextDeltaUpdate textDelta)
    {
        Console.WriteLine($"Delta: {textDelta.Delta}");
    }
    else if (streamResponse is StreamingResponseOutputTextDoneUpdate textDoneUpdate)
    {
        text = textDoneUpdate.Text;
    }
    else if (streamResponse is StreamingResponseOutputItemDoneUpdate itemDoneUpdate)
    {
        if (annotation.Length == 0)
        {
            annotation = GetFormattedAnnotation(itemDoneUpdate.Item);
        }
    }
    else if (streamResponse is StreamingResponseErrorUpdate errorUpdate)
    {
        throw new InvalidOperationException($"The stream has failed: {errorUpdate.Message}");
    }
}
Console.WriteLine($"{text}{annotation}");

// Finally, delete all the resources that were created in this sample.
projectClient.Agents.DeleteAgentVersion(agentName: agentVersion.Name, agentVersion: agentVersion.Version);
```
    
:::zone-end

:::zone pivot="rest"

The following example shows how to use the Azure AI Search tool with the REST API to query an index. The example uses cURL, but you can use any HTTP client.

```bash
curl --request POST \
  --url "$AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/openai/responses?api-version=$API_VERSION" \
  --H "Authorization: Bearer $AGENT_TOKEN" \
  --H "Content-Type: application/json" \
  --d '{
"model": "{{model}}",
"input": "Tell me about the mental health services available from Premera",
"tools": [
  {
   "type": "azure_ai_search",
   "azure_ai_search": {
        "indexes": [
              {
                  "project_connection_id": "/subscriptions/${SUBSCRIPTION_ID}/resourceGroups/${RESOURCE_GROUP}/providers/Microsoft.MachineLearningServices/workspaces/${PROJECT_NAME}/connections/${AI_SEARCH_PROJECT_CONNECTION_ID}",
                  "index_name": "${AI_SEARCH_INDEX_NAME}",
                  "query_type": "semantic",
                  "top_k": 5,
                  "filter": ""                                    
              }
          ]
        }
}
]
}'
```
:::zone-end

## Limitations

+ To use the Azure AI Search tool in the Microsoft Foundry portal behind a virtual network, you must create an agent by using the SDK or REST API. After you create the agent programmatically, you can use it in the portal. 

+ The Azure AI Search tool can only target one index.
  
+ A Microsoft Foundry resource with basic agent deployments doesn't support private Azure AI Search resources, nor Azure AI Search with public network access disabled and a private endpoint. To use a private Azure AI Search tool with your agents, deploy the standard agent with virtual network injection.

+ Your Azure AI Search resource and Microsoft Foundry Agent need to be in the same tenant.

## Setup

In this section, you create a connection between the Microsoft Foundry project that contains your agent and the Azure AI Search service that contains your index.

If you already connected your project to your search service, skip this section. 

### Get search service connection details

The project connection requires the endpoint of your search service and either key-based authentication or keyless authentication with Microsoft Entra ID.

For keyless authentication, you must enable role-based access control (RBAC) and assign roles to your project's managed identity. Although this method involves extra steps, it enhances security by eliminating the need for hard-coded API keys.

Select the tab for your desired authentication method.

#### [Key-based authentication](#tab/keys)

1. Sign in to the [Azure portal](https://portal.azure.com/) and select your search service.
1. To get the endpoint:
    1. From the left pane, select **Overview**.
    1. Make a note of the URL, which should look like `https://my-service.search.windows.net`.

       :::image type="content" source="../../../../agents/media/tools/ai-search/connection-endpoint.png" alt-text="A screenshot of an AI Search resource Overview tab in the Azure portal." lightbox="../../../../agents/media/tools/ai-search/connection-endpoint.png":::

1. To get the API key:
    1. From the left pane, select **Settings** > **Keys**.
    1. Select **Both** to enable both key-based and keyless authentication, which is recommended for most scenarios.

       :::image type="content" source="../../../../agents/media/tools/ai-search\azure-portal.png" alt-text="A screenshot of an AI Search resource Keys tab in the Azure portal." lightbox="../../../../agents/media/tools/ai-search\azure-portal.png":::

    1. Make a note of one of the keys under **Manage admin keys**.

#### [Keyless authentication](#tab/keyless)

1. Sign in to the [Azure portal](https://portal.azure.com/) and select your search service.
1. To get the endpoint:
    1. From the left pane, select **Overview**.
    1. Make a note of the URL, which should look like `https://my-service.search.windows.net`.

       :::image type="content" source="../../../../agents/media/tools/ai-search/connection-endpoint.png" alt-text="A screenshot of an AI Search resource Overview tab in the Azure portal." lightbox="../../../../agents/media/tools/ai-search/connection-endpoint.png":::

1. To enable RBAC:
    1. From the left pane, select **Settings** > **Keys**.
    1. Select **Both** to enable both key-based and keyless authentication, which is recommended for most scenarios.

       :::image type="content" source="../../../../agents/media/tools/ai-search\azure-portal.png" alt-text="A screenshot of an AI Search resource Keys tab in the Azure portal." lightbox="../../../../agents/media/tools/ai-search\azure-portal.png":::

1. To assign the necessary roles:
    1. From the left pane, select **Access control (IAM)**.
    1. Select **Add** > **Add role assignment**.
    1. Assign the **Search Index Data Contributor** role to the managed identity of your project.
    1. Repeat the role assignment for **Search Service Contributor**.

---

### Create the project connection

Next, create the project connection by using the search service details you gathered. The connection name must be the name of your search index.

You can use the Microsoft Foundry portal, or one of the following options.

#### [Azure CLI](#tab/azurecli)

**Create the following connections.yml file:**

You can use a YAML configuration file for both key-based and keyless authentication. Replace the `name`, `endpoint`, and `api_key` (optional) placeholders with your search service details. For more information, see the [Azure AI Search connection YAML schema](../../../../../machine-learning/reference-yaml-connection-ai-search.md). 

Here's a key-based example:

```yml
name: my_project_acs_connection_keys
type: azure_ai_search
endpoint: https://contoso.search.windows.net/
api_key: XXXXXXXXXXXXXXX
```

Here's a keyless example:

```yml    
name: my_project_acs_connection_keyless
type: azure_ai_search
endpoint: https://contoso.search.windows.net/
```

**Then, run the following command:**

Replace `my_resource` with the resource group that contains your project and `my_project_name` with the name of your project.

```azurecli
az ml connection create --file {connection.yml} --resource-group {my_resource_group} --workspace-name {my_project_name}
```

#### [Python](#tab/pythonsdk)

Replace the `my_connection_name`, `my_endpoint`, and `my_key` (optional) placeholders with your search service details, and then run the following code:

```python
from azure.ai.ml.entities import AzureAISearchConnection

# Create an Azure AI Search project connection
my_connection_name = "my-connection-name"
my_endpoint = "my-endpoint" # This could also be called target
my_api_keys = None # Leave blank for Authentication type = AAD

my_connection = AzureAISearchConnection(name=my_connection_name,
                                    endpoint=my_endpoint, 
                                    api_key= my_api_keys)

# Create the connection
ml_client.connections.create_or_update(my_connection)
```

---
