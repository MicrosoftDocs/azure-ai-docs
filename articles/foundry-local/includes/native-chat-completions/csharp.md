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

- [.NET 9.0 SDK](https://dotnet.microsoft.com/download/dotnet/9.0) or later installed.

## Set up project

[!INCLUDE [project-setup](../csharp-project-setup.md)]

## Use native chat completions API    

The following example demonstrates how to use the native chat completions API in Foundry Local. The code includes the following steps:

1. Initializes a `FoundryLocalManager` instance with a `Configuration`.
1. Gets a `Model` object from the model catalog using an alias.
   
   > [!NOTE]
   > Foundry Local automatically selects the best variant for the model based on the available hardware of the host machine.

1. Downloads and loads the model variant.
1. Uses the native chat completions API to generate a response.
1. Unloads the model.

Copy and paste the following code into a C# file named `Program.cs`:

:::code language="csharp" source="~/foundry-local-main/samples/cs/GettingStarted/src/HelloFoundryLocalSdk/Program.cs" id="complete_code":::

Run the code by using the following command:

```bash
dotnet run
```


> [!NOTE]
> If you're targeting Windows, use the Windows-specific instructions under the Windows tab for the best performance and experience.

## Troubleshooting

- **Build errors referencing `net9.0`**: Install the [.NET 9.0 SDK](https://dotnet.microsoft.com/download/dotnet/9.0), then rebuild the app.
- **`Model not found`**: Run the optional model listing snippet to find an alias available on your device, then update the alias passed to `GetModelAsync`.
- **Slow first run**: Model downloads can take time the first time you run the app.