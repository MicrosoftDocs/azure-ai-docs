---
title: Plan Azure AI Foundry Rollout Across My Organization
titleSuffix: Azure AI Foundry
description: Learn how to plan the rollout of Azure AI Foundry across your organization, including environment setup, data isolation, and governance.
manager: scottpolly
ms.service: azure-ai-foundry
author: sdgilley
ms.topic: concept-article
ms.date: 06/25/2025
ms.author: sgilley
ms.reviewer: deeikele
---

# Plan Azure AI Foundry rollout across my organization

This guide outlines key decisions for rolling out Azure AI Foundry, including environment setup, data isolation, integration with other Azure services, capacity management, and monitoring. Every organization is different. Use this guide as a starting point and adapt it to your needs. For implementation details, see the linked articles for further guidance.

## Example organization

Contoso is a global enterprise exploring GenAI adoption across five business groups, each with distinct needs and technical maturity.

To accelerate adoption while maintaining oversight, Contoso Enterprise IT aims to enable a model with common shared resources including networking and centralized data management, while enabling self-serve access to AI Foundry for each team within a governed, secure environment to manage their use cases.

## Rollout considerations

The Azure AI Foundry resource defines the scope for configuring, securing, and monitoring your team’s environment. Projects are like folders to organize your work within this resource context. Projects also grant access to Foundry’s developer APIs and tools.

:::image type="content" source="media/planning/foundry-resource.png" alt-text="Screenshot of a diagram showing Azure AI Foundry resource.":::

To ensure consistency, scalability, and governance across teams, consider the following environment setup practices when rolling out Azure AI Foundry:

- **Establish distinct environments for development, testing, and production** Use separate resource groups or subscriptions, and AI Foundry resources to isolate workflows, manage access, and support experimentation with controlled releases.

- **Create a separate Azure AI Foundry resource for each business group** Align deployments with logical boundaries such as data domains or business functions to ensure autonomy, governance, and cost tracking.

- **Define a project per use case** Foundry projects are designed to represent one specific use case. They're containers to organize components such as agents, files, for one application. While they inherit security settings from their parent resource, they also implement their own access controls, data integration, and other governance controls.

## Securing the AI Foundry environment

AI Foundry is built on the Azure platform, allowing you to customize security controls to meet your organization’s needs. Key configuration areas include:

- **Identity**: Use Microsoft Entra ID to manage user and service access. AI Foundry supports managed identities to allow secure, passwordless authentication to other Azure services. Managed identities can be assigned at the **AI Foundry resource level** and optionally at the **project level** for fine-grained control. [Learn more about managed identities.](/security/benchmark/azure/baselines/azure-ai-foundry-security-baseline).

- **Networking**: Deploy AI Foundry into a Virtual Network (VNet) to isolate traffic and control access using Network Security Groups (NSGs). [Learn more about networking security.](/security/benchmark/azure/baselines/azure-ai-foundry-security-baseline).

- **Customer-Managed Keys (CMK)**: Azure supports CMK for encrypting data at rest. AI Foundry supports CMK optionally for customers with strict compliance needs. [Learn more about CMK](/security/benchmark/azure/baselines/azure-ai-foundry-security-baseline).

- **Authentication & Authorization**: AI Foundry supports both **API key-based access** for simple integration and **Azure RBAC** for fine-grained control. Azure enforces a clear separation between the **control plane** (resource management) and the **data plane** (model and data access). Start with built-in roles, and define custom roles as needed. [Learn more about authentication.](/security/benchmark/azure/baselines/azure-ai-foundry-security-baseline).

- **Templates**: Use ARM templates or Bicep to automate secure deployments. Explore the [sample templates](/security/benchmark/azure/baselines/azure-ai-foundry-security-baseline).

- **Storage resource**: you might choose to use built-in storage capabilities in AI Foundry or use your own storage resources. In particular for Agent services, threads and messages can optionally be stored in [resources managed by you](/azure/ai-foundry/agents/how-to/use-your-own-resources).

### Example: Contoso’s security approach

Contoso secures its AI Foundry deployments using **private networking** with **Enterprise IT** managing a central **hub network**, and each business group connecting via a **spoke VNet**. They use **built-in Role Based Access Roles (RBAC)** to separate access:

* **Admins** manage deployments/connections/shared resources
* **Project Managers** oversee specific projects
* **Users** interact with GenAI tools

For most use cases, Contoso does **not use Customer-Managed Keys**, relying on Microsoft-managed encryption by default.

## Plan user access

Effective access management is foundational to a secure and scalable AI Foundry setup.

- **Define required access roles and responsibilities**
  - Identify which user groups require access to various aspects of the AI Foundry environment.
  - Assign built-in or custom Azure RBAC roles based on responsibilities such as:
    - Account owner: Manage top-level configurations such as security and shared resource connections.
    - Project Managers: Create and manage AI Foundry projects and their contributors.
    - Project Users: contribute to existing projects.
- **Determine access scope**
  - Choose the appropriate scope for access assignments:
    - Subscription level: broadest access, typically suitable for central IT or platform teams or smaller organizations.
    - Resource group level: Useful for grouping related resources with shared access policies. For example, an Azure Function that follows the same application lifecycle as your AI Foundry environment.
    - Resource or project level: Ideal for fine-grained control, especially when dealing with sensitive data or enabling self-service.
- **Align identity strategy**
  - For data sources and tools integrated with AI Foundry, determine whether users should authenticate using:
    - Using managed identities or API key: suitable for automated services and shared access across users.
    - User identities: Preferred when user-level accountability or auditability is required.
  - Use Microsoft Entra ID groups to simplify access management and ensure consistency across environments.

## Establish connectivity with other Azure services

Azure AI Foundry supports **connections**, which are reusable configurations that enable access to application components on Azure and non-Azure services. These connections also act as **identity brokers**, allowing Foundry to authenticate to external systems using managed identities or service principals on behalf of project users.

Connections can be created at the **AI Foundry resource level**—ideal for shared services like Azure Storage or Key Vault—or scoped to a **specific project**, which is recommended for sensitive or project-specific integrations. This flexibility allows teams to balance reuse and isolation based on their needs. [Learn more about connections in AI Foundry](/security/benchmark/azure/baselines/azure-ai-foundry-security-baseline).

Connection authentication can be configured to use either shared access tokens—such as Microsoft Entra ID managed identities or API keys—for simplified management and onboarding, or user tokens via Entra ID passthrough, which offer greater control when accessing sensitive data sources.

:::image type="content" source="media/planning/connectivity.png" alt-text="Screenshot of a diagram showing Azure AI Foundry project connectivity and integration with other Azure services.":::

### Example: Contoso’s connectivity strategy

- Contoso creates an Azure AI Foundry resource for every business group, ensuring projects with similar data needs can share same connected resources.
- By default, connected resources use shared authentication tokens and are shared across all projects.
- Projects that use sensitive data workloads, connect to data source with project-scoped connections, and EntraID passthrough authentication.

## Governance

Effective governance in Azure AI Foundry ensures secure, compliant, and cost-efficient operations across business groups.

- **Model Access Control with Azure Policy**
  Azure Policy allows you to enforce rules across Azure resources. In AI Foundry, you can use policies to restrict which models or model families specific business groups can access.
  *Example*: Contoso’s **Finance & Risk** group is restricted from using preview or noncompliant models by applying a policy at their business group’s subscription level.
- **Cost Management by Business Group**
  By deploying AI Foundry per business group, Contoso can track and manage costs independently. Use Microsoft Cost Management to view detailed usage and spending per Foundry deployment or project.
- **Usage Tracking with Azure Monitor**
  Azure Monitor provides metrics and dashboards to track usage patterns, performance, and health of AI Foundry resources.
- **Verbose Logging with Azure Log Analytics**
  Azure Log Analytics enables deep inspection of logs for operational insights. For example, log request usage, token usage, and latency to support auditing and optimization.

## Configure and optimize model deployments

When deploying models in AI Foundry, teams can choose between standard and provisioned [deployment types](../../../ai-services/openai/how-to/deployment-types.md). Standard deployments are ideal for development and experimentation, offering flexibility and ease of setup. Provisioned deployments are recommended for production scenarios where predictable performance, cost control, and model version pinning are required.

To support cross-region scenarios and let you access existing model deployments, AI Foundry allows [connections](../connections-add.md?pivots=fdp-project) to model deployments hosted in other Foundry or Azure OpenAI instances. Connections enable teams to centralize deployments for experimentation while still enabling access from distributed projects. For production workloads, consider for use cases to manage its own deployments to ensure tighter control over model lifecycle, versioning, and rollback strategies.

To prevent overuse and ensure fair resource allocation, you can apply [Tokens Per Minute (TPM) limits at the deployment level](../../../ai-services/openai/concepts/provisioned-throughput.md?tabs=global-ptum). TPM limits help control consumption, protect against accidental spikes, and align usage with project budgets or quotas. Consider setting conservative limits for shared deployments and higher thresholds for critical production services.

## Access extended functionality with Azure AI Hub

While an Azure AI Foundry resource alone gives you access to most AI Foundry functionality, select capabilities are currently only available in combination with an Azure AI hub resource powered by Azure Machine Learning. These are capabilities lower in the AI development stack, focused on model customization.

Hub resources require their own project types that can also be accessed using the Azure Machine Learning Studio/SDK/CLI. To help plan your deployment, see [this table](../../what-is-azure-ai-foundry.md#which-type-of-project-do-i-need) and [choose a resource type](../../concepts/resource-types.md), for an overview of supported capabilities.

A hub resource is deployed side-by-side with your AI Foundry resource and takes a dependency on your AI Foundry resource to provide access to select tools and models.

## Learn more

### Secure the AI Foundry Environment

- Identity & Managed Identity: [Configure managed identity in Azure AI Foundry](../../../ai-services/openai/how-to/managed-identity.md)
- Networking: [Use a virtual network with Azure AI Foundry](../../agents/how-to/virtual-networks.md)
- Customer-Managed Keys (CMK): [Customer-managed keys in Azure AI Foundry](../../concepts/encryption-keys-portal.md)
- Authentication & RBAC: [Role-based access control in Azure AI Foundry](../../concepts/rbac-azure-ai-foundry.md)
- Sample Templates: [Create an AI Foundry hub using a Bicep template](../create-azure-ai-hub-template.md)
- [Recover or purge deleted Azure AI Foundry resources](../../../ai-services/recover-purge-resources.md)

### Establish Connectivity with Other Azure Services

- Overview of Connections: [Add a new connection in Azure AI Foundry](../connections-add.md)
- Project vs. Resource-Level Connections: [Configure a connection to use Azure AI Foundry Models](../../model-inference/how-to/configure-project-connection.md)

### Governance

- Model Access Control with Azure Policy: [Control model deployment with built-in policies](../built-in-policy-model-deployment.md)
- Cost Management: [Plan and manage costs for Azure AI Foundry](../costs-plan-manage.md)
- Azure Monitor for Usage Tracking: [Monitor your Generative AI applications](../monitor-applications.md)
- Azure Log Analytics for Logging: [Enable diagnostic logging for Azure AI services](../../../ai-services/diagnostic-logging.md)

### Share Reserved Capacity Across Business Groups

- Cross-Resource Model Access: [Use Azure AI services in Azure AI Foundry](../../../ai-services/connect-services-ai-foundry-portal.md)
- Shared PTU Deployments: [Provisioned Throughput Reservations in Azure AI Foundry](/azure/cost-management-billing/reservations/azure-ai-foundry)

### Azure Landing zones

- [AI landing zones](/azure/architecture/ai-ml/architecture/baseline-azure-ai-foundry-landing-zone)
