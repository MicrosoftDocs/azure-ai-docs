---
title: 'How to use Azure AI Foundry Agent Service Code Interpreter'
titleSuffix: Azure AI Foundry
description: Learn how to use Azure AI Foundry Agent Service Code Interpreter
services: cognitive-services
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: how-to
ms.date: 10/14/2025
author: aahill
ms.author: aahi
ms.custom: azure-ai-agents
monikerRange: 'foundry-classic || foundry'
zone_pivot_groups: selection-code-interpreter
---
# Azure AI Foundry Agent Service Code Interpreter

Code Interpreter allows the agents to write and run Python code in a sandboxed execution environment. With Code Interpreter enabled, your agent can run code iteratively to solve more challenging code, math, and data analysis problems. When your Agent writes code that fails to run, it can iterate on this code by modifying and running different code until the code execution succeeds.

> [!IMPORTANT]
> Code Interpreter has [additional charges](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/) beyond the token based fees for Azure OpenAI usage. If your Agent calls Code Interpreter simultaneously in two different threads, two code interpreter sessions are created. Each session is active by default for 1 hour with an idle timeout of 30 minutes.

## Prerequisites

- A [basic or standard agent environment](../../environment-setup.md).


## Code samples
<!--
Use the following file search tool samples to implement it in your agents. You can also add this tool to agents [using the Azure AI Foundry portal](./overview.md#add-tools-to-your-agents-in-the-azure-ai-foundry-portal).
-->

:::zone pivot="python"

```python
code_interpreter = CodeInterpreterTool()

# An agent is created with the Code Interpreter capabilities:
agent = project_client.agents.create_agent(
    model=os.environ["MODEL_DEPLOYMENT_NAME"],
    name="my-agent",
    instructions="You are helpful agent",
    tools=code_interpreter.definitions,
    tool_resources=code_interpreter.resources,
)
```
::: zone-end

:::zone pivot="csharp"

```csharp
var projectEndpoint = System.Environment.GetEnvironmentVariable("ProjectEndpoint");
var modelDeploymentName = System.Environment.GetEnvironmentVariable("ModelDeploymentName");

PersistentAgentsClient client = new(projectEndpoint, new DefaultAzureCredential());

PersistentAgent agent = client.Administration.CreateAgent(
    model: modelDeploymentName,
    name: "My Friendly Test Agent",
    instructions: "You politely help with math questions. Use the code interpreter tool when asked to visualize numbers.",
    tools: [new CodeInterpreterToolDefinition()]
);
```

::: zone-end

:::zone pivot="javascript"

```javascript
// Create the code interpreter tool
const codeInterpreterTool = ToolUtility.createCodeInterpreterTool();

// Enable the code interpreter tool during agent creation
const agent = await client.createAgent("gpt-4o", {
  name: "my-agent",
  instructions: "You are a helpful agent",
  tools: [codeInterpreterTool.definition],
  toolResources: codeInterpreterTool.resources,
});
console.log(`Created agent, agent ID: ${agent.id}`);
```

::: zone-end

:::zone pivot="rest-api"

### Create an agent with the code interpreter tool

```bash
curl --request POST \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/assistants?api-version=$API_VERSION \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "instructions": "You are an AI assistant that can write code to help answer math questions.",
    "tools": [
      { "type": "code_interpreter" }
    ],
    "model": "gpt-4o-mini",
    "tool_resources"{
      "code interpreter": {
      }
    }
  }'
```

::: zone-end

:::zone pivot="java"

```java 
String agentName = "code_interpreter_agent";
CodeInterpreterToolDefinition ciTool = new CodeInterpreterToolDefinition();
CreateAgentOptions createAgentOptions = new CreateAgentOptions(modelName).setName(agentName).setInstructions("You are a helpful agent").setTools(Arrays.asList(ciTool));
PersistentAgent agent = administrationClient.createAgent(createAgentOptions);
```
::: zone-end

You can now ask your agents questions using the tool. For example, "*Draw a graph for a line with a slope of 4 and y-intercept of 9.*"
 
### Supported models

The [models page](../../quotas-limits.md) contains the most up-to-date information on regions/models where agents and code interpreter are supported.

We recommend using Agents with the latest models to take advantage of the new features, larger context windows, and more up-to-date training data.

### Supported file types

|File format|MIME Type|
|---|---|
|`.c`| `text/x-c` |
|`.cpp`|`text/x-c++` |
|`.csv`|`application/csv`|
|`.docx`|`application/vnd.openxmlformats-officedocument.wordprocessingml.document`|
|`.html`|`text/html`|
|`.java`|`text/x-java`|
|`.json`|`application/json`|
|`.md`|`text/markdown`|
|`.pdf`|`application/pdf`|
|`.php`|`text/x-php`|
|`.pptx`|`application/vnd.openxmlformats-officedocument.presentationml.presentation`|
|`.py`|`text/x-python`|
|`.py`|`text/x-script.python`|
|`.rb`|`text/x-ruby`|
|`.tex`|`text/x-tex`|
|`.txt`|`text/plain`|
|`.css`|`text/css`|
|`.jpeg`|`image/jpeg`|
|`.jpg`|`image/jpeg`|
|`.js`|`text/javascript`|
|`.gif`|`image/gif`|
|`.png`|`image/png`|
|`.tar`|`application/x-tar`|
|`.ts`|`application/typescript`|
|`.xlsx`|`application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`|
|`.xml`|`application/xml` or `text/xml`|
|`.zip`|`application/zip`|

## See also

* [How to use code interpreter](code-interpreter-samples.md).