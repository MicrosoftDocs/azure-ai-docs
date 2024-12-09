---
title: Use URL tool to get answer from knowledge base - QnA Maker
titleSuffix: Azure AI services
description: This article walks you through getting an answer from your knowledge base using a URL test tool such as cURL or the Visual Studio Code REST Client extension..
#services: cognitive-services
manager: nitinme
ms.author: jboback
author: jboback
ms.service: azure-ai-language
ms.subservice: azure-ai-qna-maker
zone_pivot_groups: URL-test-interface
ms.topic: how-to
ms.date: 01/19/2024
---

# Get an answer from a QNA Maker knowledge base

[!INCLUDE [Custom question answering](../includes/new-version.md)]

> [!NOTE]
> This documentation does not apply to the latest release. To learn about using the latest question answering APIs consult the [question answering authoring guide](../../language-service/question-answering/how-to/authoring.md).

::: zone pivot="url-test-tool-curl"

[!INCLUDE [Get answer using cURL](../includes/quickstart-test-tool-curl.md)]

::: zone-end

::: zone pivot="url-test-tool-visual-studio-code-rest-client-extension"

[!INCLUDE [Get answer using the Visual Studio Code REST Client extension](../includes/quickstart-test-tool-vscode.md)]

::: zone-end


## Next steps

> [!div class="nextstepaction"]
> [Test knowledge base with batch file](../how-to/test-knowledge-base.md#batch-test-with-tool)

Learn more about metadata:
* [Authoring - add metadata to QnA pair](../how-to/edit-knowledge-base.md#add-metadata)
* [Query prediction - filter answers by metadata](../how-to/query-knowledge-base-with-metadata.md)
