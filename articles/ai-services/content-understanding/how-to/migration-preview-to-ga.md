---
title: Migration from Azure Content Understanding in Foundry Tools Preview to GA
titleSuffix: Foundry Tools
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


# Migration from Azure Content Understanding Preview to GA

The Content Understanding GA API introduces several new capabilities and updates to features launched in earlier preview API versions. The [What's New](../whats-new.md) page provides an overview of all the changes in the `2025-11-01` Content Understanding GA API version. This document highlights the changes needed to analyzers and applications built with one of the preview API versions to migrate (`2024-12-01 preview` and `2025-05-01 preview`)

## Prerequisite

- Deploy a supported completion model and embedding model to use with the `2025-11-01` Content Understanding GA API (See [Support Models](../concepts/models-deployments.md#supported-models)). To start, try deploying a GPT-4.1 completion model and a text-embedding-3-large embedding model. For directions on how to deploy models, see [Create model deployments in Microsoft Foundry portal](/articles/ai-foundry/foundry-models/how-to/create-model-deployments.md?pivots=ai-foundry-portal).

## Updating analyzers

To update your existing analyzers the recommended approach is to follow this three step process to update.

### Step 1 - Get the analyzer definition
Get the analyzer definition by calling GET /analyzers/{analyzer name}/

The analyzer definition might look something like this if it was created with the `2025-05-01-preview` API. 

```jsonc
{
  "analyzerId": "my-custom-invoice-analyzer",
  "description": "Extracts vendor information, line items, and totals from commercial invoices",
  "baseAnalyzerId": "prebuilt-documentSearch",
  "config": {
    /*...*/
  },
  "fieldSchema": {/*...*/},
}
```

### Step 2 - Make the changes to the analyzer to target the GA API

The following changes are needed for the analyzer to work with the GA API.

1. Add or update the BaseAnalyzerID property to be included at the top-level of the analyzer definition and set to one of the four supported values  - `prebuilt-document`, `prebuilt-audio`, `prebuilt-video`, `prebuilt-image`. Select the one that corresponds with the files that you plan to process with this analyzer. The `Scenario` property from preview release is deprecated and replaced by `baseAnalyzerId`.

2. Add a models object with completion and embeddings model specified. This object specifies the default generative models that this analyzer uses.

For example, the schema from step 1 would be updated to:
```jsonc
{
  "analyzerId": "my-custom-invoice-analyzer",
  "description": "Extracts vendor information, line items, and totals from commercial invoices",
  "baseAnalyzerId": "prebuilt-document",
  "config": {
    /*...*/
  },
  "fieldSchema": {/*...*/},
  "models": {
    "completion": "gpt-4.1",
    "embedding": "text-embedding-3-large"
  }
}
```
> [!TIP]
> To maximize similarly with preview behavior use a GPT-4o `2024-08-06` generative deployment. For new analyzers, GPT-4.1 is a recommended model for Content Understanding. 

### Step 3 - Create a new analyzer
You can use the updated definition to create a new analyzer. Call PUT /analyzers/{analyzer name}_updated/ with the updated definition. You need to delete the existing analyzer to reuse the name.

## Other API Changes to Consider

1. Content classifiers and Video Segmentation are now merged into content analyzers. To segment and classify content, use the `contentCategories` properties of the analyzer. See [build a RPA solution](../tutorial/robotic-process-automation.md) and [video segmentation](../video/overview.md#segmentation-mode) for guidance on how to classify or classify and analyze.

2. Confidence and grounding are now optional properties for fields. The default field definition doesn't return confidence and grounding, to add confidence and grounding, set the `estimateFieldSourceAndConfidence` to `true`. This behavior is unchanged from the `2025-05-01-preview` API.

3. Simplified the request to GET specific components of the Analyze result. GET the embedded images or content with the API call.
``` JSON
GET /analyzerResults/{operationId}/files/{path}
```

Here, ```path``` can include:

* contents/{contentIndex}/pages/{pageNumber} - DocumentContent.pages[*].pageNumber
* contents/{contentIndex}/figures/{figureId} - DocumentContent.figures[*].id

4. The **Analyze** operation now only supports analyzing files by URL. Use the new **analyzeBinary** operation to upload files as part of the request body as a base64 encoded string. If you previously used the analyze operation to upload files inline in your code, you need to update your code to use the analyzeBinary operation instead. Learn more about the [Analyze operation](/rest/api/contentunderstanding/content-analyzers/analyzebinary).

5. The **Analyze** operation JSON payload schema is updated to add an inputs array that contains the information on the files to be analyzed. Each input element contains a url pointer to a file. Learn more about the [Analyze operation](/rest/api/contentunderstanding/content-analyzers/analyze).

Here's an example of the updated schema for PUT /analyzers/{analyzerName}

``` jsonc

{
      "inputs":[
      {
        "url": "https://documentintelligence.ai.azure.com/documents/samples/read/read-healthcare.png" /*This is the file to be analyzed*/
      }
      ],
      "modelDeployments":{
        "gpt-4.1": "myDeployment-gpt-4.1", /*generative capabilities will be processed using this deployment*/
        "text-embedding-3-large":  "myEmbeddingDeployment"
      } 
}
```

6. If you used in-context learning or labeled data, the API payload to define the labeled dataset is now updated to specify the labeled data as a type of ```knowledgeSources```. For more information see [knowledgeSources](/rest/api/contentunderstanding/content-analyzers/create-or-replace) for more details on how to define an analyzer to use labeled data.

7. For video modality analyzers, the key frames are now returned as an array of ```keyFrames```. Learn more about the [analyzer response](/rest/api/contentunderstanding/content-analyzers/analyze).
 
### New features

1. Field extraction method is now optional. When not set, the analyzer determines the approach (extract or generate). The best practice is to not add the method property to the analyzer and only set the method to extract if you need the value to be extracted verbatim.
2. Added support for confidence scores and source grounding for fields with method set to generate in document analyzers.
3. Increased field limits to 1,000 fields per analyzer.
4. Classification/segmentation supports up to 200 distinct types for documents.

### Deprecated features

1. Pro mode isn't a part of the GA API. This feature is still experimental. As a result, `AnalysisMode` is being deprecated and standard is the only mode supported in the GA API.
2. Person directory and Face API aren't part of the GA APIs. This includes the video analyzer features to detect and recognize faces in videos.
3. `TrainingData` is being deprecated and replaced with `knowledgeSources`.


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