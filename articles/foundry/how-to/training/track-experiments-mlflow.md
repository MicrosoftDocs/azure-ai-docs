---
title: Track training experiments with MLflow in Microsoft Foundry
description: "Use MLflow with azureml-mlflow to log metrics, compare training runs, and track experiments for custom code training jobs in Microsoft Foundry."
author: soumyapatro
ms.author: soumyapatro
ms.service: microsoft-foundry
ms.topic: how-to
ms.date: 05/19/2026
ms.custom: training, custom-code
ai-usage: ai-assisted
#CustomerIntent: As a data scientist, I want to log training metrics and compare runs across experiments so that I can identify the best model.
---

# Track training experiments with MLflow

Use MLflow to log training metrics, parameters, and artifacts from your custom code training jobs in Microsoft Foundry. Group related runs under experiments to compare results and identify the best model.

MLflow tracking is enabled through the `azureml-mlflow` package, which automatically configures the tracking URI when your training script runs inside a Foundry training job.

## Prerequisites

[!INCLUDE [training-prerequisites](../../includes/training-prerequisites.md)]

- The `azureml-mlflow` and `mlflow` packages installed in your training environment:

  ```dockerfile
  # In your Dockerfile
  RUN pip install azureml-mlflow mlflow
  ```

  Or included in your training script's dependencies.

## Set up MLflow in your training script

When a training script runs inside a Foundry training job, `azureml-mlflow` automatically configures the MLflow tracking URI. No manual tracking URI configuration is needed.

Import MLflow in your training script and start logging:

```python
import mlflow

# MLflow tracking URI is auto-configured by azureml-mlflow
# No manual setup required when running inside a Foundry training job

mlflow.autolog()  # Automatically logs common training metrics

# Or log metrics manually
mlflow.log_param("learning_rate", 2e-5)
mlflow.log_param("batch_size", 32)
mlflow.log_param("num_epochs", 3)
```

## Log training metrics

Log metrics at each training step or epoch to track convergence and identify issues.

```python
import mlflow

def train(model, train_loader, optimizer, num_epochs):
    for epoch in range(num_epochs):
        epoch_loss = 0.0
        for step, batch in enumerate(train_loader):
            loss = train_step(model, batch, optimizer)
            epoch_loss += loss.item()

            # Log step-level metrics
            mlflow.log_metric("train_loss", loss.item(), step=epoch * len(train_loader) + step)
            mlflow.log_metric("learning_rate", optimizer.param_groups[0]["lr"], step=epoch * len(train_loader) + step)

        # Log epoch-level metrics
        avg_loss = epoch_loss / len(train_loader)
        mlflow.log_metric("epoch_avg_loss", avg_loss, step=epoch)
        mlflow.log_metric("epoch", epoch, step=epoch)
```

### Common metrics to log

| Metric | Description | Log frequency |
|--------|-------------|---------------|
| `train_loss` | Training loss per step | Every N steps |
| `eval_loss` | Validation loss | Every epoch |
| `learning_rate` | Current learning rate | Every N steps |
| `epoch` | Current epoch number | Every epoch |
| `grad_norm` | Gradient norm (for detecting instability) | Every N steps |
| `gpu_memory_used` | GPU memory consumption | Every N steps |

## Use the experiment field

Group related training runs under a named experiment. Experiments make it easy to compare runs with different hyperparameters.

When you submit a training job, set the `experiment` parameter:

```python
# Run 1: Lower learning rate
job_1 = project_client.beta.jobs.create(
    name="sft-lr-low",
    experiment="llama-sft-sweep",
    # ... other parameters
)

# Run 2: Higher learning rate
job_2 = project_client.beta.jobs.create(
    name="sft-lr-high",
    experiment="llama-sft-sweep",
    # ... other parameters
)
```

Both jobs appear under the `llama-sft-sweep` experiment in the Foundry portal, enabling side-by-side comparison.

## View metrics in the Foundry portal

1. Go to your project in the [Foundry portal](https://ai.azure.com).
1. Select **Jobs** in the left navigation.
1. Select a job to open the job details page.
1. Select the **Metrics** tab to view logged training metrics.

The metrics view shows:
- Line charts for each logged metric over time.
- Logged parameters and their values.
- Comparison across runs within the same experiment.

## Compare runs across an experiment

Compare metrics across multiple runs within the same experiment to identify the best model.

### Compare in the portal

1. Select **Jobs** in the left navigation.
1. Filter by experiment name.
1. Select multiple jobs to compare.
1. View side-by-side metric charts and parameter tables.

### Compare with the SDK

```python
# List all jobs in an experiment
jobs = project_client.beta.jobs.list(experiment="llama-sft-sweep")

for j in jobs:
    print(f"Job: {j.name}, Status: {j.status}")
```

## Log artifacts

Log additional artifacts like model configuration files, training plots, or evaluation results:

```python
import mlflow
import json

# Log a JSON artifact
config = {"model": "llama-3-8b", "technique": "sft", "dataset_size": 50000}
with open("training_config.json", "w") as f:
    json.dump(config, f)
mlflow.log_artifact("training_config.json")
```

## Best practices

- **Log consistently**: Use the same metric names across runs so that comparisons are meaningful.
- **Use experiments**: Group related runs under an experiment name that describes the goal (for example, `llama-sft-lr-sweep`).
- **Log hyperparameters as params**: Use `mlflow.log_param()` for hyperparameters so they appear in comparison tables.
- **Log at the right frequency**: Log step-level metrics every 10-100 steps (not every step) to avoid excessive overhead.
- **Use `mlflow.autolog()`**: For HuggingFace Transformers and other supported frameworks, `autolog()` captures common metrics automatically.

## Related content

- [Monitor training jobs](monitor-training-jobs.md)
- [Debug jobs interactively](debug-jobs-interactively.md)
- [Submit a training job](submit-training-job.md)
