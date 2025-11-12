---
title: 'How to add an A2A agent endpoint to Foundry Agent Service'
titleSuffix: Microsoft Foundry
description: Learn how to use the A2A tool.
services: azure-ai-agent-service
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: how-to
ms.date: 09/12/2025
author: aahill
ms.author: aahi
ms.custom: azure-ai-agents
---

# Agent2Agent (A2A) tool (preview)

You can extend the capabilities of your Microsoft Foundry agent by connecting it to agent endpoints that support the [Agent2Agent (A2A) protocol](https://a2a-protocol.org/latest/) by using the A2A Tool. Developers and organizations maintain these agent endpoints. The A2A Tool makes sharing context between Foundry agents and external agent endpoints easier through a standardized protocol. 

Connecting agents via the A2A tool versus a multi-agent workflow:

- **Using the A2A tool**: When Agent A calls Agent B via A2A tool, Agent B's answer is passed back to Agent A, which then summarizes the answer and generates a response to the user. Agent A retains control and continues to handle future user input.
- **Using a multi-agent workflow**: When Agent A calls Agent B via a workflow or other multi-agent orchestration, the responsibility of answering the user is completely transferred to Agent B. Agent A is effectively out of the loop. All subsequent user input will be answered by Agent B.


## Usage support

|Azure AI foundry support  | Python SDK |	C# SDK | JavaScript SDK | Java SDK | REST API | Basic agent setup | Standard agent setup |
|---------|---------|---------|---------|---------|---------|---------|---------|
| ✔️  | - | - | - | - |  ✔️ | ✔️ | ✔️ | 

<!--
:::zone pivot="python"
:::zone end
-->

<!-- :::zone-pivot="rest-api"-->
## Create the remote A2A Foundry connection 

Use the following examples to store your authentication information. Adding an agent card path is optional. If not provided, `/.well-known/agent-card.json` is used by default.

### Key-based

```bash
curl --request PUT \
  --url 'https://{{region}}.management.azure.com/subscriptions/{{subscription_id}}//resourcegroups/{{resource_group_name}}/providers/Microsoft.CognitiveServices/accounts/{{foundry_account_name}}/projects/{{project_name}}/connections/{{connection_name}}?api-version=2025-04-01-preview' \
  --header 'Authorization: Bearer {{token against http://management.azure.com}}' \
  --header 'Content-Type: application/json' \
  --data '{
  "tags": null,
  "location": null,
  "type": "Microsoft.MachineLearningServices/workspaces/connections",
  "properties": {
    "authType": "CustomKeys",
    "group": "ServicesAndApps",
    "category": "RemoteA2A",
    "expiryTime": null,
    "target": "{{a2a_endpoint_endpoint}}",
    "isSharedToAll": true,
    "sharedUserList": [],
    "Credentials": {
      "Keys": {
        "{{key_name}}": "{{key_value}}"
      }
    },
    "metadata": {
      "ApiType": "Azure"
    },
    "agentCardPath": "" //optional
  }
}'
```
### Managed OAuth Identity Passthrough
These are only supported if you can "managed oauth" option in Foundry Tool Catalog.
```bash
curl --request PUT \
  --url 'https://{{region}}.management.azure.com/subscriptions/{{subscription_id}}//resourcegroups/{{resource_group_name}}/providers/Microsoft.CognitiveServices/accounts/{{foundry_account_name}}/projects/{{project_name}}/connections/{{connection_name}}?api-version=2025-04-01-preview' \
  --header 'Authorization: Bearer {{token against http://management.azure.com}}' \
  --header 'Content-Type: application/json' \
  --header 'User-Agent: insomnia/11.6.2' \
  --data '{
  "tags": null,
  "location": null,
  "type": "Microsoft.MachineLearningServices/workspaces/connections",
  "properties": {
    "authType": "OAuth2",
    "group": "ServicesAndApps",
    "category": "RemoteA2A",
    "expiryTime": null,
    "target": "{{a2a_endpoint_endpoint}}",
    "isSharedToAll": true,
    "sharedUserList": [],
    "useCustomConnector": false,
    "connectorName": {{connector_name}}              
    "Credentials": {
    },
    "metadata": {
      "ApiType": "Azure"
    },
    "agentCardPath": "" //optional
  }
}'
```
### Custom OAuth Identity Passthrough

Custom OAuth doesn't support update operation. Create a new one if you want to update certain values. 

```bash
curl --request PUT \
  --url 'https://{{region}}.management.azure.com:443/subscriptions/{{subscription_id}}//resourcegroups/{{resource_group_name}}/providers/Microsoft.CognitiveServices/accounts/{{foundry_account_name}}/projects/{{project_name}}/connections/{{connection_name}}?api-version=2025-04-01-preview' \
  --header 'Authorization: Bearer {{token against http://management.azure.com}}' \
  --header 'Content-Type: application/json' \
  --header 'User-Agent: insomnia/11.6.2' \
  --data '{
  "tags": null,
  "location": null,
  "type": "Microsoft.MachineLearningServices/workspaces/connections",
  "properties": {
    "authType": "OAuth2",
    "group": "ServicesAndApps",
    "category": "RemoteA2A",
    "expiryTime": null,
    "target": "{{a2a_endpoint_endpoint}}",
    "isSharedToAll": true,
    "sharedUserList": [],
  "TokenUrl": "{{token_url}}",
  "AuthorizationUrl": "{{auth_url}}",
  "RefreshUrl": "{{refresh_url}}",
  "Scopes": [
        "{{scope}}"
    ],
    "Credentials": {
      "ClientId": "{{client_id}}",
            "ClientSecret": "{{client_secret_optional}}", //optional
    },
    "metadata": {
      "ApiType": "Azure"
    },
    "agentCardPath": "" //optional
  }
}'
```
### Foundry Project Managed Identity
```bash
curl --request PUT \
  --url 'https://{{region}}.management.azure.com:443/subscriptions/{{subscription_id}}//resourcegroups/{{resource_group_name}}/providers/Microsoft.CognitiveServices/accounts/{{foundry_account_name}}/projects/{{project_name}}/connections/{{connection_name}}?api-version=2025-04-01-preview' \
  --header 'Authorization: Bearer {{token against http://management.azure.com}}' \
  --header 'Content-Type: application/json' \
  --header 'User-Agent: insomnia/11.6.2' \
  --data '{
  "tags": null,
  "location": null,
  "type": "Microsoft.MachineLearningServices/workspaces/connections",
  "properties": {
    "authType": "ProjectManagedIdentity",
    "group": "ServicesAndApps",
    "category": "RemoteA2A",
    "expiryTime": null,
    "target": "{{a2a_endpoint_endpoint}}",
    "isSharedToAll": true,
    "sharedUserList": [],
  "audience": "{{audience}}",
    "Credentials": {
    },
    "metadata": {
      "ApiType": "Azure"
    },
    "agentCardPath": "" //optional
  }
}'
```
### Agentic Identity
```bash
curl --request PUT \
  --url 'https://{{region}}.management.azure.com:443/subscriptions/{{subscription_id}}//resourcegroups/{{resource_group_name}}/providers/Microsoft.CognitiveServices/accounts/{{foundry_account_name}}/projects/{{project_name}}/connections/{{connection_name}}?api-version=2025-04-01-preview' \
  --header 'Authorization: Bearer {{token against http://management.azure.com}}' \
  --header 'Content-Type: application/json' \
  --header 'User-Agent: insomnia/11.6.2' \
  --data '{
  "tags": null,
  "location": null,
  "type": "Microsoft.MachineLearningServices/workspaces/connections",
  "properties": {
    "authType": "AgenticIdentity",
    "group": "ServicesAndApps",
    "category": "RemoteA2A",
    "expiryTime": null,
    "target": "{{a2a_endpoint_endpoint}}",
    "isSharedToAll": true,
    "sharedUserList": [],
  "audience": "{{audience}}",
    "Credentials": {
    },
    "metadata": {
      "ApiType": "Azure"
    },
    "agentCardPath": "" //optional
  }
}'
```
## Adding A2A tool to Foundry Agent Service
### Create an agent version with the A2A tool

```bash
curl --request POST \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/agents/$AGENTVERSION_NAME/versions?api-version=$API_VERSION \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{
  "description": "Test agent version description",
  "definition": {
    "kind": "prompt",
    "model": "{{model}}",
    "tools": [ 
      {
         "type": "a2a_preview",
         "base_url": "{{a2a_endpoint}}",
         "agent_card_path": {{agent_card_path_directory}} //optional
         "project_connection_id": "{{project_connection_name_above}}"
      }
    ],
    "instructions": "You are a helpful agent."
  }
}'
```
<!--:::zone end-->

## Considerations for using non-Microsoft services and servers 

Your use of connected non-Microsoft services and servers ("non-Microsoft services") is subject to the terms between you and the service provider. Non-Microsoft services are non-Microsoft Products under your agreement governing use of Microsoft Online services. When you connect to a non-Microsoft service, some of your data (such as prompt content) is passed to the non-Microsoft services, or your application might receive data from the non-Microsoft services. You're responsible for your use of non-Microsoft services and data, along with any charges associated with that use. 

The non-Microsoft services, including A2A agent endpoints, that you decide to use with the A2A tool described in this article were created by third parties, not Microsoft. Microsoft hasn't tested or verified these A2A agent endpoints. Microsoft has no responsibility to you or others in relation to your use of any non-Microsoft Services.  

We recommend that you carefully review and track the A2A agent endpoints you add to Foundry Agent Service. We also recommend that you rely on endpoints hosted by trusted service providers themselves rather than proxies. 

The A2A tool allows you to pass custom headers, such as authentication keys or schemas, that an A2A agent endpoint might need. We recommend that you review all data that's shared with non-Microsoft services, including A2A agent endpoints, and that you log the data for auditing purposes. Be cognizant of non-Microsoft practices for retention and location of data. 
