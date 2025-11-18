---
title: Build a Conversational Language Understanding Project Schema
titleSuffix: Foundry Tools
description: Use this article to start building a conversational language understanding project schema.
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: how-to
ms.date: 11/18/2025
ms.author: lajanuar
ms.custom: language-service-clu
---
# Build your fine-tuning schema

In conversational language understanding projects, the *schema* is defined as the combination of intents and entities within your project. Schema design is a crucial part of your project's success. When you create a schema, think about which intents and entities should be included in your project.

## Guidelines and recommendations

Consider the following guidelines when you choose intents for your project:

  - **Create distinct, separable intents.** An intent is best described as action that the user wants to perform. Think of the project you're building and identify all the different actions that your users might take when they interact with your project. Sending, calling, and canceling are all actions that are best represented as different intents. "Canceling an order" and "canceling an appointment" are similar, with the distinction being *what* they're canceling. Those two actions should be represented under the same intent, *cancel*.
  - **Create entities to extract relevant pieces of information within your text.** The entities should be used to capture the relevant information that's needed to fulfill your user's action. For example, *order* or *appointment* could be different things that a user is trying to cancel, and you should create an entity to capture that piece of information.

You can "send a message," "send an email," or "send a package." Creating an intent to capture each of those requirements won't scale over time, and you should use entities to identify *what* the user was sending. The combination of intents and entities should determine your conversation flow.

For example, consider a company where the bot developers identified the three most common actions that their users take when they use a calendar:

* Set up new meetings.
* Respond to meeting requests.
* Cancel meetings.

They might create an intent to represent each of these actions. They might also include entities to help complete these actions, such as:

* Meeting attendants
* Date
* Meeting durations

## Add intents

To build a project schema within [Foundry](https://ai.azure.com/?cid=learnDocs):

1. On the left pane, select **Define schema**.

1. Select the **Intents** or **Entities** tabs.

1. To create an intent, select **+ Add intent**. You're prompted to enter names and descriptions for as many intents as you want to create. Descriptions are required only for using the **Quick Deploy** option to help Azure OpenAI better understand the context of your intents.

1. Repeat the steps to develop intents that encompass all the actions that the user is likely to perform while interacting with the project.

    :::image type="content" source="../media/build-schema-page.png" alt-text="A screenshot that shows the schema creation page for conversation projects in Language Studio." lightbox="../media/build-schema-page.png":::

1. If you want to continue with [data labeling](tag-utterances.md) and advanced training a custom `CLU` model, on the left pane, select **Manage data** to add examples for intents and label them with entities, if desired.

## Add entities

1. Select the **Entities** tab.

1. To add an entity, select **+ Add entity**. You're prompted to enter a name to create the entity.

1. After you create an entity, you can select the entity name to change the **Entity components** type. Multiple components like learned, list, regex, or prebuilt are used to define every entity. A learned component is added to all your entities after you label them in your utterances.

   :::image type="content" source="../media/entity-details.png" alt-text="A screenshot that shows the Entity components page for conversation projects in Language Studio." lightbox="../media/entity-details.png":::

1. You can also add a [list](../concepts/entity-components.md#list-component), [regex](../concepts/entity-components.md#regex-component), or [prebuilt](../concepts/entity-components.md#prebuilt-component) component to each entity.

### Add a prebuilt component

To add a prebuilt component, select the prebuilt type from the dropdown menu in the **Entity options** section.

   <!--:::image type="content" source="../media/add-prebuilt-component.png" alt-text="A screenshot that shows a prebuilt component in Language Studio." lightbox="../media/add-prebuilt-component.png":::-->

### Add a list component

To add a list component, select **Add list**. You can add multiple lists to each entity:

1. Create a new list, and in the **List key** text box, enter the normalized value that was returned when any of the synonyms values were extracted.

1. Enter your synonyms and select Enter after each one. We recommend having a synonym list in multiple languages.

   <!--:::image type="content" source="../media/add-list-component.png" alt-text="A screenshot that shows a list component in Language Studio." lightbox="../media/add-list-component.png":::-->

### Add a regex component

To add a regex component, select **Add expression**. Name the regex key, and enter a regular expression that matches the entity to be extracted.

### Define entity options

Select the **Entity Options** tab on the entity details page. When multiple components are defined for an entity, their predictions might overlap. When an overlap occurs, each entity's final prediction is determined based on the [entity option](../concepts/entity-components.md#entity-options) that you select in this step. Select the option that you want to apply to this entity, and then select **Save**.

   <!--:::image type="content" source="../media/entity-options.png" alt-text="A screenshot that shows an entity option in Language Studio." lightbox="../media/entity-options.png":::-->

After you create your entities, you can come back and edit them. You can edit entity components or delete them by selecting **Edit** or **Delete**.

## Related content

* [Add utterances and label your data](tag-utterances.md)
