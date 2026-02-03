---
title: 'Quickstart: Use Azure OpenAI in Microsoft Foundry Models with the C# SDK to generate images'
titleSuffix: Azure OpenAI
description: Walkthrough on how to get started with Azure OpenAI and make your first image generation call with the C# SDK. 
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: include
author: PatrickFarley
ms.author: pafarley
ms.date: 01/29/2026
ai-usage: ai-assisted
---

Use this guide to get started generating images with the Azure OpenAI SDK for C#.

[Library source code](https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/openai/Azure.AI.OpenAI) | [Package (NuGet)](https://www.nuget.org/packages/Azure.AI.OpenAI/) | [Samples](https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/openai/Azure.AI.OpenAI/tests/Samples)

## Prerequisites

- An Azure subscription - [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn)
- The [.NET 7 SDK](https://dotnet.microsoft.com/download/dotnet/7.0)
- An Azure OpenAI resource created in a supported region (see [Region availability](/azure/ai-foundry/openai/concepts/models#model-summary-table-and-region-availability)). For more information, see [Create a resource and deploy a model with Azure OpenAI](../how-to/create-resource.md).

### Microsoft Entra ID prerequisites

For the recommended keyless authentication with Microsoft Entra ID, you need to:
- Install the [Azure CLI](/cli/azure/install-azure-cli) used for keyless authentication with Microsoft Entra ID.
- Assign the `Cognitive Services User` role to your user account. You can assign roles in the Azure portal under **Access control (IAM)** > **Add role assignment**.

## Set up

1. Create a new folder `image-quickstart` and go to the quickstart folder with the following command:

    ```shell
    mkdir image-quickstart && cd image-quickstart
    ```

1. Create a new console application with the following command:

    ```shell
    dotnet new console
    ```

3. Install the [OpenAI .NET client library](https://www.nuget.org/packages/Azure.AI.OpenAI/) with the [dotnet add package](/dotnet/core/tools/dotnet-add-package) command:

    ```console
    dotnet add package Azure.AI.OpenAI --version 1.0.0-beta.6
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
    using OpenAI.Images;
    using static System.Environment;
    
    string endpoint = Environment.GetEnvironmentVariable("AZURE_OPENAI_ENDPOINT") ?? "https://<your-resource-name>.openai.azure.com/";
    string key = Environment.GetEnvironmentVariable("AZURE_OPENAI_API_KEY") ?? "<your-key>";
    
    // Use the recommended keyless credential instead of the AzureKeyCredential credential.
    AzureOpenAIClient openAIClient = new AzureOpenAIClient(new Uri(endpoint), new DefaultAzureCredential()); 
    //AzureOpenAIClient openAIClient = new AzureOpenAIClient(new Uri(endpoint), new AzureKeyCredential(key));
    
    // This must match the custom deployment name you chose for your model
    ImageClient chatClient = openAIClient.GetImageClient("dalle-3");
    
    var imageGeneration = await chatClient.GenerateImageAsync(
            "a happy monkey sitting in a tree, in watercolor",
            new ImageGenerationOptions()
            {
                Size = GeneratedImageSize.W1024xH1024
            }
        );
    
    Console.WriteLine(imageGeneration.Value.ImageUri);
    ```

1. Run the application using the `dotnet run` command or the run button at the top of Visual Studio:

    ```dotnetcli
    dotnet run
    ```

## Output

The URL of the generated image is printed to the console.

```console
<SAS URL>
```

> [!NOTE]
> The Image APIs come with a content moderation filter. If the service recognizes your prompt as harmful content, it won't return a generated image. For more information, see the [content filter](../concepts/content-filter.md) article.

## Clean up resources

If you want to clean up and remove an Azure OpenAI resource, you can delete the resource. Before deleting the resource, you must first delete any deployed models.

- [Azure portal](../../../ai-services/multi-service-resource.md?pivots=azportal#clean-up-resources)
- [Azure CLI](../../../ai-services/multi-service-resource.md?pivots=azcli#clean-up-resources)

## Next steps

* Explore the Image APIs in more depth with the [Image API how-to guide](../how-to/dall-e.md).
* For more examples check out the [Azure OpenAI Samples GitHub repository](https://github.com/Azure-Samples/openai).
