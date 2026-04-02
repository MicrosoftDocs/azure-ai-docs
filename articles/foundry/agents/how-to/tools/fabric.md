---
title: "Use the Microsoft Fabric data agent with Foundry agents"
description: "Learn how to connect a Microsoft Fabric data agent to Foundry Agent Service so your agent can analyze enterprise data by using identity passthrough."
author: alvinashcraft
ms.author: aashcraft
manager: nitinme
ms.date: 03/30/2026
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: how-to
ms.custom:
  - build-2025
  - dev-focus
  - pilot-ai-workflow-jan-2026
  - doc-kit-assisted
zone_pivot_groups: selection-fabric-tool
ai-usage: ai-assisted
---

# Use the Microsoft Fabric data agent (preview)
[!INCLUDE [feature-preview](../../../includes/feature-preview.md)]

> [!NOTE]
> See [best practices](../../concepts/tool-best-practice.md) for information on optimizing tool usage.

Use the [**Microsoft Fabric data agent**](https://go.microsoft.com/fwlink/?linkid=2312815) with Foundry Agent Service to analyze enterprise data in chat. The Fabric data agent turns enterprise data into a conversational question and answer experience.

First, build and publish a Fabric data agent. Then, connect your Fabric data agent with the published endpoint. When a user sends a query, the agent determines if it should use the Fabric data agent. If so, it uses the end user's identity to generate queries over data they have access to. Lastly, the agent generates responses based on queries returned from the Fabric data agent. By using identity passthrough (On-Behalf-Of) authorization, this integration simplifies access to enterprise data in Fabric while maintaining robust security, ensuring proper access control and enterprise-grade protection.

### Usage support

The following table shows SDK and setup support.

| Microsoft Foundry support | Python SDK | C# SDK | JavaScript SDK | Java SDK | REST API | Basic agent setup | Standard agent setup |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |

## Prerequisites

> [!NOTE]
> - The model you select during agent setup is only used for orchestration and response generation. It doesn't affect which model the Fabric data agent uses for NL2SQL.
> - To help your agent invoke the Fabric tool reliably, include clear tool guidance in your agent instructions (for example, "For customer and product sales data, use the Fabric tool"). You can also force tool use with `tool_choice`.

- Create and publish a [Fabric data agent](https://go.microsoft.com/fwlink/?linkid=2312910).
- Assign developers and end users at least the `Azure AI User` Azure RBAC role. For more information, see [Azure role-based access control in Foundry](../../../concepts/rbac-foundry.md).
- Give developers and end users at least `READ` access to the Fabric data agent. Users also need the minimum permission on each underlying data source:

    | Data source | Minimum permission |
    |---|---|
    | Power BI semantic model | `Build` (includes Read). Read alone isn't sufficient because the agent generates model queries that require Build. |
    | Lakehouse | Read on the lakehouse item (and table access, if enforced). |
    | Warehouse | Read (`SELECT` on relevant tables). |
    | KQL database | Reader role on the database. |

    For full details, see [Underlying data source permissions](/fabric/data-science/data-agent-sharing#underlying-data-source-permissions).
- Ensure your Fabric data agent and Foundry project are in the same tenant.
- Use user identity authentication. Service principal authentication isn't supported for the Fabric data agent.
- Get these values before you run the samples:
  - Your Foundry project endpoint: `FOUNDRY_PROJECT_ENDPOINT`.
  - Your model deployment name: `FOUNDRY_MODEL_DEPLOYMENT_NAME`.
  - Your Fabric connection ID (project connection ID): `FABRIC_PROJECT_CONNECTION_ID`.
- For the REST sample, also set:
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
> - For more information, see [Get ready to code](../../../quickstarts/get-started-code.md).
> - Your connection ID should be in the format of `/subscriptions/{{subscriptionID}}/resourceGroups/{{resourceGroupName}}/providers/Microsoft.CognitiveServices/accounts/{{foundryAccountName}}/projects/{{foundryProjectName}}/connections/{{foundryConnectionName}}`.

:::zone pivot="python"

```python
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    PromptAgentDefinition,
    MicrosoftFabricPreviewTool,
    FabricDataAgentToolParameters,
    ToolProjectConnection,
)

# Format: "https://resource_name.ai.azure.com/api/projects/project_name"
PROJECT_ENDPOINT = "your_project_endpoint"
FABRIC_CONNECTION_NAME = "my-fabric-connection"

# Create clients to call Foundry API
project = AIProjectClient(
    endpoint=PROJECT_ENDPOINT,
    credential=DefaultAzureCredential(),
)
openai = project.get_openai_client()

# Get connection ID from connection name
fabric_connection = project.connections.get(FABRIC_CONNECTION_NAME)

# Create an agent with the Fabric data agent tool
agent = project.agents.create_version(
    agent_name="MyAgent",
    definition=PromptAgentDefinition(
        model="gpt-4.1-mini",
        instructions="You are a helpful assistant.",
        tools=[
            MicrosoftFabricPreviewTool(
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

# Send the user query and force the agent to use the Fabric tool
response = openai.responses.create(
    tool_choice="required",
    input=user_input,
    extra_body={"agent_reference": {"name": agent.name, "type": "agent_reference"}},
)

print(f"Response output: {response.output_text}")

# Clean up resources
project.agents.delete_version(agent_name=agent.name, agent_version=agent.version)
print("Agent deleted")
```

### Expected output

- A line confirming agent creation.
- A line that starts with `Response output:` followed by the response text.

For more details, see the [full Python sample for Fabric data agent](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-agents/samples/agents_tools/sample_agents_fabric.py).
:::zone-end

:::zone pivot="csharp"

To enable your agent to access the Fabric data agent, use `MicrosoftFabricAgentTool`.

```csharp
// Format: "https://resource_name.ai.azure.com/api/projects/project_name"
var projectEndpoint = "your_project_endpoint";
var fabricConnectionName = "my-fabric-connection";

// Create project client to call Foundry API
AIProjectClient projectClient = new(
    endpoint: new Uri(projectEndpoint),
    tokenProvider: new DefaultAzureCredential());

// Get connection ID from connection name
AIProjectConnection fabricConnection = projectClient.Connections.GetConnection(connectionName: fabricConnectionName);

FabricDataAgentToolOptions fabricToolOption = new()
{
    ProjectConnections = { new ToolProjectConnection(projectConnectionId: fabricConnection.Id) }
};
DeclarativeAgentDefinition agentDefinition = new(model: "gpt-4.1-mini")
{
    Instructions = "You are a helpful assistant.",
    Tools = { new MicrosoftFabricPreviewTool(fabricToolOption), }
};
AgentVersion agentVersion = projectClient.AgentAdministrationClient.CreateAgentVersion(
    agentName: "myAgent",
    options: new(agentDefinition));

// Create the response and make sure we are always using tool.
ProjectResponsesClient responseClient = projectClient.ProjectOpenAIClient.GetProjectResponsesClientForAgent(agentVersion.Name);
CreateResponseOptions responseOptions = new()
{
    ToolChoice = ResponseToolChoice.CreateRequiredChoice(),
    InputItems = { ResponseItem.CreateUserMessageItem("What was the number of public holidays in Norway in 2024?") },
};
ResponseResult response = responseClient.CreateResponse(options: responseOptions);

// Print the Agent output.
Assert.That(response.Status, Is.EqualTo(ResponseStatus.Completed));
Console.WriteLine(response.GetOutputText());

// Delete the Agent version to clean up resources.
projectClient.AgentAdministrationClient.DeleteAgentVersion(agentName: agentVersion.Name, agentVersion: agentVersion.Version);
```

### Expected output

- The response text printed to the console. For the sample question, the response should include the number of public holidays (for example, `62`).
:::zone-end

:::zone pivot="typescript"

The following TypeScript example demonstrates how to create an AI agent with Microsoft Fabric capabilities by using the `MicrosoftFabricAgentTool` and synchronous Azure AI Projects client. The agent can query Fabric data sources and provide responses based on data analysis. For a JavaScript version of this sample, see the [JavaScript sample for Fabric data agent](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/ai/ai-projects/samples/v2-beta/javascript/agents/tools/agentFabric.js) in the Azure SDK for JavaScript repository on GitHub.

```typescript
import { DefaultAzureCredential } from "@azure/identity";
import { AIProjectClient } from "@azure/ai-projects";
import * as readline from "readline";

// Format: "https://resource_name.ai.azure.com/api/projects/project_name"
const PROJECT_ENDPOINT = "your_project_endpoint";
const FABRIC_CONNECTION_NAME = "my-fabric-connection";

export async function main(): Promise<void> {
  const project = new AIProjectClient(PROJECT_ENDPOINT, new DefaultAzureCredential());
  const openai = project.getOpenAIClient();

  // Get connection ID from connection name
  const fabricConnection = await project.connections.get(FABRIC_CONNECTION_NAME);

  // Define Microsoft Fabric tool that connects to Fabric data sources
  const agent = await project.agents.createVersion("MyFabricAgent", {
    kind: "prompt",
    model: "gpt-4.1-mini",
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

  // Send the user query and force the agent to use the Fabric tool
  const response = await openai.responses.create(
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
  await project.agents.deleteVersion(agent.name, agent.version);
  console.log("Agent deleted");
}

main().catch((err) => {
  console.error("The sample encountered an error:", err);
});
```

### Expected output

- A line confirming agent creation.
- A line that starts with `Response output:` followed by the response text.
- A final confirmation that the agent was deleted.
:::zone-end

:::zone pivot="java"

## Use Microsoft Fabric in a Java agent

Add the dependency to your `pom.xml`:

```xml
<dependency>
    <groupId>com.azure</groupId>
    <artifactId>azure-ai-agents</artifactId>
    <version>2.0.0</version>
</dependency>
```

### Create an agent with Microsoft Fabric

```java
import com.azure.ai.agents.AgentsClient;
import com.azure.ai.agents.AgentsClientBuilder;
import com.azure.ai.agents.ResponsesClient;
import com.azure.ai.agents.models.*;
import com.azure.identity.DefaultAzureCredentialBuilder;
import com.openai.models.responses.Response;
import com.openai.models.responses.ResponseCreateParams;

import java.util.Arrays;
import java.util.Collections;

public class FabricToolExample {
    public static void main(String[] args) {
        // Format: "https://resource_name.ai.azure.com/api/projects/project_name"
        String projectEndpoint = "your_project_endpoint";
        String fabricConnectionId = "your-fabric-connection-id";

        AgentsClientBuilder builder = new AgentsClientBuilder()
            .credential(new DefaultAzureCredentialBuilder().build())
            .endpoint(projectEndpoint);

        AgentsClient agentsClient = builder.buildAgentsClient();
        ResponsesClient responsesClient = builder.buildResponsesClient();

        // Create Microsoft Fabric tool with connection configuration
        MicrosoftFabricPreviewTool fabricTool = new MicrosoftFabricPreviewTool(
            new FabricDataAgentToolParameters()
                .setProjectConnections(Arrays.asList(
                    new ToolProjectConnection(fabricConnectionId)
                ))
        );

        // Create agent with Fabric tool
        PromptAgentDefinition agentDefinition = new PromptAgentDefinition("gpt-4.1-mini")
            .setInstructions("You are a data assistant that can query Microsoft Fabric data.")
            .setTools(Collections.singletonList(fabricTool));

        AgentVersionDetails agent = agentsClient.createAgentVersion("fabric-agent", agentDefinition);
        System.out.printf("Agent created: %s (version %s)%n", agent.getName(), agent.getVersion());

        // Create a response
        AgentReference agentReference = new AgentReference(agent.getName())
            .setVersion(agent.getVersion());

        Response response = responsesClient.createAzureResponse(
            new AzureCreateResponseOptions().setAgentReference(agentReference),
            ResponseCreateParams.builder()
                .input("Query the latest sales data from Microsoft Fabric"));

        System.out.println("Response: " + response.output());

        // Clean up
        agentsClient.deleteAgentVersion(agent.getName(), agent.getVersion());
    }
}
```

:::zone-end

:::zone pivot="rest"
The following example shows how to call the Foundry Agent REST API by using the Fabric data agent tool.

Get an access token:

```bash
export AGENT_TOKEN=$(az account get-access-token --scope "https://ai.azure.com/.default" --query accessToken -o tsv)
```

> [!IMPORTANT]
> `AGENT_TOKEN` is a credential. Keep it secret and avoid checking it into source control.

```bash
curl --request POST \
  --url "$FOUNDRY_PROJECT_ENDPOINT/openai/v1/responses" \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
  "model": "'$FOUNDRY_MODEL_DEPLOYMENT_NAME'",
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

### Expected output

- A `200` response with a JSON body that contains the model output.
:::zone-end

## Limitations

- The Fabric data agent tool doesn't work when the agent is published to Microsoft Teams. Agents published to Teams use project managed identity for authentication, but the Fabric data agent tool requires user identity passthrough (On-Behalf-Of).

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
> [Get started with the SDK](../../../quickstarts/get-started-code.md)
