---
title: Guidelines for Deploying MLflow Models
titleSuffix: Azure Machine Learning
description: Learn how to deploy your MLflow model to the deployment targets that Azure Machine Learning supports.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: mlops
author: s-polly
ms.author: scottpolly
ms.reviewer: jturuk
ms.date: 10/20/2025
ms.topic: concept-article
ms.custom: deploy, mlflow, devplatv2, no-code-deployment, cliv2, update-code3, FY25Q1-Linter
ms.devlang: azurecli
#Customer intent: As a data scientist, I want to understand the options and guidelines for deploying MLflow models in Azure Machine Learning so I can best deploy my MLflow models.
---

# Guidelines for deploying MLflow models

[!INCLUDE [cli v2](includes/machine-learning-cli-v2.md)]

In this article, you'll learn about the deployment of [MLflow](https://www.mlflow.org) models to Azure Machine Learning for both real-time and batch inference, and about different tools you can use to manage the deployments.

## No-code deployment

When you deploy MLflow models to Azure Machine Learning, unlike with custom model deployment, you don't need to provide a scoring script or an environment. Azure Machine Learning automatically generates the scoring script and environment. This functionality is called *no-code deployment*.

For no-code deployment, Azure Machine Learning:

- Ensures that all the package dependencies indicated in the MLflow model are satisfied.
- Provides an MLflow base image or curated environment that contains the following items:
  - Packages required for Azure Machine Learning to perform inference, including [`mlflow-skinny`](https://github.com/mlflow/mlflow/blob/master/libs/skinny/README_SKINNY.md).
  - A scoring script to perform inference.

### Packages and dependencies

Azure Machine Learning automatically generates environments to run inference on MLflow models. To build the environments, Azure Machine Learning reads the Conda dependencies that are specified in the MLflow model and adds any packages that are required to run the inferencing server. These extra packages vary depending on deployment type.

> [!IMPORTANT]
> If Conda dependencies are specified in the MLflow model, it is required to include `azureml-inference-server-http` and `azureml-ai-monitoring` packages in the dependencies as in the example below. 

The following example *conda.yaml* file shows Conda dependencies specified in an MLflow model.

:::code language="yaml" source="~/azureml-examples-main/sdk/python/endpoints/online/mlflow/sklearn-diabetes/model/conda.yaml":::

> [!IMPORTANT]
> MLflow automatically detects packages when it logs a model, and it pins the package versions in the model's Conda dependencies. This automatic package detection might not reflect your intentions or requirements. You can alternatively [log models that use a custom signature, environment, or samples](how-to-log-mlflow-models.md#log-models-that-use-a-custom-signature-environment-or-samples).

### Models that include signatures

MLflow models can include a signature that indicates the expected inputs and their types. When such models are deployed to online or batch endpoints, Azure Machine Learning ensures that the number and types of the data inputs comply with the signature. If the input data can't be parsed as expected, the model invocation fails.

You can inspect an MLflow model signature by opening the MLmodel file. For more information on how signatures work in MLflow, see [Signatures in MLflow](concept-mlflow-models.md#model-signature).

The following example MLmodel file highlights the `signature`.

:::code language="yaml" source="~/azureml-examples-main/sdk/python/endpoints/online/mlflow/sklearn-diabetes/model/MLmodel" highlight="19-25":::

> [!TIP]
> Signatures in MLflow models are recommended because they provide a convenient way to detect data compatibility problems. For more information about how to log models that have signatures, see [Log models that use a custom signature, environment, or samples](how-to-log-mlflow-models.md#log-models-that-use-a-custom-signature-environment-or-samples).

<a name="models-deployed-in-azure-machine-learning-vs-models-deployed-in-the-mlflow-built-in-server"></a>
## Deployment in the MLflow built-in server vs. deployment in Azure Machine Learning inferencing server

Model developers can use MLflow built-in deployment tools to test models locally. For example, you can run a local instance of a model that's registered in the MLflow server registry by using `mlflow models serve` or the MLflow CLI `mlflow models predict`. For more information about MLflow built-in deployment tools, see [Built-in deployment tools](https://www.mlflow.org/docs/latest/models.html#built-in-deployment-tools) in the MLflow documentation.

Azure Machine Learning also supports deploying models to both online and batch endpoints. These endpoints run different inferencing technologies that can have different features.

- Azure Machine Learning online endpoints, similar to the MLflow built-in server, provide a scalable, synchronous, and lightweight way to run models for inference.

- Azure Machine Learning batch endpoints can run asynchronous inference over long-running inferencing processes that can scale to large amounts of data. The MLflow server lacks this capability, although you can achieve a similar capability by using [Spark jobs](how-to-deploy-mlflow-model-spark-jobs.md). To learn more about batch endpoints and MLflow models, see [Use MLflow models in batch deployments](how-to-mlflow-batch.md).

### Input formats

The following table shows the input types supported by the MLflow built-in server and those supported by Azure Machine Learning online endpoints.

| Input type | MLflow built-in server | Azure Machine Learning online endpoint |
|---| :-: | :-: |
| JSON-serialized pandas DataFrames in the split orientation | **&check;** | **&check;** |
| JSON-serialized pandas DataFrames in the records orientation | Deprecated |  |
| CSV-serialized pandas DataFrames | **&check;** | Use batch inferencing. For more information, see [Deploy MLflow models to batch endpoints](how-to-mlflow-batch.md). |
| TensorFlow input as JSON-serialized lists (tensors) and dictionary of lists (named tensors) | **&check;** | **&check;** |
| TensorFlow input using the TensorFlow Serving API | **&check;** |  |

The following sections focus on MLflow models that are deployed to Azure Machine Learning online endpoints.

### Input structure

Regardless of input type, Azure Machine Learning requires you to provide inputs in a JSON payload in the dictionary key `input_data`. This key isn't required when you use the command `mlflow models serve` to serve models, so payloads can't be used interchangeably for Azure Machine Learning online endpoints and the MLflow built-in server.

> [!IMPORTANT]
> The payload structure changed in MLflow 2.0.

The following payload examples show differences between a model deployed in the MLflow built-in server versus the Azure Machine Learning inferencing server.

#### JSON-serialized pandas DataFrame in the split orientation

# [Azure Machine Learning](#tab/azureml)

```json
{
    "input_data": {
        "columns": [
            "age", "sex", "trestbps", "chol", "fbs", "restecg", "thalach", "exang", "oldpeak", "slope", "ca", "thal"
        ],
        "index": [1],
        "data": [
            [1, 1, 145, 233, 1, 2, 150, 0, 2.3, 3, 0, 2]
        ]
    }
}
```

# [MLflow server](#tab/builtin)

This payload uses MLflow server 2.0+.

```json
{
    "dataframe_split": {
        "columns": [
            "age", "sex", "trestbps", "chol", "fbs", "restecg", "thalach", "exang", "oldpeak", "slope", "ca", "thal"
        ],
        "index": [1],
        "data": [
            [1, 1, 145, 233, 1, 2, 150, 0, 2.3, 3, 0, 2]
        ]
    }
}
```

---

#### Tensor input

# [Azure Machine Learning](#tab/azureml)

```json
{
    "input_data": [
          [1, 1, 0, 233, 1, 2, 150, 0, 2.3, 3, 0, 2],
          [1, 1, 0, 233, 1, 2, 150, 0, 2.3, 3, 0, 2]
          [1, 1, 0, 233, 1, 2, 150, 0, 2.3, 3, 0, 2],
          [1, 1, 145, 233, 1, 2, 150, 0, 2.3, 3, 0, 2]
    ]
}
```

# [MLflow server](#tab/builtin)

```json
{
    "inputs": [
          [1, 1, 0, 233, 1, 2, 150, 0, 2.3, 3, 0, 2],
          [1, 1, 0, 233, 1, 2, 150, 0, 2.3, 3, 0, 2]
          [1, 1, 0, 233, 1, 2, 150, 0, 2.3, 3, 0, 2],
          [1, 1, 145, 233, 1, 2, 150, 0, 2.3, 3, 0, 2]
    ]
}
```

---

#### Named-tensor input

# [Azure Machine Learning](#tab/azureml)

```json
{
    "input_data": {
        "tokens": [
          [0, 655, 85, 5, 23, 84, 23, 52, 856, 5, 23, 1]
        ],
        "mask": [
          [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
        ]
    }
}
```

# [MLflow server](#tab/builtin)

```json
{
    "inputs": {
        "tokens": [
          [0, 655, 85, 5, 23, 84, 23, 52, 856, 5, 23, 1]
        ],
        "mask": [
          [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
        ]
    }
}
```

---

## Inference customization for MLflow models

Scoring scripts customize how to run inferencing for custom models. But for MLflow model deployment, the decision about how to run inferencing is made by the model builder rather than by the deployment engineer. Each model framework can automatically apply specific inference routines.

If you need to change how inference is run for an MLflow model, you can take one of the following actions:

- Change how your model is being logged in the training routine.
- Customize inference by using a scoring script at deployment time.

### Change how your model is logged during training

When you log a model by using either `mlflow.autolog` or `mlflow.<flavor>.log_model`, the flavor used for the model determines how to run inference and what results to return. MLflow doesn't enforce any specific behavior for how the `predict()` function generates results.

In some cases, you might want to do some preprocessing or postprocessing before and after your model runs. Or you might want to change what's returned, for example, probabilities instead of classes. One solution is to implement machine learning pipelines that move from inputs to outputs directly.

For example, [`sklearn.pipeline.Pipeline`](https://scikit-learn.org/stable/modules/generated/sklearn.pipeline.Pipeline.html) or [`pyspark.ml.Pipeline`](https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.ml.Pipeline.html) are popular ways to implement pipelines, and are sometimes recommended to improve performance. You can also customize how your model does inferencing by [logging custom models](how-to-log-mlflow-models.md#log-custom-models).

### Customize inference by using a scoring script

Although MLflow models don't require a scoring script, you can still provide one to customize inference execution for MLflow models if needed. For more information on how to customize inference, see [Customize MLflow model deployments](how-to-deploy-mlflow-models-online-endpoints.md#customize-mlflow-model-deployments) for online endpoints or [Customize model deployment with scoring script](how-to-mlflow-batch.md#customize-model-deployment-with-scoring-script) for batch endpoints.

> [!IMPORTANT]
> If you choose to specify a scoring script for an MLflow model deployment, you also need to provide an environment for the deployment.

## Deployment tools

Azure Machine Learning provides the following tools for deploying MLflow models to online and batch endpoints:

- [MLflow SDK](https://mlflow.org/docs/latest/python_api/index.html)
- [Azure Machine Learning CLI v2](concept-v2.md)
- [Azure Machine Learning SDK for Python](/python/api/overview/azure/ml/)
- [Azure Machine Learning studio](overview-what-is-azure-machine-learning.md#studio)

Each tool has different capabilities, particularly for which type of compute it can target. The following table shows the support for different MLflow deployment scenarios.

| Scenario | MLflow SDK | Azure Machine Learning CLI/SDK or studio |
|---| :- | :- |
| Deploy to managed online endpoints.<sup>1</sup> | Supported. See [Progressive rollout of MLflow models to online endpoints](how-to-deploy-mlflow-models-online-progressive.md). | Supported. See [Deploy MLflow models to online endpoints](how-to-deploy-mlflow-models-online-endpoints.md). |
| Deploy to managed online endpoints with a scoring script. | Not supported.<sup>3</sup> | Supported. See [Customize MLflow model deployments](how-to-deploy-mlflow-models-online-endpoints.md#customize-mlflow-model-deployments). |
| Deploy to batch endpoints. | Not supported.<sup>3</sup> | Supported. See [Use MLflow models in batch deployments](how-to-mlflow-batch.md). |
| Deploy to batch endpoints with a scoring script. | Not supported.<sup>3</sup> | Supported. See [Customize model deployment with scoring script](how-to-mlflow-batch.md#customize-model-deployment-with-scoring-script). |
| Deploy to web services like Azure Container Instances or Azure Kubernetes Service (AKS). | Legacy support.<sup>2</sup> | Not supported.<sup>2</sup> |
| Deploy to web services like Container Instances or AKS with a scoring script. | Not supported.<sup>3</sup> | Legacy support.<sup>2</sup> |


<sup>1</sup> Switch to [managed online endpoints](concept-endpoints.md) if possible.

<sup>2</sup> Open-source MLflow doesn't support scoring scripts or batch execution.

### Choose a deployment tool

Use the MLflow SDK if both of the following are true:
- You're familiar with MLflow and want to continue using the same methods.
- You're using a platform like Azure Databricks that supports MLflow natively.

Use the Azure Machine Learning CLI v2 or SDK for Python if any of the following is true:
- You're familiar with the tool.
- You want to automate deployment by using pipelines.
- You want to store deployment configuration in a Git repository.

Use the Azure Machine Learning studio UI if you want to quickly deploy and test models trained with MLflow.

## Related content

- [MLflow model deployment to online endpoints](how-to-deploy-mlflow-models-online-endpoints.md)
- [MLflow model deployment to batch endpoints](how-to-mlflow-batch.md)
- [Progressive rollout of MLflow models](how-to-deploy-mlflow-models-online-progressive.md)
