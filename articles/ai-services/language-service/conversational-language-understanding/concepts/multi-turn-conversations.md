---
title: Conversational language understanding (CLU) entity slot filling in multi-turn conversations
titleSuffix: Foundry Tools
description: Learn how CLU handles entity slot-filling across multi-turn conversations.
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: concept-article
ms.date: 11/05/2025
ms.author: lajanuar
ms.custom: language-service-clu
---

# CLU multi-turn conversations

Entity slot filling in Conversational Language Understanding (CLU) enables your applications to facilitate seamless multi-turn conversations across multiple exchanges. Instead of overwhelming users with complex forms or lengthy questions, CLU progressively extracts and organizes the details it needs as users provide them throughout these multi-turn conversations.

This capability transforms rigid question-and-answer interactions into fluid dialogues. Your CLU model is prompted to ask for missing information when needed, creating conversations that feel more natural and intuitive.

## Understand entity slot filling

 Entity slot filling works by identifying the structured information your application requires and systematically collecting it from user input. Think of slots as containers for specific types of information that your application needs to complete a task. When users provide some details but not others, your CLU model is prompted for the missing pieces.

The process centers around three key elements:

* **Entities** are the specific data points you need to extract.
* **Slots** are the predefined containers that hold those entities.
* **Conversational continuity** guarantees that information is preserved and accessible throughout the entire dialogue.

Instead of requiring users to provide every detail at the outset, CLU enables progressive disclosure where information emerges naturally as the conversation unfolds.

## Multi-turn conversation mechanics

With CLU multi-turn conversations, you enable users to share information in whichever sequence they prefer. The model begins by recognizing the user's intent, then extracts any available entities from their initial input.

This approach accommodates how people naturally communicate. Users might correct previous information, add details as they remember them, or provide partial information that gets completed over several turns. The conversation remains coherent because CLU tracks the relationship between all collected entities.

## Usage scenario

Consider a restaurant reservation system that needs three pieces of information: party size, date, and time.

**User**: "I'd like to make a reservation for four people"
**System**: "I can help you with scheduling that reservation! What date would you prefer?"

**User**: "How about this Friday?"
**System**: "Perfect! And what time works best for your party of four on Friday?"

**User**: "7 PM would be great"
**System**: "Excellent! I reserved a table for four people this Friday at 7 PM."

In this exchange, CLU model extracts the party size, date, and time from the user input. Each piece of information is added, allowing for a natural dialogue flow rather than a rigid form-filling experience.

## Benefits of entity slot filling

Entity slot filling creates more natural user experiences by allowing people to provide information as they think of it, rather than forcing them to remember all requirements upfront. Users can correct or clarify information throughout the conversation, and the system accommodates various communication styles and preferences. This process reduces cognitive burden and makes interactions feel more conversational and less transactional.

Entity slot filling improves accuracy because conversation context helps disambiguate entities and intents. This approach efficiently collects only the information necessary for task completion while providing a scalable architecture that handles complex scenarios with multiple dependent entities. The system also manages incomplete or contradictory information gracefully, making applications more robust and user-friendly.

## Microsoft Foundry

[Foundry](https://ai.azure.com/) provides a comprehensive platform for developing and deploying CLU models with entity slot filling capabilities. The platform streamlines the process of defining your entity types and slot requirements while helping you create multi-turn conversation examples for training. You validate slot filling behavior across various scenarios and track accuracy and user satisfaction metrics to ensure your model performs well in real-world conditions.

Foundry enables you to build and refine your CLU models iteratively, ensuring they effectively handle the complexity of multi-turn conversations in your specific domain. The platform's tools support the entire development lifecycle from initial schema design through deployment and ongoing performance monitoring. 

To get started implementing entity slot filling in your applications, see [Build multi-turn models in Foundry](../how-to/build-multi-turn-model.md).

## Related content

* [Build multi-turn model](../how-to/build-multi-turn-model.md)
* [Build a fine-tuning schema](../how-to/build-schema.md)
