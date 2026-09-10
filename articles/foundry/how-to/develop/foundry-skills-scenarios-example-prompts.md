---
title: "Microsoft Foundry Skill example prompts and scenarios"
description: "Use Microsoft Foundry Skill example prompts to delegate common Foundry resource setup, hosted agent, Prompt Agent, evaluation, tracing, optimization, CI/CD, and cleanup workflows to a coding agent."
keywords: microsoft foundry skill, azure skills plugin, coding agents, copilot, claude code, foundry mcp
author: bobtabor-msft
ms.author: rotabor
ms.reviewer: junjieli
ms.date: 08/06/2026
ms.service: microsoft-foundry
ms.topic: how-to
ms.custom:
  - dev-focus
  - doc-kit-assisted
ai-usage: ai-assisted
---

# Foundry Skills scenarios and example prompts

Use the prompts in this article with a coding agent host that has the [Microsoft Foundry Skill installed](./use-microsoft-foundry-skill.md), such as GitHub Copilot in Visual Studio Code, Copilot CLI, Codex, or Claude Code. The prompts are grouped by scenario so you can find the right workflow without moving across multiple quickstarts.

Replace example names, endpoints, model deployments, and user email addresses with values from your own Foundry project. The Microsoft Foundry Skill stops and asks you to sign in when authentication is required. You should sign in interactively yourself with tools such as Azure CLI and Azure Developer CLI.

## Create and administer Foundry resources

Use these prompts when you need a Foundry project, a model deployment, or role assignments before building agents.

### Create a Foundry project

This scenario creates the Foundry account, project, Application Insights resource, managed identity, and role assignments required for basic Foundry development.

```text
Use the Microsoft Foundry Skill project-creation workflow to create a new
Foundry project named my-foundry-project. Confirm my subscription and the
target region before you provision anything, and show me the resource group
name you'll use.
```

### Deploy a model with SKU, version, and quota validation

This scenario deploys a specific model to a Foundry project and asks the skill to validate regional availability, model version, SKU support, and quota before deployment.

```text
Use the Microsoft Foundry Skill deploy-model customize workflow to deploy
gpt-5.1-mini with Standard SKU and capacity 10 to my Foundry project. Before
you deploy, dynamically validate three things: that gpt-5.1-mini supports the
Standard SKU in the target region (from the model catalog), that model
version 2025-04-14 (or the version you propose) is available, and that my
subscription has at least 10 units of unallocated quota for
OpenAI.Standard.gpt-5.1-mini. If any check fails, stop and propose a
different region, SKU, capacity, or version that satisfies my request, and
ask before deploying.
```

### Assign project access to users

This scenario grants the Foundry User role at project scope so team members can use the project and deployed models.

```text
Use the Microsoft Foundry Skill RBAC workflow to assign the Foundry User
role at project scope on my-foundry-project to the following users:
alice@contoso.com, bob@contoso.com. Show me each resulting role assignment
so I can verify it before I share the project endpoint with my team.
```

## Build and deploy hosted agents

Use these prompts to create hosted agents from samples or from your own Python code, then deploy and validate them in Foundry Agent Service.

### Build a toolbox-backed hosted agent

This scenario creates a Python hosted agent that uses a Foundry toolbox containing web search and the public Microsoft Learn MCP server. It asks the coding agent to verify the environment, initialize the sample, create the toolbox, test locally, and stop before deployment.

```text
Use the Microsoft Foundry Skill to build and deploy a Python hosted agent that
uses a Foundry toolbox. Verify my environment first, and stop if I need to sign
in myself. Initialize the Agent Framework Responses API toolbox sample from
https://github.com/microsoft-foundry/foundry-samples/blob/main/samples/python/hosted-agents/agent-framework/responses/04-foundry-toolbox/azure.yaml
in an empty my-toolbox-agent workspace, with the agent source in
src/toolbox-agent. Use 1 core and 2 GiB of memory for the agent. Ask before you
create a new Foundry project, or use the existing project and chat-capable model
deployment that I provide.

Create a toolbox named my-toolbox from src/toolbox-agent/toolbox.yaml. Confirm
that it contains web search and the public Microsoft Learn MCP server, capture
its versioned MCP endpoint, and configure the agent to use that endpoint. Test
the agent locally with one web-search prompt and one Microsoft Learn prompt.
After the local tests succeed, stop and show me the deployment plan before you
deploy the agent or create additional Azure resources.
```

### Deploy and remotely validate a toolbox-backed hosted agent

This scenario continues the toolbox workflow after local tests succeed. It stores the toolbox MCP endpoint, deploys the hosted agent, invokes it remotely, and confirms that the deployed agent can discover and use toolbox tools.

```text
Continue with the Microsoft Foundry Skill workflow. Store the versioned
my-toolbox MCP endpoint in the azd environment as TOOLBOX_ENDPOINT, deploy the
hosted agent to Foundry Agent Service, and show the deployment status,
endpoint, and playground link. Then invoke it remotely with: "What's new in
Microsoft Foundry? Use the Microsoft Learn documentation." Confirm that the
deployed agent discovered and used the toolbox tools. If the skill workflow
requires evaluation suite generation before the final summary, submit the
generation job and show me the follow-up eval command.
```

### Add the required skill marker to an existing project

This scenario adds the project guidance file that helps coding agent hosts reload the Microsoft Foundry Skill for an existing hosted-agent project.

```text
Use the Microsoft Foundry Skill create-hosted workflow to add the required
AGENTS.md (or CLAUDE.md for Claude Code) marker for the microsoft-foundry
skill at the project root. If the file already exists, weave the marker into
the existing content instead of overwriting it.
```

### Initialize existing Python code as a hosted agent

This scenario uses the brownfield hosted-agent workflow to initialize existing Python code with `azd ai agent init --src`, preserve your current agent logic, run available tests, and smoke test locally before deployment.

```text
Use the Microsoft Foundry Skill brownfield hosted-agent workflow to initialize
my existing Python code as an azd hosted agent with --deploy-mode code. Before
you run azd ai agent init --src, show me a diff of any file the workflow would
create or change, and if I have existing tests, run them so I can verify my
agent logic still works before you continue. For an existing Foundry project,
pass its ARM resource ID to --project-id (resolve the ARM ID from a project
endpoint using the skill's resolve script if I only have the endpoint). If I
don't provide an existing project, stop and ask me before creating a new one.
After init, run azd ai agent run and azd ai agent invoke --local for a single
smoke test.
```

### Deploy and invoke a hosted agent from existing code

This scenario deploys the initialized hosted agent, shows deployment details, and branches validation based on whether your agent uses the Responses protocol or the Invocations protocol.

```text
Continue with the Microsoft Foundry Skill deploy workflow. Run azd deploy,
then show me the agent status, playground link, and endpoint. If my agent
uses the Responses protocol, invoke it with a plain-text prompt:
  azd ai agent invoke "Hello from my hosted agent"
If my agent uses the Invocations protocol, inspect my handler for the
expected request schema, write a matching input file, and invoke with:
  azd ai agent invoke --protocol invocations --input-file <path>
Do not pass --output json to invoke.
```

## Create and validate Prompt Agents

Use these prompts when you want the Microsoft Foundry Skill to create a Prompt Agent and validate multi-turn conversation state.

### Create a Prompt Agent

This scenario creates a Prompt Agent with a deployed model. It asks the coding agent to fetch the prompt-agent schema, check for an existing agent with the same name, and stop before updating an existing agent.

```text
Use the Microsoft Foundry Skill create-prompt workflow to create a prompt
agent named MyAgent on PROJECT_ENDPOINT, using the MODEL_DEPLOYMENT_NAME
model deployment. Before you create the agent, call
agent_definition_schema_get with schemaType prompt to fetch the current
schema, then call agent_get to check whether an agent named MyAgent already
exists. If it exists, stop and ask me whether to update it, use a different
name, or cancel - do not silently create a new version of an existing agent.
Give the agent short instructions to answer general questions concisely,
and show me the agent name and ID once it's created.
```

### Invoke a Prompt Agent across two turns

This scenario verifies that a Prompt Agent retains context by reusing the same `conversationId` across two `agent_invoke` calls.

```text
Continue with the Microsoft Foundry Skill invoke workflow for a Prompt Agent.
Call agent_invoke on MyAgent with an initial prompt of my choice, capture the
conversationId returned by that call, and then call agent_invoke a second
time with a follow-up that only makes sense if the agent remembers turn one,
passing the same conversationId so the second turn continues the same
conversation. Show me both prompts, both responses, and the conversationId
you reused.
```

## Evaluate and observe hosted agents

Use these prompts to inspect a deployed hosted agent, prepare and run evaluations, review row-level results, and find traces.

### Inspect a deployed hosted agent

This scenario confirms the deployed hosted agent name, version, project endpoint, and container status, then performs a simple invocation without editing or redeploying the agent.

```text
Use the Microsoft Foundry Skill to inspect the hosted agent in this workspace.
Resolve the agent root and current azd environment, then confirm the deployed
agent name, version, project endpoint, and container status. Invoke it with:
"Write a haiku about deploying cloud applications." Don't edit or redeploy the
agent. Stop and tell me if I need to authenticate.
```

### Prepare a smoke evaluation suite

This scenario prepares an evaluation suite for a deployed hosted agent using a known query, expected behavior, and built-in intent resolution and task adherence evaluators.

```text
Use the Microsoft Foundry Skill observe workflow to prepare a smoke
evaluation suite for the deployed hosted agent in this workspace. Reuse a
matching eval.yaml and current .foundry evaluation cache if they exist; don't
refresh or overwrite cached artifacts without my approval. For this quickstart,
use the query "Write a haiku about deploying cloud applications." with the
expected behavior "The response is a haiku about deploying cloud applications."
Then evaluate intent resolution and task adherence. Use an existing
chat-completion deployment in the project as the judge model. Before creating or
changing anything, show me
the selected agent root, azd environment, metadata file, agent name and version,
judge deployment, test data, and evaluators.
```

### Run a smoke evaluation and summarize results

This scenario runs the selected evaluation, waits for a terminal state, downloads row-level results, clusters failures, and reports evaluation details without changing the agent.

```text
Continue with the Microsoft Foundry Skill observe workflow. Run the
selected smoke evaluation against the deployed hosted agent and poll it to a
terminal state. Download the row-level output items, save the results under
.foundry/results, and cluster any failures before summarizing the run. Show the
evaluation ID, run ID, agent version, aggregate results, row-level results, and
Foundry portal report link. Don't optimize, edit, or redeploy the agent.
```

### Review one row-level evaluation result

This scenario inspects the result for a specific evaluation query, including the agent response and evaluator pass or fail details.

```text
Show the row-level result for the haiku query. Include the agent response and,
for each evaluator, the pass or fail result, score, and explanation. If anything
failed, explain the root cause without changing the agent.
```

### Trace a hosted agent invocation

This scenario invokes a deployed hosted agent, finds the resulting trace in Application Insights, and reports telemetry details without changing application or Azure resources.

```text
Use the Microsoft Foundry Skill to trace the deployed hosted agent in this
workspace. Resolve the agent, azd environment, Foundry project, and connected
Application Insights resource from the workspace and my authenticated Azure
context. Verify that the hosted agent version is active, and then invoke it
with: "Summarize the benefits of distributed tracing for AI agents."

Use the Foundry trace workflow to find the new trace from the last hour.
Show me any KQL query before you run it, and report the trace ID, response ID,
duration, status, and span summary. Don't change my application or Azure
resources. If authentication is required, stop and ask me to sign in myself.
```

## Optimize hosted agents

Use these prompts when you have a deployed Python hosted agent with a baseline agent configuration and want to run Agent Optimizer before applying a candidate.

### Run an optimization job

This scenario resolves Foundry project context, verifies baseline and model deployment prerequisites, generates or updates evaluation configuration, runs optimization with two candidates, and stops before applying any candidate.

```text
Use the Microsoft Foundry Skill agent-optimizer workflow on this Python
hosted agent. Resolve project context from azd env get-values first; ask me
for an ARM resource ID or endpoint only if you can't resolve one from the
current azd environment. Confirm .agent_configs/baseline/ is present, verify
that my eval model deployment and optimization model deployment already
exist in the resolved Foundry project, then generate or update eval.yaml and
run azd ai agent optimize with max-candidates 2. Monitor the job to
completion, print baseline and best-candidate scores side by side, and stop
for my approval before applying any candidate.
```

### Apply an approved optimization candidate

This scenario applies a selected optimization candidate, reviews the diff, deploys the optimized agent, and validates the deployed response.

```text
The best candidate improves on baseline for my target metrics. Apply
candidate <candidate-id> with azd ai agent optimize apply, review the diff,
and then run azd deploy. After deploy, invoke the agent with:
  azd ai agent invoke "What is your return policy?"
and confirm the deployment succeeded and the response looks reasonable.
```

## Automate deployment with CI/CD

Use this prompt when you want the Microsoft Foundry Skill to adapt the hosted-agent GitHub Actions workflow to your repository.

### Create a GitHub Actions workflow for a hosted agent

This scenario generates `.github/workflows/hosted-agent-cd.yml` from the quickstart template, fills in project-specific values from the deployed `azd` environment, and lists the repository variables you must create.

```text
Use the Microsoft Foundry Skill CI/CD sub-skill to help me apply the official
hosted-agent CI/CD quickstart to my repository. Read my deployed azd
environment with azd env get-values for the selected environment (do not
copy values out of .azure/<env>/.env unless azd env get-values is
unavailable). Generate .github/workflows/hosted-agent-cd.yml from the article
template with my agent root, azd environment name, and a safe smoke-test
prompt filled in. Then list every repository variable I need to create,
mark which ones can be derived from azd env, and tell me where to find the
values that azd doesn't provide (for example AZURE_CLIENT_ID from my OIDC
app registration).
```

## Clean up

Use this prompt to identify resources before deleting anything created by a Foundry Skills quickstart.

### Review toolbox-agent cleanup commands

This scenario identifies the toolbox, hosted agent, and Azure resources created by the toolbox quickstart, then shows exact cleanup commands for review before any deletion command runs.

```text
Use the Microsoft Foundry Skill to identify my-toolbox, the hosted agent,
and the Azure resources created for this quickstart. Show me the resources
and the exact cleanup commands before any deletion command runs. Confirm
whether azd down is safe for this resource group.
```

## Related content

- [Azure Skills Plugin](https://github.com/microsoft/azure-skills)
- [Microsoft Foundry Skill](https://www.skills.sh/microsoft/azure-skills/microsoft-foundry)
- [Prepare your development environment](install-cli-sdk.md)
- [Quickstart: Deploy your first hosted agent](../../agents/quickstarts/quickstart-hosted-agent.md)
- [Get started with Foundry MCP Server](../../mcp/get-started.md)