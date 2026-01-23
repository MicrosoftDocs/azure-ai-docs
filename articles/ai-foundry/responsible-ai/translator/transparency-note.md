---
title: Azure Translator in Foundry Tools Transparency Note
titleSuffix: Foundry Tools
description: Azure Translator in Foundry Tools Responsible AI Basics, use cases, terms
author: laujan
ms.author: lajanuar
manager: nitinme
ms.service: azure-ai-translator
ms.topic: concept-article
ms.date: 05/12/2024
---

# Azure Translator in Foundry Tools Transparency Note

[!INCLUDE [non-english-translation](../includes/non-english-translation.md)]

An artificial intelligence (AI) system includes not only the technology but also the people who will use it, the people who will be affected by it, and the environment in which it is deployed. Creating a system that is fit for its intended purpose requires an understanding of how the technology works, what its capabilities and limitations are, and how to achieve the best performance. Microsoft Transparency Notes are intended to help you understand how our AI technology works, the choices system owners can make that influence system performance and behavior, and the importance of thinking about the whole system, including the technology, the people, and the environment. You can use Transparency Notes when developing or deploying your own system or share them with the people who will use or be affected by your system.  

Microsoft Transparency Notes are part of a broader effort at Microsoft to put our AI principles into practice. To find out more, see [the Microsoft AI principles](https://www.microsoft.com/ai/responsible-ai).

## The basics of Azure Translator in Foundry Tools

## Introduction

Translator is an AI service that translates text from one natural language to another. In machine learning literature this process is called machine translation. Applying AI techniques has made machine translation between languages significantly better over the past 70 years of machine translation research, to the point that we can present the result of machine translation to human recipients for direct consumption, without edits, in some use cases.

Translator provides an API that allows you to translate from one language to another language, or to multiple languages at once. 

Internally, each language translation is performed as a separate act. You may translate between any of the more than [135 languages and dialects](https://aka.ms/TranslatorLanguages) offered by Translator. 

Training translation systems is dependent on data availability between language pairs. We build either bilingual systems (translation systems between two languages) or multilingual systems (translation systems across multiple related languages). Based on model quality, the service will pick the optimal path for a particular translation requested by the user.

Translation between some pairs might involve a pivot through a third language. For example, translation between Swahili and Hindi might involve translation from Swahili to English followed by translation from English to Hindi. This process is done automatically within the service. 

## Key terms

| Term | Definition |
|--|--|
|**Character**| Translator API counts every code point defined in Unicode as a character.|
|**Text phrase** |A sentence that’s either complete or partial.|
|**Document** |A collection of text in a digital file format including but not limited to Word document, Excel spreadsheet, PowerPoint presentation, Adobe PDF, HTML, Text, and Markdown.|
| **Style and register** | The manner of spelling/punctuation of the text, which can affect translation quality.|

## Capabilities

### System behavior

Translator has capabilities to:
- Translate text into multiple languages.
- Transliterate text from one script to another.
- Asynchronously translate batches of large documents into multiple languages that retain structure and layout as in the source document.
- Synchronously translate a small single document into one target language that retains structure and layout as in the source document.

### Use cases

#### Intended uses

The following classes of translation use cases are provided to help you think through your own scenarios:

**Outbound translation**: A publisher of information provides documents or text in multiple languages, addressing the target audience in the recipient’s language. There are different classes and formats of outbound material, for example, marketing flyers, informational videos, or factory floor manuals. Machine translation is more suitable for some classes than for others. As a general rule, the suitability of machine translation is inversely proportional to the creativity of the content. The translation can be published as web content, an electronic document, or as video subtitles or dubbing or be printed on paper.
- **Raw translation**: Publish the translation as delivered by the machine translation system. This use case carries the lowest cost and comes with a non-negligible error rate. There should be mechanisms in place to react to mistranslations, such as consumer feedback.
- **Post-edited translation**: Publish the post-edited translation, which is the machine translation result corrected by a human reviewer. Human intervention increases the cost over raw translation by a factor of more than 1,000, but it significantly reduces the error rate and improves the fluency and understandability of the translation.

**Inbound translation**: Someone receives information in a foreign language and uses Translator to translate the information into their native language. Examples are websites, product reviews, financial and business reports, or bug reports arriving in a foreign language. The tolerance for translation errors might be higher in this use case, but the translation might induce significant misunderstandings in a non-negligible number of cases. Often in this scenario, a machine translation is better than no translation. An individual or a business could automatically filter or classify to extract information, or to apply other AI techniques on documents from a variety of sources, including foreign language documents. Examples could be media monitoring, multilingual virtual assistants, or e-Discovery. The recipient applies machine translation before passing the document to the automatic analysis. Most of the time, this process is fully automated with no human intervention.

**Bidirectional translation**: Two or more humans who do not speak the same language employ machine translation in a live chat over instant messaging or in a spoken conversation. For example, a support agent doesn’t speak the same language as the customer seeking help.

**Sequencing multiple Foundry Tools**:
- **Speech translation**: Azure Speech, another one of the Foundry Tools, can translate speech between languages. Speech generates the transcript in the same language as the original speech and then internally employs Translator to translate the transcript. Use cases include translated human-to-human speech conversation, dubbing, or subtitling of content.
- **Translation of text in images**: Azure Computer Vision, another Foundry Tool, can extract visible text from images. This extracted text can then be translated. Use cases include translation of scanned documents, menus, and signs.

#### Considerations when choosing other use cases

The translation quality will be influenced by the suitability of the content being translated. The style and register of the text being translated and the purpose and use case determine the suitability:

**Consider using**: content that is correctly spelled and punctuated and is accurate and fluent. Examples of such content include:
- Technical documentation
- Product manuals
- Knowledge bases
- Website content

**Carefully consider using**: Translation of nonprofessionally authored material. Examples include:
- Colloquial writing
- Transcribed speech
- Social media chat

**Carefully consider applying human review when sensitive data or scenarios are involved**: It's important to include a human in the loop for a manual review when you're dealing with high-stakes scenarios (e.g affecting someone's consequential rights) or sensitive data. Machine translation may make mistakes. Consider carefully when to include a manual review step for certain workflows. For example, translating medical records should include human oversight.

**Carefully consider when using for awarding or denying of benefits**: Translator was not designed or evaluated for the award or denial of benefits, and use in these scenarios may have unintended consequences. These scenarios include: 
- Medical insurance: This would include using translated healthcare records and medical prescriptions as the basis for decisions on insurance reward or denial.
- Loan approvals: These include translating applications for new loans or refinancing of existing ones.

**Unsupported uses**:
- Legal documents: Mistranslated contracts lead to failure to comply with contracts.
- Creative content, such as marketing materials, poetry, and fiction: Translation won’t convey creativity.

[!INCLUDE [regulatory-considerations](../includes/regulatory-considerations.md)]

## Limitations

Machine translation can be a cost-efficient method of providing translations of large volumes of content in a much shorter time. Machine translation costs less than 1/1,000th of human translation and is faster, but it can make mistakes.

Custom machine translation models typically produce significantly better-quality output with a small number of terminology errors. These machine translation models are trained with large enough and good enough previous translations that are customer specific.

### Technical limitations, operational factors and ranges

#### Full document context 

Full document translation systems are in development, but most of the generally available machine translation systems in existence today, including ours, process a document sentence by sentence. When today’s systems translate a sentence, most of them have no knowledge of the previous or subsequent sentences in the same document.  Information necessary to correctly translate a sentence (for example, pronoun gender and number) might only be available at the document level, resulting in a mistranslation.

**Example**:
1. **English**: The sun was about to set. It was still shining brightly.
1. **Machine translation to German**: Die Sonne stand kurz vor dem Untergehen. Es leuchtete noch hell.

The “sun” in German has female gender. The machine translation in this example used neutral gender.

In translations from a genderless original to a gendered translation, the translation system assumes a gender. It tries to produce a fluent and grammatically correct sentence in the target language. When the system uses a gender, it applies a bias toward the gender that was prevalent for the given context in the material used to train the system. This practice can lead to mistakes.

Genderless constructs occur in a wide variety of languages, including Chinese, Finnish, Tamil, Turkish, and Vietnamese.

#### Sequencing multiple Foundry Tools

When sequencing multiple services that each have a nonzero error rate, the errors compound. The translation of speech recognition or optical character recognition (OCR) results won’t be able to recover from a mistake in the recognition step and will add its own mistakes following the recognition.
  
#### Mixed language input

Each translation request translates from one language to another language. If multiple languages are in the source text of a single translation request, the translation of the text in the target language might be suboptimal. It might be left as is, be mistranslated, be translated correctly, or it might be transliterated correctly or incorrectly.

Translator can automatically detect the language of the source text, but it applies the detected language to the entire text.

#### Real-world knowledge 

A machine translation system is trained on previously translated documents. The system only uses what can be learned from the individual sentences of the training documents; it doesn't have a broader context.

This lack of real-world knowledge can cause several mistakes, such as:
- Translations are too literal, not reflecting the implication, nuance, or inuendo of the original.
- Idioms and expressions that aren’t meant literally don’t express the implied meaning of the original. An English example is “Knocking it out of the ballpark.”
- When a translation requires a culture-aware modification of the original, it might not be reflected appropriately. This mistake could occur for a currency conversion, date or time format conversion, change of the name of the language when the official language of a region is meant, or change of the region, for proper localization of the target document.
- Titles and ranks of individuals are potentially not reflected appropriately, for instance, when translated from a foreign language to the culture of the individual.
- The tone and mood (angry, calm, excited, sad) of the original might not be reflected appropriately. Typically, the automatic translation is more neutral and less colorful than the original.
- The age, title, relationship, or experience of someone addressed in a conversation might not be reflected appropriately. This mistake is especially significant when translating from a language where the way to address someone is relatively independent of the age and relationship, like “you” in English, to a language where there are multiple options, like “tu” and “vous” in French. Which form of address to use is almost always relevant. The translation system will pick the term that matches its training data best, based on the short context it sees within the sentence, but it won’t know, for example, if the conversation participants are related, even if that information is mentioned elsewhere in the document.

#### High-severity errors

High-severity errors are defined as errors that can tarnish the reputation of the person or institution speaking in a translated voice, or in a translated text or a document, whether it's human or machine translated. A high-severity error is embarrassing to the speaker or author, or can lead to a wrong conclusion with significant consequences. A bad translation or a grammar mistake alone doesn’t qualify as a high-severity error. Most mistakes in the machine translation can be corrected by the reviewer based on context. A high-severity error leads to a tangible negative effect.

Examples of potential high-severity errors:
- **Inverted negation**: The original text says not to do something; however, the translation says to do it. Or the original states a fact but the translation states the opposite. Complex sentences and double negatives can cause this error.
- **Changed number or unit of measurement**: A dimension indicator, unit of measurement, or currency (inch, pound, centimeter, pennies) gets incorrectly translated, which can lead to an incorrect measurement or an undue loss or gain of funds.
- **Falsified person names and titles**: The wrong title is applied to a person, for example, “King,” where it should be “Crown Prince.” In a politically sensitive environment, this error might lead to significant embarrassment.
- **Religious figures or symbols placed in unfavorable context**: Ambiguity in the original material can lead to a translation that shows a significant religious figure or a relevant symbol in an unfavorable light. It can be as simple as a phrase with a religious connotation appearing as the translation, or a non-word such as an abbreviation, a typo, or meaningless input.
- **Omissions and ungrounded content**: Machine translation might omit a portion of the source content or add a concept that wasn’t present in the original. Neural networks have the ability to produce very fluent sentences. An unusual or disfluent source sentence might be translated into a fluent target sentence that doesn’t reflect the original accurately or might be completely unrelated to the source.
- **Offense**: A literal translation of an idiom or of a neutral expression could turn more aggressive or offensive. Some expressions don’t have a cultural equivalent in the target language. For example, “Break a leg” is a wish for good luck for a stage performance. The system might not be aware of the full context to come up with a fitting translation.

With today’s machine translation systems, high-severity errors are rare. The fear of a reputation-harming mistake is a major obstacle to publishing raw, unedited machine translation. While the risk of high-severity errors might be low for more compatible language pairs, a developer will want to use techniques to reduce the effect if one should happen. Currently, human translators are better equipped to find and correct high-severity errors than machines. Adding a human review step to find and fix high-severity errors in the machine translation is a way to address this limitation. You might also consider adding a human review on request or based on business intelligence metrics, such as user ratings, audience, or the importance of the content, after publishing the document unreviewed.  
  
#### Bias

Today’s machine translation systems are built on machine learning algorithms. Translation systems learn how to translate from previously translated documents. What the system has learned is stored in a probabilistic model, which is typically a neural network. The runtime that handles a translation request refers to that neural network to produce what it determines is the best candidate among possible translations for the given input. This translation will reflect the domain, terminology, style, and bias that was present in the original training material. This bias can be very subtle. In some language pairs, for instance, when translating a sentence without a subject pronoun, the system makes up a pronoun because the target language’s grammar requires a subject. The gender of that made-up pronoun will be influenced by the context found in the training material, regardless of the actual gender of the subject in the document being translated. This issue is an area of active research, and we are working to address bias-related issues.

Examples of potential biases in machine translation:
- **Gender bias**: When translating from a gender-neutral language to a strongly gendered language, the chosen pronouns will be influenced by the context found in the training material, which might not reflect the actual gender of the actor.
- **Political bias**: Phrases or word choices with a political bias in one language don’t necessarily translate with the same bias or connotation in the other language.
- **Religious bias**: Like political bias, the choice of words can indicate a specific viewpoint, a certain belief, or a dogma. When switching languages, that viewpoint might be added or removed or altered to a different interpretation.
- **Sexual orientation, national origin, ethnicity, race**: The terms that society applies to groups within that society change over time. A discriminatory term written in an original document might have persisted in the training material and might surface in the translation in a damaging context.
- **Profanity**: What is considered profane within a culture changes over time. The intent of the translation system is to maintain the profane or nonprofane nature of the expression in the input. That level of accuracy doesn’t work with 100% reliability because many profane terms are in fact ambiguous, and the degree of profanity of the translated term varies between the involved languages.

## System performance

- Translator API has no limits on concurrent requests.
- Translator API sets various quota on count of characters that can be translated in an hour by a translator resource based on the SKU licensed by the customer. The quota limits vary from 40 million characters per hour to 200 million characters per hour.
- Translator has a maximum latency of 15 seconds by using standard models. Typically, responses for text within 100 characters are returned in 150 milliseconds to 300 milliseconds.
- Translator API response times vary based on the size of the request and language pair.
   - Translation between a language and English is faster than translation between any two non-English languages.

### Best practices for improving system performance 

- Users can get best performance on translating a text phrase into multiple target languages by making individual requests for each language rather than making a single request for multiple languages. This approach helps users to consume available translations instead of waiting for all translations to return by the system.
- If your volume of translation is high, switch to higher commitment or volume tiers. 

## Evaluation of Translator 

### Evaluation methods

Translation quality is always relative to a test set. There are no established standard translation test sets for benchmarking. For this reason, we don’t publish the absolute scores of our own measurements of the machine translation systems.

Today’s neural network-based machine translation systems can produce fluent and grammatically correct sentences, given a suitable source. However, the quality of machine translation systems differs by language pair. We can determine whether a certain class of documents is suitable for machine translation for a specific language pair.

We recommend that you measure quality for a representative test set for a given scenario. The tolerance level of mistranslation by language varies by scenario. The expectation of linguistic, formal, and colloquial translation also varies by scenario.

### Evaluation results

There are many ways to measure quality. Automatic techniques calculate the distance to a human-created reference translation. The Bi-lingual Evaluation Understudy (BLEU) score is the oldest technique and is still popular. Other techniques employ a trained language model to measure the distance to sequences and context stored in the model, like the Cross-lingual Optimized Metric for Evaluation of Translation (COMET). In a human evaluation, the evaluators judge the translation on one or more criteria, for instance, accuracy and fluency. We continuously measure Translator quality by using a multitude of techniques. Human evaluation provides the most significant and reliable scores.

## Evaluating and integrating Translator for your use

As Microsoft works to help customers safely develop and deploy solutions by using Translator, we are taking a principled approach to upholding personal agency and dignity by considering the AI systems' fairness, reliability & safety, privacy & security, inclusiveness, transparency, and human accountability. These considerations are in line with our commitment to developing responsible AI.  
  
When you're getting ready to integrate and use AI-powered products or features, keep the following principles in mind:
- **Application predevelopment recommendations**: We recommend that developers start by conducting an impact assessment to understand the intended use, context, and unintended or high-risk uses to avoid.
- **Understand what it can do**: Fully assess Translator to understand its capabilities and/or limitations. Microsoft's testing might not reflect your scenario. Understand how it will perform in your particular scenario by thoroughly testing it with real-life conditions and diverse user data that reflect your context, including fairness considerations.

**Human in the loop**: Include human oversight as a consistent pattern area to explore. This approach means ensuring constant human oversight of Translator and maintaining the role of humans in decision-making. Ensure that you can have real-time human intervention in the solution to prevent harm. This capability enables you to manage where Translator doesn’t perform as required. 
- **Quality measurements**: We recommend that you measure translation quality for a representative test set for a given scenario. The tolerance level of mistranslation by language varies by scenario. The expectation of linguistic, formal, and colloquial translation also varies by scenario. For more information, see the next section.
- **Respect an individual’s right to privacy**: Translator doesn’t retain the content that customers submit for translation. We recommend against retaining content and information received from your app users to respect individuals' right to privacy.
- **Legal review**: Obtain appropriate legal advice to review your solution, particularly if you plan to use it in sensitive or high-risk applications. Understand what restrictions you might need to work within and your responsibility to resolve any future issues.
- **Security**: Ensure that your solution is secure and has adequate controls to preserve the integrity of your content and prevent unauthorized access.
- **Customer feedback loop**: Provide a feedback channel that allows users and individuals to report issues with the service after it’s been deployed. After you’ve deployed Translator, it requires ongoing monitoring and improvement. Be ready to implement any feedback and suggestions for improvement.

### **Human in the loop**

A responsible introduction of machine translation includes the option to conduct a human review and correct the automatic translation.

Human reviewers have real-world knowledge, subject matter expertise, and a natural sensitivity for potentially controversial words and phrases. Humans can identify the relevant context and produce a translation that reflects the appropriate tone for a given situation. Machines are more limited in their ability to apply tone and context correctly.

It’s beneficial to prepare for infrastructure that can execute a human review quickly and efficiently. This type of system is called a translation management system (TMS). TMSs are available from many suppliers. Microsoft doesn’t sell a TMS. Translator is integrated into several TMSs.

Human review is an expensive undertaking. For optimal use of funds and immediate availability of documents to a target audience, you should identify indicators based on intended use or business intelligence. These indicators can suggest that the article or element of a document needs a human review.

Examples of business intelligence signals:
- **Page views**: The publisher of translated information decides on a threshold measured in page views of the translated information. If the machine-translated information passes the defined page-view threshold, the system triggers a human review of this content. Human review can reduce the exposure of a bad translation to additional viewers or customers.
- **User escalation**: The recipient of the translation can provide feedback or issue an alert on a bad, misleading, or offensive translation. This escalation triggers a human review of the content in question.
- **Employee escalation**: An employee at the publisher of translated information might issue a request to human review an article.
- **Importance or value of the item**: An article about or a description of a low-priced and low-volume item for sale might not be economically feasible to be translated by a human. However, a higher-value item can well justify the expense of a human translation. The high value might automatically trigger a human review of the translation.
- **Suitability**: Some classes of documents translate with better quality than others. A publisher can use automatic scoring mechanisms or classification of the document content to determine whether this document needs a human review. Microsoft Azure offers some techniques for content-based classification, like Language Understanding and Text Analytics. Translator doesn’t return a confidence score for its translations.

## Next steps

* [Data, privacy, and security](/azure/ai-foundry/responsible-ai/translator/data-privacy-security)

