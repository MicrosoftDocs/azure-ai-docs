---
manager: nitinme
ms.service: azure-ai-services
ms.custom:
ms.topic: include
ms.date: 10/08/2024
ms.author: aahi
author: aahill
---

### How data is ingested into Azure AI search

As of September 2024, the ingestion APIs switched to [integrated vectorization](/azure/search/vector-search-integrated-vectorization). This update does **not** alter the existing API contracts. Integrated vectorization, a new offering of Azure AI Search, utilizes prebuilt skills for chunking and embedding the input data. The Azure OpenAI On Your Data ingestion service no longer employs custom skills. Following the migration to integrated vectorization, the ingestion process has undergone some modifications and as a result only the following assets are created:
   * `{job-id}-index`
   * `{job-id}-indexer`, if an hourly or daily schedule is specified, otherwise, the indexer is cleaned-up at the end of the ingestion process.
   * `{job-id}-datasource`

The chunks container is no longer available, as this functionality is now inherently managed by Azure AI Search.
