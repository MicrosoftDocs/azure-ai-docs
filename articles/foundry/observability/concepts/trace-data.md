---
title: Microsoft Foundry Tracing and Data Handling
description: Tracing in Microsoft Foundry captures execution data to improve AI agent performance. Find out how to enable, disable, and govern trace data.
ai-usage: ai-assisted
author: lgayhardt
ms.author: lagayhar
ms.reviewer: ychen
ms.topic: concept-article
ms.date: 06/02/2026
ms.service: microsoft-foundry

---

# Tracing and data handling

Foundry tracing is an observability capability in Microsoft Foundry that captures Customer Data from AI agents. It helps developers and operators understand system behavior, debug problems, and optimize performance.

Tracing records information such as:

- User inputs and prompts
- Agent and model inputs and outputs
- Tool calls and intermediate steps
- Execution metadata (timestamps, latency, token usage, errors, etc.)

This data might include user-generated content and operational telemetry.

This data is used to provide visibility into how agents run, enabling troubleshooting and performance improvements across agent workflows. Foundry uses OpenTelemetry standards and stores trace data in connected telemetry systems Azure Monitor Application Insights.  

> [!IMPORTANT]
> When AppInsights is enabled for a Project, AppInsights logs traces to help monitor and evaluate user level interactions with agents. Project members provided with Log Analytics Reader role in AppInsights will be able to view trace data, which may contain personal data and/or Customer Content.  Be sure to review what trace data is collected and who may view and use this data.  More information is below.
>
> Default state:
>
> - **Tracing is off by default.**
> - No trace data is collected or stored unless explicitly enabled by Foundry Account Owner or Foundry Owner.
>
> Additional [Azure Monitor App Insights pricing](https://azure.microsoft.com/pricing/details/monitor/) might apply.

This ensures customers retain control over when data collection begins.

## Enable tracing

Tracing is enabled when a project is connected to an Azure Monitor Application Insights resource. Common enablement flows include:

- Creating or connecting an Application Insights resource during project creation.
- Creating or connecting an Application Insights resource to an existing project without a connected Application Insights resource.

When you enable tracing:

- Trace data begins to be collected and stored for all agents within the project.
- To view traces in the Foundry Tracing UI, users need access to the Foundry project and read permission on the connected Application Insights / Log Analytics workspace. For example, this can be granted through roles such as Log Analytics Reader, Monitoring Reader, or Reader at the Application Insights resource, Log Analytics workspace, or an appropriate parent scope.

## Disable tracing

Disable tracing by:

- Disconnecting or removing the Application Insights resource.

After you disable tracing:

- No new trace data is collected on agents in that project.
- Previously collected data remains subject to retention policies of the Application Insights.

> [!NOTE]
> Exact steps on how to disable tracing depend on the UI or SDK surface and should align with product documentation.

## Where data is stored

- The Application Insights resource connected to the Foundry project stores trace data. 
- Your Application Insights and Log Analytics configuration governs data retention and storage. 

## Data sharing considerations

- Trace data may be accessible to users with appropriate permissions on the connected telemetry resource.
- Depending on the configuration, users within the same project or tenant might see data.
- To view traces in the Foundry Tracing UI, users need access to the Foundry project and read permission on the connected Application Insights / Log Analytics workspace. For example, this can be granted through roles such as Log Analytics Reader, Monitoring Reader, or Reader at the Application Insights resource, Log Analytics workspace, or an appropriate parent scope.
- For additional considerations and important information specific to hosted agents, review [hosted agent](../../agents/concepts/hosted-agents.md) and [hosted agent's platform-injected environment variables](../../agents/how-to/deploy-hosted-agent.md#platform-injected-environment-variables).

Customers are responsible for configuring access controls and ensuring compliance with their organizational policies.

## Privacy

Tracing can capture personal data including:

- User prompts and responses
- Application-specific content

### Best practices

- Avoid logging secrets, credentials, or tokens.
- Redact or minimize personal data before it is logged.
- Apply access controls and retention policies to trace data.

### Data protection controls

- Personal data redaction: Redact personal data, such as email addresses and phone numbers.
- Restrict access to trace data by carefully managing which users have been granted the RBAC “Log Analytics Reader” role.
- Configurable policies: Control what data is captured and visible.

These controls help you manage risk and comply with privacy requirements.  

### Customer responsibilities

When you enable tracing, you're responsible for:

- Informing end users about data collection, including the types of data being collected, the purpose, who has visibility, their options, and other information needed for them to make reasonable choices (where applicable).
- Ensuring compliance with privacy, legal, and regulatory requirements.
- Configuring appropriate access controls and data retention policies.

## Summary

Foundry Tracing is a powerful observability feature that enables debugging, monitoring, and optimization of AI agents. It is: 

- Off by default.
- Explicitly enabled by connecting telemetry resources.
- Designed with customer control over data collection and handling.

## Related content

- [Agent tracing overview](./trace-agent-concept.md)
- [Set up tracing](../how-to/trace-agent-setup.md)
- [Configure tracing for AI agent frameworks](../how-to/trace-agent-framework.md)
