---
title: "Quickstart: Submit a custom code training job in Microsoft Foundry"
description: "Submit your first custom code training job in Microsoft Foundry. Fine-tune a model with your own training script using the Python SDK in under 15 minutes."
author: soumyapatro
ms.author: soumyapatro
ms.service: microsoft-foundry
ms.topic: quickstart
ms.date: 05/21/2026
ms.custom: training, custom-code
ai-usage: ai-assisted
#CustomerIntent: As a data scientist, I want to submit my first training job quickly so that I can validate my setup.
---

# Quickstart: Submit a training job in Microsoft Foundry

In this quickstart, you submit a custom code training job that runs a supervised fine-tuning (SFT) script on a GPU cluster in your Foundry project. By the end, you have a completed training job with viewable logs and outputs.

> [!div class="checklist"]
> **You will:**
> - Set up the Microsoft Foundry SDK
> - Write a minimal training script
> - Submit a training job
> - Stream job logs and check results

If you don't have an Azure subscription, create a [free Azure account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn) before you begin.

## Prerequisites

[!INCLUDE [training-prerequisites](../includes/training-prerequisites.md)]

- Python 3.10 or later. For more information, see [Install Python](../includes/install-python.md).
- The Microsoft Foundry SDK installed:

  ```bash
  pip install "azure-ai-projects>=2.0.0" azure-identity
  ```

## Set up the project client

Create a Python file called `submit_job.py` and initialize the Foundry project client.

```python
import os
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    CommandJob,
    JobResourceConfiguration,
    Input,
    Output,
    AssetTypes,
    InputOutputModes,
)

project_client = AIProjectClient(
    endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)
```

> [!TIP]
> Find your project endpoint in the Foundry portal under **Project settings** > **Overview**. Set it as the `FOUNDRY_PROJECT_ENDPOINT` environment variable.

## Prepare a training script

Create a folder called `src` and add a file called `train.py` with a minimal SFT training script.

```python
# src/train.py
import argparse
from transformers import AutoModelForCausalLM, AutoTokenizer
from trl import SFTTrainer, SFTConfig
from datasets import load_dataset

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_dir", type=str, required=True)
    parser.add_argument("--train_data", type=str, required=True)
    parser.add_argument("--output_dir", type=str, default="./outputs")
    args = parser.parse_args()

    tokenizer = AutoTokenizer.from_pretrained(args.model_dir)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(
        args.model_dir, torch_dtype="auto"
    )

    dataset = load_dataset(
        "json", data_files=args.train_data, split="train"
    )

    training_config = SFTConfig(
        output_dir=args.output_dir,
        num_train_epochs=1,
        per_device_train_batch_size=4,
        logging_steps=10,
        bf16=True,
    )

    trainer = SFTTrainer(
        model=model,
        processing_class=tokenizer,
        train_dataset=dataset,
        args=training_config,
    )

    trainer.train()
    trainer.save_model(args.output_dir)
    print(f"Training complete. Model saved to {args.output_dir}")

if __name__ == "__main__":
    main()
```

Also create a sample training data file at `data/train.jsonl`:

```json
{"messages": [{"role": "user", "content": "What is SFT?"}, {"role": "assistant", "content": "Supervised fine-tuning (SFT) trains a model on demonstration data to align its behavior with desired outputs."}]}
```

## Submit the training job

Add the following code to `submit_job.py` to build and submit the training job. The SDK uploads your local `src` and `data` folders automatically when you pass them as inputs with a local path.

```python
compute_id = os.environ["JOB_COMPUTE_ID"]
environment_image = os.environ.get(
    "JOB_ENVIRONMENT_IMAGE",
    "mcr.microsoft.com/azureml/curated/acpt-pytorch-2.2-cuda12.1:48",
)

job = CommandJob(
    display_name="my-first-sft-job",
    command=(
        'python "${{inputs.code}}/train.py"'
        ' --model_dir "${{inputs.base_model}}"'
        ' --train_data "${{inputs.train_data}}/train.jsonl"'
        ' --output_dir "${{outputs.trained_model}}"'
    ),
    environment_image_reference=environment_image,
    compute=compute_id,
    inputs={
        "code": Input(
            path="./src",
            type=AssetTypes.URI_FOLDER,
        ),
        "base_model": Input(
            path="azureml://registries/azureml-meta/models/Meta-Llama-3-8B/versions/1",
            type=AssetTypes.URI_FOLDER,
            mode=InputOutputModes.READ_ONLY_MOUNT,
        ),
        "train_data": Input(
            path="./data",
            type=AssetTypes.URI_FOLDER,
        ),
    },
    outputs={
        "trained_model": Output(
            type=AssetTypes.URI_FOLDER,
            mode=InputOutputModes.READ_WRITE_MOUNT,
        ),
    },
    resources=JobResourceConfiguration(instance_count=1),
)

created_job = project_client.beta.jobs.create_or_update(
    name="my-first-sft-job", job=job
)
print(f"Job submitted: {created_job.name}")
print(f"Status: {created_job.status}")
```

```output
Job submitted: my-first-sft-job
Status: Starting
```

Run the script:

```bash
python submit_job.py
```

> [!NOTE]
> `JOB_COMPUTE_ID` is the full resource ID of your compute cluster, in the format `/subscriptions/<sub>/resourceGroups/<rg>/providers/microsoft.cognitiveservices/accounts/<account>/computes/<cluster>`. Find it in the Foundry portal under **Compute** > your cluster > **Properties**.

## Check job status and stream logs

Check the job status and stream logs to monitor training progress.

```python
retrieved_job = project_client.beta.jobs.get(name="my-first-sft-job")
print(f"Job: {retrieved_job.name}")
print(f"Status: {retrieved_job.status}")

# Stream logs (blocks until job completes)
project_client.beta.jobs.stream(name="my-first-sft-job")
```

```output
Job: my-first-sft-job
Status: Running
```

You can also view the job in the Foundry portal. Go to your project and select **Jobs** in the left navigation to see the job status, logs, and metrics.

## Clean up resources

[!INCLUDE [clean-up-resources](../includes/clean-up-resources.md)]

## Next step

> [!div class="nextstepaction"]
> [Submit a training job with full configuration](../training/submit-training-job.md)
