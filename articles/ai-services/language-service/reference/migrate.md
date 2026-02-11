---
title: "Migrate to Azure Language from Language Understanding (LUIS) or QnA Maker"
titleSuffix: Foundry Tools
description: Use this article to learn if you need to migrate your applications from Language Understanding (LUIS), QnA Maker, and Text Analytics.
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: concept-article
ms.date: 02/09/2026
ms.author: lajanuar
---
<!-- markdownlint-disable MD025 -->
# Migrate to Azure Language in Foundry Tools

On November 2, 2021, Azure Language in Foundry Tools was released into public preview. Azure Language unifies the Text Analytics, QnA Maker, and Language Understanding (LUIS) service offerings, and provides several new features as well.

> [!IMPORTANT]
>
> * You may experience intermittent interruptions when calling the Language Understanding (LUIS) service. Microsoft is in the final phase of retiring LUIS. These interruptions are temporary but expected during this retirement phase.
> * Beginning March 31, 2026, LUIS runtime and authoring endpoints (including REST API calls) are fully retired, and all LUIS requests fail.
> * To ensure uninterrupted operation, export all of your LUIS app data as soon as possible in order to:
>   * Start using [Conversational Language Understanding (CLU)](../conversational-language-understanding/overview.md), or
>   * Try out a [Microsoft Foundry](../conversational-language-understanding/quickstart.md).
> * Use the following API to export your data: [LUIS Versions - Export](/rest/api/luis/versions/export?view=rest-luis-v2.0&preserve-view=true&tabs=HTTP).

## How do I migrate to Azure Language if I'm using Language Understanding (LUIS)?

If you're using Language Understanding (LUIS), you can [import your Language Understanding (LUIS) JSON file](../conversational-language-understanding/how-to/fail-over.md#import-to-a-new-project) to the new Conversational language understanding feature:

1. Export the LUIS app

   * Export your LUIS application as JSON by using the LUIS authoring APIs or the LUIS portal.
   * LUIS Versions – [Export REST API](/rest/api/luis/versions/export?view=rest-luis-v2.0&preserve-view=true&tabs=HTTP)

1. Map LUIS data to the CLU schema

   * Update the exported JSON to align intents, entities, and utterances with the CLU project schema.
   * [Conversational Language Understanding overview](../conversational-language-understanding/overview.md) provides details on the CLU schema and supported features.

1. Create a CLU project and import data

   * Create a CLU project and import the prepared data by using Language Studio or the CLU authoring APIs.
   * [CLU quickstart (REST API)](../conversational-language-understanding/quickstart.md?pivots=rest-api) provides instructions on creating a CLU project and importing data.

1. Train the model

   * Start a training job to build the CLU model from the imported data.
   * [Train and evaluate a CLU model](../conversational-language-understanding/how-to/train-model.md) provides details on training and evaluating your CLU model.

1. Test the model

   * Send test utterances to the CLU prediction endpoint and verify intent and entity results.
   * [Conversational Language Understanding overview](../conversational-language-understanding/how-to/call-api.md) provides details on querying your CLU model.

## How do I migrate to Azure Language if I'm using QnA Maker?

If you're using QnA Maker, you can [import your QnA Maker knowledge base](../question-answering/how-to/migrate-knowledge-base.md#import-a-project) to the custom questiona answering (CQA) feature:

1. Export the QnA Maker knowledge base

   * Download your knowledge base by using the QnA Maker REST APIs with your endpoint key and knowledge base ID.
   * [QnA Maker REST API reference](/rest/api/questionanswering/question-answering-projects/export?view=rest-questionanswering-2021-10-01&preserve-view=true&tabs=HTTP) provides instructions on exporting your knowledge base.

1. Create a Custom Question Answering project

   * Create a new Custom Question Answering project.
   * [Create a Custom Question Answering project](../question-answering/quickstart/sdk.md) provides instructions on creating a CQA project.

1. Import the knowledge base

   * Import the exported knowledge base file into your Custom Question Answering project.
   * [Import knowledge base](../question-answering/how-to/authoring.md#import-project) provides instructions on importing your knowledge base.
   * For more information , see also, [Move projects and question answer pairs](../question-answering/how-to/migrate-knowledge-base.md).

1. Create and test a knowledge base

   * Create, test, and deploy a custom question answering knowledge base in the Microsoft Foundry (classic) Language playground.
   * [Create, test, and deploy: CQA knowledge base](../question-answering/how-to/create-test-deploy.md) provides instructions on creating and testing your project.


Consider using one of the available quickstart articles to see the latest information on service endpoints, and API calls.


## See also

* [Azure Language in Foundry Tools overview](../overview.md)
* [Conversational language understanding overview](../conversational-language-understanding/overview.md)
* [Question answering overview](../question-answering/overview.md)
