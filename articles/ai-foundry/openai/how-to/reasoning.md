---
title: Azure OpenAI reasoning models - GPT-5 series, o3-mini, o1, o1-mini
titleSuffix: Azure OpenAI
description: Learn how to use Azure OpenAI's advanced GPT-5 series, o3-mini, o1, & o1-mini reasoning models 
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: how-to
ms.date: 01/14/2026
author: mrbullwinkle    
ms.author: mbullwin
monikerRange: 'foundry-classic || foundry'
---


# Azure OpenAI reasoning models

Azure OpenAI reasoning models are designed to tackle reasoning and problem-solving tasks with increased focus and capability. These models spend more time processing and understanding the user's request, making them exceptionally strong in areas like science, coding, and math compared to previous iterations.

**Key capabilities of reasoning models:**

- Complex Code Generation: Capable of generating algorithms and handling advanced coding tasks to support developers.
- Advanced Problem Solving: Ideal for comprehensive brainstorming sessions and addressing multifaceted challenges.
- Complex Document Comparison: Perfect for analyzing contracts, case files, or legal documents to identify subtle differences.
- Instruction Following and Workflow Management: Particularly effective for managing workflows requiring shorter contexts.

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
    "https://cognitiveservices.azure.com/.default");

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

If you're new to using Microsoft Entra ID for authentication see [How to configure Azure OpenAI in Microsoft Foundry Models with Microsoft Entra ID authentication](../how-to/managed-identity.md).

```python
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

client = OpenAI(  
  base_url = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",  
  api_key=token_provider,
)

response = client.chat.completions.create(
    model="o1-new", # replace with your model deployment name 
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
    model="gpt-5-mini", # replace with the model deployment name of your o1 deployment.
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

## Reasoning effort

> [!NOTE]
> Reasoning models have `reasoning_tokens` as part of `completion_tokens_details` in the model response. These are hidden tokens that aren't returned as part of the message response content but are used by the model to help generate a final answer to your request. `reasoning_effort` can be set to `low`, `medium`, or `high` for all reasoning models except `o1-mini`. GPT-5 reasoning models support a new `reasoning_effort` setting of `minimal`. The higher the effort setting, the longer the model will spend processing the request, which will generally result in a larger number of `reasoning_tokens`.

### Developer messages

Functionally developer messages ` "role": "developer"` are the same as system messages.

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
    "https://cognitiveservices.azure.com/.default");

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

If you're new to using Microsoft Entra ID for authentication see [How to configure Azure OpenAI with Microsoft Entra ID authentication](../how-to/managed-identity.md).

```python
jupy
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
          {"role": "system", "content": "You are a helpful assistant."},
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
        "content": "Here’s a practical, beginner‑friendly checklist to guide you through writing your first Python API, from idea to production.\n\n1) Clarify goals and constraints\n- Who will use it (internal team, public), what problems it solves, expected traffic, latency requirements.\n- Resources you’ll expose (users, orders, etc.) and core operations.\n- Non‑functional needs: security, compliance, uptime, scalability.\n\n2) Choose your API style\n- REST (most common for CRUD and simple integrations).\n- GraphQL (flexible queries, more complex to secure/monitor).\n- gRPC (high‑performance, strongly typed, good for service‑to‑service).\n- For a first API, REST + JSON is usually best.\n\n3) Design the contract first\n- Draft an OpenAPI/Swagger spec: endpoints, request/response schemas, status codes, error model.\n- Decide naming conventions, pagination, filtering, sorting.\n- Define consistent time/date format (ISO‑8601, UTC), ID format, and field casing.\n- Plan versioning strategy (e.g., /v1) and deprecation policy.\n\n4) Plan security and auth\n- Pick auth: API keys for simple internal use; OAuth2/JWT for user auth; mTLS for service‑to‑service.\n- CORS policy for browsers; HTTPS everywhere; security headers.\n- Validate all inputs; avoid leaking stack traces; define rate limits and quotas.\n\n5) Pick your Python stack\n- Frameworks: FastAPI (great typing, validation, auto docs), Flask (minimal), Django REST Framework (batteries included).\n- ASGI/WSGI server: Uvicorn or Gunicorn.\n- Data layer: PostgreSQL + SQLAlchemy/Django ORM; migrations with Alembic/Django migrations.\n- Caching: Redis (optional).\n- Background jobs: Celery/RQ (if needed).\n\n6) Set up the project\n- Create a virtual environment; choose dependency management (pip, Poetry).\n- Establish project structure (app, api, models, services, tests).\n- Add linting/formatting/type checks: black, isort, flake8, mypy; pre‑commit hooks.\n- Configuration via environment variables; secrets via a manager (not in code).\n\n7) Implement core functionality\n- Build endpoints that match your spec; keep business logic in a service layer, not in route handlers.\n- Schema validation (Pydantic with FastAPI, Marshmallow for Flask).\n- Consistent responses and errors; use clear status codes (201 create, 204 no content, 400/404/409/422, 500).\n- Pagination and filtering; idempotency for certain POST operations; ETags/conditional requests if useful.\n\n8) Error handling and an error model\n- Define a standard error body (code, message, details, correlation_id).\n- Log errors with context; don’t expose internal details to clients.\n\n9) Testing strategy\n- Unit tests for services/validators.\n- Integration tests for endpoints (pytest + httpx/requests) with a test database.\n- Contract tests to assert the API matches the OpenAPI spec.\n- Mock external services; measure coverage and focus on critical paths.\n\n10) Documentation and developer experience\n- Auto‑generated docs (FastAPI provides Swagger/ReDoc).\n- Write examples for each endpoint; onboarding and usage notes.\n- Keep a changelog and release notes.\n\n11) Observability and reliability\n- Structured logging (JSON), include request IDs/correlation IDs.\n- Metrics (requests, latency, error rates), health/readiness endpoints.\n- Tracing (OpenTelemetry) if you have multiple services.\n- Error reporting (Sentry or similar).\n\n12) Deployment and operations\n- Containerize with Docker; follow 12‑factor app principles.\n- CI/CD pipeline: run tests, build image, deploy, run migrations.\n- Choose hosting (Render, Fly.io, Railway, Heroku, AWS/GCP/Azure).\n- Configure scaling, connection pools, and timeouts; use a reverse proxy if needed.\n\n13) Performance and data concerns\n- Index your database; avoid N+1 queries; use connection pooling.\n- Load test key endpoints; profile hotspots.\n- Caching strategies where appropriate; consider async I/O for high‑concurrency workloads.\n\n14) Versioning and lifecycle management\n- Keep backward compatibility for minor changes; add fields rather than changing semantics.\n- Communicate deprecations; sunset old versions with a timeline.\n\n15) Governance, compliance, and safety\n- Handle PII correctly; data retention and audit logs if required.\n- Least‑privilege DB access; rotate secrets; review third‑party dependencies.\n\nBeginner‑friendly defaults\n- FastAPI + Pydantic + Uvicorn\n- PostgreSQL + SQLAlchemy + Alembic\n- pytest + httpx + coverage\n- black, isort, flake8, mypy, pre‑commit\n- Docker + simple CI (GitHub Actions) + a managed host\n\nCommon pitfalls to avoid\n- Inconsistent status codes or error formats.\n- Weak input validation and missing authentication.\n- Business logic inside route handlers (hard to test/maintain).\n- No migrations or tests; no logging/metrics.\n- Ignoring pagination and timezones; returning unbounded lists.\n\nIf you share whether it’s public vs internal, expected traffic, and preferred framework, I can tailor this to a concrete starter plan and recommended tools.",
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
    "https://cognitiveservices.azure.com/.default");

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
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
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
          "text": "Neural text degeneration refers to the ways language models produce low-quality, repetitive, or vacuous text, especially when generating long outputs. It’s “curious” because models trained to imitate fluent text can still spiral into unnatural patterns. Key aspects:\n\n- Repetition and loops: The model repeats phrases or sentences (“I’m sorry, but...”), often due to high-confidence tokens reinforcing themselves.\n- Loss of specificity: Vague, generic, agreeable text that avoids concrete details.\n- Drift and contradiction: The output gradually departs from context or contradicts itself over long spans.\n- Exposure bias: During training, models see gold-standard prefixes; at inference, they must condition on their own imperfect outputs, compounding errors.\n- Likelihood vs. quality mismatch: Maximizing token-level likelihood doesn’t align with human preferences for diversity, coherence, or factuality.\n- Token over-optimization: Frequent, safe tokens get overused; certain phrases become attractors.\n- Entropy collapse: With greedy or low-temperature decoding, the distribution narrows too much, causing repetitive, low-entropy text.\n- Length and beam search issues: Larger beams or long generations can favor bland, repetitive sequences (the “likelihood trap”).\n\nCommon mitigations:\n\n- Decoding strategies:\n  - Top-k, nucleus (top-p), or temperature sampling to keep sufficient entropy.\n  - Typical sampling and locally typical sampling to avoid dull but high-probability tokens.\n  - Repetition penalties, presence/frequency penalties, no-repeat n-grams.\n  - Contrastive decoding (and variants like DoLa) to filter generic continuations.\n  - Min/max length, stop sequences, and beam search with diversity/penalties.\n\n- Training and alignment:\n  - RLHF/DPO to better match human preferences for non-repetitive, helpful text.\n  - Supervised fine-tuning on high-quality, diverse data; instruction tuning.\n  - Debiasing objectives (unlikelihood training) to penalize repetition and banned patterns.\n  - Mixture-of-denoisers or latent planning to improve long-range coherence.\n\n- Architectural and planning aids:\n  - Retrieval-augmented generation to ground outputs.\n  - Tool use and structured prompting to constrain drift.\n  - Memory and planning modules, hierarchical decoding, or sentence-level control.\n\n- Prompting tips:\n  - Ask for concise answers, set token limits, and specify structure.\n  - Provide concrete constraints or content to reduce generic filler.\n  - Use “say nothing if uncertain” style instructions to avoid vacuity.\n\nRepresentative papers/terms to search:\n- Holtzman et al., “The Curious Case of Neural Text Degeneration” (2020): nucleus sampling.\n- Welleck et al., “Neural Text Degeneration with Unlikelihood Training.”\n- Li et al., “A Contrastive Framework for Decoding.”\n- Su et al., “DoLa: Decoding by Contrasting Layers.”\n- Meister et al., “Typical Decoding.”\n- Ouyang et al., “Training language models to follow instructions with human feedback.”\n\nIn short, degeneration arises from a mismatch between next-token likelihood and human preferences plus decoding choices; careful decoding, training objectives, and grounding help prevent it.",
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
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
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
          "text": "“strawberry” has 3 r’s, so the radius is 3.\nArea = πr² = π × 3² = 9π ≈ 28.27 square units.",
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
|---|---|---|
| `gpt-5.2-codex`| East US2 & Sweden Central (Global Standard) | Request access: [Limited access model application](https://aka.ms/oai/gpt5access). If you already have access to a limited access model no request is required. |
| `gpt-5.2`| [Model availability](../../foundry-models/concepts/models-sold-directly-by-azure.md#global-standard-model-availability)   | Request access: [Limited access model application](https://aka.ms/oai/gpt5access). If you already have access to a limited access model no request is required. |
`gpt-5.1-codex-max` | [Model availability](../../foundry-models/concepts/models-sold-directly-by-azure.md#global-standard-model-availability) |  Request access: [Limited access model application](https://aka.ms/oai/gpt5access). If you already have access to a limited access model no request is required.|
| `gpt-5.1`| [Model availability](../../foundry-models/concepts/models-sold-directly-by-azure.md#global-standard-model-availability)  | Request access: [Limited access model application](https://aka.ms/oai/gpt5access). If you already have access to a limited access model no request is required. |
| `gpt-5.1-chat` | [Model availability](../../foundry-models/concepts/models-sold-directly-by-azure.md#global-standard-model-availability) | No access request needed.  |
| `gpt-5.1-codex` | [Model availability](../../foundry-models/concepts/models-sold-directly-by-azure.md#global-standard-model-availability)  | Request access: [Limited access model application](https://aka.ms/oai/gpt5access). If you already have access to a limited access model no request is required. |
| `gpt-5.1-codex-mini` | [Model availability](../../foundry-models/concepts/models-sold-directly-by-azure.md#global-standard-model-availability)  | No access request needed. | 
| `gpt-5-pro` | [Model availability](../../foundry-models/concepts/models-sold-directly-by-azure.md#global-standard-model-availability)  | Request access: [Limited access model application](https://aka.ms/oai/gpt5access). If you already have access to a limited access model no request is required.   |
| `gpt-5-codex` |[Model availability](../../foundry-models/concepts/models-sold-directly-by-azure.md#global-standard-model-availability)  | Request access: [Limited access model application](https://aka.ms/oai/gpt5access). If you already have access to a limited access model no request is required.    |
| `gpt-5` | [Model availability](../../foundry-models/concepts/models-sold-directly-by-azure.md#global-standard-model-availability)   |  Request access: [Limited access model application](https://aka.ms/oai/gpt5access). If you already have access to a limited access model no request is required.     |
| `gpt-5-mini` | [Model availability](../../foundry-models/concepts/models-sold-directly-by-azure.md#global-standard-model-availability)  |  No access request needed.    |
| `gpt-5-nano` | [Model availability](../../foundry-models/concepts/models-sold-directly-by-azure.md#global-standard-model-availability)  |  No access request needed. |
| `o3-pro`  | [Model availability](../../foundry-models/concepts/models-sold-directly-by-azure.md#global-standard-model-availability)     |  Request access: [Limited access model application](https://aka.ms/oai/o3access). If you already have access to a limited access model no request is required.  |
| `codex-mini`  | [Model availability](../../foundry-models/concepts/models-sold-directly-by-azure.md#global-standard-model-availability)     | No access request needed.    |
| `o4-mini`  | [Model availability](../../foundry-models/concepts/models-sold-directly-by-azure.md#global-standard-model-availability)   | No access request needed to use the core capabilities of this model.<br><br> Request access: [o4-mini reasoning summary feature](https://aka.ms/oai/o3access)     |
| `o3` |  [Model availability](../../foundry-models/concepts/models-sold-directly-by-azure.md#global-standard-model-availability)  | Request access: [Limited access model application](https://aka.ms/oai/o3access)     |
| `o3-mini` | [Model availability](../../foundry-models/concepts/models-sold-directly-by-azure.md#global-standard-model-availability).  | Access is no longer restricted for this model.   |
|`o1` | [Model availability](../../foundry-models/concepts/models-sold-directly-by-azure.md#global-standard-model-availability).  | Access is no longer restricted for this model.  |

## API & feature support

# [GPT-5 Reasoning Models](#tab/gpt-5)

| **Feature**  | **gpt-5.2-codex** | **gpt-5.2** | **gpt-5.1-codex-max** | **gpt-5.1**, **2025-11-13** | **gpt-5.1-chat**, **2025-11-13** | **gpt-5.1-codex**, **2025-11-13** | **gpt-5.1-codex-mini**, **2025-11-13** | **gpt-5-pro**, **2025-10-06** | **gpt-5-codex**, **2025-09-011**  | **gpt-5**, **2025-08-07**  | **gpt-5-mini**, **2025-08-07**   | **gpt-5-nano**, **2025-08-07**  |
|:-------------------|:---:|:---:|:---:|:---:|:---:|:---:|:--------------------------:|:--------------------------:|:------:|:--------:|:--------:|
| **API Version** | [v1](../api-version-lifecycle.md#api-evolution) | [v1](../api-version-lifecycle.md#api-evolution) | [v1](../api-version-lifecycle.md#api-evolution) | [v1](../api-version-lifecycle.md#api-evolution) | [v1](../api-version-lifecycle.md#api-evolution) | [v1](../api-version-lifecycle.md#api-evolution) | [v1](../api-version-lifecycle.md#api-evolution) | [v1](../api-version-lifecycle.md#api-evolution) | [v1](../api-version-lifecycle.md#api-evolution) | [v1](../api-version-lifecycle.md#api-evolution) | [v1](../api-version-lifecycle.md#api-evolution) | [v1](../api-version-lifecycle.md#api-evolution) |
| **[Developer Messages](#developer-messages)** | ✅  | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |✅ |
| **[Structured Outputs](./structured-outputs.md)** | ✅ | ✅ | ✅| ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **[Context Window](../../foundry-models/concepts/models-sold-directly-by-azure.md#o-series-models)** | 400,000 <br><br>Input: 272,000 <br> Output: 128,000 | 400,000 <br><br>Input: 272,000 <br> Output: 128,000 | 400,000 <br><br>Input: 272,000 <br> Output: 128,000 | 400,000 <br><br>Input: 272,000 <br> Output: 128,000 | 128,000 <br><br>Input: 111,616 <br> Output: 16,384 | 400,000 <br><br>Input: 272,000 <br> Output: 128,000 | 400,000 <br><br>Input: 272,000 <br> Output: 128,000 | 400,000 <br><br>Input: 272,000 <br> Output: 128,000 | 400,000 <br><br>Input: 272,000 <br> Output: 128,000 | 400,000 <br><br>Input: 272,000 <br> Output: 128,000 | 400,000 <br><br> Input: 272,000 <br> Output: 128,000 |  400,000 <br><br> Input: 272,000 <br> Output: 128,000 |
| **[Reasoning effort](#reasoning-effort)**<sup>7</sup> | ✅ | ✅| ✅<sup>6</sup> | ✅<sup>4</sup> | ✅  | ✅  | ✅  | ✅<sup>5</sup>| ✅| ✅| ✅|✅|
| **[Image input](./gpt-with-vision.md)** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Chat Completions API | | ✅ | - | ✅| ✅ | - | - | - | - | ✅ | ✅ | ✅ |
| Responses API | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅| ✅|  ✅  | ✅  | ✅ |
| Functions/Tools | ✅ | ✅ | ✅  | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |✅ |
| Parallel Tool Calls<sup>1</sup> | ✅| ✅ | ✅  | ✅ | ✅ | ✅ | ✅ |- | ✅ | ✅ | ✅ | ✅ |
| `max_completion_tokens` <sup>2</sup> | - | ✅ | - | ✅ | ✅ | - | - | -  | - |  ✅ | ✅ | ✅ |
| System Messages <sup>3</sup> |✅ | ✅ | ✅  | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅| ✅ |
| [Reasoning summary](#reasoning-summary) |✅ | ✅ | ✅  | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Streaming | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |- | ✅ | ✅ | ✅ | ✅|

<sup>1</sup> Parallel tool calls are not supported when `reasoning_effort` is set to `minimal`<br><br>
<sup>2</sup> Reasoning models will only work with the `max_completion_tokens` parameter when using the Chat Completions API. Use `max_output_tokens` with the Responses API. <br><br>
<sup>3</sup> The latest reasoning models support system messages to make migration easier. You should not use both a developer message and a system message in the same API request.<br><br>
<sup>4</sup> `gpt-5.1` `reasoning_effort` defaults to `none`. When upgrading from previous reasoning models to `gpt-5.1` keep in mind that you may need to update your code to explicitly pass a reasoning_effort level if you want reasoning_effort to occur.<br><br>
<sup>5</sup> `gpt-5-pro` only supports `reasoning_effort` `high`, this is the default value even when not explicitly passed to the model.<br><br>
<sup>6</sup> `gpt-5.1-codex-max` adds support for a new `reasoning_effort` level of `xhigh` which is the highest level that reasoning effort can be set to.<br><br>
<sup>7</sup> `gpt-5.2`, `gpt-5.1`, `gpt-5.1-codex`, `gpt-5.1-codex-max`, and `gpt-5.1-codex-mini` support `'None'` as a value for the `reasoning_effort` parameter. If you wish to use these models to generate responses without reasoning, set `reasoning_effort='None'`. This setting can increase speed.

### NEW GPT-5 reasoning features

| Feature | Description |
|----|----|
|`reasoning_effort` | `xhigh` is only supported with `gpt-5.1-codex-max` <br> `minimal` is now supported with GPT-5 series reasoning models.<sup>*</sup> <br> `none` is only supported for `gpt-5.1` <br><br> **Options**: `none`, `minimal`, `low`, `medium`, `high`, `xhigh` |
|`verbosity` | A new parameter providing more granular control over how concise the model's output will be.<br><br>**Options:** `low`, `medium`, `high`. |
| `preamble` | GPT-5 series reasoning models have the ability to spend extra time *"thinking"* before executing a function/tool call.<br><br> When this planning occurs the model can provide insight into the planning steps in the model response via a new object called the `preamble` object.<br><br> Generation of preambles in the model response is not guaranteed though you can encourage the model by using the `instructions` parameter and passing content like "You MUST plan extensively before each function call. ALWAYS output your plan to the user before calling any function"|
| **allowed tools** | You can specify multiple tools under `tool_choice` instead of just one.  |
| **custom tool type** | Enables raw text (non-json) outputs |
| [`lark_tool`](#python-lark) | Allows you to use some of the capabilities of [Python lark](https://github.com/lark-parser/lark) for more flexible constraining of model responses |

<sup>*</sup> `gpt-5-codex` does not support `reasoning_effort` minimal.

For more information, we also recommend reading OpenAI's [GPT-5 prompting cookbook guide](https://cookbook.openai.com/examples/gpt-5/gpt-5_prompting_guide) and their [GPT-5 feature guide](https://platform.openai.com/docs/guides/latest-model).

# [O-Series Reasoning Models](#tab/o-series)

| **Feature**  | **codex-mini**, **2025-05-16**  | **o3-pro**, **2025-06-10**   | **o4-mini**, **2025-04-16**  | **o3**, **2025-04-16** | **o3-mini**, **2025-01-31**  |**o1**, **2024-12-17**   |  
|:-------------------|:--------------------------:|:------:|:--------|:-----:|:-------:|:--------------------------:|
| **API Version** | `2025-04-01-preview` & [v1](../api-version-lifecycle.md#api-evolution)   | `2025-04-01-preview`  & [v1](../api-version-lifecycle.md#api-evolution)  | `2025-04-01-preview` & [v1](../api-version-lifecycle.md#api-evolution)   |  `2025-04-01-preview` & [v1](../api-version-lifecycle.md#api-evolution)   |  `2025-04-01-preview` & [v1 preview](../api-version-lifecycle.md#api-evolution)   | `2025-04-01-preview` & [v1 preview](../api-version-lifecycle.md#api-evolution) |
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

## Markdown output

By default the `o3-mini` and `o1` models will not attempt to produce output that includes markdown formatting. A common use case where this behavior is undesirable is when you want the model to output code contained within a markdown code block. When the model generates output without markdown formatting you lose features like syntax highlighting, and copyable code blocks in interactive playground experiences. To override this new default behavior and encourage markdown inclusion in model responses, add the string `Formatting re-enabled` to the beginning of your developer message.

Adding `Formatting re-enabled` to the beginning of your developer message does not guarantee that the model will include markdown formatting in its response, it only increases the likelihood. We have found from internal testing that `Formatting re-enabled` is less effective by itself with the `o1` model than with `o3-mini`.

To improve the performance of `Formatting re-enabled` you can further augment the beginning of the developer message which will often result in the desired output. Rather than just adding `Formatting re-enabled` to the beginning of your developer message, you can experiment with adding a more descriptive initial instruction like one of the examples below:

- `Formatting re-enabled - please enclose code blocks with appropriate markdown tags.`
- `Formatting re-enabled - code output should be wrapped in markdown.`

Depending on your expected output you may need to customize your initial developer message further to target your specific use case.
