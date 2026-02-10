---
title: Safe rollout for online endpoints
titleSuffix: Azure Machine Learning
description: Find out how to deploy a new version of a machine learning model without disruption. See how to use a blue-green deployment strategy in Azure Machine Learning.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: mlops
author: s-polly
ms.author: scottpolly
ms.reviewer: jturuk
ms.date: 02/08/2026
ms.topic: how-to
ms.custom: how-to, devplatv2, cliv2, sdkv2, update-code, dev-focus
ai-usage: ai-assisted
# customer intent: As a developer, I want to see how to use a blue-green deployment strategy in Azure Machine Learning so that I can roll out a new version of a machine learning model without causing disruption.
---

# Perform safe rollout of new deployments for real-time inference

[!INCLUDE [Version 2 applies-to line](includes/machine-learning-dev-v2.md)]

In this article, you learn how to deploy a new version of a machine learning model in production without causing any disruption. Use a blue-green deployment strategy, which is also known as a safe rollout strategy, to introduce a new version of a web service to production. When you use this strategy, you roll out your new version of the web service to a small subset of users or requests before rolling it out completely.

This article assumes you use online endpoints, or endpoints that are used for online (real-time) inferencing. Two types of online endpoints exist: **managed online endpoints** and **Kubernetes online endpoints**. For more information about endpoints and the differences between endpoint types, see [Managed online endpoints vs. Kubernetes online endpoints](concept-endpoints-online.md#managed-online-endpoints-vs-kubernetes-online-endpoints).

This article uses managed online endpoints for deployment. But it also includes notes that explain how to use Kubernetes endpoints instead of managed online endpoints.

In this article, you learn how to:

- Define an online endpoint with a deployment named `blue` to serve the first version of a model.
- Scale the `blue` deployment so that it can handle more requests.
- Deploy the second version of the model, which is called the `green` deployment, to the endpoint, but send the deployment no live traffic.
- Test the `green` deployment in isolation.
- Mirror a percentage of live traffic to the `green` deployment to validate it.
- Send a small percentage of live traffic to the `green` deployment.
- Send all live traffic to the `green` deployment.
- Delete the unused `blue` deployment.

## Prerequisites

# [Azure CLI](#tab/azure-cli)

[!INCLUDE [Basic Azure CLI prerequisites](includes/machine-learning-cli-prereqs.md)]

* A user account that has at least one of the following Azure role-based access control (Azure RBAC) roles:

  * An Owner role for the Azure Machine Learning workspace
  * A Contributor role for the Azure Machine Learning workspace
  * A custom role that has `Microsoft.MachineLearningServices/workspaces/onlineEndpoints/*` permissions

  For more information, see [Manage access to Azure Machine Learning workspaces](how-to-assign-roles.md).

* Optionally, [Docker Engine](https://docs.docker.com/engine/install/), installed and running locally. This prerequisite is highly recommended. You need it to deploy a model locally, and it's helpful for debugging.

# [Python SDK](#tab/python)

[!INCLUDE [Python SDK v2](includes/machine-learning-sdk-v2.md)]

[!INCLUDE [Basic Python SDK prerequisites](includes/machine-learning-sdk-v2-prereqs.md)]

* Python 3.10 or later.

* A user account that has at least one of the following Azure role-based access control (Azure RBAC) roles:

  * An Owner role for the Azure Machine Learning workspace
  * A Contributor role for the Azure Machine Learning workspace
  * A custom role that has `Microsoft.MachineLearningServices/workspaces/onlineEndpoints/*` permissions

  For more information, see [Manage access to Azure Machine Learning workspaces](how-to-assign-roles.md).

* Optionally, [Docker Engine](https://docs.docker.com/engine/install/), installed and running locally. This prerequisite is highly recommended. You need it to deploy a model locally, and it's helpful for debugging.

# [Studio](#tab/azure-studio)

* An Azure subscription. If you don't have an Azure subscription, create a [free account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn) before you begin.

* An Azure Machine Learning workspace. For instructions for creating a workspace, see [Create the workspace](quickstart-create-resources.md#create-the-workspace).

* A user account that has at least one of the following Azure role-based access control (Azure RBAC) roles:

  * An Owner role for the Azure Machine Learning workspace
  * A Contributor role for the Azure Machine Learning workspace
  * A custom role that has `Microsoft.MachineLearningServices/workspaces/onlineEndpoints/*` permissions

  For more information, see [Manage access to Azure Machine Learning workspaces](how-to-assign-roles.md).

---

## Prepare your system

# [Azure CLI](#tab/azure-cli)

### Set environment variables

You can configure default values to use with the Azure CLI. To avoid passing values for your subscription, workspace, and resource group multiple times, run the following code:

```azurecli
az account set --subscription <subscription-ID>
az configure --defaults workspace=<Azure-Machine-Learning-workspace-name> group=<resource-group-name>
```

### Clone the examples repository

To follow along with this article, first clone the [examples repository (azureml-examples)](https://github.com/azure/azureml-examples). Then go to the repository's `cli/` directory:

```azurecli
git clone --depth 1 https://github.com/Azure/azureml-examples
cd azureml-examples
cd cli
```

> [!TIP]
> Use `--depth 1` to clone only the latest commit to the repository, which reduces the time needed to complete the operation.

The commands in this tutorial are in the `deploy-safe-rollout-online-endpoints.sh` file in the `cli` directory. The YAML configuration files are in the `endpoints/online/managed/sample/` subdirectory.

> [!NOTE]
> The YAML configuration files for Kubernetes online endpoints are in the `endpoints/online/kubernetes/` subdirectory.

# [Python SDK](#tab/python)

### Clone the examples repository

To run the training examples, first clone the [examples repository (azureml-examples)](https://github.com/azure/azureml-examples). Then go to the `azureml-examples/sdk/python/endpoints/online/managed` directory:

```bash
git clone --depth 1 https://github.com/Azure/azureml-examples
cd azureml-examples/sdk/python/endpoints/online/managed
```

> [!TIP]
> Use `--depth 1` to clone only the latest commit to the repository, which reduces the time needed to complete the operation.

This article is based on the [online-endpoints-safe-rollout.ipynb](https://github.com/Azure/azureml-examples/blob/main/sdk/python/endpoints/online/managed/online-endpoints-safe-rollout.ipynb) notebook. This article contains the same content as the notebook, but the order of the code blocks differs slightly between the two documents.

> [!NOTE]
> The steps for the Kubernetes online endpoint are based on the [kubernetes-online-endpoints-safe-rollout.ipynb](https://github.com/Azure/azureml-examples/blob/main/sdk/python/endpoints/online/kubernetes/kubernetes-online-endpoints-safe-rollout.ipynb) notebook.

### Connect to an Azure Machine Learning workspace

The [workspace](concept-workspace.md) is the top-level resource for Azure Machine Learning. A workspace provides a centralized place to work with all the artifacts you create when you use Azure Machine Learning. In this section, you connect to your workspace, where you perform deployment tasks. To follow along, open your online-endpoints-safe-rollout.ipynb notebook.

1. Import the required libraries:

    [!notebook-python[](~/azureml-examples-main/sdk/python/endpoints/online/managed/online-endpoints-safe-rollout.ipynb?name=import_libraries)]

    > [!NOTE]
    > If you're using a Kubernetes online endpoint, import the `KubernetesOnlineEndpoint` and `KubernetesOnlineDeployment` classes from the `azure.ai.ml.entities` library.

1. Configure workspace settings and get a handle to the workspace:

    To connect to a workspace, you need identifier parameters - a subscription, a resource group, and a workspace name. Use this information in the `MLClient` class from the `azure.ai.ml` module to get a handle to the required Azure Machine Learning workspace. This example uses the [default Azure authentication](/python/api/azure-identity/azure.identity.defaultazurecredential).

    [!notebook-python[](~/azureml-examples-main/sdk/python/endpoints/online/managed/online-endpoints-safe-rollout.ipynb?name=workspace_details)]

    [!notebook-python[](~/azureml-examples-main/sdk/python/endpoints/online/managed/online-endpoints-safe-rollout.ipynb?name=workspace_handle)]

# [Studio](#tab/azure-studio)

If you have Git installed on your local machine, you can follow the instructions to clone the examples repository. Otherwise, follow the instructions to download files from the examples repository.

### Clone the examples repository

To follow along with this article, clone the [azureml-examples repository](https://github.com/azure/azureml-examples). Then, go to the `azureml-examples/cli/endpoints/online/model-1` folder.

```bash
git clone --depth 1 https://github.com/Azure/azureml-examples
cd azureml-examples/cli/endpoints/online/model-1
```

> [!TIP]
> Use `--depth 1` to clone only the latest commit to the repository, which reduces the time needed to complete the operation.

### Download files from the examples repository

Instead of cloning the examples repository, you can download the repository to your local machine:

1. Go to [https://github.com/Azure/azureml-examples/](https://github.com/Azure/azureml-examples/).
1. Select **<> Code**. Go to the **Local** tab and select **Download ZIP**.

---

## Define the endpoint and deployment

Use online endpoints for online (real-time) inferencing. Online endpoints contain deployments that are ready to receive data from clients and send responses back in real time.

### Define an endpoint

The following table lists key attributes to specify when you define an endpoint.

| Attribute | Required or optional | Description |
| --- | --- | --- |
| Name | Required | The name of the endpoint. It must be unique in its Azure region. For more information about naming rules, see [Azure Machine Learning online endpoints and batch endpoints](how-to-manage-quotas.md#azure-machine-learning-online-endpoints-and-batch-endpoints). |
| Authentication mode | Optional | The authentication method for the endpoint. Choose between key-based authentication, `key`, Azure Machine Learning token-based authentication, `aml_token`, and Microsoft Entra token-based authentication, `aad_token`. A key doesn't expire, but a token does expire. For more information about authentication, see [Authenticate clients for online endpoints](how-to-authenticate-online-endpoint.md). |
| Description | Optional | The description of the endpoint. |
| Tags | Optional | A dictionary of tags for the endpoint. |
| Traffic | Optional | Rules on how to route traffic across deployments. Represent the traffic as a dictionary of key-value pairs, where the key represents the deployment name and the value represents the percentage of traffic to that deployment. You can set the traffic only after you create the deployments under an endpoint. You can also update the traffic for an online endpoint after the deployments are created. For more information about how to use mirrored traffic, see [Allocate a small percentage of live traffic to the new deployment](#allocate-a-small-percentage-of-live-traffic-to-the-new-deployment). |
| Mirror traffic | Optional | The percentage of live traffic to mirror to a deployment. For more information about how to use mirrored traffic, see [Test the deployment with mirrored traffic](#test-the-deployment-with-mirrored-traffic). |

To see a full list of attributes that you can specify when you create an endpoint, see [CLI (v2) online endpoint YAML schema](/azure/machine-learning/reference-yaml-endpoint-online). For version 2 of the Azure Machine Learning SDK for Python, see [ManagedOnlineEndpoint Class](/python/api/azure-ai-ml/azure.ai.ml.entities.managedonlineendpoint).

### Define a deployment

A *deployment* is a set of resources that host the model and perform the actual inferencing. The following table describes key attributes to specify when you define a deployment.

| Attribute | Required or optional | Description |
| --- | --- | --- |
| Name | Required | The name of the deployment. |
| Endpoint name | Required | The name of the endpoint to create the deployment under. |
| Model | Optional | The model to use for the deployment. This value can be either a reference to an existing versioned model in the workspace or an inline model specification. In this article's examples, a `scikit-learn` model does regression. |
| Code path | Optional | The path to the folder on the local development environment that contains all the Python source code for scoring the model. You can use nested directories and packages. |
| Scoring script | Optional | Python code that executes the model on a given input request. This value can be the relative path to the scoring file in the source code folder.<br>The scoring script receives data submitted to a deployed web service and passes it to the model. The script then executes the model and returns its response to the client. The scoring script is specific to your model and must understand the data that the model expects as input and returns as output.<br>This article's examples use a score.py file. This Python code must have an `init` function and a `run` function. The `init` function is called after the model is created or updated. You can use it to cache the model in memory, for example. The `run` function is called at every invocation of the endpoint to do the actual scoring and prediction. |
| Environment | Required | The environment to host the model and code. This value can be either a reference to an existing versioned environment in the workspace or an inline environment specification. The environment can be a Docker image with Conda dependencies, a Dockerfile, or a registered environment. |
| Instance type  | Required | The virtual machine size to use for the deployment. For a list of supported sizes, see [Managed online endpoints SKU list](reference-managed-online-endpoints-vm-sku-list.md). |
| Instance count | Required | The number of instances to use for the deployment. Base the value on the workload you expect. For high availability, use at least three instances. Azure Machine Learning reserves an extra 20 percent for performing upgrades. For more information, see [Azure Machine Learning online endpoints and batch endpoints](how-to-manage-quotas.md#azure-machine-learning-online-endpoints-and-batch-endpoints). |

To see a full list of attributes that you can specify when you create a deployment, see [CLI (v2) managed online deployment YAML schema](/azure/machine-learning/reference-yaml-deployment-managed-online). For version 2 of the Python SDK, see [ManagedOnlineDeployment Class](/python/api/azure-ai-ml/azure.ai.ml.entities.managedonlinedeployment).

# [Azure CLI](#tab/azure-cli)

### Create an online endpoint

First, set the endpoint name. Then, configure the endpoint. In this article, you use the `endpoints/online/managed/sample/endpoint.yml` file to configure the endpoint. That file contains the following lines:

:::code language="yaml" source="~/azureml-examples-main/cli/endpoints/online/managed/sample/endpoint.yml":::

The following table describes keys that the endpoint YAML format uses. To see how to specify these attributes, see [CLI (v2) online endpoint YAML schema](reference-yaml-endpoint-online.md). For information about limits related to managed online endpoints, see [Azure Machine Learning online endpoints and batch endpoints](how-to-manage-quotas.md#azure-machine-learning-online-endpoints-and-batch-endpoints).

| Key | Description |
| --- | --- |
| `$schema` | (Optional) The YAML schema. To see all available options in the YAML file, you can view the schema in the preceding code block in a browser. |
| `name` | The name of the endpoint. |
| `auth_mode` | The authentication mode. Use `key` for key-based authentication. Use `aml_token` for Azure Machine Learning token-based authentication. Use `aad_token` for Microsoft Entra token-based authentication. To get the most recent token, use the `az ml online-endpoint get-credentials` command. |

To create an online endpoint:

1. Set your endpoint name by running the following Unix command. Replace `YOUR_ENDPOINT_NAME` with a unique name.

    :::code language="azurecli" source="~/azureml-examples-main/cli/deploy-safe-rollout-online-endpoints.sh" ID="set_endpoint_name":::

    > [!IMPORTANT]
    > Endpoint names must be unique within an Azure region. For example, in the Azure `westus2` region, there can be only one endpoint with the name `my-endpoint`.

1. Create the endpoint in the cloud by running the following code. This code uses the `endpoint.yml` file to configure the endpoint:

    :::code language="azurecli" source="~/azureml-examples-main/cli/deploy-safe-rollout-online-endpoints.sh" ID="create_endpoint":::

### Create the blue deployment

You can use the `endpoints/online/managed/sample/blue-deployment.yml` file to configure the key aspects of a deployment named `blue`. That file contains the following lines:

:::code language="yaml" source="~/azureml-examples-main/cli/endpoints/online/managed/sample/blue-deployment.yml":::

To create the `blue` deployment for your endpoint, use the `blue-deployment.yml` file and run the following command:

:::code language="azurecli" source="~/azureml-examples-main/cli/deploy-safe-rollout-online-endpoints.sh" ID="create_blue":::

> [!IMPORTANT]
> The `--all-traffic` flag in the `az ml online-deployment create` command allocates 100 percent of the endpoint traffic to the newly created `blue` deployment.

In the `blue-deployment.yaml` file, the `path` line specifies where to upload files from. The Azure Machine Learning CLI uses this information to upload the files and register the model and environment. As a best practice for production, register the model and environment, and specify the registered name and version separately in the YAML code. Use the format `model: azureml:<model-name>:<model-version>` for the model, for example, `model: azureml:my-model:1`. For the environment, use the format `environment: azureml:<environment-name>:<environment-version>`, for example, `environment: azureml:my-env:1`.

For registration, you can extract the YAML definitions of `model` and `environment` into separate YAML files and use the commands `az ml model create` and `az ml environment create`. To find out more about these commands, run `az ml model create -h` and `az ml environment create -h`.

For more information about registering your model as an asset, see [Register a model by using the Azure CLI or Python SDK](how-to-manage-models.md#register-a-model-by-using-the-azure-cli-or-python-sdk). For more information about creating an environment, see [Create a custom environment](how-to-manage-environments-v2.md#create-a-custom-environment).

# [Python SDK](#tab/python)

### Create an online endpoint

Use the `ManagedOnlineEndpoint` class to create a managed online endpoint. This class helps you configure the key aspects of the endpoint.

1. Configure the endpoint:

    [!notebook-python[](~/azureml-examples-main/sdk/python/endpoints/online/managed/online-endpoints-safe-rollout.ipynb?name=configure_endpoint)]

    > [!NOTE]
    > To create a Kubernetes online endpoint, use the `KubernetesOnlineEndpoint` class.

1. Create the endpoint:

    [!notebook-python[](~/azureml-examples-main/sdk/python/endpoints/online/managed/online-endpoints-safe-rollout.ipynb?name=create_endpoint)]

### Create the blue deployment

To create a deployment for your managed online endpoint, use the `ManagedOnlineDeployment` class. This class provides a way for you to configure the key aspects of the deployment.

1. Configure the `blue` deployment:

    [!notebook-python[](~/azureml-examples-main/sdk/python/endpoints/online/managed/online-endpoints-safe-rollout.ipynb?name=configure_deployment)]

    In this example, the `path` parameter specifies where to upload files from. The Python SDK uses this information to upload the files and register the model and environment. As a best practice for production, register the model and environment and specify the registered name and version separately in the code.

    For more information about registering your model as an asset, see [Register a model by using the Azure CLI or Python SDK](how-to-manage-models.md#register-a-model-by-using-the-azure-cli-or-python-sdk).

    For more information about creating an environment, see [Create a custom environment](how-to-manage-environments-v2.md#create-a-custom-environment).

    > [!NOTE]
    > To create a deployment for a Kubernetes online endpoint, use the `KubernetesOnlineDeployment` class.

1. Create the deployment:

    [!notebook-python[](~/azureml-examples-main/sdk/python/endpoints/online/managed/online-endpoints-safe-rollout.ipynb?name=create_deployment)]

    [!notebook-python[](~/azureml-examples-main/sdk/python/endpoints/online/managed/online-endpoints-safe-rollout.ipynb?name=deployment_traffic)]

# [Studio](#tab/azure-studio)

When you create a managed online endpoint in Azure Machine Learning studio, you must define an initial deployment for the endpoint. Before you can define a deployment, register a model in your workspace. The following section shows you how to register a model to use for the deployment.

### Register your model

A model registration is a logical entity in the workspace. This entity can contain a single model file or a directory of multiple files. As a best practice for production, register your model and environment.

To register the example model, follow the steps in the following sections.

#### Upload the model files

1. Go to [Azure Machine Learning studio](https://ml.azure.com).

1. Select **Models**.

1. Select **Register**, and then select **From local files**.

1. Under **Model type**, select **Unspecified type**.

1. Select **Browse**, and then select **Browse folder**.

    :::image type="content" source="media/how-to-safely-rollout-managed-endpoints/register-model-folder.png" alt-text="Screenshot of the Register model from local files page. Under Browse, Browse folder is highlighted." lightbox="media/how-to-safely-rollout-managed-endpoints/register-model-folder.png":::

1. Go to the local copy of the repository you cloned or downloaded earlier, and then select **\azureml-examples\cli\endpoints\online\model-1\model**. When prompted, select **Upload** and wait for the upload to finish.

1. Select **Next**.

#### Configure and register the model

1. On the **Model settings** page, under **Name**, enter a friendly name for the model. The steps in this article assume the model is named `model-1`.

1. Select **Next**, and then select **Register** to complete the registration.

For later examples in this article, you also need to register a model from the \azureml-examples\cli\endpoints\online\model-2\model folder in your local copy of the repository. To register that model, repeat the steps in the previous two sections, but name the model `model-2`.

For more information about working with registered models, see [Work with registered models in Azure Machine Learning](how-to-manage-models.md).

For information about creating an environment in the studio, see [Create an environment](how-to-manage-environments-in-studio.md#create-an-environment).

### Create a managed online endpoint and the blue deployment

You can use Azure Machine Learning studio to create a managed online endpoint directly in your browser. When you create a managed online endpoint in the studio, you must define an initial deployment. You can't create an empty managed online endpoint.

One way to create a managed online endpoint in the studio is from the **Models** page. This method also provides an easy way to add a model to an existing managed online deployment. To deploy the model named `model-1` that you registered previously in the [Register your model](#register-your-model) section, take the steps in the following sections.

#### Select a model

1. Go to [Azure Machine Learning studio](https://ml.azure.com), and then select **Models**.

1. In the list, select the `model-1` model.

1. Select **Deploy** > **Real-time endpoint**.

    :::image type="content" source="media/how-to-safely-rollout-managed-endpoints/deploy-models-page.png" lightbox="media/how-to-safely-rollout-managed-endpoints/deploy-models-page.png" alt-text="Screenshot of the Model List page. In the model list, the model-1 model is selected. Deploy and Real-time endpoint are highlighted.":::
    
    A window opens that you can use to specify detailed information about your endpoint.

    :::image type="content" source="media/how-to-safely-rollout-managed-endpoints/online-endpoint-wizard.png" lightbox="media/how-to-safely-rollout-managed-endpoints/online-endpoint-wizard.png" alt-text="Screenshot of the Select endpoint page in the wizard for creating a managed online endpoint. An endpoint name and several settings are visible.":::

#### Configure initial settings

1. Under **Endpoint name**, enter a name for your endpoint.

1. Under **Compute type**, keep the default value of **Managed**.

1. Under **Authentication type**, keep the default value of **key-based authentication**.

1. Select **Next**, and then on the **Model** page, select **Next**.

#### Configure remaining settings and create the deployment

1. On the **Deployment** page, take the following steps:
    1. Under **Deployment name**, enter **blue**.
    1. If you want to view graphs of your endpoint activities in the studio later:
        1. Under **Inferencing data collection**, turn on the toggle.
        1. Under **Application Insights diagnostics**, turn on the toggle.
    1. Select **Next**.

1. On the **Code and environment for inferencing** page, take the following steps:
    1. Under **Select a scoring script for inferencing**, select **Browse**, and then select the \azureml-examples\cli\endpoints\online\model-1\onlinescoring\score.py file from the repository you cloned or downloaded earlier.
    1. In the search box above the list of environments, start entering **sklearn**, and then select the **sklearn-1.5:19** curated environment.
    1. Select **Next**.

1. On the **Compute** page, take the following steps:
    1. Under **Virtual machine**, keep the default value.
    1. Under **Instance count**, replace the default value with **1**.
    1. Select **Next**.

1. On the **Live Traffic** page, select **Next** to accept the default traffic allocation of 100 percent to the `blue` deployment.

1. On **Review**, review your deployment settings, and then select **Create**.

    :::image type="content" source="media/how-to-safely-rollout-managed-endpoints/review-deployment-creation-page.png" lightbox="media/how-to-safely-rollout-managed-endpoints/review-deployment-creation-page.png" alt-text="Screenshot of the review page in the wizard for creating a managed online endpoint. Settings information is visible, and Create is highlighted.":::

#### Create an endpoint from the Endpoints page

Alternatively, you can create a managed online endpoint from the **Endpoints** page in the studio.

1. Go to [Azure Machine Learning studio](https://ml.azure.com).

1. Select **Endpoints**.

1. Select **Create**.

    :::image type="content" source="media/how-to-safely-rollout-managed-endpoints/endpoint-create-managed-online-endpoint.png" lightbox="media/how-to-safely-rollout-managed-endpoints/endpoint-create-managed-online-endpoint.png" alt-text="Screenshot of the studio Endpoints page. Endpoints and Create are highlighted, and one endpoint is visible.":::

    A window opens where you can specify detailed information about your endpoint and deployment.

1. Select a model, and then select **Select**.

1. Enter settings for your endpoint and deployment as described in the previous two sections. In each step, use the default values. In the last step, select **Create** to create the deployment.

---

## Confirm your existing deployment

One way to confirm your existing deployment is to invoke your endpoint so that it can score your model for a given input request. When you invoke your endpoint via the Azure CLI or the Python SDK, you can choose to specify the name of the deployment to receive incoming traffic.

> [!NOTE]
> Unlike the Azure CLI or Python SDK, Azure Machine Learning studio requires you to specify a deployment when you invoke an endpoint.

### Invoke an endpoint with a deployment name

When you invoke an endpoint, you can specify the name of a deployment that you want to receive traffic. In this case, Azure Machine Learning routes the endpoint traffic directly to the specified deployment and returns its output. You can use the `--deployment-name` option [for the Azure Machine Learning CLI v2](/cli/azure/ml/online-endpoint#az-ml-online-endpoint-invoke-optional-parameters), or the `deployment_name` option [for the Python SDK v2](/python/api/azure-ai-ml/azure.ai.ml.operations.onlineendpointoperations#azure-ai-ml-operations-onlineendpointoperations-invoke) to specify the deployment.

### Invoke the endpoint without specifying a deployment

If you invoke the endpoint without specifying the deployment that you want to receive traffic, Azure Machine Learning routes the endpoint's incoming traffic to the deployments in the endpoint based on traffic control settings.

Traffic control settings allocate specified percentages of incoming traffic to each deployment in the endpoint. For example, if your traffic rules specify that a particular deployment in your endpoint should receive incoming traffic 40% of the time, Azure Machine Learning routes 40% of the endpoint traffic to that deployment.

# [Azure CLI](#tab/azure-cli)

To view the status of your existing endpoint and deployment, run the following commands:

```azurecli
az ml online-endpoint show --name $ENDPOINT_NAME 

az ml online-deployment show --name blue --endpoint $ENDPOINT_NAME 
```

The output lists information about the `$ENDPOINT_NAME` endpoint and the `blue` deployment.

### Test the endpoint by using sample data

You can invoke the endpoint by using the `invoke` command. The following command uses the [sample-request.json](https://github.com/Azure/azureml-examples/tree/main/cli/endpoints/online/model-1/sample-request.json) JSON file to send a sample request:

:::code language="azurecli" source="~/azureml-examples-main/cli/deploy-safe-rollout-online-endpoints.sh" ID="test_blue" :::

# [Python SDK](#tab/python)

Use the following code to check the status of the model deployment:

```python
ml_client.online_endpoints.get(name=online_endpoint_name)
```

### Test the endpoint by using sample data

You can use the `MLClient` instance that you created earlier to get a handle to the endpoint. To invoke the endpoint, use the `invoke` command with the following parameters:

* `endpoint_name`: The name of the endpoint.
* `request_file`: A file that contains request data.
* `deployment_name`: The name of a deployment to test in the endpoint.

The following code uses the [sample-request.json](https://github.com/Azure/azureml-examples/tree/main/sdk/python/endpoints/online/model-1/sample-request.json) JSON file to send a sample request.

[!notebook-python[](~/azureml-examples-main/sdk/python/endpoints/online/managed/online-endpoints-safe-rollout.ipynb?name=test_deployment)]

# [Studio](#tab/azure-studio)

### View managed online endpoints

You can view all your managed online endpoints in the studio endpoints page. The **Details** tab of each endpoint's page displays critical information, such as the endpoint URI, status, testing tools, activity monitors, deployment logs, and sample consumption code. To see this information, take the following steps:

1. In the studio, select **Endpoints**. A list of all the endpoints in the workspace is displayed.

1. Optionally, create a filter on the compute instance type to show only managed types.

1. Select an endpoint name to view the endpoint's **Details** page.

:::image type="content" source="media/how-to-safely-rollout-managed-endpoints/managed-endpoint-details-page.png" lightbox="media/how-to-safely-rollout-managed-endpoints/managed-endpoint-details-page.png" alt-text="Screenshot of the Details tab of an endpoint page. Information about a deployment and attributes are visible.":::

### Test the endpoint by using sample data

On the endpoint page, use the **Test** tab to test your managed online deployment. To enter sample input and view the results, take the following steps:

1. On the endpoint page, go to the **Test** tab. In the **Deployment** list, the `blue` deployment is already selected.

1. Go to the [sample-request.json file](https://github.com/Azure/azureml-examples/tree/main/sdk/python/endpoints/online/model-1/sample-request.json) and copy its sample input.

1. In the studio, paste the sample input into the **Input** box.

1. Select **Test**.

:::image type="content" source="media/how-to-safely-rollout-managed-endpoints/test-deployment.png" lightbox="media/how-to-safely-rollout-managed-endpoints/test-deployment.png" alt-text="Screenshot of the Test tab of an endpoint page. The blue deployment is selected, and input and output data is visible.":::

---

## Scale your existing deployment to handle more traffic

# [Azure CLI](#tab/azure-cli)

In the deployment described in [Deploy and score a machine learning model by using an online endpoint](how-to-deploy-online-endpoints.md), you set the `instance_count` value to `1` in the deployment YAML file. Scale out by using the `update` command:

:::code language="azurecli" source="~/azureml-examples-main/cli/deploy-safe-rollout-online-endpoints.sh" ID="scale_blue" :::

> [!NOTE]
> In the previous command, the `--set` option overrides the deployment configuration. Alternatively, you can update the YAML file and pass it as input to the `update` command by using the `--file` option.

# [Python SDK](#tab/python)

Use the `MLClient` instance that you created earlier to get a handle to the deployment. To scale the deployment, increase or decrease the value of `instance_count`.

[!notebook-python[](~/azureml-examples-main/sdk/python/endpoints/online/managed/online-endpoints-safe-rollout.ipynb?name=scale_deployment)]

### Get detailed information about the endpoint

[!notebook-python[](~/azureml-examples-main/sdk/python/endpoints/online/managed/online-endpoints-safe-rollout.ipynb?name=get_endpoint_details)]

# [Studio](#tab/azure-studio)

To scale the deployment up or down by adjusting the number of instances, take the following steps:

1. On the endpoint page, go to the **Details** tab, and find the card for the `blue` deployment.

1. On the header of the `blue` deployment card, select the edit icon.

1. Under **Instance count**, enter **2**.

1. Select **Update**.

:::image type="content" source="media/how-to-safely-rollout-managed-endpoints/scale-blue-deployment.png" alt-text="Screenshot of the Update deployment properties dialog. The Instance count value is two, and an Update button is visible." lightbox="media/how-to-safely-rollout-managed-endpoints/scale-blue-deployment.png":::

---

## Deploy a new model but don't send it traffic

# [Azure CLI](#tab/azure-cli)

Create a new deployment named `green`:

:::code language="azurecli" source="~/azureml-examples-main/cli/deploy-safe-rollout-online-endpoints.sh" ID="create_green" :::

Because you don't explicitly allocate any traffic to the `green` deployment, it has zero traffic allocated to it. You can verify that fact by using the following command:

:::code language="azurecli" source="~/azureml-examples-main/cli/deploy-safe-rollout-online-endpoints.sh" ID="get_traffic" :::

### Test the new deployment

Even though the `green` deployment has 0 percent of traffic allocated to it, you can invoke it directly by using the `--deployment` option:

:::code language="azurecli" source="~/azureml-examples-main/cli/deploy-safe-rollout-online-endpoints.sh" ID="test_green" :::

If you want to use a REST client to invoke the deployment directly without going through traffic rules, set the following HTTP header: `azureml-model-deployment: <deployment-name>`. The following code uses Client for URL (cURL) to invoke the deployment directly. You can run the code in a Unix or Windows Subsystem for Linux (WSL) environment. For instructions for retrieving the `$ENDPOINT_KEY` value, see [Get the key or token for data plane operations](how-to-authenticate-online-endpoint.md#get-the-key-or-token-for-data-plane-operations).

:::code language="azurecli" source="~/azureml-examples-main/cli/deploy-safe-rollout-online-endpoints.sh" ID="test_green_using_curl" :::

# [Python SDK](#tab/python)

Create a new deployment for your managed online endpoint, and name the deployment `green`:

[!notebook-python[](~/azureml-examples-main/sdk/python/endpoints/online/managed/online-endpoints-safe-rollout.ipynb?name=configure_new_deployment)]

[!notebook-python[](~/azureml-examples-main/sdk/python/endpoints/online/managed/online-endpoints-safe-rollout.ipynb?name=create_new_deployment)]

> [!NOTE]
> If you're creating a deployment for a Kubernetes online endpoint, use the `KubernetesOnlineDeployment` class, and specify a [Kubernetes instance type](how-to-manage-kubernetes-instance-types.md) in your Kubernetes cluster.

### Test the new deployment

Even though the `green` deployment has 0 percent of the traffic allocated to it, you can still invoke the endpoint and deployment. The following code uses the [sample-request.json](https://github.com/Azure/azureml-examples/tree/main/sdk/python/endpoints/online/model-2/sample-request.json) JSON file to send a sample request.

[!notebook-python[](~/azureml-examples-main/sdk/python/endpoints/online/managed/online-endpoints-safe-rollout.ipynb?name=test_new_deployment)]

# [Studio](#tab/azure-studio)

You can create a new deployment to add to your managed online endpoint. To create a deployment named `green`, follow the steps in the following sections.

### Configure initial settings

1. On the endpoint page, go to the **Details** tab, and then select **Add Deployment**.

1. On the **Select a model** page, select **model-2**, and then select **Select**.

1. On the **Endpoint** page and on the **Model** page, select **Next**.

1. On the **Deployment** page, take the following steps:
    1. Under **Deployment name**, enter **green**.
    1. Under **Inferencing data collection**, turn on the toggle.
    1. Under **Application Insights diagnostics**, turn on the toggle.
    1. Select **Next**.

1. On the **Code and environment for inferencing** page, take the following steps:
    1. Under **Select a scoring script for inferencing**, select **Browse**, and then select the \azureml-examples\cli\endpoints\online\model-2\onlinescoring\score.py file from the repository you cloned or downloaded earlier.
    1. In the search box above the list of environments, start entering **sklearn**, and then select the **sklearn-1.5:19** curated environment.
    1. Select **Next**.

1. On the **Compute** page, take the following steps:
    1. Under **Virtual machine**, keep the default value.
    1. Under **Instance count**, replace the default value with **1**.
    1. Select **Next**.

### Configure remaining settings and create the deployment

1. On **Live Traffic**, select **Next** to accept the default traffic allocation of 100 percent to the `blue` deployment and 0 percent to `green`.

1. On **Review**, review your deployment settings, and then select **Create**.

    :::image type="content" source="media/how-to-safely-rollout-managed-endpoints/add-green-deployment-endpoint-page.png" lightbox="media/how-to-safely-rollout-managed-endpoints/add-green-deployment-endpoints.png" alt-text="Screenshot of the Review page. Information about the endpoint, deployment, model, environment, compute instance, and traffic is visible.":::

### Add a deployment from the Models page

Alternatively, you can use the **Models** page to add a deployment:

1. In the studio, select **Models**.

1. Select a model in the list.

1. Select **Deploy** > **Real-time endpoint**.

1. Under **Endpoint**, select **Existing**.

1. In the list of endpoints, select the managed online endpoint that you want to deploy the model to, and then select **Next**.

    :::image type="content" source="media/how-to-safely-rollout-managed-endpoints/add-green-deployment-models-page.png" lightbox="media/how-to-safely-rollout-managed-endpoints/add-green-deployment-models-page.png" alt-text="Screenshot of the Select endpoint page. The Existing option, the Next button, and the checkmark next to an endpoint are highlighted.":::

1. On the **Model** page, select **Next**.

1. To finish creating the `green` deployment, follow steps 4 through 6 in the [Configure initial settings](#configure-initial-settings) section and all the steps in the [Configure remaining settings and create the deployment](#configure-remaining-settings-and-create-the-deployment) section.

> [!NOTE]
> When you add a new deployment to an endpoint, you can use the **Update traffic allocation** page to adjust the traffic balance between the deployments. To follow the rest of the procedures in this article, keep the default traffic allocation of 100 percent to the `blue` deployment for now and 0 percent to the `green` deployment.

### Test the new deployment

Even though 0 percent of the traffic goes to the `green` deployment, you can still invoke the endpoint and that deployment. On the endpoint page, use the **Test** tab to test your managed online deployment. To enter sample input and view the results, take the following steps:

1. On the endpoint page, go to the **Test** tab.

1. In the **Deployment** list, select **green**.

1. Go to the [sample-request.json file](https://github.com/Azure/azureml-examples/tree/main/sdk/python/endpoints/online/model-2/sample-request.json) and copy its sample input.

1. In the studio, paste the sample input into the **Input** box.

1. Select **Test**.

---

## Test the deployment with mirrored traffic

After you test your `green` deployment, you can *mirror* a percentage of the live traffic to your endpoint by copying that percentage of traffic and sending it to the `green` deployment. Traffic mirroring, which is also called *shadowing*, doesn't change the results returned to clients. All requests still flow to the `blue` deployment. The mirrored percentage of the traffic is copied and also submitted to the `green` deployment so that you can gather metrics and logging without impacting your clients.

Mirroring is useful when you want to validate a new deployment without impacting clients. For example, you can use mirroring to check whether latency is within acceptable bounds or to check that there are no HTTP errors. The use of traffic mirroring, or shadowing, to test a new deployment is also known as [shadow testing](https://microsoft.github.io/code-with-engineering-playbook/automated-testing/shadow-testing/). The deployment that receives the mirrored traffic, in this case, the `green` deployment, can also be called the *shadow deployment*.

Mirroring has the following limitations:

* Mirroring is supported for versions 2.4.0 and later of the Azure Machine Learning CLI and versions 1.0.0 and later of the Python SDK. If you use an older version of the Azure Machine Learning CLI or the Python SDK to update an endpoint, you lose the mirror traffic setting.
* Mirroring isn't currently supported for Kubernetes online endpoints.
* You can mirror traffic to only one deployment in an endpoint.
* The maximum percentage of traffic you can mirror is 50 percent. This cap limits the effect on your [endpoint bandwidth quota](how-to-manage-quotas.md#azure-machine-learning-online-endpoints-and-batch-endpoints), which has a default value of 5 MBps. Your endpoint bandwidth is throttled if you exceed the allocated quota. For information about monitoring bandwidth throttling, see [Bandwidth throttling](how-to-monitor-online-endpoints.md#bandwidth-throttling).

Also note the following behavior:

* You can configure a deployment to receive only live traffic or mirrored traffic, not both.
* When you invoke an endpoint, you can specify the name of any of its deployments - even a shadow deployment - to return the prediction.
* When you invoke an endpoint and specify the name of a deployment to receive incoming traffic, Azure Machine Learning doesn't mirror traffic to the shadow deployment. Azure Machine Learning mirrors traffic to the shadow deployment from traffic sent to the endpoint when you don't specify a deployment.

If you set the `green` deployment to receive 10 percent of mirrored traffic, clients still receive predictions from the `blue` deployment only.

:::image type="content" source="./media/how-to-safely-rollout-managed-endpoints/endpoint-concept-mirror.png" alt-text="Diagram that shows traffic flow through an endpoint. All traffic goes to the blue deployment, and 10 percent is mirrored to the green deployment.":::

# [Azure CLI](#tab/azure-cli)

Use the following command to mirror 10 percent of the traffic and send it to the `green` deployment:

:::code language="azurecli" source="~/azureml-examples-main/cli/deploy-safe-rollout-online-endpoints.sh" ID="test_green_with_mirror_traffic" :::

To test mirrored traffic, invoke the endpoint several times without specifying a deployment. The endpoint routes the incoming traffic:

```azurecli
for i in {1..20} ; do
    az ml online-endpoint invoke --name $ENDPOINT_NAME --request-file endpoints/online/model-1/sample-request.json
done
```

You can confirm that the specified percentage of the traffic is sent to the `green` deployment by checking the logs from the deployment.

```azurecli
az ml online-deployment get-logs --name green --endpoint $ENDPOINT_NAME
```

After testing, set the mirror traffic to zero to disable mirroring:

:::code language="azurecli" source="~/azureml-examples-main/cli/deploy-safe-rollout-online-endpoints.sh" ID="reset_mirror_traffic" :::

# [Python SDK](#tab/python)

Use the following code to mirror 10 percent of the traffic and send it to the `green` deployment:

[!notebook-python[](~/azureml-examples-main/sdk/python/endpoints/online/managed/online-endpoints-safe-rollout.ipynb?name=new_deployment_traffic)]

To test mirrored traffic, invoke the endpoint several times without specifying a deployment. The endpoint routes the incoming traffic:
[!notebook-python[](~/azureml-examples-main/sdk/python/endpoints/online/managed/online-endpoints-safe-rollout.ipynb?name=several_tests_to_mirror_traffic)]

You can confirm that the specified percentage of the traffic is sent to the `green` deployment by checking the logs from the deployment.

```python
ml_client.online_deployments.get_logs(
    name="green", endpoint_name=online_endpoint_name, lines=50
)
```

After testing, set the mirror traffic to zero to disable mirroring:

[!notebook-python[](~/azureml-examples-main/sdk/python/endpoints/online/managed/online-endpoints-safe-rollout.ipynb?name=disable_traffic_mirroring)]

# [Studio](#tab/azure-studio)

To mirror 10% of the traffic and send it to the `green` deployment, take the following steps:

1. On the endpoint page, go to the **Details** tab, and then select **Update traffic**.

1. Turn on the **Enable mirrored traffic** toggle.

1. In the **Deployment name** list, select **green**.

1. Under **Traffic allocation %**, keep the default value of 10%.

1. Select **Update**.

:::image type="content" source="media/how-to-safely-rollout-managed-endpoints/mirror-traffic-green-deployment.png" alt-text="Screenshot of the Update traffic allocation dialog. The allocation for the green deployment is 10 percent, and mirroring is turned on." lightbox="media/how-to-safely-rollout-managed-endpoints/mirror-traffic-green-deployment.png":::

The endpoint details page now shows a mirrored traffic allocation of 10% to the `green` deployment.

:::image type="content" source="media/how-to-safely-rollout-managed-endpoints/endpoint-details-showing-mirrored-traffic-allocation.png" alt-text="Screenshot of the Details tab of an endpoint page. In the mirrored traffic allocation, the green deployment percentage is 10 percent of traffic." lightbox="media/how-to-safely-rollout-managed-endpoints/endpoint-details-showing-mirrored-traffic-allocation.png":::

To test mirrored traffic, see the Azure CLI or Python tabs to invoke the endpoint several times. Confirm that the specified percentage of traffic is sent to the `green` deployment by checking the logs from the deployment. You can access the deployment logs on the endpoint page by going to the **Logs** tab.

You can also use metrics and logs to monitor the performance of the mirrored traffic. For more information, see [Monitor online endpoints](how-to-monitor-online-endpoints.md).

After testing, you can disable mirroring by taking the following steps:

1. On the endpoint page, go to the **Details** tab, and then select **Update traffic**.

1. Turn off the **Enable mirrored traffic** toggle.

1. Select **Update**.

:::image type="content" source="media/how-to-safely-rollout-managed-endpoints/endpoint-details-showing-disabled-mirrored-traffic.png" alt-text="Screenshot of the Details tab of an endpoint page. In the live traffic allocation, the blue deployment gets 100 percent. No traffic is mirrored." lightbox="media/how-to-safely-rollout-managed-endpoints/endpoint-details-showing-disabled-mirrored-traffic.png":::

---

## Allocate a small percentage of live traffic to the new deployment

After you test your `green` deployment, allocate a small percentage of traffic to it:

# [Azure CLI](#tab/azure-cli)

:::code language="azurecli" source="~/azureml-examples-main/cli/deploy-safe-rollout-online-endpoints.sh" ID="green_10pct_traffic" :::

# [Python SDK](#tab/python)

[!notebook-python[](~/azureml-examples-main/sdk/python/endpoints/online/managed/online-endpoints-safe-rollout.ipynb?name=allocate_some_traffic)]

# [Studio](#tab/azure-studio)

1. On the endpoint page, go to the **Details** tab, and then select  **Update traffic**.

1. Adjust the deployment traffic by allocating 10 percent to the `green` deployment and 90 percent to the `blue` deployment.

1. Select **Update**.

---

> [!TIP]
> The total traffic percentage must be either 0 percent, to disable traffic, or 100 percent, to enable traffic.

Your `green` deployment now receives 10 percent of all live traffic. Clients receive predictions from both the `blue` and `green` deployments.

:::image type="content" source="./media/how-to-safely-rollout-managed-endpoints/endpoint-concept.png" alt-text="Diagram that shows traffic flow through an endpoint. The blue deployment receives 90 percent of the traffic, and the green deployment, 10 percent.":::

## Send all traffic to the new deployment

When you're fully satisfied with your `green` deployment, switch all traffic to it.

# [Azure CLI](#tab/azure-cli)

:::code language="azurecli" source="~/azureml-examples-main/cli/deploy-safe-rollout-online-endpoints.sh" ID="green_100pct_traffic" :::

# [Python SDK](#tab/python)

[!notebook-python[](~/azureml-examples-main/sdk/python/endpoints/online/managed/online-endpoints-safe-rollout.ipynb?name=allocate_all_traffic)]

# [Studio](#tab/azure-studio)

1. On the endpoint page, go to the **Details** tab, and then select **Update traffic**.

1. Adjust the deployment traffic by allocating 100 percent to the `green` deployment and 0 percent to the `blue` deployment.

1. Select **Update**.

---

## Remove the old deployment

Use the following steps to delete an individual deployment from a managed online endpoint. Deleting an individual deployment doesn't affect the other deployments in the managed online endpoint:

# [Azure CLI](#tab/azure-cli)

:::code language="azurecli" source="~/azureml-examples-main/cli/deploy-safe-rollout-online-endpoints.sh" ID="delete_blue" :::

# [Python SDK](#tab/python)

[!notebook-python[](~/azureml-examples-main/sdk/python/endpoints/online/managed/online-endpoints-safe-rollout.ipynb?name=remove_old_deployment)]

# [Studio](#tab/azure-studio)

> [!NOTE]
> You can't delete a deployment that has live traffic allocated to it. Before you delete the deployment, [set the traffic allocation](#send-all-traffic-to-the-new-deployment) for the deployment to 0 percent.

1. On the endpoint page, go to the **Details** tab, and then go to the `blue` deployment card.

1. Next to the deployment name, select the delete icon.

---

## Delete the endpoint and deployment

If you aren't going to use the endpoint and deployment, delete them. When you delete an endpoint, you also delete all its underlying deployments.

# [Azure CLI](#tab/azure-cli)

:::code language="azurecli" source="~/azureml-examples-main/cli/deploy-safe-rollout-online-endpoints.sh" ID="delete_endpoint" :::

# [Python SDK](#tab/python)

[!notebook-python[](~/azureml-examples-main/sdk/python/endpoints/online/managed/online-endpoints-safe-rollout.ipynb?name=delete_endpoint)]

# [Studio](#tab/azure-studio)

1. Go to [Azure Machine Learning studio](https://ml.azure.com).

1. Select **Endpoints**.

1. Select an endpoint in the list.

1. Select **Delete**.

Alternatively, you can delete a managed online endpoint directly on the endpoint page. Go to the **Details** tab and select the delete icon.

---

## Related content

- [Deploy models with REST](how-to-deploy-with-rest.md)
- [Online endpoint samples](https://github.com/Azure/azureml-examples/tree/v2samplesreorg/sdk/python/endpoints)
- [Use network isolation with managed online endpoints](how-to-secure-online-endpoint.md)
- [Access Azure resources from an online endpoint with a managed identity](how-to-access-resources-from-endpoints-managed-identities.md)