---
manager: nitinme
author: PatrickFarley
ms.author: pafarley
reviewer: patrickfarley
ms.reviewer: pafarley
ms.service: azure-ai-speech
ms.topic: include
ms.date: 2/20/2026
---

In this article, you learn how to use Voice Live with [Microsoft Foundry Agent Service](/azure/ai-foundry/agents/overview) using the VoiceLive SDK for python. This article extends the [Quickstart: Create a Voice Agent with Foundry Agent Service and Voice Live](../../../voice-live-agents-quickstart.md) with more details on the features and integration options.

[!INCLUDE [Header](../../common/voice-live-python.md)] 

[!INCLUDE [Introduction](intro.md)]

## Prerequisites

> [!NOTE]
> This document refers to the [Microsoft Foundry (new)](../../../../../ai-foundry/what-is-foundry.md#microsoft-foundry-portals) portal and the latest Foundry Agent Service version.

- An Azure subscription. [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- <a href="https://www.python.org/" target="_blank">Python 3.10 or later version</a>. If you don't have a suitable version of Python installed, you can follow the instructions in the [VS Code Python Tutorial](https://code.visualstudio.com/docs/python/python-tutorial#_install-a-python-interpreter) for the easiest way of installing Python on your operating system.
- The required language runtimes, global tools, and Visual Studio Code extensions as described in [Prepare your development environment](../../../../../ai-foundry/how-to/develop/install-cli-sdk.md).
- A [Microsoft Foundry resource](../../../../multi-service-resource.md) created in one of the supported regions. For more information about region availability, see the [Voice Live overview documentation](../../../voice-live.md).
- A model deployed in Microsoft Foundry. If you don't have a model, first complete [Quickstart: Set up Microsoft Foundry resources](../../../../../ai-foundry/default/tutorials/quickstart-create-foundry-resources.md).
<!-- - A Microsoft Foundry agent created in the [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs). For more information about creating an agent, see the [Create an agent quickstart](../../../../../ai-foundry/quickstarts/get-started-code.md). -->
- Assign the `Azure AI User` role to your user account. You can assign roles in the Azure portal under **Access control (IAM)** > **Add role assignment**.

## Prepare the environment and create the agent

Please complete the [Quickstart: Create a Voice Agent with Foundry Agent Service and Voice Live](../../../voice-live-agents-quickstart.md) to prepare the environment and setup the agent with Voice Live settings and run the first test with the Voice Live service to talk to your agent.

## Connecting to a specific agent version

Useful when: controlling production vs. dev/staging versions of agent in CI/CD lifecycle management

xxx

## Connecting to an agent on a different Foundry resource

Agent is deployed on a different Foundry resource than the one used for Voice Live audio processing.

Useful when: Separating environments, using features of Voice Live or Foundry agent service not supported in all regions, ...

xxx

## Improving tool calling and latency wait times

Voice Live provides a feature called `interim_response` to bridge wait times when tool calling is required or a high latency is experienced to generate an agent response.

The feature supports the following two modes:
- LlmInterimResponseConfig: LLM-generated interim response - best for dynamic and adaptive starts
- InterimResponseTrigger: Pre-generated interim response - best for deterministic or branded messaging

The `voice-live-agents-quickstart.py` created with the quickstart shows the required code additions to configure this feature as follows:

:::code language="python" source="..\..\code-samples\voice-live-agents\voice-live-with-agent-v2.py" range="17-31,325-348" highlight="9-10,19-25,32":::

## Reconnect to a previous agent conversation

xxx
