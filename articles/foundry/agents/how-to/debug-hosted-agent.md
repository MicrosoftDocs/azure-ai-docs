---
title: "Debug a hosted agent"
description: "Diagnose Microsoft Foundry hosted agent authentication, local runtime, deployment, direct-command, log, and routine issues with azd."
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

# Debug a hosted agent


[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

Diagnose and fix common issues when you build, run, and deploy agents with `azd ai agent` for Microsoft Foundry. Start with the diagnostic commands. Then use the symptom-based sections to troubleshoot authentication, local development, deployment, direct commands, logs, and routines.

## Prerequisites

- An initialized hosted agent project. To create one, see [Initialize an agent project](init-agent-project.md).
- The azd Foundry extensions installed. For installation steps, see [Install the azd Foundry extensions](install-cli-foundry-extensions.md).
- An authenticated Azure Developer CLI session. Run `azd auth login` if needed.
- For deployment and log issues, a deployed hosted agent. To deploy one, see [Deploy a hosted agent](deploy-hosted-agent.md).

## Gather diagnostic context

Before diving into specific errors, use these commands to gather context:

```bash
# Check extension version
azd ai agent version

# Verify Azure authentication
azd auth login

# Show current environment configuration
azd env get-values

# View agent details
azd ai agent show

# Show the resolved Foundry project endpoint and where it came from
azd ai project show

# Stream production logs
azd ai agent monitor --follow
```

For a structured health report, run `azd ai agent doctor`. For more information, see [Diagnose a project with agent doctor](agent-doctor.md).

## Fix authentication errors

### Fix `AuthenticationError`

**Symptoms:** Agent fails to start locally or returns 401/403 when calling the AI model.

**Causes and fixes:**

- **Expired credentials** -- Run `azd auth login` to refresh your Azure session.
- **Wrong subscription** -- Verify with `azd env get-values | grep AZURE_SUBSCRIPTION_ID` and compare against the Foundry project's subscription.
- **Missing RBAC roles** -- Your identity needs Foundry User or equivalent access on the Foundry project.

[!INCLUDE [role-rename-note](../../includes/role-rename-note.md)]

Your identity also needs **Cognitive Services OpenAI User** to use model deployments.

### Fix `AuthorizationFailed` during provisioning

**Symptoms:** `azd up` or `azd provision` fails with a permissions error.

**Fix:** Request **Contributor** role on your Azure subscription. For CI/CD, the service principal also needs **Foundry Owner**.

### Fix `SubscriptionNotRegistered`

**Symptoms:** Provisioning fails because a required resource provider isn't registered.

**Fix:**

```bash
az provider register --namespace Microsoft.CognitiveServices
az provider register --namespace Microsoft.ContainerRegistry
```

## Fix local development issues

### Fix connection refused on port 8088

**Symptoms:** `azd ai agent invoke --local` fails to connect.

**Causes and fixes:**

- **Agent not running** -- Start it with `azd ai agent run` in a separate terminal.
- **Port conflict** -- Another process is using port 8088. Either stop it or use a custom port:

   ```bash
   azd ai agent run --port 9090
   azd ai agent invoke --local --port 9090 "Hello!"
   ```

- **Startup crash** -- Check the terminal where `azd ai agent run` is running for error output. Common causes include missing dependencies, import errors, or incorrect `startupCommand` in `azure.yaml`.

### Fix dependency installation failures

**Symptoms:** `azd ai agent run` fails during dependency installation.

**Causes and fixes:**

- **Wrong runtime version** -- Ensure Python 3.10+ or .NET 8+ is installed.
- **Missing `requirements.txt` or `.csproj`** -- The CLI auto-detects the project type from these files. Verify they exist in your agent directory.
- **Network issues** -- Package registries may be blocked by your corporate proxy. Check your `pip` or `dotnet` configuration.

### Fix `ResourceNotFound` or `DeploymentNotFound`

**Symptoms:** Agent starts but fails when trying to call the model.

**Causes and fixes:**

- **Endpoint mismatch** -- Run `azd env get-values` and verify that `FOUNDRY_PROJECT_ENDPOINT` matches the endpoint shown in the Foundry portal.
- **Model deployment name mismatch** -- The model deployment name in your `agent.yaml` must match the deployment name in your Foundry project. Check in the portal under **Deployments**.
- **Resources not provisioned** -- If you haven't run `azd up` yet, the cloud resources won't exist. Run `azd up` first, then test locally. The local agent still calls cloud-hosted models.

## Fix deployment issues

### Fix container build failures

**Symptoms:** `azd up` fails during the Docker build phase.

**Causes and fixes:**

- **Missing Dockerfile** -- Ensure your agent directory has a `Dockerfile`. If you initialized from a template, this is auto-generated.
- **Build context errors** -- The `Dockerfile` must be in the directory specified by the service `project` path in `azure.yaml`.
- **Dependency installation in Docker** -- If pip/dotnet restore fails inside the container, check that your `requirements.txt` or `.csproj` has all dependencies pinned correctly.

### Fix `azd up` hangs or timeouts

**Symptoms:** Provisioning or deployment takes an unusually long time.

**Causes and fixes:**

- **First deployment** -- The first `azd up` provisions all Azure resources, including Foundry project, ACR, managed identity, and model deployment, and can take 5-10 minutes. Subsequent deployments are faster.
- **Remote build** -- By default, container images are built remotely on ACR. This can be slower but doesn't require Docker locally. To build locally instead, set `docker.remoteBuild: false` in your `azure.yaml` service config.
- **Region capacity** -- Some regions may have limited capacity for certain model SKUs. Try a different region if provisioning consistently fails.

### Fix an agent that deploys but doesn't respond

**Symptoms:** `azd ai agent invoke` times out or returns errors after a successful deployment.

**Causes and fixes:**

- **Health probe failing** -- Your container must respond to `GET /readiness` on port 8088 with a 200 status. Check logs with `azd ai agent monitor --follow`.
- **Protocol mismatch** -- Ensure the protocol defined in `agent.yaml` matches what your code implements. If `agent.yaml` says `responses` but your code only handles `invocations`, or vice versa, requests fail.
- **Container crashes** -- Check system logs for restart events: `azd ai agent monitor --type system`. Common causes include unhandled exceptions and out-of-memory issues. Increase container resources in `azure.yaml` if needed.

## Fix direct-command failures

These errors come from the `azd ai` direct commands, such as `azd ai connection`, `azd ai toolbox`, and `azd ai routine`, when run against a Foundry project.

### Fix no resolved Foundry project endpoint

**Symptoms:** A direct command exits with `No Foundry project endpoint resolved. Run azd ai project set to set one, or pass --project-endpoint.`

**Cause:** The CLI couldn't find a Foundry project endpoint in any of the supported sources: the `--project-endpoint` flag, the active `azd` environment, the global config, or the `FOUNDRY_PROJECT_ENDPOINT` environment variable.

**Fixes:**

- Run `azd ai project set <endpoint>` to store the endpoint in your global `azd` config (`~/.azd/config.json`).
- Pass `--project-endpoint` (`-p`) on each command: `azd ai connection list -p https://my-proj.services.ai.azure.com/api/projects/my-project`.
- Set `FOUNDRY_PROJECT_ENDPOINT` in your shell environment.

For the full resolution order and when each source wins, see [Understand azd project context](cli-project-context.md).

### Fix create failures for existing resources

**Symptoms:** `azd ai connection create`, `azd ai toolbox create`, `azd ai routine create`, or `azd ai skill create` fails with an "already exists" error.

**Cause:** By design, `create` isn't upsert. The default failure mode prevents one developer from silently overwriting another's state on a shared Foundry project.

**Fixes:**

- Pick a different name and rerun.
- Pass `--force`, where the `create` command supports it, to replace the existing resource through an ARM PUT. Replacement is destructive: it overwrites the existing resource in place, and any drift from manual portal edits, metadata, or credentials is lost. The `azd ai toolbox create` command doesn't support `--force`. Delete the existing toolbox or use a new name instead.

### Fix `connection show` credential output

**Symptoms:** `azd ai connection show <name>` returns the connection's name, kind, target, and auth type, but no API key or credential value.

**Cause:** By design, credential values are never returned by default. They require the explicit `--show-credentials` flag.

**Fix:**

```bash
azd ai connection show tavily-conn --show-credentials
```

This invokes the data-plane API and requires data-plane permissions on the Foundry project, such as Foundry User or equivalent. If you have only management-plane `Reader` or `Contributor` access, the call fails with a 403. Ask your project owner for the data-plane role.

## Read agent logs

Use `azd ai agent monitor` to inspect agent behavior:

```bash
# Stream all recent logs
azd ai agent monitor --follow

# View system-level events (container starts, crashes, restarts)
azd ai agent monitor --type system

# Filter to a specific session
azd ai agent monitor --session-id <session-id>
```

Common log patterns include:

| Log message | Meaning |
|-------------|---------|
| `Listening on 0.0.0.0:8088` | Agent started successfully. |
| `AuthenticationError` | Credential or RBAC issue. Check managed identity. |
| `ModelNotFound` | Model deployment name doesn't match `agent.yaml`. |
| Container restart in system events | Crash loop. Check code errors or increase resource limits. |

## Diagnose routine failures

Routines fail differently from interactive `agent invoke` calls because no caller is present to surface the error. A routine is a timer-triggered, recurring, GitHub issue-triggered, or custom-event-triggered run of an agent. Use `azd ai routine run list` to inspect what happened.

### Inspect past runs

```bash
# Recent runs of a routine: trigger time, agent input/output, status, trace link
azd ai routine run list daily-digest
```

### Filter to failures

```bash
# Failed runs only, with an OData filter
azd ai routine run list daily-digest --filter "status eq 'failed'"
```

Combine with `--top` to widen or narrow the window.

### Drill into a single run

```bash
# Full detail for the most recent runs as JSON, then look up the run you care about
azd ai routine run list daily-digest --top 5 --output json
```

The JSON output includes the input payload, the agent's response, and a deep link to the distributed trace, the same trace you would see for an interactive invocation.

### Manually retrigger a routine

If you need to reproduce a failure or test a fix, fire the routine on demand with `dispatch`:

```bash
azd ai routine dispatch daily-digest
azd ai routine dispatch triage-issues --input '{"issue":{"number":42}}'
```

`dispatch` runs asynchronously and prints a dispatch ID. Check the result with `azd ai routine run list <name>`.

### Fix a failed routine run

`azd ai routine run list` shows the run with `status: failed`. Follow the trace link to see the underlying agent error, such as model error, tool failure, or timeout. The agent-side fixes are the same as for interactive failures. See [Fix authentication errors](#fix-authentication-errors) and [Read agent logs](#read-agent-logs).

### Fix a routine that never fires

If `azd ai routine run list` returns no runs at all, the trigger itself isn't firing:

1. Check the routine is enabled: `azd ai routine show <name>`. Look for `enabled: true`.
1. For `timer` triggers, verify `--at` is in the future and has not already fired.
1. For `recurring` triggers, verify the `--cron` expression is valid and that the `--time-zone` is what you expected.
1. For `github-issue` triggers, verify that the `--connection-id` resolves to a healthy connection and that the GitHub repository and `--issue-event` match the events the repository emits.
1. For `custom` triggers, verify the `--provider`, `--event-name`, and `--parameters` scope matches events the provider is publishing.

## Get more help

- **Debug mode** -- Add `--debug` to any `azd` command for verbose output.
- **Azure portal** -- Check the Foundry project in the Azure portal for resource health and diagnostics.
- **File a bug** -- Report issues at [github.com/Azure/azure-dev/issues](https://github.com/Azure/azure-dev/issues).

## Related content

- [Monitor hosted agent logs with the Azure Developer CLI](monitor-hosted-agent-logs.md) for deeper log inspection options.
- [Test a hosted agent](test-hosted-agent.md) to prevent issues with structured testing.
- [Diagnose a project with agent doctor](agent-doctor.md) for a structured project health report.
