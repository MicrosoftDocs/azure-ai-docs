---
title: Agentic Workflows Task Adherence (preview)
description: Learn how to use Task Adherence to ensure AI agents align with user instructions and task objectives.
author: ssalgadodev
ms.author: ssalgado
ms.service: azure-ai-content-safety
ms.topic: how-to
ms.date: 04/02/2026
zone_pivot_groups: programming-languages-content-safety-foundry-rest
---

# Agentic Workflows: Task Adherence (preview)

Ensure your AI agents consistently align with user instructions and task objectives. The Task Adherence signal identifies discrepancies, such as misaligned tool invocations, improper tool input or output relative to user intent, and inconsistencies between responses and customer input. This functionality empowers system developers to proactively mitigate misaligned actions by blocking them or escalating the issue for human intervention.

The primary objectives of the Task Adherence feature are:

- To detect tool actions that are misaligned with user goals or input intent, or improper tool input/output relative to user intent, or inconsistencies between agent responses and customer input.
- To provide reasoning when tool calls are misaligned.
- To provide a signal for downstream tool invocation blocking and escalation to human-in-the-loop (HITL) review when task alignment is at risk.
- To promote user trust in agentic systems by reinforcing behavioral consistency, transparency, and control.


::: zone pivot="programming-language-rest"

### Prerequisites

- An Azure subscription - [Create one for free](https://azure.microsoft.com/free/cognitive-services/)
- Once you have your Azure subscription, create a Content Safety resource in the Azure portal to get your key and endpoint. Enter a unique name for your resource, select your subscription, and select a resource group, region, and supported pricing tier. Then select **Create**.
  - The resource takes a few minutes to deploy. After it finishes, select **go to resource**. In the left pane, under **Resource Management**, select **Subscription Key and Endpoint**. The endpoint and either of the keys are used to call APIs.
- [cURL installed](https://curl.se).

### Request

> [!NOTE]
> For a prompt shield example, see [prompt shields](/azure/ai-services/content-safety/concepts/jailbreak-detection).

**API Version:** `2024-12-15-preview`

#### Fields in the URL

| Name | Required | Description | Type |
|------|----------|-------------|------|
| Endpoint | Yes | The base URL for the Content Safety API. Replace `<endpoint>` with the endpoint provided for your Azure service. | String |
| API Version | Yes | The version of the API to use. For this feature, the version is `2024-12-15-preview`. Example: `<endpoint>/contentsafety/agent:analyzeTaskAdherence?api-version=2024-12-15-preview` | String |

#### Parameters in the request body

| Name | Required | Description | Type |
|------|----------|-------------|------|
| tools | Yes | A list of tools that define functions to be used in the task. Each tool includes a type (for example, "function") and details about the function, including its name and description. | Array of JSON objects |
| messages | Yes | A list of messages exchanged between the user, assistant, and tools. Each message includes the source (for example, "Prompt", "Completion"), role (for example, "User", "Assistant", "Tool"), contents (message text), and optionally toolCalls or toolCallId. | Array of JSON objects |

#### Example request body schema

The following tables are descriptions of the key fields in the request body:

##### tools field

| Name | Required | Description | Type |
|------|----------|-------------|------|
| type | Yes | The type of tool being used. For this feature, it is "function" | String |
| function.name | Yes | The name of the function. For example, "read_emails" | String |
| function.description | Yes | A brief description of what the function does. For example, "Reads user's emails" | String |

##### messages field

| Name | Required | Description | Type |
|------|----------|-------------|------|
| source | Yes | The origin of the message. Possible values: "Prompt", "Completion" | String |
| role | Yes | The role associated with the message. Possible values: "User", "Assistant", "Tool" | String |
| contents | Yes | The content of the message. For example, "Summarize my emails" | String or array |
| toolCalls | No | A list of tool calls made by the agent, including type (for example, "function"), function.name, function.arguments, and a unique ID. | Array of JSON objects |
| toolCallId | No | (For Tool messages) The ID of the tool call being responded to. Matches the ID provided in the agent's tool call. | String |

### API response

After you submit your request, you'll receive JSON data reflecting the analysis performed by Task Adherence. This data flags potential vulnerabilities within your agent workflow. Here's what a typical output looks like:

```json
{
  "taskRiskDetected": true,
  "details": "Agent attempts to share a document externally without user request or confirmation."
}
```

| Name | Description | Type |
|------|-------------|------|
| taskRiskDetected | Contains risk detection results for the input | Boolean |
| details | Returns reasoning, when a risk is detected | String |

A value of `true` for `taskRiskDetected` signifies a detected risk, in which case we recommend review and action, such as blocking of the tool invocation request or human-in-the-loop escalation.

::: zone-end


::: zone pivot="programming-language-foundry-portal"

### Prerequisites

An Azure account. If you don't have one, you can create one for free.
An Azure AI resource.

### Set up and use Task Adherence

Follow these steps to use the **Content Safety try it out** page:

1. Go to Azure AI Foundry and navigate to your project/hub. Then select the **Guardrails + controls** tab on the left nav and select the Try it out tab.
1. On the **Try it out** page, you can experiment with various Guardrails & controls features such as text and image content, using adjustable thresholds to filter for harmful content.
1. Navigate to **Agentic Workflow** and select **Task Adherence**.
1. You can select one of the examples with aligned or misaligned agent tool calls or create your own to test Task Adherence.
1. Select **Run test**. Task Adherence returns the risk flag for each sample, and if a risk is detected, it returns a reason.

::: zone-end

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


## Related content

- [Azure AI Content Safety overview](/azure/ai-services/content-safety/overview)
- [Guardrails and controls overview](guardrails-overview.md)
- [Prompt shields](/azure/ai-services/content-safety/concepts/jailbreak-detection)
