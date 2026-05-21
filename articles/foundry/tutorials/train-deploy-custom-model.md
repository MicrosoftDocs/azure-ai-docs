---
title: "Tutorial: Train and deploy a custom model in Microsoft Foundry"
description: "End-to-end tutorial for training and deploying a custom model in Microsoft Foundry. Prepare data, configure a training job, monitor training, and save the model."
author: soumyapatro
ms.author: soumyapatro
ms.service: microsoft-foundry
ms.topic: tutorial
ms.date: 05/21/2026
ms.custom: training, custom-code
ai-usage: ai-assisted
#CustomerIntent: As a data scientist, I want to follow an end-to-end tutorial so that I can learn the full training workflow.
---

# Tutorial: Train and deploy a custom model

In this tutorial, you train a custom model from start to finish using Microsoft Foundry. You prepare training data, write a supervised fine-tuning (SFT) script, submit a multi-GPU training job, monitor progress, and save the trained model.

> [!div class="checklist"]
> **In this tutorial, you:**
> - Prepare and upload a training dataset
> - Write an SFT training script
> - Submit a distributed training job
> - Monitor training with logs and MLflow
> - Save and register the trained model

## Prerequisites

[!INCLUDE [training-prerequisites](../includes/training-prerequisites.md)]

- Python 3.10 or later.
- The Microsoft Foundry SDK installed:

  ```bash
  pip install "azure-ai-projects>=2.0.0" azure-identity
  ```

## Set up the project

Create a project directory with the following structure:

```
tutorial-sft/
├── src/
│   └── train_sft.py
├── data/
│   └── train.jsonl
└── submit_job.py
```

Initialize the Foundry client in `submit_job.py`:

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
    PyTorchDistribution,
)

project_client = AIProjectClient(
    endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)
```

## Step 1: Prepare training data

Create a training dataset in JSONL format with chat-formatted messages. Save this file as `data/train.jsonl`:

```json
{"messages": [{"role": "system", "content": "You are a helpful coding assistant."}, {"role": "user", "content": "Write a Python function to reverse a string."}, {"role": "assistant", "content": "def reverse_string(s):\n    return s[::-1]"}]}
{"messages": [{"role": "system", "content": "You are a helpful coding assistant."}, {"role": "user", "content": "What is a list comprehension?"}, {"role": "assistant", "content": "A list comprehension is a concise way to create lists in Python using the syntax [expression for item in iterable if condition]."}]}
```

Upload the dataset to your Foundry project:

```python
dataset = project_client.datasets.upload_folder(
    name="sft-tutorial-data",
    version="1",
    folder="./data",
)
print(f"Dataset: {dataset.id}")
```

```output
Dataset: azureai://accounts/<acct>/projects/<proj>/data/sft-tutorial-data/versions/1
```

## Step 2: Write the training script

Create `src/train_sft.py` with an SFT training script. This script uses HuggingFace Transformers and TRL:

```python
# src/train_sft.py
import argparse
import mlflow
from transformers import AutoModelForCausalLM, AutoTokenizer
from trl import SFTTrainer, SFTConfig
from datasets import load_dataset

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_dir", type=str, required=True)
    parser.add_argument("--train_data", type=str, required=True)
    parser.add_argument("--output_dir", type=str, default="./outputs")
    parser.add_argument("--num_epochs", type=int, default=3)
    parser.add_argument("--batch_size", type=int, default=4)
    parser.add_argument("--learning_rate", type=float, default=2e-5)
    args = parser.parse_args()

    # Log hyperparameters
    mlflow.log_params({
        "num_epochs": args.num_epochs,
        "batch_size": args.batch_size,
        "learning_rate": args.learning_rate,
    })

    # Load tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained(args.model_dir)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(
        args.model_dir, torch_dtype="auto"
    )

    # Load dataset
    dataset = load_dataset(
        "json", data_files=f"{args.train_data}/train.jsonl", split="train"
    )

    # Configure training
    training_config = SFTConfig(
        output_dir=args.output_dir,
        num_train_epochs=args.num_epochs,
        per_device_train_batch_size=args.batch_size,
        learning_rate=args.learning_rate,
        logging_steps=10,
        save_steps=100,
        bf16=True,
        gradient_checkpointing=True,
        report_to="mlflow",
    )

    # Train
    trainer = SFTTrainer(
        model=model,
        processing_class=tokenizer,
        train_dataset=dataset,
        args=training_config,
    )

    trainer.train()

    # Save model in safetensors format for deployment eligibility
    trainer.save_model(args.output_dir)
    tokenizer.save_pretrained(args.output_dir)

    # Log final metrics
    mlflow.log_metric("final_train_loss", trainer.state.log_history[-1].get("loss", 0))
    print(f"Training complete. Model saved to {args.output_dir}")

if __name__ == "__main__":
    main()
```

## Step 3: Submit the training job

Build and submit the training job in `submit_job.py`:

```python
compute_id = os.environ["JOB_COMPUTE_ID"]
environment_image = os.environ.get(
    "JOB_ENVIRONMENT_IMAGE",
    "mcr.microsoft.com/azureml/curated/acpt-pytorch-2.2-cuda12.1:48",
)

job = CommandJob(
    display_name="tutorial-sft-llama",
    description="SFT tutorial — fine-tuning Llama-3-8B on coding dataset",
    command=(
        'python "${{inputs.code}}/train_sft.py"'
        ' --model_dir "${{inputs.base_model}}"'
        ' --train_data "${{inputs.train_data}}"'
        ' --output_dir "${{outputs.trained_model}}"'
        ' --num_epochs 3'
        ' --batch_size 4'
        ' --learning_rate 2e-5'
    ),
    environment_image_reference=environment_image,
    compute=compute_id,
    inputs={
        "code": Input(path="./src", type=AssetTypes.URI_FOLDER),
        "base_model": Input(
            path="azureml://registries/azureml-meta/models/Meta-Llama-3-8B/versions/1",
            type=AssetTypes.URI_FOLDER,
            mode=InputOutputModes.READ_ONLY_MOUNT,
        ),
        "train_data": Input(
            path=dataset.id,
            type=AssetTypes.URI_FOLDER,
            mode=InputOutputModes.READ_ONLY_MOUNT,
        ),
    },
    outputs={
        "trained_model": Output(
            type=AssetTypes.URI_FOLDER,
            mode=InputOutputModes.READ_WRITE_MOUNT,
            asset_name="tutorial-sft-model",
        ),
    },
    resources=JobResourceConfiguration(instance_count=1),
    environment_variables={
        "NCCL_NVLS_ENABLE": "1",
    },
    tags={
        "scenario": "tutorial-sft",
        "base_model": "llama-3-8b",
    },
)

created_job = project_client.beta.jobs.create_or_update(
    name="tutorial-sft-run1", job=job
)
print(f"Job submitted: {created_job.name}")
print(f"Status: {created_job.status}")
```

```output
Job submitted: tutorial-sft-run1
Status: Starting
```

## Step 4: Monitor training

### Stream logs

```python
project_client.beta.jobs.stream(name="tutorial-sft-run1")
```

### Check status

```python
job = project_client.beta.jobs.get(name="tutorial-sft-run1")
print(f"Status: {job.status}")
```

### View in the portal

1. Go to your project in the [Foundry portal](https://ai.azure.com).
1. Select **Jobs** in the left navigation.
1. Select **tutorial-sft-run1** to view logs, metrics, and infrastructure utilization.

## Step 5: Save the trained model

The trained model is auto-registered because you specified `asset_name="tutorial-sft-model"` on the output. Verify the registration:

```python
model = project_client.models.get(name="tutorial-sft-model", version="latest")
print(f"Model: {model.name}, Version: {model.version}")
```

Download the model for local inspection:

```python
project_client.beta.jobs.download(name="tutorial-sft-run1", all=True)

from transformers import AutoModelForCausalLM, AutoTokenizer
model = AutoModelForCausalLM.from_pretrained("./outputs/trained_model")
tokenizer = AutoTokenizer.from_pretrained("./outputs/trained_model")

inputs = tokenizer("Write a function to sort a list:", return_tensors="pt")
outputs = model.generate(**inputs, max_new_tokens=100)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))
```

## Clean up resources

[!INCLUDE [clean-up-resources](../includes/clean-up-resources.md)]

## Next step

> [!div class="nextstepaction"]
> [Save and deploy trained models](../training/save-deploy-trained-model.md)
