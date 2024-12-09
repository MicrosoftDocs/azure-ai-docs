---
title: Summarize text with the conversation summarization API
titleSuffix: Azure AI services
description: This article shows you how to summarize chat logs with the conversation summarization API.
#services: cognitive-services
author: jboback
manager: nitinme
ms.service: azure-ai-language
ms.topic: how-to
ms.date: 11/21/2024
ms.author: jboback
ms.custom:
  - language-service-summarization
  - ignite-2023
  - build-2024
---

# How to use conversation summarization

[!INCLUDE [availability](../includes/regional-availability.md)]

## Conversation summarization aspects

- Chapter title and narrative (general conversation) are designed to summarize a conversation into chapter titles, and a summarization of the conversation's contents. This summarization aspect works on conversations with any number of parties. 

- Issue and resolution (call center focused) is designed to summarize text chat logs between customers and customer-service agents. This feature is capable of providing both issues and resolutions present in these logs, which occur between two parties.

- Narrative is designed to summarize the narrative of a conversation.

- Recap is designed to condense lengthy meetings or conversations into a concise one-paragraph summary to provide a quick overview.

- Follow-up tasks is designed to summarize action items and tasks that arise during a meeting.

:::image type="content" source="../media/conversation-summary-diagram.svg" alt-text="A diagram for sending data to the conversation summarization issues and resolution feature.":::

The AI models used by the API are provided by the service, you just have to send content for analysis.

For easier navigation, here are links to the corresponding sections for each service:

|Aspect                 |Section                                               |
|-----------------------|------------------------------------------------------|
|Issue and Resolution   |[Issue and Resolution](#get-summaries-from-text-chats)|
|Chapter Title          |[Chapter Title](#get-chapter-titles)                  |
|Narrative              |[Narrative](#get-narrative-summarization)             |
|Recap and Follow-up    |[Recap and follow-up](#get-narrative-summarization)   |

## Features

The conversation summarization API uses natural language processing techniques to summarize conversations into shorter summaries per request. Conversation summarization can summarize for issues and resolutions discussed in a two-party conversation or summarize a long conversation into chapters and a short narrative for each chapter.

There's another feature in Azure AI Language named [text summarization](../overview.md?tabs=text-summarization) that is more suitable to summarize documents into concise summaries. When you're deciding between text summarization and conversation summarization, consider the following points:
* Input format: Conversation summarization can operate on both chat text and speech transcripts, which have speakers and their utterances. Text summarization operates using simple text, or Word, PDF, or PowerPoint formats.
* Purpose of summarization: for example, conversation issue and resolution summarization returns a reason and the resolution for a chat between a customer and a customer service agent.

## Submitting data

> [!NOTE]
> See the [Language Studio](../../language-studio.md#valid-text-formats-for-conversation-features) article for information on formatting conversational text to submit using Language Studio. 

You submit documents to the API as strings of text. Analysis is performed upon receipt of the request. Because the API is [asynchronous](../../concepts/use-asynchronously.md), there might be a delay between sending an API request and receiving the results.  For information on the size and number of requests you can send per minute and second, see the data limits below.

When you use this feature, the API results are available for 24 hours from the time the request was ingested, and is indicated in the response. After this time period, the results are purged and are no longer available for retrieval.

When you submit data to conversation summarization, we recommend sending one chat log per request, for better latency.

### Get summaries from text chats

You can use conversation issue and resolution summarization to get summaries as you need. To see an example using text chats, see the [quickstart article](../quickstart.md).

### Get summaries from speech transcriptions 

Conversation issue and resolution summarization also enables you to get summaries from speech transcripts by using the [Speech service's speech to text feature](../../../Speech-Service/call-center-overview.md). The following example shows a short conversation that you might include in your API requests.

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

Conversation chapter title summarization lets you get chapter titles from input conversations. A guided example scenario is provided below:

1. Copy the command below into a text editor. The BASH example uses the `\` line continuation character. If your console or terminal uses a different line continuation character, use that character.

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
            "text": "Hello, you’re chatting with Rene. How may I help you?",
            "id": "1",
            "role": "Agent",
            "participantId": "Agent_1"
          },
          {
            "text": "Hi, I tried to set up wifi connection for Smart Brew 300 espresso machine, but it didn’t work.",
            "id": "2",
            "role": "Customer",
            "participantId": "Customer_1"
          },
          {
            "text": "I’m sorry to hear that. Let’s see what we can do to fix this issue. Could you please try the following steps for me? First, could you push the wifi connection button, hold for 3 seconds, then let me know if the power light is slowly blinking on and off every second?",
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
            "text": "I’m very sorry to hear that. Let me see if there’s another way to fix the issue. Please hold on for a minute.",
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

Conversation summarization also lets you get narrative summaries from input conversations. A guided example scenario is provided below:

1. Copy the command below into a text editor. The BASH example uses the `\` line continuation character. If your console or terminal uses a different line continuation character, use that character.

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
            "text": "Hello, you’re chatting with Rene. How may I help you?",
            "id": "1",
            "role": "Agent",
            "participantId": "Agent_1"
          },
          {
            "text": "Hi, I tried to set up wifi connection for Smart Brew 300 espresso machine, but it didn’t work.",
            "id": "2",
            "role": "Customer",
            "participantId": "Customer_1"
          },
          {
            "text": "I’m sorry to hear that. Let’s see what we can do to fix this issue. Could you please try the following steps for me? First, could you push the wifi connection button, hold for 3 seconds, then let me know if the power light is slowly blinking on and off every second?",
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
            "text": "I’m very sorry to hear that. Let me see if there’s another way to fix the issue. Please hold on for a minute.",
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

Conversation summarization also lets you get recaps and follow-up tasks from input conversations. A guided example scenario is provided below:

1. Copy the command below into a text editor. The BASH example uses the `\` line continuation character. If your console or terminal uses a different line continuation character, use that character.

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
            "text": "Hello, you’re chatting with Rene. How may I help you?",
            "id": "1",
            "role": "Agent",
            "participantId": "Agent_1"
          },
          {
            "text": "Hi, I tried to set up wifi connection for Smart Brew 300 espresso machine, but it didn’t work.",
            "id": "2",
            "role": "Customer",
            "participantId": "Customer_1"
          },
          {
            "text": "I’m sorry to hear that. Let’s see what we can do to fix this issue. Could you please try the following steps for me? First, could you push the wifi connection button, hold for 3 seconds, then let me know if the power light is slowly blinking on and off every second?",
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
            "text": "I’m very sorry to hear that. Let me see if there’s another way to fix the issue. Please hold on for a minute.",
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

The following text is an example of content you might submit for conversation issue and resolution summarization. This is only an example, the API can accept longer input text. See [data limits](../../concepts/data-limits.md) for more information.
 
**Agent**: "*Hello, how can I help you*?"

**Customer**: "*How can I upgrade my Contoso subscription? I've been trying the entire day.*"

**Agent**: "*Press the upgrade button then sign in and follow the instructions.*"

Summarization is performed upon receipt of the request by creating a job for the API backend. If the job succeeded, the output of the API will be returned. The output is available for retrieval for 24 hours. After this time, the output is purged. Due to multilingual and emoji support, the response might contain text offsets. See [how to process offsets](../../concepts/multilingual-emoji-support.md) for more information.

In the above example, the API might return the following summarized sentences:

| Summarized text                                                           | Aspect     |
|---------------------------------------------------------------------------|------------|
| "Customer wants to upgrade their subscription. Customer doesn't know how."| issue      |
| "Customer needs to press upgrade button, and sign in."                    | resolution |

## See also

* [Summarization overview](../overview.md)
