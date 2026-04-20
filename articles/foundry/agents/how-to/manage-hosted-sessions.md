---
title: "Manage hosted agent sessions"
description: "Create, invoke, and manage sessions for hosted agents in Foundry Agent Service by using the REST API, Python SDK, or Azure Developer CLI."
author: aahill
ms.author: aahi
ms.date: 04/14/2026
ms.manager: nitinme
ms.topic: how-to
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ai-usage: ai-assisted
ms.custom: doc-kit-assisted
zone_pivot_groups: hosted-agent-manage-method
---

# Manage hosted agent sessions

This article shows you how to create and manage sessions for hosted agents in Foundry Agent Service. Sessions provide isolated sandbox compute for each request, so you can run multiple conversations or tasks concurrently without shared state.

## Prerequisites

- A [deployed hosted agent](deploy-hosted-agent.md) with an `active` version. See [Manage hosted agents](manage-hosted-agent.md) for how to check version status.

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
BASE_URL="https://${ACCOUNT_NAME}.services.ai.azure.com/api/projects/${PROJECT_NAME}"
API_VERSION="2025-11-15-preview"
RESOURCE="https://ai.azure.com"
```

> [!IMPORTANT]
> The `--resource` parameter is required for all `az rest` calls to Foundry Agent Service data-plane endpoints. Without it, `az rest` can't derive the correct Microsoft Entra audience from the URL and authentication fails.

> [!NOTE]
> Session operations are a preview feature. Include the `Foundry-Features: HostedAgents=V1Preview` header in every REST request.

:::zone-end

:::zone pivot="python"

## Set up the client

All Python examples in this article use the following client configuration:

```python
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

project = AIProjectClient(
    endpoint="<your-project-endpoint>",
    credential=DefaultAzureCredential(),
    allow_preview=True,
)
```

> [!NOTE]
> Session operations use the preview sub-client `project.beta.agents`.

:::zone-end

## Create a session

Create a session to establish an isolated sandbox for your agent. Each session requires an isolation key that identifies the session owner and an agent version to run.

:::zone pivot="rest"

```bash
AGENT_NAME="my-agent"
AGENT_VERSION="1"

az rest --method POST \
    --url "${BASE_URL}/agents/${AGENT_NAME}/endpoint/sessions?api-version=${API_VERSION}" \
    --resource "${RESOURCE}" \
    --headers "x-session-isolation-key=user-123" "Foundry-Features=HostedAgents=V1Preview" \
    --body "{
        \"version_indicator\": {
            \"agent_version\": \"${AGENT_VERSION}\",
            \"type\": \"version_ref\"
        }
    }"
```

:::zone-end

:::zone pivot="python"

```python
from azure.ai.projects.models import VersionRefIndicator

session = project.beta.agents.create_session(
    agent_name="my-agent",
    isolation_key="user-123",
    version_indicator=VersionRefIndicator(agent_version="1"),
)
print(f"Session created (ID: {session.agent_session_id}, status: {session.status})")
```

:::zone-end

:::zone pivot="azd"

Sessions are created automatically when you invoke an agent through `azd`. Manual session creation isn't currently available as a standalone command.

:::zone-end

The isolation key is a string that you define. Use it to group sessions by user, tenant, or any other logical boundary.

## Invoke an agent through a session

After you create a session, invoke the agent by sending requests through the OpenAI Responses API with the session ID bound to the request. For agents using the Invocations protocol, see [Deploy a hosted agent](deploy-hosted-agent.md#invoke-the-agent) — invocations agents manage state directly and don't use platform-managed sessions.

:::zone pivot="rest"

```bash
AGENT_NAME="my-agent"
SESSION_ID="<session-id>"

az rest --method POST \
    --url "${BASE_URL}/agents/${AGENT_NAME}/endpoint/protocols/openai/responses?api-version=${API_VERSION}" \
    --resource "${RESOURCE}" \
    --headers "Foundry-Features=HostedAgents=V1Preview" \
    --body "{
        \"input\": \"Find me hotels in Seattle under \$200 per night\",
        \"stream\": false,
        \"agent_session_id\": \"${SESSION_ID}\"
    }"
```

:::zone-end

:::zone pivot="python"

```python
openai_client = project.get_openai_client(agent_name="my-agent")

response = openai_client.responses.create(
    input="Find me hotels in Seattle under $200 per night",
    extra_body={
        "agent_session_id": session.agent_session_id,
    },
)
print(f"Response: {response.output_text}")
```

When you call `get_openai_client` with an `agent_name`, the client is automatically configured to route requests to the correct agent endpoint.

:::zone-end

:::zone pivot="azd"

```bash
azd ai agent invoke --input "Find me hotels in Seattle under $200 per night"
```

:::zone-end

## List sessions

:::zone pivot="rest"

```bash
az rest --method GET \
    --url "${BASE_URL}/agents/my-agent/endpoint/sessions?api-version=${API_VERSION}" \
    --resource "${RESOURCE}" \
    --headers "Foundry-Features=HostedAgents=V1Preview"
```

:::zone-end

:::zone pivot="python"

```python
sessions = project.beta.agents.list_sessions(agent_name="my-agent")
for item in sessions:
    print(f"Session: {item.agent_session_id} (status: {item.status})")
```

:::zone-end

:::zone pivot="azd"

Session listing isn't currently available as a standalone command. Use the REST API or SDK.

:::zone-end

## Get session details

:::zone pivot="rest"

```bash
SESSION_ID="<session-id>"

az rest --method GET \
    --url "${BASE_URL}/agents/my-agent/endpoint/sessions/${SESSION_ID}?api-version=${API_VERSION}" \
    --resource "${RESOURCE}" \
    --headers "Foundry-Features=HostedAgents=V1Preview"
```

:::zone-end

:::zone pivot="python"

```python
session = project.beta.agents.get_session(
    agent_name="my-agent",
    session_id="<session-id>",
)
print(f"Session ID: {session.agent_session_id}, Status: {session.status}")
```

:::zone-end

:::zone pivot="azd"

Session management isn't currently available as a standalone command. Use the REST API or SDK.

:::zone-end

## Delete a session

Deleting a session terminates the sandbox and releases its resources. The isolation key must match the key used when the session was created.

:::zone pivot="rest"

```bash
SESSION_ID="<session-id>"
ISOLATION_KEY="user-123"

az rest --method DELETE \
    --url "${BASE_URL}/agents/my-agent/endpoint/sessions/${SESSION_ID}?api-version=${API_VERSION}" \
    --resource "${RESOURCE}" \
    --headers "x-session-isolation-key=${ISOLATION_KEY}" "Foundry-Features=HostedAgents=V1Preview"
```

:::zone-end

:::zone pivot="python"

```python
project.beta.agents.delete_session(
    agent_name="my-agent",
    session_id="<session-id>",
    isolation_key="user-123",
)
```

:::zone-end

:::zone pivot="azd"

Session management isn't currently available as a standalone command. Use the REST API or SDK.

:::zone-end

## Session file operations

Upload and download files to agent session sandboxes. Each file is scoped to a specific session. The maximum file size for upload is 50 MB.

### Upload a file

:::zone pivot="rest"

```bash
SESSION_ID="<session-id>"

az rest --method PUT \
    --url "${BASE_URL}/agents/my-agent/endpoint/sessions/${SESSION_ID}/files/content?api-version=${API_VERSION}&path=data.csv" \
    --resource "${RESOURCE}" \
    --body @data.csv \
    --headers "Content-Type=application/octet-stream" "Foundry-Features=HostedAgents=V1Preview"
```

:::zone-end

:::zone pivot="python"

```python
project.beta.agents.upload_session_file(
    agent_name="my-agent",
    session_id="<session-id>",
    content_or_file_path="./data.csv",
    path="data.csv",
)
```

The `content_or_file_path` parameter accepts a file path string. The SDK reads and uploads the file contents automatically.

:::zone-end

:::zone pivot="azd"

```bash
azd ai agent files upload --file ./data.csv --target-path data.csv
```

:::zone-end

### List files in a session

:::zone pivot="rest"

```bash
SESSION_ID="<session-id>"

az rest --method GET \
    --url "${BASE_URL}/agents/my-agent/endpoint/sessions/${SESSION_ID}/files?api-version=${API_VERSION}&path=." \
    --resource "${RESOURCE}" \
    --headers "Foundry-Features=HostedAgents=V1Preview"
```

:::zone-end

:::zone pivot="python"

```python
files = project.beta.agents.get_session_files(
    agent_name="my-agent",
    session_id="<session-id>",
    path=".",
)
for entry in files.entries:
    print(f"  {entry.name} (size: {entry.size}, directory: {entry.is_dir})")
```

:::zone-end

:::zone pivot="azd"

```bash
azd ai agent files list .
```

:::zone-end

### Download a file

:::zone pivot="rest"

```bash
SESSION_ID="<session-id>"

az rest --method GET \
    --url "${BASE_URL}/agents/my-agent/endpoint/sessions/${SESSION_ID}/files/content?api-version=${API_VERSION}&path=data.csv" \
    --resource "${RESOURCE}" \
    --headers "Foundry-Features=HostedAgents=V1Preview" \
    --output-file output.csv
```

:::zone-end

:::zone pivot="python"

```python
content_bytes = b"".join(
    project.beta.agents.download_session_file(
        agent_name="my-agent",
        session_id="<session-id>",
        path="data.csv",
    )
)
with open("./output.csv", "wb") as f:
    f.write(content_bytes)
```

:::zone-end

:::zone pivot="azd"

```bash
azd ai agent files download --file data.csv --target-path ./output.csv
```

:::zone-end

### Delete a file

:::zone pivot="rest"

```bash
SESSION_ID="<session-id>"

az rest --method DELETE \
    --url "${BASE_URL}/agents/my-agent/endpoint/sessions/${SESSION_ID}/files?api-version=${API_VERSION}&path=data.csv" \
    --resource "${RESOURCE}" \
    --headers "Foundry-Features=HostedAgents=V1Preview"
```

:::zone-end

:::zone pivot="python"

```python
project.beta.agents.delete_session_file(
    agent_name="my-agent",
    session_id="<session-id>",
    path="data.csv",
)
```

:::zone-end

:::zone pivot="azd"

```bash
azd ai agent files remove --file data.csv
```

:::zone-end

## Next steps

> [!div class="nextstepaction"]
> [Manage hosted agents](manage-hosted-agent.md)

## Related content

- [What are hosted agents?](../concepts/hosted-agents.md)
- [Deploy a hosted agent](deploy-hosted-agent.md)
- [Manage hosted agents](manage-hosted-agent.md)
- [Agent identity concepts](../concepts/agent-identity.md)
