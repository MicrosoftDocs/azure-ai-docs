---
title: "Debug a hosted agent"
description: "Diagnose Microsoft Foundry hosted agent authentication, local runtime, deployment, direct-command, log, and routine issues with azd."
author: aahill
ms.author: aahi
ms.manager: mcleans
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.topic: how-to
ms.date: 09/01/2026
ms.custom: dev-focus, doc-kit-assisted
ai-usage: ai-assisted
---

# Debug a hosted agent

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

## Diagnose invocation latency

Use the latency debug headers to determine whether a slow hosted agent request
spent time in the platform, provisioning infrastructure, waiting for the
container, or processing the request in your agent. These headers are
diagnostic signals, not SLA or billing metrics.

Enable the diagnostic on each request by setting
`x-ms-debug-latency-enabled: true`. If the request doesn't include this header,
the response won't include the `x-ms-debug-latency-*` headers.

1. Add the latency header to a hosted agent Responses or Invocations protocol
   request. This example uses the Responses protocol:

   ```bash
   ENDPOINT="https://{account}.services.ai.azure.com/api/projects/{project}"
   API_VERSION="v1"
   TOKEN=$(az account get-access-token \
     --resource https://ai.azure.com \
     --query accessToken -o tsv)
   AGENT="my-code-agent"

   curl --http2 -i -X POST \
     "$ENDPOINT/agents/$AGENT/endpoint/protocols/openai/responses?api-version=$API_VERSION" \
     -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     -H "x-ms-debug-latency-enabled: true" \
     -d '{"model":"gpt-5.4-mini","input":"Hello, agent!","stream":false}'
   ```

1. Inspect the response headers. All latency values are integer milliseconds:

   | Header | Meaning |
   | --- | --- |
   | `x-ms-debug-latency-session-start-type` | Type of session start the request triggered: a cold start (`cold`), warm start (`warm`), or resume from idle (`resume`). |
   | `x-ms-debug-latency-platform-preprocessing-ms` | Platform time for admission, authentication, session lookup, and orchestration. It doesn't include micro-VM provisioning or container readiness delays. Available for cold, warm, and resumed session starts. |
   | `x-ms-debug-latency-infra-setup-ms` | Time to provision the micro-VM. Omitted for warm requests. |
   | `x-ms-debug-latency-container-readiness-ms` | Time from the micro-VM creation until the container reports ready. Omitted for warm requests. |
   | `x-ms-debug-latency-container-response-ms` | Time from proxy forwarding until response headers are committed. Includes request transfer, connection setup, agent handling, retries, and output-policy buffering. |
   | `x-ms-debug-latency-response-begin-ms` | Total time from service acceptance until response headers are committed. This value isn't time to the first response body byte or first server-sent event. |

   The four timing components add up to
   `x-ms-debug-latency-response-begin-ms`. On a cold or resumed request, if the
   platform can't capture every provisioning boundary, it omits the
   infrastructure and readiness headers and includes that time in platform
   preprocessing.

1. Use the session start type and largest timing component to identify the
   likely source of delay:

   | Result | Interpretation | What to do |
   | --- | --- | --- |
   | `x-ms-debug-latency-session-start-type` is `cold` or `resume`, and `x-ms-debug-latency-infra-setup-ms` is high | The platform spent time provisioning the micro-VM. | Compare several cold or resumed requests. If the delay persists, record the response ID, timestamp, and latency headers for a support request. |
   | `x-ms-debug-latency-session-start-type` is `cold` or `resume`, and `x-ms-debug-latency-container-readiness-ms` is high | The container took a long time to start and report ready. | Measure initialization steps in your startup logs, reduce work before the readiness endpoint becomes available, and precompile application code where possible. |
   | `x-ms-debug-latency-platform-preprocessing-ms` is high for any session start type | The delay occurred in the platform before micro-VM provisioning or container readiness. | Create a support request. Include the response ID, timestamp, session start type, and latency headers. |
   | `x-ms-debug-latency-container-response-ms`, `x-ms-debug-latency-first-byte-ms`, or the trailer's `first_byte_ms` is high | The delay occurred after proxy forwarding began. | Instrument the request handler and inspect agent logs, model calls, tool calls, retries, and output buffering. |

### Reduce container readiness time

The container readiness value includes the time required to start your process,
load the application, and return HTTP 200 from `/readiness`. Add timestamps to
startup logs to identify slow imports, dependency loading, network calls, and
other initialization work.

Apply these optimizations to the slow steps you identify:

- Install dependencies and compile code when you build the image. Don't run
  package installation, restore, or compilation at container startup.
- Use a multistage build and exclude build tools, package caches, tests, and
  other development files from the runtime image.
- Avoid model calls, migrations, tool discovery, and asset downloads before
  readiness. Parallelize independent initialization that must finish first.
- Keep `/readiness` focused on whether the agent can accept requests. If you
  defer initialization, measure the first request to ensure you didn't move
  the startup delay into request handling.

# [Python](#tab/python)

Install dependencies in a virtual environment that you copy into the runtime
image. Compile dependencies on a best-effort basis so an unparsable file in a
third-party package doesn't fail the build. Compile the application strictly
so syntax errors fail the build.

```dockerfile
FROM python:3.13-slim AS build

WORKDIR /app
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN PYTHONDONTWRITEBYTECODE= python -m compileall -q /opt/venv \
      || true; \
    PYTHONDONTWRITEBYTECODE= python -m compileall -q /app

FROM python:3.13-slim AS final

ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /app

COPY --from=build /opt/venv /opt/venv
COPY --from=build /app /app

# Precompile the standard library in the runtime image.
RUN PYTHONDONTWRITEBYTECODE= python -m compileall -q \
    "$(python -c "import sysconfig; print(sysconfig.get_path('stdlib'))")" \
    || true

CMD ["python", "main.py"]
```

Clearing `PYTHONDONTWRITEBYTECODE` for this build step permits Python to write
the bytecode into the image. The environment variable blocks bytecode writes,
not reads, so the running container can still use the compiled files.

Reference: [`compileall` - Byte-compile Python libraries](https://docs.python.org/3/library/compileall.html)

# [.NET](#tab/dotnet)

Publish with ReadyToRun to compile assemblies for the target runtime and reduce
the work the just-in-time compiler performs during startup. This example
uses matching glibc-based SDK and runtime images, so the correct .NET runtime
identifier is `linux-x64`.

```dockerfile
FROM mcr.microsoft.com/dotnet/sdk:10.0 AS build

WORKDIR /src
COPY . .

RUN dotnet publish -c Release \
    -r linux-x64 \
    --self-contained false \
    -p:PublishReadyToRun=true \
    -o /app

FROM mcr.microsoft.com/dotnet/aspnet:10.0 AS final

WORKDIR /app
COPY --from=build /app .

ENTRYPOINT ["dotnet", "MyAgent.dll"]
```

Replace `MyAgent.dll` with your published assembly name. Keep restore, build,
and publish in the same command so the ReadyToRun property applies during
restore. ReadyToRun improves startup performance at the cost of a larger image
and longer build.

> [!IMPORTANT]
> The runtime identifier must match the runtime image. If you use Alpine
> Linux, use `sdk:10.0-alpine` and `aspnet:10.0-alpine` for the two stages and
> use `linux-musl-x64`. Don't use `linux-x64` with an Alpine image or
> `linux-musl-x64` with a glibc-based image. A mismatch can cause restore,
> publish, or runtime failures.

Reference: [ReadyToRun deployment](/dotnet/core/deploying/ready-to-run)

---

Build either image for the x86-64 architecture required by hosted agents:

```bash
docker build --platform linux/amd64 -t my-agent:latest .
```

Here, `linux/amd64` is a Docker platform, not a .NET runtime identifier.

Reference: [Hosted agent container requirements](deploy-hosted-agent.md#container-requirements)

### Investigate agent and model latency

If container readiness is fast but container response or first-byte time is
high, focus your investigation on the request path after forwarding begins.
Run `azd ai agent monitor --follow` while reproducing the request, and add
tracing around model calls, tool calls, external services, retries, and
response serialization. For more information, see
[Monitor hosted agent logs](monitor-hosted-agent-logs.md).

For an agent that calls a large language model, measure model latency
separately before changing the deployment. Compare time to first token, time
between tokens, generated token count, prompt size, deployment utilization,
and throttling. Then evaluate model choice, output-token limits, streaming, and
workload separation. See
[Improve Azure OpenAI performance](../../openai/how-to/latency.md#improve-performance).

If measurements show sustained capacity pressure for a predictable workload,
evaluate a provisioned deployment and size it for the observed input tokens,
output tokens, and request rate. See
[Provisioned throughput](../../openai/concepts/provisioned-throughput.md).

### Inspect completion timings

On HTTP/2 or later, the service can return the best-effort
`x-ms-debug-latency-final` response trailer. It repeats the response-header
values and can add these fields:

| Field | Meaning |
| --- | --- |
| `first_byte_ms` | Time from service acceptance until the first response body byte or server-sent event. |
| `total_last_byte_ms` | Time from service acceptance until response forwarding completes. |

The trailer uses a versioned, semicolon-delimited format:

```http
x-ms-debug-latency-final: v=1;start=cold;platform_pre_ms=...;
  infra_ms=...;ready_ms=...;container_response_ms=...;
  response_begin_ms=...;first_byte_ms=...;total_last_byte_ms=...
```

HTTP/1.1 responses don't include this trailer. A trailer can also be absent
after cancellation, client disconnection, a midstream error, or when a gateway
or SDK doesn't preserve trailers. Treat the response headers as the guaranteed
diagnostic contract.

### Retrieve stored latency results

The service stores captured timings with the response or invocation. A later
GET request for the same response or invocation ID returns the original request's
timings as response headers. The GET request doesn't require the latency header and
doesn't measure the GET request itself.

The GET request can also return these completion values as ordinary headers:

| Header | Meaning |
| --- | --- |
| `x-ms-debug-latency-first-byte-ms` | Time to the first response body byte. |
| `x-ms-debug-latency-total-last-byte-ms` | Time until response forwarding completed. |

Storage is eventually consistent, so a GET request immediately after the original
request might not include the headers yet. For an asynchronous response or
invocation, only the platform-overhead values are available: session start
type, platform preprocessing, infrastructure setup, and container readiness.
Latency headers aren't emitted for failed proxy responses or WebSocket
(`invocations_ws`) requests.

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
- **Model deployment name mismatch** -- The model deployment name configured in `azure.yaml` must match the deployment name in your Foundry project. Check in the portal under **Deployments**.
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
- **Protocol mismatch** -- Ensure the protocol defined in the `azure.ai.agent` service in `azure.yaml` matches what your code implements. If `azure.yaml` says `responses` but your code only handles `invocations`, or vice versa, requests fail.
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
| `ModelNotFound` | Model deployment name doesn't match `azure.yaml`. |
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
