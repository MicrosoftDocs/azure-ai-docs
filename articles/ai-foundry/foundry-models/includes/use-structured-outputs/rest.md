---
title: How to use structured outputs for chat models
titleSuffix: Microsoft Foundry
description: Learn how to use structured outputs with chat completions with Microsoft Foundry Models
author: msakande
reviewer: santiagxf
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: include
ms.date: 05/29/2025
ms.author: mopeakande
ms.reviewer: fasantia
zone_pivot_groups: azure-ai-inference-samples
---

[!INCLUDE [intro](intro.md)]

## How to use structured outputs

Structured outputs use JSON schemas to enforce output structure. JSON schemas describe the shape of the JSON object, including expected values, types, and which ones are required. Those JSON objects are encoded as a string within the response of the model.

### Example

To illustrate, let's try to parse the attributes of a GitHub Issue from its description. The following [example is extracted from a GitHub issue in Azure-Samples repository](https://api.github.com/repos/Azure-Samples/azure-search-openai-demo/issues/2231).

```output
<!--
IF SUFFICIENT INFORMATION IS NOT PROVIDED VIA THE FOLLOWING TEMPLATE THE ISSUE MIGHT BE CLOSED WITHOUT FURTHER CONSIDERATION OR INVESTIGATION
-->
> Please provide us with the following information:
> ---------------------------------------------------------------

### This issue is for a: (mark with an `x`)

- [x] bug report -> please search issues before submitting
- [ ] feature request
- [ ] documentation issue or request
- [ ] regression (a behavior that used to work and stopped in a new release)

### Minimal steps to reproduce
> Deploy the app with auth and acl´s turned on, configure the acls file, run all the scripts needed.

### Any log messages given by the failure
> None

### Expected/desired behavior
> groups field to be filled with the groups id's that have permissions to "view the file"

### OS and Version?
> win 10
...

> ---------------------------------------------------------------
> Thanks! We'll be in touch soon.
```

### Define the schema

The following JSON schema defines the schema of a GitHub issue:

__github_issue_schema.json__

```json
{
    "title": "Issue",
    "type": "object",
    "properties": {
        "title": {
            "title": "Title",
            "type": "string"
        },
        "description": {
            "title": "Description",
            "type": "string"
        },
        "type": {
            "enum": ["Bug", "Feature", "Documentation", "Regression"],
            "title": "Type",
            "type": "string"
        },
        "operating_system": {
            "title": "Operating System",
            "type": "string"
        }
    },
    "required": ["title", "description", "type", "operating_system"],
    "additionalProperties": false
}
```

### Use structured outputs

We can use structured outputs with the defined schema as follows:

__Request__

```http
POST https://<resource>.services.ai.azure.com/models/chat/completions?api-version=2024-05-01-preview
Content-Type: application/json
api-key: <key>
```

__Body__

```json
{
    "messages": [
        {
            "role": "system",
            "content": "Extract structured information from GitHub issues opened in our project.\n\n                Provide\n                - The title of the issue.\n                - A 1-2 sentence description of the project.\n                - The type of issue (Bug, Feature, Documentation, Regression).\n                - The operating system the issue was reported on.\n                - Whether the issue is a duplicate of another issue."
        },
        {
            "role": "user",
            "content": "'<!--\r\nIF SUFFICIENT INFORMATION IS NOT PROVIDED VIA THE FOLLOWING TEMPLATE THE ISSUE MIGHT BE CLOSED WITHOUT FURTHER CONSIDERATION OR INVESTIGATION\r\n-->\r\n> Please provide us with the following information:\r\n> ---------------------------------------------------------------\r\n\r\n### This issue is for a: (mark with an `x`)\r\n```\r\n- [x] bug report -> please search issues before submitting\r\n- [ ] feature request\r\n- [ ] documentation issue or request\r\n- [ ] regression (a behavior that used to work and stopped in a new release)\r\n```\r\n\r\n### Minimal steps to reproduce\r\n> Deploy the app with auth and acl´s turned on, configure the acls file, run all the scripts needed.\r\n\r\n### Any log messages given by the failure\r\n> None\r\n\r\n### Expected/desired behavior\r\n> groups field to be filled the the groups id's that have permissions to \"view the file\"\r\n\r\n### OS and Version?\r\n> win 10\r\n### azd version?\r\n> azd version 1.11.0\r\n\r\n### Versions\r\n>\r\n\r\n### Mention any other details that might be useful\r\n\r\nAfter configuring the json with the perms all the scripts (`adlsgen2setup.py` and `prepdocs.ps1`) everything goes well but the groups metadata tag never gets to have any groups.\r\n\r\n![image](https://github.com/user-attachments/assets/40f1eb09-2c21-4244-98b5-adfb3fa16955)\r\n\r\n\r\n> ---------------------------------------------------------------\r\n> Thanks! We'll be in touch soon.\r\n'"
        }
    ],
    "response_format": {
        "type": "json_schema",
        "json_schema": {
            "name": "github_issue",
            "schema": {
                "type": "object",
                "properties": {
                    "title": {
                        "title": "Title",
                        "type": "string"
                    },
                    "description": {
                        "title": "Description",
                        "type": "string"
                    },
                    "type": {
                        "enum": ["Bug", "Feature", "Documentation", "Regression"],
                        "title": "Type",
                        "type": "string"
                    },
                    "operating_system": {
                        "title": "Operating System",
                        "type": "string"
                    }
                },
                "required": ["title", "description", "type", "operating_system"],
                "additionalProperties": false
            },
            "strict": true
        }
    },
    "model": "gpt-4o"
}
```

Let's see how this works:

__Response__

```json
{
    "id": "0a1234b5de6789f01gh2i345j6789klm",
    "object": "chat.completion",
    "created": 1718726686,
    "model": "gpt-4o",
    "choices": [
        {
            "index": 0,
            "message": {
                "role": "assistant",
                "content": "{
                    \"title\": \"Metadata tags issue on access control lists - ADLSgen2 setup\",
                    \"description\": \"Our project seems to have an issue with the metadata tag for groups when deploying the application with access control lists and necessary settings.\",
                    \"type\": \"Bug\",
                    \"operating_system\": \"Windows 10\"
                }",
                "tool_calls": null
            },
            "finish_reason": "stop",
            "logprobs": null
        }
    ],
    "usage": {
        "prompt_tokens": 150,
        "total_tokens": 246,
        "completion_tokens": 96
    }
}
```

## Structured outputs in images

You can use structured outputs with multi-modal models to extract information from data such as image data. 

Let's consider the following chart:

:::image type="content" source="../../media/use-structured-outputs/example-graph-treecover.png" alt-text="An example image showing a chart with the annual loss in thousand square kilometers of global tree cover across different climate zones." lightbox="../../media/use-structured-outputs/example-graph-treecover.png":::

We can define a generic schema that can be used to encode the information contained in the chart and then use it for further analysis.

### Define the schema

The following schema captures generic information contained in a chart:

__graph_schema.json__

```json
{
    "$defs": {
        "DataPoint": {
            "properties": {
                "x": {
                    "title": "X",
                    "type": "number"
                },
                "y": {
                    "title": "Y",
                    "type": "number"
                },
                "serie": {
                    "title": "Serie",
                    "type": "string"
                }
            },
            "required": [
                "x",
                "y",
                "serie"
            ],
            "title": "DataPoint",
            "type": "object",
            "additionalProperties": false
        }
    },
    "title": "Graph",
    "type": "object",
    "properties": {
        "title": {
            "title": "Title",
            "type": "string"
        },
        "description": {
            "title": "Description",
            "type": "string"
        },
        "x_axis": {
            "title": "X Axis",
            "type": "string"
        },
        "y_axis": {
            "title": "Y Axis",
            "type": "string"
        },
        "legend": {
            "items": {
                "type": "string"
            },
            "title": "Legend",
            "type": "array"
        },
        "data": {
            "items": {
                "$ref": "#/$defs/DataPoint"
            },
            "title": "Data",
            "type": "array"
        }
    },
    "required": [
        "title",
        "description",
        "x_axis",
        "y_axis",
        "legend",
        "data"
    ],
    "additionalProperties": false
}
```


## Use structured outputs

We can use structured outputs with the defined schema as follows:

__Request__

```http
POST https://<resource>.services.ai.azure.com/models/chat/completions?api-version=2024-05-01-preview
Content-Type: application/json
api-key: <key>
```

__Body__

```json
{
    "messages": [
        {
            "role": "system",
            "content": "Extract the information from the graph. Extrapolate the values of the x axe to ensure you have the correct number of data points for each of the years from 2001 to 2023. Scale the values of the y axes to account for the values being stacked."
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "data:image/jpg;base64,0xABCDFGHIJKLMNOPQRSTUVWXYZ..."
                    }
                }
            ]
        }
    ],
    "response_format": {
        "type": "json_schema",
        "json_schema": {
            "name": "graph_schema",
            "schema": {
                "$defs": {
                    "DataPoint": {
                        "properties": {
                            "x": {
                                "title": "X",
                                "type": "number"
                            },
                            "y": {
                                "title": "Y",
                                "type": "number"
                            },
                            "serie": {
                                "title": "Serie",
                                "type": "string"
                            }
                        },
                        "required": [
                            "x",
                            "y",
                            "serie"
                        ],
                        "title": "DataPoint",
                        "type": "object",
                        "additionalProperties": false
                    }
                },
                "title": "Graph",
                "type": "object",
                "properties": {
                    "title": {
                        "title": "Title",
                        "type": "string"
                    },
                    "description": {
                        "title": "Description",
                        "type": "string"
                    },
                    "x_axis": {
                        "title": "X Axis",
                        "type": "string"
                    },
                    "y_axis": {
                        "title": "Y Axis",
                        "type": "string"
                    },
                    "legend": {
                        "items": {
                            "type": "string"
                        },
                        "title": "Legend",
                        "type": "array"
                    },
                    "data": {
                        "items": {
                            "$ref": "#/$defs/DataPoint"
                        },
                        "title": "Data",
                        "type": "array"
                    }
                },
                "required": [
                    "title",
                    "description",
                    "x_axis",
                    "y_axis",
                    "legend",
                    "data"
                ],
                "additionalProperties": false
            },
            "strict": true
        }
    },
    "model": "gpt-4o"
}
```

Let's see how this works:

__Response__

```json
{
    "id": "0a1234b5de6789f01gh2i345j6789klm",
    "object": "chat.completion",
    "created": 1718726686,
    "model": "gpt-4o",
    "choices": [
        {
            "index": 0,
            "message": {
                "role": "assistant",
                "content": "{
                    \"title\": \"Global tree cover: annual loss\",
                    \"description\": \"Annual loss in thousand square kilometers of global tree cover across different climate zones.\",
                    \"x_axis\": \"Year\",
                    \"y_axis\": \"Thousand square kilometers\",
                    \"legend\": [
                        \"Boreal\",
                        \"Temperate\",
                        \"Subtropical\",
                        \"Tropical\"
                    ],
                    \"data\": [
                        {
                            \"x\": 2001,
                            \"y\": -35,
                            \"serie\": \"Boreal\"
                        },
                        {
                            \"x\": 2001,
                            \"y\": -10,
                            \"serie\": \"Temperate\"
                        },
...
                        {
                            \"x\": 2023,
                            \"y\": -195,
                            \"serie\": \"Tropical\"
                        }
                    ]
                }",
                "tool_calls": null
            },
            "finish_reason": "stop",
            "logprobs": null
        }
    ],
    "usage": {
        "prompt_tokens": 1250,
        "total_tokens": 3246,
        "completion_tokens": 1996
    }
}
```

While the information isn't perfect, we can see the model was able to capture a good amount of information from the original chart.
