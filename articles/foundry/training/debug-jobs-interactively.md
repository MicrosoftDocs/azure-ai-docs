---
title: Debug training jobs interactively in Microsoft Foundry
description: "Debug custom code training jobs with SSH, JupyterLab, and TensorBoard. Connect to compute nodes for interactive troubleshooting in Microsoft Foundry."
author: soumyapatro
ms.author: soumyapatro
ms.service: microsoft-foundry
ms.topic: how-to
ms.date: 05/21/2026
ms.custom: training, custom-code
ai-usage: ai-assisted
#CustomerIntent: As a data scientist, I want to connect to a running job interactively so that I can debug environment and data issues.
---
TODO: Add other interactive debugging methods available and how to choose - Ray Dashboard, Evals??. 
# Debug training jobs interactively

When a training job fails or behaves unexpectedly, you can connect to the compute node interactively using SSH, JupyterLab, or TensorBoard. Interactive debugging lets you inspect the file system, test commands, and troubleshoot environment issues directly on the node.

## Prerequisites

[!INCLUDE [training-prerequisites](../includes/training-prerequisites.md)]

- A running or completed training job. For more information, see [Submit a training job](submit-training-job.md).

## View available services

Use `show_services()` to retrieve the list of interactive services available on a job:

```python
services = project_client.beta.jobs.show_services(name="llama-sft-run1")
print(services)
```

The response includes connection information for SSH, JupyterLab, and TensorBoard endpoints when available.

## Connect via SSH

SSH into a running job's compute node to inspect the environment, file system, and installed packages.

1. Call `show_services()` to get the SSH connection details:

   ```python
   services = project_client.beta.jobs.show_services(name="llama-sft-run1")
   # Extract SSH connection info from services
   ```

1. Connect using the provided SSH credentials:

   ```bash
   ssh -p <port> <user>@<host>
   ```

Once connected, you can:

- Verify installed packages: `pip list | grep torch`
- Check GPU availability: `nvidia-smi`
- Inspect mounted data: `ls ${{inputs.train_data}}`
- Test your training command manually

## Connect via JupyterLab

JupyterLab lets you run code interactively on the compute node with access to the same environment and mounted data as your training job.

1. Call `show_services()` to get the JupyterLab URL.
1. Open the URL in your browser.
1. Use the notebook interface to inspect data, test code, and debug issues.

## Launch TensorBoard

TensorBoard visualizes training metrics logged to the TensorBoard log directory.

### From a running job

1. In the Foundry portal, open your job's detail page.
1. Select **TensorBoard** from the services panel.
1. View loss curves, learning rate schedules, and custom metrics in the TensorBoard UI.



## Common debugging scenarios

| Scenario | Approach |
|----------|----------|
| Import error or missing package | SSH into the node and check `pip list`. Update your Docker image or environment. |
| Data not found | SSH in and verify mounted paths with `ls`. Confirm the input path and type are correct. |
| CUDA out of memory | Check `nvidia-smi` via SSH. Reduce batch size or enable gradient checkpointing. |
| NCCL timeout in distributed | SSH to rank-0 and verify `MASTER_ADDR`, `MASTER_PORT` are set. Check InfiniBand with `ibstat`. |
| Training script crashes | Stream logs first. If logs are insufficient, SSH in and run the command manually. |

## Related content

- [Monitor training jobs](monitor-training-jobs.md)
- [Track experiments with MLflow](track-experiments-mlflow.md)
- [Set up training environments](setup-training-environment.md)
