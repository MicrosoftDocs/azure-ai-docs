---
title: Include file
description: Include file
ms.author: mopeakande
ms.service: microsoft-foundry
ms.subservice: foundry-model-inference
ms.topic: include
ms.date: 08/26/2026
ai-usage: ai-assisted
ms.custom: classic-and-new
---

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

SpaceXAI's Grok models are available as Foundry Models sold by Azure and support coding, data extraction, summarization, and agentic applications. This article focuses on `grok-4.6` (preview), which provides a 200,000 token context window, multimodal input (text and image), tool calling, and advanced reasoning for coding, agentic workflows, and knowledge-work scenarios.

In this article, you learn how to:

- Deploy Grok 4.6 (preview) in Microsoft Foundry.
- Authenticate by using Microsoft Entra ID or an API key.
- Generate output with the Chat Completions and Responses APIs.
- Use configurable reasoning efforts (`low`, `medium`, `high`, or `xhigh`; default `high`).
- Call tools with function calling.
- Stream responses.
- Troubleshoot common errors.

## Prerequisites

Before you begin, you need:

- An Azure subscription with a valid payment method. If you don't have an Azure subscription, create a [paid Azure account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- Access to Microsoft Foundry with appropriate permissions to create and manage resources.
- A [Microsoft Foundry project](../../how-to/create-projects.md) in a region supported for Grok 4.6 (preview) deployment. For more information, see [Supported deployment types and regions](#supported-deployment-types-and-regions).
- The **Cognitive Services Contributor** role on the Foundry resource, to deploy models. For more information, see [Azure RBAC roles](/azure/role-based-access-control/built-in-roles).
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

## Grok models available in Foundry

Foundry Models sold by Azure include the following SpaceXAI Grok models.

| Model | Model Version | Deployment Type | API Type |
| --- | --- | --- | --- |
| `grok-4.6` (preview) | 1 | Global Standard | Chat Completions, Responses |
| `grok-4.3` (preview) | 1 | Global Standard, Data Zone Standard (US) | Chat Completions, Responses |
| `grok-4-20-reasoning` (preview) | 1 | Global Standard, Data Zone Standard (US) | Chat Completions, Responses |
| `grok-4-20-non-reasoning` (preview) | 1 | Global Standard, Data Zone Standard (US) | Chat Completions, Responses |
| `grok-4.1-fast-reasoning` | 1 | Global Standard, Data Zone Standard (US) | Chat Completions, Responses |
| `grok-4.1-fast-non-reasoning` | 1 | Global Standard, Data Zone Standard (US) | Chat Completions, Responses |
| `grok-4`<sup>1</sup> | 1 | Global Standard, Data Zone Standard (US) | Chat Completions, Responses |
| `grok-code-fast-1`<sup>1</sup> | 1 | Global Standard, Data Zone Standard (US) | Chat Completions, Responses |

<sup>1</sup> [Registration is required for access to](https://aka.ms/xai/grok-4) `grok-code-fast-1` and `grok-4`.

This article focuses on `grok-4.6`. For full capability details on all Grok models, see [SpaceXAI models sold by Azure](../concepts/models-sold-directly-by-azure.md#spacexai-models-sold-by-azure).

## Deploy Grok 4.6

To deploy Grok 4.6 (preview), follow the instructions in [Deploy Microsoft Foundry Models in the Foundry portal](../how-to/deploy-foundry-models.md), and select the `grok-4.6` model to deploy.

Alternatively, deploy the model by using the Azure CLI as shown in the following code.

Replace `<ACCOUNT_NAME>`, `<RESOURCE_GROUP>`, and `<DEPLOYMENT_NAME>` with your values.

```azurecli
az cognitiveservices account deployment create \
  --name <ACCOUNT_NAME> \
  --resource-group <RESOURCE_GROUP> \
  --deployment-name <DEPLOYMENT_NAME> \
  --model-name "grok-4.6" \
  --model-format "xAI" \
  --model-version "1" \
  --sku-name GlobalStandard \
  --sku-capacity 1
```

Use `--sku-name GlobalStandard` to deploy in any supported region. Grok 4.6 (preview) currently supports only Global Standard deployment. 

To deploy a Grok model that is [available for Data Zone Standard (US) deployment](#grok-models-available-in-foundry), use `--sku-name DataZoneStandard` to keep processing within the United States data zone.

**Reference:** [az cognitiveservices account deployment create](/cli/azure/cognitiveservices/account/deployment#az-cognitiveservices-account-deployment-create)

For more on the CLI deployment workflow, see [Add and configure models to Foundry Models](../how-to/create-model-deployments.md).

## Generate output with the Chat Completions API

Use the Chat Completions API to send messages to Grok 4.6 (preview). The `model` value is your deployment name, not the underlying model name.

Set the following environment variables. The endpoint takes the form `https://<resource-name>.services.ai.azure.com`.

```bash
export AZURE_ENDPOINT="<your-foundry-resource-endpoint>"
export AZURE_ENTRA_TOKEN=$(az account get-access-token --resource https://ai.azure.com --query accessToken --output tsv)
export DEPLOYMENT_NAME="<your-deployment-name>"
```

# [Python](#tab/python)

If you didn't install the `openai` and `azure-identity` packages in the [Prerequisites](#prerequisites) section, install them now by using your package manager, like pip:

```bash
pip install --upgrade openai azure-identity
```

Use Microsoft Entra ID to authenticate and generate a chat completion:

```python
import os
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import OpenAI

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(),
    "https://ai.azure.com/.default"
)

client = OpenAI(
    base_url=f"{os.environ['AZURE_ENDPOINT']}/openai/v1",
    api_key=token_provider,
)

response = client.chat.completions.create(
    model=os.environ["DEPLOYMENT_NAME"],
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Summarize the key benefits of an agentic coding workflow."},
    ],
    reasoning_effort="high",  # Options: "low", "medium", "high", "xhigh" (default "high").
)

print(response.choices[0].message.content)
```

To use an API key instead, pass it directly as `api_key`:

```python
client = OpenAI(
    base_url=f"{os.environ['AZURE_ENDPOINT']}/openai/v1",
    api_key=os.environ["AZURE_API_KEY"],
)
```

# [JavaScript](#tab/javascript)

If you didn't install the `openai` and `@azure/identity` packages in the [Prerequisites](#prerequisites) section, install them now by using npm:

```bash
npm install openai @azure/identity
```

Use Microsoft Entra ID to authenticate and generate a chat completion:

```javascript
import { OpenAI } from "openai";
import { DefaultAzureCredential, getBearerTokenProvider } from "@azure/identity";

const tokenProvider = getBearerTokenProvider(
  new DefaultAzureCredential(),
  "https://ai.azure.com/.default"
);

const client = new OpenAI({
  baseURL: `${process.env.AZURE_ENDPOINT}/openai/v1`,
  apiKey: tokenProvider,
});

const response = await client.chat.completions.create({
  model: process.env.DEPLOYMENT_NAME,
  messages: [
    { role: "system", content: "You are a helpful assistant." },
    { role: "user", content: "Summarize the key benefits of an agentic coding workflow." },
  ],
  reasoning_effort: "high", // Options: "low", "medium", "high", "xhigh" (default "high").
});

console.log(response.choices[0].message.content);
```

To use an API key instead, pass it directly as `apiKey`:

```javascript
const client = new OpenAI({
  baseURL: `${process.env.AZURE_ENDPOINT}/openai/v1`,
  apiKey: process.env.AZURE_API_KEY,
});
```

# [REST](#tab/rest)

```bash
curl "$AZURE_ENDPOINT/openai/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AZURE_ENTRA_TOKEN" \
  -d '{
    "model": "'"$DEPLOYMENT_NAME"'",
    "messages": [
      { "role": "system", "content": "You are a helpful assistant." },
      { "role": "user", "content": "Summarize the key benefits of an agentic coding workflow." }
    ],
    "reasoning_effort": "high"
  }'
```

To use an API key instead of Microsoft Entra ID, replace the `Authorization: Bearer $AZURE_ENTRA_TOKEN` header with `api-key: $AZURE_API_KEY`, where `AZURE_API_KEY` is a key for your Foundry resource.

---

## Generate a response with the Responses API

Grok 4.6 (preview) also supports the [Responses API](../how-to/generate-responses.md), which offers a simplified interface for stateful, multi-turn interactions and built-in tool orchestration.

# [Python](#tab/python)

```python
import os
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import OpenAI

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(),
    "https://ai.azure.com/.default"
)

client = OpenAI(
    base_url=f"{os.environ['AZURE_ENDPOINT']}/openai/v1",
    api_key=token_provider,
)

response = client.responses.create(
    model=os.environ["DEPLOYMENT_NAME"],
    instructions="You are a helpful assistant.",
    input="What are the top 3 benefits of an agentic coding workflow? Be concise.",
    reasoning={
        "effort": "high"  # Options: "low", "medium", "high", "xhigh" (default "high").
    },
)

print(response.output_text)
```

# [JavaScript](#tab/javascript)

```javascript
import { OpenAI } from "openai";
import { DefaultAzureCredential, getBearerTokenProvider } from "@azure/identity";

const tokenProvider = getBearerTokenProvider(
  new DefaultAzureCredential(),
  "https://ai.azure.com/.default"
);

const client = new OpenAI({
  baseURL: `${process.env.AZURE_ENDPOINT}/openai/v1`,
  apiKey: tokenProvider,
});

const response = await client.responses.create({
  model: process.env.DEPLOYMENT_NAME,
  instructions: "You are a helpful assistant.",
  input: "What are the top 3 benefits of an agentic coding workflow? Be concise.",
  reasoning: {
    effort: "high", // Default is "high", but you can set it to "low", "medium", "high", or "xhigh" depending on the complexity of the reasoning required.
  },
});

console.log(response.output_text);
```

# [REST](#tab/rest)

```bash
curl "$AZURE_ENDPOINT/openai/v1/responses" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AZURE_ENTRA_TOKEN" \
  -d '{
    "model": "'"$DEPLOYMENT_NAME"'",
    "instructions": "You are a helpful assistant.",
    "input": "What are the top 3 benefits of an agentic coding workflow? Be concise.",
    "reasoning": { "effort": "high" }
  }'
```

To use an API key instead of Microsoft Entra ID, replace the `Authorization: Bearer $AZURE_ENTRA_TOKEN` header with `api-key: $AZURE_API_KEY`, where `AZURE_API_KEY` is a key for your Foundry resource.

---

## Use function calling and tools

Grok 4.6 (preview) supports function calling, using both the Chat completions API and the Responses API. Use function calling when your application needs the model to select a tool, provide structured arguments, or coordinate multiple steps.

### Chat Completions API

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

### Responses API

For the Responses API, the payload differs from the Chat Completions API: pass the conversation in the `input` array by using typed content parts, and define each tool with the function fields at the top level of the tool object.

```json
{
  "model": "<deployment-name>",
  "input": [
    {
      "role": "user",
      "content": [
        {
          "type": "input_text",
          "text": "What's the weather in San Francisco today?"
        }
      ]
    }
  ],
  "tools": [
    {
      "type": "function",
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
  ]
}
```

## Stream responses

Set `stream` to `true` to receive the response incrementally instead of waiting for the full completion. Streaming is useful for chat interfaces and long-running tasks, where time-to-first-token matters more than total latency.

### Chat Completions API

# [Python](#tab/python)

```python
stream = client.chat.completions.create(
    model=os.environ["DEPLOYMENT_NAME"],
    messages=[
        {"role": "user", "content": "Count from 1 to 5, one per line."}
    ],
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
curl "$AZURE_ENDPOINT/openai/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AZURE_ENTRA_TOKEN" \
  -N \
  -d '{
    "model": "'"$DEPLOYMENT_NAME"'",
    "messages": [
      { "role": "user", "content": "Count from 1 to 5, one per line." }
    ],
    "stream": true
  }'
```

To use an API key instead of Microsoft Entra ID, replace the `Authorization: Bearer $AZURE_ENTRA_TOKEN` header with `api-key: $AZURE_API_KEY`, where `AZURE_API_KEY` is a key for your Foundry resource.

---

### Responses API

# [Python](#tab/python)

```python
stream = client.responses.create(
    model=os.environ["DEPLOYMENT_NAME"],
    input="Count from 1 to 5, one per line.",
    stream=True,
)

for event in stream:
    if event.type == "response.output_text.delta":
        print(event.delta, end="", flush=True)
```

# [JavaScript](#tab/javascript)

```javascript
const stream = await client.responses.create({
  model: process.env.DEPLOYMENT_NAME,
  input: "Count from 1 to 5, one per line.",
  stream: true,
});

for await (const event of stream) {
  if (event.type === "response.output_text.delta") {
    process.stdout.write(event.delta);
  }
}
```

# [REST](#tab/rest)

```bash
curl "$AZURE_ENDPOINT/openai/v1/responses" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AZURE_ENTRA_TOKEN" \
  -N \
  -d '{
    "model": "'"$DEPLOYMENT_NAME"'",
    "input": "Count from 1 to 5, one per line.",
    "stream": true
  }'
```

To use an API key instead of Microsoft Entra ID, replace the `Authorization: Bearer $AZURE_ENTRA_TOKEN` header with `api-key: $AZURE_API_KEY`, where `AZURE_API_KEY` is a key for your Foundry resource.

---

## When to use Grok 4.6

Use Grok 4.6 (Preview) for complex enterprise workloads that require reasoning, tool use, and multi-step execution. Grok 4.6 is optimized for coding, agentic workflows, technical problem solving, and knowledge-work applications that benefit from sustained reasoning across extended tasks.

Common use cases include:

- **Agentic applications**: Use tool calling and reasoning to plan tasks, select tools, coordinate multi-step workflows, and generate structured outputs.
- **Software engineering**: Support code generation, code understanding, debugging, repository-level analysis, test generation, and complex software engineering workflows.
- **Knowledge work and research**: Analyze information, synthesize findings, generate reports, summarize large volumes of content, and support research-intensive tasks.
- **Engineering and technical workflows**: Assist with technical problem solving, engineering analysis, procedural design, and other structured reasoning tasks.
- **Enterprise automation**: Power enterprise assistants and workflow automation that transform information into actionable business deliverables, such as reports, presentations, spreadsheets, and recommendations.

## API endpoints

After you deploy Grok 4.6 (preview), call one of the following endpoints on your Foundry resource:

- **Chat Completions**: `https://<resource-name>.services.ai.azure.com/openai/v1/chat/completions`
- **Responses**: `https://<resource-name>.services.ai.azure.com/openai/v1/responses`

To authenticate, you need your resource endpoint and either a Microsoft Entra ID token or an API key. Find these values in the **Keys and Endpoint** section of your resource in the Azure portal, or on the deployment details page in the [Foundry portal](https://ai.azure.com).

### Request parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `model` | string | Yes | Your Microsoft Foundry deployment name. |
| `messages` | array | Yes, for Chat Completions | The conversation messages to send to the model. |
| `input` | string or array | Yes, for Responses | The input to the model. |
| `instructions` | string | No | Responses only. System prompt for the Responses API. |
| `tools` | array | No | Function definitions the model can call. |
| `stream` | boolean | No | When `true`, delivers the response as a server-sent events stream. Defaults to `false`. |
| `reasoning_effort` | string | No | Chat Completions only. Controls how much reasoning the model performs. One of `low`, `medium`, `high`, or `xhigh`. Defaults to `high`. |
| `reasoning` | object | No | Responses only. Reasoning configuration. Set `effort` to `low`, `medium`, `high`, or `xhigh`. Defaults to `high`. |
| `max_completion_tokens` | integer | No | Chat Completions only. An upper bound on generated tokens, including reasoning tokens. |
| `max_output_tokens` | integer | No | Responses only. An upper bound on generated tokens, including reasoning tokens. |

For more information about the Responses API, see [Use the Azure OpenAI Responses API](../../openai/how-to/responses.md). For more information about Chat Completions API, see [Work with chat completion models](../../openai/how-to/chatgpt.md).

### Response format

The response format depends on which API you call. Grok 4.6 (preview) returns an OpenAI-compatible object for both the Chat Completions API and the Responses API.

#### Chat Completions API

A successful Chat Completions response includes the assistant message in the response choices.

| Field | Type | Description |
| --- | --- | --- |
| `choices[].message.content` | string | The assistant response. Null when the model returns tool calls. |
| `choices[].message.tool_calls` | array | Function tool calls requested by the model. |
| `choices[].finish_reason` | string | Why generation stopped. Typically `stop` (normal completion), `tool_calls` (the model requested a tool), or `length` (hit the token limit). |
| `usage.prompt_tokens` | integer | The number of tokens in the input prompt. |
| `usage.completion_tokens` | integer | The number of generated tokens, including reasoning tokens. |
| `usage.total_tokens` | integer | The total number of tokens used. |

The following example shows a Chat Completions response that contains a tool call.

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
      "finish_reason": "tool_calls"
    }
  ],
  "usage": {
    "prompt_tokens": 87,
    "completion_tokens": 41,
    "total_tokens": 128
  }
}
```

#### Responses API

A successful Responses API call returns a `response` object. Instead of a `choices` array, the model output is an ordered `output` array of typed items, such as `message`, `function_call`, and `reasoning` items.

| Field | Type | Description |
| --- | --- | --- |
| `output` | array | An ordered array of content items the model generated, such as `message`, `function_call`, or `reasoning` items. |
| `output_text` | string | An SDK convenience property that aggregates the text from the output message items. |
| `output[].content[].text` | string | The assistant text inside an output `message` item. |
| `status` | string | The response status, such as `completed`, `incomplete`, or `failed`. |
| `usage.input_tokens` | integer | The number of tokens in the input. |
| `usage.output_tokens` | integer | The number of generated tokens, including reasoning tokens. |
| `usage.total_tokens` | integer | The total number of tokens used. |

The following example shows a Responses API object for a text response.

```json
{
  "id": "resp_<id>",
  "object": "response",
  "created_at": 1785277080,
  "status": "completed",
  "model": "<deployment-name>",
  "output": [
    {
      "type": "message",
      "id": "msg_<id>",
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "An agentic coding workflow plans tasks, selects tools, and executes multiple steps with minimal supervision.",
          "annotations": []
        }
      ]
    }
  ],
  "output_text": "An agentic coding workflow plans tasks, selects tools, and executes multiple steps with minimal supervision.",
  "usage": {
    "input_tokens": 36,
    "output_tokens": 128,
    "total_tokens": 164
  }
}
```

When the model requests a tool, the `output` array contains a `function_call` item instead of a `message` item.

```json
{
  "id": "resp_<id>",
  "object": "response",
  "created_at": 1785277080,
  "status": "completed",
  "model": "<deployment-name>",
  "output": [
    {
      "type": "function_call",
      "id": "fc_<id>",
      "call_id": "call_abc123",
      "name": "get_weather",
      "arguments": "{\"city\":\"San Francisco\"}",
      "status": "completed"
    }
  ],
  "output_text": "",
  "usage": {
    "input_tokens": 87,
    "output_tokens": 41,
    "total_tokens": 128
  }
}
```

### Token limits and context window

Grok 4.6 (preview) has a context window of 200,000 tokens. Output is capped at 128,000 tokens, or the remaining context budget after input, whichever is smaller.

Input and generated output both count against the context window:

- **Input tokens**: The messages (Chat Completions) or input (Responses) in your request count toward the input token budget.
- **Output tokens**: `max_completion_tokens` (Chat Completions) or `max_output_tokens` (Responses) bounds the generated response, up to the 128,000-token output cap, and includes reasoning tokens.
- **Total**: Input and output tokens must fit within the 200,000-token context window. If a request exceeds the context window, it fails.

## Supported deployment types and regions

Grok 4.6 supports **Global Standard deployment** type in all regions. For supported deployment regions, see [Region availability for Foundry Models sold by Azure](../concepts/models-sold-directly-by-azure-region-availability.md).

## API quotas and limits

Grok 4.6 (preview) in Foundry has the following rate limits measured in requests per minute (RPM) and tokens per minute (TPM). The tier available to you depends on your subscription and deployment configuration.

| Deployment Type | Tier    | TPM     | RPM |
|-----------------|---------|:-------:|:---:|
| Global Standard | Low     | 0       | 0   |
| Global Standard | Medium  | 50,000 | 50 |
| Global Standard | High    | 5,000,000 | 5,000 |

You can request more quota if needed. For more information, see [Request increases to the default limits](../quotas-limits.md#request-increases-to-the-default-limits).

## Troubleshoot

Use the following table to identify common errors and resolutions.

| Error | Possible cause | Resolution |
| --- | --- | --- |
| 400 Bad Request | Invalid request shape or unsupported parameter. | Validate the request body against the API contract, and check the supported parameters. |
| 401 Unauthorized | Invalid API key, an expired token, or a missing or incorrect authentication header. | Check your credential, token scope, and header (`api-key` for API keys, `Authorization: Bearer` for Microsoft Entra ID). |
| 403 Forbidden | You're authenticated, but you don't have permission to access the requested model. | Verify your role assignment and model access. |
| 404 Not Found | Incorrect endpoint or deployment name, or the referenced resource wasn't found. | Verify the endpoint and deployment name in Microsoft Foundry. |
| 429 Too Many Requests | You exceeded the rate limit. | Retry with backoff, or request a quota increase if one is available. |
| 500 Internal Server Error | A server-side error or misconfiguration occurred. | Retry with backoff. If the issue persists, check service health and support guidance. |

## Responsible AI considerations

Before you use Grok 4.6 in an application, evaluate the model for your intended scenario. Follow these recommended practices:

- Validate model behavior on realistic prompts.
- Test for task-specific quality, safety, and reliability.
- Use human review for high-impact workflows.
- Log and monitor failures according to your application requirements.
- Apply appropriate content safety and abuse monitoring.

Grok models on Microsoft Foundry expose an OpenAI-compatible Chat Completions and Responses API surface. For the complete request and response schema, see SpaceXAI's [Chat Completions and Responses API reference](https://docs.x.ai/developers/rest-api-reference/inference/chat). Some parameters described there, such as live search options, don't apply to Azure-hosted deployments.

## Related content

- [Microsoft Foundry REST Reference - Azure OpenAI Responses](/rest/api/microsoft-foundry/azureopenai/responses)
- [Microsoft Foundry REST Reference - Azure OpenAI Chat](/rest/api/microsoft-foundry/azureopenai/chat)
- [Foundry Models sold by Azure](../concepts/models-sold-directly-by-azure.md)
- [Deploy Microsoft Foundry Models in the Foundry portal](../how-to/deploy-foundry-models.md)
- [Configure Microsoft Entra ID authentication](../how-to/configure-entra-id.md)
- [How to generate text responses with Microsoft Foundry Models](../how-to/generate-responses.md)
