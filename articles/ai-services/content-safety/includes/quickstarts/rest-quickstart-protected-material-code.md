---
title: "Quickstart: Use protected material detection for code with the REST API"
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-content-safety
ms.custom:
ms.topic: include
ms.date: 04/10/2025
ms.author: pafarley
ai-usage: ai-assisted
---


## Prerequisites

* An Azure subscription - [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn) 
* Once you have your Azure subscription, <a href="https://aka.ms/acs-create"  title="Create a Content Safety resource"  target="_blank">create a Content Safety resource </a> in the Azure portal to get your key and endpoint. Enter a unique name for your resource, select your subscription, and select a resource group, supported region (see [Region availability](/azure/ai-services/content-safety/overview#region-availability)), and supported pricing tier. Then select **Create**.
    * The resource takes a few minutes to deploy. After it finishes, select **Go to resource**. In the left pane, under **Resource Management**, select **Subscription Key and Endpoint**. The endpoint and either of the keys are used to call APIs.
* [cURL](https://curl.haxx.se/) installed

## Analyze code for protected material detection

The following section walks through a sample request with cURL. Paste the command below into a text editor, and make the following changes.

1. Replace `<endpoint>` with the endpoint URL associated with your resource.
1. Replace `<your_subscription_key>` with one of the keys that come with your resource.
1. Optionally, replace the `"code"` field in the body with your own code that you'd like to analyze.
    > [!TIP]
    > See [Input requirements](../../overview.md#input-requirements) for maximum code length limitations. Protected material detection is meant to be run on LLM completions, not user prompts.

```shell
curl --location --request POST '<endpoint>/contentsafety/text:detectProtectedMaterialForCode?api-version=2024-09-15-preview' \
--header 'Ocp-Apim-Subscription-Key: <your_subscription_key>' \
--header 'Content-Type: application/json' \
--data-raw '{
  "code": "python import pygame pygame.init() win = pygame.display.set_mode((500, 500)) pygame.display.set_caption(My Game) x = 50 y = 50 width = 40 height = 60 vel = 5 run = True while run: pygame.time.delay(100) for event in pygame.event.get(): if event.type == pygame.QUIT: run = False keys = pygame.key.get_pressed() if keys[pygame.K_LEFT] and x > vel: x -= vel if keys[pygame.K_RIGHT] and x < 500 - width - vel: x += vel if keys[pygame.K_UP] and y > vel: y -= vel if keys[pygame.K_DOWN] and y < 500 - height - vel: y += vel win.fill((0, 0, 0)) pygame.draw.rect(win, (255, 0, 0), (x, y, width, height)) pygame.display.update() pygame.quit()"
}'
```
The following fields must be included in the URL:

| Name      |Required?  |  Description | Type   |
| :------- |-------- |:--------------- | ------ |
| **API Version** |Required |This is the API version to be checked. The current version is: api-version=2024-09-15-preview. Example: `<endpoint>/contentsafety/text:detectProtectedMaterialForCode?api-version=2024-09-15-preview` |String |

The parameters in the request body are defined in this table:

| Name        | Required?     | Description  | Type    |
| :---------- | ----------- | :------------ | ------- |
| **code**    | Required | This is the raw code to be checked. Other non-ascii characters can be included. | String  |

See the following sample value for the `"code"` field:
```json
{
    "code": "python import pygame pygame.init() win = pygame.display.set_mode((500, 500)) pygame.display.set_caption(My Game) x = 50 y = 50 width = 40 height = 60 vel = 5 run = True while run: pygame.time.delay(100) for event in pygame.event.get(): if event.type == pygame.QUIT: run = False keys = pygame.key.get_pressed() if keys[pygame.K_LEFT] and x > vel: x -= vel if keys[pygame.K_RIGHT] and x < 500 - width - vel: x += vel if keys[pygame.K_UP] and y > vel: y -= vel if keys[pygame.K_DOWN] and y < 500 - height - vel: y += vel win.fill((0, 0, 0)) pygame.draw.rect(win, (255, 0, 0), (x, y, width, height)) pygame.display.update() pygame.quit()"
}
```

Open a command prompt window and run the cURL command.

### Interpret the API response

You should see the protected material detection results displayed as JSON data in the console output. For example:

```json
{
    "protectedMaterialAnalysis": {
        "detected": true,
        "codeCitations": [
            {
                "license": "NOASSERTION",
                "sourceUrls": [
                    "https://github.com/kolejny-projekt-z-kck/game-/tree/f134099ce970da951bac9baac83c7885e991c676/ganeee.py",
                    "https://github.com/Felipe-Velasco/Modulo-Pygame/tree/11490c44a951812dc0c6424b68b1e14fc5cc4c0b/pygame%20basics.py",
                    "https://github.com/bwootton/firstgame/tree/70d722a6b1ccb79bfa56d9cc69932051848c44bf/jump.py",
                    "https://github.com/Jason017/Pygame-Learning-Module/tree/17cd69f169d3759e00816ed4a3795dd6db7e157f/pygameModule02.py",
                    "https://github.com/Coders-Brothers/pygame-tutorial/tree/1b481f5687cdda7c0765089780ef451af6e175cd/lesson-2.py"
                ]
            }
        ]
    }
}
```

The JSON fields in the output are defined here:

| Name     | Description   | Type   |
| :------------- | :--------------- | ------ |
| **protectedMaterialAnalysis**   | Analysis results containing details about detected protected code. | Object |
| **detected** | Indicates whether protected material from GitHub repositories was detected. | Boolean |
| **codeCitations** | List of citations where the protected code was found. | Array |
| **codeCitations.license** | The license type associated with the detected code. | String |
| **codeCitations.sourceUrls** | A list of URLs from GitHub repositories where the protected code was detected.  | Array of Strings |

## Troubleshooting

- **401/403**: Confirm you’re using a valid key for the same resource as the endpoint.
- **Feature not available**: Confirm the resource is in a supported region for Protected material (Code).
- **Invalid input length**: Ensure the `code` string meets the minimum length and stays under the maximum (see [Input requirements](../../overview.md#input-requirements)).


## Clean up resources

If you want to clean up and remove an Azure AI services subscription, you can delete the resource or resource group. Deleting the resource group also deletes any other resources associated with it.

- [Azure portal](../../../multi-service-resource.md?pivots=azportal#clean-up-resources)
- [Azure CLI](../../../multi-service-resource.md?pivots=azcli#clean-up-resources)

