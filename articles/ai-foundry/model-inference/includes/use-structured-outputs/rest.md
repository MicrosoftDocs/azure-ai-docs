---
title: How to use structured outputs for chat models with Azure AI model inference
titleSuffix: Azure AI Foundry
description: Learn how to use structured outputs with chat completions with Azure AI model inference
manager: scottpolly
author: msakande
reviewer: santiagxf
ms.service: azure-ai-model-inference
ms.topic: how-to
ms.date: 1/21/2025
ms.author: mopeakande
ms.reviewer: fasantia
zone_pivot_groups: azure-ai-inference-samples
---

[!INCLUDE [intro](intro.md)]

## How to use structured outputs

Structured outputs uses JSON schemas to enforce output structure. JSON schemas describe the shape of the JSON object including expected values, types, and which ones are required. Those JSON objects are encoded as an string within the response of the model.

### Example

To exemplify the scenario, let's try to parse the attributes of a GitHub Issue from it's description. The following [example is extracted from a GitHub issue in Azure-Samples repository](https://api.github.com/repos/Azure-Samples/azure-search-openai-demo/issues/2231).

```output
'<!--\r\nIF SUFFICIENT INFORMATION IS NOT PROVIDED VIA THE FOLLOWING TEMPLATE THE ISSUE MIGHT BE CLOSED WITHOUT FURTHER CONSIDERATION OR INVESTIGATION\r\n-->\r\n> Please provide us with the following information:\r\n> ---------------------------------------------------------------\r\n\r\n### This issue is for a: (mark with an `x`)\r\n```\r\n- [x] bug report -> please search issues before submitting\r\n- [ ] feature request\r\n- [ ] documentation issue or request\r\n- [ ] regression (a behavior that used to work and stopped in a new release)\r\n```\r\n\r\n### Minimal steps to reproduce\r\n> Deploy the app with auth and acl´s turned on, configure the acls file, run all the scripts needed.\r\n\r\n### Any log messages given by the failure\r\n> None\r\n\r\n### Expected/desired behavior\r\n> groups field to be filled the the groups id\'s that have permissions to "view the file"\r\n\r\n### OS and Version?\r\n> win 10\r\n### azd version?\r\n> azd version 1.11.0\r\n\r\n### Versions\r\n>\r\n\r\n### Mention any other details that might be useful\r\n\r\nAfter configuring the json with the perms all the scripts (`adlsgen2setup.py` and `prepdocs.ps1`) everything goes well but the groups metadata tag never gets to have any groups.\r\n\r\n![image](https://github.com/user-attachments/assets/40f1eb09-2c21-4244-98b5-adfb3fa16955)\r\n\r\n\r\n> ---------------------------------------------------------------\r\n> Thanks! We\'ll be in touch soon.\r\n'
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

### Use structure outputs

We can use structure outputs with the defined schema as follows:

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
            "content": "Extract structured information from GitHub issues opened in our project.

                Provide
                - The title of the issue.
                - A 1-2 sentence description of the project.
                - The type of issue (Bug, Feature, Documentation, Regression).
                - The operating system the issue was reported on.
                - Whether the issue is a duplicate of another issue."
        },
        {
            "role": "user",
            "content": "'<!--\r\nIF SUFFICIENT INFORMATION IS NOT PROVIDED VIA THE FOLLOWING TEMPLATE THE ISSUE MIGHT BE CLOSED WITHOUT FURTHER CONSIDERATION OR INVESTIGATION\r\n-->\r\n> Please provide us with the following information:\r\n> ---------------------------------------------------------------\r\n\r\n### This issue is for a: (mark with an `x`)\r\n```\r\n- [x] bug report -> please search issues before submitting\r\n- [ ] feature request\r\n- [ ] documentation issue or request\r\n- [ ] regression (a behavior that used to work and stopped in a new release)\r\n```\r\n\r\n### Minimal steps to reproduce\r\n> Deploy the app with auth and acl´s turned on, configure the acls file, run all the scripts needed.\r\n\r\n### Any log messages given by the failure\r\n> None\r\n\r\n### Expected/desired behavior\r\n> groups field to be filled the the groups id\'s that have permissions to "view the file"\r\n\r\n### OS and Version?\r\n> win 10\r\n### azd version?\r\n> azd version 1.11.0\r\n\r\n### Versions\r\n>\r\n\r\n### Mention any other details that might be useful\r\n\r\nAfter configuring the json with the perms all the scripts (`adlsgen2setup.py` and `prepdocs.ps1`) everything goes well but the groups metadata tag never gets to have any groups.\r\n\r\n![image](https://github.com/user-attachments/assets/40f1eb09-2c21-4244-98b5-adfb3fa16955)\r\n\r\n\r\n> ---------------------------------------------------------------\r\n> Thanks! We\'ll be in touch soon.\r\n'"
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
    "model": "Cohere-command-r-plus-08-2024"
}
```

Let's see how this works:

__Response__

```json
{
    "id": "0a1234b5de6789f01gh2i345j6789klm",
    "object": "chat.completion",
    "created": 1718726686,
    "model": "mistral-large-2407",
    "choices": [
        {
            "index": 0,
            "message": {
                "role": "assistant",
                "content": "{
                    \"title\": "Metadata tags issue on access control lists - ADLSgen2 setup\",
                    \"description\": "Our project seems to have an issue with the metadata tag for groups when deploying the application with access control lists and necessary settings.\",
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
