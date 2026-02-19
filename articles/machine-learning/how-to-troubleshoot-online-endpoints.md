---
title: Troubleshoot online endpoint deployment
titleSuffix: Azure Machine Learning
description: Learn how to troubleshoot online endpoint deployment and scoring issues and understand common deployment errors.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: inferencing
author: s-polly
ms.author: scottpolly
ms.reviewer: jturuk
ms.date: 10/06/2025
ms.topic: troubleshooting
ms.custom:
  - devplatv2
  - devx-track-azurecli
  - cliv2
  - sdkv2
  - sfi-image-nochange
#Customer intent: As a data scientist, I want to figure out why my online endpoint deployment failed so that I can fix it.
---

# Troubleshoot online endpoint deployment and scoring

[!INCLUDE [dev v2](includes/machine-learning-dev-v2.md)]

This article describes how to troubleshoot and resolve common Azure Machine Learning online endpoint deployment and scoring issues.

The document structure reflects the way you should approach troubleshooting:

1. Use [local deployment](#deploy-locally) to test and debug your models locally before deploying in the cloud.
1. Use [container logs](#get-container-logs) to help debug issues.
1. Understand [common deployment errors](#common-deployment-errors) that might arise and how to fix them.

The [HTTP status codes](#http-status-codes) section explains how invocation and prediction errors map to HTTP status codes when you score endpoints with REST requests.

## Prerequisites

- An active Azure subscription with the free or paid version of Azure Machine Learning. [Get a free trial Azure subscription](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

# [Azure CLI](#tab/cli)

- An Azure Machine Learning workspace.
- The [Azure CLI](/cli/azure/install-azure-cli) and Azure Machine Learning CLI v2. [Install, set up, and use the CLI (v2)](how-to-configure-cli.md).

# [Python SDK](#tab/python)

- An Azure Machine Learning workspace.
- The Azure Machine Learning Python SDK v2. [Install the Azure Machine Learning SDK v2 for Python](/python/api/overview/azure/ai-ml-readme).

### [Studio](#tab/studio)

- An Azure Machine Learning workspace.

---

## Request tracing

There are two supported tracing headers:

- `x-request-id` is reserved for server tracing. Azure Machine Learning overrides this header to ensure it's a valid GUID. When you create a support ticket for a failed request, attach the failed request ID to expedite the investigation. Alternatively, provide the name of the region and the endpoint name.

- `x-ms-client-request-id` is available for client tracing scenarios. This header accepts only alphanumeric characters, hyphens, and underscores, and is truncated to a maximum of 40 characters.

## Deploy locally

Local deployment means to deploy a model to a local Docker environment. Local deployment supports creation, update, and deletion of a local endpoint, and allows you to invoke and get logs from the endpoint. Local deployment is useful for testing and debugging before deployment to the cloud.

> [!TIP]
> You can also use the [Azure Machine Learning inference HTTP server Python package](how-to-inference-server-http.md) to debug your scoring script locally. Debugging with the inference server helps you to debug the scoring script before deploying to local endpoints so that you can debug without being affected by the deployment container configurations.

You can deploy locally with Azure CLI or Python SDK. Azure Machine Learning studio doesn't support local deployment or local endpoints.

# [Azure CLI](#tab/cli)

To use local deployment, add `--local` to the appropriate command.

```azurecli
az ml online-deployment create --endpoint-name <endpoint-name> -n <deployment-name> -f <spec_file.yaml> --local
```

# [Python SDK](#tab/python)

For local deployment, use the  `local=True` parameter. In this command,`ml_client` is the instance for `MLCLient` class, and `online_deployment` is the instance for either the `ManagedOnlineDeployment` class or the `KubernetesOnlineDeployment` class.

```python
ml_client.begin_create_or_update(online_deployment, local=True)
```

### [Studio](#tab/studio)

Azure Machine Learning studio doesn't support local deployment.

---

The following steps occur during local deployment:

1. Docker either builds a new container image or pulls an existing image from the local Docker cache. Docker uses an existing image if one matches the environment part of the specification file.
1. Docker starts the new container with mounted local artifacts such as model and code files.

For more information, see [Deploy and debug locally by using a local endpoint](how-to-deploy-managed-online-endpoints.md#deploy-and-debug-locally-by-using-a-local-endpoint).

> [!TIP]
> You can use Visual Studio Code to test and debug your endpoints locally. For more information, see [Debug online endpoints locally in Visual Studio Code](how-to-debug-managed-online-endpoints-visual-studio-code.md).

## Get container logs

You can't get direct access to a virtual machine (VM) where a model deploys, but you can get logs from some of the containers that are running on the VM. The amount of information you get depends on the provisioning status of the deployment. If the specified container is up and running, you see its console output. Otherwise, you get a message to try again later.

You can get logs from the following types of containers:

- The [inference server](how-to-inference-server-http.md) console log contains the output of print and logging functions from your scoring script *score.py* code.
- Storage initializer logs contain information on whether code and model data successfully downloaded to the container. The container runs before the inference server container starts to run.

For Kubernetes online endpoints, administrators can directly access the cluster where you deploy the model and check the logs in Kubernetes. For example:

```bash
kubectl -n <compute-namespace> logs <container-name>
```

> [!NOTE]
> If you use Python logging, make sure to use the correct logging level, such as `INFO`, for the messages to be published to logs.

### See log output from containers

# [Azure CLI](#tab/cli)

To see log output from a container, use the following command:

```azurecli
az ml online-deployment get-logs -g <resource-group> -w <workspace-name> -e <endpoint-name> -n <deployment-name> -l 100
```

Or

```azurecli
az ml online-deployment get-logs --resource-group <resource-group> --workspace-name <workspace-name> --endpoint-name <endpoint-name> --name <deployment-name> --lines 100
```

By default, logs are pulled from the inference server. You can get logs from the storage initializer container by passing `–-container storage-initializer`.

The commands above include `--resource-group` and `--workspace-name`. You can also set these parameters globally via `az configure` to avoid repeating them in each command. For example:

```azurecli
az configure --defaults group=<resource-group> workspace=<workspace-name>
```

To check your current configuration settings, run:

```azurecli
az configure --list-defaults
```

To see more information, add `--help`  or `--debug` to commands.

# [Python SDK](#tab/python)

To see log output from containers, use the `get_logs` method as follows. For information about how to set the parameters, see the [get-logs](/python/api/azure-ai-ml/azure.ai.ml.operations.onlinedeploymentoperations#azure-ai-ml-operations-onlinedeploymentoperations-get-logs) reference.

```python
ml_client.online_deployments.get_logs(
    name="<deployment-name>", endpoint_name="<endpoint-name>", lines=100
)
```

By default, logs are pulled from the inference server. You can get logs from the storage initializer container by adding the `container_type="storage-initializer"` option. 

```python
ml_client.online_deployments.get_logs(
    name="<deployment-name>", endpoint_name="<endpoint-name>", lines=100, container_type="storage-initializer"
)
```

### [Studio](#tab/studio)

<a name="see-log-output-in-azure-machine-learning-studio"></a>
To view log output from a container in Azure Machine Learning studio:

1. Select **Endpoints** in the left pane.
1. Select an endpoint name to view the endpoint details page.
1. Select the **Logs** tab in the endpoint details page.
1. Select the deployment log you want to see from the dropdown menu.

:::image type="content" source="media/how-to-troubleshoot-online-endpoints/deployment-logs.png" lightbox="media/how-to-troubleshoot-online-endpoints/deployment-logs.png" alt-text="A screenshot of observing deployment logs in the studio.":::

The logs are pulled from the inference server. To get logs from the storage initializer container, use the Azure CLI or Python SDK commands.

---

## Common deployment errors

Deployment operation status can report the following common deployment errors:

- [ImageBuildFailure](#error-imagebuildfailure)
  - [Azure Container Registry authorization failure](#azure-container-registry-authorization-failure)
  - [Image build compute not set in a private workspace with virtual network](#image-build-compute-not-set-in-a-private-workspace-with-virtual-network)
  - [Image build timing out](#image-build-timing-out)
  - [Generic or unknown failure](#generic-image-build-failure)
- [OutOfQuota](#error-outofquota)
  - [CPU](#cpu-quota)
  - [Cluster](#cluster-quota)
  - [Disk](#disk-quota)
  - [Memory](#memory-quota)
  - [Role assignments](#role-assignment-quota)
  - [Endpoints](#endpoint-quota)
  - [Region-wide VM capacity](#region-wide-vm-capacity)
  - [Other](#other-quota)
- [BadArgument](#error-badargument)

  Common to both managed online endpoint and Kubernetes online endpoint:
  - [Subscription doesn't exist](#subscription-doesnt-exist)
  - [Startup task failed due to authorization error](#authorization-error)
  - [Startup task failed due to incorrect role assignments on resource](#authorization-error)
  - [Startup task failed due to incorrect role assignments on storage account when mdc is enabled](#authorization-error)
  - [Invalid template function specification](#invalid-template-function-specification)
  - [Unable to download user container image](#unable-to-download-user-container-image)
  - [Unable to download user model](#unable-to-download-user-model)
  
  Limited to Kubernetes online endpoint:
  
  - [Resource request was greater than limits](#resource-requests-greater-than-limits)
  - [Azureml-fe for Kubernetes online endpoint isn't ready](#azureml-fe-not-ready)
  
- [ResourceNotReady](#error-resourcenotready)
- [ResourceNotFound](#error-resourcenotfound)
  - [Azure Resource Manager can't find a required resource](#resource-manager-cant-find-a-resource)
  - [Container registry is private or otherwise inaccessible](#container-registry-authorization-error)
- [WorkspaceManagedNetworkNotReady](#error-workspacemanagednetworknotready)
- [OperationCanceled](#error-operationcanceled)
  - [Operation was canceled by another operation that has a higher priority](#operation-canceled-by-another-higher-priority-operation)
  - [Operation was canceled due to a previous operation waiting for lock confirmation](#operation-canceled-waiting-for-lock-confirmation)
- [SecretsInjectionError](#error-secretsinjectionerror)
- [InternalServerError](#error-internalservererror)

If you're creating or updating a Kubernetes online deployment, also see [Common errors specific to Kubernetes deployments](#common-errors-specific-to-kubernetes-deployments).

### ERROR: ImageBuildFailure

This error is returned when the Docker image environment is being built. You can check the build log for more information on the failure. The build log is located in the default storage for your Azure Machine Learning workspace.

The exact location might be returned as part of the error, for example `"the build log under the storage account '[storage-account-name]' in the container '[container-name]' at the path '[path-to-the-log]'"`.

The following sections describe common image build failure scenarios:

- [Azure Container Registry authorization failure](#azure-container-registry-authorization-failure)
- [Image build compute not set in a private workspace with virtual network](#image-build-compute-not-set-in-a-private-workspace-with-virtual-network)
- [Image build timing out](#image-build-timing-out)
- [Generic or unknown failure](#generic-image-build-failure)

#### Azure Container Registry authorization failure

An error message mentions `"container registry authorization failure"` when you can't access the container registry with the current credentials. The desynchronization of workspace resource keys can cause this error, and it takes some time to automatically synchronize. However, you can manually call for key synchronization with [az ml workspace sync-keys](/cli/azure/ml/workspace#az-ml-workspace-sync-keys), which might resolve the authorization failure.

Container registries that are behind a virtual network might also encounter this error if they're set up incorrectly. Verify that the virtual network is set up properly.

#### Image build compute not set in a private workspace with virtual network

If the error message mentions `"failed to communicate with the workspace's container registry"`, and you're using a virtual network, and the workspace's container registry is private and configured with a private endpoint, you need to [allow Container Registry to build images](how-to-managed-network.md#configure-image-builds) in the virtual network.

#### Image build timing out

Image build timeouts are often due to an image being too large to be able to complete building within the deployment creation timeframe. Check your image build logs at the location that the error specifies. The logs are cut off at the point that the image build timed out.

To resolve this issue, [build your image separately](/azure/devops/pipelines/ecosystems/containers/publish-to-acr?view=azure-devops&tabs=javascript%2Cportal%2Cmsi&preserve-view=true) so the image only needs to be pulled during deployment creation. Also review the default [probe settings](reference-yaml-deployment-managed-online.md#probesettings) if you have ImageBuild timeouts.

#### Generic image build failure

Check the build log for more information on the failure. If no obvious error is found in the build log and the last line is `Installing pip dependencies: ...working...`, a dependency might be causing the error. Pinning version dependencies in your conda file can fix this problem.

Try [deploying locally](#deploy-locally) to test and debug your models before deploying to the cloud.

### ERROR: OutOfQuota

The following resources might run out of quota when using Azure services:

- [CPU](#cpu-quota)
- [Cluster](#cluster-quota)
- [Disk](#disk-quota)
- [Memory](#memory-quota)
- [Role assignments](#role-assignment-quota)
- [Endpoints](#endpoint-quota)
- [Region-wide VM capacity](#region-wide-vm-capacity)
- [Other](#other-quota)

For Kubernetes online endpoints only, the [Kubernetes resource](#kubernetes-quota) might also run out of quota.

#### CPU quota

You need to have enough compute quota to deploy a model. The CPU quota defines how many virtual cores are available per subscription, per workspace, per SKU, and per region. Each deployment subtracts from available quota and adds it back after deletion, based on type of the SKU.

You can check if there are unused deployments you can delete, or you can [submit a request for a quota increase](how-to-manage-quotas.md#request-quota-and-limit-increases).

#### Cluster quota

The `OutOfQuota` error occurs when you don't have enough Azure Machine Learning compute cluster quota. The quota defines the total number of clusters per subscription that you can use at the same time to deploy CPU or GPU nodes in the Azure cloud.

#### Disk quota

The `OutOfQuota` error occurs when the size of the model is larger than the available disk space and the model can't be downloaded. Try using a [SKU](reference-managed-online-endpoints-vm-sku-list.md) with more disk space or reducing the image and model size.

#### Memory quota
The `OutOfQuota` error occurs when the memory footprint of the model is larger than the available memory. Try a [SKU](reference-managed-online-endpoints-vm-sku-list.md) with more memory.

#### Role assignment quota

When you create a managed online endpoint, role assignment is required for the [managed identity](/azure/active-directory/managed-identities-azure-resources/overview) to access workspace resources. If you hit the [role assignment limit](/azure/azure-resource-manager/management/azure-subscription-service-limits#azure-rbac-limits), try to delete some unused role assignments in this subscription. You can check all role assignments by selecting **Access control** for your Azure subscription in the Azure portal.

#### Endpoint quota

Try to delete some unused endpoints in this subscription. If all your endpoints are actively in use, try [requesting an endpoint limit increase](how-to-manage-quotas.md#endpoint-limit-increases). To learn more about the endpoint limit, see [Endpoint quota with Azure Machine Learning online endpoints and batch endpoints](how-to-manage-quotas.md#azure-machine-learning-online-endpoints-and-batch-endpoints).

#### Kubernetes quota

The `OutOfQuota` error occurs when the requested CPU or memory can't be provided due to nodes being unschedulable for this deployment. For example, nodes might be cordoned or otherwise unavailable.

The error message typically indicates the resource insufficiency in the cluster, for example `OutOfQuota: Kubernetes unschedulable. Details:0/1 nodes are available: 1 Too many pods...`. This message means that there are too many pods in the cluster and not enough resources to deploy the new model based on your request.

Try the following mitigations to address this issue:

- IT operators who maintain the Kubernetes cluster can try to add more nodes or clear some unused pods in the cluster to release some resources.
- Machine learning engineers who deploy models can try to reduce the resource request of the deployment.

  - If you directly define the resource request in the deployment configuration via the resource section, try to reduce the resource request.
  - If you use `instance_type` to define resource for model deployment, contact the IT operator to adjust the instance type resource configuration. For more information, see [Create and manage instance types](how-to-manage-kubernetes-instance-types.md).

#### Region-wide VM capacity

Due to a lack of Azure Machine Learning capacity in the region, the service failed to provision the specified VM size. Retry later or try deploying to a different region.

#### Other quota

To run the *score.py* file you provide as part of the deployment, Azure creates a container that includes all the resources that the *score.py* needs. Azure Machine Learning then runs the scoring script on that container. If your container can't start, scoring can't happen. The container might be requesting more resources than the `instance_type` can support. Consider updating the `instance_type` of the online deployment.

To get the exact reason for the error, take the following action.

# [Azure CLI](#tab/cli)

Run the following command:

```azurecli
az ml online-deployment get-logs -e <endpoint-name> -n <deployment-name> -l 100
```

# [Python SDK](#tab/python)

Run the following command:

```python
ml_client.online_deployments.get_logs(
    name="<deployment-name>", endpoint_name="<endpoint-name>", lines=100
)
```

### [Studio](#tab/studio)

[Check the deployment log output in Azure Machine Learning studio](#see-log-output-in-azure-machine-learning-studio).

---

### ERROR: BadArgument

You might get this error when you use either managed online endpoints or Kubernetes online endpoints, for the following reasons:

- [Subscription doesn't exist](#subscription-doesnt-exist)
- [Startup task failed due to authorization error](#authorization-error)
- [Startup task failed due to incorrect role assignments on resource](#authorization-error)
- [Invalid template function specification](#invalid-template-function-specification)
- [Unable to download user container image](#unable-to-download-user-container-image)
- [Unable to download user model](#unable-to-download-user-model)
- [MLflow model format with private network is unsupported](#mlflow-model-format-with-private-network-is-unsupported)

You might also get this error when using Kubernetes online endpoints only, for the following reasons:

- [Resource request was greater than limits](#resource-requests-greater-than-limits)
- [Azureml-fe for kubernetes online endpoint isn't ready](#azureml-fe-not-ready)

#### Subscription doesn't exist

The referenced Azure subscription must be existing and active. This error occurs when Azure can't find the subscription ID you entered. The error might be due to a typo in the subscription ID. Double-check that the subscription ID was correctly entered and is currently active.

#### Authorization error

After you provision the compute resource when you create a deployment, Azure pulls the user container image from the workspace container registry and mounts the user model and code artifacts into the user container from the workspace storage account. Azure uses [managed identities](/azure/active-directory/managed-identities-azure-resources/overview) to access the storage account and the container registry.

If you create the associated endpoint with user-assigned identity, the user's managed identity must have **Storage blob data reader** permission on the workspace storage account and **AcrPull** permission on the workspace container registry. Make sure your user-assigned identity has the right permissions.

When MDC is enabled, the user's managed identity must have **Storage Blob Data Contributor** permission on the workspace storage account. For more information, see [Storage Blob Authorization Error when MDC is enabled](how-to-collect-production-data.md#collect-data-to-a-custom-blob-storage-container).

If you create the associated endpoint with system-assigned identity, Azure role-based access control (RBAC) permission is automatically granted and no further permissions are needed. For more information, see [Container registry authorization error](#container-registry-authorization-error).

#### Invalid template function specification

This error occurs when a template function was specified incorrectly. Either fix the policy or remove the policy assignment to unblock. The error message might include the policy assignment name and the policy definition to help you debug this error. See [Azure policy definition structure](https://aka.ms/policy-avoiding-template-failures) for tips to avoid template failures.

#### Unable to download user container image

The user container might not be found. [Check the container logs](#get-container-logs) to get more details.

Make sure the container image is available in the workspace container registry. For example, if the image is `testacr.azurecr.io/azureml/azureml_92a029f831ce58d2ed011c3c42d35acb:latest`, you can use the following command to check the repository:

```azurecli
az acr repository show-tags -n testacr --repository azureml/azureml_92a029f831ce58d2ed011c3c42d35acb --orderby time_desc --output table`
```

#### Unable to download user model

The user model might not be found. [Check the container logs](#get-container-logs) to get more details. Make sure you registered the model to the same workspace as the deployment.

To show details for a model in a workspace, take the following action. You must specify either version or label to get the model information.

# [Azure CLI](#tab/cli)

Run the following command:

 ```azurecli
az ml model show --name <model-name> --version <version>
```

# [Python SDK](#tab/python)

Run the following command:

```python
ml_client.models.get(name="<model-name>", version=<version>)
```

### [Studio](#tab/studio)

Select a model on the Azure Machine Learning studio **Models** page.

---

Also check if the blobs are present in the workspace storage account. For example, if the blob is `https://foobar.blob.core.windows.net/210212154504-1517266419/WebUpload/210212154504-1517266419/GaussianNB.pkl`, you can use the following command to check if the blob exists:

```azurecli
az storage blob exists --account-name <storage-account-name> --container-name <container-name> --name WebUpload/210212154504-1517266419/GaussianNB.pkl --subscription <sub-name>
```

If the blob is present, you can use the following command to get the logs from the storage initializer:

# [Azure CLI](#tab/cli)

```azurecli
az ml online-deployment get-logs --endpoint-name <endpoint-name> --name <deployment-name> –-container storage-initializer`
```

# [Python SDK](#tab/python)

```python
ml_client.online_deployments.get_logs(
  name="<deployment-name>", endpoint_name="<endpoint-name>", lines=100, container_type="storage-initializer"
)
```

### [Studio](#tab/studio)

You can't see logs from the storage initializer in the studio. Use the Azure CLI or Python SDK commands.

---

#### MLflow model format with private network is unsupported

You can't use the private network feature with an MLflow model format if you're using the [legacy network isolation method for managed online endpoints](concept-secure-online-endpoint.md#secure-outbound-access-with-legacy-network-isolation-method). If you need to deploy an MLflow model with the no-code deployment approach, try using a [workspace managed virtual network](concept-secure-online-endpoint.md#secure-outbound-access-with-workspace-managed-virtual-network).

#### Resource requests greater than limits

Requests for resources must be less than or equal to limits. If you don't set limits, Azure Machine Learning sets default values when you attach your compute to a workspace. You can check the limits in the Azure portal or by using the `az ml compute show` command.

#### Azureml-fe not ready

The front-end `azureml-fe` component that routes incoming inference requests to deployed services installs during [k8s-extension](/cli/azure/k8s-extension) installation and automatically scales as needed. This component should have at least one healthy replica on the cluster.

You get this error if the component isn't available when you trigger a Kubernetes online endpoint or deployment creation or update request. Check the pod status and logs to fix this issue. You can also try to update the k8s-extension installed on the cluster.

### ERROR: ResourceNotReady

To run the *score.py* file you provide as part of the deployment, Azure creates a container that includes all the resources that the *score.py* needs, and runs the scoring script on that container. The error in this scenario is that this container crashes when running, so scoring can't happen. This error can occur under one of the following conditions:

- There's an error in *score.py*. Use `get-logs` to diagnose common problems, such as:
  - A package that *score.py* tries to import that isn't included in the conda environment
  - A syntax error
  - A failure in the `init()` method

  If `get-logs` doesn't produce any logs, it usually means that the container failed to start. To debug this issue, try [deploying locally](#deploy-locally).
  
- Readiness or liveness probes aren't set up correctly.

- Container initialization takes too long, so the readiness or liveness probe fails beyond the failure threshold. In this case, adjust [probe settings](reference-yaml-deployment-managed-online.md#probesettings) to allow a longer time to initialize the container. Or try a bigger [supported VM SKU](reference-managed-online-endpoints-vm-sku-list.md), which accelerates the initialization.

- There's an error in the container environment setup, such as a missing dependency.

  If you get the `TypeError: register() takes 3 positional arguments but 4 were given` error, check the dependency between flask v2 and `azureml-inference-server-http`. For more information, see [Troubleshoot HTTP server issues](how-to-inference-server-http.md#typeerror-during-inference-server-startup).

### ERROR: ResourceNotFound

You might get this error when using either managed online endpoint or Kubernetes online endpoint, for the following reasons:

* [Azure Resource Manager can't find a required resource](#resource-manager-cant-find-a-resource)
* [Container registry is private or otherwise inaccessible](#container-registry-authorization-error)

#### Resource Manager can't find a resource

This error occurs when Azure Resource Manager can't find a required resource. For example, you can receive this error if a storage account can't be found at the path specified. Double check path or name specifications for accuracy and spelling. For more information, see [Resolve errors for Resource Not Found](/azure/azure-resource-manager/troubleshooting/error-not-found).

#### Container registry authorization error

This error occurs when an image belonging to a private or otherwise inaccessible container registry is supplied for deployment. Azure Machine Learning APIs can't accept private registry credentials.

To mitigate this error, either ensure that the container registry isn't private, or take the following steps:

1. Grant your private registry's **acrPull** role to the system identity of your online endpoint.
1. In your environment definition, specify the address of your private image and give the instruction to not modify or build the image.

If this mitigation succeeds, the image doesn't require building, and the final image address is the given image address. At deployment time, your online endpoint's system identity pulls the image from the private registry.

For more diagnostic information, see [How to use workspace diagnostics](how-to-workspace-diagnostic-api.md).

### ERROR: WorkspaceManagedNetworkNotReady

This error occurs if you try to create an online deployment that enables a workspace managed virtual network, but the managed virtual network isn't provisioned yet. Provision the workspace managed virtual network before you create an online deployment.

To manually provision the workspace managed virtual network, follow the instructions at [Manually provision a managed VNet](how-to-managed-network.md#manually-provision-a-managed-vnet). You may then start creating online deployments. For more information, see [Network isolation with managed online endpoint](concept-secure-online-endpoint.md) and [Secure your managed online endpoints with network isolation](how-to-secure-online-endpoint.md).

### ERROR: OperationCanceled

You might get this error when using either managed online endpoint or Kubernetes online endpoint, for the following reasons:

- [Operation was canceled by another operation that has a higher priority](#operation-canceled-by-another-higher-priority-operation)
- [Operation was canceled due to a previous operation waiting for lock confirmation](#operation-canceled-waiting-for-lock-confirmation)

#### Operation canceled by another higher priority operation

Azure operations have a certain priority level and execute from highest to lowest. This error happens when another operation that has a higher priority overrides your operation. Retrying the operation might allow it to perform without cancellation.

#### Operation canceled waiting for lock confirmation

Azure operations have a brief waiting period after being submitted, during which they retrieve a lock to ensure that they don't encounter race conditions. This error happens when the operation you submitted is the same as another operation. The other operation is currently waiting for confirmation that it received the lock before it proceeds.

You might have submitted a similar request too soon after the initial request. Retrying the operation after waiting up to a minute might allow it to perform without cancellation.

### ERROR: SecretsInjectionError

Secret retrieval and injection during online deployment creation uses the identity associated with the online endpoint to retrieve secrets from the workspace connections or key vaults. This error happens for one of the following reasons:

- The endpoint identity doesn't have Azure RBAC permission to read the secrets from the workspace connections or key vaults, even though the deployment definition specified the secrets as references mapped to environment variables. Role assignment might take time for changes to take effect.

- The format of the secret references is invalid, or the specified secrets don't exist in the workspace connections or key vaults.

For more information, see [Secret injection in online endpoints (preview)](concept-secret-injection.md) and [Access secrets from online deployment using secret injection (preview)](how-to-deploy-online-endpoint-with-secret-injection.md).

### ERROR: InternalServerError

This error means there's something wrong with the Azure Machine Learning service that needs to be fixed. Submit a [customer support ticket](https://portal.azure.com/#blade/Microsoft_Azure_Support/HelpAndSupportBlade/newsupportrequest) with all information needed to address the issue.

## Common errors specific to Kubernetes deployments

Identity and authentication errors:
- [ACRSecretError](#error-acrsecreterror)
- [TokenRefreshFailed](#error-tokenrefreshfailed)
- [GetAADTokenFailed](#error-getaadtokenfailed)
- [ACRAuthenticationChallengeFailed](#error-acrauthenticationchallengefailed)
- [ACRTokenExchangeFailed](#error-acrtokenexchangefailed)
- [KubernetesUnaccessible](#error-kubernetesunaccessible)

Crashloopbackoff errors:
- [ImagePullLoopBackOff](#error-imagepullloopbackoff)
- [DeploymentCrashLoopBackOff](#error-deploymentcrashloopbackoff)
- [KubernetesCrashLoopBackOff](#error-kubernetescrashloopbackoff)

Scoring script errors:
- [UserScriptInitFailed](#error-userscriptinitfailed)
- [UserScriptImportError](#error-userscriptimporterror)
- [UserScriptFunctionNotFound](#error-userscriptfunctionnotfound)

Other errors:
- [NamespaceNotFound](#error-namespacenotfound)
- [EndpointAlreadyExists](#error-endpointalreadyexists)
- [ScoringFeUnhealthy](#error-scoringfeunhealthy)
- [ValidateScoringFailed](#error-validatescoringfailed)
- [InvalidDeploymentSpec](#error-invaliddeploymentspec)
- [PodUnschedulable](#error-podunschedulable)
- [PodOutOfMemory](#error-podoutofmemory)
- [InferencingClientCallFailed](#error-inferencingclientcallfailed)

### ERROR: ACRSecretError 

When you create or update Kubernetes online deployments, you might get this error for one of the following reasons:

- Role assignment isn't completed. Wait for a few seconds and try again.

- The Azure Arc-enabled Kubernetes cluster or AKS Azure Machine Learning extension isn't properly installed or configured. Check the Azure Arc-enabled Kubernetes or Azure Machine Learning extension configuration and status.

- The Kubernetes cluster has improper network configuration. Check the proxy, network policy, or certificate.

- Your private AKS cluster doesn't have the proper endpoints. Make sure to set up private endpoints for Container Registry, the storage account, and the workspace in the AKS virtual network.

- Your Azure Machine Learning extension version is v1.1.25 or lower. Make sure your extension version is greater than v1.1.25.

### ERROR: TokenRefreshFailed

This error occurs because the Kubernetes cluster identity isn't set properly, so the extension can't get a principal credential from Azure. Reinstall the [Azure Machine Learning extension](how-to-deploy-kubernetes-extension.md) and try again. 

### ERROR: GetAADTokenFailed

This error occurs because the Kubernetes cluster request Microsoft Entra ID token failed or timed out. Check your network access and then try again.

- Follow instructions at [Use Kubernetes compute](how-to-access-azureml-behind-firewall.md#scenario-use-kubernetes-compute) to check the outbound proxy and make sure the cluster can connect to the workspace. You can find the workspace endpoint URL in the online endpoint Custom Resource Definition (CRD) in the cluster.

- Check whether the workspace allows public access. Regardless of whether the AKS cluster itself is public or private, if a private workspace disables public network access, the Kubernetes cluster can communicate with that workspace only through a private link. For more information, see [What is a secure AKS inferencing environment](how-to-secure-kubernetes-inferencing-environment.md#what-is-a-secure-aks-inferencing-environment).

### ERROR: ACRAuthenticationChallengeFailed

This error occurs because the Kubernetes cluster can't reach the workspace Container Registry service to do an authentication challenge. Check your network, especially Container Registry public network access, then try again. You can follow the troubleshooting steps in [GetAADTokenFailed](#error-getaadtokenfailed) to check the network.

### ERROR: ACRTokenExchangeFailed

This error occurs because the Microsoft Entra ID token isn't yet authorized, so the Kubernetes cluster exchange Container Registry token fails. The role assignment takes some time, so wait a minute and then try again.

This failure might also be due to too many concurrent requests to the Container Registry service. This error should be transient, and you can try again later.

### ERROR: KubernetesUnaccessible

You might get the following error during Kubernetes model deployments:

```
{"code":"BadRequest","statusCode":400,"message":"The request is invalid.","details":[{"code":"KubernetesUnaccessible","message":"Kubernetes error: AuthenticationException. Reason: InvalidCertificate"}],...}
```

To mitigate this error, you can rotate the AKS certificate for the cluster. The new certificate should be updated after 5 hours, so you can wait for 5 hours and redeploy it. For more information, see [Certificate rotation in Azure Kubernetes Service (AKS)](/azure/aks/certificate-rotation).

### ERROR: ImagePullLoopBackOff

You might get this error when you create or update Kubernetes online deployments because you can't download the images from the container registry, resulting in the images pull failure. Check the cluster network policy and the workspace container registry to see if the cluster can pull images from the container registry.

### ERROR: DeploymentCrashLoopBackOff 

You might get this error when you create or update Kubernetes online deployments because the user container crashed when initializing. There are two possible reasons for this error:
- The user script *score.py* has a syntax error or import error that raises exceptions in initializing.
- The deployment pod needs more memory than its limit.

To mitigate this error, first check the deployment logs for any exceptions in user scripts. If the error persists, try to extend the resource/instance type memory limit.

### ERROR: KubernetesCrashLoopBackOff

You might get this error when you create or update Kubernetes online endpoints or deployments for one of the following reasons:

- One or more pods is stuck in CrashLoopBackoff status. Check if the deployment log exists and there are error messages in the log.
- There's an error in *score.py* and the container crashed when initializing your score code. Follow instructions under [ERROR: ResourceNotReady](#error-resourcenotready).
- Your scoring process needs more memory than your deployment configuration limit. You can try to update the deployment with a larger memory limit.

### ERROR: NamespaceNotFound

You might get this error when you create or update Kubernetes online endpoints because the namespace your Kubernetes compute used is unavailable in your cluster. Check the Kubernetes compute in your workspace portal and check the namespace in your Kubernetes cluster. If the namespace isn't available, detach the legacy compute and reattach to create a new one, specifying a namespace that already exists in your cluster.

### ERROR: UserScriptInitFailed 

You might get this error when you create or update Kubernetes online deployments because the `init` function in your uploaded *score.py* file raised an exception. Check the deployment logs to see the exception message in detail, and fix the exception.

### ERROR: UserScriptImportError

You might get this error when you create or update Kubernetes online deployments because the *score.py* file that you uploaded imports unavailable packages. Check the deployment logs to see the exception message in detail, and fix the exception.

### ERROR: UserScriptFunctionNotFound 

You might get this error when you create or update Kubernetes online deployments because the *score.py* file that you uploaded doesn't have a function named `init()` or `run()`. Check your code and add the function.

### ERROR: EndpointNotFound

You might get this error when you create or update Kubernetes online deployments because the system can't find the endpoint resource for the deployment in the cluster. Create the deployment in an existing endpoint or create the endpoint first in your cluster.

### ERROR: EndpointAlreadyExists

You might get this error when you create a Kubernetes online endpoint because the endpoint already exists in your cluster. The endpoint name should be unique per workspace and per cluster, so create an endpoint with another name.

### ERROR: ScoringFeUnhealthy

You might get this error when you create or update a Kubernetes online endpoint or deployment because the [azureml-fe](how-to-kubernetes-inference-routing-azureml-fe.md) system service that runs in the cluster isn't found or is unhealthy. To mitigate this issue, reinstall or update the Azure Machine Learning extension in your cluster.

### ERROR: ValidateScoringFailed

You might get this error when you create or update Kubernetes online deployments because the scoring request URL validation failed when processing the model. Check the endpoint URL and then try to redeploy.

### ERROR: InvalidDeploymentSpec

You might get this error when you create or update Kubernetes online deployments because the deployment spec is invalid. Check the error message to make sure the `instance count` is valid. If you enabled autoscaling, make sure the `minimum instance count` and `maximum instance count` are both valid.

### ERROR: PodUnschedulable

You might get this error when you create or update Kubernetes online endpoints or deployments for one of the following reasons:

- The system can't schedule the pod to nodes due to insufficient resources in your cluster.
- No node matches the node affinity selector.

To mitigate this error, follow these steps:

1. Check the `node selector` definition of the `instance_type` you used, and the `node label` configuration of your cluster nodes. 
1. Check the `instance_type` and the node SKU size for the AKS cluster or the node resource for the Azure Arc-enabled Kubernetes cluster.
1. If the cluster is under-resourced, reduce the instance type resource requirement or use another instance type with smaller resource requirements. 
1. If the cluster has no more resources to meet the requirement of the deployment, delete some deployments to release resources.

### ERROR: PodOutOfMemory 

You might get this error when you create or update an online deployment because the memory limit you gave for deployment is insufficient. To mitigate this error, you can set the memory limit to a larger value or use a bigger instance type.

### ERROR: InferencingClientCallFailed 

You might get this error when you create or update Kubernetes online endpoints or deployments because the k8s-extension of the Kubernetes cluster isn't connectable. In this case, detach and then reattach your compute. 

To troubleshoot errors by reattaching, make sure to reattach with the same configuration as the detached compute, such as compute name and namespace, to avoid other errors. If it still isn't working, ask an administrator who can access the cluster to use `kubectl get po -n azureml` to check whether the relay server pods are running.

## Model consumption issues

Common model consumption errors resulting from the endpoint `invoke` operation status include [bandwidth limit issues](#bandwidth-limit-issues), [CORS policy](#blocked-by-cors-policy), and various [HTTP status codes](#http-status-codes).

### Bandwidth limit issues

Managed online endpoints have bandwidth limits for each endpoint. You can find the limit configuration in [limits for online endpoints](how-to-manage-quotas.md#azure-machine-learning-online-endpoints-and-batch-endpoints). If your bandwidth usage exceeds the limit, your request is delayed.

To monitor the bandwidth delay, use the metric **Network bytes** to understand the current bandwidth usage. For more information, see [Monitor managed online endpoints](how-to-monitor-online-endpoints.md).

Two response trailers are returned if the bandwidth limit is enforced:
- `ms-azureml-bandwidth-request-delay-ms` is the delay time in milliseconds it took for the request stream transfer.
- `ms-azureml-bandwidth-response-delay-ms`is the delay time in milliseconds it took for the response stream transfer.

### Blocked by CORS policy

V2 online endpoints don't support [Cross-Origin Resource Sharing (CORS)](https://developer.mozilla.org/docs/Web/HTTP/CORS) natively. If your web application tries to invoke the endpoint without properly handling the CORS preflight requests, you can get the following error message:

```output
Access to fetch at 'https://{your-endpoint-name}.{your-region}.inference.ml.azure.com/score' from origin http://{your-url} has been blocked by CORS policy: Response to preflight request doesn't pass access control check. No 'Access-control-allow-origin' header is present on the request resource. If an opaque response serves your needs, set the request's mode to 'no-cors' to fetch the resource with the CORS disabled.
```
You can use Azure Functions, Azure Application Gateway, or another service as an interim layer to handle CORS preflight requests.

### HTTP status codes

When you access online endpoints with REST requests, the returned status codes adhere to the standards for [HTTP status codes](https://aka.ms/http-status-codes). The following sections present details about how endpoint invocation and prediction errors map to HTTP status codes.

#### Common error codes for managed online endpoints

The following table contains common error codes when REST requests consume managed online endpoints:

| Status code | Reason    | Description|
| ----------- | ------------------------- | ---- |
| 200         | OK                        | Your model executed successfully within your latency bounds. |
| 401         | Unauthorized              | You don't have permission to do the requested action, such as score, or your token is expired or in the wrong format. For more information, see [Authentication for managed online endpoints](concept-endpoints-online-auth.md) and [Authenticate clients for online endpoints](how-to-authenticate-online-endpoint.md).|
| 404         | Not found                 | The endpoint doesn't have any valid deployment with positive weight.|
| 408         | Request timeout           | The model execution took longer than the timeout supplied in `request_timeout_ms` under `request_settings` of your model deployment config.|
| 424         | Model error               | If your model container returns a non-200 response, Azure returns a 424. Check the `Model Status Code` dimension under the `Requests Per Minute` metric on your endpoint's [Azure Monitor Metric Explorer](/azure/azure-monitor/essentials/metrics-getting-started). Or check response headers `ms-azureml-model-error-statuscode` and `ms-azureml-model-error-reason` for more information. If 424 comes with liveness or readiness probe failing, consider adjusting [ProbeSettings](reference-yaml-deployment-managed-online.md#probesettings) to allow more time to probe container liveness or readiness. |
| 429         | Too many pending requests | Your model is currently getting more requests than it can handle. To guarantee smooth operation, Azure Machine Learning permits a maximum of `2 * max_concurrent_requests_per_instance * instance_count requests` to process in parallel at any given time. Requests that exceed this maximum are rejected.<br><br>You can review your model deployment configuration under the `request_settings` and `scale_settings` sections to verify and adjust these settings. Also ensure that the environment variable `WORKER_COUNT` is correctly passed, as outlined in [RequestSettings](reference-yaml-deployment-managed-online.md#requestsettings).<br><br>If you get this error when you're using autoscaling, your model is getting requests faster than the system can scale up. Consider resending requests with an [exponential backoff](https://en.wikipedia.org/wiki/Exponential_backoff) to give the system time to adjust. You could also increase the number of instances by using code to [calculate instance count](#how-to-calculate-instance-count). Combine these steps with setting autoscaling to help ensure that your model is ready to handle the influx of requests.|
| 429         | Rate-limited             | The number of requests per second reached the managed online endpoints [limits](how-to-manage-quotas.md#azure-machine-learning-online-endpoints-and-batch-endpoints).|
| 500         | Internal server error     | Azure Machine Learning-provisioned infrastructure is failing.|

#### Common error codes for Kubernetes online endpoints

The following table contains common error codes when REST requests consume Kubernetes online endpoints:

| Status code | Error      | Description |
| ----------- | ----------------------------------------------------------------------------- | ---------- |
| 409         | Conflict error     | When an operation is already in progress, any new operation on that same online endpoint responds with a 409 conflict error. For example, if a create or update online endpoint operation is in progress, triggering a new delete operation throws an error.     |
| 502         | Exception or crash in the `run()` method of the *score.py* file | When there's an error in *score.py*, for example an imported package that doesn't exist in the conda environment, a syntax error, or a failure in the `init()` method, see [ERROR: ResourceNotReady](#error-resourcenotready) to debug the file.|
| 503         | Large spikes in requests per second | The autoscaler is designed to handle gradual changes in load. If you receive large spikes in requests per second, clients might receive HTTP status code 503. Even though the autoscaler reacts quickly, it takes AKS a significant amount of time to create more containers. See [How to prevent 503 status code errors](#how-to-prevent-503-status-code-errors).|
| 504         | Request times out | A 504 status code indicates that the request timed out. The default timeout setting is 5 seconds. You can increase the timeout or try to speed up the endpoint by modifying *score.py* to remove unnecessary calls. If these actions don't correct the problem, the code might be in a nonresponsive state or an infinite loop. Follow [ERROR: ResourceNotReady](#error-resourcenotready) to debug the *score.py* file.  |
| 500         | Internal server error  | Azure Machine Learning-provisioned infrastructure is failing.|

#### How to prevent 503 status code errors

Kubernetes online deployments support autoscaling, which allows replicas to be added to support extra load. For more information, see [Azure Machine Learning inference router](how-to-kubernetes-inference-routing-azureml-fe.md). The decision to scale up or down is based on utilization of the current container replicas.

Two actions can help prevent 503 status code errors: Changing the utilization level for creating new replicas, or changing the minimum number of replicas. You can use these approaches individually or in combination.

- Change the utilization target at which autoscaling creates new replicas by setting the `autoscale_target_utilization` to a lower value. This change doesn't cause replicas to be created faster, but at a lower utilization threshold. For example, changing the value to 30% causes replicas to be created when 30% utilization occurs instead of waiting until the service is 70% utilized.

- Change the minimum number of replicas to provide a larger pool that can handle the incoming spikes.

#### How to calculate instance count

To increase the number of instances, you can calculate the required replicas as follows:

  ```python
  from math import ceil
  # target requests per second
  target_rps = 20
  # time to process the request (in seconds, choose appropriate percentile)
  request_process_time = 10
  # Maximum concurrent requests per instance
  max_concurrent_requests_per_instance = 1
  # The target CPU usage of the model container. 70% in this example
  target_utilization = .7
  
  concurrent_requests = target_rps * request_process_time / target_utilization
  
  # Number of instance count
  instance_count = ceil(concurrent_requests / max_concurrent_requests_per_instance)
  ```

  > [!NOTE]
  > If you receive request spikes larger than the new minimum replicas can handle, you might receive 503 again. For example, as traffic to your endpoint increases, you might need to increase the minimum replicas.

If the Kubernetes online endpoint is already using the current max replicas and you still get 503 status codes, increase the `autoscale_max_replicas` value to increase the maximum number of replicas.

## Network isolation issues

This section provides information about common network isolation issues.

[!INCLUDE [network isolation issues](includes/machine-learning-online-endpoint-troubleshooting.md)]

## Inference server issues

This section provides basic troubleshooting tips for the [Azure Machine Learning inference HTTP server](how-to-inference-server-http.md).

[!INCLUDE [inference server TSGs](includes/machine-learning-inference-server-troubleshooting.md)]

## Other common issues

Other common online endpoint issues are related to conda installation and autoscaling.

### Conda installation issues

Issues with MLflow deployment generally stem from issues with the installation of the user environment specified in the *conda.yml* file. 

To debug conda installation problems, try the following steps:

1. Check the conda installation logs. If the container crashed or took too long to start up, the conda environment update probably failed to resolve correctly.
1. Install the mlflow conda file locally with the command `conda env create -n userenv -f <CONDA_ENV_FILENAME>`. 
1. If there are errors locally, try resolving the conda environment and creating a functional one before redeploying. 
1. If the container crashes even if it resolves locally, the SKU size used for deployment might be too small. 
   - Conda package installation occurs at runtime, so if the SKU size is too small to accommodate all the packages in the *conda.yml* environment file, the container might crash. 
   - A Standard_F4s_v2 VM is a good starting SKU size, but you might need larger VMs depending on the dependencies the conda file specifies.
   - For Kubernetes online endpoints, the Kubernetes cluster must have a minimum of four vCPU cores and 8 GB of memory.

### Autoscaling issues

If you have trouble with autoscaling, see [Troubleshoot Azure Monitor autoscale](/azure/azure-monitor/autoscale/autoscale-troubleshoot).

For Kubernetes online endpoints, the Azure Machine Learning inference router is a front-end component that handles autoscaling for all model deployments on the Kubernetes cluster. For more information, see [Autoscale Kubernetes inference routing](how-to-kubernetes-inference-routing-azureml-fe.md#autoscaling).

## Related content

- [Deploy and score a machine learning model by using an online endpoint](how-to-deploy-online-endpoints.md)
- [Safe rollout for online endpoints](how-to-safely-rollout-online-endpoints.md)
- [Online endpoint YAML reference](reference-yaml-endpoint-online.md)
- [Troubleshoot Kubernetes compute](how-to-troubleshoot-kubernetes-compute.md)
