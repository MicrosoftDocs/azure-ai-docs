---
title: Track experiments with MLflow in Microsoft Foundry
description: "Log training metrics, hyperparameters, and artifacts using MLflow in Microsoft Foundry custom code training jobs. MLflow tracking is auto-configured."
author: soumyapatro
ms.author: soumyapatro
ms.service: microsoft-foundry
ms.topic: how-to
ms.date: 05/21/2026
ms.custom: training, custom-code
ai-usage: ai-assisted
#CustomerIntent: As a data scientist, I want to log metrics during training so that I can compare experiments and select the best model.
---

# Track experiments with MLflow

MLflow experiment tracking is auto-configured in Microsoft Foundry training jobs. Install the `azureml-mlflow` package in your training environment to enable automatic tracking. Your training script can log metrics, parameters, and artifacts to the Foundry-managed MLflow server without manual endpoint configuration.

## Prerequisites

[!INCLUDE [training-prerequisites](../includes/training-prerequisites.md)]

- The `azureml-mlflow` package installed in your Docker environment:

  ```dockerfile
  RUN pip install azureml-mlflow mlflow
  ```

  The curated PyTorch image (`mcr.microsoft.com/azureml/curated/acpt-pytorch-2.2-cuda12.1:48`) includes `azureml-mlflow` by default.

## How auto-configuration works

When your training job starts on Foundry compute, the `azureml-mlflow` package automatically detects the Foundry environment and configures the MLflow tracking URI. You don't need to set `MLFLOW_TRACKING_URI` or call `mlflow.set_tracking_uri()` in your code.

The auto-configuration:

- Sets the tracking URI to the project's MLflow endpoint
- Configures authentication using the job's managed identity
- Associates logged data with the training job's run ID

## Log metrics and parameters

Add MLflow logging calls to your training script:

```python
import mlflow

# Log hyperparameters
mlflow.log_params({
    "learning_rate": 2e-5,
    "batch_size": 32,
    "num_epochs": 3,
    "model": "Meta-Llama-3-8B",
})

# Log metrics during training
for epoch in range(3):
    train_loss = train_one_epoch()
    mlflow.log_metric("train_loss", train_loss, step=epoch)
    mlflow.log_metric("learning_rate", get_lr(), step=epoch)

# Log final evaluation metrics
mlflow.log_metrics({
    "eval_loss": eval_loss,
    "eval_accuracy": accuracy,
})
```


## Use MLflow with HuggingFace Trainer

The HuggingFace `Trainer` has built-in MLflow integration. Set the `report_to` parameter to enable automatic logging:

```python

# TODO: Validate code snippet
from transformers import TrainingArguments

training_args = TrainingArguments(
    output_dir="./outputs",
    report_to="mlflow",
    logging_steps=10,
    # ... other args
)
```

> [!NOTE]
> Azure MLflow has a 500-character limit on parameter values. If your training arguments exceed this limit, use a custom MLflow callback to truncate values or log them as artifacts. See the [custom MLflow callback example](#custom-mlflow-callback) later in this article.

## Custom MLflow callback

For advanced use cases, create a custom callback that handles the Azure MLflow parameter length limit:

```python
# TODO: Validate code snippet
import mlflow
from transformers import TrainerCallback

class AzureMLflowCallback(TrainerCallback):
    """Custom callback that truncates long parameter values for Azure MLflow."""

    MAX_PARAM_LENGTH = 500

    def on_train_begin(self, args, state, control, **kwargs):
        params = {k: str(v) for k, v in vars(args).items()}
        truncated = {
            k: v[:self.MAX_PARAM_LENGTH] if len(v) > self.MAX_PARAM_LENGTH else v
            for k, v in params.items()
        }
        mlflow.log_params(truncated)

    def on_log(self, args, state, control, logs=None, **kwargs):
        if logs:
            metrics = {k: v for k, v in logs.items() if isinstance(v, (int, float))}
            mlflow.log_metrics(metrics, step=state.global_step)
```

## Log artifacts

Log files and directories as MLflow artifacts for later retrieval:

```python
# Log a single file
mlflow.log_artifact("./config.json")

# Log all files in a directory
mlflow.log_artifacts("./evaluation_results", artifact_path="eval")

# Log a model
mlflow.pytorch.log_model(model, "model")
```

## Compare experiments in the portal

View and compare MLflow experiments in the Foundry portal:

1. Go to your project in the [Foundry portal](https://ai.azure.com).
1. Select **Jobs** in the left navigation.
1. Select a completed job to view its logged metrics.
1. Select multiple jobs to compare metrics side by side.

The portal displays:

- **Metrics charts** — loss curves, learning rate schedules, custom metrics
- **Parameters** — logged hyperparameters for each run
- **Artifacts** — files and models logged during training

## Query experiments with the MLflow SDK

Query your experiments programmatically:

```python
import mlflow

# Search for runs with low loss
runs = mlflow.search_runs(
    filter_string="metrics.eval_loss < 0.5",
    order_by=["metrics.eval_loss ASC"],
)
print(runs[["run_id", "metrics.eval_loss", "params.learning_rate"]])
```

## Related content

- [Monitor training jobs](monitor-training-jobs.md)
- [Save and deploy trained models](save-deploy-trained-model.md)
- [Submit a training job](submit-training-job.md)
