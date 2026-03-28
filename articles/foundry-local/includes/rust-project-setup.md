---
title: include file
description: include file
author: samuel100
ms.author: samkemp
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 07/17/2025
ms.custom: include file
ai-usage: ai-assisted
---

Use Foundry Local in your Rust project by following these Windows-specific or Cross-Platform (macOS/Linux/Windows) instructions:

### [Windows](#tab/windows)

1. Create a new Rust project and navigate into it:
    ```bash
    cargo new app-name
    cd app-name
    ```
1. Add the required dependencies:
    ```bash
    cargo add foundry-local-sdk --features winml
    cargo add tokio --features full
    cargo add tokio-stream
    ```

### [Cross-Platform](#tab/xplatform)

1. Create a new Rust project and navigate into it:
    ```bash
    cargo new app-name
    cd app-name
    ```
1. Add the required dependencies:
    ```bash
    cargo add foundry-local-sdk
    cargo add tokio --features full
    cargo add tokio-stream
    ```

---
