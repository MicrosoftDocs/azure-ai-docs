---
title: "azure.yaml reference for hosted agents"
description: "Reference for the unified azd azure.yaml project file for hosted agents: services, host types, model deployments, agent configuration, dependencies, file includes, and infrastructure."
author: aahill
ms.author: aahi
ms.manager: mcleans
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.topic: reference
ms.date: 07/23/2026
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
| `azd deploy` | Packages and uploads source for a remote build, builds and publishes a container image, or deploys a prebuilt image, then creates the hosted agent version. |
| `azd up` | Combines `provision` and `deploy` in one command. |
| `azd down` | Deletes all provisioned resources. |
| `azd env set` | Sets an environment variable, for example `azd env set MICROSOFT_FOUNDRY_MODEL_DEPLOYMENT_NAME=gpt-5.4-mini`. |

## Extension compatibility

The `azure.ai.agents` extension provides the `azure.ai.agent` host. The
`azure.ai.projects` extension provides the `azure.ai.project` host and the
`microsoft.foundry` infrastructure provider. Use `azure.ai.agents` version
`1.0.0-beta.8` or later with `azure.ai.projects` version `1.0.0-beta.4` or
later. For installation and upgrade instructions, see [Install the Azure
Developer CLI Foundry extensions](../how-to/install-cli-foundry-extensions.md).

You can declare the minimum compatible versions in `azure.yaml`:

```yaml
requiredVersions:
    azd: ">=1.27.1"
    extensions:
        azure.ai.agents: ">=1.0.0-beta.8"
        azure.ai.projects: ">=1.0.0-beta.4"
```

### Service provider lifecycle

Install the `microsoft.foundry` meta-package when your project includes
connections, toolboxes, skills, or routines. It installs the provider
extensions that implement the corresponding `azure.ai.*` hosts.

| Service host | Provider extension | Applied during |
| --- | --- | --- |
| `azure.ai.project` | `azure.ai.projects` | `azd provision` |
| `azure.ai.connection` | `azure.ai.connections` | `azd provision` |
| `azure.ai.toolbox` | `azure.ai.toolboxes` | `azd deploy` |
| `azure.ai.agent` | `azure.ai.agents` | `azd deploy` |
| `azure.ai.skill` | `azure.ai.skills` | `azd deploy` |
| `azure.ai.routine` | `azure.ai.routines` | `azd deploy` |

The project and connection providers apply their configuration during
`azd provision`. The agent, toolbox, skill, and routine providers apply their
configuration during `azd deploy`. Run `azd up` to complete both phases.
Removing a data-plane service from `azure.yaml` stops `azd` from managing it;
delete the remote resource separately when you no longer need it.
* `azd down` - Deletes the resource group when the current environment created the Foundry project. Leaves an existing project and its resources in place. |
* `azd env set` - Sets an environment variable, for example `azd env set FOUNDRY_MODEL_NAME=gpt-5.4-mini`. |

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
            MICROSOFT_FOUNDRY_MODEL_DEPLOYMENT_NAME: ${MICROSOFT_FOUNDRY_MODEL_DEPLOYMENT_NAME}
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

#### Private-network configuration

Use `network` on the `azure.ai.project` service to configure the account
private endpoint and agent egress. The following example uses a customer-managed
subnet for the agent runtime:

```yaml
services:
    ai-project:
        host: azure.ai.project
        network:
            peSubnet:
                vnet: ${VNET_RESOURCE_ID}
                name: private-endpoint-subnet
            agentSubnet:
                vnet: ${VNET_RESOURCE_ID}
                name: agent-subnet
            dns:
                resourceGroup: ${PRIVATE_DNS_RESOURCE_GROUP}
                subscription: ${PRIVATE_DNS_SUBSCRIPTION_ID}
```

| Field | Required | Description |
| --- | --- | --- |
| `peSubnet` | Yes | The subnet for the Foundry account private endpoint. It requires `vnet` and `name`. Add `prefix` when `azd` should create the subnet. |
| `agentSubnet` | No | A customer-managed subnet for hosted-agent egress. It requires `vnet` and `name`, and must be a different subnet in the same virtual network as `peSubnet`. |
| `isolationMode` | No | The outbound posture for Microsoft-managed egress. Use it only when you omit `agentSubnet`. Valid values are `AllowInternetOutbound` and `AllowOnlyApprovedOutbound`. |
| `dns.resourceGroup` | No | The resource group that contains existing private DNS zones. Omit it to let `azd` create and link the required zones. |
| `dns.subscription` | No | The subscription that contains existing private DNS zones. It defaults to the deployment subscription. |

Private networking disables public data-plane access for the account. An
automatically created Azure Container Registry isn't supported with this
configuration. Use source-code deployment or specify a prebuilt `image`.

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
| `agentCard` | Agent-level discovery metadata, including `skills`. |

### `agentCard.skills` and `azure.ai.skill`

`agentCard.skills` describes an agent's capabilities in its discovery card.
It provides metadata for clients and doesn't create or attach a reusable
Foundry skill. Each card skill requires an `id`, `name`, and `description`.

An `azure.ai.skill` service creates a versioned skill from instructions and
optional allowed tools. Declare it separately under `services`; its `uses`
list controls dependency order, but it doesn't populate `agentCard.skills` or
attach the skill to an agent. Use `agentCard.skills` for discovery metadata and
`azure.ai.skill` for reusable instructions.

```yaml
agentCard:
    description: Research agent discovery card.
    skills:
        - id: research
          name: Research
          description: Researches a requested subject.
```

```yaml
services:
    code-review:
        host: azure.ai.skill
        uses:
            - ai-project
        instructions: ./skills/code-review.md
```

#### Complete a discovery card

Add `version`, `tags`, and `examples` when clients need richer discovery
metadata. A card requires a `description` and at least one skill. Each skill
requires an `id`, `name`, and `description`.

```yaml
agentCard:
    description: Research agent discovery card.
    version: "1.0"
    skills:
        - id: research
          name: Research
          description: Researches a requested subject.
          tags:
              - research
          examples:
              - Research current product guidance.
```

### Responsible AI policies

Use `policies` to associate a Responsible AI policy with the hosted agent.
Set `raiPolicyName` to the full ARM resource ID of the policy:

```yaml
policies:
    - type: rai_policy
      raiPolicyName: ${RAI_POLICY_RESOURCE_ID}
```

The `rai_policy` type and `raiPolicyName` are required. The extension applies
the first valid policy in the list to the hosted-agent Responsible AI
configuration. For policy creation and management guidance, see [Add guardrails
to hosted agents](../how-to/add-hosted-agent-guardrails.md).

### Memory stores

Use `memoryStores` to create or reuse Foundry memory stores before deployment.
Each store requires existing chat-model and embedding-model deployment names.

```yaml
memoryStores:
    - name: customer-memory
      description: Stores durable customer context.
      chatModel: gpt-5.4-mini
      embeddingModel: text-embedding-3-large
      options:
          chatSummaryEnabled: true
          userProfileEnabled: true
          proceduralMemoryEnabled: false
          defaultTtlSeconds: 0
```

| Field | Required | Description |
| --- | --- | --- |
| `name` | Yes | The memory-store name. |
| `description` | No | A description of the memory store. |
| `chatModel` | Yes | The chat-model deployment used to process memory content. |
| `embeddingModel` | Yes | The embedding-model deployment used to process memory content. |
| `options.chatSummaryEnabled` | No | Enables chat-summary memory. |
| `options.userProfileEnabled` | No | Enables user-profile memory. |
| `options.proceduralMemoryEnabled` | No | Enables procedural memory. |
| `options.defaultTtlSeconds` | No | Sets the default retention period in seconds. Set `0` for no expiration. |
| `options.userProfileDetails` | No | Provides guidance about the profile data to retain. |

Existing stores aren't updated during deployment. If the declared definition
differs from the existing store, `azd` reports the difference. Declaring a
memory store doesn't change your agent code or automatically attach a memory
tool. Connect your application to the memory store by using the memory search
tool or memory store APIs. For details, see [Use memory with agents](../how-to/memory-usage.md).

### Configure an agent endpoint

Use `agentEndpoint` to configure the protocols and authorization schemes
published by the agent endpoint. Use an agent card with an A2A endpoint so
other agents can discover the capabilities you expose.

```yaml
agentEndpoint:
    protocols:
        - responses
        - a2a
    authorizationSchemes:
        - type: Entra
```

You can also define `versionSelector.versionSelectionRules` when you need to
control which agent version receives endpoint traffic. Agent Service validates
endpoint protocol and authorization values during deployment.

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

#### Additional runtime protocols and Activity endpoints

In addition to `responses`, `invocations`, and `a2a`, hosted agents support
`invocations_ws` for WebSocket invocations and `activity` for Microsoft 365 and
Teams activity scenarios.

```yaml
protocols:
    - protocol: invocations_ws
      version: 2.0.0
    - protocol: activity
      version: 2.0.0
```

For an Activity agent, add `activity` to the public endpoint configuration and
use the required Bot Service authorization scheme:

```yaml
agentEndpoint:
    protocols:
        - activity
    authorizationSchemes:
        - type: BotServiceRbac
```

The Activity protocol can coexist with other protocols on the same agent
endpoint. For runtime protocol behavior, see [What are hosted agents?](hosted-agents.md).

### env

```yaml
env:
    MICROSOFT_FOUNDRY_MODEL_DEPLOYMENT_NAME: ${MICROSOFT_FOUNDRY_MODEL_DEPLOYMENT_NAME}
    LOG_LEVEL: info
```

The `${ }` syntax references `azd` environment variables from `.azure/<env>/.env`.

> [!NOTE]
> Don't declare `FOUNDRY_PROJECT_ENDPOINT` in `env`. The platform injects it automatically into hosted containers, and `azd ai agent run` sets it for local development. Declaring it here is redundant and risks shadowing the platform value.

#### Platform environment, identity, and endpoints

The platform reserves the `FOUNDRY_` and `AGENT_` prefixes. Read platform
variables, such as `FOUNDRY_PROJECT_ENDPOINT`, from your application code, but
don't define or override them in `env`. Agent-defined environment values are
strings.

Each deployed hosted agent receives a dedicated Microsoft Entra ID agent
identity and endpoint. Don't add an `identity` block to the agent service.
The agent identity can use the project endpoint and session storage by default.
Assign the identity additional roles when the agent needs to access external
resources. For details, see [Hosted agent permissions reference](hosted-agent-permissions.md).

The protocols you declare determine the endpoints that are active after
deployment. Run `azd ai agent show` to inspect the deployed agent and its
endpoint URLs.

After deployment, `azd` writes the following values to the active environment,
using the normalized service name in place of `<SERVICE>`:

* `AGENT_<SERVICE>_NAME`
* `AGENT_<SERVICE>_VERSION`
* `AGENT_<SERVICE>_ENDPOINT`
* `AGENT_<SERVICE>_<PROTOCOL>_ENDPOINT` for enabled `responses`,
  `invocations`, and `invocations_ws` protocols

Use the protocol-specific output when your application or automation needs an
invocation URL. The base endpoint identifies the deployed agent version for
session-management operations.

### container

```yaml
container:
    resources:
        cpu: "0.25"
        memory: 0.5Gi
```

Set `cpu` from `"0.25"` up to `"4.0"`, and `memory` from `0.5Gi` up to `8.0Gi`.

### Source-code deployment

Set `codeConfiguration` to deploy source code as a ZIP instead of a container
image. Specify one entry-point filename or assembly name. `azd` combines it
with the selected runtime when it creates the hosted-agent version.

```yaml
codeConfiguration:
    runtime: python_3_13
    entryPoint: main.py
    dependencyResolution: remote_build
```

Use `remote_build` to restore dependencies from the project sources, or use
`bundled` when the ZIP contains Linux-compatible dependencies. Don't combine
`codeConfiguration` with image-based container configuration. For packaging and
dependency guidance, see [Deploy a hosted agent from source code](../how-to/deploy-hosted-agent-code.md).

### Container builds and prebuilt images

Use a `Dockerfile` under `project` to build a container image, or set `image`
to deploy a prebuilt image:

```yaml
image: myregistry.azurecr.io/agents/researcher:1.2.3
```

When a `Dockerfile` and an `image` are both available, choose the prebuilt image
in the interactive deployment prompt. For unattended deployment, set
`AZD_AGENT_SKIP_ACR` to `true` in the active `azd` environment to select the
configured image. For registry permissions and private registry deployment,
see [Deploy a hosted agent with a private Azure Container Registry](../how-to/deploy-hosted-agent-private-azure-container-registry.md).

### Metadata and schema limitations

Use string values for deployed agent metadata. The `authors` metadata value can
be a list of strings. Don't rely on `displayName`, `inputSchema`, or
`outputSchema` to configure the deployed hosted agent; the unified
configuration accepts these fields, but the hosted-agent create request doesn't
use them.

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

Connection changes apply during `azd provision`, not `azd deploy`. Store
credential values in your `azd` environment and reference them with `${VAR}`
instead of putting secrets in `azure.yaml`.

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

### Consume a toolbox endpoint

In a split-service project, `uses` controls deployment order. Your application
connects to the toolbox's MCP endpoint at runtime. Pass the toolbox name or
endpoint to your application through `env`, then construct the consumer endpoint
from `FOUNDRY_PROJECT_ENDPOINT` in your agent code. For an end-to-end example,
see [Use a toolbox with a hosted agent](../how-to/tools/use-toolbox-hosted-agent.md).

## azure.ai.skill and azure.ai.routine services

A `azure.ai.skill` service defines a reusable behavioral guideline that agents reference by name. A `azure.ai.routine` service defines a trigger (schedule or event) and an action that invokes an agent. Both depend on the resources they use through `uses`. For details, see [Discover tools in Foundry Tools](tool-catalog.md) and [Use routines](../how-to/use-routines.md).

Skills and routines are separate resources. Declaring either service controls
its lifecycle but doesn't automatically attach a skill to the agent or infer a
routine action target. Configure the consuming application or routine action
explicitly.

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

Keep core service fields in the root `azure.yaml` entry when you use a service
`$ref`: `host`, `uses`, `project`, `language`, `image`, and `docker`. Put
provider-owned definition fields, such as `kind`, `name`, `description`, and
`protocols`, in the referenced mapping. `$ref` resolves local YAML or JSON
files recursively; URLs and reference cycles aren't supported.

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

## Legacy configuration migration

Older agent definitions can nest environment variables under `config: env`.
In the unified `azure.yaml`, move the `env` mapping to the agent service:

```yaml
# Legacy
services:
    my-agent:
        host: azure.ai.agent
        config:
            env:
                MICROSOFT_FOUNDRY_MODEL_DEPLOYMENT_NAME: ${MICROSOFT_FOUNDRY_MODEL_DEPLOYMENT_NAME}
```

```yaml
# Unified azure.yaml
services:
    my-agent:
        host: azure.ai.agent
        env:
            MICROSOFT_FOUNDRY_MODEL_DEPLOYMENT_NAME: ${MICROSOFT_FOUNDRY_MODEL_DEPLOYMENT_NAME}
```

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
