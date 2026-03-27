---
title: include file
description: include file
author: jonburchel
ms.author: jburchel
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 05/19/2025
ms.custom: include file
---

Use Foundry Local in your JavaScript project by following these Windows-specific or Cross-Platform (macOS/Linux/Windows) instructions:

### [Windows](#tab/windows)

1. Create a new JavaScript project:
    ```bash
    mkdir app-name
    cd app-name
    npm init -y
    npm pkg set type=module
    ```
1. Install the Foundry Local SDK package:
    ```bash
    npm install --winml foundry-local-sdk
    npm install openai
    ```

### [Cross-Platform](#tab/xplatform)

1. Create a new JavaScript project:
    ```bash
    mkdir app-name
    cd app-name
    npm init -y
    npm pkg set type=module
    ```
1. Install the Foundry Local SDK package:
    ```bash
    npm install foundry-local-sdk
    npm install openai
    ```

---
