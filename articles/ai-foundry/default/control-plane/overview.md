---
title: What is Microsoft Foundry Control Plane?
ms.service: azure-ai-foundry
ms.topic: concept-article
ms.date: 02/05/2026
ms.reviewer: mesameki
ms.author: scottpolly
author: mesameki
description: Learn how Microsoft Foundry Control Plane provides unified visibility, governance, and control for AI agents, models, and tools across your enterprise.
ai-usage: ai-assisted
#customer intent: As an enterprise administrator or AI developer, I want to understand what Foundry Control Plane is and how it provides unified visibility across my AI agent fleet so that I can determine if it meets my governance and operational needs.
---

# What is Microsoft Foundry Control Plane?

Microsoft Foundry Control Plane is a unified management interface that provides visibility, governance, and control for AI agents, models, and tools across your Foundry enterprise. Use Foundry Control Plane as your central location for managing every aspect of your AI agent fleet, from build to production.

As your organization evolves from isolated copilots to autonomous multi-agent fleets, you need unified oversight. Foundry Control Plane provides the visibility, governance, and control that you need to scale with confidence.

In this article, you learn what Foundry Control Plane offers, including fleet management, observability, compliance enforcement, and security capabilities.

## Prerequisites

- An Azure subscription. [Create one for free](https://azure.microsoft.com/free/).
- A Microsoft Foundry project. For more information, see [Create a project](../../how-to/create-projects.md).
- An [AI gateway configured](../configuration/enable-ai-api-management-gateway-portal.md) for advanced governance features.

## Core functionalities

Foundry Control Plane consolidates *inventory, observability, compliance, and security* into one role-aware interface. It integrates seamlessly with Microsoft security and governance systems (Microsoft Defender, Microsoft Purview, Microsoft Entra) to deliver *trust at scale*.

The following diagram shows how Foundry Control Plane provides unified fleet visibility with agents, models, and tools listed across projects in a subscription.

:::image type="content" source="media/overview/control-plane-overall.png" alt-text="Diagram that depicts Foundry Control Plane unified fleet visibility with agents, models, and tools listed across projects in a subscription." lightbox="media/overview/control-plane-overall.png":::

You can use Foundry Control Plane for the following tasks.

### Manage your fleet across Foundry, Microsoft, and non-Microsoft agents in one place

- Track key performance indicators such as active agents, run completion, compliance posture, cost efficiency, and prohibited behaviors across [supported agent platforms](how-to-manage-agents.md#supported-agent-platforms).

- Use deep links to evaluation and monitoring experiences for rapid debugging, diagnosis, and remediation.

- Visualize fleet health through intuitive dashboards that surface trends and anomalies instantly.

### Observe, protect, and improve

- Correlate alerts, evaluation results, and trace data to pinpoint problems instantly.

- [Continuously evaluate](../../how-to/continuous-evaluation-agents.md) agent performance, quality, and risk dimensions. Risk dimensions might include [task adherence, intent resolution, tool call success](../../concepts/evaluation-evaluators/agent-evaluators.md), [groundedness](../../concepts/evaluation-evaluators/rag-evaluators.md), sensitive data leakage, and exposure to jailbreak and cross-domain prompt injection attacks (XPIAs).

- Use the [AI Red Teaming Agent](../../concepts/ai-red-teaming-agent.md) and [cluster analysis](../observability/how-to/cluster-analysis.md) for automated vulnerability probing and error root-cause discovery.

- View recommendations for prompt refinements, model version upgrades, and configuration changes.

### Govern and enforce with guardrails

- Define enterprise-wide guardrail policies for safety, compliance, and quality.

- Apply bulk remediation to instantly correct noncompliant configurations across your fleet.

### Secure agents

- Schedule automated red-teaming scans and drift monitoring for ongoing agent testing.

- View Defender and Microsoft Purview alerts directly on the Foundry Control Plane dashboard.

- Track rate limits, token usage, and cost anomalies to prevent inefficiency or abuse.

## Key features

The Foundry Control Plane experience begins when you select **Operate** on the upper-right toolbar of the Foundry workspace. From **Operate**, you can monitor, govern, and optimize every agent, model, and deployment within your subscription.

Each pane within **Operate** is designed around a specific job to be done. These panes help various roles, from builders to administrators, manage AI systems confidently at scale.

:::image type="content" source="media/overview/control-plane-operate.png" alt-text="Screenshot that shows the Operate toolbar button and the Overview pane in the Foundry workspace." lightbox="media/overview/control-plane-operate.png":::

### Overview

Use the **Overview** pane to understand fleet health, performance, and compliance at a glance.

:::image type="content" source="media/overview/control-plane-overview.gif" alt-text="Animation of the Overview pane that displays trend-based health scores, alert summaries, and aggregated compliance metrics for a fleet." lightbox="media/overview/control-plane-overview.gif":::

This pane provides a high-level snapshot of your AI estate by aggregating key operational and compliance metrics in one view. You can:

- View key statistics such as active agents, cost trends, run completion rate, and prevented behaviors.
- Drill into anomalies or cost spikes through contextual charts and direct links to inventory, observability, or policy information.
- Identify potential risks early by using trend-based health scores and alert summaries.

### Assets

Use the **Assets** pane to track, analyze, and manage every agent, model, and tool from one place.

:::image type="content" source="media/overview/assets-view.png" alt-text="Screenshot of an agent inventory table with filters and sort options applied to display metadata and health indicators for AI assets." lightbox="media/overview/assets-view.png":::

This pane provides a unified, searchable table of all AI assets across projects within a subscription. It brings together critical metadata and health indicators, so you can assess and act on your AI estate efficiently. You can:

- Filter and sort by key attributes such as version, tags, health score (percentage), cost, alerts, and token usage to locate assets quickly.
- Drill down from any entry in the agent inventory table into the [Evaluation](../../how-to/continuous-evaluation-agents.md) or [Monitoring](../../how-to/monitor-applications.md) tab for pre-deployment and post-deployment insights.
- Surface inline recommendations to refine prompts, upgrade models, or optimize configurations based on performance and cost signals.
- Correlate runtime logs with evaluation results to uncover root causes of errors or performance degradation.
- Visualize drift, latency, and error clusters across runs or builds to detect emerging issues early.
- Integrate with the [AI Red Teaming Agent](../../concepts/ai-red-teaming-agent.md) to automate vulnerability probing, regression testing, and issue reproduction.
- Observe and modify model and agent guardrails.

Together, these capabilities turn the **Assets** pane into the operational backbone of Foundry Control Plane. It's a single pane where you can understand, improve, and secure every AI asset in your environment.

### Compliance

Use the **Compliance** pane to govern your AI systems and enforce the right guardrails.

:::image type="content" source="media/overview/compliance.png" alt-text="Screenshot of the Compliance pane that shows options to define, apply, and monitor AI compliance policies with Azure Policy, Microsoft Defender, and Microsoft Purview integrations." lightbox="media/overview/compliance.png":::

The **Compliance** pane lets you define, apply, and continuously monitor guardrails and compliance policies across your AI estate. It provides a unified interface to operationalize responsible AI principles while helping to ensure enterprise-grade safety and regulatory alignment. You can:

- Define and enforce protections through deep integrations with Azure Policy, Defender, and Microsoft Purview. These integrations help ensure that identity, data, and threat safeguards work in concert.
- Apply versioned policies and track assignments to maintain full auditability and traceability across agents and environments.
- Monitor compliance posture in real time, so that you can surface noncompliant assets and enable bulk remediation directly from Foundry Control Plane.

Policy management in Foundry enables administrators and developers alike to embed quality and safety requirements into the development and deployment lifecycle. These policies help ensure that all models operate safely and adhere to organizational and regulatory standards.

### Quota

Use the **Quota** pane to view, adjust, and request quotas.

:::image type="content" source="media/overview/quota-view.png" alt-text="Screenshot of the Quota pane that shows model deployments, their quota usage, and usage patterns with options to adjust or request additional quotas." lightbox="media/overview/quota-view.png":::

The **Quota** pane shows your model deployments and how much quota each deployment is consuming. It gives insights into usage patterns and helps you manage resources effectively.

### Admin

Use the **Admin** pane to view, organize, and administer all projects, users, and connected resources across your Foundry environment.

:::image type="content" source="media/overview/admin-tab-overview.png" alt-text="Screenshot of the Admin pane that shows a list of projects with details like owners, region, connected services, and compliance status." lightbox="media/overview/admin-tab-overview.png":::

This pane extends your operational view beyond a single project. Most work in Foundry happens within a project context. The **Admin** pane provides an enterprise-level lens to oversee and configure multiple projects, user permissions, and linked Azure resources from one place.

From **Admin**, administrators and power users can:

- Gain visibility into all projects across their subscription or tenant, including active, inactive, and archived workspaces.
- View detailed project information such as owners, region, connected services, and compliance posture.
- Add or remove users directly from a project, to define granular access levels aligned with organizational roles.
- Attach or manage connected resources, such as storage accounts, compute clusters, and Foundry Tools, so that projects remain properly provisioned.
- Assign access at parent scope (subscription or resource group) to apply consistent governance and permissions inheritance across multiple projects.

Together, these capabilities make **Admin** the administrative backbone of Foundry Control Plane. It's a centralized console to help ensure that every Foundry project remains properly configured, compliant, and connected to the right people and infrastructure.

## Get started

Foundry Control Plane is available in the Foundry portal. To get started, complete these steps:

| Step | Description |
| ---- | ----------- |
| 1. [Configure an AI gateway](../configuration/enable-ai-api-management-gateway-portal.md) | Enable advanced governance features in your Foundry projects. |
| 2. [Configure monitoring for your agent fleet](monitoring-across-fleet.md) | Enable metrics and diagnostic information with observability features. |
| 3. [Discover agents in your subscription](how-to-manage-agents.md) | See which agents are available and manage them centrally. |
| 4. [Register custom agents](register-custom-agent.md) | Bring external agents into the Foundry Control Plane registry. |

## Related content

- [Manage compliance and security in Microsoft Foundry](how-to-manage-compliance-security.md): Enforce responsible AI policies, integrate Defender and Microsoft Purview signals, and respond to compliance alerts.
- [Optimize model cost and performance](how-to-optimize-cost-performance.md): Analyze cost drivers, token usage, and resource consumption to maximize the return on investment from your agent fleet.
- [Manage agents at scale](how-to-manage-agents.md): Track and manage agents from supported platforms in one unified view.
- [Continuously evaluate your AI agents (preview)](../../how-to/continuous-evaluation-agents.md): Monitor agent performance, quality, and risk dimensions automatically.
