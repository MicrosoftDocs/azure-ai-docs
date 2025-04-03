---
author: eric-urban
ms.author: eur
ms.service: azure-ai-speech
ms.topic: include
ms.date: 2/19/2025
---

Content for [Custom neural voice](https://aka.ms/customvoice) like data, models, tests, and endpoints are organized into projects in Speech Studio. Each project is specific to a country/region and language, and the gender of the voice you want to create. For example, you might create a project for a female voice for your call center's chat bots that use English in the United States.

> [!TIP]
> Try [Custom neural voice (CNV) Lite](../../../../custom-neural-voice-lite.md) to demo and evaluate CNV before investing in professional recordings to create a higher-quality voice. 

All it takes to get started are a handful of audio files and the associated transcriptions. See if custom neural voice supports your [language](../../../../language-support.md?tabs=tts) and [region](../../../../regions.md#regions).

## Create a custom neural voice Pro project

To create a custom neural voice Pro project, follow these steps:

1. Sign in to the [Speech Studio](https://aka.ms/speechstudio/customvoice).
1. Select the subscription and Speech resource to work with. 

    > [!IMPORTANT]
    > Custom neural voice training is currently only available in some regions. After your voice model is trained in a supported region, you can copy it to an AI Services resource for Speech in another region as needed. See footnotes in the [regions](../../../../regions.md#regions) table for more information.

1. Select **Custom voice** > **Create a project**. 
1. Select **Custom neural voice Pro** > **Next**. 
1. Follow the instructions provided by the wizard to create your project. 

Select the new project by name or select **Go to project**. You see these menu items in the left panel: **Set up voice talent**, **Prepare training data**, **Train model**, and **Deploy model**. 

## Next steps

> [!div class="nextstepaction"]
> [Add voice talent consent to the professional voice project.](../../../../professional-voice-create-consent.md)

