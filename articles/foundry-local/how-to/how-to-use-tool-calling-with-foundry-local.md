---
title: "Use tool calling with Foundry Local"
titleSuffix: Foundry Local
description: "Learn how to write applications with Foundry Local that make use of tool calling"
ms.service: azure-ai-foundry
ms.subservice: foundry-local
ms.topic: how-to
ms.author: nakersha
ms.reviewer: metang
author: natke
reviewer: metang
zone_pivot_groups: foundry-local-sdk-vnext
ms.date: 11/17/2025
---

# How to use tool calling with Foundry Local

Foundry Local can make use of tool calling, a technique where you prompt the model with definitions of available tools that together with a text prompt, allow the model to work out which tools should be called and with what input data. The application then calls those tools and adds the results to a subsequent model prompt to answer the user's query.

The tools can perform functions that the model doesn't have access to, such as getting the current weather, or reading files on the local file system, or accessing a user's address book (providing the application has permission to do so).

This guide shows you how to use this feature of Foundry Local.

## Models that support tool calling

Using the Foundry Local CLI, you can run the `foundry model list` command to see which models support tool calling.

In the `Task` column, you can see that the `tools` task indicates that tool calling is supported.

::: zone pivot="programming-language-csharp"
[!INCLUDE [C#](../includes/tool-calling/csharp.md)]
::: zone-end
::: zone pivot="programming-language-javascript"
[!INCLUDE [JavaScript](../includes/tool-calling/javascript.md)]
::: zone-end

## Related content

- [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling)
- [Microsoft.Extensions.AI](/dotnet/ai/microsoft-extensions-ai)
