---
title: Include file
description: Include file
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 01/06/2026
ms.author: samkemp
author: samuel100
ai-usage: ai-assisted
---

## Prerequisites

- [.NET 8.0 SDK](https://dotnet.microsoft.com/download/dotnet/8.0) or later installed.


## Samples repository

[!INCLUDE [samples-repo](../samples-repo.md)]

```bash
cd Foundry-Local/samples/cs/foundry-local-web-server
```

## Install packages

[!INCLUDE [project-setup](./../csharp-project-setup.md)]

## Use OpenAI SDK with Foundry Local

Copy-and-paste the following code into a C# file named `Program.cs`:

:::code language="csharp" source="~/foundry-local-main/samples/cs/foundry-local-web-server/Program.cs" id="complete_code":::

Reference: [Foundry Local SDK reference](../../reference/reference-sdk-current.md)
Reference: [Foundry Local REST API reference](../../reference/reference-rest.md)

```bash
dotnet run
```
