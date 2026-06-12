---
title: "Deploy a hosted agent"
description: "Deploy your containerized agent code to Foundry Agent Service using the Python SDK or REST API."
author: aahill
ms.author: aahi
ms.date: 06/12/2026
ms.manager: mcleans
ms.topic: how-to
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.custom: references_regions, doc-kit-assisted
ai-usage: ai-assisted
---

# Deploy a hosted agent

This article shows you how to deploy a containerized agent to Foundry Agent Service using the Python SDK or REST API. Use these approaches when you want to manage agent deployments directly from your own applications or services.

If you're deploying for the first time or want the fastest path, use the [Quickstart: Create and deploy a Hosted agent](../quickstarts/quickstart-hosted-agent.md) instead. The quickstart uses the **Azure Developer CLI (azd)** or **VS Code extension**, which handle building, pushing, versioning, and RBAC configuration automatically.

> [!TIP]
> Prefer a Docker-less inner loop? You can also [deploy a hosted agent directly from source code (preview)](deploy-hosted-agent-code.md) — upload a `.zip` of your Python or .NET code and the platform builds and hosts it for you.

## Deployment lifecycle

Every Hosted agent deployment follows this sequence:

1. **Build and push** — Package your agent code into a container image and push it to Azure Container Registry.
1. **Create an agent version** — Register the image with Foundry Agent Service. The platform provisions infrastructure and creates a dedicated Entra agent identity.
1. **Poll for status** — Wait for the version status to reach `active`.
1. **Invoke** — Send requests to the agent's dedicated endpoint.

## Prerequisites

* A [Microsoft Foundry project](../../how-to/create-projects.md).
* Agent code using a [supported framework](../concepts/hosted-agents.md#language-support).
* [Docker Desktop](https://docs.docker.com/get-docker/) installed for local container development.
* [Azure CLI](/cli/azure/install-azure-cli) version 2.80 or later.

### Required permissions

You need **Foundry Project Manager** at project scope to create and deploy Hosted agents. This role includes both the data plane permissions to create agents and the ability to assign the **Foundry User** role to the platform-created agent identity. The agent identity needs **Foundry User** on the project to access models and artifacts at runtime.

[!INCLUDE [role-rename-note](../../includes/role-rename-note.md)]

If you use `azd` or the VS Code extension, the tooling handles most RBAC assignments automatically, including:

- **Container Registry Repository Reader** for the project managed identity (image pulls)
- **Foundry User** for the platform-created agent identity (runtime model and tool access)

> [!NOTE]
> * The platform creates a dedicated Entra agent identity for each Hosted agent at deploy time. This identity is a service principal that your running container uses to call models and tools. You don't need to configure managed identities manually. However, the user who creates the agent must have permission to assign **Foundry User** to that identity—which is why **Foundry Project Manager** is recommended over **Foundry User** alone.
> * While `azd` and VS Code extensions handle basic RBAC assignments automatically, complex scenarios may require additional manual configuration. For comprehensive details about all permissions and role assignments involved, see [Hosted agent permissions reference](../concepts/hosted-agent-permissions.md).

For more information, see [Authentication and authorization](../../concepts/authentication-authorization-foundry.md).

> [!IMPORTANT]
> The Azure Container Registry that holds your Hosted agent's container image must currently be reachable over its public endpoint. Placing the registry behind a private network (private endpoint with public network access disabled) isn't currently supported for Hosted agents — the platform can't pull the image. For the full list of network constraints, see [Limitations](virtual-networks.md#limitations).

## Container requirements

Your container image must meet the following requirements to run on the Hosted agent platform.

> [!IMPORTANT]
> The hosting platform requires x86_64 (linux/amd64) container images. If you build on Apple Silicon or other ARM-based machines, use `docker build --platform linux/amd64 .` to avoid producing an incompatible ARM image.

### Protocol libraries

Hosted agents communicate with the Foundry gateway through protocol libraries. Choose the protocol that matches your agent's interaction pattern:

| Protocol | Python library | .NET library | Endpoint | Best for |
| ---------- | --------------- | -------------- | ---------- | ---------- |
| **Responses** | `azure-ai-agentserver-responses` | `Azure.AI.AgentServer.Responses` | `/responses` | Conversational chatbots, streaming, multi-turn with platform-managed history |
| **Invocations** | `azure-ai-agentserver-invocations` | `Azure.AI.AgentServer.Invocations` | `/invocations` | Webhook receivers, non-conversational processing, custom async workflows |
| **Invocations (WebSocket)** | `azure-ai-agentserver-invocations` | `Azure.AI.AgentServer.Invocations` | `/invocations_ws` | Bidirectional streaming: real-time voice agents, interactive media |

The WebSocket protocol uses the identifier `invocations_ws` and ships in the same `azure-ai-agentserver-invocations` package as the HTTP `/invocations` route, so one container can serve both. Use it when you need persistent, full-duplex streaming—for example, sending microphone PCM to the agent and receiving synthesized audio back. For voice scenarios, see [Build a voice agent with hosted agents](build-voice-agent.md).

> [!IMPORTANT]
> The `invocations_ws` WebSocket protocol is in preview and is currently available only in **North Central US**.

A single container can expose **multiple protocols simultaneously** by declaring them when you create the agent — in the `agent.yaml` file, SDK call, or REST API request — and importing the required libraries. Use the protocol libraries within your existing framework, whether that’s Microsoft Agent Framework, LangChain, or custom code.
<!--
> [!TIP]
> If you already have a Hosted agent that uses the **Responses** or **Invocations** protocol and you want to add real-time voice interaction without rewriting it as a WebSocket agent, see [Use Voice Live with hosted agents](../../../ai-services/speech-service/how-to-voice-live-hosted-agent-integration.md).
-->
### Responses protocol library

The Python and .NET libraries for the Responses protocol implement the Azure AI Responses API. Import the package and implement the `IResponseHandler` interface. The library handles routing, streaming with server-sent events (SSE), background execution, cancellation, caching, and response lifecycle management.

#### IResponseHandler

`IResponseHandler` is the core abstraction you implement. The library calls `CreateAsync` for each incoming request and delivers the returned `IAsyncEnumerable<ResponseStreamEvent>` to clients through SSE:

```csharp
public class EchoHandler : ResponseHandler
{
    public override IAsyncEnumerable<ResponseStreamEvent> CreateAsync(
        CreateResponse request,
        ResponseContext context,
        CancellationToken cancellationToken)
    {
        return new TextResponse(context, request,
            createText: async ct =>
            {
                var input = await context.GetInputTextAsync(cancellationToken: ct);
                return $"Echo: {input}";
            });
    }
}
```

#### ResponseEventStream

`ResponseEventStream` manages `sequenceNumber`, `outputIndex`, `contentIndex`, `itemId`, and the full `Response` lifecycle automatically. Each `yield return` maps one-to-one to an SSE event, so you don't need to track this state yourself.

#### Streaming and background modes

- **Streaming mode** (default): SSE events are delivered in real time to the connected client.
- **Background mode**: The handler runs to completion without a connected SSE client. Events are buffered and available for replay through `GET /responses/{id}`.

#### Response lifecycle

The library orchestrates the complete response lifecycle: `created` → `in_progress` → `completed` (or `failed` or `cancelled`). The library also manages cancellation, error handling, and terminal event guarantees automatically.

#### Thread safety

All service instances registered through `AddResponsesServer()` are thread-safe. Handler instances are scoped per-request.

For detailed handler implementation guidance, see the [handler implementation guide](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/agentserver/Azure.AI.AgentServer.Responses/docs/handler-implementation-guide.md). For runnable examples, see the [Responses protocol samples](https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/agentserver/Azure.AI.AgentServer.Responses/samples).

### Health endpoints

The protocol libraries automatically expose a `/readiness` endpoint for platform health checks. You don't need to implement this yourself.

### Port

Containers serve traffic on port **8088** locally. In production, the Foundry gateway handles routing — your container doesn't need to expose a public port.

### Platform-injected environment variables

The Hosted agent platform automatically injects environment variables into your container at runtime. Your code can read these without declaring them in `agent.yaml` or `environment_variables`. The `FOUNDRY_*` prefix is reserved for platform use.

| Variable | Purpose |
|----------|---------|
| `FOUNDRY_PROJECT_ENDPOINT` | Foundry project endpoint URL |
| `FOUNDRY_PROJECT_ARM_ID` | Foundry project ARM resource ID |
| `FOUNDRY_AGENT_NAME` | Name of the running agent |
| `FOUNDRY_AGENT_VERSION` | Version of the running agent |
| `FOUNDRY_AGENT_SESSION_ID` | Session ID for the current request (hosted containers only) |
| `APPLICATIONINSIGHTS_CONNECTION_STRING` | Application Insights connection string for telemetry |

Don't redeclare platform-injected variables in `agent.yaml`—they're set automatically.

Variables that you declare yourself, such as `MODEL_DEPLOYMENT_NAME` or toolbox MCP endpoints, go in the `environment_variables` section of `agent.yaml` or the SDK `create_version` call.

> [!IMPORTANT]
> When you deploy your hosted agent to Foundry Agent Service, the platform automatically injects an Application Insights connection string into your agent container as an environment variable, enabling OpenTelemetry tracing by default. To view distributed traces, requests, and dependencies, open the Application Insights resource provisioned during setup in the Azure portal and navigate to Investigate > Transaction search or Performance. Use `azd ai agent monitor` for live console logs.  When AppInsights is enabled, this project logs traces to help monitor and evaluate user level interactions with agents. Project members provided with Log Analytics Reader role in AppInsights will be able to view trace data, which may contain personal data and/or Customer Content. Review what trace data is collected and who may view and use this data.  Additional Azure Montior App Insights [pricing](https://azure.microsoft.com/pricing/details/monitor/) might apply. [Learn more](../../observability/concepts/trace-data.md#disable-tracing).

### Reference project connections in environment variables

Instead of hard-coding secrets (API keys, tokens, endpoints) into `agent.yaml` or your image, pull them from a Foundry project connection at sandbox start. Any value in `environment_variables` can be a placeholder expression that the platform resolves before your container starts.

#### Placeholder syntax

A placeholder has the form `${{connections.<name>.<path>}}`, where `<name>` is the connection's resource name (visible in the portal under **Project details** > **Connected resources**) and `<path>` is one of:

| Path | Resolves to |
|------|-------------|
| `credentials.<field>` | A secret field on the connection |
| `target` | The connection's `target` property (for example, an endpoint URL) |
| `metadata.<field>` | A field under the connection's `metadata` |

The field name to use depends on the connection category:

| Connection category | Field name in placeholder |
|---------------------|---------------------------|
| `ApiKey`, `AppInsights` | Always `key`—for example, `credentials.key` |
| `CustomKeys` | The key name you supplied when creating the connection—for example, `credentials.github_token` |

#### Example

First, create a `CustomKeys` connection on the project that holds the secret. See [Add a new connection in Microsoft Foundry](../../how-to/connections-add.md). Then reference it from `agent.yaml`:

```yaml
environment_variables:
  - name: MODEL_DEPLOYMENT_NAME
    value: gpt-5-mini
  - name: GITHUB_TOKEN
    value: ${{connections.agent-secrets.credentials.github_token}}
```

At sandbox start, Foundry resolves the placeholder and injects the resolved value as a plain environment variable. Your code reads it like any other env var:

```python
import os
token = os.environ["GITHUB_TOKEN"]
```

A GET on the agent version returns the literal `${{...}}` text—the resolved secret is never echoed back through the management API.

#### Considerations

- **Create the connection before you deploy the version.** If the connection or the referenced field is missing at sandbox start, the placeholder doesn't resolve and the variable is empty.
- **Secrets are write-only.** GET on a connection returns `credentials: null`. Verify resolution by reading the env var from inside your running container, not by inspecting the connection.
- **Record `CustomKeys` field names yourself.** The management API never echoes them back after creation. Keep them next to your agent source (for example, in IaC templates or alongside `agent.yaml`) so you can construct placeholders later without guessing.
- **Foundry manages the backing secret name.** When you create the connection, Foundry stores the value in Key Vault under a name it chooses — you can't reference a preexisting Key Vault secret by name. To attach your own Key Vault as the backing store, see [Set up a Key Vault connection](../../how-to/set-up-key-vault-connection.md).

## Package and test your agent locally

Before deploying to Foundry, validate your agent works locally using the protocol library. The container serves the same endpoints locally as it does in production.

### Test the Responses protocol

```http
POST http://localhost:8088/responses
Content-Type: application/json

{
    "input": "Where is Seattle?",
    "stream": false
}
```

### Test the Invocations protocol

```http
POST http://localhost:8088/invocations
Content-Type: application/json

{
    "message": "Hello!"
}
```

## Deploy using the Azure Developer CLI or VS Code

The Azure Developer CLI (`azd`) and VS Code extension automate the full deployment lifecycle. For a step-by-step walkthrough, see the [Quickstart: Create and deploy a Hosted agent](../quickstarts/quickstart-hosted-agent.md).

To screen prompts and responses against a content safety policy, [add a content safety guardrail to your agent](add-hosted-agent-guardrails.md).

## Deploy using the Python SDK

Use the SDK when you want to manage agent deployments directly from Python code.

### Additional prerequisites

* [Python 3.10 or later](https://www.python.org/downloads/)
* A container image in [Azure Container Registry](/azure/container-registry/container-registry-get-started-portal)
* **Container Registry Repository Writer** or **AcrPush** role on the container registry (to push images)
* Azure AI Projects SDK version 2.1.0 or later

    ```bash
    pip install "azure-ai-projects>=2.1.0"
    ```

### Build and push your container image

1. Build your Docker image:

    ```bash
    docker build --platform linux/amd64 -t myagent:v1 .
    ```

    See sample Dockerfiles for [Python](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/hosted-agents/agent-framework) and [C#](https://github.com/microsoft-foundry/foundry-samples/blob/main/samples-classic/csharp/getting-started-agents/AgentFramework/AgentsInWorkflows/Dockerfile).

1. Push to Azure Container Registry:

    ```bash
    az acr login --name myregistry
    docker tag myagent:v1 myregistry.azurecr.io/myagent:v1
    docker push myregistry.azurecr.io/myagent:v1
    ```

> [!TIP]
> Use unique image tags instead of `:latest` for reproducible deployments.

### Configure container registry permissions

Grant your project's managed identity access to pull images:

1. In the [Azure portal](https://portal.azure.com), go to your Foundry project resource.

1. Select **Identity** and copy the **Object (principal) ID** under **System assigned**.

1. Assign the **Container Registry Repository Reader** role to this identity on your container registry. See [Azure Container Registry roles and permissions](/azure/container-registry/container-registry-roles).

### Create a hosted agent version

Creating a version triggers the platform to provision the agent automatically. There's no separate start step — the platform builds a container snapshot and makes the agent ready to serve requests.

```python
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import HostedAgentDefinition, ProtocolVersionRecord, AgentProtocol, ContainerConfiguration
from azure.identity import DefaultAzureCredential

# Format: "https://resource_name.services.ai.azure.com/api/projects/project_name"
PROJECT_ENDPOINT = "your_project_endpoint"

# Create project client
credential = DefaultAzureCredential()
project = AIProjectClient(
    endpoint=PROJECT_ENDPOINT,
    credential=credential,
    allow_preview=True,
)

# Create a hosted agent version
agent = project.agents.create_version(
    agent_name="my-agent",
    definition=HostedAgentDefinition(
        protocol_versions=[
            ProtocolVersionRecord(protocol=AgentProtocol.RESPONSES, version="1.0.0")
        ],
        cpu="1",
        memory="2Gi",
        container_configuration=ContainerConfiguration(
            image="your-registry.azurecr.io/your-image:tag"
        ),
        environment_variables={
            "MODEL_DEPLOYMENT_NAME": "gpt-5-mini"
        }
    )
)

print(f"Agent created: {agent.name}, version: {agent.version}")
```

To expose both protocols, pass both in `protocol_versions`:

```python
protocol_versions=[
    ProtocolVersionRecord(protocol=AgentProtocol.RESPONSES, version="1.0.0"),
    ProtocolVersionRecord(protocol=AgentProtocol.INVOCATIONS, version="1.0.0"),
    ProtocolVersionRecord(protocol=AgentProtocol.INVOCATIONS_WS, version="1.0.0"),
],
```

Key parameters:

| Parameter | Description |
| ----------- | ------------- |
| `agent_name` | Unique name (alphanumeric with hyphens, max 63 characters) |
| `container_configuration.image` | Full Azure Container Registry image URL with tag |
| `cpu` | CPU allocation (for example, `"1"`) |
| `memory` | Memory allocation (for example, `"2Gi"`) |
| `protocol_versions` | Protocols the container exposes (`responses`, `invocations`, or both) |

### Poll for version status

After creating a version, poll until the status is `active` before invoking the agent. Provisioning typically takes less than one minute depending on image size.

```python
import time

# Poll until the agent version is active
while True:
    version_info = project.agents.get_version(
        agent_name="my-agent",
        agent_version=agent.version
    )
    status = version_info["status"]
    print(f"Status: {status}")

    if status == "active":
        print("Agent is ready!")
        break
    elif status == "failed":
        print(f"Provisioning failed: {version_info['error']}")
        break

    time.sleep(5)
```

Version status values:

| Status | Description |
| -------- | ------------- |
| `creating` | Infrastructure provisioning in progress |
| `active` | Agent is ready to serve requests |
| `failed` | Provisioning failed — check the `error` field for details |
| `deleting` | Version is being cleaned up |
| `deleted` | Version has been fully removed |

### Invoke the agent

After the version reaches `active` status, use `get_openai_client` to create an OpenAI client bound to the agent's endpoint.

For the **Responses** protocol:

```python
# Create an OpenAI client bound to the agent endpoint
openai_client = project.get_openai_client(agent_name="my-agent")

response = openai_client.responses.create(
    input="Hello! What can you do?",
)

print(response.output_text)
```

For the **Invocations** protocol, call the invocations endpoint directly:

```python
import requests

token = credential.get_token("https://ai.azure.com/.default").token
url = f"{PROJECT_ENDPOINT}/agents/my-agent/endpoint/protocols/invocations"

response = requests.post(url, headers={
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json",
    "Foundry-Features": "HostedAgents=V1Preview"
}, params={"api-version": "v1"}, json={
    "message": "Process this task"
})

print(response.json())
```

For more complete examples, see the [Hosted agent samples](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/hosted-agents).

## Deploy using the REST API

Use the REST API for direct HTTP-based deployments or when integrating with custom tooling.

Before you begin, [build and push your container image](#build-and-push-your-container-image) and [configure container registry permissions](#configure-container-registry-permissions).

### Set up variables

```bash
BASE_URL="https://{account}.services.ai.azure.com/api/projects/{project}"
API_VERSION="v1"
TOKEN=$(az account get-access-token --resource https://ai.azure.com --query accessToken -o tsv)
```

### Create an agent

```bash
curl -X POST "$BASE_URL/agents?api-version=$API_VERSION" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "my-agent",
    "definition": {
      "kind": "hosted",
      "container_configuration": {
        "image": "myacr.azurecr.io/my-agent:v1"
      },
      "cpu": "1",
      "memory": "2Gi",
      "protocol_versions": [
        {"protocol": "responses", "version": "1.0.0"}
      ],
      "environment_variables": {
        "MODEL_DEPLOYMENT_NAME": "gpt-5-mini"
      }
    }
  }'
```

Creating an agent also creates version `1` and triggers provisioning.

To screen prompts and responses against a content safety policy, include a `rai_config` object in the `definition`. See [Add a content safety guardrail to a hosted agent](add-hosted-agent-guardrails.md).

### Poll for version status

Poll the version endpoint until `status` is `active`:

```bash
while true; do
  STATUS=$(curl -s -X GET "$BASE_URL/agents/my-agent/versions/1?api-version=$API_VERSION" \
    -H "Authorization: Bearer $TOKEN" | jq -r '.status')
  echo "Status: $STATUS"
  [ "$STATUS" = "active" ] && echo "Ready!" && break
  [ "$STATUS" = "failed" ] && echo "Provisioning failed." && exit 1
  sleep 5
done
```

### Invoke the agent

Use the agent's dedicated endpoint to send requests. Set `"stream": true` to receive server-sent events.

**Responses protocol:**

```bash
curl -X POST "$BASE_URL/agents/my-agent/endpoint/protocols/openai/responses?api-version=$API_VERSION" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "input": "Hello! What can you do?",
    "store": true
  }'
```

**Invocations protocol:**

```bash
curl -X POST "$BASE_URL/agents/my-agent/endpoint/protocols/invocations?api-version=$API_VERSION" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -H "Foundry-Features: HostedAgents=V1Preview" \
  -d '{
    "message": "Process this task"
  }'
```

### Create a new version

Deploy updated code or configuration by creating a new version:

```bash
curl -X POST "$BASE_URL/agents/my-agent/versions?api-version=$API_VERSION" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "definition": {
      "kind": "hosted",
      "container_configuration": {
        "image": "myacr.azurecr.io/my-agent:v2"
      },
      "cpu": "1",
      "memory": "2Gi",
      "protocol_versions": [
        {"protocol": "responses", "version": "1.0.0"}
      ],
      "environment_variables": {
        "MODEL_DEPLOYMENT_NAME": "gpt-5-mini"
      }
    }
  }'
```

## Clean up resources

To prevent charges, clean up resources when finished. Agent compute is deprovisioned after 15 minutes of inactivity, so there's no cost when an agent isn't serving requests.

### Azure Developer CLI cleanup

```bash
azd down
```

### SDK cleanup

Delete a single version:

```python
project.agents.delete_version(agent_name="my-agent", agent_version=agent.version)
```

Or delete the entire agent and all its versions:

```python
project.agents.delete(agent_name="my-agent")
```

### REST API cleanup

Delete a single version:

```bash
curl -X DELETE "$BASE_URL/agents/my-agent/versions/1?api-version=$API_VERSION" \
  -H "Authorization: Bearer $TOKEN"
```

Or delete the entire agent:

```bash
curl -X DELETE "$BASE_URL/agents/my-agent?api-version=$API_VERSION" \
  -H "Authorization: Bearer $TOKEN"
```

> [!WARNING]
> Deleting an agent removes all its versions and terminates active sessions. This action can't be undone.

## Troubleshooting

Provisioning errors surface on the version object's `error.code` and `error.message` fields. Check the version status after creation to identify issues.

| Error code | HTTP code | Solution |
| ------------ | ----------- | ---------- |
| `image_pull_failed` | 400 | Verify the image URI is correct and the project managed identity has **Container Registry Repository Reader** on the ACR |
| `SubscriptionIsNotRegistered` | 400 | Register the subscription provider |
| `InvalidAcrPullCredentials` | 401 | Fix managed identity or registry RBAC |
| `UnauthorizedAcrPull` | 403 | Provide correct credentials or identity |
| `AcrImageNotFound` | 404 | Correct image name/tag or publish image |
| `RegistryNotFound` | 400/404 | Fix registry DNS or network reachability |

For 5xx errors, contact Microsoft support.

For detailed RBAC requirements and permission troubleshooting, see [Hosted agent permissions reference](../concepts/hosted-agent-permissions.md).

## Next steps

> [!div class="nextstepaction"]
> [Manage Hosted agent lifecycle](manage-hosted-agent.md)

## Related content

- [What are Hosted agents?](../concepts/hosted-agents.md)
- [Add a content safety guardrail to a hosted agent](add-hosted-agent-guardrails.md)
- [Agent identity concepts](../concepts/agent-identity.md)
- [Agent applications](agent-applications.md)
<!-- - [Add voice to a Hosted agent with Voice Live](../../../ai-services/speech-service/how-to-voice-live-hosted-agent-integration.md) -->
- [Azure Container Registry documentation](/azure/container-registry/)
