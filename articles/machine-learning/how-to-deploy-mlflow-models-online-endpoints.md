---
title: Deploy MLflow models to real-time endpoints
titleSuffix: Azure Machine Learning
description: Learn to deploy your MLflow model as a web service that's managed by Azure.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: inferencing
author: msakande
ms.author: mopeakande
ms.reviewer: fasantia
ms.date: 01/16/2025
ms.topic: how-to
ms.custom: deploy, mlflow, devplatv2, no-code-deployment, devx-track-azurecli, cliv2, update-code
---

# Deploy MLflow models to online endpoints

[!INCLUDE [cli v2](includes/machine-learning-cli-v2.md)]


In this article, you see how to deploy your [MLflow](https://www.mlflow.org) model to an [online endpoint](concept-endpoints.md) for real-time inference. When you deploy your MLflow model to an online endpoint, you don't need to specify a scoring script or an environment—this functionality is known as _no-code deployment_.

For no-code-deployment, Azure Machine Learning:

* Dynamically installs Python packages that you list in a `conda.yaml` file. As a result, dependencies are installed during container runtime.
* Provides an MLflow base image, or curated environment, that contains the following items:
    * The [`azureml-inference-server-http`](how-to-inference-server-http.md) package
    * The [`mlflow-skinny`](https://github.com/mlflow/mlflow/blob/master/README_SKINNY.md) package
    * A scoring script for inferencing

[!INCLUDE [mlflow-model-package-for-workspace-without-egress](includes/mlflow-model-package-for-workspace-without-egress.md)]

## Prerequisites

- An Azure subscription. If you don't have an Azure subscription, create a [free account](https://azure.microsoft.com/free/) before you begin.

- A user account that has at least one of the following Azure role-based access control (Azure RBAC) roles:
  - An Owner role for the Azure Machine Learning workspace
  - A Contributor role for the Azure Machine Learning workspace
  - A custom role that has `Microsoft.MachineLearningServices/workspaces/onlineEndpoints/*` permissions

  For more information, see [Manage access to Azure Machine Learning workspaces](how-to-assign-roles.md).

- Access to Azure Machine Learning:

    # [Azure CLI](#tab/cli)

    Install the Azure CLI and the `ml` extension to the Azure CLI. For installation steps, see [Install and set up the CLI (v2)](how-to-configure-cli.md).

    # [Python (Azure Machine Learning SDK)](#tab/sdk)

    Install the Azure Machine Learning SDK for Python.

        ```bash
        pip install azure-ai-ml azure-identity
        ```

    # [Python (MLflow SDK)](#tab/mlflow)

    - Install the MLflow SDK package, `mlflow`, and the Azure Machine Learning plug-in for MLflow, `azureml-mlflow`.

        ```bash
        pip install mlflow azureml-mlflow
        ```

    - If you don't run code in an Azure Machine Learning compute instance, configure the MLflow tracking URI or the MLflow registry URI to point to the Azure Machine Learning workspace that you work on. For more information about how to connect MLflow to your workspace, see [Configure MLflow for Azure Machine Learning](how-to-use-mlflow-configure-tracking.md).

    # [Studio](#tab/studio)

    There are no other prerequisites when you work in Azure Machine Learning studio.

---

## About the example

The example shows you how to deploy an MLflow model to an online endpoint to perform predictions. The example uses an MLflow model that's based on the [Diabetes dataset](https://www4.stat.ncsu.edu/~boos/var.select/diabetes.html). This dataset contains 10 baseline variables: age, sex, body mass index, average blood pressure, and 6 blood serum measurements obtained from 442 diabetes patients. It also contains the response of interest, a quantitative measure of disease progression one year after the date of the baseline data.

The model was trained by using a `scikit-learn` regressor. All the required preprocessing has been packaged as a pipeline, so this model is an end-to-end pipeline that goes from raw data to predictions.

The information in this article is based on code samples from the [azureml-examples](https://github.com/azure/azureml-examples) repository. To run the commands locally without having to copy or paste YAML files and other files, use the following commands to clone the repository and go to the folder for your coding language:

    # [Azure CLI](#tab/cli)

    ```azurecli
    git clone https://github.com/Azure/azureml-examples --depth 1
    cd azureml-examples/cli
    ```

    # [Python (Azure Machine Learning SDK)](#tab/sdk)

    ```azurecli
    git clone https://github.com/Azure/azureml-examples --depth 1
    cd azureml-examples/sdk/python/endpoints/online/mlflow
    ```

    # [Python (MLflow SDK)](#tab/mlflow)

    ```azurecli
    git clone https://github.com/Azure/azureml-examples --depth 1
    cd azureml-examples/sdk/python/endpoints/online/mlflow
    ```

    # [Studio](#tab/studio)

    There's no need to clone the repository when you work in Azure Machine Learning studio.

---

### Follow along in Jupyter Notebook

To follow along with the steps in this article, see the [Deploy MLflow model to online endpoints](https://github.com/Azure/azureml-examples/blob/main/sdk/python/endpoints/online/mlflow/online-endpoints-deploy-mlflow-model.ipynb) notebook in the examples repository.

### Connect to your workspace

Connect to your Azure Machine Learning workspace:

# [Azure CLI](#tab/cli)

```azurecli
az account set --subscription <subscription-ID>
az configure --defaults workspace=<workspace-name> group=<resource-group-name> location=<location>
```

# [Python (Azure Machine Learning SDK)](#tab/sdk)

1. Import the required libraries:

    ```python
    from azure.ai.ml import MLClient, Input
    from azure.ai.ml.entities import (
    ManagedOnlineEndpoint,
    ManagedOnlineDeployment,
    Model,
    Environment,
    CodeConfiguration,
    )
    from azure.identity import DefaultAzureCredential
    from azure.ai.ml.constants import AssetTypes
    ```

2. Configure workspace details and get a handle to the workspace:

    ```python
    subscription_id = "<subscription>"
    resource_group = "<resource-group>"
    workspace = "<workspace>"
    
    ml_client = MLClient(DefaultAzureCredential(), subscription_id, resource_group, workspace)
    ```

# [Python (MLflow SDK)](#tab/mlflow)

1. Import the required libraries:

    ```python
    import json
    import mlflow
    import requests
    import pandas as pd
    from mlflow.deployments import get_deploy_client
    from mlflow.tracking import MlflowClient
    ```

1. Initialize the MLflow client:

    ```python
    mlflow_client = MlflowClient()
    ```

1. Configure the deployment client:

    ```python
    deployment_client = get_deploy_client(mlflow.get_tracking_uri())    
    ```

# [Studio](#tab/studio)

Go to [Azure Machine Learning studio](https://ml.azure.com).

---

### Register the model

You can deploy only registered models to online endpoints. In this case, you already have a local copy of the model in the repository, so you only need to publish the model to the registry in the workspace. You can skip this step if the model you want to deploy is already registered.

# [Azure CLI](#tab/cli)

```azurecli
MODEL_NAME='sklearn-diabetes'
az ml model create --name $MODEL_NAME --type "mlflow_model" --path "endpoints/online/ncd/sklearn-diabetes/model"
```

# [Python (Azure Machine Learning SDK)](#tab/sdk)

```python
model_name = 'sklearn-diabetes'
model_local_path = "sklearn-diabetes/model"
model = ml_client.models.create_or_update(
        Model(name=model_name, path=model_local_path, type=AssetTypes.MLFLOW_MODEL)
)
```

# [Python (MLflow SDK)](#tab/mlflow)

```python
model_name = 'sklearn-diabetes'
model_local_path = "sklearn-diabetes/model"

registered_model = mlflow_client.create_model_version(
    name=model_name, source=f"file://{model_local_path}"
)
version = registered_model.version
```

# [Studio](#tab/studio)

To create a model in Azure Machine Learning studio:

1. In the studio, select __Models__.
1. Select __Register__, and then select where your model is located. For this example, select __From local files__.
1. On the __Upload model__ page, under __Model type__, select __MLflow__.
1. Select __Browse__ to select the model folder, and then select __Next__.
1. On the __Model settings__ page, under __Name__, enter a name for the model, and then select __Next__.
1. On the __Review__ page, review the model files and model settings, and then select __Register__.

:::image type="content" source="media/how-to-deploy-mlflow-models-online-endpoints/register-model-in-studio.png" alt-text="Screenshot of the Review page in the studio. Five uploaded model files are listed, and model settings like the name are visible." lightbox="media/how-to-deploy-mlflow-models-online-endpoints/register-model-in-studio.png":::

---

#### What if your model was logged inside a run?

If your model was logged inside a run, you can register it directly.

To register the model, you need to know its storage location. If you use the MLflow `autolog` feature, the path to the model depends on the model type and framework. You should check the jobs output to identify the name of the model's folder. This folder contains a file named `MLModel`.

If you use the `log_model` method to manually log your models, pass the path to the model as the argument to the method. For example, if you use `mlflow.sklearn.log_model(my_model, "classifier")` to log the model, the path that the model is stored on is called `classifier`.

# [Azure CLI](#tab/cli)

Use the Azure Machine Learning CLI v2 to create a model from a training job output. In the following example, a model named `$MODEL_NAME` is registered using the artifacts of a job with ID `$RUN_ID`. The path where the model is stored is `$MODEL_PATH`.

```bash
az ml model create --name $MODEL_NAME --path azureml://jobs/$RUN_ID/outputs/artifacts/$MODEL_PATH
```

> [!NOTE]
> The path `$MODEL_PATH` is the location where the model has been stored in the run.

# [Python (Azure Machine Learning SDK)](#tab/sdk)

```python
model_name = 'sklearn-diabetes'

ml_client.models.create_or_update(
    Model(
        path=f"azureml://jobs/{RUN_ID}/outputs/artifacts/{MODEL_PATH}"
        name=model_name,
        type=AssetTypes.MLFLOW_MODEL
    )
) 
```

> [!NOTE]
> The path `MODEL_PATH` is the location where the model has been stored in the run.

# [Python (MLflow SDK)](#tab/mlflow)

```python
model_name = 'sklearn-diabetes'

registered_model = mlflow_client.create_model_version(
    name=model_name, source=f"runs://{RUN_ID}/{MODEL_PATH}"
)
version = registered_model.version
```

> [!NOTE]
> The path `MODEL_PATH` is the location where the model has been stored in the run.

# [Studio](#tab/studio)

:::image type="content" source="media/how-to-deploy-mlflow-models-online-endpoints/mlflow-register-model-output.gif" lightbox="media/how-to-deploy-mlflow-models-online-endpoints/mlflow-register-model-output.gif" alt-text="Screenshot showing how to download Outputs and logs from Experimentation run":::

---

## Deploy an MLflow model to an online endpoint

1. Use the following code to configure the name and authentication mode of the endpoint that you want to deploy the model to:

    # [Azure CLI](#tab/cli)

    Set an endpoint name by running the following command. First replace `YOUR_ENDPOINT_NAME` with a unique name.

    :::code language="azurecli" source="~/azureml-examples-main/cli/deploy-managed-online-endpoint-ncd.sh" ID="set_endpoint_name":::

    To configure your endpoint, create a YAML file named create-endpoint.yaml that contains the following lines:

    :::code language="yaml" source="~/azureml-examples-main/cli/endpoints/online/ncd/create-endpoint.yaml":::

    # [Python (Azure Machine Learning SDK)](#tab/sdk)

    ```python
    # To create a unique endpoint name, use a time stamp of the current date and time.
    import datetime

    endpoint_name = "sklearn-diabetes-" + datetime.datetime.now().strftime("%m%d%H%M%f")

    endpoint = ManagedOnlineEndpoint(
        name=endpoint_name,
        description="An online endpoint to generate predictions for the diabetes dataset",
        auth_mode="key",
        tags={"env": "dev"},
    )
    ```

    # [Python (MLflow SDK)](#tab/mlflow)

    You can use a configuration file to configure the properties of this endpoint. In this case, you configure the authentication mode of the endpoint to be `key`.
    
    ```python

    # To create a unique endpoint name, use a time stamp of the current date and time.
    import datetime
    
    endpoint_name = "sklearn-diabetes-" + datetime.datetime.now().strftime("%m%d%H%M%f")

    endpoint_config = {
        "auth_mode": "key",
        "identity": {
            "type": "system_assigned"
        }
    }
    ```

    Write this configuration information to a `JSON` file:

    ```python
    endpoint_config_path = "endpoint_config.json"
    with open(endpoint_config_path, "w") as outfile:
        outfile.write(json.dumps(endpoint_config))
    ```

    # [Studio](#tab/studio)

    You perform this step in the deployment stage.

1. Create the endpoint:
    
    # [Azure CLI](#tab/cli)
    
    :::code language="azurecli" source="~/azureml-examples-main/cli/deploy-managed-online-endpoint-ncd.sh" ID="create_endpoint":::

    # [Python (Azure Machine Learning SDK)](#tab/sdk)
    
    ```python
    ml_client.begin_create_or_update(endpoint)
    ```

    # [Python (MLflow SDK)](#tab/mlflow)

    ```python
    endpoint = deployment_client.create_endpoint(
        name=endpoint_name,
        config={"endpoint-config-file": endpoint_config_path},
    )
    ```

    # [Studio](#tab/studio)

    You perform this step in the deployment stage.

1. Configure the deployment. A deployment is a set of resources required for hosting the model that does the actual inferencing.
    
    # [Azure CLI](#tab/cli)

    Create a YAML file named sklearn-deployment.yaml that contains the following lines:

    :::code language="yaml" source="~/azureml-examples-main/cli/endpoints/online/ncd/sklearn-deployment.yaml":::

    # [Python (Azure Machine Learning SDK)](#tab/sdk)

    ```python
    blue_deployment = ManagedOnlineDeployment(
        name="blue",
        endpoint_name=endpoint_name,
        model=model,
        instance_type="Standard_F4s_v2",
        instance_count=1
    )
    ```

    Alternatively, if your endpoint doesn't have egress connectivity, use [model packaging (preview)](how-to-package-models.md) by including the argument `with_package=True`:

    ```python
    blue_deployment = ManagedOnlineDeployment(
        name="blue",
        endpoint_name=endpoint_name,
        model=model,
        instance_type="Standard_F4s_v2",
        instance_count=1,
        with_package=True,
    )
    ```

    # [Python (MLflow SDK)](#tab/mlflow)

    ```python
    blue_deployment_name = "blue"
    ```

    To configure the hardware requirements of your deployment, create a JSON file with the desired configuration:

    ```python
    deploy_config = {
        "instance_type": "Standard_F4s_v2",
        "instance_count": 1,
    }
    ```
    
    > [!NOTE]
    > For details about the full specification of this configuration, see [Managed online deployment schema (v2)](reference-yaml-deployment-managed-online.md).
    
    Write the configuration to a file:

    ```python
    deployment_config_path = "deployment_config.json"
    with open(deployment_config_path, "w") as outfile:
        outfile.write(json.dumps(deploy_config))
    ```

    # [Studio](#tab/studio)

    You perform this step in the deployment stage.

    ---
    
    > [!NOTE]
    > Autogeneration of the `scoring_script` and `environment` are only supported for the `pyfunc` model flavor. To use a different model flavor, see [Customizing MLflow model deployments](#customize-mlflow-model-deployments).

1. Create the deployment:
    
    # [Azure CLI](#tab/cli)
    
    :::code language="azurecli" source="~/azureml-examples-main/cli/deploy-managed-online-endpoint-ncd.sh" ID="create_sklearn_deployment":::

    If your endpoint doesn't have egress connectivity, use model packaging (preview) by including the flag `--with-package`:

    ```azurecli
    az ml online-deployment create --with-package --name sklearn-deployment --endpoint $ENDPOINT_NAME -f endpoints/online/ncd/sklearn-deployment.yaml --all-traffic
    ```

    # [Python (Azure Machine Learning SDK)](#tab/sdk)

    ```python
    ml_client.online_deployments.begin_create_or_update(blue_deployment)
    ```

    # [Python (MLflow SDK)](#tab/mlflow)

    ```python
    blue_deployment = deployment_client.create_deployment(
        name=blue_deployment_name,
        endpoint=endpoint_name,
        model_uri=f"models:/{model_name}/{version}",
        config={"deploy-config-file": deployment_config_path},
    )    
    ```

    # [Studio](#tab/studio)

    1. Select __Endpoints__. Go to the **Real-time endpoints** tab, and then select **Create**.

        :::image type="content" source="media/how-to-deploy-mlflow-models-online-endpoints/create-from-endpoints.png" lightbox="media/how-to-deploy-mlflow-models-online-endpoints/create-from-endpoints.png" alt-text="Screenshot showing create option on the Endpoints UI page.":::

    1. Select the MLflow model that you registered previously, and then select **Select**.
    
        > [!NOTE]
        > The configuration page includes a note to inform you that the scoring script and environment are automatically generated for your selected MLflow model.

    1. Under **Endpoint**, select **New** to deploy to a new endpoint.
    
    1. Under **Endpoint name**, enter a name for the endpoint or keep the default name.
    
    1. Under **Deployment name**, enter a name for the deployment or keep the default name.
    
    1. Select __Deploy__ to deploy the model to the endpoint.

        :::image type="content" source="media/how-to-deploy-mlflow-models-online-endpoints/deployment-wizard.png" lightbox="media/how-to-deploy-mlflow-models-online-endpoints/deployment-wizard.png" alt-text="Screenshot showing no code and environment needed for MLflow models.":::


1. Assign all the traffic to the deployment. So far, the endpoint has one deployment, but none of its traffic is assigned to it.

    # [Azure CLI](#tab/cli)
    
    This step isn't required in the Azure CLI if you use the `--all-traffic` flag during creation. If you need to change the traffic, you can use the `az ml online-endpoint update --traffic` command. For more information on how to update traffic, see [Progressively update traffic](how-to-deploy-mlflow-models-online-progressive.md#progressively-update-the-traffic).
    
    # [Python (Azure Machine Learning SDK)](#tab/sdk)
    
    ```python
    endpoint.traffic = {"blue": 100}
    ```
    
    # [Python (MLflow SDK)](#tab/mlflow)

    ```python
    traffic_config = {"traffic": {blue_deployment_name: 100}}
    ```

    Write the configuration to a file:

    ```python
    traffic_config_path = "traffic_config.json"
    with open(traffic_config_path, "w") as outfile:
        outfile.write(json.dumps(traffic_config))
    ```

    # [Studio](#tab/studio)

    This step isn't required in the studio.

1. Update the endpoint configuration:

    # [Azure CLI](#tab/cli)

    This step isn't required in the Azure CLI if you use the `--all-traffic` flag during creation. If you need to change traffic, you can use the `az ml online-endpoint update --traffic` command. For more information on how to update traffic, see [Progressively update traffic](how-to-deploy-mlflow-models-online-progressive.md#progressively-update-the-traffic).
    
    # [Python (Azure Machine Learning SDK)](#tab/sdk)
    
    ```python
    ml_client.begin_create_or_update(endpoint).result()
    ```
    
    # [Python (MLflow SDK)](#tab/mlflow)

    ```python
    deployment_client.update_endpoint(
        endpoint=endpoint_name,
        config={"endpoint-config-file": traffic_config_path},
    )
    ```

    # [Studio](#tab/studio)

    This step isn't required in the studio.

## Invoke the endpoint

When your deployment is ready, you can use it to serve requests. One way to test the deployment is by using the built-in invocation capability in the deployment client that you use. In the examples repository, the sample-request-sklearn.json file contains the following JSON code. You can use it as a sample request file for the deployment.

# [Azure CLI](#tab/cli)

:::code language="json" source="~/azureml-examples-main/cli/endpoints/online/ncd/sample-request-sklearn.json":::

# [Python (Azure Machine Learning SDK)](#tab/sdk)

:::code language="json" source="~/azureml-examples-main/sdk/python/endpoints/online/mlflow/sample-request-sklearn.json":::

# [Python (MLflow SDK)](#tab/mlflow)

:::code language="json" source="~/azureml-examples-main/sdk/python/endpoints/online/mlflow/sample-request-sklearn.json":::

# [Studio](#tab/studio)

:::code language="json" source="~/azureml-examples-main/cli/endpoints/online/ncd/sample-request-sklearn.json":::

---

> [!NOTE]
> This file uses the `input_data` key instead of `inputs`, which MLflow serving uses. Azure Machine Learning requires a different input format to be able to automatically generate the swagger contracts for the endpoints. For more information about expected input formats, see [Deployment in the MLflow built-in server vs. deployment in Azure Machine Learning inferencing server](how-to-deploy-mlflow-models.md#models-deployed-in-azure-machine-learning-vs-models-deployed-in-the-mlflow-built-in-server).

Submit a request to the endpoint:

# [Azure CLI](#tab/cli)

:::code language="azurecli" source="~/azureml-examples-main/cli/deploy-managed-online-endpoint-ncd.sh" ID="test_sklearn_deployment":::

# [Python (Azure Machine Learning SDK)](#tab/sdk)

```python
response = ml_client.online_endpoints.invoke(
    endpoint_name=endpoint_name,
    request_file="sample-request-sklearn.json",
)
```

# [Python (MLflow SDK)](#tab/mlflow)

```python
# Read the sample request that's in the json file to construct a pandas data frame
with open("sample-request-sklearn.json", "r") as f:
    sample_request = json.loads(f.read())
    samples = pd.DataFrame(**sample_request["input_data"])

deployment_client.predict(endpoint=endpoint_name, df=samples)
```

# [Studio](#tab/studio)

MLflow models can use the __Test__ tab to create invocations to the created endpoints:

1. Select __Endpoints__, and then select the endpoint that you created.
1. Go to the __Test__ tab.
1. In the __Input__ box, paste the contents of the cli/endpoints/online/ncd/sample-request-sklearn.json file.
1. Select __Test__.
1. The box on the right displays the predictions.

---

The response should be similar to the following text:

# [Azure CLI](#tab/cli)

```json
[ 
  11633.100167144921,
  8522.117402884991
]
```

# [Python (Azure Machine Learning SDK)](#tab/sdk)

```json
[ 
  11633.100167144921
]
```

# [Python (MLflow SDK)](#tab/mlflow)

```json
[ 
  11633.100167144921
]
```

# [Studio](#tab/studio)

```json
[ 
  11633.100167144921,
  8522.117402884991
]
```

---

> [!IMPORTANT]
> For MLflow no-code-deployment, **[testing via local endpoints](how-to-deploy-online-endpoints.md#deploy-and-debug-locally-by-using-a-local-endpoint)** is currently not supported.


## Customize MLflow model deployments

You don't have to specify a scoring script in the deployment definition of an MLflow model to an online endpoint. But you can specify a scoring script if you want to customize your inference process.

You typically want to customize your MLflow model deployment in the following cases:

- The model doesn't have a `PyFunc` flavor.
- You need to customize the way the model is run. For instance, you need to use `mlflow.<flavor>.load_model()` to use a specific flavor to load the model.
- You need to do preprocessing or postprocessing in your scoring routine when it's not done by the model itself.
- The output of the model can't be nicely represented in tabular data. For instance, it's a tensor representing an image.

> [!IMPORTANT]
> If you choose to specify a scoring script for an MLflow model deployment, you also have to specify the environment where the deployment runs.

### Steps

To deploy an MLflow model with a custom scoring script:

1. Identify the folder that contains your MLflow model:
    1 Go to [Azure Machine Learning studio](https://ml.azure.com).
    1. Go to the __Models__ section.
    1. Select the model that you want to deploy and go to its __Artifacts__ tab.
    1. Take note of the folder that's displayed. You specified this folder when you registered the model.

    :::image type="content" source="media/how-to-deploy-mlflow-models-online-endpoints/mlflow-model-folder-name.png" lightbox="media/how-to-deploy-mlflow-models-online-endpoints/mlflow-model-folder-name.png" alt-text="Screenshot showing the folder where the model artifacts are placed.":::

1. Create a scoring script. The following script, score.py, provides an example of how to perform inference with an MLflow model. You can adapt this script to your needs or change any of its parts to reflect your scenario. Notice that the folder name that you previously identified, `model`, is included in the `init()` function.

    :::code language="python" source="~/azureml-examples-main/cli/endpoints/online/ncd/sklearn-diabetes/src/score.py" highlight="14":::

    > [!WARNING]
    > __MLflow 2.0 advisory__: The example scoring script works with MLflow 1.X and MLflow 2.X. However, the expected input and output formats on those versions can vary. Check your environment definition to see which MLflow version you use. MLflow 2.0 is only supported in Python 3.8 and later versions.

1. Create an environment that you can run the scoring script in. Because the model is an MLflow model, the conda requirements are also specified in the model package. For more details about the files included in an MLflow model, see [The MLmodel format](concept-mlflow-models.md#the-mlmodel-format). You build the environment by using the conda dependencies from the file. However, you need to also include the `azureml-inference-server-http` package, which is required for online deployments in Azure Machine Learning.
    
    You can create a conda definition file named conda.yaml that contains the following lines:

    :::code language="yaml" source="~/azureml-examples-main/cli/endpoints/online/ncd/sklearn-diabetes/environment/conda.yaml":::

    > [!NOTE]
    > The `azureml-inference-server-http` package has been added to the original conda dependencies file.

    Use this conda dependencies file to create the environment:

    # [Azure CLI](#tab/cli)
    
    The environment is created inline in the deployment configuration.
    
    # [Python (Azure Machine Learning SDK)](#tab/sdk)
    
    ```pythonS
    environment = Environment(
        conda_file="sklearn-diabetes/environment/conda.yaml",
        image="mcr.microsoft.com/azureml/openmpi4.1.0-ubuntu22.04:latest",
    )
    ```

    # [Python (MLflow SDK)](#tab/mlflow)

    This operation isn't supported in the MLflow SDK.

    # [Studio](#tab/studio)

    1. On the side menu, select __Environments__.
    1. Select __Custom environments__ > __Create__.
    1. Enter the name of the environment, in this case `sklearn-mlflow-online-py37`.
    1. For __Select environment source__, select __Use existing docker image with optional conda file__.
    1. For __Container registry image path__, enter `mcr.microsoft.com/azureml/openmpi4.1.0-ubuntu22.04`.
    1. Select __Next__ to go to the __Customize__ section.
    1. Copy the content of the `sklearn-diabetes/environment/conda.yml` file and paste it in the text box. 
    1. Select __Next__ to go to the __Tags__ page, and then select __Next__ again.
    1. On the __Review__ page, select __Create__. The environment is ready for use.
    ---

1. Create the deployment:

    # [Azure CLI](#tab/cli)

    In the endpoints/online/ncd folder, create a deployment configuration file, __deployment.yml__, that contains the following lines:

    ```yaml
    $schema: https://azuremlschemas.azureedge.net/latest/managedOnlineDeployment.schema.json
    name: sklearn-diabetes-custom
    endpoint_name: my-endpoint
    model: azureml:sklearn-diabetes@latest
    environment: 
      image: mcr.microsoft.com/azureml/openmpi4.1.0-ubuntu22.04
      conda_file: sklearn-diabetes/environment/conda.yaml
    code_configuration:
      code: sklearn-diabetes/src
      scoring_script: score.py
    instance_type: Standard_F2s_v2
    instance_count: 1
    ```

    Create the deployment:

    ```azurecli
    az ml online-deployment create -f endpoints/online/ncd/deployment.yml
    ```
    
    # [Python (Azure Machine Learning SDK)](#tab/sdk)
    
    ```python
    blue_deployment = ManagedOnlineDeployment(
        name="blue",
        endpoint_name=endpoint_name,
        model=model,
        environment=environment,
        code_configuration=CodeConfiguration(
            code="sklearn-diabetes/src",
            scoring_script="score.py"
        ),
        instance_type="Standard_F4s_v2",
        instance_count=1,
    )

    ml_client.online_deployments.begin_create_or_update(blue_deployment)

    ```

    # [Python (MLflow SDK)](#tab/mlflow)

    This operation isn't supported in the MLflow SDK.

    # [Studio](#tab/studio)

    1. On the __Endpoints__ page, Select **+Create**.
    1. Select the MLflow model that you registered previously.
    1. In the endpoint creation wizard, select __More options__ to open up advanced options.

        :::image type="content" source="media/how-to-deploy-mlflow-models-online-endpoints/select-advanced-deployment-options.png" lightbox="media/how-to-deploy-mlflow-models-online-endpoints/select-advanced-deployment-options.png" alt-text="Screenshot showing how to select advanced deployment options when creating an endpoint."::: 

    1. Provide a name and authentication type for the endpoint, and then select __Next__ to see that the model you selected is being used for your deployment.
    1. Select __Next__ to continue to the ___Deployment__ page.
    1. Select __Next__ to go to the __Code + environment__ page.
    1. Select the slider next to __Customize environment and scoring script__.

        :::image type="content" source="media/how-to-deploy-mlflow-models-online-endpoints/configure-scoring-script-mlflow.png" lightbox="media/how-to-deploy-mlflow-models-online-endpoints/configure-scoring-script-mlflow.png" alt-text="Screenshot showing how to indicate an environment and scoring script for MLflow models.":::

    1. Browse to select the scoring script you created previously.
    1. For the environment type, select __Custom environments__.
    1. Select the custom environment you created previously, and then select __Next__.
    1. Complete the wizard to deploy the model to the endpoint.

    ---

1. When your deployment is complete, it's ready to serve requests. One way to test the deployment is to use the `invoke` method with a sample request file such as the following file, sample-request-sklearn.json:
    
    # [Azure CLI](#tab/cli)

    :::code language="json" source="~/azureml-examples-main/cli/endpoints/online/ncd/sample-request-sklearn.json":::
    
    # [Python (Azure Machine Learning SDK)](#tab/sdk)
    
    :::code language="json" source="~/azureml-examples-main/sdk/python/endpoints/online/mlflow/sample-request-sklearn.json":::

    # [Python (MLflow SDK)](#tab/mlflow)

    This operation isn't supported in the MLflow SDK.

    # [Studio](#tab/studio)

    :::code language="json" source="~/azureml-examples-main/cli/endpoints/online/ncd/sample-request-sklearn.json":::

    ---
    
    Submit a request to the endpoint:
    
    # [Azure CLI](#tab/cli)

    :::code language="azurecli" source="~/azureml-examples-main/cli/deploy-managed-online-endpoint-ncd.sh" ID="test_sklearn_deployment":::
    
    # [Python (Azure Machine Learning SDK)](#tab/sdk)
    
    ```python
    response = ml_client.online_endpoints.invoke(
        endpoint_name=endpoint_name,
        deployment_name=deployment.name,
        request_file="sample-request-sklearn.json",
    )
    ```

    # [Python (MLflow SDK)](#tab/mlflow)

    This operation isn't supported in the MLflow SDK.

    # [Studio](#tab/studio)

    1. Select __Endpoints__, and then select the endpoint that you created.
    1. Go to the __Test__ tab.
    1. In the __Input__ box, paste the contents of the cli/endpoints/online/ncd/sample-request-sklearn.json file.
    1. Select __Test__.
    1. The box on the right displays the predictions.

    ---
    
    The response should be similar to the following text:
    
    # [Azure CLI](#tab/cli)

    ```json
    {
      "predictions": [ 
        1095.2797413413252,
        1134.585328803727
      ]
    }
    ```
    
    # [Python (Azure Machine Learning SDK)](#tab/sdk)
    
    ```json
    {
      "predictions": [ 
        1095.2797413413252
      ]
    }
    ```

    # [Python (MLflow SDK)](#tab/mlflow)

    This operation isn't supported in the MLflow SDK.

    # [Studio](#tab/studio)

    ```json
    {
      "predictions": [ 
        1095.2797413413252,
        1134.585328803727
      ]
    }
    ```

    ---

    > [!WARNING]
    > __MLflow 2.0 advisory__: In MLflow 1.X, the response doesn't contain the `predictions` key.


## Clean up resources

If you no longer need the endpoint, delete its associated resources:

# [Azure CLI](#tab/cli)

:::code language="azurecli" source="~/azureml-examples-main/cli/deploy-managed-online-endpoint-ncd.sh" ID="delete_endpoint":::

# [Python (Azure Machine Learning SDK)](#tab/sdk)

```python
ml_client.online_endpoints.begin_delete(endpoint_name)
```

# [Python (MLflow SDK)](#tab/mlflow)

```python
deployment_client.delete_endpoint(endpoint_name)
```

# [Studio](#tab/studio)

1. In the studio, go to the __Endpoints__ tab.
1. Select the __Real-time endpoints__ tab.
1. Select the endpoint that you want to delete.
1. Select __Delete__. The endpoint and all its deployments are deleted.

---

## Related content

- [Deploy models with REST](how-to-deploy-with-rest.md)
- [Safe rollout for online endpoints](how-to-safely-rollout-online-endpoints.md)
- [Troubleshoot online endpoint deployment](how-to-troubleshoot-managed-online-endpoints.md)
