---
title: Transparency Note for CLU
titleSuffix: Foundry Tools
description: Transparency Note for conversational language understanding
author: laujan
ms.author: lajanuar
manager: nitinme
ms.service: azure-ai-language
ms.topic: concept-article
ms.date: 09/15/2021
---

# Use cases for conversational language understanding

[!INCLUDE [non-english-translation](../includes/non-english-translation.md)]

## What is a Transparency Note?

An AI system includes not only the technology, but also the people who will use it, the people who will be affected by it, and the environment in which it is deployed. Creating a system that is fit for its intended purpose requires an understanding of how the technology works, its capabilities and limitations, and how to achieve the best performance. Microsoft’s Transparency Notes are intended to help you understand how our AI technology works, the choices system owners can make that influence system performance and behavior, and the importance of thinking about the whole system, including the technology, the people, and the environment. You can use Transparency Notes when developing or deploying your own system, or share them with the people who will use or be affected by your system.  

Microsoft’s Transparency Notes are part of a broader effort at Microsoft to put our AI Principles into practice. To find out more, [visit Microsoft AI principles](https://www.microsoft.com/ai/responsible-ai).

## Introduction to conversational language understanding

[Conversational language understanding (CLU)](/azure/ai-services/language-service/conversational-language-understanding/overview) is a cloud-based API feature that applies custom machine-learning on top of Microsoft Turing technologies to a user's natural language text. It predicts the overall meaning of an input text and pulls out specific information from it. CLU needs to be integrated with a client application, which can be any conversational application that communicates with a user in natural language to complete a task. The most common client application is a chat bot.

Client applications use the output returned by CLU to make a decision or perform an action to fulfill the user's requests. For example, a user enters "I want to order a pizza" in a chat bot, which is sent to CLU for interpretation. CLU analyzes the input text and returns its interpretation in a form that can be processed by the chat bot. CLU links the input text with a preconfigured action to order the pizza for the user. CLU only provides the intelligence to understand the input text for the client application and doesn't perform any actions. CLU is not only supported in multiple languages, but also it supports multi-lingual projects. [Learn more about multi-linguality](/azure/ai-services/language-service/conversational-language-understanding/language-support).

### The basics of conversational language understanding

Conversational language understanding (CLU) is offered as part of the custom features within [Azure Language in Foundry Tools](/azure/ai-services/language-service/overview). This feature is a natural language understanding component in an end-to-end conversational application that predicts the overall intention of an incoming text and extracts important information from it. By creating a CLU project, developers can iteratively tag data, train, evaluate, and improve model performance before they make it available for consumption.

Users of the service need to provide and label training data relevant to the domain of the client application being built. The quality of the provided training data is important and needs to be similar to the expected user input. Users may also connect different custom capabilities together including other CLU projects, [Custom question answering knowledge bases](/azure/ai-services/language-service/question-answering/overview), and [LUIS applications](/azure/ai-services/luis/what-is-luis) using the [Orchestration workflow feature](/azure/ai-services/language-service/orchestration-workflow/overview) within CLU. The Language provides a web portal, [Language Studio](https://language.cognitive.azure.com), to simplify the customization experience for domain experts and nontechnical users. Get started with the feature by following the steps in this [quickstart](/azure/ai-services/language-service/conversational-language-understanding/quickstart?pivots=language-studio).

For more information, see:

- [Create a new CLU project](/azure/ai-services/language-service/conversational-language-understanding/how-to/create-project)
- [Build your project's schema to determine user intentions and extract data](/azure/ai-services/language-service/conversational-language-understanding/how-to/build-schema)
- [Connect multiple features in an Orchestration workflow project](/azure/ai-services/language-service/conversational-language-understanding/how-to/create-project#create-an-orchestration-workflow-project)

## Conversational language understanding terminology

The following terms are commonly used within CLU.

|Term| Definition|
|:-----|:----|
|Project| A project is a work area for building your custom ML models based on your data. Within a project, you can tag data, build models, evaluate and improve them where necessary, and eventually deploy a model to be ready for consumption. |
|Utterances | Utterances represent the input text from a user that CLU needs to interpret. Developers add example utterances as training data and tag them with the intents and entities to train the model. For example, "I want to order a large cheese pizza" would be an example utterance in a model that orders pizza. |
|Intents | Intents are tasks or actions that the user wants to perform. Intent models understand and classify the overall meaning and intention of an input text. Developers define a set of intents to trigger an action users want to take in the client application. For example, intents in a model that orders pizza could be "Make Order," "Edit Order," or "Cancel Order." [Learn more](/azure/ai-services/language-service/conversational-language-understanding/how-to/build-schema) |
|Entities | Entities represent a word or phrase in an utterance that's relevant to the user’s intent. Entity models extract different types of entities, as defined by developers. In the example utterance "I want to order a large cheese pizza," developers could define a "size" entity to extract "large" and a "type" entity to extract "cheese" from the utterance. Developers define entities to extract key data from user utterances in CLU models. When developers create a CLU model, they tag a word or multiple words they want extracted within the example utterances with a specific entity. [Learn more](/azure/ai-services/language-service/conversational-language-understanding/how-to/build-schema) |


## Example use cases

CLU can be used in multiple scenarios across a variety of industries. Some examples are:

* **End-to-end conversational bot.** Use CLU to build and train a custom natural language understanding model based on a specific domain and the expected users' utterances. Integrate it with any end-to-end conversational bot so that it can process and analyze incoming text in real time to identify the intention of the text and extract important information from it. Have the bot perform the desired action based on the intention and extracted information. An example would be a customized retail bot for online shopping or food ordering.
* **Human assistant bots.** One example of a human assistant bot is to help staff improve customer engagements by triaging customer queries and assigning them to the appropriate support engineer. Another example would be a human resources bot in an enterprise that allows employees to communicate in natural language and receive guidance based on the query.
* **Command and control application.** When you integrate a client application with a speech to text component, users can speak a command in natural language for CLU to process, identify intent, and extract information from the text for the client application to perform an action. This use case has many applications, such as to stop, play, forward, and rewind a song or turn lights on or off.
* **Enterprise chat bot.** In a large corporation, an enterprise chat bot may handle a variety of employee affairs. It may be able to handle frequently asked questions served by a custom question answering knowledge base, a calendar specific skill served by conversational language understanding, and an interview feedback skill served by LUIS. Use Orchestration workflow to connect all these skills together and appropriately route the incoming requests to the correct service.


## Consideration when you choose a use case

* **Avoid using CLU for decisions that might have serious adverse impacts.** For example, suggesting medications or diagnoses, as replacing a doctor's advice may have serious adverse impacts.
* **Avoid creating custom entities that extract unnecessary or sensitive information.** It's your responsibility to ensure that the entities being created only extract the necessary information for your end-to-end scenario. Avoid extracting sensitive user information if it isn't required for your scenario. For example, if your scenario requires extracting your user's city and country/region, create entities that extract only the city and country/region from a user's address. Don't create one that extracts their full address. To ensure that your model is inclusive, make sure you represent a variety of cities, countries/regions, and address formats within your training data (example utterances).
* [!INCLUDE [regulatory-considerations](../includes/regulatory-considerations.md)]

## Next steps

* [Introduction to conversational language understanding](/azure/ai-services/language-service/conversational-language-understanding/overview)
* [Characteristics and limitations for using Language Understanding](clu-characteristics-and-limitations.md)

* [Data, privacy, and security](clu-data-privacy-security.md)

* [Microsoft AI principles](https://www.microsoft.com/ai/responsible-ai?rtc=1&activetab=pivot1%3aprimaryr6)
* [Building responsible bots](https://www.microsoft.com/research/uploads/prod/2018/11/Bot_Guidelines_Nov_2018.pdf)
