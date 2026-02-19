---
title: Create Jobs and Input Data for Batch Endpoints
titleSuffix: Azure Machine Learning
description: Find out how to access input data from various sources in Azure Machine Learning batch endpoint jobs. See code for the Azure CLI, the Python SDK, and REST API calls.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: inferencing
ms.topic: how-to
author: s-polly
ms.author: scottpolly
ms.date: 01/13/2026
ms.reviewer: jturuk
ms.custom:
  - devplatv2
  - devx-track-azurecli
  - ignite-2023

#customer intent: As a developer, I want to specify input data for batch endpoints in Azure Machine Learning deployments so I can create jobs by using the Azure Machine Learning CLI, the Azure Machine Learning SDK for Python, or REST requests.
---

# Create jobs and input data for batch endpoints

When you use batch endpoints in Azure Machine Learning, you can perform long batch operations over large amounts of input data. The data can be located in different places, such as across different regions. Certain types of batch endpoints can also receive literal parameters as inputs.

This article describes how to specify parameter inputs for batch endpoints and create deployment jobs. The process supports working with data from various sources, such as data assets, data stores, storage accounts, and local files.

## Prerequisites

- A batch endpoint and deployment. To create these resources, see [Deploy MLflow models in batch deployments in Azure Machine Learning](how-to-mlflow-batch.md).
- Permissions to run a batch endpoint deployment. You can use the **AzureML Data Scientist**, **Contributor**, and **Owner** roles to run a deployment. To review specific permissions that are required for custom role definitions, see [Authorization on batch endpoints](how-to-authenticate-batch-endpoint.md).
- Credentials to invoke an endpoint. For more information, see [Establish authentication](#establish-authentication).
- Read access to the input data from the compute cluster where the endpoint is deployed. 

  > [!TIP]
  > Certain situations require the use of a credential-less data store or external Azure Storage account as data input. In these scenarios, ensure that you [configure compute clusters for data access](how-to-authenticate-batch-endpoint.md#configure-compute-clusters-for-data-access), because the managed identity of the compute cluster is used for mounting the storage account. You still have granular access control because the identity of the job (the invoker) is used to read the underlying data.

## Establish authentication

To invoke an endpoint, you need a valid Microsoft Entra token. When you invoke an endpoint, Azure Machine Learning creates a batch deployment job under the identity that's associated with the token.

- If you use the Azure Machine Learning CLI (v2) or the Azure Machine Learning SDK for Python (v2) to invoke endpoints, you don't need to get the Microsoft Entra token manually. During sign in, the system authenticates your user identity. It also retrieves and passes the token for you.
- If you use the REST API to invoke endpoints, you need to get the token manually.

You can use your own credentials for the invocation, as described in the following procedures.

# [Azure CLI](#tab/cli)

Use the Azure CLI to sign in with **interactive** or **device code** authentication:

```azurecli
az login
```

# [Python SDK](#tab/sdk)

Use the Azure Machine Learning SDK for Python to sign in:

```python
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential

ml_client = MLClient.from_config(credential=DefaultAzureCredential())
```

If your configuration runs outside an Azure Machine Learning compute instance, you need to specify the workspace where the endpoint is deployed:

```python
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential

subscription_id = "<subscription-ID>"
resource_group = "<resource-group-name>"
workspace = "<workspace-name>"

ml_client = MLClient(DefaultAzureCredential(), subscription_id, resource_group, workspace)
```
    
# [REST](#tab/rest)

The easiest way to get a valid token for your user account is to use the Azure CLI. In a console, run the following Azure CLI command:

```azurecli
az account get-access-token --resource https://ml.azure.com --query "accessToken" --output tsv
```

> [!TIP]
> When you work with REST requests, we recommend that you use a service principal to invoke batch endpoints. For more information, see [Running jobs using a service principal](how-to-authenticate-batch-endpoint.md?tabs=rest#running-jobs-using-a-service-principal).

---

For more information about various types of credentials, see [How to run jobs using different types of credentials](how-to-authenticate-batch-endpoint.md#how-to-run-jobs-using-different-types-of-credentials).

## Create basic jobs

To create a job from a batch endpoint, you invoke the endpoint. You can perform invocation by using the Azure Machine Learning CLI, the Azure Machine Learning SDK for Python, or a REST API call.

The following examples show invocation basics for a batch endpoint that receives a single input data folder for processing. For examples that involve various inputs and outputs, see [Understand inputs and outputs](#understand-inputs-and-outputs).

# [Azure CLI](#tab/cli)
 
Use the `invoke` operation under batch endpoints:

```azurecli
az ml batch-endpoint invoke --name $ENDPOINT_NAME \
                            --input https://azuremlexampledata.blob.core.windows.net/data/heart-disease-uci/data
```

# [Python SDK](#tab/sdk)

Use the `MLClient.batch_endpoints.invoke()` method to invoke a batch endpoint. In the following code, `endpoint` is an endpoint object.

```python
from azure.ai.ml import Input

job = ml_client.batch_endpoints.invoke(
    endpoint_name=endpoint.name,
    inputs={
        "heart_data": Input(path="https://azuremlexampledata.blob.core.windows.net/data/heart-disease-uci/data")
    }
)
```

# [REST](#tab/rest)

Make a `POST` request to the invocation URI of the endpoint. To get the invocation URI, go to Azure Machine Learning studio and open the details page for the endpoint.

Use the following body in your request:
 
```json
{
    "properties": {
        "InputData": {
           "heart_data": {
               "JobInputType" : "UriFolder",
               "Uri": "https://azuremlexampledata.blob.core.windows.net/data/heart-disease-uci/data"
           }
        }
    }
}
```

Create your request:

```
POST HTTP/1.1
Host: <endpoint-URI>
Authorization: Bearer <token>
Content-Type: application/json
```

---

### Invoke a specific deployment

Batch endpoints can host multiple deployments under the same endpoint. The default deployment is used unless you specify another one. You can use the following procedures to change the deployment that you use.

# [Azure CLI](#tab/cli)
 
Use the argument `--deployment-name` or `-d` to specify the name of the deployment:

```azurecli
az ml batch-endpoint invoke --name $ENDPOINT_NAME \
                            --deployment-name $DEPLOYMENT_NAME \
                            --input https://azuremlexampledata.blob.core.windows.net/data/heart-disease-uci/data
```

# [Python SDK](#tab/sdk)

Use the parameter `deployment_name` to specify the name of the deployment. In the following code, `deployment` is a deployment object.

```python
job = ml_client.batch_endpoints.invoke(
    endpoint_name=endpoint.name,
    deployment_name=deployment.name,
    inputs={
        "heart_data": Input(path="https://azuremlexampledata.blob.core.windows.net/data/heart-disease-uci/data")
    }
)
```

# [REST](#tab/rest)

Use the following body in your request:
 
```json
{
    "properties": {
        "InputData": {
           "heart_data": {
               "JobInputType" : "UriFolder",
               "Uri": "https://azuremlexampledata.blob.core.windows.net/data/heart-disease-uci/data"
           }
        }
    }
}
```

Add the header key `azureml-model-deployment` to your request. For its value, use the name of the deployment that you want to invoke. 

```
POST HTTP/1.1
Host: <endpoint-URI>
Authorization: Bearer <token>
Content-Type: application/json
azureml-model-deployment: <deployment-name>
```

---

### Configure job properties

You can configure some job properties at invocation time.

> [!NOTE]
> Currently, you can configure job properties only in batch endpoints with pipeline component deployments.

#### Configure the experiment name

Use the following procedures to configure your experiment name.

# [Azure CLI](#tab/cli)
 
Use the argument `--experiment-name` to specify the name of the experiment:

```azurecli
az ml batch-endpoint invoke --name $ENDPOINT_NAME \
                            --experiment-name "my-batch-job-experiment" \
                            --input https://azuremlexampledata.blob.core.windows.net/data/heart-disease-uci/data
```

# [Python SDK](#tab/sdk)

Use the parameter `experiment_name` to specify the name of the experiment:

```python
job = ml_client.batch_endpoints.invoke(
    endpoint_name=endpoint.name,
    experiment_name="my-batch-job-experiment",
    inputs={
        "heart_data": Input(path="https://azuremlexampledata.blob.core.windows.net/data/heart-disease-uci/data"),
    }
)
```

# [REST](#tab/rest)

Indicate the experiment name by using the `experimentName` key in the `properties` section of the body:
 
```json
{
    "properties": {
        "InputData": {
           "heart_data": {
               "JobInputType" : "UriFolder",
               "Uri": "https://azuremlexampledata.blob.core.windows.net/data/heart-disease-uci/data"
           }
        },
        "properties":
        {
            "experimentName": "my-batch-job-experiment"
        }
    }
}
```

Create your request:

```
POST HTTP/1.1
Host: <endpoint-URI>
Authorization: Bearer <token>
Content-Type: application/json
```

---

## Understand inputs and outputs

Batch endpoints provide a durable API that consumers can use to create batch jobs. The same interface can be used to specify the inputs and outputs your deployment expects. Use inputs to pass any information your endpoint needs to perform the job. 

:::image type="content" source="./media/concept-endpoints/batch-endpoint-inputs-outputs.png" border="false" alt-text="Diagram that shows how inputs and outputs are used in batch endpoints." lightbox="./media/concept-endpoints/batch-endpoint-inputs-outputs.png":::

Batch endpoints support two types of inputs:

- [Data inputs](#explore-data-inputs), or pointers to a specific storage location or Azure Machine Learning asset
- [Literal inputs](#explore-literal-inputs), or literal values like numbers or strings that you want to pass to the job

The number and type of inputs and outputs depend on the [type of batch deployment](concept-endpoints-batch.md#batch-deployments). Model deployments always require one data input and produce one data output. Literal inputs aren't supported in model deployments. In contrast, pipeline component deployments provide a more general construct for building endpoints. In a pipeline component deployment, you can specify any number of data inputs, literal inputs, and outputs.

The following table summarizes the inputs and outputs for batch deployments:

| Deployment type | Number of inputs | Supported input types | Number of outputs | Supported output types |
| --- | --- | --- | --- | --- |
| [Model deployment](concept-endpoints-batch.md#model-deployment) | 1 | [Data inputs](#explore-data-inputs) | 1 | [Data outputs](#explore-data-outputs) |
| [Pipeline component deployment](concept-endpoints-batch.md#pipeline-component-deployment) | 0-*N* | [Data inputs](#explore-data-inputs) and [literal inputs](#explore-literal-inputs) | 0-*N* | [Data outputs](#explore-data-outputs) |

> [!TIP]
> Inputs and outputs are always named. Each name serves as a key for identifying the data and passing the value during invocation. Because model deployments always require one input and output, the names are ignored during invocation in model deployments. You can assign the name that best describes your use case, such as `sales_estimation`.

### Explore data inputs

Data inputs refer to inputs that point to a location where data is located. Because batch endpoints usually consume large amounts of data, you can't pass the input data as part of the invocation request. Instead, you specify the location where the batch endpoint should go to look for the data. Input data is mounted and streamed on the target compute instance to improve performance. 

Batch endpoints can read files that are located in the following types of storage:

- [Azure Machine Learning data assets](#use-input-data-from-a-data-asset), including the folder (`uri_folder`) and file (`uri_file`) types.
- [Azure Machine Learning data stores](#use-input-data-from-a-data-store), including Azure Blob Storage, Azure Data Lake Storage Gen1, and Azure Data Lake Storage Gen2.
- [Azure Storage accounts](#use-input-data-from-an-azure-storage-account), including Blob Storage, Data Lake Storage Gen1, and Data Lake Storage Gen2.
- Local data folders and files, when you use the Azure Machine Learning CLI or the Azure Machine Learning SDK for Python to invoke endpoints. The local data gets uploaded to the default data store of your Azure Machine Learning workspace.

> [!IMPORTANT]
> **Deprecation notice**: Data assets of type `FileDataset` (V1) are deprecated and will be retired in the future. Existing batch endpoints that rely on this functionality will continue to work. But there's no support for V1 datasets in batch endpoints that are created with:
>
> - Versions of the Azure Machine Learning CLI v2 that are generally available (2.4.0 and newer).
> - Versions of the REST API that are generally available (2022-05-01 and newer).

### Explore literal inputs

Literal inputs refer to inputs that can be represented and resolved at invocation time, like strings, numbers, and Boolean values. You typically use literal inputs to pass parameters to your endpoint as part of a pipeline component deployment. Batch endpoints support the following literal types:

- `string`
- `boolean`
- `float`
- `integer`

Literal inputs are only supported in pipeline component deployments. For information about specifying literal endpoints, see [Create jobs with literal inputs](#create-jobs-with-literal-inputs).

### Explore data outputs

Data outputs refer to the location where the results of a batch job are placed. Each output has an identifiable name, and Azure Machine Learning automatically assigns a unique path to each named output. You can specify another path if you need to. 

> [!IMPORTANT]
> Batch endpoints only support writing outputs in Blob Storage data stores. If you need to write to a storage account with hierarchical namespaces enabled, such as Data Lake Storage Gen2, you can register the storage service as a Blob Storage data store, because the services are fully compatible. In this way, you can write outputs from batch endpoints to Data Lake Storage Gen2.

## Create jobs with data inputs

The following examples show how to create jobs while taking data inputs from [data assets](#use-input-data-from-a-data-asset), [data stores](#use-input-data-from-a-data-store), and [Azure Storage accounts](#use-input-data-from-an-azure-storage-account).

### Use input data from a data asset

Azure Machine Learning data assets (formerly known as datasets) are supported as inputs for jobs. Follow these steps to run a batch endpoint job that uses input data that's stored in a registered data asset in Azure Machine Learning.

> [!WARNING]
> Data assets of type table (MLTable) aren't currently supported for model deployments. MLTable is supported for pipeline component deployments.

1. Create the data asset. In this example, it consists of a folder that contains multiple CSV files. You use batch endpoints to process the files in parallel. You can skip this step if your data is already registered as a data asset.

    # [Azure CLI](#tab/cli)

    1. Create a data asset definition in a YAML file named heart-data.yml:

        ```yml
        $schema: https://azuremlschemas.azureedge.net/latest/data.schema.json
        name: heart-data
        description: An unlabeled data asset for heart classification.
        type: uri_folder
        path: data
        ```

    1. Create the data asset:
  
        ```bash
        az ml data create -f heart-data.yml
        ```

    # [Python SDK](#tab/sdk)
  
    1. Create a data asset definition:

        ```python
        from azure.ai.ml.constants import AssetTypes
        from azure.ai.ml.entities import Data

        data_path = "heart-classifier-mlflow/data"
        data_asset_name = "heart-data"

        heart_data_object = Data(
            path=data_path,
            type=AssetTypes.URI_FOLDER,
            description="An unlabeled data asset for heart classification",
            name=data_asset_name
        )
        ```

    1. Create the data asset:
   
        ```python
        ml_client.data.create_or_update(heart_data_object)
        ```

        To retrieve the newly created data asset, use the following command:
   
        ```python
        heart_data_asset = ml_client.data.get(name=data_asset_name, label="latest")
        ```

    # [REST](#tab/rest)

    Use the Azure Machine Learning CLI or the Azure Machine Learning SDK for Python to create the data asset.

    ---

1. Set up the input:

    # [Azure CLI](#tab/cli)
 
    ```azurecli
    DATA_ASSET_ID=$(az ml data show -n heart-data --label latest | jq -r .id)
    ```

    # [Python SDK](#tab/sdk)

    ```python
    input = Input(path=heart_data_asset.id)
    ```

    # [REST](#tab/rest)

    Look up the following values, and then construct the data asset ID:

    - Subscription ID
    - Resource group name
    - Workspace name
    - Data asset name
    - Data asset version

    ---

    The data asset ID has the format `/subscriptions/<subscription-ID>/resourceGroups/<resource-group-name>/providers/Microsoft.MachineLearningServices/workspaces/<workspace-name>/data/<data-asset-name>/versions/<data-asset-version>`.

1. Run the endpoint:

    # [Azure CLI](#tab/cli)

    Use the `--set` argument to specify the input. First replace any hyphens in the data asset name with underscore characters. Keys can contain only alphanumeric characters and underscore characters.

    ```azurecli
    az ml batch-endpoint invoke --name $ENDPOINT_NAME \
        --set inputs.heart_data.type="uri_folder" inputs.heart_data.path=$DATA_ASSET_ID
    ```

    For an endpoint that serves a model deployment, you can use the `--input` argument to specify the data input because a model deployment always requires only one data input.

    ```azurecli
    az ml batch-endpoint invoke --name $ENDPOINT_NAME --input $DATA_ASSET_ID
    ```

    The argument `--set` tends to produce long commands when you specify multiple inputs. In such cases, you can list your inputs in a file and then refer to the file when you invoke your endpoint. For instance, you can create a YAML file named inputs.yml that contains the following lines:

    ```yml
    inputs:
      heart_data:
        type: uri_folder
        path: /subscriptions/<subscription-ID>/resourceGroups/<resource-group-name>/providers/Microsoft.MachineLearningServices/workspaces/<workspace-name>/data/heart-data/versions/1
    ```

    Then you can run the following command, which uses the `--file` argument to specify the inputs:

    ```azurecli
    az ml batch-endpoint invoke --name $ENDPOINT_NAME --file inputs.yml
    ```

    # [Python SDK](#tab/sdk)

    Call the `invoke` method, and use the `inputs` parameter to specify the required inputs:

    ```python
    job = ml_client.batch_endpoints.invoke(
        endpoint_name=endpoint.name,
        inputs={
            "heart_data": input
        }
    )
    ```

    To streamline the `invoke` call for a model deployment, use the `input` parameter to specify the location of the input data:

    ```python
    job = ml_client.batch_endpoints.invoke(
       endpoint_name=endpoint.name,
       input=input
    )
    ```

    > [!TIP]
    > [!INCLUDE [batch-endpoint-invoke-inputs-sdk](includes/batch-endpoint-invoke-inputs-sdk.md)]

    # [REST](#tab/rest)

    Use the following body in your request:

    ```json
    {
        "properties": {
            "InputData": {
                "heart_data": {
                    "JobInputType" : "UriFolder",
                    "Uri": "<data-asset-ID>"
                }
            }
        }
    }
    ```

    Create your request:

    ```
    POST HTTP/1.1
    Host: <endpoint-URI>
    Authorization: Bearer <token>
    Content-Type: application/json
    ```

    ---

### Use input data from a data store

Your batch deployment jobs can directly reference data that's in Azure Machine Learning registered data stores. In this example, you first upload some data to a data store in your Azure Machine Learning workspace. You then run a batch deployment on that data.

This example uses the default data store, but you can use a different data store. In any Azure Machine Learning workspace, the name of the default blob data store is **workspaceblobstore**. If you want to use a different data store in the following steps, replace `workspaceblobstore` with the name of your preferred data store.

1. Upload sample data to the data store. The sample data is available in the [azureml-examples](https://github.com/Azure/azureml-examples) repository. You can find the data in the [sdk/python/endpoints/batch/deploy-models/heart-classifier-mlflow/data](https://github.com/Azure/azureml-examples/tree/main/sdk/python/endpoints/batch/deploy-models/heart-classifier-mlflow/data) folder of that repository.

    1. In Azure Machine Learning studio, open the data assets page for your default blob data store, and then look up the name of its blob container.
    1. Use a tool like Azure Storage Explorer or AzCopy to upload the sample data to a folder named heart-disease-uci-unlabeled in that container.

1. Set up the input information:

    # [Azure CLI](#tab/cli)

    Place the file path in the `INPUT_PATH` variable:

    ```azurecli
    DATA_PATH="heart-disease-uci-unlabeled"
    INPUT_PATH="azureml://datastores/workspaceblobstore/paths/$DATA_PATH"
    ```

    # [Python SDK](#tab/sdk)

    Place the file path in the `input` variable:

    ```python
    data_path = "heart-disease-uci-unlabeled"
    input = Input(type=AssetTypes.URI_FOLDER, path=f"azureml://datastores/workspaceblobstore/paths/{data_path}")
    ```

    If your data is in a file, change the input type assignment to `type=AssetTypes.URI_FILE`. 

    # [REST](#tab/rest)

    Use the following body in your request. First replace the placeholders with appropriate values. Replace the `<data-path>` placeholder with `heart-disease-uci-unlabeled`.

    ```json
    {
        "properties": {
            "InputData": {
                "heart_data": {
                    "JobInputType" : "UriFolder",
                    "Uri": "/subscriptions/<subscription-ID>/resourceGroups/<resource-group-name>/providers/Microsoft.MachineLearningServices/workspaces/<workspace-name>/datastores/workspaceblobstore/paths/<data-path>"
                }
            }
        }
    }

    ```

    If your data is in a file, use the `UriFile` type for the `JobInputType` value. 

    ---
    
    Notice how the `paths` folder is part of the input path. This format indicates that the value that follows is a path.

1. Run the endpoint:

    # [Azure CLI](#tab/cli)

    Use the `--set` argument to specify the input:

    ```azurecli
    az ml batch-endpoint invoke --name $ENDPOINT_NAME \
        --set inputs.heart_data.type="uri_folder" inputs.heart_data.path=$INPUT_PATH
    ```

    For an endpoint that serves a model deployment, you can use the `--input` argument to specify the data input because a model deployment always requires only one data input.

    ```azurecli
    az ml batch-endpoint invoke --name $ENDPOINT_NAME --input $INPUT_PATH --input-type uri_folder
    ```
    
    The argument `--set` tends to produce long commands when you specify multiple inputs. In such cases, you can list your inputs in a file and then refer to the file when you invoke your endpoint. For instance, you can create a YAML file named inputs.yml that contains the following lines:
    
    ```yml
    inputs:
      heart_data:
        type: uri_folder
        path: azureml://datastores/workspaceblobstore/paths/<data-path>
    ```
    
    If your data is in a file, use the `uri_file` type for the input instead.

    Then you can run the following command, which uses the `--file` argument to specify the inputs:

    ```azurecli
    az ml batch-endpoint invoke --name $ENDPOINT_NAME --file inputs.yml
    ```

    # [Python SDK](#tab/sdk)

    Call the `invoke` method by using the `inputs` parameter to specify the required inputs:

    ```python
    job = ml_client.batch_endpoints.invoke(
        endpoint_name=endpoint.name,
        inputs={
            "heart_data": input
        }
    )
    ```

    To streamline the `invoke` call for a model deployment, use the `input` parameter to specify the location of the input data:

    ```python
    job = ml_client.batch_endpoints.invoke(
       endpoint_name=endpoint.name,
       input=input
    )
    ```

    > [!TIP]
    > [!INCLUDE [batch-endpoint-invoke-inputs-sdk](includes/batch-endpoint-invoke-inputs-sdk.md)]

    # [REST](#tab/rest)

    Create your request:

    ```
    POST HTTP/1.1
    Host: <endpoint-URI>
    Authorization: Bearer <token>
    Content-Type: application/json
    ```

    ---

### Use input data from an Azure Storage account

Azure Machine Learning batch endpoints can read data from cloud locations in Azure Storage accounts, both public and private. Use the following steps to run a batch endpoint job with data in a storage account.

For more information about extra required configurations for reading data from storage accounts, see [Configure compute clusters for data access](how-to-authenticate-batch-endpoint.md#configure-compute-clusters-for-data-access).

1. Set up the input:

    # [Azure CLI](#tab/cli)

    Set the `INPUT_DATA` variable:

    ```azurecli
    INPUT_DATA="https://azuremlexampledata.blob.core.windows.net/data/heart-disease-uci/data"
    ```

    If your data is in a file, use a format similar to the following one to define the input path:

    ```azurecli
    INPUT_DATA="https://azuremlexampledata.blob.core.windows.net/data/heart-disease-uci/data/heart.csv"
    ```

    # [Python SDK](#tab/sdk)

    Set the `input` variable:

    ```python
    input = Input(
        type=AssetTypes.URI_FOLDER, 
        path="https://azuremlexampledata.blob.core.windows.net/data/heart-disease-uci/data"
    )
    ```

    If your data is in a file, change the input type assignment to `type=AssetTypes.URI_FILE`:

    ```python
    input = Input(
        type=AssetTypes.URI_FILE,
        path="https://azuremlexampledata.blob.core.windows.net/data/heart-disease-uci/data/heart.csv"
    )
    ```

    # [REST](#tab/rest)

    Use the following body in your request:

    ```json
    {
       "properties": {
           "InputData": {
               "heart_data": {
                   "JobInputType" : "UriFolder",
                   "Uri": "https://azuremlexampledata.blob.core.windows.net/data/heart-disease-uci/data"
               }
           }
       }
    }
    ```

    If your data is in a file, change the `JobInputType` value to `UriFile`:

    ```json
    {
       "properties": {
           "InputData": {
               "heart_data": {
                   "JobInputType" : "UriFile",
                   "Uri": "https://azuremlexampledata.blob.core.windows.net/data/heart-disease-uci/data/heart.csv"
               }
           }
       }
    }
    ```

    ---

1. Run the endpoint:

    # [Azure CLI](#tab/cli)
    
    Use the `--set` argument to specify the input:

    ```azurecli
    az ml batch-endpoint invoke --name $ENDPOINT_NAME \
        --set inputs.heart_data.type="uri_folder" inputs.heart_data.path=$INPUT_DATA
    ```

    For an endpoint that serves a model deployment, you can use the `--input` argument to specify the data input because a model deployment always requires only one data input.

    ```azurecli
    az ml batch-endpoint invoke --name $ENDPOINT_NAME --input $INPUT_DATA --input-type uri_folder
    ```
    
    The `--set` argument tends to produce long commands when you specify multiple inputs. In such cases, you can list your inputs in a file and then refer to the file when you invoke your endpoint. For instance, you can create a YAML file named inputs.yml that contains the following lines:
    
    ```yml
    inputs:
      heart_data:
        type: uri_folder
        path: https://azuremlexampledata.blob.core.windows.net/data/heart-disease-uci/data
    ```
    
    You can then run the following command, which uses the `--file` argument to specify the inputs:

    ```azurecli
    az ml batch-endpoint invoke --name $ENDPOINT_NAME --file inputs.yml
    ```

    If your data is in a file, use the `uri_file` type for the data input in the inputs.yml file. 

    # [Python SDK](#tab/sdk)

    Call the `invoke` method by using the `inputs` parameter to specify the required inputs:

    ```python
    job = ml_client.batch_endpoints.invoke(
        endpoint_name=endpoint.name,
        inputs={
            "heart_data": input
        }
    )
    ```

    To streamline the `invoke` call for a model deployment, use the `input` parameter to specify the location of the input data:

    ```python
    job = ml_client.batch_endpoints.invoke(
       endpoint_name=endpoint.name,
       input=input
    )
    ```

    > [!TIP]
    > [!INCLUDE [batch-endpoint-invoke-inputs-sdk](includes/batch-endpoint-invoke-inputs-sdk.md)]

    # [REST](#tab/rest)

    Create your request:

    ```
    POST HTTP/1.1
    Host: <endpoint-URI>
    Authorization: Bearer <token>
    Content-Type: application/json
    ```

    ---

## Create jobs with literal inputs

Pipeline component deployments can take literal inputs. For an example of a batch deployment that contains a basic pipeline, see [How to deploy pipelines with batch endpoints](how-to-use-batch-pipeline-deployments.md).

The following example shows how to specify an input named `score_mode`, of type `string`, with a value of `append`:

# [Azure CLI](#tab/cli)

Place your inputs in a YAML file, such as one named inputs.yml:

```yml
inputs:
  score_mode:
    type: string
    default: append
```

Run the following command, which uses the `--file` argument to specify the inputs.

```azurecli
az ml batch-endpoint invoke --name $ENDPOINT_NAME --file inputs.yml
```

You can also use the `--set` argument to specify the type and default value. But this approach tends to produce long commands when you specify multiple inputs:

```azurecli
az ml batch-endpoint invoke --name $ENDPOINT_NAME \
    --set inputs.score_mode.type="string" inputs.score_mode.default="append"
```

# [Python SDK](#tab/sdk)

Use the `inputs` parameter to supply information about the literal input.

```python
job = ml_client.batch_endpoints.invoke(
    endpoint_name=endpoint.name, 
    inputs = { 
        'score_mode': Input(type="string", default="append")
        }
)
```

# [REST](#tab/rest)

Use the following body in your request:

```json
{
    "properties": {
        "InputData": {
            "score_mode": {
                "JobInputType" : "Literal",
                "Value": "append"
            }
        }
    }
}
```

Create your request:

```
POST HTTP/1.1
Host: <endpoint-URI>
Authorization: Bearer <token>
Content-Type: application/json
```

---

## Create jobs with data outputs

The following example shows how to change the location of an output named `score`. For completeness, the example also configures an input named `heart_data`.

This example uses the default data store, **workspaceblobstore**. But you can use any other data store in your workspace as long as it's a Blob Storage account. If you want to use a different data store, replace `workspaceblobstore` in the following steps with the name of your preferred data store.

1. Get the ID of the data store.  

    # [Azure CLI](#tab/cli)

    ```azurecli
    DATA_STORE_ID=$(az ml datastore show -n workspaceblobstore | jq -r '.id')
    ```

    # [Python SDK](#tab/sdk)

    ```python
    from azure.ai.ml import Output

    default_ds = ml_client.datastores.get_default()
    ```

    # [REST](#tab/rest)

    Look up the following values, and then construct the data store ID:

    - Subscription ID
    - Resource group name
    - Workspace name

    ---
    
    The data store ID has the format `/subscriptions/<subscription-ID>/resourceGroups/<resource-group-name>/providers/Microsoft.MachineLearningServices/workspaces/<workspace-name>/datastores/workspaceblobstore`.

1. Create a data output:

    # [Azure CLI](#tab/cli)
    
    Define the input and output values in a file named inputs-and-outputs.yml. Use the data store ID in the output path. For completeness, also define the data input.

    ```yml
    inputs:
      heart_data:
        type: uri_folder
        path: https://azuremlexampledata.blob.core.windows.net/data/heart-disease-uci/data
    outputs:
      score:
        type: uri_file
        path: <data-store-ID>/paths/batch-jobs/my-unique-path
    ```

    # [Python SDK](#tab/sdk)

    Set the `output` path variable:

    ```python
    data_path = "batch-jobs/my-unique-path"
    output = Output(type=AssetTypes.URI_FILE, path=f"{default_ds.id}/paths/{data_path}")
    ```

    For completeness, also create a data input:

    ```python
    input = Input(
        type=AssetTypes.URI_FOLDER,
        path="https://azuremlexampledata.blob.core.windows.net/data/heart-disease-uci/data"
    )
    ```

    # [REST](#tab/rest)

    Use the following body in your request. First replace the `<data-path>` placeholder with a unique path, such as `batch-jobs/my-unique-path`. Also replace the `<data-store-ID>` placeholder with the ID of your data store.

    ```json
    {
        "properties": {
            "InputData": {
               "heart_data": {
                   "JobInputType" : "UriFolder",
                   "Uri": "https://azuremlexampledata.blob.core.windows.net/data/heart-disease-uci/data"
               }
            },
            "OutputData": {
                "score": {
                    "JobOutputType" : "UriFile",
                    "Uri": "<data-store-ID>/paths/<data-path>"
                }
            }
        }
    }
    ```

    ---
    
    > [!NOTE]
    > Notice how the `paths` folder is part of the output path. This format indicates that the value that follows is a path.

1. Run the deployment:

    # [Azure CLI](#tab/cli)
   
    Use the `--file` argument to specify the input and output values:

    ```azurecli
    az ml batch-endpoint invoke --name $ENDPOINT_NAME --file inputs-and-outputs.yml
    ```
   
    # [Python SDK](#tab/sdk)

    Use the `outputs` parameter to supply information about the output.

    ```python
    job = ml_client.batch_endpoints.invoke(
       endpoint_name=endpoint.name,
       inputs={ "heart_data": input },
       outputs={ "score": output }
    )
    ```

    # [REST](#tab/rest)

    Create your request:

    ```
    POST HTTP/1.1
    Host: <endpoint-URI>
    Authorization: Bearer <token>
    Content-Type: application/json
    ```

    ---

## Related content

- [Customize outputs in batch deployments](how-to-deploy-model-custom-output.md)
- [How to deploy a pipeline to perform batch scoring with preprocessing](how-to-use-batch-scoring-pipeline.md)
- [Run batch endpoints from Azure Data Factory](how-to-use-batch-azure-data-factory.md)
