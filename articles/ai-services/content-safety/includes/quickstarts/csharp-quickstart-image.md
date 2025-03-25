---
title: "Quickstart: Analyze image content with C#"
description: In this quickstart, get started using the Azure AI Content Safety .NET SDK to analyze image content for objectionable material.
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-content-safety
ms.custom:
ms.topic: include
ms.date: 03/07/2024
ms.author: pafarley
---

[Reference documentation](/dotnet/api/overview/azure/ai.contentsafety-readme) | [Library source code](https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/contentsafety/Azure.AI.ContentSafety) | [Package (NuGet)](https://www.nuget.org/packages/Azure.AI.ContentSafety) | [Samples](https://github.com/Azure-Samples/AzureAIContentSafety/tree/main/dotnet/1.0.0)

## Prerequisites

* An Azure subscription - [Create one for free](https://azure.microsoft.com/free/cognitive-services/) 
* The [Visual Studio IDE](https://visualstudio.microsoft.com/vs/) with workload .NET desktop development enabled. Or if you don't plan on using Visual Studio IDE, you need the current version of [.NET Core](https://dotnet.microsoft.com/download/dotnet-core).
* [.NET Runtime](https://dotnet.microsoft.com/download/dotnet/) installed.
* Once you have your Azure subscription, <a href="https://aka.ms/acs-create"  title="Create a Content Safety resource"  target="_blank">create a Content Safety resource </a> in the Azure portal to get your key and endpoint. Enter a unique name for your resource, select your subscription, and select a resource group, supported region (see [Region availability](/azure/ai-services/content-safety/overview#region-availability)), and supported pricing tier. Then select **Create**.
  * The resource takes a few minutes to deploy. After it finishes, Select **go to resource**. In the left pane, under **Resource Management**, select **Subscription Key and Endpoint**. The endpoint and either of the keys are used to call APIs.

## Set up application

Create a new C# application.

#### [Visual Studio IDE](#tab/visual-studio)

Open Visual Studio, and under **Get started** select **Create a new project**. Set the template filters to _C#/All Platforms/Console_. Select **Console App** (command-line application that can run on .NET on Windows, Linux and macOS) and choose **Next**. Update the project name to _ContentSafetyQuickstart_ and choose **Next**. Select **.NET 6.0** or above, and choose **Create** to create the project.

### Install the client SDK 

Once you've created a new project, install the client SDK by right-clicking on the project solution in the **Solution Explorer** and selecting **Manage NuGet Packages**. In the package manager that opens select **Browse** and search for `Azure.AI.ContentSafety`. Select **Install**.

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

Within the application directory, install the Computer Vision client SDK for .NET with the following command:

```dotnet
dotnet add package Azure.AI.ContentSafety
```
    
---

[!INCLUDE [Create environment variables](../env-vars.md)]

## Analyze image content

From the project directory, open the *Program.cs* file that was created previously. Paste in the following code.

```csharp
using System;
using Azure.AI.ContentSafety;

namespace Azure.AI.ContentSafety.Dotnet.Sample
{
  class ContentSafetySampleAnalyzeImage
  {
    public static void AnalyzeImage()
    {
      // retrieve the endpoint and key from the environment variables created earlier
      string endpoint = Environment.GetEnvironmentVariable("CONTENT_SAFETY_ENDPOINT");
      string key = Environment.GetEnvironmentVariable("CONTENT_SAFETY_KEY");

      ContentSafetyClient client = new ContentSafetyClient(new Uri(endpoint), new AzureKeyCredential(key));

      // Example: analyze image

      string imagePath = @"sample_data\image.png";
      ContentSafetyImageData image = new ContentSafetyImageData(BinaryData.FromBytes(File.ReadAllBytes(imagePath)));

      var request = new AnalyzeImageOptions(image);

      Response<AnalyzeImageResult> response;
      try
      {
          response = client.AnalyzeImage(request);
      }
      catch (RequestFailedException ex)
      {
          Console.WriteLine("Analyze image failed.\nStatus code: {0}, Error code: {1}, Error message: {2}", ex.Status, ex.ErrorCode, ex.Message);
          throw;
      }

      Console.WriteLine("Hate severity: {0}", response.Value.CategoriesAnalysis.FirstOrDefault(a => a.Category == ImageCategory.Hate)?.Severity ?? 0);
      Console.WriteLine("SelfHarm severity: {0}", response.Value.CategoriesAnalysis.FirstOrDefault(a => a.Category == ImageCategory.SelfHarm)?.Severity ?? 0);
      Console.WriteLine("Sexual severity: {0}", response.Value.CategoriesAnalysis.FirstOrDefault(a => a.Category == ImageCategory.Sexual)?.Severity ?? 0);
      Console.WriteLine("Violence severity: {0}", response.Value.CategoriesAnalysis.FirstOrDefault(a => a.Category == ImageCategory.Violence)?.Severity ?? 0);
    }
    static void Main()
    {
      AnalyzeImage();
    }
  }
}
```

Create a _sample_data_ folder in your project directory, and add an _image.png_ file into it.

#### [Visual Studio IDE](#tab/visual-studio)

Build and run the application by selecting **Start Debugging** from the **Debug** menu at the top of the IDE window (or press **F5**).

#### [CLI](#tab/cli)

Build and run the application from your application directory with these commands:

```dotnet
dotnet build
dotnet run
```

---