---
title: API reference - Content Moderator
titleSuffix: Azure AI services
description: Learn about the content moderation APIs for Content Moderator.
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-content-moderator
ms.topic: reference
ms.date: 06/12/2025
ms.author: pafarley

---

# Content Moderator API reference

You can get started with Azure Content Moderator APIs by doing the following:

- In the Azure portal, [subscribe to the Content Moderator API](https://portal.azure.com/#create/Microsoft.CognitiveServicesContentModerator).

You can use the following **Content Moderator APIs** to set up your post-moderation workflows.

| Description | Reference |
| -------------------- |-------------|
| **Image Moderation API**<br /><br />Scan images and detect potential adult and racy content by using tags, confidence scores, and other extracted information. | [Image Moderation API reference](/rest/api/cognitiveservices/contentmoderator/image-moderation)   |
| **Text Moderation API**<br /><br />Scan text content. Profanity terms and personal data are returned. | [Text Moderation API reference](/rest/api/cognitiveservices/contentmoderator/text-moderation)   |
| **Video Moderation API**<br /><br />Scan videos and detect potential adult and racy content.  | [Video Moderation API overview](video-moderation-api.md "Video Moderation API overview")   |
| **List Management API**<br /><br />Create and manage custom exclusion or inclusion lists of images and text. If enabled, the **Image - Match** and **Text - Screen** operations do fuzzy matching of the submitted content against your custom lists. <br /><br />For efficiency, you can skip the machine learning-based moderation step.<br /><br /> | [List Management API reference](/rest/api/cognitiveservices/contentmoderator/list-management-image-lists)   |
