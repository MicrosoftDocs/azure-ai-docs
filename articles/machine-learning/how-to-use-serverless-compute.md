---
title: Model Training on Serverless Compute
titleSuffix: Azure Machine Learning
description: Use serverless compute to run training jobs on Azure Machine Learning. Serverless compute is a fully managed on-demand compute. 
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: core
ms.custom:
  - build-2023
  - ignite-2023
  - dev-focus
ms.topic: how-to
ai-usage: ai-assisted
ms.author: scottpolly
author: s-polly
ms.reviewer: bijuv
ms.date: 10/24/2025
#customer intent: As a machine learning professional, I want to learn how to use serverless compute to run training jobs on Azure Machine Learning. 
---

# Model training on serverless compute

[!INCLUDE [dev v2](includes/machine-learning-dev-v2.md)]

You don't need to [create and manage compute](./how-to-create-attach-compute-cluster.md) to train your model in a scalable way. You can instead submit your job to a compute target type called _serverless compute_. Serverless compute is the easiest way to run training jobs on Azure Machine Learning. Serverless compute is a fully managed, on-demand compute. Azure Machine Learning creates, scales, and manages the compute for you. When you use serverless compute to train models, you can focus on building machine learning models and not have to learn about compute infrastructure or setting it up.

You can specify the resources the job needs. Azure Machine Learning manages the compute infrastructure and provides managed network isolation, reducing the burden on you.

Enterprises can also reduce costs by specifying optimal resources for each job. IT administrators can still apply control by specifying core quota at subscription and workspace levels and applying Azure policies.

You can use serverless compute to fine-tune models in the model catalog. You can use it to run all types of jobs by using Azure Machine Learning studio, the Python SDK, and Azure CLI. You can also use serverless compute to build environment images and for responsible AI dashboard scenarios. Serverless jobs consume the same quota as Azure Machine Learning compute quota. You can choose standard (dedicated) tier or spot (low-priority) VMs. Managed identity and user identity are supported for serverless jobs. The billing model is the same as the model for Azure Machine Learning compute.

## Prerequisites

- An Azure subscription. If you don't have one, create a [free account](https://azure.microsoft.com/free/).
- An [Azure Machine Learning workspace](how-to-manage-workspace.md).
- The Azure CLI with the `ml` extension, or the Azure Machine Learning Python SDK v2:

  # [Python SDK](#tab/python)

  ```bash
  pip install azure-ai-ml azure-identity
  ```

  # [Azure CLI](#tab/cli)

  ```azurecli
  az extension add --name ml
  ```

  ---

- **Role requirements**: You need at least **Contributor** or **Azure ML Data Scientist** role on the workspace to submit jobs.

## Submit your first serverless job

The following example shows a minimal command job that runs on serverless compute. When you omit the `compute` parameter, the job automatically uses serverless compute.

# [Python SDK](#tab/python)

```python
from azure.ai.ml import command, MLClient
from azure.identity import DefaultAzureCredential

# Initialize the ML client
credential = DefaultAzureCredential()
ml_client = MLClient(
    credential=credential,
    subscription_id="<Azure-subscription-ID>",
    resource_group_name="<Azure-resource-group>",
    workspace_name="<Azure-Machine-Learning-workspace>",
)

# Create a simple command job - omitting 'compute' uses serverless
job = command(
    command="echo 'hello world'",
    environment="azureml://registries/azureml/environments/sklearn-1.5/labels/latest",
)

# Submit the job
returned_job = ml_client.create_or_update(job)
print(f"Job submitted: {returned_job.name}")
```

# [Azure CLI](#tab/cli)

Create a file named `hello-serverless.yaml`:

```yaml
$schema: https://azuremlschemas.azureedge.net/latest/commandJob.schema.json
command: echo "hello world"
environment:
  image: library/python:latest
```

Submit the job:

```azurecli
az ml job create --file hello-serverless.yaml --resource-group <resource-group> --workspace-name <workspace>
```

---

**Expected output:** The job is created and returns a job object with status `NotStarted` or `Starting`. Monitor progress in Azure ML studio or by calling `ml_client.jobs.get(returned_job.name)`.

**Reference:** [command function](/python/api/azure-ai-ml/azure.ai.ml#azure-ai-ml-command) | [MLClient](/python/api/azure-ai-ml/azure.ai.ml.mlclient)

## Advantages of serverless compute

* Azure Machine Learning manages creating, setting up, scaling, deleting, and patching compute infrastructure to reduce management overhead.
* You don't need to learn about compute, various compute types, or related properties.
* You don't need to repeatedly create clusters for each VM size that you need, using the same settings, and replicating for each workspace.
* You can optimize costs by specifying the exact resources each job needs at runtime for instance type (VM size) and instance count. You can also monitor the utilization metrics of the job to optimize the resources a job needs.
* Fewer steps are required to run a job.
* To further simplify job submission, you can skip the resources altogether. Azure Machine Learning defaults the instance count and chooses an instance type by taking into account factors like quota, cost, performance, and disk size.
* In some scenarios, wait times before jobs start running are reduced.
* User identity and workspace user-assigned managed identity are supported for job submission.
* With managed network isolation, you can streamline and automate your network isolation configuration. Customer virtual networks are also supported.
* Administrative control is available via quota and Azure policies.

## How to use serverless compute

* When you create your own compute cluster, you use its name in the command job. For example, `compute="cpu-cluster"`. With serverless, you can skip the creation of a compute cluster, and omit the `compute` parameter to instead use serverless compute. When `compute` isn't specified for a job, the job runs on serverless compute. Omit the compute name in your Azure CLI or Python SDK jobs to use serverless compute in the following job types, and optionally provide resources the job needs for instance count and instance type:

  * Command jobs, including interactive jobs and distributed training
  * AutoML jobs
  * Sweep jobs
  * Parallel jobs

* For pipeline jobs via the Azure CLI, use `default_compute: azureml:serverless` for pipeline-level default compute. For pipeline jobs via the Python SDK, use `default_compute="serverless"`. See [Pipeline job](#pipeline-job) for an example.

* When you [submit a training job in studio](how-to-train-with-ui.md), select **Serverless** as the compute type.
* When using [Azure Machine Learning designer](concept-designer.md), select **Serverless** as the default compute.


## Performance considerations

Serverless compute can increase the speed of your training in the following ways:

**Avoid insufficient quota failures.** When you create your own compute cluster, you're responsible for determining the VM size and node count. When your job runs, if you don't have sufficient quota for the cluster, the job fails. Serverless compute uses information about your quota to select an appropriate VM size by default.

**Scale-down optimization.** When a compute cluster is scaling down, a new job has to wait for the cluster to scale down and then scale up before the job can run. With serverless compute, you don't have to wait for scale down. Your job can start running on another cluster/node (assuming you have quota).

**Cluster-busy optimization.** When a job is running on a compute cluster and another job is submitted, your job is queued behind the currently running job. With serverless compute, your job can start running on another node/cluster (assuming you have quota).

## Quota

When you submit a job, you still need sufficient Azure Machine Learning compute quota to proceed (both workspace-level and subscription-level quota). The default VM size for serverless jobs is selected based on this quota. If you specify your own VM size/family:

* If you have some quota for your VM size/family but not sufficient quota for the number of instances, you see an error. The error recommends that you decrease the number of instances to a valid number based on your quota limit, request a quota increase for the VM family, or change the VM size.
* If you don't have quota for your specified VM size, you see an error. The error recommends that you select a different VM size for which you do have quota or request quota for the VM family.
* If you do have sufficient quota for a VM family to run the serverless job but other jobs are using the quota, you get a message stating that your job must wait in a queue until quota is available.

When you [view your usage and quotas in the Azure portal](how-to-manage-quotas.md#view-your-usage-and-quotas-in-the-azure-portal), you see the name **Serverless** for all quota consumed by serverless jobs.

## Identity support and credential passthrough

Serverless compute supports two identity options for accessing storage and other resources:

- **User credential passthrough**: Uses your Microsoft Entra ID token. Best for interactive development and testing.
- **User-assigned managed identity**: Uses the workspace's managed identity. Best for production scenarios and automation.

* **User credential passthrough**: Serverless compute fully supports user credential passthrough. The user token of the user submitting the job is used for storage access. These credentials are from Microsoft Entra ID.

  Serverless compute doesn't support system-assigned identity.

    # [Python SDK](#tab/python)

    ```python
    from azure.ai.ml import command
    from azure.ai.ml import MLClient     # Handle to the workspace.
    from azure.identity import DefaultAzureCredential     # Authentication package.
    from azure.ai.ml.entities import UserIdentityConfiguration 

    credential = DefaultAzureCredential()
    # Get a handle to the workspace. You can find the info on the workspace tab on ml.azure.com.
    ml_client = MLClient(
        credential=credential,
        subscription_id="<Azure subscription ID>", 
        resource_group_name="<Azure resource group>",
        workspace_name="<Azure Machine Learning workspace>",
    )
    job = command(
        command="echo 'hello world'",
        environment="azureml://registries/azureml/environments/sklearn-1.5/labels/latest",
        identity=UserIdentityConfiguration(),
    )
    # Submit the command job.
    ml_client.create_or_update(job)
    ```

    # [Azure CLI](#tab/cli)

    Create a file named hello.yaml that contains the following:

    ```YAML
    $schema: https://azuremlschemas.azureedge.net/latest/commandJob.schema.json
    command: echo "hello world"
    environment:
      image: library/python:latest
    identity:
      type: user_identity
    ```

    Submit the job by using this command:

    ```azurecli
    az ml job create --file hello.yaml --resource-group my-resource-group --workspace-name my-workspace
    ```

    The rest of the Azure CLI examples show variations of the hello.yaml file. Run each of them in the same way.

    ---

    **Reference:** [UserIdentityConfiguration](/python/api/azure-ai-ml/azure.ai.ml.entities.useridentityconfiguration) | [command function](/python/api/azure-ai-ml/azure.ai.ml#azure-ai-ml-command)

* **User-assigned managed identity**: When you have a workspace configured with [user-assigned managed identity](how-to-identity-based-service-authentication.md#workspace), you can use that identity with the serverless job for storage access. For information about accessing secrets, see [Use authentication credential secrets in Azure Machine Learning jobs](how-to-use-secrets-in-runs.md).  

1. Verify your workspace identity configuration.
    
    # [Python SDK](#tab/python)
    
    ```python
    from azure.ai.ml import MLClient
    from azure.identity import DefaultAzureCredential
    
    subscription_id = "<your-subscription-id>"
    resource_group = "<your-resource-group>"
    workspace = "<your-workspace-name>"
    
    ml_client = MLClient(
        DefaultAzureCredential(),
        subscription_id,
        resource_group,
        workspace
    )
    
    # Get workspace details.
    ws = ml_client.workspaces.get(name=workspace)
    print(ws)
    
    ```
    
    # [Azure CLI](#tab/cli)
    
    ```azurecli
    az ml workspace show --name <workspace-sname>  --resource-group <resource-group-name>
    ```    
    
    ---

    Look for the user-assigned identity in the output. If it's missing, create a new workspace with a user-assigned managed identity by following the instructions in [Set up authentication between Azure Machine Learning and other services](how-to-identity-based-service-authentication.md).

1. Use your user-assigned managed identity in your job.

    # [Python SDK](#tab/python)
    
    ```python
    from azure.ai.ml import command
    from azure.ai.ml import MLClient     # Handle to the workspace.
    from azure.identity import DefaultAzureCredential    # Authentication package.
    from azure.ai.ml.entities import ManagedIdentityConfiguration
    
    credential = DefaultAzureCredential()
    # Get a handle to the workspace. You can find the info on the workspace tab on ml.azure.com.
    ml_client = MLClient(
        credential=credential,
        subscription_id="<Azure-subscription-ID>", 
        resource_group_name="<Azure-resource-group>",
        workspace_name="<Azure-Machine-Learning-workspace>",
    )
    job = command(
        command="echo 'hello world'",
        environment="azureml://registries/azureml/environments/sklearn-1.5/labels/latest",
        identity= ManagedIdentityConfiguration(client_id="<workspace-UAMI-client-ID>"),
    )
    # Submit the command job.
    ml_client.create_or_update(job)
    ```
    
    # [Azure CLI](#tab/cli)
    
    ```YAML
    $schema: https://azuremlschemas.azureedge.net/latest/commandJob.schema.json
    command: echo "hello world"
    environment:
      image: library/python:latest
    identity:
      type: managed
    ```
    
    ---

**Reference:** [ManagedIdentityConfiguration](/python/api/azure-ai-ml/azure.ai.ml.entities.managedidentityconfiguration)

## Configure properties for command jobs

If no compute target is specified for command, sweep, and AutoML jobs, the compute defaults to serverless compute.
Here's an example:

# [Python SDK](#tab/python)

```python
from azure.ai.ml import command 
from azure.ai.ml import MLClient # Handle to the workspace.
from azure.identity import DefaultAzureCredential # Authentication package.

credential = DefaultAzureCredential()
# Get a handle to the workspace. You can find the info on the workspace tab on ml.azure.com.
ml_client = MLClient(
    credential=credential,
    subscription_id="<Azure-subscription-ID>", 
    resource_group_name="<Azure-resource-group>",
    workspace_name="<Azure-Machine-Learning-workspace>",
)
job = command(
    command="echo 'hello world'",
    environment="azureml://registries/azureml/environments/sklearn-1.5/labels/latest",
)
# Submit the command job.
ml_client.create_or_update(job)
```

# [Azure CLI](#tab/cli)

```YAML
$schema: https://azuremlschemas.azureedge.net/latest/commandJob.schema.json
command: echo "hello world"
environment:
  image: library/python:latest
```

---

The compute defaults to serverless compute with:

* A single node, for this job. The default number of nodes is based on the type of job. See following sections for other job types.
* A CPU virtual machine. The VM is determined based on quota, performance, cost, and disk size.
* Dedicated virtual machines.
* Workspace location.

You can override these defaults. If you want to specify the VM type or number of nodes for serverless compute, add `resources` to your job:

* Use `instance_type` to choose a specific VM. Use this parameter if you want a specific CPU or GPU VM size
* Use `instance_count` to specify the number of nodes.

    # [Python SDK](#tab/python)
    ```python
    from azure.ai.ml import command 
    from azure.ai.ml import MLClient # Handle to the workspace.
    from azure.identity import DefaultAzureCredential # Authentication package.
    from azure.ai.ml.entities import JobResourceConfiguration 

    credential = DefaultAzureCredential()
    # Get a handle to the workspace. You can find the info on the workspace tab on ml.azure.com.
    ml_client = MLClient(
        credential=credential,
        subscription_id="<Azure-subscription-ID>", 
        resource_group_name="<Azure-resource-group>",
        workspace_name="<Azure-Machine-Learning-workspace>",
    )
    job = command(
        command="echo 'hello world'",
        environment="azureml://registries/azureml/environments/sklearn-1.5/labels/latest",
        resources = JobResourceConfiguration(instance_type="Standard_NC24", instance_count=4)
    )
    # Submit the command job.
    ml_client.create_or_update(job)
    ```

    # [Azure CLI](#tab/cli)

    ```YAML
    $schema: https://azuremlschemas.azureedge.net/latest/commandJob.schema.json
    command: echo "hello world"
    environment:
      image: library/python:latest
    resources:
      instance_count: 4
      instance_type: Standard_NC24 
    ```

    ---

    **Reference:** [JobResourceConfiguration](/python/api/azure-ai-ml/azure.ai.ml.entities.jobresourceconfiguration)

* To change the job tier, use `queue_settings` to choose between dedicated VMs (`job_tier: Standard`) and low priority VMs (`job_tier: Spot`).

    # [Python SDK](#tab/python)

    ```python
    from azure.ai.ml import command
    from azure.ai.ml import MLClient    # Handle to the workspace.
    from azure.identity import DefaultAzureCredential    # Authentication package.
    credential = DefaultAzureCredential()
    # Get a handle to the workspace. You can find the info on the workspace tab on ml.azure.com.
    ml_client = MLClient(
        credential=credential,
        subscription_id="<Azure-subscription-ID>", 
        resource_group_name="<Azure-resource-group>",
        workspace_name="<Azure-Machine-Learning-workspace>",
    )
    job = command(
        command="echo 'hello world'",
        environment="azureml://registries/azureml/environments/sklearn-1.5/labels/latest",
        queue_settings={
          "job_tier": "Spot"  
        }
    )
    # Submit the command job.
    ml_client.create_or_update(job)
    ```

    # [Azure CLI](#tab/cli)
    ```YAML
    $schema: https://azuremlschemas.azureedge.net/latest/commandJob.schema.json
    component: ./train.yml 
    queue_settings:
       job_tier: Standard # Possible values are Standard (dedicated) and Spot (low priority). The default is Standard.
    ```
    
## Example for all fields with command jobs

Here's an example that shows all fields specified, including the identity the job should use. You don't need to specify virtual network settings because workspace-level managed network isolation is automatically used.

# [Python SDK](#tab/python)

```python
from azure.ai.ml import command
from azure.ai.ml import MLClient      # Handle to the workspace.
from azure.identity import DefaultAzureCredential     # Authentication package.
from azure.ai.ml.entities import JobResourceConfiguration
from azure.ai.ml.entities import UserIdentityConfiguration 

credential = DefaultAzureCredential()
# Get a handle to the workspace. You can find the info on the workspace tab on ml.azure.com.
ml_client = MLClient(
    credential=credential,
    subscription_id="<Azure-subscription-ID>", 
    resource_group_name="<Azure-resource-group>",
    workspace_name="<Azure-Machine-Learning-workspace>",
)
job = command(
    command="echo 'hello world'",
    environment="azureml://registries/azureml/environments/sklearn-1.5/labels/latest",
    identity=UserIdentityConfiguration(),
    queue_settings={
        "job_tier": "Standard"
    }
)
job.resources = JobResourceConfiguration(instance_type="Standard_E4s_v3", instance_count=1)
# Submit the command job.
ml_client.create_or_update(job)
```

# [Azure CLI](#tab/cli)
```YAML
$schema: https://azuremlschemas.azureedge.net/latest/commandJob.schema.json
command: echo "hello world"
environment:
  image: library/python:latest
queue_settings:
   job_tier: Standard # Possible values are Standard and Spot. The default is Standard.
identity:
  type: user_identity # Possible values are Managed and user_identity.
resources:
  instance_count: 1
  instance_type: Standard_E4s_v3 

```

---

**Reference:** [JobResourceConfiguration](/python/api/azure-ai-ml/azure.ai.ml.entities.jobresourceconfiguration) | [UserIdentityConfiguration](/python/api/azure-ai-ml/azure.ai.ml.entities.useridentityconfiguration) | [command function](/python/api/azure-ai-ml/azure.ai.ml#azure-ai-ml-command)

Here are two more examples of using serverless compute for training:
* [First look at Azure Machine Learning](https://github.com/Azure/azureml-examples/blob/main/tutorials/get-started-notebooks/quickstart.ipynb)
* [Train a model](https://github.com/Azure/azureml-examples/blob/main/tutorials/get-started-notebooks/train-model.ipynb)
  
## AutoML job

You don't need to specify compute for AutoML jobs. Resources can optionally be specified. If an instance count isn't specified, it's defaulted based on the `max_concurrent_trials` and `max_nodes` parameters. If you submit an AutoML image classification or NLP task without specifying an instance type, the GPU VM size is automatically selected. You can submit AutoML jobs by using CLIs, the Python SDK, or studio. 

# [Python SDK](#tab/python)

If you want to specify the type or instance count, use the `ResourceConfiguration` class.

[!notebook-python[] (~/azureml-examples-main/sdk/python/jobs/automl-standalone-jobs/automl-classification-task-bankmarketing/automl-classification-task-bankmarketing-serverless.ipynb?name=classification-configuration)]

# [Azure CLI](#tab/cli)

If you want to specify the type or instance count, add a `resources` section.

:::code language="yaml" source="~/azureml-examples-main/cli/jobs/automl-standalone-jobs/cli-automl-classification-task-bankmarketing/cli-automl-classification-task-bankmarketing-serverless.yml":::

---

## Pipeline job 

# [Python SDK](#tab/python)

For a pipeline job, specify `"serverless"` as your default compute type to use serverless compute.

[!notebook-python[] (~/azureml-examples-main/sdk/python/jobs/pipelines/1a_pipeline_with_components_from_yaml/pipeline_with_components_from_yaml_serverless.ipynb?name=build-pipeline)]

# [Azure CLI](#tab/cli)

For a pipeline job, specify `azureml:serverless` as your default compute type to use serverless compute.

:::code language="yaml" source="~/azureml-examples-main/cli/jobs/pipelines-with-components/basics/1b_e2e_registered_components/pipeline-serverless.yml":::

---

You can also set serverless compute as the default compute in Designer.

### Configure serverless pipeline jobs with user-assigned managed identity

When you use serverless compute in pipeline jobs, we recommend that you set user identity at the individual step level that will be run on a compute, rather than at the root pipeline level. (Although the identity setting is supported at both root pipeline and step levels, the step-level setting takes precedence if both are set. However, for pipelines containing pipeline components, identity must be set on individual steps that will be run. Identity set at the root pipeline or pipeline component level won't function. Therefore, we suggest setting identity at the individual step level for the sake of simplicity.)

# [Python SDK](#tab/python)

```python
def my_pipeline():
    train_job = train_component(
        training_data=Input(type="uri_folder", path="./data")
    )
    # Set managed identity for the job
    train_job.identity = {"type": "managed"}
    return {"train_output": train_job.outputs}

pipeline_job = my_pipeline()
# Configure the pipeline to use serverless compute.
pipeline_job.settings.default_compute = "serverless"
```

# [Azure CLI](#tab/cli)
```YAML    
$schema: https://azuremlschemas.azureedge.net/latest/pipelineJob.schema.json
type: pipeline
description: E2E dummy train-score-eval pipeline with registered components
settings:
    default_compute: azureml:serverless
jobs:
 train_job:
   type: command
   component: azureml:my_train@latest
inputs:
   training_data: 
     type: uri_folder 
      path: ./data   
 identity:
   type: managed
```

---
## Related content

View more examples of training with serverless compute:
* [First look at Azure Machine Learning](https://github.com/Azure/azureml-examples/blob/main/tutorials/get-started-notebooks/quickstart.ipynb)
* [Train a model](https://github.com/Azure/azureml-examples/blob/main/tutorials/get-started-notebooks/train-model.ipynb)
