---
title: "agent.yaml schema reference"
description: "Reference for the AgentSchema YAML used to define hosted agents: AgentDefinition, AgentManifest, ContainerAgent, fields, resources, and variable substitution."
author: aahill
ms.author: aahi
ms.manager: mcleans
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.topic: reference
ms.date: 06/15/2026
ms.custom: doc-kit-assisted
ai-usage: ai-assisted
---

# agent.yaml schema reference

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

The [AgentSchema specification](https://microsoft.github.io/AgentSchema/) is an open standard for defining AI agents. When you build hosted agents, you primarily work with three top-level schema types: **AgentDefinition**, **AgentManifest**, and **ContainerAgent**. The schema isn't specific to one tool. The Azure Developer CLI (`azd`) and the Microsoft Foundry Toolkit for Visual Studio Code both use it.

The schema appears in two file contexts with distinct naming conventions:

* `agent.manifest.yaml` is an **AgentManifest**, a parameterized template that template authors and samples publish. The `azd ai agent init -m` command reads it.
* `agent.yaml` is an **AgentDefinition**, the concrete configuration that `azd ai agent init` writes into your project at `src/<agent>/agent.yaml`. This is the file you edit day to day.

Both files describe *what* an agent is: its model, tools, protocols, environment, and resources. This is distinct from `azure.yaml`, which describes *how* to provision and deploy Azure resources. For the `azure.yaml` reference, see [azure.yaml reference for hosted agents](azure-yaml-reference.md).

## Schema types

### AgentDefinition

An AgentDefinition is a concrete specification of an agent that's ready to run. It describes a single agent instance with a specific configuration and no `{{ parameter }}` template placeholders.

Every AgentDefinition has a `kind` field that determines the agent type.

| Kind | Description |
| ---- | ----------- |
| `prompt` | A prompt-based agent configured through instructions only. |
| `hosted` | A containerized agent deployed as a container image. |
| `workflow` | An orchestration agent that coordinates other agents. |

A generated AgentDefinition can still contain `${VAR_NAME}` references. These are `azd` environment variable placeholders, not part of the AgentSchema specification. They let a single definition file work across multiple `azd` environments by resolving values from each environment's `.azure/<env>/.env` file at deploy time.

### AgentManifest

An AgentManifest is a parameterized template for creating agents dynamically. It wraps an AgentDefinition as its `template` field and adds:

* `parameters`: values that are prompted or injected at creation time, using `{{ parameter }}` substitution syntax.
* `resources`: external dependencies such as model deployments, toolboxes, or connections.

Use an AgentManifest when you need reusable templates or want to deploy similar agents with different configurations. When you run `azd ai agent init`, you typically point at a manifest, either by selecting a template or providing a URL. The init process prompts for parameter values and generates an AgentDefinition.

### ContainerAgent

A ContainerAgent is an AgentDefinition with `kind: hosted`. It extends the base definition with container-specific fields and is the `template` inside an AgentManifest when you build a hosted agent.

### When to use a manifest or a definition

| Use a manifest when | Use a definition when |
| ------------------- | --------------------- |
| You publish a reusable agent template for others to instantiate. | You deploy a specific, single-purpose agent. |
| You want users to configure the model, tools, or connections at init time. | All configuration values are known and fixed. |
| You build a sample or starter template. | You already ran `azd ai agent init` and have a generated definition. |

Most developers start from a manifest through `azd ai agent init` and then work with the generated definition. Template authors and sample publishers are the primary creators of manifests.

## Top-level fields

The reference below documents the manifest fields, which are a superset of the definition fields.

| Field | Type | Required | Description |
| ----- | ---- | -------- | ----------- |
| `name` | string | Yes | Name of the agent manifest. |
| `description` | string | No | Description of the agent. |
| `metadata` | object | No | Additional metadata, such as `tags`. |
| `template` | ContainerAgent | Yes | The agent definition template. |
| `parameters` | object | No | Configurable parameters prompted during init. |
| `resources` | array | Yes | Resources required by the agent. |

## template (ContainerAgent)

The `template` field defines the hosted container agent.

| Field | Type | Required | Description |
| ----- | ---- | -------- | ----------- |
| `name` | string | Yes | Agent name. |
| `kind` | string | Yes | Must be `hosted` for hosted agents. |
| `protocols` | array | Yes | Protocol support. |
| `environment_variables` | array | No | Environment variables for the container. |
| `resources` | object | No | Container CPU and memory resources. |
| `image` | string | No | Prebuilt container image path. |
| `dockerfilePath` | string | No | Path to the Dockerfile. |

### protocols

```yaml
protocols:
  - protocol: responses    # OpenAI Responses API
    version: 1.0.0
```

| Protocol | Description |
| -------- | ----------- |
| `responses` | OpenAI Responses API. Includes conversation history management. |
| `invocations` | Custom payload protocol. No built-in conversation management. |

For the full protocol specification, see [Hosted agent runtime contract](hosted-agent-contract.md).

### environment_variables

```yaml
environment_variables:
  - name: AZURE_AI_MODEL_DEPLOYMENT_NAME
    value: ${AZURE_AI_MODEL_DEPLOYMENT_NAME}
```

The `${ }` syntax references `azd` environment variables from `.azure/<env>/.env`.

> [!NOTE]
> Don't declare `FOUNDRY_PROJECT_ENDPOINT` in `environment_variables`. The platform injects it automatically into hosted containers, and `azd ai agent run` sets it for local development. Declaring it here is redundant and risks shadowing the platform value.

## parameters

Parameters are prompted during `azd ai agent init`. Use `secret: true` for sensitive values.

```yaml
parameters:
  github_pat:
    secret: true
    description: GitHub Personal Access Token
```

## resources

Resources define what the agent needs. The shapes below describe what manifests declare and what `azd ai agent init` writes into your project. After init, manage the same project-scoped resources at runtime with direct CLI commands: `azd ai connection`, `azd ai toolbox`, `azd ai skill`, and `azd ai routine`.

> [!NOTE]
> The schema doesn't include a skills field. The `azd ai agent init`, `azd ai agent run`, and `azd up` commands don't auto-download skills. Manage skills as project-level resources with `azd ai skill` and wire them into your agent runtime yourself.

### Model resource

```yaml
resources:
  - kind: model
    name: chat
    id: gpt-4.1-mini
```

### Connection resource

```yaml
resources:
  - kind: connection
    name: MyConnection
    target: https://api.example.com
    category: remoteTool
    credentials:
        type: CustomKeys
        keys:
            Authorization: "Bearer {{ my_api_key }}"
```

### Toolbox resource

```yaml
resources:
  - kind: toolbox
    name: agent-tools
    description: Agent toolbox
    tools:
      - name: webSearch
        type: builtin
        capability: web-search
      - name: codeInterpreter
        type: builtin
        capability: code-interpreter
      - name: myMcp
        type: connection
        connection: "{{ MyConnection }}"
```

A toolbox version carries three kinds of entries: raw `tools` entries (built-in capabilities like `web-search` or `code-interpreter`), `connections` (project connections such as a remote-tool MCP server or a search index), and `skills` (references to existing project skills). The `tools` slot is declared up front in the manifest. Add connections and skill references incrementally with `azd ai toolbox connection add` and `azd ai toolbox skill add`.

## Complete example

```yaml
name: my-web-search-agent
description: An agent with web search and MCP tools

metadata:
  tags:
    - AI Agent Hosting

template:
  name: my-web-search-agent
  kind: hosted
  protocols:
    - protocol: responses
      version: 1.0.0
  environment_variables:
    - name: AZURE_AI_MODEL_DEPLOYMENT_NAME
      value: ${AZURE_AI_MODEL_DEPLOYMENT_NAME}
    - name: TOOLBOX_ENDPOINT
      value: ${TOOLBOX_ENDPOINT}

parameters:
  github_pat:
    secret: true
    description: GitHub PAT for MCP connection

resources:
  - kind: model
    name: chat
    id: gpt-4.1-mini

  - kind: connection
    name: GithubMcpConnection
    target: https://api.githubcopilot.com/mcp
    category: remoteTool
    credentials:
        type: CustomKeys
        keys:
            Authorization: "Bearer {{ github_pat }}"

  - kind: toolbox
    name: agent-tools
    description: Web search and GitHub MCP tools
    tools:
      - name: webSearch
        type: builtin
        capability: web-search
      - name: github
        type: connection
        connection: "{{ GithubMcpConnection }}"
```

## Variable substitution

Substitution happens in two layers: manifest parameters resolve at init time, and environment variables resolve at run or deploy time. One definition file can then work across all your `azd` environments.

| Syntax | Resolved when | By what |
| ------ | ------------- | ------- |
| `{{ param_name }}` | `azd ai agent init` | Manifest parameter values prompted from the user. |
| `${VAR_NAME}` | `azd deploy` or `azd ai agent run` | `azd` environment variables from `.azure/<env>/.env`. |

## Related content

* [AgentSchema specification](https://microsoft.github.io/AgentSchema/)
* [azure.yaml reference for hosted agents](azure-yaml-reference.md)
* [Hosted agent runtime contract](hosted-agent-contract.md)
* [What are hosted agents?](hosted-agents.md)
