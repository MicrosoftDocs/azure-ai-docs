---
title: Work with data in training jobs in Microsoft Foundry
description: "Attach training and validation datasets to custom code training jobs in Microsoft Foundry. Use mounted or downloaded data from Azure Storage or bring your own storage."
author: soumyapatro
ms.author: soumyapatro
ms.service: microsoft-foundry
ms.topic: how-to
ms.date: 05/19/2026
ms.custom: training, custom-code
ai-usage: ai-assisted
#CustomerIntent: As a data scientist, I want to attach training and validation datasets to my job so that my script can access them.
---

# Work with data in training jobs

Custom code training jobs in Microsoft Foundry can access data from multiple sources. Pass training datasets, validation datasets, and configuration files as job inputs. Save processed datasets and artifacts as job outputs. Foundry supports both managed storage and bring-your-own Azure Storage.

## Prerequisites

[!INCLUDE [training-prerequisites](../../includes/training-prerequisites.md)]

## Bring your own storage

By default, Foundry stores data in managed storage within your project. If you need to use data from your own Azure Blob Storage or Azure Data Lake Storage (ADLS) account, attach it to your project.

For more information on connecting external storage, see [Bring your own Azure Storage](../bring-your-own-azure-storage-foundry.md).

## Define data inputs

Data inputs let you pass files and folders to your training job. The job's training script accesses these inputs as local paths on the compute node.

### Supported input types

| Input type | Description | Example use |
|-----------|-------------|-------------|
| `uri_file` | A single file | Training configuration, single dataset file |
| `uri_folder` | A folder | Dataset folder, multi-file dataset |

### Supported access modes

| Access mode | Description | When to use |
|------------|-------------|-------------|
| `mount` | Data is mounted as a virtual filesystem. Files are read on demand from storage. | Large datasets where you don't need all data upfront |
| `download` | Data is downloaded to the compute node's local disk before the job starts. | Small to medium datasets, or when random access performance matters |

### Supported URI schemes

| URI scheme | Example |
|-----------|---------|
| `azureml://` | `azureml://datastores/mydatastore/paths/data/train.jsonl` |
| `https://` | `https://mystorage.blob.core.windows.net/container/data/` |
| `wasbs://` | `wasbs://container@mystorage.blob.core.windows.net/data/` |
| `abfss://` | `abfss://container@mystorage.dfs.core.windows.net/data/` |

### Example: Define data inputs

```python
from azure.ai.projects.models import Input

train_data = Input(
    type="uri_folder",
    path="azureml://datastores/mydatastore/paths/training-data/",
    mode="mount",
)

val_data = Input(
    type="uri_file",
    path="azureml://datastores/mydatastore/paths/validation/val.jsonl",
    mode="download",
)

job = project_client.beta.jobs.create(
    name="sft-with-data",
    inputs={"train": train_data, "val": val_data},
    command="python train.py --train_dir ${{inputs.train}} --val_file ${{inputs.val}}",
    # ... other parameters
)
```

The `${{inputs.<name>}}` placeholders in the command string resolve to the local paths where the data is mounted or downloaded on the compute node.

## Define data outputs

Data outputs let you save artifacts produced by your training job. Outputs are stored in managed storage or your configured datastore.

```python
from azure.ai.projects.models import Output

processed_data = Output(
    type="uri_folder",
    path="azureml://datastores/mydatastore/paths/outputs/processed/",
)

job = project_client.beta.jobs.create(
    name="data-processing-job",
    outputs={"processed": processed_data},
    command="python process.py --output_dir ${{outputs.processed}}",
    # ... other parameters
)
```

## Pass scalar inputs

Scalar inputs pass hyperparameters and configuration values to your training script. Scalar inputs are surfaced as properties on the job overview page in the Foundry portal.

Supported scalar types: `string`, `integer`, `number`, `boolean`.

```python
job = project_client.beta.jobs.create(
    name="sft-with-hyperparams",
    inputs={
        "train": train_data,
        "batch_size": 32,
        "learning_rate": 2e-5,
        "num_epochs": 3,
        "use_fp16": True,
    },
    command="python train.py --train_dir ${{inputs.train}} --batch_size ${{inputs.batch_size}} --lr ${{inputs.learning_rate}} --epochs ${{inputs.num_epochs}}",
    # ... other parameters
)
```

## Related content

- [Work with models in training jobs](work-with-models.md)
- [Submit a training job](submit-training-job.md)
- [Bring your own Azure Storage](../bring-your-own-azure-storage-foundry.md)
- [Generate synthetic data for fine-tuning](../../fine-tuning/data-generation.md)
