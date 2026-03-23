---
title: Include file
description: Include file
author: sdgilley
ms.reviewer: deeikele
ms.author: sgilley
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 03/20/2026
ms.custom: include
---

## How resources relate in Foundry

Use this model when planning architecture and access boundaries:

- **Foundry resource**: Top-level Azure resource where you manage governance settings such as networking, security, and model deployments.
- **Project**: Development boundary inside the Foundry resource where teams build and evaluate use cases.
- **Project assets**: Files, agents, evaluations, and related artifacts scoped to a project.

This separation lets IT teams apply centralized controls at the resource level while development teams work within project-level boundaries.

## Security-driven separation of concerns

Foundry enforces a clear separation between management and development operations to ensure secure and scalable AI workloads.

- **Top-Level Resource Governance:** Management operations, such as configuring security, establishing connectivity with other Azure services, and managing deployments, are scoped to the top-level Foundry resource. Development activities are isolated within dedicated project containers, which encapsulate use cases and provide boundaries for access control, files, agents, and evaluations.

- **Role-Based Access Control (RBAC):** Azure RBAC actions reflect this separation of concerns. Control plane actions, such as creating deployments and projects, are distinct from data plane actions, such as building agents, running evaluations, and uploading files. You can scope RBAC assignments at both the top-level resource and individual project level. Assign [managed identities](/entra/identity/managed-identities-azure-resources/overview) at either scope to support secure automation and service access. For more information, see [Role-based access control for Microsoft Foundry](../concepts/rbac-foundry.md).

  Common starter assignments for least-privilege onboarding include:

  - **Azure AI User** for each developer user principal at the Foundry resource scope.
  - **Azure AI User** for each project managed identity at the Foundry resource scope.

  For role definitions and scope planning guidance, see [Role-based access control for Microsoft Foundry](../concepts/rbac-foundry.md).

- **Monitoring and Observability:** Azure Monitor metrics are segmented by scope. You can view management and usage metrics at the top-level resource, while project-specific metrics, such as evaluation performance or agent activity, are scoped to the individual project containers.
