---
title: What is Azure text translation in Microsoft Foundry?
titleSuffix: Microsoft Foundry
description: Integrate the Azure Translator text translation API into your applications, websites, tools, and workflows for multilingual experiences.
author: laujan
manager: nitinme
ms.service: azure-ai-translator
ms.topic: overview
ms.date: 06/02/2026
ms.author: lajanuar
ms.custom: pilot-ai-workflow-jan-2026
ai-usage: ai-assisted
---

# What is Azure text translation in Microsoft Foundry?

Azure text translation is a cloud-based REST API for multilingual translation across more than 100 supported languages and dialects. You can integrate it into applications, services, and automation workflows to translate text in real time at production scale by using REST APIs or SDKs.

The latest generally available release is `2026-06-06`. This version introduces a revised request and response schema, adds support for model selection between standard Neural Machine Translation (NMT) and supported Large Language Models (LLMs), and expands translation controls for scenarios that require adaptive output, tone, and gender-specific variations.

Translator is designed for high-volume multilingual workloads where consistency, scalability, and operational control matter. If you're currently on v3.0, plan migration and validation before rollout because `2026-06-06` includes breaking changes.

## What's new in `2026-06-06` (GA)

API version `2026-06-06` is generally available and includes breaking changes compared to v3.0.

This release adds new translation controls and model options while updating request and response contracts. If you're migrating from v3.0, plan a full validation pass for payload shape, response parsing, and production quality checks before rollout.

>[!IMPORTANT]
>
> * Azure Translator REST API `2026-06-06` introduces breaking changes.
> * Thoroughly test your applications before migrating production workloads from v3.0.
> * Validate code paths and internal workflows, and restrict production use to versions you have fully tested.

Key updates in `2026-06-06` include:

* **Revised request and response JSON schema**. The request array uses `inputs`, and the response array uses `value`. For an end-to-end example, see [REST API guide](2026-06-06/rest-api-guide.md#rest-api-code-sample-translate).
* **Model choice (NMT or LLM)**. You can select standard NMT or an LLM deployment (for example, GPT-5.1) based on quality, cost, and scenario requirements. Using LLM-based translation requires a Microsoft Foundry resource. For setup guidance, see [Create Translator resources](../how-to/create-translator-resource.md).
* **Adaptive custom translation**. You can provide up to five reference translations or an adaptive dataset index ID to influence LLM output style and terminology. For more information, see [Adaptive custom translation](../custom-translator/azure-ai-foundry/concepts/adaptive-custom-translation.md).
* **Tone and gender controls**. LLM-based translation supports tone variants (formal, informal, neutral) and gender-specific output controls.

## Core operations

The `2026-06-06` API includes the following primary operations:

These operations cover the most common runtime needs for text localization pipelines: discovering supported languages, translating text at scale, and transliterating scripts for language pairs that require script conversion.

* [**Languages**](2026-06-06/get-languages.md): Returns supported languages for translation operations. This request does not require authentication.

  ```bash
  https://api.cognitive.microsofttranslator.com/languages?api-version=2026-06-06
  ```

* [**Translate**](2026-06-06/translate-api.md): Translates source text to one or more target languages in a single `POST` request.
* [**Transliterate**](2026-06-06/transliterate-api.md): Converts script or character sets from one writing system to another.

For a complete request walkthrough, see [REST API guide](2026-06-06/rest-api-guide.md).

## Development options

Use the following options to build and deploy multilingual text translation solutions in your applications and workflows:

Choose your integration path based on how much control and automation you need. Most production systems use direct REST API or SDK integration, while portal workflows can be useful for setup, testing, and operational troubleshooting.

| Development option | Description |
| --- | --- |
| **Microsoft Foundry portal** | Use [Microsoft Foundry](https://ai.azure.com/) to manage projects, models, and related AI resources. |
| **REST API** | Integrate directly with [text translation REST APIs](2026-06-06/rest-api-guide.md). |
| **Client libraries (SDKs)** | Build with supported SDKs using [client library quickstarts](quickstart/client-library-sdk.md). |
| **Docker container** | Use the Translator container for supported disconnected or controlled scenarios. Start with [Container: translate text](../containers/translate-text-parameters.md). |

## Authentication

All text translation requests require authentication headers. For production deployments, choose an approach that matches your security and operations model. Resource keys are simple to start with, while Microsoft Entra ID is typically preferred for enterprise environments that require centralized identity and keyless access.

| Method | Description |
| --- | --- |
| **Resource key** | Pass `Ocp-Apim-Subscription-Key` from your Translator resource. |
| **Bearer token** | Obtain a time-limited token and send it in the `Authorization` header. |
| **Microsoft Entra ID** | Use managed identities or service principals for keyless authentication. |

For required headers and endpoint-specific examples, see [Authentication and authorization](reference/authentication.md).

## Endpoints and data residency

Requests are typically processed in the nearest available datacenter when you use the global endpoint. To constrain processing geography, use a regional endpoint.

Endpoint selection affects latency, geography, and regulatory posture. Use the global endpoint for broad availability and automatic routing, or use a regional endpoint when your architecture requires processing to remain within a specific geography.

| Service endpoint | Request processing data center |
| --- | --- |
| **Global (recommended):**<br>**`api.cognitive.microsofttranslator.com`** | Closest available data center. |
| **Americas:**<br>**`api-nam.cognitive.microsofttranslator.com`** | East US 2, West US 2 |
| **Asia Pacific:**<br>**`api-apc.cognitive.microsofttranslator.com`** | Japan East, Southeast Asia |
| **Europe (except Switzerland):**<br>**`api-eur.cognitive.microsofttranslator.com`** | France Central, West Europe |
| **Switzerland:**<br>See [Switzerland service endpoints](#switzerland-service-endpoints). | Switzerland North, Switzerland West |

### Switzerland service endpoints

If your Translator resource is deployed in `Switzerland North` or `Switzerland West`, you can keep text translation processing in Switzerland by using the resource-specific custom endpoint.

This configuration is useful for workloads with stricter geographic processing requirements. Ensure your Translator resource region and request endpoint remain aligned so requests are routed within Switzerland.

Example request:

```bash
curl -X POST "https://my-swiss-n.cognitiveservices.azure.com/translator/text/v3.0/translate?to=fr" \
  -H "Ocp-Apim-Subscription-Key: ${TRANSLATOR_KEY}" \
  -H "Ocp-Apim-Subscription-Region: switzerlandnorth" \
  -H "Content-Type: application/json" \
  -d "[{\"Text\":\"Hello\"}]"
```

Custom Translator is not currently available in Switzerland.

## LLM processing, limits, and pricing

When you deploy an LLM, your deployment configuration (global, data zone, or regional) determines where LLM translation data is processed.

For mixed NMT and LLM deployments, treat model routing, limits, and cost as part of your runtime design. Throughput and payload sizing differ between NMT and LLM paths, so baseline both latency and cost before scaling traffic.

### Service limits

| Operation | Maximum number of array elements | Maximum size of array element | LLM maximum number of array elements | LLM maximum size of array element |
| --- | --- | --- | --- | --- |
| Translate | 1,000 | 50,000 | 50 | 5,000 |

For broader quotas and limits, see [Service limits - Translator](../service-limits.md#text-translation).

### Pricing

* NMT translation is billed by source-text characters. See [Azure Translator pricing](https://azure.microsoft.com/pricing/details/cognitive-services/translator-text-api/).
* LLM translation is billed by processed input and output tokens. See [Azure OpenAI pricing](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/).

If you support multiple traffic tiers, define routing rules that reserve LLM use for scenarios that require adaptive behavior, tone control, or richer contextual handling, and keep high-volume baseline traffic on NMT where appropriate.

## Troubleshooting

If a request fails, start with the HTTP status and the service error code.

In production systems, the fastest way to isolate issues is to log request IDs, endpoint, region, API version, and key headers with each failed call. This context helps distinguish authentication, quota, payload, and feature-availability failures.

| Symptom | Likely cause | Resolution |
| --- | --- | --- |
| `401 Unauthorized` | Missing or invalid subscription key. | Verify `Ocp-Apim-Subscription-Key` and resource association. |
| `403 Forbidden` | Valid credentials but unsupported operation or configuration. | Confirm region, resource type, and feature availability. |
| `429 Too Many Requests` | Rate or quota exceeded. | Reduce request rate and review [service limits](../service-limits.md#text-translation). |
| `400 Bad Request` | Invalid payload or unsupported language value. | Validate request JSON and [supported languages](../language-support.md). |

For detailed codes, see [Response codes and messages](reference/status-response-codes.md).

## Get started

Use this sequence to move from provisioning to your first validated translation workflow. Keep test payloads small at first, then scale request size and concurrency after you validate authentication, endpoint routing, and response handling.

1. [Create a Translator resource](../how-to/create-translator-resource.md).
1. [Get access keys and endpoint URL](../how-to/create-translator-resource.md#authentication-keys-and-endpoint-url).
1. Run the [text translation quickstart](quickstart/rest-api.md) in your preferred language:
   * [C#/.NET](quickstart/rest-api.md?tabs=csharp)
   * [Go](quickstart/rest-api.md?tabs=go)
   * [Java](quickstart/rest-api.md?tabs=java)
   * [JavaScript/Node.js](quickstart/rest-api.md?tabs=nodejs)
   * [Python](quickstart/rest-api.md?tabs=python)

## Related content

* [Translate API reference (`2026-06-06`)](2026-06-06/translate-api.md)
* [Migration guide (`2026-06-06`)](how-to/migrate-to-2026-06-06.md)
* [Adaptive custom translation](../custom-translator/azure-ai-foundry/concepts/adaptive-custom-translation.md)