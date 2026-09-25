---
title: "Publish and share a voice-based agent"
description: "Share a voice-based agent through a preview web app or phone-number channel and understand the available publishing paths."
author: varshasaha
ms.author: varshasaha
ms.date: 09/25/2026
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.topic: how-to
ai-usage: ai-assisted
# customer intent: As a developer, I want to publish and share a voice-based agent so that approved users can access it through supported channels.
---

# Publish and share a voice-based agent

This article explains how the voice-based channels experience differs from standard agent application and Microsoft Teams app publishing. In the Foundry portal, use the voice-based **Channels** tab to share a browser preview or connect a phone number. 


## Prerequisites

- A saved and tested voice-based agent.
- A selected agent version for customer testing.
- Permission to view and manage the agent.
- Application Insights if you want to monitor the shared experience.

## Understand the available paths

The following table summarizes the available publishing paths for voice-based agents. 

| Path | Use it for | Current voice-based behavior |
| --- | --- | --- |
| Playground | Developer testing with microphone, transcript, and avatar. | Available from the build page. |
| Preview web app | Browser-based sharing with people who have access. | Shown in the voice-based **Channels** tab when the endpoint supports the Responses protocol. |
| Phone numbers | Audio-only inbound calls. | Teams Phone extensibility and Twilio. |
| Standard Teams and Microsoft 365 Copilot publishing | A Teams or Microsoft 365 app backed by the agent. | The standard card is intentionally hidden from the current voice-based Channels layout. Don't use these steps as a substitute for Teams Phone extensibility integration. |
| Agent Application | A stable managed endpoint with a dedicated identity. | General Agent Application guidance might not represent the current native voice media path. Verify support before documenting or releasing this route. |

> [!IMPORTANT]
> "Publish to Microsoft Teams" and "connect a Microsoft Teams phone number" are different integrations. App publishing distributes a bot or agent app. [Teams Phone extensibility](/azure/communication-services/concepts/interop/tpe/teams-phone-extensibility-overview) routes a telephone call through Azure Communication Services to the voice agent.

## Open the Channels tab

In the Microsoft Foundry portal:
1. Select **Build** > **Agents**.
2. Select the voice-based agent.
3. Open **Channels**.

The current voice-based layout contains:

- **Phone numbers**.
- **Preview web app**.

The layout doesn't show the Routines card used by some text agents.

<!-- Screenshot: Voice-based Channels tab showing Phone numbers and Preview web app. Alt text: "Voice-agent Channels tab with phone-number and preview-web-app cards." -->

## Share the preview web app

The preview web app is available when the agent endpoint supports the Responses protocol.

### Open the web app

1. In **Preview web app**, select **Open web app**.
2. Complete a voice scenario in the new browser tab.
3. Confirm microphone permissions, session startup, transcript, voice output, and avatar behavior.

### Copy the web app link

1. Select **Copy web app link**.
2. Share the link only with the intended audience.
3. Tell recipients which organizational account to use.
4. Confirm they have access.

### Grant access

When **Grant access** is available:

1. Open the card's actions menu.
2. Select **Grant access**.
3. Add the approved users or groups.
4. Review the access scope.
5. Ask a recipient to validate the link with their own account.

The card identifies the experience as available to people in the organization. Don't treat possession of the link as authorization.

<!-- Screenshot: Preview-web-app actions showing open, copy, and grant-access controls. Alt text: "Preview web app channel controls for opening, copying, and granting access." -->

## Connect a phone number channel

In **Phone numbers**, select **Add a number** and follow [Integrate telephony channels with a voice agent](voice-agent-telephony-channels.md).

To place outbound calls, use the [outbound call-job API](voice-agent-telephony-channels.md#place-outbound-calls-by-using-the-api). Outbound jobs use a provider connection and don't require an inbound number binding.

After you connect a Microsoft Teams number, the **Publish** menu can offer **Call preview agent**. The dialog currently lists active Microsoft Teams phone-number bindings and provides a link back to the **Channels** tab when you need another number. Test Twilio numbers by calling them directly.

<!-- Screenshot: Call preview agent dialog listing active numbers. Alt text: "Call preview dialog showing phone numbers connected to the voice agent." -->

## Choose a release version

Treat the agent configuration like application code:

1. Save a version after completing configuration.
2. Test that exact version in the playground.
3. Test the preview web app.
4. Test each phone number.
5. Record the version used by the customer channel.
6. Repeat regression tests before changing the active version.

Don't point a customer channel at unsaved changes. Avoid automatically adopting every new version unless that change is an explicit release policy.

## Identity and access considerations

- Project collaborators can have broader access than preview-web-app users.
- Tool authentication can behave differently after a general Agent Application is published because the published application receives a distinct identity.
- Permissions assigned to the project identity don't automatically transfer to a separately published application identity.
- Phone-number provisioning uses a Foundry project connection for the selected provider. Teams requires Azure Communication Services; Twilio doesn't require Azure Communication Services or Event Grid.
- Use least-privilege roles for tools, data, Application Insights, ACS, Event Grid, and app registrations.

## Validate a shared experience

For each channel, test:

- Authentication and authorization.
- Microphone and audio behavior.
- The greeting and AI disclosure.
- Recognition and turn-taking.
- Tool and knowledge calls.
- Human handoff.
- Session end and reconnect behavior.
- Monitoring and trace creation.
- Behavior when a downstream dependency is unavailable.

## Troubleshoot channels

| Symptom | What to check |
| --- | --- |
| Preview web app controls are disabled | Confirm the endpoint supports the Responses protocol and the agent has a valid preview URL. |
| A recipient can't open the web app | Confirm organizational sign-in, granted access, tenant, and browser policy. |
| The voice-based Channels layout doesn't appear | Confirm the agent was created with Voice interaction mode and the preview is available in the project. |
| The expected Teams publishing card isn't shown | This card is intentionally missing in the current voice-based layout. Use the phone-number article for Teams Phone extensibility. |
| **Call preview agent** has no numbers | Add a number in **Channels > Phone numbers**, or verify that the telephony binding is active. |

## Related content

- [Integrate a telephony channel](voice-agent-telephony-channels.md)
- [Voice agent tracing, monitoring, and evaluation](../concepts/voice-agent-observability.md).
- [Publish an Agent Application](/azure/foundry/agents/how-to/agent-applications)
- [Publish agents to Microsoft 365 Copilot and Microsoft Teams](/azure/foundry/agents/how-to/publish-copilot)
