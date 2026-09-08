---
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: include
ms.date: 09/02/2026
ai-usage: ai-assisted
---

Starting with the `2026-08-01-preview` API version, automatic per-language analyzers are available for blob, indexed OneLake, and indexed SharePoint knowledge sources. When enabled, Azure AI Search detects each source document's language and automatically applies a matching Microsoft language analyzer. You don't specify an analyzer in the knowledge source definition or in a query.

To enable automatic per-language analyzers, set `contentExtractionMode` to `minimal` and configure `ingestionParameters.aiServices` in the knowledge source definition.

For keyless authentication, omit `aiServices.apiKey` and assign the **Cognitive Services User** role on your Microsoft Foundry resource to the managed identity of your search service. For key-based authentication, set `aiServices.apiKey` to a valid key for your Foundry resource.

The following languages are supported:

+ English
+ Japanese
+ French
+ Spanish
+ German
+ Dutch
+ Italian
+ Brazilian Portuguese
+ European Portuguese
+ Simplified Chinese
+ Traditional Chinese
+ Korean

For multilingual content, Azure AI Search selects an analyzer based on the predominant detected language. It uses the standard analyzer when the language is unsupported or uncertain.

When you enable automatic per-language analyzers, Azure AI Search adds language-specific content fields for every supported language to the generated index schema, whether or not your data contains documents in those languages. During ingestion, documents are routed to the appropriate language-specific field based on their detected language.

Unused language fields don't contain indexed content and have minimal storage impact, but they remain part of the index schema and count toward the index field limit. Consider the additional fields when you plan your index design, field count, and storage requirements. For more information, see [Index limits](../../search-limits-quotas-capacity.md#index-limits) and [Estimate and manage capacity of a search service](../../search-capacity-planning.md).

Language detection is billable after the free AI enrichment allocation. For more information, see [Free enrichments](../../cognitive-search-attach-cognitive-services.md#free-enrichments).