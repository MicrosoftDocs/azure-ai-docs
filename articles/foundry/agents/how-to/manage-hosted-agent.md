---
title: "Manage hosted agents"
description: "View, monitor, and manage hosted agents in Foundry Agent Service by using the REST API, Python SDK, or Azure Developer CLI."
author: aahill
ms.author: aahi
ms.date: 04/09/2026
ms.manager: nitinme
ms.topic: how-to
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ai-usage: ai-assisted
ms.custom: doc-kit-assisted
zone_pivot_groups: hosted-agent-manage-method
---

# Manage hosted agents

This article shows you how to manage hosted agents in Foundry Agent Service. After you [deploy a hosted agent](deploy-hosted-agent.md), you can view its status, monitor logs, manage session files, and delete it when it's no longer needed.

The platform manages the container lifecycle automatically. Compute is provisioned when a request arrives and deprovisioned after the idle timeout (15 minutes). There are no manual start or stop operations.

## Prerequisites

- A [deployed hosted agent](deploy-hosted-agent.md).

:::zone pivot="rest"

- [Azure CLI](/cli/azure/install-azure-cli) version 2.80 or later, authenticated with `az login`.

:::zone-end

:::zone pivot="python"

- Python SDK: `azure-ai-projects>=2.0.0` and `azure-identity`.

> [!NOTE]
> Session management and file operations use the preview sub-client `project.beta.agents`. Pass `api_version="2025-11-15-preview"` when you create the `AIProjectClient` to enable these operations.

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
BASE_URL="https://${ACCOUNT_NAME}.services.ai.azure.com/api/projects/${PROJECT_NAME}"
API_VERSION="2025-11-15-preview"
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
    api_version="2025-11-15-preview",
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
    --url "${BASE_URL}/agents/my-agent?api-version=${API_VERSION}" \
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
    --url "${BASE_URL}/agents/my-agent/versions/1?api-version=${API_VERSION}" \
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
    --url "${BASE_URL}/agents/my-agent/versions?api-version=${API_VERSION}" \
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

### Version status values

After you create or update an agent version, poll the version endpoint until the status reaches `active`:

| Status | Description |
|--------|-------------|
| `creating` | Infrastructure is being provisioned (typically 2-5 minutes). |
| `active` | Agent is ready to serve requests. |
| `failed` | Provisioning failed. Check the `error` field in the response for details. |
| `deleting` | Version is being cleaned up. |
| `deleted` | Version has been fully removed. |

## Delete an agent

You can delete a specific version or an entire agent with all its versions.

### Delete a specific version

:::zone pivot="rest"

```bash
az rest --method DELETE \
    --url "${BASE_URL}/agents/my-agent/versions/1?api-version=${API_VERSION}" \
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
    --url "${BASE_URL}/agents/my-agent?api-version=${API_VERSION}" \
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
SESSION_ID="<session-id>"

az rest --method GET \
    --url "${BASE_URL}/agents/my-agent/endpoint/sessions/${SESSION_ID}:logstream?api-version=${API_VERSION}&kind=console&tail=100&follow=true" \
    --resource "${RESOURCE}"
```

| Parameter | Description |
|-----------|-------------|
| `kind` | Log type: `console` (stdout/stderr) or `system` (container events). |
| `tail` | Number of trailing lines to fetch (1-300). |
| `follow` | `true` to stream indefinitely, `false` to fetch and return. |

Timeouts:

- Maximum connection duration: 10 minutes
- Idle timeout: 1 minute

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

## Manage sessions

Each hosted agent uses sessions to provide isolated sandbox compute for requests. Sessions are scoped to an agent and are identified by a session ID. You can list, inspect, and delete sessions for an agent.

### List sessions

:::zone pivot="rest"

```bash
az rest --method GET \
    --url "${BASE_URL}/agents/my-agent/endpoint/sessions?api-version=${API_VERSION}" \
    --resource "${RESOURCE}"
```

:::zone-end

:::zone pivot="python"

```python
for session in project.beta.agents.list_sessions(agent_name="my-agent"):
    print(f"Session: {session.id}")
```

:::zone-end

:::zone pivot="azd"

Session management isn't currently available as a standalone command. Use the REST API or SDK.

:::zone-end

### Get session details

:::zone pivot="rest"

```bash
SESSION_ID="<session-id>"

az rest --method GET \
    --url "${BASE_URL}/agents/my-agent/endpoint/sessions/${SESSION_ID}?api-version=${API_VERSION}" \
    --resource "${RESOURCE}"
```

:::zone-end

:::zone pivot="python"

```python
session = project.beta.agents.get_session(
    agent_name="my-agent", session_id="session-id"
)
print(f"Session ID: {session.id}")
```

:::zone-end

:::zone pivot="azd"

Session management isn't currently available as a standalone command. Use the REST API or SDK.

:::zone-end

### Delete a session

Deleting a session terminates the sandbox and releases its resources. The `x-session-isolation-key` header must match the key used when the session was created.

:::zone pivot="rest"

```bash
SESSION_ID="<session-id>"
ISOLATION_KEY="<isolation-key>"

az rest --method DELETE \
    --url "${BASE_URL}/agents/my-agent/endpoint/sessions/${SESSION_ID}?api-version=${API_VERSION}" \
    --resource "${RESOURCE}" \
    --headers "x-session-isolation-key=${ISOLATION_KEY}"
```

:::zone-end

:::zone pivot="python"

```python
project.beta.agents.delete_session(
    agent_name="my-agent",
    session_id="session-id",
    isolation_key="<isolation-key>",
)
```

:::zone-end

:::zone pivot="azd"

Session management isn't currently available as a standalone command. Use the REST API or SDK.

:::zone-end

## Session file operations

Upload and download files to agent session sandboxes. Each file is scoped to a specific session.

:::zone pivot="rest"

```bash
SESSION_ID="<session-id>"
ENDPOINT_BASE="${BASE_URL}/agents/my-agent/endpoint/sessions/${SESSION_ID}/files"

# Upload a file to a session (max 50 MB)
az rest --method PUT \
    --url "${ENDPOINT_BASE}/content?api-version=${API_VERSION}&path=/data.csv" \
    --resource "${RESOURCE}" \
    --body @data.csv \
    --headers "Content-Type=application/octet-stream"

# Download a file from a session
az rest --method GET \
    --url "${ENDPOINT_BASE}/content?api-version=${API_VERSION}&path=/data.csv" \
    --resource "${RESOURCE}" \
    --output-file output.csv

# List files in a session
az rest --method GET \
    --url "${ENDPOINT_BASE}?api-version=${API_VERSION}&path=/" \
    --resource "${RESOURCE}"

# Delete a file from a session
az rest --method DELETE \
    --url "${ENDPOINT_BASE}?api-version=${API_VERSION}&path=/data.csv" \
    --resource "${RESOURCE}"
```

:::zone-end

:::zone pivot="python"

```python
# Upload a file to a session (max 50 MB)
with open("./data.csv", "rb") as f:
    project.beta.agents.upload_session_file(
        agent_name="my-agent",
        session_id="session-id",
        content=f.read(),
        path="/data.csv",
    )

# Download a file from a session
chunks = project.beta.agents.download_session_file(
    agent_name="my-agent", session_id="session-id", path="/data.csv"
)
with open("./output.csv", "wb") as f:
    for chunk in chunks:
        f.write(chunk)

# List files in a session
files = project.beta.agents.list_session_files(
    agent_name="my-agent", session_id="session-id", path="/"
)

# Delete a file from a session
project.beta.agents.delete_session_file(
    agent_name="my-agent", session_id="session-id", path="/data.csv"
)
```

:::zone-end

:::zone pivot="azd"

```bash
azd ai agent files upload --file ./data.csv --target-path /data.csv
azd ai agent files download --file /data.csv --target-path ./output.csv
azd ai agent files list /
azd ai agent files remove --file /data.csv
```

:::zone-end

For details on invoking agents through these endpoints, see the [hosted agents quickstart](../../agents/quickstarts/quickstart-hosted-agent.md).

## Next steps

> [!div class="nextstepaction"]
> [Publish and share agents](publish-agent.md)

## Related content

- [What are hosted agents?](../concepts/hosted-agents.md)
- [Deploy a hosted agent](deploy-hosted-agent.md)
- [Agent identity concepts](../concepts/agent-identity.md)
- [Evaluate your AI agents](../../observability/concepts/trace-agent-concept.md)
