---
title: "Quickstart: Entity Linking client library for C#"
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: include
ms.date: 06/30/2025
ms.author: lajanuar
---

[Reference documentation](/dotnet/api/azure.ai.textanalytics?preserve-view=true&view=azure-dotnet) | [More samples](https://github.com/Azure/azure-sdk-for-net/tree/master/sdk/textanalytics/Azure.AI.TextAnalytics/samples) | [Package (NuGet)](https://www.nuget.org/packages/Azure.AI.TextAnalytics/5.2.0) | [Library source code](https://github.com/Azure/azure-sdk-for-net/tree/master/sdk/textanalytics/Azure.AI.TextAnalytics)

Use this quickstart to create an entity linking application with the client library for .NET. In the following example, you create a C# application that can identify and disambiguate entities found in text.

[!INCLUDE [Use Language Studio](../../../includes/use-language-studio.md)]

## Prerequisites

* Azure subscription - [Create one for free](https://azure.microsoft.com/free/cognitive-services)
* The [Visual Studio IDE](https://visualstudio.microsoft.com/vs/)


## Setting up

[!INCLUDE [Create an Azure resource](../../../includes/create-resource.md)]



[!INCLUDE [Get your key and endpoint](../../../includes/get-key-endpoint.md)]



[!INCLUDE [Create environment variables](../../../includes/environment-variables.md)]

### Create a new .NET Core application

Using the Visual Studio IDE, create a new .NET Core console app. This will create a "Hello World" project with a single C# source file: *program.cs*.

Install the client library by right-clicking on the solution in the **Solution Explorer** and selecting **Manage NuGet Packages**. In the package manager that opens select **Browse** and search for `Azure.AI.TextAnalytics`. Select version `5.2.0`, and then **Install**. You can also use the [Package Manager Console](/nuget/consume-packages/install-use-packages-powershell#find-and-install-a-package).



## Code example

Copy the following code into your *program.cs* file and run the code. 

```csharp
using Azure;
using System;
using System.Globalization;
using Azure.AI.TextAnalytics;

namespace EntityLinkingExample
{
    class Program
    {
        // This example requires environment variables named "LANGUAGE_KEY" and "LANGUAGE_ENDPOINT"
        static string languageKey = Environment.GetEnvironmentVariable("LANGUAGE_KEY");
        static string languageEndpoint = Environment.GetEnvironmentVariable("LANGUAGE_ENDPOINT");

        private static readonly AzureKeyCredential credentials = new AzureKeyCredential(languageKey);
        private static readonly Uri endpoint = new Uri(languageEndpoint);
        
        // Example method for recognizing entities and providing a link to an online data source.
        static void EntityLinkingExample(TextAnalyticsClient client)
        {
            var response = client.RecognizeLinkedEntities(
                "Microsoft was founded by Bill Gates and Paul Allen on April 4, 1975, " +
                "to develop and sell BASIC interpreters for the Altair 8800. " +
                "During his career at Microsoft, Gates held the positions of chairman, " +
                "chief executive officer, president and chief software architect, " +
                "while also being the largest individual shareholder until May 2014.");
            Console.WriteLine("Linked Entities:");
            foreach (var entity in response.Value)
            {
                Console.WriteLine($"\tName: {entity.Name},\tID: {entity.DataSourceEntityId},\tURL: {entity.Url}\tData Source: {entity.DataSource}");
                Console.WriteLine("\tMatches:");
                foreach (var match in entity.Matches)
                {
                    Console.WriteLine($"\t\tText: {match.Text}");
                    Console.WriteLine($"\t\tScore: {match.ConfidenceScore:F2}\n");
                }
            }
        }

        static void Main(string[] args)
        {
            var client = new TextAnalyticsClient(endpoint, credentials);
            EntityLinkingExample(client);

            Console.Write("Press any key to exit.");
            Console.ReadKey();
        }

    }
}

```



### Output

```console
Linked Entities:
    Name: Microsoft,        ID: Microsoft,  URL: https://en.wikipedia.org/wiki/Microsoft    Data Source: Wikipedia
    Matches:
            Text: Microsoft
            Score: 0.55

            Text: Microsoft
            Score: 0.55

    Name: Bill Gates,       ID: Bill Gates, URL: https://en.wikipedia.org/wiki/Bill_Gates   Data Source: Wikipedia
    Matches:
            Text: Bill Gates
            Score: 0.63

            Text: Gates
            Score: 0.63

    Name: Paul Allen,       ID: Paul Allen, URL: https://en.wikipedia.org/wiki/Paul_Allen   Data Source: Wikipedia
    Matches:
            Text: Paul Allen
            Score: 0.60

    Name: April 4,  ID: April 4,    URL: https://en.wikipedia.org/wiki/April_4      Data Source: Wikipedia
    Matches:
            Text: April 4
            Score: 0.32

    Name: BASIC,    ID: BASIC,      URL: https://en.wikipedia.org/wiki/BASIC        Data Source: Wikipedia
    Matches:
            Text: BASIC
            Score: 0.33

    Name: Altair 8800,      ID: Altair 8800,        URL: https://en.wikipedia.org/wiki/Altair_8800  Data Source: Wikipedia
    Matches:
            Text: Altair 8800
            Score: 0.88
```

[!INCLUDE [clean up resources](../../../includes/clean-up-resources.md)]



## Next steps

* [Entity linking language support](../../language-support.md)
* [How to call the entity linking API](../../how-to/call-api.md)  
* [Reference documentation](/dotnet/api/azure.ai.textanalytics?preserve-view=true&view=azure-dotnet)
* [Additional samples](https://github.com/Azure/azure-sdk-for-net/tree/master/sdk/textanalytics/Azure.AI.TextAnalytics/samples)
