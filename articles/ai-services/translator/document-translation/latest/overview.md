
# Azure Document Translation (2026-03-01) Overview

Azure Document Translation is the latest cloud-based feature of the Azure Translator and is part of the Foundry Tool family of REST APIs. The Document Translation API translates documents across all [supported languages and dialects](https://learn.microsoft.com/en-us/azure/ai-services/translator/language-support) while preserving document structure and data format.

## What's new in version 2026-03-01

* **Large Language Model (LLM) selection (Public Preview):**  
  By default, Document Translation uses Neural Machine Translation (NMT) models. With this version, you can optionally select Large Language Models (GPT-5.1, GPT-5.2, or GPT-5.2-chat) based on quality, cost, and other factors.

  > 📌️ Using LLM-based translation requires a Microsoft Foundry resource. For more information, see [Configure Azure resources](https://learn.microsoft.com/en-us/azure/ai-services/translator/how-to/create-translator-resource).

* **Image Translation:**  
  Translate text within standalone image files (.jpeg, .png, .bmp, .webp), with translated content rendered back into the image.

* **PDF Translation leveraging Azure Document Intelligence (batch only):**  
  Translate PDF files using Azure Document Intelligence to preserve layout and structure in the translated document. Supported only in batch/asynchronous document translation.

* **Translate images in Office documents (batch only):**  
  Translate text within images embedded in Word (.docx) and PowerPoint (.pptx) documents while preserving overall document structure. Supported only in batch/asynchronous document translation.

## Language support

Language support for LLM-based translation is listed in the Translation section of our [Language support page](https://learn.microsoft.com/en-us/azure/ai-services/translator/language-support#translation).

### LLM processing

When you deploy a large language model (LLM), the configuration options you choose—global, data zone, or regional—directly impact and determine the specific location in which your data is processed. Your selections during setup define the geographical boundaries for how and where the model processes your information.

## Pricing

* By default, document translations using general NMT models are billed according to the number of characters or images in the source document. For more information, see [Azure Translator pricing](https://azure.microsoft.com/pricing/details/cognitive-services/translator/).
* Document translations using generative AI LLMs are charged according to the number of input and output tokens processed. For more information, see [Azure OpenAI pricing](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/).

Would you like any adjustments to the content or help with saving this file?