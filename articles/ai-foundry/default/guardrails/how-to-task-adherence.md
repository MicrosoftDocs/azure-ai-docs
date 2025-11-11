---
title: How to Use Task Adherence for Your Agentic Workflows
description: Learn how to use the Task Adherence feature to ensure AI agents execute tool actions aligned with user instructions and intent.
author: ssalgadodev
ms.author: ssalgado
ms.service: azure-ai-content-safety
ms.topic: quickstart
ms.date: 11/06/2025
---

# How to use Task Adherence for your Agentic workflows

In this quickstart, you use the Task Adherence feature. The Task Adherence API for agentic workflows is designed to ensure that AI agents execute tool actions that are aligned with the user's instructions and intent. This feature helps detect and prevent situations where an agent takes an action that are unintended or premature, especially when invoking tools that affect user data, perform high-risk actions, or initiate external operations.


Task Adherence is critical in systems where agents have the ability to plan and act autonomously. By verifying that planned tool invocations match the user and task instructions, and flagging misaligned tool use, Task Adherence helps maintain system reliability, user trust, and safety.


The primary objectives of the Task Adherence feature are:

- To detect tool actions that are misaligned with user goals or input intent, or improper tool input/output relative to user intent, or inconsistencies between agent responses and customer input.
- To provide reasoning when tool calls are misaligned.
- To provide a signal for downstream tool invocation blocking and escalation to human-in-the-loop (HITL) review when task alignment is at risk.
- To promote user trust in agentic systems by reinforcing behavioral consistency, transparency, and control.

For more information on how Task Adherence works, see the [Task Adherence concepts page](task-adherence.md).

## Prerequisites

- An Azure subscription - [Create one for free](https://azure.microsoft.com/free/cognitive-services/)
- Once you have your Azure subscription, create a Content Safety resource in the Azure portal to get your key and endpoint. Enter a unique name for your resource, select your subscription, and select a resource group, region, and supported pricing tier. Then select **Create**.
  - The resource takes a few minutes to deploy. After it finishes, select **go to resource**. In the left pane, under **Resource Management**, select **Subscription Key and Endpoint**. The endpoint and either of the keys are used to call APIs.
- [cURL installed](https://curl.se).

## Request

> [!NOTE]
> For a prompt shield example, see [prompt shields](/azure/ai-services/content-safety/concepts/jailbreak-detection).

**API Version:** `2024-12-15-preview`

### Fields in the URL

| Name | Required | Description | Type |
|------|----------|-------------|------|
| Endpoint | Yes | The base URL for the Content Safety API. Replace `<endpoint>` with the endpoint provided for your Azure service. | String |
| API Version | Yes | The version of the API to use. For this feature, the version is `2024-12-15-preview`. Example: `<endpoint>/contentsafety/agent:analyzeTaskAdherence?api-version=2024-12-15-preview` | String |

### Parameters in the request body

| Name | Required | Description | Type |
|------|----------|-------------|------|
| tools | Yes | A list of tools that define functions to be used in the task. Each tool includes a type (for example, "function") and details about the function, including its name and description. | Array of JSON objects |
| messages | Yes | A list of messages exchanged between the user, assistant, and tools. Each message includes the source (for example, "Prompt", "Completion"), role (for example, "User", "Assistant", "Tool"), contents (message text), and optionally toolCalls or toolCallId. | Array of JSON objects |

### Example request body schema

The following tables are descriptions of the key fields in the request body:

#### tools field

| Name | Required | Description | Type |
|------|----------|-------------|------|
| type | Yes | The type of tool being used. For this feature, it is "function" | String |
| function.name | Yes | The name of the function. For example, "read_emails" | String |
| function.description | Yes | A brief description of what the function does. For example, "Reads user's emails" | String |

#### messages field

| Name | Required | Description | Type |
|------|----------|-------------|------|
| source | Yes | The origin of the message. Possible values: "Prompt", "Completion" | String |
| role | Yes | The role associated with the message. Possible values: "User", "Assistant", "Tool" | String |
| contents | Yes | The content of the message. For example, "Summarize my emails" | String or array |
| toolCalls | No | A list of tool calls made by the agent, including type (for example, "function"), function.name, function.arguments, and a unique ID. | Array of JSON objects |
| toolCallId | No | (For Tool messages) The ID of the tool call being responded to. Matches the ID provided in the agent's tool call. | String |

## API response

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


## Related content

- [Azure AI Content Safety overview](/azure/ai-services/content-safety/overview)
- [Prompt shields](/azure/ai-services/content-safety/concepts/jailbreak-detection) 
