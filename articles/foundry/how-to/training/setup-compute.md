---
title: Set up compute for custom code training in Microsoft Foundry
description: "Configure a GPU compute cluster for custom code training jobs in Microsoft Foundry. Choose GPU SKUs, set instance counts, and manage quotas."
author: soumyapatro
ms.author: soumyapatro
ms.service: microsoft-foundry
ms.topic: how-to
ms.date: 05/19/2026
ms.custom: training, custom-code
ai-usage: ai-assisted
#CustomerIntent: As a data scientist, I want to configure a GPU compute cluster so that I can run training jobs.
---

# Set up compute for training jobs

Before you submit a custom code training job, you need a GPU compute cluster attached to your Microsoft Foundry project. This article explains how to select a GPU SKU, create a compute cluster, and configure instance counts for your training workload.

## Prerequisites

- An Azure subscription. [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- A Foundry project. For more information, see [Create a project](../create-projects.md).
- A minimum role of **Foundry User** on the Foundry resource. For more information, see [RBAC in Foundry](../../concepts/rbac-foundry.md).

  [!INCLUDE [role-rename-note](../../includes/role-rename-note.md)]

## Choose a GPU SKU

Select a GPU SKU based on your model size and training requirements. Larger models and multi-GPU training techniques require SKUs with more GPU memory and higher interconnect bandwidth.

<!-- [TO VERIFY] Confirm exact SKU availability and regions with Engineering -->

| GPU SKU | GPUs per node | GPU memory | Best for |
|---------|--------------|------------|----------|
| Standard_NC24ads_A100_v4 | 1 | 80 GB | Small to medium models, single-GPU training |
| Standard_NC48ads_A100_v4 | 2 | 160 GB | Medium models, data-parallel training |
| Standard_NC96ads_A100_v4 | 4 | 320 GB | Large models, multi-GPU training |
| Standard_ND96asr_v4 | 8 | 320 GB | Large models, multi-node distributed training with InfiniBand |
| Standard_ND96amsr_A100_v4 | 8 | 640 GB | Very large models, multi-node training with NVLink + InfiniBand |

> [!NOTE]
> GPU SKU availability varies by region. Check the [region availability](../../reference/region-support.md) page for current availability.

## Create a compute cluster

Create a GPU compute cluster in the Foundry portal or through the SDK.

### Create a compute cluster in the portal

1. Go to your Foundry project in the [Foundry portal](https://ai.azure.com).
1. Select **Compute** in the left navigation.
1. Select **+ New compute cluster**.
1. Select the GPU SKU that matches your requirements.
1. Set the **Minimum number of nodes** and **Maximum number of nodes**.
1. Enter a **Compute name** (for example, `gpu-cluster`).
1. Select **Create**.

### Create a compute cluster with the SDK

```python
# [TO VERIFY] Compute cluster creation via Foundry SDK
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

project_client = AIProjectClient(
    endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)

# Create or reference an existing compute cluster
compute = project_client.compute.create_or_update(
    name="gpu-cluster",
    size="Standard_NC96ads_A100_v4",
    min_instances=0,
    max_instances=4,
)
print(f"Compute cluster: {compute.name}")
```

## Configure instance count and processes per node

When you submit a training job, specify how many nodes and processes to use:

- **`instance_count`**: The number of nodes (VMs) to allocate for the job. Use multiple nodes for distributed training of large models.
- **`process_per_node`**: The number of processes to run per node. Typically set to the number of GPUs per node for data-parallel training.

For example, a job on a 4-GPU SKU with `instance_count=2` and `process_per_node=4` uses 8 GPUs total across 2 nodes.

```python
job = project_client.beta.jobs.create(
    name="distributed-training",
    compute="gpu-cluster",
    instance_count=2,
    process_per_node=4,
    distribution="PyTorch",
    # ... other parameters
)
```

## Manage quotas

GPU compute clusters are subject to quota limits per subscription and region. If you need more capacity:

1. Go to the [Foundry portal](https://ai.azure.com).
1. Select **Quota** in the left navigation.
1. Find the GPU SKU you need and select **Request increase**.

For more information, see [Manage quotas for Foundry resources](../quota.md).

## Related content

- [What is custom code training?](../../concepts/custom-training-overview.md)
- [Use custom environments](use-custom-environments.md)
- [Submit a training job](submit-training-job.md)
