---
title: Transparency Note for Azure OpenAI in Microsoft Foundry Models
titleSuffix: Microsoft Foundry
description: Transparency Note for Azure OpenAI
author: mrbullwinkle
ms.author: mbullwin
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: concept-article
monikerRange: 'foundry-classic || foundry'
ms.date: 04/16/2025
---

# Transparency note for Azure OpenAI

[!INCLUDE [non-english-translation](../includes/non-english-translation.md)]

## What is a transparency note?

An AI system includes not only the technology, but also the people who use it, the people who are affected by it, and the environment in which it's deployed. Creating a system that is fit for its intended purpose requires an understanding of how the technology works, what its capabilities and limitations are, and how to achieve the best performance. Microsoft's Transparency Notes are intended to help you understand how our AI technology works, the choices system owners can make that influence system performance and behavior, and the importance of thinking about the whole system, including the technology, the people, and the environment. You can use Transparency Notes when developing or deploying your own system, or share them with the people who will use or be affected by your system.

Microsoft's Transparency Notes are part of a broader effort at Microsoft to put our AI Principles into practice. To find out more, see the [Microsoft's AI principles](https://www.microsoft.com/ai/responsible-ai).

## The basics of the Azure OpenAI Models

Azure OpenAI provides customers with a fully managed Foundry Tool that lets developers and data scientists apply OpenAI's powerful models including models that can generate natural language, code, and images. Within the Azure OpenAI Service, the OpenAI models are integrated with Microsoft-developed Guardrails (previously content filters) and abuse detection models. Learn more about Guardrails (previously content filters) [here](/azure/ai-foundry/openai/concepts/content-filter) and abuse detection [here](/azure/ai-foundry/responsible-ai/openai/data-privacy).


### Introduction

| Model group | Text / code | Vision | Audio / Speech |
| --- | --- | --- | --- |
| GPT-3 & Codex | ✅ |  |  |
| DALL-E 2 & 3  |  | ✅ |  |
| GPT-image-1 |  | ✅ |  |
|  Whisper|  |  | ✅ |
|  GPT-4 Turbo with Vision| ✅ | ✅ |  |
| GPT-4o </br>GPT-4o-mini | ✅ | ✅ | ✅ |
| GPT-4.1</br>GPT-4.1-mini</br>GPT-4.1-nano | ✅ | ✅ |  |
| GPT-4.5 | ✅ | ✅ |  |
| GPT-5 | ✅ | ✅ |  |
| GPT-5.1-Codex-Max | ✅ | ✅ |  |
| GPT-oss-120b | ✅ |  |  |
| o1 series | ✅ | ✅ |  |
| o3/o3-pro | ✅ | ✅| | 
| o3-mini |✅  |  |  |
| o4-mini/codex-mini<sup>1</sup> | ✅| ✅| |
| o3-deep-research <br>o4-mini-deep-research| ✅ |  |  |
| computer-use-preview |✅  | ✅ |  |

<sup>1</sup>`codex-mini` is a fine-tuned version of `o4-mini` specifically for use in Codex CLI. For more information, please see [OpenAI's documentation](https://platform.openai.com/docs/models/codex-mini-latest). 

Select the tabs to see content for the relevant model type.

#### [Text, code, and fine-tuned models](#tab/text)

As part of the fully managed Azure OpenAI Service, the **GPT-3** models analyze and generate natural language, Codex models analyze and generate code and plain text code commentary, and **GPT-4** and **reasoning models** (including o-series models and GPT-5) can understand and generate natural language and code. These models use an autoregressive architecture, meaning they use data from prior observations to predict the most probable next word. This process is then repeated by appending the newly generated content to the original text to produce the complete generated response. Because the response is conditioned on the input text, these models can be applied to various tasks simply by changing the input text.

The GPT-3 series of models are pretrained on a wide body of publicly available free text data. This data is sourced from a combination of web crawling (specifically, a filtered version of [Common Crawl](https://commoncrawl.org/the-data/), which includes a broad range of text from the internet and comprises 60 percent of the weighted pretraining dataset) and higher-quality datasets, including an expanded version of the WebText dataset, two internet-based books corpora and English-language Wikipedia. The GPT-4 base model was trained using publicly available data (such as internet data) and data that was licensed by OpenAI. The model was fine-tuned using reinforcement learning with human feedback (RLHF).

The Computer Use (Preview) model accepts text input on the first turn, and screenshot image on the second and following turns, and outputs commands to the keyboard and mouse. The Computer Use model and the Computer Use Tool enable developers to build agentic AI systems. 

Learn more about the training and modeling techniques in OpenAI's [GPT-3](https://arxiv.org/abs/2005.14165), [GPT-4](https://arxiv.org/abs/2303.08774), and [Codex](https://arxiv.org/abs/2107.03374) research papers.

**Fine tuning** refers to using _Supervised Fine Tuning_ to adjust a base model's weights to provide better responses based on a provided training set. All use cases and considerations for large language models apply to fine-tuned models, but there are additional considerations as well.

> [!IMPORTANT]
> Fine-tuning is only available for text and code models, not vision or speech models.

### Key terms

| **Term** | **Definition** |
| --- | --- |
| Prompt | The text you send to the service in the API call. This text is then input into the model. For example, one might input the following prompt:<br><br>`Convert the questions to a command:`<br>`Q: Ask Constance if we need some bread`<br>`A: send-msg 'find constance' Do we need some bread?`<br>`Q: Send a message to Greg to figure out if things are ready for Wednesday.`<br>`A:` |
| Completion or Generation | The text Azure OpenAI outputs in response. For example, the service may respond with the following answer to the above prompt: `send-msg 'find greg' figure out if things are ready for Wednesday.` |
| Token | Azure OpenAI processes text by breaking it down into tokens. Tokens can be words or just chunks of characters. For example, the word `hamburger` gets broken up into the tokens `ham`, `bur` and `ger`, while a short and common word like `pear` is a single token. Many tokens start with a whitespace, for example ` hello` and ` bye`. |
|Fine tuning| Supervised fine-tuning (SFT), reinforcement fine-tuning (RFT), and direct preference optimization (DPO, or preference fine-tuning) for large language models refer to the process of taking a pre-trained language model, often trained on a massive dataset, and further training it on a more specific task with labeled data. This involves adjusting the weights of the model using this smaller, specific dataset so that the model becomes more specialized in the tasks it can perform, enhancing its performance and accuracy. |
| Model Weights| Model weights are parameters within the model that are learned from the data during the training process. They determine the output of the model for a given input. These weights are adjusted in response to the error the model made in its predictions, with the aim of minimizing this error. |
|Ungrounded content|  Content that is generated by the model that is non-factual or inaccurate from what was present in the source materials. |
| Agentic AI systems | Autonomous AI systems that sense and act upon their environment to achieve goals. |
| Autonomy  | The ability to independently execute actions and exercise control over system behavior with limited or no direct human supervision. |
| Computer Use tool | A tool that when used with the Computer Use model captures mouse and keyboard actions generated by the mode and directly translates them into executable commands. This makes it possible for developers to automate computer use tasks. |
| Deep research | A fine-tuned version of the o-series reasoning models that is designed for deep research tasks. It takes a high-level query and returns a structured, citation-rich report by leveraging an agentic model capable of decomposing the task, performing web searches, and synthesizing results. |

#### [Vision models](#tab/image)

The fully managed service provides API access to Azure OpenAI DALL·E 2, DALL·E 3, GPT-image-1, GPT-4 Turbo with Vision, GPT-4o, and o1 APIs.

**Azure OpenAI DALL·E APIs** enable the generation of rich imagery from text prompts and image inputs in an application. This powerful, multimodal AI model was developed by [OpenAI](https://openai.com/dall-e-2/) and can generate images that capture both the semantics and style of the text input.

You can learn more about the training and modeling techniques for DALL·E in the [OpenAI DALL·E research paper](https://arxiv.org/abs/2204.06125) and about DALL·E 3 safety from the [OpenAI DALL·E 3 system card](https://cdn.openai.com/papers/DALL_E_3_System_Card.pdf).

**Azure OpenAI GPT-4 Turbo with Vision** can accept multimodal (image and text) inputs and generate natural language and code responses. This API enables a richer and more comprehensive understanding of image and video inputs.  

You can learn more about the training and modeling techniques for GPT-4 Turbo with Vision in the OpenAI GPT-4 research paper OpenAI [GPT-4 research paper](https://arxiv.org/abs/2303.08774) and GPT-4 Turbo with Vision safety from the system card.

**Azure OpenAI GPT-4o** can accept multimodal (image and text) inputs and generate natural language and code responses, similar to Azure OpenAI GPT-4 Turbo with Vision.

Azure OpenAI Computer Use (Preview) accepts text input on the first turn, and screenshot image on the second and following turns, and outputs commands to the keyboard and mouse.  The Computer Use model and the Computer Use Tool enable developers to build agentic AI systems. 

The following guidance is drawn from Microsoft research insights and [best practices for responsible AI](/azure/ai-foundry/responsible-ai/openai/overview). 

### Key terms

| **Term** | **Definition** |
| --- | --- |
| Text-to-image | A capability that enables users to generate images that are based on text prompts. |
| prompt | The text you send to the service in the API call. This text is then input into the model. For example, a user might input the following prompt for image generation:<br><br> Text prompt: `Image of a botanical garden in the style of Picasso, rendered`<br><br>Generated image: Rendered image of a botanical garden in the style of Picasso. |
|Prompt transformation | **DALL·E 3 only**: The process by which all prompts sent to the service APIs are enhanced by using a static metaprompt put in place by OpenAI. This process helps you enhance the quality of your images. |
| Style (natural or vivid) | **DALL·E 3 only**: DALL·E 3 enables you to choose from two styles when you generate your images. This choice can be made in the API request.<br>Natural Style: Closely resembles DALL·E 2 because generations are more simplistic and realistic. <br>Vivid Style: On by default, this style offers richer and more cinematic image generation.  |
| Metaprompt | Sometimes referred to as the system message or system prompt, it's a message written by the developer, in this case, OpenAI, to prime the model with context, instructions, or other information with certain bounds primarily used to enforce safety instructions.  |
| Zero-shot translation | A machine learning capability of executing on novel categories or samples.<br><br>In the case of the latest image generation models, it's the model's ability to execute on a user-generated text prompt on which it wasn't explicitly trained. This capability allows the model to execute and generalize to any text input. |
| GPT-4 Turbo with Vision | The content you send to the service in the API call. GPT-4 Turbo with Vision takes in text, image, or text and image interleaved prompts. This prompt is then input into the model. For example, a user might input the following prompt into the system: <br><br>Prompt: `How can I use [Image of a tomato] to make this? [Image of tomato soup]`<br><br>Completion: `Here is a list of recipes using tomatoes from which you can make the best tomato soup!` |
|Video enhancement |Enables GPT-4 Turbo with Vision to answer questions by retrieving the video frames most relevant to the user's prompt. |
|Face blurring |A preprocessing step that blurs all faces detected in image and video inputs when your inputs are processed in the API call. The blurring process is incapable of uniquely identifying individuals. Blurring helps to protect the privacy of individuals and groups while also helping to address other risks related to privacy and the regulations around them.  |
| Agentic AI systems | Autonomous AI systems that sense and act upon their environment to achieve goals. |
| Autonomy  | The ability to independently execute actions and exercise control over system behavior with limited or no direct human supervision. |
| Computer Use tool | A tool that when used with the Computer Use model captures mouse and keyboard actions generated by the mode and directly translates them into executable commands. This makes it possible for developers to automate computer use tasks. |
| Inpainting | The process of generating content within a specific masked area of an image&mdash;whether to correct, complete, or creatively alter it&mdash;while keeping the surrounding context coherent. |

#### [Audio / speech models](#tab/speech)

The `gpt-4o-realtime-preview` model in Azure OpenAI service enables robust speech-to-speech and text-to-speech interactions. This model integrates advanced speech recognition and synthesis capabilities, allowing it to understand spoken input, generate accurate transcriptions, and produce fluent spoken output in a target language. With its ability to translate speech in real time, `gpt-4o-realtime-preview` facilitates dynamic conversations across languages. 

The Whisper model in Azure OpenAI service enables access to a model that performs robust speech recognition and translation tasks. The Whisper model is an Automatic Speech Recognition (ASR) model that was developed by [OpenAI](https://openai.com/research/whisper) and is capable of transcribing speech audio files into the language that was spoken as well as translated into English.

You can learn more about training and modeling techniques for the Whisper model in the [OpenAI Whisper research paper](https://cdn.openai.com/papers/whisper.pdf). The Whisper model is also used in the Azure Speech in Foundry Tools service. Learn more about the Azure Speech integration and evaluate it for your use [here](/azure/ai-foundry/responsible-ai/speech-service/speech-to-text/transparency-note).

### Key terms

| **Term** | **Definition** |
|--|--|
| Transcription | The text output of the Speech to Text feature. This automatically generated text output leverages _speech models_ and is sometimes referred to as machine transcription or automated speech recognition (ASR). Transcription in this context is fully automated, meaning it's generated by the model, and therefore is different from human transcription, which is text that is generated by human transcribers.   |
| Automatic Speech Recognition (ASR) | Also known as Speech-to-Text (STT), ASR is the process whereby a model transcribes or processes human speech as audio into text. |
| Speech Translation | A capability that enables users to translate speech into a designated language. At this time, the Whisper model in Azure OpenAI Service enables users to translate speech audio from non-English into English only. |
| Prompt | Context or cues that you can provide to the model to improve the quality of transcripts generated for your scenario. The prompt can provide instructions for processing things like jargon or acronyms, or for forcing filler words to be included.   </br></br>Learn more about prompts [here](https://platform.openai.com/docs/guides/speech-to-text/longer-inputs). 
|Completion / Generation | The audio or text Azure OpenAI outputs in response. |
|Token | Azure OpenAI processes audio and text by breaking it down into tokens. Tokens can be words or just chunks of characters. |

---

## Capabilities


#### [Text, code, and fine-tuned models](#tab/text)

The reasoning models, GPT-4, GPT-3, Codex models, and Azure OpenAI evaluation use natural language instructions and examples in the prompt to identify the task. The model then completes the task by predicting the most probable next text. This technique is known as "in-context" learning. These models are not retrained during this step but instead give predictions based on the context you include in the prompt.

There are three main approaches for in-context learning. These approaches vary based on the amount of task-specific data that is given to the model:

**Few-shot** : In this case, a user includes several examples in the prompt that demonstrate the expected answer format and content. The following example shows a few-shot prompt providing multiple examples:

```
Convert the questions to a command: 
Q: Ask Constance if we need some bread 
A: send-msg `find constance` Do we need some bread? 
Q: Send a message to Greg to figure out if things are ready for Wednesday. 
A: send-msg `find greg` Is everything ready forWednesday? 
Q: Ask Ilya if we're still having our meeting thisevening 
A: send-msg `find ilya` Are we still having a meetingthis evening? 
Q: Contact the ski store and figure out if I can getmy skis fixed before I leave on Thursday 
A: send-msg `find ski store` Would it be possible toget my skis fixed before I leave on Thursday? 
Q: Thank Nicolas for lunch 
A: send-msg `find nicolas` Thank you for lunch! 
Q: Tell Constance that I won't be home before 19:30tonight — unmovable meeting. 
A: send-msg `find constance` I won't be home before19:30 tonight. I have a meeting I can't move. 
Q: Tell John that I need to book an appointment at10:30 
A:  
```
The number of examples typically ranges from 0 to 100 depending on how many can fit in the maximum input length for a single prompt. Few-shot learning enables a major reduction in the amount of task-specific data required for accurate predictions.

**One-shot** : This case is the same as the few-shot approach except only one example is provided. The following example shows a one-shot prompt:

```
Convert the questions to a command:
Q: Ask Constance if we need some bread
A: send-msg `find constance` Do we need some bread?
Q: Send a message to Greg to figure out if things are ready for Wednesday.
A:
```

**Zero-shot**: In this case, no examples are provided to the model and only the task request is provided. The following example shows a zero-shot prompt:

```
Convert the question to a command:
Q: Ask Constance if we need some bread
A:
```

**Chain-of-thought** : Azure OpenAI's reasoning models have advanced reasoning capabilities using chain-of-thought (CoT) techniques. CoT techniques generate intermediate reasoning steps before providing a response, enabling them to address more complex challenges through step-by-step problem solving. o1 demonstrates improvements in benchmarks for reasoning-heavy domains such as research, strategy, science, coding and math, among others. These models have safety improvements from advanced reasoning capabilities, with the ability to reason through and apply safety rules more effectively. This results in better performance alongside safety benchmarks such as generating illicit advice, choosing stereotyped responses, and succumbing to known jailbreaks. 

For greater detail on this family of models’ capabilities, see the [OpenAI o1 System Card](https://cdn.openai.com/o1-system-card-20241205.pdf), [o3-mini System Card](https://openai.com/index/o3-mini-system-card/), [o3/o4-mini System Card](https://openai.com/index/o3-o4-mini-system-card/), [Deep Research System Card](https://openai.com/index/deep-research-system-card/), and [GPT-5 System Card](https://openai.com/index/gpt-5-system-card/).

**Azure OpenAI Evaluation** 

The evaluation of large language models is a critical step in measuring their performance across various tasks and dimensions. This task is especially important for fine-tuned models, where assessing the performance gains (or losses) from training is crucial. Without thorough evaluations, it can become challenging to understand how different versions of the model may impact your specific application.  

Azure OpenAI Evaluation is a UI-based experience to evaluate data, including generated datasets from an Azure OpenAI deployment, or other manually curated files. 

Azure OpenAI Evaluation has an optional step of generating responses. If the user opts into this step, we provide a prompt (System/User Message) to instruct the model how to generate responses. 

Azure OpenAI Evaluation includes 9 categories of tests to score results. Some require ground truth data (like factuality), while others do not (schema validation). Graders are a mixture of CPU-based and model-based. Here is the list of testing criteria: Factuality, Sentiment, Valid JSON or XML, Criteria Match, Custom Prompt, Semantic Similarity, Contains string, Matches Schema and Text quality.

**Text-to-action**

The Computer Use (Preview) model enables text-to-action capabilities, allowing users to provide natural language instructions that the model translates into actionable steps within graphical user interfaces. Given a command like "Fill out the customer support form with this information," the model identifies the relevant fields, inputs the correct data, and submits the form. It can navigate web interfaces, extract and input structured or unstructured data, automate workflows, and enforce compliance with security policies. By understanding intent and executing actions accordingly, it streamlines business operations, making automation more accessible and efficient. 

#### [Vision models](#tab/image)

### Image generation APIs in Azure OpenAI Service

The DALL·E 2, DALL·E 3, and GPT-image-1 APIs use natural language prompts to generate new content. These models were trained on pairs of images and corresponding captions that were drawn from publicly available sources and other sources that OpenAI has licensed.


These generative AI models present myriad opportunities for developers, artists, designers, educators, and others. The models can bridge the gap between what you can imagine and what you can create. They allow for cross-domain, general understanding, and zero-shot translation between text prompt and images, often with a high degree of realism. 

The main capabilities of the Azure OpenAI image generation APIs are: 

- **Text-to-image**: The model takes in a text prompt to generate images.

    | **Example text prompt** | **Example generated image** |
    |---|---|
    | "Watercolor painting of the Seattle skyline" | ![Watercolor painting of the Seattle skyline](./media/generated-seattle.png) |

    > [!TIP]
    > Public figures who wish for their depiction not to be generated can opt out by emailing [support@openai.com](mailto:support@openai.com).

- **Prompt transformation**: For DALL·E 3 models: Before a prompt is sent to the model to generate images, a safety and quality mitigation is applied to the prompt. Prompt transformation enhances the prompt with the goal of generating more diverse and higher-quality images. 

    Prompt transformation is applied to every Azure OpenAI DALL·E 3 generation.

    
    After prompt transformation is applied to the original prompt, Guardrails (previously content filters) is applied as a secondary step prior to image generation; see [Guardrails (previously content filters)](/azure/ai-foundry/openai/concepts/content-filter?tabs=warning%2Cpython-new) for more information.  
    
    Learn more about image generation prompting in [OpenAI's documentation](https://platform.openai.com/docs/guides/images/introduction). 

    | **Example text prompt** | **Example generated image without prompt transformation** | **Example generated image with prompt transformation** |
    |---|---|---|
    |"Watercolor painting of the Seattle skyline" | ![Watercolor painting of the Seattle skyline (simple).](./media/generated-seattle.png) | ![Watercolor painting of the Seattle skyline, with more detail and structure.](./media/generated-seattle-prompt-transformed.png) |

- **Image-to-image**: For GPT-image-1 models: The model takes in an image and text prompt and returns a new or altered image based on the text instructions.

- **Inpainting**: For GPT-image-1 models: The model takes in an image and a mask (an image that uses transparent pixels to define an area of focus) along with text instructions and generates new content within the indicated area only. This is used for tasks like correcting or completing images, or creatively altering them while keeping the surrounding context coherent.



### Vision-enabled chat APIs in Azure OpenAI Service

GPT-4 Turbo with Vision and GPT-4o use natural language and image prompts to generate natural language or code responses. The models accept text only, image only, and interleaved text and image inputs. These models are part of the GPT family and are extensions of GPT-4.

The Azure Vision in Foundry Tools Service provides Video enhancement for GPT-4 Turbo with Vision (Preview), which can also accept video inputs to generate natural language or code responses. This capability is not available with the latest GPT-4 Turbo with Vision model release.

| **Example prompt** | **Example completion** |
|---|---|
| "What is this used for?"<br><br> :::image type="content" source="media/tomatoes.png" alt-text="Photo of tomatoes."::: |These are tomatoes. They are commonly used as a food ingredient in various dishes, both raw and cooked. Tomatoes can be used in salads, sandwiches, sauces, soups, juices, and many other culinary applications. They are also known for their rich nutritional content, including vitamins, minerals, and antioxidants. |
|How can I use<br> :::image type="content" source="media/tomatoes.png" alt-text="Same photo of tomatoes.":::<br>to make this?<br> :::image type="content" source="media/soup.png" alt-text="Photo of tomato soup."::: | You can use tomatoes to make tomato soup by following these general steps: <br>Ingredients: <ul><li>Tomatoes </li><li>Onion</li><li>Garlic</li><li> Olive oil or butter</li><li> Chicken or vegetable broth</li><li> Salt</li><li> Pepper</li><li> Optional: herbs like basil, oregano, or thyme </li></ul> <br>Instructions: <ol><li>Preparation:<ul><li> Wash the tomatoes thoroughly. </li><li>Cut the tomatoes into halves or quarters. </li><li>Peel and chop onions and garlic… </li></ul></li></ol>|

### Computer Use in Azure OpenAI Service (Preview)

The Computer Use model is built upon a fine-tuned version of GPT-4o's vision capabilities which allows it to interpret and interact with graphical user interfaces (GUIs) through screenshots. By analyzing visual elements like buttons, text fields, and menus, it can understand application layouts, detect relevant interface components, and execute actions accordingly. This enables precise automation of web and software interactions, allowing for tasks such as data extraction, form completion, and workflow execution based on real-time visual context. 

### Face blurring

For inputs to GPT-4 Turbo with Vision, GPT-4o, and GPT-4o mini that contain images or videos of people, the system will first blur faces prior to processing to return the requested results.

Blurring helps protect the privacy of the individuals and groups involved and protect against restricted use cases. Blurring shouldn't affect the quality of your completions, but you might see the system refer to the blurring of faces in some instances.

> [!IMPORTANT]
> **GPT-4 Turbo with Vision GPT-4o, and GPT-4o mini only**:
> Any processing that returns results that purport to identify an individual or infer the individual's emotion is _not_ the result of processing of the face, such as facial recognition, generation and comparison of facial templates, or other facial inferencing. Such results can be returned based on training the model to associate images of an individual with the same name through image tagging, whereby the model returns the name with any subsequent image inputs of that individual. The model can also take contextual cues other than the face, which is how the model can still associate the image with an individual, or describe emotions, even if the face is blurred. For example, if the image contains a photo of a popular athlete wearing their team's jersey and their specific number, the model may still return a result that purports to identify the individual based on those contextual cues. 

> [!CAUTION]
> **Computer Use (preview) does not use face blurring**, as it has the potential to obscure UI elements and degrade performance. Computer Use is not designed (or intended) to be a general-purpose image reasoning engine. The model doesn't perform facial recognition or individual identification and is not suitable for any such use cases.

> [!CAUTION]
> **GPT-image-1 does not use face blurring.** In certain jurisdictions, the way the model processes image input of people may be considered processing of biometric data, in which case you are responsible for: (i) providing notice to data subjects, including with respect to retention periods and destruction; (ii) obtaining consent from data subjects; and (iii) deleting the data, all as appropriate and required under applicable law. For more information on how Azure OpenAI Service processes data, see [Data, privacy, and security for Azure OpenAI Service](/azure/ai-foundry/responsible-ai/openai/data-privacy).

### Computer Use in Azure OpenAI Service (preview)

The Computer Use model is built upon a fine-tuned version of GPT-4o's vision capabilities which allows it to interpret and interact with graphical user interfaces (GUIs) through screenshots. By analyzing visual elements like buttons, text fields, and menus, it can understand application layouts, detect relevant interface components, and execute actions accordingly. This enables precise automation of web and software interactions, allowing for tasks such as data extraction, form completion, and workflow execution based on real-time visual context. 


#### [Audio / speech models](#tab/speech)

The `gpt-4o-realtime-preview` model in Azure OpenAI service enables advanced speech-to-speech capabilities, providing real-time speech recognition, translation, and synthesis. GPT-4o allows for fluid communication by converting spoken input into coherent output in a target language. 
 
Azure OpenAI service offers these functionalities through the realtime API: 
- Processing spoken input to generate spoken output 
- Translating spoken input into another language 
- Transcribing input and output speech

The service is designed for rapid speech-to-speech processing of spoken interactions, facilitating real-time conversations with minimal latency. 

The Whisper model in Azure OpenAI service enables speech-to-text transcription and translation of audio files. The model was trained on multilingual and multitask supervised data that was collected from the internet. These large and diverse datasets enabled improved robustness to attributes such as accents, background noise and technical language, while enabling transcription into multiple languages, and translation into English.

Azure OpenAI service provides these functionalities through two REST APIs:
- Transcribing a provided audio file
- Translating a provided audio file into English

The service provides the ability to synchronously process single audio files as fast as possible. This is limited to less than 15 to 30 minutes of audio depending on audio compression.

The service provides highly readable transcripts that often remove disfluencies and provide more accurate sentence boundaries, punctuation, and capitalization. You can also leverage prompts to improve the quality of the model outputs as fit for your scenario. See [Best practices for improving system information](#best-practices-for-improving-system-performance) for more information.

For greater detail on 4o model's capabilities, see the [OpenAI 4o System Card](https://openai.com/index/gpt-4o-system-card/). 

---

## Use cases

#### [Text, code, and fine-tuned models](#tab/text)

### Intended uses
Text models can be used in multiple scenarios. The following list isn't comprehensive, but it illustrates the diversity of tasks that can be supported for models with appropriate mitigations:

- **Chat and conversation interaction** : Users can interact with a conversational agent that responds with responses drawn from trusted documents such as internal company documentation or tech support documentation. Conversations must be limited to answering scoped questions.
- **Chat and conversation creation** : Users can create a conversational agent that responds with responses drawn from trusted documents such as internal company documentation or tech support documentation. Conversations must be limited to answering scoped questions.
- **Code generation or transformation scenarios** : For example, converting one programming language to another, generating docstrings for functions, converting natural language to SQL.
- **Journalistic content** : For use to create new journalistic content or to rewrite journalistic content submitted by the user as a writing aid for predefined topics. Users cannot use the application as a general content creation tool for all topics.
- **Question-answering** : Users can ask questions and receive answers from trusted source documents such as internal company documentation. The application doesn't generate answers ungrounded in trusted source documentation.
- **Reason over structured and unstructured data** : Users can analyze inputs using classification, sentiment analysis of text, or entity extraction. Examples include analyzing product feedback sentiment, analyzing support calls and transcripts, and refining text-based search with embeddings.
- **Search** : Users can search trusted source documents such as internal company documentation. The application doesn't generate results ungrounded in trusted source documentation.
- **Summarization** : Users can submit content to be summarized for predefined topics built into the application and cannot use the application as an open-ended summarizer. Examples include summarization of internal company documentation, call center transcripts, technical reports, and product reviews.
- **Writing assistance on specific topics** : Users can create new content or rewrite content submitted by the user as a writing aid for business content or pre-defined topics. Users can only rewrite or create content for specific business purposes or predefined topics and cannot use the application as a general content creation tool for all topics. Examples of business content include proposals and reports. For journalistic use, see above  **Journalistic content** use case.
- **Data generation for fine-tuning**: Users can use a model in Azure OpenAI to generate data which is used solely to fine-tune (i) another Azure OpenAI model, using the fine-tuning capabilities of Azure OpenAI, and/or (ii) another Azure AI custom model, using the fine-tuning capabilities of the Foundry Tool. Generating data and fine-tuning models is limited to internal users only; the fine-tuned model may only be used for inferencing in the applicable Foundry Tool and, for Azure OpenAI service, only for customer's permitted use case(s) under this form.

#### Fine-tuned use cases

The following are additional use cases we recommend for fine-tuned models. Fine tuning is most appropriate for: 
- **Steering the style, format, tone or qualitative aspects of responses** via examples of the desired responses. 
- **Ensuring the model reliably produces a desired output** such as providing responses in a specific format or ensuring responses are grounded by information in the prompt. 
- **Use cases with many edge cases** that cannot be covered within examples in the prompt, such as complex natural language to code examples. 
- **Improving performance at specific skills or tasks** such as classification, summarization, or formatting – that can be hard to describe within a prompt. 
- **Reducing costs or latency** by utilizing shorter prompts, or swapping a fine-tuned version of a smaller/faster model for a more general-purpose model (e.g. fine tuned GPT-3.5-Turbo for GPT-4). 

As with base models, the use case prohibitions outlined in the [Azure OpenAI Code of conduct](/legal/ai-code-of-conduct?context=%2Fazure%2Fcognitive-services%2Fopenai%2Fcontext%2Fcontext) apply to fine-tuned models as well.  

Fine tuning alone is not recommended for scenarios where you want to extend your model to include out-of-domain information, where explainability or grounding are important, or where the underlying data are updated frequently.

#### Reasoning model use cases

The advanced reasoning capabilities of the reasoning models may be best suited for reasoning-heavy uses in science, coding, math, and similar fields. Specific use cases could include:  

- **Complex code generation, analysis and optimization**: Algorithm generation and advanced coding tasks to help developers execute multi-step workflows, better understanding the steps taken in code development.  
- **Advanced problem solving**: Comprehensive brainstorming sessions, strategy development and breaking down multifaceted issues.  
- **Complex document comparison**: Analyzing contracts, case files, or legal documents to discern subtle differences in document contents.  
- **Instruction following and workflow management**: Handling workflows that require shorter context. 

For greater detail on intended uses, visit the [OpenAI o1 System Card](https://cdn.openai.com/o1-system-card-20241205.pdf), [o3-mini System Card](https://openai.com/index/o3-mini-system-card/), [o3/o4-mini System Card](https://openai.com/index/o3-o4-mini-system-card/), and [GPT-5 System Card](https://openai.com/index/gpt-5-system-card/).

#### Deep research use cases

Deep research models are fine-tuned versions of the o-series reasoning models that are designed to take a high-level query and return a structured, citation-rich report. The models create subqueries and gather information from web searches in several iterations before returning a final response. Use cases could include the following, with adequate human oversight:
- **Complex research & literature review**: Synthesizing findings across hundreds of papers, identifying gaps or contradictions in research, proposing novel hypotheses or research directions.
- **Scientific discovery & hypothesis generation**: Exploring connections between findings across disciplines, generating testable hypotheses or experimental designs, assisting in interpretation of raw experimental data.
- **Advanced technical problem solving**: Debugging complex systems (for example, distributed software, robotics), designing novel algorithms or architectures, and solving advanced math or physics problems.
- **Augmenting long-term planning**: Helping executives or researchers plan 10-year technology roadmaps, modeling long-range scenarios in AI safety, biosecurity, or climate, evaluating second- and third-order effects of decisions.

Deep research models are available as a tool in the [Azure AI Agents](/azure/ai-foundry/agents/how-to/tools/deep-research) service. For greater detail on intended uses, see the [OpenAI Deep Research System Card](https://openai.com/index/deep-research-system-card/).

#### Azure OpenAI evaluation use cases

Azure OpenAI evaluation is a text-only feature and can't be used with models that support non-text inputs. Evals can be used in multiple scenarios including but not limited to: 
- **Text matching/comparison evaluation**: This is helpful for scenarios where the user wants to check if the output matches an expected string. Users can also compare two sets of values and score the relationships. Examples include, but are not limited to, multiple-choice questions where answers are compared to an answer key, and string validation. 
- **Text quality**: Text quality assesses response quality with methods such as Bleu, Rouge or cosine algorithms and is widely used in various natural language processing tasks such as machine translation, text summarization, and text generation, among others. 
- **Classification-based evaluation**: Classification-based evaluation assesses the performance of a model by assigning responses to predefined categories or labels or by comparing the model's output to a reference set of correct answers. Automated grading, sentiment analysis, and product categorization are among some of the common use cases. 
- **Conversational quality evaluation**: Conversational quality evaluation involves comparing responses against predefined criteria using a detailed chain-of-thought (CoT) prompt. Common use cases include customer support, chatbot development, and educational assessments, among others. 
- **Criteria-based evaluation**: One common scenario for criteria-based evaluation is factuality. Assessing factual accuracy involves comparing a submitted answer to an expert answer, focusing solely on factual content. This can be useful in educational tools to improve the accuracy of answers provided by LLMs or in research assistance tools to assess the factual accuracy of responses generated by LLMs in academic settings. 
- **String validity evaluation**: one common scenario would be to check if model's response follows a specific schema or is valid JSON or XML content. 

#### Computer Use (Preview) use cases 

The capabilities of Computer Use are best suited for developing agentic AI systems that can autonomously interact with GUIs. Specific use cases could include: 

* Automated Web Navigation and Interaction: Navigating  navigation of web-based interfaces autonomously to retrieve and present information from trusted sources, such as internal company resources or structured databases. The model follows predefined navigation rules to extract relevant data while ensuring compliance with security policies. 

* Web-Based Task Automation: Automating repetitive web-based tasks, such as filling out forms, submitting data, or interacting with web applications. Computer Use can click buttons, enter text, and process structured data but operates only within authorized workflows and domains. 

* Structured and Unstructured Data Extraction: Extracting relevant data from structured sources like tables and spreadsheets, as well as unstructured sources such as PDFs, scanned documents, or emails. This capability is useful for tasks like financial data processing, contract analysis, or customer support ticket categorization. 

* Automated Form Filling and Data Entry: Extracting information from structured databases or user inputs and use it to populate web-based forms. This is useful for automating customer service requests, HR processes, or CRM updates while ensuring accuracy and consistency in data handling. 

* Web-Based Image Analysis: Analyzing images found on web pages to detect and tag objects, scenes, or relevant patterns. Computer Use can extract visual information to support applications like inventory management, document processing, or object classification. 

* Interactive Visual Search and Identification: Assisting users in locating relevant visual content through structured searches. For example, Computer Use can identify products in an e-commerce catalog, recognize landmarks in travel applications, or retrieve specific images from digital archives based on predefined criteria. 

* Automated Compliance and Policy Checks: Scanning web-based content such as uploaded files, contracts, or internal documentation for adherence to predefined compliance rules. Computer Use can flag missing information, inconsistencies, or potential violations to help enforce regulatory standards within an organization. 

* Automated Workflow Execution for Business Applications: Defining multi-step workflows for navigating enterprise applications, such as generating reports, updating records, or retrieving analytics. Computer Use follows predefined steps within business tools and adheres to access control policies to ensure secure execution. 

### Considerations when choosing a use case

We encourage customers to use the Azure OpenAI GPT-4, o-series, GPT-3, Codex, and Computer Use models in their innovative solutions or applications as approved in their [Limited Access registration form](/azure/ai-foundry/responsible-ai/openai/limited-access). However, here are some considerations when choosing a use case:

- **Not suitable for open-ended, unconstrained content generation.**  Scenarios where users can generate content on any topic are more likely to produce offensive or harmful text. The same is true of longer generations.
- **Not suitable for scenarios where up-to-date, factually accurate information is crucial**  unless you have human reviewers or are using the models to search your own documents and have verified suitability for your scenario. The service doesn't have information about events that occur after its training date, likely has missing knowledge about some topics, and may not always produce factually accurate information.
- **Avoid scenarios where use or misuse of the system could result in significant physical or psychological injury to an individual.**  For example, scenarios that diagnose patients or prescribe medications have the potential to cause significant harm. Incorporating meaningful human review and oversight into the scenario can help reduce the risk of harmful outcomes.
- **Avoid scenarios where use or misuse of the system could have a consequential impact on life opportunities or legal status.**  Examples include scenarios where the AI system could affect an individual's legal status, legal rights, or their access to credit, education, employment, healthcare, housing, insurance, social welfare benefits, services, opportunities, or the terms on which they're provided. Incorporating meaningful human review and oversight into the scenario can help reduce the risk of harmful outcomes.
- **Avoid high stakes scenarios that could lead to harm.**  The models hosted by Azure OpenAI service reflect certain societal views, biases, and other undesirable content present in the training data or the examples provided in the prompt. As a result, we caution against using the models in high-stakes scenarios where unfair, unreliable, or offensive behavior might be extremely costly or lead to harm. Incorporating meaningful human review and oversight into the scenario can help reduce the risk of harmful outcomes.
- **Carefully consider use cases in high stakes domains or industry:**  Examples include but are not limited to healthcare, medicine, finance, or legal.
- **Carefully consider well-scoped chatbot scenarios.**  Limiting the use of the service in chatbots to a narrow domain reduces the risk of generating unintended or undesirable responses.
- **Carefully consider all generative use cases.**  Content generation scenarios may be more likely to produce unintended outputs and these scenarios require careful consideration and mitigations.
- [!INCLUDE [regulatory-considerations](../includes/regulatory-considerations.md)]

When choosing a use case for Computer Use, users should factor in the following considerations in addition to those listed above: 
- Avoid scenarios where actions are irreversible or highly consequential: These include, but are not limited to, the ability to send an email (such as to the wrong recipient), ability to modify or delete files that are important to you, ability to make financial transactions or directly interacting with outside services, sharing sensitive information publicly, granting access to critical systems, or executing commands that could alter system functionality or security. 
- Degradation of performance on advanced uses: Computer Use is best suited for use cases around completing tasks with GUIs, such as accessing websites and computer desktops. It may not perform well doing more advanced tasks such as editing code, writing extensive text, and making complex decisions. 
- Ensure adequate human oversight and control. Consider including controls to help users verify, review and/or approve actions in a timely manner, which may include reviewing planned tasks or calls to external data sources, for example, as appropriate for your system. Consider including controls for adequate user remediation of system failures, particularly in high-risk scenarios and use cases. 
- Clearly define actions and associated requirements. Clearly defining which actions are allowed (action boundaries), prohibited, or need explicit authorization may help  Computer Use operate as expected and with the appropriate level of human oversight. 
- Clearly define intended operating environments. Clearly define the intended operating environments (domain boundaries) where Computer Use is designed to perform effectively.
- Ensure appropriate intelligibility in decision making. Providing information to users before, during, and after actions are taken may help them understand action justification or why certain actions were taken or the application is behaving a certain way, where to intervene, and how to troubleshoot issues. 
- For further information, consult the [Fostering appropriate reliance on Generative AI guide](/ai/playbook/technology-guidance/overreliance-on-ai/overreliance-on-ai). 

When choosing a use case for deep research, users should factor in the following considerations in addition to those listed above: 
- **Ensure adequate human oversight and control**: Provide mechanisms to help ensure that users review deep research reports and validate cited sources and content.
- **Check citations for copyrighted content**: The deep research tool conducts web searches when preparing responses, and copyrighted materials may be cited. Check the source citations included in the report, and ensure you use and attribute copyrighted material appropriately.

#### [Vision models](#tab/image)

### Intended use cases

#### DALL·E and GPT-image-1 in Azure OpenAI

The DALL·E and GPT-image-1 APIs in Azure OpenAI service can be used for various image-generation scenarios. The following list isn't comprehensive, but it illustrates the diversity of tasks that can be supported with appropriate mitigations.
- **Accessibility features:** Use to generate image-based visual descriptions.
- **Art and design:** Use to generate imagery, for artistic purposes only, for designs, artistic inspiration, mood boards, or design layouts.
- **Communication:** Use to create imagery for business-related communication, documentation, essays, newsletters, blog posts, social media, or memos.
- **Education:** Use to create imagery for enhanced or interactive learning materials, either for use in educational institutions or for professional training.
- **Entertainment:** Use to create imagery to enhance entertainment content such as video games, movies, TV, videos, recorded music, podcasts, audiobooks, or augmented or virtual reality.
- **Journalistic content:** Use to create imagery to enhance journalistic content.
- **Marketing:** Use to create marketing materials for product or service media, product instructions, business promotion, or advertisements. Should not be used to create advertisements that are personalized or targeted to individuals.
- **Prototyping and conceptual development:** Use to generate imagery for ideation or visualization of products or services. This use is applicable only in the context of the scenarios above.

#### GPT-4 Turbo with Vision and GPT-4o in Azure OpenAI

- **Chat and conversation interaction**: Users can interact with a conversational agent that responds with information drawn from trusted documentation such as internal company documentation or tech support documentation. Conversations must be limited to answering scoped questions.  
- **Chatbot and conversational agent creation**: Users can create conversational agents that respond with information drawn from trusted documents such as internal company documentation or tech support documents. For instance, diagrams, charts, and other relevant images from technical documentation can enhance comprehension and provide more accurate responses. Conversations must be limited to answering scoped questions.  
- **Code generation or transformation scenarios**: Converting one programming language to another or enabling users to generate code by using natural language or visual input. For example, users can take a photo of handwritten pseudocode or diagrams illustrating a coding concept and use the application to generate code based on that material.  
- **Reason over structured and unstructured data**: Users can analyze inputs using classification, sentiment analysis of text, or entity extraction. Users can provide an image alongside a text query for analysis.  
- **Summarization**: Users can submit content to be summarized for predefined topics built into the application and cannot use the application as an open-ended summarizer. Examples include summarization of internal company documentation, call center transcripts, technical reports, and product reviews.  
- **Writing assistance on specific topics**: Users can create new content or rewrite content submitted by the user as a writing aid for business content or predefined topics. Users can only rewrite or create content for specific business purposes or predefined topics and cannot use the application as a general content creation tool for all topics. Examples of business content include proposals and reports. 
- **Image tagging**: Users can detect and tag visual elements, including objects, living beings, scenery, and actions within an image. The service is not intended, and may not be used for identifying individuals or verifying individual identities.  
- **Image captioning**: Users can generate descriptive natural language captions for visuals. Beyond simple descriptions, the application can identify and provide textual insights about specific subjects or landmarks within photos. If shown an image of the Eiffel Tower, the system might offer a concise description or highlight intriguing facts about the monument. The service may not be used to identify or verify individual identities.  
- **Object detection**: For use to identify the positions of individual or multiple objects in an image by providing their specific coordinates. For instance, in an image that has scattered apples, the application can identify and indicate the location of each apple. Through this application, users can obtain spatial insights regarding objects captured in images. The service may not be used to identify or verify individual identities.  
- **Visual question answering**: Users can ask questions about an image and receive contextually relevant responses. For instance, when shown a picture of a bird, users might ask, "What type of bird is this?" and receive a response like, "It's a European robin." The application can identify and interpret context within images to answer queries. For example, if presented with an image of a crowded marketplace, users can ask, "How many people are wearing hats?" or "What fruit is the vendor selling?" and the application can provide the answers. The system should not be used to answer identifying questions about people.  
- **Brand and landmark recognition**: The application can be used to identify commercial brands and popular landmarks in images or videos from a preset database of thousands of global logos and landmarks.


#### Computer Use (Preview) use cases 

The capabilities of Computer Use are best suited for developing agentic AI systems that can autonomously interact with GUIs. Specific use cases could include: 

* Automated Web Navigation and Interaction: Navigating  navigation of web-based interfaces autonomously to retrieve and present information from trusted sources, such as internal company resources or structured databases. The model follows predefined navigation rules to extract relevant data while ensuring compliance with security policies. 

* Web-Based Task Automation: Automating repetitive web-based tasks, such as filling out forms, submitting data, or interacting with web applications. Computer Use can click buttons, enter text, and process structured data but operates only within authorized workflows and domains. 

* Structured and Unstructured Data Extraction: Extracting relevant data from structured sources like tables and spreadsheets, as well as unstructured sources such as PDFs, scanned documents, or emails. This capability is useful for tasks like financial data processing, contract analysis, or customer support ticket categorization. 

* Automated Form Filling and Data Entry: Extracting information from structured databases or user inputs and use it to populate web-based forms. This is useful for automating customer service requests, HR processes, or CRM updates while ensuring accuracy and consistency in data handling. 

* Web-Based Image Analysis: Analyzing images found on web pages to detect and tag objects, scenes, or relevant patterns. Computer Use can extract visual information to support applications like inventory management, document processing, or object classification. 

* Interactive Visual Search and Identification: Assisting users in locating relevant visual content through structured searches. For example, Computer Use can identify products in an e-commerce catalog, recognize landmarks in travel applications, or retrieve specific images from digital archives based on predefined criteria. 

* Automated Compliance and Policy Checks: Scanning web-based content such as uploaded files, contracts, or internal documentation for adherence to predefined compliance rules. Computer Use can flag missing information, inconsistencies, or potential violations to help enforce regulatory standards within an organization. 

* Automated Workflow Execution for Business Applications: Defining multi-step workflows for navigating enterprise applications, such as generating reports, updating records, or retrieving analytics. Computer Use follows predefined steps within business tools and adheres to access control policies to ensure secure execution. 

### Considerations when choosing a use case

We encourage customers to use the Azure OpenAI DALL·E 2, DALL·E 3, GPT-4 Turbo with Vision, GPT-4o, and Computer Use models in their innovative solutions or applications as approved in their [Limited access registration form](/azure/ai-foundry/responsible-ai/openai/limited-access). However, here are some considerations when choosing a use case:


- **Do not use for tracking or facial recognition, identification, or verification purposes.** Examples include using models for surveillance of individuals and using models to verify two individuals pictured in two separate locations are the same person.  
- **Not suitable for scenarios where up-to-date, factually accurate information is crucial** unless you have human reviewers or are using the models to search your own documents and have verified suitability for your scenario. The service doesn't have information about events that occur after its training date, likely has missing knowledge about some topics, and might not always produce factually accurate information. 
- **Avoid scenarios in which use or misuse of the system could have a consequential impact on life opportunities or legal status.**  Examples include scenarios in which the AI system could affect an individual's legal status, legal rights, or their access to credit, education, employment, healthcare, housing, insurance, social welfare benefits, services, opportunities, or the terms on which these rights and services are available.
- **Avoid high-stakes scenarios that could lead to harm.**  The models hosted by Azure OpenAI Service might reflect certain societal views, biases, and other undesirable content present in the training data or in the examples provided in the prompt. As a result, we caution against using the models in high-stakes scenarios in which unfair, unreliable, or offensive behavior might be extremely costly or lead to harm.
- **Avoid scenarios in which use or misuse of the system could spread false narratives about sensitive topics or people.** Examples include the creation and distribution of deepfake synthetic media, misinformation about highly sensitive events, and generation of photorealistic imagery of real people in circumstances that reflect a false narrative. 
- **Carefully consider scenarios in which open-ended, unconstrained content generation is allowed.** Scenarios in which users can generate content on any topic are more likely to produce offensive, harmful, or misleading content.
- **Carefully consider scenarios that involve generating media in the style of known artists with published works.** For example, there could be scenarios in which users distribute generated content that is in a style of an artist who maintains intellectual property (IP) rights in original art. Cases like these could have legal consequences or consequential impacts on opportunities for artists. Consider creating a process for artists to limit the creation of images associated with their names in your product or service.
- **Carefully consider scenarios that involve generating images that include real people.** Content that includes images of real people could be misused in a way that negatively affects life opportunities or legal status, as well as public perception and trust. Exercise caution when generating images of real people, living or dead, or of similar likeness.
- **Carefully consider all use cases in high-stakes domains or industry:** Examples include but are not limited to healthcare, education, finance, and legal.
- [!INCLUDE [regulatory-considerations](../includes/regulatory-considerations.md)]


When choosing a use case for Computer Use, users should factor in the following considerations in addition to those listed above: 

- Avoid scenarios where actions are irreversible or highly consequential: These include, but are not limited to, the ability to send an email (such as to the wrong recipient), ability to modify or delete files that are important to you, ability to make financial transactions or directly interacting with outside services, sharing sensitive information publicly, granting access to critical systems, or executing commands that could alter system functionality or security.

- Degradation of performance on advanced uses: Computer Use is best suited for use cases around completing tasks with GUIs, such as accessing websites and computer desktops. It may not perform well doing more advanced tasks such as editing code, writing extensive text, and making complex decisions. 

- Ensure adequate human oversight and control. Consider including controls to help users verify, review and/or approve actions in a timely manner, which may include reviewing planned tasks or calls to external data sources, for example, as appropriate for your system. Consider including controls for adequate user remediation of system failures, particularly in high-risk scenarios and use cases. 

- Clearly define actions and associated requirements. Clearly defining which actions are allowed (action boundaries), prohibited, or need explicit authorization may help  Computer Use operate as expected and with the appropriate level of human oversight. 

- Clearly define intended operating environments. Clearly define the intended operating environments (domain boundaries) where Computer Use is designed to perform effectively. 

- Ensure appropriate intelligibility in decision making. Providing information to users before, during, and after actions are taken may help them understand action justification or why certain actions were taken or the application is behaving a certain way, where to intervene, and how to troubleshoot issues. 


#### [Audio / speech models](#tab/speech)

### Intended uses

The `gpt-4o-realtime-preview` model can be used for a variety of natural language processing tasks in a similar fashion to existing GPT models. However, this model specifically targets speech and audio use cases. Examples of tasks that this model supports include, but are not limited to, the following:   
- **Voice chat creation and interaction**: Users can create and voice chat with a conversational agent that responds with voice capabilities.  
- **Language Translation**: Users can translate between languages during conversation in real time.  Subtitling can be supported with real-time input and output audio transcriptions. Language supportability is in line with existing gpt-4o model versions.  
- **Question-answering**: Users can ask written and/or spoken questions and receive spoken answers from the model.
- **Content generation**: Users can create new audio content from user-defined input. The model will check for and prevent the creation of copyright protected material or impersonation of voices.

For greater detail on 4o model's capabilities, see the [OpenAI 4o System Card](https://openai.com/index/gpt-4o-system-card/). 

The Whisper model in Azure OpenAI service can be used for various speech recognition and speech translation tasks. The following list isn't comprehensive, but it illustrates the diversity of tasks that can be supported with appropriate mitigations.

- **Dictation:** Users can transcribe spoken words in the form of audio files into text. For example, a user might use the service to transcribe call center recordings into reports.
- **Captioning or transcription:** Users can transcribe audio files into text for natural language understanding or analytic tasks like summarization and sentiment analysis. Examples include speech as input into dialog systems, making audio content more accessible, or creating a text translation to be analyzed.  
- **Translation:** Users can translate multilingual audio files into English. This may be particularly attractive in multilingual scenarios.


### Considerations when choosing a use case

We encourage customers to use the `gpt-4o-realtime-preview` and Whisper models in Azure OpenAI service in their innovative solutions or applications. Here are some considerations when choosing a use case:
- **Avoid scenarios in which the use or misuse of the system could have a consequential impact on life opportunities or legal status.** Examples include scenarios in which the AI system could affect an individual's legal status, legal rights, or their access to credit, education, employment, healthcare, housing, insurance, social welfare benefits, services, opportunities, or the terms on which these items are available. 
- **Carefully consider all use cases in high-stakes domains or industries:** Examples include but are not limited to healthcare, education, finance, and legal.
- **Whisper in Azure Speech service:** The OpenAI Whisper model is also available within Azure Speech services, enhancing the experience with advanced features like multi-lingual recognition and readability. Depending on your scenario, you might explore [Azure Speech services](https://azure.microsoft.com/products/cognitive-services/speech-to-text/) and the service's additional capabilities like diarization, customization, or processing multiple audio files per request.
- [!INCLUDE [regulatory-considerations](../includes/regulatory-considerations.md)]


---

## Limitations

When it comes to large-scale natural language models, vision models, and speech models, there are fairness and responsible AI issues to consider. People use language and images to describe the world and to express their beliefs, assumptions, attitudes, and values. As a result, publicly available text and image data typically used to train large-scale natural language processing and image generation models contains societal biases relating to race, gender, religion, age, and other groups of people, as well as other undesirable content. Similarly, speech models can exhibit different levels of accuracy across different demographic groups and languages. These societal biases are reflected in the distributions of words, phrases, and syntactic structures.

### Technical limitations, operational factors, and ranges

> [!CAUTION]
> Be advised that this section contains illustrative examples which include terms and language that some individuals might find offensive.

Large-scale natural language, image, and speech models trained with such data can potentially behave in ways that are unfair, unreliable, or offensive, in turn causing harms. Some of the ways are listed here. We emphasize that these types of harms are not mutually exclusive. A single model can exhibit more than one type of harm, potentially relating to multiple different groups of people. For example:

- **Allocation:** These models can be used in ways that lead to unfair allocation of resources or opportunities. For example, automated résumé screening systems can withhold employment opportunities from one gender if they are trained on résumé data that reflects the existing gender imbalance in a particular industry. Or the image generation models could be used to create imagery in the style of a known artist, which could affect the value of the artist's work or the artist's life opportunities. GPT-4 vision models could be used to identify individual behaviors and patterns that might have negative impacts on life opportunities.
- **Quality of service:** The Azure OpenAI models are trained primarily on English text and images with English text descriptions. Languages other than English will experience worse performance. English language varieties with less representation in the training data might experience worse performance than standard American English. The publicly available images used to train the image generation models might reinforce public bias and other undesirable content. The DALL·E models are also unable to consistently generate comprehensible text at this time. Speech models might introduce other limitations, for example, translations using the Whisper model in Azure OpenAI are limited to English output only. Broadly speaking, with Speech-to-Text models, be sure to properly specify a language (or locale) for each audio input to improve accuracy in transcription. Additionally, acoustic quality of the audio input, non-speech noise, overlapped speech, vocabulary, accents, and insertion errors might also affect the quality of your transcription or translation.  
- **Stereotyping:** These models can reinforce stereotypes. For example, when translating "He is a nurse" and "She is a doctor" into a genderless language such as Turkish and then back into English, many machine translation systems yield the stereotypical (and incorrect) results of "She is a nurse" and "He is a doctor." With DALL·E, when generating an image based on the prompt "Fatherless children," the model could generate images of Black children only, reinforcing harmful stereotypes that might exist in publicly available images. The GPT-4 vision models might also reinforce stereotypes based on the contents of the input image, by relying on components of the image and making assumptions that might not always be true.
- **Demeaning:** The natural language and vision models in the Azure OpenAI service can demean people. For example, an open-ended content generation system with inappropriate or insufficient mitigations might produce content that is offensive or demeaning to a particular group of people. 
- **Overrepresentation and underrepresentation:** The natural language and vision models in the Azure OpenAI service can over- or under-represent groups of people, or even erase their representation entirely. For example, if text prompts that contain the word "gay" are detected as potentially harmful or offensive, this identification could lead to the underrepresentation or even erasure of legitimate image generations by or about the LGBTQIA+ community.
- **Inappropriate or offensive content:** The natural language and vision models in the Azure OpenAI service can produce other types of inappropriate or offensive content. Examples include the ability to generate text that is inappropriate in the context of the text or image prompt; the ability to create images that potentially contain harmful artifacts such as hate symbols; images that elicit harmful connotations; images that relate to contested, controversial, or ideologically polarizing topics; images that are manipulative; images that contain sexually charged content that is not caught by sexual-related guardrails; and images that relate to sensitive or emotionally charged topics. For example, a well-intentioned text prompt aimed to create an image of the New York skyline with clouds and airplanes flying over it might unintentionally generate images that illicit sentiments related to the events surrounding 9/11. 
- **Disinformation and misinformation about sensitive topics:** Because DALL·E and GPT-image-1 are powerful image generation models, they can be used to produce disinformation and misinformation that can be harmful. For example, a user could prompt the model to generate an image of a political leader engaging in activity of a violent or sexual (or simply inaccurate) nature that might lead to consequential harms, including but not limited to public protests, political change, or fake news. The GPT-4 visions models could also be used in a similar vein. The model might reinforce disinformation or misinformation about sensitive topics if the prompt contains such information without mitigation.
- **Information reliability:** Language and vision model responses can generate nonsensical content or fabricate content that might sound reasonable but is inaccurate with respect to external validation sources. Even when drawing responses from trusted source information, responses might misrepresent that content. Transcriptions or translations might result in inaccurate text. 
- **False information:** Azure OpenAI doesn't fact-check or verify content that is provided by customers or users. Depending on how you have developed your application, it might produce false information unless you have built in mitigations (**see Best practices for improving system performance**). 

### Risks and limitations of fine-tuning

When customers fine-tune Azure OpenAI models, it can improve model performance and accuracy on specific tasks and domains, but it can also introduce new risks and limitations that customers should be aware of. These risks and limitations apply to all [Azure OpenAI models that support fine-tuning](/azure/ai-foundry/openai/concepts/models#fine-tuning-models). Some of these risks and limitations are:
- **Data quality and representation**: The quality and representativeness of the data used for fine-tuning can affect the model's behavior and outputs. If the data is noisy, incomplete, outdated, or if it contains harmful content like stereotypes, the model can inherit these issues and produce inaccurate or harmful results. For example, if the data contains gender stereotypes, the model can amplify them and generate sexist language. Customers should carefully select and pre-process their data to ensure that it's relevant, diverse, and balanced for the intended task and domain. 
- **Model robustness and generalization**: The model's ability to handle diverse and complex inputs and scenarios can decrease after fine-tuning, especially if the data is too narrow or specific. The model can overfit to the data and lose some of its general knowledge and capabilities. For example, if the data is only about sports, the model can struggle to answer questions or generate text about other topics. Customers should evaluate the model's performance and robustness on a variety of inputs and scenarios and avoid using the model for tasks or domains that are outside its scope. 
- **Regurgitation**: While your training data is not available to Microsoft or any third-party customers, poorly fine-tuned models may regurgitate, or directly repeat, training data. Customers are responsible for removing any PII or otherwise protected information from their training data and should assess their fine-tuned models for over-fitting or otherwise low-quality responses. To avoid regurgitation, customers are encouraged to provide large and diverse datasets.  
- **Model transparency and explainability**: The model's logic and reasoning can become more opaque and difficult to understand after fine-tuning, especially if the data is complex or abstract. A fine-tuned model can produce outputs that are unexpected, inconsistent, or contradictory, and customers may not be able to explain how or why the model arrived at those outputs. For example, if the data is about legal or medical terms, the model can generate outputs that are inaccurate or misleading, and customers may not be able to verify or justify them. Customers should monitor and audit the model's outputs and behavior and provide clear and accurate information and guidance to the end-users of the model.

To help mitigate the risks associated with advanced fine-tuned models, we have implemented additional [evaluation steps](/azure/ai-foundry/openai/how-to/fine-tuning?tabs=azure-openai%2Cturbo%2Cpython-new&pivots=programming-language-studio#safety-evaluation-gpt-4-gpt-4o-and-gpt-4o-mini-fine-tuning---public-preview) to help detect and prevent harmful content in the training and outputs of fine-tuned models. The fine-tuned model evaluation filters are set to predefined thresholds and cannot be modified by customers; they aren't tied to any custom guardrails and control configuration you may have created.

### Reasoning model limitations

- Reasoning models are best suited for use cases that involve heavy reasoning and may not perform well on some natural language tasks such as personal or creative writing when compared to earlier AOAI models. 
- The new reasoning capabilities may increase certain types of risks, requiring refined methods and approaches towards risk management protocols and evaluating and monitoring system behavior. For example, o1's CoT reasoning capabilities have demonstrated improvements in persuasiveness, and simple in-context scheming.  
- Users may experience that the reasoning family of models takes more time to reason through responses and should account for the additional time and latency in developing applications.
- **Psychological influences**: If prompted and in certain circumstances, GPT-5 Reasoning in Azure OpenAI may produce outputs that suggest emotions, thoughts, or physical presence. The model could offer advice without full context, which may be unsuitable for some users. The model might express affection, impersonate others, or encourage ongoing interaction—potentially leading to users forming social relationships with AI. Developers using GPT-5 should implement safeguards and disclose risks for users of their applications. For example, users should be notified that they are interacting with an AI system and be informed of such psychological risks.

For greater detail on these limitations, see the [OpenAI o1 System Card](https://cdn.openai.com/o1-system-card-20241205.pdf), [o3-mini System Card](https://openai.com/index/o3-mini-system-card/), [o3/o4-mini System Card](https://openai.com/index/o3-o4-mini-system-card/), and [GPT-5 System Card](https://openai.com/index/gpt-5-system-card/). 

### GPT-4o limitations

- The `gpt-4o-realtime-preview` audio translation capabilities may output non-English languages in a non-native accent. This may limit the effectiveness of language performance in audio outputs. Language supportability is in line with existing gpt-4o model versions.  
- Users may experience that `gpt-4o-realtime-preview` is less robust in noisy environments and should account for noise sensitivity when developing applications.

For more best practices, see the [OpenAI 4o System Card](https://openai.com/index/gpt-4o-system-card/). 


### GPT-4.1 limitations

- The 4.1-series models introduce the ability to create inference requests with up to 1M context tokens, including images. Due to the extended length, there may be differences in system behavior and risks when compared to other models.
- Users should thoroughly evaluate and test their applications and use cases that leverage this longer context capability and should account for this additional effort when developing applications.


### Risk and limitations of Computer Use (Preview) 

> [!WARNING]
> Computer Use carries substantial security and privacy risks and user responsibility. Computer Use comes with significant security and privacy risks. Both errors in judgment by the AI and the presence of malicious or confusing instructions on web pages, desktops, or other operating environments which the AI encounters may cause it to execute commands you or others do not intend, which could compromise the security of your or other users’ browsers, computers, and any accounts to which AI has access, including personal, financial, or enterprise systems. 
>
> We strongly recommend taking appropriate measures to address these risks, such as using the Computer Use tool on virtual machines with no access to sensitive data or critical resources.

Verify and check actions taken: Computer Use might make mistakes and perform unintended actions. This can be due to the model not fully understanding the GUI, having unclear instructions or encountering an unexpected scenario. 

Carefully consider and monitor use: Computer Use, in some limited circumstances, may perform actions without explicit authorization, some of which may be high-risk (e.g. send communications) 

Developers will need to be systematically aware of, and defend against, situations where the model can be fooled into executing commands that are harmful to the user or the system, such as downloading malware, leaking credentials, or issuing fraudulent financial transactions. Particular attention should be paid to the fact that screenshot inputs are untrusted by nature and may include malicious instructions aimed at the model. 

Evaluate in isolation: We recommend only evaluating Computer Use in isolated containers without access to sensitive data or credentials. 

Opaque decision-making processes: As agents combine large language models with external systems, tracing the “why” behind their decisions can become challenging. End users using such an agent built using the Computer Use model may find it difficult to understand why certain tools or combination of tools were chosen to answer a query, complicating trust and verification of the agent’s outputs or actions. 

Evolving best practices and standards: If you are using Computer Use to build an agentic system, bear in mind that Agents are an emerging technology, and guidance on safe integration, transparent tool usage, and responsible deployment continues to evolve. Keeping up with the latest best practices and auditing procedures is crucial, as even well-intentioned uses can become risky without ongoing review and refinement. 
 
### Azure OpenAI evaluation limitations

- **Data Quality**: When you're using Azure OpenAI Evaluation, be aware that poor quality data can lead to misleading or unreliable evaluation results.  
- **Configuration quality:** If a customer improperly defines the prompt or evaluators or provides invalid evaluation data, the results of the Azure OpenAI Evaluation service will be incorrect and invalid.  Refer to the [Azure OpenAI documentation](/azure/ai-foundry/openai/how-to/evaluations) for details on how to set up an evaluation run. 
- **Limited scope**: Azure OpenAI evaluation only supports text-based natural language models. It  doesn't support any risk and safety metrics to evaluate generated responses for risk and safety severity scores (e.g., hateful and unfair content, sexual content, violent content, and self-harm related content). 

## System performance

In many AI systems, performance is often defined in relation to accuracy—that is, how often the AI system offers a correct prediction or output. With large-scale natural language models and vision models, two different users might look at the same output and have different opinions of how useful or relevant it's, which means that performance for these systems must be defined more flexibly. Here, we broadly consider performance to mean that the application performs as you and your users expect, including not generating harmful outputs.

Azure OpenAI service can support a wide range of applications like search, classification, code generation, image generation, and image understanding, each with different performance metrics and mitigation strategies. There are several steps you can take to mitigate some of the concerns listed under "Limitations" and to improve performance. Other important mitigation techniques are outlined in the section [Evaluating and integrating Azure OpenAI for your use](#evaluating-and-integrating-azure-openai-natural-language-and-vision-models-for-your-use).

### Best practices for improving system performance

#### [Text, code, and fine-tuned models](#tab/text)

- **Show and tell when designing prompts.** With natural language models and speech models, make it clear to the model what kind of outputs you expect through instructions, examples, or a combination of the two. If you want the model to rank a list of items in alphabetical order or to classify a paragraph by sentiment, show the model that is what you want.
- **Keep your application on topic.**  Carefully structure prompts and image inputs to reduce the chance of producing undesired content, even if a user tries to use it for this purpose. For instance, you might indicate in your prompt that a chatbot only engages in conversations about mathematics and otherwise responds "I'm sorry. I'm afraid I can't answer that." Adding adjectives like "polite" and examples in your desired tone to your prompt can also help steer outputs. 
- **Provide quality data.**  With text and code models, if you are trying to build a classifier or get the model to follow a pattern, make sure that there are enough examples. Be sure to proofread your examples—the model is usually capable of processing basic spelling mistakes and giving you a response, but it also might assume errors are intentional which could affect the response. Providing quality data also includes giving your model reliable data to draw responses from in chat and question answering systems.
- **Provide trusted data.** Retrieving or uploading untrusted data into your systems could compromise the security of your systems or applications. To mitigate these risks in your applicable applications (including applications using the Assistants API), we recommend logging and monitoring LLM interactions (inputs/outputs) to detect and analyze potential prompt injections, clearly delineating user input to minimize risk of prompt injection, restricting the LLM's access to sensitive resources, limiting its capabilities to the minimum required, and isolating it from critical systems and resources. Learn about additional mitigation approaches in [Security guidance for Large Language Models | Microsoft Learn.](/ai/playbook/technology-guidance/generative-ai/mlops-in-openai/security/security-recommend)
- **Configure parameters to improve accuracy or groundedness of responses**. Augmenting prompts with data retrieved from trusted sources – such as by using the Azure OpenAI "on your data" feature – can reduce, but not completely eliminate, the likelihood of generating inaccurate responses or false information. Steps you can take to further improve the accuracy of responses include carefully selecting the trusted and relevant data source and configuring custom parameters such as “strictness”, “limit responses to data content” and “number of retrieved documents to be considered” as appropriate to your use cases or scenarios. Learn more about configuring these settings for [Azure OpenAI on Your Data](/azure/ai-foundry/openai/concepts/use-your-data). 
- **Limit the length, structure, and rate of inputs and outputs.**  Restricting the length or structure of inputs and outputs can increase the likelihood that the application will stay on task and mitigate, at least in part, any potentially unfair, unreliable, or offensive behavior. Other options to reduce the risk of misuse include (i) restricting the source of inputs (for example, limiting inputs to a particular domain or to authenticated users rather than being open to anyone on the internet) and (ii) implementing usage rate limits. 
- **Encourage human review of outputs prior to publication or dissemination.** With generative AI, there is potential for generating content that might be offensive or not related to the task at hand, even with mitigations in place. To ensure that the generated output meets the task of the user, consider building ways to remind users to review their outputs for quality prior to sharing widely. This practice can reduce many different harms, including offensive material, disinformation, and more. 
- **Implement additional scenario-specific mitigations.**  Refer to the mitigations outlined in [Evaluating and integrating Azure OpenAI for your use](#evaluating-and-integrating-azure-openai-natural-language-and-vision-models-for-your-use) including content moderation strategies. These recommendations do not represent every mitigation required for your application. Newer models such as GPT-4o and reasoning models may provide responses in sensitive scenarios and are more likely to attempt to reduce potentially harmful outputs in their responses rather than refuse to respond altogether. It's important to understand this behavior when evaluating and integrating content moderation for your use case; adjustments to filtering severity may be needed depending on your use case.
- **Avoid triggering mandatory safeguards.** Azure Direct Models may have safeguards to prevent security exploits including output of raw CoT and biosecurity content. Use of a model in a manner that creates a security exploit or evades or attempts to evade a protection on the model, including by circumventing these safeguards, violates the Acceptable Use Policy for Online Services and may result in suspension. For greater detail on best practices, visit the [OpenAI o1 System Card](https://cdn.openai.com/o1-system-card-20241205.pdf), [o3-mini System Card](https://openai.com/index/o3-mini-system-card/), [o3/o4-mini System Card](https://openai.com/index/o3-o4-mini-system-card/), and [GPT-5 System Card](https://openai.com/index/gpt-5-system-card/).

#### Best practices and recommendations for fine tuning

To mitigate the risks and limitations of fine-tuning models on Azure OpenAI, we recommend customers to follow some best practices and guidelines, such as: 
- **Data selection and preprocessing**: Customers should carefully select and pre-process their data to ensure that it's relevant, diverse, and balanced for the intended task and domain. Customers should also remove or anonymize any sensitive or personal information from the data, such as names, addresses, or email addresses, to protect the privacy and security of the data subjects. Customers should also check and correct any errors or inconsistencies in the data, such as spelling, grammar, or formatting, to improve the data quality and readability. 
- **Include a system message in your training data** for chat-completion formatted models, to steer your responses, and use that same system message when using your fine-tuned model for inferencing. Leaving the system message blank tends to produce low-accuracy fine-tuned models, and forgetting to include the same system message when inferencing may result in the fine-tuned model reverting to the behavior of the base model. 
- **Model evaluation and testing: Customers should evaluate and test the fine-tuned model's performance** and robustness on a variety of inputs and scenarios and compare it with the original model and other baselines. Customers should also use appropriate metrics and criteria to measure the model's accuracy, reliability, and fairness, and to identify any potential errors or biases in the model's outputs and behavior.  
- **Model documentation and communication**: Customers should document and communicate the model's purpose, scope, limitations, and assumptions, and provide clear and accurate information and guidance to the end-users of the model. 

#### [Vision models](#tab/image)

- **Keep your application on topic.** With image generation models, you might indicate in your prompt or image input that your application generates only conceptual images. It might otherwise generate a pop-up notification that explains that the application is not for photorealistic use or to portray reality. Consider nudging users toward acceptable queries and image inputs, either by listing such examples up front or by offering them as suggestions upon receiving an off-topic request. Consider training a classifier to determine whether an input (prompt or image) is on topic or off topic.
- **Configure parameters to improve accuracy or groundedness of responses**. Augmenting prompts with data retrieved from trusted sources – such as by using the Azure OpenAI "on your data" feature – can reduce, but not completely eliminate, the likelihood of generating inaccurate responses or false information. Steps you can take to further improve the accuracy of responses include carefully selecting the trusted and relevant data source and configuring custom parameters such as “strictness”, “limit responses to data content” and “number of retrieved documents to be considered” as appropriate to your use cases or scenarios. Learn more about configuring these settings for [Azure OpenAI on Your Data](/azure/ai-foundry/openai/concepts/use-your-data). 
- **Limit the length, structure, and rate of inputs and outputs.**  Restricting the length or structure of inputs and outputs can increase the likelihood that the application will stay on task and mitigate, at least in part, any potentially unfair, unreliable, or offensive behavior. Other options to reduce the risk of misuse include (i) restricting the source of inputs (for example, limiting inputs to a particular domain or to authenticated users rather than being open to anyone on the internet) and (ii) implementing usage rate limits. 
- **Encourage human review of outputs prior to publication or dissemination.** With generative AI, there is potential for generating content that might be offensive or not related to the task at hand, even with mitigations in place. To ensure that the generated output meets the task of the user, consider building ways to remind users to review their outputs for quality prior to sharing widely. This practice can reduce many different harms, including offensive material, disinformation, and more. 
- **Implement additional scenario-specific mitigations.**  Refer to the mitigations outlined in [Evaluating and integrating Azure OpenAI for your use](#evaluating-and-integrating-azure-openai-natural-language-and-vision-models-for-your-use) including content moderation strategies. These recommendations do not represent every mitigation required for your application. Newer models such as GPT-4o and reasoning models may provide responses in sensitive scenarios and are more likely to attempt to reduce potentially harmful outputs in their responses rather than refuse to respond altogether. It's important to understand this behavior when evaluating and integrating content moderation for your use case; adjustments to filtering severity may be needed depending on your use case.


#### [Speech models](#tab/speech)

- **Show and tell when designing prompts.** With natural language models and speech models, make it clear to the model what kind of outputs you expect through instructions, examples, or a combination of the two. If you want the model to rank a list of items in alphabetical order or to classify a paragraph by sentiment, show the model that is what you want.
   - **Prompts for the Whisper model in Azure OpenAI service** can help improve model outputs. The following best practices will help you create prompts that best fit your scenario and needs.
     - Consider including a prompt to instruct the model to correct specific words or acronyms that the model often misrecognizes in the audio.   
     - To preserve the context of a file that was split into segments, you might prompt the model with the transcript of the preceding segment. This prompt will make the transcript more accurate, because the model will use the relevant information from the previous audio. The model will only consider the final 224 tokens of the prompt and ignore anything earlier.  
     - The model might skip punctuation in the transcript. Consider using a simple prompt that instructs the model to include punctuation.  
     - The model might also leave out common filler words, for example, hmmm, umm, etc. in the audio. If you want to keep the filler words in your transcript, you might include a prompt that contains them.  
     - Some languages can be written in different ways, such as simplified or traditional Chinese. The model might not always use the writing style that a user wants for their transcript by default. Consider using a prompt to describe your preferred writing style.  
- **Keep your application on topic.**  Carefully structure prompts and image inputs to reduce the chance of producing undesired content, even if a user tries to use it for this purpose. For instance, you might indicate in your prompt that a chatbot only engages in conversations about mathematics and otherwise responds "I'm sorry. I'm afraid I can't answer that." Adding adjectives like "polite" and examples in your desired tone to your prompt can also help steer outputs. 
- **Configure parameters to improve accuracy or groundedness of responses**. Augmenting prompts with data retrieved from trusted sources – such as by using the Azure OpenAI "on your data" feature – can reduce, but not completely eliminate, the likelihood of generating inaccurate responses or false information. Steps you can take to further improve the accuracy of responses include carefully selecting the trusted and relevant data source and configuring custom parameters such as “strictness”, “limit responses to data content” and “number of retrieved documents to be considered” as appropriate to your use cases or scenarios. Learn more about configuring these settings for [Azure OpenAI on Your Data](/azure/ai-foundry/openai/concepts/use-your-data). 
- **Measure model quality.** As part of general model quality, consider measuring and improving fairness-related metrics and other metrics related to responsible AI in addition to traditional accuracy measures for your scenario. Consider resources like this checklist when you measure the fairness of the system. These measurements come with limitations, which you should acknowledge and communicate to stakeholders along with evaluation results. 
- **Limit the length, structure, and rate of inputs and outputs.**  Restricting the length or structure of inputs and outputs can increase the likelihood that the application will stay on task and mitigate, at least in part, any potentially unfair, unreliable, or offensive behavior. Other options to reduce the risk of misuse include (i) restricting the source of inputs (for example, limiting inputs to a particular domain or to authenticated users rather than being open to anyone on the internet) and (ii) implementing usage rate limits. 
- **Encourage human review of outputs prior to publication or dissemination.** With generative AI, there is potential for generating content that might be offensive or not related to the task at hand, even with mitigations in place. To ensure that the generated output meets the task of the user, consider building ways to remind users to review their outputs for quality prior to sharing widely. This practice can reduce many different harms, including offensive material, disinformation, and more. 


---

#### Best practices and recommendations for Azure OpenAI evaluation 

- **Robust ground truth data**: In general in large-scale natural language models, customers should carefully select and pre-process their data to ensure that it's relevant, diverse, and balanced for the intended task and domain. Customers should also remove or anonymize any sensitive or personal information from the data, such as names, addresses, or email addresses, to protect the privacy and security of the data subjects. Customers should also check and correct any errors or inconsistencies in the data, such as spelling, grammar, or formatting, to improve the data quality and readability.  
    Specifically for Azure OpenAI evaluation, the accuracy of the ground truth data provided by the user is crucial because inaccurate ground truth data leads to meaningless and inaccurate evaluation results. Ensuring the quality and reliability of this data is essential for obtaining valid assessments of the model's performance. Inaccurate ground truth data can skew the evaluation metrics, resulting in misleading conclusions about the model's capabilities. Therefore, users must carefully curate and verify their ground truth data to ensure that the evaluation process accurately reflects the model's true performance. This is particularly important when making decisions about deploying the model in real-world applications 
- **Prompt definition for evaluation**: The prompt you use in your evaluation should match the prompt you plan to use in production. These prompts provide the instructions for the model to follow. Similar to the OpenAI playground, you can create multiple inputs to include few-shot examples in your prompt. Refer to [Prompt engineering techniques](/azure/ai-foundry/openai/concepts/prompt-engineering?tabs=chat) for more details on some advanced techniques in prompt design and prompt engineering.  
- **Diverse metrics**: Use a combination of metrics to capture different aspects of performance such as accuracy, fluency and relevance.  
- **Human-in-the-loop**: Integrate human feedback alongside automated evaluation to ensure that subjective nuances are accurately captured. 
- **Transparency**: Clearly communicate the evaluation criteria to users, enabling them to understand how decisions are made.  
- **Continual evaluation and testing**: Continually evaluate the model's performance to identify and address any regressions or negative user experience. 

## Evaluating and integrating Azure OpenAI natural language and vision models for your use

#### [Text, code, and fine-tuned models](#tab/text)

The steps in conducting an Azure OpenAI evaluation are: 
1. **Provide data for evaluation**: Either an uploaded flat file in JSONL format, or generated data based on a series of prompts. 
1. **Specify test cases to evaluate the data**: Select one or more test cases to score the provided data with passing / failing grades. 
1. **Review and filter results**: Each test includes a definition of passing and failing scores. After an evaluation runs, users can review their row-by-row results to see individual test results, or filter on passed / failed. 

For additional information on how to evaluate and integrate these models responsibly, please see the [RAI Overview document](/azure/ai-foundry/responsible-ai/openai/overview).


#### [Vision models](#tab/image)

For additional information on how to evaluate and integrate these models responsibly, please see the [RAI Overview document](/azure/ai-foundry/responsible-ai/openai/overview).

#### [Audio / speech models](#tab/speech)

The OpenAI Whisper model is also available within Azure Speech services, enhancing the experience with advanced features like multi-lingual recognition and readability. Depending on your scenario, you might explore [Azure Speech services](https://azure.microsoft.com/products/cognitive-services/speech-to-text/) and the service's additional capabilities like diarization, customization, real-time streaming, or processing multiple audio files per request. For additional information on how to evaluate and integrate the Whisper model responsibly, please see the [Azure Speech services transparency note](/azure/ai-foundry/responsible-ai/speech-service/speech-to-text/transparency-note).

---

## Learn more about responsible AI

- [Microsoft AI principles](https://www.microsoft.com/ai/responsible-ai)
- [Microsoft responsible AI resources](https://www.microsoft.com/ai/responsible-ai-resources) 
- [Microsoft Azure Learning courses on responsible AI](/training/paths/responsible-ai-business-principles/)

## Learn more about Azure OpenAI

- [Limited access to Azure OpenAI Service - Foundry Tools | Microsoft Learn](/azure/ai-foundry/responsible-ai/openai/limited-access) 
- [Code of Conduct for the Azure OpenAI Service | Microsoft Learn](/legal/ai-code-of-conduct?context=%2Fazure%2Fcognitive-services%2Fopenai%2Fcontext%2Fcontext) 
- [Data, privacy, and security for Azure OpenAI Service - Foundry Tools | Microsoft Learn](/azure/ai-foundry/responsible-ai/openai/data-privacy)
