---
title: Authentication and authorization in Microsoft Foundry
ms.service: azure-ai-foundry
ms.date: 02/02/2026
ms.reviewer: meerakurup
ms.author: jburchel
author: jonburchel
description: Learn how to authenticate and authorize access in Microsoft Foundry using Microsoft Entra ID and API keys. Explore RBAC, identity types, and best practices.
#customer intent: As an IT admin, I want to understand how to configure authentication and authorization in Microsoft Foundry so that I can secure access to resources and operations.
ms.topic: concept-article
ms.custom: dev-focus
ai-usage: ai-assisted
monikerRange: 'foundry-classic || foundry'
---

# Authentication and authorization in Microsoft Foundry

Authentication and authorization in Microsoft Foundry define how principals prove identity and gain permission to perform control plane and data plane operations. Foundry supports API key and Microsoft Entra ID token-based authentication. Microsoft Entra ID enables conditional access, managed identities, granular role-based access control (RBAC) actions, and least privilege scenarios. API keys remain available for rapid prototyping and legacy integration but lack per-user traceability. This article explains the control plane and data plane model, compares API key and Microsoft Entra ID authentication, maps identities to roles, and describes common least privilege scenarios.

> [!IMPORTANT]
> Use Microsoft Entra ID for production workloads to enable conditional access, managed identities, and least privilege RBAC. API keys are convenient for quick evaluation but provide coarse-grained access.

## Prerequisites

- An Azure subscription. If you don't have one, [create a free account](https://azure.microsoft.com/free/).
- A Microsoft Foundry resource with a [custom subdomain](/azure/ai-services/cognitive-services-custom-subdomains) configured.
- Understanding of [Azure RBAC concepts](/azure/role-based-access-control/overview).
- To assign roles, you need the **Owner** role or **User Access Administrator** role at the appropriate scope.
- (Optional) The [Azure CLI](/cli/azure/install-azure-cli) or [Azure SDK for Python](https://pypi.org/project/azure-identity/) installed for programmatic authentication.

## Control plane and data plane

Azure operations divide into two categories: control plane and data plane. Azure separates resource management (control plane) from operational runtime (data plane). Therefore, you use the control plane to manage resources in your subscription and use the data plane to use capabilities exposed by your instance of a resource type. To learn more about control plane and data plane, see [Azure control plane and data plane](/azure/azure-resource-manager/management/control-plane-and-data-plane).
In Foundry, there's a clear distinction between control plane operations versus data plane operations. The following table explains the difference between the two, the scope in Foundry, typical operations of a user, example tools and features, and the authorization surface to use each.

| Plane | Scope in Foundry | Typical operations | Example tools | Authorization surface |
| --- | --- | --- | --- | --- |
| Control plane | Setting up and configuring resource, projects, networking, encryption, and connections | Create or delete resources, assign roles, rotate keys, set up Private Link | Azure portal, Azure CLI, ARM templates, Bicep, Terraform | Azure RBAC actions |
| Data plane | Running and using model inference, agent interactions, evaluation jobs, and content safety calls | Chat completions, embedding generation, start fine-tune jobs, send agent messages, analyzer and classifier operations | SDKs, REST APIs, Foundry portal playground | Azure RBAC dataActions |

For all Bicep, Terraform, and SDK samples, see the [foundry-samples repository on GitHub](https://github.com/azure-ai-foundry/foundry-samples) for Foundry.


### Control plane and data plane diagram
Within Foundry, there's a clear separation between control plane and data plane actions.
Control plane actions within Foundry include:
* Foundry resource creation
* Foundry project creation
* Account Capability Host creation
* Project Capability Host creation
* Model deployment
* Account and project connection creation

Data plane actions within Foundry include:
* Building agents
* Running an evaluation
* Tracing and monitoring
* Fine-tuning

The following diagram shows the view of control plane versus data plane separation in Foundry alongside role-based access control (RBAC) assignments and what access a user might have in either the control plane or data plane or both. As seen in the diagram, RBAC "actions" are associated with control plane while RBAC "dataActions" are associated with data plane. 

:::image type="content" source="../media/authentication-authorization/foundry-rbac-control-data-separation.png" alt-text="Diagram illustrating separation of control plane and data plane operations with associated RBAC surfaces." lightbox="../media/authentication-authorization/foundry-rbac-control-data-separation.png":::

## Authentication methods

Foundry supports Microsoft Entra ID (token-based, keyless) and API keys.

### Microsoft Entra ID

Microsoft Entra ID uses OAuth 2.0 bearer tokens scoped to `https://cognitiveservices.azure.com/.default`.

Use Microsoft Entra ID for:
- Production workloads.
- Conditional access, multifactor authentication (MFA), and just-in-time access.
- Least privilege RBAC and managed identity integration.

Advantages: Fine-grained role assignments, per-principal auditing, controllable token lifetimes, automatic secret hygiene, and managed identities for services.

Limitations: Higher initial setup complexity. Requires understanding of role-based access control (RBAC). For more on RBAC in Foundry, see [Role-based access control for Microsoft Foundry](rbac-foundry.md).

### API keys

API keys are static secrets scoped to a Foundry resource.

Use API keys for:
- Rapid prototyping.
- Isolated test environments where single-secret rotation is acceptable.

Advantages: Simple, language agnostic, and doesn't require token acquisition.

Limitations: Can't express user identity, is difficult to scope granularly, and is harder to audit. Generally not accepted by enterprise production workloads and not recommended by Microsoft. 

For more information on enabling keyless authentication, see [Configure key-less authentication with Microsoft Entra ID](../foundry-models/how-to/configure-entra-id.md).

### Authenticate with Microsoft Entra ID (Python)

The following example shows how to authenticate with Microsoft Entra ID by using the `azure-identity` library and make a request to a Foundry endpoint:

```python
from azure.identity import DefaultAzureCredential
import requests

# Create a credential object using DefaultAzureCredential
# This automatically uses environment variables, managed identity, or Azure CLI credentials
credential = DefaultAzureCredential()

# Get an access token for the Cognitive Services scope
token = credential.get_token("https://cognitiveservices.azure.com/.default")

# Use the token in your API request
headers = {
    "Authorization": f"Bearer {token.token}",
    "Content-Type": "application/json"
}

# Replace with your Foundry endpoint
endpoint = "https://<your-resource-name>.cognitiveservices.azure.com"

# Example: List deployments (adjust the path for your specific API)
response = requests.get(f"{endpoint}/openai/deployments?api-version=2024-10-21", headers=headers)
print(response.json())
```

**Expected output**: A JSON response listing your model deployments, or an authentication error if credentials are missing or the role assignment isn't configured.

**Reference**: [DefaultAzureCredential](/python/api/azure-identity/azure.identity.defaultazurecredential) | [azure-identity library](/python/api/overview/azure/identity-readme)

### Authenticate with an API key (Python)

The following example shows how to authenticate by using an API key. Use this approach for quick prototyping only; Microsoft Entra ID is recommended for production.

```python
import requests

# Replace with your actual API key and endpoint
api_key = "<your-api-key>"
endpoint = "https://<your-resource-name>.cognitiveservices.azure.com"

headers = {
    "api-key": api_key,
    "Content-Type": "application/json"
}

# Example: List deployments
response = requests.get(f"{endpoint}/openai/deployments?api-version=2024-10-21", headers=headers)
print(response.json())
```

> [!WARNING]
> API keys provide full access to the resource and can't be scoped to specific users or actions. Rotate keys regularly and avoid committing them to source control.

**Expected output**: A JSON response listing your model deployments, or a 401 error if the API key is invalid.

**Reference**: [Rotate API access keys](../../ai-services/rotate-keys.md?context=/azure/ai-foundry/context/context)

## Feature support matrix

Reference the following matrix to understand what capabilities in Foundry support API key versus Microsoft Entra ID. 

| Capability or feature | API key | Microsoft Entra ID | Notes |
| --- | --- | --- | --- |
| Basic model inference (chat, embeddings) | Yes | Yes | Fully supported. |
| Fine-tuning operations | Yes | Yes | Entra ID adds per-principal audit. |
| Agents service | No | Yes | Use Entra ID for managed identity tool access. |
| Evaluations | No | Yes | Use Entra ID. |
| Content safety analyze calls | Yes | Yes | Use RBAC to limit high-risk operations. |
| Batch analysis jobs (Content Understanding) | Yes | Yes | Entra ID recommended for scale. |
| Portal playground usage | Yes | Yes | Playground uses project connection mode. |
| Network isolation with Private Link | Yes | Yes | Entra ID adds conditional access. |
| Least privilege with built-in and custom roles | No | Yes | Keys are all-or-nothing per resource. |
| Managed identity (system or user-assigned) | No | Yes | Enables secret-less auth. |
| Per-request user attribution | No | Yes | Token contains tenant and object IDs. |
| Revocation (immediate) | Rotate key | Remove role or disable principal | Short token lifetime applies. |
| Support in automation pipelines | Yes (secret) | Yes (service principal or managed identity) | Entra ID reduces secret rotation. |
| Assistants API | Yes | Yes | Recommended to use Entra ID. |
| Batch inferencing | Yes | Yes |  |

## Identity types

Azure resources and applications authenticate by using different identity types, each designed for specific scenarios. User principals represent human users, service principals represent applications or automated processes, and managed identities provide a secure, credential-free way for Azure resources to access other services. Understanding these distinctions helps you choose the right identity for interactive sign-ins, app-to-app communication, or workload automation.

Azure supports the following identity types.

| Identity type | Description | 
| --- | --- |
| User principal | Individual user in Microsoft Entra ID |
| [Service principal](/entra/identity-platform/app-objects-and-service-principals) (app registration) | Application identity that uses a client secret or certificate | 
| [Managed identity](/entra/identity/managed-identities-azure-resources/overview) (system-assigned) | Azure resource-bound identity automatically managed by the platform. | 
| Managed identity (user-assigned) | Standalone identity that attaches to multiple resources. |


## Built-in roles overview

In Foundry, use the built-in roles to separate the allowed actions for a user. Most enterprises want a separation of control and data plane actions for their built-in roles. Others expect a combined data and control plane role to minimize the number of role assignments required. The following table lists scenarios and the corresponding built-in Foundry roles that best fit each scenario. 

| Scenario | Typical built-in roles | Notes |
| --- | --- | --- |
| Build agents with pre-deployed models | Azure AI User | Data plane usage only; no management writes. |
| Manage deployments or fine-tune models | Azure AI Project Manager | Includes model deployment creation and update. |
| Rotate keys or manage resource | Azure AI Account Owner | High privilege; consider custom role for least privilege. |
| Manage resource, manage deployments, build agents | Azure AI Owner | Highly privileged self-serve role for users who need both control plane and data plane access. Combine with Azure Monitor Reader if observability required. |
| Observability, tracing, monitoring | Azure AI User (minimum) | Add Azure Monitor Reader on Application Insights. |

To understand the breakdown of built-in roles and the control and data plane actions, review the following diagram. 

:::image type="content" source="../media/authentication-authorization/role-mapping-diagram.png" alt-text="Diagram mapping built-in roles to control plane actions and data plane actions in Foundry." lightbox="../media/authentication-authorization/role-mapping-diagram.png":::

> [!TIP]
> Create a custom role if a built-in role grants excess permissions for your use case.


## Set up Microsoft Entra ID

For high-level guidance on setting up Entra ID authentication in Foundry, see [Configure key-less authentication](../foundry-models/how-to/configure-entra-id.md).

1. Ensure your Microsoft Foundry resource has a custom subdomain configured. See [Custom subdomains](/azure/ai-services/cognitive-services-custom-subdomains). A custom subdomain is required for token-based authentication.
1. Assign the needed built-in or custom role to each principal. You need the **Owner** or **User Access Administrator** role at the target scope to assign roles. Common role assignments:
   - **Azure AI User**: For developers who need to build and test with pre-deployed models.
   - **Azure AI Project Manager**: For team leads who need to create projects and manage deployments.
   - **Azure AI Account Owner**: For administrators who need full resource management without data plane access.
   - **Azure AI Owner**: For users who need both full resource management and data plane access.
1. (Optional) For a service principal, create an app registration, add a client secret or certificate, and note the tenant ID, client ID, and secret or certificate.
1. (Optional) For a managed identity, enable the system-assigned identity on the calling service or attach a user-assigned identity, then assign a role to it on the Foundry resource.
1. Remove key-based authentication after all callers use token authentication. Optionally disable local authentication in deployment templates.

**Reference**: [Assign Azure roles](/azure/role-based-access-control/role-assignments-portal) | [Role-based access control for Foundry](rbac-foundry.md)

## Related content

- [Role-based access control for Foundry](rbac-foundry.md)
- [Configure key-less authentication with Microsoft Entra ID](../foundry-models/how-to/configure-entra-id.md)
- [Rotate API access keys](../../ai-services/rotate-keys.md?context=/azure/ai-foundry/context/context)
- [Azure built-in roles (AI + machine learning)](/azure/role-based-access-control/built-in-roles#ai-+-machine-learning)
- [Authentication vs. authorization (Microsoft Entra ID)](/entra/identity-platform/authentication-vs-authorization)
- [Identity fundamentals](/entra/fundamentals/identity-fundamental-concepts)
