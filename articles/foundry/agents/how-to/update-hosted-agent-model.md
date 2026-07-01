---
title: "Update the model for a hosted agent"
description: "Change the model deployment used by a Microsoft Foundry hosted agent and redeploy the project with Azure Developer CLI."
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

# Update the model for a hosted agent

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

Change the AI model your hosted agent uses after initial deployment. You update the azd environment, adjust the relevant YAML files, and redeploy the Microsoft Foundry hosted agent.

## Prerequisites

- An initialized and deployed hosted agent project. For setup, see [Initialize an agent project](init-agent-project.md) and [Deploy a hosted agent](deploy-hosted-agent.md).
- The [azd Foundry extensions installed](install-cli-foundry-extensions.md).
- An authenticated `azd` session.
- A target model deployment name that is available for your Foundry project and region.

## Choose a model

When selecting a model, consider:

| Factor | Guidance |
|--------|----------|
| **Task complexity** | Use larger models (for example, `gpt-4.1`) for complex reasoning, tool use, and multi-step tasks. Use smaller models (for example, `gpt-4.1-mini`) for simpler conversations and lower cost. |
| **Latency** | Smaller models respond faster. If your agent needs quick responses, prefer mini/nano variants. |
| **Cost** | Model pricing varies significantly. Check the Azure AI pricing page for current rates. |
| **Region availability** | Not all models are available in all regions. Verify availability in the Foundry portal before switching. |

## Update the environment variable

There is no dedicated command for updating the model yet. Start by updating the model deployment name in your azd environment:

```bash
azd env set AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4.1
```

## Update agent YAML

Update the YAML file that defines your agent.

### Update `agent.yaml`

If your project has an `agent.yaml` definition, update the environment variable reference to match:

```yaml
environment_variables:
  - name: AZURE_AI_MODEL_DEPLOYMENT_NAME
    value: ${AZURE_AI_MODEL_DEPLOYMENT_NAME}
```

The model `resources` section in a definition doesn't need to change. The environment variable controls which deployment is used at runtime.

### Update `agent.manifest.yaml`

If your project has an `agent.manifest.yaml` manifest, update both the `resources` section and the environment variable template:

```yaml
resources:
  - kind: model
    name: chat
    id: gpt-4.1

template:
  environment_variables:
    - name: AZURE_AI_MODEL_DEPLOYMENT_NAME
      value: ${AZURE_AI_MODEL_DEPLOYMENT_NAME}
```

## Update Azure YAML

If your `azure.yaml` includes model deployment configuration, it will if you initialized with a manifest that declared a model resource. Update the `config.deployments` section:

```yaml
config:
    deployments:
        - model:
            format: OpenAI
            name: gpt-4.1
            version: "2025-04-14"
          name: gpt-4.1
          sku:
            capacity: 10
            name: GlobalBatch
```

## Redeploy the project

Run `azd up`:

```bash
azd up
```

Use `azd up`, not just `azd deploy`, if the new model needs to be provisioned. If the model deployment already exists in your Foundry project, `azd deploy` is sufficient.

> [!TIP]
> Run `azd env get-values` to see all current environment variables.

## Configure different models per environment

You can configure different models for development and production using azd environments:

```bash
# Development environment -- use a cheaper model
azd env select dev
azd env set AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4.1-mini

# Production environment -- use a more capable model
azd env select prod
azd env set AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4.1
```

Each environment maintains its own set of variables in `.azure/<env-name>/.env`.

## Related content

- [Azure YAML reference](../concepts/azure-yaml-reference.md) for deployment configuration details.
- [Deploy a hosted agent](deploy-hosted-agent.md) to understand how deployment works.
