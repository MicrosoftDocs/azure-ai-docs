---
title: How to use chat completions with Azure AI model inference
titleSuffix: Azure AI Foundry
description: Learn how to generate chat completions with Azure AI model inference
manager: scottpolly
author: mopeakande
reviewer: santiagxf
ms.service: azure-ai-model-inference
ms.topic: how-to
ms.date: 1/21/2025
ms.author: mopeakande
ms.reviewer: fasantia
ms.custom: references_regions, tool_generated
zone_pivot_groups: azure-ai-inference-samples
---

[!INCLUDE [Feature preview](~/reusable-content/ce-skilling/azure/includes/ai-studio/includes/feature-preview.md)]

This article explains how to use chat completions API with models deployed to Azure AI model inference in Azure AI services.

## Prerequisites

To use chat completion models in your application, you need:

[!INCLUDE [how-to-prerequisites](../how-to-prerequisites.md)]

* A chat completions model deployment. If you don't have one read [Add and configure models to Azure AI services](../../how-to/create-model-deployments.md) to add a chat completions model to your resource.

* Install the [Azure AI inference package](https://aka.ms/azsdk/azure-ai-inference/python/reference) with the following command:

    ```bash
    dotnet add package Azure.AI.Inference --prerelease
    ```
    
* If you are using Entra ID, you also need the following package:

    ```bash
    dotnet add package Azure.Identity
    ```

## Use chat completions

First, create the client to consume the model. The following code uses an endpoint URL and key that are stored in environment variables.


```csharp
ChatCompletionsClient client = new ChatCompletionsClient(
    new Uri(Environment.GetEnvironmentVariable("AZURE_INFERENCE_ENDPOINT")),
    new AzureKeyCredential(Environment.GetEnvironmentVariable("AZURE_INFERENCE_CREDENTIAL")),
    "mistral-large-2407"
);
```

If you have configured the resource to with **Microsoft Entra ID** support, you can use the following code snippet to create a client.


```csharp
client = new ChatCompletionsClient(
    new Uri(Environment.GetEnvironmentVariable("AZURE_INFERENCE_ENDPOINT")),
    new DefaultAzureCredential(includeInteractiveCredentials: true),
    "mistral-large-2407"
);
```

### Create a chat completion request

The following example shows how you can create a basic chat completions request to the model.

```csharp
ChatCompletionsOptions requestOptions = new ChatCompletionsOptions()
{
    Messages = {
        new ChatRequestSystemMessage("You are a helpful assistant."),
        new ChatRequestUserMessage("How many languages are in the world?")
    },
};

Response<ChatCompletions> response = client.Complete(requestOptions);
```

> [!NOTE]
> Some models don't support system messages (`role="system"`). When you use the Azure AI model inference API, system messages are translated to user messages, which is the closest capability available. This translation is offered for convenience, but it's important for you to verify that the model is following the instructions in the system message with the right level of confidence.

The response is as follows, where you can see the model's usage statistics:


```csharp
Console.WriteLine($"Response: {response.Value.Content}");
Console.WriteLine($"Model: {response.Value.Model}");
Console.WriteLine("Usage:");
Console.WriteLine($"\tPrompt tokens: {response.Value.Usage.PromptTokens}");
Console.WriteLine($"\tTotal tokens: {response.Value.Usage.TotalTokens}");
Console.WriteLine($"\tCompletion tokens: {response.Value.Usage.CompletionTokens}");
```

```console
Response: As of now, it's estimated that there are about 7,000 languages spoken around the world. However, this number can vary as some languages become extinct and new ones develop. It's also important to note that the number of speakers can greatly vary between languages, with some having millions of speakers and others only a few hundred.
Model: mistral-large-2407
Usage: 
  Prompt tokens: 19
  Total tokens: 91
  Completion tokens: 72
```

Inspect the `usage` section in the response to see the number of tokens used for the prompt, the total number of tokens generated, and the number of tokens used for the completion.

#### Stream content

By default, the completions API returns the entire generated content in a single response. If you're generating long completions, waiting for the response can take many seconds.

You can _stream_ the content to get it as it's being generated. Streaming content allows you to start processing the completion as content becomes available. This mode returns an object that streams back the response as [data-only server-sent events](https://html.spec.whatwg.org/multipage/server-sent-events.html#server-sent-events). Extract chunks from the delta field, rather than the message field.

To stream completions, use `CompleteStreamingAsync` method when you call the model. Notice that in this example we the call is wrapped in an asynchronous method.


```csharp
static async Task StreamMessageAsync(ChatCompletionsClient client)
{
    ChatCompletionsOptions requestOptions = new ChatCompletionsOptions()
    {
        Messages = {
            new ChatRequestSystemMessage("You are a helpful assistant."),
            new ChatRequestUserMessage("How many languages are in the world? Write an essay about it.")
        },
        MaxTokens=4096
    };

    StreamingResponse<StreamingChatCompletionsUpdate> streamResponse = await client.CompleteStreamingAsync(requestOptions);

    await PrintStream(streamResponse);
}
```

To visualize the output, define an asynchronous method to print the stream in the console.

```csharp
static async Task PrintStream(StreamingResponse<StreamingChatCompletionsUpdate> response)
{
    await foreach (StreamingChatCompletionsUpdate chatUpdate in response)
    {
        if (chatUpdate.Role.HasValue)
        {
            Console.Write($"{chatUpdate.Role.Value.ToString().ToUpperInvariant()}: ");
        }
        if (!string.IsNullOrEmpty(chatUpdate.ContentUpdate))
        {
            Console.Write(chatUpdate.ContentUpdate);
        }
    }
}
```

You can visualize how streaming generates content:


```csharp
StreamMessageAsync(client).GetAwaiter().GetResult();
```

#### Explore more parameters supported by the inference client

Explore other parameters that you can specify in the inference client. For a full list of all the supported parameters and their corresponding documentation, see [Azure AI Model Inference API reference](https://aka.ms/azureai/modelinference).

```csharp
requestOptions = new ChatCompletionsOptions()
{
    Messages = {
        new ChatRequestSystemMessage("You are a helpful assistant."),
        new ChatRequestUserMessage("How many languages are in the world?")
    },
    PresencePenalty = 0.1f,
    FrequencyPenalty = 0.8f,
    MaxTokens = 2048,
    StopSequences = { "<|endoftext|>" },
    Temperature = 0,
    NucleusSamplingFactor = 1,
    ResponseFormat = new ChatCompletionsResponseFormatText()
};

response = client.Complete(requestOptions);
Console.WriteLine($"Response: {response.Value.Content}");
```

Some models don't support JSON output formatting. You can always prompt the model to generate JSON outputs. However, such outputs are not guaranteed to be valid JSON.

If you want to pass a parameter that isn't in the list of supported parameters, you can pass it to the underlying model using *extra parameters*. See [Pass extra parameters to the model](#pass-extra-parameters-to-the-model).

#### Create JSON outputs

Some models can create JSON outputs. Set `response_format` to `json_object` to enable JSON mode and guarantee that the message the model generates is valid JSON. You must also instruct the model to produce JSON yourself via a system or user message. Also, the message content might be partially cut off if `finish_reason="length"`, which indicates that the generation exceeded `max_tokens` or that the conversation exceeded the max context length.


```csharp
requestOptions = new ChatCompletionsOptions()
{
    Messages = {
        new ChatRequestSystemMessage(
            "You are a helpful assistant that always generate responses in JSON format, " +
            "using. the following format: { \"answer\": \"response\" }."
        ),
        new ChatRequestUserMessage(
            "How many languages are in the world?"
        )
    },
    ResponseFormat = new ChatCompletionsResponseFormatJsonObject()
};

response = client.Complete(requestOptions);
Console.WriteLine($"Response: {response.Value.Content}");
```

### Pass extra parameters to the model

The Azure AI Model Inference API allows you to pass extra parameters to the model. The following code example shows how to pass the extra parameter `logprobs` to the model. 


```csharp
requestOptions = new ChatCompletionsOptions()
{
    Messages = {
        new ChatRequestSystemMessage("You are a helpful assistant."),
        new ChatRequestUserMessage("How many languages are in the world?")
    },
    AdditionalProperties = { { "logprobs", BinaryData.FromString("true") } },
};

response = client.Complete(requestOptions, extraParams: ExtraParameters.PassThrough);
Console.WriteLine($"Response: {response.Value.Content}");
```

Before you pass extra parameters to the Azure AI model inference API, make sure your model supports those extra parameters. When the request is made to the underlying model, the header `extra-parameters` is passed to the model with the value `pass-through`. This value tells the endpoint to pass the extra parameters to the model. Use of extra parameters with the model doesn't guarantee that the model can actually handle them. Read the model's documentation to understand which extra parameters are supported.

### Use tools

Some models support the use of tools, which can be an extraordinary resource when you need to offload specific tasks from the language model and instead rely on a more deterministic system or even a different language model. The Azure AI Model Inference API allows you to define tools in the following way.

The following code example creates a tool definition that is able to look from flight information from two different cities.


```csharp
FunctionDefinition flightInfoFunction = new FunctionDefinition("getFlightInfo")
{
    Description = "Returns information about the next flight between two cities. This includes the name of the airline, flight number and the date and time of the next flight",
    Parameters = BinaryData.FromObjectAsJson(new
    {
        Type = "object",
        Properties = new
        {
            origin_city = new
            {
                Type = "string",
                Description = "The name of the city where the flight originates"
            },
            destination_city = new
            {
                Type = "string",
                Description = "The flight destination city"
            }
        }
    },
        new JsonSerializerOptions() { PropertyNamingPolicy = JsonNamingPolicy.CamelCase }
    )
};

ChatCompletionsFunctionToolDefinition getFlightTool = new ChatCompletionsFunctionToolDefinition(flightInfoFunction);
```

In this example, the function's output is that there are no flights available for the selected route, but the user should consider taking a train.


```csharp
static string getFlightInfo(string loc_origin, string loc_destination)
{
    return JsonSerializer.Serialize(new
    {
        info = $"There are no flights available from {loc_origin} to {loc_destination}. You " +
        "should take a train, specially if it helps to reduce CO2 emissions."
    });
}
```

> [!NOTE]
> Cohere models require a tool's responses to be a valid JSON content formatted as a string. When constructing messages of type *Tool*, ensure the response is a valid JSON string.

Prompt the model to book flights with the help of this function:


```csharp
var chatHistory = new List<ChatRequestMessage>(){
        new ChatRequestSystemMessage(
            "You are a helpful assistant that help users to find information about traveling, " +
            "how to get to places and the different transportations options. You care about the" +
            "environment and you always have that in mind when answering inqueries."
        ),
        new ChatRequestUserMessage("When is the next flight from Miami to Seattle?")
    };

requestOptions = new ChatCompletionsOptions(chatHistory);
requestOptions.Tools.Add(getFlightTool);
requestOptions.ToolChoice = ChatCompletionsToolChoice.Auto;

response = client.Complete(requestOptions);
```

You can inspect the response to find out if a tool needs to be called. Inspect the finish reason to determine if the tool should be called. Remember that multiple tool types can be indicated. This example demonstrates a tool of type `function`.


```csharp
var responseMessage = response.Value;
var toolsCall = responseMessage.ToolCalls;

Console.WriteLine($"Finish reason: {response.Value.Choices[0].FinishReason}");
Console.WriteLine($"Tool call: {toolsCall[0].Id}");
```

To continue, append this message to the chat history:


```csharp
requestOptions.Messages.Add(new ChatRequestAssistantMessage(response.Value));
```

Now, it's time to call the appropriate function to handle the tool call. The following code snippet iterates over all the tool calls indicated in the response and calls the corresponding function with the appropriate parameters. The response is also appended to the chat history.


```csharp
foreach (ChatCompletionsToolCall tool in toolsCall)
{
    if (tool is ChatCompletionsFunctionToolCall functionTool)
    {
        // Get the tool details:
        string callId = functionTool.Id;
        string toolName = functionTool.Name;
        string toolArgumentsString = functionTool.Arguments;
        Dictionary<string, object> toolArguments = JsonSerializer.Deserialize<Dictionary<string, object>>(toolArgumentsString);

        // Here you have to call the function defined. In this particular example we use 
        // reflection to find the method we definied before in an static class called 
        // `ChatCompletionsExamples`. Using reflection allows us to call a function 
        // by string name. Notice that this is just done for demonstration purposes as a 
        // simple way to get the function callable from its string name. Then we can call 
        // it with the corresponding arguments.

        var flags = BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Static;
        string toolResponse = (string)typeof(ChatCompletionsExamples).GetMethod(toolName, flags).Invoke(null, toolArguments.Values.Cast<object>().ToArray());

        Console.WriteLine("->", toolResponse);
        requestOptions.Messages.Add(new ChatRequestToolMessage(toolResponse, callId));
    }
    else
        throw new Exception("Unsupported tool type");
}
```

View the response from the model:


```csharp
response = client.Complete(requestOptions);
```

### Apply content safety

The Azure AI model inference API supports [Azure AI content safety](https://aka.ms/azureaicontentsafety). When you use deployments with Azure AI content safety turned on, inputs and outputs pass through an ensemble of classification models aimed at detecting and preventing the output of harmful content. The content filtering system detects and takes action on specific categories of potentially harmful content in both input prompts and output completions.

The following example shows how to handle events when the model detects harmful content in the input prompt and content safety is enabled.


```csharp
try
{
    requestOptions = new ChatCompletionsOptions()
    {
        Messages = {
            new ChatRequestSystemMessage("You are an AI assistant that helps people find information."),
            new ChatRequestUserMessage(
                "Chopping tomatoes and cutting them into cubes or wedges are great ways to practice your knife skills."
            ),
        },
    };

    response = client.Complete(requestOptions);
    Console.WriteLine(response.Value.Content);
}
catch (RequestFailedException ex)
{
    if (ex.ErrorCode == "content_filter")
    {
        Console.WriteLine($"Your query has trigger Azure Content Safety: {ex.Message}");
    }
    else
    {
        throw;
    }
}
```

> [!TIP]
> To learn more about how you can configure and control Azure AI content safety settings, check the [Azure AI content safety documentation](https://aka.ms/azureaicontentsafety).

## Use chat completions with images

Some models can reason across text and images and generate text completions based on both kinds of input. In this section, you explore the capabilities of Some models for vision in a chat fashion:

> [!IMPORTANT]
> Some models support only one image for each turn in the chat conversation and only the last image is retained in context. If you add multiple images, it results in an error.

To see this capability, download an image and encode the information as `base64` string. The resulting data should be inside of a [data URL](https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/Data_URLs):


```csharp
string imageUrl = "https://news.microsoft.com/source/wp-content/uploads/2024/04/The-Phi-3-small-language-models-with-big-potential-1-1900x1069.jpg";
string imageFormat = "jpeg";
HttpClient httpClient = new HttpClient();
httpClient.DefaultRequestHeaders.Add("User-Agent", "Mozilla/5.0");
byte[] imageBytes = httpClient.GetByteArrayAsync(imageUrl).Result;
string imageBase64 = Convert.ToBase64String(imageBytes);
string dataUrl = $"data:image/{imageFormat};base64,{imageBase64}";
```

Visualize the image:

:::image type="content" source="../../../../ai-studio/media/how-to/sdks/small-language-models-chart-example.jpg" alt-text="A chart displaying the relative capabilities between large language models and small language models." lightbox="../../../../ai-studio/media/how-to/sdks/small-language-models-chart-example.jpg":::

Now, create a chat completion request with the image:


```csharp
ChatCompletionsOptions requestOptions = new ChatCompletionsOptions()
{
    Messages = {
        new ChatRequestSystemMessage("You are an AI assistant that helps people find information."),
        new ChatRequestUserMessage([
            new ChatMessageTextContentItem("Which conclusion can be extracted from the following chart?"),
            new ChatMessageImageContentItem(new Uri(dataUrl))
        ]),
    },
    MaxTokens=2048,
};

var response = client.Complete(requestOptions);
Console.WriteLine(response.Value.Content);
```

The response is as follows, where you can see the model's usage statistics:


```csharp
Console.WriteLine($"{response.Value.Role}: {response.Value.Content}");
Console.WriteLine($"Model: {response.Value.Model}");
Console.WriteLine("Usage:");
Console.WriteLine($"\tPrompt tokens: {response.Value.Usage.PromptTokens}");
Console.WriteLine($"\tTotal tokens: {response.Value.Usage.TotalTokens}");
Console.WriteLine($"\tCompletion tokens: {response.Value.Usage.CompletionTokens}");
```

```console
ASSISTANT: The chart illustrates that larger models tend to perform better in quality, as indicated by their size in billions of parameters. However, there are exceptions to this trend, such as Phi-3-medium and Phi-3-small, which outperform smaller models in quality. This suggests that while larger models generally have an advantage, there might be other factors at play that influence a model's performance.
Model: mistral-large-2407
Usage: 
  Prompt tokens: 2380
  Completion tokens: 126
  Total tokens: 2506
```
