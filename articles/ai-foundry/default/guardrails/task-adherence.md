---
title: Agentic Workflows Task Adherence (preview)
description: Learn how to use Task Adherence to ensure AI agents align with user instructions and task objectives.
author: ssalgadodev
ms.author: ssalgado
ms.service: azure-ai-content-safety
ms.topic: conceptual
ms.date: 11/06/2025
---

# Agentic Workflows: Task Adherence (preview)

Ensure your AI agents consistently align with user instructions and task objectives. The Task Adherence signal identifies discrepancies, such as misaligned tool invocations, improper tool input or output relative to user intent, and inconsistencies between responses and customer input. This functionality empowers system developers to proactively mitigate misaligned actions by blocking them or escalating the issue for human intervention.

## User scenarios

### Customer Support

**Scenario:** A customer support assistant integrated into an enterprise platform helps users check data usage, troubleshoot issues, and manage account settings. To maintain accurate automation, the system incorporates Task Adherence to validate agent plans before executing backend tool calls.

**User:** End-users, support agents, and customer experience teams.

**Action:** A user messages the chatbot: "Can you check how much data I've used this month?" The assistant plans to invoke a `change_data_plan()` tool. Task Adherence detects a misalignment between the user's intent (information request) and the proposed action (subscription change). The tool invocation can be blocked, and the system either halts execution or asks the user for review.

### Human Resources

**Scenario:** An enterprise assistant automates routine HR-related workflows such as booking leave, submitting expenses, and checking policy details. Task Adherence ensures that agent actions stay within the expected scope and do not take unintended shortcuts.

**User:** Employees, HR business partners, and workflow automation teams.

**Action:** An employee types: "I want to know how much annual leave I have left." The agent plans to invoke `apply_leave()`. Task Adherence identifies a task mismatch—the user asked for information, not to initiate a process. The execution is blocked; the agent rephrases or prompts for confirmation.

### Productivity Tools

**Scenario:** A productivity assistant embedded in an email platform helps professionals connect to databases, and draft, review, and send messages. Task Adherence is used to distinguish between writing a draft and executing a send command, especially in cases where user intent is ambiguous.

**User:** Knowledge workers, executive assistants, and IT compliance teams.

**Action:** The user prompts: "Write an email to the client about the missed deadline." The agent generates a message and plans to invoke `send_email()`. Task Adherence flags the plan as potentially premature; there is no explicit instruction to send. The system instead blocks the intended tool call, and prompts user review.

## Task Adherence: Aligned vs. Misaligned Tool Use

The Task Adherence API signal helps developers and platform owners understand when an agent's tool invocation matches or deviates from the user's intent.

### Examples

| Classification | Description | Example |
|----------------|-------------|---------|
| **Aligned** | Agent retrieves requested information without taking unintended action. | **User:** "Can you show me my recent calendar events?"<br>**Planned Tool:** `get_calendar_events()`<br>✅ Agent retrieves events as asked.<br><br>**Output:**<br> ```{   "taskRiskDetected": false }``` |
| **Misaligned** | Agent attempts to modify user settings when only an information request was made. | **User:** "Can you show me my recent calendar events?"<br>**Planned Tool:** `clear_calendar_events()`<br>❌ Agent prepares to delete data.<br><br>**Output:**<br>```{  "taskRiskDetected": true, "details": "Planned action deletes calendar events, but user only requested to view them."}``` |
| **Aligned** | Agent begins a document creation flow after user requests to generate a new document. | **User:** "Create a new project proposal document for the client."<br>**Planned Tool:** `create_document()`<br>✅ Matches the user's task request.<br><br>**Output:**<br>```{  "taskRiskDetected": false}``` |
| **Misaligned** | Agent shares the document with external collaborators without user instruction. | **User:** "Create a new project proposal document for the client."<br>**Planned Tool:** `share_document()`<br>❌ No user instruction to share.<br><br>**Output:**<br>```{  "taskRiskDetected": true,  "details": "Agent attempts to share a document externally without user request or confirmation."}``` |

## Limitations

### Language availability

Task Adherence has been tested on text in English; however, the feature can work in many other languages, though the quality might vary. In all cases, we recommend testing for your use case and application to ensure that it works for your scenarios.

### Text length limitation

Currently, the task adherence API has input length limitations. The maximum text length is 100,000 characters. If your input length exceeds this limitation, you'll receive an error.

### Region availability and data processing

While Task Adherence can be enabled in all Azure AI Content Safety regions, data may be routed to and processed in other US and EU regions outside the specified Geo.

## Next steps

> [!div class="nextstepaction"]
> [Azure AI Content Safety documentation](/azure/ai-services/content-safety/)

## Related content

- [Azure AI Content Safety overview](/azure/ai-services/content-safety/overview)
- [Guardrails and controls overview](guardrails-overview.md)
