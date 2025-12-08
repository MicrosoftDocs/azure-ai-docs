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

[!INCLUDE [agent-v2-switch](agent-v2-switch.md)]

# [Python](#tab/python2)

:::code language="python" source="~/foundry-samples-main/samples/python/quickstart/quickstart-create-agent.py":::

# [C#](#tab/csharp2)

:::code language="csharp" source="~/foundry-samples-main/samples/csharp/quickstart/quickstart-create-agent.cs":::

<!-- # [TypeScript](#tab/typescript)

Not yet available

# [Java](#tab/java)

Not yet available -->

# [REST API](#tab/rest2)

Replace `YOUR-FOUNDRY-RESOURCE-NAME` with your values:

:::code language="console" source="~/foundry-samples-main/samples/REST/quickstart/quickstart-create-agent.sh":::

# [Microsoft Foundry portal](#tab/portal)

Now create an agent and interact with it.
1. Still in the **Build** section, select **Agents** in the left pane.
1. Select **Create agent** and give it a name.

---
