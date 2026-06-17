---
title: Include file
description: Include file
ms.service: microsoft-foundry
ms.topic: include
ms.date: 04/24/2026
ms.author: natke
author: natke
ai-usage: ai-assisted
---

## Prerequisites

- [Node.js 20](https://nodejs.org/en/download/) or later installed.


## Samples repository

The complete sample code for this article is available in the [foundry-samples GitHub repository](https://github.com/microsoft-foundry/foundry-samples). To clone the repository and navigate to the sample use:

```bash
git clone https://github.com/microsoft-foundry/foundry-samples.git
cd foundry-samples/samples/javascript/foundry-local/embeddings
```

## Install packages

[!INCLUDE [project-setup](./../javascript-project-setup.md)]

## Generate text embeddings

Copy and paste the following code into a JavaScript file named `app.js`:

:::code language="javascript" source="~/foundry-local-main/samples/javascript/foundry-local/embeddings/app.js" id="complete_code":::

Run the code by using the following command:

```bash
node app.js
```

## Troubleshooting

- **`Cannot find module 'foundry-local-sdk'`**: Run `npm install foundry-local-sdk` to install the SDK.
- **`Model not found`**: Verify the model alias is correct. Use `manager.catalog.getModels()` to list available models.
- **Slow first run**: Model downloads can take time the first time you run the app.
