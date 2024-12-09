---
title: 'Run Azure OpenAI models in batch endpoints'
titleSuffix: Azure Machine Learning
description: In this article, learn how to use batch endpoints with Azure OpenAI models.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: inferencing
ms.topic: conceptual
author: msakande
ms.author: mopeakande
ms.reviewer: cacrest
ms.date: 11/04/2023
ms.custom: how-to, devplatv2, update-code
---

# Run Azure OpenAI models in batch endpoints to compute embeddings

[!INCLUDE [cli v2](includes/machine-learning-dev-v2.md)]

Batch Endpoints can deploy models to run inference over large amounts of data, including Azure OpenAI models. In this example, you learn how to create a batch endpoint to deploy `text-embedding-ada-002` model from Azure OpenAI to compute embeddings at scale but you can use the same approach for completions and chat completions models. It uses Microsoft Entra authentication to grant access to the Azure OpenAI resource.

## About this example

In this example, we're going to compute embeddings over a dataset using `text-embedding-ada-002` model via the Azure OpenAI Service. We will register the particular model in MLflow format using the Azure OpenAI flavor which has support to orchestrate all the calls to the Azure OpenAI Service at scale.

[!INCLUDE [machine-learning-batch-clone](includes/azureml-batch-clone-samples.md)]

The files for this example are in:

```azurecli
cd endpoints/batch/deploy-models/openai-embeddings
```

### Follow along in Jupyter Notebooks

You can follow along this sample in the following notebooks. In the cloned repository, open the notebook: [deploy-and-test.ipynb](https://github.com/Azure/azureml-examples/blob/main/sdk/python/endpoints/batch/deploy-models/openai-embeddings/deploy-and-test.ipynb).

## Prerequisites

[!INCLUDE [machine-learning-batch-prereqs](includes/azureml-batch-prereqs.md)]


### Ensure you have an Azure OpenAI deployment

The example shows how to run OpenAI models hosted in Azure OpenAI Service. To begin, you need an Azure OpenAI resource correctly deployed in Azure and a deployment for the model you want to use. To deploy an Azure OpenAI model in Azure OpenAI Service, see [Focus on Azure OpenAI Service](../ai-studio/azure-openai-in-ai-studio.md#focus-on-azure-openai-service).

:::image type="content" source="./media/how-to-use-batch-model-openai-embeddings/aoai-deployments.png" alt-text="A screenshot of the Azure OpenAI Service page within Azure AI Foundry, showing the model deployments available in a particular Azure OpenAI Service resource." lightbox="media/how-to-use-batch-model-openai-embeddings/aoai-deployments.png":::

The previous image is an example that shows a deployed Azure OpenAI model and the Azure OpenAI Service resource to which it is deployed. Note the name of the resource used for your model deployment, as you use it later to construct the URL of the resource. 

# [Azure CLI](#tab/cli)

```azurecli
OPENAI_API_BASE="https://<your-azure-openai-resource-name>.openai.azure.com"
```

# [Python](#tab/python)

```python
openai_api_base="https://<your-azure-openai-resource-name>.openai.azure.com"
```

---

### Ensure you have a compute cluster where to deploy the endpoint

Batch endpoints use compute cluster to run the models. In this example, we use a compute cluster called **batch-cluster**. We create the compute cluster here but you can skip this step if you already have one:

# [Azure CLI](#tab/cli)

```azurecli
COMPUTE_NAME="batch-cluster"
az ml compute create -n batch-cluster --type amlcompute --min-instances 0 --max-instances 5
```

# [Python](#tab/python)

[!notebook-python[] (~/azureml-examples-main/sdk/python/endpoints/batch/deploy-models/openai-embeddings/deploy-and-test.ipynb?name=create_compute)]

---

### Decide in the authentication mode

You can access the Azure OpenAI resource in two ways:

* Using Microsoft Entra authentication (recommended).
* Using an access key.

Using Microsoft Entra is recommended because it helps you avoid managing secrets in the deployments.

# [Microsoft Entra authentication](#tab/ad)

You can configure the identity of the compute to have access to the Azure OpenAI deployment to get predictions. In this way, you don't need to manage permissions for each of the users using the endpoint. To configure the identity of the compute cluster get access to the Azure OpenAI resource, follow these steps:

1. Ensure or assign an identity to the compute cluster your deployment uses. In this example, we use a compute cluster called **batch-cluster** and we assign a system assigned managed identity, but you can use other alternatives.

    ```azurecli
    COMPUTE_NAME="batch-cluster"
    az ml compute update --name $COMPUTE_NAME --identity-type system_assigned
    ```

1. Get the managed identity principal ID assigned to the compute cluster you plan to use. 

    ```azurecli
    PRINCIPAL_ID=$(az ml compute show -n $COMPUTE_NAME --query identity.principal_id)
    ```

1. Get the unique ID of the resource group where the Azure OpenAI resource is deployed:

    ```azurecli
    RG="<openai-resource-group-name>"
    RESOURCE_ID=$(az group show -g $RG --query "id" -o tsv)
    ```

1. Grant the role **Cognitive Services User** to the managed identity:

    ```azurecli
    az role assignment create --role "Cognitive Services User" --assignee $PRINCIPAL_ID --scope $RESOURCE_ID
    ```

# [Access keys](#tab/keys)

You can get an access key and configure the batch deployment to use the access key to get predictions. Grab the access key from your account and keep it for future reference in this tutorial.

---


### Register the Azure OpenAI model

Model deployments in batch endpoints can only deploy registered models. You can use MLflow models with the Azure OpenAI flavor to create a model in your workspace referencing a deployment in Azure OpenAI.

1. Create an MLflow model in the workspace's models registry pointing to your Azure OpenAI deployment with the model you want to use. Use the MLflow SDK to create the model:

    > [!TIP]
    > In the cloned repository in the **model** folder, you already have an MLflow model to generate embeddings based on `text-embedding-ada-002` model in case you want to skip this step.

    ```python
    import mlflow
    import openai

    engine = openai.Model.retrieve("text-embedding-ada-002")

    model_info = mlflow.openai.save_model(
        path="model",
        model="text-embedding-ada-002",
        engine=engine.id,
        task=openai.Embedding,
    )
    ```

1. Register the model in the workspace:
   
    # [Azure CLI](#tab/cli)

    :::code language="azurecli" source="~/azureml-examples-main/cli/endpoints/batch/deploy-models/openai-embeddings/deploy-and-run.sh" ID="register_model" :::

    # [Python](#tab/python)

    [!notebook-python[] (~/azureml-examples-main/sdk/python/endpoints/batch/deploy-models/openai-embeddings/deploy-and-test.ipynb?name=register_model)]


## Create a deployment for an Azure OpenAI model

1. First, let's create the endpoint that hosts the model. Decide on the name of the endpoint:

    # [Azure CLI](#tab/cli)

    :::code language="azurecli" source="~/azureml-examples-main/cli/endpoints/batch/deploy-models/openai-embeddings/deploy-and-run.sh" ID="name_endpoint" :::

    # [Python](#tab/python)

    [!notebook-python[] (~/azureml-examples-main/sdk/python/endpoints/batch/deploy-models/openai-embeddings/deploy-and-test.ipynb?name=name_endpoint)]


1. Configure the endpoint:

    # [Azure CLI](#tab/cli)

    The following YAML file defines a batch endpoint:
    
    __endpoint.yml__
    
    :::code language="yaml" source="~/azureml-examples-main/cli/endpoints/batch/deploy-models/openai-embeddings/endpoint.yml":::

    # [Python](#tab/python)

    [!notebook-python[] (~/azureml-examples-main/sdk/python/endpoints/batch/deploy-models/openai-embeddings/deploy-and-test.ipynb?name=configure_endpoint)]

1. Create the endpoint resource:

    # [Azure CLI](#tab/cli)

    :::code language="azurecli" source="~/azureml-examples-main/cli/endpoints/batch/deploy-models/openai-embeddings/deploy-and-run.sh" ID="create_endpoint" :::

    # [Python](#tab/python)

    [!notebook-python[] (~/azureml-examples-main/sdk/python/endpoints/batch/deploy-models/openai-embeddings/deploy-and-test.ipynb?name=create_endpoint)]

1. Our scoring script uses some specific libraries that are not part of the standard OpenAI SDK so we need to create an environment that have them. Here, we configure an environment with a base image a conda YAML.

    # [Azure CLI](#tab/cli)

    __environment/environment.yml__

    :::code language="yaml" source="~/azureml-examples-main/cli/endpoints/batch/deploy-models/openai-embeddings/environment/environment.yml":::

    # [Python](#tab/python)

    [!notebook-python[] (~/azureml-examples-main/sdk/python/endpoints/batch/deploy-models/openai-embeddings/deploy-and-test.ipynb?name=configure_environment)]
    
    ---

    The conda YAML looks as follows:

    __conda.yaml__

    :::code language="yaml" source="~/azureml-examples-main/cli/endpoints/batch/deploy-models/openai-embeddings/environment/conda.yaml":::

1. Let's create a scoring script that performs the execution. In Batch Endpoints, MLflow models don't require a scoring script. However, in this case we want to extend a bit the capabilities of batch endpoints by:

    > [!div class="checklist"]
    > * Allow the endpoint to read multiple data types, including `csv`, `tsv`, `parquet`, `json`, `jsonl`, `arrow`, and `txt`.
    > * Add some validations to ensure the MLflow model used has an Azure OpenAI flavor on it.
    > * Format the output in `jsonl` format.
    > * Add an environment variable `AZUREML_BI_TEXT_COLUMN` to control (optionally) which input field you want to generate embeddings for.

    > [!TIP]
    > By default, MLflow will use the first text column available in the input data to generate embeddings from. Use the environment variable `AZUREML_BI_TEXT_COLUMN` with the name of an existing column in the input dataset to change the column if needed. Leave it blank if the default behavior works for you.
    
    The scoring script looks as follows:

    __code/batch_driver.py__

    :::code language="python" source="~/azureml-examples-main/cli/endpoints/batch/deploy-models/openai-embeddings/code/batch_driver.py" :::

1. One the scoring script is created, it's time to create a batch deployment for it. We use environment variables to configure the Azure OpenAI deployment. Particularly we use the following keys:

    * `OPENAI_API_BASE` is the URL of the Azure OpenAI resource to use.
    * `OPENAI_API_VERSION` is the version of the API you plan to use.
    * `OPENAI_API_TYPE` is the type of API and authentication you want to use.

    # [Microsoft Entra authentication](#tab/ad)

    The environment variable `OPENAI_API_TYPE="azure_ad"` instructs the Azure OpenAI Service to use Microsoft Entra authentication and hence no key is required to invoke the Azure OpenAI deployment. The identity of the cluster is used instead.
    
    # [Access keys](#tab/keys)

    To use access keys instead of Microsoft Entra authentication, we need the following environment variables:

    * Use `OPENAI_API_TYPE="azure"`
    * Use `AZURE_OPENAI_API_KEY="<YOUR_AZURE_OPENAI_KEY>"`

1. Once we decided on the authentication and the environment variables, we can use them in the deployment. The following example shows how to use Microsoft Entra authentication particularly:

    # [Azure CLI](#tab/cli)

    __deployment.yml__

    :::code language="yaml" source="~/azureml-examples-main/cli/endpoints/batch/deploy-models/openai-embeddings/deployment.yml" highlight="26-28":::

    > [!TIP]
    > Notice the `environment_variables` section where we indicate the configuration for the Azure OpenAI deployment. The value for `OPENAI_API_BASE` will be set later in the creation command so you don't have to edit the YAML configuration file.

    # [Python](#tab/python)

    [!notebook-python[] (~/azureml-examples-main/sdk/python/endpoints/batch/deploy-models/openai-embeddings/deploy-and-test.ipynb?name=configure_deployment)]
    
    > [!TIP]
    > Notice the `environment_variables` section where we indicate the configuration for the Azure OpenAI deployment.

1. Now, let's create the deployment.

    # [Azure CLI](#tab/cli)

    :::code language="azurecli" source="~/azureml-examples-main/cli/endpoints/batch/deploy-models/openai-embeddings/deploy-and-run.sh" ID="create_deployment" :::

    # [Python](#tab/python)

    [!notebook-python[] (~/azureml-examples-main/sdk/python/endpoints/batch/deploy-models/openai-embeddings/deploy-and-test.ipynb?name=create_deployment)]

    Finally, set the new deployment as the default one:

    [!notebook-python[] (~/azureml-examples-main/sdk/python/endpoints/batch/deploy-models/openai-embeddings/deploy-and-test.ipynb?name=set_default_deployment)]

1. At this point, our batch endpoint is ready to be used.  

## Test the deployment
   
For testing our endpoint, we are going to use a sample of the dataset [BillSum: A Corpus for Automatic Summarization of US Legislation](https://arxiv.org/abs/1910.00523). This sample is included in the repository in the folder data.

1. Create a data input for this model:

   # [Azure CLI](#tab/cli)
   
   :::code language="azurecli" source="~/azureml-examples-main/cli/endpoints/batch/deploy-models/imagenet-classifier/deploy-and-run.sh" ID="show_job_in_studio" :::
   
   # [Python](#tab/python)
   
   ```python
   ml_client.jobs.get(job.name)
   ```

1. Invoke the endpoint:

   # [Azure CLI](#tab/cli)
   
   :::code language="azurecli" source="~/azureml-examples-main/cli/endpoints/batch/deploy-models/openai-embeddings/deploy-and-run.sh" ID="start_batch_scoring_job" :::
   
   # [Python](#tab/python)

   > [!TIP]
   > [!INCLUDE [batch-endpoint-invoke-inputs-sdk](includes/batch-endpoint-invoke-inputs-sdk.md)]

   [!notebook-python[] (~/azureml-examples-main/sdk/python/endpoints/batch/deploy-models/openai-embeddings/deploy-and-test.ipynb?name=start_batch_scoring_job)]

1. Track the progress:

   # [Azure CLI](#tab/cli)
   
   :::code language="azurecli" source="~/azureml-examples-main/cli/endpoints/batch/deploy-models/openai-embeddings/deploy-and-run.sh" ID="show_job_in_studio" :::
   
   # [Python](#tab/python)
   
   [!notebook-python[] (~/azureml-examples-main/sdk/python/endpoints/batch/deploy-models/openai-embeddings/deploy-and-test.ipynb?name=get_job)]

1. Once the deployment is finished, we can download the predictions:

   # [Azure CLI](#tab/cli)

   To download the predictions, use the following command:

    :::code language="azurecli" source="~/azureml-examples-main/cli/endpoints/batch/deploy-models/openai-embeddings/deploy-and-run.sh" ID="download_outputs" :::

   # [Python](#tab/python)

   [!notebook-python[] (~/azureml-examples-main/sdk/python/endpoints/batch/deploy-models/openai-embeddings/deploy-and-test.ipynb?name=download_outputs)]

1. The output predictions look like the following.

    ```python
    import pandas as pd 
       
    embeddings = pd.read_json("named-outputs/score/embeddings.jsonl", lines=True)
    embeddings
    ```

    __embeddings.jsonl__
    
    ```json
    {
        "file": "billsum-0.csv",
        "row": 0,
        "embeddings": [
            [0, 0, 0 ,0 , 0, 0, 0 ]
        ]
    },
    {
        "file": "billsum-0.csv",
        "row": 1,
        "embeddings": [
            [0, 0, 0 ,0 , 0, 0, 0 ]
        ]
    },
    ```
    
## Next steps

* [Create jobs and input data for batch endpoints](how-to-access-data-batch-endpoints-jobs.md)
