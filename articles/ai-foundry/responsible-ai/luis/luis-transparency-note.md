---
title: Transparency note for LUIS
titleSuffix: Foundry Tools
description: Transparency Note for Language Understanding
author: laujan
ms.author: lajanuar
manager: nitinme
ms.service: azure-ai-language
ms.topic: concept-article
ms.subservice: azure-ai-luis
ms.date: 02/08/2024
---

# Use cases for Language Understanding

[!INCLUDE [non-english-translation](../includes/non-english-translation.md)]

## What is a Transparency Note?

An AI system includes not only the technology, but also the people who use it, the people who will be affected by it, and the environment in which it's deployed. Creating a system that is fit for its intended purpose requires an understanding of how the technology works, its capabilities and limitations, and how to achieve the best performance.

Microsoft provides *Transparency Notes* to help you understand how our AI technology works. These notes includes the choices system owners can make that influence system performance and behavior, and the importance of thinking about the whole system, including the technology, the people, and the environment. You can use Transparency Notes when developing or deploying your own system, or share them with the people who will use or be affected by your system.

Transparency Notes are part of a broader effort at Microsoft to put our AI principles into practice. To find out more, see [Microsoft AI Principles](https://www.microsoft.com/ai/responsible-ai).

## Introduction to Language Understanding

[Language Understanding (LUIS)](/azure/ai-services/luis/what-is-luis) is a cloud-based conversational AI service that applies custom machine-learning intelligence to a user's natural language text. It predicts the overall meaning of an input text and pulls out specific information from it. LUIS needs to be integrated with a client application, which can be any conversational application that communicates with a user in natural language to complete a task. The most common client application is a chat bot.

Client applications use the output returned by LUIS to make a decision or perform an action about how to fulfill the user's requests. For example, a user types "I want to order a Pizza" in a chat bot that is sent to LUIS for interpretation. LUIS analyzes the input text and returns its interpretation in a form that can be processed by the chat bot, linking the input text with a preconfigured action to order the Pizza for the user. LUIS only provides the intelligence to understand the input text for the client application and doesn't perform any actions. LUIS currently [supports multiple languages](/azure/ai-services/luis/luis-language-support).

### The basics of Language Understanding

LUIS is the natural language understanding component in an end-to-end conversational application that predicts the overall intention of an incoming text and extracts important information from it. The service enables its users to [customize domain-specific LUIS applications](/azure/ai-services/luis/concepts/application-design) where they can iteratively train, test, and publish these applications. Users of the service need to provide and label training data relevant to the domain of the client application being built. The quality of the provided training data is important and needs to be similar to the expected user input. LUIS provides a [web portal](https://www.luis.ai) to simplify the customization experience for domain experts and nontechnical users.

For more information, see:

- [Create a new LUIS app in the LUIS portal](/azure/ai-services/luis/how-to/sign-in)
- [Add intents to determine user intention of utterances](/azure/ai-services/luis/how-to/intents)
- [Add entities to extract data](/azure/ai-services/luis/how-to/entities)

## Language Understanding terminology

The following terms are commonly used within LUIS:

|Term| Definition|
|:-----|:----|
|Authoring | Authoring is the phase prior to publishing a LUIS application. Everything from creating the application, creating intent and entity models, adding example utterances, labeling utterances, training, testing, and publishing the application is part of the authoring phase. All this can be done through the LUIS custom portal or through REST APIs. |
|Utterances | Utterances represent the input text from an end-user that LUIS needs to interpret. Developers add example utterances as training data to each intent and label them with the intents and entities they want extracted to train LUIS. It's important to capture different example utterances with varied terminologies when they're added for each intent. For example, "I wanted to order a large cheese pizza" would be an example utterance in an application that orders pizza. [Learn more](/azure/ai-services/luis/concepts/utterances) |
|Intents | Intents are tasks or actions that the user wants to perform. Intent models understand and classify the overall meaning and intention of an input text. Developers define a set of intents to trigger an action users want to take in the client application. For example, intents for an application that orders pizza could be, "Make Order", "Edit Order", or "Cancel Order". [Learn more](/azure/ai-services/luis/concepts/intents) |
|Entities | Entities represent a word or phrase in an utterance that's relevant to the user’s intent. Entity models extract different types of entities, as defined by developers. In an example utterance "I wanted to order a large cheese pizza", developers could define a "size" entity to extract "large" and a "type" entity to extract "cheese" from the utterance. Developers define entities to extract key data from user utterances in LUIS apps. When authoring the LUIS app, developers [label](/azure/ai-services/luis/how-to/label-utterances) aa word or multiple words they want extracted within the example utterances with a specific entity. [Learn more](/azure/ai-services/luis/concepts/entities) |
|Prebuilt entities | Prebuilt entities are pretrained models that can recognize common types of information, such as names, geographies, dates, times, numbers, and measurements. When a prebuilt entity is included in a LUIS application, its predictions are included in the published application. Prebuilt entities can't be modified. |
|Prebuilt domains| Prebuilt domains are pretrained, ready-to-use LUIS applications that contain prebuilt intent and entity models, along with labeled example utterances. LUIS offers multiple prebuilt application domains that can be added such as home automation or restaurant reservation. Prebuilt domains are fully customizable. Developers can add, edit, and delete intents, entities, or example utterances and retrain the application. [Learn more](/azure/ai-services/luis/luis-get-started-create-app) |


## Example use cases

LUIS can be used in multiple scenarios across a variety of industries. Some examples are:

* **Use in an end-to-end conversational bot.** Use LUIS to build and train a custom natural language understanding model based on a specific domain and the expected users' utterances. Integrate it with any end-to-end conversational bot so that it can process and analyze incoming text in real time to identify the intention of the text and extract important information from it. Have the bot perform the desired action based on the intention and extracted information.
* **Human assistant bots.** One example for a human assistant bot is to help staff improve customer engagements by triaging customer queries and assigning them to the appropriate support engineer. Another example would be a human resources bot in an enterprise that allows employees to communicate in natural language and receive guidance based on the query.
* **Command and control application.** Integrating a client application with a speech to text component, users can speak a command in natural language for LUIS to process, identify intent, and extract information from the text for the client application to perform an action. This use case has many applications, such as to stop, play, forward, and rewind a song or turn lights on or off.

## Considerations when choosing a use case

* **Don’t use LUIS for decisions that may have serious adverse impacts,** such as use cases that include identifying whether to accept or reject an insurance claim based on a user's description of an incident. Additionally, it's advisable to include human review of decisions that have the potential for serious impacts on individuals.
* **Avoid creating custom entities that extract unnecessary or sensitive information.** It's your responsibility to ensure that the entities being created only extract the necessary information for your end-to-end scenario. Avoid extracting sensitive user information if it isn't required for your scenario. For example, if your scenario requires extracting your user's city and country/region, create entities that extract only the city and country/region from a user's address, and don't create one that would extract their full address. To ensure that your model is inclusive, make sure you represent a variety of cities, countries/regions, and address formats within your training data (example utterances).
* **Avoid storing users' personal data.** LUIS doesn't retain end user data by default, but LUIS customers have the option to retain the data if they opt to, which should then be relayed appropriately to the end users. If you do opt to retain user data, avoid storing private user data (like name, date of birth, or other identifying information) or sending requests to LUIS that contain private user data. You can deploy a private user data detector or a profanity filter on the original text prior to sending it to the LUIS model. 
* [!INCLUDE [regulatory-considerations](../includes/regulatory-considerations.md)]

## Next steps

* [Introduction to Language Understanding](/azure/ai-services/luis/what-is-luis)
* [Characteristics and limitations for using Language Understanding](characteristics-and-limitations.md)
* [Data, privacy, and security](data-privacy-security.md)
* [Microsoft AI principles](https://www.microsoft.com/ai/responsible-ai?rtc=1&activetab=pivot1%3aprimaryr6)
* [Building responsible bots](https://www.microsoft.com/research/uploads/prod/2018/11/Bot_Guidelines_Nov_2018.pdf)
