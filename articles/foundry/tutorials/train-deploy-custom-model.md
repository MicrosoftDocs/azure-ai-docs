---
title: "Tutorial: Train and deploy a model with custom code in Microsoft Foundry"
description: "Walk through an end-to-end workflow: prepare data, write a training script with MLflow, submit a training job, save the model, and deploy it for inference in Microsoft Foundry."
author: soumyapatro
ms.author: soumyapatro
ms.service: microsoft-foundry
ms.topic: tutorial
ms.date: 05/19/2026
ms.custom: training, custom-code
ai-usage: ai-assisted
#CustomerIntent: As a data scientist, I want to walk through a complete end-to-end workflow from data prep to deployment so that I can learn custom code training in Foundry.
---

# Tutorial: Train and deploy a model with custom code

In this tutorial, you fine-tune a Llama model using HuggingFace TRL on Foundry GPU compute, track metrics with MLflow, save the model, and deploy it for inference.

> [!div class="checklist"]
> **In this tutorial, you:**
> - Prepare a training dataset
> - Write a training script with SFT and MLflow logging
> - Submit a multi-node distributed training job
> - Monitor training progress and metrics
> - Save the trained model as a model asset
> - Deploy the model and test it with a chat completion request

## Prerequisites

[!INCLUDE [training-prerequisites](../includes/training-prerequisites.md)]

- A GPU compute cluster with at least 2 nodes. For more information, see [Set up compute for training](../how-to/training/setup-compute.md).
- An environment with TRL, MLflow, and `azureml-mlflow`. For more information, see [Use custom environments](../how-to/training/use-custom-environments.md).
- Python 3.10 or later and the Microsoft Foundry SDK installed:

  ```bash
  pip install azure-ai-projects azure-identity
  ```

## Prepare the training data

Create a training dataset in JSONL format for supervised fine-tuning. Each line contains a conversation with instruction-response pairs.

Create a file called `train.jsonl`:

```json
{"messages": [{"role": "user", "content": "What is reinforcement learning from human feedback?"}, {"role": "assistant", "content": "Reinforcement learning from human feedback (RLHF) is a technique that uses human preferences to train reward models, which then guide policy optimization of language models to produce outputs better aligned with human intent."}]}
{"messages": [{"role": "user", "content": "Explain the difference between SFT and DPO."}, {"role": "assistant", "content": "Supervised fine-tuning (SFT) trains a model on demonstration data to mimic desired behavior. Direct preference optimization (DPO) skips the reward model step and directly optimizes the policy using preference pairs, making it simpler to implement while achieving similar alignment quality."}]}
```

Upload the dataset to your project's datastore:

```python
import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.projects.models import Input, Output

project_client = AIProjectClient(
    endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)

# Upload data to managed storage
# [TO VERIFY] Data upload SDK signature
train_data = Input(
    type="uri_file",
    path="azureml://datastores/workspaceblobstore/paths/training/train.jsonl",
    mode="download",
)
```

## Write the training script

Create a folder called `src` and add a file called `train.py`. This script uses HuggingFace TRL for SFT and logs metrics with MLflow.

```python
# src/train.py
import argparse
import mlflow
from datasets import load_dataset
from transformers import AutoModelForCausalLM, AutoTokenizer
from trl import SFTTrainer, SFTConfig

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_dir", type=str, required=True, help="Path to base model")
    parser.add_argument("--data_file", type=str, required=True, help="Path to training data")
    parser.add_argument("--output_dir", type=str, required=True, help="Path to save trained model")
    parser.add_argument("--num_epochs", type=int, default=3)
    parser.add_argument("--batch_size", type=int, default=4)
    parser.add_argument("--learning_rate", type=float, default=2e-5)
    args = parser.parse_args()

    # Log hyperparameters to MLflow
    mlflow.log_param("num_epochs", args.num_epochs)
    mlflow.log_param("batch_size", args.batch_size)
    mlflow.log_param("learning_rate", args.learning_rate)

    # Load model and tokenizer
    tokenizer = AutoTokenizer.from_pretrained(args.model_dir)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(
        args.model_dir,
        torch_dtype="auto",
        device_map="auto",
    )

    # Load dataset
    dataset = load_dataset("json", data_files=args.data_file, split="train")

    # Configure training
    training_config = SFTConfig(
        output_dir=args.output_dir,
        num_train_epochs=args.num_epochs,
        per_device_train_batch_size=args.batch_size,
        learning_rate=args.learning_rate,
        logging_steps=10,
        save_steps=100,
        report_to="mlflow",
        bf16=True,
    )

    # Train
    trainer = SFTTrainer(
        model=model,
        tokenizer=tokenizer,
        train_dataset=dataset,
        args=training_config,
    )

    trainer.train()

    # Save final model
    trainer.save_model(args.output_dir)
    tokenizer.save_pretrained(args.output_dir)

    # Log final metrics
    mlflow.log_metric("final_train_loss", trainer.state.log_history[-1].get("loss", 0))
    print(f"Training complete. Model saved to {args.output_dir}")

if __name__ == "__main__":
    main()
```

## Submit the training job

Submit a distributed training job that runs the SFT script across multiple nodes.

```python
base_model = Input(
    type="model",
    path="azureml://registries/azureml-openai-oss/models/Meta-Llama-3-8B/versions/1",
    mode="download",
)

model_output = Output(
    type="safetensor_model",
    name="llama-3-8b-sft",
)

job = project_client.beta.jobs.create(
    name="llama-sft-tutorial",
    experiment="llama-sft-tutorial",
    environment="myregistry.azurecr.io/my-training:v1",
    code="./src",
    command=(
        "python train.py "
        "--model_dir ${{inputs.base_model}} "
        "--data_file ${{inputs.train_data}} "
        "--output_dir ${{outputs.trained_model}} "
        "--num_epochs ${{inputs.num_epochs}} "
        "--batch_size ${{inputs.batch_size}} "
        "--learning_rate ${{inputs.learning_rate}}"
    ),
    compute="gpu-cluster",
    instance_count=2,
    process_per_node=4,
    distribution="PyTorch",
    inputs={
        "base_model": base_model,
        "train_data": train_data,
        "num_epochs": 3,
        "batch_size": 4,
        "learning_rate": 2e-5,
    },
    outputs={
        "trained_model": model_output,
    },
)

print(f"Job submitted: {job.name}, Status: {job.status}")
```

```output
Job submitted: llama-sft-tutorial, Status: Starting
```

## Monitor training progress

### Check job status

```python
import time

while True:
    job = project_client.beta.jobs.get(name="llama-sft-tutorial")
    print(f"Status: {job.status}")
    if job.status in ["Completed", "Failed", "Cancelled"]:
        break
    time.sleep(60)
```

### Tail logs

```python
logs = project_client.beta.jobs.get_logs(name="llama-sft-tutorial")
for line in logs:
    print(line)
```

```output
[2026-05-19 10:35:12] Loading model from /mnt/inputs/base_model...
[2026-05-19 10:40:00] Model loaded. Starting SFT training...
[2026-05-19 10:40:15] Epoch 1/3, Step 10, Loss: 2.4532, LR: 1.98e-05
[2026-05-19 10:40:30] Epoch 1/3, Step 20, Loss: 2.1287, LR: 1.95e-05
[2026-05-19 10:45:00] Epoch 1/3, Step 100, Loss: 1.5432, LR: 1.80e-05
...
[2026-05-19 11:30:00] Training complete. Model saved to /mnt/outputs/trained_model
```

### View metrics in the portal

1. Go to your project in the [Foundry portal](https://ai.azure.com).
1. Select **Jobs** > **llama-sft-tutorial**.
1. Select the **Metrics** tab to view loss curves and learning rate schedules.

## Save the trained model

When the job completes with status `Completed`, the model output is automatically registered as a model asset.

Verify the model asset:

```python
# List models in the project
models = project_client.models.list()
for m in models:
    print(f"Model: {m.name}, Version: {m.version}")
```

```output
Model: llama-3-8b-sft, Version: 1
```

You can also view the model in the portal by selecting **Jobs** > **llama-sft-tutorial** > **Models** tab.

## Deploy the model

Deploy the trained model for inference.

### Deploy in the portal

1. Select **Jobs** > **llama-sft-tutorial** > **Models** tab.
1. Select **llama-3-8b-sft**.
1. Map the model to the **Meta-Llama-3-8B** base architecture.
1. Select **Deploy** and configure the deployment settings.
1. Wait for the deployment to become active.

## Test the deployment

Send a chat completion request to verify the deployed model:

```python
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

client = OpenAI(
    base_url=f"{os.environ['AZURE_AI_PROJECT_ENDPOINT']}/openai/v1/",
    api_key=token_provider(),
)

response = client.chat.completions.create(
    model="llama-3-8b-sft",
    messages=[
        {"role": "user", "content": "What is the difference between SFT and RLHF?"}
    ],
    max_tokens=200,
)

print(response.choices[0].message.content)
```

```output
Supervised fine-tuning (SFT) trains a language model directly on demonstration data,
teaching it to mimic desired input-output behavior. RLHF adds a second stage where a
reward model trained on human preferences guides policy optimization, allowing the
model to generalize beyond the demonstration data and better align with nuanced human
preferences.
```

## Clean up resources

[!INCLUDE [clean-up-resources](../includes/clean-up-resources.md)]

## Next step

> [!div class="nextstepaction"]
> [Track experiments with MLflow](../how-to/training/track-experiments-mlflow.md)

## Related content

- [What is custom code training?](../concepts/custom-training-overview.md)
- [Monitor training jobs](../how-to/training/monitor-training-jobs.md)
- [Save and deploy trained models](../how-to/training/save-deploy-trained-model.md)
- [Debug jobs interactively](../how-to/training/debug-jobs-interactively.md)
