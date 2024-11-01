---
title: 'Quickstart: Use GPT-4 Turbo with Vision on your images and videos with the .NET SDK'
titleSuffix: Azure OpenAI
description: Get started using the Azure OpenAI .NET SDK to deploy and use the GPT-4 Turbo with Vision model.
services: cognitive-services
manager: nitinme
ms.service: azure-ai-openai
ms.topic: include
ms.custom: references_regions
ms.date: 01/22/2024
---

Use this article to get started using the Azure OpenAI .NET SDK to deploy and use the GPT-4 Turbo with Vision model. 

## Prerequisites

- An Azure subscription. You can [create one for free](https://azure.microsoft.com/free/cognitive-services?azure-portal=true).
- [The .NET 8.0 SDK](https://dotnet.microsoft.com/en-us/download)
- An Azure OpenAI Service resource with a GPT-4 Turbo with Vision model deployed. See [GPT-4 and GPT-4 Turbo Preview model availability](../concepts/models.md#gpt-4-and-gpt-4-turbo-model-availability) for available regions. For more information about resource creation, see the [resource deployment guide](/azure/ai-services/openai/how-to/create-resource).

## Set up

### Retrieve key and endpoint

To successfully make a call against Azure OpenAI, you need an **endpoint** and a **key**.

|Variable name | Value |
|--------------------------|-------------|
| `AZURE_OPENAI_ENDPOINT`               | The service endpoint can be found in the **Keys & Endpoint** section when examining your resource from the Azure portal. Alternatively, you can find the endpoint via the **Deployments** page in Azure AI Studio. An example endpoint is: `https://docs-test-001.openai.azure.com/`. |
| `AZURE_OPENAI_API_KEY` | This value can be found in the **Keys & Endpoint** section when examining your resource from the Azure portal. You can use either `KEY1` or `KEY2`.|

Go to your resource in the Azure portal. The **Endpoint and Keys** can be found in the **Resource Management** section. Copy your endpoint and access key as you need both for authenticating your API calls. You can use either `KEY1` or `KEY2`. Always having two keys allows you to securely rotate and regenerate keys without causing a service disruption.

:::image type="content" source="../media/quickstarts/endpoint.png" alt-text="Screenshot of the overview UI for an Azure OpenAI resource in the Azure portal with the endpoint & access keys location highlighted." lightbox="../media/quickstarts/endpoint.png":::


## Create the .NET app

1. Create a .NET app using the `dotnet new` command:

    ```dotnetcli
    dotnet new console -n OpenAISpeech
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
    using Azure.Identity;
    using OpenAI.Chat; // Required for Passwordless auth
    
    var endpoint = new Uri("YOUR_AZURE_OPENAI_ENDPOINT");
    var credentials = new AzureKeyCredential("YOUR_AZURE_OPENAI_KEY");
    // var credentials = new DefaultAzureCredential(); // Use this line for Passwordless auth
    var deploymentName = "gpt-4"; // Default name, update with your own if needed
    
    var openAIClient = new AzureOpenAIClient(endpoint, credentials);
    var chatClient = openAIClient.GetChatClient(deploymentName);
    
    var imageUri = "YOUR_IMAGE_URL";
    
    List<ChatMessage> messages = [
        new UserChatMessage(
            ChatMessageContentPart.CreateTextMessageContentPart("Please describe the following image:"),
            ChatMessageContentPart.CreateImageMessageContentPart(new Uri(imageUri), "image/png"))
    ];
    
    ChatCompletion chatCompletion = await chatClient.CompleteChatAsync(messages);
    
    Console.WriteLine($"[ASSISTANT]:");
    Console.WriteLine($"{chatCompletion.Content[0].Text}");
    ```

    > [!IMPORTANT]
    > For production, store and access your credentials using a secure method, such as [Azure Key Vault](/azure/key-vault/general/overview). For more information about credential security, see [Azure AI services security](../../security-features.md).

1. Run the application using the `dotnet run` command or the run button at the top of Visual Studio:

    ```dotnetcli
    dotnet run
    ```

  The app generates an audio file at the location you specified for the `speechFilePath` variable. Play the file on your device to hear the generated audio.

## Clean up resources

If you want to clean up and remove an Azure OpenAI resource, you can delete the resource or resource group. Deleting the resource group also deletes any other resources associated with it.

- [Azure portal](../../multi-service-resource.md?pivots=azportal#clean-up-resources)
- [Azure CLI](../../multi-service-resource.md?pivots=azcli#clean-up-resources)


