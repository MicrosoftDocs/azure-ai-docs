---
ms.topic: include
manager: nitinme
ms.service: azure-ai-openai
ms.topic: include
ms.date: 09/23/2024
ms.reviewer: v-baolianzou
ms.author: alexwolf
author: alexwolfmsft
recommendations: false
---

## Prerequisites

- An Azure subscription. You can [create one for free](https://azure.microsoft.com/free/cognitive-services?azure-portal=true).
- An Azure OpenAI resource with a Whisper model deployed in a [supported region](../concepts/models.md#whisper-models). For more information, see [Create a resource and deploy a model with Azure OpenAI](../how-to/create-resource.md).
- [The .NET 8.0 SDK](https://dotnet.microsoft.com/en-us/download)

## Set up

### Retrieve key and endpoint

To successfully make a call against Azure OpenAI, you need an **endpoint** and a **key**.

|Variable name | Value |
|--------------------------|-------------|
| `AZURE_OPENAI_ENDPOINT`               | This value can be found in the **Keys & Endpoint** section when examining your resource from the Azure portal. Alternatively, you can find the value in the **Azure OpenAI Studio** > **Playground** > **Code View**. An example endpoint is: `https://aoai-docs.openai.azure.com/`.|
| `AZURE_OPENAI_API_KEY` | This value can be found in the **Keys & Endpoint** section when examining your resource from the Azure portal. You can use either `KEY1` or `KEY2`.|

Go to your resource in the Azure portal. The **Endpoint and Keys** can be found in the **Resource Management** section. Copy your endpoint and access key as you need both for authenticating your API calls. You can use either `KEY1` or `KEY2`. Always having two keys allows you to securely rotate and regenerate keys without causing a service disruption.

:::image type="content" source="../media/quickstarts/endpoint.png" alt-text="Screenshot of the overview UI for an Azure OpenAI resource in the Azure portal with the endpoint & access keys location highlighted." lightbox="../media/quickstarts/endpoint.png":::


## Create the .NET app

1. Create a .NET app using the `dotnet new` command:

    ```dotnetcli
    dotnet new console -n TextToSpeech
    ```

1. Change into the directory of the new app:

    ```dotnetcli
    cd OpenAISpeech
    ```

## Install the client library

Install the [`Azure.OpenAI`](https://www.nuget.org/packages/Azure.AI.OpenAI/) client library:

```dotnetcli
dotnet add package Azure.AI.OpenAI
```

## Passwordless authentication is recommended

Passwordless authentication is more secure than key-based alternatives and is the recommended approach for connecting to Azure services. If you choose to use Passwordless authentication, you'll need to complete the following:

1. Add the [`Azure.Identity`](https://www.nuget.org/packages/Azure.Identity) package.

    ```dotnetcli
    dotnet add package Azure.Identity
    ```

1. Assign the `Cognitive Services User` role to your user account. This can be done in the Azure portal on your OpenAI resource under **Access control (IAM)** > **Add role assignment**.
1. Sign-in to Azure using Visual Studio or the Azure CLI via `az login`.

## Update the app code

1. Replace the contents of `program.cs` with the following code and update the placeholder values with your own.

    ```csharp
    using Azure;
    using Azure.AI.OpenAI;
    using Azure.Identity; // Required for Passwordless auth
    
    var endpoint = new Uri("YOUR_OPENAI_ENDPOINT");
    var credentials = new AzureKeyCredential("YOUR_OPENAI_KEY");
    // var credentials = new DefaultAzureCredential(); // Use this line for Passwordless auth
    var deploymentName = "tts"; // Default deployment name, update with your own if necessary
    var speechFilePath = "YOUR_AUDIO_FILE_PATH";
    
    var openAIClient = new AzureOpenAIClient(endpoint, credentials);
    var audioClient = openAIClient.GetAudioClient(deploymentName);
    
    var result = await audioClient.GenerateSpeechAsync(
                    "the quick brown chicken jumped over the lazy dogs");
    
    Console.WriteLine("Streaming response to ${speechFilePath}");
    await File.WriteAllBytesAsync(speechFilePath, result.Value.ToArray());
    Console.WriteLine("Finished streaming");
    ```

    > [!IMPORTANT]
    > For production, store and access your credentials using a secure method, such as [Azure Key Vault](/azure/key-vault/general/overview). For more information about credential security, see [Azure AI services security](../../security-features.md).

1. Run the application using the `dotnet run` command or the run button at the top of Visual Studio:

    ```dotnetcli
    dotnet run
    ```

  The app generates an audio file at the location you specified for the `speechFilePath` variable. Play the file on your device to hear the generated audio.
