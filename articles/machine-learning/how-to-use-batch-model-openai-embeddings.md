---
title: Run OpenAI models in batch endpoints
titleSuffix: Azure Machine Learning
description: In this article, learn how to use batch endpoints with OpenAI models.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: inferencing
ms.topic: how-to
author: msakande
ms.author: mopeakande
ms.reviewer: cacrest
ms.date: 11/13/2024
ms.custom: how-to, devplatv2, update-code
---

# Run OpenAI models in batch endpoints to compute embeddings

[!INCLUDE [cli v2](includes/machine-learning-dev-v2.md)]

To run inference over large amounts of data, you can use batch endpoints to deploy models, including OpenAI models. In this article, you see how to create a batch endpoint to deploy an ADA-002 model from OpenAI to compute embeddings at scale. You can use the same approach for completions and chat completions models. 

The examples in this article use Microsoft Entra authentication to grant access to the Azure OpenAI resource. The model is registered in MLflow format. It uses the OpenAI flavor, which provides support for calling the OpenAI service at scale.

To follow along with the example steps, see the Jupyter notebook [Score OpenAI models in batch using Batch Endpoints](https://github.com/Azure/azureml-examples/blob/main/sdk/python/endpoints/batch/deploy-models/openai-embeddings/deploy-and-test.ipynb).

## Prerequisites

[!INCLUDE [machine-learning-batch-prereqs](includes/azureml-batch-prereqs.md)]

## Clone the examples repository

[!INCLUDE [machine-learning-batch-clone](includes/azureml-batch-clone-samples.md)]

Use the following command to go to the folder for this example:

# [Azure CLI](#tab/cli)

```azurecli
cd endpoints/batch/deploy-models/openai-embeddings
```

# [Python SDK](#tab/python)

```python
cd endpoints/batch/deploy-models/openai-embeddings
```

---

## Create an OpenAI resource

This article shows you how to run OpenAI models hosted in Azure OpenAI Service. To follow the steps, you need an OpenAI resource that's deployed in Azure. For information about creating an Azure OpenAI Service resource, see [Create a resource](../ai-services/openai/how-to/create-resource.md#create-a-resource).

:::image type="content" source="./media/how-to-use-batch-model-openai-embeddings/aoai-deployments.png" alt-text="An screenshot showing the Azure OpenAI studio with the list of model deployments available.":::

The name of your OpenAI resource forms part of the resource URL. Use the following command to save that URL for use in later steps.

# [Azure CLI](#tab/cli)

```azurecli
OPENAI_API_BASE="https://<your-azure-openai-resource-name>.openai.azure.com"
```

# [Python SDK](#tab/python)

```python
openai_api_base="https://<your-azure-openai-resource-name>.openai.azure.com"
```

---

## Create a compute cluster

Batch endpoints use a compute cluster to run models. Use the following code to create a compute cluster called **batch-cluster-lp**. If you already have a compute cluster, you can skip this step.

# [Azure CLI](#tab/cli)

```azurecli
COMPUTE_NAME="batch-cluster-lp"
az ml compute create -n batch-cluster-lp --type amlcompute --min-instances 0 --max-instances 5
```

# [Python SDK](#tab/python)

[!notebook-python[] (~/azureml-examples-main/sdk/python/endpoints/batch/deploy-models/openai-embeddings/deploy-and-test.ipynb?name=create_compute)]

---

## Choose an authentication mode

You can access the Azure OpenAI resource in two ways:

* Microsoft Entra authentication (recommended)
* An access key

Using Microsoft Entra is recommended because it helps you avoid managing secrets in deployments.

# [Microsoft Entra authentication](#tab/ad)

You can configure the identity of the compute instance to have access to the Azure OpenAI deployment to get predictions. In this way, you don't need to manage permissions for each endpoint user. To give the identity of the compute cluster access to the Azure OpenAI resource, follow these steps:

1. Assign an identity to the compute cluster that your deployment uses. This example uses a compute cluster called **batch-cluster-lp** and a system-assigned managed identity, but you can use other alternatives. If your compute cluster already has an assigned identity, you can skip this step.

    ```azurecli
    COMPUTE_NAME="batch-cluster-lp"
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

You can configure the batch deployment to use the OpenAI resource access key to get predictions. Copy the access key from your account, and keep it for later steps.

---


### Register the OpenAI model

Model deployments in batch endpoints can only deploy registered models. You can use MLflow models with the flavor OpenAI to create a model in your workspace referencing a deployment in Azure OpenAI.

1. Create an MLflow model in the workspace's models registry pointing to your OpenAI deployment with the model you want to use. Use MLflow SDK to create the model:

    > [!TIP]
    > In the cloned repository in the folder **model** you already have an MLflow model to generate embeddings based on ADA-002 model in case you want to skip this step.

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

    # [Python SDK](#tab/python)

    [!notebook-python[] (~/azureml-examples-main/sdk/python/endpoints/batch/deploy-models/openai-embeddings/deploy-and-test.ipynb?name=register_model)]


## Create a deployment for an OpenAI model

1. First, let's create the endpoint that hosts the model. Decide on the name of the endpoint:

    # [Azure CLI](#tab/cli)

    :::code language="azurecli" source="~/azureml-examples-main/cli/endpoints/batch/deploy-models/openai-embeddings/deploy-and-run.sh" ID="name_endpoint" :::

    # [Python SDK](#tab/python)

    [!notebook-python[] (~/azureml-examples-main/sdk/python/endpoints/batch/deploy-models/openai-embeddings/deploy-and-test.ipynb?name=name_endpoint)]


1. Configure the endpoint:

    # [Azure CLI](#tab/cli)

    The following YAML file defines a batch endpoint:
    
    __endpoint.yml__
    
    :::code language="yaml" source="~/azureml-examples-main/cli/endpoints/batch/deploy-models/openai-embeddings/endpoint.yml":::

    # [Python SDK](#tab/python)

    [!notebook-python[] (~/azureml-examples-main/sdk/python/endpoints/batch/deploy-models/openai-embeddings/deploy-and-test.ipynb?name=configure_endpoint)]

1. Create the endpoint resource:

    # [Azure CLI](#tab/cli)

    :::code language="azurecli" source="~/azureml-examples-main/cli/endpoints/batch/deploy-models/openai-embeddings/deploy-and-run.sh" ID="create_endpoint" :::

    # [Python SDK](#tab/python)

    [!notebook-python[] (~/azureml-examples-main/sdk/python/endpoints/batch/deploy-models/openai-embeddings/deploy-and-test.ipynb?name=create_endpoint)]

1. Our scoring script uses some specific libraries that are not part of the standard OpenAI SDK so we need to create an environment that have them. Here, we configure an environment with a base image a conda YAML.

    # [Azure CLI](#tab/cli)

    __environment/environment.yml__

    :::code language="yaml" source="~/azureml-examples-main/cli/endpoints/batch/deploy-models/openai-embeddings/environment/environment.yml":::

    # [Python SDK](#tab/python)

    [!notebook-python[] (~/azureml-examples-main/sdk/python/endpoints/batch/deploy-models/openai-embeddings/deploy-and-test.ipynb?name=configure_environment)]
    
    ---

    The conda YAML looks as follows:

    __conda.yaml__

    :::code language="yaml" source="~/azureml-examples-main/cli/endpoints/batch/deploy-models/openai-embeddings/environment/conda.yaml":::

1. Let's create a scoring script that performs the execution. In Batch Endpoints, MLflow models don't require a scoring script. However, in this case we want to extend a bit the capabilities of batch endpoints by:

    > [!div class="checklist"]
    > * Allow the endpoint to read multiple data types, including `csv`, `tsv`, `parquet`, `json`, `jsonl`, `arrow`, and `txt`.
    > * Add some validations to ensure the MLflow model used has an OpenAI flavor on it.
    > * Format the output in `jsonl` format.
    > * Add an environment variable `AZUREML_BI_TEXT_COLUMN` to control (optionally) which input field you want to generate embeddings for.

    > [!TIP]
    > By default, MLflow will use the first text column available in the input data to generate embeddings from. Use the environment variable `AZUREML_BI_TEXT_COLUMN` with the name of an existing column in the input dataset to change the column if needed. Leave it blank if the default behavior works for you.
    
    The scoring script looks as follows:

    __code/batch_driver.py__

    :::code language="python" source="~/azureml-examples-main/cli/endpoints/batch/deploy-models/openai-embeddings/code/batch_driver.py" :::

1. One the scoring script is created, it's time to create a batch deployment for it. We use environment variables to configure the OpenAI deployment. Particularly we use the following keys:

    * `OPENAI_API_BASE` is the URL of the Azure OpenAI resource to use.
    * `OPENAI_API_VERSION` is the version of the API you plan to use.
    * `OPENAI_API_TYPE` is the type of API and authentication you want to use.

    # [Microsoft Entra authentication](#tab/ad)

    The environment variable `OPENAI_API_TYPE="azure_ad"` instructs OpenAI to use Active Directory authentication and hence no key is required to invoke the OpenAI deployment. The identity of the cluster is used instead.
    
    # [Access keys](#tab/keys)

    To use access keys instead of Microsoft Entra authentication, we need the following environment variables:

    * Use `OPENAI_API_TYPE="azure"`
    * Use `OPENAI_API_KEY="<YOUR_AZURE_OPENAI_KEY>"`

1. Once we decided on the authentication and the environment variables, we can use them in the deployment. The following example shows how to use Microsoft Entra authentication particularly:

    # [Azure CLI](#tab/cli)

    __deployment.yml__

    :::code language="yaml" source="~/azureml-examples-main/cli/endpoints/batch/deploy-models/openai-embeddings/deployment.yml" highlight="26-28":::

    > [!TIP]
    > Notice the `environment_variables` section where we indicate the configuration for the OpenAI deployment. The value for `OPENAI_API_BASE` will be set later in the creation command so you don't have to edit the YAML configuration file.

    # [Python SDK](#tab/python)

    [!notebook-python[] (~/azureml-examples-main/sdk/python/endpoints/batch/deploy-models/openai-embeddings/deploy-and-test.ipynb?name=configure_deployment)]
    
    > [!TIP]
    > Notice the `environment_variables` section where we indicate the configuration for the OpenAI deployment.

1. Now, let's create the deployment.

    # [Azure CLI](#tab/cli)

    :::code language="azurecli" source="~/azureml-examples-main/cli/endpoints/batch/deploy-models/openai-embeddings/deploy-and-run.sh" ID="create_deployment" :::

    # [Python SDK](#tab/python)

    [!notebook-python[] (~/azureml-examples-main/sdk/python/endpoints/batch/deploy-models/openai-embeddings/deploy-and-test.ipynb?name=create_deployment)]

    Finally, set the new deployment as the default one:

    [!notebook-python[] (~/azureml-examples-main/sdk/python/endpoints/batch/deploy-models/openai-embeddings/deploy-and-test.ipynb?name=set_default_deployment)]

1. At this point, our batch endpoint is ready to be used.  

## Test the deployment
   
For testing our endpoint, we are going to use a sample of the dataset [BillSum: A Corpus for Automatic Summarization of US Legislation](https://arxiv.org/abs/1910.00523). This sample is included in the repository in the folder data.

1. Create a data input for this model:

   # [Azure CLI](#tab/cli)
   
   1. Create a YAML file, bill-summarization.yml:

   ```yml
   $schema: https://azuremlschemas.azureedge.net/latest/data.schema.json
   name: bill_summarization
   description: A sample of a dataset for summarization of US Congressional and California state bills.
   type: uri_file
   path: data/billsum-0.csv
   ```

   1. Create a data asset.

      ```azurecli
      az ml data create -f bill-summarization.yml
      ```

   1. Get the ID of the data asset.

      ```azurecli
      DATA_ASSET_ID=$(az ml data show -n bill_summarization --label latest | jq -r .id)
      ```

   # [Python SDK](#tab/python)
   
   [!notebook-python[] (~/azureml-examples-main/sdk/python/endpoints/batch/deploy-models/openai-embeddings/deploy-and-test.ipynb?name=configure_inputs)]

1. Invoke the endpoint:

   # [Azure CLI](#tab/cli)
   
   ```azurecli
   JOB_NAME=$(az ml batch-endpoint invoke --name $ENDPOINT_NAME --set inputs.bill_summarization.type="uri_file" inputs.bill_summarization.path=$DATASET_ID --query name -o tsv)
   ```
   
   # [Python SDK](#tab/python)

   > [!TIP]
   > [!INCLUDE [batch-endpoint-invoke-inputs-sdk](includes/batch-endpoint-invoke-inputs-sdk.md)]

   [!notebook-python[] (~/azureml-examples-main/sdk/python/endpoints/batch/deploy-models/openai-embeddings/deploy-and-test.ipynb?name=start_batch_scoring_job)]

1. Track the progress:

   # [Azure CLI](#tab/cli)
   
   :::code language="azurecli" source="~/azureml-examples-main/cli/endpoints/batch/deploy-models/openai-embeddings/deploy-and-run.sh" ID="show_job_in_studio" :::
   
   # [Python SDK](#tab/python)
   
   [!notebook-python[] (~/azureml-examples-main/sdk/python/endpoints/batch/deploy-models/openai-embeddings/deploy-and-test.ipynb?name=get_job)]

1. Once the deployment is finished, we can download the predictions:

   # [Azure CLI](#tab/cli)

   To download the predictions, use the following command:

    :::code language="azurecli" source="~/azureml-examples-main/cli/endpoints/batch/deploy-models/openai-embeddings/deploy-and-run.sh" ID="download_outputs" :::

   # [Python SDK](#tab/python)

   The deployment creates a child job that implements the scoring. Get a reference to that child job:

   ```python
   scoring_job = list(ml_client.jobs.list(parent_job_name=job.name))[0]
   ```

   Download the scores:

   [!notebook-python[] (~/azureml-examples-main/sdk/python/endpoints/batch/deploy-models/openai-embeddings/deploy-and-test.ipynb?name=download_outputs)]

1. The output predictions look like the following.

    ```python
    import pandas as pd
    from io import StringIO

    # Read the output data into an object.
    with open('sample-output.jsonl', 'r') as f:
        json_lines = f.readlines()
    string_io = StringIO()
    for line in json_lines:
        string_io.write(line)
    string_io.seek(0)

    # Read the data into a data frame.
    embeddings = pd.read_json(string_io, lines=True)

    # Print the data frame.
    print(embeddings)
    ```

    __embeddings.jsonl__
    
    ```json
    {
        "file": "billsum-0.csv",
        "row": 0,
        "embeddings": [
            [0, 0, 0, 0, 0, 0, 0 ]
        ]
    },
    {
        "file": "billsum-0.csv",
        "row": 1,
        "embeddings": [
            [0, 0, 0, 0, 0, 0, 0 ]
        ]
    },
    ```
    
## Next steps

* [Create jobs and input data for batch endpoints](how-to-access-data-batch-endpoints-jobs.md)
