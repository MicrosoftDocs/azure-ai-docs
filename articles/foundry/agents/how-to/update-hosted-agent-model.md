---
title: "Update the model for a hosted agent"
description: "Change the model deployment used by a Microsoft Foundry hosted agent and redeploy the project with Azure Developer CLI."
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

# Update the model for a hosted agent

Change the AI model your hosted agent uses after initial deployment. Update the model deployment in `azure.yaml`, set the azd environment value that your agent reads at runtime, and redeploy the Microsoft Foundry hosted agent.

## Prerequisites

- An initialized and deployed hosted agent project. For setup, see [Initialize an agent project](init-agent-project.md) and [Deploy a hosted agent](deploy-hosted-agent.md).
- The [azd Foundry extensions installed](install-cli-foundry-extensions.md).
- An authenticated `azd` session.
- A target model deployment name that is available for your Foundry project and region.

## Choose a model

When selecting a model, consider:

| Factor | Guidance |
|--------|----------|
| **Task complexity** | Use larger models for complex reasoning, tool use, and multistep tasks. Use smaller models (for example, `gpt-5.4-mini`) for simpler conversations and lower cost. |
| **Latency** | Smaller models respond faster. If your agent needs quick responses, prefer mini/nano variants. |
| **Cost** | Model pricing varies significantly. Check the Azure AI pricing page for current rates. |
| **Region availability** | Not all models are available in all regions. Verify availability in the Foundry portal before switching. |

## Update the environment variable

There is no dedicated command for updating the model yet. Start by updating the model deployment name in your azd environment:

```bash
azd env set FOUNDRY_MODEL_NAME=gpt-5.4-mini
```

## Update azure.yaml

Model selection for hosted agents is defined in two places in `azure.yaml`:

- The `azure.ai.project` service defines the model deployment in its `deployments` list.
- The `azure.ai.agent` service defines the runtime environment variable that your agent code reads from the `env` map.

Update both entries to use the target deployment name:

```yaml
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
    kind: hosted
    uses:
      - ai-project
    env:
      FOUNDRY_MODEL_NAME: ${FOUNDRY_MODEL_NAME}
```

The model deployment name in the azd environment should match the deployment name in `services.<project-service>.deployments[].name`.

## Redeploy the project

Run `azd up`:

```bash
azd up
```

Use `azd up`, not just `azd deploy`, if the new model deployment needs to be provisioned. If the model deployment already exists in your Foundry project, `azd deploy` is sufficient.

> [!TIP]
> Run `azd env get-values` to see all current environment variables.

## Configure different models per environment

You can configure different models for development and production using azd environments:

```bash
# Development environment
azd env select dev
azd env set FOUNDRY_MODEL_NAME=<development-model-deployment>

# Production environment
azd env select prod
azd env set FOUNDRY_MODEL_NAME=<production-model-deployment>
```

Each environment maintains its own set of variables in `.azure/<env-name>/.env`.

## Related content

- [Azure YAML reference](../concepts/azure-yaml-reference.md) for deployment configuration details.
- [Deploy a hosted agent](deploy-hosted-agent.md) to understand how deployment works.
