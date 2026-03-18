---
manager: nitinme
author: alexeyo26
ms.author: alexeyo
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: include
ms.date: 3/20/2025
---

## Deploy a model for real-time audio

[!INCLUDE [Deploy model](realtime-deploy-model.md)]

### Microsoft Entra ID

Currently Microsoft Entra ID authentication isn't supported for .NET scenario. You need to use API Key authentication.

## Retrieve resource information

You need to retrieve the following information to authenticate your application with your Azure OpenAI resource:

|Variable name | Value |
|--------------------------|-------------|
| `AZURE_OPENAI_ENDPOINT`               | This value can be found in the **Keys and Endpoint** section when examining your resource from the Azure portal. |
| `AZURE_OPENAI_API_KEY` | This value can be found in the **Keys and Endpoint** section when examining your resource from the Azure portal. You can use either `KEY1` or `KEY2`.|
| `AZURE_OPENAI_DEPLOYMENT_NAME` | This value corresponds to the custom name you chose for your deployment when you deployed a model. This value can be found under **Resource Management** > **Model Deployments** in the Azure portal.|

Learn more about [finding API keys](/azure/ai-services/cognitive-services-environment-variables) and [setting environment variables](/azure/ai-services/cognitive-services-environment-variables).

[!INCLUDE [Azure key vault](~/reusable-content/ce-skilling/azure/includes/ai-services/security/azure-key-vault.md)]

## Set up Visual Studio project

1. Create new Visual Studio project. In Visual Studio interface select File -> New -> Project...
1. Select *Console App C#* project type.
1. Use `RealtimeAudioQuickstartCSharp` as *Project name*.
1. Select .NET Framework to use and finish creating the project.
1. In *Solution Explorer* window right-click project name (`RealtimeAudioQuickstartCSharp`) and select Add -> New Folder.
1. Rename the created folder to `Properties`.
1. Right-click `Properties` and select Add -> New Item...
1. Use `launchSettings.json` as new item file name.
1. Replace the contents of `launchSettings.json` file with the following code. Use actual parameters of your resource for environment variable values:

    ```json
    {
      "profiles": {
        "RealtimeAudioQuickstartCSharp": {
          "commandName": "Project",
          "environmentVariables": {
            "AZURE_OPENAI_ENDPOINT": "https://<your-endpoint-name>.openai.azure.com/",
            "AZURE_OPENAI_DEPLOYMENT_NAME": "gpt-realtime",
            "AZURE_OPENAI_API_KEY": "<your-resource-api-key>"
          }
        }
      }
    }
    ```
1. Right-click *Dependencies* and select Manage NuGet Packages...
1. Select *Browse* tab and search for `openai`.
1. Download OpenAI NuGet Package and add it to your solution. Make sure, that OpenAI library version is 2.9.1 or later.

## Send text, receive audio response

1. Replace the contents of `Program.cs` with this code:

    ```csharp
    #pragma warning disable OPENAI002
    #pragma warning disable SCME0001
    using System.ClientModel;
    using OpenAI.Realtime;
    
    static string GetRequiredEnvironmentVariable(string name)
    {
        string? value = Environment.GetEnvironmentVariable(name);
        return !string.IsNullOrWhiteSpace(value)
            ? value
            : throw new InvalidOperationException($"Environment variable '{name}' is required.");
    }
    
    static Uri BuildRealtimeEndpointUri(string endpoint)
    {
        string normalized = endpoint.TrimEnd('/');
        if (!normalized.EndsWith("/openai/v1", StringComparison.OrdinalIgnoreCase))
        {
            normalized = $"{normalized}/openai/v1";
        }
    
        return new Uri(normalized, UriKind.Absolute);
    }
    
    string endpoint = GetRequiredEnvironmentVariable("AZURE_OPENAI_ENDPOINT");
    string deploymentName = GetRequiredEnvironmentVariable("AZURE_OPENAI_DEPLOYMENT_NAME");
    string apiKey = GetRequiredEnvironmentVariable("AZURE_OPENAI_API_KEY");
    
    RealtimeClient client = new(new ApiKeyCredential(apiKey), new RealtimeClientOptions
    {
        Endpoint = BuildRealtimeEndpointUri(endpoint),
    });
    
    using RealtimeSessionClient sessionClient = await client.StartConversationSessionAsync(model: deploymentName);
    
    RealtimeConversationSessionOptions sessionOptions = new()
    {
        Instructions = "You are a helpful assistant. You respond by voice and text.",
        AudioOptions = new()
        {
            InputAudioOptions = new()
            {
                AudioTranscriptionOptions = new()
                {
                    Model = "whisper-1",
                },
                TurnDetection = new RealtimeServerVadTurnDetection(),
            },
            OutputAudioOptions = new()
            {
                Voice = RealtimeVoice.Alloy,
            },
        },
    };
    
    await sessionClient.ConfigureConversationSessionAsync(sessionOptions);
    
    while (true)
    {
        Console.Write("Enter a message: ");
        string? userInput = Console.ReadLine();
    
        if (string.Equals(userInput, "q", StringComparison.OrdinalIgnoreCase))
        {
            Console.WriteLine("Stopping the conversation.");
            break;
        }
    
        if (string.IsNullOrWhiteSpace(userInput))
        {
            continue;
        }
    
        await sessionClient.AddItemAsync(RealtimeItem.CreateUserMessageItem(userInput));
        await sessionClient.StartResponseAsync();
    
        bool responseDone = false;
    
        await foreach (RealtimeServerUpdate update in sessionClient.ReceiveUpdatesAsync())
        {
            switch (update)
            {
                case RealtimeServerUpdateSessionCreated sessionCreatedUpdate:
                    Console.WriteLine($"Session ID: {sessionCreatedUpdate.Session.Patch.GetString("$.id"u8)}");
                    break;
    
                case RealtimeServerUpdateResponseOutputTextDelta textDeltaUpdate:
                    Console.Write(textDeltaUpdate.Delta);
                    break;
    
                case RealtimeServerUpdateResponseOutputAudioDelta audioDeltaUpdate:
                    Console.WriteLine($"Received {audioDeltaUpdate.Delta.Length} bytes of audio data.");
                    break;
    
                case RealtimeServerUpdateResponseOutputAudioTranscriptDelta transcriptDeltaUpdate:
                    Console.WriteLine($"Received text delta: {transcriptDeltaUpdate.Delta}");
                    break;
    
                case RealtimeServerUpdateResponseOutputTextDone:
                    Console.WriteLine();
                    break;
    
                case RealtimeServerUpdateError errorUpdate:
                    Console.WriteLine("Received an error event.");
                    Console.WriteLine($"Error code: {errorUpdate.Error.Code}");
                    Console.WriteLine($"Error Event ID: {errorUpdate.Error.EventId}");
                    Console.WriteLine($"Error message: {errorUpdate.Error.Message}");
                    responseDone = true;
                    break;
    
                case RealtimeServerUpdateResponseDone:
                    responseDone = true;
                    break;
            }
    
            if (responseDone)
            {
                break;
            }
        }
    }
    
    Console.WriteLine("Conversation ended.");
    #pragma warning restore OPENAI002
    #pragma warning restore SCME0001
    ```
1. Build the solution
1. To run the built `RealtimeAudioQuickstartCSharp.exe` you need to create the following environment variables with the values, corresponding to your resource:
    - `AZURE_OPENAI_ENDPOINT`
    - `AZURE_OPENAI_DEPLOYMENT_NAME`
    - `AZURE_OPENAI_API_KEY`
1. Alternatively if you built your solution in *Debug* configuration you might either use *Start Debugging* command in Visual Studio user interface (F5 key) or`dotnet run` command. In both cases the system uses configuration parameters defined in `launchSettings.json` file. To use `dotnet run` command:
    - Open Windows command prompt, go the folder containing `RealtimeAudioQuickstartCSharp.csproj` file and execute `dotnet run` command. 
1. When prompted for user input, type a message and hit enter to send it to the model. Enter "q" to quit the conversation. Wait a few moments to get the response.

## Output

The client program gets a response from the model and prints the transcript and audio data received.

The output looks similar to the following:
    
```console
Enter a message: How are you?
Session ID: sess_DKexmpK2z10zLGGEC2eGV
Received text delta: I'm
Received text delta:  doing
Received text delta:  well
Received text delta: ,
Received 4800 bytes of audio data.
Received 7200 bytes of audio data.
Received 12000 bytes of audio data.
Received text delta:  thank
Received text delta:  you
Received text delta:  for
Received text delta:  asking
Received text delta: !
Received 12000 bytes of audio data.
Received 12000 bytes of audio data.
Received text delta:  How
Received text delta:  about
Received 12000 bytes of audio data.
Received 12000 bytes of audio data.
Received 12000 bytes of audio data.
Received text delta:  you
Received text delta: ?
Received text delta:  How
Received text delta: 's
Received text delta:  your
Received text delta:  day
Received text delta:  going
Received text delta: ?
Received 12000 bytes of audio data.
Received 12000 bytes of audio data.
Received 12000 bytes of audio data.
Received 12000 bytes of audio data.
Received 12000 bytes of audio data.
Received 12000 bytes of audio data.
Received 12000 bytes of audio data.
Received 12000 bytes of audio data.
Received 28800 bytes of audio data.
Enter a message: q
Stopping the conversation.
Conversation ended.
```
