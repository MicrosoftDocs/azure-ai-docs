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

If you're developing or shipping on Windows, select the **Windows** tab. The Windows package integrates with the [Windows ML](/windows/ai/new-windows-ml/overview) runtime — it provides the same API surface area with a wider breadth of hardware acceleration.

### [Windows](#tab/windows)

```bash
dotnet add package Microsoft.AI.Foundry.Local.WinML
dotnet add package OpenAI
```

### [Cross-Platform](#tab/xplatform)

```bash
dotnet add package Microsoft.AI.Foundry.Local
dotnet add package OpenAI
```

---

The C# samples in the GitHub repository are preconfigured projects. If you're building from scratch, you should read the [Foundry Local SDK reference](../reference/reference-sdk-current.md) for more details on how to set up your C# project with Foundry Local. 
