---
title: What is secret injection in online endpoints (preview)?
titleSuffix: Azure Machine Learning
description: Learn about secret injection as it applies to online endpoints in Azure Machine Learning.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: inferencing
ms.topic: concept-article
author: s-polly
ms.author: scottpolly
ms.reviewer: jturuk
ms.custom: ignite-2023
ms.date: 11/24/2025

#CustomerIntent: As an ML Pro, I want to retrieve and inject secrets into the deployment environment easily so that deployments I create can consume the secrets in a secured manner.
---

# Secret injection in online endpoints (preview)

[!INCLUDE [dev v2](includes/machine-learning-dev-v2.md)]

Secret injection in online endpoints helps you securely use API keys and other secrets in your deployments without exposing them in your code. This article explains:

- Why secret injection matters for secure deployments
- How to use managed identities to retrieve secrets
- How the secret injection feature simplifies the process

By the end, you'll understand which approach works best for your scenario.

Secret injection in the context of an online endpoint is a process of retrieving secrets, such as API keys, from secret stores and injecting them into your user container that runs inside an online deployment. The inference server that runs your scoring script or the inferencing stack that you bring with a BYOC (bring your own container) deployment approach securely accesses secrets through environment variables.

[!INCLUDE [machine-learning-preview-generic-disclaimer](includes/machine-learning-preview-generic-disclaimer.md)]

## Problem statement

When you create an online deployment, you might want to use secrets from within the deployment to access external services. Some of these external services include Microsoft Azure OpenAI service, Foundry Tools, and Azure AI Content Safety.

To use the secrets, you need a way to securely pass them to your user container that runs inside the deployment. Don't include secrets as part of the deployment definition, since this practice exposes the secrets in the deployment definition. 

A better approach is to store the secrets in secret stores and then retrieve them securely from within the deployment. However, this approach poses its own challenge: how the deployment should authenticate itself to the secret stores to retrieve secrets. Because the online deployment runs your user container by using the _endpoint identity_, which is a [managed identity](/entra/identity/managed-identities-azure-resources/overview), you can use [Azure RBAC](/azure/role-based-access-control/overview) to control the endpoint identity's permissions and allow the endpoint to retrieve secrets from the secret stores.
Using this approach requires you to complete the following tasks:

- Assign the right roles to the endpoint identity so that it can read secrets from the secret stores.
- Implement the scoring logic for the deployment so that it uses the endpoint's managed identity to retrieve the secrets from the secret stores.

While this approach of using a managed identity is a secure way to retrieve and inject secrets, [secret injection via the secret injection feature](#secret-injection-via-the-secret-injection-feature) further simplifies the process of retrieving secrets for [workspace connections](prompt-flow/concept-connections.md) and [key vaults](/azure/key-vault/general/overview).


## Managed identity associated with the endpoint


An online deployment runs your user container with the managed identity associated with the endpoint. This managed identity, called the _endpoint identity_, is a [Microsoft Entra ID](/entra/fundamentals/whatis) that supports [Azure RBAC](/azure/role-based-access-control/overview). Therefore, you can assign Azure roles to the identity to control permissions that are required to perform operations. The endpoint identity can be either a system-assigned identity (SAI) or a user-assigned identity (UAI). You decide which of these kinds of identities to use when you create the endpoint.

- For a _system-assigned identity_, the identity is created automatically when you create the endpoint, and roles with fundamental permissions (such as the Azure Container Registry pull permission and the storage blob data reader) are automatically assigned.
- For a _user-assigned identity_, you need to create the identity first, and then associate it with the endpoint when you create the endpoint. You're also responsible for assigning proper roles to the UAI as needed.

For more information on using managed identities of an endpoint, see [How to access resources from endpoints with managed identities](how-to-access-resources-from-endpoints-managed-identities.md), and the example for [using managed identities to interact with external services](https://github.com/Azure/azureml-examples/tree/main/cli/endpoints/online/managed/managed-identities).


## Role assignment to the endpoint identity

The following roles are required by the secret stores:

- For __secrets stored in workspace connections under your workspace__: `Workspace Connections` provides a [List Secrets API (preview)](/rest/api/azureml/2023-08-01-preview/workspace-connections/list-secrets) that requires the identity that calls the API to have `Azure Machine Learning Workspace Connection Secrets Reader` role (or equivalent) assigned to the identity.
- For __secrets stored in an external Microsoft Azure Key Vault__: Key Vault provides a [Get Secret Versions API](/rest/api/keyvault/secrets/get-secret-versions/get-secret-versions) that requires the identity that calls the API to have `Key Vault Secrets User` role (or equivalent) assigned to the identity.


## Implementation of secret injection

After you retrieve secrets, such as API keys, from secret stores, you can inject them into a user container that runs inside the online deployment in two ways:

- **[Inject secrets yourself, by using managed identities](#secret-injection-by-using-managed-identities)** - For maximum control and flexibility
- **[Inject secrets, by using the secret injection feature](#secret-injection-via-the-secret-injection-feature)** - For a simplified, code-free approach

Choose the approach that best fits your security requirements and development workflow.

Both approaches involve two steps:

1. Retrieve secrets from the secret stores, by using the endpoint identity.
1. Inject the secrets into your user container.

### Secret injection by using managed identities

In your deployment definition, use the endpoint identity to call the APIs from secret stores. You can implement this logic either in your scoring script or in shell scripts that you run in your BYOC container. For more information about implementing secret injection by using managed identities, see the [example for using managed identities to interact with external services](https://github.com/Azure/azureml-examples/tree/main/cli/endpoints/online/managed/managed-identities).

### Secret injection via the secret injection feature

To use the secret injection feature, map the secrets you want to refer to from workspace connections or the Key Vault onto the environment variables in your deployment definition. This approach doesn't require you to write any code in your scoring script or in shell scripts that you run in your BYOC container. To map the secrets from workspace connections or the Key Vault onto the environment variables, the following conditions must be met:

- During endpoint creation, if you define an online endpoint to enforce access to default secret stores (workspace connections under the current workspace), your user identity that creates the deployment under the endpoint must have the permissions to read secrets from workspace connections.
- The endpoint identity that the deployment uses must have permissions to read secrets from either workspace connections or the Key Vault, as referenced in the deployment definition.

> [!NOTE]
> - If you successfully create the endpoint with an SAI and set the flag to enforce access to default secret stores, the endpoint automatically has permission for workspace connections. 
> - If the endpoint uses a UAI, or you don't set the flag to enforce access to default secret stores, the endpoint identity might not have permission for workspace connections. In this situation, you need to manually assign the role for the workspace connections to the endpoint identity.
> - The endpoint identity doesn't automatically receive permission for the external Key Vault. If you're using the Key Vault as a secret store, you need to manually assign the role for the Key Vault to the endpoint identity.

For more information on using secret injection, see [Deploy machine learning models to online endpoints with secret injection (preview)](how-to-deploy-online-endpoint-with-secret-injection.md).


## Next steps

Now that you understand secret injection concepts, learn how to implement it:

- **[Deploy with secret injection (preview)](how-to-deploy-online-endpoint-with-secret-injection.md)** - Step-by-step guide to implement secret injection in your deployments
- **[Authentication for managed online endpoints](concept-endpoints-online-auth.md)** - Understand authentication options for your endpoints
- **[Online endpoints overview](concept-endpoints-online.md)** - Learn the fundamentals of online endpoints

Ready to get started? Follow the [deployment guide](how-to-deploy-online-endpoint-with-secret-injection.md).
