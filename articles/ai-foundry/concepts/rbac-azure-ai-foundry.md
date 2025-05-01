---
title: Role-based access control in Azure AI Foundry portal
titleSuffix: Azure AI Foundry
description: This article introduces role-based access control in Azure AI Foundry portal.
manager: scottpolly
ms.service: azure-ai-foundry
ms.custom:
  - ignite-2023
  - build-2024
  - ignite-2024
ms.topic: conceptual
ms.date: 03/04/2025
ms.reviewer: deeikele
ms.author: larryfr
author: Blackmist
---

# Role-based access control in Azure AI Foundry portal

In this article, you learn how to manage access (authorization) to an [Azure AI Foundry](https://ai.azure.com) hub. Azure role-based access control (Azure RBAC) is used to manage access to Azure resources, such as the ability to create new resources or use existing ones. Users in your Microsoft Entra ID are assigned specific roles, which grant access to resources. Azure provides both built-in roles and the ability to create custom roles. 

> [!WARNING]
> Applying some roles might limit UI functionality in Azure AI Foundry portal for other users. For example, if a user's role doesn't have the ability to create a compute instance, the option to create a compute instance isn't available in studio. This behavior is expected, and prevents the user from attempting operations that would return an access denied error. 

## Azure AI Foundry hub vs project

In the Azure AI Foundry portal, there are two levels of access: the hub and the project. The hub is home to the infrastructure (including virtual network setup, customer-managed keys, managed identities, and policies) and where you configure your Azure AI services. Hub access can allow you to modify the infrastructure, create new hubs, and create projects. Projects are a subset of the hub that act as workspaces that allow you to build and deploy AI systems. Within a project you can develop flows, deploy models, and manage project assets. Project access lets you develop AI end-to-end while taking advantage of the infrastructure setup on the hub.

:::image type="content" source="../media/concepts/resource-provider-connected-resources.svg" alt-text="Diagram of the relationship between Azure AI Foundry resources.":::

One of the key benefits of the hub and project relationship is that developers can create their own projects that inherit the hub security settings. You might also have developers who are contributors to a project, and can't create new projects.

## Default roles for the hub 

The Azure AI Foundry hub has built-in roles that are available by default. 

Here's a table of the built-in roles and their permissions for the hub:

| Role | Description | 
| --- | --- |
| Owner | Full access to the hub, including the ability to manage and create new hubs and assign permissions. This role is automatically assigned to the hub creator|
| Contributor | User has full access to the hub, including the ability to create new hubs, but isn't able to manage hub permissions on the existing resource. |
| Azure AI Administrator (preview) | This role is automatically assigned to the system-assigned managed identity for the hub. The Azure AI Administrator role has the minimum permissions needed for the managed identity to perform its tasks. For more information, see [Azure AI Administrator role (preview)](#azure-ai-administrator-role-preview). |
| Azure AI Developer |     Perform all actions except create new hubs and manage the hub permissions. For example, users can create projects, compute, and connections. Users can assign permissions within their project. Users can interact with existing Azure AI resources such as Azure OpenAI, Azure AI Search, and Azure AI services. |
| Azure AI Inference Deployment Operator | Perform all actions required to create a resource deployment within a resource group. |
| Reader |     Read only access to the hub. This role is automatically assigned to all project members within the hub. |

The key difference between Contributor and Azure AI Developer is the ability to make new hubs. If you don't want users to make new hubs (due to quota, cost, or just managing how many hubs you have), assign the Azure AI Developer role.

Only the Owner and Contributor roles allow you to make a hub. At this time, custom roles can't grant you permission to make hubs.

### Azure AI Administrator role (preview)

Prior to 11/19/2024, the system-assigned managed identity created for the hub was automatically assigned the __Contributor__ role for the resource group that contains the hub and projects. Hubs created after this date have the system-assigned managed identity assigned to the __Azure AI Administrator__ role. This role is more narrowly scoped to the minimum permissions needed for the managed identity to perform its tasks.

The __Azure AI Administrator__ role is currently in public preview.

[!INCLUDE [feature-preview](../includes/feature-preview.md)]

The __Azure AI Administrator__ role has the following permissions:

```json
{
    "permissions": [
        {
            "actions": [
                "Microsoft.Authorization/*/read",
                "Microsoft.CognitiveServices/*",
                "Microsoft.ContainerRegistry/registries/*",
                "Microsoft.DocumentDb/databaseAccounts/*",
                "Microsoft.Features/features/read",
                "Microsoft.Features/providers/features/read",
                "Microsoft.Features/providers/features/register/action",
                "Microsoft.Insights/alertRules/*",
                "Microsoft.Insights/components/*",
                "Microsoft.Insights/diagnosticSettings/*",
                "Microsoft.Insights/generateLiveToken/read",
                "Microsoft.Insights/logDefinitions/read",
                "Microsoft.Insights/metricAlerts/*",
                "Microsoft.Insights/metricdefinitions/read",
                "Microsoft.Insights/metrics/read",
                "Microsoft.Insights/scheduledqueryrules/*",
                "Microsoft.Insights/topology/read",
                "Microsoft.Insights/transactions/read",
                "Microsoft.Insights/webtests/*",
                "Microsoft.KeyVault/*",
                "Microsoft.MachineLearningServices/workspaces/*",
                "Microsoft.Network/virtualNetworks/subnets/joinViaServiceEndpoint/action",
                "Microsoft.ResourceHealth/availabilityStatuses/read",
                "Microsoft.Resources/deployments/*",
                "Microsoft.Resources/deployments/operations/read",
                "Microsoft.Resources/subscriptions/operationresults/read",
                "Microsoft.Resources/subscriptions/read",
                "Microsoft.Resources/subscriptions/resourcegroups/deployments/*",
                "Microsoft.Resources/subscriptions/resourceGroups/read",
                "Microsoft.Resources/subscriptions/resourceGroups/write",
                "Microsoft.Storage/storageAccounts/*",
                "Microsoft.Support/*",
                "Microsoft.Search/searchServices/write",
                "Microsoft.Search/searchServices/read",
                "Microsoft.Search/searchServices/delete",
                "Microsoft.Search/searchServices/indexes/*",
                "Microsoft.DataFactory/factories/*"
            ],
            "notActions": [],
            "dataActions": [],
            "notDataActions": []
        }
    ]
}
```

> [!TIP]
> We recommend that you convert hubs created before 11/19/2024 to use the Azure AI Administrator role. The Azure AI Administrator role is more narrowly scoped than the previously used Contributor role and follows the principal of least privilege.

You can convert hubs created before 11/19/2024 to use the new Azure AI Administrator role by using one of the following methods:

- Azure REST API: Use a `PATCH` request to the Azure REST API for the workspace. The body of the request should set `{"properties":{"allowRoleAssignmeentOnRG":true}}`. The following example shows a `PATCH` request using `curl`. Replace `<your-subscription>`, `<resource-group-name>`, `<workspace-name>`, and `<YOUR-ACCESS-TOKEN>` with the values for your scenario. For more information on using REST APIs, visit the [Azure REST API documentation](/rest/api/azure/).

    ```bash
    curl -X PATCH https://management.azure.com/subscriptions/<your-subscription>/resourcegroups/<resource-group-name>/providers/Microsoft.MachineLearningServices/workspaces/<workspace-name>?api-version=2024-04-01-preview -H "Authorization:Bearer <YOUR-ACCESS-TOKEN>"
    ```

- Azure CLI: Use the `az ml workspace update` command with the `--allow-roleassignment-on-rg true` parameter. The following example updates a workspace named `myworkspace`. This command requires the Azure Machine Learning CLI extension version 2.27.0 or later.

    ```azurecli
    az ml workspace update --name myworkspace --allow-roleassignment-on-rg true
    ```

- Azure Python SDK: Set the `allow_roleassignment_on_rg` property of the Workspace object to `True` and then perform an update operation. The following example updates a workspace named `myworkspace`. This operation requires the Azure Machine Learning SDK version 1.17.0 or later.

    ```python
    ws = ml_client.workspaces.get(name="myworkspace")
    ws.allow_roleassignment_on_rg = True
    ws = ml_client.workspaces.begin_update(workspace=ws).result()
    ```

If you encounter problems with the Azure AI Administrator role, you can revert to the Contributor role as a troubleshooting step. For more information, see [Revert to the Contributor role](#revert-to-the-contributor-role).

### Azure AI Developer role

The full set of permissions for the new "Azure AI Developer" role are as follows:

```json
{
    "Permissions": [ 
        { 
        "Actions": [
            "Microsoft.MachineLearningServices/workspaces/*/read",
            "Microsoft.MachineLearningServices/workspaces/*/action",
            "Microsoft.MachineLearningServices/workspaces/*/delete",
            "Microsoft.MachineLearningServices/workspaces/*/write",
            "Microsoft.MachineLearningServices/locations/*/read",
            "Microsoft.Authorization/*/read",
            "Microsoft.Resources/deployments/*"
        ],
    
        "NotActions": [
            "Microsoft.MachineLearningServices/workspaces/delete",
            "Microsoft.MachineLearningServices/workspaces/write",
            "Microsoft.MachineLearningServices/workspaces/listKeys/action",
            "Microsoft.MachineLearningServices/workspaces/hubs/write",
            "Microsoft.MachineLearningServices/workspaces/hubs/delete",
            "Microsoft.MachineLearningServices/workspaces/featurestores/write",
            "Microsoft.MachineLearningServices/workspaces/featurestores/delete"
        ], 
        "DataActions": [ 
            "Microsoft.CognitiveServices/accounts/OpenAI/*", 
            "Microsoft.CognitiveServices/accounts/SpeechServices/*", 
            "Microsoft.CognitiveServices/accounts/ContentSafety/*" 
        ], 
        "NotDataActions": [], 
        "Condition": null, 
        "ConditionVersion": null 
        } 
    ] 
}
```

If the built-in Azure AI Developer role doesn't meet your needs, you can create a [custom role](#create-custom-roles).

## Default roles for projects 

Projects in Azure AI Foundry portal have built-in roles that are available by default. 

Here's a table of the built-in roles and their permissions for the project:

| Role | Description | 
| --- | --- |
| Owner | Full access to the project, including the ability to assign permissions to project users. |
| Contributor |    User has full access to the project but can't assign permissions to project users. |
| Azure AI Administrator (preview) | This role is automatically assigned to the system-assigned managed identity for the hub. The Azure AI Administrator role has the minimum permissions needed for the managed identity to perform its tasks. For more information, see [Azure AI Administrator role (preview)](#azure-ai-administrator-role-preview). |
| Azure AI Developer |     User can perform most actions, including create deployments, but can't assign permissions to project users. |
| Azure AI Inference Deployment Operator | Perform all actions required to create a resource deployment within a resource group. |
| Reader |     Read only access to the project. |

When a user is granted access to a project (for example, through the Azure AI Foundry portal permission management), two more roles are automatically assigned to the user. The first role is Reader on the hub. The second role is the Inference Deployment Operator role, which allows the user to create deployments on the resource group that the project is in. This role is composed of these two permissions: ```"Microsoft.Authorization/*/read"``` and    ```"Microsoft.Resources/deployments/*"```.

In order to complete end-to-end AI development and deployment, users only need these two autoassigned roles and either the Contributor or Azure AI Developer role on a project.

The minimum permissions needed to create a project is a role that has the allowed action of `Microsoft.MachineLearningServices/workspaces/hubs/join` on the hub. The Azure AI Developer built-in role has this permission.

## Dependency service Azure RBAC permissions

The hub has dependencies on other Azure services. The following table lists the permissions required for these services when you create a hub. The person that creates the hub needs these permissions. The person who creates a project from the hub doesn't need them.

| Permission | Purpose |
|------------|-------------|
| `Microsoft.Storage/storageAccounts/write` | Create a storage account with the specified parameters or update the properties or tags or adds custom domain for the specified storage account. |
| `Microsoft.KeyVault/vaults/write` | Create a new key vault or updates the properties of an existing key vault. Certain properties might require more permissions. |
| `Microsoft.CognitiveServices/accounts/write` | Write API Accounts. |
| `Microsoft.MachineLearningServices/workspaces/write` | Create a new workspace or updates the properties of an existing workspace. |

## Sample enterprise RBAC setup
The following table is an example of how to set up role-based access control for your Azure AI Foundry for an enterprise.

| Persona | Role | Purpose |
| --- | --- | ---|
| IT admin | Owner of the hub | The IT admin can ensure the hub is set up to their enterprise standards. They can assign managers the Contributor role on the resource if they want to enable managers to make new hubs. Or they can assign managers the Azure AI Developer role on the resource to not allow for new hub creation. |
| Managers | Contributor or Azure AI Developer on the hub | Managers can manage the hub, audit compute resources, audit connections, and create shared connections. |
| Team lead/Lead developer | Azure AI Developer on the hub | Lead developers can create projects for their team and create shared resources (such as compute and connections) at the hub level. After project creation, project owners can invite other members. |
| Team members/developers | Contributor or Azure AI Developer on the project | Developers can build and deploy AI models within a project and create assets that enable development such as computes and connections. |

## Access to resources created outside of the hub

When you create a hub, the built-in role-based access control permissions grant you access to use the resource. However, if you wish to use resources outside of what was created on your behalf, you need to ensure both: 
- The resource you're trying to use has permissions set up to allow you to access it.
- Your hub is allowed to access it. 

For example, if you're trying to consume a new Blob storage, you need to ensure that hub's managed identity is added to the Blob Storage Reader role for the Blob. If you're trying to use a new Azure AI Search source, you might need to add the hub to the Azure AI Search's role assignments. 

## Manage access with roles 

If you're an owner of a hub, you can add and remove roles for Azure AI Foundry. Go to the **Home** page in [Azure AI Foundry](https://ai.azure.com) and select your hub. Then select **Users** to add and remove users for the hub. You can also manage permissions from the Azure portal under **Access Control (IAM)** or through the Azure CLI. For example, use the [Azure CLI](/cli/azure/) to assign the Azure AI Developer role to "joe@contoso.com" for resource group "this-rg" with the following command: 
 
```azurecli-interactive
az role assignment create --role "Azure AI Developer" --assignee "joe@contoso.com" --resource-group this-rg 
```

## Create custom roles

If the built-in roles are insufficient, you can create custom roles. Custom roles might have the read, write, delete, and compute resource permissions in that Azure AI Foundry. You can make the role available at a specific project level, a specific resource group level, or a specific subscription level. 

> [!NOTE]
> You must be an owner of the resource at that level to create custom roles within that resource.

The following JSON example defines a custom Azure AI Foundry developer role at the subscription level:

```json
{
    "properties": {
        "roleName": "Azure AI Foundry Developer",
        "description": "Custom role for Azure AI Foundry. At subscription level",
        "assignableScopes": [
            "/subscriptions/<your-subscription-id>"
        ],
        "permissions": [
            {
                "actions": [
                    "Microsoft.MachineLearningServices/workspaces/write",
                    "Microsoft.MachineLearningServices/workspaces/endpoints/write",
                    "Microsoft.Storage/storageAccounts/write",
                    "Microsoft.Resources/deployments/validate/action",
                    "Microsoft.KeyVault/vaults/write",
                    "Microsoft.Authorization/roleAssignments/read",
                    "Microsoft.Authorization/roleDefinitions/read",
                    "Microsoft.CognitiveServices/*/read"
                ],
                "notActions": [
                    "Microsoft.MachineLearningServices/workspaces/delete",
                    "Microsoft.MachineLearningServices/workspaces/write",
                    "Microsoft.MachineLearningServices/workspaces/listKeys/action",
                    "Microsoft.MachineLearningServices/workspaces/hubs/write",
                    "Microsoft.MachineLearningServices/workspaces/hubs/delete",
                    "Microsoft.MachineLearningServices/workspaces/featurestores/write",
                    "Microsoft.MachineLearningServices/workspaces/featurestores/delete"
                ],
                "dataActions": [
                    "Microsoft.CognitiveServices/accounts/OpenAI/*/read",
                    "Microsoft.CognitiveServices/accounts/OpenAI/engines/completions/action",
                    "Microsoft.CognitiveServices/accounts/OpenAI/engines/search/action",
                    "Microsoft.CognitiveServices/accounts/OpenAI/engines/generate/action",
                    "Microsoft.CognitiveServices/accounts/OpenAI/deployments/search/action",
                    "Microsoft.CognitiveServices/accounts/OpenAI/deployments/completions/action",
                    "Microsoft.CognitiveServices/accounts/OpenAI/deployments/chat/completions/action",
                    "Microsoft.CognitiveServices/accounts/OpenAI/deployments/extensions/chat/completions/action",
                    "Microsoft.CognitiveServices/accounts/OpenAI/deployments/embeddings/action",
                    "Microsoft.CognitiveServices/accounts/OpenAI/images/generations/action"
                ],
                "notDataActions": []
            }
        ]
    }
}
```

For steps on creating a custom role, use one of the following articles:
- [Azure portal](/azure/role-based-access-control/custom-roles-portal)
- [Azure CLI](/azure/role-based-access-control/custom-roles-cli)
- [Azure PowerShell](/azure/role-based-access-control/custom-roles-powershell)

For more information on creating custom roles in general, visit the [Azure custom roles](/azure/role-based-access-control/custom-roles) article.

## Assigning roles in Azure AI Foundry portal

You can add users and assign roles directly from Azure AI Foundry at either the hub or project level. In the [management center](management-center.md), select **Users** in either the hub or project section, then select **New user** to add a user. 

> [!NOTE]
> You're limited to selecting built-in roles. If you need to assign custom roles, you must use the [Azure portal](/azure/role-based-access-control/role-assignments-portal), [Azure CLI](/azure/role-based-access-control/role-assignments-cli), or [Azure PowerShell](/azure/role-based-access-control/role-assignments-powershell).

:::image type="content" source="../media/concepts/hub-overview-add-user.png" lightbox="../media/concepts/hub-overview-add-user.png" alt-text="Screenshot of the Azure AI Foundry hub overview with the new user button highlighted.":::

You're then prompted to enter the user information and select a built-in role.

:::image type="content" source="../media/concepts/add-resource-users.png" lightbox="../media/concepts/add-resource-users.png" alt-text="Screenshot of the add users prompt with the role set to Azure AI Developer.":::

## Scenario: Use a customer-managed key

When configuring a hub to use a customer-managed key (CMK), an Azure Key Vault is used to store the key. The user or service principal used to create the workspace must have owner or contributor access to the key vault.

If your Azure AI Foundry hub is configured with a **user-assigned managed identity**, the identity must be granted the following roles. These roles allow the managed identity to create the Azure Storage, Azure Cosmos DB, and Azure Search resources used when using a customer-managed key:

- `Microsoft.Storage/storageAccounts/write`
- `Microsoft.Search/searchServices/write`
- `Microsoft.DocumentDB/databaseAccounts/write`

Within the key vault, the user or service principal must have the create, get, delete, and purge access to the key through a key vault access policy. For more information, see [Azure Key Vault security](/azure/key-vault/general/security-features#controlling-access-to-key-vault-data).

## Scenario: Connections using Microsoft Entra ID authentication

When you create a connection that uses Microsoft Entra ID authentication, you must assign roles to your developers so they can access the resource.

| Resource connection | Role | Description |
|----------|------|-------------|
| Azure AI Search | Contributor | List API-Keys to list indexes from Azure AI Foundry. |
| Azure AI Search | Search Index Data Contributor | Required for indexing scenarios |
| Azure AI services / Azure OpenAI | Cognitive Services OpenAI Contributor | Call public ingestion API from Azure AI Foundry. |
| Azure AI services / Azure OpenAI | Cognitive Services User | List API-Keys from Azure AI Foundry. |
| Azure AI services / Azure OpenAI | Cognitive Services Contributor | Allows for calls to the control plane. |
| Azure Blob Storage | Storage Blob Data Contributor | Required for reading and writing data to the blob storage. |
| Azure Data Lake Storage Gen 2 | Storage Blob Data Contributor | Required for reading and writing data to the data lake. |
| Microsoft OneLake | Contributor | To give someone access to Microsoft OneLake, you must [give them access to your Microsoft Fabric workspace](/fabric/get-started/give-access-workspaces). |

> [!IMPORTANT]
> If you're using Promptflow with Azure Storage (including Azure Data Lake Storage Gen 2), you must also assign the __Storage File Data Privileged Contributor__ role.

When using Microsoft Entra ID authenticated connections in the chat playground, the services need to authorize each other to access the required resources. The admin performing the configuration needs to have the __Owner__ role on these resources to add role assignments. The following table lists the required role assignments for each resource. The __Assignee__ column refers to the system-assigned managed identity of the listed resource. The __Resource__ column refers to the resource that the assignee needs to access. For example, Azure OpenAI has a system-assigned managed identity that needs to be assigned the __Search Index Data Reader__ role for the Azure AI Search resource.

| Role | Assignee | Resource | Description |
|------|----------|----------|-------------|
| Search Index Data Reader | Azure AI services / Azure OpenAI | Azure AI Search | Inference service queries the data from the index. Only used for inference scenarios. |
| Search Index Data Contributor | Azure AI services / Azure OpenAI | Azure AI Search | Read-write access to content in indexes. Import, refresh, or query the documents collection of an index. Only used for ingestion and inference scenarios. |
| Search Service Contributor | Azure AI services / Azure OpenAI | Azure AI Search | Read-write access to object definitions (indexes, aliases, synonym maps, indexers, data sources, and skillsets). Inference service queries the index schema for auto fields mapping. Data ingestion service creates index, data sources, skill set, indexer, and queries the indexer status. |
| Cognitive Services OpenAI Contributor | Azure AI Search | Azure AI services / Azure OpenAI | Custom skill |
| Cognitive Services OpenAI User | Azure OpenAI Resource for chat model | Azure OpenAI resource for embedding model | Required only if using two Azure OpenAI resources to communicate. |
| Storage Blob Data Contributor | Azure AI Search | Azure Storage Account | Reads blob and writes knowledge store. |
| Storage Blob Data Contributor | Azure AI services / Azure OpenAI | Azure Storage Account | Reads from the input container and writes the preprocess results to the output container. |

> [!NOTE]
> The __Cognitive Services OpenAI User__ role is only required if you're using two Azure OpenAI resources: one for your chat model and one for your embedding model. If this applies, enable Trusted Services AND ensure the connection for your embedding model Azure OpenAI resource has Microsoft Entra ID enabled.  

## Scenario: Use an existing Azure OpenAI resource

When you create a connection to an existing Azure OpenAI resource, you must also assign roles to your users so they can access the resource. You should assign either the **Cognitive Services OpenAI User** or **Cognitive Services OpenAI Contributor** role, depending on the tasks they need to perform. For information on these roles and the tasks they enable, see [Azure OpenAI roles](/azure/ai-services/openai/how-to/role-based-access-control#azure-openai-roles).

## Scenario: Use Azure Container Registry

An Azure Container Registry instance is an optional dependency for Azure AI Foundry hub. The following table lists the support matrix when authenticating a hub to Azure Container Registry, depending on the authentication method and the __Azure Container Registry's__ [public network access configuration](/azure/container-registry/container-registry-access-selected-networks). 

| Authentication method | Public network access </br>disabled | Azure Container Registry</br>Public network access enabled |
| ---- | :----: | :----: |
| Admin user | ✓ | ✓ |
| Azure AI Foundry hub system-assigned managed identity | ✓ | ✓ |
| Azure AI Foundry hub user-assigned managed identity </br>with the **ACRPull** role assigned to the identity |  | ✓ |

A system-assigned managed identity is automatically assigned to the correct roles when the hub is created. If you're using a user-assigned managed identity, you must assign the **ACRPull** role to the identity.

## Scenario: Use Azure Application Insights for logging

Azure Application Insights is an optional dependency for Azure AI Foundry hub. The following table lists the permissions required if you want to use Application Insights when you create a hub. The person that creates the hub needs these permissions. The person who creates a project from the hub doesn't need these permissions.

| Permission | Purpose |
|------------|-------------|
| `Microsoft.Insights/Components/Write` | Write to an application insights component configuration. |
| `Microsoft.OperationalInsights/workspaces/write` | Create a new workspace or links to an existing workspace by providing the customer ID from the existing workspace. |

## Scenario: Provisioned throughput unit procurer

The following example defines a custom role that can procure [provisioned throughput units (PTU)](/azure/ai-services/openai/concepts/provisioned-throughput).

```json
{
    "properties": {
        "roleName": "PTU procurer",
        "description": "Custom role to purchase PTU",
        "assignableScopes": [
            "/subscriptions/<your-subscription-id>"
        ],
        "permissions": [
            {
                "actions": [
                    "Microsoft.CognitiveServices/accounts/commitmentplans/read",
                    "Microsoft.CognitiveServices/accounts/commitmentplans/write",
                    "Microsoft.CognitiveServices/accounts/commitmentplans/delete",
                    "Microsoft.CognitiveServices/locations/commitmentTiers/read",
                    "Microsoft.CognitiveServices/accounts/commitmentplans/read",
                    "Microsoft.CognitiveServices/accounts/commitmentplans/write",
                    "Microsoft.CognitiveServices/accounts/commitmentplans/delete",
                    "Microsoft.Features/features/read",
                    "Microsoft.Features/providers/features/read",
                    "Microsoft.Features/providers/features/register/action",
                    "Microsoft.Insights/logDefinitions/read",
                    "Microsoft.Insights/metricdefinitions/read",
                    "Microsoft.Insights/metrics/read",
                    "Microsoft.ResourceHealth/availabilityStatuses/read",
                    "Microsoft.Resources/deployments/operations/read",
                    "Microsoft.Resources/subscriptions/operationresults/read",
                    "Microsoft.Resources/subscriptions/read",
                    "Microsoft.Resources/subscriptions/resourcegroups/deployments/*",
                    "Microsoft.Resources/subscriptions/resourceGroups/read"
                ],
                "notActions": [],
                "dataActions": [],
                "notDataActions": []
            }
        ]
    }
}
```

## Scenario: Azure OpenAI Assistants API

The following example defines a role for a developer using [Azure OpenAI Assistants](/azure/ai-services/openai/how-to/assistant).

```json
{
    "id": "",
    "properties": {
        "roleName": "Azure OpenAI Assistants API Developer",
        "description": "Custom role to work with Azure OpenAI Assistants API",
        "assignableScopes": [
            "<your-scope>"
        ],
        "permissions": [
            {
                "actions": [
                    "Microsoft.CognitiveServices/*/read",
                    "Microsoft.Authorization/roleAssignments/read",
                    "Microsoft.Authorization/roleDefinitions/read"
                ],
                "notActions": [],
                "dataActions": [
                    "Microsoft.CognitiveServices/accounts/OpenAI/*/read",
                    "Microsoft.CognitiveServices/accounts/OpenAI/engines/completions/action",
                    "Microsoft.CognitiveServices/accounts/OpenAI/engines/search/action",
                    "Microsoft.CognitiveServices/accounts/OpenAI/engines/generate/action",
                    "Microsoft.CognitiveServices/accounts/OpenAI/deployments/search/action",
                    "Microsoft.CognitiveServices/accounts/OpenAI/deployments/completions/action",
                    "Microsoft.CognitiveServices/accounts/OpenAI/deployments/chat/completions/action",
                    "Microsoft.CognitiveServices/accounts/OpenAI/deployments/extensions/chat/completions/action",
                    "Microsoft.CognitiveServices/accounts/OpenAI/deployments/embeddings/action",
                    "Microsoft.CognitiveServices/accounts/OpenAI/images/generations/action",
                    "Microsoft.CognitiveServices/accounts/OpenAI/assistants/write",
                    "Microsoft.CognitiveServices/accounts/OpenAI/assistants/read",
                    "Microsoft.CognitiveServices/accounts/OpenAI/assistants/delete",
                    "Microsoft.CognitiveServices/accounts/OpenAI/assistants/files/write",
                    "Microsoft.CognitiveServices/accounts/OpenAI/assistants/files/read",
                    "Microsoft.CognitiveServices/accounts/OpenAI/assistants/files/delete",
                    "Microsoft.CognitiveServices/accounts/OpenAI/assistants/threads/write",
                    "Microsoft.CognitiveServices/accounts/OpenAI/assistants/threads/read",
                    "Microsoft.CognitiveServices/accounts/OpenAI/assistants/threads/delete",
                    "Microsoft.CognitiveServices/accounts/OpenAI/assistants/threads/messages/write",
                    "Microsoft.CognitiveServices/accounts/OpenAI/assistants/threads/messages/read",
                    "Microsoft.CognitiveServices/accounts/OpenAI/assistants/threads/messages/files/read",
                    "Microsoft.CognitiveServices/accounts/OpenAI/assistants/threads/runs/write",
                    "Microsoft.CognitiveServices/accounts/OpenAI/assistants/threads/runs/read",
                    "Microsoft.CognitiveServices/accounts/OpenAI/assistants/threads/runs/steps/read"
                ],
                "notDataActions": []
            }
        ]
    }
}
```

## Troubleshooting

### Error: Principal doesn't have access to API/Operation

#### Symptoms

When using the Azure AI Foundry portal chat playground, you receive an error message stating "Principal doesn't have access to API/Operation". The error might also include an "Apim-request-id".

#### Cause

The user or service principal used to authenticate requests to Azure OpenAI or Azure AI Search doesn't have the required permissions to access the resource.

#### Solution

Assign the following roles to the user or service principal. The role you assign depends on the services you're using and the level of access the user or service principal requires:

| Service being accessed | Role | Description |
| --- | --- | --- |
| Azure OpenAI | Cognitive Services OpenAI Contributor | Call public ingestion API from Azure AI Foundry. |
| Azure OpenAI | Cognitive Services User | List API-Keys from Azure AI Foundry. |
| Azure AI Search | Search Index Data Contributor | Required for indexing scenarios. |
| Azure AI Search| Search Index Data Reader | Inference service queries the data from the index. Only used for inference scenarios. |

### Revert to the Contributor role

If you create a new hub and encounter errors with the new default role assignment of Azure AI Administrator for the managed identity, use the following steps to change the hub to the Contributor role:

> [!IMPORTANT]
> We don't recommend reverting a hub to the Contributor role unless you encounter problems. If reverting does solve the problems that you're encountering, open a support incident with information on the problems that reverting solved so that we can invesitage further.
>
> If you would like to revert to the Contributor role as the _default_ for new hubs, open a [support request](https://ms.portal.azure.com/#view/Microsoft_Azure_Support/NewSupportRequestV3Blade) with your Azure subscription details and request that your subscription be changed to use the Contributor role as the default for the system-assigned managed identity of new hubs.

1. Delete the role assignment for the hub's managed-identity. The scope for this role assignment is the __resource group__ that contains the hub, so the role must be deleted from the resource group. 

    > [!TIP]
    > The system-assigned managed identity for the hub is the same as the hub name.

    From the Azure portal, navigate to the __resource group__ that contains the hub. Select __Access control (IAM)__, and then select __Role assignments__. In the list of role assignments, find the role assignment for the managed identity. Select it, and then select __Delete__.

    For information on deleting a role assignment, see [Remove role assignments](/azure/role-based-access-control/role-assignments-remove).

1. Create a new role assignment on the __resource group__ for the __Contributor__ role. When adding this role assignment, select the managed-identity for the hub as the assignee. The name of the system-assigned managed identity is same as the hub name.

    1. From the Azure portal, navigate to the __resource group__ that contains the hub. Select __Access control (IAM)__, and then select __Add role assignment__. 
    1. From the __Role__ tab, select __Contributor__. 
    1. From the __Members__ tab, select __Managed identity__, __+ Select members__, and set the __Managed identity__ dropdown to __Azure AI hub__. In the __Select__ field, enter the name of the hub. Select the hub from the list, and then select __Select__.
    1. From the __Review + assign__ tab, select __Review + assign__.

## Next steps

- [How to create an Azure AI Foundry hub](../how-to/create-azure-ai-resource.md)
- [How to create an Azure AI Foundry project](../how-to/create-projects.md)
- [How to create a connection in Azure AI Foundry portal](../how-to/connections-add.md)
