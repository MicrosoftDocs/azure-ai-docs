---
title: "Microsoft Foundry architecture"
description: "Learn about the architecture of Microsoft Foundry."
ms.service: azure-ai-foundry
ms.custom:
  - classic-and-new
  - build-2024
  - ignite-2024
  - doc-kit-assisted
ms.topic: concept-article
ms.date: 04/06/2026
ms.reviewer: deeikele
ms.author: sgilley
author: sdgilley
ai-usage: ai-assisted
---

# Microsoft Foundry architecture
Microsoft Foundry organizes AI workloads through a layered architecture: a top-level Foundry resource for governance, projects for development isolation, and connected Azure services for storage, search, and secrets management.

This article provides IT operations and security teams with details on the Foundry resource and underlying Azure service architecture, its components, and its relation with other Azure resource types. Use this information to guide how to [customize](../how-to/configure-private-link.md) your Foundry deployment to your organization's requirements. For more information on how to roll out Foundry in your organization, see [Foundry Rollout](../concepts/planning.md).

[!INCLUDE [architecture 1](../includes/concepts-architecture-1.md)]

[!INCLUDE [Resource provider kinds](../includes/resource-provider-kinds.md)]

Resource types under the same provider namespaces share the same management APIs, and use similar [Azure role-based access control (Azure RBAC)](/azure/role-based-access-control/overview) actions, networking configurations, and aliases for Azure Policy configuration. If you're upgrading from Azure OpenAI to Foundry, your existing custom Azure policies and Azure RBAC actions continue to apply.

[!INCLUDE [architecture 2](../includes/concepts-architecture-2.md)]

## Computing infrastructure

Foundry manages compute infrastructure for model hosting, agent execution, and batch processing. This section covers deployment types, agent and evaluation infrastructure, virtual network integration, tenant isolation, content safety controls, and regional availability.

### Model deployment types

Foundry supports multiple deployment types for model hosting, grouped by data-processing scope: global (cross-region), data zone (within a defined boundary), and regional (single region). Each type balances latency, throughput, and data-processing location differently:

| Deployment type | Data processing | Billing |
| --- | --- | --- |
| Global Standard | Cross-region, Azure-managed | Pay-per-token |
| Global Provisioned | Cross-region, Azure-managed | Hourly reserved capacity |
| Global Batch | Cross-region, Azure-managed | Batch token pricing |
| Data Zone Standard | Within data-zone boundary | Pay-per-token |
| Data Zone Provisioned | Within data-zone boundary | Hourly reserved capacity |
| Data Zone Batch | Within data-zone boundary | Batch token pricing |
| Standard | Single region | Pay-per-token |
| Regional Provisioned | Single region | Hourly reserved capacity |
| Developer | Any Azure region (no data residency guarantee) | Pay-per-token (fine-tuned model evaluation only; 24-hour lifetime; no SLA) |

For details on how to choose the right deployment type, see [Deployment types for Foundry Models](../foundry-models/concepts/deployment-types.md).

### Agents, evaluations, and batch processing

Agents, evaluations, and batch jobs are fully managed by Microsoft. Agent workloads run inside the platform's container infrastructure, which supports [virtual network integration](#virtual-network-integration) for network-isolated scenarios. Evaluations invoke model endpoints, compare outputs against grading criteria, and store results within the project scope. Batch processing queues inference requests for asynchronous execution at reduced per-token pricing. Results for all three workload types are accessible through the portal or SDK.

### Virtual network integration

When your agents connect with external systems, you can isolate network traffic using [container injection](../agents/how-to/virtual-networks.md), where the platform injects a subnet into your virtual network, enabling local communication with your Azure resources within the same virtual network.

Foundry supports two networking models for outbound isolation:

| Model | How it works | Trade-off |
| --- | --- | --- |
| **Customer-managed VNet (BYO)** | You provide the VNet and a dedicated subnet delegated to `Microsoft.App/environments`. The platform injects into your subnet, enabling local communication with your private Azure resources. | Full control over network configuration; requires your own network management. |
| **Managed VNet** (preview) | Foundry manages the VNet on your behalf. | Simpler setup; limits customization options. For details, see [Configure managed virtual network](../how-to/managed-virtual-network.md). |

> [!NOTE]
> Some network-isolated scenarios require the SDK or CLI instead of the portal. For example, deployments with private endpoints that block all public access aren't configurable through the portal UI. For details, see [How to configure a private link for Foundry](../how-to/configure-private-link.md).

### Tenant isolation

Workloads run in logically isolated environments per project. Customer code doesn't share runtime containers with other tenants.

### Content safety and guardrails

Foundry integrates content safety controls into the model and agent inference pipeline. Guardrails define risks to detect, intervention points to scan (user input, output, tool calls (preview), and tool responses (preview)), and response actions when a risk is detected. Content filters run inline with model requests and can be configured per deployment. For more information, see [Guardrails and controls overview](../guardrails/guardrails-overview.md) and [Content filtering severity levels](../openai/concepts/content-filter-severity-levels.md).

### Regional availability

Compute capabilities vary by Azure region. Model availability, deployment type options, and feature support such as Agents or evaluations might differ across regions. Confirm that your target region supports the required capabilities before provisioning. For current availability, see [Feature availability across cloud regions](../reference/region-support.md).

[!INCLUDE [architecture 3](../includes/concepts-architecture-3.md)]
