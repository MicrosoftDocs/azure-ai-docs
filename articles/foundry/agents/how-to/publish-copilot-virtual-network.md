---
title: "Publish a virtual network agent to Microsoft 365 and Teams"
description: "Publish a Microsoft Foundry agent that runs in a virtual network to Microsoft 365 Copilot and Microsoft Teams when public network access is disabled."
author: fosteramanda
ms.author: fosteramanda
ms.reviewer: aahill
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.topic: how-to
ms.date: 06/08/2026
ms.custom: pilot-ai-workflow-jan-2026
ai-usage: ai-assisted
#CustomerIntent: As a developer who runs a Foundry agent inside a virtual network, I want to publish it to Microsoft 365 Copilot and Teams so that users can reach it even though public network access is disabled.
---

# Publish agents in a virtual network to Microsoft 365 Copilot and Teams

> [!IMPORTANT]
> Publishing agents to Microsoft 365 Copilot and Microsoft Teams is an "Early Access Preview" and is licensed to you as part of your Azure subscription and subject to terms applicable to "Previews" and "Early Access Previews" in the [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/) and the [Microsoft Products and Services Data Protection Addendum](https://www.microsoft.com/licensing/docs/view/Microsoft-Products-and-Services-Data-Protection-Addendum-DPA) ("DPA"). It is your responsibility to manage whether your data flows outside of your organization's Azure compliance and geographic boundaries and any related implications.

When your Microsoft Foundry project disables public network access (PNA) and runs behind a private endpoint, the one-click **Publish to Teams and Microsoft 365 Copilot** button in the Foundry portal isn't available. The Microsoft channel adapters that deliver Teams and Copilot messages run outside your network, but your agent's endpoint resolves to a private IP address they can't reach.

This article shows the manual flow that replaces the button. When you finish, users in your tenant can use your agent in Microsoft 365 Copilot and Teams while it stays on your private network.

## Prerequisites

- Access to the [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs).
- A [Foundry project](../../how-to/create-projects.md) configured with [private networking](./virtual-networks.md): the project's Foundry resource uses a private endpoint, and public network access is disabled.
- An agent in that project that you tested and want to publish. Test the agent thoroughly and select the active version that consumers interact with. For more information, see [Configure your agent endpoint and settings](./configure-agent.md).
- The following role assignments:
    - **Foundry User** role on the Foundry project to create, manage, and publish agents.
    - Permission to create an Azure Bot Service resource (for example, **Azure Bot Service Contributor**) in the target resource group.
    - Permission to manage the firewall, DNS, and reverse proxy that route inbound traffic to your network.
- [Azure CLI](/cli/azure/install-azure-cli) installed and signed in with `az login` to the subscription that contains your Foundry resource.
- The `Microsoft.BotService` resource provider registered in your subscription:

   ```azurecli
   az provider register --namespace Microsoft.BotService
   ```

## Steps

> [!NOTE]
> Steps 1 through 4 are the manual equivalent of the one-click **Publish to Teams and Microsoft 365 Copilot** button and work for any project, with or without public network access. Only step 5 (firewall and networking) is required for projects that disable public network access.

1. Get your agent's identity and tenant ID.
1. Create an Azure Bot Service resource.
1. Enable the activity protocol and add BotServiceRbac or BotServiceTenant as an authorization scheme on the agent.
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

In the JSON response, copy `instance_identity.principal_id`. Also copy `versions.latest.agent_guid` for the publish step.

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

## Step 3: Enable the activity protocol and Bot Service authorization

Interacting with an agent from Microsoft 365 and Teams requires two additions to the agent endpoint: the **`activity`** protocol, which lets the channel adapters deliver messages, and a **Bot Service authorization scheme**, which controls who can call the agent.

Choose one authorization scheme:

| Authorization scheme | Who can call the agent from Microsoft 365 and Teams |
|---|---|
| `BotServiceRbac` | Only identities that have the Azure permissions required to call the agent in Foundry, through the portal, SDK, or REST API. |
| `BotServiceTenant` | Everyone in your tenant. |

The authorization scheme controls *who can call* the agent. This is separate from *visibility* — who sees the agent in the Microsoft 365 Copilot and Teams stores — which you set with `appPublishScope` in the publish request (step 4).

In the Foundry portal, the **Who can use this agent** option pairs the two as defaults: **Just you** applies `BotServiceRbac` with `Shared` visibility, and **People in your organization** applies `BotServiceTenant` with `Tenant` visibility. Because you call the API directly, you can combine them however you need. For example, publish org-wide for visibility (`Tenant`) but still restrict calling to Foundry users (`BotServiceRbac`). For more information, see [Publish agents to Microsoft 365 Copilot and Microsoft Teams](./publish-copilot.md).

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
        "protocols": [
            "responses",
            "activity"
        ],
        "authorization_schemes": [
            {
                "type": "Entra",
                "isolation_key_source": {
                    "kind": "Entra"
                }
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

> [!NOTE]
> The Microsoft 365 publish API is in preview. A generally available (GA) version is planned, and the request format might change when it ships.

| Placeholder | Description | Where to get it |
|---|---|---|
| `<region>` | Azure region of your Foundry resource, for example `eastus2` | Azure portal |
| `<subscription-id>` | Subscription that contains your Foundry resource | `az account show --query id -o tsv` |
| `<resource-group>` | Resource group that contains your Foundry resource | Azure portal |
| `<account-name>` | Foundry resource name | Foundry portal |
| `<project-name>` | Foundry project name | Foundry portal |
| `<agent-guid>` | The GUID of your agent | `versions.latest.agent_guid` from the get-agent response |
| `<agent-principal-id>` | Agent principal ID, sent as `botId` | `instance_identity.principal_id` from the get-agent response |
| `<agent-name>` | Your agent's name | Foundry portal |

```http
POST https://<region>.api.azureml.ms/agent-asset/v2.0/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.MachineLearningServices/workspaces/<account-name>@<project-name>@AML/microsoft365/publish
Authorization: Bearer {{token}}
Content-Type: application/json

{
  "agentGuid": "<agent-guid>",
  "botId": "<agent-principal-id>",
  "subscriptionId": "<subscription-id>",
  "agentName": "<agent-name>",
  "appPublishScope": "Shared",
  "publishAsDigitalWorker": false,
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

- `appPublishScope`: `Shared` (the portal's **Just you**) makes the agent available only to you. It appears under **Your agents** in the agent store, and you share it with a link. `Tenant` (the portal's **People in your organization**) submits the agent for Microsoft 365 admin approval and, once approved, makes it available to your whole organization under **Built by your org**.
- `appVersion`: a semantic version string such as `1.0.0`. Increment it to update the user-facing properties; republishing an existing version returns a `version already exists` error. To roll out a new agent version, update the agent version receiving traffic instead.
- `shortDescription` and `fullDescription`: descriptions shown in the agent store.
- `developerName`, `developerWebsiteUrl`, `privacyUrl`, and `termsOfUseUrl`: developer metadata shown to users.
- `publishAsDigitalWorker`: required; set to `false`. To publish as an autopilot agent, see [Foundry agents in Microsoft Agent 365](./agent-365.md).

> [!WARNING]
> Don't include secrets, API keys, or other sensitive information in any metadata field. These fields are visible to users.

A successful response returns the published agent metadata. The agent isn't reachable from Teams or Copilot until you configure networking in step 5.

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
- **Validate the caller's tenant ID.** The Bot Channel Adapter includes the caller's tenant ID in the `x-tenant-id` header. Reject any request whose tenant ID isn't your own.

A published agent's Teams app can be installed in any tenant, so requests from outside your organization can reach your endpoint before Foundry applies RBAC. Checking the tenant ID lets you drop calls from tenants you don't intend to serve. This combination is weaker than JWT validation, because any caller that reaches your endpoint can set a header. Pair it with the source IP restriction so that only the Bot Channel Adapter can present the header. Together, the two checks give customers without JWT-capable infrastructure a meaningful layer of defense.

## Verify the published agent

1. In Microsoft 365 Copilot or Microsoft Teams, open the agent store and find your agent. With `Shared` scope, it appears under **Your agents**. With `Tenant` scope, it appears under **Built by your org** after a Microsoft 365 admin approves it in the [Microsoft 365 admin center](https://admin.cloud.microsoft/?#/agents/all/requested).
1. Start a conversation and send a message.
1. Confirm the agent replies. A reply confirms that both the inbound path (channel adapter to agent) and the outbound path (agent reply to the channel) work.

## Troubleshooting

| Issue | Cause | Resolution |
|---|---|---|
| Publishing from the portal returns `403` | Public network access is disabled, so the portal can't complete publishing | Use the API-based flow in this article. You can also download the manifest `.zip` and create the agent from it in the [Microsoft 365 admin center](https://admin.cloud.microsoft). |
| The channel adapter can't reach the agent | DNS, DNAT, or TLS isn't configured | Confirm your `A` record points to the firewall, the DNAT rule forwards port 443 to the reverse proxy, and the reverse proxy presents a certificate for your hostname. |
| The agent receives messages but never replies | Outbound traffic is blocked | Allow outbound access to `smba.trafficmanager.net`, `login.microsoftonline.com`, and `login.botframework.com`. |
| Requests reach the agent but are rejected | Token validation fails | Confirm the `validate-jwt` policy uses issuer `https://api.botframework.com` and an audience that matches your bot's Microsoft App ID. |
| Organization-scope agent doesn't appear | Admin approval is pending | Confirm an admin approved the agent in the [Microsoft 365 admin center](https://admin.cloud.microsoft/?#/agents/all/requested). |

## Related content

- [Publish agents to Microsoft 365 Copilot and Microsoft Teams](./publish-copilot.md)
- [Set up private networking for Foundry Agent Service](./virtual-networks.md)
- [Configure your agent endpoint and settings](./configure-agent.md)
- [Foundry agents and custom engine agents through the corporate firewall](https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/foundry-agents-and-custom-engine-agents-through-the-corporate-firewall/4502218)
