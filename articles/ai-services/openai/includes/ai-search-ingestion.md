---
manager: nitinme
ms.service: azure-ai-studio
ms.custom:
ms.topic: include
ms.date: 10/08/2024
ms.author: fshakerin
author: fshakerin
---

### How data is ingested into Azure AI search

Data is ingested into Azure AI search using the following process:
1. As of September 2024, the ingestion APIs have switched to [integrated vectoriztion](/azure/search/vector-search-integrated-vectorization). This update does **not** alter the existing API contracts. Integrated Vectorization - a new offering of Azure AI Search- utilizes prebuilt skills for chunking and embedding the input data. Consequently, the Azure OpenAI On Your Data ingestion service no longer employs custom skills. Following the migration to Integrated Vectorization, the ingestion process has undergone some modifications and as a result only the following assets are created: a single index, a single indexer (if an hourly or daily schedule is specified), and a data source. The chunks container is no longer available, as this functionality is now inherently managed by Azure AI Search.
