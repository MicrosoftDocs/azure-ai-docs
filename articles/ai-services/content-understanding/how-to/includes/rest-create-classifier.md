---
title: Create a basic classifier using the Content Understanding REST API
author: PatrickFarley
manager: mcleans
description: Create a classifier analyzer with the Content Understanding REST API.
ms.service: azure-content-understanding-foundry-tools
ms.topic: include
ms.date: 07/20/2026
ms.author: pafarley
ai-usage: ai-assisted
---

<!-- markdownlint-disable MD025 -->

Before running any of the following cURL commands, replace `{endpoint}` and `{key}` with the corresponding values from your Foundry instance in the Azure portal. The examples use `gpt-5.2`. For current model options, see [Supported generative models](../../service-limits.md#supported-generative-models).

#### Define the classifier

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
      "Loan_Application": {
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
  "models": {"completion": "gpt-5.2"}
}
```

The key fields in this definition are:

| Field | Description |
|---|---|
| `baseAnalyzerId` | The prebuilt analyzer to extend. Use `prebuilt-document` for document classification. |
| `contentCategories` | A dictionary of up to 200 category names and descriptions. |
| `enableSegment` | When `true`, automatically splits and classifies different document types within a single file. When `false`, treats the entire file as a single document. |

#### Create the classifier

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

#### Classify a document

Submit a document for classification by using the `:analyze` endpoint. Replace `{classifierId}` with the name of the classifier you created.  

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

#### Get classification results

```bash
curl -i -X GET "{Operation-Location}" \
  -H "Ocp-Apim-Subscription-Key: {key}"
```

A successful response returns `"status": "Succeeded"` with classification results in the `result` object. Each segment includes a `category`, `startPageNumber`, and `endPageNumber`.

**Reference**: [Analyzer Results - Get](/rest/api/contentunderstanding/content-analyzers/get-result?view=rest-contentunderstanding-2025-11-01&preserve-view=true)

#### Clean up

Delete the classifier when you're done.

```bash
curl -i -X DELETE "{endpoint}/contentunderstanding/analyzers/{classifierId}?api-version=2025-11-01" \
  -H "Ocp-Apim-Subscription-Key: {key}"
```
