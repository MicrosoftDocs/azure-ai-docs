---
title: Call Center Voice Agent Accelerator 
titleSuffix: Foundry Tools
description: Learn how to use the Voice Live API with telephony systems.
manager: nitinme
author: PatrickFarley
ms.author: pafarley
ms.service: azure-ai-speech
ms.topic: how-to
ms.date: 09/26/2025
---

# Use the Call Center Voice Agent Accelerator 

The Call Center Voice Agent Accelerator is a solution template designed to help developers build real-time speech-to-speech voice agents that deliver personalized self-service experiences for call centers. It lets you develop conversational interactions that feel fast and natural, and it integrates seamlessly with telephony systems, making it ideal for modern contact centers looking to enhance customer interactions. 

This accelerator combines the Azure Voice Live API and Azure Communication Services (ACS) to enable developers to start locally and deploy to an Azure Web App when ready. It doesn't require a PSTN number to get started, which further simplifies the initial setup process. 

You can find the solution template on GitHub: [Call Center Voice Agent Accelerator with Azure Voice Live API](https://github.com/Azure-Samples/call-center-voice-agent-accelerator). 

## Solution overview

This solution provides an end-to-end framework for creating scalable, efficient, and low-latency call center voice agent experiences using the Azure Voice Live API and Azure Communication Services APIs.  

The Azure Voice Live API provides a single, unified interface that integrates speech recognition, generative AI, and text-to-speech functionalities. 

Additionally, the Azure Communication Services Call Automation APIs provide the telephony integration. You can use either an [ACS provided number](/azure/communication-services/quickstarts/telephony/get-trial-phone-number) or direct routing using Session Initiation Protocol (SIP) with your existing PSTN carrier or third-party PBX (see [Use direct routing to connect existing telephony service](/azure/communication-services/concepts/telephony/direct-routing-provisioning)). 

:::image type="content" source="media/voice-live/telephony.png" alt-text="Diagram of the call center telephony setup.":::


## Related content 

- Learn more about [Voice Live API](/azure/ai-services/speech-service/voice-live).
- Learn more about [Azure Communication Services](/azure/communication-services/overview). 