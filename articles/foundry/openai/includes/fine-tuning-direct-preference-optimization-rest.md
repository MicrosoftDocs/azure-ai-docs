---
title: Include file
description: Create a managed DPO job with REST.
author: ssalgadodev
ms.author: ssalgado
ms.service: microsoft-foundry
ms.topic: include
ms.date: 10/06/2026
ms.custom: include
ai-usage: ai-assisted
---

In a Bash-compatible shell, upload each dataset with `purpose=fine-tune`. Retain the separate `id` values:

```bash
curl -X POST "$AZURE_OPENAI_ENDPOINT/openai/v1/files" \
  -H "api-key: $AZURE_OPENAI_API_KEY" \
  -F "purpose=fine-tune" -F "file=@training.jsonl"

curl -X POST "$AZURE_OPENAI_ENDPOINT/openai/v1/files" \
  -H "api-key: $AZURE_OPENAI_API_KEY" \
  -F "purpose=fine-tune" -F "file=@validation.jsonl"
```

Reference: [Files API](/rest/api/azureopenai/files).

Replace `<TRAINING_FILE_ID>` and `<VALIDATION_FILE_ID>` with those IDs:

```bash
curl -X POST "$AZURE_OPENAI_ENDPOINT/openai/v1/fine_tuning/jobs" \
  -H "api-key: $AZURE_OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  --data '{
    "model": "gpt-4.1-mini-2025-04-14",
    "training_file": "<TRAINING_FILE_ID>",
    "validation_file": "<VALIDATION_FILE_ID>",
    "trainingType": "GlobalStandard",
    "method": {
      "type": "dpo",
      "dpo": {
        "hyperparameters": {
          "n_epochs": "auto",
          "batch_size": "auto",
          "learning_rate_multiplier": "auto",
          "beta": "auto"
        }
      }
    }
  }'
```

Reference: [v1 fine-tuning REST API](/rest/api/microsoft-foundry/azureopenai/fine-tuning).
