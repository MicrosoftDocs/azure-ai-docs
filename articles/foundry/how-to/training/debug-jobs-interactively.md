---
title: Debug training jobs interactively in Microsoft Foundry
description: "Debug running training jobs in Microsoft Foundry using SSH, JupyterLab, and TensorBoard for interactive inspection and monitoring."
author: soumyapatro
ms.author: soumyapatro
ms.service: microsoft-foundry
ms.topic: how-to
ms.date: 05/19/2026
ms.custom: training, custom-code
ai-usage: ai-assisted
#CustomerIntent: As a data scientist, I want to SSH into my running job or attach a notebook so that I can inspect state and debug issues interactively.
---

# Debug training jobs interactively

When a custom code training job in Microsoft Foundry is running, you can connect to the compute nodes for interactive debugging. Use SSH for command-line access, JupyterLab for notebook-based inspection, or TensorBoard for training visualization.

## Prerequisites

[!INCLUDE [training-prerequisites](../../includes/training-prerequisites.md)]

- A running training job. For more information, see [Submit a training job](submit-training-job.md).

## Connect via SSH

SSH into a compute node to inspect the job environment, check file system state, run diagnostic commands, or attach a debugger.

# [Python SDK](#tab/python)

```python
# Get SSH connection details for a running job
ssh_info = project_client.beta.jobs.get_ssh_info(name="llama-sft")
print(f"SSH command: ssh {ssh_info.username}@{ssh_info.hostname} -p {ssh_info.port}")
```

# [Foundry CLI (Private Preview)](#tab/cli)

```bash
# Connect to a running job via SSH
foundry training jobs ssh --name llama-sft
```

---

After connecting, you can:

- Inspect GPU utilization with `nvidia-smi`.
- Check mounted data paths.
- View running processes with `ps aux`.
- Inspect environment variables for distributed training.

## Use JupyterLab

Launch JupyterLab on a compute node for interactive exploration. JupyterLab is useful for:

- Inspecting intermediate model outputs or checkpoints.
- Running lightweight experiments on loaded data.
- Debugging data loading or preprocessing issues.

### Start a JupyterLab session

1. Go to your project in the [Foundry portal](https://ai.azure.com).
1. Select **Jobs** in the left navigation.
1. Select the running job.
1. On the job details page, select **Debug** > **JupyterLab**.

A JupyterLab session opens in your browser, connected to the compute node running your job. You have access to the same file system, data mounts, and environment as the training script.

> [!NOTE]
> JupyterLab sessions share compute resources with the running training job. Avoid running memory-intensive operations that could interfere with training.

## Use TensorBoard

TensorBoard visualizes training metrics, model graphs, histograms, and embeddings. It's especially useful for monitoring training dynamics in real time.

### Write TensorBoard logs in your training script

Add TensorBoard logging to your training script alongside MLflow:

```python
from torch.utils.tensorboard import SummaryWriter

writer = SummaryWriter(log_dir="./tb_logs")

for step, batch in enumerate(train_loader):
    loss = train_step(model, batch, optimizer)
    writer.add_scalar("train/loss", loss.item(), step)
    writer.add_scalar("train/learning_rate", optimizer.param_groups[0]["lr"], step)

writer.close()
```

> [!TIP]
> HuggingFace `SFTTrainer` and `Trainer` write TensorBoard logs automatically when `report_to="tensorboard"` is set in the training configuration.

### View TensorBoard in the Foundry portal

1. Go to your project in the [Foundry portal](https://ai.azure.com).
1. Select **Jobs** in the left navigation.
1. Select the running job.
1. On the job details page, select **Debug** > **TensorBoard**.

TensorBoard opens in your browser, loading the logs from your training job.

### View TensorBoard locally

If you prefer to run TensorBoard locally, download the log files from the job output and launch TensorBoard:

```bash
pip install tensorboard
tensorboard --logdir ./tb_logs
```

## Best practices

- **Use SSH for quick diagnostics**: Check `nvidia-smi`, environment variables, and file paths.
- **Use JupyterLab for data exploration**: Inspect data loading, check tensor shapes, and validate preprocessing.
- **Use TensorBoard for training dynamics**: Monitor loss curves, gradient distributions, and learning rate schedules.
- **Don't interfere with training**: Avoid running heavy computations on the same node during training. Interactive debugging should be lightweight.

## Related content

- [Monitor training jobs](monitor-training-jobs.md)
- [Track experiments with MLflow](track-experiments-mlflow.md)
- [Submit a training job](submit-training-job.md)
