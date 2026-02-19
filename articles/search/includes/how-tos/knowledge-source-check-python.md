---
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: include
ms.date: 11/13/2025
---

A knowledge source is a top-level, reusable object. Knowing about existing knowledge sources is helpful for either reuse or naming new objects.

Run the following code to list knowledge sources by name and type.

```python
# List knowledge sources by name and type
import requests
import json

endpoint = "{search_url}/knowledgesources"
params = {"api-version": "2025-11-01-preview", "$select": "name, kind"}
headers = {"api-key": "{api_key}"}

response = requests.get(endpoint, params = params, headers = headers)
print(json.dumps(response.json(), indent = 2))
```

You can also return a single knowledge source by name to review its JSON definition.

```python
# Get a knowledge source definition
import requests
import json

endpoint = "{search_url}/knowledgesources/{knowledge_source_name}"
params = {"api-version": "2025-11-01-preview"}
headers = {"api-key": "{api_key}"}

response = requests.get(endpoint, params = params, headers = headers)
print(json.dumps(response.json(), indent = 2))
```
