---
title: Migrate from Azure Content Understanding in Foundry Tools Preview to GA
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

# Migrate from Azure Content Understanding Preview to GA

The Azure Content Understanding API has reached general availability (GA). It introduces several new capabilities and updates to features that were released in earlier preview API versions. The [What's new](../whats-new.md) page provides an overview of all the changes in the `2025-11-01` Content Understanding GA API version.

This article highlights changes needed to migrate analyzers and applications that were built with one of the preview API versions (`2024-12-01 preview` and `2025-05-01 preview`).

## Prerequisites

[!INCLUDE [foundry-model-deployment-setup](../includes/foundry-model-deployment-setup.md)]

## Update analyzers

To update your existing analyzers, we recommend that you follow this three-step process.

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

Make the following changes so that the analyzer works with the GA API.

1. Add or update the `baseAnalyzerId` property at the top level of the analyzer definition and set it to one of the supported values: `prebuilt-document`, `prebuilt-audio`, `prebuilt-video`, or `prebuilt-image`. Select the one that corresponds to the files that you plan to process with this analyzer. The `Scenario` property from the preview release is deprecated.

1. Add a `models` object and specify the completion and embeddings model. This object sets the default generative models that this analyzer uses.

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
> To more closely match preview behavior, use a GPT-4o `2024-08-06` generative deployment. For new analyzers, we recommend GPT-4.1 for Content Understanding.

### Step 3: Create a new analyzer

You can use the updated definition to create a new analyzer:

```http
PUT /analyzers/{analyzerName}_updated
```

You need to delete the existing analyzer to reuse the name.

## Consider these other API changes

- Content classifiers and video segmentation are now merged into content analyzers. To segment and classify content, use the `contentCategories` properties of the analyzer. See [Build a robotic process automation (RPA) solution](../tutorial/robotic-process-automation.md) and [Video segmentation](../video/overview.md#segmentation-mode) for guidance.

- Confidence and grounding are now optional properties for fields. The default field definition doesn't return confidence and grounding. To add confidence and grounding, set `estimateFieldSourceAndConfidence` to `true`. This behavior is unchanged from the `2025-05-01-preview` API.

- The request to get specific components of the `analyze` result is simplified. To get embedded images or content, call:

  ```http
  GET /analyzerResults/{operationId}/files/{path}
  ```

  Here, `path` can include:

  * `contents/{contentIndex}/pages/{pageNumber}` - `DocumentContent.pages[*].pageNumber`
  * `contents/{contentIndex}/figures/{figureId}` - `DocumentContent.figures[*].id`

- The `analyze` operation now supports only analyzing files by URL. Use the new `analyzeBinary` operation to upload files as part of the request body as a base64-encoded string. If you previously used the `analyze` operation to upload files inline in your code, you need to update your code to instead use the `analyzeBinary` operation. [Learn more about the `analyzeBinary` operation](/rest/api/contentunderstanding/content-analyzers/analyze-binary).

- The `analyze` operation's JSON payload schema is updated. There's now an inputs array that contains the information on the file to be analyzed. Each input element contains a URL pointer to a file. Learn more about the [`analyze` operation](/rest/api/contentunderstanding/content-analyzers/analyze).

  > [!NOTE]
  > The inputs array supports only a single item in the `2025-11-01` version.

  Here's an example of the updated schema for `PUT /analyzers/{analyzerName}`:

  ``` jsonc

  {
        "inputs":[
        {
          "url": "https://documentintelligence.ai.azure.com/documents/samples/read/read-healthcare.png" /*This is the file to be analyzed*/
        }
        ]
  }
  ```

- If you used in-context learning or labeled data, the API payload that defines the labeled dataset now specifies the labeled data as a type of `knowledgeSources`. For more information, see [Create or replace](/rest/api/contentunderstanding/content-analyzers/create-or-replace).

- For video analyzers, the key frames are now returned as an array of `keyFrames`. [Learn more in Analyze](/rest/api/contentunderstanding/content-analyzers/analyze).

### New features

- The field extraction method is optional. When the method isn't set, the analyzer determines the approach (`extract` or `generate`). Don't add the `method` property unless you need the value extracted verbatim.
- There's added support for confidence scores and source grounding for fields in document analyzers that have the method set to generate.
- There are now increased field limits to 1,000 fields per analyzer.
- For documents, classification and segmentation supports up to 200 distinct types.

### Deprecated features

- The GA API doesn't include Pro mode, which is still experimental. As a result, `AnalysisMode` is being deprecated and standard is the only mode supported in the GA API.
- Person directory and Face API aren't part of the GA APIs, including the video analyzer features to detect and recognize faces in videos.
- The `TrainingData` feature is being deprecated and replaced with the `knowledgeSources` feature.

# Related content

- [Learn more about Content Understanding pricing](../pricing-explainer.md)
- [Learn more about Content Understanding analyzers](../concepts/analyzer-reference.md)
