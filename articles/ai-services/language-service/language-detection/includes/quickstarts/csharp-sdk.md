---
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: include
ms.date: 11/18/2025
ms.author: lajanuar
ai-usage: ai-assisted
---
[Reference documentation](/dotnet/api/azure.ai.textanalytics?preserve-view=true&view=azure-dotnet-preview) | [More samples](https://github.com/Azure/azure-sdk-for-net/tree/master/sdk/textanalytics/Azure.AI.TextAnalytics/samples) | [Package (NuGet)](https://www.nuget.org/packages/Azure.AI.TextAnalytics/5.2.0) | [Library source code](https://github.com/Azure/azure-sdk-for-net/tree/master/sdk/textanalytics/Azure.AI.TextAnalytics)

Use this quickstart to create a language detection application with the client library for .NET. In the following example, you create a C# application that can identify the language a text sample was written in.


## Prerequisites

* Azure subscription - [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn)
* The [Visual Studio IDE](https://visualstudio.microsoft.com/vs/)


## Setting up

[!INCLUDE [Create an Azure resource](../../../includes/create-resource.md)]



[!INCLUDE [Get your key and endpoint](../../../includes/get-key-endpoint.md)]



[!INCLUDE [Create environment variables](../../../includes/environment-variables.md)]


### Create a new .NET Core application

Using the Visual Studio IDE, create a new .NET Core console app. This creates a "Hello World" project with a single C# source file: *program.cs*.

Install the client library by right-clicking the solution in the **Solution Explorer** and selecting **Manage NuGet Packages**. In the package manager that opens select **Browse** and search for `Azure.AI.TextAnalytics`. Select version `5.2.0`, and then **Install**. You can also use the [Package Manager Console](/nuget/consume-packages/install-use-packages-powershell#find-and-install-a-package).


## Code example

Copy the following code into your *program.cs* file. Then run the code.  

```csharp
using Azure;
using System;
using Azure.AI.TextAnalytics;

namespace LanguageDetectionExample
{
    class Program
    {
        // This example requires environment variables named "LANGUAGE_KEY" and "LANGUAGE_ENDPOINT".
        static void LanguageDetectionExample(TextAnalyticsClient client)
        {
            DetectedLanguage detectedLanguage = client.DetectLanguage("Ce document est rédigé en Français.");
            Console.WriteLine("Language:");
            Console.WriteLine($"\t{detectedLanguage.Name},\tISO-6391: {detectedLanguage.Iso6391Name}\n");
        }

        static void Main(string[] args)
        {
            string languageKey = Environment.GetEnvironmentVariable("LANGUAGE_KEY");
            string languageEndpoint = Environment.GetEnvironmentVariable("LANGUAGE_ENDPOINT");

            if (string.IsNullOrWhiteSpace(languageKey) || string.IsNullOrWhiteSpace(languageEndpoint))
            {
                Console.WriteLine("Set the LANGUAGE_KEY and LANGUAGE_ENDPOINT environment variables before running this sample.");
                return;
            }

            var endpoint = new Uri(languageEndpoint);
            var credentials = new AzureKeyCredential(languageKey);
            var client = new TextAnalyticsClient(endpoint, credentials);

            LanguageDetectionExample(client);

            Console.Write("Press any key to exit.");
            Console.ReadKey();
        }

    }
}

```



### Output

```console
Language:
    French, ISO-6391: fr
```
