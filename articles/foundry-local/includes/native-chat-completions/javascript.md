---
title: Include file
description: Include file
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 01/06/2026
ms.author: samkemp
author: samuel100
ai-usage: ai-assisted
---

## Prerequisites
- [Node.js 20](https://nodejs.org/en/download/) or later installed.


## Samples repository

[!INCLUDE [samples-repo](../samples-repo.md)]

```bash
cd Foundry-Local/samples/js/native-chat-completions
```

## Install packages

[!INCLUDE [project-setup](./../javascript-project-setup.md)]

## Use native chat completions API

Copy and paste the following code into a JavaScript file named `app.js`:

:::code language="javascript" source="~/foundry-local-main/samples/js/native-chat-completions/app.js" id="complete_code":::

Run the code by using the following command:

```bash
node app.js
```