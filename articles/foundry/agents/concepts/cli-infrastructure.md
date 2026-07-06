---
title: "Hosted agent infrastructure with the Azure Developer CLI"
description: "Understand the Bicep infrastructure that azd scaffolds for a hosted agent project: provisioned resources, project structure, parameters, and customization."
author: aahill
ms.author: aahi
ms.manager: mcleans
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.topic: concept-article
ms.date: 06/15/2026
ms.custom: references_regions, doc-kit-assisted
ai-usage: ai-assisted
---

# Hosted agent infrastructure with the Azure Developer CLI

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

When you run `azd ai agent init`, the Azure Developer CLI (`azd`) scaffolds an `infra/` directory into your project that contains Bicep templates. These templates define all the Azure resources your hosted agent needs. Running `azd provision` deploys the templates to create the infrastructure. This article explains what those templates provision and how to customize them.

## What gets provisioned

The Bicep templates are based on the [azd-ai-starter-basic](https://github.com/Azure-Samples/azd-ai-starter-basic) repository and create the following Azure resources:

| Resource | Purpose |
| -------- | ------- |
| Resource group | Organizes all resources. Named `rg-<agent-name>`. |
| AI Services account | The Microsoft Foundry account. |
| Foundry project | Hosts the agent and AI capabilities. |
| Model deployments | The models the agent uses, for example `gpt-4.1-mini`. |
| Azure Container Registry | Stores the agent container images. |
| Application Insights | Agent performance monitoring and telemetry. |
| Log Analytics workspace | Centralized log collection. |
| Managed identity | The project's system-assigned identity that authenticates the agent identity blueprint to Microsoft Entra ID and holds platform role assignments. |

The templates create more resources conditionally, based on your `agent.yaml` configuration:

* Capability host -- supports hosted agent deployment on the Foundry project. Created when you need custom storage of conversations.
* Grounding with Bing or Grounding with Bing Custom Search -- for the web search tool.
* Azure AI Search -- for search grounding.
* Azure Storage -- for file operations.

## Project structure

```
infra/
|-- main.bicep                 # Main deployment template (subscription-scoped)
|-- main.parameters.json       # Parameter bindings to azd environment variables
|-- abbreviations.json         # Naming convention abbreviations
\-- core/
    |-- ai/                    # Foundry account, project, and connections
    |-- host/                  # Container registry
    |-- monitor/               # Application Insights and Log Analytics
    |-- search/                # Azure AI Search (conditional)
    \-- storage/               # Azure Storage (conditional)
```

## How parameters flow

The `main.parameters.json` file maps `azd` environment variables to Bicep parameters:

```json
{
  "environmentName": { "value": "${AZURE_ENV_NAME}" },
  "location": { "value": "${AZURE_LOCATION}" },
  "aiFoundryResourceName": { "value": "${AZURE_AI_ACCOUNT_NAME}" },
  "aiProjectDeploymentsJson": { "value": "${AI_PROJECT_DEPLOYMENTS=[]}" }
}
```

During `azd provision`, `azd` resolves these `${VAR}` references from the environment (`.azure/<env>/.env`) and passes them to the Bicep deployment. Outputs from the deployment, such as the Foundry project endpoint, model deployment name, and container registry endpoint, are written back to the environment for use by `azd deploy`, `azd ai agent run`, and the `azd ai` resource commands.

## Existing resources

The Bicep templates support connecting to existing Azure resources instead of creating new ones. This is useful when your team already has shared infrastructure.

| Existing resource | Environment variables to set |
| ----------------- | ---------------------------- |
| AI Services account | `AZURE_AI_ACCOUNT_NAME` |
| Container Registry | `AZURE_CONTAINER_REGISTRY_RESOURCE_ID` and `AZURE_CONTAINER_REGISTRY_ENDPOINT` |
| Application Insights | `APPLICATIONINSIGHTS_CONNECTION_STRING` and `APPLICATIONINSIGHTS_RESOURCE_ID` |

Set these variables with `azd env set` before you run `azd provision`.

## Customize the infrastructure

The `infra/` directory is standard `azd` infrastructure, so you have full control over it. To add or change resources:

1. Edit `infra/main.bicep` or add new modules under `infra/core/`.
1. Add new parameters to `main.parameters.json` with `${VAR}` bindings.
1. Set the corresponding `azd` environment variables with `azd env set`.
1. Run `azd provision` to apply the changes.

Changes to the Bicep files persist across deployments.

## Region restrictions

The `main.bicep` template restricts `location` to regions where hosted agents are supported. If you need to deploy to a region that isn't in the allowed list, update the `@allowed` decorator in `main.bicep`.

## Related content

* [azure.yaml reference for hosted agents](azure-yaml-reference.md)
* [Deploy a hosted agent](../how-to/deploy-hosted-agent.md)
* [azd-ai-starter-basic repository](https://github.com/Azure-Samples/azd-ai-starter-basic)
