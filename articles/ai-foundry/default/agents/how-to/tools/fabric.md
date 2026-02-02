---
title: Use the Microsoft Fabric data agent with Foundry agents
titleSuffix: Microsoft Foundry
description: Learn how to connect a Microsoft Fabric data agent to Foundry Agent Service so your agent can analyze enterprise data by using identity passthrough.
author: alvinashcraft
ms.author: aashcraft
manager: nitinme
ms.date: 01/20/2026
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: how-to
ms.custom:
  - build-2025
  - dev-focus
  - pilot-ai-workflow-jan-2026
zone_pivot_groups: selection-fabric-tool
ai-usage: ai-assisted
---

# Use the Microsoft Fabric data agent (preview)

[!INCLUDE [feature-preview](../../../../includes/feature-preview.md)]

> [!NOTE]
> See [best practices](../../concepts/tool-best-practice.md) for information on optimizing tool usage.

Use the [**Microsoft Fabric data agent**](https://go.microsoft.com/fwlink/?linkid=2312815) with Foundry Agent Service to analyze enterprise data in chat. The Fabric data agent turns enterprise data into a conversational question and answer experience.

First, build and publish a Fabric data agent. Then, connect your Fabric data agent with the published endpoint. When a user sends a query, the agent determines if it should use the Fabric data agent. If so, it uses the end user's identity to generate queries over data they have access to. Lastly, the agent generates responses based on queries returned from Fabric data agents. By using Identity Passthrough (On-Behalf-Of) authorization, this integration simplifies access to enterprise data in Fabric while maintaining robust security, ensuring proper access control and enterprise-grade protection.

### Usage support

| Microsoft Foundry support | Python SDK | C# SDK | JavaScript SDK | Java SDK | REST API | Basic agent setup | Standard agent setup |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ✔️ | ✔️ | ✔️ | ✔️ | - | ✔️ | ✔️ | ✔️ |

## Prerequisites

> [!NOTE]
> - The model you select during agent setup is only used for orchestration and response generation. It doesn't affect which model the Fabric data agent uses for NL2SQL.
> - To help your agent invoke the Fabric tool reliably, include clear tool guidance in your agent instructions (for example, "For customer and product sales data, use the Fabric tool"). You can also force tool use with `tool_choice`.

- Create and publish a [Fabric data agent](https://go.microsoft.com/fwlink/?linkid=2312910).
- Assign developers and end users at least the `Azure AI User` Azure RBAC role. For more information, see [Azure role-based access control in Foundry](../../../../concepts/rbac-foundry.md).
- Give developers and end users at least `READ` access to the Fabric data agent and the underlying data sources it connects to.
- Ensure your Fabric data agent and Foundry project are in the same tenant.
- Use user identity authentication. Service principal authentication isn't supported for the Fabric data agent.
- Get these values before you run the samples:
  - Your Foundry project endpoint: `AZURE_AI_PROJECT_ENDPOINT`.
  - Your model deployment name: `AZURE_AI_MODEL_DEPLOYMENT_NAME`.
  - Your Fabric connection ID (project connection ID): `FABRIC_PROJECT_CONNECTION_ID`.
- For the REST sample, also set:
  - `API_VERSION`.
  - `AGENT_TOKEN` (a bearer token). You can get a temporary token with Azure CLI:

    ```azurecli
    az account get-access-token --scope https://ai.azure.com/.default
    ```

  ## Set up the Microsoft Fabric connection

  Before you run the samples, create a project connection to your Fabric data agent.

  1. In Microsoft Fabric, open your data agent.
  1. Copy the `workspace_id` and `artifact_id` values from the URL.

    The URL path looks similar to `.../groups/<workspace_id>/aiskills/<artifact_id>...`. Both values are GUIDs.

  1. In the Foundry portal, open your project.
  1. In the left pane, select **Management center**, and then select **Connected resources**.
  1. Create a connection of type **Microsoft Fabric**.
  1. Enter the `workspace_id` and `artifact_id` values.
  1. Save the connection, and then copy the connection **ID**.

    Use the connection ID as the value for `FABRIC_PROJECT_CONNECTION_ID`. The value looks like `/subscriptions/<subscriptionId>/resourceGroups/<resourceGroupName>/providers/Microsoft.CognitiveServices/accounts/<foundryAccountName>/projects/<foundryProjectName>/connections/<connectionName>`.

  ## Identity passthrough and access control

  This integration uses identity passthrough (On-Behalf-Of). The Fabric tool runs queries by using the identity of the signed-in user.

  - Give each end user access to the Fabric data agent and its underlying data sources, or the tool call fails.
  - Use user identity authentication. Service principal authentication isn't supported for the Fabric data agent.
  - For more information about how agent identity works, see [Agent identity](../../concepts/agent-identity.md).

## Code example

> [!NOTE]
> - To run this code, you need the latest prerelease package. For more information, see [Get ready to code](../../../../quickstarts/get-started-code.md#get-ready-to-code).
> - Your connection ID should be in the format of `/subscriptions/{{subscriptionID}}/resourceGroups/{{resourceGroupName}}/providers/Microsoft.CognitiveServices/accounts/{{foundryAccountName}}/projects/{{foundryProjectName}}/connections/{{foundryConnectionName}}`.

:::zone pivot="python"

### Quick verification

Before running the full sample, verify your Fabric connection exists:

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
    
    # Verify Fabric connection exists
    connection_name = os.environ.get("FABRIC_PROJECT_CONNECTION_NAME")
    if connection_name:
        try:
            conn = project_client.connections.get(connection_name)
            print(f"Fabric connection verified: {conn.name}")
            print(f"Connection ID: {conn.id}")
        except Exception as e:
            print(f"Fabric connection '{connection_name}' not found: {e}")
    else:
        # List available connections to help find the right one
        print("FABRIC_PROJECT_CONNECTION_NAME not set. Available connections:")
        for conn in project_client.connections.list():
            print(f"  - {conn.name}")
```

If this code runs without errors, your credentials and Fabric connection are configured correctly.

### Full sample

```python
import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    PromptAgentDefinition,
    MicrosoftFabricAgentTool,
    FabricDataAgentToolParameters,
    ToolProjectConnection,
)

load_dotenv()

with (
    DefaultAzureCredential() as credential,
    AIProjectClient(endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"], credential=credential) as project_client,
    project_client.get_openai_client() as openai_client,
):
    # Get connection ID from connection name
    fabric_connection = project_client.connections.get(
        os.environ["FABRIC_PROJECT_CONNECTION_NAME"],
    )
    print(f"Fabric connection ID: {fabric_connection.id}")

    agent = project_client.agents.create_version(
        agent_name="MyAgent",
        definition=PromptAgentDefinition(
            model=os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
            instructions="You are a helpful assistant.",
            tools=[
                MicrosoftFabricAgentTool(
                    fabric_dataagent_preview=FabricDataAgentToolParameters(
                        project_connections=[
                            ToolProjectConnection(project_connection_id=fabric_connection.id)
                        ]
                    )
                )
            ],
        ),
    )
    print(f"Agent created (id: {agent.id}, name: {agent.name}, version: {agent.version})")

    user_input = input("Enter your question for Fabric (e.g., 'Tell me about sales records'): \n")

    response = openai_client.responses.create(
        tool_choice="required",
        input=user_input,
        extra_body={"agent": {"name": agent.name, "type": "agent_reference"}},
    )

    print(f"Response output: {response.output_text}")
```

### What this code does

1. Creates an `AIProjectClient` using `DefaultAzureCredential`.
1. Creates an agent version configured with the Fabric data agent tool.
1. Prompts you for a question.
1. Calls the Responses API with `tool_choice="required"` to force tool use.
1. Prints the agent response.

### Required inputs

- Environment variables: `AZURE_AI_PROJECT_ENDPOINT`, `AZURE_AI_MODEL_DEPLOYMENT_NAME`, `FABRIC_PROJECT_CONNECTION_ID`.
- Authentication: `DefaultAzureCredential` must be able to obtain a token (for example, via `az login`).

### Expected output

- A line confirming agent creation.
- A line that starts with `Response output:` followed by the response text.

For more details, see the [full Python sample for Fabric data agent](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-agents/samples/agents_tools/sample_agents_fabric.py).
:::zone-end

:::zone pivot="csharp"

### Quick verification

Before running the full sample, verify your Fabric connection exists:

```csharp
using Azure.AI.Projects;
using Azure.Identity;

var projectEndpoint = System.Environment.GetEnvironmentVariable("AZURE_AI_PROJECT_ENDPOINT");
var fabricConnectionName = System.Environment.GetEnvironmentVariable("FABRIC_PROJECT_CONNECTION_NAME");

AIProjectClient projectClient = new(endpoint: new Uri(projectEndpoint), tokenProvider: new DefaultAzureCredential());

// Verify Fabric connection exists
try
{
    AIProjectConnection conn = projectClient.Connections.GetConnection(connectionName: fabricConnectionName);
    Console.WriteLine($"Fabric connection verified: {conn.Name}");
    Console.WriteLine($"Connection ID: {conn.Id}");
}
catch (Exception ex)
{
    Console.WriteLine($"Fabric connection '{fabricConnectionName}' not found: {ex.Message}");
    // List available connections
    Console.WriteLine("Available connections:");
    foreach (var conn in projectClient.Connections.GetConnections())
    {
        Console.WriteLine($"  - {conn.Name}");
    }
}
```

If this code runs without errors, your credentials and Fabric connection are configured correctly.

### Full sample

To enable your agent to access the Fabric data agent, use `MicrosoftFabricAgentTool`.

```csharp
// Create an Agent client and read the environment variables, which will be used in the next steps.
var projectEndpoint = System.Environment.GetEnvironmentVariable("AZURE_AI_PROJECT_ENDPOINT");
var modelDeploymentName = System.Environment.GetEnvironmentVariable("AZURE_AI_MODEL_DEPLOYMENT_NAME");
var fabricConnectionName = System.Environment.GetEnvironmentVariable("FABRIC_PROJECT_CONNECTION_NAME");
AIProjectClient projectClient = new(endpoint: new Uri(projectEndpoint), tokenProvider: new DefaultAzureCredential());

// Get connection ID from connection name
AIProjectConnection fabricConnection = projectClient.Connections.GetConnection(connectionName: fabricConnectionName);

FabricDataAgentToolOptions fabricToolOption = new()
{
  ProjectConnections = { new ToolProjectConnection(projectConnectionId: fabricConnection.Id) }
};
PromptAgentDefinition agentDefinition = new(model: modelDeploymentName)
{
    Instructions = "You are a helpful assistant.",
    Tools = { new MicrosoftFabricAgentTool(fabricToolOption), }
};
AgentVersion agentVersion = projectClient.Agents.CreateAgentVersion(
    agentName: "myAgent",
    options: new(agentDefinition));

// Create the response and make sure we are always using tool.
ProjectResponsesClient responseClient = projectClient.OpenAI.GetProjectResponsesClientForAgent(agentVersion.Name);
ResponseCreationOptions responseOptions = new()
{
    ToolChoice = ResponseToolChoice.CreateRequiredChoice()
};
OpenAIResponse response = responseClient.CreateResponse("What was the number of public holidays in Norway in 2024?", options: responseOptions);

// Print the Agent output.
Assert.That(response.Status, Is.EqualTo(ResponseStatus.Completed));
Console.WriteLine(response.GetOutputText());

// Delete the Agent version to clean up resources.
projectClient.Agents.DeleteAgentVersion(agentName: agentVersion.Name, agentVersion: agentVersion.Version);
```

### What this code does

1. Creates an `AIProjectClient` using `DefaultAzureCredential`.
1. Configures the Fabric data agent tool by using your project connection ID.
1. Creates an agent version.
1. Sends a question through the agent and forces tool usage.
1. Writes the response text and deletes the agent version.

### Required inputs

- Environment variables: `AZURE_AI_PROJECT_ENDPOINT`, `AZURE_AI_MODEL_DEPLOYMENT_NAME`, `FABRIC_PROJECT_CONNECTION_ID`.
- Authentication: `DefaultAzureCredential` must be able to obtain a token (for example, via `az login`).

### Expected output

- The response text printed to the console. For the sample question, the response should include the number of public holidays (for example, `62`).
:::zone-end

:::zone pivot="typescript"

### Quick verification

Before running the full sample, verify your Fabric connection exists:

```typescript
import { DefaultAzureCredential } from "@azure/identity";
import { AIProjectClient } from "@azure/ai-projects";
import "dotenv/config";

const projectEndpoint = process.env["AZURE_AI_PROJECT_ENDPOINT"] || "<project endpoint>";
const fabricConnectionName = process.env["FABRIC_PROJECT_CONNECTION_NAME"] || "<fabric connection name>";

async function verifyConnection(): Promise<void> {
  const project = new AIProjectClient(projectEndpoint, new DefaultAzureCredential());
  console.log("Connected to project.");

  try {
    const conn = await project.connections.get(fabricConnectionName);
    console.log(`Fabric connection verified: ${conn.name}`);
    console.log(`Connection ID: ${conn.id}`);
  } catch (error) {
    console.log(`Fabric connection '${fabricConnectionName}' not found: ${error}`);
    // List available connections
    console.log("Available connections:");
    for await (const conn of project.connections.list()) {
      console.log(`  - ${conn.name}`);
    }
  }
}

verifyConnection().catch(console.error);
```

If this code runs without errors, your credentials and Fabric connection are configured correctly.

### Full sample

The following TypeScript example demonstrates how to create an AI agent with Microsoft Fabric capabilities by using the `MicrosoftFabricAgentTool` and synchronous Azure AI Projects client. The agent can query Fabric data sources and provide responses based on data analysis. For a JavaScript version of this sample, see the [JavaScript sample for Fabric data agent](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/ai/ai-projects/samples/v2-beta/javascript/agents/tools/agentFabric.js) in the Azure SDK for JavaScript repository on GitHub.

```typescript
import { DefaultAzureCredential } from "@azure/identity";
import { AIProjectClient } from "@azure/ai-projects";
import * as readline from "readline";
import "dotenv/config";

const projectEndpoint = process.env["AZURE_AI_PROJECT_ENDPOINT"] || "<project endpoint>";
const deploymentName =
  process.env["AZURE_AI_MODEL_DEPLOYMENT_NAME"] || "<model deployment name>";
const fabricConnectionName =
  process.env["FABRIC_PROJECT_CONNECTION_NAME"] || "<fabric connection name>";

export async function main(): Promise<void> {
  const project = new AIProjectClient(projectEndpoint, new DefaultAzureCredential());
  const openAIClient = await project.getOpenAIClient();

  // Get connection ID from connection name
  const fabricConnection = await project.connections.get(fabricConnectionName);
  console.log(`Fabric connection ID: ${fabricConnection.id}`);

  console.log("Creating agent with Microsoft Fabric tool...");

  // Define Microsoft Fabric tool that connects to Fabric data sources
  const agent = await project.agents.createVersion("MyFabricAgent", {
    kind: "prompt",
    model: deploymentName,
    instructions: "You are a helpful assistant.",
    tools: [
      {
        type: "fabric_dataagent_preview",
        fabric_dataagent_preview: {
          project_connections: [
            {
              project_connection_id: fabricConnection.id,
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
      "Enter your question for Fabric (e.g., 'Tell me about sales records'): \n",
      (answer) => {
        rl.close();
        resolve(answer);
      },
    );
  });

  console.log("\nSending request to Fabric agent...");
  const response = await openAIClient.responses.create(
    {
      input: userInput,
    },
    {
      body: {
        agent: { name: agent.name, type: "agent_reference" },
        tool_choice: "required",
      },
    },
  );

  console.log(`\nResponse output: ${response.output_text}`);

  // Clean up resources by deleting the agent version
  // This prevents accumulation of unused resources in your project
  console.log("\nCleaning up resources...");
  await project.agents.deleteVersion(agent.name, agent.version);
  console.log("Agent deleted");

  console.log("\nMicrosoft Fabric agent sample completed!");
}

main().catch((err) => {
  console.error("The sample encountered an error:", err);
});
```

### What this code does

1. Creates an `AIProjectClient` using `DefaultAzureCredential`.
1. Creates an agent version configured with the Fabric data agent tool.
1. Prompts you for a question.
1. Calls the Responses API with `tool_choice: "required"` to force tool use.
1. Prints the response output text.
1. Deletes the agent version.

### Required inputs

- Environment variables: `AZURE_AI_PROJECT_ENDPOINT`, `AZURE_AI_MODEL_DEPLOYMENT_NAME`, `FABRIC_PROJECT_CONNECTION_ID`.
- Authentication: `DefaultAzureCredential` must be able to obtain a token (for example, via `az login`).

### Expected output

- A line confirming agent creation.
- A line that starts with `Response output:` followed by the response text.
- A final confirmation that the agent was deleted.
:::zone-end

:::zone pivot="rest"
The following example shows how to call the Foundry Agent REST API by using the Fabric data agent tool.

> [!IMPORTANT]
> `AGENT_TOKEN` is a credential. Keep it secret and avoid checking it into source control.

```bash
curl --request POST \
  --url "$AZURE_AI_PROJECT_ENDPOINT/openai/responses?api-version=$API_VERSION" \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
  "model": "'$AZURE_AI_MODEL_DEPLOYMENT_NAME'",
  "input": "Tell me about sales records for the last quarter.",
  "tool_choice": "required",
  "tools": [
    {
      "type": "fabric_dataagent_preview",
      "fabric_dataagent_preview": {
        "project_connections": [
          {
            "project_connection_id": "'$FABRIC_PROJECT_CONNECTION_ID'"
          }
        ]
      }
    }
  ]
}'
```

### What this code does

1. Calls the Responses API.
1. Configures the request to use the Fabric data agent tool.
1. Forces tool usage by using `tool_choice`.

### Required inputs

- Environment variables: `AZURE_AI_PROJECT_ENDPOINT`, `API_VERSION`, `AGENT_TOKEN`, `AZURE_AI_MODEL_DEPLOYMENT_NAME`, `FABRIC_PROJECT_CONNECTION_ID`.

### Expected output

- A `200` response with a JSON body that contains the model output.
:::zone-end

## Troubleshooting

| Issue | Cause | Resolution |
| --- | --- | --- |
| `Artifact Id should not be empty and needs to be a valid GUID.` | Fabric connection created with invalid `workspace_id` or `artifact_id` | Recreate the Fabric connection. Copy `workspace_id` and `artifact_id` from the data agent URL path `.../groups/<workspace_id>/aiskills/<artifact_id>...`. |
| `Can't add messages to thread_... while a run ... is active.` | A run is still active for the thread | Start a new conversation or wait for the active run to finish, then try again. |
| `unauthorized` | End user lacks access to the Fabric data agent or its underlying data sources | Grant the end user access in Fabric, and confirm you're using user identity authentication. |
| `Cannot find the requested item` or `configuration not found` | Fabric data agent isn't published or its configuration changed | Publish the Fabric data agent and confirm it's active and its data sources are valid. |
| Connection timeout errors | Network latency or Fabric service delays | Increase timeout settings in your client configuration. Consider implementing retry logic with exponential backoff. |
| Data query returns empty results | Query doesn't match available data | Verify the data sources in the Fabric data agent contain the expected data. Test queries directly in Fabric first. |
| `Invalid workspace ID format` | Workspace ID isn't a valid GUID | Copy the exact workspace GUID from the Fabric URL or portal. Don't modify the ID format. |
| Agent doesn't use the Fabric tool | Tool not properly configured or prompt doesn't trigger it | Verify the Fabric tool is enabled in the agent definition. Update the prompt to reference data that requires Fabric access. |

## Next steps

> [!div class="nextstepaction"]
> [Tool use best practices](../../concepts/tool-best-practice.md)

> [!div class="nextstepaction"]
> [Agent identity](../../concepts/agent-identity.md)

> [!div class="nextstepaction"]
> [Get started with the SDK](../../../../quickstarts/get-started-code.md?view=foundry&preserve-view=true)
