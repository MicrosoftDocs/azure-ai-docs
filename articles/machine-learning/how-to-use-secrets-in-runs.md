---
title: Authentication secrets
titleSuffix: Azure Machine Learning
description: Learn how to securely get secrets from Azure Key Vault in your training jobs by using the Key Vault Secrets client library.
services: machine-learning
author: s-polly
ms.author: scottpolly
ms.reviewer: shshubhe
ms.service: azure-machine-learning
ms.subservice: enterprise-readiness
ms.date: 03/12/2026
ms.topic: how-to
ms.custom: sdkv2, FY25Q1-Linter, dev-focus
ai-usage: ai-assisted
ms.custom: sdkv2, FY25Q1-Linter, dev-focus
ai-usage: ai-assisted
# Customer intent: As a data scientist, I want to securely access secrets from Azure Key Vault in my training jobs so that I can use them in my training scripts.
---

# Use authentication credential secrets in Azure Machine Learning jobs

[!INCLUDE [sdk v2](includes/machine-learning-sdk-v2.md)]

Authentication information, such as your user name and password, are secrets. For example, if you connect to an external database to query training data, you need to pass your user name and password to the remote job context. Coding such values into training scripts in clear text is insecure because it exposes the secret.

Azure Key Vault provides secure storage and retrieval of secrets. In this article, learn how to retrieve secrets stored in a key vault from a training job running on a compute cluster.

> [!IMPORTANT]
> Use the [Azure Key Vault Secrets client library for Python](/python/api/overview/azure/keyvault-secrets-readme) to store and retrieve secrets. The Azure Machine Learning SDK v2 provides workspace information you need to connect to your key vault.

## Prerequisites

Before following the steps in this article, make sure you have the following prerequisites:

> [!TIP]
> Many of the prerequisites in this section require __Contributor__, __Owner__, or equivalent access to your Azure subscription, or the Azure Resource Group that contains the resources. You might need to contact your Azure administrator and have them perform these actions.

* An Azure subscription. If you don't have an Azure subscription, create a free account before you begin. Try the [free or paid version of Azure Machine Learning](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

* Python 3.10 or later. The `azure-keyvault-secrets` and `azure-identity` packages require Python 3.9 or later, but Python 3.10 or later is recommended.

* An Azure Machine Learning workspace. If you don't have one, use the steps in the [Create resources to get started](quickstart-create-resources.md) article to create one.

* An Azure Key Vault. If you used the [Create resources to get started](quickstart-create-resources.md) article to create your workspace, a key vault was created for you. You can also create a separate key vault instance by using the information in the [Quickstart: Create a key vault](/azure/key-vault/general/quick-create-portal) article.

    > [!TIP]
    > You don't have to use the same key vault as the workspace.

* (Optional) An Azure Machine Learning compute cluster configured to use a [managed identity](how-to-create-attach-compute-cluster.md?tabs=azure-studio#set-up-managed-identity). The cluster can be configured for either a system-assigned or user-assigned managed identity.

* If your job runs on a compute cluster, grant the managed identity for the compute cluster access to the secrets stored in key vault. Or, if the job runs on serverless compute, grant the managed identity specified for the job access to the secrets. The method used to grant access depends on how your key vault is configured:

    * [Azure role-based access control (Azure RBAC)](/azure/key-vault/general/rbac-guide): When configured for Azure RBAC, add the managed identity to the __Key Vault Secrets User__ role on your key vault.
    * [Azure Key Vault access policy](/azure/key-vault/general/assign-access-policy): When configured to use access policies, add a new policy that grants the __get__ operation for secrets and assign it to the managed identity.

* A stored secret value in the key vault. You can retrieve this value by using a key. For more information, see [Quickstart: Set and retrieve a secret from Azure Key Vault](/azure/key-vault/secrets/quick-create-python).

    > [!TIP]
    > The quickstart link is to the steps for using the Azure Key Vault Python SDK. In the table of contents in the left pane are links to other ways to set a key.

## Get the key vault URL

When you create an Azure Machine Learning workspace, a default key vault is provisioned alongside it. Use the `MLClient` to retrieve the vault URL programmatically:

```python
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential

subscription_id = "<subscription-id>"
resource_group = "<resource-group>"
workspace_name = "<workspace-name>"

ml_client = MLClient(
    DefaultAzureCredential(),
    subscription_id=subscription_id,
    resource_group_name=resource_group,
    workspace_name=workspace_name,
)

workspace = ml_client.workspaces.get(workspace_name)
key_vault_arm_id = workspace.key_vault
vault_name = key_vault_arm_id.split("/")[-1]
vault_url = f"https://{vault_name}.vault.azure.net/"
print(vault_url)  # https://<your-vault-name>.vault.azure.net/
```

You can then pass this `vault_url` value to your training job as an environment variable, as shown in the examples that follow.

> [!TIP]
> You can also find the key vault URL in the [Azure portal](https://portal.azure.com) by navigating to your workspace and selecting **Overview**. The key vault is listed in the workspace properties.

## Get secrets

You can get secrets during training in two ways:

- Use a managed identity that's associated with the compute resource where the training job runs.
- Use your own identity by having the compute run the job on your behalf.

# [Managed identity](#tab/managed)

1. Add the `azure-keyvault-secrets` and `azure-identity` packages to the [Azure Machine Learning environment](concept-environments.md) that you use to train the model. For example, add them to the conda file used to build the environment.

    Use this environment to build the Docker image that the training job runs in on the compute cluster.

1. From your training code, use the [Azure Identity SDK](/python/api/overview/azure/identity-readme) and [Key Vault client library](/python/api/overview/azure/keyvault-secrets-readme) to get the managed identity credentials and authenticate to key vault. The `KEY_VAULT_URL` environment variable is passed to the job at submission time (see step 3):

    ```python
    import os
    from azure.identity import DefaultAzureCredential
    from azure.keyvault.secrets import SecretClient

    credential = DefaultAzureCredential()

    vault_url = os.environ["KEY_VAULT_URL"]
    secret_client = SecretClient(vault_url=vault_url, credential=credential)
    ```

    > [!TIP]
    > In production, set the `AZURE_TOKEN_CREDENTIALS` environment variable to `ManagedIdentityCredential` to restrict the `DefaultAzureCredential` chain to only the managed identity credential. This change improves startup time and reduces ambiguity.

1. After authenticating, use the Key Vault client library to retrieve a secret by providing the associated key:

    ```python
    secret = secret_client.get_secret("secret-name")
    print(secret.value)
    ```

1. When you submit the training job, pass the key vault URL as an environment variable. Use the `vault_url` value retrieved in [Get the key vault URL](#get-the-key-vault-url):

    ```python
    from azure.ai.ml import command

    job = command(
        code="./src",
        command="python train.py",
        environment="AzureML-sklearn-1.0-ubuntu20.04-py38-cpu:1",
        compute="cpu-cluster",
        environment_variables={"KEY_VAULT_URL": vault_url},
    )

    ml_client.jobs.create_or_update(job)
    ```

# [Your identity](#tab/user)

1. Add the `azure-keyvault-secrets`, `azure-identity`, and `azure-ai-ml` packages to the [Azure Machine Learning environment](concept-environments.md) used when training the model. For example, add them to the conda file used to build the environment.

    Use this environment to build the Docker image that the training job runs in on the compute cluster.

1. From your training code, use the [Azure Machine Learning SDK](/python/api/overview/azure/ai-ml-readme) and [Key Vault client library](/python/api/overview/azure/keyvault-secrets-readme) to authenticate on behalf of your user identity. The `KEY_VAULT_URL` environment variable is passed to the job at submission time (see step 3):

    ```python
    import os
    from azure.ai.ml.identity import AzureMLOnBehalfOfCredential
    from azure.keyvault.secrets import SecretClient

    credential = AzureMLOnBehalfOfCredential()

    vault_url = os.environ["KEY_VAULT_URL"]
    secret_client = SecretClient(vault_url=vault_url, credential=credential)
    ```

    After authenticating, use the Key Vault client library to retrieve a secret by providing the associated key:

    ```python
    secret = secret_client.get_secret("secret-name")
    print(secret.value)
    ```

1. When you submit the training job, specify that it runs on behalf of your identity by using `identity=UserIdentityConfiguration()`. The following example submits a job by using this parameter:

    ```python
    from azure.ai.ml import Input, command
    from azure.ai.ml.constants import AssetTypes
    from azure.ai.ml.entities import UserIdentityConfiguration

    job = command(
        code="./sdk/ml/azure-ai-ml/samples/src",
        command="python read_data.py --input_data ${{inputs.input_data}}",
        inputs={"input_data": Input(type=AssetTypes.MLTABLE, path="./sample_data")},
        environment="AzureML-sklearn-1.0-ubuntu22.04-py39-cpu:1",
        compute="cpu-cluster",
        identity=UserIdentityConfiguration(),
        environment_variables={"KEY_VAULT_URL": vault_url},
    )
    ```    

    For an example of using the Azure CLI to submit a job that uses your identity, see [on-behalf-of job example](https://github.com/Azure/azureml-examples/blob/main/cli/jobs/single-step/on-behalf-of/README.md).

---

## Related content

For an example of submitting a training job by using the Azure Machine Learning Python SDK v2, see [Train models with the Python SDK v2](how-to-train-sdk.md).
