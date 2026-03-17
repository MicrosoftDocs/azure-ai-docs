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
        <version>1.0.0-beta.1</version>
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
models.put("embedding", "text-embedding-3-large");

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
```

> [!TIP]
> This code is based on the [Sample04_CreateAnalyzer.java](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/contentunderstanding/azure-ai-contentunderstanding/src/samples/java/com/azure/ai/contentunderstanding/samples/Sample04_CreateAnalyzer.java) sample in the SDK repository.

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
            "Custom analyzer for charts and graphs")
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
```

> [!TIP]
> This code adapts the [Sample04_CreateAnalyzer.java](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/contentunderstanding/azure-ai-contentunderstanding/src/samples/java/com/azure/ai/contentunderstanding/samples/Sample04_CreateAnalyzer.java) pattern for image content.

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
peopleDef.setItems(personItemDef);
fields.put("People", peopleDef);

ContentFieldSchema fieldSchema =
    new ContentFieldSchema();
fieldSchema.setName("call_center_schema");
fieldSchema.setDescription(
    "Schema for analyzing customer support calls");
fieldSchema.setFields(fields);

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
        .setFieldSchema(fieldSchema);

SyncPoller<ContentAnalyzerOperationStatus,
    ContentAnalyzer> operation =
    client.beginCreateAnalyzer(
        analyzerId, customAnalyzer, true);

ContentAnalyzer result =
    operation.getFinalResult();
System.out.println(
    "Analyzer '" + analyzerId
    + "' created successfully!");
```

> [!TIP]
> This code adapts the [Sample04_CreateAnalyzer.java](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/contentunderstanding/azure-ai-contentunderstanding/src/samples/java/com/azure/ai/contentunderstanding/samples/Sample04_CreateAnalyzer.java) pattern for audio content.

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
segmentsDef.setItems(segItemDef);
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
            .setReturnDetails(true)
            .setSegmentationMode("auto"))
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
```

> [!TIP]
> This code adapts the [Sample04_CreateAnalyzer.java](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/contentunderstanding/azure-ai-contentunderstanding/src/samples/java/com/azure/ai/contentunderstanding/samples/Sample04_CreateAnalyzer.java) pattern for video content.

---

## Use the custom analyzer

# [Document](#tab/document)

After creating the analyzer, use it to analyze a document and extract the custom fields.

```java
String documentUrl =
    "https://raw.githubusercontent.com/"
    + "Azure-Samples/"
    + "azure-ai-content-understanding-python/"
    + "main/data/receipt.png";

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
```

> [!TIP]
> This code adapts the [Sample04_CreateAnalyzer.java](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/contentunderstanding/azure-ai-contentunderstanding/src/samples/java/com/azure/ai/contentunderstanding/samples/Sample04_CreateAnalyzer.java) pattern for document content.

# [Image](#tab/image)

After creating the analyzer, use it to analyze an image and extract the custom fields.

```java
String imageUrl =
    "https://raw.githubusercontent.com/"
    + "Azure-Samples/"
    + "azure-ai-content-understanding-python/"
    + "main/data/pieChart.jpg";

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
```

> [!TIP]
> This code adapts the [Sample04_CreateAnalyzer.java](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/contentunderstanding/azure-ai-contentunderstanding/src/samples/java/com/azure/ai/contentunderstanding/samples/Sample04_CreateAnalyzer.java) pattern for image content.

# [Audio](#tab/audio)

After creating the analyzer, use it to analyze an audio file and extract the custom fields.

```java
String audioUrl =
    "https://raw.githubusercontent.com/"
    + "Azure-Samples/"
    + "azure-ai-content-understanding-python/"
    + "main/data/audio.wav";

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
                + ((ContentStringField) summaryField)
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
```

> [!TIP]
> This code adapts the [Sample04_CreateAnalyzer.java](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/contentunderstanding/azure-ai-contentunderstanding/src/samples/java/com/azure/ai/contentunderstanding/samples/Sample04_CreateAnalyzer.java) pattern for audio content.

# [Video](#tab/video)

After creating the analyzer, use it to analyze a video and extract the custom fields.

```java
String videoUrl =
    "https://raw.githubusercontent.com/"
    + "Azure-Samples/"
    + "azure-ai-content-understanding-python/"
    + "main/data/FlightSimulator.mp4";

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
        if (segmentsField != null) {
            System.out.println(
                "Segments: " + segmentsField);
        }
    }
}
```

> [!TIP]
> This code adapts the [Sample04_CreateAnalyzer.java](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/contentunderstanding/azure-ai-contentunderstanding/src/samples/java/com/azure/ai/contentunderstanding/samples/Sample04_CreateAnalyzer.java) pattern for video content.

---

## Clean up resources

Delete the analyzer when you no longer need it.

```java
client.deleteAnalyzer(analyzerId);
System.out.println(
    "Analyzer '" + analyzerId
    + "' deleted successfully.");
```

> [!NOTE]
> The document example is based on the [Sample04_CreateAnalyzer.java](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/contentunderstanding/azure-ai-contentunderstanding/src/samples/java/com/azure/ai/contentunderstanding/samples/Sample04_CreateAnalyzer.java) sample. Custom analyzers support the same field schema concepts across all content types. For the complete set of samples, see [Java SDK samples](https://github.com/Azure/azure-sdk-for-java/tree/main/sdk/contentunderstanding/azure-ai-contentunderstanding/src/samples/java/com/azure/ai/contentunderstanding).