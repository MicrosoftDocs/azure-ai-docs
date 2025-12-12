---
title: MCP server authentication
titleSuffix: Microsoft Foundry
description: Learn about ways of adding authentication to the MCP server tool in the Foundry Agent Service.
services: cognitive-services
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: how-to
ms.date: 11/14/2025
author: aahill
ms.author: aahi
---

# Authentication support for the Model Context Protocol (MCP) tool (preview)

Most MCP servers will require you to authenticate in order to access the MCP server and its underlying service. Authentication ensures that only authorized users can interact with each MCP server.  

> [!NOTE]
> If you do not already have an account with the MCP server publisher, you will need to create a new account by visiting the website of the MCP server publisher.  

In general, there are two authentication scenarios: 

- **Shared authentication**: If you want every user of your agent to use the same identity to authenticate with the MCP server, you can use key-based, Microsoft Entra Agent Identity, or Microsoft Entra Foundry Project Managed Identity for authentication. The individual user identity or context does not persist with any of these methods. For example, if you're developing a chat agent for your organization’s users to retrieve information from Azure Cosmos DB, you may want every user of your agent to access the same folder or container in Azure Cosmos DB containing data accessible to all users in your organization, without requiring each user to authenticate with a unique identity.  
- **Individual authentication**: If you want every user of your agent to use their own account to authenticate with the MCP server so that their personal user context persists, you can use OAuth identity passthrough. For example, if you're developing a coding agent for your developers and you want them to retrieve commits and pull requests from their GitHub repo, you might want each developer (user of your agent) to sign in and provide their account info so that the GitHub MCP server can retrieve commits and pull requests from the developer’s individual account.  

### Supported Authentication 

|Type  | Description |  Is the user context persisted? |
|:---:| :----------: |:------------------------:|
| Key-based| Provide API key or access token to authenticate with the MCP server | No |
| Microsoft Entra – Agent Identity| Use your agent’s Agentic Identity to authenticate with the MCP server. This Agent Identity needs to have proper RBAC assignment to the underlying service | No |
|Microsoft Entra – Foundry Project Managed Identity |Use your Foundry Project’s Managed Identity to authenticate with the MCP server. Your Foundry Project needs to have proper RBAC assignment to the underlying service | No |
|OAuth Identity Passthrough | Apply OAuth to allow users interacting with your agent to sign in and authorize to the MCP server.| Yes |
|Unauthenticated|No authentication is needed | No |

### Key-based authentication 

You can pass your API key, PAT token, and other credentials to MCP servers supporting key-based authentication. With Foundry Agent Service, we recommend you put your credentials in Foundry connection instead of manually passing each time during runtime for improved security. When you connect your MCP server to an agent in Foundry portal, a Foundry connection will be automatically created for you. You need to provide the credential name and credential value. For example, if you're trying to connect with GitHub MCP server, you can select to use key-based authentication to pass your personal access token. The credential name is `Authorization` and the credential value is `Bearer <your personal access token>`. 

When the agent invokes the MCP server, it will retrieve the credentials from your Foundry connection and pass them to the MCP server for authentication. 

### Microsoft Entra 

#### Agentic identity 

You can use your agent’s Agent Identity to authenticate with MCP servers that support authenticating with Agent Identity. If your agent is created with Foundry Agent Service, your agent will automatically be assigned an Agent Identity. All agents in your Foundry Project will share the same Agent Identity before publishing. After you publish an agent, your agent will be assigned a unique Agent Identity. When you choose to authenticate with Agent Identity, Foundry Agent Service will use the shared Agent Identity if the agent hasn’t been published and therefore doesn’t have a unique Agent Identity; it will use the unique Agent Identity if the agent has been published and has a unique Agent Identity.  

You need to make sure your Agent Identity has the proper RBAC role to the underlying service powering the MCP server.<!--(please refer to the MCP server documentation for specific RBAC roles needed)--> When you're connecting an MCP server to your agent, you need to specify the scope URI of the service, for example, when you're connecting to the Microsoft Foundry MCP server, the scope URI is `http://ai.azure.com`.  

When the agent invokes the MCP server, it will use the available Agent Identity to get its authorization token from the scope URI and pass it to the MCP server for authentication.  

#### Foundry project managed identity 

You can use your Foundry project's Managed Identity to authenticate with MCP servers that support authenticating with Managed Identity. You need to make sure your Foundry project's Managed Identity has the proper RBAC role to the underlying service powering the MCP server.<!--(please refer to the MCP server documentation for specific RBAC roles needed)--> When you're connecting the MCP server to your agent, you need to specify the scope URI of the service, for example, when you're connecting to Foundry MCP server, the scope URI is `http://ai.azure.com`.  

When the agent invokes the MCP server, it will use the Foundry Project's Managed Identity to get its authorization token from the scope URI and pass it to the MCP server for authentication. 

### OAuth identity passthrough 

> [!NOTE]
> To use OAuth identity passthrough, your users interacting with your agent need to have at least `Azure AI User` Role. 

OAuth identity passthrough is available for authentication to Microsoft and non-Microsoft MCP servers and underlying services compliant with OAuth, including Microsoft Entra.

You can use [OAuth identity](/entra/architecture/auth-oauth2) passthrough to prompt users interacting with your agent to sign into the MCP server and its underlying service and grant the agent the ability to use the user's credentials when interacting with the MCP server. Foundry Agent Service securely stores the user's credentials and uses them only within the context of the agent communicating with the MCP server. Importantly, OAuth does not grant a non-Microsoft app or service unlimited access to the user's data. Part of the protocol is specifying what data the app or service is allowed to access and what it can do with that data. 

When you use OAuth identity passthrough, the agent will need to use credentials from the user interacting with the agent to connect to the MCP server. The first time a particular user interacts with the agent, Foundry Agent Service will generate a consent link, which the user can accept to log into the identity provider associated with the MCP server. After the user logs in and consents to allow Foundry Agent Service to use their credentials to communicate with the MCP Server, the agent is able to discover and invoke tools on the MCP server with the user's credentials. 

The user's OAuth credentials are stored securely and scoped to the particular user and the particular agent they interacted with. These credentials are generally a refresh token and an access token.

There are usually two tokens involved in OAuth flow: refresh token and access token. 

**Access token**:
- Used to call APIs (for example Microsoft Graph, GitHub).
- Short-lived by design - usually minutes to an hour (commonly 1 hour).
- Purpose: limit the damage if stolen.
- When it expires, the OAuth App can use a refresh token (if available) to get a new one. 

**Refresh token**:
- Used only to get new access tokens.
- Longer-lived - can last hours, days, weeks, or even "until revoked" depending on server settings.
- Can often be revoked by the user (for example via account settings).
- Some providers rotate refresh tokens each time they’re used (for extra security). 

Foundry Agent Service supports two OAuth options: **managed OAuth** and **custom OAuth**. With managed OAuth, the OAuth App is managed by Microsoft or the MCP server publisher. With custom OAuth, you bring your own OAuth App. The OAuth App is a client application that registers with an OAuth provider (such as Microsoft or GitHub) and uses the flow above to get the necessary OAuth token. The benefit of custom OAuth is that you can customize the consent link content for your organization and application. For example, with custom OAuth, Contoso can ask users of its agent to give permission to Contoso to pass the user’s credentials to the MCP server. If you want to use custom OAuth, you will need to provide all required information, including a client ID, client secret, authorization URL, token URL, refresh URL, and suggested scopes.  

> [!NOTE]
> If you decide to use custom OAuth and provide all information above, you will then get a redirect URL. Make sure to add this redirect URL to your OAuth app, as it will delegate the handling of the access token to enable use of your connection.

When you set up **custom OAuth**, the following information is needed:

- client ID: required, you can find this in your OAuth app
- client secret: optional depending on if this is required by your OAuth app
- auth URL: required, the auth URL is used for users to log in. You can find this from your OAuth app or your MCP server provider documentation. Some providers provide the same auth URL for all MCP servers and others provide a custom auth URL for different MCP servers. Review the documentation to make sure you use the proper one. 
- refresh URL: required, the refresh URL is used to get a refresh token. You can find this from your OAuth app or your MCP server provider documentation. If you don't find a specific refresh URL, you can provide the token URL. Some providers provide the same refresh URL for all MCP servers and others provide custom refresh URL for different MCP servers. Review the documentation to make sure you use the proper one. 
- token URL: required, the token URL is used to get a token. You can find this from your OAuth app or your MCP server provider documentation. Some providers provide the same token URL for all MCP servers and others provide custom token URL for different MCP servers; please review the documentation to make sure you use the proper one. 
- scopes: optional, scopes specify which permission/scope you want the user to have access to, make sure the scopes use the correct naming from the OAuth app. 

#### Bring your own Microsoft Entra app registration

> [!NOTE]
> Agent 365 MCP servers are only available to [Frontier tenants](https://adoption.microsoft.com/en-us/copilot/frontier-program/).

To use with Microsoft services and identity passthrough, you can bring your own [Microsoft Entra app registration](/entra/identity-platform/quickstart-register-app). By bringing your own Microsoft Entra app registration, you can control what permissions you give to your Entra app. Let's use the Agents 365 MCP server as an example:
1. Follow the [app registration guide](/entra/identity-platform/quickstart-register-app) to create a Microsoft Entra app and get the client ID and client secret. 

1. Grant [scoped permissions](/entra/identity-platform/quickstart-configure-app-access-web-apis) to your Microsoft Entra app. For Agents 365 MCP servers, you can go to **Manage** > **API Permissions** and search for **Agent 365 Tools**. If you can't find it, search for `ea9ffc3e-8a23-4a7d-836d-234d7c7565c1`. Then assign permissions you need and select them to grant admin consent for your tenant. Here is a list of what permissions you need for each MCP server:
- Microsoft Outlook Mail MCP Server (Frontier): `McpServers.Mail.All`
- Microsoft Outlook Calendar MCP Server (Frontier): `McpServers.Calendar.All`
- Microsoft Teams MCP Server (Frontier): `McpServers.Teams.All`
- Microsoft 365 User Profile MCP Server (Frontier): `McpServers.Me.All`
- Microsoft SharePoint and OneDrive MCP Server (Frontier): `McpServers.OneDriveSharepoint.All`
- Microsoft SharePoint Lists MCP Server (Frontier): `McpServers.SharepointLists.All`
- Microsoft Word MCP Server (Frontier): `McpServers.Word.All`
- Microsoft 365 Copilot (Search) MCP Server (Frontier): `McpServers.CopilotMCP.All`
- Microsoft 365 Admin Center MCP Server (Frontier): `McpServers.M365Admin.All`
- Microsoft Dataverse MCP Server (Frontier): `McpServers.Dataverse.All`

1. Go back to [Foundry portal](https://ai.azure.com/build/tools) and configure your MCP server. Click to connect a tool, go to **custom** and then select **MCP**. Provide a name, MCP server endpoint and select **OAuth Identity Passthrough** for authentication:
- The client ID and client secret that you got in the previous step.
- token url: `https://login.microsoftonline.com/{tenantId}/oauth2/v2.0/token`
- auth url: `https://login.microsoftonline.com/{tenantId}/oauth2/v2.0/authorize`
- refresh url: `https://login.microsoftonline.com/{tenantId}/oauth2/v2.0/token`
- scopes: `ea9ffc3e-8a23-4a7d-836d-234d7c7565c1/{permission above}`

1. Once you finish this process, you will get a [redirect URL](/entra/identity-platform/how-to-add-redirect-uri) that you'll need to add back to your Microsoft Entra app. 

### Unauthenticated 

This is supported if the MCP server doesn’t require authentication.  

## Prerequisites

* A configured agent

## Setup

1. Find the remote MCP server that you want to connect to, such as the GitHub MCP server. Create or update a Foundry agent with an `mcp` tool with the following information:

   1. `server_url`: The URL of the MCP server. For example, `https://api.githubcopilot.com/mcp/`.
   2. `server_label`: A unique identifier of this MCP server to the agent; for example, `github`.
   3. `require_approval`: Optionally determine whether approval is required. Supported values are:
      * `always`: A developer needs to provide approval for every call. If you don't provide a value, this one is the default.
      * `never`: No approval is required.
      * `{"never":[<tool_name_1>, <tool_name_2>]}`: You provide a list of tools that don't require approval.
      * `{"always":[<tool_name_1>, <tool_name_2>]}`: You provide a list of tools that require approval.
   1. `project_connection_id`: the connection name that stores the MCP server endpoint, auth you select and relevant information. If you provide different endpoints in connection vs `server_url`, the endpoint in connection will be used.
   
1. If the model tries to invoke a tool in your MCP server with approval required or require sign in for OAuth identity passthrough, you will get an output with the consent link (type: oauth_consent_request) or the tool_calling to get approval (type: mcp_approval_request). After the user is logged in or it's approved, submit another response to continue.

## Host a local MCP server

The Foundry Agent Service runtime only accepts a remote MCP server endpoint. If you want to add tools from a local MCP server, you'll have to self-host it on [Azure Container Apps](/samples/azure-samples/mcp-container-ts/mcp-container-ts/) or [Azure Functions](https://github.com/Azure-Samples/mcp-sdk-functions-hosting-python/tree/main) to get a remote MCP server endpoint. Pay attention to the following considerations when attempting to host local MCP servers in the cloud:

|Local MCP server setup | Hosting in Azure Container Apps | Hosting in Azure Functions |
|:---------:|:---------:|:---------:|
| **Transport** | HTTP POST/GET endpoints required. | HTTP streamable required. | 
| **Code changes** | The container must rebuild. | Azure Functions-specific configuration files required in the root directory. |
| **Authentication** | Custom authentication implementation required. | Key-based only. OAuth needs API Management. |
| **Language** | Any language that runs in Linux containers (Python, Node.js, .NET, TypeScript, Go). | Python, Node.js, Java, .NET only. |
| **Container Requirements** | Linux (linux/amd64) only. No privileged containers.| Containerized servers are not supported. |
| **Dependencies** | All dependencies must be in container image. | OS-level dependencies (such as Playwright) are not supported. |
| **State** | Stateless only. | Stateless only. |
| **UVX/NPX** | Supported. | Not supported. `npx` start commands not supported. |
