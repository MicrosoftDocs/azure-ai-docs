---
title: Manage hosted agent lifecycle
titleSuffix: Microsoft Foundry
description: Start, stop, update, and delete hosted agent deployments using the Azure CLI or Python SDK.
author: aahill
ms.author: aahi
ms.date: 01/26/2026
ms.manager: nitinme
ms.topic: how-to
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ai-usage: ai-assisted
---

# Manage hosted agent lifecycle

This article shows you how to manage hosted agent deployments in Foundry Agent Service. After you deploy a hosted agent, you can start, stop, update, and delete it as your needs change.

## Prerequisites

* A [deployed hosted agent](deploy-hosted-agent.md)
* [Azure CLI](/cli/azure/install-azure-cli) version 2.80 or later
* Azure Cognitive Services CLI extension:

    ```bash
    az extension add --name cognitiveservices --upgrade
    ```

## Start an agent deployment

Start a hosted agent to make it available for requests. Use this command to start a new deployment or restart a stopped agent.

```bash
az cognitiveservices agent start \
    --account-name myAccount \
    --project-name myProject \
    --name myAgent \
    --agent-version 1 \
    --min-replicas 1 \
    --max-replicas 2
```

| Argument | Required | Description |
|----------|----------|-------------|
| `--account-name -a` | Yes | Microsoft Foundry account name |
| `--project-name` | Yes | AI project name |
| `--name -n` | Yes | Hosted agent name |
| `--agent-version` | Yes | Agent version to start |
| `--min-replicas` | No | Minimum replicas (default: 1) |
| `--max-replicas` | No | Maximum replicas (default: 1) |

State transitions when starting:

- **Stopped** → **Starting** → **Started** (success) or **Failed** (error)

## Stop an agent deployment

Stop a running agent to pause processing and reduce costs. The agent version remains available for restarting later.

```bash
az cognitiveservices agent stop \
    --account-name myAccount \
    --project-name myProject \
    --name myAgent \
    --agent-version 1
```

| Argument | Required | Description |
|----------|----------|-------------|
| `--account-name -a` | Yes | Microsoft Foundry account name |
| `--project-name` | Yes | AI project name |
| `--name -n` | Yes | Hosted agent name |
| `--agent-version` | Yes | Agent version to stop |

State transitions when stopping:

- **Running** → **Stopping** → **Stopped** (success) or **Running** (error)

## Update an agent

You can update agents with versioned or non-versioned changes.

### Versioned updates

Versioned updates create a new agent version. Use them for:

- Container image changes
- CPU or memory allocation changes
- Environment variable modifications
- Protocol version updates

You can create a new version using the Azure CLI.

#### Create version using Azure CLI

For CLI-based version creation, see [az cognitiveservices agent create](/cli/azure/cognitiveservices/agent#az-cognitiveservices-agent-create).

### Non-versioned updates

Non-versioned updates modify scaling or metadata without creating a new version:

```bash
az cognitiveservices agent update \
    --account-name myAccount \
    --project-name myProject \
    --name myAgent \
    --agent-version 1 \
    --min-replicas 2 \
    --max-replicas 5 \
    --description "Updated production agent"
```

| Argument | Required | Description |
|----------|----------|-------------|
| `--account-name -a` | Yes | Microsoft Foundry account name |
| `--project-name` | Yes | AI project name |
| `--name -n` | Yes | Hosted agent name |
| `--agent-version` | Yes | Agent version to update |
| `--min-replicas` | No | Minimum replicas for scaling |
| `--max-replicas` | No | Maximum replicas for scaling |
| `--description` | No | Agent description |
| `--tags` | No | Space-separated tags (`key=value`) |

## Delete an agent

### Delete a deployment only

Stop the agent deployment but keep the version definition for later use:

```bash
az cognitiveservices agent delete-deployment \
    --account-name myAccount \
    --project-name myProject \
    --name myAgent \
    --agent-version 1
```

### Delete a specific version

Delete an agent version and its deployment:

```bash
az cognitiveservices agent delete \
    --account-name myAccount \
    --project-name myProject \
    --name myAgent \
    --agent-version 1
```

> [!NOTE]
> If the agent deployment is running, this operation fails. Stop the deployment first.

### Delete all versions

Remove all versions of an agent:

```bash
az cognitiveservices agent delete \
    --account-name myAccount \
    --project-name myProject \
    --name myAgent
```

### Delete using the SDK

```python
client.agents.delete_version(agent_name="my-agent", agent_version="1")
```

## List and view agents

### List all versions of an agent

```bash
az cognitiveservices agent list-versions \
    --account-name myAccount \
    --project-name myProject \
    --name myAgent
```

### Show agent details

```bash
az cognitiveservices agent show \
    --account-name myAccount \
    --project-name myProject \
    --name myAgent
```

## View container logs

Access container logs for debugging startup and runtime issues.

### REST API

```http
GET https://{endpoint}/api/projects/{projectName}/agents/{agentName}/versions/{agentVersion}/containers/default:logstream
```

Timeouts:

- Maximum connection duration: 10 minutes
- Idle timeout: 1 minute

### Example console log response

```text
2025-12-15T08:43:48.72656  Connecting to the container 'agent-container'...
2025-12-15T08:43:48.75451  Successfully Connected to container: 'agent-container'
2025-12-15T08:33:59.0671054Z stdout F INFO: 127.0.0.1:42588 - "GET /readiness HTTP/1.1" 200 OK
```

## Invoke a hosted agent

Test your running agent using the SDK:

```python
import os
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import AgentReference

endpoint = os.environ["AZURE_AI_PROJECT_ENDPOINT"]
agent_name = os.environ["AZURE_AI_AGENT_NAME"]

with (
    DefaultAzureCredential() as credential,
    AIProjectClient(endpoint=endpoint, credential=credential) as client,
    client.get_openai_client() as openai_client,
):
    agent = client.agents.get(agent_name=agent_name)
    
    response = openai_client.responses.create(
        input=[{"role": "user", "content": "Hello! What can you help me with?"}],
        extra_body={"agent": AgentReference(name=agent.name, version="1").as_dict()}
    )
    
    print(f"Response: {response.output_text}")
```

You can also test agents in the agent playground UI in the Foundry portal.

## Troubleshooting

### Agent fails to start

| Symptom | Cause | Resolution |
|---------|-------|------------|
| Status shows `Failed` | Container image issues | Check image exists and is accessible |
| `AcrPullUnauthorized` error | Missing ACR permissions | Grant Container Registry Repository Reader role to project identity |
| `RegistryNotFound` error | Network or DNS issues | Verify registry URL and network connectivity |

### Agent starts but doesn't respond

1. Check container logs for runtime errors
1. Verify the hosting adapter is correctly configured
1. Confirm environment variables are set correctly
1. Test the agent locally before deploying

### Common pitfalls

- **Forgetting ACR permissions**: The project's managed identity needs explicit pull access to the container registry
- **Wrong SDK version**: Hosted agents require `azure-ai-projects>=2.0.0b3`
- **Missing capability host**: Create an account-level capability host before deploying. See [Deploy a hosted agent](deploy-hosted-agent.md#create-an-account-level-capability-host)
- **Publishing identity mismatch**: After publishing, the agent uses a different identity. Reassign RBAC permissions

## Next steps

> [!div class="nextstepaction"]
> [Publish and share agents](publish-agent.md)

## Related content

- [What are hosted agents?](../concepts/hosted-agents.md)
- [Deploy a hosted agent](deploy-hosted-agent.md)
- [Agent identity concepts](../concepts/agent-identity.md)
- [Evaluate your AI agents locally](../../../how-to/develop/agent-evaluate-sdk.md)
