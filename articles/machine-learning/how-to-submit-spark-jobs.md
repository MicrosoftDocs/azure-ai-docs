---
title: Submit Spark jobs in Azure Machine Learning
titleSuffix: Azure Machine Learning
description: Learn how to submit standalone and pipeline Spark jobs in Azure Machine Learning 
author: s-polly
ms.author: scottpolly
ms.reviewer: yogipandey
ms.service: azure-machine-learning
ms.subservice: mldata
ms.topic: how-to 
ms.date: 09/30/2024
ms.custom: template-how-to 
---

# Submit Spark jobs in Azure Machine Learning

[!INCLUDE [dev v2](includes/machine-learning-dev-v2.md)]

Azure Machine Learning supports standalone machine learning job submissions, and creation of [machine learning pipelines](./concept-ml-pipelines.md) that involve multiple machine learning workflow steps. Azure Machine Learning handles both standalone Spark job creation, and creation of reusable Spark components that Azure Machine Learning pipelines can use. In this article, you learn how to submit Spark jobs, with:
- Azure Machine Learning studio UI
- Azure Machine Learning CLI
- Azure Machine Learning SDK

For more information about **Apache Spark in Azure Machine Learning** concepts, visit [this resource](./apache-spark-azure-ml-concepts.md).

## Prerequisites

# [CLI](#tab/cli)
[!INCLUDE [cli v2](includes/machine-learning-cli-v2.md)]
- An Azure subscription; if you don't have an Azure subscription, [create a free account](https://azure.microsoft.com/free) before you begin.
- An Azure Machine Learning workspace. Visit [Create workspace resources](./quickstart-create-resources.md) for more information.
- Create an [Azure Machine Learning compute instance](./concept-compute-instance.md#create).
- Install the [Azure Machine Learning CLI](./how-to-configure-cli.md?tabs=public).
- (Optional): [An attached Synapse Spark pool in the Azure Machine Learning workspace](./how-to-manage-synapse-spark-pool.md).

# [Python SDK](#tab/sdk)
[!INCLUDE [sdk v2](includes/machine-learning-sdk-v2.md)]
- An Azure subscription; if you don't have an Azure subscription, [create a free account](https://azure.microsoft.com/free) before you begin.
- An Azure Machine Learning workspace. Visit [Create workspace resources](./quickstart-create-resources.md) for more information.
- [Configure your development environment](./how-to-configure-environment.md), or [create an Azure Machine Learning compute instance](./concept-compute-instance.md#create).
- Install the [Azure Machine Learning SDK for Python](/python/api/overview/azure/ai-ml-readme).
- (Optional): [An attached Synapse Spark pool in the Azure Machine Learning workspace](./how-to-manage-synapse-spark-pool.md).

# [Studio UI](#tab/ui)
These prerequisites cover the submission of a Spark job from Azure Machine Learning studio UI:
- An Azure subscription; if you don't have an Azure subscription, [create a free account](https://azure.microsoft.com/free) before you begin.
- An Azure Machine Learning workspace. Visit [Create workspace resources](./quickstart-create-resources.md) for more information.
- (Optional): [An attached Synapse Spark pool in the Azure Machine Learning workspace](./how-to-manage-synapse-spark-pool.md).

---

> [!NOTE]
> - For more information about resource access while using Azure Machine Learning serverless Spark compute and attached Synapse Spark pool, visit [Ensuring resource access for Spark jobs](apache-spark-environment-configuration.md#ensuring-resource-access-for-spark-jobs).
> - Azure Machine Learning provides a [shared quota](how-to-manage-quotas.md#azure-machine-learning-shared-quota) pool, from which all users can access compute quota to perform testing for a limited time. When you use the serverless Spark compute, Azure Machine Learning allows you to access this shared quota for a short time.

### Attach user assigned managed identity using CLI v2

1. Create a YAML file that defines the user-assigned managed identity that should be attached to the workspace:
    ```yaml
    identity:
      type: system_assigned,user_assigned
      tenant_id: <TENANT_ID>
      user_assigned_identities:
        '/subscriptions/<SUBSCRIPTION_ID/resourceGroups/<RESOURCE_GROUP>/providers/Microsoft.ManagedIdentity/userAssignedIdentities/<AML_USER_MANAGED_ID>':
          {}
    ```
1. With the `--file` parameter, use the YAML file in the `az ml workspace update` command to attach the user assigned managed identity:
    ```azurecli
    az ml workspace update --subscription <SUBSCRIPTION_ID> --resource-group <RESOURCE_GROUP> --name <AML_WORKSPACE_NAME> --file <YAML_FILE_NAME>.yaml
    ```

### Attach user assigned managed identity using `ARMClient`

1. Install [`ARMClient`](https://github.com/projectkudu/ARMClient), a simple command line tool that invokes the Azure Resource Manager API.
1. Create a JSON file that defines the user-assigned managed identity that should be attached to the workspace:
    ```json
    {
        "properties":{
        },
        "location": "<AZURE_REGION>",
        "identity":{
            "type":"SystemAssigned,UserAssigned",
            "userAssignedIdentities":{
                "/subscriptions/<SUBSCRIPTION_ID/resourceGroups/<RESOURCE_GROUP>/providers/Microsoft.ManagedIdentity/userAssignedIdentities/<AML_USER_MANAGED_ID>": { }
            }
        }
    }
    ```
1. To attach the user-assigned managed identity to the workspace, execute the following command in the PowerShell prompt or the command prompt.
    ```cmd
    armclient PATCH https://management.azure.com/subscriptions/<SUBSCRIPTION_ID>/resourceGroups/<RESOURCE_GROUP>/providers/Microsoft.MachineLearningServices/workspaces/<AML_WORKSPACE_NAME>?api-version=2022-05-01 '@<JSON_FILE_NAME>.json'
    ```

> [!NOTE]
> - To ensure successful execution of the Spark job, assign the **Contributor** and **Storage Blob Data Contributor** roles, on the Azure storage account used for data input and output, to the identity that the Spark job uses
> - Public Network Access should be enabled in Azure Synapse workspace to ensure successful execution of the Spark job using an [attached Synapse Spark pool](./how-to-manage-synapse-spark-pool.md).
> - In an Azure Synapse workspace that has a managed virtual network associated with it, if an [attached Synapse Spark pool](./how-to-manage-synapse-spark-pool.md) points to a Synapse Spark pool, you should [configure](/azure/synapse-analytics/security/connect-to-a-secure-storage-account) a managed private endpoint to storage account, to ensure data access.
> - Serverless Spark compute supports Azure Machine Learning managed virtual network. If a managed network is provisioned for the serverless Spark compute, the corresponding private endpoints for the storage account [should also be provisioned](./how-to-managed-network.md#configure-for-serverless-spark-jobs) to ensure data access.

## Submit a standalone Spark job
After you make the necessary changes for Python script parameterization, you can use a Python script developed with [interactive data wrangling](./interactive-data-wrangling-with-apache-spark-azure-ml.md) to submit a batch job, to process a larger volume of data. You can submit a data wrangling batch job as a standalone Spark job.

A Spark job requires a Python script that takes arguments. You can modify the Python code originally developed from [interactive data wrangling](./interactive-data-wrangling-with-apache-spark-azure-ml.md) to develop that script. A sample Python script is shown here.

```python
# titanic.py
import argparse
from operator import add
import pyspark.pandas as pd
from pyspark.ml.feature import Imputer

parser = argparse.ArgumentParser()
parser.add_argument("--titanic_data")
parser.add_argument("--wrangled_data")

args = parser.parse_args()
print(args.wrangled_data)
print(args.titanic_data)

df = pd.read_csv(args.titanic_data, index_col="PassengerId")
imputer = Imputer(inputCols=["Age"], outputCol="Age").setStrategy(
    "mean"
)  # Replace missing values in Age column with the mean value
df.fillna(
    value={"Cabin": "None"}, inplace=True
)  # Fill Cabin column with value "None" if missing
df.dropna(inplace=True)  # Drop the rows which still have any missing value
df.to_csv(args.wrangled_data, index_col="PassengerId")
```

> [!NOTE]
> This Python code sample uses `pyspark.pandas`. Only the Spark runtime version 3.2 or later supports this.

This script takes two arguments, which pass the path of input data and output folder, respectively:

- `--titanic_data`
- `--wrangled_data`

# [Azure CLI](#tab/cli)
[!INCLUDE [cli v2](includes/machine-learning-cli-v2.md)]

To create a job, you can define a standalone Spark job as a YAML specification file, which you can use in the `az ml job create` command, with the `--file` parameter. Define these properties in the YAML file:

### YAML properties in the Spark job specification

- `type` - set to `spark`.
- `code` - defines the location of the folder that contains source code and scripts for this job.
- `entry` - defines the entry point for the job. It should cover one of these properties:
  - `file` - defines the name of the Python script that serves as an entry point for the job.
  - `class_name` - defines the name of the class that servers as an entry point for the job.
- `py_files` - defines a list of `.zip`, `.egg`, or `.py` files, to be placed in the `PYTHONPATH`, for successful execution of the job. This property is optional.
- `jars` - defines a list of `.jar` files to include on the Spark driver, and the executor `CLASSPATH`, for successful execution of the job. This property is optional.
- `files` - defines a list of files that should be copied to the working directory of each executor, for successful job execution. This property is optional.
- `archives` - defines a list of archives that should be extracted into the working directory of each executor, for successful job execution. This property is optional.
- `conf` - defines these Spark driver and executor properties:
  - `spark.driver.cores`: the number of cores for the Spark driver.
  - `spark.driver.memory`: allocated memory for the Spark driver, in gigabytes (GB).
  - `spark.executor.cores`: the number of cores for the Spark executor.
  - `spark.executor.memory`: the memory allocation for the Spark executor, in gigabytes (GB).
  - `spark.dynamicAllocation.enabled` - whether or not executors should be dynamically allocated, as a `True` or `False` value.
  -   If dynamic allocation of executors is enabled, define these properties:
      - `spark.dynamicAllocation.minExecutors` - the minimum number of Spark executors instances, for dynamic allocation.
      - `spark.dynamicAllocation.maxExecutors` - the maximum number of Spark executors instances, for dynamic allocation.
  -   If dynamic allocation of executors is disabled, define this property:
      - `spark.executor.instances` - the number of Spark executor instances.
- `environment` - an [Azure Machine Learning environment](./reference-yaml-environment.md) to run the job.
- `args` - the command line arguments that should be passed to the job entry point Python script. Review the YAML specification file provided here for an example.
- `resources` - this property defines the resources to be used by an Azure Machine Learning serverless Spark compute. It uses the following properties:
  - `instance_type` - the compute instance type to be used for Spark pool. The following instance types are currently supported:
    - `standard_e4s_v3`
    - `standard_e8s_v3`
    - `standard_e16s_v3`
    - `standard_e32s_v3`
    - `standard_e64s_v3`
  - `runtime_version` - defines the Spark runtime version. The following Spark runtime versions are currently supported:
    - `3.3`
    - `3.4`
      > [!IMPORTANT]
      > Azure Synapse Runtime for Apache Spark: Announcements
      > * Azure Synapse Runtime for Apache Spark 3.3:
      >   * EOLA Announcement Date: July 12, 2024
      >   * End of Support Date: March 31, 2025. After this date, the runtime will be disabled.
      > * For continued support and optimal performance, we advise migrating to Apache Spark 3.4.

  This is an example YAML file:
  ```yaml
  resources:
    instance_type: standard_e8s_v3
    runtime_version: "3.4"
  ```
- `compute` - this property defines the name of an attached Synapse Spark pool, as shown in this example:
  ```yaml
  compute: mysparkpool
  ```
- `inputs` - this property defines inputs for the Spark job. Inputs for a Spark job can be either a literal value, or data stored in a file or folder.
  - A **literal value** can be a number, a boolean value, or a string. Some examples are shown here:
      ```yaml
      inputs:
        sampling_rate: 0.02 # a number
        hello_number: 42 # an integer
        hello_string: "Hello world" # a string
        hello_boolean: True # a boolean value
      ```
  - **Data** stored in a file or folder should be defined using these properties:
    - `type` - set this property to `uri_file`, or `uri_folder`, for input data contained in a file or a folder respectively.
    - `path` - the URI of the input data, such as `azureml://`, `abfss://`, or `wasbs://`.
    - `mode` - set this property to `direct`.
      This sample shows the definition of a job input, which can be referred to as `$${inputs.titanic_data}}`:
      ```YAML
      inputs:
        titanic_data:
          type: uri_file
          path: azureml://datastores/workspaceblobstore/paths/data/titanic.csv
          mode: direct
      ```
- `outputs` - this property defines the Spark job outputs. Outputs for a Spark job can be written to either a file or a folder location, which is defined using the following three properties:
  - `type` - you can set this property to `uri_file` or `uri_folder`, to write output data to a file or a folder respectively.
  - `path` - this property defines the output location URI, such as `azureml://`, `abfss://`, or `wasbs://`.
  - `mode` - set this property to `direct`.
    This sample shows the definition of a job output, which you can refer to as `${{outputs.wrangled_data}}`:
    ```YAML
    outputs:
      wrangled_data:
        type: uri_folder
        path: azureml://datastores/workspaceblobstore/paths/data/wrangled/
        mode: direct
    ```
- `identity` - this optional property defines the identity used to submit this job. It can have `user_identity` and `managed` values. If the YAML specification doesn't define an identity, the Spark job uses the default identity.

### Standalone Spark job

This example YAML specification shows a standalone Spark job. It uses an Azure Machine Learning serverless Spark compute:

```yaml
$schema: http://azureml/sdk-2-0/SparkJob.json
type: spark

code: ./ 
entry:
  file: titanic.py

conf:
  spark.driver.cores: 1
  spark.driver.memory: 2g
  spark.executor.cores: 2
  spark.executor.memory: 2g
  spark.executor.instances: 2

inputs:
  titanic_data:
    type: uri_file
    path: azureml://datastores/workspaceblobstore/paths/data/titanic.csv
    mode: direct

outputs:
  wrangled_data:
    type: uri_folder
    path: azureml://datastores/workspaceblobstore/paths/data/wrangled/
    mode: direct

args: >-
  --titanic_data ${{inputs.titanic_data}}
  --wrangled_data ${{outputs.wrangled_data}}

identity:
  type: user_identity

resources:
  instance_type: standard_e4s_v3
  runtime_version: "3.4"
```

> [!NOTE]
> To use an attached Synapse Spark pool, define the `compute` property in the sample YAML specification file shown earlier, instead of the `resources` property.

You can use the YAML files shown earlier in the `az ml job create` command, with the `--file` parameter, to create a standalone Spark job as shown:

```azurecli
az ml job create --file <YAML_SPECIFICATION_FILE_NAME>.yaml --subscription <SUBSCRIPTION_ID> --resource-group <RESOURCE_GROUP> --workspace-name <AML_WORKSPACE_NAME>
```

You can execute the above command from:
- [terminal of an Azure Machine Learning compute instance](how-to-access-terminal.md#access-a-terminal).
- a Visual Studio Code terminal, [connected](./how-to-set-up-vs-code-remote.md?tabs=studio) to an Azure Machine Learning compute instance.
- your local computer that has [Azure Machine Learning CLI](./how-to-configure-cli.md?tabs=public) installed.

# [Python SDK](#tab/sdk)
[!INCLUDE [sdk v2](includes/machine-learning-sdk-v2.md)]

### Standalone Spark job using Python SDK 
To create a standalone Spark job, use the `azure.ai.ml.spark` function, with these parameters:
- `name` - the name of the Spark job.
- `display_name` - the display name of the Spark job that should be displayed in the UI and elsewhere.
- `code` - the location of the folder that contains the source code and scripts for this job.
- `entry` - the entry point for the job. It should be a dictionary that defines the file entry point.
- `py_files` - a list of `.zip`, `.egg`, or `.py` files to be placed in the `PYTHONPATH`, for successful execution of the job. This parameter is optional.
- `jars` - a list of `.jar` files to include in the Spark driver and executor `CLASSPATH`, for successful execution of the job. This parameter is optional.
- `files` - a list of files that should be copied to the working directory of each executor, for successful execution of the job. This parameter is optional.
- `archives` - a list of archives that is automatically extracted and placed in the working directory of each executor, for successful execution of the job. This parameter is optional.
- `conf` - a dictionary with predefined Spark configuration key-value pairs.
- `driver_cores`: the number of cores allocated for the Spark driver.
- `driver_memory`: the allocated memory for the Spark driver, with a size unit suffix `k`, `m`, `g`, or `t` (for example, `512m`, `2g`).
- `executor_cores`: the number of cores allocated for the Spark executor.
- `executor_memory`: the allocated memory for the Spark executor, with a size unit suffix `k`, `m`, `g`, or `t` (for example, `512m`, `2g`).
- `dynamic_allocation_enabled` - a boolean parameter that defines whether or not executors should be allocated dynamically.
  - If dynamic allocation of executors is enabled, then define these parameters:
    - `dynamic_allocation_min_executors` - the minimum number of Spark executors instances for dynamic allocation.
    - `dynamic_allocation_max_executors` - the maximum number of Spark executors instances for dynamic allocation.
  - If dynamic allocation of executors is disabled, then define these parameters:
    - `executor_instances` - the number of Spark executor instances.
    - `environment` - the Azure Machine Learning environment that runs the job. This parameter should pass:
      - an object of `azure.ai.ml.entities.Environment`, or an Azure Machine Learning environment name (string).
- `args` - the command line arguments that should be passed to the job entry point Python script. See the sample code provided here for an example.
- `resources` - the resources to be used by an Azure Machine Learning serverless Spark compute. This parameter should pass a dictionary with:
  - `instance_type` - a key that defines the compute instance type to be used for the serverless Spark compute. The following instance types are currently supported:
    - `Standard_E4S_V3`
    - `Standard_E8S_V3`
    - `Standard_E16S_V3`
    - `Standard_E32S_V3`
    - `Standard_E64S_V3`
  - `runtime_version` - a key that defines the Spark runtime version. The following Spark runtime versions are currently supported:
    - `3.3.0`
    - `3.4.0`
      > [!IMPORTANT]
      > Azure Synapse Runtime for Apache Spark: Announcements
      > * Azure Synapse Runtime for Apache Spark 3.3:
      >   * EOLA Announcement Date: July 12, 2024
      >   * End of Support Date: March 31, 2025. After this date, the runtime will be disabled.
      > * For continued support and optimal performance, we advise migrating to Apache Spark 3.4.

- `compute` - the name of an attached Synapse Spark pool.
- `inputs` - the inputs for the Spark job. This parameter should pass a dictionary with mappings of the input data bindings used in the job. This dictionary has these values:
  - a dictionary key defines the input name
  - a corresponding value might be:
    - a literal value: integer, number, boolean, or string.
    - an object of class `azure.ai.ml.Input`, with the following parameters:
      - `type` - set this parameter to `uri_file` or `uri_folder`, for input data contained in a file or a folder respectively.
      - `path` - the URI of the input data, such as `azureml://`, `abfss://`, or `wasbs://`.
      - `mode` - set this parameter to `direct`.
- `outputs` - the outputs for the Spark job. This parameter should pass a dictionary with mappings of the output data bindings used in the job. This dictionary has these values:
  - a dictionary key defines the output name
  - a corresponding value is an object of class `azure.ai.ml.Output`, with the following parameters:
    - `type` - set this parameter to `uri_file` or `uri_folder`, for an output data file or a folder respectively.
    - `path` - the URI of the output data, such as `azureml://`, `abfss://`, or `wasbs://`.
    - `mode` - set this parameter to `direct`.
- `identity` - an optional parameter that defines the identity used for submission of this job. Allowed values are an object of class
  - `azure.ai.ml.entities.UserIdentityConfiguration`
  or
  - `azure.ai.ml.entities.ManagedIdentityConfiguration`
  for user identity and managed identity respectively. If no identity is defined, the Spark job uses the default identity.

You can submit a standalone Spark job from:
- an Azure Machine Learning Notebook connected to an Azure Machine Learning compute instance. 
- [Visual Studio Code connected to an Azure Machine Learning compute instance](./how-to-set-up-vs-code-remote.md?tabs=studio).
- your local computer that has [the Azure Machine Learning SDK for Python](/python/api/overview/azure/ai-ml-readme) installed.

This Python code snippet shows the creation of a standalone Spark job, with an Azure Machine Learning serverless Spark compute, using user identity.

```python
from azure.ai.ml import MLClient, spark, Input, Output
from azure.identity import DefaultAzureCredential
from azure.ai.ml.entities import UserIdentityConfiguration

subscription_id = "<SUBSCRIPTION_ID>"
resource_group = "<RESOURCE_GROUP>"
workspace_name = "<AML_WORKSPACE_NAME>"
ml_client = MLClient(
    DefaultAzureCredential(), subscription_id, resource_group, workspace_name
)

spark_job = spark(
    display_name="Titanic-Spark-Job-SDK",
    code="./src",
    entry={"file": "titanic.py"},
    driver_cores=1,
    driver_memory="2g",
    executor_cores=2,
    executor_memory="2g",
    executor_instances=2,
    resources={
        "instance_type": "Standard_E8S_V3",
        "runtime_version": "3.4.0",
    },
    inputs={
        "titanic_data": Input(
            type="uri_file",
            path="azureml://datastores/workspaceblobstore/paths/data/titanic.csv",
            mode="direct",
        ),
    },
    outputs={
        "wrangled_data": Output(
            type="uri_folder",
            path="azureml://datastores/workspaceblobstore/paths/data/wrangled/",
            mode="direct",
        ),
    },
    identity=UserIdentityConfiguration(),
    args="--titanic_data ${{inputs.titanic_data}} --wrangled_data ${{outputs.wrangled_data}}",
)

returned_spark_job = ml_client.jobs.create_or_update(spark_job)

# Wait until the job completes
ml_client.jobs.stream(returned_spark_job.name)
```

> [!NOTE]
> To use an attached Synapse Spark pool, define the `compute` parameter in the `azure.ai.ml.spark` function, instead of `resources`.

# [Studio UI](#tab/ui)

### Submit a standalone Spark job from Azure Machine Learning studio UI (preview)

[!INCLUDE [machine-learning-preview-generic-disclaimer](includes/machine-learning-preview-generic-disclaimer.md)]

To submit a standalone Spark job using the Azure Machine Learning studio UI:

:::image type="content" source="media/how-to-submit-spark-jobs/create-standalone-spark-job.png" alt-text="Screenshot showing creation of a new Spark job in Azure Machine Learning studio UI.":::

- Near the top right side of the screen, select **+ New**.
- Select **Spark job (preview)**.
- On the **Compute** screen:

:::image type="content" source="media/how-to-submit-spark-jobs/create-standalone-spark-job-compute.png" alt-text="Screenshot that shows the compute selection screen for a new Spark job in Azure Machine Learning studio UI.":::

1. Under **Select compute type**, select **Spark serverless** for serverless Spark compute, or **Attached compute** for an attached Synapse Spark pool.
1. If you selected **Spark serverless**:
   1. Select **Virtual machine size**.
   1. Select **Spark runtime version**.
      > [!IMPORTANT]
      > Azure Synapse Runtime for Apache Spark: Announcements
      > * Azure Synapse Runtime for Apache Spark 3.3:
      >   * EOLA Announcement Date: July 12, 2024
      >   * End of Support Date: March 31, 2025. After this date, the runtime will be disabled.
      > * For continued support and optimal performance, we advise migrating to Apache Spark 3.4.

1. If you selected **Attached compute**:
   1. Select an attached Synapse Spark pool from the **Select Azure Machine Learning attached compute** menu.
1. Select **Next**.
1. On the **Environment** screen:
   1. Select one of the available environments from the list. Environment selection is optional.
   1. Select **Next**.
1. On the **Job settings** screen:
   1. Provide a job **Name**. You can use the job **Name**, which is generated by default.
   1. Select **Experiment name** from the dropdown menu.
   1. Under **Add tags**, provide **Name** and **Value**, then select **Add**. Adding tags is optional.
   1. Under the **Code** section:
      1. Select an option from **Choose code location** dropdown. Choose **Upload local file** or **Azure Machine Learning workspace default blob storage**.
      1. If you selected **Choose code location**:
         - Select **Browse**, and navigate to the location containing the code file or files on your local machine.
      1. If you selected **Azure Machine Learning workspace default blob storage**:
         1. Under **Path to code file to upload**, select **Browse**.
         1. In the pop-up screen titled **Path selection**, select the path of code files on the workspace default blob storage.
         1. Select **Save**.
      1. Input the name of **Entry file** for the standalone job. This file should contain the Python code that takes arguments.
      1. To add any other Python file or files that the standalone job requires at runtime, select **+ Add file** under **Py files** and input the name of the `.zip`, `.egg`, or `.py` file to be placed in the `PYTHONPATH` for successful job execution. Multiple files can be added.
      1. To add any Jar file or files that the standalone job requires at runtime, select **+ Add file** under **Jars** and input the name of the `.jar` file to be included in the Spark driver. Also, add the executor `CLASSPATH` for successful job execution. Multiple files can be added.
      1. To add an archive or archives that should be extracted into the working directory of each executor for successful job execution, select **+ Add file** under **Archives**, and input the name of the archive. Multiple archives can be added.
      1. Adding **Py files**, **Jars**, and **Archives** is optional.
      1. To add an input, select **+ Add input** under **Inputs** and
         1. Enter an **Input name**. The input should refer to this name later in the **Arguments**.
         1. Select an **Input type**.
         1. For type **Data**:
            1. Select **Data type** as **File** or **Folder**.
            1. Select **Data source** as **Upload from local**, **URI**, or **Datastore**.
               - For **Upload from local**, select **Browse** under **Path to upload**, to choose the input file or folder.
               - For **URI**, enter a storage data URI (for example, `abfss://` or `wasbs://` URI), or enter a data asset `azureml://`.
               - For **Datastore**:
                 1. **Select a datastore** from the dropdown menu.
                 1. Under **Path to data**, select **Browse**.
                 1. In the pop-up screen titled **Path selection**, select the path of the code files on the workspace default blob storage.
                 1. Select **Save**.
            1. For type **Integer**, enter an integer value as **Input value**.
            1. For type **Number**, enter a numeric value as **Input value**.
            1. For type **Boolean**, select **True** or **False** as **Input value**.
            1. For type **String**, enter a string as **Input value**.
         1. To add an input, select **+ Add output** under **Outputs** and
            1. Enter an **Output name**. The output should refer to this name later to in the **Arguments**.
            1. Select **Output type** as **File** or **Folder**.
            1. For **Output URI destination**, enter a storage data URI (for example, `abfss://` or `wasbs://` URI) or enter a data asset `azureml://`.
         1. Enter **Arguments** by using the names defined in the **Input name** and **Output name** fields in the earlier steps, and the names of input and output arguments used in the Python script **Entry file**. For example, if the **Input name** and **Output name** are defined as `job_input` and `job_output`, and the arguments are added in the **Entry file** as shown here

            ``` python
            import argparse

            parser = argparse.ArgumentParser()
            parser.add_argument("--input_param")
            parser.add_argument("--output_param")
            ```
         then enter **Arguments** as `--input_param ${{inputs.job_input}} --output_param ${{outputs.job_output}}`.
         1. Under the **Spark configurations** section:
            1. For **Executor size**:
               1. Enter the number of executor **Cores** and executor **Memory (GB)**, in gigabytes.
               1. For **Dynamically allocated executors**, select the **Disabled** or **Enabled** option.
                  - If dynamic allocation of executors is **Disabled**, enter the number of **Executor instances**.
                  - If dynamic allocation of executors is **Enabled**, use the slider to select the minimum and maximum number of executors.
            1. For **Driver size**:
               1. Enter the number of driver **Cores** and driver **Memory (GB)**, in gigabytes.
               1. Enter the **Name** and **Value** pairs for any **Additional configurations**, then select **Add**. You can optionally provide **Additional configurations**.
            1. Select **Next**.
      1. On the **Review** screen:
         1. Review the job specification before you submit it.
         1. Select **Create** to submit the standalone Spark job.
---

## Spark component in a pipeline job

A Spark component offers the flexibility to use the same component in multiple [Azure Machine Learning pipelines](./concept-ml-pipelines.md), as a pipeline step.

# [Azure CLI](#tab/cli)
[!INCLUDE [cli v2](includes/machine-learning-cli-v2.md)]

The YAML syntax for a Spark component resembles the [YAML syntax for Spark job specification](#yaml-properties-in-the-spark-job-specification) in most ways. These properties are defined differently in the Spark component YAML specification:
- `name` - the name of the Spark component.
- `version` - the version of the Spark component.
- `display_name` - the name of the Spark component to display in the UI and elsewhere.
- `description` - the description of the Spark component.
- `inputs` - this property resembles the `inputs` property described in [YAML syntax for Spark job specification](#yaml-properties-in-the-spark-job-specification), except that it doesn't define the `path` property. This code snippet shows an example of the Spark component `inputs` property:

  ```yaml
  inputs:
    titanic_data:
      type: uri_file
      mode: direct
  ```

- `outputs` - this property resembles the `outputs` property described in [YAML syntax for Spark job specification](#yaml-properties-in-the-spark-job-specification), except that it doesn't define the `path` property. This code snippet shows an example of the Spark component `outputs` property:

  ```yaml
  outputs:
    wrangled_data:
      type: uri_folder
      mode: direct
  ```

> [!NOTE]
> A Spark component does not define the `identity`, `compute` or `resources` properties. The pipeline YAML specification file defines these properties.

This YAML specification file provides an example of a Spark component:

```yaml
$schema: http://azureml/sdk-2-0/SparkComponent.json
name: titanic_spark_component
type: spark
version: 1
display_name: Titanic-Spark-Component
description: Spark component for Titanic data

code: ./src
entry:
  file: titanic.py

inputs:
  titanic_data:
    type: uri_file
    mode: direct

outputs:
  wrangled_data:
    type: uri_folder
    mode: direct

args: >-
  --titanic_data ${{inputs.titanic_data}}
  --wrangled_data ${{outputs.wrangled_data}}

conf:
  spark.driver.cores: 1
  spark.driver.memory: 2g
  spark.executor.cores: 2
  spark.executor.memory: 2g
  spark.dynamicAllocation.enabled: True
  spark.dynamicAllocation.minExecutors: 1
  spark.dynamicAllocation.maxExecutors: 4
```

You can use The Spark component defined in the above YAML specification file in an Azure Machine Learning pipeline job. Visit the [pipeline job YAML schema](./reference-yaml-job-pipeline.md) resource to learn more about the YAML syntax that defines a pipeline job. This example shows a YAML specification file for a pipeline job, with a Spark component, and an Azure Machine Learning serverless Spark compute:

```yaml
$schema: http://azureml/sdk-2-0/PipelineJob.json
type: pipeline
display_name: Titanic-Spark-CLI-Pipeline
description: Spark component for Titanic data in Pipeline

jobs:
  spark_job:
    type: spark
    component: ./spark-job-component.yaml
    inputs:
      titanic_data: 
        type: uri_file
        path: azureml://datastores/workspaceblobstore/paths/data/titanic.csv
        mode: direct

    outputs:
      wrangled_data:
        type: uri_folder
        path: azureml://datastores/workspaceblobstore/paths/data/wrangled/
        mode: direct

    identity:
      type: managed

    resources:
      instance_type: standard_e8s_v3
      runtime_version: "3.4"
```
> [!NOTE]
> To use an attached Synapse Spark pool, define the `compute` property in the sample YAML specification file shown above, instead of `resources` property.

You can use the YAML specification file seen above in the `az ml job create` command, using the `--file` parameter, to create a pipeline job as shown:

```azurecli
az ml job create --file <YAML_SPECIFICATION_FILE_NAME>.yaml --subscription <SUBSCRIPTION_ID> --resource-group <RESOURCE_GROUP> --workspace-name <AML_WORKSPACE_NAME>
```

You can execute the above command from:
- the [terminal](how-to-access-terminal.md#access-a-terminal) of an Azure Machine Learning compute instance. 
- the [terminal](./how-to-set-up-vs-code-remote.md?tabs=studio) of Visual Studio Code connected to an Azure Machine Learning compute instance.
- your local computer that has [Azure Machine Learning CLI](./how-to-configure-cli.md?tabs=public) installed.

# [Python SDK](#tab/sdk)
[!INCLUDE [sdk v2](includes/machine-learning-sdk-v2.md)]

Creation of an Azure Machine Learning pipeline with a Spark component involves the creation of [Azure Machine Learning pipelines from components, using Python SDK](./tutorial-pipeline-python-sdk.md#create-the-pipeline-from-components). A Spark component is created using `azure.ai.ml.spark` function. The function parameters are defined almost the same way as for the [standalone Spark job](#standalone-spark-job-using-python-sdk). These parameters are defined differently for the Spark component:

- `name` - the name of the Spark component.
- `display_name` - the name of the Spark component displayed in the UI and elsewhere.
- `inputs` - this parameter resembles the `inputs` parameter described for the [standalone Spark job](#standalone-spark-job-using-python-sdk), except that the `azure.ai.ml.Input` class is instantiated without the `path` parameter.
- `outputs` - this parameter resembles the `outputs` parameter described for the [standalone Spark job](#standalone-spark-job-using-python-sdk), except that the `azure.ai.ml.Output` class is instantiated without the `path` parameter.

> [!NOTE]
> A Spark component created using `azure.ai.ml.spark` function does not define the `identity`,  `compute` or `resources` parameters. The Azure Machine Learning pipeline defines these parameters.

You can submit a pipeline job with a Spark component from:
- an Azure Machine Learning Notebook connected to an Azure Machine Learning compute instance. 
- Visual Studio Code [connected](./how-to-set-up-vs-code-remote.md?tabs=studio) to an Azure Machine Learning compute instance.
- your local computer that has [the Azure Machine Learning SDK for Python](/python/api/overview/azure/ai-ml-readme) installed.

This Python code snippet shows use of a managed identity, together with the creation of an Azure Machine Learning pipeline job. Additionally, it shows use of a Spark component and an Azure Machine Learning Managed (Automatic) Synapse compute:

```python
from azure.ai.ml import MLClient, dsl, spark, Input, Output
from azure.identity import DefaultAzureCredential
from azure.ai.ml.entities import ManagedIdentityConfiguration
from azure.ai.ml.constants import InputOutputModes

subscription_id = "<SUBSCRIPTION_ID>"
resource_group = "<RESOURCE_GROUP>"
workspace_name = "<AML_WORKSPACE_NAME>"
ml_client = MLClient(
    DefaultAzureCredential(), subscription_id, resource_group, workspace_name
)

spark_component = spark(
    name="Spark Component",
    inputs={
        "titanic_data": Input(type="uri_file", mode="direct"),
    },
    outputs={
        "wrangled_data": Output(type="uri_folder", mode="direct"),
    },
    # The source folder of the component
    code="./src",
    entry={"file": "titanic.py"},
    driver_cores=1,
    driver_memory="2g",
    executor_cores=2,
    executor_memory="2g",
    executor_instances=2,
    args="--titanic_data ${{inputs.titanic_data}} --wrangled_data ${{outputs.wrangled_data}}",
)


@dsl.pipeline(
    description="Sample Pipeline with Spark component",
)
def spark_pipeline(spark_input_data):
    spark_step = spark_component(titanic_data=spark_input_data)
    spark_step.inputs.titanic_data.mode = InputOutputModes.DIRECT
    spark_step.outputs.wrangled_data = Output(
        type="uri_folder",
        path="azureml://datastores/workspaceblobstore/paths/data/wrangled/",
    )
    spark_step.outputs.wrangled_data.mode = InputOutputModes.DIRECT
    spark_step.identity = ManagedIdentityConfiguration()
    spark_step.resources = {
        "instance_type": "Standard_E8S_V3",
        "runtime_version": "3.4.0",
    }

pipeline = spark_pipeline(
    spark_input_data=Input(
        type="uri_file",
        path="azureml://datastores/workspaceblobstore/paths/data/titanic.csv",
    )
)

pipeline_job = ml_client.jobs.create_or_update(
    pipeline,
    experiment_name="Titanic-Spark-Pipeline-SDK",
)

# Wait until the job completes
ml_client.jobs.stream(pipeline_job.name)
```

> [!NOTE]
> To use an attached Synapse Spark pool, define the `compute` parameter in the `azure.ai.ml.spark` function, instead of the `resources` parameter. For example, in the code sample shown above, define `spark_step.compute = "<ATTACHED_SPARK_POOL_NAME>"` instead of defining `spark_step.resources`.

# [Studio UI](#tab/ui)
This functionality isn't available in the Studio UI. The Studio UI doesn't support this feature.

---

## Troubleshooting Spark jobs
To troubleshoot a Spark job, you can access the logs generated for that job in Azure Machine Learning studio. To view the logs for a Spark job:
1. Navigate to **Jobs** from the left panel in the Azure Machine Learning studio UI
1. Select the **All jobs** tab
1. Select the **Display name** value for the job
1. On the job details page, select the **Output + logs** tab
1. In the file explorer, expand the **logs** folder, and then expand the **azureml** folder
1. Access the Spark job logs inside the **driver** and **library manager** folders

> [!NOTE]
> To troubleshoot Spark jobs created during interactive data wrangling in a notebook session, select **Job details** near the top right corner of the notebook UI. A Spark jobs from an interactive notebook session is created under the experiment name **notebook-runs**.

## Next steps

- [Code samples for Spark jobs using Azure Machine Learning CLI](https://github.com/Azure/azureml-examples/tree/main/cli/jobs/spark)
- [Code samples for Spark jobs using Azure Machine Learning Python SDK](https://github.com/Azure/azureml-examples/tree/main/sdk/python/jobs/spark)
