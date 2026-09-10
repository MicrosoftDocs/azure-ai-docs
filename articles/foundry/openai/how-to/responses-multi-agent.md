---
title: "Use multi-agent orchestration with the Azure OpenAI Responses API"
description: "Learn how to use multi-agent orchestration with the Azure OpenAI Responses API to delegate parallel work, handle tools, and inspect agent output."
author: alvinashcraft
ms.author: aashcraft
ms.service: microsoft-foundry
ms.subservice: foundry-openai
ms.topic: how-to
ms.date: 08/11/2026
ms.custom:
  - doc-kit-assisted
ai-usage: ai-assisted
---

# Use multi-agent orchestration with the Azure OpenAI Responses API

By using multi-agent orchestration, a model can create and coordinate subagents in parallel, then combine their work into a final response. Use it for complex tasks that benefit from independent workstreams, such as code review, research, documentation, and implementation. This feature is in preview and is available with GPT-5.6 models.

## Prerequisites

- An Azure OpenAI resource in a region that supports the [Responses API](responses.md).
- A GPT-5.6 model deployment. Check [model availability](../../foundry-models/concepts/models-sold-directly-by-azure-region-availability.md?pivots=standard) before you create the deployment.
- Python 3.10 or later.
- For Microsoft Entra ID authentication, the `Cognitive Services OpenAI User` role assigned to your identity.
- For REST requests, cURL and the Azure CLI signed in to your Azure subscription.
- The latest OpenAI and Azure Identity packages:

  ```bash
  pip install --upgrade openai azure-identity
  ```

## Choose when to use multi-agent orchestration

Use multi-agent orchestration when a task can be divided into concrete, independent workstreams.

| Use multi-agent orchestration when | Prefer one agent when |
| --- | --- |
| Work can be split into independent, bounded tasks. | Each step depends directly on the previous step. |
| Separate context improves focus. | The task is small enough to complete in one short run. |
| Parallel exploration can reduce wall-clock time. | Agents would contend over the same mutable resource. |
| Comparing independent findings improves coverage. | You require a fixed, deterministic execution graph. |

Adding subagents can increase token usage. It might not improve tasks that require an ordered chain of reasoning, frequent writes to shared state, or one slow external operation.

## Create a multi-agent response

Use the beta Responses client with `api-version=preview`. Set `multi_agent.enabled` to `true` to let the root agent create subagents. In Azure OpenAI requests, `model` contains your deployment name, which doesn't have to match the underlying model name.

The following example asks three subagents to evaluate separate disaster-recovery proposals. Each proposal includes enough information for a subagent to work independently, and the root agent reconciles their findings against shared requirements.

1. Replace `YOUR-RESOURCE-NAME` with your Azure OpenAI resource name.
1. If your deployment name isn't `gpt-5.6-sol`, replace the value of `model` with your deployment name.
1. Run the code, and confirm that the output contains one consolidated review from `/root`.

```python
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import OpenAI

# Configure Microsoft Entra ID credentials.
endpoint = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/"
scope = "https://ai.azure.com/.default"
token_provider = get_bearer_token_provider(DefaultAzureCredential(), scope)
openai = OpenAI(
    base_url=endpoint,
    api_key=token_provider,
    default_query={"api-version": "preview"},
)

# Delegate each proposal to a separate subagent.
prompt = """
Evaluate three disaster-recovery proposals. Create one subagent per proposal.
Each subagent must assess recovery targets, monthly cost, and operational risk.

Alpha: Active-active across two regions; RTO under 5 minutes; near-zero RPO;
$42,000/month; quarterly failover tests.
Beta: Warm standby; 30-minute RTO; 5-minute RPO; $18,000/month;
monthly failover tests.
Gamma: Backup and restore; 8-hour RTO; 24-hour RPO; $6,000/month;
annual restore test.

The checkout system requires RTO <= 30 minutes, RPO <= 5 minutes, and a
monthly budget <= $20,000. After the subagents finish, compare their evidence
in a table and recommend one proposal. Explain any residual risk.
"""

response = openai.beta.responses.create(
    model="gpt-5.6-sol",
  input=prompt,
    multi_agent={"enabled": True, "max_concurrent_subagents": 3},
)

# Print only the root agent's final answer.
for item in response.output:
    if (
        item.type == "message"
        and item.phase == "final_answer"
        and item.agent
        and item.agent.agent_name == "/root"
    ):
        for part in item.content:
            if part.type == "output_text":
                print(part.text)
```

Reference: [Azure OpenAI v1 API authentication](../api-version-lifecycle.md) | [Use the Azure OpenAI Responses API](responses.md)

The output contains the root agent's comparison and recommendation. Response wording can vary, but the result should identify Beta as the only proposal that meets all stated recovery and budget requirements.

```output
| Proposal | Recovery targets | Monthly cost | Operational risk |
| ... | ... | ... | ... |

Recommendation: Beta meets the stated RTO, RPO, and budget requirements.
```

To use an Azure OpenAI API key instead, set `AZURE_OPENAI_API_KEY`, and create the client as follows:

```python
import os

from openai import OpenAI

# Authenticate with an Azure OpenAI API key.
endpoint = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/"
openai = OpenAI(
    base_url=endpoint,
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
    default_query={"api-version": "preview"},
)
```

Reference: [Azure OpenAI v1 API authentication](../api-version-lifecycle.md)

### Send a REST request

For REST requests, use the Azure OpenAI v1 endpoint and add `api-version=preview`.

### Microsoft Entra ID

Set `AZURE_OPENAI_AUTH_TOKEN` to an access token for the Azure AI audience:

```bash
export AZURE_OPENAI_AUTH_TOKEN=$(
  az account get-access-token \
    --resource https://ai.azure.com \
    --query accessToken \
    --output tsv
)
```

Reference: [Azure OpenAI v1 API authentication](../api-version-lifecycle.md)

```bash
curl -X POST "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/responses?api-version=preview" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AZURE_OPENAI_AUTH_TOKEN" \
  -d '{
    "model": "gpt-5.6-sol",
    "input": "Evaluate three disaster-recovery proposals with one subagent per proposal. Alpha: active-active, RTO under 5 minutes, near-zero RPO, $42,000/month. Beta: warm standby, 30-minute RTO, 5-minute RPO, $18,000/month. Gamma: backup and restore, 8-hour RTO, 24-hour RPO, $6,000/month. The checkout system requires RTO at most 30 minutes, RPO at most 5 minutes, and a monthly budget at most $20,000. Compare the evidence and recommend one proposal.",
    "multi_agent": {
      "enabled": true,
      "max_concurrent_subagents": 3
    }
  }'
```

Reference: [Use the Azure OpenAI Responses API](responses.md)

### API key

Set `AZURE_OPENAI_API_KEY` to a key from your Azure OpenAI resource:

```bash
export AZURE_OPENAI_API_KEY="<your-api-key>"
```

```bash
curl -X POST "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/responses?api-version=preview" \
  -H "Content-Type: application/json" \
  -H "api-key: $AZURE_OPENAI_API_KEY" \
  -d '{
    "model": "gpt-5.6-sol",
    "input": "Evaluate three disaster-recovery proposals with one subagent per proposal. Alpha: active-active, RTO under 5 minutes, near-zero RPO, $42,000/month. Beta: warm standby, 30-minute RTO, 5-minute RPO, $18,000/month. Gamma: backup and restore, 8-hour RTO, 24-hour RPO, $6,000/month. The checkout system requires RTO at most 30 minutes, RPO at most 5 minutes, and a monthly budget at most $20,000. Compare the evidence and recommend one proposal.",
    "multi_agent": {
      "enabled": true,
      "max_concurrent_subagents": 3
    }
  }'
```

Reference: [Use the Azure OpenAI Responses API](responses.md)

`max_concurrent_subagents` limits how many subagents can be active at the same time across the entire agent tree. The limit includes children, grandchildren, and deeper descendants, but excludes the root agent. The default is `3`, which is recommended for most workloads.

## Control delegation

The model decides whether delegation is useful. Make the workstreams explicit in the input when the task requires parallel work.

Add developer instructions to control when the root model delegates. For example:

- `Do not create subagents unless the user explicitly asks for delegation or parallel work.`
- `Use subagents when parallel work would materially improve speed or quality.`

These instructions supplement the orchestration instructions that the service provides to the root agent and subagents.

## Understand agent coordination

The agent that receives the original request is the root agent and is named `/root`. Subagents use hierarchical names that show their position in the agent tree:

```text
/root
|-- /root/researcher
|-- /root/reviewer
|   `-- /root/reviewer/tester
`-- /root/writer
```

The root agent delegates work, waits for results, reconciles findings, and produces the final answer. Subagents use the same model and have access to the tools configured in the original request.

The service provides hosted collaboration actions. They appear in a response as `multi_agent_call` items. Your application must not execute these actions or submit outputs for them.

| Action | Purpose |
| --- | --- |
| `spawn_agent` | Create a subagent and assign its initial task. |
| `send_message` | Queue a message for an existing agent without starting a new turn. |
| `followup_task` | Assign more work to an existing non-root agent and start or resume its turn. |
| `wait_agent` | Wait for an update in the calling agent's mailbox. |
| `interrupt_agent` | Interrupt another agent's active turn without deleting its context. |
| `list_agents` | Return the agent tree, statuses, and each agent's latest task message. |

## Handle function calls

Any agent can call developer-defined functions included in the request. Execute every returned `function_call`, and submit a matching `function_call_output`. Don't handle hosted `multi_agent_call` items as developer-defined functions because the service manages them.

With HTTP, a response completes after every active agent finishes or pauses for a client-executed function call. Run all pending function calls, preserve the output items, and submit their outputs in the next request so the paused agents can continue. For the base tool execution pattern, see [Function calling](function-calling.md).

## Inspect multi-agent output

Multi-agent responses can include these additional output item types:

- `multi_agent_call`: A hosted collaboration action, such as `spawn_agent`.
- `multi_agent_call_output`: The result of a hosted collaboration action.
- `agent_message`: An encrypted message sent from one agent to another.

The `call_id` field links each `multi_agent_call` to its corresponding `multi_agent_call_output`. Each item also has an `agent` property. For an `agent_message`, use `author` and `recipient` to trace the message direction.

```json
[
  {
    "type": "multi_agent_call",
    "call_id": "call_spawn_a",
    "action": "spawn_agent",
    "agent": { "agent_name": "/root" }
  },
  {
    "type": "multi_agent_call_output",
    "call_id": "call_spawn_a",
    "action": "spawn_agent",
    "agent": { "agent_name": "/root" }
  },
  {
    "type": "agent_message",
    "author": "/root/researcher",
    "recipient": "/root",
    "content": [{ "type": "encrypted_content", "encrypted_content": "<encrypted-content>" }]
  }
]
```

Preserve these items when you manually replay conversation state or collect orchestration traces. Don't expose encrypted agent messages as user-visible content.

## Choose HTTP or WebSocket mode

HTTP and WebSocket transports support the same multi-agent orchestration capabilities, but their function-call behavior differs.

| Transport | Behavior | Recommended use |
| --- | --- | --- |
| HTTP | Waits until active agents finish or pause for function output. Your application submits pending outputs in a continuation request. | Hosted-tool workflows or requests with few developer-defined function calls. |
| WebSocket | Lets your application inject each function output into the active response as soon as it becomes available. | Tool-heavy or long-running workflows where lower coordination latency matters. |

In WebSocket mode, send a `response.inject` event for each function output:

```json
{
  "type": "response.inject",
  "response_id": "resp_123",
  "input": [
    {
      "type": "function_call_output",
      "call_id": "call_123",
      "output": "{\"temperature\":72}"
    }
  ]
}
```

Continue reading events until the response completes and each injection returns either `response.inject.created` or `response.inject.failed`. If an injection fails with `response_already_completed`, send the returned input in a new response that continues from the completed response. For connection and recovery guidance, see [Use the Responses API in WebSocket mode](websockets.md).

## Apply security controls

Every agent in the tree has access to the tools configured in the original request. Apply the same controls to calls from subagents that you apply to calls from the root agent.

- Grant tools and calling identities only the permissions required for the task.
- Validate function arguments and authorize each action in application code.
- Require user approval before write, destructive, financial, or other high-impact actions.
- Treat content returned by external tools as untrusted input, and protect against prompt injection.
- Log the agent name, tool name, arguments, approval decision, and result for auditing.
- Bound delegated work, and monitor token usage because subagents can increase consumption.

## Review limitations

- The `/responses/compact` endpoint isn't supported when multi-agent orchestration is enabled.
- Automatic server-side compaction is enabled when `multi_agent.enabled` is `true`, even if the request doesn't define `context_management`. Compaction runs independently for the root agent and each subagent.
- You can override the compaction threshold by setting `context_management.compact_threshold`.
- `reasoning.summary` isn't supported when multi-agent orchestration is enabled.
- `max_tool_calls` isn't supported when multi-agent orchestration is enabled.
- `max_concurrent_subagents` defaults to `3`, which is recommended for most workloads.
- Multi-agent orchestration has no fixed limit on tree depth or the total number of subagents created during a run. Control concurrency and bound delegated work to manage latency and token usage.

## Troubleshoot multi-agent requests

| Symptom | Resolution |
| --- | --- |
| HTTP 401 or 403 | For Microsoft Entra ID, verify that the token uses the `https://ai.azure.com/.default` scope and that the identity has the `Cognitive Services OpenAI User` role. For API key authentication, verify that the key belongs to the resource in the endpoint. |
| HTTP 404 | Verify that `model` is the Azure OpenAI deployment name and that the deployment is available on the resource in the endpoint. |
| Unknown request parameter | Upgrade the OpenAI SDK, use the beta Responses client, and confirm that the request targets the Azure OpenAI v1 endpoint with `api-version=preview`. |
| No subagents are created | Make the workstreams explicit in the prompt, and verify that `multi_agent.enabled` is `true`. The model decides whether delegation is useful unless the prompt requires it. |
| Unexpected function-call pauses | Execute every developer-defined `function_call`, including calls attributed to subagents, and submit a matching `function_call_output` for each call ID. |

## Related content

- [Use the Azure OpenAI Responses API](responses.md)
- [Use function calling](function-calling.md)
- [Use the Responses API in WebSocket mode](websockets.md)