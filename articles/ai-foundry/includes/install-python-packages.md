---
title: include file
description: include file
author: sdgilley
ms.reviewer: sgilley
ms.author: sgilley
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 08/29/2024
ms.custom: include, ignite-2024
---

1. Create a file named **requirements.txt** in your project folder. Add the following packages, or modify as needed:

    ```txt
    azure-ai-projects 
    azure-identity 
    openai 
    azure-ai-inference 
    azure-search-documents 
    azure-ai-evaluation 
    azure-monitor-opentelemetry
    ```

    > [!NOTE]
    > Use `azure-ai-projects` to access resources in a [!INCLUDE [hub-project-name](hub-project-name.md)].  This package is not needed when working with a [!INCLUDE [fdp-project-name](fdp-project-name.md)].
    
1. Install the packages:

    ```bash
    pip install -r requirements.txt
    ```
