---
title: Deploy a model in a custom container to an online endpoint
titleSuffix: Azure Machine Learning
description: Learn how to use a custom container with an open-source server to deploy a model in Azure Machine Learning.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: inferencing
author: msakande
ms.author: mopeakande
ms.reviewer: sehan
ms.date: 03/26/2024
ms.topic: how-to
ms.custom: deploy, devplatv2, devx-track-azurecli, cliv2, sdkv2
ms.devlang: azurecli
---

# Use a custom container to deploy a model to an online endpoint

[!INCLUDE [dev v2](includes/machine-learning-dev-v2.md)]

In Azure Machine Learning, you can use a custom container to deploy a model to an online endpoint.

Custom container deployments can use web servers other than the default Python Flask server that Azure Machine Learning uses. When you use a custom deployment, you can still take advantage of the built-in monitoring, scaling, alerting, and authentication that Azure Machine Learning offers.

The following table lists various [deployment examples](https://github.com/Azure/azureml-examples/tree/main/cli/endpoints/online/custom-container) that use custom containers. The examples use various tools and technologies, such as TensorFlow Serving, TorchServe, Triton Inference Server, the Plumber R package, and the Azure Machine Learning inference minimal image.

|Example|Script (CLI)|Description|
|-------|------|---------|
|[minimal/multimodel](https://github.com/Azure/azureml-examples/blob/main/cli/endpoints/online/custom-container/minimal/multimodel)|[deploy-custom-container-minimal-multimodel](https://github.com/Azure/azureml-examples/blob/main/cli/deploy-custom-container-minimal-multimodel.sh)|Deploys multiple models to a single deployment by extending the Azure Machine Learning inference minimal image.|
|[minimal/single-model](https://github.com/Azure/azureml-examples/blob/main/cli/endpoints/online/custom-container/minimal/single-model)|[deploy-custom-container-minimal-single-model](https://github.com/Azure/azureml-examples/blob/main/cli/deploy-custom-container-minimal-single-model.sh)|Deploys a single model by extending the Azure Machine Learning inference minimal image.|
|[mlflow/multideployment-scikit](https://github.com/Azure/azureml-examples/blob/main/cli/endpoints/online/custom-container/mlflow/multideployment-scikit)|[deploy-custom-container-mlflow-multideployment-scikit](https://github.com/Azure/azureml-examples/blob/main/cli/deploy-custom-container-mlflow-multideployment-scikit.sh)|Deploys two MLFlow models with different Python requirements to two separate deployments behind a single endpoint. Uses the Azure Machine Learning inference minimal image.|
|[r/multimodel-plumber](https://github.com/Azure/azureml-examples/blob/main/cli/endpoints/online/custom-container/r/multimodel-plumber)|[deploy-custom-container-r-multimodel-plumber](https://github.com/Azure/azureml-examples/blob/main/cli/deploy-custom-container-r-multimodel-plumber.sh)|Deploys three regression models to one endpoint. Uses the Plumber R package.|
|[tfserving/half-plus-two](https://github.com/Azure/azureml-examples/blob/main/cli/endpoints/online/custom-container/tfserving/half-plus-two)|[deploy-custom-container-tfserving-half-plus-two](https://github.com/Azure/azureml-examples/blob/main/cli/deploy-custom-container-tfserving-half-plus-two.sh)|Deploys a Half Plus Two model by using a TensorFlow Serving custom container. Uses the standard model registration process.|
|[tfserving/half-plus-two-integrated](https://github.com/Azure/azureml-examples/blob/main/cli/endpoints/online/custom-container/tfserving/half-plus-two-integrated)|[deploy-custom-container-tfserving-half-plus-two-integrated](https://github.com/Azure/azureml-examples/blob/main/cli/deploy-custom-container-tfserving-half-plus-two-integrated.sh)|Deploys a Half Plus Two model by using a TensorFlow Serving custom container with the model integrated into the image.|
|[torchserve/densenet](https://github.com/Azure/azureml-examples/blob/main/cli/endpoints/online/custom-container/torchserve/densenet)|[deploy-custom-container-torchserve-densenet](https://github.com/Azure/azureml-examples/blob/main/cli/deploy-custom-container-torchserve-densenet.sh)|Deploys a single model by using a TorchServe custom container.|
|[triton/single-model](https://github.com/Azure/azureml-examples/blob/main/cli/endpoints/online/custom-container/triton/single-model)|[deploy-custom-container-triton-single-model](https://github.com/Azure/azureml-examples/blob/main/cli/deploy-custom-container-triton-single-model.sh)|Deploys a Triton model by using a custom container.|

This article focuses on serving a TensorFlow model with TensorFlow (TF) Serving.

> [!WARNING]
> Microsoft might not be able to help troubleshoot problems caused by a custom image. If you encounter problems, you might be asked to use the default image or one of the images Microsoft provides to see if the problem is specific to your image.

## Prerequisites

[!INCLUDE [cli & sdk](includes/machine-learning-cli-sdk-v2-prereqs.md)]

* You, or the service principal you use, must have *Contributor* access to the Azure resource group that contains your workspace. You have such a resource group if you configured your workspace using the quickstart article.

* To deploy locally, you must have [Docker engine](https://docs.docker.com/engine/install/) running locally. This step is **highly recommended**. It helps you debug issues.

## Download the source code

To follow along with the steps in this article, clone the source code from GitHub.

# [Azure CLI](#tab/cli)

```azurecli
git clone https://github.com/Azure/azureml-examples --depth 1
cd azureml-examples/cli
```

# [Python SDK](#tab/python)

```azurecli
git clone https://github.com/Azure/azureml-examples --depth 1
cd azureml-examples/sdk/python
```

See also [the example notebook](https://github.com/Azure/azureml-examples/blob/main/sdk/python/endpoints/online/custom-container/online-endpoints-custom-container.ipynb), but note that `3. Test locally` section in the notebook assumes that it runs under the `azureml-examples/sdk` directory.

---

## Initialize environment variables

Define environment variables:

:::code language="azurecli" source="~/azureml-examples-main/cli/deploy-custom-container-tfserving-half-plus-two.sh" id="initialize_variables":::

## Download a TensorFlow model

Download and unzip a model that divides an input by two and adds 2 to the result:

:::code language="azurecli" source="~/azureml-examples-main/cli/deploy-custom-container-tfserving-half-plus-two.sh" id="download_and_unzip_model":::

## Run a TF Serving image locally to test that it works

Use docker to run your image locally for testing:

:::code language="azurecli" source="~/azureml-examples-main/cli/deploy-custom-container-tfserving-half-plus-two.sh" id="run_image_locally_for_testing":::

### Check that you can send liveness and scoring requests to the image

First, check that the container is *alive*, meaning that the process inside the container is still running. You should get a 200 (OK) response.

:::code language="azurecli" source="~/azureml-examples-main/cli/deploy-custom-container-tfserving-half-plus-two.sh" id="check_liveness_locally":::

Then, check that you can get predictions about unlabeled data:

:::code language="azurecli" source="~/azureml-examples-main/cli/deploy-custom-container-tfserving-half-plus-two.sh" id="check_scoring_locally":::

### Stop the image

Now that you tested locally, stop the image:

:::code language="azurecli" source="~/azureml-examples-main/cli/deploy-custom-container-tfserving-half-plus-two.sh" id="stop_image":::

## Deploy your online endpoint to Azure

Next, deploy your online endpoint to Azure.

# [Azure CLI](#tab/cli)

### Create YAML files for your endpoint and deployment

You can configure your cloud deployment by using YAML. For instance, to configure your endpoint, you can create a YAML file named tfserving-endpoint.yml that contains the following lines:

:::code language="yaml" source="~/azureml-examples-main/cli/endpoints/online/custom-container/tfserving/half-plus-two/tfserving-endpoint.yml":::

To configure your deployment, you can create a YAML file named tfserving-deployment.yml that contains the following lines:

```yml
$schema: https://azuremlschemas.azureedge.net/latest/managedOnlineDeployment.schema.json
name: tfserving-deployment
endpoint_name: tfserving-endpoint
model:
  name: tfserving-mounted
  version: <model-version>
  path: ./half_plus_two
environment_variables:
  MODEL_BASE_PATH: /var/azureml-app/azureml-models/tfserving-mounted/<model-version>
  MODEL_NAME: half_plus_two
environment:
  #name: tfserving
  #version: 1
  image: docker.io/tensorflow/serving:latest
  inference_config:
    liveness_route:
      port: 8501
      path: /v1/models/half_plus_two
    readiness_route:
      port: 8501
      path: /v1/models/half_plus_two
    scoring_route:
      port: 8501
      path: /v1/models/half_plus_two:predict
instance_type: Standard_DS3_v2
instance_count: 1
```

# [Python SDK](#tab/python)

### Connect to Azure Machine Learning workspace

Connect to your Azure Machine Learning workspace, configure workspace details, and get a handle to the workspace as follows:

1. Import the required libraries:

```python
# import required libraries
from azure.ai.ml import MLClient
from azure.ai.ml.entities import (
   ManagedOnlineEndpoint,
   ManagedOnlineDeployment,
   Model,
   Environment,
   CodeConfiguration,
)
from azure.identity import DefaultAzureCredential
```

2. Configure workspace details and get a handle to the workspace:

```python
# enter details of your Azure Machine Learning workspace
subscription_id = "<SUBSCRIPTION_ID>"
resource_group = "<RESOURCE_GROUP>"
workspace = "<AZUREML_WORKSPACE_NAME>"

# get a handle to the workspace
ml_client = MLClient(
   DefaultAzureCredential(), subscription_id, resource_group, workspace
)
```

For more information, see [Deploy machine learning models to managed online endpoint using Python SDK v2](how-to-deploy-managed-online-endpoint-sdk-v2.md).

### Configure online endpoint

> [!TIP]
> * `name`: The name of the endpoint. It must be unique in the Azure region. The name for an endpoint must start with an upper- or lowercase letter and only consist of '-'s and alphanumeric characters. For more information on the naming rules, see [endpoint limits](how-to-manage-quotas.md#azure-machine-learning-online-endpoints-and-batch-endpoints).
> * `auth_mode` : Use `key` for key-based authentication. Use `aml_token` for Azure Machine Learning token-based authentication. A `key` doesn't expire, but `aml_token` does expire. For more information on authenticating, see [Authenticate to an online endpoint](how-to-authenticate-online-endpoint.md).

Optionally, you can add description, tags to your endpoint.

```python
# Creating a unique endpoint name with current datetime to avoid conflicts
import datetime

online_endpoint_name = "endpoint-" + datetime.datetime.now().strftime("%m%d%H%M%f")

# create an online endpoint
endpoint = ManagedOnlineEndpoint(
    name=online_endpoint_name,
    description="this is a sample online endpoint",
    auth_mode="key",
    tags={"foo": "bar"},
)
```

### Configure online deployment

A deployment is a set of resources required for hosting the model that does the actual inferencing. Create a deployment for our endpoint using the `ManagedOnlineDeployment` class.

> [!TIP]
> - `name` - Name of the deployment.
> - `endpoint_name` - Name of the endpoint to create the deployment under.
> - `model` - The model to use for the deployment. This value can be either a reference to an existing versioned > model in the workspace or an inline model specification.
> - `environment` - The environment to use for the deployment. This value can be either a reference to an existing > versioned environment in the workspace or an inline environment specification.
> - `code_configuration` - the configuration for the source code and scoring script
>     - `path`- Path to the source code directory for scoring the model
>     - `scoring_script` - Relative path to the scoring file in the source code directory
> - `instance_type` - The VM size to use for the deployment. For the list of supported sizes, see [endpoints SKU list](reference-managed-online-endpoints-vm-sku-list.md).
> - `instance_count` - The number of instances to use for the deployment

```python
# create a blue deployment
model = Model(name="tfserving-mounted", version="1", path="half_plus_two")

env = Environment(
    image="docker.io/tensorflow/serving:latest",
    inference_config={
        "liveness_route": {"port": 8501, "path": "/v1/models/half_plus_two"},
        "readiness_route": {"port": 8501, "path": "/v1/models/half_plus_two"},
        "scoring_route": {"port": 8501, "path": "/v1/models/half_plus_two:predict"},
    },
)

blue_deployment = ManagedOnlineDeployment(
    name="blue",
    endpoint_name=online_endpoint_name,
    model=model,
    environment=env,
    environment_variables={
        "MODEL_BASE_PATH": "/var/azureml-app/azureml-models/tfserving-mounted/1",
        "MODEL_NAME": "half_plus_two",
    },
    instance_type="Standard_DS2_v2",
    instance_count=1,
)
```

---

There are a few important concepts to note in this YAML/Python parameter:

#### Base image

The base image is specified as a parameter in environment, and `docker.io/tensorflow/serving:latest` is used in this example. As you inspect the container, you can find that this server uses `ENTRYPOINT` to start an entry point script, which takes the environment variables such as `MODEL_BASE_PATH` and `MODEL_NAME`, and exposes ports such as `8501`. These details are all specific information for this chosen server. You can use this understanding of the server, to determine how to define the deployment. For example, if you set environment variables for `MODEL_BASE_PATH` and `MODEL_NAME` in the deployment definition, the server (in this case, TF Serving) will take the values to initiate the server. Likewise, if you set the port for the routes to be `8501` in the deployment definition, the user request to such routes will be correctly routed to the TF Serving server.

Note that this specific example is based on the TF Serving case, but you can use any containers that will stay up and respond to requests coming to liveness, readiness, and scoring routes. You can refer to other examples and see how the dockerfile is formed (for example, using `CMD` instead of `ENTRYPOINT`) to create the containers.

#### Inference config

Inference config is a parameter in environment, and it specifies the port and path for 3 types of the route: liveness, readiness, and scoring route. Inference config is required if you want to run your own container with managed online endpoint.

#### Readiness route vs liveness route

The API server you choose may provide a way to check the status of the server. There are two types of the route that you can specify: _liveness_ and _readiness_. A liveness route is used to check whether the server is running. A readiness route is used to check whether the server is ready to do work. In the context of machine learning inferencing, a server could respond 200 OK to a liveness request before loading a model, and the server could respond 200 OK to a readiness request only after the model is loaded into the memory.

For more information about liveness and readiness probes in general, see the [Kubernetes documentation](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/).

The liveness and readiness routes will be determined by the API server of your choice, as you would have identified when testing the container locally in earlier step. Note that the example deployment in this article uses the same path for both liveness and readiness, since TF Serving only defines a liveness route. Refer to other examples for different patterns to define the routes.

#### Scoring route

The API server you choose would provide a way to receive the payload to work on. In the context of machine learning inferencing, a server would receive the input data via a specific route. Identify this route for your API server as you test the container locally in earlier step, and specify it when you define the deployment to create.
Note that the successful creation of the deployment will update the scoring_uri parameter of the endpoint as well, which you can verify with `az ml online-endpoint show -n <name> --query scoring_uri`.

#### Locate the mounted model

When you deploy a model as an online endpoint, Azure Machine Learning *mounts* your model to your endpoint. When the model is mounted, you can deploy new versions of the model without having to create a new Docker image. By default, a model registered with the name *my-model* and version *1* is located on the following path inside your deployed container: */var/azureml-app/azureml-models/my-model/1*.

For example, consider the following setup:

- A directory structure on your local machine of /azureml-examples/cli/endpoints/online/custom-container
- A model name of `half_plus_two`

:::image type="content" source="./media/how-to-deploy-custom-container/local-directory-structure.png" alt-text="Diagram showing a tree view of the local directory structure.":::

# [Azure CLI](#tab/cli)

Suppose your tfserving-deployment.yml file contains the following lines in its `model` section. Note that in this section, the `name` value refers to the name that you use to register the model in Azure Machine Learning.

```yaml
model:
    name: tfserving-mounted
    version: 1
    path: ./half_plus_two
```

# [Python SDK](#tab/python)

Suppose you use the following code to create a `Model` class. Note that in this code, the `name` value refers to the name that you use to register the model in Azure Machine Learning.

```python
model = Model(name="tfserving-mounted", version="1", path="half_plus_two")
```

---

In this case, when you create a deployment, your model is located under the following folder: /var/azureml-app/azureml-models/tfserving-mounted/1.

:::image type="content" source="./media/how-to-deploy-custom-container/deployment-location.png" alt-text="Diagram showing a tree view of the deployment directory structure.":::

You can optionally configure your `model_mount_path` value. By adjusting this setting, you can change the path where the model is mounted.

> [!IMPORTANT]
> The `model_mount_path` value must be a valid absolute path in Linux (the OS of the container image).

When you change the value of `model_mount_path`, you also need to update the `MODEL_BASE_PATH` environment variable. Set `MODEL_BASE_PATH` to the same value as `model_mount_path` to avoid a failed deployment due to an error about the base path not being found.

# [Azure CLI](#tab/cli)

For example, you can add the `model_mount_path` parameter to your tfserving-deployment.yml file. You can also update the `MODEL_BASE_PATH` value in that file:

```YAML
name: tfserving-deployment
endpoint_name: tfserving-endpoint
model:
  name: tfserving-mounted
  version: 1
  path: ./half_plus_two
model_mount_path: /var/tfserving-model-mount
environment_variables:
  MODEL_BASE_PATH: /var/tfserving-model-mount
...
```

# [Python SDK](#tab/python)

For example, you can add the `model_mount_path` parameter to your `ManagedOnlineDeployment` class. You can also update the `MODEL_BASE_PATH` value in that code:

```python
blue_deployment = ManagedOnlineDeployment(
    name="blue",
    endpoint_name=online_endpoint_name,
    model=model,
    environment=env,
    model_mount_path="/var/tfserving-model-mount",
    environment_variables={
        "MODEL_BASE_PATH": "/var/tfserving-model-mount",
    ...
)
```

---

Then in your deployment, your model is located at /var/tfserving-model-mount/tfserving-mounted/1. It's no longer under azureml-app/azureml-models, but under the mount path that you specify:

:::image type="content" source="./media/how-to-deploy-custom-container/mount-path-deployment-location.png" alt-text="Diagram showing a tree view of the deployment directory structure when using mount_model_path.":::

### Create your endpoint and deployment

# [Azure CLI](#tab/cli)

Now that you understand how the YAML file is constructed, create your endpoint.

```azurecli
az ml online-endpoint create --name tfserving-endpoint -f endpoints/online/custom-container/tfserving/half-plus-two/tfserving-endpoint.yml
```

Create your deployment. This step might run for a few minutes.

```azurecli
az ml online-deployment create --name tfserving-deployment -f endpoints/online/custom-container/tfserving/half-plus-two/tfserving-deployment.yml --all-traffic
```

# [Python SDK](#tab/python)

Use the instance of `MLClient` that you created earlier to create the endpoint in the workspace. This code starts the endpoint creation and returns a confirmation response while the endpoint creation continues.

```python
ml_client.begin_create_or_update(endpoint)
```

Create the deployment by running the following code:

```python
ml_client.begin_create_or_update(blue_deployment)
```

---

### Invoke the endpoint

After your deployment is complete, make a scoring request to the deployed endpoint.

# [Azure CLI](#tab/cli)

:::code language="azurecli" source="~/azureml-examples-main/cli/deploy-custom-container-tfserving-half-plus-two.sh" id="invoke_endpoint":::

# [Python SDK](#tab/python)

Use the instance of `MLClient` that you created earlier to get a handle to the endpoint. Then use the `invoke` method and the following parameters to invoke the endpoint:

- `endpoint_name`: The name of the endpoint
- `request_file`: The file that contains the request data
- `deployment_name`: The name of the deployment to test in the endpoint

For the request data, you can use a sample JSON file from the [example repository](https://github.com/Azure/azureml-examples/tree/main/sdk/python/endpoints/online/custom-container).

```python
# Test the blue deployment by using some sample data.
response = ml_client.online_endpoints.invoke(
    endpoint_name=online_endpoint_name,
    deployment_name="blue",
    request_file="sample-request.json",
)
```

---

### Delete the endpoint

Now that you successfully scored with your endpoint, you can delete it:

# [Azure CLI](#tab/cli)

```azurecli
az ml online-endpoint delete --name tfserving-endpoint
```

# [Python SDK](#tab/python)

```python
ml_client.online_endpoints.begin_delete(name=online_endpoint_name)
```

---

## Related content

- [Safe rollout for online endpoints](how-to-safely-rollout-online-endpoints.md)
- [Troubleshooting online endpoints deployment](./how-to-troubleshoot-online-endpoints.md)
- [Torch serve sample](https://github.com/Azure/azureml-examples/blob/main/cli/deploy-custom-container-torchserve-densenet.sh)
