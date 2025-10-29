---
title: Authentication secrets
titleSuffix: Azure Machine Learning
description: Learn how to securely get secrets from Azure Key Vault in your training jobs by using the Key Vault Secrets client library.
services: machine-learning
author: s-polly
ms.author: scottpolly
ms.reviewer: roastala
ms.service: azure-machine-learning
ms.subservice: enterprise-readiness
ms.date: 08/20/2024
ms.topic: how-to
ms.custom: sdkv2, FY25Q1-Linter
# Customer intent: As a data scientist, I want to securely access secrets from Azure Key Vault in my training jobs so that I can use them in my training scripts.
---

# Use authentication credential secrets in Azure Machine Learning jobs

[!INCLUDE [sdk v2](includes/machine-learning-sdk-v2.md)]

Authentication information such as your user name and password are secrets. For example, if you connect to an external database in order to query training data, you would need to pass your username and password to the remote job context. Coding such values into training scripts in clear text is insecure as it would potentially expose the secret.

The Azure Key Vault allows you to securely store and retrieve secrets. In this article, learn how you can retrieve secrets stored in a key vault from a training job running on a compute cluster.

> [!IMPORTANT]
> The Azure Machine Learning Python SDK v2 and Azure CLI extension v2 for machine learning do not provide the capability to set or get secrets. Instead, the information in this article uses the [Azure Key Vault Secrets client library for Python](/python/api/overview/azure/keyvault-secrets-readme).

## Prerequisites

Before following the steps in this article, make sure you have the following prerequisites:

> [!TIP]
> Many of the prerequisites in this section require __Contributor__, __Owner__, or equivalent access to your Azure subscription, or the Azure Resource Group that contains the resources. You might need to contact your Azure administrator and have them perform these actions.

* An Azure subscription. If you don't have an Azure subscription, create a free account before you begin. Try the [free or paid version of Azure Machine Learning](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
 
* An Azure Machine Learning workspace. If you don't have one, use the steps in the [Create resources to get started](quickstart-create-resources.md) article to create one.

* An Azure Key Vault. If you used the [Create resources to get started](quickstart-create-resources.md) article to create your workspace, a key vault was created for you. You can also create a separate key vault instance using the information in the [Quickstart: Create a key vault](/azure/key-vault/general/quick-create-portal) article.

    > [!TIP]
    > You do not have to use same key vault as the workspace.

* (Optional) An Azure Machine Learning compute cluster configured to use a [managed identity](how-to-create-attach-compute-cluster.md?tabs=azure-studio#set-up-managed-identity). The cluster can be configured for either a system-assigned or user-assigned managed identity.

* If your job runs on a compute cluster, grant the managed identity for the compute cluster access to the secrets stored in key vault. Or, if the job runs on serverless compute, grant the managed identity specified for the job access to the secrets. The method used to grant access depends on how your key vault is configured:

    * [Azure role-based access control (Azure RBAC)](/azure/key-vault/general/rbac-guide): When configured for Azure RBAC, add the managed identity to the __Key Vault Secrets User__ role on your key vault.
    * [Azure Key Vault access policy](/azure/key-vault/general/assign-access-policy): When configured to use access policies, add a new policy that grants the __get__ operation for secrets and assign it to the managed identity.

* A stored secret value in the key vault. This value can then be retrieved using a key. For more information, see [Quickstart: Set and retrieve a secret from Azure Key Vault](/azure/key-vault/secrets/quick-create-python).

    > [!TIP]
    > The quickstart link is to the steps for using the Azure Key Vault Python SDK. In the table of contents in the left pane are links to other ways to set a key.

## Get secrets

There are two ways to get secrets during training:

- Using a managed identity associated with the compute resource the training job runs on.
- Using your identity by having the compute run the job on your behalf.

# [Managed identity](#tab/managed)

1. Add the `azure-keyvault-secrets` and `azure-identity` packages to the [Azure Machine Learning environment](concept-environments.md) used when training the model. For example, by adding them to the conda file used to build the environment.

    The environment is used to build the Docker image that the training job runs in on the compute cluster.

1. From your training code, use the [Azure Identity SDK](/python/api/overview/azure/identity-readme) and [Key Vault client library](/python/api/overview/azure/keyvault-secrets-readme) to get the managed identity credentials and authenticate to key vault:

    ```python
    from azure.identity import DefaultAzureCredential
    from azure.keyvault.secrets import SecretClient

    credential = DefaultAzureCredential()

    secret_client = SecretClient(vault_url="https://my-key-vault.vault.azure.net/", credential=credential)
    ```

1. After authenticating, use the Key Vault client library to retrieve a secret by providing the associated key:

    ```python
    secret = secret_client.get_secret("secret-name")
    print(secret.value)
    ```

# [Your identity](#tab/user)

1. Add the `azure-keyvault-secrets`, `azure-identity`, and `azure-ai-ml` packages to the [Azure Machine Learning environment](concept-environments.md) used when training the model. For example, by adding them to the conda file used to build the environment.

    The environment is used to build the Docker image that the training job runs in on the compute cluster.

1. From your training code, use the [Azure Machine Learning SDK](/python/api/overview/azure/ai-ml-readme) and [Key Vault client library](/python/api/overview/azure/keyvault-secrets-readme) to get the managed identity credentials and authenticate to key vault. The `AzureMLOnBehalfOfCredential` class is used to authenticate on behalf of your user identity:

    ```python
    from azure.ai.ml.identity import AzureMLOnBehalfOfCredential
    from azure.keyvault.secrets import SecretClient

    credential = AzureMLOnBehalfOfCredential()
    secret_client = SecretClient(vault_url="https://my-key-vault.vault.azure.net/", credential=credential)
    ```

    After authenticating, use the Key Vault client library to retrieve a secret by providing the associated key:

    ```python
    secret = secret_client.get_secret("secret-name")
    print(secret.value)
    ```

1. When you submit the training job, you must specify that it runs on behalf of your identity by using `identity=UserIdentityConfiguration()`. The following example submits a job using this parameter:

    ```python
    from azure.ai.ml import Input, command
    from azure.ai.ml.constants import AssetTypes
    from azure.ai.ml.entities import UserIdentityConfiguration

    job = command(
        code="./sdk/ml/azure-ai-ml/samples/src",
        command="python read_data.py --input_data ${{inputs.input_data}}",
        inputs={"input_data": Input(type=AssetTypes.MLTABLE, path="./sample_data")},
        environment="AzureML-sklearn-1.0-ubuntu20.04-py38-cpu:1",
        compute="cpu-cluster",
        identity=UserIdentityConfiguration(),
    )
    ```    

    For an example of using the Azure CLI to submit a job that uses your identity, visit [Https://github.com/Azure/azureml-examples/blob/d4c90eead3c1fd97393d0657f7a78831490adf1c/cli/jobs/single-step/on-behalf-of/README.md](https://github.com/Azure/azureml-examples/blob/d4c90eead3c1fd97393d0657f7a78831490adf1c/cli/jobs/single-step/on-behalf-of/README.md).

---

## Related content

For an example of submitting a training job using the Azure Machine Learning Python SDK v2, see [Train models with the Python SDK v2](how-to-train-sdk.md).
