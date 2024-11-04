---
title: Include file
description: Include file
author: sdgilley
ms.reviewer: sgilley
ms.author: sgilley
ms.service: azure-ai-studio
ms.topic: include
ms.date: 11/03/2024
ms.custom: include
---

Your project connection string is required to call the Azure OpenAI service from your code. In this quickstart, you save this value in a `.env` file, which is a file that contains environment variables that your application can read. 

Create a `.env` file, and paste the following code:

```text
AIPROJECT_CONNECTION_STRING=<your-connection-string>
AISEARCH_INDEX_NAME="example-index"
EMBEDDINGS_MODEL="text-embedding-ada-002"
INTENT_MAPPING_MODEL="gpt-40-mini"
CHAT_MODEL="gpt-40-mini"
```

Find your connection string in the Azure AI Studio project you created in the [AI Studio playground quickstart](../quickstarts/get-started-playground.md).  Open the project, then find the connection string on the **Overview** page.  Copy the connection string and paste it into the `.env` file.

:::image type="content" source="../media/quickstarts/azure-ai-sdk/connection-string.png" alt-text="Screenshot shows the overview page of a project and the location of the connection string.":::

If you have a search index that you want to use, update the `AISEARCH_INDEX_NAME` value to match the name of your search index.  If you don't have one, you'll create one in Part 2 of this tutorial.

If you changed the names of the models when you deployed them, update the values in the `.env` file to match the names you used.

> [!WARNING]
> Ensure that your `.env` is in your `.gitignore` file so that you don't accidentally check it into your git repository.
