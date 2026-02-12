---
ms.topic: include
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.date: 3/11/2025
ms.reviewer: alexwolf
ms.author: pafarley
author: PatrickFarley
recommendations: false
---

## Prerequisites

- An Azure subscription. You can [create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- An Azure OpenAI resource with a text to speech model (such as `tts`) deployed in a [supported region](../../foundry-models/concepts/models-sold-directly-by-azure.md?tabs=standard-audio). For more information, see [Create a resource and deploy a model with Azure OpenAI](../how-to/create-resource.md).
- [The .NET 8.0 SDK](https://dotnet.microsoft.com/en-us/download)

### Microsoft Entra ID prerequisites

For the recommended keyless authentication with Microsoft Entra ID, you need to:
- Install the [Azure CLI](/cli/azure/install-azure-cli) used for keyless authentication with Microsoft Entra ID.
- Assign the `Cognitive Services User` role to your user account. You can assign roles in the Azure portal under **Access control (IAM)** > **Add role assignment**.

## Set up

1. Create a new folder `to-speech-quickstart` and go to the quickstart folder with the following command:

    ```shell
    mkdir to-speech-quickstart && cd to-speech-quickstart
    ```

1. Create a new console application with the following command:

    ```shell
    dotnet new console
    ```

3. Install the [OpenAI .NET client library](https://www.nuget.org/packages/Azure.AI.OpenAI/) with the [dotnet add package](/dotnet/core/tools/dotnet-add-package) command:

    ```console
    dotnet add package Azure.AI.OpenAI
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

> [!NOTE]
> You can get sample audio files, such as *wikipediaOcelot.wav*, from the [Azure Speech in Foundry Tools SDK repository at GitHub](https://github.com/Azure-Samples/cognitive-services-speech-sdk/tree/master/sampledata/audiofiles).

To run the quickstart, follow these steps:

1. Replace the contents of `Program.cs` with the following code and update the placeholder values with your own.
    
    ```csharp
    using Azure;
    using Azure.AI.OpenAI;
    using Azure.Identity; // Required for Passwordless auth
    
    var endpoint = new Uri(
        Environment.GetEnvironmentVariable("YOUR_OPENAI_ENDPOINT") ?? throw new ArgumentNullException());
    var credentials = new DefaultAzureCredential();

    // Use this line for key auth
    // var credentials = new AzureKeyCredential(
    //    Environment.GetEnvironmentVariable("YOUR_OPENAI_KEY") ?? throw new ArgumentNullException());

    var deploymentName = "tts"; // Default deployment name, update with your own if necessary
    var speechFilePath = "YOUR_AUDIO_FILE_PATH";
    
    AzureOpenAIClient openAIClient = new AzureOpenAIClient(endpoint, credentials);
    AudioClient audioClient = openAIClient.GetAudioClient(deploymentName);
    
    var result = await audioClient.GenerateSpeechAsync(
                    "the quick brown chicken jumped over the lazy dogs");
    
    Console.WriteLine("Streaming response to ${speechFilePath}");
    await File.WriteAllBytesAsync(speechFilePath, result.Value.ToArray());
    Console.WriteLine("Finished streaming");
    ```

1. Run the application using the `dotnet run` command or the run button at the top of Visual Studio:

    ```dotnetcli
    dotnet run
    ```

## Output

The application will generate an audio file at the location you specified for the `speechFilePath` variable. Play the file on your device to hear the generated audio.
