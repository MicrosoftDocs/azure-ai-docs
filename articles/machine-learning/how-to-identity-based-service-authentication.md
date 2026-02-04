---
title: Set up service authentication
titleSuffix: Azure Machine Learning
description: Learn how to set up and configure authentication between Azure Machine Learning and other Azure services.
services: machine-learning
author: s-polly
ms.author: scottpolly
ms.reviewer: shshubhe
ms.service: azure-machine-learning
ms.subservice: enterprise-readiness
ms.date: 01/22/2026
ms.topic: how-to
ms.custom: has-adal-ref, subject-rbac-steps, cliv2, sdkv2, devx-track-azurecli, dev-focus
ai-usage: ai-assisted
---

# Set up authentication between Azure Machine Learning and other services

[!INCLUDE [dev v2](includes/machine-learning-dev-v2.md)]

Azure Machine Learning is composed of multiple Azure services. Multiple methods support authentication between Azure Machine Learning and the services it relies on.

* The Azure Machine Learning workspace uses a __managed identity__ to communicate with other services. By default, this identity is a system-assigned managed identity. You can also use a user-assigned managed identity instead.
* Azure Machine Learning uses Azure Container Registry (ACR) to store Docker images used to train and deploy models. If you allow Azure Machine Learning to automatically create ACR, it enables the __admin account__.
* The Azure Machine Learning compute cluster uses a __managed identity__ to retrieve connection information for datastores from Azure Key Vault and to pull Docker images from ACR. You can also configure identity-based access to datastores, which uses the managed identity of the compute cluster.
* Data access can happen along multiple paths depending on the data storage service and your configuration. For example, authentication to the datastore might use an account key, token, security principal, managed identity, or user identity.
* Managed online endpoints can use a managed identity to access Azure resources when performing inference. For more information, see [Access Azure resources from an online endpoint](how-to-access-resources-from-endpoints-managed-identities.md).

## Prerequisites

[!INCLUDE [cli & sdk v2](includes/machine-learning-cli-sdk-v2-prereqs.md)]

* To assign roles, the sign in for your Azure subscription must have the [Managed Identity Operator](/azure/role-based-access-control/built-in-roles#managed-identity-operator) role, or another role that grants the required actions (such as __Owner__).

* You must be familiar with creating and working with [Managed Identities](/azure/active-directory/managed-identities-azure-resources/overview).

### RBAC roles by scenario

Depending on your scenario, you need specific Azure RBAC roles:

| Scenario | Required roles |
|----------|----------------|
| Workspace with user-assigned identity | Contributor on workspace, Storage Blob Data Contributor on storage, Key Vault Administrator, or access policies on key vault, Contributor on ACR |
| Compute cluster accessing storage | Storage Blob Data Reader (minimum) on storage account |
| Identity-based data access | Storage Blob Data Reader on Azure Blob Storage, Azure Data Lake Storage Gen1, or Gen2 |
| Pulling images from ACR | ACRPull on the container registry |
| Private ACR access | ACRPull on the private container registry |

For more information on assigning roles, see [Manage access to Azure Machine Learning workspaces](how-to-assign-roles.md).

## Choose an authentication method

The following table summarizes when to use each authentication approach:

| Scenario | Recommended identity | Alternative |
|----------|---------------------|-------------|
| Workspace accessing storage, Key Vault, and ACR | System-assigned managed identity | User-assigned managed identity |
| Compute cluster in training jobs | Compute managed identity | User identity (via job configuration) |
| Kubernetes cluster inferencing | Endpoint managed identity | System-assigned identity |
| Interactive data access (notebooks, studio) | User identity | Workspace managed identity |
| Azure Container Registry without admin user | System-assigned managed identity | User-assigned managed identity |
| Multiple workspaces sharing resources | User-assigned managed identity with data isolation | System-assigned identity (not recommended) |

## Limitations

Before configuring authentication, be aware of these limitations:

* **Identity type changes**: After you create a workspace with system-assigned plus user-assigned identities (SAI+UAI), you can't change it back to system-assigned only (SAI).
* **Cross-tenant access**: Cross-tenant access to storage accounts isn't supported. If your scenario requires cross-tenant access, [create an Azure support request](https://portal.azure.com/#blade/Microsoft_Azure_Support/HelpAndSupportBlade/newsupportrequest) for assistance with a custom code solution.
* **Compute cluster identity**: Azure Machine Learning compute clusters support only **one system-assigned identity** or **multiple user-assigned identities**, not both concurrently.
* **Kubernetes cluster identity**: Azure Machine Learning Kubernetes clusters support only **one system-assigned identity** or **one user-assigned identity**, not both concurrently.
* **Endpoint identity immutability**: The identity for an online endpoint is immutable. You can associate it with a system-assigned identity (default) or a user-assigned identity during creation, but you can't change it after the endpoint is created.
* **Data isolation timing**: You can set the data isolation option only when creating a workspace. You can't enable or disable it after workspace creation.

## Verify your setup

After configuring managed identities, verify your setup works correctly.

# [Azure CLI](#tab/azure-cli)

[!INCLUDE [cli v2](includes/machine-learning-cli-v2.md)]

```azurecli
# Verify workspace identity
az ml workspace show --name <workspace-name> --resource-group <resource-group> --query identity
```

Expected output: JSON object showing the identity type (`SystemAssigned`, `UserAssigned`, or `SystemAssigned,UserAssigned`) and principal IDs.

```azurecli
# Verify compute cluster identity
az ml compute show --name <compute-name> --resource-group <resource-group> --workspace-name <workspace-name> --query identity
```

Expected output: JSON object showing the managed identity configuration for the compute cluster.

# [Python SDK](#tab/python)

[!INCLUDE [sdk v2](includes/machine-learning-sdk-v2.md)]

```python
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()
ml_client = MLClient(credential, "<subscription-id>", "<resource-group>", "<workspace-name>")

# Verify workspace identity
workspace = ml_client.workspaces.get("<workspace-name>")
print(f"Identity type: {workspace.identity.type}")
print(f"Principal ID: {workspace.identity.principal_id}")
```

**Expected result**: Prints the identity type and principal ID. If you use user-assigned identities, also prints the user-assigned identity resource IDs.

**Reference**: [MLClient.workspaces.get](/python/api/azure-ai-ml/azure.ai.ml.operations.workspaceoperations#azure-ai-ml-operations-workspaceoperations-get)

# [Studio](#tab/azure-portal)

1. Go to [Azure Machine Learning studio](https://ml.azure.com).
1. Select your workspace.
1. Select **Settings** > **Properties**.
1. Verify the **Managed identity** section shows the expected identity type and principal ID.

---

## Workspace identity types

The Azure Machine Learning workspace uses a __managed identity__ to communicate with other services. Azure Machine Learning supports multiple identity types.

| Managed identity type | Role assignment creation | Purpose |
| ---- | :----: | :----: |
| System-assigned (SAI) | Managed by Microsoft | Lifecycle tied to resource; single resource use; simple to get started |
| System-assigned +user-assigned (SAI+UAI) | [Managed by you](#user-assigned-managed-identity) | Independent lifecycle for user-assigned identity; multiresource use; controls least privileged access; access data in training jobs. |

After you create a workspace with the SAI identity type, you can update it to SAI+UAI. You can't update a workspace from SAI+UAI to SAI. You can assign multiple user-assigned identities to the same workspace. 


## User-assigned managed identity

### Workspace

You can add a user-assigned managed identity when creating an Azure Machine Learning workspace from the [Azure portal](https://portal.azure.com). Use the following steps while creating the workspace:

1. From the __Basics__ page, select the Azure Storage Account, Azure Container Registry, and Azure Key Vault you want to use with the workspace.
1. From the __Identity__ page, select __User-assigned identity__ and then select the managed identity to use.

The following [Azure RBAC role assignments](/azure/role-based-access-control/role-assignments) are required on your user-assigned managed identity for your Azure Machine Learning workspace to access data on the workspace-associated resources.

|Resource|Permission|
|---|---|
|Azure Machine Learning workspace|Contributor|
|Azure Storage|Contributor (control plane) + Storage Blob Data Contributor (data plane, optional, to enable data preview in the Azure Machine Learning studio)|
|Azure Key Vault (when using [RBAC permission model](/azure/key-vault/general/rbac-guide))|Contributor (control plane) + Key Vault Administrator (data plane)|
|Azure Key Vault (when using [access policies permission model](/azure/key-vault/general/assign-access-policy))|Contributor + any access policy permissions besides **purge** operations|
|Azure Container Registry|Contributor|
|Azure Application Insights|Contributor|

For automated creation of role assignments on your user-assigned managed identity, you can use [this ARM template](https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.machinelearningservices/machine-learning-dependencies-role-assignment).

> [!TIP]
> For a workspace with [customer-managed keys for encryption](concept-data-encryption.md), you can pass in a user-assigned managed identity to authenticate from storage to Key Vault. Use the `user-assigned-identity-for-cmk-encryption` (CLI) or `user_assigned_identity_for_cmk_encryption` (SDK) parameters to pass in the managed identity. This managed identity can be the same or different as the workspace primary user assigned managed identity.

#### Find the user-assigned managed identity resource ID

When configuring a user-assigned managed identity (UAI), you need its resource ID. Use one of the following methods to find it:

- **Azure portal**: Navigate to your managed identity resource, select **Properties** from the left menu, and copy the **Resource ID** value.
- **Azure CLI**: Run the following command:

    ```azurecli
    az identity show --name <identity-name> --resource-group <resource-group> --query id --output tsv
    ```

The resource ID follows this format:

```
/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.ManagedIdentity/userAssignedIdentities/<identity-name>
```

#### To create a workspace with multiple user assigned identities, use one of the following methods:

# [Azure CLI](#tab/azure-cli)

[!INCLUDE [cli v2](includes/machine-learning-cli-v2.md)]

```azurecli
az ml workspace create -f workspace_creation_with_multiple_UAIs.yml --subscription <subscription ID> --resource-group <resource group name> --name <workspace name>
```

The following example shows the contents of *workspace_creation_with_multiple_UAIs.yml*:

```yaml
location: <region name>
identity:
   type: user_assigned
   user_assigned_identities:
    # Format: /subscriptions/<sub-id>/resourceGroups/<rg>/providers/Microsoft.ManagedIdentity/userAssignedIdentities/<name>
    '<UAI resource ID 1>': {}
    '<UAI resource ID 2>': {}
storage_account: <storage account resource ID>
key_vault: <key vault resource ID>
image_build_compute: <compute (virtual machine) resource ID>
primary_user_assigned_identity: <one of the UAI resource IDs in the above list>
```

# [Python SDK](#tab/python)

[!INCLUDE [sdk v2](includes/machine-learning-sdk-v2.md)]

```python
from azure.ai.ml import MLClient, load_workspace
from azure.identity import DefaultAzureCredential

sub_id="<subscription ID>"
rg_name="<resource group name>"
ws_name="<workspace name>"

client = MLClient(DefaultAzureCredential(), sub_id, rg_name)
wps = load_workspace("workspace_creation_with_multiple_UAIs.yml")

workspace = client.workspaces.begin_create(workspace=wps).result()
```

**Expected result**: Returns a `Workspace` object with the configured user-assigned identities. The operation might take several minutes to complete.

**Reference**: [MLClient.workspaces.begin_create](/python/api/azure-ai-ml/azure.ai.ml.operations.workspaceoperations#azure-ai-ml-operations-workspaceoperations-begin-create) | [load_workspace](/python/api/azure-ai-ml/azure.ai.ml#azure-ai-ml-load-workspace)

# [Studio](#tab/azure-portal)

Currently, not supported.

---


#### To update user assigned identities for a workspace, including adding a new one or deleting the existing ones, use one of the following methods:

# [Azure CLI](#tab/azure-cli)

[!INCLUDE [cli v2](includes/machine-learning-cli-v2.md)]

```azurecli
az ml workspace update -f workspace_update_with_multiple_UAIs.yml --subscription <subscription ID> --resource-group <resource group name> --name <workspace name>
```

The following example shows the contents of *workspace_update_with_multiple_UAIs.yml*:

```yaml
identity:
   type: user_assigned
   user_assigned_identities:
    # Format: /subscriptions/<sub-id>/resourceGroups/<rg>/providers/Microsoft.ManagedIdentity/userAssignedIdentities/<name>
    '<UAI resource ID 1>': {}
    '<UAI resource ID 2>': {}
primary_user_assigned_identity: <one of the UAI resource IDs in the above list>
```


# [Python SDK](#tab/python)

[!INCLUDE [sdk v2](includes/machine-learning-sdk-v2.md)]

```python
from azure.ai.ml import MLClient, load_workspace
from azure.identity import DefaultAzureCredential

sub_id="<subscription ID>"
rg_name="<resource group name>"
ws_name="<workspace name>"

client = MLClient(DefaultAzureCredential(), sub_id, rg_name)
wps = load_workspace("workspace_update_with_multiple_UAIs.yml")

workspace = client.workspaces.begin_update(workspace=wps).result()
```

**Expected result**: Returns the updated `Workspace` object. Verify the update by checking `workspace.identity.user_assigned_identities`.

**Reference**: [MLClient.workspaces.begin_update](/python/api/azure-ai-ml/azure.ai.ml.operations.workspaceoperations#azure-ai-ml-operations-workspaceoperations-begin-update)

# [Studio](#tab/azure-portal)

Currently, not supported.

---


> [!TIP]
> To add a new UAI, specify the new UAI ID under the `user_assigned_identities` section along with the existing UAIs. You must pass all the existing UAI IDs.<br>
To delete one or more existing UAIs, add the UAI IDs you want to keep under the `user_assigned_identities` section. The UAI IDs you don't include are deleted.<br>

### Add a user-assigned managed identity to a workspace in addition to a system-assigned identity

In some scenarios, you might need to use a user-assigned managed identity in addition to the default system-assigned workspace identity. To add a user-assigned managed identity without changing the existing workspace identity, use the following steps:

1. [Create a user-assigned managed identity](/entra/identity/managed-identities-azure-resources/how-manage-user-assigned-managed-identities). Save the ID for the managed identity that you create.
1. To attach the managed identity to your workspace, create a YAML file that specifies the identity. The following example shows the contents of the YAML file. Replace the `<TENANT_ID>`, `<RESOURCE_GROUP>`, and `<USER_MANAGED_ID>` placeholders with your values.
   
    ```yml
    identity:
        type: system_assigned,user_assigned
        tenant_id: <TENANT_ID>
        user_assigned_identities:
            '/subscriptions/<SUBSCRIPTION_ID/resourceGroups/<RESOURCE_GROUP>/providers/Microsoft.ManagedIdentity/userAssignedIdentities/<USER_MANAGED_ID>':
            {}
    ```
 
1. Use the Azure CLI `az ml workspace update` command to update your workspace. Specify the YAML file from the previous step by using the `--file` parameter. The following example shows what this command looks like:
 
    ```azurecli
    az ml workspace update --resource-group <RESOURCE_GROUP> --name <WORKSPACE_NAME> --file <YAML_FILE_NAME>.yaml
    ```

## Data isolation for shared resources

When multiple workspaces share the same associated resources (storage account, key vault, or container registry), enable data isolation to prevent naming conflicts and ensure each workspace can only access its own data. The `enableDataIsolation` flag configures how workspace artifacts are stored and accessed in shared resources.

> [!IMPORTANT]
> You can set the data isolation option only when creating a workspace. You can't enable or disable it after the workspace is created.

### Effects of enabling data isolation

When you enable data isolation, the workspace applies the following configurations:

| Resource | Behavior |
|----------|----------|
| **Storage account** | Container names are prefixed with the workspace GUID (for example, `{workspaceGUID}-azureml-blobstore`). The workspace managed identity receives a data plane role assignment with an [Azure attribute-based access control (ABAC)](/azure/role-based-access-control/conditions-overview) condition that limits access to only the workspace's specific containers. |
| **Key vault** | Secret names are prefixed with the workspace GUID to isolate secrets between workspaces sharing the same key vault. |
| **Container registry** | Docker image names are prefixed with the workspace GUID to isolate images between workspaces sharing the same registry. |

### Default behavior by workspace kind

Azure Machine Learning supports different workspace kinds for different organizational patterns:

- **default**: A standalone workspace for individual projects or teams. This workspace kind is the standard workspace type.
- **hub**: A central workspace that manages shared resources, policies, and connections for multiple related projects. For more information, see [hub workspaces](concept-hub-workspace.md).
- **project**: A lightweight workspace that inherits resources and settings from a parent hub workspace.

The default value for data isolation depends on the workspace kind:

| Workspace kind | Data isolation default |
|----------------|------------------------|
| `hub` | Enabled |
| `project` | Enabled (inherited from hub) |
| `default` | Disabled |

### When to enable data isolation

Enable data isolation when:

- Multiple workspaces share the same storage account, key vault, or container registry.
- You need to prevent naming conflicts for artifacts (such as Docker images or secrets) created with the same name across workspaces.
- You require stricter access control to ensure workspace identities can only access their own data.

For hub and project workspaces, enable data isolation by default to support the shared resource model. For more information, see [What is an Azure Machine Learning hub workspace?](concept-hub-workspace.md)

### Enable data isolation when creating a workspace

# [Azure CLI](#tab/azure-cli)

[!INCLUDE [cli v2](includes/machine-learning-cli-v2.md)]

```azurecli
az ml workspace create --name <WORKSPACE_NAME> \
    --resource-group <RESOURCE_GROUP> \
    --enable-data-isolation
```

Alternatively, specify data isolation in a YAML configuration file:

```yaml
$schema: https://azuremlschemas.azureedge.net/latest/workspace.schema.json
name: my-workspace
location: eastus
enable_data_isolation: true
storage_account: /subscriptions/<SUBSCRIPTION_ID>/resourceGroups/<RESOURCE_GROUP>/providers/Microsoft.Storage/storageAccounts/<STORAGE_ACCOUNT>
key_vault: /subscriptions/<SUBSCRIPTION_ID>/resourceGroups/<RESOURCE_GROUP>/providers/Microsoft.KeyVault/vaults/<KEY_VAULT>
container_registry: /subscriptions/<SUBSCRIPTION_ID>/resourceGroups/<RESOURCE_GROUP>/providers/Microsoft.ContainerRegistry/registries/<CONTAINER_REGISTRY>
```

Then create the workspace:

```azurecli
az ml workspace create --file workspace.yml --resource-group <RESOURCE_GROUP>
```

# [Python SDK](#tab/python)

[!INCLUDE [sdk v2](includes/machine-learning-sdk-v2.md)]

```python
from azure.ai.ml import MLClient
from azure.ai.ml.entities import Workspace
from azure.identity import DefaultAzureCredential

# Replace with your Azure subscription and resource group
subscription_id = "<SUBSCRIPTION_ID>"
resource_group = "<RESOURCE_GROUP>"

credential = DefaultAzureCredential()
ml_client = MLClient(credential, subscription_id, resource_group)

workspace = Workspace(
    name="my-workspace",
    location="eastus",
    enable_data_isolation=True,
    storage_account="/subscriptions/<SUBSCRIPTION_ID>/resourceGroups/<RESOURCE_GROUP>/providers/Microsoft.Storage/storageAccounts/<STORAGE_ACCOUNT>",
    key_vault="/subscriptions/<SUBSCRIPTION_ID>/resourceGroups/<RESOURCE_GROUP>/providers/Microsoft.KeyVault/vaults/<KEY_VAULT>",
    container_registry="/subscriptions/<SUBSCRIPTION_ID>/resourceGroups/<RESOURCE_GROUP>/providers/Microsoft.ContainerRegistry/registries/<CONTAINER_REGISTRY>"
)

ml_client.workspaces.begin_create(workspace).result()
```

**Expected result**: Returns the created `Workspace` object with `enable_data_isolation=True`. Container names in the storage account are prefixed with the workspace GUID.

**Reference**: [Workspace](/python/api/azure-ai-ml/azure.ai.ml.entities.workspace)

# [Studio](#tab/azure-portal)

When you create hub or project workspaces through Azure Machine Learning studio, data isolation is automatically enabled. For default workspaces, the studio interface doesn't provide this setting. Use the Azure CLI or Python SDK to create a default workspace with data isolation enabled.

---


## Compute cluster

> [!NOTE]
> Azure Machine Learning compute clusters support only **one system-assigned identity** or **multiple user-assigned identities**, not both concurrently.

The **default managed identity** is the system-assigned managed identity or the first user-assigned managed identity.

During a run, an identity has two applications:

1. The system uses an identity to set up the user's storage mounts, container registry, and datastores.

    * In this case, the system uses the default-managed identity.

1. You apply an identity to access resources from within the code for a submitted job:

    * In this case, provide the *client_id* corresponding to the managed identity you want to use to retrieve a credential.
    * Alternatively, get the user-assigned identity's client ID through the *DEFAULT_IDENTITY_CLIENT_ID* environment variable.

    For example, to retrieve a token for a datastore with the default-managed identity:

    ```python
    import os
    from azure.identity import ManagedIdentityCredential

    client_id = os.environ.get('DEFAULT_IDENTITY_CLIENT_ID')
    credential = ManagedIdentityCredential(client_id=client_id)
    token = credential.get_token('https://storage.azure.com/')
    ```

    **Expected result**: Returns an access token for Azure Storage. If `DEFAULT_IDENTITY_CLIENT_ID` isn't set, the call fails with an environment variable error.

    **Reference**: [ManagedIdentityCredential](/python/api/azure-identity/azure.identity.managedidentitycredential)

To configure a compute cluster with managed identity, use one of the following methods:

# [Azure CLI](#tab/azure-cli)

[!INCLUDE [cli v2](includes/machine-learning-cli-v2.md)]

```azurecli
az ml compute create -f create-cluster.yml
```

The following example shows the contents of *create-cluster.yml*: 

:::code language="yaml" source="~/azureml-examples-main/cli/resources/compute/cluster-user-identity.yml":::

For comparison, the following example is from a YAML file that creates a cluster that uses a system-assigned managed identity:

:::code language="yaml" source="~/azureml-examples-main/cli/resources/compute/cluster-system-identity.yml":::

If you have an existing compute cluster, you can switch between user-managed and system-managed identity. The following examples demonstrate how to change the configuration:

__User-assigned managed identity__

:::code language="azurecli" source="~/azureml-examples-main/cli/deploy-mlcompute-update-to-user-identity.sh":::

__System-assigned managed identity__

:::code language="azurecli" source="~/azureml-examples-main/cli/deploy-mlcompute-update-to-system-identity.sh":::

# [Python SDK](#tab/python)

[!INCLUDE [sdk v2](includes/machine-learning-sdk-v2.md)]

```python
from azure.ai.ml.entities import ManagedIdentityConfiguration, IdentityConfiguration, AmlCompute
from azure.ai.ml.constants import ManagedServiceIdentityType

# Create an identity configuration from the user-assigned managed identity
managed_identity = ManagedIdentityConfiguration(resource_id="/subscriptions/<subscription_id>/resourcegroups/<resource_group>/providers/Microsoft.ManagedIdentity/userAssignedIdentities/<identity>")
identity_config = IdentityConfiguration(type = ManagedServiceIdentityType.USER_ASSIGNED, user_assigned_identities=[managed_identity])

# specify aml compute name.
cpu_compute_target = "cpu-cluster"

try:
    ml_client.compute.get(cpu_compute_target)
except Exception:
    print("Creating a new cpu compute target...")
    # Pass the identity configuration
    compute = AmlCompute(
        name=cpu_compute_target, size="STANDARD_D2_V2", min_instances=0, max_instances=4, identity=identity_config
    )
    ml_client.compute.begin_create_or_update(compute)
```

**Expected result**: Creates or updates a compute cluster with the specified managed identity. The operation returns an `AmlCompute` object.

**Reference**: [AmlCompute](/python/api/azure-ai-ml/azure.ai.ml.entities.amlcompute) | [ManagedIdentityConfiguration](/python/api/azure-ai-ml/azure.ai.ml.entities.managedidentityconfiguration) | [IdentityConfiguration](/python/api/azure-ai-ml/azure.ai.ml.entities.identityconfiguration)

# [Studio](#tab/azure-portal)

During cluster creation or when you edit compute cluster details, in the **Advanced settings**, toggle **Assign a managed identity** and specify a system-assigned identity or user-assigned identity.

---


## Kubernetes cluster compute

> [!NOTE]
> Azure Machine Learning Kubernetes clusters support only **one system-assigned identity** or **one user-assigned identity**, not both concurrently.

The **default managed identity** is the system-assigned managed identity or the first user-assigned managed identity.


During a run, an identity has two applications:

- The system uses an identity to set up the user's storage mounts, container registry, and datastores.

    * In this case, the system uses the default-managed identity.

- You apply an identity to access resources from within the code for a submitted job:

    * In the case of Kubernetes cluster compute, the ManagedIdentityCredential object should be provided **without any client_id**.

    For example, to retrieve a token for a datastore with the default-managed identity:

    ```python
    from azure.identity import ManagedIdentityCredential

    credential = ManagedIdentityCredential()
    token = credential.get_token('https://storage.azure.com/')
    ```

    **Expected result**: Returns an access token for Azure Storage. Unlike compute clusters, don't specify a `client_id` for Kubernetes clusters.

    **Reference**: [ManagedIdentityCredential](/python/api/azure-identity/azure.identity.managedidentitycredential)

To configure a Kubernetes cluster compute, make sure that it has the [necessary AML extension deployed in it](how-to-deploy-kubernetes-extension.md?view=azureml-api-2&preserve-view=true&tabs=deploy-extension-with-cli) and follow the documentation on [how to attach the Kubernetes cluster compute to your AML workspace](how-to-attach-kubernetes-to-workspace.md?view=azureml-api-2&preserve-view=true&tabs=cli).

> [!IMPORTANT] 
> For training purposes (Machine Learning Jobs), use the identity assigned to the Kubernetes cluster compute. However, for inferencing (Managed Online Endpoints), use the identity assigned to the endpoint. For more information, see [How to Access Azure Resources from an Online Endpoint](how-to-access-resources-from-endpoints-managed-identities.md?view=azureml-api-2&preserve-view=true&tabs=system-identity-cli).

## Data storage

When you create a datastore that uses **identity-based data access**, you use your Azure account ([Microsoft Entra token](/azure/active-directory/fundamentals/active-directory-whatis)) to confirm you have permission to access the storage service. In the **identity-based data access** scenario, you don't save any authentication credentials. You only store the storage account information in the datastore.

In contrast, datastores that use **credential-based authentication** cache connection information, like your storage account key or SAS token, in the [key vault](https://azure.microsoft.com/services/key-vault/) that's associated with the workspace. This approach has the limitation that other workspace users with sufficient permissions can retrieve those credentials, which might be a security concern for some organizations.

For more information on how data access is authenticated, see the [Data administration](how-to-administrate-data-authentication.md) article. For information on configuring identity based access to data, see [Create datastores](how-to-datastore.md).

You can apply identity-based data access in Azure Machine Learning in two scenarios. These scenarios are a good fit for identity-based access when you're working with confidential data and need more granular data access management:

- Accessing storage services
- Training machine learning models

By using identity-based access, you can use [role-based access controls (RBAC)](/azure/storage/blobs/assign-azure-role-data-access) to restrict which identities, such as users or compute resources, have access to the data. 

### Access storage services

You can connect to storage services by using identity-based data access with [Azure Machine Learning datastores](how-to-datastore.md). 

When you use identity-based data access, Azure Machine Learning prompts you for your Microsoft Entra token for data access authentication instead of keeping your credentials in the datastore. This approach allows for data access management at the storage level and keeps credentials confidential. 

The same behavior applies when you work with data interactively via a Jupyter Notebook on your local computer or [compute instance](concept-compute-instance.md).

> [!NOTE]
> Credentials stored through credential-based authentication include subscription IDs, shared access signature (SAS) tokens, storage access key, and service principal information such as client IDs and tenant IDs.

To securely connect to your storage service on Azure, Azure Machine Learning requires that you have permission to access the corresponding data storage.
 
> [!WARNING]
> Cross-tenant access to storage accounts isn't supported. If your scenario requires cross-tenant access, [create an Azure support request](https://portal.azure.com/#blade/Microsoft_Azure_Support/HelpAndSupportBlade/newsupportrequest) for assistance with a custom code solution.

Identity-based data access supports connections to **only** the following storage services.

* Azure Blob Storage
* Azure Data Lake Storage Gen1
* Azure Data Lake Storage Gen2

To access these storage services, you must have at least [Storage Blob Data Reader](/azure/role-based-access-control/built-in-roles#storage-blob-data-reader) access to the storage account. Only storage account owners can [change your access level via the Azure portal](/azure/storage/blobs/assign-azure-role-data-access). 

### Access data for training jobs on compute using managed identity

Certain machine learning scenarios involve working with private data. In such cases, data scientists might not have direct access to data as Microsoft Entra users. In this scenario, use the managed identity of a compute for data access authentication. You can only access the data from a compute instance or a machine learning compute cluster executing a training job. By using this approach, the admin grants the compute instance or compute cluster managed identity Storage Blob Data Reader permissions on the storage. The individual data scientists don't need to be granted access.

To enable authentication by using compute managed identity:

 * Create compute with managed identity enabled. See the [compute cluster](#compute-cluster) section, or for compute instance, the [Assign managed identity](how-to-create-compute-instance.md#assign-managed-identity) section.

    > [!IMPORTANT]
    > If you configure the compute instance for [idle shutdown](how-to-create-compute-instance.md#configure-idle-shutdown), the compute instance doesn't shut down due to inactivity unless the managed identity has *contributor* access to the Azure Machine Learning workspace. For more information on assigning permissions, see [Manage access to Azure Machine Learning workspaces](how-to-assign-roles.md).

 * Grant compute managed identity at least Storage Blob Data Reader role on the storage account.
 * Create any datastores with identity-based authentication enabled. See [Create datastores](how-to-datastore.md).

> [!NOTE]
> The name of the created system managed identity for compute instance or cluster is in the format `/workspace-name/computes/compute-name` in your Microsoft Entra ID.

Once you enable identity-based authentication, the compute managed identity is used by default when accessing data within your training jobs. Optionally, you can authenticate by using user identity by following the steps described in next section.

For information on configuring Azure RBAC for the storage, see [role-based access controls](/azure/storage/blobs/assign-azure-role-data-access).

### Access data for training jobs on compute clusters by using user identity

[!INCLUDE [cli v2](includes/machine-learning-cli-v2.md)]

When you train on [Azure Machine Learning compute clusters](how-to-create-attach-compute-cluster.md#what-is-a-compute-cluster), you can authenticate to storage by using your user Microsoft Entra token. 

This authentication mode enables you to: 
* Set up fine-grained permissions, where different workspace users can access different storage accounts or folders within storage accounts.
* Let data scientists reuse existing permissions on storage systems.
* Audit storage access because the storage logs show which identities were used to access data.

> [!IMPORTANT] 
> This functionality has the following limitations:
> * Experiments submitted through the [Azure Machine Learning CLI and Python SDK V2](concept-v2.md) support this feature, but ML Studio doesn't.
> * You can't use user identity and compute managed identity for authentication in the same job.
> * For pipeline jobs, set user identity at the individual step level that runs on a compute, rather than at the root pipeline level. While identity setting is supported at both root pipeline and step levels, the step level setting takes precedence if both are set. However, for pipelines containing pipeline components, identity must be set on individual steps that run. Identity set at the root pipeline or pipeline component level doesn't function. Therefore, set identity at the individual step level for simplicity.

To set up data access by using user identity for training jobs on compute clusters from CLI, follow these steps: 

1. Grant the user identity access to storage resources. For example, grant StorageBlobReader access to the specific storage account you want to use or grant ACL-based permission to specific folders or files in Azure Data Lake Gen 2 storage.

1. Create an Azure Machine Learning datastore without cached credentials for the storage account. If a datastore has cached credentials, such as storage account key, those credentials are used instead of user identity.

1. Submit a training job with property **identity** set to **type: user_identity**, as shown in following job specification. During the training job, the authentication to storage happens via  the identity of the user that submits the job.

    > [!NOTE] 
    > If you don't specify the **identity** property and the datastore doesn't have cached credentials, the system uses compute managed identity as a fallback. 

    ```yaml
    command: |
    echo "--census-csv: ${{inputs.census_csv}}"
    python hello-census.py --census-csv ${{inputs.census_csv}}
    code: src
    inputs:
    census_csv:
        type: uri_file 
        path: azureml://datastores/mydata/paths/census.csv
    environment: azureml:AzureML-sklearn-1.0-ubuntu20.04-py38-cpu@latest
    compute: azureml:cpu-cluster
    identity:
    type: user_identity
    ```

To set up data access by using user identity for training jobs on compute clusters from Python SDK, follow these steps:

1. Grant data access and create data store as described earlier for CLI.

1. Submit a training job with identity parameter set to [azure.ai.ml.UserIdentityConfiguration](/python/api/azure-ai-ml/azure.ai.ml.entities.useridentityconfiguration). This parameter setting enables the job to access data on behalf of user submitting the job.

    ```python
    from azure.ai.ml import command
    from azure.ai.ml.entities import Data, UriReference
    from azure.ai.ml import Input
    from azure.ai.ml.constants import AssetTypes
    from azure.ai.ml import UserIdentityConfiguration
    
    # Specify the data location
    my_job_inputs = {
        "input_data": Input(type=AssetTypes.URI_FILE, path="<path-to-my-data>")
    }

    # Define the job
    job = command(
        code="<my-local-code-location>", 
        command="python <my-script>.py --input_data ${{inputs.input_data}}",
        inputs=my_job_inputs,
        environment="AzureML-sklearn-0.24-ubuntu18.04-py37-cpu:9",
        compute="<my-compute-cluster-name>",
        identity= UserIdentityConfiguration() 
    )
    # submit the command
    returned_job = ml_client.jobs.create_or_update(job)
    ```

> [!IMPORTANT] 
> When you submit a job with authentication by using user identity, checksum validation protects the code snapshots against tampering. If you have existing pipeline components and you intend to use them with authentication by using user identity, you might need to re-upload them. Otherwise, the job might fail during checksum validation. 


### Work with virtual networks

By default, Azure Machine Learning can't communicate with a storage account that's behind a firewall or in a virtual network.

You can configure storage accounts to allow access only from specific virtual networks. This configuration requires extra steps to ensure data isn't leaked outside of the network. This behavior is the same for credential-based data access. For more information, see [How to prevent data exfiltration](how-to-prevent-data-loss-exfiltration.md). 

If your storage account has virtual network settings, those settings dictate what identity type and permissions access is needed. For example, for data preview and data profile, the virtual network settings determine what type of identity is used to authenticate data access. 
 
* In scenarios where only certain IPs and subnets can access the storage, Azure Machine Learning uses the workspace MSI to accomplish data previews and profiles.

* If your storage is ADLS Gen2 or Blob and has virtual network settings, you can use either user identity or workspace MSI depending on the datastore settings defined during creation. 

* If the virtual network setting is **Allow Azure services on the trusted services list to access this storage account**, Workspace MSI is used. 

## Scenario: Azure Container Registry without admin user

When you disable the admin user for ACR, Azure Machine Learning uses a managed identity to build and pull Docker images. There are two workflows when configuring Azure Machine Learning to use an ACR with the admin user disabled:

* Allow Azure Machine Learning to create the ACR instance and then disable the admin user.
* Bring an existing ACR with the admin user already disabled.

### Azure Machine Learning with autocreated ACR instance

1. Create a new Azure Machine Learning workspace.
1. Perform an action that requires Azure Container Registry. For example, see the [Tutorial: Train your first model](tutorial-1st-experiment-sdk-train.md).
1. Get the name of the ACR created by the cluster.

    [!INCLUDE [cli v2](includes/machine-learning-cli-v2.md)]

    ```azurecli-interactive
    az ml workspace show --name <my workspace name> \
    --resource-group <my resource group> \
    --subscription <my subscription id> \
    --query container_registry
    ```

    This command returns a value similar to the following text. You only want the last portion of the text, which is the ACR instance name:

    ```output
    /subscriptions/<subscription id>/resourceGroups/<my resource group>/providers/MicrosoftContainerReggistry/registries/<ACR instance name>
    ```

1. Update the ACR to disable the admin user:

    ```azurecli-interactive
    az acr update --name <ACR instance name> --admin-enabled false
    ```

### Bring your own ACR

If the subscription policy disallows ACR admin user, first create ACR without admin user, and then associate it with the workspace. 
[Create ACR from Azure CLI](/azure/container-registry/container-registry-get-started-azure-cli) without setting the `--admin-enabled` argument, or from Azure portal without enabling admin user. When creating Azure Machine Learning workspace, specify the Azure resource ID of the ACR. The following example demonstrates creating a new Azure Machine Learning workspace that uses an existing ACR:

[!INCLUDE [cli v2](includes/machine-learning-cli-v2.md)]

```azurecli-interactive
az ml workspace create -n <workspace name> \
-g <workspace resource group> \
-l <region> \
--container-registry /subscriptions/<subscription id>/resourceGroups/<acr resource group>/providers/Microsoft.ContainerRegistry/registries/<acr name>
```

> [!TIP]
> To get the value for the `--container-registry` parameter, use the [az acr show](/cli/azure/acr#az-acr-show) command to show information for your ACR. The `id` field contains the resource ID for your ACR.

Also, if you already have an existing ACR with admin user disabled, you can attach it to the workspace by updating it. The following example demonstrates updating an Azure Machine Learning workspace to use an existing ACR:

[!INCLUDE [cli v2](includes/machine-learning-cli-v2.md)]

```azurecli-interactive
az ml workspace update --update-dependent-resources \
--name <workspace name> \
--resource-group <workspace resource group> \
--container-registry /subscriptions/<subscription id>/resourceGroups/<acr resource group>/providers/Microsoft.ContainerRegistry/registries/<acr name>
```

### Create compute with managed identity to access Docker images for training

To access the workspace ACR, create machine learning compute cluster with system-assigned managed identity enabled. You can enable the identity from Azure portal or Studio when creating compute, or from Azure CLI using the following command. For more information, see [using managed identity with compute clusters](how-to-create-attach-compute-cluster.md#set-up-managed-identity).

# [Azure CLI](#tab/azure-cli)

[!INCLUDE [cli v2](includes/machine-learning-cli-v2.md)]

```azurecli-interactive
az ml compute create --name cpu-cluster --type <cluster name>  --identity-type systemassigned
```

# [Python](#tab/python)

[!INCLUDE [sdk v2](includes/machine-learning-sdk-v2.md)]

```python
    from azure.ai.ml.entities import IdentityConfiguration, AmlCompute
    from azure.ai.ml.constants import ManagedServiceIdentityType
    
    # Create an identity configuration for a system-assigned managed identity
    identity_config = IdentityConfiguration(type = ManagedServiceIdentityType.SYSTEM_ASSIGNED)
    
    # specify aml compute name.
    cpu_compute_target = "cpu-cluster"
    
    try:
        ml_client.compute.get(cpu_compute_target)
    except Exception:
        print("Creating a new cpu compute target...")
        # Pass the identity configuration
        compute = AmlCompute(
            name=cpu_compute_target, size="STANDARD_D2_V2", min_instances=0, max_instances=4, identity=identity_config
        )
        ml_client.compute.begin_create_or_update(compute)
```

# [Studio](#tab/azure-portal)

For information on configuring managed identity when creating a compute cluster in studio, see [Set up managed identity](how-to-create-attach-compute-cluster.md#set-up-managed-identity).

---


A managed identity automatically gets the ACRPull role on the workspace ACR to enable pulling Docker images for training.

> [!NOTE]
> If you create compute first, before the workspace ACR exists, you need to assign the ACRPull role manually.

### Use Docker images for inference

After you configure ACR without admin user as described earlier, you can access Docker images for inference without admin keys from your Azure Kubernetes service (AKS). When you create or attach AKS to workspace, the cluster's service principal automatically gets ACRPull access to the workspace ACR.

> [!NOTE]
> If you bring your own AKS cluster, the cluster must have service principal enabled instead of managed identity.

## Scenario: Use a private Azure Container Registry

By default, Azure Machine Learning uses Docker base images from a public repository that Microsoft manages. It builds your training or inference environment on those images. For more information, see [What are ML environments?](concept-environments.md)

To use a custom base image internal to your enterprise, use managed identities to access your private ACR.

1. Create a machine learning compute cluster with system-assigned managed identity enabled as described earlier. Then, determine the principal ID of the managed identity.

    [!INCLUDE [cli v2](includes/machine-learning-cli-v2.md)]

    ```azurecli-interactive
    az ml compute show --name <cluster name> -n <workspace> -g <resource group>
    ```

    Optionally, you can update the compute cluster to assign a user-assigned managed identity:

    [!INCLUDE [cli v2](includes/machine-learning-cli-v2.md)]

    ```azurecli-interactive
    az ml compute update --name <cluster name> --user-assigned-identities <my-identity-id>
    ```

1. To allow the compute cluster to pull the base images, grant the managed service identity (for the workspace or compute) ACRPull role on the private ACR.

    [!INCLUDE [cli v2](includes/machine-learning-cli-v2.md)]

    ```azurecli-interactive
    az role assignment create --assignee <principal ID> \
    --role acrpull \
    --scope "/subscriptions/<subscription ID>/resourceGroups/<private ACR resource group>/providers/Microsoft.ContainerRegistry/registries/<private ACR name>"
    ```

1. Create an environment and specify the base image location in the [environment YAML file](reference-yaml-environment.md). The following YAML file demonstrates how to define an environment that references the private ACR. Replace the `<acr-url>` with the URL of your private ACR, such as `myregistry.azurecr.io`. Replace the `<image-path>` with the path to your image in the private ACR, such as `pytorch/pytorch:latest`:

    ```yml
    $schema: https://azuremlschemas.azureedge.net/latest/environment.schema.json
    name: docker-image-example
    image: <acr-url>/<image-path>:latest
    description: Environment created from a Docker image.
    ```
    
1. The following command demonstrates how to create the environment from the YAML file. Replace `<yaml file>` with the path to your YAML file:

    ```azurecli
    az ml environment create --file <yaml file>
    ```

    You can now use the environment in a [training job](how-to-train-cli.md).

## Troubleshooting

This section addresses common issues when configuring identity-based authentication.

### Identity doesn't have permission to access storage

**Symptom**: You receive a 403 Forbidden error when trying to access data from Azure Storage.

**Cause**: The managed identity doesn't have the required Azure RBAC role on the storage account.

**Resolution**: Assign the appropriate role to the managed identity:

```azurecli
# Assign Storage Blob Data Reader role
az role assignment create \
    --assignee <principal-id> \
    --role "Storage Blob Data Reader" \
    --scope /subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.Storage/storageAccounts/<storage-account>
```

Replace `<principal-id>` with the managed identity's principal ID from the [Verify your setup](#verify-your-setup) section.

### Token retrieval fails in training job

**Symptom**: `ManagedIdentityCredential` fails to retrieve a token with an environment variable error.

**Cause**: The `DEFAULT_IDENTITY_CLIENT_ID` environment variable isn't set, or the compute cluster doesn't have a managed identity configured.

**Resolution**: 
1. Verify the compute cluster has a managed identity enabled. See [Compute cluster](#compute-cluster).
1. In your code, retrieve the client ID from the environment:

```python
import os
from azure.identity import ManagedIdentityCredential

client_id = os.environ.get('DEFAULT_IDENTITY_CLIENT_ID')
if not client_id:
    raise ValueError("DEFAULT_IDENTITY_CLIENT_ID environment variable not set. Verify compute has managed identity enabled.")

credential = ManagedIdentityCredential(client_id=client_id)
```

### Storage firewall blocks access

**Symptom**: Access denied errors when storage account has firewall rules enabled.

**Cause**: The workspace or compute managed identity can't access storage through the firewall.

**Resolution**: Configure the storage account to allow access from trusted Azure services:

1. In Azure portal, go to your storage account.
1. Select **Networking** > **Firewalls and virtual networks**.
1. Under **Exceptions**, select **Allow Azure services on the trusted services list to access this storage account**.

For more information, see [Work with virtual networks](#work-with-virtual-networks).

### ACR image pull fails

**Symptom**: Training jobs fail to pull Docker images from Azure Container Registry.

**Cause**: The compute managed identity doesn't have the ACRPull role on the container registry.

**Resolution**: Assign the ACRPull role:

```azurecli
az role assignment create \
    --assignee <principal-id> \
    --role acrpull \
    --scope /subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.ContainerRegistry/registries/<registry-name>
```

> [!NOTE]
> If you create the compute cluster before the workspace ACR exists, you must assign the ACRPull role manually.

### User identity authentication fails in job

**Symptom**: Jobs that use user identity for data access fail during checksum validation.

**Cause**: Pipeline components need to be re-uploaded when you create them before enabling user identity authentication.

**Resolution**: Re-upload pipeline components to regenerate checksums:

```azurecli
az ml component create --file <component-yaml> --resource-group <resource-group> --workspace-name <workspace-name>
```

For more data access troubleshooting, see [Troubleshoot data access errors](how-to-troubleshoot-data-access.md).

## Next steps

> [!div class="nextstepaction"]
> [Create datastores with identity-based access](how-to-datastore.md)

> [!div class="nextstepaction"]
> [Submit training jobs](how-to-train-cli.md)

## Related content

* [Enterprise security in Azure Machine Learning](concept-enterprise-security.md)
* [Data administration and authentication](how-to-administrate-data-authentication.md)
* [Managed identities on compute clusters](how-to-create-attach-compute-cluster.md)
* [Troubleshoot data access errors](how-to-troubleshoot-data-access.md)
* [Access Azure resources from online endpoints](how-to-access-resources-from-endpoints-managed-identities.md)
* [Set up authentication for Azure Machine Learning](how-to-setup-authentication.md)
* [Authenticate clients for online endpoints](how-to-authenticate-online-endpoint.md)
