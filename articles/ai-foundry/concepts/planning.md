---
title: Microsoft Foundry Rollout Across My Organization
titleSuffix: Microsoft Foundry
description: Learn how to plan the rollout of Microsoft Foundry across your organization, including environment setup, data isolation, and governance.
ms.service: azure-ai-foundry
author: sdgilley
ms.topic: concept-article
ms.date: 12/24/2025
ms.author: sgilley
ms.reviewer: deeikele
monikerRange: 'foundry-classic || foundry'
ms.custom:
  - dev-focus
ai-usage: ai-assisted
---

# Microsoft Foundry rollout across my organization

[!INCLUDE [version-banner](../includes/version-banner.md)]

This guide outlines key decisions for rolling out Microsoft Foundry, including environment setup, data isolation, integration with other Azure services, capacity management, and monitoring. Use this guide as a starting point and adapt it to your needs. For implementation details, see the linked articles for further guidance.

## Prerequisites

Before you begin rollout planning, confirm that you have:

- A target Azure subscription and resource group strategy for development, test, and production environments.
- Microsoft Entra ID groups (or equivalent identity groups) defined for admins, project managers, and project users.
- An initial region plan based on model and feature availability. For details, see [Feature availability across cloud regions](../reference/region-support.md).
- Agreement on security requirements for networking, encryption, and data isolation in your organization.

## Baseline rollout checklist

Use this checklist before your first production rollout:

1. Define environment boundaries across development, testing, and production.
1. Assign ownership for each Foundry resource and project scope.
1. Define RBAC assignments for admins, project managers, and project users.
1. Define networking approach for each environment (public access, private endpoint, or hybrid).
1. Decide whether customer-managed keys are required by policy.
1. Define cost and monitoring ownership for each business group.
1. Identify required shared connections and project-scoped connections.

## Example organization

Contoso is a global enterprise exploring GenAI adoption across five business groups, each with distinct needs and technical maturity.

To accelerate adoption while maintaining oversight, Contoso Enterprise IT aims to enable a model with common shared resources including networking and centralized data management, while enabling self-serve access to Foundry for each team within a governed, secure environment to manage their use cases.

## Rollout considerations

The Foundry resource defines the scope for configuring, securing, and monitoring your team's environment. It's available in the Foundry portal and through Azure APIs. Projects are like folders to organize your work within this resource context. Projects also control access and permissions to Foundry developer APIs and tools.

:::image type="content" source="../media/planning/foundry-resource.png" alt-text="Screenshot of a diagram showing Foundry resource.":::

To ensure consistency, scalability, and governance across teams, consider the following environment setup practices when rolling out Foundry:

- **Establish distinct environments for development, testing, and production.** Use separate resource groups or subscriptions, and Foundry resources to isolate workflows, manage access, and support experimentation with controlled releases.

- **Create a separate Foundry resource for each business group.** Align deployments with logical boundaries such as data domains or business functions to ensure autonomy, governance, and cost tracking.

- **Associate projects with use cases.** Foundry projects are designed to represent specific use cases. They're containers to organize components such as agents or files for an application. While they inherit security settings from their parent resource, they can also implement their own access controls, data integration, and other governance controls.

## Securing the Foundry environment

Foundry is built on the Azure platform, so you can customize security controls to meet your organization's needs. Key configuration areas include:

- **Identity**: Use Microsoft Entra ID to manage user and service access. Foundry supports managed identities to allow secure, passwordless authentication to other Azure services. You can assign managed identities at the **Foundry resource level** and optionally at the **project level** for fine-grained control. [Learn more about managed identities.](/security/benchmark/azure/baselines/azure-ai-foundry-security-baseline)

- **Networking**: Deploy Foundry into a Virtual Network to isolate traffic and control access by using Network Security Groups (NSGs). [Learn more about networking security.](/security/benchmark/azure/baselines/azure-ai-foundry-security-baseline)

  For private connectivity scenarios, use private endpoints and validate DNS and endpoint approval status. For implementation details and limitations, see [How to configure a private link for Foundry](../how-to/configure-private-link.md).

  > [!IMPORTANT]
  > End-to-end network isolation isn't fully supported in the new Foundry portal experience. For network-isolated deployments, use the guidance for the classic experience, SDK, or CLI in [How to configure a private link for Foundry](../how-to/configure-private-link.md).

- **Customer-Managed Keys (CMK)**: Azure supports CMK for encrypting data at rest. Foundry supports CMK optionally for customers with strict compliance needs. [Learn more about CMK](/security/benchmark/azure/baselines/azure-ai-foundry-security-baseline).

- **Authentication and Authorization**: Foundry supports both **API key-based access** for simple integration and **Azure RBAC** for fine-grained control. API keys can simplify setup, but they don't provide the same role-based granularity as Microsoft Entra ID with RBAC. Azure enforces a clear separation between the **control plane** (resource management) and the **data plane** (model and data access). Start with built-in roles, and define custom roles as needed. [Learn more about authentication.](/security/benchmark/azure/baselines/azure-ai-foundry-security-baseline)

- **Templates**: Use ARM templates or Bicep to automate secure deployments. Explore the [sample templates](/security/benchmark/azure/baselines/azure-ai-foundry-security-baseline).

- **Storage resource**: You might choose to use built-in storage capabilities in Foundry or use your own storage resources. For the Agent Service, threads and messages can optionally be stored in [resources managed by you](/azure/ai-foundry/agents/how-to/use-your-own-resources).

## Example: Contoso's security approach

Contoso secures its Foundry deployments by using private networking with Enterprise IT managing a central hub network. Each business group connects via a spoke virtual network. They use built-in Role Based Access Control (RBAC) to separate access:

* **Admins** manage deployments, connections, and shared resources
* **Project Managers** oversee specific projects
* **Users** interact with GenAI tools

For most use cases, Contoso relies on Microsoft-managed encryption by default and does **not use Customer-Managed Keys**.

## Plan user access

Effective access management is foundational to a secure and scalable Foundry setup.

- **Define required access roles and responsibilities**
  - Identify which user groups require access to various aspects of the Foundry environment.
  - Assign built-in or custom Azure RBAC roles based on responsibilities such as:
    - Account owner: Manage top-level configurations such as security and shared resource connections.
    - Project Managers: Create and manage Foundry projects and their contributors.
    - Project Users: contribute to existing projects.

  Use this starter role-to-scope mapping for rollout planning:

  | Persona | Starter role | Recommended scope |
  |---|---|---|
  | Admins | Owner or Azure AI Account Owner | Subscription or Foundry resource |
  | Project Managers | Azure AI Project Manager | Foundry resource |
  | Project Users | Azure AI User | Foundry project |

  Adjust assignments based on least-privilege requirements and enterprise policies.
- **Determine access scope**
  - Choose the appropriate scope for access assignments:
    - Subscription level: broadest access, typically suitable for central IT or platform teams or smaller organizations.
    - Resource group level: Useful for grouping related resources with shared access policies. For example, an Azure Function that follows the same application lifecycle as your Foundry environment.
    - Resource or project level: Ideal for fine-grained control, especially when dealing with sensitive data or enabling self-service.
- **Align identity strategy**
  - For data sources and tools integrated with Foundry, determine whether users should authenticate by using:
    - Managed identities or API key: suitable for automated services and shared access across users.
    - User identities: Preferred when user-level accountability or auditability is required.
  - Use Microsoft Entra ID groups to simplify access management and ensure consistency across environments.

  For least-privilege onboarding, start with the **Azure AI User** role for developers and project managed identities, then add elevated roles only where required. For details, see [Role-based access control in Foundry](../concepts/rbac-foundry.md).

## Establish connectivity with other Azure services

Foundry supports **connections**, which are reusable configurations that enable access to application components on Azure and non-Azure services. These connections also act as **identity brokers**, allowing Foundry to authenticate to external systems by using managed identities or service principals on behalf of project users.

Create connections at the **Foundry resource level** for shared services like Azure Storage or Key Vault. Scope connections to a **specific project** for sensitive or project-specific integrations. This flexibility allows teams to balance reuse and isolation based on their needs. [Learn more about connections in Foundry](../how-to/connections-add.md).

Configure connection authentication to use either shared access tokens, such as Microsoft Entra ID managed identities or API keys, for simplified management and onboarding, or user tokens via Entra ID passthrough, which offer greater control when accessing sensitive data sources.

:::image type="content" source="../media/planning/connectivity.png" alt-text="Screenshot of a diagram showing Foundry project connectivity and integration with other Azure services.":::

### Example: Contoso's connectivity strategy

- Contoso creates a Foundry resource for every business group, ensuring projects with similar data needs share the same connected resources.
- By default, connected resources use shared authentication tokens and are shared across all projects.
- Projects that use sensitive data workloads connect to data sources with project-scoped connections and Microsoft Entra ID passthrough authentication.

## Governance

Effective governance in Foundry ensures secure, compliant, and cost-efficient operations across business groups.

- **Model Access Control with Azure Policy**
  Azure Policy enforces rules across Azure resources. In Foundry, use policies to restrict which models or model families specific business groups can access.
  *Example*: Contoso’s **Finance & Risk** group is restricted from using preview or noncompliant models by applying a policy at their business group’s subscription level.
- **Cost Management by Business Group**
  By deploying Foundry per business group, Contoso can track and manage costs independently. Use the Azure pricing calculator for predeployment estimates and Microsoft Cost Management for ongoing actual usage and trend tracking. Treat Foundry costs as one part of the total solution cost.
- **Usage Tracking with Azure Monitor**
  Azure Monitor provides metrics and dashboards to track usage patterns, performance, and health of Foundry resources.
- **Verbose Logging with Azure Log Analytics**
  Azure Log Analytics enables deep inspection of logs for operational insights. For example, log request usage, token usage, and latency to support auditing and optimization.

## Validate rollout decisions

After you define your rollout plan, validate the following outcomes:

- Identity and access: Role assignments map to approved personas and scopes.
- Networking: Connectivity path and isolation model are documented for each environment.
- Networking verification: Private endpoint connection status is **Approved**, and DNS resolves Foundry endpoints to private IP addresses from inside the virtual network.
- Data protection: Encryption approach (Microsoft-managed keys or customer-managed keys) is documented and approved.
- Operations: Cost and monitoring owners are assigned per business group.
- Operations verification: Cost views and dashboards are defined in Microsoft Cost Management and monitoring is connected to Application Insights for each production project.
- Model operations: Deployment strategy (standard or provisioned) is documented per use case.
- Region readiness: Required models and services are confirmed in target regions before rollout.

## Configure and optimize model deployments

When deploying models in Foundry, teams can choose between standard and provisioned [deployment types](../../ai-services/openai/how-to/deployment-types.md). Standard deployments are ideal for development and experimentation, offering flexibility and ease of setup. Provisioned deployments are recommended for production scenarios where predictable performance, cost control, and model version pinning are required.

To support cross-region scenarios and let you access existing model deployments, Foundry allows [connections](../how-to/connections-add.md) to model deployments hosted in other Foundry or Azure OpenAI instances. By using connections, teams can centralize deployments for experimentation while still enabling access from distributed projects. For production workloads, consider having use cases manage their own deployments to ensure tighter control over model lifecycle, versioning, and rollback strategies.

To prevent overuse and ensure fair resource allocation, you can apply [Tokens Per Minute (TPM) limits at the deployment level](../openai/concepts/provisioned-throughput.md?tabs=global-ptum). TPM limits help control consumption, protect against accidental spikes, and align usage with project budgets or quotas. Consider setting conservative limits for shared deployments and higher thresholds for critical production services.

::: moniker range="foundry-classic"

## Access extended functionality with Azure AI Hub

While a Foundry resource alone gives you access to most Foundry functionality, select capabilities are currently only available in combination with an Azure AI hub resource powered by Azure Machine Learning. These capabilities are lower in the AI development stack and focus on model customization.

Hub resources require their own project types that you can also access by using the Azure Machine Learning Studio, SDK, or CLI. To help plan your deployment, see [this table](../what-is-foundry.md#which-type-of-project-do-i-need) and [choose a resource type](../concepts/resource-types.md) for an overview of supported capabilities.

You deploy a hub resource side-by-side with your Foundry resource. The hub resource takes a dependency on your Foundry resource to provide access to select tools and models.

::: moniker-end

## Learn more

- Secure the Foundry environment

  - Authentication and RBAC: [Role-based access control in Foundry](../concepts/rbac-foundry.md)
  - Networking: [Use a virtual network with Foundry](../how-to/configure-private-link.md)
  - Identity and managed identity: [Configure managed identity in Foundry](../../ai-services/openai/how-to/managed-identity.md)
  - Customer-managed keys (CMK): [Customer-managed keys in Foundry](../concepts/encryption-keys-portal.md)
  - Example infrastructure: [templates repository with sample infrastructure templates](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples)
  - [Recover or purge deleted Foundry resources](../../ai-services/recover-purge-resources.md?toc=/azure/ai-foundry/toc.json&bc=/azure/ai-foundry/breadcrumb/toc.json)

- Establish connectivity with other Azure services

  - Overview of connections: [Add a new connection in Foundry](../how-to/connections-add.md)

- Governance

  - Model access control with Azure Policy: [Control model deployment with built-in policies](../how-to/built-in-policy-model-deployment.md)
  - Cost management: [Plan and manage costs for Foundry](../how-to/costs-plan-manage.md)
  - Azure Monitor for usage tracking: [Monitor your Generative AI applications](../how-to/monitor-applications.md)