---
title: Create a basic classifier using the Content Understanding JavaScript SDK
author: PatrickFarley
manager: mcleans
description: Create a classifier analyzer with the Content Understanding JavaScript SDK.
ms.service: azure-content-understanding-foundry-tools
ms.topic: include
ms.date: 07/20/2026
ms.author: pafarley
ai-usage: ai-assisted
---

<!-- markdownlint-disable MD025 -->

Install the required packages:

```bash
npm install @azure/ai-content-understanding @azure/identity @azure/core-auth dotenv
```

The following sample creates a classifier, analyzes a multi-document PDF, and then deletes the classifier. The `Invoice` category also sets `analyzerId: "prebuilt-invoice"` to demonstrate optional per-category routing (covered in Step 2).

```javascript
// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

require("dotenv/config");
const fs = require("fs");
const path = require("path");
const { DefaultAzureCredential } = require("@azure/identity");
const { AzureKeyCredential } = require("@azure/core-auth");
const { ContentUnderstandingClient } = require("@azure/ai-content-understanding");

function getCredential() {
  const key = process.env["CONTENTUNDERSTANDING_KEY"];
  if (key) {
    return new AzureKeyCredential(key);
  }
  return new DefaultAzureCredential();
}

async function main() {
  console.log("== Create Classifier Sample ==");

  const endpoint = process.env["CONTENTUNDERSTANDING_ENDPOINT"];
  if (!endpoint) {
    throw new Error("CONTENTUNDERSTANDING_ENDPOINT is required.");
  }

  const client = new ContentUnderstandingClient(endpoint, getCredential());

  // Generate a unique analyzer ID
  const analyzerId = `my_classifier_${Math.floor(Date.now() / 1000)}`;
  console.log(`Creating classifier '${analyzerId}'...`);

  // Define content categories for classification
  const contentCategories = {
    Loan_Application: {
      description:
        "Documents submitted by individuals or businesses to request funding, " +
        "typically including personal or business details, financial history, " +
        "loan amount, purpose, and supporting documentation.",
    },
    Invoice: {
      description:
        "Billing documents issued by sellers or service providers to request " +
        "payment for goods or services, detailing items, prices, taxes, totals, " +
        "and payment terms.",
    },
    Bank_Statement: {
      description:
        "Official statements issued by banks that summarize account activity " +
        "over a period, including deposits, withdrawals, fees, and balances.",
    },
  };

  // Create analyzer configuration
  const config = {
    returnDetails: true,
    enableSegment: true, // Enable automatic segmentation by category
    contentCategories,
  };

  // Create the classifier analyzer
  const classifier = {
    baseAnalyzerId: "prebuilt-document",
    description: "Custom classifier for financial document categorization",
    config,
    models: { completion: "gpt-5.2" },
  };

  // Create the classifier
  const poller = client.createAnalyzer(analyzerId, classifier);
  await poller.pollUntilDone();

  // Get the full analyzer details after creation
  const result = await client.getAnalyzer(analyzerId);

  console.log(`Classifier '${analyzerId}' created successfully!`);
  if (result.description) {
    console.log(`  Description: ${result.description}`);
  }

  // Analyze a document with the classifier
  // Assets folder is at ../assets relative to samples/v1/javascript or samples/v1/typescript
  const filePath = path.join("..", "..", "assets", "mixed_financial_docs.pdf");
  const fileBytes = fs.readFileSync(filePath);
  console.log(`\nAnalyzing document with classifier '${analyzerId}'...`);

  const analyzePoller = client.analyzeBinary(analyzerId, fileBytes);
  const analyzeResult = await analyzePoller.pollUntilDone();

  // Display classification results
  if (analyzeResult.contents && analyzeResult.contents.length > 0) {
    const content = analyzeResult.contents[0];
    if (content.kind === "document") {
      const documentContent = content;
      console.log(`Pages: ${documentContent.startPageNumber}-${documentContent.endPageNumber}`);

      // Display segments (classification results)
      if (documentContent.segments && documentContent.segments.length > 0) {
        console.log(`\nFound ${documentContent.segments.length} segment(s):`);
        for (const segment of documentContent.segments) {
          console.log(`  Category: ${segment.category ?? "(unknown)"}`);
          console.log(`  Pages: ${segment.startPageNumber}-${segment.endPageNumber}`);
          console.log(`  Segment ID: ${segment.segmentId ?? "(not available)"}`);
        }
      } else {
        console.log("No segments found (document classified as a single unit).");
      }
    }
  } else {
    console.log("No content found in the analysis result.");
  }

  // Clean up - delete the classifier
  console.log(`\nCleaning up: deleting classifier '${analyzerId}'...`);
  await client.deleteAnalyzer(analyzerId);
  console.log(`Classifier '${analyzerId}' deleted successfully.`);
}

main().catch((err) => {
  console.error("The sample encountered an error:", err);
});

module.exports = { main };
```

**Reference**: [`@azure/ai-content-understanding` JavaScript samples](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/contentunderstanding/ai-content-understanding/samples/v1/javascript)
