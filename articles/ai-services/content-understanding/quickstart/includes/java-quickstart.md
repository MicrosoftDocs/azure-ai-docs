---
title: "Quickstart: Use the Content Understanding Java SDK"
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-content-understanding
ms.topic: include
ms.date: 03/06/2026
ms.author: lahlouchu
ai-usage: ai-assisted
---

<!-- markdownlint-disable MD025 -->

[Client library](https://central.sonatype.com/artifact/com.azure/azure-ai-contentunderstanding) | [Samples](https://github.com/Azure/azure-sdk-for-java/tree/main/sdk/contentunderstanding/azure-ai-contentunderstanding/src/samples/java/com/azure/ai/contentunderstanding) | [SDK source](https://github.com/Azure/azure-sdk-for-java/tree/main/sdk/contentunderstanding/azure-ai-contentunderstanding)

This quickstart shows you how to use the Content Understanding Java SDK to extract structured data using prebuilt analyzers from document, image, audio, and video files. To learn more about prebuilt analyzers and other features, see the documentation of [Prebuilt Analyzers](../../concepts/prebuilt-analyzers.md).

## Prerequisites

* An active Azure subscription. If you don't have an Azure account, [create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
* A [Microsoft Foundry resource](https://portal.azure.com/#create/Microsoft.CognitiveServicesAIFoundry) created in a [supported region](https://learn.microsoft.com/en-us/azure/ai-services/content-understanding/language-region-support).
* Your resource endpoint and API key (found under Keys and Endpoint in the Azure portal).
* Model deployment defaults configured for your resource. See [Models and deployments](../../concepts/models-deployments.md) or this one-time [configuration script](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/contentunderstanding/azure-ai-contentunderstanding/src/samples/java/com/azure/ai/contentunderstanding/samples/Sample00_UpdateDefaults.java) for setup instructions.
* [Java Development Kit (JDK)](https://learn.microsoft.com/java/openjdk/download) version 8 or later.
* [Apache Maven](https://maven.apache.org/download.cgi).

## Set up

1. Create a new Maven project:

    ```console
    mvn archetype:generate -DgroupId=com.example \
        -DartifactId=content-understanding-quickstart \
        -DarchetypeArtifactId=maven-archetype-quickstart \
        -DinteractiveMode=false
    cd content-understanding-quickstart
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


# [Windows](#tab/windows)

```cmd
setx CONTENTUNDERSTANDING_ENDPOINT "your-endpoint"
setx CONTENTUNDERSTANDING_KEY "your-key"
```

# [Linux / macOS](#tab/linux)

```bash
export CONTENTUNDERSTANDING_ENDPOINT="your-endpoint"
export CONTENTUNDERSTANDING_KEY="your-key"
```

## Create a client

The `ContentUnderstandingClient` is the main entry point for interacting with the service. Create an instance by providing your endpoint and credential.

```java
import com.azure.core.credential.AzureKeyCredential;
import com.azure.ai.contentunderstanding.ContentUnderstandingClient;
import com.azure.ai.contentunderstanding.ContentUnderstandingClientBuilder;

String endpoint = System.getenv("CONTENTUNDERSTANDING_ENDPOINT");
String key = System.getenv("CONTENTUNDERSTANDING_KEY");

ContentUnderstandingClient client =
    new ContentUnderstandingClientBuilder()
        .endpoint(endpoint)
        .credential(new AzureKeyCredential(key))
        .buildClient();
```

## Get started with a prebuilt analyzer

Analyzers define how your content is processed and the insights that are extracted. We offer [prebuilt analyzers](../../concepts/prebuilt-analyzers.md) for common use cases. You can [customize prebuilt analyzers](../../concepts/prebuilt-analyzers.md) to better fit your specific needs and use cases.
This quickstart uses prebuilt invoice, image, audio, and video analyzers to help you get started.


# [Document](#tab/document)

This example uses the `prebuilt-invoice` analyzer to extract structured data from an invoice document.

```java
import java.util.Arrays;
import com.azure.core.credential.AzureKeyCredential;
import com.azure.core.util.polling.SyncPoller;
import com.azure.ai.contentunderstanding.ContentUnderstandingClient;
import com.azure.ai.contentunderstanding.ContentUnderstandingClientBuilder;
import com.azure.ai.contentunderstanding.models.*;

public class test_document {

    public static void main(String[] args) {
        String endpoint = System.getenv("CONTENTUNDERSTANDING_ENDPOINT");
        String key = System.getenv("CONTENTUNDERSTANDING_KEY");

        ContentUnderstandingClient client =
            new ContentUnderstandingClientBuilder()
                .endpoint(endpoint)
                .credential(new AzureKeyCredential(key))
                .buildClient();

        // Sample invoice
        String invoiceUrl =
            "https://raw.githubusercontent.com/"
            + "Azure-Samples/"
            + "azure-ai-content-understanding-assets/"
            + "main/document/invoice.pdf";

        AnalysisInput input = new AnalysisInput();
        input.setUrl(invoiceUrl);

        SyncPoller<ContentAnalyzerAnalyzeOperationStatus, AnalysisResult> poller =
            client.beginAnalyze(
                "prebuilt-invoice",
                Arrays.asList(input)
            );
        AnalysisResult result = poller.getFinalResult();

        if (result.getContents() == null
            || result.getContents().isEmpty()) {
            System.out.println(
                "No content found in the analysis result."
            );
            return;
        }

        // Get the document content
        var content = result.getContents().get(0);
        if (content instanceof DocumentContent) {
            DocumentContent documentContent =
                (DocumentContent) content;

            System.out.printf(
                "Document unit: %s%n",
                documentContent.getUnit() != null
                    ? documentContent.getUnit()
                    : "unknown"
            );
            System.out.printf(
                "Pages: %d to %d%n",
                documentContent.getStartPageNumber(),
                documentContent.getEndPageNumber()
            );

            if (documentContent.getFields() == null) {
                System.out.println("No fields found.");
                return;
            }

            // Extract simple string fields
            var customerNameField =
                documentContent.getFields()
                    .get("CustomerName");
            if (customerNameField != null) {
                System.out.printf(
                    "Customer Name: %s%n",
                    customerNameField.getValue()
                );
                if (customerNameField.getConfidence() != null) {
                    System.out.printf(
                        "  Confidence: %.2f%n",
                        customerNameField.getConfidence()
                    );
                }
            }

            // Extract date fields
            var invoiceDateField =
                documentContent.getFields()
                    .get("InvoiceDate");
            if (invoiceDateField != null) {
                System.out.printf(
                    "Invoice Date: %s%n",
                    invoiceDateField.getValue()
                );
                if (invoiceDateField.getConfidence() != null) {
                    System.out.printf(
                        "  Confidence: %.2f%n",
                        invoiceDateField.getConfidence()
                    );
                }
            }

            // Extract object fields (nested structures)
            var totalAmountField =
                documentContent.getFields()
                    .get("TotalAmount");
            if (totalAmountField
                instanceof ContentObjectField) {

                ContentObjectField totalAmountObj =
                    (ContentObjectField) totalAmountField;

                if (totalAmountObj.getValue() != null) {
                    var amountField = totalAmountObj
                        .getValue().get("Amount");
                    var currencyField = totalAmountObj
                        .getValue().get("CurrencyCode");

                    String amount = amountField != null
                        && amountField.getValue() != null
                            ? amountField.getValue().toString()
                            : "(None)";
                    String currency =
                        currencyField != null
                        && currencyField.getValue() != null
                            ? currencyField.getValue().toString()
                            : "";

                    System.out.printf(
                        "%nTotal: %s%s%n",
                        currency, amount
                    );
                }
            }

            // Extract array fields (line items)
            var lineItemsField =
                documentContent.getFields()
                    .get("LineItems");
            if (lineItemsField
                instanceof ContentArrayField) {

                ContentArrayField lineItemsArr =
                    (ContentArrayField) lineItemsField;

                if (lineItemsArr.getValue() != null
                    && !lineItemsArr.getValue().isEmpty()) {

                    System.out.printf(
                        "%nLine Items (%d):%n",
                        lineItemsArr.getValue().size()
                    );

                    for (int i = 0;
                        i < lineItemsArr.getValue().size();
                        i++) {

                        var item =
                            lineItemsArr.getValue().get(i);
                        if (item
                            instanceof ContentObjectField) {

                            ContentObjectField itemObj =
                                (ContentObjectField) item;

                            if (itemObj.getValue() != null) {
                                var descField = itemObj
                                    .getValue().get("Description");
                                var qtyField = itemObj
                                    .getValue().get("Quantity");

                                String description =
                                    descField != null
                                    && descField.getValue()
                                        != null
                                        ? descField.getValue()
                                            .toString()
                                        : "N/A";
                                String quantity =
                                    qtyField != null
                                    && qtyField.getValue()
                                        != null
                                        ? qtyField.getValue()
                                            .toString()
                                        : "N/A";

                                System.out.printf(
                                    "  Item %d: %s%n",
                                    i + 1, description
                                );
                                System.out.printf(
                                    "    Quantity: %s%n",
                                    quantity
                                );
                            }
                        }
                    }
                }
            }
        }
    }
}
```

This will produce the following output:
```text
Document unit: inch
Pages: 1 to 1
Customer Name: MICROSOFT CORPORATION
  Confidence: 0.47
Invoice Date: 2019-11-15
  Confidence: 0.94

Total: USD110.0

Line Items (3):
  Item 1: Consulting Services
    Quantity: 2.0
  Item 2: Document Fee
    Quantity: 3.0
  Item 3: Printing Fee
    Quantity: 10.0
```

> [!NOTE]
> This code is based on the [Sample03_AnalyzeInvoice](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/contentunderstanding/azure-ai-contentunderstanding/src/samples/java/com/azure/ai/contentunderstanding/samples/Sample03_AnalyzeInvoice.java) sample in the SDK repository.

# [Image](#tab/image)

This example uses the `prebuilt-imageSearch` analyzer to generate a description of the image.

```java
import java.util.Arrays;
import com.azure.core.credential.AzureKeyCredential;
import com.azure.core.util.polling.SyncPoller;
import com.azure.ai.contentunderstanding.ContentUnderstandingClient;
import com.azure.ai.contentunderstanding.ContentUnderstandingClientBuilder;
import com.azure.ai.contentunderstanding.models.*;

public class test_image {

    public static void main(String[] args) {
        String endpoint = System.getenv("CONTENTUNDERSTANDING_ENDPOINT");
        String key = System.getenv("CONTENTUNDERSTANDING_KEY");

        ContentUnderstandingClient client =
            new ContentUnderstandingClientBuilder()
                .endpoint(endpoint)
                .credential(new AzureKeyCredential(key))
                .buildClient();

        AnalysisInput input = new AnalysisInput();
        input.setUrl(
            "https://raw.githubusercontent.com/"
            + "Azure-Samples/"
            + "azure-ai-content-understanding-assets/"
            + "main/image/pieChart.jpg"
        );

        SyncPoller<ContentAnalyzerAnalyzeOperationStatus, AnalysisResult> operation =
            client.beginAnalyze(
                "prebuilt-imageSearch",
                Arrays.asList(input)
            );

        AnalysisResult result = operation.getFinalResult();
        AnalysisContent content = result.getContents().get(0);
        System.out.println(content.getMarkdown());

        String summary = content.getFields() != null
            && content.getFields().containsKey("Summary")
            ? content.getFields().get("Summary")
                .getValue().toString()
            : "";
        System.out.println("Summary: " + summary);
    }
}

```

This will produce an output like the following:
```text
![image](pages/1)

Summary: The pie chart displays the distribution of hours in four categories: 1-39 hours (6.7%), 40-50 hours (18.9%), 50-60 hours (36.6%), and 60+ hours (37.8%). The largest segment is 60+ hours, followed closely by 50-60 hours, then 40-50 hours, and the smallest segment is 1-39 hours.
```
> [!NOTE]
> This code is based on the [Sample02_AnalyzeUrl.java](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/contentunderstanding/azure-ai-contentunderstanding/src/samples/java/com/azure/ai/contentunderstanding/samples/Sample02_AnalyzeUrl.java) sample in the SDK repository.

# [Audio](#tab/audio)

This example uses the `prebuilt-audioSearch` analyzer to extract the audio transcript, generate a summary, and perform speaker labeling.

```java
import java.util.Arrays;
import com.azure.core.credential.AzureKeyCredential;
import com.azure.core.util.polling.SyncPoller;
import com.azure.ai.contentunderstanding.ContentUnderstandingClient;
import com.azure.ai.contentunderstanding.ContentUnderstandingClientBuilder;
import com.azure.ai.contentunderstanding.models.*;

public class test_audio {

    public static void main(String[] args) {
        String endpoint = System.getenv("CONTENTUNDERSTANDING_ENDPOINT");
        String key = System.getenv("CONTENTUNDERSTANDING_KEY");

        ContentUnderstandingClient client =
            new ContentUnderstandingClientBuilder()
                .endpoint(endpoint)
                .credential(new AzureKeyCredential(key))
                .buildClient();

        AnalysisInput input = new AnalysisInput();
        input.setUrl(
            "https://raw.githubusercontent.com/"
            + "Azure-Samples/"
            + "azure-ai-content-understanding-assets/"
            + "main/audio/callCenterRecording.mp3"
        );

        SyncPoller<ContentAnalyzerAnalyzeOperationStatus, AnalysisResult> operation =
            client.beginAnalyze(
                "prebuilt-audioSearch",
                Arrays.asList(input)
            );

        AnalysisResult result = operation.getFinalResult();

        // Cast to AudioVisualContent for audio-specific properties
        AudioVisualContent audioContent =
            (AudioVisualContent) result.getContents().get(0);
        System.out.println(audioContent.getMarkdown());

        String summary = audioContent.getFields() != null
            && audioContent.getFields().containsKey("Summary")
            ? audioContent.getFields().get("Summary")
                .getValue().toString()
            : "";
        System.out.println("Summary: " + summary);

        if (audioContent.getTranscriptPhrases() != null
            && !audioContent.getTranscriptPhrases().isEmpty()) {
            System.out.println("Transcript (first two phrases):");
            int count = 0;
            for (TranscriptPhrase phrase
                : audioContent.getTranscriptPhrases()) {
                if (count >= 2) break;
                System.out.println(
                    "  [" + phrase.getSpeaker() + "] "
                    + phrase.getStartTime().toMillis()
                    + " ms: " + phrase.getText()
                );
                count++;
            }
        }
    }
}

```

This will produce an output like the following:
```text
# Audio: 00:00.000 => 00:32.183

Transcript

WEBVTT

00:00.080 --> 00:00.640
<v Speaker 1>Good day.

00:00.880 --> 00:02.240
<v Speaker 1>Welcome to Contoso.

00:02.560 --> 00:03.760
<v Speaker 1>My name is John Doe.

00:03.920 --> 00:05.120
<v Speaker 1>How can I help you today?

00:05.440 --> 00:06.320
<v Speaker 2>Yes, good day.

00:06.640 --> 00:08.160
<v Speaker 2>My name is Maria Smith.

00:08.560 --> 00:11.360
<v Speaker 2>I would like to inquire about my current point balance.  

00:11.680 --> 00:12.560
<v Speaker 1>No problem.

00:12.880 --> 00:13.920
<v Speaker 1>I am happy to help.

00:14.240 --> 00:16.720
<v Speaker 1>I need your date of birth to confirm your identity.      

00:17.120 --> 00:19.600
<v Speaker 2>It is April 19th, 1988.

00:20.000 --> 00:20.480
<v Speaker 1>Great.

00:20.800 --> 00:24.160
<v Speaker 1>Your current point balance is 599 points.

00:24.560 --> 00:26.160
<v Speaker 1>Do you need any more information?

00:26.480 --> 00:27.200
<v Speaker 2>No, thank you.

00:27.600 --> 00:28.320
<v Speaker 2>That was all.

00:28.720 --> 00:29.360
<v Speaker 2>Goodbye.

00:29.680 --> 00:31.920
<v Speaker 1>You're welcome, goodbye a Cantoso.

Summary: The conversation is a customer service interaction where Maria Smith contacts Contoso to inquire about her current point balance. The agent, John Doe, verifies her identity by asking for her date of birth and then provides her with the information that she has 599 points. The customer confirms that she does not need any further information and ends the call politely.
Transcript (first two phrases):
  [Speaker 1] 80 ms: Good day.
  [Speaker 1] 880 ms: Welcome to Contoso.
```
> [!NOTE]
> This code is based on the [Sample02_AnalyzeUrl.java](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/contentunderstanding/azure-ai-contentunderstanding/src/samples/java/com/azure/ai/contentunderstanding/samples/Sample02_AnalyzeUrl.java) sample in the SDK repository.

# [Video](#tab/video)

This example uses the `prebuilt-videoSearch` analyzer to extract keyframes, transcript, and chapter segments from video.

```java
import java.util.Arrays;
import com.azure.core.credential.AzureKeyCredential;
import com.azure.core.util.polling.SyncPoller;
import com.azure.ai.contentunderstanding.ContentUnderstandingClient;
import com.azure.ai.contentunderstanding.ContentUnderstandingClientBuilder;
import com.azure.ai.contentunderstanding.models.*;

public class test_video {

    public static void main(String[] args) {
        String endpoint = System.getenv("CONTENTUNDERSTANDING_ENDPOINT");
        String key = System.getenv("CONTENTUNDERSTANDING_KEY");

        ContentUnderstandingClient client =
            new ContentUnderstandingClientBuilder()
                .endpoint(endpoint)
                .credential(new AzureKeyCredential(key))
                .buildClient();

        AnalysisInput input = new AnalysisInput();
        input.setUrl(
            "https://raw.githubusercontent.com/"
            + "Azure-Samples/"
            + "azure-ai-content-understanding-assets/"
            + "main/videos/sdk_samples/FlightSimulator.mp4"
        );

        SyncPoller<ContentAnalyzerAnalyzeOperationStatus, AnalysisResult> operation =
            client.beginAnalyze(
                "prebuilt-videoSearch",
                Arrays.asList(input)
            );

        AnalysisResult result = operation.getFinalResult();

        int segmentIndex = 1;
        for (AnalysisContent media : result.getContents()) {
            AudioVisualContent videoContent =
                (AudioVisualContent) media;

            System.out.println("--- Segment " + segmentIndex + " ---");
            System.out.println("Markdown:");
            System.out.println(videoContent.getMarkdown());

            String summary = videoContent.getFields() != null
                && videoContent.getFields().containsKey("Summary")
                ? videoContent.getFields().get("Summary")
                    .getValue().toString()
                : "";
            System.out.println("Summary: " + summary);

            System.out.println(
                "Start: " + videoContent.getStartTime().toMillis()
                + " ms, End: " + videoContent.getEndTime().toMillis()
                + " ms"
            );
            System.out.println(
                "Frame size: " + videoContent.getWidth()
                + " x " + videoContent.getHeight()
            );

            System.out.println("---------------------");
            segmentIndex++;
        }
    }
}

```

This will produce an output like the following:
```text
--- Segment 1 ---
Markdown:
# Video: 00:00.733 => 00:15.467
Width: 1080
Height: 608

Transcript

WEBVTT

00:01.360 --> 00:06.640
<Speaker 1>When it comes to the neural TTS, in order to get a good voice, it's better to have good data.

00:07.120 --> 00:13.320
<Speaker 2>To achieve that, we build a universal TTS model based on 3,000 hours of data.

00:13.440 --> 00:23.680
<Speaker 1>We actually accumulated tons of the data so that this universal model is able to capture the nuance of the audio and generate a more natural voice for the algorithm.


Key Frames
- 00:00.733 ![](keyFrame.733.jpg)
- 00:02.067 ![](keyFrame.2067.jpg)
- 00:02.667 ![](keyFrame.2667.jpg)
- 00:04.067 ![](keyFrame.4067.jpg)
- 00:04.900 ![](keyFrame.4900.jpg)
- 00:05.733 ![](keyFrame.5733.jpg)
- 00:06.567 ![](keyFrame.6567.jpg)
- 00:07.800 ![](keyFrame.7800.jpg)
- 00:09.000 ![](keyFrame.9000.jpg)
- 00:09.800 ![](keyFrame.9800.jpg)
- 00:10.600 ![](keyFrame.10600.jpg)
- 00:12.100 ![](keyFrame.12100.jpg)
- 00:12.833 ![](keyFrame.12833.jpg)
- 00:14.200 ![](keyFrame.14200.jpg)
- 00:14.833 ![](keyFrame.14833.jpg)
- 00:15.467 ![](keyFrame.15467.jpg)
Summary: The video opens with a scenic aerial view of an island and a small plane flying over it, accompanied by the Flight Simulator and Microsoft Azure AI logos. It then transitions to a person speaking about the importance of good data for neural text-to-speech (TTS) technology, mentioning the creation of a universal TTS model trained on 3,000 hours of data to capture audio nuances and generate natural voices. Visuals include audio waveform displays and shots of a data center and server racks, emphasizing the technological infrastructure behind the TTS model.      
Start: 733 ms, End: 15467 ms
Frame size: 1080 x 608
---------------------
--- Segment 2 ---
Markdown:
# Video: 00:15.467 => 00:23.100
Width: 1080
Height: 608



Key Frames
- 00:15.467 ![](keyFrame.15467.jpg)
- 00:16.933 ![](keyFrame.16933.jpg)
- 00:17.767 ![](keyFrame.17767.jpg)
- 00:18.600 ![](keyFrame.18600.jpg)
- 00:20.167 ![](keyFrame.20167.jpg)
- 00:20.900 ![](keyFrame.20900.jpg)
- 00:21.633 ![](keyFrame.21633.jpg)
- 00:22.367 ![](keyFrame.22367.jpg)
- 00:23.100 ![](keyFrame.23100.jpg)
Summary: The video shifts to vibrant in-game footage from Flight Simulator, showcasing detailed landscapes, including a red biplane flying over coastal areas and a castle surrounded by greenery and mountains. This segment visually demonstrates the immersive and realistic environments within the simulator.
Start: 15467 ms, End: 23100 ms
Frame size: 1080 x 608
---------------------
--- Segment 3 ---
Markdown:
# Video: 00:23.100 => 00:43.233
Width: 1080
Height: 608

Transcript

WEBVTT

00:24.040 --> 00:29.120
<Speaker 3>What we liked about cognitive services offerings were that they had a much higher fidelity.

00:29.600 --> 00:32.880
<Speaker 3>And they sounded a lot more like an actual human voice.

00:33.680 --> 00:37.200
<Speaker 4>Orlando ground 9555 requesting the end of pushback.

00:38.680 --> 00:41.280
<Speaker 4>9555 request to end pushback received.


Key Frames
- 00:23.100 ![](keyFrame.23100.jpg)
- 00:24.833 ![](keyFrame.24833.jpg)
- 00:25.700 ![](keyFrame.25700.jpg)
- 00:26.567 ![](keyFrame.26567.jpg)
- 00:27.433 ![](keyFrame.27433.jpg)
- 00:28.300 ![](keyFrame.28300.jpg)
- 00:29.167 ![](keyFrame.29167.jpg)
- 00:30.833 ![](keyFrame.30833.jpg)
- 00:31.633 ![](keyFrame.31633.jpg)
- 00:32.433 ![](keyFrame.32433.jpg)
- 00:33.900 ![](keyFrame.33900.jpg)
- 00:34.600 ![](keyFrame.34600.jpg)
- 00:36.067 ![](keyFrame.36067.jpg)
- 00:36.867 ![](keyFrame.36867.jpg)
- 00:38.200 ![](keyFrame.38200.jpg)
- 00:38.700 ![](keyFrame.38700.jpg)
- 00:39.900 ![](keyFrame.39900.jpg)
- 00:40.600 ![](keyFrame.40600.jpg)
- 00:41.300 ![](keyFrame.41300.jpg)
- 00:42.633 ![](keyFrame.42633.jpg)
- 00:43.233 ![](keyFrame.43233.jpg)
Summary: The focus returns to a different person discussing the high fidelity of cognitive services' offerings, emphasizing how the voices sound more like actual human voices. The scene then transitions to airport ground operations, showing an airplane on the tarmac with ground crew directing pushback procedures. The audio includes realistic ATC (air traffic control) communications, enhancing the authenticity of the simulation experience.
Start: 23100 ms, End: 43233 ms
Frame size: 1080 x 608
```
> [!NOTE]
> This code is based on the [Sample02_AnalyzeUrl.java](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/contentunderstanding/azure-ai-contentunderstanding/src/samples/java/com/azure/ai/contentunderstanding/samples/Sample02_AnalyzeUrl.java) sample in the SDK repository.

## Next steps

* Explore more [Java SDK samples](https://github.com/Azure/azure-sdk-for-java/tree/main/sdk/contentunderstanding/azure-ai-contentunderstanding/src/samples/java/com/azure/ai/contentunderstanding)
* [Create a custom analyzer](../../tutorial/create-custom-analyzer.md)
* [Prebuilt analyzers](../../concepts/prebuilt-analyzers.md)
* [Language and region support](../../language-region-support.md)
