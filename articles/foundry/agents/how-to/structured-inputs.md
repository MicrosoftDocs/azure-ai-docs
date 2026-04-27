---
title: "Customize Agent Behavior at Runtime with Structured Inputs"
description: "Learn how to customize agent behavior at runtime using structured inputs. Define placeholders with handlebar templates, dynamically configure agent instructions and tools, and pass values at runtime to your agent."
services: cognitive-services
manager: nitinme
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.topic: how-to
ms.date: 03/31/2026
author: alvinashcraft
ms.author: aashcraft
ms.custom: azure-ai-agents, dev-focus, doc-kit-assisted
zone_pivot_groups: selection-structured-inputs
ai-usage: ai-assisted
#CustomerIntent: As a developer building AI agents, I want to use structured inputs with handlebar templates so that I can dynamically configure agent instructions and tool resources at runtime.
---

# Customize agent behavior at runtime with structured inputs

You can customize agent instructions at runtime using **structured inputs**. Structured inputs are placeholders defined in the agent using handlebar template syntax (`{{variableName}}`). At runtime, you provide actual values to dynamically customize agent instructions, tool resource configurations, and response parameters—without creating separate agent versions for each configuration.

In this article, you learn how to:

- Define structured inputs in an agent definition
- Use handlebar templates in agent instructions
- Dynamically configure tool resources such as Code Interpreter and File Search
- Pass structured input values at runtime through the Responses API

## Prerequisites

- A [basic or standard agent environment](../../agents/environment-setup.md).
- The latest SDK package for your language. See the [quickstart](../../quickstarts/get-started-code.md) for installation steps.
- Azure credentials configured for authentication (such as `DefaultAzureCredential`).
- Your Foundry project endpoint URL and model deployment name.

## What are structured inputs?

Structured inputs use handlebar template syntax (`{{variableName}}`) to create parameterized agent definitions. You define input schemas in the agent definition under `structured_inputs`, where each input has a name, description, type, and optional default value. At runtime, supply actual values that replace the template placeholders before the agent processes the request.

Structured inputs support two categories of overrides:

- **Instruction overrides**: Parameterize agent instructions, response-level instructions, and system or developer messages.
- **Tool resource overrides**: Dynamically configure tool properties at runtime, including:
  - File search vector store IDs
  - Code interpreter file IDs and containers
  - Model Context Protocol (MCP) server URLs and headers

For array fields like `file_ids` and `vector_store_ids`, the system automatically removes empty string values at runtime. This feature enables flexible input counts – define more template slots than needed and leave unused ones empty.

### Supported structured input properties

The following table lists the agent definition properties that support handlebar templates:

| Category | Property | Description |
| -------- | -------- | ----------- |
| Instructions | Agent `instructions` | Agent-level instruction text |
| Instructions | Response `instructions` | Instructions passed in the Responses API request |
| Instructions | System/developer message `content` | Message content in the input array |
| File Search | `vector_store_ids` | Array of vector store IDs (empty values stripped) |
| Code Interpreter | `container` (string) | Container ID for a preconfigured container |
| Code Interpreter | `container.file_ids` (array) | File IDs in an auto container (empty values stripped) |
| MCP | `server_label` | Label for the MCP server |
| MCP | `server_url` | URL for the MCP server endpoint |
| MCP | `headers` (values) | HTTP header values as key-value pairs |

## Use structured inputs with agent instructions

The simplest use of structured inputs is to parameterize agent instructions. Define handlebar templates in the `instructions` field and supply values at runtime. This approach lets you personalize agent behavior for different users or contexts without creating multiple agent versions.

The following examples create an agent whose instructions include user-specific details and then supply those values when creating a response.

:::zone pivot="python"

```python
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition, StructuredInputDefinition
from azure.identity import DefaultAzureCredential

# Format: "https://resource_name.ai.azure.com/api/projects/project_name"
PROJECT_ENDPOINT = "your_project_endpoint"

# Create clients to call Foundry API
project = AIProjectClient(endpoint=PROJECT_ENDPOINT, credential=DefaultAzureCredential())
openai = project.get_openai_client()

# Create agent with handlebar templates in instructions
agent = project.agents.create_version(
    agent_name="structured-input-agent",
    definition=PromptAgentDefinition(
        model="gpt-5-mini",
        instructions=(
            "You are a helpful assistant. "
            "The user's name is {{userName}} and their role is {{userRole}}. "
            "Greet them and confirm their details."
        ),
        structured_inputs={
            "userName": StructuredInputDefinition(
                description="The user's name", required=True, schema={"type": "string"},
            ),
            "userRole": StructuredInputDefinition(
                description="The user's role", required=True, schema={"type": "string"},
            ),
        },
    ),
)
print(f"Agent created: {agent.name}, version: {agent.version}")

# Create conversation and send request with runtime values
conversation = openai.conversations.create()
response = openai.responses.create(
    conversation=conversation.id,
    input="Hello! Can you confirm my details?",
    extra_body={
        "agent_reference": {"name": agent.name, "type": "agent_reference"},
        "structured_inputs": {"userName": "Alice Smith", "userRole": "Senior Developer"},
    },
)
print(response.output_text)
```

### Expected output

```console
Agent created: structured-input-agent, version: 1
Hello Alice Smith! I can confirm your details: your name is Alice Smith and your role is Senior Developer. How can I help you today?
```

The agent replaces the `{{userName}}` and `{{userRole}}` placeholders in the instructions with "Alice Smith" and "Senior Developer" before processing the request.

:::zone-end

:::zone pivot="csharp"

```csharp
using System;
using Azure.AI.Projects;
using Azure.AI.Projects.Agents;
using Azure.AI.Extensions.OpenAI;
using Azure.Identity;
using OpenAI.Responses;

// Format: "https://resource_name.ai.azure.com/api/projects/project_name"
var projectEndpoint = "your_project_endpoint";

// Create project client to call Foundry API
AIProjectClient projectClient = new(
    endpoint: new Uri(projectEndpoint),
    tokenProvider: new DefaultAzureCredential());

// Create agent with handlebar templates in instructions
DeclarativeAgentDefinition agentDefinition = new(model: "gpt-5-mini")
{
    Instructions = "You are a helpful assistant. "
        + "The user's name is {{userName}} and their role is {{userRole}}. "
        + "Greet them and confirm their details.",
    StructuredInputs =
    {
        ["userName"] = new StructuredInputDefinition
            { Description = "The user's name", IsRequired = true },
        ["userRole"] = new StructuredInputDefinition
            { Description = "The user's role", IsRequired = true }
    }
};
AgentVersion agent = projectClient.AgentAdministrationClient.CreateAgentVersion(
    agentName: "structured-input-agent", options: new(agentDefinition));

// Send response with runtime structured input values
AgentReference agentRef = new(name: agent.Name, version: agent.Version);
ProjectResponsesClient responseClient =
    projectClient.ProjectOpenAIClient.GetProjectResponsesClientForAgent(agentRef);

CreateResponseOptions responseOptions = new()
{
    Input = [ResponseItem.CreateUserMessageItem("Hello! Can you confirm my details?")]
};
responseOptions.Patch.Set(
    "$.structured_inputs[\"userName\"]"u8,
    BinaryData.FromObjectAsJson("Alice Smith"));
responseOptions.Patch.Set(
    "$.structured_inputs[\"userRole\"]"u8,
    BinaryData.FromObjectAsJson("Senior Developer"));

ResponseResult response = responseClient.CreateResponse(responseOptions);
Console.WriteLine(response.GetOutputText());

// Clean up
projectClient.AgentAdministrationClient.DeleteAgentVersion(
    agentName: agent.Name, agentVersion: agent.Version);
```

### Expected output

```console
Hello Alice Smith! I can confirm your details: your name is Alice Smith and your role is Senior Developer. How can I help you today?
```

The `StructuredInputs` dictionary on the agent definition maps template names to their schemas. At runtime, use the `Patch.Set` method on `CreateResponseOptions` to supply the actual values via the `$.structured_inputs` JSON path.

:::zone-end

:::zone pivot="typescript"

```typescript
import { DefaultAzureCredential } from "@azure/identity";
import { AIProjectClient } from "@azure/ai-projects";

// Format: "https://resource_name.ai.azure.com/api/projects/project_name"
const PROJECT_ENDPOINT = "your_project_endpoint";

export async function main(): Promise<void> {
  // Create clients to call Foundry API
  const project = new AIProjectClient(PROJECT_ENDPOINT, new DefaultAzureCredential());
  const openai = project.getOpenAIClient();

  // Create agent with handlebar templates in instructions
  const agent = await project.agents.createVersion("structured-input-agent", {
    kind: "prompt",
    model: "gpt-5-mini",
    instructions:
      "You are a helpful assistant. " +
      "The user's name is {{userName}} and their role is {{userRole}}. " +
      "Greet them and confirm their details.",
    structured_inputs: {
      userName: { description: "The user's name", required: true },
      userRole: { description: "The user's role", required: true },
    },
  });
  console.log(`Agent created: ${agent.name}, version: ${agent.version}`);

  // Create conversation and send request with runtime values
  const conversation = await openai.conversations.create();
  const response = await openai.responses.create(
    {
      conversation: conversation.id,
      input: "Hello! Can you confirm my details?",
    },
    {
      body: {
        agent_reference: { name: agent.name, type: "agent_reference" },
        structured_inputs: { userName: "Alice Smith", userRole: "Senior Developer" },
      },
    },
  );
  console.log(response.output_text);

  // Clean up
  await project.agents.deleteVersion(agent.name, agent.version);
}

main().catch(console.error);
```

### Expected output

```console
Agent created: structured-input-agent, version: 1
Hello Alice Smith! I can confirm your details: your name is Alice Smith and your role is Senior Developer. How can I help you today?
```

The agent definition uses `structured_inputs` to declare the template schemas. At runtime, pass the actual values in the `body` parameter alongside the `agent_reference`.

:::zone-end

:::zone pivot="java"

Add the dependency to your `pom.xml`:

```xml
<dependency>
    <groupId>com.azure</groupId>
    <artifactId>azure-ai-agents</artifactId>
    <version>2.0.0</version>
</dependency>
```

```java
import com.azure.ai.agents.AgentsClient;
import com.azure.ai.agents.AgentsClientBuilder;
import com.azure.ai.agents.AgentsServiceVersion;
import com.azure.ai.agents.ResponsesClient;
import com.azure.ai.agents.models.AgentReference;
import com.azure.ai.agents.models.AgentVersionDetails;
import com.azure.ai.agents.models.AzureCreateResponseOptions;
import com.azure.ai.agents.models.PromptAgentDefinition;
import com.azure.ai.agents.models.StructuredInputDefinition;
import com.azure.core.util.BinaryData;
import com.azure.identity.DefaultAzureCredentialBuilder;
import com.openai.models.responses.Response;
import com.openai.models.responses.ResponseCreateParams;

import java.util.LinkedHashMap;
import java.util.Map;

public class StructuredInputInstructionsExample {
    public static void main(String[] args) {
        // Format: "https://resource_name.ai.azure.com/api/projects/project_name"
        String projectEndpoint = "your_project_endpoint";

        AgentsClientBuilder builder = new AgentsClientBuilder()
            .credential(new DefaultAzureCredentialBuilder().build())
            .endpoint(projectEndpoint)
            .serviceVersion(AgentsServiceVersion.getLatest());

        AgentsClient agentsClient = builder.buildAgentsClient();
        ResponsesClient responsesClient = builder.buildResponsesClient();

        // Define structured input schemas
        Map<String, StructuredInputDefinition> inputDefs = new LinkedHashMap<>();
        inputDefs.put("userName",
            new StructuredInputDefinition().setDescription("The user's name").setRequired(true));
        inputDefs.put("userRole",
            new StructuredInputDefinition().setDescription("The user's role").setRequired(true));

        // Create agent with handlebar templates in instructions
        AgentVersionDetails agent = agentsClient.createAgentVersion(
            "structured-input-agent",
            new PromptAgentDefinition("gpt-5-mini")
                .setInstructions("You are a helpful assistant. "
                    + "The user's name is {{userName}} and their role is {{userRole}}. "
                    + "Greet them and confirm their details.")
                .setStructuredInputs(inputDefs));

        // Supply structured input values at runtime
        Map<String, BinaryData> inputValues = new LinkedHashMap<>();
        inputValues.put("userName", BinaryData.fromObject("Alice Smith"));
        inputValues.put("userRole", BinaryData.fromObject("Senior Developer"));

        Response response = responsesClient.createAzureResponse(
            new AzureCreateResponseOptions()
                .setAgentReference(
                    new AgentReference(agent.getName()).setVersion(agent.getVersion()))
                .setStructuredInputs(inputValues),
            ResponseCreateParams.builder()
                .input("Hello! Can you confirm my details?"));

        System.out.println("Response: " + response.output());

        // Clean up
        agentsClient.deleteAgentVersion(agent.getName(), agent.getVersion());
    }
}
```

### Expected output

```console
Response: Hello Alice Smith! I can confirm your details: your name is Alice Smith and your role is Senior Developer. How can I help you today?
```

The Java SDK uses `StructuredInputDefinition` for the agent schema and `Map<String, BinaryData>` for the runtime values passed through `AzureCreateResponseOptions`.

:::zone-end

:::zone pivot="rest"

### Create an agent with structured inputs

```bash
curl -X POST "$FOUNDRY_PROJECT_ENDPOINT/agents?api-version=v1" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -d '{
    "name": "structured-input-agent",
    "definition": {
      "kind": "prompt",
      "model": "<MODEL_DEPLOYMENT>",
      "instructions": "You are a helpful assistant. The user'\''s name is {{userName}} and their role is {{userRole}}. Greet them and confirm their details.",
      "structured_inputs": {
        "userName": {
          "type": "string",
          "description": "The user'\''s name",
          "default_value": "Unknown"
        },
        "userRole": {
          "type": "string",
          "description": "The user'\''s role",
          "default_value": "User"
        }
      }
    }
  }'
```

### Create a response with structured input values

```bash
curl -X POST "$FOUNDRY_PROJECT_ENDPOINT/openai/v1/responses" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -d '{
    "agent_reference": {
      "type": "agent_reference",
      "name": "structured-input-agent"
    },
    "input": [
      {
        "type": "message",
        "role": "user",
        "content": "Hello! Can you confirm my details?"
      }
    ],
    "structured_inputs": {
      "userName": "Alice Smith",
      "userRole": "Senior Developer"
    }
  }'
```

The agent definition's `structured_inputs` object declares the schemas with descriptions and default values. The response request's `structured_inputs` provides the actual runtime values that replace the `{{userName}}` and `{{userRole}}` templates.

:::zone-end

## Use structured inputs with Code Interpreter

By using structured inputs, you can dynamically configure which files and containers the Code Interpreter tool uses at runtime. Define handlebar templates in the tool's `file_ids` or `container` properties, and then supply actual IDs when creating a response.

:::zone pivot="python"

```python
from io import BytesIO
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    PromptAgentDefinition,
    CodeInterpreterTool,
    AutoCodeInterpreterToolParam,
    StructuredInputDefinition,
)
from azure.identity import DefaultAzureCredential

# Format: "https://resource_name.ai.azure.com/api/projects/project_name"
PROJECT_ENDPOINT = "your_project_endpoint"

# Create clients to call Foundry API
project = AIProjectClient(endpoint=PROJECT_ENDPOINT, credential=DefaultAzureCredential())
openai = project.get_openai_client()

# Upload a CSV file for the code interpreter
csv_file = BytesIO(b"x\n1\n2\n3\n")
csv_file.name = "numbers.csv"
uploaded = openai.files.create(purpose="assistants", file=csv_file)
print(f"File uploaded (id: {uploaded.id})")

# Create agent with a template placeholder for the file ID
tool = CodeInterpreterTool(
    container=AutoCodeInterpreterToolParam(file_ids=["{{analysis_file_id}}"])
)
agent = project.agents.create_version(
    agent_name="code-interp-structured",
    definition=PromptAgentDefinition(
        model="gpt-5-mini",
        instructions="You are a helpful data analyst.",
        tools=[tool],
        structured_inputs={
            "analysis_file_id": StructuredInputDefinition(
                description="File ID for the code interpreter",
                required=True,
                schema={"type": "string"},
            ),
        },
    ),
)

# Supply the actual file ID at runtime
conversation = openai.conversations.create()
response = openai.responses.create(
    conversation=conversation.id,
    input="Read numbers.csv and return the sum of x.",
    extra_body={
        "agent_reference": {"name": agent.name, "type": "agent_reference"},
        "structured_inputs": {"analysis_file_id": uploaded.id},
    },
    tool_choice="required",
)
print(response.output_text)
```

### Expected output

```console
File uploaded (id: <file-id>)
The sum of x in numbers.csv is 6.
```

The `{{analysis_file_id}}` placeholder in the tool's `file_ids` array is replaced by the actual file ID at runtime. By using this approach, you can reuse the same agent definition with different files for each request.

:::zone-end

:::zone pivot="csharp"

```csharp
using System;
using Azure.AI.Projects;
using Azure.AI.Projects.Agents;
using Azure.AI.Extensions.OpenAI;
using Azure.Identity;
using OpenAI.Responses;

// Format: "https://resource_name.ai.azure.com/api/projects/project_name"
var projectEndpoint = "your_project_endpoint";

// Create project client to call Foundry API
AIProjectClient projectClient = new(
    endpoint: new Uri(projectEndpoint),
    tokenProvider: new DefaultAzureCredential());

// Create agent with a structured input placeholder for the file ID
DeclarativeAgentDefinition agentDefinition = new(model: "gpt-5-mini")
{
    Instructions = "You are a helpful data analyst.",
    Tools = {
        ResponseTool.CreateCodeInterpreterTool(
            new CodeInterpreterToolContainer(
                CodeInterpreterToolContainerConfiguration
                    .CreateAutomaticContainerConfiguration(
                        fileIds: ["{{analysis_file_id}}"])))
    },
    StructuredInputs =
    {
        ["analysis_file_id"] = new StructuredInputDefinition
            { Description = "File ID for the code interpreter", IsRequired = true }
    }
};
AgentVersion agent = projectClient.AgentAdministrationClient.CreateAgentVersion(
    agentName: "code-interp-structured", options: new(agentDefinition));

// Supply the actual file ID at runtime
AgentReference agentRef = new(name: agent.Name, version: agent.Version);
ProjectResponsesClient responseClient =
    projectClient.ProjectOpenAIClient.GetProjectResponsesClientForAgent(agentRef);

CreateResponseOptions responseOptions = new()
{
    Input = [ResponseItem.CreateUserMessageItem(
        "Read numbers.csv and return the sum of x.")]
};
responseOptions.Patch.Set(
    "$.structured_inputs[\"analysis_file_id\"]"u8,
    BinaryData.FromObjectAsJson("<uploaded-file-id>"));

ResponseResult response = responseClient.CreateResponse(responseOptions);
Console.WriteLine(response.GetOutputText());

// Clean up
projectClient.AgentAdministrationClient.DeleteAgentVersion(
    agentName: agent.Name, agentVersion: agent.Version);
```

### Expected output

```console
The sum of x in numbers.csv is 6.
```

:::zone-end

:::zone pivot="typescript"

```typescript
import { DefaultAzureCredential } from "@azure/identity";
import { AIProjectClient } from "@azure/ai-projects";

// Format: "https://resource_name.ai.azure.com/api/projects/project_name"
const PROJECT_ENDPOINT = "your_project_endpoint";

export async function main(): Promise<void> {
  const project = new AIProjectClient(PROJECT_ENDPOINT, new DefaultAzureCredential());
  const openai = project.getOpenAIClient();

  // Upload a file for code interpreter
  const file = new File(["x\n1\n2\n3\n"], "numbers.csv");
  const uploaded = await openai.files.create({ file, purpose: "assistants" });
  console.log(`File uploaded (id: ${uploaded.id})`);

  // Create agent with a template placeholder for the file ID
  const agent = await project.agents.createVersion("code-interp-structured", {
    kind: "prompt",
    model: "gpt-5-mini",
    instructions: "You are a helpful data analyst.",
    tools: [
      {
        type: "code_interpreter",
        container: { type: "auto", file_ids: ["{{analysis_file_id}}"] },
      },
    ],
    structured_inputs: {
      analysis_file_id: {
        description: "File ID for the code interpreter",
        required: true,
      },
    },
  });

  // Supply the actual file ID at runtime
  const conversation = await openai.conversations.create();
  const response = await openai.responses.create(
    {
      conversation: conversation.id,
      input: "Read numbers.csv and return the sum of x.",
      tool_choice: "required",
    },
    {
      body: {
        agent_reference: { name: agent.name, type: "agent_reference" },
        structured_inputs: { analysis_file_id: uploaded.id },
      },
    },
  );
  console.log(response.output_text);

  // Clean up
  await project.agents.deleteVersion(agent.name, agent.version);
}

main().catch(console.error);
```

### Expected output

```console
File uploaded (id: <file-id>)
The sum of x in numbers.csv is 6.
```

:::zone-end

:::zone pivot="java"

```java
import com.azure.ai.agents.AgentsClient;
import com.azure.ai.agents.AgentsClientBuilder;
import com.azure.ai.agents.AgentsServiceVersion;
import com.azure.ai.agents.ResponsesClient;
import com.azure.ai.agents.models.*;
import com.azure.core.util.BinaryData;
import com.azure.identity.DefaultAzureCredentialBuilder;
import com.openai.models.responses.Response;
import com.openai.models.responses.ResponseCreateParams;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Map;

public class CodeInterpreterStructuredInputExample {
    public static void main(String[] args) {
        // Format: "https://resource_name.ai.azure.com/api/projects/project_name"
        String projectEndpoint = "your_project_endpoint";

        AgentsClientBuilder builder = new AgentsClientBuilder()
            .credential(new DefaultAzureCredentialBuilder().build())
            .endpoint(projectEndpoint)
            .serviceVersion(AgentsServiceVersion.getLatest());

        AgentsClient agentsClient = builder.buildAgentsClient();
        ResponsesClient responsesClient = builder.buildResponsesClient();

        // Create code interpreter tool with a template placeholder
        CodeInterpreterTool tool = new CodeInterpreterTool()
            .setContainer(new AutoCodeInterpreterToolParameter()
                .setFileIds(Arrays.asList("{{analysis_file_id}}")));

        Map<String, StructuredInputDefinition> inputDefs = new LinkedHashMap<>();
        inputDefs.put("analysis_file_id",
            new StructuredInputDefinition()
                .setDescription("File ID for the code interpreter")
                .setRequired(true));

        AgentVersionDetails agent = agentsClient.createAgentVersion(
            "code-interp-structured",
            new PromptAgentDefinition("gpt-5-mini")
                .setInstructions("You are a helpful data analyst.")
                .setTools(Arrays.asList(tool))
                .setStructuredInputs(inputDefs));

        // Supply the actual file ID at runtime
        Map<String, BinaryData> inputValues = new LinkedHashMap<>();
        inputValues.put("analysis_file_id",
            BinaryData.fromObject("<uploaded-file-id>"));

        Response response = responsesClient.createAzureResponse(
            new AzureCreateResponseOptions()
                .setAgentReference(
                    new AgentReference(agent.getName()).setVersion(agent.getVersion()))
                .setStructuredInputs(inputValues),
            ResponseCreateParams.builder()
                .input("Read numbers.csv and return the sum of x."));

        System.out.println("Response: " + response.output());

        // Clean up
        agentsClient.deleteAgentVersion(agent.getName(), agent.getVersion());
    }
}
```

### Expected output

```console
Response: The sum of x in numbers.csv is 6.
```

:::zone-end

:::zone pivot="rest"

### Create an agent with dynamic Code Interpreter files

```bash
curl -X POST "$FOUNDRY_PROJECT_ENDPOINT/agents?api-version=v1" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -d '{
    "name": "code-interp-structured",
    "definition": {
      "kind": "prompt",
      "model": "<MODEL_DEPLOYMENT>",
      "instructions": "You are a helpful data analyst.",
      "tools": [
        {
          "type": "code_interpreter",
          "container": {
            "type": "auto",
            "file_ids": ["{{analysis_file_id}}"]
          }
        }
      ],
      "structured_inputs": {
        "analysis_file_id": {
          "description": "File ID for the code interpreter",
          "required": true,
          "schema": {"type": "string"}
        }
      }
    }
  }'
```

### Create a response with the file ID

```bash
curl -X POST "$FOUNDRY_PROJECT_ENDPOINT/openai/v1/responses" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -d '{
    "agent_reference": {
      "type": "agent_reference",
      "name": "code-interp-structured"
    },
    "input": [
      {
        "type": "message",
        "role": "user",
        "content": "Read numbers.csv and return the sum of x."
      }
    ],
    "structured_inputs": {
      "analysis_file_id": "<FILE_ID>"
    },
    "tool_choice": "required"
  }'
```

The `{{analysis_file_id}}` template in `file_ids` is replaced with the actual file ID at runtime. You can define multiple file ID placeholders and leave unused ones empty. Empty values are automatically removed from the array.

:::zone-end

## Use structured inputs with File Search

By using structured inputs, you can dynamically configure which vector stores the File Search tool queries at runtime. Define template placeholders in the `vector_store_ids` array, and then supply actual vector store IDs when creating a response.

:::zone pivot="python"

```python
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    PromptAgentDefinition,
    FileSearchTool,
    StructuredInputDefinition,
)
from azure.identity import DefaultAzureCredential

# Format: "https://resource_name.ai.azure.com/api/projects/project_name"
PROJECT_ENDPOINT = "your_project_endpoint"

# Create clients to call Foundry API
project = AIProjectClient(endpoint=PROJECT_ENDPOINT, credential=DefaultAzureCredential())
openai = project.get_openai_client()

# Create a vector store and upload a file
vector_store = openai.vector_stores.create(name="ProductInfoStore")
with open("product_info.md", "rb") as f:
    file = openai.vector_stores.files.upload_and_poll(
        vector_store_id=vector_store.id, file=f
    )
print(f"Vector store created (id: {vector_store.id})")

# Create agent with a template placeholder for vector store ID
tool = FileSearchTool(vector_store_ids=["{{vector_store_id}}"])
agent = project.agents.create_version(
    agent_name="file-search-structured",
    definition=PromptAgentDefinition(
        model="gpt-5-mini",
        instructions="You are a helpful assistant that searches product information.",
        tools=[tool],
        structured_inputs={
            "vector_store_id": StructuredInputDefinition(
                description="Vector store ID for file search",
                required=True,
                schema={"type": "string"},
            ),
        },
    ),
)

# Supply the actual vector store ID at runtime
conversation = openai.conversations.create()
response = openai.responses.create(
    conversation=conversation.id,
    input="Tell me about Contoso products",
    extra_body={
        "agent_reference": {"name": agent.name, "type": "agent_reference"},
        "structured_inputs": {"vector_store_id": vector_store.id},
    },
)
print(response.output_text)
```

### Expected output

```console
Vector store created (id: <vector-store-id>)
Based on the product information, Contoso offers several product lines including...
```

The `{{vector_store_id}}` placeholder is replaced with the actual vector store ID at runtime. You can define multiple vector store placeholders to enable tiered or context-specific knowledge bases.

:::zone-end

:::zone pivot="csharp"

```csharp
using System;
using Azure.AI.Projects;
using Azure.AI.Projects.Agents;
using Azure.AI.Extensions.OpenAI;
using Azure.Identity;
using OpenAI.Responses;

// Format: "https://resource_name.ai.azure.com/api/projects/project_name"
var projectEndpoint = "your_project_endpoint";

AIProjectClient projectClient = new(
    endpoint: new Uri(projectEndpoint),
    tokenProvider: new DefaultAzureCredential());

// Create agent with a template placeholder for vector store ID
DeclarativeAgentDefinition agentDefinition = new(model: "gpt-5-mini")
{
    Instructions = "You are a helpful assistant that searches product information.",
    Tools = {
        ResponseTool.CreateFileSearchTool(
            vectorStoreIds: ["{{vector_store_id}}"])
    },
    StructuredInputs =
    {
        ["vector_store_id"] = new StructuredInputDefinition
            { Description = "Vector store ID for file search", IsRequired = true }
    }
};
AgentVersion agent = projectClient.AgentAdministrationClient.CreateAgentVersion(
    agentName: "file-search-structured", options: new(agentDefinition));

// Supply the actual vector store ID at runtime
AgentReference agentRef = new(name: agent.Name, version: agent.Version);
ProjectResponsesClient responseClient =
    projectClient.ProjectOpenAIClient.GetProjectResponsesClientForAgent(agentRef);

CreateResponseOptions responseOptions = new()
{
    Input = [ResponseItem.CreateUserMessageItem("Tell me about Contoso products")]
};
responseOptions.Patch.Set(
    "$.structured_inputs[\"vector_store_id\"]"u8,
    BinaryData.FromObjectAsJson("<vector-store-id>"));

ResponseResult response = responseClient.CreateResponse(responseOptions);
Console.WriteLine(response.GetOutputText());

// Clean up
projectClient.AgentAdministrationClient.DeleteAgentVersion(
    agentName: agent.Name, agentVersion: agent.Version);
```

### Expected output

```console
Based on the product information, Contoso offers several product lines including...
```

:::zone-end

:::zone pivot="typescript"

```typescript
import { DefaultAzureCredential } from "@azure/identity";
import { AIProjectClient } from "@azure/ai-projects";

// Format: "https://resource_name.ai.azure.com/api/projects/project_name"
const PROJECT_ENDPOINT = "your_project_endpoint";

export async function main(): Promise<void> {
  const project = new AIProjectClient(PROJECT_ENDPOINT, new DefaultAzureCredential());
  const openai = project.getOpenAIClient();

  // Create a vector store (assumes file already uploaded)
  const vectorStore = await openai.vectorStores.create({ name: "ProductInfoStore" });
  console.log(`Vector store created (id: ${vectorStore.id})`);

  // Create agent with a template placeholder for vector store ID
  const agent = await project.agents.createVersion("file-search-structured", {
    kind: "prompt",
    model: "gpt-5-mini",
    instructions: "You are a helpful assistant that searches product information.",
    tools: [
      {
        type: "file_search",
        vector_store_ids: ["{{vector_store_id}}"],
      },
    ],
    structured_inputs: {
      vector_store_id: {
        description: "Vector store ID for file search",
        required: true,
      },
    },
  });

  // Supply the actual vector store ID at runtime
  const conversation = await openai.conversations.create();
  const response = await openai.responses.create(
    {
      conversation: conversation.id,
      input: "Tell me about Contoso products",
    },
    {
      body: {
        agent_reference: { name: agent.name, type: "agent_reference" },
        structured_inputs: { vector_store_id: vectorStore.id },
      },
    },
  );
  console.log(response.output_text);

  // Clean up
  await project.agents.deleteVersion(agent.name, agent.version);
}

main().catch(console.error);
```

### Expected output

```console
Vector store created (id: <vector-store-id>)
Based on the product information, Contoso offers several product lines including...
```

:::zone-end

:::zone pivot="java"

```java
import com.azure.ai.agents.AgentsClient;
import com.azure.ai.agents.AgentsClientBuilder;
import com.azure.ai.agents.AgentsServiceVersion;
import com.azure.ai.agents.ResponsesClient;
import com.azure.ai.agents.models.AgentReference;
import com.azure.ai.agents.models.AgentVersionDetails;
import com.azure.ai.agents.models.AzureCreateResponseOptions;
import com.azure.ai.agents.models.FileSearchTool;
import com.azure.ai.agents.models.PromptAgentDefinition;
import com.azure.ai.agents.models.StructuredInputDefinition;
import com.azure.core.util.BinaryData;
import com.azure.identity.DefaultAzureCredentialBuilder;
import com.openai.models.responses.Response;
import com.openai.models.responses.ResponseCreateParams;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Map;

public class FileSearchStructuredInputExample {
    public static void main(String[] args) {
        // Format: "https://resource_name.ai.azure.com/api/projects/project_name"
        String projectEndpoint = "your_project_endpoint";

        AgentsClientBuilder builder = new AgentsClientBuilder()
            .credential(new DefaultAzureCredentialBuilder().build())
            .endpoint(projectEndpoint)
            .serviceVersion(AgentsServiceVersion.getLatest());

        AgentsClient agentsClient = builder.buildAgentsClient();
        ResponsesClient responsesClient = builder.buildResponsesClient();

        // Create agent with a template placeholder for vector store ID
        FileSearchTool tool = new FileSearchTool()
            .setVectorStoreIds(Arrays.asList("{{vector_store_id}}"));

        Map<String, StructuredInputDefinition> inputDefs = new LinkedHashMap<>();
        inputDefs.put("vector_store_id",
            new StructuredInputDefinition()
                .setDescription("Vector store ID for file search")
                .setRequired(true));

        AgentVersionDetails agent = agentsClient.createAgentVersion(
            "file-search-structured",
            new PromptAgentDefinition("gpt-5-mini")
                .setInstructions(
                    "You are a helpful assistant that searches product information.")
                .setTools(Arrays.asList(tool))
                .setStructuredInputs(inputDefs));

        // Supply the actual vector store ID at runtime
        Map<String, BinaryData> inputValues = new LinkedHashMap<>();
        inputValues.put("vector_store_id",
            BinaryData.fromObject("<vector-store-id>"));

        Response response = responsesClient.createAzureResponse(
            new AzureCreateResponseOptions()
                .setAgentReference(
                    new AgentReference(agent.getName()).setVersion(agent.getVersion()))
                .setStructuredInputs(inputValues),
            ResponseCreateParams.builder()
                .input("Tell me about Contoso products"));

        System.out.println("Response: " + response.output());

        // Clean up
        agentsClient.deleteAgentVersion(agent.getName(), agent.getVersion());
    }
}
```

### Expected output

```console
Response: Based on the product information, Contoso offers several product lines including...
```

:::zone-end

:::zone pivot="rest"

### Create an agent with dynamic file search vector stores

```bash
curl -X POST "$FOUNDRY_PROJECT_ENDPOINT/agents?api-version=v1" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -d '{
    "name": "file-search-structured",
    "definition": {
      "kind": "prompt",
      "model": "<MODEL_DEPLOYMENT>",
      "instructions": "You are a helpful assistant that searches product information.",
      "tools": [
        {
          "type": "file_search",
          "vector_store_ids": [
            "vs_base_kb",
            "{{tier_specific_kb}}"
          ]
        }
      ],
      "structured_inputs": {
        "tier_specific_kb": {
          "description": "Vector store ID for customer tier",
          "required": true,
          "schema": {"type": "string"}
        }
      }
    }
  }'
```

### Create a response with the vector store ID

```bash
curl -X POST "$FOUNDRY_PROJECT_ENDPOINT/openai/v1/responses" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -d '{
    "agent_reference": {
      "type": "agent_reference",
      "name": "file-search-structured"
    },
    "input": [
      {
        "type": "message",
        "role": "user",
        "content": "Tell me about Contoso products"
      }
    ],
    "structured_inputs": {
      "tier_specific_kb": "vs_premium_kb_2024"
    }
  }'
```

This example combines a static vector store (`vs_base_kb`) with a dynamic one (`{{tier_specific_kb}}`). The template placeholder is replaced at runtime, and the process automatically removes any empty string values in the array.

:::zone-end

## Use structured inputs with MCP servers

By using structured inputs, you can dynamically configure MCP server connections at runtime. You can set the server URL, authentication headers, and server label. By using this approach, a single agent definition can connect to different MCP servers depending on the context.

The following JSON shows the request body for the [Create Agent Version](/rest/api/aifoundry/aiproject#agents---create-agent-version) operation (`POST /agents?api-version=v1`). The agent definition includes MCP tool properties with handlebar template placeholders:

```json
{
  "name": "mcp-dynamic-agent",
  "definition": {
    "kind": "prompt",
    "model": "gpt-4o",
    "instructions": "You are a development assistant for {{project_name}}.",
    "tools": [
      {
        "type": "mcp",
        "server_label": "{{server_label}}",
        "server_url": "{{server_url}}",
        "require_approval": "never",
        "headers": {
          "Authorization": "{{auth_token}}",
          "X-Project-ID": "{{project_id}}"
        }
      }
    ],
    "structured_inputs": {
      "project_name": {
        "description": "Project name",
        "required": true
      },
      "server_label": {
        "description": "MCP server label",
        "required": true,
        "schema": {"type": "string"}
      },
      "server_url": {
        "description": "MCP server URL",
        "required": true,
        "schema": {"type": "string"}
      },
      "auth_token": {
        "description": "Authentication token",
        "required": true,
        "schema": {"type": "string"}
      },
      "project_id": {
        "description": "Project identifier",
        "required": true,
        "schema": {"type": "string"}
      }
    }
  }
}
```

At runtime, supply the actual server configuration values in the request body for the Create Response operation (`POST /openai/v1/responses`):

```json
{
  "agent_reference": {
    "type": "agent_reference",
    "name": "mcp-dynamic-agent"
  },
  "input": [{"type": "message", "role": "user", "content": "List recent commits"}],
  "structured_inputs": {
    "project_name": "CloudSync API",
    "server_label": "cloudsync-repo",
    "server_url": "https://gitmcp.io/myorg/cloudsync-api",
    "auth_token": "Bearer ghp_xxxxxxxxxxxx",
    "project_id": "proj_12345"
  }
}
```

The SDK patterns for MCP structured inputs follow the same approach shown in the previous examples. Define the template placeholders in the MCP tool properties, declare the structured input schemas in the agent definition, and supply the values at runtime.

The following Python example shows the complete pattern:

```python
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    MCPTool,
    PromptAgentDefinition,
    StructuredInputDefinition,
)
from azure.identity import DefaultAzureCredential

# Format: "https://resource_name.ai.azure.com/api/projects/project_name"
PROJECT_ENDPOINT = "your_project_endpoint"

# Create clients to call Foundry API
project = AIProjectClient(endpoint=PROJECT_ENDPOINT, credential=DefaultAzureCredential())
openai = project.get_openai_client()

# Create MCP tool with template placeholders
tool = MCPTool(
    server_label="{{server_label}}",
    server_url="{{server_url}}",
    require_approval="never",
    headers={"Authorization": "{{auth_token}}", "X-Project-ID": "{{project_id}}"},
)

# Create agent with structured inputs for MCP configuration
agent = project.agents.create_version(
    agent_name="mcp-dynamic-agent",
    definition=PromptAgentDefinition(
        model="gpt-5-mini",
        instructions="You are a helpful development assistant for {{project_name}}.",
        tools=[tool],
        structured_inputs={
            "project_name": StructuredInputDefinition(
                description="Project name", required=True, schema={"type": "string"},
            ),
            "server_label": StructuredInputDefinition(
                description="MCP server label", required=True, schema={"type": "string"},
            ),
            "server_url": StructuredInputDefinition(
                description="MCP server URL", required=True, schema={"type": "string"},
            ),
            "auth_token": StructuredInputDefinition(
                description="Authentication token", required=True, schema={"type": "string"},
            ),
            "project_id": StructuredInputDefinition(
                description="Project identifier", required=True, schema={"type": "string"},
            ),
        },
    ),
)

# Supply MCP server configuration at runtime
conversation = openai.conversations.create()
response = openai.responses.create(
    conversation=conversation.id,
    input="List recent commits",
    extra_body={
        "agent_reference": {"name": agent.name, "type": "agent_reference"},
        "structured_inputs": {
            "project_name": "CloudSync API",
            "server_label": "cloudsync-repo",
            "server_url": "https://gitmcp.io/myorg/cloudsync-api",
            "auth_token": "Bearer ghp_xxxxxxxxxxxx",
            "project_id": "proj_12345",
        },
    },
)
print(response.output_text)
```

For more information about connecting to MCP servers, see [Connect agents to MCP servers](tools/model-context-protocol.md).

## Use structured inputs in the Responses API

You can use handlebar templates directly in Responses API calls without defining them in the agent definition. This approach works for response-level instructions and for system or developer messages in the input array.

### Response-level instructions with structured inputs

Pass structured inputs alongside `instructions` in a response request to parameterize the system prompt:

```json
{
  "instructions": "You are assisting {{customerName}} from {{companyName}} located in {{location}}.",
  "input": [
    {
      "type": "message",
      "role": "user",
      "content": "Hello, who am I?"
    }
  ],
  "structured_inputs": {
    "customerName": "Bob Johnson",
    "companyName": "Tech Corp",
    "location": "San Francisco"
  },
  "model": "gpt-4o"
}
```

### System and developer messages with structured inputs

Use handlebar templates in system and developer message content to inject runtime values into the conversation context:

```json
{
  "instructions": "You are a helpful assistant.",
  "input": [
    {
      "type": "message",
      "role": "system",
      "content": "The user's name is {{userName}} and they work in {{department}}."
    },
    {
      "type": "message",
      "role": "developer",
      "content": [
        {
          "type": "input_text",
          "text": "User role: {{userRole}}. Always be professional."
        }
      ]
    },
    {
      "type": "message",
      "role": "user",
      "content": "Hello, can you confirm my details?"
    }
  ],
  "structured_inputs": {
    "userName": "Sarah Connor",
    "department": "Engineering",
    "userRole": "Tech Lead"
  },
  "model": "gpt-4o"
}
```

In SDK code, pass these values by using the same `extra_body` (Python), `body` (TypeScript), or `AzureCreateResponseOptions` (Java/C#) patterns shown in the previous examples.

The following Python example shows how to use response-level instructions with structured inputs:

```python
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

# Format: "https://resource_name.ai.azure.com/api/projects/project_name"
PROJECT_ENDPOINT = "your_project_endpoint"

# Create clients to call Foundry API
project = AIProjectClient(endpoint=PROJECT_ENDPOINT, credential=DefaultAzureCredential())
openai = project.get_openai_client()

# Pass structured inputs with response-level instructions
response = openai.responses.create(
    model="gpt-5-mini",
    instructions="You are assisting {{customerName}} from {{companyName}} located in {{location}}.",
    input=[
        {
            "type": "message",
            "role": "user",
            "content": "Hello, who am I?",
        }
    ],
    extra_body={
        "structured_inputs": {
            "customerName": "Bob Johnson",
            "companyName": "Tech Corp",
            "location": "San Francisco",
        },
    },
)
print(response.output_text)
```

## Advanced template syntax

Structured inputs support full [Handlebars](https://handlebarsjs.com/) template syntax beyond simple variable substitution. You can use conditionals, loops, and other built-in helpers to create dynamic instruction logic within a single agent definition.

The following example creates a weather assistant whose behavior adapts based on runtime inputs. The instructions template uses `{{#if}}` for conditional sections and `{{#each}}` to iterate over a list of user preferences:

```python
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition, StructuredInputDefinition
from azure.identity import DefaultAzureCredential

# Format: "https://resource_name.ai.azure.com/api/projects/project_name"
PROJECT_ENDPOINT = "your_project_endpoint"

# Create clients to call Foundry API
project = AIProjectClient(endpoint=PROJECT_ENDPOINT, credential=DefaultAzureCredential())
openai = project.get_openai_client()

# Define instructions with conditionals and loops
instructions = """You are a weather assistant. Provide a helpful weather summary for the user.

The user asked about: {{location}}
Use the following units: {{units}}

{{#if includeForecast}}
Include a brief multi-day forecast in your response.
{{else}}
Focus only on the current conditions.
{{/if}}

{{#if preferences}}
The user has these additional preferences:
{{#each preferences}}
- {{this}}
{{/each}}
{{/if}}

Keep the final answer clear and easy to read."""

agent = project.agents.create_version(
    agent_name="weather-assistant",
    definition=PromptAgentDefinition(
        model="gpt-5-mini",
        instructions=instructions,
        structured_inputs={
            "location": StructuredInputDefinition(
                description="City or region to check weather for",
                required=True,
                schema={"type": "string"},
            ),
            "units": StructuredInputDefinition(
                description="Temperature units (Celsius or Fahrenheit)",
                default_value="Celsius",
                schema={"type": "string"},
            ),
            "includeForecast": StructuredInputDefinition(
                description="Whether to include a multi-day forecast",
                default_value="false",
                schema={"type": "boolean"},
            ),
            "preferences": StructuredInputDefinition(
                description="Additional user preferences",
                schema={"type": "array"},
            ),
        },
    ),
)

# Supply values at runtime — conditionals and loops resolve automatically
conversation = openai.conversations.create()
response = openai.responses.create(
    conversation=conversation.id,
    input="What's the weather like?",
    extra_body={
        "agent_reference": {"name": agent.name, "type": "agent_reference"},
        "structured_inputs": {
            "location": "Seattle, WA",
            "units": "Fahrenheit",
            "includeForecast": True,
            "preferences": ["Highlight UV index", "Include wind speed"],
        },
    },
)
print(response.output_text)
```

With these values, the resolved instructions become:

> You are a weather assistant. Provide a helpful weather summary for the user.
>
> The user asked about: Seattle, WA
> 
> Use the following units: Fahrenheit
>
> Include a brief multi-day forecast in your response.
>
> The user has these additional preferences:
> - Highlight UV index
> - Include wind speed
>
> Keep the final answer clear and easy to read.

The following table summarizes the supported Handlebars helpers:

| Helper | Syntax | Description |
|--------|--------|-------------|
| Conditional | `{{#if value}}...{{else}}...{{/if}}` | Render content based on a truthy or falsy value |
| Negation | `{{#unless value}}...{{/unless}}` | Render content when a value is falsy |
| Loop | `{{#each array}}{{this}}{{/each}}` | Iterate over array items |
| Last item check | `{{#unless @last}}, {{/unless}}` | Conditionally render separators between loop items |

## Related content

- [Code Interpreter tool for Foundry agents](tools/code-interpreter.md)
- [File search tool for agents](tools/file-search.md)
- [Connect agents to MCP servers](tools/model-context-protocol.md)
- [Agent development lifecycle](../concepts/development-lifecycle.md)
- [Agent runtime components](../concepts/runtime-components.md)
