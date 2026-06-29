---
title: Manage projects - custom question answering
description: Manage custom question answering projects in Microsoft Foundry, including sources, project settings, project lifecycle tasks, export, import, refresh, and smart URL refresh.
ms.service: azure-ai-language
ms.topic: how-to
author: laujan
ms.author: lajanuar
ms.date: 06/29/2026
ms.custom: language-service-question-answering
---
<!-- markdownlint-disable MD025 -->

# Manage projects in custom question answering

Use Microsoft Foundry to manage your custom question answering (CQA) projects, including project settings, sources, and project lifecycle operations.

If you haven't created a CQA project yet, start with [Create, test, and deploy a CQA knowledge base](create-test-deploy.md).

## Prerequisites

* If you don't have an Azure subscription, [create a free account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn) before you begin.
* A [Foundry resource](../../../multi-service-resource.md) or [Language resource](https://aka.ms/create-language-resource).
* A Foundry project that contains a CQA fine-tuning task. For setup instructions, see [Create, test, and deploy a CQA knowledge base](create-test-deploy.md).

## Create a project

To create a project in Foundry, follow [Create, test, and deploy a CQA knowledge base](create-test-deploy.md).

## Manage projects

In Foundry, you can:

* Create projects.
* Delete projects.
* Deploy or redeploy projects.
* Open projects for source management and testing.

For backup and restore operations, see [Export, import, and refresh a project](#export-import-and-refresh-a-project).

## Manage sources

1. Open your CQA fine-tuning task in Foundry.
1. From **Getting Started**, select **Manage sources**.
1. Add and maintain your sources:

   |Goal|Action|
   |--|--|
   |Add source|Select **Add source** and choose **URLs**, **Files**, or **Chit-chat**.|
   |Delete source|Select one or more sources, then delete them.|
   |Classify file structure|For uploaded files, choose **Auto-detect** or **Unstructured content** based on source format.|

For URL-specific updates, see [Use smart URL refresh with a project](#use-smart-url-refresh-with-a-project).

## Manage large projects

From the CQA authoring experience, you can:

* Search by question, answer, and metadata.
* Review large datasets incrementally.
* Validate behavior using **Test knowledge base** before deployment.

## Delete a project

Deleting a project is permanent and can't be undone.

Before you delete a project, export it for backup by using [Export, import, and refresh a project](#export-import-and-refresh-a-project).

If you share a project with collaborators and then delete it, they lose access immediately.

## Export, import, and refresh a project

You might want to create a copy of your custom question answering project or related question and answer pairs for several reasons:

* To implement a backup and restore process
* To integrate with your CI/CD pipeline
* To move your data to different regions

### Export a project programmatically

To automate the export process, use the [export functionality of the authoring API](./authoring.md#export-project-metadata-and-assets).

### Import a project programmatically

To automate the import process, use the [import functionality of the authoring API](./authoring.md#import-project).

### Refresh a URL programmatically

To automate the URL refresh process, use the [update sources functionality of the authoring API](./authoring.md#update-sources).

The update sources example in the [Authoring API docs](./authoring.md#update-sources) shows the syntax for adding a new URL-based source. An example query for an update would be as follows:

|Variable name | Value |
|--------------------------|-------------|
| `ENDPOINT`               | Find this value in the **Keys & Endpoint** section when examining your resource from the Azure portal. An example endpoint is: `https://southcentralus.cognitiveservices.azure.com/` and you only need to add the region-specific portion of `southcentral`. The endpoint path is already present.|
| `API-KEY` | Find this value in the **Keys & Endpoint** section when examining your resource from the Azure portal. You can use either Key1 or Key2. Always having two valid keys allows for secure key rotation with zero downtime. The key value is part of the sample request.|
| `PROJECT-NAME` | The name of project where you want to update sources.|

```bash
curl -X PATCH -H "Ocp-Apim-Subscription-Key: {API-KEY}" -H "Content-Type: application/json" -d '[
  {
    "op": "replace",
    "value": {
      "displayName": "source5",
      "sourceKind": "url",
      "sourceUri": "https://support.microsoft.com/en-US/surface/models/surface-book-3-specs-and-features",
      "refresh": "true"
    }
  }
]'  -i 'https://{ENDPOINT}.cognitiveservices.azure.com/language/query-knowledgebases/projects/{PROJECT-NAME}/sources?api-version=2021-10-01'
```

## Use smart URL refresh with a project

Custom question answering helps you keep your source content up to date by retrieving the latest information from a source URL. With just one selection, you can update the corresponding project to reflect these changes. The service ingests content from the URL and either creates, merges, or deletes question-and-answer pairs in the project. 

This functionality supports scenarios where the content in the source URL changes frequently, such as product FAQ page updates. The service refreshes the source and updates the project to the latest content while retaining any manual edits you made previously.

> [!NOTE]
> This feature only applies to URL sources. You must refresh them individually, not in bulk. 

> [!IMPORTANT]
> This feature is only available in the `2021-10-01` version of Azure Language API.

### How it works

If you have a project with a URL source that changed, you can trigger a smart URL refresh to keep your project up to date. The service scans the URL for updated content and generates QnA pairs. It adds any new QnA pairs to your project and also deletes any pairs that disappeared from the source (with exceptions). It also merges old and new QnA pairs in some situations.

> [!IMPORTANT]
> Because smart URL refresh can delete old content from your project, [create a backup](#export-import-and-refresh-a-project) of your project before you do any refresh operations.

You can trigger a refresh programmatically by using the REST API. For parameters and a sample request, see the **[Update Sources](/rest/api/questionanswering/question-answering-projects/update-sources)** reference documentation.

### Smart refresh behavior

When you refresh content by using this feature, the project of QnA pairs might update in the following ways:

#### Delete old pair

If the content at the source URL changes and an existing QnA pair from the previous version is no longer present, the process removes that pair from the updated project. This process ensures that your refreshed project only contains QnA pairs that match the current source content. For example, if a QnA pair like Q1A1 existed in the previous version of the project, but after refreshing, the updated source no longer generates the A1 answer, that pair is considered outdated. As a result, Q1A1 is removed from the project entirely.

However, if you manually edit the old QnA pairs in the authoring portal, the process doesn't delete them.

#### Add new pair

If the URL has new content, and a new QnA pair appears in the old knowledge base, the process adds the new pair. This addition ensures your knowledge base always includes the latest information from the source. For example, if the service finds that a new answer A2 can be generated, it inserts the QnA pair Q2A2 into the knowledge base.

#### Merge pairs

If the answer of a new QnA pair matches the answer of an old QnA pair, the process merges the two pairs. The new pair's question is added as an alternate question to the old QnA pair. For example, consider Q3A3 exists in the old source. When you refresh the source, a new QnA pair Q3'A3 is introduced. In that case, the two QnA pairs are merged: Q3' is added to Q3 as an alternate question. 

If the old QnA pair has a metadata value, the process retains and persists that data in the newly merged pair.
  
If the old QnA pair has follow-up prompts associated with it, then the following scenarios might arise:
* If the prompt attached to the old pair is from the source being refreshed, the process deletes that prompt, and appends the prompt of the new pair (if any exists) to the newly merged QnA pair.
* If the prompt attached to the old pair is from a different source, the process maintains that prompt as-is. The prompt from the new question (if any exists) is appended to the newly merged QnA pair.

#### Merge example
See the following example of a merge operation with differing questions and prompts:

|Source iteration|Question  |Answer  |Prompts  |
|---------|---------|---------|--|
|old |"What is the new HR policy?"     |  "You might have to choose among the following options:"       | P1, P2        |
|new |"What is the new payroll policy?"    |  "You might have to choose among the following options:"    |  P3, P4   |

The prompts P1 and P2 come from the original source and are different from prompts P3 and P4 of the new QnA pair. They both have the same answer, `You might have to choose among the following options:`, but it leads to different prompts. In this case, the resulting QnA pair looks like this:

|Question  |Answer  |Prompts  |
|---------|---------|--|
|"What is the new HR policy?" </br>(Alternate question: "What is the new payroll policy?")    |  "You might have to choose among the following options:"       | P3, P4  |

#### Duplicate answers scenario

When the original source has two or more QnA pairs with the same answer (as in, Q1A1 and Q2A1), the merge behavior might be more complex.

If each QnA pair has its own prompt (like Q1A1 with P1 and Q2A1 with P2), the updated source might make a new QnA pair with the same answer but a new prompt, such as Q1'A1 with P3. In this case, the new question is added as an alternate to the originals. This process helps keep the QnA pairs up to date with the latest source content. However, the new prompt from the refreshed content replaces all of the original prompts. So the final pair set looks like this:

|Question  |Answer  |Prompts  |
|---------|---------|--|
|Q1 </br>(alternate question: Q1')    |  A1    | P3  |
|Q2 </br>(alternate question: Q1')    |  A1    | P3  |

## Next steps

* [Create, test, and deploy a CQA knowledge base](./create-test-deploy.md)
* [Configure your environment for Azure AI resources](./configure-azure-resources.md)
* [Update Sources API reference](/rest/api/questionanswering/question-answering-projects/update-sources)
