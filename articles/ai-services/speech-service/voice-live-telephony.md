---
title: Call Center Voice Agent Accelerator 
titleSuffix: Foundry Tools
description: Connect call centers with Microsoft Foundry voice agents and native telephony, or use the Voice Live API accelerator for application-managed integration.
manager: mcleans
author: PatrickFarley
ms.author: pafarley
ms.service: azure-speech-foundry-tools
ms.topic: how-to
ms.date: 10/08/2026
ai-usage: ai-assisted
---

# Use the Call Center Voice Agent Accelerator 

For call center solutions, use **Microsoft Foundry voice agents (preview)** with native telephony integration, especially for **Teams Phone extensibility (TPE)** and **Twilio**. Foundry manages the telephony integration for inbound and outbound calls, rather than requiring your application to implement it.

For existing Voice Live telephony solutions, including accelerator-based applications, migrate to Foundry voice agents for native telephony integration. Start by [creating a voice-based prompt agent](../../foundry/agents/quickstarts/prompt-voice-agent.md). Then follow [Integrate telephony channels with a voice agent](../../foundry/agents/how-to/voice-agent-telephony-channels.md) to configure TPE or Twilio and connect your phone number.

If you need application-managed telephony integration with the Voice Live API, use the [Call Center Voice Agent Accelerator](https://github.com/Azure-Samples/call-center-voice-agent-accelerator). This solution template helps you build real-time speech-to-speech agents for call center self-service scenarios. The following overview describes this accelerator approach, not the native Foundry telephony integration.

## Solution overview

This solution provides an end-to-end framework for creating scalable, efficient, and low-latency call center voice agent experiences.  

The Azure Voice Live API provides a single, unified interface that integrates speech recognition, generative AI, and text-to-speech functionalities. 

The Azure Communication Services Call Automation APIs provide the telephony integration. You can use either an [ACS provided number](/azure/communication-services/quickstarts/telephony/get-trial-phone-number) or direct routing using Session Initiation Protocol (SIP) with your existing PSTN carrier or third-party PBX (see [Use direct routing to connect existing telephony service](/azure/communication-services/concepts/telephony/direct-routing-provisioning)). 

Alternatively, telephony integration is supported through third-party providers' audio connectors, including:
- [**Twilio Media Streams**](https://www.twilio.com/docs/voice/media-streams)
- [**Infobip Calls**](https://www.infobip.com/docs/voice-and-video/calls)
- [**Genesys AudioHook**](https://developer.genesys.cloud/devapps/audiohook/)
- [**Sinch Voice**](https://developers.sinch.com/docs/voice)
- [**Bandwidth Voice**](https://dev.bandwidth.com/docs/voice/)
- [**Vonage Voice**](https://developer.vonage.com/voice)


:::image type="content" source="media/voice-live/telephony.png" alt-text="Diagram of the call center telephony setup." lightbox="media/voice-live/telephony.png":::


## Related content 

- Learn more about [Voice Live API](/azure/ai-services/speech-service/voice-live).
