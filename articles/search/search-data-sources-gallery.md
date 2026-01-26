---
title: Data sources gallery
titleSuffix: Azure AI Search
description: Lists data source connectors for importing into an Azure AI Search index.
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search
ms.update-cycle: 180-days
ms.custom:
  - ignite-2023
ms.topic: concept-article
ms.date: 10/21/2025
---

# Data sources gallery

Find a data connector from Microsoft or a partner that works with [an indexer](search-indexer-overview.md) to simplify data ingestion into a search index.

> [!NOTE]
> The connectors mentioned in this article represent one method for indexing data in Azure AI Search. You also have the option of developing your own connector using the [Push REST API or An Azure SDK](search-what-is-data-import.md#pushing-data-to-an-index).

<a name="ga"></a>

## Generally available data sources by Azure AI Search

Pull in content from other Azure services using indexers and the following data source connectors.

:::row:::
:::column span="":::

---

### Azure Blob Storage

By [Azure AI Search](search-what-is-azure-search.md)

Extract blob metadata and content, serialized into JSON documents, and imported into a search index as search documents. Set properties in both data source and indexer definitions to optimize for various blob content types. Change detection is supported automatically.

[More details](search-how-to-index-azure-blob-storage.md)

:::image type="icon" source="media/search-data-sources-gallery/azure_storage.png":::

:::column-end:::
:::column span="":::

---

### Azure Table Storage

By [Azure AI Search](search-what-is-azure-search.md)

Extract rows from an Azure Table, serialized into JSON documents, and imported into a search index as search documents. 

[More details](search-how-to-index-azure-tables.md)

:::image type="icon" source="media/search-data-sources-gallery/azure_storage.png":::

:::column-end:::
:::column span="":::

---

### Azure Data Lake Storage Gen2

By [Azure AI Search](search-what-is-azure-search.md)

Connect to Azure Storage through Azure Data Lake Storage Gen2 to extract content from a hierarchy of directories and nested subdirectories.

[More details](search-how-to-index-azure-data-lake-storage.md)

:::image type="icon" source="media/search-data-sources-gallery/azure_storage.png":::

:::column-end:::
:::row-end:::
:::row:::
:::column span="":::

   :::column-end:::
   :::column span="":::
   :::column-end:::

:::row-end:::

:::row:::
:::column span="":::

---

### Azure Cosmos DB for NoSQL

By [Azure AI Search](search-what-is-azure-search.md)

Connect to Azure Cosmos DB through the SQL API to extract items from a container, serialized into JSON documents, and imported into a search index as search documents. Configure change tracking to refresh the search index with the latest changes in your database.

[More details](search-how-to-index-cosmosdb-sql.md)

:::image type="icon" source="media/search-data-sources-gallery/azure_cosmos_db_logo_small.png":::

:::column-end:::
:::column span="":::

---

### Azure SQL Database

By [Azure AI Search](search-what-is-azure-search.md)

Extract field values from a single table or view, serialized into JSON documents, and imported into a search index as search documents. Configure change tracking to refresh the search index with the latest changes in your database.

[More details](search-how-to-index-sql-database.md)

:::image type="icon" source="media/search-data-sources-gallery/azuresqlconnectorlogo_medium.png":::

:::column-end:::
:::column span="":::

---

### Microsoft OneLake files

By [Azure AI Search](search-how-to-index-onelake-files.md)

Connect to a OneLake lakehouse to extract supported files content from a hierarchy of directories and nested subdirectories.

[More details](search-how-to-index-onelake-files.md)

:::image type="icon" source="media/search-data-sources-gallery/fabric_onelake_logo.png":::

:::column-end:::
:::row-end:::
:::row:::
:::column span="":::

   :::column-end:::
   :::column span="":::
   :::column-end:::

:::row-end:::

---

## Logic app connectors

Pull in content [using logic app workflows](search-how-to-index-logic-apps.md) and the following supported data sources. Note that the Logic Apps artifacts mentioned below, they have a pre-built workflow, however, you can use [any connectors listed under Logic Apps](/connectors/connector-reference/connector-reference-logicapps-connectors) that pull data from sources and create your own indexing pipeline workflow that pushes data to [Azure AI Search via a Logic App connector](/azure/logic-apps/connectors/azure-ai#azure-ai-search).

:::row:::
:::column span="":::

---

### SharePoint

By [Logic Apps](/connectors/sharepointonline)

SharePoint helps organizations share and collaborate with colleagues, partners, and customers. You can connect to SharePoint in Microsoft 365 or to an on-premises SharePoint 2016 or 2019 farm using the On-Premises Data Gateway to manage documents and list items.

[More details](search-how-to-index-logic-apps.md#supported-connectors)

:::image type="icon" source="media/search-data-sources-gallery/sharepoint_online_logo.png":::

:::column-end:::
:::column span="":::

---

### OneDrive

By [Logic Apps](/connectors/onedrive/)

Connect to OneDrive to manage your files. You can perform various actions such as upload, update, get, and delete on files in OneDrive.

[More details](search-how-to-index-logic-apps.md#supported-connectors)

:::column-end:::
:::column span="":::

---

### OneDrive for Business

By [Logic Apps](/connectors/onedriveforbusiness/)

OneDrive for Business is a cloud storage, file hosting service that allows users to sync files and later access them from a web browser or mobile device. Connect to OneDrive for Business to manage your files. You can perform various actions such as upload, update, get, and delete files.

[More details](search-how-to-index-logic-apps.md#supported-connectors)

:::column-end:::
:::row-end:::
:::row:::
:::column span="":::

   :::column-end:::
   :::column span="":::
   :::column-end:::

:::row-end:::

:::row:::
:::column span="":::

---

### Azure File Storage

By [Logic Apps](/connectors/azurefile/)

Microsoft Azure Storage provides a massively scalable, durable, and highly available storage for data on the cloud, and serves as the data storage solution for modern applications. Connect to File Storage to perform various operations such as create, update, get and delete on files in your Azure Storage account.

[More details](search-how-to-index-logic-apps.md#supported-connectors)

<!-- :::image type="icon" source="media/search-data-sources-gallery/sharepoint_online_logo.png"::: -->

:::column-end:::
:::column span="":::

---

### Azure Queues

By [Logic Apps](/connectors/azurequeues/)

Azure Queue storage provides cloud messaging between application components. Queue storage also supports managing asynchronous tasks and building process work flows.

[More details](search-how-to-index-logic-apps.md#supported-connectors)

<!-- :::image type="icon" source="media/search-data-sources-gallery/azure_mysql.png"::: -->

:::column-end:::
:::column span="":::

---

### Service Bus

By [Logic Apps](/connectors/servicebus/)

Connect to Azure Service Bus to send and receive messages. You can perform actions such as send to queue, send to topic, receive from queue, receive from subscription, etc.

[More details](search-how-to-index-logic-apps.md#supported-connectors)

<!-- :::image type="icon" source="media/search-data-sources-gallery/azure_storage.png"::: -->

:::column-end:::
:::row-end:::
:::row:::
:::column span="":::

   :::column-end:::
   :::column span="":::
   :::column-end:::

:::row-end:::

---

<a name="preview"></a>

## Preview data sources by Azure AI Search

New data sources are issued as preview features. [Sign up](https://aka.ms/azure-cognitive-search/indexer-preview) to get started.

:::row:::
:::column span="":::

---

### Azure Files

By [Azure AI Search](search-what-is-azure-search.md)

Connect to Azure Storage through Azure Files share to extract content serialized into JSON documents, and imported into a search index as search documents.

[More details](search-file-storage-integration.md)

:::image type="icon" source="media/search-data-sources-gallery/azure_storage.png":::

:::column-end:::
:::column span="":::

---

### Azure Cosmos DB for Apache Gremlin

By [Azure AI Search](search-what-is-azure-search.md)

Connect to Azure Cosmos DB for Apache Gremlin to extract items from a container, serialized into JSON documents, and imported into a search index as search documents. Configure change tracking to refresh the search index with the latest changes in your database.

[More details](search-how-to-index-cosmosdb-gremlin.md)

:::image type="icon" source="media/search-data-sources-gallery/azure_cosmos_db_logo_small.png":::

:::column-end:::
:::column span="":::

---

### Azure Cosmos DB for MongoDB

By [Azure AI Search](search-what-is-azure-search.md)

Connect to Azure Cosmos DB for MongoDB to extract items from a container, serialized into JSON documents, and imported into a search index as search documents. Configure change tracking to refresh the search index with the latest changes in your database.

[More details](search-how-to-index-cosmosdb-sql.md)

:::image type="icon" source="media/search-data-sources-gallery/azure_cosmos_db_logo_small.png":::

:::column-end:::
:::row-end:::
:::row:::
:::column span="":::

   :::column-end:::
   :::column span="":::
   :::column-end:::

:::row-end:::

:::row:::
:::column span="":::

---

### SharePoint

By [Azure AI Search](search-what-is-azure-search.md)

Connect to a SharePoint site and index documents from one or more document libraries, for accounts and search services in the same tenant. Text and normalized images are extracted by default. Optionally, you can configure a skillset for more content transformation and enrichment, or configure change tracking to refresh a search index with new or changed content in SharePoint.

[More details](search-how-to-index-sharepoint-online.md)

:::image type="icon" source="media/search-data-sources-gallery/sharepoint_online_logo.png":::

:::column-end:::
:::column span="":::

---

### Azure MySQL

By [Azure AI Search](search-what-is-azure-search.md)

Connect to MySQL database on Azure to extract rows in a table, serialized into JSON documents, and imported into a search index as search documents. On subsequent runs, assuming High Water Mark change detection policy is configured, the indexer takes all changes, uploads, and delete and reflect those changes in your search index.

[More details](search-how-to-index-mysql.md)

:::image type="icon" source="media/search-data-sources-gallery/azure_mysql.png":::

:::column-end:::
:::column span="":::

---

:::column-end:::
:::row-end:::
:::row:::
:::column span="":::

   :::column-end:::
   :::column span="":::
   :::column-end:::

:::row-end:::

---

<a name="partners"></a>

## Data sources from our partners

The following Microsoft partners offer custom third-party data connectors. Each partner implements and supports these connectors, which aren't part of Azure AI Search built-in indexers. Before you use a custom connector, review the partner's licensing and usage instructions.

+ [BA Insight](https://www.bainsight.com)

+ [RheinInsights](https://www.rheininsights.com/)

+ [ServiceNow](https://www.servicenow.com)
