---
title: What is the Microsoft Foundry Control Plane?
ms.service: azure-ai-foundry
ms.topic: concept-article
ms.date: 02/05/2026
ms.reviewer: mesameki
ms.author: scottpolly
author: mesameki
description: Learn about the Foundry Control Plane, a unified management interface that provides visibility, governance, and control for AI agents, models, and tools across your Microsoft Foundry enterprise.
ai-usage: ai-assisted
#customer intent: As an enterprise administrator or AI developer, I want to understand what the Foundry Control Plane is and how it provides unified visibility across my AI fleet so that I can determine if it meets my governance and operational needs.
---

# What is the Microsoft Foundry Control Plane?

The **Microsoft Foundry Control Plane** is a unified management interface that provides visibility, governance, and control for AI agents, models, and tools across your Foundry enterprise. Use the Foundry Control Plane as your central location for managing every aspect of your AI fleet, from build to production.

As your organization evolves from isolated copilots to autonomous multi-agent fleets, you need unified oversight. The Foundry Control Plane provides the visibility, governance, and control you need to scale with confidence.

In this article, you learn what the Foundry Control Plane offers, including fleet management, observability, compliance enforcement, and security capabilities.

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

## Core functionalities

The Foundry Control Plane consolidates **inventory, observability, compliance, and security** into one role-aware interface. It integrates seamlessly with Microsoft security and governance systems (Defender, Purview, Microsoft Entra) to deliver **trust at scale**.

The following diagram shows how the Foundry Control Plane provides unified fleet visibility with agents, models, and tools listed across projects in a subscription:

:::image type="content" source="media/overview/control-plane-overall.png" alt-text="A diagram depicting the Foundry Control Plane unified fleet visibility with agents, models, and tools listed across projects in a subscription." lightbox="media/overview/control-plane-overall.png":::

The Foundry Control Plane allows you to:

### Manage your fleet across Foundry, Microsoft, and third-party agents in one place

- Track key performance indicators such as active agents, run completion, compliance posture, cost efficiency, and prohibited behaviors across [supported agent platforms](how-to-manage-agents.md#supported-agent-platforms).

- Use deep links to evaluation and monitoring experiences for rapid debugging, diagnosis, and remediation.

- Visualize fleet health through intuitive dashboards that surface trends and anomalies instantly.

### Observe, protect, and improve

- Correlate alerts, evaluation results, and trace data to pinpoint problems instantly.

- [Continuously evaluate](../../how-to/continuous-evaluation-agents.md) agent performance, quality, and risk dimensions such as **[Task Adherence, Intent Resolution, Tool Call Success](../../concepts/evaluation-evaluators/agent-evaluators.md), [Groundedness](../../concepts/evaluation-evaluators/rag-evaluators.md), Sensitive Data Leakage, and Jailbreak/XPIA exposure.**

- Use the [**AI Red Teaming Agent**](../../concepts/ai-red-teaming-agent.md) and [**cluster analysis**](../observability/how-to/cluster-analysis.md) for automated vulnerability probing and error root-cause discovery.

- Let **Foundry Agent** recommend improvements, from prompt refinements to model version upgrades.

### Govern and enforce with guardrails

- Define enterprise-wide guardrail policies for safety, compliance, and quality.

- Apply **bulk remediation** to instantly correct noncompliant configurations across your fleet.

### Secure agents

- Schedule **automated red-teaming scans** and **drift monitoring** for ongoing agent testing.

- View Defender and Purview alerts directly in the Control Plane dashboard.

- Track rate limits, token usage, and cost anomalies to prevent inefficiency or abuse.

## Key features

The Foundry Control Plane experience begins in the **Operate** tab, your command center on the upper right-hand side of the Foundry workspace. From Operate, you can monitor, govern, and optimize every agent, model, and deployment within your subscription. Each sub-tab within Operate is designed around a specific job-to-be-done (JTBD), helping different roles, from builders to administrators, manage AI systems confidently at scale.

:::image type="content" source="media/overview/control-plane-operate.png" alt-text="A screenshot showing the Operate tab in the upper navigation." lightbox="media/overview/control-plane-operate.png":::

### Overview

Use this page to understand fleet health, performance, and compliance at a glance.

:::image type="content" source="media/overview/control-plane-overview.gif" alt-text="Animation of the Fleet Overview page displaying trend-based health scores, alert summaries, and aggregated compliance metrics." lightbox="media/overview/control-plane-overview.gif":::

The Fleet Overview page provides a high-level snapshot of your AI estate, aggregating key operational and compliance metrics in one view.

- View key stats such as active agents, cost trends, run completion rate, and prevented behaviors.
- Drill into anomalies or cost spikes through contextual charts and direct links to Inventory, Observability, or Policy pages.
- Identify potential risks early with trend-based health scores and alert summaries.

### Assets

Use this view to track, analyze, and manage every agent, model, and tool from one place.

:::image type="content" source="media/overview/assets-view.png" alt-text="Screenshot of the Agent Inventory table with filters and sort options applied, displaying metadata and health indicators for AI assets." lightbox="media/overview/assets-view.png":::

The **Inventory** view provides a unified, searchable table of all AI assets across projects within a subscription. It brings together critical metadata and health indicators, so you can assess and act on your AI estate efficiently.

- Filter and sort by key attributes such as version, tags, health score (%), cost, alerts, and token usage to locate assets quickly.
- Drill down from any entry in the **Agent Inventory** table into **[Evaluation](../../how-to/continuous-evaluation-agents.md)** or **[Monitoring](../../how-to/monitor-applications.md)** tabs for pre- and post-deployment insights.
- Surface inline recommendations to refine prompts, upgrade models, or optimize configurations based on performance and cost signals.
- Correlate runtime logs with evaluation results to uncover root causes of errors or performance degradation.
- Visualize drift, latency, and error clusters across runs or builds to detect emerging issues early.
- Integrate with the **[**AI Red Teaming Agent**](../../concepts/ai-red-teaming-agent.md)** to automate vulnerability probing, regression testing, and issue reproduction.
- Observe and modify model and agent guardrails.

Together, these capabilities turn the Inventory into the operational backbone of the Control Plane, a single pane to understand, improve, and secure every AI asset in your environment.

### Compliance

Use this tab to govern your AI systems and enforce the right guardrails.

:::image type="content" source="media/overview/compliance.png" alt-text="Screenshot of the Policy & Security tab showing options to define, apply, and monitor AI compliance policies with Azure Policy, Defender, and Purview integrations." lightbox="media/overview/compliance.png":::

The **Policy & Security** tab empowers organizations to define, apply, and continuously monitor guardrails and compliance policies across their AI estate. It provides a unified interface to operationalize Responsible AI principles while ensuring enterprise-grade safety and regulatory alignment.

- Define and enforce protections through deep integrations with **Azure Policy**, **Microsoft Defender**, and **Purview**, ensuring that identity, data, and threat safeguards work in concert.
- Apply versioned policies and track assignments to maintain full auditability and traceability across agents and environments.
- Monitor compliance posture in real time, surfacing noncompliant assets and enabling bulk remediation directly from the Control Plane.

Policy Management in Foundry allows administrators and developers alike to embed quality and safety requirements into the development and deployment lifecycle. These policies ensure that all models operate safely, adhering to organizational and regulatory standards.


### Quota

Use this tab to view, adjust, and request quotas.

:::image type="content" source="media/overview/quota-view.png" alt-text="Screenshot of the Quota tab showing model deployments, their quota usage, and usage patterns with options to adjust or request additional quotas." lightbox="media/overview/quota-view.png":::

The **Quota** tab shows your model deployments and how much quota each deployment is consuming. It gives insights into usage patterns and helps you manage resources effectively. 

### Admin

Use this tab to view, organize, and administer all projects, users, and connected resources across your Foundry environment.

:::image type="content" source="media/overview/admin-tab-overview.png" alt-text="Screenshot of the Admin tab showing a list of projects with details like owners, region, connected services, and compliance status." lightbox="media/overview/admin-tab-overview.png":::

The **[Admin](../../concepts/management-center.md)** tab extends your operational view beyond a single project. While most work in Foundry takes place within a project context, **Admin** provides an enterprise-level lens to oversee and configure multiple projects, user permissions, and linked Azure resources from one place.

From **Operate → Admin**, administrators and power users can:

- Gain visibility into all projects across their subscription or tenant, including active, inactive, and archived workspaces.
- View detailed project information such as owners, region, connected services, and compliance posture.
- Add or remove users directly from a project, defining granular access levels aligned with organizational roles.
- Attach or manage connected resources, such as storage accounts, compute clusters, and Foundry Tools, ensuring projects remain properly provisioned.
- Assign access at parent scope (subscription or resource group) to apply consistent governance and permissions inheritance across multiple projects.

Together, these capabilities make **Admin** the Control Plane's administrative backbone. It's a centralized console to ensure every Foundry project remains properly configured, compliant, and connected to the right people and infrastructure.

## Get started

The Foundry Control Plane is a feature available in the Foundry (new) portal. To get started, complete these steps:

| Step | Description |
|------|-------------|
| 1. [Configure AI Gateway](../configuration/enable-ai-api-management-gateway-portal.md) | Enable advanced governance features in your Foundry projects. |
| 2. [Configure monitoring for your agents fleet](monitoring-across-fleet.md) | Enable metrics and diagnostic information with observability features. |
| 3. [Discover agents in your subscription](how-to-manage-agents.md) | See which agents are available and manage them centrally. |
| 4. [Register custom agents](register-custom-agent.md) | Bring third-party or external agents into the Foundry Control Plane registry. |

## Related content

- [Ensure compliance and security](how-to-manage-compliance-security.md) - Enforce Responsible AI policies, integrate Defender and Purview signals, and respond to compliance alerts.
- [Optimize model cost and performance](how-to-optimize-cost-performance.md) - Analyze cost drivers, token usage, and resource consumption to maximize ROI from your agent fleet.
- [Manage agents across platforms](how-to-manage-agents.md) - Track and manage agents from supported platforms in one unified view.
- [Set up continuous evaluation](../../how-to/continuous-evaluation-agents.md) - Monitor agent performance, quality, and risk dimensions automatically.

