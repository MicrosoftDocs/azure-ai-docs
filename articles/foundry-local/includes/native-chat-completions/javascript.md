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

Navigate to the sample for this article:

```bash
cd js/native-chat-completions
```

## Install packages

[!INCLUDE [project-setup](./../javascript-project-setup.md)]

## Use native chat completions API

The following example demonstrates how to use the native chat completions API in Foundry Local. The benefit of using the native chat completions API is there's no need for a REST web server running and therefore it provides a simplified deployment. The code includes the following steps:

1. Initializes a `FoundryLocalManager` instance with a configuration.
1. Gets a `Model` object from the model catalog using an alias.
1. Downloads and loads the model variant.
1. Uses the native chat completions API to generate a response.
1. Unloads the model.

Copy and paste the following code into a JavaScript file named `app.js`:

:::code language="javascript" source="~/foundry-local-main/samples/js/native-chat-completions/app.js" id="complete_code":::

## Run the code

Run the code by using the following command:

```bash
node app.js
```