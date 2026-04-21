---
title: "Manage hosted agents"
description: "View, monitor, and manage hosted agents in Foundry Agent Service by using the REST API, Python SDK, or Azure Developer CLI."
author: aahill
ms.author: aahi
ms.date: 04/09/2026
ms.manager: nitinme
ms.topic: how-to
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ai-usage: ai-assisted
ms.custom: doc-kit-assisted
zone_pivot_groups: hosted-agent-manage-method
---

# Manage hosted agents

This article shows you how to manage hosted agents in Foundry Agent Service. After you [deploy a hosted agent](deploy-hosted-agent.md), you can view its status, create new versions, configure traffic routing, monitor logs, and delete agents when they're no longer needed.

The platform manages the container lifecycle automatically. Compute is provisioned when a request arrives and deprovisioned after the idle timeout (15 minutes). There are no manual start or stop operations.

## Prerequisites

- A [deployed hosted agent](deploy-hosted-agent.md).

:::zone pivot="rest"

- [Azure CLI](/cli/azure/install-azure-cli) version 2.80 or later, authenticated with `az login`.

:::zone-end

:::zone pivot="python"

- Python SDK: `azure-ai-projects>=2.1.0` and `azure-identity`.

:::zone-end

:::zone pivot="azd"

- [Azure Developer CLI](/azure/developer/azure-developer-cli/install-azd) version 1.23.0 or later.
- The Foundry agents extension:

    ```bash
    azd ext install azure.ai.agents
    ```

:::zone-end

:::zone pivot="rest"

## Set up variables

The REST API examples in this article use `az rest` to call the Foundry Agent Service endpoints directly. Set the following variables before running the commands:

```bash
ACCOUNT_NAME="<your-foundry-account-name>"
PROJECT_NAME="<your-project-name>"
AGENT_NAME="<your-agent-name>"
BASE_URL="https://${ACCOUNT_NAME}.services.ai.azure.com/api/projects/${PROJECT_NAME}"
API_VERSION="v1"
RESOURCE="https://ai.azure.com"
```

> [!IMPORTANT]
> The `--resource` parameter is required for all `az rest` calls to Foundry Agent Service data-plane endpoints. Without it, `az rest` can't derive the correct Azure AD audience from the URL and authentication fails.

:::zone-end

## View agents and versions

Use the following commands to list agents and inspect version details.

### List all agents in a project

:::zone pivot="rest"

```bash
az rest --method GET \
    --url "${BASE_URL}/agents?api-version=${API_VERSION}" \
    --resource "${RESOURCE}"
```

:::zone-end

:::zone pivot="python"

```python
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

project = AIProjectClient(
    endpoint=PROJECT_ENDPOINT,
    credential=DefaultAzureCredential(),
)

for agent in project.agents.list():
    print(agent.name)
```

:::zone-end

:::zone pivot="azd"

```bash
azd ai agent show
```

> [!NOTE]
> `azd ai agent show` reads the agent name and version from the `azd` service entry in your project configuration.

:::zone-end

### Get agent details

:::zone pivot="rest"

```bash
az rest --method GET \
    --url "${BASE_URL}/agents/${AGENT_NAME}?api-version=${API_VERSION}" \
    --resource "${RESOURCE}"
```

The response includes the agent's latest version, status, and definition.

:::zone-end

:::zone pivot="python"

```python
agent = project.agents.get(agent_name="my-agent")
print(f"Name: {agent.name}")
print(f"Status: {agent.versions['latest']['status']}")
```

:::zone-end

:::zone pivot="azd"

```bash
azd ai agent show
```

:::zone-end

### Get a specific version

:::zone pivot="rest"

```bash
az rest --method GET \
    --url "${BASE_URL}/agents/${AGENT_NAME}/versions/1?api-version=${API_VERSION}" \
    --resource "${RESOURCE}"
```

:::zone-end

:::zone pivot="python"

```python
agent_version = project.agents.get_version(
    agent_name="my-agent", agent_version="1"
)
print(f"Version: {agent_version.version}")
print(f"Status: {agent_version['status']}")
```

:::zone-end

:::zone pivot="azd"

Version information is included in the output of `azd ai agent show`.

:::zone-end

### List all versions of an agent

:::zone pivot="rest"

```bash
az rest --method GET \
    --url "${BASE_URL}/agents/${AGENT_NAME}/versions?api-version=${API_VERSION}" \
    --resource "${RESOURCE}"
```

:::zone-end

:::zone pivot="python"

```python
for version in project.agents.list_versions(agent_name="my-agent"):
    print(f"Version: {version.version}, Status: {version['status']}")
```

:::zone-end

:::zone pivot="azd"

Version information is included in the output of `azd ai agent show`.

:::zone-end

### Create a new version

Create a new agent version when you need to update the container image, change resource allocation, or modify environment variables.

:::zone pivot="rest"

```bash
az rest --method POST \
    --url "${BASE_URL}/agents/${AGENT_NAME}/versions?api-version=${API_VERSION}" \
    --resource "${RESOURCE}" \
    --body '{
        "definition": {
            "kind": "hosted",
            "image": "myregistry.azurecr.io/my-agent:v2",
            "cpu": "1",
            "memory": "2Gi",
            "container_protocol_versions": [
                {"protocol": "responses", "version": "1.0.0"}
            ]
        }
    }'
```

Replace `responses` with `invocations` if your agent uses the Invocations protocol, or include both to expose both protocols. For details on protocol selection, see [Deploy a hosted agent](deploy-hosted-agent.md#container-requirements).

:::zone-end

:::zone pivot="python"

```python
from azure.ai.projects.models import HostedAgentDefinition, ProtocolVersionRecord

agent = project.agents.create_version(
    agent_name="my-agent",
    definition=HostedAgentDefinition(
        cpu="1",
        memory="2Gi",
        image="myregistry.azurecr.io/my-agent:v2",
        container_protocol_versions=[
            ProtocolVersionRecord(protocol="responses", version="1.0.0"),
        ],
    ),
)
print(f"Created version: {agent.version}")
```

Replace `responses` with `invocations` if your agent uses the Invocations protocol, or pass both to expose both protocols.

:::zone-end

:::zone pivot="azd"

New versions are created automatically when you run `azd deploy` with updated code or configuration.

:::zone-end

### Version status values

After you create or update an agent version, poll the version endpoint until the status reaches `active`:

| Status | Description |
|--------|-------------|
| `creating` | Infrastructure is being provisioned (typically 2-5 minutes). |
| `active` | Agent is ready to serve requests. |
| `failed` | Provisioning failed. Check the `error` field in the response for details. |
| `deleting` | Version is being cleaned up. |
| `deleted` | Version has been fully removed. |

:::zone pivot="python"

Poll the version status after creation:

```python
import time

def wait_for_version_active(project, agent_name, agent_version, max_attempts=60):
    for attempt in range(max_attempts):
        time.sleep(10)
        version = project.agents.get_version(
            agent_name=agent_name, agent_version=agent_version
        )
        status = version["status"]
        print(f"Version status: {status} (attempt {attempt + 1})")
        if status == "active":
            return
        if status == "failed":
            raise RuntimeError(f"Version provisioning failed: {dict(version)}")
    raise RuntimeError("Timed out waiting for version to become active")
```

:::zone-end

## Delete an agent

You can delete a specific version or an entire agent with all its versions.

### Delete a specific version

:::zone pivot="rest"

```bash
az rest --method DELETE \
    --url "${BASE_URL}/agents/${AGENT_NAME}/versions/1?api-version=${API_VERSION}" \
    --resource "${RESOURCE}"
```

:::zone-end

:::zone pivot="python"

```python
project.agents.delete_version(agent_name="my-agent", agent_version="1")
```

:::zone-end

:::zone pivot="azd"

Not currently supported as a standalone command. Use the REST API or SDK.

:::zone-end

### Delete an agent and all versions

> [!WARNING]
> This action permanently deletes the agent and all its versions. Active sessions are terminated. This operation can't be undone.

:::zone pivot="rest"

```bash
az rest --method DELETE \
    --url "${BASE_URL}/agents/${AGENT_NAME}?api-version=${API_VERSION}" \
    --resource "${RESOURCE}"
```

:::zone-end

:::zone pivot="python"

```python
project.agents.delete(agent_name="my-agent")
```

:::zone-end

:::zone pivot="azd"

Not currently supported as a standalone command. Use the REST API or SDK.

:::zone-end

## View logs and monitor

Access container logs for debugging provisioning and runtime issues.

:::zone pivot="rest"

Stream logs from a specific agent session:

```bash
AGENT_VERSION="<version>"
SESSION_ID="<session-id>"

az rest --method GET \
    --url "${BASE_URL}/agents/${AGENT_NAME}/versions/${AGENT_VERSION}/sessions/${SESSION_ID}:logstream?api-version=${API_VERSION}" \
    --resource "${RESOURCE}" \
    --headers "Foundry-Features=HostedAgents=V1Preview" "Accept=text/event-stream"
```

The logstream endpoint returns Server-Sent Events (SSE) with `event: log` frames. Each frame contains a JSON payload with `timestamp`, `stream` (`stdout`, `stderr`, or `status`), and `message` fields.

Timeouts:

- Maximum connection duration: 30 minutes
- Idle timeout: 2 minutes

:::zone-end

:::zone pivot="python"

Viewing container logs isn't currently supported through the Python SDK. Use the REST API or Azure Developer CLI.

:::zone-end

:::zone pivot="azd"

Monitor a running agent with real-time status and log information:

```bash
azd ai agent monitor
```

This command reads the agent name and version from the `azd` service entry in your project configuration.

:::zone-end

### Example log output

```text
2026-04-09T08:43:48.72656  Connecting to the container 'agent-container'...
2026-04-09T08:43:48.75451  Successfully connected to container: 'agent-container'
2026-04-09T08:43:59.0671054Z stdout F INFO: 127.0.0.1:42588 - "GET /readiness HTTP/1.1" 200 OK
```

## Configure agent endpoint routing

Agent endpoints control how traffic is distributed across agent versions. Use version selectors to route a percentage of traffic to specific versions, enabling canary deployments or gradual rollouts.

:::zone pivot="rest"

Endpoint routing is configured by patching the agent object. Use `PATCH /agents/{agent_name}` with `Content-Type: application/merge-patch+json`:

```bash
az rest --method PATCH \
    --url "${BASE_URL}/agents/${AGENT_NAME}?api-version=${API_VERSION}" \
    --resource "${RESOURCE}" \
    --headers "Content-Type=application/merge-patch+json" "Foundry-Features=AgentEndpoints=V1Preview" \
    --body '{
        "agent_endpoint": {
            "version_selector": {
                "version_selection_rules": [
                    {"agent_version": "1", "traffic_percentage": 100, "type": "FixedRatio"}
                ]
            },
            "protocols": ["responses"]
        }
    }'
```

Set `protocols` to `["invocations"]` or `["responses", "invocations"]` to match the protocols your agent exposes.

To split traffic between two versions (for example, 90/10 for a canary deployment):

```bash
az rest --method PATCH \
    --url "${BASE_URL}/agents/${AGENT_NAME}?api-version=${API_VERSION}" \
    --resource "${RESOURCE}" \
    --headers "Content-Type=application/merge-patch+json" "Foundry-Features=AgentEndpoints=V1Preview" \
    --body '{
        "agent_endpoint": {
            "version_selector": {
                "version_selection_rules": [
                    {"agent_version": "1", "traffic_percentage": 90, "type": "FixedRatio"},
                    {"agent_version": "2", "traffic_percentage": 10, "type": "FixedRatio"}
                ]
            },
            "protocols": ["responses"]
        }
    }'
```

:::zone-end

:::zone pivot="python"

```python
from azure.ai.projects.models import (
    AgentEndpoint,
    AgentEndpointProtocol,
    FixedRatioVersionSelectionRule,
    VersionSelector,
)

endpoint_config = AgentEndpoint(
    version_selector=VersionSelector(
        version_selection_rules=[
            FixedRatioVersionSelectionRule(
                agent_version="1", traffic_percentage=100
            ),
        ]
    ),
    protocols=[AgentEndpointProtocol.RESPONSES],
)

project.beta.agents.patch_agent_details(
    agent_name="my-agent",
    agent_endpoint=endpoint_config,
)
```

:::zone-end

:::zone pivot="azd"

Endpoint routing is configured automatically during `azd deploy`. To customize traffic distribution, use the REST API or SDK.

:::zone-end

## Retrieve the agent identity for role assignments

Each hosted agent has an *instance identity* — a Microsoft Entra ID service principal that the agent uses at runtime to authenticate to downstream resources. To grant the agent access to services such as Azure Storage or Azure Cosmos DB, you need the identity's principal ID so you can create RBAC role assignments.

For more information on how agent identities work, see [Agent identity concepts](../concepts/agent-identity.md).

### Extract the agent identity principal ID

:::zone pivot="rest"

Use the `--query` parameter to extract the `instance_identity.principal_id` directly from the agent details:

```bash
AGENT_IDENTITY=$(az rest --method GET \
    --url "${BASE_URL}/agents/${AGENT_NAME}?api-version=${API_VERSION}" \
    --resource "${RESOURCE}" \
    --query "instance_identity.principal_id" \
    --output tsv)

echo "Agent identity principal ID: ${AGENT_IDENTITY}"
```

:::zone-end

:::zone pivot="python"

```python
agent = project.agents.get(agent_name="my-agent")
agent_identity = agent.instance_identity["principal_id"]
print(f"Agent identity principal ID: {agent_identity}")
```

:::zone-end

:::zone pivot="azd"

Use the REST API or Python SDK to retrieve the agent identity principal ID.

:::zone-end

### Assign roles to the agent identity

After you have the principal ID, assign RBAC roles to the agent identity at the appropriate resource scope. Use `--assignee-object-id` with `--assignee-principal-type ServicePrincipal` to avoid Microsoft Graph lookup issues with agent identity service principals.

The agent identity works with any Azure resource that supports RBAC. The following examples show two common scenarios: granting access to the Foundry project and granting access to a storage account.

:::zone pivot="rest"

Assign a role on the Foundry project (for example, to allow the agent to use project resources):

```bash
az role assignment create \
    --assignee-object-id "$AGENT_IDENTITY" \
    --assignee-principal-type ServicePrincipal \
    --role "Azure AI Developer" \
    --scope "/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.CognitiveServices/accounts/<account-name>/projects/<project-name>"
```

Assign a role on a storage account (for example, to allow the agent to read and write blobs):

```bash
az role assignment create \
    --assignee-object-id "$AGENT_IDENTITY" \
    --assignee-principal-type ServicePrincipal \
    --role "Storage Blob Data Contributor" \
    --scope "/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.Storage/storageAccounts/<storage-account>"
```

:::zone-end

:::zone pivot="python"

Role assignments are an Azure Resource Manager operation. Use the Azure CLI commands shown in the REST tab with the `agent_identity` value from the previous step, or use the [Azure Authorization Management](/python/api/azure-mgmt-authorization) SDK to create role assignments programmatically.

:::zone-end

:::zone pivot="azd"

Use the Azure CLI directly to create role assignments. Retrieve the agent identity principal ID by using the REST API or Python SDK, then run `az role assignment create` as shown in the REST tab.

:::zone-end

### Verify role assignments

:::zone pivot="rest"

List the roles assigned to the agent identity on the Foundry project:

```bash
az role assignment list \
    --assignee "$AGENT_IDENTITY" \
    --scope "/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.CognitiveServices/accounts/<account-name>/projects/<project-name>" \
    --output table
```

List the roles assigned to the agent identity on a storage account:

```bash
az role assignment list \
    --assignee "$AGENT_IDENTITY" \
    --scope "/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.Storage/storageAccounts/<storage-account>" \
    --output table
```

:::zone-end

:::zone pivot="python"

Use the Azure CLI commands shown in the REST tab to verify role assignments.

:::zone-end

:::zone pivot="azd"

Use the Azure CLI directly to verify role assignments as shown in the REST tab.

:::zone-end

## Next steps

> [!div class="nextstepaction"]
> [Publish and share agents](publish-agent.md)

## Related content

- [What are hosted agents?](../concepts/hosted-agents.md)
- [Deploy a hosted agent](deploy-hosted-agent.md)
- [Agent identity concepts](../concepts/agent-identity.md)
- [Evaluate your AI agents](../../observability/concepts/trace-agent-concept.md)
