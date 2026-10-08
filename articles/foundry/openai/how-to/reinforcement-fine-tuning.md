---
title: Fine-tune a model with reinforcement fine-tuning in Microsoft Foundry
description: Prepare data, configure graders and response formats, set hyperparameters, and run reinforcement fine-tuning in Microsoft Foundry.
author: alvinashcraft
ms.author: aashcraft
manager: mcleans
ms.date: 10/05/2026
ms.service: microsoft-foundry
ms.subservice: foundry-openai
ms.topic: how-to
zone_pivot_groups: foundry-fine-tuning
ms.custom:
  - classic-and-new
  - build-2025
  - doc-kit-assisted
ai-usage: ai-assisted
---

# Fine-tune a model with reinforcement fine-tuning in Microsoft Foundry

Prepare your data and grader, then choose a response format and training settings. Create a reinforcement fine-tuning (RFT) job in Microsoft Foundry. For method comparisons and training concepts, see the [fine-tuning overview](../../fine-tuning/overview.md).

## Prerequisites

- A Foundry resource with an [RFT-supported model and training region](../../fine-tuning/overview.md#supported-models), including any required model access approval.
- The **Foundry User** role for training, or the **Foundry Owner** role if you also deploy a fine-tuned model or grader model.

::: zone pivot="programming-language-python"

- The client packages and credentials described in the [Python procedure](#create-an-rft-job-with-python).

::: zone-end

::: zone pivot="rest-api"

- Your resource endpoint and credentials, and a Bash-compatible shell for the REST examples.

::: zone-end

::: zone pivot="azd"

- [Azure Developer CLI](/azure/developer/azure-developer-cli/install-azd) version 1.22.1 or later.

::: zone-end

[!INCLUDE [Role rename note](../../includes/role-rename-note.md)]

[!INCLUDE [RFT data and grader preparation](../../includes/reinforcement-fine-tuning-preparation.md)]

## Configure hyperparameters

Start with your selected model's defaults. Compare validation rewards and grader behavior before adjusting training, sampling, or evaluation settings.

::: zone pivot="programming-language-studio"

Use the settings available in the job configuration. The available controls and accepted values depend on your selected model.

::: zone-end

::: zone pivot="programming-language-python,rest-api"

The v1 examples below omit optional hyperparameters. To override defaults, use supported settings under `method.reinforcement.hyperparameters` in the [v1 fine-tuning API](/rest/api/microsoft-foundry/azureopenai/fine-tuning).

::: zone-end

::: zone pivot="azd"

Keep the default settings in your model's YAML configuration for your first job. Use the configuration sample for your selected model rather than copying settings from another model.

::: zone-end

::: zone pivot="programming-language-studio"

## Create an RFT job in the portal

Use your prepared datasets and grader to create the job:

1. Open **Build** > **Fine-tune** in the [Foundry portal](https://ai.azure.com), and select **Fine-tune**.
1. Select an eligible model and the reinforcement fine-tuning method.
1. Upload the training and validation datasets.
1. [Configure and test the grader](#configure-and-test-the-grader). For a model grader, check [who hosts the grader deployment](#model-grader-deployments).
1. Choose a [response format](#choose-a-response-format) supported by your model, and use a matching grader.
1. Select a supported [training type](../../fine-tuning/overview.md#training-types), and leave [hyperparameters](#configure-hyperparameters) at their defaults for your first job.
1. Review the configuration and create the job. Retain its ID.

::: zone-end

::: zone pivot="programming-language-python"

## Create an RFT job with Python

[!INCLUDE [Python client setup](../../includes/fine-tuning-python-client.md)]

Set `FINE_TUNING_MODEL` to an identifier from [supported model IDs and versions](../../fine-tuning/overview.md#supported-models) that supports RFT with this API.

Upload the files, load and validate `grader.json`, and submit the job with default hyperparameters. For structured output, also set `RFT_RESPONSE_FORMAT_PATH` to your response-format JSON file and use a matching grader and dataset.

```python
import json
import os

with open("training.jsonl", "rb") as training:
    training_file = client.files.create(file=training, purpose="fine-tune")
with open("validation.jsonl", "rb") as validation:
    validation_file = client.files.create(
        file=validation, purpose="fine-tune"
    )
client.files.wait_for_processing(training_file.id)
client.files.wait_for_processing(validation_file.id)
with open("grader.json", encoding="utf-8") as grader_file:
    grader = json.load(grader_file)
client.fine_tuning.alpha.graders.validate(grader=grader)

reinforcement = {
    "grader": grader,
}
response_format_path = os.environ.get("RFT_RESPONSE_FORMAT_PATH")
if response_format_path:
    with open(response_format_path, encoding="utf-8") as format_file:
        reinforcement["response_format"] = json.load(format_file)

job = client.fine_tuning.jobs.create(
    model=os.environ["FINE_TUNING_MODEL"],
    training_file=training_file.id,
    validation_file=validation_file.id,
    extra_body={
        "method": {
            "type": "reinforcement",
            "reinforcement": reinforcement,
        },
    },
    suffix="my-rft-model",
)
print(job.id, job.status)
```

Reference: [Fine-tuning API](/rest/api/microsoft-foundry/azureopenai/fine-tuning).

The example sends the RFT method configuration in `extra_body` and prints the job ID and status. Leave `RFT_RESPONSE_FORMAT_PATH` unset for the plain-text example.

::: zone-end

::: zone pivot="rest-api"

## Create an RFT job with REST

Set `AZURE_OPENAI_ENDPOINT` and `AZURE_OPENAI_API_KEY` for your resource. Choose a model from [supported model IDs and versions](../../fine-tuning/overview.md#supported-models) that supports RFT with this API.

In a Bash-compatible shell, upload both datasets and retain their distinct file IDs:

```bash
curl -X POST "$AZURE_OPENAI_ENDPOINT/openai/v1/files" \
  -H "api-key: $AZURE_OPENAI_API_KEY" \
  -F "purpose=fine-tune" -F "file=@training.jsonl"

curl -X POST "$AZURE_OPENAI_ENDPOINT/openai/v1/files" \
  -H "api-key: $AZURE_OPENAI_API_KEY" \
  -F "purpose=fine-tune" -F "file=@validation.jsonl"
```

Reference: [Files API](/rest/api/azureopenai/files).

Replace `<SUPPORTED_MODEL_ID>` and the file IDs, then submit the job with default hyperparameters. The grader matches the exact-answer sample dataset:

```bash
curl -X POST "$AZURE_OPENAI_ENDPOINT/openai/v1/fine_tuning/jobs" \
  -H "api-key: $AZURE_OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  --data '{
    "model": "<SUPPORTED_MODEL_ID>",
    "training_file": "<TRAINING_FILE_ID>",
    "validation_file": "<VALIDATION_FILE_ID>",
    "method": {
      "type": "reinforcement",
      "reinforcement": {
        "grader": {
          "name": "medmcqa_ans_grader",
          "type": "string_check",
          "input": "{{item.reference_answer}}",
          "reference": "{{sample.output_text}}",
          "operation": "eq"
        }
      }
    },
    "suffix": "my-rft-model"
  }'
```

Reference: [v1 fine-tuning REST API](/rest/api/microsoft-foundry/azureopenai/fine-tuning).

For structured output, add your response-format object as `method.reinforcement.response_format` and replace the grader with one that evaluates that JSON output. Don't use the MedMCQ exact-text grader unchanged.

::: zone-end

<!-- [TO VERIFY] Confirm model-specific job-creation contracts for new RFT models before extending these v1 examples to them. -->

::: zone pivot="azd"

[!INCLUDE [Azure Developer CLI job workflow](../../includes/fine-tuning-cli.md)]

::: zone-end

Review [RFT cost management](../../fine-tuning/cost-management.md#managing-costs-and-spending-limits-when-using-rft) and [fine-tuning pricing](https://aka.ms/oai/pricing) before starting or resuming a job. Billing and spending-limit behavior depend on your selected model.

## Review training metrics

RFT measures the rewards assigned by your grader, not SFT token-prediction accuracy. Compare rewards, grader errors, and reasoning-token use across training and validation.

Metric availability depends on your model and grader configuration:

| Metrics | What to look for |
| --- | --- |
| Training mean reward. | Average grader reward for the current training batch. Batches differ, so inspect the trend rather than comparing individual steps directly. |
| Validation mean reward. | Average grader reward over the validation set. Use this more stable signal to compare checkpoints, then inspect held-out responses. |
| Per-grader rewards. | For combined graders, inspect each grader's scores. A higher overall reward can hide poor performance on one criterion. |
| Grader error rates. | Check parse errors, missing reference fields, and execution errors. These indicate problems with the output format or grader configuration. |
| Mean reasoning tokens, when reported. | Compare token use with reward and held-out task quality. More reasoning tokens don't necessarily mean a better model. |

::: zone pivot="programming-language-python,rest-api"

In metric events, overall rewards are `train_reward_mean` and `valid_reward_mean` under `data.scores`. Per-grader scores are under `data.scores.graders`.

Reasoning-token metrics are `train_reasoning_tokens_mean` and `valid_reasoning_tokens_mean` under `data.usage.samples`. Grader errors are under `data.errors.graders`. These aren't SFT loss or token-accuracy fields.

::: zone-end

When the job provides linked automatic evaluations, compare scores and failed responses across runs and checkpoints. High grader rewards alone don't establish that the model solves your task.

For explanations of reward-quality risks, see [challenges and limitations](../../fine-tuning/overview.md#challenges-and-limitations).

[!INCLUDE [Managed job monitoring](../../includes/fine-tuning-job-management.md)]

## Related content

- [Countdown RFT workflow](https://github.com/microsoft-foundry/fine-tuning/tree/main/Demos/RFT_Countdown).
