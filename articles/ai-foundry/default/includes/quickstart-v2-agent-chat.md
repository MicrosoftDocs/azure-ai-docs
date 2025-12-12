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

Use the previously created agent named "MyAgent" to interact by asking a question and a related follow-up. The conversation maintains history across these interactions. 

[!INCLUDE [agent-v2-switch](agent-v2-switch.md)]

# [Python](#tab/python2)

:::code language="python" source="~/foundry-samples-main/samples/python/quickstart/quickstart-chat-with-agent.py":::

# [C#](#tab/csharp2)

:::code language="csharp" source="~/foundry-samples-main/samples/csharp/quickstart/quickstart-chat-with-agent.cs":::

<!-- # [TypeScript](#tab/typescript) -->

<!-- :::code language="typescript" source="~/foundry-samples-main/samples/typescript/quickstart/src/quickstart.ts"::: -->

<!-- # [Java](#tab/java) -->

<!-- :::code language="java" source="~/foundry-samples-main/samples/java/quickstart/src/main/java/com/azure/ai/foundry/samples/AgentSample.java" ::: -->


# [REST API](#tab/rest2)

Replace `YOUR-FOUNDRY-RESOURCE-NAME` with your values:

:::code language="console" source="~/foundry-samples-main/samples/REST/quickstart/quickstart-chat-with-agent.sh":::

# [Microsoft Foundry portal](#tab/portal)

Interact with your agent.
1. Add instructions, such as, "You are a helpful writing assistant."
1. Start chatting with your agent, for example, "Write a poem about the sun." 
1. Follow up with "How about a haiku?"

---
