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
| What you get | A full scaffolded project: a single `azure.yaml`, agent source under `src/<agent-name>/`, and a Dockerfile for container deployment. Infrastructure is bicep-less by default and can be ejected later. | A generated `azure.yaml` service entry and, for container deployment, a Dockerfile wrapping your code. Infrastructure is bicep-less by default and can be ejected later. | An `azure.yaml` wired to your existing Foundry project. Infrastructure is bicep-less by default and can be ejected later. |
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

The agent name comes from the template. The CLI creates an `azd` environment named `<directory>-dev` and configures it with details from your selected Foundry project. Each template includes agent source code, a `Dockerfile`, and an `azure.yaml` file that acts as the unified project manifest for the `azd` project and hosted agent configuration.

### Initialize from an azure.yaml URL

If you have a specific agent sample, point `-m` to the sample's `azure.yaml`. The CLI adopts that file as the project manifest and downloads the referenced agent source.

```bash
azd ai agent init -m https://github.com/microsoft-foundry/foundry-samples/blob/main/samples/python/hosted-agents/agent-framework/responses/01-basic/azure.yaml
```

> [!NOTE]
> Agent manifests (`agent.manifest.yaml`) and standalone agent definitions (`agent.yaml`) are deprecated. As of the Foundry `azd` extensions (`azure.ai.agents` 1.0.0-beta.1), all hosted agent configuration lives in a single `azure.yaml`. See [Author azure.yaml for hosted agents](author-azure-yaml.md).

The `-m` option still accepts a legacy agent manifest URL, but current samples publish a unified `azure.yaml`.

### Specify a model

Choose a model at init time:

```bash
azd ai agent init --model gpt-4.1
```

Or use an existing model deployment in your Foundry project:

```bash
azd ai agent init --model-deployment my-deployment
```

### Choose a deploy mode

By default, `azd ai agent init` uses code deployment for Python and .NET projects. Code deployment uploads your source as a ZIP package. To scaffold a container-based project instead, pass `--deploy-mode container`:

```bash
azd ai agent init --deploy-mode container
```

To deploy a prebuilt container image, pass `--image` and `--agent-name`. This option skips template and language selection, code scaffolding, Dockerfile generation, and Azure Container Registry setup.

```bash
azd ai agent init --agent-name my-agent --image myregistry.azurecr.io/my-agent:v1
```

### Browse templates noninteractively

To inspect the catalog before you scaffold, or to drive `azd ai agent init` from a script, list the catalog:

```bash
# Everything in the catalog
azd ai agent sample list

# Just the featured Python agent samples
azd ai agent sample list --featured-only --language python --type agent

# Full azd templates only, as JSON for scripting
azd ai agent sample list --type azd --output json
```

Each entry includes a ready-to-run `initCommand` that you copy and run in the directory you want to scaffold into.

> [!TIP]
> When you reuse a sample under a different Foundry agent identity, pass `--agent-name <new-name>` on `azd ai agent init` so the name written to `azure.yaml` doesn't collide with the sample default name.

## Initialize from existing code

If you have existing Python or .NET agent code, run `azd ai agent init` inside the directory that already contains your code:

```bash
cd my-agent/
azd ai agent init
```

The CLI detects the existing files and generates an `azure.yaml` service entry around them without overwriting your code. For container deployment, it also adds a Dockerfile. Infrastructure remains bicep-less by default unless you eject infrastructure as code later.

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
|-- azure.yaml                  # Unified azd project and hosted agent configuration
|-- src/
|   \-- <agent-name>/
|       |-- Dockerfile          # Container build definition
|       \-- ...                 # Agent source code
|-- .azure/                     # Environment configuration
\-- infra/                      # Optional IaC, created only after you eject infrastructure
```

Templates and samples publish a unified `azure.yaml` at the project root. During init, `azd` adopts or generates that file. You work with `azure.yaml` going forward. Infrastructure is bicep-less by default. Eject infrastructure only when you need to manage the generated IaC files directly.

## Related content

* [Quickstart: Deploy your first hosted agent](../quickstarts/quickstart-hosted-agent.md)
* [Author azure.yaml for hosted agents](author-azure-yaml.md)
* [azure.yaml reference for hosted agents](../concepts/azure-yaml-reference.md)
* [Hosted agent infrastructure with the Azure Developer CLI](../concepts/cli-infrastructure.md)
