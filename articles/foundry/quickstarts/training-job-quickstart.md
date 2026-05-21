---
title: "Quickstart: Submit a custom code training job in Microsoft Foundry"
description: "Submit your first custom code training job in Microsoft Foundry. Fine-tune a model with your own training script using the Python SDK in under 15 minutes."
author: soumyapatro
ms.author: soumyapatro
ms.service: microsoft-foundry
ms.topic: quickstart
ms.date: 05/19/2026
ms.custom: training, custom-code
ai-usage: ai-assisted
#CustomerIntent: As a data scientist, I want to submit my first training job quickly so that I can validate my setup.
---

# Quickstart: Submit a training job in Microsoft Foundry

In this quickstart, you submit a custom code training job that runs a supervised fine-tuning (SFT) script on a GPU cluster in your Foundry project. By the end, you'll have a completed training job with viewable logs and outputs.

> [!div class="checklist"]
> **You will:**
> - Set up the Microsoft Foundry SDK
> - Write a minimal training script
> - Submit a training job
> - Check job status and view logs

If you don't have an Azure subscription, create a [free Azure account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn) before you begin.

## Prerequisites

[!INCLUDE [training-prerequisites](../includes/training-prerequisites.md)]

- Python 3.10 or later. For more information, see [Install Python](../includes/install-python.md).
- The Microsoft Foundry SDK installed:

  ```bash
  pip install azure-ai-projects azure-identity
  ```

## Set up the project client

Create a Python file called `submit_job.py` and initialize the Foundry project client. Replace the endpoint with your project endpoint.

```python
import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

project_client = AIProjectClient(
    endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)
```

> [!TIP]
> Find your project endpoint in the Foundry portal under **Project settings** > **Overview**.

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
    parser.add_argument("--output_dir", type=str, default="./outputs")
    args = parser.parse_args()

    tokenizer = AutoTokenizer.from_pretrained(args.model_dir)
    model = AutoModelForCausalLM.from_pretrained(args.model_dir)

    dataset = load_dataset("json", data_files="train.jsonl", split="train")

    training_config = SFTConfig(
        output_dir=args.output_dir,
        num_train_epochs=1,
        per_device_train_batch_size=4,
        logging_steps=10,
    )

    trainer = SFTTrainer(
        model=model,
        tokenizer=tokenizer,
        train_dataset=dataset,
        args=training_config,
    )

    trainer.train()
    trainer.save_model(args.output_dir)

if __name__ == "__main__":
    main()
```

## Submit the training job

Add the following code to `submit_job.py` to submit the training job.

```python
job = project_client.beta.jobs.create(
    name="my-first-sft-job",
    experiment="quickstart-experiment",
    environment="mcr.microsoft.com/azureml/curated/acpt-pytorch:latest",  # [TO VERIFY] curated image URI
    code="./src",
    command="python train.py --model_dir ${{inputs.base_model}} --output_dir ${{outputs.trained_model}}",
    compute="my-gpu-cluster",
    instance_count=1,
    process_per_node=1,
)

print(f"Job submitted: {job.name}, Status: {job.status}")
```

Run the script to submit the job:

```bash
python submit_job.py
```

```output
Job submitted: my-first-sft-job, Status: Starting
```

## Check job status and view logs

Poll the job status and retrieve logs after the job starts running.

```python
# Check job status
job = project_client.beta.jobs.get(name="my-first-sft-job")
print(f"Job: {job.name}, Status: {job.status}")

# View logs
logs = project_client.beta.jobs.get_logs(name="my-first-sft-job")
for line in logs:
    print(line)
```

```output
Job: my-first-sft-job, Status: Running
```

You can also view the job in the Foundry portal. Go to your project and select **Jobs** in the left navigation to see the job status, logs, and metrics.

## Clean up resources

[!INCLUDE [clean-up-resources](../includes/clean-up-resources.md)]

## Next step

> [!div class="nextstepaction"]
> [Submit a training job with full configuration](../how-to/training/submit-training-job.md)
