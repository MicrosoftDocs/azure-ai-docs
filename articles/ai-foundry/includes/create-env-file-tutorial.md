---
title: Include file
description: Include file
author: sdgilley
ms.reviewer: sgilley
ms.author: sgilley
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 11/03/2024
ms.custom: include, ignite-2024
---

Your project connection string is required to call Azure OpenAI in Microsoft Foundry Models from your code. In this quickstart, you save this value in a `.env` file, which is a file that contains environment variables that your application can read. 

Create a `.env` file, and paste the following code:

```text
AIPROJECT_CONNECTION_STRING=<your-connection-string>
AISEARCH_INDEX_NAME="example-index"
EMBEDDINGS_MODEL="text-embedding-ada-002"
INTENT_MAPPING_MODEL="gpt-4o-mini"
CHAT_MODEL="gpt-4o-mini"
EVALUATION_MODEL="gpt-4o-mini"
```

* Find your connection string in the Foundry project you created in the [Foundry playground quickstart](../quickstarts/get-started-playground.md).  Open the project, then find the connection string on the **Overview** page.  Copy the connection string and paste it into the `.env` file.

    :::image type="content" source="../media/quickstarts/azure-ai-sdk/connection-string.png" alt-text="Screenshot shows the overview page of a project and the location of the connection string.":::

* If you don't yet have a search index, keep the value "example-index" for `AISEARCH_INDEX_NAME`. In Part 2 of this tutorial you'll create the index using this name. If you have previously created a search index that you want to use instead, update the value to match the name of that search index.  

* If you changed the names of the models when you deployed them, update the values in the `.env` file to match the names you used.

> [!TIP]
> If you're working in VS Code, close and reopen the terminal window after you've saved changes in the `.env` file.

> [!WARNING]
> Ensure that your `.env` is in your `.gitignore` file so that you don't accidentally check it into your git repository.
