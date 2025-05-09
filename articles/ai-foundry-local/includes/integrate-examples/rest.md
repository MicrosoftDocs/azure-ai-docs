---
ms.service: azure-ai-foundry
ms.custom: build-2025
ms.topic: reference
ms.date: 05/02/2025
ms.author: maanavdalal
author: maanavd
---

## Basic Request

For quick tests or integrations with command line scripts:

```bash
curl http://localhost:5272/v1/chat/completions ^
  -H "Content-Type: application/json" ^
  -d "{\"model\": \"Phi-4-mini-gpu-int4-rtn-block-32\", \"messages\": [{\"role\": \"user\", \"content\": \"Tell me a short story\"}]}"
```

## Streaming Response

> [!NOTE]
> The example here works, but because there's no cleansing of the output, it may not be as clean as the other examples.

```bash
curl http://localhost:5272/v1/chat/completions ^
  -H "Content-Type: application/json" ^
  -d "{\"model\": \"Phi-4-mini-gpu-int4-rtn-block-32\", \"messages\": [{\"role\": \"user\", \"content\": \"Tell me a short story\"}], \"stream\": true}"
```
