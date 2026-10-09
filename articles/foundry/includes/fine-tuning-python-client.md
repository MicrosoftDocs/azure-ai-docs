---
title: Include file
description: Initialize a Python fine-tuning client with the Foundry SDK first or the OpenAI SDK as an alternative.
author: ssalgadodev
ms.author: ssalgado
ms.service: microsoft-foundry
ms.topic: include
ms.date: 10/07/2026
ms.custom: include
ai-usage: ai-assisted
---

Initialize the client with the Microsoft Foundry SDK for your project, or use the OpenAI SDK with a resource endpoint. Both clients use the same upload and job commands below.

### [Foundry SDK](#tab/foundry-sdk)

Install `azure-ai-projects`, `azure-identity`, and `openai`. Sign in with a credential supported by `DefaultAzureCredential`, and set `FOUNDRY_PROJECT_ENDPOINT` to your project endpoint:

```python
import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

project = AIProjectClient(
    endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)
client = project.get_openai_client()
```

Reference: [AIProjectClient](/python/api/azure-ai-projects/azure.ai.projects.aiprojectclient) and [DefaultAzureCredential](/python/api/azure-identity/azure.identity.defaultazurecredential).

### [OpenAI SDK](#tab/oai-sdk)

Install `openai` and set `AZURE_OPENAI_ENDPOINT` and `AZURE_OPENAI_API_KEY` for your resource:

```python
import os
from openai import OpenAI

client = OpenAI(
    base_url=os.environ["AZURE_OPENAI_ENDPOINT"].rstrip("/") + "/openai/v1/",
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
)
```

Reference: [Azure OpenAI client configuration](../openai/api-version-lifecycle.md#code-changes).

---
