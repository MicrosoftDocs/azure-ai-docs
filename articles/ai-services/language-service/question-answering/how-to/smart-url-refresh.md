---
title: Smart URL refresh - custom question answering
titleSuffix: Foundry Tools
description: Use the custom question answering smart URL refresh feature to keep your project up to date.
ms.service: azure-ai-language
author: laujan
ms.author: lajanuar
ms.topic: how-to
ms.date: 12/15/2025
---
# Use smart URL refresh with a project

Custom question answering allows you to keep your source content up to date by retrieving the latest information from a source URL. With just one selection, you can update the corresponding project to reflect these changes. The service ingests content from the URL and either creates, merges, or deletes question-and-answer pairs in the project. 

This functionality is provided to support scenarios where the content in the source URL changes frequently, such as product FAQ page updates. The service refreshes the source and update the project to the latest content while retaining any manual edits made previously.

> [!NOTE]
> This feature is only applicable to URL sources, and they must be refreshed individually, not in bulk. 

> [!IMPORTANT]
> This feature is only available in the `2021-10-01` version of Azure Language API.

## How it works

If you have a project with a URL source that changed, you can trigger a smart URL refresh to keep your project up to date. The service scans the URL for updated content and generates QnA pairs. It adds any new QnA pairs to your project and also delete any pairs that disappeared from the source (with exceptions&mdash;). It also merges old and new QnA pairs in some situations.

> [!IMPORTANT]
> Because smart URL refresh can involve deleting old content from your project, you might want to [create a backup](./export-import-refresh.md) of your project before you do any refresh operations.

You can trigger a refresh programmatically using the REST API. See the **[Update Sources](/rest/api/questionanswering/question-answering-projects/update-sources)** reference documentation for parameters and a sample request.

## Smart refresh behavior

When the user refreshes content using this feature, the project of QnA pairs may be updated in the following ways:

### Delete old pair

If the content at the source URL changes and an existing QnA pair from the previous version is no longer present, that pair is removed from the updated project. This process ensures that your refreshed project only contains QnA pairs that match the current source content. For example, if a QnA pair like Q1A1 existed in the previous version of the project, but after refreshing, the updated source no longer generates the A1 answer, that pair is considered outdated. As a result, Q1A1 is removed from the project entirely.

However, if the old QnA pairs are manually edited in the authoring portal, they aren't deleted.

### Add new pair

If the URL has new content, and a new QnA pair appears in the old knowledge base, the new pair is added. This addition ensures your knowledge base always includes the latest information from the source. For example, if the service finds that a new answer A2 can be generated, then the QnA pair Q2A2 is inserted into the KB.

### Merge pairs

If the answer of a new QnA pair matches the answer of an old QnA pair, the two pairs are merged. The new pair's question is added as an alternate question to the old QnA pair. For example, consider Q3A3 exists in the old source. When you refresh the source, a new QnA pair Q3'A3 is introduced. In that case, the two QnA pairs are merged: Q3' is added to Q3 as an alternate question. 

If the old QnA pair has a metadata value, that data is retained and persisted in the newly merged pair.
  
If the old QnA pair has follow-up prompts associated with it, then the following scenarios may arise:
* If the prompt attached to the old pair is from the source being refreshed, that prompt is deleted, and the prompt of the new pair (if any exists) is appended to the newly merged QnA pair.
* If the prompt attached to the old pair is from a different source, then that prompt is maintained as-is. The prompt from the new question (if any exists) is appended to the newly merged QnA pair.


#### Merge example
See the following example of a merge operation with differing questions and prompts:

|Source iteration|Question  |Answer  |Prompts  |
|---------|---------|---------|--|
|old |"What is the new HR policy?"     |  "You might have to choose among the following options:"       | P1, P2        |
|new |"What is the new payroll policy?"    |  "You might have to choose among the following options:"    |  P3, P4   |

The prompts P1 and P2 come from the original source and are different from prompts P3 and P4 of the new QnA pair. They both have the same answer, `You might have to choose among the following options:`, but it leads to different prompts. In this case, the resulting QnA pair would look like this:

|Question  |Answer  |Prompts  |
|---------|---------|--|
|"What is the new HR policy?" </br>(Alternate question: "What is the new payroll policy?")    |  "You might have to choose among the following options:"       | P3, P4  |

#### Duplicate answers scenario

When the original source has two or more QnA pairs with the same answer (as in, Q1A1 and Q2A1), the merge behavior may be more complex.

If each QnA pair has its own prompt (like Q1A1 with P1 and Q2A1 with P2), the updated source might make a new QnA pair with the same answer but a new prompt, such as Q1'A1 with P3. In this case, the new question is added as an alternate to the originals. This process helps keep the QnA pairs up to date with the latest source content. However, all of the original prompts are replaced via the new prompt from the refreshed content. So the final pair set looks like this:

|Question  |Answer  |Prompts  |
|---------|---------|--|
|Q1 </br>(alternate question: Q1')    |  A1    | P3  |
|Q2 </br>(alternate question: Q1')    |  A1    | P3  |

## Next steps

* [Custom question answering quickstart](../quickstart/sdk.md?pivots=studio)
* [Update Sources API reference](/rest/api/questionanswering/question-answering-projects/update-sources)
