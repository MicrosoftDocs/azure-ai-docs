---
title: Agent2Agent (A2A) authentication
titleSuffix: Microsoft Foundry
description: Learn about ways of adding authentication to the Agent2Agent tool in the Foundry Agent Service.
services: cognitive-services
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: how-to
ms.date: 10/10/2025
author: aahill
ms.author: aahi
---

# Authentication support in A2A tool
Most A2A endpoints will require you to authenticate in order to access the A2A endpoint and its underlying service. Authentication ensures that only authorized users can interact with each A2A endpoint.   

In general, there are two authentication scenarios: 

- **Shared authentication**: If you want every user of your agent to use the same identity to authenticate with the A2A endpoint, you can use key-based, Microsoft Entra – Agentic Identity, or Microsoft Entra – Foundry Project Managed Identity for authentication. The individual user identity or context doesn't persist with any of these methods. For example, if you're developing a chat agent for your organization’s users to retrieve information from Azure Cosmos DB, you might want every user of your agent to access the same folder or container in Azure Cosmos DB containing data accessible to all users in your organization, without requiring each user to authenticate with a unique identity.  
- **Individual authentication**: If you want every user of your agent to use their own account to authenticate with the A2A endpoint so that their personal user context persists, you can use OAuth Identity Passthrough. For example, if you're developing a coding agent for your developers and you want them to retrieve commits and pull requests from their GitHub repo, you might want each developer (user of your agent) to sign in and provide their account info so that the A2A endpoint can retrieve commits and pull requests from the developer’s individual account.  

## Supported authentication 
|Type  | Description |  User context persisted? |
|:---:| :----------: |:------------------------:|
| Key-based| Provide API key or access token to authenticate with the A2A endpoint | No |
| Microsoft Entra – Agentic Identity| Use your agent’s Agentic Identity to authenticate with the A2A endpoint. This Agentic Identity needs to have proper RBAC assignment to the underlying service | No |
|Microsoft Entra – Foundry Project Managed Identity |Use your Foundry Project’s Managed Identity to authenticate with the A2A endpoint. Your Foundry Project needs to have proper RBAC assignment to the underlying service | No |
|OAuth Identity Passthrough | Leverage OAuth to allow users interacting with your agent to sign in and authorize to the A2A endpoint.| Yes |
|Unauthenticated|No authentication is needed | No |

## Key-based authentication 

You can pass your API key, PAT token, and other credentials to A2A endpoints supporting key-based authentication. With Foundry Agent Service, we recommend you put your credentials in the Foundry connection instead of manually passing each time during runtime for improved security. When you connect your A2A endpoint to an agent in the Foundry portal, a Foundry connection will be automatically created for you. You need to provide the credential name and credential value. For example, if you're trying to connect with a key-based A2A endpoint, you can select to use key-based authentication to pass your personal access token. The credential name is `Authorization` and the credential value is `Bearer < your bearer token >`. 

When the agent invokes the A2A endpoint, it will retrieve the credentials from your Foundry Connection and pass them to the A2A endpoint for authentication. 

## Microsoft Entra 

### Agentic identity 

You can use your agent’s Agentic Identity to authenticate with A2A endpoints that support authenticating with Agentic Identity. If your agent is created with Foundry Agent Service, your agent will automatically be assigned an Agentic Identity. All agents in your Foundry Project will share the same Agentic Identity before publishing. After you publish an agent, your agent will be assigned a unique Agentic Identity. When you choose to authenticate with Agentic Identity, Foundry Agent Service will use the shared Agentic Identity if the agent hasn’t been published and therefore doesn’t have a unique Agentic Identity; it will use the unique Agentic Identity if the agent has been published and has a unique Agentic Identity.  

You need to make sure your Agentic Identity has the proper RBAC role to the underlying service powering the A2A endpoint. <!--(please refer to the A2A endpoint documentation for specific RBAC roles needed)--> When you're connecting an A2A endpoint to your agent, you need to specify the scope URI of the service, for example, when you're connecting to Microsoft Foundry A2A endpoint, the scope URI is `http://ai.azure.com`.  

When the agent invokes the A2A endpoint, it will use the available Agentic Identity to get its authorization token from the scope URI and pass it to the A2A endpoint for authentication.  

### Foundry project managed identity 

You can use your Foundry Project's Managed Identity to authenticate with A2A endpoints that support authenticating with Managed Identity. You need to make sure your Foundry Project’s Managed Identity has the proper RBAC role to the underlying service powering the A2A endpoint. <!--(please refer to the A2A endpoint documentation for specific RBAC roles needed)--> When you're connecting the A2A endpoint to your agent, you need to specify the scope URI of the service, for example, when you're connecting to Foundry A2A endpoint, the scope URI is `http://ai.azure.com`.  

When the agent invokes the A2A endpoint, it will use the Foundry Project’s Managed Identity to get its authorization token from the scope URI and pass it to the A2A endpoint for authentication. 

## OAuth identity passthrough 

> [!NOTE]
> To use OAuth identity passthrough, your users interacting with your agent need to have at least `Azure AI User` Role 

OAuth identity passthrough is available for authentication to Microsoft and non-Microsoft A2A endpoints and underlying services compliant with OAuth, including Microsoft Entra 

You can use OAuth identity passthrough to prompt users interacting with your agent to sign into the A2A endpoint and its underlying service and grant the agent the ability to use the user's credentials when interacting with the A2A endpoint. Foundry Agent Service securely stores the user's credentials and uses them only within the context of the agent communicating with the A2A endpoint. Importantly, OAuth doesn't grant a non-Microsoft app or service unlimited access to the user's data. Part of the protocol is specifying what data the non-Microsoft party is allowed to access and what it can do with that data. See the [Microsoft security](https://www.microsoft.com/security/business/security-101/what-is-oauth) documentation for more information.

When you use OAuth identity passthrough, the agent will need to use credentials from the user interacting with the agent to connect to the A2A endpoint. The first time a particular user interacts with the agent, Foundry Agent Service will generate a consent link, which the user can accept to log into the identity provider associated with the A2A endpoint. After the user logs in and consents to allow Foundry Agent Service to use their credentials to communicate with the A2A endpoint, the agent is able to discover and invoke tools on the A2A endpoint with the user's credentials. 

The user's OAuth credentials are stored securely and scoped to the particular user and the particular agent they interacted with. These credentials are generally a refresh token and an access token. <!--(explanation of the types of tokens here)--> 

There are usually two tokens involved in OAuth flow: refresh token and access token. 

**Access Token**:
- Used to call APIs (for example Microsoft Graph, GitHub).
- Short-lived by design. Usually minutes to an hour (commonly 1 hour).
- Purpose: limit the damage if stolen.
- When it expires, the OAuth App can use a refresh token (if available) to get a new one. 

**Refresh Token**
- Used only to get new access tokens.
- Longer-lived. Can last hours, days, weeks, or even “until revoked” depending on server settings.
- Can often be revoked by the user (for example, using account settings).
- Some providers rotate refresh tokens each time they’re used (for extra security). 

Foundry Agent Service supports two OAuth options: **Managed OAuth** and **Custom OAuth**. With Managed OAuth, the OAuth App is managed by Microsoft or the A2A endpoint publisher. With Custom OAuth, you bring your own OAuth App. The OAuth App is a client application that registers with an OAuth provider (such as Microsoft, or GitHub) and uses the flow above to get the necessary OAuth token. The benefit of Custom OAuth is that you can customize the consent link content for your organization and application. For example, with Custom OAuth, Contoso can ask users of its agent to give permission to Contoso to pass the user’s credentials to the A2A endpoint. If you want to use Custom OAuth, you will need to provide all required information, including a client ID, client secret, authorization URL, token URL, refresh URL, and suggested scopes.  

> [!NOTE]
> If you decide to use Custom OAuth and provide all information above, you will then get a redirect URL. Make sure to add this redirect URL to your OAuth app, as it will delegate the handling of the access token to enable use of your connection.  

### Unauthenticated 

This is supported if the A2A endpoint doesn’t require authentication.  
