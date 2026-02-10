---
title: Disclosure for voice and avatar talent
description: Disclosure for voice and avatar talent which covers background as well as best patterns and practices for deployment of this technology.
author: PatrickFarley
ms.author: pafarley
manager: nitinme
ms.service: azure-ai-speech
ms.topic: concept-article
ms.date: 02/19/2022
---

# Disclosure for voice and avatar talent

[!INCLUDE [non-english-translation](../../includes/non-english-translation.md)]

The goal of this article is to help voice and avatar talent understand the technology behind the text to speech capabilities that their voices and images help create. It also contains important privacy disclosures for talent about how Microsoft may process, use, and retain audio and video files containing talent’s recorded voices and images and helps Microsoft prevent, and/or respond to complaints of, misuse of Foundry Tools.

Microsoft is committed to designing AI responsibly. We hope this note will foster a greater shared understanding among tech builders, voice talent, avatar talent, and the general public about the intended and beneficial uses of this technology.

## Key text to speech terms

**Voice model:** A text to speech computer model that can mimic unique vocal characteristics of a target speaker. A voice model is also called voice font or synthetic voice. A voice model is a set of parameters in binary format that is not human readable and does not contain audio recordings. It cannot be reverse engineered to derive or construct the audio recordings of a human being speaking.

**Voice talent:** Individuals or target speakers whose voices are recorded and used to create voice models that are intended to sound like the voice talent's voice.

**Avatar model:** A text to speech avatar computer model that can mimic unique facial characteristics of a target actor. An avatar model is a set of parameters in binary format that is not human readable and does not contain video or audio recordings. It cannot be reverse engineered to derive or construct video recordings of a human being acting. 

**Avatar talent:** Custom text to speech avatar model building requires training on a video recording of a real human speaking. This person is the avatar talent. Customers must get sufficient consent under all relevant laws and regulations from the avatar talent to use their image to create a custom avatar.

## How neural text to speech works 

**How it works:** Neural text to speech synthesizes speech using deep neural networks that have "learned" the way phonetics are combined in natural human speech rather than using classical programming or statistical methods. In addition to the recordings of a particular voice talent, neural text to speech uses a source library that contains voice recordings from many different speakers.

**What to know about it:** Because of the way it synthesizes voices, neural text to speech can produce styles of speech that were not part of the original recordings, such as changes in tone of voice and affectation. Neural text to speech voices sound fluid and are good at replicating the natural pauses, idiosyncrasies, and hesitancy that people express when they are speaking. Those who hear synthetic voices made via neural text to speech tend to rate them closer to human speech than standard text to speech voices.

**Examples of how Microsoft uses it**: 
- **Prebuilt neural voice** is a feature of text to speech that offers "off-the-shelf" voice models for customer use. Prebuilt neural voices are also used in several Microsoft products including the Edge Browser, Narrator, Office, and Teams.
- **Custom neural voice** is a feature of text to speech that enables the creation of one-of-a-kind custom synthetic voice models. The following are capabilities of custom neural voice:
  - **Language transfer** can express in a language different from the original voice recordings.
  - **Style transfer** can express in a style of speaking different from the original voice recordings. For example, a newscaster voice.
  - **Voice transformation** can express in a manner different from the original voice recordings. For example, modifying tone or pitch to create different character voices.
  - **Other voices used in Microsoft's products and services**, such as Cortana.

**What to expect when recording:** Contributing at least 300 lines for a proof-of-concept voice model and about 2,000 lines to produce a new voice model for production use.

## How text to speech avatar works 

**How it works:** Text to speech avatar is built on top of prebuilt neural voice and custom neural voice, and synthesizes avatar video content with synchronized text to speech prebuilt neural voice or custom neural voice. The synthesis process uses deep neural networks trained on models that are developed based on video recordings of avatar talent. The models are trained with the acoustic features extracted from the audio elements of the recording, and physical characteristics, mouth movements, facial expressions, and related visual elements extracted from the video elements of the recording. 
 
**What to know about it:** The synthesized text to speech avatar’s face, body, and movements closely resemble the avatar talent, but the text to speech avatar’s voice may be generated from any of the prebuilt neural voices Microsoft makes available or from a custom neural voice, including where the voice talent is the same individual as the avatar talent, if the individual has authorized such use.

**Examples of how Microsoft uses it**:  
- **Prebuilt text to speech avatar** is a feature of Azure Speech in Foundry Tools text to speech that offers "off-the-shelf" text to speech avatar models for customer use.
- **Custom text to speech avatar** is a feature of Azure Speech text to speech that enables the creation of one-of-a-kind custom synthetic text to speech avatar models.


**What to expect when recording**: You will need to contribute at least 10 minutes of video recording for a proof-of-concept custom avatar model and about 20 minutes of video recording to produce a complete custom avatar model for production use. 


## Voice talent and synthetic voices: an evolving relationship 

Recognizing the integral relationship between voice talent and synthetic voices, Microsoft interviewed voice talent to better understand their perspectives on new developments in technology. Research we conducted in 2019 showed that voice talent saw potential benefit from the capabilities introduced by neural text to speech, such as saving studio time to complete recording jobs, and adding capacity to complete more voice acting assignments. At the same time, there were varying degrees of awareness about how developments in text to speech technology could potentially impact their profession.

Overall, voice talent expressed a desire for transparency and clarity about:
- Limits on what their voice likeness could and could not be used to express.
- The duration of allowable use of their voice likeness.
- Potential impact on future recording opportunities.
- The persona that would be associated with their voice likeness.

## Synthetic voice in wider use 

Traditionally, text to speech voices were limited in adoption due to their robotic sound. Most were used to support accessibility, for example as a screen reader for people who are blind or have low vision. Text to speech voices have also been used by people with speech impairment. For instance, the late Stephen Hawking used a text to speech-generated voice.

Now, with increasingly realistic-sounding synthetic voices and the uptick in more familiar, everyday interactions between machines and humans, the uses of this technology have proliferated and expanded. Text to speech systems power voice assistants across an array of devices and applications. They read out news, search results, public service announcements, educational content, and much more.

## Synthetic avatar in wider use  

Similar to text to speech voices, avatars now offer realistic appearances, movements, and facial expressions paired with lifelike sounding voices. These speaking avatars may be used in a variety of situations, such as to present content in an online training, present a speech on behalf of a company, interact with customers in customer service settings, and much more. 

## Microsoft's approach to responsible use of text to speech  

Every day, people find new ways to apply text to speech technology, and not all are for the good of individuals or society. If misused, believably human-sounding text to speech voices or realistic speaking avatars could cause harm. For example, a misinformation campaign could become much more potent if it used the voice and image of a well-known public figure.

We recognize that there's no perfect way to prevent media from being modified or to unequivocally prove where it came from. Therefore, our approach to responsible use has focused on being transparent about Azure Speech text to speech features by limiting permitted uses of custom versions of these features and demonstrating our values through action.

## Requirements and tips for meaningful consent from voice and avatar talent 

If you are using Microsoft products or services to process Biometric Data, you are responsible for: (i) providing notice to data subjects, including with respect to retention periods and destruction; (ii) obtaining consent from data subjects; and (iii), deleting the Biometric Data, all as appropriate and required under applicable Data Protection Requirements. "Biometric Data" will have the meaning set forth in Article 4 of the GDPR and, if applicable, equivalent terms in other data protection requirements.

#### [Custom neural voice](#tab/cnv)

To use custom neural voice, we contractually require customers to do the following: 
- Obtain explicit written permission from voice talent to use that person’s voice for the purpose of creating a custom neural voice.
- Provide this document to voice talent so they can understand how text to speech works, and how it may be used once they complete the audio recording process.
- Get necessary permissions from voice talent for Microsoft’s processing, use, and retention of voice talent's audio files to perform speaker verification against training data and for Microsoft’s use and retention of voice models as described below.

We also recommend that customers do the following: 
- Share the intended contexts of use with voice talent so they are aware of who will hear their voice, in what scenarios, and whether/how people will be able to interact with it.
- Ensure voice talent are aware that a voice model made from their recordings can say things they didn't specifically record in the studio.
- Discuss whether there's anything they'd be uncomfortable with the voice model being used to say.

#### [Custom text to speech avatar](#tab/avatar)

To use custom text to speech avatar, we contractually require customers to do the following: 
- Obtain explicit written permission from avatar talent to use that person's image and voice for the purpose of creating a custom text to speech avatar. 
- Provide this document to avatar talent so they can understand how custom avatar works, and how their video recording may be used once they complete the video recording process. 
- Get necessary permissions from avatar talent for Microsoft's processing, use, and retention of the avatar talent’s video files to perform verification against training data and for Microsoft’s use and retention of custom avatar models as described below. 

We also recommend that you do the following:  
- Share the intended contexts of use with avatar talent so they are aware of who will see their image, in what scenarios, and whether/how people will be able to interact with it. 
- Ensure avatar talent are aware that an avatar model made from their video recordings can be generated with content that they didn’t specifically record in the studio. 
- Discuss whether there's anything they'd be uncomfortable with the avatar model being used to say or do. 

---

## Microsoft's processing, use, and retention of data

#### [Custom neural voice](#tab/cnv)

### Microsoft's use of voice talent audio files for speaker verification 

Customers must obtain permission from voice talent to use their voice to create custom voice models for a synthetic voice. This technical safeguard is intended to help prevent misuse of our service by, for example, preventing someone from training voice models with audio recordings and using the models to spoof a voice without the speaker's knowledge or consent.

In [Speech Studio](https://speech.microsoft.com/customvoice), you must upload an audio file with a recorded acknowledgement statement from the voice talent. Microsoft reserves the right to use Microsoft's speaker recognition technology on this recorded acknowledgement statement and verify it against the training audio data to confirm that the voices came from the same speaker, or as otherwise necessary to investigate misuse of Azure Speech.

The speaker's voice signatures created from the recorded acknowledgement statement files and training audio data are used by Microsoft solely for the purposes stated above. Microsoft will retain the recorded statement file for as long as necessary to preserve the security and integrity of Microsoft's Foundry Tools. Learn more about how we process, use, and retain data in the [Data, privacy, and security doc](/azure/ai-foundry/responsible-ai/speech-service/text-to-speech/data-privacy-security). 

#### [Custom text to speech avatar](#tab/avatar)

### Microsoft's use of avatar talent’s video files for face comparison and speaker verification.

Customers must obtain permission from avatar talent for use of their image/likeness to create a custom text to speech avatar for a synthetic video. This technical safeguard is intended to help prevent misuse of our service by, for example, preventing someone from training avatar models with video recordings and using the models to spoof an avatar without the person’s knowledge or consent.

You must provide a video file with a recorded acknowledgement statement from the avatar talent. Microsoft reserves the right to verify the recorded acknowledgement statement against the training video data to confirm that the images and voices came from the same person, or as otherwise necessary to investigate misuse of Foundry Tools.

The avatar talent’s video signatures created from the recorded acknowledgement statement files and training video data are used by Microsoft solely for the purposes stated above. Microsoft will retain the recorded statement file for as long as necessary to preserve the security and integrity of Microsoft's Foundry Tools. Learn more about how we process, use, and retain data in the [Data, privacy, and security doc](/azure/ai-foundry/responsible-ai/speech-service/text-to-speech/data-privacy-security). 

---

## Microsoft's use of custom models

#### [Custom neural voice](#tab/cnv)

While customers maintain the exclusive usage rights to their custom neural voice model, Microsoft may independently retain a copy of custom neural voice models for as long as necessary. Microsoft may use your custom neural voice model for the sole purpose of protecting the security and integrity of Foundry Tools.

Microsoft will secure and store a copy of voice talent’s recorded acknowledgement statement and custom neural voice models with the same high-level security that it uses for its other Azure Services. Learn more at Microsoft Trust Center.

We will continue to identify and be explicit about the intentional, beneficial, and intended uses of text to speech that are based upon existing social norms and expectations people have around media when they believe it to be real or fake. In line with Microsoft's trust principles, Microsoft does not actively monitor or moderate the audio content generated by your use of custom neural voice. Customers are solely responsible for ensuring that usage complies with all applicable laws and regulations and in accordance with the terms of the customer’s agreement with voice talent.

### Microsoft's use of voice talent data with custom neural voice lite 

Custom neural voice lite is a project type in public preview that allows you to record 20-50 voice samples on Speech Studio and create a lightweight custom voice model for demonstration and evaluation purposes. Both the recording script and the testing script are pre-defined by Microsoft. A synthetic voice model you create using custom neural voice lite may be deployed and used more broadly only if you apply for and receive full access to custom neural voice (subject to applicable terms).

The synthetic voice and related audio recording you submit via the Speech Studio will automatically be deleted within 90 days unless you gain full access to custom neural voice and choose to deploy the synthetic voice, in which case you will control the duration of its retention. If the voice talent would like to have the synthetic voice and the related audio recordings deleted before 90 days, they can delete them on the portal directly, or contact their enterprise to do so.

In addition, before you can deploy any synthetic voice model created using a custom neural voice lite project, the voice talent must provide an additional recording in which they acknowledge that the synthetic voice will be used for additional purposes beyond demonstration and evaluation.

#### [Custom text to speech avatar](#tab/avatar)

While you maintain the exclusive usage rights to your custom text to speech avatar model, Microsoft may independently retain a copy of your custom avatar models for as long as necessary. Microsoft may use your custom avatar models for the sole purpose of protecting the security and integrity of Foundry Tools. 

Microsoft will secure and store a copy of custom avatar models with the same high level of security that it uses for its other Azure Services. Learn more at Microsoft Trust Center. 

We will continue to identify and be explicit about the intentional, beneficial, and intended uses of avatar that are based upon existing social norms and expectations people have around media when they believe it to be real or fake. In line with Microsoft's trust principles, Microsoft does not actively monitor or moderate the video and audio content generated by your use of custom text to speech avatar. Customers are solely responsible for ensuring that usage complies with all applicable laws and regulations and in accordance with the terms of the customer’s agreement with talent. 

---

## Guidelines for responsible deployment

Because text to speech is an adaptable technology, there are grey areas in determining how it should or shouldn't be used. To navigate these, we've formulated the following guidelines for using synthetic voice and avatar models:
- Protect owners of voices and images/likenesses from misuse or identity theft. 
- Prevent the proliferation of fake and misleading content. 
- Encourage use in scenarios where consumers expect to be interacting with synthetic content. 
- Encourage use in scenarios where consumers observe the generation of the synthetic content. 

### Examples of inappropriate use

Azure AI text to speech must not be used: 
- To deceive people and/or intentionally misinform;
- For the purpose of false advertising, including via live commercials;  To claim to be from any person, company, government body, or entity without explicit permission to make that representation;
- To impersonate any person without explicit permission, including to gain information or privileges;
- To create, incite, or disguise hate speech, discrimination, defamation, terrorism, or acts of violence;
- To exploit or manipulate children;
- To make unsolicited phone calls, bulk communications, posts, or messages;
- To disguise policy positions or political ideologies;
- To disseminate unattributed content or misrepresent sources.

### Examples of appropriate use

Appropriate use cases could include, but are not limited to: 
- Virtual agents based on fictional personas. For example, on-demand web searching, IoT control, or customer support provided by a company's branded character.
- Entertainment media for use in fictional content. For example, movies, video games, tv, recorded music, or audio books.
- Accredited educational institutions or educational media. For example, interactive lesson plans or guided museum tours.
- Assistive technology and real-time translation. For example, ALS-afflicted individuals preserving their voices.
- Public service announcements using fictional personas. For example, airport or train terminal announcements.
- Advertising/live streaming: advertising content, live streaming associated with marketing or sale of a product.  

## See also

- [Transparency note and use cases for custom neural voice](/azure/ai-foundry/responsible-ai/speech-service/text-to-speech/transparency-note)
- [Responsible deployment of synthetic speech](/azure/ai-foundry/responsible-ai/speech-service/text-to-speech/transparency-note)
- [Disclosure design guidelines](/azure/ai-foundry/responsible-ai/speech-service/text-to-speech/concepts-disclosure-guidelines)
- [Disclosure design patterns](/azure/ai-foundry/responsible-ai/speech-service/text-to-speech/concepts-disclosure-patterns)
- [Data, privacy, and security for custom neural voice](/azure/ai-foundry/responsible-ai/speech-service/text-to-speech/data-privacy-security)