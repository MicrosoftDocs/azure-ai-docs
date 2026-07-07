---
title: "azure.yaml reference for hosted agents"
description: "Reference for the unified azd azure.yaml project file for hosted agents: services, host types, model deployments, agent configuration, dependencies, file includes, and infrastructure."
author: aahill
ms.author: aahi
ms.manager: mcleans
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.topic: reference
ms.date: 07/01/2026
ms.custom: doc-kit-assisted
ai-usage: ai-assisted
---

# azure.yaml reference for hosted agents

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

The `azure.yaml` file is the single Azure Developer CLI (`azd`) project configuration for a hosted agent project. It declares your Foundry resources -- the project, model deployments, connections, toolboxes, skills, routines, and the agents themselves -- as a set of services, and it tells `azd` how to provision and deploy them. This unified file replaces the earlier two-file model that split configuration between `agent.manifest.yaml` and `agent.yaml`.

To learn how to compose and author this file step by step, see [Author azure.yaml for hosted agents](../how-to/author-azure-yaml.md).

## How azd uses azure.yaml

The Azure Developer CLI streamlines the developer-to-cloud workflow. It handles two things: provisioning Azure resources, such as Foundry projects, model deployments, and container registries; and deploying your code to those resources. For hosted agents, the `azure.ai.agents` extension adds agent-specific commands such as `azd ai agent init` and `azd ai agent run`.

Every `azd` project has an `azure.yaml` file at its root. For agent projects, this file is the source of truth for both the agent configuration and the deployment configuration.

### Environments

An environment is a named configuration, such as `dev`, `staging`, or `prod`, that stores settings for a particular deployment. Each environment tracks the Azure subscription and location, the resource group and resource names, and any custom variables you set. Settings are stored locally in `.azure/<env-name>/.env`. You can have multiple environments for the same project.

### Core commands

| Command | What it does |
| ------- | ------------ |
| `azd provision` | Creates Azure resources, such as the Foundry project, model deployments, and container registry. |
| `azd deploy` | Builds and packages your agent, uploads it, and creates the hosted agent version. |
| `azd up` | Combines `provision` and `deploy` in one command. |
| `azd down` | Deletes all provisioned resources. |
| `azd env set` | Sets an environment variable, for example `azd env set FOUNDRY_MODEL_NAME=gpt-5.4-mini`. |

## The split-service model

Under `services`, each entry is a named service with a `host` field that identifies the kind of Foundry resource it declares. Services reference each other through the `uses` field, which forms a dependency graph that `azd` resolves at provision and deploy time. A typical project has one `azure.ai.project` service that owns the model deployments and one `azure.ai.agent` service that depends on it.

| Host | Resource | Purpose |
| ---- | -------- | ------- |
| `azure.ai.project` | Foundry project | Owns model deployments and optional private networking. |
| `azure.ai.agent` | Hosted or prompt agent | Carries the agent definition and its build and deploy settings. |
| `azure.ai.connection` | Project connection | Links the project to an external resource, such as an MCP server or a search index. |
| `azure.ai.toolbox` | Toolbox (Foundry Toolset) | A named bundle of connection-backed tools that agents reference. |
| `azure.ai.skill` | Skill | A reusable behavioral guideline shared across agents. |
| `azure.ai.routine` | Routine | A trigger plus an action that invokes an agent. |

## Minimal example

```yaml
# yaml-language-server: $schema=https://raw.githubusercontent.com/Azure/azure-dev/main/schemas/v1.0/azure.yaml.json
name: my-agent-project

services:
    ai-project:
        host: azure.ai.project
        deployments:
            - name: gpt-5.4-mini
              model:
                format: OpenAI
                name: gpt-5.4-mini
                version: "2026-03-17"
              sku:
                name: GlobalStandard
                capacity: 10

    my-agent:
        host: azure.ai.agent
        project: src/my-agent
        language: docker
        uses:
            - ai-project
        kind: hosted
        name: my-agent
        description: A hosted agent built from source.
        protocols:
            - protocol: responses
              version: 2.0.0
        env:
            FOUNDRY_MODEL_NAME: ${FOUNDRY_MODEL_NAME}
        container:
            resources:
                cpu: "0.25"
                memory: 0.5Gi
```

## Full example

The following project adds a connection, a toolbox, and private networking.

```yaml
# yaml-language-server: $schema=https://raw.githubusercontent.com/Azure/azure-dev/main/schemas/v1.0/azure.yaml.json
requiredVersions:
    extensions:
        azure.ai.agents: '>=0.1.0-preview'

name: research-agent-project

services:
    ai-project:
        host: azure.ai.project
        deployments:
            - name: gpt-5.4-mini
              model:
                format: OpenAI
                name: gpt-5.4-mini
                version: "2026-03-17"
              sku:
                name: GlobalStandard
                capacity: 50

    search-conn:
        host: azure.ai.connection
        uses:
            - ai-project
        category: CognitiveSearch
        target: https://my-search.search.windows.net
        authType: ApiKey
        credentials:
            key: ${SEARCH_API_KEY}

    research-tools:
        host: azure.ai.toolbox
        uses:
            - ai-project
            - search-conn
        description: Tools used by the research agent.
        tools:
            - type: azure_ai_search
              connection: search-conn
            - type: code_interpreter

    researcher:
        host: azure.ai.agent
        project: src/researcher
        language: docker
        uses:
            - ai-project
            - search-conn
            - research-tools
        kind: hosted
        name: researcher
        description: Hosted research agent built from source.
        startupCommand: python main.py
        toolboxes:
            - research-tools
        env:
            LOG_LEVEL: info
        protocols:
            - protocol: responses
              version: 2.0.0
        container:
            resources:
                cpu: "1.0"
                memory: 2Gi

infra:
    provider: bicep
    path: ./infra
```

## Top-level fields

| Field | Required | Description |
| ----- | -------- | ----------- |
| `name` | Yes | Project name. |
| `requiredVersions.extensions` | No | Minimum extension version constraints, for example `azure.ai.agents: '>=0.1.0-preview'`. |
| `metadata` | No | Project metadata, such as the `template` identifier. |
| `services` | Yes | Map of service names to service configurations. |
| `infra` | No | Infrastructure-as-code settings. Present when you eject IaC. |

## azure.ai.project service

The project service provisions or connects to a Foundry project and owns its model deployments.

| Field | Description |
| ----- | ----------- |
| `host` | Must be `azure.ai.project`. |
| `endpoint` | Endpoint URL of an existing Foundry project. When set, `azd` connects to that project instead of provisioning a new one. When omitted, `azd` provisions a new project. |
| `deployments` | Array of model deployments to create on the project. |
| `network` | Optional private networking for the account that backs the project. |

### deployments

| Field | Description |
| ----- | ----------- |
| `name` | Deployment name. |
| `model.format` | Model format, for example `OpenAI`. |
| `model.name` | Model name, for example `gpt-5.4-mini`. |
| `model.version` | Model version string. |
| `sku.name` | SKU name, for example `GlobalStandard`, `Standard`, or `GlobalBatch`. |
| `sku.capacity` | SKU capacity in tokens-per-minute units. |

A deployment entry can also be an external file include: `- $ref: ./deployments/embeddings.yaml`.

### network

Set `network` to provision a network-secured account. The `peSubnet` field is required and establishes the account private endpoint. Add `agentSubnet` to inject the agent runtime into your own subnet (bring your own virtual network), or omit it to use the Microsoft-managed network. For a complete walkthrough, see [Hosted agent private networking](../how-to/virtual-networks.md).

## azure.ai.agent service

The agent service carries the agent definition and its build and deploy settings. It's the service that replaces the old `agent.yaml`.

| Field | Description |
| ----- | ----------- |
| `host` | Must be `azure.ai.agent`. |
| `kind` | Agent kind. Use `hosted` for containerized agents built from source. |
| `name` | Agent name. Reusing a name creates a new version of the existing agent. |
| `displayName` | Optional human-friendly display name. |
| `description` | Optional description of the agent. |
| `project` | Path to the agent source directory, for example `src/my-agent`. |
| `language` | Build language for hosted agents. Use `docker`. |
| `uses` | List of services this agent depends on, such as the project, connections, and toolboxes. |
| `protocols` | Invocation protocols the agent implements. |
| `env` | Map of environment variables passed to the container. |
| `container` | Container CPU and memory settings. |
| `startupCommand` | Command that starts the agent server, for example `python main.py`. Used by `azd ai agent run` for local development and for container startup. |
| `toolboxes` | List of `azure.ai.toolbox` service names the agent uses at runtime. |
| `codeConfiguration` | Source (ZIP) deploy settings. See [Deploy modes](#deploy-modes). |
| `image` | Prebuilt container image URL. When set, `azd` deploys the image directly and skips the Dockerfile build. |
| `metadata` | Optional metadata key-value pairs. |

### protocols

```yaml
protocols:
    - protocol: responses
      version: 2.0.0
```

| Protocol | Description |
| -------- | ----------- |
| `responses` | OpenAI Responses API. Includes conversation history management. |
| `invocations` | Custom payload protocol. No built-in conversation management. |
| `a2a` | Agent-to-agent protocol for agent orchestration. |

For the full protocol specification, see [Hosted agent runtime contract](hosted-agent-contract.md).

### env

```yaml
env:
    FOUNDRY_MODEL_NAME: ${FOUNDRY_MODEL_NAME}
    LOG_LEVEL: info
```

The `${ }` syntax references `azd` environment variables from `.azure/<env>/.env`.

> [!NOTE]
> Don't declare `FOUNDRY_PROJECT_ENDPOINT` in `env`. The platform injects it automatically into hosted containers, and `azd ai agent run` sets it for local development. Declaring it here is redundant and risks shadowing the platform value.

### container

```yaml
container:
    resources:
        cpu: "0.25"
        memory: 0.5Gi
```

Set `cpu` from `"0.25"` up to `"4.0"`, and `memory` from `0.5Gi` up to `8.0Gi`.

## azure.ai.connection service

A connection links the project to an external resource. The service key is the connection name, and the service depends on the project through `uses`.

| Field | Description |
| ----- | ----------- |
| `host` | Must be `azure.ai.connection`. |
| `category` | Connection category, for example `CustomKeys`, `ApiKey`, `AzureOpenAI`, `CognitiveSearch`, or `RemoteTool`. |
| `target` | Target endpoint URL or ARM resource ID. |
| `authType` | Authentication type, for example `ApiKey`, `CustomKeys`, `AAD`, `ManagedIdentity`, or `OAuth2`. |
| `credentials` | Credentials for the connection. Values can contain `${VAR}` references. |
| `metadata` | Additional metadata as key-value pairs. |

```yaml
github-conn:
    host: azure.ai.connection
    uses:
        - ai-project
    category: RemoteTool
    target: https://api.githubcopilot.com/mcp
    authType: CustomKeys
    credentials:
        Authorization: ${GITHUB_PAT}
```

## azure.ai.toolbox service

A toolbox is a named bundle of tools that agents reference. Connection-backed tools name an `azure.ai.connection` service through the `connection` field.

| Field | Description |
| ----- | ----------- |
| `host` | Must be `azure.ai.toolbox`. |
| `description` | Description of the toolbox. |
| `tools` | List of tools. Each entry has a `type` and, for connection-backed tools, a `connection`. |

```yaml
research-tools:
    host: azure.ai.toolbox
    uses:
        - ai-project
        - search-conn
    tools:
        - type: azure_ai_search
          connection: search-conn
        - type: code_interpreter
```

An agent references a toolbox by adding the toolbox service name to both `uses` and its `toolboxes` list.

## azure.ai.skill and azure.ai.routine services

A `azure.ai.skill` service defines a reusable behavioral guideline that agents reference by name. A `azure.ai.routine` service defines a trigger (schedule or event) and an action that invokes an agent. Both depend on the resources they use through `uses`. For details, see [Discover tools in Foundry Tools](tool-catalog.md) and [Use routines](../how-to/use-routines.md).

## Dependencies with uses

The `uses` field declares the services a given service depends on. `azd` uses this graph to order provisioning and to wire references, such as an agent's connections and toolboxes.

```yaml
uses:
    - ai-project
    - search-conn
    - research-tools
```

## File includes with $ref

Any service or list entry can be replaced with a reference to an external YAML or JSON file. Relative paths resolve from the file that contains the `$ref`. Remote URLs aren't supported.

```yaml
services:
    triage:
        host: azure.ai.agent
        uses:
            - ai-project
        $ref: ./agents/triage.yaml
```

File includes let you keep large agent definitions in their own files and share definitions across projects.

## Variable substitution

Two substitution syntaxes can appear in `azure.yaml`:

| Syntax | Resolved when | By what |
| ------ | ------------- | ------- |
| `${VAR_NAME}` | `azd provision` or `azd deploy` | `azd` environment variables from `.azure/<env>/.env`, resolved client-side. |
| `${{ ... }}` | At runtime | Foundry server-side resolution. `azd` passes these through untouched. |

## Infrastructure and deploy modes

### Bicep-less by default

`azd ai agent init` is bicep-less by default: it doesn't write an `infra/` directory, and `azd` synthesizes the infrastructure from your `azure.yaml` services at provision time. To materialize infrastructure-as-code files, eject them:

| Command | Result |
| ------- | ------ |
| `azd ai agent init --infra` | Ejects Bicep into `./infra/`. |
| `azd ai agent init --infra=bicep` | Ejects Bicep (explicit). |
| `azd ai agent init --infra=terraform` | Ejects Terraform and sets `infra.provider: terraform`. |

When `infra` is present in `azure.yaml`, `azd` uses those files instead of synthesizing infrastructure.

### Deploy modes

A hosted agent deploys in one of two modes:

| Mode | How it works | How to select |
| ---- | ------------ | ------------- |
| `code` | `azd` uploads your source as a ZIP and builds it remotely. This is the default for Python and .NET projects. | `azd ai agent init --deploy-mode code` |
| `container` | `azd` builds a Docker image from your `Dockerfile` and deploys it. | `azd ai agent init --deploy-mode container` |

For source deploys, the `codeConfiguration` field on the agent service captures the runtime and entry point. For prebuilt images, set the `image` field on the agent service and skip the Dockerfile build.

## JSON schema validation

Add the schema reference for IDE autocompletion:

```yaml
# yaml-language-server: $schema=https://raw.githubusercontent.com/Azure/azure-dev/main/schemas/v1.0/azure.yaml.json
```

## Related content

* [Author azure.yaml for hosted agents](../how-to/author-azure-yaml.md)
* [Initialize a hosted agent project with the Azure Developer CLI](../how-to/init-agent-project.md)
* [Hosted agent infrastructure with the Azure Developer CLI](cli-infrastructure.md)
* [Hosted agent runtime contract](hosted-agent-contract.md)
* [What are hosted agents?](hosted-agents.md)
