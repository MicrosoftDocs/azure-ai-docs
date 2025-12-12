---
title: "How to use the data agents in Microsoft Fabric for the Microsoft Foundry Agent Service"
titleSuffix: Microsoft Foundry
description: Learn how to perform data analytics in Microsoft Foundry with the Fabric data agent.
author: alvinashcraft
ms.author: aashcraft
manager: nitinme
ms.date: 12/11/2025
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: how-to
ms.custom:
  - build-2025
zone_pivot_groups: selection-fabric-tool
---

# Use the Microsoft Fabric data agent (preview)

[!INCLUDE [feature-preview](../../../../includes/feature-preview.md)]

> [!NOTE]
> See [best practices](../../concepts/tool-best-practice.md) for information on optimizing tool usage.

Integrate your Microsoft Foundry Agent with the [**Microsoft Fabric data agent**](https://go.microsoft.com/fwlink/?linkid=2312815) to unlock powerful data analysis capabilities. The Fabric data agent transforms enterprise data into conversational question and answer systems, allowing users to interact with the data through chat and uncover data-driven and actionable insights. 

You need to first build and publish a Fabric data agent and then connect your Fabric data agent with the published endpoint. When a user sends a query, the agent first determines if the Fabric data agent should be leveraged or not. If so, it uses the end user’s identity to generate queries over data they have access to. Lastly, the agent generates responses based on queries returned from Fabric data agents. By using Identity Passthrough (On-Behalf-Of) authorization, this integration simplifies access to enterprise data in Fabric while maintaining robust security, ensuring proper access control and enterprise-grade protection.

## Prerequisites

> [!NOTE]
> - The model you select in Foundry Agent setup is only used for agent orchestration and response generation. It doesn't impact which model the Fabric data agent uses for NL2SQL operation.
> - To help your model invoke your Microsoft Fabric tool in the expected way, make sure you update agent instructions with descriptions of your Fabric data agent and what data it can access. An example is "for customer and product sales related data, please use the Fabric tool". Use a smaller AI model such as `gpt-4o-mini`. You can also use the `tool_choice` parameter in SDK or API to force the Fabric tool to be invoked at each run. 

- You created and published a [Fabric data agent](https://go.microsoft.com/fwlink/?linkid=2312910).
- Developers and end users have at least the `Azure AI User` RBAC role. 
- Developers and end users have at least `READ` access to the Fabric data agent and the underlying data sources it connects with.
- Your Fabric Data Agent and Foundry Agent are in the same tenant.
- The Fabric data agent only supports user identity authentication. Service Principal Name (SPN) authentication isn't supported.
- Your Foundry Project endpoint.
- The name of your Microsoft Fabric connection name. 

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

For more details, see the [full Python sample for Fabric data agent](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-agents/samples/agents_tools/sample_agents_fabric.py).
:::zone-end

:::zone pivot="rest"
The following example shows how to call the Foundry Agent REST API by using the Fabric data agent tool.

```bash
curl --request POST \
  --url "$AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/openai/responses?api-version=$API_VERSION" \
  --H "Authorization: Bearer $AGENT_TOKEN" \
  --H "Content-Type: application/json" \
  --H "User-Agent: insomnia/11.6.1" \
  --d '{
"model": "$AZURE_AI_MODEL_DEPLOYMENT_NAME",
"input": "Tell me about sales records for the last quarter.",
"tools": [
  {
   "type": "fabric_dataagent_preview",
   "fabric_dataagent_preview": [
        {
            "project_connections": [
                {
                    "project_connection_id": "/subscriptions/${SUBSCRIPTION_ID}/resourceGroups/${RESOURCE_GROUP}/providers/Microsoft.CognitiveServices/accounts/${AI_SERVICES_NAME}/projects/${PROJECT_NAME}/connections/${FABRIC_PROJECT_CONNECTION_ID}"
                }
                ]
        }
        ]
    }
    ]
}'
```
:::zone-end

:::zone pivot="typescript"
The following TypeScript example demonstrates how to create an AI agent with Microsoft Fabric capabilities using the `MicrosoftFabricAgentTool` and synchronous Azure AI Projects client. The agent can query Fabric data sources and provide responses based on data analysis. For a JavaScript version of this sample, see the [JavaScript sample for Fabric data agent](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/ai/ai-projects/samples/v2-beta/javascript/agents/tools/agentFabric.js) in the Azure SDK for JavaScript repository on GitHub.

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
:::zone-end

> [!NOTE]
> - Make sure you **publish** the [data agent](https://go.microsoft.com/fwlink/?linkid=2312910) in Fabric.
> - The model you select in Foundry Agent setup is only used for agent orchestration and response generation. It doesn't impact which model the Fabric data agent uses for NL2SQL operation.
> - To help your model invoke your Microsoft Fabric tool in the expected way, make sure you update agent instructions with descriptions of your Fabric data agent and what data it can access. An example is "for customer and product sales related data, please use the Fabric tool". Use a smaller AI model such as `gpt-4o-mini`. You can also use the `tool_choice` parameter in SDK or API to force the Fabric tool to be invoked at each run. 
