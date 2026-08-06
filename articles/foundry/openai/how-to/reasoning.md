---
title: "Azure OpenAI reasoning models - GPT-5 series, o3-mini, o1, o1-mini"
description: "Learn how to use Azure OpenAI's advanced GPT-5 series, o3-mini, o1, & o1-mini reasoning models"
manager: mcleans
ms.service: microsoft-foundry
ms.subservice: foundry-openai
ms.topic: how-to
ms.date: 07/29/2026
author: alvinashcraft
ms.author: aashcraft
ai-usage: ai-assisted
ms.custom:
  - classic-and-new
  - doc-kit-assisted
---

# Azure OpenAI reasoning models
Azure OpenAI reasoning models are designed to tackle reasoning and problem-solving tasks with increased focus and capability. These models spend more time processing and understanding the user's request, making them exceptionally strong in areas like science, coding, and math compared to previous iterations.

**Key capabilities of reasoning models:**

- Complex Code Generation: Capable of generating algorithms and handling advanced coding tasks to support developers.
- Advanced Problem Solving: Ideal for comprehensive brainstorming sessions and addressing multifaceted challenges.
- Complex Document Comparison: Perfect for analyzing contracts, case files, or legal documents to identify subtle differences.
- Instruction Following and Workflow Management: Particularly effective for managing workflows requiring shorter contexts.

## Prerequisites

- An Azure OpenAI reasoning model deployed.

- If you use the REST examples:
  - Install the Azure CLI. For more information, see [Install the Azure CLI](/cli/azure/install-azure-cli).
  - Sign in with `az login`, then generate a bearer token and store it in the `AZURE_OPENAI_AUTH_TOKEN` environment variable.

    ```azurecli
    az account get-access-token --resource https://cognitiveservices.azure.com --query accessToken -o tsv
    ```

## Usage

These models [don't currently support the same set of parameters](#api--feature-support) as other models that use the chat completions API. 

### Chat completions API

# [C#](#tab/csharp)

```c#
using Azure.Identity;
using OpenAI;
using OpenAI.Chat;
using System.ClientModel.Primitives;

#pragma warning disable OPENAI001 //currently required for token based authentication

BearerTokenPolicy tokenPolicy = new(
    new DefaultAzureCredential(),
    "https://ai.azure.com/.default");

ChatClient client = new(
    model: "o4-mini",
    authenticationPolicy: tokenPolicy,
    options: new OpenAIClientOptions()
    {

        Endpoint = new Uri("https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1")
    }
);

ChatCompletionOptions options = new ChatCompletionOptions
{
    MaxOutputTokenCount = 100000
};

ChatCompletion completion = client.CompleteChat(
         new DeveloperChatMessage("You are a helpful assistant"),
         new UserChatMessage("Tell me about the bitter lesson")
    );

Console.WriteLine($"[ASSISTANT]: {completion.Content[0].Text}");

```

# [Python](#tab/python)

**Microsoft Entra ID:**

If you're new to using Microsoft Entra ID for authentication see [How to configure Azure OpenAI in Microsoft Foundry Models with Microsoft Entra ID authentication](../../../foundry-classic/openai/how-to/managed-identity.md).

```python
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://ai.azure.com/.default"
)

client = OpenAI(  
  base_url = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",  
  api_key=token_provider,
)

response = client.chat.completions.create(
  model="YOUR-DEPLOYMENT-NAME", # replace with your model deployment name
    messages=[
        {"role": "user", "content": "What steps should I think about when writing my first Python API?"},
    ],
    max_completion_tokens = 5000

)

print(response.model_dump_json(indent=2))
```

**API Key:**

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    base_url="https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
)

response = client.chat.completions.create(
  model="YOUR-DEPLOYMENT-NAME", # replace with your model deployment name
    messages=[
        {"role": "user", "content": "What steps should I think about when writing my first Python API?"},
    ],
    max_completion_tokens = 5000

)

print(response.model_dump_json(indent=2))
```

# [REST](#tab/REST)

```bash
curl -X POST "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AZURE_OPENAI_AUTH_TOKEN" \
  -d '{
      "model": "gpt-5",
      "messages": [
          {"role": "system", "content": "You are a helpful assistant."},
          {"role": "user", "content": "What steps should I think about when writing my first Python API?"}
      ],
      "max_completion_tokens": 1000
  }'
```

# [Output](#tab/output)

**Python  Chat Completions API Output:**

```json
{
  "id": "chatcmpl-AEj7pKFoiTqDPHuxOcirA9KIvf3yz",
  "choices": [
    {
      "finish_reason": "stop",
      "index": 0,
      "logprobs": null,
      "message": {
        "content": "Writing your first Python API is an exciting step in developing software that can communicate with other applications. An API (Application Programming Interface) allows different software systems to interact with each other, enabling data exchange and functionality sharing. Here are the steps you should consider when creating your first Python API...truncated for brevity.",
        "refusal": null,
        "role": "assistant",
        "function_call": null,
        "tool_calls": null
      },
      "content_filter_results": {
        "hate": {
          "filtered": false,
          "severity": "safe"
        },
        "protected_material_code": {
          "filtered": false,
          "detected": false
        },
        "protected_material_text": {
          "filtered": false,
          "detected": false
        },
        "self_harm": {
          "filtered": false,
          "severity": "safe"
        },
        "sexual": {
          "filtered": false,
          "severity": "safe"
        },
        "violence": {
          "filtered": false,
          "severity": "safe"
        }
      }
    }
  ],
  "created": 1728073417,
  "model": "o1-2024-12-17",
  "object": "chat.completion",
  "service_tier": null,
  "system_fingerprint": "fp_503a95a7d8",
  "usage": {
    "completion_tokens": 1843,
    "prompt_tokens": 20,
    "total_tokens": 1863,
    "completion_tokens_details": {
      "audio_tokens": null,
      "reasoning_tokens": 448
    },
    "prompt_tokens_details": {
      "audio_tokens": null,
      "cached_tokens": 0
    }
  },
  "prompt_filter_results": [
    {
      "prompt_index": 0,
      "content_filter_results": {
        "custom_blocklists": {
          "filtered": false
        },
        "hate": {
          "filtered": false,
          "severity": "safe"
        },
        "jailbreak": {
          "filtered": false,
          "detected": false
        },
        "self_harm": {
          "filtered": false,
          "severity": "safe"
        },
        "sexual": {
          "filtered": false,
          "severity": "safe"
        },
        "violence": {
          "filtered": false,
          "severity": "safe"
        }
      }
    }
  ]
}
```

---

## How reasoning works

Reasoning models generate **reasoning tokens** in addition to the input and output tokens you're already familiar with. The model uses those tokens to work through your prompt: breaking the problem apart, weighing approaches, and abandoning paths that don't hold up. Reasoning tokens never appear in the message content, but they occupy space in the context window and are billed as output tokens.

To see how many reasoning tokens a request consumed, check `completion_tokens_details.reasoning_tokens` in a Chat Completions API response, or `output_tokens_details.reasoning_tokens` in a Responses API response.

The `gpt-5.4` and `gpt-5.5` models support interleaved thinking with the Responses API. They can produce visible output before and between periods of reasoning, and reason between tool calls.

Across a multi-turn conversation, input and output tokens carry forward from each turn. What happens to the reasoning from earlier turns depends on the model and on the `reasoning.context` value you set.

:::image type="content" source="../media/how-to/reasoning/reasoning-context-modes.svg" alt-text="Diagram showing that current_turn drops earlier reasoning, while all_turns carries compatible reasoning across three turns." lightbox="../media/how-to/reasoning/reasoning-context-modes.svg":::

To choose a mode, see [Preserve reasoning across calls](#preserve-reasoning-across-calls).

### Manage the context window

Reasoning tokens share the context window with your input and the visible output. A single request can spend anywhere from a few hundred to tens of thousands of reasoning tokens depending on how hard the problem is, so leave room for them when you size a request.

The usage object reports the exact count for each request:

```json
{
  "usage": {
    "input_tokens": 75,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 1186,
    "output_tokens_details": {
      "reasoning_tokens": 1024
    },
    "total_tokens": 1261
  }
}
```

Context window sizes differ by model. For the limits that apply to your deployment, see [API & feature support](#api--feature-support).

### Control costs

Reasoning tokens are billed as output tokens, so a request that thinks longer costs more even when the visible answer is short. To cap the total the model generates, set `max_output_tokens` with the Responses API or `max_completion_tokens` with the Chat Completions API. Both limits cover reasoning tokens, visible output tokens, and formatting tokens.

Capping output addresses only half of a multi-turn workload. Reasoning models also resend a growing conversation on every turn, and `all_turns` adds earlier reasoning items on top of that. To reduce what you pay for those repeated input tokens, see [Prompt caching](./prompt-caching.md).

### Allocate space for reasoning

If generation reaches the context window limit or the token cap you set, the response comes back incomplete:

```json
{
  "status": "incomplete",
  "incomplete_details": {
    "reason": "max_output_tokens"
  }
}
```

This condition can occur before the model produces any visible output. You pay for input and reasoning tokens but receive no answer. Check `status` on every response so your application handles this case instead of treating it as an empty result.

To avoid running out of room, reserve at least 25,000 tokens for reasoning and output while you're getting a feel for a workload. Once you know how many reasoning tokens your prompts typically consume, tune the buffer to match.

### Keep reasoning items in context

When a reasoning model calls functions through the Responses API, pass the reasoning items from the previous response back along with your function output. If the model called several functions in a row, send every reasoning item, function call item, and function call output item since the last user message. The model then continues the same line of reasoning instead of starting over, which reaches a good answer in fewer tokens.

The simplest approach is to pass all output items from the previous response into the next request, either with `previous_response_id` or by copying the items into the next `input` array. Reasoning items that aren't relevant to your functions are ignored, and the relevant ones are retained.

If you trim or reorder context before sending it, keep everything between the last user message and your function call output intact.

## Reasoning effort

The `reasoning_effort` parameter tells the model how much to think before it answers. Supported values vary by model and include `none`, `minimal`, `low`, `medium`, `high`, `xhigh`, and `max`. Defaults vary by model as well. For the values each model accepts, see [API & feature support](#api--feature-support).

| Effort | Best for |
| --- | --- |
| `none` | Latency-critical work that doesn't benefit from reasoning or chained tool calls, such as voice, fast information retrieval, and classification. |
| `low` | Efficient reasoning with a modest latency increase. Suits tool use, planning, search, and multistep decisions where speed and cost matter. |
| `medium` | A balanced starting point for most workloads, especially when the task involves planning, complex reasoning, or judgment. |
| `high` | Hard reasoning, complex debugging, deep planning, and high-value tasks where quality matters more than latency. |
| `xhigh` | Deep research, asynchronous workflows, and agentic tasks with long runs. Use it when your evaluations show a gain that justifies the extra latency and cost. |
| `max` | Your most complex tasks. If you currently use `xhigh`, compare both settings before you switch. |

Reasoning models adapt within a setting, spending fewer tokens on simple tasks and thinking harder on complex ones. The higher the effort, the longer the model spends on the request, which generally produces more [reasoning tokens](#how-reasoning-works).

> [!NOTE]
> `o1-mini` doesn't support `reasoning_effort`.

For a faster first visible token in latency-sensitive applications, prompt the model to produce a short preamble before it reasons more deeply.

### Developer messages

Developer messages (`"role": "developer"`) are functionally the same as system messages.

Adding a developer message to the previous code example would look as follows:

# [C#](#tab/csharp)

```csharp

using Azure.Identity;
using OpenAI;
using OpenAI.Chat;
using System.ClientModel.Primitives;

#pragma warning disable OPENAI001 //currently required for token based authentication

BearerTokenPolicy tokenPolicy = new(
    new DefaultAzureCredential(),
    "https://ai.azure.com/.default");

ChatClient client = new(
    model: "o4-mini",
    authenticationPolicy: tokenPolicy,
    options: new OpenAIClientOptions()
    {

        Endpoint = new Uri("https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1")
    }
);

ChatCompletionOptions options = new ChatCompletionOptions
{
    ReasoningEffortLevel = ChatReasoningEffortLevel.Low,
    MaxOutputTokenCount = 100000
};

ChatCompletion completion = client.CompleteChat(
         new DeveloperChatMessage("You are a helpful assistant"),
         new UserChatMessage("Tell me about the bitter lesson")
    );

Console.WriteLine($"[ASSISTANT]: {completion.Content[0].Text}");

```

# [Python](#tab/python)

**Microsoft Entra ID:**

If you're new to using Microsoft Entra ID for authentication see [How to configure Azure OpenAI with Microsoft Entra ID authentication](../../../foundry-classic/openai/how-to/managed-identity.md).

```python
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
  DefaultAzureCredential(), "https://ai.azure.com/.default"
)

client = OpenAI(
  base_url="https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
  api_key=token_provider,
)

response = client.chat.completions.create(
  model="YOUR-DEPLOYMENT-NAME",  # replace with your model deployment name
  messages=[
    {"role": "developer", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What steps should I think about when writing my first Python API?"},
  ],
  max_completion_tokens=5000,
  reasoning_effort="medium",  # low, medium, or high
)

print(response.model_dump_json(indent=2))
```

**API Key:**

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    base_url="https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
)

response = client.chat.completions.create(
    model="gpt-5-mini", # replace with the model deployment name of your o1 deployment.
    messages=[
        {"role": "developer","content": "You are a helpful assistant."}, # optional equivalent to a system message for reasoning models 
        {"role": "user", "content": "What steps should I think about when writing my first Python API?"},
    ],
    max_completion_tokens = 5000,
    reasoning_effort = "medium" # low, medium, or high
)

print(response.model_dump_json(indent=2))
```

# [REST](#tab/REST)

```bash
curl -X POST "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AZURE_OPENAI_AUTH_TOKEN" \
  -d '{
      "model": "gpt-5",
      "messages": [
        {"role": "developer", "content": "You are a helpful assistant."},
          {"role": "user", "content": "What steps should I think about when writing my first Python API?"}
      ],
      "max_completion_tokens": 1000,
      "reasoning_effort": "medium"
  }'
```

# [Output](#tab/output)

**Python  Chat Completions API Output:**

```json
{
  "id": "chatcmpl-CaODNsQOHoRLcb9JVSKYY1e2Iss5s",
  "choices": [
    {
      "finish_reason": "stop",
      "index": 0,
      "logprobs": null,
      "message": {
        "content": "Here's a practical, beginner‑friendly checklist to guide you through writing your first Python API, from idea to production.\n\n1) Clarify goals and constraints\n- Who will use it (internal team, public), what problems it solves, expected traffic, latency requirements.\n- Resources you'll expose (users, orders, etc.) and core operations.\n- Non‑functional needs: security, compliance, uptime, scalability.\n\n2) Choose your API style\n- REST (most common for CRUD and simple integrations).\n- GraphQL (flexible queries, more complex to secure/monitor).\n- gRPC (high‑performance, strongly typed, good for service‑to‑service).\n- For a first API, REST + JSON is usually best.\n\n3) Design the contract first\n- Draft an OpenAPI/Swagger spec: endpoints, request/response schemas, status codes, error model.\n- Decide naming conventions, pagination, filtering, sorting.\n- Define consistent time/date format (ISO‑8601, UTC), ID format, and field casing.\n- Plan versioning strategy (e.g., /v1) and deprecation policy.\n\n4) Plan security and auth\n- Pick auth: API keys for simple internal use; OAuth2/JWT for user auth; mTLS for service‑to‑service.\n- CORS policy for browsers; HTTPS everywhere; security headers.\n- Validate all inputs; avoid leaking stack traces; define rate limits and quotas.\n\n5) Pick your Python stack\n- Frameworks: FastAPI (great typing, validation, auto docs), Flask (minimal), Django REST Framework (batteries included).\n- ASGI/WSGI server: Uvicorn or Gunicorn.\n- Data layer: PostgreSQL + SQLAlchemy/Django ORM; migrations with Alembic/Django migrations.\n- Caching: Redis (optional).\n- Background jobs: Celery/RQ (if needed).\n\n6) Set up the project\n- Create a virtual environment; choose dependency management (pip, Poetry).\n- Establish project structure (app, api, models, services, tests).\n- Add linting/formatting/type checks: black, isort, flake8, mypy; pre‑commit hooks.\n- Configuration via environment variables; secrets via a manager (not in code).\n\n7) Implement core functionality\n- Build endpoints that match your spec; keep business logic in a service layer, not in route handlers.\n- Schema validation (Pydantic with FastAPI, Marshmallow for Flask).\n- Consistent responses and errors; use clear status codes (201 create, 204 no content, 400/404/409/422, 500).\n- Pagination and filtering; idempotency for certain POST operations; ETags/conditional requests if useful.\n\n8) Error handling and an error model\n- Define a standard error body (code, message, details, correlation_id).\n- Log errors with context; don't expose internal details to clients.\n\n9) Testing strategy\n- Unit tests for services/validators.\n- Integration tests for endpoints (pytest + httpx/requests) with a test database.\n- Contract tests to assert the API matches the OpenAPI spec.\n- Mock external services; measure coverage and focus on critical paths.\n\n10) Documentation and developer experience\n- Auto‑generated docs (FastAPI provides Swagger/ReDoc).\n- Write examples for each endpoint; onboarding and usage notes.\n- Keep a changelog and release notes.\n\n11) Observability and reliability\n- Structured logging (JSON), include request IDs/correlation IDs.\n- Metrics (requests, latency, error rates), health/readiness endpoints.\n- Tracing (OpenTelemetry) if you have multiple services.\n- Error reporting (Sentry or similar).\n\n12) Deployment and operations\n- Containerize with Docker; follow 12‑factor app principles.\n- CI/CD pipeline: run tests, build image, deploy, run migrations.\n- Choose hosting (Render, Fly.io, Railway, Heroku, AWS/GCP/Azure).\n- Configure scaling, connection pools, and timeouts; use a reverse proxy if needed.\n\n13) Performance and data concerns\n- Index your database; avoid N+1 queries; use connection pooling.\n- Load test key endpoints; profile hotspots.\n- Caching strategies where appropriate; consider async I/O for high‑concurrency workloads.\n\n14) Versioning and lifecycle management\n- Keep backward compatibility for minor changes; add fields rather than changing semantics.\n- Communicate deprecations; sunset old versions with a timeline.\n\n15) Governance, compliance, and safety\n- Handle PII correctly; data retention and audit logs if required.\n- Least‑privilege DB access; rotate secrets; review third‑party dependencies.\n\nBeginner‑friendly defaults\n- FastAPI + Pydantic + Uvicorn\n- PostgreSQL + SQLAlchemy + Alembic\n- pytest + httpx + coverage\n- black, isort, flake8, mypy, pre‑commit\n- Docker + simple CI (GitHub Actions) + a managed host\n\nCommon pitfalls to avoid\n- Inconsistent status codes or error formats.\n- Weak input validation and missing authentication.\n- Business logic inside route handlers (hard to test/maintain).\n- No migrations or tests; no logging/metrics.\n- Ignoring pagination and timezones; returning unbounded lists.\n\nIf you share whether it's public vs internal, expected traffic, and preferred framework, I can tailor this to a concrete starter plan and recommended tools.",
        "refusal": null,
        "role": "assistant",
        "annotations": [],
        "audio": null,
        "function_call": null,
        "tool_calls": null
      },
      "content_filter_results": {
        "hate": {
          "filtered": false,
          "severity": "safe"
        },
        "protected_material_code": {
          "filtered": false,
          "detected": false
        },
        "protected_material_text": {
          "filtered": false,
          "detected": false
        },
        "self_harm": {
          "filtered": false,
          "severity": "safe"
        },
        "sexual": {
          "filtered": false,
          "severity": "safe"
        },
        "violence": {
          "filtered": false,
          "severity": "safe"
        }
      }
    }
  ],
  "created": 1762788925,
  "model": "gpt-5-2025-08-07",
  "object": "chat.completion",
  "service_tier": null,
  "system_fingerprint": null,
  "usage": {
    "completion_tokens": 2919,
    "prompt_tokens": 29,
    "total_tokens": 2948,
    "completion_tokens_details": {
      "accepted_prediction_tokens": 0,
      "audio_tokens": 0,
      "reasoning_tokens": 1792,
      "rejected_prediction_tokens": 0
    },
    "prompt_tokens_details": {
      "audio_tokens": 0,
      "cached_tokens": 0
    }
  },
  "prompt_filter_results": [
    {
      "prompt_index": 0,
      "content_filter_results": {
        "hate": {
          "filtered": false,
          "severity": "safe"
        },
        "jailbreak": {
          "filtered": false,
          "detected": false
        },
        "self_harm": {
          "filtered": false,
          "severity": "safe"
        },
        "sexual": {
          "filtered": false,
          "severity": "safe"
        },
        "violence": {
          "filtered": false,
          "severity": "safe"
        }
      }
    }
  ]
}
```

---

## Reasoning mode

The `gpt-5.6` models support two execution modes in the Responses API. Standard mode is the default on Azure OpenAI. Set `reasoning.mode` to `pro` for difficult tasks that justify more model work and can absorb the extra latency.

Mode and effort are independent controls. The mode selects standard or pro execution, and `reasoning_effort` controls how much reasoning the model applies within that mode.

```json
{
  "model": "gpt-5.6",
  "reasoning": {
    "mode": "pro",
    "effort": "medium"
  },
  "input": "Review this database migration plan and identify potential failure modes."
}
```

Pro mode aggregates the work it performs into a single answer and bills those tokens at the model's standard rates. Because it performs more work than standard mode, expect higher token usage and higher cost. Existing pro model deployments keep their current behavior and pricing.

## Reasoning summary

When using the latest reasoning models with the [Responses API](./responses.md) you can use the reasoning summary parameter to receive summaries of the model's chain of thought reasoning. 

> [!IMPORTANT]
> Attempting to extract raw reasoning through methods other than the reasoning summary parameter are not supported, may violate the Acceptable Use Policy, and may result in throttling or suspension when detected.

# [C#](#tab/csharp)

```csharp
using OpenAI;
using OpenAI.Responses;
using System.ClientModel.Primitives;
using Azure.Identity;

#pragma warning disable OPENAI001 //currently required for token based authentication

BearerTokenPolicy tokenPolicy = new(
    new DefaultAzureCredential(),
    "https://ai.azure.com/.default");

OpenAIResponseClient client = new(
    model: "o4-mini",
    authenticationPolicy: tokenPolicy,
    options: new OpenAIClientOptions()
    {
        Endpoint = new Uri("https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1")
    }
);

OpenAIResponse response = await client.CreateResponseAsync(
    userInputText: "What's the optimal strategy to win at poker?",
    new ResponseCreationOptions()
    {
        ReasoningOptions = new ResponseReasoningOptions()
        {
            ReasoningEffortLevel = ResponseReasoningEffortLevel.High,
            ReasoningSummaryVerbosity = ResponseReasoningSummaryVerbosity.Auto,
        },
    });

// Get the reasoning summary from the first OutputItem (ReasoningResponseItem)
Console.WriteLine("=== Reasoning Summary ===");
foreach (var item in response.OutputItems)
{
    if (item is ReasoningResponseItem reasoningItem)
    {
        foreach (var summaryPart in reasoningItem.SummaryParts)
        {
            if (summaryPart is ReasoningSummaryTextPart textPart)
            {
                Console.WriteLine(textPart.Text);
            }
        }
    }
}

Console.WriteLine("\n=== Assistant Response ===");
// Get the assistant's output
Console.WriteLine(response.GetOutputText());
```

# [Python](#tab/python)

You'll need to upgrade your OpenAI client library for access to the latest parameters.

```cmd
pip install openai --upgrade
```

**Microsoft Entra ID:**

```python
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://ai.azure.com/.default"
)

client = OpenAI(  
  base_url = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",  
  api_key=token_provider,
)

response = client.responses.create(
    input="Tell me about the curious case of neural text degeneration",
    model="gpt-5", # replace with model deployment name
    reasoning={
        "effort": "medium",
        "summary": "auto" # auto, concise, or detailed, gpt-5 series do not support concise 
    },
    text={
        "verbosity": "low" # New with GPT-5 models
    }
)

print(response.model_dump_json(indent=2))
```

**API Key:**

```python
import os
from openai import OpenAI

client = OpenAI(  
  base_url = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
  api_key=os.getenv("AZURE_OPENAI_API_KEY")  
)

response = client.responses.create(
    input="Tell me about the curious case of neural text degeneration",
    model="gpt-5", # replace with model deployment name
    reasoning={
        "effort": "medium",
        "summary": "auto" # auto, concise, or detailed, gpt-5 series do not support concise 
    },
    text={
        "verbosity": "low" # New with GPT-5 models
    }
)

print(response.model_dump_json(indent=2))
```

# [REST](#tab/REST)

```bash
curl -X POST "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/responses" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AZURE_OPENAI_AUTH_TOKEN" \
 -d '{
     "model": "gpt-5",
     "input": "Tell me about the curious case of neural text degeneration",
     "reasoning": {"summary": "auto"},
     "text": {"verbosity": "low"}
    }'
```

# [Output](#tab/output)

```output
{
  "id": "resp_689a0a3090808190b418acf12b5cc40e0fc1c31bc69d8719",
  "created_at": 1754925616.0,
  "error": null,
  "incomplete_details": null,
  "instructions": null,
  "metadata": {},
  "model": "gpt-5",
  "object": "response",
  "output": [
    {
      "id": "rs_689a0a329298819095d90c34dc9b80db0fc1c31bc69d8719",
      "summary": [],
      "type": "reasoning",
      "encrypted_content": null,
      "status": null
    },
    {
      "id": "msg_689a0a33009881909fe0fcf57cba30200fc1c31bc69d8719",
      "content": [
        {
          "annotations": [],
          "text": "Neural text degeneration refers to the ways language models produce low-quality, repetitive, or vacuous text, especially when generating long outputs. It's "curious" because models trained to imitate fluent text can still spiral into unnatural patterns. Key aspects:\n\n- Repetition and loops: The model repeats phrases or sentences ("I'm sorry, but..."), often due to high-confidence tokens reinforcing themselves.\n- Loss of specificity: Vague, generic, agreeable text that avoids concrete details.\n- Drift and contradiction: The output gradually departs from context or contradicts itself over long spans.\n- Exposure bias: During training, models see gold-standard prefixes; at inference, they must condition on their own imperfect outputs, compounding errors.\n- Likelihood vs. quality mismatch: Maximizing token-level likelihood doesn't align with human preferences for diversity, coherence, or factuality.\n- Token over-optimization: Frequent, safe tokens get overused; certain phrases become attractors.\n- Entropy collapse: With greedy or low-temperature decoding, the distribution narrows too much, causing repetitive, low-entropy text.\n- Length and beam search issues: Larger beams or long generations can favor bland, repetitive sequences (the "likelihood trap").\n\nCommon mitigations:\n\n- Decoding strategies:\n  - Top-k, nucleus (top-p), or temperature sampling to keep sufficient entropy.\n  - Typical sampling and locally typical sampling to avoid dull but high-probability tokens.\n  - Repetition penalties, presence/frequency penalties, no-repeat n-grams.\n  - Contrastive decoding (and variants like DoLa) to filter generic continuations.\n  - Min/max length, stop sequences, and beam search with diversity/penalties.\n\n- Training and alignment:\n  - RLHF/DPO to better match human preferences for non-repetitive, helpful text.\n  - Supervised fine-tuning on high-quality, diverse data; instruction tuning.\n  - Debiasing objectives (unlikelihood training) to penalize repetition and banned patterns.\n  - Mixture-of-denoisers or latent planning to improve long-range coherence.\n\n- Architectural and planning aids:\n  - Retrieval-augmented generation to ground outputs.\n  - Tool use and structured prompting to constrain drift.\n  - Memory and planning modules, hierarchical decoding, or sentence-level control.\n\n- Prompting tips:\n  - Ask for concise answers, set token limits, and specify structure.\n  - Provide concrete constraints or content to reduce generic filler.\n  - Use "say nothing if uncertain" style instructions to avoid vacuity.\n\nRepresentative papers/terms to search:\n- Holtzman et al., "The Curious Case of Neural Text Degeneration" (2020): nucleus sampling.\n- Welleck et al., "Neural Text Degeneration with Unlikelihood Training."\n- Li et al., "A Contrastive Framework for Decoding."\n- Su et al., "DoLa: Decoding by Contrasting Layers."\n- Meister et al., "Typical Decoding."\n- Ouyang et al., "Training language models to follow instructions with human feedback."\n\nIn short, degeneration arises from a mismatch between next-token likelihood and human preferences plus decoding choices; careful decoding, training objectives, and grounding help prevent it.",
          "type": "output_text",
          "logprobs": null
        }
      ],
      "role": "assistant",
      "status": "completed",
      "type": "message"
    }
  ],
  "parallel_tool_calls": true,
  "temperature": 1.0,
  "tool_choice": "auto",
  "tools": [],
  "top_p": 1.0,
  "background": false,
  "max_output_tokens": null,
  "max_tool_calls": null,
  "previous_response_id": null,
  "prompt": null,
  "prompt_cache_key": null,
  "reasoning": {
    "effort": "minimal",
    "generate_summary": null,
    "summary": "detailed"
  },
  "safety_identifier": null,
  "service_tier": "default",
  "status": "completed",
  "text": {
    "format": {
      "type": "text"
    }
  },
  "top_logprobs": null,
  "truncation": "disabled",
  "usage": {
    "input_tokens": 16,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 657,
    "output_tokens_details": {
      "reasoning_tokens": 0
    },
    "total_tokens": 673
  },
  "user": null,
  "content_filters": null,
  "store": true
}
```

---

> [!NOTE]
> Even when enabled, reasoning summaries are not guaranteed to be generated for every step/request. This is expected behavior.

## Preserve reasoning across calls

Conversation state and reasoning state aren't the same thing. Passing messages across calls gives the model the visible conversation history. Persisted reasoning goes a step further: on models that support it, the model can also render its own reasoning items from earlier turns into the current context.

Persisted reasoning is about continuity, not transparency. The reasoning items stay opaque, and the API never returns their reasoning text. Set `reasoning.context` to control which of the available reasoning items the model can draw on.

| Value | Behavior |
| --- | --- |
| `auto` | Uses the model's default. Omitting `reasoning.context` has the same effect. |
| `current_turn` | Makes the active turn's reasoning available to the model, but doesn't render reasoning from earlier turns into the next sample. |
| `all_turns` | Renders available, compatible reasoning items from earlier turns into the next sample. Only the `gpt-5.6` models support this value. |

The `gpt-5.6` models support `all_turns` and use it by default. Earlier reasoning models default to `current_turn`.

> [!IMPORTANT]
> Because `all_turns` renders more reasoning items into context, it increases the tokens billed for a request. If you upgrade an existing workload to a `gpt-5.6` model, expect higher token consumption on multi-turn conversations even when your code doesn't change. Set `reasoning.context` to `current_turn` to keep the earlier behavior.

Keep these behaviors in mind:

- Setting `reasoning.context` doesn't create reasoning items that aren't already available. It only controls which existing items the model renders.
- `all_turns` has an effect only when the request can reach earlier response items. Use `previous_response_id`, attach the response to a conversation, or replay the complete response history yourself.
- On the first request in a conversation, `current_turn` and `all_turns` behave the same way, because no earlier reasoning exists yet.
- Each response reports the mode it actually used in its `reasoning.context` field, as either `current_turn` or `all_turns`. Check that field to confirm the effective mode.

### Continue reasoning with stored responses

When you store responses, `previous_response_id` is the shortest way to make earlier reasoning available to the model.

# [C#](#tab/csharp)

A C# example for `reasoning.context` isn't available yet. Select the **Python** or **REST** tab to see how to set the mode and read the effective value back from the response.

# [Python](#tab/python)

```python
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://ai.azure.com/.default"
)

client = OpenAI(
    base_url="https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
    api_key=token_provider,
)

# First turn: no earlier reasoning exists yet.
first = client.responses.create(
    model="gpt-5.6",  # replace with your model deployment name
    input="Inspect this repository and identify the likely bug.",
    reasoning={"context": "current_turn"},
)

# Second turn: previous_response_id gives the model access to earlier items.
second = client.responses.create(
    model="gpt-5.6",
    previous_response_id=first.id,
    input="Now patch the bug and explain the change.",
    reasoning={"context": "all_turns"},
)

print(second.output_text)
print(second.reasoning.context)  # effective mode: current_turn or all_turns
```

# [REST](#tab/REST)

```bash
# First turn: no earlier reasoning exists yet.
curl -X POST "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/responses" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AZURE_OPENAI_AUTH_TOKEN" \
  -d '{
      "model": "gpt-5.6",
      "input": "Inspect this repository and identify the likely bug.",
      "reasoning": {"context": "current_turn"}
  }'

# Second turn: pass the ID returned by the first response.
curl -X POST "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/responses" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AZURE_OPENAI_AUTH_TOKEN" \
  -d '{
      "model": "gpt-5.6",
      "previous_response_id": "resp_abc123",
      "input": "Now patch the bug and explain the change.",
      "reasoning": {"context": "all_turns"}
  }'
```

# [Output](#tab/output)

The second call prints the model's answer, followed by the effective reasoning context mode:

```output
<model response text>
all_turns
```

---

Use `current_turn` when you replay older response items that the model no longer needs. Those items can stay in the request payload for continuity, but the service doesn't render them into the new sample, which reduces the rendered context in long-running workflows.

### Preserve reasoning without stored responses

In stateless mode, reasoning items in the response's `output` array include an `encrypted_content` property by default. Stateless mode applies when you set `store` to `false`, and when your organization uses Zero Data Retention. You don't need to request the property: the API still accepts `reasoning.encrypted_content` in the `include` parameter for compatibility, but no longer requires it.

To use `all_turns` in this mode, keep every output item, append the next user message, and replay the complete history.

# [C#](#tab/csharp)

A C# example for stateless persisted reasoning isn't available yet. Select the **Python** or **REST** tab to see how to replay encrypted reasoning items across turns.

# [Python](#tab/python)

```python
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://ai.azure.com/.default"
)

client = OpenAI(
    base_url="https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
    api_key=token_provider,
)

history = [{"role": "user", "content": "Inspect this repository and identify the likely bug."}]

# Stateless requests return encrypted reasoning items in the output array.
first = client.responses.create(
    model="gpt-5.6",  # replace with your model deployment name
    store=False,
    input=history,
    reasoning={"context": "current_turn"},
)

# Replay every output item, including the encrypted reasoning.
history.extend(item.model_dump() for item in first.output)
history.append({"role": "user", "content": "Now patch the bug and explain the change."})

second = client.responses.create(
    model="gpt-5.6",
    store=False,
    input=history,
    reasoning={"context": "all_turns"},
)

print(second.output_text)
```

# [REST](#tab/REST)

```bash
curl -X POST "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/responses" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AZURE_OPENAI_AUTH_TOKEN" \
  -d '{
      "model": "gpt-5.6",
      "store": false,
      "input": "Inspect this repository and identify the likely bug.",
      "reasoning": {"context": "current_turn"}
  }'
```

The reasoning items in the `output` array carry an `encrypted_content` property. Send those items back, along with the next user message, in the `input` array of your next request and set `reasoning.context` to `all_turns`.

# [Output](#tab/output)

Each reasoning item in the `output` array includes the encrypted payload that you replay in the next request:

```json
{
  "id": "rs_<reasoning_item_id>",
  "type": "reasoning",
  "summary": [],
  "encrypted_content": "<encrypted reasoning payload>",
  "status": null
}
```

---

For more information about encrypted reasoning items, see [Encrypted reasoning items](./responses.md#encrypted-reasoning-items).

## Phase parameter

In long-running or tool-heavy workflows that use `gpt-5.5` and `gpt-5.4` in the Responses API, mark each assistant message with a `phase` value. The parameter is optional, but omitting it can cause the model to treat a preamble as the final answer and stop early.

Use `commentary` for intermediate assistant updates, such as the preamble a model produces before a tool call, and `final_answer` for the completed response. Don't add `phase` to user messages.

```json
{
  "model": "gpt-5.5",
  "input": [
    {
      "role": "assistant",
      "phase": "commentary",
      "content": "I'll inspect the logs, then summarize the root cause and the fix."
    },
    {
      "role": "assistant",
      "phase": "final_answer",
      "content": "Root cause: a cache invalidation race."
    },
    {
      "role": "user",
      "content": "Now give me a rollout-safe fix plan."
    }
  ]
}
```

When you continue a conversation by using `previous_response_id`, the service preserves the earlier assistant state for you. If you replay assistant history yourself, keep each message's original `phase` value.

## Python lark

GPT-5 series reasoning models have the ability to call a new `custom_tool` called `lark_tool`. This tool is based on [Python lark](https://github.com/lark-parser/lark) and can be used for more flexible constraining of model output.

### Responses API

```json
{
  "model": "gpt-5-2025-08-07",
  "input": "please calculate the area of a circle with radius equal to the number of 'r's in strawberry",
  "tools": [
    {
      "type": "custom",
      "name": "lark_tool",
      "format": {
        "type": "grammar",
        "syntax": "lark",
        "definition": "start: QUESTION NEWLINE ANSWER\nQUESTION: /[^\\n?]{1,200}\\?/\nNEWLINE: /\\n/\nANSWER: /[^\\n!]{1,200}!/"
      }
    }
  ],
  "tool_choice": "required"
}
```

**Microsoft Entra ID:**

```python
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://ai.azure.com/.default"
)

client = OpenAI(  
  base_url = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",  
  api_key=token_provider,
)

response = client.responses.create(  
    model="gpt-5",  # replace with your model deployment name  
    tools=[  
        {  
            "type": "custom",
            "name": "lark_tool",
            "format": {
                "type": "grammar",
                "syntax": "lark",
                "definition": "start: QUESTION NEWLINE ANSWER\nQUESTION: /[^\\n?]{1,200}\\?/\nNEWLINE: /\\n/\nANSWER: /[^\\n!]{1,200}!/"
            }
        }  
    ],  
    input=[{"role": "user", "content": "Please calculate the area of a circle with radius equal to the number of 'r's in strawberry"}],  
)  

print(response.model_dump_json(indent=2))  
```

**API Key:**

```python
import os
from openai import OpenAI

client = OpenAI(  
  base_url = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
  api_key=os.getenv("AZURE_OPENAI_API_KEY")  
)

response = client.responses.create(  
    model="gpt-5",  # replace with your model deployment name  
    tools=[  
        {  
            "type": "custom",
            "name": "lark_tool",
            "format": {
                "type": "grammar",
                "syntax": "lark",
                "definition": "start: QUESTION NEWLINE ANSWER\nQUESTION: /[^\\n?]{1,200}\\?/\nNEWLINE: /\\n/\nANSWER: /[^\\n!]{1,200}!/"
            }
        }  
    ],  
    input=[{"role": "user", "content": "Please calculate the area of a circle with radius equal to the number of 'r's in strawberry"}],  
)  

print(response.model_dump_json(indent=2))  
  
```

**Output**:

```json
{
  "id": "resp_689a0cf927408190b8875915747667ad01c936c6ffb9d0d3",
  "created_at": 1754926332.0,
  "error": null,
  "incomplete_details": null,
  "instructions": null,
  "metadata": {},
  "model": "gpt-5",
  "object": "response",
  "output": [
    {
      "id": "rs_689a0cfd1c888190a2a67057f471b5cc01c936c6ffb9d0d3",
      "summary": [],
      "type": "reasoning",
      "encrypted_content": null,
      "status": null
    },
    {
      "id": "msg_689a0d00e60c81908964e5e9b2d6eeb501c936c6ffb9d0d3",
      "content": [
        {
          "annotations": [],
          "text": ""strawberry" has 3 r's, so the radius is 3.\nArea = πr<sup>2</sup> = π × 3<sup>2</sup> = 9π ≈ 28.27 square units.",
          "type": "output_text",
          "logprobs": null
        }
      ],
      "role": "assistant",
      "status": "completed",
      "type": "message"
    }
  ],
  "parallel_tool_calls": true,
  "temperature": 1.0,
  "tool_choice": "auto",
  "tools": [
    {
      "name": "lark_tool",
      "parameters": null,
      "strict": null,
      "type": "custom",
      "description": null,
      "format": {
        "type": "grammar",
        "definition": "start: QUESTION NEWLINE ANSWER\nQUESTION: /[^\\n?]{1,200}\\?/\nNEWLINE: /\\n/\nANSWER: /[^\\n!]{1,200}!/",
        "syntax": "lark"
      }
    }
  ],
  "top_p": 1.0,
  "background": false,
  "max_output_tokens": null,
  "max_tool_calls": null,
  "previous_response_id": null,
  "prompt": null,
  "prompt_cache_key": null,
  "reasoning": {
    "effort": "medium",
    "generate_summary": null,
    "summary": null
  },
  "safety_identifier": null,
  "service_tier": "default",
  "status": "completed",
  "text": {
    "format": {
      "type": "text"
    }
  },
  "top_logprobs": null,
  "truncation": "disabled",
  "usage": {
    "input_tokens": 139,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 240,
    "output_tokens_details": {
      "reasoning_tokens": 192
    },
    "total_tokens": 379
  },
  "user": null,
  "content_filters": null,
  "store": true
}
```

### Chat Completions

```json
{
  "messages": [
    {
      "role": "user",
      "content": "Which one is larger, 42 or 0?"
    }
  ],
  "tools": [
    {
      "type": "custom",
      "name": "custom_tool",
      "custom": {
        "name": "lark_tool",
        "format": {
          "type": "grammar",
          "grammar": {
            "syntax": "lark",
            "definition": "start: QUESTION NEWLINE ANSWER\nQUESTION: /[^\\n?]{1,200}\\?/\nNEWLINE: /\\n/\nANSWER: /[^\\n!]{1,200}!/"
          }
        }
      }
    }
  ],
  "tool_choice": "required",
  "model": "gpt-5-2025-08-07"
}
```

## Availability

### Region availability

| Model | Region | Limited access |
| --- | --- | --- |
| `gpt-5.6-sol` | [Model availability](../../foundry-models/concepts/models-sold-directly-by-azure-region-availability.md?pivots=standard) | No access request needed. Quota request required depending on [quota tier](../quotas-limits.md). Tier 5 and Tier 6 subscriptions have quota by default. |
| `gpt-5.6-terra` | [Model availability](../../foundry-models/concepts/models-sold-directly-by-azure-region-availability.md?pivots=standard) | No access request needed. Quota request required depending on [quota tier](../quotas-limits.md). Tier 5 and Tier 6 subscriptions have quota by default. |
| `gpt-5.6-luna` | [Model availability](../../foundry-models/concepts/models-sold-directly-by-azure-region-availability.md?pivots=standard) | No access request needed. Quota request required depending on [quota tier](../quotas-limits.md). Tier 5 and Tier 6 subscriptions have quota by default. |
| `gpt-chat-latest` | [Model availability](../../foundry-models/concepts/models-sold-directly-by-azure-region-availability.md?pivots=standard) | No access request needed. |
| `gpt-5.5` | [Model availability](../../foundry-models/concepts/models-sold-directly-by-azure-region-availability.md?pivots=standard) | No access request needed. Quota request required depending on [quota tier](../quotas-limits.md). Tier 5 and Tier 6 subscriptions have quota by default. |
| `gpt-5.4-mini` | [Model availability](../../foundry-models/concepts/models-sold-directly-by-azure-region-availability.md?pivots=standard) | No access request needed. |
| `gpt-5.4-nano` | [Model availability](../../foundry-models/concepts/models-sold-directly-by-azure-region-availability.md?pivots=standard) | No access request needed. |
| `gpt-5.4-pro` | [Model availability](../../foundry-models/concepts/models-sold-directly-by-azure-region-availability.md?pivots=standard) | Access is no longer restricted for this model. |
| `gpt-5.4` | [Model availability](../../foundry-models/concepts/models-sold-directly-by-azure-region-availability.md?pivots=standard) | Access is no longer restricted for this model. |
| `gpt-5.3-codex` | [Model availability](../../foundry-models/concepts/models-sold-directly-by-azure-region-availability.md?pivots=standard) | Access is no longer restricted for this model. |
| `gpt-5.2-codex` | [Model availability](../../foundry-models/concepts/models-sold-directly-by-azure-region-availability.md?pivots=standard) | Access is no longer restricted for this model. |
| `gpt-5.2` | [Model availability](../../foundry-models/concepts/models-sold-directly-by-azure-region-availability.md?pivots=standard) | Access is no longer restricted for this model. |
| `gpt-5.1-codex-max` | [Model availability](../../foundry-models/concepts/models-sold-directly-by-azure-region-availability.md?pivots=standard) | Access is no longer restricted for this model. |
| `gpt-5.1` | [Model availability](../../foundry-models/concepts/models-sold-directly-by-azure-region-availability.md?pivots=standard) | Access is no longer restricted for this model. |
| `gpt-5.1-chat` | [Model availability](../../foundry-models/concepts/models-sold-directly-by-azure-region-availability.md?pivots=standard) | No access request needed. |
| `gpt-5.1-codex` | [Model availability](../../foundry-models/concepts/models-sold-directly-by-azure-region-availability.md?pivots=standard) | Access is no longer restricted for this model. |
| `gpt-5.1-codex-mini` | [Model availability](../../foundry-models/concepts/models-sold-directly-by-azure-region-availability.md?pivots=standard) | No access request needed. | 
| `gpt-5-pro` | [Model availability](../../foundry-models/concepts/models-sold-directly-by-azure-region-availability.md?pivots=standard) | Access is no longer restricted for this model. |
| `gpt-5-codex` | [Model availability](../../foundry-models/concepts/models-sold-directly-by-azure-region-availability.md?pivots=standard) | Access is no longer restricted for this model. |
| `gpt-5` | [Model availability](../../foundry-models/concepts/models-sold-directly-by-azure-region-availability.md?pivots=standard) | Access is no longer restricted for this model. |
| `gpt-5-mini` | [Model availability](../../foundry-models/concepts/models-sold-directly-by-azure-region-availability.md?pivots=standard) | No access request needed. |
| `gpt-5-nano` | [Model availability](../../foundry-models/concepts/models-sold-directly-by-azure-region-availability.md?pivots=standard) | No access request needed. |
| `o3-pro` | [Model availability](../../foundry-models/concepts/models-sold-directly-by-azure-region-availability.md?pivots=standard) | Access is no longer restricted for this model. |
| `codex-mini` | [Model availability](../../foundry-models/concepts/models-sold-directly-by-azure-region-availability.md?pivots=standard) | No access request needed. |
| `o4-mini` | [Model availability](../../foundry-models/concepts/models-sold-directly-by-azure-region-availability.md?pivots=standard) | Access is no longer restricted for this model. |
| `o3` | [Model availability](../../foundry-models/concepts/models-sold-directly-by-azure-region-availability.md?pivots=standard) | Access is no longer restricted for this model. |
| `o3-mini` | [Model availability](../../foundry-models/concepts/models-sold-directly-by-azure-region-availability.md?pivots=standard) | Access is no longer restricted for this model. |
| `o1` | [Model availability](../../foundry-models/concepts/models-sold-directly-by-azure-region-availability.md?pivots=standard) | Access is no longer restricted for this model. |

## API & feature support

Input and output limits share the available context budget and aren't additive. For details and a GPT-5.5 calculation example, see [Understand model token limits](../../foundry-models/concepts/models-sold-directly-by-azure.md?pivots=azure-openai#understand-model-token-limits) and [Responses API token budget](../../foundry-models/concepts/models-sold-directly-by-azure.md?pivots=azure-openai#responses-api-token-budget).

# [GPT-5 Reasoning Models](#tab/gpt-5)

| **Feature**  | **gpt-5.6-sol**, **2026-06-25** | **gpt-5.6-terra**, **2026-06-25** | **gpt-5.6-luna**, **2026-06-25** | **gpt-5.5**, **2026-04-24** |**gpt-5.4-nano**, **2026-03-17** | **gpt-5.4-mini**, **2026-03-17** | **gpt-5.4-pro**  | **gpt-5.4**, **2026-03-05** | **gpt-5.3-codex**, **2026-02-24** | **gpt-5.2-codex**, **2026-01-14**  | **gpt-5.2**, **2025-12-11** | **gpt-5.1-codex-max**, **2025-12-04** | **gpt-5.1**, **2025-11-13** | **gpt-5.1-chat**, **2025-11-13** | **gpt-5.1-codex**, **2025-11-13** | **gpt-5.1-codex-mini**, **2025-11-13** | **gpt-5-pro**, **2025-10-06** | **gpt-5-codex**, **2025-09-011**  | **gpt-5**, **2025-08-07**  | **gpt-5-mini**, **2025-08-07**   | **gpt-5-nano**, **2025-08-07**  |
|:-------------------|:----:|:----:|:----:|:----:|:----:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:--------------------------:|:--------------------------:|:------:|:--------:|:--------:|
| **[Developer Messages](#developer-messages)** | ✅ | ✅ | ✅ | ✅ | ✅| ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |✅ |
| **[Structured Outputs](./structured-outputs.md)** | ✅ | ✅ | ✅ | ✅ | ✅ |✅ | ✅ | ✅ | ✅ | ✅ | ✅| ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **[Context Window](../../foundry-models/concepts/models-sold-directly-by-azure.md#o-series-models)** | 1,050,000<br><br>Input:<br>922,000<br>Output:<br>128,000 | 1,050,000<br><br>Input:<br>922,000<br>Output:<br>128,000 | 1,050,000<br><br>Input:<br>922,000<br>Output:<br>128,000 | 1,050,000<br><br>Input:<br>922,000<br>Output:<br>128,000 | 400,000 <br><br>Input: 272,000 <br> Output: 128,000 <br>| 400,000 <br><br>Input: 272,000 <br> Output: 128,000 <br>| 1,050,000<br><br>Input:<br>922,000<br>Output:<br>128,000 | 1,050,000 <br><br>Input:<br>922,000<br>Output:<br>128,000  | 400,000 <br><br>Input: 272,000 <br> Output: 128,000  | 400,000 <br><br>Input: 272,000 <br> Output: 128,000 | 400,000 <br><br>Input: 272,000 <br> Output: 128,000 | 400,000 <br><br>Input: 272,000 <br> Output: 128,000 | 400,000 <br><br>Input: 272,000 <br> Output: 128,000 | 128,000 <br><br>Input: 111,616 <br> Output: 16,384 | 400,000 <br><br>Input: 272,000 <br> Output: 128,000 | 400,000 <br><br>Input: 272,000 <br> Output: 128,000 | 400,000 <br><br>Input: 272,000 <br> Output: 128,000 | 400,000 <br><br>Input: 272,000 <br> Output: 128,000 | 400,000 <br><br>Input: 272,000 <br> Output: 128,000 | 400,000 <br><br> Input: 272,000 <br> Output: 128,000 |  400,000 <br><br> Input: 272,000 <br> Output: 128,000 |
| **[Reasoning effort](#reasoning-effort)**<sup>7</sup> | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅  | ✅ | ✅ | ✅ | ✅| ✅<sup>6</sup> | ✅<sup>4</sup> | ✅  | ✅  | ✅  | ✅<sup>5</sup>| ✅| ✅| ✅|✅|
| **[Image input](./gpt-with-vision.md)** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅| ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Chat Completions API | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | - | ✅ | - | - | ✅ | - | ✅| ✅ | - | - | - | - | ✅ | ✅ | ✅ |
| Responses API | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅| ✅|  ✅  | ✅  | ✅ |
| Functions/Tools | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅  | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |✅ |
| Parallel Tool Calls<sup>1</sup> | ✅ | ✅ | ✅ | ✅| ✅ | ✅ | - | ✅ |✅| ✅| ✅ | ✅  | ✅ | ✅ | ✅ | ✅ |- | ✅ | ✅ | ✅ | ✅ |
| `max_completion_tokens` <sup>2</sup> | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | - | ✅ | -| - | ✅ | - | ✅ | ✅ | - | - | -  | - |  ✅ | ✅ | ✅ |
| System Messages <sup>3</sup> | ✅ | ✅ | ✅ | ✅| ✅ | ✅ | ✅ | ✅ |✅ | ✅ | ✅ | ✅  | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅| ✅ |
| [Reasoning summary](#reasoning-summary) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |✅ |✅ | ✅ | ✅  | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| [Persisted reasoning](#preserve-reasoning-across-calls)<sup>8</sup> | ✅ | ✅ | ✅ | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| Streaming | ✅ | ✅ | ✅ | ✅  | ✅ | ✅ | ✅  | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |- | ✅ | ✅ | ✅ | ✅ |


<sup>1</sup> Parallel tool calls are not supported when `reasoning_effort` is set to `minimal`<br><br>
<sup>2</sup> Reasoning models will only work with the `max_completion_tokens` parameter when using the Chat Completions API. Use `max_output_tokens` with the Responses API. <br><br>
<sup>3</sup> The latest reasoning models support system messages to make migration easier. You should not use both a developer message and a system message in the same API request.<br><br>
<sup>4</sup> `gpt-5.1` `reasoning_effort` defaults to `none`. When upgrading from previous reasoning models to `gpt-5.1` keep in mind that you may need to update your code to explicitly pass a reasoning_effort level if you want reasoning_effort to occur.<br><br>
<sup>5</sup> `gpt-5-pro` only supports `reasoning_effort` `high`, this is the default value even when not explicitly passed to the model.<br><br>
<sup>6</sup> `gpt-5.1-codex-max` adds support for a new `reasoning_effort` level of `xhigh` which is the highest level that reasoning effort can be set to.<br><br>
<sup>7</sup> `gpt-5.6`, `gpt-5.5`, `gpt-5.4`, `gpt-5.2`, `gpt-5.1`, `gpt-5.1-codex`, `gpt-5.1-codex-max`, and `gpt-5.1-codex-mini` support `'None'` as a value for the `reasoning_effort` parameter. To use these models to generate responses without reasoning, set `reasoning_effort='None'`. This setting can increase speed.<br><br>
<sup>8</sup> The `gpt-5.6` models support `all_turns` for the `reasoning.context` parameter and use it by default. Earlier reasoning models support only `auto` and `current_turn`.

### NEW GPT-5 reasoning features

| Feature | Description |
|----|----|
|`reasoning_effort` | `max` is only supported with `gpt-5.6` and Responses API <br> `xhigh` is only supported with `gpt-5.6`, `gpt-5.5`, `gpt-5.4`, and `gpt-5.1-codex-max` <br> `minimal` is only supported with the original GPT-5 reasoning models. `minimal` isn't supported with `gpt-5.1` or greater <sup>*</sup> <br><br> **Options**: `none`, `minimal`, `low`, `medium`, `high`, `xhigh` |
|`verbosity` | A new parameter providing more granular control over how concise the model's output will be.<br><br>**Options:** `low`, `medium`, `high`. |
| [`reasoning.context`](#preserve-reasoning-across-calls) | Controls which available reasoning items the model renders into its next context. `all_turns` is only supported with `gpt-5.6`, which uses it by default.<br><br>**Options:** `auto`, `current_turn`, `all_turns`. |
| [`reasoning.mode`](#reasoning-mode) | Selects standard or pro execution for `gpt-5.6` with the Responses API. Pro mode performs more model work on a request before returning a single answer, which increases latency and token usage. Azure OpenAI uses `standard` as the default.<br><br>**Options:** `standard`, `pro`. |
| `preamble` | GPT-5 series reasoning models have the ability to spend extra time *"thinking"* before executing a function/tool call.<br><br> When this planning occurs the model can provide insight into the planning steps in the model response via a new object called the `preamble` object.<br><br> Generation of preambles in the model response is not guaranteed though you can encourage the model by using the `instructions` parameter and passing content like "You MUST plan extensively before each function call. ALWAYS output your plan to the user before calling any function"|
| **allowed tools** | You can specify multiple tools under `tool_choice` instead of just one.  |
| **custom tool type** | Enables raw text (non-json) outputs |
| [`lark_tool`](#python-lark) | Allows you to use some of the capabilities of [Python lark](https://github.com/lark-parser/lark) for more flexible constraining of model responses |

<sup>*</sup> `gpt-5-codex` also does not support `reasoning_effort` `minimal`.

# [O-Series Reasoning Models](#tab/o-series)

| **Feature**  | **codex-mini**, **2025-05-16**  | **o3-pro**, **2025-06-10**   | **o4-mini**, **2025-04-16**  | **o3**, **2025-04-16** | **o3-mini**, **2025-01-31**  |**o1**, **2024-12-17**   |  
|:-------------------|:--------------------------:|:------:|:--------|:-----:|:-------:|:--------------------------:|
| **[Developer Messages](#developer-messages)** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **[Structured Outputs](./structured-outputs.md)** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **[Context Window](../../foundry-models/concepts/models-sold-directly-by-azure.md#o-series-models)** |  Input: 200,000 <br> Output: 100,000 | Input: 200,000 <br> Output: 100,000 | Input: 200,000 <br> Output: 100,000 | Input: 200,000 <br> Output: 100,000 | Input: 200,000 <br> Output: 100,000 | Input: 200,000 <br> Output: 100,000  | 
| **[Reasoning effort](#reasoning-effort)** | ✅| ✅| ✅| ✅ |✅ | ✅ |
| **[Image input](./gpt-with-vision.md)** | ✅ | ✅ | ✅ | ✅ | - | ✅ |
| Chat Completions API | - | - | ✅ | ✅ | ✅ | ✅ |
| Responses API | ✅  | ✅  | ✅ | ✅  | ✅ | ✅ |
| Functions/Tools | ✅ | ✅ |✅ | ✅ | ✅  | ✅  |
| Parallel Tool Calls | - | - | - | - | -  | -  |
| `max_completion_tokens` <sup>1</sup> |  ✅ | ✅ | ✅ | ✅ |✅ |✅ |
| System Messages <sup>2</sup> | ✅ | ✅| ✅ | ✅ | ✅ | ✅ |
| [Reasoning summary](#reasoning-summary) |  ✅ | - | ✅ | ✅ | -  | -  |
| [Persisted reasoning](#preserve-reasoning-across-calls) | - | - | - | - | - | - |
| Streaming <sup>3</sup>  | ✅ | - | ✅ | ✅| ✅ | - |

<sup>1</sup> Reasoning models will only work with the `max_completion_tokens` parameter when using the Chat Completions API. Use `max_output_tokens` with the Responses API.<br><br>
<sup>2</sup> The latest o<sup>&#42;</sup> series model support system messages to make migration easier. When you use a system message with `o4-mini`, `o3`, `o3-mini`, and `o1` it will be treated as a developer message. You should not use both a developer message and a system message in the same API request.
<sup>3</sup> Streaming for `o3` is limited access only.

---

> [!NOTE]
> - To avoid timeouts [background mode](./responses.md#background-tasks) is recommended for `o3-pro`.
> - `o3-pro` does not currently support image generation.

### Not Supported

The following are currently unsupported with reasoning models:

- `temperature`, `top_p`, `presence_penalty`, `frequency_penalty`, `logprobs`, `top_logprobs`, `logit_bias`, `max_tokens`

## Prompting guidance

Reasoning models work best when you give them a clear goal, firm constraints, and an explicit output contract. Unlike non-reasoning models, they don't need you to prescribe every intermediate step.

- State the task, the constraints, and the output format you expect.
- Treat `reasoning_effort` as a tuning knob rather than the first thing you reach for when quality drops.
- For agentic or research-heavy workflows, define what counts as done and how the model should verify its own work.

## Markdown output

By default the `o3-mini` and `o1` models will not attempt to produce output that includes markdown formatting. A common use case where this behavior is undesirable is when you want the model to output code contained within a markdown code block. When the model generates output without markdown formatting you lose features like syntax highlighting, and copyable code blocks in interactive playground experiences. To override this new default behavior and encourage markdown inclusion in model responses, add the string `Formatting re-enabled` to the beginning of your developer message.

Adding `Formatting re-enabled` to the beginning of your developer message does not guarantee that the model will include markdown formatting in its response, it only increases the likelihood. We have found from internal testing that `Formatting re-enabled` is less effective by itself with the `o1` model than with `o3-mini`.

To improve the performance of `Formatting re-enabled` you can further augment the beginning of the developer message which will often result in the desired output. Rather than just adding `Formatting re-enabled` to the beginning of your developer message, you can experiment with adding a more descriptive initial instruction like one of the examples below:

- `Formatting re-enabled - please enclose code blocks with appropriate markdown tags.`
- `Formatting re-enabled - code output should be wrapped in markdown.`

Depending on your expected output you may need to customize your initial developer message further to target your specific use case.
