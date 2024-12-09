---
title: Data sources gallery
titleSuffix: Azure AI Search
description: Lists data source connectors for importing into an Azure AI Search index.
author: HeidiSteen
ms.author: heidist

ms.service: azure-ai-search
ms.custom:
  - ignite-2023
ms.topic: conceptual
ms.date: 09/04/2024
---

# Data sources gallery

Find a data connector from Microsoft or a partner that works with [an indexer](search-indexer-overview.md) to simplify data ingestion into a search index. This article has the following sections:

+ [Generally available data sources by Azure AI Search](#ga)
+ [Preview data sources by Azure AI Search](#preview)
+ [Data sources from our Partners](#partners)


> [!NOTE]
> The connectors mentioned in this article don't represent the only methods for indexing data from data sources to AI Search, but low/no-code options to accomplish this task. You have the option to develop your own connector utilizing the [Push REST API/SDK](search-what-is-data-import.md#pushing-data-to-an-index). This implies that provided you can programmatically extract data from a source, you can also employ the corresponding programmatic Push method to index your data.


<a name="ga"></a>

## Generally available data sources by Azure AI Search

Pull in content from other Azure services using indexers and the following data source connectors. 

:::row:::
:::column span="":::

---

### Azure Blob Storage

By [Azure AI Search](search-what-is-azure-search.md)

Extract blob metadata and content, serialized into JSON documents, and imported into a search index as search documents. Set properties in both data source and indexer definitions to optimize for various blob content types. Change detection is supported automatically.

[More details](search-howto-indexing-azure-blob-storage.md)

:::image type="icon" source="media/search-data-sources-gallery/azure_storage.png":::

:::column-end:::
:::column span="":::

---

### Azure Cosmos DB for NoSQL

By [Azure AI Search](search-what-is-azure-search.md)

Connect to Azure Cosmos DB through the SQL API to extract items from a container, serialized into JSON documents, and imported into a search index as search documents. Configure change tracking to refresh the search index with the latest changes in your database.

[More details](search-howto-index-cosmosdb.md)

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

### Azure Table Storage

By [Azure AI Search](search-what-is-azure-search.md)

Extract rows from an Azure Table, serialized into JSON documents, and imported into a search index as search documents. 

[More details](search-howto-indexing-azure-tables.md)

:::image type="icon" source="media/search-data-sources-gallery/azure_storage.png":::

:::column-end:::
:::column span="":::

---

### Azure Data Lake Storage Gen2

By [Azure AI Search](search-what-is-azure-search.md)

Connect to Azure Storage through Azure Data Lake Storage Gen2 to extract content from a hierarchy of directories and nested subdirectories.

[More details](search-howto-index-azure-data-lake-storage.md)

:::image type="icon" source="media/search-data-sources-gallery/azure_storage.png":::

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

<a name="preview"></a>

## Preview data sources by Azure AI Search

New data sources are issued as preview features. [Sign up](https://aka.ms/azure-cognitive-search/indexer-preview) to get started.

:::row:::
:::column span="":::

---

### Fabric OneLake files

By [Azure AI Search](search-how-to-index-onelake-files.md)

Connect to a OneLake lakehouse to extract supported files content from a hierarchy of directories and nested subdirectories.

[More details](search-how-to-index-onelake-files.md)

:::image type="icon" source="media/search-data-sources-gallery/fabric_onelake_logo.png":::

:::column-end:::
:::column span="":::

---


### Azure Cosmos DB for Apache Gremlin

By [Azure AI Search](search-what-is-azure-search.md)

Connect to Azure Cosmos DB for Apache Gremlin to extract items from a container, serialized into JSON documents, and imported into a search index as search documents. Configure change tracking to refresh the search index with the latest changes in your database.

[More details](search-howto-index-cosmosdb-gremlin.md)

:::image type="icon" source="media/search-data-sources-gallery/azure_cosmos_db_logo_small.png":::

:::column-end:::
:::column span="":::

---

### Azure Cosmos DB for MongoDB

By [Azure AI Search](search-what-is-azure-search.md)

Connect to Azure Cosmos DB for MongoDB to extract items from a container, serialized into JSON documents, and imported into a search index as search documents. Configure change tracking to refresh the search index with the latest changes in your database.

[More details](search-howto-index-cosmosdb.md)

:::image type="icon" source="media/search-data-sources-gallery/azure_cosmos_db_logo_small.png":::

:::column-end:::
:::column span="":::

---

### SharePoint

By [Azure AI Search](search-what-is-azure-search.md)

Connect to a SharePoint site and index documents from one or more document libraries, for accounts and search services in the same tenant. Text and normalized images are extracted by default. Optionally, you can configure a skillset for more content transformation and enrichment, or configure change tracking to refresh a search index with new or changed content in SharePoint.

[More details](search-howto-index-sharepoint-online.md)

:::image type="icon" source="media/search-data-sources-gallery/sharepoint_online_logo.png":::

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

### Azure MySQL

By [Azure AI Search](search-what-is-azure-search.md)

Connect to MySQL database on Azure to extract rows in a table, serialized into JSON documents, and imported into a search index as search documents. On subsequent runs, assuming High Water Mark change detection policy is configured, the indexer takes all changes, uploads, and delete and reflect those changes in your search index.

[More details](search-howto-index-mysql.md)

:::image type="icon" source="media/search-data-sources-gallery/azure_mysql.png":::

:::column-end:::
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

## Data sources from our Partners

Data source connectors are also provided by third-party Microsoft partners. See our [Terms of Use statement](search-data-sources-terms-of-use.md) and check the partner licensing and usage instructions before using a data source. These third-party Microsoft Partner data source connectors are implemented and supported by each partner and are not part of Azure AI Search built-in indexers. 

:::row:::
:::column span="":::

---

### Aderant

By [BA Insight](https://www.bainsight.com/)

The Aderant connector honors the security of the source system and provides both full and incremental crawls, so the users have the latest information available to them all the time.

[More details](https://www.bainsight.com/connectors/aderant-connector-sharepoint-azure-elasticsearch/)

:::column-end:::
:::column span="":::

---

### Adobe AEM

By [Accenture](https://www.accenture.com)

Allows your company to crawl content from the Adobe Experience Manager server, providing connection throttling and expected values or patterns filtering.

[More details](https://contentanalytics.digital.accenture.com/display/aspire40/AEM+Connector)

:::column-end:::
:::column span="":::

---

### Adobe AEM

By [BA Insight](https://www.bainsight.com/)

The Adobe Experience Manager connector enables indexing of content managed by the Adobe Experience Manager (AEM) platform and supports both Full and Incremental crawling to ensure index freshness.

[More details](https://www.bainsight.com/connectors/adobe-em-connector-for-sharepoint-azure-elasticsearch/)

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

### Adobe AEM

By [Raytion](https://www.raytion.com/contact)

Secure enterprise search connector for reliably indexing content from the Adobe Active Experience Manager (AEM) and intelligently searching it with Azure AI Search. It robustly indexes pages, attachments, and other generated document types from Adobe AEM in near real time. The connector fully supports Adobe AEM’s permission model, its built-in user and group management, and AEM installations based on Microsoft Entra ID or other directory services.

[More details](https://www.raytion.com/connectors/adobe-experience-manager-aem)

:::column-end:::
:::column span="":::

---

### Alfresco

By [BA Insight](https://www.bainsight.com/)

The Alfresco Connector is built on the BAI connector framework, which is the platform used to build all our connectors and provides secure connectivity to enterprise systems.

[More details](https://www.bainsight.com/connectors/alfresco-connector-sharepoint-azure-elasticsearch/)

:::column-end:::
:::column span="":::

---

### Alfresco

By [Raytion](https://www.raytion.com/contact)

Secure enterprise search connector for reliably indexing content from Alfresco One and intelligently searching it with Azure AI Search. It robustly indexes files, folders, and user profiles from Alfresco One in near real time. The connector fully supports Alfresco One’s permission model, its built-in user and group management, and Alfresco One installations based on Microsoft Entra ID and other directory services.

[More details](https://www.raytion.com/connectors/raytion-alfresco-connector)

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

### Amazon Aurora

By [BA Insight](https://www.bainsight.com/)

The Amazon Aurora Connector is built upon industry standard database access methods, so it equally supports databases from other systems such as Oracle, MySQL, and IBM DB2.

[More details](https://www.bainsight.com/connectors/amazon-aurora-connector-sharepoint-azure-elasticsearch/)

:::column-end:::
:::column span="":::

---

### Amazon RDS

By [BA Insight](https://www.bainsight.com/)

The Amazon RDS Connector is built upon industry standard database access methods, so it can equally support databases from other systems such as Oracle, MySQL, and IBM DB2.

[More details](https://www.bainsight.com/connectors/amazon-rds-connector-sharepoint-azure-elasticsearch/)

:::column-end:::
:::column span="":::

---

### Amazon S3

By [BA Insight](https://www.bainsight.com/)

The Amazon S3 Connector works with all content stored in S3. Your organization can use the connector to securely connect to S3 and index content from S3 buckets. Powerful filtering capabilities give your organization control about what content found in S3 should be indexed.

[More details](https://www.bainsight.com/connectors/amazon-s3-connector-sharepoint-azure-elasticsearch/)

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

### Aspider

By [Accenture](https://www.accenture.com)

The Aspider connector allows crawling of content from web sites, using HTTP Authentication, incremental crawls, connection throttling, distributed and HTTPS crawling, among other features.

[More details](https://contentanalytics.digital.accenture.com/display/aspire40/Aspider+Web+Crawler)

:::column-end:::
:::column span="":::

---

### Atlassian Confluence (Cloud)

By [BA Insight](https://www.bainsight.com/)

Our Confluence (Cloud Version) Connector is an enterprise grade indexing connector that enables content stored in Confluence to be crawled and indexed.

[More details](https://www.bainsight.com/connectors/connector-for-confluence-cloud-version/)

:::column-end:::
:::column span="":::

---

<a name='azure-ad'></a>

### Microsoft Entra ID

By [BA Insight](https://www.bainsight.com)

The BA Insight Microsoft Entra Connector makes it possible to surface content from your Microsoft Entra tenancy into a single consolidated search index, along with content from other repositories, making searches such as employee look-up or expertise locator a reality.

[More details](https://www.bainsight.com/connectors/azure-active-directory-connector-for-sharepoint-azure-elasticsearch/)

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

<a name='azure-ad'></a>

### Microsoft Entra ID

By [Raytion](https://www.raytion.com/contact)

Secure enterprise search connector for reliably indexing content from Microsoft Entra ID and intelligently searching it with Azure AI Search. It indexes objects from Microsoft Entra ID via the Microsoft Graph API. The connector can be used for ingesting principals into Azure AI Search in near real time to implement use cases like expert search, equipment search, and location search or to provide early-binding security trimming with custom data sources. The connector supports federated authentication against Microsoft 365.

[More details](https://www.raytion.com/connectors/raytion-azure-ad-connector)

:::column-end:::
:::column span="":::

---

### Azure blobs

By [Accenture](https://www.accenture.com)

Provides the ability to crawl content from an Azure Blob container, allowing incremental crawling, document level security, and access to folders and subfolders.

[More details](https://contentanalytics.digital.accenture.com/display/aspire40/Azure+Blob+Storage+Connector)

:::column-end:::
:::column span="":::

---

### Azure Data Lake

By [Accenture](https://www.accenture.com)

The Azure Data Lake connector crawls content from the Azure Data Lake Store cloud at either root or specified paths, with incremental crawling, fetching objects ACLs, OAuth 2 authentication and more.

[More details](https://contentanalytics.digital.accenture.com/display/aspire40/Azure+Data+Lake+Connector)

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

### Azure Events Hub

By [Accenture](https://www.accenture.com)

Crawls content from an Azure event hub, allowing incremental crawling and retrieval of any type of event or attributes.

[More details](https://contentanalytics.digital.accenture.com/display/aspire40/Azure+Events+Hub+Connector)

:::column-end:::
:::column span="":::

---

### Azure SQL Database

By [BA Insight](https://www.bainsight.com/)

BA Insight’s Azure SQL Database Connector honors the security of the source database and provides both full and incremental crawls so that users have the latest information available to them all of the time.

[More details](https://www.bainsight.com/connectors/azure-sql-database-connector-sharepoint-azure-elasticsearch/)

:::column-end:::
:::column span="":::

---

### Bentley

By [BA Insight](https://www.bainsight.com/)

The BAI Bentley AssetWise Connector makes it possible to surface content from AssetWise into a single consolidated search index, along with content from other repositories.

[More details](https://www.bainsight.com/connectors/bentley-connector-for-sharepoint-azure-elasticsearch/)

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

### Box

By [Accenture](https://www.accenture.com)

The Box connector crawls content from a Box repository. The connector retrieves the supported elements via the REST API, providing full or incremental crawling, metadata extraction, fetching ACLs, and more.

[More details](https://contentanalytics.digital.accenture.com/display/aspire40/Box++Connector)

:::column-end:::
:::column span="":::

---

### Box

By [BA Insight](https://www.bainsight.com/)

The Box connector makes it possible to surface content from Box in SharePoint and other portals, enabling users to get integrated search results from SharePoint and Box.

[More details](https://www.bainsight.com/connectors/box-connector-sharepoint-azure-elasticsearch/)

:::column-end:::
:::column span="":::

---

### Box

By [Raytion](https://www.raytion.com/contact)

Secure enterprise search connector for reliably indexing content from Box and intelligently searching it with Azure AI Search. It robustly indexes files, folders, comments, users, groups, and tasks from Box in near real time. The connector fully supports Box’ built-in user and group management.

[More details](https://www.raytion.com/connectors/raytion-box-connector)

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

### Confluence

By [Accenture](https://www.accenture.com)

The Confluence connector crawls content from any Confluence content repository. The connector retrieves spaces, pages, blogs, attachments, and comments through a REST API, allowing incremental crawling, fetching ACLs, support for HTTP and HTTPS, and more.

[More details](https://contentanalytics.digital.accenture.com/display/aspire40/Atlassian+Confluence+Connector)

:::column-end:::
:::column span="":::

---

### Confluence

By [BA Insight](https://www.bainsight.com/)

The Confluence Connector is an enterprise grade indexing connector that enables content stored in Confluence to be crawled and indexed. This enables SharePoint, or any other portal, to serve as the single point from which users can search and retrieve the content they need from multiple content sources.

[More details](https://www.bainsight.com/connectors/confluence-connector-sharepoint-azure-elasticsearch/)

:::column-end:::
:::column span="":::

---

### Confluence

By [Raytion](https://www.raytion.com/contact)

Secure enterprise search connector for reliably indexing content from Atlassian Confluence and intelligently searching it with Azure AI Search. It robustly indexes pages, blog posts, attachments, comments, spaces, profiles, and hub sites for tags from on-premises Confluence instances in near real time. The connector fully supports Atlassian Confluence’s built-in user and group management, and Confluence installations based on Microsoft Entra ID and other directory services.

[More details](https://www.raytion.com/connectors/raytion-confluence-connector)

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

### Confluence Cloud

By [Raytion](https://www.raytion.com/contact)

Secure enterprise search connector for reliably indexing content from Atlassian Confluence Cloud and intelligently searching it with Azure AI Search. It robustly indexes pages, blog posts, attachments, comments, spaces, profiles, and hub sites for tags from Confluence Cloud instances in near real time. The connector fully supports Atlassian Confluence Cloud’s built-in user and group management.

[More details](https://www.raytion.com/connectors/raytion-confluence-cloud-connector)

:::column-end:::
:::column span="":::

---

### CuadraSTAR

By [BA Insight](https://www.bainsight.com/)

The CuadraSTAR Connector crawls content in CuadraSTAR and creates a single index that makes it possible to use Azure AI Search to find relevant information within CuadraSTAR, and over 70 other supported repositories, eliminating the need to perform separate searches.

[More details](https://www.bainsight.com/connectors/cuadrastar-connector-sharepoint-azure-elasticsearch/)

:::column-end:::
:::column span="":::

---

### Database

By [Accenture](https://www.accenture.com)

The Database Server connector crawls content from a Relational Database server, scanning all databases on the server and extracting rows and table information.

[More details](https://contentanalytics.digital.accenture.com/display/aspire40/Database+Server+Connector)

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

### Deltek

By [BA Insight](https://www.bainsight.com/)

The Deltek Vision Connector honors the security of the source system and provides both full and incremental crawls, so users always have the latest information available to them. It indexes content from Deltek Vision into Azure, SharePoint in Microsoft 365, or SharePoint 2016/2013, surfacing it through BA Insight's SmartHub to provide users with integrated search results.

[More details](https://www.bainsight.com/connectors/deltek-connector-sharepoint-azure-elasticsearch/)

:::column-end:::
:::column span="":::

---

### Documentum

By [Accenture](https://www.accenture.com)

The Aspire Documentum DQL connector crawls content from Documentum, allowing crawls based on user-defined DQL SELECT statements, incremental crawling, fetching of ACLs, group expansion of nested permissions, and more.

[More details](https://contentanalytics.digital.accenture.com/display/aspire40/Documentum+DQL+Connector)

:::column-end:::
:::column span="":::

---

### Documentum

By [BA Insight](https://www.bainsight.com/)

BA Insight's Documentum Connector securely indexes both the full text and metadata of Documentum objects into Azure AI Search, enabling a single searchable result set across content from multiple repositories. This connector is unlike some others that surface Documentum records with Azure AI Search one at a time for process management.

[More details](https://www.bainsight.com/connectors/documentum-connector-sharepoint-azure-elasticsearch/)

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

### Documentum

By [Raytion](https://www.raytion.com/contact)

Secure enterprise search connector for reliably indexing content from OpenText Documentum and intelligently searching it with Azure AI Search. It robustly indexes repositories, folders and files together with their meta data and properties from Documentum in near real time. The connector fully supports OpenText Documentum’s built-in user and group management.

[More details](https://www.raytion.com/connectors/raytion-documentum-connector)

:::column-end:::
:::column span="":::

---

### Drupal 

By [Raytion](https://www.raytion.com/contact)

Raytion's Drupal Connector indexes content from Drupal into Azure AI Search to be able to access and explore all pages and attachments published by Drupal alongside content from other corporate systems in Azure AI Search.

[More details](https://www.raytion.com/connectors/raytion-drupal-connector)

:::column-end:::
:::column span="":::

---

### Egnyte

By [BA Insight](https://www.bainsight.com/)

The Egnyte Connector supports both full and incremental crawls and indexes with high throughput.

[More details](https://www.bainsight.com/connectors/egnyte-connector-for-sharepoint-azure-elasticsearch/)

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

### Elasticsearch

By [Accenture](https://www.accenture.com)

The Elasticsearch connector crawls content from an Elasticsearch index, allowing crawling of multiple indexes, Slice support, use of Get of MGet methods for fetching content, and connection throttling.

[More details](https://contentanalytics.digital.accenture.com/display/aspire40/Elasticsearch+Connector)

:::column-end:::
:::column span="":::

---

### Elite / E3

By [BA Insight](https://www.bainsight.com/)

BA Insight's Elite Connector provides a single point of access for lawyers to access firm content and knowledge in line with Elite content using Azure AI Search.

[More details](https://www.bainsight.com/connectors/elite-connector-sharepoint-azure-elasticsearch/)

:::column-end:::
:::column span="":::

---

### EMC eRoom

By [BA Insight](https://www.bainsight.com/)

The eRoom Connector establishes a secure connection to the eRoom application and maps the content, including metadata and attachments, from the eRoom schema to the search engine schema. It then extracts content and feeds it to the search engine in a process called crawling.

[More details](https://www.bainsight.com/connectors/eroom-connector-sharepoint-azure-elasticsearch/)

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

### Facebook Workplace

By [BA Insight](https://www.bainsight.com/)

Organizations who use Workplace by Facebook can now extend the reach of this data into their existing search indexes via the BA Insight Workplace by Facebook Connector.

[More details](https://www.bainsight.com/connectors/connector-for-workplace-by-facebook/)

:::column-end:::
:::column span="":::

---

### Facebook Workplace

By [Raytion](https://www.raytion.com/contact)

Secure enterprise search connector for reliably indexing content from Facebook Workplace and intelligently searching it with Azure AI Search. It robustly indexes project groups, conversations and shared documents from Facebook Workplace in near real time. The connector fully supports Facebook Workplace’s built-in user and group management.

[More details](https://www.raytion.com/connectors/raytion-facebook-workplace-connector)

:::column-end:::
:::column span="":::
---

### File Share

By [BA Insight](https://www.bainsight.com/)

The File Share Connector makes it possible to surface content from File Shares (Windows, SMB/CIFS) in a single consolidated search index, along with content from other repositories.

[More details](https://www.bainsight.com/connectors/file-share-connector-sharepoint-azure-elasticsearch/)

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

### File System

By [Accenture](https://www.accenture.com)

The File System connector crawls content from a file system location, allowing incremental crawling, metadata extraction, filtering of documents by path, supporting Windows/Linux/macOS file systems.

[More details](https://contentanalytics.digital.accenture.com/display/aspire40/File+System+Connector)

:::column-end:::
:::column span="":::

---

### File System

By [Raytion](https://www.raytion.com/contact)

Secure enterprise search connector for reliably indexing content from locally mounted file systems and intelligently searching it with Azure AI Search. It robustly indexes files and folders from file systems in near real time.

[More details](https://www.raytion.com/connectors/raytion-file-system-connector)

:::column-end:::
:::column span="":::

---

### FirstSpirit

By [Raytion](https://www.raytion.com/contact)

Secure enterprise search connector for reliably indexing content from e-Spirit FirstSpirit and intelligently searching it with Azure AI Search. It robustly indexes pages, attachments and other generated document types from FirstSpirit in near real time. The connector fully supports e-Spirit FirstSpirit’s built-in user, group and permission management, and FirstSpirit installations based on Microsoft Entra ID and other directory services.

[More details](https://www.raytion.com/connectors/raytion-firstspirit-connector)

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

### GitLab

By [Raytion](https://www.raytion.com/contact)

Secure enterprise search connector for reliably indexing content from GitLab and intelligently searching it with Azure AI Search. It robustly indexes projects, files, folders, commit messages, issues, and wiki pages from GitLab in near real time. The connector fully supports GitLab’s built-in user and group management.

[More details](https://www.raytion.com/connectors/raytion-gitlab-connector)

:::column-end:::
:::column span="":::

---

### Google Cloud SQL

By [BA Insight](https://www.bainsight.com/)

The Google Cloud SQL Connector indexes content from Google Cloud SQL into the Azure AI Search index surfacing it through BA Insight's SmartHub to provide users with integrated search results.

[More details](https://www.bainsight.com/connectors/google-cloud-sql-connector-sharepoint-azure-elasticsearch/)

:::column-end:::
:::column span="":::

---

### Google Drive

By [BA Insight](https://www.bainsight.com/)

The BAI Google Drive connector makes it possible to surface content from Google Drive in a single consolidated search index referencing Google Drive content, along with content from other repositories.

[More details](https://www.bainsight.com/connectors/google-drive-connector-sharepoint-azure-elasticsearch/)

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

### Google Drive

By [Raytion](https://www.raytion.com/contact)

Secure enterprise search connector for reliably indexing content from Google Drive and intelligently searching it with Azure AI Search. It robustly indexes files, folders, and comments on personal drives and team drives from Google Drive in near real time. The connector fully supports Google Drive’s built-in permission model and the user and group management by the Google Admin Directory.

[More details](https://www.raytion.com/connectors/raytion-google-drive-connector)

:::column-end:::
:::column span="":::

---

### Happeo 

By [Raytion](https://www.raytion.com/contact)

Raytion's Happeo Connector indexes content from Happeo into Azure AI Search and keeps track of all changes, whether for your company-wide enterprise search platform or in vibrant social collaboration environments. It guarantees an updated Azure Cognitive index and advances knowledge sharing.

[More details](https://www.raytion.com/connectors/raytion-happeo-connector)

:::column-end:::
:::column span="":::

---


### HP Consolidated Archive (EAS)

By [BA Insight](https://www.bainsight.com/)

BA Insight's HP Consolidated Archive Connector securely indexes both the full text and metadata of documents in archives into various search engines, including SharePoint Search and Azure Search. This enables a single searchable result set across content from multiple repositories. It allows organizations to tap into the wealth of information accessible within Consolidated Archive, SharePoint and other repositories, making that data instantly actionable to users through search.

[More details](https://www.bainsight.com/connectors/hp-consolidated-archive-connector-sharepoint-azure-elasticsearch/)

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

### IBM Connections

By [Accenture](https://www.accenture.com)

The IBM Connections connector crawls content from IBM Connections server, featuring incremental crawling, metadata extraction, fetching of ACLs, filtering documents by regex patterns, and more.

[More details](https://contentanalytics.digital.accenture.com/display/aspire40/IBM+Connections+Connector)

:::column-end:::
:::column span="":::

---

### IBM Connections

By [BA Insight](https://www.bainsight.com/)

The IBM Connections Connector was developed for IBM Connections, establishing a secure connection to the Connections application and mapping the content, including metadata and attachments, from the Connections schema to the search engine schema. It then extracts content and feeds it to the search engine in a process called crawling.

[More details](https://www.bainsight.com/connectors/ibm-connections-connector-sharepoint-azure-elasticsearch/)

:::column-end:::
:::column span="":::

---

### IBM Connections

By [Raytion](https://www.raytion.com/contact)

Secure enterprise search connector for reliably indexing content from IBM Connections and intelligently searching it with Azure AI Search. It robustly indexes public and personal files, blogs, wikis, forums, communities, bookmarks, profiles, and status updates from on-premises Connections instances in near real time. The connector fully supports IBM Connection’s built-in user and group management, and Connections installations based on Microsoft Entra ID and other directory services.

[More details](https://www.raytion.com/connectors/raytion-ibm-connections-connector)

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

### IBM Connections Cloud

By [Raytion](https://www.raytion.com/contact)

Secure enterprise search connector for reliably indexing content from IBM Connections Cloud and intelligently searching it with Azure AI Search. It robustly indexes public and personal files, blogs, wikis, forums, communities, profiles, and status updates from Connections Cloud in near real time. The connector fully supports IBM Connections Cloud’s built-in user and group management.

[More details](https://www.raytion.com/connectors/raytion-ibm-connections-cloud-connector)

:::column-end:::
:::column span="":::

---

### IBM Content Manager

By [BA Insight](https://www.bainsight.com/)

The IBM Content Manager Connector honors the security of source applications and provides both full and incremental crawls, so users always have the latest information available to them.

[More details](https://www.bainsight.com/connectors/ibm-content-manager-connector-sharepoint-azure-elasticsearch/)

:::column-end:::
:::column span="":::

---

### IBM Db2

By [BA Insight](https://www.bainsight.com/)

The Db2 Connector allows organizations to tap into the wealth of data stored within DB2 databases and applications and make that data instantly actionable to users through search.

[More details](https://www.bainsight.com/connectors/ibm-db2-connector-sharepoint-azure-elasticsearch/)

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

### IBM FileNet P8

By [BA Insight](https://www.bainsight.com/)

The IBM FileNet Content Manager Connector allows SharePoint, and other portal users, to securely search for content stored in FileNet repositories. Access to content is determined by security established in FileNet, ensuring that your content is as safe when accessed through any other portal as it is directly within FileNet.

[More details](https://www.bainsight.com/connectors/ibm-filenet-sharepoint-azure-elasticsearch/)

:::column-end:::
:::column span="":::

---

### IBM Lotus Notes

By [BA Insight](https://www.bainsight.com/)

With BA Insight's IBM Notes Email Connector, users have the ability to search Lotus Notes emails directly from within SharePoint or another portal. Security defined within IBM Notes is automatically reflected in the search experience, so users see search results from their own mailbox, public mailboxes, and other mailboxes for which they have been granted access.

[More details](https://www.bainsight.com/connectors/lotus-notes-connector-sharepoint-azure-elasticsearch/)

:::column-end:::
:::column span="":::

---

### IBM WebSphere

By [BA Insight](https://www.bainsight.com/)

BA Insight's WebSphere Connector securely indexes both the full text and metadata of WebSphere objects into Microsoft's search engine, enabling a single searchable result set across content from multiple repositories. This connector allows organizations to tap into the wealth of information accessible within Microsoft platforms, and makes that data instantly actionable to users through search.

[More details](https://www.bainsight.com/connectors/ibm-websphere-connector-sharepoint-azure-elasticsearch/)

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

### iManage Cloud

By [BA Insight](https://www.bainsight.com/)

BA Insight's iManage Cloud Connector securely indexes both the full text and metadata of documents in the Work workspaces into the search engine.

[More details](https://www.bainsight.com/connectors/connector-for-imanage-work-cloud/)

:::column-end:::
:::column span="":::

---

### iManage Work

By [BA Insight](https://www.bainsight.com/)

The iManage Work Connector provides full security and operates at high throughput to minimize crawl times while maintaining a low-performance impact on Work. It only requires read access, and there is no need to install client software on any iManage server. This results in seamless and simultaneous access to all content stored in iManage Work.

[More details](https://www.bainsight.com/connectors/imanage-work-connector-sharepoint-azure-elasticsearch/)

:::column-end:::
:::column span="":::

---

### Jira

By [BA Insight](https://www.bainsight.com/)

The Jira Connector enables users to perform searches against all Jira objects, eliminating the need to go to Jira directly.

[More details](https://www.bainsight.com/connectors/jira-connector-for-sharepoint-azure-elasticsearch/)

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

### Jira

By [Raytion](https://www.raytion.com/contact)

Secure enterprise search connector for reliably indexing content from Atlassian Jira and intelligently searching it with Azure AI Search. It robustly indexes projects, issues, attachments, comments, work logs, issue histories, links, and profiles from on-premises Jira instances in near real time. The connector fully supports Atlassian Jira’s built-in user and group management, and Jira installations based on Microsoft Entra ID and other directory services.

[More details](https://www.raytion.com/connectors/raytion-jira-connector)

:::column-end:::
:::column span="":::

---

### Jira Cloud

By [BA Insight](https://www.bainsight.com/)

The Jira (Cloud Version) Connector performs searches against all Jira objects, eliminating the need to navigate to Jira directly.

[More details](https://www.bainsight.com/connectors/jira-cloud-connector-for-sharepoint-azure-elasticsearch/)

:::column-end:::
:::column span="":::

---

### Jira Cloud

By [Raytion](https://www.raytion.com/contact)

Secure enterprise search connector for reliably indexing content from Atlassian Jira Cloud and intelligently searching it with Azure AI Search. It robustly indexes projects, issues, attachments, comments, work logs, issue histories, links and profiles from Jira Cloud in near real time. The connector fully supports Atlassian Jira Cloud’s built-in user and group management.

[More details](https://www.raytion.com/connectors/raytion-jira-cloud-connector)

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

### Jive

By [BA Insight](https://www.bainsight.com/)

The Jive Connector was developed for Jive, establishing a secure connection to the Jive application and mapping the content including metadata and attachments from the Jive schema to the search engine schema. It then extracts content and feeds it to the search engine in a process called crawling.

[More details](https://www.bainsight.com/connectors/jive-connector-sharepoint-azure-elasticsearch/)

:::column-end:::
:::column span="":::

---

### Jive

By [Raytion](https://www.raytion.com/contact)

Secure enterprise search connector for reliably indexing content from Jive and intelligently searching it with Azure AI Search. It robustly indexes discussions, polls, files, blogs, spaces, groups, projects, tasks, videos, messages, ideas, profiles, and status updates from on-premises and cloud-hosted Jive instances in near real time. The connector fully supports Jive’s built-in user and group management and supports Jive’s native authentication models, OAuth and Basic authentication.

[More details](https://www.raytion.com/connectors/raytion-jive-connector)

:::column-end:::
:::column span="":::

---

### Kaltura

By [BA Insight](https://www.bainsight.com/)

The Kaltura Connector enables the indexing of not only video, but also various other types of information including Categories, Data, Documents and more.

[More details](https://www.bainsight.com/connectors/kaltura-connector-for-sharepoint-azure-elasticsearch/)

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

### LDAP

By [BA Insight](https://www.bainsight.com/) 

The LDAP Connector enables organizations to connect to any LDAP-compliant directory and index any record from it. Organizations can filter to specific subsets of the directory and retrieve only specific fields, making it simple to search for users, contacts, or groups stored anywhere in your directory.

[More details](https://www.bainsight.com/connectors/ldap-connector-for-sharepoint-azure-elasticsearch/)

:::column-end:::
:::column span="":::

---

### LDAP

By [Raytion](https://www.raytion.com/contact)

Secure enterprise search connector for reliably indexing content from directory services compatible with the Lightweight Directory Access Protocol (LDAP) and intelligently searching it with Azure AI Search. It robustly indexes LDAP objects from Microsoft Entra ID, Novell E-Directory and other LDAP-compatible directory services in near real time. The connector can be used for ingesting principals into Google Cloud Search for use cases like expert, equipment and location searches or for implementing security trimming for custom data sources. The connector supports LDAP over SSL.

[More details](https://www.raytion.com/connectors/raytion-ldap-connector)

:::column-end:::
:::column span="":::

---

### LegalKEY

By [BA Insight](https://www.bainsight.com/) 

BA Insight's OpenText LegalKEY Connector securely indexes both the full text and metadata of client and matter records in LegalKEY into the Microsoft search engine, enabling a single searchable result set across content from multiple repositories. This connector allows organizations to tap into the wealth of information accessible within LegalKEY, SharePoint, and other repositories, making that data instantly actionable to users through search.

[More details](https://www.bainsight.com/connectors/legalkey-connector-sharepoint-azure-elasticsearch/)

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

### LexisNexis InterAction

By [BA Insight](https://www.bainsight.com/)

The LexisNexis InterAction Connector makes it easier for lawyers and other firm employees throughout the organization to find important information stored in InterAction without the need to directly log in and perform a separate search.

[More details](https://www.bainsight.com/connectors/lexisnexis-interaction-connector-sharepoint-azure-elasticsearch/)

:::column-end:::
:::column span="":::

---

### Lotus Notes Databases

By [BA Insight](https://www.bainsight.com/) 

With the IBM Notes Database Connector, users have the ability to find content stored in Notes databases using Azure AI Search. Security defined within IBM Notes is automatically reflected in the search experience, which ensures that users see content for which they are authorized. Ultimately, users can find everything they need in one place.

[More details](https://www.bainsight.com/connectors/ibm-lotus-notes-connector-sharepoint-azure-elasticsearch/)

:::column-end:::
:::column span="":::

---

### M-Files

By [BA Insight](https://www.bainsight.com/)

The M-Files connector enables indexing of content managed by the M-Files platform and supports both Full and Incremental crawling to ensure index freshness.

[More details](https://www.bainsight.com/connectors/m-files-connector-for-sharepoint-azure-elasticsearch/)

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

### MediaPlatform PrimeTime

By [BA Insight](https://www.bainsight.com/)

BA Insight's MediaPlatform PrimeTime indexing connector makes it possible to make the content accessible to users via an organization's enterprise search platform, combining the connector with BA Insight's SmartHub. The BA Insight MediaPlatform PrimeTime Connector retrieves information about channels and videos from MediaPlatform PrimeTime and indexes them via an Azure AI Search.

[More details](https://www.bainsight.com/connectors/mediaplatform-primetime-connector-sharepoint-azure-elasticsearch/)

:::column-end:::
:::column span="":::

---

### MediaWiki

By [Raytion](https://www.raytion.com/contact)

Secure enterprise search connector for reliably indexing content from MediaWiki and intelligently searching it with Azure AI Search. It robustly indexes pages, discussion pages, and attachments from MediaWiki instances in near real time. The connector fully supports MediaWiki’s built-in permission model, and MediaWiki installations based on Microsoft Entra ID and other directory services.

[More details](https://www.raytion.com/connectors/raytion-mediawiki-connector)

:::column-end:::
:::column span="":::

---

### Micro Focus Content Manager (HPE Records Manager/HP TRIM)

By [BA Insight](https://www.bainsight.com/)

The HP TRIM Connector was developed for HP Records Manager, establishing a secure connection to the TRIM application and mapping the content, including metadata and attachments, from the TRIM schema to the search engine schema. It then extracts content and feeds it to the search engine in a process called crawling.

[More details](https://www.bainsight.com/connectors/hp-trim-connector-sharepoint-azure-elasticsearch/)

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

### Microsoft Dynamics 365

By [BA Insight](https://www.bainsight.com/)

Our Microsoft Dynamics 365 CRM connector supports both on-premises CRM installations and Dynamics CRM Online.

[More details](https://www.bainsight.com/connectors/microsoft-dynamics-crm-connector-sharepoint-azure-elasticsearch/)

:::column-end:::
:::column span="":::

---

### Microsoft Dynamics 365 (Cloud)

By [BA Insight](https://www.bainsight.com/)

Our Microsoft Dynamics 365 (Cloud Version) CRM Connector establishes a secure connection to the CRM application and maps the content from the CRM schema to the search engine schema.

[More details](https://www.bainsight.com/connectors/connector-for-microsoft-dynamics-cloud/)

:::column-end:::
:::column span="":::

---

### Microsoft Exchange Online

By [BA Insight](https://www.bainsight.com/)

Using the BA Insight Microsoft Exchange Online Connector, users can retrieve content from Exchange Online through various search platforms.

[More details](https://www.bainsight.com/connectors/microsoft-exchange-online-connector-sharepoint-azure-elasticsearch/)

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

### Microsoft Exchange Public Folders

By [BA Insight](https://www.bainsight.com/)

Using the BAI Microsoft Exchange Public Folders Connector, users can retrieve content from Exchange through various search platforms.

[More details](https://www.bainsight.com/connectors/microsoft-exchange-connector-sharepoint-azure-elasticsearch/)

:::column-end:::
:::column span="":::

---

### Microsoft Exchange Server

By [BA Insight](https://www.bainsight.com/)

Using the BA Insight Microsoft Exchange Connector, users can retrieve content from Exchange through various search engines.

[More details](https://www.bainsight.com/connectors/microsoft-exchange-server-connector-sharepoint-azure-elasticsearch/)

:::column-end:::
:::column span="":::

---

### Microsoft SQL Server

By [BA Insight](https://www.bainsight.com/)

The database connector is built upon industry standard database access methods, so it can equally support databases from other systems such as Oracle, MySQL, and IBM DB2. It honors the security of the source database and provides both full and incremental crawls, so users always have the latest information available to them.

[More details](https://www.bainsight.com/connectors/sql-connector-sharepoint-azure-elasticsearch/)

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

### Microsoft Teams

By [BA Insight](https://www.bainsight.com/)

The BA Insight Microsoft Teams Connector indexes content from Microsoft Teams alongside content from other enterprise systems to provide unified results.

[More details](https://www.bainsight.com/connectors/microsoft-teams-connector-for-sharepoint-azure-elasticsearch/)

:::column-end:::
:::column span="":::

---

### Microsoft Windows File Server

By [Raytion](https://www.raytion.com/contact)

Secure enterprise search connector for reliably indexing content from Microsoft Windows File Server including its Distributed File System (DFS) and intelligently searching it with Azure AI Search. It robustly indexes files and folders from Windows File Server in near real time. The connector fully supports Microsoft Windows File Server’s document-level security and the latest versions of the SMB2 and SMB3 protocols.

[More details](https://www.raytion.com/connectors/raytion-windows-file-server-connector)

:::column-end:::
:::column span="":::

---

### MySQL

By [BA Insight](https://www.bainsight.com/)

The MySQL connector is built upon industry standard database access methods, so it can equally support databases from other systems such as Oracle, MySQL, and IBM DB2. It honors the security of the source database and provides both full and incremental crawls, so users always have the latest information available to them.

[More details](https://www.bainsight.com/connectors/mysql-connector-sharepoint-azure-elasticsearch/)

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

### NetDocuments

By [BA Insight](https://www.bainsight.com/)

The NetDocuments Connector indexes content stored in NetDocs so that users can search and retrieve NetDocuments content directly from within their portal. The connector applies document security in NetDocs to Azure AI Search automatically, so user information remains secure. Metadata stored in NetDocuments can be mapped to equivalent terms so that users have a seamless search experience.

[More details](https://www.bainsight.com/connectors/netdocuments-connector-sharepoint-azure-elasticsearch/)

:::column-end:::
:::column span="":::

---

### Neudesic The Firm Directory

By [BA Insight](https://www.bainsight.com/)

The Firm Directory Connector honors the security of the source system and provides both full and incremental crawls so the users have the latest information available to them all the time.

[More details](https://www.bainsight.com/connectors/the-firm-directory-connector-sharepoint-azure-elasticsearch/)

:::column-end:::
:::column span="":::

---

### Notes

By [Raytion](https://www.raytion.com/contact)

Secure enterprise search connector for reliably indexing content from IBM Notes (formerly Lotus Note) and intelligently searching it with Azure AI Search. It robustly indexes records from a configurable set of Notes databases in near real time. The connector fully supports IBM Notes’ built-in user and group management.

[More details](https://www.raytion.com/connectors/raytion-notes-connector)

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

### Nuxeo

By [BA Insight](https://www.bainsight.com/)

The Nuxeo connector lets organizations index their Nuxeo content, including both security information and standard and custom metadata set on content into Azure AI Search alongside content present in Office 365. Ultimately, users can find everything they need in one place.

[More details](https://www.bainsight.com/connectors/nuxeo-connector-for-sharepoint-azure-elasticsearch/)

:::column-end:::
:::column span="":::

---

### Objective

By [BA Insight](https://www.bainsight.com/)

The Objective Connector was developed for Objective, establishing a secure connection to Objective and mapping the content including metadata from the Objective schema to the search engine schema. It then extracts content and feeds it to the search engine in a process called crawling.

[More details](https://www.bainsight.com/connectors/objective-connector-sharepoint-azure-elasticsearch/)

:::column-end:::
:::column span="":::

---

### OneDrive

By [Accenture](https://www.accenture.com)

The OneDrive connector crawls content from Microsoft OneDrive, allowing incremental crawling, including and excluding items based on regex patterns, metadata extraction, retrieving several types of documents.

[More details](https://contentanalytics.digital.accenture.com/display/aspire40/OneDrive+Connector)

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

### OneDrive for work or school

By [BA Insight](https://www.bainsight.com/)

The BA Insight OneDrive Connector makes it possible to index content from OneDrive into various search platforms, providing users with integrated search results from multiple sources.

[More details](https://www.bainsight.com/connectors/onedrive-business-connector-sharepoint-azure-elasticsearch/)

:::column-end:::
:::column span="":::

---

### OpenText Content Server

By [BA Insight](https://www.bainsight.com/)

The connector indexes Content Server content in much the same way as the native portal content, supporting both full crawls and incremental crawls. Security defined in Content Server is automatically reflected in the search experience, which ensures that users only see content for which they are authorized.

[More details](https://www.bainsight.com/connectors/livelink-connector-sharepoint-azure-elasticsearch/)

:::column-end:::
:::column span="":::

---

### OpenText Content Server

By [Raytion](https://www.raytion.com/contact)

Secure enterprise search connector for reliably indexing content from OpenText Content Server and intelligently searching it with Azure AI Search. It robustly indexes files, folders, virtual folders, compound documents, news, emails, volumes, collections, classifications, and many more objects from Content Server instances in near real time. The connector fully supports OpenText Content Server’s built-in user and group management.

[More details](https://www.raytion.com/connectors/raytion-opentext-content-server-connector)

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

### OpenText Documentum (Cloud)

By [BA Insight](https://www.bainsight.com/)

BA Insight's OpenText Documentum Cloud Connector securely indexes both the full text and metadata of Documentum objects into the search engine, enabling a single searchable result set across content from multiple repositories.

[More details](https://www.bainsight.com/connectors/connector-for-documentum-cloud/)

:::column-end:::
:::column span="":::

---

### OpenText Documentum eRoom

By [Raytion](https://www.raytion.com/contact)

Secure enterprise search connector for reliably indexing content from OpenText Documentum eRoom and intelligently searching it with Azure AI Search. It robustly indexes repositories, folders and files together with their meta data and properties from Documentum eRoom in near real time. The connector fully supports OpenText Documentum eRoom’s built-in user and group management.

[More details](https://www.raytion.com/connectors/raytion-opentext-documentum-eroom-connector)

:::column-end:::
:::column span="":::

---

### OpenText eDOCS DM

By [BA Insight](https://www.bainsight.com/)

Users of the OpenText eDOCS DM Connector can search for content housed in eDOCS repositories directly from within Azure AI Search, eliminating the need to perform multiple searches to locate needed content. Security established within eDOCS is maintained by the connector to make certain that content is only seen by those who have been granted access.

[More details](https://www.bainsight.com/connectors/edocs-dm-connector-sharepoint-azure-elasticsearch/)

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

### Oracle Database

By [BA Insight](https://www.bainsight.com/)

The Oracle Database Connector is built upon industry standard database access methods, so it can equally support databases from other systems such as Microsoft SQL Server, MySQL, and IBM DB2.

[More details](https://www.bainsight.com/connectors/oracle-database-connector-sharepoint-azure-elasticsearch/)

:::column-end:::
:::column span="":::

---

### Oracle WebCenter

By [BA Insight](https://www.bainsight.com/)

The WebCenter Connector integrates WebCenter with Azure AI Search, making it easier for users throughout the organization to find important information stored in WebCenter without the need to directly log in and do a separate search.

[More details](https://www.bainsight.com/connectors/oracle-webcenter-connector-sharepoint-azure-elasticsearch/)

:::column-end:::
:::column span="":::

---

### Oracle KA Cloud

By [Raytion](https://www.raytion.com/contact)

Secure enterprise search connector for reliably indexing content from Oracle Knowledge Advanced (KA) Cloud and intelligently searching it Azure AI Search. It robustly indexes pages and attachments from Oracle KA Cloud in near real time. The connector fully supports Oracle KA Cloud’s built-in user and group management. In particular, the connector handles snippet-based permissions within Oracle KA Cloud pages.

[More details](https://www.raytion.com/connectors/raytion-oracle-ka-cloud-connector)

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

### Oracle WebCenter Content (UCM/Stellent)

By [BA Insight](https://www.bainsight.com/)

The WebCenter Content Connector fully supports the underlying security of all content made available to Azure AI Search and keeps this content up to date via scheduled crawls, ensuring users get the most recent updates when doing a search.

[More details](https://www.bainsight.com/connectors/oracle-webcenter-content-connector-sharepoint-azure-elasticsearch/)

:::column-end:::
:::column span="":::

---

### pirobase CMS

By [Raytion](https://www.raytion.com/contact)

Secure enterprise search connector for reliably indexing content from pirobase CMS and intelligently searching it with Azure AI Search. It robustly indexes pages, attachments, and other generated document types from pirobase CMS in near real time. The connector fully supports pirobase CMS’ built-in user and group management.

[More details](https://www.raytion.com/connectors/raytion-pirobase-cms-connector)

:::column-end:::
:::column span="":::

---

### PostgreSQL

By [BA Insight](https://www.bainsight.com/)

BA Insight's PostgreSQL Connector honors the security of the source database and provides full and incremental crawls, so users always have the latest information available. It indexes content from PostgreSQL into Azure AI Search, surfacing it through BA Insight's SmartHub to provide users with integrated search results.

[More details](https://www.bainsight.com/connectors/postgresql-connector-connector-sharepoint-azure-elasticsearch/)

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


### Practical Law

By [BA Insight](https://www.bainsight.com/)

The BA Insight Practical Law Connector enables users to perform searches against the Practical Law database, eliminating the need to navigate to Practical Law directly.

[More details](https://www.bainsight.com/connectors/practical-law-connector-sharepoint-azure-elasticsearch/)

:::column-end:::
:::column span="":::

---

### ProLaw

By [BA Insight](https://www.bainsight.com/)

The BA Insight Connector for Pro Law connects any portal to ProLaw, enabling information from ProLaw to be surfaced while respecting the user privileges within ProLaw.

[More details](https://www.bainsight.com/connectors/prolaw-connector-sharepoint-azure-elasticsearch/)

:::column-end:::
:::column span="":::

### RDB via Snapshots

By [Accenture](https://www.accenture.com)

The RDB via Snapshots connector crawls content from any relational database that can be accessed using JDBC and performs incremental crawls using a snapshot database. It extracts data directly based on SQL statements.

[More details](https://contentanalytics.digital.accenture.com/display/aspire40/RDB+via+Snapshots+Connector)

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

### RDB via Tables

By [Accenture](https://www.accenture.com)

The RDB via Tables connector crawls content from any relational database that can be accessed using JDBC and performs incremental crawls fetching updates using tables that hold identifiers of updated content. It extracts data directly based on SQL statements.

[More details](https://contentanalytics.digital.accenture.com/display/aspire40/RDB+via+Table+Connector)

:::column-end:::
:::column span="":::

---

### S3

By [Accenture](https://www.accenture.com)

The Amazon S3 connector crawls content from any Amazon Simple Storage Service. It performs incremental crawls, fetch object ACLs for S3 document level security and includes documents stored in buckets, folders and subfolders.

[More details](https://contentanalytics.digital.accenture.com/display/aspire40/Amazon+S3+Connector)

:::column-end:::
:::column span="":::

---

### Salesforce

By [Accenture](https://www.accenture.com)

The Salesforce connector crawls content from a Salesforce repository. The connector supports Salesforce Knowledge Base and Chatter, metadata and custom metadata retrieval, performs full or incremental crawls, fetches ACLs, selectable element types and group expansion.

[More details](https://contentanalytics.digital.accenture.com/display/aspire40/Salesforce+Connector)

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

### Salesforce

By [BA Insight](https://www.bainsight.com/)

The Salesforce Connector integrates Salesforce's Service, Sales, and Marketing Cloud with Azure AI Search, making all the content within Salesforce available to all employees through this portal.

[More details](https://www.bainsight.com/connectors/salesforce-connector-sharepoint-azure-elasticsearch/)

:::column-end:::
:::column span="":::

---

### Salesforce

By [Raytion](https://www.raytion.com/contact)

Secure enterprise search connector for reliably indexing content from Salesforce and intelligently searching it with Azure AI Search. It robustly indexes accounts, chatter messages, profiles, leads, cases, and all other record objects from Salesforce in near real time. The connector fully supports Salesforce’s built-in user and group management.

[More details](https://www.raytion.com/connectors/raytion-salesforce-connector)

:::column-end:::
:::column span="":::

---

### SAP ERP

By [BA Insight](https://www.bainsight.com/)

BA Insight's SAP ERP Connector is designed to bring items from SAP into a search index. This in turn lights up the UI and allows for a unified view across information in SAP, SharePoint, and other systems.

[More details](https://www.bainsight.com/connectors/sap-erp-connector-sharepoint-azure-elasticsearch/)

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

### SAP ERP (Cloud)

By [BA Insight](https://www.bainsight.com/)

BA Insight's SAP ERP (Cloud Version) Connector is designed to bring items from SAP into a search index.

[More details](https://www.bainsight.com/connectors/connector-for-sap-erp-cloud/)

:::column-end:::
:::column span="":::

---

### SAP HANA

By [BA Insight](https://www.bainsight.com/)

The SAP HANA Connector honors the security of the source database and provides both full and incremental crawls, so users always have the latest information available to them. It indexes content from SAP HANA into Azure AI Search, surfacing it through BA Insight's SmartHub to provide users with integrated search results.

[More details](https://www.bainsight.com/connectors/sap-hana-connector-sharepoint-azure-elasticsearch/)

:::column-end:::
:::column span="":::

---

### SAP HANA (Cloud)

By [BA Insight](https://www.bainsight.com/)

The SAP HANA (Cloud Version) Connector honors the security of the source database and provides both full and incremental crawls so that users have the latest information available all of the time.

[More details](https://www.bainsight.com/connectors/connector-sap-hana-cloud-version/)

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


### SAP NetWeaver Portal

By [Raytion](https://www.raytion.com/contact)

Secure enterprise search connector for reliably indexing content from the SAP NetWeaver Portal (NWP) and intelligently searching it with Azure AI Search. It robustly indexes pages, attachments, and other document types from SAP NWP, its Knowledge Management and Collaboration (KMC) and Portal Content Directory (PCD) areas in near real time. The connector fully supports SAP NetWeaver Portal’s built-in user and group management, and SAP NWP installations based on Microsoft Entra ID and other directory services.

[More details](https://www.raytion.com/connectors/raytion-sap-netweaver-portal-connector)

:::column-end:::
:::column span="":::

---

### SAP PLM DMS

By [Raytion](https://www.raytion.com/contact)

Secure enterprise search connector for reliably indexing content from SAP PLM DMS and intelligently searching it with Azure AI Search. It robustly indexes documents, attachments, and other records from SAP PLM DMS in near real time.

[More details](https://www.raytion.com/connectors/raytion-sap-plm-dms-connector)

:::column-end:::
:::column span="":::

---

### Selenium

By [Accenture](https://www.accenture.com)

The Selenium connector crawls content from websites using an internet browser to retrieve several types of documents like web pages, sitemaps, binary documents, and more. It avoids compatibility issues with frameworks like Angular and React.

[More details](https://contentanalytics.digital.accenture.com/display/aspire40/Selenium+Crawler)

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

### ServiceNow

By [Accenture](https://www.accenture.com)

The ServiceNow connector retrieves several types of documents from a ServiceNow Repository, like Knowledge Articles, Catalog Items and Attachments. It also retrieves security ACLs and performs group expansion.

[More details](https://contentanalytics.digital.accenture.com/display/aspire40/ServiceNow+Connector)

:::column-end:::
:::column span="":::

---

### ServiceNow

By [BA Insight](https://www.bainsight.com/)

 ServiceNow Connector honors the security of the source system and provides both full and incremental crawls, so users always have the latest information available to them.

[More details](https://www.bainsight.com/connectors/servicenow-connector-sharepoint-azure-elasticsearch)

:::column-end:::
:::column span="":::

---

### ServiceNow

By [Raytion](https://www.raytion.com/contact)

Secure enterprise search connector for reliably indexing content from ServiceNow and intelligently searching it with Azure AI Search. It robustly indexes issues, tasks, attachments, knowledge management articles, pages, among others from ServiceNow in near real time. The connector supports ServiceNow’s built-in user and group management.

[More details](https://www.raytion.com/connectors/raytion-servicenow-connector)

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

By [Raytion](https://www.raytion.com/contact)

Secure enterprise search connector for reliably indexing content from Microsoft SharePoint and intelligently searching it with Azure AI Search. It robustly indexes sites, webs, modern (SharePoint 2016 and later) and classic pages, wiki pages, OneNote documents, list items, tasks, calendar items, attachments, and files from SharePoint on-premises instances in near real time. The connector fully supports Microsoft SharePoint’s built-in user and group management, and Microsoft Entra ID and also OAuth providers like SiteMinder and Okta. The connector comes with support for Basic, NTLM, and Kerberos authentication.

[More details](https://www.raytion.com/connectors/raytion-sharepoint-connector)

:::column-end:::
:::column span="":::

---

### SharePoint 2010

By [BA Insight](https://www.bainsight.com/)

BA Insight's SharePoint 2010 Connector allows you to connect to SharePoint 2010, fetch data from any site, document library, or list, and index this content securely.

[More details](https://www.bainsight.com/connectors/sharepoint-2010-connector/)

:::column-end:::
:::column span="":::

---

### SharePoint 2013

By [Accenture](https://www.accenture.com)

The SharePoint 2013 connector crawls content from any SharePoint 2013 site collection URL. It performs incremental crawls using SharePoint's change log timestamp or a snapshot database, fetches ACLs, supports NTLM and HTTPS, BCS external lists, and runs without installing anything on SharePoint.

[More details](https://contentanalytics.digital.accenture.com/display/aspire40/SharePoint+2013+Connector)

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

### SharePoint 2013

By [BA Insight](https://www.bainsight.com/)

BA Insight's SharePoint 2013 Connector allows you to connect to SharePoint 2013, fetch data from any site, document library, or list, and index this content securely.

[More details](https://www.bainsight.com/connectors/sharepoint-2013-connector/)

:::column-end:::
:::column span="":::

---

### SharePoint 2016

By [Accenture](https://www.accenture.com)

The SharePoint 2016 connector crawls content from any SharePoint 2016 site collection URL. It performs incremental crawls using SharePoint's change log timestamp or a snapshot database, fetches ACLs, supports NTLM and HTTPS, BCS external lists, and runs without installing anything on SharePoint.

[More details](https://contentanalytics.digital.accenture.com/display/aspire40/SharePoint+2016+Connector)

:::column-end:::
:::column span="":::

---

### SharePoint 2016

By [BA Insight](https://www.bainsight.com/)

BA Insight's SharePoint Connector allows you to connect to SharePoint 2016, fetch data from any site, document library, or list, and index this content securely.

[More details](https://www.bainsight.com/connectors/sharepoint-2016-connector/)

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

### SharePoint 2019

By [BA Insight](https://www.bainsight.com/)

BA Insight's SharePoint Connector allows you to connect to SharePoint 2019, fetch data from any site, document library, or list, and index this content securely.

[More details](https://www.bainsight.com/connectors/connector-for-sharepoint-2019/)

:::column-end:::
:::column span="":::

---

### SharePoint in Microsoft 365

By [Accenture](https://www.accenture.com)

The SharePoint connector crawls content from any SharePoint site collection URL. The connector retrieves Sites, Lists, Folders, List Items and Attachments, and other pages (in .aspx format). Supports SharePoint running in the Microsoft 365 offering.

[More details](https://contentanalytics.digital.accenture.com/display/aspire40/SharePoint+Online+Connector)

:::column-end:::
:::column span="":::

---

### SharePoint in Microsoft 365

By [BA Insight](https://www.bainsight.com/)

BA Insight's SharePoint Connector allows you to connect to SharePoint in Microsoft 365, fetch data from any site, document library, or list; and index this content securely.

[More details](https://www.bainsight.com/connectors/sharepoint-online-connector/)

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

### Sitecore

By [BA Insight](https://www.bainsight.com/)

The Sitecore Connector honors the security of the source system and provides both full and incremental crawls, so users always have the latest information available to them.

[More details](https://www.bainsight.com/connectors/sitecore-connector-sharepoint-azure-elasticsearch/)

:::column-end:::
:::column span="":::

---

### Sitecore

By [Raytion](https://www.raytion.com/contact)

Secure enterprise search connector for reliably indexing content from Sitecore and intelligently searching it with Azure AI Search. It robustly indexes pages, attachments, and further generated document types in near real time. The connector fully supports Sitecore’s permission model and the user and group management in the associated Microsoft Entra ID tenant.

[More details](https://www.raytion.com/connectors/raytion-sitecore-connector)

:::column-end:::
:::column span="":::

---

### Slack

By [Raytion](https://www.raytion.com/contact)

Secure enterprise search connector for reliably indexing content from Slack and intelligently searching it with Azure AI Search. It robustly indexes messages, threads, and shared files from all public channels from Slack in near real time.

[More details](https://www.raytion.com/connectors/raytion-slack-connector)

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


### SMB

By [Accenture](https://www.accenture.com)

The SMB connector retrieves files and directories across shared drives. It has Distributed File System support, security information retrieval, and it can access documents for indexing without changing the last accessed date.

[More details](https://contentanalytics.digital.accenture.com/display/aspire40/SMB+Connector)

:::column-end:::
:::column span="":::

---

### SMB File Share

By [Raytion](https://www.raytion.com/contact)

Secure enterprise search connector for reliably indexing content from SMB file shares and intelligently searching it with Azure AI Search. It robustly indexes files and folders from file shares in near real time. The connector fully supports SMB’s document-level security and the latest versions of the SMB2/SMB3 protocols.

[More details](https://www.raytion.com/connectors/raytion-smb-file-share-connector)

:::column-end:::
:::column span="":::

---

### SQL Database

By [Raytion](https://www.raytion.com/contact)

Secure enterprise search connector for reliably indexing content from SQL databases, such as Microsoft SQL Server or Oracle, and intelligently searching it with Azure AI Search. It robustly indexes records and fields including binary documents from SQL databases in near real time. The connector supports the implementation of a custom document-level security model.

[More details](https://www.raytion.com/connectors/raytion-sql-database-connector)

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

### Any SQL-based CRM system

By [BA Insight](https://www.bainsight.com/)

The SQL Server Connector is built upon industry standard database access methods, so it can equally support databases from other systems such as Oracle, MySQL, and IBM DB2. It honors the security of the source database, and provides both full and incremental crawls, so users always have the latest information available to them.

[More details](https://www.bainsight.com/connectors/sql-connector-sharepoint-azure-elasticsearch/)

:::column-end:::
:::column span="":::

---

### Symantec Enterprise Vault

By [Raytion](https://www.raytion.com/contact)

Secure enterprise search connector for reliably indexing content from Symantec Enterprise Vault and intelligently searching it with Azure AI Search. It robustly indexes archived data, such as e-mails, attachments, files, calendar items, and contacts from Enterprise Vault in near real time. The connector fully supports Symantec Enterprise Vault’s authentication models Basic, NTLM, and Kerberos authentication.

[More details](https://www.raytion.com/connectors/raytion-enterprise-vault-connector-2)

:::column-end:::
:::column span="":::

---

### Twitter

By [Accenture](https://www.accenture.com)

The Twitter connector crawls content from any X account. It performs full and incremental crawls, supports authentication using X user, consumer key and consumer secret key.

[More details](https://contentanalytics.digital.accenture.com/display/aspire40/Twitter+Connector)

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


### Veeva Vault

By [BA Insight](https://www.bainsight.com/)

BA Insight's Veeva Vault Connector securely indexes both the full text and metadata of Veeva Vault objects into Azure AI Search. This enables users to retrieve a single result set for content within Veeva Vault and Microsoft 365.

[More details](https://www.bainsight.com/connectors/veeva-vault-connector-sharepoint-azure-elasticsearch/)

:::column-end:::
:::column span="":::

---

### Veritas Enterprise Vault (Symantec eVault)

By [BA Insight](https://www.bainsight.com/)

The Veritas Enterprise Vault Connector honors the security of the source system and provides full and incremental crawls, so users always have the latest information available to them.

[More details](https://www.bainsight.com/connectors/enterprise-vault-connector-sharepoint-azure-elasticsearch/)

:::column-end:::
:::column span="":::

### Veritas Enterprise Vault

By [Raytion](https://www.raytion.com/contact)

Secure enterprise search connector for reliably indexing content from Veritas Enterprise Vault and intelligently searching it with Azure AI Search. It robustly indexes archived data, such as e-mails, attachments, files, calendar items and contacts from Enterprise Vault in near real time. The connector fully supports Veritas Enterprise Vault’s authentication models Basic, NTLM and Kerberos authentication.

[More details](https://www.raytion.com/connectors/raytion-enterprise-vault-connector)

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

### Website Crawler

By [BA Insight](https://www.bainsight.com/)

The BA Insight Website Crawler Connector makes it possible to surface content from any website in a single consolidated search index, along with content from other repositories.

[More details](https://www.bainsight.com/connectors/website-connector-for-sharepoint-azure-elasticsearch/)

:::column-end:::
:::column span="":::

---

### West km

By [BA Insight](https://www.bainsight.com/)

The BA Insight West km Connector supports search across transaction and litigation documents, including the creation of custom search results pages.

[More details](https://www.bainsight.com/connectors/westkm-connector-sharepoint-azure-elasticsearch/)

:::column-end:::
:::column span="":::

---

### windream ECM-System

By [Raytion](https://www.raytion.com/contact)

Secure enterprise search connector for reliably indexing content from windream ECM-System and intelligently searching it with Azure AI Search. It robustly indexes files and folders including the comprehensive sets of metadata associated by windream ECM-System in near real time. The connector fully supports windream ECM-System’s permission model and the user and group management in the associated Microsoft Entra ID tenant.

[More details](https://www.raytion.com/connectors/raytion-windream-ecm-system-connector)

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

### Xerox DocuShare

By [BA Insight](https://www.bainsight.com/)

Search for content housed in Docushare repositories directly from within Azure AI Search, eliminating the need to perform multiple searches to locate needed content.

[More details](https://www.bainsight.com/connectors/docushare-connector-sharepoint-azure-elasticsearch/)

:::column-end:::
:::column span="":::

---

### Xerox DocuShare

By [Raytion](https://www.raytion.com/contact)

Secure enterprise search connector for reliably indexing content from Xerox DocuShare and intelligently searching it with Azure AI Search. It robustly indexes data repositories, folders, profiles, groups, and files from DocuShare in near real time. The connector fully supports Xerox DocuShare’s built-in user and group management.

[More details](https://www.raytion.com/connectors/raytion-xerox-docushare-connector)

:::column-end:::
:::column span="":::

---

### Yammer

By [Accenture](https://www.accenture.com)

The Yammer connector crawls content from Yammer messages. It retrieves messages by Group, Thread or Topic and gets User, Group and Thread details.

[More details](https://contentanalytics.digital.accenture.com/display/aspire40/Yammer+Connector)

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

### Yammer

By [BA Insight](https://www.bainsight.com/)

The Yammer Connector establishes a secure connection to the Yammer application and maps the content including metadata and attachments from the Yammer schema to the search engine schema. It then extracts content and feeds it to the search engine in a process called crawling.

[More details](https://www.bainsight.com/connectors/yammer-connector-sharepoint-azure-elasticsearch/)

:::column-end:::
:::column span="":::

---

### Yammer

By [Raytion](https://www.raytion.com/contact)

Secure enterprise search connector for reliably indexing content from Microsoft Yammer and intelligently searching it with Azure AI Search. It robustly indexes channels, posts, replies, attachments, polls and announcements from Yammer in near real time. The connector fully supports Microsoft Yammer’s built-in user and group management, and in particular federated authentication against Microsoft 365.

[More details](https://www.raytion.com/connectors/raytion-yammer-connector)

:::column-end:::
:::column span="":::

---

### Zendesk Guide 

By [Raytion](https://www.raytion.com/contact)

Raytion's Zendesk Guide Connector indexes content from Zendesk Guide into Azure AI Search and keeps track of all changes, whether for your company-wide enterprise search platform or a knowledge search for customers or agents. It guarantees an updated Azure Cognitive index and advances knowledge sharing.

[More details](https://www.raytion.com/connectors/raytion-zendesk-guide-connector)

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
