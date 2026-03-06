---
title: Support fine-tune models
titleSuffix: Microsoft Foundry
description: Describes the models that support fine-tuning and the regions where fine-tuning is available.
ms.author: wujohn
ms.date: 03/05/2026
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: include
---
The following models are supported for fine-tuning:

|  Model ID  | Standard regions | Global | Developer | Methods | Status | Modality |
|  --- | --- | :---: | :---: | :---: | --- |
| `gpt-4o-mini` <br> (2024-07-18) | North Central US <br> Sweden Central | ✅ | ✅ | SFT | GA | Text to text |
| `gpt-4o` <br> (2024-08-06) | East US2 <br> North Central US <br> Sweden Central | ✅ | ✅ | SFT, DPO | GA | Text and vision to text |
| `gpt-4.1` <br> (2025-04-14) | North Central US <br> Sweden Central | ✅ | ✅ | SFT, DPO | GA | Text and vision to text |
| `gpt-4.1-mini` <br> (2025-04-14) | North Central US <br> Sweden Central | ✅ | ✅ | SFT, DPO | GA | Text to text |
| `gpt-4.1-nano` (2025-04-14) | North Central US <br> Sweden Central | ✅ | ✅ | SFT, DPO | GA | Text to text |
| `o4-mini` <br> (2025-04-16) | East US2 <br> Sweden Central | ✅ | ❌ | RFT | GA | Text to text |
| `gpt-5` <br> (2025-08-07) | North Central US <br> Sweden Central | ✅ | ✅ | RFT | Private preview | Text to text |
| `Ministral-3B` <br> (2411) | Not supported | ✅ | ❌ | SFT | Public preview | Text to text |
| `Qwen-32B` | Not supported | ✅ | ❌ | SFT | Public preview | Text to text |
| `Llama-3.3-70B-Instruct` | Not supported | ✅ | ❌ | SFT | Public preview | Text to text |
| `gpt-oss-20b` | Not supported | ✅ | ❌ | SFT | Public preview | Text to text |

Or you can fine-tune a previously fine-tuned model, formatted as `base-model.ft-{jobid}`.