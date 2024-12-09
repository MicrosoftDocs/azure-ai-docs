---
title: Video translation overview - Speech service
titleSuffix: Azure AI services
description: With video translation, you can seamlessly integrate multi-language voice-over capabilities into your videos.
manager: nitinme
ms.service: azure-ai-speech
ms.topic: overview
ms.date: 9/24/2024
ms.reviewer: sally-baolian
ms.author: eur
author: eric-urban
ms.custom: references_regions
#Customer intent: As a developer, I want to learn about video translation in Azure AI Speech.
---

# What is video translation (preview) 

[!INCLUDE [Feature preview](../includes/preview-feature.md)]

Video translation is a feature in Azure AI Speech that enables you to seamlessly translate and generate videos in multiple languages automatically. This feature is designed to help you localize your video content to cater to diverse audiences around the globe. You can efficiently create immersive, localized videos across various use cases such as vlogs, education, news, enterprise training, advertising, film, TV shows, and more.

The process of replacing the original language of a video with audio recorded in a different language is often relied upon to cater to diverse audiences. Traditionally achieved through human recording and manual post-production, translation is essential for ensuring that viewers can enjoy video content in their native language. However, this process comes with key pain points, including its high cost, lengthy duration, and inability to replicate the original speaker's voice accurately. Video translation in Azure AI Speech addresses these challenges by providing an automated, efficient, and cost-effective solution for creating localized videos.

## Use case 

Video translation provided by Azure AI Speech has a wide range of use cases across various industries and content types. Here are some key applications: 

- **News + interviews**: News organizations can translate and dub news segments and interviews to provide accurate and timely information to audiences worldwide. 

- **Advertisement + marketing**: Businesses can localize their advertising and marketing videos to resonate with target audiences in different markets, enhancing brand awareness and customer engagement.

- **Education + learning**: Educational institutions and e-learning platforms can dub their instructional videos and lectures into different languages, making learning more accessible and inclusive. 

- **Film + TV show**: Film studios and production companies can dub their movies and TV shows for international distribution, reaching a broader audience and maximizing revenue potential. 

- **Vlog + short video**: Content owners can easily translate and dub their vlogs and short videos to reach international audiences, expanding their viewership and engagement. 

- **Enterprise training**: Corporations can localize their training videos for employees in different regions, ensuring consistent and effective communication across their workforce. 

## Supported regions and languages

Currently, video translation in Azure AI Speech is only supported in the East US region.

We support video translation between various languages, enabling you to tailor your content to specific linguistic preferences. For the languages supported for video translation, refer to the [supported source and target languages](language-support.md?tabs=speech-translation#video-translation). 

## Core features

- **Dialogue audio extraction and spoken content transcription.**
  
  Automatically extracts dialogue audio from the source video and transcribe the spoken content.
- **Translation from language A to B and large language model (LLM) reformulation.**
  
  Translates the transcribed content from the original language (Language A) to the target language (Language B) using advanced language processing techniques. Enhances translation quality and refines gender-aware translated text through LLM reformulation. 
- **Automatic translation – voice generation in other language.**
  
  Utilizes AI-powered text-to-speech technology to automatically generate human-like voices in the target language. These voices are precisely synchronized with the video, ensuring a flawless translation experience. This includes utilizing prebuilt neural voices for high-quality output and offering options for personal voice. 
- **Human in the loop for content editing.**
  
  Allows for human intervention to review and edit the translated content, ensuring accuracy and cultural appropriateness before finalizing the dubbed video. 
- **Subtitles generation.**
 
  Delivers the fully dubbed video with translated dialogue, synchronized subtitles, and generated voices, ready for download and distribution across various platforms. You can also set the subtitle length on each screen for optimal display. 

## Get started 

To get started with video translation, refer to [How to use video translation](video-translation-get-started.md).

## Price 

For pricing details on video translation, see [Speech service pricing](https://azure.microsoft.com/pricing/details/cognitive-services/speech-services/). Note that video translation pricing will only be visible for [service regions](#supported-regions-and-languages) where the feature is available.

## Related content

* Try the [video translation](video-translation-get-started.md)
  