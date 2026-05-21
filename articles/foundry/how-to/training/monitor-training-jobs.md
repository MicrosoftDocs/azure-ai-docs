---
title: Monitor training jobs in Microsoft Foundry
description: "Monitor custom code training jobs in Microsoft Foundry. View logs, infrastructure metrics, and job status in the SDK, CLI, and Foundry portal."
author: soumyapatro
ms.author: soumyapatro
ms.service: microsoft-foundry
ms.topic: how-to
ms.date: 05/19/2026
ms.custom: training, custom-code
ai-usage: ai-assisted
#CustomerIntent: As a data scientist, I want to monitor my training job's progress and GPU utilization so that I can diagnose issues.
---

# Monitor training jobs in Microsoft Foundry

After you submit a custom code training job, monitor its progress through logs, status updates, and infrastructure metrics. Use the Microsoft Foundry SDK, Foundry CLI, or the Foundry portal to track your jobs.

## Prerequisites

[!INCLUDE [training-prerequisites](../../includes/training-prerequisites.md)]

- A submitted training job. For more information, see [Submit a training job](submit-training-job.md).

## View job status and metadata

Check the current status of a training job and view its metadata, including the experiment name, compute target, and configuration.

# [Python SDK](#tab/python)

```python
job = project_client.beta.jobs.get(name="llama-sft")
print(f"Job: {job.name}")
print(f"Status: {job.status}")
print(f"Experiment: {job.experiment}")
print(f"Compute: {job.compute}")
print(f"Created: {job.created_time}")
```

```output
Job: llama-sft
Status: Running
Experiment: sft-experiments
Compute: gpu-cluster
Created: 2026-05-19T10:30:00Z
```

# [Foundry CLI (Private Preview)](#tab/cli)

```bash
foundry training jobs show --name llama-sft
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

## Tail job logs

Stream logs from your running job to monitor training progress, debug errors, and track output.

# [Python SDK](#tab/python)

```python
logs = project_client.beta.jobs.get_logs(name="llama-sft")
for line in logs:
    print(line)
```

```output
[2026-05-19 10:35:12] Loading model from /mnt/inputs/base_model...
[2026-05-19 10:36:45] Model loaded. Starting training...
[2026-05-19 10:36:50] Epoch 1/3, Step 10/1000, Loss: 2.4532
[2026-05-19 10:36:55] Epoch 1/3, Step 20/1000, Loss: 2.1287
```

# [Foundry CLI (Private Preview)](#tab/cli)

```bash
# Follow logs in real time
foundry training jobs logs --name llama-sft --follow
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
| **Overview** | Job status, parameters, scalar inputs (shown as properties), experiment name, duration |
| **Logs** | Streaming logs from all nodes |
| **Metrics** | Training metrics logged with MLflow (loss, learning rate, and custom metrics) |
| **Code** | The training script and files submitted with the job |
| **Infra metrics** | Infrastructure metrics for the compute nodes |
| **Models** | Model assets created from job outputs |

## View infrastructure metrics

Infrastructure metrics help you identify resource bottlenecks and optimize your compute configuration.

Available infrastructure metrics:

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
> Low GPU utilization combined with high CPU usage can indicate a data loading bottleneck. Consider increasing the number of data loader workers or using mounted data instead of downloaded data.

## Related content

- [Track experiments with MLflow](track-experiments-mlflow.md)
- [Debug jobs interactively](debug-jobs-interactively.md)
- [Submit a training job](submit-training-job.md)
