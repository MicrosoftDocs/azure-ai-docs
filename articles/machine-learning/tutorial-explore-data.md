---
title: "Tutorial: Upload, access, and explore your data"
titleSuffix: Azure Machine Learning
description: Upload data to cloud storage, create an Azure Machine Learning data asset, create new versions for data assets, and use the data for interactive development. 
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: core
ms.topic: tutorial
ms.reviewer: None
author: s-polly
ms.author: scottpolly
ms.date: 08/05/2025
#Customer intent: As a data scientist, I want to know how to prototype and develop machine learning models on a cloud workstation.
---

# Tutorial: Upload, access, and explore your data in Azure Machine Learning

[!INCLUDE [sdk v2](includes/machine-learning-sdk-v2.md)]

In this tutorial, you:

> [!div class="checklist"]
> * Upload your data to cloud storage
> * Create an Azure Machine Learning data asset
> * Access your data in a notebook for interactive development
> * Create new versions of data assets

A machine learning project typically starts with exploratory data analysis (EDA), data preprocessing (cleaning, feature engineering), and building machine learning model prototypes to validate hypotheses. This _prototyping_ project phase is highly interactive and lends itself to development in an IDE or a Jupyter notebook with a _Python interactive console_. This tutorial describes these concepts.

## Prerequisites

1. [!INCLUDE [workspace](includes/prereq-workspace.md)]

1. [!INCLUDE [sign in](includes/prereq-sign-in.md)]

1. [!INCLUDE [open or create  notebook](includes/prereq-open-or-create.md)]
    * [!INCLUDE [new notebook](includes/prereq-new-notebook.md)]
    * Or, open **tutorials/get-started-notebooks/explore-data.ipynb** from the **Samples** section of studio. [!INCLUDE [clone notebook](includes/prereq-clone-notebook.md)]

[!INCLUDE [notebook set kernel](includes/prereq-set-kernel.md)]

<!-- nbstart https://raw.githubusercontent.com/Azure/azureml-examples/main/tutorials/get-started-notebooks/explore-data.ipynb -->

## Download the data used in this tutorial

For data ingestion, Azure Data Explorer handles raw data in [these formats](/azure/data-explorer/ingestion-supported-formats). This tutorial uses a [CSV-format credit card client data sample](https://azuremlexamples.blob.core.windows.net/datasets/credit_card/default_of_credit_card_clients.csv). The steps take place in an Azure Machine Learning resource. In that resource, you create a local folder with the suggested name of **data**, directly under the folder where this notebook is located.

> [!NOTE]
> This tutorial depends on data placed in an Azure Machine Learning resource folder location. For this tutorial, 'local' means a folder location in that Azure Machine Learning resource.

1. Select **Open terminal** below the three dots, as shown in this image:

    :::image type="content" source="media/tutorial-cloud-workstation/open-terminal.png" alt-text="Screenshot shows open terminal tool in notebook toolbar.":::

1. The terminal window opens in a new tab.
1. Make sure you change directory (`cd`) to the same folder where this notebook is located. For example, if the notebook is in a folder named **get-started-notebooks**:

    ```bash
    cd get-started-notebooks    # modify this to the path where your notebook is located
    ```

1. Enter these commands in the terminal window to copy the data to your compute instance:

    ```bash
    mkdir data
    cd data                     # the subfolder where you'll store the data
    wget https://azuremlexamples.blob.core.windows.net/datasets/credit_card/default_of_credit_card_clients.csv
    ```
1. You can now close the terminal window.

For more information about the data in the UC Irvine Machine Learning Repository, visit [this resource](https://archive.ics.uci.edu/ml/datasets/default+of+credit+card+clients).

## Create a handle to the workspace

Before you explore the code, you need a way to reference your workspace. You create `ml_client` as a handle to the workspace. You then use `ml_client` to manage resources and jobs.

In the next cell, enter your Subscription ID, Resource Group name, and Workspace name. To find these values:

1. In the upper right Azure Machine Learning studio toolbar, select your workspace name.
1. Copy the value for workspace, resource group, and subscription ID into the code.
1. You must copy each value individually, one at a time. Close the area, paste the value, then continue to the next one.

```python
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential
from azure.ai.ml.entities import Data
from azure.ai.ml.constants import AssetTypes

# authenticate
credential = DefaultAzureCredential()

# Get a handle to the workspace
ml_client = MLClient(
    credential=credential,
    subscription_id="<SUBSCRIPTION_ID>",
    resource_group_name="<RESOURCE_GROUP>",
    workspace_name="<AML_WORKSPACE_NAME>",
)
```

> [!NOTE]
> Creating MLClient won't connect to the workspace. The client initialization is lazy and waits for the first time it needs to make a call. This happens in the next code cell.

## Upload data to cloud storage

Azure Machine Learning uses Uniform Resource Identifiers (URIs), which point to storage locations in the cloud. A URI makes it easy to access data in notebooks and jobs. Data URI formats are similar to the web URLs that you use in your web browser to access web pages. For example:

* Access data from public https server: `https://<account_name>.blob.core.windows.net/<container_name>/<folder>/<file>`
* Access data from Azure Data Lake Gen 2: `abfss://<file_system>@<account_name>.dfs.core.windows.net/<folder>/<file>`

An Azure Machine Learning data asset is similar to web browser bookmarks (favorites). Instead of remembering long storage paths (URIs) that point to your most frequently used data, you can create a data asset and then access that asset with a friendly name.

Data asset creation also creates a _reference_ to the data source location, along with a copy of its metadata. Because the data remains in its existing location, you incur no extra storage cost and don't risk data source integrity. You can create data assets from Azure Machine Learning datastores, Azure Storage, public URLs, and local files.

> [!TIP]
> For smaller data uploads, Azure Machine Learning data asset creation works well for uploading data from local machine resources to cloud storage. This approach avoids the need for extra tools or utilities. However, larger data uploads might require a dedicated tool or utility - for example, **azcopy**. The azcopy command-line tool moves data to and from Azure Storage. For more information about azcopy, see [Get started with AzCopy](/azure/storage/common/storage-use-azcopy-v10).

The next notebook cell creates the data asset. The code sample uploads the raw data file to the designated cloud storage resource.

Each time you create a data asset, you need a unique version for it. If the version already exists, you get an error. In this code, you use "initial" for the first read of the data. If that version already exists, the code doesn't recreate it.

You can also omit the **version** parameter. In this case, a version number is generated for you, starting with 1 and incrementing from there.

This tutorial uses the name "initial" as the first version. The [Create production machine learning pipelines](tutorial-pipeline-python-sdk.md) tutorial also uses this version of the data, so you use a value that you see again in that tutorial.

```python
from azure.ai.ml.entities import Data
from azure.ai.ml.constants import AssetTypes

# Update the 'my_path' variable to match the location of where you downloaded the data on your
# local filesystem

my_path = "./data/default_of_credit_card_clients.csv"
# Set the version number of the data asset
v1 = "initial"

my_data = Data(
    name="credit-card",
    version=v1,
    description="Credit card data",
    path=my_path,
    type=AssetTypes.URI_FILE,
)

## Create data asset if it doesn't already exist:
try:
    data_asset = ml_client.data.get(name="credit-card", version=v1)
    print(
        f"Data asset already exists. Name: {my_data.name}, version: {my_data.version}"
    )
except:
    ml_client.data.create_or_update(my_data)
    print(f"Data asset created. Name: {my_data.name}, version: {my_data.version}")
```

To examine the uploaded data, select **Data** in the **Assets** section of the left-hand navigation menu. The data is uploaded and a data asset is created:

:::image type="content" source="media/tutorial-explore-data/access-and-explore-data.png" alt-text="Screenshot shows the data in studio.":::

This data is named **credit-card**. In the **Data assets** tab, you can see it in the **Name** column.

An Azure Machine Learning datastore is a *reference* to an *existing* storage account on Azure. A datastore offers these benefits:

1. A common and easy-to-use API to interact with different storage types:
 
    - Azure Data Lake Storage
    - Blob
    - Files

   and authentication methods.
1. An easier way to discover useful datastores when working as a team.
1. In your scripts, a way to hide connection information for credential-based data access (service principal/SAS/key).

## Access your data in a notebook

You want to create data assets for frequently accessed data. You can access the data using the URI as described in [Access data from a datastore URI, like a filesystem](how-to-access-data-interactive.md#access-data-from-a-datastore-uri-like-a-filesystem).  However, as mentioned previously, it can become difficult to remember these URIs. 

 An alternative is to use the `azureml-fsspec` library, which provides a file system interface for Azure Machine Learning datastores. This is an easier way to access the CSV file in Pandas:

> [!IMPORTANT]
> In a notebook cell, execute this code to install the `azureml-fsspec` Python library in your Jupyter kernel:

```python
%pip install -U azureml-fsspec
```

```python
import pandas as pd

# Get a handle of the data asset and print the URI
data_asset = ml_client.data.get(name="credit-card", version=v1)
print(f"Data asset URI: {data_asset.path}")

# Read into pandas - note that you will see 2 headers in your data frame - that is ok, for now

df = pd.read_csv(data_asset.path)
df.head()
```

For more information about data access in a notebook, see [Access data from Azure cloud storage during interactive development](how-to-access-data-interactive.md).

## Create a new version of the data asset

The data needs some light cleaning to make it suitable for training a machine learning model. It has:

* Two headers
* A client ID column that wouldn't be used as a feature in machine learning
* Spaces in the response variable name

Also, compared to the CSV format, the Parquet file format is a better way to store this data. Parquet offers compression and maintains schema. To clean the data and store it in Parquet format:

```python
# Read in data again, this time using the 2nd row as the header
df = pd.read_csv(data_asset.path, header=1)
# Rename column
df.rename(columns={"default payment next month": "default"}, inplace=True)
# Remove ID column
df.drop("ID", axis=1, inplace=True)

# Write file to filesystem
df.to_parquet("./data/cleaned-credit-card.parquet")
```

This table shows the structure of the data in the original **default_of_credit_card_clients.csv** file downloaded in an earlier step. The uploaded data contains 23 explanatory variables and 1 response variable, as shown here:

|Column Name(s) | Variable Type  |Description  |
|---------|---------|---------|
|X1     |   Explanatory      |    Amount of the given credit (NT dollar): it includes both the individual consumer credit and their family (supplementary) credit.    |
|X2     |   Explanatory      |   Gender (1 = male; 2 = female).      |
|X3     |   Explanatory      |   Education (1 = graduate school; 2 = university; 3 = high school; 4 = others).      |
|X4     |   Explanatory      |    Marital status (1 = married; 2 = single; 3 = others).     |
|X5     |   Explanatory      |    Age (years).     |
|X6-X11     | Explanatory        |  History of past payment. Past monthly payment records tracked from April to September 2005. -1 = pay duly; 1 = payment delay for one month; 2 = payment delay for two months; . . .; 8 = payment delay for eight months; 9 = payment delay for nine months and above.      |
|X12-17     | Explanatory        |  Amount of bill statement (NT dollar) from April to September 2005.      |
|X18-23     | Explanatory        |  Amount of previous payment (NT dollar) from April to September 2005.      |
|Y     | Response        |    Default payment (Yes = 1, No = 0)     |

Next, create a new _version_ of the data asset. The data automatically uploads to cloud storage. For this version, add a time value so that each time this code runs, a different version number is created.

```python
from azure.ai.ml.entities import Data
from azure.ai.ml.constants import AssetTypes
import time

# Next, create a new version of the data asset (the data is automatically uploaded to cloud storage):
v2 = "cleaned" + time.strftime("%Y.%m.%d.%H%M%S", time.gmtime())
my_path = "./data/cleaned-credit-card.parquet"

# Define the data asset, and use tags to make it clear the asset can be used in training

my_data = Data(
    name="credit-card",
    version=v2,
    description="Default of credit card clients data.",
    tags={"training_data": "true", "format": "parquet"},
    path=my_path,
    type=AssetTypes.URI_FILE,
)

## Create the data asset

my_data = ml_client.data.create_or_update(my_data)

print(f"Data asset created. Name: {my_data.name}, version: {my_data.version}")
```

The cleaned Parquet file is the latest version data source. This code shows the CSV version result set first, then the Parquet version:

```python
import pandas as pd

# Get a handle of the data asset and print the URI
data_asset_v1 = ml_client.data.get(name="credit-card", version=v1)
data_asset_v2 = ml_client.data.get(name="credit-card", version=v2)

# Print the v1 data
print(f"V1 Data asset URI: {data_asset_v1.path}")
v1df = pd.read_csv(data_asset_v1.path)
print(v1df.head(5))

# Print the v2 data
print(
    "_____________________________________________________________________________________________________________\n"
)
print(f"V2 Data asset URI: {data_asset_v2.path}")
v2df = pd.read_parquet(data_asset_v2.path)
print(v2df.head(5))
```

<!-- nbend -->

## Clean up resources

If you plan to continue now to other tutorials, skip to [Next steps](#next-steps).

### Stop compute instance

If you don't plan to use it now, stop the compute instance:

1. In the studio, in the left pane, select **Compute**.
1. In the top tabs, select **Compute instances.**
1. Select the compute instance in the list.
1. On the top toolbar, select **Stop**.

### Delete all resources

[!INCLUDE [aml-delete-resource-group](includes/aml-delete-resource-group.md)]

## Next steps

For more information about data assets, see [Create data assets](how-to-create-data-assets.md).

For more information about datastores, see [Create datastores](how-to-datastore.md).

Continue with the next tutorial to learn how to develop a training script:

> [!div class="nextstepaction"]
> [Model development on a cloud workstation](tutorial-cloud-workstation.md)
>
