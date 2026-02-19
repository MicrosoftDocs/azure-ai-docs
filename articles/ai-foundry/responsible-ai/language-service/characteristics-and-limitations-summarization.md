---
title: Characteristics and limitations for summarization
titleSuffix: Foundry Tools
description: System characteristics and limitations for summarization 
author: laujan
ms.author: lajanuar
manager: nitinme
ms.service: azure-ai-language
ms.topic: concept-article
ms.date: 04/09/2022
---

# Characteristics and limitations for Summarization

[!INCLUDE [non-english-translation](../includes/non-english-translation.md)]

Large-scale, natural language models are trained with publicly available text data which typically contain societal biases. Such data can potentially behave in ways that are unfair, unreliable, or offensive. This behavior, in turn, may cause harms of varying severities. These types of harms aren't mutually exclusive. A single model can exhibit more than one type of harm, potentially relating to multiple groups of people. For example:

* **Allocation:** It's possible to use language models in ways that lead to unfair allocation of resources or opportunities. For example, automated systems that screen resumes can withhold employment opportunities from women, if these systems are trained on resume data that reflects the existing gender imbalance in the technology industries.

* **Quality of service:** Language models can fail to provide the same quality of service to some people as they do to others. For example, summary generation can work less well for some dialects or language varieties, because of their lack of representation in the training data. The models are trained primarily on English text. English language varieties less well represented in the training data might experience worse performance.

* **Stereotyping:** Language models can reinforce stereotypes. For example, when translating *He is a nurse* and *She is a doctor* into a genderless language, such as Turkish, and then back into English, you can get an error. Many machine translation systems yield the stereotypical (and incorrect) results of *She is a nurse* and *He is a doctor*.

* **Demeaning:** Language models can demean people. For example, an open-ended content generation system with inappropriate mitigation might produce offensive text, targeted at a particular group of people.

* **Over- and underrepresentation:** Language models can over- or under-represent groups of people, or even erase them entirely. For example, toxicity detection systems that rate text containing the word *gay* as toxic might lead to the under-representation, or even erasure, of legitimate text written by or about the LGBTQ community.

* **Inappropriate or offensive content:** Language models can produce other types of inappropriate or offensive content. Examples include:

  - Hate speech.
  - Text that contains profane words or phrases.
  - Text that relates to illicit activities.
  - Text that relates to contested, controversial, or ideologically polarizing topics.
  - Misinformation.
  - Text that's manipulative.
  - Text that relates to sensitive or emotionally charged topics.

  For example, [suggested-reply systems that are restricted to positive replies](https://www.microsoft.com/research/uploads/prod/2021/02/assistiveWritingBiases-CHI.pdf) can suggest inappropriate or insensitive replies for messages about negative events.

* **False information:** The service doesn't check facts or verify content provided by customers or users. Depending on how you've developed your application, it might promote false information unless you've built in an effective mitigation for this possibility.

* **Inaccurate summary:** The feature uses an *abstractive* summarization method, in which the model doesn't simply extract contexts from the input text. Instead, the model tries to understand the input and paraphrase the key information in succinct natural sentences. However, there can be information or accuracy loss.

* **Genre consideration:** The training data used to train the summarization feature in Foundry Tools for language is mainly texts and transcripts between two participants. The model might perform with lower accuracy for the input text in other types of genres, such as documents or reports, which are less represented in the training data.

* **Language support:** Most of the training data is in English, and in other commonly used languages like German and Spanish. The trained models might not perform as well on input in other languages, because these languages are less represented in the training data. Microsoft is invested in expanding the language support of this feature.

## Best practices for improving system performance

The performance of the models varies based on the scenario and input data.  The following sections are designed to help you understand key concepts about performance. 

### [Document summarization](#tab/document)

You can use document summarization in a wide range of applications, each with different focuses and performance metrics. Here, we broadly consider performance to mean the application performs as you expect, including the absence of harmful outputs. There are several steps you can take to mitigate some of the concerns mentioned earlier in this article, and to improve performance:

*Because the document summarization feature is trained on document-based texts, such as news articles, scientific reports, and legal documents, when used with texts in different genres that are less represented in the training data, such as conversations and transcriptions, the system might product output with lower accuracy.
* When used with texts that may contain errors or are less similar to well-formed sentences, such as texts extracted from lists, tables, charts, or scanned in via OCR (Optical Character Recognition), the document summarization feature may produce output with lower accuracy.
* Most of the training data is in commonly used languages such as English, German, French, Chinese, Japanese, and Korean. The trained models may not perform as well on input in other languages.
* Documents must be "cracked," or converted, from their original format into plain and unstructured text.
* Although the service can handle a maximum of 25 documents per request, the latency performance of the API increases with larger documents (it becomes slower). This is especially true if the documents contain close to the maximum 125,000 characters. [Learn more about system limits](/azure/ai-services/language-service/concepts/data-limits)
* The extractive summarization gives a score between 0 and 1 to each sentence and returns the highest scored sentences per request. If you request a three-sentence summary, the service returns the three highest scored sentences. If you request a five-sentence summary from the same document, the service returns the next two highest scored sentences in addition to the first three sentences.
* The extractive summarization returns extracted sentences in their chronological order by default. To change the order, specify sortBy. The accepted values for sortBy are Offset (default). The value of Offset is the character positions of the extracted sentences and the value of Rank is the rank scores of the extracted sentences. 

### [Conversation summarization](#tab/conversation)

You can use conversation summarization in a wide range of applications, each with different focuses and performance metrics. Here, we broadly consider performance to mean the application performs as you expect, including the absence of harmful outputs. There are several steps you can take to mitigate some of the concerns mentioned earlier in this article, and to improve performance:

* **Service limit:** Understand that there are some limits enforced on the user, such as the number of conversations per request, and the length of a conversation. For more information, see the [system limits](/azure/ai-services/language-service/concepts/data-limits).

* **Provide quality input:** The model is to summarize your input, so the quality of your input is critical to the generated summary output. It's a good idea to have some measurements in place to ensure a good quality of input. This reduces the likelihood of unfair, unreliable, or offensive output.

* **Measure model quality:** As part of general model quality, consider measuring and improving fairness-related metrics, and other metrics related to responsible AI, in addition to traditional accuracy measures for your scenario. These measurements come with limitations, which you should acknowledge and communicate to stakeholders, along with your evaluation results. Here's a [checklist on GitHub](https://github.com/marcotcr/checklist) that might be useful to you when you measure the fairness of the system.

* **Implement additional, scenario-specific mitigation:** You might want to use content moderation strategies, such as those referred to in the article on integration and responsible use of summarization. These strategies aren't comprehensive, but they're often a good starting point, and are similar to what Microsoft checks for when evaluating use cases for this service.

---

## Next steps

* [Transparency note for Azure Language in Foundry Tools](/azure/ai-foundry/responsible-ai/language-service/transparency-note)
* [Transparency note for named entity recognition](/azure/ai-foundry/responsible-ai/language-service/transparency-note-named-entity-recognition)
* [Transparency note for health](/azure/ai-foundry/responsible-ai/language-service/transparency-note-health)
* [Transparency note for key phrase extraction](/azure/ai-foundry/responsible-ai/language-service/transparency-note-key-phrase-extraction)
* [Transparency note for sentiment analysis](/azure/ai-foundry/responsible-ai/language-service/transparency-note-sentiment-analysis)
* [Guidance for integration and responsible use with language](/azure/ai-foundry/responsible-ai/language-service/guidance-integration-responsible-use)
* [Data privacy for language](/azure/ai-foundry/responsible-ai/language-service/data-privacy)
