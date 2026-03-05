---
title: Authentication and authorization for online endpoints
titleSuffix: Azure Machine Learning
description: Learn how authentication, authorization, and Azure role-based access control (RBAC) work for Azure Machine Learning online endpoints.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: inferencing
ms.topic: concept-article
author: s-polly
ms.author: scottpolly
ms.reviewer: jturuk
ms.custom: devplatv2, FY25Q1-Linter
ms.date: 11/14/2025
#Customer intent: As a data scientist, I want to learn how authentication and authorization work for Azure Machine Learning online endpoints so I can create and deploy online endpoints.
---

# Authentication and authorization for online endpoints

[!INCLUDE [machine-learning-dev-v2](includes/machine-learning-dev-v2.md)]

This article explains the concepts of identity and permission in the context of Azure Machine Learning online endpoints. The article discusses [Microsoft Entra IDs](/entra/fundamentals/whatis) that support role-based access control and permissions. A Microsoft Entra ID is called either a *user identity* or an *endpoint identity*, depending on its purpose.

- A user identity is a Microsoft Entra ID that can create an endpoint and its deployments, or interact with endpoints or workspaces. A user identity issues requests to endpoints, deployments, or workspaces. The user identity needs proper permissions to perform *control plane* and *data plane* operations on the endpoints or workspaces.

- An endpoint identity is a Microsoft Entra ID that runs the user container in deployments. The user container uses the endpoint identity for the deployment. The endpoint identity also needs proper permissions for the user container to interact with resources as needed. For example, the endpoint identity needs the proper permissions to pull images from Azure Container Registry or to interact with other Azure services.

The user identity and endpoint identity have separate permission requirements. For more information on managing identities and permissions, see [How to authenticate clients for online endpoints](how-to-authenticate-online-endpoint.md).

>[!IMPORTANT]
>Microsoft Entra ID `aad_token` authentication is supported for managed online endpoints only. For Kubernetes online endpoints, you can use either a key or an Azure Machine Learning `aml_token`.

## Permissions and scope for authorization

[Azure role-based access control (RBAC)](/azure/role-based-access-control/overview) allows you to define and assign **roles** with a set of allowed and/or denied **actions** on specific **scopes**. You can customize these roles and scopes according to your business needs. The following examples serve as a starting point that you can extend as necessary.

For user identity:

- To manage control plane and data plane operations, use the built-in role **AzureML Data Scientist** that includes the permission action `Microsoft.MachineLearningServices/workspaces/onlineEndpoints/*/actions`.
- To control the operations for a specific endpoint, use the scope `/subscriptions/<subscriptionId>/resourcegroups/<resourceGroupName>/providers/Microsoft.MachineLearningServices/workspaces/<workspaceName>/onlineEndpoints/<endpointName>`.
- To control the operations for all endpoints in a workspace, use the scope `/subscriptions/<subscriptionId>/resourcegroups/<resourceGroupName>/providers/Microsoft.MachineLearningServices/workspaces/<workspaceName>`.

For endpoint identity, to allow the user container to read blobs, use the built-in role **Storage Blob Data Reader** that includes the permission data action `Microsoft.Storage/storageAccounts/blobServices/containers/blobs/read`.

For more information on managing authorization to Azure Machine Learning workspaces, see [Manage access to Azure Machine Learning](how-to-assign-roles.md). For more information on role definition, scope, and role assignment, see [Azure RBAC](/azure/role-based-access-control/overview). To understand the scope for assigned roles, see [Understand scope for Azure RBAC](/azure/role-based-access-control/scope-overview).

## Permissions needed for user identity

When you sign in to your Azure tenant with your Microsoft account, for example by using `az login`, you complete the **authn** user authentication step that determines your identity as a user. To create an online endpoint under an Azure Machine Learning workspace, your identity needs the proper permission, also called authorization or **authz**. User identities need appropriate permissions to perform both [control plane](#control-plane-operations) and [data plane](#data-plane-operations) operations.

### Control plane operations

Control plane operations control and change the online endpoints. These operations include create, read, update, and delete (CRUD) operations on online endpoints and online deployments. For online endpoints and deployments, requests to perform control plane operations go to the Azure Machine Learning workspace.

#### Authentication for control plane operations

For control plane operations, use a Microsoft Entra token to authenticate a client to the workspace. Depending on your use case, choose from [several authentication workflows](how-to-setup-authentication.md) to get this token. The user identity also needs to have the proper Azure RBAC role assigned to access resources.

#### Authorization for control plane operations

For control plane operations, your user identity needs to have the proper Azure RBAC role assigned to access your resources. Specifically, for CRUD operations on online endpoints and deployments, the user identity needs to have roles assigned for the following actions:

| Operation | Required Azure RBAC role | Scope |
| --- | --- | --- |
| Perform create/update operations on online endpoints and deployments. | **Owner**, **Contributor**, or any role allowing `Microsoft.MachineLearningServices/workspaces/onlineEndpoints/write` | Workspace |
| Perform delete operations on online endpoints and deployments. | **Owner**, **Contributor**, or any role allowing `Microsoft.MachineLearningServices/workspaces/onlineEndpoints/delete` | Workspace |
| Perform create/update/delete operations on online endpoints and deployments via Azure Machine Learning studio. | **Owner**, **Contributor**, or any role allowing `Microsoft.Resources/deployments/write` | Resource group that contains the workspace |
| Perform read operations on online endpoints and deployments. | **Owner**, **Contributor**, or any role allowing `Microsoft.MachineLearningServices/workspaces/onlineEndpoints/read` | Workspace |
| Fetch an Azure Machine Learning token (`aml_token`) for invoking both managed and Kubernetes online endpoints from the workspace. | **Owner**, **Contributor**, or any role allowing `Microsoft.MachineLearningServices/workspaces/onlineEndpoints/token/action` | Endpoint |
| Fetch a key for invoking online endpoints (both managed and Kubernetes) from the workspace. | **Owner**, **Contributor**, or any role allowing `Microsoft.MachineLearningServices/workspaces/onlineEndpoints/listKeys/action` | Endpoint |
| Regenerate keys for both managed and Kubernetes online endpoints. | **Owner**, **Contributor**, or any role allowing `Microsoft.MachineLearningServices/workspaces/onlineEndpoints/regenerateKeys/action` | Endpoint |
| Fetch a Microsoft Entra `aad_token` for invoking managed online endpoints. | Doesn't require a role | Not applicable\*|

\* You can fetch your Microsoft Entra `aad_token` directly from Microsoft Entra ID once you sign in, so that operation doesn't require Azure RBAC permission on the workspace.

#### Permissions for user identity to enforce access to default secret stores

If you use the [secret injection](concept-secret-injection.md) feature, and you set the flag to enforce access to the default secret stores while creating endpoints, your user identity must have permission to read secrets from workspace connections.

An endpoint identity can be either a system-assigned identity (SAI) or a user-assigned identity (UAI). When you create the endpoint with a SAI and set the flag to enforce access to the default secret stores, a user identity must have permissions to read secrets from workspace connections when creating an endpoint and deployments. This restriction ensures that only a user identity with the permission to read secrets can grant the endpoint identity the permission to read secrets.

If a user identity that doesn't have permission to read secrets from workspace connections tries to create an endpoint or a deployment with a SAI, and the endpoint's flag is set to enforce access to the default secret stores, the endpoint, or deployment creation is rejected.

If you create the endpoint with a UAI, or the endpoint uses a SAI but you don't set the flag to enforce access to the default secret stores, the user identity doesn't need to be able to read secrets from workspace connections to create an endpoint or deployment. In this case, the endpoint identity isn't automatically granted the permission to read secrets, but you can manually grant this permission by assigning the proper role.

Regardless of whether the role assignment is automatic or manual, the secret retrieval and injection is triggered if you mapped the environment variables with secret references in the endpoint or deployment definition. The secret injection feature uses the endpoint identity to do the secret retrieval and injection. For more information on secret injection, see [Secret injection in online endpoints](concept-secret-injection.md).

### Data plane operations

Data plane operations don't change the online endpoints but use data that interacts with the endpoints. An example of a data plane operation is sending a scoring request to an online endpoint and getting a response from it. For online endpoints and deployments, requests to perform data plane operations go to the endpoint's scoring URI.

#### Authentication for data plane operations

For data plane operations, choose from the following ways to authenticate a client to send requests to an endpoint's scoring URI:

- Key
- Azure Machine Learning `aml_token`
- Microsoft Entra `aad_token`

For more information on how to authenticate clients for data plane operations, see [How to authenticate clients for online endpoints](how-to-authenticate-online-endpoint.md).

#### Authorization for data plane operations

For data plane operations, your user identity needs proper Azure RBAC roles to allow access to your resources only if the endpoint is set to use Microsoft Entra `aad_token`. For data plane operations on online endpoints and deployments, the user identity needs to have a role assigned with the following actions:

| Operation | Required Azure RBAC role | Scope |
| --- | --- | --- |
| Invoke online endpoints with `key` or Azure Machine Learning `aml_token`. | No role required. | Not applicable |
| Invoke managed online endpoints with Microsoft Entra `aad_token`. | **Owner**, **Contributor**, or any role allowing `Microsoft.MachineLearningServices/workspaces/onlineEndpoints/score/action` | Endpoint |
| Invoke Kubernetes online endpoints with Microsoft Entra `aad_token`. | Kubernetes online endpoint doesn't support Microsoft Entra token for data plane operations. | Not applicable |

## Permissions needed for endpoint identity

An online deployment runs your user container with the endpoint identity, which is the managed identity associated with the endpoint. The endpoint identity is a [Microsoft Entra ID](/entra/fundamentals/whatis) that supports Azure RBAC. Therefore, you can assign Azure roles to the endpoint identity to control permissions that are required to perform operations. This endpoint identity can be either a SAI or a UAI. You decide whether to use an SAI or a UAI when you create the endpoint.

- For an SAI, the identity is created automatically when you create the endpoint, and roles with fundamental permissions, such as the Container Registry pull permission **AcrPull** and the **Storage Blob Data Reader**, are automatically assigned.
- For a UAI, you need to create the identity first, then associate it with the endpoint when you create the endpoint. You're also responsible for assigning proper roles to the UAI as needed.

> [!IMPORTANT]
> If you configure your Container registry to use **[RBAC Registry + ABAC Repository Permissions](/azure/container-registry/container-registry-rbac-abac-repository-permissions?tabs=azure-portal)** 
>
> ![Screenshot showing an ABAC permission on container.](/azure/container-registry/media/container-registry-rbac-abac-repository-permissions/rbac-abac-repository-permissions-02-update-registry.png)
>
>In this case, some existing role assignments aren't honored or will have different effects, because a different set of ACR built-in roles apply to ABAC-enabled registries.
>
> For example, the **AcrPull**, **AcrPush**, and **AcrDelete** roles aren't honored in an ABAC-enabled registry.
> Instead, in ABAC-enabled registries, use the `Container Registry Repository Reader`, `Container Registry Repository Writer`, and `Container Registry Repository Contributor` roles to grant either registry-wide or repository-specific image permissions.
>
> Ensure that the SAI or the UAI of your endpoint has the **Container Registry Repository Contributor** role assigned on the Container registry.

### Automatic role assignment for endpoint identity

If the endpoint identity is an SAI, the following roles are assigned to the endpoint identity for convenience.

| Role | Description | Condition for automatic role assignment |
| --- | --- | --- |
| **AcrPull** | Allows the endpoint identity to pull images from the Azure Container Registry associated with the workspace | The endpoint identity is an SAI.
| **Storage Blob Data Reader** | Allows the endpoint identity to read blobs from the default datastore of the workspace | The endpoint identity is an SAI.
| **AzureML Metrics Writer (preview)** | Allows the endpoint identity to write metrics to the workspace | The endpoint identity is an SAI.
| **Azure Machine Learning Workspace Connection Secrets Reader** | Allows the endpoint identity to read secrets from workspace connections | The endpoint identity is an SAI and the endpoint creation has a flag to enforce access to the default secret stores. The user identity that creates the endpoint also has permission to read secrets from workspace connections.

- If the endpoint identity is an SAI, and the enforce flag isn't set or the user identity doesn't have permission to read secrets, there's no automatic role assignment for the **Azure Machine Learning Workspace Connection Secrets Reader** role. For more information, see [How to deploy online endpoint with secret injection](how-to-deploy-online-endpoint-with-secret-injection.md#create-an-endpoint).
- If the endpoint identity is a UAI, there's no automatic role assignment for the **Azure Machine Learning Workspace Connection Secrets Reader** role. In this case, you need to manually assign roles to the endpoint identity as needed.

For more information on the **Azure Machine Learning Workspace Connection Secrets Reader** role, see [Assign permissions to the identity](how-to-authenticate-online-endpoint.md#assign-permissions-to-the-identity).

## Related content

- [Set up authentication](how-to-setup-authentication.md)
- [How to authenticate to an online endpoint](how-to-authenticate-online-endpoint.md)
- [How to deploy an online endpoint](how-to-deploy-online-endpoints.md)
