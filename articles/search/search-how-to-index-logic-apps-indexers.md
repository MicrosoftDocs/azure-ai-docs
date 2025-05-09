---
title: Connect to Logic Apps
titleSuffix: Azure AI Search
description: Use a Logic Apps workflow for indexer-based indexing in Azure AI Search.
manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search
ms.custom: references_regions
ms.topic: how-to
ms.date: 05/15/2025
---

# Use a Logic Apps workflow for indexer-based indexing in Azure AI Search

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

Support for Logic Apps integration is now in public preview, available in the Azure portal [Quickstart wizard](search-get-started-portal-import-vectors.md) only.

A Logic apps workflow is equivalent to an indexer in Azure AI Search, inclusive of both the data source and indexer definition. Logic Apps integration adds support for more data sources, and extends to Azure OpenAI models for vectorizing data during indexing.

You can create a workflow in Azure AI Search using the Quickstart wizard, and then manage it in Logic Apps alongside your other workflows. Behind the scenes, the wizard follows a workflow template that pulls in (ingests) content from a source for indexing in AI Search. The connectors used in this scenario are prebuilt and already exist in Azure Logic Apps, so the workflow template just provides details for those connectors to create connections to the data source, AI Search, and other items to complete the ingestion workflow. 

After you're done with the wizard, you've got a logic app resource and workflow that's live and running. You can view the running workflow, or you can open the designer in Azure Logic Apps to edit the workflow, as you regularly do if you'd started from Azure Logic Apps instead.

Logic Apps workflows are a billable resource. For more information, see [Azure Logic Apps pricing](/azure/logic-apps/logic-apps-pricing).

## Key features

The Quickstart wizard generates a Logic Apps template one each for on-demand or scheduled indexing, and a search index. This capability provides:

+ Support for more data sources
+ Integrated vectorization
+ Scheduled or on-demand indexing

## Supported regions

End-to-end functionality is available in the following regions, which provide the data source connection, document cracking, document chunks, support for Azure OpenAI embedding models, and the Azure AI indexer support for pulling the data:

+ Australia East
+ Brazil South
+ South Central US
+ East US
+ East US 2
+ East Asia
+ North Europe
+ Southeast Asia
+ Sweden Central
+ UK South
+ West US 2
+ West US 3

## Create a Logic Apps workflow

Follow these steps to create a Logic Apps workflow for indexing content in Azure AI Search.

1. Start the Quickstart wizard in the Azure portal.

1. Choose a Logic Apps indexer.

   :::image type="content" source="media/logic-apps-connectors/choose-data-source.png" alt-text="Screenshot of the choose data source page in the Quickstart wizard." lightbox="media/logic-apps-connectors/choose-data-source.png" :::

## Template management

Templates are created by the wizard when you specify a Logic Apps indexer. To create and manage templates, including template deletion, do this through Logic Apps. The Azure portal search service dashboard doesn't provide template management, and currently there's no programmatic support in Azure AI Search APIs.

## Related content

+ [Indexers](search-indexer-overview.md)

