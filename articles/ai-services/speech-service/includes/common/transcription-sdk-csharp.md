---
manager: nitinme
author: PatrickFarley
ms.author: pafarley
ms.service: azure-ai-speech
ms.topic: include
ms.date: 03/11/2026
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
- Assign the `Cognitive Services User` role to your user account. You can assign roles in the Azure portal under **Access control (IAM)** > **Add role assignment**.

## Set up the project

1. Create a new console application with the .NET CLI:

    ```dotnetcli
    dotnet new console -n transcription-quickstart
    cd transcription-quickstart
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

## Transcribe audio

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

string audioFilePath = "path/to/audio.wav";
using FileStream audioStream = File.OpenRead(audioFilePath);

TranscriptionOptions options = new TranscriptionOptions(audioStream);
ClientResult<TranscriptionResult> response = await client.TranscribeAsync(options);

var channelPhrases = response.Value.PhrasesByChannel.First();
Console.WriteLine(channelPhrases.Text);
```

Run the application:

```dotnetcli
dotnet run
```

The transcribed text from your audio file prints to the console.

## Access word-level details

To access timestamps, confidence scores, and individual words, iterate over phrases:

```csharp
var channelPhrases = response.Value.PhrasesByChannel.First();

foreach (TranscribedPhrase phrase in channelPhrases.Phrases)
{
    Console.WriteLine($"\nPhrase: {phrase.Text}");
    Console.WriteLine($"  Offset: {phrase.Offset} | Duration: {phrase.Duration}");
    Console.WriteLine($"  Confidence: {phrase.Confidence:F2}");

    foreach (TranscribedWord word in phrase.Words)
    {
        Console.WriteLine(
            $"    Word: '{word.Text}' | " +
            $"Confidence: {word.Confidence:F2} | " +
            $"Offset: {word.Offset}");
    }
}
```

Reference: [`TranscribedPhrase`](/dotnet/api/azure.ai.speech.transcription.transcribedphrase), [`TranscribedWord`](/dotnet/api/azure.ai.speech.transcription.transcribedword)

## Identify speakers with diarization

Speaker diarization identifies who spoke when in multi-speaker audio:

```csharp
TranscriptionOptions options = new TranscriptionOptions(audioStream)
{
    DiarizationOptions = new TranscriptionDiarizationOptions
    {
        MaxSpeakers = 4
    }
};

ClientResult<TranscriptionResult> response = await client.TranscribeAsync(options);

var channelPhrases = response.Value.PhrasesByChannel.First();
foreach (TranscribedPhrase phrase in channelPhrases.Phrases)
{
    Console.WriteLine($"Speaker {phrase.Speaker}: {phrase.Text}");
}
```

Reference: [`TranscriptionDiarizationOptions`](/dotnet/api/azure.ai.speech.transcription.transcriptiondiarizationoptions)

