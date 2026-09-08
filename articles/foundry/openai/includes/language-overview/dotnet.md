---
title: Azure OpenAI C# support
titleSuffix: Azure OpenAI in Microsoft Foundry Models
description: Azure OpenAI C# support.
author: alvinashcraft
manager: mcleans
ms.author: aashcraft
ms.service: microsoft-foundry
ms.subservice: foundry-openai
ms.topic: include
ms.date: 07/20/2026
ms.custom: include, classic-and-new, doc-kit-assisted
ai-usage: ai-assisted
---

[Source code](https://github.com/openai/openai-dotnet) | [Package](https://www.nuget.org/packages/OpenAI) | [API surface](https://github.com/openai/openai-dotnet/blob/main/api/OpenAI.netstandard2.0.cs)

The examples were tested with `OpenAI` 2.12.0, `Azure.Identity` 1.21.0, and .NET 8. The OpenAI package also targets .NET Standard 2.0 and later .NET versions.

## Install the packages

Install the OpenAI and Azure Identity packages:

```dotnetcli
dotnet add package OpenAI
dotnet add package Azure.Identity
```

The commands add both package references to your project.

## Create a response with Microsoft Entra ID

Use `DefaultAzureCredential` and `BearerTokenPolicy` to authenticate without storing an API key.

```csharp
using Azure.Identity;
using OpenAI.Responses;
using System.ClientModel.Primitives;

#pragma warning disable OPENAI001

var endpoint = new Uri(
    "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/");
var tokenPolicy = new BearerTokenPolicy(
    new DefaultAzureCredential(),
    "https://ai.azure.com/.default");
var openAIClient = new ResponsesClient(
    tokenPolicy,
    new ResponsesClientOptions { Endpoint = endpoint });

var response = await openAIClient.CreateResponseAsync(
    "gpt-5-mini",
    "Explain the purpose of an API in one sentence.");
Console.WriteLine(response.Value.GetOutputText());
```

The following output is representative. The exact wording might vary:

```output
An API allows software applications to communicate and exchange data through a defined set of rules.
```

Reference: [`ResponsesClient`](https://github.com/openai/openai-dotnet/blob/main/README.md#how-to-work-with-azure-openai)

## Create a response with an API key

API keys aren't recommended for production use. Store the key in the `AZURE_OPENAI_API_KEY` environment variable instead of placing it in source code.

```bash
export AZURE_OPENAI_API_KEY="<your-api-key>"
```

Then create the client and request:

```csharp
using OpenAI.Responses;
using System.ClientModel;

#pragma warning disable OPENAI001

var endpoint = new Uri(
    "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/");
var apiKey = Environment.GetEnvironmentVariable("AZURE_OPENAI_API_KEY")
    ?? throw new InvalidOperationException("AZURE_OPENAI_API_KEY is required.");
var openAIClient = new ResponsesClient(
    new ApiKeyCredential(apiKey),
    new ResponsesClientOptions { Endpoint = endpoint });

var response = await openAIClient.CreateResponseAsync(
    "gpt-5-mini",
    "Explain the purpose of an API in one sentence.");
Console.WriteLine(response.Value.GetOutputText());
```

The following output is representative. The exact wording might vary:

```output
An API allows software applications to communicate and exchange data through a defined set of rules.
```

Reference: [`CreateResponseAsync`](https://github.com/openai/openai-dotnet/blob/main/examples/Responses/Example01_SimpleResponseAsync.cs)

## Use Chat Completions

For new applications, use the Responses API. Use Chat Completions when you need its message-based interface or are maintaining an existing application.

```csharp
using Azure.Identity;
using OpenAI;
using OpenAI.Chat;
using System.ClientModel.Primitives;

#pragma warning disable OPENAI001

var endpoint = new Uri(
    "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/");
var tokenPolicy = new BearerTokenPolicy(
    new DefaultAzureCredential(),
    "https://ai.azure.com/.default");
var openAIClient = new ChatClient(
    model: "gpt-5-mini",
    authenticationPolicy: tokenPolicy,
    options: new OpenAIClientOptions { Endpoint = endpoint });

var completion = await openAIClient.CompleteChatAsync([
    new SystemChatMessage("You are a helpful assistant."),
    new UserChatMessage("Explain the purpose of an API.")
]);
Console.WriteLine(completion.Value.Content[0].Text);
```

The following output is representative. The exact wording might vary:

```output
An API allows software applications to communicate and exchange data through a defined set of rules.
```

Reference: [`ChatClient`](https://github.com/openai/openai-dotnet/tree/main/examples/Chat)

## Stream a response

Call `CreateResponseStreamingAsync` and process text delta updates as the model generates them:

```csharp
using OpenAI.Responses;
using System.ClientModel;

#pragma warning disable OPENAI001

var endpoint = new Uri(
    "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/");
var apiKey = Environment.GetEnvironmentVariable("AZURE_OPENAI_API_KEY")
    ?? throw new InvalidOperationException("AZURE_OPENAI_API_KEY is required.");
var openAIClient = new ResponsesClient(
    new ApiKeyCredential(apiKey),
    new ResponsesClientOptions { Endpoint = endpoint });

// Stream text as the model generates it.
var updates = openAIClient.CreateResponseStreamingAsync(
    "gpt-5-mini",
    "Explain the purpose of an API in one sentence.");
await foreach (var update in updates)
{
    if (update is StreamingResponseOutputTextDeltaUpdate delta)
    {
        Console.Write(delta.Delta);
    }
}
```

The following streamed output is representative. The exact wording might vary:

```output
An API allows software applications to communicate and exchange data through a defined set of rules.
```

Reference: [`CreateResponseStreamingAsync`](https://github.com/openai/openai-dotnet/blob/main/examples/Responses/Example02_SimpleResponseStreamingAsync.cs)

## Handle errors and retries

The client automatically retries HTTP 408, 429, 500, 502, 503, and 504 responses with exponential backoff. Configure the retry policy through the client options when you need different behavior. Catch `ClientResultException` to inspect the HTTP status and error details for a failed request.

For diagnostics, retain the `ClientResult<T>` returned by an operation and inspect its raw response headers. Failed operations expose status information through `ClientResultException`.

Reference: [Error handling and client result details](https://github.com/openai/openai-dotnet#how-to-handle-errors)

## More SDK examples

- [Use the Responses API](../../how-to/responses.md)
- [Generate embeddings](../../how-to/embeddings.md)
- [Analyze images](../../how-to/gpt-with-vision.md)
- [Fine-tune a model](../../how-to/fine-tuning.md)
