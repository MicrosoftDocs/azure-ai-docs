---
title: Migration from Azure Content Understanding in Foundry Tools Preview to GA
titleSuffix: Azure AI services
description: Migrate from Azure Content Understanding in Foundry Tools Preview to GA, including API changes and best practices.
author: PatrickFarley
ms.author: pafarley
ms.service: azure-ai-content-understanding
ms.topic: how-to
ms.date: 10/30/2025
ms.custom:
  - references_regions
  - ignite-2025
---


# Migration from Azure Content Understanding in Foundry Tools Preview to GA

The Content Understanding GA API introduces several new capabilities and updates to features launched in earlier preview API versions. The [what's new](../whats-new.md) page provides an overview of all the changes in the GA API version. This document highlights the changes needed to analyzers built with  one of the preview API versions to use with the GA API version.

To update your analyzer, the recommended approach is to create an updated analyzer:
1. GET the analyzer definition
2. Make the changes to the analyzer to target the GA API. The changes that are needed depend on the API version the analyzer was created with.
3. Create a new analyzer using the GA API PUT operation. You'll need to delete the existing analyzer to reuse the name.

#### [from `2025-05-01 preview`](#tab/2025-05-01)

## Migrating from `2025-05-01 preview`

The `2025-05-01-preview` API version is the latest preview version and migrating from this version of the API to the GA API requires a few updates to your analyzer definitions. 

1. Connect to an Azure Foundry model deployment. The GA API requires a deployment of an LLM to be used by your analyzer. This is a three step process. 

* **Step 1** You can specify the deployments to use on the resource via a ```PATCH``` request. 

``` JSON
PATCH /contentunderstanding/defaults
{
  // Specify the default model deployments for each LLM/embedding model.
  "modelDeployments": {
    "gpt-4.1": "gpt-4.1-deployment-name",
    "gpt41-mini": "gpt-4.1-mini",
    "ada002":  "text-embedding-ada-002"
  }
}

```

* **Step 2** Define the models that a specific analyzer should use when building the analyzer

``` JSON

{
"analyzerId": "myReceipt",
// Specify the LLM/embedding models used by this analyzer.
    "models": {
      "completion": "gpt-4.1",
      "embedding": "text-embedding-ada-002"
    },
  "config": {
    
    
  },
  // Complete analyzer definition
}

```

* **Step 3** At analyze time, connect the model that the analyzer should use with the deployment. If you have defaults defined on the resource, no action is required, if no defaults are defined, or you want to override the defaults, provide the `modelDeployment` to use.

``` JSON
POST /myReceipt:analyze
{

  "modelDeployments": {
    "gpt-4.1": "myGpt41Deployment"
  },
  "inputs": ....
}

```

> [!NOTE]
> [Prebuilt analyzers](../concepts/prebuilt-analyzers.md) require a specific model. See the models catalog for the models each prebuilt works with.

For a detailed description of how to define the models and deployments for use with your analyzers, see [supported models and deployments](../concepts/models-deployments.md).

2. Content classifiers are now merged into content analyzers. To classify content, use the `contentCategories` properties of the analyzer. See [build a RPA solution](../tutorial/robotic-process-automation.md) for guidance on how to classify or classify and analyze.

3. Confidence and grounding are now optional properties for fields. The default field definition doesn't return confidence and grounding, to add confidence and grounding, set the `estimateFieldSourceAndConfidence`  to `true`. This is unchanged from the `2025-05-01-preview` API, it's documented here for completeness.

4. Simplified the request to GET specific components of the Analyze result. GET the embedded images or content with the API call.
``` JSON
GET /analyzerResults/{operationId}/files/{path}
```

Here, ```path``` can include:


* contents/{contentIndex}/pages/{pageNumber} - DocumentContent.pages[*].pageNumber
* contents/{contentIndex}/figures/{figureId} - DocumentContent.figures[*].id

5. New **analyzeBinary** operation to support file upload scenarios. The analyzeBiunary enables files to be uploaded as part of the request body.

6. The **Analyze** operation JSON payload schema is updated to add an inputs array that contains the information on the files to be analyzed. Each input can contain the URL or base64 encoded data. Learn more about the [Analyze operation](/rest/api/contentunderstanding/content-analyzers/analyze).

7. If you used in-context learning or labeled data, the API payload to define the labeled dataset is now updated to specify the labeled data as a type of ```knowledgeSources```. See [knowledgeSources](https://review.learn.microsoft.com/en-us/rest/api/contentunderstanding/content-analyzers/create-or-replace?view=rest-contentunderstanding-2025-11-01&branch=main&tabs=HTTP#referenceknowledgesource) for more details on how to define an analyzer to use labeled data.

8. For video modality analyzers, the key frames are now returned as  an array of ```keyFrames```. Learn more about the [analyzer response](https://review.learn.microsoft.com/en-us/rest/api/contentunderstanding/content-analyzers/analyze?view=rest-contentunderstanding-2025-11-01&branch=main&tabs=HTTP#response).

### Analyze operation

The Analyze operation schema is being updated to add the new ```inputs``` property to the request.

``` JSON

{
    "inputs":[
      {
        "url": "https://documentintelligence.ai.azure.com/documents/samples/read/read-healthcare.png"
      }
    ]
}
```
 
### New features

1. Field extraction method is now optional. When not set, the analyzer determines the approach (extract or generate). The best practice is to not add the method property to the analyzer and only set the method to extract if you need the value to be extracted verbatim.
2. Added support for confidence scores and grounding (source) for generate type fields.
3. Increased field limits to 1,000 fields per analyzer.
4. Field extraction results are now included in the markdown response in YAML front matter format. [Learn more](). 
5. Classification/segmentation supports up to 200 distinct types.

### Deprecated features

1. Pro mode isn't a part of the GA API.This feature is still experimental. As a result, `AnalysisMode` is being deprecated and standard is the only mode supported in the GA API.
2. Person directory and Face API aren't carried forward from the preview APIs. This includes the video analyzer features to detect and recognize faces in videos.
3. `TrainingData` is being deprecated and replaced with `knowledgeSources`.


#### [from `2024-12-01 preview`](#tab/2024-12-01)

## Migrating from `2024-12-01 preview`

The `2024-12-01-preview` API version is the earliest preview version and migrating from this version of the API to the GA API will require a few more updates to your analyzer definitions. Follow the updates described above, with these other changes.

1. Defining a custom analyzer requires a `baseAnalyzerId` property. See [Analyzer configuration reference](../concepts/analyzer-reference.md) for a list of base analyzers that can be used to derive a custom analyzer.
3. Content classifiers are now merged into content analyzers. To classify content, use the `contentCategories` properties of the analyzer. See [build a RPA solution](../tutorial/robotic-process-automation.md) for guidance on how to classify or classify and analyze.
4. Confidence and grounding are now optional properties for fields. The default field definition doesn't return confidence and grounding, to add confidence and grounding, set the `estimateFieldSourceAndConfidence`  to `true`.
5. The `method` property in `fieldSchema` now supports a new default method of `auto`. This is the recommended option for the field method to support both extractive and generative scenarios with confidence and grounding.

### Deprecated features

1. `Scenario` is being deprecated and replaced by `baseAnalyzerId`.

---

<!--

## Breaking changes

[List of breaking changes from Preview to GA]

## API changes

[Detailed API changes]

### Endpoint changes

[URL and endpoint modifications]

### Request/response format changes

[Schema and format updates]

### Authentication changes

[Authentication method updates]

## Migration steps

[Step-by-step migration process]

### Step 1: Update endpoints

[Endpoint migration instructions]

### Step 2: Update authentication

[Authentication migration instructions]

### Step 3: Update request formats

[Request format updates]

### Step 4: Update response handling

[Response handling updates]

### Step 5: Test and validate

[Testing and validation steps]

## Best practices

[Migration best practices]

## Troubleshooting

[Common migration issues and solutions]

-->

## Next steps

* [Learn more about Content Understanding pricing](../pricing-explainer.md)

* [Learn more Content Understanding analyzers](../concepts/analyzer-reference.md)