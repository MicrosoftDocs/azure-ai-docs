---
title: "Set up CI/CD for hosted agents with the Azure Developer CLI"
description: "Configure GitHub Actions or Azure DevOps pipelines to provision and deploy Microsoft Foundry hosted agents with azd."
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

# Set up CI/CD for hosted agents with the Azure Developer CLI

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

Automate your hosted agent deployment with `azd pipeline config`. In this article, you set up continuous integration and delivery in GitHub Actions or Azure DevOps, then apply pipeline-friendly `azd ai` flags for unattended jobs.

## Prerequisites

- An initialized hosted agent project that works locally with `azd ai agent run` and `azd ai agent invoke --local`. For setup, see [Initialize an agent project](init-agent-project.md).
- A project that you've successfully deployed at least once with `azd up`. For deployment steps, see [Deploy a hosted agent](deploy-hosted-agent.md).
- The [azd Foundry extensions installed](install-cli-foundry-extensions.md) locally and in your pipeline runner.
- An authenticated `azd` session.
- Your code in a Git repository hosted in GitHub or Azure DevOps.

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

## Review the pipeline flow

The generated pipeline runs on push to `main` by default and executes:

1. **`azd provision`** -- creates or updates Azure infrastructure from `infra/` Bicep templates.
1. **`azd deploy`** -- builds the container, pushes to ACR, and creates a new hosted agent version.

This is the same flow as running `azd up` locally, but automated in CI.

## Configure GitHub Actions

After `azd pipeline config`, you'll have a `.github/workflows/azure-dev.yml` file. A typical workflow looks like:

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

jobs:
  build:
    runs-on: ubuntu-latest
    env:
      AZURE_CLIENT_ID: ${{ vars.AZURE_CLIENT_ID }}
      AZURE_TENANT_ID: ${{ vars.AZURE_TENANT_ID }}
      AZURE_SUBSCRIPTION_ID: ${{ vars.AZURE_SUBSCRIPTION_ID }}
      AZURE_ENV_NAME: ${{ vars.AZURE_ENV_NAME }}
      AZURE_LOCATION: ${{ vars.AZURE_LOCATION }}
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Install azd
        uses: Azure/setup-azd@v2

      - name: Install Foundry extensions
        run: azd ext install microsoft.foundry

      - name: Sign in to Azure (federated credentials)
        run: azd auth login --client-id $AZURE_CLIENT_ID --federated-credential-provider github --tenant-id $AZURE_TENANT_ID

      - name: Provision and Deploy
        run: azd up --no-prompt
```

> [!NOTE]
> The `azd ext install microsoft.foundry` step is required in CI because the runner image doesn't include the extension. The meta-package installs every individual Foundry extension (`azure.ai.agents`, `azure.ai.connections`, `azure.ai.inspector`, `azure.ai.projects`, `azure.ai.routines`, `azure.ai.skills`, and `azure.ai.toolboxes`). To install just the agent surface, replace it with `azd ext install azure.ai.agents`, which also pulls in `azure.ai.inspector` as a dependency.

## Configure Azure DevOps

`azd pipeline config` also supports Azure DevOps.

1. Select "Azure DevOps" when prompted.
1. Review the generated `azure-pipelines.yml` file.
1. Confirm that the generated file contains equivalent install, sign-in, provision, and deploy steps.

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

## Manage secrets

`azd pipeline config` stores the following values as repository secrets or variables:

- `AZURE_CLIENT_ID` -- service principal client ID.
- `AZURE_TENANT_ID` -- Microsoft Entra tenant ID.
- `AZURE_SUBSCRIPTION_ID` -- target subscription.
- `AZURE_ENV_NAME` -- azd environment name.
- `AZURE_LOCATION` -- Azure region.

Add agent-specific secrets, such as MCP API keys defined as `secret: true` parameters in `agent.yaml`, as more repository secrets. Map each one to an `azd` environment variable in the pipeline.

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

- [Deploy a hosted agent](deploy-hosted-agent.md) to understand what happens during deployment.
- [Azure YAML reference](../concepts/azure-yaml-reference.md) to review deployment configuration details.
- [Configure a DevOps pipeline with azd](/azure/developer/azure-developer-cli/configure-devops-pipeline) for the full azd pipeline reference.
