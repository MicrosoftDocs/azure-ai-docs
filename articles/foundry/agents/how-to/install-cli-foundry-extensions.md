---
title: "Install the Azure Developer CLI Foundry extensions"
description: "Install and verify the azd ai extensions for building, deploying, evaluating, and operating AI agents on Microsoft Foundry from your terminal."
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

# Install the Azure Developer CLI Foundry extensions

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

The Azure Developer CLI (`azd`) `ai` extensions let you build, deploy, evaluate, and operate AI agents on Microsoft Foundry from your terminal. In this article, you install the extensions, verify the installation, and authenticate to Azure.

## Prerequisites

* An Azure subscription. [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account).
* Azure Developer CLI (`azd`) version 1.25.2 or later. [Install azd](/azure/developer/azure-developer-cli/install-azd).
* Python 3.10 or later, or .NET 8 or later, depending on the agent framework you plan to use.

### Azure permissions

You need the following roles on your Azure subscription.

| Role | Purpose |
| ---- | ------- |
| Contributor | Provision and manage Azure resources. |
| Foundry Owner | Required only if you create new Foundry projects. |

[!INCLUDE [role-rename-note](../../includes/role-rename-note.md)]

## Understand how the extensions are packaged

The `azd ai` namespace is composed of multiple independent `azd` extensions. Each one contributes a top-level command group under `azd ai`.

| Extension ID | Command group | What it does |
| ------------ | ------------- | ------------ |
| `microsoft.foundry` | meta-package | Bundles all of the Foundry extensions for a single install. |
| `azure.ai.agents` | `azd ai agent` | Ship agents with Foundry from your terminal. |
| `azure.ai.connections` | `azd ai connection` | Manage Foundry project connections. |
| `azure.ai.inspector` | `azd ai inspector` | Browser-based inspector UI for locally running agents. |
| `azure.ai.projects` | `azd ai project` | Manage Foundry project context (`set`, `unset`, `show`). |
| `azure.ai.routines` | `azd ai routine` | Manage Foundry routines (timers, schedules, event triggers). |
| `azure.ai.skills` | `azd ai skill` | Manage Foundry skills (reusable agent behavioral guidelines). |
| `azure.ai.toolboxes` | `azd ai toolbox` | Manage Foundry toolboxes (versioned tool collections). |

The `microsoft.foundry` package is a thin meta-package that doesn't contribute its own commands. Installing it pulls in every individual extension, which is the recommended starting point. Installing `azure.ai.agents` on its own also pulls in `azure.ai.inspector` automatically, because the agent extension depends on it.

## Install the full bundle

Install every Foundry extension in one step through the meta-package:

```bash
azd ext install microsoft.foundry
```

To update later:

```bash
azd ext upgrade microsoft.foundry
```

## Install or upgrade an individual extension

You can also manage each extension on its own:

```bash
# Just the agent surface
azd ext install azure.ai.agents

# Just the routine surface
azd ext install azure.ai.routines

# Upgrade one extension without touching the others
azd ext upgrade azure.ai.connections
```

The individual extensions are independently versioned, so you can pin or upgrade one at a time.

## Verify the installation

List installed extensions:

```bash
azd ext list
```

You should see `microsoft.foundry` plus each individual extension. Each extension also exposes a `version` subcommand:

```bash
azd ai agent version
azd ai connection version
azd ai inspector version
azd ai project version
azd ai routine version
azd ai skill version
azd ai toolbox version
```

## Authenticate

Sign in to Azure so the CLI can provision and manage resources on your behalf:

```bash
azd auth login
```

This command opens a browser window for interactive authentication. After you sign in, the CLI caches your credentials locally for subsequent commands.

## Related content

* [Quickstart: Deploy your first hosted agent](../quickstarts/quickstart-hosted-agent.md)
* [Initialize a hosted agent project with the Azure Developer CLI](init-agent-project.md)
* [Set the Foundry project context for azd commands](cli-project-context.md)
