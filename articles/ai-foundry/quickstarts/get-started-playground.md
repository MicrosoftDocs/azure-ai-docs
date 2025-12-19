---
title: Get Answers in Chat Playground - Microsoft Foundry Quickstart
titleSuffix: Microsoft Foundry
description: Get answers using the chat playground in Microsoft Foundry portal. Learn how to deploy models, ask questions, and get AI responses quickly with this step-by-step tutorial.
ms.service: azure-ai-foundry
ms.custom:
  - build-2024
  - ignite-2024
ms.topic: quickstart
ms.date: 08/25/2025
ms.reviewer: zuramir
ms.author: sgilley
author: sdgilley
ai-usage: ai-assisted
# customer intent: As a developer, I want use the chat playground in Microsoft Foundry portal so I can work with generative AI.
---

# Quickstart: Get answers in the chat playground

[!INCLUDE [classic-banner](../includes/classic-banner.md)]

Learn how to get answers by using the chat playground in [Microsoft Foundry](https://ai.azure.com/?cid=learnDocs). Deploy (or reuse) a chat model and send prompts to receive AI-generated responses.

In this quickstart, you learn how to:
- Configure a system message.
- Send a user question.
- Interpret the model response.
- Add safety system messages.

For this quickstart, you can use either a [!INCLUDE [hub](../includes/hub-project-name.md)] or a [!INCLUDE [fdp](../includes/fdp-project-name.md)]. For more information about the differences between these two project types, see [Project types](../what-is-azure-ai-foundry.md#types-of-projects).


[!INCLUDE [azure-subscription](../includes/azure-subscription.md)]

[!INCLUDE [feature-preview](../includes/first-run-experience-classic.md)]

## Get answers in the playground

Use the [Foundry](https://ai.azure.com/?cid=learnDocs) playground to get answers from AI models. In this quickstart, you learn how to ask questions and get responses from deployed chat models.

To get answers from your deployed model in the chat playground:

1. In the **System message** text box, provide this prompt to guide the assistant: "You're an AI assistant that helps people find information." You can tailor the prompt for your scenario.
1. Optionally, add a safety system message by selecting the **Add section** button, and then **Safety system messages**. Choose from the prebuilt messages, and then edit them to your needs.

1. Select **Apply changes** to save your changes. When prompted to see if you want to update the system message, select **Continue**. 
1. In the chat session pane, enter the following question: "How much do the TrailWalker hiking shoes cost?"
1. Select the right arrow icon to send.

    :::image type="content" source="../media/tutorials/chat/chat-without-data.png" alt-text="Screenshot of the first chat question without grounding data." lightbox="../media/tutorials/chat/chat-without-data.png":::

1. The assistant either replies that it doesn't know the answer or provides a generic response, such as noting price variability. The model doesn't have access to current product data yet.

Next, add your data so the model can answer domain-specific questions. Try the enterprise chat web app tutorial.

### Troubleshooting

| Issue | Action |
|-------|--------|
| No deployed models listed | Deploy a model from the model catalog first. |
| Repeated generic answers | Refine system message or add domain data. |
| Safety message overrides tone | Adjust or remove conflicting safety sections. |
| Slow first response | Allow for cold start; subsequent prompts are faster. |

## Next steps

- Build a custom chat app by using the SDK.
- Add evaluations to measure response quality.
- Fine-tune a model for improved intent handling.

## Related content

- [Build a custom chat app in Python using the Microsoft Foundry SDK](./get-started-code.md).
- [Deploy an enterprise chat web app](../tutorials/deploy-chat-web-app.md).
