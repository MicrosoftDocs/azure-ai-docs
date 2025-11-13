---
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: include
ms.date: 11/18/2025
ms.author: lajanuar
---
## Prerequisites

* [Create a Project in Foundry in the Microsoft Foundry portal](../../../../../ai-foundry/how-to/create-projects.md)

## Navigate to the Foundry Playground

Using the left side pane, select **Playgrounds**. Then select the **Try Azure Language Playground** button.

:::image type="content" source="../../media/quickstarts/azure-ai-foundry/foundry-playground-navigation.png" alt-text="The development lifecycle" lightbox="../../media/quickstarts/azure-ai-foundry/foundry-playground-navigation.png":::

## Use Summarization in the Foundry Playground

The **Language Playground** consists of four sections:

* Top banner: You can select any of the currently available Languages here.
* Right pane: This pane is where you can find the **Configuration** options for the service, such as the API and model version, along with features specific to the service.
* Center pane: This pane is where you enter your text for processing. After the operation is run, some results are shown here.
* Right pane: This pane is where **Details** of the run operation are shown.

Here you can select the Summarization capability that you want to use by choosing one of these top banner tiles: **Summarize conversation**, **Summarize for call center**, or **Summarize text**.

### Use Summarize conversation

**Summarize conversation** is designed to recap conversations and segment long meetings into timestamped chapters.

In **Configuration** there are the following options:

|Option              |Description                              |
|--------------------|-----------------------------------------|
|Select API version  | Select which version of the API to use.    |
|Select text language| Select the language of the input text.|
|Summarization Aspects| Different methods of summarization that are returned. At least one must be selected.|

After your operation is completed, the **Details** section contains the following fields for the selected methods of summarization:

|Field | Description                |
|------|----------------------------|
|Sentence|
|Recap| A recap of the processed text. The **Recap** Summarization aspect must be toggled on for this to appear.|
|Chapter Title|  A list of titles for semantically segmented chapters with corresponding timestamps. The **Chapter title** Summarization aspect must be toggled on for this to appear.|
|Narrative|  A list of narrative summaries for semantically segmented chapters with corresponding timestamps. The **Narrative** Summarization aspect must be toggled on for this to appear.|

:::image type="content" source="../../media/quickstarts/azure-ai-foundry/conversation-summarization.png" alt-text="A screenshot of an example of summarize conversation in Foundry portal." lightbox="../../media/quickstarts/azure-ai-foundry/conversation-summarization.png":::

### Use Summarize for call center

**Summarize for call center** is designed to recap calls and summarize them for customer issues and resolutions.

In **Configuration** there are the following options:

|Option              |Description                              |
|--------------------|-----------------------------------------|
|Select API version  | Select which version of the API to use.    |
|Select text language| Select the language of the input text.|
|Summarization Aspects| Different methods of summarization that are returned. At least one must be selected.|

After your operation is completed, the **Details** section contains the following fields for the selected methods of summarization:

|Field | Description                |
|------|----------------------------|
|Sentence|
|Recap| A recap of the processed text. The **Recap** Summarization aspect must be toggled on for this to appear.|
|Issue|  A summary of the customer issue in the customer-and-agent conversation. The **Issue** Summarization aspect must be toggled on for this to appear.|
|Resolution|  A summary of the solutions tried in the customer-and-agent conversation. The **Resolution** Summarization aspect must be toggled on for this to appear.|

:::image type="content" source="../../media/quickstarts/azure-ai-foundry/call-center-summarization.png" alt-text="A screenshot of an example of summarize for call center in Foundry portal." lightbox="../../media/quickstarts/azure-ai-foundry/call-center-summarization.png":::

### Use Summarize text

**Summarize text** is designed to summarize and extract key information at scale from text.

In **Configuration** there are the following options:

|Option              |Description                              |
|--------------------|-----------------------------------------|
|Extractive summarization  |  The service will produce a summary by extracting salient sentences.  |
|Number of sentences| The number of sentences that Extractive summarization will extract.|
|Abstractive summarization| the service will generate a summary with novel sentences.|
|Summary length| The length of the summary generated by Abstractive summarization.|
|Define keywords for summary focus (preview)| Helps focus summarization on a particular set of keywords.|

After your operation is completed, the **Details** section contains the following fields for the selected methods of summarization:

|Field | Description                |
|------|----------------------------|
|Extractive summary| Extracted sentences from the input text, ranked by detected relevance and prioritized for words in the **Defined keywords for summary focus** field, if any. Sentences are sorted by rank score of detected relevance (default) or order of appearance in the input text.|
|Abstractive summary| A summary of the input text of the length chosen in the **Summary length** field and prioritized for words in the **Defined keywords for summary focus** field, if any.|

:::image type="content" source="../../media/quickstarts/azure-ai-foundry/text-summarization.png" alt-text="A screenshot of an example of summarize text in Foundry portal." lightbox="../../media/quickstarts/azure-ai-foundry/text-summarization.png":::
