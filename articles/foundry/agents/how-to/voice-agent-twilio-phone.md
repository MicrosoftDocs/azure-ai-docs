---
title: "Connect a voice agent to a Twilio phone number"
description: "Connect a Microsoft Foundry voice-first agent to a Twilio phone number so callers reach the agent over the phone."
author: sdgilley
ms.author: sgilley
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.topic: how-to
ms.date: 08/31/2026
ms.custom: preview
ai-usage: ai-assisted
zone_pivot_groups: voice-agent-telephony-setup
#customer intent: As a developer, I want to connect my voice-first agent to a Twilio phone number so that callers can reach the agent by dialing in.
---

# Connect a voice agent to a Twilio phone number

You can now directly import a phone number you purchased from Twilio and connect it to your voice agent. 

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]


## Prerequisites

- Existing phone numbers purchased from [Twilio](https://www.twilio.com/phone-numbers).
- Twilio **Account SID** and **Auth Token**.
- A saved voice-first agent in a Foundry project that passes browser testing. See [Quickstart: Create a voice-first prompt agent](../quickstarts/prompt-voice-agent.md).


::: zone pivot="foundry-portal"

## Connect a number in the Foundry portal

The portal walks you through selecting the Azure Communication Services resource, choosing secure delivery, and entering the identifier. It then creates the project connection, the telephony binding, and the Event Grid subscription for you.

### Open the phone-number channel

1. In Foundry, open **Build** > **Agents**.
1. Select the voice-first agent.
1. Open **Channels**.
1. In **Phone numbers**, select **Add a number**.
1. Select **Twilio**.

<!-- Screenshot: Voice-first Channels page with Add a number and Twilio highlighted. Alt text: "Twilio Phone numbers channel menu for a voice-first agent." -->


### Add the number

Enter your Twilio *Account SID* and the primary *Auth Token*.

The number appears in the **Select phone numbers** card after provisioning succeeds.

::: zone-end

::: zone pivot="api"

## Connect a number by using the API

Replace `{projectEndpoint}` with your Foundry project endpoint and `{agentName}` with the voice agent's name. For each Foundry request, send a Microsoft Entra bearer token for `https://ai.azure.com/` and the `Foundry-Features: VoiceAgents=V1Preview` header.

### Create the binding

Create the binding on the agent. Set `connection` to the project connection name. The optional `phone_number` is a display number for the resource account.

```http
POST {projectEndpoint}/agents/{agentName}/telephony/bindings?api-version=v1
Authorization: Bearer <access-token>
Foundry-Features: VoiceAgents=V1Preview
Content-Type: application/json

{
  "provider": "twilio",
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
      "destination": { "kind": "twilio", "value": "28:orgid:00000000-0000-0000-0000-000000000000" }
    }
  ]
}
```

A `twilio` destination can be a Twilio user, or the resource account of a call queue or auto attendant. That's how a voice agent hands a caller back into an existing Twilio call flow.

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
- Azure Communication Services resource ID.
- Agent name and version.
- Event Grid delivery result.
- Azure Communication Services call correlation ID.

<!-- Screenshot: Phone numbers card showing the connected number and actions menu. Alt text: "Voice-agent phone-number channel after a Twilio number is connected." -->

## Trace phone calls

When a call arrives through telephony, the session's root trace span records the provider, the provider's call ID, and the dialed and calling numbers. You can correlate a Foundry session with a record in your telephony provider.

Caller and callee phone numbers are personal data. Review who can read your project's Application Insights resource before you enable content capture. See [Voice agent tracing, monitoring, and evaluation](../concepts/voice-agent-observability.md).

## Troubleshoot telephony

| Symptom | What to check |
| --- | --- |
| Busy signal and no services event | Twilio number activation. |
| Call connects but is silent | Media endpoint reachability, selected model and voice, output device path, and required PCM media format. |
| Call disconnects unexpectedly | Callback reachability, media errors, service limits, and correlation logs. |
| The wrong agent answers | Confirm the agent that owns the binding collection and inspect that agent's active version. |
| The number doesn't appear after refresh | Query active bindings and confirm provisioning completed; don't rely only on temporary browser state. |
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

- Release the Twilio number.
- Remove the Twilio resource account.
- Delete Azure Communication Services.
- Remove the bot or app registration.
- Revoke Twilio Phone Extensibility consent.

Coordinate upstream cleanup separately.

## Security checklist

- Use Microsoft Entra authentication and managed identities.
- Don't share Azure Communication Services keys, connection strings, tokens, bot secrets, or portal cookies.
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
- [Publish and share a voice-first agent](voice-agent-channels-publish.md)
- [Voice agent tracing, monitoring, and evaluation](../concepts/voice-agent-observability.md).
- [Best practices for voice-first agents](../concepts/voice-agent-best-practice.md)
- [Call automation in Azure Communication Services](/azure/communication-services/concepts/call-automation/call-automation)
- [Azure Event Grid security and authentication](/azure/event-grid/security-authentication)
