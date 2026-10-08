---
title: Create a supervised fine-tuning job with Python
titleSuffix: Microsoft Foundry
description: Upload data and submit an SFT job with the Foundry or OpenAI Python SDK.
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

## Create an SFT job with Python

[!INCLUDE [Python client setup](../../includes/fine-tuning-python-client.md)]

Set `FINE_TUNING_MODEL` to an identifier from [supported model IDs and versions](../../fine-tuning/overview.md#supported-models) that supports SFT with this API.

Set `FINE_TUNING_TRAINING_TYPE` to the API value for a supported [training type](../../fine-tuning/overview.md#training-types). For example, Global training uses `GlobalStandard`.

[!INCLUDE [SFT hyperparameter settings](../../includes/supervised-fine-tuning-settings.md)]

Upload `training.jsonl` and `validation.jsonl`, then submit the job. The example includes hyperparameters in the job body and uses `auto` to request service-selected values:

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
    suffix="my-model",
    method={
        "type": "supervised",
        "supervised": {
            "hyperparameters": {
                "batch_size": "auto",
                "learning_rate_multiplier": "auto",
                "n_epochs": "auto",
            }
        },
    },
    extra_body={
        "trainingType": os.environ["FINE_TUNING_TRAINING_TYPE"],
    },
)
print(job.id, job.status)
```

Reference: [Files API](/rest/api/azureopenai/files) and [v1 fine-tuning API](/rest/api/microsoft-foundry/azureopenai/fine-tuning).

Retain the returned job ID and continue to [monitor the job](#monitor-the-job-and-select-a-checkpoint).
