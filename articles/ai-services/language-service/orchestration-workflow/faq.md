---
title: Frequently Asked Questions for orchestration projects
titleSuffix: Foundry Tools
description: Use this article to quickly get the answers to FAQ about orchestration projects
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: faq
ms.date: 12/17/2025
ms.author: lajanuar
ms.custom: mode-other
---
# Frequently asked questions for orchestration workflows

Use this article to quickly get the answers to common questions about orchestration workflows

## How do I create a project?

For more information, *see* the [quickstart](./quickstart.md) to quickly create your first project, or the [how-to article](./how-to/create-project.md).

## How do I connect other service applications in orchestration workflow projects?

For more information, *see* [How to create projects and build schemas](./how-to/create-project.md).

## Which `LUIS` applications can I connect to in orchestration workflow projects?

`LUIS` applications that use Azure Language resource as their authoring resource are available for connection. You can only connect to `LUIS` applications that are owned via the same resource. This option is only available for resources in West Europe, as it's the only common available region between `LUIS` and `CLU`.

## Which question answering project can I connect to in orchestration workflow projects?

Question answering projects that use Azure Language resource are available for connection. You can only connect to question answering projects that are in the same Language resource.

## Training is taking a long time, is this time period expected?

For orchestration projects, long training times are expected. Based on the number of examples you have your training times may vary from 5 minutes to 1 hour or more. 

## Can I add entities to orchestration workflow projects?

No. Orchestration projects are only enabled for intents that can be connected to other projects for routing. 

<!--
## Which languages are supported in this feature?

See the [language support](./language-support.md) article.
-->
## How do I get more accurate results for my project?

For more information, *see*  [evaluation metrics](./concepts/evaluation-metrics.md).
<!--
## How many intents, and utterances can I add to a project?

See the [service limits](./service-limits.md) article. 
-->
## Can I label the same word as two different entities?

Unlike `LUIS`, you can't label the same text as two different entities. Learned components across different entities are mutually exclusive, and only one learned span is predicted for each set of characters.

## Is there any SDK support?

Yes, only for predictions, and [samples are available](https://aka.ms/cluSampleCode). There's currently no authoring support for the SDK.

## Are there APIs for this feature?

Yes, all the APIs are available.
* [Authoring APIs](https://aka.ms/clu-authoring-apis)
* [Prediction API](/rest/api/language/2023-04-01/conversation-analysis-runtime/analyze-conversation)

## Next steps

[Orchestration workflow overview](overview.md)
