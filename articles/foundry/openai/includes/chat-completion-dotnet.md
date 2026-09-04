---
title: Work with the Chat Completions API
titleSuffix: Azure OpenAI
description: Learn how to work with the Chat Completions API using the Azure OpenAI .NET SDK.
author: alvinashcraft
ms.author: aashcraft
ms.service: microsoft-foundry
ms.subservice: foundry-openai
ms.topic: include
ms.date: 07/22/2026
manager: mcleans
keywords: ChatGPT
ms.custom: doc-kit-assisted
ai-usage: ai-assisted
---

## Set up

1. Create a new .NET console application:

    ```shell
    dotnet new console -n chat-completions
    cd chat-completions
    ```

1. Install the required NuGet packages:

    ```dotnetcli
    dotnet add package OpenAI
    dotnet add package Azure.Identity
    ```

    The OpenAI package is stable. The Microsoft Entra ID examples use an experimental custom authentication constructor and suppress the `OPENAI001` warning.

1. For keyless authentication with Microsoft Entra ID, sign in to Azure:

    ```shell
    az login
    ```

## Work with chat completion models

The following code snippet shows the most basic way to interact with models that use the Chat Completions API.

> [!NOTE]
> The [responses API](../how-to/responses.md) uses the same chat style of interaction, but supports the latest features that aren't supported with the older chat completions API.

# [Microsoft Entra ID](#tab/dotnet-secure)

```csharp
using Azure.Identity;
using OpenAI;
using OpenAI.Chat;
using System.ClientModel.Primitives;

#pragma warning disable OPENAI001

BearerTokenPolicy tokenPolicy = new(
    new DefaultAzureCredential(),
    "https://ai.azure.com/.default");

ChatClient client = new(
    model: "YOUR-DEPLOYMENT-NAME",
    authenticationPolicy: tokenPolicy,
    options: new OpenAIClientOptions()
    {
        Endpoint = new Uri("https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/")
    }
);

ChatCompletion completion = await client.CompleteChatAsync(
[
    new SystemChatMessage("Assistant is a large language model trained by OpenAI."),
    new UserChatMessage("Who were the founders of Microsoft?"),
]);

Console.WriteLine(completion.Content[0].Text);
```

# [API Key](#tab/dotnet-key)

```csharp
using OpenAI;
using OpenAI.Chat;
using System.ClientModel;

ChatClient client = new(
    model: "YOUR-DEPLOYMENT-NAME",
    credential: new ApiKeyCredential(
        Environment.GetEnvironmentVariable("AZURE_OPENAI_API_KEY")),
    options: new OpenAIClientOptions()
    {
        Endpoint = new Uri("https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/")
    }
);

ChatCompletion completion = await client.CompleteChatAsync(
[
    new SystemChatMessage("Assistant is a large language model trained by OpenAI."),
    new UserChatMessage("Who were the founders of Microsoft?"),
]);

Console.WriteLine(completion.Content[0].Text);
```

---

```output
Microsoft was founded by Bill Gates and Paul Allen. They established the company on April 4, 1975. Bill Gates served as the CEO of Microsoft until 2000 and later as Chairman and Chief Software Architect until his retirement in 2008, while Paul Allen left the company in 1983 but remained on the board of directors until 2000.
```

Every response includes a `FinishReason`. The possible values for `FinishReason` are:

* **Stop**: The API returned complete model output.
* **Length**: Incomplete model output because of the `MaxOutputTokenCount` parameter or the token limit.
* **ContentFilter**: Omitted content because of a content filter flag.
* **ToolCalls**: The model called a tool.
* **FunctionCall**: The model called a function. This value is deprecated.

Set `MaxOutputTokenCount` high enough for the expected response. A higher value helps prevent the model from stopping before it reaches the end of the message.

## Work with the Chat Completions API

OpenAI trained chat completion models to accept input formatted as a conversation. The messages parameter takes an array of message objects with a conversation organized by role. When you use the .NET SDK, you use strongly typed message classes for each role.

The format of a basic chat completion is:

```csharp
new SystemChatMessage("Provide some context and/or instructions to the model"),
new UserChatMessage("The user's message goes here")
```

A conversation with one example answer followed by a question would look like:

```csharp
new SystemChatMessage("Provide some context and/or instructions to the model."),
new UserChatMessage("Example question goes here."),
new AssistantChatMessage("Example answer goes here."),
new UserChatMessage("First question/message for the model to actually respond to.")
```

### System role

The system role, also known as the system message, is included at the beginning of the array. This message provides the initial instructions to the model. You can provide various information in the system role, such as:

* A brief description of the assistant.
* Personality traits of the assistant.
* Instructions or rules you want the assistant to follow.
* Data or information needed for the model, such as relevant questions from an FAQ.

Customize the system role for your use case or include basic instructions. The system message is optional, but include at least a basic one to get the best results.

### Messages

After the system role, you can include a series of messages between the `user` and the `assistant`.

```csharp
new UserChatMessage("What is thermodynamics?")
```

To trigger a response from the model, end with a user message to indicate that it's the assistant's turn to respond. You can also include a series of example messages between the user and the assistant as a way to do few-shot learning.

### Message prompt examples

The following section shows examples of different styles of prompts that you can use with chat completions models. These examples are only a starting point. You can experiment with different prompts to customize the behavior for your own use cases.

#### Basic example

If you want your chat completions model to behave similarly to [chatgpt.com](https://chatgpt.com/), you can use a basic system message like `Assistant is a large language model trained by OpenAI.`

```csharp
new SystemChatMessage("Assistant is a large language model trained by OpenAI."),
new UserChatMessage("Who were the founders of Microsoft?")
```

#### Example with instructions

For some scenarios, you might want to give more instructions to the model to define guardrails for what the model is able to do.

```csharp
new SystemChatMessage(@"Assistant is an intelligent chatbot designed to help users answer their tax related questions.
Instructions:
- Only answer questions related to taxes.
- If you're unsure of an answer, you can say ""I don't know"" or ""I'm not sure"" and recommend users go to the IRS website for more information."),
new UserChatMessage("When are my taxes due?")
```

#### Use data for grounding

You can also include relevant data or information in the system message to give the model extra context for the conversation. If you need to include only a small amount of information, you can hard code it in the system message. If you have a large amount of data that the model should be aware of, you can use [embeddings](../tutorials/embeddings.md?tabs=command-line) or a product like [Azure AI Search](https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/revolutionize-your-enterprise-data-with-chatgpt-next-gen-apps-w-azure-openai-and/3762087) to retrieve the most relevant information at query time.

```csharp
new SystemChatMessage(@"Assistant is an intelligent chatbot designed to help users answer technical questions about Azure OpenAI in Microsoft Foundry Models. Only answer questions using the context below and if you're not sure of an answer, you can say 'I don't know'.

Context:
- Azure OpenAI provides REST API access to OpenAI models, including GPT-5, GPT-4.1, and Embeddings model series.
- Azure OpenAI gives customers advanced language AI with GPT-5, GPT-image, and Embeddings models with the security and enterprise capabilities of Azure. Azure OpenAI co-develops the APIs with OpenAI, ensuring compatibility and a smooth transition between the services.
- At Microsoft, we're committed to the advancement of AI driven by principles that put people first. Microsoft has made significant investments to help guard against abuse and unintended harm, which includes requiring applicants to show well-defined use cases, incorporating Microsoft's principles for responsible AI use."),
new UserChatMessage("What is Azure OpenAI?")
```

#### Few-shot learning with chat completion

You can also give few-shot examples to the model. You can include a series of messages between the user and the assistant in the prompt as few-shot examples. By using these examples, you can seed answers to common questions to prime the model or teach particular behaviors to the model.

This example uses current chat completion models such as `gpt-5-mini` and `gpt-5`.

```csharp
new SystemChatMessage("Assistant is an intelligent chatbot designed to help users answer their tax related questions."),
new UserChatMessage("When do I need to file my taxes by?"),
new AssistantChatMessage("Check the current individual filing deadline at https://www.irs.gov/filing/individuals/when-to-file."),
new UserChatMessage("How can I check the status of my tax refund?"),
new AssistantChatMessage("Check your refund status at https://www.irs.gov/refunds.")
```

#### Use chat completion for nonchat scenarios

The Chat Completions API is designed to work with multi-turn conversations, but it also works well for nonchat scenarios.

For example, for an entity extraction scenario, you might use the following prompt:

```csharp
new SystemChatMessage(@"You are an assistant designed to extract entities from text. Users will paste in a string of text and you will respond with entities you've extracted from the text as a JSON object. Here's an example of your output format:
{
   ""name"": """",
   ""company"": """",
   ""phone_number"": """"
}"),
new UserChatMessage("Hello. My name is Robert Smith. I'm calling from Contoso Insurance, Delaware. My colleague mentioned that you are interested in learning about our comprehensive benefits policy. Could you give me a call back at (555) 346-9322 when you get a chance so we can go over the benefits?")
```

## Create a basic conversation loop

The preceding examples show the basic mechanics of interacting with the Chat Completions API. This example shows how to create a conversation loop that performs the following actions:

- Continuously takes console input and properly formats it as part of the messages list as user role content.
- Outputs responses that are printed to the console and formatted and added to the messages list as assistant role content.

Every time you ask a new question, the request sends the running conversation transcript along with the latest question. Because the model has no memory, send an updated transcript with each question or the model loses the context of previous questions and answers.

# [Microsoft Entra ID](#tab/dotnet-secure)

```csharp
using Azure.Identity;
using OpenAI;
using OpenAI.Chat;
using System.ClientModel.Primitives;

#pragma warning disable OPENAI001

BearerTokenPolicy tokenPolicy = new(
    new DefaultAzureCredential(),
    "https://ai.azure.com/.default");

ChatClient client = new(
    model: "YOUR-DEPLOYMENT-NAME",
    authenticationPolicy: tokenPolicy,
    options: new OpenAIClientOptions()
    {
        Endpoint = new Uri("https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/")
    }
);

List<ChatMessage> conversation =
[
    new SystemChatMessage("You are a helpful assistant."),
];

while (true)
{
    Console.Write("Q: ");
    string? userInput = Console.ReadLine();
    if (string.IsNullOrWhiteSpace(userInput)) break;

    conversation.Add(new UserChatMessage(userInput));

    ChatCompletion response = await client.CompleteChatAsync(conversation);
    string assistantMessage = response.Content[0].Text;

    conversation.Add(new AssistantChatMessage(assistantMessage));
    Console.WriteLine($"\n{assistantMessage}\n");
}
```

# [API Key](#tab/dotnet-key)

```csharp
using OpenAI;
using OpenAI.Chat;
using System.ClientModel;

ChatClient client = new(
    model: "YOUR-DEPLOYMENT-NAME",
    credential: new ApiKeyCredential(
        Environment.GetEnvironmentVariable("AZURE_OPENAI_API_KEY")),
    options: new OpenAIClientOptions()
    {
        Endpoint = new Uri("https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/")
    }
);

List<ChatMessage> conversation =
[
    new SystemChatMessage("You are a helpful assistant."),
];

while (true)
{
    Console.Write("Q: ");
    string? userInput = Console.ReadLine();
    if (string.IsNullOrWhiteSpace(userInput)) break;

    conversation.Add(new UserChatMessage(userInput));

    ChatCompletion response = await client.CompleteChatAsync(conversation);
    string assistantMessage = response.Content[0].Text;

    conversation.Add(new AssistantChatMessage(assistantMessage));
    Console.WriteLine($"\n{assistantMessage}\n");
}
```

---

When you run the preceding code, you get a blank console window. Enter your first question in the window and then select the `Enter` key. After the response is returned, you can repeat the process and keep asking questions.

## Manage conversations

The previous example runs until the model's token limit (context window) is reached. With each question asked and answer received, the `conversation` list grows in size. The combined token count of your messages plus the requested output tokens must stay within the model's limit, or the request fails. Consult the [models page](../../foundry-models/concepts/models-sold-directly-by-azure.md) for current token limits.

It's your responsibility to ensure that the prompt and completion fall within the token limit. For longer conversations, you need to keep track of the token count and only send the model a prompt that falls within the limit. Alternatively, with the [responses API](../how-to/responses.md) you can have the API handle truncation and management of the conversation history for you.

The following code sample trims the conversation at a 4,096-token demonstration threshold. Set `TokenLimit` to the context window of your deployed model for production use. The sample removes the oldest non-system messages to keep the conversation within bounds.

Install the [Microsoft.ML.Tokenizers](https://www.nuget.org/packages/Microsoft.ML.Tokenizers) and [Microsoft.ML.Tokenizers.Data.O200kBase](https://www.nuget.org/packages/Microsoft.ML.Tokenizers.Data.O200kBase) packages for accurate token counting:

```dotnetcli
dotnet add package Microsoft.ML.Tokenizers
dotnet add package Microsoft.ML.Tokenizers.Data.O200kBase
```

# [Microsoft Entra ID](#tab/dotnet-secure)

```csharp
using Azure.Identity;
using Microsoft.ML.Tokenizers;
using OpenAI;
using OpenAI.Chat;
using System.ClientModel.Primitives;

#pragma warning disable OPENAI001

BearerTokenPolicy tokenPolicy = new(
    new DefaultAzureCredential(),
    "https://ai.azure.com/.default");

ChatClient client = new(
    model: "YOUR-DEPLOYMENT-NAME",
    authenticationPolicy: tokenPolicy,
    options: new OpenAIClientOptions()
    {
        Endpoint = new Uri("https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/")
    }
);

const int MaxResponseTokens = 250;
const int TokenLimit = 4096;

var tokenizer = TiktokenTokenizer.CreateForModel("gpt-4o");

List<ChatMessage> conversation =
[
    new SystemChatMessage("You are a helpful assistant."),
];

static int CountTokens(TiktokenTokenizer tokenizer, IEnumerable<ChatMessage> messages)
{
    int count = 3; // base overhead for reply priming
    foreach (var message in messages)
    {
        count += 4; // per-message overhead
        string content = message switch
        {
            SystemChatMessage s => s.Content[0].Text ?? string.Empty,
            UserChatMessage u => u.Content[0].Text ?? string.Empty,
            AssistantChatMessage a => a.Content[0].Text ?? string.Empty,
            _ => string.Empty
        };
        count += tokenizer.CountTokens(content);
    }
    return count;
}

while (true)
{
    Console.Write("Q: ");
    string? userInput = Console.ReadLine();
    if (string.IsNullOrWhiteSpace(userInput)) break;

    conversation.Add(new UserChatMessage(userInput));

    int historyTokens = CountTokens(tokenizer, conversation);
    while (historyTokens + MaxResponseTokens >= TokenLimit && conversation.Count > 2)
    {
        conversation.RemoveAt(1); // remove oldest non-system message
        historyTokens = CountTokens(tokenizer, conversation);
    }

    ChatCompletionOptions options = new() { MaxOutputTokenCount = MaxResponseTokens };
    ChatCompletion response = await client.CompleteChatAsync(conversation, options);
    string assistantMessage = response.Content[0].Text;

    conversation.Add(new AssistantChatMessage(assistantMessage));
    Console.WriteLine($"\n{assistantMessage}\n");
}
```

# [API Key](#tab/dotnet-key)

```csharp
using Microsoft.ML.Tokenizers;
using OpenAI;
using OpenAI.Chat;
using System.ClientModel;

ChatClient client = new(
    model: "YOUR-DEPLOYMENT-NAME",
    credential: new ApiKeyCredential(
        Environment.GetEnvironmentVariable("AZURE_OPENAI_API_KEY")),
    options: new OpenAIClientOptions()
    {
        Endpoint = new Uri("https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/")
    }
);

const int MaxResponseTokens = 250;
const int TokenLimit = 4096;

var tokenizer = TiktokenTokenizer.CreateForModel("gpt-4o");

List<ChatMessage> conversation =
[
    new SystemChatMessage("You are a helpful assistant."),
];

static int CountTokens(TiktokenTokenizer tokenizer, IEnumerable<ChatMessage> messages)
{
    int count = 3; // base overhead for reply priming
    foreach (var message in messages)
    {
        count += 4; // per-message overhead
        string content = message switch
        {
            SystemChatMessage s => s.Content[0].Text ?? string.Empty,
            UserChatMessage u => u.Content[0].Text ?? string.Empty,
            AssistantChatMessage a => a.Content[0].Text ?? string.Empty,
            _ => string.Empty
        };
        count += tokenizer.CountTokens(content);
    }
    return count;
}

while (true)
{
    Console.Write("Q: ");
    string? userInput = Console.ReadLine();
    if (string.IsNullOrWhiteSpace(userInput)) break;

    conversation.Add(new UserChatMessage(userInput));

    int historyTokens = CountTokens(tokenizer, conversation);
    while (historyTokens + MaxResponseTokens >= TokenLimit && conversation.Count > 2)
    {
        conversation.RemoveAt(1); // remove oldest non-system message
        historyTokens = CountTokens(tokenizer, conversation);
    }

    ChatCompletionOptions options = new() { MaxOutputTokenCount = MaxResponseTokens };
    ChatCompletion response = await client.CompleteChatAsync(conversation, options);
    string assistantMessage = response.Content[0].Text;

    conversation.Add(new AssistantChatMessage(assistantMessage));
    Console.WriteLine($"\n{assistantMessage}\n");
}
```

---

In this example, after the token count is reached, the oldest messages in the conversation transcript are removed. We always preserve the system message and only remove user or assistant messages. Over time, this method of managing the conversation can cause the conversation quality to degrade as the model gradually loses the context of the earlier portions of the conversation.

An alternative approach is to limit the conversation duration to the maximum token length or a specific number of turns. After the maximum token limit is reached, the model would lose context if you were to allow the conversation to continue. You can prompt the user to begin a new conversation and clear the messages list to start a new conversation with the full token limit available.

## Troubleshooting

### Failed to create completion as the model generated invalid Unicode output

- **Error code:** 500
- **Error message:** `500 - InternalServerError: Error code: 500 - {"error": {"message": "Failed to create completion as the model generated invalid Unicode output"}}`
- **Workaround:** Set `Temperature` in `ChatCompletionOptions` to less than 1, and use a client with retry logic. Retrying the request often succeeds.

### Common errors

- **401/403 (authentication)**: Verify your API key or confirm you have Microsoft Entra ID access to the Azure OpenAI resource.
- **400/404 (deployment not found)**: Confirm that the model name passed to the `ChatClient` constructor matches your deployment name.
- **Invalid endpoint**: Confirm that the `Endpoint` URI in `OpenAIClientOptions` points to `https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/`.
