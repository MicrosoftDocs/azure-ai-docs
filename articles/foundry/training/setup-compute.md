---
title: Set up compute for training in Microsoft Foundry
description: "Create and manage GPU compute clusters for custom code training jobs in Microsoft Foundry. Select GPU SKUs and configure autoscaling."
author: soumyapatro
ms.author: soumyapatro
ms.service: microsoft-foundry
ms.topic: how-to
ms.date: 05/21/2026
ms.custom: training, custom-code
ai-usage: ai-assisted
#CustomerIntent: As a platform engineer, I want to set up GPU compute for training jobs so that data scientists can submit work.
---

# Set up compute for training

Before you submit a training job, attach a GPU compute cluster to your Microsoft Foundry project. Compute clusters scale automatically based on demand and provide the GPU resources your training jobs need.

> [!NOTE]
> Creating and managing compute clusters requires elevated permissions beyond the Foundry User role. Contact your project administrator if you don't have the required permissions.

## Prerequisites

[!INCLUDE [training-prerequisites](../includes/training-prerequisites.md)]

## Create a compute cluster in the Foundry portal

1. Go to your project in the [Foundry portal](https://ai.azure.com).
1. Select **Compute** in the left navigation.
1. Select **+ New** to create a compute cluster.
1. Configure the cluster settings:

   | Setting | Description |
   |---------|-------------|
   | **Name** | A unique name for the cluster (for example, `gpu-cluster-a100`) |
   | **GPU SKU** | The GPU VM size (for example, `Standard_NC96ads_A100_v4`) |
   | **Minimum nodes** | Minimum number of nodes (set to 0 to scale down when idle) |
   | **Maximum nodes** | Maximum number of nodes for autoscaling |
   | **Idle seconds before scale down** | Seconds to wait before removing idle nodes |

1. Select **Create** to provision the cluster.

## Select a GPU SKU

Choose a GPU SKU based on your training requirements.

| SKU family | GPU | GPU memory | Interconnect | Best for |
|-----------|-----|------------|--------------|----------|
| NC A100 v4 | A100 80 GB | 80 GB per GPU | InfiniBand | Large model training, multi-node |
| NC H100 v5 | H100 80 GB | 80 GB per GPU | InfiniBand | Fastest training, large-scale distributed |
| NC A10 v3 | A10 24 GB | 24 GB per GPU | Ethernet | Smaller models, prototyping |

> [!TIP]
> For multi-node distributed training, use SKUs with InfiniBand interconnect (A100 or H100) for optimal NCCL performance.

## Reference compute in a training job

When you submit a training job, reference your compute cluster by its full resource ID:

```python
compute_id = (
    "/subscriptions/<subscription-id>"
    "/resourceGroups/<resource-group>"
    "/providers/microsoft.cognitiveservices/accounts/<account>"
    "/computes/<cluster-name>"
)
```

Find the compute ID in the Foundry portal:

1. Go to **Compute** in the left navigation.
1. Select your cluster.
1. Copy the **Resource ID** from the **Properties** panel.

## Check compute quota

View your current GPU quota and usage:

1. Go to **Compute** in the Foundry portal.
1. Select **Quota** to view available quota by region and SKU.
1. If you need more quota, select **Request increase** and submit a support request.

## Related content

- [Submit a training job](submit-training-job.md)
- [Set up training environments](setup-training-environment.md)
- [What is custom code training?](../concepts/custom-training-overview.md)
