---
title: Run Azure OpenAI models in batch endpoints
titleSuffix: Azure Machine Learning
description: Find out how to compute embeddings by running Azure OpenAI models in batch endpoints. See how to deploy the text-embedding-ada-002 model in MLflow format.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: inferencing
ms.topic: how-to
author: s-polly
ms.author: scottpolly
ms.reviewer: jturuk
ms.date: 12/16/2024
ms.custom: how-to, devplatv2, update-code2
# customer intent: As a developer, I want to deploy an Azure OpenAI ADA-002 model to a batch endpoint so I can compute embeddings at scale.
---

# Run Azure OpenAI models in batch endpoints to compute embeddings

[!INCLUDE [cli v2](includes/machine-learning-dev-v2.md)]

To run inference over large amounts of data, you can use batch endpoints to deploy models, including Azure OpenAI models. In this article, you see how to create a batch endpoint to deploy the `text-embedding-ada-002` model from Azure OpenAI to compute embeddings at scale. You can use the same approach for completions and chat completions models. 

The example in this article uses Microsoft Entra authentication to grant access to an Azure OpenAI in Microsoft Foundry Models resource, but you can also use an access key. The model is registered in MLflow format. It uses the Azure OpenAI flavor, which provides support for calling the Azure OpenAI at scale.

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

## Create an Azure OpenAI resource

This article shows you how to run OpenAI models hosted in Azure OpenAI. To begin, you need an Azure OpenAI resource that's deployed in Azure. For information about creating an Azure OpenAI resource, see [Create a resource](../ai-services/openai/how-to/create-resource.md#create-a-resource).

The name of your Azure OpenAI resource forms part of the resource URL. Use the following command to save that URL for use in later steps.

# [Azure CLI](#tab/cli)

```azurecli
OPENAI_API_BASE="https://<your-azure-openai-resource-name>.openai.azure.com"
```

# [Python SDK](#tab/python)

```python
openai_api_base="https://<your-azure-openai-resource-name>.openai.azure.com"
```

---

In this article, you see how to create a deployment for an Azure OpenAI model. The following image shows a deployed Azure OpenAI model and highlights the Azure OpenAI resource that it's deployed to:

:::image type="content" source="./media/how-to-use-batch-model-openai-embeddings/azure-openai-deployments.png" alt-text="Screenshot of the Azure OpenAI page within Foundry. A model deployment that's available in a particular Azure OpenAI resource is visible." lightbox="media/how-to-use-batch-model-openai-embeddings/azure-openai-deployments.png":::

For information about managing Azure OpenAI models in Azure OpenAI, see [Focus on Azure OpenAI](../ai-studio/azure-openai-in-ai-studio.md#focus-on-azure-openai-service).

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

You can configure the identity of the compute cluster to have access to the Azure OpenAI deployment to get predictions. In this way, you don't need to manage permissions for each endpoint user. To give the identity of the compute cluster access to the Azure OpenAI resource, follow these steps:

1. Assign an identity to the compute cluster that your deployment uses. This example uses a compute cluster called **batch-cluster-lp** and a system-assigned managed identity, but you can use other options. If your compute cluster already has an assigned identity, you can skip this step.

    ```azurecli
    COMPUTE_NAME="batch-cluster-lp"
    az ml compute update --name $COMPUTE_NAME --identity-type system_assigned
    ```

1. Get the managed identity principal ID that's assigned to the compute cluster you plan to use. 

    ```azurecli
    PRINCIPAL_ID=$(az ml compute show -n $COMPUTE_NAME --query identity.principal_id)
    ```

1. Get the unique ID of the resource group where the Azure OpenAI resource is deployed:

    ```azurecli
    RG="<openai-resource-group-name>"
    RESOURCE_ID=$(az group show -g $RG --query "id" -o tsv)
    ```

1. Assign the Cognitive Services User role to the managed identity:

    ```azurecli
    az role assignment create --role "Cognitive Services User" --assignee $PRINCIPAL_ID --scope $RESOURCE_ID
    ```

# [Access keys](#tab/keys)

You can configure the batch deployment to use the access key of your Azure OpenAI resource to get predictions. Copy the access key from your account, and keep it for later steps.

---

## Register the Azure OpenAI model

Model deployments in batch endpoints can deploy only registered models. You can use MLflow models with the Azure OpenAI flavor to create a model in your workspace that references a deployment in Azure OpenAI.

In the cloned repository, the model folder contains an MLflow model that generates embeddings based on the `text-embedding-ada-002` model.

Register the model in the workspace:

# [Azure CLI](#tab/cli)

:::code language="azurecli" source="~/azureml-examples-main/cli/endpoints/batch/deploy-models/openai-embeddings/deploy-and-run.sh" ID="register_model" :::

# [Python SDK](#tab/python)

[!notebook-python[] (~/azureml-examples-main/sdk/python/endpoints/batch/deploy-models/openai-embeddings/deploy-and-test.ipynb?name=register_model)]

---

## Create a deployment for an Azure OpenAI model

To deploy the Azure OpenAI model, you need to create an endpoint, an environment, a scoring script, and a batch deployment. The following sections show you how to set up these components.

### Create an endpoint

An endpoint is needed to host the model. To create an endpoint, take the following steps:

1. Set up a variable to store your endpoint name. Replace the name in the following code with one that's unique within the region of your resource group.

    # [Azure CLI](#tab/cli)

    :::code language="azurecli" source="~/azureml-examples-main/cli/endpoints/batch/deploy-models/openai-embeddings/deploy-and-run.sh" ID="name_endpoint" :::

    # [Python SDK](#tab/python)

    [!notebook-python[] (~/azureml-examples-main/sdk/python/endpoints/batch/deploy-models/openai-embeddings/deploy-and-test.ipynb?name=name_endpoint)]

    ---

1. Configure the endpoint:

    # [Azure CLI](#tab/cli)

    Create a YAML file called endpoint.yml that contains the following lines. Replace the `name` value with your endpoint name. 
    
    :::code language="yaml" source="~/azureml-examples-main/cli/endpoints/batch/deploy-models/openai-embeddings/endpoint.yml":::

    # [Python SDK](#tab/python)

    [!notebook-python[] (~/azureml-examples-main/sdk/python/endpoints/batch/deploy-models/openai-embeddings/deploy-and-test.ipynb?name=configure_endpoint)]

    ---

1. Create the endpoint resource:

    # [Azure CLI](#tab/cli)

    :::code language="azurecli" source="~/azureml-examples-main/cli/endpoints/batch/deploy-models/openai-embeddings/deploy-and-run.sh" ID="create_endpoint" :::

    # [Python SDK](#tab/python)

    [!notebook-python[] (~/azureml-examples-main/sdk/python/endpoints/batch/deploy-models/openai-embeddings/deploy-and-test.ipynb?name=create_endpoint)]

    ---

### Configure an environment

The scoring script in this example uses some libraries that aren't part of the standard OpenAI SDK. Create an environment that contains a base image and also a conda YAML file to capture those dependencies:

# [Azure CLI](#tab/cli)

The environment definition consists of the following lines, which are included in the deployment definition.

:::code language="yaml" source="~/azureml-examples-main/cli/endpoints/batch/deploy-models/openai-embeddings/environment/environment.yml":::

# [Python SDK](#tab/python)

[!notebook-python[] (~/azureml-examples-main/sdk/python/endpoints/batch/deploy-models/openai-embeddings/deploy-and-test.ipynb?name=configure_environment)]

---

The conda YAML file, conda.yml, contains the following lines:

:::code language="yaml" source="~/azureml-examples-main/cli/endpoints/batch/deploy-models/openai-embeddings/environment/conda.yaml":::

### Create a scoring script

This example uses a scoring script that performs the execution. In batch endpoints, MLflow models don't require a scoring script. But this example extends the capabilities of batch endpoints by:

- Allowing the endpoint to read multiple data types, including CSV, TSV, Parquet, JSON, JSON Lines, Arrow, and text formats.
- Adding some validations to ensure the MLflow model has an Azure OpenAI flavor.
- Formatting the output in JSON Lines format.
- Optionally adding the `AZUREML_BI_TEXT_COLUMN` environment variable to control which input field you want to generate embeddings for.

> [!TIP]
> By default, MLflow generates embeddings from the first text column that's available in the input data. If you want to use a different column, set the `AZUREML_BI_TEXT_COLUMN` environment variable to the name of your preferred column. Leave that variable blank if the default behavior works for you.

The scoring script, code/batch_driver.py, contains the following lines:

:::code language="python" source="~/azureml-examples-main/cli/endpoints/batch/deploy-models/openai-embeddings/code/batch_driver.py" :::

### Create a batch deployment

To configure the Azure OpenAI deployment, you use environment variables. Specifically, you use the following keys:

- `OPENAI_API_TYPE` is the type of API and authentication that you want to use.
- `OPENAI_API_BASE` is the URL of your Azure OpenAI resource.
- `OPENAI_API_VERSION` is the version of the API that you plan to use.

# [Microsoft Entra authentication](#tab/ad)

If you use the `OPENAI_API_TYPE` environment variable with a value of `azure_ad`, Azure OpenAI uses Microsoft Entra authentication. No key is required to invoke the Azure OpenAI deployment. Instead, the identity of the cluster is used.

# [Access keys](#tab/keys)

To use an access key instead of Microsoft Entra authentication, you use the following environment variables and values:

- `OPENAI_API_TYPE: "azure"`
- `AZURE_OPENAI_API_KEY: "<your-Azure-OpenAI-resource-key>"`

---

1. Update the values of the authentication and environment variables in the deployment configuration. The following example uses Microsoft Entra authentication:

    # [Azure CLI](#tab/cli)

    The deployment.yml file configures the deployment:

    :::code language="yaml" source="~/azureml-examples-main/cli/endpoints/batch/deploy-models/openai-embeddings/deployment.yml" highlight="26-28":::

    > [!TIP]
    > The `environment_variables` section provides the configuration for the Azure OpenAI deployment. The `OPENAI_API_BASE` value is set when the deployment is created, so you don't have to edit that value in the YAML configuration file.

    # [Python SDK](#tab/python)

    [!notebook-python[] (~/azureml-examples-main/sdk/python/endpoints/batch/deploy-models/openai-embeddings/deploy-and-test.ipynb?name=configure_deployment)]
    
    > [!TIP]
    > The `environment_variables` section provides the configuration for the Azure OpenAI deployment.

    ---

1. Create the deployment.

    # [Azure CLI](#tab/cli)

    :::code language="azurecli" source="~/azureml-examples-main/cli/endpoints/batch/deploy-models/openai-embeddings/deploy-and-run.sh" ID="create_deployment" :::

    # [Python SDK](#tab/python)

    [!notebook-python[] (~/azureml-examples-main/sdk/python/endpoints/batch/deploy-models/openai-embeddings/deploy-and-test.ipynb?name=create_deployment)]

    Set the new deployment as the default one:

    [!notebook-python[] (~/azureml-examples-main/sdk/python/endpoints/batch/deploy-models/openai-embeddings/deploy-and-test.ipynb?name=set_default_deployment)]

    ---

    The batch endpoint is ready for use.  

## Test the deployment
   
For testing the endpoint, you use a sample of the dataset [BillSum: A Corpus for Automatic Summarization of US Legislation](https://arxiv.org/abs/1910.00523). This sample is included in the data folder of the cloned repository.

1. Set up the input data:

    # [Azure CLI](#tab/cli)

    In the commands in this section, use **data** as the name of the folder that contains the input data.

    # [Python SDK](#tab/python)
   
    [!notebook-python[] (~/azureml-examples-main/sdk/python/endpoints/batch/deploy-models/openai-embeddings/deploy-and-test.ipynb?name=configure_inputs)]

    ---

1. Invoke the endpoint:

    # [Azure CLI](#tab/cli)
   
    :::code language="azurecli" source="~/azureml-examples-main/cli/endpoints/batch/deploy-models/openai-embeddings/deploy-and-run.sh" ID="start_batch_scoring_job" :::
   
    # [Python SDK](#tab/python)

    > [!TIP]
    > [!INCLUDE [batch-endpoint-invoke-inputs-sdk](includes/batch-endpoint-invoke-inputs-sdk.md)]

    [!notebook-python[] (~/azureml-examples-main/sdk/python/endpoints/batch/deploy-models/openai-embeddings/deploy-and-test.ipynb?name=start_batch_scoring_job)]

    ---

1. Track the progress:

    # [Azure CLI](#tab/cli)
   
    :::code language="azurecli" source="~/azureml-examples-main/cli/endpoints/batch/deploy-models/openai-embeddings/deploy-and-run.sh" ID="show_job_in_studio" :::
   
    # [Python SDK](#tab/python)
   
    [!notebook-python[] (~/azureml-examples-main/sdk/python/endpoints/batch/deploy-models/openai-embeddings/deploy-and-test.ipynb?name=get_job)]

    ---

1. After the deployment is finished, download the predictions:

    # [Azure CLI](#tab/cli)

    :::code language="azurecli" source="~/azureml-examples-main/cli/endpoints/batch/deploy-models/openai-embeddings/deploy-and-run.sh" ID="download_outputs" :::

    # [Python SDK](#tab/python)

    The deployment creates a child job that implements the scoring. Get a reference to that child job:

    [!notebook-python[] (~/azureml-examples-main/sdk/python/endpoints/batch/deploy-models/openai-embeddings/deploy-and-test.ipynb?name=get_scoring_job_reference)]

    Download the scores:

    [!notebook-python[] (~/azureml-examples-main/sdk/python/endpoints/batch/deploy-models/openai-embeddings/deploy-and-test.ipynb?name=download_outputs)]

    ---

1. Use the following code to view the output predictions:

    ```python
    import pandas as pd
    from io import StringIO

    # Read the output data into an object.
    with open('embeddings.jsonl', 'r') as f:
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

    You can also open the output file, embeddings.jsonl, to see the predictions:
    
    ```jsonl
    {"file": "billsum-0.csv", "row": 0, "embeddings": [[0, 0, 0, 0, 0, 0, 0]]}
    {"file": "billsum-0.csv", "row": 1, "embeddings": [[0, 0, 0, 0, 0, 0, 0]]}
    ```

## Related content

- [Create jobs and input data for batch endpoints](how-to-access-data-batch-endpoints-jobs.md)
