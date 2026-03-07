---
title: "Quickstart: Use the Content Understanding .NET SDK"
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-content-understanding
ms.topic: include
ms.date: 03/06/2026
ms.author: paulhsu
ai-usage: ai-assisted
---

<!-- markdownlint-disable MD025 -->

[Client library](https://www.nuget.org/packages/Azure.AI.ContentUnderstanding) | [Samples](https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/contentunderstanding/Azure.AI.ContentUnderstanding/samples) | [SDK source](https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/contentunderstanding/Azure.AI.ContentUnderstanding)

This quickstart shows you how to use the Content Understanding .NET SDK to extract structured data from multimodal content in document, image, audio, and video files.

## Prerequisites

* An active Azure subscription. If you don't have an Azure account, [create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
* A [Microsoft Foundry resource](https://portal.azure.com/#create/Microsoft.CognitiveServicesAIFoundry) created in a [supported region](/azure/ai-services/content-understanding/language-region-support).
* [!INCLUDE [foundry-model-deployment-setup](../../includes/foundry-model-deployment-setup.md)]
* The current version of [.NET](https://dotnet.microsoft.com/download/dotnet).

## Set up

1. Create a new .NET console application:

    ```console
    dotnet new console -n ContentUnderstandingQuickstart
    cd ContentUnderstandingQuickstart
    ```

1. Install the Content Understanding client library for .NET:

    ```console
    dotnet add package Azure.AI.ContentUnderstanding
    ```

1. Optionally, install the Azure Identity library for Microsoft Entra authentication:

    ```console
    dotnet add package Azure.Identity
    ```

## Create your .NET application

1. Open the **Program.cs** file in your preferred editor or IDE.

1. Replace the contents of **Program.cs** with one of the following code samples:

    * [**Document search**](#document-search-model) — analyze and extract markdown content from documents.
    * [**Prebuilt invoice**](#prebuilt-model) — analyze and extract common fields from invoices.

[!INCLUDE [Azure key vault](~/reusable-content/ce-skilling/azure/includes/ai-services/security/microsoft-entra-id-akv-expanded.md)]

## Document search model

Extract markdown content, page information, and summaries from documents.

> [!div class="checklist"]
>
> * For this example, you need a **document file from a URL**. You can use the [sample invoice document](https://raw.githubusercontent.com/Azure-Samples/azure-ai-content-understanding-assets/main/document/invoice.pdf) for this quickstart.
> * The file URL value is set in the `documentUrl` variable within the `Main` method.

**Add the following code sample to your Program.cs file. Make sure you update the endpoint and key variables with values from your Microsoft Foundry resource in the Azure portal:**

```csharp
using System;
using System.Threading.Tasks;
using Azure;
using Azure.AI.ContentUnderstanding;

// set `<your-endpoint>` and `<your-key>` variables
// with the values from the Azure portal
string endpoint = "<your-endpoint>";
string key = "<your-key>";

var client = new ContentUnderstandingClient(
    new Uri(endpoint),
    new AzureKeyCredential(key)
);

// Sample document
string documentUrl =
    "https://raw.githubusercontent.com/"
    + "Azure-Samples/"
    + "azure-ai-content-understanding-assets/"
    + "main/document/invoice.pdf";

var result = await client.AnalyzeAsync(
    WaitUntil.Completed,
    "prebuilt-documentSearch",
    inputs: new[] { new AnalysisInput { Uri = documentUrl } }
);

if (result.Value.Contents != null
    && result.Value.Contents.Count > 0)
{
    var content = result.Value.Contents[0];
    Console.WriteLine("Markdown:");
    Console.WriteLine(content.Markdown);

    // Access document-specific properties
    if (content is DocumentContent documentContent)
    {
        Console.WriteLine(
            $"\nPages: {documentContent.StartPageNumber}"
            + $" - {documentContent.EndPageNumber}"
        );

        if (documentContent.Pages != null
            && documentContent.Pages.Count > 0)
        {
            Console.WriteLine(
                $"Number of pages: {documentContent.Pages.Count}"
            );

            foreach (var page in documentContent.Pages)
            {
                string unit = documentContent.Unit ?? "units";
                Console.WriteLine(
                    $"  Page {page.PageNumber}: "
                    + $"{page.Width} x {page.Height} {unit}"
                );
            }
        }
    }
}
```

> [!NOTE]
> This code is based on the [Sample02_AnalyzeUrl](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/contentunderstanding/Azure.AI.ContentUnderstanding/samples/Sample02_AnalyzeUrl.md) sample in the SDK repository.

**Run the application**

After you add the code sample to your application, build and run your program:

1. Navigate to the folder where you have your **ContentUnderstandingQuickstart** project.

1. Type the following command in your terminal:

    ```console
    dotnet run
    ```

**Reference**: [`ContentUnderstandingClient`](https://www.nuget.org/packages/Azure.AI.ContentUnderstanding), [`AnalyzeAsync`](https://www.nuget.org/packages/Azure.AI.ContentUnderstanding)

___

## Prebuilt model

Analyze and extract common fields from specific document types using a prebuilt model. In this example, we analyze an invoice using the **prebuilt-invoice** analyzer.

> [!TIP]
> You aren't limited to invoices—there are several prebuilt analyzers to choose from, each of which has its own set of supported fields. For more information, see [prebuilt analyzers](../../concepts/prebuilt-analyzers.md).

> [!div class="checklist"]
>
> * Analyze an invoice using the prebuilt-invoice analyzer. You can use the [sample invoice document](https://raw.githubusercontent.com/Azure-Samples/azure-ai-content-understanding-assets/main/document/invoice.pdf) for this quickstart.
> * The file URL value is set in the `invoiceUrl` variable within the `Main` method.

**Add the following code sample to your Program.cs file. Make sure you update the endpoint and key variables with values from your Microsoft Foundry resource in the Azure portal:**

```csharp
using System;
using System.Threading.Tasks;
using Azure;
using Azure.AI.ContentUnderstanding;

// set `<your-endpoint>` and `<your-key>` variables
// with the values from the Azure portal
string endpoint = "<your-endpoint>";
string key = "<your-key>";

var client = new ContentUnderstandingClient(
    new Uri(endpoint),
    new AzureKeyCredential(key)
);

// Sample invoice
string invoiceUrl =
    "https://raw.githubusercontent.com/"
    + "Azure-Samples/"
    + "azure-ai-content-understanding-assets/"
    + "main/document/invoice.pdf";

var result = await client.AnalyzeAsync(
    WaitUntil.Completed,
    "prebuilt-invoice",
    inputs: new[] { new AnalysisInput { Uri = invoiceUrl } }
);

if (result.Value.Contents == null
    || result.Value.Contents.Count == 0)
{
    Console.WriteLine("No content found in the analysis result.");
    return;
}

// Get the document content
if (result.Value.Contents[0] is DocumentContent documentContent)
{
    Console.WriteLine(
        $"Document unit: {documentContent.Unit ?? "unknown"}"
    );
    Console.WriteLine(
        $"Pages: {documentContent.StartPageNumber}"
        + $" to {documentContent.EndPageNumber}"
    );

    if (documentContent.Fields == null)
    {
        Console.WriteLine("No fields found.");
        return;
    }

    // Extract simple string fields
    if (documentContent.Fields.TryGetValue(
            "CustomerName", out var customerNameField))
    {
        Console.WriteLine(
            $"Customer Name: {customerNameField.Value}"
        );
        if (customerNameField.Confidence.HasValue)
        {
            Console.WriteLine(
                $"  Confidence: "
                + $"{customerNameField.Confidence.Value:F2}"
            );
        }
        Console.WriteLine(
            $"  Source: {customerNameField.Source ?? "N/A"}"
        );
    }

    // Extract date fields
    if (documentContent.Fields.TryGetValue(
            "InvoiceDate", out var invoiceDateField))
    {
        Console.WriteLine(
            $"Invoice Date: {invoiceDateField.Value}"
        );
        if (invoiceDateField.Confidence.HasValue)
        {
            Console.WriteLine(
                $"  Confidence: "
                + $"{invoiceDateField.Confidence.Value:F2}"
            );
        }
    }

    // Extract object fields (nested structures)
    if (documentContent.Fields.TryGetValue(
            "TotalAmount", out var totalAmountField)
        && totalAmountField is ContentObjectField totalAmountObj
        && totalAmountObj.Value != null)
    {
        totalAmountObj.Value.TryGetValue(
            "Amount", out var amountField);
        totalAmountObj.Value.TryGetValue(
            "CurrencyCode", out var currencyField);

        string amount = amountField?.Value?.ToString() ?? "(None)";
        string currency = currencyField?.Value?.ToString() ?? "";

        Console.WriteLine($"\nTotal: {currency}{amount}");
    }

    // Extract array fields (line items)
    if (documentContent.Fields.TryGetValue(
            "LineItems", out var lineItemsField)
        && lineItemsField is ContentArrayField lineItemsArr
        && lineItemsArr.Value != null)
    {
        Console.WriteLine(
            $"\nLine Items ({lineItemsArr.Value.Count}):"
        );

        for (int i = 0; i < lineItemsArr.Value.Count; i++)
        {
            if (lineItemsArr.Value[i]
                is ContentObjectField itemObj
                && itemObj.Value != null)
            {
                itemObj.Value.TryGetValue(
                    "Description", out var descField);
                itemObj.Value.TryGetValue(
                    "Quantity", out var qtyField);

                string description =
                    descField?.Value?.ToString() ?? "N/A";
                string quantity =
                    qtyField?.Value?.ToString() ?? "N/A";

                Console.WriteLine(
                    $"  Item {i + 1}: {description}"
                );
                Console.WriteLine(
                    $"    Quantity: {quantity}"
                );
            }
        }
    }
}
```

> [!NOTE]
> This code is based on the [Sample03_AnalyzeInvoice](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/contentunderstanding/Azure.AI.ContentUnderstanding/samples/Sample03_AnalyzeInvoice.md) sample in the SDK repository.

**Run the application**

After you add the code sample to your application, build and run your program:

1. Navigate to the folder where you have your **ContentUnderstandingQuickstart** project.

1. Type the following command in your terminal:

    ```console
    dotnet run
    ```

**Reference**: [`ContentUnderstandingClient`](https://www.nuget.org/packages/Azure.AI.ContentUnderstanding), [`AnalyzeAsync`](https://www.nuget.org/packages/Azure.AI.ContentUnderstanding)

## Next steps

* Explore more [.NET SDK samples](https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/contentunderstanding/Azure.AI.ContentUnderstanding/samples)
* [Create a custom analyzer](../../tutorial/create-custom-analyzer.md)
* [Prebuilt analyzers](../../concepts/prebuilt-analyzers.md)
* [Language and region support](../../language-region-support.md)
