---
title: Include file
description: Include file
author: jonburchel
ms.author: jburchel
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 05/19/2025
ms.custom: include file
---

### [Windows](#tab/windows)

```bash
dotnet add package Microsoft.AI.Foundry.Local.WinML
dotnet add package OpenAI
```

> [!NOTE]
> The Windows package uses the Windows Machine Learning (WinML) framework for hardware acceleration and automatic execution provider management.

### [Cross-Platform](#tab/xplatform)

```bash
dotnet add package Microsoft.AI.Foundry.Local
dotnet add package OpenAI
```

---
