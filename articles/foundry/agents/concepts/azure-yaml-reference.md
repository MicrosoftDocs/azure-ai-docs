---
title: "azure.yaml reference for hosted agents"
description: "Reference for the azd azure.yaml project file in hosted agent projects: services, container config, model deployments, infrastructure, and multi-agent projects."
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

# azure.yaml reference for hosted agents

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

The `azure.yaml` file is the Azure Developer CLI (`azd`) project configuration. For hosted agents, it declares agent services and their deployment settings. This reference describes the `azure.yaml` fields and how they relate to the `agent.yaml` definition.

## How azd uses azure.yaml

The Azure Developer CLI streamlines the developer-to-cloud workflow. It handles two things: provisioning Azure resources, such as Foundry projects, model deployments, and container registries; and deploying your code to those resources. For hosted agents, the `azure.ai.agents` extension adds agent-specific commands such as `azd ai agent init` and `azd ai agent run`.

Every `azd` project has an `azure.yaml` file at its root. For agent projects, this file tells `azd` what to provision and how to build and deploy your agent.

### Environments

An environment is a named configuration, such as `dev`, `staging`, or `prod`, that stores settings for a particular deployment. Each environment tracks the Azure subscription and location, the resource group and resource names, and any custom variables you set. Settings are stored locally in `.azure/<env-name>/.env`. You can have multiple environments for the same project.

### Core commands

| Command | What it does |
| ------- | ------------ |
| `azd provision` | Creates Azure resources, such as the Foundry project, model deployments, and container registry. |
| `azd deploy` | Builds your container, pushes it to Azure, and creates the hosted agent version. |
| `azd up` | Combines `provision` and `deploy` in one command. |
| `azd down` | Deletes all provisioned resources. |
| `azd env set` | Sets an environment variable, for example `azd env set AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4.1`. |

## Minimal example

```yaml
name: my-agent-project

services:
    my-agent:
        project: src/my-agent
        host: azure.ai.agent
        language: docker
```

## Full example

```yaml
# yaml-language-server: $schema=https://raw.githubusercontent.com/Azure/azure-dev/main/schemas/v1.0/azure.yaml.json
requiredVersions:
    extensions:
        azure.ai.agents: '>=0.1.0-preview'

name: my-agent-project

services:
    my-agent:
        project: src/my-agent
        host: azure.ai.agent
        language: docker
        config:
            container:
                resources:
                    cpu: "0.25"
                    memory: 0.5Gi
            deployments:
                - model:
                    format: OpenAI
                    name: gpt-4.1-mini
                    version: "2025-04-14"
                  name: gpt-4.1-mini
                  sku:
                    capacity: 10
                    name: GlobalBatch
            startupCommand: python main.py

infra:
    provider: bicep
    path: ./infra
```

## Top-level fields

| Field | Required | Description |
| ----- | -------- | ----------- |
| `name` | Yes | Project name. |
| `requiredVersions.extensions` | No | Minimum extension version constraint. |
| `services` | Yes | Map of service names to service configurations. |
| `infra` | No | Infrastructure-as-code settings. |

## Service fields

| Field | Required | Description |
| ----- | -------- | ----------- |
| `project` | Yes | Path to the agent source code, the directory that contains `agent.yaml`. |
| `host` | Yes | Must be `azure.ai.agent` for hosted agents. |
| `language` | Yes | Must be `docker` for hosted agents. |

## config fields

| Field | Description |
| ----- | ----------- |
| `config.container.resources.cpu` | CPU allocation, for example `"0.25"`, `"1.0"`, up to `"4.0"`. |
| `config.container.resources.memory` | Memory allocation, for example `0.5Gi`, `1.0Gi`, up to `8.0Gi`. |
| `config.startupCommand` | Command to start the agent, for example `python main.py`. Used by `azd ai agent run` for local development and for container startup. |
| `docker.remoteBuild` | Set to `true` (default) for remote container builds in Azure Container Registry, or `false` for local Docker builds. |

## config.deployments fields

| Field | Description |
| ----- | ----------- |
| `name` | Deployment name. |
| `model.format` | Model format, for example `OpenAI`. |
| `model.name` | Model name, for example `gpt-4.1-mini`. |
| `model.version` | Model version string. |
| `sku.name` | SKU name, for example `GlobalBatch` or `Standard`. |
| `sku.capacity` | SKU capacity units. |

## infra fields

| Field | Description |
| ----- | ----------- |
| `infra.provider` | Infrastructure-as-code provider: `bicep` (default) or `terraform`. |
| `infra.path` | Path to infrastructure files. |

## Remote and local builds

By default, `azd` builds container images remotely in Azure Container Registry, so you don't need Docker Desktop installed locally. The `docker.remoteBuild` flag in `azure.yaml` controls this behavior:

```yaml
services:
    my-agent:
        docker:
            remoteBuild: true  # default; no local Docker required
```

If you set `docker.remoteBuild: false`, `azd` builds images locally and then pushes them to the registry. This requires Docker to be installed and running on your machine. Remote builds are recommended for most workflows.

## Multi-agent projects

You can define multiple agent services in one project:

```yaml
services:
    agent-one:
        project: src/agent-one
        host: azure.ai.agent
        language: docker
        config:
            startupCommand: python main.py

    agent-two:
        project: src/agent-two
        host: azure.ai.agent
        language: docker
        config:
            startupCommand: dotnet run
```

When multiple services exist, specify the agent name in CLI commands:

```bash
azd ai agent run agent-one
azd ai agent invoke agent-one "Hello"
```

## How azure.yaml and agent.yaml relate

These are two different files with different purposes:

* `azure.yaml` lives at the project root and tells `azd` how to provision infrastructure and deploy services.
* `agent.yaml` lives in the agent source directory, such as `src/my-agent/agent.yaml`, and describes the agent itself, including protocols, tools, and environment variables.

During deployment, `azd` reads both files: `azure.yaml` for the infrastructure and build configuration, and `agent.yaml` for the agent definition.

## JSON schema validation

Add the schema reference for IDE autocompletion:

```yaml
# yaml-language-server: $schema=https://raw.githubusercontent.com/Azure/azure-dev/main/schemas/v1.0/azure.yaml.json
```

## Related content

* [agent.yaml schema reference](agent-yaml-reference.md)
* [Hosted agent infrastructure with the Azure Developer CLI](cli-infrastructure.md)
* [What are hosted agents?](hosted-agents.md)
