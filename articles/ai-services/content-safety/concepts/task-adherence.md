---
title: Task Adherence in Azure AI Content Safety
description: Learn about Task Adherence, a feature in Azure AI Content Safety that helps ensure AI agents align with user instructions and task objectives by detecting misaligned tool use.
author: PatrickFarley
ms.author: pafarley
ms.service: azure-ai-content-safety
ms.topic: concept-article
ms.date: 08/13/2025
manager: nitinme
---

# Agent Workflows: Task Adherence (preview) 

Ensure your AI agents consistently align with user instructions and task objectives. The Task Adherence feature identifies discrepancies such as misaligned [tool invocations](/azure/ai-foundry/agents/how-to/tools/overview), improper tool input or output relative to user intent, and inconsistencies between responses and customer input. This feature lets system developers proactively mitigate misaligned actions by blocking them or escalating the issue for human intervention.

The primary objectives of Task Adherence are: 
- To detect tool actions that are misaligned with user goals or input intent, or improper tool input/output relative to user intent, or inconsistencies between agent responses and customer input. 
- To provide reasoning when tool calls are misaligned.
- To provide a signal for downstream tool invocation blocking and escalation to human-in-the-loop review when task alignment is at risk.
- To promote user trust in agentic systems by reinforcing behavioral consistency, transparency, and control.

## User scenarios

### Customer support 

Scenario: A customer support assistant chatbot integrated into an enterprise platform helps users check data usage, troubleshoot issues, and manage account settings. To maintain accurate automation, the system incorporates Task Adherence to validate agent plans before executing backend tool calls. 

User: End-users, support agents, and customer experience teams.

Action: A user messages the chatbot: "Can you check how much data I’ve used this month?" The assistant plans to invoke a `change_data_plan()` tool. Task Adherence detects a misalignment between the user’s intent (information request) and the proposed action (subscription change). The tool invocation can be blocked, and the system either halts execution or asks the user for review.

### Human resources 

Scenario: An enterprise assistant chatbot automates routine HR-related workflows such as booking leave, submitting expenses, and checking policy details. Task Adherence ensures that agent actions stay within the expected scope and don't take unintended shortcuts.

User: Employees, HR business partners, and workflow automation teams.

Action: An employee writes: "I want to know how much annual leave I have left." The agent plans to invoke `apply_leave()`. Task Adherence identifies a task mismatch: the user asked for information, not to initiate a process. The execution is blocked, and the agent rephrases or prompts for confirmation. 

### Productivity tools 

Scenario: A productivity assistant chatbot embedded in an email platform helps professionals connect to databases and draft, review, and send messages. Task Adherence is used to distinguish between writing a draft and executing a send command, especially in cases where user intent is ambiguous. 

User: Knowledge workers, executive assistants, and IT compliance teams.

Action: The user prompts: "Write an email to the client about the missed deadline." The agent generates a message and plans to invoke `send_email()`. Task Adherence flags the plan as potentially premature: there's no explicit instruction to send. The system instead blocks the intended tool call and prompts user review. 

## Aligned vs. misaligned tool use 

This Task Adherence API signal helps developers and platform owners understand when an agent’s tool invocation matches or deviates from the user's intent.

### Examples

| Classification | Action | Example |
|--|--| 
| Aligned | Agent retrieves requested information without taking unintended action. | **User**: "Can you show me my recent calendar events?"<br>**Planned Tool**: get_calendar_events()<br>✅ Agent retrieves events as asked.<br>**Output**:<br>`{"taskRiskDetected":false}` | 
| Misaligned | Agent attempts to modify user settings when only an information request was made. | **User**: "Can you show me my recent calendar events?"<br>**Planned Tool**: clear_calendar_events()<br>❌ Agent prepares to delete data.<br>**Output**:<br>`{"taskRiskDetected": true,"details": "Planned action deletes calendar events, but user only requested to view them."}` |
| Aligned | Agent begins a document creation flow after user requests to generate a new document. | **User**: "Create a new project proposal document for the client."<br>**Planned Tool**: create_document()<br>✅ Matches the user’s task request.<br>**Output**:<br>`{"taskRiskDetected": false }` | 
| Misaligned | Agent shares the document with external collaborators without user instruction. | **User**: "Create a new project proposal document for the client."<br>**Planned Tool**: share_document()<br>❌ No user instruction to share.<br>**Output**:<br>`{"taskRiskDetected": true, "details": "Agent attempts to share a document externally without user request or confirmation."}` | 



## Limitations 

### Language availability 

Task Adherence is tested on text in English. However, the feature can work in many other languages, but the quality might vary. In all cases, we recommend testing for your use case and application to ensure that it works for your scenarios.

### Text length limitation 

See [Input requirements](/azure/ai-services/content-safety/overview#input-requirements) for maximum text length limitations.


### Region availability and data processing 

While Task Adherence can be enabled in all Azure AI Content Safety regions, customer data might be routed to and processed in US and EU regions outside their specified region.


