---
title: "Deploy a hosted agent from source code (preview)"
description: "Deploy your hosted agent directly from source code—without building a container—by using the Azure Developer CLI, Python SDK, .NET SDK, or REST API."
author: aahill
ms.author: aahi
ms.date: 06/04/2026
ms.manager: mcleans
ms.topic: how-to
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.custom: doc-kit-assisted
ai-usage: ai-assisted
#CustomerIntent: As a developer new to Foundry Agent Service, I want to deploy my Python or .NET agent code without building a container so that I can iterate quickly without learning Docker or managing a registry.
---

# Deploy a hosted agent from source code (preview)

This article shows you how to deploy a [Hosted agent](../concepts/hosted-agents.md) in Foundry Agent Service from Python or .NET source code, without building or pushing a container image. You upload a `.zip` of your code (and optionally your dependencies), and Agent Service either runs it as-is or builds your dependencies for you in the cloud.

> [!TIP]
> For most scenarios, deploy with the **Azure Developer CLI (azd)** or the **Foundry Toolkit for VS Code**. These tools do the heavy lifting for you: they package your source, upload it, poll for `active`, and configure role-based access control automatically. To get started, follow the [Quickstart: Deploy your first hosted agent](../quickstarts/quickstart-hosted-agent.md) and choose **Code** (or **Source Code (ZIP upload)**) when prompted for a deployment method.

Use the SDK and REST procedures in this article when you need to deploy source-code agents programmatically—from the Python SDK or .NET SDK in your own applications, or directly over the REST API for custom tooling, language-agnostic automation, or integration with existing continuous-delivery systems. In this article, you complete the following tasks:

- Pick a [dependency-resolution mode](#choose-how-dependencies-are-resolved) and package your source.
- Create the agent, wait for it to reach `active`, and invoke it.
- Update, version, download, and stream logs for the deployed agent.

If you need full control of the runtime image or you already have a working Dockerfile, use the container-based path: [Deploy a hosted agent](deploy-hosted-agent.md).

> [!IMPORTANT]
> Source-code deployment for Hosted agents is in **preview**. Functionality, region availability, and APIs might change before general availability.

## Prerequisites

- A [Microsoft Foundry project](../../how-to/create-projects.md) in a supported region.
- [Azure CLI](/cli/azure/install-azure-cli) version 2.80 or later, signed in to the tenant that owns the project.

# [Python](#tab/python)

- `pip` from Python 3.13 or later, to package your source locally.
- The `azure-ai-projects` version 2.2.0 or later and `azure-identity` packages.

    ```bash
    pip install "azure-ai-projects>=2.2.0" azure-identity
    ```

# [C#](#tab/csharp)

- The .NET 10 SDK, to package your source locally.
- The `Azure.AI.Projects.Agents` and `Azure.Identity` packages.

    ```dotnetcli
    dotnet add package Azure.AI.Projects.Agents
    dotnet add package Azure.Identity
    ```

# [REST API](#tab/rest)

- A command-line HTTP client such as `curl` (the REST examples in this article use `curl`).
- To package your source locally, install the toolchain for your agent's language: `pip` from Python 3.13 or later, or the .NET 10 SDK.

---

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

Your agent runs as a platform-assigned managed identity that's separate from your user identity. That identity needs **Foundry User** to call models from inside the container. If you deploy with `azd` or the Foundry Toolkit for Visual Code, the tooling assigns this role automatically. If you deploy with REST, grant it yourself—see [Hosted agent permissions reference](../concepts/hosted-agent-permissions.md).

For REST calls, include the preview feature header on mutating requests (Create, Update, Delete) while the feature is in preview:

```http
Foundry-Features: CodeAgents=V1Preview,HostedAgents=V1Preview
```

GET requests work without it today, but include it on every call to be safe—the header gates preview behavior and might be enforced more strictly before GA.

## Deployment lifecycle

Every source-code deployment follows the same sequence: **package → create or update → poll until `active` → invoke**. The source-code path uses `code_configuration` in the agent definition; the image-based path uses `container_configuration` instead—the two are mutually exclusive on a single version.

Choose the path that fits your workflow. If you're not sure, start with the Azure Developer CLI or VS Code—it's the recommended path for most customers.

| Path | Best for | Packaging |
| --- | --- | --- |
| [Azure Developer CLI or VS Code](#deploy-using-the-azure-developer-cli-or-vs-code) | **Most deployments**, including first deployments and the fastest inner loop. | Tooling builds and uploads the zip for you. |
| [Python SDK](#deploy-from-source-code) | Programmatic deployment from Python apps or automation. | You build the zip; the SDK uploads it. |
| [.NET SDK](#deploy-from-source-code) | Programmatic deployment from .NET apps or automation. | The SDK zips a folder for you. |
| [REST API](#deploy-from-source-code) | Custom tooling, language-agnostic automation, and CD systems. | You build the zip and send the multipart request. |

## Choose how dependencies are resolved

Before you start, pick a value for `code_configuration.dependency_resolution`. This choice affects what you put in the zip.

| Value | Behavior | Use when |
| --- | --- | --- |
| `remote_build` | Agent Service installs dependencies from `requirements.txt` (Python) or restores the project file (.NET) during provisioning. | You want a small upload and the simplest inner loop. **Recommended for first-time users.** |
| `bundled` | The zip is run as-is. You ship prebuilt Linux dependencies in `packages/` (Python) or `dotnet publish` output (.NET). | You need reproducible builds, your dependencies are private or wheels-only, or your project doesn't restore cleanly server-side. |

For bundled mode, see [Package the zip manually](#package-the-zip-manually) for the local build commands.

## Deploy using the Azure Developer CLI or VS Code

The Azure Developer CLI (`azd`) and the Foundry Toolkit for VS Code automate the full source-code deployment lifecycle—they package your source into a zip, compute the SHA-256, upload it, poll for `active`, and configure role-based access control for you. These tools are the recommended path for most customers, and the fastest inner loop.

For a step-by-step walkthrough, see the [Quickstart: Deploy your first hosted agent](../quickstarts/quickstart-hosted-agent.md). Choose **Code** (or **Source Code (ZIP upload)**) when the quickstart asks for a deployment method.

### Select source-code deployment

When you run `azd ai agent init` interactively, the tool prompts you to choose a deployment mode. Choose **code** to deploy from source as a ZIP upload instead of building a container image. The Foundry Toolkit for VS Code prompts you for the deployment method in the same way.

To select source-code deployment non-interactively—for example, in a CI/CD pipeline—pass `--deploy-mode code`. This mode requires `--runtime` and `--entry-point`, and accepts an optional `--dep-resolution` value of `remote_build` (default) or `bundled`:

```azurecli
azd ai agent init --no-prompt --project-id "<project-resource-id>" \
  --deploy-mode code --runtime python_3_13 --entry-point main.py
```

With `--no-prompt`, the deployment mode defaults to `container`, so pass `--deploy-mode code` explicitly for source-code deployments. After initialization, run `azd up` to provision and deploy.

Use the SDK or REST paths in the following sections when you need to deploy programmatically from your own application or integrate with existing tooling.

## Deploy from source code

Select your language or interface. Each tab walks through the same lifecycle: create the agent, poll until it reaches `active`, invoke it, and download the deployed code.

# [Python](#tab/python)

Use the Python SDK to deploy source-code agents from your own applications or automation. You build the zip yourself and pass its bytes and SHA-256 to the SDK, which uploads it and exposes the same create, poll, invoke, and download operations as the REST API. Code-deployment requires `azure-ai-projects` version 2.2.0 or later.

Source-code deployment uses the preview `beta` client surface, so create the client with `allow_preview=True`.

### Build the zip

The Python SDK uploads a zip that you build. Use the same layout and dependency-resolution rules described in [Package the zip manually](#package-the-zip-manually). The minimal `remote_build` payload is a flat zip with `main.py` and `requirements.txt` at the root.

### Create the agent

```python
import hashlib
from pathlib import Path

from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    CodeConfiguration,
    CreateAgentVersionFromCodeContent,
    CreateAgentVersionFromCodeMetadata,
    HostedAgentDefinition,
    ProtocolVersionRecord,
)
from azure.identity import DefaultAzureCredential

# Format: "https://<account>.services.ai.azure.com/api/projects/<project>"
PROJECT_ENDPOINT = "your_project_endpoint"
AGENT_NAME = "my-code-agent"
ZIP_PATH = Path("agent-code.zip")

code_zip_bytes = ZIP_PATH.read_bytes()
code_zip_sha256 = hashlib.sha256(code_zip_bytes).hexdigest()

credential = DefaultAzureCredential()
project = AIProjectClient(
    endpoint=PROJECT_ENDPOINT,
    credential=credential,
    allow_preview=True,
)

content = CreateAgentVersionFromCodeContent(
    metadata=CreateAgentVersionFromCodeMetadata(
        description="Hello-world code agent",
        definition=HostedAgentDefinition(
            cpu="1",
            memory="2Gi",
            code_configuration=CodeConfiguration(
                runtime="python_3_13",
                entry_point=["python", "main.py"],
                dependency_resolution="remote_build",
            ),
            protocol_versions=[
                ProtocolVersionRecord(protocol="responses", version="1.0.0")
            ],
            environment_variables={"AZURE_AI_MODEL_DEPLOYMENT_NAME": "gpt-4.1-mini"},
        ),
    ),
    code=(ZIP_PATH.name, code_zip_bytes, "application/zip"),
)

created = project.beta.agents.create_version_from_code(
    agent_name=AGENT_NAME,
    content=content,
    code_zip_sha256=code_zip_sha256,
)
print(f"Created version: {created.version}")
```

For the Invocations protocol, set the `protocol_versions` entry to `ProtocolVersionRecord(protocol="invocations", version="1.0.0")`. For `bundled` mode, set `dependency_resolution="bundled"` and ship prebuilt dependencies in the zip—see [Build Linux dependencies locally](#build-linux-dependencies-locally-bundled-python).

### Poll for active

The code-deploy methods (`create_version_from_code` and `download_code`) live on the preview `project.beta.agents` surface, but read and delete operations such as `get_version` are on `project.agents`.

```python
import time

while True:
    version = project.agents.get_version(
        agent_name=AGENT_NAME, agent_version=created.version
    )
    status = version["status"]
    print(f"Status: {status}")
    if status == "active":
        break
    if status == "failed":
        raise RuntimeError(f"Provisioning failed: {version.get('error')}")
    time.sleep(5)
```

See [Poll for active](#poll-for-active) for the full list of status values and how to read the `error` object on failure.

### Invoke the agent

After the version reaches `active`, bind an OpenAI client to the agent endpoint and call it. This example uses the Responses protocol:

```python
openai_client = project.get_openai_client(agent_name=AGENT_NAME)

response = openai_client.responses.create(input="Hello! What can you do?")
print(response.output_text)
```

For the Invocations protocol, call the invoke endpoint directly with a bearer token, as shown in [Invoke the agent](#invoke-the-agent).

### Download the deployed zip

Verify exactly what's deployed by downloading the zip and comparing its SHA-256 against the value you uploaded:

```python
import hashlib
from pathlib import Path

out_path = Path(f"{AGENT_NAME}-{created.version}.zip")
sha = hashlib.sha256()
with open(out_path, "wb") as f:
    for chunk in project.beta.agents.download_code(
        agent_name=AGENT_NAME, agent_version=created.version
    ):
        f.write(chunk)
        sha.update(chunk)

print(f"Downloaded {out_path} (matches upload: {sha.hexdigest() == code_zip_sha256})")
```

For a complete runnable example, see the [Python hosted-agent samples](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/hosted-agents).

# [C#](#tab/csharp)

Use the .NET SDK to deploy source-code agents from your own applications or automation. Unlike the Python and REST paths, the .NET SDK zips a source folder for you—you pass a folder path instead of building the zip yourself.

Source-code deployment is a preview feature. Suppress the `AAIP001` experimental warning and add the preview feature header to every call with a pipeline policy.

### Create the agent

```csharp
using System;
using System.ClientModel.Primitives;
using Azure.AI.Projects.Agents;
using Azure.Identity;

#pragma warning disable AAIP001 // Hosted agents are an experimental preview feature.

// Format: "https://<account>.services.ai.azure.com/api/projects/<project>"
string projectEndpoint = Environment.GetEnvironmentVariable("FOUNDRY_PROJECT_ENDPOINT");

var options = new AgentAdministrationClientOptions();
options.AddPolicy(
    new FeaturePolicy("HostedAgents=V1Preview,CodeAgents=V1Preview"),
    PipelinePosition.PerCall);

var agentsClient = new AgentAdministrationClient(
    endpoint: new Uri(projectEndpoint),
    tokenProvider: new DefaultAzureCredential(),
    options: options);

var agentDefinition = new HostedAgentDefinition(cpu: "1", memory: "2Gi")
{
    Versions = { new ProtocolVersionRecord(ProjectsAgentProtocol.Responses, "1.0.0") },
    CodeConfiguration = new(
        runtime: "dotnet_10",
        entryPoint: ["dotnet", "MyAgent.dll"],
        dependencyResolution: CodeDependencyResolution.RemoteBuild),
};

var metadata = new CreateAgentVersionFromCodeMetadata(agentDefinition);

ProjectsAgentVersion agentVersion = agentsClient.CreateAgentVersionFromCode(
    agentName: "my-code-agent",
    filePath: "./AgentCode",
    metadata: metadata);

Console.WriteLine($"Created version: {agentVersion.Version}");
```

With `remote_build`, point `filePath` at a folder of .NET project sources. Agent Service runs `dotnet restore` and `dotnet publish` for you during provisioning. The `entryPoint` refers to the published assembly name—for example, `["dotnet", "MyAgent.dll"]` for a project named `MyAgent.csproj`.

`FeaturePolicy` is a small `PipelinePolicy` that adds the `Foundry-Features` header to each request:

```csharp
internal class FeaturePolicy(string feature) : PipelinePolicy
{
    private const string FeatureHeader = "Foundry-Features";

    public override void Process(PipelineMessage message, IReadOnlyList<PipelinePolicy> pipeline, int currentIndex)
    {
        message.Request.Headers.Add(FeatureHeader, feature);
        ProcessNext(message, pipeline, currentIndex);
    }

    public override async ValueTask ProcessAsync(PipelineMessage message, IReadOnlyList<PipelinePolicy> pipeline, int currentIndex)
    {
        message.Request.Headers.Add(FeatureHeader, feature);
        await ProcessNextAsync(message, pipeline, currentIndex);
    }
}
```

For the Invocations protocol, change the `Versions` entry to `new ProtocolVersionRecord(ProjectsAgentProtocol.Invocations, "1.0.0")`. For `bundled` mode, set `dependencyResolution: CodeDependencyResolution.Bundled` and point `filePath` at a folder that holds your `dotnet publish` output. See [Build .NET output (bundled)](#build-net-output-bundled).

### Poll for active

```csharp
while (agentVersion.Status != AgentVersionStatus.Active &&
       agentVersion.Status != AgentVersionStatus.Failed)
{
    Thread.Sleep(500);
    agentVersion = agentsClient.GetAgentVersion(
        agentName: agentVersion.Name,
        agentVersion: agentVersion.Version);
}

if (agentVersion.Status != AgentVersionStatus.Active)
{
    throw new InvalidOperationException($"Deployment failed, status: {agentVersion.Status}");
}
```

### Download the deployed code

Download and extract the deployed code to a local directory to verify what's running. The SDK writes the unzipped contents to `path`:

```csharp
agentsClient.DownloadAgentCode(agentName: agentVersion.Name, path: "./downloaded");
Console.WriteLine("Downloaded agent code to ./downloaded");
```

For a complete runnable example, see the [.NET hosted-agent samples](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/csharp/hosted-agents).

# [REST API](#tab/rest)

Use the [REST API](https://ai.azure.com/api-reference/agents) for direct HTTP-based deployments or custom tooling. The sections walk through a first deployment in order: set up variables, build a zip, create the agent, poll until `active`, and invoke it. Update, version, download, and log-streaming endpoints are grouped under [Ongoing operations](#ongoing-operations).

### Set up variables

**Bash**

```bash
ENDPOINT="https://{account}.services.ai.azure.com/api/projects/{project}"
API_VERSION="2025-11-15-preview"
TOKEN=$(az account get-access-token --resource https://ai.azure.com --query accessToken -o tsv)
AGENT=my-code-agent
ZIP=./agent-code.zip
SHA=$(sha256sum "$ZIP" | cut -d' ' -f1)
```

**PowerShell**

```powershell
$Endpoint    = "https://{account}.services.ai.azure.com/api/projects/{project}"
$ApiVersion  = "2025-11-15-preview"
$Token       = az account get-access-token --resource https://ai.azure.com --query accessToken -o tsv
$Agent       = "my-code-agent"
$Zip         = "./agent-code.zip"
$Sha         = (Get-FileHash $Zip -Algorithm SHA256).Hash.ToLower()
```

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
| `failed` | Provisioning failed. Inspect the version's `error` object—`error.code` (for example, `CodeError`) and `error.message` summarize the failure. For `remote_build`, `error.message` includes the final restore or compile error line (pip for Python, NuGet for .NET), an exit code, and an `aka.ms` troubleshooting link. (Container log streaming doesn't apply to provisioning failures—the container never starts. Use `error.message` for the cause.) |

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

---

## Package the zip manually

If you use `azd`, skip this section—`azd` builds the zip for you. Read it if you use the REST API, if you switch to **bundled** dependency resolution, or if you need full control over the upload contents.

The zip must be **flat at the root**—no top-level wrapper folder.

Select the tab for your agent's language.

# [Python](#tab/python)

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

### Build Linux dependencies locally (bundled, Python)

Use the `manylinux2014_x86_64` platform tag so `pip` downloads Linux wheels even from Windows or macOS.

**Bash**

```bash
pip install -r requirements.txt \
    --target packages/ \
    --platform manylinux2014_x86_64 \
    --python-version 3.13 \
    --implementation cp \
    --only-binary=:all:

zip -r agent-code.zip main.py requirements.txt packages/
```

**PowerShell / Windows cmd**

```cmd
pip install -r requirements.txt --target packages --platform manylinux2014_x86_64 --python-version 3.13 --implementation cp --only-binary=:all:

tar -a -c -f agent-code.zip main.py requirements.txt packages
```

`--only-binary=:all:` forces wheels (no source builds). The `--python-version` must match the `runtime` value in the agent definition.

# [C#](#tab/csharp)

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

### Build .NET output (bundled)

```bash
dotnet publish -c Release -r linux-x64 --self-contained false -o publish/
cd publish && zip -r ../agent-code.zip .
```

Use `--self-contained true` if you want to ship the .NET runtime in the zip. The `runtime` you set in the agent definition must match the `TargetFramework`.

# [REST API](#tab/rest)

See the Python or C# tabs. 

---

> [!WARNING]
> Common packaging mistakes that cause `session_creation_failed` or `ModuleNotFoundError`:
> - Wrapping the source in a folder (`my-agent/main.py` instead of `main.py` at the root).
> - Including raw `.whl` files in `packages/` instead of extracted modules.
> - Bundling Windows binaries (`.pyd`, `.dll`) for a Linux runtime.

### Limits

| Limit | Value |
| --- | --- |
| Maximum zip size (multipart upload) | 250 MB |

For the supported `cpu` and `memory` combinations, see [Sandbox sizes](../concepts/hosted-agents.md#sandbox-sizes).

## Troubleshooting

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| `401 Unauthorized` | Missing or wrong-scope token | Acquire a token with `--resource https://ai.azure.com`. |
| `403 Forbidden` | Caller lacks Role Based Access Control on the project | Grant **Foundry User** (or higher) at project scope. |
| `409 conflict` on Create (`Agent '<name>' already exists`) | Agent name already exists | Use Update (POST `/agents/{name}`), or pick a new name. |
| `400 bad_request` (`CPU and Memory must be specified as a valid resource tier`) on Create or Update | `cpu`/`memory` aren't one of the supported tiers | Set `cpu` and `memory` to a valid pair from [Sandbox sizes](../concepts/hosted-agents.md#sandbox-sizes). |
| `400 bad_request` (`Agent version is still being provisioned`) on invoke | A new version is mid-deploy and the active version is being swapped in | Poll the version `status` until `active`, then retry. |
| `424 session_not_ready` on invoke | Container started but `/readiness` didn't return HTTP 200 within the timeout | Stream logs with [`:logstream`](#stream-container-logs), fix the readiness probe or startup error, redeploy. |
| `409 conflict` on DELETE agent (`Agent has active sessions`) | Open sessions block deletion | Wait for sessions to go idle, or append `&force=true` to cascade-delete sessions. |
| Version stuck in `creating` (>10 min, remote build) | Server build failed or couldn't resolve `requirements.txt` | Switch to `dependency_resolution: bundled` and prebuild locally. |
| Version transitions to `failed` | Bad zip layout, syntax error, or (`remote_build`) a restore/compile failure | Read the version's `error` object first—`error.code` classifies the failure and `error.message` contains the underlying restore or compile error line (pip for Python, NuGet for .NET) plus a troubleshooting link. Verify the [folder structure](#package-the-zip-manually). Use [`:logstream`](#stream-container-logs) only after the container starts. |
| `ModuleNotFoundError` at runtime | `packages/` missing, contains raw `.whl` files, or has Windows binaries | Rebuild with `pip install --target packages/ --platform manylinux2014_x86_64 --only-binary=:all:`. |
| `409 AgentNotCodeBased` on download | Agent is image-based | Use the [container-based deploy doc](deploy-hosted-agent.md). |

## Clean up resources

If you scaffolded the project from the [Quickstart](../quickstarts/quickstart-hosted-agent.md) with `azd`, run `azd down` from the project root to remove the entire provisioned environment.

To delete an agent you deployed with the SDK or REST API, use the matching path below.

# [Python](#tab/python)

```python
# Delete one version
project.agents.delete_version(agent_name=AGENT_NAME, agent_version=created.version)

# Delete the agent and all its versions
project.agents.delete(agent_name=AGENT_NAME)
```

# [C#](#tab/csharp)

```csharp
// Delete the agent and all its versions (force cascades to active sessions)
agentsClient.DeleteAgent(agentName: "my-code-agent", force: true);
```

# [REST API](#tab/rest)

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

---

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
