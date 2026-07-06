---
title: "Run a hosted agent locally with the Azure Developer CLI"
description: "Start and test a Microsoft Foundry hosted agent on your local machine with azd before you deploy it to Foundry."
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

# Run a hosted agent locally with the Azure Developer CLI

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

Use `azd ai agent run` to start your Microsoft Foundry hosted agent on your local machine and `azd ai agent invoke --local` to test it without deploying to Azure. You also learn how to set ports, choose an agent in a multi-agent project, override startup commands, and pass local runtime secrets.

## Prerequisites

- An initialized hosted agent project. To create one, see [Initialize an agent project](init-agent-project.md).
- The azd Foundry extensions installed. For installation steps, see [Install the azd Foundry extensions](install-cli-foundry-extensions.md).
- An authenticated Azure Developer CLI session. Run `azd auth login` if needed.
- Required language runtimes for your agent, such as Python 3.10+, .NET 8+, or Node.js.

## Start the agent

- Start the agent from your project directory:

   ```bash
   azd ai agent run
   ```

   This command auto-detects the project type (Python, .NET, Node.js), installs dependencies, and starts the agent server on `localhost:8088`. The startup command is read from the `startupCommand` property in `azure.yaml`.

> [!TIP]
> `azd ai agent run` automatically injects environment variables from your default [azd environment](../concepts/azure-yaml-reference.md), the one you set with `azd env select` or created during `azd ai agent init`. This means variables like `FOUNDRY_PROJECT_ENDPOINT`, `AZURE_SUBSCRIPTION_ID`, and any values you've set with `azd env set` are available to your agent without manual configuration.
>
> See [Configure environment variables for a hosted agent](configure-hosted-agent-env-variables.md) for the full list.

## Start on a custom port

- Pass `--port` when the default port is unavailable:

   ```bash
   azd ai agent run --port 9090
   ```

## Start a specific agent

- If your project defines multiple agents, specify which one to run:

   ```bash
   azd ai agent run my-agent
   ```

## Override the startup command

- Pass `--start-command` to override the command in `azure.yaml`:

   ```bash
   azd ai agent run --start-command "python app.py"
   ```

   This overrides the `startupCommand` defined in your `azure.yaml` service configuration. The `startupCommand` is the default command used both for local development (`azd ai agent run`) and for container startup when deployed. See [azure.yaml service configuration](../concepts/azure-yaml-reference.md) for details.

## Pass environment variables and secrets

A local run reads the `environment_variables` declared in your `agent.yaml` and resolves any `${VAR}` placeholders from the active `azd` environment. To provide a value, such as an API key, set it as an `azd` environment variable and reference it in `agent.yaml`.

1. Set the value in the active `azd` environment:

   ```bash
   azd env set OPENAI_KEY <value>
   ```

   `azd` stores environment values in `.azure/<env>/.env`. The `.azure` directory is gitignored by default, so these values stay out of source control.

1. Reference the variable in `agent.yaml` so the local run injects it:

   ```yaml
   environment_variables:
     - name: OPENAI_KEY
       value: ${OPENAI_KEY}
   ```

For secrets that shouldn't live in a local `.env` file at all, store them in a Foundry project connection and reference them with a `${{connections.<name>.credentials.<field>}}` placeholder in `environment_variables`. The platform resolves the placeholder at runtime. For more information, see [Configure environment variables for a hosted agent](configure-hosted-agent-env-variables.md).

## Test with invoke

- Open a separate terminal and send a message to your running agent:

   ```bash
   azd ai agent invoke --local "Hello, what can you do?"
   ```

   The `--local` flag routes the request to `localhost:8088` instead of the deployed endpoint.

### Test protocols with invoke

The protocol your agent uses is defined in `agent.yaml` under `protocols`. If your agent implements the `responses` protocol, `invoke` sends a standard Responses API request. If your agent uses the `invocations` protocol, the payload is whatever your agent code expects. Use `--input-file` (`-f`) to send a custom JSON body:

```bash
azd ai agent invoke --local -f request.json
```

For `invocations` agents, refer to the sample's README or inspect the handler or entry point to understand the expected payload structure.

If your agent implements multiple protocols, `invoke` uses the `responses` protocol by default. Pass `-p` (`--protocol`) with `responses` or `invocations` to select one explicitly:

```bash
azd ai agent invoke --local --protocol invocations -f request.json
```

## Test with curl

- Test directly with `curl`:

   ```bash
   curl -X POST http://localhost:8088/responses \
     -H "Content-Type: application/json" \
     -d '{"input": "Hello, what can you do?"}'
   ```

## Troubleshoot local development

| Issue | Solution |
|-------|----------|
| `AuthenticationError` | Run `azd auth login` to refresh credentials. |
| `ResourceNotFound` | Verify endpoint URLs match Foundry portal values. |
| `DeploymentNotFound` | Check the deployment name in your `azure.yaml`. |
| Connection refused on port 8088 | Ensure no other process is using the port. |
| Dependencies fail to install | Ensure Python 3.10+ or .NET 8+ is installed. |

## Related content

- [Invoke a hosted agent with the Azure Developer CLI](invoke-hosted-agent.md) for invoke options, sessions, and file input.
- [Inspect a local agent with the Agent Inspector](agent-inspector.md) for a browser-based local test UI.
- [Configure environment variables for a hosted agent](configure-hosted-agent-env-variables.md) for local and deployed configuration.
