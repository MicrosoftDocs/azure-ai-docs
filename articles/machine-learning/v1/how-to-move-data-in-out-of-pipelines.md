---
title: Moving Data in ML Pipelines
titleSuffix: Azure Machine Learning
description: Learn how Azure Machine Learning pipelines ingest data, and how to manage and move data between pipeline steps.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: mldata
ms.author: scottpolly
author: lgayhardt
ms.reviewer: soumyapatro
ms.date: 06/24/2025
ms.topic: how-to
ms.custom: UpdateFrequency5, devx-track-python, data4ml, sdkv1
#Customer intent: As a data scientist using Python, I want to get data into my pipeline and propogate it between steps.
---

# Moving data into and between machine learning pipeline steps (Python)

[!INCLUDE [sdk v1](../includes/machine-learning-sdk-v1.md)]

[!INCLUDE [v1 deprecation](../includes/sdk-v1-deprecation.md)]

This article provides code for importing data, transforming data, and moving data between steps in an Azure Machine Learning pipeline. For an overview of how data works in Azure Machine Learning, see [Access data in Azure storage services](how-to-access-data.md). For information about the benefits and structure of Azure Machine Learning pipelines, see [What are Azure Machine Learning pipelines?](../concept-ml-pipelines.md).

This article shows how to:

- Use `Dataset` objects for preexisting data
- Access data within your steps
- Split `Dataset` data into subsets, such as training and validation subsets
- Create `OutputFileDatasetConfig` objects to transfer data to the next pipeline step
- Use `OutputFileDatasetConfig` objects as input to pipeline steps
- Create new `Dataset` objects from `OutputFileDatasetConfig` that you want to persist

## Prerequisites

- An Azure subscription. If you don't have one, create a free account before you begin. Try the [free or paid version of Azure Machine Learning](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

- The [Azure Machine Learning SDK for Python](/python/api/overview/azure/ml/intro), or access to [Azure Machine Learning studio](https://ml.azure.com/).

- An Azure Machine Learning workspace.
  
  Either [create an Azure Machine Learning workspace](../quickstart-create-resources.md) or use an existing one via the Python SDK. Import the `Workspace` and `Datastore` classes, and load your subscription information from the `config.json` file by using the function `from_config()`. This function looks for the JSON file in the current directory by default, but you can also specify a path parameter to point to the file by using `from_config(path="your/file/path")`.

   ```python
   import azureml.core
   from azureml.core import Workspace, Datastore
        
   ws = Workspace.from_config()
   ```

- Some preexisting data. This article briefly shows the use of an [Azure blob container](/azure/storage/blobs/storage-blobs-overview).

- Optional: An existing machine learning pipeline, such as the one described in [Create and run machine learning pipelines with Azure Machine Learning SDK](./how-to-create-machine-learning-pipelines.md).

## Use `Dataset` objects for preexisting data 

The preferred way to ingest data into a pipeline is to use a [Dataset](/python/api/azureml-core/azureml.core.dataset%28class%29) object. `Dataset` objects represent persistent data that's available throughout a workspace.

There are many ways to create and register `Dataset` objects. Tabular datasets are for delimited data that's available in one or more files. File datasets are for binary data (such as images) or for data that you parse. The simplest programmatic ways to create `Dataset` objects are to use existing blobs in workspace storage or public URLs:

```python
datastore = Datastore.get(workspace, 'training_data')
iris_dataset = Dataset.Tabular.from_delimited_files(DataPath(datastore, 'iris.csv'))

datastore_path = [
    DataPath(datastore, 'animals/dog/1.jpg'),
    DataPath(datastore, 'animals/dog/2.jpg'),
    DataPath(datastore, 'animals/cat/*.jpg')
]
cats_dogs_dataset = Dataset.File.from_files(path=datastore_path)
```

For more information about creating datasets with different options and from different sources, registering them and reviewing them in the Azure Machine Learning UI, understanding how data size interacts with compute capacity, and versioning them, see [Create Azure Machine Learning datasets](how-to-create-register-datasets.md). 

### Pass datasets to your script

To pass the dataset's path to your script, use the `Dataset` object's `as_named_input()` method. You can either pass the resulting `DatasetConsumptionConfig` object to your script as an argument or, by using the `inputs` argument to your pipeline script, you can retrieve the dataset by using `Run.get_context().input_datasets[]`.

After you create a named input, you can choose its access mode (for `FileDataset` only): `as_mount()` or `as_download()`. If your script processes all the files in your dataset and the disk on your compute resource is large enough for the dataset, the download access mode is a better choice. The download access mode avoids the overhead of streaming the data at runtime. If your script accesses a subset of the dataset or is too large for your compute, use the mount access mode. For more information, see [Mount vs. download](how-to-train-with-datasets.md#mount-vs-download).

To pass a dataset to your pipeline step:

1. Use `TabularDataset.as_named_input()` or `FileDataset.as_named_input()` (no *s* at the end) to create a `DatasetConsumptionConfig` object
1. **For `FileDataset` only:** Use `as_mount()` or `as_download()` to set the access mode. With `TabularDataset`, you can't set the access mode. 
1. Pass the datasets to your pipeline steps by using either `arguments` or `inputs`.

The following snippet shows the common pattern of combining these steps within the `PythonScriptStep` constructor by using `iris_dataset` (`TabularDataset`): 

```python

train_step = PythonScriptStep(
    name="train_data",
    script_name="train.py",
    compute_target=cluster,
    inputs=[iris_dataset.as_named_input('iris')]
)
```

> [!NOTE]
> You need to replace the values for all of these arguments (that is, `"train_data"`, `"train.py"`, `cluster`, and `iris_dataset`) with your own data. 
> The above snippet just shows the form of the call and isn't part of a Microsoft sample. 

You can also use methods like `random_split()` and `take_sample()` to create multiple inputs or to reduce the amount of data that's passed to your pipeline step:

```python
seed = 42 # PRNG seed
smaller_dataset = iris_dataset.take_sample(0.1, seed=seed) # 10%
train, test = smaller_dataset.random_split(percentage=0.8, seed=seed)

train_step = PythonScriptStep(
    name="train_data",
    script_name="train.py",
    compute_target=cluster,
    inputs=[train.as_named_input('train'), test.as_named_input('test')]
)
```

### Access datasets within your script

Named inputs to your pipeline step script are available as a dictionary within the `Run` object. Retrieve the active `Run` object by using `Run.get_context()`, and then retrieve the dictionary of named inputs by using `input_datasets`. If you passed the `DatasetConsumptionConfig` object by using the `arguments` argument rather than the `inputs` argument, access the data by using `ArgumentParser` code. Both techniques are demonstrated in the following snippets:

__The pipeline definition script__

```python
# Code is for demonstration only: It would be confusing to split datasets between `arguments` and `inputs`
train_step = PythonScriptStep(
    name="train_data",
    script_name="train.py",
    compute_target=cluster,
    # Datasets passed as arguments
    arguments=['--training-folder', train.as_named_input('train').as_download()],
    # Datasets passed as inputs
    inputs=[test.as_named_input('test').as_download()]
)
```

__The `train.py` script referenced from the PythonScriptStep__

```python
# In pipeline script
parser = argparse.ArgumentParser()
# Retrieve the dataset passed as an argument
parser.add_argument('--training-folder', type=str, dest='train_folder', help='training data folder mounting point')
args = parser.parse_args()
training_data_folder = args.train_folder
# Retrieve the dataset passed as an input
testing_data_folder = Run.get_context().input_datasets['test']
```

The passed value is the path to the dataset file or files.

Because registered datasets are persistent and shared across a workspace, you can retrieve them directly:

```python
run = Run.get_context()
ws = run.experiment.workspace
ds = Dataset.get_by_name(workspace=ws, name='mnist_opendataset')
```

> [!NOTE]
> The preceding snippets show the form of the calls. They aren't part of a Microsoft sample. You need to replace the arguments with values from your own project.

## Use `OutputFileDatasetConfig` for intermediate data

Although `Dataset` objects represent only persistent data, [`OutputFileDatasetConfig`](/python/api/azureml-core/azureml.data.outputfiledatasetconfig) objects can be used for temporary data output from pipeline steps and for persistent output data. `OutputFileDatasetConfig` supports writing data to blob storage, fileshare, Azure Data Lake Storage Gen1, or Data Lake Storage Gen2. It supports both mount mode and upload mode. In mount mode, files written to the mounted directory are permanently stored when the file is closed. In upload mode, files written to the output directory are uploaded at the end of the job. If the job fails or is canceled, the output directory isn't uploaded.

 The `OutputFileDatasetConfig` object's default behavior is to write to the default datastore of the workspace. Pass your `OutputFileDatasetConfig` objects to your `PythonScriptStep` by using the `arguments` parameter.

```python
from azureml.data import OutputFileDatasetConfig
dataprep_output = OutputFileDatasetConfig()
input_dataset = Dataset.get_by_name(workspace, 'raw_data')

dataprep_step = PythonScriptStep(
    name="prep_data",
    script_name="dataprep.py",
    compute_target=cluster,
    arguments=[input_dataset.as_named_input('raw_data').as_mount(), dataprep_output]
    )
```

> [!NOTE]
> Concurrent writes to a `OutputFileDatasetConfig` will fail. Don't try to use a single `OutputFileDatasetConfig` concurrently. Don't share a single `OutputFileDatasetConfig` in a multiprocessing situation, like when you use [distributed training](../how-to-train-distributed-gpu.md). 

### Use `OutputFileDatasetConfig` as outputs of a training step

In your pipeline's `PythonScriptStep`, you can retrieve the available output paths by using the program's arguments. If this step is the first one and will initialize the output data, you need to create the directory at the specified path. You can then write whatever files you want to be contained in the `OutputFileDatasetConfig`.

```python
parser = argparse.ArgumentParser()
parser.add_argument('--output_path', dest='output_path', required=True)
args = parser.parse_args()

# Make directory for file
os.makedirs(os.path.dirname(args.output_path), exist_ok=True)
with open(args.output_path, 'w') as f:
    f.write("Step 1's output")
```

### Read `OutputFileDatasetConfig` as inputs to non-initial steps

After the initial pipeline step writes some data to the `OutputFileDatasetConfig` path and it becomes an output of that initial step, it can be used as an input to a later step. 

In the following code: 

* `step1_output_data` indicates that the output of the `PythonScriptStep` `step1` is written to the Data Lake Storage Gen2 datastore `my_adlsgen2` in upload access mode. For information about setting up role permissions in order to write data back to Data Lake Storage Gen2 datastores, see [Connect to storage services on Azure with datastores](how-to-access-data.md). 

* After `step1` completes and the output is written to the destination that's indicated by `step1_output_data`, `step2` is ready to use `step1_output_data` as an input. 

```python
# Get Data Lake Storage Gen2 datastore that's already registered with the workspace
datastore = workspace.datastores['my_adlsgen2']
step1_output_data = OutputFileDatasetConfig(name="processed_data", destination=(datastore, "mypath/{run-id}/{output-name}")).as_upload()

step1 = PythonScriptStep(
    name="generate_data",
    script_name="step1.py",
    runconfig = aml_run_config,
    arguments = ["--output_path", step1_output_data]
)

step2 = PythonScriptStep(
    name="read_pipeline_data",
    script_name="step2.py",
    compute_target=compute,
    runconfig = aml_run_config,
    arguments = ["--pd", step1_output_data.as_input()]

)

pipeline = Pipeline(workspace=ws, steps=[step1, step2])
```

> [!TIP]
> The process for reading the data in the Python script `step2.py` is the same as the process described earlier in [Access datasets within your script](#access-datasets-within-your-script). Use `ArgumentParser` to add an argument of `--pd` in your script to access the data.

## Register `OutputFileDatasetConfig` objects for reuse

If you want to make an `OutputFileDatasetConfig` object available for longer than the duration of your experiment, register it to your workspace to share and reuse across experiments:

```python
step1_output_ds = step1_output_data.register_on_complete(
    name='processed_data', 
    description = 'files from step1'
)
```

## Delete `OutputFileDatasetConfig` content when it's no longer needed

Azure doesn't automatically delete intermediate data that's written with `OutputFileDatasetConfig`. To avoid storage charges for large amounts of unneeded data, you should take one of the following actions:

* Programmatically delete intermediate data at the end of a pipeline job, when it's no longer needed. 
* Use blob storage with a short-term storage policy for intermediate data. (See [Optimize costs by automating Azure Blob Storage access tiers](/azure/storage/blobs/lifecycle-management-overview).) This policy can be set only on a workspace's nondefault datastore. Use `OutputFileDatasetConfig` to export intermediate data to another datastore that isn't the default.

  ```Python
  # Get Data Lake Storage Gen2 datastore that's already registered with the workspace
  datastore = workspace.datastores['my_adlsgen2']
  step1_output_data = OutputFileDatasetConfig(name="processed_data", destination=(datastore, "mypath/{run-id}/{output-name}")).as_upload()
  ```

* Regularly review data and delete data that you don't need.

> [!CAUTION]
> Only delete intermediate data after 30 days from the last change date of the data. Deleting intermediate data earlier could cause the pipeline run to fail because the pipeline assumes the data exists for a 30 day period for reuse.

For more information, see [Plan to manage costs for Azure Machine Learning](../concept-plan-manage-cost.md).

## Next steps

* [Create an Azure Machine Learning dataset](how-to-create-register-datasets.md)
* [Create and run machine learning pipelines with Azure Machine Learning SDK](how-to-create-machine-learning-pipelines.md)
