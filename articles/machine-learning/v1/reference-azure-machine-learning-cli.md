---
title: 'Install and set up the CLI (v1)'
description: Learn how to use the Azure CLI extension (v1) for ML to create & manage resources such as your workspace, datastores, datasets, pipelines, models, and deployments.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: core
ms.topic: reference
author: Blackmist
ms.author: larryfr
ms.reviewer: balapv
ms.date: 07/26/2024
ms.custom: UpdateFrequency5, devx-track-azurecli, cliv1
---

# Install & use the CLI (v1)

[!INCLUDE [cli v1](../includes/machine-learning-cli-v1.md)]


[!INCLUDE [cli-version-info](../includes/machine-learning-cli-v1-deprecation.md)]

The Azure Machine Learning CLI is an extension to the [Azure CLI](/cli/azure/), a cross-platform command-line interface for the Azure platform. This extension provides commands for working with Azure Machine Learning. It allows you to automate your machine learning activities. The following list provides some example actions that you can do with the CLI extension:

+ Run experiments to create machine learning models

+ Register machine learning models for customer usage

+ Package, deploy, and track the lifecycle of your machine learning models

The CLI isn't a replacement for the Azure Machine Learning SDK. It's a complementary tool that is optimized to handle highly parameterized tasks which suit themselves well to automation.

## Prerequisites

* To use the CLI, you must have an Azure subscription. If you don't have an Azure subscription, create a free account before you begin. Try the [free or paid version of Azure Machine Learning](https://azure.microsoft.com/free/) today.

* To use the CLI commands in this document from your **local environment**, you need the [Azure CLI](/cli/azure/install-azure-cli).

    If you use the [Azure Cloud Shell](https://azure.microsoft.com/features/cloud-shell/), the CLI is accessed through the browser and lives in the cloud.

## Full reference docs

Find the [full reference docs for the azure-cli-ml extension of Azure CLI](/cli/azure/ml(v1)/).

## Connect the CLI to your Azure subscription

> [!IMPORTANT]
> If you are using the Azure Cloud Shell, you can skip this section. The cloud shell automatically authenticates you using the account you log into your Azure subscription.

There are several ways that you can authenticate to your Azure subscription from the CLI. The most basic is to interactively authenticate using a browser. To authenticate interactively, open a command line or terminal and use the following command:

```azurecli-interactive
az login
```

If the CLI can open your default browser, it will do so and load a sign-in page. Otherwise, you need to open a browser and follow the instructions on the command line. The instructions involve browsing to [https://aka.ms/devicelogin](https://aka.ms/devicelogin) and entering an authorization code.

[!INCLUDE [select-subscription](../includes/machine-learning-cli-subscription.md)]

For other methods of authenticating, see [Sign in with Azure CLI](/cli/azure/authenticate-azure-cli).

## Install the extension

To install the CLI (v1) extension:
```azurecli-interactive
az extension add -n azure-cli-ml
```

## Update the extension

To update the Machine Learning CLI extension, use the following command:

```azurecli-interactive
az extension update -n azure-cli-ml
```

## Remove the extension

To remove the CLI extension, use the following command:

```azurecli-interactive
az extension remove -n azure-cli-ml
```

## Resource management

The following commands demonstrate how to use the CLI to manage resources used by Azure Machine Learning.

+ If you don't already have one, create a resource group:

    ```azurecli-interactive
    az group create -n myresourcegroup -l westus2
    ```

+ Create an Azure Machine Learning workspace:

    ```azurecli-interactive
    az ml workspace create -w myworkspace -g myresourcegroup
    ```

    For more information, see [az ml workspace create](/cli/azure/ml/workspace#az-ml-workspace-create).

+ Attach a workspace configuration to a folder to enable CLI contextual awareness.

    ```azurecli-interactive
    az ml folder attach -w myworkspace -g myresourcegroup
    ```

    This command creates a `.azureml` subdirectory that contains example runconfig and conda environment files. It also contains a `config.json` file that is used to communicate with your Azure Machine Learning workspace.

    For more information, see [az ml folder attach](/cli/azure/ml(v1)/folder#az-ml-folder-attach).

+ Attach an Azure blob container as a Datastore.

    ```azurecli-interactive
    az ml datastore attach-blob  -n datastorename -a accountname -c containername
    ```

    For more information, see [az ml datastore attach-blob](/cli/azure/ml/datastore#az-ml-datastore-attach-blob).

+ Upload files to a Datastore.

    ```azurecli-interactive
    az ml datastore upload  -n datastorename -p sourcepath
    ```

    For more information, see [az ml datastore upload](/cli/azure/ml/datastore#az-ml-datastore-upload).

+ Attach an AKS cluster as a Compute Target.

    ```azurecli-interactive
    az ml computetarget attach aks -n myaks -i myaksresourceid -g myresourcegroup -w myworkspace
    ```

    For more information, see [az ml computetarget attach aks](/cli/azure/ml(v1)/computetarget/attach#az-ml-computetarget-attach-aks)

### Compute clusters

+ Create a new managed compute cluster.

    ```azurecli-interactive
    az ml computetarget create amlcompute -n cpu --min-nodes 1 --max-nodes 1 -s STANDARD_D3_V2
    ```



+ Create a new managed compute cluster with managed identity

  + User-assigned managed identity

    ```azurecli
    az ml computetarget create amlcompute --name cpu-cluster --vm-size Standard_NC6 --max-nodes 5 --assign-identity '/subscriptions/<subscription_id>/resourcegroups/<resource_group>/providers/Microsoft.ManagedIdentity/userAssignedIdentities/<user_assigned_identity>'
    ```

  + System-assigned managed identity

    ```azurecli
    az ml computetarget create amlcompute --name cpu-cluster --vm-size Standard_NC6 --max-nodes 5 --assign-identity '[system]'
    ```
+ Add a managed identity to an existing cluster:

    + User-assigned managed identity
        ```azurecli
        az ml computetarget amlcompute identity assign --name cpu-cluster '/subscriptions/<subscription_id>/resourcegroups/<resource_group>/providers/Microsoft.ManagedIdentity/userAssignedIdentities/<user_assigned_identity>'
        ```
    + System-assigned managed identity

        ```azurecli
        az ml computetarget amlcompute identity assign --name cpu-cluster '[system]'
        ```

For more information, see [az ml computetarget create amlcompute](/cli/azure/ml(v1)/computetarget/create#az-ml-computetarget-create-amlcompute).

> [!NOTE]
> Azure Machine Learning compute clusters support only **one system-assigned identity** or **multiple user-assigned identities**, not both concurrently.

<a id="computeinstance"></a>

### Compute instance
Manage compute instances.  In all the examples below, the name of the compute instance is **cpu**

+ Create a new computeinstance.

    ```azurecli-interactive
    az ml computetarget create computeinstance -n cpu -s "STANDARD_D3_V2" -v
    ```

    For more information, see [az ml computetarget create computeinstance](/cli/azure/ml(v1)/computetarget/create#az-ml-computetarget-create-computeinstance).

+ Stop a computeinstance.

    ```azurecli-interactive
    az ml computetarget computeinstance stop -n cpu -v
    ```

    For more information, see [az ml computetarget computeinstance stop](/cli/azure/ml(v1)/computetarget/computeinstance#az-ml-computetarget-computeinstance-stop).

+ Start a computeinstance.

    ```azurecli-interactive
    az ml computetarget computeinstance start -n cpu -v
    ```

    For more information, see [az ml computetarget computeinstance start](/cli/azure/ml(v1)/computetarget/computeinstance#az-ml-computetarget-computeinstance-start).

+ Restart a computeinstance.

    ```azurecli-interactive
    az ml computetarget computeinstance restart -n cpu -v
    ```

    For more information, see [az ml computetarget computeinstance restart](/cli/azure/ml(v1)/computetarget/computeinstance#az-ml-computetarget-computeinstance-restart).

+ Delete a computeinstance.

    ```azurecli-interactive
    az ml computetarget delete -n cpu -v
    ```

    For more information, see [az ml computetarget delete computeinstance](/cli/azure/ml(v1)/computetarget#az-ml-computetarget-delete).


## <a id="experiments"></a>Run experiments

* Start a run of your experiment. When using this command, specify the name of the runconfig file (the text before \*.runconfig if you're looking at your file system) against the -c parameter.

    ```azurecli-interactive
    az ml run submit-script -c sklearn -e testexperiment train.py
    ```

    > [!TIP]
    > The `az ml folder attach` command creates a `.azureml` subdirectory, which contains two example runconfig files. 
    >
    > If you have a Python script that creates a run configuration object programmatically, you can use [RunConfig.save()](/python/api/azureml-core/azureml.core.runconfiguration#save-path-none--name-none--separate-environment-yaml-false-) to save it as a runconfig file.
    >
    > The full runconfig schema can be found in this [JSON file](https://github.com/microsoft/MLOps/blob/b4bdcf8c369d188e83f40be8b748b49821f71cf2/infra-as-code/runconfigschema.json). The schema is self-documenting through the `description` key of each object. Additionally, there are enums for possible values, and a template snippet at the end.

    For more information, see [az ml run submit-script](/cli/azure/ml(v1)/run#az-ml-run-submit-script).

* View a list of experiments:

    ```azurecli-interactive
    az ml experiment list
    ```

    For more information, see [az ml experiment list](/cli/azure/ml(v1)/experiment#az-ml-experiment-list).

### HyperDrive run

You can use HyperDrive with Azure CLI to perform parameter tuning runs. First, create a HyperDrive configuration file in the following format. See [Tune hyperparameters for your model](../how-to-tune-hyperparameters.md) article for details on hyperparameter tuning parameters.

```yml
# hdconfig.yml
sampling: 
    type: random # Supported options: Random, Grid, Bayesian
    parameter_space: # specify a name|expression|values tuple for each parameter.
    - name: --penalty # The name of a script parameter to generate values for.
      expression: choice # supported options: choice, randint, uniform, quniform, loguniform, qloguniform, normal, qnormal, lognormal, qlognormal
      values: [0.5, 1, 1.5] # The list of values, the number of values is dependent on the expression specified.
policy: 
    type: BanditPolicy # Supported options: BanditPolicy, MedianStoppingPolicy, TruncationSelectionPolicy, NoTerminationPolicy
    evaluation_interval: 1 # Policy properties are policy specific. See the above link for policy specific parameter details.
    slack_factor: 0.2
primary_metric_name: Accuracy # The metric used when evaluating the policy
primary_metric_goal: Maximize # Maximize|Minimize
max_total_runs: 8 # The maximum number of runs to generate
max_concurrent_runs: 2 # The number of runs that can run concurrently.
max_duration_minutes: 100 # The maximum length of time to run the experiment before cancelling.
```

Add this file alongside the run configuration files. Then submit a HyperDrive run using:
```azurecli
az ml run submit-hyperdrive -e <experiment> -c <runconfig> --hyperdrive-configuration-name <hdconfig> my_train.py
```

Note the *arguments* section in runconfig and *parameter space* in HyperDrive config. They contain the command-line arguments to be passed to training script. The value in runconfig stays the same for each iteration, while the range in HyperDrive config is iterated over. Don't specify the same argument in both files.

## Dataset management

The following commands demonstrate how to work with datasets in Azure Machine Learning:

+ Register a dataset:

    ```azurecli-interactive
    az ml dataset register -f mydataset.json
    ```

    For information on the format of the JSON file used to define the dataset, use `az ml dataset register --show-template`.

    For more information, see [az ml dataset register](/cli/azure/ml(v1)/dataset#az-ml-dataset-register).

+ List all datasets in a workspace:

    ```azurecli-interactive
    az ml dataset list
    ```

    For more information, see [az ml dataset list](/cli/azure/ml(v1)/dataset#az-ml-dataset-list).

+ Get details of a dataset:

    ```azurecli-interactive
    az ml dataset show -n dataset-name
    ```

    For more information, see [az ml dataset show](/cli/azure/ml(v1)/dataset#az-ml-dataset-show).

+ Unregister a dataset:

    ```azurecli-interactive
    az ml dataset unregister -n dataset-name
    ```

    For more information, see [az ml dataset unregister](/cli/azure/ml(v1)/dataset#az-ml-dataset-archive).

## Environment management

The following commands demonstrate how to create, register, and list Azure Machine Learning [environments](how-to-configure-environment.md) for your workspace:

+ Create scaffolding files for an environment:

    ```azurecli-interactive
    az ml environment scaffold -n myenv -d myenvdirectory
    ```

    For more information, see [az ml environment scaffold](/cli/azure/ml/environment#az-ml-environment-scaffold).

+ Register an environment:

    ```azurecli-interactive
    az ml environment register -d myenvdirectory
    ```

    For more information, see [az ml environment register](/cli/azure/ml/environment#az-ml-environment-register).

+ List registered environments:

    ```azurecli-interactive
    az ml environment list
    ```

    For more information, see [az ml environment list](/cli/azure/ml/environment#az-ml-environment-list).

+ Download a registered environment:

    ```azurecli-interactive
    az ml environment download -n myenv -d downloaddirectory
    ```

    For more information, see [az ml environment download](/cli/azure/ml/environment#az-ml-environment-download).

### Environment configuration schema

If you used the `az ml environment scaffold` command, it generates a template `azureml_environment.json` file that can be modified and used to create custom environment configurations with the CLI. The top level object loosely maps to the [`Environment`](/python/api/azureml-core/azureml.core.environment%28class%29) class in the Python SDK. 

```json
{
    "name": "testenv",
    "version": null,
    "environmentVariables": {
        "EXAMPLE_ENV_VAR": "EXAMPLE_VALUE"
    },
    "python": {
        "userManagedDependencies": false,
        "interpreterPath": "python",
        "condaDependenciesFile": null,
        "baseCondaEnvironment": null
    },
    "docker": {
        "enabled": false,
        "baseImage": "mcr.microsoft.com/azureml/openmpi3.1.2-ubuntu18.04:20210615.v1",
        "baseDockerfile": null,
        "sharedVolumes": true,
        "shmSize": "2g",
        "arguments": [],
        "baseImageRegistry": {
            "address": null,
            "username": null,
            "password": null
        }
    },
    "spark": {
        "repositories": [],
        "packages": [],
        "precachePackages": true
    },
    "databricks": {
        "mavenLibraries": [],
        "pypiLibraries": [],
        "rcranLibraries": [],
        "jarLibraries": [],
        "eggLibraries": []
    },
    "inferencingStackVersion": null
}
```

The following table details each top-level field in the JSON file, its type, and a description. If an object type is linked to a class from the Python SDK, there's a loose 1:1 match between each JSON field and the public variable name in the Python class. In some cases, the field may map to a constructor argument rather than a class variable. For example, the `environmentVariables` field maps to the `environment_variables` variable in the [`Environment`](/python/api/azureml-core/azureml.core.environment%28class%29) class.

| JSON field | Type | Description |
|---|---|---|
| `name` | `string` | Name of the environment. Don't start name with **Microsoft** or **AzureML**. |
| `version` | `string` | Version of the environment. |
| `environmentVariables` | `{string: string}` | A hash-map of environment variable names and values. |
| `python` | [`PythonSection`](/python/api/azureml-core/azureml.core.environment.pythonsection)hat defines the Python environment and interpreter to use on target compute resource. |
| `docker` | [`DockerSection`](/python/api/azureml-core/azureml.core.environment.dockersection) | Defines settings to customize the Docker image built to the environment's specifications. |
| `spark` | [`SparkSection`](/python/api/azureml-core/azureml.core.environment.sparksection) | The section configures Spark settings. It's only used when framework is set to PySpark. |
| `databricks` | [`DatabricksSection`](/python/api/azureml-core/azureml.core.databricks.databrickssection) | Configures Databricks library dependencies. |
| `inferencingStackVersion` | `string` | Specifies the inferencing stack version added to the image. To avoid adding an inferencing stack, leave this field `null`. Valid value: "latest". |

## ML pipeline management

The following commands demonstrate how to work with machine learning pipelines:

+ Create a machine learning pipeline:

    ```azurecli-interactive
    az ml pipeline create -n mypipeline -y mypipeline.yml
    ```

    For more information, see [az ml pipeline create](/cli/azure/ml(v1)/pipeline#az-ml-pipeline-create).

    For more information on the pipeline YAML file, see [Define machine learning pipelines in YAML](reference-pipeline-yaml.md).

+ Run a pipeline:

    ```azurecli-interactive
    az ml run submit-pipeline -n myexperiment -y mypipeline.yml
    ```

    For more information, see [az ml run submit-pipeline](/cli/azure/ml(v1)/run#az-ml-run-submit-pipeline).

    For more information on the pipeline YAML file, see [Define machine learning pipelines in YAML](reference-pipeline-yaml.md).

+ Schedule a pipeline:

    ```azurecli-interactive
    az ml pipeline create-schedule -n myschedule -e myexperiment -i mypipelineid -y myschedule.yml
    ```

    For more information, see [az ml pipeline create-schedule](/cli/azure/ml(v1)/pipeline#az-ml-pipeline-create-schedule).

## Model registration, profiling, deployment

The following commands demonstrate how to register a trained model, and then deploy it as a production service:

+ Register a model with Azure Machine Learning:

    ```azurecli-interactive
    az ml model register -n mymodel -p sklearn_regression_model.pkl
    ```

    For more information, see [az ml model register](/cli/azure/ml/model#az-ml-model-register).

+ **OPTIONAL** Profile your model to get optimal CPU and memory values for deployment.
    ```azurecli-interactive
    az ml model profile -n myprofile -m mymodel:1 --ic inferenceconfig.json -d "{\"data\": [[1,2,3,4,5,6,7,8,9,10],[10,9,8,7,6,5,4,3,2,1]]}" -t myprofileresult.json
    ```

    For more information, see [az ml model profile](/cli/azure/ml/model#az-ml-model-profile).

+ Deploy your model to AKS
    ```azurecli-interactive
    az ml model deploy -n myservice -m mymodel:1 --ic inferenceconfig.json --dc deploymentconfig.json --ct akscomputetarget
    ```
    
    For more information on the inference configuration file schema, see [Inference configuration schema](#inferenceconfig).
    
    For more information on the deployment configuration file schema, see [Deployment configuration schema](#deploymentconfig).

    For more information, see [az ml model deploy](/cli/azure/ml/model#az-ml-model-deploy).

<a id="inferenceconfig"></a>

## Inference configuration schema

The entries in the `inferenceconfig.json` document map to the parameters for the [InferenceConfig](/python/api/azureml-core/azureml.core.model.inferenceconfig) class. The following table describes the mapping between entities in the JSON document and the parameters for the method:

| JSON entity | Method parameter | Description |
| ----- | ----- | ----- |
| `entryScript` | `entry_script` | Path to a local file that contains the code to run for the image. |
| `sourceDirectory` | `source_directory` | Optional. Path to folders that contain all files to create the image, which makes it easy to access any files within this folder or subfolder. You can upload an entire folder from your local machine as dependencies for the Webservice. Note: your entry_script, conda_file, and extra_docker_file_steps paths are relative paths to the source_directory path. |
| `environment` | `environment` | Optional.  Azure Machine Learning [environment](/python/api/azureml-core/azureml.core.environment.environment).|

You can include full specifications of an Azure Machine Learning [environment](/python/api/azureml-core/azureml.core.environment.environment) in the inference configuration file. If this environment doesn't exist in your workspace, Azure Machine Learning will create it. Otherwise, Azure Machine Learning will update the environment if necessary. The following JSON is an example:

```json
{
    "entryScript": "score.py",
    "environment": {
        "docker": {
            "arguments": [],
            "baseDockerfile": null,
            "baseImage": "mcr.microsoft.com/azureml/intelmpi2018.3-ubuntu18.04",
            "enabled": false,
            "sharedVolumes": true,
            "shmSize": null
        },
        "environmentVariables": {
            "EXAMPLE_ENV_VAR": "EXAMPLE_VALUE"
        },
        "name": "my-deploy-env",
        "python": {
            "baseCondaEnvironment": null,
            "condaDependencies": {
                "channels": [
                    "conda-forge"
                ],
                "dependencies": [
                    "python=3.7",
                    {
                        "pip": [
                            "azureml-defaults",
                            "azureml-telemetry",
                            "scikit-learn==0.22.1",
                            "inference-schema[numpy-support]"
                        ]
                    }
                ],
                "name": "project_environment"
            },
            "condaDependenciesFile": null,
            "interpreterPath": "python",
            "userManagedDependencies": false
        },
        "version": "1"
    }
}
```

You can also use an existing Azure Machine Learning [environment](/python/api/azureml-core/azureml.core.environment.environment) in separated CLI parameters and remove the "environment" key from the inference configuration file. Use -e for the environment name, and --ev for the environment version. If you don't specify --ev, the latest version will be used. Here is an example of an inference configuration file:

```json
{
    "entryScript": "score.py",
    "sourceDirectory": null
}
```

The following command demonstrates how to deploy a model using the previous inference configuration file (named myInferenceConfig.json). 

It also uses the latest version of an existing Azure Machine Learning [environment](/python/api/azureml-core/azureml.core.environment.environment) (named AzureML-Minimal).

```azurecli-interactive
az ml model deploy -m mymodel:1 --ic myInferenceConfig.json -e AzureML-Minimal --dc deploymentconfig.json
```

<a id="deploymentconfig"></a>

## Deployment configuration schema

### Local deployment configuration schema

The entries in the `deploymentconfig.json` document map to the parameters for [LocalWebservice.deploy_configuration](/python/api/azureml-core/azureml.core.webservice.local.localwebservicedeploymentconfiguration). The following table describes the mapping between the entities in the JSON document and the parameters for the method:

| JSON entity | Method parameter | Description |
| ----- | ----- | ----- |
| `computeType` | NA | The compute target. For local targets, the value must be `local`. |
| `port` | `port` | The local port on which to expose the service's HTTP endpoint. |

This JSON is an example deployment configuration for use with the CLI:


:::code language="json" source="~/azureml-examples-archive/v1/python-sdk/tutorials/deploy-local/deploymentconfig.json":::

Save this JSON as a file called `deploymentconfig.json`.

### Azure Container Instance deployment configuration schema 

The entries in the `deploymentconfig.json` document map to the parameters for [AciWebservice.deploy_configuration](/python/api/azureml-core/azureml.core.webservice.aci.aciservicedeploymentconfiguration). The following table describes the mapping between the entities in the JSON document and the parameters for the method:

| JSON entity | Method parameter | Description |
| ----- | ----- | ----- |
| `computeType` | NA | The compute target. For ACI, the value must be `ACI`. |
| `containerResourceRequirements` | NA | Container for the CPU and memory entities. |
| &emsp;&emsp;`cpu` | `cpu_cores` | The number of CPU cores to allocate. Defaults, `0.1` |
| &emsp;&emsp;`memoryInGB` | `memory_gb` | The amount of memory (in GB) to allocate for this web service. Default, `0.5` |
| `location` | `location` | The Azure region to deploy this Webservice to. If not specified the Workspace location will be used. More details on available regions can be found here: [ACI Regions](https://azure.microsoft.com/global-infrastructure/services/?regions=all&products=container-instances) |
| `authEnabled` | `auth_enabled` | Whether to enable auth for this Webservice. Defaults to False |
| `sslEnabled` | `ssl_enabled` | Whether to enable SSL for this Webservice. Defaults to False. |
| `appInsightsEnabled` | `enable_app_insights` | Whether to enable AppInsights for this Webservice. Defaults to False |
| `sslCertificate` | `ssl_cert_pem_file` | The cert file needed if SSL is enabled |
| `sslKey` | `ssl_key_pem_file` | The key file needed if SSL is enabled |
| `cname` | `ssl_cname` | The cname for if SSL is enabled |
| `dnsNameLabel` | `dns_name_label` | The dns name label for the scoring endpoint. If not specified a unique dns name label will be generated for the scoring endpoint. |

The following JSON is an example deployment configuration for use with the CLI:

```json
{
    "computeType": "aci",
    "containerResourceRequirements":
    {
        "cpu": 0.5,
        "memoryInGB": 1.0
    },
    "authEnabled": true,
    "sslEnabled": false,
    "appInsightsEnabled": false
}
```

### Azure Kubernetes Service deployment configuration schema

The entries in the `deploymentconfig.json` document map to the parameters for [AksWebservice.deploy_configuration](/python/api/azureml-core/azureml.core.webservice.aks.aksservicedeploymentconfiguration). The following table describes the mapping between the entities in the JSON document and the parameters for the method:

| JSON entity | Method parameter | Description |
| ----- | ----- | ----- |
| `computeType` | NA | The compute target. For AKS, the value must be `aks`. |
| `autoScaler` | NA | Contains configuration elements for autoscale. See the autoscaler table. |
| &emsp;&emsp;`autoscaleEnabled` | `autoscale_enabled` | Whether to enable autoscaling for the web service. If `numReplicas` = `0`, `True`; otherwise, `False`. |
| &emsp;&emsp;`minReplicas` | `autoscale_min_replicas` | The minimum number of containers to use when autoscaling this web service. Default, `1`. |
| &emsp;&emsp;`maxReplicas` | `autoscale_max_replicas` | The maximum number of containers to use when autoscaling this web service. Default, `10`. |
| &emsp;&emsp;`refreshPeriodInSeconds` | `autoscale_refresh_seconds` | How often the autoscaler attempts to scale this web service. Default, `1`. |
| &emsp;&emsp;`targetUtilization` | `autoscale_target_utilization` | The target utilization (in percent out of 100) that the autoscaler should attempt to maintain for this web service. Default, `70`. |
| `dataCollection` | NA | Contains configuration elements for data collection. |
| &emsp;&emsp;`storageEnabled` | `collect_model_data` | Whether to enable model data collection for the web service. Default, `False`. |
| `authEnabled` | `auth_enabled` | Whether or not to enable key authentication for the web service. Both `tokenAuthEnabled` and `authEnabled` cannot be `True`. Default, `True`. |
| `tokenAuthEnabled` | `token_auth_enabled` | Whether or not to enable token authentication for the web service. Both `tokenAuthEnabled` and `authEnabled` cannot be `True`. Default, `False`. |
| `containerResourceRequirements` | NA | Container for the CPU and memory entities. |
| &emsp;&emsp;`cpu` | `cpu_cores` | The number of CPU cores to allocate for this web service. Defaults, `0.1` |
| &emsp;&emsp;`memoryInGB` | `memory_gb` | The amount of memory (in GB) to allocate for this web service. Default, `0.5` |
| `appInsightsEnabled` | `enable_app_insights` | Whether to enable Application Insights logging for the web service. Default, `False`. |
| `scoringTimeoutMs` | `scoring_timeout_ms` | A timeout to enforce for scoring calls to the web service. Default, `60000`. |
| `maxConcurrentRequestsPerContainer` | `replica_max_concurrent_requests` | The maximum concurrent requests per node for this web service. Default, `1`. |
| `maxQueueWaitMs` | `max_request_wait_time` | The maximum time a request will stay in thee queue (in milliseconds) before a 503 error is returned. Default, `500`. |
| `numReplicas` | `num_replicas` | The number of containers to allocate for this web service. No default value. If this parameter is not set, the autoscaler is enabled by default. |
| `keys` | NA | Contains configuration elements for keys. |
| &emsp;&emsp;`primaryKey` | `primary_key` | A primary auth key to use for this Webservice |
| &emsp;&emsp;`secondaryKey` | `secondary_key` | A secondary auth key to use for this Webservice |
| `gpuCores` | `gpu_cores` | The number of GPU cores (per-container replica) to allocate for this Webservice. Default is 1. Only supports whole number values. |
| `livenessProbeRequirements` | NA | Contains configuration elements for liveness probe requirements. |
| &emsp;&emsp;`periodSeconds` | `period_seconds` | How often (in seconds) to perform the liveness probe. Default to 10 seconds. Minimum value is 1. |
| &emsp;&emsp;`initialDelaySeconds` | `initial_delay_seconds` | Number of seconds after the container has started before liveness probes are initiated. Defaults to 310 |
| &emsp;&emsp;`timeoutSeconds` | `timeout_seconds` | Number of seconds after which the liveness probe times out. Defaults to 2 seconds. Minimum value is 1 |
| &emsp;&emsp;`successThreshold` | `success_threshold` | Minimum consecutive successes for the liveness probe to be considered successful after having failed. Defaults to 1. Minimum value is 1. |
| &emsp;&emsp;`failureThreshold` | `failure_threshold` | When a Pod starts and the liveness probe fails, Kubernetes will try failureThreshold times before giving up. Defaults to 3. Minimum value is 1. |
| `namespace` | `namespace` | The Kubernetes namespace that the webservice is deployed into. Up to 63 lowercase alphanumeric ('a'-'z', '0'-'9') and hyphen ('-') characters. The first and last characters can't be hyphens. |

The following JSON is an example deployment configuration for use with the CLI:

```json
{
    "computeType": "aks",
    "autoScaler":
    {
        "autoscaleEnabled": true,
        "minReplicas": 1,
        "maxReplicas": 3,
        "refreshPeriodInSeconds": 1,
        "targetUtilization": 70
    },
    "dataCollection":
    {
        "storageEnabled": true
    },
    "authEnabled": true,
    "containerResourceRequirements":
    {
        "cpu": 0.5,
        "memoryInGB": 1.0
    }
}
```

## Next steps

* [Command reference for the Machine Learning CLI extension](/cli/azure/ml).

* [Train and deploy machine learning models using Azure Pipelines](/azure/devops/pipelines/targets/azure-machine-learning)
