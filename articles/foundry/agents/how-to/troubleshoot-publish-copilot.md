---
title: "Troubleshoot publishing agents to Microsoft Copilot and Microsoft Teams"
description: "Resolve publishing, discovery, authorization, runtime, and network issues for Microsoft Foundry agents in Microsoft Copilot and Teams."
author: fosteramanda
ms.author: fosteramanda
ms.reviewer: aahill
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.topic: troubleshooting
ms.date: 09/28/2026
ms.custom: pilot-ai-workflow-jan-2026, dev-focus
ai-usage: ai-assisted
#CustomerIntent: As a developer, I want to troubleshoot publishing and runtime issues so that customers can use my agent in Microsoft Copilot and Microsoft Teams.
---

# Troubleshoot publishing agents to Microsoft Copilot and Microsoft Teams

Use this guide to resolve issues when you publish a Microsoft Foundry agent to
Microsoft Copilot and Microsoft Teams, find it in the agent store, or chat
with the published agent. It also covers publishing from a project that
disables public network access.

## Resolve publishing issues

Use the following table for errors that occur when you publish from the Foundry
portal or through the Microsoft 365 publish API.

| Symptom | Cause | Resolution |
|---|---|---|
| The publish request fails with a validation error. Example messages include `AppVersion can only contain digits and periods`, `AppVersion cannot start with 0`, `Developer name cannot exceed length of 32`, `Description cannot exceed length of 4000`, and `Developer Website URL must begin with 'https://'`. | The metadata or version is invalid. | Fix the field identified in the error, and retry. The version must contain only digits and periods and can't start with `0`. The developer name must be 32 characters or fewer, and the full description must be 4,000 characters or fewer. |
| The publish API reports that the app version already exists. | You republished an existing `appVersion`. | Increment `appVersion`. To roll out new agent behavior, update the agent version that receives traffic instead. |
| The publish API reports a missing field, such as `BotServiceArmId is required.` or `App scope is required. Must be one of 'Personal', 'Shared', or 'Tenant'`. | The request doesn't include a required field. | Pass a valid `botServiceArmId`, and set `publishScope` to `Personal`, `Shared`, or `Tenant`. |
| The publish API rejects a color or outline icon. Example messages include `ColorIconBase64 is not valid base64.`, `ColorIconBase64 must be a PNG image.`, and `ColorIconBase64 must be a 192x192 PNG image.` | The icon doesn't meet the format, dimensions, or encoding requirements. | Provide a 192×192 color PNG and a 32×32 outline PNG. Base64-encode each image, and keep it within the size limit. |
| **Download ZIP** doesn't return a package. | The request or generated manifest failed validation. | Correct the field identified in the error, and retry. Foundry doesn't return a package that fails manifest validation. |
| Teams rejects a package that downloaded successfully. | A required file, generated identifier, or manifest section changed after download. | Download the package again, and limit customizations to supported user-facing metadata and assets. |
| The package download API returns `400` and no ZIP file. | The request fields or generated manifest failed validation. The download endpoint doesn't return an unvalidated package. | Correct the validation error, and call the download endpoint again. The request body follows the same validation rules as the publish request. |
| The package download API returns `401` or `403`. | The token is missing or invalid, the caller lacks agent write permission, or the request wasn't sent through the Foundry project endpoint. | Get a token for the `https://ai.azure.com` audience, confirm that the caller has the **Foundry User** role or equivalent agent write permission, and use the project endpoint. |
| The package download API returns `429`. | The service is throttling the request. | Wait for the duration in the `Retry-After` response header, and then retry. |
| Azure Bot Service creation fails. | Your account doesn't have the required permissions, or the `Microsoft.BotService` resource provider isn't registered. | Confirm that you can create resources in the target resource group. Register the `Microsoft.BotService` resource provider, and retry. |
| The portal or API returns `403 AuthorizationFailed` for `Microsoft.BotService/botServices/write`. | Your identity can't create or update the Azure Bot Service resource in the target resource group. | Assign the **Azure Bot Service Contributor Role**, or the broader **Contributor** or **Owner** role, on the resource group. Refresh your credentials, reopen the publish flow, and retry. |
| The publish request returns an identity error, or `agent.identity` is null. | The agent doesn't have a unique identity. | [Migrate the agent application to the new agent model](./migrate-agent-applications.md), and then publish the migrated agent. |
| The publish API reports `The acting user does not have the required permission on the workspace.` | Your identity doesn't have agent write access on the Foundry project. | Assign a role that grants agent write access on the Foundry project, and retry. |
| The portal reports that the agent uses an older format that can no longer be published. | The generally available publishing flow doesn't support new publishing for the older agent application format. | [Migrate the agent application to the new agent model](./migrate-agent-applications.md), and then publish. Existing agents in the older format keep working and can still be updated. |

## Find a published agent

If you can't find your agent in the Microsoft Copilot or Microsoft Teams
agent store, check its publish scope, approval status, and the store cache.

| Symptom | Cause | Resolution |
|---|---|---|
| The agent doesn't appear immediately after publishing. | The store cache refreshes when you open the store, on about a one-hour cycle. For organization scope, admin approval might still be pending. | For **Just you** in the portal or `Shared` through the API, clear the store cache or sign out and sign back in. For **People in your organization** in the portal or `Tenant` through the API, confirm that a Microsoft 365 admin approved the request in the [Microsoft 365 admin center](https://admin.cloud.microsoft/?#/agents/all/requested). |
| The agent isn't in the expected section of the store. | The publish scope determines where the agent appears. | Look under **Your agents** for **Just you** or `Shared` agents. Look under **Built by your org** for approved **People in your organization** or `Tenant` agents. |

## Resolve runtime issues

Use the following table when an agent is available in Microsoft Copilot or
Microsoft Teams but fails when a user chats with it.

> [!NOTE]
> End users don't need a Microsoft 365 Copilot license to use a published agent
> in Microsoft Copilot Chat. Without a Copilot license, usage that accesses
> shared tenant data, such as SharePoint or Copilot connectors, might incur
> usage-based charges. For more information, see
> [Licensing and cost considerations for Copilot extensibility](/microsoft-365/copilot/extensibility/cost-considerations).

| Symptom | Cause | Resolution |
|---|---|---|
| The conversation is stuck, the agent stops responding, or the agent returns `no tool output found`. | The conversation entered a locked state after a tool error, so later messages keep failing. | [Reset the conversation](#reset-a-conversation). |
| The user receives an insufficient permissions or authorization error. | The user doesn't have access to the Foundry project, or the agent is published to `Shared` scope, which uses Azure role-based access control. | Verify that the user has access to the Foundry project and an appropriate role. Alternatively, publish to `Tenant` scope so users get access through admin approval. |
| The agent works in the Foundry playground but fails after publishing. | The agent's identity doesn't have permissions for one or more Azure resources that the agent uses. | Assign the required roles to the agent's identity for each Azure resource it accesses. |
| Authentication or agent identity errors occur during execution. | The agent identity application is disabled. | Verify that the agent identity is enabled, and reenable it if necessary. |
| A request fails because an MCP approval request wasn't approved. | A required MCP tool approval was missed or dismissed. | Approve the pending MCP request in the conversation. If the approval card is no longer available, start a new conversation and retry. |
| Tool calls fail because required services are unavailable. | The required licenses or service plans aren't assigned to the user. | Verify that all required licenses and service plans are assigned and enabled. |
| Sign-in or authentication fails or times out. | The authentication process wasn't completed before the timeout period expired. | Retry sign-in, and complete authentication before you submit the request again. |
| The sign-in card opens, but the redirect URL doesn't load or authentication doesn't complete. | A firewall or proxy on the user's network blocks the Foundry redirect domain. | Allow outbound HTTPS access on TCP port 443 to `*.azureml.ms`, and then retry signing in from the Teams card. |
| A request fails with a rate-limit error. | Request volume exceeded the available capacity for the model deployment. | Wait and retry later. Reduce the request frequency, or increase deployment capacity if the issue occurs frequently. |
| A request fails because the prompt or conversation is too large. | The combined prompt, conversation history, or attachments exceed the model's context window. | Start a new conversation, or reduce the amount of content in the request. |
| A file upload fails because the file type isn't supported. | The agent doesn't support the uploaded file type. | Upload a supported file type, or convert the file to a supported format. |
| A request reports that another response is already in progress. | The service can't start a new response while an existing response is active. | Wait for the current request to complete, and then retry. If the session appears stuck, start a new conversation. |

### Reset a conversation

If a published agent stops responding or returns an error such as
`no tool output found`, start a fresh conversation:

- In Microsoft Copilot, start a new chat with the agent.
- In Microsoft Teams, send the agent `/foundry_new_preview` to reset the
  conversation. Teams doesn't currently provide another way to start a new
  session.

You can't restore the previous conversation after you reset it. The agent
responds normally in the new conversation.

## Resolve virtual network issues

The following issues apply to projects that disable public network access. For
the required publishing configuration and network flow, see
[Publish agents from a virtual network by using the REST API](./publish-copilot-virtual-network.md).

| Symptom | Cause | Resolution |
|---|---|---|
| Publishing from the portal returns `403`. | Public network access is disabled, so the portal can't complete publishing. | Use the REST API flow from a client that can reach the project's private endpoint. You can also download the manifest `.zip` and create the agent from it in the [Microsoft 365 admin center](https://admin.cloud.microsoft). |
| The channel adapter receives `403 NetworkAccessDenied`. | `enable_m365_public_endpoint` is omitted or set to `false`, or the request source IP doesn't match an Azure Bot Service or Microsoft 365 range. | Set `agent_endpoint.protocol_configuration.activity.enable_m365_public_endpoint` to `true`. Confirm that the request is sent through Azure Bot Service, Microsoft Copilot, or Teams. Direct requests from other public networks are blocked. |
| A direct Activity Protocol request over the public internet receives `403 NetworkAccessDenied`. | The caller's source IP isn't in an allowed service range. | Test the published agent through Microsoft Copilot or Teams. Direct public requests from arbitrary networks aren't allowed. |
| Requests reach the Activity Protocol endpoint but are rejected. | A Bot Service authorization scheme isn't configured, or the caller isn't in the project's tenant. | Configure `BotServiceRbac` or `BotServiceTenant`, and verify that the user signs in from the same tenant as the project. Guest users can't call these agents. |

## Related content

- [Publish agents to Microsoft Copilot and Microsoft Teams](./publish-copilot.md)
- [Publish agents from a virtual network by using the REST API](./publish-copilot-virtual-network.md)
- [Configure your agent endpoint and settings](./configure-agent.md)
