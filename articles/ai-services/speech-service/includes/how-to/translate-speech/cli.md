---
author: PatrickFarley
ms.service: azure-ai-speech
ms.topic: include
ms.date: 1/21/2024
ms.author: pafarley
---

[!INCLUDE [Introduction](intro.md)]

## Prerequisites

[!INCLUDE [Prerequisites](../../common/azure-prerequisites.md)]

## Download and install

[!INCLUDE [SPX Setup](../../spx-setup-quick.md)]

## Set source and target languages

This command calls the Speech CLI to translate speech from the microphone from Italian to French:

```shell
spx translate --microphone --source it-IT --target fr
```
