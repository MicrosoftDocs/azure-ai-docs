---
title: Get default answer - custom question answering
description: The default answer is returned when there is no match to the question. You might want to change the default answer from the standard default answer in custom question answering.
ms.service: azure-ai-language
ms.topic: how-to
ms.date: 12/15/2025
author: laujan
ms.author: lajanuar
ms.custom: language-service-question-answering
---
# Change default answer for custom question answering

The default answer for a project is meant to be returned when an answer is not found. If you're using a client application, such as the [Azure AI Bot Service](/azure/bot-service/bot-builder-howto-qna), it may also have a separate default answer, indicating no answer met the score threshold.

## Default answer


|Default answer|Description of answer|
|--|--|
|KB answer when no answer is determined|`No good match found in KB.` - When the custom question answering API finds no matching answer to the question it displays a default text response. In custom question answering, you can set this text in the **Settings** of your project. |

### Client application integration

For a client application, such as a bot with the [Azure AI Bot Service](/azure/bot-service/bot-builder-howto-qna), you can choose from the following scenarios:

* Use your project's setting
* Use different text in the client application to distinguish when an answer is returned but doesn't meet the score threshold. This text can either be static text stored in code, or can be stored in the client application's settings list.

## Next steps

* [Create a project](manage-knowledge-base.md)
