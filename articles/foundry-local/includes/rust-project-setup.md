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

Create a new Rust project and add the required dependencies:

1. Create a new Rust project and navigate into it:
    ```bash
    cargo new app-name
    cd app-name
    ```
1. Add the required dependencies:
    ```bash
    cargo add foundry-local-sdk tokio --features tokio/full
    cargo add tokio-stream
    ```
