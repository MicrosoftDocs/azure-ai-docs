---
title: "Set the Foundry project context for azd commands"
description: "Run azd ai commands inside or outside an azd project. Set, inspect, and clear the active Microsoft Foundry project endpoint for standalone and scripted use."
author: aahill
ms.author: aahi
ms.manager: mcleans
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.topic: how-to
ms.date: 06/15/2026
ms.custom: dev-focus, doc-kit-assisted
ai-usage: ai-assisted
---

# Set the Foundry project context for azd commands

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

The `azd ai` commands run in two contexts: inside an `azd` project (the typical team workflow) and standalone (ad hoc work, one-off scripts, or invocations from automation that has no `azure.yaml` to anchor on). Both modes target the same Microsoft Foundry resources. They differ only in how the CLI determines which Foundry project to talk to. In this article, you learn the resolution order and how to set the standalone context.

## Prerequisites

* The [Azure Developer CLI Foundry extensions](install-cli-foundry-extensions.md) installed.
* An authenticated Azure session (`azd auth login`).
* An existing Foundry project endpoint for standalone use.

## When to use each context

| Context | What it looks like | Use when |
| ------- | ------------------ | -------- |
| In an `azd` project | You run `azd ai ...` from a directory that contains `azure.yaml` and an active `azd` environment. | You build or operate an agent as part of a tracked project and want the environment to govern which Foundry project you target. |
| Standalone | You run `azd ai ...` from any other directory. | You do ad hoc work against an existing Foundry project, or you script one-off operations from automation that doesn't own an `azd` project. |

The resource commands (`azd ai connection`, `azd ai toolbox`, `azd ai skill`, and `azd ai routine`) operate on a single Foundry project, so they need a project endpoint resolved from one of these contexts before they can run.

The `azd ai agent` commands (such as `run`, `invoke`, and `optimize`) aren't standalone. They require an `azd` project for `azure.yaml` and environment resolution. Use `--agent-endpoint` on `azd ai agent invoke` to call a deployed agent without an `azd` project on disk.

## How endpoint resolution works

For every command that targets a Foundry project, the CLI resolves the endpoint in this order. The first source that returns a value wins, and later sources aren't consulted:

1. The `-p` or `--project-endpoint` flag on the command. Always wins, regardless of context.
1. The active `azd` environment, if you're inside an `azd` project directory.
1. Global config, under `extensions.ai-agents.context.endpoint` in `~/.azd/config.json`. This is what `azd ai project set` writes.
1. The `FOUNDRY_PROJECT_ENDPOINT` environment variable in the current shell.
1. Error. The CLI exits with a structured suggestion to run `azd ai project set` or pass `--project-endpoint`.

The endpoint is the only thing the CLI needs. It resolves the Azure Resource Manager resource ID (subscription, resource group, account, and project) from the endpoint at invocation time, so commands work the same whether they got the endpoint from your environment or your global config.

## Set the standalone context

The `azd ai project set` command writes the active Foundry project endpoint to your global `azd` config, so subsequent commands run from anywhere can omit `--project-endpoint`. The command takes the endpoint as a positional argument:

```bash
azd ai project set https://my-project.services.ai.azure.com/api/projects/my-project
```

The command is fully non-interactive when you pass the endpoint. Add `--no-prompt` in scripts and CI so a missing or unresolved value fails fast instead of blocking:

```bash
azd ai project set https://my-project.services.ai.azure.com/api/projects/my-project --no-prompt
```

> [!NOTE]
> Only the endpoint is canonical. Resource commands re-derive the subscription, resource group, account, and project from the endpoint at call time.

## Clear the standalone context

```bash
azd ai project unset
```

This command removes the entire `context` block from `~/.azd/config.json`. It doesn't touch any `azd` environment values.

## Inspect the active context

The `azd ai project show` command walks the full resolution chain and reports which source provided the active endpoint. Use it to confirm what your next command targets before you run it:

```bash
azd ai project show
```

Sample output when the endpoint comes from global config:

```output
Project endpoint:  https://my-project.services.ai.azure.com/api/projects/my-project
Source:            global config (~/.azd/config.json)
Tenant:            contoso.onmicrosoft.com
Subscription:      Contoso Dev (00000000-0000-0000-0000-000000000000)
Foundry project:   my-project
```

Inside an `azd` project, the `Source` line reads `azd env <env-name>` instead, and the displayed values come from the environment's `.env` file rather than from global config.

## Storage location

The standalone context lives under the `extensions.ai-agents` namespace in `~/.azd/config.json`:

```json
{
  "extensions": {
    "ai-agents": {
      "context": {
        "endpoint": "https://my-project.services.ai.azure.com/api/projects/my-project",
        "subscription": "00000000-0000-0000-0000-000000000000",
        "tenant": "contoso.onmicrosoft.com",
        "foundryProject": "my-project",
        "setAt": "2026-01-15T10:23:00Z"
      }
    }
  }
}
```

Only `endpoint` is canonical. The other fields exist to make `azd ai project show` readable. The CLI never reads them when resolving a target. You can edit the file by hand, but `azd ai project set` and `azd ai project unset` are the supported way to manage it.

## Precedence inside an azd project

Inside an `azd` project, the active environment's project endpoint always wins over the global context. Running `azd ai project set` from within a project still updates global config, but the CLI prints a one-line warning that the environment continues to take precedence for commands run from that directory.

This behavior is intentional. Project-level environment values are part of the team's workflow, while the global context is a per-machine preference. To override the environment for a single command from inside a project, pass `--project-endpoint`, or set `FOUNDRY_PROJECT_ENDPOINT` in the shell, instead of relying on global config.

## Related content

* [Quickstart: Deploy your first hosted agent](../quickstarts/quickstart-hosted-agent.md)
* [Install the Azure Developer CLI Foundry extensions](install-cli-foundry-extensions.md)
* [Initialize a hosted agent project with the Azure Developer CLI](init-agent-project.md)
