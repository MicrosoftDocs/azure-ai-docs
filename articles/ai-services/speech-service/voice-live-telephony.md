---
title: Call Center Voice Agent Accelerator 
titleSuffix: Azure AI services
description: Learn how to use the Voice live API with telephony systems.
manager: nitinme
author: PatrickFarley
ms.author: pafarley
ms.service: azure-ai-speech
ms.topic: how-to
ms.date: 10/23/2025
---

# Call Center Voice Agent Accelerator 

The Call Center Voice Agent Accelerator is a solution template that helps developers build real-time speech-to-speech voice agents. These agents deliver personalized self-service experiences for call centers. With this solution, you can develop conversational interactions that feel fast and natural. It **integrates seamlessly with telephony systems**, making it perfect for modern contact centers that want to enhance customer interactions.

This accelerator combines the Voice live API and Azure Communication Services (ACS). You can start development locally and deploy to an Azure Web App when you're ready. You don't need a PSTN number to get started, which simplifies the initial setup process.

You can find the solution template on [GitHub](https://github.com/Azure-Samples/call-center-voice-agent-accelerator).

## Solution description

This solution provides an end-to-end framework for creating scalable, efficient, and low-latency call center voice agent experiences. It uses the Voice live API and Azure Communication Services APIs. 

The Voice live API provides a single, unified interface that integrates speech recognition, generative AI, and text-to-speech functionalities.

The Azure Communication Services Call Automation APIs provide the telephony integration. You can use either an [ACS-provided number](/azure/communication-services/quickstarts/telephony/get-trial-phone-number) or direct routing with Session Initiation Protocol (SIP) using your existing PSTN carrier or third-party PBX. For more information, see [Use direct routing to connect existing telephony service](/azure/communication-services/concepts/telephony/direct-routing-provisioning). 