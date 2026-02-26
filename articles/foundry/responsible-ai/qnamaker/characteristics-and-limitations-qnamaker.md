---
title: Characteristics and limitations of QnA Maker
titleSuffix: Foundry Tools
description: Characteristics and limitations of QnA Maker
author: laujan
ms.author: lajanuar
manager: nitinme
ms.service: azure-ai-language
ms.topic: concept-article
ms.subservice: azure-ai-qna-maker
ms.date: 02/25/2021
---

# Characteristics and limitations of QnA Maker

[!INCLUDE [non-english-translation](../includes/non-english-translation.md)]

Depending on your scenario and the input data, you might experience different levels of performance from QnA Maker. A common way to evaluate the quality of responses is to create a set of commonly asked queries in your scenario, and check whether the QnA Maker response matches the expected response. The [batch testing tool](/azure/ai-services/qnamaker/reference-tsv-format-batch-testing) will help you in evaluating your query set. The following sections discuss key concepts and best practices to improve the performance.

## Enhance system performance 

There are two main technology pieces of QnA Maker: QnA extraction from the source, and returning the best response for a query.

### QnA extraction from the source

QnA Maker is able to extract question and answer pairs from semi-structured content. The
algorithm looks for a repeating pattern in the source documents, or for a particular layout of the content, to determine which sections constitute a question and answer. You can extract from content such as FAQ URLs, product manuals, and support documentation. When extracting, QnA Maker focuses on using content that is suitable for a chat bot, which typically has a small surface area.

Note the following limitations and best practices:

- The extraction is primarily focused on text and images (from URLs and documents). Other elements, like tables and images in files are ignored in the extraction. This might lead to incomplete extractions.

- The extraction relies heavily on the structure of each document and looks for a pattern of question and answer pairs or recurring topics and sections. Content that doesn't have a dominant structure, or that has different formats in the same document, makes it more difficult for QnA Maker to extract questions and answers (for example, news articles and blogs).

- When you're deciding on the sources for your knowledge base, choose content that has some structure to it. For more information, see [Importing from data sources](/azure/ai-services/qnamaker/concepts/data-sources-and-content). Also keep in mind that the extracted answers need to be displayed in a chat bot, which usually has limitations in rendering content.

- Sources that are in a secure storage, such as OneDrive or DropBox, are currently unsupported in QnA Maker. You can only extract files stored in [SharePoint](/azure/ai-services/qnamaker/how-to/add-sharepoint-datasources).

### Return the best response for a query

QnA Maker uses sophisticated natural language processing and ranking technology to match an incoming user query with the best QnA match in its index. To optimize performance, these models are trained on several open source and custom datasets. However, depending on the contents of your knowledge base, the relevance of responses may vary. Learn more about the ranking process [here](/azure/ai-services/qnamaker/concepts/query-knowledge-base?tabs=v1). Each response is associated with a [confidence score](/azure/ai-services/qnamaker/concepts/confidence-score), which usually denotes the quality of the response. The higher the confidence scores, the higher the likelihood that the answer is correct for the asked question. False positive results occur when a wrong answer has a high confidence score, or the correct answer is not the top result.

Note the following limitations and best practices:

- Repeating the same word set within different questions in question and answer pairs will reduce the likelihood that the right answer is chosen for a particular user query with those words. For example, you might have two separate QnAs with the following questions: *"where is the parking location"*, *"where is the ATM location"*. Because these two QnAs use such similar words, this similarity might cause very similar scores for many user queries that are phrased like *\"where is the *\<x\>* location\"*. Instead, you might clearly differentiate with queries like *\"where is the parking lot\"* and *\"where is the ATM\"*. 

- Add as many alternate questions as you need, but keep the alternate questions simple. Adding more words or phrasings that aren't part of the main goal of the question doesn't help QnA Maker
find a match. Your user might enter questions with either a conversational style of text, ("*How do I add a toner cartridge to my printer?"*), or a keyword search (*"toner cartridge"*). The knowledge base should have both styles of questions in order to correctly return the best answer. If you aren't sure what keywords a customer is entering, use telemetry data to analyze queries.

- If a question in the knowledge base is ambiguous or could have multiple possible responses to it, ask the user for additional information. For more details, see [Use follow-up prompts to create multiple turns of a conversation](/azure/ai-services/qnamaker/how-to/multi-turn).

- [Metadata](/azure/ai-services/qnamaker/how-to/edit-knowledge-base) helps narrow down the results of a user query based on metadata tags. The knowledge base answer can differ based on the metadata tag, even if the query is the same. For example, *\"where is restaurant parking located\"* can have a different answer depending on the location of the restaurant branch.

- QnA Maker supports some basic synonyms in the English language like *I am*, *I'm*, etc. To add synonyms to keywords that take different forms, use the Alterations API to add case-insensitive word alterations. For example, if the original word is *Buy*, you might create the following synonyms: *purchase*, *net-banking*, and *net banking*. All the knowledge bases created in a particular QnA Maker service will share the synonym list. Synonyms are not shared across QnA Maker services.

## Next steps

* [Microsoft AI principles](https://www.microsoft.com/ai/responsible-ai)

* [Microsoft responsible AI resources](https://www.microsoft.com/ai/responsible-ai-resources)

* [Microsoft principles for developing and deploying facial recognition technology](https://blogs.microsoft.com/wp-content/uploads/prod/sites/5/2018/12/MSFT-Principles-on-Facial-Recognition.pdf)

* [Identify principles and practices for responsible AI](/training/paths/responsible-ai-business-principles/)

* [Building responsible bots](https://www.microsoft.com/research/uploads/prod/2018/11/Bot_Guidelines_Nov_2018.pdf)
