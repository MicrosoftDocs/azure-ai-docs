---
title: "Agent development with the Azure Developer CLI"
description: "Understand the end-to-end Azure Developer CLI workflow for building, deploying, and operating hosted and prompt-based voice agents on Microsoft Foundry."
author: aahill
ms.author: aahi
ms.manager: mcleans
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.topic: concept-article
ms.date: 08/27/2026
ms.custom: dev-focus, doc-kit-assisted
ai-usage: ai-assisted
---

# Agent development with the Azure Developer CLI

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

The Azure Developer CLI (`azd`) and its `azd ai agent` extension give you a single command-line workflow to go from idea to a production-ready agent on Microsoft Foundry. You can develop code-based hosted agents and declarative prompt-based voice agents. This article explains the developer journey, the files that define an agent, and the core concepts you encounter along the way.

This article is for developers who prefer a terminal-first, scriptable workflow over the Foundry portal or language SDKs.

## The developer journey

The `azd ai` workflow follows the same lifecycle whether you build a small prototype or a production agent. You scaffold a project once, then mix and match commands as your project grows.

| Stage | What you do | Where to learn more |
| ----- | ----------- | ------------------- |
| Install | Install `azd` and the Foundry extensions. | [Set up your developer environment](../../how-to/develop/install-cli-sdk.md) |
| Scaffold | Initialize a hosted agent from a template or your existing code, or create a prompt-based voice agent. | [Quickstart: Deploy a hosted agent](../quickstarts/quickstart-hosted-agent.md) or [Quickstart: Create a prompt voice agent](../quickstarts/prompt-voice-agent.md) |
| Define | Configure the agent, model deployment dependencies, protocols, tools, and environment in `azure.yaml`. | [Author azure.yaml for hosted agents](../how-to/author-azure-yaml.md) |
| Develop | Write agent logic, add tools using a toolbox, and test locally. | [Toolbox overview](toolbox-overview.md) |
| Deploy | Provision infrastructure and deploy to Foundry. | [Deploy a hosted agent](../how-to/deploy-hosted-agent.md) |
| Operate | Monitor logs, manage versions, and automate runs. | [Manage hosted agents](../how-to/manage-hosted-agent.md) |
| Evaluate | Measure agent quality and improve the prompt. | [Run agent evaluations with the azd CLI](../../observability/how-to/azure-developer-cli-evaluation.md) |

## Agent types

The `azd ai agent` extension supports code-based and declarative agent types.

| Type | Description | When to use |
| ---- | ----------- | ----------- |
| Hosted agent | A containerized application you build in code, package as a Docker image, and deploy to Foundry. | You need custom logic, framework integration, or full control over behavior. |
| Prompt agent | An agent defined entirely through instructions and tool configurations, with no custom code. | You want a quick, config-driven agent without writing application code. |
| Prompt-based voice agent | A declarative voice agent that uses a managed or self-deployed model without custom runtime code. | You want a real-time conversational voice experience without building and hosting an audio pipeline. |
| Hosted voice agent with a managed wrapper | A hosted target handles conversation logic, while a separate voice service delegates to it through `conversationEngine`. Voice Live handles the audio experience. | You need custom agent logic without implementing speech recognition and synthesis in the hosted target. |

Hosted agents give you full control over the runtime, framework, and tool integrations, while Foundry handles infrastructure, scaling, and session management.

Prompt-based voice agents don't require a custom container. If you need to run
a custom speech-to-speech or cascaded audio pipeline in your own container,
build a [voice agent with a hosted agent](../how-to/build-voice-agent.md) and
use the `invocations_ws` protocol.

To keep conversation logic in a hosted text agent while Voice Live handles audio, use the [hosted voice wrapper workflow](../how-to/deploy-hosted-voice-agent.md). The wrapper and target are separate services in the same `azure.yaml` project. This flow doesn't replace the existing custom `invocations_ws` audio-pipeline flow.

Before using the public-preview voice CLI options, check your installed extension as described in the [voice agent quickstart prerequisites](../quickstarts/prompt-voice-agent.md#prerequisites).

## Configuration files

A hosted agent project uses one `azure.yaml` file at the project root to declare both the agent and its provisioning and deployment model. The file uses a split-service model, where each named service has a `host` value such as `azure.ai.project`, `azure.ai.agent`, `azure.ai.connection`, `azure.ai.toolbox`, `azure.ai.skill`, or `azure.ai.routine`.

| File | Purpose | Who maintains it |
| ---- | ------- | ---------------- |
| `azure.yaml` | Declares the Foundry project, model deployments, hosted agent service, dependencies, protocols, tools, environment variables, container resources, and deployment settings. Agent identity, model, protocols, tools, and environment values live in the `azure.ai.agent` service. | Initialization generates it. You customize it as needed. |

The `azure.ai.agent` service defines your hosted agent inline and uses `uses:` to reference other services, such as the project, connections, toolboxes, skills, and routines. There is no standalone `agent.yaml` or `agent.manifest.yaml` file in the current hosted-agent `azd` project model.

For a prompt-based voice agent, `azure.yaml` stores the declarative agent
definition, including `kind: prompt-voice`, the model, the model type, and the
agent name. It doesn't include a hosted-agent container runtime. To customize
instructions, audio, turn detection, transcription, voice output, tools, and
greetings, see
[Configure a voice agent](../how-to/configure-voice-agent.md).

For a hosted voice wrapper, `conversationEngine.name` references the hosted target's service name. The wrapper's `uses` dependency orders deployment, and `conversationEngine.version` defaults to the version deployed by the current environment. See the [voice service reference](azure-yaml-reference.md#voice-services) for the configuration fields.

### Variable substitution

Use `${VAR_NAME}` in `azure.yaml` for values that differ by `azd` environment. The placeholder resolves from `.azure/<env>/.env` at deploy or run time, so the same `azure.yaml` works across environments such as dev, staging, and production.

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

These protocol settings apply to hosted-agent containers. Prompt-based voice
agents don't configure a hosted-agent protocol.

`azd ai agent invoke` doesn't implement voice conversations for prompt-based voice agents or hosted voice wrappers. For the CLI behavior and testing guidance, see [Voice agent limitations](../how-to/invoke-hosted-agent.md#voice-agent-limitations).

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

For the managed voice-agent path, see
[Quickstart: Create a prompt voice agent](../quickstarts/prompt-voice-agent.md).

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

* [Quickstart: Create a prompt voice agent](../quickstarts/prompt-voice-agent.md)
* [Configure a voice agent](../how-to/configure-voice-agent.md)
* [Quickstart: Deploy your first hosted agent](../quickstarts/quickstart-hosted-agent.md)
* [What are hosted agents?](hosted-agents.md)
* [Hosted agent runtime contract](hosted-agent-contract.md)
* [Agent development lifecycle](development-lifecycle.md)
