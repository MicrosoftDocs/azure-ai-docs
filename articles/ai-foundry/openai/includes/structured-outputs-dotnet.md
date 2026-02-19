---
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: how-to
ms.date: 12/6/2025
author: mrbullwinkle
ms.author: mbullwin
zone_pivot_groups: structured-outputs
---

## Getting started

Add the following packages to your project:

- **[OpenAI](https://www.nuget.org/packages/OpenAI)**: Standard OpenAI .NET library.
- **[Azure.Identity](https://www.nuget.org/packages/Azure.Identity)**: Provides Microsoft Entra ID token authentication support across the Azure SDK libraries.

```dotnetcli
dotnet add package OpenAI
dotnet add package Azure.Identity
```

# [Microsoft Entra ID](#tab/dotnet-entra-id)

If you're new to using Microsoft Entra ID for authentication see [How to configure Azure OpenAI in Microsoft Foundry Models with Microsoft Entra ID authentication](../how-to/managed-identity.md).

```csharp
using Azure.Identity;
using OpenAI;
using OpenAI.Chat;
using System.ClientModel.Primitives;
using System.Text.Json;

#pragma warning disable OPENAI001

BearerTokenPolicy tokenPolicy = new(
    new DefaultAzureCredential(),
    "https://cognitiveservices.azure.com/.default");

ChatClient client = new(
    model: "gpt-4.1",
    authenticationPolicy: tokenPolicy,
    options: new OpenAIClientOptions()
    {
        Endpoint = new Uri("https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1")
    }
);

ChatCompletionOptions options = new()
{
    ResponseFormat = ChatResponseFormat.CreateJsonSchemaFormat(
        jsonSchemaFormatName: "math_reasoning",
        jsonSchema: BinaryData.FromBytes("""
            {
                "type": "object",
                "properties": {
                    "steps": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "explanation": { "type": "string" },
                                "output": { "type": "string" }
                            },
                            "required": ["explanation", "output"],
                            "additionalProperties": false
                        }
                    },
                    "final_answer": { "type": "string" }
                },
                "required": ["steps", "final_answer"],
                "additionalProperties": false
            }
            """u8.ToArray()),
        jsonSchemaIsStrict: true)
};

// Create a list of ChatMessage objects
ChatCompletion completion = client.CompleteChat(
    [
        new UserChatMessage("How can I solve 8x + 7 = -23?")
    ],
    options);

using JsonDocument structuredJson = JsonDocument.Parse(completion.Content[0].Text);

Console.WriteLine($"Final answer: {structuredJson.RootElement.GetProperty("final_answer")}");
Console.WriteLine("Reasoning steps:");

foreach (JsonElement stepElement in structuredJson.RootElement.GetProperty("steps").EnumerateArray())
{
    Console.WriteLine($"  - Explanation: {stepElement.GetProperty("explanation")}");
    Console.WriteLine($"    Output: {stepElement.GetProperty("output")}");
}
```

# [API Key](#tab/dotnet-keys)

```csharp

using OpenAI;
using OpenAI.Chat;
using System.ClientModel;
using System.Text.Json;

string keyFromEnvironment = Environment.GetEnvironmentVariable("AZURE_OPENAI_API_KEY");

ChatClient client = new(
    model: "gpt-4o-mini",
    credential: new ApiKeyCredential(keyFromEnvironment),
    options: new OpenAIClientOptions() { 
        Endpoint = new Uri("https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1")
    }
);

ChatCompletionOptions options = new()
{
    ResponseFormat = ChatResponseFormat.CreateJsonSchemaFormat(
        jsonSchemaFormatName: "math_reasoning",
        jsonSchema: BinaryData.FromBytes("""
            {
                "type": "object",
                "properties": {
                    "steps": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "explanation": { "type": "string" },
                                "output": { "type": "string" }
                            },
                            "required": ["explanation", "output"],
                            "additionalProperties": false
                        }
                    },
                    "final_answer": { "type": "string" }
                },
                "required": ["steps", "final_answer"],
                "additionalProperties": false
            }
            """u8.ToArray()),
        jsonSchemaIsStrict: true)
};

// Create a list of ChatMessage objects
ChatCompletion completion = client.CompleteChat(
    [
        new UserChatMessage("How can I solve 8x + 7 = -23?")
    ],
    options);

using JsonDocument structuredJson = JsonDocument.Parse(completion.Content[0].Text);

Console.WriteLine($"Final answer: {structuredJson.RootElement.GetProperty("final_answer")}");
Console.WriteLine("Reasoning steps:");

foreach (JsonElement stepElement in structuredJson.RootElement.GetProperty("steps").EnumerateArray())
{
    Console.WriteLine($"  - Explanation: {stepElement.GetProperty("explanation")}");
    Console.WriteLine($"    Output: {stepElement.GetProperty("output")}");
}

```

---
