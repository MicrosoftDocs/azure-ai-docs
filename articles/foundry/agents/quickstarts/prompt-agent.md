---
title: "Quickstart: Create a prompt agent"
description: "Create a prompt agent in Foundry Agent Service using the Microsoft Foundry SDK."
author: aahill
ms.author: aahi
ms.date: 03/30/2026
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: quickstart
ms.custom: build-2025
ai-usage: ai-assisted
# customer intent: As a developer, I want to create a prompt agent in Foundry Agent Service so that I can build AI-powered automation.
---

# Quickstart: Create a prompt agent

In this quickstart, you create a prompt agent in Foundry Agent Service and have a conversation with it. A prompt agent is a declaratively defined agent that combines model configuration, instructions, tools, and natural language prompts to drive behavior.

If you don't have an Azure subscription, create a [free account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

## Prerequisites

* A model deployed in Microsoft Foundry. If you don't have a model, first complete [Quickstart: Set up Microsoft Foundry resources](../../tutorials/quickstart-create-foundry-resources.md).
* The required language runtimes, global tools, and Visual Studio Code extensions as described in [Prepare your development environment](../../how-to/develop/install-cli-sdk.md).

## Set environment variables

Store [your project endpoint](../../tutorials/quickstart-create-foundry-resources.md#get-your-project-connection-details) as an environment variable. Also set these values for use in your scripts.

**Python and JavaScript**

```
PROJECT_ENDPOINT=<endpoint copied from welcome screen>
AGENT_NAME="MyAgent"
```

**C# and Java**

```
ProjectEndpoint = <endpoint copied from welcome screen>
AgentName = "MyAgent"
```

## Install packages and authenticate

[!INCLUDE [quickstart-v2-install](../../includes/quickstart-v2-install.md)]

## Create a prompt agent

Create a prompt agent using your deployed model. The agent uses a `PromptAgentDefinition` with instructions that define the agent's behavior. You can update or delete agents anytime.

# [Python](#tab/python)

:::code language="python" source="~/foundry-samples-main/samples/python/quickstart/create-agent/quickstart-create-agent.py":::

# [C#](#tab/csharp)

:::code language="csharp" source="~/foundry-samples-main/samples/csharp/quickstart/create-agent/quickstart-create-agent.cs":::

# [TypeScript](#tab/typescript)

:::code language="typescript" source="~/foundry-samples-main/samples/typescript/quickstart/create-agent/src/quickstart-create-agent.ts":::

# [Java](#tab/java)

:::code language="java" source="~/foundry-samples-main/samples/java/quickstart/create-agent/src/main/java/com/azure/ai/agents/CreateAgent.java":::

# [REST API](#tab/rest)

Replace `YOUR-FOUNDRY-RESOURCE-NAME` with your values:

:::code language="console" source="~/foundry-samples-main/samples/REST/quickstart/quickstart-create-agent.sh":::

---

The output confirms the agent was created. You see the agent name and ID printed to the console.

## Chat with the agent

Use the agent you created to interact by asking a question and a related follow-up. The conversation maintains history across these interactions.

# [Python](#tab/python)

:::code language="python" source="~/foundry-samples-main/samples/python/quickstart/chat-with-agent/quickstart-chat-with-agent.py":::

# [C#](#tab/csharp)

:::code language="csharp" source="~/foundry-samples-main/samples/csharp/quickstart/chat-with-agent/quickstart-chat-with-agent.cs":::

# [TypeScript](#tab/typescript)

:::code language="typescript" source="~/foundry-samples-main/samples/typescript/quickstart/chat-with-agent/src/quickstart-chat-with-agent.ts":::

# [Java](#tab/java)

:::code language="java" source="~/foundry-samples-main/samples/java/quickstart/chat-with-agent/src/main/java/com/azure/ai/agents/ChatWithAgent.java":::

# [REST API](#tab/rest)

Replace `YOUR-FOUNDRY-RESOURCE-NAME` with your values:

:::code language="console" source="~/foundry-samples-main/samples/REST/quickstart/quickstart-chat-with-agent.sh":::

---

You see the agent's responses to both prompts. The follow-up response demonstrates that the agent maintains conversation history across turns.

## Clean up resources

[!INCLUDE [clean-up-resources](../../includes/clean-up-resources.md)]

## Related content

- [Agent development lifecycle](../concepts/development-lifecycle.md)
- [What is Foundry Agent Service?](../overview.md)
- [Use tools with agents](../how-to/tools/model-context-protocol.md)
- [Quickstart: Deploy your first hosted agent](quickstart-hosted-agent.md)
