---
title: Guardrails in Azure Content Understanding in Foundry Tools
titleSuffix: Foundry Tools
description: Learn how guardrails affect Content Understanding results, including warnings, field suppression, blocking thresholds, and annotate-only configuration.
author: PatrickFarley
ms.author: pafarley
manager: mcleans
ms.date: 09/15/2026
ai-usage: ai-assisted
ms.service: azure-content-understanding-foundry-tools
ms.topic: concept-article
---

# Guardrails in Azure Content Understanding in Foundry Tools

Azure Content Understanding in Foundry Tools uses the guardrails assigned to your Foundry model deployments to detect potentially harmful content. Depending on the configured actions and severity thresholds, detections can produce warnings, suppress field values, or prevent analysis from completing.

This article explains how to interpret those outcomes and choose between automatic blocking and annotate-only behavior. For the underlying risks, controls, and intervention points, see [Guardrails in Microsoft Foundry](../../../foundry/guardrails/guardrails-overview.md).

## Extracted content and field generation

Document analysis has two types of output:

| Output | Response properties | Effect of guardrails |
|---|---|---|
| Extracted document content | `result.contents[0].markdown`, `pages`, `paragraphs`, and other enabled extraction outputs | Source content can remain available when guardrails suppress field values. Returning this extracted content is distinct from generating new field values. |
| LLM-generated field values | `result.contents[0].fields` | Values can be empty or absent when guardrails prevent the model from generating content at or above the configured blocking threshold. |

The paths show the first content object; inspect every returned content object. Available extraction properties depend on the analyzer configuration.

When document extraction completes but guardrails suppress field output, Content Understanding retains the extracted source content and can return `Succeeded` with warnings. `Succeeded` doesn't guarantee that every requested field has a value. The field-generation restriction avoids generating harmful content beyond the severity level allowed by your guardrail.

## Warnings and errors in the analyze response

The action you configure on a model deployment's guardrail determines whether flagged content is annotated or blocked.

| Model deployment control action | Behavior and CU response handling |
|---|---|
| **Annotate** | Allows flagged content through without suppressing field values for that control. Inspect `result.warnings` for reported detections, such as `HarmfulContentDetected`. |
| **Annotate and block** | Blocks content at or above the configured threshold. Affected fields can be empty or absent while extracted document content is returned with warnings. If blocking prevents the operation from completing, inspect the top-level `error` and its nested details. |

Content below a blocking threshold can still produce warnings without being blocked. Guardrails restrictions on field generation don't mean that the original document has no value for the field.

Warnings are part of `AnalysisResult.warnings`. In the polling response from the Get Result operation, the analysis result is nested under `result`, so inspect `result.warnings`.

These warnings summarize detections; they aren't a passthrough of raw Azure OpenAI guardrail annotations. Each warning uses the `Azure.Core.Foundations.Error` structure:

| Property | Type | Description |
|---|---|---|
| `code` | string | Identifies the type of warning. |
| `message` | string | A human-readable diagnostic message. For harmful-content warnings, it can include the detected category and severity. |
| `target` | string | Identifies the affected part of the result, when provided. |
| `details` | array | Additional error objects, when provided. |
| `innererror` | object | Additional nested error information, when provided. |

Guardrail warning codes include:

| Code | Meaning |
|---|---|
| `HarmfulContentDetected` | Potentially harmful content was detected. Route the affected result to human review. This warning alone doesn't establish whether all field values are present or why a particular field is empty. |
| `HarmfulContentFiltered` | Fields were filtered because potentially harmful content was detected. Don't assume that all requested fields are present. |

Harmful-content warning messages can identify categories such as `Violence`, `Sexual`, `Hate`, or `SelfHarm`, along with a severity. Category and severity aren't separate structured properties in the warning. Use `code` and `target` for programmatic handling; don't parse `message` as a stable API contract.

Inspect warnings even when the operation status is `Succeeded`. A `HarmfulContentFiltered` warning indicates field suppression, not necessarily failure of the entire operation. If the operation status is `Failed`, inspect the top-level `error` object and its `details`, when present.

An empty or absent warnings collection isn't a safety guarantee. Check the operation status and any `error` as well as the reported warnings.

## Review warnings and empty fields

An empty or missing field can mean that the source doesn't contain the requested value, extraction didn't identify it, or guardrails suppressed the output. Don't infer the cause from the field value alone.

If `HarmfulContentDetected` appears in `result.warnings`, route the result to human review before using it in an automated workflow. Also review `HarmfulContentFiltered`, which explicitly indicates suppression. Use the warning's `target`, when provided, to locate the affected content and compare it with the retained document text or source document. A detection warning isn't proof that a particular empty field was filtered.

For workflows where false-positive blocking prevents required field extraction, consider approved annotate-only guardrails together with human review. This keeps detection warnings while avoiding suppression by those controls.

## Example guardrail warning

The following illustrative response fragment shows a successful analysis with a harmful-content warning. Other response properties are omitted.

```json
{
  "status": "Succeeded",
  "result": {
    "warnings": [
      {
        "code": "HarmfulContentDetected",
        "message": "Content of category `Violence` detected with severity `Medium`. Please use the field content with caution.",
        "target": "Result.Contents[0]"
      }
    ]
  }
}
```

**Reference**: [AnalysisResult and warnings in Get Result](/rest/api/contentunderstanding/content-analyzers/get-result?view=rest-contentunderstanding-2025-11-01&preserve-view=true#analysisresult).

## Adjust the blocking threshold

To retain automatic blocking but allow more content through, adjust the severity threshold for the relevant control in your model deployment's guardrail. For example, **Annotate and block** at **High** blocks high-severity content but allows medium-severity content through that control. Field extraction can then proceed for medium-severity content unless another control or error prevents it.

Content is blocked **at or above** the configured threshold, not below it. Allowing content below the threshold doesn't guarantee that extraction finds a value for every field. For configuration steps, see [Configure guardrails and controls in Microsoft Foundry](../../../foundry/guardrails/how-to-create-guardrails.md).

## Configure annotate-only behavior

To retain warnings without automatically suppressing field values for supported controls, apply for the required modified-guardrails approval and configure annotate-only behavior. Approval alone doesn't change the guardrail assigned to your model deployment.

> [!IMPORTANT]
> Approval is required to turn guardrails partially or fully off for completions, including using annotate-only instead of blocking for controls that require approval. Only managed customers can apply for full control through [Limited Access Review: Modified Guardrails (previously Content Filters)](https://ncv.microsoft.com/uEfCgnITdR). See the [configuration and approval guidance](../../../foundry-classic/openai/how-to/content-filters.md) for the applicable requirements.

After approval, change the guardrail assigned to the Foundry model deployment used by your analyzer:

1. In your Foundry project, select **Build**, then **Guardrails**.
1. Create a custom guardrail or edit an existing one. You can't edit Microsoft default guardrails.
1. For the relevant risks and input or output intervention points, select **Annotate** instead of **Annotate and block**.
1. Assign the guardrail to the model deployment used by your analyzer and save your changes.

For the complete procedure, see [Configure guardrails and controls in Microsoft Foundry](../../../foundry/guardrails/how-to-create-guardrails.md). That guide explains how to override existing controls and assign a guardrail to a model.

> [!NOTE]
> Annotate-only keeps detections enabled without blocking content for those controls. Content Understanding continues to report warning summaries in `result.warnings`, so your application can route flagged results to human review. This avoids field suppression by those controls, but doesn't guarantee a value for every field: source content, extraction quality, other controls, and unrelated errors still affect the result.

## Related content

- [Analyzer configuration and reference](analyzer-reference.md)
- [Model deployment options](models-deployments.md)
- [Guardrails and controls overview in Microsoft Foundry](../../../foundry/guardrails/guardrails-overview.md)
