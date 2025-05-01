---
title: include file
description: include file
author: pablolopes
ms.reviewer: pablolopes
ms.author: pablolopes
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 04/30/2025
ms.custom: include, build-2025
---

To work with Azure AI services in your .NET project, you'll need to install several NuGet packages. There are two ways to add these packages:

#### Option 1: Using the .NET CLI

You can add NuGet packages using the .NET CLI in the integrated terminal:


```bash
# Add Azure AI SDK packages
dotnet add package Azure.AI.Foundry.Project
dotnet add package Azure.Identity
dotnet add package Microsoft.SemanticKernel
dotnet add package Azure.AI.Projects.OneDP
dotnet add package Azure.AI.Agents.Persistant
dotnet add package Azure.AI.OpenAI
dotnet add package Azure.Search.Documents
dotnet add package Azure.Monitor.OpenTelemetry.AspNetCore
```

#### Option 2: Using the NuGet Package Manager in VS Code

1. Open your project in VS Code
2. Right-click on your project in the Solution Explorer panel (from C# Dev Kit)
3. Select "Manage NuGet Packages..." 
4. Search for and install each of the following packages:
   - Azure.AI.Foundry.Project
   - Azure.Identity
   - Microsoft.SemanticKernel
   - Azure.AI.OpenAI
   - Azure.Search.Documents
   - Azure.Monitor.OpenTelemetry.AspNetCore
   - Azure.AI.Projects.OneDP
   - Azure.AI.Agents.Persistant

After installing these packages, you'll need to add the appropriate using directives to your C# files:

```csharp
using Azure.AI.Foundry.Project;
using Azure.Identity;
using Microsoft.SemanticKernel;
using Azure.AI.OpenAI;
using Azure.Search.Documents;
// Add other namespaces as needed
```


