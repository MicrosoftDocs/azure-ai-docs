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
- [Node.js 20](https://nodejs.org/en/download/) or later installed.


## Samples repository

[!INCLUDE [samples-repo](../samples-repo.md)]

Navigate to the sample for this article:

```bash
cd js/tool-calling-foundry-local
```

## Set up project

[!INCLUDE [project-setup](./../javascript-project-setup.md)]

## Understanding tool choice settings

When using tool calling with Foundry Local, the tool choice parameter controls whether and how the model invokes the tools you provide. It is sent as part of the chat completion request alongside your tool definitions.

Different models have different capabilities when it comes to tool calling, but in general you can expect the following behavior for each option:

| Option | Value | Behavior | Reliability |
|--------|-------|----------|-------------|
| **Auto** | `"auto"` | The model decides whether to call a tool or respond directly, based on the user's message and the available tool definitions. | Reliable across all tool-calling models |
| **None** | `"none"` | The model will not call any tools, even if tools are provided in the request. | Reliable across all tool-calling models |
| **Required** | `"required"` | The model must call at least one tool. It will not return a plain text response. | Best-effort — may be ignored by smaller models |
| **Specific function** | `{"type": "function", "function": {"name": "my_function"}}` | The model must call the specified function. | Best-effort — may be ignored by smaller models |

## Use chat completions with tool calling

Copy and paste the following code into a JavaScript file named `app.js`:

:::code language="javascript" source="~/foundry-local-main/samples/js/tool-calling-foundry-local/src/app.js" id="complete_code":::

## Run the application

To run the application, execute the following command in your terminal:

```bash
node app.js
```
