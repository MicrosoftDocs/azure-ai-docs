---
title: Bring your own AI gateway to Azure AI Agent Service (preview)
titleSuffix: Microsoft Foundry
description: "Learn how to connect and use models hosted behind your enterprise AI gateways."
author: aahil
ms.author: aahi
ms.date: 11/10/2025
ms.service: azure-ai-foundry
ms.topic: how-to
---

# Bring your own AI gateway to Azure AI Agent Service (preview)

The Azure AI Agent Service allows you to connect and use models hosted behind your enterprise AI gateways such as **Azure API Management** or other **non-Azure hosted AI model gateways**. This capability allows you to maintain control over your model endpoints while leveraging the power of Foundry's agent capabilities.

> [!NOTE]
> This feature is currently in preview. Consider the preview conditions before enabling this feature. 

This capability enables organizations to:

- Maintain control over their model endpoints. Keep your model endpoints secure behind your existing enterprise infrastructure. 
- Integrate securely with enterprise gateways. Leverage your existing gateway investments and security policies.
- Build agents that leverage models without exposing them publicly.
- Apply your organization's compliance and governance requirements to AI model access.

View the diagram to understand the potential flows from the Agent service to your gateway and models behind it:

:::image type="content" source="../media/gateway.png" alt-text="A diagram explaining the AI gateway feature and potential gateways to use." lightbox="../media/gateway.png":::

## Prerequisites

- An Azure subscription with access to Microsoft Foundry. Create a Foundry resource in your subscription. 
- Installed **Azure CLI** and **Agent SDK**.
- Access credentials for your enterprise AI gateway (for example API Management or another non-Azure AI model gateway).
- GitHub access for [Foundry samples](https://github.com/azure-ai-foundry/foundry-samples/blob/main/infrastructure/infrastructure-setup-bicep/01-connections/apim-and-modelgateway-integration-guide.md)

## Connections for AI gateway

Depending on the AI gateway you would like to use, there are two different connections you can create to your resource from Microsoft Foundry. For more details on these connections, see the samples [on GitHub](https://github.com/azure-ai-foundry/foundry-samples/blob/main/infrastructure/infrastructure-setup-bicep/01-connections/apim-and-modelgateway-integration-guide.md)

## API Management (APIM) connection 
APIM connections are specialized model gateway connections designed for Azure API management scenarios. These connections provide intelligent defaults and follow APIM standard conventions while integrating with the broader model gateway ecosystem.

Connections provide:

- **APIM category**: Uses `"category": "ApiManagement"` for proper APIM-specific handling.
- **Intelligent defaults**: Provides standard APIM endpoints when metadata is not specified.
- **Convention-based**: Follows Azure API management naming and routing patterns.
- **Flexible override**: Supports metadata overrides for custom APIM configurations.
- **Enterprise ready**: Designed for production APIM gateway scenarios.

### APIM specific behavior

- **Default endpoints**: When metadata is not provided, APIM connections use these defaults:
  - List Deployments: `/deployments`
  - Get Deployment: `/deployments/{deploymentName}`
  - Provider: `AzureOpenAI`

- **Configuration priority**:
  1. Explicit metadata values (highest priority)
  2. APIM standard defaults (fallback)

- **Authentication patterns**:
  - **API Key**: Standard subscription key authentication
  - **Microsoft Entra ID**: Enterprise identity integration is coming soon. 

## Model gateway connection  

Model gateway connections provide a unified interface for connecting to various AI model providers through the Azure Machine Learning workspace connection framework. These connections support both static model configuration (predefined models) and dynamic model discovery (runtime model detection). Model gateway connections provide:

- **Unified API**: Single connection interface for multiple AI providers (Azure AI, OpenAI, MuleSoft, etc.)
- **Authentication**: Support for API key authentication with workspace credential management or OAuth2
- **Discovery Patterns**: Choose between static model lists or dynamic discovery endpoints
- **Provider Abstraction**: Consistent model format regardless of underlying provider
- **Enterprise Integration**: Support for enterprise gateways like MuleSoft for multi-provider scenarios

### Connection categories

All ModelGateway connections use `"category": "ModelGateway"` to ensure proper routing through the model gateway service infrastructure.

#### Discovery Methods

- **Static Discovery**: Models are predefined in the connection metadata using the models array. Best for:
  - Dynamic discovery not possible
  - Fixed model deployments
  - Known model configurations
  - Enterprise scenarios with approved model lists

- **Dynamic Discovery**: Models are discovered at runtime using API endpoints defined in modelDiscovery. Best for:
  - Frequently changing model deployments
  - Provider-managed model catalogs
  - Development and testing scenarios

## Authentication Types 

The supported authentication types are API key or OAuth 2.0, depending on the connection type. For API Keys, the actual API keys are stored securely and referenced through the credential system. 

## Create a model gateway connection

You’ll use the Azure CLI to create a connection of type **model gateway**.

1. Navigate to the connection samples [on GitHub](https://github.com/azure-ai-foundry/foundry-samples/blob/main/infrastructure/infrastructure-setup-bicep/01-connections/apim-and-modelgateway-integration-guide.md). Select your model gateway connection depending on your requirements.

1. Run the `az deployment group create` command to create the connection. For example:
    
    ```bash
    az deployment group create \
      --resource-group <your-resource-group> \
      --template-file [bicep-file-of-connection-type].bicep \
      --parameters @[parameters-file-of-connection-type].json
    ```
1. View your successful connection creation by navigating to **Admin** in the Microsoft Foundry portal. 
## Deploy a prompt agent using the SDK 

After creating the connection, deploy a prompt agent that uses the model gateway connection. 

1. Navigate to the [Agents SDK samples](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-projects/samples/agents) to run a sample agent with the BYO AI gateway feature. 

1. Use the Agent SDK to deploy the agent. Update the env variable so that the model name is `[connection-name]/[model-name]`. For example: `AZURE_AI_MODEL_DEPLOYMENT_NAME=my-apim-deployment-api-v2/gpt-4o `
 
## Validation 

* Confirm the connection is active in Foundry. You should see the connection in the Foundry portal under **Operate** --> **Admin** --> **Projects** --> **Connected resources**. 
* Test the deployed prompt agent by sending a sample prompt. 

## Limitations

- This feature is in public preview.
- You can only use this feature using the Azure CLI and SDK.
- Supported by Prompt Agents in the Agent SDK.
- Public networking is supported for either APIM or other self-hosted gateways. For a full network isolation set up, set up Foundry with Standard Secured Agents set-up with virtual network injection. If you are using APIM as your AI gateway and want full network isolation, deploy Foundry and APIM following [this GitHub template](https://github.com/azure-ai-foundry/foundry-samples/tree/main/infrastructure/infrastructure-setup-bicep/16-private-network-standard-agent-apim-setup-preview). If you're using your self-hosted gateway as your AI gateway and want full network isolation, ensure that your gateway's endpoints are accessible inside the virtual network injection used by the Agent service. 
- The Agent tools supported with this feature are CodeInterpreter, Functions, File Search, OpenAPI, Foundry IQ, Sharepoint Grounding, Fabric Data Agent, MCP, and Browser Automation.
- This feature is different from the AI Gateway in Foundry feature where a new, unique APIM instance is deployed with your Foundry resource. For more on this feature, see [Enforce token limits with AI Gateway](/azure/ai-foundry/configuration/enable-ai-api-management-gateway-portal).
