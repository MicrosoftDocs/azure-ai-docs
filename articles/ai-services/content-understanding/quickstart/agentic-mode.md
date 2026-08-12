---
title: "Quickstart: Analyze a document with agentic mode"
titleSuffix: Foundry Tools
description: Create an Azure Content Understanding in Foundry Tools analyzer that uses agentic mode, submit a document, and retrieve structured results.
author: PatrickFarley
ms.author: paulhsu
manager: mcleans
ms.date: 07/22/2026
ai-usage: ai-assisted
ms.service: azure-content-understanding-foundry-tools
ms.topic: quickstart
ms.custom:
  - dev-focus
---

# Quickstart: Analyze a document with agentic mode

In this quickstart, you use the Azure Content Understanding in Foundry Tools REST API to create a document analyzer with agentic mode, analyze one document, and retrieve structured results. Agentic mode is useful when an answer must be built from evidence instead of extracted from a single location.

Agentic mode can connect information across a document, perform calculations, validate results, interpret complex tables or figures, and return fields that match your schema.

If you don't have an Azure subscription, [create a free account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

[!INCLUDE [preview-notice](../includes/preview-notice.md)]

> [!IMPORTANT]
> Agentic mode requires API version `2026-06-01-preview`.

## Prerequisites

* An active Azure subscription.
* A [Microsoft Foundry resource](https://portal.azure.com/#create/Microsoft.CognitiveServicesAIFoundry) in a [supported region](../language-region-support.md). To create the resource, you need the **Contributor** role or higher on the target subscription or resource group.
* A supported Foundry chat completion model deployment configured as the default completion model for your Content Understanding resource. Configure at least 400,000 tokens per minute (TPM) capacity for the deployment to help avoid 429 rate-limit errors during an agentic analysis job. For setup instructions, see [Connect your Content Understanding resource with Foundry models](../concepts/models-deployments.md).
* Your resource endpoint and key from the Azure portal.
* [cURL](https://everything.curl.dev/install/index.html).

## Create an agentic analyzer

The analyzer schema defines the structured fields that agentic mode returns. This example evaluates an invoice by calculating its line-item total and comparing that value with the reported total.

Create a file named `agentic-invoice.json` with the following content:

```json
{
  "description": "Calculate and validate totals in an invoice",
  "baseAnalyzerId": "prebuilt-document",
  "models": {
    "completion": "{your-completion-model}"
  },
  "config": {
    "workflow": "agentic"
  },
  "fieldSchema": {
    "fields": {
      "CalculatedLineItemTotal": {
        "type": "number",
        "method": "generate",
        "description": "Calculate the sum of all line-item amounts in the invoice."
      },
      "ReportedInvoiceTotal": {
        "type": "number",
        "method": "generate",
        "description": "Return the final total reported by the invoice."
      },
      "TotalsMatch": {
        "type": "boolean",
        "method": "generate",
        "description": "Return true when the calculated line-item total equals the reported invoice total. Otherwise, return false."
      },
      "ValidationSummary": {
        "type": "string",
        "method": "generate",
        "description": "Briefly explain whether the totals match and identify any discrepancy."
      }
    }
  }
}
```

The `"agentic"` request value enables agentic mode. Use `"default"`, or omit `workflow`, to let the service select a standard workflow based on the analyzer configuration.

Replace `{endpoint}`, `{key}`, and `{analyzerId}` in the following request. Then create the analyzer:

```bash
curl -i -X PUT \
  "{endpoint}/contentunderstanding/analyzers/{analyzerId}?api-version=2026-06-01-preview" \
  -H "Ocp-Apim-Subscription-Key: {key}" \
  -H "Content-Type: application/json" \
  -d @agentic-invoice.json
```

The `201 Created` response includes an `Operation-Location` header. Copy its URL, and use it to check the analyzer creation status:

```bash
curl -i -X GET "{operation-location}" \
  -H "Ocp-Apim-Subscription-Key: {key}"
```

Repeat the request until the response returns `"status": "Succeeded"`. Wait at least one second between requests.

When you retrieve the created analyzer, `config.workflow` is `"agentic.2026-06-01-preview"`. The service resolves the creation-time selector to this versioned workflow family value. The `agentic` family uses the advanced contextualization rate.

## Analyze a document

Submit one document to the analyzer. This example uses a sample invoice:

```bash
curl -i -X POST \
  "{endpoint}/contentunderstanding/analyzers/{analyzerId}:analyze?api-version=2026-06-01-preview" \
  -H "Ocp-Apim-Subscription-Key: {key}" \
  -H "Content-Type: application/json" \
  -d '{
    "inputs": [
      {
        "url": "https://github.com/Azure-Samples/azure-ai-content-understanding-python/raw/refs/heads/main/data/invoice.pdf"
      }
    ]
  }'
```

To analyze your own document, replace the sample URL with a publicly accessible URL. For example, use an Azure Storage blob URL with a shared access signature.

The `202 Accepted` response includes an `Operation-Location` header. Copy its URL, and use it to retrieve the analysis result:

```bash
curl -i -X GET "{operation-location}" \
  -H "Ocp-Apim-Subscription-Key: {key}"
```

If the returned `status` is `Running` or `NotStarted`, repeat the request after one or two seconds. When the status is `Succeeded`, find the schema-shaped output under `result.contents[].fields`. The result contains the calculated total, reported total, comparison, and validation summary defined in the analyzer schema.

Review agentic results before you use them in high-impact workflows. Agentic mode isn't a replacement for human review.


## Preview limitations

[!INCLUDE [Agentic mode preview limitations](../includes/agentic-preview-limitations.md)]



## Clean up resources

Delete the custom analyzer when you no longer need it:

```bash
curl -i -X DELETE \
  "{endpoint}/contentunderstanding/analyzers/{analyzerId}?api-version=2026-06-01-preview" \
  -H "Ocp-Apim-Subscription-Key: {key}"
```

Deleting the analyzer doesn't delete the Foundry resource or its connected model deployment.

## Related content

* [Agentic mode overview](../concepts/agentic-mode.md)
* [What is a Content Understanding analyzer?](../concepts/analyzer-reference.md)
* [Content Understanding pricing](../pricing-explainer.md)
