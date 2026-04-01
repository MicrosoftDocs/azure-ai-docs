---
title: Classify and route your data using Content Understanding
titleSuffix: Foundry Tools
description: Learn how to create classification workflows to categorize and route your data using Content Understanding Studio or the REST API.
author: PatrickFarley 
ms.author: pafarley
manager: nitinme
ms.date: 01/29/2026
ai-usage: ai-assisted
ms.service: azure-ai-content-understanding
ms.topic: how-to
ms.custom:
  - ignite-2024-understanding-release
  - references_regions
  - ignite-2025
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
* [cURL](https://everything.curl.dev/install/index.html) installed for your dev environment (for the REST API tab).

## Step 1: Create a basic classifier

A basic classifier categorizes documents into custom content categories. You define the categories with names and descriptions, and the service uses those definitions to classify your input files. The `enableSegment` parameter controls whether the classifier splits multi-document files into segments or treats the entire file as a single document.

# [Content Understanding Studio](#tab/studio)

### Sign in to Content Understanding Studio

Go to the [Content Understanding Studio portal](https://aka.ms/cu-studio) and sign in with your credentials. If you're familiar with the classic Azure Document Intelligence in Foundry Tools Studio experience, Content Understanding extends the same content and field extraction across all modalities—document, image, video, and audio. Select the option to try the new Content Understanding experience to access multimodal capabilities.

### Create a classifier project

1. **Start with a new project**: Select **Create project** on the home page.

1. **Select your project type**: Select the option to `Classify and route with custom categories`.

1. **Upload your data**: Upload a piece of sample data to get started with classifying.

1. **Create routing rules**: Under the **Routing rules** tab, select `Add category`. Give the category a name and description. For a basic classifier, you can skip assigning a specific analyzer to each category.

1. **Test your classification workflow**: When your custom routing rules are ready for testing, select **Run analysis** to see the output of the rules on your data.

    :::image type="content" source="../media/quickstarts/classify-test.png" lightbox="../media/quickstarts/classify-test.png" alt-text="Screenshot of Content Understanding Studio with the Test button highlighted.":::

1. **Build your classification analyzer**: When you're satisfied with the output, select the **Build analyzer** button at the top of the page. Give the analyzer a name and select **Save**.

# [REST API](#tab/rest-api)

Before running any of the following cURL commands, replace `{endpoint}` and `{key}` with the corresponding values from your Foundry instance in the Azure portal.

### Define the classifier

Define `contentCategories` within the analyzer configuration. Each category has a name and description that the service uses to classify your input files.

Create a JSON file named `classifier.json` with the following content:

```json
{
  "baseAnalyzerId": "prebuilt-document",
  "description": "Custom classifier for document categorization",
  "config": {
    "returnDetails": true,
    "enableSegment": true,
    "contentCategories": {
      "Loan application": {
        "description": "Documents submitted by individuals or businesses to request funding, typically including personal or business details, financial history, loan amount, purpose, and supporting documentation."
      },
      "Invoice": {
        "description": "Billing documents issued by sellers or service providers to request payment for goods or services, detailing items, prices, taxes, totals, and payment terms."
      },
      "Bank_Statement": {
        "description": "Official statements issued by banks that summarize account activity over a period, including deposits, withdrawals, fees, and balances."
      }
    }
  },
  "models": {"completion": "gpt-4.1"}
}
```

The key fields in this definition are:

| Field | Description |
|---|---|
| `baseAnalyzerId` | The prebuilt analyzer to extend. Use `prebuilt-document` for document classification. |
| `contentCategories` | A dictionary of up to 200 category names and descriptions. |
| `enableSegment` | When `true`, automatically splits and classifies different document types within a single file. When `false`, treats the entire file as a single document. |

### Create the classifier

Use a `PUT` request to create the classifier analyzer.

```bash
curl -i -X PUT "{endpoint}/contentunderstanding/analyzers/{classifierId}?api-version=2025-11-01" \
  -H "Ocp-Apim-Subscription-Key: {key}" \
  -H "Content-Type: application/json" \
  -d @classifier.json
```

The `201 Created` response includes an `Operation-Location` header with a URL that you can use to track the status of the asynchronous creation operation.

```
201 Created
Operation-Location: {endpoint}/contentunderstanding/analyzers/{classifierId}/operations/{operationId}?api-version=2025-11-01
```

When the operation finishes, an HTTP GET on the operation location URL returns `"status": "succeeded"`.

```bash
curl -i -X GET "{endpoint}/contentunderstanding/analyzers/{classifierId}/operations/{operationId}?api-version=2025-11-01" \
  -H "Ocp-Apim-Subscription-Key: {key}"
```

**Reference**: [Content Analyzers - Create or Replace](/rest/api/contentunderstanding/content-analyzers/create-or-replace?view=rest-contentunderstanding-2025-11-01&preserve-view=true)

### Classify a document

Submit a document for classification using the `:analyze` endpoint. Replace `{classifierId}` with the name of the classifier you created.

```bash
curl -i -X POST "{endpoint}/contentunderstanding/analyzers/{classifierId}:analyze?api-version=2025-11-01" \
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

The response includes an `Operation-Location` header. Use that URL to retrieve the analysis results.

### Get classification results

```bash
curl -i -X GET "{Operation-Location}" \
  -H "Ocp-Apim-Subscription-Key: {key}"
```

A successful response returns `"status": "Succeeded"` with classification results in the `result` object. Each segment includes a `category`, `startPageNumber`, and `endPageNumber`.

**Reference**: [Analyzer Results - Get](/rest/api/contentunderstanding/content-analyzers/get-result?view=rest-contentunderstanding-2025-11-01&preserve-view=true)

### Clean up

Delete the classifier when you're done.

```bash
curl -i -X DELETE "{endpoint}/contentunderstanding/analyzers/{classifierId}?api-version=2025-11-01" \
  -H "Ocp-Apim-Subscription-Key: {key}"
```

---

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
  "models": {"completion": "gpt-4.1"}
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
      "Loan application": {
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
  "models": {"completion": "gpt-4.1"}
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

## Next steps

* Learn more about [best practices for Azure Content Understanding in Foundry Tools](../concepts/best-practices.md).
* Follow the tutorial to [create a custom analyzer using REST APIs](../tutorial/create-custom-analyzer.md).
* Explore [classifier concepts](../concepts/classifier.md) for advanced scenarios.
