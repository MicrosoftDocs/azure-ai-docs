---
title: "Quickstart: Analyze a document with agentic mode"
titleSuffix: Foundry Tools
description: Use Content Understanding Studio or the REST API to create an Azure Content Understanding in Foundry Tools agentic analyzer and analyze a document.
author: PatrickFarley
ms.author: paulhsu
manager: mcleans
ms.date: 09/16/2026
ai-usage: ai-assisted
ms.service: azure-content-understanding-foundry-tools
ms.topic: quickstart
ms.custom:
  - dev-focus
---

# Quickstart: Analyze a document with agentic mode

In this quickstart, you create an agentic mode document analyzer in Azure Content Understanding, analyze one document, and review structured results. Choose Content Understanding Studio for a browser-based walkthrough or the REST API for a code-based workflow.

Agentic mode connects information across a document, performs calculations, and returns fields that match your schema. Use it when an answer requires reasoning over evidence instead of extraction from a single location. Agentic mode requires API version `2026-06-01-preview`.
For more information, see the [Agentic mode overview](../concepts/agentic-mode.md).

[!INCLUDE [preview-notice](../includes/preview-notice.md)]

## Prerequisites

#### [Content Understanding Studio](#tab/cu-studio)

* An active Azure subscription. If you don't have an Azure subscription, [create a free account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
* A [Microsoft Foundry resource](https://portal.azure.com/#create/Microsoft.CognitiveServicesAIFoundry) in a [supported region](../language-region-support.md). To create the resource, you need the **Contributor** role or higher on the target subscription or resource group.
* A supported Foundry chat completion model deployment configured as the default completion model for your Content Understanding resource. Configure at least 400,000 tokens per minute (TPM) capacity for the deployment to help avoid 429 rate-limit errors during an agentic analysis job. For setup instructions, see [Connect your Content Understanding resource with Foundry models](../concepts/models-deployments.md).
* A storage account and blob container for your Studio project.

Connect your Foundry resource to Content Understanding Studio before you create the project:

[!INCLUDE [Studio model deployment setup](../includes/foundry-model-deployment-setup-studio.md)]

#### [REST API](#tab/rest-api)

* An active Azure subscription. If you don't have an Azure subscription, [create a free account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
* A [Microsoft Foundry resource](https://portal.azure.com/#create/Microsoft.CognitiveServicesAIFoundry) in a [supported region](../language-region-support.md). To create the resource, you need the **Contributor** role or higher on the target subscription or resource group.
* A supported Foundry chat completion model deployment configured as the default completion model for your Content Understanding resource. Configure at least 400,000 tokens per minute (TPM) capacity for the deployment to help avoid 429 rate-limit errors during an agentic analysis job. For setup instructions, see [Connect your Content Understanding resource with Foundry models](../concepts/models-deployments.md).
* Your resource endpoint and key from the Azure portal.
* [cURL](https://everything.curl.dev/install/index.html).

---

## Create an agentic analyzer

#### [Content Understanding Studio](#tab/cu-studio)

Create an agentic project, and then define the fields you want to return. This example summarizes the parties, dates, renewal terms, and obligations in a contract.

### Create a project

1. Open [Content Understanding Studio](https://aka.ms/cu-studio) and sign in with your Azure account.
1. Select **Build**, open **Project list**, and select **Create**.
1. In **Create a new project**, enter `agentic-contracts` for **Project name**.
1. For **API version**, select **2026-06-01 (Preview)**.
1. Under **Workflow kind**, select **Agentic Extraction**.

    :::image type="content" source="../media/quickstarts/agentic-mode-select-workflow.png" alt-text="Screenshot of Content Understanding Studio with the project list behind the new project dialog and Agentic Extraction selected for agentic-contracts." lightbox="../media/quickstarts/agentic-mode-select-workflow.png" :::

1. Select **Create**.

### Define the contract schema

The schema describes the answers you want, including instructions for combining clauses and handling missing information. Use **Generate** for each field in this example. The agentic preview doesn't support **Extract** fields yet.

1. Download the [sample web hosting agreement (`contract.png`)](https://github.com/Azure-Samples/document-intelligence-code-samples/blob/main/Data/contract/contract.png) from GitHub, or use your own contract document.
2. In Studio, select **Browse for files** and upload the contract.
3. Download the [contract field schema](https://github.com/Azure-Samples/document-intelligence-code-samples/blob/main/Data/contract/agentic-contracts-schema.json) from GitHub and save it as **agentic-contracts-schema.json**.
4. On the **Schema** tab, select **Import**, choose the downloaded JSON file, and open it.
5. Review the imported imported **Field definitions**

    | Field name | Value type | Method | Field description |
    |---|---|---|---|
    | `Parties` | String | Generate | List the legal names of the contracting parties and their roles. Use only information in the contract. |
    | `EffectiveDate` | Date | Generate | Return the date the contract takes effect. Distinguish it from signature dates. Return null if the effective date can't be determined from the contract. |
    | `TerminationNoticeDays` | Number | Generate | Return the number of calendar days of notice required for termination without cause. Return null if the contract doesn't specify one unambiguous calendar-day notice period. |
    | `RenewalSummary` | String | Generate | Summarize the renewal terms, including whether renewal is automatic, the renewal period, and any notice deadline. If renewal terms aren't stated, say so. |
    | `ObligationsSummary` | String | Generate | Summarize each party's main obligations, combining relevant clauses across the contract. Include stated deadlines and conditions. Don't infer obligations that aren't stated. |

1. Select **Save** to save the imported schema. You can edit the field descriptions to adapt the schema to your contract.

    :::image type="content" source="../media/quickstarts/agentic-mode-contract-schema.png" alt-text="Screenshot of the agentic-contracts project with a sample contract and five saved schema fields that use the Generate method." lightbox="../media/quickstarts/agentic-mode-contract-schema.png" :::

#### [REST API](#tab/rest-api)

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

Replace `{your-completion-model}` with the catalog name of your supported completion model, not its deployment name.

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

---

## Analyze a document

#### [Content Understanding Studio](#tab/cu-studio)

Run the schema against your contract and check the generated answers against the document.

1. Select the uploaded contract, select the **Test** tab, and then select **Run analysis**. Agentic analysis can take a few minutes.
1. When analysis finishes, open **Test** > **Fields**. Check the parties and effective date against the contract. Compare the renewal and obligation summaries with the relevant clauses.

    :::image type="content" source="../media/quickstarts/agentic-mode-contract-results.png" alt-text="Screenshot of the Test tab showing generated contract fields, including the effective date and a termination notice period marked Not found." lightbox="../media/quickstarts/agentic-mode-contract-results.png" :::

1. Select **Result** to inspect the JSON response and token usage.
1. If a field is incorrect or incomplete, refine its description on the **Schema** tab, select **Save**, and run analysis again.

Each analysis run incurs Content Understanding and model usage charges. For details, see [Content Understanding pricing](../pricing-explainer.md).

To use the analyzer in an application, select **Build analyzer** after reviewing the results. For the remaining build and integration steps, see [Create and improve your custom analyzer in Content Understanding Studio](../how-to/customize-analyzer-content-understanding-studio.md#create-your-custom-analyzer).

#### [REST API](#tab/rest-api)

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

---

Review agentic results before you use them in high-impact workflows. Agentic mode isn't a replacement for human review.

## Preview limitations

[!INCLUDE [Agentic mode preview limitations](../includes/agentic-preview-limitations.md)]

## Related content

* [Agentic mode overview](../concepts/agentic-mode.md)
* [What is a Content Understanding analyzer?](../concepts/analyzer-reference.md)
* [Content Understanding pricing](../pricing-explainer.md)
