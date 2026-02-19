---
title: Use Grounding with Bing Search tools with the agents API
titleSuffix: Microsoft Foundry
description: Learn how to use Grounding with Bing Search and Grounding with Bing Custom Search (preview) tools to ground agent responses with web data.
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

# Grounding agents with Bing Search tools

Traditional language models work with a knowledge cutoff. They can't access new information beyond a fixed point in time. By using Grounding with Bing Search and Grounding with Bing Custom Search (preview), your agents can incorporate real-time public web data when generating responses. By using these tools, you can ask questions such as "what is the top AI news today".

The grounding process involves several key steps:

1. **Query formulation**: The agent identifies information gaps and constructs search queries.
1. **Search execution**: The grounding tool submits queries to search engines and retrieves results.
1. **Information synthesis**: The agent processes search results and integrates findings into responses.
1. **Source attribution**: The agent provides transparency by citing search sources.

>[!IMPORTANT]
> - Grounding with Bing Search and Grounding with Bing Custom Search are [First Party Consumption Services](https://www.microsoft.com/licensing/terms/product/Glossary/EAEAS#:~:text=First-Party%20Consumption%20Services) with [terms for online services](https://www.microsoft.com/licensing/terms/product/ForOnlineServices/EAEAS). They're governed by the [Grounding with Bing terms of use](https://www.microsoft.com/bing/apis/grounding-legal-enterprise) and the [Microsoft Privacy Statement](https://go.microsoft.com/fwlink/?LinkId=521839&clcid=0x409). 
> - The Microsoft [Data Protection Addendum](https://aka.ms/dpa) doesn't apply to data sent to Grounding with Bing Search or Grounding with Bing Custom Search. When you use these services, your data flows outside the Azure compliance and Geo boundary. This also means use of these services waives all elevated Government Community Cloud security and compliance commitments, including data sovereignty and screened/citizenship-based support, as applicable.  
> - Use of Grounding with Bing Search and Grounding with Bing Custom Search incurs costs. See pricing for [details](https://www.microsoft.com/bing/apis/grounding-pricing). 
> - See the [manage section](#manage-grounding-with-bing-search-and-grounding-with-bing-custom-search) for information about how Azure admins can manage access to use of Grounding with Bing Search and Grounding with Bing Custom Search.

>[!NOTE]
> Start with the [web search tool (preview)](./web-search.md). Learn more about the differences between web search and Grounding with Bing Search (or Grounding with Bing Custom Search) in the [web grounding overview](./web-overview.md).

### Usage support

| Microsoft Foundry support | Python SDK | C# SDK | JavaScript SDK | Java SDK | REST API | Basic agent setup | Standard agent setup |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ✔️ | ✔️ | ✔️ | ✔️ | - | ✔️ | ✔️ | ✔️ |

Java SDK samples are not yet available.

## Prerequisites

Before you begin, make sure you have:

- An Azure subscription with the right permissions.
- Azure RBAC roles:
  - **Contributor** or **Owner** role at the subscription or resource group level to create Bing resources and get resource keys.
  - **Azure AI Project Manager** role to create project connections in Foundry. For more information, see [Role-based access control for Microsoft Foundry](../../../../concepts/rbac-foundry.md?view=foundry&preserve-view=true).
- A Foundry project created with a configured endpoint.
- An AI model deployed in your project.
- SDK installed for your preferred language:
  - Python: `azure-ai-projects` (latest prerelease version)
  - C#: `Azure.AI.Projects.OpenAI`
  - TypeScript/JavaScript: `@azure/ai-projects`
- Environment variables set up:
  - `AZURE_AI_PROJECT_ENDPOINT`: Your Foundry project endpoint URL.
  - `AZURE_AI_MODEL_DEPLOYMENT_NAME`: Your deployed model name.
  - For SDK samples:
    - `BING_PROJECT_CONNECTION_NAME`: Your Grounding with Bing Search project connection name.
    - `BING_CUSTOM_SEARCH_PROJECT_CONNECTION_NAME`: Your Grounding with Bing Custom Search project connection name.
  - For REST samples:
    - `BING_PROJECT_CONNECTION_ID`: Your Grounding with Bing Search project connection ID.
    - `BING_CUSTOM_SEARCH_PROJECT_CONNECTION_ID`: Your Grounding with Bing Custom Search project connection ID.
    - `API_VERSION`, `AGENT_TOKEN`.
  - For Bing Custom Search: `BING_CUSTOM_SEARCH_INSTANCE_NAME`: Your custom search instance name.
- A Bing Grounding or Bing Custom Search resource created and connected to your Foundry project. A paid subscription is required to create a Grounding with Bing Search or Grounding with Bing Custom Search resource.
- The Grounding with Bing Search tool works in a network-secured Foundry project, but it behaves like a public endpoint. Consider this behavior when you use the tool in a network-secured environment.

## Setup

In this section, you add a project connection for the Bing resource and capture the values used in the samples. SDK samples use the project connection name and resolve the connection ID at runtime. REST samples use the project connection ID. You can use this [bicep template](https://github.com/microsoft-foundry/foundry-samples/tree/main/infrastructure/infrastructure-setup-bicep/45-basic-agent-bing) to create a basic agent with Grounding with Bing Search tool enabled.

If you already have a project connection ID for the Bing resource you want to use, skip this section.

1. Add the appropriate connection to your project.

   For step-by-step instructions, see [Add a new connection to your project](../../../../how-to/connections-add.md?view=foundry&preserve-view=true).
   >[!IMPORTANT]
   > - You need the **Contributor** or **Owner** role at the subscription or resource group level to create Bing resources and get resource keys.
   > - To find the resource keys, go to your Grounding with Bing resource in the [Azure portal](https://portal.azure.com) > **Resource Management** > **Keys**.

1. Get the project connection name and ID from the connection details, then set the values as environment variables.

  - For SDK samples:
    - For Grounding with Bing Search: set `BING_PROJECT_CONNECTION_NAME`.
    - For Grounding with Bing Custom Search: set `BING_CUSTOM_SEARCH_PROJECT_CONNECTION_NAME`.
  - For REST samples:
    - For Grounding with Bing Search: set `BING_PROJECT_CONNECTION_ID`.
    - For Grounding with Bing Custom Search: set `BING_CUSTOM_SEARCH_PROJECT_CONNECTION_ID`.

  The project connection ID uses the format:

  `/subscriptions/{{subscriptionID}}/resourceGroups/{{resourceGroupName}}/providers/Microsoft.CognitiveServices/accounts/{{foundryAccountName}}/projects/{{foundryProjectName}}/connections/{{foundryConnectionName}}`

## Available tools

| Tool | Description | Use case |
| --- | --- | --- |
| Grounding with Bing Search | Gives agents standard access to Bing's search capabilities. | Scenarios requiring broad knowledge access. |
| Grounding with Bing Custom Search (preview) | Allows agents to search within a configurable set of public web domains. You define the parts of the web you want to draw from so users only see relevant results from domains you choose. | Scenarios requiring information management. |

> [!NOTE]
> See [best practices](../../concepts/tool-best-practice.md) for information on optimizing tool usage.

## Code examples

> [!NOTE]
> - You need the latest prerelease package. See the [quickstart](../../../../quickstarts/get-started-code.md?view=foundry&preserve-view=true#get-ready-to-code) for details.
> - For SDK samples, use the project connection name. For REST samples, use the project connection ID in the format `/subscriptions/{{subscriptionID}}/resourceGroups/{{resourceGroupName}}/providers/Microsoft.CognitiveServices/accounts/{{foundryAccountName}}/projects/{{foundryProjectName}}/connections/{{foundryConnectionName}}`.

:::zone pivot="python"

### Quick verification

Before running the full samples, verify your Bing connection exists:

```python
import os

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()

with (
    DefaultAzureCredential() as credential,
    AIProjectClient(endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"], credential=credential) as project_client,
):
    print("Connected to project.")
    
    # Verify Bing connection exists
    connection_name = os.environ.get("BING_PROJECT_CONNECTION_NAME")
    if connection_name:
        try:
            conn = project_client.connections.get(connection_name)
            print(f"Bing connection verified: {conn.name}")
            print(f"Connection ID: {conn.id}")
        except Exception as e:
            print(f"Bing connection '{connection_name}' not found: {e}")
    else:
        # List available connections to help find the right one
        print("BING_PROJECT_CONNECTION_NAME not set. Available connections:")
        for conn in project_client.connections.list():
            print(f"  - {conn.name}")
```

If this code runs without errors, your credentials and Bing connection are configured correctly.

### Full samples

The following examples demonstrate how to create an agent with Grounding with Bing Search tools, and how to use the agent to respond to user queries.

#### Grounding with Bing Search

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

with (
    DefaultAzureCredential() as credential,
    AIProjectClient(endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"], credential=credential) as project_client,
    project_client.get_openai_client() as openai_client,
):
    # Get connection ID from connection name
    bing_connection = project_client.connections.get(
        os.environ["BING_PROJECT_CONNECTION_NAME"],
    )
    print(f"Grounding with Bing Search connection ID: {bing_connection.id}")

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
                                project_connection_id=bing_connection.id
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
        input="What is today's date and weather in Seattle?",
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

### What this code does

This example creates an agent with grounding by using the Bing Search tool that can retrieve real-time information from the web. When you run the code:

1. It creates an `AIProjectClient` and authenticates by using your Azure credentials.
1. Creates an agent with the Bing grounding tool configured by using your Bing connection.
1. Sends a query asking about current date and weather in Seattle.
1. The agent uses the Bing grounding tool to search the web and streams the response.
1. Extracts and displays URL citations from the search results.

### Required inputs

- Environment variables: `AZURE_AI_PROJECT_ENDPOINT`, `AZURE_AI_MODEL_DEPLOYMENT_NAME`, `BING_PROJECT_CONNECTION_NAME`
- Azure credentials configured for `DefaultAzureCredential`

### Expected output

```console
Agent created (id: asst_abc123, name: MyAgent, version: 1)
Follow-up response created with ID: resp_xyz789
Delta: Today
Delta: 's date
Delta:  is December 12, 2025...
Follow-up response done!
URL Citation: https://www.weather.gov/seattle/
Follow-up completed!
Full response: Today's date is December 12, 2025, and the weather in Seattle is...
```

### Grounding with Bing Custom Search (preview)

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

with (
    DefaultAzureCredential() as credential,
    AIProjectClient(endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"], credential=credential) as project_client,
    project_client.get_openai_client() as openai_client,
):
    # Get connection ID from connection name
    bing_custom_connection = project_client.connections.get(
        os.environ["BING_CUSTOM_SEARCH_PROJECT_CONNECTION_NAME"],
    )
    print(f"Grounding with Bing Custom Search connection ID: {bing_custom_connection.id}")

        bing_custom_search_tool = BingCustomSearchAgentTool(
        bing_custom_search_preview=BingCustomSearchToolParameters(
            search_configurations=[
                BingCustomSearchConfiguration(
                    project_connection_id=bing_custom_connection.id,
                    instance_name=os.environ["BING_CUSTOM_SEARCH_INSTANCE_NAME"],
                )
            ]
        )
    )

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

**What this code does**

This example creates an agent with Grounding with Bing Custom Search tool that searches within a configurable set of public web domains. When you run the code:

1. It creates an `AIProjectClient` and authenticates by using your Azure credentials.
1. Creates an agent with the Bing Custom Search tool configured by using your custom search instance.
1. Prompts for user input asking about specific topics within your configured domains.
1. The agent uses the Bing Custom Search tool to search only your specified domains and streams the response.
1. Extracts and displays URL citations with start and end positions from the custom search results.

**Required inputs**

- Environment variables: `AZURE_AI_PROJECT_ENDPOINT`, `AZURE_AI_MODEL_DEPLOYMENT_NAME`, `BING_CUSTOM_SEARCH_PROJECT_CONNECTION_NAME`, `BING_CUSTOM_SEARCH_INSTANCE_NAME`
- Azure credentials configured for `DefaultAzureCredential`
- User input at runtime

**Expected output**

```console
Agent created (id: asst_abc123, name: MyAgent, version: 1)
Enter your question for the Bing Custom Search agent (e.g., 'Tell me more about foundry agent service'):
Tell me more about foundry agent service
Follow-up response created with ID: resp_xyz789
Delta: Microsoft
Delta:  Foundry
Delta:  Agent Service...
Follow-up response done!
URL Citation: https://learn.microsoft.com/azure/ai-foundry/agents, Start index: 45, End index: 120
Follow-up completed!
Full response: Microsoft Foundry Agent Service enables you to build...
```

:::zone-end

:::zone pivot="csharp"

### Quick verification

Before running the full samples, verify your Bing connection exists:

```csharp
using Azure.AI.Projects;
using Azure.Identity;

var projectEndpoint = System.Environment.GetEnvironmentVariable("AZURE_AI_PROJECT_ENDPOINT");
var bingConnectionName = System.Environment.GetEnvironmentVariable("BING_PROJECT_CONNECTION_NAME");

AIProjectClient projectClient = new(endpoint: new Uri(projectEndpoint), tokenProvider: new DefaultAzureCredential());

// Verify Bing connection exists
try
{
    AIProjectConnection conn = projectClient.Connections.GetConnection(connectionName: bingConnectionName);
    Console.WriteLine($"Bing connection verified: {conn.Name}");
    Console.WriteLine($"Connection ID: {conn.Id}");
}
catch (Exception ex)
{
    Console.WriteLine($"Bing connection '{bingConnectionName}' not found: {ex.Message}");
    // List available connections
    Console.WriteLine("Available connections:");
    foreach (var conn in projectClient.Connections.GetConnections())
    {
        Console.WriteLine($"  - {conn.Name}");
    }
}
```

If this code runs without errors, your credentials and Bing connection are configured correctly.

### Full samples

The following C# examples demonstrate how to create an agent with Grounding with Bing Search tool, and how to use the agent to respond to user queries. These examples use synchronous calls for simplicity. For asynchronous examples, see the [agent tools C# samples](https://github.com/Azure/azure-sdk-for-net/tree/feature/ai-foundry/agents-v2/sdk/ai/Azure.AI.Projects.OpenAI/samples).

To enable your Agent to use Bing search API, use `BingGroundingAgentTool`.

#### Grounding with Bing Search

```csharp
// Read the environment variables, which will be used in the next steps.
var projectEndpoint = System.Environment.GetEnvironmentVariable("AZURE_AI_PROJECT_ENDPOINT");
var modelDeploymentName = System.Environment.GetEnvironmentVariable("AZURE_AI_MODEL_DEPLOYMENT_NAME");
var bingConnectionName = System.Environment.GetEnvironmentVariable("BING_PROJECT_CONNECTION_NAME");

// Create an instance of AIProjectClient.
AIProjectClient projectClient = new(endpoint: new Uri(projectEndpoint), tokenProvider: new DefaultAzureCredential());

// Get connection ID from connection name
AIProjectConnection bingConnection = projectClient.Connections.GetConnection(connectionName: bingConnectionName);

// Create the agent version with Bing grounding tool
BingGroundingTool bingGroundingAgentTool = new(new BingGroundingSearchToolOptions(
  searchConfigurations: [new BingGroundingSearchConfiguration(projectConnectionId: bingConnection.Id)]
    )
);
PromptAgentDefinition agentDefinition = new(model: modelDeploymentName)
{
    Instructions = "You are a helpful agent.",
    Tools = { bingGroundingAgentTool, }
};
AgentVersion agentVersion = projectClient.Agents.CreateAgentVersion(
    agentName: "myAgent",
    options: new(agentDefinition));

// Output the agent version info
ProjectResponsesClient responseClient = projectClient.OpenAI.GetProjectResponsesClientForAgent(agentVersion.Name);

ResponseResult response = responseClient.CreateResponse("How does wikipedia explain Euler's Identity?");

// Extract and format URL citation annotations
string citation = "";
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
                    citation = $" [{uriAnnotation.Title}]({uriAnnotation.Uri})";
                }
            }
        }
    }
}

// Validate and print the response
Assert.That(response.Status, Is.EqualTo(ResponseStatus.Completed));
Console.WriteLine($"{response.GetOutputText()}{citation}");

// Clean up resources by deleting the agent version
projectClient.Agents.DeleteAgentVersion(agentName: agentVersion.Name, agentVersion: agentVersion.Version);
```

### What this code does

This example creates an agent that uses the Grounding with Bing Search tool and demonstrates synchronous response handling. When you run the code:

1. It creates an AIProjectClient by using your project endpoint.
1. Retrieves the Bing connection configuration from your project.
1. Creates an agent with the Bing grounding tool configured.
1. Sends a query asking how Wikipedia explains Euler's Identity.
1. The agent uses the Bing grounding tool to search and returns formatted results with URL citations.
1. Cleans up by deleting the agent version.

### Required inputs

- Environment variables: `AZURE_AI_PROJECT_ENDPOINT`, `AZURE_AI_MODEL_DEPLOYMENT_NAME`, `BING_PROJECT_CONNECTION_NAME`
- Azure credentials configured for `DefaultAzureCredential`

### Expected output

```console
Euler's identity is considered one of the most elegant equations in mathematics... [Euler's identity - Wikipedia](https://en.wikipedia.org/wiki/Euler%27s_identity)
```

## Grounding with Bing in streaming scenarios

```csharp
// Read the environment variables, which will be used in the next steps.
var projectEndpoint = System.Environment.GetEnvironmentVariable("AZURE_AI_PROJECT_ENDPOINT");
var modelDeploymentName = System.Environment.GetEnvironmentVariable("AZURE_AI_MODEL_DEPLOYMENT_NAME");
var bingConnectionName = System.Environment.GetEnvironmentVariable("BING_PROJECT_CONNECTION_NAME");

// Create an instance of AIProjectClient
AIProjectClient projectClient = new(endpoint: new Uri(projectEndpoint), tokenProvider: new DefaultAzureCredential());

// Get connection ID from connection name
AIProjectConnection bingConnection = projectClient.Connections.GetConnection(connectionName: bingConnectionName);

// Create the agent version with Bing grounding tool
BingGroundingTool bingGroundingAgentTool = new(new BingGroundingSearchToolOptions(
  searchConfigurations: [new BingGroundingSearchConfiguration(projectConnectionId: bingConnection.Id)]
    )
);
PromptAgentDefinition agentDefinition = new(model: modelDeploymentName)
{
    Instructions = "You are a helpful agent.",
    Tools = { bingGroundingAgentTool }
};
AgentVersion agentVersion = projectClient.Agents.CreateAgentVersion(
    agentName: "myAgent",
    options: new(agentDefinition));

// Stream the response from the agent version
ProjectResponsesClient responseClient = projectClient.OpenAI.GetProjectResponsesClientForAgent(agentVersion.Name);

string annotation = "";
string text = "";

// Parse the streaming response and output the results
foreach (StreamingResponseUpdate streamResponse in responseClient.CreateResponseStreaming("How does wikipedia explain Euler's Identity?"))
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
            // Extract and format URL citation annotations
            if (itemDoneUpdate.Item is MessageResponseItem messageItem)
            {
                foreach (ResponseContentPart content in messageItem.Content)
                {
                    foreach (ResponseMessageAnnotation messageAnnotation in content.OutputTextAnnotations)
                    {
                        if (messageAnnotation is UriCitationMessageAnnotation uriAnnotation)
                        {
                            annotation = $" [{uriAnnotation.Title}]({uriAnnotation.Uri})";
                        }
                    }
                }
            }
        }
    }
    else if (streamResponse is StreamingResponseErrorUpdate errorUpdate)
    {
        throw new InvalidOperationException($"The stream has failed: {errorUpdate.Message}");
    }
}
Console.WriteLine($"{text}{annotation}");

// Clean up resources by deleting the agent version
projectClient.Agents.DeleteAgentVersion(agentName: agentVersion.Name, agentVersion: agentVersion.Version);
```

### What this code does

This example creates an agent with grounding by using the Bing Search tool and demonstrates streaming response handling. When you run the code:

1. It creates an AIProjectClient by using your project endpoint.
1. Retrieves the Bing connection configuration from your project.
1. Creates an agent with the Bing grounding tool configured.
1. Sends a query asking how Wikipedia explains Euler's Identity.
1. The agent uses the Bing grounding tool and streams the response in real-time.
1. Processes streaming events including delta text updates and citation extraction.
1. Cleans up by deleting the agent version.

### Required inputs

- Environment variables: `AZURE_AI_PROJECT_ENDPOINT`, `AZURE_AI_MODEL_DEPLOYMENT_NAME`, `BING_PROJECT_CONNECTION_NAME`
- Azure credentials configured for `DefaultAzureCredential`

### Expected output

```console
Stream response created with ID: resp_xyz789
Delta: Euler
Delta: 's
Delta:  Identity
Delta:  is one of the most...
Euler's Identity is one of the most elegant equations in mathematics... [Euler's identity - Wikipedia](https://en.wikipedia.org/wiki/Euler%27s_identity)
```

:::zone-end

:::zone pivot="rest"
The following REST API examples demonstrate how to use Grounding with Bing Search and Grounding with Bing Custom Search (preview) tools to respond to user queries.

### Grounding with Bing Search

### Authentication setup

Before running REST API calls, configure authentication:

1. Set environment variables:
   - `AZURE_AI_PROJECT_ENDPOINT`: Your Foundry project endpoint URL.
   - `API_VERSION`: API version (for example, `2025-11-15-preview`).
   - `AZURE_AI_MODEL_DEPLOYMENT_NAME`: Your deployed model name.
   - `BING_PROJECT_CONNECTION_ID`: Your Grounding with Bing Search project connection ID.
  - `AGENT_TOKEN`: A bearer token for your user or service principal.
1. Obtain a bearer token:
   ```azurecli
   az account get-access-token --resource https://ai.azure.com --query accessToken -o tsv
   ```

  Save the output as the `AGENT_TOKEN` environment variable.

   ```bash
   curl --request POST \
     --url "$AZURE_AI_PROJECT_ENDPOINT/openai/responses?api-version=$API_VERSION" \
     -H "Authorization: Bearer $AGENT_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
     "model": "'$AZURE_AI_MODEL_DEPLOYMENT_NAME'",
     "input": "How does Wikipedia explain Euler\u0027s identity?",
     "tool_choice": "required",
     "tools": [
       {
         "type": "bing_grounding",
         "bing_grounding": {
           "search_configurations": [
             {
               "project_connection_id": "'$BING_PROJECT_CONNECTION_ID'",
               "count": 7,
               "market": "en-US",
               "set_lang": "en",
               "freshness": "7d"
             }
           ]
         }
       }
     ]
   }'
   ```

### What this code does

This REST API request creates a response using Grounding with Bing Search. The request:

1. Sends a POST request to the Foundry responses endpoint.
1. Includes the model deployment and user input in the request body.
1. Configures the Bing grounding tool with search parameters (count, market, language, freshness).
1. Returns a response with web search results and citations.

### Required inputs

- Environment variables: `AZURE_AI_PROJECT_ENDPOINT`, `API_VERSION`, `AGENT_TOKEN`, `AZURE_AI_MODEL_DEPLOYMENT_NAME`, `BING_PROJECT_CONNECTION_ID`.
- Valid bearer token with appropriate permissions.

### Expected output

JSON response with:
- `id`: Response identifier
- `output_text`: Generated text with grounded information
- `citations`: Array of URL citations used to generate the response

### Grounding with Bing Custom Search (preview)

```bash
curl --request POST \
  --url "$AZURE_AI_PROJECT_ENDPOINT/openai/responses?api-version=$API_VERSION" \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
  "model": "'$AZURE_AI_MODEL_DEPLOYMENT_NAME'",
  "input": "How does Wikipedia explain Euler\u0027s identity?",
  "tool_choice": "required",
  "tools": [
    {
      "type": "bing_custom_search_preview",
      "bing_custom_search_preview": {
        "search_configurations": [
          {
            "project_connection_id": "'$BING_CUSTOM_SEARCH_PROJECT_CONNECTION_ID'",
            "instance_name": "'$BING_CUSTOM_SEARCH_INSTANCE_NAME'",
            "count": 7,
            "market": "en-US",
            "set_lang": "en",
            "freshness": "7d"
          }
        ]
      }
    }
  ]
}'
```

### What this code does

This REST API request creates a response using Grounding with Bing Custom Search. The request:

1. Sends a POST request to the Foundry responses endpoint.
1. Includes the model deployment and user input in the request body.
1. Configures the Bing Custom Search tool with your instance name and search parameters.
1. Returns a response with custom search results limited to your configured domains.

### Required inputs

- Environment variables: `AZURE_AI_PROJECT_ENDPOINT`, `API_VERSION`, `AGENT_TOKEN`, `AZURE_AI_MODEL_DEPLOYMENT_NAME`, `BING_CUSTOM_SEARCH_PROJECT_CONNECTION_ID`, `BING_CUSTOM_SEARCH_INSTANCE_NAME`
- Valid bearer token with appropriate permissions.
- Bing Custom Search instance already configured with target domains

### Expected output

JSON response with:
- `id`: Response identifier
- `output_text`: Generated text with information from your custom domain set
- `citations`: Array of URL citations from your configured domains

:::zone-end

:::zone pivot="typescript"

### Quick verification

Before running the full samples, verify your Bing connection exists:

```typescript
import { DefaultAzureCredential } from "@azure/identity";
import { AIProjectClient } from "@azure/ai-projects";
import "dotenv/config";

const projectEndpoint = process.env["AZURE_AI_PROJECT_ENDPOINT"] || "<project endpoint>";
const bingConnectionName = process.env["BING_PROJECT_CONNECTION_NAME"] || "<bing connection name>";

async function verifyConnection(): Promise<void> {
  const project = new AIProjectClient(projectEndpoint, new DefaultAzureCredential());
  console.log("Connected to project.");

  try {
    const conn = await project.connections.get(bingConnectionName);
    console.log(`Bing connection verified: ${conn.name}`);
    console.log(`Connection ID: ${conn.id}`);
  } catch (error) {
    console.log(`Bing connection '${bingConnectionName}' not found: ${error}`);
    // List available connections
    console.log("Available connections:");
    for await (const conn of project.connections.list()) {
      console.log(`  - ${conn.name}`);
    }
  }
}

verifyConnection().catch(console.error);
```

If this code runs without errors, your credentials and Bing connection are configured correctly.

### Full samples

The following TypeScript examples demonstrate how to create an agent with Grounding with Bing Search and Grounding with Bing Custom Search (preview) tools, and how to use the agent to respond to user queries. For JavaScript examples, see the [agent tools JavaScript samples](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/ai/ai-projects/samples/v2-beta/javascript/agents/tools) in the Azure SDK for JavaScript repository on GitHub.

#### Grounding with Bing Search

```typescript
import { DefaultAzureCredential } from "@azure/identity";
import { AIProjectClient } from "@azure/ai-projects";
import "dotenv/config";

const projectEndpoint = process.env["AZURE_AI_PROJECT_ENDPOINT"] || "<project endpoint>";
const deploymentName =
  process.env["AZURE_AI_MODEL_DEPLOYMENT_NAME"] || "<model deployment name>";
const bingConnectionName =
  process.env["BING_PROJECT_CONNECTION_NAME"] || "<bing connection name>";

export async function main(): Promise<void> {
  const project = new AIProjectClient(projectEndpoint, new DefaultAzureCredential());
  const openAIClient = await project.getOpenAIClient();

  // Get connection ID from connection name
  const bingConnection = await project.connections.get(bingConnectionName);
  console.log(`Bing connection ID: ${bingConnection.id}`);

  console.log("Creating agent with Bing grounding tool...");

  const agent = await project.agents.createVersion("MyBingGroundingAgent", {
    kind: "prompt",
    model: deploymentName,
    instructions: "You are a helpful assistant.",
    tools: [
      {
        type: "bing_grounding",
        bing_grounding: {
          search_configurations: [
            {
              project_connection_id: bingConnection.id,
            },
          ],
        },
      },
    ],
  });
  console.log(`Agent created (id: ${agent.id}, name: ${agent.name}, version: ${agent.version})`);

  // Send request that requires current information from the web
  console.log("\nSending request to Bing grounding agent with streaming...");
  const streamResponse = await openAIClient.responses.create(
    {
      input: "What is today's date and weather in Seattle?",
      stream: true,
    },
    {
      body: {
        agent: { name: agent.name, type: "agent_reference" },
        tool_choice: "required",
      },
    },
  );

  // Process the streaming response
  for await (const event of streamResponse) {
    if (event.type === "response.created") {
      console.log(`Follow-up response created with ID: ${event.response.id}`);
    } else if (event.type === "response.output_text.delta") {
      process.stdout.write(event.delta);
    } else if (event.type === "response.output_text.done") {
      console.log("\n\nFollow-up response done!");
    } else if (event.type === "response.output_item.done") {
      if (event.item.type === "message") {
        const item = event.item;
        if (item.content && item.content.length > 0) {
          const lastContent = item.content[item.content.length - 1];
          if (lastContent.type === "output_text" && lastContent.annotations) {
            for (const annotation of lastContent.annotations) {
              if (annotation.type === "url_citation") {
                console.log(
                  `URL Citation: ${annotation.url}, Start index: ${annotation.start_index}, End index: ${annotation.end_index}`,
                );
              }
            }
          }
        }
      }
    } else if (event.type === "response.completed") {
      console.log("\nFollow-up completed!");
    }
  }

  // Clean up resources by deleting the agent version
  // This prevents accumulation of unused resources in your project
  console.log("\nCleaning up resources...");
  await project.agents.deleteVersion(agent.name, agent.version);
  console.log("Agent deleted");

  console.log("\nBing grounding agent sample completed!");
}

main().catch((err) => {
  console.error("The sample encountered an error:", err);
});
```

**What this code does**

This example creates an agent with grounding by using the Bing Search tool that can retrieve real-time information from the web. When you run the code:

1. It creates an `AIProjectClient` and authenticates by using your Azure credentials.
1. Creates an agent with the Bing grounding tool configured by using your Bing connection.
1. Sends a query asking about current date and weather in Seattle with tool choice set to "required".
1. The agent uses the Bing grounding tool to search the web and streams the response.
1. Processes streaming events and extracts URL citations with their positions in the text.
1. Cleans up by deleting the agent version.

**Required inputs**

- Environment variables: `AZURE_AI_PROJECT_ENDPOINT`, `AZURE_AI_MODEL_DEPLOYMENT_NAME`, `BING_PROJECT_CONNECTION_NAME`
- Azure credentials configured for `DefaultAzureCredential`

**Expected output**

```console
Creating agent with Bing grounding tool...
Agent created (id: asst_abc123, name: MyBingGroundingAgent, version: 1)

Sending request to Bing grounding agent with streaming...
Follow-up response created with ID: resp_xyz789
Today's date is December 12, 2025, and the weather in Seattle...

Follow-up response done!
URL Citation: https://www.weather.gov/seattle/, Start index: 45, End index: 120

Follow-up completed!

Cleaning up resources...
Agent deleted

Bing grounding agent sample completed!
```

### Grounding with Bing Custom Search (preview)

```typescript
import { DefaultAzureCredential } from "@azure/identity";
import { AIProjectClient } from "@azure/ai-projects";
import * as readline from "readline";
import "dotenv/config";

const projectEndpoint = process.env["AZURE_AI_PROJECT_ENDPOINT"] || "<project endpoint>";
const deploymentName =
  process.env["AZURE_AI_MODEL_DEPLOYMENT_NAME"] || "<model deployment name>";
const bingCustomSearchConnectionName =
  process.env["BING_CUSTOM_SEARCH_PROJECT_CONNECTION_NAME"] ||
  "<bing custom search connection name>";
const bingCustomSearchInstanceName =
  process.env["BING_CUSTOM_SEARCH_INSTANCE_NAME"] || "<bing custom search instance name>";

export async function main(): Promise<void> {
  const project = new AIProjectClient(projectEndpoint, new DefaultAzureCredential());
  const openAIClient = await project.getOpenAIClient();

  // Get connection ID from connection name
  const bingCustomConnection = await project.connections.get(bingCustomSearchConnectionName);
  console.log(`Bing Custom Search connection ID: ${bingCustomConnection.id}`);

  console.log("Creating agent with Bing Custom Search tool...");

  const agent = await project.agents.createVersion("MyAgent", {
    kind: "prompt",
    model: deploymentName,
    instructions:
      "You are a helpful agent that can use Bing Custom Search tools to assist users. Use the available Bing Custom Search tools to answer questions and perform tasks.",
    tools: [
      {
        type: "bing_custom_search_preview",
        bing_custom_search_preview: {
          search_configurations: [
            {
              project_connection_id: bingCustomConnection.id,
              instance_name: bingCustomSearchInstanceName,
            },
          ],
        },
      },
    ],
  });
  console.log(`Agent created (id: ${agent.id}, name: ${agent.name}, version: ${agent.version})`);

  // Prompt user for input
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });

  const userInput = await new Promise<string>((resolve) => {
    rl.question(
      "Enter your question for the Bing Custom Search agent (e.g., 'Tell me more about foundry agent service'): \n",
      (answer) => {
        rl.close();
        resolve(answer);
      },
    );
  });

  // Send initial request that will trigger the Bing Custom Search tool
  console.log("\nSending request to Bing Custom Search agent with streaming...");
  const streamResponse = await openAIClient.responses.create(
    {
      input: userInput,
      stream: true,
    },
    {
      body: {
        agent: { name: agent.name, type: "agent_reference" },
      },
    },
  );

  // Process the streaming response
  for await (const event of streamResponse) {
    if (event.type === "response.created") {
      console.log(`Follow-up response created with ID: ${event.response.id}`);
    } else if (event.type === "response.output_text.delta") {
      process.stdout.write(event.delta);
    } else if (event.type === "response.output_text.done") {
      console.log("\n\nFollow-up response done!");
    } else if (event.type === "response.output_item.done") {
      if (event.item.type === "message") {
        const item = event.item;
        if (item.content && item.content.length > 0) {
          const lastContent = item.content[item.content.length - 1];
          if (lastContent.type === "output_text" && lastContent.annotations) {
            for (const annotation of lastContent.annotations) {
              if (annotation.type === "url_citation") {
                console.log(
                  `URL Citation: ${annotation.url}, Start index: ${annotation.start_index}, End index: ${annotation.end_index}`,
                );
              }
            }
          }
        }
      }
    } else if (event.type === "response.completed") {
      console.log("\nFollow-up completed!");
    }
  }

  // Clean up resources by deleting the agent version
  // This prevents accumulation of unused resources in your project
  console.log("\nCleaning up resources...");
  await project.agents.deleteVersion(agent.name, agent.version);
  console.log("Agent deleted");

  console.log("\nBing Custom Search agent sample completed!");
}

main().catch((err) => {
  console.error("The sample encountered an error:", err);
});
```

**What this code does**

This example creates an agent with Grounding with Bing Custom Search tool that searches within your configured domains. When you run the code:

1. It creates an `AIProjectClient` and authenticates by using your Azure credentials.
1. Creates an agent with the Bing Custom Search tool configured by using your custom search instance.
1. Prompts for user input at runtime through the command line.
1. The agent uses the Bing Custom Search tool to search only your specified domains and streams the response.
1. Processes streaming events and extracts URL citations with their positions in the text.
1. Cleans up by deleting the agent version.

**Required inputs**

- Environment variables: `AZURE_AI_PROJECT_ENDPOINT`, `AZURE_AI_MODEL_DEPLOYMENT_NAME`, `BING_CUSTOM_SEARCH_PROJECT_CONNECTION_NAME`, `BING_CUSTOM_SEARCH_INSTANCE_NAME`
- Azure credentials configured for `DefaultAzureCredential`
- User input provided at runtime via console

**Expected output**

```console
Creating agent with Bing Custom Search tool...
Agent created (id: asst_abc123, name: MyAgent, version: 1)
Enter your question for the Bing Custom Search agent (e.g., 'Tell me more about foundry agent service'):
Tell me more about foundry agent service

Sending request to Bing Custom Search agent with streaming...
Follow-up response created with ID: resp_xyz789
Microsoft Foundry Agent Service enables you to build...

Follow-up response done!
URL Citation: https://learn.microsoft.com/azure/ai-foundry/agents, Start index: 0, End index: 89

Follow-up completed!

Cleaning up resources...
Agent deleted

Bing Custom Search agent sample completed!
```

:::zone-end

## How it works

The user query is the message that an end user sends to an agent, such as *"should I take an umbrella with me today? I'm in Seattle."* Instructions are the system message a developer can provide to share context and provide instructions to the AI model on how to use various tools or behave. 

When a user sends a query, the customer's AI model deployment first processes it (using the provided instructions) to later perform a Bing search query (which is [visible to developers](#how-to-display-search-results)). 
Grounding with Bing returns relevant search results to the customer's model deployment, which then generates the final output. 

> [!NOTE]
> When you use Grounding with Bing Search or Grounding with Bing Custom Search, the only information sent to Bing is the Bing search query, tool parameters, and your resource key. The service doesn't send any end user-specific information. Your resource key is sent to Bing solely for billing and rate limiting purposes. 

Authorization happens between the Grounding with Bing Search or Grounding with Bing Custom Search service and Foundry Agent Service. Any Bing search query that the service generates and sends to Bing for the purposes of grounding is transferred, along with the resource key, outside of the Azure compliance boundary to the Grounding with Bing Search service. Grounding with Bing Search is subject to Bing's terms and doesn't have the same compliance standards and certifications as the Agent Service, as described in the [Terms of Use](https://www.microsoft.com/bing/apis/grounding-legal-enterprise). You're responsible for assessing whether the use of Grounding with Bing Search or Grounding with Bing Custom Search in your agent meets your needs and requirements.

Transactions with your Grounding with Bing resource are counted by the number of tool calls per run. You can see how many tool calls are made from the run step.

Developers and end users don't have access to raw content returned from Grounding with Bing Search. The model response, however, includes citations with links to the websites used to generate the response, and a link to the Bing query used for the search. You can retrieve the **model response** by accessing the data in the conversation that was created. These two *references* must be retained and displayed in the exact form provided by Microsoft, as per Grounding with Bing Search's [Use and Display Requirements](https://www.microsoft.com/bing/apis/grounding-legal-enterprise#use-and-display-requirements). See the [how to display Grounding with Bing Search results](#how-to-display-search-results) section for details.

## How to display search results

According to Grounding with Bing's [terms of use and use and display requirements](https://www.microsoft.com/bing/apis/grounding-legal-enterprise#use-and-display-requirements#use-and-display-requirements), you need to display both website URLs and Bing search query URLs in your custom interface. You can find this information in the API response, in the `arguments` parameter. To render the webpage, replace the endpoint of Bing search query URLs with `www.bing.com` and your Bing search query URL would look like `https://www.bing.com/search?q={search query}`.

:::image type="content" source="../../../../agents/media/tools/bing/website-citations.png" alt-text="A screenshot showing citations for Bing search results." lightbox="../../../../agents/media/tools/bing/website-citations.png":::

## Grounding with Bing Custom Search configuration

Grounding with Bing Custom Search is a powerful tool that you can use to select a subspace of the web to limit your agent’s grounding knowledge. Here are a few tips to help you take full advantage of this capability: 

- If you own a public site that you want to include in the search but Bing hasn't indexed, see the [Bing Webmaster Guidelines](https://www.bing.com/webmasters/help/webmasters-guidelines-30fba23a) for details about getting your site indexed. The webmaster documentation also provides details about getting Bing to crawl your site if the index is out of date. 
- You need at least the contributor role for the Bing Custom Search resource to create a configuration.
- You can only block certain domains and perform a search against the rest of the web (a competitor's site, for example). 
- Grounding with Bing Custom Search only returns results for domains and webpages that are public and indexed by Bing. 
  - Domain (for example, `https://www.microsoft.com`) 
  - Domain and path (for example, `https://www.microsoft.com/surface`) 
  - Webpage (for example, `https://www.microsoft.com/en-us/p/surface-earbuds/8r9cpq146064`)
 
## Optional parameters

When you add the Grounding with Bing Search or Grounding with Bing Custom Search tool to your agent, you can pass the following parameters. These parameters will impact the tool output, and the AI model might not fully use all of the outputs. See the code examples for information on API version support and how to pass these parameters.

|Name|Value|Type|Required |
|-|-|-|- |
|`count`|The number of search results to return in the response. The default is 5 and the maximum value is 50. The actual number delivered may be less than requested. It is possible for multiple pages to include some overlap in results. This parameter affects only web page results. It's possible that AI model might not use all search results returned by Bing.|`UnsignedShort`|No |
|`freshness`|Filter search results by the following case-insensitive age values: <br/> **Day**: Return webpages that Bing discovered within the last 24 hours.<br/> **Week**: Return webpages that Bing discovered within the last 7 days.<br/> **Month**: Return webpages that Bing discovered within the last 30 days. To get articles discovered by Bing during a specific timeframe, specify a date range in the form: `YYYY-MM-DD..YYYY-MM-DD`. For example, `freshness=2019-02-01..2019-05-30`. To limit the results to a single date, set this parameter to a specific date. For example, `freshness=2019-02-04`.|String|No |
|`market`|The market where the results come from. Typically, `mkt` is the country/region where the user is making the request from. However, it could be a different country/region if the user is not located in a country/region where Bing delivers results. The market must be in the form: `<language>-<country/region>`. For example, `en-US`. The string is case insensitive. For a list of possible market values, see [Market codes](/bing/search-apis/bing-web-search/reference/market-codes). If known, you are encouraged to always specify the market. Specifying the market helps Bing route the request and return an appropriate and optimal response. If you specify a market that is not listed in Market codes, Bing uses a best fit market code based on an internal mapping that is subject to change. |String|No |
|`set_lang`|The language to use for user interface strings. You may specify the language using either a 2-letter or 4-letter code. Using 4-letter codes is preferred.<br/> For a list of supported language codes, see [Bing supported languages](/bing/search-apis/bing-web-search/reference/market-codes#bing-supported-language-codes).<br/> Bing loads the localized strings if `setlang` contains a valid 2-letter neutral culture code (`fr`) or a valid 4-letter specific culture code (`fr-ca`). For example, for `fr-ca`, Bing loads the `fr` neutral culture code strings.<br/> If `setlang` is not valid (for example, `zh`) or Bing doesn’t support the language (for example, `af`, `af-na`), Bing defaults to `en` (English).<br/> To specify the 2-letter code, set this parameter to an ISO 639-1 language code.<br/> To specify the 4-letter code, use the form `<language>-<country/region>` where `<language>` is an ISO 639-1 language code (neutral culture) and `<country/region>` is an ISO 3166 country/region (specific culture) code. For example, use `en-US` for United States English.<br/> Although optional, you should always specify the language. Typically, you set `setLang` to the same language specified by `mkt` unless the user wants the user interface strings displayed in a different language. |String|No |

## Supported capabilities and known issues

- The Grounding with Bing Search tool is designed to retrieve real-time information from the web, not specific web domains. To retrieve information from specific domains, use the Grounding with Bing Custom Search tool.
- Don't ask the model to **summarize** an entire web page.
- Within one run, the AI model evaluates the tool outputs and might decide to invoke the tool again for more information and context. The AI model might also decide which pieces of tool outputs are used to generate the response.
- Foundry Agent Service returns **AI model generated responses** as output, so end-to-end latency is impacted by model pre-processing and post-processing.
- The Grounding with Bing Search and Grounding with Bing Custom Search tools don't return the tool output to developers and end users.
- Grounding with Bing Search and Grounding with Bing Custom Search only work with agents that aren't using VPN or private endpoints. The agent must have normal network access.
- Use the default citations pattern (the links sent in `annotation`) for links from the Grounding with Bing tools. Don't ask the model to generate citation links.

## Troubleshooting

Use this section to resolve common issues when using Grounding with Bing Search tools.

### Connection ID format errors

**Problem**: Error message stating invalid connection ID format.

**Solution**: Verify your connection ID matches the required format:
```text
/subscriptions/{{subscriptionID}}/resourceGroups/{{resourceGroupName}}/providers/Microsoft.CognitiveServices/accounts/{{foundryAccountName}}/projects/{{foundryProjectName}}/connections/{{foundryConnectionName}}
```

Replace all placeholder values (including `{{` and `}}`) with your actual resource identifiers.

### Authentication failures

**Problem**: "Unauthorized" or "Forbidden" errors when creating agents or running queries.

**Solution**: 
1. Verify you have the required RBAC roles:
   - **Contributor** or **Owner** role for creating Bing resources
   - **Azure AI Project Manager** role for creating project connections
1. Check that your Azure credentials are properly configured:
   - For Python/TypeScript: `DefaultAzureCredential` can authenticate
   - For REST: Bearer token is valid and not expired
1. Run `az login` to refresh your credentials if you're using Azure CLI

### Network connectivity problems

**Problem**: Grounding with Bing Search requests time out or can't connect.

**Solution**: Grounding with Bing Search and Grounding with Bing Custom Search don't work with VPN or Private Endpoints. Ensure:
- Your network has normal internet access.
- You're not using a VPN connection.
- Private Endpoints aren't configured for the agent service.
- Firewall rules allow outbound connections to Bing services.

### Custom search returns no results

**Problem**: Bing Custom Search returns empty results or doesn't find expected content.

**Solution**:
- Verify your custom search instance is properly configured with target domains.
- Ensure the domains you want to search are public and indexed by Bing.
- Check that the configured domains match your search query expectations.
- If your site isn't indexed, see [Bing Webmaster Guidelines](https://www.bing.com/webmasters/help/webmasters-guidelines-30fba23a) for indexing instructions.
- Wait for Bing to crawl recently added or updated content (can take several days).

### Missing or invalid environment variables

**Problem**: Code fails with `KeyError` or "environment variable not found" errors.

**Solution**: Ensure you set all required environment variables:
- `AZURE_AI_PROJECT_ENDPOINT`
- `AZURE_AI_MODEL_DEPLOYMENT_NAME`
- `BING_PROJECT_CONNECTION_ID` or `BING_CUSTOM_SEARCH_PROJECT_CONNECTION_ID`
- For custom search: `BING_CUSTOM_SEARCH_INSTANCE_NAME`
- For REST API: `API_VERSION`, `AGENT_TOKEN`

Create a `.env` file or set system environment variables with these values.

### Agent doesn't use the grounding tool

**Problem**: Agent responds without calling the Bing grounding tool.

**Solution**:
- Ensure your query requires current information that the model doesn't know.
- For explicit tool usage, set `tool_choice="required"` in your request (Python/TypeScript examples show this).
- Verify the tool is properly configured in the agent definition.
- Check agent instructions encourage using available tools for current information.

### Instance name not found for Grounding with Bing Custom Search tool

**Problem**:

```json
{"error": "Tool_User_Error", "message": "[bing_search] Failed to call Get Custom Search Instance with status 404: {\"error\":{\"code\":\"ResourceNotFound\",\"message\":\"Instance or Customer not found\",\"target\":\"instanceName or customerId\"}}."}
```

**Solution**:
- Ensure your instance name is in the Grounding with Bing Custom Search resource you are using.
- Double check if your instance name is spelled correctly.

## Manage Grounding with Bing Search and Grounding with Bing Custom Search

Admins can use RBAC role assignments to enable or disable the use of Grounding with Bing and Grounding with Bing Custom Search within the subscription or resource group. 

1. The admin registers `Microsoft.Bing` in the Azure subscription. The admin needs permissions to perform the `/register/action` operation for the resource provider. The Contributor and Owner roles include this permission. For more information about how to register, see [Azure resource providers and types](/azure/azure-resource-manager/management/resource-providers-and-types).
1. After the admin registers `Microsoft.Bing`, users with permissions can create, delete, or retrieve the resource key for a Grounding with Bing and/or Grounding with Bing Custom Search resource. These users need the **Contributor** or **Owner** role at the subscription or resource group level. 
1. After creating a Grounding with Bing and/or Grounding with Bing Custom Search resource, users with permissions can create a Microsoft Foundry connection to connect to the resource and use it as a tool in Foundry Agent Service. These users need at least the **Azure AI Project Manager** role. 

### Disable use of Grounding with Bing Search and Grounding with Bing Custom Search

1. The admin needs the **Owner** or **Contributor** role in the subscription.
1. The admin deletes all Grounding with Bing Search and Grounding with Bing Custom Search resources in the subscription.
1. The admin unregisters the `Microsoft.Bing` resource provider in the subscription (you can't unregister before deleting all resources). For more information, see [Azure resource providers and types](/azure/azure-resource-manager/management/resource-providers-and-types).
1. The admin creates an Azure Policy to disallow creation of Grounding with Bing Search and Grounding with Bing Custom Search resources in their subscription, following the [sample](https://github.com/azure-ai-foundry/foundry-samples/blob/main/infrastructure/infrastructure-setup-bicep/05-custom-policy-definitions/deny-disallowed-connections.json).

## Next steps

- [Tool use best practices](../../concepts/tool-best-practice.md) - Learn optimization strategies for agent tools
- [Web search tool (preview)](web-search.md) - Use web search without configuring Bing tool parameters
- [Manage Grounding with Bing in Microsoft Foundry and Azure](../manage-grounding-with-bing.md) - Control and disable Grounding with Bing features
- [Connect OpenAPI tools to agents](openapi.md) - Integrate custom APIs with your agents
- [Discover tools in the Foundry Tools (preview)](../../concepts/tool-catalog.md) - Explore all available agent tools in Foundry Agent Service
