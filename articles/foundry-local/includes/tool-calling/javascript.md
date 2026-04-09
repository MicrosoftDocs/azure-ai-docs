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

The complete sample code for this article is available in the [Foundry Local GitHub repository](https://github.com/microsoft/Foundry-Local). To clone the repository and navigate to the sample use:

```bash
git clone https://github.com/microsoft/Foundry-Local.git
cd Foundry-Local/samples/js/tool-calling-foundry-local
```

## Install packages

[!INCLUDE [project-setup](./../javascript-project-setup.md)]

## Understanding tool choice settings

The tool choice parameter controls whether and how the model invokes the tools you provide. Tool choice is sent as part of the chat completion request alongside your tool definitions.

Different models have different capabilities when it comes to tool calling, but in general you can expect the following behavior for each option:

| Option | Value | Behavior | Reliability |
|--------|-------|----------|-------------|
| **Auto** | `"auto"` | The model decides whether to call a tool or respond directly, based on the user's message and the available tool definitions. | Reliable across all tool-calling models |
| **None** | `"none"` | The model doesn't invoke any tools, even if tools are provided in the request. | Reliable across all tool-calling models |
| **Required** | `"required"` | The model must call at least one tool. | Best-effort |
| **Specific function** | `{"type": "function", "function": {"name": "my_function"}}` | The model must call the specified function. | Best-effort |

## Use chat completions with tool calling

Copy and paste the following code into a JavaScript file named `app.js`:

:::code language="javascript" source="~/foundry-local-main/samples/js/tool-calling-foundry-local/src/app.js" id="complete_code":::

To run the application, execute the following command in your terminal:

```bash
node app.js
```
