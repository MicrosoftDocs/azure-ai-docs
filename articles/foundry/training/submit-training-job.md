---
title: Submit a custom code training job in Microsoft Foundry
description: "Submit and manage custom code training jobs in Microsoft Foundry using the Python SDK or Foundry CLI. Configure inputs, outputs, compute, distribution, and experiments."
author: soumyapatro
ms.author: soumyapatro
ms.service: microsoft-foundry
ms.topic: how-to
ms.date: 05/21/2026
ms.custom: training, custom-code
ai-usage: ai-assisted
#CustomerIntent: As a data scientist, I want to submit a training job with full control over all parameters so that I can train a foundation model.
---

# Submit a training job in Microsoft Foundry

Submit a custom code training job to run your training script on a compute cluster in your Microsoft Foundry project. This article covers the full set of job parameters including inputs, outputs, compute, distribution, and lifecycle management.

For a minimal first job, see [Quickstart: Submit a training job](../quickstarts/training-job-quickstart.md).

## Prerequisites

Before you submit a training job, complete the following setup:

- [Set up compute for training](setup-compute.md) — a compute cluster attached to your project.
- [Set up training environments](setup-training-environment.md) — a curated or custom Docker environment.
- [Work with data](work-with-data.md) — training data accessible from your project.
- [Work with models](work-with-models.md) — a base model available as input (if needed).
- The Microsoft Foundry SDK installed:

  ```bash
  pip install "azure-ai-projects>=2.0.0" azure-identity
  ```

## Initialize the project client

# [Python SDK](#tab/python)

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

# [Foundry CLI (Private Preview)](#tab/cli)

```bash
az login
foundry config set project <your-project-endpoint>
```

> [!IMPORTANT]
> The Foundry CLI for training is in Private Preview. Command syntax might change before general availability.

---

## Understand the CommandJob model

Training jobs use the `CommandJob` class. Build a `CommandJob` object with your configuration and pass it to `create_or_update()`:

| Parameter | Required | Description |
|-----------|----------|-------------|
| `display_name` | No | A human-readable name for the job |
| `command` | Yes | The shell command to run. Use `${{inputs.<name>}}` and `${{outputs.<name>}}` as placeholders for input/output paths. |
| `environment_image_reference` | Yes | A Docker image URI (ACR or curated) |
| `compute` | Yes | Full resource ID of the GPU compute cluster |
| `inputs` | No | Dictionary of `Input` objects for data, models, code, and scalar values |
| `outputs` | No | Dictionary of `Output` objects for trained models and artifacts |
| `resources` | No | `JobResourceConfiguration` specifying `instance_count` (number of nodes) |
| `distribution` | No | `PyTorchDistribution` or `RayDistribution` for multi-GPU/node training |
| `environment_variables` | No | Dictionary of environment variables to set in the job |
| `tags` | No | Dictionary of metadata tags (visible in portal) |
| `properties` | No | Dictionary of system properties |
| `description` | No | Free-text description of the job |

## Configure inputs and outputs

Inputs pass data, models, code, and scalar values to your training script. Outputs capture trained models and artifacts. For full details, see [Work with data](work-with-data.md) and [Work with models](work-with-models.md).

### Upload code as an input

Training code is passed as an input, not as a separate `code` parameter. You can upload a local folder directly or reference a dataset:

```python
# TODO: Update when code does not need to be manually uploaded as dataset
# Option 1: Local folder (auto-uploaded by the SDK)
code_input = Input(path="./src", type=AssetTypes.URI_FOLDER)

# Option 2: Pre-uploaded dataset
code_input = Input(
    path="azureai://accounts/<acct>/projects/<proj>/data/my-code/versions/1",
    type=AssetTypes.URI_FOLDER,
    mode=InputOutputModes.READ_ONLY_MOUNT,
)
```

For large code folders that you iterate on frequently, upload as a versioned dataset:

```python
code_dataset = project_client.datasets.upload_folder(
    name="my-training-code",
    version="1",
    folder="./src",
)
code_input = Input(
    path=code_dataset.id,
    type=AssetTypes.URI_FOLDER,
    mode=InputOutputModes.READ_ONLY_MOUNT,
)
```

### Define data and model inputs

```python
# Data input — mount a dataset folder
train_data = Input(
    path="azureml://datastores/mydatastore/paths/sft-data/",
    type=AssetTypes.URI_FOLDER,
    mode=InputOutputModes.READ_ONLY_MOUNT,
)

# Model input — mount from catalog
base_model = Input(
    path="azureml://registries/azureml-meta/models/Meta-Llama-3-8B/versions/1",
    type=AssetTypes.CUSTOM_MODEL,
    mode=InputOutputModes.READ_ONLY_MOUNT,
)
```

### Define outputs

```python
model_output = Output(
    type=AssetTypes.CUSTOM_MODEL,
    mode=InputOutputModes.READ_WRITE_MOUNT,
    asset_name="my-llama-sft-model",
)
```

Use `${{inputs.<name>}}` and `${{outputs.<name>}}` as placeholders in the command string. These resolve to local paths on the compute node at runtime.

## Configure distribution

For multi-node or multi-GPU training, set the `distribution` parameter. Foundry configures the required environment variables and rendezvous points automatically.

### PyTorch distribution

[] TODO: Verify auto configuration, manual or manual override.

PyTorch distribution uses `torch.distributed` with NCCL backend. Foundry auto-configures `MASTER_ADDR`, `MASTER_PORT`, `WORLD_SIZE`, `RANK`, and `LOCAL_RANK`.

```python
from azure.ai.projects.models import PyTorchDistribution

distribution = PyTorchDistribution(process_count_per_instance=8)
```

| Environment variable | Description |
|---------------------|-------------|
| `MASTER_ADDR` | Address of the rank-0 node |
| `MASTER_PORT` | Port for distributed communication |
| `WORLD_SIZE` | Total number of processes |
| `RANK` | Global rank of the current process |
| `LOCAL_RANK` | Local rank on the current node |

## Submit the job

# [Python SDK](#tab/python)

```python
job = CommandJob(
    display_name="llama-sft",
    description="SFT fine-tuning Llama-3-8B on custom dataset",
    command=(
        'python "${{inputs.code}}/train.py"'
        ' --model_dir "${{inputs.base_model}}"'
        ' --train_data "${{inputs.train_data}}"'
        ' --output_dir "${{outputs.trained_model}}"'
    ),
    environment_image_reference=os.environ["JOB_ENVIRONMENT_IMAGE"],
    compute=os.environ["JOB_COMPUTE_ID"],
    inputs={
        "code": Input(path="./src", type=AssetTypes.URI_FOLDER),
        "base_model": base_model,
        "train_data": train_data,
    },
    outputs={
        "trained_model": model_output,
    },
    resources=JobResourceConfiguration(instance_count=2),
    distribution=PyTorchDistribution(process_count_per_instance=8),
    environment_variables={
        "NCCL_NVLS_ENABLE": "1",
    },
    tags={"scenario": "sft", "base_model": "llama-3-8b"},
)

# Validate first (optional)
validation = project_client.beta.jobs.validate(job)
print(validation)

# Submit the job
created_job = project_client.beta.jobs.create_or_update(
    name="llama-sft-run1", job=job
)
print(f"Job submitted: {created_job.name}")
print(f"Status: {created_job.status}")
```

```output
Job submitted: llama-sft-run1
Status: Starting
```

# [Foundry CLI (Private Preview)](#tab/cli)

```bash
foundry training jobs create \
    --name llama-sft-run1 \
    --display-name llama-sft \
    --environment-image myregistry.azurecr.io/my-training:v1 \
    --command "python train.py --model_dir \${{inputs.base_model}} --output_dir \${{outputs.trained_model}}" \
    --compute $JOB_COMPUTE_ID \
    --instance-count 2 \
    --distribution pytorch \
    --process-count-per-instance 8
```

> [!IMPORTANT]
> The Foundry CLI for training is in Private Preview. Command syntax might change before general availability.

---

## List and get jobs

# [Python SDK](#tab/python)

```python
# List all jobs
for listed_job in project_client.beta.jobs.list():
    print(f"{listed_job.name}: {listed_job.status}")

# Get a specific job
job = project_client.beta.jobs.get(name="llama-sft-run1")
print(f"Job: {job.name}, Status: {job.status}")
```

# [Foundry CLI (Private Preview)](#tab/cli)

```bash
foundry training jobs list
foundry training jobs show --name llama-sft-run1
```

---

## Cancel a job

# [Python SDK](#tab/python)

```python
cancel_poller = project_client.beta.jobs.begin_cancel("llama-sft-run1")
cancel_poller.result()
print("Job cancelled.")
```

# [Foundry CLI (Private Preview)](#tab/cli)

```bash
foundry training jobs cancel --name llama-sft-run1
```

---

## Download job outputs

Download outputs from a completed job to inspect results locally:

```python
project_client.beta.jobs.download(name="llama-sft-run1", all=True)
print("Outputs downloaded.")
```

## Related content

- [Monitor training jobs](monitor-training-jobs.md)
- [Track experiments with MLflow](track-experiments-mlflow.md)
- [Save and deploy trained models](save-deploy-trained-model.md)
- [What is custom code training?](../concepts/custom-training-overview.md)
