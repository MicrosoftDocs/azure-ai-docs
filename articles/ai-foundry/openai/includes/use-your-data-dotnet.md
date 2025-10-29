---
manager: nitinme
author: travisw
ms.author: travisw
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: include
ms.date: 3/11/2025
---

[!INCLUDE [Set up required variables](./use-your-data-common-variables.md)]

From the project directory, open the *Program.cs* file and replace its contents with the following code:

```csharp
using System;
using Azure.AI.OpenAI;
using System.ClientModel;
using Azure.AI.OpenAI.Chat;
using OpenAI.Chat;
using static System.Environment;

string azureOpenAIEndpoint = GetEnvironmentVariable("AZURE_OPENAI_ENDPOINT");
string azureOpenAIKey = GetEnvironmentVariable("AZURE_OPENAI_API_KEY");
string deploymentName = GetEnvironmentVariable("AZURE_OPENAI_DEPLOYMENT_NAME");
string searchEndpoint = GetEnvironmentVariable("AZURE_AI_SEARCH_ENDPOINT");
string searchKey = GetEnvironmentVariable("AZURE_AI_SEARCH_API_KEY");
string searchIndex = GetEnvironmentVariable("AZURE_AI_SEARCH_INDEX");

AzureOpenAIClient openAIClient = new(
			new Uri(azureOpenAIEndpoint),
			new ApiKeyCredential(azureOpenAIKey));
ChatClient chatClient = openAIClient.GetChatClient(deploymentName);

// Extension methods to use data sources with options are subject to SDK surface changes. Suppress the
// warning to acknowledge and this and use the subject-to-change AddDataSource method.
#pragma warning disable AOAI001

ChatCompletionOptions options = new();
options.AddDataSource(new AzureSearchChatDataSource()
{
	Endpoint = new Uri(searchEndpoint),
	IndexName = searchIndex,
	Authentication = DataSourceAuthentication.FromApiKey(searchKey),
});

ChatCompletion completion = chatClient.CompleteChat(
	[
		new UserChatMessage("What health plans are available?"),
			],
	options);

ChatMessageContext onYourDataContext = completion.GetMessageContext();

if (onYourDataContext?.Intent is not null)
{
	Console.WriteLine($"Intent: {onYourDataContext.Intent}");
}
foreach (ChatCitation citation in onYourDataContext?.Citations ?? [])
{
	Console.WriteLine($"Citation: {citation.Content}");
}
```

> [!IMPORTANT]
> For production, use a secure way of storing and accessing your credentials like [Azure Key Vault](/azure/key-vault/general/overview). For more information about credential security, see this [security](../../../ai-services/security-features.md) article.

```cmd
dotnet run Program.cs
```

## Output

```output
Contoso Electronics offers two health plans: Northwind Health Plus and Northwind Standard [doc1]. Northwind Health Plus is a comprehensive plan that provides coverage for medical, vision, and dental services, prescription drug coverage, mental health and substance abuse coverage, and coverage for preventive care services. It also offers coverage for emergency services, both in-network and out-of-network. On the other hand, Northwind Standard is a basic plan that provides coverage for medical, vision, and dental services, prescription drug coverage, and coverage for preventive care services. However, it does not offer coverage for emergency services, mental health and substance abuse coverage, or out-of-network services [doc1].

Intent: ["What are the available health plans?", "List of health plans available", "Health insurance options", "Types of health plans offered"]

Citation:
Contoso Electronics plan and benefit packages

Thank you for your interest in the Contoso electronics plan and benefit packages. Use this document to

learn more about the various options available to you...// Omitted for brevity
```

This will wait until the model has generated its entire response before printing the results.