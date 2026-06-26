---
title: Manage projects - custom question answering
description: Manage custom question answering projects in Microsoft Foundry, including sources, project settings, and project lifecycle tasks.
ms.service: azure-ai-language
ms.topic: how-to
author: laujan
ms.author: lajanuar
ms.date: 06/18/2026
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

For backup and restore operations, see [Export-import-refresh in custom question answering](./export-import-refresh.md).

## Manage sources

1. Open your CQA fine-tuning task in Foundry.
1. From **Getting Started**, select **Manage sources**.
1. Add and maintain your sources:

   |Goal|Action|
   |--|--|
   |Add source|Select **Add source** and choose **URLs**, **Files**, or **Chit-chat**.|
   |Delete source|Select one or more sources, then delete them.|
   |Classify file structure|For uploaded files, choose **Auto-detect** or **Unstructured content** based on source format.|

For URL-specific updates, see [Use smart URL refresh with a project](./smart-url-refresh.md).

## Manage large projects

From the CQA authoring experience, you can:

* Search by question, answer, and metadata.
* Review large datasets incrementally.
* Validate behavior using **Test knowledge base** before deployment.

## Delete a project

Deleting a project is permanent and can't be undone.

Before you delete a project, export it for backup by using [Export-import-refresh in custom question answering](./export-import-refresh.md).

If you share a project with collaborators and then delete it, they lose access immediately.

## Next steps

* [Create, test, and deploy a CQA knowledge base](./create-test-deploy.md)
* [Export-import-refresh in custom question answering](./export-import-refresh.md)
* [Configure your environment for Azure AI resources](./configure-azure-resources.md)
