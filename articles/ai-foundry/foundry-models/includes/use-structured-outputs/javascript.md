---
title: How to use structured outputs for chat models with Microsoft Foundry Models
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

[!INCLUDE [how-to-prerequisites-javascript](../how-to-prerequisites-javascript.md)]

* Initialize a client to consume the model:

    ```javascript
    const client = ModelClient(
        "https://<resource>.services.ai.azure.com/models", 
        new AzureKeyCredential(process.env.AZURE_INFERENCE_CREDENTIAL)
    );
    ```

## How to use structured outputs

Structured outputs use JSON schemas to enforce output structure. JSON schemas describe the shape of the JSON object, including expected values, types, and which ones are required. Those JSON objects are encoded as a string within the response of the model.

### Example

To illustrate, let's try to parse the attributes of a GitHub Issue from its description.

```javascript
const url = 'https://api.github.com/repos/Azure-Samples/azure-search-openai-demo/issues/2231';

async function getIssueBody() {
    try {
        const response = await fetch(url);
        const data = await response.json();
        const issueBody = data.body;
        return issueBody;
    } catch (error) {
        console.error('Error fetching issue:', error);
    }
}

issueBody = await getIssueBody();
```

The output of `issueBody` is:

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

```javascript
import fs from "fs";

const data = fs.readFileSync('./github_issue_schema.json', 'utf-8');
const gitHubIssueSchema = JSON.parse(data);
```

### Use structured outputs

We can use structured outputs with the defined schema as follows:


```javascript
var messages = [
    { role: "system", content: `
        Extract structured information from GitHub issues opened in our project.

            Provide
            - The title of the issue
            - A 1-2 sentence description of the project
            - The type of issue (Bug, Feature, Documentation, Regression)
            - The operating system the issue was reported on
            - Whether the issue is a duplicate of another issue`
    },
    { role: "user", content: issueBody },
];

var response = await client.path("/chat/completions").post({
    body: {
        model: "gpt-4o",
        messages: messages,
        response_format: {
            type: "json_schema",
            json_schema: {
                name: "github_issue",
                schema: gitHubIssueSchema,
                description: "Describes a GitHub issue",
                strict: true,
            },
        }
    }
});
```

Let's see how this works:

```javascript
const rawContent = response.body.choices[0].message.content;
const jsonResponseMessage = JSON.parse(rawContent);

console.log(JSON.stringify(jsonResponseMessage, null, 4));
```

```output
{
    "title": "Metadata tags issue on access control lists - ADLSgen2 setup",
    "description": "Our project seems to have an issue with the metadata tag for groups when deploying the application with access control lists and necessary settings.",
    "type": "Bug",
    "operating_system": "Windows 10"
}
```

## Structured outputs in images

You can use structured outputs with multi-modal models to extract information from data such as image data. 

Let's consider the following chart:

:::image type="content" source="../../media/use-structured-outputs/example-graph-treecover.png" alt-text="An example image showing a chart with the annual loss in thousand square kilometers of global tree cover across different climate zones." lightbox="../../media/use-structured-outputs/example-graph-treecover.png":::

We can define a generic schema that can be used to encode the information contained in the chart and then use it for further analysis.

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

Let's load this schema:

```javascript
import fs from "fs";

const data = fs.readFileSync('./graph_schema.json', 'utf-8');
const graphSchema = JSON.parse(data);
```

We can load the image as follows to pass it to the model:

```javascript
/**
 * Get the data URL of an image file.
 * @param {string} imageFile - The path to the image file.
 * @param {string} imageFormatType - The format of the image file. For example: "jpeg", "png".
 * @returns {string} The data URL of the image.
 */
function getImageDataUrl(imageFile, imageFormatType) {
    try {
        const imageBuffer = fs.readFileSync(imageFile);
        const imageBase64 = imageBuffer.toString("base64");
        return `data:image/${imageFormatType};base64,${imageBase64}`;
    } catch (error) {
        console.error(`Could not read '${imageFile}'.`);
        console.error("Set the correct path to the image file before running this sample.");
        process.exit(1);
    }
}

var imageContent = getImageDataUrl("example-graph-treecover.png", "png");
```

Use structured outputs to extract the information:

```javascript
var messages = [
    {
        role: "system",
        content: `
            Extract the information from the graph. Extrapolate the values of the x axe to ensure you have the correct number
            of data points for each of the years from 2001 to 2023. Scale the values of the y axes to account for the values
            being stacked.`
    },
    {
        role: "user",
        content: [
            {
                type: "image_url",
                image_url: {
                    url: imageContent,
                }
            }
        ]
    }
];

const response = await client.path("/chat/completions").post({
    body: {
        messages: messages,
        response_format: {
            type: "json_schema",
            json_schema: {
                name: "graph_schema",
                schema: graphSchema,
                description: "Describes the data in the graph",
                strict: true,
            },
        },
        model: "gpt-4o",
    },
});
```


Let's inspect the output:

```javascript
var rawContent = response.body.choices[0].message.content;
var jsonResponseMessage = JSON.parse(rawContent);

console.log(JSON.stringify(jsonResponseMessage, null, 4));
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

To see how much information the model was able to capture, we can try to plot the data:

:::image type="content" source="../../media/use-structured-outputs/graph-treecover-plot.png" alt-text="The resulting plot of the data contained in the structured output generated by the model." lightbox="../../media/use-structured-outputs/graph-treecover-plot.png":::

While the information isn't perfect, we can see the model was able to capture a good amount of information from the original chart.