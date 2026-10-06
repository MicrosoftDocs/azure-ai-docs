---
title: "Set up CI/CD for hosted agents with the Azure Developer CLI"
description: "Configure hosted-agent CI/CD with azd, choose Terraform or Bicep infrastructure, and manage remote state, deployment checks, and production version selection."
author: aahill
ms.author: aahi
ms.manager: mcleans
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.topic: how-to
ms.date: 09/23/2026
ms.custom: dev-focus, doc-kit-assisted
ai-usage: ai-assisted
---

# Set up CI/CD for hosted agents with the Azure Developer CLI

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

Automate your hosted agent deployment with `azd pipeline config`. In this article, you set up continuous integration and delivery in GitHub Actions or Azure DevOps, then apply pipeline-friendly `azd ai` flags for unattended jobs.

Choose Terraform or Bicep for infrastructure provisioning. If you want Terraform to manage the hosted-agent data-plane resource without azd, use [Deploy a hosted agent with Terraform](deploy-hosted-agent-terraform.md) instead.

## Prerequisites

- An initialized hosted agent project that works locally with `azd ai agent run` and `azd ai agent invoke --local`. For setup, see [Initialize an agent project](init-agent-project.md).
- A project that you've successfully deployed at least once with `azd up`. For deployment steps, see [Deploy a hosted agent](deploy-hosted-agent.md).
- The [azd Foundry extensions installed](install-cli-foundry-extensions.md) locally and in your pipeline runner.
- An authenticated `azd` session.
- Your code in a Git repository hosted in GitHub or Azure DevOps.

## Choose the infrastructure provider

To use Terraform instead of Bicep, initialize your project with:

```bash
azd ai agent init --infra=terraform
```

For a container-based agent, specify the deployment mode independently:

```bash
azd ai agent init --infra=terraform --deploy-mode container
```

The infrastructure option doesn't change the default code-deployment mode for Python and .NET projects. For Bicep, use `--infra=bicep` or `--infra`. Without `--infra`, azd synthesizes infrastructure from `azure.yaml` instead of writing IaC files.

For a new project, review the generated `infra/` directory and Terraform provider configuration in `azure.yaml`. Existing projects can use a separate Foundry infrastructure layer. See [Hosted agent infrastructure](../concepts/cli-infrastructure.md#terraform-infrastructure) for file structure and ejection limitations.

Commit the infrastructure configuration and provider lockfile with your application code. Don't commit Terraform state, `.terraform/`, saved plans, or `.azure/` environment state. Initialization is a project-authoring step, not a command to rerun on every CI deployment.

## Configure Terraform state

Skip this section if you aren't using Terraform.

Before configuring the pipeline:

1. Install [Terraform](/azure/developer/terraform/quickstart-configure) locally and on the runner. Use the same reviewed version in development and CI.
1. Create an Azure Storage account and blob container for remote state outside the workload deployment. Use a different state key for each environment.
1. Add an `azurerm` backend declaration to the existing `terraform` block in your Terraform provider file. Keep the generated provider and Terraform version constraints:

   ```terraform
   terraform {
     backend "azurerm" {}
   }
   ```

1. Create `provider.conf.json` in the Terraform infrastructure directory. For a new project using the default layout, the path is `infra/provider.conf.json`:

   ```json
   {
     "storage_account_name": "${RS_STORAGE_ACCOUNT}",
     "container_name": "${RS_CONTAINER_NAME}",
     "key": "hosted-agent-ci/${AZURE_ENV_NAME}.tfstate",
     "resource_group_name": "${RS_RESOURCE_GROUP}",
     "use_azuread_auth": true
   }
   ```

   Choose a key prefix unique to your application if multiple applications share the container. azd resolves these environment substitutions and passes the configuration to `terraform init`; they aren't Terraform input variables.

   This example deliberately enables Microsoft Entra authentication for Blob access with `use_azuread_auth`. OIDC authentication alone doesn't select that backend mode. Without it, a backend can require permission to retrieve a storage account key. For more information, see [Enable remote state](/azure/developer/azure-developer-cli/use-terraform-for-azd#enable-remote-state).
1. Set the backend values in your azd environment:

   ```bash
   azd env set RS_RESOURCE_GROUP "<state-resource-group>"
   azd env set RS_STORAGE_ACCOUNT "<state-storage-account>"
   azd env set RS_CONTAINER_NAME "<state-container>"
   ```

1. Grant the pipeline identity Blob data-plane access to the backend, separately from its infrastructure and Foundry permissions. Review the backend's role and network requirements in [Store Terraform state in Azure Storage](/azure/developer/terraform/store-state-in-azure-storage).
1. Confirm that `azd provision` uses the remote backend before configuring the pipeline.

State and saved plans can contain sensitive values. Restrict access to both, and don't upload them as unrestricted workflow artifacts.

Backend locking protects Terraform state operations. It doesn't coordinate other tools updating the same hosted agent. Serialize production releases across azd, Terraform, and any other deployment writers.

## Configure the pipeline

Run the pipeline configuration command:

```bash
azd pipeline config
```

This interactive command:

1. Detects your Git provider, such as GitHub or Azure DevOps.
1. Creates a service principal for CI/CD authentication.
1. Configures repository secrets and variables with your azd environment values.
1. Generates a workflow file, such as `.github/workflows/azure-dev.yml` for GitHub Actions, or an Azure Pipelines YAML file.

For Terraform projects on GitHub, the command checks that the three `RS_*` values are present and copies them to repository variables. That check doesn't verify storage existence, permissions, or connectivity.

## Review the pipeline flow

The generated pipeline runs on push to `main` by default and executes:

1. **`azd provision`** -- creates or updates Azure infrastructure using the provider configured in `azure.yaml`, including ejected Terraform or Bicep files.
1. **`azd deploy`** -- builds the container, pushes to ACR, and creates a new hosted agent version.

For code deployment, `azd deploy` uploads the source package instead of building your container. In either mode, azd owns agent-version deployment; choosing Terraform infrastructure doesn't put those versions under Terraform management.

This is the same flow as running `azd up` locally, but automated in CI. Deployment doesn't replace an application-level smoke test.

For an application-only release against existing infrastructure, run `azd deploy` without repeating provisioning when the infrastructure configuration is unchanged. Keep shared-resource provisioning in the platform team's workflow if that team owns its lifecycle.

If your application team needs Terraform to manage the logical agent too, use the [standalone Terraform deployment stages](deploy-hosted-agent-terraform.md#plan-the-deployment-stages). That path separates base infrastructure, image build and push, and agent definition updates without requiring `azd`.

## Configure GitHub Actions

After running `azd pipeline config`, review `.github/workflows/azure-dev.yml`. Keep the generated Terraform setup and authentication steps if you chose Terraform.

The following example shows the provision and deploy flow. For Terraform, configure the three `RS_*` repository variables from your backend and set `TERRAFORM_VERSION` to your reviewed Terraform version. You don't need those values for Bicep.

<!-- [TO VERIFY] Validate the Terraform remote-state/OIDC variant on a fresh GitHub runner before publication. -->

```yaml
name: Azure Developer CLI

on:
  push:
    branches:
      - main
  workflow_dispatch:

permissions:
  id-token: write
  contents: read

concurrency:
  group: hosted-agent-deployment
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    env:
      AZURE_CLIENT_ID: ${{ vars.AZURE_CLIENT_ID }}
      AZURE_TENANT_ID: ${{ vars.AZURE_TENANT_ID }}
      AZURE_SUBSCRIPTION_ID: ${{ vars.AZURE_SUBSCRIPTION_ID }}
      AZURE_ENV_NAME: ${{ vars.AZURE_ENV_NAME }}
      AZURE_LOCATION: ${{ vars.AZURE_LOCATION }}
      ARM_CLIENT_ID: ${{ vars.AZURE_CLIENT_ID }}
      ARM_TENANT_ID: ${{ vars.AZURE_TENANT_ID }}
      ARM_SUBSCRIPTION_ID: ${{ vars.AZURE_SUBSCRIPTION_ID }}
      ARM_USE_OIDC: "true"
      RS_RESOURCE_GROUP: ${{ vars.RS_RESOURCE_GROUP }}
      RS_STORAGE_ACCOUNT: ${{ vars.RS_STORAGE_ACCOUNT }}
      RS_CONTAINER_NAME: ${{ vars.RS_CONTAINER_NAME }}
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Install azd
        uses: Azure/setup-azd@v2

      - name: Install Terraform
        if: ${{ hashFiles('infra/**/*.tf') != '' }}
        uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: ${{ vars.TERRAFORM_VERSION }}
          terraform_wrapper: false

      - name: Install Foundry extensions
        run: azd ext install microsoft.foundry

      - name: Sign in to Azure (federated credentials)
        run: azd auth login --client-id $AZURE_CLIENT_ID --federated-credential-provider github --tenant-id $AZURE_TENANT_ID

      - name: Provision infrastructure
        run: azd provision --no-prompt

      - name: Deploy agent
        run: azd deploy --no-prompt
```

The concurrency group serializes this workflow's deployments. Coordinate any other repositories or tools that deploy the same agent; a GitHub concurrency group isn't a service-wide lock.

Terraform's Azure provider authentication and `azd` authentication are separate. Keep the `ARM_*` OIDC settings as well as the `azd` sign-in step. Don't add a long-lived client secret solely because your infrastructure uses Terraform.

> [!NOTE]
> The `azd ext install microsoft.foundry` step is required in CI because the runner image doesn't include the extension. The meta-package installs every individual Foundry extension (`azure.ai.agents`, `azure.ai.connections`, `azure.ai.inspector`, `azure.ai.projects`, `azure.ai.routines`, `azure.ai.skills`, and `azure.ai.toolboxes`). To install just the agent surface, replace it with `azd ext install azure.ai.agents`, which also pulls in `azure.ai.inspector` as a dependency.

## Configure Azure DevOps

`azd pipeline config` also supports Azure DevOps.

1. Select "Azure DevOps" when prompted.
1. Review the generated `azure-pipelines.yml` file.
1. Confirm that the generated file contains equivalent install, sign-in, provision, and deploy steps.

For Terraform, also configure the remote backend, Terraform installation, and authentication for the backend and providers. Don't copy GitHub-specific OIDC environment assumptions into Azure Pipelines. See [Configure Azure Pipelines](/azure/developer/azure-developer-cli/pipeline-azure-pipelines).

## Set pipeline-friendly flags

Most `azd ai` commands accept flags that make them safe to run unattended in CI. Set these on the relevant `azd ai` steps in your pipeline.

- `--no-prompt` -- disables interactive prompts. The command fails fast with a helpful error rather than blocking on input. Every `azd ai` command supports it. Always set this in CI; without it, a missing required value can hang the job until it times out.
- `--output json` -- emits structured output you can parse with `jq`, PowerShell `ConvertFrom-Json`, or any other JSON tool, for commands that support it, such as `azd ai agent show` and the `connection`, `toolbox`, `skill`, and `routine` commands. `azd ai agent invoke` uses `--output raw` instead.
- `--project-endpoint` (`-p`) -- pins the Microsoft Foundry project endpoint for a single resource command (`connection`, `toolbox`, `skill`, or `routine`). The `azd ai agent` commands resolve the project from the active `azd` environment, global config, or the `FOUNDRY_PROJECT_ENDPOINT` environment variable.
- `--debug` -- emits verbose diagnostic output. Helpful when investigating a CI failure, but noisy for normal runs.

Example:

```bash
azd ai agent invoke my-agent "ping" --no-prompt --output raw
```

## Set the project context in CI

Pipelines run outside an interactive `azd` project context, so `azd ai` direct commands need to know which Foundry project to target. Pick whichever of the following two patterns fits your pipeline.

### Set the environment variable

Set `FOUNDRY_PROJECT_ENDPOINT` once on the job or the whole workflow. Every `azd ai` command picks it up automatically after the in-project azd env and the global config.

```yaml
jobs:
  agent-checks:
    runs-on: ubuntu-latest
    env:
      FOUNDRY_PROJECT_ENDPOINT: ${{ vars.FOUNDRY_PROJECT_ENDPOINT }}
    steps:
      - uses: actions/checkout@v4
      - uses: Azure/setup-azd@v2
      - run: azd ext install microsoft.foundry
      - run: azd ai agent show --no-prompt --output json
```

### Pin the endpoint with `azd ai project set`

Run `azd ai project set $FOUNDRY_PROJECT_ENDPOINT --no-prompt` early in the job. It writes the endpoint to the global azd config (`~/.azd/config.json`), and subsequent `azd ai` commands in the same job use that context.

```yaml
- run: azd ai project set ${{ vars.FOUNDRY_PROJECT_ENDPOINT }} --no-prompt
- run: azd ai agent show --no-prompt --output json
```

The CLI resolves the endpoint in this order: the `--project-endpoint` flag, the active `azd` environment inside an `azd` project, the global config set by `azd ai project set`, and finally the `FOUNDRY_PROJECT_ENDPOINT` environment variable. If none resolve, the command exits with a structured error.

For more on running `azd ai` commands without an azd project on disk, see [Set the azd project context](cli-project-context.md).

## Verify with eval in CI

After the pipeline deploys, or gains access to a target project, use `azd ai agent eval run` for regression checks. Run a stored eval against the current agent and fail the job if scores drop below your threshold.

```bash
azd ai agent eval run --no-prompt
```

`eval run` resolves `eval.yaml` in the project root by default, or you can pass `--config <path>`. It doesn't regenerate datasets and evaluators as a side effect. To bring up the eval suite in CI, run `azd ai agent eval generate` first. That command requires a deployed agent that you can invoke.

## Configure environment-specific deployments

For multiple environments, such as development, staging, and production:

1. Create separate azd environments:

   ```bash
   azd env new staging
   azd env set AZURE_LOCATION=eastus2
   ```

1. Configure a pipeline per environment, or use branch-based triggers:

   - `main` -> production
   - `develop` -> staging

1. Use each pipeline run's own azd environment variables so resources are isolated.

## Validate a candidate before production promotion

By default, a Foundry endpoint follows the latest version. A pipeline that deploys and then tests can therefore change production traffic before the test runs.

For gated releases, [pin production to its existing version before deployment](manage-hosted-agent.md#release-a-version-without-changing-production). Capture the version created by the deployment, validate that exact candidate, and promote it only after approval.

`azd deploy` waits for version activation, but readiness alone doesn't establish that your agent behaves correctly. Use a fresh version-pinned session and check expected response content. Don't treat any nonempty CLI output as a successful smoke test.

During deployment, azd also applies endpoint settings configured for the agent. Review those settings and deployment hooks so they don't overwrite the production pin. Keep promotion separate from ordinary `azd deploy` and from infrastructure provisioning.

## Manage secrets

`azd pipeline config` stores the following values as repository secrets or variables:

- `AZURE_CLIENT_ID` -- service principal client ID.
- `AZURE_TENANT_ID` -- Microsoft Entra tenant ID.
- `AZURE_SUBSCRIPTION_ID` -- target subscription.
- `AZURE_ENV_NAME` -- azd environment name.
- `AZURE_LOCATION` -- Azure region.

Add agent-specific secrets, such as MCP API keys referenced from the `env` map for your `azure.ai.agent` service in `azure.yaml`, as more repository secrets. Map each one to an `azd` environment variable in the pipeline.

## Troubleshoot pipeline issues

Review common issues before you rerun the pipeline. For CI provisioning, you might need **Foundry Owner** in addition to Azure roles.

[!INCLUDE [role-rename-note](../../includes/role-rename-note.md)]

| Issue | Solution |
|-------|----------|
| `azd ext install` fails in CI | Ensure the runner has internet access and azd 1.25.2+ is installed. |
| `AuthorizationFailed` during provision | Verify the service principal has **Contributor** and **Foundry Owner** roles. |
| Foundry extensions not found | Add `azd ext install microsoft.foundry`, or the individual extension, before any `azd ai` or `azd up` commands. |
| Secrets not available | Check that `azd pipeline config` completed and that the secrets are visible in your repository settings. |

## Related content

- [Promote hosted agents to production](deploy-hosted-agent-production.md) for environment promotion, canary deployments, and rollback.
- [Deploy a hosted agent](deploy-hosted-agent.md) to understand what happens during deployment.
- [Azure YAML reference](../concepts/azure-yaml-reference.md) to review deployment configuration details.
- [Configure a DevOps pipeline with azd](/azure/developer/azure-developer-cli/configure-devops-pipeline) for the full azd pipeline reference.
