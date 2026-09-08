---
title: Create a basic classifier using the Content Understanding .NET SDK
author: PatrickFarley
manager: mcleans
description: Create a classifier analyzer with the Content Understanding .NET SDK.
ms.service: azure-content-understanding-foundry-tools
ms.topic: include
ms.date: 07/20/2026
ms.author: pafarley
ai-usage: ai-assisted
---

<!-- markdownlint-disable MD025 -->

Install the required NuGet packages:

```bash
dotnet add package Azure.AI.ContentUnderstanding
dotnet add package Azure.Identity
```

Create the `ContentUnderstandingClient`:

```csharp
// Example: https://your-foundry.services.ai.azure.com/
string endpoint = "<endpoint>";
var credential = new DefaultAzureCredential();
var client = new ContentUnderstandingClient(new Uri(endpoint), credential);
```

Or authenticate with an API key:

```csharp
// Example: https://your-foundry.services.ai.azure.com/
string endpoint = "<endpoint>";
string apiKey = "<apiKey>";
var client = new ContentUnderstandingClient(new Uri(endpoint), new AzureKeyCredential(apiKey));
```

Create a classifier analyzer with content categories:

```csharp
// Define content categories for classification
var categories = new Dictionary<string, ContentCategoryDefinition>
{
    ["Loan_Application"] = new ContentCategoryDefinition
    {
        Description = "Documents submitted by individuals or businesses to request funding, typically including personal or business details, financial history, loan amount, purpose, and supporting documentation."
    },
    ["Invoice"] = new ContentCategoryDefinition
    {
        Description = "Billing documents issued by sellers or service providers to request payment for goods or services, detailing items, prices, taxes, totals, and payment terms.",
        AnalyzerId = "prebuilt-invoice" // Route Invoice segments for field extraction
    },
    ["Bank_Statement"] = new ContentCategoryDefinition
    {
        Description = "Official statements issued by banks that summarize account activity over a period, including deposits, withdrawals, fees, and balances."
    }
};

// Create analyzer configuration
var config = new ContentAnalyzerConfig
{
    ShouldReturnDetails = true,
    EnableSegment = true // Enable automatic segmentation by category
};

// Add categories to config
foreach (var kvp in categories)
{
    config.ContentCategories.Add(kvp.Key, kvp.Value);
}

// Create the classifier analyzer
var classifier = new ContentAnalyzer
{
    BaseAnalyzerId = "prebuilt-document",
    Description = "Custom classifier for financial document categorization",
    Config = config
};
classifier.Models["completion"] = "gpt-5.2";

// Create the classifier
string analyzerId = $"my_classifier_{DateTimeOffset.UtcNow.ToUnixTimeSeconds()}";
var operation = await client.CreateAnalyzerAsync(
    WaitUntil.Completed,
    analyzerId,
    classifier);

ContentAnalyzer result = operation.Value;
Console.WriteLine($"Classifier '{analyzerId}' created successfully!");
```

Analyze a document with automatic segmentation:

```csharp
// Analyze a document (EnableSegment=true automatically segments by category)
string filePath = "<file_path>";
byte[] fileBytes = File.ReadAllBytes(filePath);
Operation<AnalysisResult> analyzeOperation = await client.AnalyzeBinaryAsync(
    WaitUntil.Completed,
    analyzerId,
    BinaryData.FromBytes(fileBytes));

var analyzeResult = analyzeOperation.Value;

// Display classification results with automatic segmentation
DocumentContent docContent = (DocumentContent)analyzeResult.Contents!.First();
Console.WriteLine($"Found {docContent.Segments?.Count ?? 0} segment(s):");
foreach (var segment in docContent.Segments ?? Enumerable.Empty<DocumentContentSegment>())
{
    Console.WriteLine($"  Category: {segment.Category ?? "(unknown)"}");
    Console.WriteLine($"  Pages: {segment.StartPageNumber}-{segment.EndPageNumber}");
    Console.WriteLine($"  Segment ID: {segment.SegmentId ?? "(not available)"}");
}
```

Convert classification results to LLM-friendly text:

```csharp
// Convert classification results to LLM-friendly text.
// ToLlmInput automatically detects classification results: it expands the parent
// into per-segment blocks, each with its category label in the YAML front matter.
// Segments are separated by a ***** divider.
string llmText = analyzeResult.ToLlmInput();
Console.WriteLine(llmText);
```

Clean up:

```csharp
// Clean up: delete the classifier (for testing purposes only)
// In production, classifiers are typically kept and reused
await client.DeleteAnalyzerAsync(analyzerId);
Console.WriteLine($"Classifier '{analyzerId}' deleted successfully.");
```

**Reference**: [`Azure.AI.ContentUnderstanding` .NET samples](https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/contentunderstanding/Azure.AI.ContentUnderstanding/samples)
