---
title: "Tutorial: Create a custom analyzer using the Content Understanding .NET SDK"
author: PatrickFarley
manager: nitinme
description: Learn to create a custom analyzer with Content Understanding using the .NET SDK.
ms.service: azure-ai-content-understanding
ms.topic: include
ms.date: 03/16/2026
ms.author: lahlouchu
ai-usage: ai-assisted
---

<!-- markdownlint-disable MD025 -->

[Client library](https://www.nuget.org/packages/Azure.AI.ContentUnderstanding) | [Samples](https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/contentunderstanding/Azure.AI.ContentUnderstanding/samples) | [SDK source](https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/contentunderstanding/Azure.AI.ContentUnderstanding)

This guide shows you how to use the Content Understanding .NET SDK to create a custom analyzer that extracts structured data from your content. Custom analyzers support document, image, audio, and video content types.

## Prerequisites

* An active Azure subscription. If you don't have an Azure account, [create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
* A [Microsoft Foundry resource](https://portal.azure.com/#create/Microsoft.CognitiveServicesAIFoundry) created in a [supported region](../../language-region-support.md).
* Your resource endpoint and API key (found under **Keys and Endpoint** in the Azure portal).
* Model deployment defaults configured for your resource. See [Models and deployments](../../concepts/models-deployments.md) or this one-time [configuration script](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/contentunderstanding/Azure.AI.ContentUnderstanding/samples/Sample00_UpdateDefaults.md) for setup instructions.
* The current version of [.NET](https://dotnet.microsoft.com/download/dotnet).

## Set up

1. Create a new .NET console application:

    ```console
    dotnet new console -n CustomAnalyzerTutorial
    cd CustomAnalyzerTutorial
    ```

1. Install the Content Understanding client library for .NET:

    ```console
    dotnet add package Azure.AI.ContentUnderstanding
    ```

1. Optionally, install the Azure Identity library for Microsoft Entra authentication:

    ```console
    dotnet add package Azure.Identity
    ```

## Set up environment variables

To authenticate with the Content Understanding service, set the environment variables with your own values before running the sample:
1) `CONTENTUNDERSTANDING_ENDPOINT` - the endpoint to your Content Understanding resource.
2) `CONTENTUNDERSTANDING_KEY` - your Content Understanding API key (optional if using [Microsoft Entra ID](../../concepts/secure-communications.md) DefaultAzureCredential).

### Windows

```cmd
setx CONTENTUNDERSTANDING_ENDPOINT "your-endpoint"
setx CONTENTUNDERSTANDING_KEY "your-key"
```

### Linux / macOS

```bash
export CONTENTUNDERSTANDING_ENDPOINT="your-endpoint"
export CONTENTUNDERSTANDING_KEY="your-key"
```

## Create the client

```csharp
using Azure;
using Azure.AI.ContentUnderstanding;

string endpoint = Environment.GetEnvironmentVariable(
    "CONTENTUNDERSTANDING_ENDPOINT");
string key = Environment.GetEnvironmentVariable(
    "CONTENTUNDERSTANDING_KEY");

var client = new ContentUnderstandingClient(
    new Uri(endpoint),
    new AzureKeyCredential(key)
);
```

## Create a custom analyzer

# [Document](#tab/document)

The following example creates a custom document analyzer based on the [prebuilt document analyzer](../../concepts/prebuilt-analyzers.md). It defines fields using three extraction methods: `extract` for literal text, `generate` for AI-generated summaries, and `classify` for categorization.

```csharp
string analyzerId =
    $"my_document_analyzer_{DateTimeOffset.UtcNow.ToUnixTimeSeconds()}";

var fieldSchema = new ContentFieldSchema(
    new Dictionary<string, ContentFieldDefinition>
    {
        ["company_name"] = new ContentFieldDefinition
        {
            Type = ContentFieldType.String,
            Method = GenerationMethod.Extract,
            Description = "Name of the company"
        },
        ["total_amount"] = new ContentFieldDefinition
        {
            Type = ContentFieldType.Number,
            Method = GenerationMethod.Extract,
            Description =
                "Total amount on the document"
        },
        ["document_summary"] = new ContentFieldDefinition
        {
            Type = ContentFieldType.String,
            Method = GenerationMethod.Generate,
            Description =
                "A brief summary of the document content"
        },
        ["document_type"] = new ContentFieldDefinition
        {
            Type = ContentFieldType.String,
            Method = GenerationMethod.Classify,
            Description = "Type of document"
        }
    })
{
    Name = "company_schema",
    Description =
        "Schema for extracting company information"
};

fieldSchema.Fields["document_type"].Enum.Add("invoice");
fieldSchema.Fields["document_type"].Enum.Add("receipt");
fieldSchema.Fields["document_type"].Enum.Add("contract");
fieldSchema.Fields["document_type"].Enum.Add("report");
fieldSchema.Fields["document_type"].Enum.Add("other");

var config = new ContentAnalyzerConfig
{
    EnableFormula = true,
    EnableLayout = true,
    EnableOcr = true,
    EstimateFieldSourceAndConfidence = true,
    ShouldReturnDetails = true
};

var customAnalyzer = new ContentAnalyzer
{
    BaseAnalyzerId = "prebuilt-document",
    Description =
        "Custom analyzer for extracting"
        + " company information",
    Config = config,
    FieldSchema = fieldSchema
};

customAnalyzer.Models["completion"] = "gpt-4.1";
customAnalyzer.Models["embedding"] =
    "text-embedding-3-large";

var operation = await client.CreateAnalyzerAsync(
    WaitUntil.Completed,
    analyzerId,
    customAnalyzer);

ContentAnalyzer result = operation.Value;
Console.WriteLine(
    $"Analyzer '{analyzerId}'"
    + " created successfully!");

// Get the full analyzer details after creation
var analyzerDetails =
    await client.GetAnalyzerAsync(analyzerId);
result = analyzerDetails.Value;

if (result.Description != null)
{
    Console.WriteLine(
        $"  Description: {result.Description}");
}

if (result.FieldSchema?.Fields != null)
{
    Console.WriteLine(
        $"  Fields"
        + $" ({result.FieldSchema.Fields.Count}):");
    foreach (var kvp
        in result.FieldSchema.Fields)
    {
        var method =
            kvp.Value.Method?.ToString()
            ?? "auto";
        var fieldType =
            kvp.Value.Type?.ToString()
            ?? "unknown";
        Console.WriteLine(
            $"    - {kvp.Key}:"
            + $" {fieldType} ({method})");
    }
}
```

An example output looks like:

```text
Analyzer 'my_document_analyzer_ID' created successfully!
  Description: Custom analyzer for extracting company information
  Fields (4):
    - company_name: String (Extract)
    - total_amount: Number (Extract)
    - document_summary: String (Generate)
    - document_type: String (Classify)
```

> [!TIP]
> This code is based on [Sample04_CreateAnalyzer.md](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/contentunderstanding/Azure.AI.ContentUnderstanding/samples/Sample04_CreateAnalyzer.md) in the SDK repository.


Optionally, you can create a classifier analyzer to categorize documents and use its results to route documents to prebuilt or custom analyzers you created. Here is an example of creating a custom analyzer for classification workflows.

```csharp
// Generate a unique analyzer ID
string classifierId =
    $"my_classifier_{DateTimeOffset.UtcNow.ToUnixTimeSeconds()}";

Console.WriteLine(
    $"Creating classifier '{classifierId}'...");

// Define content categories for classification
var classifierConfig = new ContentAnalyzerConfig
{
    ShouldReturnDetails = true,
    EnableSegment = true
};

classifierConfig.ContentCategories
    .Add("Loan_Application",
        new ContentCategoryDefinition
        {
            Description =
                "Documents submitted by individuals"
                + " or businesses to request"
                + " funding, typically including"
                + " personal or business details,"
                + " financial history, loan amount,"
                + " purpose, and supporting"
                + " documentation."
        });

classifierConfig.ContentCategories
    .Add("Invoice",
        new ContentCategoryDefinition
        {
            Description =
                "Billing documents issued by"
                + " sellers or service providers"
                + " to request payment for goods"
                + " or services, detailing items,"
                + " prices, taxes, totals, and"
                + " payment terms."
        });

classifierConfig.ContentCategories
    .Add("Bank_Statement",
        new ContentCategoryDefinition
        {
            Description =
                "Official statements issued by"
                + " banks that summarize account"
                + " activity over a period,"
                + " including deposits,"
                + " withdrawals, fees,"
                + " and balances."
        });

// Create the classifier analyzer
var classifierAnalyzer = new ContentAnalyzer
{
    BaseAnalyzerId = "prebuilt-document",
    Description =
        "Custom classifier for financial"
        + " document categorization",
    Config = classifierConfig
};

classifierAnalyzer.Models["completion"] =
    "gpt-4.1";

var classifierOp =
    await client.CreateAnalyzerAsync(
        WaitUntil.Completed,
        classifierId,
        classifierAnalyzer);

// Get the full classifier details
var classifierDetails =
    await client.GetAnalyzerAsync(classifierId);
var classifierResult =
    classifierDetails.Value;

Console.WriteLine(
    $"Classifier '{classifierId}'"
    + " created successfully!");

if (classifierResult.Description != null)
{
    Console.WriteLine(
        $"  Description:"
        + $" {classifierResult.Description}");
}
```

> [!TIP]
> This code adapts the [Sample04_CreateAnalyzer.md](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/contentunderstanding/Azure.AI.ContentUnderstanding/samples/Sample04_CreateAnalyzer.md) pattern for classification workflows.



# [Image](#tab/image)

The following example creates a custom image analyzer based on the [prebuilt image analyzer](../../concepts/prebuilt-analyzers.md) for processing charts and graphs.

```csharp
string analyzerId =
    $"my_image_analyzer_{DateTimeOffset.UtcNow.ToUnixTimeSeconds()}";

var fieldSchema = new ContentFieldSchema(
    new Dictionary<string, ContentFieldDefinition>
    {
        ["Title"] = new ContentFieldDefinition
        {
            Type = ContentFieldType.String,
            Description = "Title of the chart"
        },
        ["ChartType"] = new ContentFieldDefinition
        {
            Type = ContentFieldType.String,
            Method = GenerationMethod.Classify,
            Description = "Type of chart"
        }
    })
{
    Name = "chart_schema",
    Description =
        "Schema for extracting chart information"
};

fieldSchema.Fields["ChartType"].Enum.Add("bar");
fieldSchema.Fields["ChartType"].Enum.Add("line");
fieldSchema.Fields["ChartType"].Enum.Add("pie");

var customAnalyzer = new ContentAnalyzer
{
    BaseAnalyzerId = "prebuilt-image",
    Description =
        "Custom analyzer for charts and graphs",
    FieldSchema = fieldSchema
};

customAnalyzer.Models["completion"] = "gpt-4.1";

var operation = await client.CreateAnalyzerAsync(
    WaitUntil.Completed,
    analyzerId,
    customAnalyzer);

ContentAnalyzer result = operation.Value;
Console.WriteLine(
    $"Analyzer '{analyzerId}'"
    + " created successfully!");

// Get the full analyzer details after creation
var analyzerDetails =
    await client.GetAnalyzerAsync(analyzerId);
result = analyzerDetails.Value;

if (result.Description != null)
{
    Console.WriteLine(
        $"  Description: {result.Description}");
}

if (result.FieldSchema?.Fields != null)
{
    Console.WriteLine(
        $"  Fields"
        + $" ({result.FieldSchema.Fields.Count}):");
    foreach (var kvp
        in result.FieldSchema.Fields)
    {
        var method =
            kvp.Value.Method?.ToString()
            ?? "auto";
        var fieldType =
            kvp.Value.Type?.ToString()
            ?? "unknown";
        Console.WriteLine(
            $"    - {kvp.Key}:"
            + $" {fieldType} ({method})");
    }
}
```

An example output looks like:

```text
Analyzer 'my_image_analyzer_ID' created successfully!
  Description: Custom analyzer for charts and graphs
  Fields (2):
    - Title: String (auto)
    - ChartType: String (Classify)
```

> [!TIP]
> This code adapts the [Sample04_CreateAnalyzer.md](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/contentunderstanding/Azure.AI.ContentUnderstanding/samples/Sample04_CreateAnalyzer.md) pattern for image content.

# [Audio](#tab/audio)

The following example creates a custom audio analyzer based on the [prebuilt audio analyzer](../../concepts/prebuilt-analyzers.md) for processing customer support call recordings.

```csharp
string analyzerId =
    $"my_audio_analyzer_{DateTimeOffset.UtcNow.ToUnixTimeSeconds()}";

var fieldSchema = new ContentFieldSchema(
    new Dictionary<string, ContentFieldDefinition>
    {
        ["Summary"] = new ContentFieldDefinition
        {
            Type = ContentFieldType.String,
            Method = GenerationMethod.Generate,
            Description = "Summary of the call"
        },
        ["Sentiment"] = new ContentFieldDefinition
        {
            Type = ContentFieldType.String,
            Method = GenerationMethod.Classify,
            Description =
                "Overall sentiment of the call"
        },
        ["People"] = new ContentFieldDefinition
        {
            Type = ContentFieldType.Array,
            Description =
                "List of people mentioned",
            Items = new ContentFieldDefinition
            {
                Type = ContentFieldType.Object,
                Properties =
                    new Dictionary<string,
                        ContentFieldDefinition>
                {
                    ["Name"] =
                        new ContentFieldDefinition
                    {
                        Type =
                            ContentFieldType.String
                    },
                    ["Role"] =
                        new ContentFieldDefinition
                    {
                        Type =
                            ContentFieldType.String
                    }
                }
            }
        }
    })
{
    Name = "call_center_schema",
    Description =
        "Schema for analyzing customer"
        + " support calls"
};

fieldSchema.Fields["Sentiment"]
    .Enum.Add("Positive");
fieldSchema.Fields["Sentiment"]
    .Enum.Add("Neutral");
fieldSchema.Fields["Sentiment"]
    .Enum.Add("Negative");

var config = new ContentAnalyzerConfig
{
    ShouldReturnDetails = true
};

config.Locales.Add("en-US");
config.Locales.Add("fr-FR");

var customAnalyzer = new ContentAnalyzer
{
    BaseAnalyzerId = "prebuilt-audio",
    Description =
        "Custom analyzer for customer"
        + " support calls",
    Config = config,
    FieldSchema = fieldSchema
};

customAnalyzer.Models["completion"] = "gpt-4.1";
customAnalyzer.Models["embedding"] =
    "text-embedding-3-large";

var operation = await client.CreateAnalyzerAsync(
    WaitUntil.Completed,
    analyzerId,
    customAnalyzer);

ContentAnalyzer result = operation.Value;
Console.WriteLine(
    $"Analyzer '{analyzerId}'"
    + " created successfully!");

// Get the full analyzer details after creation
var analyzerDetails =
    await client.GetAnalyzerAsync(analyzerId);
result = analyzerDetails.Value;

if (result.Description != null)
{
    Console.WriteLine(
        $"  Description: {result.Description}");
}

if (result.FieldSchema?.Fields != null)
{
    Console.WriteLine(
        $"  Fields"
        + $" ({result.FieldSchema.Fields.Count}):");
    foreach (var kvp
        in result.FieldSchema.Fields)
    {
        var method =
            kvp.Value.Method?.ToString()
            ?? "auto";
        var fieldType =
            kvp.Value.Type?.ToString()
            ?? "unknown";
        Console.WriteLine(
            $"    - {kvp.Key}:"
            + $" {fieldType} ({method})");
    }
}
```

An example output looks like:

```text
Analyzer 'my_audio_analyzer_ID' created successfully!
  Description: Custom analyzer for customer support calls
  Fields (3):
    - Summary: String (Generate)
    - Sentiment: String (Classify)
    - People: Array (auto)
```

> [!TIP]
> This code adapts the [Sample04_CreateAnalyzer.md](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/contentunderstanding/Azure.AI.ContentUnderstanding/samples/Sample04_CreateAnalyzer.md) pattern for audio content.

# [Video](#tab/video)

The following example creates a custom video analyzer based on the [prebuilt video analyzer](../../concepts/prebuilt-analyzers.md) for processing product demos and reviews.

```csharp
string analyzerId =
    $"my_video_analyzer_{DateTimeOffset.UtcNow.ToUnixTimeSeconds()}";

var fieldSchema = new ContentFieldSchema(
    new Dictionary<string, ContentFieldDefinition>
    {
        ["Segments"] = new ContentFieldDefinition
        {
            Type = ContentFieldType.Array,
            Items = new ContentFieldDefinition
            {
                Type = ContentFieldType.Object,
                Properties =
                    new Dictionary<string,
                        ContentFieldDefinition>
                {
                    ["SegmentId"] =
                        new ContentFieldDefinition
                    {
                        Type =
                            ContentFieldType.String
                    },
                    ["Description"] =
                        new ContentFieldDefinition
                    {
                        Type =
                            ContentFieldType.String,
                        Method =
                            GenerationMethod.Generate,
                        Description =
                            "Detailed summary of the "
                            + "video segment"
                    },
                    ["Sentiment"] =
                        new ContentFieldDefinition
                    {
                        Type =
                            ContentFieldType.String,
                        Method =
                            GenerationMethod.Classify
                    }
                }
            }
        }
    })
{
    Name = "video_schema",
    Description =
        "Schema for analyzing product"
        + " demo videos"
};

var sentimentDef =
    fieldSchema.Fields["Segments"]
        .Items.Properties["Sentiment"];
sentimentDef.Enum.Add("Positive");
sentimentDef.Enum.Add("Neutral");
sentimentDef.Enum.Add("Negative");

var config = new ContentAnalyzerConfig
{
    ShouldReturnDetails = true
};

config.Locales.Add("en-US");
config.Locales.Add("fr-FR");

var customAnalyzer = new ContentAnalyzer
{
    BaseAnalyzerId = "prebuilt-video",
    Description =
        "Custom analyzer for product"
        + " demo videos",
    Config = config,
    FieldSchema = fieldSchema
};

customAnalyzer.Models["completion"] = "gpt-4.1";

var operation = await client.CreateAnalyzerAsync(
    WaitUntil.Completed,
    analyzerId,
    customAnalyzer);

ContentAnalyzer result = operation.Value;
Console.WriteLine(
    $"Analyzer '{analyzerId}'"
    + " created successfully!");

// Get the full analyzer details after creation
var analyzerDetails =
    await client.GetAnalyzerAsync(analyzerId);
result = analyzerDetails.Value;

if (result.Description != null)
{
    Console.WriteLine(
        $"  Description: {result.Description}");
}

if (result.FieldSchema?.Fields != null)
{
    Console.WriteLine(
        $"  Fields"
        + $" ({result.FieldSchema.Fields.Count}):");
    foreach (var kvp
        in result.FieldSchema.Fields)
    {
        var method =
            kvp.Value.Method?.ToString()
            ?? "auto";
        var fieldType =
            kvp.Value.Type?.ToString()
            ?? "unknown";
        Console.WriteLine(
            $"    - {kvp.Key}:"
            + $" {fieldType} ({method})");
    }
}
```

An example output looks like:

```text
Analyzer 'my_video_analyzer_ID' created successfully!
  Description: Custom analyzer for product demo videos
  Fields (1):
    - Segments: Array (auto)
```

> [!TIP]
> This code adapts the [Sample04_CreateAnalyzer.md](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/contentunderstanding/Azure.AI.ContentUnderstanding/samples/Sample04_CreateAnalyzer.md) pattern for video content.

---

## Use the custom analyzer

# [Document](#tab/document)

After creating the analyzer, use it to analyze a document and extract the custom fields. Delete the analyzer when you no longer need it.

```csharp
var documentUrl = new Uri(
    "https://raw.githubusercontent.com/"
    + "Azure-Samples/"
    + "azure-ai-content-understanding-assets/"
    + "main/document/invoice.pdf"
);

var analyzeOperation = await client.AnalyzeAsync(
    WaitUntil.Completed,
    analyzerId,
    inputs: new[] {
        new AnalysisInput { Uri = documentUrl }
    });

var analyzeResult = analyzeOperation.Value;

if (analyzeResult.Contents?.FirstOrDefault()
    is DocumentContent content)
{
    if (content.Fields.TryGetValue(
        "company_name", out var companyField))
    {
        var name =
            companyField is ContentStringField sf
                ? sf.Value : null;
        Console.WriteLine(
            $"Company Name: "
            + $"{name ?? "(not found)"}");
        Console.WriteLine(
            "  Confidence: "
            + (companyField.Confidence?
                .ToString("F2") ?? "N/A"));
    }

    if (content.Fields.TryGetValue(
        "total_amount", out var totalField))
    {
        var total =
            totalField is ContentNumberField nf
                ? nf.Value : null;
        Console.WriteLine(
            $"Total Amount: {total}");
    }

    if (content.Fields.TryGetValue(
        "document_summary", out var summaryField))
    {
        var summary =
            summaryField is ContentStringField sf
                ? sf.Value : null;
        Console.WriteLine(
            $"Summary: "
            + $"{summary ?? "(not found)"}");
    }

    if (content.Fields.TryGetValue(
        "document_type", out var typeField))
    {
        var docType =
            typeField is ContentStringField sf
                ? sf.Value : null;
        Console.WriteLine(
            $"Document Type: "
            + $"{docType ?? "(not found)"}");
    }
}

// --- Clean up ---
Console.WriteLine(
    $"\nCleaning up: deleting analyzer"
    + $" '{analyzerId}'...");
await client.DeleteAnalyzerAsync(analyzerId);
Console.WriteLine(
    $"Analyzer '{analyzerId}'"
    + " deleted successfully.");
```

An example output looks like:

```text
Company Name: CONTOSO LTD.
  Confidence: 0.81
Total Amount: 610.0
Summary: This document is an invoice from CONTOSO LTD. ...
Document Type: invoice

Cleaning up: deleting analyzer 'my_document_analyzer_ID'...
Analyzer 'my_document_analyzer_ID' deleted successfully.
```

> [!TIP]
> Check out more examples of running analyzers at [.NET SDK samples](https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/contentunderstanding/Azure.AI.ContentUnderstanding/samples).

# [Image](#tab/image)

After creating the analyzer, use it to analyze an image and extract the custom fields. Delete the analyzer when you no longer need it.

```csharp
var imageUrl = new Uri(
    "https://raw.githubusercontent.com/"
    + "Azure-Samples/"
    + "azure-ai-content-understanding-assets/"
    + "main/image/pieChart.jpg"
);

var analyzeOperation = await client.AnalyzeAsync(
    WaitUntil.Completed,
    analyzerId,
    inputs: new[] {
        new AnalysisInput { Uri = imageUrl }
    });

var analyzeResult = analyzeOperation.Value;

if (analyzeResult.Contents?.FirstOrDefault()
    is DocumentContent content)
{
    if (content.Fields.TryGetValue(
        "Title", out var titleField))
    {
        var title =
            titleField is ContentStringField sf
                ? sf.Value : null;
        Console.WriteLine(
            $"Title: {title ?? "(not found)"}");
    }

    if (content.Fields.TryGetValue(
        "ChartType", out var chartField))
    {
        var chartType =
            chartField is ContentStringField sf
                ? sf.Value : null;
        Console.WriteLine(
            $"Chart Type: "
            + $"{chartType ?? "(not found)"}");
    }
}

// --- Clean up ---
Console.WriteLine(
    $"\nCleaning up: deleting analyzer"
    + $" '{analyzerId}'...");
await client.DeleteAnalyzerAsync(analyzerId);
Console.WriteLine(
    $"Analyzer '{analyzerId}'"
    + " deleted successfully.");
```

An example output looks like:

```text
Title: Distribution of Weekly Working Hours
Chart Type: pie

Cleaning up: deleting analyzer 'my_image_analyzer_ID'...
Analyzer 'my_image_analyzer_ID' deleted successfully.
```

> [!TIP]
> Check out more examples of running analyzers at [.NET SDK samples](https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/contentunderstanding/Azure.AI.ContentUnderstanding/samples).

# [Audio](#tab/audio)

After creating the analyzer, use it to analyze an audio file and extract the custom fields. Delete the analyzer when you no longer need it.

```csharp
var audioUrl = new Uri(
    "https://raw.githubusercontent.com/"
    + "Azure-Samples/"
    + "azure-ai-content-understanding-assets/"
    + "main/audio/callCenterRecording.mp3"
);

var analyzeOperation = await client.AnalyzeAsync(
    WaitUntil.Completed,
    analyzerId,
    inputs: new[] {
        new AnalysisInput { Uri = audioUrl }
    });

var analyzeResult = analyzeOperation.Value;

if (analyzeResult.Contents?.Count > 0)
{
    var content = analyzeResult.Contents[0];
    if (content.Fields != null)
    {
        if (content.Fields.TryGetValue(
            "Summary", out var summaryField))
        {
            var summary =
                summaryField
                    is ContentStringField sf
                    ? sf.Value : null;
            Console.WriteLine(
                $"Summary: "
                + $"{summary ?? "(not found)"}");
        }

        if (content.Fields.TryGetValue(
            "Sentiment", out var sentField))
        {
            var sentiment =
                sentField
                    is ContentStringField sf
                    ? sf.Value : null;
            Console.WriteLine(
                $"Sentiment: "
                + $"{sentiment ?? "(not found)"}");
        }
    }
}

// --- Clean up ---
Console.WriteLine(
    $"\nCleaning up: deleting analyzer"
    + $" '{analyzerId}'...");
await client.DeleteAnalyzerAsync(analyzerId);
Console.WriteLine(
    $"Analyzer '{analyzerId}'"
    + " deleted successfully.");
```

An example output looks like:

```text
Summary: Maria Smith contacted Contoso to inquire about her current point balance...
Sentiment: Positive

Cleaning up: deleting analyzer 'my_audio_analyzer_ID'...
Analyzer 'my_audio_analyzer_ID' deleted successfully.
```

> [!TIP]
> Check out more examples of running analyzers at [.NET SDK samples](https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/contentunderstanding/Azure.AI.ContentUnderstanding/samples).

# [Video](#tab/video)

After creating the analyzer, use it to analyze a video and extract the custom fields. Delete the analyzer when you no longer need it.

```csharp
var videoUrl = new Uri(
    "https://raw.githubusercontent.com/"
    + "Azure-Samples/"
    + "azure-ai-content-understanding-assets/"
    + "main/videos/sdk_samples/"
    + "FlightSimulator.mp4"
);

var analyzeOperation = await client.AnalyzeAsync(
    WaitUntil.Completed,
    analyzerId,
    inputs: new[] {
        new AnalysisInput { Uri = videoUrl }
    });

var analyzeResult = analyzeOperation.Value;

if (analyzeResult.Contents?.Count > 0)
{
    var content = analyzeResult.Contents[0];
    Console.WriteLine(
        $"Content type: {content.Kind}");
    if (content.Fields != null
        && content.Fields.TryGetValue(
            "Segments", out var segmentsField))
    {
        Console.WriteLine(
            $"Segments: {segmentsField}");
    }
}

// --- Clean up ---
Console.WriteLine(
    $"\nCleaning up: deleting analyzer"
    + $" '{analyzerId}'...");
await client.DeleteAnalyzerAsync(analyzerId);
Console.WriteLine(
    $"Analyzer '{analyzerId}'"
    + " deleted successfully.");
```

An example output looks like:

```text
Content type: video
Segments: [placeholder - video segment data]

Cleaning up: deleting analyzer 'my_video_analyzer_ID'...
Analyzer 'my_video_analyzer_ID' deleted successfully.
```

> [!TIP]
> Check out more examples of running analyzers at [.NET SDK samples](https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/contentunderstanding/Azure.AI.ContentUnderstanding/samples).

---



