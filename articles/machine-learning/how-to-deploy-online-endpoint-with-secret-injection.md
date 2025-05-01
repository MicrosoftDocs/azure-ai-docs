---
title: Access secrets from online deployment using secret injection (preview)
titleSuffix: Azure Machine Learning
description: Learn to use secret injection with online endpoint and deployment to access secrets like API keys.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: inferencing
author: msakande
ms.author: mopeakande
ms.reviewer: sehan
ms.date: 01/10/2024
ms.topic: how-to
ms.custom: how-to, ignite-2023, sdkv2, devx-track-azurecli
---

# Access secrets from online deployment using secret injection (preview)

[!INCLUDE [dev v2](includes/machine-learning-dev-v2.md)]

In this article, you learn to use secret injection with an online endpoint and deployment to access secrets from a secret store. 

You'll learn to:

> [!div class="checklist"]
> * Set up your user identity and its permissions
> * Create workspace connections and/or key vaults to use as secret stores
> * Create the endpoint and deployment by using the secret injection feature

[!INCLUDE [machine-learning-preview-generic-disclaimer](includes/machine-learning-preview-generic-disclaimer.md)]

## Prerequisites

- To use Azure Machine Learning, you must have an Azure subscription. If you don't have an Azure subscription, create a free account before you begin. Try the [free or paid version of Azure Machine Learning](https://azure.microsoft.com/free/) today.

- Install and configure the [Azure Machine Learning CLI (v2) extension](how-to-configure-cli.md) or the [Azure Machine Learning Python SDK (v2)](https://aka.ms/sdk-v2-install).

- An Azure Resource group, in which you (or the service principal you use) need to have `User Access Administrator` and  `Contributor` access. You'll have such a resource group if you configured your Azure Machine Learning extension as stated previously.

- An Azure Machine Learning workspace. You'll have a workspace if you configured your Azure Machine Learning extension as stated previously.

- Any trained machine learning model ready for scoring and deployment.

## Choose a secret store

You can choose to store your secrets (such as API keys) using either:

- __Workspace connections under the workspace__: If you use this kind of secret store, you can later grant permission to the endpoint identity (at endpoint creation time) to read secrets from workspace connections automatically, provided certain conditions are met. For more information, see the system-assigned identity tab from the [Create an endpoint](#create-an-endpoint) section.
- __Key vaults__ that aren't necessarily under the workspace: If you use this kind of secret store, the endpoint identity won't be granted permission to read secrets from the key vaults automatically. Therefore, if you want to use a managed key vault service such as Microsoft Azure Key Vault as a secret store, you must assign a proper role later.

#### Use workspace connection as a secret store

You can create workspace connections to use in your deployment. For example, you can create a connection to Microsoft Azure OpenAI Service by using [Workspace Connections - Create REST API](/rest/api/azureml/2023-08-01-preview/workspace-connections/create).

Alternatively, you can create a custom connection by using Azure Machine Learning studio (see [How to create a custom connection for prompt flow](./prompt-flow/tools-reference/python-tool.md#create-a-custom-connection)) or Azure AI Foundry (see [How to create a custom connection in Azure AI Foundry portal](/azure/ai-studio/how-to/connections-add?tabs=custom#create-a-new-connection)).

1. Create an Azure OpenAI connection:

    ```REST
    PUT https://management.azure.com/subscriptions/{{subscriptionId}}/resourceGroups/{{resourceGroupName}}/providers/Microsoft.MachineLearningServices/workspaces/{{workspaceName}}/connections/{{connectionName}}?api-version=2023-08-01-preview
    Authorization: Bearer {{token}}
    Content-Type: application/json
    
    {
        "properties": {
            "authType": "ApiKey",
            "category": "AzureOpenAI",
            "credentials": {
                "key": "<key>",
                "endpoint": "https://<name>.openai.azure.com/",
            },
            "expiryTime": null,
            "target": "https://<name>.openai.azure.com/",
            "isSharedToAll": false,
            "sharedUserList": [],
            "metadata": {
                "ApiType": "Azure"
            }
        }
    }
    ```

1. Alternatively, you can create a custom connection:

    ```REST
    PUT https://management.azure.com/subscriptions/{{subscriptionId}}/resourceGroups/{{resourceGroupName}}/providers/Microsoft.MachineLearningServices/workspaces/{{workspaceName}}/connections/{{connectionName}}?api-version=2023-08-01-preview
    Authorization: Bearer {{token}}
    Content-Type: application/json
    
    {
        "properties": {
            "authType": "CustomKeys",
            "category": "CustomKeys",
            "credentials": {
                "keys": {
                    "OPENAI_API_KEY": "<key>",
                    "SPEECH_API_KEY": "<key>"
                }
            },
            "expiryTime": null,
            "target": "_",
            "isSharedToAll": false,
            "sharedUserList": [],
            "metadata": {
                "OPENAI_API_BASE": "<oai endpoint>",
                "OPENAI_API_VERSION": "<oai version>",
                "OPENAI_API_TYPE": "azure",
                "SPEECH_REGION": "eastus",
            }
        }
    }
    ```

1. Verify that the user identity can read the secrets from the workspace connection, by using [Workspace Connections - List Secrets REST API (preview)](/rest/api/azureml/2023-08-01-preview/workspace-connections/list-secrets).

    ```REST
    POST https://management.azure.com/subscriptions/{{subscriptionId}}/resourceGroups/{{resourceGroupName}}/providers/Microsoft.MachineLearningServices/workspaces/{{workspaceName}}/connections/{{connectionName}}/listsecrets?api-version=2023-08-01-preview
    Authorization: Bearer {{token}}
    ```

> [!NOTE]
> The previous code snippets use a token in the `Authorization` header when making REST API calls. You can get the token by running `az account get-access-token`. For more information on getting a token, see [Get an access token](how-to-authenticate-online-endpoint.md#get-the-microsoft-entra-token-for-control-plane-operations).

#### (Optional) Use Azure Key Vault as a secret store

Create the key vault and set a secret to use in your deployment. For more information on creating the key vault, see [Set and retrieve a secret from Azure Key Vault using Azure CLI](/azure/key-vault/secrets/quick-create-cli). Also,
- [az keyvault CLI](/cli/azure/keyvault#az-keyvault-create) and [Set Secret REST API](/rest/api/keyvault/secrets/set-secret/set-secret) show how to set a secret.
- [az keyvault secret show CLI](/cli/azure/keyvault/secret#az-keyvault-secret-show) and [Get Secret Versions REST API](/rest/api/keyvault/secrets/get-secret-versions/get-secret-versions) show how to retrieve a secret version.

1. Create an Azure Key Vault:

    ```azurecli
    az keyvault create --name mykeyvault --resource-group myrg --location eastus
    ```

1. Create a secret:

    ```azurecli
    az keyvault secret set --vault-name mykeyvault --name secret1 --value <value>
    ```

    This command returns the secret version it creates. You can check the `id` property of the response to get the secret version. The returned response looks like `https://mykeyvault.vault.azure.net/secrets/<secret_name>/<secret_version>`.

1. Verify that the user identity can read the secret from the key vault:

    ```azurecli
    az keyvault secret show --vault-name mykeyvault --name secret1 --version <secret_version>
    ```

> [!IMPORTANT]
> If you use the key vault as a secret store for secret injection, you must configure the key vault's permission model as Azure role-based access control (RBAC). For more information, see [Azure RBAC vs. access policy for Key Vault](/azure/key-vault/general/rbac-access-policy).

## Choose a user identity

Choose the user identity that you'll use to create the online endpoint and online deployment. This user identity can be a user account, a service principal account, or a managed identity in Microsoft Entra ID. To set up the user identity, follow the steps in [Set up authentication for Azure Machine Learning resources and workflows](how-to-setup-authentication.md).

#### (Optional) Assign a role to the user identity

- If your user identity wants the endpoint's system-assigned identity (SAI) to be automatically granted permission to read secrets from workspace connections, the user identity __must__ have the `Azure Machine Learning Workspace Connection Secrets Reader` role (or higher) on the scope of the workspace.
    - An admin that has the `Microsoft.Authorization/roleAssignments/write` permission can run a CLI command to assign the role to the _user identity_:

        ```azurecli
        az role assignment create --assignee <UserIdentityID> --role "Azure Machine Learning Workspace Connection Secrets Reader" --scope /subscriptions/<subscriptionId>/resourcegroups/<resourceGroupName>/providers/Microsoft.MachineLearningServices/workspaces/<workspaceName>
        ```

    > [!NOTE]
    > The endpoint's system-assigned identity (SAI) won't be automatically granted permission for reading secrets from key vaults. Hence, the user identity doesn't need to be assigned a role for the Key Vault.

- If you want to use a user-assigned identity (UAI) for the endpoint, you __don't need__ to assign the role to your user identity. Instead, if you intend to use the secret injection feature, you must assign the role to the endpoint's UAI manually.
    - An admin that has the `Microsoft.Authorization/roleAssignments/write` permission can run the following commands to assign the role to the _endpoint identity_:

        __For workspace connections__:

        ```azurecli
        az role assignment create --assignee <EndpointIdentityID> --role "Azure Machine Learning Workspace Connection Secrets Reader" --scope /subscriptions/<subscriptionId>/resourcegroups/<resourceGroupName>/providers/Microsoft.MachineLearningServices/workspaces/<workspaceName>
        ```
    
        __For key vaults__:
    
        ```azurecli
        az role assignment create --assignee <EndpointIdentityID> --role "Key Vault Secrets User" --scope /subscriptions/<subscriptionId>/resourcegroups/<resourceGroupName>/providers/Microsoft.KeyVault/vaults/<vaultName>
        ```

- Verify that an identity (either a user identity or endpoint identity) has the role assigned, by going to the resource in the Azure portal. For example, in the Azure Machine Learning workspace or the Key Vault:
    1. Select the __Access control (IAM)__ tab.
    1. Select the __Check access__ button and find the identity.
    1. Verify that the right role shows up under the __Current role assignments__ tab.

## Create an endpoint

### [System-assigned identity](#tab/sai)

If you're using a system-assigned identity (SAI) as the endpoint identity, specify whether you want to enforce access to default secret stores (namely, workspace connections under the workspace) to the endpoint identity.

1. Create an `endpoint.yaml` file:

    ```YAML
    $schema: https://azuremlschemas.azureedge.net/latest/managedOnlineEndpoint.schema.json
    name: my-endpoint
    auth_mode: key
    properties:
        enforce_access_to_default_secret_stores: enabled  # default: disabled
    ```

1. Create the endpoint, using the `endpoint.yaml` file:

    ```azurecli
    az ml online-endpoint create -f endpoint.yaml
    ```

If you don't specify the `identity` property in the endpoint definition, the endpoint will use an SAI by default.

If the following conditions are met, the endpoint identity will automatically be granted the `Azure Machine Learning Workspace Connection Secrets Reader` role (or higher) on the scope of the workspace:
  
- The user identity that creates the endpoint has the permission to read secrets from workspace connections (`Microsoft.MachineLearningServices/workspaces/connections/listsecrets/action`).
- The endpoint uses an SAI.
- The endpoint is defined with a flag to enforce access to default secret stores (workspace connections under the current workspace) when creating the endpoint.

The endpoint identity won't automatically be granted a role to read secrets from the Key Vault. If you want to use the Key Vault as a secret store, you need to manually assign a proper role such as `Key Vault Secrets User` to the _endpoint identity_ on the scope of the Key Vault. For more information on roles, see [Azure built-in roles for Key Vault data plane operations](/azure/key-vault/general/rbac-guide#azure-built-in-roles-for-key-vault-data-plane-operations).

### [User-assigned identity](#tab/uai)

If you're using a user-assigned identity (UAI) as the endpoint identity, you're not allowed to specify the `enforce_access_to_default_secret_stores` flag.

1. Create an `endpoint.yaml` file:

    ```YAML
    $schema: https://azuremlschemas.azureedge.net/latest/managedOnlineEndpoint.schema.json
    name: my-endpoint
    auth_mode: key
    identity:
        type: user_assigned
        user_assigned_identities: /subscriptions/00000000-0000-0000-000-000000000000/resourcegroups/myrg/providers/Microsoft.ManagedIdentity/userAssignedIdentities/my-identity 
    ```

1. Create the endpoint, using the `endpoint.yaml` file:

    ```azurecli
    az ml online-endpoint create -f endpoint.yaml
    ```

When using a UAI, you must manually assign any required roles to the endpoint identity as described in the optional section [Assign role to the user identity](#optional-assign-a-role-to-the-user-identity).

---

## Create a deployment

1. Author a scoring script or Dockerfile and the related scripts so that the deployment can consume the secrets via environment variables.
    
    - There's no need for you to call the secret retrieval APIs for the workspace connections or key vaults. The environment variables are populated with the secrets when the user container in the deployment initiates.

    - The value that gets injected into an environment variable can be one of the three types:
        - The whole [List Secrets API (preview)](/rest/api/azureml/workspace-connections/list-secrets) response. You'll need to understand the API response structure, parse it, and use it in your user container.
        - Individual secret or metadata from the workspace connection. You can use it without understanding the workspace connection API response structure.
        - Individual secret version from the Key Vault. You can use it without understanding the Key Vault API response structure.

1. Initiate the creation of the deployment, using either the scoring script (if you use a custom model) or a Dockerfile (if you take the BYOC approach to deployment). Specify environment variables the user expects within the user container.

    If the values that are mapped to the environment variables follow certain patterns, the endpoint identity will be used to perform secret retrieval and injection.

    | Pattern | Behavior |
    | -- | -- |
    | `${{azureml://connections/<connection_name>}}` | The whole [List Secrets API (preview)](/rest/api/azureml/workspace-connections/list-secrets) response is injected into the environment variable. |
    | `${{azureml://connections/<connection_name>/credentials/<credential_name>}}` | The value of the credential is injected into the environment variable. |
    | `${{azureml://connections/<connection_name>/metadata/<metadata_name>}}` | The value of the metadata is injected into the environment variable. |
    | `${{azureml://connections/<connection_name>/target}}` | The value of the target (where applicable) is injected into the environment variable. |
    | `${{keyvault:https://<keyvault_name>.vault.azure.net/secrets/<secret_name>/<secret_version>}}` | The value of the secret version is injected into the environment variable. |

    For example:

    1. Create `deployment.yaml`:

        ```YAML
        $schema: https://azuremlschemas.azureedge.net/latest/managedOnlineDeployment.schema.json
        name: blue
        endpoint_name: my-endpoint
        #…
        environment_variables:
            AOAI_CONNECTION: ${{azureml://connections/aoai_connection}}
            LANGCHAIN_CONNECTION: ${{azureml://connections/multi_connection_langchain}}
            
            OPENAI_KEY: ${{azureml://connections/multi_connection_langchain/credentials/OPENAI_API_KEY}}
            OPENAI_VERSION: ${{azureml://connections/multi_connection_langchain/metadata/OPENAI_API_VERSION}}
            
            USER_SECRET_KV1_KEY: ${{keyvault:https://mykeyvault.vault.azure.net/secrets/secret1/secretversion1}}
        ```

    1. Create the deployment:

        ```azurecli
        az ml online-deployment create -f deployment.yaml
        ```


If the `enforce_access_to_default_secret_stores` flag was set for the endpoint, the user identity's permission to read secrets from workspace connections will be checked both at endpoint creation and deployment creation time. If the user identity doesn't have the permission, the creation will fail.

At deployment creation time, if any environment variable is mapped to a value that follows the patterns in the previous table, secret retrieval and injection will be performed with the endpoint identity (either an SAI or a UAI). If the endpoint identity doesn't have the permission to read secrets from designated secret stores (either workspace connections or key vaults), the deployment creation will fail. Also, if the specified secret reference doesn't exist in the secret stores, the deployment creation will fail.

For more information on errors that can occur during deployment of Azure Machine Learning online endpoints, see [Secret Injection Errors](how-to-troubleshoot-online-endpoints.md#error-secretsinjectionerror).


## Consume the secrets

You can consume the secrets by retrieving them from the environment variables within the user container running in your deployments.


## Related content

- [Secret injection in online endpoints (preview)](concept-secret-injection.md)
- [How to authenticate clients for online endpoint](how-to-authenticate-online-endpoint.md)
- [Deploy and score a model using an online endpoint](how-to-deploy-online-endpoints.md)
- [Use a custom container to deploy a model using an online endpoint](how-to-deploy-custom-container.md)
