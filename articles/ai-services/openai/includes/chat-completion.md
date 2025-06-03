---
title: Work with the Chat Completion API 
titleSuffix: Azure OpenAI
description: Learn how to work with the Chat Completion API. 
author: mrbullwinkle #dereklegenzoff
ms.author: mbullwin #delegenz
ms.service: azure-ai-openai
ms.topic: include
ms.date: 08/29/2024
manager: nitinme
keywords: ChatGPT

---

## Work with chat completion models

The following code snippet shows the most basic way to interact with models that use the Chat Completion API. If this is your first time using these models programmatically, we recommend that you start with the [chat completions quickstart](../chatgpt-quickstart.md).


```python
import os
from openai import AzureOpenAI

client = AzureOpenAI(
  api_key = os.getenv("AZURE_OPENAI_API_KEY"),  
  api_version = "2024-10-21",
  azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
)

response = client.chat.completions.create(
    model="gpt-4o", # model = "deployment_name".
    messages=[
        {"role": "system", "content": "Assistant is a large language model trained by OpenAI."},
        {"role": "user", "content": "Who were the founders of Microsoft?"}
    ]
)

#print(response)
print(response.model_dump_json(indent=2))
print(response.choices[0].message.content)
```

```output
{
  "id": "chatcmpl-8GHoQAJ3zN2DJYqOFiVysrMQJfe1P",
  "choices": [
    {
      "finish_reason": "stop",
      "index": 0,
      "message": {
        "content": "Microsoft was founded by Bill Gates and Paul Allen. They established the company on April 4, 1975. Bill Gates served as the CEO of Microsoft until 2000 and later as Chairman and Chief Software Architect until his retirement in 2008, while Paul Allen left the company in 1983 but remained on the board of directors until 2000.",
        "role": "assistant",
        "function_call": null
      },
      "content_filter_results": {
        "hate": {
          "filtered": false,
          "severity": "safe"
        },
        "self_harm": {
          "filtered": false,
          "severity": "safe"
        },
        "sexual": {
          "filtered": false,
          "severity": "safe"
        },
        "violence": {
          "filtered": false,
          "severity": "safe"
        }
      }
    }
  ],
  "created": 1698892410,
  "model": "gpt-4o",
  "object": "chat.completion",
  "usage": {
    "completion_tokens": 73,
    "prompt_tokens": 29,
    "total_tokens": 102
  },
  "prompt_filter_results": [
    {
      "prompt_index": 0,
      "content_filter_results": {
        "hate": {
          "filtered": false,
          "severity": "safe"
        },
        "self_harm": {
          "filtered": false,
          "severity": "safe"
        },
        "sexual": {
          "filtered": false,
          "severity": "safe"
        },
        "violence": {
          "filtered": false,
          "severity": "safe"
        }
      }
    }
  ]
}
Microsoft was founded by Bill Gates and Paul Allen. They established the company on April 4, 1975. Bill Gates served as the CEO of Microsoft until 2000 and later as Chairman and Chief Software Architect until his retirement in 2008, while Paul Allen left the company in 1983 but remained on the board of directors until 2000.
```

Every response includes `finish_reason`. The possible values for `finish_reason` are:

* **stop**: API returned complete model output.
* **length**: Incomplete model output because of the `max_tokens` parameter or the token limit.
* **content_filter**: Omitted content because of a flag from our content filters.
* **null**: API response still in progress or incomplete.

Consider setting `max_tokens` to a slightly higher value than normal. A higher value ensures that the model doesn't stop generating text before it reaches the end of the message.

## Work with the Chat Completion API

OpenAI trained chat completion models to accept input formatted as a conversation. The messages parameter takes an array of message objects with a conversation organized by role. When you use the Python API, a list of dictionaries is used.

The format of a basic chat completion is:

```
{"role": "system", "content": "Provide some context and/or instructions to the model"},
{"role": "user", "content": "The users messages goes here"}
```

A conversation with one example answer followed by a question would look like:

```
{"role": "system", "content": "Provide some context and/or instructions to the model."},
{"role": "user", "content": "Example question goes here."},
{"role": "assistant", "content": "Example answer goes here."},
{"role": "user", "content": "First question/message for the model to actually respond to."}
```

### System role

The system role, also known as the system message, is included at the beginning of the array. This message provides the initial instructions to the model. You can provide various information in the system role, such as:

* A brief description of the assistant.
* Personality traits of the assistant.
* Instructions or rules you want the assistant to follow.
* Data or information needed for the model, such as relevant questions from an FAQ.

You can customize the system role for your use case or include basic instructions. The system role/message is optional, but we recommend that you at least include a basic one to get the best results.

### Messages

After the system role, you can include a series of messages between the `user` and the `assistant`.

```
 {"role": "user", "content": "What is thermodynamics?"}
```

To trigger a response from the model, end with a user message to indicate that it's the assistant's turn to respond. You can also include a series of example messages between the user and the assistant as a way to do few-shot learning.

### Message prompt examples

The following section shows examples of different styles of prompts that you can use with chat completions models. These examples are only a starting point. You can experiment with different prompts to customize the behavior for your own use cases.

#### Basic example

If you want you chat completions model to behave similarly to [chatgpt.com](https://chatgpt.com/), you can use a basic system message like `Assistant is a large language model trained by OpenAI.`

```
{"role": "system", "content": "Assistant is a large language model trained by OpenAI."},
{"role": "user", "content": "Who were the founders of Microsoft?"}
```

#### Example with instructions

For some scenarios, you might want to give more instructions to the model to define guardrails for what the model is able to do.

```
{"role": "system", "content": "Assistant is an intelligent chatbot designed to help users answer their tax related questions.
Instructions: 
- Only answer questions related to taxes. 
- If you're unsure of an answer, you can say "I don't know" or "I'm not sure" and recommend users go to the IRS website for more information. "},
{"role": "user", "content": "When are my taxes due?"}
```

#### Use data for grounding

You can also include relevant data or information in the system message to give the model extra context for the conversation. If you need to include only a small amount of information, you can hard code it in the system message. If you have a large amount of data that the model should be aware of, you can use [embeddings](../tutorials/embeddings.md?tabs=command-line) or a product like [Azure AI Search](https://techcommunity.microsoft.com/t5/ai-applied-ai-blog/revolutionize-your-enterprise-data-with-chatgpt-next-gen-apps-w/ba-p/3762087) to retrieve the most relevant information at query time.

```
{"role": "system", "content": "Assistant is an intelligent chatbot designed to help users answer technical questions about Azure OpenAI in Azure AI Foundry Models. Only answer questions using the context below and if you're not sure of an answer, you can say 'I don't know'.

Context:
- Azure OpenAI provides REST API access to OpenAI's powerful language models including the GPT-3, Codex and Embeddings model series.
- Azure OpenAI gives customers advanced language AI with OpenAI GPT-3, Codex, and DALL-E models with the security and enterprise promise of Azure. Azure OpenAI co-develops the APIs with OpenAI, ensuring compatibility and a smooth transition from one to the other.
- At Microsoft, we're committed to the advancement of AI driven by principles that put people first. Microsoft has made significant investments to help guard against abuse and unintended harm, which includes requiring applicants to show well-defined use cases, incorporating Microsoft’s principles for responsible AI use."
},
{"role": "user", "content": "What is Azure OpenAI?"}
```

#### Few-shot learning with chat completion

You can also give few-shot examples to the model. The approach for few-shot learning has changed slightly because of the new prompt format. You can now include a series of messages between the user and the assistant in the prompt as few-shot examples. By using these examples, you can seed answers to common questions to prime the model or teach particular behaviors to the model.

This example shows how you can use few-shot learning with GPT-35-Turbo and GPT-4. You can experiment with different approaches to see what works best for your use case.

```
{"role": "system", "content": "Assistant is an intelligent chatbot designed to help users answer their tax related questions. "},
{"role": "user", "content": "When do I need to file my taxes by?"},
{"role": "assistant", "content": "In 2023, you will need to file your taxes by April 18th. The date falls after the usual April 15th deadline because April 15th falls on a Saturday in 2023. For more details, see https://www.irs.gov/filing/individuals/when-to-file."},
{"role": "user", "content": "How can I check the status of my tax refund?"},
{"role": "assistant", "content": "You can check the status of your tax refund by visiting https://www.irs.gov/refunds"}
```

#### Use chat completion for nonchat scenarios

The Chat Completion API is designed to work with multi-turn conversations, but it also works well for nonchat scenarios.

For example, for an entity extraction scenario, you might use the following prompt:

```
{"role": "system", "content": "You are an assistant designed to extract entities from text. Users will paste in a string of text and you will respond with entities you've extracted from the text as a JSON object. Here's an example of your output format:
{
   "name": "",
   "company": "",
   "phone_number": ""
}"},
{"role": "user", "content": "Hello. My name is Robert Smith. I'm calling from Contoso Insurance, Delaware. My colleague mentioned that you are interested in learning about our comprehensive benefits policy. Could you give me a call back at (555) 346-9322 when you get a chance so we can go over the benefits?"}
```

## Create a basic conversation loop

The examples so far show the basic mechanics of interacting with the Chat Completion API. This example shows you how to create a conversation loop that performs the following actions:

- Continuously takes console input and properly formats it as part of the messages list as user role content.
- Outputs responses that are printed to the console and formatted and added to the messages list as assistant role content.

Every time a new question is asked, a running transcript of the conversation so far is sent along with the latest question. Because the model has no memory, you need to send an updated transcript with each new question or the model will lose the context of the previous questions and answers.

```python
import os
from openai import AzureOpenAI

client = AzureOpenAI(
  api_key = os.getenv("AZURE_OPENAI_API_KEY"),  
  api_version = "2024-10-21",
  azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")  # Your Azure OpenAI resource's endpoint value.
)

conversation=[{"role": "system", "content": "You are a helpful assistant."}]

while True:
    user_input = input("Q:")      
    conversation.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="gpt-4o", # model = "deployment_name".
        messages=conversation
    )

    conversation.append({"role": "assistant", "content": response.choices[0].message.content})
    print("\n" + response.choices[0].message.content + "\n")
```

When you run the preceding code, you get a blank console window. Enter your first question in the window and then select the `Enter` key. After the response is returned, you can repeat the process and keep asking questions.

## Manage conversations

The previous example runs until you hit the model's token limit. With each question asked, and answer received, the `messages` list grows in size. The token limit for chat completions models varies across models and versions The token limits for `gpt-4` and `gpt-4-32k` are 8,192 and 32,768, respectively. These limits include the token count from both the message list sent and the model response. The number of tokens in the messages list combined with the value of the `max_tokens` parameter must stay under these limits or you receive an error. Consult the [models page](../concepts/models.md) for each models token limits/context windows.

It's your responsibility to ensure that the prompt and completion fall within the token limit. For longer conversations, you need to keep track of the token count and only send the model a prompt that falls within the limit. Alternatively, with the [responses API](../how-to/responses.md) you can have the API handle truncation/management of the conversation history for you.

> [!NOTE]  
> We strongly recommend that you stay within the [documented input token limit](../concepts/models.md) for all models, even if you discover that you can exceed that limit.

The following code sample shows a simple chat loop example with a technique for handling a 4,096-token count by using OpenAI's tiktoken library.

The code uses tiktoken `0.5.1`. If you have an older version, run `pip install tiktoken --upgrade`.

```python
import tiktoken
import os
from openai import AzureOpenAI

client = AzureOpenAI(
  api_key = os.getenv("AZURE_OPENAI_API_KEY"),  
  api_version = "2024-10-21",
  azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")  # Your Azure OpenAI resource's endpoint value.
)

system_message = {"role": "system", "content": "You are a helpful assistant."}
max_response_tokens = 250
token_limit = 4096
conversation = []
conversation.append(system_message)

def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613"):
    """Return the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    if model in {
        "gpt-3.5-turbo-0613",
        "gpt-3.5-turbo-16k-0613",
        "gpt-4-0314",
        "gpt-4-32k-0314",
        "gpt-4-0613",
        "gpt-4-32k-0613",
        }:
        tokens_per_message = 3
        tokens_per_name = 1
    elif model == "gpt-3.5-turbo-0301":
        tokens_per_message = 4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
        tokens_per_name = -1  # if there's a name, the role is omitted
    elif "gpt-3.5-turbo" in model:
        print("Warning: gpt-3.5-turbo may update over time. Returning num tokens assuming gpt-3.5-turbo-0613.")
        return num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613")
    elif "gpt-4" in model:
        print("Warning: gpt-4 may update over time. Returning num tokens assuming gpt-4-0613.")
        return num_tokens_from_messages(messages, model="gpt-4-0613")
    else:
        raise NotImplementedError(
            f"""num_tokens_from_messages() is not implemented for model {model}."""
        )
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens
while True:
    user_input = input("Q:")      
    conversation.append({"role": "user", "content": user_input})
    conv_history_tokens = num_tokens_from_messages(conversation)

    while conv_history_tokens + max_response_tokens >= token_limit:
        del conversation[1] 
        conv_history_tokens = num_tokens_from_messages(conversation)

    response = client.chat.completions.create(
        model="gpt-35-turbo", # model = "deployment_name".
        messages=conversation,
        temperature=0.7,
        max_tokens=max_response_tokens
    )


    conversation.append({"role": "assistant", "content": response.choices[0].message.content})
    print("\n" + response.choices[0].message.content + "\n")
```

In this example, after the token count is reached, the oldest messages in the conversation transcript are removed. For efficiency, `del` is used instead of `pop()`. We start at index 1 to always preserve the system message and only remove user or assistant messages. Over time, this method of managing the conversation can cause the conversation quality to degrade as the model gradually loses the context of the earlier portions of the conversation.

An alternative approach is to limit the conversation duration to the maximum token length or a specific number of turns. After the maximum token limit is reached, the model would lose context if you were to allow the conversation to continue. You can prompt the user to begin a new conversation and clear the messages list to start a new conversation with the full token limit available.

The token counting portion of the code demonstrated previously is a simplified version of one of [OpenAI's cookbook examples](https://github.com/openai/openai-cookbook/blob/main/examples/How_to_format_inputs_to_ChatGPT_models.ipynb).

## Troubleshooting

### Don't use ChatML syntax or special tokens with the chat completion endpoint

Some customers try to use the [legacy ChatML syntax](../how-to/chat-markup-language.md) with the chat completion endpoints and newer models. ChatML was a preview capability that only worked with the legacy completions endpoint with the `gpt-35-turbo` version 0301 model. This model is [slated for retirement](../concepts/model-retirements.md). If you attempt to use ChatML syntax with newer models and the chat completion endpoint, it can result in errors and unexpected model response behavior. We don't recommend this use. This same issue can occur when using common special tokens.

| Error Code | Error Message | Solution |
|---|---|---|
| 400 | 400 - "Failed to generate output due to special tokens in the input." | Your prompt contains special tokens or legacy ChatML tokens not recognized or supported by the model/endpoint. Ensure that your prompt/messages array doesn't contain any legacy ChatML tokens/special tokens. If you're upgrading from a legacy model, exclude all special tokens before you submit an API request to the model.|

### Failed to create completion as the model generated invalid Unicode output

| Error Code | Error Message | Workaround |
|---|---|---|
| 500 | 500 - InternalServerError: Error code: 500 - {'error': {'message': 'Failed to create completion as the model generated invalid Unicode output}}. | You can minimize the occurrence of these errors by reducing the temperature of your prompts to less than 1 and ensuring you're using a client with retry logic. Reattempting the request often results in a successful response. |

## Next steps

* [Learn more about Azure OpenAI](../overview.md).
* Get started with chat completions models with [the chat completion quickstart](../chatgpt-quickstart.md).
* For more examples, see the [Azure OpenAI Samples GitHub repository](https://github.com/Azure-Samples/openai).
