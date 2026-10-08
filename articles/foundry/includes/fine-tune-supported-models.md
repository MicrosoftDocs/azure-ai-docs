---
title: Fine-tuning model support
titleSuffix: Microsoft Foundry
description: Compare model support for managed fine-tuning, interactive training, training types, and deployment types.
ms.author: wujohn
ms.date: 10/06/2026
ms.service: microsoft-foundry
ms.subservice: foundry-openai
ms.topic: include
ms.custom: doc-kit-assisted
ai-usage: ai-assisted
---

For supported serverless deployments, Global Standard, Data Zone Standard, and Developer are available unless a legend states otherwise. Check [Standard deployment regions](#supported-standard-deployment-regions) and [Provisioned Throughput deployment regions](#supported-provisioned-throughput-deployment-regions) for those deployment types.

| Model ID | Approach | Training types | Deployment options |
| --- | --- | --- | --- |
| `MAI-Code-1.1-Flash`<br>(preview) | Managed: ✅ (RFT)<br>Interactive: ❌ | Standard: ❌<br>Data zone: ❌<br>Global: ✅<br>Developer: ✅ | Serverless: ✅<sup>2</sup><br>Managed compute: ❌<br>Fireworks: ❌ |
| `Muse-Glimmer-30B`<br>(preview) | Managed: ✅ (SFT, RFT)<br>Interactive: ✅ | Standard: ❌<br>Data zone: ❌<br>Global: ✅<br>Developer: ✅ | Serverless: ❌<br>Managed compute: ✅<br>Fireworks: ✅<sup>1</sup> |
| `Llama-3.3-70B-Instruct` | Managed: ✅ (SFT)<br>Interactive: ❌ | Standard: ❌<br>Data zone: ✅<br>Global: ✅<br>Developer: ❌ | Serverless: ✅<sup>2</sup><br>Managed compute: ❌<br>Fireworks: ❌ |
| `Qwen3-32B` | Managed: ✅ (SFT)<br>Interactive: ❌ | Standard: ❌<br>Data zone: ✅<br>Global: ✅<br>Developer: ❌ | Serverless: ✅<sup>2</sup><br>Managed compute: ❌<br>Fireworks: ❌ |
| `Qwen3.6-35B-A3B`<br>(preview) | Managed: ✅ (SFT, RFT)<br>Interactive: ✅ | Standard: ❌<br>Data zone: ❌<br>Global: ✅<br>Developer: ✅ | Serverless: ❌<br>Managed compute: ✅<br>Fireworks: ✅<sup>1</sup> |
| `Qwen3.8-27B`<br>(preview) | Managed: ✅ (SFT, RFT)<br>Interactive: ✅ | Standard: ❌<br>Data zone: ❌<br>Global: ✅<br>Developer: ✅ | Serverless: ❌<br>Managed compute: ✅<br>Fireworks: ✅<sup>1</sup> |
| `gpt-oss-20b` | Managed: ✅ (SFT)<br>Interactive: ✅ | Standard: ❌<br>Data zone: ✅<br>Global: ✅<br>Developer: ❌ | Serverless: ✅<sup>2</sup><br>Managed compute: ❌<br>Fireworks: ❌ |
| `gpt-oss-120b`<br>(preview) | Managed: ✅ (SFT, RFT)<br>Interactive: ✅ | Standard: ❌<br>Data zone: ❌<br>Global: ✅<br>Developer: ✅ | Serverless: ❌<br>Managed compute: ✅<br>Fireworks: ✅<sup>1</sup> |
| `Ministral-3B`<br>(2411) | Managed: ✅ (SFT)<br>Interactive: ❌ | Standard: ❌<br>Data zone: ✅<br>Global: ✅<br>Developer: ❌ | Serverless: ✅<sup>2</sup><br>Managed compute: ❌<br>Fireworks: ❌ |
| `gpt-4o-mini`<br>(2024-07-18) | Managed: ✅ (SFT)<br>Interactive: ❌ | Standard: ✅<br>Data zone: ✅<br>Global: ✅<br>Developer: ✅ | Serverless: ✅<sup>5</sup><br>Managed compute: ❌<br>Fireworks: ❌ |
| `gpt-4o`<br>(2024-08-06) | Managed: ✅ (SFT, DPO)<br>Interactive: ❌ | Standard: ✅<br>Data zone: ✅<br>Global: ✅<br>Developer: ✅ | Serverless: ✅<sup>5</sup><br>Managed compute: ❌<br>Fireworks: ❌ |
| `gpt-4.1`<br>(2025-04-14) | Managed: ✅ (SFT, DPO)<br>Interactive: ❌ | Standard: ✅<br>Data zone: ✅<br>Global: ✅<br>Developer: ✅ | Serverless: ✅<br>Managed compute: ❌<br>Fireworks: ❌ |
| `gpt-4.1-mini`<br>(2025-04-14) | Managed: ✅ (SFT, DPO)<br>Interactive: ❌ | Standard: ✅<br>Data zone: ✅<br>Global: ✅<br>Developer: ✅ | Serverless: ✅<br>Managed compute: ❌<br>Fireworks: ❌ |
| `gpt-4.1-nano`<br>(2025-04-14) | Managed: ✅ (SFT, DPO)<br>Interactive: ❌ | Standard: ✅<br>Data zone: ✅<br>Global: ✅<br>Developer: ✅ | Serverless: ✅<br>Managed compute: ❌<br>Fireworks: ❌ |
| `o4-mini`<br>(2025-04-16) | Managed: ✅ (RFT)<br>Interactive: ❌ | Standard: ✅<br>Data zone: ✅<br>Global: ✅<br>Developer: ✅ | Serverless: ✅<br>Managed compute: ❌<br>Fireworks: ❌ |
| `gpt-5`<br>(2025-08-07)<sup>3</sup> | Managed: ✅ (RFT)<br>Interactive: ❌ | Standard: ✅<br>Data zone: ✅<br>Global: ✅<br>Developer: ❌ | Serverless: ✅<sup>4</sup><br>Managed compute: ❌<br>Fireworks: ❌ |
| `MedImageInsight-Premium`<br>(preview) | Managed: ✅ (SFT)<br>Interactive: ❌ | Global | Serverless: ✅<sup>2</sup><br>Managed compute: ❌<br>Fireworks: ❌ |
| `CXRReportgen-Premium`<br>(preview) | Managed: ✅ (SFT)<br>Interactive: ❌ | Global | Serverless: ✅<sup>2</sup><br>Managed compute: ❌<br>Fireworks: ❌ |

<a id="serverless-deployment-skus"></a>

**Legend**

- <sup>1</sup> Only Provisioned Throughput deployment type is supported.
- <sup>2</sup> Only Global Standard deployment type is supported.
- <sup>3</sup> GPT-5 reinforcement fine-tuning requires an invitation. Contact your Microsoft account team for enrollment.
- <sup>4</sup> Only Standard deployment type is supported. See [Standard deployment regions](#supported-standard-deployment-regions).
- <sup>5</sup> Developer deployment type is not supported.
