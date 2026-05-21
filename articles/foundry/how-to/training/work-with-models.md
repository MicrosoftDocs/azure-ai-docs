---
title: Work with models in training jobs in Microsoft Foundry
description: "Pass base models as inputs to training jobs and save trained models as outputs. Register model assets manually or through auto-registration in Microsoft Foundry."
author: soumyapatro
ms.author: soumyapatro
ms.service: microsoft-foundry
ms.topic: how-to
ms.date: 05/19/2026
ms.custom: training, custom-code
ai-usage: ai-assisted
#CustomerIntent: As a data scientist, I want to pass a base model as input to my training job and save the trained model as output.
---

# Work with models in training jobs

Training jobs in Microsoft Foundry can use model assets as inputs and produce model assets as outputs. Pass a base model from the Foundry model catalog, your project, or your own storage as a job input. Define model outputs so that trained weights are automatically registered as model assets in your project.

## Prerequisites

[!INCLUDE [training-prerequisites](../../includes/training-prerequisites.md)]

## Understand model assets

Model assets represent packaged artifacts (weights, configuration, tokenizer, and metadata) that you can use as training job inputs and, when eligible, deploy for inference. Model assets are created through three paths:

| Creation path | Description |
|---------------|-------------|
| **Manual import** | Register an existing model folder as a model asset |
| **Training job auto-registration** | A training job automatically registers its output as a model asset |
| **Create from dataset** | Create a model asset that references a dataset as its source (for checkpoints) |

## Pass a model as job input

Specify a model input so your training script can access the base model weights on the compute node.

### From the Foundry model catalog

Pass an open-weight model from the catalog as input:

```python
from azure.ai.projects.models import Input

base_model = Input(
    type="model",
    path="azureml://registries/azureml-openai-oss/models/Meta-Llama-3-8B/versions/1",
    mode="download",
)

job = project_client.beta.jobs.create(
    name="llama-sft",
    inputs={"base_model": base_model},
    command="python train.py --model_dir ${{inputs.base_model}}",
    # ... other parameters
)
```

### From your project

Pass a model already registered in your project:

```python
base_model = Input(
    type="model",
    path="azureml://models/my-pretrained-model/versions/1",
    mode="mount",
)
```

### From your own storage

Pass model weights stored in Azure Blob or ADLS:

```python
base_model = Input(
    type="uri_folder",
    path="azureml://datastores/mydatastore/paths/models/llama-3-8b/",
    mode="mount",
)
```

### Access modes for model inputs

| Access mode | Description | When to use |
|------------|-------------|-------------|
| `mount` | Model files are accessed on demand from storage | Large models where you want to avoid full download wait time |
| `download` | Model files are copied to the compute node before the job starts | When your training script needs fast random access to all model files |

## Define model outputs

Specify model outputs in the job specification so that trained weights are saved and optionally registered as model assets when the job completes.

### Model output asset types

| Asset type | Description | Auto-registered | Deployable |
|-----------|-------------|-----------------|------------|
| `SAFETENSOR_MODEL` | Model weights in safetensors format | Yes | Yes |
| `CUSTOM_MODEL` | Custom model format | Yes | Yes |
| `URI_FOLDER` | General folder output (for example, multiple checkpoints) | No | No |

### Example: Define model outputs

```python
from azure.ai.projects.models import Output

model_output = Output(
    type="safetensor_model",
    name="my-llama-sft",
)

checkpoint_output = Output(
    type="uri_folder",
)

job = project_client.beta.jobs.create(
    name="llama-sft",
    inputs={"base_model": base_model},
    outputs={"trained_model": model_output, "checkpoints": checkpoint_output},
    command="python train.py --model_dir ${{inputs.base_model}} --output_dir ${{outputs.trained_model}} --checkpoint_dir ${{outputs.checkpoints}}",
    # ... other parameters
)
```

When the job completes, outputs of type `SAFETENSOR_MODEL` or `CUSTOM_MODEL` are automatically registered as model assets in your Foundry project.

## Register a model asset manually

Register an existing model folder as a model asset. Use manual registration when you want to import a model from local storage or register a specific checkpoint after inspecting job outputs.

```python
from azure.ai.projects.models import CustomModel, ModelSource

model = project_client.models.create_or_update(
    CustomModel(
        name="my-llama-sft",
        version="1",
        type="FullWeight",
        source=ModelSource(
            source_type="Local",
            path="./my-model-folder",
        ),
    )
)
print(f"Model registered: {model.name}, Version: {model.version}")
```

## Save multiple checkpoints

Save multiple checkpoints during training by writing them to a `URI_FOLDER` output. After the job completes, inspect the checkpoints and register the best one as a model asset.

Your training script writes checkpoints to the output folder:

```python
# In your training script
trainer.save_model(f"{args.checkpoint_dir}/checkpoint_{step}")
```

After the job completes, create a model asset from a specific checkpoint:

```python
model = project_client.models.create_or_update(
    CustomModel(
        name="my-llama-best-checkpoint",
        version="1",
        type="FullWeight",
        base_model="azureml://registries/azureml-openai-oss/models/Meta-Llama-3-8B/versions/1",
        source=ModelSource(
            source_type="TrainingJob",
            job_name="llama-sft",
            job_output_path="checkpoints/checkpoint_500/",
        ),
    )
)
```

## Inspect models interactively

Download a registered model asset to a compute instance for debugging, inspection, or lightweight experiments.

```python
local_path = project_client.models.download(
    name="my-llama-sft",
    version="1",
    download_path="./my-local-model",
)

from transformers import AutoModel
model = AutoModel.from_pretrained(local_path)
```

## Allowed files and deployment eligibility

All files are accepted at upload and registration time to avoid blocking experimentation. However, a model asset is deployable only if it meets these constraints:

- Weights are in **safetensors** format.
- Auxiliary artifacts are limited to **non-executable formats** (for example, JSON, `.md` files).
- **No executable files** are present.

If your model contains non-compliant files, remove them before deployment. For more information about deploying trained models, see [Save and deploy trained models](save-deploy-trained-model.md).

## Model storage

By default, model assets are stored in managed storage within your Foundry project.

> [!NOTE]
> Storage size limits and quotas per project are subject to your subscription tier. `[TO VERIFY]`

## Related content

- [Work with data in training jobs](work-with-data.md)
- [Save and deploy trained models](save-deploy-trained-model.md)
- [Submit a training job](submit-training-job.md)
- [What is custom code training?](../../concepts/custom-training-overview.md)
