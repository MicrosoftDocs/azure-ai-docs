---
title: Microsoft Foundry Notification Center overview
description: The Microsoft Foundry Notification Center surfaces security, policy, and performance alerts in one place. Explore key features to keep your AI solutions reliable.
#customer intent: As an AI developer using Microsoft Foundry, I want to understand what the Notification Center is, so that I can determine how it helps me monitor my AI agents and projects.
author: s-polly
ms.author: scottpolly
ms.reviewer: scottpolly
ms.date: 07/09/2026
ms.topic: concept-article
ms.service: microsoft-foundry
ai-usage: ai-assisted
---

# Microsoft Foundry Notification Center

Microsoft Foundry Notification Center centralizes all important observability alerts and notifications for your AI agents, models, and projects. Previously, developers had to manually monitor multiple siloed systems and configure Azure Monitor alerts to catch agent issues - an error-prone and time-consuming process. Now, the Notification Center automatically aggregates critical signals into a single in-app feed, so you can see and address problems directly within the Foundry portal, without complex setup.

By delivering timely notifications in the same UI where you manage your agents, the Notification Center helps you stay on top of issues in real time and maintain your AI solutions' reliability and compliance.

## Prerequisites

- An active Microsoft Foundry project. To create one, see [Create a project](../how-to/create-projects.md).
- Access to the [Foundry portal](https://ai.azure.com).

## Delivery channels

Currently, the Foundry web portal (in-app) delivers notifications. A small badge on the bell icon indicates new unread items whenever they arrive. 

## Key capabilities and alert coverage

The Foundry Notification Center provides a comprehensive alerting experience integrated into the Foundry web portal. Key capabilities include:

### Centralized notifications panel
A bell icon in the Foundry portal's header opens the Notification Center panel. This panel shows recent notifications (unread and read) with timestamps (for example, "3m ago") and short descriptions, giving you an immediate overview of new events. You can click any item to see details or navigate to the relevant resource for resolution. A **Dismiss All** action is available to mark all notifications as read (with a confirmation prompt) for quick cleanup.

### "View all" notifications page
For deeper review, a dedicated expanded view page lists all notifications in a table format, including older or previously-read items. Unlike the compact bell panel, this page is designed for detailed review, filtering, and auditing of notifications. You can sort or filter notifications by criteria like type, project, or severity (with more filtering options on the way). The **View All** page ensures you can explore your entire notification history across all categories of events, not just the latest alerts.

### Alert types covered
The Notification Center aggregates multiple categories of key events from across the Foundry environment. It supports four main types of notifications:

- **Security alerts (Defender)**: The Notification Center surfaces high-severity security issues, such as malicious activities or content safety violations flagged by Microsoft Defender for Cloud, through integration with Azure's security alert APIs. These alerts ensure that you're promptly informed of potential threats to your agents or underlying infrastructure.

- **Policy and compliance**: The Notification Center delivers notifications about issues arising from Azure Policy or Foundry's built-in guardrails, such as ML governance policy violations or required compliance actions. You can quickly address governance and compliance concerns.


- **Run completion and other events**: Certain long-running operations in Foundry, such as evaluation runs or model training jobs, trigger notifications upon completion or failure. These events push a notification to the center via Foundry's backend API as soon as they occur, ensuring near-real-time updates for these workflows.

## Use the Notification Center

> [!NOTE]
> These steps require portal access. For RBAC role requirements, see [Role-based access control for Microsoft Foundry](rbac-foundry.md).

**Accessing notifications**: In the Foundry portal, select the Notification Center (bell) icon to open the notifications panel. The panel displays a scrollable list of your most recent notifications, with each entry showing a concise description and an icon or color indicating its category or importance. New (unread) notifications are highlighted.

**Viewing details**: To learn more about a notification, select it in the panel. Selecting a notification opens a detailed view or relevant page:

For agent evaluation alerts or run completions, selecting an item might open the Foundry **Operate** page or evaluation results for the specific agent or run, where you can inspect metrics and logs around the time of the alert.

For security or policy alerts, selecting a notification directs you to the appropriate details. For example, a deep link to the Azure portal's security center or policy compliance page so you can investigate and remediate the issue.

**Marking notifications as read**: After you review an alert, the panel marks it as read automatically (the visual highlight disappears). In the notifications panel, you can use the **Dismiss All** button to mark all current notifications as read at once.



## Related content

- [Observability in generative AI](observability.md)
- [Monitor agents with the Agent Monitoring Dashboard](../observability/how-to/how-to-monitor-agents-dashboard.md)
- [Role-based access control for Microsoft Foundry](rbac-foundry.md)
- [Guardrails overview](../guardrails/guardrails-overview.md)
