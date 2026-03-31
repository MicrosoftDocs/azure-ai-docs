---
title: Include file
description: Include file
ms.service: azure-ai-foundry
ms.custom: build-2025
ms.topic: include
ms.date: 05/02/2025
ms.author: jburchel
ms.reviewer: maanavd
reviewer: maanavdalal
author: jonburchel
ai-usage: ai-assisted
---

## Prerequisites

Before starting this tutorial, you need:

- **Node.js 20 or later** installed on your computer. You can download Node.js from the [official website](https://nodejs.org/).


## Samples repository

[!INCLUDE [samples-repo](../samples-repo.md)]

Navigate to the sample for this article:

```bash
cd js/langchain-integration-example
```

## Install packages

[!INCLUDE [project-setup](../javascript-project-setup.md)]

### Install LangChain packages

You also need to install the following Node.js packages:

```bash
npm install @langchain/openai @langchain/core
```

## Create a translation application

Create a new JavaScript file named `translation_app.js` in your favorite IDE and add the following code:

:::code language="javascript" source="~/foundry-local-main/samples/js/langchain-integration-example/app.js" id="complete_code":::

#To run the application, open a terminal and navigate to the directory where you saved the `translation_app.js` file. Then, run the following command:

```bash
node translation_app.js
```

You're done when you see a `Response:` line with the translated text.

You should see output similar to:

```text
Translating 'I love to code.' to French...
Response: J'aime le coder
```
