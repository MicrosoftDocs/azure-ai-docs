---
title: Use custom environments for training jobs in Microsoft Foundry
description: "Configure Docker environments for custom code training jobs in Microsoft Foundry. Use curated environments or custom images from Azure Container Registry."
author: soumyapatro
ms.author: soumyapatro
ms.service: microsoft-foundry
ms.topic: how-to
ms.date: 05/19/2026
ms.custom: training, custom-code
ai-usage: ai-assisted
#CustomerIntent: As a data scientist, I want to configure a Docker environment with my training dependencies so that my job has the right packages.
---

# Use custom environments for training jobs

Training jobs in Microsoft Foundry run inside Docker containers. You specify the environment as a container image reference in the job specification. Use a curated environment for common frameworks or a custom image from Azure Container Registry (ACR) for specialized dependencies.

## Prerequisites

- An Azure subscription. [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- A Foundry project. For more information, see [Create a project](../create-projects.md).
- (For custom images) An Azure Container Registry attached to your project.

## Use a curated environment

Foundry provides curated environments with popular training frameworks preinstalled. Curated environments are maintained and optimized for Azure GPU infrastructure.

<!-- [TO VERIFY] Confirm exact curated image URIs with Engineering -->

| Curated environment | Includes | Image URI |
|--------------------|---------|----|
| Azure Container for PyTorch (ACPT) | PyTorch, CUDA, NCCL, optimized for Azure GPU VMs | `mcr.microsoft.com/azureml/curated/acpt-pytorch:latest` |
| RL Training | VERL, Slime, PyTorch, RL libraries | `[TO VERIFY]` |

Reference a curated environment in your job specification by using the image URI:

```python
job = project_client.beta.jobs.create(
    name="sft-with-acpt",
    environment="mcr.microsoft.com/azureml/curated/acpt-pytorch:latest",
    # ... other parameters
)
```

## Use a custom Docker image from ACR

When curated environments don't include the packages you need, build a custom Docker image and push it to an Azure Container Registry attached to your project.

### Build and push a custom image

1. Create a `Dockerfile` with your training dependencies:

   ```dockerfile
   FROM mcr.microsoft.com/azureml/curated/acpt-pytorch:latest

   RUN pip install trl datasets accelerate unsloth
   RUN pip install azureml-mlflow mlflow
   ```

1. Build and push the image to your ACR:

   ```bash
   az acr build --registry myregistry --image my-training:v1 --file Dockerfile .
   ```

### Attach ACR to your project

Your Foundry project needs a connection to the ACR that hosts the image. If you haven't attached your ACR:

1. Go to your Foundry project in the [Foundry portal](https://ai.azure.com).
1. Select **Connected resources** in the left navigation.
1. Select **+ New connection** > **Azure Container Registry**.
1. Select your ACR and complete the connection.

### Reference the custom image in a job

Use the full image URI when you specify the environment:

```python
job = project_client.beta.jobs.create(
    name="custom-sft-job",
    environment="myregistry.azurecr.io/my-training:v1",
    # ... other parameters
)
```

## Best practices

- **Start from a curated base**: Build custom images on top of curated environments to get the benefits of Azure GPU optimizations (NCCL tuning, InfiniBand drivers).
- **Pin versions**: Use specific image tags (`:v1`, `:20260501`) instead of `:latest` for reproducible training runs.
- **Keep images small**: Install only the packages your training script needs to reduce image pull time.
- **Test locally**: Verify your Docker image runs the training script correctly before submitting a job.

## Related content

- [Set up compute for training](setup-compute.md)
- [Submit a training job](submit-training-job.md)
- [What is custom code training?](../../concepts/custom-training-overview.md)
