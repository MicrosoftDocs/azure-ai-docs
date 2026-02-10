---
title: Guidance for integration and responsible use with custom NER
titleSuffix: Foundry Tools
description: Guidance for integration and responsible use with custom named entity recognition
author: laujan
ms.author: lajanuar
manager: nitinme
ms.service: azure-ai-language
ms.topic: best-practice
ms.date: 09/29/2021
---

# Guidance for integration and responsible use with custom named entity recognition

[!INCLUDE [non-english-translation](../includes/non-english-translation.md)]

Microsoft works to help customers responsibly develop and deploy solutions by using custom named entity recognition. Our principled approach upholds personal agency and dignity by considering the AI system's:

* Fairness, reliability, and safety.
* Privacy and security.
* Inclusiveness.
* Transparency.
* Human accountability.

These considerations reflect our commitment to developing responsible AI.

## General guidelines for integration and responsible use

When you get ready to integrate and responsibly use AI-powered products or features, the following activities help to set you up for success:

* **Understand what it can do:** Fully assess the potential of any AI system to understand its capabilities and limitations. Understand how it will perform in your particular scenario and context, by thoroughly testing it with real-life conditions and data.

* **Respect an individual's right to privacy:** Only collect data and information from individuals for lawful and justifiable purposes. Only use data and information that you have consent to use for this purpose.

* **Obtain legal review:** Obtain appropriate legal advice to review your solution, particularly if you will use it in sensitive or high-risk applications. Understand what restrictions you might need to work within, and your responsibility to resolve any issues that might come up in the future.

* **Have a human in the loop:** Keep a human in the loop, and include human oversight as a consistent pattern area to explore. This means ensuring constant human oversight of the AI-powered product or feature, and maintaining the role of humans in decision-making. Ensure that you can have real-time human intervention in the solution to prevent harm. This enables you to manage situations where the AI model doesn't perform as expected.

* **Maintain security:** Ensure your solution is secure, and that it has adequate controls to preserve the integrity of your content and prevent unauthorized access.

* **Build trust with affected stakeholders:** Communicate the expected benefits and potential risks to affected stakeholders. Help people understand why the data is needed and how the use of the data will lead to their benefit. Describe data handling in an understandable way.

* **Create a customer feedback loop:** Provide a feedback channel that allows users and individuals to report issues with the service after it has been deployed. Monitor and improve the AI-powered product or feature on an ongoing basis. Be ready to implement any feedback and suggestions for improvement. Establish channels to collect questions and concerns from affected stakeholders (people who might be directly or indirectly impacted by the system, including employees, visitors, and the general public). For example, consider using:

    * Feedback features built into app experiences.
    * An easy-to-remember email address for feedback.
    * Anonymous feedback boxes placed in semi-private spaces.
    * Knowledgeable representatives in the lobby.

* **Always seek user confirmation of an action:** Plan to have your user confirm an action before that action is processed by your client application. This helps you avoid incorrect responses that might come from the custom named entity recognition (NER) models. For example, suppose your custom NER model is integrated in an insurance claim approval system to extract user-filled data. Have the user confirm that the extracted entities are the correct data submitted by the user. Process the data only after receiving this confirmation.

* **Always plan to have a correction path for the user:** After a certain action is taken by the client application, show a confirmation message to the user of the action that was processed. Plan that the response of the custom NER model might not be accurate, and that your user might end up in an error state. In that case, always have a fallback plan or a correction path that allows the user to exit from that state.  

  For example, if your custom NER application is integrated in an insurance claim approval system, show a confirmation message with the submitted data by the user. The confirmation message should include a link to delete the request or to update the data.

## Next steps

* [Introduction to custom NER](/azure/ai-services/language-service/custom-named-entity-recognition/overview)

* [Custom NER transparency note](custom-named-entity-recognition-transparency-note.md)

* [Microsoft AI principles](https://www.microsoft.com/ai/responsible-ai?rtc=1&activetab=pivot1%3aprimaryr6)
