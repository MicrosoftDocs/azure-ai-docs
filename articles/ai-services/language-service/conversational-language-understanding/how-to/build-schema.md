---
title: How to build a Conversational Language Understanding project schema
titleSuffix: Azure AI services
description: Use this article to start building a Conversational Language Understanding project schema
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: how-to
ms.date: 05/20/2025
ms.author: lajanuar
ms.custom: language-service-clu
---

# How to build your fine-tuning schema

In conversational language understanding projects, the *schema* is defined as the combination of intents and entities within your project. Schema design is a crucial part of your project's success. When creating a schema, think about which intents and entities should be included in your project.

## Guidelines and recommendations

Consider the following guidelines when picking intents for your project:

  1. Create distinct, separable intents. An intent is best described as action the user wants to perform. Think of the project you're building and identify all the different actions your users may take when interacting with your project. Sending, calling, and canceling are all actions that are best represented as different intents. "Canceling an order" and "canceling an appointment" are similar, with the distinction being *what* they're canceling. Those two actions should be represented under the same intent, *Cancel*.

  1. Create entities to extract relevant pieces of information within your text. The entities should be used to capture the relevant information needed to fulfill your user's action. For example, *order* or *appointment* could be different things a user is trying to cancel, and you should create an entity to capture that piece of information.

You can *"send"* a *message*, *"send"* an *email*, or *"send"* a package. Creating an intent to capture each of those requirements won't scale over time, and you should use entities to identify *what* the user was sending. The combination of intents and entities should determine your conversation flow.

For example, consider a company where the bot developers identified the three most common actions their users take when using a calendar:

* Setup new meetings
* Respond to meeting requests
* Cancel meetings

They might create an intent to represent each of these actions. They might also include entities to help complete these actions, such as:

* Meeting attendants
* Date
* Meeting durations

## Add intents

To build a project schema within [AI Foundry](https://ai.azure.com/?cid=learnDocs):

1. Select **Define schema** from the left side menu.

1. From the top pivots, you can change the view to be **Intents** or **Entities**.

1. To create an intent, select **+ Add intent**. You're prompted to type in names and descriptions for as many intents as you'd like to create. Descriptions are only required for using Quick Deploy to help Azure OpenAI better understand the context of your intents.

1. Repeat the steps to develop intents that encompass all the actions the user is likely to perform while interacting with the project.



    :::image type="content" source="../media/build-schema-page.png" alt-text="A screenshot showing the schema creation page for conversation projects in Language Studio." lightbox="../media/build-schema-page.png":::

1. If you'd like to continue with [data labeling](tag-utterances.md) and advanced training a custom `CLU` model, you can select **Manage data** from the left side menu to add examples for intents and label them with entities, if desired.

## Add entities

1. Move to **Entities** pivot from the top of the page.

1. To add an entity, select **+ Add entity** from the top. You're prompted to type in a name to create the entity.

1. After creating an entity, you can select the entity name to change the **Entity components** type. Multiple components—learned, list, regex, or prebuilt—define every entity. A learned component is added to all your entities once you label them in your utterances.

   :::image type="content" source="../media/entity-details.png" alt-text="A screenshot showing the entity details page for conversation projects in Language Studio." lightbox="../media/entity-details.png":::

1. You can also add a [list](../concepts/entity-components.md#list-component), [regex](../concepts/entity-components.md#regex-component), or [prebuilt](../concepts/entity-components.md#prebuilt-component) component to each entity.

### Add prebuilt component

To add a **prebuilt** component, select the prebuilt type from the drop-down menu in the Entity options section.

   <!--:::image type="content" source="../media/add-prebuilt-component.png" alt-text="A screenshot showing a prebuilt-component in Language Studio." lightbox="../media/add-prebuilt-component.png":::-->

### Add list component

To add a **list** component, select **Add list**. You can add multiple lists to each entity:

1. Create a new list, in the *List key* text box, enter the normalized value that is returned when any of the synonyms values is extracted.

1. Start typing in your synonyms and hit enter after each one. We recommend having a synonym list in multiple languages.

   <!--:::image type="content" source="../media/add-list-component.png" alt-text="A screenshot showing a list component in Language Studio." lightbox="../media/add-list-component.png":::-->

### Add regex component

To add a regex component, select Add expression. Name the regex key and type a regular expression that matches the entity to be extracted.

### Define entity options

Change to the **Entity options** pivot in the entity details page. When multiple components are defined for an entity, their predictions may overlap. When an overlap occurs, each entity's final prediction is determined based on the [entity option](../concepts/entity-components.md#entity-options) you select in this step. Select the one that you want to apply to this entity and select the **Save** button.

   <!--:::image type="content" source="../media/entity-options.png" alt-text="A screenshot showing an entity option in Language Studio." lightbox="../media/entity-options.png":::-->


After you create your entities, you can come back and edit them. You can **edit entity components** or **delete** them by selecting this option from the top menu.

## Next Steps

* [Add utterances and label your data](tag-utterances.md)
