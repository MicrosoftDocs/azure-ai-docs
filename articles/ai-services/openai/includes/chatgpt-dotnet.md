---
title: 'Quickstart: Use Azure OpenAI in Azure AI Foundry Models with the C# SDK'
titleSuffix: Azure OpenAI
description: Walkthrough on how to get started with Azure OpenAI and make your first completions call with the C# SDK.
manager: nitinme
ms.service: azure-ai-openai
ms.topic: include
author: mrbullwinkle
ms.author: mbullwin
ms.date: 3/11/2025
---

[Source code](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/openai/Azure.AI.OpenAI/src) | [Package (NuGet)](https://www.nuget.org/packages/Azure.AI.OpenAI/) | [Samples](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/openai/Azure.AI.OpenAI/tests/Samples)| [Retrieval Augmented Generation (RAG) enterprise chat template](/dotnet/ai/get-started-app-chat-template) |

## Prerequisites

- An Azure subscription - [Create one for free](https://azure.microsoft.com/free/cognitive-services?azure-portal=true)
- The [.NET 7 SDK](https://dotnet.microsoft.com/download/dotnet/7.0)
- An Azure OpenAI in Azure AI Foundry Models resource with the `gpt-4o` model deployed. For more information about model deployment, see the [resource deployment guide](../how-to/create-resource.md).

### Microsoft Entra ID prerequisites

For the recommended keyless authentication with Microsoft Entra ID, you need to:
- Install the [Azure CLI](/cli/azure/install-azure-cli) used for keyless authentication with Microsoft Entra ID.
- Assign the `Cognitive Services User` role to your user account. You can assign roles in the Azure portal under **Access control (IAM)** > **Add role assignment**.

## Set up

1. Create a new folder `chat-quickstart` and go to the quickstart folder with the following command:

    ```shell
    mkdir chat-quickstart && cd chat-quickstart
    ```

1. Create a new console application with the following command:

    ```shell
    dotnet new console
    ```

3. Install the [OpenAI .NET client library](https://www.nuget.org/packages/Azure.AI.OpenAI/) with the [dotnet add package](/dotnet/core/tools/dotnet-add-package) command:

    ```console
    dotnet add package Azure.AI.OpenAI --prerelease
    ```

1. For the **recommended** keyless authentication with Microsoft Entra ID, install the [Azure.Identity](https://www.nuget.org/packages/Azure.Identity) package with:

    ```console
    dotnet add package Azure.Identity
    ```

1. For the **recommended** keyless authentication with Microsoft Entra ID, sign in to Azure with the following command:

    ```console
    az login
    ```

## Retrieve resource information

[!INCLUDE [resource authentication](resource-authentication.md)]

## Run the quickstart

The sample code in this quickstart uses Microsoft Entra ID for the recommended keyless authentication. If you prefer to use an API key, you can replace the `DefaultAzureCredential` object with an `AzureKeyCredential` object. 

#### [Microsoft Entra ID](#tab/keyless)

```csharp
AzureOpenAIClient openAIClient = new AzureOpenAIClient(new Uri(endpoint), new DefaultAzureCredential()); 
```

#### [API key](#tab/api-key)

```csharp
AzureOpenAIClient openAIClient = new AzureOpenAIClient(new Uri(endpoint), new AzureKeyCredential(key));
```
---

You can use streaming or non-streaming to get the chat completion. The following code examples show how to use both methods. The first example shows how to use the non-streaming method, and the second example shows how to use the streaming method.

### Without response streaming

To run the quickstart, follow these steps:

1. Replace the contents of `Program.cs` with the following code and update the placeholder values with your own.

    ```csharp
    using Azure;
    using Azure.Identity;
    using OpenAI.Assistants;
    using Azure.AI.OpenAI;
    using OpenAI.Chat;
    using static System.Environment;
    
    string endpoint = Environment.GetEnvironmentVariable("AZURE_OPENAI_ENDPOINT") ?? "https://<your-resource-name>.openai.azure.com/";
    string key = Environment.GetEnvironmentVariable("AZURE_OPENAI_API_KEY") ?? "<your-key>";
    
    // Use the recommended keyless credential instead of the AzureKeyCredential credential.
    AzureOpenAIClient openAIClient = new AzureOpenAIClient(new Uri(endpoint), new DefaultAzureCredential()); 
    //AzureOpenAIClient openAIClient = new AzureOpenAIClient(new Uri(endpoint), new AzureKeyCredential(key));
    
    // This must match the custom deployment name you chose for your model
    ChatClient chatClient = openAIClient.GetChatClient("gpt-4o");
    
    ChatCompletion completion = chatClient.CompleteChat(
        [
            new SystemChatMessage("You are a helpful assistant that talks like a pirate."),
            new UserChatMessage("Does Azure OpenAI support customer managed keys?"),
            new AssistantChatMessage("Yes, customer managed keys are supported by Azure OpenAI"),
            new UserChatMessage("Do other Azure services support this too?")
        ]);
    
    Console.WriteLine($"{completion.Role}: {completion.Content[0].Text}");
    ```

1. Run the application with the following command:

    ```shell
    dotnet run
    ```


#### Output

```output
Assistant: Arrr, ye be askin’ a fine question, matey! Aye, several Azure services support customer-managed keys (CMK)! This lets ye take the wheel and secure yer data with encryption keys stored in Azure Key Vault. Services such as Azure Machine Learning, Azure Cognitive Search, and others also offer CMK fer data protection. Always check the specific service's documentation fer the latest updates, as features tend to shift swifter than the tides, aye!
```

This will wait until the model has generated its entire response before printing the results. Alternatively, if you want to asynchronously stream the response and print the results, you can replace the contents of *Program.cs* with the code in the next example.

### Async with streaming

To run the quickstart, follow these steps:

1. Replace the contents of `Program.cs` with the following code and update the placeholder values with your own.

    ```csharp
    using Azure;
    using Azure.Identity;
    using OpenAI.Assistants;
    using Azure.AI.OpenAI;
    using OpenAI.Chat;
    using static System.Environment;
    
    string endpoint = Environment.GetEnvironmentVariable("AZURE_OPENAI_ENDPOINT") ?? "https://<your-resource-name>.openai.azure.com/";
    string key = Environment.GetEnvironmentVariable("AZURE_OPENAI_API_KEY") ?? "<your-key>";
    
    // Use the recommended keyless credential instead of the AzureKeyCredential credential.
    AzureOpenAIClient openAIClient = new AzureOpenAIClient(new Uri(endpoint), new DefaultAzureCredential()); 
    //AzureOpenAIClient openAIClient = new AzureOpenAIClient(new Uri(endpoint), new AzureKeyCredential(key));
    
    // This must match the custom deployment name you chose for your model
    ChatClient chatClient = openAIClient.GetChatClient("gpt-4o");
    
    var chatUpdates = chatClient.CompleteChatStreamingAsync(
        [
            new SystemChatMessage("You are a helpful assistant that talks like a pirate."),
            new UserChatMessage("Does Azure OpenAI support customer managed keys?"),
            new AssistantChatMessage("Yes, customer managed keys are supported by Azure OpenAI"),
            new UserChatMessage("Do other Azure services support this too?")
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

1. Run the application with the following command:

    ```shell
    dotnet run
    ```


#### Output

```output
Assistant: Arrr, ye be askin’ a fine question, matey! Aye, many Azure services support customer-managed keys (CMK)! This lets ye take the wheel and secure yer data with encryption keys stored in Azure Key Vault. Services such as Azure Machine Learning, Azure Cognitive Search, and others also offer CMK fer data protection. Always check the specific service's documentation fer the latest updates, as features tend to shift swifter than the tides, aye!
```


## Clean up resources

If you want to clean up and remove an Azure OpenAI resource, you can delete the resource. Before deleting the resource, you must first delete any deployed models.

- [Azure portal](../../multi-service-resource.md?pivots=azportal#clean-up-resources)
- [Azure CLI](../../multi-service-resource.md?pivots=azcli#clean-up-resources)

## Next steps

* [Get started with the chat using your own data sample for .NET](/dotnet/ai/get-started-app-chat-template?toc=/azure/ai-services/openai/toc.json&bc=/azure/ai-services/openai/breadcrumb/toc.json&tabs=github-codespaces)
* For more examples, check out the [Azure OpenAI Samples GitHub repository](https://github.com/Azure-Samples/openai)
