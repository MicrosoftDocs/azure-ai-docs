---
title: Create a supervised fine-tuning job with REST
titleSuffix: Microsoft Foundry
description: Upload data and submit an SFT job with the REST API.
author: ssalgadodev
ms.author: ssalgado
manager: mcleans
ms.date: 10/05/2026
ms.service: microsoft-foundry
ms.subservice: foundry-openai
ms.topic: include
ms.custom:
  - build-2025, classic-and-new
ai-usage: ai-assisted
---

## Create an SFT job with REST

Set `AZURE_OPENAI_ENDPOINT` and `AZURE_OPENAI_API_KEY` for your resource. Run these commands in a Bash-compatible shell.

Upload each dataset with `purpose=fine-tune`, and retain the distinct file IDs:

```bash
curl -X POST "$AZURE_OPENAI_ENDPOINT/openai/v1/files" \
  -H "api-key: $AZURE_OPENAI_API_KEY" \
  -F "purpose=fine-tune" -F "file=@training.jsonl"

curl -X POST "$AZURE_OPENAI_ENDPOINT/openai/v1/files" \
  -H "api-key: $AZURE_OPENAI_API_KEY" \
  -F "purpose=fine-tune" -F "file=@validation.jsonl"
```

Reference: [Files API](/rest/api/azureopenai/files).

Replace `<SUPPORTED_MODEL_ID>` with an identifier from [supported model IDs and versions](../../fine-tuning/overview.md#supported-models) that supports SFT with this API.

Replace `<SUPPORTED_TRAINING_TYPE>` with the API value for a supported [training type](../../fine-tuning/overview.md#training-types). For example, Global training uses `GlobalStandard`.

[!INCLUDE [SFT hyperparameter settings](../../includes/supervised-fine-tuning-settings.md)]

Replace the file IDs and submit the job. The request includes hyperparameters in the job body and uses `auto` to request service-selected values:

```bash
curl -X POST "$AZURE_OPENAI_ENDPOINT/openai/v1/fine_tuning/jobs" \
  -H "api-key: $AZURE_OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  --data '{
    "model": "<SUPPORTED_MODEL_ID>",
    "training_file": "<TRAINING_FILE_ID>",
    "validation_file": "<VALIDATION_FILE_ID>",
    "trainingType": "<SUPPORTED_TRAINING_TYPE>",
    "method": {
      "type": "supervised",
      "supervised": {
        "hyperparameters": {
          "batch_size": "auto",
          "learning_rate_multiplier": "auto",
          "n_epochs": "auto"
        }
      }
    },
    "suffix": "my-model"
  }'
```

Reference: [v1 fine-tuning API](/rest/api/microsoft-foundry/azureopenai/fine-tuning).

Retain the returned job ID and continue to [monitor the job](#monitor-the-job-and-select-a-checkpoint).
