---
title: Immersive Reader Node.js client library quickstart 
titleSuffix: Azure AI services
description: In this quickstart, you build a web app from scratch and add the Immersive Reader API functionality.
author: sharmas
manager: nitinme
ms.service: azure-ai-immersive-reader
ms.topic: include
ms.date: 02/14/2024
ms.author: sharmas
ms.custom: devx-track-js
---

In this quickstart, you build a web app from scratch and integrate Immersive Reader using the Immersive Reader client library. A full working sample of this quickstart is [available on GitHub](https://github.com/microsoft/immersive-reader-sdk/tree/master/js/samples/quickstart-nodejs).

## Prerequisites

* An Azure subscription. You can [create one for free](https://azure.microsoft.com/free/ai-services).
* An Immersive Reader resource configured for Microsoft Entra authentication. Follow [these instructions](../../how-to-create-immersive-reader.md) to get set up. Save the output of your session into a text file so you can configure the environment properties.
* An IDE such as [Visual Studio Code](https://code.visualstudio.com).

## Create a Node.js web app with Express

Create a Node.js web app by using the `express-generator` tool.

```bash
npm install express-generator -g
express --view=pug quickstart-nodejs
cd quickstart-nodejs
```

Install yarn dependencies, and add dependencies `request` and `dotenv`.

```bash
yarn
yarn add request
yarn add dotenv
```

Install the `axios` and `qs` libraries.

```bash
npm install axios qs
```

## Set up authentication

Create a new file called *.env* in the root of your project. Paste the following code into it, supplying the values given when you created your Immersive Reader resource. Don't include quotation marks or the `{` and `}` characters.

> [!IMPORTANT]
> Remember to never post secrets publicly. For production, use a secure way of storing and accessing your credentials like [Azure Key Vault](/azure/key-vault/general/overview).

```text
TENANT_ID={YOUR_TENANT_ID}
CLIENT_ID={YOUR_CLIENT_ID}
CLIENT_SECRET={YOUR_CLIENT_SECRET}
SUBDOMAIN={YOUR_SUBDOMAIN}
```

Be sure not to commit this file into source control, since it contains secrets that shouldn't be made public.

Next, open *app.js* and add the following code to the top of the file. This loads the properties defined in the *.env* file as environment variables into Node.

```javascript
require('dotenv').config();
```

### Update the router to acquire the token

Open the *routes\index.js* file and replace the automatically generated code with the following code.

This code creates an API endpoint that acquires a Microsoft Entra ID authentication token using your service principal password. It also retrieves the subdomain. It then returns an object containing the token and subdomain.

```javascript
var axios = require('axios');
var express = require('express');
var router = express.Router();
var qs = require('qs');

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Express' });
});

router.get('/GetTokenAndSubdomain', function(req, res) {
    try {
        var config ={
            headers: {
                'content-type': 'application/x-www-form-urlencoded'
            }
        }
        var data = {
            grant_type: 'client_credentials',
            client_id: process.env.CLIENT_ID,
            client_secret: process.env.CLIENT_SECRET,
            resource: 'https://cognitiveservices.azure.com/'
        };
        var url = `https://login.windows.net/${process.env.TENANT_ID}/oauth2/token`
        console.log(qs.stringify(data));
        axios.post(url, qs.stringify(data), config)
        .then(function (response) {
            var token = response.data.access_token;
            var subdomain = process.env.SUBDOMAIN;
            return res.send({token, subdomain});
        })
        .catch(function (response) {
            if (response.status !== 200) {
                return res.send({error :  "Unable to acquire Microsoft Entra token. Check the debugger for more information."})
            }
        });
    } catch (error) {
        console.log(error);
        return res.status(500).send('CogSvcs IssueToken error');
    }
});

module.exports = router;
```

The **GetTokenAndSubdomain** API endpoint should be secured behind some form of authentication, such as [OAuth](https://oauth.net/2/), to prevent unauthorized users from obtaining tokens to use against your Immersive Reader service and billing; that work is beyond the scope of this quickstart.

## Add sample content

Now add sample content to this web app. Open *views\index.pug* and replace the automatically generated code with this sample:

```pug
doctype html
html
   head
      title Immersive Reader Quickstart Node.js

      link(rel='icon', href='data:;base64,iVBORw0KGgo=')

      link(rel='stylesheet', href='https://stackpath.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css')

      // A polyfill for Promise is needed for IE11 support.
      script(src='https://cdn.jsdelivr.net/npm/promise-polyfill@8/dist/polyfill.min.js')

      script(src='https://ircdname.azureedge.net/immersivereadersdk/immersive-reader-sdk.1.4.0.js')
      script(src='https://code.jquery.com/jquery-3.3.1.min.js')

      style(type="text/css").
        .immersive-reader-button {
          background-color: white;
          margin-top: 5px;
          border: 1px solid black;
          float: right;
        }
   body
      div(class="container")
        button(class="immersive-reader-button" data-button-style="iconAndText" data-locale="en")

        h1(id="ir-title") About Immersive Reader
        div(id="ir-content" lang="en-us")
          p Immersive Reader is a tool that implements proven techniques to improve reading comprehension for emerging readers, language learners, and people with learning differences. The Immersive Reader is designed to make reading more accessible for everyone. The Immersive Reader

            ul
                li Shows content in a minimal reading view
                li Displays pictures of commonly used words
                li Highlights nouns, verbs, adjectives, and adverbs
                li Reads your content out loud to you
                li Translates your content into another language
                li Breaks down words into syllables

          h3 The Immersive Reader is available in many languages.

          p(lang="es-es") El Lector inmersivo está disponible en varios idiomas.
          p(lang="zh-cn") 沉浸式阅读器支持许多语言
          p(lang="de-de") Der plastische Reader ist in vielen Sprachen verfügbar.
          p(lang="ar-eg" dir="rtl" style="text-align:right") يتوفر \"القارئ الشامل\" في العديد من اللغات.

script(type="text/javascript").
  function getTokenAndSubdomainAsync() {
        return new Promise(function (resolve, reject) {
            $.ajax({
                url: "/GetTokenAndSubdomain",
                type: "GET",
                success: function (data) {
                    if (data.error) {
                        reject(data.error);
                    } else {
                        resolve(data);
                    }
                },
                error: function (err) {
                    reject(err);
                }
            });
        });
    }

    $(".immersive-reader-button").click(function () {
        handleLaunchImmersiveReader();
    });

    function handleLaunchImmersiveReader() {
        getTokenAndSubdomainAsync()
            .then(function (response) {
                const token = response["token"];
                const subdomain = response["subdomain"];
                // Learn more about chunk usage and supported MIME types https://learn.microsoft.com/azure/ai-services/immersive-reader/reference#chunk
                const data = {
                    title: $("#ir-title").text(),
                    chunks: [{
                        content: $("#ir-content").html(),
                        mimeType: "text/html"
                    }]
                };
                // Learn more about options https://learn.microsoft.com/azure/ai-services/immersive-reader/reference#options
                const options = {
                    "onExit": exitCallback,
                    "uiZIndex": 2000
                };
                ImmersiveReader.launchAsync(token, subdomain, data, options)
                    .catch(function (error) {
                        alert("Error in launching the Immersive Reader. Check the console.");
                        console.log(error);
                    });
            })
            .catch(function (error) {
                alert("Error in getting the Immersive Reader token and subdomain. Check the console.");
                console.log(error);
            });
    }

    function exitCallback() {
        console.log("This is the callback function. It is executed when the Immersive Reader closes.");
    }
```

Notice that all of the text has a `lang` attribute, which describes the languages of the text. This attribute helps the Immersive Reader provide relevant language and grammar features.

## Build and run the app

Our web app is now ready. Start the app by running:

```bash
npm start
```

Open your browser and navigate to `http://localhost:3000`. You should see:

:::image type="content" source="../../media/quickstart-nodejs/1-build-app.png" alt-text="Screenshot of the app in the browser.":::

### Launch the Immersive Reader

When you select the **Immersive Reader** button, the Immersive Reader launches with the content on the page.

:::image type="content" source="../../media/quickstart-nodejs/2-view-immersive-reader.png" alt-text="Screenshot of the Immersive Reader app.":::

## Next step

> [!div class="nextstepaction"]
> [Explore the Immersive Reader SDK reference](../../reference.md)
