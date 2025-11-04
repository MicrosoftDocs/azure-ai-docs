---
title: 'How to add an A2A agent endpoint to Foundry Agent Service'
titleSuffix: Azure AI Foundry
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

You can extend the capabilities of your Azure AI Foundry agent by connecting it to agent endpoints that support the [Agent2Agent (A2A) protocol](https://a2a-protocol.org/latest/) by using the A2A Tool. Developers and organizations maintain these agent endpoints. The A2A Tool makes sharing context between AI Foundry agents and external agent endpoints easier through a standardized protocol. 

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
## Create the remote A2A AI Foundry connection 

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

We recommend that you carefully review and track the A2A agent endpoints you add to AI Foundry Agent Service. We also recommend that you rely on endpoints hosted by trusted service providers themselves rather than proxies. 

The A2A tool allows you to pass custom headers, such as authentication keys or schemas, that an A2A agent endpoint might need. We recommend that you review all data that's shared with non-Microsoft services, including A2A agent endpoints, and that you log the data for auditing purposes. Be cognizant of non-Microsoft practices for retention and location of data. 

## Authentication support in A2A tool
Most A2A endpoints will require you to authenticate in order to access the A2A endpoint and its underlying service. Authentication ensures that only authorized users can interact with each A2A endpoint.   

In general, there are two authentication scenarios: 

- **Shared authentication**: If you want every user of your agent to use the same identity to authenticate with the A2A endpoint, you can use key-based, Microsoft Entra – Agentic Identity, or Microsoft Entra – Foundry Project Managed Identity for authentication. The individual user identity or context does not persist with any of these methods. For example, if you are developing a chat agent for your organization’s users to retrieve information from Azure Cosmos DB, you may want every user of your agent to access the same folder or container in Azure Cosmos DB containing data accessible to all users in your organization, without requiring each user to authenticate with a unique identity.  
- **Individual authentication**: If you want every user of your agent to use their own account to authenticate with the A2A endpoint so that their personal user context persists, you can use OAuth Identity Passthrough. For example, if you are developing a coding agent for your developers and you want them to retrieve commits and pull requests from their GitHub repo, you may want each developer (user of your agent) to sign in and provide their account info so that the A2A endpoint can retrieve commits and pull requests from the developer’s individual account.  

### Supported Authentication 
|Type  | Description |  User context persisted? |
|:---:| :----------: |:------------------------:|
| Key-based| Provide API key or access token to authenticate with the A2A endpoint | No |
| Microsoft Entra – Agentic Identity| Use your agent’s Agentic Identity to authenticate with the A2A endpoint. This Agentic Identity needs to have proper RBAC assignment to the underlying service | No |
|Microsoft Entra – Foundry Project Managed Identity |Use your Foundry Project’s Managed Identity to authenticate with the A2A endpoint. Your Foundry Project needs to have proper RBAC assignment to the underlying service | No |
|OAuth Identity Passthrough | Leverage OAuth to allow users interacting with your agent to sign in and authorize to the A2A endpoint.| Yes |
|Unauthenticated|No authentication is needed | No |

### Key-based Authentication 

You can pass your API key, PAT token, and other credentials to A2A endpoints supporting key-based authentication. With AI Foundry Agent Service, we recommend you put your credentials in the AI Foundry connection instead of manually passing each time during runtime for improved security. When you connect your A2A endpoint to an agent in the AI Foundry portal, an AI Foundry connection will be automatically created for you. You need to provide the credential name and credential value. For example, if you are trying to connect with a key-based A2A endpoint, you can select to use key-based authentication to pass your personal access token. The credential name is `Authorization` and the credential value is `Bearer < your bearer token >`. 

When the agent invokes the A2A endpoint, it will retrieve the credentials from your Foundry Connection and pass them to the A2A endpoint for authentication. 

### Microsoft Entra 

#### Agentic Identity 

You can use your agent’s Agentic Identity to authenticate with A2A endpoints that support authenticating with Agentic Identity. If your agent is created with Foundry Agent Service, your agent will automatically be assigned an Agentic Identity. All agents in your Foundry Project will share the same Agentic Identity before publishing. After you publish an agent, your agent will be assigned a unique Agentic Identity. When you choose to authenticate with Agentic Identity, Foundry Agent Service will use the shared Agentic Identity if the agent hasn’t been published and therefore doesn’t have a unique Agentic Identity; it will use the unique Agentic Identity if the agent has been published and has a unique Agentic Identity.  

You need to make sure your Agentic Identity has the proper RBAC role to the underlying service powering the A2A endpoint <!--(please refer to the A2A endpoint documentation for specific RBAC roles needed)-->. When you are connecting an A2A endpoint to your agent, you need to specify the scope URI of the service, for example, when you are connecting to Azure AI Foundry A2A endpoint, the scope URI is `http://ai.azure.com`.  

When the agent invokes the A2A endpoint, it will use the available Agentic Identity to get its authorization token from the scope URI and pass it to the A2A endpoint for authentication.  

#### Foundry Project Managed Identity 

You can use your Foundry Project's Managed Identity to authenticate with A2A endpoints that support authenticating with Managed Identity. You need to make sure your Foundry Project’s Managed Identity has the proper RBAC role to the underlying service powering the A2A endpoint <!--(please refer to the A2A endpoint documentation for specific RBAC roles needed)-->. When you are connecting the A2A endpoint to your agent, you need to specify the scope URI of the service, for example, when you are connecting to Azure AI Foundry A2A endpoint, the scope URI is `http://ai.azure.com`.  

When the agent invokes the A2A endpoint, it will use the Foundry Project’s Managed Identity to get its authorization token from the scope URI and pass it to the A2A endpoint for authentication. 

### OAuth Identity Passthrough 

> [!NOTE]
> To use OAuth Identity Passthrough, your users interacting with your agent need to have at least `Azure AI User` Role 

OAuth Identity Passthrough is available for authentication to Microsoft and non-Microsoft A2A endpoints and underlying services compliant with OAuth, including Microsoft Entra 

You can use OAuth Identity Passthrough to prompt users interacting with your agent to sign into the A2A endpoint and its underlying service and grant the agent the ability to use the user's credentials when interacting with the A2A endpoint. AI Foundry Agent Service securely stores the user's credentials and uses them only within the context of the agent communicating with the A2A endpoint. Importantly, OAuth does not grant a non-Microsoft app or service unlimited access to the user's data. Part of the protocol is specifying what data the non-Microsoft party is allowed to access and what it can do with that data. See the [Microsoft security](https://www.microsoft.com/security/business/security-101/what-is-oauth) documentation for more information.

When you use OAuth Identity Passthrough, the agent will need to use credentials from the user interacting with the agent to connect to the A2A endpoint. The first time a particular user interacts with the agent, AI Foundry Agent Service will generate a consent link, which the user can accept to log into the identity provider associated with the A2A endpoint. After the user logs in and consents to allow AI Foundry Agent Service to use their credentials to communicate with the A2A endpoint, the agent is able to discover and invoke tools on the A2A endpoint with the user's credentials. 

The user's OAuth credentials are stored securely and scoped to the particular user and the particular agent they interacted with. These credentials are generally a refresh token and an access token. (explanation of the types of tokens here) 

There are usually two tokens involved in OAuth flow: refresh token and access token. 

**Access Token**:
- Used to call APIs (for example Microsoft Graph, GitHub).
- Short-lived by design — usually minutes to an hour (commonly 1 hour).
- Purpose: limit the damage if stolen.
- When it expires, the OAuth App can use a refresh token (if available) to get a new one. 

**Refresh Token**
- Used only to get new access tokens.
- Longer-lived — can last hours, days, weeks, or even “until revoked” depending on server settings.
- Can often be revoked by the user (e.g., via account settings).
- Some providers rotate refresh tokens each time they’re used (for extra security). 

Foundry Agent Service supports two OAuth options: **Managed OAuth** and **Custom OAuth**. With Managed OAuth, the OAuth App is managed by Microsoft or the A2A endpoint publisher. With Custom OAuth, you bring your own OAuth App. The OAuth App is a client application that registers with an OAuth provider (such as Microsoft, GitHub, etc,) and uses the flow above to get the necessary OAuth token. The benefit of Custom OAuth is that you can customize the consent link content for your organization and application. For example, with Custom OAuth, Contoso can ask users of its agent to give permission to Contoso to pass the user’s credentials to the A2A endpoint. If you want to use Custom OAuth, you will need to provide all required information, including a client ID, client secret, authorization URL, token URL, refresh URL, and suggested scopes.  

> [!NOTE]
> If you decide to use Custom OAuth and provide all information above, you will then get a redirect URL. Make sure to add this redirect URL to your OAuth app, as it will delegate the handling of the access token to enable use of your connection.  

### Unauthenticated 

This is supported if the A2A endpoint doesn’t require authentication.  
