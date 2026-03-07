---
title: "Quickstart: Use the Content Understanding Java SDK"
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-content-understanding
ms.topic: include
ms.date: 03/06/2026
ms.author: paulhsu
ai-usage: ai-assisted
---

<!-- markdownlint-disable MD025 -->

[Client library](https://central.sonatype.com/artifact/com.azure/azure-ai-contentunderstanding) | [Samples](https://github.com/Azure/azure-sdk-for-java/tree/main/sdk/contentunderstanding/azure-ai-contentunderstanding/src/samples/java/com/azure/ai/contentunderstanding) | [SDK source](https://github.com/Azure/azure-sdk-for-java/tree/main/sdk/contentunderstanding/azure-ai-contentunderstanding)

This quickstart shows you how to use the Content Understanding Java SDK to extract structured data from multimodal content in document, image, audio, and video files.

## Prerequisites

* An active Azure subscription. If you don't have an Azure account, [create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
* A [Microsoft Foundry resource](https://portal.azure.com/#create/Microsoft.CognitiveServicesAIFoundry) created in a [supported region](/azure/ai-services/content-understanding/language-region-support).
* [!INCLUDE [foundry-model-deployment-setup](../../includes/foundry-model-deployment-setup.md)]
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

## Create your Java application

1. Open the **App.java** file (located in `src/main/java/com/example/`) in your preferred editor or IDE.

1. Replace the contents of **App.java** with one of the following code samples:

    * [**Document search**](#document-search-model) — analyze and extract markdown content from documents.
    * [**Prebuilt invoice**](#prebuilt-model) — analyze and extract common fields from invoices.

[!INCLUDE [Azure key vault](~/reusable-content/ce-skilling/azure/includes/ai-services/security/microsoft-entra-id-akv-expanded.md)]

## Document search model

Extract markdown content, page information, and summaries from documents.

> [!div class="checklist"]
>
> * For this example, you need a **document file from a URL**. You can use the [sample invoice document](https://raw.githubusercontent.com/Azure-Samples/azure-ai-content-understanding-assets/main/document/invoice.pdf) for this quickstart.
> * The file URL value is set in the `documentUrl` variable within the `main` method.

**Add the following code sample to your App.java file. Make sure you update the endpoint and key variables with values from your Microsoft Foundry resource in the Azure portal:**

```java
import java.util.Arrays;
import com.azure.core.credential.AzureKeyCredential;
import com.azure.core.util.polling.SyncPoller;
import com.azure.ai.contentunderstanding.ContentUnderstandingClient;
import com.azure.ai.contentunderstanding.ContentUnderstandingClientBuilder;
import com.azure.ai.contentunderstanding.models.AnalysisInput;
import com.azure.ai.contentunderstanding.models.AnalysisResult;
import com.azure.ai.contentunderstanding.models.DocumentContent;

public class App {

    public static void main(String[] args) {
        // set `<your-endpoint>` and `<your-key>` variables
        // with the values from the Azure portal
        String endpoint = "<your-endpoint>";
        String key = "<your-key>";

        ContentUnderstandingClient client =
            new ContentUnderstandingClientBuilder()
                .endpoint(endpoint)
                .credential(new AzureKeyCredential(key))
                .buildClient();

        // Sample document
        String documentUrl =
            "https://raw.githubusercontent.com/"
            + "Azure-Samples/"
            + "azure-ai-content-understanding-assets/"
            + "main/document/invoice.pdf";

        AnalysisInput input = new AnalysisInput(documentUrl);

        SyncPoller<AnalysisResult, AnalysisResult> poller =
            client.beginAnalyze(
                "prebuilt-documentSearch",
                Arrays.asList(input)
            );
        AnalysisResult result = poller.getFinalResult();

        if (result.getContents() != null
            && !result.getContents().isEmpty()) {

            var content = result.getContents().get(0);
            System.out.println("Markdown:");
            System.out.println(content.getMarkdown());

            // Access document-specific properties
            if (content instanceof DocumentContent) {
                DocumentContent documentContent =
                    (DocumentContent) content;

                System.out.printf(
                    "%nPages: %d - %d%n",
                    documentContent.getStartPageNumber(),
                    documentContent.getEndPageNumber()
                );

                if (documentContent.getPages() != null
                    && !documentContent.getPages().isEmpty()) {

                    System.out.printf(
                        "Number of pages: %d%n",
                        documentContent.getPages().size()
                    );

                    for (var page
                        : documentContent.getPages()) {

                        String unit =
                            documentContent.getUnit() != null
                                ? documentContent.getUnit()
                                : "units";
                        System.out.printf(
                            "  Page %d: %.0f x %.0f %s%n",
                            page.getPageNumber(),
                            page.getWidth(),
                            page.getHeight(),
                            unit
                        );
                    }
                }
            }
        }
    }
}
```

> [!NOTE]
> This code is based on the [Sample02_AnalyzeUrl](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/contentunderstanding/azure-ai-contentunderstanding/src/samples/java/com/azure/ai/contentunderstanding/Sample02_AnalyzeUrl.java) sample in the SDK repository.

**Run the application**

After you add the code sample to your application, build and run your program:

1. Navigate to the folder where you have your **content-understanding-quickstart** project.

1. Type the following commands in your terminal:

    ```console
    mvn compile exec:java -Dexec.mainClass="com.example.App"
    ```

**Reference**: [`ContentUnderstandingClient`](https://central.sonatype.com/artifact/com.azure/azure-ai-contentunderstanding), [`beginAnalyze`](https://central.sonatype.com/artifact/com.azure/azure-ai-contentunderstanding)

___

## Prebuilt model

Analyze and extract common fields from specific document types using a prebuilt model. In this example, we analyze an invoice using the **prebuilt-invoice** analyzer.

> [!TIP]
> You aren't limited to invoices—there are several prebuilt analyzers to choose from, each of which has its own set of supported fields. For more information, see [prebuilt analyzers](../../concepts/prebuilt-analyzers.md).

> [!div class="checklist"]
>
> * Analyze an invoice using the prebuilt-invoice analyzer. You can use the [sample invoice document](https://raw.githubusercontent.com/Azure-Samples/azure-ai-content-understanding-assets/main/document/invoice.pdf) for this quickstart.
> * The file URL value is set in the `invoiceUrl` variable within the `main` method.

**Add the following code sample to your App.java file. Make sure you update the endpoint and key variables with values from your Microsoft Foundry resource in the Azure portal:**

```java
import java.util.Arrays;
import com.azure.core.credential.AzureKeyCredential;
import com.azure.core.util.polling.SyncPoller;
import com.azure.ai.contentunderstanding.ContentUnderstandingClient;
import com.azure.ai.contentunderstanding.ContentUnderstandingClientBuilder;
import com.azure.ai.contentunderstanding.models.AnalysisInput;
import com.azure.ai.contentunderstanding.models.AnalysisResult;
import com.azure.ai.contentunderstanding.models.DocumentContent;
import com.azure.ai.contentunderstanding.models.ContentObjectField;
import com.azure.ai.contentunderstanding.models.ContentArrayField;

public class App {

    public static void main(String[] args) {
        // set `<your-endpoint>` and `<your-key>` variables
        // with the values from the Azure portal
        String endpoint = "<your-endpoint>";
        String key = "<your-key>";

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

        AnalysisInput input = new AnalysisInput(invoiceUrl);

        SyncPoller<AnalysisResult, AnalysisResult> poller =
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
                System.out.printf(
                    "  Source: %s%n",
                    customerNameField.getSource() != null
                        ? customerNameField.getSource()
                        : "N/A"
                );
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
                        .getFieldOrDefault("Amount", null);
                    var currencyField = totalAmountObj
                        .getFieldOrDefault(
                            "CurrencyCode", null
                        );

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
                                    .getFieldOrDefault(
                                        "Description", null
                                    );
                                var qtyField = itemObj
                                    .getFieldOrDefault(
                                        "Quantity", null
                                    );

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

> [!NOTE]
> This code is based on the [Sample03_AnalyzeInvoice](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/contentunderstanding/azure-ai-contentunderstanding/src/samples/java/com/azure/ai/contentunderstanding/Sample03_AnalyzeInvoice.java) sample in the SDK repository.

**Run the application**

After you add the code sample to your application, build and run your program:

1. Navigate to the folder where you have your **content-understanding-quickstart** project.

1. Type the following commands in your terminal:

    ```console
    mvn compile exec:java -Dexec.mainClass="com.example.App"
    ```

**Reference**: [`ContentUnderstandingClient`](https://central.sonatype.com/artifact/com.azure/azure-ai-contentunderstanding), [`beginAnalyze`](https://central.sonatype.com/artifact/com.azure/azure-ai-contentunderstanding)

## Next steps

* Explore more [Java SDK samples](https://github.com/Azure/azure-sdk-for-java/tree/main/sdk/contentunderstanding/azure-ai-contentunderstanding/src/samples/java/com/azure/ai/contentunderstanding)
* [Create a custom analyzer](../../tutorial/create-custom-analyzer.md)
* [Prebuilt analyzers](../../concepts/prebuilt-analyzers.md)
* [Language and region support](../../language-region-support.md)
