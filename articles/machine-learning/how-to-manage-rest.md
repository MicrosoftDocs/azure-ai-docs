---
title: Use REST to manage ML resources
titleSuffix: Azure Machine Learning
description: How to use REST APIs to create, run, and delete Azure Machine Learning resources, such as a workspace, or register models.
author: s-polly
ms.author: scottpolly
ms.reviewer: shshubhe
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: enterprise-readiness
ms.date: 03/23/2026
ms.topic: how-to
ms.custom: dev-focus
ai-usage: ai-assisted

---

# Create, run, and delete Azure Machine Learning resources by using REST



You can manage your Azure Machine Learning resources in several ways. Use the [Azure portal](https://portal.azure.com/), [Azure CLI](/cli/azure), or the [Python SDK](https://aka.ms/sdk-v2-install). Or, choose the REST API. The REST API uses HTTP verbs in a standard way to create, retrieve, update, and delete resources. The REST API works with any language or tool that can make HTTP requests. REST's straightforward structure often makes it a good choice in scripting environments and for MLOps automation. 

In this article, you learn how to:

> [!div class="checklist"]
> * Retrieve an authorization token
> * Create a properly formatted REST request by using service principal authentication
> * Use GET requests to retrieve information about Azure Machine Learning's hierarchical resources
> * Use GET requests to retrieve and manage jobs
> * Use PUT and POST requests to create and modify resources
> * Use PUT requests to create Azure Machine Learning workspaces
> * Use DELETE requests to clean up resources 

## Prerequisites

- An **Azure subscription** for which you have administrative rights. If you don't have such a subscription, try the [free or paid personal subscription](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- An [Azure Machine Learning workspace](quickstart-create-resources.md).
- Administrative REST requests use service principal authentication. Follow the steps in [Set up authentication for Azure Machine Learning resources and workflows](./how-to-setup-authentication.md#service-principal-authentication) to create a service principal in your workspace.
- The **curl** utility. The **curl** program is available in the [Windows Subsystem for Linux](/windows/wsl/install-win10) or any UNIX distribution. In PowerShell, **curl** is an alias for **Invoke-WebRequest**. The command `curl -d "key=val" -X POST uri` becomes `Invoke-WebRequest -Body "key=val" -Method POST -Uri uri`. 

## Retrieve a service principal authentication token

Administrative REST requests use OAuth 2.0 implicit flow for authentication. This authentication flow uses a token provided by your subscription's service principal. To retrieve this token, you need:

- Your tenant ID (identifies the organization to which your subscription belongs)
- Your client ID (associates with the created token)
- Your client secret (safeguard this value)

You get these values from the response to the creation of your service principal. For more information, see [Set up authentication for Azure Machine Learning resources and workflows](./how-to-setup-authentication.md#service-principal-authentication). If you're using your company subscription, you might not have permission to create a service principal. In that case, use either a [free or paid personal subscription](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

To retrieve a token:

1. Open a terminal window.
1. Enter the following code at the command line.
1. Substitute your own values for `<YOUR-TENANT-ID>`, `<YOUR-CLIENT-ID>`, and `<YOUR-CLIENT-SECRET>`. Throughout this article, strings surrounded by angle brackets are variables you replace with your own appropriate values.
1. Run the command.

```bash
curl -X POST https://login.microsoftonline.com/<YOUR-TENANT-ID>/oauth2/v2.0/token \
-d "grant_type=client_credentials&scope=https%3A%2F%2Fmanagement.azure.com%2F.default&client_id=<YOUR-CLIENT-ID>&client_secret=<YOUR-CLIENT-SECRET>" \
```

The response provides an access token that's valid for one hour:

```json
{
    "token_type": "Bearer",
    "expires_in": 3599,
    "ext_expires_in": 3599,
    "access_token": "YOUR-ACCESS-TOKEN"
}
```

Make note of the token, as you use it to authenticate all administrative requests. Set an `Authorization` header in all requests:

```bash
curl -H "Authorization:Bearer <YOUR-ACCESS-TOKEN>" ...more args...
```

> [!NOTE]
> The value starts with the string `Bearer ` including a single space before you add the token.

## Get a list of resource groups associated with your subscription

To retrieve the list of resource groups associated with your subscription, run:

```bash
curl https://management.azure.com/subscriptions/<YOUR-SUBSCRIPTION-ID>/resourceGroups?api-version=2022-04-01 -H "Authorization:Bearer <YOUR-ACCESS-TOKEN>"
```

Azure publishes many REST APIs. Each service provider updates its API on its own schedule, but it doesn't break existing programs. The service provider uses the `api-version` argument to ensure compatibility. 

> [!IMPORTANT]
> The `api-version` argument varies from service to service. For the Machine Learning Service, for instance, the current API version is `2025-09-01`. To find the latest API version for other Azure services, see the [Azure REST API reference](/rest/api/azure/) for the specific service.

Set the `api-version` argument to the expected value in all REST calls. You can rely on the syntax and semantics of the specified version even as the API continues to evolve. If you send a request to a provider without the `api-version` argument, the response contains a human-readable list of supported values. 

The preceding call returns a compacted JSON response of the form: 

```json
{
    "value": [
        {
            "id": "/subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/resourceGroups/RG1",
            "name": "RG1",
            "type": "Microsoft.Resources/resourceGroups",
            "location": "westus2",
            "properties": {
                "provisioningState": "Succeeded"
            }
        },
        {
            "id": "/subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/resourceGroups/RG2",
            "name": "RG2",
            "type": "Microsoft.Resources/resourceGroups",
            "location": "eastus",
            "properties": {
                "provisioningState": "Succeeded"
            }
        }
    ]
}
```


## Drill down into workspaces and their resources

To retrieve the set of workspaces in a resource group, run the following command, replacing `<YOUR-SUBSCRIPTION-ID>`, `<YOUR-RESOURCE-GROUP>`, and `<YOUR-ACCESS-TOKEN>`: 

```bash
curl https://management.azure.com/subscriptions/<YOUR-SUBSCRIPTION-ID>/resourceGroups/<YOUR-RESOURCE-GROUP>/providers/Microsoft.MachineLearningServices/workspaces/?api-version=2025-09-01 \
-H "Authorization:Bearer <YOUR-ACCESS-TOKEN>"
```

Again, you receive a JSON list containing details for each workspace.

```json
{
    "id": "/subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/resourceGroups/DeepLearningResourceGroup/providers/Microsoft.MachineLearningServices/workspaces/my-workspace",
    "name": "my-workspace",
    "type": "Microsoft.MachineLearningServices/workspaces",
    "location": "centralus",
    "tags": {},
    "etag": null,
    "properties": {
        "friendlyName": "",
        "description": "",
        "creationTime": "2023-01-03T19:56:09.7588299+00:00",
        "storageAccount": "/subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/resourcegroups/DeepLearningResourceGroup/providers/microsoft.storage/storageaccounts/myworkspace0275623111",
        "containerRegistry": null,
        "keyVault": "/subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/resourcegroups/DeepLearningResourceGroup/providers/microsoft.keyvault/vaults/myworkspace2525649324",
        "applicationInsights": "/subscriptions/aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e/resourcegroups/DeepLearningResourceGroup/providers/microsoft.insights/components/myworkspace2053523719",
        "hbiWorkspace": false,
        "workspaceId": "cba12345-abab-abab-abab-ababab123456",
        "subscriptionState": null,
        "subscriptionStatusChangeTimeStampUtc": null,
        "discoveryUrl": "https://centralus.experiments.azureml.net/discovery"
    },
    "identity": {
        "type": "SystemAssigned",
        "principalId": "abcdef1-abab-1234-1234-abababab123456",
        "tenantId": "1fedcba-abab-1234-1234-abababab123456"
    },
    "sku": {
        "name": "Basic",
        "tier": "Basic"
    }
}
```

To work with resources within a workspace, switch from the general **management.azure.com** server to a REST API server specific to the location of the workspace. Note the value of the `discoveryUrl` key in the preceding JSON response. If you GET that URL, you receive a response like:

```json
{
  "api": "https://centralus.api.azureml.ms",
  "experimentation": "https://centralus.experiments.azureml.net",
  "history": "https://centralus.experiments.azureml.net",
  "hyperdrive": "https://centralus.experiments.azureml.net",
  "labeling": "https://centralus.experiments.azureml.net",
  "modelmanagement": "https://centralus.modelmanagement.azureml.net",
  "pipelines": "https://centralus.aether.ms",
  "studiocoreservices": "https://centralus.studioservice.azureml.com"
}
```

The value of the `api` response is the URL of the server that you use for more requests. To list experiments, send the following command. Replace `REGIONAL-API-SERVER` with the value of the `api` response (for example, `centralus.api.azureml.ms`). Also replace `YOUR-SUBSCRIPTION-ID`, `YOUR-RESOURCE-GROUP`, `YOUR-WORKSPACE-NAME`, and `YOUR-ACCESS-TOKEN` as usual:

```bash
curl https://<REGIONAL-API-SERVER>/history/v1.0/subscriptions/<YOUR-SUBSCRIPTION-ID>/resourceGroups/<YOUR-RESOURCE-GROUP>/\
providers/Microsoft.MachineLearningServices/workspaces/<YOUR-WORKSPACE-NAME>/experiments?api-version=2025-09-01 \
-H "Authorization:Bearer <YOUR-ACCESS-TOKEN>"
```

Similarly, to retrieve registered models in your workspace, send:

```bash
curl https://<REGIONAL-API-SERVER>/modelmanagement/v1.0/subscriptions/<YOUR-SUBSCRIPTION-ID>/resourceGroups/<YOUR-RESOURCE-GROUP>/\
providers/Microsoft.MachineLearningServices/workspaces/<YOUR-WORKSPACE-NAME>/models?api-version=2025-09-01 \
-H "Authorization:Bearer <YOUR-ACCESS-TOKEN>"
```

## Retrieve and manage jobs

Jobs are a fundamental concept in Azure Machine Learning, representing training runs, batch inference, and other machine learning workloads. Use REST API calls to retrieve job information, monitor status, and manage the job lifecycle.

### Get a specific job by ID

To retrieve details about a specific job by using its ID, use the management API:

```bash
curl https://management.azure.com/subscriptions/<YOUR-SUBSCRIPTION-ID>/resourceGroups/<YOUR-RESOURCE-GROUP>/\
providers/Microsoft.MachineLearningServices/workspaces/<YOUR-WORKSPACE-NAME>/jobs/<JOB-ID>?api-version=2025-09-01 \
-H "Authorization:Bearer <YOUR-ACCESS-TOKEN>"
```

This command returns a JSON response with complete job details, including status, configuration, and results.

### List all jobs in a workspace

To list all jobs in your workspace:

```bash
curl https://management.azure.com/subscriptions/<YOUR-SUBSCRIPTION-ID>/resourceGroups/<YOUR-RESOURCE-GROUP>/\
providers/Microsoft.MachineLearningServices/workspaces/<YOUR-WORKSPACE-NAME>/jobs?api-version=2025-09-01 \
-H "Authorization:Bearer <YOUR-ACCESS-TOKEN>"
```

### Get job runs by using the regional API

You can also retrieve job information by using the regional API server. To list job runs:

```bash
curl https://<REGIONAL-API-SERVER>/history/v1.0/subscriptions/<YOUR-SUBSCRIPTION-ID>/resourceGroups/<YOUR-RESOURCE-GROUP>/\
providers/Microsoft.MachineLearningServices/workspaces/<YOUR-WORKSPACE-NAME>/runs?api-version=2025-09-01 \
-H "Authorization:Bearer <YOUR-ACCESS-TOKEN>"
```

To get details about a specific run:

```bash
curl https://<REGIONAL-API-SERVER>/history/v1.0/subscriptions/<YOUR-SUBSCRIPTION-ID>/resourceGroups/<YOUR-RESOURCE-GROUP>/\
providers/Microsoft.MachineLearningServices/workspaces/<YOUR-WORKSPACE-NAME>/runs/<RUN-ID>?api-version=2025-09-01 \
-H "Authorization:Bearer <YOUR-ACCESS-TOKEN>"
```

Notice that to list experiments the path begins with `history/v1.0` while to list models, the path begins with `modelmanagement/v1.0`. The REST API is divided into several operational groups, each with a distinct path. 

| Area | Path |
|-|-|
| Artifacts | /rest/api/azureml |
| Data stores | /azure/machine-learning/how-to-access-data |
| Hyperparameter tuning | hyperdrive/v1.0/ |
| Jobs | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.MachineLearningServices/workspaces/{workspaceName}/jobs |
| Models | modelmanagement/v1.0/ |
| Run history | execution/v1.0/ and history/v1.0/ |

You can explore the REST API by using the following general pattern:

| URL component | Example |
|-|-|
| `https://` |  |
| `REGIONAL-API-SERVER/` | `centralus.api.azureml.ms/` |
| `operations-path/` | `history/v1.0/` |
| `subscriptions/YOUR-SUBSCRIPTION-ID/` | `subscriptions/abcde123-abab-abab-1234-0123456789abc/` |
| `resourceGroups/YOUR-RESOURCE-GROUP/` | `resourceGroups/MyResourceGroup/` |
| `providers/operation-provider/` | `providers/Microsoft.MachineLearningServices/` |
| `provider-resource-path/` | `workspaces/MyWorkspace/experiments/FirstExperiment/runs/1/` |
| `operations-endpoint/` | `artifacts/metadata/` |


## Create and modify resources using PUT and POST requests

In addition to resource retrieval by using the GET verb, the REST API supports the creation of all the resources necessary to train, deploy, and monitor ML solutions. 

Training and running ML models require compute resources. You can list the compute resources of a workspace by using the following command: 

```bash
curl https://management.azure.com/subscriptions/<YOUR-SUBSCRIPTION-ID>/resourceGroups/<YOUR-RESOURCE-GROUP>/\
providers/Microsoft.MachineLearningServices/workspaces/<YOUR-WORKSPACE-NAME>/computes?api-version=2025-09-01 \
-H "Authorization:Bearer <YOUR-ACCESS-TOKEN>"
```

To create or overwrite a named compute resource, use a PUT request. In the following example, in addition to the now-familiar replacements of `YOUR-SUBSCRIPTION-ID`, `YOUR-RESOURCE-GROUP`, `YOUR-WORKSPACE-NAME`, and `YOUR-ACCESS-TOKEN`, replace `YOUR-COMPUTE-NAME`, and values for `location`, `vmSize`, `vmPriority`, and `scaleSettings`. The following command creates a dedicated, single-node Standard_D2s_v3 (a basic CPU compute resource) that scales down after 30 minutes:

```bash
curl -X PUT \
  'https://management.azure.com/subscriptions/<YOUR-SUBSCRIPTION-ID>/resourceGroups/<YOUR-RESOURCE-GROUP>/providers/Microsoft.MachineLearningServices/workspaces/<YOUR-WORKSPACE-NAME>/computes/<YOUR-COMPUTE-NAME>?api-version=2025-09-01' \
  -H 'Authorization:Bearer <YOUR-ACCESS-TOKEN>' \
  -H 'Content-Type: application/json' \
  -d '{
    "location": "eastus",
    "properties": {
        "computeType": "AmlCompute",
        "properties": {
            "vmSize": "Standard_D2s_v3",
            "vmPriority": "Dedicated",
            "scaleSettings": {
                "maxNodeCount": 1,
                "minNodeCount": 0,
                "nodeIdleTimeBeforeScaleDown": "PT30M"
            }
        }
    }
}'
```

> [!NOTE]
> In Windows terminals, you might have to escape the double-quote symbols when sending JSON data. That is, text such as `"location"` becomes `\"location\"`. 

A successful request returns a `201 Created` response, but this response simply means that the provisioning process has begun. You need to poll (or use the portal) to confirm its successful completion.

## Create a workspace by using REST 

Every Azure Machine Learning workspace depends on four other Azure resources: an Azure Container Registry resource, Azure Key Vault, Azure Application Insights, and an Azure Storage account. You can't create a workspace until these resources exist. Consult the REST API reference for the details of creating each such resource.

To create a workspace, send a PUT request similar to the following to `management.azure.com`. While this call requires you to set a large number of variables, it's structurally identical to other calls that this article discussed. 

```bash
curl -X PUT \
  'https://management.azure.com/subscriptions/<YOUR-SUBSCRIPTION-ID>/resourceGroups/<YOUR-RESOURCE-GROUP>\
/providers/Microsoft.MachineLearningServices/workspaces/<YOUR-NEW-WORKSPACE-NAME>?api-version=2025-09-01' \
  -H 'Authorization: Bearer <YOUR-ACCESS-TOKEN>' \
  -H 'Content-Type: application/json' \
  -d '{
    "location": "<AZURE-LOCATION>",
    "identity" : {
        "type" : "systemAssigned"
    },
    "properties": {
        "friendlyName" : "<YOUR-WORKSPACE-FRIENDLY-NAME>",
        "description" : "<YOUR-WORKSPACE-DESCRIPTION>",
        "containerRegistry" : "/subscriptions/<YOUR-SUBSCRIPTION-ID>/resourceGroups/<YOUR-RESOURCE-GROUP>/\
providers/Microsoft.ContainerRegistry/registries/<YOUR-REGISTRY-NAME>",
        "keyVault" : "/subscriptions/<YOUR-SUBSCRIPTION-ID>/resourceGroups/<YOUR-RESOURCE-GROUP>\
/providers/Microsoft.Keyvault/vaults/<YOUR-KEYVAULT-NAME>",
        "applicationInsights" : "subscriptions/<YOUR-SUBSCRIPTION-ID>/resourceGroups/<YOUR-RESOURCE-GROUP>/\
providers/Microsoft.insights/components/<YOUR-APPLICATION-INSIGHTS-NAME>",
        "storageAccount" : "/subscriptions/<YOUR-SUBSCRIPTION-ID>/resourceGroups/<YOUR-RESOURCE-GROUP>/\
providers/Microsoft.Storage/storageAccounts/<YOUR-STORAGE-ACCOUNT-NAME>"
    }
}'
```

You should receive a `202 Accepted` response and, in the returned headers, a `Location` URI. You can GET this URI for information on the deployment, including helpful debugging information if there's a problem with one of your dependent resources (for instance, if you forgot to enable admin access on your container registry). 

## Create a workspace by using a user-assigned managed identity 

When creating a workspace, you can specify a user-assigned managed identity that accesses the associated resources: ACR, KeyVault, Storage, and App Insights. To create a workspace with user-assigned managed identity, use the following request body. 

```bash
curl -X PUT \
  'https://management.azure.com/subscriptions/<YOUR-SUBSCRIPTION-ID>/resourceGroups/<YOUR-RESOURCE-GROUP>\
/providers/Microsoft.MachineLearningServices/workspaces/<YOUR-NEW-WORKSPACE-NAME>?api-version=2025-09-01' \
  -H 'Authorization: Bearer <YOUR-ACCESS-TOKEN>' \
  -H 'Content-Type: application/json' \
  -d '{
    "location": "<AZURE-LOCATION>",
    "identity": {
      "type": "SystemAssigned,UserAssigned",
      "userAssignedIdentities": {
        "/subscriptions/<YOUR-SUBSCRIPTION-ID>/resourceGroups/<YOUR-RESOURCE-GROUP>/\
providers/Microsoft.ManagedIdentity/userAssignedIdentities/<YOUR-MANAGED-IDENTITY>": {}
      }
    },
    "properties": {
        "friendlyName" : "<YOUR-WORKSPACE-FRIENDLY-NAME>",
        "description" : "<YOUR-WORKSPACE-DESCRIPTION>",
        "containerRegistry" : "/subscriptions/<YOUR-SUBSCRIPTION-ID>/resourceGroups/<YOUR-RESOURCE-GROUP>/\
providers/Microsoft.ContainerRegistry/registries/<YOUR-REGISTRY-NAME>",
        "keyVault" : "/subscriptions/<YOUR-SUBSCRIPTION-ID>/resourceGroups/<YOUR-RESOURCE-GROUP>\
/providers/Microsoft.Keyvault/vaults/<YOUR-KEYVAULT-NAME>",
        "applicationInsights" : "subscriptions/<YOUR-SUBSCRIPTION-ID>/resourceGroups/<YOUR-RESOURCE-GROUP>/\
providers/Microsoft.insights/components/<YOUR-APPLICATION-INSIGHTS-NAME>",
        "storageAccount" : "/subscriptions/<YOUR-SUBSCRIPTION-ID>/resourceGroups/<YOUR-RESOURCE-GROUP>/\
providers/Microsoft.Storage/storageAccounts/<YOUR-STORAGE-ACCOUNT-NAME>"
    }
}'
```

## Create a workspace using customer-managed encryption keys

By default, Azure Machine Learning stores workspace metadata in an Azure Cosmos DB instance that Microsoft maintains. This data is encrypted by using Microsoft-managed keys. Instead of using the Microsoft-managed key, you can also provide your own key. By using your key, you create [another set of resources](./concept-data-encryption.md#azure-cosmos-db) in your Azure subscription to store your data.

To create a workspace that uses your keys for encryption, you need to meet the following prerequisites:

* The Azure Machine Learning service principal must have contributor access to your Azure subscription.
* You must have an existing Azure Key Vault that contains an encryption key.
* The Azure Key Vault must exist in the same Azure region where you create the Azure Machine Learning workspace.
* The Azure Key Vault must have soft delete and purge protection enabled to protect against data loss if you accidentally delete it.
* You must have an access policy in Azure Key Vault that grants get, wrap, and unwrap access to the Azure Cosmos DB application.

To create a workspace that uses a user-assigned managed identity and customer-managed keys for encryption, use the following request body. When using a user-assigned managed identity for the workspace, also set the `userAssignedIdentity` property to the resource ID of the managed identity.

```bash
curl -X PUT \
  'https://management.azure.com/subscriptions/<YOUR-SUBSCRIPTION-ID>/resourceGroups/<YOUR-RESOURCE-GROUP>\
/providers/Microsoft.MachineLearningServices/workspaces/<YOUR-NEW-WORKSPACE-NAME>?api-version=2025-09-01' \
  -H 'Authorization: Bearer <YOUR-ACCESS-TOKEN>' \
  -H 'Content-Type: application/json' \
  -d '{
    "location": "eastus2euap",
    "identity": {
      "type": "SystemAssigned"
    },
    "properties": {
      "friendlyName": "<YOUR-WORKSPACE-FRIENDLY-NAME>",
      "description": "<YOUR-WORKSPACE-DESCRIPTION>",
      "containerRegistry" : "/subscriptions/<YOUR-SUBSCRIPTION-ID>/resourceGroups/<YOUR-RESOURCE-GROUP>/\
providers/Microsoft.ContainerRegistry/registries/<YOUR-REGISTRY-NAME>",
      "keyVault" : "/subscriptions/<YOUR-SUBSCRIPTION-ID>/resourceGroups/<YOUR-RESOURCE-GROUP>\
/providers/Microsoft.Keyvault/vaults/<YOUR-KEYVAULT-NAME>",
      "applicationInsights" : "subscriptions/<YOUR-SUBSCRIPTION-ID>/resourceGroups/<YOUR-RESOURCE-GROUP>/\
providers/Microsoft.insights/components/<YOUR-APPLICATION-INSIGHTS-NAME>",
      "storageAccount" : "/subscriptions/<YOUR-SUBSCRIPTION-ID>/resourceGroups/<YOUR-RESOURCE-GROUP>/\
providers/Microsoft.Storage/storageAccounts/<YOUR-STORAGE-ACCOUNT-NAME>",
      "encryption": {
        "status": "Enabled",
        "identity": {
          "userAssignedIdentity": null
        },      
        "keyVaultProperties": {
           "keyVaultArmId": "/subscriptions/<YOUR-SUBSCRIPTION-ID>/resourceGroups/<YOUR-RESOURCE-GROUP>/\
providers/Microsoft.KeyVault/vaults/<YOUR-VAULT>",
           "keyIdentifier": "https://<YOUR-VAULT>.vault.azure.net/keys/<YOUR-KEY>/<YOUR-KEY-VERSION>",
           "identityClientId": ""
        }
      },
      "hbiWorkspace": false
    }
}'
```

### Delete resources you no longer need

Some, but not all, resources support the DELETE verb. Check the [API Reference](/rest/api/azureml/) before committing to the REST API for deletion use cases. To delete a model, for instance, you can use:

```bash
curl
  -X DELETE \
'https://<REGIONAL-API-SERVER>/modelmanagement/v1.0/subscriptions/<YOUR-SUBSCRIPTION-ID>/resourceGroups/<YOUR-RESOURCE-GROUP>/providers/Microsoft.MachineLearningServices/workspaces/<YOUR-WORKSPACE-NAME>/models/<YOUR-MODEL-ID>?api-version=2025-09-01' \
  -H 'Authorization:Bearer <YOUR-ACCESS-TOKEN>' 
```

## Troubleshooting

### Resource provider errors

[!INCLUDE [machine-learning-resource-provider](includes/machine-learning-resource-provider.md)]

### Moving the workspace

> [!WARNING]
> You can't move your Azure Machine Learning workspace to a different subscription. You also can't move the subscription that owns the workspace to a new tenant. If you try to move the workspace, you might see errors.

### Deleting the Azure Container Registry

The Azure Machine Learning workspace uses Azure Container Registry (ACR) for some operations. It automatically creates an ACR instance when it first needs one.

[!INCLUDE [machine-learning-delete-acr](includes/machine-learning-delete-acr.md)]

## Next steps

- Explore the complete [Azure Machine Learning REST API reference](/rest/api/azureml/).
- Explore [Azure Machine Learning with Jupyter notebooks](../machine-learning/samples-notebooks.md).
