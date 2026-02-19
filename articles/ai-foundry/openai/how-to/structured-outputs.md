---
title: 'How to use structured outputs with Azure OpenAI in Microsoft Foundry Models'
titleSuffix: Azure OpenAI
description: Learn how to improve your model responses with structured outputs
services: cognitive-services
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: how-to
ms.date: 12/6/2025
author: mrbullwinkle
ms.author: mbullwin
recommendations: false
zone_pivot_groups: structured-outputs
monikerRange: 'foundry-classic || foundry'
ai-usage: ai-assisted
---

# Structured outputs

Structured outputs make a model follow a [JSON Schema](https://json-schema.org/overview/what-is-jsonschema) definition that you provide as part of your inference API call. This is in contrast to the older [JSON mode](./json-mode.md) feature, which guaranteed valid JSON would be generated, but was unable to ensure strict adherence to the supplied schema. Structured outputs are recommended for function calling, extracting structured data, and building complex multi-step workflows.

::: zone pivot="programming-language-python"

[!INCLUDE [structured-outputs-python](../includes/structured-outputs-python.md)]

::: zone-end


::: zone pivot="programming-language-csharp"

[!INCLUDE [structured-outputs-dotnet](../includes/structured-outputs-dotnet.md)]

::: zone-end


::: zone pivot="programming-language-rest"

[!INCLUDE [structured-outputs-rest](../includes/structured-outputs-rest.md)]

::: zone-end

## JSON Schema support and limitations

Azure OpenAI structured outputs support the same subset of the [JSON Schema](https://json-schema.org/docs) as OpenAI.

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
}
```

If needed, it's possible to emulate an optional parameter by using a union type with `null`. In this example, this is achieved with the line `"type": ["string", "null"],`.

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

A schema may have up to 100 object properties total, with up to five levels of nesting

### additionalProperties: false must always be set in objects

This property controls if an object can have additional key value pairs that weren't defined in the JSON Schema. In order to use structured outputs, you must set this value to false.

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

Example using # for root recursion:

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

Example of explicit recursion:

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
> [!NOTE]
> Currently structured outputs are not supported with:
> - [Bring your own data](../concepts/use-your-data.md) scenarios.
> - [Assistants](../how-to/assistant.md) or [Foundry Agents Service](../../agents/overview.md).
> - `gpt-4o-audio-preview` and `gpt-4o-mini-audio-preview` version: `2024-12-17`.

## Supported models

- `gpt-5.1-codex` version: `2025-11-13`
- `gpt-5.1-codex mini` version: `2025-11-13`
- `gpt-5.1` version: `2025-11-13`
- `gpt-5.1-chat` version: `2025-11-13`
- `gpt-5-pro` version `2025-10-06`
- `gpt-5-codex` version `2025-09-11`
- `gpt-5` version `2025-08-07`
- `gpt-5-mini` version `2025-08-07`
- `gpt-5-nano` version `2025-08-07`
- `codex-mini` version `2025-05-16`
- `o3-pro` version `2025-06-10`
- `o3-mini` version `2025-01-31`
- `o1` version: `2024-12-17`
- `gpt-4o-mini` version: `2024-07-18`
- `gpt-4o` version: `2024-08-06`
- `gpt-4o` version: `2024-11-20`
- `gpt-4.1` version `2025-04-14`
- `gpt-4.1-nano` version `2025-04-14`
- `gpt-4.1-mini` version: `2025-04-14`
- `o4-mini` version: `2025-04-16`
- `o3` version: `2025-04-16`


## API support

Support for structured outputs was first added in API version `2024-08-01-preview`. It is available in the latest preview APIs as well as the latest GA API: `v1`.
