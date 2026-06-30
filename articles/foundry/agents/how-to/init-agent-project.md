---
title: "Initialize a hosted agent project with the Azure Developer CLI"
description: "Scaffold a hosted agent project with azd ai agent init: start from a template, bring your own code, or connect to an existing Microsoft Foundry project."
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

# Initialize a hosted agent project with the Azure Developer CLI

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

Use `azd ai agent init` to scaffold a hosted agent project with the files you need to build, test, and deploy an AI agent to Microsoft Foundry. In this article, you choose a starting point and initialize the project from a template, from your own code, or against an existing Foundry project.

## Prerequisites

* The [Azure Developer CLI Foundry extensions](install-cli-foundry-extensions.md) installed.
* An authenticated Azure session (`azd auth login`).
* Contributor access on your Azure subscription.

## Choose a starting point

There are three ways to begin a project. Pick the path that matches your situation.

| Consideration | Start from a template | Bring your own code | Connect an existing project |
| --- | --- | --- | --- |
| Best for | New agents, learning the tooling. | Existing agent code you want to host on Foundry. | Agents already running in a Foundry project. |
| Command | `azd ai agent init` in an empty directory. | `azd ai agent init` in a directory with existing code. | `azd ai agent init`, then select an existing project. |
| What you get | A full scaffolded project: agent code, `agent.yaml`, `azure.yaml`, Bicep infrastructure, and a Dockerfile. | A generated `agent.yaml`, `azure.yaml`, Bicep infrastructure, and a Dockerfile wrapping your code. | `azure.yaml` and Bicep infrastructure wired to your existing Foundry project. |
| Code changes | None. Ready to run. | Might need a protocol adapter. | None. |

## Initialize from a template

Run the interactive wizard in an empty directory and select **Start new from a template**:

```bash
azd ai agent init
```

The wizard walks you through the following choices.

| Prompt | Description |
| ------ | ----------- |
| Agent template | Choose from templates organized by framework and language (Python or .NET). |
| Azure subscription | The subscription used to find or create a Foundry project. |
| Foundry project | Select an existing project or create a new one. If you create one, you also choose a region. |
| Model deployment | Select an existing model deployment, or one is created from template defaults. |

The agent name is derived from the template. The CLI creates an `azd` environment named `<directory>-dev` and configures it with details from your selected Foundry project. Each template includes agent source code, a `Dockerfile`, and an `agent.manifest.yaml` that describes the agent's configuration and resource dependencies.

### Initialize from a manifest URL

If you have a specific agent sample, point directly to its manifest:

```bash
azd ai agent init -m https://github.com/org/repo/blob/main/agent.manifest.yaml
```

This command downloads the agent code referenced by the manifest and scaffolds the project around it.

### Specify a model

Choose a model at init time:

```bash
azd ai agent init --model gpt-4.1
```

Or use an existing model deployment in your Foundry project:

```bash
azd ai agent init --model-deployment my-deployment
```

### Browse templates noninteractively

To inspect the catalog before you scaffold, or to drive `azd ai agent init` from a script, list the catalog:

```bash
# Everything in the catalog
azd ai agent sample list

# Just the featured Python agent manifests
azd ai agent sample list --featured-only --language python --type agent

# Full azd templates only, as JSON for scripting
azd ai agent sample list --type azd --output json
```

Each entry includes a ready-to-run `initCommand` that you copy and run in the directory you want to scaffold into.

> [!TIP]
> When you reuse a manifest under a different Foundry agent identity, pass `--agent-name <new-name>` on `azd ai agent init` so the new project doesn't collide with the manifest's default name.

## Initialize from existing code

If you have existing Python or .NET agent code, run `azd ai agent init` inside the directory that already contains your code:

```bash
cd my-agent/
azd ai agent init
```

The CLI detects the existing files and generates the deployment scaffolding (`agent.yaml`, `azure.yaml`, Bicep templates, and a Dockerfile) around them, without overwriting your code.

Your agent code must meet the [hosted agent runtime contract](../concepts/hosted-agent-contract.md):

* Listen on port 8088.
* Serve a health probe at `GET /readiness`.
* Handle one of the supported protocols (`responses` or `invocations`).

If your code doesn't already speak one of these protocols, [add a protocol adapter](add-protocol-adapter.md), a lightweight SDK wrapper that translates between the Foundry protocol and your agent's logic.

To add an agent to an existing `azd` project, `init` detects the project and adds a new service entry to your existing `azure.yaml`. Use `--src` to specify a subdirectory:

```bash
azd ai agent init --src src/my-agent
```

## Connect to an existing Foundry project

To manage an existing Foundry project through `azd`, run the wizard and select the option to connect to an existing project. You can also skip the interactive selection by providing the project's Azure resource ID directly:

```bash
azd ai agent init --project-id /subscriptions/{sub}/resourceGroups/{rg}/providers/Microsoft.CognitiveServices/accounts/{account}/projects/{project}
```

To find the project ID, open the [Foundry portal](https://ai.azure.com), go to **Operate** > **Admin**, select your Foundry project, and copy the **Resource ID** value.

> [!WARNING]
> When you initialize against an existing project with `--project-id`, the tooling skips the automatic role assignments that it performs when it creates a new project. Make sure the required roles are already assigned. For the full matrix, see [Hosted agent permissions reference](../concepts/hosted-agent-permissions.md).

## Review what gets created

After `init` completes, your project directory contains the following structure:

```
.
|-- azure.yaml                  # azd project configuration
|-- infra/                      # Bicep infrastructure-as-code
|   |-- main.bicep              # Main deployment template
|   |-- main.parameters.json    # Parameter bindings to azd env vars
|   \-- core/                   # Reusable Bicep modules
|-- src/
|   \-- <agent-name>/
|       |-- agent.yaml          # Agent definition (generated from manifest)
|       |-- Dockerfile          # Container build definition
|       \-- ...                 # Agent source code
\-- .azure/                     # Environment configuration
```

Templates and samples publish an `agent.manifest.yaml`, a parameterized template. During init, parameter values are resolved and an `agent.yaml` definition is generated in your project. You work with `agent.yaml` going forward.

## Related content

* [Quickstart: Deploy your first hosted agent](../quickstarts/quickstart-hosted-agent.md)
* [agent.yaml schema reference](../concepts/agent-yaml-reference.md)
* [azure.yaml reference for hosted agents](../concepts/azure-yaml-reference.md)
* [Hosted agent infrastructure with the Azure Developer CLI](../concepts/cli-infrastructure.md)
