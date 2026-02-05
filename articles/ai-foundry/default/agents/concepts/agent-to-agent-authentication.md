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

The Agent2Agent (A2A) protocol enables your agents to discover and invoke tools exposed by other agents. Most A2A endpoints require authentication to access the endpoint and its underlying service. Configuring authentication ensures that only authorized users can invoke your A2A tools in Foundry Agent Service (Agent Service).

This article explains the authentication methods available for A2A connections and helps you choose the right approach for your scenario.

## Authentication scenarios

In general, there are two authentication scenarios: 

- **Shared authentication**: Every user of your agent uses the same identity to authenticate to the A2A endpoint. Individual user context doesn't persist. This approach is ideal when all users should have the same level of access. For example, if you build a chat agent to retrieve information from Azure Cosmos DB for your organization, you might want every user to access the same shared container without requiring individual sign-in.
- **Individual authentication**: Each user of your agent authenticates with their own account, so their user context persists across interactions. This approach is essential when actions should be scoped to the user's permissions. For example, if you build a coding agent that retrieves commits and pull requests from GitHub, you want each developer to sign in with their own GitHub account so they only see repositories they have access to.

## Prerequisites

Before you choose an authentication method, you need:

- Access to the [Foundry portal](https://ai.azure.com/?cid=learnDocs) and a project. If you don't have one, see [Create projects in Foundry](../../../how-to/create-projects.md).
- The **Azure AI Developer** role or higher on your project. This role grants permissions to create project connections and configure agents. For details, see [Role-based access control in the Foundry portal](../../../concepts/rbac-foundry.md).
- The A2A endpoint URL you want to connect to. Contact the endpoint publisher to confirm which authentication methods the endpoint supports.
- Credentials for your selected authentication method:
  - **Key-based**: An API key, personal access token (PAT), or other secret token from the endpoint publisher.
  - **Microsoft Entra authentication**: Role assignments for the agent identity or project managed identity on the underlying service. The specific roles depend on the service (for example, **Cosmos DB Data Reader** for Azure Cosmos DB).
  - **OAuth identity passthrough**: A managed OAuth option from the endpoint publisher, or your own OAuth app registration in Microsoft Entra ID (custom OAuth).

## Choose an authentication method

The authentication method you choose depends on whether you need shared or individual user context, and what authentication protocols the A2A endpoint supports.

Use the following table to choose the right method for your scenario:

| Your goal | Recommended method |
| --- | --- |
| Use one shared identity for all users | Key-based authentication or Microsoft Entra authentication |
| Preserve each user's identity and permissions | OAuth identity passthrough |
| Avoid managing secrets when the underlying service supports Microsoft Entra | Microsoft Entra authentication |
| Connect to an A2A endpoint that doesn't require auth | Unauthenticated access |

## Supported authentication methods

The following table summarizes the authentication methods available for A2A connections:

| Method | Description | User context persists |
| --- | --- | --- |
| Key-based | Provide an API key or access token to authenticate with the A2A endpoint. Best for endpoints that use simple token-based authentication. | No |
| Microsoft Entra ID - agent identity | Use the agent's managed identity to authenticate. Requires role assignments on the underlying service. Best for Azure services that support managed identities. | No |
| Microsoft Entra ID - project managed identity | Use the project's managed identity to authenticate. Requires role assignments on the underlying service. Use this option when you want all agents in a project to share the same identity. | No |
| OAuth identity passthrough | Prompt users to sign in and authorize access to the A2A endpoint. Required when you need per-user permissions. | Yes |
| Unauthenticated access | No authentication required. Use this method only for A2A endpoints that are publicly accessible or don't require authentication. | No |

## Key-based authentication

> [!NOTE]
> Anyone with access to the project can access secrets stored in a project connection. Store only shared secrets in project connections. For user-specific access, use OAuth identity passthrough instead.

Use key-based authentication when the A2A endpoint accepts an API key, a personal access token (PAT), or another secret credential. For improved security, store shared credentials in a project connection instead of passing them at runtime.

When you connect your A2A endpoint to an agent in the Foundry portal, Foundry creates a project connection for you. Provide the credential name (the HTTP header name) and credential value (the header value). The format depends on what the endpoint expects.

**Common credential formats:**

| Endpoint type | Credential name | Credential value |
| --- | --- | --- |
| Bearer token | `Authorization` | `Bearer <your-token>` |
| API key in header | `x-api-key` | `<your-api-key>` |
| Custom header | `<custom-header-name>` | `<your-secret-value>` |

When the agent invokes the A2A endpoint, Agent Service retrieves the credentials from the project connection and includes them in the request headers.

### Security best practices for key-based authentication

- **Use least-privilege credentials**: Request only the minimum permissions needed for the agent's tasks.
- **Rotate tokens regularly**: Set a reminder to regenerate tokens before they expire.
- **Restrict project access**: Limit who can access projects that contain shared secrets.
- **Audit credential usage**: Monitor project connection access in your Azure activity logs.

## Microsoft Entra ID authentication

Use Microsoft Entra ID authentication when the A2A endpoint and its underlying service accept Microsoft Entra ID tokens. This method eliminates the need to manage secrets because Azure handles token acquisition and renewal automatically.

### Agent identity

Use your agent's managed identity to authenticate with A2A endpoints that support Microsoft Entra ID authentication. When you create an agent in Agent Service, the agent automatically receives a managed identity.

**Identity lifecycle:**

- **Before publishing**: All agents in the same project share a common identity. This simplifies development and testing.
- **After publishing**: Each published agent receives a unique identity. This provides isolation and enables granular access control.

For more information about agent identity lifecycle, see [Agent identity concepts in Microsoft Foundry](agent-identity.md).

**To configure agent identity authentication:**

1. Identify the underlying service that powers the A2A endpoint (for example, Azure Cosmos DB or Azure Storage).
1. Assign the required roles to the agent identity on that service. The specific roles depend on the service and the operations your agent needs to perform.
1. Configure the A2A connection to use agent identity authentication.

When the agent invokes the A2A endpoint, Agent Service uses the agent identity to request an authorization token from Microsoft Entra ID and includes it in the request.

### Foundry project managed identity

Use your Foundry project's managed identity to authenticate with A2A endpoints. This option is useful when you want all agents in a project to share the same identity for accessing resources.

**To configure project managed identity authentication:**

1. Identify the underlying service that powers the A2A endpoint.
1. Assign the required roles to the project's managed identity on that service.
1. Configure the A2A connection to use project managed identity authentication.

When the agent invokes the A2A endpoint, Agent Service uses the project's managed identity to request an authorization token from Microsoft Entra ID and includes it in the request.

## OAuth identity passthrough

> [!NOTE]
> To use OAuth identity passthrough, users interacting with your agent need at least the **Azure AI User** role on the project.

OAuth identity passthrough enables your agent to act on behalf of individual users. Use this method when actions should be scoped to each user's permissions, such as accessing their personal files, repositories, or other protected resources.

OAuth identity passthrough works with Microsoft and non-Microsoft A2A endpoints that support OAuth 2.0, including services that use Microsoft Entra ID.

### How OAuth identity passthrough works

1. **First interaction**: When a user first interacts with your agent, Agent Service generates a consent link.
1. **User consent**: The user opens the link, signs in to the underlying service, and authorizes the agent to access their data.
1. **Token storage**: Agent Service securely stores the user's OAuth tokens (access token and refresh token). These tokens are scoped to that specific user and agent combination.
1. **Subsequent requests**: When the agent invokes the A2A endpoint, Agent Service includes the user's access token in the request. If the access token expires, Agent Service uses the refresh token to obtain a new one.

### OAuth token types

OAuth uses two types of tokens:

| Token type | Purpose | Lifetime |
| --- | --- | --- |
| **Access token** | Authorizes API calls to the underlying service | Short-lived (typically 1 hour) to limit exposure if compromised |
| **Refresh token** | Obtains new access tokens without requiring the user to sign in again | Longer-lived (hours to weeks, or until revoked) |

OAuth scopes define what the agent can access and do on the user's behalf. The scopes are specified when you configure the connection and are presented to the user during the consent flow. For more information about OAuth, see the [Microsoft security documentation](https://www.microsoft.com/security/business/security-101/what-is-oauth). 

### Managed OAuth vs. custom OAuth

Agent Service supports two OAuth configuration options:

| Option | Description | When to use |
| --- | --- | --- |
| **Managed OAuth** | Microsoft or the A2A endpoint publisher manages the OAuth app registration. | Use when available. Simplifies setup and reduces configuration errors. |
| **Custom OAuth** | You provide your own OAuth app registration from Microsoft Entra ID or another identity provider. | Use when managed OAuth isn't available, or when you need custom scopes or branding. |

**To configure custom OAuth**, provide the following information:

- **Client ID**: The application ID from your OAuth app registration.
- **Client secret** (if required): The secret associated with your app registration.
- **Authorization URL**: The endpoint where users authorize access.
- **Token URL**: The endpoint where Agent Service exchanges the authorization code for tokens.
- **Refresh URL**: The endpoint for refreshing expired access tokens.
- **Scopes**: The permissions your agent needs (for example, `repo` for GitHub or `Files.Read` for Microsoft Graph).

> [!IMPORTANT]
> If you use custom OAuth, you receive a redirect URL from Agent Service. Add this URL to your OAuth app registration's allowed redirect URIs so Agent Service can complete the authorization flow.

## Unauthenticated access

Use unauthenticated access only when the A2A endpoint is publicly accessible and doesn't require authentication. This option is rare in production scenarios but might be appropriate for:

- Public APIs that don't require authentication
- Internal development or testing endpoints
- Endpoints protected by network-level security (such as private endpoints) instead of authentication

## Set up authentication for an A2A connection

Follow these steps to configure authentication for an A2A connection:

1. **Identify the A2A endpoint and supported authentication methods**. Contact the endpoint publisher or check the endpoint documentation to determine which authentication methods are supported.

1. **Gather the required credentials** based on your chosen authentication method:
   - **Key-based**: Obtain the API key or token from the endpoint publisher.
   - **Microsoft Entra ID**: Identify the required role assignments for the underlying service.
   - **OAuth**: Determine whether managed OAuth is available, or gather your custom OAuth app registration details.

1. **Create a project connection** in the Foundry portal. The connection stores the A2A endpoint URL, authentication method, and credentials.
   - For general connection guidance, see [Add a new connection to your project](../../../how-to/connections-add.md).
   - For A2A-specific configuration, see [Add an A2A agent endpoint to Foundry Agent Service](../how-to/tools/agent-to-agent.md).

1. **Configure role assignments** (Microsoft Entra ID authentication only). Assign the required roles to the agent identity or project managed identity on the underlying service.

1. **Add the A2A tool to your agent**. Reference the project connection you created and configure which tools from the A2A endpoint your agent can invoke.

## Validate authentication

After you configure authentication, test the connection to confirm it works correctly.

### Validate key-based or Microsoft Entra ID authentication

1. Open your agent in the Foundry portal.
1. Start a conversation and trigger an action that invokes the A2A tool.
1. Confirm the tool call completes successfully. If the call fails, check the error message and see [Troubleshooting](#troubleshooting).

### Validate OAuth identity passthrough

1. Open your agent in the Foundry portal using a test user account that hasn't previously consented.
1. Start a conversation and trigger an action that invokes the A2A tool.
1. Confirm that a consent link appears in the agent's response.
1. Open the consent link and sign in with the test user's credentials.
1. Authorize the requested permissions.
1. Return to the agent and trigger the A2A tool again.
1. Confirm the tool call completes successfully using the test user's credentials.
1. (Optional) Test with another user account to confirm consent flows work for multiple users.

## Troubleshooting

Use the following table to diagnose and resolve common authentication issues:

| Issue | Possible cause | Resolution |
| --- | --- | --- |
| Key-based authentication fails with 401 Unauthorized | Invalid or expired token | Regenerate the token from the endpoint publisher and update the project connection. |
| Key-based authentication fails with 400 Bad Request | Incorrect header name or value format | Check the endpoint documentation for the expected header format. Common formats include `Authorization: Bearer <token>` and `x-api-key: <key>`. |
| Microsoft Entra ID authentication fails with 403 Forbidden | The identity doesn't have the required role assignments | Assign the required roles to the agent identity or project managed identity on the underlying service. Role assignment changes can take up to 10 minutes to propagate. |
| Microsoft Entra ID authentication fails with 401 Unauthorized | The underlying service doesn't accept Microsoft Entra ID tokens, or the audience is incorrect | Confirm the underlying service supports Microsoft Entra ID authentication. Check that the A2A endpoint is configured to accept tokens for the correct audience. |
| Consent completes but tool calls fail | The user doesn't have permissions in the underlying service | Confirm the user has the required permissions in the underlying service. Also confirm the user has at least the **Azure AI User** role on the Foundry project. |
| No consent link appears for OAuth | OAuth identity passthrough isn't configured, or the agent didn't invoke the A2A tool | Verify the project connection is configured for OAuth identity passthrough. Trigger an action that invokes the A2A tool. |
| Consent link appears but sign-in fails | Custom OAuth configuration is incorrect | For custom OAuth, verify the authorization URL, client ID, and redirect URL are correct. Confirm the redirect URL is added to your OAuth app registration. |
| Refresh token expired | User hasn't interacted with the agent for an extended period | The user needs to go through the consent flow again. This is expected behavior for security. |

## Related content

- [Add an A2A agent endpoint to Foundry Agent Service](../how-to/tools/agent-to-agent.md): Step-by-step guide to configure an A2A tool for your agent.
- [Agent identity concepts in Microsoft Foundry](agent-identity.md): Learn how agent identities work and their lifecycle.
- [Role-based access control for Microsoft Foundry](../../../concepts/rbac-foundry.md): Understand the roles and permissions available in Foundry.
- [Add a new connection to your project](../../../how-to/connections-add.md): General guidance for creating project connections.
