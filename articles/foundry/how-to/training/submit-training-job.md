---
title: Submit a custom code training job in Microsoft Foundry
description: "Submit and manage custom code training jobs in Microsoft Foundry using the Python SDK or Foundry CLI. Configure inputs, outputs, compute, distribution, and experiments."
author: soumyapatro
ms.author: soumyapatro
ms.service: microsoft-foundry
ms.topic: how-to
ms.date: 05/19/2026
ms.custom: training, custom-code
ai-usage: ai-assisted
#CustomerIntent: As a data scientist, I want to submit a training job with full control over all parameters so that I can train a foundation model.
---

# Submit a training job in Microsoft Foundry

Submit a custom code training job to run your training script on GPU compute in your Microsoft Foundry project. This article covers the full set of job parameters including inputs, outputs, compute, distribution, experiments, and lifecycle management.

For a minimal first job, see [Quickstart: Submit a training job](../../quickstarts/training-job-quickstart.md).

## Prerequisites

Before you submit a training job, complete the following setup:

- [Set up compute for training](setup-compute.md) — a GPU compute cluster attached to your project.
- [Use custom environments](use-custom-environments.md) — a curated or custom Docker environment.
- [Work with data](work-with-data.md) — training data accessible from your project.
- [Work with models](work-with-models.md) — a base model available as input (if needed).
- The Microsoft Foundry SDK installed:

  ```bash
  pip install azure-ai-projects azure-identity
  ```

## Initialize the project client

# [Python SDK](#tab/python)

```python
import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

project_client = AIProjectClient(
    endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)
```

# [Foundry CLI (Private Preview)](#tab/cli)

```bash
# Sign in and set the default project
az login
foundry config set project <your-project-endpoint>
```

> [!IMPORTANT]
> The Foundry CLI for training is in Private Preview. Command syntax might change before general availability.

---

## Define job parameters

A training job requires the following core parameters:

| Parameter | Required | Description |
|-----------|----------|-------------|
| `name` | Yes | A unique name for the job |
| `experiment` | No | A named grouping for related job runs. Use to organize and compare runs. |
| `environment` | Yes | A Docker image URI (ACR or curated) |
| `code` | Yes | Path to the local folder containing your training script |
| `command` | Yes | The shell command to run. Use `${{inputs.<name>}}` and `${{outputs.<name>}}` placeholders for input/output paths. |
| `compute` | Yes | Name of the GPU compute cluster |
| `instance_count` | No | Number of nodes for distributed training (default: 1) |
| `process_per_node` | No | Number of processes per node (default: 1). Typically matches the number of GPUs per node. |
| `distribution` | No | Distribution strategy: `"PyTorch"` or `"Ray"` |
| `inputs` | No | Dictionary of data, model, and scalar inputs |
| `outputs` | No | Dictionary of data and model outputs |

## Configure inputs and outputs

Inputs pass data, models, and hyperparameters to your training script. Outputs capture trained models and artifacts.

For full details on configuring inputs and outputs, see [Work with data](work-with-data.md) and [Work with models](work-with-models.md).

```python
from azure.ai.projects.models import Input, Output

# Data input
train_data = Input(type="uri_folder", path="azureml://datastores/mydatastore/paths/sft-data/", mode="mount")

# Model input from catalog
base_model = Input(type="model", path="azureml://registries/azureml-openai-oss/models/Meta-Llama-3-8B/versions/1", mode="download")

# Scalar inputs (hyperparameters)
batch_size = 32
learning_rate = 2e-5

# Model output
model_output = Output(type="safetensor_model", name="my-llama-sft")
```

Use `${{inputs.<name>}}` and `${{outputs.<name>}}` as placeholders in the command string. These resolve to local paths on the compute node.

## Configure distribution

For multi-node or multi-GPU training, set the `distribution` parameter. Foundry configures the required environment variables and rendezvous points automatically.

### PyTorch distribution

PyTorch distribution uses `torch.distributed` with NCCL backend. Foundry auto-configures:

| Environment variable | Value |
|---------------------|-------|
| `MASTER_ADDR` | Address of the rank-0 node |
| `MASTER_PORT` | Port for distributed communication |
| `WORLD_SIZE` | Total number of processes |
| `RANK` | Global rank of the current process |
| `LOCAL_RANK` | Local rank on the current node |

```python
job = project_client.beta.jobs.create(
    name="distributed-sft",
    compute="gpu-cluster",
    instance_count=4,
    process_per_node=8,
    distribution="PyTorch",
    # ... other parameters
)
```

### Ray distribution

Ray distribution creates a Ray cluster across the allocated nodes.

```python
job = project_client.beta.jobs.create(
    name="ray-training",
    compute="gpu-cluster",
    instance_count=2,
    process_per_node=8,
    distribution="Ray",
    # ... other parameters
)
```

## Submit the job

# [Python SDK](#tab/python)

```python
job = project_client.beta.jobs.create(
    name="llama-sft",
    experiment="sft-experiments",
    environment="myregistry.azurecr.io/my-training:v1",
    code="./src",
    command="python train.py --model_dir ${{inputs.base_model}} --data_dir ${{inputs.train}} --output_dir ${{outputs.trained_model}} --batch_size ${{inputs.batch_size}} --lr ${{inputs.learning_rate}}",
    compute="gpu-cluster",
    instance_count=2,
    process_per_node=8,
    distribution="PyTorch",
    inputs={
        "base_model": base_model,
        "train": train_data,
        "batch_size": batch_size,
        "learning_rate": learning_rate,
    },
    outputs={
        "trained_model": model_output,
    },
)

print(f"Job submitted: {job.name}, Status: {job.status}")
```

```output
Job submitted: llama-sft, Status: Starting
```

# [Foundry CLI (Private Preview)](#tab/cli)

```bash
foundry training jobs create \
    --name llama-sft \
    --experiment sft-experiments \
    --environment myregistry.azurecr.io/my-training:v1 \
    --code ./src \
    --command "python train.py --model_dir \${{inputs.base_model}} --data_dir \${{inputs.train}} --output_dir \${{outputs.trained_model}}" \
    --compute gpu-cluster \
    --instance-count 2 \
    --process-per-node 8 \
    --distribution PyTorch
```

> [!IMPORTANT]
> The Foundry CLI for training is in Private Preview. Command syntax might change before general availability.

---

## List and get jobs

# [Python SDK](#tab/python)

```python
# List all jobs
jobs = project_client.beta.jobs.list()
for j in jobs:
    print(f"{j.name}: {j.status}")

# List jobs in a specific experiment
jobs = project_client.beta.jobs.list(experiment="sft-experiments")

# Get a specific job
job = project_client.beta.jobs.get(name="llama-sft")
print(f"Job: {job.name}, Status: {job.status}")
```

# [Foundry CLI (Private Preview)](#tab/cli)

```bash
# List all jobs
foundry training jobs list

# List jobs in a specific experiment
foundry training jobs list --experiment sft-experiments

# Get a specific job
foundry training jobs show --name llama-sft
```

---

## Cancel a job

# [Python SDK](#tab/python)

```python
project_client.beta.jobs.cancel(name="llama-sft")
print("Job cancelled.")
```

# [Foundry CLI (Private Preview)](#tab/cli)

```bash
foundry training jobs cancel --name llama-sft
```

---

## Related content

- [Monitor training jobs](monitor-training-jobs.md)
- [Track experiments with MLflow](track-experiments-mlflow.md)
- [Save and deploy trained models](save-deploy-trained-model.md)
- [What is custom code training?](../../concepts/custom-training-overview.md)
