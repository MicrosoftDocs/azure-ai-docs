---
services: ai-services
author: mrbullwinkle
ms.author: mbullwin
ms.service: openai
ms.topic: include
ms.date: 3/19/2024
---

## Prerequisites

- An Azure subscription. You can [create one for free](https://azure.microsoft.com/free/cognitive-services?azure-portal=true).
- An Azure OpenAI resource with a Whisper model deployed in a [supported region](../concepts/models.md#whisper-models). For more information, see [Create a resource and deploy a model with Azure OpenAI](../how-to/create-resource.md).
- [The .NET 8.0 SDK](https://dotnet.microsoft.com/en-us/download)

## Set up

### Retrieve key and endpoint

To successfully make a call against Azure OpenAI, you need an *endpoint* and a *key*.

|Variable name | Value |
|--------------------------|-------------|
| `AZURE_OPENAI_ENDPOINT`               | This value can be found in the **Keys & Endpoint** section when examining your resource from the Azure portal. Alternatively, you can find the value in the **Azure OpenAI Studio** > **Playground** > **Code View**. An example endpoint is: `https://aoai-docs.openai.azure.com/`.|
| `AZURE_OPENAI_API_KEY` | This value can be found in the **Keys & Endpoint** section when examining your resource from the Azure portal. You can use either `KEY1` or `KEY2`.|

Go to your resource in the Azure portal. The **Endpoint and Keys** can be found in the **Resource Management** section. Copy your endpoint and access key as you'll need both for authenticating your API calls. You can use either `KEY1` or `KEY2`. Always having two keys allows you to securely rotate and regenerate keys without causing a service disruption.

:::image type="content" source="../media/quickstarts/endpoint.png" alt-text="Screenshot of the overview UI for an Azure OpenAI resource in the Azure portal with the endpoint & access keys location circled in red." lightbox="../media/quickstarts/endpoint.png":::

## Create the .NET app

1. Create a .NET app using the `dotnet new` command:

    ```dotnetcli
    dotnet new console -n OpenAIWhisper
    ```

1. Change into the directory of the new app:

    ```dotnetcli
    cd OpenAIWhisper
    ```

1. Install the [`Azure.OpenAI`](https://www.nuget.org/packages/Azure.AI.OpenAI/) client library:

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

    > [!NOTE]
    > You can get sample audio files, such as *wikipediaOcelot.wav*, from the [Azure AI Speech SDK repository at GitHub](https://github.com/Azure-Samples/cognitive-services-speech-sdk/tree/master/sampledata/audiofiles).
    
    ```csharp
    using Azure;
    using Azure.AI.OpenAI;
    using Azure.Identity; // Required for Passwordless auth
    
    var endpoint = new Uri("YOUR_OPENAI_ENDPOINT");
    var credentials = new AzureKeyCredential("YOUR_OPENAI_KEY");
    // var credentials = new DefaultAzureCredential(); // Use this line for Passwordless auth
    var deploymentName = "whisper"; // Default deployment name, update with your own if necessary
    var audioFilePath = "YOUR_AUDIO_FILE_PATH";
    
    var openAIClient = new AzureOpenAIClient(endpoint, credentials);
    
    var audioClient = openAIClient.GetAudioClient(deploymentName);
    
    var result = await audioClient.TranscribeAudioAsync(audioFilePath);
    
    Console.WriteLine("Transcribed text:");
    foreach (var item in result.Value.Text)
    {
        Console.Write(item);
    }
    ```

    > [!IMPORTANT]
    > For production, store and access your credentials using a secure method, such as [Azure Key Vault](/azure/key-vault/general/overview). For more information about credential security, see [Azure AI services security](../../security-features.md).

1. Run the application using the `dotnet run` command or the run button at the top of Visual Studio:

    ```dotnetcli
    dotnet run
    ```

    If you are using the sample audio file, you should see the following text printed out in the console:

    ```text
    The ocelot, Lepardus paradalis, is a small wild cat native to the southwestern United States, 
    Mexico, and Central and South America. This medium-sized cat is characterized by solid 
    black spots and streaks on its coat, round ears...
    ```
    