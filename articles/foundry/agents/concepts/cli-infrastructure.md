---
title: "Hosted agent infrastructure with the Azure Developer CLI"
description: "Understand the optional Bicep or Terraform infrastructure that azd can scaffold for a hosted agent project, including provisioning, parameters, and outputs."
author: aahill
ms.author: aahi
ms.manager: mcleans
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.topic: concept-article
ms.date: 09/16/2026
ms.custom: references_regions, doc-kit-assisted
ai-usage: ai-assisted
---

# Hosted agent infrastructure with the Azure Developer CLI

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

The Azure Developer CLI (`azd`) can generate Bicep or Terraform infrastructure from the services declared in `azure.yaml`. Choose Terraform with `azd ai agent init --infra=terraform`, or Bicep with `--infra=bicep`. Running `azd provision` applies the selected infrastructure.

Infrastructure provisioning and agent deployment are separate. Terraform or Bicep manages supporting Azure resources; `azd deploy` creates the hosted-agent data-plane version. To manage the agent itself with Terraform instead of azd, see [Deploy a hosted agent with Terraform](../how-to/deploy-hosted-agent-terraform.md).

## What gets provisioned

By default, `azd ai agent init` doesn't create infrastructure-as-code files. Use `--infra` or `--infra=bicep` to add Bicep infrastructure. Use `--infra=terraform` to add Terraform infrastructure and set `infra.provider: terraform`.

When you add Bicep infrastructure, the templates are based on the [azd-ai-starter-basic](https://github.com/Azure-Samples/azd-ai-starter-basic) repository and create the following Azure resources:

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

The templates create more resources conditionally, based on the services and dependencies declared in `azure.yaml`:

* Agent capability settings -- declare the Azure resources that hold agent state, vector data, and files. Set them when you need agents to use storage you own.
* Grounding with Bing or Grounding with Bing Custom Search -- for the web search tool.
* Azure AI Search -- for search grounding.
* Azure Storage -- for file operations.

## Project structure

For Bicep, a generated project has the following structure:

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

For Bicep, the `main.parameters.json` file maps `azd` environment variables to parameters:

```json
{
  "environmentName": { "value": "${AZURE_ENV_NAME}" },
  "location": { "value": "${AZURE_LOCATION}" },
  "aiFoundryResourceName": { "value": "${AZURE_AI_ACCOUNT_NAME}" },
  "aiProjectDeploymentsJson": { "value": "${AI_PROJECT_DEPLOYMENTS=[]}" }
}
```

During `azd provision`, `azd` resolves these `${VAR}` references from the environment (`.azure/<env>/.env`) and passes them to the Bicep deployment. Outputs from the deployment, such as the Foundry project endpoint, model deployment name, and container registry endpoint, are written back to the environment for use by `azd deploy`, `azd ai agent run`, and the `azd ai` resource commands.

## Terraform infrastructure

For a new project, `azd ai agent init --infra=terraform` generates files such as the following:

```text
infra/
|-- main.tf
|-- provider.tf
|-- variables.tf
|-- outputs.tf
|-- main.tfvars.json
\-- .azd-foundry
```

Container-based services can also generate `container-registry.tf`. Existing projects can retain their infrastructure and receive a separate Foundry layer under `infra/foundry/`. Use the actual generated layout rather than moving files between layers.

The Terraform configuration provisions the Foundry account, project, model deployments, and related resources required by the selected services. Container registry creation depends on the deployment mode and image configuration.

`main.tfvars.json` binds infrastructure inputs to azd environment values. `outputs.tf` exposes values such as the Foundry project endpoint to azd after provisioning. These bindings are part of the azd workflow; don't assume a generated parameter file works unchanged with a standalone `terraform apply`.

To customize Terraform infrastructure, edit the generated `.tf` files, preserve the outputs needed by your agent services, and run `azd provision`. Review the Terraform plan before applying infrastructure changes.

### Terraform state and CI/CD

The generated files don't bootstrap a remote-state backend. For team deployments, configure Azure Storage-backed state, separate state keys for each environment, and the required backend permissions before configuring CI/CD.

See [Set up CI/CD with Terraform](../how-to/set-up-ci-cd-cli.md#configure-terraform-state) for the deployment flow and [Use Terraform with azd](/azure/developer/azure-developer-cli/use-terraform-for-azd#enable-remote-state) for backend configuration.

### Terraform ejection limitations

The Terraform ejection path doesn't support service `network:` configuration in the current Foundry agents extension. Review existing-resource constraints before ejecting a project that already has infrastructure. Ejection isn't a general Bicep-to-Terraform state migration, and deleting production resources isn't a prerequisite for adopting Terraform.

## Existing resources

The Bicep templates support connecting to existing Azure resources instead of creating new ones. This is useful when your team already has shared infrastructure.

| Existing resource | Environment variables to set |
| ----------------- | ---------------------------- |
| AI Services account | `AZURE_AI_ACCOUNT_NAME` |
| Container Registry | `AZURE_CONTAINER_REGISTRY_RESOURCE_ID` and `AZURE_CONTAINER_REGISTRY_ENDPOINT` |
| Application Insights | `APPLICATIONINSIGHTS_CONNECTION_STRING` and `APPLICATIONINSIGHTS_RESOURCE_ID` |

Set these variables with `azd env set` before you run `azd provision`.

## Customize the infrastructure

The `infra/` directory is standard `azd` infrastructure. To add or change Bicep resources:

1. Edit `infra/main.bicep` or add new modules under `infra/core/`.
1. Add new parameters to `main.parameters.json` with `${VAR}` bindings.
1. Set the corresponding `azd` environment variables with `azd env set`.
1. Run `azd provision` to apply the changes.

Changes to the Bicep files persist across deployments.

## Region restrictions

The `main.bicep` template restricts `location` to regions where hosted agents are supported. If you need to deploy to a region that isn't in the allowed list, update the `@allowed` decorator in `main.bicep`.

## Related content

* [azure.yaml reference for hosted agents](azure-yaml-reference.md)
* [Set up CI/CD for hosted agents](../how-to/set-up-ci-cd-cli.md)
* [azd-ai-starter-basic repository](https://github.com/Azure-Samples/azd-ai-starter-basic)
