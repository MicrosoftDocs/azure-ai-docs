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

- [.NET 9.0 SDK](https://dotnet.microsoft.com/download/dotnet/9.0) or later installed.
- Azure role-based access control (RBAC): Not applicable.

## Samples repository

You can find the sample in this article in the [Foundry Local SDK Samples GitHub repository](https://aka.ms/foundrylocalSDK).

## Set up project

[!INCLUDE [project-setup](../csharp-project-setup.md)]

## Understanding tool choice settings

When using tool calling with Foundry Local, the tool choice parameter controls whether and how the model invokes the tools you provide. It is sent as part of the chat completion request alongside your tool definitions.

Different models have different capabilities when it comes to tool calling, but in general you can expect the following behavior for each option:

| Option | Value | Behavior | Reliability |
|--------|-------|----------|-------------|
| **Auto** | `"auto"` | The model decides whether to call a tool or respond directly, based on the user's message and the available tool definitions. | Reliable across all tool-calling models |
| **None** | `"none"` | The model will not call any tools, even if tools are provided in the request. | Reliable across all tool-calling models |
| **Required** | `"required"` | The model must call at least one tool. It will not return a plain text response. | Best-effort — may be ignored by smaller models |
| **Specific function** | `{"type": "function", "function": {"name": "my_function"}}` | The model must call the specified function. | Best-effort — may be ignored by smaller models |


## Use native chat completions with tool calling

Copy and paste the following code into a C# file named `Program.cs`:

:::code language="csharp" source="~/foundry-local-main/samples/cs/tool-calling-foundry-local-sdk/Program.cs" id="complete_code":::

## Run the native chat completions example

#### [Windows](#tab/windows)

For x64 Windows, use the following command:

```bash
dotnet run -r:win-x64
```

For arm64 Windows, use the following command:

```bash
dotnet run -r:win-arm64
```

#### [Cross-Platform](#tab/xplatform)

For macOS, use the following command:

```bash
dotnet run -r:osx-arm64
```

For Linux, use the following command:

```bash
dotnet run -r:linux-x64
```

---

## Use OpenAI Web server for tool calling

If you prefer to use the OpenAI SDKs to call the Foundry Local web service, you can follow the example below which demonstrates how to handle tool calling in that scenario.

> [!TIP]
> Use `options.ToolChoice = ChatToolChoice.CreateAutoChoice();` (the default) for the most reliable behavior. Write clear tool names and descriptions so the model calls the correct tool on its own.

:::code language="csharp" source="~/foundry-local-main/samples/cs/tool-calling-foundry-local-web-server/Program.cs" id="complete_code":::

## Run the OpenAI web service example

### [Windows](#tab/windows)

For x64 Windows, use the following command:

```bash
dotnet run -r:win-x64
```

For arm64 Windows, use the following command:

```bash
dotnet run -r:win-arm64
```


### [Cross-Platform](#tab/xplatform)

For macOS, use the following command:

```bash
dotnet run -r:osx-arm64
```

For Linux, use the following command:

```bash
dotnet run -r:linux-x64
```

---