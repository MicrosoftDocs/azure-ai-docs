---
title: Use SharePoint content with agent API
titleSuffix: Microsoft Foundry
description: Learn how to ground Microsoft Foundry agents with SharePoint content using the agent API. Connect to SharePoint sites or folders, use identity passthrough, and keep enterprise access controls intact.
services: cognitive-services
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: how-to
ms.date: 01/26/2026
author: alvinashcraft
ms.author: aashcraft
ms.custom: 
    - azure-ai-agents
    - dev-focus
    - pilot-ai-workflow-jan-2026
ai-usage: ai-assisted
zone_pivot_groups: selection-agent-sharepoint-new
---

# Use SharePoint tool with the agent API (preview)

[!INCLUDE [feature-preview](../../../../includes/feature-preview.md)]

> [!NOTE]
> - This article describes the Microsoft SharePoint tool for Foundry Agent Service. For information on using and deploying SharePoint sites, see the [SharePoint documentation](/sharepoint/).
> - See [best practices](../../concepts/tool-best-practice.md) for information on optimizing tool usage.

Use the SharePoint tool (preview) for SharePoint grounding in Microsoft Foundry Agent Service by retrieving content from a SharePoint site or folder (for example, `contoso.sharepoint.com/sites/policies`). When a user asks a question, the agent can invoke the SharePoint tool to retrieve relevant text from documents the user can access (requires a Microsoft 365 Copilot license). The agent then generates a response based on that retrieved content.

This integration uses identity passthrough (On-Behalf-Of) so SharePoint permissions continue to apply to every request. For details on the underlying Microsoft 365 Copilot Retrieval API integration, see [How it works](#how-it-works).

### Usage support

| Microsoft Foundry support | Python SDK | C# SDK | JavaScript SDK | Java SDK | REST API | Basic agent setup | Standard agent setup |
|---------|---------|---------|---------|---------|---------|---------|
| ✔️ | ✔️ | ✔️ | ✔️ | - | ✔️ | ✔️ | ✔️ |

## Prerequisites

- Eligible license or Pay-as-you-go model:
  - Developers and end users have Microsoft 365 Copilot license, as required by [Microsoft 365 Copilot API](/microsoft-365-copilot/extensibility/api-reference/retrieval-api-overview).
  - If developers and end users don't have Microsoft 365 Copilot license, you can enable the [pay-as-you-go model](/microsoft-365-copilot/extensibility/api/ai-services/retrieval/paygo-retrieval).
- Developers and end users have at least `Azure AI User` RBAC role assigned on the Foundry project. For more information about Azure role-based access control, see [Azure role-based access control in Foundry](../../../../concepts/rbac-foundry.md?view=foundry&preserve-view=true).
- Developers and end users have at least `READ` access to the SharePoint site.
- The latest prerelease package installed:
  - **Python**: `pip install azure-ai-projects --pre`
  - **C#**: Install the `Azure.AI.Projects` NuGet package (prerelease)
  - **TypeScript/JavaScript**: `npm install @azure/ai-projects`
- Environment variables configured:
  - `AZURE_AI_PROJECT_ENDPOINT`: Your Foundry project endpoint URL
  - `AZURE_AI_MODEL_DEPLOYMENT_NAME`: Your model deployment name (for example, `gpt-4`)
  - `SHAREPOINT_PROJECT_CONNECTION_ID`: Your SharePoint connection ID in the format `/subscriptions/{{subscriptionID}}/resourceGroups/{{resourceGroupName}}/providers/Microsoft.CognitiveServices/accounts/{{foundryAccountName}}/projects/{{foundryProjectName}}/connections/{{foundryConnectionName}}`
  - For REST samples: `API_VERSION`, `AGENT_TOKEN`
- See the [quickstart](../../../../quickstarts/get-started-code.md?view=foundry&preserve-view=true#get-ready-to-code) for additional authentication setup details.

## Parameters

The SharePoint tool uses your project connection to determine which SharePoint site or folder it can retrieve from.

| Parameter | Required | Notes |
| --- | --- | --- |
| `type` | Yes | Use `sharepoint_grounding_preview`. |
| `sharepoint_grounding_preview.project_connections[].project_connection_id` | Yes | Use the value of `SHAREPOINT_PROJECT_CONNECTION_ID`. |

If you need to create a SharePoint connection for your project, see [Add a new connection to your project](../../../../how-to/connections-add.md?view=foundry&preserve-view=true).

## Code example

:::zone pivot="python"

### Quick verification

Before running the full sample, verify your SharePoint connection exists:

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
    
    # Verify SharePoint connection exists
    connection_name = os.environ.get("SHAREPOINT_PROJECT_CONNECTION_NAME")
    if connection_name:
        try:
            conn = project_client.connections.get(connection_name)
            print(f"SharePoint connection verified: {conn.name}")
            print(f"Connection ID: {conn.id}")
        except Exception as e:
            print(f"SharePoint connection '{connection_name}' not found: {e}")
    else:
        # List available connections to help find the right one
        print("SHAREPOINT_PROJECT_CONNECTION_NAME not set. Available connections:")
        for conn in project_client.connections.list():
            print(f"  - {conn.name}")
```

If this code runs without errors, your credentials and SharePoint connection are configured correctly.

### Full sample

The following sample demonstrates how to create an Agent that uses the SharePoint tool to ground responses with content from a SharePoint site.

```python
import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    PromptAgentDefinition,
    SharepointAgentTool,
    SharepointGroundingToolParameters,
    ToolProjectConnection,
)

load_dotenv()

with (
    DefaultAzureCredential() as credential,
    AIProjectClient(endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"], credential=credential) as project_client,
    project_client.get_openai_client() as openai_client,
):
    # Get connection ID from connection name
    sharepoint_connection = project_client.connections.get(
        os.environ["SHAREPOINT_PROJECT_CONNECTION_NAME"],
    )
    print(f"SharePoint connection ID: {sharepoint_connection.id}")

    sharepoint_tool = SharepointAgentTool(
        sharepoint_grounding_preview=SharepointGroundingToolParameters(
            project_connections=[
                ToolProjectConnection(project_connection_id=sharepoint_connection.id)
            ]
        )
    )

    agent = project_client.agents.create_version(
        agent_name="MyAgent",
        definition=PromptAgentDefinition(
            model=os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
            instructions="""You are a helpful agent that can use SharePoint tools to assist users. 
            Use the available SharePoint tools to answer questions and perform tasks.""",
            tools=[sharepoint_tool],
        ),
    )
    print(f"Agent created (id: {agent.id}, name: {agent.name}, version: {agent.version})")

    # Send initial request that will trigger the SharePoint tool
    stream_response = openai_client.responses.create(
        stream=True,
      tool_choice="required",
        input="Please summarize the last meeting notes stored in SharePoint.",
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

### What this code does

This example creates an agent with SharePoint grounding capabilities and processes a streaming response:

1. **Initialize the project client** by using your Foundry project endpoint and Azure credentials.
1. **Configure the SharePoint tool** with your project connection to enable access to SharePoint content.
1. **Create the agent** with instructions and the SharePoint tool attached.
1. **Send a query** asking the agent to summarize meeting notes from SharePoint.
1. **Process the streaming response** to display the agent's answer in real-time.
1. **Extract URL citations** from the response annotations showing which SharePoint documents were referenced.

### Expected output

When you run this code, you see output similar to:

```text
Agent created (id: asst_abc123, name: MyAgent, version: 1)

Sending request to SharePoint agent with streaming...
Follow-up response created with ID: resp_xyz789
Delta: Based
Delta:  on
Delta:  the
Delta:  meeting
Delta:  notes
...
URL Citation: https://contoso.sharepoint.com/sites/policies/Documents/meeting-notes.docx, Start index: 0, End index: 245

Follow-up response done!

Follow-up completed!
Full response: Based on the meeting notes from your SharePoint site, the last meeting covered the following topics: project timeline updates, budget review, and next quarter planning.
```

:::zone-end

:::zone pivot="csharp"

### Quick verification

Before running the full sample, verify your SharePoint connection exists:

```csharp
using Azure.AI.Projects;
using Azure.Identity;

var projectEndpoint = System.Environment.GetEnvironmentVariable("AZURE_AI_PROJECT_ENDPOINT");
var sharepointConnectionName = System.Environment.GetEnvironmentVariable("SHAREPOINT_PROJECT_CONNECTION_NAME");

AIProjectClient projectClient = new(endpoint: new Uri(projectEndpoint), tokenProvider: new DefaultAzureCredential());

// Verify SharePoint connection exists
try
{
    AIProjectConnection conn = projectClient.Connections.GetConnection(connectionName: sharepointConnectionName);
    Console.WriteLine($"SharePoint connection verified: {conn.Name}");
    Console.WriteLine($"Connection ID: {conn.Id}");
}
catch (Exception ex)
{
    Console.WriteLine($"SharePoint connection '{sharepointConnectionName}' not found: {ex.Message}");
    // List available connections
    Console.WriteLine("Available connections:");
    foreach (var conn in projectClient.Connections.GetConnections())
    {
        Console.WriteLine($"  - {conn.Name}");
    }
}
```

If this code runs without errors, your credentials and SharePoint connection are configured correctly.

### Full sample

The following sample demonstrates how to create an Agent that uses the SharePoint tool to ground responses with content from a SharePoint site. This example uses synchronous methods for simplicity. For an asynchronous version, refer to the [SharePoint agent sample documentation](https://github.com/Azure/azure-sdk-for-net/blob/feature/ai-foundry/agents-v2/sdk/ai/Azure.AI.Projects.OpenAI/samples/Sample24_Sharepoint.md) on the Azure SDK for .NET GitHub repository.

To enable your Agent to access SharePoint, use `SharepointAgentTool`.

```csharp
using System;
using Azure.AI.Projects;
using Azure.AI.Projects.OpenAI;
using Azure.Identity;

// Create an agent client and read the environment variables, which will be used in the next steps.
var projectEndpoint = System.Environment.GetEnvironmentVariable("AZURE_AI_PROJECT_ENDPOINT");
var modelDeploymentName = System.Environment.GetEnvironmentVariable("AZURE_AI_MODEL_DEPLOYMENT_NAME");
var sharepointConnectionName = System.Environment.GetEnvironmentVariable("SHAREPOINT_PROJECT_CONNECTION_NAME");
AIProjectClient projectClient = new(endpoint: new Uri(projectEndpoint), tokenProvider: new DefaultAzureCredential());

// Get connection ID from connection name
AIProjectConnection sharepointConnection = projectClient.Connections.GetConnection(connectionName: sharepointConnectionName);

// Use the SharePoint connection ID to initialize the SharePointGroundingToolOptions,
// which will be used to create SharepointAgentTool. Use this tool to create an Agent.
SharePointGroundingToolOptions sharepointToolOption = new()
{
    ProjectConnections = { new ToolProjectConnection(projectConnectionId: sharepointConnection.Id) }
};
PromptAgentDefinition agentDefinition = new(model: modelDeploymentName)
{
    Instructions = "You are a helpful assistant.",
    Tools = { new SharepointPreviewTool(sharepointToolOption), }
};
AgentVersion agentVersion = projectClient.Agents.CreateAgentVersion(
    agentName: "myAgent",
    options: new(agentDefinition));

// Create the response and make sure we are always using tool.
ProjectResponsesClient responseClient = projectClient.OpenAI.GetProjectResponsesClientForAgent(agentVersion.Name);
CreateResponseOptions responseOptions = new()
{
    ToolChoice = ResponseToolChoice.CreateRequiredChoice(),
    InputItems = { ResponseItem.CreateUserMessageItem("What is Contoso whistleblower policy") }
};
ResponseResult response = responseClient.CreateResponse(options: responseOptions);

// SharePoint tool can create the reference to the page, grounding the data.
// Create the GetFormattedAnnotation method to get the URI annotation.
string annotation = "";
foreach (ResponseItem item in response.OutputItems)
{
    if (item is MessageResponseItem messageItem)
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

// Print the Agent output and add the annotation at the end.
Assert.That(response.Status, Is.EqualTo(ResponseStatus.Completed));
Console.WriteLine($"{response.GetOutputText()}{annotation}");

// After the sample is completed, delete the Agent we have created.
projectClient.Agents.DeleteAgentVersion(agentName: agentVersion.Name, agentVersion: agentVersion.Version);
```

### What this code does

This example demonstrates SharePoint grounding with synchronous methods:

1. **Create a project client** using your Foundry project endpoint
1. **Retrieve the SharePoint connection** by name from your project's connections
1. **Configure the SharePoint tool** with the connection ID
1. **Create an agent** with the SharePoint tool to enable document access
1. **Create a response** asking about the Contoso whistleblower policy
1. **Format and display the response** with a helper method that extracts URL citations from annotations
1. **Clean up** by deleting the agent version

### Expected output

When you run this code, you see output similar to:

```text
The Contoso whistleblower policy outlines procedures for reporting unethical behavior confidentially. Employees can submit concerns through the ethics hotline or online portal. [Whistleblower Policy](https://contoso.sharepoint.com/sites/policies/Documents/whistleblower-policy.pdf)
```

The output includes the agent's response grounded in SharePoint content, with a citation link to the source document.

:::zone-end

:::zone pivot="rest"
## Sample for use of an Agent with SharePoint

The following sample demonstrates how to create an Agent that uses the SharePoint tool to ground responses with content from a SharePoint site.

```bash
curl --request POST \
  --url "$AZURE_AI_PROJECT_ENDPOINT/openai/responses?api-version=$API_VERSION" \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
  "model": "'$AZURE_AI_MODEL_DEPLOYMENT_NAME'",
  "input": "Please summarize the last meeting notes stored in SharePoint.",
  "tool_choice": "required",
  "tools": [
    {
      "type": "sharepoint_grounding_preview",
      "sharepoint_grounding_preview": {
        "project_connections": [
          {
            "project_connection_id": "'$SHAREPOINT_PROJECT_CONNECTION_ID'"
          }
        ]
      }
    }
  ]
}'
```

### What this code does

This REST API call creates a response with SharePoint grounding:

1. **Sends a POST request** to the `/openai/responses` endpoint
2. **Authenticates** using a bearer token for your agent
3. **Specifies the model** deployment to use for generating responses
4. **Includes the user's query** asking for meeting notes from SharePoint
5. **Configures the SharePoint tool** with your project connection ID to enable document retrieval
6. **Returns a JSON response** with the agent's answer and citations to source documents

### Expected output

The API returns a JSON response with the agent's answer and citation information:

```json
{
  "id": "resp_abc123xyz",
  "object": "response",
  "created_at": 1702345678,
  "status": "completed",
  "output_text": "Based on the meeting notes from your SharePoint site, the last meeting covered project timeline updates, budget review, and next quarter planning.",
  "output_items": [
    {
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "Based on the meeting notes...",
          "annotations": [
            {
              "type": "url_citation",
              "url": "https://contoso.sharepoint.com/sites/policies/Documents/meeting-notes.docx",
              "start_index": 0,
              "end_index": 245
            }
          ]
        }
      ]
    }
  ]
}
```

:::zone-end

:::zone pivot="typescript"

### Quick verification

Before running the full sample, verify your SharePoint connection exists:

```typescript
import { DefaultAzureCredential } from "@azure/identity";
import { AIProjectClient } from "@azure/ai-projects";
import "dotenv/config";

const projectEndpoint = process.env["AZURE_AI_PROJECT_ENDPOINT"] || "<project endpoint>";
const sharepointConnectionName = process.env["SHAREPOINT_PROJECT_CONNECTION_NAME"] || "<sharepoint connection name>";

async function verifyConnection(): Promise<void> {
  const project = new AIProjectClient(projectEndpoint, new DefaultAzureCredential());
  console.log("Connected to project.");

  try {
    const conn = await project.connections.get(sharepointConnectionName);
    console.log(`SharePoint connection verified: ${conn.name}`);
    console.log(`Connection ID: ${conn.id}`);
  } catch (error) {
    console.log(`SharePoint connection '${sharepointConnectionName}' not found: ${error}`);
    // List available connections
    console.log("Available connections:");
    for await (const conn of project.connections.list()) {
      console.log(`  - ${conn.name}`);
    }
  }
}

verifyConnection().catch(console.error);
```

If this code runs without errors, your credentials and SharePoint connection are configured correctly.

### Full sample

This sample demonstrates how to create an AI agent with SharePoint capabilities using the `SharepointAgentTool` and synchronous Azure AI Projects client. The agent can search SharePoint content and provide responses with relevant information from SharePoint sites. For a JavaScript version of this sample, refer to the [SharePoint agent sample documentation](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/ai/ai-projects/samples/v2-beta/javascript/agents/tools/agentSharepoint.js) in the Azure SDK for JavaScript GitHub repository.

```typescript
import { DefaultAzureCredential } from "@azure/identity";
import { AIProjectClient } from "@azure/ai-projects";
import "dotenv/config";

const projectEndpoint = process.env["AZURE_AI_PROJECT_ENDPOINT"] || "<project endpoint>";
const deploymentName = process.env["AZURE_AI_MODEL_DEPLOYMENT_NAME"] || "<model deployment name>";
const sharepointConnectionName =
  process.env["SHAREPOINT_PROJECT_CONNECTION_NAME"] || "<sharepoint connection name>";

export async function main(): Promise<void> {
  const project = new AIProjectClient(projectEndpoint, new DefaultAzureCredential());
  const openAIClient = await project.getOpenAIClient();

  // Get connection ID from connection name
  const sharepointConnection = await project.connections.get(sharepointConnectionName);
  console.log(`SharePoint connection ID: ${sharepointConnection.id}`);

  console.log("Creating agent with SharePoint tool...");

  const agent = await project.agents.createVersion("MyAgent", {
    kind: "prompt",
    model: deploymentName,
    instructions:
      "You are a helpful agent that can use SharePoint tools to assist users. Use the available SharePoint tools to answer questions and perform tasks.",
    // Define SharePoint tool that searches SharePoint content
    tools: [
      {
        type: "sharepoint_grounding_preview",
        sharepoint_grounding_preview: {
          project_connections: [
            {
              project_connection_id: sharepointConnection.id,
            },
          ],
        },
      },
    ],
  });
  console.log(`Agent created (id: ${agent.id}, name: ${agent.name}, version: ${agent.version})`);

  // Send initial request that will trigger the SharePoint tool
  console.log("\nSending request to SharePoint agent with streaming...");
  const streamResponse = await openAIClient.responses.create(
    {
      input: "Please summarize the last meeting notes stored in SharePoint.",
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

  console.log("\nSharePoint agent sample completed!");
}

main().catch((err) => {
  console.error("The sample encountered an error:", err);
});
```

### What this code does

This TypeScript example demonstrates the complete agent lifecycle with SharePoint:

1. **Initialize the project client** with your Foundry endpoint and Azure credentials.
1. **Get the OpenAI client** for creating responses.
1. **Create an agent** with SharePoint tool configuration using your project connection ID.
1. **Send a streaming request** asking the agent to summarize meeting notes.
1. **Process streaming events** to display the response as it's generated.
1. **Extract and display URL citations** from response annotations.
1. **Clean up resources** by deleting the agent version after completion.

### Expected output

When you run this code, you see output similar to:

```text
Creating agent with SharePoint tool...
Agent created (id: asst_abc123, name: MyAgent, version: 1)

Sending request to SharePoint agent with streaming...
Follow-up response created with ID: resp_xyz789
Based on the meeting notes from your SharePoint site, the last meeting covered the following topics: project timeline updates, budget review, and next quarter planning.

Follow-up response done!
URL Citation: https://contoso.sharepoint.com/sites/policies/Documents/meeting-notes.docx, Start index: 0, End index: 245

Follow-up completed!

Cleaning up resources...
Agent deleted

SharePoint agent sample completed!
```

:::zone-end

## Limitations

- The SharePoint tool only supports user identity authentication. App-only (service principal) authentication isn't supported.
- Your SharePoint site and your Microsoft Foundry agent must be in the same tenant.
- You can add only one SharePoint tool per agent.
- The underlying Microsoft 365 Copilot Retrieval API returns text extracts. Retrieval from nontextual content, including images and charts, isn't supported.
- For semantic and hybrid retrieval, the Microsoft 365 Copilot Retrieval API supports `.doc`, `.docx`, `.pptx`, `.pdf`, `.aspx`, and `.one` file types. For details, see the [Microsoft 365 Copilot API](/microsoft-365-copilot/extensibility/api-reference/retrieval-api-overview).

## Setup

> [!NOTE]
> Start with SharePoint sites that have a simple folder structure and a small number of short documents.

1. Select **SharePoint** and follow the prompts to add the tool. You can only add one per agent.

1. Add a SharePoint connection.

   For step-by-step instructions, see [Add a new connection to your project](../../../../how-to/connections-add.md?view=foundry&preserve-view=true).

  1. In the SharePoint connection configuration, enter the site URL or folder URL.

     - Site URL example: `https://<company>.sharepoint.com/sites/<site_name>`
     - Folder URL example: `https://<company>.sharepoint.com/sites/<site_name>/Shared%20documents/<folder_name>`

     > [!NOTE]
     > Your `site_url` needs to follow the format above. If you copy the entire value from the address bar of your SharePoint, it doesn't work.

  1. Save the connection, and then copy its connection **ID**.
  1. Set the connection ID as `SHAREPOINT_PROJECT_CONNECTION_ID`.

## How it works

The SharePoint tool makes it possible by enabling seamless integrations between AI agents and business documents stored in SharePoint. This capability is empowered by the [Microsoft 365 Copilot API](/microsoft-365-copilot/extensibility/api-reference/retrieval-api-overview). To ground your SharePoint documents, enter the sites or folders to connect with. The SharePoint tool leverages [built-in indexing capabilities](/microsoftsearch/semantic-index-for-copilot) to enhance the search and retrieval experience, including intelligent indexing, query processing, and content chunking.

For more information about delegated access and identity passthrough in Foundry, see [Agent identity concepts in Microsoft Foundry](../../concepts/agent-identity.md).

Instead of requiring developers to export SharePoint content, build a custom semantic index, manage governance controls, and configure refresh logic, this capability automates the entire retrieval pipeline. It dynamically indexes documents, breaks content into meaningful chunks, and applies advanced query processing to surface the most relevant information. By leveraging the same enterprise-grade retrieval stack that powers Microsoft 365 Copilot, it ensures AI agent responses are grounded in the most up-to-date and contextually relevant content. 

Customers rely on data security in SharePoint to access, create, and share documents with flexible document-level access control. Enterprise features such as Identity Passthrough/On-Behalf-Of (OBO) authentication ensure proper access control. End users receive responses generated from SharePoint documents they have permission to access. By using OBO authentication, the Foundry Agent service uses the end user's identity to authorize and retrieve relevant SharePoint documents, generating responses tailored towards specific end users.

## Troubleshooting

| Issue | Cause | Resolution |
| --- | --- | --- |
| `AuthenticationError: AppOnly OBO tokens not supported by target service` | Using application identity instead of user identity | The SharePoint tool requires user identity (identity passthrough). Don't use application-only authentication. |
| `Forbidden: Authorization Failed - User does not have valid license` | Missing Microsoft 365 Copilot license | Assign a Microsoft 365 Copilot license to the user, as required by the [Microsoft 365 Copilot API](/microsoft-365-copilot/extensibility/api-reference/retrieval-api-overview). |
| 401 or authentication failures | Cross-tenant access attempt | Confirm the user in Foundry and Microsoft 365 is in the same tenant. |
| Tool returns no results | User lacks access to SharePoint content | Verify the user has read access to the SharePoint sites and documents being queried. |
| Slow response times | Large document search scope | Narrow the search scope by specifying specific sites or libraries. Consider using more specific search queries. |
| Incomplete document retrieval | Content not indexed | Confirm the SharePoint content is indexed by Microsoft Search. Recently added content might need time to be indexed. |
| `Resource not found` errors | Invalid site or library path | Verify the SharePoint site URL and library paths are correct and accessible to the user. |
| Inconsistent search results | Semantic index sync delay | Wait for the semantic index to sync. Large content changes might take time to propagate. See [Semantic indexing for Microsoft 365 Copilot](/microsoftsearch/semantic-index-for-copilot). |

## Next steps

- For reference, see articles about content retrieval used by the tool:
  - [Overview of the Microsoft 365 Copilot Retrieval API](/microsoft-365-copilot/extensibility/api-reference/retrieval-api-overview).
  - [Semantic indexing for Microsoft 365 Copilot](/microsoftsearch/semantic-index-for-copilot)
