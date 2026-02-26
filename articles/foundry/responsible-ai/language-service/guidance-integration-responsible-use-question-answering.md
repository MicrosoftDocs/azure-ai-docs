---
title: Guidance for integration and responsible use of question answering
titleSuffix: Foundry Tools
description: Guidance for integration and responsible use of question answering
author: laujan
ms.author: lajanuar
manager: nitinme
ms.service: azure-ai-language
ms.topic: best-practice
ms.date: 09/29/2021
---

# Guidance for integration and responsible use of question answering

[!INCLUDE [non-english-translation](../includes/non-english-translation.md)]

Microsoft wants to help you responsibly develop and deploy solutions that use question answering. We're taking a principled approach to upholding personal agency and dignity by considering the AI systems' fairness, reliability and safety, privacy and security, inclusiveness, transparency, and human accountability. These considerations reflect our commitment to developing Responsible AI.

## General deployment principles

When you're getting ready to deploy AI-powered products or features, the following activities help to set you up for success:

* **Understand what it can do:** Fully assess the capabilities of any AI model you are using to understand its capabilities and limitations. Understand how it will perform in your particular scenario and context, by thoroughly testing it with real-life conditions and data. Synthetic data and tests that don't reflect your end-to-end scenario won't be sufficient.

* **Respect an individual's right to privacy:** Only collect data and information from individuals for lawful and justifiable purposes. Only use data and information that you have consent to use for this purpose.

* **Legal review:** Obtain appropriate legal advice to review your solution, particularly if you will use it in sensitive or high-risk applications. Understand what restrictions you might need to work within, and your responsibility to resolve any issues that might come up in the future. Do not provide any legal advice or guidance.

* **System review:** If you're planning to deploy an AI-powered product or feature into an existing system of software, customers, and organizational processes, take the time to understand how each part of your system will be affected. Consider how your AI solution aligns with [Microsoft's AI principles](https://www.microsoft.com/ai/responsible-ai).

* **Human in the loop:** Keep a human in the loop. This means ensuring constant human oversight of the AI-powered product or feature, and maintaining the role of humans in decision making. Ensure that you can have real-time human intervention in the solution to prevent harm. This enables you to manage situations when the AI model does not perform as required.

* **Security:** Ensure your solution is secure, and that it has adequate controls to preserve the integrity of your content and prevent any unauthorized access.

* **Customer feedback loop:** Provide a feedback channel that allows users and individuals to report issues with the service after it has been deployed. Monitor and improve the AI-powered product or feature on an ongoing basis.

## Specific deployment guidance for question answering

Common use cases of question answering include customer support chat bots and internal enterprise FAQ chat bots. When you're deploying an application that uses question answering, you should ask the following questions:

* **How is the data processed?** All the customer data is stored in Azure Cognitive Search and Azure Monitor in the customer's Azure subscription. Question answering processes the data when extracting questions and answers from sources and serving the correct answers for a particular query. The question answering service doesn't retain customer data after responding to a client application's query.

* **Where is the data stored?** Some countries or domains might have restrictions on the data being stored in a particular geographic area. Choose the appropriate regions for Azure Cognitive Search, and Azure Monitor, keeping in mind the data residency requirements of your scenario.

* **How is user privacy handled?** In some scenarios, users can be asked for additional information before the response is returned from question answering. These scenarios are called [multi-turn conversations](/azure/ai-services/qnamaker/how-to/multi-turn). Some of the information collected from the users can include personal information or other sensitive information. For more information about best practices for data privacy, see the [Responsible bots guidelines](https://www.microsoft.com/research/uploads/prod/2018/11/Bot_Guidelines_Nov_2018.pdf) for developers.

    - **Inform users up front about the data that is collected and how it is used, and obtain their consent beforehand.** Provide easy access to a valid privacy statement and applicable service agreement, and include a "profile page" for users to obtain information about the bot, with links to relevant privacy and legal information.

    - **Collect no more personal data than you need, limit access to it, and store it for no longer than needed.** Collect only the personal data that is essential for your bot to operate effectively. If your bot will share data (such as with another bot), be sure only to share the minimum amount of user data necessary in order to complete the requested function on behalf of the user. If you enable access by other agents to your bot's user data, do so only for the time necessary in order to complete the requested function. Always give users the opportunity to choose which agents your bot will share data with, and what data is suitable for sharing. Consider whether you can purge stored user data from time to time, while still enabling your bot to learn. Shorter retention periods minimize security risks for users.

    - **Provide privacy-protecting user controls.** For bots that store personal information, such as authenticated bots, consider providing easily discoverable buttons to protect privacy. For example: **Show me all you know about me**, **Forget my last interaction** and **Delete all you know about me**. In some cases, such controls might be legally required.

    - **Obtain legal and privacy review.** The privacy aspects of bot design are subject to important and increasingly stringent legal requirements. Be sure to obtain both a legal and a privacy review of your bot's privacy practices through the appropriate channels in your organization.

## Next steps

* [Microsoft AI principles](https://www.microsoft.com/ai/responsible-ai)

* [Microsoft responsible AI resources](https://www.microsoft.com/ai/responsible-ai-resources)

* [Microsoft principles for developing and deploying facial recognition technology](https://blogs.microsoft.com/wp-content/uploads/prod/sites/5/2018/12/MSFT-Principles-on-Facial-Recognition.pdf)

* [Identify principles and practices for responsible AI](/training/paths/responsible-ai-business-principles/)

* [Building responsible bots](https://www.microsoft.com/research/uploads/prod/2018/11/Bot_Guidelines_Nov_2018.pdf)
