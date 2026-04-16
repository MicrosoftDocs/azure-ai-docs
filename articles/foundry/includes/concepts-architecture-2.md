---
title: Include file
description: Include file
author: sdgilley
ms.reviewer: deeikele
ms.author: sgilley
ms.service: microsoft-foundry
ms.topic: include
ms.date: 03/20/2026
ms.custom: include
---

## Foundry resource hierarchy

The following diagram shows a Foundry resource with model deployments, security settings, connections, and two projects. Connected Azure services such as Storage, Key Vault, and Azure AI Search are separate Azure resources under their own governance boundaries:

:::image type="content" source="../media/architecture/architecture.svg" alt-text="Diagram showing the Foundry resource hierarchy with a governance boundary containing model deployments, security settings, connections, and two projects. Connected resources like Storage, Key Vault, and Azure AI Search are shown as separate governance boundaries.":::

> [!IMPORTANT]
> Connected resources like Storage, Key Vault, and Azure AI Search are independent Azure resources with their own governance boundaries. You manage networking, access policies, and compliance settings for these resources separately from the Foundry resource.

Use this model when planning architecture and access boundaries:

- **Foundry resource**: Top-level Azure resource where you manage governance settings such as networking, security, and model deployments.
- **Project**: Development boundary inside the Foundry resource where teams build and evaluate use cases. Projects let teams prototype within a preconfigured environment, reusing existing model deployments and connections without repeated IT setup.
- **Project assets**: Files, agents, evaluations, and related artifacts scoped to a project.
- **Connected resources**: Azure services such as Storage, Key Vault, and Azure AI Search that the Foundry resource references through connections. These resources have separate governance boundaries, so you manage their networking and access policies independently.

This separation lets IT teams apply centralized controls at the resource level while development teams work within project-level boundaries.

> [!NOTE]
> Most new APIs are available at the project scope. However, some capabilities originally supported at the account level through Azure OpenAI, Speech, Vision, and Language services are available only at the Foundry resource level, not at the project scope. For example, the Translator API is available only from the Foundry resource level. Plan your deployment structure based on which API scopes your workloads require.

## Security-driven separation of concerns

Foundry enforces a clear separation between management and development operations to ensure secure and scalable AI workloads.

### Top-level resource governance

The top-level Foundry resource scopes management operations such as configuring security, establishing connectivity with other Azure services, and managing deployments. Dedicated project containers isolate development activities and provide boundaries for access control, files, agents, and evaluations.

### Role-based access control

Azure RBAC actions reflect this separation of concerns. Control plane actions, such as creating deployments and projects, are distinct from data plane actions, such as building agents, running evaluations, and uploading files. You can scope RBAC assignments at both the top-level resource and individual project level. Assign [managed identities](/entra/identity/managed-identities-azure-resources/overview) at either scope to support secure automation and service access. For more information, see [Role-based access control for Microsoft Foundry](../concepts/rbac-foundry.md).

Common starter assignments for least-privilege onboarding include:

- **Azure AI User** for each developer user principal at the Foundry resource scope.
- **Azure AI User** for each project managed identity at the Foundry resource scope.

For role definitions and scope planning guidance, see [Role-based access control for Microsoft Foundry](../concepts/rbac-foundry.md).

## Monitoring and observability

Azure Monitor segments metrics by scope. You can view management and usage metrics at the top-level resource, while project-specific metrics, such as evaluation performance or agent activity, are scoped to the individual project containers.

Key monitoring capabilities include:

- **Resource-level metrics**: Token consumption, model latency, request counts, and error rates across all projects.
- **Project-level metrics**: Evaluation run outcomes, agent invocation counts, and file operation activity.
- **Diagnostic logging**: Enable diagnostic settings to route logs to Log Analytics, Storage, or Event Hubs for analysis and retention.

For more information, see [Azure Monitor overview](/azure/azure-monitor/overview).
