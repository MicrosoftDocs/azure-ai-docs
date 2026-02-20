---
title: Include file
description: Include file
author: sdgilley
ms.reviewer: sgilley
ms.author: sgilley
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 11/05/2025
ms.custom: include
---

Create an agent using your deployed model.

An agent defines core behavior. Once created, it ensures consistent responses in user interactions without repeating instructions each time. You can update or delete agents anytime. 


# [Python](#tab/python)

:::code language="python" source="~/foundry-samples-main/samples/python/quickstart/quickstart-create-agent.py":::

# [C#](#tab/csharp)

:::code language="csharp" source="~/foundry-samples-main/samples/csharp/quickstart/quickstart-create-agent.cs":::

# [TypeScript](#tab/typescript)

:::code language="typescript" source="~/foundry-samples-main/samples/typescript/quickstart/src/quickstart-create-agent.ts":::


# [Java](#tab/java)

:::code language="java" source="~/foundry-samples-main/samples/java/quickstart/src/main/java/com/microsoft/foundry/samples/CreateAgent.java":::

# [REST API](#tab/rest)

Replace `YOUR-FOUNDRY-RESOURCE-NAME` with your values:

:::code language="console" source="~/foundry-samples-main/samples/REST/quickstart/quickstart-create-agent.sh":::

# [Foundry portal](#tab/portal)

Now create an agent and interact with it.
1. Still in the **Build** section, select **Agents** in the left pane.
1. Select **Create agent** and give it a name.

---

The output confirms the agent was created. For SDK tabs, you see the agent name and ID printed to the console.

[!INCLUDE [agent-v2-switch](agent-v2-switch.md)]