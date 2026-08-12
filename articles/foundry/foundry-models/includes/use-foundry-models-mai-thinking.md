---
title: Include file
description: Include file
ms.author: mopeakande
author: msakande
ms.reviewer: rtalukder
reviewer: rashedtalukder
ms.service: microsoft-foundry
ms.subservice: foundry-model-inference
ms.topic: include
ms.date: 08/04/2026
ai-usage: ai-assisted
ms.custom: classic-and-new
---

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

MAI-Thinking-1 (preview) is a reasoning model from Microsoft for workloads that depend on multi-step reasoning, such as math, coding, and enterprise scenarios. The model uses a chat completions API that's compatible with OpenAI SDK-style chat completions patterns. To use MAI-Thinking-1, deploy it in Microsoft Foundry, set your Foundry endpoint, authenticate your request, and call the chat completions endpoint with your deployment name.

In this article, you learn how to:

- Deploy MAI-Thinking-1 in Microsoft Foundry
- Authenticate and call the chat completions API by using Microsoft Entra ID or an API key
- Call tools with function calling
- Preserve reasoning state across turns
- Stream responses
- Troubleshoot common errors

## Prerequisites

Before you begin, you need:

- An Azure subscription with a valid payment method. If you don't have an Azure subscription, create a [paid Azure account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- Access to Microsoft Foundry.
- A [Microsoft Foundry project](../../how-to/create-projects.md) in a [supported deployment region](../concepts/models-sold-directly-by-azure-region-availability.md). MAI-Thinking-1 is available for **global standard deployment**. 

    > [!NOTE]
    > PTU deployment is currently not supported for MAI-Thinking-1.

- Permission to create and manage model deployments. The **Cognitive Services Contributor** role lets you deploy models. For more information, see [Azure RBAC roles](/azure/role-based-access-control/built-in-roles).
- An authentication method: Microsoft Entra ID (recommended) or an API key.

- Install the required dependencies to run the examples with Microsoft Entra ID authentication.

    # [Python](#tab/python)
    
    ```bash
    pip install openai azure-identity
    ```
    
    # [JavaScript](#tab/javascript)
    
    ```bash
    npm install openai @azure/identity
    ```
    
    # [REST](#tab/rest)
    
    REST examples require `curl` to be installed and available on `PATH`.
    
    ---

## MAI-Thinking-1 at a glance

| Model name | Model version | Deployment type | API type |
| --- | --- | --- | --- |
| `MAI-Thinking-1` (preview) | 2026-06-01 | GlobalStandard | Chat completions |

## Deploy MAI-Thinking-1

To deploy MAI-Thinking-1 (preview), follow the instructions in [Deploy Microsoft Foundry Models in the Foundry portal](../how-to/deploy-foundry-models.md), and select the `MAI-Thinking-1` model to deploy.

Alternatively, you can deploy the model by using the Azure CLI as shown in the following code:

Replace `<ACCOUNT_NAME>`, `<RESOURCE_GROUP>`, and `<DEPLOYMENT_NAME>` with your values.

```bash
az cognitiveservices account deployment create \
  --name <ACCOUNT_NAME> \
  --resource-group <RESOURCE_GROUP> \
  --deployment-name <DEPLOYMENT_NAME> \
  --model-name "mai-thinking-1" \
  --model-format Microsoft \
  --model-version 2026-06-01 \
  --sku-name GlobalStandard \
  --sku-capacity 1
```

**Reference:** [az cognitiveservices account deployment create](/cli/azure/cognitiveservices/account/deployment#az-cognitiveservices-account-deployment-create)

To list all available deployments on your resource:

```bash
az cognitiveservices account deployment list \
  --resource-group <RESOURCE_GROUP> \
  --name <ACCOUNT_NAME> \
  -o table
```

**Reference:** [az cognitiveservices account deployment list](/cli/azure/cognitiveservices/account/deployment#az-cognitiveservices-account-deployment-list)

### Retrieve your deployment details and credentials

After deployment, gather the endpoint, deployment name, and API key that you use to authenticate and route your API requests. If you use Microsoft Entra ID for REST requests, also retrieve an access token. 

1. Find the endpoint, deployment name, and key on the **Details** tab of your deployment in the [Foundry portal](https://ai.azure.com) or in the **Keys and Endpoint** section of your resource in the Azure portal.
    
    - **Endpoint**: Foundry resource endpoint of the form `https://<resource-name>.services.ai.azure.com`
    - **Name**: Deployment name - use this as the `model` value in chat completions requests
    - **Key**: API key for use with API key authentication. Alternatively, you can use a Microsoft Entra ID token for authentication.

1. For REST requests that use Microsoft Entra ID, sign in with the Azure CLI, and then retrieve an access token and set it as an environment variable:
    
    ```bash
    export AZURE_ENTRA_TOKEN=$(az account get-access-token \
      --resource https://cognitiveservices.azure.com \
      --query accessToken \
      --output tsv)
    ```

    **Reference:** [az account get-access-token](/cli/azure/account#az-account-get-access-token)

## Run a chat completion

Use the [chat completions API](#api-endpoints) to send messages to MAI-Thinking-1 (preview). The `model` value is your deployment name, not the underlying model name.

Set these environment variables:

```bash
export AZURE_ENDPOINT="<your-foundry-resource-endpoint>"
export AZURE_API_KEY="<your-api-key>"
export DEPLOYMENT_NAME="<your-deployment-name>"
```

An example endpoint value is `https://<resource-name>.services.ai.azure.com`.

# [Python](#tab/python)

```python
import os
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import OpenAI

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(),
    "https://cognitiveservices.azure.com/.default"
)

client = OpenAI(
    base_url=f"{os.environ['AZURE_ENDPOINT']}/mai/v1",
    api_key=token_provider,
)

response = client.chat.completions.create(
    model=os.environ["DEPLOYMENT_NAME"],
    messages=[
        {"role": "user", "content": "Who were the founders of Microsoft?"}
    ],
    max_completion_tokens=32768,
)

print(response.choices[0].message.content)
```

To use an API key instead, pass it through default headers:

```python
import os
from openai import OpenAI

client = OpenAI(
    base_url=f"{os.environ['AZURE_ENDPOINT']}/mai/v1",
    api_key="unused",
    default_headers={"api-key": os.environ["AZURE_API_KEY"]},
)
```

# [JavaScript](#tab/javascript)

```javascript
import { OpenAI } from "openai";
import { DefaultAzureCredential } from "@azure/identity";

const credential = new DefaultAzureCredential();
const { token } = await credential.getToken("https://cognitiveservices.azure.com/.default");

const client = new OpenAI({
  baseURL: `${process.env.AZURE_ENDPOINT}/mai/v1`,
  apiKey: token,
});

const response = await client.chat.completions.create({
  model: process.env.DEPLOYMENT_NAME,
  messages: [
    { role: "user", content: "Who were the founders of Microsoft?" },
  ],
  max_completion_tokens: 32768,
});

console.log(response.choices[0].message.content);
```

To use an API key instead, pass it through default headers:

```javascript
const client = new OpenAI({
  baseURL: `${process.env.AZURE_ENDPOINT}/mai/v1`,
  apiKey: "unused",
  defaultHeaders: { "api-key": process.env.AZURE_API_KEY },
});
```

# [REST](#tab/rest)

```bash
curl "$AZURE_ENDPOINT/mai/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AZURE_ENTRA_TOKEN" \
  -d '{
    "model": "'"$DEPLOYMENT_NAME"'",
    "messages": [
      { "role": "user", "content": "Who were the founders of Microsoft?" }
    ],
    "max_completion_tokens": 32768
  }'
```

To use an API key instead, replace the `Authorization` header with `-H "api-key: $AZURE_API_KEY"`.

---

### Use function calling and tools

Use MAI-Thinking-1 in agentic workflows that call tools or functions. Only function tools are supported. Use function calling when your application needs the model to select a tool, provide structured arguments, or coordinate multiple steps.

```json
{
  "model": "<deployment-name>",
  "messages": [
    { "role": "user", "content": "What's the weather in San Francisco today?" }
  ],
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "get_weather",
        "description": "Get the current weather for a city.",
        "parameters": {
          "type": "object",
          "properties": {
            "city": { "type": "string" }
          },
          "required": ["city"]
        }
      }
    }
  ]
}
```

### Preserve reasoning state across turns

To receive the encrypted reasoning state, set `reasoning_display` to `encrypted` on each request. When set, the response includes `reasoning.encrypted_content` on the assistant message (non-streaming) or on the final stream chunk (`delta.reasoning.encrypted_content`). When you don't set it, `reasoning` is null and there's nothing to carry across turns.

MAI-Thinking-1 returns encrypted chain-of-thought content with a response. The encrypted value is opaque to your application and doesn't expose the model's raw reasoning. Pass it back to the model when a later turn in the same conversation benefits from the reasoning the model already did, such as multi-turn agent loops and tool-calling workflows. To pass back the encrypted reasoning state:

- Return the value exactly as you received it. Any change invalidates it.
- Send back the complete assistant message rather than rebuilding it field by field.
- Don't inspect, decode, transform, log, or display the value.
- The value counts toward the context window when you send it back.

> [!NOTE]
> Serializing the complete assistant message preserves the encrypted chain-of-thought field exactly as returned. If your SDK version doesn't expose the field, preserve the equivalent assistant-message object from the raw API response.

# [Python](#tab/python)

```python
first_response = client.chat.completions.create(
    model=os.environ["DEPLOYMENT_NAME"],
    messages=[{"role": "user", "content": "Plan a migration in three phases."}],
    max_completion_tokens=32768,
    extra_body={"reasoning_display": "encrypted"},
)

assistant_message = first_response.choices[0].message

follow_up_messages = [
    {"role": "user", "content": "Plan a migration in three phases."},
    assistant_message.model_dump(exclude_none=True),
    {"role": "user", "content": "Expand phase two with risks and mitigations."},
]

follow_up_response = client.chat.completions.create(
    model=os.environ["DEPLOYMENT_NAME"],
    messages=follow_up_messages,
    max_completion_tokens=32768,
)

print(follow_up_response.choices[0].message.content)
```

# [JavaScript](#tab/javascript)

```javascript
const firstResponse = await client.chat.completions.create({
  model: process.env.DEPLOYMENT_NAME,
  messages: [
    { role: "user", content: "Plan a migration in three phases." },
  ],
  max_completion_tokens: 32768,
  reasoning_display: "encrypted",
});

const assistantMessage = firstResponse.choices[0].message;

const followUpResponse = await client.chat.completions.create({
  model: process.env.DEPLOYMENT_NAME,
  messages: [
    { role: "user", content: "Plan a migration in three phases." },
    assistantMessage,
    { role: "user", content: "Expand phase two with risks and mitigations." },
  ],
  max_completion_tokens: 32768,
});

console.log(followUpResponse.choices[0].message.content);
```

# [REST](#tab/rest)

```bash
curl "$AZURE_ENDPOINT/mai/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AZURE_ENTRA_TOKEN" \
  -d '{
    "model": "'"$DEPLOYMENT_NAME"'",
    "messages": [
      { "role": "user", "content": "Plan a migration in three phases." },
      <assistant message from the previous response, returned unchanged>,
      { "role": "user", "content": "Expand phase two with risks and mitigations." }
    ],
    "max_completion_tokens": 32768,
    "reasoning_display": "encrypted"
  }'
```

---

## Stream responses

Set `stream` to `true` to receive the response incrementally instead of waiting for the full completion. Streaming is useful for chat interfaces and long reasoning tasks, where time-to-first-token matters more than total latency.

When streaming is enabled, the response is delivered as a series of server-sent events. Each event is a `chat.completion.chunk` object rather than the single `chat.completion` object returned by a non-streamed request. The streamed response has the following characteristics:

- Each chunk carries a `delta` with the incremental fields for that step. Text arrives in the `delta.content` field across successive chunks.
- Intermediate chunks set `usage` to null and `finish_reason` to null.
- The final chunk sets `finish_reason` and includes the populated `usage` object, including `usage.prompt_tokens_details.cached_tokens`.
- When you set `reasoning_display` to `encrypted`, the encrypted reasoning state is delivered on the final chunk as `delta.reasoning.encrypted_content`. Otherwise, `reasoning` is null on every chunk.
- The stream terminates with a `data: [DONE]` sentinel.

# [Python](#tab/python)

```python
stream = client.chat.completions.create(
    model=os.environ["DEPLOYMENT_NAME"],
    messages=[
        {"role": "user", "content": "Count from 1 to 5, one per line."}
    ],
    max_completion_tokens=32768,
    stream=True,
)

for chunk in stream:
    if not chunk.choices:
        continue
    delta = chunk.choices[0].delta
    if delta.content:
        print(delta.content, end="", flush=True)
```

# [JavaScript](#tab/javascript)

```javascript
const stream = await client.chat.completions.create({
  model: process.env.DEPLOYMENT_NAME,
  messages: [
    { role: "user", content: "Count from 1 to 5, one per line." },
  ],
  max_completion_tokens: 32768,
  stream: true,
});

for await (const chunk of stream) {
  const delta = chunk.choices?.[0]?.delta;
  if (delta?.content) {
    process.stdout.write(delta.content);
  }
}
```

# [REST](#tab/rest)

```bash
curl "$AZURE_ENDPOINT/mai/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AZURE_ENTRA_TOKEN" \
  -N \
  -d '{
    "model": "'"$DEPLOYMENT_NAME"'",
    "messages": [
      { "role": "user", "content": "Count from 1 to 5, one per line." }
    ],
    "max_completion_tokens": 32768,
    "stream": true
  }'
```

---

An intermediate chunk has the following shape:

```text
data: {
  "id": "mai-api-<uuid>",
  "object": "chat.completion.chunk",
  "created": 1785277080,
  "model": "MAI-Thinking-1",
  "choices": [
    {
      "delta": {
        "content": "1\n",
        "role": "assistant",
        "tool_calls": null,
        "reasoning": null,
        "annotations": null
      },
      "index": 0,
      "finish_reason": null
    }
  ],
  "system_fingerprint": "",
  "usage": null
}
```

The final chunk carries the reasoning state, finish reason, and token usage. This example shows the response to a request that sets `reasoning_display` to `encrypted`. Otherwise, `reasoning` is null.

```text
data: {
  "id": "mai-api-<uuid>",
  "object": "chat.completion.chunk",
  "created": 1785277080,
  "model": "MAI-Thinking-1",
  "choices": [
    {
      "delta": {
        "content": null,
        "role": "assistant",
        "tool_calls": null,
        "reasoning": {
          "encrypted_content": "<encrypted-reasoning-blob>",
          "content": null,
          "summary": null
        },
        "annotations": null
      },
      "index": 0,
      "finish_reason": "stop"
    }
  ],
  "system_fingerprint": "",
  "usage": {
    "prompt_tokens": 19,
    "completion_tokens": 76,
    "total_tokens": 95,
    "prompt_tokens_details": { "cached_tokens": 2 }
  }
}

data: [DONE]
```

### Content safety in streamed responses

Content safety applies to streamed responses. A prompt blocked by input safety fails before generation starts and returns HTTP 400. Output safety is evaluated as the response streams, so generation can stop mid-response. With `stream: true`, the client receives the chunks produced so far, followed by a terminal SSE error event where `error.type = SafetyBlockedError`, and then `data: [DONE]`. Handle a truncated response that ends in an error event as an expected case. For non-streaming requests, an output safety block returns HTTP 400.

## When to use MAI-Thinking-1

Use MAI-Thinking-1 (preview) for workloads that benefit from deeper reasoning, longer context, or more deliberate planning. It's best suited for tasks where answer quality depends on multi-step reasoning. Common use cases include:

- **Enterprise deployments**: A 256K context window, clean data provenance, function calling, and the ability to follow complex instructions.
- **Coding workflows**: Reading code, editing files, running tests, fixing bugs, observing failures, and recovering from intermediate mistakes.
- **Complex reasoning tasks**: Quantitative reasoning such as financial modeling, statistical analysis, market sizing, and forecasting.

## API endpoints

After you deploy MAI-Thinking-1 (preview), call the **chat completions endpoint** on your Foundry resource:

```
https://<resource-name>.services.ai.azure.com/mai/v1/chat/completions
```

To authenticate, you need your resource endpoint and either a Microsoft Entra ID token or an API key. You can find these values in the **Keys and Endpoint** section of your resource in the Azure portal, or on the deployment details page in the [Foundry portal](https://ai.azure.com).

### Request parameters

The chat completions API accepts the following parameters.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `model` | string | Required | Your Microsoft Foundry deployment name. |
| `messages` | array | Required | The conversation messages to send to the model. |
| `max_completion_tokens` | integer | Optional | The maximum number of generated tokens, including reasoning tokens. Output is capped at 64K tokens and must fit within the remaining context budget. |
| `tools` | array | Optional | Function definitions the model can call. Only function tools are supported. |
| `stream` | boolean | Optional | When `true`, delivers the response as a server-sent events stream of `chat.completion.chunk` objects. Defaults to `false`. |
| `reasoning_display` | string | Optional | Request the encrypted reasoning envelope in the response. Set to `encrypted` to return `reasoning.encrypted_content` on the assistant message. This parameter is a MAI extension: send it with `extra_body` (Python) or as an additional field (JavaScript and REST). When omitted, no reasoning envelope is returned. |

### Response format

A successful chat completions response includes the assistant message in the response choices.

| Field | Type | Description |
| --- | --- | --- |
| `choices[].message.content` | string | The assistant response. Null when the model returns tool calls. |
| `choices[].message.tool_calls` | array | Function tool calls requested by the model. |
| `choices[].message.reasoning.encrypted_content` | string | Opaque reasoning state returned with the assistant message when `reasoning_display` is set to `encrypted`. Preserve it unchanged across turns. |
| `choices[].finish_reason` | string | Why generation stopped. Typically `stop` (normal completion, including when the message contains tool calls), `length` (hit the token limit), or content filter. Inspect `choices[].message.tool_calls` to detect tool calls rather than relying on `finish_reason`. |
| `usage.prompt_tokens_details.cached_tokens` | integer | The number of prompt tokens served from the prefix cache. |

The following example shows a response that contains a tool call.

```json
{
  "id": "<completion-id>",
  "object": "chat.completion",
  "created": 1785277080,
  "model": "<deployment-name>",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": null,
        "refusal": null,
        "tool_calls": [
          {
            "id": "call_abc123",
            "type": "function",
            "function": {
              "name": "get_weather",
              "arguments": "{\"city\":\"San Francisco\"}"
            }
          }
        ]
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 87,
    "completion_tokens": 41,
    "total_tokens": 128,
    "prompt_tokens_details": { "cached_tokens": 0 }
  }
}
```

### Token limits and context window

MAI-Thinking-1 (preview) has a total token budget of 256K per request, which supports long-context prompts and extended conversation history. Output is capped at 64K tokens, or the remaining context budget after input, whichever is smaller.

Messages and generated output count against this token budget:

- **Input tokens**: The messages in your request count toward the input token budget.
- **Output tokens**: `max_completion_tokens` bounds the generated response, up to the 64K output cap, and includes reasoning tokens.
- **Total**: Input and output tokens must fit within the 256K-token context window. If a request exceeds the context window, it fails.

## API quotas and limits

MAI-Thinking-1 (preview) has the following rate limits measured in requests per minute (RPM) and tokens per minute (TPM). The tier available to you depends on your subscription and deployment configuration.

| Deployment Type | Tier          | TPM     | RPM |
|-----------------|---------------|:-------:|:---:|
| Global Standard | Low (Default) | 0       | 0   |
| Global Standard | Medium        | 100,000 | 100 |
| Global Standard | High          | 250,000 | 250 |

MAI-Thinking-1 **supports global standard deployment**. For supported deployment regions, see [Region availability for Foundry Models sold by Azure](../concepts/models-sold-directly-by-azure-region-availability.md). **PTU deployment isn't currently supported**.

## Troubleshoot

Use the following table to identify common errors and resolutions.

| Error | Possible cause | Resolution |
| --- | --- | --- |
| 400 Bad Request | Invalid request shape or unsupported parameter, such as `max_tokens` instead of `max_completion_tokens`. Also returned when input safety blocks the prompt. | Validate the request body against the API contract and check the supported parameters. |
| 401 Unauthorized | Invalid API key, expired token, or missing or incorrect authentication header. | Check your credential, token scope, and header (`api-key` for API keys, `Authorization: Bearer` for Microsoft Entra ID). |
| 403 Forbidden | Authenticated, but not permitted to access the requested model. | Verify role assignment and model access. |
| 404 Not Found | Incorrect endpoint or deployment name, or a referenced resource wasn't found. | Verify the endpoint and deployment name in Microsoft Foundry. |
| 422 Unprocessable Entity | The request failed API schema validation. | Correct the request body to match the API schema. |
| 429 Too Many Requests | Rate limit exceeded. | Retry with backoff, or request a quota increase if available. |
| 500 Internal Server Error | Server-side error or misconfiguration. | Retry with backoff. If the issue persists, check service health and support guidance. |
| 502 Bad Gateway | Upstream error from the agent orchestrator or inference backend. | Retry with backoff. |
| 503 Service Unavailable | A dependency, such as the safety service, is temporarily unavailable. | Retry with backoff. |

## Write effective prompts for reasoning tasks

For reasoning-heavy tasks, provide the model with the goal, context, constraints, and expected output format. Recommended patterns:

- State the goal clearly.
- Include relevant context.
- Provide constraints, such as audience, format, length, or business rules.
- Ask for concise final answers when you don't need a detailed explanation.

The following example shows a well-structured prompt.

```text
You are helping someone plan a weekend trip.

Goal: Suggest a simple two-day itinerary for a first-time visitor to Seattle.

Context: The visitor enjoys food, walking, and being outdoors, and is traveling on a modest budget.

Output: Return a prioritized list with:
- Activity
- Why it's worth doing
- Rough time of day
- Approximate cost
- One tip
```

## Responsible AI considerations

Before you use MAI-Thinking-1 (preview) in an application, evaluate the model for your intended scenario. Follow these recommended practices:

- Validate model behavior on realistic prompts.
- Test for task-specific quality, safety, and reliability.
- Use human review for high-impact workflows.
- Log and monitor failures according to your application requirements.
- Apply appropriate content safety and abuse monitoring.

Microsoft Foundry screens requests with input safety and screens responses with output safety. For details about how blocked prompts and responses behave, including streaming requests, see [Content safety in streamed responses](#content-safety-in-streamed-responses).

## Related content

- [Explore available models in Foundry](../concepts/models-sold-directly-by-azure.md)
- [Deploy Microsoft Foundry Models in the Foundry portal](../how-to/deploy-foundry-models.md)
- [Configure Microsoft Entra ID authentication](../how-to/configure-entra-id.md)
