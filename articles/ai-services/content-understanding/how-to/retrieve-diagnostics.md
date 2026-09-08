---
title: Retrieve diagnostics from Azure Content Understanding in Foundry Tools
titleSuffix: Foundry Tools
description: Learn how to retrieve diagnostic information from Content Understanding analysis results by using the REST API.
author: PatrickFarley
ms.author: pafarley
manager: mcleans
ms.date: 08/27/2026
ms.service: azure-content-understanding-foundry-tools
ms.topic: how-to
ai-usage: ai-assisted
---

# Retrieve diagnostics from Azure Content Understanding in Foundry Tools

Azure Content Understanding in Foundry Tools can return optional diagnostic information about completion and embedding calls. Use these diagnostics to investigate an analysis operation's model calls and latency.

## Prerequisites

* An active Azure subscription. If you don't have an Azure account, [create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
* A [Microsoft Foundry resource](https://portal.azure.com/#create/Microsoft.CognitiveServicesAIFoundry) in a [supported region](../language-region-support.md).
* The resource endpoint and key.
* [cURL](https://everything.curl.dev/install/index.html) installed for your development environment.

## Submit an analysis request

Analysis is asynchronous. Submit the content for analysis, and then save the `Operation-Location` response header. The header contains the URL that you poll to retrieve the result.

The following request uses an analyze URL for the `prebuilt-invoice` analyzer:

```bash
curl -i -X POST "{analyze-url}" \
  -H "Ocp-Apim-Subscription-Key: {key}" \
  -H "Content-Type: application/json" \
  -d '{"inputs": [{"url": "{input-file-url}"}]}'
```

Replace the placeholders with your resource key, input file URL, and the full analyze operation URL. The analyze URL has the following format: `{endpoint}/contentunderstanding/analyzers/{analyzer-id}:analyze?api-version={api-version}`. Use `2025-11-01` for the GA behavior or `2026-06-01-preview` for the preview behavior.

**Reference**: [Content Analyzers - Analyze](/rest/api/contentunderstanding/content-analyzers/analyze?view=rest-contentunderstanding-2025-11-01&preserve-view=true)

## Retrieve diagnostic information

Poll the `Operation-Location` URL until the response status is `Succeeded`. How you request diagnostics depends on the API version.

| API version | Diagnostic behavior |
| --- | --- |
| `2025-11-01` GA | Add `x-ms-diagnostics: true` to every result retrieval request. Without the header, the response omits the `infos` property. |
| `2026-06-01-preview` | The response includes available diagnostics automatically. The header is optional and doesn't change the response. |

### Use the GA API

Add the diagnostic header to every polling `GET` request. Sending the header only on the initial `POST` request doesn't enable diagnostics on the result response.

```bash
curl -i -X GET "{operation-location}" \
  -H "Ocp-Apim-Subscription-Key: {key}" \
  -H "x-ms-diagnostics: true"
```

The accepted header value is `true`, after whitespace is removed, and isn't case-sensitive. A missing header, `false`, or another value doesn't enable GA diagnostics.

### Use the preview API

By using the `2026-06-01-preview` API, retrieve the result without the diagnostic header:

```bash
curl -i -X GET "{operation-location}" \
  -H "Ocp-Apim-Subscription-Key: {key}"
```

**Reference**: [Content Analyzers - Get Result](/rest/api/contentunderstanding/content-analyzers/get-result?view=rest-contentunderstanding-2025-11-01&preserve-view=true)

## Interpret diagnostic information

When diagnostics are available, the completed response includes the optional `result.infos` array. The current diagnostic code is `LLMStats`, which summarizes completion and embedding calls and latency.

```json
{
  "status": "Succeeded",
  "result": {
    "analyzerId": "prebuilt-invoice",
    "warnings": [],
    "infos": [
      {
        "code": "LLMStats",
        "message": "completion calls: 2; avg completion latency: 5.14s; total completion latency: 10.28s"
      }
    ],
    "contents": []
  }
}
```

The `infos` property isn't guaranteed to exist. For example, an analyzer that doesn't invoke a generative model might not produce an `LLMStats` entry.

Treat `message` as human-readable troubleshooting text, not as a stable telemetry format. When you process the response:

* Tolerate an absent or empty `infos` property.
* Handle unknown future diagnostic codes.
* Use `code` for coarse programmatic branching.
* Use OpenTelemetry or another structured telemetry source for automation.

## Related content

* [Use the Content Understanding REST API](../quickstart/use-rest-api.md)
* [Content Understanding REST API reference](/rest/api/contentunderstanding/operation-groups)
