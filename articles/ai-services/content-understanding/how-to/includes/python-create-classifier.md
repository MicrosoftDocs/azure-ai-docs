---
title: Create a basic classifier using the Content Understanding Python SDK
author: PatrickFarley
manager: mcleans
description: Create a classifier analyzer with the Content Understanding Python SDK.
ms.service: azure-content-understanding-foundry-tools
ms.topic: include
ms.date: 07/20/2026
ms.author: pafarley
ai-usage: ai-assisted
---

<!-- markdownlint-disable MD025 -->

Install the required packages. Use `--pre` to pull the prerelease build of `azure-ai-contentunderstanding` (1.2.0b2 or later), which is the first version that exports the `to_llm_input` helper used in this sample. The current stable release (1.1.0) doesn't include it.

```bash
pip install --pre azure-ai-contentunderstanding
pip install azure-identity python-dotenv
```

The following sample creates a classifier, analyzes a multi-document PDF, converts the classification result to LLM-friendly text, and then deletes the classifier. The `Invoice` category also sets `analyzer_id="prebuilt-invoice"` to demonstrate optional per-category routing (covered in Step 2).

```python
import os
import time
from typing import cast

from dotenv import load_dotenv
from azure.ai.contentunderstanding import ContentUnderstandingClient
from azure.ai.contentunderstanding import to_llm_input
from azure.ai.contentunderstanding.models import (
    ContentAnalyzer,
    ContentAnalyzerConfig,
    ContentCategoryDefinition,
    AnalysisResult,
    DocumentContent,
)
from azure.core.credentials import AzureKeyCredential
from azure.identity import DefaultAzureCredential

load_dotenv()


def main() -> None:
    endpoint = os.environ["CONTENTUNDERSTANDING_ENDPOINT"]
    key = os.getenv("CONTENTUNDERSTANDING_KEY")
    credential = AzureKeyCredential(key) if key else DefaultAzureCredential()

    client = ContentUnderstandingClient(endpoint=endpoint, credential=credential)

    # Generate a unique analyzer ID
    analyzer_id = f"my_classifier_{int(time.time())}"

    print(f"Creating classifier '{analyzer_id}'...")

    # Define content categories for classification.
    # Each category has a description that helps the AI model identify matching documents.
    # Optionally, set analyzer_id on a category to route matched segments to a prebuilt
    # or custom analyzer for field extraction. For example, setting
    # analyzer_id="prebuilt-invoice" on the Invoice category will automatically extract
    # invoice fields (vendor, line items, totals, etc.) from segments classified as Invoice.
    categories = {
        "Loan_Application": ContentCategoryDefinition(
            description="Documents submitted by individuals or businesses to request funding, "
            "typically including personal or business details, financial history, "
            "loan amount, purpose, and supporting documentation."
        ),
        "Invoice": ContentCategoryDefinition(
            description="Billing documents issued by sellers or service providers to request "
            "payment for goods or services, detailing items, prices, taxes, totals, "
            "and payment terms.",
            analyzer_id="prebuilt-invoice",  # Route Invoice segments for field extraction
        ),
        "Bank_Statement": ContentCategoryDefinition(
            description="Official statements issued by banks that summarize account activity "
            "over a period, including deposits, withdrawals, fees, and balances."
        ),
    }

    # Create analyzer configuration
    config = ContentAnalyzerConfig(
        return_details=True,
        enable_segment=True,  # Enable automatic segmentation by category
        content_categories=categories,
    )

    # Create the classifier analyzer
    classifier = ContentAnalyzer(
        base_analyzer_id="prebuilt-document",
        description="Custom classifier for financial document categorization",
        config=config,
        models={"completion": "gpt-5.2"},
    )

    # Create the classifier
    poller = client.begin_create_analyzer(
        analyzer_id=analyzer_id,
        resource=classifier,
    )
    result = poller.result()  # Wait for creation to complete

    # Get the full analyzer details after creation
    result = client.get_analyzer(analyzer_id=analyzer_id)

    print(f"Classifier '{analyzer_id}' created successfully!")
    if result.description:
        print(f"  Description: {result.description}")

    file_path = "sample_files/mixed_financial_docs.pdf"

    with open(file_path, "rb") as f:
        file_bytes = f.read()

    print(f"\nAnalyzing document with classifier '{analyzer_id}'...")

    analyze_poller = client.begin_analyze_binary(
        analyzer_id=analyzer_id,
        binary_input=file_bytes,
    )
    analyze_result: AnalysisResult = analyze_poller.result()

    # Display classification results
    if analyze_result.contents and len(analyze_result.contents) > 0:
        document_content = cast(DocumentContent, analyze_result.contents[0])
        print(
            f"Pages: {document_content.start_page_number}-{document_content.end_page_number}"
        )

        # Display segments (classification results)
        if document_content.segments and len(document_content.segments) > 0:
            print(f"\nFound {len(document_content.segments)} segment(s):")
            for segment in document_content.segments:
                print(f"  Category: {segment.category or '(unknown)'}")
                print(f"  Pages: {segment.start_page_number}-{segment.end_page_number}")
                print(f"  Segment ID: {segment.segment_id or '(not available)'}")
                print()
        else:
            print("No segments found (document classified as a single unit).")
    else:
        print("No content found in the analysis result.")

    # Convert classification results to LLM-friendly text.
    # to_llm_input automatically detects classification results: it expands the parent
    # into per-segment blocks, each with its category label in the YAML front matter.
    # Segments are separated by a ***** divider.
    print("\n" + "=" * 60)
    print("CLASSIFICATION RESULT AS LLM INPUT")
    print("=" * 60)

    text = to_llm_input(analyze_result)
    print(text)

    # Clean up - delete the classifier
    print(f"\nCleaning up: deleting classifier '{analyzer_id}'...")
    client.delete_analyzer(analyzer_id=analyzer_id)
    print(f"Classifier '{analyzer_id}' deleted successfully.")


if __name__ == "__main__":
    main()
```

**Reference**: [`azure-ai-contentunderstanding` Python samples](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/contentunderstanding/azure-ai-contentunderstanding/samples)
