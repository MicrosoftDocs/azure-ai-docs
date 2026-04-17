---
ms.service: azure-ai-search
ms.topic: include
ms.date: 04/17/2026
---

> [!IMPORTANT]
> If your search service has `publicNetworkAccess` disabled or uses a shared private link to the data source, the auto-generated indexer defaults to multitenant execution, which can't traverse private endpoints. This causes silent indexing failures and an empty index. To fix this issue, update the indexer to set `executionEnvironment` to `"Private"`. For more information, see [Indexer access to content protected by Azure network security](../search-indexer-howto-access-private.md).
