---
title: Monitor training jobs in Microsoft Foundry
description: "Monitor custom code training jobs in Microsoft Foundry. View logs, infrastructure metrics, and job status in the SDK, CLI, and Foundry portal."
author: soumyapatro
ms.author: soumyapatro
ms.service: microsoft-foundry
ms.topic: how-to
ms.date: 05/21/2026
ms.custom: training, custom-code
ai-usage: ai-assisted
#CustomerIntent: As a data scientist, I want to monitor my training job's progress and GPU utilization so that I can diagnose issues.
---

# Monitor training jobs in Microsoft Foundry

After you submit a custom code training job, monitor its progress through logs, status updates, and infrastructure metrics. Use the Microsoft Foundry SDK, Foundry CLI, or the Foundry portal to track your jobs.

## Prerequisites

[!INCLUDE [training-prerequisites](../includes/training-prerequisites.md)]

- A submitted training job. For more information, see [Submit a training job](submit-training-job.md).

## View job status and metadata

# [Python SDK](#tab/python)

```python
retrieved_job = project_client.beta.jobs.get(name="llama-sft-run1")
print(f"Job: {retrieved_job.name}")
print(f"Display name: {retrieved_job.display_name}")
print(f"Status: {retrieved_job.status}")
```

```output
Job: llama-sft-run1
Display name: llama-sft
Status: Running
```

# [Foundry CLI (Private Preview)](#tab/cli)

```bash
foundry training jobs show --name llama-sft-run1
```

---

### Job status values

| Status | Description |
|--------|-------------|
| `Starting` | Job is being prepared and resources are being allocated |
| `Running` | Job is actively running on compute |
| `Completed` | Job finished successfully |
| `Failed` | Job encountered an error |
| `Cancelled` | Job was cancelled by the user |

## Stream job logs

Stream logs from your running job to monitor training progress. The `stream` method blocks until the job completes.

# [Python SDK](#tab/python)

```python
# Stream logs (blocks until job completes or fails)
project_client.beta.jobs.stream(name="llama-sft-run1")
```

# [Foundry CLI (Private Preview)](#tab/cli)

```bash
foundry training jobs logs --name llama-sft-run1 --follow
```

---

## Monitor in the Foundry portal

The Foundry portal provides a visual interface for monitoring training jobs.

1. Go to your project in the [Foundry portal](https://ai.azure.com).
1. Select **Jobs** in the left navigation.
1. Select a job to open the job details page.

The job details page includes the following tabs:

| Tab | Description |
|-----|-------------|
| **Overview** | Job status, parameters, tags, duration |
| **Logs** | Streaming logs from all nodes |
| **Metrics** | Training metrics logged with MLflow (loss, learning rate, custom metrics) |
| **Code** | The training script and files submitted with the job |
| **Infra metrics** | Infrastructure metrics for the compute nodes |
| **Models** | Model assets created from job outputs |

## View infrastructure metrics

Infrastructure metrics help you identify resource bottlenecks and optimize your compute configuration.

| Metric | Description |
|--------|-------------|
| **GPU utilization** | Percentage of GPU compute capacity in use |
| **GPU memory** | GPU memory usage and allocation |
| **CPU utilization** | CPU usage across all nodes |
| **Memory** | System memory usage |
| **Disk** | Disk read/write throughput and capacity |
| **InfiniBand** | Network throughput for multi-node distributed training |

View infrastructure metrics in the Foundry portal:

1. Open the job details page.
1. Select the **Infra metrics** tab.
1. Select the node and metric type to visualize.

> [!TIP]
> Low GPU utilization combined with high CPU usage can indicate a data loading bottleneck. Consider increasing `dataloader_num_workers` or using mounted data instead of downloaded data.

## Troubleshooting

| Issue | Possible cause | Resolution |
|-------|---------------|------------|
| Job stays in `Starting` | Insufficient quota or no available nodes | Check quota under **Compute** > **Quota**. Request an increase if needed. |
| Job fails immediately | Image pull failure from ACR | Verify the ACR is attached to your project and the image URI is correct. |
| NCCL timeout in multi-node jobs | Network communication failure between nodes | Ensure InfiniBand is available on your SKU. Set `NCCL_NVLS_ENABLE=1` in environment variables. |
| Out of memory (OOM) | Model or batch too large for GPU | Reduce `per_device_train_batch_size`, enable gradient checkpointing, or use a larger GPU SKU. |

## Related content

- [Track experiments with MLflow](track-experiments-mlflow.md)
- [Debug jobs interactively](debug-jobs-interactively.md)
- [Submit a training job](submit-training-job.md)
