---
title: High-Performance Model Serving with Triton
titleSuffix: Azure Machine Learning
description: 'Learn how to deploy your model with NVIDIA Triton Inference Server in Azure Machine Learning.'
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: inferencing
ms.date: 12/29/2025
ms.topic: how-to
author: s-polly
ms.author: scottpolly
ms.reviewer: jturuk
ms.custom: deploy, devplatv2, devx-track-azurecli, cliv2, sdkv2
ms.devlang: azurecli
---

# High-performance serving with Triton Inference Server

[!INCLUDE [dev v2](includes/machine-learning-dev-v2.md)]

This article describes how to use [NVIDIA Triton Inference Server](https://aka.ms/nvidia-triton-docs) in Azure Machine Learning with [online endpoints](concept-endpoints-online.md).

Triton is multi-framework open-source software that's optimized for inference. It supports popular machine learning frameworks like TensorFlow, ONNX Runtime, PyTorch, and NVIDIA TensorRT. You can use it for CPU or GPU workloads.

There are two main approaches you can take to use Triton models when deploying them to online endpoints: No-code deployment or full-code (Bring Your Own Container) deployment.
- No-code deployment for Triton models is a simple way to deploy them because you only need to bring Triton models to deploy.
- Full-code deployment for Triton models is a more advanced way to deploy them because you have full control over customizing the configurations available for Triton inference server.

For both options, Triton Inference Server performs inferencing based on the [Triton model as defined by NVIDIA](https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/user_guide/model_repository.html). For instance, [ensemble models](https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/user_guide/architecture.html#ensemble-models) can be used for more advanced scenarios.

Triton is supported in both [managed online endpoints and Kubernetes online endpoints](concept-endpoints-online.md#managed-online-endpoints-vs-kubernetes-online-endpoints).

In this article, you'll learn how to deploy a model by using no-code deployment for Triton to a [managed online endpoint](concept-endpoints-online.md#online-endpoints). Information is provided for using the Azure CLI, Python SDK v2, and Azure Machine Learning studio. If you want to customize further by directly using Triton Inference Server's configuration, see [Use a custom container to deploy a model](how-to-deploy-custom-container.md) and the BYOC example for Triton ([deployment definition](https://github.com/Azure/azureml-examples/tree/main/cli/endpoints/online/custom-container/triton/single-model) and [end-to-end script](https://github.com/Azure/azureml-examples/blob/main/cli/deploy-custom-container-triton-single-model.sh)). 

> [!NOTE]
> Use of the NVIDIA Triton Inference Server container is governed by the [NVIDIA AI Enterprise Software license agreement](https://www.nvidia.com/en-us/data-center/products/nvidia-ai-enterprise/eula/) and can be used for 90 days without an enterprise product subscription. For more information, see [NVIDIA AI Enterprise on Azure Machine Learning](https://www.nvidia.com/en-us/data-center/azure-ml).

## Prerequisites

# [Azure CLI](#tab/azure-cli)

[!INCLUDE [basic prereqs](includes/machine-learning-cli-prereqs.md)]

* A working Python 3.10 or later environment. 

* You must have additional Python packages installed for scoring. You can install them by using the following code. They include:
    * NumPy. An array and numerical computing library.
    * [Triton Inference Server Client](https://github.com/triton-inference-server/client). Facilitates requests to the Triton Inference Server.
    * Pillow. A library for image operations.
    * Gevent. A networking library used for connecting to the Triton server.

    ```azurecli
    pip install numpy
    pip install tritonclient[http]
    pip install pillow
    pip install gevent
    ```

* Access to NCv3-series VMs for your Azure subscription.

    > [!IMPORTANT]
    > You might need to request a quota increase for your subscription before you can use this series of VMs. For more information, see [NCv3-series](/azure/virtual-machines/ncv3-series).

* NVIDIA Triton Inference Server requires a specific model repository structure, where there's a directory for each model and subdirectories for the model versions. The contents of each model version subdirectory is determined by the type of the model and the requirements of the backend that supports the model. For information about the structure for all models, see [Model Files](https://github.com/triton-inference-server/server/blob/main/docs/user_guide/model_repository.md#model-files).

   The information in this document is based on using a model stored in ONNX format, so the directory structure of the model repository is `<model-repository>/<model-name>/1/model.onnx`. Specifically, this model performs image identification.

[!INCLUDE [clone repo & set defaults](includes/machine-learning-cli-prepare.md)]

# [Python](#tab/python)

[!INCLUDE [sdk v2](includes/machine-learning-sdk-v2.md)]

[!INCLUDE [sdk](includes/machine-learning-sdk-v2-prereqs.md)]

* A working Python 3.10 or later environment.

* You must have additional Python packages installed for scoring. You can install them by using the following code. They include:
    * NumPy. An array and numerical computing library.
    * [Triton Inference Server Client](https://github.com/triton-inference-server/client). Facilitates requests to the Triton Inference Server.
    * Pillow. A library for image operations.
    * Gevent. A networking library used for connecting to the Triton server.

    ```azurecli
    pip install numpy
    pip install tritonclient[http]
    pip install pillow
    pip install gevent
    ```

* Access to NCv3-series VMs for your Azure subscription.

    > [!IMPORTANT]
    > You might need to request a quota increase for your subscription before you can use this series of VMs. For more information, see [NCv3-series](/azure/virtual-machines/ncv3-series).

The information in this article is based on the [online-endpoints-triton.ipynb](https://github.com/Azure/azureml-examples/blob/main/sdk/python/endpoints/online/triton/single-model/online-endpoints-triton.ipynb) notebook contained in the [azureml-examples](https://github.com/azure/azureml-examples) repository. To run the commands locally without having to copy and paste files, clone the repo, and then change directories to the `sdk/endpoints/online/triton/single-model/` directory in the repo:

```azurecli
git clone https://github.com/Azure/azureml-examples --depth 1
cd azureml-examples/sdk/python/endpoints/online/triton/single-model/
```

# [Studio](#tab/azure-studio)

* An Azure subscription. If you don't have an Azure subscription, create a free account before you begin. Try the [free or paid version of Azure](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

* An Azure Machine Learning workspace. If you don't have one, complete the steps in [Manage Azure Machine Learning workspaces in the portal, or with the Python SDK](how-to-manage-workspace.md) to create one.

--- 

## Define the deployment configuration

# [Azure CLI](#tab/azure-cli)

[!INCLUDE [cli v2](includes/machine-learning-cli-v2.md)]

This section describes how to deploy to a managed online endpoint by using the Azure CLI with the Machine Learning extension (v2).

> [!IMPORTANT]
> For Triton no-code-deployment, [testing via local endpoints](how-to-deploy-online-endpoints.md#deploy-and-debug-locally-by-using-a-local-endpoint) is currently not supported.

1. To avoid typing in a path for multiple commands, use the following command to set a `BASE_PATH` environment variable. This variable points to the directory where the model and associated YAML configuration files are located:

    ```azurecli
    BASE_PATH=endpoints/online/triton/single-model
    ```

1. Use the following command to set the name of the endpoint that will be created. In this example, a random name is created for the endpoint:

    :::code language="azurecli" source="~/azureml-examples-main/cli/deploy-triton-managed-online-endpoint.sh" ID="set_endpoint_name":::

1. Create a YAML configuration file for your endpoint. The following example configures the name and authentication mode of the endpoint. The file used in the following commands is located at `/cli/endpoints/online/triton/single-model/create-managed-endpoint.yml` in the azureml-examples repo you cloned earlier:

    __create-managed-endpoint.yaml__

    :::code language="yaml" source="~/azureml-examples-main/cli/endpoints/online/triton/single-model/create-managed-endpoint.yaml":::

1. Create a YAML configuration file for the deployment. The following example configures a deployment named `blue` to the endpoint defined in the previous step. The file used in the following commands is located at `/cli/endpoints/online/triton/single-model/create-managed-deployment.yml` in the azureml-examples repo you cloned earlier:

    > [!IMPORTANT]
    > For Triton no-code-deployment to work, you need to set `type` to `triton_model​`: `type: triton_model​`. For more information, see [CLI (v2) model YAML schema](reference-yaml-model.md).
    >
    > This deployment uses a Standard_NC6s_v3 VM. You might need to request a quota increase for your subscription before you can use this VM. For more information, see [NCv3-series](/azure/virtual-machines/ncv3-series).

    :::code language="yaml" source="~/azureml-examples-main/cli/endpoints/online/triton/single-model/create-managed-deployment.yaml":::

# [Python](#tab/python)

[!INCLUDE [sdk v2](includes/machine-learning-sdk-v2.md)]

This section describes how to define a Triton deployment to deploy to a managed online endpoint by using the Azure Machine Learning Python SDK (v2).

> [!IMPORTANT]
> For Triton no-code-deployment, [testing via local endpoints](how-to-deploy-online-endpoints.md#deploy-and-debug-locally-by-using-a-local-endpoint) is currently not supported.


1. To connect to a workspace, you need identifier parameters: a subscription, resource group, and workspace name. 

    ```python 
    subscription_id = "<SUBSCRIPTION_ID>"
    resource_group = "<RESOURCE_GROUP>"
    workspace_name = "<WORKSPACE_NAME>"
    ```

1. Use the following command to set the name of the endpoint that will be created. In this example, a random name is created for the endpoint:

    ```python
    import random

    endpoint_name = f"endpoint-{random.randint(0, 10000)}"
    ```

1. Use the identifier parameters configured earlier in the `azure.ai.ml` `MLClient` to get a handle to the required Azure Machine Learning workspace. See the [configuration notebook](https://github.com/Azure/azureml-examples/blob/main/sdk/python/jobs/configuration.ipynb) for more details on how to configure credentials and connect to a workspace.

    ```python 
    from azure.ai.ml import MLClient
    from azure.identity import DefaultAzureCredential

    ml_client = MLClient(
        DefaultAzureCredential(),
        subscription_id,
        resource_group,
        workspace_name,
    )
    ```

1. Create a `ManagedOnlineEndpoint` object to configure the endpoint. The following example configures the name and authentication mode of the endpoint. 

    ```python 
    from azure.ai.ml.entities import ManagedOnlineEndpoint

    endpoint = ManagedOnlineEndpoint(name=endpoint_name, auth_mode="key")
    ```

1. Create a `ManagedOnlineDeployment` object to configure the deployment. The following example configures a deployment named `blue` to the endpoint defined in the previous step and defines a local model inline.

    ```python
    from azure.ai.ml.entities import ManagedOnlineDeployment, Model
    
    model_name = "densenet-onnx-model"
    model_version = "1"
    
    deployment = ManagedOnlineDeployment(
        name="blue",
        endpoint_name=endpoint_name,
        model=Model(
            name=model_name, 
            version=model_version,
            path="./models",
            type="triton_model"
        ),
        instance_type="Standard_NC6s_v3",
        instance_count=1,
    )
    ``` 

# [Studio](#tab/azure-studio)

This section describes how to define a Triton deployment on a managed online endpoint by using [Azure Machine Learning studio](https://ml.azure.com).

1. Register your model in Triton format by using the following YAML and CLI command. The YAML uses a densenet-onnx model from [azureml-examples/cli/endpoints/online/triton/single-model](https://github.com/Azure/azureml-examples/tree/main/cli/endpoints/online/triton/single-model).

    __create-triton-model.yaml__

    ```yml
    name: densenet-onnx-model
    version: 1
    path: ./models
    type: triton_model​
    description: Registering my Triton format model.
    ```

    ```azurecli
    az ml model create -f create-triton-model.yaml
    ```

    The following screenshot shows how your registered model will look on the __Models__ page of Azure Machine Learning studio.

    :::image type="content" source="media/how-to-deploy-with-triton/triton-model-format.png" lightbox="media/how-to-deploy-with-triton/triton-model-format.png" alt-text="Screenshot showing the Triton model format on the Models page.":::

1. In [studio](https://ml.azure.com), select your workspace and then use the __Endpoints__ or __Models__ page to create the endpoint deployment:

    # [Endpoints page](#tab/endpoint)

    1. On the __Endpoints__ page, select **Create**.

        :::image type="content" source="media/how-to-deploy-with-triton/create-option-from-endpoints-page.png" lightbox="media/how-to-deploy-with-triton/create-option-from-endpoints-page.png" alt-text="Screenshot showing the Create option on the Endpoints page.":::

    1. Select the Triton model that you registered earlier, and then click **Select**.

    1. When you select a model registered in Triton format, you don't need a scoring script or environment.

        :::image type="content" source="media/how-to-deploy-with-triton/ncd-triton.png" lightbox="media/how-to-deploy-with-triton/ncd-triton.png" alt-text="Screenshot showing the message stating that no script or environment is needed for Triton models":::

    # [Models page](#tab/models)

    1. Select the Triton model, and then select **Use this model** > __Real-time endpoint__.

        :::image type="content" source="media/how-to-deploy-with-triton/deploy-from-models-page.png" lightbox="media/how-to-deploy-with-triton/deploy-from-models-page.png" alt-text="Screenshot showing how to deploy a model from the Model page.":::

    
    ---
---


## Deploy to Azure

# [Azure CLI](#tab/azure-cli)

[!INCLUDE [cli v2](includes/machine-learning-cli-v2.md)]

1. To create an endpoint by using the YAML configuration, use the following command:

    :::code language="azurecli" source="~/azureml-examples-main/cli/deploy-triton-managed-online-endpoint.sh" ID="create_endpoint":::


1. To create the deployment by using the YAML configuration, use the following command:

    :::code language="azurecli" source="~/azureml-examples-main/cli/deploy-triton-managed-online-endpoint.sh" ID="create_deployment":::


# [Python](#tab/python)

[!INCLUDE [sdk v2](includes/machine-learning-sdk-v2.md)]

1. To create an endpoint by using the `ManagedOnlineEndpoint` object, use the following command:

    ```python 
    endpoint = ml_client.online_endpoints.begin_create_or_update(endpoint)
    ``` 

1. To create the deployment by using the `ManagedOnlineDeployment` object, use the following command:

    ```python 
    ml_client.online_deployments.begin_create_or_update(deployment)
    ```

1. After the deployment is complete, its `traffic` value will be set to 0%. Update the `traffic` value to 100%:

    ```python 
    endpoint.traffic = {"blue": 100}
    ml_client.online_endpoints.begin_create_or_update(endpoint)
    ```


# [Studio](#tab/azure-studio)

1. In the **Deploy** pane, select **Deploy**.

   :::image type="content" source="media/how-to-deploy-with-triton/review-screen-triton.png" lightbox="media/how-to-deploy-with-triton/review-screen-triton.png" alt-text="Screenshot showing the Deploy button.":::

1. After the deployment is complete, its traffic value will be set to 0%. Update the traffic value to 100% by selecting **Update traffic** on the page for the endpoint. 

---

## Test the endpoint

# [Azure CLI](#tab/azure-cli)

[!INCLUDE [cli v2](includes/machine-learning-cli-v2.md)]

After your deployment is complete, use the following command to make a scoring request to the deployed endpoint. 

> [!TIP]
> The file `/cli/endpoints/online/triton/single-model/triton_densenet_scoring.py` in the azureml-examples repo is used for scoring. The image passed to the endpoint needs preprocessing to meet the size, type, and format requirements, and post-processing to show the predicted label. The `triton_densenet_scoring.py` file uses the `tritonclient.http` library to communicate with the Triton inference server. This file runs on the client side.

1. To get the endpoint scoring URI, use the following command:

    :::code language="azurecli" source="~/azureml-examples-main/cli/deploy-triton-managed-online-endpoint.sh" ID="get_scoring_uri":::

1. To get an authentication key, use the following command:

    :::code language="azurecli" source="~/azureml-examples-main/cli/deploy-triton-managed-online-endpoint.sh" ID="get_token":::

1. To score data with the endpoint, use the following command. It submits the image of a [peacock](https://aka.ms/peacock-pic) to the endpoint:

    :::code language="azurecli" source="~/azureml-examples-main/cli/deploy-triton-managed-online-endpoint.sh" ID="check_scoring_of_model":::

    The response from the script is similar to the following response:

    ```
    Is server ready - True
    Is model ready - True
    /azureml-examples/cli/endpoints/online/triton/single-model/densenet_labels.txt
    84 : PEACOCK
    ```

# [Python](#tab/python)

[!INCLUDE [sdk v2](includes/machine-learning-sdk-v2.md)]

1. To get the endpoint scoring URI, use the following command:

    ```python 
    endpoint = ml_client.online_endpoints.get(endpoint_name)
    scoring_uri = endpoint.scoring_uri
    ```

1. To get an authentication key, use the following command:
 
    ```python
    keys = ml_client.online_endpoints.get_keys(endpoint_name)
    auth_key = keys.primary_key
    ```

1. The following scoring code uses the [Triton Inference Server Client](https://github.com/triton-inference-server/client) to submit the image of a peacock to the endpoint. This script is available in the companion notebook to this example: [Deploy a model to online endpoints using Triton](https://github.com/Azure/azureml-examples/blob/main/sdk/python/endpoints/online/triton/single-model/online-endpoints-triton.ipynb).

    ```python
    # Test the blue deployment with some sample data
    import requests
    import gevent.ssl
    import numpy as np
    import tritonclient.http as tritonhttpclient
    from pathlib import Path
    import prepost

    img_uri = "http://aka.ms/peacock-pic"

    # Remove the scheme from the URL
    url = scoring_uri[8:]

    # Initialize the client handler
    triton_client = tritonhttpclient.InferenceServerClient(
        url=url,
        ssl=True,
        ssl_context_factory=gevent.ssl._create_default_https_context,
    )

    # Create headers
    headers = {}
    headers["Authorization"] = f"Bearer {auth_key}"

    # Check the status of the Triton server
    health_ctx = triton_client.is_server_ready(headers=headers)
    print("Is server ready - {}".format(health_ctx))

    # Check the status of the model
    model_name = "model_1"
    status_ctx = triton_client.is_model_ready(model_name, "1", headers)
    print("Is model ready - {}".format(status_ctx))

    if Path(img_uri).exists():
        img_content = open(img_uri, "rb").read()
    else:
        agent = f"Python Requests/{requests.__version__} (https://github.com/Azure/azureml-examples)"
        img_content = requests.get(img_uri, headers={"User-Agent": agent}).content

    img_data = prepost.preprocess(img_content)

    # Populate inputs and outputs
    input = tritonhttpclient.InferInput("data_0", img_data.shape, "FP32")
    input.set_data_from_numpy(img_data)
    inputs = [input]
    output = tritonhttpclient.InferRequestedOutput("fc6_1")
    outputs = [output]

    result = triton_client.infer(model_name, inputs, outputs=outputs, headers=headers)
    max_label = np.argmax(result.as_numpy("fc6_1"))
    label_name = prepost.postprocess(max_label)
    print(label_name)
    ``` 

1. The response from the script is similar to the following response:

    ```
    Is server ready - True
    Is model ready - True
    /azureml-examples/sdk/endpoints/online/triton/single-model/densenet_labels.txt
    84 : PEACOCK
    ```

# [Studio](#tab/azure-studio)

Triton Inference Server requires the use of Triton Client for inference, and it supports tensor-typed input. Azure Machine Learning studio doesn't currently support this functionality. Instead, use the CLI or SDK to invoke endpoints with Triton.

--- 

### Delete the endpoint and model
# [Azure CLI](#tab/azure-cli)

[!INCLUDE [cli v2](includes/machine-learning-cli-v2.md)]

1. When you're done with the endpoint, use the following command to delete it:

    :::code language="azurecli" source="~/azureml-examples-main/cli/deploy-triton-managed-online-endpoint.sh" ID="delete_endpoint":::

1. Use the following command to archive your model:

    ```azurecli
    az ml model archive --name sample-densenet-onnx-model --version 1
    ```

# [Python](#tab/python)

[!INCLUDE [sdk v2](includes/machine-learning-sdk-v2.md)]

1. Delete the endpoint. Deleting the endpoint also deletes any child deployments, but it won't archive associated environments or models. 

    ```python
    ml_client.online_endpoints.begin_delete(name=endpoint_name)
    ```

1. Archive the model by using the following code.

    ```python 
    ml_client.models.archive(name=model_name, version=model_version)
    ```

# [Studio](#tab/azure-studio)

1. On the endpoint's page, select **Delete**. 

1. On the model's page, select **Archive**. 
---


## Next steps

To learn more, review these articles:

- [Deploy models with REST](how-to-deploy-with-rest.md)
- [Create and use managed online endpoints in the studio](how-to-use-managed-online-endpoint-studio.md)
- [Safe rollout for online endpoints ](how-to-safely-rollout-online-endpoints.md)
- [How to autoscale managed online endpoints](how-to-autoscale-endpoints.md)
- [View costs for an Azure Machine Learning managed online endpoint](how-to-view-online-endpoints-costs.md)
- [Access Azure resources from an online endpoint with a managed identity](how-to-access-resources-from-endpoints-managed-identities.md)
- [Troubleshoot online endpoint deployment and scoring](how-to-troubleshoot-managed-online-endpoints.md)
