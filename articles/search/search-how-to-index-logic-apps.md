---
title: Connect to Azure Logic Apps
titleSuffix: Azure AI Search
description: Use an Azure Logic Apps workflow for automated indexing in Azure AI Search.
author: HeidiSteen
ms.author: heidist
manager: nitinme
ms.date: 01/23/2026
ms.service: azure-ai-search
ms.topic: how-to
ms.custom:
  - references_regions
  - build-2025
---

# Use an Azure Logic Apps workflow for automated indexing in Azure AI Search

In Azure AI Search, you can use the [**Import data (new)** wizard](search-get-started-portal-import-vectors.md) in the Azure portal to create a logic app workflow that indexes and vectorizes your content. This capability is equivalent to an [indexer](search-indexer-overview.md) and data source that generates an indexing pipeline and creates searchable content.

After you create a workflow in the wizard, you can manage the workflow in Azure Logic Apps alongside your other workflows. Behind the scenes, the wizard follows a workflow template that pulls in (ingests) content from a source for indexing in AI Search. The connectors used in this scenario are prebuilt and already exist in Azure Logic Apps, so the workflow template just provides details for those connectors to create connections to the data source, AI Search, and other items to complete the ingestion workflow. 

## Key features

Azure Logic Apps integration in Azure AI Search adds support for:

+ [More data sources](search-data-sources-gallery.md) from Microsoft and other providers
+ Integrated vectorization
+ Scheduled or on-demand indexing
+ Change detection of new and existing documents

The **Import data (new)** wizard inputs include:

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

> [!NOTE]
> A logic app workflow is a billable resource. For more information, see [Azure Logic Apps pricing](/azure/logic-apps/logic-apps-pricing).

### Supported regions

End-to-end functionality is available in the following regions, which provide the data source connection, document cracking, document chunks, support for Azure OpenAI embedding models, and the built-in indexing support for pulling the data. The following regions for Azure Logic Apps provide the `ParseDocument` action upon which indexing integration is based.

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

The logic app path through the **Import data (new)** wizard supports a selection of embedding models.

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

### Supported actions

Logic apps integration includes the following indexing actions. For more information, see [Connect to Foundry Tools from workflows in Azure Logic Apps](/azure/logic-apps/connectors/azure-ai#ingest-data-workflow).

+ Check for new data.
+ Get the data. An HTTP action that retrieves the uploaded document using the file URL from the trigger output.
+ Compose document details. A Data Operations action that concatenates various items.
+ Create token string. A Data Operations action that produces a token string using the output from the Compose action.
+ Create content chunks. A Data Operations action that splits the token string into pieces, based on either the number of characters or tokens per content chunk.
+ Convert tokenized data to JSON. A Data Operations action that converts the token string chunks into a JSON array.
+ Select JSON array items. A Data Operations action that selects multiple items from the JSON array.
+ Generate the embeddings. An Azure OpenAI action that creates embeddings for each JSON array item.
+ Select embeddings and other information. A Data Operations action that selects embeddings and other document information.
+ Index the data. An Azure AI Search action that indexes the data based on each selected embedding.

It also supports the following query actions:

+ Wait for input prompt. A trigger that either polls or waits for new data to arrive, either based on a scheduled recurrence or in response to specific events respectively.
+ Input system message for the model. A Data Operations action that provides input to train the model.
+ Input sample questions and responses. A Data Operations action that provides sample customer questions and associated roles to train the model.
+ Input system message for search query. A Data Operations action that provides search query input to train the model.
+ Generate search query. An Inline Code action that uses JavaScript to create a search query for the vector store, based on the outputs from the preceding Compose actions.
+ Convert query to embedding. An Azure OpenAI action that connects to the chat completion API, which guarantees reliable responses in chat conversations.
+ Get an embedding. An Azure OpenAI action that gets a single vector embedding.
+ Search the vector database. An Azure AI Search action that executes searches in the vector store.
+ Create prompt. An Inline Code action that uses JavaScript to build prompts.
+ Perform chat completion. An Azure OpenAI action that connects to the chat completion API, which guarantees reliable responses in chat conversations.
+ Return a response. A Request action that returns the results to the caller when you use the Request trigger.

## Limitations

+ The search index is generated using a fixed schema (document ID, content, and vectorized content), with text extraction only. You can [modify the index](#modify-existing-objects) as long as the update doesn't affect existing fields.
+ Vectorization supports text embedding only.
+ Deletion detection isn't supported. You must manually [delete orphaned documents](search-how-to-delete-documents.md#delete-a-single-document) from the index.
+ Duplicate documents in the search index are a known issue in this preview. Consider deleting objects and starting over if this becomes an issue.
+ No support for private endpoints in the logic app workflow created by the portal wizard. The workflow is hosted using the [**Consumption** hosting option](/azure/logic-apps/single-tenant-overview-compare) and is subject to its constraints. To use the **Standard** hosting option, use a programmatic approach to creating the workflow.

## Create a logic app workflow

Follow these steps to create a logic app workflow for indexing content in Azure AI Search.

1. Start the **Import data (new)** wizard in the Azure portal.

1. Choose a [supported Azure Logic Apps connector](#supported-connectors).

   :::image type="content" source="media/logic-apps-connectors/choose-data-source.png" alt-text="Screenshot of the chosen data source page in the Import data (new) wizard." lightbox="media/logic-apps-connectors/choose-data-source.png" :::

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

+ [Connect to Foundry Tools from workflows in Azure Logic Apps](/azure/logic-apps/connectors/azure-ai)

+ [Manage logic apps](/azure/logic-apps/manage-logic-apps-with-azure-portal)
