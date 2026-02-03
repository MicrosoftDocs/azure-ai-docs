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


Interacting with a model is the basic building block of AI applications.  Send an input and receive a response from the model:



# [Python](#tab/python)

:::code language="python" source="~/foundry-samples-main/samples/python/quickstart/quickstart-responses.py":::

 # [C#](#tab/csharp)

:::code language="csharp" source="~/foundry-samples-main/samples/csharp/quickstart/quickstart-responses.cs":::

# [TypeScript](#tab/typescript)

:::code language="typescript" source="~/foundry-samples-main/samples/typescript/quickstart/src/quickstart-responses.ts":::

# [Java](#tab/java)

:::code language="java" source="~/foundry-samples-main/samples/java/quickstart/src/main/java/com/microsoft/foundry/samples/CreateResponses.java":::

# [REST API](#tab/rest)

Replace `YOUR-FOUNDRY-RESOURCE-NAME` with your values:

:::code language="console" source="~/foundry-samples-main/samples/REST/quickstart/quickstart-responses.sh":::

# [Foundry portal](#tab/portal)

1. After the model deploys, you're automatically moved from **Home** to the **Build** section. Your new model is selected and ready for you to try out.

1. Start chatting with your model, for example, "Write me a poem about flowers."

---

[!INCLUDE [agent-v2-switch](agent-v2-switch.md)]