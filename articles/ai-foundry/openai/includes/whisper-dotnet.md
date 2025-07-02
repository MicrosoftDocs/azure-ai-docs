---
services: ai-services
author: eric-urban
ms.author: eur
ms.service: azure-ai-openai
ms.topic: include
ms.date: 3/11/2025
---

## Prerequisites

- An Azure subscription. You can [create one for free](https://azure.microsoft.com/free/cognitive-services?azure-portal=true).
- An Azure OpenAI resource with a speech to text model deployed in a [supported region](../concepts/models.md?tabs=standard-audio#standard-deployment-regional-models-by-endpoint). For more information, see [Create a resource and deploy a model with Azure OpenAI](../how-to/create-resource.md).
- [The .NET 8.0 SDK](https://dotnet.microsoft.com/en-us/download)

### Microsoft Entra ID prerequisites

For the recommended keyless authentication with Microsoft Entra ID, you need to:
- Install the [Azure CLI](/cli/azure/install-azure-cli) used for keyless authentication with Microsoft Entra ID.
- Assign the `Cognitive Services User` role to your user account. You can assign roles in the Azure portal under **Access control (IAM)** > **Add role assignment**.

## Set up

1. Create a new folder `whisper-quickstart` and go to the quickstart folder with the following command:

    ```shell
    mkdir whisper-quickstart && cd whisper-quickstart
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
> You can get sample audio files, such as *wikipediaOcelot.wav*, from the [Azure AI Speech SDK repository at GitHub](https://github.com/Azure-Samples/cognitive-services-speech-sdk/tree/master/sampledata/audiofiles).

To run the quickstart, follow these steps:

1. Replace the contents of `Program.cs` with the following code and update the placeholder values with your own.
    
    ```csharp
    using Azure;
    using Azure.AI.OpenAI;
    using Azure.Identity; // Required for Passwordless auth
    
    
    string deploymentName = "whisper";
    
    string endpoint = Environment.GetEnvironmentVariable("AZURE_OPENAI_ENDPOINT") ?? "https://<your-resource-name>.openai.azure.com/";
    string key = Environment.GetEnvironmentVariable("AZURE_OPENAI_API_KEY") ?? "<your-key>";
    
    // Use the recommended keyless credential instead of the AzureKeyCredential credential.
    AzureOpenAIClient openAIClient = new AzureOpenAIClient(new Uri(endpoint), new DefaultAzureCredential()); 
    //AzureOpenAIClient openAIClient = new AzureOpenAIClient(new Uri(endpoint), new AzureKeyCredential(key));
    
    var audioFilePath = "<audio file path>"
    
    var audioClient = openAIClient.GetAudioClient(deploymentName);
    
    var result = await audioClient.TranscribeAudioAsync(audioFilePath);
    
    Console.WriteLine("Transcribed text:");
    foreach (var item in result.Value.Text)
    {
        Console.Write(item);
    }
    ```

1. Run the application using the `dotnet run` command or the run button at the top of Visual Studio:

    ```dotnetcli
    dotnet run
    ```

## Output

If you are using the sample audio file, you should see the following text printed out in the console:

```text
The ocelot, Lepardus paradalis, is a small wild cat native to the southwestern United States, 
Mexico, and Central and South America. This medium-sized cat is characterized by solid 
black spots and streaks on its coat, round ears...
```
