---
ms.service: azure-ai-search
ms.topic: include
ms.date: 04/16/2026
---

A knowledge source is a top-level, reusable object. Knowing about existing knowledge sources is helpful for either reuse or naming new objects.

Use [Knowledge Sources - Get (REST API)](/rest/api/searchservice/knowledge-sources/get?view=rest-searchservice-2026-04-01) to list knowledge sources by name and type.

```http
### List knowledge sources by name and type
GET {{search-url}}/knowledgesources?api-version=2026-04-01&$select=name,kind
api-key: {{api-key}}
```

You can also return a single knowledge source by name to review its JSON definition.

```http
### Get a knowledge source definition
GET {{search-url}}/knowledgesources/{{knowledge-source-name}}?api-version=2026-04-01
api-key: {{api-key}}
```
