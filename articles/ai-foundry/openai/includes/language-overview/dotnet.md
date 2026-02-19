---
title: Azure OpenAI C# support
titleSuffix: Azure OpenAI in Microsoft Foundry Models
description: Azure OpenAI C# support
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: include
ms.date: 08/31/2025
ai-usage: ai-assisted
---




[Source code](https://github.com/openai/openai-dotnet) | [Package (NuGet)](https://www.nuget.org/packages/OpenAI) 
 
## Azure OpenAI API version support

- v1 Generally Available (GA) API now allows access to both GA and Preview operations. To learn more, see the [API version lifecycle guide](../../api-version-lifecycle.md).

## Installation

```dotnetcli
dotnet add package OpenAI
```

## Authentication

# [Microsoft Entra ID](#tab/dotnet-secure)

A secure, keyless authentication approach is to use Microsoft Entra ID (formerly Azure Active Directory) via the [Azure Identity library](/dotnet/api/overview/azure/identity-readme?view=azure-dotnet&preserve-view=true ). To use the library:

```dotnetcli
dotnet add package Azure.Identity
```

Use the desired credential type from the library. For example, [`DefaultAzureCredential`](/dotnet/api/azure.identity.defaultazurecredential?view=azure-dotnet&preserve-view=true):

```csharp
using Azure.Identity;
using OpenAI;
using OpenAI.Chat;
using System.ClientModel.Primitives;

#pragma warning disable OPENAI001

BearerTokenPolicy tokenPolicy = new(
    new DefaultAzureCredential(),
    "https://cognitiveservices.azure.com/.default");

ChatClient client = new(
    model: "gpt-4.1-nano",
    authenticationPolicy: tokenPolicy,
    options: new OpenAIClientOptions() { 
    
        Endpoint = new Uri("https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1")
   }
);

ChatCompletion completion = client.CompleteChat("Tell me about the bitter lesson.");

Console.WriteLine($"[ASSISTANT]: {completion.Content[0].Text}");
```

For more information about Azure OpenAI keyless authentication, see the "[Get started with the Azure OpenAI security building block](/azure/developer/ai/get-started-securing-your-ai-app?tabs=github-codespaces&pivots=dotnet)" QuickStart article. 

# [API Key](#tab/dotnet-key)

```csharp
using OpenAI;
using OpenAI.Chat;
using System.ClientModel;

string keyFromEnvironment = Environment.GetEnvironmentVariable("AZURE_OPENAI_API_KEY");

ChatClient client = new(
    model: "gpt-4.1-nano",
    credential: new ApiKeyCredential(keyFromEnvironment),
    options: new OpenAIClientOptions() { 
    
        Endpoint = new Uri("https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1")
   }
);

ChatCompletion completion = client.CompleteChat("Tell me about the bitter lesson.");

Console.WriteLine($"[ASSISTANT]: {completion.Content[0].Text}");

```

---

## Chat

Example of chat completions request to a [reasoning model](../../how-to/reasoning.md).

```csharp
using OpenAI;
using OpenAI.Chat;
using System.ClientModel.Primitives;

#pragma warning disable OPENAI001 //currently required for token based authentication

BearerTokenPolicy tokenPolicy = new(
    new DefaultAzureCredential(),
    "https://cognitiveservices.azure.com/.default");

ChatClient client = new(
    model: "o4-mini",
    authenticationPolicy: tokenPolicy,
    options: new OpenAIClientOptions()
    {

        Endpoint = new Uri("https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1")
    }
);

ChatCompletionOptions options = new ChatCompletionOptions
{
    ReasoningEffortLevel = ChatReasoningEffortLevel.Low,
    MaxOutputTokenCount = 100000
};

ChatCompletion completion = client.CompleteChat(
         new DeveloperChatMessage("You are a helpful assistant"),
         new UserChatMessage("Tell me about the bitter lesson")
    );

Console.WriteLine($"[ASSISTANT]: {completion.Content[0].Text}");

```

## Embeddings

```csharp
using OpenAI;
using OpenAI.Embeddings;
using System.ClientModel;

string apiKey = Environment.GetEnvironmentVariable("AZURE_OPENAI_API_KEY")
    ?? throw new InvalidOperationException("AZURE_OPENAI_API_KEY environment variable is not set");

EmbeddingClient client = new(
    "text-embedding-3-large",
    credential: new ApiKeyCredential(apiKey),
    options: new OpenAIClientOptions()
    {
        Endpoint = new Uri("https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1")
    }
);

string input = "This is a test";

OpenAIEmbedding embedding = client.GenerateEmbedding(input);
ReadOnlyMemory<float> vector = embedding.ToFloats();
Console.WriteLine($"Embeddings: [{string.Join(", ", vector.ToArray())}]");
```

## Responses API

```csharp
using OpenAI;
using OpenAI.Responses;
using System.ClientModel.Primitives;
using Azure.Identity;

#pragma warning disable OPENAI001 //currently required for token based authentication

BearerTokenPolicy tokenPolicy = new(
    new DefaultAzureCredential(),
    "https://cognitiveservices.azure.com/.default");

OpenAIResponseClient client = new(
    model: "o4-mini",
    authenticationPolicy: tokenPolicy,
    options: new OpenAIClientOptions()
    {
        Endpoint = new Uri("https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1")
    }
);

OpenAIResponse response = await client.CreateResponseAsync(
    userInputText: "What's the optimal strategy to win at poker?",
    new ResponseCreationOptions()
    {
        ReasoningOptions = new ResponseReasoningOptions()
        {
            ReasoningEffortLevel = ResponseReasoningEffortLevel.High,
        },
    });

Console.WriteLine(response.GetOutputText());

```

### Streaming

```csharp
using OpenAI;
using OpenAI.Responses;
using System.ClientModel.Primitives;
using Azure.Identity;

#pragma warning disable OPENAI001 //currently required for token based authentication

BearerTokenPolicy tokenPolicy = new(
    new DefaultAzureCredential(),
    "https://cognitiveservices.azure.com/.default");

#pragma warning disable OPENAI001

OpenAIResponseClient client = new(
    model: "o4-mini",
    authenticationPolicy: tokenPolicy,
    options: new OpenAIClientOptions()
    {
        Endpoint = new Uri("https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1")
    }
);


await foreach (StreamingResponseUpdate update
    in client.CreateResponseStreamingAsync(
        userInputText: "What's the optimal strategy to win at poker?",
        new ResponseCreationOptions()
        {
            ReasoningOptions = new ResponseReasoningOptions()
            {
                ReasoningEffortLevel = ResponseReasoningEffortLevel.High,
            },
        }))
{
    if (update is StreamingResponseOutputItemAddedUpdate itemUpdate
        && itemUpdate.Item is ReasoningResponseItem reasoningItem)
    {
        Console.WriteLine($"[Reasoning] ({reasoningItem.Status})");
    }
    else if (update is StreamingResponseOutputTextDeltaUpdate delta)
    {
        Console.Write(delta.Delta);
    }
}
```

### MCP Server

```csharp
using OpenAI;
using OpenAI.Responses;
using System.ClientModel.Primitives;
using Azure.Identity;

#pragma warning disable OPENAI001 //currently required for token based authentication

BearerTokenPolicy tokenPolicy = new(
    new DefaultAzureCredential(),
    "https://cognitiveservices.azure.com/.default");

OpenAIResponseClient client = new(
    model: "o4-mini",
    authenticationPolicy: tokenPolicy,
    options: new OpenAIClientOptions()
    {
        Endpoint = new Uri("https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1")
    }
);

ResponseCreationOptions options = new();
options.Tools.Add(ResponseTool.CreateMcpTool(
    serverLabel: "microsoft_learn",
    serverUri: new Uri("https://learn.microsoft.com/api/mcp"),
    toolCallApprovalPolicy: new McpToolCallApprovalPolicy(GlobalMcpToolCallApprovalPolicy.NeverRequireApproval)
));

OpenAIResponse response = (OpenAIResponse)client.CreateResponse([
    ResponseItem.CreateUserMessageItem([
        ResponseContentPart.CreateInputTextPart("Search for information about Azure Functions")
    ])
], options);

Console.WriteLine(response.GetOutputText());
```

## Error handling

### Error codes

| Status Code | Error Type |
|----|---|
| 400         | `Bad Request Error`          |
| 401         | `Authentication Error`      |
| 403         | `Permission Denied Error`    |
| 404         | `Not Found Error`            |
| 422         | `Unprocessable Entity Error` |
| 429         | `Rate Limit Error`           |
| 500         | `Internal Server Error`      |
| 503         | `Service Unavailable`       |
| 504         | `Gateway Timeout` |

### Retries

The client classes will automatically retry the following errors up to three more times using exponential backoff:

- 408 Request Timeout
- 429 Too Many Requests
- 500 Internal Server Error
- 502 Bad Gateway
- 503 Service Unavailable
- 504 Gateway Timeout


