---
title: include file
description: include file
author: PatrickFarley
ms.author: pafarley
ms.service: azure-ai-speech
ms.topic: include
ms.date: 5/19/2025
ms.custom: include
---

If you select the **Neural** training type, you can train a voice to speak in multiple languages. The `zh-CN`, `zh-HK`, and `zh-TW` locales support bilingual training for the voice to speak both Chinese and English. Depending in part on your training data, the synthesized voice can speak English with an English native accent or English with the same accent as the training data.

> [!NOTE]
> To enable a voice in the `zh-CN` locale to speak English with the same accent as the sample data, you should upload English data to a **Contextual** training set, or choose `Chinese (Mandarin, Simplified), English bilingual` when creating a project or specify the `zh-CN (English bilingual)` locale for the training set data via REST API.
>
> In your contextual training set, include at least 100 sentences or 10 minutes of English content and do not exceed the amount of Chinese content.

The following table shows the differences among the locales:

| Speech Studio locale | REST API locale | Bilingual support |
|:------------- |:------- |:-------------------------- |
| `Chinese (Mandarin, Simplified)` | `zh-CN` |If your sample data includes English, the synthesized voice speaks English with an English native accent, instead of the same accent as the sample data, regardless of the amount of English data. |
| `Chinese (Mandarin, Simplified), English bilingual` | `zh-CN (English bilingual)` |If you want the synthesized voice to speak English with the same accent as the sample data, we recommend including over 10% English data in your training set. Otherwise, the English speaking accent might not be ideal. |
| `Chinese (Cantonese, Simplified)` |`zh-HK` | If you want to train a synthesized voice capable of speaking English with the same accent as your sample data, make sure to provide over 10% English data in your training set. Otherwise, it defaults to an English native accent. The 10% threshold is calculated based on the data accepted after successful uploading, not the data before uploading. If some uploaded English data is rejected due to defects and doesn't meet the 10% threshold, the synthesized voice defaults to an English native accent. |
| `Chinese (Taiwanese Mandarin, Traditional)` | `zh-TW` | If you want to train a synthesized voice capable of speaking English with the same accent as your sample data, make sure to provide over 10% English data in your training set. Otherwise, it defaults to an English native accent. The 10% threshold is calculated based on the data accepted after successful uploading, not the data before uploading. If some uploaded English data is rejected due to defects and doesn't meet the 10% threshold, the synthesized voice defaults to an English native accent. |