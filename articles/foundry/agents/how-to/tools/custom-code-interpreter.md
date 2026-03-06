---
title: "Configure a custom code interpreter for agents"
description: "Configure a custom MCP-based code interpreter for Microsoft Foundry agents using Azure Container Apps Dynamic Sessions. Customize Python packages and compute resources."
services: azure-ai-agent-service
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: how-to
ms.date: 03/06/2026
author: alvinashcraft
ms.author: aashcraft
ms.custom: pilot-ai-workflow-jan-2026
ai-usage: ai-assisted
zone_pivot_groups: selection-custom-code-interpreter
---

# Custom code interpreter tool for agents (preview)
[!INCLUDE [feature-preview](../../../includes/feature-preview.md)]

A custom code interpreter gives you full control over the runtime environment for agent-generated Python code. You can configure custom Python packages, compute resources, and [Azure Container Apps environment](/azure/container-apps/environment) settings. The code interpreter container exposes a Model Context Protocol (MCP) server.

Use a custom code interpreter when the built-in [Code Interpreter tool for agents](code-interpreter.md) doesn't meet your requirements—for example, when you need specific Python packages, custom container images, or dedicated compute resources.

For more information about MCP and how agents connect to MCP tools, see [Connect to Model Context Protocol servers (preview)](model-context-protocol.md).

## Usage support

This article uses the Azure CLI and a runnable sample project.

✔️ (GA) indicates general availability, ✔️ (Preview) indicates public preview, and a dash (-) indicates the feature isn't available.

| Microsoft Foundry support | Python SDK | C# SDK | JavaScript SDK | Java SDK | REST API | Basic agent setup | Standard agent setup |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ✔️ | ✔️ (GA) | ✔️ (Preview) | ✔️ (GA) | ✔️ (Preview) | ✔️ (GA) | - | ✔️ |

For the latest SDK and API support for agents tools, see [Best practices for using tools in Microsoft Foundry Agent Service](../../concepts/tool-best-practice.md).

## SDK support

The custom code interpreter uses the MCP tool type. Any SDK that supports MCP tools can create a custom code interpreter agent. The .NET and Java SDKs are currently in preview. For the infrastructure provisioning steps (Azure CLI, Bicep), see [Create an agent with custom code interpreter](#create-an-agent-with-custom-code-interpreter).

## Prerequisites

- [Azure CLI](/cli/azure/install-azure-cli) version 2.60.0 or later.
- (Optional) [uv](https://docs.astral.sh/uv/getting-started/installation/) for faster Python package management.
- An Azure subscription and resource group with the following role assignments:
  - [Azure AI Owner](/azure/role-based-access-control/built-in-roles/ai-machine-learning#azure-ai-owner)
  - [Container Apps ManagedEnvironment Contributor](/azure/role-based-access-control/built-in-roles/containers#container-apps-managedenvironments-contributor)
- An Azure AI Foundry SDK. See the [quickstart](../../../quickstarts/get-started-code.md) for installation.

## Before you begin

This procedure provisions Azure infrastructure, including Azure Container Apps resources. Review your organization's Azure cost and governance requirements before deploying.

## Create an agent with custom code interpreter

The following steps show how to provision the infrastructure and create an agent that uses a custom code interpreter MCP server. The infrastructure setup applies to all languages. Language-specific code samples follow.

### Register the preview feature

Register the MCP server feature for Azure Container Apps Dynamic Sessions:

```console
az feature register --namespace Microsoft.App --name SessionPoolsSupportMCP
az provider register -n Microsoft.App
```

### Get the sample code

Clone the [sample code in the GitHub repo](https://github.com/azure-ai-foundry/foundry-samples) and navigate to the `samples/python/prompt-agents/code-interpreter-custom` folder in your terminal.

### Provision the infrastructure

To provision the infrastructure, run the following command by using the Azure CLI (`az`):

```console
az deployment group create \
    --name custom-code-interpreter \
    --subscription <your_subscription> \
    --resource-group <your_resource_group> \
    --template-file ./infra.bicep
```

> [!NOTE]
> Deployment can take up to one hour, depending on the number of standby instances you request. The dynamic session pool allocation is the longest step.

### Configure and run the agent

Copy the `.env.sample` file from the repository to `.env` and populate the values from your deployment output. You can find these values in the Azure portal under the resource group.

Install the Python dependencies by using `uv sync` or `pip install`. Finally, run `./main.py`.

:::zone pivot="python"

### Code example

The following Python sample shows how to create an agent with a custom code interpreter MCP tool:

```python
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition, MCPTool

# Format: "https://resource_name.ai.azure.com/api/projects/project_name"
PROJECT_ENDPOINT = "your_project_endpoint"
MCP_SERVER_URL = "https://your-mcp-server-url"
# Optional: set to your project connection ID if your MCP server requires authentication
MCP_CONNECTION_ID = "your-mcp-connection-id"

# Create clients to call Foundry API
project = AIProjectClient(
    endpoint=PROJECT_ENDPOINT,
    credential=DefaultAzureCredential(),
)
openai = project.get_openai_client()

# Configure the custom code interpreter MCP tool
custom_code_interpreter = MCPTool(
    server_label="custom-code-interpreter",
    server_url=MCP_SERVER_URL,
    project_connection_id=MCP_CONNECTION_ID,
)

# Create an agent with the custom code interpreter
agent = project.agents.create_version(
    agent_name="CustomCodeInterpreterAgent",
    definition=PromptAgentDefinition(
        model="gpt-5-mini",
        instructions="You are a helpful assistant that can run Python code to analyze data and solve problems.",
        tools=[custom_code_interpreter],
    ),
    description="Agent with custom code interpreter for data analysis.",
)
print(f"Agent created (id: {agent.id}, name: {agent.name}, version: {agent.version})")

# Test the agent with a simple calculation
response = openai.responses.create(
    input="Calculate the factorial of 10 using Python.",
    extra_body={"agent_reference": {"name": agent.name, "type": "agent_reference"}},
)
print(f"Response: {response.output_text}")

# Clean up
project.agents.delete_version(agent_name=agent.name, agent_version=agent.version)
print("Agent deleted")
```

### Expected output

When you run the sample, you see output similar to:

```console
Agent created (id: agent-xxxxxxxxxxxx, name: CustomCodeInterpreterAgent, version: 1)
Response: The factorial of 10 is 3,628,800. I calculated this using Python's math.factorial() function.
Agent deleted
```

:::zone-end

:::zone pivot="csharp"

### Code example

The following C# sample shows how to create an agent with a custom code interpreter MCP tool. For more information about working with MCP tools in .NET, see the [MCP tool sample](https://github.com/Azure/azure-sdk-for-net/blob/feature/ai-foundry/agents-v2/sdk/ai/Azure.AI.Projects.OpenAI/samples/Sample19_MCP.md) in the Azure SDK for .NET repository on GitHub.

```csharp
using Azure.AI.Projects;
using Azure.AI.Projects.OpenAI;
using Azure.Identity;

// Format: "https://resource_name.ai.azure.com/api/projects/project_name"
var projectEndpoint = "your_project_endpoint";
var mcpServerUrl = "https://your-mcp-server-url";
// Optional: set to your project connection ID if your MCP server requires authentication
var mcpConnectionId = "your-mcp-connection-id";

// Create project client to call Foundry API
AIProjectClient projectClient = new(
    endpoint: new Uri(projectEndpoint),
    tokenProvider: new DefaultAzureCredential());

// Create agent with custom code interpreter MCP tool
// Code runs in a sandboxed Azure Container Apps session
McpTool tool = ResponseTool.CreateMcpTool(
    serverLabel: "custom-code-interpreter",
    serverUri: new Uri(mcpServerUrl));
tool.ProjectConnectionId = mcpConnectionId;

PromptAgentDefinition agentDefinition = new(model: "gpt-5-mini")
{
    Instructions = "You are a helpful assistant that can run Python code to analyze data and solve problems.",
    Tools = { tool }
};

AgentVersion agent = projectClient.Agents.CreateAgentVersion(
    agentName: "CustomCodeInterpreterAgent",
    options: new(agentDefinition));

Console.WriteLine($"Agent created: {agent.Name} (version {agent.Version})");

// Create a response using the agent
ProjectResponsesClient responseClient = projectClient.OpenAI.GetProjectResponsesClientForAgent(agent.Name);

ResponseResult response = responseClient.CreateResponse(
    new([ResponseItem.CreateUserMessageItem("Calculate the factorial of 10 using Python.")]));

Console.WriteLine(response.GetOutputText());

// Clean up
projectClient.Agents.DeleteAgentVersion(
    agentName: agent.Name,
    agentVersion: agent.Version);
Console.WriteLine("Agent deleted");
```

### Expected output

```console
Agent created: CustomCodeInterpreterAgent (version 1)
The factorial of 10 is 3,628,800.
Agent deleted
```

:::zone-end

:::zone pivot="typescript"

### Code example

The following TypeScript sample shows how to create an agent with a custom code interpreter MCP tool. For a JavaScript version, see the [MCP tool sample](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/ai/ai-projects/samples/v2-beta/javascript/agents/tools/agentMcp.js) in the Azure SDK for JavaScript repository on GitHub.

```typescript
import { DefaultAzureCredential } from "@azure/identity";
import { AIProjectClient } from "@azure/ai-projects";

// Format: "https://resource_name.ai.azure.com/api/projects/project_name"
const PROJECT_ENDPOINT = "your_project_endpoint";
const MCP_SERVER_URL = "https://your-mcp-server-url";

export async function main(): Promise<void> {
  // Create clients to call Foundry API
  const project = new AIProjectClient(PROJECT_ENDPOINT, new DefaultAzureCredential());
  const openai = project.getOpenAIClient();

  // Create agent with custom code interpreter MCP tool
  // The custom code interpreter uses require_approval: "never" because code
  // runs in a sandboxed Azure Container Apps session
  const agent = await project.agents.createVersion("CustomCodeInterpreterAgent", {
    kind: "prompt",
    model: "gpt-5-mini",
    instructions:
      "You are a helpful assistant that can run Python code to analyze data and solve problems.",
    tools: [
      {
        type: "mcp",
        server_label: "custom-code-interpreter",
        server_url: MCP_SERVER_URL,
        require_approval: "never",
      },
    ],
  });
  console.log(`Agent created (name: ${agent.name}, version: ${agent.version})`);

  // Send a request to the agent
  const response = await openai.responses.create(
    {
      input: "Calculate the factorial of 10 using Python.",
    },
    {
      body: { agent: { name: agent.name, type: "agent_reference" } },
    },
  );
  console.log(`Response: ${response.output_text}`);

  // Clean up
  await project.agents.deleteVersion(agent.name, agent.version);
  console.log("Agent deleted");
}

main().catch((err) => {
  console.error("The sample encountered an error:", err);
});
```

### Expected output

```console
Agent created (name: CustomCodeInterpreterAgent, version: 1)
Response: The factorial of 10 is 3,628,800. I calculated this using Python's math.factorial() function.
Agent deleted
```

:::zone-end

:::zone pivot="java"

Add the dependency to your `pom.xml`:

```xml
<dependency>
    <groupId>com.azure</groupId>
    <artifactId>azure-ai-agents</artifactId>
    <version>2.0.0-beta.1</version>
</dependency>
```

### Code example

```java
import com.azure.ai.agents.AgentsClient;
import com.azure.ai.agents.AgentsClientBuilder;
import com.azure.ai.agents.ResponsesClient;
import com.azure.ai.agents.models.AgentReference;
import com.azure.ai.agents.models.AgentVersionDetails;
import com.azure.ai.agents.models.McpTool;
import com.azure.ai.agents.models.PromptAgentDefinition;
import com.azure.core.util.BinaryData;
import com.azure.identity.DefaultAzureCredentialBuilder;
import com.openai.models.responses.Response;
import com.openai.models.responses.ResponseCreateParams;

import java.util.Collections;

public class CustomCodeInterpreterExample {
    public static void main(String[] args) {
        // Format: "https://resource_name.ai.azure.com/api/projects/project_name"
        String projectEndpoint = "your_project_endpoint";
        String mcpServerUrl = "https://your-mcp-server-url";
        // Optional: set to your project connection ID if your MCP server requires authentication
        String mcpConnectionId = "your-mcp-connection-id";

        // Create clients to call Foundry API
        AgentsClientBuilder builder = new AgentsClientBuilder()
            .credential(new DefaultAzureCredentialBuilder().build())
            .endpoint(projectEndpoint);

        AgentsClient agentsClient = builder.buildAgentsClient();
        ResponsesClient responsesClient = builder.buildResponsesClient();

        // Create custom code interpreter MCP tool
        // Uses require_approval: "never" because code runs in a sandboxed Container Apps session
        McpTool customCodeInterpreter = new McpTool("custom-code-interpreter")
            .setServerUrl(mcpServerUrl)
            .setProjectConnectionId(mcpConnectionId)
            .setRequireApproval(BinaryData.fromString("\"never\""));

        PromptAgentDefinition agentDefinition = new PromptAgentDefinition("gpt-5-mini")
            .setInstructions("You are a helpful assistant that can run Python code to analyze data and solve problems.")
            .setTools(Collections.singletonList(customCodeInterpreter));

        AgentVersionDetails agent = agentsClient.createAgentVersion(
            "CustomCodeInterpreterAgent", agentDefinition);
        System.out.printf("Agent created: %s (version %s)%n", agent.getName(), agent.getVersion());

        // Create a response
        AgentReference agentReference = new AgentReference(agent.getName())
            .setVersion(agent.getVersion());

        Response response = responsesClient.createWithAgent(
            agentReference,
            ResponseCreateParams.builder()
                .input("Calculate the factorial of 10 using Python."));

        System.out.println("Response: " + response.output());

        // Clean up
        agentsClient.deleteAgentVersion(agent.getName(), agent.getVersion());
        System.out.println("Agent deleted");
    }
}
```

### Expected output

```console
Agent created: CustomCodeInterpreterAgent (version 1)
Response: The factorial of 10 is 3,628,800.
Agent deleted
```

:::zone-end

:::zone pivot="rest"

### Prerequisites

Set these environment variables:

- `FOUNDRY_PROJECT_ENDPOINT`: Your project endpoint URL.
- `AGENT_TOKEN`: A bearer token for Foundry.

Get an access token:

```bash
export AGENT_TOKEN=$(az account get-access-token --scope "https://ai.azure.com/.default" --query accessToken -o tsv)
```

### Code example

#### 1. Create an agent with custom code interpreter

```bash
curl -X POST "$FOUNDRY_PROJECT_ENDPOINT/agents?api-version=v1" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -d '{
    "name": "CustomCodeInterpreterAgent",
    "definition": {
      "kind": "prompt",
      "model": "<MODEL_DEPLOYMENT>",
      "instructions": "You are a helpful assistant that can run Python code to analyze data and solve problems.",
      "tools": [
        {
          "type": "mcp",
          "server_label": "custom-code-interpreter",
          "server_url": "<MCP_SERVER_URL>",
          "project_connection_id": "<MCP_PROJECT_CONNECTION_ID>",
          "require_approval": "never"
        }
      ]
    }
  }'
```

#### 2. Create a response

```bash
curl -X POST "$FOUNDRY_PROJECT_ENDPOINT/openai/v1/responses" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -d '{
    "agent_reference": {"type": "agent_reference", "name": "CustomCodeInterpreterAgent"},
    "input": "Calculate the factorial of 10 using Python."
  }'
```

#### 3. Clean up

```bash
curl -X DELETE "$FOUNDRY_PROJECT_ENDPOINT/agents/CustomCodeInterpreterAgent?api-version=v1" \
  -H "Authorization: Bearer $AGENT_TOKEN"
```

### Expected output

```json
{
  "id": "resp_xxxxxxxxxxxx",
  "output": [
    {
      "type": "message",
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "The factorial of 10 is 3,628,800."
        }
      ]
    }
  ]
}
```

:::zone-end

## Verify your setup

After you've provisioned the infrastructure and run the sample:

1. Confirm the Azure deployment completed successfully.
1. Confirm the sample connects using the values in your `.env` file.
1. In Microsoft Foundry, verify your agent calls the tool using tracing. For more information, see [Best practices for using tools in Microsoft Foundry Agent Service](../../concepts/tool-best-practice.md).

## Troubleshooting

| Issue | Likely cause | Resolution |
| --- | --- | --- |
| Feature registration is still pending | The `az feature register` command returns `Registering` state. | Wait for registration to complete (can take 15-30 minutes). Check status with `az feature show --namespace Microsoft.App --name SessionPoolsSupportMCP`. Then run `az provider register -n Microsoft.App` again. |
| Deployment fails with permission error | Missing required role assignments. | Confirm you have **Azure AI Owner** and **Container Apps ManagedEnvironment Contributor** roles on the subscription or resource group. |
| Deployment fails with region error | The selected region doesn't support Azure Container Apps Dynamic Sessions. | Try a different region. See [Azure Container Apps regions](/azure/container-apps/overview#regions) for supported regions. |
| Agent doesn't call the tool | The MCP connection isn't configured correctly, or the agent instructions don't prompt tool use. | Use tracing in Microsoft Foundry to confirm tool invocation. Verify the `MCP_SERVER_URL` matches your deployed Container Apps endpoint. See [Best practices](../../concepts/tool-best-practice.md). |
| MCP server connection timeout | The Container Apps session pool isn't running or has no standby instances. | Check the session pool status in the Azure portal. Increase `standbyInstanceCount` in your Bicep template if needed. |
| Code execution fails in container | Missing Python packages in the custom container. | Update your container image to include required packages. Rebuild and redeploy the container. |
| Authentication error connecting to MCP server | The project connection credentials are invalid or expired. | Regenerate the connection credentials and update the `.env` file. Verify the `MCP_PROJECT_CONNECTION_ID` format. |

## Limitations

The APIs don't directly support file input or output, or the use of file stores. To get data in and out, you must use URLs, such as data URLs for small files and Azure Blob Service shared access signature (SAS) URLs for large files.

## Security

If you use SAS URLs to pass data in or out of the runtime:

- Use short-lived SAS tokens.
- Don't log SAS URLs or store them in source control.
- Scope permissions to the minimum required (for example, read-only or write-only).

## Clean up

To stop billing for provisioned resources, delete the resources created by the sample deployment. If you used a dedicated resource group for this article, delete the resource group.

## Related content

- [Connect to Model Context Protocol servers (preview)](model-context-protocol.md)
- [Best practices for using tools in Microsoft Foundry Agent Service](../../concepts/tool-best-practice.md)
- [Azure Container Apps Dynamic Sessions](/azure/container-apps/sessions)
- [Session pools with custom containers](/azure/container-apps/session-pool#custom-container-pool)
- [Azure Container Apps environment](/azure/container-apps/environment)
- [Install the Azure CLI](/cli/azure/install-azure-cli)
- [Code Interpreter tool for agents](code-interpreter.md)
