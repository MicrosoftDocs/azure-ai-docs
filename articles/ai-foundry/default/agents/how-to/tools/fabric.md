---
title: Use Fabric Data Agent with Foundry Agents
titleSuffix: Microsoft Foundry
description: Learn how to connect a Microsoft Fabric data agent to Foundry Agent Service to analyze enterprise data in chat with identity passthrough. Try the sample code.
author: alvinashcraft
ms.author: aashcraft
manager: nitinme
ms.date: 12/11/2025
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: how-to
ms.custom:
  - build-2025
  - dev-focus
zone_pivot_groups: selection-fabric-tool
ai-usage: ai-assisted
---

# Use the Microsoft Fabric data agent (preview)

[!INCLUDE [feature-preview](../../../../includes/feature-preview.md)]

> [!NOTE]
> See [best practices](../../concepts/tool-best-practice.md) for information on optimizing tool usage.

By integrating your agent in Foundry Agent Service with the [**Microsoft Fabric data agent**](https://go.microsoft.com/fwlink/?linkid=2312815), you unlock powerful data analysis capabilities. The Fabric data agent transforms enterprise data into conversational question and answer systems. Users can interact with the data through chat and uncover data-driven and actionable insights.

First, build and publish a Fabric data agent. Then, connect your Fabric data agent with the published endpoint. When a user sends a query, the agent determines if it should use the Fabric data agent. If so, it uses the end user's identity to generate queries over data they have access to. Lastly, the agent generates responses based on queries returned from Fabric data agents. By using Identity Passthrough (On-Behalf-Of) authorization, this integration simplifies access to enterprise data in Fabric while maintaining robust security, ensuring proper access control and enterprise-grade protection.

### Usage support

| Microsoft Foundry support | Python SDK | C# SDK | JavaScript SDK | Java SDK | REST API | Basic agent setup | Standard agent setup |
|---------|---------|---------|---------|---------|---------|---------|
| ✔️ | ✔️ | ✔️ | ✔️ | - | ✔️ | ✔️ | ✔️ |

## Prerequisites

> [!NOTE]
> - The model you select during agent setup is only used for orchestration and response generation. It doesn't affect which model the Fabric data agent uses for NL2SQL.
> - To help your agent invoke the Fabric tool reliably, include clear tool guidance in your agent instructions (for example, "For customer and product sales data, use the Fabric tool"). You can also force tool use with `tool_choice`.

- Create and publish a [Fabric data agent](https://go.microsoft.com/fwlink/?linkid=2312910).
- Assign developers and end users at least the `Azure AI User` Azure RBAC role.
- Give developers and end users at least `READ` access to the Fabric data agent and the underlying data sources it connects to.
- Ensure your Fabric data agent and Foundry project are in the same tenant.
- Use user identity authentication. Service principal authentication isn't supported for the Fabric data agent.
- Get these values before you run the samples:
  - Your Foundry project endpoint for SDK samples: `AZURE_AI_PROJECT_ENDPOINT`.
  - Your model deployment name:
    - Python sample: `AZURE_AI_MODEL_DEPLOYMENT_NAME`.
    - TypeScript sample: `MODEL_DEPLOYMENT_NAME`.
  - Your Fabric connection ID (project connection ID): `FABRIC_PROJECT_CONNECTION_ID`.
- For the REST sample, also set:
  - `AZURE_AI_FOUNDRY_PROJECT_ENDPOINT`.
  - `API_VERSION`.
  - `AGENT_TOKEN` (a bearer token). You can get a temporary token with Azure CLI:

    ```azurecli
    az account get-access-token --scope https://ai.azure.com/.default
    ```

## Code example

> [!NOTE]
> - To run this code, you need the latest prerelease package. For more information, see the [quickstart](../../../../quickstarts/get-started-code.md?view=foundry&preserve-view=true#install-and-authenticate).
> - Your connection ID should be in the format of `/subscriptions/{{subscriptionID}}/resourceGroups/{{resourceGroupName}}/providers/Microsoft.CognitiveServices/accounts/{{foundryAccountName}}/projects/{{foundryProjectName}}/connections/{{foundryConnectionName}}`.

:::zone pivot="python"
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
                MicrosoftFabricAgentTool(
                    fabric_dataagent_preview=FabricDataAgentToolParameters(
                        project_connections=[
                            ToolProjectConnection(project_connection_id=os.environ["FABRIC_PROJECT_CONNECTION_ID"])
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
## Sample for use of an agent with Fabric Data Agent

As a prerequisite for this example, you need to create Microsoft Fabric with a Lakehouse data repository. For guidance, see the end-to-end tutorials on [using Microsoft Fabric](/fabric/fundamentals/end-to-end-tutorials).

### Create a Fabric Capacity

1. Create a **Fabric Capacity** resource in the Azure portal. Charges apply.
1. Create the workspace in [Power BI portal](https://msit.powerbi.com/home) by selecting the **Workspaces** icon on the left panel.
1. At the bottom, select **+ New workspace**.
1. In the right panel, enter the name of the workspace, select **Fabric capacity** as the **License mode**. In the **Capacity** dropdown, select the Fabric Capacity resource you just created.
1. Select **Apply**.

### Create a Lakehouse data repository

1. Select a **Lakehouse** icon in the **Other items you can create with Microsoft Fabric** section and name the new data repository.
1. Download the [public holidays data set](https://github.com/microsoft/fabric-samples/raw/refs/heads/main/docs-samples/data-engineering/Lakehouse/PublicholidaysSample/publicHolidays.parquet).
1. In the Lakehouse menu, select **Get data > Upload files** and upload the `publicHolidays.parquet` file.
1. In the **Files** section, select the three dots next to the uploaded file and select **Load to Tables > new table** and then **Load** in the opened window.
1. Delete the uploaded file by selecting the three dots and selecting **Delete**.

### Add a data agent to the Fabric

1. In the top panel, select **Add to data agent > New data agent** and name the newly created Agent.
1. In the open view on the left panel, select the Lakehouse "publicholidays" table and set a checkbox next to it.
1. Ask the question you will further use in the Requests API: "What was the number of public holidays in Norway in 2024?"
1. The Agent shows a table containing one column called "NumberOfPublicHolidays" with the single row, containing number 62.
1. Select **Publish** and in the description add "Agent has data about public holidays." If you omit this stage, an error saying "Stage configuration not found." is returned during sample run.

### Create a Fabric connection in Microsoft Foundry

After you create the Fabric data agent, connect Fabric to Microsoft Foundry.
1. Open the [Power BI](https://msit.powerbi.com/home) and select the workspace you created.
1. In the open view, select the agent you created.
1. The URL of the opened page looks like `https://msit.powerbi.com/groups/%workspace_id%/aiskills/%artifact_id%?experience=power-bi`, where `workspace_id` and `artifact_id` are GUIDs in a form like `811acded-d5f7-11f0-90a4-04d3b0c6010a`.
1. In **Microsoft Foundry** you're using for the experimentation, on the left panel select **Management center**.
1. Choose **Connected resources**.
1. Create a new connection of type **Microsoft Fabric**.
1. Populate **workspace-id** and **artifact-id** fields with GUIDs found in the Microsoft Data Agent URL and name the new connection.

### Create the sample

To enable your Agent to access Microsoft Fabric Data Agent, use `MicrosoftFabricAgentTool`.

```csharp
// Create an Agent client and read the environment variables, which will be used in the next steps.
var projectEndpoint = System.Environment.GetEnvironmentVariable("PROJECT_ENDPOINT");
var modelDeploymentName = System.Environment.GetEnvironmentVariable("MODEL_DEPLOYMENT_NAME");
var fabricConnectionName = System.Environment.GetEnvironmentVariable("FABRIC_CONNECTION_NAME");
AIProjectClient projectClient = new(endpoint: new Uri(projectEndpoint), tokenProvider: new DefaultAzureCredential());

// Use the Microsoft Fabric connection name as it is shown in the connections section
// of Microsoft Foundry to get the connection. Get the connection ID to initialize
// the FabricDataAgentToolOptions, which will be used to create MicrosoftFabricAgentTool.
AIProjectConnection fabricConnection = projectClient.Connections.GetConnection(fabricConnectionName);
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
1. Looks up your Microsoft Fabric project connection and uses it to configure the Fabric data agent tool.
1. Creates an agent version.
1. Sends a question through the agent and forces tool usage.
1. Writes the response text and deletes the agent version.

### Required inputs

- Environment variables: `PROJECT_ENDPOINT`, `MODEL_DEPLOYMENT_NAME`, `FABRIC_CONNECTION_NAME`.
- Authentication: `DefaultAzureCredential` must be able to obtain a token (for example, via `az login`).

### Expected output

- The response text printed to the console. For the sample question, the response should include the number of public holidays (for example, `62`).
:::zone-end

:::zone pivot="rest"
The following example shows how to call the Foundry Agent REST API by using the Fabric data agent tool.

```bash
curl --request POST \
  --url "$AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/openai/responses?api-version=$API_VERSION" \
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

- Environment variables: `AZURE_AI_FOUNDRY_PROJECT_ENDPOINT`, `API_VERSION`, `AGENT_TOKEN`, `AZURE_AI_MODEL_DEPLOYMENT_NAME`, `FABRIC_PROJECT_CONNECTION_ID`.

### Expected output

- A `200` response with a JSON body that contains the model output.
:::zone-end

:::zone pivot="typescript"
The following TypeScript example demonstrates how to create an AI agent with Microsoft Fabric capabilities by using the `MicrosoftFabricAgentTool` and synchronous Azure AI Projects client. The agent can query Fabric data sources and provide responses based on data analysis. For a JavaScript version of this sample, see the [JavaScript sample for Fabric data agent](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/ai/ai-projects/samples/v2-beta/javascript/agents/tools/agentFabric.js) in the Azure SDK for JavaScript repository on GitHub.

```typescript
import { DefaultAzureCredential } from "@azure/identity";
import { AIProjectClient } from "@azure/ai-projects";
import * as readline from "readline";
import "dotenv/config";

const projectEndpoint = process.env["AZURE_AI_PROJECT_ENDPOINT"] || "<project endpoint>";
const deploymentName = process.env["MODEL_DEPLOYMENT_NAME"] || "<model deployment name>";
const fabricProjectConnectionId =
  process.env["FABRIC_PROJECT_CONNECTION_ID"] || "<fabric project connection id>";

export async function main(): Promise<void> {
  const project = new AIProjectClient(projectEndpoint, new DefaultAzureCredential());
  const openAIClient = await project.getOpenAIClient();

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
              project_connection_id: fabricProjectConnectionId,
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

- Environment variables: `AZURE_AI_PROJECT_ENDPOINT`, `MODEL_DEPLOYMENT_NAME`, `FABRIC_PROJECT_CONNECTION_ID`.
- Authentication: `DefaultAzureCredential` must be able to obtain a token (for example, via `az login`).

### Expected output

- A line confirming agent creation.
- A line that starts with `Response output:` followed by the response text.
- A final confirmation that the agent was deleted.
:::zone-end
