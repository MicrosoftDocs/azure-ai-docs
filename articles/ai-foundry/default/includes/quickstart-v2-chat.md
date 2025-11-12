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

[!INCLUDE [agent-v2-switch](agent-v2-switch.md)]

# [Python](#tab/python2)

:::code language="python" source="~/foundry-samples-nov25-updates/samples-v2/microsoft/python/quickstart/quickstart-responses.py":::

 # [C#](#tab/csharp2)

:::code language="python" source="~/foundry-samples-nov25-updates/samples-v2/microsoft/csharp/quickstart/quickstart-responses.cs":::

<!-- # [TypeScript](#tab/typescript)

Not yet available

# [Java](#tab/java)

Not yet available -->

# [REST API](#tab/rest2)

Replace `YOUR-FOUNDRY-RESOURCE-NAME` with your values:

:::code language="console" source="~/foundry-samples-nov25-updates/samples-v2/microsoft/REST/quickstart/quickstart-responses.sh":::

# [Microsoft Foundry portal](#tab/portal)

1. After the model deploys, you're automatically moved from **Home** to the **Build** section. Your new model is selected and ready for you to try out.

1. Start chatting with your model, for example, "Write me a poem about flowers."

---
