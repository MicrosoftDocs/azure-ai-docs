---
title: "Deploy a hosted agent from source code (preview)"
description: "Deploy your hosted agent directly from source code—without building a container—using the Azure Developer CLI or the REST API."
author: aahill
ms.author: aahi
ms.date: 04/14/2026
ms.manager: nitinme
ms.topic: how-to
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.custom: references_regions, doc-kit-assisted
ai-usage: ai-assisted
#CustomerIntent: As a developer new to Foundry Agent Service, I want to deploy my Python or .NET agent code without building a container so that I can iterate quickly without learning Docker or managing a registry.
---

# Deploy a hosted agent from source code (preview)

This article shows you how to deploy a [Hosted agent](../concepts/hosted-agents.md) in Foundry Agent Service from Python or .NET source code, without building or pushing a container image. You upload a `.zip` of your code (and optionally your dependencies), and Agent Service either runs it as-is or builds your dependencies for you in the cloud.

In this article, you complete the following tasks:

- Pick a deployment method (Foundry Toolkit for VS Code, Azure Developer CLI, or REST API) and a dependency-resolution mode.
- Create the agent, wait for it to reach `active`, and invoke it.
- Iterate by deploying new versions.

Use this approach when you don't require full control of the operating system or a container registry. If you need full control of the runtime image or you already have a working Dockerfile, use the container-based path: [Deploy a hosted agent](deploy-hosted-agent.md).

> [!IMPORTANT]
> Source-code deployment for Hosted agents is in **preview**. Functionality, region availability, and APIs might change before general availability.

## Prerequisites

- A [Microsoft Foundry project](../../how-to/create-projects.md) in a supported region.
- [Azure CLI](/cli/azure/install-azure-cli) version 2.80 or later, signed in to the tenant that owns the project.
- For the azd path: the [Azure Developer CLI](/azure/developer/azure-developer-cli/) and the `azure.ai.agents` extension (installed in the [Install the azd extension](#install-the-azd-extension) step).
- For the VS Code path: [Visual Studio Code](https://code.visualstudio.com/) and the [Foundry Toolkit for VS Code](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio) extension.
- For local Python packaging: `pip` from Python 3.13 or later.
- For local .NET packaging: the .NET 10 SDK.

### Supported regions

Source-code deployment is enabled in the following regions during preview. Your Foundry project must live in one of these regions; requests against projects in other regions return `404` or capability errors.

- North Central US
- Canada Central

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

You need **Azure AI Project Manager** at project scope to deploy a Hosted agent. This role grants the data-plane permissions to create and update agents, plus the ability to assign **Azure AI User** to the platform-created agent identity that your running code uses to call models and tools.

Your agent runs as a platform-assigned managed identity that's separate from your user identity. That identity needs **Azure AI User** to call models from inside the container. If you deploy with `azd` or the Visual Studio Code Foundry extension, the tooling assigns this role automatically. If you deploy with REST, grant it yourself—see [Hosted agent permissions reference](../concepts/hosted-agent-permissions.md).

For REST calls, include the preview feature header on every request:

```http
Foundry-Features: CodeAgents=V1Preview,HostedAgents=V1Preview
```

## Choose a deployment method

This article covers three deployment methods. Pick the one that matches your scenario:

| Method | Best for | What you do |
| --- | --- | --- |
| [Foundry Toolkit for VS Code](#deploy-by-using-the-foundry-toolkit-for-vs-code) | VS Code users who want a guided, in-editor flow with a built-in playground. | Open the source folder, run a Command Palette command, and answer the prompts. The extension handles packaging, upload, and polling. |
| [Azure Developer CLI (azd)](#deploy-by-using-the-azure-developer-cli) | First-time users on the command line, local inner loop, CI pipelines. | Run `azd ai agent init` and `azd deploy`. `azd` packages your source, handles the upload, polls for `active`, and configures role-based access control. |
| [REST API](#deploy-by-using-the-rest-api) | Custom tooling, language-agnostic automation, integration with existing CD systems. | Build the zip yourself, send a `multipart/form-data` request, and poll for status. |

Every deployment, regardless of method, follows the same lifecycle: **package → create or update → poll until `active` → invoke**.

## Choose how dependencies are resolved

Both deployment methods ask you to pick a value for `code_configuration.dependency_resolution`. Make this choice before you start; it affects what you put in the zip.

| Value | Behavior | Use when |
| --- | --- | --- |
| `remote_build` | Agent Service installs dependencies from `requirements.txt` (Python) or restores the project file (.NET) during provisioning. | You want a small upload and the simplest inner loop. **Recommended for first-time users.** |
| `bundled` | The zip is run as-is. You ship prebuilt Linux dependencies in `packages/` (Python) or `dotnet publish` output (.NET). | You need reproducible builds, your dependencies are private or wheels-only, or your project doesn't restore cleanly server-side. |

For bundled mode, see [Package the zip manually](#package-the-zip-manually) for the local build commands.

## Deploy by using the Foundry Toolkit for VS Code

The [Foundry Toolkit for VS Code](https://marketplace.visualstudio.com/items?itemName=ms-windows-ai-studio.windows-ai-studio) extension wraps the same management APIs as `azd` and adds an in-editor flow: it packages the open folder, uploads it, polls for `active`, and opens the Hosted Agent Playground when the version is ready.

### Quickstart: deploy and invoke

1. **Open the source folder.** In VS Code, open the folder that contains your `main.py` (Python) or `.csproj` (.NET) at the root.

1. **Run the deploy command.** Open the Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`) and run **Foundry Toolkit: Deploy Hosted Agent**. 

1. **Answer the prompts.** Use the following values for a hello-world agent.

   | Prompt | Value |
   | --- | --- |
   | Deployment method | **Code** |
   | Package mode | **Remote package** (service builds dependencies) or **Local package** (bundle locally). Matches [Choose how dependencies are resolved](#choose-how-dependencies-are-resolved). |
   | Preparation mode (Local package only) | **No, prepare for me**—the extension runs `pip install` or `dotnet publish` before upload. **Yes, upload as-is**—the extension uploads the folder unchanged. |
   | Runtime | **Python 3.13**, **Python 3.14**, or **.NET 10**. For .NET, the extension reads `TargetFramework` from `.csproj` and shows it as **Detected** when it matches a supported runtime. |
   | Entry point | For example, `python main.py` or `dotnet MyAgent.dll`. |
   | CPU / memory | Defaults to 0.5 cores / 1 Gi (fine for hello-world). |

1. **Wait for deployment to finish.** The extension polls until the version reaches `active`, then opens the Hosted Agent Playground.

1. **Invoke the agent** from the playground to verify the deployed version.

To redeploy after a code change, rerun the same command. Each deploy creates a new version using the same content-addressable dedup rules as the REST API.

## Deploy by using the Azure Developer CLI

The [Azure Developer CLI (azd)](/azure/developer/azure-developer-cli/) `azure.ai.agents` extension supports source-code deploy. `azd` handles packaging, the multipart upload, version polling, and RBAC for you. This is the recommended path for first-time users.

### Install the azd extension

```bash
azd ext install azure.ai.agents
azd ext show azure.ai.agents
```

### Quickstart: scaffold, deploy, and invoke

Follow these steps from an empty working directory.

1. **Scaffold the project.**

   ```bash
   azd ai agent init
   ```

1. **Answer the prompts.** Use the following values for a hello-world agent.

   | Prompt | Value |
   | --- | --- |
   | Language | **Python** or **C#** |
   | Template | **Hello World** (Invocations or Responses) |
   | Deploy mode | **Source Code (ZIP upload)** |
   | Runtime | for example, **Python 3.13** or **.NET 10** |
   | Entry point | For Python: the entry script, for example `main.py`. For .NET: the published assembly name, for example `MyAgent.dll`. |
   | Dependency resolution | **Remote build** (recommended) or **Bundled**. See [Choose how dependencies are resolved](#choose-how-dependencies-are-resolved). |
   | Resources | 0.5 cores / 1 Gi |

   The generated `agent.yaml` contains a `code_configuration` block (no `image:` field), and `azure.yaml` declares `language: python` or `language: csharp` (no `docker:` block). For Python, `agent.yaml` stores the entry point as `entry_point: ["python", "main.py"]`; for .NET, it's `entry_point: ["dotnet", "MyAgent.dll"]` — `azd` writes the full command for you.

1. **Provision and deploy.** From the project root:

   ```bash
   azd up
   ```

   `azd up` provisions the underlying resources (if needed), packages your source, uploads it, polls for `active`, and prints the agent endpoint. Subsequent code changes only need `azd deploy <service-name>`.

1. **Invoke the agent.**

   ```bash
   azd ai agent invoke "Hello"
   ```

1. **Iterate.** Edit your source, then rerun `azd deploy <service-name>`. Each deploy creates a new version that becomes the live endpoint when it reaches `active`.

### Switch dependency resolution after scaffolding

To switch between **remote build** and **bundled** dependency resolution, edit the `code_configuration.dependency_resolution` field in your service's `agent.yaml` and rerun `azd deploy`. For bundled mode, install Linux wheels into the source directory before redeploying—see [Build Linux dependencies locally (bundled, Python)](#build-linux-dependencies-locally-bundled-python).

## Deploy by using the REST API

Use the REST API for direct HTTP-based deployments or custom tooling. The sections below walk through a first deployment in order: set up variables, build a zip, create the agent, poll until `active`, and invoke it. Update, version, download, and log-streaming endpoints are grouped under [Ongoing operations](#ongoing-operations).

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

Before you call Create, build a flat zip with three files. This is the minimum payload Agent Service accepts for a Python `remote_build` deployment.

```text
agent-code.zip
├── main.py            # your agent loop (uses azure.ai.agentserver)
├── requirements.txt   # dependencies (azure-ai-agentserver, azure-identity, ...)
└── metadata.json      # the agent definition (see "Metadata example" below)
```

`metadata.json` lives next to the zip on your local disk; it isn't part of the zip itself. For full layouts (including `bundled` mode and .NET), see [Package the zip manually](#package-the-zip-manually). For working source files, see the [Python](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/hosted-agents) and [.NET](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/csharp/hosted-agents) samples.

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

The `x-ms-code-zip-sha256` header is an integrity check: the service rejects requests whose computed SHA-256 doesn't match the supplied value. Always include it.

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
      "MODEL_DEPLOYMENT_NAME": "gpt-4.1-mini"
    }
  }
}
```

For the Invocations protocol, replace the `protocol_versions` entry with `{ "protocol": "invocations", "version": "1.0.0" }`. For `bundled` mode, set `"dependency_resolution": "bundled"` and follow [Build Linux dependencies locally](#build-linux-dependencies-locally-bundled-python).

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

`x-ms-agent-name` is required only on the Create call. It accepts up to 63 characters of alphanumerics and hyphens. The response includes an initial `status` of `creating`.

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
| `failed` | Provisioning failed. Inspect the version's `error.message` field—for `remote_build`, it contains the full server-side build log. You can also [stream container logs](#stream-container-logs) once the container starts. |

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
| `x-agent-response-id` | Per-call response ID for the Responses protocol. Include when filing bugs. |
| `x-agent-version-resolved` | Numeric version that handled the request. |

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

If your tooling prefers a version-shaped response (a bare `AgentVersionObject` instead of the agent envelope), post the same multipart body to `$ENDPOINT/agents/$AGENT/versions?api-version=$API_VERSION`. The dedup rule is identical — both endpoints share the same content-addressable logic.

#### Download the deployed zip

Verify exactly what's deployed by downloading the zip for a version:

```bash
curl -O -J "$ENDPOINT/agents/$AGENT/code:download?api-version=$API_VERSION" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Accept: application/zip" \
  -H "Foundry-Features: CodeAgents=V1Preview,HostedAgents=V1Preview"
```

The response header `x-ms-code-zip-sha256` echoes the SHA-256 of the uploaded zip—verify it matches your local computation.

Use `/agents/{agent}/versions/{version}/code:download` to download a specific version. Image-based agents return `409 AgentNotCodeBased`.

#### Stream container logs

```bash
curl -N "$ENDPOINT/agents/$AGENT/sessions/<sessionId>:logstream?api-version=$API_VERSION" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Accept: text/event-stream" \
  -H "Foundry-Features: CodeAgents=V1Preview,HostedAgents=V1Preview"
```

Logs are delivered as server-sent events. `{sessionId}` is the value of `x-agent-session-id` from the invoke response. Use this endpoint to debug runtime failures and `424 session_not_ready` responses.

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

## Known preview limitations

- **Region scope.** Source-code deployment is limited to the [supported regions](#supported-regions) listed in Prerequisites.
- **Zip size.** The multipart upload is capped at 250 MB.
- **Private networking parity.** Source-code deploy follows the same network constraints as container-based Hosted agents. For details, see [Limitations](virtual-networks.md#limitations).

## Troubleshooting

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| `401 Unauthorized` | Missing or wrong-scope token | Acquire a token with `--resource https://ai.azure.com`. |
| `403 Forbidden` | Caller lacks RBAC on the project | Grant **Azure AI User** (or higher) at project scope. |
| `404` on the project endpoint | Project not in a supported region | Use a project in [North Central US or Canada Central](#supported-regions). |
| `409 Conflict` on Create | Agent name already exists | Use Update, or pick a new name. |
| Version stuck in `creating` (>10 min, remote build) | Server build failed or couldn't resolve `requirements.txt` | Switch to `dependency_resolution: bundled` and prebuild locally. |
| Version transitions to `failed` | Bad zip layout, syntax error, or (`remote_build`) a restore/compile failure | Inspect the version's `error.message` field first—for `remote_build`, it contains the full server-side build log (NuGet restore output for .NET, `pip` output for Python). Verify the [folder structure](#package-the-zip-manually). Use [`:logstream`](#stream-container-logs) only after the container starts. |
| `424 session_not_ready` on first invoke | Container still warming | Retry with backoff. If it persists, stream logs. |
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
```

With `azd`, run `azd down` to remove the entire provisioned environment.

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
