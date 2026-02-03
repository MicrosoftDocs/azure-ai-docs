---
title: Agent2Agent (A2A) authentication
titleSuffix: Microsoft Foundry
description: Learn about ways of adding authentication to the Agent2Agent tool in the Foundry Agent Service.
services: cognitive-services
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: how-to
ms.date: 01/21/2026
author: aahill
ms.author: aahi
ms.custom: pilot-ai-workflow-jan-2026
ai-usage: ai-assisted
---

# Agent2Agent (A2A) authentication

Most Agent2Agent (A2A) endpoints require authentication to access the endpoint and its underlying service. Authentication ensures only authorized users can invoke your A2A tools in Microsoft Foundry Agent Service (Agent Service).

In general, there are two authentication scenarios: 

- **Shared authentication**: Every user of your agent uses the same identity to authenticate to the A2A endpoint. Individual user context doesn't persist. For example, if you build a chat agent to retrieve information from Azure Cosmos DB for your organization, you might want every user to access the same shared container without signing in.
- **Individual authentication**: Each user of your agent authenticates with their own account so their user context persists. For example, if you build a coding agent that retrieves commits and pull requests from GitHub, you might want each developer to sign in with their own GitHub account.

## Prerequisites

Before you choose an authentication method, you need:

- Access to the [Foundry portal](https://ai.azure.com/?cid=learnDocs) and a project. If you don't have one, see [Create projects in Foundry](../../../how-to/create-projects.md).
- Permissions to create project connections and configure agents. For details, see [Role-based access control in the Foundry portal](../../../concepts/rbac-foundry.md).
- The A2A endpoint URL you want to connect to, and which authentication methods it supports.
- Credentials for your selected authentication method:
  - Key-based: an API key, personal access token (PAT), or other token.
  - Microsoft Entra authentication: role assignments for the agent identity or project managed identity on the underlying service.
  - OAuth identity passthrough: a managed OAuth option from the endpoint publisher, or an OAuth app registration (custom OAuth).

## Choose an authentication method

Use the following guidance to choose a method:

| Your goal | Recommended method |
| --- | --- |
| Use one shared identity for all users | Key-based authentication or Microsoft Entra authentication |
| Preserve each user's identity and permissions | OAuth identity passthrough |
| Avoid managing secrets when the underlying service supports Microsoft Entra | Microsoft Entra authentication |
| Connect to an A2A endpoint that doesn't require auth | Unauthenticated access |

## Supported authentication methods

| Method | Description | User context persists |
| --- | --- | --- |
| Key-based | Provide an API key or access token to authenticate with the A2A endpoint. | No |
| Microsoft Entra - agent identity | Use the agent identity to authenticate with the A2A endpoint. Assign the required roles on the underlying service. | No |
| Microsoft Entra - project managed identity | Use the project managed identity to authenticate with the A2A endpoint. Assign the required roles on the underlying service. | No |
| OAuth identity passthrough | Prompt users interacting with your agent to sign in and authorize access to the A2A endpoint. | Yes |
| Unauthenticated access | Use this method only when the A2A endpoint doesn't require authentication. | No |

## Key-based authentication

> [!NOTE]
> People who have access to the project can access a secret stored in a project connection. Store only shared secrets in a project connection. For user-specific access, use OAuth identity passthrough.

Pass an API key, a personal access token (PAT), or other credentials to A2A endpoints that support key-based authentication. For improved security, store shared credentials in a project connection instead of passing them at runtime.

When you connect your A2A endpoint to an agent in the Foundry portal, Foundry creates a project connection for you. Provide the credential name and credential value. For example:

- Credential name: `Authorization`
- Credential value: `Bearer <your-token>`

When the agent invokes the A2A endpoint, Agent Service retrieves the credentials from the project connection and passes them to the A2A endpoint.

For security:

- Use least-privilege credentials where possible.
- Rotate tokens regularly.
- Restrict access to projects that contain shared secrets.

## Microsoft Entra authentication

Use Microsoft Entra authentication when the A2A endpoint and its underlying service accept Microsoft Entra tokens.

### Agent identity

Use your agent identity to authenticate with A2A endpoints that support agent identity authentication. If you create your agent by using Agent Service, you automatically assign an agent identity to it.

Before publishing, agents in the same project share a common identity. After you publish an agent, it gets a unique identity. For background and identity lifecycle details, see [Agent identity concepts in Microsoft Foundry](agent-identity.md).

Make sure the agent identity has the required role assignments on the underlying service that powers the A2A endpoint.

When the agent invokes the A2A endpoint, Agent Service uses the available agent identity to request an authorization token and passes it to the A2A endpoint.

### Foundry project managed identity

Use your Foundry project's managed identity to authenticate with A2A endpoints that support managed identity authentication.

Make sure the project managed identity has the required role assignments on the underlying service that powers the A2A endpoint.

When the agent invokes the A2A endpoint, Agent Service uses the project's managed identity to request an authorization token and passes it to the A2A endpoint.

## OAuth identity passthrough

> [!NOTE]
> To use OAuth identity passthrough, users interacting with your agent need at least the **Azure AI User** role on the project.

OAuth identity passthrough is available for authentication to Microsoft and non-Microsoft A2A endpoints and underlying services that are compliant with OAuth, including Microsoft Entra.

Use OAuth identity passthrough to prompt users interacting with your agent to sign in to the A2A endpoint and its underlying service. Agent Service securely stores the user's credentials and uses them only within the context of the agent communicating with the A2A endpoint.

OAuth doesn't grant unlimited access to a user's data. Part of the protocol is specifying what the A2A endpoint can access and what it can do. For more information, see the [Microsoft security](https://www.microsoft.com/security/business/security-101/what-is-oauth) documentation.

When you use OAuth identity passthrough, the agent uses credentials from the user interacting with the agent to connect to the A2A endpoint. The first time a user interacts with the agent, Agent Service generates a consent link. After the user signs in and consents, the agent can discover and invoke tools on the A2A endpoint with that user's credentials.

The user's OAuth credentials are stored securely and scoped to the specific user and the specific agent they interacted with. These credentials typically include a refresh token and an access token.

An OAuth flow typically uses two tokens.

**Access token**
- Used to call APIs (for example Microsoft Graph, GitHub).
- Short-lived by design. Usually minutes to an hour (commonly 1 hour).
- Purpose: limit the damage if stolen.
- When it expires, the OAuth app can use a refresh token (if available) to get a new one. 

**Refresh token**
- Used only to get new access tokens.
- Longer-lived. Can last hours, days, weeks, or even “until revoked” depending on server settings.
- Can often be revoked by the user (for example, using account settings).
- Some providers rotate refresh tokens each time they’re used (for extra security). 

Agent Service supports two OAuth options: **managed OAuth** and **custom OAuth**.

- With managed OAuth, Microsoft or the A2A endpoint publisher manages the OAuth app.
- With custom OAuth, you bring your own OAuth app registration.

If you use custom OAuth, provide the required information, such as a client ID, client secret (if required), authorization URL, token URL, refresh URL, and requested scopes.

> [!NOTE]
> If you use custom OAuth, you get a redirect URL. Add it to your OAuth app registration so Agent Service can complete the flow.

## Unauthenticated access

Use unauthenticated access only when the A2A endpoint doesn't require authentication.

## Set up authentication for an A2A connection

1. Identify the A2A endpoint you want to connect to and the authentication method it supports.
1. Create or select a project connection that stores the A2A endpoint URL, authentication method, and any required credentials.

   - For general connection guidance, see [Add a new connection to your project](../../../how-to/connections-add.md).
   - For A2A-specific connection configuration and end-to-end A2A tool setup, see [Add an A2A agent endpoint to Foundry Agent Service](../how-to/tools/agent-to-agent.md).

1. Configure your agent to use the A2A tool and reference the project connection.

## Validate

1. Trigger an A2A tool call from your agent.
1. Confirm the tool call completes successfully.
1. If you're using OAuth identity passthrough, confirm a new user gets a consent link and that subsequent calls succeed after the user consents.

## Troubleshooting

| Issue | Cause | Resolution |
| --- | --- | --- |
| Key-based authentication fails | Invalid or expired token, or the endpoint expects a different header name or value format | Regenerate or rotate the credential and update the project connection. Confirm the required header name and value format in the endpoint documentation. |
| Microsoft Entra authentication fails | The identity doesn't have the required role assignments on the underlying service | Assign the required roles to the agent identity or project managed identity on the underlying service, and then try again. |
| Consent completes but tool calls still fail | The user doesn't have access in the underlying service | Confirm the user has access to the underlying service and has the **Azure AI User** role (or higher) on the project. |
| You don't get a consent link when you expect one | OAuth identity passthrough isn't configured for the connection, or the agent didn't invoke the A2A tool | Confirm the project connection is configured for OAuth identity passthrough and trigger an A2A tool call again. |

## Next steps

- [Add an A2A agent endpoint to Foundry Agent Service](../how-to/tools/agent-to-agent.md)
- [Agent identity concepts in Microsoft Foundry](agent-identity.md)
- [Role-based access control for Microsoft Foundry](../../../concepts/rbac-foundry.md)
- [Add a new connection to your project](../../../how-to/connections-add.md)
