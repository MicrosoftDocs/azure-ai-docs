---
title: Azure Content Understanding in Foundry Tools Classifier Overview
titleSuffix: Foundry Tools
description: Learn about Azure Content Understanding in Foundry Tools classifier solutions.
author: PatrickFarley 
ms.author: pafarley
manager: mcleans
ms.date: 07/09/2026
ms.service: azure-content-understanding-foundry-tools
ms.topic: overview
ms.custom:
  - build-2025
  - dev-focus
ai-usage: ai-assisted
---

# Content Understanding classification/segmentation


Content Understanding lets you implement classification and splitting as part of the analyzer operation request. You can perform content classification and content extraction as part of a single API call. 

The global concept of `analyzer` now includes the concept of `contentCategories` and `enableSegment` to classify and split the input data you process within your application. This analyzer feature can perform classification of an input file as a whole. It can also identify multiple documents or multiple instances of a single document within an input file. 

Starting with the GA version, document classification and video segmentation design are unified, allowing for a coherent approach to process input data regardless of its modality. In the documentation, "Content Understanding classification" refers to the analyze operations required for classifying and splitting input data (`contentCategories` and `enableSegment`).

## Business use cases

Content Understanding classification lets you process complex documents and videos in various formats and templates:

* **Invoices**: Categorize invoices from multiple vendors to process each category with a different Content Understanding analyzer, if needed.
* **Tax documents**: Categorize multiple tax documents into different types of tax forms, such as 1040 and 1099.
* **Contracts**: Categorize long, unstructured contracts to streamline operations to understand different types of agreements and their specific legal implications.
* **Sports video**: Automatically segment the scenes to break the video into logical chunks such as ads and the actual sports content.

## Classification/segmentation capabilities

Content Understanding can analyze single or multi-file documents to identify whether an input file can be classified into a defined category. The following scenarios are supported:

**Document scenarios:**
* **Classify only**: Classifies the input file as a whole. For example, a single file that contains one document type, such as a loan application form.
* **Classify and analyze**: Classifies and analyzes the input file by routing the input to the desired extraction analyzer.
* **Classify and segment**: Classifies and segments a single input file that might have multiple types or instances of documents concatenated. For example, a loan application package that contains a loan application form, pay slip, and bank statement. Another example is a collection of scanned invoices in a single file.
* **Classify, segment, and analyze**: Once the segments are classified, route each segment to the desired extraction analyzer for further field extraction.
* **[Hierarchical classifier](#hierarchical-classifier)**: Optional additional analysis depending on the category can also be a classifier analyzer.

**Video scenarios:**
* **Segment only**: Split video into segments based on content characteristics defined in the `description` field of `contentCategories`. For example, splitting a sports broadcast into game play, commercials, and commentary segments.
* **Segment and analyze**: Split video into segments and route each segment to an analyzer for field extraction.

> [!NOTE]
> The minimum unit for classification of documents is a single page. Intra-page classification isn't supported.

### Create classification categories

Content Understanding classification doesn't require a training dataset. You can define up to 200 category names and descriptions within the analyze operation. By default, the entire file is treated as a single content object, which means the file is associated with a single category.

Starting with the GA version, you need to include the `other` category within the `contentCategories` to ensure that content can remain unmatched to any of your defined categories. If the `other` category isn't included, all files are classified into one of your defined categories. Each of the category names you define within `contentCategories` can also include a `description` to give further information about the category you're defining.


### Input file splitting

When you have more than one document in a file, the classifier can identify the different document types that are contained within the input file with splitting capability. The classifier response contains the page ranges for each of the identified document types that are contained within a file. This response can include multiple instances of the same document type.

When you run the `analyze` operation, it includes an `enableSegment` property that gives you granular control over the splitting behavior. You can also specify the page numbers to analyze only certain pages of the input document:

* To treat the entire input file as multiple documents combined together for classification, set `enableSegment` to `true`. When you do so, the service returns categories for the segments within the input file automatically.
* To treat the entire input file as a single document, set `enableSegment` to `false`.

By default, segments start at page boundaries. The `2026-06-01-preview` API version adds in-page segmentation, which can split a single page into multiple segments when it contains content from different document types. In-page segmentation is controlled by a separate `allowInPageSegments` field, so you can opt in to sub-page splits without changing existing `enableSegment` behavior. For more information, see [Classification enhancements (2026-06-01 preview)](#classification-enhancements-2026-06-01-preview).

> [!NOTE]
> For videos, only segmentation is supported. You must define a single `contentCategories` with `enableSegment` set to `true`. Use the `description` field to specify criteria for splitting the video into segments.


### Optional analysis

For a complete end-to-end flow, you can link classifier categories with existing custom analyzers and prebuilt analyzers. For each content object classified to categories with linked analyzers, the service automatically invokes analysis on the content object by using the corresponding analyzer.

For example, you can use this linking to create classifiers that identify and analyze only invoices from a PDF that contains multiple types of forms. Set `analyzerId` to a prebuilt analyzer or custom analyzer to route and perform field extraction from the classified documents or pages.

You can also omit setting any `analyzerId` to categorize, but not perform any content analysis on the categorized file or segment.

At the top layer, you can also set `omitContent` to `true` to omit the original content object and return only content objects from analysis performed on the classified segments or files.

#### Hierarchical classifier

The analyzer operation supports hierarchical splitting and classification. In the base analyzer operation, set `analyzerId` on each content category to a custom analyzer that performs additional classification or splitting. This approach supports scenarios such as invoices, contracts, and receipts, where each category's `analyzerId` can point to another analyzer operation that classifies different document subtypes.

Document inputs support five levels of nesting, and video inputs support two.

### Classification enhancements (2026-06-01 preview)

The preceding sections describe GA behavior. This section describes preview-only capabilities that require API version `2026-06-01-preview`.

The `2026-06-01-preview` API version includes two enhancements to document classification and splitting. To use these enhancements, target the preview API version when you submit an analyze request.

> [!IMPORTANT]
> These features are in public preview. Preview capabilities are provided without a service-level agreement and aren't recommended for production workloads.

#### Layout-based feature extraction (preview)

In the `2026-06-01-preview` API, the classifier adds rich classification signals such as layout-based document features - section markers, table headers, figure descriptions, and more.

Layout-aware sampling improves classification accuracy in scenarios where the distinguishing content is highly unstructured or spread across a page. For example:

* Pages that are sparse in text, for example X-ray images or scanned diagnostic reports.
* Figure-heavy pages, where a figure description carries most of the classification signal.
* Pages where key section headers or table headers appear in the middle of the page.

No configuration change is required. When you call the preview API, the classifier automatically uses the layout-based features.

#### In-page segmentation (preview)

The `2026-06-01-preview` API adds *in-page* segmentation, which can split a single page into multiple segments when the page contains content that belongs to different document types.

In-page segmentation is helpful for scenarios such as:

* **Medical records** where a single page mixes content types, for example a patient demographics section followed by a referral order on the same page.
* **Tax packages** where multiple schedules or forms are stacked on the same page, for example K-1 schedules.
* **Multi-form packets** where consecutive forms don't always start on a new page.

To enable in-page segmentation, set `allowInPageSegments` to `true` when you create or update a custom analyzer (you can't set this field in an analyze request). The response from the analyzer includes per-segment page ranges, each segment's category, a confidence score, and a source expression that identifies the segment's bounding position on the page.

The following example shows the `segments` array in an analyze response, where a single page is split into a credit card segment and an identity card segment:

```json
"segments": [
    {
        "span": {
            "offset": 0,
            "length": 301
        },
        "segmentId": "segment1",
        "startPageNumber": 1,
        "endPageNumber": 1,
        "category": "Credit_card",
        "confidence": 0.98,
        "source": "D(1,1.32,1.49,3.13,1.49,3.13,3.86,1.32,3.86)"
    },
    {
        "span": {
            "offset": 301,
            "length": 798
        },
        "segmentId": "segment2",
        "startPageNumber": 1,
        "endPageNumber": 1,
        "category": "Identity_card",
        "confidence": 0.99,
        "source": "D(1,1.16,4.95,3.82,4.95,3.82,8.52,1.16,8.52)"
    }
]
```

##### API fields

The following API fields support in-page segmentation:

| Field | Type | Description |
|---|---|---|
| `ContentAnalyzerConfig.allowInPageSegments` | `boolean` | Set when you create or update a custom analyzer. When `true`, segments can cover a portion of a page instead of full pages. |
| `DocumentContentSegment.segmentId` | `string` | Stable identifier for the segment, such as `segment1`. |
| `DocumentContentSegment.span` | `Span` | `offset` and `length` of the segment within the parent content text in Markdown format. |
| `DocumentContentSegment.confidence` | `float32` | Value in `[0–1]`. Confidence score for segmentation and category classification. |
| `DocumentContentSegment.source` | `SourceExpression` | Bounding position of the segment on the page, as a polygon expression of the form `D(pageNumber, x1, y1, x2, y2, x3, y3, x4, y4)`. Pass this value as a `range` to a sub-analyzer. |


## Classifier limits

For information on supported input document formats and classifier limits, see [Service quotas and limits](../service-limits.md#basic-limits).

## Best practices

To improve classification and splitting quality, use a good category name and description so that the model can understand the categories with some context. For more information on category names and descriptions, see [Best practices](../concepts/best-practices.md#optimize-classification-and-categorization).

### Key benefits

* **Accuracy and reliability**: Ensure precise document classification to reduce errors and boost efficiency.
* **Scalability**: Scale out document processing to meet business demands.
* **Customizable**: Adapt the document classifier to fit specific workflows.

## Supported languages and regions

For a list of supported languages and regions, see [Language and region support](../language-region-support.md).

## Data privacy and security

If you use Content Understanding, review Microsoft policies on customer data. For more information, see [Data, protection, and privacy](https://www.microsoft.com/trust-center/privacy).

## Related content

* Try processing your document content in [Content Understanding Studio](../quickstart/content-understanding-studio.md)
* Learn about how to process document content using [analyzer templates](../concepts/analyzer-templates.md).
