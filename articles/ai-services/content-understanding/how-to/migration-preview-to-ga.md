---
title: Migration from Azure Content Understanding in Foundry Tools Preview to GA
titleSuffix: Foundry Tools
description: Migrate from Azure Content Understanding in Foundry Tools Preview to GA, including API changes and best practices.
author: PatrickFarley
ms.author: pafarley
ms.service: azure-ai-content-understanding
ms.topic: how-to
ms.date: 01/29/2026
ai-usage: ai-assisted
ms.custom:
  - references_regions
  - ignite-2025
---


# Migrate from Azure Content Understanding preview to GA

The Content Understanding GA API introduces new capabilities and updates to features that launched in earlier preview API versions. The [What's new](../whats-new.md) page provides an overview of changes in the `2025-11-01` Content Understanding GA API version.

This article highlights changes needed to migrate analyzers and applications built with preview API versions (`2024-12-01-preview` and `2025-05-01-preview`).

## Prerequisites

* [!INCLUDE [foundry-model-deployment-setup](../includes/foundry-model-deployment-setup.md)]

## Update analyzers

To update your existing analyzers, follow this three-step process.

### Step 1: Get the analyzer definition

Get the analyzer definition by calling:

```http
GET /analyzers/{analyzerName}
```

The analyzer definition might look like this if it was created with the `2025-05-01-preview` API.

```jsonc
{
  "analyzerId": "my-custom-invoice-analyzer",
  "description": "Extracts vendor information, line items, and totals from commercial invoices",
  "baseAnalyzerId": "prebuilt-documentSearch",
  "config": {
    /*...*/
  },
  "fieldSchema": {/*...*/}
}
```

### Step 2: Update the analyzer definition for the GA API

The following changes are needed for the analyzer to work with the GA API:

1. Add or update the `baseAnalyzerId` property at the top level of the analyzer definition and set it to one of the supported values: `prebuilt-document`, `prebuilt-audio`, `prebuilt-video`, or `prebuilt-image`. Select the one that corresponds to the files that you plan to process with this analyzer. The `Scenario` property from the preview release is deprecated.

2. Add a `models` object with a completion model and embeddings model specified. This object sets the default generative models that this analyzer uses.

For example, the schema from step 1 is updated to:
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
> To match preview behavior as closely as possible, use a GPT-4o `2024-08-06` generative deployment. For new analyzers, GPT-4.1 is a recommended model for Content Understanding.

### Step 3: Create a new analyzer

You can use the updated definition to create a new analyzer:

```http
PUT /analyzers/{analyzerName}_updated
```

You need to delete the existing analyzer to reuse the same analyzer name.

## Other API changes to consider

1. Content classifiers and video segmentation are now merged into content analyzers. To segment and classify content, use the `contentCategories` property of the analyzer. See [Build a robotic process automation (RPA) solution](../tutorial/robotic-process-automation.md) and [Video segmentation](../video/overview.md#segmentation-mode) for guidance.

2. Confidence and grounding are optional properties for fields. By default, a field definition doesn't return confidence or grounding. To add confidence and grounding, set `estimateFieldSourceAndConfidence` to `true`. This behavior is unchanged from the `2025-05-01-preview` API.

3. The request to get specific components of the analyze result is simplified. To get embedded images or content, call:

```http
GET /analyzerResults/{operationId}/files/{path}
```

Here, `path` can include:

* `contents/{contentIndex}/pages/{pageNumber}` - `DocumentContent.pages[*].pageNumber`
* `contents/{contentIndex}/figures/{figureId}` - `DocumentContent.figures[*].id`

4. The **Analyze** operation now only supports analyzing files by URL. Use the **analyzeBinary** operation to upload files in the request body as a base64-encoded string. If you previously used the analyze operation to upload files inline in your code, update your code to use analyzeBinary instead. Learn more about [Analyze binary](/rest/api/contentunderstanding/content-analyzers/analyze-binary).

5. The **Analyze** operation JSON payload schema is updated to add an `inputs` array that contains information about the file to be analyzed. Each input element contains a URL pointer to a file. Learn more about [Analyze](/rest/api/contentunderstanding/content-analyzers/analyze).

> [!NOTE]
> The inputs array only supports a single item in the `2025-11-01` version.

Here's an example of the updated schema for `PUT /analyzers/{analyzerName}`:

```jsonc
{
  "inputs": [
    {
      "url": "https://documentintelligence.ai.azure.com/documents/samples/read/read-healthcare.png" /* This is the file to be analyzed */
    }
  ]
}
```

6. If you used in-context learning or labeled data, the API payload to define the labeled dataset is now updated to specify labeled data as a type of `knowledgeSources`. For more information, see [Create or replace](/rest/api/contentunderstanding/content-analyzers/create-or-replace).

7. For video analyzers, key frames are returned as an array of `keyFrames`. Learn more in [Analyze](/rest/api/contentunderstanding/content-analyzers/analyze).
 
### New features

1. Field extraction method is optional. When it's not set, the analyzer determines the approach (`extract` or `generate`). Don't add the `method` property unless you need the value extracted verbatim.
2. Added support for confidence scores and source grounding for fields with method set to generate in document analyzers.
3. Increased field limits to 1,000 fields per analyzer.
4. Classification/segmentation supports up to 200 distinct types for documents.

### Deprecated features

1. Pro mode isn't part of the GA API. This feature is still experimental. As a result, `AnalysisMode` is deprecated and standard is the only mode supported in the GA API.
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

* [Learn more about Content Understanding pricing](../pricing-explainer.md).
* [Learn more about Content Understanding analyzers](../concepts/analyzer-reference.md).