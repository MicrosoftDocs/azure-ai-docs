---
title: 'Quickstart: Use the OpenAI Service via the .NET SDK'
titleSuffix: Azure OpenAI Service
description: Walkthrough on how to get started with Azure OpenAI and make your first completions call with the .NET SDK. 
manager: masoucou
author: aapowell
ms.author: aapowell
ms.service: azure-ai-openai
ms.topic: include
ms.date: 9/27/2024
---

[Reference documentation](/dotnet/api/overview/azure/ai.openai.assistants-readme?context=/azure/ai-services/openai/context/context) |  [Source code](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/openai/Azure.AI.OpenAI/src) | [Package (NuGet)](https://www.nuget.org/packages/Azure.AI.OpenAI/)

## Prerequisites

- An Azure subscription - <a href="https://azure.microsoft.com/free/cognitive-services" target="_blank">Create one for free</a>
- The [.NET 8 SDK](https://dotnet.microsoft.com/download/dotnet/8.0)
- An Azure OpenAI resource with a [compatible model in a supported region](../concepts/models.md#assistants-preview).
- We recommend reviewing the [Responsible AI transparency note](/legal/cognitive-services/openai/transparency-note?context=%2Fazure%2Fai-services%2Fopenai%2Fcontext%2Fcontext&tabs=text) and other [Responsible AI resources](/legal/cognitive-services/openai/overview?context=%2Fazure%2Fai-services%2Fopenai%2Fcontext%2Fcontext) to familiarize yourself with the capabilities and limitations of the Azure OpenAI Service.
- An Azure OpenAI resource with the `gpt-4 (1106-preview)` model deployed was used testing this example.

## Set up

### Create a new .NET Core application

1. In a console window (such as cmd, PowerShell, or Bash), use the [`dotnet new`](/dotnet/core/tools/dotnet-new) command to create a new console app with the name `azure-openai-quickstart`:
    
    ```dotnetcli
    dotnet new console -n azure-openai-assistants-quickstart
    ```

2. Change into the directory of the newly created app folder and build the app with the [`dotnet build`](/dotnet/core/tools/dotnet-build) command:

    ```dotnetcli
    dotnet build
    ```

    The build output should contain no warnings or errors.
    
    ```output
    ...
    Build succeeded.
     0 Warning(s)
     0 Error(s)
    ...
    ```

3. Install the [OpenAI .NET client library](https://www.nuget.org/packages/Azure.AI.OpenAI/) with the [dotnet add package](/dotnet/core/tools/dotnet-add-package) command:

    ```console
    dotnet add package Azure.AI.OpenAI --prerelease
    ```

[!INCLUDE [get-key-endpoint](get-key-endpoint.md)]

[!INCLUDE [environment-variables](environment-variables.md)]

### Create the assistant

Update the `Program.cs` file with the following code to create an assistant:

```csharp
using Azure;
using Azure.AI.OpenAI.Assistants;

// Assistants is a beta API and subject to change; acknowledge its experimental status by suppressing the matching warning.
string endpoint = Environment.GetEnvironmentVariable("AZURE_OPENAI_ENDPOINT");
string key = Environment.GetEnvironmentVariable("AZURE_OPENAI_API_KEY");

var openAIClient = new AzureOpenAIClient(new Uri(endpoint), new AzureKeyCredential(key));

// Use for passwordless auth
//var openAIClient = new AzureOpenAIClient(new Uri(endpoint), new DefaultAzureCredential()); 

FileClient fileClient = openAIClient.GetFileClient();
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

OpenAIFileInfo salesFile = await fileClient.UploadFileAsync(
    document,
    "monthly_sales.json",
    FileUploadPurpose.Assistants);

// Now, we'll create a client intended to help with that data
AssistantCreationOptions assistantOptions = new()
{
    Name = "Example: Contoso sales RAG",
    Instructions =
        "You are an assistant that looks up sales data and helps visualize the information based"
        + " on user queries. When asked to generate a graph, chart, or other visualization, use"
        + " the code interpreter tool to do so.",
    Tools =
            {
                new FileSearchToolDefinition(),
                new CodeInterpreterToolDefinition(),
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

// Now we'll create a thread with a user query about the data already associated with the assistant, then run it
ThreadCreationOptions threadOptions = new()
{
    InitialMessages = { "How well did product 113045 sell in February? Graph its trend over time." }
};

ThreadRun threadRun = await assistantClient.CreateThreadAndRunAsync(assistant.Id, threadOptions);

// Check back to see when the run is done
do
{
    Thread.Sleep(TimeSpan.FromSeconds(1));
    threadRun = assistantClient.GetRun(threadRun.ThreadId, threadRun.Id);
} while (!threadRun.Status.IsTerminal);

// Finally, we'll print out the full history for the thread that includes the augmented generation
AsyncCollectionResult<ThreadMessage> messages
    = assistantClient.GetMessagesAsync(threadRun.ThreadId, new MessageCollectionOptions() { Order = MessageCollectionOrder.Ascending });

await foreach (ThreadMessage message in messages)
{
    Console.Write($"[{message.Role.ToString().ToUpper()}]: ");
    foreach (MessageContent contentItem in message.Content)
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
            OpenAIFileInfo imageInfo = await fileClient.GetFileAsync(contentItem.ImageFileId);
            BinaryData imageBytes = await fileClient.DownloadFileAsync(contentItem.ImageFileId);
            using FileStream stream = File.OpenWrite($"{imageInfo.Filename}.png");
            imageBytes.ToStream().CopyTo(stream);

            Console.WriteLine($"<image: {imageInfo.Filename}.png>");
        }
    }
    Console.WriteLine();
}
```

Run the app using the [`dotnet run`](/dotnet/core/tools/dotnet-run) command:

```csharp
dotnet run
```

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
