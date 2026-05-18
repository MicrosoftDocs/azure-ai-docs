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

Foundry tracing is an observability capability in Microsoft Foundry that captures execution data from AI agents. It helps developers and operators understand system behavior, debug problems, and optimize performance. 

Tracing records information such as: 

- User inputs and prompts
- Agent and model inputs and outputs 
- Tool calls and intermediate steps 
- Execution metadata (timestamps, latency, token usage, errors, etc.) 

This data might include user-generated content and operational telemetry. 

This data is used to provide visibility into how agents run, enabling troubleshooting and performance improvements across agent workflows. Foundry uses OpenTelemetry standards and stores trace data in connected telemetry systems Azure Monitor Application Insights.  

> [!IMPORTANT]
> Default state:
>
> - **Tracing is off by default.**
> - No trace data is collected or stored unless explicitly enabled by Foundry Owner.

This ensures customers retain control over when data collection begins and aligns with privacy-by-default expectations. 

## Enable tracing 

Tracing is enabled when a project is connected to an Azure Monitor Application Insights resource. Common enablement flows include: 

- Creating or connecting an Application Insights resource during project creation. 
- Creating or connecting an Application Insights resource to an existing project without a connected Application Insights resource. 

When you enable tracing: 

- Trace data begins to be collected and stored.
- Traces become visible in Foundry Tracing UI. 

## Disable tracing

Disable tracing by: 

- Disconnecting or removing the Application Insights resource. 

After you disable tracing: 

- No new trace data is collected. 
- Previously collected data remains subject to retention policies of the Application Insights. 

> [!NOTE]
> Exact steps depend on the UI or SDK surface and should align with product documentation. 

## Where data is stored

- The Application Insights resource connected to the Foundry project stores trace data. 
- Your Application Insights and Log Analytics configuration governs data retention and storage. 

## Data sharing considerations

- Trace data may be accessible to users with appropriate permissions on the connected telemetry resource. 
- Depending on the configuration, users within the same project or tenant might see data.
- For hosted or external agents, you can control where trace data is sent. 

Customers are responsible for configuring access controls and ensuring compliance with their organizational policies. 

## Privacy and sensitive data

Tracing can capture sensitive information, including: 

- Personal data
- User prompts and responses 
- Application-specific content 

### Best practices: 

- Avoid logging secrets, credentials, or sensitive tokens.
- Redact or minimize personal data before it is logged.
- Apply access controls and retention policies to trace data. 

## Data protection controls 

- PII redaction: Redact common sensitive data, such as email addresses and phone numbers.
- RBAC (role-based access control): Restrict access to trace data to the Log Analytics Reader role.
- Configurable policies: Control what data is captured and visible. 

These controls help you manage risk and comply with privacy requirements.  

Customer responsibilities 

When you enable tracing, you're responsible for: 

- Informing end users about data collection (where applicable).
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