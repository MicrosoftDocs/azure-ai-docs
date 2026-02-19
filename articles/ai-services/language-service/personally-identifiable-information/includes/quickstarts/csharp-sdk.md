---
author: laujan
ms.author: lajanuar
manager: nitinme
ms.date: 01/30/2026
ms.service: azure-ai-language
ms.topic: include
ms.custom:
  - language-service-pii
  - ignite-2024
  - build-2025
ai-usage: ai-assisted
---
<!-- markdownlint-disable MD041 -->
[Reference documentation](/dotnet/api/azure.ai.textanalytics?view=azure-dotnet&preserve-view=true) | [More samples](https://github.com/Azure/azure-sdk-for-net/tree/master/sdk/textanalytics/Azure.AI.TextAnalytics/samples) | [Package (NuGet)](https://www.nuget.org/packages/Azure.AI.TextAnalytics/5.2.0) | [Library source code](https://github.com/Azure/azure-sdk-for-net/tree/master/sdk/textanalytics/Azure.AI.TextAnalytics)

Use this quickstart to create a Personally Identifiable Information (PII) detection application with the client library for .NET. In the following example, you create a C# application that can identify [recognized sensitive information](../../concepts/entity-categories.md) in text.

[!INCLUDE [Tip: use Microsoft Foundry](../use-microsoft-foundry.md)]

## Prerequisites

* Azure subscription - [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn)
* Once you have your Azure subscription, [create a Foundry resource](../../../../../ai-services/multi-service-resource.md?pivots=azportal).
* The [Visual Studio IDE](https://visualstudio.microsoft.com/vs/)

## Setting up

[!INCLUDE [Create an Azure resource](../../../includes/create-resource.md)]

[!INCLUDE [Get your key and endpoint](../../../includes/get-key-endpoint.md)]

[!INCLUDE [Create environment variables](../../../includes/environment-variables.md)]

### Create a new .NET Core application

Using the Visual Studio IDE, create a new .NET Core console app. This step creates a "Hello World" project with a single C# source file: *program.cs*.

Install the client library by right-clicking the solution in the **Solution Explorer** and selecting **Manage NuGet Packages**. In the package manager that opens select **Browse** and search for `Azure.AI.TextAnalytics`. Select version `5.2.0`, and then **Install**. You can also use the [Package Manager Console](/nuget/consume-packages/install-use-packages-powershell#find-and-install-a-package).

## Code example

Copy the following code into your *program.cs* file and run the code.

```csharp
using Azure;
using System;
using Azure.AI.TextAnalytics;

namespace Example
{
    class Program
    {
        // This example requires environment variables named "LANGUAGE_KEY" and "LANGUAGE_ENDPOINT"
        static string languageKey = Environment.GetEnvironmentVariable("LANGUAGE_KEY");
        static string languageEndpoint = Environment.GetEnvironmentVariable("LANGUAGE_ENDPOINT");

        // Example method for detecting sensitive information (PII) from text 
        static void RecognizePIIExample(TextAnalyticsClient client)
        {
            string document = "Call our office at 312-555-1234, or send an email to support@contoso.com.";
        
            PiiEntityCollection entities = client.RecognizePiiEntities(document).Value;
        
            Console.WriteLine($"Redacted Text: {entities.RedactedText}");
            if (entities.Count > 0)
            {
                Console.WriteLine($"Recognized {entities.Count} PII entit{(entities.Count > 1 ? "ies" : "y")}:");
                foreach (PiiEntity entity in entities)
                {
                    Console.WriteLine($"Text: {entity.Text}, Category: {entity.Category}, SubCategory: {entity.SubCategory}, Confidence score: {entity.ConfidenceScore}");
                }
            }
            else
            {
                Console.WriteLine("No entities were found.");
            }
        }

        static void Main(string[] args)
        {
            if (string.IsNullOrWhiteSpace(languageKey) || string.IsNullOrWhiteSpace(languageEndpoint))
            {
                Console.WriteLine("Missing LANGUAGE_KEY or LANGUAGE_ENDPOINT environment variables.");
                return;
            }

            var endpoint = new Uri(languageEndpoint);
            var credentials = new AzureKeyCredential(languageKey);
            var client = new TextAnalyticsClient(endpoint, credentials);
            RecognizePIIExample(client);

            Console.Write("Press any key to exit.");
            Console.ReadKey();
        }

    }
}
```

## Output

```console
Redacted Text: Call our office at ************, or send an email to *******************.
Recognized 2 PII entities:
Text: 312-555-1234, Category: PhoneNumber, SubCategory: , Confidence score: 0.8
Text: support@contoso.com, Category: Email, SubCategory: , Confidence score: 0.8
```
