---
title: Set up training environments in Microsoft Foundry
description: "Configure Docker-based training environments for custom code training jobs in Microsoft Foundry. Use curated images or build custom ones with Azure Container Registry."
author: soumyapatro
ms.author: soumyapatro
ms.service: microsoft-foundry
ms.topic: how-to
ms.date: 05/21/2026
ms.custom: training, custom-code
ai-usage: ai-assisted
#CustomerIntent: As a data scientist, I want to use a specific Docker image for my training job so that my code has the right dependencies.
---

# Set up training environments

Training jobs in Microsoft Foundry run inside Docker containers. Choose a curated image from the Foundry registry for common frameworks, or build a custom image with your specific dependencies. Reference the image by its URI in the `environment_image_reference` parameter of your `CommandJob`.

## Prerequisites

[!INCLUDE [training-prerequisites](../includes/training-prerequisites.md)]

- For custom images: An [Azure Container Registry (ACR)](/azure/container-registry/container-registry-get-started-portal) attached to your Foundry project.

## Use a curated environment

TODO: Add full list of curated environments

Foundry provides curated Docker images optimized for common training frameworks. These images include pre-installed packages, CUDA drivers, and distributed training libraries.

| Image | Framework | Description |
|-------|-----------|-------------|
| `mcr.microsoft.com/azureml/curated/acpt-pytorch-2.2-cuda12.1:48` | PyTorch 2.2 | PyTorch with CUDA 12.1, DeepSpeed, NCCL, `azureml-mlflow` |

Reference a curated image in your job:

```python
from azure.ai.projects.models import CommandJob

job = CommandJob(
    environment_image_reference="mcr.microsoft.com/azureml/curated/acpt-pytorch-2.2-cuda12.1:48",
    command='python "${{inputs.code}}/train.py"',
    # ... other parameters
)
```

## Build a custom Docker image

When a curated image doesn't meet your requirements, build a custom image. Start from a curated base image and add your dependencies.

### Create a Dockerfile

```dockerfile
FROM mcr.microsoft.com/azureml/curated/acpt-pytorch-2.2-cuda12.1:48

# Install additional Python packages
RUN pip install --no-cache-dir \
    transformers==4.45.0 \
    trl==0.11.0 \
    datasets==3.0.0 \
    peft==0.12.0 \
    bitsandbytes==0.44.0 \
    accelerate==0.34.0 \
    azureml-mlflow \
    mlflow

# Copy any custom scripts or configs
COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt
```

### Push to Azure Container Registry

```bash
# Build the image
docker build -t myregistry.azurecr.io/my-training:v1 .

# Login to ACR
az acr login --name myregistry

# Push the image
docker push myregistry.azurecr.io/my-training:v1
```

### Use the custom image in a job

```python
job = CommandJob(
    environment_image_reference="myregistry.azurecr.io/my-training:v1",
    command='python "${{inputs.code}}/train.py" --output_dir "${{outputs.trained_model}}"',
    # ... other parameters
)
```

## Grant your project access to ACR

Your Foundry project's user-assigned managed identity (UAMI) needs permission to pull images from your ACR. Assign the **AcrPull** role to the project's UAMI on the ACR resource:

> [!IMPORTANT]
> Custom image pull from ACR currently supports only user-assigned managed identity (UAMI) authentication. Other authentication methods such as admin credentials or service principals aren't supported for training jobs.

1. In the [Azure portal](https://portal.azure.com), go to your Azure Container Registry resource.
1. Select **Access control (IAM)** in the left navigation.
1. Select **+ Add** > **Add role assignment**.
1. Search for and select the **AcrPull** role, then select **Next**.
1. Select **Managed identity**, then select **+ Select members**.
1. Filter by **User-assigned managed identity** and select the managed identity associated with your Foundry project.
1. Select **Review + assign** to complete the role assignment.

> [!NOTE]
> You need **Owner** or **User Access Administrator** permissions on the ACR resource to assign roles. Contact your subscription administrator if you don't have these permissions.

## Best practices for training environments

- **Start from curated images** to inherit optimized CUDA drivers and distributed training libraries.
- **Pin package versions** (for example, `transformers==4.45.0`) for reproducible training.
- **Keep images small** by using `--no-cache-dir` with pip and combining `RUN` commands.
- **Include `azureml-mlflow`** for automatic experiment tracking integration.
- **Verify your image locally** after building to catch dependency issues before submitting a job:

  ```bash
  docker run --rm myregistry.azurecr.io/my-training:v1 python -c "import torch; import transformers; print('All imports OK')"
  ```

## Related content

- [Set up compute for training](setup-compute.md)
- [Submit a training job](submit-training-job.md)
- [Track experiments with MLflow](track-experiments-mlflow.md)
