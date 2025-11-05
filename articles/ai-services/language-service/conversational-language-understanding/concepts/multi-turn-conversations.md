---
title: Conversational language understanding (CLU) entity slot filling in multi-turn conversations
titleSuffix: Azure AI services
description: Learn how CLU handles entity slot-filling across multi-turn conversations, enabling context-aware entity extraction and better understanding of user intent over multiple conversation exchanges.
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: concept
ms.date: 11/052025
ms.author: lajanuar
ms.custom: language-service-clu
---

# CLU entity slot filling in multi-turn conversations

Entity slot filling in Conversational Language Understanding (CLU) enables multi-turn conversations where your applications gather information naturally across multiple exchanges. Instead of overwhelming users with complex forms or lengthy questions, CLU progressively extracts and organizes the details it needs as users provide them throughout these multi-turn conversations.

This capability transforms rigid question-and-answer interactions into fluid, context-aware dialogues. Your CLU model remembers what users have already shared and intelligently asks for missing information when needed, creating conversations that feel more natural and intuitive.

## Understanding entity slot filling

Entity slot filling works by identifying the structured information your application requires and systematically collecting it from user input. Think of slots as containers for specific types of information that your application needs to complete a task. When users provide some details but not others, CLU maintains the conversation context and can prompt for the missing pieces.

The process centers around three key elements:

* **Entities** are the specific data points you need to extract.
* **Slots** are the predefined containers that hold those entities.
* **Conversational continuity** guarantees that information is preserved and accessible throughout the entire dialogue.

Instead of requiring users to provide every details at the outset, CLU enables progressive disclosure where information emerges naturally as the conversation unfolds.

## Multi-turn conversation mechanics

Multi-turn conversations in CLU maintain state across multiple exchanges, allowing users to provide information in any order they choose. The model begins by recognizing the user's intent, then extracts any available entities from their initial input. It evaluates which required information is still missing and can contextually prompt for specific details while preserving everything that has already been collected.

This approach accommodates how people naturally communicate. Users might correct previous information, add details as they remember them, or provide partial information that gets completed over several turns. The conversation remains coherent because CLU tracks the relationship between all collected entities.

## Simple example

Consider a restaurant reservation system that needs three pieces of information: party size, date, and time.

**User**: "I'd like to make a reservation for four people"
**System**: "I can help you with that! What date would you prefer?"

**User**: "How about this Friday?"
**System**: "Perfect! And what time works best for your party of four on Friday?"

**User**: "7 PM would be great"
**System**: "Excellent! I've reserved a table for four people this Friday at 7 PM."

In this exchange, CLU extracted the party size from the first input, prompted for the missing date, then prompted for the time. Each piece of information was preserved as the conversation progressed, allowing for a natural dialogue flow rather than a rigid form-filling experience.

## Benefits of entity slot filling

Entity slot filling creates more natural user experiences by allowing people to provide information as they think of it, rather than forcing them to remember all requirements upfront. Users can correct or clarify information throughout the conversation, and the system accommodates various communication styles and preferences. This reduces cognitive burden and makes interactions feel more conversational and less transactional.

Entity slot filling improves accuracy because conversation context helps disambiguate entities and intents. This approach efficiently collects only the information necessary for task completion while providing a scalable architecture that handles complex scenarios with multiple dependent entities. The system also manages incomplete or contradictory information gracefully, making applications more robust and user-friendly.

## Azure AI Foundry

[Azure AI Foundry](https://ai.azure.com/) provides a comprehensive platform for developing and deploying CLU models with entity slot filling capabilities. The platform streamlines the process of defining your entity types and slot requirements while helping you create multi-turn conversation examples for training. You can validate slot filling behavior across various scenarios and track accuracy and user satisfaction metrics to ensure your model performs well in real-world conditions.

Azure AI Foundry enables you to build and refine your CLU models iteratively, ensuring they effectively handle the complexity of multi-turn conversations in your specific domain. The platform's tools support the entire development lifecycle from initial schema design through deployment and ongoing performance monitoring. To learn how to implement entity slot filling in your applications. *see* [Build multi-turn models in Azure Foundry](../how-to/build-multi-turn-model.md).

## Related content

* [Build multi-turn model](../how-to/build-multi-turn-model.md)
* [Build a fine-tuning schema](../how-to/build-schema.md)