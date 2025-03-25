---
title: Azure AI Translator release history
titleSuffix: Azure AI services
description: Release notes and updates for Azure AI Translator Service API.
author: laujan
manager: nitinme
ms.service: azure-ai-translator
ms.topic: reference
ms.date: 03/10/2025
ms.author: lajanuar
---

# Azure AI Translator release history

Azure AI Translator is an innovative language service that enables users to translate text and documents, helps entities expand their global outreach, and supports preservation of at-risk and endangered languages. By utilizing the strengths of artificial intelligence and machine learning, this cutting-edge tool continually improved to offer more precise, swift, and adaptable translation services. Here, you can explore key milestones and enhancements in the evolution of Azure AI Translator. For more information on recent advances, *see* [What's new?](whats-new.md).

## September 2023

* Translator service has [text, document translation, and container language support](language-support.md) for the following 18 languages:

|Language|Code|Cloud – Text Translation and Document Translation|Containers – Text Translation|Description
|:----|:----|:----|:----|
|chiShona|`sn`|✔|✔|The official language of Zimbabwe with more than 8 million native speakers.|
|Hausa|`ha`|✔|✔|The most widely used language in West Africa with more than 150 million speakers worldwide.|
|Igbo|`ig`|✔|✔|The principal native language of the Igbo people of Nigeria with more than 44 million speakers.|
|Kinyarwanda|`rw`|✔|✔|The national language of Rwanda with more than 12 million speakers primarily in East and Central Africa.|
|Lingala|`ln`|✔|✔|One of four official languages of the Democratic Republic of the Congo with more than 60 million speakers.|
|Luganda|`lug`|✔|✔|A major language of Uganda with more than 5 million speakers.|
|Nyanja|`nya`|✔|✔| Nynaja, also known as Chewa, is spoken mainly in Malawi and has more than 2 million native speakers.|
|Rundi|`run`|✔|✔| Rundi, also known as Kirundi, is the national language of Burundi and has more than 6 million native speakers.|
|Sesotho|`st`|✔|✔| Sesotho, also know as Sotho, is the national and official language of Lesotho, one of 12 official languages of South Africa, and one of 16 official languages of Zimbabwe. It has more than 5.6 native speakers.
|Sesotho sa Leboa|`nso`|✔|✔|Sesotho, also known as Northern Sotho, is the native language of more than 4.6 million people in South Africa.|
|Setswana|`tn`|✔|✔|Setswana, also known as Tswana, is an official language of Botswana and South Africa and has more than 5 million speakers.|
|Xhosa|`xh`|✔|✔|An official language of South Africa and Zimbabwe, Xhosa has more than 20 million speakers.|
|Yoruba|`yo`|✔|✔|The principal native language of the Yoruba people of West Africa, it has more than 50 million speakers.|
|Konkani|`gom`|✔|✔|The official language of the Indian state of Goa with more than 7 million speakers worldwide.|
|Maithili|`mai`|✔|✔|One of the 22 officially recognized languages of India and the second most spoken language in Nepal. It has more than 20 million speakers.|
|Sindhi|`sd`|✔|✔|Sindhi is an official language of the Sindh province of Pakistan and the Rajasthan state in India. It has more than 33 million speakers worldwide.|
|Sinhala|`si`|✔|✔|One of the official and national languages of Sri Lanka, Sinhala has more than 16 million native speakers.|
|Lower Sorbian|`dsb`|✔|Currently, not supported in containers |A West Slavic language spoken primarily in eastern Germany. It has approximately 7,000 speakers.|

## July 2023

* Document Translation REST API v1.1 is now Generally Available (GA).

## June 2023

**Documentation updates**

* The [Document Translation SDK overview](document-translation/document-sdk-overview.md) is now available to provide guidance and resources for the .NET/C# and Python `SDK`s.
* The [Document Translation SDK quickstart](document-translation/quickstarts/client-library-sdks.md) is now available for the C# and Python programming languages.

## May 2023

**Announcing new releases for Build 2023**

### Text Translation SDK (preview)

The Text translation `SDK`s are now available in public preview for C#/.NET, Java, JavaScript/TypeScript, and Python programming languages.

* To learn more, see [Text translation SDK overview](text-translation/sdk-overview.md).
* To get started, try a [Text Translation SDK quickstart](document-translation/document-sdk-overview.md) using a programming language of your choice.

### Microsoft Translator V3 Connector (preview)

The Translator V3 Connector is now available in public preview. The connector creates a connection between your Translator Service instance and Microsoft Power Automate enabling you to use one or more prebuilt operations as steps in your apps and workflows. To learn more, see the following documentation:

* [Automate document translation](connector/document-translation-flow.md)
* [Automate text translation](solutions/connector/text-translator-flow.md)

## February 2023

[**Document Translation in Language Studio**](document-translation/language-studio.md) is now available for Public Preview. The feature provides a no-code user interface to interactively translate documents from local or Azure Blob Storage.

## November 2022

### Custom Translator stable GA v2.0 release

Custom Translator version v2.0 is generally available and ready for use in your production applications!

### Changes to Translator `Usage` metrics

> [!IMPORTANT]
> **`Characters Translated`** and **`Characters Trained`** metrics are deprecated and are removed from the Azure portal.

|Deprecated metric| Current metrics | Description|
|---|---|---|
|Characters Translated (Deprecated)</br></br></br></br>|**&bullet; Text Characters Translated**</br></br>**&bullet;Text Custom Characters Translated**| &bullet; Number of characters in incoming **text** translation request.</br></br> &bullet; Number of characters in incoming **custom** translation request.  |
|Characters Trained (Deprecated) | **&bullet; Text Trained Characters** | &bullet; Number of characters **trained** using text translation service.|

* In 2021, two new metrics, **Text Characters Translated** and **Text Custom Characters Translated**, were added to help with granular metrics data service usage. These metrics replaced **Characters Translated** which provided combined usage data for the general and custom text translation service.

* Similarly, the **Text Trained Characters** metric was added to replace the  **Characters Trained** metric.

* **Characters Trained** and **Characters Translated** metrics support continues in the Azure portal with the deprecated flag to allow migration to the current metrics. As of October 2022, Characters Trained and Characters Translated are no longer available in the Azure portal.

## June 2022

### Document Translation stable GA 1.0.0 release

Document Translation .NET and Python client-library `SDK`s are now generally available and ready for use in production applications!

### [**C#**](#tab/csharp)

**Version 1.0.0 (GA)** </br>
**2022-06-07**

##### [README](https://github.com/Azure/azure-sdk-for-net/blob/Azure.AI.Translation.Document_1.0.0/sdk/translation/Azure.AI.Translation.Document/README.md)

##### [**Changelog/Release History**](https://github.com/Azure/azure-sdk-for-net/blob/Azure.AI.Translation.Document_1.0.0/sdk/translation/Azure.AI.Translation.Document/CHANGELOG.md)

##### [**Package (NuGet)**](https://www.nuget.org/packages/Azure.AI.Translation.Document)

##### [**SDK reference documentation**](/dotnet/api/overview/azure/AI.Translation.Document-readme)

### [Python](#tab/python)

**Version 1.0.0 (GA)** </br>
**2022-06-07**

##### [README](https://github.com/Azure/azure-sdk-for-python/blob/azure-ai-translation-document_1.0.0/sdk/translation/azure-ai-translation-document/README.md)

##### [**Changelog/Release History**](https://github.com/Azure/azure-sdk-for-python/blob/azure-ai-translation-document_1.0.0/sdk/translation/azure-ai-translation-document/CHANGELOG.md)

##### [**Package (PyPI)**](https://pypi.org/project/azure-ai-translation-document/1.0.0/)

##### [**SDK reference documentation**](/python/api/overview/azure/ai-translation-document-readme?view=azure-python&preserve-view=true)

---

## May 2022

### [Document Translation support for scanned PDF documents](https://aka.ms/blog_ScannedPdfTranslation)

* Document Translation uses optical character recognition (OCR) technology to extract and translate text in scanned PDF document while retaining the original layout.

## April 2022

### [Text and document translation support for Faroese](https://www.microsoft.com/translator/blog/2022/04/25/introducing-faroese-translation-for-faroese-flag-day/)

* Translator service has [text and document translation language support](language-support.md) for Faroese, a Germanic language originating on the Faroe Islands. The Faroe Islands are a self-governing region within the Kingdom of Denmark located between Norway and Iceland. Faroese is descended from Old West Norse spoken by Vikings in the Middle Ages.

### [Text and document translation support for Basque and Galician](https://www.microsoft.com/translator/blog/2022/04/12/break-the-language-barrier-with-translator-now-with-two-new-languages/)

* Translator service has [text and document translation language support](language-support.md) for Basque and Galician. Basque is a language isolate, meaning it isn't related to any other modern language and is spoken in parts of northern Spain and southern France. Galician is spoken in northern Portugal and western Spain. Both Basque and Galician are official languages of Spain.

## March 2022

### [Text and document translation support for Somali and Zulu languages](https://www.microsoft.com/translator/blog/2022/03/29/translator-welcomes-two-new-languages-somali-and-zulu/)

* Translator service has [text and document translation language support](language-support.md) for Somali and Zulu. The Somali language, spoken throughout Africa, has more than 21 million speakers and is in the Cushitic branch of the Afroasiatic language family. The Zulu language has 12 million speakers and is recognized as one of South Africa's 11 official languages.

## February 2022

### [Text and document translation support for Upper Sorbian](https://www.microsoft.com/translator/blog/2022/02/21/translator-celebrates-international-mother-language-day-by-adding-upper-sorbian/),

* Translator service has [text and document translation language support](language-support.md) for Upper Sorbian. The Translator team works tirelessly to preserve indigenous and endangered languages around the world. Language data provided by the Upper Sorbian language community was instrumental in introducing this language to Translator.

### [Text and document translation support for Inuinnaqtun and Romanized Inuktitut](https://www.microsoft.com/translator/blog/2022/02/01/introducing-inuinnaqtun-and-romanized-inuktitut/)

* Translator service has [text and document translation language support](language-support.md) for Inuinnaqtun and Romanized Inuktitut. Both are indigenous languages that are essential and treasured foundations of Canadian culture and society.

## January 2022

### Custom Translator portal (v2.0) public preview

The [Custom Translator portal (v2.0)](https://portal.customtranslator.azure.ai/) is now in public preview and includes significant changes that makes it easier to create your custom translation systems.

To learn more, see our Custom Translator [documentation](custom-translator/overview.md) and try our [quickstart](custom-translator/quickstart.md) for step-by-step instructions.

## October 2021

### [Text and document support for more than 100 languages](https://www.microsoft.com/translator/blog/2021/10/11/translator-now-translates-more-than-100-languages/)

* Translator service adds [text and document language support](language-support.md) for the following languages:
  * **Bashkir**. A Turkic language spoken by approximately 1.4 million native speakers. It has three regional language groups: Southern, Eastern, and Northwestern.
  * **Dhivehi**. Also known as Maldivian, it's an Indo-Iranian language primarily spoken in the island nation of Maldives.
  * **Georgian**. A Kartvelian language that is the official language of Georgia. It has approximately 4 million speakers.
  * **Kyrgyz**. A Turkic language that is the official language of Kyrgyzstan.
  * **Macedonian (cyrillic)**. An Eastern South Slavic language that is the official language of North Macedonia. It has approximately 2 million people.
  * **Mongolian (traditional)**. Traditional Mongolian script is the first writing system created specifically for the Mongolian language. Mongolian is the official language of Mongolia.
  * **Tatar**. A Turkic language used by speakers in modern Tatarstan closely related to Crimean Tatar and Siberian Tatar but each belongs to different subgroups.
  * **Tibetan**. It has nearly 6 million speakers and can be found in many Tibetan Buddhist publications.
  * **Turkmen**. The official language of Turkmenistan. It's similar to Turkish and Azerbaijani.
  * **Uyghur**. A Turkic language with nearly 15 million speakers spoken primarily in Western China.
  * **Uzbek (latin)**. A Turkic language that is the official language of Uzbekistan. It has 34 million native speakers.

These additions bring the total number of languages supported in Translator to 103.

## August 2021

### [Text and document translation support for literary Chinese](https://www.microsoft.com/translator/blog/2021/08/25/microsoft-translator-releases-literary-chinese-translation/)

* Azure AI Translator has [text and document language support](language-support.md) for  literary Chinese. Classical or literary Chinese is a traditional style of written Chinese used by traditional Chinese poets and in ancient Chinese poetry.

## June 2021

### [Document Translation client libraries for C#/.NET and Python](document-translation/document-sdk-overview.md)—now available in prerelease

## May 2021

### [Document Translation ― now generally available](https://www.microsoft.com/translator/blog/2021/05/25/translate-full-documents-with-document-translation-%e2%80%95-now-in-general-availability/)

* **Feature release**: Translator's [Asynchronous batch translation](document-translation/overview.md)  feature is generally available. Document Translation is designed to translate large files and batch documents with rich content while preserving original structure and format. You can also use custom glossaries and custom models built with [Custom Translator](custom-translator/overview.md) to ensure your documents are translated quickly and accurately.

### [Translator service available in containers](https://www.microsoft.com/translator/blog/2021/05/25/translator-service-now-available-in-containers/)

* **New release**: Translator service is available in containers as a gated preview. [Submit an online request](https://aka.ms/csgate-translator) for approval to get started. Containers enable you to run several Translator service features in your own environment and are great for specific security and data governance requirements. For more information, *See* [Install and run Translator containers (preview)](containers/translator-how-to-install-container.md)

## February 2021

### [Document Translation public preview](https://www.microsoft.com/translator/blog/2021/02/17/introducing-document-translation/)

* **New release**:  [Asynchronous batch translation](document-translation/overview.md) is available as a preview feature of the Translator Service. Preview features are still in development and aren't meant for production use. They're made available on a "preview" basis so customers can get early access and provide feedback. Document Translation enables you to translate large documents and process batch files while still preserving the original structure and format. _See_ [Microsoft Translator blog: Introducing Document Translation](https://www.microsoft.com/translator/blog/2021/02/17/introducing-document-translation/)

### [Text and document translation support for nine added languages](https://www.microsoft.com/translator/blog/2021/02/22/microsoft-translator-releases-nine-new-languages-for-international-mother-language-day-2021/)

* Translator service has [text and document translation language support](language-support.md) for the following languages:

  * **Albanian**. An isolate language unrelated to any other and spoken by nearly 8 million people.
  * **Amharic**. An official language of Ethiopia spoken by approximately 32 million people. It's also the liturgical language of the Ethiopian Orthodox church.
  * **Armenian**. The official language of Armenia with 5-7 million speakers.
  * **Azerbaijani**. A Turkic language spoken by approximately 23 million people.
  * **Khmer**. The official language of Cambodia with approximately 16 million speakers.
  * **Lao**. The official language of Laos with 30 million native speakers.
  * **Myanmar**. The official language of Myanmar, spoken as a first language by approximately 33 million people.
  * **Nepali**. The official language of Nepal with approximately 16 million native speakers.
  * **Tigrinya**. A language spoken in Eritrea and northern Ethiopia with nearly 11 million speakers.

## January 2021

### [Text and document translation support for Inuktitut](https://www.microsoft.com/translator/blog/2021/01/27/inuktitut-is-now-available-in-microsoft-translator/)

* Translator service has [text and document translation language support](language-support.md) for **Inuktitut**, one of the principal Inuit languages of Canada. Inuktitut is one of eight official Aboriginal languages in the Northwest Territories.

## November 2020

### [Custom Translator V2 is generally available](https://www.microsoft.com/translator/blog/2021/01/27/inuktitut-is-now-available-in-microsoft-translator/)

* **New release**: Custom Translator V2 upgrade is fully available to the generally available (GA). The V2 platform enables you to build custom models with all document types (training, testing, tuning, phrase dictionary, and sentence dictionary). _See_  [Microsoft Translator blog: Custom Translator pushes the translation quality bar closer to human parity](https://www.microsoft.com/translator/blog/2020/11/12/microsoft-custom-translator-pushes-the-translation-quality-bar-closer-to-human-parity).

## October 2020

### [Text and document translation support for Canadian French](https://www.microsoft.com/translator/blog/2020/10/20/cest-tiguidou-ca-translator-adds-canadian-french/)

* Translator service has [text and document translation language support](language-support.md) for **Canadian French**. Canadian French and European French are similar to one another and are mutually understandable. However, there can be significant differences in vocabulary, grammar, writing, and pronunciation. Over 7 million Canadians (20 percent of the population) speak French as their first language.

## September 2020

### [Text and document translation support for Assamese and Axomiya](https://www.microsoft.com/translator/blog/2020/09/29/assamese-text-translation-is-here/)

* Translator service has [text and document translation language support](language-support.md) for **Assamese** also knows as **Axomiya**. Assamese / Axomiya is primarily spoken in Eastern India by approximately 14 million people.

## August 2020

### [Introducing virtual networks and private links for translator](https://www.microsoft.com/translator/blog/2020/08/19/virtual-networks-and-private-links-for-translator-are-now-generally-available/)

* **New release**: Virtual network capabilities and Azure private links for Translator are generally available (GA). Azure private links allow you to access Translator and your Azure hosted services over a private endpoint in your virtual network. You can use private endpoints for Translator to allow clients on a virtual network to securely access data over a private link. _See_ [Microsoft Translator blog: Virtual Networks and Private Links for Translator are generally available](https://www.microsoft.com/translator/blog/2020/08/19/virtual-networks-and-private-links-for-translator-are-now-generally-available/)

### [Custom Translator upgrade to v2](https://www.microsoft.com/translator/blog/2020/08/05/custom-translator-v2-is-now-available/)

* **New release**: Custom Translator V2 phase 1 is available. The newest version of Custom Translator rolls out in two phases to provide quicker translation and quality improvements, and allow you to keep your training data in the region of your choice. *See* [Microsoft Translator blog: Custom Translator: Introducing higher quality translations and regional data residency](https://www.microsoft.com/translator/blog/2020/08/05/custom-translator-v2-is-now-available/)

### [Text and document translation support for two Kurdish regional languages](https://www.microsoft.com/translator/blog/2020/08/20/translator-adds-two-kurdish-dialects-for-text-translation/)

* **Northern (Kurmanji) Kurdish** (15 million native speakers) and **Central (Sorani) Kurdish** (7 million native speakers). Most Kurdish texts are written in Kurmanji and Sorani.

### [Text and document translation support for two Afghan languages](https://www.microsoft.com/translator/blog/2020/08/17/translator-adds-dari-and-pashto-text-translation/)

* **Dari** (20 million native speakers) and **Pashto** (40 - 60 million speakers). The two official languages of Afghanistan.

### [Text and document translation support for Odia](https://www.microsoft.com/translator/blog/2020/08/13/odia-language-text-translation-is-now-available-in-microsoft-translator/)

* **Odia** is a classical language spoken by 35 million people in India and across the world. It joins **Bangla**, **Gujarati**, **Hindi**, **Kannada**, **Malayalam**, **Marathi**, **Punjabi**, **Tamil**, **Telugu**, **Urdu**, and **English** as the 12th most used language of India supported by Microsoft Translator.
