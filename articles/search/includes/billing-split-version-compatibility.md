---
ms.service: azure-ai-search
ms.topic: include
ms.date: 04/24/2026
---

You set billing consent using the Search Management REST API. The following table shows which property takes effect based on the Search Service REST API version your application uses.

| Search Service REST API version | Semantic ranker billing | Agentic retrieval billing |
|---|---|---|
| [2026-04-01](/rest/api/searchservice/operation-groups?view=rest-searchservice-2026-04-01&preserve-view=true) and later | Controlled by `semanticSearch` | Controlled by `knowledgeRetrieval` |
| [2025-11-01-preview](/rest/api/searchservice/operation-groups?view=rest-searchservice-2025-11-01-preview&preserve-view=true) and earlier | Controlled by `semanticSearch` | Controlled by `semanticSearch` |
