---
title: How to use structured outputs for chat models with Azure AI model inference
titleSuffix: Azure AI Foundry
description: Learn how to use structured outputs with chat completions with Azure AI model inference
manager: scottpolly
author: mopeakande
reviewer: santiagxf
ms.service: azure-ai-model-inference
ms.topic: how-to
ms.date: 1/21/2025
ms.author: mopeakande
ms.reviewer: fasantia
ms.custom: references_regions
zone_pivot_groups: azure-ai-inference-samples
---

[!INCLUDE [Feature preview](~/reusable-content/ce-skilling/azure/includes/ai-studio/includes/feature-preview.md)]

When working with software, it's more challenging to parse free-form text outputs coming from language models. Structured outputs, like JSON, provide a clear format that software routines can read and process. This article explains how to use structured outputs to generate specific JSON schemas with the chat completions API with models deployed to Azure AI model inference in Azure AI services.

## Prerequisites

To use structured outputs with chat completions models in your application, you need:

[!INCLUDE [how-to-prerequisites](../how-to-prerequisites.md)]

[!INCLUDE [how-to-prerequisites-python](../how-to-prerequisites-python.md)]

* A chat completions model deployment with JSON and structured outputs support. If you don't have one read [Add and configure models to Azure AI services](../../how-to/create-model-deployments.md).

    * You can check which models support structured outputs by checking the column **Response format** in the [Models](../../concepts/models.md) article.

    * This article uses `Cohere-command-r-plus-08-2024`.

* Initialize a client to consume the model:

    ```python
    import os
    import json
    from azure.ai.inference import ChatCompletionsClient
    from azure.ai.inference.models import SystemMessage, UserMessage, JsonSchemaFormat
    from azure.core.credentials import AzureKeyCredential
    
    client = ChatCompletionsClient(
        endpoint="https://aiservices-demo-wus2.services.ai.azure.com/models",
        credential=AzureKeyCredential(os.environ["AZURE_INFERENCE_CREDENTIAL"]),
        model="Cohere-command-r-plus-08-2024",
    )
    ```

## How to use structured outputs

Structured outputs uses JSON schemas to enforce output structure. JSON schemas describe the shape of the JSON object including expected values, types, and which ones are required. Those JSON objects are encoded as an string within the response of the model.

### Example

To exemplify the scenario, let's try to parse the attributes of a GitHub Issue from it's description.

```python
import requests

url = "https://api.github.com/repos/Azure-Samples/azure-search-openai-demo/issues/2231"
response = requests.get(url)
issue_body = response.json()["body"]
```

The output of `issue_body` looks as follows:

```output
'<!--\r\nIF SUFFICIENT INFORMATION IS NOT PROVIDED VIA THE FOLLOWING TEMPLATE THE ISSUE MIGHT BE CLOSED WITHOUT FURTHER CONSIDERATION OR INVESTIGATION\r\n-->\r\n> Please provide us with the following information:\r\n> ---------------------------------------------------------------\r\n\r\n### This issue is for a: (mark with an `x`)\r\n```\r\n- [x] bug report -> please search issues before submitting\r\n- [ ] feature request\r\n- [ ] documentation issue or request\r\n- [ ] regression (a behavior that used to work and stopped in a new release)\r\n```\r\n\r\n### Minimal steps to reproduce\r\n> Deploy the app with auth and acl´s turned on, configure the acls file, run all the scripts needed.\r\n\r\n### Any log messages given by the failure\r\n> None\r\n\r\n### Expected/desired behavior\r\n> groups field to be filled the the groups id\'s that have permissions to "view the file"\r\n\r\n### OS and Version?\r\n> win 10\r\n### azd version?\r\n> azd version 1.11.0\r\n\r\n### Versions\r\n>\r\n\r\n### Mention any other details that might be useful\r\n\r\nAfter configuring the json with the perms all the scripts (`adlsgen2setup.py` and `prepdocs.ps1`) everything goes well but the groups metadata tag never gets to have any groups.\r\n\r\n![image](https://github.com/user-attachments/assets/40f1eb09-2c21-4244-98b5-adfb3fa16955)\r\n\r\n\r\n> ---------------------------------------------------------------\r\n> Thanks! We\'ll be in touch soon.\r\n'
```

### Define the schema

The following JSON schema defines the schema of a GitHub issue:

__github_issue_schema.json__

```json
{
    "title": "github_issue",
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

Let's load this schema:

```python
with open("github_issue_schema.json", "r") as f:
    github_issue_schema = json.load(f)
```

When defining schemas, follow these recommendations:

> [!div class="checklist"]
> * Use clear and expressive keys.
> * Use `_` if you need to separate words to convey meaning.
> * Create clear titles and descriptions for important keys in your structure.
> * Evaluate multiple structures until finding the one that works best for your use case.

### Use structure outputs

We can use structure outputs with the defined schema as follows:

```python
response = client.complete(
    response_format=JsonSchemaFormat(
        name="github_issue",
        schema=github_issue_schema,
        description="Describes a GitHub issue",
        strict=True,
    ),
    messages=[
        SystemMessage("""
            Extract structured information from GitHub issues opened in our project.

                Provide
                - The title of the issue
                - A 1-2 sentence description of the project
                - The type of issue (Bug, Feature, Documentation, Regression)
                - The operating system the issue was reported on
                - Whether the issue is a duplicate of another issue
            """),
        UserMessage(issue_body),
    ],
)
```

Let's see how this works:

```python
json_response_message = json.loads(response.choices[0].message.content)
print(json.dumps(json_response_message, indent=4))
```

```output
{
    "title": "Metadata tags issue on access control lists - ADLSgen2 setup",
    "description": "Our project seems to have an issue with the metadata tag for groups when deploying the application with access control lists and necessary settings.",
    "type": "Bug",
    "operating_system": "Windows 10"
}
```


## Use Pydantic objects

Maintaining JSON schemas by hand is difficult and prone to errors. AI developers usually use [Pydantic](https://docs.pydantic.dev/) objects to describe the shapes of a given object. Pydantic is an open-source data validation library where you can flexibly define data structures for your applications.

### Define the schema

The following example shows how you can use Pydantic to define an schema for a GitHub issue.

```python
from pydantic import BaseModel
from typing import Literal
from enum import Enum

class Issue(BaseModel, extra="forbid"):
    title: str
    description: str
    type: Literal["Bug", "Feature", "Documentation", "Regression"]
    operating_system: str
```

Some things to notice:

> [!div class="checklist"]
> * We represent schemas using a class that inherits from `BaseModel`.
> * We set `extra="forbid"` to instruct Pyndantic to do not accept additional properties from what we have specified.
> * We use type annotations to indicate the expected types.
> * `Literal` indicates we expect specific fixed values.

```python
github_issue_schema = Issue.model_json_schema()
```

### Use structure outputs

Let's see how we can use the schema in the same way:

```python
response = client.complete(
    response_format=JsonSchemaFormat(
        name="github_issue",
        schema=github_issue_schema,
        description="Describes a GitHub issue",
        strict=True,
    ),
    messages=[
        SystemMessage("""
            Extract structured information from GitHub issues opened in our project.

                Provide
                - The title of the issue
                - A 1-2 sentence description of the project
                - The type of issue (Bug, Feature, Documentation, Regression)
                - The operating system the issue was reported on
                - Whether the issue is a duplicate of another issue
            """),
        UserMessage(issue_body),
    ],
)
```

Let's see how this works:

```python
json_response_message = json.loads(response.choices[0].message.content)
print(json.dumps(json_response_message, indent=4))
```

```output
{
    "title": "Metadata tags issue on access control lists - ADLSgen2 setup",
    "description": "Our project seems to have an issue with the metadata tag for groups when deploying the application with access control lists and necessary settings.",
    "type": "Bug",
    "operating_system": "Windows 10"
}
```

### Validate

Structured Outputs can still contain mistakes. If you see mistakes, try adjusting your instructions, providing examples in the system instructions, or splitting tasks into simpler subtasks.

The following example uses validators in Pydantic to verify the schema:

```python
from pydantic import ValidationError

try:
    Issue.model_validate(json.loads(response.choices[0].message.content), strict=True)
except ValidationError as e:
    print(f"Validation error: {e}")
```