---
title: "Region availability overview"
description: "Details about region availability of AACS and Guardrails"
author: ssalgadodev
ms.date: 09/09/2026
ms.topic: include
ms.author: ssalgado
ai-usage: ai-assisted
---
## Guardrails in Foundry
Microsoft Foundry supports global, data zone, and regional deployments to meet different compliance requirements. Guardrails follow the model or agent deployment configuration: regional deployments keep Guardrails processing in-region, while global deployments use global processing. Some features are available only with global or data zone deployments.

#### Availability for Guardrails in Microsoft Foundry


# [Americas](#tab/foundry-americas)

| **Guardrail** | **brazilsouth** | **canadacentral** | **canadaeast** | **centralus** | **eastus** | **eastus2** | **northcentralus** | **southcentralus** | **westus** | **westus3** |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| Content harms | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Prompt shields | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Protected material | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Groundedness | - | - | ✅ | - | ✅ | ✅ | - | - | ✅ | - |
| Task Adherence* | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Content provenance detection | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Blocklists | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| PII | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

# [Europe](#tab/foundry-europe)

| **Guardrail** | **francecentral** | **germanywestcentral** | **italynorth** | **norwayeast** | **polandcentral** | **spaincentral** | **swedencentral** | **switzerlandnorth** | **switzerlandwest** | **uksouth** | **westeurope** |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| Content harms | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Prompt shields | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Protected material | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Groundedness | - | - | - | - | - | - | ✅ | - | - | ✅ | - |
| Task Adherence* | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Content provenance detection | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Blocklists | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| PII | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

# [Asia Pacific](#tab/foundry-apac)

| **Guardrail** | **australiaeast** | **japaneast** | **koreacentral** | **southeastasia** | **southindia** |
| :--- | :--- | :---: | :---: | :---: | :---: |
| Content harms | ✅ | ✅ | ✅ | ✅ | ✅ |
| Prompt shields | ✅ | ✅ | ✅ | ✅ | ✅ |
| Protected material | ✅ | ✅ | ✅ | ✅ | ✅ |
| Groundedness | - | - | - | - | - |
| Task Adherence* | ✅ | ✅ | ✅ | ✅ | ✅ |
| Content provenance detection | ✅ | ✅ | ✅ | ✅ | ✅ |
| Blocklists | ✅ | ✅ | ✅ | ✅ | ✅ |
| PII | ✅ | ✅ | ✅ | ✅ | ✅ |

# [Middle East & Africa](#tab/foundry-mea)

| **Guardrail** | **southafricanorth** | **uaenorth** |
| :--- | :---: | :---: |
| Content harms | ✅ | ✅ |
| Prompt shields | ✅ | ✅ |
| Protected material | ✅ | ✅ |
| Groundedness | - | - |
| Task Adherence* | ✅ | ✅ |
| Content provenance detection | ✅ | ✅ |
| Block lists | ✅ | ✅ |
| PII | ✅ | ✅ |

--- 

*Only available in Global, US Datazone, and EU Datazone deployments.

## Guardrails in Azure AI Content Safety
When you use Azure AI Content Safety directly, create the resource in the region where you want data processed. Features that support regional processing remain within that region. Some features require global or data zone routing. Although you can enable them in any supported Azure AI Content Safety region, customer data might be routed to and processed outside the resource’s region.

#### Availability for guardrails in Azure AI Content Safety

# [Americas](#tab/acs-americas)

| **Guardrail** | **brazilsouth** | **canadacentral** | **canadaeast** | **centralus** | **eastus** | **eastus2** | **northcentralus** | **southcentralus** | **westus** | **westus2** | **westus3** |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| Content harms | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Prompt shields | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Protected material | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Groundedness | - | - | ✅ | - | ✅ | ✅ | - | - | ✅ | - | - |
| Task Adherence* | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Content provenance detection | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Blocklists | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| PII | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

# [Europe](#tab/acs-europe)

| **Guardrail** | **francecentral** | **germanywestcentral** | **italynorth** | **polandcentral** | **spaincentral** | **swedencentral** | **switzerlandnorth** | **switzerlandwest** | **uksouth** | **westeurope** |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| Content harms | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Prompt shields | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Protected material | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Groundedness | - | - | - | - | - | ✅ | - | - | ✅ | - |
| Task Adherence* | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Content provenance detection | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Blocklists | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| PII | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

# [Asia Pacific](#tab/acs-apac)

| **Guardrail** | **australiaeast** | **japaneast** | **koreacentral** | **southeastasia** | **southindia** |
| :--- | :--- | :---: | :---: | :---: | :---: |
| Content harms | ✅ | ✅ | ✅ | ✅ | ✅ |
| Prompt shields | ✅ | ✅ | ✅ | ✅ | ✅ |
| Protected material | ✅ | ✅ | ✅ | ✅ | ✅ |
| Groundedness | - | - | - | - | - |
| Task Adherence* | ✅ | ✅ | ✅ | ✅ | ✅ |
| Content provenance detection | ✅ | ✅ | ✅ | ✅ | ✅ |
| Blocklists | ✅ | ✅ | ✅ | ✅ | ✅ |
| PII | ✅ | ✅ | ✅ | ✅ | ✅ |

# [Middle East & Africa](#tab/acs-mea)

| **Guardrail** | **southafricanorth** | **uaenorth** |
| :--- | :---: | :---: |
| Content harms | ✅ | ✅ |
| Prompt shields | ✅ | ✅ |
| Protected material | ✅ | ✅ |
| Groundedness | - | - |
| Task Adherence* | ✅ | ✅ |
| Content provenance detection | ✅ | ✅ |
| Block lists | ✅ | ✅ |
| PII | ✅ | ✅ |

*Not available for in-region, global routing is used

---

## Service limits

### Input limits for Guardrails in Foundry
The first 1000 characters for text scenarios will be moderated using Guardrails.

### Input limits for Azure AI Content Safety

See the following list for the input requirements for each feature.

- **Analyze text API**: 
  - Default maximum length: 10K characters (split longer texts as needed).
- **Analyze image API**: 
  - Maximum image file size: 4 MB
  - Dimensions between 50 x 50 and 7200 x 7,200 pixels.
  - Images can be in JPEG, PNG, GIF, BMP, TIFF, or WEBP formats.
- **Analyze multimodal API (preview)**:
  - Default maximum text length: 1K characters.
  - Maximum image file size: 4 MB
  - Dimensions between 50 x 50 and 7200 x 7,200 pixels.
  - Images can be in JPEG, PNG, GIF, BMP, TIFF, or WEBP formats.
- **Prompt Shields API**: 
  - Maximum prompt length: 10K characters.
  - Up to five documents with a total of 10K characters.
- **Groundedness detection API (preview)**: 
  - Maximum length for grounding sources: 55,000 characters (per API call).
  - Maximum text and query length: 7,500 characters.
  - Minimum query length: 3 words.
- **Protected material detection APIs**: 
  - Default maximum length: 10K characters.
  - Default minimum length: 110 characters (for scanning LLM completions, not user prompts).
- **Custom categories (standard) API (preview)**:
  - Maximum inference input length: 1K characters.
- **Task adherence (preview)**:
  - Maximum input length: 100K characters.


## Language availability
The Azure AI Content Safety features for content harms were trained and tested on the following languages: Chinese, English, French, German, Spanish, Italian, Japanese, and Portuguese. You tested prompt shields, protected material, groundedness detection, task adherence, and custom categories (standard) with English only. However, these features can work in many other languages, but the quality might vary. In all cases, you should do your own testing to ensure that it works for your application.
