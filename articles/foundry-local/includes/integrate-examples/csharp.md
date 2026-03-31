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


## Samples repository

[!INCLUDE [samples-repo](../samples-repo.md)]

Navigate to the sample for this article:

```bash
cd cs/foundry-local-web-server
```

## Set up project

[!INCLUDE [project-setup](./../csharp-project-setup.md)]

## Use OpenAI SDK with Foundry Local

The following example demonstrates how to use the OpenAI SDK with Foundry Local. The code includes the following steps:

1. Initializes a `FoundryLocalManager` instance with a `Configuration` that includes the web service configuration. The web service is an OpenAI compliant endpoint.
1. Gets a `Model` object from the model catalog using an alias.

   > [!NOTE]
   > Foundry Local selects the best variant for the model automatically based on the available hardware of the host machine.

1. Downloads and loads the model variant.
1. Starts the web service.
1. Uses the OpenAI SDK to call the local Foundry web service.
1. Tidies up by stopping the web service and unloading the model.

Copy-and-paste the following code into a C# file named `Program.cs`:

:::code language="csharp" source="~/foundry-local-main/samples/cs/foundry-local-web-server/Program.cs" id="complete_code":::

Reference: [Foundry Local SDK reference](../../reference/reference-sdk-current.md)
Reference: [Foundry Local REST API reference](../../reference/reference-rest.md)

## Run the application

```bash
dotnet run
```
