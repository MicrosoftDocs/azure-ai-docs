---
title: Move projects - custom question answering
description: Moving a custom question answering project uses export and import operations.
ms.service: azure-ai-language
ms.topic: how-to
author: laujan
ms.author: lajanuar
ms.date: 06/18/2026
ms.custom: language-service-question-answering
---
<!-- markdownlint-disable MD025 -->

# Move projects in custom question answering

Use this guide to move custom question answering (CQA) projects by exporting from one environment and importing into another.

For the complete backup and restore workflow, including refresh operations, see [Export, import, and refresh a project](./manage-knowledge-base.md#export-import-and-refresh-a-project).

## Export a project

1. Open your CQA fine-tuning task in Microsoft Foundry.
1. Go to the export operation for your project assets.
1. Save the exported package to a secure location.

For detailed steps and API options, see [Export, import, and refresh a project](./manage-knowledge-base.md#export-import-and-refresh-a-project).

## Import a project

1. Open the target CQA fine-tuning task in Microsoft Foundry.
1. Start the import operation and select the previously exported package.
1. Validate imported sources and settings before deployment.

For detailed steps and API options, see [Import a project programmatically](./manage-knowledge-base.md#import-a-project-programmatically).

## Next steps

* [Export, import, and refresh a project](./manage-knowledge-base.md#export-import-and-refresh-a-project)
* [Create, test, and deploy a CQA knowledge base](./create-test-deploy.md)
