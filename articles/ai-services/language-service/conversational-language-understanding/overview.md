---
title: Conversational Language Understanding - Foundry Tools
titleSuffix: Foundry Tools
description: Customize an AI model to predict the intentions of utterances, and extract important information from them.
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: overview
ms.date: 12/05/2025
ms.author: lajanuar
ms.custom: language-service-clu
---
# What is conversational language understanding?

Conversational language understanding is one of the custom features offered by [Azure Language](../overview.md). It's a cloud-based API service that applies machine-learning intelligence to enable you to build natural language understanding component to be used in an end-to-end conversational application. 

Conversational language understanding (CLU) enables users to build custom natural language understanding models to predict the overall intention of an incoming utterance and extract important information from it. CLU only provides the intelligence to understand the input text for the client application and doesn't perform any actions. Developers can iteratively label utterances, train, and evaluate model performance before making it available for consumption by creating a CLU project. The quality of the labeled data greatly impacts model performance. To simplify building and customizing your model, the service offers a custom web portal that can be accessed through the [Microsoft Foundry](https://ai.azure.com/). You can easily get started with the service by following the steps in this [quickstart](quickstart.md). 

This documentation contains the following article types:

* [Quickstarts](quickstart.md) are getting-started instructions to guide you through making requests to the service.
* [Concepts](concepts/evaluation-metrics.md) provide explanations of the service functionality and features.
* [How-to guides](how-to/create-project.md) contain instructions for using the service in more specific or customized ways.


## Example usage scenarios

CLU can be used in multiple scenarios across various industries. Some examples are:

### Multi-turn conversations 🆕

Use CLU with entity slot filling to enable natural, progressive information gathering across multiple conversation turns. Instead of overwhelming users with complex forms, your application can collect required details as they emerge naturally in dialogue. This approach is ideal for scenarios like booking systems, customer service workflows, or any application where complete information needs to be gathered through conversational exchanges.

* For more information, *see* [Multi-turn conversations](concepts/multi-turn-conversations.md).

* To get started, *see* [Build a multi-turn model](how-to/build-multi-turn-model.md).

### End-to-end conversational bot

Use CLU to build and train a custom natural language understanding model tailored to a specific domain and the expected users' utterances. You can then connect this solution with any end-to-end conversational bot. This process enables the bot to handle and interpret incoming messages in real time. This integration allows the bot to determine the user's intent and extract key information from the conversation as it happens. The bot performs the desired action based on the intention and extracted information. An example would be a customized retail bot for online shopping or food ordering.

By combining it with a comprehensive conversational bot framework, the system is able to analyze text instantaneously, accurately identify user intentions, and pull out relevant details for further processing.

### Human assistant bots

A human assistant bot can enhance customer service by sorting customer inquiries and directing them to the right support engineer. Similarly, in a corporate environment, a human resources bot enables employees to ask questions in everyday language and receive relevant guidance based on their requests.

### Command and control application

When you integrate a client application with a speech to text component, users can speak a command in natural language for CLU to process, identify intent, and extract information from the text for the client application to perform an action. This use case has many applications, such as to stop, play, forward, and rewind a song or turn lights on or off.

### Enterprise chat bot

Within a large corporation, the enterprise chatbot actively handles a wide range of employee matters. Employees rely on the chatbot to address frequently asked questions, drawing on a custom question-answering knowledge base. When users interact with their calendars, the chatbot uses a calendar-specific skill powered by conversational language understanding. Employees also benefit from an interview feedback skill, which operates through CLU. The Orchestration workflow seamlessly connects these skills, ensuring each request routes directly to the appropriate service.

## Project development lifecycle

Creating a CLU project typically involves several different steps.

:::image type="content" source="media/llm-quick-deploy.png" alt-text="Chart of the LLM-powered quick deploy path." lightbox="media/llm-quick-deploy.png":::

> [!NOTE]
> In the Foundry, you create a fine-tuning task as your workspace for customizing your CLU model. Previously, a CLU fine-tuning task was referred to as a CLU project. You may see these terms used interchangeably in legacy CLU documentation.

CLU offers two paths for you to get the most out of your implementation.

Option 1 (LLM-powered quick deploy):

1. **Define your schema**: Know your data and define the actions and relevant information that needs to be recognized from user's input utterances. In this step, you create the intents and provide a detailed description on the meaning of your intents that you want to assign to user's utterances.

2. **Deploy the model**: Deploying a model with the LLM-based training config makes it available for use via the Runtime API.

3. **Predict intents and entities**: Use your custom model deployment to predict custom intents and prebuilt entities from user's utterances. 

Option 2 (Custom machine learned model)

Follow these steps to get the most out of your trained model:

1. **Define your schema**: Know your data and define the actions and relevant information that needs to be recognized from user's input utterances. In this step, you create the [intents](glossary.md#intent) that you want to assign to user's utterances, and the relevant [entities](glossary.md#entity) you want extracted.

2. **Label your data**: The quality of data labeling is a key factor in determining model performance. 

3. **Train the model**: Your model starts learning from your labeled data.

4. **View the model's performance**: View the evaluation details for your model to determine how well it performs when introduced to new data.

6. **Improve the model**: After reviewing the model's performance, you can then learn how you can improve the model.

7. **Deploy the model**: Deploying a model makes it available for use via the [Runtime API](https://aka.ms/clu-apis).

8. **Predict intents and entities**: Use your custom model to predict intents and entities from user's utterances.

## Reference documentation and code samples

As you use CLU, see the following reference documentation and samples for Azure Language:

|Development option / language  |Reference documentation |Samples  |
|---------|---------|---------|
|REST APIs (Authoring)   | [REST API documentation](/rest/api/language/analyze-conversations-authoring/operation-groups?view=rest-language-analyze-conversations-authoring-2025-11-01&preserve-view=true)        |         |
|REST APIs (Runtime)    | [REST API documentation](/rest/api/language/analyze-conversations/analyze-conversations/analyze-conversations?view=rest-language-analyze-conversations-2025-05-15-preview&tabs=HTTP&preserve-view=true)        |         |
|C# (Runtime)    | [C# documentation](/dotnet/api/overview/azure/ai.language.conversations-readme)        | [C# samples](https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/cognitivelanguage/Azure.AI.Language.Conversations/samples)        |
|Python (Runtime)| [Python documentation](/python/api/overview/azure/ai-language-conversations-readme?view=azure-python-preview&preserve-view=true)        | [Python samples](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/cognitivelanguage/azure-ai-language-conversations/samples) |

## Responsible AI 

An AI system includes the technology, the individuals who operate the system, the people who experience its effects, and the broader environment where the system functions all play a role. Read the transparency note for CLU to learn about responsible AI use and deployment in your systems. 

[!INCLUDE [Responsible AI links](../includes/overview-responsible-ai-links.md)]

## Next steps

* Use the [quickstart article](quickstart.md) to start using conversational language understanding.  

* As you go through the project development lifecycle, review the [glossary](glossary.md) to learn more about the terms used throughout the documentation for this feature. 

* Remember to view the [service limits](service-limits.md) for information such as [regional availability](service-limits.md#regional-availability).
