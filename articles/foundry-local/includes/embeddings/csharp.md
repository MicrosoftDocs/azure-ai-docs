---
title: Include file
description: Include file
ms.service: microsoft-foundry
ms.topic: include
ms.date: 06/15/2026
ms.author: natke
author: natke
ai-usage: ai-assisted
---

## Prerequisites

- [.NET 8.0 SDK](https://dotnet.microsoft.com/download/dotnet/8.0) or later installed.


## Samples repository

The complete sample code for this article is available in the [foundry-samples GitHub repository](https://github.com/microsoft-foundry/foundry-samples). To clone the repository and navigate to the sample use:

```bash
git clone https://github.com/microsoft-foundry/foundry-samples.git
cd foundry-samples/samples/csharp/foundry-local/embeddings
```

## Install packages

[!INCLUDE [project-setup](../csharp-project-setup.md)]

## Generate text embeddings

Copy and paste the following code into a C# file named `Program.cs`:

:::code language="csharp" source="~/foundry-local-main/samples/csharp/foundry-local/embeddings/Program.cs" id="complete_code":::

Run the code by using the following command:

```bash
dotnet run
```

## Troubleshooting

- **Build errors referencing `net8.0`**: Install the [.NET 8.0 SDK](https://dotnet.microsoft.com/download/dotnet/8.0), then rebuild the app.
- **`Model not found`**: Run the optional model listing snippet to find an alias available on your device, then update the alias passed to `GetModelAsync`.
- **Slow first run**: Model downloads can take time the first time you run the app.
