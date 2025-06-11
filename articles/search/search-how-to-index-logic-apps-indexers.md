---
title: Connect to Azure Logic Apps
titleSuffix: Azure AI Search
description: Use an Azure Logic Apps workflow for indexer-based indexing in Azure AI Search.
author: HeidiSteen
ms.author: heidist
manager: nitinme
ms.date: 05/19/2025
ms.service: azure-ai-search
ms.topic: how-to
ms.custom:
  - references_regions
  - build-2025
---

# Use an Azure Logic Apps workflow for indexer-based indexing in Azure AI Search

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

Support for Azure Logic Apps integration is now in public preview, available in the Azure portal [Import and vectorize data wizard](search-get-started-portal-import-vectors.md) only. In Azure AI Search, a logic app workflow is used for indexing and vectorization, and it's equivalent to an indexer and data source in Azure AI Search. 

You can create a workflow in Azure AI Search using the Import and vectorize data wizard, and then manage the workflow in Azure Logic Apps alongside your other workflows. Behind the scenes, the wizard follows a workflow template that pulls in (ingests) content from a source for indexing in AI Search. The connectors used in this scenario are prebuilt and already exist in Azure Logic Apps, so the workflow template just provides details for those connectors to create connections to the data source, AI Search, and other items to complete the ingestion workflow. 

> [!NOTE]
> A logic app workflow is a billable resource. For more information, see [Azure Logic Apps pricing](/azure/logic-apps/logic-apps-pricing).

## Key features

Azure Logic Apps integration in Azure AI Search adds support for:

+ More data sources from Microsoft and other providers
+ Integrated vectorization
+ Scheduled or on-demand indexing
+ Change detection of new and existing documents

Import and vectorize data wizard inputs include:

+ A supported data source
+ A supported text embedding model

After the wizard completes, you have the following components:

| Component | Location | Description |
|-----------|----------|------------|
| Search index | Azure AI Search | Contains indexed content from a supported Logic Apps connector. The index schema is a default index created by the wizard. You can add extra elements, such as scoring profile or semantic configuration, but you can't change existing fields. You view, manage, and access the search index on Azure AI Search. |
| Logic app resource and workflow | Azure Logic Apps | You can view the running workflow, or you can open the designer in Azure Logic Apps to edit the workflow, as you regularly do if you'd started from Azure Logic Apps instead. You can edit and extend the workflow, but exercise caution so as to not break the indexing pipeline. The workflow created by the wizard uses the **Consumption** hosting option. |
| Logic app templates | Azure Logic Apps | Up to two templates created per workflow: one for on-demand indexing, and a second template for scheduled indexing. You can modify the indexing schedule in the **Index multiple documents** step of the workflow. |

## Prerequisites

Review the following requirements before you start:

+ You must be an **Owner** or **Contributor** in your Azure subscription, with permissions to create resources.

+ Azure AI Search, Basic pricing tier or higher if you want to use a search service identity for connections to an Azure data source, otherwise you can use any tier, subject to tier limits. 

+ Azure OpenAI, with a [supported embedding model](#supported-models) deployment. Vectorization is integrated into the workflow. If you don't need vectors, you can ignore the fields or try another indexing strategy.

+ Azure Logic Apps is a [supported region](#supported-regions). It should have a [system-assigned managed identity](/azure/logic-apps/authenticate-with-managed-identity) if you want to use Microsoft Entra ID authentication on connections rather than API keys.

### Supported regions

End-to-end functionality is available in the following regions, which provide the data source connection, document cracking, document chunks, support for Azure OpenAI embedding models, and the Azure AI indexer support for pulling the data. The following regions for Azure Logic Apps provide the `ParseDocument` action upon which Azure AI Search integration is based.

+ East US
+ East US 2
+ South Central US
+ West US 2
+ West US 3
+ Brazil South
+ Australia East
+ East Asia
+ Southeast Asia
+ North Europe
+ Sweden Central
+ UK South

### Supported models

The logic app path through the **Import and vectorize data** wizard supports a selection of embedding models.
Deploy one of the following [embedding models](/azure/ai-services/openai/concepts/models#embeddings) on Azure OpenAI for your end-to-end workflow.

+ text-embedding-3-small
+ text-embedding-3-large
+ text-embedding-ada-002

### Supported connectors

The following connectors are useful for indexing unstructured data, as a complement to classic indexers that primarily target structured data. 

+ [SharePoint](/connectors/sharepointonline/)
+ [OneDrive](/connectors/onedrive/)
+ [OneDrive for Business](/connectors/onedriveforbusiness/)
+ [Azure File Storage](/connectors/azurefile/)
+ [Azure Queues](/connectors/azurequeues/)
+ [Service Bus](/connectors/servicebus/)

## Limitations

Currently, the public preview has these limitations:

+ The search index is generated using a fixed schema (document ID, content, and vectorized content), with text extraction only. You can [modify the index](#modify-existing-objects) as long as the update doesn't affect existing fields.
+ Vectorization supports text embedding only.
+ Deletion detection isn't supported. You must manually [delete orphaned documents](search-howto-reindex.md#delete-orphan-documents) from the index.
+ Duplicate documents in the search index are a known issue in this preview. Consider deleting objects and starting over if this becomes an issue.
+ No support for private endpoints in the logic app workflow created by the portal wizard. The workflow is hosted using the [**Consumption** hosting option](/azure/logic-apps/single-tenant-overview-compare) and is subject to its constraints. To use the **Standard** hosting option, use a programmatic approach to creating the workflow. Use the [2025-05-01-preview REST API](/rest/api/searchservice/operation-groups?view=rest-searchservice-2025-05-01-preview&preserve-view=true) or a prerelease Azure SDK package that provides the feature.

## Create a logic app workflow

Follow these steps to create a logic app workflow for indexing content in Azure AI Search.

1. Start the Import and vectorize data wizard in the Azure portal.

1. Choose a [supported Azure Logic Apps indexer](#supported-connectors).

   :::image type="content" source="media/logic-apps-connectors/choose-data-source.png" alt-text="Screenshot of the chosen data source page in the Import and vectorize data wizard." lightbox="media/logic-apps-connectors/choose-data-source.png" :::

1. In **Connect to your data**, provide a name prefix used for the search index and workflow. Having a common name helps you manage them together.

1. Specify the indexing frequency. If you choose on a schedule, a template that includes a scheduling option is used to create the workflow. You can modify the indexing schedule in the **Index multiple documents** step of the workflow after it's created.

1. Select an authentication type where the logic app workflow connects to the search engine and starts the indexing process. The workflow can connect using  [Azure AI Search API keys](search-security-api-keys.md) or the wizard can create a role assignment that grants permissions to the Logic Apps system-assigned managed identity, assuming one exists.

1. Select **Next** to continue to the next page.

1. In **Vectorize your text**, provide the model deployment and Azure OpenAI connection information. Choose the subscription and service, a [supported text embedding model](#supported-models), and the authentication type that the workflow uses to connect to Azure OpenAI.

1. Select **Next** to continue to the next page. Review the configuration.
 
1. Select **Create** to begin processing.

   The workflow runs as a serverless workflow in Logic Apps (Consumption), separate from the AI Search service.  

1. Confirm index creation in the Azure portal, in the **Indexes** page in Azure AI Search. [Search Explorer](search-explorer.md) is the first tab. Select **Search** to return some content.

## Modify existing objects

You can make the following modifications to a search index without breaking indexing:

+ [Add scoring profiles](index-add-scoring-profiles.md)
+ [Add semantic ranking](semantic-how-to-configure.md)
+ [Add spell check](speller-how-to-add.md)
+ [Add synonym maps](search-synonyms.md)
+ [Add suggesters](index-add-suggesters.md)

You can make the following updates to a workflow without breaking indexing:

+ Modify **List files in folder** to change the number of documents sent to indexing.
+ Modify **Chunk Text** to vary token inputs. The recommended token size is 512 tokens for most scenarios.
+ Modify **Chunk Text** to add a page overlap length.
+ Modify **Index multiple documents** step to control indexing frequency if you chose scheduled indexing in the wizard.

In logic apps designer, review the workflow and each step in the indexing pipeline. The workflow specifies document extraction, default document chunking ([Text Split skill](cognitive-search-skill-textsplit.md)), embedding ([Azure OpenAI embedding skill](cognitive-search-skill-azure-openai-embedding.md)), output field mappings, and finally indexing.

:::image type="content" source="media/logic-apps-connectors/logic-app-workflow.png" alt-text="Screenshot of the workflow in logic app designer." lightbox="media/logic-apps-connectors/logic-app-workflow.png" :::

## Template and workflow management

The wizard creates templates and workflows when you specify a Logic Apps indexer. To create and manage them, including template deletion, use the logic app designer. The Azure portal search service dashboard doesn't provide template or workflow management, and currently there's no programmatic support in Azure AI Search APIs.

## Related content

+ [Indexers](search-indexer-overview.md)

+ [Connect to Azure AI services from workflows in Azure Logic Apps](/azure/logic-apps/connectors/azure-ai)

+ [Manage logic apps](/azure/logic-apps/manage-logic-apps-with-azure-portal)
