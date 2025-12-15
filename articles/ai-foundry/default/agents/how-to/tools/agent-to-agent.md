---
title: Add an A2A agent endpoint to Foundry Agent Service
titleSuffix: Microsoft Foundry
description: Learn how to add an A2A agent endpoint to Microsoft Foundry Agent Service for agent-to-agent communication using the Agent2Agent protocol.
services: azure-ai-agent-service
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: how-to
ms.date: 12/15/2025
author: alvinashcraft
ms.author: aashcraft
ms.custom: azure-ai-agents, dev-focus
ai-usage: ai-assisted
zone_pivot_groups: selection-agent-to-agent
---

# Add an A2A agent endpoint to Foundry Agent Service (preview)

[!INCLUDE [feature-preview](../../../../includes/feature-preview.md)]

> [!NOTE]
> See [best practices](../../concepts/tool-best-practice.md) for information on optimizing tool usage.

You can extend the capabilities of your Microsoft Foundry agent by adding an Agent2Agent (A2A) agent endpoint that supports the [A2A protocol](https://a2a-protocol.org/latest/). The A2A Tool enables agent-to-agent communication, making it easier to share context between Foundry agents and external agent endpoints through a standardized protocol. This guide shows you how to configure and use the A2A tool in your Foundry Agent Service.

Connecting agents via the A2A tool versus a multi-agent workflow:

- **Using the A2A tool**: When Agent A calls Agent B through the A2A tool, Agent B's answer goes back to Agent A. Agent A then summarizes the answer and generates a response for the user. Agent A keeps control and continues to handle future user input.
- **Using a multi-agent workflow**: When Agent A calls Agent B through a workflow or other multi-agent orchestration, Agent B takes full responsibility for answering the user. Agent A is out of the loop. Agent B handles all subsequent user input.

## Usage support

| Microsoft Foundry support  | Python SDK |	C# SDK | JavaScript SDK | Java SDK | REST API | Basic agent setup | Standard agent setup |
|---------|---------|---------|---------|---------|---------|---------|---------|
| ✔️  | ✔️ | ✔️ | ✔️ | - |  ✔️ | ✔️ | ✔️ | 

## Prerequisites

- An Azure subscription with an active Foundry project.
- A model deployment (for example, gpt-4) in your Foundry project.
- Required Azure role: Contributor or Owner on the Foundry project resource.
- SDK installation:
  - Python: `pip install azure-ai-projects[agents]` (latest prerelease)
  - C#: `Azure.AI.Projects` NuGet package
  - TypeScript: `@azure/ai-projects` npm package
- Environment variables configured:
  - `FOUNDRY_PROJECT_ENDPOINT`: Your project endpoint URL.
  - `FOUNDRY_MODEL_DEPLOYMENT_NAME`: Your model deployment name.
  - `A2A_PROJECT_CONNECTION_ID`: Your A2A connection ID.
- An A2A connection configured in your Foundry project. For REST API connection setup details, see [Create the remote A2A Foundry connection](#create-the-remote-a2a-foundry-connection).

## Sample code

> [!NOTE]
> You need the latest prerelease package. See the [quickstart](../../../../quickstarts/get-started-code.md?view=foundry&preserve-view=true#install-and-authenticate) for details.

:::zone pivot="python"
## Sample for use of an agent with Fabric Data Agent

```python
import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    PromptAgentDefinition,
    A2ATool,
)

load_dotenv()

endpoint = os.environ["FOUNDRY_PROJECT_ENDPOINT"]

with (
    DefaultAzureCredential() as credential,
    AIProjectClient(endpoint=endpoint, credential=credential) as project_client,
    project_client.get_openai_client() as openai_client,
):
    tool = A2ATool(
        project_connection_id=os.environ["A2A_PROJECT_CONNECTION_ID"],
    )

    agent = project_client.agents.create_version(
        agent_name="MyAgent",
        definition=PromptAgentDefinition(
            model=os.environ["FOUNDRY_MODEL_DEPLOYMENT_NAME"],
            instructions="You are a helpful assistant.",
            tools=[tool],
        ),
    )
    print(f"Agent created (id: {agent.id}, name: {agent.name}, version: {agent.version})")

    user_input = input("Enter your question (e.g., 'What can the secondary agent do?'): \n")

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
            item = event.item
            if item.type == "remote_function_call":  # TODO: support remote_function_call schema
                print(f"Call ID: {getattr(item, 'call_id')}")
                print(f"Label: {getattr(item, 'label')}")
        elif event.type == "response.completed":
            print(f"\nFollow-up completed!")
            print(f"Full response: {event.response.output_text}")

    print("\nCleaning up...")
    project_client.agents.delete_version(agent_name=agent.name, agent_version=agent.version)
    print("Agent deleted")
```

### Expected output

The agent responds with information about the secondary agent's capabilities, demonstrating successful A2A communication. You see streaming delta text as the response is generated, followed by completion messages. The output includes the follow-up response ID, text deltas, and a final summary of what the secondary agent can do.
:::zone-end

:::zone pivot="csharp"

## Sample for use of an agent with Fabric Data Agent

In the following scenario, you have an application endpoint that complies with A2A. Authentication happens through the header `x-api-key` value.

### Create a connection to A2A agent

Create the specialized A2A connection. If you use the Agent2Agent connection, you don't need to provide the endpoint because it already contains it.

1. Select **New foundry** at the top of the Microsoft Foundry UI.
1. Select **Tools** in the left panel.
1. Select **Connect tool** in the upper right corner.
1. In the open window, select the **Custom** tab.
1. Select **Agent2Agent (A2A)** and select **Create**.
1. Enter a **Name** and **A2A Agent Endpoint**. Don't change **Authentication** from "Key-based".
1. In the **Credential** section, set the key "x-api-key" with your secret key.

### Create and run the sample

To enable your agent communication to the A2A endpoint, use `A2ATool`.

```csharp
// Create an Agent client and read the environment variables, which will be used in the next steps.
var projectEndpoint = System.Environment.GetEnvironmentVariable("FOUNDRY_PROJECT_ENDPOINT");
var modelDeploymentName = System.Environment.GetEnvironmentVariable("FOUNDRY_MODEL_DEPLOYMENT_NAME");
var a2aConnectionName = System.Environment.GetEnvironmentVariable("A2A_PROJECT_CONNECTION_ID");
var a2aBaseUri = System.Environment.GetEnvironmentVariable("A2A_BASE_URI");

AIProjectClient projectClient = new(endpoint: new Uri(projectEndpoint), tokenProvider: new DefaultAzureCredential());

// Create the A2ATool and provide it with the A2A connection ID.
AIProjectConnection a2aConnection = projectClient.Connections.GetConnection(a2aConnectionName);
A2ATool a2aTool = new()
{
    ProjectConnectionId = a2aConnection.Id
};
if (!string.Equals(a2aConnection.Type.ToString(), "RemoteA2A"))
{
    if (a2aBaseUri is null)
    {
        throw new InvalidOperationException($"The connection {a2aConnection.Name} is of {a2aConnection.Type.ToString()} type and does not carry the A2A service base URI. Please provide this value through A2A_BASE_URI environment variable.");
    }
    // Provide the service endpoint as a baseUri parameter
    // if the connection is not of a RemoteA2A type.
    a2aTool.BaseUri = new Uri(a2aBaseUri);
}
PromptAgentDefinition agentDefinition = new(model: modelDeploymentName)
{
    Instructions = "You are a helpful assistant.",
    Tools = { a2aTool }
};
// Create the Agent version with the A2A tool.
AgentVersion agentVersion = projectClient.Agents.CreateAgentVersion(
    agentName: "myAgent",
    options: new(agentDefinition));

// Create the response and make sure we are always using tool.
ProjectResponsesClient responseClient = projectClient.OpenAI.GetProjectResponsesClientForAgent(agentVersion.Name);
CreateResponseOptions responseOptions = new()
{
    ToolChoice = ResponseToolChoice.CreateRequiredChoice(),
    InputItems = { ResponseItem.CreateUserMessageItem("What can the secondary agent do?") },
};
ResponseResult response = responseClient.CreateResponse(responseOptions);

// Print the Agent output.
Assert.That(response.Status, Is.EqualTo(ResponseStatus.Completed));
Console.WriteLine(response.GetOutputText());

// Clean up the created Agent version.
projectClient.Agents.DeleteAgentVersionAsync(agentName: agentVersion.Name, agentVersion: agentVersion.Version);
```

:::zone-end

:::zone pivot="rest-api"
## Create the remote A2A Foundry connection 

Use the following examples to store your authentication information.

### Key-based

```bash
curl --request PUT \
  --url 'https://{{region}}.management.azure.com/subscriptions/{{subscription_id}}//resourcegroups/{{resource_group_name}}/providers/Microsoft.CognitiveServices/accounts/{{foundry_account_name}}/projects/{{project_name}}/connections/{{connection_name}}?api-version=2025-04-01-preview' \
  --header 'Authorization: Bearer {{token against http://management.azure.com}}' \
  --header 'Content-Type: application/json' \
  --data '{
  "tags": null,
  "location": null,
  "type": "Microsoft.MachineLearningServices/workspaces/connections",
  "properties": {
    "authType": "CustomKeys",
    "group": "ServicesAndApps",
    "category": "RemoteA2A",
    "expiryTime": null,
    "target": "{{a2a_endpoint_endpoint}}",
    "isSharedToAll": true,
    "sharedUserList": [],
    "Credentials": {
      "Keys": {
        "{{key_name}}": "{{key_value}}"
      }
    },
    "metadata": {
      "ApiType": "Azure"
    }
  }
}'
```

### Managed OAuth Identity Passthrough

These options are only supported if you select the **managed oauth** option in Foundry Tool Catalog.

```bash
curl --request PUT \
  --url 'https://{{region}}.management.azure.com/subscriptions/{{subscription_id}}//resourcegroups/{{resource_group_name}}/providers/Microsoft.CognitiveServices/accounts/{{foundry_account_name}}/projects/{{project_name}}/connections/{{connection_name}}?api-version=2025-04-01-preview' \
  --header 'Authorization: Bearer {{token against http://management.azure.com}}' \
  --header 'Content-Type: application/json' \
  --header 'User-Agent: insomnia/11.6.2' \
  --data '{
  "tags": null,
  "location": null,
  "type": "Microsoft.MachineLearningServices/workspaces/connections",
  "properties": {
    "authType": "OAuth2",
    "group": "ServicesAndApps",
    "category": "RemoteA2A",
    "expiryTime": null,
    "target": "{{a2a_endpoint_endpoint}}",
    "isSharedToAll": true,
    "sharedUserList": [],
    "useCustomConnector": false,
    "connectorName": {{connector_name}}              
    "Credentials": {
    },
    "metadata": {
      "ApiType": "Azure"
    }
  }
}'
```

### Custom OAuth Identity Passthrough

Custom OAuth doesn't support the update operation. Create a new one if you want to update certain values. 

```bash
curl --request PUT \
  --url 'https://{{region}}.management.azure.com:443/subscriptions/{{subscription_id}}//resourcegroups/{{resource_group_name}}/providers/Microsoft.CognitiveServices/accounts/{{foundry_account_name}}/projects/{{project_name}}/connections/{{connection_name}}?api-version=2025-04-01-preview' \
  --header 'Authorization: Bearer {{token against http://management.azure.com}}' \
  --header 'Content-Type: application/json' \
  --header 'User-Agent: insomnia/11.6.2' \
  --data '{
  "tags": null,
  "location": null,
  "type": "Microsoft.MachineLearningServices/workspaces/connections",
  "properties": {
    "authType": "OAuth2",
    "group": "ServicesAndApps",
    "category": "RemoteA2A",
    "expiryTime": null,
    "target": "{{a2a_endpoint_endpoint}}",
    "isSharedToAll": true,
    "sharedUserList": [],
  "TokenUrl": "{{token_url}}",
  "AuthorizationUrl": "{{auth_url}}",
  "RefreshUrl": "{{refresh_url}}",
  "Scopes": [
        "{{scope}}"
    ],
    "Credentials": {
      "ClientId": "{{client_id}}",
            "ClientSecret": "{{client_secret_optional}}", //optional
    },
    "metadata": {
      "ApiType": "Azure"
    }
  }
}'
```

### Foundry Project Managed Identity

```bash
curl --request PUT \
  --url 'https://{{region}}.management.azure.com:443/subscriptions/{{subscription_id}}//resourcegroups/{{resource_group_name}}/providers/Microsoft.CognitiveServices/accounts/{{foundry_account_name}}/projects/{{project_name}}/connections/{{connection_name}}?api-version=2025-04-01-preview' \
  --header 'Authorization: Bearer {{token against http://management.azure.com}}' \
  --header 'Content-Type: application/json' \
  --header 'User-Agent: insomnia/11.6.2' \
  --data '{
  "tags": null,
  "location": null,
  "type": "Microsoft.MachineLearningServices/workspaces/connections",
  "properties": {
    "authType": "ProjectManagedIdentity",
    "group": "ServicesAndApps",
    "category": "RemoteA2A",
    "expiryTime": null,
    "target": "{{a2a_endpoint_endpoint}}",
    "isSharedToAll": true,
    "sharedUserList": [],
  "audience": "{{audience}}",
    "Credentials": {
    },
    "metadata": {
      "ApiType": "Azure"
    }
  }
}'
```

### Agent identity

```bash
curl --request PUT \
  --url 'https://{{region}}.management.azure.com:443/subscriptions/{{subscription_id}}//resourcegroups/{{resource_group_name}}/providers/Microsoft.CognitiveServices/accounts/{{foundry_account_name}}/projects/{{project_name}}/connections/{{connection_name}}?api-version=2025-04-01-preview' \
  --header 'Authorization: Bearer {{token against http://management.azure.com}}' \
  --header 'Content-Type: application/json' \
  --header 'User-Agent: insomnia/11.6.2' \
  --data '{
  "tags": null,
  "location": null,
  "type": "Microsoft.MachineLearningServices/workspaces/connections",
  "properties": {
    "authType": "AgenticIdentity",
    "group": "ServicesAndApps",
    "category": "RemoteA2A",
    "expiryTime": null,
    "target": "{{a2a_endpoint_endpoint}}",
    "isSharedToAll": true,
    "sharedUserList": [],
  "audience": "{{audience}}",
    "Credentials": {
    },
    "metadata": {
      "ApiType": "Azure"
    }
  }
}'
```

## Add A2A tool to Foundry Agent Service

### Create an agent version with the A2A tool

```bash
curl --request POST \
  --url $FOUNDRY_PROJECT_ENDPOINT/agents/$AGENTVERSION_NAME/versions?api-version=$API_VERSION \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{
  "description": "Test agent version description",
  "definition": {
    "kind": "prompt",
    "model": "{{model}}",
    "tools": [ 
      {
         "type": "a2a_preview",
         "base_url": "{{a2a_endpoint}}",
         "project_connection_id": "{{project_connection_name_above}}"
      }
    ],
    "instructions": "You are a helpful agent."
  }
}'
```
:::zone-end

:::zone pivot="typescript"

This sample demonstrates how to create an AI agent with A2A capabilities by using the `A2ATool` and synchronous Azure AI Projects client. The agent can communicate with other agents and provide responses based on inter-agent interactions by using the A2A protocol.

```typescript
import { DefaultAzureCredential } from "@azure/identity";
import { AIProjectClient } from "@azure/ai-projects";
import * as readline from "readline";
import "dotenv/config";

// Load environment variables
const projectEndpoint = process.env["FOUNDRY_PROJECT_ENDPOINT"] || "<project endpoint>";
const deploymentName = process.env["FOUNDRY_MODEL_DEPLOYMENT_NAME"] || "<model deployment name>";
const a2aProjectConnectionId =
  process.env["A2A_PROJECT_CONNECTION_ID"] || "<a2a project connection id>";

export async function main(): Promise<void> {
  const project = new AIProjectClient(projectEndpoint, new DefaultAzureCredential());
  const openAIClient = await project.getOpenAIClient();

  console.log("Creating agent with A2A tool...");

  // Create the agent with A2A tool
  const agent = await project.agents.createVersion("MyA2AAgent", {
    kind: "prompt",
    model: deploymentName,
    instructions: "You are a helpful assistant.",
    // Define A2A tool for agent-to-agent communication
    tools: [
      {
        type: "a2a_preview",
        project_connection_id: a2aProjectConnectionId,
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
    rl.question("Enter your question (e.g., 'What can the secondary agent do?'): \n", (answer) => {
      rl.close();
      resolve(answer);
    });
  });

  console.log("\nSending request to A2A agent with streaming...");
  const streamResponse = await openAIClient.responses.create(
    {
      input: userInput,
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
      const item = event.item as any;
      if (item.type === "remote_function_call") {
        // TODO: support remote_function_call schema
        const callId = item.call_id;
        const label = item.label;
        console.log(`Call ID: ${callId ?? "None"}`);
        console.log(`Label: ${label ?? "None"}`);
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

  console.log("\nAgent-to-Agent sample completed!");
}

main().catch((err) => {
  console.error("The sample encountered an error:", err);
});
```

:::zone-end

## Considerations for using non-Microsoft services and servers 

Your use of connected non-Microsoft services and servers ("non-Microsoft services") is subject to the terms between you and the service provider. Non-Microsoft services are non-Microsoft Products under your agreement governing use of Microsoft Online services. When you connect to a non-Microsoft service, you pass some of your data (such as prompt content) to the non-Microsoft services, or your application might receive data from the non-Microsoft services. You're responsible for your use of non-Microsoft services and data, along with any charges associated with that use. 

The non-Microsoft services, including A2A agent endpoints, that you decide to use with the A2A tool described in this article are created by third parties, not Microsoft. Microsoft didn't test or verify these A2A agent endpoints. Microsoft has no responsibility to you or others in relation to your use of any non-Microsoft services.  

Carefully review and track the A2A agent endpoints you add to Foundry Agent Service. Rely on endpoints hosted by trusted service providers themselves rather than proxies. 

The A2A tool allows you to pass custom headers, such as authentication keys or schemas, that an A2A agent endpoint might need. Review all data that you share with non-Microsoft services, including A2A agent endpoints, and log the data for auditing purposes. Be aware of non-Microsoft practices for retention and location of data. 
