---
title: Work with data in training jobs in Microsoft Foundry
description: "Attach training and validation datasets to custom code training jobs in Microsoft Foundry. Upload data, use mounted or downloaded access modes, and bring your own storage."
author: soumyapatro
ms.author: soumyapatro
ms.service: microsoft-foundry
ms.topic: how-to
ms.date: 05/21/2026
ms.custom: training, custom-code
ai-usage: ai-assisted
#CustomerIntent: As a data scientist, I want to attach training and validation datasets to my job so that my script can access them.
---

# Work with data in training jobs

Custom code training jobs in Microsoft Foundry can access data from multiple sources. Pass training datasets, validation datasets, and configuration files as job inputs. Save processed datasets and artifacts as job outputs. Foundry supports both managed storage and bring-your-own Azure Storage.

## Prerequisites

[!INCLUDE [training-prerequisites](../includes/training-prerequisites.md)]

## Upload data as a dataset

Upload local data files to Foundry as versioned datasets using the SDK. Use `project_client.datasets.upload_folder()` for folder uploads.

```python
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
import os

project_client = AIProjectClient(
    endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)

# Upload a local folder as a dataset
dataset = project_client.datasets.upload_folder(
    name="my-training-data",
    version="1",
    folder="./data",
)
print(f"Dataset uploaded: {dataset.id}")
```

```output
Dataset uploaded: azureai://accounts/<acct>/projects/<proj>/data/my-training-data/versions/1
```

The returned dataset ID can be used as an input path in your training job.

## Bring your own storage

By default, Foundry stores data in managed storage within your project. If you need to use data from your own Azure Blob Storage or Azure Data Lake Storage (ADLS) account, attach it to your project.

For more information on connecting external storage, see [Bring your own Azure Storage](../how-to/bring-your-own-azure-storage-foundry.md).

> [!NOTE]
> Adding project connections to external resources (including BYO storage) requires elevated permissions beyond the Foundry User role.

## Define data inputs

Data inputs let you pass files and folders to your training job. The job's training script accesses these inputs as local paths on the compute node.

### Supported input types

| Asset type | Constant | Description |
|-----------|----------|-------------|
| File | `AssetTypes.URI_FILE` | A single file |
| Folder | `AssetTypes.URI_FOLDER` | A folder of files |

### Supported access modes

| Access mode | Constant | When to use |
|------------|----------|-------------|
| Read-only mount | `InputOutputModes.READ_ONLY_MOUNT` | Large datasets where you don't need all data upfront |
| Download | `InputOutputModes.DOWNLOAD` | Small to medium datasets, or when random access performance matters |

### Example: Define data inputs

```python
from azure.ai.projects.models import Input, AssetTypes, InputOutputModes

# From an uploaded dataset
train_data = Input(
    path="azureai://accounts/<acct>/projects/<proj>/data/my-training-data/versions/1",
    type=AssetTypes.URI_FOLDER,
    mode=InputOutputModes.READ_ONLY_MOUNT,
)

# From a local folder (auto-uploaded by the SDK)
train_data = Input(
    path="./data",
    type=AssetTypes.URI_FOLDER,
)
```

Reference inputs in the `command` string using `${{inputs.<name>}}` placeholders, which resolve to local paths on the compute node at runtime.

## Define data outputs

Data outputs let you save artifacts produced by your training job. Use `READ_WRITE_MOUNT` mode to write outputs during training. The `asset_name` property registers the output as a named dataset when the job completes.

```python
from azure.ai.projects.models import Output

processed_data = Output(
    type=AssetTypes.URI_FOLDER,
    mode=InputOutputModes.READ_WRITE_MOUNT,
    asset_name="my-processed-data",
)
```

## Pass scalar inputs

Scalar values such as hyperparameters can be passed directly in the `command` string or as `tags` on the `CommandJob`. Tags are surfaced as properties on the job overview page in the Foundry portal.

```python
from azure.ai.projects.models import CommandJob

job = CommandJob(
    command=(
        'python "${{inputs.code}}/train.py"'
        ' --batch_size 32'
        ' --learning_rate 2e-5'
        ' --num_epochs 3'
    ),
    tags={
        "batch_size": "32",
        "learning_rate": "2e-5",
        "num_epochs": "3",
    },
    # ... other parameters
)
```

## Related content

- [Work with models in training jobs](work-with-models.md)
- [Submit a training job](submit-training-job.md)
- [Bring your own Azure Storage](../how-to/bring-your-own-azure-storage-foundry.md)
- [Generate synthetic data for fine-tuning](../fine-tuning/data-generation.md)
