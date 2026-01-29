---
title: Guidance for integration and responsible use with conversational language understanding
titleSuffix: Foundry Tools
description: Guidance for how to deploy conversational language understanding responsibly, based on the knowledge and understanding from the team that created this product.
author: laujan
ms.author: lajanuar
manager: nitinme
ms.service: azure-ai-language
ms.topic: best-practice
ms.date: 09/15/2021
---

# Guidance for integration and responsible use with conversational language understanding

[!INCLUDE [non-english-translation](../includes/non-english-translation.md)]

Microsoft works to help customers responsibly develop and deploy solutions by using conversational language understanding (CLU). Our principled approach upholds personal agency and dignity by considering the AI system's:

- Fairness, reliability, and safety.
- Privacy and security.
- Inclusiveness.
- Transparency.
- Human accountability.

These considerations reflect our commitment to developing responsible AI.

## General guidelines for integration and responsible use principles

When you get ready to integrate and responsibly use AI-powered products or features, the following activities help to set you up for success:

* **Understand what it can do.** Fully assess the potential of any AI system to understand its capabilities and limitations. Understand how it will perform in your particular scenario and context by thoroughly testing it with real-life conditions and data.
* **Respect an individual's right to privacy.** Only collect data and information from individuals for lawful and justifiable purposes. Only use data and information that you have consent to use for this purpose.
* **Obtain legal review.** Obtain appropriate legal advice to review your solution, particularly if you will use it in sensitive or high-risk applications. Understand what restrictions you might need to work within and your responsibility to resolve any issues that might come up in the future.
* **Have a human in the loop.** Keep a human in the loop, and include human oversight as a consistent pattern area to explore. Ensure constant human oversight of the AI-powered product or feature. Maintain the role of humans in decision making. Make sure you can have real-time human intervention in the solution to prevent harm and manage situations when the AI system doesn’t perform as expected.
* **Build trust with affected stakeholders.** Communicate the expected benefits and potential risks to affected stakeholders. Help people understand why the data is needed and how the use of the data will lead to their benefit. Describe data handling in an understandable way.
* **Create a customer feedback loop.** Provide a feedback channel that allows users and individuals to report issues with the service after it's deployed. After you've deployed an AI-powered product or feature, it requires ongoing monitoring and improvement. Be ready to implement any feedback and suggestions for improvement. Establish channels to collect questions and concerns from affected stakeholders. People who might be directly or indirectly affected by the system include employees, visitors, and the general public. For example, consider using:

    - Feedback features built into app experiences.
    - An easy-to-remember email address for feedback.
    - Anonymous feedback boxes placed in semi-private spaces.
    - Knowledgeable representatives in the lobby.

* **Always plan to have the user confirm an action before being processed.** Plan to have your user confirm an action before being processed by your client application to avoid incorrect responses that might come from the CLU model. For example, suppose your CLU model is integrated in an HR bot and CLU returns that your user requests five days off. Have the user confirm that this request is the correct action to be taken before processing it.
* **Always plan to have a correction path for the user.** After a certain action is taken by the client application, show a confirmation message to the user of the action that was processed. Plan that the response of the CLU model might not be accurate and that your user might end up in an error state. In that case, always have a fallback plan or a correction path that the user can use to exit from that state. For example, if your CLU model is integrated in an HR bot and the user requested five days off, show a confirmation message that days were deducted from the balance. Include the start and end dates with a link to delete the request or to update the dates.

## Next steps

* [Introduction to conversational language understanding](/azure/ai-services/language-service/conversational-language-understanding/overview)
* [Language Understanding transparency note](clu-transparency-note.md)
* [Microsoft AI principles](https://www.microsoft.com/ai/responsible-ai?rtc=1&activetab=pivot1%3aprimaryr6)
* [Building responsible bots](https://www.microsoft.com/research/uploads/prod/2018/11/Bot_Guidelines_Nov_2018.pdf)
