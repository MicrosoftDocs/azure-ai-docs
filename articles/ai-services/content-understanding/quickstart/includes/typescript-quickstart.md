---
title: "Quickstart: Use the Content Understanding TypeScript SDK"
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-content-understanding
ms.topic: include
ms.date: 03/06/2026
ms.author: paulhsu
ai-usage: ai-assisted
---

<!-- markdownlint-disable MD025 -->

[Client library](https://www.npmjs.com/package/@azure/ai-content-understanding) | [Samples](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/contentunderstanding/ai-content-understanding/samples/v1/typescript) | [SDK source](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/contentunderstanding/ai-content-understanding)

This quickstart shows you how to use the Content Understanding TypeScript SDK to extract structured data from multimodal content in document, image, audio, and video files.

## Prerequisites

* An active Azure subscription. If you don't have an Azure account, [create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
* A [Microsoft Foundry resource](https://portal.azure.com/#create/Microsoft.CognitiveServicesAIFoundry) created in a [supported region](/azure/ai-services/content-understanding/language-region-support).
* [!INCLUDE [foundry-model-deployment-setup](../../includes/foundry-model-deployment-setup.md)]
* [Node.js](https://nodejs.org/) LTS version.
* [TypeScript](https://www.typescriptlang.org/) 5.x or later.

## Set up

1. Create a new Node.js project:

    ```console
    mkdir content-understanding-quickstart
    cd content-understanding-quickstart
    npm init -y
    ```

1. Install TypeScript and the Content Understanding client library:

    ```console
    npm install typescript ts-node @azure/ai-content-understanding
    ```

1. Optionally, install the Azure Identity library for Microsoft Entra authentication:

    ```console
    npm install @azure/identity
    ```

1. Create a **tsconfig.json** file with the following content:

    ```json
    {
        "compilerOptions": {
            "target": "ES2020",
            "module": "commonjs",
            "strict": true,
            "esModuleInterop": true,
            "skipLibCheck": true
        }
    }
    ```

## Create your TypeScript application

1. Create a new file called **index.ts** in your preferred editor or IDE.

1. Open the **index.ts** file and select one of the following code samples to copy and paste into your application:

    * [**Document search**](#document-search-model) — analyze and extract markdown content from documents.
    * [**Prebuilt invoice**](#prebuilt-model) — analyze and extract common fields from invoices.

[!INCLUDE [Azure key vault](~/reusable-content/ce-skilling/azure/includes/ai-services/security/microsoft-entra-id-akv-expanded.md)]

## Document search model

Extract markdown content, page information, and summaries from documents.

> [!div class="checklist"]
>
> * For this example, you need a **document file from a URL**. You can use the [sample invoice document](https://raw.githubusercontent.com/Azure-Samples/azure-ai-content-understanding-assets/main/document/invoice.pdf) for this quickstart.
> * The file URL value is set in the `documentUrl` variable within the `main` function.

**Add the following code sample to your index.ts file. Make sure you update the endpoint and key variables with values from your Microsoft Foundry resource in the Azure portal:**

```typescript
import { AzureKeyCredential } from "@azure/core-auth";
import {
    ContentUnderstandingClient,
    type DocumentContent,
} from "@azure/ai-content-understanding";

// set `<your-endpoint>` and `<your-key>` variables
// with the values from the Azure portal
const endpoint = "<your-endpoint>";
const key = "<your-key>";

async function main(): Promise<void> {
    const client = new ContentUnderstandingClient(
        endpoint,
        new AzureKeyCredential(key)
    );

    // Sample document
    const documentUrl =
        "https://raw.githubusercontent.com/"
        + "Azure-Samples/"
        + "azure-ai-content-understanding-assets/"
        + "main/document/invoice.pdf";

    const poller = client.analyze(
        "prebuilt-documentSearch",
        [{ url: documentUrl }]
    );
    const result = await poller.pollUntilDone();

    if (result.contents && result.contents.length > 0) {
        const content = result.contents[0];
        console.log("Markdown:");
        console.log(content.markdown);

        // Access document-specific properties
        if (content.kind === "document") {
            const documentContent =
                content as DocumentContent;

            console.log(
                `\nPages: `
                + `${documentContent.startPageNumber}`
                + ` - ${documentContent.endPageNumber}`
            );

            if (
                documentContent.pages
                && documentContent.pages.length > 0
            ) {
                console.log(
                    `Number of pages: `
                    + `${documentContent.pages.length}`
                );
                for (const page
                    of documentContent.pages) {

                    const unit =
                        documentContent.unit ?? "units";
                    console.log(
                        `  Page ${page.pageNumber}: `
                        + `${page.width} x `
                        + `${page.height} ${unit}`
                    );
                }
            }
        }
    }
}

main().catch((err) => {
    console.error("The sample encountered an error:", err);
});
```

> [!NOTE]
> This code is based on the [analyzeUrl.ts](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/contentunderstanding/ai-content-understanding/samples/v1/typescript/src/analyzeUrl.ts) sample in the SDK repository.

**Run the application**

After you add the code sample to your application, run your program:

1. Navigate to the folder where you have your **index.ts** file.

1. Type the following command in your terminal:

    ```console
    npx ts-node index.ts
    ```

**Reference**: [`ContentUnderstandingClient`](https://www.npmjs.com/package/@azure/ai-content-understanding), [`analyze`](https://www.npmjs.com/package/@azure/ai-content-understanding)

___

## Prebuilt model

Analyze and extract common fields from specific document types using a prebuilt model. In this example, we analyze an invoice using the **prebuilt-invoice** analyzer.

> [!TIP]
> You aren't limited to invoices—there are several prebuilt analyzers to choose from, each of which has its own set of supported fields. For more information, see [prebuilt analyzers](../../concepts/prebuilt-analyzers.md).

> [!div class="checklist"]
>
> * Analyze an invoice using the prebuilt-invoice analyzer. You can use the [sample invoice document](https://raw.githubusercontent.com/Azure-Samples/azure-ai-content-understanding-assets/main/document/invoice.pdf) for this quickstart.
> * The file URL value is set in the `invoiceUrl` variable within the `main` function.

**Add the following code sample to your index.ts file. Make sure you update the endpoint and key variables with values from your Microsoft Foundry resource in the Azure portal:**

```typescript
import { AzureKeyCredential } from "@azure/core-auth";
import {
    ContentUnderstandingClient,
    type DocumentContent,
    type ArrayField,
    type ObjectField,
} from "@azure/ai-content-understanding";

// set `<your-endpoint>` and `<your-key>` variables
// with the values from the Azure portal
const endpoint = "<your-endpoint>";
const key = "<your-key>";

async function main(): Promise<void> {
    const client = new ContentUnderstandingClient(
        endpoint,
        new AzureKeyCredential(key)
    );

    // Sample invoice
    const invoiceUrl =
        "https://raw.githubusercontent.com/"
        + "Azure-Samples/"
        + "azure-ai-content-understanding-assets/"
        + "main/document/invoice.pdf";

    const poller = client.analyze(
        "prebuilt-invoice",
        [{ url: invoiceUrl }]
    );
    const result = await poller.pollUntilDone();

    if (
        !result.contents
        || result.contents.length === 0
    ) {
        console.log(
            "No content found in the analysis result."
        );
        return;
    }

    const content = result.contents[0];

    // Get the document content
    if (content.kind === "document") {
        const documentContent =
            content as DocumentContent;

        console.log(
            `Document unit: `
            + `${documentContent.unit ?? "unknown"}`
        );
        console.log(
            `Pages: ${documentContent.startPageNumber}`
            + ` to ${documentContent.endPageNumber}`
        );

        if (!documentContent.fields) {
            console.log("No fields found.");
            return;
        }

        // Extract simple string fields
        const customerNameField =
            documentContent.fields["CustomerName"];
        if (customerNameField) {
            console.log(
                `Customer Name: `
                + `${customerNameField.value ?? "(None)"}`
            );
            if (
                customerNameField.confidence !== undefined
            ) {
                console.log(
                    `  Confidence: `
                    + `${customerNameField.confidence
                        .toFixed(2)}`
                );
            }
            console.log(
                `  Source: `
                + `${customerNameField.source ?? "N/A"}`
            );
        }

        // Extract date fields
        const invoiceDateField =
            documentContent.fields["InvoiceDate"];
        if (invoiceDateField) {
            console.log(
                `Invoice Date: `
                + `${invoiceDateField.value ?? "(None)"}`
            );
            if (
                invoiceDateField.confidence !== undefined
            ) {
                console.log(
                    `  Confidence: `
                    + `${invoiceDateField.confidence
                        .toFixed(2)}`
                );
            }
        }

        // Extract object fields (nested structures)
        const totalAmountField =
            documentContent.fields["TotalAmount"];
        if (
            totalAmountField
            && totalAmountField.type === "object"
        ) {
            const objField =
                totalAmountField as ObjectField;
            if (objField.value) {
                const amountField =
                    objField.value["Amount"];
                const currencyField =
                    objField.value["CurrencyCode"];

                const amount =
                    amountField?.value ?? "(None)";
                const currency =
                    currencyField?.value ?? "";

                console.log(
                    `\nTotal: ${currency}${amount}`
                );
            }
        }

        // Extract array fields (line items)
        const lineItemsField =
            documentContent.fields["LineItems"];
        if (
            lineItemsField
            && lineItemsField.type === "array"
        ) {
            const arrField =
                lineItemsField as ArrayField;
            if (
                arrField.value
                && arrField.value.length > 0
            ) {
                console.log(
                    `\nLine Items `
                    + `(${arrField.value.length}):`
                );
                arrField.value.forEach(
                    (item, index) => {
                        if (item.type === "object") {
                            const itemObj =
                                item as ObjectField;
                            if (itemObj.value) {
                                const descField =
                                    itemObj.value[
                                        "Description"
                                    ];
                                const qtyField =
                                    itemObj.value[
                                        "Quantity"
                                    ];

                                const description =
                                    descField?.value
                                    ?? "N/A";
                                const quantity =
                                    qtyField?.value
                                    ?? "N/A";

                                console.log(
                                    `  Item `
                                    + `${index + 1}: `
                                    + `${description}`
                                );
                                console.log(
                                    `    Quantity: `
                                    + `${quantity}`
                                );
                            }
                        }
                    }
                );
            }
        }
    }
}

main().catch((err) => {
    console.error("The sample encountered an error:", err);
});
```

> [!NOTE]
> This code is based on the [analyzeInvoice.ts](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/contentunderstanding/ai-content-understanding/samples/v1/typescript/src/analyzeInvoice.ts) sample in the SDK repository.

**Run the application**

After you add the code sample to your application, run your program:

1. Navigate to the folder where you have your **index.ts** file.

1. Type the following command in your terminal:

    ```console
    npx ts-node index.ts
    ```

**Reference**: [`ContentUnderstandingClient`](https://www.npmjs.com/package/@azure/ai-content-understanding), [`analyze`](https://www.npmjs.com/package/@azure/ai-content-understanding)

## Next steps

* Explore more [TypeScript SDK samples](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/contentunderstanding/ai-content-understanding/samples/v1/typescript)
* [Create a custom analyzer](../../tutorial/create-custom-analyzer.md)
* [Prebuilt analyzers](../../concepts/prebuilt-analyzers.md)
* [Language and region support](../../language-region-support.md)
