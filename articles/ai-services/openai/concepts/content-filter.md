---
title: Azure OpenAI Service content filtering
titleSuffix: Azure OpenAI
description: Learn about the content filtering capabilities of Azure OpenAI Service, including how it detects and prevents harmful content in various scenarios.
author: PatrickFarley
ms.author: pafarley
ms.service: azure-ai-openai
ms.topic: conceptual
ms.date: 05/07/2025
ms.custom: template-concept, devx-track-python
manager: nitinme
---

# Content filtering overview

Azure OpenAI Service includes a content filtering system that works alongside core models, including image generation models. This system works by running both the prompt and completion through a set of classification models designed to detect and prevent the output of harmful content. The content filtering system detects and takes action on specific categories of potentially harmful content in both input prompts and output completions. Variations in API configurations and application design might affect completions and thus filtering behavior.

> [!IMPORTANT]
> The content filtering system isn't applied to prompts and completions processed by the audio models such as Whisper in Azure OpenAI Service. Learn more about the [Audio models in Azure OpenAI](models.md?tabs=standard-audio#standard-deployment-regional-models-by-endpoint).


In addition to the content filtering system, Azure OpenAI Service performs monitoring to detect content and/or behaviors that suggest use of the service in a manner that might violate applicable product terms. For more information about understanding and mitigating risks associated with your application, see the [Transparency Note for Azure OpenAI](/legal/cognitive-services/openai/transparency-note?tabs=text). For more information about how data is processed for content filtering and abuse monitoring, see [Data, privacy, and security for Azure OpenAI Service](/legal/cognitive-services/openai/data-privacy?context=/azure/ai-services/openai/context/context#preventing-abuse-and-harmful-content-generation).  

The articles in this section provide information about the content filtering categories, the filtering severity levels and their configurability, and API scenarios to be considered in application design and implementation. 

> [!NOTE]
> No prompts or completions are stored for the purposes of content filtering. No prompts or completions are used to train, retrain, or improve the content filtering system without your consent. For more information, see [Data, privacy, and security](/legal/cognitive-services/openai/data-privacy?context=%2Fazure%2Fai-services%2Fopenai%2Fcontext%2Fcontext&tabs=azure-portal).

## Content filter types

The content filtering system integrated in the Azure OpenAI Service contains: 
* Neural multi-class classification models aimed at detecting and filtering harmful content; the models cover four categories (hate, sexual, violence, and self-harm) across four severity levels (safe, low, medium, and high). Content detected at the 'safe' severity level is labeled in annotations but isn't subject to filtering and isn't configurable.
* Other optional classification models aimed at detecting jailbreak risk and known content for text and code; these models are binary classifiers that flag whether user or model behavior qualifies as a jailbreak attack or match to known text or source code. The use of these models is optional, but use of protected material code model may be required for Customer Copyright Commitment coverage.

## Risk categories

The following table summarizes the risk categories supported by Azure OpenAI's content filtering system.


|Category|Description|
|--------|-----------|
| Hate and Fairness      | Hate and fairness-related harms refer to any content that attacks or uses discriminatory language with reference to a person or Identity group based on certain differentiating attributes of these groups. <br><br>This includes, but is not limited to:<ul><li>Race, ethnicity, nationality</li><li>Gender identity groups and expression</li><li>Sexual orientation</li><li>Religion</li><li>Personal appearance and body size</li><li>Disability status</li><li>Harassment and bullying</li></ul> |
| Sexual  | Sexual describes language related to anatomical organs and genitals, romantic relationships and sexual acts, acts portrayed in erotic or affectionate terms, including those portrayed as an assault or a forced sexual violent act against one’s will. <br><br> This includes but is not limited to:<ul><li>Vulgar content</li><li>Prostitution</li><li>Nudity and Pornography</li><li>Abuse</li><li>Child exploitation, child abuse, child grooming</li></ul>   |
| Violence  | Violence describes language related to physical actions intended to hurt, injure, damage, or kill someone or something; describes weapons, guns and related entities. <br><br>This includes, but isn't limited to:  <ul><li>Weapons</li><li>Bullying and intimidation</li><li>Terrorist and violent extremism</li><li>Stalking</li></ul>  |
| Self-Harm  | Self-harm describes language related to physical actions intended to purposely hurt, injure, damage one’s body or kill oneself. <br><br> This includes, but isn't limited to: <ul><li>Eating Disorders</li><li>Bullying and intimidation</li></ul>  |
| Protected Material for Text<sup>1</sup> | Protected material text describes known text content (for example, song lyrics, articles, recipes, and selected web content) that can be outputted by large language models.
| Protected Material for Code | Protected material code describes source code that matches a set of source code from public repositories, which can be outputted by large language models without proper citation of source repositories.
|User Prompt Attacks |User prompt attacks are User Prompts designed to provoke the Generative AI model into exhibiting behaviors it was trained to avoid or to break the rules set in the System Message. Such attacks can vary from intricate roleplay to subtle subversion of the safety objective. |
|Indirect Attacks |Indirect Attacks, also referred to as Indirect Prompt Attacks or Cross-Domain Prompt Injection Attacks, are a potential vulnerability where third parties place malicious instructions inside of documents that the Generative AI system can access and process. Requires [document embedding and formatting](./content-filter-document-embedding.md). |
| Groundedness<sup>2</sup> | Groundedness detection flags whether the text responses of large language models (LLMs) are grounded in the source materials provided by the users. Ungrounded material refers to instances where the LLMs produce information that is non-factual or inaccurate from what was present in the source materials. Requires [document embedding and formatting](./content-filter-document-embedding.md). |

<sup>1</sup> If you're an owner of text material and want to submit text content for protection, [file a request](https://aka.ms/protectedmaterialsform).

<sup>2</sup> Not available in non-streaming scenarios; only available for streaming scenarios. The following regions support Groundedness Detection: Central US, East US, France Central, and Canada East 

## Scenario details

When the content filtering system detects harmful content, you receive either an error on the API call if the prompt was deemed inappropriate, or the `finish_reason` on the response will be `content_filter` to signify that some of the completion was filtered. When building your application or system, you'll want to account for these scenarios where the content returned by the Completions API is filtered, which might result in content that is incomplete. How you act on this information will be application specific. The behavior can be summarized in the following points:

-	Prompts that are classified at a filtered category and severity level will return an HTTP 400 error.
-	Non-streaming completions calls won't return any content when the content is filtered. The `finish_reason` value is set to content_filter. In rare cases with longer responses, a partial result can be returned. In these cases, the `finish_reason` is updated.
-	For streaming completions calls, segments are returned back to the user as they're completed. The service continues streaming until either reaching a stop token, length, or when content that is classified at a filtered category and severity level is detected.  

### Scenario: You send a non-streaming completions call asking for multiple outputs; no content is classified at a filtered category and severity level

The table below outlines the various ways content filtering can appear:

 **HTTP response code** | **Response behavior** |
|------------------------|-------------------|
| 200 |   In the cases when all generation passes the filters as configured, no content moderation details are added to the response. The `finish_reason` for each generation will be either stop or length. |

**Example request payload:**

```json
{
    "prompt":"Text example", 
    "n": 3,
    "stream": false
}
```

**Example response JSON:**

```json
{
    "id": "example-id",
    "object": "text_completion",
    "created": 1653666286,
    "model": "davinci",
    "choices": [
        {
            "text": "Response generated text",
            "index": 0,
            "finish_reason": "stop",
            "logprobs": null
        }
    ]
}

```

### Scenario: Your API call asks for multiple responses (N>1) and at least one of the responses is filtered

| **HTTP Response Code** | **Response behavior**|
|------------------------|----------------------|
| 200 |The generations that were filtered will have a `finish_reason` value of `content_filter`.

**Example request payload:**

```json
{
    "prompt":"Text example",
    "n": 3,
    "stream": false
}
```

**Example response JSON:**

```json
{
    "id": "example",
    "object": "text_completion",
    "created": 1653666831,
    "model": "ada",
    "choices": [
        {
            "text": "returned text 1",
            "index": 0,
            "finish_reason": "length",
            "logprobs": null
        },
        {
            "text": "returned text 2",
            "index": 1,
            "finish_reason": "content_filter",
            "logprobs": null
        }
    ]
}
```

### Scenario: An inappropriate input prompt is sent to the completions API (either for streaming or non-streaming)

**HTTP Response Code** | **Response behavior**
|------------------------|----------------------|
|400 |The API call fails when the prompt triggers a content filter as configured. Modify the prompt and try again.|

**Example request payload:**

```json
{
    "prompt":"Content that triggered the filtering model"
}
```

**Example response JSON:**

```json
"error": {
    "message": "The response was filtered",
    "type": null,
    "param": "prompt",
    "code": "content_filter",
    "status": 400
}
```

### Scenario: You make a streaming completions call; no output content is classified at a filtered category and severity level

|**HTTP Response Code** | **Response behavior**|
|------------|------------------------|
|200|In this case, the call streams back with the full generation and `finish_reason` will be either 'length' or 'stop' for each generated response.|

**Example request payload:**

```json
{
    "prompt":"Text example",
    "n": 3,
    "stream": true
}
```

**Example response JSON:**

```json
{
    "id": "cmpl-example",
    "object": "text_completion",
    "created": 1653670914,
    "model": "ada",
    "choices": [
        {
            "text": "last part of generation",
            "index": 2,
            "finish_reason": "stop",
            "logprobs": null
        }
    ]
}
```

### Scenario: You make a streaming completions call asking for multiple completions and at least a portion of the output content is filtered

|**HTTP Response Code** | **Response behavior**|
|------------|------------------------|
| 200 | For a given generation index, the last chunk of the generation includes a non-null `finish_reason` value. The value is `content_filter` when the generation was filtered.|

**Example request payload:**

```json
{
    "prompt":"Text example",
    "n": 3,
    "stream": true
}
```

**Example response JSON:**

```json
 {
    "id": "cmpl-example",
    "object": "text_completion",
    "created": 1653670515,
    "model": "ada",
    "choices": [
        {
            "text": "Last part of generated text streamed back",
            "index": 2,
            "finish_reason": "content_filter",
            "logprobs": null
        }
    ]
}
```

### Scenario: Content filtering system doesn't run on the completion

**HTTP Response Code** | **Response behavior**
|------------------------|----------------------|
| 200 | If the content filtering system is down or otherwise unable to complete the operation in time, your request will still complete without content filtering. You can determine that the filtering wasn't applied by looking for an error message in the `content_filter_result` object.|

**Example request payload:**

```json
{
    "prompt":"Text example",
    "n": 1,
    "stream": false
}
```

**Example response JSON:**

```json
{
    "id": "cmpl-example",
    "object": "text_completion",
    "created": 1652294703,
    "model": "ada",
    "choices": [
        {
            "text": "generated text",
            "index": 0,
            "finish_reason": "length",
            "logprobs": null,
            "content_filter_result": {
                "error": {
                    "code": "content_filter_error",
                    "message": "The contents are not filtered"
                }
            }
        }
    ]
}
```


## Best practices

As part of your application design, consider the following best practices to deliver a positive experience with your application while minimizing potential harms:

- Decide how you want to handle scenarios where your users send prompts containing content that is classified at a filtered category and severity level or otherwise misuse your application.
- Check the `finish_reason` to see if a completion is filtered.
- Check that there's no error object in the `content_filter_result` (indicating that content filters didn't run).
- If you're using the protected material code model in annotate mode, display the citation URL when you're displaying the code in your application.

## Related content

- Learn about the [content filtering categories and severity levels](./content-filter-risk-categories.md).
- Learn more about the [underlying models that power Azure OpenAI](../concepts/models.md).
- Apply for modified content filters via [this form](https://ncv.microsoft.com/uEfCgnITdR).
- Azure OpenAI content filtering is powered by [Azure AI Content Safety](https://azure.microsoft.com/products/cognitive-services/ai-content-safety).
- Learn more about understanding and mitigating risks associated with your application: [Overview of Responsible AI practices for Azure OpenAI models](/legal/cognitive-services/openai/overview?context=/azure/ai-services/openai/context/context).
- Learn more about how data is processed in connection with content filtering and abuse monitoring: [Data, privacy, and security for Azure OpenAI Service](/legal/cognitive-services/openai/data-privacy?context=/azure/ai-services/openai/context/context#preventing-abuse-and-harmful-content-generation).
