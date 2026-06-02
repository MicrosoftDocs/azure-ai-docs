---
title: "Use the Microsoft Foundry Skill in coding agents"
description: "Install and use the Microsoft Foundry Skill with coding agents such as GitHub Copilot in Visual Studio Code, Copilot CLI, and Claude Code."
keywords: microsoft foundry skill, azure skills plugin, coding agents, copilot, claude code, foundry mcp
author: junjieli
ms.author: junjieli
ms.reviewer:
ms.date: 05/27/2026
ms.service: microsoft-foundry
ms.topic: how-to
ms.custom:
  - dev-focus
  - doc-kit-assisted
ai-usage: ai-assisted
# customer intent: As a developer, I want to install the Microsoft Foundry Skill so that my coding agent can help with Foundry deployment, evaluation, and troubleshooting workflows.
---

# Use the Microsoft Foundry Skill in coding agents

The [Microsoft Foundry Skill](https://www.skills.sh/microsoft/azure-skills/microsoft-foundry) gives coding agents reusable guidance for Foundry
agent workflows. Use it to help standardize deployment, evaluation, prompt
optimization, dataset curation from traces, and troubleshooting tasks across
agent-enabled development environments.

## Prerequisites

- An Azure account with an active subscription. If you don't have one,
  [create a free Azure account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- A coding agent host, such as GitHub Copilot in Visual Studio Code,
  Copilot CLI, or Claude Code.
- [Node.js](https://nodejs.org/) 18 or later on your `PATH`. The plugin uses
  `npx` to start MCP servers in compatible hosts.
- [Git](https://git-scm.com/downloads), so the host can download plugin and
  skill content.
- [Azure CLI](/cli/azure/install-azure-cli) installed and authenticated:

  ```azurecli
  az login
  ```

- [Azure Developer CLI](/azure/developer/azure-developer-cli/install-azd)
  installed and authenticated if you plan to use `azd` deployment workflows:

  ```bash
  azd auth login
  ```

- A Microsoft Foundry project if you want the agent to inspect or modify
  project-scoped resources. For setup steps, see
  [Create a project](../create-projects.md).

## What the Foundry Skill provides

The `microsoft-foundry` skill is a meta skill for Foundry work. It helps a
coding agent choose the right Foundry workflow, load the matching sub-skill,
inspect available Foundry MCP tools, and keep deployment and evaluation context
consistent across turns.

Use it when you want the agent to help with these capability areas:

| Capability area | What the skill helps the agent do |
| --- | --- |
| Foundry onboarding | Create or connect to a Foundry project, provision a Foundry resource, choose public or network-isolated setup, and prepare the workspace for agent development. |
| Access and capacity | Check RBAC assignments, managed identities, service principals, quota, model availability, region capacity, and deployment prerequisites. |
| Model deployment | Deploy models with quick presets or custom settings such as version, SKU, capacity, and responsible AI configuration. |
| Model customization | Fine-tune models with supervised fine-tuning, direct preference optimization, or reinforcement fine-tuning workflows. |
| Agent creation | Create hosted agent applications that use Microsoft Agent Framework, LangGraph, or custom frameworks in Python or C#. |
| Agent deployment | Containerize an agent, build and push images to Azure Container Registry, create or update hosted agent deployments, and redeploy after code changes. |
| Invocation and testing | Send single-turn or multi-turn messages to deployed agents, test prompt agents, and test hosted agents that use HTTP or WebSocket-based protocols. |
| Evaluation and optimization | Run batch evaluations, set up continuous evaluation, compare versions, optimize prompts, improve agent instructions, and prepare Agent Optimizer jobs. |
| Trace and dataset work | Query traces, analyze latency or failures, correlate evaluation results with responses, and curate evaluation datasets from production traces. |
| Troubleshooting | Inspect hosted agent logs, query telemetry, diagnose deployment or runtime failures, and plan a repair-and-redeploy loop. |

The installed skill includes specialized sub-skills for those areas. You don't
usually need to name the sub-skill directly. Ask for the outcome you want, and
the coding agent uses the skill instructions to route the task.



## Installation

### [VS Code](#tab/vscode)

The [Foundry Toolkit extension for VS Code](https://aka.ms/foundrytk) comes with the Foundry Skill. To install the extension, see [Work with the Microsoft Foundry for Visual Studio Code extension](get-started-projects-vs-code.md).

After installation, reload Visual Studio Code if prompted. Open Copilot Chat,
switch to agent mode, and confirm that Foundry skills are available. When
prompted, sign in with the Azure account that has access to your Foundry
project.

For more information about MCP setup in Visual Studio Code, see
[Get started with the Azure MCP Server](/azure/developer/azure-mcp-server/get-started/tools/visual-studio-code)
and [Get started with Foundry MCP Server](../../mcp/get-started.md).

### [Coding agents such as Copilot CLI and Claude Code](#tab/coding-agents)

The [Azure Skills Plugin](https://github.com/microsoft/azure-skills) bundles a curated set of Azure skills—including the Foundry Skill, Azure MCP Server configuration, and Foundry MCP Server—into a single install. Together, they give coding agents an optimized experience for building with Foundry and other Azure services.

#### [Copilot CLI](#tab/copilot-cli)
Run the plugin commands inside Copilot CLI.

1. Add the Azure Skills Plugin marketplace the first time you install from it:

   ```text
   /plugin marketplace add microsoft/azure-skills
   ```

1. Install the plugin:

   ```text
   /plugin install azure@azure-skills
   ```

1. Check that the plugin configured MCP servers for Azure and Foundry:

   ```text
   /mcp show
   ```

1. Update the plugin when you want the latest skills and MCP configuration:

   ```text
   /plugin update azure@azure-skills
   ```

#### [Claude Code](#tab/claude-code)

Run the plugin commands inside Claude Code.

1. Install the Azure plugin:

   ```text
   /plugin install azure@claude-plugins-official
   ```

1. If you prefer marketplace discovery, run `/plugin` and search for `azure`.
1. Update the plugin when you want the latest skills and MCP configuration:

   ```text
   /plugin update azure@claude-plugins-official
   ```

1. Restart Claude Code if the Azure or Foundry tools don't appear after
   installation.

---

#### [Install just the Foundry Skill](#tab/foundry-skill-alone)

If your host already has MCP server configuration and you only need the skill
content, install the `microsoft-foundry` skill directly:

```bash
npx skills add https://github.com/microsoft/azure-skills --skill microsoft-foundry
```

The skill-only path downloads the Foundry workflow guidance. Use the Azure
Skills Plugin when you want the skill, Azure MCP Server configuration, and
Foundry MCP Server configuration installed together.

## Verify the setup

After installation, try these checks from your coding agent:

- Ask `What AI models are available in Microsoft Foundry?` The response should
  use Foundry tools instead of a generic summary.
- Ask `List my Azure resource groups.` The response should use Azure MCP tools
  after you authenticate.
- In a Foundry agent project, ask `Use the Microsoft Foundry Skill to review
  this agent for deployment readiness.` The response should identify workflow
  checks such as configuration, project access, model deployment, evaluation
  data, and deployment validation.

If a check fails, reload the host, confirm the plugin installed successfully,
and verify that `az login` uses the subscription that contains your Foundry
resources.

## Use the skill in a project

Open the folder that contains your Foundry agent code. Ask for the outcome you
want, and include the target project, environment, agent folder, or deployment
name if you already know it.

Use these prompt patterns to invoke the skill's capabilities:

| Goal | Example prompt | Typical workflow |
| --- | --- | --- |
| Set up Foundry for a new agent | `Use the Microsoft Foundry Skill to create a public Foundry project, deploy a model, and scaffold a hosted agent.` | Project setup, model deployment, agent creation, deployment, and invocation. |
| Set up a private environment | `Use the Microsoft Foundry Skill to plan a network-isolated Foundry deployment for this project.` | Private-network planning, template selection, deployment checks, and validation. |
| Deploy an existing hosted agent | `Use the Microsoft Foundry Skill to prepare this hosted agent for deployment to my dev environment.` | Workspace context resolution, container build, ACR push, hosted agent deployment, and smoke test. |
| Redeploy after code changes | `Use the Microsoft Foundry Skill to redeploy this agent and verify it still responds correctly.` | Deployment update, invocation, and evaluation follow-up. |
| Test an agent | `Use the Microsoft Foundry Skill to invoke this agent with a short multi-turn test conversation.` | Agent lookup, invocation, and response review. |
| Evaluate quality | `Use the Microsoft Foundry Skill to create an evaluation plan for this agent from eval.yaml.` | Evaluation suite setup, dataset and evaluator checks, batch evaluation, and result summary. |
| Optimize instructions | `Use the Microsoft Foundry Skill to improve the agent instructions based on recent evaluation results.` | Evaluation analysis, prompt optimization, candidate review, and follow-up evaluation. |
| Build an evaluation dataset | `Use the Microsoft Foundry Skill to create an evaluation dataset from the last seven days of production traces.` | Trace query, dataset curation, versioning, and lineage tracking. |
| Troubleshoot a failure | `Use the Microsoft Foundry Skill to troubleshoot why this hosted agent deployment is failing.` | Invocation check, logs, telemetry, root-cause analysis, repair plan, redeploy, and retest. |
| Check access or capacity | `Use the Microsoft Foundry Skill to check RBAC and quota blockers before I deploy this model.` | Role assignment review, quota lookup, capacity planning, and remediation steps. |
| Fine-tune a model | `Use the Microsoft Foundry Skill to plan a supervised fine-tuning workflow for this training dataset.` | Dataset readiness, training setup, checkpoint review, model deployment, and evaluation. |

Before you approve changes or commands, review the plan, generated files, and
Azure resources the agent proposes to create or modify. For deployment,
fine-tuning, and provisioning tasks, confirm role assignments and cost-bearing
resources before the agent runs commands.

## Use Foundry Toolkit skills in VS Code

[Foundry Toolkit for Visual Studio Code](https://code.visualstudio.com/docs/intelligentapps/overview)
also makes Foundry-specific skills available in VS Code. These skills, such as
`vscode-microsoft-foundry` and `foundrytk-quick-start`, focus on the VS Code
development experience: onboarding to Foundry Toolkit, exploring models,
building agents, selecting a model, deploying an agent, evaluating performance,
and managing toolboxes. They're different from the core `microsoft-foundry`
skill, which provides the broader knowledge base and concrete workflow details
for Foundry resource management, RBAC, quotas, model deployment, hosted agent
deployment, evaluation, tracing, and troubleshooting. Install Foundry Toolkit
for VS Code to make these extension-provided skills available in your VS Code
agent experience.

## How the skill works

When a coding agent uses the Microsoft Foundry Skill, it follows a few common
patterns:

1. It starts with Foundry MCP discovery so it knows which Foundry tools and
  parameters are available in your environment.
1. It loads the sub-skill that matches your workflow, such as creation,
  deployment, invocation, evaluation, tracing, troubleshooting, RBAC, quota, or
  model deployment.
1. It resolves project and agent context from your workspace before it proposes
  changes or commands.
1. It prefers structured Foundry and Azure MCP tools when they're available.
1. It asks for missing values only when they can't be resolved from your prompt,
  workspace files, or authenticated Azure context.

The skill supports two common agent types:

| Agent type | Use case |
| --- | --- |
| Prompt agent | An LLM-backed agent that uses a model deployment and prompt configuration. |
| Hosted agent | A container-based agent that runs custom code in Foundry Agent Service. |

For hosted agent workflows, the skill can also work with agents that use the
`responses`, `invocations`, or `invocations_ws` protocols. Use
`invocations_ws` for real-time or duplex WebSocket scenarios, such as voice
agents or streaming interactions.

## Workspace files the skill uses

The skill looks for Foundry project and agent context in common workspace files.
Keep these files current so your coding agent can make specific, repeatable
recommendations.

| File or folder | How the skill uses it |
| --- | --- |
| `azure.yaml` | Finds `azd` services, agent project folders, deployment host settings, and environment bindings. |
| `.azure/<environment>/.env` | Resolves authenticated `azd` environment values such as subscription, resource group, project endpoint, agent name, registry, and Application Insights connection string. |
| `.foundry/agent-metadata.yaml` | Stores Foundry-specific overlay state such as evaluation suite references, dataset references, local cache paths, result summaries, and non-`azd` overrides. |
| `.foundry/agent-metadata.<env>.yaml` | Stores environment-specific overlay state for a target such as production or CI. |
| `agent.yaml` | Provides local agent configuration for create, deploy, invoke, and evaluation workflows. |
| `eval.yaml` | Defines local evaluation intent, such as dataset file, evaluator names, pass threshold, sample count, trace lookback, and generation instructions. |

For deployment and evaluation workflows, prefer `.foundry/agent-metadata.yaml`
for nonsecret overlay state. Don't store secrets in `.foundry` files. If `azd`
already provides a deployment value, such as a project endpoint or registry, let
the coding agent use the `azd` value instead of duplicating it in metadata.

## Troubleshooting

| Issue | Resolution |
| ----- | ---------- |
| The host doesn't find the skill. | Confirm the plugin installed successfully, then reload or restart the host so it re-indexes plugin content. |
| MCP tools don't appear. | Confirm Node.js is installed, `npx` works, and the Azure and Foundry MCP server entries were added for your host. |
| Azure requests fail with authentication errors. | Run `az login` again. For `azd` workflows, also run `azd auth login`. |
| The agent uses the wrong subscription. | Set the intended Azure subscription in Azure CLI before you retry the prompt. |
| Foundry project operations fail. | Confirm your account has access to the Foundry project and required Azure RBAC roles. |

## Related content

- [Azure Skills Plugin](https://github.com/microsoft/azure-skills)
- [Microsoft Foundry Skill](https://www.skills.sh/microsoft/azure-skills/microsoft-foundry)
- [Prepare your development environment](install-cli-sdk.md)
- [Quickstart: Deploy your first hosted agent](../../agents/quickstarts/quickstart-hosted-agent.md)
- [Get started with Foundry MCP Server](../../mcp/get-started.md)