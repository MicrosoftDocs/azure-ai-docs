---
title: "Configure environment variables for a hosted agent"
description: "Define Microsoft Foundry hosted agent environment variables in azure.yaml and azd environments without baking settings into images."
author: aahill
ms.author: aahi
ms.manager: mcleans
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.topic: how-to
ms.date: 07/21/2026
ms.custom: dev-focus, doc-kit-assisted
ai-usage: ai-assisted
---

# Configure environment variables for a hosted agent

Configure environment variables for your hosted agent by defining where values belong in `azure.yaml`, what the Microsoft Foundry platform provides automatically, and how azd environment integration works. You also learn how to add custom variables and handle local development secrets.

> [!NOTE]
> Agent manifests (`agent.manifest.yaml`) and standalone agent definitions (`agent.yaml`) are deprecated. As of the Foundry `azd` extensions (`azure.ai.agents` 1.0.0-beta.1), all hosted agent configuration lives in a single `azure.yaml`. See [Author azure.yaml for hosted agents](author-azure-yaml.md).

## Prerequisites

- An initialized hosted agent project with an `azure.yaml` file. To create or update a project, see [Author azure.yaml for hosted agents](author-azure-yaml.md).
- The azd Foundry extensions installed. For installation steps, see [Install the azd Foundry extensions](install-cli-foundry-extensions.md).
- An authenticated Azure Developer CLI session. Run `azd auth login` if needed.
- An active azd environment. Select or create one with `azd env select` or `azd env new`.

## Define environment variables in azure.yaml

Define environment variables in the `env` map of the `azure.ai.agent` service in your project `azure.yaml`, not in your Dockerfile. This approach keeps your container image portable and lets you change configuration without rebuilding.

```yaml
services:
  my-agent:
    host: azure.ai.agent
    project: src/my-agent
    kind: hosted
    env:
      AZURE_AI_MODEL_DEPLOYMENT_NAME: ${AZURE_AI_MODEL_DEPLOYMENT_NAME}
      MY_CUSTOM_VAR: ${MY_CUSTOM_VAR}
```

Use the `${VAR_NAME}` syntax to reference azd environment variables. The platform resolves these variables at deploy time from `.azure/<env>/.env`.

> [!NOTE]
> **Why not the Dockerfile?** Values baked into a Dockerfile are fixed at image build time and visible to anyone with access to the image. Using `azure.yaml` lets you change values per environment and keeps secrets out of the image layer.

> [!IMPORTANT]
> **Don't declare `FOUNDRY_PROJECT_ENDPOINT` in the `azure.yaml` `env` map.** The platform injects it automatically into hosted containers, and `azd ai agent run` sets it for local development from the active azd env. Declaring it explicitly is redundant and risks shadowing the platform-managed value.

## Set azd environment variables

1. Add or change a variable in your current azd environment:

   ```bash
   azd env set MY_CUSTOM_VAR=my-value
   ```

1. View all current values:

   ```bash
   azd env get-values
   ```

   These values are stored in `.azure/<env-name>/.env` and resolved into your `azure.yaml` at deploy time.

## Review platform environment variables

The Foundry platform automatically injects the following environment variables into every hosted agent container at startup. These variables are read-only. Your agent code should consume them but never override them.

### Foundry variables

| Variable | Description |
|----------|-------------|
| `FOUNDRY_HOSTING_ENVIRONMENT` | The platform injects a non-empty value when hosting in Foundry. Check for this variable to determine if the container is running in a Foundry context. |
| `FOUNDRY_AGENT_NAME` | The agent's name, such as `my-weather-agent`. |
| `FOUNDRY_AGENT_ID` | The ID of the agent. |
| `FOUNDRY_AGENT_VERSION` | The agent's version. |
| `FOUNDRY_PROJECT_ENDPOINT` | Foundry project endpoint, such as `https://{account}.services.ai.azure.com/api/projects/{project}`. |
| `FOUNDRY_AGENT_SESSION_ID` | The agent's session ID. |
| `FOUNDRY_PROJECT_ARM_ID` | The project's full ARM resource ID. |

> [!NOTE]
> **Reserved prefix:** The platform reserves all `AGENT_*` and `FOUNDRY_*` environment variables for platform use and automatically injects them into the container.

During local development with `azd ai agent run`, azd sets `FOUNDRY_PROJECT_ENDPOINT` automatically from your azd environment so your agent code works the same locally and when deployed.

### Network variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | `8088` | HTTP listen port. Set only when the platform requires a non-default port. |
| `SSE_KEEPALIVE_INTERVAL` | Disabled | SSE keep-alive comment interval in seconds. |

### Observability variables

| Variable | Description |
|----------|-------------|
| `APPLICATIONINSIGHTS_CONNECTION_STRING` | Azure Monitor connection string for telemetry export. |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | OTLP collector endpoint for OpenTelemetry. |

### Session file variables

| Variable | Default | Description |
|----------|---------|-------------|
| `HOME` | `/home/session` | Filesystem path to persisted session data. |

## Add a new environment variable

1. Define the variable in the `env` map for the `azure.ai.agent` service in `azure.yaml`.

   ```yaml
   services:
     my-agent:
       host: azure.ai.agent
       environmentVariables:
         MY_API_URL: ${MY_API_URL}
   ```

1. Set the value in your azd environment.

   ```bash
   azd env set MY_API_URL=https://api.example.com
   ```

1. Redeploy the application.

   ```bash
   azd deploy
   ```

For local development, `azd ai agent run` also resolves `${VAR}` from the azd environment, so the same setup works locally.

## Handle sensitive values

For secrets such as API keys and tokens, don't bake values into your image or commit them to `azure.yaml`. Store secrets in a Foundry project connection, and reference connection values from your configuration when the platform supports that connection type.

### Use secrets during local development

For local runs with `azd ai agent run`, set values as `azd` environment variables and reference them in `azure.yaml`. `azd` stores environment values in `.azure/<env>/.env`, which is gitignored by default, so they stay out of source control.

```bash
azd env set OPENAI_KEY <value>
```

```yaml
services:
  my-agent:
    host: azure.ai.agent
    env:
      OPENAI_KEY: ${OPENAI_KEY}
```

For secrets that shouldn't live in a local `.env` file, store them in a Foundry project connection and reference them with a `${{connections.<name>.credentials.<field>}}` placeholder. The platform resolves the placeholder at runtime. See [Run a hosted agent locally with the Azure Developer CLI](run-hosted-agent-locally.md) for the local run workflow.

## Related content

- [Author azure.yaml for hosted agents](author-azure-yaml.md) to configure hosted agent services.
- [Azure YAML reference](../concepts/azure-yaml-reference.md) for azd environments and `azd env set`.
- [Deploy a hosted agent](deploy-hosted-agent.md) to redeploy after configuration changes.
