---
title: "Connect an AI gateway to Foundry Agent Service (preview)"
description: "Connect and use models hosted behind enterprise AI gateways like Azure API Management with Foundry Agent Service."
author: aahil
ms.author: aahi
ms.date: 04/09/2026
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.topic: how-to
ai-usage: ai-assisted
ms.custom: doc-kit-assisted
---

# Connect an AI gateway to Foundry Agent Service (preview)
Foundry Agent Service allows you to connect and use models hosted behind your enterprise AI gateways such as **Azure API Management** or other **non-Azure hosted AI model gateways**. This capability allows you to maintain control over your model endpoints while using Foundry agent capabilities.

> [!IMPORTANT]
> This feature is currently in preview. Preview features aren't meant for production use. For more information, see [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).

This capability enables organizations to:

- Maintain control over model endpoints behind existing enterprise infrastructure.
- Integrate securely with enterprise gateways using existing security policies.
- Build agents that use models without exposing them publicly.
- Apply compliance and governance requirements to AI model access.

:::image type="content" source="../media/gateway.png" alt-text="Diagram that shows the AI gateway architecture with flows from Agent Service to your gateway and models behind it." lightbox="../media/gateway.png":::

In this article, you create a gateway connection to your AI model endpoint, deploy a prompt agent that routes requests through the gateway, and verify the end-to-end flow.

## Prerequisites

- An Azure subscription. [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- A [Microsoft Foundry project](../../how-to/create-projects.md).
- [Azure CLI](/cli/azure/install-azure-cli) version 2.67 or later.
- [Python 3.10 or later](https://www.python.org/downloads/).
- The `azure-ai-projects` SDK package (version 2.0.0 or later). For installation steps, see the [quickstart](../../quickstarts/get-started-code.md).
- Access credentials for your enterprise AI gateway (for example, an API Management subscription key or an API key for another non-Azure AI model gateway).

### Required permissions

You need the following role assignments:

| Resource | Required role |
|----------|---------------|
| Foundry project | **Azure AI User** or higher |
| Resource group (for connection deployment) | **Contributor** |

## Create a gateway connection

Use the Azure CLI to create a connection to your AI gateway. Agent Service supports two connection types: **API Management (APIM)** connections and **Model Gateway** connections.

Choose the connection type that matches your gateway:

| Connection type | Use when | Category value |
|----------------|----------|----------------|
| **APIM** | You already use Azure API Management for model routing and want intelligent APIM defaults. | `ApiManagement` |
| **Model Gateway** | You use OpenAI, MuleSoft, or a custom gateway and need static or dynamic model discovery. | `ModelGateway` |

For detailed connection specifications, see the [connection samples on GitHub](https://github.com/microsoft-foundry/foundry-samples/blob/main/infrastructure/infrastructure-setup-bicep/01-connections/apim-and-modelgateway-integration-guide.md).

### Deploy the connection

1. Clone or download the [Foundry samples repository](https://github.com/microsoft-foundry/foundry-samples) and locate the Bicep template for your connection type under `infrastructure/infrastructure-setup-bicep/01-connections/`. The directory contains separate Bicep files and parameter files for APIM and Model Gateway connections.

1. Deploy the connection by running `az deployment group create` with your resource group, the Bicep template file, and the corresponding parameters file. Replace the placeholder values in the parameters file with your gateway endpoint URL and credentials before deploying. For the full command reference, see [az deployment group create](/cli/azure/deployment/group#az-deployment-group-create).

   > [!TIP]
   > A successful deployment returns `provisioningState: Succeeded` in the command output.

1. Verify the connection in the Foundry portal. Go to the [Foundry portal](https://ai.azure.com) and select your project. Navigate to **Connected resources** in your project settings. The new connection appears with an **Active** status and the gateway endpoint URL you specified.

## Create a prompt agent with the gateway connection

After creating the connection, create and run a prompt agent that uses models behind your gateway. The key difference from a standard agent is the model deployment name format: `<connection-name>/<model-name>`.

1. Set the following environment variables:

    | Variable | Value | Example |
    |----------|-------|---------|
    | `FOUNDRY_PROJECT_ENDPOINT` | Your project endpoint URL | `https://<your-ai-services-account>.services.ai.azure.com/api/projects/<project-name>` |
    | `FOUNDRY_MODEL_DEPLOYMENT_NAME` | `<connection-name>/<model-name>` | `my-apim-connection/gpt-4o` |

1. Initialize an `AIProjectClient` with your endpoint and `DefaultAzureCredential`, then call `agents.create_version()` with a `PromptAgentDefinition`. Set the `model` parameter to the `FOUNDRY_MODEL_DEPLOYMENT_NAME` value.

   A successful call returns an agent object with its `id`, `name`, and `version` fields populated.

1. Get the OpenAI client with `project.get_openai_client()`, create a conversation with `conversations.create()`, and send a request with `responses.create()`. Pass the agent reference in `extra_body` as `{"agent_reference": {"name": agent.name, "type": "agent_reference"}}`.

   A successful response returns the model's reply text, confirming the agent is routing through your gateway.

   > [!NOTE]
   > If the response fails with a `model not found` error, verify the `FOUNDRY_MODEL_DEPLOYMENT_NAME` value uses the format `<connection-name>/<model-name>`.

1. Clean up by deleting the conversation and agent version when testing is complete.

For a complete working example, see the [agent SDK samples on GitHub](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-projects/samples/agents). For API details, see [AIProjectClient](/python/api/azure-ai-projects/azure.ai.projects.aiprojectclient) and [PromptAgentDefinition](/python/api/azure-ai-projects/azure.ai.projects.models.promptagentdefinition).

## Verify the deployment

After deploying your agent, confirm that the full pipeline works correctly:

1. **Check connection status** — In the Foundry portal, navigate to **Connected resources** in your project settings. Verify the connection shows an **Active** status. If the status is **Inactive**, check the gateway endpoint URL and credentials.

1. **Send a test prompt** — Use the SDK to create a conversation and send a request as described in the previous section. A successful response returns the model's reply text, confirming the agent can reach the model through your gateway.

1. **Review gateway logs** — Confirm requests are routed correctly. For APIM, check **API Management analytics** in the Azure portal. For other gateways, review your gateway's request logging. You should see incoming requests from the Agent Service endpoint.

> [!TIP]
> If any step fails, see the [Troubleshoot common issues](#troubleshoot-common-issues) section for resolution steps.

## Connection type details

This section provides reference details about each connection type and their configuration options.

### API Management (APIM) connection

APIM connections provide intelligent defaults and follow APIM standard conventions:

| Setting | Default value |
|---------|---------------|
| List Deployments endpoint | `/deployments` |
| Get Deployment endpoint | `/deployments/{deploymentName}` |
| Provider | `AzureOpenAI` |

Configuration priority:

1. Explicit metadata values (highest priority).
1. APIM standard defaults (fallback).

Authentication:

- **API Key** — Standard subscription key authentication.
- **Microsoft Entra ID** — Enterprise identity integration.

### Model Gateway connection

Model Gateway connections provide a unified interface for connecting to various AI model providers. These connections support both static and dynamic model discovery:

- **Static discovery** — Models are predefined in the connection metadata. Best for fixed deployments and enterprise-approved model lists.
- **Dynamic discovery** — Models are discovered at runtime using API endpoints. Best for frequently changing deployments and provider-managed catalogs.

Supported authentication types are API key and OAuth 2.0. API keys are stored securely and referenced through the credential system.

## Troubleshoot common issues

| Issue | Resolution |
|-------|------------|
| Connection shows **Inactive** status | Verify the gateway endpoint URL is reachable and authentication credentials are valid. |
| Agent returns `model not found` error | Confirm the `FOUNDRY_MODEL_DEPLOYMENT_NAME` value uses the correct format: `<connection-name>/<model-name>`. |
| Timeout errors from the gateway | Check that your gateway endpoints are accessible from the Agent Service network. For private networks, see the network isolation guidance in the Limitations section. |
| Authentication failures | For APIM, verify your subscription key. For Model Gateway, verify the API key or OAuth 2.0 configuration. |

## Limitations

- This feature is in public preview.
- You can only use this feature through the Azure CLI and SDK.
- Only prompt agents in the Agent SDK support this feature.
- Supported agent tools: Code Interpreter, Functions, File Search, OpenAPI, Foundry IQ, SharePoint Grounding, Fabric Data Agent, MCP, and Browser Automation.
- Public networking is supported for both APIM and self-hosted gateways.
- For full network isolation:
  - **APIM as your AI gateway**: Deploy Foundry and APIM together using [this GitHub template](https://github.com/microsoft-foundry/foundry-samples/tree/main/infrastructure/infrastructure-setup-bicep/16-private-network-standard-agent-apim-setup-preview).
  - **Self-hosted gateway**: Ensure your gateway endpoints are accessible inside the virtual network used by Agent Service.
- This feature is different from the AI Gateway in Foundry feature, which deploys a new APIM instance with your Foundry resource. For more information, see [Enforce token limits with AI Gateway](/azure/ai-foundry/configuration/enable-ai-api-management-gateway-portal).

## Related content

- [Foundry Agent Service overview](../../agents/overview.md)
- [Agent environment setup](../../agents/environment-setup.md)
- [Create a Foundry project](../../how-to/create-projects.md)
- [Agent SDK samples on GitHub](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-projects/samples/agents)
- [APIM and model gateway integration guide](https://github.com/microsoft-foundry/foundry-samples/blob/main/infrastructure/infrastructure-setup-bicep/01-connections/apim-and-modelgateway-integration-guide.md)
- [Enforce token limits with AI Gateway](/azure/ai-foundry/configuration/enable-ai-api-management-gateway-portal)