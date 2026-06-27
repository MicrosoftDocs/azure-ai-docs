---
title: Summarize text, documents, and conversations
titleSuffix: Foundry Tools
description: This article shows you how to summarize text, native documents, and conversations with the summarization APIs.
author: laujan
manager: mcleans
ms.service: azure-ai-language
ms.topic: how-to
ms.date: 06/26/2026
ms.author: lajanuar
ms.custom:
  - language-service-summarization
---
<!-- markdownlint-disable MD025 -->
<!-- markdownlint-disable MD024 -->

# How to use summarization

Summarization condenses content that users consider too long to read. The service provides summarization solutions for three types of genre: plain text, conversations, and native documents. Select the tab that matches the type of content you want to summarize.

# [Text summarization](#tab/text-summarization)

Text summarization shortens content that users consider too long to read. Both extractive and abstractive summarization condense articles, papers, or documents to key sentences.

**Extractive summarization**: Produces a summary by extracting sentences that collectively represent the most important or relevant information within the original content.

**Abstractive summarization**: Produces a summary by generating summarized sentences from the document that capture the main idea.

**Query-focused summarization**: Allows you to use a query when summarizing.

Each of these capabilities can summarize around specific items of interest when specified.

The service provides the AI models that the API uses. You just have to send content for analysis.

For easier navigation, here are links to the corresponding sections for each service:

|Aspect       |Section                                                            |
|-------------|-------------------------------------------------------------------|
|Extractive   |[Extractive Summarization](#try-text-extractive-summarization) |
|Abstractive  |[Abstractive Summarization](#try-text-abstractive-summarization)|
|Query-focused|[Query-focused Summarization](#query-based-summarization)          |

## Features

> [!TIP]
> To start using these features, see the [quickstart article](../quickstart.md). You can also make example requests by using [Microsoft Foundry](https://ai.azure.com/) without needing to write code.

The extractive summarization API uses natural language processing techniques to locate key sentences in an unstructured text document. These sentences collectively convey the main idea of the document.

Extractive summarization returns a rank score as part of the system response along with extracted sentences and their position in the original documents. A rank score indicates how relevant a sentence is to the main idea of a document. The model gives a score between 0 and 1 (inclusive) to each sentence and returns the highest scored sentences per request. For example, if you request a three-sentence summary, the service returns the three highest scored sentences.

Another feature in Azure Language in Foundry Tools, [key phrase extraction](./../../key-phrase-extraction/how-to/call-api.md), can extract key information. When deciding between key phrase extraction and extractive summarization, consider these factors:

* Key phrase extraction returns phrases while extractive summarization returns sentences.
* Extractive summarization returns sentences together with a rank score, and top ranked sentences are returned per request.
* Extractive summarization also returns the following positional information:
    * Offset: The start position of each extracted sentence.
    * Length: The length of each extracted sentence.

## Determine how to process the data (optional)

### Submitting data

Submit documents to the API as strings of text. The API performs analysis upon receipt of the request. Because the API is [asynchronous](../../concepts/use-asynchronously.md), there might be a delay between sending an API request and receiving the results.

When you use this feature, the API results are available for 24 hours from the time the request is ingested, and the response indicates this availability. After this time period, the results are purged and are no longer available for retrieval.

### Getting text summarization results

When you get results from language detection, you can stream the results to an application or save the output to a file on the local system.

The following example shows content you might submit for summarization. The content is extracted from the Microsoft blog article [A holistic representation toward integrative AI](https://www.microsoft.com/research/blog/a-holistic-representation-toward-integrative-ai/). This article is only an example. The API can accept longer input text. For more information, *see* [data and service limits](../overview.md#input-requirements-and-service-limits).
 
*"At Microsoft, we are on a quest to advance AI beyond existing techniques, by taking a more holistic, human-centric approach to learning and understanding. As Chief Technology Officer of Foundry Tools, I have been working with a team of amazing scientists and engineers to turn this quest into a reality. In my role, I enjoy a unique perspective in viewing the relationship among three attributes of human cognition: monolingual text (X), audio or visual sensory signals, (Y) and multilingual (Z). At the intersection of all three, there's magic—what we call XYZ-code as illustrated in Figure 1—a joint representation to create more powerful AI that can speak, hear, see, and understand humans better. We believe XYZ-code enables us to fulfill our long-term vision: cross-domain transfer learning, spanning modalities and languages. The goal is to have pretrained models that can jointly learn representations to support a broad range of downstream AI tasks, much in the way humans do today. Over the past five years, we achieved human performance on benchmarks in conversational speech recognition, machine translation, conversational question answering, machine reading comprehension, and image captioning. These five breakthroughs provided us with strong signals toward our more ambitious aspiration to produce a leap in AI capabilities, achieving multi-sensory and multilingual learning that's closer in line with how humans learn and understand. I believe the joint XYZ-code is a foundational component of this aspiration, if grounded with external knowledge sources in the downstream AI tasks."*

The text summarization API request is processed upon receipt of the request by creating a job for the API backend. If the job succeeded, the output of the API is returned. The output is available for retrieval for 24 hours. After this time, the output is purged. Due to multilingual and emoji support, the response might contain text offsets. For more information, *see* [how to process offsets](../../concepts/multilingual-emoji-support.md).

When you use the preceding example, the API might return these summarized sentences:

**Extractive summarization**:

- "At Microsoft, we're on a quest to advance AI beyond existing techniques by taking a more holistic, human-centric approach to learning and understanding."
- "We believe XYZ-code enables us to fulfill our long-term vision: cross-domain transfer learning, spanning modalities and languages."
- "The goal is to have pretrained models that can jointly learn representations to support a broad range of downstream AI tasks, much in the way humans do today."

**Abstractive summarization**:
- "Microsoft is taking a more holistic, human-centric approach to learning and understanding. We believe XYZ-code enables us to fulfill our long-term vision: cross-domain transfer learning, spanning modalities and languages. Over the past five years, we achieved human performance on key benchmarks."

### Try text extractive summarization

You can use text extractive summarization to get summaries of articles, papers, or documents. To see an example, see the [quickstart article](../quickstart.md).

Use the `sentenceCount` parameter to guide how many sentences are returned, with `3` being the default. The range is from 1 to 20.

Use the `sortby` parameter to specify in what order the extracted sentences are returned—either `Offset` or `Rank`, with `Offset` being the default. 

| Parameter value | Description |
|--|--|
| Rank | Order sentences according to their relevance to the input document, as decided by the service. |
| Offset | Keeps the original order in which the sentences appear in the input document. |

### Try text abstractive summarization

The following example shows how to get started with text abstractive summarization:

1. Copy the following command into a text editor. The BASH example uses the `\` line continuation character. If your console or terminal uses a different line continuation character, use that character instead.

```bash
curl -i -X POST https://<your-language-resource-endpoint>/language/analyze-text/jobs?api-version=2023-04-01 \
-H "Content-Type: application/json" \
-H "Ocp-Apim-Subscription-Key: <your-language-resource-key>" \
-d \
' 
{
  "displayName": "Text Abstractive Summarization Task Example",
  "analysisInput": {
    "documents": [
      {
        "id": "1",
        "language": "en",
        "text": "At Microsoft, we have been on a quest to advance AI beyond existing techniques, by taking a more holistic, human-centric approach to learning and understanding. As Chief Technology Officer of Foundry Tools, I have been working with a team of amazing scientists and engineers to turn this quest into a reality. In my role, I enjoy a unique perspective in viewing the relationship among three attributes of human cognition: monolingual text (X), audio or visual sensory signals, (Y) and multilingual (Z). At the intersection of all three, there's magic—what we call XYZ-code as illustrated in Figure 1—a joint representation to create more powerful AI that can speak, hear, see, and understand humans better. We believe XYZ-code enables us to fulfill our long-term vision: cross-domain transfer learning, spanning modalities and languages. The goal is to have pretrained models that can jointly learn representations to support a broad range of downstream AI tasks, much in the way humans do today. Over the past five years, we have achieved human performance on benchmarks in conversational speech recognition, machine translation, conversational question answering, machine reading comprehension, and image captioning. These five breakthroughs provided us with strong signals toward our more ambitious aspiration to produce a leap in AI capabilities, achieving multi-sensory and multilingual learning that is closer in line with how humans learn and understand. I believe the joint XYZ-code is a foundational component of this aspiration, if grounded with external knowledge sources in the downstream AI tasks."
      }
    ]
  },
  "tasks": [
    {
      "kind": "AbstractiveSummarization",
      "taskName": "Text Abstractive Summarization Task 1",
    }
  ]
}
'
```

1. Make the following changes in the command where needed:
    - Replace the value `your-language-resource-key` with your key.
    - Replace the first part of the request URL `your-language-resource-endpoint` with your endpoint URL.

1. Open a command prompt window (for example: BASH).

1. Paste the command from the text editor into the command prompt window, and then run the command.

1. Get the `operation-location` from the response header. The value looks similar to the following URL:

```http
https://<your-language-resource-endpoint>/language/analyze-text/jobs/12345678-1234-1234-1234-12345678?api-version=2022-10-01-preview
```

1. To get the results of the request, use the following cURL command. Be sure to replace `<my-job-id>` with the numerical ID value you received from the previous `operation-location` response header:

```bash
curl -X GET https://<your-language-resource-endpoint>/language/analyze-text/jobs/<my-job-id>?api-version=2022-10-01-preview \
-H "Content-Type: application/json" \
-H "Ocp-Apim-Subscription-Key: <your-language-resource-key>"
```

### Abstractive text summarization example JSON response

```json
{
    "jobId": "cd6418fe-db86-4350-aec1-f0d7c91442a6",
    "lastUpdateDateTime": "2022-09-08T16:45:14Z",
    "createdDateTime": "2022-09-08T16:44:53Z",
    "expirationDateTime": "2022-09-09T16:44:53Z",
    "status": "succeeded",
    "errors": [],
    "displayName": "Text Abstractive Summarization Task Example",
    "tasks": {
        "completed": 1,
        "failed": 0,
        "inProgress": 0,
        "total": 1,
        "items": [
            {
                "kind": "AbstractiveSummarizationLROResults",
                "taskName": "Text Abstractive Summarization Task 1",
                "lastUpdateDateTime": "2022-09-08T16:45:14.0717206Z",
                "status": "succeeded",
                "results": {
                    "documents": [
                        {
                            "summaries": [
                                {
                                    "text": "Microsoft is taking a more holistic, human-centric approach to AI. We've developed a joint representation to create more powerful AI that can speak, hear, see, and understand humans better. We've achieved human performance on benchmarks in conversational speech recognition, machine translation, ...... and image captions.",
                                    "contexts": [
                                        {
                                            "offset": 0,
                                            "length": 247
                                        }
                                    ]
                                }
                            ],
                            "id": "1"
                        }
                    ],
                    "errors": [],
                    "modelVersion": "latest"
                }
            }
        ]
    }
}
```

| Parameter | Description |
|---------|---------|
|`-X POST <endpoint>`     | Specifies your endpoint for accessing the API.        |
|`-H Content-Type: application/json`     | The content type for sending JSON data.          |
|`-H "Ocp-Apim-Subscription-Key:<key>`    | Specifies the key for accessing the API.        |
|`-d <documents>`     | The JSON containing the documents you want to send.         |

The following cURL commands are executed from a BASH shell. Edit these commands with your own resource name, resource key, and JSON values.

## Query based summarization

The query-based text summarization API is an extension to the existing text summarization API.

The biggest difference is a new `query` field in the request body (under `tasks` > `parameters` > `query`).

> [!TIP]
> Query-based summarization has some differentiation in the utilization of length control based on the type of query based summarization you're using:
> - Query-based extractive summarization supports length control by specifying `sentenceCount`.
> - Query-based abstractive summarization doesn't support length control.

Here's an example request:

```bash
curl -i -X POST https://<your-language-resource-endpoint>/language/analyze-text/jobs?api-version=2023-11-15-preview \
-H "Content-Type: application/json" \
-H "Ocp-Apim-Subscription-Key: <your-language-resource-key>" \
-d \
' 
{
  "displayName": "Text Extractive Summarization Task Example",
  "analysisInput": {
    "documents": [
      {
        "id": "1",
        "language": "en",
        "text": "At Microsoft, we have been on a quest to advance AI beyond existing techniques, by taking a more holistic, human-centric approach to learning and understanding. As Chief Technology Officer of Foundry Tools, I have been working with a team of amazing scientists and engineers to turn this quest into a reality. In my role, I enjoy a unique perspective in viewing the relationship among three attributes of human cognition: monolingual text (X), audio or visual sensory signals, (Y) and multilingual (Z). At the intersection of all three, there's magic—what we call XYZ-code as illustrated in Figure 1—a joint representation to create more powerful AI that can speak, hear, see, and understand humans better. We believe XYZ-code enables us to fulfill our long-term vision: cross-domain transfer learning, spanning modalities and languages. The goal is to have pretrained models that can jointly learn representations to support a broad range of downstream AI tasks, much in the way humans do today. Over the past five years, we have achieved human performance on benchmarks in conversational speech recognition, machine translation, conversational question answering, machine reading comprehension, and image captioning. These five breakthroughs provided us with strong signals toward our more ambitious aspiration to produce a leap in AI capabilities, achieving multi-sensory and multilingual learning that is closer in line with how humans learn and understand. I believe the joint XYZ-code is a foundational component of this aspiration, if grounded with external knowledge sources in the downstream AI tasks."
      }
    ]
  },
"tasks": [
    {
      "kind": "AbstractiveSummarization",
      "taskName": "Query-based Abstractive Summarization",
      "parameters": {
          "query": "XYZ-code",
          "summaryLength": "short"
      }
    },    {
      "kind": "ExtractiveSummarization",
      "taskName": "Query_based Extractive Summarization",
      "parameters": {
          "query": "XYZ-code"
      }
    }
  ]
}
'
```

### Summary length control

#### Using the summaryLength parameter in abstractive summarization

If you don't specify `summaryLength`, the model determines the summary length.

For the `summaryLength` parameter, three values are accepted:

* `oneSentence`: Generates a summary of mostly one sentence, with around 80 tokens.
* `short`: Generates a summary of mostly two to three sentences, with around 120 tokens.
* `medium`: Generates a summary of mostly four to six sentences, with around 170 tokens.
* `long`: Generates a summary of mostly over seven sentences, with around 210 tokens.

Here's an example request:

```bash
curl -i -X POST https://<your-language-resource-endpoint>/language/analyze-text/jobs?api-version=2023-04-01 \
-H "Content-Type: application/json" \
-H "Ocp-Apim-Subscription-Key: <your-language-resource-key>" \
-d \
' 
{
  "displayName": "Text Abstractive Summarization Task Example",
  "analysisInput": {
    "documents": [
      {
        "id": "1",
        "language": "en",
        "text": "At Microsoft, we have been on a quest to advance AI beyond existing techniques, by taking a more holistic, human-centric approach to learning and understanding. As Chief Technology Officer of Foundry Tools, I have been working with a team of amazing scientists and engineers to turn this quest into a reality. In my role, I enjoy a unique perspective in viewing the relationship among three attributes of human cognition: monolingual text (X), audio or visual sensory signals, (Y) and multilingual (Z). At the intersection of all three, there's magic—what we call XYZ-code as illustrated in Figure 1—a joint representation to create more powerful AI that can speak, hear, see, and understand humans better. We believe XYZ-code enables us to fulfill our long-term vision: cross-domain transfer learning, spanning modalities and languages. The goal is to have pretrained models that can jointly learn representations to support a broad range of downstream AI tasks, much in the way humans do today. Over the past five years, we have achieved human performance on benchmarks in conversational speech recognition, machine translation, conversational question answering, machine reading comprehension, and image captioning. These five breakthroughs provided us with strong signals toward our more ambitious aspiration to produce a leap in AI capabilities, achieving multi-sensory and multilingual learning that is closer in line with how humans learn and understand. I believe the joint XYZ-code is a foundational component of this aspiration, if grounded with external knowledge sources in the downstream AI tasks."
      }
    ]
  },
  "tasks": [
    {
      "kind": "AbstractiveSummarization",
      "taskName": "Length controlled Abstractive Summarization",
          "parameters": {
          "summaryLength": "short"
      }
    }
  ]
}
'
```

#### Using the sentenceCount parameter in extractive summarization
For the `sentenceCount` parameter, enter a value from 1 to 20 to indicate the desired number of output sentences.

Here's an example request:

```bash
curl -i -X POST https://<your-language-resource-endpoint>/language/analyze-text/jobs?api-version=2023-11-15-preview \
-H "Content-Type: application/json" \
-H "Ocp-Apim-Subscription-Key: <your-language-resource-key>" \
-d \
' 
{
  "displayName": "Text Extractive Summarization Task Example",
  "analysisInput": {
    "documents": [
      {
        "id": "1",
        "language": "en",
        "text": "At Microsoft, we have been on a quest to advance AI beyond existing techniques, by taking a more holistic, human-centric approach to learning and understanding. As Chief Technology Officer of Foundry Tools, I have been working with a team of amazing scientists and engineers to turn this quest into a reality. In my role, I enjoy a unique perspective in viewing the relationship among three attributes of human cognition: monolingual text (X), audio or visual sensory signals, (Y) and multilingual (Z). At the intersection of all three, there's magic—what we call XYZ-code as illustrated in Figure 1—a joint representation to create more powerful AI that can speak, hear, see, and understand humans better. We believe XYZ-code enables us to fulfill our long-term vision: cross-domain transfer learning, spanning modalities and languages. The goal is to have pretrained models that can jointly learn representations to support a broad range of downstream AI tasks, much in the way humans do today. Over the past five years, we have achieved human performance on benchmarks in conversational speech recognition, machine translation, conversational question answering, machine reading comprehension, and image captioning. These five breakthroughs provided us with strong signals toward our more ambitious aspiration to produce a leap in AI capabilities, achieving multi-sensory and multilingual learning that is closer in line with how humans learn and understand. I believe the joint XYZ-code is a foundational component of this aspiration, if grounded with external knowledge sources in the downstream AI tasks."
      }
    ]
  },
"tasks": [
    {
      "kind": "ExtractiveSummarization",
      "taskName": "Length controlled Extractive Summarization",
      "parameters": {
          "sentenceCount": "5"
      }
    }
  ]
}
'
```

## Service and data limits

[!INCLUDE [service limits article](../../includes/service-limits-link.md)]

# [Conversation summarization](#tab/conversation-summarization)

[!INCLUDE [availability](../includes/regional-availability.md)]

## Conversation summarization aspects

- **Chapter title and narrative (general conversation)** summarize a conversation into chapter titles and a summary of the conversation's contents. This summarization aspect works on conversations with any number of parties. 

- **Issues and resolutions (call center focused)** summarize text chat logs between customers and customer-service agents. This feature provides both issues and resolutions present in these logs, which occur between two parties.

- **Narrative** summarizes the narrative of a conversation.

- **Recap** condenses lengthy meetings or conversations into a concise one-paragraph summary to provide a quick overview.

- **Follow-up tasks** summarizes action items and tasks that arise during a meeting.

:::image type="content" source="../media/conversation-summary-diagram.svg" alt-text="A diagram for sending data to the conversation summarization issues and resolution feature.":::

The service provides the AI models that the API uses. You just have to send content for analysis.

For easier navigation, here are links to the corresponding sections for each service:

|Aspect                 |Section                                               |
|-----------------------|------------------------------------------------------|
|Issue and Resolution   |[Issue and Resolution](#get-summaries-from-text-chats)|
|Chapter Title          |[Chapter Title](#get-chapter-titles)                  |
|Narrative              |[Narrative](#get-narrative-summarization)             |
|Recap and Follow-up    |[Recap and follow-up](#get-narrative-summarization)   |

## Features

The conversation summarization API uses natural language processing techniques to summarize conversations into shorter summaries per request. Conversation summarization can summarize for issues and resolutions discussed in a two-party conversation or summarize a long conversation into chapters and a short narrative for each chapter.

Another feature in Azure Language in Foundry Tools named [text summarization](../overview.md?tabs=text-summarization) is more suitable to summarize documents into concise summaries. When you're deciding between text summarization and conversation summarization, consider the following points:
* Input format: Conversation summarization can operate on both chat text and speech transcripts, which have speakers and their utterances. Text summarization operates using simple text, or Word, PDF, or PowerPoint formats.
* Purpose of summarization: For example, `conversation issue and resolution summarization` returns a reason and the resolution for a chat between a customer and a customer service agent.

## Submitting data

Submit documents to the API as strings of text. The API performs analysis when it receives the request. Because the API is [asynchronous](../../concepts/use-asynchronously.md), there might be a delay between sending an API request and receiving the results. For information on the size and number of requests you can send per minute and second, see the following data limits.

When you use this feature, the API results are available for 24 hours from the time the request was ingested, and is indicated in the response. After this time period, the results are purged and are no longer available for retrieval.

When you submit data to conversation summarization, we recommend sending one chat log per request, for better latency.

### Get summaries from text chats

You can use conversation issue and resolution summarization to get summaries as you need. To see an example using text chats, see the [quickstart article](../quickstart.md).

### Get summaries from speech transcriptions 

The `conversation issue and resolution summarization` also enables you to get summaries from speech transcripts by using the [Speech service's speech to text feature](../../../Speech-Service/call-center-overview.md). The following example shows a short conversation that you might include in your API requests.

```json
"conversations":[
   {
      "id":"abcdefgh-1234-1234-1234-1234abcdefgh",
      "language":"en",
      "modality":"transcript",
      "conversationItems":[
         {
            "modality":"transcript",
            "participantId":"speaker",
            "id":"12345678-abcd-efgh-1234-abcd123456",
            "content":{
               "text":"Hi.",
               "lexical":"hi",
               "itn":"hi",
               "maskedItn":"hi",
               "audioTimings":[
                  {
                     "word":"hi",
                     "offset":4500000,
                     "duration":2800000
                  }
               ]
            }
         }
      ]
   }
]
```

### Get chapter titles

Conversation chapter title summarization lets you get chapter titles from input conversations. A guided example scenario follows:

1. Copy the following command into a text editor. The BASH example uses the `\` line continuation character. If your console or terminal uses a different line continuation character, use that character.

```bash
curl -i -X POST https://<your-language-resource-endpoint>/language/analyze-conversations/jobs?api-version=2023-11-15-preview \
-H "Content-Type: application/json" \
-H "Ocp-Apim-Subscription-Key: <your-language-resource-key>" \
-d \
' 
{
  "displayName": "Conversation Task Example",
  "analysisInput": {
    "conversations": [
      {
        "conversationItems": [
          {
            "text": "Hello, you're chatting with Rene. How may I help you?",
            "id": "1",
            "role": "Agent",
            "participantId": "Agent_1"
          },
          {
            "text": "Hi, I tried to set up wifi connection for Smart Brew 300 espresso machine, but it didn't work.",
            "id": "2",
            "role": "Customer",
            "participantId": "Customer_1"
          },
          {
            "text": "I'm sorry to hear that. Let's see what we can do to fix this issue. Could you please try the following steps for me? First, could you push the wifi connection button, hold for 3 seconds, then let me know if the power light is slowly blinking on and off every second?",
            "id": "3",
            "role": "Agent",
            "participantId": "Agent_1"
          },
          {
            "text": "Yes, I pushed the wifi connection button, and now the power light is slowly blinking.",
            "id": "4",
            "role": "Customer",
            "participantId": "Customer_1"
          },
          {
            "text": "Great. Thank you! Now, please check in your Contoso Coffee app. Does it prompt to ask you to connect with the machine? ",
            "id": "5",
            "role": "Agent",
            "participantId": "Agent_1"
          },
          {
            "text": "No. Nothing happened.",
            "id": "6",
            "role": "Customer",
            "participantId": "Customer_1"
          },
          {
            "text": "I'm very sorry to hear that. Let me see if there's another way to fix the issue. Please hold on for a minute.",
            "id": "7",
            "role": "Agent",
            "participantId": "Agent_1"
          }
        ],
        "modality": "text",
        "id": "conversation1",
        "language": "en"
      }
    ]
  },
  "tasks": [
    {
      "taskName": "Conversation Task 1",
      "kind": "ConversationalSummarizationTask",
      "parameters": {
        "summaryAspects": [
          "chapterTitle"
        ]
      }
    }
  ]
}
'
```

2. Make the following changes in the command where needed:
    - Replace the value `your-value-language-key` with your key.
    - Replace the first part of the request URL `your-language-resource-endpoint` with your endpoint URL.

3. Open a command prompt window (for example: BASH).

4. Paste the command from the text editor into the command prompt window, then run the command.

5. Get the `operation-location` from the response header. The value looks similar to the following URL:

```http
https://<your-language-resource-endpoint>/language/analyze-conversations/jobs/12345678-1234-1234-1234-12345678?api-version=2023-11-15-preview
```

6. To get the results of the request, use the following cURL command. Be sure to replace `<my-job-id>` with the GUID value you received from the previous `operation-location` response header:

```curl
curl -X GET https://<your-language-resource-endpoint>/language/analyze-conversations/jobs/<my-job-id>?api-version=2023-11-15-preview \
-H "Content-Type: application/json" \
-H "Ocp-Apim-Subscription-Key: <your-language-resource-key>"
``` 

Example chapter title summarization JSON response:

```json
{
    "jobId": "b01af3b7-1870-460a-9e36-09af28d360a1",
    "lastUpdatedDateTime": "2023-11-15T18:24:26Z",
    "createdDateTime": "2023-11-15T18:24:23Z",
    "expirationDateTime": "2023-11-16T18:24:23Z",
    "status": "succeeded",
    "errors": [],
    "displayName": "Conversation Task Example",
    "tasks": {
        "completed": 1,
        "failed": 0,
        "inProgress": 0,
        "total": 1,
        "items": [
            {
                "kind": "conversationalSummarizationResults",
                "taskName": "Conversation Task 1",
                "lastUpdateDateTime": "2023-11-15T18:24:26.3433677Z",
                "status": "succeeded",
                "results": {
                    "conversations": [
                        {
                            "summaries": [
                                {
                                    "aspect": "chapterTitle",
                                    "text": "\"Discussing the Problem of Smart Blend 300 Espresso Machine's Wi-Fi Connectivity\"",
                                    "contexts": [
                                        {
                                            "conversationItemId": "1",
                                            "offset": 0,
                                            "length": 53
                                        },
                                        {
                                            "conversationItemId": "2",
                                            "offset": 0,
                                            "length": 94
                                        },
                                        {
                                            "conversationItemId": "3",
                                            "offset": 0,
                                            "length": 266
                                        },
                                        {
                                            "conversationItemId": "4",
                                            "offset": 0,
                                            "length": 85
                                        },
                                        {
                                            "conversationItemId": "5",
                                            "offset": 0,
                                            "length": 119
                                        },
                                        {
                                            "conversationItemId": "6",
                                            "offset": 0,
                                            "length": 21
                                        },
                                        {
                                            "conversationItemId": "7",
                                            "offset": 0,
                                            "length": 109
                                        }
                                    ]
                                }
                            ],
                            "id": "conversation1",
                            "warnings": []
                        }
                    ],
                    "errors": [],
                    "modelVersion": "latest"
                }
            }
        ]
    }
}
```
For long conversation, the model might segment it into multiple cohesive parts, and summarize each segment. There's also a lengthy `contexts` field for each summary, which tells from which range of the input conversation we generated the summary.

 ### Get narrative summarization

Conversation summarization also lets you get narrative summaries from input conversations. A guided example scenario is provided:

1. Copy the following command into a text editor. The BASH example uses the `\` line continuation character. If your console or terminal uses a different line continuation character, use that character.

```bash
curl -i -X POST https://<your-language-resource-endpoint>/language/analyze-conversations/jobs?api-version=2023-11-15-preview \
-H "Content-Type: application/json" \
-H "Ocp-Apim-Subscription-Key: <your-language-resource-key>" \
-d \
' 
{
  "displayName": "Conversation Task Example",
  "analysisInput": {
    "conversations": [
      {
        "conversationItems": [
          {
            "text": "Hello, you're chatting with Rene. How may I help you?",
            "id": "1",
            "role": "Agent",
            "participantId": "Agent_1"
          },
          {
            "text": "Hi, I tried to set up wifi connection for Smart Brew 300 espresso machine, but it didn't work.",
            "id": "2",
            "role": "Customer",
            "participantId": "Customer_1"
          },
          {
            "text": "I'm sorry to hear that. Let's see what we can do to fix this issue. Could you please try the following steps for me? First, could you push the wifi connection button, hold for 3 seconds, then let me know if the power light is slowly blinking on and off every second?",
            "id": "3",
            "role": "Agent",
            "participantId": "Agent_1"
          },
          {
            "text": "Yes, I pushed the wifi connection button, and now the power light is slowly blinking.",
            "id": "4",
            "role": "Customer",
            "participantId": "Customer_1"
          },
          {
            "text": "Great. Thank you! Now, please check in your Contoso Coffee app. Does it prompt to ask you to connect with the machine? ",
            "id": "5",
            "role": "Agent",
            "participantId": "Agent_1"
          },
          {
            "text": "No. Nothing happened.",
            "id": "6",
            "role": "Customer",
            "participantId": "Customer_1"
          },
          {
            "text": "I'm very sorry to hear that. Let me see if there's another way to fix the issue. Please hold on for a minute.",
            "id": "7",
            "role": "Agent",
            "participantId": "Agent_1"
          }
        ],
        "modality": "text",
        "id": "conversation1",
        "language": "en"
      }
    ]
  },
  "tasks": [
    {
      "taskName": "Conversation Task 1",
      "kind": "ConversationalSummarizationTask",
      "parameters": {
        "summaryAspects": [
          "narrative"
        ]
      }
    }
  ]
}
'
```

2. Make the following changes in the command where needed:
    - Replace the value `your-language-resource-key` with your key.
    - Replace the first part of the request URL `your-language-resource-endpoint` with your endpoint URL.

3. Open a command prompt window (for example: BASH).

4. Paste the command from the text editor into the command prompt window, then run the command.

5. Get the `operation-location` from the response header. The value looks similar to the following URL:

```http
https://<your-language-resource-endpoint>/language/analyze-conversations/jobs/12345678-1234-1234-1234-12345678?api-version=2023-11-15-preview
```

6. To get the results of a request, use the following cURL command. Be sure to replace `<my-job-id>` with the GUID value you received from the previous `operation-location` response header:

```curl
curl -X GET https://<your-language-resource-endpoint>/language/analyze-conversations/jobs/<my-job-id>?api-version=2023-11-15-preview \
-H "Content-Type: application/json" \
-H "Ocp-Apim-Subscription-Key: <your-language-resource-key>"
```

Example narrative summarization JSON response:

```json
{
  "jobId": "d874a98c-bf31-4ac5-8b94-5c236f786754",
  "lastUpdatedDateTime": "2022-09-29T17:36:42Z",
  "createdDateTime": "2022-09-29T17:36:39Z",
  "expirationDateTime": "2022-09-30T17:36:39Z",
  "status": "succeeded",
  "errors": [],
  "displayName": "Conversation Task Example",
  "tasks": {
    "completed": 1,
    "failed": 0,
    "inProgress": 0,
    "total": 1,
    "items": [
      {
        "kind": "conversationalSummarizationResults",
        "taskName": "Conversation Task 1",
        "lastUpdateDateTime": "2022-09-29T17:36:42.895694Z",
        "status": "succeeded",
        "results": {
          "conversations": [
            {
              "summaries": [
                {
                  "aspect": "narrative",
                  "text": "Agent_1 helps customer to set up wifi connection for Smart Brew 300 espresso machine.",
                  "contexts": [
                    { "conversationItemId": "1", "offset": 0, "length": 53 },
                    { "conversationItemId": "2", "offset": 0, "length": 94 },
                    { "conversationItemId": "3", "offset": 0, "length": 266 },
                    { "conversationItemId": "4", "offset": 0, "length": 85 },
                    { "conversationItemId": "5", "offset": 0, "length": 119 },
                    { "conversationItemId": "6", "offset": 0, "length": 21 },
                    { "conversationItemId": "7", "offset": 0, "length": 109 }
                  ]
                }
              ],
              "id": "conversation1",
              "warnings": []
            }
          ],
          "errors": [],
          "modelVersion": "latest"
        }
      }
    ]
  }
}
```

For long conversation, the model might segment it into multiple cohesive parts, and summarize each segment. There's also a lengthy `contexts` field for each summary, which tells from which range of the input conversation we generated the summary.

 ### Get recap and follow-up task summarization

Conversation summarization also lets you get recaps and follow-up tasks from input conversations. A guided example scenario is provided:

1. Copy the following command into a text editor. The BASH example uses the `\` line continuation character. If your console or terminal uses a different line continuation character, use that character.

```bash
curl -i -X POST https://<your-language-resource-endpoint>/language/analyze-conversations/jobs?api-version=2023-11-15-preview \
-H "Content-Type: application/json" \
-H "Ocp-Apim-Subscription-Key: <your-language-resource-key>" \
-d \
' 
{
  "displayName": "Conversation Task Example",
  "analysisInput": {
    "conversations": [
      {
        "conversationItems": [
          {
            "text": "Hello, you're chatting with Rene. How may I help you?",
            "id": "1",
            "role": "Agent",
            "participantId": "Agent_1"
          },
          {
            "text": "Hi, I tried to set up wifi connection for Smart Brew 300 espresso machine, but it didn't work.",
            "id": "2",
            "role": "Customer",
            "participantId": "Customer_1"
          },
          {
            "text": "I'm sorry to hear that. Let's see what we can do to fix this issue. Could you please try the following steps for me? First, could you push the wifi connection button, hold for 3 seconds, then let me know if the power light is slowly blinking on and off every second?",
            "id": "3",
            "role": "Agent",
            "participantId": "Agent_1"
          },
          {
            "text": "Yes, I pushed the wifi connection button, and now the power light is slowly blinking.",
            "id": "4",
            "role": "Customer",
            "participantId": "Customer_1"
          },
          {
            "text": "Great. Thank you! Now, please check in your Contoso Coffee app. Does it prompt to ask you to connect with the machine? ",
            "id": "5",
            "role": "Agent",
            "participantId": "Agent_1"
          },
          {
            "text": "No. Nothing happened.",
            "id": "6",
            "role": "Customer",
            "participantId": "Customer_1"
          },
          {
            "text": "I'm very sorry to hear that. Let me see if there's another way to fix the issue. Please hold on for a minute.",
            "id": "7",
            "role": "Agent",
            "participantId": "Agent_1"
          }
        ],
        "modality": "text",
        "id": "conversation1",
        "language": "en"
      }
    ]
  },
  "tasks": [
    {
      "taskName": "Conversation Task 1",
      "kind": "ConversationalSummarizationTask",
      "parameters": {
        "summaryAspects": [
          "recap",
          "follow-up tasks"
        ]
      }
    }
  ]
}
'
```

2. Make the following changes in the command where needed:
    - Replace the value `your-language-resource-key` with your key.
    - Replace the first part of the request URL `your-language-resource-endpoint` with your endpoint URL.

3. Open a command prompt window (for example: BASH).

4. Paste the command from the text editor into the command prompt window, then run the command.

5. Get the `operation-location` from the response header. The value looks similar to the following URL:

```http
https://<your-language-resource-endpoint>/language/analyze-conversations/jobs/12345678-1234-1234-1234-12345678?api-version=2023-11-15-preview
```

6. To get the results of a request, use the following cURL command. Be sure to replace `<my-job-id>` with the GUID value you received from the previous `operation-location` response header:

```curl
curl -X GET https://<your-language-resource-endpoint>/language/analyze-conversations/jobs/<my-job-id>?api-version=2023-11-15-preview \
-H "Content-Type: application/json" \
-H "Ocp-Apim-Subscription-Key: <your-language-resource-key>"
```

Example recap and follow-up summarization JSON response:

```json
{
    "jobId": "e585d097-c19a-466e-8f99-a9646e55b1f5",
    "lastUpdatedDateTime": "2023-11-15T18:19:56Z",
    "createdDateTime": "2023-11-15T18:19:53Z",
    "expirationDateTime": "2023-11-16T18:19:53Z",
    "status": "succeeded",
    "errors": [],
    "displayName": "Conversation Task Example",
    "tasks": {
        "completed": 1,
        "failed": 0,
        "inProgress": 0,
        "total": 1,
        "items": [
            {
                "kind": "conversationalSummarizationResults",
                "taskName": "Conversation Task 1",
                "lastUpdateDateTime": "2023-11-15T18:19:56.1801785Z",
                "status": "succeeded",
                "results": {
                    "conversations": [
                        {
                            "summaries": [
                                {
                                    "aspect": "recap",
                                    "text": "The customer contacted the service agent, Rene, regarding an issue with setting up a wifi connection for their Smart Brew 300 espresso machine. The agent guided the customer through several steps, including pushing the wifi connection button and checking if the power light was blinking. However, the customer reported that no prompts were received in the Contoso Coffee app to connect with the machine. The agent then decided to look for another solution.",
                                    "contexts": [
                                        {
                                            "conversationItemId": "1",
                                            "offset": 0,
                                            "length": 53
                                        },
                                        {
                                            "conversationItemId": "2",
                                            "offset": 0,
                                            "length": 94
                                        },
                                        {
                                            "conversationItemId": "3",
                                            "offset": 0,
                                            "length": 266
                                        },
                                        {
                                            "conversationItemId": "4",
                                            "offset": 0,
                                            "length": 85
                                        },
                                        {
                                            "conversationItemId": "5",
                                            "offset": 0,
                                            "length": 119
                                        },
                                        {
                                            "conversationItemId": "6",
                                            "offset": 0,
                                            "length": 21
                                        },
                                        {
                                            "conversationItemId": "7",
                                            "offset": 0,
                                            "length": 109
                                        }
                                    ]
                                },
                                {
                                    "aspect": "Follow-Up Tasks",
                                    "text": "@Agent_1 will ask the customer to push the wifi connection button, hold for 3 seconds, then check if the power light is slowly blinking on and off every second."
                                },
                                {
                                    "aspect": "Follow-Up Tasks",
                                    "text": "@Agent_1 will ask the customer to check in the Contoso Coffee app if it prompts to connect with the machine."
                                },
                                {
                                    "aspect": "Follow-Up Tasks",
                                    "text": "@Agent_1 will investigate another way to fix the issue."
                                }
                            ],
                            "id": "conversation1",
                            "warnings": []
                        }
                    ],
                    "errors": [],
                    "modelVersion": "latest"
                }
            }
        ]
    }
}
```

For long conversation, the model might segment it into multiple cohesive parts, and summarize each segment. There's also a lengthy `contexts` field for each summary, which tells from which range of the input conversation we generated the summary.

## Getting conversation issue and resolution summarization results

The following text is an example of content you might submit for conversation issue and resolution summarization. It's only an example. The API can accept longer input text. For more information, *see* [data limits](../../concepts/data-limits.md).
 
**Agent**: "*Hello, how can I help you*?"

**Customer**: "*How can I upgrade my Contoso subscription? I've been trying the entire day.*"

**Agent**: "*Press the upgrade button then sign in and follow the instructions.*"

Summarization is performed upon receipt of the request by creating a job for the API backend. If the job succeeded, the output of the API is returned. The output is available for retrieval for 24 hours. After this time, the output is purged. Due to multilingual and emoji support, the response might contain text offsets. For more information, *see* [how to process offsets](../../concepts/multilingual-emoji-support.md).

In the previous example, the API might return this summarized sentences output:

| Summarized text                                                           | Aspect     |
|---------------------------------------------------------------------------|------------|
| "Customer wants to upgrade their subscription. Customer doesn't know how."| issue      |
| "Customer needs to press upgrade button, and sign in."                    | resolution |

# [Document summarization (preview)](#tab/document-summarization)

> [!IMPORTANT]
>
> * Azure Language in Foundry Tools public preview releases provide early access to features that are in active development.
> * Features, approaches, and processes may change, before General Availability (GA), based on user feedback.

Language is a cloud-based service that applies Natural Language Processing (NLP) features to text-based data. Document summarization uses natural language processing to generate extractive (salient sentence extraction) or abstractive (contextual word extraction) summaries for documents. Both `AbstractiveSummarization` and `ExtractiveSummarization` APIs support native document processing. A native document refers to the file format used to create the original document such as Microsoft Word (docx) or a portable document file (pdf). Native document support eliminates the need for text preprocessing before using Language resource capabilities. The native document support capability enables you to send API requests asynchronously, using an HTTP POST request body to send your data and HTTP GET request query string to retrieve the status results. Your processed documents are located in your Azure Blob Storage target container.

## Supported document formats

 Applications use native file formats to create, save, or open native documents. Currently **PII** and **Document summarization** capabilities supports the following native document formats:

|File type|File extension|Description|
|---------|--------------|-----------|
|Text| `.txt`|An unformatted text document.|
|Adobe PDF| `.pdf`|A portable document file formatted document.|
|Microsoft Word| `.docx`|A Microsoft Word document file.|

## Input guidelines

***Supported file formats***

|Type|support and limitations|
|---|---|
|**PDFs**| Fully scanned PDFs aren't supported.|
|**Text within images**| Digital images with embedded text aren't supported.|
|**Digital tables**| Tables in scanned documents aren't supported.|

***Document Size***

|Attribute|Input limit|
|---|---|
|**Total number of documents per request** |**≤ 20**|
|**Total content size per request**| **≤ 10 MB**|

## Include native documents with an HTTP request

***Let's get started:***

* For this project, we use the cURL command-line tool to make REST API calls.

    > [!NOTE]
    > The cURL package is preinstalled on most Windows 10 and Windows 11 and most macOS and Linux distributions. You can check the package version with the following commands:
    > Windows: `curl.exe -V`
    > macOS `curl -V`
    > Linux: `curl --version`

* An active [**Azure account**](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn). If you don't have one, you can [**create a free account**](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

* An [**Azure Blob Storage account**](https://portal.azure.com/#create/Microsoft.StorageAccount-ARM). You also need to [create containers](#create-azure-blob-storage-containers) in your Azure Blob Storage account for your source and target files:

  * **Source container**. This container is where you upload your native files for analysis (required).
  * **Target container**. This container is where your analyzed files are stored (required).

* A [**single-service Language resource**](https://ms.portal.azure.com/#create/Microsoft.CognitiveServicesTextAnalytics) (**not** a multi-service Microsoft Foundry resource):

  **Complete Azure Language resource project and instance details fields as follows:**

  1. **Subscription**. Select one of your available Azure subscriptions.

  1. **Resource Group**. You can create a new resource group or add your resource to a preexisting resource group that shares the same lifecycle, permissions, and policies.

  1. **Resource Region**. Choose **Global** unless your business or application requires a specific region. If you're planning on using a [system-assigned managed identity](../../concepts/role-based-access-control.md) for authentication, choose a **geographic** region like **West US**.

  1. **Name**. Enter the name you chose for your resource. The name you choose must be unique within Azure.

  1. **Pricing tier**. You can use the free pricing tier (`Free F0`) to try the service, and upgrade later to a paid tier for production.

  1. Select **Review + Create**.

  1. Review the service terms and select **Create** to deploy your resource.

  1. After your resource successfully deploys, select **Go to resource**.

### Retrieve your key and Language endpoint

Requests to Azure Language require a read-only key and custom endpoint to authenticate access.

1. If you created a new resource, after it deploys, select **Go to resource**. If you have an existing Language resource, navigate directly to your resource page.

1. In the left rail, under *Resource Management*, select **Keys and Endpoint**.

1. You can copy and paste your **`key`** and your **`Language instance endpoint`** into the code samples to authenticate your request to Azure Language. Only one key is necessary to make an API call.

## Create Azure Blob Storage containers

[**Create containers**](/azure/storage/blobs/storage-quickstart-blobs-portal#create-a-container) in your [**Azure Blob Storage account**](https://portal.azure.com/#create/Microsoft.StorageAccount-ARM) for source and target files.

* **Source container**. This container is where you upload your native files for analysis (required).
* **Target container**. This container is where your analyzed files are stored (required).

### **Authentication**

Your Language resource needs granted access to your storage account before it can create, read, or delete blobs. There are two primary methods you can use to grant access to your storage data:

* [**Shared access signature (SAS) tokens**](../../native-document-support/shared-access-signatures.md). User delegation SAS tokens are secured with Microsoft Entra credentials. SAS tokens provide secure, delegated access to resources in your Azure storage account.

* [**Managed identity role-based access control (RBAC)**](../../native-document-support/managed-identities.md). Managed identities for Azure resources are service principals that create a Microsoft Entra identity and specific permissions for Azure managed resources.

For this project, we authenticate access to the `source location` and `target location` URLs with Shared Access Signature (SAS) tokens appended as query strings. Each token is assigned to a specific blob (file).

:::image type="content" source="../../native-document-support/media/sas-url-token.png" alt-text="Screenshot of a storage url with SAS token appended.":::

* Your **source** container or blob must designate **read** and **list** access.
* Your **target** container or blob must designate **write** and **list** access.

The extractive summarization API uses natural language processing techniques to locate key sentences in an unstructured text document. These sentences collectively convey the main idea of the document.

Extractive summarization returns a rank score as a part of the system response along with extracted sentences and their position in the original documents. A rank score is an indicator of how relevant a sentence is determined to be, to the main idea of a document. The model gives a score between 0 and 1 (inclusive) to each sentence and returns the highest scored sentences per request. For example, if you request a three-sentence summary, the service returns the three highest scored sentences.

There's another feature in Language, [key phrase extraction](./../../key-phrase-extraction/how-to/call-api.md), that can extract key information. To decide between key phrase extraction and extractive summarization, here are helpful considerations:

* Key phrase extraction returns phrases while extractive summarization returns sentences.
* Extractive summarization returns sentences together with a rank score, and top ranked sentences are returned per request.
* Extractive summarization also returns the following positional information:
    * Offset: The start position of each extracted sentence.
    * Length: The length of each extracted sentence.

## Determine how to process the data (optional)

### Submitting data

You submit documents to the API as strings of text. Analysis is performed upon receipt of the request. Because the API is [asynchronous](../../concepts/use-asynchronously.md), there might be a delay between sending an API request, and receiving the results.

When you use this feature, the API results are available for 24 hours from the time the request was ingested, and is indicated in the response. After this time period, the results are purged and are no longer available for retrieval.

### Getting text summarization results

When you get results from language detection, you can stream the results to an application or save the output to a file on the local system.

Here's an example of content you might submit for summarization, which is extracted using the Microsoft blog article [A holistic representation toward integrative AI](https://www.microsoft.com/research/blog/a-holistic-representation-toward-integrative-ai/). This article is only an example. The API can accept longer input text. For more information, *see* [data and service limits](../overview.md#input-requirements-and-service-limits).
 
*"At Microsoft, we are on a quest to advance AI beyond existing techniques, by taking a more holistic, human-centric approach to learning and understanding. As Chief Technology Officer of Foundry Tools, I have been working with a team of amazing scientists and engineers to turn this quest into a reality. In my role, I enjoy a unique perspective in viewing the relationship among three attributes of human cognition: monolingual text (X), audio or visual sensory signals, (Y) and multilingual (Z). At the intersection of all three, there's magic—what we call XYZ-code as illustrated in Figure 1—a joint representation to create more powerful AI that can speak, hear, see, and understand humans better. We believe XYZ-code enables us to fulfill our long-term vision: cross-domain transfer learning, spanning modalities and languages. The goal is to have pretrained models that can jointly learn representations to support a broad range of downstream AI tasks, much in the way humans do today. Over the past five years, we achieved human performance on benchmarks in conversational speech recognition, machine translation, conversational question answering, machine reading comprehension, and image captioning. These five breakthroughs provided us with strong signals toward our more ambitious aspiration to produce a leap in AI capabilities, achieving multi-sensory and multilingual learning that is closer in line with how humans learn and understand. I believe the joint XYZ-code is a foundational component of this aspiration, if grounded with external knowledge sources in the downstream AI tasks."*

The text summarization API request is processed upon receipt of the request by creating a job for the API backend. If the job succeeded, the output of the API is returned. The output is available for retrieval for 24 hours. After this time, the output is purged. Due to multilingual and emoji support, the response might contain text offsets. For more information, *see* [how to process offsets](../../concepts/multilingual-emoji-support.md).

When you use the preceding example, the API might return these summarized sentences:

**Extractive summarization**:

* "At Microsoft, we are on a quest to advance AI beyond existing techniques, by taking a more holistic, human-centric approach to learning and understanding."
* "We believe XYZ-code enables us to fulfill our long-term vision: cross-domain transfer learning, spanning modalities and languages."
* "The goal is to have pretrained models that can jointly learn representations to support a broad range of downstream AI tasks, much in the way humans do today."

**Abstractive summarization**:
- "Microsoft is taking a more holistic, human-centric approach to learning and understanding. We believe XYZ-code enables us to fulfill our long-term vision: cross-domain transfer learning, spanning modalities and languages. Over the past five years, we achieved human performance on benchmarks in."

### Try text extractive summarization

You can use text extractive summarization to get summaries of articles, papers, or documents. To see an example, see the [quickstart article](../quickstart.md).

You can use the `sentenceCount` parameter to guide how many sentences are returned, with `3` being the default. The range is from 1 to 20.

You can also use the `sortby` parameter to specify in what order the extracted sentences are returned - either `Offset` or `Rank`, with `Offset` being the default. 

|parameter value  |Description  |
|---------|---------|
|Rank    | Order sentences according to their relevance to the input document, as decided by the service.        |
|Offset    | Keeps the original order in which the sentences appear in the input document.        |

### Try text abstractive summarization

The following example gets you started with text abstractive summarization:

1. Copy the following command into a text editor. The BASH example uses the `\` line continuation character. If your console or terminal uses a different line continuation character, use that character instead.

```bash
curl -i -X POST https://<your-language-resource-endpoint>/language/analyze-text/jobs?api-version=2023-04-01 \
-H "Content-Type: application/json" \
-H "Ocp-Apim-Subscription-Key: <your-language-resource-key>" \
-d \
' 
{
  "displayName": "Text Abstractive Summarization Task Example",
  "analysisInput": {
    "documents": [
      {
        "id": "1",
        "language": "en",
        "text": "At Microsoft, we have been on a quest to advance AI beyond existing techniques, by taking a more holistic, human-centric approach to learning and understanding. As Chief Technology Officer of Foundry Tools, I have been working with a team of amazing scientists and engineers to turn this quest into a reality. In my role, I enjoy a unique perspective in viewing the relationship among three attributes of human cognition: monolingual text (X), audio or visual sensory signals, (Y) and multilingual (Z). At the intersection of all three, there's magic—what we call XYZ-code as illustrated in Figure 1—a joint representation to create more powerful AI that can speak, hear, see, and understand humans better. We believe XYZ-code enables us to fulfill our long-term vision: cross-domain transfer learning, spanning modalities and languages. The goal is to have pretrained models that can jointly learn representations to support a broad range of downstream AI tasks, much in the way humans do today. Over the past five years, we have achieved human performance on benchmarks in conversational speech recognition, machine translation, conversational question answering, machine reading comprehension, and image captioning. These five breakthroughs provided us with strong signals toward our more ambitious aspiration to produce a leap in AI capabilities, achieving multi-sensory and multilingual learning that is closer in line with how humans learn and understand. I believe the joint XYZ-code is a foundational component of this aspiration, if grounded with external knowledge sources in the downstream AI tasks."
      }
    ]
  },
  "tasks": [
    {
      "kind": "AbstractiveSummarization",
      "taskName": "Text Abstractive Summarization Task 1",
    }
  ]
}
'
```

2. Make the following changes in the command where needed:
    - Replace the value `your-language-resource-key` with your key.
    - Replace the first part of the request URL `your-language-resource-endpoint` with your endpoint URL.

3. Open a command prompt window (for example: BASH).

4. Paste the command from the text editor into the command prompt window, then run the command.

5. Get the `operation-location` from the response header. The value looks similar to the following URL:

```http
https://<your-language-resource-endpoint>/language/analyze-text/jobs/12345678-1234-1234-1234-12345678?api-version=2022-10-01-preview
```

6. To get the results of the request, use the following cURL command. Be sure to replace `<my-job-id>` with the numerical ID value you received from the previous `operation-location` response header:

```bash
curl -X GET https://<your-language-resource-endpoint>/language/analyze-text/jobs/<my-job-id>?api-version=2022-10-01-preview \
-H "Content-Type: application/json" \
-H "Ocp-Apim-Subscription-Key: <your-language-resource-key>"
```

### Abstractive text summarization example JSON response

```json
{
    "jobId": "cd6418fe-db86-4350-aec1-f0d7c91442a6",
    "lastUpdateDateTime": "2022-09-08T16:45:14Z",
    "createdDateTime": "2022-09-08T16:44:53Z",
    "expirationDateTime": "2022-09-09T16:44:53Z",
    "status": "succeeded",
    "errors": [],
    "displayName": "Text Abstractive Summarization Task Example",
    "tasks": {
        "completed": 1,
        "failed": 0,
        "inProgress": 0,
        "total": 1,
        "items": [
            {
                "kind": "AbstractiveSummarizationLROResults",
                "taskName": "Text Abstractive Summarization Task 1",
                "lastUpdateDateTime": "2022-09-08T16:45:14.0717206Z",
                "status": "succeeded",
                "results": {
                    "documents": [
                        {
                            "summaries": [
                                {
                                    "text": "Microsoft is taking a more holistic, human-centric approach to AI. We've developed a joint representation to create more powerful AI that can speak, hear, see, and understand humans better. We've achieved human performance on benchmarks in conversational speech recognition, machine translation, ...... and image captions.",
                                    "contexts": [
                                        {
                                            "offset": 0,
                                            "length": 247
                                        }
                                    ]
                                }
                            ],
                            "id": "1"
                        }
                    ],
                    "errors": [],
                    "modelVersion": "latest"
                }
            }
        ]
    }
}
```

|parameter  |Description  |
|---------|---------|
|`-X POST <endpoint>`     | Specifies your Language resource endpoint for accessing the API.        |
|`--header Content-Type: application/json`     | The content type for sending JSON data.          |
|`--header "Ocp-Apim-Subscription-Key:<key>`    | Specifies Azure Language resource key for accessing the API.        |
|`-data`     | The JSON file containing the data you want to pass with your request.         |

The following cURL commands are executed from a BASH shell. Edit these commands with your own resource name, resource key, and JSON values. Try analyzing native documents by selecting the `Personally Identifiable Information (PII)` or `Document Summarization` code sample project:

### Summarization sample document

For this project, you need a **source document** uploaded to your **source container**. You can download our [Microsoft Word sample document](https://raw.githubusercontent.com/Azure-Samples/cognitive-services-REST-api-samples/master/curl/Language/native-document-summarization.docx) or [Adobe PDF](https://raw.githubusercontent.com/Azure-Samples/cognitive-services-REST-api-samples/master/curl/Language/native-document-summarization.pdf) for this quickstart. The source language is English.

### Build the POST request

1. Using your preferred editor or IDE, create a new directory for your app named `native-document`.
1. Create a new json file called **document-summarization.json** in your **native-document** directory.

1. Copy and paste the Document Summarization **request sample** into your `document-summarization.json` file. Replace **`{your-source-container-SAS-URL}`** and **`{your-target-container-SAS-URL}`** with values from your Azure portal Storage account containers instance:

  ***Request sample***

```json
  {
  "tasks": [
    {
      "kind": "ExtractiveSummarization",
      "parameters": {
        "sentenceCount": 6
      }
    }
  ],
  "analysisInput": {
    "documents": [
      {
        "source": {
          "location": "{your-source-blob-SAS-URL}"
        },
        "targets": {
          "location": "{your-target-container-SAS-URL}"
        }
      }
    ]
  }
}

```

### Run the POST request

Before you run the **POST** request, replace `{your-language-resource-endpoint}` and `{your-key}` with the endpoint value from your Azure portal Language resource instance.

  > [!IMPORTANT]
  > Remember to remove the key from your code when you're done, and never post it publicly. For production, use a secure way of storing and accessing your credentials like [Azure Key Vault](/azure/key-vault/general/overview). For more information, *see* Foundry Tools [security](/azure/ai-services/security-features).

  ***PowerShell***

  ```powershell
   cmd /c curl "{your-language-resource-endpoint}/language/analyze-documents/jobs?api-version=2024-11-15-preview" -i -X POST --header "Content-Type: application/json" --header "Ocp-Apim-Subscription-Key: {your-key}" --data "@document-summarization.json"
  ```

  ***command prompt / terminal***

  ```bash
  curl -v -X POST "{your-language-resource-endpoint}/language/analyze-documents/jobs?api-version=2024-11-15-preview" --header "Content-Type: application/json" --header "Ocp-Apim-Subscription-Key: {your-key}" --data "@document-summarization.json"
  ```

#### Sample response:

   ```http
   HTTP/1.1 202 Accepted
   Content-Length: 0
   operation-location: https://{your-language-resource-endpoint}/language/analyze-documents/jobs/f1cc29ff-9738-42ea-afa5-98d2d3cabf94?api-version=2024-11-15-preview
   apim-request-id: e7d6fa0c-0efd-416a-8b1e-1cd9287f5f81
   x-ms-region: West US 2
   Date: Thu, 25 Jan 2024 15:12:32 GMT
   ```

### POST response (jobId)

You receive a 202 (Success) response that includes a read-only Operation-Location header. The value of this header contains a jobId that can be queried to get the status of the asynchronous operation and retrieve the results using a GET request:

  :::image type="content" source="../../native-document-support/media/operation-location-result-id.png" alt-text="Screenshot showing the operation-location value in the POST response.":::

## Get analyze results (GET request)

1. After your successful **POST** request, poll the operation-location header returned in the POST request to view the processed data.

1. Here's the structure of the **GET** request:

   ```bash
   GET {cognitive-service-endpoint}/language/analyze-documents/jobs/{jobId}?api-version=2024-11-15-preview
   ```

1. Before you run the command, make these changes:

    * Replace {**jobId**} with the Operation-Location header from the POST response.

    * Replace {**your-language-resource-endpoint**} and {**your-key**} with the values from your Language instance in the Azure portal.

## Get request

```powershell
    cmd /c curl "{your-language-resource-endpoint}/language/analyze-documents/jobs/{jobId}?api-version=2024-11-15-preview" -i -X GET --header "Content-Type: application/json" --header "Ocp-Apim-Subscription-Key: {your-key}"
```

```bash
    curl -v -X GET "{your-language-resource-endpoint}/language/analyze-documents/jobs/{jobId}?api-version=2024-11-15-preview" --header "Content-Type: application/json" --header "Ocp-Apim-Subscription-Key: {your-key}"
```

#### Examine the response

You receive a 200 (Success) response with JSON output. The **status** field indicates the result of the operation. If the operation isn't complete, the value of **status** is "running" or "notStarted", and you should call the API again, either manually or through a script. We recommend an interval of one second or more between calls.

#### Sample response

```json
{
  "jobId": "f1cc29ff-9738-42ea-afa5-98d2d3cabf94",
  "lastUpdatedDateTime": "2024-01-24T13:17:58Z",
  "createdDateTime": "2024-01-24T13:17:47Z",
  "expirationDateTime": "2024-01-25T13:17:47Z",
  "status": "succeeded",
  "errors": [],
  "tasks": {
    "completed": 1,
    "failed": 0,
    "inProgress": 0,
    "total": 1,
    "items": [
      {
        "kind": "ExtractiveSummarizationLROResults",
        "lastUpdateDateTime": "2024-01-24T13:17:58.33934Z",
        "status": "succeeded",
        "results": {
          "documents": [
            {
              "id": "doc_0",
              "source": {
                "kind": "AzureBlob",
                "location": "https://myaccount.blob.core.windows.net/sample-input/input.pdf"
              },
              "targets": [
                {
                  "kind": "AzureBlob",
                  "location": "https://myaccount.blob.core.windows.net/sample-output/df6611a3-fe74-44f8-b8d4-58ac7491cb13/ExtractiveSummarization-0001/input.result.json"
                }
              ],
              "warnings": []
            }
          ],
          "errors": [],
          "modelVersion": "2023-02-01-preview"
        }
      }
    ]
  }
}
```

***Upon successful completion***:

* The analyzed documents can be found in your target container.
* The successful POST method returns a `202 Accepted` response code indicating that the service created the batch request.
* The POST request also returned response headers including `Operation-Location` that provides a value used in subsequent GET requests.

## Clean up resources

To clean up and remove an Azure AI resource, you can delete either the individual resource or the entire resource group. If you delete the resource group, all resources contained within are also deleted.

* [Azure portal](../../../multi-service-resource.md?pivots=azportal#clean-up-resources)
* [Azure CLI](../../../multi-service-resource.md?pivots=azcli#clean-up-resources)

---

## See also

* [Summarization overview](../overview.md)
