---
ms.service: microsoft-foundry
ms.subservice: foundry-openai
ms.topic: how-to
ms.date: 08/06/2026
author: alvinashcraft
ms.author: aashcraft
zone_pivot_groups: structured-outputs
ai-usage: ai-assisted
ms.custom: classic-and-new, doc-kit-assisted
---

## Getting started

`response_format` is set to `json_schema` with `strict: true` set.

```bash
curl -X POST  https://YOUR_RESOURCE_NAME.openai.azure.com/openai/v1/chat/completions \
  -H "api-key: $AZURE_OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
    -d '{
        "model": "YOUR_MODEL_DEPLOYMENT_NAME",
        "messages": [
                {"role": "system", "content": "Extract the event information."},
                {"role": "user", "content": "Alice and Bob are going to a science fair on Friday."}
            ],
            "response_format": {
                "type": "json_schema",
                "json_schema": {
                    "name": "CalendarEventResponse",
                    "strict": true,
                    "schema": {
                        "type": "object",
                        "properties": {
                            "name": {
                              "type": "string"
                            },
                            "date": {
                                "type": "string"
                            },
                            "participants": {
                                "type": "array",
                                "items": {
                                    "type": "string"
                                }
                            }
                        },
                        "required": [
                            "name",
                            "date",
                            "participants"
                        ],
                        "additionalProperties": false
                    }
                }
          }
  }'
```

Output:

```json
{
  "id": "chatcmpl-A1HKsHAe2hH9MEooYslRn9UmEwsag",
  "object": "chat.completion",
  "created": 1724868330,
  "model": "gpt-4o-2024-08-06",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "{\n  \"name\": \"Science Fair\",\n  \"date\": \"Friday\",\n  \"participants\": [\"Alice\", \"Bob\"]\n}"
      },
      "logprobs": null,
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 33,
    "completion_tokens": 27,
    "total_tokens": 60
  },
  "system_fingerprint": "fp_1c2eaec9fe"
}

```

## Use structured outputs with the Responses API

For the Responses API, define the JSON Schema under `text.format`. Set `type`, `name`, `schema`, and `strict` as sibling properties of `format`. Before you run the request, set `AZURE_OPENAI_AUTH_TOKEN` to a Microsoft Entra ID access token.

```bash
curl -X POST https://YOUR_RESOURCE_NAME.openai.azure.com/openai/v1/responses \
  -H "Authorization: Bearer $AZURE_OPENAI_AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-5-mini",
    "input": "Extract the event information from: Alice and Bob are going to a science fair on Friday.",
    "text": {
      "format": {
        "type": "json_schema",
        "name": "CalendarEventResponse",
        "schema": {
          "type": "object",
          "properties": {
            "name": {"type": "string"},
            "date": {"type": "string"},
            "participants": {
              "type": "array",
              "items": {"type": "string"}
            }
          },
          "required": ["name", "date", "participants"],
          "additionalProperties": false
        },
        "strict": true
      }
    }
  }'
```

The `output_text` content contains:

```json
{
  "name": "Science Fair",
  "date": "Friday",
  "participants": ["Alice", "Bob"]
}
```

## Function calling with structured outputs

```bash
curl -X POST  https://YOUR_RESOURCE_NAME.openai.azure.com/openai/v1/chat/completions \
  -H "api-key: $AZURE_OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
  "model": "YOUR_MODEL_DEPLOYMENT_NAME",
  "messages": [
    {
      "role": "system",
      "content": "You are a helpful assistant. The current date is August 6, 2024. You help users query for the data they are looking for by calling the query function."
    },
    {
      "role": "user",
      "content": "look up all my orders in may of last year that were fulfilled but not delivered on time"
    }
  ],
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "query",
        "description": "Execute a query.",
        "strict": true,
        "parameters": {
          "type": "object",
          "properties": {
            "table_name": {
              "type": "string",
              "enum": ["orders"]
            },
            "columns": {
              "type": "array",
              "items": {
                "type": "string",
                "enum": [
                  "id",
                  "status",
                  "expected_delivery_date",
                  "delivered_at",
                  "shipped_at",
                  "ordered_at",
                  "canceled_at"
                ]
              }
            },
            "conditions": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": {
                  "column": {
                    "type": "string"
                  },
                  "operator": {
                    "type": "string",
                    "enum": ["=", ">", "<", ">=", "<=", "!="]
                  },
                  "value": {
                    "anyOf": [
                      {
                        "type": "string"
                      },
                      {
                        "type": "number"
                      },
                      {
                        "type": "object",
                        "properties": {
                          "column_name": {
                            "type": "string"
                          }
                        },
                        "required": ["column_name"],
                        "additionalProperties": false
                      }
                    ]
                  }
                },
                "required": ["column", "operator", "value"],
                "additionalProperties": false
              }
            },
            "order_by": {
              "type": "string",
              "enum": ["asc", "desc"]
            }
          },
          "required": ["table_name", "columns", "conditions", "order_by"],
          "additionalProperties": false
        }
      }
    }
  ]
}'
```
