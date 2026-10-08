---
title: Include file
description: Submit a model-configurable DPO job with Python or REST.
author: ssalgadodev
ms.author: ssalgado
ms.service: microsoft-foundry
ms.topic: include
ms.date: 10/07/2026
ms.custom: include
ai-usage: ai-assisted
---

::: zone pivot="programming-language-python"

## Create a DPO job with Python

[!INCLUDE [Python client setup](fine-tuning-python-client.md)]

Set `FINE_TUNING_MODEL` to an identifier from [supported model IDs and versions](../fine-tuning/overview.md#supported-models) that supports DPO with this API.

Set `FINE_TUNING_TRAINING_TYPE` to the API value for a supported [training type](../fine-tuning/overview.md#training-types). For example, Global training uses `GlobalStandard`.

For DPO after SFT, use the supported fine-tuned model's identifier, not its deployment name.

Upload the files and submit the job with default hyperparameters:

```python
import os

with open("training.jsonl", "rb") as training:
    training_file = client.files.create(file=training, purpose="fine-tune")
with open("validation.jsonl", "rb") as validation:
    validation_file = client.files.create(
        file=validation, purpose="fine-tune"
    )
client.files.wait_for_processing(training_file.id)
client.files.wait_for_processing(validation_file.id)

job = client.fine_tuning.jobs.create(
    model=os.environ["FINE_TUNING_MODEL"],
    training_file=training_file.id,
    validation_file=validation_file.id,
    method={"type": "dpo"},
    extra_body={
        "trainingType": os.environ["FINE_TUNING_TRAINING_TYPE"],
    },
)
print(job.id, job.status)
```

Reference: [Fine-tuning API](/rest/api/microsoft-foundry/azureopenai/fine-tuning).

Retain the returned job ID and continue to [monitor the job](#monitor-the-job-and-select-a-checkpoint).

::: zone-end

::: zone pivot="rest-api"

## Create a DPO job with REST

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

Replace `<SUPPORTED_MODEL_ID>` with an identifier from [supported model IDs and versions](../fine-tuning/overview.md#supported-models) that supports DPO with this API. For DPO after SFT, use the supported fine-tuned model's identifier, not its deployment name.

Replace `<SUPPORTED_TRAINING_TYPE>` with the API value for a supported [training type](../fine-tuning/overview.md#training-types). For example, Global training uses `GlobalStandard`.

Replace the file IDs and submit the job with default hyperparameters:

```bash
curl -X POST "$AZURE_OPENAI_ENDPOINT/openai/v1/fine_tuning/jobs" \
  -H "api-key: $AZURE_OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  --data '{
    "model": "<SUPPORTED_MODEL_ID>",
    "training_file": "<TRAINING_FILE_ID>",
    "validation_file": "<VALIDATION_FILE_ID>",
    "trainingType": "<SUPPORTED_TRAINING_TYPE>",
    "method": {"type": "dpo"}
  }'
```

Reference: [v1 fine-tuning API](/rest/api/microsoft-foundry/azureopenai/fine-tuning).

Retain the returned job ID and continue to [monitor the job](#monitor-the-job-and-select-a-checkpoint).

::: zone-end
