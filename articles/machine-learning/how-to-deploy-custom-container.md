---
title: Deploy a model in a custom container to an online endpoint
titleSuffix: Azure Machine Learning
description: See how to use a custom container with an open-source server to deploy a model in Azure Machine Learning.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: inferencing
author: s-polly
ms.author: scottpolly
ms.reviewer: jturuk
ms.date: 03/31/2025
ms.topic: how-to
ms.custom: deploy, devplatv2, devx-track-azurecli, cliv2, sdkv2
ms.devlang: azurecli
# customer intent: As a developer, I want to see how to use a custom container to deploy a model to an online endpoint so that I can use a variety of web servers to serve machine learning models.
---

# Use a custom container to deploy a model to an online endpoint

[!INCLUDE [dev v2](includes/machine-learning-dev-v2.md)]

In Azure Machine Learning, you can use a custom container to deploy a model to an online endpoint. Custom container deployments can use web servers other than the default Python Flask server that Azure Machine Learning uses.

When you use a custom deployment, you can:

- Use various tools and technologies, such as TensorFlow Serving (TF Serving), TorchServe, Triton Inference Server, the Plumber R package, and the Azure Machine Learning inference minimal image.
- Still take advantage of the built-in monitoring, scaling, alerting, and authentication that Azure Machine Learning offers.

This article shows you how to use a TF Serving image to serve a TensorFlow model.

## Prerequisites

[!INCLUDE [cli & sdk](includes/machine-learning-cli-sdk-v2-prereqs.md)]

* An Azure resource group that contains your workspace and that you or your service principal have Contributor access to. If you use the steps in [Create the workspace](quickstart-create-resources.md#create-the-workspace) to configure your workspace, you meet this requirement.

* [Docker Engine](https://docs.docker.com/engine/install/), installed and running locally. This prerequisite is **highly recommended**. You need it to deploy a model locally, and it's helpful for debugging.

## Deployment examples

The following table lists [deployment examples](https://github.com/Azure/azureml-examples/tree/main/cli/endpoints/online/custom-container) that use custom containers and take advantage of various tools and technologies.

|Example|Azure CLI script|Description|
|-------|------|---------|
|[minimal/multimodel](https://github.com/Azure/azureml-examples/blob/main/cli/endpoints/online/custom-container/minimal/multimodel)|[deploy-custom-container-minimal-multimodel](https://github.com/Azure/azureml-examples/blob/main/cli/deploy-custom-container-minimal-multimodel.sh)|Deploys multiple models to a single deployment by extending the Azure Machine Learning inference minimal image.|
|[minimal/single-model](https://github.com/Azure/azureml-examples/blob/main/cli/endpoints/online/custom-container/minimal/single-model)|[deploy-custom-container-minimal-single-model](https://github.com/Azure/azureml-examples/blob/main/cli/deploy-custom-container-minimal-single-model.sh)|Deploys a single model by extending the Azure Machine Learning inference minimal image.|
|[mlflow/multideployment-scikit](https://github.com/Azure/azureml-examples/blob/main/cli/endpoints/online/custom-container/mlflow/multideployment-scikit)|[deploy-custom-container-mlflow-multideployment-scikit](https://github.com/Azure/azureml-examples/blob/main/cli/deploy-custom-container-mlflow-multideployment-scikit.sh)|Deploys two MLFlow models with different Python requirements to two separate deployments behind a single endpoint. Uses the Azure Machine Learning inference minimal image.|
|[r/multimodel-plumber](https://github.com/Azure/azureml-examples/blob/main/cli/endpoints/online/custom-container/r/multimodel-plumber)|[deploy-custom-container-r-multimodel-plumber](https://github.com/Azure/azureml-examples/blob/main/cli/deploy-custom-container-r-multimodel-plumber.sh)|Deploys three regression models to one endpoint. Uses the Plumber R package.|
|[tfserving/half-plus-two](https://github.com/Azure/azureml-examples/blob/main/cli/endpoints/online/custom-container/tfserving/half-plus-two)|[deploy-custom-container-tfserving-half-plus-two](https://github.com/Azure/azureml-examples/blob/main/cli/deploy-custom-container-tfserving-half-plus-two.sh)|Deploys a Half Plus Two model by using a TF Serving custom container. Uses the standard model registration process.|
|[tfserving/half-plus-two-integrated](https://github.com/Azure/azureml-examples/blob/main/cli/endpoints/online/custom-container/tfserving/half-plus-two-integrated)|[deploy-custom-container-tfserving-half-plus-two-integrated](https://github.com/Azure/azureml-examples/blob/main/cli/deploy-custom-container-tfserving-half-plus-two-integrated.sh)|Deploys a Half Plus Two model by using a TF Serving custom container with the model integrated into the image.|
|[torchserve/densenet](https://github.com/Azure/azureml-examples/blob/main/cli/endpoints/online/custom-container/torchserve/densenet)|[deploy-custom-container-torchserve-densenet](https://github.com/Azure/azureml-examples/blob/main/cli/deploy-custom-container-torchserve-densenet.sh)|Deploys a single model by using a TorchServe custom container.|
|[triton/single-model](https://github.com/Azure/azureml-examples/blob/main/cli/endpoints/online/custom-container/triton/single-model)|[deploy-custom-container-triton-single-model](https://github.com/Azure/azureml-examples/blob/main/cli/deploy-custom-container-triton-single-model.sh)|Deploys a Triton model by using a custom container.|

This article shows you how to use the tfserving/half-plus-two example.

> [!WARNING]
> Microsoft support teams might not be able to help troubleshoot problems caused by a custom image. If you encounter problems, you might be asked to use the default image or one of the images that Microsoft provides to see whether the problem is specific to your image.

## Download the source code

The steps in this article use code samples from the [azureml-examples](https://github.com/Azure/azureml-examples) repository. Use the following commands to clone the repository:

# [Azure CLI](#tab/cli)

```azurecli
git clone https://github.com/Azure/azureml-examples --depth 1
cd azureml-examples/cli
```

# [Python SDK](#tab/python)

```azurecli
git clone https://github.com/Azure/azureml-examples --depth 1
cd azureml-examples/cli
```

In the examples repository, most Python samples are under the sdk/python folder. For this article, go to the cli folder instead. The folder structure under the cli folder is slightly different than the sdk/python structure in this case. Most steps in this article require the cli structure.

To follow along with the example steps, see a [Jupyter notebook in the examples repository](https://github.com/Azure/azureml-examples/blob/main/sdk/python/endpoints/online/custom-container/online-endpoints-custom-container.ipynb). But in the following sections of that notebook, the steps run from the azureml-examples/sdk/python folder instead of the cli folder:

- 3. Test locally
- 5. Test the endpoint with sample data

---

## Initialize environment variables

To use a TensorFlow model, you need several environment variables. Run the following commands to define those variables:

:::code language="azurecli" source="~/azureml-examples-main/cli/deploy-custom-container-tfserving-half-plus-two.sh" id="initialize_variables":::

## Download a TensorFlow model

Download and unzip a model that divides an input value by two and adds two to the result:

:::code language="azurecli" source="~/azureml-examples-main/cli/deploy-custom-container-tfserving-half-plus-two.sh" id="download_and_unzip_model":::

## Test a TF Serving image locally

Use Docker to run your image locally for testing:

:::code language="azurecli" source="~/azureml-examples-main/cli/deploy-custom-container-tfserving-half-plus-two.sh" id="run_image_locally_for_testing":::

### Send liveness and scoring requests to the image

Send a liveness request to check that the process inside the container is running. You should get a response status code of 200 OK.

:::code language="azurecli" source="~/azureml-examples-main/cli/deploy-custom-container-tfserving-half-plus-two.sh" id="check_liveness_locally":::

Send a scoring request to check that you can get predictions about unlabeled data:

:::code language="azurecli" source="~/azureml-examples-main/cli/deploy-custom-container-tfserving-half-plus-two.sh" id="check_scoring_locally":::

### Stop the image

When you finish testing locally, stop the image:

:::code language="azurecli" source="~/azureml-examples-main/cli/deploy-custom-container-tfserving-half-plus-two.sh" id="stop_image":::

## Deploy your online endpoint to Azure

To deploy your online endpoint to Azure, take the steps in the following sections.

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

### Connect to your Azure Machine Learning workspace

To configure your Azure Machine Learning workspace, take the following steps:

1. Import the required libraries:

    ```python
    # Import the required libraries.
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

1. Configure workspace settings and get a handle to the workspace:

    ```python
    # Enter information about your Azure Machine Learning workspace.
    subscription_id = "<subscription-ID>"
    resource_group = "<resource-group-name>"
    workspace = "<Azure-Machine-Learning-workspace-name>"

    # Get a handle to the workspace.
    ml_client = MLClient(
      DefaultAzureCredential(), subscription_id, resource_group, workspace
    )
    ```

For more information, see [Deploy and score a machine learning model by using an online endpoint](how-to-deploy-online-endpoints.md?view=azureml-api-2&tabs=python&preserve-view=true).

### Configure an online endpoint

Use the following code to configure an online endpoint. Keep the following points in mind:

- The name of the endpoint must be unique in its Azure region. Also, an endpoint name must start with a letter and only consist of alphanumeric characters and hyphens. For more information about naming rules, see [Azure Machine Learning online endpoints and batch endpoints](how-to-manage-quotas.md#azure-machine-learning-online-endpoints-and-batch-endpoints).
- For the `auth_mode` value, use `key` for key-based authentication. Use `aml_token` for Azure Machine Learning token-based authentication. A key doesn't expire, but a token does expire. For more information about authentication, see [Authenticate clients for online endpoints](how-to-authenticate-online-endpoint.md).
- The description and tags are optional.

```python
# To create a unique endpoint name, use a time stamp of the current date and time.
import datetime

online_endpoint_name = "endpoint-" + datetime.datetime.now().strftime("%m%d%H%M%f")

# Configure an online endpoint.
endpoint = ManagedOnlineEndpoint(
    name=online_endpoint_name,
    description="A sample online endpoint",
    auth_mode="key",
    tags={"env": "dev"},
)
```

### Configure an online deployment

A deployment is a set of resources that are required for hosting the model that does the actual inferencing. You can use the `ManagedOnlineDeployment` class to configure a deployment for your endpoint. The constructor of that class uses the following parameters:

- `name`: The name of the deployment.
- `endpoint_name`: The name of the endpoint to create the deployment under.
- `model`: The model to use for the deployment. This value can be either a reference to an existing versioned model in the workspace or an inline model specification.
- `environment`: The environment to use for the deployment. This value can be either a reference to an existing versioned environment in the workspace or an inline environment specification.
- `environment_variables`: Environment variables that are set during deployment.
  - `MODEL_BASE_PATH`: The path to the parent folder that contains a folder for your model.
  - `MODEL_NAME`: The name of your model.
- `instance_type`: The virtual machine size to use for the deployment. For a list of supported sizes, see [Managed online endpoints SKU list](reference-managed-online-endpoints-vm-sku-list.md).
- `instance_count`: The number of instances to use for the deployment.

Use the following code to configure a deployment for your endpoint:

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

The following sections discuss important concepts about the YAML and Python parameters.

#### Base image

In the `environment` section in YAML, or the `Environment` constructor in Python, you specify the base image as a parameter. This example uses `docker.io/tensorflow/serving:latest` as the `image` value.

If you inspect your container, you can see that this server uses `ENTRYPOINT` commands to start an entry point script. That script takes environment variables such as `MODEL_BASE_PATH` and `MODEL_NAME`, and it exposes ports such as `8501`. These details all pertain to this server, and you can use this information to determine how to define your deployment. For example, if you set the `MODEL_BASE_PATH` and `MODEL_NAME` environment variables in your deployment definition, TF Serving uses those values to initiate the server. Likewise, if you set the port for each route to `8501` in the deployment definition, user requests to those routes are correctly routed to the TF Serving server.

This example is based on the TF Serving case. But you can use any container that stays up and responds to requests that go to liveness, readiness, and scoring routes. To see how to form a Dockerfile to create a container, you can refer to other examples. Some servers use `CMD` instructions instead of `ENTRYPOINT` instructions.

#### The inference_config parameter

In the `environment` section or the `Environment` class, `inference_config` is a parameter. It specifies the port and path for three types of routes: liveness, readiness, and scoring routes. The `inference_config` parameter is required if you want to run your own container with a managed online endpoint.

#### Readiness routes vs. liveness routes

Some API servers provide a way to check the status of the server. There are two types of routes that you can specify for checking the status:

- *Liveness* routes: To check whether a server is running, you use a liveness route.
- *Readiness* routes: To check whether a server is ready to do work, you use a readiness route.

In the context of machine learning inferencing, a server might respond with a status code of 200 OK to a liveness request before loading a model. The server might respond with a status code of 200 OK to a readiness request only after it loads the model into memory.

For more information about liveness and readiness probes, see [Configure Liveness, Readiness and Startup Probes](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/).

The API server that you choose determines the liveness and readiness routes. You identify that server in an earlier step when you test the container locally. In this article, the example deployment uses the same path for the liveness and readiness routes, because TF Serving only defines a liveness route. For other ways of defining the routes, see other examples.

#### Scoring routes

The API server that you use provides a way to receive the payload to work on. In the context of machine learning inferencing, a server receives the input data via a specific route. Identify that route for your API server when you test the container locally in an earlier step. Specify that route as the scoring route when you define the deployment to create.

The successful creation of the deployment also updates the `scoring_uri` parameter of the endpoint. You can verify this fact by running the following command: `az ml online-endpoint show -n <endpoint-name> --query scoring_uri`.

#### Locate the mounted model

When you deploy a model as an online endpoint, Azure Machine Learning *mounts* your model to your endpoint. When the model is mounted, you can deploy new versions of the model without having to create a new Docker image. By default, a model registered with the name *my-model* and version *1* is located on the following path inside your deployed container: */var/azureml-app/azureml-models/my-model/1*.

For example, consider the following setup:

- A directory structure on your local machine of /azureml-examples/cli/endpoints/online/custom-container
- A model name of `half_plus_two`

:::image type="content" source="./media/how-to-deploy-custom-container/local-directory-structure.png" alt-text="Screenshot that shows a tree view of a local directory structure. The /azureml-examples/cli/endpoints/online/custom-container path is visible.":::

# [Azure CLI](#tab/cli)

Suppose your tfserving-deployment.yml file contains the following lines in its `model` section. In this section, the `name` value refers to the name that you use to register the model in Azure Machine Learning.

```yaml
model:
    name: tfserving-mounted
    version: 1
    path: ./half_plus_two
```

# [Python SDK](#tab/python)

Suppose you use the following code to create a `Model` class. In this code, the `name` value refers to the name that you use to register the model in Azure Machine Learning.

```python
model = Model(name="tfserving-mounted", version="1", path="half_plus_two")
```

---

In this case, when you create a deployment, your model is located under the following folder: /var/azureml-app/azureml-models/tfserving-mounted/1.

:::image type="content" source="./media/how-to-deploy-custom-container/deployment-location.png" alt-text="Screenshot that shows a tree view of the deployment directory structure. The var/azureml-app/azureml-models/tfserving-mounted/1 path is visible.":::

You can optionally configure your `model_mount_path` value. By adjusting this setting, you can change the path where the model is mounted.

> [!IMPORTANT]
> The `model_mount_path` value must be a valid absolute path in Linux (in the guest OS of the container image).

> [!IMPORTANT]
> `model_mount_path` is usable only in BYOC (Bring your own container) scenario. In BYOC scenario, the environment that the online deployment uses must have [`inference_config` parameter](#the-inference_config-parameter) configured. You can use Azure ML CLI or Python SDK to specify `inference_config` parameter when creating the environment. Studio UI currently doesn't support specifying this parameter.

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

In your deployment, your model is then located at /var/tfserving-model-mount/tfserving-mounted/1. It's no longer under azureml-app/azureml-models, but under the mount path that you specify:

:::image type="content" source="./media/how-to-deploy-custom-container/mount-path-deployment-location.png" alt-text="Screenshot that shows a tree view of the deployment directory structure. The /var/tfserving-model-mount/tfserving-mounted/1 path is visible.":::

### Create your endpoint and deployment

# [Azure CLI](#tab/cli)

After you construct your YAML file, use the following command to create your endpoint:

```azurecli
az ml online-endpoint create --name tfserving-endpoint -f endpoints/online/custom-container/tfserving/half-plus-two/tfserving-endpoint.yml
```

Use the following command to create your deployment. This step might run for a few minutes.

```azurecli
az ml online-deployment create --name tfserving-deployment -f endpoints/online/custom-container/tfserving/half-plus-two/tfserving-deployment.yml --all-traffic
```

# [Python SDK](#tab/python)

Use the following code to create the endpoint in the workspace. This code uses the instance of `MLClient` that you created earlier. The `begin_create_or_update` method starts the endpoint creation. It then returns a confirmation response while the endpoint creation continues.

```python
ml_client.begin_create_or_update(endpoint)
```

Create the deployment by running the following code:

```python
ml_client.begin_create_or_update(blue_deployment)
```

---

### Invoke the endpoint

When your deployment is complete, make a scoring request to the deployed endpoint.

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
    request_file="sample_request.json",
)
```

---

### Delete the endpoint

If you no longer need your endpoint, run the following command to delete it:

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

- [Perform safe rollout of new deployments for real-time inference](how-to-safely-rollout-online-endpoints.md)
- [Troubleshoot online endpoint deployment and scoring](./how-to-troubleshoot-online-endpoints.md)
- [Torch serve sample](https://github.com/Azure/azureml-examples/blob/main/cli/deploy-custom-container-torchserve-densenet.sh)
