---
title: 'How to use structured outputs with Azure OpenAI Service'
titleSuffix: Azure OpenAI
description: Learn how to improve your model responses with structured outputs
services: cognitive-services
manager: nitinme
ms.service: azure-ai-openai
ms.topic: how-to
ms.date: 08/28/2024
author: mrbullwinkle
ms.author: mbullwin
recommendations: false
---

# Structured outputs

Structured outputs makes a model to follow a [JSON Schema](https://json-schema.org/overview/what-is-jsonschema) definition that you provide as part of your chat completions API call. This is in contrast to the older [JSON mode](./json-mode.md) feature which guaranteed valid JSON would be generated, but was unable to ensure strict adherence to the supplied schema.

## Supported models

Currently only `gpt-4o` version: `2024-08-06` supports structured outputs.

## API support

Support for JSON mode was first added in API version [`2024-08-01-preview`](https://github.com/Azure/azure-rest-api-specs/blob/main/specification/cognitiveservices/data-plane/AzureOpenAI/inference/preview/2024-08-01-preview/inference.json).

## Getting started

# [Python (Microsoft Entra ID)](#tab/python-secure)

You can use [Pydantic](https://docs.pydantic.dev/latest/) to define object schemas in Python. Depending on what version of the [OpenAI](https://pypi.org/project/openai/) and [Pydantic libraries](https://pypi.org/project/pydantic/) you are running you may need to upgrade to a newer version. These examples were tested against `openai 1.42.0` and `pydantic 2.8.2`.

```cmd
pip install openai pydantic --upgrade
```

If you new to using Microsoft Entra ID for authentication see [How to configure Azure OpenAI Service with Microsoft Entra ID authentication](./managed-identity.md).

```python
from pydantic import BaseModel
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

client = AzureOpenAI(
  azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"), 
  azure_ad_token_provider=token_provider,
  api_version="2024-08-01-preview"
)


class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: list[str]

completion = client.beta.chat.completions.parse(
    model="MODEL_DEPLOYMENT_NAME", # replace with the model deployment name of your gpt-4o 2024-08-06 deployment
    messages=[
        {"role": "system", "content": "Extract the event information."},
        {"role": "user", "content": "Alice and Bob are going to a science fair on Friday."},
    ],
    response_format=CalendarEvent,
)

event = completion.choices[0].message.parsed

print(event)
print(completion.model_dump_json(indent=2))
```

### Output

```json
name='Science Fair' date='Friday' participants=['Alice', 'Bob']
{
  "id": "chatcmpl-A1EUP2fAmL4SeB1lVMinwM7I2vcqG",
  "choices": [
    {
      "finish_reason": "stop",
      "index": 0,
      "logprobs": null,
      "message": {
        "content": "{\n  \"name\": \"Science Fair\",\n  \"date\": \"Friday\",\n  \"participants\": [\"Alice\", \"Bob\"]\n}",
        "refusal": null,
        "role": "assistant",
        "function_call": null,
        "tool_calls": [],
        "parsed": {
          "name": "Science Fair",
          "date": "Friday",
          "participants": [
            "Alice",
            "Bob"
          ]
        }
      }
    }
  ],
  "created": 1724857389,
  "model": "gpt-4o-2024-08-06",
  "object": "chat.completion",
  "service_tier": null,
  "system_fingerprint": "fp_1c2eaec9fe",
  "usage": {
    "completion_tokens": 27,
    "prompt_tokens": 32,
    "total_tokens": 59
  }
}
```

# [Python (key-based auth)](#tab/python)

You can use [Pydantic](https://docs.pydantic.dev/latest/) to define object schemas in Python. Depending on what version of the [OpenAI](https://pypi.org/project/openai/) and [Pydantic libraries](https://pypi.org/project/pydantic/) you are running you may need to upgrade to a newer version. These examples were tested against `openai 1.42.0` and `pydantic 2.8.2`.

```cmd
pip install openai pydantic --upgrade
```

```python
from pydantic import BaseModel
from openai import AzureOpenAI

client = AzureOpenAI(
  azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"), 
  api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
  api_version="2024-08-01-preview"
)


class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: list[str]

completion = client.beta.chat.completions.parse(
    model="MODEL_DEPLOYMENT_NAME", # replace with the model deployment name of your gpt-4o 2024-08-06 deployment
    messages=[
        {"role": "system", "content": "Extract the event information."},
        {"role": "user", "content": "Alice and Bob are going to a science fair on Friday."},
    ],
    response_format=CalendarEvent,
)

event = completion.choices[0].message.parsed

print(event)
print(completion.model_dump_json(indent=2))
```

### Output

```json
name='Science Fair' date='Friday' participants=['Alice', 'Bob']
{
  "id": "chatcmpl-A1EUP2fAmL4SeB1lVMinwM7I2vcqG",
  "choices": [
    {
      "finish_reason": "stop",
      "index": 0,
      "logprobs": null,
      "message": {
        "content": "{\n  \"name\": \"Science Fair\",\n  \"date\": \"Friday\",\n  \"participants\": [\"Alice\", \"Bob\"]\n}",
        "refusal": null,
        "role": "assistant",
        "function_call": null,
        "tool_calls": [],
        "parsed": {
          "name": "Science Fair",
          "date": "Friday",
          "participants": [
            "Alice",
            "Bob"
          ]
        }
      }
    }
  ],
  "created": 1724857389,
  "model": "gpt-4o-2024-08-06",
  "object": "chat.completion",
  "service_tier": null,
  "system_fingerprint": "fp_1c2eaec9fe",
  "usage": {
    "completion_tokens": 27,
    "prompt_tokens": 32,
    "total_tokens": 59
  }
}
```

# [REST](#tab/rest)

`response_format` is set to `json_schema` with `strict: true` set.

```bash
curl -X POST  https://YOUR_RESOURCE_NAME.openai.azure.com/openai/deployments/YOUR_MODEL_DEPLOYMENT_NAME/chat/completions?api-version=2024-08-01-preview \
  -H "api-key: $AZURE_OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
    -d '{
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

---

## Function calling with structured outputs

Structured Outputs for function calling can be enabled with a single parameter, by supplying `strict: true`.

# [Python (Microsoft Entra ID)](#tab/python-secure)

```python
from enum import Enum
from typing import Union
from pydantic import BaseModel
import openai
from openai import AzureOpenAI

client = AzureOpenAI(
  azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"), 
  api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
  api_version="2024-08-01-preview"
)


class GetDeliveryDate(BaseModel):
    order_id: str

tools = [openai.pydantic_function_tool(GetDeliveryDate)]

messages = []
messages.append({"role": "system", "content": "You are a helpful customer support assistant. Use the supplied tools to assist the user."})
messages.append({"role": "user", "content": "Hi, can you tell me the delivery date for my order #12345?"}) 

response = client.chat.completions.create(
    model="MODEL_DEPLOYMENT_NAME", # replace with the model deployment name of your gpt-4o 2024-08-06 deployment
    messages=messages,
    tools=tools
)

print(response.choices[0].message.tool_calls[0].function)
print(response.model_dump_json(indent=2))
```

# [Python (key-based auth)](#tab/python)

```python
from enum import Enum
from typing import Union
from pydantic import BaseModel
import openai
from openai import OpenAI

client = AzureOpenAI(
  azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"), 
  api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
  api_version="2024-08-01-preview"
)

class GetDeliveryDate(BaseModel):
    order_id: str

tools = [openai.pydantic_function_tool(GetDeliveryDate)]

messages = []
messages.append({"role": "system", "content": "You are a helpful customer support assistant. Use the supplied tools to assist the user."})
messages.append({"role": "user", "content": "Hi, can you tell me the delivery date for my order #12345?"}) 

response = client.chat.completions.create(
    model="MODEL_DEPLOYMENT_NAME", # replace with the model deployment name of your gpt-4o 2024-08-06 deployment
    messages=messages,
    tools=tools
)

print(response.choices[0].message.tool_calls[0].function)
print(response.model_dump_json(indent=2))
```

# [REST](#tab/rest)

```bash
curl -X POST  https://YOUR_RESOURCE_NAME.openai.azure.com/openai/deployments/YOUR_MODEL_DEPLOYMENT_NAME/chat/completions?api-version=2024-08-01-preview \
  -H "api-key: $AZURE_OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
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

---

## Supported schemas and limitations

Azure OpenAI structured outputs supports the same subset of the [JSON Schema](https://json-schema.org/docs) as OpenAI.

### Supported types

- String
- Number
- Boolean
- Integer
- Object
- Array
- Enum
- anyOf

> [!NOTE]
> Root objects cannot be the `anyOf` type.

### All fields must be required

All fields or function parameters must be included as required. In the example below `location`, and `unit` are both specified under `"required": ["location", "unit"]`.

```json
{
    "name": "get_weather",
    "description": "Fetches the weather in the given location",
    "strict": true,
    "parameters": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "The location to get the weather for"
            },
            "unit": {
                "type": "string",
                "description": "The unit to return the temperature in",
                "enum": ["F", "C"]
            }
        },
        "additionalProperties": false,
        "required": ["location", "unit"]
    }
```

If needed, it is possible to emulate an optional parameter by using a union type with `null`. In this example this is achieved with the line `"type": ["string", "null"],`.

```json
{
    "name": "get_weather",
    "description": "Fetches the weather in the given location",
    "strict": true,
    "parameters": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "The location to get the weather for"
            },
            "unit": {
                "type": ["string", "null"],
                "description": "The unit to return the temperature in",
                "enum": ["F", "C"]
            }
        },
        "additionalProperties": false,
        "required": [
            "location", "unit"
        ]
    }
}
```

### Nesting depth

A schema may have up to 100 object properties total, with up to 5 levels of nesting

### additionalProperties: false must always be set in objects

This controls if an object can have additional key value pairs that were not defined in the JSON Schema. In order to use structured outputs you must set this value to false.

### Key ordering

Structured outputs are ordered the same as the provided schema. To change the output order, modify the order of the schema that you send as part of your inference request.

### Unsupported type-specific keywords

| Type | Unsupported Keyword
|---|----|
| String | minlength<br> maxLength<br> pattern<br> format |
| Number | minimum<br> maximum<br> multipleOf |
| Objects | patternProperties<br> unevaluatedProperties<br> propertyNames<br> minProperties<br> maxProperties |
| Arrays | unevaluatedItems <br> contains <br> minContains <br> maxContains <br> minItems<br> maxItems<br> uniqueItems |

### Nested schemas using anyOf must adhere to the overall JSON Schema subset

Example supported `anyOf` schema:

```json
{
	"type": "object",
	"properties": {
		"item": {
			"anyOf": [
				{
					"type": "object",
					"description": "The user object to insert into the database",
					"properties": {
						"name": {
							"type": "string",
							"description": "The name of the user"
						},
						"age": {
							"type": "number",
							"description": "The age of the user"
						}
					},
					"additionalProperties": false,
					"required": [
						"name",
						"age"
					]
				},
				{
					"type": "object",
					"description": "The address object to insert into the database",
					"properties": {
						"number": {
							"type": "string",
							"description": "The number of the address. Eg. for 123 main st, this would be 123"
						},
						"street": {
							"type": "string",
							"description": "The street name. Eg. for 123 main st, this would be main st"
						},
						"city": {
							"type": "string",
							"description": "The city of the address"
						}
					},
					"additionalProperties": false,
					"required": [
						"number",
						"street",
						"city"
					]
				}
			]
		}
	},
	"additionalProperties": false,
	"required": [
		"item"
	]
}
```

### Definitions are supported

Supported example:

```json
{
	"type": "object",
	"properties": {
		"steps": {
			"type": "array",
			"items": {
				"$ref": "#/$defs/step"
			}
		},
		"final_answer": {
			"type": "string"
		}
	},
	"$defs": {
		"step": {
			"type": "object",
			"properties": {
				"explanation": {
					"type": "string"
				},
				"output": {
					"type": "string"
				}
			},
			"required": [
				"explanation",
				"output"
			],
			"additionalProperties": false
		}
	},
	"required": [
		"steps",
		"final_answer"
	],
	"additionalProperties": false
}
```

### Recursive schemas are supported

Example using # for root recursion

```json
{
        "name": "ui",
        "description": "Dynamically generated UI",
        "strict": true,
        "schema": {
            "type": "object",
            "properties": {
                "type": {
                    "type": "string",
                    "description": "The type of the UI component",
                    "enum": ["div", "button", "header", "section", "field", "form"]
                },
                "label": {
                    "type": "string",
                    "description": "The label of the UI component, used for buttons or form fields"
                },
                "children": {
                    "type": "array",
                    "description": "Nested UI components",
                    "items": {
                        "$ref": "#"
                    }
                },
                "attributes": {
                    "type": "array",
                    "description": "Arbitrary attributes for the UI component, suitable for any element",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "The name of the attribute, for example onClick or className"
                            },
                            "value": {
                                "type": "string",
                                "description": "The value of the attribute"
                            }
                        },
                      "additionalProperties": false,
                      "required": ["name", "value"]
                    }
                }
            },
            "required": ["type", "label", "children", "attributes"],
            "additionalProperties": false
        }
    }
```

Example of explicit recursion

```json
{
	"type": "object",
	"properties": {
		"linked_list": {
			"$ref": "#/$defs/linked_list_node"
		}
	},
	"$defs": {
		"linked_list_node": {
			"type": "object",
			"properties": {
				"value": {
					"type": "number"
				},
				"next": {
					"anyOf": [
						{
							"$ref": "#/$defs/linked_list_node"
						},
						{
							"type": "null"
						}
					]
				}
			},
			"additionalProperties": false,
			"required": [
				"next",
				"value"
			]
		}
	},
	"additionalProperties": false,
	"required": [
		"linked_list"
	]
}
```

##