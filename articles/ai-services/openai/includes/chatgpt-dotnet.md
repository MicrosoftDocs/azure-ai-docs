---
title: 'Quickstart: Use Azure OpenAI Service with the C# SDK'
titleSuffix: Azure OpenAI
description: Walkthrough on how to get started with Azure OpenAI and make your first completions call with the C# SDK.
manager: nitinme
ms.service: azure-ai-openai
ms.topic: include
author: mrbullwinkle
ms.author: mbullwin
ms.date: 11/15/2023
---

[Source code](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/openai/Azure.AI.OpenAI/src) | [Package (NuGet)](https://www.nuget.org/packages/Azure.AI.OpenAI/) | [Samples](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/openai/Azure.AI.OpenAI/tests/Samples)| [Retrieval Augmented Generation (RAG) enterprise chat template](/dotnet/ai/get-started-app-chat-template) |

## Prerequisites

- An Azure subscription - [Create one for free](https://azure.microsoft.com/free/cognitive-services?azure-portal=true)
- The [.NET 7 SDK](https://dotnet.microsoft.com/download/dotnet/7.0)
- An Azure OpenAI Service resource with either the `gpt-35-turbo` or the `gpt-4` models deployed. For more information about model deployment, see the [resource deployment guide](../how-to/create-resource.md).


## Set up

[!INCLUDE [Create a new .NET application](./dotnet-new-application.md)]

[!INCLUDE [get-key-endpoint](get-key-endpoint.md)]

[!INCLUDE [environment-variables](environment-variables.md)]


## Create a sample application

From the project directory, open the *program.cs* file and replace with the following code:

### Without response streaming

```csharp
using Azure;
using Azure.AI.OpenAI;
using static System.Environment;

string endpoint = GetEnvironmentVariable("AZURE_OPENAI_ENDPOINT");
string key = GetEnvironmentVariable("AZURE_OPENAI_API_KEY");

AzureOpenAIClient azureClient = new(
    new Uri(endpoint),
    new AzureKeyCredential(key));

// This must match the custom deployment name you chose for your model
ChatClient chatClient = azureClient.GetChatClient("gpt-35-turbo");

ChatCompletion completion = chatClient.CompleteChat(
    [
        new SystemChatMessage("You are a helpful assistant that talks like a pirate."),
        new UserChatMessage("Does Azure OpenAI support customer managed keys?"),
        new AssistantChatMessage("Yes, customer managed keys are supported by Azure OpenAI"),
        new UserChatMessage("Do other Azure AI services support this too?")
    ]);

Console.WriteLine($"{completion.Role}: {completion.Content[0].Text}");
```

> [!IMPORTANT]
> For production, use a secure way of storing and accessing your credentials like [Azure Key Vault](/azure/key-vault/general/overview). For more information about credential security, see the Azure AI services [security](../../security-features.md) article.

```cmd
dotnet run program.cs
```

## Output

```output
Assistant : Yes, many other Azure AI services also support customer managed keys, including Azure Cognitive Services, Azure Machine Learning, and Azure Databricks. By using customer managed keys, you can retain complete control over your encryption keys and provide an additional layer of security for your AI assets.
```

This will wait until the model has generated its entire response before printing the results. Alternatively, if you want to asynchronously stream the response and print the results, you can replace the contents of *program.cs* with the code in the next example.

### Async with streaming

```csharp
using Azure;
using Azure.AI.OpenAI;
using OpenAI.Chat;
using static System.Environment;

string endpoint = GetEnvironmentVariable("AZURE_OPENAI_ENDPOINT");
string key = GetEnvironmentVariable("AZURE_OPENAI_API_KEY");

AzureOpenAIClient azureClient = new(
    new Uri(endpoint),
    new AzureKeyCredential(key));

// This must match the custom deployment name you chose for your model
ChatClient chatClient = azureClient.GetChatClient("gpt-35-turbo");

var chatUpdates = chatClient.CompleteChatStreamingAsync(
    [
        new SystemChatMessage("You are a helpful assistant that talks like a pirate."),
        new UserChatMessage("Does Azure OpenAI support customer managed keys?"),
        new AssistantChatMessage("Yes, customer managed keys are supported by Azure OpenAI"),
        new UserChatMessage("Do other Azure AI services support this too?")
    ]);

await foreach(var chatUpdate in chatUpdates)
{
    if (chatUpdate.Role.HasValue)
    {
        Console.Write($"{chatUpdate.Role} : ");
    }
    
    foreach(var contentPart in chatUpdate.ContentUpdate)
    {
        Console.Write(contentPart.Text);
    }
}
```


## Clean up resources

If you want to clean up and remove an Azure OpenAI resource, you can delete the resource. Before deleting the resource, you must first delete any deployed models.

- [Azure portal](../../multi-service-resource.md?pivots=azportal#clean-up-resources)
- [Azure CLI](../../multi-service-resource.md?pivots=azcli#clean-up-resources)

## Next steps

* For more examples, check out the [Azure OpenAI Samples GitHub repository](https://aka.ms/AOAICodeSamples)
