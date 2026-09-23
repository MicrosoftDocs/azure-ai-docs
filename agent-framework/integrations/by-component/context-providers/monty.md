---
title: Monty
description: Add cross-platform CodeAct execution to Agent Framework Python agents with Monty.
author: eavanvalkenburg
ms.topic: article
ms.author: edvan
ms.date: 09/19/2026
ms.service: agent-framework
ai-usage: ai-assisted
---

# Monty

Monty is a Rust-based interpreter for a restricted Python subset. `MontyCodeActProvider` gives an Agent Framework agent one `execute_code` tool and lets generated code call provider-owned tools as typed async functions or through `call_tool(...)`.

This integration uses the CodeAct pattern with a restricted interpreter rather than a hardware-isolated sandbox.

Use Monty when you need a cross-platform CodeAct runtime without Hyperlight's hypervisor or WASM guest dependency.

> [!NOTE]
> `agent-framework-monty` is a beta package. Monty restricts operating-system, subprocess, and direct network access, but it isn't a hardware-isolated virtual machine.

## Install the packages

```bash
pip install agent-framework-monty agent-framework-foundry --pre
```

## Add `MontyCodeActProvider`

Register host tools on the provider rather than directly on the agent. The model sees `execute_code` and calls those tools from generated code.

:::code language="python" source="~/../agent-framework-code/python/samples/02-agents/context_providers/code_act/monty_code_act.py" range="137-171":::

### Control host tool parameter descriptions

`MontyCodeActProvider` and `MontyExecuteCodeTool` accept `tool_description_format`. The default, `"compact"`, includes scalar parameter types, required or optional status, descriptions, enum values, and defaults in the `execute_code` description and CodeAct instructions. Use `"json"` for complete JSON Schema, or select a format by exact, case-sensitive tool name:

```python
codeact = MontyCodeActProvider(
    tools=[compute, fetch_data],
    tool_description_format={
        "compute": "json",
        "fetch_data": "compact",
    },
)
```

Tools omitted from a mapping use compact format. Compact rendering automatically falls back to complete JSON Schema when it can't represent a schema without losing constraints, such as nested objects, arrays, references, or unions. Parameter schemas are visible to the model, so don't include credentials or other secrets in descriptions, enum values, defaults, or custom schema fields.

## Configure capabilities

`MontyCodeActProvider` and `MontyExecuteCodeTool` support:

- host tools and runtime tool management
- `never_require` or `always_require` approval for `execute_code`
- a workspace root and explicit file mounts
- Monty resource limits
- files returned from read-write mounts as Agent Framework content

Monty doesn't provide an outbound URL allow list. Provide network access through a narrow host tool that validates destinations and inputs.

## Choose Monty or Hyperlight

| Runtime | Choose it when |
|---|---|
| Monty | Cross-platform execution and a restricted interpreter are sufficient. |
| [Hyperlight](hyperlight.md) | You need a hardened sandbox, filesystem controls, or outbound-domain allow lists. |

## Next steps

> [!div class="nextstepaction"]
> [Review the CodeAct pattern](../../../agents/code-act.md)
