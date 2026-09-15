---
title: Classify and route your data using Content Understanding
titleSuffix: Foundry Tools
description: Learn how to create classification workflows to categorize and route your data using Content Understanding Studio, the REST API, or the Azure SDKs for Python, C#, JavaScript, TypeScript, and Java.
author: PatrickFarley 
ms.author: pafarley
manager: mcleans
ms.date: 07/20/2026
ai-usage: ai-assisted
ms.service: azure-content-understanding-foundry-tools
ms.topic: how-to
ms.custom:
  - ignite-2024-understanding-release
  - references_regions
  - ignite-2025
  - build-2026
  - dev-focus
zone_pivot_groups: programming-languages-content-understanding
---

# Classify and route your data using Content Understanding

Content Understanding enables you to create custom classification workflows that categorize your content and route it to the right analyzer. With routing, you can send multiple data streams through the same pipeline and ensure your data is processed by the best analyzer for its type.

This guide walks you through two steps:

1. **Create a basic classifier** that categorizes documents into custom categories.
1. **Classify and route with custom analyzers** that combine classification with field extraction for each category.

## Prerequisites

To get started, make sure you have the following resources and permissions:

* An Azure subscription. If you don't have an Azure subscription, [create a free account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
* A [Microsoft Foundry resource](https://portal.azure.com/#create/Microsoft.CognitiveServicesAIFoundry) in the Azure portal, created in a [supported region](/azure/ai-services/content-understanding/language-region-support).
  * This resource is listed under **Foundry** > **Foundry** in the portal.
* [!INCLUDE [foundry-model-deployment-setup](../includes/foundry-model-deployment-setup.md)]
* [cURL](https://everything.curl.dev/install/index.html) installed for your dev environment (if you use the REST API).
* Language-specific requirements for the SDK samples:
  * **Python**: Python 3.9+ and the `azure-ai-contentunderstanding`, `azure-identity`, and `python-dotenv` packages. The `to_llm_input` helper used in the Python samples is available only in the prerelease SDK (`azure-ai-contentunderstanding` 1.2.0b2 or later). Install it by running `pip install --pre azure-ai-contentunderstanding`.
  * **C#**: .NET 8.0+ and the `Azure.AI.ContentUnderstanding` and `Azure.Identity` NuGet packages.
  * **JavaScript / TypeScript**: Node.js 20 LTS or later and the `@azure/ai-content-understanding`, `@azure/identity`, `@azure/core-auth`, and `dotenv` packages.
  * **Java**: JDK 11+, Maven or Gradle, and the `azure-ai-contentunderstanding` and `azure-identity` dependencies.
* Set the environment variables `CONTENTUNDERSTANDING_ENDPOINT` and (optionally) `CONTENTUNDERSTANDING_KEY` before running any SDK sample. If `CONTENTUNDERSTANDING_KEY` isn't set, the samples fall back to `DefaultAzureCredential`.

## Step 1: Create a basic classifier

A basic classifier categorizes documents into custom content categories. You define the categories with names and descriptions, and the service uses those definitions to classify your input files. The `enableSegment` parameter controls whether the classifier splits multi-document files into segments or treats the entire file as a single document.

The following sections show how to create a basic classifier using Content Understanding Studio and how to create one programmatically with the REST API or an Azure SDK.

### Create a classifier in Content Understanding Studio

Go to the [Content Understanding Studio portal](https://aka.ms/cu-studio) and sign in with your credentials. If you're familiar with the classic Azure Document Intelligence in Foundry Tools Studio experience, Content Understanding extends the same content and field extraction across all modalities—document, image, video, and audio. Select the option to try the new Content Understanding experience to access multimodal capabilities.

1. **Start with a new project**: Select **Create project** on the home page.

1. **Select your project type**: Select the option to `Classify and route with custom categories`.

1. **Upload your data**: Upload a piece of sample data to get started with classifying.

1. **Create routing rules**: Under the **Routing rules** tab, select `Add category`. Give the category a name and description. For a basic classifier, you can skip assigning a specific analyzer to each category.

1. **Test your classification workflow**: When your custom routing rules are ready for testing, select **Run analysis** to see the output of the rules on your data.

    :::image type="content" source="../media/quickstarts/classify-test.png" lightbox="../media/quickstarts/classify-test.png" alt-text="Screenshot of Content Understanding Studio with the Test button highlighted.":::

1. **Build your classification analyzer**: When you're satisfied with the output, select the **Build analyzer** button at the top of the page. Give the analyzer a name and select **Save**.

### Create a classifier programmatically

Select your language or the REST API tab to see the steps for creating a basic classifier.

::: zone pivot="programming-language-rest"

[!INCLUDE [REST API create classifier](./includes/rest-create-classifier.md)]

::: zone-end

::: zone pivot="programming-language-python"

[!INCLUDE [Python SDK create classifier](./includes/python-create-classifier.md)]

::: zone-end

::: zone pivot="programming-language-csharp"

[!INCLUDE [.NET SDK create classifier](./includes/csharp-create-classifier.md)]

::: zone-end

::: zone pivot="programming-language-java"

[!INCLUDE [Java SDK create classifier](./includes/java-create-classifier.md)]

::: zone-end

::: zone pivot="programming-language-javascript"

[!INCLUDE [JavaScript SDK create classifier](./includes/javascript-create-classifier.md)]

::: zone-end

::: zone pivot="programming-language-typescript"

[!INCLUDE [TypeScript SDK create classifier](./includes/typescript-create-classifier.md)]

::: zone-end

## Step 2: Classify and route with custom analyzers

To go beyond basic classification, you can route each category to a specific analyzer for field extraction. This approach combines classification with data extraction in a single pipeline: the classifier identifies the document type and then routes it to the correct analyzer, which extracts fields tailored to that category.

# [Content Understanding Studio](#tab/studio)

To successfully route your data, create custom analyzers for each category. For more information on building custom analyzers, see [Create and improve your custom analyzer in Content Understanding Studio](./customize-analyzer-content-understanding-studio.md).

1. **Create custom analyzers first**: Build custom analyzers for each document type you want to route. For example, create a custom analyzer for loan applications with a field extraction schema specific to that document type.

1. **Create or update routing rules**: Under the **Routing rules** tab, select `Add category`. Give the category a name and description, and select an analyzer to correspond to that route. The tool allows you to preview the schema for each analyzer to ensure you have the right one.

    :::image type="content" source="../media/quickstarts/classify-define-routes.png" alt-text="Screenshot of routes UX for classification." lightbox="../media/quickstarts/classify-define-routes.png" :::

1. **Test your classification workflow**: Select **Run analysis** to see the output of the rules on your data. You can upload additional sample data for testing to see how it performs with multiple different rules.

    :::image type="content" source="../media/quickstarts/classify-test.png" lightbox="../media/quickstarts/classify-test.png" alt-text="Screenshot of Content Understanding Studio with the Test button highlighted.":::

1. **Build your classification analyzer**: When you're satisfied with the output, select the **Build analyzer** button at the top of the page. Give the analyzer a name and select **Save**.

1. **Use your classification analyzer**: Now you have an analyzer endpoint that you can use in your own application via the REST API.

# [REST API](#tab/rest-api)

### Create a custom analyzer for a category

First, create a custom analyzer that extracts fields specific to a document category. This example defines a loan application analyzer with field extraction.

Create a JSON file named `loan-analyzer.json` with the following content:

```json
{
  "baseAnalyzerId": "prebuilt-document",
  "description": "Loan application analyzer - extracts key information from loan applications",
  "config": {
    "returnDetails": true,
    "enableLayout": true,
    "enableFormula": false,
    "estimateFieldSourceAndConfidence": true
  },
  "fieldSchema": {
    "fields": {
      "ApplicationDate": {
        "type": "date",
        "method": "generate",
        "description": "The date when the loan application was submitted."
      },
      "ApplicantName": {
        "type": "string",
        "method": "generate",
        "description": "Full name of the loan applicant or company."
      },
      "LoanAmountRequested": {
        "type": "number",
        "method": "generate",
        "description": "The total loan amount requested by the applicant."
      },
      "LoanPurpose": {
        "type": "string",
        "method": "generate",
        "description": "The stated purpose or reason for the loan."
      },
      "Summary": {
        "type": "string",
        "method": "generate",
        "description": "A brief summary overview of the loan application details."
      }
    }
  },
  "models": {"completion": "gpt-5.2"}
}
```

Create the custom analyzer with a `PUT` request:

```bash
curl -i -X PUT "{endpoint}/contentunderstanding/analyzers/{loanAnalyzerId}?api-version=2025-11-01" \
  -H "Ocp-Apim-Subscription-Key: {key}" \
  -H "Content-Type: application/json" \
  -d @loan-analyzer.json
```

Poll the `Operation-Location` URL from the response header until the status is `"succeeded"`.

**Reference**: [Content Analyzers - Create or Replace](/rest/api/contentunderstanding/content-analyzers/create-or-replace?view=rest-contentunderstanding-2025-11-01&preserve-view=true)

### Define the enhanced classifier with routing

Create a classifier that routes each category to a specific analyzer. Use the `analyzerId` field in each category to point to the analyzer that handles that category.

Create a JSON file named `enhanced-classifier.json` with the following content. Replace `{loanAnalyzerId}` with the analyzer ID you used in the previous step.

```json
{
  "baseAnalyzerId": "prebuilt-document",
  "description": "Enhanced classifier with custom loan analyzer",
  "config": {
    "returnDetails": true,
    "enableSegment": true,
    "contentCategories": {
      "Loan_Application": {
        "description": "Documents submitted by individuals or businesses to request funding, typically including personal or business details, financial history, loan amount, purpose, and supporting documentation.",
        "analyzerId": "{loanAnalyzerId}"
      },
      "Invoice": {
        "description": "Billing documents issued by sellers or service providers to request payment for goods or services, detailing items, prices, taxes, totals, and payment terms."
      },
      "Bank_Statement": {
        "description": "Official statements issued by banks that summarize account activity over a period, including deposits, withdrawals, fees, and balances."
      }
    }
  },
  "models": {"completion": "gpt-5.2"}
}
```

The key difference from a basic classifier is the `analyzerId` property in the `Loan application` category. This tells the service to route documents classified as loan applications through the custom analyzer for field extraction. Categories without an `analyzerId` are classified but not routed to a specific analyzer.

### Create the enhanced classifier

```bash
curl -i -X PUT "{endpoint}/contentunderstanding/analyzers/{enhancedClassifierId}?api-version=2025-11-01" \
  -H "Ocp-Apim-Subscription-Key: {key}" \
  -H "Content-Type: application/json" \
  -d @enhanced-classifier.json
```

Poll the `Operation-Location` URL from the response header until the status is `"succeeded"`.

### Analyze a document with the enhanced classifier

```bash
curl -i -X POST "{endpoint}/contentunderstanding/analyzers/{enhancedClassifierId}:analyze?api-version=2025-11-01" \
  -H "Ocp-Apim-Subscription-Key: {key}" \
  -H "Content-Type: application/json" \
  -d '{
        "inputs": [
          {
            "url": "https://github.com/Azure-Samples/azure-ai-content-understanding-python/raw/refs/heads/main/data/mixed_financial_docs.pdf"
          }
        ]
      }'
```

### Get enhanced classification results

Use the `Operation-Location` URL from the response header to retrieve the results.

```bash
curl -i -X GET "{Operation-Location}" \
  -H "Ocp-Apim-Subscription-Key: {key}"
```

A successful response returns `"status": "Succeeded"` with classification results alongside extracted fields. Documents routed to the custom loan analyzer include extracted field values such as `ApplicantName`, `LoanAmountRequested`, and `LoanPurpose` in the `fields` object for that segment.

**Reference**: [Analyzer Results - Get](/rest/api/contentunderstanding/content-analyzers/get-result?view=rest-contentunderstanding-2025-11-01&preserve-view=true)

### Clean up

Delete the analyzers when you're done.

```bash
curl -i -X DELETE "{endpoint}/contentunderstanding/analyzers/{enhancedClassifierId}?api-version=2025-11-01" \
  -H "Ocp-Apim-Subscription-Key: {key}"
```

```bash
curl -i -X DELETE "{endpoint}/contentunderstanding/analyzers/{loanAnalyzerId}?api-version=2025-11-01" \
  -H "Ocp-Apim-Subscription-Key: {key}"
```

---

> [!TIP]
> For a complete end-to-end Python notebook, see the [classifier sample on GitHub](https://github.com/Azure-Samples/azure-ai-content-understanding-python/blob/main/notebooks/classifier.ipynb).

## Step 3: Enable sub-page segmentation (preview)

You can complete steps 1 and 2 by using the GA API version `2025-11-01`. This step requires using `2026-06-01-preview`.

The `2026-06-01-preview` API version adds *sub-page* (in-page) segmentation and richer per-segment metadata. Use this feature when a single page contains content from more than one document type, for example a scanned page that mixes a credit card and an identity card, or a medical record where a patient demographics section is followed by a referral order on the same page.

> [!IMPORTANT]
> Sub-page segmentation is in public preview. Preview capabilities are provided without a service-level agreement and aren't recommended for production workloads.

# [Content Understanding Studio](#tab/studio)

To enable sub-page segmentation on a classifier in Content Understanding Studio:

1. Open your classifier project and go to the **Routing rules** tab.
1. Confirm that **Enable segment** is turned on, and then select the settings (gear) icon next to it.

    :::image type="content" source="../media/quickstarts/classify-enable-segment-toggle.png" alt-text="Screenshot of the Routing rules tab in Content Understanding Studio with the Enable segment toggle highlighted." lightbox="../media/quickstarts/classify-enable-segment-toggle.png":::

1. In the **Segment Settings** dialog, keep **Auto segment content** selected and select the **Allow in-page segments** checkbox.

    :::image type="content" source="../media/quickstarts/classify-allow-in-page-segments.png" alt-text="Screenshot of the Segment Settings dialog with the Allow in-page segments checkbox highlighted." lightbox="../media/quickstarts/classify-allow-in-page-segments.png":::

    The **Segment Settings** dialog offers two segmentation modes:

    * **Auto segment content**: Content Understanding automatically groups consecutive pages that belong to the same document into a single segment, so one segment can span 1-N pages. Select **Allow in-page segments** to also allow splits in the middle of a page when a page contains content from more than one document type.
    * **Segment by page**: Content Understanding creates one segment for every single page in the document, regardless of content.

1. Select **Close**. The classifier now splits pages that contain more than one document type into separate in-page segments when you run analysis or build the analyzer.

# [REST API](#tab/rest-api)

### New API fields

| Field | Type | Description |
|---|---|---|
| `ContentAnalyzerConfig.allowInPageSegments` | `boolean` | When `true`, segments can cover a portion of a page instead of full pages. |
| `DocumentContentSegment.segmentId` | `string` | Identifier for the segment, such as `segment1`. |
| `DocumentContentSegment.span` | `Span` | `offset` and `length` of the segment within the parent content text. |
| `DocumentContentSegment.confidence` | `float32` | Value in `[0–1]`. Confidence score for segmentation and category classification. |
| `DocumentContentSegment.source` | `SourceExpression` | Bounding position of the segment on the page. Pass this value as a `range` to a sub-analyzer for targeted field extraction. |

### Define a classifier with sub-page segmentation

Set both `enableSegment` and `allowInPageSegments` to `true` in the analyzer configuration. The existing `segmentPerPage` flag defaults to `false` and must remain `false` (or be omitted) when `allowInPageSegments` is `true` - the two options are mutually exclusive. Create a JSON file named `sub-page-classifier.json`:

```json
{
  "baseAnalyzerId": "prebuilt-document",
  "description": "Classifier with sub-page segmentation (preview)",
  "config": {
    "returnDetails": true,
    "enableSegment": true,
    "allowInPageSegments": true,
    "contentCategories": {
      "Credit_card": {
        "description": "Credit card information."
      },
      "Identity_card": {
        "description": "Identity card information."
      },
      "Passport": {
        "description": "Passport document."
      },
      "Other": {
        "description": "Use the Other category only if a segment does not clearly fit into any of the specified categories, and ensure this is a last resort."
      }
    }
  },
  "models": {"completion": "gpt-5.2"}
}
```

Create the classifier against the preview API version:

```bash
curl -i -X PUT "{endpoint}/contentunderstanding/analyzers/{classifierId}?api-version=2026-06-01-preview" \
  -H "Ocp-Apim-Subscription-Key: {key}" \
  -H "Content-Type: application/json" \
  -d @sub-page-classifier.json
```

### Analyze a document with sub-page segmentation

```bash
curl -i -X POST "{endpoint}/contentunderstanding/analyzers/{classifierId}:analyze?api-version=2026-06-01-preview" \
  -H "Ocp-Apim-Subscription-Key: {key}" \
  -H "Content-Type: application/json" \
  -d '{
        "inputs": [
          {
            "url": "https://<your-storage-account>.blob.core.windows.net/samples/mixed_id_documents.pdf"
          }
        ]
      }'
```

### Expected response shape

The result includes a `segments` array on the document content. Each segment carries a `category`, page range, `span`, `confidence`, and `source`. The `source` value is a polygon expression of the form `D(pageNumber, x1, y1, x2, y2, x3, y3, x4, y4)`, where the coordinates are in the analyzer's `unit` (such as `inch`) and describe the segment's bounding box on the page.

The following excerpt is from an analyze result for a single page that contains both a credit card and an identity card:

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

### Route sub-page segments to a sub-analyzer

To extract fields from each in-page segment, set `analyzerId` on the corresponding category. The classifier automatically forwards each segment's `source` as the `range` for the sub-analyzer, so a credit card segment is analyzed by a credit-card analyzer and a passport segment is analyzed by an ID-document analyzer. Update your classifier to reference prebuilt or custom analyzers per category:

```json
{
  "baseAnalyzerId": "prebuilt-document",
  "description": "Classifier with sub-page segmentation and per-category routing (preview)",
  "config": {
    "returnDetails": true,
    "enableSegment": true,
    "allowInPageSegments": true,
    "contentCategories": {
      "Credit_card": {
        "description": "Credit card information.",
        "analyzerId": "prebuilt-creditCard"
      },
      "Passport": {
        "description": "Passport document.",
        "analyzerId": "prebuilt-idDocument.passport"
      },
      "Identity_card": {
        "description": "Identity card information."
      },
      "Other": {
        "description": "Use the Other category only if a segment does not clearly fit into any of the specified categories."
      }
    }
  },
  "models": {"completion": "gpt-5.2"}
}
```

---

For more information about how sub-page segmentation is computed and when to use it, see [Classification enhancements (2026-06-01 preview)](../concepts/classifier.md#classification-enhancements-2026-06-01-preview).

## Next steps

* Learn more about [best practices for Azure Content Understanding in Foundry Tools](../concepts/best-practices.md).
* Follow the tutorial to [create a custom analyzer using REST APIs](../tutorial/create-custom-analyzer.md).
* Explore [classifier concepts](../concepts/classifier.md) for advanced scenarios.
