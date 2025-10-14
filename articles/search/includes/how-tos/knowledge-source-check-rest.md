---
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: include
ms.date: 10/13/2025
---

A knowledge source is a top-level, reusable object. All knowledge sources must be uniquely named within the knowledge sources collection. Knowing about existing knowledge sources is helpful for either reuse or naming new objects.

Use [Knowledge Sources - Get (REST API)](/rest/api/searchservice/knowledge-sources/get?view=rest-searchservice-2025-08-01-preview&preserve-view=true) to list knowledge sources by name and type.

```http
### List knowledge sources by name and type
GET {{search-url}}/knowledgeSources?api-version=2025-08-01-preview&$select=name,kind
api-key: {{api-key}}
Content-Type: application/json
```

You can also return a single knowledge source by name to review its JSON definition.

```http
### Get a knowledge source definition
GET {{search-url}}/knowledgeSources/{{knowledge-source-name}}?api-version=2025-08-01-preview
api-key: {{api-key}}
Content-Type: application/json
```
