---
manager: nitinme
author: eric-urban
ms.author: eur
ms.service: azure-ai-openai
ms.topic: include
ms.date: 1/21/2025
---

To deploy the `gpt-4o-mini-realtime-preview` model in the Azure AI Foundry portal:
1. Go to the [Azure OpenAI Service page](https://ai.azure.com/resource/overview) in Azure AI Foundry portal. Make sure you're signed in with the Azure subscription that has your Azure OpenAI Service resource (with or without model deployments.)
1. Select the **Real-time audio** playground from under **Playgrounds** in the left pane.
1. Select **+ Create new deployment** > **From base models** to open the deployment window. 
1. Search for and select the `gpt-4o-mini-realtime-preview` model and then select **Deploy to selected resource**.
1. In the deployment wizard, select the `2024-12-17` model version.
1. Follow the wizard to finish deploying the model.

Now that you have a deployment of the `gpt-4o-mini-realtime-preview` model, you can interact with it in real time in the Azure AI Foundry portal **Real-time audio** playground or Realtime API.
