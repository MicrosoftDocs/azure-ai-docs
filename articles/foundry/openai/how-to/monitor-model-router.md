---
title: "Monitor model router in Microsoft Foundry"
description: "Learn how to inspect preview model router metadata for routing attempts, fallback, latency, and Chat Completions session affinity in Microsoft Foundry."
author: PatrickFarley
ms.author: pafarley
manager: mcleans
ms.date: 09/15/2026
ms.service: microsoft-foundry
ms.subservice: foundry-model-inference
ms.topic: how-to
ai-usage: ai-assisted
ms.custom: update-code1
---

# Monitor model router in Microsoft Foundry

Model router observability helps you verify routing behavior and investigate latency, errors, fallback, and session affinity for individual requests. The preview metadata includes a `routing_trace` that describes model attempts and a `session_affinity` object that describes whether model router initialized, retained, or switched a model association.

Both signals appear in the optional `model_selection_details` response object for the Chat Completions API. These request-level signals complement aggregate metrics and logs. For aggregate monitoring, see [Monitor model deployments](../../foundry-models/how-to/monitor-models.md).

## Prerequisites

- Python 3.9 or later.
- The `openai>=1.75.0` and `python-dotenv` packages. Install them by running `pip install "openai>=1.75.0" python-dotenv`.
- A model router deployment that you can access through an Azure OpenAI endpoint.
- The endpoint and API key for your Azure OpenAI resource. The complete sample reads them from the `AZURE_OPENAI_ENDPOINT` and `AZURE_OPENAI_API_KEY` environment variables.
- Azure OpenAI API version `2024-10-21`.

## Enable request-level metadata

After your application reads the endpoint and API key into `endpoint` and `api_key`, create the client with the preview feature header:

:::code language="python" source="~/foundry-samples-main/samples/python/foundry-models/model-router/model-router-chat-completions-observability.py" id="response_observability_enable":::

The `Foundry-Features: ModelRouterControls=V1Preview` header requests per-request routing metadata. Because this feature is in preview, the metadata presence and response schema can vary by request and service version.

- Reference: [`AzureOpenAI` class](https://github.com/openai/openai-python/blob/main/src/openai/lib/azure.py)

## Understand the response envelope

Use the top-level `model` field and the optional `model_selection_details` object together to understand how the model router handled a request:

| Field | What it describes |
| --- | --- |
| `model` | The underlying model that served the response. |
| `model_selection_details.model_router_details.mode` | The routing mode used for the request. |
| `model_selection_details.model_router_details.routing_trace` | Ordered model attempts, routing latency, status, and optional errors. |
| `model_selection_details.model_router_details.session_affinity` | The affinity mode, session ID source, and final association decision. |

The `model_selection_details` envelope and each child field are optional during preview. Parse fields defensively, and tolerate additional fields in future service versions. Don't infer routing or affinity details when the corresponding field is absent.

## Inspect routing attempts and fallback

Send a Chat Completions request through the model router deployment. The response includes the completion and, when available, routing metadata:

:::code language="python" source="~/foundry-samples-main/samples/python/foundry-models/model-router/model-router-chat-completions-observability.py" id="response_observability_request":::

- Reference: [Chat Completions API](https://platform.openai.com/docs/api-reference/chat/create)

### Review the routing trace

The following illustrative `model_selection_details` fragment contains two ordered model attempts:

```json
{
   "model_selection_details": {
      "model_router_details": {
         "mode": "balanced",
         "routing_trace": [
            {
               "latency_ms": 19,
               "attempts": [
                  {
                     "model": "example-model-a",
                     "result": {
                        "status": 404,
                        "error": {
                           "code": "NotFound",
                           "message": "The request failed."
                        }
                     }
                  },
                  {
                     "model": "example-model-b",
                     "result": {
                        "status": 200
                     }
                  }
               ]
            }
         ]
      }
   }
}
```

- `mode` is the routing mode returned for the request.
- `routing_trace` contains the routing entries returned for the request.
- `latency_ms` is the latency reported for a routing-trace entry.
- `attempts` lists model attempts in order.
- Each attempt contains a model and an HTTP status in `result.status`.
- A failed attempt can include an optional `error` with a code and message.

### Parse routing and fallback information

After the Chat Completions request returns `response`, inspect the serving model and model selection details:

:::code language="python" source="~/foundry-samples-main/samples/python/foundry-models/model-router/model-router-chat-completions-observability.py" id="response_observability_extract":::

The parsing code produces output similar to the following example for the illustrative routing trace:

```output
--- Chat Completions Response ---
Response:Pike Place Market is Seattle's most popular tourist destination.
Usage: 29 prompt + 278 completion = 307 total tokens

Routed to model: example-model-b
--- Model Selection Details ---
Routing mode: balanced
Routing decision 1 (latency: 19 ms)
   Attempt 1: example-model-a - HTTP 404 (failed)
      Error: NotFound - The request failed.
   Attempt 2: example-model-b - HTTP 200 (selected)
```

Ordered attempts can reveal automatic fallback for an individual request. In this example, the failed attempt followed by a successful attempt is evidence of fallback. Requests don't always include multiple attempts, and an attempt can omit `error`. Model names, HTTP statuses, attempt counts, and latency can vary by request and service version.

## Interpret session affinity metadata

Session affinity asks the model router to try the same eligible model for related Chat Completions requests. Configure an opaque, application-owned session ID and use the same value across conversation turns:

:::code language="python" source="~/foundry-samples-main/samples/python/foundry-models/model-router/model-router-chat-completions-session-affinity.py" id="session_affinity_enable":::

For session ID validation, expiration, and disable behavior, see [Keep Chat Completions requests on the same model](model-router.md#keep-chat-completions-requests-on-the-same-model-preview).

- Reference: [`AzureOpenAI` class](https://github.com/openai/openai-python/blob/main/src/openai/lib/azure.py)

### Send related conversation turns

Send the first request, append its response and a new user message to the conversation history, and send the next request with the same session affinity configuration:

:::code language="python" source="~/foundry-samples-main/samples/python/foundry-models/model-router/model-router-chat-completions-session-affinity.py" id="session_affinity_turns":::

- Reference: [Chat Completions API](https://platform.openai.com/docs/api-reference/chat/create)

### Review session affinity metadata

The first successful request for a new session ID typically returns an `initialize` decision. The following illustrative response shows that result:

```json
{
   "model": "example-model-a",
   "model_selection_details": {
      "model_router_details": {
         "mode": "balanced",
         "session_affinity": {
            "mode": "sticky",
            "source": "session_id_payload",
            "decision": "initialize"
         }
      }
   }
}
```

Interpret the feature-specific fields as follows:

| Field | Value | Meaning |
| --- | --- | --- |
| `mode` | `sticky` | Model router attempts the associated eligible model first. |
| `source` | `session_id_payload` or `session_id_header` | The request body or header supplied the session ID. The response doesn't return the identifier. |
| `decision` | `initialize` | No previous association was available, and the initially selected model served the response. |
| `decision` | `retain` | The associated model served the response. |
| `decision` | `switch` | A different model served because of eligibility or fallback. |

### Parse the affinity decision

Inspect the optional `session_affinity` object for each response:

:::code language="python" source="~/foundry-samples-main/samples/python/foundry-models/model-router/model-router-chat-completions-session-affinity.py" id="session_affinity_extract":::

A typical two-turn run produces output similar to the following example:

```output
--- First turn ---
Serving model: example-model-a
Routing mode: balanced
Affinity mode: sticky
Affinity source: session_id_payload
Affinity decision: initialize
Response:
<first-response>

--- Second turn ---
Serving model: example-model-a
Routing mode: balanced
Affinity mode: sticky
Affinity source: session_id_payload
Affinity decision: retain
Response:
<second-response>
```

If affinity lookup or persistence isn't available, inference continues through normal routing and the response omits the complete `session_affinity` object. Don't infer an affinity decision when the object or `decision` field is absent.

### Diagnose an affinity switch

The `session_affinity` and `routing_trace` signals complement each other and can appear in the same response. When `decision` is `switch`, check the top-level `model` field to identify the serving model and `routing_trace` to understand the attempts or fallback that caused the change:

```json
{
   "model": "example-model-b",
   "model_selection_details": {
      "model_router_details": {
         "mode": "balanced",
         "session_affinity": {
            "mode": "sticky",
            "source": "session_id_payload",
            "decision": "switch"
         },
         "routing_trace": [
            {
               "latency_ms": 51,
               "attempts": [
                  {
                     "model": "example-model-a",
                     "result": { "status": 429 }
                  },
                  {
                     "model": "example-model-b",
                     "result": { "status": 200 }
                  }
               ]
            }
         ]
      }
   }
}
```

In this example, the associated model returns a retryable response before fallback selects another model. Session affinity works on a best-effort basis: it doesn't prevent normal fallback or guarantee that related requests use the same model.

For complete application setup and runnable examples, see the [Foundry Model Router samples](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/foundry-models/model-router).

## Related content

- [Use model router](model-router.md)
- [How model router works](../concepts/model-router-how-it-works.md)
- [Monitor model deployments](../../foundry-models/how-to/monitor-models.md)
