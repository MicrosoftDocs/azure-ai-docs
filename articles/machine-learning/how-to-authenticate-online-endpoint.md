---
title: Authenticate Clients for Online Endpoints
titleSuffix: Azure Machine Learning
description: Learn to authenticate clients for an Azure Machine Learning online endpoint.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: inferencing
author: s-polly
ms.author: scottpolly
ms.reviewer: jturuk
ms.date: 01/05/2026
ms.topic: how-to
ms.custom: how-to, devplatv2, cliv2, sdkv2, devx-track-azurecli, build-2024, dev-focus
ai-usage: ai-assisted
---

# Authenticate clients for online endpoints

[!INCLUDE [dev v2](includes/machine-learning-dev-v2.md)]

This article describes how to authenticate clients to perform control plane and data plane operations on online endpoints.

A _control plane operation_ controls an endpoint and changes it. Control plane operations include create, read, update, and delete (CRUD) operations on online endpoints and online deployments.

A _data plane operation_ uses data to interact with an online endpoint without changing the endpoint. For example, a data plane operation could consist of sending a scoring request to an online endpoint and getting a response.


## Prerequisites

[!INCLUDE [cli & sdk v2](includes/machine-learning-cli-sdk-v2-prereqs.md)]

- A user identity in Microsoft Entra ID. For information about creating a user identity, see [Set up authentication](how-to-setup-authentication.md#microsoft-entra-id). You'll need the identity ID later.
- **Required RBAC role for control plane and data plane operations**: Assign one of the following roles to your user identity at the workspace scope:
  - **AzureML Data Scientist** (built-in) — Includes permissions for CRUD operations on endpoints and scoring. See [AzureML Data Scientist role](/azure/role-based-access-control/built-in-roles#azureml-data-scientist).
  - **Owner** or **Contributor** — Full access to manage endpoints.
  - A custom role with `Microsoft.MachineLearningServices/workspaces/onlineEndpoints/*` actions.
- (Optional) **Azure Machine Learning Workspace Connection Secrets Reader** — Required only if you need to access secrets from workspace connections.

## Verify your setup

Run this snippet to verify that your credentials and RBAC permissions are correctly configured:

### [Azure CLI](#tab/azure-cli)

```azurecli
az login
az ml online-endpoint list --resource-group <RESOURCE_GROUP> --workspace-name <WORKSPACE_NAME>
```

Expected output: JSON array of endpoints (empty `[]` if no endpoints exist yet).

Reference: [az ml online-endpoint list](/cli/azure/ml/online-endpoint#az-ml-online-endpoint-list)

### [Python](#tab/python)

```python
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential

subscription_id = "<SUBSCRIPTION_ID>"
resource_group = "<RESOURCE_GROUP>"
workspace = "<WORKSPACE_NAME>"

ml_client = MLClient(
    DefaultAzureCredential(), subscription_id, resource_group, workspace
)

# List existing endpoints to verify access
endpoints = ml_client.online_endpoints.list()
print("Existing endpoints:", [ep.name for ep in endpoints])
```

Expected output: A list of endpoint names (empty list `[]` if no endpoints exist yet).

Reference: [MLClient](/python/api/azure-ai-ml/azure.ai.ml.mlclient), [DefaultAzureCredential](/python/api/azure-identity/azure.identity.defaultazurecredential)

### [REST](#tab/rest)

```bash
# First, get a token
export CONTROL_PLANE_TOKEN=$(az account get-access-token \
    --resource https://management.azure.com \
    --query accessToken -o tsv)

# List endpoints
curl -s -X GET \
    "https://management.azure.com/subscriptions/<SUBSCRIPTION_ID>/resourceGroups/<RESOURCE_GROUP>/providers/Microsoft.MachineLearningServices/workspaces/<WORKSPACE_NAME>/onlineEndpoints?api-version=2024-04-01" \
    -H "Authorization: Bearer $CONTROL_PLANE_TOKEN" \
    -H "Content-Type: application/json"
```

Expected output: JSON response with a `value` array containing endpoints.

### [Studio](#tab/studio)

Sign in to [Azure Machine Learning studio](https://ml.azure.com) and navigate to **Endpoints** > **Real-time endpoints** to verify access.

---

## Assign permissions to the identity

If you already have the required RBAC role assigned (as listed in [Prerequisites](#prerequisites)), skip to [Create an endpoint](#create-an-endpoint). This section provides details for custom role creation if needed.

<details>
<summary><strong>View built-in role details</strong></summary>

The `AzureML Data Scientist` [built-in role](/azure/role-based-access-control/built-in-roles#azureml-data-scientist) includes these control plane RBAC actions:
- `Microsoft.MachineLearningServices/workspaces/onlineEndpoints/write`
- `Microsoft.MachineLearningServices/workspaces/onlineEndpoints/delete`
- `Microsoft.MachineLearningServices/workspaces/onlineEndpoints/read`
- `Microsoft.MachineLearningServices/workspaces/onlineEndpoints/token/action`
- `Microsoft.MachineLearningServices/workspaces/onlineEndpoints/listKeys/action`
- `Microsoft.MachineLearningServices/workspaces/onlineEndpoints/regenerateKeys/action`

And this data plane RBAC action:
- `Microsoft.MachineLearningServices/workspaces/onlineEndpoints/score/action`

The `Azure Machine Learning Workspace Connection Secrets Reader` built-in role includes:
- `Microsoft.MachineLearningServices/workspaces/connections/listsecrets/action`
- `Microsoft.MachineLearningServices/workspaces/metadata/secrets/read`

</details>

### (Optional) Create a custom role

You can skip this step if you're using built-in roles or other pre-made custom roles.

1. Define the scope and actions for custom roles by creating JSON definitions of the roles. For example, the following role definition,  _custom-role-for-control-plane.json_, allows the user to perform CRUD operations on an online endpoint in a specified workspace.


    
    ```json
    {
        "Name": "Custom role for control plane operations - online endpoint",
        "IsCustom": true,
        "Description": "Can CRUD against online endpoints.",
        "Actions": [
            "Microsoft.MachineLearningServices/workspaces/onlineEndpoints/write",
            "Microsoft.MachineLearningServices/workspaces/onlineEndpoints/delete",
            "Microsoft.MachineLearningServices/workspaces/onlineEndpoints/read",
            "Microsoft.MachineLearningServices/workspaces/onlineEndpoints/token/action",
            "Microsoft.MachineLearningServices/workspaces/onlineEndpoints/listKeys/action",
            "Microsoft.MachineLearningServices/workspaces/onlineEndpoints/regenerateKeys/action"
        ],
        "NotActions": [
        ],
        "AssignableScopes": [
            "/subscriptions/<subscriptionID>/resourcegroups/<resourceGroupName>"
        ]
    }
    ```
    
    The following role definition, _custom-role-for-scoring.json_, allows the user to send scoring requests to an online endpoint in a specified workspace.
    
    
    ```json
    {
        "Name": "Custom role for scoring - online endpoint",
        "IsCustom": true,
        "Description": "Can score against online endpoints.",
        "Actions": [
            "Microsoft.MachineLearningServices/workspaces/onlineEndpoints/*/action"
        ],
        "NotActions": [
        ],
        "AssignableScopes": [
            "/subscriptions/<subscriptionID>/resourcegroups/<resourceGroupName>"
        ]
    }
    ```

1. Use the JSON definitions to create custom roles:

    ```bash
    az role definition create --role-definition custom-role-for-control-plane.json --subscription <subscriptionID>
    
    az role definition create --role-definition custom-role-for-scoring.json --subscription <subscriptionID>
    ```

    > [!NOTE]
    > To create custom roles, you need one of three roles: 
    >
    > - Owner
    > - User Access Administrator
    > - A custom role with `Microsoft.Authorization/roleDefinitions/write` permission (to create/update/delete custom roles) and `Microsoft.Authorization/roleDefinitions/read` permission (to view custom roles).
    >
    > For more information on creating custom roles, see [Azure custom roles](/azure/role-based-access-control/custom-roles#who-can-create-delete-update-or-view-a-custom-role).
    
1. Verify the role definition:

    ```bash
    az role definition list --custom-role-only -o table
    
    az role definition list -n "Custom role for control plane operations - online endpoint"
    az role definition list -n "Custom role for scoring - online endpoint"
    
    export role_definition_id1=`(az role definition list -n "Custom role for control plane operations - online endpoint" --query "[0].id" | tr -d '"')`
    
    export role_definition_id2=`(az role definition list -n "Custom role for scoring - online endpoint" --query "[0].id" | tr -d '"')`
    ```

### Assign the role to the identity

1. If you're using the `AzureML Data Scientist` built-in role, use the following code to assign the role to your user identity.

    ```bash
    az role assignment create --assignee <identityID> --role "AzureML Data Scientist" --scope /subscriptions/<subscriptionID>/resourcegroups/<resourceGroupName>/providers/Microsoft.MachineLearningServices/workspaces/<workspaceName>
    ```

1. Optionally, if you're using the `Azure Machine Learning Workspace Connection Secrets Reader` built-in role, use the following code to assign the role to your user identity.

    ```bash
    az role assignment create --assignee <identityID> --role "Azure Machine Learning Workspace Connection Secrets Reader" --scope /subscriptions/<subscriptionID>/resourcegroups/<resourceGroupName>/providers/Microsoft.MachineLearningServices/workspaces/<workspaceName>
    ```

1. If you're using a custom role, use the following code to assign the role to your user identity.

    ```bash
    az role assignment create --assignee <identityID> --role "Custom role for control plane operations - online endpoint" --scope /subscriptions/<subscriptionID>/resourcegroups/<resourceGroupName>/providers/Microsoft.MachineLearningServices/workspaces/<workspaceName>
    
    az role assignment create --assignee <identityID> --role "Custom role for scoring - online endpoint" --scope /subscriptions/<subscriptionID>/resourcegroups/<resourceGroupName>/providers/Microsoft.MachineLearningServices/workspaces/<workspaceName>
    ```

    > [!NOTE]
    > To assign custom roles to the user identity, you need one of three roles: 
    >
    > - Owner
    > - User Access Administrator
    > - A custom role that allows `Microsoft.Authorization/roleAssignments/write` permission (to assign custom roles) and `Microsoft.Authorization/roleAssignments/read` (to view role assignments).
    >
    > For more information on Azure roles and their permissions, see [Azure roles](/azure/role-based-access-control/rbac-and-directory-admin-roles#azure-roles) and [Assign Azure roles using the Azure portal](/azure/role-based-access-control/role-assignments-portal).

1. Confirm the role assignment:

    ```bash
    az role assignment list --scope /subscriptions/<subscriptionID>/resourcegroups/<resourceGroupName>/providers/Microsoft.MachineLearningServices/workspaces/<workspaceName>
    ```


## Get the Microsoft Entra token for control plane operations

Complete this step if you plan to perform control plane operations by using the REST API, which directly uses the token. 

If you plan to use other methods, like Azure CLI with the ml extension v2, Python SDK v2, or Azure Machine Learning studio, you don't need to get the Microsoft Entra token manually. Your user identity will authenticate during sign in, and the token will automatically be retrieved and passed for you.

You can retrieve the Microsoft Entra token for control plane operations from the Azure resource endpoint: `https://management.azure.com`.

### [Azure CLI](#tab/azure-cli)

1. Sign in to Azure.

    ```azurecli
    az login
    ```

1. If you want to use a specific identity, use the following code to sign in with the identity:

    ```azurecli
    az login --identity --username <identityID>
    ```

1. Use this context to get the token:

    ```bash
    export CONTROL_PLANE_TOKEN=$(az account get-access-token \
        --resource https://management.azure.com \
        --query accessToken -o tsv)
    ```

Reference: [az login](/cli/azure/reference-index#az-login), [az account get-access-token](/cli/azure/account#az-account-get-access-token)

### [Python](#tab/python)

```python
from azure.identity import DefaultAzureCredential, InteractiveBrowserCredential

try:
    credential = DefaultAzureCredential()
    # Check whether given credential can get token.
    access_token = credential.get_token("https://management.azure.com/.default")
    print(access_token)
except Exception as ex:
    # Fall back to InteractiveBrowserCredential in case DefaultAzureCredential doesn't work.
    # This will open a browser page. 
    credential = InteractiveBrowserCredential()
```

Reference: [DefaultAzureCredential](/python/api/azure-identity/azure.identity.defaultazurecredential), [InteractiveBrowserCredential](/python/api/azure-identity/azure.identity.interactivebrowsercredential)

For more information, see [Get a token using the Azure Identity client library](/entra/identity/managed-identities-azure-resources/how-to-use-vm-token#get-a-token-using-the-azure-identity-client-library).

### [REST](#tab/rest)

__From an Azure virtual machine__

You can get the token based on the managed identity for an Azure VM (when the VM enables a managed identity). 

- To get the Microsoft Entra token (`aad_token`) for the control plane operation on the Azure VM, submit the request to the [Azure Instance Metadata Service](/azure/virtual-machines/instance-metadata-service) (IMDS) endpoint for the Azure resource endpoint `management.azure.com`:

    ```bash
    export CONTROL_PLANE_TOKEN=$(curl -s \
        'http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https%3A%2F%2Fmanagement.azure.com%2F' \
        -H Metadata:true | jq -r '.access_token')
    ```
    
    > [!TIP]
    > The `jq` utility is used to extract the token from the JSON output. However, you can use any suitable tool for this purpose.
    
    For more information on getting tokens based on managed identities, see [Get a token using HTTP](/entra/identity/managed-identities-azure-resources/how-to-use-vm-token#get-a-token-using-http).

__From a compute instance__

You can get the token if you're using the Azure Machine Learning workspace's compute instance. To get the token, you must pass the client ID and the secret of the compute instance's managed identity to the Managed System Identity (MSI) endpoint that's configured locally at the compute instance. You can get the MSI endpoint, client ID, and secret from the environment variables `MSI_ENDPOINT`, `DEFAULT_IDENTITY_CLIENT_ID`, and `MSI_SECRET`, respectively. These variables are set automatically if you enable managed identity for the compute instance. 

- Get the token for the Azure resource endpoint `management.azure.com` from the workspace's compute instance:

    ```bash
    export CONTROL_PLANE_TOKEN=$(curl -s \
        "${MSI_ENDPOINT}?api-version=2018-02-01&resource=https%3A%2F%2Fmanagement.azure.com%2F&clientid=${DEFAULT_IDENTITY_CLIENT_ID}" \
        -H Metadata:true \
        -H "Secret:$MSI_SECRET" | jq -r '.access_token')
    ```

### [Studio](#tab/studio)

The studio doesn't expose the Microsoft Entra token for control plane operations.

---

### (Optional) Verify the resource endpoint and client ID for the Microsoft Entra token

After you retrieve the Microsoft Entra token, you can verify that the token is for the right Azure resource endpoint (`management.azure.com`) and the right client ID by decoding the token via [jwt.ms](https://jwt.ms/), which returns a JSON response containing the following information:

```json
{
    "aud": "https://management.azure.com",
    "oid": "<your-object-id>"
}
```


## Create an endpoint

The following example creates the endpoint with a system-assigned identity as the endpoint identity. The system-assigned identity is the default identity type of the managed identity for endpoints. Some basic roles are automatically assigned for the system-assigned identity. For more information on role assignment for a system-assigned identity, see [Automatic role assignment for endpoint identity](concept-endpoints-online-auth.md#automatic-role-assignment-for-endpoint-identity).

### [Azure CLI](#tab/azure-cli)

The CLI doesn't require you to explicitly provide the control plane token. Instead, the CLI `az login` command authenticates you during sign in, and the token is automatically retrieved and passed for you.

1. Create an endpoint definition YAML file named _endpoint.yml_:
    
    ```yaml
    $schema: https://azuremlschemas.azureedge.net/latest/managedOnlineEndpoint.schema.json
    name: my-endpoint
    auth_mode: aad_token
    ```

   You can set `auth_mode` to `key` for key authentication or `aml_token` for Azure Machine Learning token authentication. This example uses `aad_token` for Microsoft Entra token authentication.

1. Create the endpoint: 

    ```azurecli
    az ml online-endpoint create -f endpoint.yml
    ```

1. Check the endpoint's status:

    ```azurecli
    az ml online-endpoint show -n my-endpoint
    ```

1. If you want to override `auth_mode` (for example, to `aad_token`) when creating an endpoint, run the following code:

    ```azurecli
    az ml online-endpoint create -n my-endpoint --auth-mode aad_token
    ```

1. If you want to update the existing endpoint and specify `auth_mode` (for example, as `aad_token`), run the following code:

    ```azurecli
    az ml online-endpoint update -n my-endpoint --set auth_mode=aad_token
    ```

Reference: [az ml online-endpoint create](/cli/azure/ml/online-endpoint#az-ml-online-endpoint-create), [az ml online-endpoint show](/cli/azure/ml/online-endpoint#az-ml-online-endpoint-show), [az ml online-endpoint update](/cli/azure/ml/online-endpoint#az-ml-online-endpoint-update)

### [Python](#tab/python)

Python SDK doesn't require you to explicitly provide the control plane token. Rather, the SDK `MLClient` authenticates you during sign in, and the token is automatically retrieved and passed for you.

```python
from azure.ai.ml import MLClient
from azure.ai.ml.entities import (
    ManagedOnlineEndpoint,
    ManagedOnlineDeployment,
    Model,
    Environment,
    CodeConfiguration,
)
from azure.identity import DefaultAzureCredential

subscription_id = "<SUBSCRIPTION_ID>"
resource_group = "<RESOURCE_GROUP>"
workspace = "<WORKSPACE_NAME>"

ml_client = MLClient(
    DefaultAzureCredential(), subscription_id, resource_group, workspace
)

endpoint = ManagedOnlineEndpoint(
    name="my-endpoint",
    description="this is a sample online endpoint",
    auth_mode="aad_token",
    tags={"foo": "bar"},
)
ml_client.online_endpoints.begin_create_or_update(endpoint).result()
```

You can replace `auth_mode` with `key` for key authentication or with `aml_token` for Azure Machine Learning token authentication. The example uses `aad_token` for Microsoft Entra token authentication.

Reference: [MLClient](/python/api/azure-ai-ml/azure.ai.ml.mlclient), [ManagedOnlineEndpoint](/python/api/azure-ai-ml/azure.ai.ml.entities.managedonlineendpoint), [begin_create_or_update](/python/api/azure-ai-ml/azure.ai.ml.operations.onlineendpointoperations#azure-ai-ml-operations-onlineendpointoperations-begin-create-or-update)

### [REST](#tab/rest)

The REST API call requires you to explicitly provide the control plane token. Use the control plane token you retrieved earlier.

1. Create or update an endpoint:

    ```bash
    export SUBSCRIPTION_ID=<SUBSCRIPTION_ID>
    export RESOURCE_GROUP=<RESOURCE_GROUP>
    export WORKSPACE=<WORKSPACE_NAME>
    export ENDPOINT_NAME=<ENDPOINT_NAME>
    export LOCATION=<LOCATION_NAME>
    export API_VERSION=2024-04-01
    
    response=$(curl --location --request PUT \
        "https://management.azure.com/subscriptions/$SUBSCRIPTION_ID/resourceGroups/$RESOURCE_GROUP/providers/Microsoft.MachineLearningServices/workspaces/$WORKSPACE/onlineEndpoints/$ENDPOINT_NAME?api-version=$API_VERSION" \
        --header "Content-Type: application/json" \
        --header "Authorization: Bearer $CONTROL_PLANE_TOKEN" \
        --data-raw '{
            "identity": {
               "type": "systemAssigned"
            },
            "properties": {
                "authMode": "AADToken"
            },
            "location": "'"$LOCATION"'"
        }')
    
    echo $response
    ```

    You can replace `authMode` with `key` for key authentication or with `AMLToken` for Azure Machine Learning token authentication. In this example, you use `AADToken` for Microsoft Entra token authentication.

1. Get the current status of the online endpoint:

    ```bash
    response=$(curl --location --request GET \
        "https://management.azure.com/subscriptions/$SUBSCRIPTION_ID/resourceGroups/$RESOURCE_GROUP/providers/Microsoft.MachineLearningServices/workspaces/$WORKSPACE/onlineEndpoints/$ENDPOINT_NAME?api-version=$API_VERSION" \
        --header "Content-Type: application/json" \
        --header "Authorization: Bearer $CONTROL_PLANE_TOKEN")
    
    echo $response
    ```

Reference: [Online Endpoints - Create Or Update](/rest/api/azureml/online-endpoints/create-or-update), [Online Endpoints - Get](/rest/api/azureml/online-endpoints/get)

### [Studio](#tab/studio)

The studio doesn't require you to explicitly provide the control plane token because the studio authenticates you during sign in, and the token is automatically retrieved and passed for you.

For more information on deploying online endpoints, see [Deploy a machine learning model with an online endpoint (via the studio)](how-to-deploy-online-endpoints.md?tabs=azure-studio#deploy-to-azure).

---


## Create a deployment

To create a deployment, see [Deploy a machine learning model with an online endpoint](how-to-deploy-online-endpoints.md) or [Use REST to deploy a model as an online endpoint](how-to-deploy-with-rest.md). There's no difference in how you create deployments for different authentication modes. 

### [Azure CLI](#tab/azure-cli)

The following code is an example of how to create a deployment. For more information on deploying online endpoints, see [Deploy a machine learning model with an online endpoint (via CLI)](how-to-deploy-online-endpoints.md?tabs=azure-cli#deploy-to-azure).

1. Create a deployment definition YAML file named _blue-deployment.yml_:

    ```yaml
    $schema: https://azuremlschemas.azureedge.net/latest/managedOnlineDeployment.schema.json
    name: blue
    endpoint_name: my-aad-auth-endp1
    model:
      path: ../../model-1/model/
    code_configuration:
      code: ../../model-1/onlinescoring/
      scoring_script: score.py
    environment: 
      conda_file: ../../model-1/environment/conda.yml
      image: mcr.microsoft.com/azureml/openmpi4.1.0-ubuntu22.04:latest
    instance_type: Standard_DS3_v2
    instance_count: 1
    ```

1. Create the deployment by using the YAML file. For this example, set all traffic to the new deployment.

    ```azurecli
    az ml online-deployment create -f blue-deployment.yml --all-traffic
    ```

Reference: [az ml online-deployment create](/cli/azure/ml/online-deployment#az-ml-online-deployment-create)

### [Python](#tab/python)

For more information on deploying online endpoints, see [Deploy a machine learning model with an online endpoint (via SDK)](how-to-deploy-online-endpoints.md?tabs=python#deploy-to-azure).

### [REST](#tab/rest)

For more information on deploying online endpoints by using REST, see [Use REST to deploy a model as an online endpoint](how-to-deploy-with-rest.md).

### [Studio](#tab/studio)

For more information on deploying online endpoints, see [Deploy a machine learning model with an online endpoint (via the studio)](how-to-deploy-online-endpoints.md?tabs=azure-studio#deploy-to-azure).

---


## Get the scoring URI for the endpoint

### [Azure CLI](#tab/azure-cli)

If you use `az ml online-endpoint invoke` to call the endpoint, the CLI resolves the scoring URI automatically, so you don't need to retrieve it manually.

However, if you need the scoring URI for use with other tools (such as REST API or custom HTTP clients), you can retrieve it with the following command:

```azurecli
scoringUri=$(az ml online-endpoint show -n my-endpoint --query "scoring_uri")
```

Reference: [az ml online-endpoint show](/cli/azure/ml/online-endpoint#az-ml-online-endpoint-show)

### [Python](#tab/python)

If you plan to use the Python SDK to invoke the endpoint, you don't need to get the scoring URI explicitly because the SDK provides it for you. However, you can still use the SDK to get the scoring URI so that you can use it with other channels, such as the REST API.

```python
scoring_uri = ml_client.online_endpoints.get(name=endpoint_name).scoring_uri
```

Reference: [OnlineEndpointOperations.get](/python/api/azure-ai-ml/azure.ai.ml.operations.onlineendpointoperations#azure-ai-ml-operations-onlineendpointoperations-get)

### [REST](#tab/rest)

```bash
export SUBSCRIPTION_ID=<SUBSCRIPTION_ID>
export RESOURCE_GROUP=<RESOURCE_GROUP>
export WORKSPACE=<WORKSPACE_NAME>
export ENDPOINT_NAME=<ENDPOINT_NAME>
export API_VERSION=2024-04-01

response=$(curl --location --request GET \
    "https://management.azure.com/subscriptions/$SUBSCRIPTION_ID/resourceGroups/$RESOURCE_GROUP/providers/Microsoft.MachineLearningServices/workspaces/$WORKSPACE/onlineEndpoints/$ENDPOINT_NAME?api-version=$API_VERSION" \
    --header "Content-Type: application/json" \
    --header "Authorization: Bearer $CONTROL_PLANE_TOKEN")

scoringUri=$(echo $response | jq -r '.properties.scoringUri')

echo $response
echo $scoringUri
```

### [Studio](#tab/studio)

If you plan to use the studio to invoke the endpoint, you don't need to get the scoring URI explicitly because the studio provides it for you. However, you can still use the studio to get the scoring URI so that you can use it with other channels, such as the REST API.

You can find the scoring URI on the __Details__ tab of the endpoint's page.

---


## Get the key or token for data plane operations

You can use a key or token for data plane operations, even though the process of getting the key or token is a control plane operation. In other words, you use a control plane token to get the key or token that you later use to perform your data plane operations.

To get the key or Azure Machine Learning token, the user identity that's requesting it needs to have the correct role assigned to it, as described in [Authorization for control plane operations](concept-endpoints-online-auth.md#control-plane-operations).
The user identity doesn't need any extra roles to get the Microsoft Entra token.

### [Azure CLI](#tab/azure-cli)

If you plan to use the CLI to invoke the endpoint, you don't need to get the keys or token for data plane operations explicitly because the CLI provides it for you. However, you can still use the CLI to get the keys or token for data plane operations so that you can use it with other channels, such as the REST API.

To get the keys or token for data plane operations, use the [az ml online-endpoint get-credentials](/cli/azure/ml/online-endpoint#az-ml-online-endpoint-get-credentials) command. This command returns JSON output that contains the keys, token, and/or additional information.

> [!TIP]
> In the following command, the `--query` parameter is used to extract specific information from the JSON output. However, you can use any suitable tool for that purpose.

__When the `auth_mode` of the endpoint is `key`__

- Keys are returned in the `primaryKey` and `secondaryKey` fields.

   ```bash
   export DATA_PLANE_TOKEN=$(az ml online-endpoint get-credentials -n $ENDPOINT_NAME -g $RESOURCE_GROUP -w $WORKSPACE_NAME -o tsv --query primaryKey)
   export DATA_PLANE_TOKEN2=$(az ml online-endpoint get-credentials -n $ENDPOINT_NAME -g $RESOURCE_GROUP -w $WORKSPACE_NAME -o tsv --query secondaryKey)
   ```

__When the `auth_mode` of the endpoint is `aml_token`__

- The token is returned in the `accessToken` field.
- The token expiration time is returned in the `expiryTimeUtc` field.
- The token refresh time is returned in the `refreshAfterTimeUtc` field.

   ```bash
   export DATA_PLANE_TOKEN=$(az ml online-endpoint get-credentials -n $ENDPOINT_NAME -g $RESOURCE_GROUP -w $WORKSPACE_NAME -o tsv --query accessToken)
   export EXPIRY_TIME_UTC=$(az ml online-endpoint get-credentials -n $ENDPOINT_NAME -g $RESOURCE_GROUP -w $WORKSPACE_NAME -o tsv --query expiryTimeUtc)
   export REFRESH_AFTER_TIME_UTC=$(az ml online-endpoint get-credentials -n $ENDPOINT_NAME -g $RESOURCE_GROUP -w $WORKSPACE_NAME -o tsv --query refreshAfterTimeUtc)
   ```

__When the `auth_mode` of the endpoint is `aad_token`__

- The token is returned in the `accessToken` field.
- The token expiration time is returned in the `expiryTimeUtc` field.

   ```bash
   export DATA_PLANE_TOKEN=$(az ml online-endpoint get-credentials -n $ENDPOINT_NAME -g $RESOURCE_GROUP -w $WORKSPACE_NAME -o tsv --query accessToken)
   export EXPIRY_TIME_UTC=$(az ml online-endpoint get-credentials -n $ENDPOINT_NAME -g $RESOURCE_GROUP -w $WORKSPACE_NAME -o tsv --query expiryTimeUtc)
   ```

Reference: [az ml online-endpoint get-credentials](/cli/azure/ml/online-endpoint#az-ml-online-endpoint-get-credentials)

### [Python](#tab/python)

If you use the SDK's `invoke()` method to call the endpoint, the SDK handles authentication automatically, so you don't need to retrieve keys or tokens manually.

However, if you need to retrieve keys or tokens for use with other tools (such as REST API or custom HTTP clients), you can use the [get_keys](/python/api/azure-ai-ml/azure.ai.ml.operations.onlineendpointoperations#azure-ai-ml-operations-onlineendpointoperations-get-keys) method in the `OnlineEndpointOperations` class. This method returns an object that includes keys and token.

__When the `auth_mode` of the endpoint is `key`__

- Keys are returned in the `primary_key` and `secondary_key` fields.

   ```python
   DATA_PLANE_TOKEN = ml_client.online_endpoints.get_keys(name=endpoint_name).primary_key
   DATA_PLANE_TOKEN2 = ml_client.online_endpoints.get_keys(name=endpoint_name).secondary_key
   ```

__When the `auth_mode` of the endpoint is `aml_token`__

- The token is returned in the `access_token` field.
- The token expiration time is returned in the `expiry_time_utc` field.
- The token refresh time is returned in the `refresh_after_time_utc` field.

   ```python
   DATA_PLANE_TOKEN = ml_client.online_endpoints.get_keys(name=endpoint_name).access_token
   EXPIRY_TIME_UTC = ml_client.online_endpoints.get_keys(name=endpoint_name).expiry_time_utc
   REFRESH_AFTER_TIME_UTC = ml_client.online_endpoints.get_keys(name=endpoint_name).refresh_after_time_utc
   ```

__When the `auth_mode` of the endpoint is `aad_token`__

- The token is returned in the `access_token` field.
- The token expiration time is returned in the `expiry_time_utc` field.

   ```python
   DATA_PLANE_TOKEN = ml_client.online_endpoints.get_keys(name=endpoint_name).access_token
   EXPIRY_TIME_UTC = ml_client.online_endpoints.get_keys(name=endpoint_name).expiry_time_utc
   ```

Reference: [OnlineEndpointOperations.get_keys](/python/api/azure-ai-ml/azure.ai.ml.operations.onlineendpointoperations#azure-ai-ml-operations-onlineendpointoperations-get-keys)

For more information, see [Get a token using the Azure identity client library](/entra/identity/managed-identities-azure-resources/how-to-use-vm-token#get-a-token-using-the-azure-identity-client-library).

### [REST](#tab/rest)

To get the keys or token for data plane operations, choose the right API, depending on the `auth_mode` of the endpoint. The API returns JSON output that includes the keys and token.

> [!TIP]
> The `jq` utility is used to demonstrate how to extract specific information from the JSON output. However, you can use any suitable tool for that purpose.

__When the `auth_mode` of the endpoint is `key`__

- Use the `listkeys` API.
- Keys are returned in the `primaryKey` and `secondaryKey` fields.

   ```bash
   response=$(curl -H "Content-Length: 0" --location --request POST \
       "https://management.azure.com/subscriptions/$SUBSCRIPTION_ID/resourceGroups/$RESOURCE_GROUP/providers/Microsoft.MachineLearningServices/workspaces/$WORKSPACE/onlineEndpoints/$ENDPOINT_NAME/listkeys?api-version=$API_VERSION" \
       --header "Authorization: Bearer $CONTROL_PLANE_TOKEN")

   export DATA_PLANE_TOKEN=$(echo $response | jq -r '.primaryKey')
   ```

__When the `auth_mode` of the endpoint is `aml_token`__

- Use the `token` API.
- The token is returned in the `accessToken` field.
- The token expiration time is returned in the `expiryTimeUtc` field.
- The token refresh time is returned in the `refreshAfterTimeUtc` field.

   ```bash
   response=$(curl -H "Content-Length: 0" --location --request POST \
       "https://management.azure.com/subscriptions/$SUBSCRIPTION_ID/resourceGroups/$RESOURCE_GROUP/providers/Microsoft.MachineLearningServices/workspaces/$WORKSPACE/onlineEndpoints/$ENDPOINT_NAME/token?api-version=$API_VERSION" \
       --header "Authorization: Bearer $CONTROL_PLANE_TOKEN")

   export DATA_PLANE_TOKEN=$(echo $response | jq -r '.accessToken')
   export EXPIRY_TIME_UTC=$(echo $response | jq -r '.expiryTimeUtc')
   export REFRESH_AFTER_TIME_UTC=$(echo $response | jq -r '.refreshAfterTimeUtc')
   ```

__When the `auth_mode` of the endpoint is `aad_token`__

- Use the IMDS endpoint or MSI endpoint, depending on where you request the token.
- The token is returned in the `accessToken` field.
- The token expiration time is returned in the `expiryTimeUtc` field.

__From an Azure virtual machine__

You can get the token based on the managed identities for an Azure VM (when the VM enables a managed identity). 

- To get the Microsoft Entra token (`aad_token`) for the data plane operation on the Azure VM with managed identity, submit the request to the [IMDS](/azure/virtual-machines/instance-metadata-service)  endpoint for the Azure resource endpoint `ml.azure.com`:

    ```bash
    export DATA_PLANE_TOKEN=$(curl -s \
        'http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https%3A%2F%2Fml.azure.com%2F' \
        -H Metadata:true | jq -r '.access_token')
    export EXPIRY_TIME_UTC=$(curl -s \
        'http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https%3A%2F%2Fml.azure.com%2F' \
        -H Metadata:true | jq -r '.expiryTimeUtc')
    ```

    For more information on getting tokens based on managed identities, see [Get a token using HTTP](/entra/identity/managed-identities-azure-resources/how-to-use-vm-token#get-a-token-using-http).

__From a compute instance__

You can get the token if you're using the Azure Machine Learning workspace's compute instance. To get the token, you must pass the client ID and the secret of the compute instance's managed identity to the MSI endpoint that's configured locally at the compute instance. You can get the MSI endpoint, client ID, and secret from the environment variables `MSI_ENDPOINT`, `DEFAULT_IDENTITY_CLIENT_ID`, and `MSI_SECRET`, respectively. These variables are set automatically if you enable managed identity for the compute instance. 

- Get the token for the Azure resource endpoint `ml.azure.com` from the workspace's compute instance:

    ```bash
    export DATA_PLANE_TOKEN=$(curl -s \
        "${MSI_ENDPOINT}?api-version=2018-02-01&resource=https%3A%2F%2Fml.azure.com%2F&clientid=${DEFAULT_IDENTITY_CLIENT_ID}" \
        -H Metadata:true \
        -H "Secret:$MSI_SECRET" | jq -r '.access_token')
    export EXPIRY_TIME_UTC=$(curl -s \
        "${MSI_ENDPOINT}?api-version=2018-02-01&resource=https%3A%2F%2Fml.azure.com%2F&clientid=${DEFAULT_IDENTITY_CLIENT_ID}" \
        -H Metadata:true \
        -H "Secret:$MSI_SECRET" | jq -r '.expiryTimeUtc')
    ```

> [!IMPORTANT]
> Unlike the Microsoft Entra token for control plane operations, which is retrieved from `management.azure.com`, the Microsoft Entra token for data plane operations is retrieved from the Azure resource endpoint `ml.azure.com`.


### [Studio](#tab/studio)

You can find the key, Azure Machine Learning token, or Microsoft Entra token on the __Consume__ tab of a deployment's page.

---

### Verify the resource endpoint and client ID for the Microsoft Entra token

After getting the Entra token, you can verify that the token is for the right Azure resource endpoint, `ml.azure.com`, and the right client ID by decoding the token via [jwt.ms](https://jwt.ms/), which returns a JSON response with the following information:

```json
{
    "aud": "https://ml.azure.com",
    "oid": "<your-object-id>"
}
```


## Score data using the key or token

### [Azure CLI](#tab/azure-cli)

You can use `az ml online-endpoint invoke` for endpoints with a key, an Azure Machine Learning token, or a Microsoft Entra token. The CLI provides the key or token automatically so you don't need to pass it explicitly.

```azurecli
az ml online-endpoint invoke -n my-endpoint -r request.json
```

Reference: [az ml online-endpoint invoke](/cli/azure/ml/online-endpoint#az-ml-online-endpoint-invoke)

### [Python](#tab/python)

Azure Machine Learning SDK `ml_client.online_endpoints.invoke()` is supported for keys, Azure Machine Learning tokens, and Microsoft Entra tokens.
You can also use a generic Python SDK to send the POST request to the scoring URI.

When calling the online endpoint for scoring, pass the key or token in the authorization header. The following code shows how to call the online endpoint by using a key or token with a generic Python SDK. In the code, replace the `api_key` variable with your key or token.

```python
import urllib.request
import json
import os

data = {"data": [
    [1,2,3,4,5,6,7,8,9,10], 
    [10,9,8,7,6,5,4,3,2,1]
]}

body = str.encode(json.dumps(data))

url = '<scoring URI as retrieved earlier>'
api_key = '<key or token as retrieved earlier>'
headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

req = urllib.request.Request(url, body, headers)

try:
    response = urllib.request.urlopen(req)

    result = response.read()
    print(result)
except urllib.error.HTTPError as error:
    print("The request failed with status code: " + str(error.code))

    # Print the headers - useful for debugging
    print(error.info())
    print(error.read().decode("utf8", 'ignore'))
```

Alternatively, use the SDK's `invoke()` method:

```python
ml_client.online_endpoints.invoke(
    endpoint_name="my-endpoint",
    request_file="./sample-request.json"
)
```

Reference: [OnlineEndpointOperations.invoke](/python/api/azure-ai-ml/azure.ai.ml.operations.onlineendpointoperations#azure-ai-ml-operations-onlineendpointoperations-invoke)

### [REST](#tab/rest)

When invoking the online endpoint for scoring, pass the key, Azure Machine Learning token, or Microsoft Entra token in the authorization header. The following code shows how to use the cURL utility to call the online endpoint by using a key or token:

```bash
curl --request POST "$scoringUri" \
    --header "Authorization: Bearer $DATA_PLANE_TOKEN" \
    --header 'Content-Type: application/json' \
    --data @endpoints/online/model-1/sample-request.json
```

### [Studio](#tab/studio)

#### Key or Azure Machine Learning token

The __Test__ tab of the deployment's detail page supports scoring for endpoints with key, Azure Machine Learning token, or Microsoft Entra token authentication.

---


## Log and monitor traffic

To enable traffic logging in the diagnostics settings for the endpoint, complete the steps in [Turn on logs](how-to-monitor-online-endpoints.md#turn-on-logs).

If the diagnostic setting is enabled, you can view the `AmlOnlineEndpointTrafficLogs` table to see the authentication mode and user identity.


## Related content

* [Authentication and authorization for online endpoints](concept-endpoints-online-auth.md)
* [Deploy and score a machine learning model by using an online endpoint](how-to-deploy-online-endpoints.md)
* [Secure managed online endpoints by using network isolation](how-to-secure-online-endpoint.md)
