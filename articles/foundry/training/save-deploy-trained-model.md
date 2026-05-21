---
title: Save and deploy trained models in Microsoft Foundry
description: "Save trained model outputs from training jobs and deploy them for inference. Register model assets, validate deployment eligibility, and understand BYOW in Microsoft Foundry."
author: soumyapatro
ms.author: soumyapatro
ms.service: microsoft-foundry
ms.topic: how-to
ms.date: 05/21/2026
ms.custom: training, custom-code
ai-usage: ai-assisted
#CustomerIntent: As a data scientist, I want to save my trained model and deploy it for inference so that applications can use it.
---
TODO: WIP - Work with @Gulsimo Osimi to update.

# Save and deploy trained models

After a training job completes, save the trained model as a registered model asset in your Microsoft Foundry project. Registered model assets can be versioned, shared, and deployed for inference.

## Prerequisites

[!INCLUDE [training-prerequisites](../includes/training-prerequisites.md)]

- A completed training job with model outputs. For more information, see [Submit a training job](submit-training-job.md).

## Auto-register models from job outputs

When you specify `asset_name` on a job output, Foundry automatically registers the output as a model asset when the job completes.

```python
from azure.ai.projects.models import Output, AssetTypes, InputOutputModes

model_output = Output(
    type=AssetTypes.URI_FOLDER,
    mode=InputOutputModes.READ_WRITE_MOUNT,
    asset_name="my-trained-model",
)
```

After the job completes, the model asset appears in your project's model catalog with the specified name and an auto-generated version.

## Register a model asset manually

Register an existing model folder as a model asset. Use manual registration when you want to import a model from local storage, register a specific checkpoint, or create a model from job outputs without auto-registration.

```python
from azure.ai.projects.models import CustomModel, ModelSource

# Register from a training job output
model = project_client.models.create_or_update(
    CustomModel(
        name="my-trained-model",
        version="1",
        type="FullWeight",
        base_model="azureml://registries/azureml-meta/models/Meta-Llama-3-8B/versions/1",
        source=ModelSource(
            source_type="TrainingJob",
            job_name="llama-sft-run1",
        ),
    )
)
print(f"Registered: {model.name} v{model.version}")
```

## Download and inspect model outputs

Download job outputs to inspect the model locally before registering or deploying:

```python
# Download all outputs
project_client.beta.jobs.download(name="llama-sft-run1", all=True)

# Inspect the model
from transformers import AutoModelForCausalLM, AutoTokenizer
model = AutoModelForCausalLM.from_pretrained("./outputs/trained_model")
tokenizer = AutoTokenizer.from_pretrained("./outputs/trained_model")

# Test the model
inputs = tokenizer("Hello, how are you?", return_tensors="pt")
outputs = model.generate(**inputs, max_new_tokens=50)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))
```

## Deployment eligibility

A registered model asset is deployable for serverless inference if it meets these constraints:

| Requirement | Description |
|-------------|-------------|
| **Safetensors format** | Model weights must be saved in `.safetensors` format |
| **No executable files** | The model folder must not contain `.py`, `.sh`, or other executable files |
| **Supported auxiliaries** | Only non-executable formats (JSON, Markdown, text) are accepted alongside weights |

### Save in safetensors format

Ensure your training script saves weights in safetensors format:

```python
# In your training script
model.save_pretrained(output_dir, safe_serialization=True)
tokenizer.save_pretrained(output_dir)
```

## Understand deployment phases

Deploying a trained model involves multiple phases:

| Phase | Description |
|-------|-------------|
| **Registration** | Create a model asset from job outputs |
| **Validation** | System checks deployment eligibility (safetensors, no executables) |
| **Deployment** | Create an endpoint and deploy the model for inference |
| **Testing** | Validate the deployment with test requests |

> [!NOTE]
> Creating model deployments requires elevated permissions beyond the Foundry User role.

## Bring your own weights (BYOW)

You can deploy model weights that weren't trained on Foundry. Upload them as a dataset, register as a model asset, and deploy:

```python
# Upload weights
dataset = project_client.datasets.upload_folder(
    name="external-model-weights",
    version="1",
    folder="./my-external-model",
)

# Register as model asset
model = project_client.models.create_or_update(
    CustomModel(
        name="external-model",
        version="1",
        type="FullWeight",
        source=ModelSource(
            source_type="Dataset",
            dataset_name="external-model-weights",
            dataset_version="1",
        ),
    )
)
```

## Related content

- [Work with models in training jobs](work-with-models.md)
- [Submit a training job](submit-training-job.md)
- [Deploy models with Azure AI model inference](/azure/ai-foundry/model-inference/how-to/create-model-deployments)
