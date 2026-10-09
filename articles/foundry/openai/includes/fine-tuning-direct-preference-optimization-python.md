---
title: Include file
description: Create a managed DPO job with Python.
author: ssalgadodev
ms.author: ssalgado
ms.service: microsoft-foundry
ms.topic: include
ms.date: 10/06/2026
ms.custom: include
ai-usage: ai-assisted
---

Install `openai`. Upload the files and submit the job with default hyperparameters:

```python
import os
from openai import OpenAI

client = OpenAI(
    base_url=os.environ["AZURE_OPENAI_ENDPOINT"].rstrip("/") + "/openai/v1/",
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
)
with open("training.jsonl", "rb") as training:
    training_file = client.files.create(file=training, purpose="fine-tune")
with open("validation.jsonl", "rb") as validation:
    validation_file = client.files.create(
        file=validation, purpose="fine-tune"
    )
client.files.wait_for_processing(training_file.id)
client.files.wait_for_processing(validation_file.id)

job = client.fine_tuning.jobs.create(
    model="gpt-4.1-mini-2025-04-14",
    training_file=training_file.id,
    validation_file=validation_file.id,
    method={
        "type": "dpo",
        "dpo": {
            "hyperparameters": {
                "n_epochs": "auto",
                "batch_size": "auto",
                "learning_rate_multiplier": "auto",
                "beta": "auto",
            }
        },
    },
    extra_body={"trainingType": "GlobalStandard"},
)
print(job.id, job.status)
```

Reference: [OpenAI Python client](https://github.com/openai/openai-python).
