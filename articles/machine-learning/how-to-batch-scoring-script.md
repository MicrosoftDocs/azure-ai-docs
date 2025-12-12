---
title: 'Author scoring scripts for batch deployments'
titleSuffix: Azure Machine Learning
description: In this article, learn how to author scoring scripts to perform batch inference in batch deployments.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: inferencing
ms.topic: concept-article
author: s-polly
ms.author: scottpolly
ms.reviewer: jturuk
ms.date: 11/13/2025
ms.custom: how-to, update-code2
---

# Author scoring scripts for batch deployments

[!INCLUDE [cli v2](includes/machine-learning-dev-v2.md)]

Batch endpoints allow you to deploy models that perform long-running inference at scale. When deploying models, you must create and specify a scoring script (also known as a **batch driver script**) to indicate how to use the model over the input data to create predictions. In this article, you learn how to use scoring scripts in model deployments for different scenarios. You also learn about best practices for batch endpoints.

> [!TIP]
> MLflow models don't require a scoring script. The service autogenerates it for you. For more information about how batch endpoints work with MLflow models, visit the [Using MLflow models in batch deployments](how-to-mlflow-batch.md) dedicated tutorial.

> [!WARNING]
> To deploy an Automated ML model under a batch endpoint, note that Automated ML provides a scoring script that only works for online endpoints. That scoring script isn't designed for batch execution. For more information about how to create a scoring script that's customized for what your model does, see the following guidelines.

## Understanding the scoring script

The scoring script is a Python file (`.py`) that specifies how to run the model and read the input data that the batch deployment executor submits. Each model deployment provides the scoring script (along with all other required dependencies) at creation time. The scoring script usually looks like this:

# [Azure CLI](#tab/cli)

__deployment.yml__

:::code language="yaml" source="~/azureml-examples-main/cli/endpoints/batch/deploy-models/mnist-classifier/deployment-torch/deployment.yml" range="9-11":::

# [Python](#tab/python)

```python
deployment = ModelBatchDeployment(
    ...
    code_configuration=CodeConfiguration(
        code="src",
        scoring_script="batch_driver.py"
    ),
    ...
)
```

# [Studio](#tab/azure-studio)

When you create a new deployment, you receive prompts for a scoring script and dependencies as shown here:

:::image type="content" source="./media/how-to-batch-scoring-script/configure-scoring-script.png" alt-text="Screenshot of the step where you can configure the scoring script in a new deployment.":::

For MLflow models, scoring scripts are automatically generated but you can indicate one by selecting this option:

:::image type="content" source="./media/how-to-batch-scoring-script/configure-scoring-script-mlflow.png" alt-text="Screenshot of the step where you can configure the scoring script in a new deployment when the model has MLflow format.":::

---

The scoring script must contain two methods:

#### The `init` method

Use the `init()` method for any costly or common preparation. For example, use it to load the model into memory. The start of the entire batch job calls this function one time. The files of your model are available in a path determined by the environment variable `AZUREML_MODEL_DIR`. Depending on how you registered your model, its files might be contained in a folder. In the next example, the model has several files in a folder named `model`. For more information, visit [how you can determine the folder that your model uses](#using-models-that-are-folders).

```python
def init():
    global model

    # AZUREML_MODEL_DIR is an environment variable created during deployment
    # The path "model" is the name of the registered model's folder
    model_path = os.path.join(os.environ["AZUREML_MODEL_DIR"], "model")

    # load the model
    model = load_model(model_path)
```

In this example, you place the model in global variable `model`. To make available the assets required to perform inference on your scoring function, use global variables.

#### The `run` method

Use the `run(mini_batch: List[str]) -> Union[List[Any], pandas.DataFrame]` method to handle the scoring of each mini-batch that the batch deployment generates. This method is called once for each `mini_batch` generated for your input data. Batch deployments read data in batches according to how you configure the deployment.

```python
import pandas as pd
from typing import List, Any, Union

def run(mini_batch: List[str]) -> Union[List[Any], pd.DataFrame]:
    results = []

    for file in mini_batch:
        (...)

    return pd.DataFrame(results)
```

The method receives a list of file paths as a parameter (`mini_batch`). You can use this list to iterate over and individually process each file, or to read the entire batch and process it all at once. The best option depends on your compute memory and the throughput you need to achieve. For an example that describes how to read entire batches of data at once, visit [High throughput deployments](how-to-image-processing-batch.md#high-throughput-deployments).

> [!NOTE]
> __How is work distributed?__
> 
> Batch deployments distribute work at the file level, which means that a folder that contains 100 files, with mini-batches of 10 files, generates 10 batches of 10 files each. Note that the sizes of the relevant files have no relevance. For files too large to process in large mini-batches, split the files into smaller files to achieve a higher level of parallelism, or decrease the number of files per mini-batch. At this time, batch deployment can't account for skews in the file's size distribution.

The `run()` method should return a Pandas `DataFrame` or an array/list. Each returned output element indicates one successful run of an input element in the input `mini_batch`. For file or folder data assets, each returned row/element represents a single file processed. For a tabular data asset, each returned row/element represents a row in a processed file.

> [!IMPORTANT]
> __How to write predictions?__
> 
> Everything that the `run()` function returns is appended in the output predictions file that the batch job generates. It's important to return the right data type from this function. Return __arrays__ when you need to output a single prediction. Return __pandas DataFrames__ when you need to return multiple pieces of information. For instance, for tabular data, you might want to append your predictions to the original record. Use a pandas DataFrame to do this. Although a pandas DataFrame might contain column names, the output file doesn't include those names.
>
> To write predictions in a different way, you can [customize outputs in batch deployments](how-to-deploy-model-custom-output.md).

> [!WARNING]
> In the `run` function, don't output complex data types (or lists of complex data types) instead of `pandas.DataFrame`. Those outputs are transformed to strings and they become hard to read.

The resulting DataFrame or array is appended to the indicated output file. There's no requirement about the cardinality of the results. One file can generate one or many rows/elements in the output. All elements in the result DataFrame or array are written to the output file as-is (considering the `output_action` isn't `summary_only`).

#### Python packages for scoring

You must indicate any library that your scoring script requires to run in the environment where your batch deployment runs. For scoring scripts, indicate environments per deployment. Usually, you indicate your requirements using a `conda.yml` dependencies file, which might look like this:

__mnist/environment/conda.yaml__
        
:::code language="yaml" source="~/azureml-examples-main/cli/endpoints/batch/deploy-models/mnist-classifier/deployment-torch/environment/conda.yaml":::

Visit [Create a batch deployment](how-to-use-batch-model-deployments.md#create-a-batch-deployment) for more information about how to indicate the environment for your model.

## Writing predictions in a different way

By default, the batch deployment writes the model's predictions in a single file as indicated in the deployment. However, in some cases, you must write the predictions in multiple files. For instance, for partitioned input data, you likely want to generate partitioned output as well. In those cases, you can [Customize outputs in batch deployments](how-to-deploy-model-custom-output.md) to indicate:

> [!div class="checklist"]
> * The file format (CSV, parquet, json, etc) used to write predictions
> * The way data is partitioned in the output

For more information, see [Customize outputs in batch deployments](how-to-deploy-model-custom-output.md).

## Source control of scoring scripts

Place scoring scripts under source control.

## Best practices for writing scoring scripts

When writing scoring scripts that handle large amounts of data, consider several factors, including

* The size of each file
* The amount of data in each file
* The amount of memory required to read each file
* The amount of memory required to read an entire batch of files
* The memory footprint of the model
* The model memory footprint when running over the input data
* The available memory in your compute

Batch deployments distribute work at the file level. This distribution means that a folder that contains 100 files, in mini-batches of 10 files, generates 10 batches of 10 files each (regardless of the size of the files involved). For files too large to process in large mini-batches, split the files into smaller files to achieve a higher level of parallelism, or decrease the number of files per mini-batch. At this time, batch deployment can't account for skews in the file size distribution.

### Relationship between the degree of parallelism and the scoring script

Your deployment configuration controls both the size of each mini-batch and the number of workers on each node. This configuration matters when you decide whether to read the entire mini-batch to perform inference, run inference file by file, or run the inference row by row (for tabular). For more information, see [Running inference at the mini-batch, file, or row level](#running-inference-at-the-mini-batch-file-or-row-level).

When you run multiple workers on the same instance, remember that all the workers share memory. If you increase the number of workers per node, you should generally decrease the mini-batch size or change the scoring strategy if data size and compute SKU remain the same.

### Running inference at the mini-batch, file, or row level

Batch endpoints call the `run()` function in a scoring script once per mini-batch. However, you can decide if you want to run the inference over the entire batch, over one file at a time, or over one row at a time for tabular data.

#### Mini-batch level

You typically run inference over the entire batch to achieve high throughput in your batch scoring process. This approach works well if you run inference over a GPU, where you want to saturate the inference device. You might also rely on a data loader that can handle the batching itself if data doesn't fit in memory, like `TensorFlow` or `PyTorch` data loaders. In these cases, you run inference on the entire batch.

> [!WARNING]
> Running inference at the batch level might require close control over the input data size, to correctly account for the memory requirements and to avoid out-of-memory exceptions. Whether or not you can load the entire mini-batch in memory depends on the size of the mini-batch, the size of the instances in the cluster, the number of workers on each node, and the size of the mini-batch.

Visit [High throughput deployments](how-to-image-processing-batch.md#high-throughput-deployments) to learn how to achieve this. This example processes an entire batch of files at a time.

#### File level

One of the easiest ways to perform inference is to iterate over all the files in the mini-batch, then run the model over each file. In some cases, such as image processing, this approach works well. For tabular data, you need to estimate the number of rows in each file. This estimate shows whether your model can handle the memory requirements to both load the entire data into memory and perform inference over it. Some models (especially those models based on recurrent neural networks) unfold and present a memory footprint with a potentially nonlinear row count. For a model with high memory expense, consider running inference at the row level.

> [!TIP]
> Consider breaking down files that are too large to read at once into multiple smaller files, to improve parallelization.

Visit [Image processing with batch deployments](how-to-image-processing-batch.md) to learn how to do this. That example processes a file at a time.

#### Row level (tabular)

For models that present challenges with their input sizes, you might want to run inference at the row level. Your batch deployment still provides your scoring script with a mini-batch of files. However, you read one file, one row at a time. This approach might seem inefficient, but for some deep learning models it might be the only way to perform inference without scaling up your hardware resources.

Visit [Text processing with batch deployments](how-to-nlp-processing-batch.md) to learn how to do this. That example processes a row at a time.

### Using models that are folders

The `AZUREML_MODEL_DIR` environment variable contains the path to the selected model location. The `init()` function typically uses it to load the model into memory. However, some models might contain their files in a folder, and you might need to account for that structure when loading them. You can identify the folder structure of your model as shown here:

1. Go to [Azure Machine Learning portal](https://ml.azure.com).

1. Go to the **Models** section.

1. Select the model you want to deploy, and select the **Artifacts** tab.

1. Note the displayed folder. This folder is indicated when the model is registered.

    :::image type="content" source="media/how-to-deploy-mlflow-models-online-endpoints/mlflow-model-folder-name.png" lightbox="media/how-to-deploy-mlflow-models-online-endpoints/mlflow-model-folder-name.png" alt-text="Screenshot showing the folder where the model artifacts are placed.":::

Use this path to load the model:

```python
def init():
    global model

    # AZUREML_MODEL_DIR is an environment variable created during deployment
    # The path "model" is the name of the registered model's folder
    model_path = os.path.join(os.environ["AZUREML_MODEL_DIR"], "model")

    model = load_model(model_path)
```

## Next steps

* [Troubleshooting batch endpoints](how-to-troubleshoot-batch-endpoints.md)
* [Use MLflow models in batch deployments](how-to-mlflow-batch.md)
* [Image processing with batch deployments](how-to-image-processing-batch.md)