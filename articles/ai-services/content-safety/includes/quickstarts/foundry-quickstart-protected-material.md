---
title: "Quickstart: Use protected material detection"
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-content-safety
ms.custom:
ms.topic: include
ms.date: 04/10/2025
ms.author: pafarley
ai-usage: ai-assisted
---


## Prerequisites 

- An Azure account. If you don't have one, you can [create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- A Content Safety resource in a supported region. To create one, see <https://aka.ms/acs-create>.
- An Azure AI Foundry project or hub.


## Setup

Follow these steps to use the Content Safety **try it out** page: 

1. Go to [Azure AI Foundry](https://ai.azure.com/?cid=learnDocs) and navigate to your project/hub. Then select the **Guardrails + controls** tab on the left nav and select the **Try it out** tab.
1. On the **Try it out** page, you can experiment with various Guardrails & controls features such as text and image content, using adjustable thresholds to filter for inappropriate or harmful content.

> [!NOTE]
> Labels and navigation might vary across portal updates. If you don't see **Guardrails + controls**, look for the Content Safety **Try it out** experience in your project.

:::image type="content" source="/azure/ai-foundry/media/content-safety/try-it-out.png" alt-text="Screenshot of the try it out page for Guardrails & controls.":::


## Use protected material detection

This feature scans AI-generated outputs for known protected text or protected code content.

1. Select **Protected material detection for text** to scan text, or select **Protected material detection for code** to scan code.
1. Paste text or code for testing. For best results, test LLM completions rather than user prompts.
1. Select **Run test**. 
    The service returns the protected content result.

For more information, see the [Protected material conceptual guide](/azure/ai-services/content-safety/concepts/protected-material).