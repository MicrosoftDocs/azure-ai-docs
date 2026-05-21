---
title: Work with models in training jobs in Microsoft Foundry
description: "Pass base models as inputs to training jobs and save trained models as outputs. Register model assets manually or through auto-registration in Microsoft Foundry."
author: soumyapatro
ms.author: soumyapatro
ms.service: microsoft-foundry
ms.topic: how-to
ms.date: 05/21/2026
ms.custom: training, custom-code
ai-usage: ai-assisted
#CustomerIntent: As a data scientist, I want to pass a base model as input to my training job and save the trained model as output.
---

# Work with models in training jobs

Training jobs in Microsoft Foundry can use model assets as inputs and produce model assets as outputs. Pass a base model from the Foundry model catalog, your project, or your own storage as a job input. Define model outputs so that trained weights are automatically registered as model assets in your project.

## Prerequisites

[!INCLUDE [training-prerequisites](../includes/training-prerequisites.md)]

## Understand model assets

Model assets represent packaged artifacts (weights, configuration, tokenizer, and metadata) that you can use as training job inputs and, when eligible, deploy for inference. Model assets are created through three paths:

| Creation path | Description |
|---------------|-------------|
| **Manual import** | Register an existing model folder as a model asset |
| **Training job auto-registration** | A training job automatically registers its output as a model asset |
| **Create a dataset** | Model files can be added to project as datasets |

## Pass a model as job input

Specify a model input so your training script can access the base model weights on the compute node.

### From the Foundry model catalog

```python
from azure.ai.projects.models import Input, AssetTypes, InputOutputModes

base_model = Input(
    path="azureml://registries/azureml-meta/models/Meta-Llama-3-8B/versions/1",
    type=AssetTypes.CUSTOM_MODEL,
    mode=InputOutputModes.READ_ONLY_MOUNT,
)
```

### From a model asset in your project

Upload your own model weights and reference by model asset Id

```python
#TODO: Add BYOW SDK snippet
```

### From a dataset in your project

Upload model weights as a dataset and reference by dataset ID:

```python
# One-time upload
model_dataset = project_client.datasets.upload_folder(
    name="my-base-model",
    version="1",
    folder="./model-weights",
)

# Use as input
base_model = Input(
    path=model_dataset.id,
    type=AssetTypes.URI_FOLDER,
    mode=InputOutputModes.READ_ONLY_MOUNT,
)
```

### Access modes for model inputs

| Access mode | Constant | When to use |
|------------|----------|-------------|
| Read-only mount | `InputOutputModes.READ_ONLY_MOUNT` | Large models — files accessed on demand from storage |
| Download | `InputOutputModes.DOWNLOAD` | When your script needs fast random access to all model files |

## Define model outputs

Specify model outputs in the job specification. When an output type is set to `AssetTypes.CUSTOM_MODEL`, the job automatically registers the output as a model asset when it completes. The `asset_name` property defines the name under which the model asset is registered. There's no manual registration step.

```python
from azure.ai.projects.models import Output

final_model_output = Output(
    type=AssetTypes.CUSTOM_MODEL,
    mode=InputOutputModes.READ_WRITE_MOUNT,
    asset_name="my-llama-sft-final-trained",
)

single_checkpoint_output = Output(
    type=AssetTypes.CUSTOM_MODEL,
    mode=InputOutputModes.READ_WRITE_MOUNT,
    asset_name="my-llama-sft-checkpoint-01"
)
```

You can also save model outputs as datasets by using `AssetTypes.URI_FOLDER`. This approach is useful for evaluation or inspection, but outputs saved as datasets aren't directly deployable.

```python
multiple_checkpoints_output = Output(
    type=AssetTypes.URI_FOLDER,
    mode=InputOutputModes.READ_WRITE_MOUNT,
    asset_name="my-llama-sft-all-checkpoints",
)
```

Include inputs and outputs in the `CommandJob`:

```python
job = CommandJob(
    command=(
        'python "${{inputs.code}}/train.py"'
        ' --model_dir "${{inputs.base_model}}"'
        ' --output_dir "${{outputs.trained_model}}"'
        ' --checkpoint_dir "${{outputs.checkpoints}}"'
    ),
    inputs={
        "code": Input(path="./src", type=AssetTypes.URI_FOLDER),
        "base_model": base_model,
    },
    outputs={
        "trained_model": final_model_output,
        "checkpoint-n": single_checkpoint_output,
        "all_checkpoints": multiple_checkpoints_output
    },
    # ... other parameters
)
```

## Inspect models interactively

Download a registered model asset to a supported compute for inspection or interactive experiments:

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

All files are accepted at upload and registration time. But a model asset is deployable only if it meets these constraints:

- Weights are in **safetensors** format.
- Other artifacts are limited to **non-executable formats** (JSON, `.md` files).
- **No executable files** are present.

For more information about deploying trained models, see [Save and deploy trained models](save-deploy-trained-model.md).

## Related content

- [Work with data in training jobs](work-with-data.md)
- [Save and deploy trained models](save-deploy-trained-model.md)
- [Submit a training job](submit-training-job.md)
