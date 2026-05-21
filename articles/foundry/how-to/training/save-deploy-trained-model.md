---
title: Save and deploy a trained model from a training job in Microsoft Foundry
description: "Save model outputs from a training job as model assets in Microsoft Foundry and deploy them for inference using a vLLM-based inferencing stack."
author: soumyapatro
ms.author: soumyapatro
ms.service: microsoft-foundry
ms.topic: how-to
ms.date: 05/19/2026
ms.custom: training, custom-code
ai-usage: ai-assisted
#CustomerIntent: As a data scientist, I want to save my trained model and deploy it for inference so that I can use it in agents or applications.
---

# Save and deploy a trained model from a training job

After a custom code training job completes in Microsoft Foundry, save the trained weights as a model asset and deploy it for inference. This article covers model asset creation from job outputs, deployment eligibility, and the deployment process.

## Prerequisites

[!INCLUDE [training-prerequisites](../../includes/training-prerequisites.md)]

- A completed training job with model outputs. For more information, see [Submit a training job](submit-training-job.md).

## How model assets are created from jobs

When a training job completes, outputs of type `SAFETENSOR_MODEL` or `CUSTOM_MODEL` are automatically registered as model assets in your Foundry project. The model asset includes:

- Model weights produced by the training script.
- Configuration files (`config.json`, `tokenizer.json`, and others) written to the output folder.
- Metadata linking back to the source training job for traceability.

For the auto-registration to work, define the output in your job specification:

```python
from azure.ai.projects.models import Output

model_output = Output(
    type="safetensor_model",
    name="my-llama-sft",
)

job = project_client.beta.jobs.create(
    name="llama-sft",
    outputs={"trained_model": model_output},
    # ... other parameters
)
```

## Create a model asset from a training job

Create a model asset from a specific training job output. This approach is useful when you want to register a specific checkpoint or when auto-registration doesn't apply.

### With the SDK

```python
from azure.ai.projects.models import CustomModel, ModelSource

model = project_client.models.create_or_update(
    CustomModel(
        name="my-gpt-oss-120B",
        version="1",
        type="FullWeight",
        base_model="azureml://registries/azureml-openai-oss/models/gpt-oss-120B/versions/4",
        description="gpt-oss-120B fine-tuned on internal medical Q&A data via GRPO",
        source=ModelSource(
            source_type="TrainingJob",
            job_name="grpo-reasoning-training-job",
            job_output_path="checkpoints/checkpoint_100/",
        ),
    )
)
print(f"Model: {model.name}, Version: {model.version}")
```

```output
Model: my-gpt-oss-120B, Version: 1
```

### With the REST API

```http
PUT {account}.services.ai.azure.com/api/projects/{project}/models/my-gpt-oss-120B/versions/1?api-version=2025-06-01-preview
Content-Type: application/json
Authorization: Bearer {token}

{
  "type": "FullWeight",
  "baseModel": "azureml://registries/azureml-openai-oss/models/gpt-oss-120B/versions/4",
  "description": "gpt-oss-120B fine-tuned on internal medical Q&A data via GRPO",
  "source": {
    "sourceType": "TrainingJob",
    "jobName": "grpo-reasoning-training-job",
    "job_output_path": "checkpoints/checkpoint_100/"
  }
}
```

## View model assets from a job

### In the Foundry portal

1. Go to your project in the [Foundry portal](https://ai.azure.com).
1. Select **Jobs** in the left navigation.
1. Select the completed training job.
1. Select the **Models** tab to view model assets created from job outputs.

### With the SDK

```python
models = project_client.models.list()
for m in models:
    print(f"Model: {m.name}, Version: {m.version}, Type: {m.type}")
```

## Verify deployment eligibility

A model asset is deployable only if it meets the following constraints:

| Requirement | Description |
|------------|-------------|
| **Safetensors format** | Model weights must be in safetensors format |
| **Non-executable auxiliary files** | Only non-executable formats are allowed (JSON, `.md`, `.txt`) |
| **No executable files** | No `.py`, `.sh`, `.exe`, or other executable files in the model folder |

If your model asset contains non-compliant files, update it to remove unsafe files before deployment.

> [!IMPORTANT]
> All files are accepted at registration time to avoid blocking experimentation. Deployment eligibility is validated only when you attempt to deploy.

## Deploy a full-weight model

Deploy a trained model for inference by mapping it to a supported base model architecture. Foundry uses a vLLM-based Microsoft inferencing stack to serve supported models.

### Supported architectures

A trained model is deployable if its base architecture matches a model in the Foundry model catalog that has a deployment template. This includes models like Llama, Mistral, Phi, DeepSeek, Qwen, and other open-weight models available through Foundry Models as a Platform (MaaP).

### Deploy in the portal

1. Go to your project in the [Foundry portal](https://ai.azure.com).
1. Select **Jobs** in the left navigation.
1. Select the completed training job.
1. Select the **Models** tab.
1. Select the model you want to deploy.
1. Map the model to a supported base model architecture.
1. Select **Deploy** and configure the deployment settings.

### Deploy with the SDK

```python
# [TO VERIFY] Deployment SDK signature for BYOW models
deployment = project_client.deployments.create(
    name="my-llama-sft-deployment",
    model_name="my-llama-sft",
    model_version="1",
)
print(f"Deployment: {deployment.name}, Status: {deployment.status}")
```

## Deployment phases

Custom code training model deployment is being released in phases:

| Phase | Scope | Status |
|-------|-------|--------|
| **Phase 1** (Build) | Full-weight safetensor models deployed to managed compute (IPP capacity). Runtime/template auto-selected based on mapped base model. | Available at launch |
| **Phase 2** (Post-build) | LoRA and multi-LoRA adapter deployment alongside base models. | Planned |
| **Phase 3** (Post-build) | Bring your own inference container (BYOC). Requires cluster isolation. | Planned |

> [!NOTE]
> At launch, only full-weight models can be deployed. LoRA adapter deployment is planned for a future release.

## Test the deployed model

Send a chat completion request to the deployed model to verify it works:

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
    model="my-llama-sft-deployment",
    messages=[
        {"role": "user", "content": "Summarize the key benefits of reinforcement learning from human feedback."}
    ],
)

print(response.choices[0].message.content)
```

## Related content

- [Work with models in training jobs](work-with-models.md)
- [Submit a training job](submit-training-job.md)
- [Deploy Foundry Models in the portal](../../foundry-models/how-to/deploy-foundry-models.md)
- [What is custom code training?](../../concepts/custom-training-overview.md)
