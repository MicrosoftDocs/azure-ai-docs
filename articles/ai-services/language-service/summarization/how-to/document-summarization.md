---
title: Summarize text with the extractive summarization API
titleSuffix: Azure AI services
description: This article shows you how to summarize text with the extractive summarization API.
#services: cognitive-services
author: jboback
manager: nitinme
ms.service: azure-ai-language
ms.topic: how-to
ms.date: 10/21/2024
ms.author: jboback
ms.custom:
  - language-service-summarization
  - ignite-2023
  - build-2024
---

# How to use text summarization

Text summarization is designed to shorten content that users consider too long to read. Both extractive and abstractive summarization condense articles, papers, or documents to key sentences.

**Extractive summarization**: Produces a summary by extracting sentences that collectively represent the most important or relevant information within the original content.

**Abstractive summarization**: Produces a summary by generating summarized sentences from the document that capture the main idea.

**Query-focused summarization**: Allows you to use a query when summarizing.

Each of these capabilities are able to summarize around specific items of interest when specified.

The AI models used by the API are provided by the service, you just have to send content for analysis.

For easier navigation, here are links to the corresponding sections for each service:

|Aspect       |Section                                                            |
|-------------|-------------------------------------------------------------------|
|Extractive   |[Extractive Summarization](#try-text-extractive-summarization) |
|Abstractive  |[Abstractive Summarization](#try-text-abstractive-summarization)|
|Query-focused|[Query-focused Summarization](#query-based-summarization)          |


## Features

> [!TIP]
> If you want to start using these features, you can follow the [quickstart article](../quickstart.md) to get started. You can also make example requests using [Language Studio](../../language-studio.md) without needing to write code.

The extractive summarization API uses natural language processing techniques to locate key sentences in an unstructured text document. These sentences collectively convey the main idea of the document.

Extractive summarization returns a rank score as a part of the system response along with extracted sentences and their position in the original documents. A rank score is an indicator of how relevant a sentence is determined to be, to the main idea of a document. The model gives a score between 0 and 1 (inclusive) to each sentence and returns the highest scored sentences per request. For example, if you request a three-sentence summary, the service returns the three highest scored sentences.

There's another feature in Azure AI Language, [key phrase extraction](./../../key-phrase-extraction/how-to/call-api.md), that can extract key information. When deciding between key phrase extraction and extractive summarization, consider the following:
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

The following is an example of content you might submit for summarization, which is extracted using the Microsoft blog article [A holistic representation toward integrative AI](https://www.microsoft.com/research/blog/a-holistic-representation-toward-integrative-ai/). This article is only an example, the API can accept longer input text. See the data limits section for more information.
 
*"At Microsoft, we have been on a quest to advance AI beyond existing techniques, by taking a more holistic, human-centric approach to learning and understanding. As Chief Technology Officer of Azure AI services, I have been working with a team of amazing scientists and engineers to turn this quest into a reality. In my role, I enjoy a unique perspective in viewing the relationship among three attributes of human cognition: monolingual text (X), audio or visual sensory signals, (Y) and multilingual (Z). At the intersection of all three, there’s magic—what we call XYZ-code as illustrated in Figure 1—a joint representation to create more powerful AI that can speak, hear, see, and understand humans better. We believe XYZ-code enables us to fulfill our long-term vision: cross-domain transfer learning, spanning modalities and languages. The goal is to have pretrained models that can jointly learn representations to support a broad range of downstream AI tasks, much in the way humans do today. Over the past five years, we have achieved human performance on benchmarks in conversational speech recognition, machine translation, conversational question answering, machine reading comprehension, and image captioning. These five breakthroughs provided us with strong signals toward our more ambitious aspiration to produce a leap in AI capabilities, achieving multi-sensory and multilingual learning that is closer in line with how humans learn and understand. I believe the joint XYZ-code is a foundational component of this aspiration, if grounded with external knowledge sources in the downstream AI tasks."*

The text summarization API request is processed upon receipt of the request by creating a job for the API backend. If the job succeeded, the output of the API is returned. The output is available for retrieval for 24 hours. After this time, the output is purged. Due to multilingual and emoji support, the response might contain text offsets. See [how to process offsets](../../concepts/multilingual-emoji-support.md) for more information.

When you use the above example, the API might return the following summarized sentences:

**Extractive summarization**:
- "At Microsoft, we have been on a quest to advance AI beyond existing techniques, by taking a more holistic, human-centric approach to learning and understanding."
- "We believe XYZ-code enables us to fulfill our long-term vision: cross-domain transfer learning, spanning modalities and languages."
- "The goal is to have pretrained models that can jointly learn representations to support a broad range of downstream AI tasks, much in the way humans do today."

**Abstractive summarization**:
- "Microsoft is taking a more holistic, human-centric approach to learning and understanding. We believe XYZ-code enables us to fulfill our long-term vision: cross-domain transfer learning, spanning modalities and languages. Over the past five years, we have achieved human performance on benchmarks in."

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

1. Copy the command below into a text editor. The BASH example uses the `\` line continuation character. If your console or terminal uses a different line continuation character, use that character instead.

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
        "text": "At Microsoft, we have been on a quest to advance AI beyond existing techniques, by taking a more holistic, human-centric approach to learning and understanding. As Chief Technology Officer of Azure AI services, I have been working with a team of amazing scientists and engineers to turn this quest into a reality. In my role, I enjoy a unique perspective in viewing the relationship among three attributes of human cognition: monolingual text (X), audio or visual sensory signals, (Y) and multilingual (Z). At the intersection of all three, there’s magic—what we call XYZ-code as illustrated in Figure 1—a joint representation to create more powerful AI that can speak, hear, see, and understand humans better. We believe XYZ-code enables us to fulfill our long-term vision: cross-domain transfer learning, spanning modalities and languages. The goal is to have pretrained models that can jointly learn representations to support a broad range of downstream AI tasks, much in the way humans do today. Over the past five years, we have achieved human performance on benchmarks in conversational speech recognition, machine translation, conversational question answering, machine reading comprehension, and image captioning. These five breakthroughs provided us with strong signals toward our more ambitious aspiration to produce a leap in AI capabilities, achieving multi-sensory and multilingual learning that is closer in line with how humans learn and understand. I believe the joint XYZ-code is a foundational component of this aspiration, if grounded with external knowledge sources in the downstream AI tasks."
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
|`-X POST <endpoint>`     | Specifies your endpoint for accessing the API.        |
|`-H Content-Type: application/json`     | The content type for sending JSON data.          |
|`-H "Ocp-Apim-Subscription-Key:<key>`    | Specifies the key for accessing the API.        |
|`-d <documents>`     | The JSON containing the documents you want to send.         |

The following cURL commands are executed from a BASH shell. Edit these commands with your own resource name, resource key, and JSON values.

## Query based summarization

The query-based text summarization API is an extension to the existing text summarization API.

The biggest difference is a new `query` field in the request body (under `tasks` > `parameters` > `query`).

> [!TIP]
> Query based summarization has some differentiation in the utilization of length control based on the type of query based summarization you're using:
> - Query based extractive summarization supports length control by specifying sentenceCount.
> - Query based abstractive summarization doesn't support length control.

Below is an example request:

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
        "text": "At Microsoft, we have been on a quest to advance AI beyond existing techniques, by taking a more holistic, human-centric approach to learning and understanding. As Chief Technology Officer of Azure AI services, I have been working with a team of amazing scientists and engineers to turn this quest into a reality. In my role, I enjoy a unique perspective in viewing the relationship among three attributes of human cognition: monolingual text (X), audio or visual sensory signals, (Y) and multilingual (Z). At the intersection of all three, there’s magic—what we call XYZ-code as illustrated in Figure 1—a joint representation to create more powerful AI that can speak, hear, see, and understand humans better. We believe XYZ-code enables us to fulfill our long-term vision: cross-domain transfer learning, spanning modalities and languages. The goal is to have pretrained models that can jointly learn representations to support a broad range of downstream AI tasks, much in the way humans do today. Over the past five years, we have achieved human performance on benchmarks in conversational speech recognition, machine translation, conversational question answering, machine reading comprehension, and image captioning. These five breakthroughs provided us with strong signals toward our more ambitious aspiration to produce a leap in AI capabilities, achieving multi-sensory and multilingual learning that is closer in line with how humans learn and understand. I believe the joint XYZ-code is a foundational component of this aspiration, if grounded with external knowledge sources in the downstream AI tasks."
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
* oneSentence: Generates a summary of mostly 1 sentence, with around 80 tokens.
* short: Generates a summary of mostly 2-3 sentences, with around 120 tokens.
* medium: Generates a summary of mostly 4-6 sentences, with around 170 tokens.
* long: Generates a summary of mostly over 7 sentences, with around 210 tokens.

Below is an example request:

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
        "text": "At Microsoft, we have been on a quest to advance AI beyond existing techniques, by taking a more holistic, human-centric approach to learning and understanding. As Chief Technology Officer of Azure AI services, I have been working with a team of amazing scientists and engineers to turn this quest into a reality. In my role, I enjoy a unique perspective in viewing the relationship among three attributes of human cognition: monolingual text (X), audio or visual sensory signals, (Y) and multilingual (Z). At the intersection of all three, there’s magic—what we call XYZ-code as illustrated in Figure 1—a joint representation to create more powerful AI that can speak, hear, see, and understand humans better. We believe XYZ-code enables us to fulfill our long-term vision: cross-domain transfer learning, spanning modalities and languages. The goal is to have pretrained models that can jointly learn representations to support a broad range of downstream AI tasks, much in the way humans do today. Over the past five years, we have achieved human performance on benchmarks in conversational speech recognition, machine translation, conversational question answering, machine reading comprehension, and image captioning. These five breakthroughs provided us with strong signals toward our more ambitious aspiration to produce a leap in AI capabilities, achieving multi-sensory and multilingual learning that is closer in line with how humans learn and understand. I believe the joint XYZ-code is a foundational component of this aspiration, if grounded with external knowledge sources in the downstream AI tasks."
      }
    ]
  },
  "tasks": [
    {
      "kind": "AbstractiveSummarization",
      "taskName": "Length controlled Abstractive Summarization",
          "parameters": {
          "sentenceLength": "short"
      }
    }
  ]
}
'
```

#### Using the sentenceCount parameter in extractive summarization
For the `sentenceCount` parameter, you can input a value 1-20 to indicate the desired number of output sentences.

Below is an example request:

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
        "text": "At Microsoft, we have been on a quest to advance AI beyond existing techniques, by taking a more holistic, human-centric approach to learning and understanding. As Chief Technology Officer of Azure AI services, I have been working with a team of amazing scientists and engineers to turn this quest into a reality. In my role, I enjoy a unique perspective in viewing the relationship among three attributes of human cognition: monolingual text (X), audio or visual sensory signals, (Y) and multilingual (Z). At the intersection of all three, there’s magic—what we call XYZ-code as illustrated in Figure 1—a joint representation to create more powerful AI that can speak, hear, see, and understand humans better. We believe XYZ-code enables us to fulfill our long-term vision: cross-domain transfer learning, spanning modalities and languages. The goal is to have pretrained models that can jointly learn representations to support a broad range of downstream AI tasks, much in the way humans do today. Over the past five years, we have achieved human performance on benchmarks in conversational speech recognition, machine translation, conversational question answering, machine reading comprehension, and image captioning. These five breakthroughs provided us with strong signals toward our more ambitious aspiration to produce a leap in AI capabilities, achieving multi-sensory and multilingual learning that is closer in line with how humans learn and understand. I believe the joint XYZ-code is a foundational component of this aspiration, if grounded with external knowledge sources in the downstream AI tasks."
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

## See also

* [Summarization overview](../overview.md)
