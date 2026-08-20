---
title: "Publish agents to Microsoft 365 and Teams by using the REST API"
description: "Publish a Microsoft Foundry agent that runs in a virtual network to Microsoft 365 Copilot and Microsoft Teams when public network access is disabled."
author: fosteramanda
ms.author: fosteramanda
ms.reviewer: aahill
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.topic: how-to
ms.date: 07/07/2026
ms.custom: pilot-ai-workflow-jan-2026
ai-usage: ai-assisted
#CustomerIntent: As a developer who runs a Foundry agent inside a virtual network, I want to publish it to Microsoft 365 Copilot and Teams so that users can reach it even though public network access is disabled.
---

# Publish agents to Microsoft 365 Copilot and Microsoft Teams by using the REST API + VNet Guidance 

This article shows how to publish a Foundry agent to Microsoft 365 Copilot and Teams by using the REST API. You can follow it for any project, whether or not public network access is disabled:

- **Steps 1 through 4** are the REST equivalent of the one-click **Publish to Teams and Microsoft 365 Copilot** button in the Foundry portal, and they work for any project.
- **Step 5** (firewall and networking) is required only when your project disables public network access (PNA) and runs behind a private endpoint. In that case, the portal button isn't available because the Microsoft channel adapters that deliver Teams and Copilot messages run outside your network and can't reach your agent's private IP address.

When you finish, users in your tenant can use your agent in Microsoft 365 Copilot and Teams, including when the agent stays on a private network.

> [!WARNING]
> When you publish agents to Microsoft 365 and Teams, certain data associated with publishing and using the agent in Microsoft 365 and Teams is processed and stored by those services and is subject to the terms, compliance commitments, data residency commitments, and data handling practices applicable to Microsoft 365 and Teams.
>
> This data can include data necessary to publish the agent, such as the agent's name, icon, and description, as well as data contained in responses provided by the agent when users in your organization submit queries to the agent from Microsoft 365 and Teams.
>
> Before you publish an agent to Microsoft 365 and Teams, evaluate whether the resulting data flows and processing are consistent with your organization's compliance, data residency, and governance requirements.

## Prerequisites

- Access to the [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs).
- A [Foundry project](../../how-to/create-projects.md) configured with [private networking](./virtual-networks.md): the project's Foundry resource uses a private endpoint, and public network access is disabled.
- An agent in that project that you tested and want to publish. Test the agent thoroughly and select the active version that consumers interact with. For more information, see [Configure your agent endpoint and settings](./configure-agent.md).
- The following role assignments:
    - **Foundry User** role on the Foundry project to create, manage, and publish agents.
    - Permission to create an Azure Bot Service resource and configure its channels in the target resource group (for example, the **Azure Bot Service Contributor Role**, or the broader **Contributor** or **Owner** role).
    - Permission to manage the firewall, DNS, and reverse proxy that route inbound traffic to your network.
- [Azure CLI](/cli/azure/install-azure-cli) installed and signed in with `az login` to the subscription that contains your Foundry resource.
- The `Microsoft.BotService` resource provider registered in your subscription:

   ```azurecli
   az provider register --namespace Microsoft.BotService
   ```

[!INCLUDE [publish-what-happens](../includes/publish-copilot-what-happens.md)]

## Steps

1. Get your agent's identity and tenant ID.
1. Create an Azure Bot Service resource.
1. Optionally, enable the activity protocol and add BotServiceRbac or BotServiceTenant as an authorization scheme on the agent. The publish API in the next step also does this automatically.
1. Call Foundry's Microsoft 365 publish API.
1. Configure your network for inbound and outbound traffic.

For a Python example of steps 1 through 4, see the [publish-agent notebook](https://github.com/mattfeltonma/azure-terraform-lab-base-azfw/blob/main/workloads/microsoft-foundry/sample-code/publish-agent-teams/publish-agent.ipynb).

## Step 1: Get the agent identity and tenant ID

Before creating the Azure Bot Service resource, collect two values you'll need in Step 2:

- **Agent identity principal ID** — the agent identity of your Foundry agent
- **Tenant ID** — your Microsoft Entra ID tenant

### 1.1 Get a bearer token

The steps authenticate with a bearer token for the `https://ai.azure.com` audience. Get a token once and reuse it:

```azurecli
az login
az account get-access-token --resource https://ai.azure.com --query accessToken -o tsv
```

Use the returned value as `{{token}}` in the requests that follow.

### 1.2 Get the agent identity principal ID

Get the principal ID by calling the **Agents - Get agent** API. Your `{{endpoint}}` is the project endpoint, in the form `https://<resource-name>.services.ai.azure.com/api/projects/<project-name>`.

```http
GET {{endpoint}}/agents/{{agent_name}}?api-version=v1
Authorization: Bearer {{token}}
Content-Type: application/json
```

In the JSON response, copy `instance_identity.principal_id`. You use it in the next step when you create the Azure Bot Service resource.

```json
"instance_identity": {
  "principal_id": "aaaaaaaa-bbbb-cccc-1111-222222222222",
  "client_id":    "00001111-aaaa-2222-bbbb-3333cccc4444"
}
```

### 1.3 Get your tenant ID

To get your tenant ID, run the command:

```azurecli
az account show --query tenantId -o tsv
```

Save both values for the next step.

## Step 2: Create the Azure Bot Service resource

The Azure Bot Service resource proxies messages between the Microsoft channel adapters (Teams and Copilot) and your agent. Create the bot with public network access disabled and connect it to the Microsoft Teams channel. The bot's `endpoint` is the agent's activity protocol endpoint, in this form:

```
https://<resource-name>.services.ai.azure.com/api/projects/<project-name>/agents/<agent-name>/endpoint/protocols/activityProtocol?api-version=2025-05-15-preview
```

1. Save the following template as `bot-service.bicep`:

   ```bicep
   param botName string
   param displayName string
   param msaAppId string          // Agent principal ID from the previous section
   param tenantId string          // Your Microsoft Entra tenant ID
   param endpoint string          // Agent activity protocol endpoint
   param botServiceSku string = 'F0'

   resource botService 'Microsoft.BotService/botServices@2022-09-15' = {
     name: botName
     kind: 'azurebot'
     location: 'global'
     sku: {
       name: botServiceSku
     }
     properties: {
       displayName: displayName
       endpoint: endpoint
       msaAppId: msaAppId
       msaAppTenantId: tenantId
       msaAppType: 'SingleTenant'
       publicNetworkAccess: 'Disabled'
     }
   }

   resource botServiceMsTeamsChannel 'Microsoft.BotService/botServices/channels@2021-03-01' = {
     parent: botService
     location: 'global'
     name: 'MsTeamsChannel'
     properties: {
       channelName: 'MsTeamsChannel'
     }
   }
   ```

1. Deploy the template to the resource group that contains your Foundry resource:

   ```azurecli
   az login
   az deployment group create \
     --resource-group <your-resource-group> \
     --template-file bot-service.bicep \
     --parameters \
         botName=<bot-name> \
         displayName="<Display Name>" \
         msaAppId=<agent-principal-id> \
         tenantId=<tenant-id> \
         endpoint=<agent-activity-protocol-endpoint>
   ```

1. Capture the Azure Bot Service resource ID. You pass it as `botServiceArmId` when you publish in Step 4:

   ```azurecli
   az bot show --name <bot-name> --resource-group <your-resource-group> --query id -o tsv
   ```

## Step 3: Enable the activity protocol and Bot Service authorization

> [!NOTE]
> This step is optional. The Microsoft 365 publish API in Step 4 automatically adds the `activity` protocol and sets the bot-service authorization scheme that matches your `publishScope`. Complete this step to configure them explicitly, for example to test message delivery before you publish. Choose the scheme that matches the `publishScope` you use in Step 4, because publishing updates the scheme to match.

Interacting with an agent from Microsoft 365 and Teams requires two additions to the agent endpoint: the **`activity`** protocol, which lets the channel adapters deliver messages, and a **Bot Service authorization scheme**, which controls who can call the agent.

Choose one authorization scheme:

| Authorization scheme | Who can call the agent from Microsoft 365 and Teams |
|---|---|
| `BotServiceRbac` | Only identities that have the Azure permissions required to call the agent in Foundry, through the portal, SDK, or REST API. |
| `BotServiceTenant` | Everyone in your tenant. |

The `publishScope` value in the publish request (step 4) determines both the agent's store visibility and its authorization scheme. `Tenant` maps to `BotServiceTenant`, and `Shared` or `Personal` maps to `BotServiceRbac`. Publishing sets the matching scheme for you, so the scheme you choose here must match the `publishScope` you use in step 4.

In the Foundry portal, the **Who can use this agent** option applies these pairings: **Just you** applies `BotServiceRbac` with `Shared` visibility, and **People in your organization** applies `BotServiceTenant` with `Tenant` visibility. For more information, see [Publish agents to Microsoft 365 Copilot and Microsoft Teams](./publish-copilot.md).

> [!IMPORTANT]
> Keep `responses` and `Entra` in the lists as well — removing them will break chatting with the agent from the Foundry portal or SDK.

Call the **Agents - Update agent** API to add `activity` and `BotServiceRbac` to the agent's existing schemes:

```http
PATCH {{endpoint}}/agents/{{agent_name}}?api-version=v1
Authorization: Bearer {{token}}
Content-Type: application/merge-patch+json
Foundry-Features: AgentEndpoints=V1Preview

{
    "agent_endpoint": {
        "protocol_configuration": {
            "responses": {},
            "activity": {}
        },
        "authorization_schemes": [
            {
                "type": "Entra"
            },
            {
                "type": "BotServiceRbac"
            }
        ]
    }
}
```

## Step 4: Publish the agent to Microsoft 365

Publish the agent by calling the **Microsoft 365 publish** API with the `{{token}}` from the first step. Replace the placeholders using these values:

| Placeholder | Description | Where to get it |
|---|---|---|
| `{{endpoint}}` | Your project endpoint, `https://<resource-name>.services.ai.azure.com/api/projects/<project-name>` | From Step 1.2 |
| `<agent-name>` | Your agent's name | Foundry portal |
| `<bot-service-arm-id>` | ARM resource ID of the Azure Bot Service resource you created in Step 2 | `az bot show` output from Step 2 |

The agent name is part of the request URL. The service resolves the agent and its identity from that name, so you no longer pass the agent GUID or bot ID in the request body.

```http
POST {{endpoint}}/agents/<agent-name>/microsoft365/publish?api-version=v1
Authorization: Bearer {{token}}
Content-Type: application/json

{
  "agentDisplayName": "Contoso Helpdesk",
  "botServiceArmId": "<bot-service-arm-id>",
  "publishScope": "Shared",
  "publishAsAutopilot": false,
  "appVersion": "1.0.0",
  "shortDescription": "Foundry M365 Agent",
  "fullDescription": "A Foundry agent published to Microsoft 365.",
  "developerName": "Azure Developer",
  "developerWebsiteUrl": "https://azure.microsoft.com",
  "privacyUrl": "https://privacy.microsoft.com",
  "termsOfUseUrl": "https://www.microsoft.com/legal/terms-of-use"
}
```

Customize the body before you publish:

- `agentDisplayName`: the display name shown in Teams and Microsoft 365 Copilot. Optional; when omitted, the agent name is used.
- `botServiceArmId`: the ARM resource ID of the Azure Bot Service resource you created in Step 2. Required.
- `publishScope`: `Shared` (the portal's **Just you**) makes the agent available only to you. It appears under **Your agents** in the agent store, and you share it with a link. `Tenant` (the portal's **People in your organization**) submits the agent for Microsoft 365 admin approval and, once approved, makes it available to your whole organization under **Built by your org**. `Personal` is also accepted and treated as `Shared`.
- `appVersion`: a semantic version string such as `1.0.0`. Increment it to update the user-facing properties; republishing an existing version returns a `version already exists` error. To roll out a new agent version, update the agent version receiving traffic instead.
- `shortDescription` and `fullDescription`: descriptions shown in the agent store.
- `developerName`, `developerWebsiteUrl`, `privacyUrl`, and `termsOfUseUrl`: developer metadata shown to users.
- `publishAsAutopilot`: set to `false`. To publish as an autopilot agent, see [Foundry agents in Microsoft Agent 365](./agent-365.md).
- `canRespondWithoutMention`, `colorIconBase64`, and `outlineIconBase64`: optional. Control whether an autopilot responds to all messages on its Teams surfaces or only when @mentioned, and set custom color (192×192 PNG) and outline (32×32 PNG) app icons.

> [!WARNING]
> Don't include secrets, API keys, or other sensitive information in any metadata field. These fields are visible to users.

A successful response returns the published title ID (`titleId`). The agent isn't reachable from Teams or Copilot until you configure networking in step 5.

## Step 5: Configure networking and secure inbound traffic

After publishing your agent to Microsoft 365, you need to ensure that Microsoft's Bot Channel Adapters can reach your agent's messaging endpoint. Because your agent is deployed behind a private endpoint, it isn't directly reachable from the public internet. This section covers the inbound network path you need to establish, and the security controls available to you at each layer.

### Understanding the inbound traffic flow

When a user sends a message in Teams or Microsoft 365 Copilot, Microsoft's Bot Channel Adapter POSTs the message to your agent's messaging endpoint. Because your agent's endpoint resolves to a private IP address inside your network, two things need to be true before traffic can reach it:

- **A publicly reachable entry point** — something in your architecture must be accessible from the public internet on an endpoint you control, and able to route traffic inward.
- **TLS termination and proxying** — something in your architecture must terminate TLS and forward the request on to your agent's private endpoint.

These might be the same component, or different components. The order might vary — a firewall might provide the public entry point and pass traffic to a TLS-terminating proxy behind it, or a single appliance such as Azure Application Gateway might handle both. What matters is that both requirements are met end-to-end.

### 5.1 Inbound network requirements

- **A publicly reachable entry point**: You need at least one component in your architecture with a public-facing IP that you control, capable of routing inbound traffic toward your private network. This might be a firewall, load balancer, CDN, or other network appliance, depending on your organization's existing architecture.
- **TLS termination**: Something in your architecture must terminate TLS and present a valid certificate for the hostname the Bot Channel Adapter is connecting to. This might be a component you manage directly, or one provided by your platform. For example, Azure Application Gateway can present a certificate against a public IP without requiring you to supply your own. If your public entry point doesn't terminate TLS, you need a component behind it that does.
- **Source IP ranges**: Microsoft publishes the IP ranges used by the Bot Channel Adapters as part of the [Microsoft 365 URLs and IP address ranges](/microsoft-365/enterprise/urls-and-ip-address-ranges). Restricting inbound traffic to these ranges reduces your attack surface at the network perimeter before any application-layer controls are applied.

### 5.2 Authenticating inbound requests

Establishing a network path is necessary but not sufficient. Every request from the Bot Channel Adapter includes a signed JWT in the `Authorization` header. Foundry validates this token on your behalf and also authorizes the end user. In most cases, no additional configuration is required.

However, if your network security requirements mean that traffic must be authenticated before it crosses a security boundary — for example before it reaches Foundry — you can perform JWT validation at your TLS-terminating component independently. The full authentication specification is documented in [Bot Framework REST API authentication](/azure/bot-service/rest-api/bot-framework-rest-connector-authentication).

### 5.3 Validate the caller's tenant as a lighter-weight alternative

Validating the JWT is the strongest control, but it requires a component that can verify a signed token. If you don't have infrastructure that can validate a JWT, you can still reduce risk with two simpler checks at your inbound component:

- **Restrict the source IP ranges** to the Teams Required ranges (see **Source IP ranges** in 5.1), so that only the Bot Channel Adapter can reach your entry point.
- **Validate the caller's tenant ID.** The Bot Channel Adapter includes the caller's tenant ID in the `x-ms-tenant-id` header. Reject any request whose tenant ID isn't your own.

A published agent's Teams app can be installed in any tenant, so requests from outside your organization can reach your endpoint before Foundry applies RBAC. Checking the tenant ID lets you drop calls from tenants you don't intend to serve. This combination is weaker than JWT validation, because any caller that reaches your endpoint can set a header. Pair it with the source IP restriction so that only the Bot Channel Adapter can present the header. Together, the two checks give customers without JWT-capable infrastructure a meaningful layer of defense.

## Verify the published agent

1. In Microsoft 365 Copilot or Microsoft Teams, open the agent store and find your agent. With `Shared` scope, it appears under **Your agents**. With `Tenant` scope, it appears under **Built by your org** after a Microsoft 365 admin approves it in the [Microsoft 365 admin center](https://admin.cloud.microsoft/?#/agents/all/requested).
1. Start a conversation and send a message.
1. Confirm the agent replies. A reply confirms that both the inbound path (channel adapter to agent) and the outbound path (agent reply to the channel) work.

## Limitations

| Limitation | Description |
| --- | --- |
| File uploads and image generation in Microsoft 365 | These features don't work for agents published to Microsoft 365. They work in Microsoft Teams. |
| Private Link | Not supported for Teams or Azure Bot Service integrations. |
| Streaming and citations | Published agents don't support streaming responses or citations. |

## Troubleshooting

After you publish, problems generally fall into three types: an error while publishing, not finding the agent in the agent store, or an error when you chat with the agent.

### Publishing issues

These errors occur when you publish through the Microsoft 365 publish API.

| Symptom | Cause | Resolution |
|-------|-------|------------|
| The publish API rejects the request with a validation error | Invalid metadata or version. Example messages include `AppVersion can only contain digits and periods`, `AppVersion cannot start with 0`, `Developer name cannot exceed length of 32`, `Description cannot exceed length of 4000`, and `Developer Website URL must begin with 'https://'`. | Fix the flagged field and retry. The version must contain only digits and periods and can't start with `0`, the developer name must be 32 characters or fewer, and the full description must be 4,000 characters or fewer. |
| The publish API rejects the request because the app version already exists | You republished an existing `appVersion`. The service returns `Microsoft 365 app with {version} version already exists, please increment the version number while publishing.` | Increment `appVersion`. To roll out new agent behavior, update the agent version that receives traffic instead. |
| The publish API rejects the request for a missing field | The request is missing a required field, for example `BotServiceArmId is required.` or `App scope is required. Must be one of 'Personal', 'Shared', or 'Tenant'`. | Pass a valid `botServiceArmId`, and set `publishScope` to `Personal`, `Shared`, or `Tenant`. |
| The publish API rejects the request for an invalid icon | The color or outline icon isn't valid, for example `ColorIconBase64 is not valid base64.`, `ColorIconBase64 must be a PNG image.`, or `ColorIconBase64 must be a 192x192 PNG image.` | Provide a 192×192 color PNG and a 32×32 outline PNG, base64-encoded and within the size limit. |
| The publish API returns a `403 AuthorizationFailed` error for `Microsoft.BotService/botServices/write` | Your identity doesn't have permission to create or update the Azure Bot Service resource in the target resource group | Assign the **Azure Bot Service Contributor Role** (or the broader **Contributor** or **Owner** role) on the resource group that contains the bot service. |
| The publish API returns an identity error | The agent doesn't have a unique identity (`agent.identity` is null) | See the [migration guide](./migrate-agent-applications.md) for steps to resolve this. |
| The publish API returns a permission error | The acting user doesn't have the required permission on the workspace: `The acting user does not have the required permission on the workspace.` | Assign a role that grants agent write access on the Foundry project. |

The following issues are specific to publishing behind a virtual network:

| Symptom | Cause | Resolution |
|---|---|---|
| Publishing from the portal returns `403` | Public network access is disabled, so the portal can't complete publishing | Use the API-based flow in this article. You can also download the manifest `.zip` and create the agent from it in the [Microsoft 365 admin center](https://admin.cloud.microsoft). |
| The channel adapter can't reach the agent | DNS, DNAT, or TLS isn't configured | Confirm your `A` record points to the firewall, the DNAT rule forwards port 443 to the reverse proxy, and the reverse proxy presents a certificate for your hostname. |
| The agent receives messages but never replies | Outbound traffic is blocked | Allow outbound access to `smba.trafficmanager.net`, `login.microsoftonline.com`, and `login.botframework.com`. |
| Requests reach the agent but are rejected | Token validation fails | Confirm the `validate-jwt` policy uses issuer `https://api.botframework.com` and an audience that matches your bot's Microsoft App ID. |

### Find your published agent

If you can't find your agent in the Microsoft 365 Copilot or Microsoft Teams agent store, use the following table.

| Symptom | Cause | Resolution |
|-------|-------|------------|
| The agent doesn't appear right after publishing | The store cache refreshes only when you open the store, on about a one-hour cycle. For organization scope, admin approval might still be pending. | For **Just you** (portal) or `Shared` (API) agents, clear the store cache or sign out and sign back in. For **People in your organization** (portal) or `Tenant` (API) agents, confirm a Microsoft 365 admin approved the request in the [Microsoft 365 admin center](https://admin.cloud.microsoft/?#/agents/all/requested). |
| The agent isn't where you expect it | You're looking in the wrong section for the publish scope | **Just you** (portal) or `Shared` (API) agents appear under **Your agents**. **People in your organization** (portal) or `Tenant` (API) agents appear under **Built by your org**. |

### Runtime issues

Use the following table for errors when you chat with a published agent in Microsoft 365 Copilot or Microsoft Teams.

> [!NOTE]
> End users don't need a Microsoft 365 Copilot license to use a published agent in Microsoft 365 Copilot Chat. Without a Copilot license, usage that accesses shared tenant data, such as SharePoint or Copilot connectors, might incur usage-based charges. For more information, see [Licensing and cost considerations for Copilot extensibility](/microsoft-365/copilot/extensibility/cost-considerations).

| Symptom | Cause | Resolution |
|---------|-------|------------|
| **Conversation stuck.** The agent stops responding, or returns `no tool output found`. | The conversation entered a locked state after a tool error, so later messages keep failing. | Reset the conversation. See [Reset a conversation](#reset-a-conversation). |
| **Insufficient permissions.** Authorization errors when you chat with the agent. | The user doesn't have access to the Foundry project, or the agent is published to `Shared` scope, which uses Azure role-based access control. | Verify the user has access to the Foundry project and an appropriate role, or publish to `Tenant` scope so users get access through admin approval. |
| **Agent identity missing resource permissions.** The agent works in the Foundry playground but fails after publishing. | The agent's identity is missing permissions for the resources it uses. | Assign the required roles to the agent's identity for any Azure resources it accesses. |
| **Agent identity disabled.** Authentication or agent identity errors occur during execution. | The agent identity application is disabled. | Verify the agent identity is enabled, and re-enable it if necessary. |
| **MCP approval required.** Requests fail with an error that an MCP approval request wasn't approved. | A required MCP tool approval was missed or dismissed. | Approve the pending MCP request in the conversation. If the approval card is no longer available, start a new conversation and retry. |
| **Missing required license.** Tool calls fail because required services are unavailable. | The required licenses or service plans aren't assigned to the user. | Verify that all required licenses and service plans are assigned and enabled. |
| **Authentication timeout.** Sign-in or authentication fails or times out. | The authentication process wasn't completed before the timeout period expired. | Retry the sign-in process, and complete authentication before you submit the request again. |
| **Rate limit exceeded.** Requests fail with a rate-limit error. | Request volume exceeded the available capacity for the model deployment. | Wait and retry later. Reduce request frequency, or increase deployment capacity if the issue occurs frequently. |
| **Context length exceeded.** Requests fail because the prompt or conversation is too large. | The combined prompt, conversation history, or attachments exceed the model's context window. | Start a new conversation, or reduce the amount of content in the request. |
| **Unsupported file type.** A file upload fails. | The uploaded file type isn't supported. | Upload a supported file type, or convert the file to a supported format. |
| **Another response already in progress.** Requests fail because a previous request is still running. | The service can't start a new response while an existing response is active. | Wait for the current request to complete, then retry. If the session appears stuck, start a new conversation. |

### Reset a conversation

If a published agent stops responding, or returns an error such as `no tool output found`, the conversation can enter a state where later messages keep failing. To recover, start a fresh conversation with the agent:

- **Microsoft 365 Copilot**: Start a new chat with the agent.
- **Microsoft Teams**: Teams doesn't yet provide a way to start a new session, so send the agent the message `/foundry_new_preview` to reset the conversation.

You can't restore the previous conversation after you reset it. The agent responds normally in the new conversation.

<!--
Editorial note: The following categories are intentionally excluded from this public article and are covered in internal troubleshooting guides instead:
- Internal service errors
- Generic server errors
- Request ID collection guidance
- Incident references and escalation paths
- Monitoring and dashboard guidance
- Infrastructure implementation details
- Internal service dependencies and investigations
-->

## Related content

- [Publish agents to Microsoft 365 Copilot and Microsoft Teams](./publish-copilot.md)
- [Set up private networking for Foundry Agent Service](./virtual-networks.md)
- [Configure your agent endpoint and settings](./configure-agent.md)
- [Foundry agents and custom engine agents through the corporate firewall](https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/foundry-agents-and-custom-engine-agents-through-the-corporate-firewall/4502218)
