---
title: Train ML models
titleSuffix: Azure Machine Learning
description: Configure and submit Azure Machine Learning jobs to train your models using the SDK, CLI, etc.
services: machine-learning
author: s-polly
ms.author: scottpolly
ms.reviewer: sooryar
ms.service: azure-machine-learning
ms.subservice: training
ms.date: 05/20/2026
ms.topic: how-to
ai-usage: ai-assisted
ms.custom:
  - sdkv2
  - build-2023
  - ignite-2023
  - update-code3
  - dev-focus
---

# Train models with Azure Machine Learning CLI, SDK, and REST API

[!INCLUDE [dev v2](includes/machine-learning-dev-v2.md)]

Azure Machine Learning provides multiple ways to submit ML training jobs. In this article, you learn how to submit jobs by using the following methods:

* Azure CLI extension for machine learning: The `ml` extension, also referred to as CLI v2.
* Python SDK v2 for Azure Machine Learning.
* REST API: The API that the CLI and SDK are built on.

## Prerequisites

* An Azure subscription. If you don't have an Azure subscription, create a free account before you begin. Try the [free or paid version of Azure Machine Learning](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
* An Azure Machine Learning workspace. If you don't have one, you can use the steps in the [Create resources to get started](quickstart-create-resources.md) article.

# [Python SDK](#tab/python)

To use the __SDK__:

- Install the Azure Machine Learning [SDK v2 for Python](https://aka.ms/sdk-v2-install).
- Install the [azure-identity](/python/api/azure-identity) package: `pip install azure-identity`.

# [Azure CLI](#tab/azurecli)

To use the __CLI__, install the [Azure CLI and extension for machine learning](how-to-configure-cli.md).

# [REST API](#tab/restapi)

To use the __REST API__ information, you need the following items:

- A __service principal__ in your workspace. Use [service principal authentication](how-to-setup-authentication.md#use-service-principal-authentication) for administrative REST requests.
- A service principal __authentication token__. Follow the steps in [Retrieve a service principal authentication token](./how-to-manage-rest.md#retrieve-a-service-principal-authentication-token) to get this token. 
- The __curl__ utility. The curl program is available in the [Windows Subsystem for Linux](/windows/wsl/install-win10) or any UNIX distribution. 

    > [!TIP]
    > In PowerShell, `curl` is an alias for `Invoke-WebRequest`. The command `curl -d "key=val" -X POST uri` becomes `Invoke-WebRequest -Body "key=val" -Method POST -Uri uri`.
    >
    > While it's possible to call the REST API from PowerShell, the examples in this article assume you're using Bash.

- The [jq](https://jqlang.github.io/jq/) utility for processing JSON. Use this utility to extract values from the JSON documents that REST API calls return.

---

### Clone the examples repository

The code snippets in this article are based on examples in the [Azure Machine Learning examples GitHub repo](https://github.com/azure/azureml-examples). To clone the repository to your development environment, use the following command:

```bash
git clone --depth 1 https://github.com/Azure/azureml-examples
cd azureml-examples
```

> [!TIP]
> Use `--depth 1` to clone only the latest commit to the repository, which reduces the time to complete the operation.

The remaining commands in this article assume you're running from the `azureml-examples` directory.

## Example job

The examples in this article use the iris flower dataset to train an MLFlow model.

## Train in the cloud

When you train in the cloud, you must connect to your Azure Machine Learning workspace and select a compute resource to run the training job.

### Connect to the workspace

> [!TIP]
> Use the following tabs to select the method you want to use to train a model. Selecting a tab automatically switches all the tabs in this article to the same tab. You can select another tab at any time.

# [Python SDK](#tab/python)

To connect to the workspace, you need identifier parameters - a subscription, resource group, and workspace name. Use these details in the `MLClient` from the `azure.ai.ml` namespace to get a handle to the required Azure Machine Learning workspace. To authenticate, use the [default Azure authentication](/python/api/azure-identity/azure.identity.defaultazurecredential?view=azure-python&preserve-view=true). For more information about how to configure credentials and connect to a workspace, see this [example](https://github.com/Azure/azureml-examples/blob/main/sdk/python/jobs/configuration.ipynb).

```python
#import required libraries
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential

#Enter details of your Azure Machine Learning workspace
subscription_id = '<SUBSCRIPTION_ID>'
resource_group = '<RESOURCE_GROUP>'
workspace = '<AZUREML_WORKSPACE_NAME>'

#connect to the workspace
ml_client = MLClient(DefaultAzureCredential(), subscription_id, resource_group, workspace)
```

Verify the connection by printing the workspace name:

```python
print(ml_client.workspace_name)
```


# [Azure CLI](#tab/azurecli)

When you use the Azure CLI, you need identifier parameters - a subscription, resource group, and workspace name. While you can specify these parameters for each command, you can also set defaults that all commands use. Use the following commands to set default values. Replace `<subscription ID>`, `<Azure Machine Learning workspace name>`, and `<resource group>` with the values for your configuration:

```azurecli
az account set --subscription <subscription ID>
az configure --defaults workspace=<Azure Machine Learning workspace name> group=<resource group>
```


# [REST API](#tab/restapi)

The REST API examples in this article use `$SUBSCRIPTION_ID`, `$RESOURCE_GROUP`, `$LOCATION`, and `$WORKSPACE` placeholders. Replace the placeholders with your own values as follows:

* `$SUBSCRIPTION_ID`: Your Azure subscription ID.
* `$RESOURCE_GROUP`: The Azure resource group that contains your workspace.
* `$LOCATION`: The Azure region where your workspace is located.
* `$WORKSPACE`: The name of your Azure Machine Learning workspace.
* `$COMPUTE_NAME`: The name of your Azure Machine Learning compute cluster.

Administrative REST requests require a [service principal authentication token](how-to-manage-rest.md#retrieve-a-service-principal-authentication-token). You can retrieve a token with the following command. The token is stored in the `$TOKEN` environment variable:

:::code language="azurecli" source="~/azureml-examples-main/deploy-arm-templates-az-cli.sh" id="get_access_token":::

The service provider uses the `api-version` argument to ensure compatibility. The `api-version` argument varies from service to service.

This article uses Azure Resource Manager endpoints (`management.azure.com`). Set `API_VERSION` to the current Azure Machine Learning Resource Manager version:

```bash
API_VERSION="2025-09-01"
```

If you use Azure Machine Learning data plane APIs, they can use a different version. For example, the Azure AI Assets data plane reference uses `2024-04-01-preview`. For more information, see the REST operation groups for [Azure Machine Learning (Resource Manager)](/rest/api/azureml/operation-groups?view=rest-azureml-2025-09-01&preserve-view=true) and [Azure AI Assets (data plane)](/rest/api/ai-assets/operation-groups?view=rest-ai-assets-2024-04-01-preview&preserve-view=true).

When you train by using the REST API, you must upload data and training scripts to a storage account that the workspace can access. The following example gets the storage information for your workspace and saves it into variables so you can use it later:

:::code language="azurecli" source="~/azureml-examples-main/deploy-arm-templates-az-cli.sh" id="get_storage_details":::

---

### Create a compute resource for training

> [!NOTE]
> To try [serverless compute](./how-to-use-serverless-compute.md), skip this step and proceed to [Submit the training job](#submit-the-training-job).

An Azure Machine Learning compute cluster is a fully managed compute resource that you can use to run the training job. In the following examples, you create a compute cluster named `cpu-cluster`.



# [Python SDK](#tab/python)

[!notebook-python[] (~/azureml-examples-main/sdk/python/jobs/configuration.ipynb?name=create-cpu-compute)]

Verify the compute cluster exists:

```python
cpu_cluster = ml_client.compute.get("cpu-cluster")
print(f"Compute '{cpu_cluster.name}' provisioning state: {cpu_cluster.provisioning_state}")
```

# [Azure CLI](#tab/azurecli)

```azurecli
az ml compute create -n cpu-cluster --type amlcompute --min-instances 0 --max-instances 4
```

# [REST API](#tab/restapi)

```bash
curl -X PUT \
  "https://management.azure.com/subscriptions/$SUBSCRIPTION_ID/resourceGroups/$RESOURCE_GROUP/providers/Microsoft.MachineLearningServices/workspaces/$WORKSPACE/computes/$COMPUTE_NAME?api-version=$API_VERSION" \
  -H "Authorization:Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "location": "'$LOCATION'",
    "properties": {
        "computeType": "AmlCompute",
        "properties": {
            "vmSize": "Standard_D2_V2",
            "vmPriority": "Dedicated",
            "scaleSettings": {
                "maxNodeCount": 4,
                "minNodeCount": 0,
                "nodeIdleTimeBeforeScaleDown": "PT30M"
            }
        }
    }
}'
```

> [!TIP]
> While the operation returns a response after a few seconds, this response only indicates that the creation request is accepted. It can take several minutes for the cluster creation to finish.

---

### Submit the training job

# [Python SDK](#tab/python)

To run this script, use a `command` that executes the main.py Python script located under `./sdk/python/jobs/single-step/lightgbm/iris/src/`. You submit the command as a `job` to Azure Machine Learning. 

> [!NOTE]
> To use [serverless compute](./how-to-use-serverless-compute.md), delete `compute="cpu-cluster"` in this code.

[!notebook-python[] (~/azureml-examples-main/sdk/python/jobs/single-step/lightgbm/iris/lightgbm-iris-sweep.ipynb?name=create-command)]

Submit the job in the same Python session:

[!notebook-python[] (~/azureml-examples-main/sdk/python/jobs/single-step/lightgbm/iris/lightgbm-iris-sweep.ipynb?name=run-command)]

In the preceding examples, you configured:
- `code` - path where the code to run the command is located.
- `command` - command that needs to run.
- `environment` - the environment needed to run the training script. In this example, use a curated or ready-made environment provided by Azure Machine Learning called `AzureML-lightgbm-3.2-ubuntu18.04-py37-cpu@latest`. You can also use custom environments by specifying a base docker image and specifying a conda yaml on top of it.
- `inputs` - dictionary of inputs using name value pairs to the command. The key is a name for the input within the context of the job and the value is the input value. Reference inputs in the `command` by using the `${{inputs.<input_name>}}` expression. To use files or folders as inputs, use the `Input` class. For more information, see [SDK and CLI v2 expressions](concept-expressions.md).

For more information, see the [reference documentation](/python/api/azure-ai-ml/azure.ai.ml?view=azure-python&preserve-view=true#azure-ai-ml-command).

When you submit the job, the service returns a URL to the job status in the Azure Machine Learning studio. Use the studio UI to view the job progress. You can also use `returned_job.status` to check the current status of the job.

```python
print(f"Studio URL: {returned_job.studio_url}")
```

# [Azure CLI](#tab/azurecli)

The `az ml job create` command in this example requires a YAML job definition file. The file used in this example contains the following content:


> [!NOTE]
> To use [serverless compute](./how-to-use-serverless-compute.md), delete `compute: azureml:cpu-cluster"` in this code.

:::code language="yaml" source="~/azureml-examples-main/cli/jobs/single-step/lightgbm/iris/job.yml":::

In the preceding YAML, you configured:
- `code` - path where the code to run the command is located.
- `command` - command that needs to be run.
- `inputs` - dictionary of inputs using name value pairs to the command. The key is a name for the input within the context of the job and the value is the input value. Inputs are referenced in the `command` by using the `${{inputs.<input_name>}}` expression. For more information, see [SDK and CLI v2 expressions](concept-expressions.md).
- `environment` - the environment needed to run the training script. In this example, use a curated or ready-made environment provided by Azure Machine Learning called `AzureML-lightgbm-3.3@latest`. You can also use custom environments by specifying a base docker image and specifying a conda yaml on top of it.
To submit the job, use the following command. The run ID (name) of the training job is stored in the `$run_id` variable:

```azurecli
run_id=$(az ml job create -f jobs/single-step/lightgbm/iris/job.yml --query name -o tsv)
```

Use the stored run ID to return information about the job. The `--web` parameter opens the Azure Machine Learning studio web UI where you can drill into details on the job:

:::code language="azurecli" source="~/azureml-examples-main/cli/train.sh" id="hello_world_show":::

# [REST API](#tab/restapi)

When you submit a job, you need to upload the training scripts and data to a cloud storage location that your Azure Machine Learning workspace can access. 

1. Use the following Azure CLI command to upload the training script. The command specifies the _directory_ that contains the files needed for training, not an individual file. If you want to use REST to upload the data instead, see the [Put Blob](/rest/api/storageservices/put-blob) reference:

    ```azurecli
    az storage blob upload-batch -d $AZUREML_DEFAULT_CONTAINER/testjob -s cli/jobs/single-step/lightgbm/iris/src/ --account-name $AZURE_STORAGE_ACCOUNT
    ```

1. Create a versioned reference to the training data. In this example, the data is already in the cloud and located at `https://azuremlexamples.blob.core.windows.net/datasets/iris.csv`. For more information on referencing data, see [Data in Azure Machine Learning](concept-data.md):

    ```bash
    DATA_VERSION=$RANDOM
    curl --location --request PUT "https://management.azure.com/subscriptions/$SUBSCRIPTION_ID/resourceGroups/$RESOURCE_GROUP/providers/Microsoft.MachineLearningServices/workspaces/$WORKSPACE/data/iris-data/versions/$DATA_VERSION?api-version=$API_VERSION" \
    --header "Authorization: Bearer $TOKEN" \
    --header "Content-Type: application/json" \
    --data-raw "{
            \"properties\": {
            \"description\": \"Iris dataset\",
            \"dataType\": \"uri_file\",
            \"dataUri\": \"https://azuremlexamples.blob.core.windows.net/datasets/iris.csv\"
        }
    }"
    ```

1. Register a versioned reference to the training script for use with a job. In this example, the script location is the default storage account and container you uploaded to in step 1. The ID of the versioned training code is returned and stored in the `$TRAIN_CODE` variable:

    ```bash
    TRAIN_CODE=$(curl --location --request PUT "https://management.azure.com/subscriptions/$SUBSCRIPTION_ID/resourceGroups/$RESOURCE_GROUP/providers/Microsoft.MachineLearningServices/workspaces/$WORKSPACE/codes/train-lightgbm/versions/1?api-version=$API_VERSION" \
    --header "Authorization: Bearer $TOKEN" \
    --header "Content-Type: application/json" \
    --data-raw "{
            \"properties\": {
            \"description\": \"Train code\",
            \"codeUri\": \"https://$AZURE_STORAGE_ACCOUNT.blob.core.windows.net/$AZUREML_DEFAULT_CONTAINER/testjob\"
        }
    }" | jq -r '.id')
    ```

1. Create the environment that the cluster uses to run the training script. In this example, use a curated or ready-made environment provided by Azure Machine Learning called `AzureML-lightgbm-3.3`.

Azure Resource Manager doesn't support an `@latest` shortcut for environment IDs. The following command lists the environment versions and selects the most recently modified version ID, which is then stored in the `$ENVIRONMENT` variable.

```bash
ENVIRONMENT_NAME="AzureML-lightgbm-3.3"
ENVIRONMENT=$(curl --location --request GET "https://management.azure.com/subscriptions/$SUBSCRIPTION_ID/resourceGroups/$RESOURCE_GROUP/providers/Microsoft.MachineLearningServices/workspaces/$WORKSPACE/environments/$ENVIRONMENT_NAME/versions?api-version=$API_VERSION" \
    --header "Authorization: Bearer $TOKEN" | jq -r '.value | sort_by(.systemData.lastModifiedAt) | last | .id')
```

1. Finally, submit the job. The following example shows how to submit the job, reference the training code ID, environment ID, URL for the input data, and the ID of the compute cluster. The job output location is stored in the `$JOB_OUTPUT` variable:

    > [!TIP]
    > The job name must be unique. In this example, `uuidgen` is used to generate a unique value for the name.

    > [!NOTE]
    > To use [serverless compute](./how-to-use-serverless-compute.md), delete the `\"computeId\":` line in this code.

    ```bash
    run_id=$(uuidgen)
    curl --location --request PUT "https://management.azure.com/subscriptions/$SUBSCRIPTION_ID/resourceGroups/$RESOURCE_GROUP/providers/Microsoft.MachineLearningServices/workspaces/$WORKSPACE/jobs/$run_id?api-version=$API_VERSION" \
    --header "Authorization: Bearer $TOKEN" \
    --header "Content-Type: application/json" \
    --data-raw "{
        \"properties\": {
            \"jobType\": \"Command\",
            \"codeId\": \"$TRAIN_CODE\",
            \"command\": \"python main.py --iris-csv \$AZURE_ML_INPUT_iris\",
            \"environmentId\": \"$ENVIRONMENT\",
            \"inputs\": {
                \"iris\": {
                    \"jobInputType\": \"uri_file\",
                    \"uri\": \"https://azuremlexamples.blob.core.windows.net/datasets/iris.csv\"
                }
            },
            \"experimentName\": \"lightgbm-iris\",
            \"computeId\": \"/subscriptions/$SUBSCRIPTION_ID/resourceGroups/$RESOURCE_GROUP/providers/Microsoft.MachineLearningServices/workspaces/$WORKSPACE/computes/$COMPUTE_NAME\"
        }
    }"
    ```

---

> [!IMPORTANT]
> Azure Machine Learning training and command jobs don't support Azure Container Registries (ACR) that use customized domain name labels. Jobs that reference such a registry might fail during startup due to image pull or environment resolution errors. To avoid this issue:
>
> - Use the default login server format (`<registry-name>.azurecr.io`) for your ACR.
> - When you create the registry, set **Domain name label scope** to **Unsecure**.

### Monitor the training job

Wait for the training job to complete before you register the model. The job status transitions through `Starting` → `Preparing` → `Running` → `Completed`.

# [Python SDK](#tab/python)

Use `ml_client.jobs.stream()` to monitor the job output in real time:

```python
ml_client.jobs.stream(returned_job.name)
```

Alternatively, check the job status programmatically:

```python
returned_job = ml_client.jobs.get(returned_job.name)
print(f"Job status: {returned_job.status}")
```

# [Azure CLI](#tab/azurecli)

Use the `az ml job show` command with `--query status` to check job status:

```azurecli
az ml job show -n $run_id --query status -o tsv
```

To stream the job logs until completion:

```azurecli
az ml job stream -n $run_id
```

# [REST API](#tab/restapi)

Check the job status with a GET request:

```bash
curl --location --request GET "https://management.azure.com/subscriptions/$SUBSCRIPTION_ID/resourceGroups/$RESOURCE_GROUP/providers/Microsoft.MachineLearningServices/workspaces/$WORKSPACE/jobs/$run_id?api-version=$API_VERSION" \
--header "Authorization: Bearer $TOKEN" | jq -r '.properties.status'
```

---

## Register the trained model

The following examples demonstrate how to register a model in your Azure Machine Learning workspace.

# [Python SDK](#tab/python)

> [!TIP]
> The training job returns a `name` property. Use this name as part of the path to the model.

```python
from azure.ai.ml.entities import Model
from azure.ai.ml.constants import AssetTypes

run_model = Model(
    path="azureml://jobs/{}/outputs/artifacts/paths/model/".format(returned_job.name),
    name="run-model-example",
    description="Model created from run.",
    type=AssetTypes.MLFLOW_MODEL
)

ml_client.models.create_or_update(run_model)
```

Verify the model was registered:

```python
registered_model = ml_client.models.get("run-model-example", version="1")
print(f"Model '{registered_model.name}' version {registered_model.version} registered successfully.")
```

# [Azure CLI](#tab/azurecli)

> [!TIP]
> Use the name stored in the `$run_id` variable as part of the path to the model.

:::code language="azurecli" source="~/azureml-examples-main/cli/train.sh" id="sklearn_download_register_model":::

# [REST API](#tab/restapi)

> [!TIP]
> Use the name stored in the `$run_id` variable as part of the path to the model.

```bash
curl --location --request PUT "https://management.azure.com/subscriptions/$SUBSCRIPTION_ID/resourceGroups/$RESOURCE_GROUP/providers/Microsoft.MachineLearningServices/workspaces/$WORKSPACE/models/sklearn/versions/1?api-version=$API_VERSION" \
--header "Authorization: Bearer $TOKEN" \
--header "Content-Type: application/json" \
--data-raw "{
    \"properties\": {
        \"modelType\": \"mlflow_model\",
        \"modelUri\":\"runs:/$run_id/model\"
    }
}"
```

---

## Clean up resources

If you don't plan to use the compute cluster for more training jobs, delete it to stop incurring charges. The cluster continues to bill while it exists, even with zero nodes running.

# [Python SDK](#tab/python)

```python
ml_client.compute.begin_delete("cpu-cluster").wait()
```

# [Azure CLI](#tab/azurecli)

```azurecli
az ml compute delete -n cpu-cluster --yes
```

# [REST API](#tab/restapi)

```bash
curl --location --request DELETE "https://management.azure.com/subscriptions/$SUBSCRIPTION_ID/resourceGroups/$RESOURCE_GROUP/providers/Microsoft.MachineLearningServices/workspaces/$WORKSPACE/computes/$COMPUTE_NAME?api-version=$API_VERSION" \
--header "Authorization: Bearer $TOKEN"
```

---

## Troubleshoot common errors

| Error | Cause | Resolution |
|---|---|---|
| `ImportError: No module named 'azure.identity'` | Missing `azure-identity` package | Run `pip install azure-identity` |
| `DefaultAzureCredential failed` | Not signed in to Azure | Run `az login` first, or set environment variables for [service principal authentication](how-to-setup-authentication.md#use-service-principal-authentication) |
| `ComputeNotFound` | Cluster name mismatch or cluster deleted | Verify the cluster name and check provisioning state |
| `EnvironmentNotFound` | Curated environment deprecated or unavailable | List available environments with `ml_client.environments.list()` and use a current version |
| `QuotaExceeded` | Insufficient vCPU quota for the VM size | [Request a quota increase](/azure/quotas/quickstart-increase-quota-portal) or use a smaller VM size |

For environment-specific issues, see [Troubleshoot environment image builds](how-to-troubleshoot-environments.md).

## Next steps

Now that you have a trained model, learn [how to deploy it using an online endpoint](how-to-deploy-online-endpoints.md).

For more examples, see the [Azure Machine Learning examples](https://github.com/azure/azureml-examples) GitHub repository.

For more information on the Azure CLI commands, Python SDK classes, or REST APIs used in this article, see the following reference documentation:

* [Azure CLI `ml` extension](/cli/azure/ml)
* [Python SDK](/python/api/azure-ai-ml/azure.ai.ml)
* [REST API](/rest/api/azureml/)
