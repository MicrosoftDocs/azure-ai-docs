---
title: Include file
description: Include file
ms.service: azure-ai-foundry
ms.custom: build-2025
ms.topic: include
ms.date: 01/06/2026
ms.author: jburchel
reviewer: maanavdalal
author: jonburchel
ms.reviewer: maanavd
ai-usage: ai-assisted
---

## Prerequisites

- [Node.js](https://nodejs.org/en/download/) version 20 or later installed.


## Samples repository

[!INCLUDE [samples-repo](../samples-repo.md)]

Navigate to the sample for this article:

```bash
cd js/web-server-example
```

## Install packages

[!INCLUDE [project-setup](./../javascript-project-setup.md)]

## Use OpenAI SDK with Foundry Local

Copy-and-paste the following code into a JavaScript file named `app.js`:

:::code language="javascript" source="~/foundry-local-main/samples/js/web-server-example/app.js" id="complete_code":::

Reference: [Foundry Local SDK reference](../../reference/reference-sdk-current.md)
Reference: [Foundry Local REST API reference](../../reference/reference-rest.md)

Run the code using the following command:

```bash
node app.js
```

You should see a text response printed in your terminal. On the first run, Foundry Local might download execution providers and the model, which can take a few minutes.

> [!TIP]
> For a complete working sample that combines chat and audio transcription, see the [Chat + Audio sample](https://github.com/microsoft/Foundry-Local/tree/main/samples/js/chat-and-audio-foundry-local) on GitHub.
