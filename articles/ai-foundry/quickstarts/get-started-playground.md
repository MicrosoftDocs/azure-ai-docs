---
title: Get Answers in Chat Playground - Microsoft Foundry Quickstart
titleSuffix: Microsoft Foundry
description: Get answers using the chat playground in Microsoft Foundry portal. Learn how to deploy models, ask questions, and get AI responses quickly with this step-by-step tutorial.
ms.service: azure-ai-foundry
ms.custom:
  - build-2024
  - ignite-2024
  - dev-focus
ms.topic: quickstart
ms.date: 12/19/2025
ms.reviewer: zuramir
ms.author: sgilley
author: sdgilley
ai-usage: ai-assisted
# customer intent: As a developer, I want use the chat playground in Microsoft Foundry portal so I can work with generative AI.
---

# Quickstart: Get answers in the chat playground

[!INCLUDE [classic-banner](../includes/classic-banner.md)]

Learn how to use the chat playground in [Microsoft Foundry](https://ai.azure.com/?cid=learnDocs) to explore AI model capabilities interactively. This quickstart focuses on the web-based UI experience; to build applications programmatically, see [Build a custom chat app using the SDK](./get-started-code.md).

Deploy (or reuse) a chat model and send prompts to receive AI-generated responses.

In this quickstart, you learn how to:
- Configure a system message to guide model behavior.
- Send a user question and receive a response.
- Interpret model responses and recognize limitations.
- Add safety system messages to ensure responsible AI use.

For this quickstart, you can use either a [!INCLUDE [hub](../includes/hub-project-name.md)] or a [!INCLUDE [fdp](../includes/fdp-project-name.md)]. For more information about the differences between these two project types, see [Project types](../what-is-foundry.md#types-of-projects).

## Prerequisites

* [!INCLUDE [azure-subscription](../includes/azure-subscription.md)]
* The following Azure RBAC roles are required. To verify your role, see [Manage access control](../how-to/create-azure-ai-resource.md#manage-access-control).
    * **Owner** on the subscription to create a project and assign roles.
    * **Azure AI User** on the project to deploy models (assigned automatically when you create the project as Owner of the subscription).

## Deploy a model

[!INCLUDE [feature-preview](../includes/first-run-experience-classic.md)]




## Use the chat playground

Use the [Foundry](https://ai.azure.com/?cid=learnDocs) playground to interact with deployed chat models and test prompts in real time.

To get answers from your deployed model in the chat playground:

1. In the **System message** text box, provide a prompt to guide the assistant. For example, for a customer support scenario, use: "You're a helpful customer support agent. Answer questions about product features, pricing, and troubleshooting. If you don't know the answer, offer to escalate to a specialist." You can tailor the prompt for your specific use case.
1. Optionally, add a safety system message by selecting the **Add section** button, and then **Safety system messages**. Choose from the prebuilt messages, and then edit them to your needs.

1. Select **Apply changes** to save your changes. When prompted to see if you want to update the system message, select **Continue**. 
1. In the chat session pane, enter the following question: "How much do the TrailWalker hiking shoes cost?"
1. Select the right arrow icon to send.

    :::image type="content" source="../media/tutorials/chat/chat-without-data.png" alt-text="Screenshot of the first chat question without grounding data." lightbox="../media/tutorials/chat/chat-without-data.png":::

1. The assistant either replies that it doesn't know the answer or provides a generic response, such as noting price variability. This is expected because the model doesn't have access to current product data.

**Understanding the response:** The model generated text based on its training data and system message, but without grounding data (like a product catalog), it can't provide accurate domain-specific answers. This limitation is normal and expected in this scenario.

Next, add your data so the model can answer domain-specific questions. Try the enterprise chat web app tutorial.

### Troubleshooting

| Issue | Action |
|-------|--------|
| No deployed models listed | Deploy a model from the model catalog first. |
| Repeated generic answers | Refine system message or add domain data. |
| Safety message overrides tone | Adjust or remove conflicting safety sections. |
| Slow first response | Allow for cold start; subsequent prompts are faster. |

## Next step

> [!div class="nextstepaction"]
> [Build a custom chat app using the SDK](./get-started-code.md)

## Related content

- [Deploy an enterprise chat web app](../tutorials/deploy-chat-web-app.md).
- [Add evaluations to measure response quality](../how-to/evaluate-generative-ai-app.md).
- [Fine-tune a model for improved performance](../how-to/fine-tune-serverless.md).
