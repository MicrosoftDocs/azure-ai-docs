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

### [Windows](#tab/windows)

```bash
cargo add foundry-local-sdk --features winml
cargo add tokio --features full
cargo add tokio-stream anyhow
```

> [!NOTE]
> The `winml` feature uses the Windows Machine Learning (WinML) framework for hardware acceleration and automatic execution provider management.

### [Cross-Platform](#tab/xplatform)

```bash
cargo add foundry-local-sdk
cargo add tokio --features full
cargo add tokio-stream anyhow
```

---
