---
title: "Monitor model router in Microsoft Foundry"
description: "Learn how to inspect preview per-request routing metadata for model router, including routing attempts, status, and latency, in Microsoft Foundry."
author: PatrickFarley
ms.author: pafarley
manager: mcleans
ms.date: 09/01/2026
ms.service: microsoft-foundry
ms.subservice: foundry-model-inference
ms.topic: how-to
ai-usage: ai-assisted
---

# Monitor model router in Microsoft Foundry

Observability helps you understand how model router handles requests, verify routing behavior, and investigate latency, errors, and fallback. Request-level signals complement aggregate metrics and logs, giving developers and operators context to evaluate application performance.

This article covers the per-request routing metadata preview for the Chat Completions API. The metadata identifies the serving model and describes routing attempts for an individual request. For aggregate metrics and logs, see [Monitor model deployments](../../foundry-models/how-to/monitor-models.md).

## Prerequisites

- Python 3.9 or later.
- The `openai>=1.75.0` and `python-dotenv` packages. Install them by running `pip install "openai>=1.75.0" python-dotenv`.
- A model router deployment that you can access through an Azure OpenAI endpoint.
- The endpoint and API key for your Azure OpenAI resource. The complete sample reads them from the `AZURE_OPENAI_ENDPOINT` and `AZURE_OPENAI_API_KEY` environment variables.
- Azure OpenAI API version `2024-10-21`.

## Enable per-request routing metadata

After your application reads the endpoint and API key into `endpoint` and `api_key`, create the client with the preview feature header:

:::code language="python" source="~/foundry-samples-main/samples/python/foundry-models/model-router/model-router-chat-completions-observability.py" id="response_observability_enable":::

The `Foundry-Features: ModelRouterControls=V1Preview` header requests per-request routing metadata. Because this feature is in preview, the metadata presence and response schema can vary by request and service version.

## Send a Chat Completions request

Use the model router deployment name to send a request. The response includes the completion and, when available, the per-request routing metadata:

```python
response = client.chat.completions.create(
   model=deployment,
   messages=[
      {"role": "system", "content": "You are a helpful assistant."},
      {
         "role": "user",
         "content": "In one sentence, name the most popular tourist destination in Seattle.",
      },
   ],
)
```

## Understand routing metadata

The following `model_selection_details` fragment illustrates a request with two ordered model attempts:

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

## Extract routing and fallback information

After the Chat Completions request returns `response`, inspect the serving model and model selection details:

:::code language="python" source="~/foundry-samples-main/samples/python/foundry-models/model-router/model-router-chat-completions-observability.py" id="response_observability_extract":::

Ordered attempts can reveal automatic fallback for an individual request. In the example response, the failed attempt followed by a successful attempt is evidence of fallback for that request. Requests don't always include multiple attempts, so don't expect fallback on every request.

For complete application setup and runnable examples, see the [Foundry Model Router samples](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/foundry-models/model-router).

## Interpret the results

The following output shows the response and routing metadata for an example request:

```text
--- Chat Completions Response ---
Response:Pike Place Market is Seattle's most popular tourist destination.
Usage: 29 prompt + 278 completion = 307 total tokens

Routed to model: gpt-5-mini-2025-08-07
--- Model Selection Details ---
Routing mode: balanced
Routing decision 1 (latency: 19 ms)
   Attempt 1: grok-4-1-fast-reasoning - HTTP 404 (failed)
      Error: NotFound - The request failed with HTTP status code 404 (NotFound).
   Attempt 2: gpt-5-mini - HTTP 200 (selected)
```

- If `model_selection_details` is absent, the sample reports that no model selection details were returned. Don't infer routing details that aren't present.
- If `routing_trace` is empty, the sample reports that no routing trace was returned.
- An attempt can omit `error`. The extraction code prints an error only when the response includes one.
- Model names, HTTP statuses, attempt counts, and reported latency can vary by request and service version.
- `response.model` identifies the serving model for the demonstrated request.

## Related content

- [Use model router](model-router.md)
- [How model router works](../concepts/model-router-how-it-works.md)
- [Monitor model deployments](../../foundry-models/how-to/monitor-models.md)
