---
title: "Integrate telephony channels with a voice agent"
description: "Integrate Microsoft Teams Phone or Twilio with a Microsoft Foundry voice-first agent so callers can reach the agent over the phone."
author: sdgilley
ms.author: sgilley
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.topic: how-to
ms.date: 09/17/2026
ms.custom: preview
ai-usage: ai-assisted
zone_pivot_groups: voice-agent-telephony-setup
#customer intent: As a developer, I want to integrate a telephony channel with my voice-first agent so that callers can reach the agent by dialing in.
---

# Integrate telephony channels with a voice agent

You can now directly import a phone number you purchased from a telephony provider and connect it to your voice agent. 

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

## Compare the channel integrations

| Path | Use it when | What you provide in Foundry |
| --- | --- | --- |
| Microsoft Teams | Your organization owns a service number in Teams and routes it through a Teams resource account to Azure Communication Services. | Teams resource-account object ID|
| Twilio | Your organization owns one or more active voice-capable numbers in Twilio. | Twilio Account SID and Auth Token. |

The Twilio option appears only in supported public-cloud environments.

## Understand the call path

The channel integration determines how an inbound call reaches the agent.

```text
Caller
  -> Teams resource-account number or Twilio number
  -> telephony provider
  -> Foundry project telephony endpoint
  -> telephony binding
  -> voice-based agent
```

For Microsoft Teams, your Teams tenant keeps ownership of the number and Azure Communication Services provides the call automation and media path:

1. A caller dials the Teams phone number.
1. Teams routes the call to your resource account.
1. The resource account routes the call to your Communication Services resource.
1. Communication Services raises a `Microsoft.Communication.IncomingCall` event through Event Grid to your agent's telephony callback endpoint.
1. Foundry matches the callee to a telephony binding, answers the call on your Communication Services resource, and streams the audio to the agent.

Because the Teams number stays in Teams, the agent can act as one destination among others in your existing call flow. You can leave auto attendants and call queues in place and route selected paths to the agent.

For Twilio, Foundry uses the selected project connection to discover the numbers in your Twilio account and create a binding for each number you select. You don't create an Azure Communication Services resource or Event Grid subscription for the Twilio path.



## Prerequisites

### Voice agent prerequisites

- A saved voice-first agent in a Foundry project that passes browser testing. See [Quickstart: Create a voice-first prompt agent](../quickstarts/prompt-voice-agent.md).
- [Foundry User role](../../concepts/rbac-foundry.md) on the project, to create and manage telephony bindings.

  [!INCLUDE [role-rename-note](../../includes/role-rename-note.md)]


### Teams Phone prerequisites

For the Teams path, you need:
- [Get Microsoft Teams Calling Plan phone numbers for your tenant](/microsoftteams/getting-phone-numbers-for-your-users).
- A Teams or Microsoft 365 administrator usually completes these steps:

  - Follow [Teams Phone System extensibility quick start](/azure/communication-services/quickstarts/tpe/teams-phone-extensibility-quickstart) to provision the application, bot, resource account, and Azure Communication Services association.
  - Create or select the Azure Communication Services resource that receives calls for the resource account.
  - Create the Teams resource account with the Phone Extensibility application ID.
  - Associate the resource account with the Azure Communication Services resource, and synchronize the resource account.
  - Acquire a Teams service number and assign it to the resource account. The number can use Calling Plan, Operator Connect, or Direct Routing according to your Teams telephony configuration.
  - Assign the **Microsoft Teams Phone Resource Account** license when required.
  - Provide Azure Communication Services server consent for the exact tenant and resource-account object ID.
  - Place a controlled call and confirm that Azure Communication Services emits `Microsoft.Communication.IncomingCall`.

- The Foundry owner needs to prepare:
  - The callable Teams number.
  - The Azure Communication Services ARM resource ID.
  - The resource-account object ID.
  - Confirmation that Azure Communication Services received the test call.

The current project-managed-identity flow requires the Foundry project and Azure Communication Services resource to be in the same Microsoft Entra tenant.

<!-- Screenshot: Teams resource account showing the service number and application association. Alt text: "Teams resource account with its assigned service number and Phone Extensibility application." -->

### Twilio prerequisites

For the Twilio path, you need:

- A [Twilio](https://www.twilio.com/phone-numbers) account with at least one active, voice-capable phone number.
- The Twilio **Account SID** and **Auth Token** if you need to create a Foundry project connection.
  
Treat the Twilio Auth Token as a secret. Enter it only in the Foundry connection dialog, and don't include it in documentation, logs, screenshots, or support requests.



::: zone pivot="foundry-portal"

## Connect a number in the Foundry portal

The portal provides separate setup flows for Microsoft Teams and Twilio.

### Open the phone-number channel

1. In Foundry, open **Build** > **Agents**.
1. Select the voice-based agent.
1. Open **Channels**.
1. In **Phone numbers**, select **Add a number**.
1. Select **Microsoft Teams** or **Twilio**.

<!-- Screenshot: Voice-first Channels page with Add a number, Microsoft Teams, and Twilio highlighted. Alt text: "Phone numbers channel menu for a voice-first agent with Microsoft Teams and Twilio options." -->

### Connect a Microsoft Teams number

The Microsoft Teams flow creates or updates the Azure Communication Services project connection and telephony binding. Depending on the secure-delivery option, Foundry can also configure the webhook application and IncomingCall Event Grid subscription.

#### Choose secure incoming-call delivery

When **Secure incoming-call delivery** is shown, choose the approved mode.

| Option | Use it when |
| --- | --- |
| **Automatic configuration (Recommended)** | Use when the tenant allows Foundry to create or update the webhook app, app-role assignments, and Event Grid subscription. |
| **Manual configuration** | **Use a customer-managed app registration and let Foundry configure Event Grid** - Use an approved dedicated single-tenant application. The signed-in user must own it or an administrator must complete the changes. Or **Event Grid and app registration are already configured** - Use only when authenticated Event Grid delivery to the exact Foundry webhook is already complete. Foundry skips that bootstrap work. |

For a customer-managed application:

1. Select an eligible single-tenant app registration.
1. Enter any governance reference required by your organization.
1. If the application isn't listed, confirm that you're an owner and refresh.
1. Ask a tenant administrator to complete required API permissions and app-role assignments.

Never disable authentication to work around a webhook validation error.

<!-- Screenshot: Secure-delivery choices and app-registration picker. Alt text: "Microsoft Teams phone-number dialog showing secure Event Grid delivery options." -->

#### Select Azure Communication Services

In **Azure Communication Services resource**, select the resource that receives the calls.

If it isn't listed:

- Confirm the tenant and subscription.
- Confirm you can read the resource.
- Confirm the expected resource provider is registered.
- Ask an Azure administrator to correct RBAC.

Foundry creates or updates the project connection to the Azure Communication Services endpoint and uses the project managed identity. Don't enter an Azure Communication Services key or connection string.

#### Enter the Teams number details

Enter the **Resource account object ID** that the Teams administrator provides. Foundry constructs:

```text
28:orgid:<resource-account-object-id>
```

### Connect a Twilio number

1. In **Phone numbers**, select **Add a number** > **Twilio**.
1. Select a compatible existing Twilio connection. If none is available, select **Create a new Twilio connection**.
1. To create a connection, enter:
   - A unique **Connection name**.
   - The Twilio **Account SID**. It starts with `AC` and contains 34 characters.
   - The Twilio **Primary Auth Token**.
1. Select **Connect** or **Continue**.
1. Select one or more voice-capable phone numbers discovered from the Twilio account. You can't select numbers without the Voice capability.
1. Select **Continue**.
1. Review the agent, connection, masked Account SID, and selected numbers.
1. Optionally change the display label for each number.
1. Select **Add selected numbers**.
1. Review the result for each number. Retry any number that has a failed or unconfirmed result.
1. Select **Done** after all binding operations finish.

Foundry stores the Twilio credentials in the project connection and creates a separate telephony binding for each selected number. If you don't find any voice-capable numbers, get a number in the Twilio Console and retry discovery.

<!-- Screenshot: Twilio add-number wizard showing connection selection, discovered voice-capable numbers, and review step. Alt text: "Twilio phone-number wizard with a project connection and selected voice-capable numbers." -->

### Manage a connected number

The **Phone numbers** card shows each connected number, its optional label, and its provider.

1. Open the number's actions menu.
1. Select **View details**.
1. Select **Edit** if the binding supports updates.
1. For Microsoft Teams, update the displayed phone number or label. The resource-account object ID and connection are read-only.
1. For Twilio, update the label. The phone number and connection are read-only.
1. Select **Save**.

::: zone-end

::: zone pivot="api"

## Understand telephony bindings

A telephony binding connects a provider-specific destination to one voice agent in your project.

A binding holds:

- A service-generated binding `id`.
- The provider and its destination, such as the Teams resource account object ID.
- A `status` of `active` or `suspended`, which lets you take a number offline without deleting the mapping.
- A `connection` that names the Foundry project connection for your provider. Secrets aren't stored in the binding itself.
- An `incoming_call_url` that the service generates for incoming-call delivery.

The agent that owns the binding is identified by the request path. Create and list bindings at `{projectEndpoint}/agents/{agentName}/telephony/bindings`. To get, update, or delete one binding, append `/{bindingId}`.

Binding reads return an `ETag`. Send that value in `If-Match` when updating or deleting the binding to avoid overwriting a concurrent change. Transfer targets are configured separately for the agent, not on each binding.

## Connect a number by using the API

The REST examples in this section use Microsoft Teams Phone Extensibility. Use the Foundry portal for the Twilio connection and number-discovery flow.

Replace `{projectEndpoint}` with your Foundry project endpoint and `{agentName}` with the voice agent's name. For each Foundry request, send a Microsoft Entra bearer token for `https://ai.azure.com/` and the `Foundry-Features: VoiceAgents=V1Preview` header.

### Create a connection to Communication Services

Create a project connection of type Azure Communication Services that points at your Communication Services resource by its Azure resource ID. Foundry uses this connection to answer incoming calls on your behalf.

Choose one of these authentication types:

| Authentication | What you provide | When to use it |
|---|---|---|
| Project managed identity | Nothing | The simplest option. Grant the project identity a role on the Communication Services resource. |
| Account managed identity | Nothing | The Foundry account identity answers calls instead of the project identity. |
| User-assigned managed identity | Resource ID and client ID | You already manage a dedicated identity for telephony. |
| Service principal | Tenant ID, client ID, and client secret | A dedicated application identity instead of managed identity. |
| Connection string | The Communication Services connection string | Fastest to configure. Requires you to rotate a secret. |

For a managed identity or service principal, grant that principal a role on the target Communication Services resource before you create the binding.

### Create the binding

Create the binding on the agent. Set `connection` to the project connection name and `resource_account_object_id` to the Teams resource account's Microsoft Entra object ID. The optional `phone_number` is a display number for the resource account.

```http
POST {projectEndpoint}/agents/{agentName}/telephony/bindings?api-version=v1
Authorization: Bearer <access-token>
Foundry-Features: VoiceAgents=V1Preview
Content-Type: application/json

{
  "provider": "teams_phone_extension",
  "connection": "my-acs-connection",
  "resource_account_object_id": "00000000-0000-0000-0000-000000000000",
  "phone_number": "+12065550123",
  "label": "Support line"
}
```

Don't send the `28:orgid:` prefix, `identifier`, or `provider_config` in this request.

The service returns `201 Created`, the binding's `id` and `incoming_call_url`, and an `ETag` response header. Save the binding ID for later requests. Use the returned `incoming_call_url` in the next step instead of constructing a callback path.

### Read or update the binding

Read the binding to get its current properties and `ETag`:

```http
GET {projectEndpoint}/agents/{agentName}/telephony/bindings/{bindingId}?api-version=v1
Authorization: Bearer <access-token>
Foundry-Features: VoiceAgents=V1Preview
```

Use `PATCH` with `application/merge-patch+json` to update the binding. For example, suspend new inbound calls without deleting the binding:

```http
PATCH {projectEndpoint}/agents/{agentName}/telephony/bindings/{bindingId}?api-version=v1
Authorization: Bearer <access-token>
Foundry-Features: VoiceAgents=V1Preview
Content-Type: application/merge-patch+json
If-Match: <etag-from-latest-binding-read>

{
  "status": "suspended"
}
```

Set `status` to `active` to accept new calls again. Read the latest `ETag` before each update. You can't change the binding's provider.

### Register the Event Grid subscription

Communication Services must deliver its `IncomingCall` events to your agent. Create an event subscription on the Communication Services resource that targets the binding's `incoming_call_url`.

Before running the Bash example, sign in with `az login` and set these variables:

| Variable | Value |
| --- | --- |
| `eventSubscriptionName` | A name for the Event Grid event subscription. |
| `acsResourceId` | The Azure resource ID of the Communication Services resource. |
| `webhook` | The `incoming_call_url` returned when you create the binding. |
| `webhookTenantId` | The tenant ID configured for the webhook application. |
| `webhookApplicationIdOrUri` | The webhook application's client ID or Application ID URI. |

Complete the application and role setup in [Deliver events to Microsoft Entra protected endpoints](/azure/event-grid/secure-webhook-delivery) first. Obtain the webhook tenant and audience from the administrator who configures secure incoming-call delivery. The webhook application identifies the token audience; it isn't the Microsoft Event Grid first-party application.

```azurecli
az eventgrid event-subscription create \
  --name "$eventSubscriptionName" \
  --source-resource-id "$acsResourceId" \
  --endpoint-type webhook \
  --endpoint "$webhook" \
  --included-event-types Microsoft.Communication.IncomingCall \
  --event-delivery-schema eventgridschema \
  --azure-active-directory-tenant-id "$webhookTenantId" \
  --azure-active-directory-application-id-or-uri "$webhookApplicationIdOrUri"
```

Reference: [az eventgrid event-subscription create](/cli/azure/eventgrid/event-subscription#az-eventgrid-event-subscription-create).

During creation, Event Grid sends a validation event that the endpoint answers automatically.

Foundry validates the Microsoft Entra token that Event Grid attaches to each delivery, and then requires an active binding whose project, agent, Communication Services resource, and callee all match the event. Calls that don't match a binding aren't answered.

Event Grid allows up to 500 event subscriptions per Communication Services system topic, which caps how many resource accounts you can route through a single Communication Services resource.

::: zone-end

## Configure transfer to a person

An agent that can't complete a request should reach a human rather than end the call. Configure named transfer targets for the agent. These targets are separate from its telephony bindings.

First, read the current target list and its `ETag` response header:

```http
GET {projectEndpoint}/agents/{agentName}/telephony/transfer_targets?api-version=v1
Authorization: Bearer <access-token>
Foundry-Features: VoiceAgents=V1Preview
```

Replace the target list with `PUT`, using the returned `ETag` in `If-Match`. Include every target you want to keep: this operation replaces the entire list, and an empty array clears it.

```http
PUT {projectEndpoint}/agents/{agentName}/telephony/transfer_targets?api-version=v1
Authorization: Bearer <access-token>
Foundry-Features: VoiceAgents=V1Preview
Content-Type: application/json
If-Match: <etag-from-latest-transfer-targets-read>

{
  "transfer_targets": [
    {
      "name": "billing",
      "description": "Billing and payment questions",
      "destination": { "kind": "pstn", "value": "+14255550111" }
    },
    {
      "name": "operator",
      "description": "A person at the front desk",
      "destination": { "kind": "teams", "value": "28:orgid:00000000-0000-0000-0000-000000000000" }
    }
  ]
}
```

A `teams` destination can be a Teams user, or the resource account of a call queue or auto attendant. That's how a voice agent hands a caller back into an existing Teams call flow.

Give each target a `description` that says when to use it. The agent chooses based on that text.

Transfer requests select a target from the agent's configured list rather than supplying an arbitrary destination.

## Manage a live call

List the agent's calls, and use the service-generated call `id` as `{callId}` in subsequent requests:

```http
GET {projectEndpoint}/agents/{agentName}/telephony/calls?api-version=v1
Authorization: Bearer <access-token>
Foundry-Features: VoiceAgents=V1Preview
```

To transfer an active call to the configured `operator` target:

```http
POST {projectEndpoint}/agents/{agentName}/telephony/calls/{callId}:transfer?api-version=v1
Authorization: Bearer <access-token>
Foundry-Features: VoiceAgents=V1Preview
Content-Type: application/json

{ "target": "operator" }
```

To end an active call, send a separate request with no request body:

```http
POST {projectEndpoint}/agents/{agentName}/telephony/calls/{callId}:end?api-version=v1
Authorization: Bearer <access-token>
Foundry-Features: VoiceAgents=V1Preview
```

Both operations return the call record. To inspect the call's current status and lifecycle events, use `GET {projectEndpoint}/agents/{agentName}/telephony/calls/{callId}?api-version=v1`.

## Configure audio for phone calls

Phone networks carry narrowband audio, so tune the agent for the channel:

- Set `noise_reduction` to `azure_deep_noise_suppression` for contact center traffic.
- Increase `silence_duration_ms`. Callers on a phone pause more than callers at a keyboard.
- Add `phrase_list` hints for the identifiers callers read aloud, such as order or policy numbers.
- Attach the `end_conversation` system tool so the agent can end a completed call.

See [Configure a voice agent](configure-voice-agent.md).

## Test the call

1. Wait for the selected provider and binding changes to propagate. For Microsoft Teams, also allow time for Azure Communication Services and Event Grid propagation.
1. From a controlled caller, call the configured number.
1. Confirm the agent answers.
1. Complete a short conversation.
1. Interrupt the agent.
1. Use one safe tool or knowledge path.
1. Test the approved human-handoff behavior.
1. End the call.
1. Confirm that monitoring and trace data appear.

Record:

- Test timestamp and time zone.
- Called number.
- Callee identifier.
- Telephony provider and provider call ID, such as an Azure Communication Services correlation ID or Twilio Call SID.
- Agent name and version.
- For Microsoft Teams, the Azure Communication Services resource ID and Event Grid delivery result.
- For Twilio, the Foundry project connection name.

<!-- Screenshot: Phone numbers card showing connected numbers and their actions menus. Alt text: "Voice-agent phone-number channel with connected numbers and provider badges." -->

## Trace phone calls

When a call arrives through telephony, the session's root trace span records the provider, the provider's call ID, and the dialed and calling numbers. You can correlate a Foundry session with a record in your telephony provider.

Caller and callee phone numbers are personal data. Review who can read your project's Application Insights resource before you enable content capture. See [Voice agent tracing, monitoring, and evaluation](../concepts/voice-agent-observability.md).

## Troubleshoot telephony

| Symptom | What to check |
| --- | --- |
| Busy signal and no Azure Communication Services event | Teams number activation, license, PSTN connectivity, calling bot channel, TPE association, synchronization, and Azure Communication Services consent. |
| Azure Communication Services receives the call but Foundry reports no binding | Compare `IncomingCall.data.to.rawId` with the full binding identifier, including prefix and formatting. |
| Event Grid validation fails | Endpoint, tenant, webhook audience, app-role assignment, delivery identity, and Event Grid write access. |
| Secure setup reports a Graph permission error | Ask a tenant administrator to grant the approved application-management permissions and retry. |
| Azure Communication Services `AnswerCall` returns 401 or 403 | Project connection target, project managed identity, Azure Communication Services role assignment, and RBAC propagation. |
| Call connects but is silent | Media endpoint reachability, selected model and voice, output device path, and required PCM media format. |
| Call disconnects unexpectedly | Callback reachability, media errors, service limits, and correlation logs. |
| The wrong agent answers | Confirm the agent that owns the binding collection and inspect that agent's active version. |
| The number doesn't appear after refresh | Query active bindings and confirm provisioning completed; don't rely only on temporary browser state. |
| Twilio numbers don't load | Confirm the project connection uses the correct Account SID and Primary Auth Token, and that you can read the connection credentials. |
| No Twilio numbers can be selected | Confirm the Twilio account owns an active number with the Voice capability. |
| Twilio rejects the credentials | Update or recreate the project connection with the current Account SID and Primary Auth Token. |
| A Twilio number is already bound | Use the existing binding or disconnect it from the other agent before retrying. |
| A binding update, deletion, or transfer-target replacement fails with a precondition error | Read the resource again, review any concurrent changes, and use the latest `ETag` in `If-Match`. |

## Disconnect a number

::: zone pivot="foundry-portal"

1. Open the agent **Channels** tab.
1. In **Phone numbers**, open the number's actions menu.
1. Select **Disconnect number**.
1. Confirm.

::: zone-end

::: zone pivot="api"

Read the binding to get its current `ETag`, and then delete it by using that value in `If-Match`.  

```http
GET {projectEndpoint}/agents/{agentName}/telephony/bindings/{bindingId}?api-version=v1
Authorization: Bearer <access-token>
Foundry-Features: VoiceAgents=V1Preview
```

```http
DELETE {projectEndpoint}/agents/{agentName}/telephony/bindings/{bindingId}?api-version=v1
Authorization: Bearer <access-token>
Foundry-Features: VoiceAgents=V1Preview
If-Match: <etag-from-latest-binding-read>
```

A successful deletion returns `204 No Content`.

::: zone-end

Disconnecting removes the Foundry binding. It doesn't:

- Release the Teams or Twilio number.
- Remove the Teams resource account.
- Delete Azure Communication Services.
- Remove the bot or app registration.
- Revoke Teams Phone Extensibility consent.
- Delete the Twilio account or the Foundry project connection.

Coordinate upstream cleanup separately.

## Security checklist

- Use Microsoft Entra authentication and managed identities.
- Don't share Azure Communication Services keys, connection strings, tokens, bot secrets, or portal cookies.
- Don't share Twilio Account SIDs together with Auth Tokens, and rotate an Auth Token if it is exposed.
- Validate that the Event Grid topic is the intended Azure Communication Services resource.
- Use the exact public Foundry project webhook endpoint.
- Keep webhook audience and Event Grid delivery identity concepts separate.
- Use a dedicated single-tenant webhook application when governance requires it.
- Don't persist service-generated call callback or media tokens.
- Confirm the binding target before update or deletion.
- Apply recording, consent, disclosure, retention, and privacy requirements.
- Prevent sensitive caller data from being read aloud or unnecessarily stored.

## Related content

- [Configure a voice agent](configure-voice-agent.md)
- [Publish and share a voice-based agent](voice-agent-channels-publish.md)
- [Voice agent tracing, monitoring, and evaluation](../concepts/voice-agent-observability.md).
- [Best practices for voice-based agents](../concepts/voice-agent-best-practice.md)
- [Call automation in Azure Communication Services](/azure/communication-services/concepts/call-automation/call-automation)
- [Manage resource accounts in Microsoft Teams](/microsoftteams/manage-resource-accounts)
- [Azure Event Grid security and authentication](/azure/event-grid/security-authentication)
