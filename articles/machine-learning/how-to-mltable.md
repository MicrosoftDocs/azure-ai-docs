---
title: Working with tables in Azure Machine Learning
titleSuffix: Azure Machine Learning
description: Learn how to work with tables (meltable) in Azure Machine Learning.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: mldata
ms.topic: how-to
ms.author: scottpolly
author: s-polly
ms.reviewer: samkemp
ms.date: 09/18/2025
ms.custom: data4ml
# Customer intent: As an experienced Python developer, I need to make my Azure storage data available to my remote compute, to train my machine learning models.
---

# Working with tables in Azure Machine Learning

[!INCLUDE [dev v2](includes/machine-learning-dev-v2.md)]

Azure Machine Learning supports a Table type (`mltable`). This allows for the creation of a *blueprint* that defines how to load data files into memory as a Pandas or Spark data frame. In this article you learn:

> [!div class="checklist"]
> - When to use Azure Machine Learning Tables instead of Files or Folders
> - How to install the `mltable` SDK
> - How to define a data loading blueprint using an `mltable` file
> - Examples that show how `mltable` is used in Azure Machine Learning
> - How to use the `mltable` during interactive development (for example, in a notebook)

## Prerequisites

- An Azure subscription. If you don't already have an Azure subscription, create a free account before you begin. Try the [free or paid version of Azure Machine Learning](https://azure.microsoft.com/free/)

- The [Azure Machine Learning SDK for Python](https://aka.ms/sdk-v2-install)

- An Azure Machine Learning workspace

> [!IMPORTANT]
> Ensure you have the latest `mltable` package installed in your Python environment:
> ```bash
> pip install -U mltable azureml-dataprep[pandas]
> ```

### Clone the examples repository

The code snippets in this article are based on examples in the [Azure Machine Learning examples GitHub repo](https://github.com/Azure/azureml-examples/tree/main/sdk/python/using-mltable). To clone the repository to your development environment, use this command:

```bash
git clone --depth 1 https://github.com/Azure/azureml-examples
```

> [!TIP]
> Use `--depth 1` to clone only the latest commit to the repository. This reduces the time needed to complete the operation.

You can find examples relevant to Azure Machine Learning Tables in this folder of the cloned repo:

```bash
cd azureml-examples/sdk/python/using-mltable
```

## Introduction

Azure Machine Learning Tables (`mltable`) allow you to define how you want to *load* your data files into memory, as a Pandas and/or Spark data frame. Tables have two key features:

1. **An MLTable file.** A YAML-based file that defines the data loading *blueprint*. In the MLTable file, you can specify:
    - The storage location or locations of the data - local, in the cloud, or on a public http(s) server.
    - *Globbing* patterns over cloud storage. These locations can specify sets of filenames, with wildcard characters (`*`).
    - *read transformation* - for example, the file format type (delimited text, Parquet, Delta, json), delimiters, headers, etc.
    - Column type conversions (to enforce schema).
    - New column creation, using folder structure information - for example, creation of a year and month column, using the `{year}/{month}` folder structure in the path.
    - *Subsets of data* to load - for example, filter rows, keep/drop columns, take random samples.
1. **A fast and efficient engine** to load the data into a Pandas or Spark dataframe, according to the blueprint defined in the MLTable file. The engine relies on [Rust](https://www.rust-lang.org/) for high speed and memory efficiency.

Azure Machine Learning Tables are useful in these scenarios:

- You need to [glob](https://wikipedia.org/wiki/Glob_(programming)) over storage locations.
- You need to create a table using data from different storage locations (for example, different blob containers).
- The path contains relevant information that you want to capture in your data (for example, date and time).
- The data schema changes frequently.
- You want easy *reproducibility* of your data loading steps.
- You only need a subset of large data.
- Your data contains storage locations that you want to stream into your Python session. For example, you want to stream `path` in the following JSON lines structure: `[{"path": "abfss://fs@account.dfs.core.windows.net/my-images/cats/001.jpg", "label":"cat"}]`.
- You want to train ML models using Azure Machine Learning AutoML.

> [!TIP]
> For tabular data, Azure Machine Learning *doesn't require* use of Azure Machine Learning Tables (`mltable`). You can use Azure Machine Learning File (`uri_file`) and Folder (`uri_folder`) types, and your own parsing logic loads the data into a Pandas or Spark data frame.
>
> For a simple CSV file or Parquet folder, it's **easier** to use Azure Machine Learning Files/Folders instead of Tables.

## Azure Machine Learning Tables Quickstart

In this quickstart, you create a Table (`mltable`) of the [NYC Green Taxi Data](../open-datasets/dataset-taxi-green.md?tabs=azureml-opendatasets) from Azure Open Datasets. The data has a parquet format, and it covers the years 2008-2021. On a publicly accessible blob storage account, the data files have this folder structure:

```text
/
└── green
    ├── puYear=2008
    │   ├── puMonth=1
    │   │   ├── _committed_2983805876188002631
    │   │   └── part-XXX.snappy.parquet
    │   ├── ...
    │   └── puMonth=12
    │       ├── _committed_2983805876188002631
    │       └── part-XXX.snappy.parquet
    ├── ...
    └── puYear=2021
        ├── puMonth=1
        │   ├── _committed_2983805876188002631
        │   └── part-XXX.snappy.parquet
        ├── ...
        └── puMonth=12
            ├── _committed_2983805876188002631
            └── part-XXX.snappy.parquet
```

With this data, you need to load into a Pandas data frame:

- Only the parquet files for years 2015-19
- A random sample of the data
- Only rows with a rip distance greater than 0
- Relevant columns for Machine Learning
- New columns - year and month - using the path information (`puYear=X/puMonth=Y`)

Pandas code handles this. However, achieving *reproducibility* would become difficult because you must either:

- Share code, which means that if the schema changes (for example, a column name might change) then all users must update their code
- Write an ETL pipeline, which has heavy overhead

Azure Machine Learning Tables provide a light-weight mechanism to serialize (save) the data loading steps in an `MLTable` file. Then, you and members of your team can *reproduce* the Pandas data frame. If the schema changes, you only update the `MLTable` file, instead of updates in many places that involve Python data loading code.

### Clone the quickstart notebook or create a new notebook/script

If you use an Azure Machine Learning compute instance, [Create a new notebook](quickstart-run-notebooks.md#create-a-new-notebook). If you use an IDE, you should create a new Python script.

Additionally, the quickstart notebook is available in the [Azure Machine Learning examples GitHub repo](https://github.com/Azure/azureml-examples/blob/main/sdk/python/using-mltable/quickstart/mltable-quickstart.ipynb). Use this code to clone and access the Notebook:

```bash
git clone --depth 1 https://github.com/Azure/azureml-examples
cd azureml-examples/sdk/python/using-mltable/quickstart
```

### Install the `mltable` Python SDK

To load the NYC Green Taxi Data into an Azure Machine Learning Table, you must have the `mltable` Python SDK and `pandas` installed in your Python environment, with this command:

```bash
pip install -U mltable azureml-dataprep[pandas]
```

### Author an MLTable file

Use the `mltable` Python SDK to create an MLTable file, to document the data loading blueprint. For this, copy-and-paste the following code into your Notebook/Script, and then execute that code:

```python
import mltable

# glob the parquet file paths for years 2015-19, all months.
paths = [
    {
        "pattern": "wasbs://nyctlc@azureopendatastorage.blob.core.windows.net/green/puYear=2015/puMonth=*/*.parquet"
    },
    {
        "pattern": "wasbs://nyctlc@azureopendatastorage.blob.core.windows.net/green/puYear=2016/puMonth=*/*.parquet"
    },
    {
        "pattern": "wasbs://nyctlc@azureopendatastorage.blob.core.windows.net/green/puYear=2017/puMonth=*/*.parquet"
    },
    {
        "pattern": "wasbs://nyctlc@azureopendatastorage.blob.core.windows.net/green/puYear=2018/puMonth=*/*.parquet"
    },
    {
        "pattern": "wasbs://nyctlc@azureopendatastorage.blob.core.windows.net/green/puYear=2019/puMonth=*/*.parquet"
    },
]

# create a table from the parquet paths
tbl = mltable.from_parquet_files(paths)

# table a random sample
tbl = tbl.take_random_sample(probability=0.001, seed=735)

# filter trips with a distance > 0
tbl = tbl.filter("col('tripDistance') > 0")

# Drop columns
tbl = tbl.drop_columns(["puLocationId", "doLocationId", "storeAndFwdFlag"])

# Create two new columns - year and month - where the values are taken from the path
tbl = tbl.extract_columns_from_partition_format("/puYear={year}/puMonth={month}")

# print the first 5 records of the table as a check
tbl.show(5)
```

You can optionally choose to load the MLTable object into Pandas, using:

```python
# You can load the table into a pandas dataframe
# NOTE: The data is in East US region and the data is large, so this will take several minutes (~7mins)
# to load if you are in a different region.

df = tbl.to_pandas_dataframe()
```

#### Save the data loading steps
Next, save all your data loading steps into an MLTable file. Saving your data loading steps in an MLTable file allows you to reproduce your Pandas data frame at a later point in time, without need to redefine the code each time.

You can save the MLTable yaml file to a cloud storage resource, or you can save it to local path resources.
```python
# save the data loading steps in an MLTable file to a cloud storage resource
# NOTE: the tbl object was defined in the previous snippet.
tbl.save(path="azureml://subscriptions/<subid>/resourcegroups/<rgname>/workspaces/<wsname>/datastores/<name>/paths/nyc_taxi", colocated=True, show_progress=True, overwrite=True)
```

```python
# save the data loading steps in an MLTable file to a local resource
# NOTE: the tbl object was defined in the previous snippet.
tbl.save("./nyc_taxi")
```

> [!IMPORTANT]
> - If colocated == True, then we will copy the data to the same folder with the MLTable yaml file if they are not currently colocated, and we will use relative paths in MLTable yaml.
> - If colocated == False, we will not move the data, we will use absolute paths for cloud data, and use relative paths for local data.
> - We don't support this parameter combination: data is stored in a local resource, colocated == False, `path` targets a cloud directory. Please upload your local data to cloud, and use the cloud data paths for MLTable instead.
>

### Reproduce data loading steps
Now that you serialized the data loading steps into a file, you can reproduce them at any point in time with the load() method. This way, you don't need to redefine your data loading steps in code, and you can more easily share the file.

```python
import mltable

# load the previously saved MLTable file
tbl = mltable.load("./nyc_taxi/")
tbl.show(5)

# You can load the table into a pandas dataframe
# NOTE: The data is in East US region and the data is large, so this will take several minutes (~7mins)
# to load if you are in a different region.

# load the table into pandas
df = tbl.to_pandas_dataframe()

# print the head of the data frame
df.head()
# print the shape and column types of the data frame
print(f"Shape: {df.shape}")
print(f"Columns:\n{df.dtypes}")
```

#### Create a data asset to aid sharing and reproducibility

You might have your MLTable file currently saved on disk, which makes it hard to share with team members. When you create a data asset in Azure Machine Learning, your MLTable is uploaded to cloud storage and "bookmarked."Your team members can then access the MLTable with a friendly name. Also, the data asset is versioned.

# [CLI](#tab/cli)

```azurecli
az ml data create --name green-quickstart --version 1 --path ./nyc_taxi --type mltable
```

> [!NOTE]
> The path points to the **folder** that contains the `MLTable` file.

# [Python](#tab/Python-SDK)

Set your subscription, resource group, and workspace:

```python
subscription_id = "<SUBSCRIPTION_ID>"
resource_group = "<RESOURCE_GROUP>"
workspace = "<AML_WORKSPACE_NAME>"
```

You can create a data asset in Azure Machine Learning with this Python Code:

```python
from azure.ai.ml import MLClient
from azure.ai.ml.entities import Data
from azure.ai.ml.constants import AssetTypes
from azure.identity import DefaultAzureCredential

# set VERSION variable
VERSION="1"

# connect to the AzureML workspace
# NOTE: the subscription_id, resource_group, workspace variables are set
# in the previous code snippet.
ml_client = MLClient(
    DefaultAzureCredential(), subscription_id, resource_group, workspace
)

my_data = Data(
    path="./nyc_taxi",
    type=AssetTypes.MLTABLE,
    description="A random sample of NYC Green Taxi Data between 2015-19.",
    name="green-quickstart",
    version=VERSION,
)

ml_client.data.create_or_update(my_data)
```
> [!NOTE]
> The path points to the **folder** containing the MLTable artifact.

---

#### Read the data asset in an interactive session

Now that you have your MLTable stored in the cloud, you and team members can access it with a friendly name in an interactive session (for example, a notebook):

```python
import mltable
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential

# connect to the AzureML workspace
# NOTE: the subscription_id, resource_group, workspace variables are set
# in a previous code snippet.
ml_client = MLClient(
    DefaultAzureCredential(), subscription_id, resource_group, workspace
)

# get the latest version of the data asset
# Note: The version was set in the previous snippet. If you changed the version
# number, update the VERSION variable below.
VERSION="1"
data_asset = ml_client.data.get(name="green-quickstart", version=VERSION)

# create a table
tbl = mltable.load(f"azureml:/{data_asset.id}")
tbl.show(5)

# load into pandas
# NOTE: The data is in East US region and the data is large, so this will take several minutes (~7mins) to load if you are in a different region.
df = tbl.to_pandas_dataframe()
```

#### Read the data asset in a job

If you or a team member want to access the Table in a job, your Python training script would contain:

```python
# ./src/train.py
import argparse
import mltable

# parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('--input', help='mltable to read')
args = parser.parse_args()

# load mltable
tbl = mltable.load(args.input)

# load into pandas
df = tbl.to_pandas_dataframe()
```

Your job needs a conda file that includes the Python package dependencies:

```yml
# ./conda_dependencies.yml
dependencies:
  - python=3.10
  - pip=21.2.4
  - pip:
      - mltable
      - azureml-dataprep[pandas]
```

You would submit the job using:

# [CLI](#tab/cli)

Create the following job YAML file:

```yml
# mltable-job.yml
$schema: https://azuremlschemas.azureedge.net/latest/commandJob.schema.json

code: ./src

command: python train.py --input ${{inputs.green}}
inputs:
    green:
      type: mltable
      path: azureml:green-quickstart:1

compute: cpu-cluster

environment:
  image: mcr.microsoft.com/azureml/openmpi4.1.0-ubuntu20.04
  conda_file: conda_dependencies.yml
```

In the CLI, create the job:

```azurecli
az ml job create -f mltable-job.yml
```

# [Python](#tab/Python-SDK)

```python
from azure.ai.ml import MLClient, command, Input
from azure.ai.ml.entities import Environment
from azure.identity import DefaultAzureCredential

# connect to the AzureML workspace
ml_client = MLClient(
    DefaultAzureCredential(), subscription_id, resource_group, workspace
)

# get the latest version of the data asset
# Note: the VERSION was set in a previous cell.
data_asset = ml_client.data.get(name="green-quickstart", version=VERSION)

job = command(
    command="python train.py --input ${{inputs.green}}",
    inputs={"green": Input(type="mltable", path=data_asset.id)},
    compute="cpu-cluster",
    environment=Environment(
        image="mcr.microsoft.com/azureml/openmpi4.1.0-ubuntu20.04",
        conda_file="./job-env/conda_dependencies.yml",
    ),
    code="./src",
)

ml_client.jobs.create_or_update(job)
```

---

## Authoring MLTable Files

To directly create the MLTable file, we suggest that you use the `mltable` Python SDK to author your MLTable files - as shown in the [Azure Machine Learning Tables Quickstart](#azure-machine-learning-tables-quickstart) - instead of a text editor. In this section, we outline the capabilities in the `mltable` Python SDK.

### Supported file types

You can create an MLTable with a range of different file types:

| File Type | `MLTable` Python SDK  |
|---------|---------|
|Delimited Text<br>(for example, CSV files)     |   `from_delimited_files(paths=[path])`     |
|Parquet     |    `from_parquet_files(paths=[path])`     |
|Delta Lake    |   `from_delta_lake(delta_table_uri=<uri_pointing_to_delta_table_directory>,timestamp_as_of='2022-08-26T00:00:00Z')`      |
|JSON Lines     |   `from_json_lines_files(paths=[path])`      |
|Paths<br>(Create a table with a column of paths to stream)     |   `from_paths(paths=[path])`      |

For more information, read the [MLTable reference resource](/python/api/mltable/mltable.mltable.mltable)

### Defining paths

For delimited text, parquet, JSON lines, and paths, define a list of Python dictionaries that defines the path or paths from which to read:

```python
import mltable

# A List of paths to read into the table. The paths are a python dict that define if the path is
# a file, folder, or (glob) pattern.
paths = [
    {
        "file": "<supported_path>"
    }
]

tbl = mltable.from_delimited_files(paths=paths)

# alternatively
# tbl = mltable.from_parquet_files(paths=paths)
# tbl = mltable.from_json_lines_files(paths=paths)
# tbl = mltable.from_paths(paths=paths)
```

MLTable supports these path types:

|Location  | Examples  |
|---------|---------|
|A path on your local computer     | `./home/username/data/my_data`         |
|A path on a public http(s) server    |  `https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2024-01.parquet`    | 
|A path on Azure Storage    |   `wasbs://<container_name>@<account_name>.blob.core.windows.net/<path>` <br> `abfss://<file_system>@<account_name>.dfs.core.windows.net/<path>`    |
|A long-form Azure Machine Learning datastore  |   `azureml://subscriptions/<subid>/resourcegroups/<rgname>/workspaces/<wsname>/datastores/<name>/paths/<path>`      |

> [!NOTE]
> `mltable` handles user credential passthrough for paths on Azure Storage and Azure Machine Learning datastores. If you don't have permission to the data on the underlying storage, you can't access the data.

#### A note on defining paths for Delta Lake Tables

Compared to the other file types, defining paths to read Delta Lake tables is different. For Delta Lake tables, the path points to a *single* folder (typically on ADLS gen2) that contains the "_delta_log" folder and data files. *time travel* is supported. The following code shows how to define a path for a Delta Lake table:

```python
import mltable

# define the cloud path containing the delta table (where the _delta_log file is stored)
delta_table = "abfss://<file_system>@<account_name>.dfs.core.windows.net/<path_to_delta_table>"

# create an MLTable. Note the timestamp_as_of parameter for time travel.
tbl = mltable.from_delta_lake(
    delta_table_uri=delta_table,
    timestamp_as_of='2022-08-26T00:00:00Z'
)
```

To get the latest version of Delta Lake data, you can pass current timestamp into `timestamp_as_of`.

```python
import mltable

# define the relative path containing the delta table (where the _delta_log file is stored)
delta_table_path = "./working-directory/delta-sample-data"

# get the current timestamp in the required format
current_timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
print(current_timestamp)
tbl = mltable.from_delta_lake(delta_table_path, timestamp_as_of=current_timestamp)
df = tbl.to_pandas_dataframe()
```

> [!IMPORTANT]
> **Limitation**: `mltable` doesn't support partition key extraction when reading data from Delta Lake.
> The `mltable` transformation `extract_columns_from_partition_format` won't work when you are reading Delta Lake data via `mltable`.

> [!IMPORTANT]
> `mltable` handles user credential passthrough for paths on Azure Storage and Azure Machine Learning datastores. If you don't have permission to the data on the underlying storage, you can't access the data.

### Files, folders and globs

Azure Machine Learning Tables support reading from:

- file(s), for example: `abfss://<file_system>@<account_name>.dfs.core.windows.net/my-csv.csv`
- folder(s), for example `abfss://<file_system>@<account_name>.dfs.core.windows.net/my-folder/`
- [glob](https://wikipedia.org/wiki/Glob_(programming)) pattern(s), for example `abfss://<file_system>@<account_name>.dfs.core.windows.net/my-folder/*.csv`
- a combination of files, folders, and globbing patterns

### Supported data loading transformations

Find full, up-to-date details of the supported data loading transformations in the [MLTable reference documentation](/python/api/mltable/mltable.mltable.mltable).

## Additional Examples

Examples in the [Azure Machine Learning examples GitHub repo](https://github.com/Azure/azureml-examples/tree/main/sdk/python/using-mltable) became the basis for the code snippets in this article. Use this command to clone the repository to your development environment:

```bash
git clone --depth 1 https://github.com/Azure/azureml-examples
```

> [!TIP]
> Use `--depth 1` to clone only the latest commit to the repository. This reduces the time needed to complete the operation.

This clone repo folder hosts the examples relevant to Azure Machine Learning Tables:

```bash
cd azureml-examples/sdk/python/using-mltable
```
The examples below describe how to work with [delimited text files](#use-delimited-files) and [parquet files.](#use-parquet-files), and how to [Create a data asset](#create-a-data-asset-to-aid-sharing-and-reproducibility).


### Use delimited files

These examples use the popular Titanic dataset (12 variables, 891 rows) used to model survival predictions. First, create an MLTable from a CSV file with this code:

```python
import mltable
from mltable import MLTableHeaders, MLTableFileEncoding, DataType

# create paths to the data files
# Using a public dataset for easier access
paths = [{"file": "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"}]

# create an MLTable from the data files
tbl = mltable.from_delimited_files(
    paths=paths,
    delimiter=",",
    header=MLTableHeaders.all_files_same_headers,
    infer_column_types=True,
    include_path_column=False,
    encoding=MLTableFileEncoding.utf8,
)

# filter out rows undefined ages
tbl = tbl.filter("col('Age') > 0")

# drop PassengerId
tbl = tbl.drop_columns(["PassengerId"])

# ensure survived column is treated as boolean
data_types = {
    "Survived": DataType.to_bool(
        true_values=["True", "true", "1"], false_values=["False", "false", "0"]
    )
}
tbl = tbl.convert_column_types(data_types)

# show the first 5 records
tbl.show(5)

# You can also load into pandas - this dataset is small so it's safe to load
df = tbl.to_pandas_dataframe()
df.head(5)
```

#### Save the data loading steps

Next, save all your data loading steps into an MLTable file. When you save your data loading steps in an MLTable file, you can reproduce your Pandas data frame at a later point in time, without need to redefine the code each time.

```python
# save the data loading steps in an MLTable file
# NOTE: the tbl object was defined in the previous snippet.
tbl.save("./titanic")
```

#### Reproduce data loading steps

Now that file has the serialized data loading steps, you can reproduce them at any point in time with the `load()` method. This way, you don't need to redefine your data loading steps in code, and you can more easily share the file.

```python
import mltable

# load the previously saved MLTable file
tbl = mltable.load("./titanic/")
```

To share this MLTable with team members, you can create a data asset in Azure Machine Learning. See [Create a data asset to aid sharing and reproducibility (1)](#create-a-data-asset-to-aid-sharing-and-reproducibility-1) for details.

### Use parquet files

The [Azure Machine Learning Tables Quickstart](#azure-machine-learning-tables-quickstart) explains how to read parquet files.

### Paths: Create a table of image files 

You can create a table containing the paths on cloud storage. This example has several dog and cat images located in cloud storage, in the following folder structure:

```
/pet-images
  /cat
    0.jpeg
    1.jpeg
    ...
  /dog
    0.jpeg
    1.jpeg
```

The `mltable` can construct a table that contains the storage paths of these images and their folder names (labels), which can be used to stream the images. This code creates the MLTable:

```python
import mltable

# create paths to the data files
paths = [{"pattern": "wasb://data@azuremlexampledata.blob.core.windows.net/pet-images/**/*.jpg"}]

# create the mltable
tbl = mltable.from_paths(paths)

# extract useful information from the path
tbl = tbl.extract_columns_from_partition_format("{account}/{container}/{folder}/{label}")

tbl = tbl.drop_columns(["account", "container", "folder"])

df = tbl.to_pandas_dataframe()
print(df.head())

# save the data loading steps in an MLTable file
tbl.save("./pets")
```

This code shows how to open the storage location in the Pandas data frame, and plot the images:

```python
# plot images on a grid. Note this takes ~1min to execute.
import matplotlib.pyplot as plt
from PIL import Image

fig = plt.figure(figsize=(20, 20))
columns = 4
rows = 5
for i in range(1, columns*rows +1):
    with df.Path[i].open() as f:
        img = Image.open(f)
        fig.add_subplot(rows, columns, i)
        plt.imshow(img)
        plt.title(df.label[i])
```

### Create a data asset to aid sharing and reproducibility

You might have your `mltable` file currently saved on disk, which makes it hard to share with team members. When you create a data asset in Azure Machine Learning, the `mltable` is uploaded to cloud storage and "bookmarked." Your team members can then access the `mltable` with a friendly name. Also, the data asset is versioned.

```python
import time
from azure.ai.ml import MLClient
from azure.ai.ml.entities import Data
from azure.ai.ml.constants import AssetTypes
from azure.identity import DefaultAzureCredential

# set the version number of the data asset to the current UTC time
VERSION = time.strftime("%Y.%m.%d.%H%M%S", time.gmtime())

# connect to the AzureML workspace
# NOTE: subscription_id, resource_group, workspace were set in a previous snippet.
ml_client = MLClient(
    DefaultAzureCredential(), subscription_id, resource_group, workspace
)

my_data = Data(
    path="./pets",
    type=AssetTypes.MLTABLE,
    description="A sample of cat and dog images",
    name="pets-mltable-example",
    version=VERSION,
)

ml_client.data.create_or_update(my_data)
```

Now that the `mltable` is stored in the cloud, you and your team members can access it with a friendly name in an interactive session (for example, a notebook):

```python
import mltable
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential

# connect to the AzureML workspace
# NOTE: subscription_id, resource_group, workspace were set in a previous snippet.
ml_client = MLClient(
    DefaultAzureCredential(), subscription_id, resource_group, workspace
)

# get the latest version of the data asset
# Note: the variable VERSION is set in the previous code
data_asset = ml_client.data.get(name="pets-mltable-example", version=VERSION)

# the table from the data asset id
tbl = mltable.load(f"azureml:/{data_asset.id}")

# load into pandas
df = tbl.to_pandas_dataframe()
df.head()
```

You can also load the data into your job.

## Next steps

- [Access data in a job](how-to-read-write-data-v2.md#access-data-in-a-job)
- [Create and manage data assets](how-to-create-data-assets.md#create-and-manage-data-assets)
- [Import data assets (preview)](how-to-import-data-assets.md#import-data-assets-preview)
- [Data administration](how-to-administrate-data-authentication.md#data-administration)