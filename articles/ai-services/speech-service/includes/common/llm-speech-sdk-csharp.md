---
manager: nitinme
author: PatrickFarley
ms.author: pafarley
ms.service: azure-ai-speech
ms.topic: include
ms.date: 03/16/2026
ai-usage: ai-assisted
---

[Reference documentation](/dotnet/api/overview/azure/ai.speech.transcription-readme) | [Package (NuGet)](https://www.nuget.org/packages/Azure.AI.Speech.Transcription/1.0.0-beta.1) | [GitHub samples](https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/transcription/Azure.AI.Speech.Transcription/samples)

## Prerequisites

- An Azure subscription. [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- [.NET 8.0 SDK](https://dotnet.microsoft.com/download) or later.
- A [Microsoft Foundry resource](/azure/ai-services/multi-service-resource) created in one of the supported regions. For more information about region availability, see [Region support](/azure/ai-services/speech-service/regions?tabs=stt).
- A sample `.wav` audio file to transcribe.

### Microsoft Entra ID prerequisites

For the recommended keyless authentication with Microsoft Entra ID, you need to:
- Install the [Azure CLI](/cli/azure/install-azure-cli) used for keyless authentication with Microsoft Entra ID.
- Sign in with the Azure CLI by running `az login`.
- Assign the `Cognitive Services User` role to your user account. You can assign roles in the Azure portal under **Access control (IAM)** > **Add role assignment**.

## Set up the project

1. Create a new console application with the .NET CLI:

    ```dotnetcli
    dotnet new console -n llm-speech-quickstart
    cd llm-speech-quickstart
    ```

1. Install the required packages:

    ```dotnetcli
    dotnet add package Azure.AI.Speech.Transcription --prerelease
    dotnet add package Azure.Identity
    ```

## Retrieve resource information

You need to retrieve your resource endpoint for authentication.

1. Sign in to [Foundry portal](https://ai.azure.com).
1. Select **Management center** from the left menu. Under **Connected resources**, select your Speech or multi-service resource.
1. Select **Keys and Endpoint**.
1. Copy the **Endpoint** value and set it as an environment variable:

    ```powershell
    $env:AZURE_SPEECH_ENDPOINT="<your-speech-endpoint>"
    ```

## Transcribe audio with LLM speech

LLM speech uses the `EnhancedModeProperties` class to enable large-language-model-enhanced transcription. Enhanced mode is automatically enabled when you create an `EnhancedModeProperties` instance. The model automatically detects the language in your audio.

Replace the contents of `Program.cs` with the following code:

```csharp
using System;
using System.ClientModel;
using System.Linq;
using System.Threading.Tasks;
using Azure.AI.Speech.Transcription;
using Azure.Identity;

Uri endpoint = new Uri(Environment.GetEnvironmentVariable("AZURE_SPEECH_ENDPOINT")
    ?? throw new InvalidOperationException("Set the AZURE_SPEECH_ENDPOINT environment variable."));

// Use DefaultAzureCredential for keyless authentication (recommended).
// To use an API key instead, replace with:
// ApiKeyCredential credential = new ApiKeyCredential("<your-api-key>");
var credential = new DefaultAzureCredential();
TranscriptionClient client = new TranscriptionClient(endpoint, credential);

string audioFilePath = "<path-to-your-audio-file.wav>";
using FileStream audioStream = File.OpenRead(audioFilePath);

// Create enhanced mode properties for LLM speech transcription
TranscriptionOptions options = new TranscriptionOptions(audioStream)
{
    EnhancedMode = new EnhancedModeProperties
    {
        Task = "transcribe"
    }
};

ClientResult<TranscriptionResult> response = await client.TranscribeAsync(options);

// Print combined transcription
foreach (var combinedPhrase in response.Value.CombinedPhrases)
{
    Console.WriteLine($"Transcription: {combinedPhrase.Text}");
}

// Print detailed phrase information
foreach (var channel in response.Value.PhrasesByChannel)
{
    Console.WriteLine("\nDetailed phrases:");
    foreach (var phrase in channel.Phrases)
    {
        Console.WriteLine($"  [{phrase.Offset}] ({phrase.Locale}): {phrase.Text}");
    }
}
```

Replace `<path-to-your-audio-file.wav>` with the path to your audio file. The service supports WAV, MP3, FLAC, OGG, and other common audio formats.

Run the application:

```dotnetcli
dotnet run
```

Reference: [`TranscriptionClient`](/dotnet/api/azure.ai.speech.transcription.transcriptionclient), [`EnhancedModeProperties`](/dotnet/api/azure.ai.speech.transcription.enhancedmodeproperties)

## Translate audio with LLM speech

You can also use LLM speech to translate audio into a target language. Set the `Task` to `translate` and specify the `TargetLanguage`:

```csharp
using System;
using System.ClientModel;
using System.Linq;
using System.Threading.Tasks;
using Azure.AI.Speech.Transcription;
using Azure.Identity;

Uri endpoint = new Uri(Environment.GetEnvironmentVariable("AZURE_SPEECH_ENDPOINT")
    ?? throw new InvalidOperationException("Set the AZURE_SPEECH_ENDPOINT environment variable."));

var credential = new DefaultAzureCredential();
TranscriptionClient client = new TranscriptionClient(endpoint, credential);

string audioFilePath = "<path-to-your-audio-file.wav>";
using FileStream audioStream = File.OpenRead(audioFilePath);

// Create enhanced mode properties for LLM speech translation
TranscriptionOptions options = new TranscriptionOptions(audioStream)
{
    EnhancedMode = new EnhancedModeProperties
    {
        Task = "translate",
        TargetLanguage = "de"
    }
};

ClientResult<TranscriptionResult> response = await client.TranscribeAsync(options);

// Print translation result
foreach (var combinedPhrase in response.Value.CombinedPhrases)
{
    Console.WriteLine($"Translation: {combinedPhrase.Text}");
}
```

Replace `<path-to-your-audio-file.wav>` with the path to your audio file.

Reference: [`EnhancedModeProperties`](/dotnet/api/azure.ai.speech.transcription.enhancedmodeproperties)

## Use prompt-tuning

You can provide an optional prompt to guide the output style for transcription or translation tasks:

```csharp
TranscriptionOptions options = new TranscriptionOptions(audioStream)
{
    EnhancedMode = new EnhancedModeProperties
    {
        Task = "transcribe",
        Prompt = { "Output must be in lexical format." }
    }
};

ClientResult<TranscriptionResult> response = await client.TranscribeAsync(options);

foreach (var combinedPhrase in response.Value.CombinedPhrases)
{
    Console.WriteLine($"Transcription: {combinedPhrase.Text}");
}
```

### Best practices for prompts

- Prompts are subject to a maximum length of 4,096 characters.
- Prompts should preferably be written in English.
- Use `Output must be in lexical format.` to enforce lexical formatting instead of the default display format.
- Use `Pay attention to *phrase1*, *phrase2*, …` to improve recognition of specific phrases or acronyms.

Reference: [`EnhancedModeProperties`](/dotnet/api/azure.ai.speech.transcription.enhancedmodeproperties)

## Clean up resources

When you finish the quickstart, delete the project folder:

```powershell
Remove-Item -Recurse -Force llm-speech-quickstart
```
