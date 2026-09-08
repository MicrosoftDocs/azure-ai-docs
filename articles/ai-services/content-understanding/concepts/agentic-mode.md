---
title: Agentic mode overview for document analysis (preview)
titleSuffix: Foundry Tools
description: Learn when to use agentic mode in Azure Content Understanding in Foundry Tools for complex document analysis.
author: PatrickFarley
ms.author: pafarley
manager: mcleans
ms.date: 07/22/2026
ai-usage: ai-assisted
ms.service: azure-content-understanding-foundry-tools
ms.topic: concept-article
ms.custom:
  - dev-focus
---

# Agentic mode for document analysis (preview)

Agentic mode in Azure Content Understanding in Foundry Tools analyzes complex documents when an answer must be built from evidence instead of extracted from a single location. It can reason across a document, perform calculations, validate results, interpret visual information, and return structured fields that match your schema.

[!INCLUDE [preview-notice](../includes/preview-notice.md)]

> [!IMPORTANT]
> Agentic mode is available with API version `2026-06-01-preview`. The initial preview supports one input file per analysis request. The input file can contain a single document or multiple logically related documents (such as a contract, appendix, company rules, and so on).

## When to use agentic mode

Agentic mode is the most advanced Content Understanding option for your most challenging document analysis problems. If standard extraction doesn't produce the result you need, try agentic mode when additional reasoning over the data in the input file could construct a better answer. Agentic mode applies the service's highest reasoning effort to help you get the most from its AI capabilities.

Use agentic mode for document scenarios that require one or more of these capabilities:

* **Multistep reasoning**: Connect related information in different parts of a document to construct an answer.
* **Calculations**: Derive values such as totals, differences, or reconciliations that aren't stated directly.
* **Validation**: Check values for internal consistency or against conditions in your field descriptions.
* **Visual analysis**: Use information in complex tables, figures, forms, and other visual elements as part of the analysis.
* **Structured output**: Return the result as fields that conform to your analyzer schema.

For example, use agentic mode to reconcile values in a financial report, validate whether a document meets a set of requirements, or analyze how a contract and its amendments in the same file relate to each other.

Agentic mode can extract fields from a single document or reason across multiple logical documents contained in the input file.

For straightforward field extraction, use a standard document analyzer. Agentic mode isn't a replacement for human review in high-impact scenarios.

## Select agentic workflow

Set `config.workflow` when you create a document analyzer by using API version `2026-06-01-preview`:

* Use `"default"`, or omit `workflow`, to let the service select the standard or advanced workflow based on your analyzer configuration.
* Use `"agentic"` to enable agentic mode.

```jsonc
{
  "description": "Calculate and validate totals in an invoice",
  "baseAnalyzerId": "prebuilt-document",
  "models": {
    "completion": "gpt-5.2"
  },
  "config": {
    "workflow": "agentic" // Agentic workflow selector
  },
  "fieldSchema": {
    "fields": {
      ...
    }
  }
}
```

The value you send is a creation-time selector. After the analyzer is created, `config.workflow` contains a resolved, versioned value. For example, `"agentic"` resolves to `"agentic.2026-06-01-preview"`. For the resolution rules, see [`workflow`](analyzer-reference.md#workflow).

## Cost and latency

The resolved `agentic.*` workflow uses the advanced contextualization rate. Agentic mode also consumes more model tokens than a standard workflow and typically takes longer for the same document. Test with representative documents to determine whether the quality improvement meets your latency and cost requirements.

> [!NOTE]
> Agentic mode typically requires approximately 400,000 tokens per minute (TPM) per analyzer job on the Foundry model deployment. Configure at least 400,000 TPM capacity to help avoid 429 rate-limit errors.

For more information, see [Content Understanding pricing](../pricing-explainer.md).

## Preview limitations

[!INCLUDE [Agentic mode preview limitations](../includes/agentic-preview-limitations.md)]

## Migrate from pro mode

Pro mode is only available in the `2025-05-01-preview` API, which is now retired. Migrate to agentic mode in the `2026-06-01-preview` API.


Keep the following differences in mind when you migrate:

* Configure agentic mode through the `2026-06-01-preview` API by setting `config.workflow` to `"agentic"`. After creation, the service returns the resolved value `"agentic.2026-06-01-preview"`. Agentic mode isn't a drop-in replacement for the `2025-05-01-preview` pro mode configuration. Review your analyzer and field schema against the [agentic mode](agentic-mode.md) documentation before you migrate.
* The initial agentic mode preview supports one input file per analysis request. If your pro mode workflow relies on multiple input documents or reference data, confirm agentic mode supports your scenario before you migrate.



## Related content

Use these resources to learn more about analyzers, document processing, and pricing:

* [Quickstart: Analyze a document with agentic mode](../quickstart/agentic-mode.md)
* [What is a Content Understanding analyzer?](analyzer-reference.md)
* [Document processing overview](../document/overview.md)
