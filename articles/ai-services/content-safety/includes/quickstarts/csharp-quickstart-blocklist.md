---
title: "Quickstart: Use a blocklist with C#"
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-content-safety
ms.custom:
ms.topic: include
ms.date: 02/22/2025
ms.author: pafarley
ai-usage: ai-assisted
---

[Reference documentation](/dotnet/api/overview/azure/ai.contentsafety-readme) | [Library source code](https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/contentsafety/Azure.AI.ContentSafety) | [Package (NuGet)](https://www.nuget.org/packages/Azure.AI.ContentSafety) | [Samples](https://github.com/Azure-Samples/AzureAIContentSafety/tree/main/dotnet/1.0.0)


## Prerequisites

* An Azure subscription - [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn) 
* The [Visual Studio IDE](https://visualstudio.microsoft.com/vs/) with workload .NET desktop development enabled. Or if you don't plan on using Visual Studio IDE, you need the current version of [.NET Core](https://dotnet.microsoft.com/download/dotnet-core).
* Once you have your Azure subscription, <a href="https://aka.ms/acs-create"  title="Create a Content Safety resource"  target="_blank">create a Content Safety resource </a> in the Azure portal to get your key and endpoint. Enter a unique name for your resource, select your subscription, and select a resource group, supported region (see [Region availability](/azure/ai-services/content-safety/overview#region-availability)), and supported pricing tier. Then select **Create**.
  * The resource takes a few minutes to deploy. After it finishes, Select **go to resource**. In the left pane, under **Resource Management**, select **Subscription Key and Endpoint**. The endpoint and either of the keys are used to call APIs.

## Set up application

Create a new C# application.

#### [Visual Studio IDE](#tab/visual-studio)

Open Visual Studio, and under **Get started** select **Create a new project**. Set the template filters to _C#/All Platforms/Console_. Select **Console App** (command-line application that can run on .NET on Windows, Linux and macOS) and choose **Next**. Update the project name to _ContentSafetyQuickstart_ and choose **Next**. Select **.NET 6.0** or above, and choose **Create** to create the project.

### Install the client SDK 

Once you've created a new project, install the client SDK by right-clicking on the project solution in the **Solution Explorer** and selecting **Manage NuGet Packages**. In the package manager that opens select **Browse**, and search for `Azure.AI.ContentSafety`. Select **Install**.

#### [CLI](#tab/cli)

In a console window (such as cmd, PowerShell, or Bash), use the `dotnet new` command to create a new console app with the name `content-safety-quickstart`. This command creates a simple "Hello World" C# project with a single source file: *Program.cs*.

```dotnet
dotnet new console -n content-safety-quickstart
```

Change your directory to the newly created app folder. You can build the application with:

```dotnet
dotnet build
```

The build output should contain no warnings or errors. 

```console
...
Build succeeded.
  0 Warning(s)
  0 Error(s)
...
```

### Install the client SDK

Within the application directory, install the Azure AI Content Safety client SDK for .NET with the following command:

```dotnet
dotnet add package Azure.AI.ContentSafety
```
    
---

[!INCLUDE [Create environment variables](../env-vars.md)]

## Create and use a blocklist

From the project directory, open the *Program.cs* file that was created previously. Paste in the following code. This code creates a new blocklist, adds items to it, and then analyzes a text string against the blocklist.

```csharp
using System;
using Azure.AI.ContentSafety;
using Azure;
using Azure.Core;

class ContentSafetyBlocklist
{
    public static void UseBlocklist()
    {
        
        string endpoint = Environment.GetEnvironmentVariable("CONTENT_SAFETY_ENDPOINT");
        string key = Environment.GetEnvironmentVariable("CONTENT_SAFETY_KEY");
        Console.WriteLine("Endpoint: "+ endpoint);
        Console.WriteLine("Key: "+ key);
        
        BlocklistClient blocklistClient = new BlocklistClient(new Uri(endpoint), new AzureKeyCredential(key));
        
        var blocklistName = "ProductSaleBlocklist";
        var blocklistDescription = "Contains terms related to the sale of a product.";
        
        var data = new
        {
            description = blocklistDescription,
        };
        
        // create blocklist
        var createResponse = blocklistClient.CreateOrUpdateTextBlocklist(blocklistName, RequestContent.Create(data));
        
        if (createResponse.Status == 201)
        {
            Console.WriteLine("\nBlocklist {0} created.", blocklistName);
        }
        
        // Add blocklistItems
                
        string blocklistItemText1 = "price";
        string blocklistItemText2 = "offer";
        
        var blocklistItems = new TextBlocklistItem[] { new TextBlocklistItem(blocklistItemText1), new TextBlocklistItem(blocklistItemText2) };
        var addedBlocklistItems = blocklistClient.AddOrUpdateBlocklistItems(blocklistName, new AddOrUpdateTextBlocklistItemsOptions(blocklistItems));
        
        if (addedBlocklistItems != null && addedBlocklistItems.Value != null)
        {
            Console.WriteLine("\nBlocklistItems added:");
            foreach (var addedBlocklistItem in addedBlocklistItems.Value.BlocklistItems)
            {
                Console.WriteLine("BlocklistItemId: {0}, Text: {1}, Description: {2}", addedBlocklistItem.BlocklistItemId, addedBlocklistItem.Text, addedBlocklistItem.Description);
            }
        }
        
        // Analyze text
        ContentSafetyClient client = new ContentSafetyClient(new Uri(endpoint), new AzureKeyCredential(key));
                
        // After you edit your blocklist, it usually takes effect in 5 minutes, please wait some time before analyzing with blocklist after editing.
        var request = new AnalyzeTextOptions("You can order a copy now for the low price of $19.99.");
        request.BlocklistNames.Add(blocklistName);
        request.HaltOnBlocklistHit  = true;
        
        Response<AnalyzeTextResult> response;
        try
        {
            response = client.AnalyzeText(request);
        }
        catch (RequestFailedException ex)
        {
            Console.WriteLine("Analyze text failed.\nStatus code: {0}, Error code: {1}, Error message: {2}", ex.Status, ex.ErrorCode, ex.Message);
            throw;
        }
        
        if (response.Value.BlocklistsMatch != null)
        {
            Console.WriteLine("\nBlocklist match result:");
            foreach (var matchResult in response.Value.BlocklistsMatch)
            {
                Console.WriteLine("BlocklistName: {0}, BlocklistItemId: {1}, BlocklistText: {2}, ", matchResult.BlocklistName, matchResult.BlocklistItemId, matchResult.BlocklistItemText);
            }
        }
    }
    static void Main()
    {
        UseBlocklist();
    }
}
```

Optionally replace the blocklist name and items with your own.

#### [Visual Studio IDE](#tab/visual-studio)

Build and run the application by selecting **Start Debugging** from the **Debug** menu at the top of the IDE window (or press **F5**).

#### [CLI](#tab/cli)

Build and run the application from your application directory with these commands:

```dotnet
dotnet build
dotnet run
```

---