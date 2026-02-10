---
title: Deploy a hosted agent
titleSuffix: Microsoft Foundry
description: Deploy your containerized agent code to Foundry Agent Service using the Azure Developer CLI or Python SDK.
author: aahill
ms.author: aahi
ms.date: 01/26/2026
ms.manager: nitinme
ms.topic: how-to
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.custom: references_regions
ai-usage: ai-assisted
---

# Deploy a hosted agent

This article shows you how to deploy a containerized agent to Foundry Agent Service. Use hosted agents when you need to run custom agent code built with frameworks like LangGraph, Microsoft Agent Framework, or your own implementation.

## Prerequisites

* A [Microsoft Foundry project](../../../how-to/create-projects.md)
* [Python 3.10 or later](https://www.python.org/downloads/) for SDK-based development
* [Azure CLI](/cli/azure/install-azure-cli) version 2.80 or later
* [Docker Desktop](https://docs.docker.com/get-docker/) installed for local container development
* Familiarity with [Azure Container Registry](/azure/container-registry/container-registry-intro)
* Agent code using a [supported framework](../concepts/hosted-agents.md#framework-and-language-support)

### Required permissions

You need one of the following role combinations depending on your deployment scenario:

| Scenario | Required roles |
|----------|----------------|
| Create new Foundry project | **Azure AI Owner** on Foundry resource |
| Deploy to existing project with new resources | **Azure AI Owner** on Foundry + **Contributor** on subscription |
| Deploy to fully configured project | **Reader** on account + **Azure AI User** on project |

For more information, see [Authentication and authorization](../../../concepts/authentication-authorization-foundry.md).

## Package and test your agent locally

Before deploying to Foundry, validate your agent works locally using the hosting adapter.

### Run your agent locally

The hosting adapter starts a local web server that exposes your agent as a REST API:

```http
@baseUrl = http://localhost:8088

POST {{baseUrl}}/responses
Content-Type: application/json.
{
    "input": {
        "messages": [
            {
                "role": "user",
                "content": "Where is Seattle?"
            }
        ]
    }
}
```

A successful response:

```json
{
    "id": "resp_abc123",
    "object": "response",
    "output": [
        {
            "type": "message",
            "role": "assistant",
            "content": "Seattle is a major city in the Pacific Northwest region of the United States..."
        }
    ],
    "status": "completed"
}
```

Local testing helps you:

- Validate agent behavior before containerization
- Debug issues in your development environment
- Verify API compatibility with the Foundry Responses API

## Deploy using the Azure Developer CLI

The Azure Developer CLI `ai agent` extension provides the fastest path to deploy hosted agents.

> [!NOTE]
> This extension is currently in preview. Don't use it for production workloads.

### Install and configure the Azure Developer CLI

1. Verify you have Azure Developer CLI version 1.23.0 or later:

    ```bash
    azd version
    ```

    To upgrade, see [Install or update the Azure Developer CLI](/azure/developer/azure-developer-cli/install-azd).

1. Initialize a new project with the Foundry starter template:

    ```bash
    azd init -t https://github.com/Azure-Samples/azd-ai-starter-basic
    ```

    Or, if you have an existing Foundry project:

    ```bash
    azd ai agent init --project-id /subscriptions/[SUBSCRIPTIONID]/resourceGroups/[RESOURCEGROUPNAME]/providers/Microsoft.CognitiveServices/accounts/[ACCOUNTNAME]/projects/[PROJECTNAME]
    ```

### Configure your agent

Initialize the template with your agent definition:

```bash
azd ai agent init -m <repo-path-to-agent.yaml>
```

The agent repository should contain:

- Application code
- Dockerfile for containerization
- `agent.yaml` file with your agent's definition

Get started with samples on [GitHub](https://github.com/azure-ai-foundry/foundry-samples).

### Deploy your agent

Package, provision, and deploy in one command:

```bash
azd up
```

This command:

- Generates infrastructure configuration
- Provisions required Azure resources
- Builds and pushes your container image
- Creates a hosted agent version and deployment

### Verify deployment

```bash
az cognitiveservices agent show \
    --account-name <your-account-name> \
    --project-name <your-project-name> \
    --name <your-agent-name>
```

A successful deployment shows `status: Started`. If the status shows `Failed`, check the deployment logs.

## Deploy using the Python SDK

Use the SDK for programmatic deployments or CI/CD integration.

### Additional prerequisites

* A container image in [Azure Container Registry](/azure/container-registry/container-registry-get-started-portal)
* User Access Administrator or Owner permissions on the container registry
* Azure AI Projects SDK version 2.0.0b3 or later

    ```bash
    pip install --pre "azure-ai-projects>=2.0.0b3" azure-identity
    ```

### Build and push your container image

1. Build your Docker image:

    ```bash
    docker build -t myagent:v1 .
    ```

    See sample Dockerfiles for [Python](https://github.com/microsoft-foundry/foundry-samples/blob/main/samples/python/hosted-agents/agent-framework/agents-in-workflow/Dockerfile) and [C#](https://github.com/microsoft-foundry/foundry-samples/blob/main/samples/csharp/hosted-agents/AgentsInWorkflows/Dockerfile).

1. Push to Azure Container Registry:

    ```bash
    az acr login --name myregistry
    docker tag myagent:v1 myregistry.azurecr.io/myagent:v1
    docker push myregistry.azurecr.io/myagent:v1
    ```

### Configure container registry permissions

Grant your project's managed identity access to pull images:

1. In the [Azure portal](https://portal.azure.com), go to your Foundry project resource.

1. Select **Identity** and copy the **Object (principal) ID** under **System assigned**.

1. Assign the **Container Registry Repository Reader** role to this identity on your container registry. See [Azure Container Registry roles and permissions](/azure/container-registry/container-registry-roles).

### Create an account-level capability host

Hosted agents require a capability host with public hosting enabled:

# [Bash](#tab/bash)

```bash
az rest --method put \
    --url "https://management.azure.com/subscriptions/[SUBSCRIPTIONID]/resourceGroups/[RESOURCEGROUPNAME]/providers/Microsoft.CognitiveServices/accounts/[ACCOUNTNAME]/capabilityHosts/accountcaphost?api-version=2025-10-01-preview" \
    --headers "content-type=application/json" \
    --body '{
        "properties": {
            "capabilityHostKind": "Agents",
            "enablePublicHostingEnvironment": true
        }
    }'
```

# [PowerShell](#tab/powershell)

```powershell
az rest --method put `
    --url "https://management.azure.com/subscriptions/[SUBSCRIPTIONID]/resourceGroups/[RESOURCEGROUPNAME]/providers/Microsoft.CognitiveServices/accounts/[ACCOUNTNAME]/capabilityHosts/accountcaphost?api-version=2025-10-01-preview" `
    --headers "content-type=application/json" `
    --body '{
        "properties": {
            "capabilityHostKind": "Agents",
            "enablePublicHostingEnvironment": true
        }
    }'
```

---

> [!NOTE]
> Updating capability hosts isn't supported. If you have an existing capability host, delete and recreate it with `enablePublicHostingEnvironment` set to `true`.

### Create the hosted agent

```python
import os
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import ImageBasedHostedAgentDefinition, ProtocolVersionRecord, AgentProtocol
from azure.identity import DefaultAzureCredential

endpoint = os.environ["AZURE_AI_PROJECT_ENDPOINT"]

client = AIProjectClient(
    endpoint=endpoint,
    credential=DefaultAzureCredential()
)

agent = client.agents.create_version(
    agent_name="my-agent",
    definition=ImageBasedHostedAgentDefinition(
        container_protocol_versions=[ProtocolVersionRecord(protocol=AgentProtocol.RESPONSES, version="v1")],
        cpu="1",
        memory="2Gi",
        image="your-registry.azurecr.io/your-image:tag",
        environment_variables={
            "AZURE_AI_PROJECT_ENDPOINT": endpoint,
            "MODEL_NAME": "gpt-4.1"
        }
    )
)

print(f"Agent created: {agent.name}, version: {agent.version}")
```

Key parameters:

| Parameter | Description |
|-----------|-------------|
| `agent_name` | Unique name (alphanumeric with hyphens, max 63 characters) |
| `image` | Full Azure Container Registry image URL with tag |
| `cpu` | CPU allocation (for example, `"1"`) |
| `memory` | Memory allocation (for example, `"2Gi"`) |

### Add tools to your agent

Include tools when creating the agent:

```python
agent = client.agents.create_version(
    agent_name="my-agent",
    definition=ImageBasedHostedAgentDefinition(
        container_protocol_versions=[ProtocolVersionRecord(protocol=AgentProtocol.RESPONSES, version="v1")],
        cpu="1",
        memory="2Gi",
        image="your-registry.azurecr.io/your-image:tag",
        tools=[
            {"type": "code_interpreter"},
            {"type": "mcp", "project_connection_id": os.environ["GITHUB_CONNECTION_ID"]}
        ],
        environment_variables={
            "AZURE_AI_PROJECT_ENDPOINT": endpoint,
            "MODEL_NAME": "gpt-4.1"
        }
    )
)
```

Supported tools:

- Code Interpreter
- Image Generation
- Web Search
- MCP connections (see [Connect to Model Context Protocol servers](tools/model-context-protocol.md))

## Clean up resources

To prevent charges, clean up resources when finished.

### Azure Developer CLI cleanup

```bash
azd down
```

### SDK cleanup

```python
client.agents.delete_version(agent_name="my-agent", agent_version=agent.version)
```

## Troubleshooting

| Error | HTTP code | Solution |
|-------|-----------|----------|
| `SubscriptionIsNotRegistered` | 400 | Register the subscription provider |
| `InvalidAcrPullCredentials` | 401 | Fix managed identity or registry RBAC |
| `UnauthorizedAcrPull` | 403 | Provide correct credentials or identity |
| `AcrImageNotFound` | 404 | Correct image name/tag or publish image |
| `RegistryNotFound` | 400/404 | Fix registry DNS or network reachability |

For 5xx errors, contact Microsoft support.

## Next steps

> [!div class="nextstepaction"]
> [Manage hosted agent lifecycle](manage-hosted-agent.md)

## Related content

- [What are hosted agents?](../concepts/hosted-agents.md)
- [Agent identity concepts](../concepts/agent-identity.md)
- [Publish and share agents](publish-agent.md)
- [Azure Container Registry documentation](/azure/container-registry/)
