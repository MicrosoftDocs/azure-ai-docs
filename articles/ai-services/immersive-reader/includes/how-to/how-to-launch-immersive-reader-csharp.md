---
author: sharmas
manager: nitinme
ms.service: azure-ai-immersive-reader
ms.topic: include
ms.date: 03/02/2026
ms.author: sharmas
---

## Prerequisites

* An Azure subscription. You can [create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
* An Immersive Reader resource configured for Microsoft Entra authentication. Follow [these instructions](../../how-to-create-immersive-reader.md) to get set up. Save the output of your session into a text file so you can configure the environment properties.
* [Visual Studio](https://visualstudio.microsoft.com) with the **ASP.NET and web development** workload, or the [.NET SDK](https://dotnet.microsoft.com/download) and an IDE such as [Visual Studio Code](https://code.visualstudio.com).
* [Git](https://git-scm.com).
* Clone the [Immersive Reader SDK](https://github.com/microsoft/immersive-reader-sdk) from GitHub.

## Configure authentication credentials

This guide uses [`DefaultAzureCredential`](/dotnet/api/azure.identity.defaultazurecredential) from the `Azure.Identity` library to authenticate with the Immersive Reader service. No client secret is required in your code. Locally, `DefaultAzureCredential` uses your signed-in Azure CLI or Visual Studio credentials. When deployed to Azure, it automatically uses the managed identity assigned to your app.

You need only your Immersive Reader resource **subdomain**. Save the subdomain value from when you created your Immersive Reader resource.

Secure the **GetTokenAndSubdomain** API endpoint behind some form of authentication, such as [OAuth](https://oauth.net/2/). Authentication prevents unauthorized users from obtaining tokens to use against your Immersive Reader service and billing. That work is beyond the scope of this tutorial.

## Create an ASP.NET Core MVC web app

Create a new ASP.NET Core MVC web application.

# [.NET CLI](#tab/dotnet-cli)

```dotnetcli
dotnet new mvc -n QuickstartSampleWebApp
cd QuickstartSampleWebApp
```

Install the `Azure.Identity` package to acquire Microsoft Entra tokens without any client secrets:

```dotnetcli
dotnet add package Azure.Identity
```

# [Visual Studio](#tab/visual-studio)

1. Select **File** > **New** > **Project**.
2. Select **ASP.NET Core Web App (Model-View-Controller)** and select **Next**.
3. Name the project **QuickstartSampleWebApp** and select **Create**.

Install the `Azure.Identity` NuGet package. In the **NuGet Package Manager Console** (**Tools** > **NuGet Package Manager** > **Package Manager Console**), run:

```console
Install-Package Azure.Identity
```

---

## Set up the controller

Open *Controllers\HomeController.cs* and replace its contents with the following code. Replace `{YOUR_SUBDOMAIN}` with the subdomain of your Immersive Reader resource. This controller uses `DefaultAzureCredential` to acquire a Microsoft Entra authentication token and passes the token and subdomain to the view.

```csharp
using System.Threading;
using System.Threading.Tasks;
using Azure.Core;
using Azure.Identity;
using Microsoft.AspNetCore.Mvc;

namespace QuickstartSampleWebApp.Controllers
{
    public class HomeController : Controller
    {
        // Replace with your Immersive Reader resource subdomain.
        private const string Subdomain = "{YOUR_SUBDOMAIN}";

        private static readonly TokenCredential Credential = new DefaultAzureCredential();
        private static readonly string[] Scopes =
            new[] { "https://cognitiveservices.azure.com/.default" };

        private async Task<string> GetTokenAsync()
        {
            var tokenRequestContext = new TokenRequestContext(Scopes);
            var accessToken = await Credential
                .GetTokenAsync(tokenRequestContext, CancellationToken.None)
                .ConfigureAwait(false);
            return accessToken.Token;
        }

        public async Task<IActionResult> Index()
        {
            ViewData["Token"]     = await GetTokenAsync();
            ViewData["Subdomain"] = Subdomain;
            return View();
        }
    }
}
```

## Launch the Immersive Reader with sample content

1. Open *Views\Home\Index.cshtml* and replace its contents with the following code. This code populates the page with sample content and adds a button that launches the Immersive Reader.

   ```cshtml
   @{
       ViewData["Title"] = "Immersive Reader C# Quickstart";
       var token     = ViewData["Token"]     as string;
       var subdomain = ViewData["Subdomain"] as string;
   }

   <div class="container">
       <button class="immersive-reader-button"
               data-button-style="iconAndText"
               data-locale="en">
       </button>

       <h1 id="ir-title">Geography</h1>
       <div id="ir-content" lang="en-us">
           <p>
               The study of Earth's landforms is called physical geography.
               Landforms can be mountains and valleys.
               They can also be glaciers, lakes, or rivers.
           </p>
       </div>
   </div>

   @section Scripts {
       <script src="https://ircdname.azureedge.net/immersivereadersdk/immersive-reader-sdk.1.4.0.js">
       </script>
       <script>
           function handleLaunchImmersiveReader() {
               const token     = "@token";
               const subdomain = "@subdomain";

               const data = {
                   title: document.getElementById('ir-title').innerText,
                   chunks: [{
                       content: document.getElementById('ir-content').innerHTML,
                       mimeType: 'text/html'
                   }]
               };

               const options = {
                   onExit: exitCallback
               };

               ImmersiveReader.launchAsync(token, subdomain, data, options)
                   .catch(function (error) {
                       console.log(error);
                       alert('Error in launching the Immersive Reader. Check the console.');
                   });
           }

           function exitCallback() {
               console.log('This is the callback function. It is executed when the Immersive Reader closes.');
           }

           document.querySelector('.immersive-reader-button')
               .addEventListener('click', handleLaunchImmersiveReader);
       </script>
   }
   ```

2. Start the app.

   # [.NET CLI](#tab/dotnet-cli)

   ```dotnetcli
   dotnet run
   ```

   # [Visual Studio](#tab/visual-studio)

   Select **Debug** > **Start Debugging**.

   ---

3. Open your browser and go to `https://localhost:5001`. You should see the sample content on the page. Select the **Immersive Reader** button to launch the Immersive Reader with your content.

## Specify the language of your content

The Immersive Reader supports many different languages. You can specify the language of your content by following these steps.

1. In *Views\Home\Index.cshtml*, add the following paragraph inside `#ir-content`, after the existing English paragraph:

   ```html
   <p lang="es">
       El estudio de las formas terrestres de la Tierra se llama geografía física.
       Los accidentes geográficos pueden ser montañas y valles.
       También pueden ser glaciares, lagos o ríos.
   </p>
   ```

2. In the `data` object in the script block, update the `chunks` array to include the Spanish paragraph:

   ```javascript
   const data = {
       title: document.getElementById('ir-title').innerText,
       chunks: [
           {
               content: document.getElementById('ir-content').innerHTML,
               mimeType: 'text/html'
           }
       ]
   };
   ```

   The Immersive Reader automatically detects languages within the HTML content, so no additional changes to the chunks array are required.

3. Navigate to `https://localhost:5001` again. You should see the Spanish text on the page, and when you select **Immersive Reader**, it shows up in the Immersive Reader as well.

## Specify the language of the Immersive Reader interface

By default, the language of the Immersive Reader interface matches your browser language settings. You can also specify it explicitly.

1. In *Views\Home\Index.cshtml*, update the `options` object in the script block:

   ```javascript
   const options = {
       uiLang: 'fr',
       onExit: exitCallback
   };
   ```

2. Navigate to `https://localhost:5001`. When you launch the Immersive Reader, the interface is shown in French.

## Launch the Immersive Reader with math content

You can include math content in the Immersive Reader by using [MathML](https://developer.mozilla.org/en-US/docs/Web/MathML).

1. In *Views\Home\Index.cshtml*, add the following code inside `handleLaunchImmersiveReader`, just before the `ImmersiveReader.launchAsync` call:

   ```javascript
   const mathML = '<math xmlns="https://www.w3.org/1998/Math/MathML" display="block">'
       + '<munderover><mo>∫</mo><mn>0</mn><mn>1</mn></munderover>'
       + '<mrow><msup><mi>x</mi><mn>2</mn></msup><mo>ⅆ</mo><mi>x</mi></mrow>'
       + '</math>';

   data.chunks.push({
       content: mathML,
       mimeType: 'application/mathml+xml'
   });
   ```

2. Navigate to `https://localhost:5001`. When you launch the Immersive Reader and scroll to the bottom, you'll see the math formula.

## Next step

> [!div class="nextstepaction"]
> [Explore the Immersive Reader SDK reference](../../reference.md)
