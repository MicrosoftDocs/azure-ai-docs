---
title: Project best practices
description: Best practices for custom question answering
ms.service: azure-ai-language
ms.topic: how-to
author: laujan
ms.author: lajanuar
recommendations: false
ms.date: 11/18/2025
---
# Project best practices

The following list of QnA pairs are used to represent a project to highlight best practices when authoring in custom question answering. 

|Question                             |Answer                                                 | 
|-------------------------------------|-------------------------------------------------------|
|I want to buy a car.                 |There are three options for buying a car.              |
|I want to purchase software license. |Software licenses can be purchased online at no cost.  |
|How to get access to WPA?            |WPA can be accessed via the company portal.            |
|What is the price of Microsoft stock?|$200.                                                  |
|How do I buy Microsoft Services?     |Microsoft services can be bought online.               |
|I want to sell car.                  |Please send car pictures and documents.                |
|How do I get an identification card? |Apply via company portal to get an identification card.|
|How do I use WPA?                    |WPA is easy to use with the provided manual.           |
|What is the utility of WPA?          |WPA provides a secure way to access company resources. |

## When should you add alternate questions to a QnA?

- Custom question answering employs a transformer-based ranker that takes care of user queries that are semantically similar to questions in the project. For example, consider the following question answer pair:

   **Question: "What is the price of Microsoft Stock?"**

   **Answer: "$200".**

   The service can return expected responses for semantically similar queries such as:

   "How much is Microsoft stock worth?"

   "How much is Microsoft's share value?"

   "How much does a Microsoft share cost?"

   "What is the market value of Microsoft stock?"

   "What is the market value of a Microsoft share?"

   The system's confidence score depends on the input query and how closely it matches the original question-answer pair. Greater differences between them can lead to changes in the confidence level.

- There are certain scenarios that require the customer to add an alternate question. When a query doesn't return the correct answer despite it being present in the project, we advise adding that query as an alternate question to the intended QnA pair.

## How many alternate questions per QnA is optimal?

- Users can add up to 10 alternate questions depending on their scenario. Alternate questions beyond the first 10 aren't considered via our core ranker. However, they're evaluated in the other processing layers resulting in better output overall. All the alternate questions are considered in the preprocessing step to look for an exact match.

- Semantic understanding in custom question answering should be able to take care of similar alternate questions.

- The return on investment starts diminishing once you exceed 10 questions. Even if you're adding more than 10 alternate questions, try to make the initial 10 questions as semantically dissimilar as possible so that all intents for the answer are captured via these 10 questions. For the project in QNA #1, adding alternate questions such as "How can I buy a car?", "I wanna buy a car." aren't required. Whereas adding alternate questions such as "How to purchase a car.", "What are the options for buying a vehicle?" can be useful.

## When to add synonyms to a project

- Custom question answering provides the flexibility to use synonyms at the project level, unlike QnA Maker where synonyms are shared across projects for the entire service.

- For better relevance, the customer needs to provide a list of acronyms that the end user intends to use interchangeably. For instance, the following list provides acceptable acronyms:

   * MSFT – Microsoft

   * ID – Identification

   * ETA – Estimated time of Arrival

- Apart from acronyms, if you think your words are similar in context of a particular domain and generic language models don't consider them similar, it's better to add them as synonyms. For instance, if an auto company producing a car model X receives queries such as "my car's audio isn't working" and the project has questions on "fixing audio for car X," then we need to add "X" and "car" as synonyms.

- The Transformer based model already takes care of most of the common synonym cases, for example- Purchase – Buy, Sell - Auction, Price – Value. For example, consider the following QnA pair: Q: "What is the price of Microsoft Stock?" A: "$200".

Users should receive accurate answers to queries like "Microsoft stock value," "Microsoft share value," or "stock worth," even if terms such as "share," "value," or "worth" aren't present in the knowledge base.

## How are lowercase/uppercase characters treated?

Custom question answering takes casing into account but it's intelligent enough to understand when it's to be ignored. You shouldn't be seeing any perceivable difference due to wrong casing.

## How are QnAs prioritized for multi-turn questions?

When a knowledge base has hierarchical relationships, and the previous answer related to other QnAs, the system slightly favors, in order: child QnAs, sibling QnAs, then grandchild QnAs for the next query. Along with any query, the [custom question Answering API] (/rest/api/cognitiveservices/questionanswering/question-answering/get-answers) expects a "context" object with the property "previousQnAId" that denotes the last top answer. Based on this previous QnA ID, all the related QnAs are boosted.

## How are accents treated?

Accents are supported for all major European languages. If the query has an incorrect accent, confidence score might be slightly different, but the service still returns the relevant answer and takes care of minor errors by using fuzzy search.

## How is punctuation in a user query treated?

Punctuation is ignored in user query before sending it to the ranking stack. Ideally it shouldn't impact the relevance scores. Punctuation that is ignored:  ,?:;\"'(){}[]-+。./!*؟

## Next steps

