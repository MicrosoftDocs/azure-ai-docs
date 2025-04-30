---
title: 'Quickstart: Use the OpenAI Service via the .NET SDK'
titleSuffix: Azure OpenAI Service
description: Walkthrough on how to get started with Azure OpenAI and make your first completions call with the .NET SDK. 
manager: masoucou
author: aapowell
ms.author: aapowell
ms.service: azure-ai-openai
ms.topic: include
ms.date: 3/11/2025
---

[Reference documentation](/dotnet/api/overview/azure/ai.openai.assistants-readme?context=/azure/ai-services/openai/context/context) |  [Source code](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/openai/Azure.AI.OpenAI/src) | [Package (NuGet)](https://www.nuget.org/packages/Azure.AI.OpenAI/)

## Prerequisites

- An Azure subscription - <a href="https://azure.microsoft.com/free/cognitive-services" target="_blank">Create one for free</a>
- The [.NET 8 SDK](https://dotnet.microsoft.com/download/dotnet/8.0)
- An Azure OpenAI resource with a [compatible model in a supported region](../concepts/models.md#assistants-preview).
- We recommend reviewing the [Responsible AI transparency note](/legal/cognitive-services/openai/transparency-note?context=%2Fazure%2Fai-services%2Fopenai%2Fcontext%2Fcontext&tabs=text) and other [Responsible AI resources](/legal/cognitive-services/openai/overview?context=%2Fazure%2Fai-services%2Fopenai%2Fcontext%2Fcontext) to familiarize yourself with the capabilities and limitations of the Azure OpenAI Service.
- An Azure OpenAI resource with the `gpt-4o` model deployed was used testing this example.

### Microsoft Entra ID prerequisites

For the recommended keyless authentication with Microsoft Entra ID, you need to:
- Install the [Azure CLI](/cli/azure/install-azure-cli) used for keyless authentication with Microsoft Entra ID.
- Assign the `Cognitive Services User` role to your user account. You can assign roles in the Azure portal under **Access control (IAM)** > **Add role assignment**.

## Set up

1. Create a new folder `assistants-quickstart` and go to the quickstart folder with the following command:

    ```shell
    mkdir assistants-quickstart && cd assistants-quickstart
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

To run the quickstart, follow these steps:

1. Replace the contents of `Program.cs` with the following code and update the placeholder values with your own.
    
    ```csharp
    using Azure;
    using Azure.AI.OpenAI;
    using Azure.Identity;
    using OpenAI.Assistants;
    using OpenAI.Files;
    using System.ClientModel;
    
    // Assistants is a beta API and subject to change
    // Acknowledge its experimental status by suppressing the matching warning.
    #pragma warning disable OPENAI001
    
    string deploymentName = "gpt-4o";
    
    string endpoint = Environment.GetEnvironmentVariable("AZURE_OPENAI_ENDPOINT") ?? "https://<your-resource-name>.openai.azure.com/";
    string key = Environment.GetEnvironmentVariable("AZURE_OPENAI_API_KEY") ?? "<your-key>";
    
    // Use the recommended keyless credential instead of the AzureKeyCredential credential.
    AzureOpenAIClient openAIClient = new AzureOpenAIClient(new Uri(endpoint), new DefaultAzureCredential()); 
    //AzureOpenAIClient openAIClient = new AzureOpenAIClient(new Uri(endpoint), new AzureKeyCredential(key));
    
    OpenAIFileClient fileClient = openAIClient.GetOpenAIFileClient();
    AssistantClient assistantClient = openAIClient.GetAssistantClient();
    
    // First, let's contrive a document we'll use retrieval with and upload it.
    using Stream document = BinaryData.FromString("""
        {
            "description": "This document contains the sale history data for Contoso products.",
            "sales": [
                {
                    "month": "January",
                    "by_product": {
                        "113043": 15,
                        "113045": 12,
                        "113049": 2
                    }
                },
                {
                    "month": "February",
                    "by_product": {
                        "113045": 22
                    }
                },
                {
                    "month": "March",
                    "by_product": {
                        "113045": 16,
                        "113055": 5
                    }
                }
            ]
        }
        """).ToStream();
    
    OpenAI.Files.OpenAIFile salesFile = await fileClient.UploadFileAsync(
        document,
        "monthly_sales.json",
        FileUploadPurpose.Assistants);
    
    // Now, we'll create a client intended to help with that data
    OpenAI.Assistants.AssistantCreationOptions assistantOptions = new()
    {
        Name = "Example: Contoso sales RAG",
        Instructions =
            "You are an assistant that looks up sales data and helps visualize the information based"
            + " on user queries. When asked to generate a graph, chart, or other visualization, use"
            + " the code interpreter tool to do so.",
        Tools =
                {
                    new FileSearchToolDefinition(),
                    new OpenAI.Assistants.CodeInterpreterToolDefinition(),
                },
        ToolResources = new()
        {
            FileSearch = new()
            {
                NewVectorStores =
                    {
                        new VectorStoreCreationHelper([salesFile.Id]),
                    }
            }
        },
    };
    
    Assistant assistant = await assistantClient.CreateAssistantAsync(deploymentName, assistantOptions);
    
    // Create and run a thread with a user query about the data already associated with the assistant
    ThreadCreationOptions threadOptions = new()
    {
        InitialMessages = { "How well did product 113045 sell in February? Graph its trend over time." }
    };
    
    var initialMessage = new OpenAI.Assistants.ThreadInitializationMessage(OpenAI.Assistants.MessageRole.User, ["hi"]);
    
    ThreadRun threadRun = await assistantClient.CreateThreadAndRunAsync(assistant.Id, threadOptions);
    
    // Check back to see when the run is done
    do
    {
        Thread.Sleep(TimeSpan.FromSeconds(1));
        threadRun = assistantClient.GetRun(threadRun.ThreadId, threadRun.Id);
    } while (!threadRun.Status.IsTerminal);
    
    // Finally, we'll print out the full history for the thread that includes the augmented generation
    AsyncCollectionResult<OpenAI.Assistants.ThreadMessage> messages
        = assistantClient.GetMessagesAsync(
            threadRun.ThreadId,
            new MessageCollectionOptions() { Order = MessageCollectionOrder.Ascending });
    
    await foreach (OpenAI.Assistants.ThreadMessage message in messages)
    {
        Console.Write($"[{message.Role.ToString().ToUpper()}]: ");
        foreach (OpenAI.Assistants.MessageContent contentItem in message.Content)
        {
            if (!string.IsNullOrEmpty(contentItem.Text))
            {
                Console.WriteLine($"{contentItem.Text}");
    
                if (contentItem.TextAnnotations.Count > 0)
                {
                    Console.WriteLine();
                }
    
                // Include annotations, if any.
                foreach (TextAnnotation annotation in contentItem.TextAnnotations)
                {
                    if (!string.IsNullOrEmpty(annotation.InputFileId))
                    {
                        Console.WriteLine($"* File citation, file ID: {annotation.InputFileId}");
                    }
                    if (!string.IsNullOrEmpty(annotation.OutputFileId))
                    {
                        Console.WriteLine($"* File output, new file ID: {annotation.OutputFileId}");
                    }
                }
            }
            if (!string.IsNullOrEmpty(contentItem.ImageFileId))
            {
                OpenAI.Files.OpenAIFile imageFile = await fileClient.GetFileAsync(contentItem.ImageFileId);
                BinaryData imageBytes = await fileClient.DownloadFileAsync(contentItem.ImageFileId);
                using FileStream stream = File.OpenWrite($"{imageFile.Filename}.png");
                imageBytes.ToStream().CopyTo(stream);
    
                Console.WriteLine($"<image: {imageFile.Filename}.png>");
            }
        }
        Console.WriteLine();
    }
    ```

1. Run the application with the following command:

    ```shell
    dotnet run
    ```

## Output

The console output should resemble the following:

```text
[USER]: How well did product 113045 sell in February? Graph its trend over time.

[ASSISTANT]: Product 113045 sold 22 units in February. Let's visualize its sales trend over the given months (January through March).

I'll create a graph to depict this trend.

[ASSISTANT]: <image: 553380b7-fdb6-49cf-9df6-e8e6700d69f4.png>
The graph above visualizes the sales trend for product 113045 from January to March. As seen, the sales peaked in February with 22 units sold, and fluctuated over the period from January (12 units) to March (16 units).

If you need further analysis or more details, feel free to ask!
```

## Clean up resources

If you want to clean up and remove an Azure OpenAI resource, you can delete the resource or resource group. Deleting the resource group also deletes any other resources associated with it.

- [Azure portal](../../multi-service-resource.md?pivots=azportal#clean-up-resources)
- [Azure CLI](../../multi-service-resource.md?pivots=azcli#clean-up-resources)

## See also

* Learn more about how to use Assistants with our [How-to guide on Assistants](../how-to/assistant.md).
* [Azure OpenAI Assistants API samples](https://github.com/Azure-Samples/azureai-samples/tree/main/scenarios/Assistants)
