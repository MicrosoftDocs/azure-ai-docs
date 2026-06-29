---
title: "Deploy a hosted agent from source code (preview)"
description: "Deploy your hosted agent directly from source code—without building a container—by calling the Foundry Agent Service REST API."
author: aahill
ms.author: aahi
ms.date: 05/26/2026
ms.manager: nitinme
ms.topic: how-to
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.custom: doc-kit-assisted
ai-usage: ai-assisted
#CustomerIntent: As a developer new to Foundry Agent Service, I want to deploy my Python or .NET agent code without building a container so that I can iterate quickly without learning Docker or managing a registry.
---

# Deploy a hosted agent from source code (preview)

This article shows you how to deploy a [Hosted agent](../concepts/hosted-agents.md) in Foundry Agent Service from Python or .NET source code, without building or pushing a container image. You upload a `.zip` of your code (and optionally your dependencies), and Agent Service either runs it as-is or builds your dependencies for you in the cloud.

If you're deploying for the first time or want the fastest path, use the [Quickstart: Deploy your first hosted agent](../quickstarts/quickstart-hosted-agent.md) instead. The quickstart uses the **Azure Developer CLI (azd)** or the **Foundry Toolkit for VS Code**, which package your source, upload it, poll for `active`, and configure role-based access control automatically. Choose **Code** (or **Source Code (ZIP upload)**) when the quickstart asks for a deployment method.

Use this article when you want to deploy source-code agents directly with the REST API—for custom tooling, language-agnostic automation, or integration with existing CD systems. In this article, you complete the following tasks:

- Build the source `.zip` and pick a [dependency-resolution mode](#choose-how-dependencies-are-resolved).
- Create the agent over REST, wait for it to reach `active`, and invoke it.
- Update, version, download, and stream logs for the deployed agent.

If you need full control of the runtime image or you already have a working Dockerfile, use the container-based path: [Deploy a hosted agent](deploy-hosted-agent.md).

> [!IMPORTANT]
> Source-code deployment for Hosted agents is in **preview**. Functionality, region availability, and APIs might change before general availability.

## Prerequisites

- A [Microsoft Foundry project](../../how-to/create-projects.md) in a supported region.
- [Azure CLI](/cli/azure/install-azure-cli) version 2.80 or later, signed in to the tenant that owns the project.
- A command-line HTTP client such as `curl` (the REST examples in this article use `curl`).
- For local Python packaging: `pip` from Python 3.13 or later.
- For local .NET packaging: the .NET 10 SDK.

### Supported runtimes

The `code_configuration.runtime` field in the agent definition accepts the following values. Pick the runtime that matches the binaries in your zip—Linux x86_64 wheels for Python, or the `TargetFramework` of your `dotnet publish` output for .NET.

| Language | Runtime values |
| --- | --- |
| Python | `python_3_13`, `python_3_14` |
| .NET | `dotnet_10` |

### Language version support policy

The Agent Service runtime includes the platform-built container image for each value of `code_configuration.runtime`. To keep your deployed agents fully supported, Foundry aligns hosted agent language support with end-of-life support for each language. Support ends on the community end-of-support date for the language version. Microsoft might retire a `code_configuration.runtime` value earlier when platform constraints (such as the underlying base image) require it. 

For upstream end-of-support schedules, see:

- Python: [Status of Python versions](https://devguide.python.org/versions/) (python.org).
- .NET: [.NET and .NET Core support policy](https://dotnet.microsoft.com/platform/support/policy/dotnet-core).

#### Retirement phase

After a language end-of-life date, you can still create, update, and run hosted agents that use the retired runtime value. However, those agents aren't eligible for support, new features, or security patches until you upgrade them to a supported runtime by setting a current `code_configuration.runtime` value and redeploying.

### Required permissions

You need **Foundry Project Manager** at project scope to deploy a Hosted agent. This role grants the data-plane permissions to create and update agents, plus the ability to assign **Foundry User** to the platform-created agent identity that your running code uses to call models and tools.

Your agent runs as a platform-assigned managed identity that's separate from your user identity. That identity needs **Foundry User** to call models from inside the container. If you deploy with `azd` or the Foundry Toolkit for VS Code, the tooling assigns this role automatically. If you deploy with REST, grant it yourself—see [Hosted agent permissions reference](../concepts/hosted-agent-permissions.md).

For REST calls, include the preview feature header on mutating requests (Create, Update, Delete) while the feature is in preview:

```http
Foundry-Features: CodeAgents=V1Preview,HostedAgents=V1Preview
```

GET requests work without it today, but include it on every call to be safe—the header gates preview behavior and might be enforced more strictly before GA.

## Deployment lifecycle

Every source-code deployment follows the same sequence: **package → create or update → poll until `active` → invoke**. The source-code path uses `code_configuration` in the agent definition; the image-based path uses `container_configuration` instead—the two are mutually exclusive on a single version.

For a guided walkthrough using `azd` or the Foundry Toolkit, see the [Quickstart](../quickstarts/quickstart-hosted-agent.md). The rest of this article walks the same lifecycle using the REST API.

## Choose how dependencies are resolved

Before you start, pick a value for `code_configuration.dependency_resolution`. This choice affects what you put in the zip.

| Value | Behavior | Use when |
| --- | --- | --- |
| `remote_build` | Agent Service installs dependencies from `requirements.txt` (Python) or restores the project file (.NET) during provisioning. | You want a small upload and the simplest inner loop. **Recommended for first-time users.** |
| `bundled` | The zip is run as-is. You ship prebuilt Linux dependencies in `packages/` (Python) or `dotnet publish` output (.NET). | You need reproducible builds, your dependencies are private or wheels-only, or your project doesn't restore cleanly server-side. |

For bundled mode, see [Package the zip manually](#package-the-zip-manually) for the local build commands.

> [!IMPORTANT]
> **Private virtual network prerequisite for `bundled` deployments:** If your project is secured with a private virtual network, allow outbound connections in your network policy to the following endpoints before you deploy with `bundled` dependency resolution:
>
> - `mcr.microsoft.com`
> - `agent365.svc.cloud.microsoft`
> - `deb.debian.org`
> - `packages.microsoft.com`
> - `*.login.microsoft.com`
>
> Without these outbound paths, provisioning can't download the packages it needs and the deployment fails. For network configuration, see [Deploy a hosted agent in a virtual network](virtual-networks.md).

## Deploy using the REST API

Use the [REST API](https://ai.azure.com/api-reference/agents) for direct HTTP-based deployments or custom tooling. The sections below walk through a first deployment in order: set up variables, build a zip, create the agent, poll until `active`, and invoke it. Update, version, download, and log-streaming endpoints are grouped under [Ongoing operations](#ongoing-operations).

### Set up variables

# [Bash](#tab/bash)

```bash
ENDPOINT="https://{account}.services.ai.azure.com/api/projects/{project}"
API_VERSION="2025-11-15-preview"
TOKEN=$(az account get-access-token --resource https://ai.azure.com --query accessToken -o tsv)
AGENT=my-code-agent
ZIP=./agent-code.zip
SHA=$(sha256sum "$ZIP" | cut -d' ' -f1)
```

# [PowerShell](#tab/powershell)

```powershell
$Endpoint    = "https://{account}.services.ai.azure.com/api/projects/{project}"
$ApiVersion  = "2025-11-15-preview"
$Token       = az account get-access-token --resource https://ai.azure.com --query accessToken -o tsv
$Agent       = "my-code-agent"
$Zip         = "./agent-code.zip"
$Sha         = (Get-FileHash $Zip -Algorithm SHA256).Hash.ToLower()
```

---

> [!NOTE]
> The remaining REST examples use Bash-style `curl` commands. On Windows, run them in PowerShell with `curl.exe`, using backticks (`` ` ``) instead of backslashes for line continuation.

### Build a minimal hello-world zip

Before you call Create, build a flat zip with two files. This is the minimum payload Agent Service accepts for a Python `remote_build` deployment.

```text
agent-code.zip
├── main.py            # your agent loop (starts a Foundry hosting server)
└── requirements.txt   # dependencies (for example, agent-framework, agent-framework-foundry-hosting)
```

`metadata.json` (the agent definition shown in [Metadata example](#metadata-example-remote-build-responses)) sits next to the zip on disk and is sent as a separate multipart part—it isn't inside the zip. For full layouts (including `bundled` mode and .NET), see [Package the zip manually](#package-the-zip-manually). For working source files, see the [Python](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/hosted-agents) and [.NET](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/csharp/hosted-agents) samples.

### Multipart request shape

All mutating endpoints (Create, Update) use `multipart/form-data` with two parts:

| Part | Content-Type | Body |
| --- | --- | --- |
| `metadata` | `application/json` | Agent definition. |
| `code` | `application/zip` | Raw zip bytes. Set `filename=<agent>.zip`. |

Required headers on every multipart call:

```http
Authorization: Bearer <token>
Accept: application/json
Foundry-Features: CodeAgents=V1Preview,HostedAgents=V1Preview
x-ms-code-zip-sha256: <sha256-hex-of-zip>
```

The `x-ms-code-zip-sha256` header records the SHA-256 of the zip you uploaded. The service stores it and echoes it back on `code:download` so you can detect drift between what you expected to deploy and what's deployed. Always include it.

The Create call also requires `x-ms-agent-name: <agent-name>`. Update calls omit it because the name is already part of the URL.

### Metadata example (remote build, Responses)

This metadata matches the hello-world zip.

```json
{
  "description": "Hello-world code agent",
  "definition": {
    "kind": "hosted",
    "protocol_versions": [
      { "protocol": "responses", "version": "1.0.0" }
    ],
    "cpu": "1",
    "memory": "2Gi",
    "code_configuration": {
      "runtime": "python_3_13",
      "entry_point": ["python", "main.py"],
      "dependency_resolution": "remote_build"
    },
    "environment_variables": {
      "AZURE_AI_MODEL_DEPLOYMENT_NAME": "gpt-4.1-mini"
    }
  }
}
```

For the Invocations protocol, replace the `protocol_versions` entry with `{ "protocol": "invocations", "version": "1.0.0" }`. For `bundled` mode, set `"dependency_resolution": "bundled"` and follow [Build Linux dependencies locally](#build-linux-dependencies-locally-bundled-python).

`code_configuration` and `container_configuration` are mutually exclusive in the agent definition: include `code_configuration` for source-code deploy (this article) or `container_configuration` for image-based deploy. See [Deploy a hosted agent (container)](deploy-hosted-agent.md) for the image variant.

### Create the agent

```bash
curl -X POST "$ENDPOINT/agents?api-version=$API_VERSION" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Accept: application/json" \
  -H "Foundry-Features: CodeAgents=V1Preview,HostedAgents=V1Preview" \
  -H "x-ms-agent-name: $AGENT" \
  -H "x-ms-code-zip-sha256: $SHA" \
  -F "metadata=@metadata.json;type=application/json" \
  -F "code=@$ZIP;type=application/zip;filename=$AGENT.zip"
```

`x-ms-agent-name` is required only on the Create call. The name must start and end with alphanumeric characters, can contain hyphens in the middle, and must not exceed 63 characters. The response includes an initial `status` of `creating`.

### Poll for active

```bash
while true; do
  STATUS=$(curl -s -H "Authorization: Bearer $TOKEN" \
    -H "Foundry-Features: CodeAgents=V1Preview,HostedAgents=V1Preview" \
    "$ENDPOINT/agents/$AGENT/versions/1?api-version=$API_VERSION" | jq -r '.status')
  echo "Status: $STATUS"
  [ "$STATUS" = "active" ] && break
  [ "$STATUS" = "failed" ] && echo "Provisioning failed." && exit 1
  sleep 5
done
```

| Status | Meaning |
| --- | --- |
| `creating` | Still provisioning. |
| `active` | Ready to invoke. |
| `failed` | Provisioning failed. Inspect the version's `error` object—`error.code` (for example, `ProvisioningError`) and `error.message` summarize the failure. For `remote_build`, `error.message` includes the final restore or compile error line (pip for Python, NuGet for .NET), an exit code, and an `aka.ms` troubleshooting link. (Container log streaming doesn't apply to provisioning failures—the container never starts. Use `error.message` for the cause.) |

### Invoke the agent

Pick the protocol your agent declared in `protocol_versions`.

**Responses protocol:**

```bash
curl -X POST "$ENDPOINT/agents/$AGENT/endpoint/protocols/openai/responses?api-version=v1" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -H "Foundry-Features: CodeAgents=V1Preview,HostedAgents=V1Preview" \
  -d '{"model":"gpt-4.1-mini","input":"Hello, agent!","stream":false}'
```

**Invocations protocol:**

```bash
curl -X POST "$ENDPOINT/agents/$AGENT/endpoint/protocols/invocations?api-version=v1" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -H "Foundry-Features: CodeAgents=V1Preview,HostedAgents=V1Preview" \
  -d '{"input":"Hello, this is a test invocation!"}'
```

Useful response headers:

| Header | Use |
| --- | --- |
| `x-agent-session-id` | Container session ID. Pass to [`:logstream`](#stream-container-logs). Returned even on `424` / `500`. |
| `x-ms-region` | Region that handled the call. Useful when filing support tickets. |

For the Responses protocol, the per-call response identifier is the `id` field in the response JSON body (for example, `caresp_<random>`). Use it to correlate the call with container logs or to reference the call in a support request.

### Ongoing operations

After your first deploy, use these endpoints to evolve and operate the agent.

#### Update or version an agent

To deploy a code change or a definition update, repost the multipart body to the agent resource. The service uses **content-addressable versioning**: a new version is minted only when the zip's SHA-256 or the agent definition actually changes. Identical reposts return the existing latest version.

```bash
curl -X POST "$ENDPOINT/agents/$AGENT?api-version=$API_VERSION" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Foundry-Features: CodeAgents=V1Preview,HostedAgents=V1Preview" \
  -H "x-ms-code-zip-sha256: $SHA" \
  -F "metadata=@metadata.json;type=application/json" \
  -F "code=@$ZIP;type=application/zip;filename=$AGENT.zip"
```

The response is the full agent envelope with `versions.latest` populated. Poll the resulting version as shown in [Poll for active](#poll-for-active).

If your tooling prefers a version-shaped response (a bare `AgentVersionObject` instead of the agent envelope), post the same multipart body to `$ENDPOINT/agents/$AGENT/versions?api-version=$API_VERSION`. The dedup rule is identical—both endpoints share the same content-addressable logic.

#### Download the deployed zip

Verify exactly what's deployed by downloading the zip. Omit `agent_version` to download the latest; pass `agent_version=<n>` to target a specific version.

```bash
VERSION=1

# Latest version
curl -O -J "$ENDPOINT/agents/$AGENT/code:download?api-version=$API_VERSION" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Accept: application/zip" \
  -H "Foundry-Features: CodeAgents=V1Preview,HostedAgents=V1Preview"

# Specific version
curl -O -J "$ENDPOINT/agents/$AGENT/code:download?api-version=$API_VERSION&agent_version=$VERSION" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Accept: application/zip" \
  -H "Foundry-Features: CodeAgents=V1Preview,HostedAgents=V1Preview"
```

Two response headers help you confirm what you downloaded:

| Header | Use |
| --- | --- |
| `x-ms-agent-version` | Version number the service served. When you omit `agent_version`, use this header to learn which version is currently "latest". |
| `x-ms-code-zip-sha256` | SHA-256 the service stored for the uploaded zip. Compare it against your local computation to detect drift between what you expected to deploy and what's deployed. |

Image-based agents return `409 AgentNotCodeBased`.

#### Stream container logs

```bash
curl -N "$ENDPOINT/agents/$AGENT/sessions/<sessionId>:logstream?api-version=$API_VERSION" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Accept: text/event-stream"
```

Logs are delivered as server-sent events. `{sessionId}` is the value of `x-agent-session-id` from the invoke response. Use this endpoint to debug runtime failures and `424 session_not_ready` responses. The log-streaming endpoint doesn't require the `Foundry-Features` preview header.

## Package the zip manually

If you use `azd`, skip this section—`azd` builds the zip for you. Read it if you use the REST API, if you switch to **bundled** dependency resolution, or if you need full control over the upload contents.

The zip must be **flat at the root**—no top-level wrapper folder.

### Python layout (remote build mode)

The service installs dependencies in the cloud from `requirements.txt`.

```text
agent-code.zip
├── main.py
└── requirements.txt
```

### Python layout (bundled mode)

You ship prebuilt Linux dependencies in `packages/`.

```text
agent-code.zip
├── main.py                    # entry point
├── requirements.txt
└── packages/                  # extracted modules (not raw .whl files)
    ├── azure/identity/__init__.py
    └── requests/__init__.py
```

### .NET layout (remote build mode)

Zip the project sources only—no `bin/`, `obj/`, or `publish/` output. Agent Service runs `dotnet restore` and `dotnet publish` for you during provisioning.

```text
agent-code.zip
├── MyAgent.csproj
├── Program.cs
└── ... (additional .cs files)
```

The `entry_point` you set in the agent definition still refers to the published assembly name (for example, `["dotnet", "MyAgent.dll"]`), produced by the server-side publish.

### .NET layout (bundled mode)

Zip the output of `dotnet publish -c Release -r linux-x64 --self-contained false` rooted directly in the zip:

```text
agent-code.zip
├── MyAgent.dll
├── MyAgent.runtimeconfig.json
└── ... (publish output)
```

> [!WARNING]
> Common packaging mistakes that cause `session_creation_failed` or `ModuleNotFoundError`:
> - Wrapping the source in a folder (`my-agent/main.py` instead of `main.py` at the root).
> - Including raw `.whl` files in `packages/` instead of extracted modules.
> - Bundling Windows binaries (`.pyd`, `.dll`) for a Linux runtime.

### Build Linux dependencies locally (bundled, Python)

Use the `manylinux2014_x86_64` platform tag so `pip` downloads Linux wheels even from Windows or macOS.

# [Bash](#tab/bash)

```bash
pip install -r requirements.txt \
    --target packages/ \
    --platform manylinux2014_x86_64 \
    --python-version 3.13 \
    --implementation cp \
    --only-binary=:all:

zip -r agent-code.zip main.py requirements.txt packages/
```

# [PowerShell / Windows cmd](#tab/powershell)

```cmd
pip install -r requirements.txt --target packages --platform manylinux2014_x86_64 --python-version 3.13 --implementation cp --only-binary=:all:

tar -a -c -f agent-code.zip main.py requirements.txt packages
```

---

`--only-binary=:all:` forces wheels (no source builds). The `--python-version` must match the `runtime` value in the agent definition.

### Build .NET output (bundled)

```bash
dotnet publish -c Release -r linux-x64 --self-contained false -o publish/
cd publish && zip -r ../agent-code.zip .
```

Use `--self-contained true` if you want to ship the .NET runtime in the zip. The `runtime` you set in the agent definition must match the `TargetFramework`.

### Limits

| Limit | Value |
| --- | --- |
| Maximum zip size (multipart upload) | 250 MB |

## Troubleshooting

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| `401 Unauthorized` | Missing or wrong-scope token | Acquire a token with `--resource https://ai.azure.com`. |
| `403 Forbidden` | Caller lacks RBAC on the project | Grant **Foundry User** (or higher) at project scope. |
| `409 conflict` on Create (`Agent '<name>' already exists`) | Agent name already exists | Use Update (POST `/agents/{name}`), or pick a new name. |
| `400 bad_request` (`Agent version is still being provisioned`) on invoke | A new version is mid-deploy and the active version is being swapped in | Poll the version `status` until `active`, then retry. |
| `424 session_not_ready` on invoke | Container started but `/readiness` didn't return HTTP 200 within the timeout | Stream logs with [`:logstream`](#stream-container-logs), fix the readiness probe or startup error, redeploy. |
| `409 conflict` on DELETE agent (`Agent has active sessions`) | Open sessions block deletion | Wait for sessions to go idle, or append `&force=true` to cascade-delete sessions. |
| Version stuck in `creating` (>10 min, remote build) | Server build failed or couldn't resolve `requirements.txt` | Switch to `dependency_resolution: bundled` and prebuild locally. |
| `bundled` deployment fails in a private virtual network | Outbound network is blocked, so required packages can't be downloaded | Allow outbound connections in your network policy to the endpoints in the [`bundled` private virtual network prerequisite](#choose-how-dependencies-are-resolved), then redeploy. |
| Version transitions to `failed` | Bad zip layout, syntax error, or (`remote_build`) a restore/compile failure | Read the version's `error` object first—`error.code` classifies the failure and `error.message` contains the underlying restore or compile error line (pip for Python, NuGet for .NET) plus a troubleshooting link. Verify the [folder structure](#package-the-zip-manually). Use [`:logstream`](#stream-container-logs) only after the container starts. |
| `ModuleNotFoundError` at runtime | `packages/` missing, contains raw `.whl` files, or has Windows binaries | Rebuild with `pip install --target packages/ --platform manylinux2014_x86_64 --only-binary=:all:`. |
| `409 AgentNotCodeBased` on download | Agent is image-based | Use the [container-based deploy doc](deploy-hosted-agent.md). |

## Clean up resources

```bash
# Delete one version
curl -X DELETE "$ENDPOINT/agents/$AGENT/versions/1?api-version=$API_VERSION" \
  -H "Authorization: Bearer $TOKEN"

# Delete the agent and all its versions
curl -X DELETE "$ENDPOINT/agents/$AGENT?api-version=$API_VERSION" \
  -H "Authorization: Bearer $TOKEN"

# Force-delete the agent (cascades to any active sessions)
curl -X DELETE "$ENDPOINT/agents/$AGENT?api-version=$API_VERSION&force=true" \
  -H "Authorization: Bearer $TOKEN"
```

If you scaffolded the project from the [Quickstart](../quickstarts/quickstart-hosted-agent.md) with `azd`, run `azd down` from the project root to remove the entire provisioned environment instead.

> [!WARNING]
> Deleting an agent removes all of its versions and terminates active sessions. This action can't be undone.

## Next steps

> [!div class="nextstepaction"]
> [Manage Hosted agent lifecycle](manage-hosted-agent.md)

- [Hosted agent permissions reference](../concepts/hosted-agent-permissions.md)
- [Deploy a hosted agent in a virtual network](virtual-networks.md)

## Related content

- [Deploy a hosted agent (container)](deploy-hosted-agent.md)
- [What are Hosted agents?](../concepts/hosted-agents.md)
- [Hosted agent samples (Python)](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/hosted-agents)
- [Hosted agent samples (.NET)](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/csharp/hosted-agents)
