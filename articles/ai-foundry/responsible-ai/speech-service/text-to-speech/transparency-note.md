---
title: Text to speech transparency note
titleSuffix: Foundry Tools
description: This Transparency Note discusses Text to speech and the key considerations for making use of this technology responsibly.
author: PatrickFarley
manager: nitinme
ms.author: pafarley
ms.service: azure-ai-speech
ms.topic: concept-article
ms.date: 11/14/2023
---

# Transparency note: text to speech 

[!INCLUDE [non-english-translation](../../includes/non-english-translation.md)]

## What is a Transparency Note? 

An AI system includes not only the technology, but also the people who will use it, the people who will be affected by it, and the environment in which it is deployed. Creating a system that is fit for its intended purpose requires an understanding of how technology works, what its capabilities and limitations are, and how to achieve the best performance. Microsoft’s Transparency Notes are intended to help you understand how our AI technology works, the choices system owners can make that influence system performance and behavior, and the importance of thinking about the whole system, including the technology, the people, and the environment. You can use Transparency Notes when developing or deploying your own system or share them with the people who will use or be affected by your system. 

Microsoft’s Transparency Notes are part of a broader effort at Microsoft to put our AI Principles into practice. To find out more, see [the Microsoft AI principles](https://www.microsoft.com/ai/responsible-ai). 

## The basics of text to speech 

### Introduction 

[Text to speech](/azure/ai-services/speech-service/text-to-speech), part of Azure Speech in Foundry Tools, is a versatile tool that can convert written text into natural-sounding speech audio. The feature takes input in the form of text and generates high-quality speech audio output that can be played on devices. For the speech audio output, text to speech offers a range of prebuilt neural voices or, for Limited Access customers, the option to create a custom neural voice for your product or brand.

Text to speech also has visual capabilities. Using text to speech avatar, customers can input text and create a synthetic video of an avatar speaking. Both prebuilt text to speech avatars and custom text to speech avatars are available, which can be used with both prebuilt neural voice and custom neural voice, though some features are only available for Limited Access customers.

In a text to speech system, customers can turn written information into audible speech and improve accessibility for users. Whether listening to documents or enhancing user experiences with synthesized speech, text to speech transforms text into natural-sounding spoken words.

### Key terms

|Term |Definition |
|---|---|
|Real-time speech synthesis |Use the [Speech SDK](/azure/cognitive-services/speech-service/get-started-text-to-speech) or [REST API](/azure/cognitive-services/speech-service/rest-text-to-speech) to convert text to speech by using [prebuilt neural voice](/azure/cognitive-services/speech-service/language-support?tabs=tts), [prebuilt text to speech avatar](/azure/ai-services/speech-service/text-to-speech-avatar/what-is-text-to-speech-avatar), [custom neural voice](/azure/cognitive-services/speech-service/custom-neural-voice), and [custom text to speech avatar](/azure/ai-services/speech-service/text-to-speech-avatar/what-is-custom-text-to-speech-avatar). |
|Voice model |In a text to speech system, a voice model refers to a machine learning-based model or algorithm that generates synthetic speech from written text. This model is trained to convert text input into spoken language output, mimicking the characteristics of a human voice, including pitch, tone, and pronunciation. |
|Prosody | Prosody refers to the modulation of speech elements such as pitch, duration, volume, and pauses to infuse synthetic voices with a natural and expressive quality, conveying emotional nuances and contextual meaning, thereby reducing the robotic quality of the generated speech, and making it more engaging and comprehensible to listeners.  |
|Speech Synthesis Markup Language (“SSML”) | Speech Synthesis Markup Language (SSML) is an XML-based markup language that's used to customize text to speech outputs. With SSML, you can adjust pitch, add pauses, improve pronunciation, change speaking rate, adjust volume, and attribute multiple voices to a single document. You can use SSML to define your own lexicons or switch to different speaking styles. |
|Asynchronous synthesis of long audio | Use the [batch synthesis API (preview)](/azure/cognitive-services/speech-service/batch-synthesis) to asynchronously synthesize text to speech files longer than 10 minutes (for example, audio books or lectures). Unlike synthesis performed via the Speech SDK or Speech to text REST API, responses aren't returned in real-time. The expectation is that requests are sent asynchronously, responses are polled for, and synthesized audio is downloaded when the service makes it available. |
|Visemes | [Visemes](/azure/cognitive-services/speech-service/how-to-speech-synthesis-viseme) are the key poses in observed speech, including the position of the lips, jaw, and tongue in producing a particular phoneme. Visemes have a strong correlation with voices and phonemes. |

#### [Prebuilt neural voice](#tab/prebuilt-voice)

### Introduction 

Prebuilt neural voice provides a wide range of voices, offering over 400 options in more than 140 languages and locales. These text to speech voices enable you to quickly integrate read-aloud functionality into your applications for enhanced accessibility. 

### Key terms

|Term |Definition |
|---|---|
|Prebuilt neural voice  |Microsoft offers a set of prebuilt neural voices, which use deep neural networks to overcome the limits of traditional speech synthesis with regard to stress and intonation in spoken language. Prosody prediction and voice synthesis happen simultaneously, which results in more fluid and natural-sounding outputs. Each prebuilt neural voice model is available at 24kHz and high-fidelity 48kHz, and the output can be upsampled or downsampled to other formats.  |

#### [Custom neural voice](#tab/custom-voice)

### Introduction 

Custom neural voice is a Limited Access [text to speech](/azure/ai-services/speech-service/text-to-speech) feature that allows customers to create a one-of-a-kind customized synthetic voice for their applications by providing their own audio data of their selected voice talents. For more information on custom neural voice, see [Overview of custom neural voice](https://go.microsoft.com/fwlink/?linkid=2153856).

### Key terms 

In addition to the common terms from prebuilt neural voice, the following key terms are relevant to custom neural voice: 

|Term |Definition |
|---|---|
|Custom neural voice |Custom neural voice is a text to speech feature that lets you create a one-of-a-kind, customized, synthetic voice for your applications. With custom neural voice, you can build a natural-sounding voice for your brand or character by providing human speech samples as training data.|
|Recording scripts| A recording script is used for building a custom neural voice. This script includes a variety of sentences or phrases carefully chosen to cover a wide range of phonemes, linguistic features, and contextual scenarios. When trained on a diverse recording script, custom neural voice is capable of accurately and naturally synthesizing speech for a broad range of applications and scenarios. |
|Voice talent |Individuals whose voices are recorded and used to create synthetic voice models. Customers must get sufficient consent under all relevant laws and regulations from the voice talent to use their voice to create a custom neural voice. |
|Personal voice |Personal voice is a new feature in preview that allows customers to create synthetic voices on behalf of their users quickly from a short human voice sample as training data (also known as the prompt).   |

#### [Prebuilt text to speech avatar](#tab/avatar)

### Introduction 

Prebuilt text to speech avatar offers a range of prebuilt avatar choices that can speak using either a [custom neural voice](https://go.microsoft.com/fwlink/?linkid=2153856) or a prebuilt neural Voice. Prebuilt text to speech avatars can be accessed through the Speech Studio UI or from an API and can be synthesized in real time or in batch mode. Currently we provide a small collection of prebuilt avatars.

### Key terms 

In addition to the common terms from [prebuilt neural voice](#key-terms-1), the following key terms are relevant to prebuilt text to speech avatar:

| **Term**       | **Definition*      |
|-------------------|---------------|
| **Real-time synthesis**  | The synthetic avatar video will be generated in almost real time after the system receives the text input.    |
| **Batch mode synthesis** | The synthetic avatar video will be generated asynchronously after the system receives text input. The generated video output can be downloaded in batch mode synthesis. |

#### [Custom text to speech avatar](#tab/cust-avatar)

### Introduction 

Limited Access customers can also create a custom text to speech avatar for their product or brand. To do this, a customer provides their own video recording of avatar talent, which the custom text to speech avatar service uses as training data to create a synthetic video of the custom avatar speaking. Custom avatars may use either a prebuilt neural voice or a custom neural voice. If a customer pairs a custom neural voice with a custom avatar using the same individual’s voice and image/likeness, the resulting custom avatar will be very similar to that individual.

### Key terms

In addition to the common terms from prebuilt neural voice, custom neural voice, and prebuilt text to speech avatar, the following key terms are relevant to custom text to speech avatar:

|Term |Definition |
|---|---|
| Avatar talent | Custom text to speech avatar model building requires training on a video recording of a real human speaking. This person is the avatar talent. Customers must get sufficient consent under all relevant laws and regulations from the avatar talent to use their image/likeness to create a custom avatar. |

#### [Video translation](#tab/video)

### Introduction

Video translation can efficiently localize your video content to cater to diverse audiences around the globe. This service empowers you to create immersive, localized content efficiently and effectively across various use cases such as vlogs, education, news, advertising, and more.

Video translation using prebuilt neural voices is available for all users.

### Key terms

|Term |Definition |
|---|---|
| Batch mode| When customers upload video and specify the source and target language, video translation will return the translated video asynchronously.|
|Content editing| Customer can modify the translated content with prebuilt neural voice or with authorized personal voice.   |

---

## Capabilities

### System behavior

#### Text to speech 

Text to speech converts text into natural-sounding speech. 

Below are the main options for calling the text to speech service. 

##### Real-time text to speech API 

This is a common API call via the [Speech SDK](/azure/ai-services/speech-service/speech-sdk) or [REST API](/azure/ai-services/speech-service/rest-text-to-speech?tabs=streaming) to send a text input and receive an audio output in real time. The Speech system uses a text to speech voice model to convert the text into human-like synthetic speech. The output audio can be saved as a file or be played back to an output device such as a speaker (learn more about [how to synthesize speech from text](/azure/ai-services/speech-service/how-to-speech-synthesis?tabs=browserjs%2Cterminal&pivots=programming-language-csharp#synthesize-to-speaker-output)). Users can also use [SSML](/azure/ai-services/speech-service/speech-synthesis-markup) to fine-tune the text to speech output.  

Text to speech models are trained on large amounts of diverse audio across typical usage scenarios and a wide range of speakers. For example, the text to speech service is often used for voice-enabled chat bots or for audio content creation. 


##### Batch synthesis API 

Batch synthesis is another type of API call. It’s typically used to send large text files and to receive audio outputs asynchronously (that is, at a later time). To use this API, you can specify locations for multiple text files. The text to speech technology reads the text input from the file and generates audio files that are returned to the storage location that you specify. This feature is used to support larger speech synthesis jobs in which it is not necessary to provide end users with the audio output in real time. An example is to create audio books.


### Text to speech – custom neural voice 

Custom neural voice is a [text to speech](/azure/ai-services/speech-service/text-to-speech) feature that allows Limited Access customers to create a one-of-a-kind customized synthetic voice for their applications by providing their own audio data of customer’s selected voice talents. 

With custom neural voice, you can record your voice talent by having them read Microsoft-provided scripts in the Speech Studio and quickly create a synthetic voice that sounds like your voice talent using a lite project (Preview). A lite project is ideal for a quick trial or a proof of concept.

With a pro project, you can upload studio-recorded high-quality voice data of your selected voice talent and create a realistic-sounding voice. Pro supports highly natural voice training that even more closely resembles your voice talent’s voice and can be adapted to speak in multiple emotions and across languages, without the need for additional emotion-specific or language-specific training data.

Once a custom neural voice is created, you can deploy the voice model with a unique endpoint and use the model to generate synthetic speech with the real-time synthesis API or the batch synthesis API described above.

For more information on custom neural voice, see [Overview of custom neural voice](https://go.microsoft.com/fwlink/?linkid=2153856). 

### Personal voice

The personal voice feature allows Limited Access customers to create a voice model from a short human voice sample. The feature can create a voice model based on the prompt in as little as a few seconds. This feature is typically used to power personalized voice experiences for business customers’ applications. Personal voice models can create realistic-sounding voices that can speak in close to 100 languages.

[Watermarks](https://techcommunity.microsoft.com/t5/ai-azure-ai-services-blog/introducing-the-watermark-algorithm-for-synthetic-voice/ba-p/3298548) are added to custom neural voices created with the personal voice feature. Watermarks allow users to identify whether speech is synthesized using Azure Speech, and specifically, which voice was used. Eligible customers can use Azure Speech watermark detection capabilities. To request to add watermark detection to your applications please contact `mstts[at]microsoft.com`.

For more information on personal voice, see [personal voice](https://aka.ms/InstantVoiceDocs). 

### Text to speech avatar 

Text to speech avatar converts text into a digital video of a photorealistic human (either a prebuilt avatar or a custom avatar) speaking with a natural-sounding voice powered by text to speech features like prebuilt neural voice or custom neural voice. The text to speech avatar video can be synthesized asynchronously or in real time. Developers can build applications integrated with text to speech avatar through an API, or use a content creation tool on Speech Studio to create video content without coding.

With text to speech avatar’s advanced neural network models, the feature empowers users to deliver life-like and high-quality synthetic talking avatar videos for various applications.

Text to speech avatar adopts Coalition for Content Provenance and Authenticity (C2PA) Standard to provide audiences with clearer insights into the source and history of video content created by avatars. This standard offers transparent information about AI-generation of video content. For more details on the integration of C2PA with text to speech avatars, refer to [Content Credentials in Azure Text to Speech Avatar](/azure/ai-services/speech-service/text-to-speech-avatar/content-credentials).

In addition, avatar outputs are automatically watermarked. Watermarks allow approved users to identify whether a video is synthesized using the avatar feature of Azure Speech.  To request watermark detection, please contact [avatarvoice[at]microsoft.com](mailto:avatarvoice@microsoft.com).


### Video translation

Video translation can efficiently localize your video content to cater to diverse audiences around the globe. Video translation will automatically extract dialogue audio, transcribe, translate and dub the content with prebuilt or personal voice to the target language, with accurate subtitles for better accessibility. Multi-speaker features will help identify the number of individuals speaking and recommend suitable voices. Content editing with human in the loop allows for precise alignment with customer preference. Enhanced translation quality ensures precise audio and video alignment with GPT integration. Video translation enables authentic and personalized dubbing experiences with personal voice.

## Use cases

Text to speech offers a variety of features catering to a wide range of intended uses across industries and domains. All text to speech features including video translation are subject to the terms and conditions applicable to customers’ Azure subscription, including the Azure Acceptable Use Policy and the [Code of conduct for Azure Speech text to speech](/legal/ai-code-of-conduct?context=%2Fazure%2Fai-services%2Fspeech-service%2Fcontext%2Fcontext).  


In addition, custom text to speech features like custom neural voice, personal voice, and custom text to speech avatar are limited to the approved use cases as outlined in the specific scenarios described below:

### Intended uses for Custom Neural Voice Pro and Custom Neural Voice Lite

The following are the approved use cases for Custom Neural Voice Pro and Custom Neural Voice Lite: 

- **Educational or interactive learning**: To create a fictional brand or character voice for reading or speaking educational materials, online learning, interactive lesson plans, simulation learning, or guided museum tours. 
- **Media: Entertainment**: To create a fictional brand or character voice for reading or speaking entertainment content for video games, movies, TV, recorded music, podcasts, audio books, or augmented or virtual reality. 
- **Media: Marketing**: To create a fictional brand or character voice for reading or speaking marketing and product or service media, product introductions, business promotion, or advertisements. 
- **Self-authored content**: To create a voice for reading content authored by the voice talent. 
- **Accessibility Features**: For use in audio description systems and narration, including any fictional brand or character voice, or to facilitate communication by people with speech impairments. 
- **Interactive Voice Response (IVR) Systems**: To create voices, including any fictional brand or character voice, for call center operations, telephony systems, or responses for phone interactions. 
- **Public Service and Informational Announcements**: To create a fictional brand or character voice for communicating public service information, including announcements for public venues, or for informational broadcasts such as traffic, weather, event information, and schedules. This use case is not intended for journalistic or news content. 
- **Translation and Localization**: For use in translation applications for translating conversations in different languages or translating audio media. 
- **Virtual Assistant or Chatbot**: To create a fictional brand or character voice for smart assistants in or for virtual web assistants, appliances, cars, home appliances, toys, control of IoT devices, navigation systems, reading out personal messages, virtual companions, or customer service scenarios.  

 

### Intended uses for personal voice

The personal voice API (see [Personal voice](/azure/ai-services/speech-service/personal-voice-overview) for more information) is available in Limited Access preview. Only customers who meet Limited Access eligibility criteria can integrate the personal voice API with their applications. These eligible customers are permitted to use personal voices for the following use cases only:  

- **Applications**: For use in applications where voice output is constrained and defined by customers, and where the voice does not read user-generated or open-ended content. Voice model usage must remain within the application and output must not be publishable or shareable from the application. Some examples of applications that fit this description are voice assistants in smart devices and customizing a character voice in gaming.
- **Media, films, and TV**: To dub for films, TV, video, and audio for entertainment scenarios only, where customers maintain sole control over the creation of, access to, and use of the voice models and their output. 
- **Business content**: To create audio and video content for business scenarios to communicate product information, marketing materials, business promotional content, and internal business communications.
- **Special use, bundled with video translation**:  To synthesize voices for each speaker in a video. Customers can also edit and generate lip-synced audio content in target languages. Customers are not required to submit to Microsoft  additional [audio consent](/legal/ai-code-of-conduct?context=%2Fazure%2Fai-services%2Fspeech-service%2Fcontext%2Fcontext) for video content in this scenario, but customers must maintain sole control over the creation, access to, and use of the voice models and their outputs. 

All other uses of custom neural voice, including Custom Neural Voice Pro, Custom Neural Voice Lite, and personal voice, are prohibited. In addition, custom neural voice is a Limited Access service, and registration is required for access to this service. To learn more about Microsoft’s Limited Access policy, refer to [Limited Access features for Foundry Tools](https://aka.ms/limitedaccesscogservices). Certain features are only available to Microsoft managed customers and partners, and only for certain use cases approved by Microsoft at the time of registration. 

Prebuilt neural voice may also be used for the custom neural voice use cases above, as well as additional use cases selected by customers and consistent with the Azure Acceptable Use Policy and the [Code of conduct for Azure Speech text to speech](/legal/ai-code-of-conduct?context=%2Fazure%2Fai-services%2Fspeech-service%2Fcontext%2Fcontext). No registration or pre-approval is required for additional use cases for prebuilt neural voice that meet all applicable terms and conditions. 

### Intended use cases for video translation

Video translation could be used for films, TV, and other visual (including but not limited to video or animation) and audio applications, where customers maintain sole control over the creation of, access to, and use of the voice models and their output. Personal voice and lip syncing are subject to the Limited Access framework, and eligible customers may use these capabilities with Video translation. The following are the approved use cases for Video translation service:
- **Education & learning**: To translate audio in educational visuals, online courses, training modules, simulation-based learning, or guided museum tour visuals for multilingual learners.  
- **Media: Entertainment**: To translate audio in films, movies, TV shows, documentaries, video games, mini-series, short-play and AR/VR content for global audiences, ensuring seamless storytelling across languages.  
- **Media: Marketing**: To translate audio in promotional visuals, product demos, advertisements, and branding campaigns to resonate with international markets and cultures.  
- **Self-Authored Content**: To translate audio in vlogs, short-form visuals, influencer content, travel guides, destination promotional videos, social media visuals, and cultural highlight reels making them accessible and engaging.  
- **Corporate Training and Communication**: To translate audio in internal communication visuals, employee onboarding materials, compliance training, and global corporate announcements for international teams.  
- **E-commerce & Product Demonstrations**: To translate audio in product unboxing visuals, tutorials, customer testimonials, and explainer visuals to cater to international shoppers.  
- **Public Service and Informational Announcements**: To translate audio in public awareness visuals, event schedules, safety announcements, and government informational broadcasts for multilingual accessibility.  
- **Accessibility Features**: To broaden the accessibility of video content through multilingual audio and subtitles. 
- **News and Journalistic Content**: To translate audio in news segments, interviews, press releases, and breaking news reports for diverse linguistic audiences. Customers looking to translate news sources will require additional review.  


### Intended uses for custom text to speech avatar and prebuilt text to speech avatar 

The following are the approved use cases for custom text to speech avatar:
  
- **Virtual Assistant or Chatbot**: To create virtual assistants, virtual companions, virtual sales assistants, or for customer service applications. 
- **Content generation for enterprise contexts**: For use to communicate product information, marketing materials, business promotional content, and internal business communications. Examples include character avatars or digital twins of a business leader to promote a brand. 
- **Educational or interactive learning**: To create a fictional brand or character avatar for presenting educational materials, online learning, interactive lesson plans, simulation learning, or guided museum tours.  
- **Media: Entertainment**: To present updates, share knowledge, create interactive media, or make talking head videos for entertainment scenarios such as videos, gaming, and augmented or virtual reality.  
- **Accessibility Features**: For use to facilitate communication by people with speech impairments. 
- **Self-authored content**: To create an avatar for reading content authored by the avatar talent. 
- **Public Service and Informational Announcements**: To create a fictional brand or character image for communicating public service information, including announcements for public venues, or for informational broadcasts such as traffic, weather, event information, and schedules. This use case is not intended for journalistic or news content. 
- **Translation and Localization**: For use in translation applications for translating conversations in different languages or translating audio media in video format. 

All other uses of custom text to speech avatar are prohibited. In addition, custom text to speech avatar is a Limited Access service, and registration is required for access to this feature. To learn more about Microsoft’s Limited Access policy visit [aka.ms/limitedaccesscogservices](https://aka.ms/limitedaccesscogservices). Certain features are only available to Microsoft managed customers and partners, and only for certain use cases approved by Microsoft at the time of registration. 

Prebuilt text to speech avatar may also be used for the custom avatar use cases above, as well as additional use cases selected by customers and consistent with Azure Acceptable Use Policy and the [Code of conduct for Azure Speech text to speech](/legal/ai-code-of-conduct?context=/azure/ai-services/speech-service/context/context). No registration or pre-approval is required for additional use cases for prebuilt text to speech avatar that meet all applicable terms and conditions.   

### Considerations when choosing use cases 

We encourage customers to use text to speech features in their innovative solutions or applications. All text to speech features must adhere to the Azure Acceptable Use Policy and the [Code of conduct for Azure Speech text to speech](/legal/ai-code-of-conduct?context=/azure/ai-services/speech-service/context/context). In addition, custom neural voice and custom text to speech avatars may only be used for the use cases approved through the [Limited Access registration form](https://aka.ms/customneural). Additionally, here are some considerations when choosing a use case for any text to speech feature: 

- **Ensure use case alignment**: Ensure that the intended use of any text to speech feature aligns with the capabilities and intended purpose of the text to speech feature. 
- **Responsible AI considerations**: Prioritize responsible AI practices by avoiding the creation of misleading or harmful content. Adhere to privacy, data protection, and legal regulations when using text to speech features. 
- **Review the code of conduct**: Microsoft has established a code of conduct that prohibits certain uses of all text to speech features. Ensure compliance with the code of conduct when selecting a use case for text to speech services. 
- **Exercise editorial control**: Carefully consider using synthetic voices with content that lacks proper editorial control, as synthetic voices can sound human-like and amplify the effect of incorrect or misleading content. 
- **Disclosure**: Disclose the synthetic nature of voices, images, and/or videos to users such that users are not likely to be deceived or duped—or able to prank others—into believing they are interacting with a real person. 
- [!INCLUDE [regulatory-considerations](../../includes/regulatory-considerations.md)]

By adhering to these considerations, users can leverage both prebuilt and custom neural voice responsibly.  

## Limitations

The limitations of text to speech should be considered at the intersection of technology and the human, social, and organizational factors that influence its usage and impact. While text to speech offers advanced speech synthesis capabilities, there are certain limitations to be aware of in deploying it responsibly to minimize potential errors.

### Technical limitations, operational factors, and ranges 

Technical limitations to consider when using text to speech include the accuracy of pronunciation and intonation. While text to speech is designed to generate natural-sounding speech, it may encounter difficulties with certain words, names, or uncommon phrases. Users should be aware that there can be instances where the system may mispronounce or emphasize words incorrectly, especially when dealing with niche or domain-specific vocabulary.

It is important to note that certain populations may be more negatively impacted by these technical limitations. For example, individuals with hearing impairments who rely heavily on synthesized speech may face challenges in understanding unclear or distorted speech output. Similarly, users with cognitive or language-related disabilities may find it difficult to comprehend speech with unnatural intonation or mispronounced words.

#### [Prebuilt neural voice](#tab/prebuilt-voice)

- **Linguistic limitations**: While we carefully curate and prepare training data to minimize biases, especially related to gender, ethnicity, or regional accents, and while text to speech supports multiple languages and accents, there may be variations in the quality and availability of voices across different languages. Customers should be aware of potential limitations in pronunciation accuracy, intonation, and linguistic nuances specific to certain languages or dialects. 
- **Context and emotion**: Text to speech may have limitations in accurately conveying contextual information and emotions. Customers should be mindful of the system's inability to understand the emotional nuances or subtle cues present in the input text. Considerations should be made to provide additional context or utilize other methods to convey emotions effectively. 
- **Availability**: Microsoft will provide customers with 12 months’ notice before removing any prebuilt neural voices from our catalog, unless security, legal, or system performance considerations require an expedited removal. This does not apply to previews. 

#### [Custom neural voice](#tab/custom-voice)

- Custom neural voice models are trained using transfer learning technology based on our multi-lingual, multi-speaker base model, with the recording samples of human voices that you provide. The richer the base model, the more powerful the transfer learning, requiring less training data from your voice talent. While our base model is built using a wide range of speech data that includes different speaking accents, age groups, and genders, across about 100 languages (see list of supported languages [here](/azure/ai-services/speech-service/language-support#neural-voices)), it’s possible that certain demographic groups are not well represented in some languages. For example, we cover less speech data from children than from adults. To accommodate this limitation, we require at least 300 lines of recordings (or, around 30 minutes of speech) to be prepared as training data for custom neural voice, and we recommend 2,000 lines of recordings (2-3 hours of speech) to create a voice for production use. Each line of recording (a.k.a. “utterance”) consists of a normal sentence or a short phrase that is read by your chosen voice talent. With 2,000 utterances, our system can learn the target voice characteristics well even if the base model doesn’t include a similar speaker.
- Privacy and data protection: When utilizing custom neural voice, customers should adhere to privacy regulations and ensure that sensitive or personal information is handled securely. It is important to be cautious when processing and storing data, and to follow best practices for data protection and consent management. 

    > [!NOTE]
    > Personal voice requires at least 10 seconds of training data as minimum to create a voice. The feature can then create a voice model based on the training data in as little as 5 seconds. This feature is designed to provide a cost-effective way for Limited Access customers to provide personalized voice experiences to their users. While the resulting voice output will sound like the user, the speaking style may not closely resemble the user’s speaking style including tones and prosodies, especially when the voice model is used to speak another language. It’s also possible the voice output will not sound equally natural across all supported languages.

#### [Prebuilt text to speech avatar](#tab/avatar)

Technical limitations to consider are the accuracy of lip sync alignment with the audio and the naturalness of the avatar’s gestures or body movements. In some cases, text to speech avatars may produce lip sync images that do not perfectly match with the audio content or that lack the desired naturalness. And in other cases, the head, hands, or body may look less smooth during movements. While efforts have been made to improve the quality of synthesized images, there may still be instances where the output does not meet the expectations of human-like lip sync accuracy and body movement expression naturalness, particularly in complex or emotionally nuanced contexts, or when avatar begins to speak. 

- **Training data**: Text to speech avatars rely on training data to generate images, and the quality and naturalness of the synthetic avatar video depends on the size of the training data, the quality of the video recording, and the processing of the data used in the output video. 
- **Context and emotion**: Text to speech avatars may have limitations in accurately conveying contextual information and emotions. Customers should be mindful of the system's inability to understand the emotional nuances or subtle cues present in the input text. Considerations should be made to provide additional context or utilize other methods to convey emotions effectively. 
- **Body movements**: Text to speech avatars are designed to be used in speaking scenarios, such as presenting, so the avatar has limited poses in synthetic video. In general, the avatar is in front facing posture, sitting, or standing.
- **Gestures**: Avatars may use hand gestures during speaking to deliver a natural speaking experience, but the gestures are not pre-programmed, they are learned from video clips in the training data and are included in synthetic video regardless of the input text. Also, avatars cannot make gestures that were not made by the actor in the training data. Avatars are not able to tailor gestures according to contextual information and emotions, so customers should be mindful of the avatar system’s inability to automatically play a gesture appropriate for the context.  
- **Availability**: Microsoft will provide customers with 12 months’ notice before removing any prebuilt text to speech avatars from our catalog, unless security, legal, or system performance considerations require an expedited removal. This does not apply to previews. 
- **Privacy and data protection**: When utilizing text to speech avatars, customers should adhere to all applicable privacy laws and regulations and ensure that sensitive or personal information is handled securely. It is important to be cautious when processing and storing data, and to follow best practices for data protection and consent management. 

Each application is different, and our base model may not match your context or cover all scenarios required for your use case. We encourage developers to thoroughly evaluate the quality of text to speech synthetic voice and video with real-world data that reflects your use case, including testing with users from different demographic groups and with different speech characteristics. Please see the [Quality of the voice model trained](/azure/ai-foundry/responsible-ai/speech-service/text-to-speech/transparency-note#quality-of-the-voice-model-trained) section for best practices for building high quality voice models. 


#### [Custom text to speech avatar](#tab/cust-avatar)

Technical limitations to consider are the accuracy of lip sync alignment with the audio and the naturalness of the avatar’s gestures or body movements. In some cases, text to speech avatars may produce lip sync images that do not perfectly match with the audio content or that lack the desired naturalness. And in other cases, the head, hands, or body may look less smooth during movements. While efforts have been made to improve the quality of synthesized images, there may still be instances where the output does not meet the expectations of human-like lip sync accuracy and body movement expression naturalness, particularly in complex or emotionally nuanced contexts, or when avatars begin to speak. 

- **Training data**: Text to speech avatars rely on training data to generate images, and the quality and naturalness of the synthetic avatar video depends on the size of the training data, the quality of the video recording, and the processing of the data used in the output video. For custom avatars, it is essential to carefully curate and prepare training data from your avatar talent to achieve more natural avatars. 
- **Context and emotion**: Text to speech avatars may have limitations in accurately conveying contextual information and emotions. Customers should be mindful of the system's inability to understand the emotional nuances or subtle cues present in the input text. Considerations should be made to provide additional context or utilize other methods to convey emotions effectively. 
- **Body movements**: Text to speech avatars are designed to be used in speaking scenarios, such as presenting, so the avatar has limited poses in synthetic video. In general, the avatar is in front facing posture, sitting, or standing. Some custom avatars may be capable of a broader range of body movements, like walking or head turning, but if high-quality video of these body movements was not included in the training data, then the avatar synthetic video may be of lower quality than desired.  
- **Gestures**: Avatars may use hand gestures during speaking to deliver a natural speaking experience, but the gestures are not pre-programmed. Instead, they are learned from video clips in the training data and are included in synthetic video regardless of the input text. Also, avatars cannot make gestures that were not made by the avatar talent and captured in the training data. Avatars are not able to tailor gestures according to contextual information and emotions, so customers should be mindful of the avatar system’s inability to automatically play a gesture appropriate for the context.  
- **Privacy and data protection**: When utilizing text to speech avatars, customers should adhere to all applicable privacy laws and regulations and ensure that sensitive or personal information is handled securely. It is important to be cautious when processing and storing data, and to follow best practices for data protection and consent management.

#### [Video translation](#tab/video)

* **Translation quality**: Translation quality will depend on the transcription accuracy and translation accuracy. If the input video is mixed with background music or noise, this will impact the quality of the translation. Translation results will be dependent on context.
* **Dubbing voice similarity and intonation**: When you choose prebuilt neural voices for dubbing, the voice output characteristics may not be similar to the original voice characteristics. If you use the personal voice feature, the voice output will more closely resemble the original voice, but the speaking style may not closely resemble the user’s speaking style including tones and prosodies. It’s also possible the voice output will not sound equally natural across all supported languages. 
* **Privacy and data protection**: When utilizing video translation, you must adhere to all applicable privacy laws and regulations and ensure that sensitive or personal information is handled securely. It is important to be cautious when processing and storing data, and to follow best practices for data protection and consent management.

---

Each application is different, and our base model may not match your context or cover all scenarios required for your use case. We encourage developers to thoroughly evaluate the quality of text to speech synthetic voice and video with real-world data that reflects your use case, including testing with users from different demographic groups and with different speech characteristics. Please see the [Quality of the voice model trained](/azure/ai-foundry/responsible-ai/speech-service/text-to-speech/transparency-note#quality-of-the-voice-model-trained) section for best practices for building high quality voice models. 

In addition to ensuring performance, it is important to consider how to minimize risks of stereotyping and erasure that may result from synthetic voices and avatar. For example, if you are creating a custom neural voice for a smart voice assistant, carefully consider what voice is appropriate to create, and seek diverse perspectives from individuals from a variety of backgrounds. When building and evaluating your system, always seek diverse input. 



## Fairness considerations

At Microsoft, we strive to empower every person on the planet to do more. An essential part of this goal is working to create technologies and products that are fair and inclusive. Fairness is a multi-dimensional, socio-technical topic and impacts many different aspects of our product development. You can learn more about Microsoft’s approach to fairness [here](https://www.microsoft.com/ai/responsible-ai?activetab=pivot1%3aprimaryr6).

One important dimension to consider when using AI systems, including text to speech, is how well the system performs for different groups of people. Research has shown that without conscious effort focused on improving performance for all groups, AI systems can exhibit varying levels of performance across different demographic factors such as race, ethnicity, gender, and age.

As part of our evaluation of Azure AI text to speech, we have conducted an analysis to assess potential fairness harms. We have examined the system's performance across different demographic groups, aiming to identify any disparities or differences that may exist and could potentially impact fairness.

In some cases, there may be remaining performance disparities. It is important to note that these disparities may exceed the target, and we are actively working to address and minimize any potential biases or performance gaps, carefully consider the demographic group choice of the actor, and seek diverse perspectives from a variety of backgrounds.

Regarding representational harms, such as stereotyping, demeaning, or erasing outputs, we acknowledge the risks associated with these issues. While our evaluation process aims to mitigate such risks, we encourage users to consider their specific use cases carefully and implement additional mitigations as appropriate. Having a human in the loop can provide an extra layer of oversight to address any potential biases or unintended consequences. The use of blocklists or allowlists can also help ensure that the synthesized speech aligns with desired standards and avoids any harmful or inappropriate content.

We are committed to continuously improving our fairness evaluations to gain a deeper understanding of the system's performance across various demographic groups and potential fairness concerns. The evaluation process is ongoing, and we are actively working to enhance fairness and inclusivity, and mitigate any identified disparities. We understand the importance of addressing fairness considerations and strive to ensure that text to speech delivers reliable and equitable synthesized speech outputs.

Please note that this information represents what we know so far about fairness evaluations, and we remain dedicated to refining our evaluation methodologies and addressing any fairness concerns that may arise.

## System performance

Performance for the text to speech system refers to how accurately and naturally it can convert written text into synthesized speech. This is measured using various metrics to evaluate the quality and effectiveness of the generated audio output. Some common performance metrics used include:

- **Mean opinion score (MOS)**: A rating system where judges provide a score that represents the overall quality of synthesized speech and avatar video. A higher MOS indicates better quality. 
- **MOS gap**: The difference between the MOS score of human recordings and the generated audio tracks/videos. A smaller MOS Gap indicates a closer resemblance to human speech/human likeness. 
- **Similarity MOS (SMOS)**: Measures the similarity of the generated audio tracks/videos to the human recordings. A higher SMOS signifies better similarity. 
- **Intelligibility**: The percentage of correctly intelligible words in synthesized speech. 

Even with state-of-the-art models, AI systems like text to speech can produce errors. For example, the system may produce synthesized speech with subtle unnatural intonations or pronunciation errors, leading to a less-than-ideal user experience, or the system may misinterpret text or struggle with unusual linguistic constructs, resulting in unnatural or unintelligible speech.


### Best practices for improving system performance  

To improve system performance and adapt system behavior in text to speech, there are several best practices that can be followed. These practices involve adjusting various components and parameters to optimize the tradeoffs and meet specific use case requirements. However, it is important to consider the potential impact on different populations to ensure fairness and inclusivity.

#### [Prebuilt neural voice](#tab/prebuilt-voice)

Using SSML (Speech Synthesis Markup Language) is considered a best practice to enhance text to speech output quality. SSML allows users to exert greater control over synthesized speech, enabling the customization of pronunciation, intonation, emphasis, and other prosodic features. By incorporating SSML tags into the text, users can add pauses, adjust speech rate, specify phonetic pronunciations, and control pitch and volume, among other parameters. This level of fine-tuning helps create more natural and expressive speech, making the text to speech output sound more human-like and engaging. All the SSML markups can be passed directly to the API. We also provide an online tool, Audio Content Creation, that allows customers to fine-tune using an intuitive user interface.

If your use case involves specialized vocabulary or domain-specific content, consider using the custom lexicon feature to improve the system's ability to accurately pronounce and convey domain-specific terms or phrases.


#### [Custom neural voice](#tab/custom-voice)

Creating a custom voice requires careful quality control in each step, from voice design, to data preparation, to the deployment of the voice model to your system.

#### Persona design 

Before building a custom neural voice, particularly if it is for a fictional brand or character voice, it is a good practice to design a persona of the voice that would best represent your brand, fit well with user scenarios, and resonate with your intended audience. This can be specified in a persona brief – a document that describes the features of the voice and the fictitious or real person behind the voice. This persona brief will help guide the process of creating a custom voice model including the recording scripts, voice talent selection, and training and tuning of the voice.

#### Script selection 

Your recording script defines the training dataset for your voice model and is the starting point of any custom voice recording session. Your recording script must be carefully selected to represent the user scenarios for your voice. For example, if you are going to use the voice model for your customer service bot, you may want to use the phrases from your bot conversations to create the recording script. To create a voice for reading stories, you can use a relevant story script for your recordings.

Follow the [guidance here](/azure/ai-services/speech-service/record-custom-voice-samples#create-a-script) to prepare your script. 

> [!NOTE]
> When preparing your recording script, make sure you include a statement sentence to acquire voice talent’s acknowledgment that you are using their voice data to create a text to speech voice model and generate synthetic speech. You can find the required statement in multiple languages [here](https://github.com/Azure-Samples/Cognitive-Speech-TTS/blob/master/CustomVoice/script/verbal-statement-all-locales.txt). The language of the verbal statement must be the same as the training data language. 
>
> As a technical safeguard intended to prevent misuse of custom neural voice, Microsoft will use this verbal statement to verify that the voice talent’s voice in the verbal statement matches the voice provided in the training data through [Speaker Verification](/azure/ai-services/speech-service/speaker-recognition-overview#speaker-verification). Read more about this process in the [Data and Privacy section here](https://aka.ms/CNV-data-privacy). 

#### Preparing training data 

We recommend that the audio recordings should be captured in a professional quality recording studio so that high signal-to-noise ratio is achieved without distortion, and other defects are minimized. Follow the [recording guidance here](/azure/ai-services/speech-service/record-custom-voice-samples).

The quality of the custom voice heavily depends on the recorded voice used for training. Consistent volume, speaking rate, speaking pitch, and consistency in expressive mannerisms of speech are essential to create a high-quality custom neural voice. Custom neural voice creates a synthetic voice model that mimics the voice in the training data. The quality of the recording of the voice talent is the upper bound of the quality of the custom neural voice model. The voice model will capture the styles, accents, and other characteristics of the voice, including defects such as noises and mispronunciations.

Unexpected errors such as mismatching of the transcript to the recordings can introduce mistakes in the pronunciation labeling to the training system. The [Speech Studio](/azure/ai-services/speech-service/how-to-custom-voice) provides capabilities for users to evaluate the pronunciation accuracy, identify noises, check the audio length for each utterance in the training dataset, and filter out unqualified recordings. For example, in the dataset detail view, you can check the pronunciation score, the signal-to-noise ratio and the audio length for your training data.

It is not possible to provide 100% accurate results. As the developer creating the synthetic voice, you are responsible for reviewing and ensuring the audio quality of the training data is sufficient for voice model building and your intended use.

#### [Prebuilt text to speech avatar](#tab/avatar)

To improve system performance for prebuilt text to speech avatars, we recommend that customers experiment with avatar selection and voice selection. Prebuilt text to speech avatar offers multiple prebuilt avatars with different characteristics, and prebuilt neural voice also offers a rich set of voices and characteristics. The diversity of prebuilt avatars is an important aspect for the feature and we aim to add a more diverse representation of prebuilt avatars. Explore and select an avatar image and voice combination that aligns well with your desired scenarios and target audience. You can also apply to customize your prebuilt avatar by using custom neural voice to create a voice model based on your own voice talent’s training data. For more information on custom neural voice, see [Overview of custom neural voice.](https://go.microsoft.com/fwlink/?linkid=2153856)

#### [Custom text to speech avatar](#tab/cust-avatar)

When building a custom text to speech avatar, preparing high quality training data can help improve the quality of the custom avatar model. We recommend video recording avatar talent in a professional video shooting environment and using a green screen, a bright and even light source, and high signal-to-noise ratio for audio.

The quality of the resulting avatar heavily depends on the recorded video used for training. Speaking rate, body posture, facial expression, hand gestures, consistency in actor position, and appropriate lighting are essential to create an engaging and natural custom avatar. The audio recording in the video is used only for custom avatar model training, to enable the avatar model to learn the phoneme of the voice and lip sync match. The audio is not used to create a custom neural voice model, so the avatar talent doesn’t have to read a script; they can talk freely. The audio should be clear, without background noise and other people’s voices. If a customer wishes to use a custom neural voice based on the voice of the same talent for a custom avatar, the customer must build a custom neural voice separately.

The appearance and performance of the avatar talent are also key factors impacting the system performance; please see our guidance [How to record video samples for custom text to speech avatar](/azure/ai-services/speech-service/text-to-speech-avatar/custom-avatar-record-video-samples).

#### [Video translation](#tab/video)
---

## Evaluation of text to speech  

### Evaluation methods 

Some commonly used metrics for evaluating text to speech overall system performance include: 

- Mean opinion score (MOS) gap with human recording: usually used to compare the quality of the text to speech voice model against a human recording. The quality of a voice model created by custom neural voice compared to that of a human recording is expected to be close, with a gap of no more than 0.5 in the MOS score. 
- For custom neural voice, you also can use Similarity MOS (SMOS) to measure how similar the custom voice sounds compared to the original human recordings. With SMOS studies, judges are asked to listen to a set of paired audio tracks, one generated using the custom voice, the other from the original human recordings in the training data, and rate if the two audio tracks in each pair are spoken by the same person, using a five-point scale (1 being the lowest, 5 the highest). The average score is reported as the SMOS score. We recommend that a good custom neural voice should achieve an SMOS higher than 4.0.
- Besides measuring naturalness with MOS and SMOS, you can also assess the intelligibility of the voice model by checking the pronunciation accuracy of the generated speech. This is done by having judges listen to a set of testing samples, determining whether they can understand the meaning and indicate any words that were unintelligible to them. Intelligibility rate is calculated using the percentage of the correctly intelligible words among the total number of words tested (i.e., the number of intelligible words/the total number of words tested \* 100%). Normally a usable text to speech engine needs to reach a score of \> 98% for intelligibility.

### Evaluation results 

Text to speech consistently delivers high-quality and natural-sounding synthesized speech, meeting the requirements of diverse industries and domains. Our evaluations include extensive testing of the system's training and test data, ensuring that it represents the intended uses and operational factors encountered in real-world scenarios, as well as testing samples of synthesized speech outputs.

The evaluation results have influenced decisions about the constraints in the system's design, such as the maximum case size and the minimum amount of training data required. By analyzing the performance of the system across different data sets, settings, and parameters, appropriate constraints have been set to optimize the system's behavior, reliability, and safety.

While the evaluation covers a wide range of use cases, it is important to note that the results are generalizable to some extent across use cases that were not directly part of the evaluation. The robustness and performance of the system provides confidence in its ability to handle various scenarios, including those that may not have been explicitly tested.

Here are some recommended tests and score ranges based on our experience: 

| Measurement   | Definition   | How it is calculated      | Recommended text size       | Recommended score      | 
|--------|------------|-----------|-----|---------| 
| MOS       | Mean opinion score of the quality of the audio tracks     | Average of the rating scores of each judge on each audio | > 30 generated audio tracks      | > 4.0 (normally requires the MOS of the human recording is higher than 4.5) | 
| MOS gap     | The MOS score difference between human recordings and the generated audio tracks | The MOS score on the human recordings minus the MOS score on the generated audio tracks| > 10 human recordings, > 30 generated audio tracks, > 20 judges on each audio | < 0.5                 | 
| SMOS   | The similarity of the generated audio tracks to the human recordings | Average of the rating scores of the similarity level on each pair of audio tracks | > 40 pairs, > 20 judges on each pair | > 4.0, > 3.5 (secondary language) | 
| Intelligibility | The pronunciation accuracy of the generated speech at the word level | Percentage of the correctly intelligible words among the total number of words tested | > 60 generated audio tracks, > 10 judges on each audio | > 98%                 | 

## Evaluating and integrating text to speech for your use 

Below are some best practices to help you responsibly integrate text to speech features into your use cases. 

### Disclose when the voice is synthetic 

Disclosing that a voice is computer generated not only minimizes the risk of harmful outcomes from deception but also increases trust in the organization delivering the voice. Learn more about [how to disclose](/azure/ai-foundry/responsible-ai/speech-service/text-to-speech/concepts-disclosure-guidelines). 

Microsoft requires its customers to disclose the synthetic nature of text to speech voices to its users. 

- Make sure to provide adequate disclosure to audiences, especially when using the voice of a well-known person. People make judgments about information based in part on the person who delivers it, whether they do so consciously or unconsciously. For example, a disclosure could be verbally shared at the start of a broadcast. For more information, visit [disclosure patterns](/azure/ai-foundry/responsible-ai/speech-service/text-to-speech/concepts-disclosure-patterns). 
- Consider proper disclosure to parents or other parties with use cases that are designed for or may be used in situations involving minors and children. If your use case is intended for minors or children, you'll need to ensure that your disclosure is clear and transparent so that parents or legal guardians can understand the role of synthetic media and make an informed decision on behalf of minors or children about whether to use the experience. 

### Disclose when the avatar video is synthetic  

Disclosing that an avatar speaking video is computer generated not only minimizes the risk of harmful outcomes from deception but also increases trust in the organization delivering the video. Learn more about [how to disclose](/azure/ai-foundry/responsible-ai/speech-service/text-to-speech/concepts-disclosure-guidelines).  

Microsoft requires its customers to disclose the synthetic nature of text to speech avatars to its users.  

- Make sure to provide adequate disclosure to audiences, especially when using the image (and voice) of a well-known person. People make judgments about information based in part on the person who delivers it, whether they do so consciously or unconsciously. **For example, a disclosure could be made with a watermark, such as, “The voice and image in this video are AI-generated,” in text or verbally shared at the start of a video.** For more information visit [disclosure patterns](/azure/ai-foundry/responsible-ai/speech-service/text-to-speech/concepts-disclosure-patterns).  
- Consider proper disclosure to parents or other parties with use cases that are designed for or may be used in situations involving minors and children. If your use case is intended for minors or children, you'll need to ensure that your disclosure is clear and transparent so that parents or legal guardians can understand the role of synthetic media and make an informed decision on behalf of minors or children about whether to use the experience.  

### Select appropriate voice types for your scenario 

Carefully consider the context of use and the potential harms associated with using text to speech voices or avatars. For example, high-fidelity synthetic voices may not be appropriate in high-risk scenarios, such as for personal messaging, financial transactions, or complex situations that require human adaptability or empathy. 

Users may also have different expectations for voice types and avatar expressions or gestures, depending on the context. For example, when listening to sensitive news read by a synthetic voice, some users prefer a more empathetic and human-like tone, while others prefer a neutral voice. Consider testing your application to better understand user preferences. 

### Be transparent about capabilities and limitations 

Users are more likely to have higher expectations when interacting with high-fidelity synthetic voice agents. When system capabilities don't meet those expectations, trust can suffer, and may result in unpleasant, or even harmful experiences. 

### Provide optional human support 

In ambiguous, transactional scenarios (for example, a call support center), users don't always trust a computer agent to appropriately respond to their requests. Human support may be necessary in these situations, regardless of the realistic quality of the voice or capability of the system. 

### Considerations for voice talent 

When customers work with voice talent to create custom neural voice, the guidelines below apply. 

- Voice talent should have control over their voice model (how and where it will be used) and be compensated for its use. Microsoft requires custom neural voice customers to obtain explicit written permission from voice talent to create a synthetic voice and to ensure that the customer’s agreement with each individual contemplates the duration, use, and any content limitations. **If you are creating a synthetic voice of a well-known person, you should provide a way for the voice talent to edit or approve the content of the output you plan to generate with the voice model**. 
- Some voice talent may be unaware of potential malicious uses of technology and should be educated by system owners about the capabilities of the technology. Microsoft requires customers to share Microsoft’s [Disclosure for voice and avatar talent](/azure/ai-foundry/responsible-ai/speech-service/text-to-speech/disclosure-voice-talent?tabs=cnv) with voice talent directly or through the voice talent’s authorized representative to describe how synthetic voices are developed and operate in conjunction with text to speech services. 

### Considerations for avatar talent  

When customers work with avatar talent to create custom avatars, the guidelines below apply.  

- Avatar talent should have control over their avatar model (how and where it will be used) and be compensated for its use. Microsoft requires custom avatar customers to obtain explicit written permission from their avatar talent to create a synthetic text to speech avatar and ensure that the customer’s agreement with each individual contemplates the duration, use, and any content limitations. **If you are creating a custom avatar of a well-known person, you should provide a way for the avatar talent to edit or approve the content of the output you plan to generate with the voice model**.  
- Some avatar talent may be unaware of potential malicious uses of technology and should be educated by system owners about the capabilities of the technology. Microsoft requires customers to share Microsoft’s [Disclosure for voice and avatar talent](/azure/ai-foundry/responsible-ai/speech-service/text-to-speech/disclosure-voice-talent?tabs=avatar) with avatar talent directly or through the avatar talent’s authorized representative to describe how synthetic avatar video is developed and operates in conjunction with text to speech services.  

### Considerations for people with speech disorders 

When working with individuals with speech disorders to create or deploy synthetic voice technology, the following guidelines apply. 

### Provide guidelines for contracts with talent in accessibility scenarios 

Customers should develop guidelines for establishing contracts with individuals who use synthetic voices for assistance in speaking. Customers should consider specifying in their contracts with individuals the duration of use, ownership transfer and/or license criteria, procedures for deleting the voice model, and how to prevent unauthorized access.  

### Account for inconsistencies in speech patterns 

For individuals with speech disorders who record their own voice fonts, inconsistencies in their speech pattern (slurring or inability to pronounce certain words) may complicate the recording process. In these cases, synthetic voice technology and recording sessions should be designed with appropriate accommodations determined by the customer (for example, provide breaks or additional recording sessions). 

### Allow modification over time 

Individuals with speech disorders may wish to update their synthetic voice to reflect changes due to aging or other factors. Individuals may also have stylistic preferences that change over time, and may want to make changes to pitch, accent, or other voice characteristics. 

## Learn more about responsible AI

- [Microsoft AI principles](https://www.microsoft.com/ai/responsible-ai)
- [Microsoft responsible AI resources](https://www.microsoft.com/ai/responsible-ai-resources) 
- [Microsoft Azure Learning courses on responsible AI](/training/paths/responsible-ai-business-principles/)

## Learn more about Azure Speech

- [Limited access to Azure Speech Service - Foundry Tools | Microsoft Learn](/azure/ai-foundry/responsible-ai/speech-service/text-to-speech/limited-access) 
- [Code of conduct for Azure Speech Service | Microsoft Learn](/legal/ai-code-of-conduct?context=/azure/ai-services/speech-service/context/context) 
- [Data, privacy, and security for Azure Speech Service - Foundry Tools | Microsoft Learn](/azure/ai-foundry/responsible-ai/speech-service/text-to-speech/data-privacy-security) 