---
title: "Tutorial: Create a custom analyzer using the Content Understanding Java SDK"
author: PatrickFarley
manager: nitinme
description: Learn to create a custom analyzer with Content Understanding using the Java SDK.
ms.service: azure-ai-content-understanding
ms.topic: include
ms.date: 03/16/2026
ms.author: lahlouchu
ai-usage: ai-assisted
---

<!-- markdownlint-disable MD025 -->

[Client library](https://central.sonatype.com/artifact/com.azure/azure-ai-contentunderstanding) | [Samples](https://github.com/Azure/azure-sdk-for-java/tree/main/sdk/contentunderstanding/azure-ai-contentunderstanding/src/samples/java/com/azure/ai/contentunderstanding) | [SDK source](https://github.com/Azure/azure-sdk-for-java/tree/main/sdk/contentunderstanding/azure-ai-contentunderstanding)

This guide shows you how to use the Content Understanding Java SDK to create a custom analyzer that extracts structured data from your content. Custom analyzers support document, image, audio, and video content types.

## Prerequisites

* An active Azure subscription. If you don't have an Azure account, [create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
* A [Microsoft Foundry resource](https://portal.azure.com/#create/Microsoft.CognitiveServicesAIFoundry) created in a [supported region](../../language-region-support.md).
* Your resource endpoint and API key (found under **Keys and Endpoint** in the Azure portal).
* Model deployment defaults configured for your resource. See [Models and deployments](../../concepts/models-deployments.md) or this one-time [configuration script](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/contentunderstanding/azure-ai-contentunderstanding/src/samples/java/com/azure/ai/contentunderstanding/samples/Sample00_UpdateDefaults.java) for setup instructions.
* [Java Development Kit (JDK)](/java/openjdk/download) version 8 or later.
* [Apache Maven](https://maven.apache.org/download.cgi).

## Set up

1. Create a new Maven project:

    ```console
    mvn archetype:generate -DgroupId=com.example \
        -DartifactId=custom-analyzer-tutorial \
        -DarchetypeArtifactId=maven-archetype-quickstart \
        -DinteractiveMode=false
    cd custom-analyzer-tutorial
    ```

1. Add the Content Understanding dependency to your **pom.xml** file in the `<dependencies>` section:

    ```xml
    <dependency>
        <groupId>com.azure</groupId>
        <artifactId>azure-ai-contentunderstanding</artifactId>
        <version>1.0.0</version>
    </dependency>
    ```

1. Optionally, add the Azure Identity library for Microsoft Entra authentication:

    ```xml
    <dependency>
        <groupId>com.azure</groupId>
        <artifactId>azure-identity</artifactId>
        <version>1.14.2</version>
    </dependency>
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

```java
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;
import com.azure.core.credential.AzureKeyCredential;
import com.azure.core.util.polling.SyncPoller;
import com.azure.ai.contentunderstanding
    .ContentUnderstandingClient;
import com.azure.ai.contentunderstanding
    .ContentUnderstandingClientBuilder;
import com.azure.ai.contentunderstanding.models.*;

String endpoint =
    System.getenv("CONTENTUNDERSTANDING_ENDPOINT");
String key =
    System.getenv("CONTENTUNDERSTANDING_KEY");

ContentUnderstandingClient client =
    new ContentUnderstandingClientBuilder()
        .endpoint(endpoint)
        .credential(new AzureKeyCredential(key))
        .buildClient();
```

## Create a custom analyzer

# [Document](#tab/document)

The following example creates a custom document analyzer based on the [prebuilt document analyzer](../../concepts/prebuilt-analyzers.md). It defines fields using three extraction methods: `extract` for literal text, `generate` for AI-generated summaries, and `classify` for categorization.

```java
String analyzerId =
    "my_document_analyzer_"
    + System.currentTimeMillis();

Map<String, ContentFieldDefinition> fields =
    new HashMap<>();

ContentFieldDefinition companyNameDef =
    new ContentFieldDefinition();
companyNameDef.setType(ContentFieldType.STRING);
companyNameDef.setMethod(
    GenerationMethod.EXTRACT);
companyNameDef.setDescription(
    "Name of the company");
fields.put("company_name", companyNameDef);

ContentFieldDefinition totalAmountDef =
    new ContentFieldDefinition();
totalAmountDef.setType(ContentFieldType.NUMBER);
totalAmountDef.setMethod(
    GenerationMethod.EXTRACT);
totalAmountDef.setDescription(
    "Total amount on the document");
fields.put("total_amount", totalAmountDef);

ContentFieldDefinition summaryDef =
    new ContentFieldDefinition();
summaryDef.setType(ContentFieldType.STRING);
summaryDef.setMethod(
    GenerationMethod.GENERATE);
summaryDef.setDescription(
    "A brief summary of the document content");
fields.put("document_summary", summaryDef);

ContentFieldDefinition documentTypeDef =
    new ContentFieldDefinition();
documentTypeDef.setType(ContentFieldType.STRING);
documentTypeDef.setMethod(
    GenerationMethod.CLASSIFY);
documentTypeDef.setDescription(
    "Type of document");
documentTypeDef.setEnumProperty(
    Arrays.asList(
        "invoice", "receipt", "contract",
        "report", "other"
    ));
fields.put("document_type", documentTypeDef);

ContentFieldSchema fieldSchema =
    new ContentFieldSchema();
fieldSchema.setName("company_schema");
fieldSchema.setDescription(
    "Schema for extracting company information");
fieldSchema.setFields(fields);

Map<String, String> models = new HashMap<>();
models.put("completion", "gpt-4.1");
models.put("embedding", "text-embedding-3-large"); // Required when using field_schema and prebuilt-document base analyzer

ContentAnalyzer customAnalyzer =
    new ContentAnalyzer()
        .setBaseAnalyzerId("prebuilt-document")
        .setDescription(
            "Custom analyzer for extracting"
            + " company information")
        .setConfig(new ContentAnalyzerConfig()
            .setOcrEnabled(true)
            .setLayoutEnabled(true)
            .setFormulaEnabled(true)
            .setEstimateFieldSourceAndConfidence(
                true)
            .setReturnDetails(true))
        .setFieldSchema(fieldSchema)
        .setModels(models);

SyncPoller<ContentAnalyzerOperationStatus,
    ContentAnalyzer> operation =
    client.beginCreateAnalyzer(
        analyzerId, customAnalyzer, true);

ContentAnalyzer result =
    operation.getFinalResult();
System.out.println(
    "Analyzer '" + analyzerId
    + "' created successfully!");

if (result.getDescription() != null) {
    System.out.println(
        "  Description: "
        + result.getDescription());
}

if (result.getFieldSchema() != null
    && result.getFieldSchema()
        .getFields() != null) {
    System.out.println(
        "  Fields ("
        + result.getFieldSchema()
            .getFields().size() + "):");
    result.getFieldSchema().getFields()
        .forEach((fieldName, fieldDef) -> {
            String method =
                fieldDef.getMethod() != null
                    ? fieldDef.getMethod()
                        .toString()
                    : "auto";
            String type =
                fieldDef.getType() != null
                    ? fieldDef.getType()
                        .toString()
                    : "unknown";
            System.out.println(
                "    - " + fieldName
                + ": " + type
                + " (" + method + ")");
        });
}
```

An example output looks like:

```text
Analyzer 'my_document_analyzer_ID' created successfully!
  Description: Custom analyzer for extracting company information
  Fields (4):
    - total_amount: number (extract)
    - company_name: string (extract)
    - document_summary: string (generate)
    - document_type: string (classify)
```

> [!TIP]
> This code is based on the [CreateAnalyzer](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/contentunderstanding/azure-ai-contentunderstanding/src/samples/java/com/azure/ai/contentunderstanding/samples/Sample04_CreateAnalyzer.java) sample in the SDK repository.


Optionally, you can create a classifier analyzer to categorize documents and use its results to route documents to prebuilt or custom analyzers you created. Here is an example of creating a custom analyzer for classification workflows.

```java
// Generate a unique analyzer ID
String classifierId =
    "my_classifier_" + System.currentTimeMillis();

System.out.println(
    "Creating classifier '"
    + classifierId + "'...");

// Define content categories for classification
Map<String, ContentCategoryDefinition>
    categories = new HashMap<>();

categories.put("Loan_Application",
    new ContentCategoryDefinition()
        .setDescription(
            "Documents submitted by individuals"
            + " or businesses to request funding,"
            + " typically including personal or"
            + " business details, financial"
            + " history, loan amount, purpose,"
            + " and supporting documentation."));

categories.put("Invoice",
    new ContentCategoryDefinition()
        .setDescription(
            "Billing documents issued by sellers"
            + " or service providers to request"
            + " payment for goods or services,"
            + " detailing items, prices, taxes,"
            + " totals, and payment terms."));

categories.put("Bank_Statement",
    new ContentCategoryDefinition()
        .setDescription(
            "Official statements issued by banks"
            + " that summarize account activity"
            + " over a period, including deposits,"
            + " withdrawals, fees,"
            + " and balances."));

// Create the classifier
Map<String, String> classifierModels =
    new HashMap<>();
classifierModels.put("completion", "gpt-4.1");

ContentAnalyzer classifier =
    new ContentAnalyzer()
        .setBaseAnalyzerId("prebuilt-document")
        .setDescription(
            "Custom classifier for financial"
            + " document categorization")
        .setConfig(new ContentAnalyzerConfig()
            .setReturnDetails(true)
            .setSegmentEnabled(true)
            .setContentCategories(categories))
        .setModels(classifierModels);

SyncPoller<ContentAnalyzerOperationStatus,
    ContentAnalyzer> classifierOp =
    client.beginCreateAnalyzer(
        classifierId, classifier, true);
classifierOp.getFinalResult();

// Get the full classifier details
ContentAnalyzer classifierResult =
    client.getAnalyzer(classifierId);

System.out.println(
    "Classifier '" + classifierId
    + "' created successfully!");

if (classifierResult.getDescription() != null) {
    System.out.println(
        "  Description: "
        + classifierResult.getDescription());
}
```

> [!TIP]
> This code is based on the [CreateClassifier](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/contentunderstanding/azure-ai-contentunderstanding/src/samples/java/com/azure/ai/contentunderstanding/samples/Sample05_CreateClassifier.java) sample for classification workflows.



# [Image](#tab/image)

The following example creates a custom image analyzer based on the [prebuilt image analyzer](../../concepts/prebuilt-analyzers.md) for processing charts and graphs.

```java
String analyzerId =
    "my_image_analyzer_"
    + System.currentTimeMillis();

Map<String, ContentFieldDefinition> fields =
    new HashMap<>();

ContentFieldDefinition titleDef =
    new ContentFieldDefinition();
titleDef.setType(ContentFieldType.STRING);
titleDef.setDescription("Title of the chart");
fields.put("Title", titleDef);

ContentFieldDefinition chartTypeDef =
    new ContentFieldDefinition();
chartTypeDef.setType(ContentFieldType.STRING);
chartTypeDef.setMethod(
    GenerationMethod.CLASSIFY);
chartTypeDef.setDescription("Type of chart");
chartTypeDef.setEnumProperty(
    Arrays.asList("bar", "line", "pie"));
fields.put("ChartType", chartTypeDef);

ContentFieldSchema fieldSchema =
    new ContentFieldSchema();
fieldSchema.setName("chart_schema");
fieldSchema.setDescription(
    "Schema for extracting chart information");
fieldSchema.setFields(fields);

Map<String, String> models = new HashMap<>();
models.put("completion", "gpt-4.1");

ContentAnalyzer customAnalyzer =
    new ContentAnalyzer()
        .setBaseAnalyzerId("prebuilt-image")
        .setDescription(
            "Custom analyzer for charts"
            + " and graphs")
        .setFieldSchema(fieldSchema)
        .setModels(models);

SyncPoller<ContentAnalyzerOperationStatus,
    ContentAnalyzer> operation =
    client.beginCreateAnalyzer(
        analyzerId, customAnalyzer, true);

ContentAnalyzer result =
    operation.getFinalResult();
System.out.println(
    "Analyzer '" + analyzerId
    + "' created successfully!");

if (result.getDescription() != null) {
    System.out.println(
        "  Description: "
        + result.getDescription());
}

if (result.getFieldSchema() != null
    && result.getFieldSchema()
        .getFields() != null) {
    System.out.println(
        "  Fields ("
        + result.getFieldSchema()
            .getFields().size() + "):");
    result.getFieldSchema().getFields()
        .forEach((fieldName, fieldDef) -> {
            String method =
                fieldDef.getMethod() != null
                    ? fieldDef.getMethod()
                        .toString()
                    : "auto";
            String type =
                fieldDef.getType() != null
                    ? fieldDef.getType()
                        .toString()
                    : "unknown";
            System.out.println(
                "    - " + fieldName
                + ": " + type
                + " (" + method + ")");
        });
}
```

An example output looks like:

```text
Analyzer 'my_image_analyzer_ID' created successfully!
  Description: Custom analyzer for charts and graphs
  Fields (2):
    - Title: string (auto)
    - ChartType: string (classify)
```

> [!TIP]
> This code adapts the [CreateAnalyzer](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/contentunderstanding/azure-ai-contentunderstanding/src/samples/java/com/azure/ai/contentunderstanding/samples/Sample04_CreateAnalyzer.java) pattern for image content.

# [Audio](#tab/audio)

The following example creates a custom audio analyzer based on the [prebuilt audio analyzer](../../concepts/prebuilt-analyzers.md) for processing customer support call recordings.

```java
String analyzerId =
    "my_audio_analyzer_"
    + System.currentTimeMillis();

Map<String, ContentFieldDefinition> fields =
    new HashMap<>();

ContentFieldDefinition summaryDef =
    new ContentFieldDefinition();
summaryDef.setType(ContentFieldType.STRING);
summaryDef.setMethod(
    GenerationMethod.GENERATE);
summaryDef.setDescription("Summary of the call");
fields.put("Summary", summaryDef);

ContentFieldDefinition sentimentDef =
    new ContentFieldDefinition();
sentimentDef.setType(ContentFieldType.STRING);
sentimentDef.setMethod(
    GenerationMethod.CLASSIFY);
sentimentDef.setDescription(
    "Overall sentiment of the call");
sentimentDef.setEnumProperty(
    Arrays.asList(
        "Positive", "Neutral", "Negative"));
fields.put("Sentiment", sentimentDef);

// Define "People" as an array of objects
Map<String, ContentFieldDefinition> personProps =
    new HashMap<>();
ContentFieldDefinition nameDef =
    new ContentFieldDefinition();
nameDef.setType(ContentFieldType.STRING);
personProps.put("Name", nameDef);
ContentFieldDefinition roleDef =
    new ContentFieldDefinition();
roleDef.setType(ContentFieldType.STRING);
personProps.put("Role", roleDef);

ContentFieldDefinition personItemDef =
    new ContentFieldDefinition();
personItemDef.setType(ContentFieldType.OBJECT);
personItemDef.setProperties(personProps);

ContentFieldDefinition peopleDef =
    new ContentFieldDefinition();
peopleDef.setType(ContentFieldType.ARRAY);
peopleDef.setDescription(
    "List of people mentioned");
peopleDef.setItemDefinition(personItemDef);
fields.put("People", peopleDef);

ContentFieldSchema fieldSchema =
    new ContentFieldSchema();
fieldSchema.setName("call_center_schema");
fieldSchema.setDescription(
    "Schema for analyzing customer"
    + " support calls");
fieldSchema.setFields(fields);

Map<String, String> models = new HashMap<>();
models.put("completion", "gpt-4.1");

ContentAnalyzer customAnalyzer =
    new ContentAnalyzer()
        .setBaseAnalyzerId("prebuilt-audio")
        .setDescription(
            "Custom analyzer for customer"
            + " support calls")
        .setConfig(new ContentAnalyzerConfig()
            .setLocales(
                Arrays.asList("en-US", "fr-FR"))
            .setReturnDetails(true))
        .setFieldSchema(fieldSchema)
        .setModels(models);

SyncPoller<ContentAnalyzerOperationStatus,
    ContentAnalyzer> operation =
    client.beginCreateAnalyzer(
        analyzerId, customAnalyzer, true);

ContentAnalyzer result =
    operation.getFinalResult();
System.out.println(
    "Analyzer '" + analyzerId
    + "' created successfully!");

if (result.getDescription() != null) {
    System.out.println(
        "  Description: "
        + result.getDescription());
}

if (result.getFieldSchema() != null
    && result.getFieldSchema()
        .getFields() != null) {
    System.out.println(
        "  Fields ("
        + result.getFieldSchema()
            .getFields().size() + "):");
    result.getFieldSchema().getFields()
        .forEach((fieldName, fieldDef) -> {
            String method =
                fieldDef.getMethod() != null
                    ? fieldDef.getMethod()
                        .toString()
                    : "auto";
            String type =
                fieldDef.getType() != null
                    ? fieldDef.getType()
                        .toString()
                    : "unknown";
            System.out.println(
                "    - " + fieldName
                + ": " + type
                + " (" + method + ")");
        });
}
```

An example output looks like:

```text
Analyzer 'my_audio_analyzer_ID' created successfully!
  Description: Custom analyzer for customer support calls
  Fields (3):
    - People: array (auto)
    - Summary: string (generate)
    - Sentiment: string (classify)
```

> [!TIP]
> This code adapts the [CreateAnalyzer](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/contentunderstanding/azure-ai-contentunderstanding/src/samples/java/com/azure/ai/contentunderstanding/samples/Sample04_CreateAnalyzer.java) pattern for audio content.

# [Video](#tab/video)

The following example creates a custom video analyzer based on the [prebuilt video analyzer](../../concepts/prebuilt-analyzers.md) for processing product demos and reviews.

```java
String analyzerId =
    "my_video_analyzer_"
    + System.currentTimeMillis();

// Define segment properties
Map<String, ContentFieldDefinition> segProps =
    new HashMap<>();
ContentFieldDefinition segIdDef =
    new ContentFieldDefinition();
segIdDef.setType(ContentFieldType.STRING);
segProps.put("SegmentId", segIdDef);

ContentFieldDefinition descDef =
    new ContentFieldDefinition();
descDef.setType(ContentFieldType.STRING);
descDef.setMethod(GenerationMethod.GENERATE);
descDef.setDescription(
    "Detailed summary of the video segment");
segProps.put("Description", descDef);

ContentFieldDefinition sentDef =
    new ContentFieldDefinition();
sentDef.setType(ContentFieldType.STRING);
sentDef.setMethod(GenerationMethod.CLASSIFY);
sentDef.setEnumProperty(
    Arrays.asList(
        "Positive", "Neutral", "Negative"));
segProps.put("Sentiment", sentDef);

ContentFieldDefinition segItemDef =
    new ContentFieldDefinition();
segItemDef.setType(ContentFieldType.OBJECT);
segItemDef.setProperties(segProps);

Map<String, ContentFieldDefinition> fields =
    new HashMap<>();
ContentFieldDefinition segmentsDef =
    new ContentFieldDefinition();
segmentsDef.setType(ContentFieldType.ARRAY);
segmentsDef.setItemDefinition(segItemDef);
fields.put("Segments", segmentsDef);

ContentFieldSchema fieldSchema =
    new ContentFieldSchema();
fieldSchema.setName("video_schema");
fieldSchema.setDescription(
    "Schema for analyzing product demo videos");
fieldSchema.setFields(fields);

Map<String, String> models = new HashMap<>();
models.put("completion", "gpt-4.1");

ContentAnalyzer customAnalyzer =
    new ContentAnalyzer()
        .setBaseAnalyzerId("prebuilt-video")
        .setDescription(
            "Custom analyzer for product"
            + " demo videos")
        .setConfig(new ContentAnalyzerConfig()
            .setLocales(
                Arrays.asList("en-US", "fr-FR"))
            .setReturnDetails(true))
        .setFieldSchema(fieldSchema)
        .setModels(models);

SyncPoller<ContentAnalyzerOperationStatus,
    ContentAnalyzer> operation =
    client.beginCreateAnalyzer(
        analyzerId, customAnalyzer, true);

ContentAnalyzer result =
    operation.getFinalResult();
System.out.println(
    "Analyzer '" + analyzerId
    + "' created successfully!");

if (result.getDescription() != null) {
    System.out.println(
        "  Description: "
        + result.getDescription());
}

if (result.getFieldSchema() != null
    && result.getFieldSchema()
        .getFields() != null) {
    System.out.println(
        "  Fields ("
        + result.getFieldSchema()
            .getFields().size() + "):");
    result.getFieldSchema().getFields()
        .forEach((fieldName, fieldDef) -> {
            String method =
                fieldDef.getMethod() != null
                    ? fieldDef.getMethod()
                        .toString()
                    : "auto";
            String type =
                fieldDef.getType() != null
                    ? fieldDef.getType()
                        .toString()
                    : "unknown";
            System.out.println(
                "    - " + fieldName
                + ": " + type
                + " (" + method + ")");
        });
}
```

An example output looks like:

```text
Analyzer 'my_video_analyzer_ID' created successfully!
  Description: Custom analyzer for product demo videos
  Fields (1):
    - Segments: array (auto)
```

> [!TIP]
> This code adapts the [CreateAnalyzer](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/contentunderstanding/azure-ai-contentunderstanding/src/samples/java/com/azure/ai/contentunderstanding/samples/Sample04_CreateAnalyzer.java) pattern for video content.

---

## Use the custom analyzer

# [Document](#tab/document)

After creating the analyzer, use it to analyze a document and extract the custom fields. Delete the analyzer when you no longer need it.

```java
String documentUrl =
    "https://raw.githubusercontent.com/"
    + "Azure-Samples/"
    + "azure-ai-content-understanding-assets/"
    + "main/document/invoice.pdf";

AnalysisInput input = new AnalysisInput();
input.setUrl(documentUrl);

SyncPoller<ContentAnalyzerAnalyzeOperationStatus,
    AnalysisResult> analyzeOperation =
    client.beginAnalyze(
        analyzerId, Arrays.asList(input));

AnalysisResult analyzeResult =
    analyzeOperation.getFinalResult();

if (analyzeResult.getContents() != null
    && !analyzeResult.getContents().isEmpty()
    && analyzeResult.getContents().get(0)
        instanceof DocumentContent) {
    DocumentContent content =
        (DocumentContent) analyzeResult
            .getContents().get(0);

    ContentField companyField =
        content.getFields() != null
            ? content.getFields()
                .get("company_name") : null;
    if (companyField
        instanceof ContentStringField) {
        ContentStringField sf =
            (ContentStringField) companyField;
        System.out.println(
            "Company Name: " + sf.getValue());
        System.out.println(
            "  Confidence: "
            + companyField.getConfidence());
    }

    ContentField totalField =
        content.getFields() != null
            ? content.getFields()
                .get("total_amount") : null;
    if (totalField != null) {
        System.out.println(
            "Total Amount: "
            + totalField.getValue());
    }

    ContentField summaryField =
        content.getFields() != null
            ? content.getFields()
                .get("document_summary") : null;
    if (summaryField
        instanceof ContentStringField) {
        ContentStringField sf =
            (ContentStringField) summaryField;
        System.out.println(
            "Summary: " + sf.getValue());
    }

    ContentField typeField =
        content.getFields() != null
            ? content.getFields()
                .get("document_type") : null;
    if (typeField
        instanceof ContentStringField) {
        ContentStringField sf =
            (ContentStringField) typeField;
        System.out.println(
            "Document Type: " + sf.getValue());
    }
}

// --- Clean up ---
System.out.println(
    "\nCleaning up: deleting analyzer '"
    + analyzerId + "'...");
client.deleteAnalyzer(analyzerId);
System.out.println(
    "Analyzer '" + analyzerId
    + "' deleted successfully.");
```

An example output looks like:

```text
Company Name: CONTOSO LTD.
  Confidence: 0.781
Total Amount: 610.0
Summary: This document is an invoice from CONTOSO LTD. to Microsoft Corporation for consulting services, document fees, and printing fees, detailing service dates, itemized charges, taxes, and the total amount due.
Document Type: invoice

Cleaning up: deleting analyzer 'my_document_analyzer_ID'...
Analyzer 'my_document_analyzer_ID' deleted successfully.
```

> [!TIP]
> Check out more examples of running analyzers at [Java SDK samples](https://github.com/Azure/azure-sdk-for-java/tree/main/sdk/contentunderstanding/azure-ai-contentunderstanding/src/samples/java/com/azure/ai/contentunderstanding).

# [Image](#tab/image)

After creating the analyzer, use it to analyze an image and extract the custom fields. Delete the analyzer when you no longer need it.

```java
String imageUrl =
    "https://raw.githubusercontent.com/"
    + "Azure-Samples/"
    + "azure-ai-content-understanding-assets/"
    + "main/image/pieChart.jpg";

AnalysisInput input = new AnalysisInput();
input.setUrl(imageUrl);

SyncPoller<ContentAnalyzerAnalyzeOperationStatus,
    AnalysisResult> analyzeOperation =
    client.beginAnalyze(
        analyzerId, Arrays.asList(input));

AnalysisResult analyzeResult =
    analyzeOperation.getFinalResult();

if (analyzeResult.getContents() != null
    && !analyzeResult.getContents().isEmpty()) {
    var content =
        analyzeResult.getContents().get(0);

    if (content.getFields() != null) {
        ContentField titleField =
            content.getFields().get("Title");
        if (titleField
            instanceof ContentStringField) {
            System.out.println(
                "Title: "
                + ((ContentStringField) titleField)
                    .getValue());
        }

        ContentField chartField =
            content.getFields().get("ChartType");
        if (chartField
            instanceof ContentStringField) {
            System.out.println(
                "Chart Type: "
                + ((ContentStringField) chartField)
                    .getValue());
        }
    }
}

// --- Clean up ---
System.out.println(
    "\nCleaning up: deleting analyzer '"
    + analyzerId + "'...");
client.deleteAnalyzer(analyzerId);
System.out.println(
    "Analyzer '" + analyzerId
    + "' deleted successfully.");
```

An example output looks like:

```text
Title: Weekly Working Hours Distribution
Chart Type: pie

Cleaning up: deleting analyzer 'my_image_analyzer_ID'...
Analyzer 'my_image_analyzer_ID' deleted successfully.
```

> [!TIP]
> Check out more examples of running analyzers at [Java SDK samples](https://github.com/Azure/azure-sdk-for-java/tree/main/sdk/contentunderstanding/azure-ai-contentunderstanding/src/samples/java/com/azure/ai/contentunderstanding).

# [Audio](#tab/audio)

After creating the analyzer, use it to analyze an audio file and extract the custom fields. Delete the analyzer when you no longer need it.

```java
String audioUrl =
    "https://raw.githubusercontent.com/"
    + "Azure-Samples/"
    + "azure-ai-content-understanding-assets/"
    + "main/audio/callCenterRecording.mp3";

AnalysisInput input = new AnalysisInput();
input.setUrl(audioUrl);

SyncPoller<ContentAnalyzerAnalyzeOperationStatus,
    AnalysisResult> analyzeOperation =
    client.beginAnalyze(
        analyzerId, Arrays.asList(input));

AnalysisResult analyzeResult =
    analyzeOperation.getFinalResult();

if (analyzeResult.getContents() != null
    && !analyzeResult.getContents().isEmpty()) {
    var content =
        analyzeResult.getContents().get(0);

    if (content.getFields() != null) {
        ContentField summaryField =
            content.getFields().get("Summary");
        if (summaryField
            instanceof ContentStringField) {
            System.out.println(
                "Summary: "
                + ((ContentStringField)
                    summaryField)
                    .getValue());
        }

        ContentField sentField =
            content.getFields().get("Sentiment");
        if (sentField
            instanceof ContentStringField) {
            System.out.println(
                "Sentiment: "
                + ((ContentStringField) sentField)
                    .getValue());
        }
    }
}

// --- Clean up ---
System.out.println(
    "\nCleaning up: deleting analyzer '"
    + analyzerId + "'...");
client.deleteAnalyzer(analyzerId);
System.out.println(
    "Analyzer '" + analyzerId
    + "' deleted successfully.");
```

An example output looks like:

```text
Summary: Maria Smith contacted Contoso to inquire about her current point balance. John Doe, the customer service representative, confirmed her identity by requesting her date of birth and provided her point balance. The conversation ended politely with no further requests.
Sentiment: Positive

Cleaning up: deleting analyzer 'my_audio_analyzer_ID'...
Analyzer 'my_audio_analyzer_ID' deleted successfully.
```

> [!TIP]
> Check out more examples of running analyzers at [Java SDK samples](https://github.com/Azure/azure-sdk-for-java/tree/main/sdk/contentunderstanding/azure-ai-contentunderstanding/src/samples/java/com/azure/ai/contentunderstanding).

# [Video](#tab/video)

After creating the analyzer, use it to analyze a video and extract the custom fields. Delete the analyzer when you no longer need it.

```java
String videoUrl =
    "https://raw.githubusercontent.com/"
    + "Azure-Samples/"
    + "azure-ai-content-understanding-assets/"
    + "main/videos/sdk_samples/"
    + "FlightSimulator.mp4";

AnalysisInput input = new AnalysisInput();
input.setUrl(videoUrl);

SyncPoller<ContentAnalyzerAnalyzeOperationStatus,
    AnalysisResult> analyzeOperation =
    client.beginAnalyze(
        analyzerId, Arrays.asList(input));

AnalysisResult analyzeResult =
    analyzeOperation.getFinalResult();

if (analyzeResult.getContents() != null
    && !analyzeResult.getContents().isEmpty()) {
    var content =
        analyzeResult.getContents().get(0);
    System.out.println(
        "Content kind: " + content.getKind());
    if (content.getFields() != null) {
        ContentField segmentsField =
            content.getFields().get("Segments");
        if (segmentsField
            instanceof ContentArrayField) {
            ContentArrayField segments =
                (ContentArrayField) segmentsField;
            System.out.println(
                "Segments (" + segments.size()
                + "):");
            for (int i = 0;
                i < segments.size(); i++) {
                ContentField seg = segments.get(i);
                if (seg instanceof
                    ContentObjectField) {
                    ContentObjectField obj =
                        (ContentObjectField) seg;
                    ContentField idField =
                        obj.getFieldOrDefault(
                            "SegmentId");
                    ContentField descField =
                        obj.getFieldOrDefault(
                            "Description");
                    ContentField sentField =
                        obj.getFieldOrDefault(
                            "Sentiment");
                    String segId = idField != null
                        ? String.valueOf(
                            idField.getValue())
                        : "N/A";
                    String desc = descField != null
                        ? String.valueOf(
                            descField.getValue())
                        : "N/A";
                    String sent = sentField != null
                        ? String.valueOf(
                            sentField.getValue())
                        : "N/A";
                    System.out.println(
                        "  Segment " + segId
                        + ": " + desc
                        + " (Sentiment: "
                        + sent + ")");
                }
            }
        }
    }
}

// --- Clean up ---
System.out.println(
    "\nCleaning up: deleting analyzer '"
    + analyzerId + "'...");
client.deleteAnalyzer(analyzerId);
System.out.println(
    "Analyzer '" + analyzerId
    + "' deleted successfully.");
```

An example output looks like:

```text
Content kind: audioVisual
Segments (16):
  Segment 00:00:00.000-00:00:01.467: The video opens with a scenic aerial view of an island, featuring a small aircraft flying above the landscape. The screen displays the logos for 'Flight Simulator' and 'Microsoft Azure AI,' indicating a collaboration or integration between the two products. (Sentiment: Positive)
  Segment 00:00:01.467-00:00:03.233: A man is shown in an interview setting, sitting in a modern office environment. The transcript begins discussing neural TTS (Text-to-Speech) and the importance of good data for achieving a high-quality voice. (Sentiment: Neutral)
  Segment 00:00:03.233-00:00:07.367: The visuals shift to a digital audio waveform, emphasizing the technical aspect of TTS. The transcript explains that a universal TTS model was built using 3,000 hours of data, highlighting the scale and quality of the dataset. (Sentiment: Positive)
  Segment 00:00:07.367-00:00:08.200: Another man appears in an interview setting, continuing the discussion about the accumulation of data for the universal TTS model. The transcript notes that the model captures audio nuances for more natural voice generation. (Sentiment: Positive)
  Segment 00:00:08.200-00:00:11.367: The video transitions to an outdoor scene showing a large facility, likely a data center, set in a rural landscape. This visually supports the scale of infrastructure required for the TTS model. (Sentiment: Neutral)
  Segment 00:00:11.367-00:00:13.567: Inside a data center, rows of servers are shown, reinforcing the technological backbone of the TTS system. The transcript continues to emphasize the accumulation of data and the model's capabilities. (Sentiment: Neutral)
  Segment 00:00:13.567-00:00:16.100: The interview returns to the first man, who elaborates on the universal model's ability to generate natural voices. The transcript mentions the model's ability to capture nuances, supporting the visuals. (Sentiment: Positive)
  Segment 00:00:16.100-00:00:19.433: A biplane is seen flying over a coastal landscape, visually connecting the Flight Simulator experience to the advanced AI voice technology discussed earlier. (Sentiment: Positive)
  Segment 00:00:19.433-00:00:23.967: A scenic view of a castle with a plane flying overhead, further showcasing the immersive environments possible in Flight Simulator. The transcript highlights the naturalness of the generated voices. (Sentiment: Positive)
  Segment 00:00:23.967-00:00:30.033: A bald man is interviewed in a modern office setting. The transcript discusses the high fidelity of cognitive services offerings, noting that the voices sound much more like actual human voices. (Sentiment: Positive)
  Segment 00:00:30.033-00:00:33.200: The interview with the bald man continues, reinforcing the message about the realism and fidelity of the AI-generated voices. (Sentiment: Positive)
  Segment 00:00:33.200-00:00:35.267: The video shows an overhead view of an airplane on the tarmac, possibly preparing for pushback. The transcript transitions to a simulated ATC (Air Traffic Control) exchange, demonstrating the practical application of TTS in Flight Simulator. (Sentiment: Neutral)
  Segment 00:00:35.267-00:00:37.700: A ground crew member directs an Airbus aircraft, visually representing the realism and immersion of Flight Simulator. The transcript includes ATC communication, showing the integration of natural-sounding AI voices. (Sentiment: Positive)
  Segment 00:00:37.700-00:00:39.200: Ground crew members are seen walking on the tarmac near aircraft, continuing the realistic airport environment. The transcript features further ATC communication. (Sentiment: Neutral)
  Segment 00:00:39.200-00:00:42.033: A close-up of an Airbus aircraft at the gate, reinforcing the realism and detail in Flight Simulator. The transcript continues with ATC exchanges, demonstrating the natural voice output. (Sentiment: Positive)
  Segment 00:00:42.033-00:00:43.866: The video ends with the Microsoft logo and branding, signifying the conclusion of the demo and reinforcing the partnership between Flight Simulator and Microsoft Azure AI. (Sentiment: Positive)

Cleaning up: deleting analyzer 'my_video_analyzer_ID'...
Analyzer 'my_video_analyzer_ID' deleted successfully.
```

> [!TIP]
> Check out more examples of running analyzers at [Java SDK samples](https://github.com/Azure/azure-sdk-for-java/tree/main/sdk/contentunderstanding/azure-ai-contentunderstanding/src/samples/java/com/azure/ai/contentunderstanding).

---



