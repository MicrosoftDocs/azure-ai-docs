---
title: How to use structured outputs for chat models
titleSuffix: Microsoft Foundry
description: Learn how to use structured outputs with chat completions with Microsoft Foundry Models
author: msakande
reviewer: santiagxf
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: include
ms.date: 08/28/2025
ms.author: mopeakande
ms.reviewer: fasantia
zone_pivot_groups: azure-ai-inference-samples
---

[!INCLUDE [intro](intro.md)]

[!INCLUDE [how-to-prerequisites-python](../how-to-prerequisites-python.md)]

* Initialize a client to consume the model:

    ```python
    import os
    import json
    from azure.ai.inference import ChatCompletionsClient
    from azure.ai.inference.models import SystemMessage, UserMessage, JsonSchemaFormat
    from azure.core.credentials import AzureKeyCredential
    
    client = ChatCompletionsClient(
        endpoint="https://<resource>.services.ai.azure.com/models",
        credential=AzureKeyCredential(os.environ["AZURE_INFERENCE_CREDENTIAL"]),
        model="gpt-4o"
    )
    ```

## How to use structured outputs

Structured outputs use JSON schemas to enforce output structure. JSON schemas describe the shape of the JSON object, including expected values, types, and which ones are required. Those JSON objects are encoded as a string within the response of the model.

### Example

To illustrate, let's try to parse the attributes of a GitHub Issue from its description.

```python
import requests

url = "https://api.github.com/repos/Azure-Samples/azure-search-openai-demo/issues/2231"
response = requests.get(url)
issue_body = response.json()["body"]
```

The output of `issue_body` is:

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

When defining schemas, follow these recommendations:


* Use clear and expressive keys.
* Use `_` if you need to separate words to convey meaning.
* Create clear titles and descriptions for important keys in your structure.
* Evaluate multiple structures until you find the one that works best for your use case.
* Take into account limitations when indicating schemas—limitations might vary per model.

Let's load this schema:

```python
with open("github_issue_schema.json", "r") as f:
    github_issue_schema = json.load(f)
```

### Use structured outputs

We can use structured outputs with the defined schema as follows:

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

The following example shows how you can use Pydantic to define a schema for a GitHub issue.

```python
from pydantic import BaseModel
from typing import Literal

class Issue(BaseModel, extra="forbid"):
    title: str
    description: str
    type: Literal["Bug", "Feature", "Documentation", "Regression"]
    operating_system: str
```

Some things to notice:

* We represent schemas using a class that inherits from `BaseModel`.
* We set `extra="forbid"` to instruct Pydantic to _not_ accept additional properties from what we've specified.
* We use type annotations to indicate the expected types.
* `Literal` indicates we expect specific fixed values.

```python
github_issue_schema = Issue.model_json_schema()
```

### Use structured outputs

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

Structured outputs can still contain mistakes. If you see mistakes, try adjusting your instructions, providing examples in the system instructions, or splitting tasks into simpler subtasks.

It's a best practice to use validators to ensure you get valid structures. In Pydantic, you can verify the schema of a given object as follows:

```python
from pydantic import ValidationError

try:
    Issue.model_validate(json_response_message, strict=True)
except ValidationError as e:
    print(f"Validation error: {e}")
```

### Specifying a schema

There are some limitations that models might place in schemas definitions. Such limitations might vary per-model. **We recommend reviewing the documentation from the model provider** to verify that your schemas are valid.

The following guidelines apply to most of the models:

#### Optional fields

Some models might require all the fields to be in the `required` section of the schema. If you need to use optional fields, use unions with null types to express that a given field can be optional.

```python
from pydantic import BaseModel
from typing import Literal, Union

class Issue(BaseModel, extra="forbid"):
    title: str
    description: str
    type: Literal["Bug", "Feature", "Documentation", "Regression"]
    operating_system: Union[str, None]
```

#### Nested types

Models might support indicating nesting types. You can compose complex structures as needed:

```python
from pydantic import BaseModel
from typing import Literal

class Project(BaseModel, extra="forbid"):
    name: str
    owner: str

class Issue(BaseModel, extra="forbid"):
    title: str
    description: str
    type: Literal["Bug", "Feature", "Documentation", "Regression"]
    operating_system: str
    project: Project
```

Nested types also include recursive definition of types:

```python
from pydantic import BaseModel
from typing import Literal, List

class Issue(BaseModel, extra="forbid"):
    title: str
    description: str
    type: Literal["Bug", "Feature", "Documentation", "Regression"]
    operating_system: str
    related_issues: List[Issue]
```

Verify the level of nesting supported by the model you're working with.

## Structured outputs in images

You can use structured outputs with multi-modal models to extract information from data such as image data. 

Let's consider the following chart:

:::image type="content" source="../../media/use-structured-outputs/example-graph-treecover.png" alt-text="An example image showing a chart with the annual loss in thousand square kilometers of global tree cover across different climate zones." lightbox="../../media/use-structured-outputs/example-graph-treecover.png":::

We can define a generic schema that can be used to encode the information contained in the chart and then use it for further analysis. We use [Pydantic objects as described before](#use-pydantic-objects).

```python
from pydantic import BaseModel

class DataPoint(BaseModel):
    x: float
    y: float
    serie: str

class Graph(BaseModel):
    title: str
    description: str
    x_axis: str
    y_axis: str
    legend: list[str]
    data: list[DataPoint]
```

We can load the image as follows to pass it to the model:

```python
from azure.ai.inference.models import ImageContentItem, ImageUrl

image_graph = ImageUrl.load(
    image_file="example-graph-treecover.png",
    image_format="png"
)
```

Use structured outputs to extract the information:

```python
response = client.complete(
    response_format=JsonSchemaFormat(
        name="graph_schema",
        schema=Graph.model_json_schema(),
        description="Describes the data in the graph",
        strict=False,
    ),
    messages=[
        SystemMessage("""
                      Extract the information from the graph. Extrapolate the values of the x axe to ensure you have the correct number
                      of data points for each of the years from 2001 to 2023. Scale the values of the y axes to account for the values
                      being stacked.
                      """
        ),
        UserMessage(content=[ImageContentItem(image_url=image_graph)]),
    ],
)
```

It's always a good practice to validate the outputs and schemas:

```python
import json

json_response_message = json.loads(response.choices[0].message.content)
data = Graph.model_validate(json_response_message)
print(json.dumps(json_response_message, indent=4))
```

```output
{
    "title": "Global tree cover: annual loss",
    "description": "Annual loss in thousand square kilometers of global tree cover across different climate zones.",
    "x_axis": "Year",
    "y_axis": "Thousand square kilometers",
    "legend": [
        "Boreal",
        "Temperate",
        "Subtropical",
        "Tropical"
    ],
    "data": [
        {
            "x": 2001,
            "y": -35,
            "serie": "Boreal"
        },
        {
            "x": 2001,
            "y": -10,
            "serie": "Temperate"
        },
        {
            "x": 2001,
            "y": -55,
...
            "serie": "Tropical"
        }
    ]
}
```

We can see how much information the model was able to capture by plotting the data using `matplotlib`:

```python
import matplotlib.pyplot as plt
import pandas as pd

# Convert data to a DataFrame for easier manipulation
df = pd.DataFrame(data.model_dump()["data"])

# Pivot the data to prepare for stacked bar chart
pivot_df = df.pivot(index="x", columns="serie", values="y").fillna(0)

# Plotting
fig, ax = plt.subplots(figsize=(10, 6))

# Stacked bar chart
pivot_df.plot(kind="bar", stacked=True, ax=ax, color=["#114488", "#3CB371", "#1188AA", "#006400"])

# Chart customization
ax.set_title(data.title, fontsize=16)
ax.set_xlabel(data.x_axis, fontsize=12)
ax.set_ylabel(data.y_axis, fontsize=12)
ax.legend(title=data.legend, fontsize=10)
ax.grid(axis="y", linestyle="--", alpha=0.7)

# Show the plot
plt.tight_layout()
plt.show()
```

:::image type="content" source="../../media/use-structured-outputs/graph-treecover-plot.png" alt-text="The resulting plot of the data contained in the structured output generated by the model." lightbox="../../media/use-structured-outputs/graph-treecover-plot.png":::

While the information isn't perfect, we can see the model was able to capture a good amount of information from the original chart.