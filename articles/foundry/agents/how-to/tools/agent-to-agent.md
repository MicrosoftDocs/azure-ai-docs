---
title: "Add an A2A agent endpoint to Foundry Agent Service"
description: "Add an Agent2Agent (A2A) endpoint to Foundry Agent Service for cross-agent communication. Configure connections, authentication, and SDK integration."
services: azure-ai-agent-service
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: how-to
ms.date: 03/30/2026
author: alvinashcraft
ms.author: aashcraft
ms.custom: azure-ai-agents, dev-focus, pilot-ai-workflow-jan-2026, doc-kit-assisted
ai-usage: ai-assisted
zone_pivot_groups: selection-agent-to-agent
---

# Add an A2A agent endpoint to Foundry Agent Service (preview)
[!INCLUDE [feature-preview](../../../includes/feature-preview.md)]

> [!NOTE]
> For information on optimizing tool usage, see [best practices](../../concepts/tool-best-practice.md).

You can extend the capabilities of your Microsoft Foundry agent by adding an Agent2Agent (A2A) agent endpoint that supports the [A2A protocol](https://a2a-protocol.org/latest/). The A2A tool enables agent-to-agent communication, making it easier to share context between Foundry agents and external agent endpoints through a standardized protocol. This guide shows you how to configure and use the A2A tool in your Foundry Agent Service.

Connecting agents via the A2A tool versus a multi-agent workflow:

- **Using the A2A tool**: When Agent A calls Agent B through the A2A tool, Agent B's answer goes back to Agent A. Agent A then summarizes the answer and generates a response for the user. Agent A keeps control and continues to handle future user input.
- **Using a multi-agent workflow**: When Agent A calls Agent B through a workflow or other multi-agent orchestration, Agent B takes full responsibility for answering the user. Agent A is out of the loop. Agent B handles all subsequent user input. For more information, see [Build a workflow in Microsoft Foundry](../../concepts/workflow.md).

## Usage support

The following table shows SDK and setup support. ✔️ (GA) indicates general availability, ✔️ (Preview) indicates public preview, and a dash (-) indicates the feature isn't available.

| Microsoft Foundry support | Python SDK | C# SDK | JavaScript SDK | Java SDK | REST API | Basic agent setup | Standard agent setup |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ✔️ | ✔️ (GA) | ✔️ (Preview) | ✔️ (GA) | ✔️ (GA) | ✔️ (GA) | ✔️ | ✔️ |

## Prerequisites

- An Azure subscription with an active Foundry project.
- A model deployment (for example, `gpt-4.1-mini`) in your Foundry project.
- Required Azure role: On the Foundry resource, **Contributor** or **Owner** for management and **Azure AI User** for building an agent.
- SDK installation:
  - Python (GA): `pip install "azure-ai-projects>=2.0.0"`
  - C# (Preview): `Azure.AI.Projects` prerelease NuGet package
  - TypeScript (GA): `@azure/ai-projects` npm package
  - Java: `com.azure:azure-ai-agents:2.0.0` Maven dependency
- Values to update in code:
  - Project endpoint URL (for example, `https://<resource>.ai.azure.com/api/projects/<project>`).
  - Model deployment name (for example, `gpt-4.1-mini`).
  - A2A connection name (created in the Foundry portal).
  - A2A base URI (optional, only needed for non-`RemoteA2A` connections).
- An A2A connection configured in your Foundry project. For connection setup and REST examples, see [Create an A2A connection](#create-an-a2a-connection).

## Create an A2A connection

Create a project connection for your A2A endpoint so you can store authentication securely and reuse it across agent versions.

For details about supported authentication approaches, see [Agent2Agent (A2A) authentication](../../concepts/agent-to-agent-authentication.md).

### Create the connection in the Foundry portal

1. [!INCLUDE [foundry-sign-in](../../../includes/foundry-sign-in.md)]
1. Select **Tools**.
1. Select **Connect tool**.
1. Select the **Custom** tab.
1. Select **Agent2Agent (A2A)**, and then select **Create**.
1. Enter a **Name** and an **A2A Agent Endpoint**.
1. Under **Authentication**, select an authentication method. For key-based authentication, set the credential name (for example, `x-api-key`) and the corresponding secret value.

### Get the connection identifier for code

Use your connection name in code. Your code uses this name to retrieve the full connection ID at runtime:

- **Python/C#/TypeScript**: Call `project.connections.get(connection_name)` to get the connection object, then access `connection.id`.
- **REST API**: Include the connection ID in the `project_connection_id` field of the A2A tool definition.

## Code example

> [!NOTE]
> The .NET SDK is currently in preview. See the [quickstart](../../../quickstarts/get-started-code.md) for details.

:::zone pivot="python"
## Create an agent with the A2A tool

```python
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    PromptAgentDefinition,
    A2APreviewTool,
)

# Format: "https://resource_name.ai.azure.com/api/projects/project_name"
PROJECT_ENDPOINT = "your_project_endpoint"
A2A_CONNECTION_NAME = "my-a2a-connection"
AGENT_NAME = "my-agent"

# Create clients to call Foundry API
project = AIProjectClient(
    endpoint=PROJECT_ENDPOINT,
    credential=DefaultAzureCredential(),
)
openai = project.get_openai_client()

a2a_connection = project.connections.get(A2A_CONNECTION_NAME)

tool = A2APreviewTool(
    project_connection_id=a2a_connection.id,
)

agent = project.agents.create_version(
    agent_name=AGENT_NAME,
    definition=PromptAgentDefinition(
        model="gpt-4.1-mini",
        instructions="You are a helpful assistant.",
        tools=[tool],
    ),
)
print(f"Agent created (id: {agent.id}, name: {agent.name}, version: {agent.version})")

user_input = input("Enter your question (e.g., 'What can the secondary agent do?'): \n")

stream_response = openai.responses.create(
    stream=True,
    tool_choice="required",
    input=user_input,
    extra_body={"agent_reference": {"name": agent.name, "type": "agent_reference"}},
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
        if item.type == "remote_function_call":
            print(f"Call ID: {getattr(item, 'call_id')}")
            print(f"Label: {getattr(item, 'label')}")
    elif event.type == "response.completed":
        print(f"\nFollow-up completed!")
        print(f"Full response: {event.response.output_text}")

# Clean up the created agent version
project.agents.delete_version(agent_name=agent.name, agent_version=agent.version)
```

### Expected output

The agent responds with information about the secondary agent's capabilities, demonstrating successful A2A communication. You see streaming delta text as the response is generated, followed by completion messages. The output includes the follow-up response ID, text deltas, and a final summary of what the secondary agent can do.
:::zone-end

:::zone pivot="csharp"

## Create an agent with the A2A tool

This example creates an agent that can call a remote A2A endpoint. For the connection setup steps, see [Create an A2A connection](#create-an-a2a-connection).

```csharp
using System;
using Azure.AI.Projects;
using Azure.AI.Extensions.OpenAI;
using Azure.Identity;

var projectEndpoint = "https://<resource>.ai.azure.com/api/projects/<project>";
var a2aConnectionName = "my-a2a-connection";
var a2aBaseUri = "https://<a2a-endpoint>"; // Optional for non-RemoteA2A connections.

AIProjectClient projectClient = new(endpoint: new Uri(projectEndpoint), tokenProvider: new DefaultAzureCredential());

// Create the A2ATool and provide it with the A2A connection ID.
AIProjectConnection a2aConnection = projectClient.Connections.GetConnection(connectionName: a2aConnectionName);
A2APreviewTool a2aTool = new()
{
    ProjectConnectionId = a2aConnection.Id
};
if (!string.Equals(a2aConnection.Type.ToString(), "RemoteA2A"))
{
  if (string.IsNullOrWhiteSpace(a2aBaseUri))
    {
    throw new InvalidOperationException($"The connection {a2aConnection.Name} is of {a2aConnection.Type.ToString()} type and does not carry the A2A service base URI. Set a2aBaseUri before running this sample.");
    }
    // Provide the service endpoint as a baseUri parameter
    // if the connection is not of a RemoteA2A type.
    a2aTool.BaseUri = new Uri(a2aBaseUri);
}
PromptAgentDefinition agentDefinition = new(model: "gpt-4.1-mini")
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
if (response.Status != ResponseStatus.Completed)
{
    throw new InvalidOperationException($"Response did not complete. Status: {response.Status}");
}
Console.WriteLine(response.GetOutputText());

// Clean up the created Agent version.
projectClient.Agents.DeleteAgentVersion(agentName: agentVersion.Name, agentVersion: agentVersion.Version);
```

### Expected output

The console displays the agent's response text from the A2A endpoint. After completion, the agent version is deleted to clean up resources.
:::zone-end

:::zone pivot="rest-api"
## Create an A2A connection by using the REST API

Use these examples to create a project connection that stores your authentication information.

To get an access token for the Azure Resource Manager endpoint:

```azurecli
az account get-access-token --scope https://management.azure.com/.default --query accessToken -o tsv
```

### Key-based

```bash
curl --request PUT \
  --url 'https://management.azure.com/subscriptions/{{subscription_id}}/resourceGroups/{{resource_group_name}}/providers/Microsoft.CognitiveServices/accounts/{{foundry_account_name}}/projects/{{project_name}}/connections/{{connection_name}}?api-version=2025-04-01-preview' \
  --header 'Authorization: Bearer {{token}}' \
  --header 'Content-Type: application/json' \
  --data '{
    "tags": null,
    "location": null,
    "name": "{{connection_name}}",
    "type": "Microsoft.MachineLearningServices/workspaces/connections",
    "properties": {
      "authType": "CustomKeys",
      "group": "ServicesAndApps",
      "category": "RemoteA2A",
      "expiryTime": null,
      "target": "{{a2a_endpoint}}",
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

This option is supported when you select **Managed OAuth** in the Foundry tool catalog.

```bash
curl --request PUT \
  --url 'https://management.azure.com/subscriptions/{{subscription_id}}/resourceGroups/{{resource_group_name}}/providers/Microsoft.CognitiveServices/accounts/{{foundry_account_name}}/projects/{{project_name}}/connections/{{connection_name}}?api-version=2025-04-01-preview' \
  --header 'Authorization: Bearer {{token}}' \
  --header 'Content-Type: application/json' \
  --data '{
    "tags": null,
    "location": null,
    "name": "{{connection_name}}",
    "type": "Microsoft.MachineLearningServices/workspaces/connections",
    "properties": {
      "authType": "OAuth2",
      "group": "ServicesAndApps",
      "category": "RemoteA2A",
      "expiryTime": null,
      "target": "{{a2a_endpoint}}",
      "isSharedToAll": true,
      "sharedUserList": [],
      "useCustomConnector": false,
      "connectorName": "{{connector_name}}",
      "Credentials": {},
      "metadata": {
        "ApiType": "Azure"
      }
    }
  }'
```

### Custom OAuth Identity Passthrough

Custom OAuth doesn't support the update operation. Create a new connection if you want to update certain values.

If your OAuth app doesn't require a client secret, omit `ClientSecret`.

```bash
curl --request PUT \
  --url 'https://management.azure.com/subscriptions/{{subscription_id}}/resourceGroups/{{resource_group_name}}/providers/Microsoft.CognitiveServices/accounts/{{foundry_account_name}}/projects/{{project_name}}/connections/{{connection_name}}?api-version=2025-04-01-preview' \
  --header 'Authorization: Bearer {{token}}' \
  --header 'Content-Type: application/json' \
  --data '{
    "tags": null,
    "location": null,
    "name": "{{connection_name}}",
    "type": "Microsoft.MachineLearningServices/workspaces/connections",
    "properties": {
      "authType": "OAuth2",
      "group": "ServicesAndApps",
      "category": "RemoteA2A",
      "expiryTime": null,
      "target": "{{a2a_endpoint}}",
      "isSharedToAll": true,
      "sharedUserList": [],
      "TokenUrl": "{{token_url}}",
      "AuthorizationUrl": "{{authorization_url}}",
      "RefreshUrl": "{{refresh_url}}",
      "Scopes": [
        "{{scope}}"
      ],
      "Credentials": {
        "ClientId": "{{client_id}}",
        "ClientSecret": "{{client_secret}}"
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
  --url 'https://management.azure.com/subscriptions/{{subscription_id}}/resourceGroups/{{resource_group_name}}/providers/Microsoft.CognitiveServices/accounts/{{foundry_account_name}}/projects/{{project_name}}/connections/{{connection_name}}?api-version=2025-04-01-preview' \
  --header 'Authorization: Bearer {{token}}' \
  --header 'Content-Type: application/json' \
  --data '{
    "tags": null,
    "location": null,
    "name": "{{connection_name}}",
    "type": "Microsoft.MachineLearningServices/workspaces/connections",
    "properties": {
      "authType": "ProjectManagedIdentity",
      "group": "ServicesAndApps",
      "category": "RemoteA2A",
      "expiryTime": null,
      "target": "{{a2a_endpoint}}",
      "isSharedToAll": true,
      "sharedUserList": [],
      "audience": "{{audience}}",
      "Credentials": {},
      "metadata": {
        "ApiType": "Azure"
      }
    }
  }'
```

### Agent identity

```bash
curl --request PUT \
  --url 'https://management.azure.com/subscriptions/{{subscription_id}}/resourceGroups/{{resource_group_name}}/providers/Microsoft.CognitiveServices/accounts/{{foundry_account_name}}/projects/{{project_name}}/connections/{{connection_name}}?api-version=2025-04-01-preview' \
  --header 'Authorization: Bearer {{token}}' \
  --header 'Content-Type: application/json' \
  --data '{
    "tags": null,
    "location": null,
    "name": "{{connection_name}}",
    "type": "Microsoft.MachineLearningServices/workspaces/connections",
    "properties": {
      "authType": "AgenticIdentity",
      "group": "ServicesAndApps",
      "category": "RemoteA2A",
      "expiryTime": null,
      "target": "{{a2a_endpoint}}",
      "isSharedToAll": true,
      "sharedUserList": [],
      "audience": "{{audience}}",
      "Credentials": {},
      "metadata": {
        "ApiType": "Azure"
      }
    }
  }'
```

## Add A2A tool to Foundry Agent Service

Get an access token:

```azurecli
az account get-access-token --scope https://ai.azure.com/.default --query accessToken -o tsv
```

Use that token as `{{agent_token}}` in the request.

### Create an agent version with the A2A tool

```bash
curl --request POST \
  --url '{{project_endpoint}}/agents/{{agent_name}}/versions?api-version=v1' \
  -H 'Authorization: Bearer {{agent_token}}' \
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
         "project_connection_id": "{{project_connection_id}}"
      }
    ],
    "instructions": "You are a helpful agent."
  }
}'
```

To delete an agent version, send a `DELETE` request to the same endpoint with the agent name and version.
:::zone-end

:::zone pivot="typescript"

This sample demonstrates how to create an AI agent with A2A capabilities by using the `A2ATool` and the Azure AI Projects client. The agent can communicate with other agents and provide responses based on inter-agent interactions by using the A2A protocol.

```typescript
import { DefaultAzureCredential } from "@azure/identity";
import { AIProjectClient } from "@azure/ai-projects";
import * as readline from "readline";

const PROJECT_ENDPOINT = "https://<resource>.ai.azure.com/api/projects/<project>";
const A2A_CONNECTION_NAME = "my-a2a-connection";

export async function main(): Promise<void> {
  const project = new AIProjectClient(PROJECT_ENDPOINT, new DefaultAzureCredential());
  const openAIClient = project.getOpenAIClient();

  // Get the A2A connection by name to retrieve its ID
  const a2aConnection = await project.connections.get(A2A_CONNECTION_NAME);

  // Create the agent with A2A tool
  const agent = await project.agents.createVersion("MyA2AAgent", {
    kind: "prompt",
    model: "gpt-4.1-mini",
    instructions: "You are a helpful assistant.",
    // Define A2A tool for agent-to-agent communication
    tools: [
      {
        type: "a2a_preview",
        project_connection_id: a2aConnection.id,
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

  // Send request and stream the response
  const streamResponse= await openAIClient.responses.create(
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
        // Add your handling logic for remote function call items here
        const callId = item.call_id;
        const label = item.label;
        console.log(`Call ID: ${callId ?? "None"}`);
        console.log(`Label: ${label ?? "None"}`);
      }
    } else if (event.type === "response.completed") {
      console.log("\nFollow-up completed!");
    }
  }

  // Clean up the created agent version
  await project.agents.deleteVersion(agent.name, agent.version);
}

main().catch((err) => {
  console.error("The sample encountered an error:", err);
});
```

### Expected output

The console displays streamed response text as the A2A agent processes the request. You see the follow-up response ID, text deltas printed to stdout, and completion messages. The agent version is deleted after the interaction completes.
:::zone-end

:::zone pivot="java"

## Use agent-to-agent communication in Java

Update these values in the sample:

- `projectEndpoint` — Your project endpoint.
- `model` — A deployed model name.
- `a2aConnectionId` — The ID of the A2A connection in your Foundry project.

Add the dependency to your `pom.xml`:

```xml
<dependency>
    <groupId>com.azure</groupId>
    <artifactId>azure-ai-agents</artifactId>
    <version>2.0.0</version>
</dependency>
```

### Create agents with agent-to-agent tool

```java
import com.azure.ai.agents.AgentsClient;
import com.azure.ai.agents.AgentsClientBuilder;
import com.azure.ai.agents.ResponsesClient;
import com.azure.ai.agents.models.AgentReference;
import com.azure.ai.agents.models.AgentVersionDetails;
import com.azure.ai.agents.models.A2APreviewTool;
import com.azure.ai.agents.models.AzureCreateResponseOptions;
import com.azure.ai.agents.models.PromptAgentDefinition;
import com.azure.identity.DefaultAzureCredentialBuilder;
import com.openai.models.responses.Response;
import com.openai.models.responses.ResponseCreateParams;

import java.util.Collections;

public class AgentToAgentExample {
    public static void main(String[] args) {
        String projectEndpoint = "https://<resource>.ai.azure.com/api/projects/<project>";
        String a2aConnectionId = "<a2a-connection-id>";

        AgentsClientBuilder builder = new AgentsClientBuilder()
            .credential(new DefaultAzureCredentialBuilder().build())
            .endpoint(projectEndpoint);

        AgentsClient agentsClient = builder.buildAgentsClient();
        ResponsesClient responsesClient = builder.buildResponsesClient();

        // Create agent-to-agent tool with connection ID
        A2APreviewTool a2aTool = new A2APreviewTool()
            .setProjectConnectionId(a2aConnectionId);

        // Create agent with agent-to-agent tool
        PromptAgentDefinition agentDefinition = new PromptAgentDefinition("gpt-4.1-mini")
            .setInstructions("You are a coordinator agent that can communicate with other agents.")
            .setTools(Collections.singletonList(a2aTool));

        AgentVersionDetails agent = agentsClient.createAgentVersion("a2a-agent", agentDefinition);
        System.out.printf("Agent created: %s (version %s)%n", agent.getName(), agent.getVersion());

        // Create a response
        AgentReference agentReference = new AgentReference(agent.getName())
            .setVersion(agent.getVersion());

        Response response = responsesClient.createAzureResponse(
            new AzureCreateResponseOptions().setAgentReference(agentReference),
            ResponseCreateParams.builder()
                .input("What can the secondary agent do?"));

        System.out.println("Response: " + response.output());

        // Clean up
        agentsClient.deleteAgentVersion(agent.getName(), agent.getVersion());
    }
}
```

:::zone-end

## Troubleshooting

| Issue | Cause | Resolution |
| --- | --- | --- |
| Agent doesn't invoke the A2A tool | Agent definition doesn't include A2A tool configuration | Confirm your agent definition includes the A2A tool and that you configured the connection. If you're using responses, confirm you're not forcing a different tool. |
| Agent doesn't invoke the A2A tool | Prompt doesn't require remote agent | Update your prompt to require calling the remote agent, or remove conflicting tool choice settings. |
| Authentication failures (401 or 403) | Connection authentication type mismatch | Confirm the connection's authentication type matches your endpoint requirements. For key-based auth, confirm the credential name matches what the endpoint expects (`x-api-key` or `Authorization`). |
| SDK sample can't find the connection | Connection name mismatch | Confirm the connection name in code matches the connection name in Foundry. |
| Network or TLS errors | Endpoint unreachable or invalid certificate | Confirm the endpoint is publicly reachable and uses a valid TLS certificate. Check firewall rules and proxy settings. |
| Remote agent returns unexpected response | Response format incompatibility | Confirm the remote agent follows A2A protocol specifications. Check that response content types match expected formats. |
| Connection timeout | Remote agent slow to respond | Increase timeout settings or verify the remote agent's performance. Consider implementing retry logic with exponential backoff. |
| Missing A2A tool in response | Tool not enabled for the agent | Recreate the agent with the A2A tool explicitly enabled, and verify the connection is active and properly configured. |

<!-- The verbiage in the following section is required. Do not remove or modify. -->
## Considerations for using non-Microsoft services

You're subject to the terms between you and the service provider when you use connected non-Microsoft services and servers ("non-Microsoft services"). Under your agreement governing use of Microsoft Online services, non-Microsoft services are non-Microsoft Products. When you connect to a non-Microsoft service, you pass some of your data (such as prompt content) to the non-Microsoft services, or your application might receive data from the non-Microsoft services. You're responsible for your use of non-Microsoft services and data, along with any charges associated with that use. 

Third parties, not Microsoft, create the non-Microsoft services, including A2A agent endpoints, that you decide to use with the A2A tool described in this article. Microsoft didn't test or verify these A2A agent endpoints. Microsoft has no responsibility to you or others in relation to your use of any non-Microsoft services.  

Carefully review and track the A2A agent endpoints you add to Foundry Agent Service. Rely on endpoints hosted by trusted service providers themselves rather than proxies. 

The A2A tool allows you to pass custom headers, such as authentication keys or schemas, that an A2A agent endpoint might need. Review all data that you share with non-Microsoft services, including A2A agent endpoints, and log the data for auditing purposes. Be aware of non-Microsoft practices for retention and location of data. 

## Related content

- [Agent2Agent (A2A) authentication](../../concepts/agent-to-agent-authentication.md)
- [Build a workflow in Microsoft Foundry](../../concepts/workflow.md)
- [Best practices for tools](../../concepts/tool-best-practice.md)
- [Foundry project REST API (preview)](../../../reference/foundry-project-rest-preview.md)
