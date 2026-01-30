---
title: Include file
description: Include file
author: sdgilley
ms.reviewer: sgilley
ms.author: sgilley
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 11/05/2025
ms.custom: include, update-code1
---

Use the previously created agent named "MyAgent" to interact by asking a question and a related follow-up. The conversation maintains history across these interactions. 


# [Python](#tab/python)

:::code language="python" source="~/foundry-samples-main/samples/python/quickstart/quickstart-chat-with-agent.py":::

# [C#](#tab/csharp)

:::code language="csharp" source="~/foundry-samples-main/samples/csharp/quickstart/quickstart-chat-with-agent.cs":::

# [TypeScript](#tab/typescript)

:::code language="typescript" source="~/foundry-samples-main/samples/typescript/quickstart/src/quickstart-chat-with-agent.ts":::

# [Java](#tab/java) 

:::code language="java" source="~/foundry-samples-main/samples/java/quickstart/src/main/java/com/microsoft/foundry/samples/ChatWithAgent.java" :::


# [REST API](#tab/rest)

Replace `YOUR-FOUNDRY-RESOURCE-NAME` with your values:

:::code language="console" source="~/foundry-samples-main/samples/REST/quickstart/quickstart-chat-with-agent.sh":::

# [Foundry portal](#tab/portal)

Interact with your agent.
1. Add instructions, such as, "You are a helpful writing assistant."
1. Start chatting with your agent, for example, "Write a poem about the sun." 
1. Follow up with "How about a haiku?"

---

[!INCLUDE [agent-v2-switch](agent-v2-switch.md)]