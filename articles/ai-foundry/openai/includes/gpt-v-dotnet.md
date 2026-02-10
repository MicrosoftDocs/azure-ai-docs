---
title: 'Quickstart: Use GPT-4 Turbo with Vision on your images with the .NET SDK'
titleSuffix: Azure OpenAI
description: Get started using the Azure OpenAI .NET SDK to deploy and use the GPT-4 Turbo with Vision model.
services: cognitive-services
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: include
ms.custom: references_regions
ms.date: 01/29/2026
ai-usage: ai-assisted
---

Use this article to get started using the Azure OpenAI .NET SDK to deploy and use a vision-enabled chat model. 

## Prerequisites

- An Azure subscription. You can [create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- [The .NET 8.0 SDK](https://dotnet.microsoft.com/download)
- An Azure OpenAI in Microsoft Foundry Models resource with a vision-enabled chat model deployed. See [Model availability](../../foundry-models/concepts/models-sold-directly-by-azure.md) for available regions. For more information about resource creation, see the [resource deployment guide](/azure/ai-foundry/openai/how-to/create-resource).

### Microsoft Entra ID prerequisites

For the recommended keyless authentication with Microsoft Entra ID, you need to:
- Install the [Azure CLI](/cli/azure/install-azure-cli) used for keyless authentication with Microsoft Entra ID.
- Assign the `Cognitive Services User` role to your user account. You can assign roles in the Azure portal under **Access control (IAM)** > **Add role assignment**.

## Set up

1. Create a new folder `vision-quickstart` and go to the quickstart folder with the following command:

    ```shell
    mkdir vision-quickstart && cd vision-quickstart
    ```

1. Create a new console application with the following command:

    ```shell
    dotnet new console
    ```

3. Install the [OpenAI .NET client library](https://www.nuget.org/packages/Azure.AI.OpenAI/) with the [dotnet add package](/dotnet/core/tools/dotnet-add-package) command:

    ```console
    dotnet add package Azure.AI.OpenAI
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

To run the quickstart, follow these steps:

1. Replace the contents of `Program.cs` with the following code and update the placeholder values with your own.

    ```csharp
    using Azure;
    using Azure.AI.OpenAI;
    using Azure.Identity;
    using OpenAI.Chat; // Required for Passwordless auth
    
    string deploymentName = "gpt-4";
    
    string endpoint = Environment.GetEnvironmentVariable("AZURE_OPENAI_ENDPOINT") ?? "https://<your-resource-name>.openai.azure.com/";
    string key = Environment.GetEnvironmentVariable("AZURE_OPENAI_API_KEY") ?? "<your-key>";
    
    // Use the recommended keyless credential instead of the AzureKeyCredential credential.
    AzureOpenAIClient openAIClient = new AzureOpenAIClient(new Uri(endpoint), new DefaultAzureCredential()); 
    //AzureOpenAIClient openAIClient = new AzureOpenAIClient(new Uri(endpoint), new AzureKeyCredential(key));

    var chatClient = openAIClient.GetChatClient(deploymentName);
    
    var imageUrl = "YOUR_IMAGE_URL";
    
    var textPart = ChatMessageContentPart.CreateTextPart("Describe this picture:");
    var imgPart = ChatMessageContentPart.CreateImagePart(imageUrl); 

    var chatMessages = new List<ChatMessage>
    {
        new SystemChatMessage("You are a helpful assistant."),
        new UserChatMessage(textPart, imgPart)

    };
        
    ChatCompletion chatCompletion = await chatClient.CompleteChatAsync(chatMessages);
    
    Console.WriteLine($"[ASSISTANT]:");
    Console.WriteLine($"{chatCompletion.Content[0].Text}");
    ```

1. Replace `YOUR_IMAGE_URL` with the publicly accessible of the image you want to upload.

1. Run the application using the `dotnet run` command or the run button at the top of Visual Studio:

    ```dotnetcli
    dotnet run
    ```

## Output

The output of the application will be a description of the image you provided in the `imageUri` variable. The assistant will analyze the image and provide a detailed description based on its content.

## Clean up resources

If you want to clean up and remove an Azure OpenAI resource, you can delete the resource or resource group. Deleting the resource group also deletes any other resources associated with it.

- [Azure portal](../../../ai-services/multi-service-resource.md?pivots=azportal#clean-up-resources)
- [Azure CLI](../../../ai-services/multi-service-resource.md?pivots=azcli#clean-up-resources)


