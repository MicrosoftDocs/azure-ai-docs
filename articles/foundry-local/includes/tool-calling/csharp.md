---
title: Include file
description: Include file
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 01/06/2026
ms.author: samkemp
author: samuel100
ai-usage: ai-assisted
---

## Prerequisites

- [.NET 8.0 SDK](https://dotnet.microsoft.com/download/dotnet/8.0) or later installed.

## Samples repository

The complete sample code for this article is available in the [Foundry Local GitHub repository](https://github.com/microsoft/Foundry-Local). To clone the repository and navigate to the sample use:

```bash
git clone https://github.com/microsoft/Foundry-Local.git
cd Foundry-Local/samples/cs/tool-calling-foundry-local-sdk
```

## Install packages

[!INCLUDE [project-setup](../csharp-project-setup.md)]

## Understanding tool choice settings

The tool choice parameter controls whether and how the model invokes the tools you provide. Tool choice is sent as part of the chat completion request alongside your tool definitions.

Different models have different capabilities when it comes to tool calling, but in general you can expect the following behavior for each option:

| Option | Value | Behavior | Reliability |
|--------|-------|----------|-------------|
| **Auto** | `"auto"` | The model decides whether to call a tool or respond directly, based on the user's message and the available tool definitions. | Reliable across all tool-calling models |
| **None** | `"none"` | The model won't call any tools, even if tools are provided in the request. | Reliable across all tool-calling models |
| **Required** | `"required"` | The model must call at least one tool. | Best-effort |
| **Specific function** | `{"type": "function", "function": {"name": "my_function"}}` | The model must call the specified function. | Best-effort |


## Use native chat completions with tool calling

Copy and paste the following code into a C# file named `Program.cs`:

:::code language="csharp" source="~/foundry-local-main/samples/cs/tool-calling-foundry-local-sdk/Program.cs" id="complete_code":::

## Run the native chat completions example

```bash
dotnet run
```

## Use OpenAI Web server for tool calling

If you prefer to use the OpenAI SDKs to call the Foundry Local web service, use the following example that demonstrates how to handle tool calling in that scenario.

> [!TIP]
> Use `options.ToolChoice = ChatToolChoice.CreateAutoChoice();` (the default) for the most reliable behavior. Write clear tool names and descriptions so the model calls the correct tool on its own.

:::code language="csharp" source="~/foundry-local-main/samples/cs/tool-calling-foundry-local-web-server/Program.cs" id="complete_code":::

## Run the OpenAI web service example

```bash
dotnet run
```
