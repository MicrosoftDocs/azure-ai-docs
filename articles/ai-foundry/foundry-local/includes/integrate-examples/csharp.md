---
ms.service: azure-ai-foundry
ms.custom: build-2025
ms.topic: include
ms.date: 05/02/2025
ms.author: maanavdalal
author: maanavd
---

## Create project and install NuGet packages

To create a new C# project and install the required NuGet packages, run the following commands in your terminal:

```bash
mkdir FoundryLocalExample
cd FoundryLocalExample
dotnet new console
dotnet add package Azure.AI.OpenAI
dotnet add package Microsoft.AI.FoundryLocal
```

## OpenAI SDK with Foundry Local

The following example demonstrates how to use the OpenAI SDK with Foundry Local. The code initializes the Foundry Local service, loads a model, and generates a response using the OpenAI SDK.

Copy-and-paste the following code into a C# file named `Program.cs`:

```csharp
using Azure.AI.OpenAI;
using Azure;
using Microsoft.AI.FoundryLocal;

var foundryManager = new FoundryLocalManager();
var modelInfo = await foundryManager.StartModelAsync("deepseek-r1-1.5b")

// Create a client
OpenAIClient client = new OpenAIClient(
    foundryManager.Endpoint,
    foundryManager.ApiKey
);

// Chat completions
ChatCompletionsOptions options = new ChatCompletionsOptions()
{
    Messages =
    {
        new ChatMessage(ChatRole.User, "What is Foundry Local?")
    },
    DeploymentName = modelInfo.Id,
};

Response<ChatCompletions> response = await client.GetChatCompletionsAsync(options);
string completion = response.Value.Choices[0].Message.Content;
Console.WriteLine(completion);
```
