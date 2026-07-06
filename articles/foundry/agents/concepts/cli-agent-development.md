---
title: "Agent development with the Azure Developer CLI"
description: "Understand the end-to-end developer workflow for building, deploying, and operating hosted agents on Microsoft Foundry with the Azure Developer CLI."
author: aahill
ms.author: aahi
ms.manager: mcleans
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.topic: concept-article
ms.date: 06/15/2026
ms.custom: dev-focus, doc-kit-assisted
ai-usage: ai-assisted
---

# Agent development with the Azure Developer CLI

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

The Azure Developer CLI (`azd`) and its `azd ai agent` extension give you a single command-line workflow to go from idea to a production-ready hosted agent on Microsoft Foundry. This article explains the developer journey, the files that define an agent, and the core concepts you encounter along the way.

This article is for developers who prefer a terminal-first, scriptable workflow over the Foundry portal or language SDKs.

## The developer journey

The `azd ai` workflow follows the same lifecycle whether you build a small prototype or a production agent. You scaffold a project once, then mix and match commands as your project grows.

| Stage | What you do | Where to learn more |
| ----- | ----------- | ------------------- |
| Install | Install `azd` and the Foundry extensions. | [Set up your developer environment](../../how-to/develop/install-cli-sdk.md) |
| Scaffold | Initialize a project from a template or your existing code. | [Quickstart: Deploy a hosted agent](../quickstarts/quickstart-hosted-agent.md) |
| Define | Configure the model, instructions, and tools in `agent.yaml`. | [Hosted agent runtime contract](hosted-agent-contract.md) |
| Develop | Write agent logic, add tools, and test locally. | [Tools overview](tool-catalog.md) |
| Deploy | Provision infrastructure and deploy to Foundry. | [Deploy a hosted agent](../how-to/deploy-hosted-agent.md) |
| Operate | Monitor logs, manage versions, and automate runs. | [Manage hosted agents](../how-to/manage-hosted-agent.md) |
| Evaluate | Measure agent quality and improve the prompt. | [Run agent evaluations with the azd CLI](../../observability/how-to/azure-developer-cli-evaluation.md) |

## Agent types

The `azd ai agent` extension focuses on hosted agents.

| Type | Description | When to use |
| ---- | ----------- | ----------- |
| Hosted agent | A containerized application you build in code, package as a Docker image, and deploy to Foundry. | You need custom logic, framework integration, or full control over behavior. |
| Prompt agent | An agent defined entirely through instructions and tool configurations, with no custom code. | You want a quick, config-driven agent without writing application code. |

Hosted agents give you full control over the runtime, framework, and tool integrations, while Foundry handles infrastructure, scaling, and session management.

## Configuration files

Three files define how an agent is built and deployed.

| File | Purpose | Who maintains it |
| ---- | ------- | ---------------- |
| `agent.yaml` | Defines the agent's identity: model, instructions, tools, protocols, and environment variables. | You edit it directly. |
| `agent.manifest.yaml` | A parameterized template of `agent.yaml` that template authors use. It contains `{{ parameter }}` placeholders that resolve during initialization. | Template authors create it. `azd ai agent init` reads it. |
| `azure.yaml` | Defines how Azure resources are provisioned and deployed: services, infrastructure, and container settings. | Initialization generates it. You customize it as needed. |

The key distinction is that `agent.yaml` describes *what* your agent is, while `azure.yaml` describes *how* it gets deployed.

Resources that live on the Foundry project itself, such as connections, toolboxes, skills, and routines, are managed through direct `azd ai` commands rather than declared in `agent.yaml`.

### Variable substitution

You see two variable syntaxes in agent project files:

* `${VAR_NAME}` is an `azd` environment variable placeholder. It resolves from `.azure/<env>/.env` at deploy time, so the same `agent.yaml` works across environments such as dev, staging, and production.
* `{{ parameter }}` is a manifest template parameter. It resolves during `azd ai agent init` when a template is scaffolded into a concrete project.

## Where the CLI runs

The `azd ai` commands work both inside and outside an `azd` project directory:

* Inside an `azd` project, commands resolve the Foundry project endpoint from the active `azd` environment.
* Outside an `azd` project, set the active context once with `azd ai project set <endpoint>`, or pass `--project-endpoint` on an individual resource command (`connection`, `toolbox`, `skill`, or `routine`). As a fallback, `azd ai` reads the `FOUNDRY_PROJECT_ENDPOINT` environment variable.
* An in-project environment always takes precedence over the global context, so changing directories into a project retargets the CLI at that project's endpoint.

## Protocols

A protocol defines the HTTP contract between Foundry and your agent container. Your agent listens on port 8088 and serves a health probe, regardless of protocol.

| Protocol | API style | When to use |
| -------- | --------- | ----------- |
| `responses` | OpenAI Responses API (`POST /responses`) | The standard choice, compatible with the OpenAI API ecosystem. |
| `invocations` | Custom JSON contract (`POST /invocations`) | When you need full control over request and response payloads. |

For the full specification, see [Hosted agent runtime contract](hosted-agent-contract.md).

## Sessions and conversations

| Concept | Description |
| ------- | ----------- |
| Session | An isolated execution environment for a single agent interaction. Each session runs in its own sandbox with dedicated resources. |
| Conversation | A sequence of messages within a session. Foundry manages conversation history and can hydrate it across requests. |

Sessions are identified by a `session_id`. When you run `azd ai agent invoke`, Foundry reuses the session from your last invocation by default. Use `--new-session` to start fresh, or `--session-id <id>` to target a specific session.

## Resources on a Foundry project

A Foundry project hosts more than agents. It also holds shared resources that agents reference at runtime. The CLI manages each one through a dedicated command group.

| Resource | What it is | Managed with |
| -------- | ---------- | ------------ |
| Connection | Links a Foundry project to an external resource, such as an MCP server, Azure AI Search, or Grounding with Bing. | `azd ai connection` commands |
| Toolbox | A named collection of tools that agents use at runtime. | `azd ai toolbox` commands |
| Skill | A reusable behavioral guideline shared across agents on the project. | `azd ai skill` commands |
| Routine | A trigger plus an action that invokes an agent. | `azd ai routine` commands |

These resources are shared across developers and agents on the same project. Each command group exposes the standard `create`, `update`, `delete`, `show`, and `list` verbs.

## Evaluate and improve an agent

After an agent runs, two related workflows help you measure and improve its quality:

* Evaluation runs your agent against a dataset, scores the responses with one or more evaluators, and reports an aggregate quality signal. You manage it with `azd ai agent eval`.
* Optimization iteratively rewrites your agent's prompt to lift an evaluation signal. It uses an evaluation as its objective function and produces a candidate prompt that you review and accept. You manage it with `azd ai agent optimize`.

For details, see [Run agent evaluations with the azd CLI](../../observability/how-to/azure-developer-cli-evaluation.md) and [Optimize agent prompts](../../observability/how-to/prompt-optimizer.md).

## Deployment lifecycle

The full developer loop condenses into a short sequence of commands. Scaffold once, then use the direct commands as your project grows.

```bash
# Scaffold a project from a template or your existing code
azd ai agent init

# Run locally and invoke
azd ai agent run
azd ai agent invoke --local "Hello, world!"

# Provision infrastructure and deploy the agent
azd up

# Extend the project with shared resources at any time
azd ai connection create my-search --kind cognitive-search --target https://... --auth-type api-key --key "..."
azd ai routine create daily-digest --trigger recurring --cron "0 7 * * *" --agent-name my-agent

# Evaluate quality
azd ai agent eval generate
azd ai agent eval run

# Tear down all Azure resources
azd down
```

## Related content

* [Quickstart: Deploy your first hosted agent](../quickstarts/quickstart-hosted-agent.md)
* [What are hosted agents?](hosted-agents.md)
* [Hosted agent runtime contract](hosted-agent-contract.md)
* [Agent development lifecycle](development-lifecycle.md)
