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

Your project connection string is required to call the Azure OpenAI service from your code. In this quickstart, you save this value in a `.env` file, which is a file that contains environment variables that your application can read. 

Create a `.env` file, and paste the following code:

```text
PROJECT_CONNECTION_STRING=<your-connection-string>
```

You find your connection string in the Azure AI Foundry project you created in the [Azure AI Foundry playground quickstart](../quickstarts/get-started-playground.md).  Open the project, then find the connection string on the **Overview** page.  Copy the connection string and paste it into the `.env` file.

:::image type="content" source="../media/quickstarts/azure-ai-sdk/connection-string.png" alt-text="Screenshot shows the overview page of a project and the location of the connection string.":::

> [!WARNING]
> Ensure that your `.env` is in your `.gitignore` file so that you don't accidentally check it into your git repository.
