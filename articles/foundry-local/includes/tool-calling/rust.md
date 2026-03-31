---
title: Include file
description: Include file
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 07/17/2025
ms.author: samkemp
author: samuel100
ai-usage: ai-assisted
---

## Prerequisites

- [Rust and Cargo](https://www.rust-lang.org/tools/install) installed (Rust 1.70.0 or later).


## Samples repository

[!INCLUDE [samples-repo](../samples-repo.md)]

Navigate to the sample for this article:

```bash
cd rust/tool-calling-foundry-local
```

## Set up project

[!INCLUDE [project-setup](../rust-project-setup.md)]

Add extra dependencies for HTTP and JSON:

```bash
cargo add anyhow reqwest --features reqwest/json
cargo add serde serde_json --features serde/derive
```

## Understanding tool choice settings

The tool choice parameter controls whether and how the model invokes the tools you provide. Tool choice is sent as part of the chat completion request alongside your tool definitions.

Different models have different capabilities when it comes to tool calling, but in general you can expect the following behavior for each option:

| Option | Value | Behavior | Reliability |
|--------|-------|----------|-------------|
| **Auto** | `"auto"` | The model decides whether to call a tool or respond directly, based on the user's message and the available tool definitions. | Reliable across all tool-calling models |
| **None** | `"none"` | The model doesn't call any tools, even if tools are provided in the request. | Reliable across all tool-calling models |
| **Required** | `"required"` | The model must call at least one tool. | Best effort (tool call could be ignored by smaller models) |
| **Specific function** | `{"type": "function", "function": {"name": "my_function"}}` | The model must call the specified function. | Best-effort (tool call could be ignored by smaller models) |

## Use chat completions with tool calling

Replace the contents of `src/main.rs` with the following code:

:::code language="rust" source="~/foundry-local-main/samples/rust/tool-calling-foundry-local/src/main.rs" id="complete_code":::

## Run the application

To run the application, execute the following command in your terminal:

```bash
cargo run
```
