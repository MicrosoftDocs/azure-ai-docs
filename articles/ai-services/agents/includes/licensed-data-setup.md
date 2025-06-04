---
manager: nitinme
author: aahill
ms.author: aahi
ms.service: azure-ai-agent-service
ms.topic: include
ms.date: 04/28/2025
---

## Setup

1. Go to [Azure AI Foundry portal](https://ai.azure.com/?cid=learnDocs) and select your AI Project. Select **Management Center**.
   
   :::image type="content" source="../media/tools/licensed-data/project-assets.png" alt-text="A screenshot showing the selectors for the management center for an AI project." lightbox="../media/tools/licensed-data/project-assets.png":::

1. Select **+new connection** in the settings page.

   :::image type="content" source="../media/tools/licensed-data/connected-resources.png" alt-text="A screenshot showing the connections for the selected AI project." lightbox="../media/tools/licensed-data/connected-resources.png":::
   
1. Select **custom keys** in **other resource types**.

   :::image type="content" source="../media/tools/licensed-data/custom-keys.png" alt-text="A screenshot showing the custom key option in the settings page." lightbox="../media/tools/licensed-data/custom-keys.png":::

1. Enter the following information to create a connection to store your Tripadvisor or Morningstar key:
   1. Set **Custom keys** to "key", with the value being your API key.
   1. Make sure **is secret** is checked.
   1. Set the connection name to your connection name. You use this connection name in your sample code or Foundry Portal later.
   1. For the **Access** setting, you can choose either *this project only* or *shared to all projects*. Just make sure in your code, the connection string of the project you entered has access to this connection.

   :::image type="content" source="../media/tools/licensed-data/connect-custom-resource.png" alt-text="A screenshot showing the screen for adding connection information." lightbox="../media/tools/licensed-data/connect-custom-resource.png":::

## Use the tool through the Azure AI Foundry portal

1. To use the tool in the Azure AI Foundry, in the **Agents** screen for your agent, scroll down the **Setup** pane to **action**. Then select **Add**.

    :::image type="content" source="../media/tools/knowledge-tools.png" alt-text="A screenshot showing the available tool categories in the Azure AI Foundry portal." lightbox="../media/tools/knowledge-tools.png":::

1. Select the appropriate tool and follow the prompts to add the tool. 

   :::image type="content" source="../media/tools/knowledge-tools-list.png" alt-text="A screenshot showing available knowledge tools." lightbox="../media/tools/knowledge-tools-list.png":::

1. Give a name for your tool and provide an optional description.
 
    :::image type="content" source="../media/tools/licensed-data/add-data-source.png" alt-text="A screenshot showing the data source." lightbox="../media/tools/licensed-data/add-data-source.png":::

1. Select the custom key connection you just created. 

    :::image type="content" source="../media/tools/licensed-data/add-connection.png" alt-text="A screenshot showing the connection for your tool, and a JSON example." lightbox="../media/tools/licensed-data/add-connection.png":::

1. Finish and start chatting.