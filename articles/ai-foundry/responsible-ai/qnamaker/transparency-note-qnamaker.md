---
title: Use cases for QnA Maker
titleSuffix: Foundry Tools
description: Transparency note for QnA Maker.
author: laujan
ms.author: lajanuar
manager: nitinme
ms.service: azure-ai-language
ms.topic: concept-article
ms.subservice: azure-ai-qna-maker
ms.date: 5/5/2021

---

# Transparency note and use cases for QnA Maker

[!INCLUDE [non-english-translation](../includes/non-english-translation.md)]

## What is a transparency note?

An AI system includes not only the technology, but also the people who will use it, the people who will be affected by it, and the environment in which it is deployed. Creating a system that is fit for its intended purpose requires an understanding of how the technology works, its capabilities and limitations, and how to achieve the best performance.

Microsoft provides *transparency notes* to help you understand how our AI technology works. This includes the choices system owners can make that influence system performance and behavior, and the importance of thinking about the whole system, including the technology, the people, and the environment. You can use transparency notes when developing or deploying your own system, or share them with the people who will use or be affected by your system.

Transparency notes are part of a broader effort at Microsoft to put our AI principles into practice. To find out more, see [Microsoft's AI principles](https://www.microsoft.com/ai/responsible-ai).

## Introduction to QnA Maker

QnA Maker is a cloud-based, natural language processing service that easily creates a natural conversational layer over your data. It can be used to find the most appropriate answer for a specified natural language input, from your custom knowledge base of information. See the list of supported languages [here](/azure/ai-services/qnamaker/overview/language-support?tabs=v1).

QnA Maker is commonly used to build conversational client applications, which include social media applications, chat bots, and speech-enabled desktop applications. A client application based on QnA Maker can be any conversational application that communicates with a user in natural language to answer a question.

QnA Maker uses several Azure resources, each for a different purpose: [Azure Cognitive Search](/azure/ai-services/qnamaker/concepts/azure-resources#cognitive-search-resource), [App Server and App Service plan](/azure/ai-services/qnamaker/concepts/azure-resources#app-service-and-app-service-plan) and [Application Insights](/azure/ai-services/qnamaker/concepts/azure-resources#application-insights). All customer data (question answers and chatlogs) is stored in the region where the customer deploys the dependent service instances. For more details on dependent services see [here](/azure/ai-services/qnamaker/concepts/plan?tabs=v1).

### The basics of QnA Maker

The first step in using QnA Maker is training and preparing the QnA service to recognize the questions and answers that may be developed from your content.  QnA Maker imports your content into a knowledge base of question and answer pairs. The import process extracts information about the relationship between the parts of your structured and semi-structured content to infer relationships between the question and answer pairs.

The extracted QnA pairs are displayed in the following way:

![A diagram of an example question and answer with metadata.](media\qnamaker-qna-table.png)

You can edit these question and answer pairs, and add new pairs yourself. When you're satisfied with the content of your knowledge base, you can publish it, which will make it ready to be used to respond to questions sent to your client applications. At the second step, your client application sends the user's question to your QnA Maker service API. Your QnA Maker service processes the question and responds with the best answer.

![A diagram of asking a bot a question, and getting an answer from knowledge base content.](media\qnamaker-request-response.png)

For more details, see the [QnA Maker documentation](/azure/ai-services/qnamaker/). 

### Terms and definitions

**Term**    |  **Definition**
------ | ------
Knowledge base   | A collection of questions, answers, and metadata that have been extracted from content sources or added manually. The collection is then used to develop question and answer pairs. Queries to the QnA service are matched against the contents of the knowledge base.
Active learning | Consumes the feedback from use of the system to provide suggestions (in the form of new questions) to the knowledge base owner to improve the contents of their knowledge base. Learn more [here](/azure/ai-services/qnamaker/how-to/use-active-learning?tabs=v1).
Multi-turn | Sometimes additional information is needed for QnA Maker to determine the best answer to a user question. QnA Maker asks a follow-up question to the user.
Metadata | Additional information in the form of a name and value that you can associate with each QnA pair in your knowledge base. Metadata can be used to pass context and filter results.
Synonyms  | Alternate terms that can be used interchangeably in the knowledge base.

### Example use cases

You can use QnA Maker in multiple scenarios and across a variety of industries. Typically information retrieval use cases are best suited for QnA Maker where there are usually one or only a few correct responses to a user question. Scenarios or topics that have a wide variety of viewpoints, worldviews, geopolitical views, controversial content, etc. will be more difficult to answer correctly. Customers should be aware that providing this type of content via QnA Maker can create negative sentiment and reactions, and result in negative publicity. If you do provide this type of content, consider adding source attribution to allow your users to evaluate the answers for themselves. 

Some typical scenarios where QnA Maker is recommended are:

- **Customer support:** In most customer support scenarios, common questions get asked frequently. QnA Maker lets you instantly create a chat bot from existing support content, and this bot can act as the front line system for handling customer queries. If the questions can't be answered by the bot, then additional components can help identify and flag the question for human intervention.

- **Enterprise FAQ bot:** Information retrieval is a challenge for enterprise employees. Internal FAQ bots are a great tool for helping employees get answers to their common questions. QnA Maker enables various departments, such as human resources or payroll, to build FAQ chat bots to help employees.

- **Instant answers over search:** Many search systems augment their search results with instant answers, which provide the user with immediate access to information relevant to their query. Answers from QnA Maker can be combined with the results from document search to offer an instant answer experience to the end user.

### Considerations when choosing other use cases

* **Avoid high-risk scenarios:** The machine learnt algorithm used by QnA Maker optimizes the performance based on the data it is trained on, however there will always be edge cases where the correct answer isn't returned for a user query which the system doesn't understand well. When you design your scenarios with QnA Maker, be aware of the possibility of false positive results. It is advisable to create a dataset of the top queries asked in your scenario and the corresponding expected answers, and periodically test the service for the correctness of the responses. For example:

  * **Healthcare:** This often requires high precision, and wrong information can have life-threatening consequences. Consider the example of a Doctor Assistant bot that uses QnA Maker to understand the patient's symptoms and match it to common illnesses.  Likewise, any bots that are designed to converse with patients with mental health issues, such as depression or anxiety, must be very careful of the responses returned. QnA Maker can be helpful in parsing through clinical terminology and deriving useful question and answer pairs, but is not designed, intended or made available to create medical devices, and is not designed or intended and should not be used as a substitute for professional medical advice, diagnosis, treatment, or judgment. Customer is solely responsible for displaying and/or obtaining appropriate consents, warnings, disclaimers and acknowledgements to end users of their implementation.

* **Avoid open domain scenarios:** QnA Maker is meant to answer questions from a particular domain knowledge base, not open-ended questions, or out-of-domain questions. Using out-of-domain questions with QnA Maker runs the risk of returning incorrect responses. For example:

  * **Social bots:** Bots that are meant for generic chit-chat, not related to a particular domain, are difficult to design with QnA Maker. In these scenarios, the user intents and viewpoints can range widely (for example, sports, fashion, politics, and religion). Building a QnA Maker knowledge base is best used for facts and/or discovery of content.  Using QnA Maker for diverse worldview topics may be challenging and we recommend customers consider more careful review or curating of such content.

  * **Handling inappropriate conversations:** It's possible that users will initiate inappropriate conversations with the bot, including expletives or hate speech. The bot designer must be very careful about how to handle these conversations, and make sure that these intents are detected with high accuracy and the appropriate response given. It's difficult to build a comprehensive knowledge base in QnA Maker containing every variation of inappropriate utterances possible. It is therefore better to handle such cases with a rule based system, for example the user utterances can be quickly checked for the presence of any words from a pre-processed blocklist of inappropriate keywords. This is not part of the QnA Maker service and would need to be developed on top of the QnA Maker service. 

* [!INCLUDE [regulatory-considerations](../includes/regulatory-considerations.md)]

## Next steps

* [Microsoft AI principles](https://www.microsoft.com/ai/responsible-ai)

* [Microsoft responsible AI resources](https://www.microsoft.com/ai/responsible-ai-resources)

* [Microsoft principles for developing and deploying facial recognition technology](https://blogs.microsoft.com/wp-content/uploads/prod/sites/5/2018/12/MSFT-Principles-on-Facial-Recognition.pdf)

* [Identify principles and practices for responsible AI](/training/paths/responsible-ai-business-principles/)

* [Building responsible bots](https://www.microsoft.com/research/uploads/prod/2018/11/Bot_Guidelines_Nov_2018.pdf)
