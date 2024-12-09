---
title: Use Document Translation APIs programmatically
description: "How to create a Document Translation service using C#, Go, Java, Node.js, or Python and the REST API"
#services: cognitive-services
author: laujan
manager: nitinme
ms.service: azure-ai-translator
ms.topic: quickstart
ms.date: 11/19/2024
ms.author: lajanuar
recommendations: false
ms.devlang: csharp
# ms.devlang: csharp, golang, java, javascript, python
ms.custom: mode-other, build-2023, devx-track-extended-java, devx-track-python, ignite-2024
---

# Use REST APIs programmatically

 Document Translation is a cloud-based feature of the [Azure AI Translator](../../translator-overview.md) service. You can use the Document Translation API to asynchronously translate whole documents in [supported languages](../../language-support.md) and various [file formats](../overview.md#batch-supported-document-formats) while preserving source document structure and text formatting. In this how-to guide, you learn to use Document Translation APIs with a programming language of your choice and the HTTP REST API.

## Prerequisites

> [!NOTE]
>
> Document Translation is supported in the S1 Standard Service Plan (Pay-as-you-go) and C2, C3, C4, and D3 Volume Discount Plans. _See_ [Azure AI services pricing—Translator](https://azure.microsoft.com/pricing/details/cognitive-services/translator/).
>

To get started, you need:

* An active [**Azure account**](https://azure.microsoft.com/free/cognitive-services/). If you don't have one, you can [**create a free account**](https://azure.microsoft.com/free/)

* An [**Azure Blob Storage account**](https://portal.azure.com/#create/Microsoft.StorageAccount-ARM). You also need to [create containers](#create-azure-blob-storage-containers) in your Azure Blob Storage account for your source and target files:

  * **Source container**. This container is where you upload your files for translation (required).
  * **Target container**. This container is where your translated files are stored (required).

* A [**Translator resource**](https://portal.azure.com/#create/Microsoft.CognitiveServicesTextTranslation):

  **Complete the Translator project and instance details fields as follows:**

  1. **Subscription**. Select one of your available Azure subscriptions.

  1. **Resource Group**. You can create a new resource group or add your resource to an existing resource group that shares the same lifecycle, permissions, and policies.

  1. **Resource Region**. Choose **Global** unless your business or application requires a specific region. If you're planning on using a [system-assigned managed identity](create-use-managed-identities.md) for authentication, choose a **geographic** region like **West US**.

  1. **Name**. Enter the name you chose for your resource. The name you choose must be unique within Azure.

     > [!NOTE]
     > Document Translation requires a custom domain endpoint. The value that you enter in the Name field will be the custom domain name parameter for your endpoint.

  1. **Pricing tier**. Document Translation isn't supported in the free tier. To try the service, select Standard S1.

  1. Select **Review + Create**.

  1. Review the service terms and select **Create** to deploy your resource.

  1. After your resource successfully deploys, select **Go to resource** to [retrieve your key and endpoint](#set-up-your-coding-platform).

### Retrieve your key and custom domain endpoint

* Requests to the Translator service require a read-only key and custom endpoint to authenticate access. The custom domain endpoint is a URL formatted with your resource name, hostname, and Translator subdirectories and is available in the Azure portal.

1. If you created a new resource, after it deploys, select **Go to resource**. If you have an existing Document Translation resource, navigate directly to your resource page.

1. In the left rail, under *Resource Management*, select **Keys and Endpoint**.

1. Copy and paste your **`key`** and **`document translation endpoint`** in a convenient location, such as *Microsoft Notepad*. Only one key is necessary to make an API call.

1. You **`key`** and **`document translation endpoint`** into the code samples to authenticate your request to the Document Translation service.

    :::image type="content" source="../media/document-translation-key-endpoint.png" alt-text="Screenshot showing the get your key field in Azure portal.":::

### Get your key

Requests to the Translator service require a read-only key for authenticating access.

1. If you created a new resource, after it deploys, select **Go to resource**. If you have an existing Document Translation resource, navigate directly to your resource page.
1. In the left rail, under *Resource Management*, select **Keys and Endpoint**.
1. Copy and paste your key in a convenient location, such as *Microsoft Notepad*.
1. You paste it into the code sample to authenticate your request to the Document Translation service.

:::image type="content" source="../../media/translator-keys.png" alt-text="Image of the get your key field in Azure portal.":::

## Create Azure Blob Storage containers

You need to  [**create containers**](/azure/storage/blobs/storage-quickstart-blobs-portal#create-a-container) in your [**Azure Blob Storage account**](https://portal.azure.com/#create/Microsoft.StorageAccount-ARM) for source and target files.

* **Source container**. This container is where you upload your files for translation (required).
* **Target container**. This container is where your translated files are stored (required).

> [!NOTE]
> Document Translation supports glossaries as blobs in target containers (not separate glossary containers). If want to include a custom glossary, add it to the target container and include the` glossaryUrl` with the request.  If the translation language pair is not present in the glossary, it will not be applied. *See* [Translate documents using a custom glossary](#translate-documents-using-a-custom-glossary)

### **Create SAS access tokens for Document Translation**

The `sourceUrl` , `targetUrl` , and optional `glossaryUrl`  must include a Shared Access Signature (SAS) token, appended as a query string. The token can be assigned to your container or specific blobs. *See* [**Create SAS tokens for Document Translation process**](create-sas-tokens.md).

* Your **source** container or blob must designate  **read** and **list** access.
* Your **target** container or blob must designate  **write** and **list** access.
* Your **glossary** blob must designate  **read** and **list** access.

> [!TIP]
>
> * If you're translating **multiple** files (blobs) in an operation, **delegate SAS access at the  container level**.
> * If you're translating a **single** file (blob) in an operation, **delegate SAS access at the blob level**.
> * As an alternative to SAS tokens, you can use a [**system-assigned managed identity**](../how-to-guides/create-use-managed-identities.md) for authentication.

## HTTP requests

An asynchronous batch translation request is submitted to your Translator service endpoint via a POST request. If successful, the POST method returns a `202 Accepted`  response code and the service creates a batch request. The translated documents are listed in your target container.

For detailed information regarding Azure AI Translator Service request limits, _see_ [**Document Translation request limits**](../../service-limits.md#document-translation).

### HTTP headers

The following headers are included with each Document Translation API request:

|HTTP header|Description|
|---|--|
|Ocp-Apim-Subscription-Key|**Required**: The value is the Azure key for your Translator or Azure AI services resource.|
|Content-Type|**Required**: Specifies the content type of the payload. Accepted values are application/json or charset=UTF-8.|

### POST request body properties

* The POST request URL is POST `https://<NAME-OF-YOUR-RESOURCE>.cognitiveservices.azure.com/translator/text/batch/v1.1/batches`.
* The POST request body is a JSON object named `inputs`.
* The `inputs` object contains both  `sourceURL` and `targetURL`  container addresses for your source and target language pairs.
* The `prefix` and `suffix` are case-sensitive strings to filter documents in the source path for translation. The `prefix` field is often used to delineate subfolders for translation. The `suffix` field is most often used for file extensions.
* A value for the  `glossaries`  field (optional) is applied when the document is being translated.
* The `targetUrl` for each target language must be unique.

>[!NOTE]
> If a file with the same name already exists in the destination, the job will fail.

<!-- markdownlint-disable MD024 -->
### Translate all documents in a container

```json
{
    "inputs": [
        {
            "source": {
                "sourceUrl": "{sourceSASUrl}"
            },
            "targets": [
                {
                    "targetUrl": "{targetSASUrl}",
                    "language": "fr"
                }
            ]
        }
    ]
}
```

### Translate a specific document in a container

* Specify `"storageType": "File"`.
* If you aren't using a [**system-assigned managed identity**](create-use-managed-identities.md) for authentication, make sure you created source URL & SAS tokens for the specific blob/document (not for the container).
* Ensure you specified the target filename as part of the target URL – though the SAS token is still for the container.
* This sample request returns a single document translated into two target languages.

```json
{
    "inputs": [
        {
            "storageType": "File",
            "source": {
                "sourceUrl": "{sourceSASUrl}"
            },
            "targets": [
                {
                    "targetUrl": "{targetSASUrl}",
                    "language": "es"
                },
                {
                    "targetUrl": "{targetSASUrl}",
                    "language": "de"
                }
            ]
        }
    ]
}
```

### Translate documents using a custom glossary

```json
{
    "inputs": [
        {
            "source": {
                "sourceUrl": "{sourceSASUrl}"
             },
            "targets": [
                {
                    "targetUrl": "{targetSASUrl}",
                    "language": "es",
                    "glossaries": [
                        {
                            "glossaryUrl": "{glossaryUrl/en-es.xlf}",
                            "format": "xliff"
                        }
                    ]
                }
            ]
        }
    ]
}
```

### 🆕 Translate text embedded in images within documents

> [!Note]
>
> * This feature is optional and must be enabled for each translation request.
> * Enabling this feature will incur additional costs based on usage. For more information, *see* [Azure AI Vision pricing](https://azure.microsoft.com/pricing/details/cognitive-services/computer-vision/)
> * This feature is currently available only with the Batch Document Translation API.
> * The Supported file format is `.docx` only.
> * An Azure AI Services resource (not the standalone Translator resource) is required to use this feature.

### Request configuration

* Use the optional `translateTextWithinImage` parameter in the `options` field

   * Data type: Boolean (`true` or `false`) 
   * Default Boolean setting is `false`. Set the option to `true` to enable image text translation.

* **Response Details**. When the feature is enabled, added image processing information is included with the response: 

   * **`totalImageScansSucceeded`**. The number of successfully translated image scans.

   * **`totalImageScansFailed`**. The number of image scans that failed processing.


## Use code to submit Document Translation requests

### Set up your coding Platform

### [C#](#tab/csharp)

* Create a new project.
* Replace Program.cs with the C# code sample.
* Set your endpoint, key, and container URL values in Program.cs.
* Add [Newtonsoft.Json package using .NET CLI](https://www.nuget.org/packages/Newtonsoft.Json/) for processing JSON data.
* Run the program from the project directory.

### [Node.js](#tab/javascript)

* Create a new Node.js project.
* Install the Axios library with `npm i axios`.
* Copy/paste the JavaScript sample code into your project.
* Set your endpoint, key, and container URL values.
* Run the program.

### [Python](#tab/python)

* Create a new project.
* Copy and paste the code from one of the samples into your project.
* Set your endpoint, key, and container URL values.
* Run the program. For example: `python translate.py`.

### [Java](#tab/java)

* Create a working directory for your project. For example:

```powershell
mkdir sample-project
```

* In your project directory, create the following subdirectory structure:

  src</br>
&emsp; └ main</br>
&emsp;&emsp;&emsp;└ java

```powershell
mkdir -p src/main/java/
```

**NOTE**: Java source files (for example, _sample.java_) live in src/main/**java**.

* In your root directory (for example, *sample-project*),  initialize your project with Gradle:

```powershell
gradle init --type basic
```

* When prompted to choose a **DSL**, select **Kotlin**.

* Update the `build.gradle.kts` file. Keep in mind that you need to update your `mainClassName` depending on the sample:

    ```java
    plugins {
      java
      application
    }
    application {
      mainClassName = "{NAME OF YOUR CLASS}"
    }
    repositories {
      mavenCentral()
    }
    dependencies {
      compile("com.squareup.okhttp:okhttp:2.5.0")
    }
    ```

* Create a Java file in the **java** directory and copy/paste the code from the provided sample. Don't forget to add your key and endpoint.

* **Build and run the sample from the root directory**:

  ```powershell
  gradle build
  gradle run
  ```

### [Go](#tab/go)

* Create a new Go project.
* Add the provided Go code sample.
* Set your endpoint, key, and container URL values.
* Save the file with a `.go` extension.
* Open a command prompt on a computer with Go installed.
* Build the file. For example: `go build example-code.go`.
* Run the file, for example: `example-code`.

 ---

> [!IMPORTANT]
>
> For the code samples, you'll hard-code your Shared Access Signature (SAS) URL where indicated. Remember to remove the SAS URL from your code when you're done, and never post it publicly. For production, use a secure way of storing and accessing your credentials like [Azure Managed Identity](create-use-managed-identities.md). For more information, _see_ Azure Storage [security](/azure/storage/common/authorize-data-access).

> You may need to update the following fields, depending upon the operation:
>>>
>> * `endpoint`
>> * `basePath`
>> * `key`
>> * `sourceURL`
>> * `targetURL`
>> * `glossaryURL`
>> * `id`  (job ID)
>>

#### Locating  the `id` value

* You can find the job `id`  in the POST `start-batch-translation` method response Header `Operation-Location`  URL value. The alphanumeric string following the `/document/` parameter is the operation's job **`id`**:

|**Response header**|**Response URL**|
|-----------------------|----------------|
|Operation-Location   | {document-translation-endpoint}/translator/document/`9dce0aa9-78dc-41ba-8cae-2e2f3c2ff8ec`?api-version={date}|

* You can also use a [get-translations-status](../reference/get-translations-status.md) request to retrieve a list of translation _**jobs**_ and their `id`s.

## Start asynchronous batch translation

### [C#](#tab/csharp)

```csharp

    using System;
    using System.Net.Http;
    using System.Threading.Tasks;
    using System.Text;


    class Program
    {

        static readonly string route = "?api-version={date}";

        private static readonly string basePath = "{your-document-translation-endpoint}/translator/document/batches";

        private static readonly string key = "{your-api-key}";

        static readonly string json = ("{\"inputs\": [{\"source\": {\"sourceUrl\": \"https://YOUR-SOURCE-URL-WITH-READ-LIST-ACCESS-SAS\",\"storageSource\": \"AzureBlob\",\"language\": \"en\"}, \"targets\": [{\"targetUrl\": \"https://YOUR-TARGET-URL-WITH-WRITE-LIST-ACCESS-SAS\",\"storageSource\": \"AzureBlob\",\"category\": \"general\",\"language\": \"es\"}]}]}");

        static async Task Main(string[] args)
        {
            using HttpClient client = new HttpClient();
            using HttpRequestMessage request = new HttpRequestMessage();
            {

                StringContent content = new StringContent(json, Encoding.UTF8, "application/json");

                request.Method = HttpMethod.Post;
                request.RequestUri = new Uri(basePath + route);
                request.Headers.Add("Ocp-Apim-Subscription-Key", key);
                request.Content = content;

                HttpResponseMessage  response = await client.SendAsync(request);
                string result = response.Content.ReadAsStringAsync().Result;
                if (response.IsSuccessStatusCode)
                {
                    Console.WriteLine($"Status code: {response.StatusCode}");
                    Console.WriteLine();
                    Console.WriteLine($"Response Headers:");
                    Console.WriteLine(response.Headers);
                }
                else
                    Console.Write("Error");

            }

        }

    }
```

### [Node.js](#tab/javascript)

```javascript

const axios = require('axios').default;

let basePath = '{your-document-translation-endpoint}/translator/document/batches';
let route = '?api-version={date}';
let key = '{your-api-key}';

let data = JSON.stringify({"inputs": [
  {
      "source": {
          "sourceUrl": "https://YOUR-SOURCE-URL-WITH-READ-LIST-ACCESS-SAS",
          "storageSource": "AzureBlob",
          "language": "en"
          }
      },
      "targets": [
          {
              "targetUrl": "https://YOUR-TARGET-URL-WITH-WRITE-LIST-ACCESS-SAS",
              "storageSource": "AzureBlob",
              "category": "general",
              "language": "es"}]});

let config = {
  method: 'post',
  baseURL: basePath,
  url: route,
  headers: {
    'Ocp-Apim-Subscription-Key': key,
    'Content-Type': 'application/json'
  },
  data: data
};

axios(config)
.then(function (response) {
  let result = { statusText: response.statusText, statusCode: response.status, headers: response.headers };
  console.log()
  console.log(JSON.stringify(result));
})
.catch(function (error) {
  console.log(error);
});
```

### [Python](#tab/python)

```python

import requests

base_path = '{your-document-translation-endpoint}/translator/document/batches'
key =  '{your-api-key}'
route = '?api-version={date}'
constructed_url = base_path + route

payload= {
    "inputs": [
        {
            "source": {
                "sourceUrl": "https://YOUR-SOURCE-URL-WITH-READ-LIST-ACCESS-SAS",
                "storageSource": "AzureBlob",
                "language": "en"
            },
            "targets": [
                {
                    "targetUrl": "https://YOUR-TARGET-URL-WITH-WRITE-LIST-ACCESS-SAS",
                    "storageSource": "AzureBlob",
                    "category": "general",
                    "language": "es"
                }
            ]
        }
    ]
}
headers = {
  'Ocp-Apim-Subscription-Key': key,
  'Content-Type': 'application/json'
}

response = requests.post(constructed_url, headers=headers, json=payload)

print(f'response status code: {response.status_code}\nresponse status: {response.reason}\nresponse headers: {response.headers}')
```

### [Java](#tab/java)

```java

import java.io.*;
import java.net.*;
import java.util.*;
import com.squareup.okhttp.*;

public class DocumentTranslation {
    String key = "{your-api-key}";
    String basePath = "{your-document-translation-endpoint}/translator/document/batches";
    String route = basePath + "?api-version={date}";

    OkHttpClient client = new OkHttpClient();

    public void post() throws IOException {
        MediaType mediaType = MediaType.parse("application/json");
        RequestBody body = RequestBody.create(mediaType,  "{\n \"inputs\": [\n {\n \"source\": {\n \"sourceUrl\": \"https://YOUR-SOURCE-URL-WITH-READ-LIST-ACCESS-SAS\",\n  },\n  \"language\": \"en\",\n \"storageSource\": \"AzureBlob\"\n  },\n \"targets\": [\n {\n \"targetUrl\": \"https://YOUR-TARGET-URL-WITH-WRITE-LIST-ACCESS-SAS\",\n \"category\": \"general\",\n\"language\": \"fr\",\n\"storageSource\": \"AzureBlob\"\n }\n ],\n \"storageType\": \"Folder\"\n }\n  ]\n}");
        Request request = new Request.Builder()
                .url(route).post(body)
                .addHeader("Ocp-Apim-Subscription-Key", key)
                .addHeader("Content-type", "application/json")
                .build();
        Response response = client.newCall(request).execute();
        System.out.println(response.code());
        System.out.println(response.headers());
    }

  public static void main(String[] args) {
        try {
            DocumentTranslation sampleRequest = new DocumentTranslation();
            sampleRequest.post();
        } catch (Exception e) {
            System.out.println(e);
        }
    }
}
```

### [Go](#tab/go)

```go

package main

import (
 "bytes"
 "fmt"
"net/http"
)

func main() {
basePath := "{your-document-translation-endpoint}/translator/document/batches"
key := "{your-api-key}"
uri := basePath + "?api-version={date}"
method := "POST"

var jsonStr = []byte(`{"inputs":[{"source":{"sourceUrl":"https://YOUR-SOURCE-URL-WITH-READ-LIST-ACCESS-SAS","storageSource":"AzureBlob","language":"en"},"targets":[{"targetUrl":"https://YOUR-TARGET-URL-WITH-WRITE-LIST-ACCESS-SAS","storageSource":"AzureBlob","category":"general","language":"es"}]}]}`)

req, err := http.NewRequest(method, uri, bytes.NewBuffer(jsonStr))
req.Header.Add("Ocp-Apim-Subscription-Key", key)
req.Header.Add("Content-Type", "application/json")

client := &http.Client{}

if err != nil {
    fmt.Println(err)
    return
  }
  res, err := client.Do(req)
  if err != nil {
    fmt.Println(err)
    return
  }
  defer res.Body.Close()
  fmt.Println("response status:",  res.Status)
  fmt.Println("response headers",  res.Header)
}
```

---

## Get supported document formats

Retrieve a list of supported file formats. If successful, this method returns a `200 OK` response code.

### [C#](#tab/csharp)

```csharp

using System;
using System.Net.Http;
using System.Threading.Tasks;


class Program
{


    private static readonly string basePath = "{your-document-translation-endpoint}/translator/document/formats";

    static readonly string route = "?api-version={date}&type=document";

    private static readonly string key = "{your-api-key}";

    static async Task Main(string[] args)
    {

        HttpClient client = new HttpClient();
            using HttpRequestMessage request = new HttpRequestMessage();
            {
                request.Method = HttpMethod.Get;
                request.RequestUri = new Uri(basePath + route);
                request.Headers.Add("Ocp-Apim-Subscription-Key", key);


                HttpResponseMessage response = await client.SendAsync(request);
                string result = response.Content.ReadAsStringAsync().Result;

                Console.WriteLine($"Status code: {response.StatusCode}");
                Console.WriteLine($"Response Headers: {response.Headers}");
                Console.WriteLine();
                Console.WriteLine(result);
            }
}
```

### [Node.js](#tab/javascript)

```javascript

const axios = require('axios');

let basePath = '{your-document-translation-endpoint}/translator/document/formats}';
let key = '{your-api-key}';
let route = '?api-version={date}&type=document';

let config = {
  method: 'get',
  url: basePath + route,
  headers: {
    'Ocp-Apim-Subscription-Key': key
  }
};

axios(config)
.then(function (response) {
  console.log(JSON.stringify(response.data));
})
.catch(function (error) {
  console.log(error);
});

```

### [Java](#tab/java)

```java
import java.io.*;
import java.net.*;
import java.util.*;
import com.squareup.okhttp.*;

public class GetFileFormats {

    String key = "{your-api-key}";
    String basePath = "{your-document-translation-endpoint}/translator/document/formats";
    String url = basePath + "?api-version={date}&type=document";
    OkHttpClient client = new OkHttpClient();

    public void get() throws IOException {
        Request request = new Request.Builder().url(
                url).method("GET", null).addHeader("Ocp-Apim-Subscription-Key", key).build();
        Response response = client.newCall(request).execute();
            System.out.println(response.body().string());
        }

    public static void main(String[] args) throws IOException {
        try{
            GetJobs jobs = new GetJobs();
            jobs.get();
        } catch (Exception e) {
            System.out.println(e);
        }
    }
}

```

### [Python](#tab/python)

```python

import http.client

host = '{your-document-translation-endpoint}/translator/document/formats'
parameters = '?api-version={date}&type=document'
key =  '{your-api-key}'
conn = http.client.HTTPSConnection(host)
payload = ''
headers = {
  'Ocp-Apim-Subscription-Key': key
}
conn.request("GET", parameters , payload, headers)
res = conn.getresponse()
data = res.read()
print(res.status)
print()
print(data.decode("utf-8"))
```

### [Go](#tab/go)

```go

package main

import (
  "fmt"
  "net/http"
  "io/ioutil"
)

func main() {

  basePath := "https://<NAME-OF-YOUR-RESOURCE>.cognitiveservices.azure.com/translator/text/batch/v1.1{your-document-translation-endpoint}/translator/document/formats"
  key := "{your-api-key}"
  uri := basePath + "?api-version={date}&type=document"
  method := "GET"

  client := &http.Client {
  }
  req, err := http.NewRequest(method, uri, nil)

  if err != nil {
    fmt.Println(err)
    return
  }
  req.Header.Add("Ocp-Apim-Subscription-Key", key)

  res, err := client.Do(req)
  if err != nil {
    fmt.Println(err)
    return
  }
  defer res.Body.Close()

  body, err := ioutil.ReadAll(res.Body)
  if err != nil {
    fmt.Println(err)
    return
  }
  fmt.Println(res.StatusCode)
  fmt.Println(string(body))
}
```

---

## Get status for a translation job

Get the current status for a single job and a summary of all jobs in a Document Translation request. If successful, this method returns a `200 OK` response code.
<!-- markdownlint-disable MD024 -->

### [C#](#tab/csharp)

```csharp

using System;
using System.Net.Http;
using System.Threading.Tasks;


class Program
{


    private static readonly string basePath = "{your-document-translation-endpoint}/translator/document/batches/{id}";

    static readonly string route = "?api-version={date}";

    private static readonly string key = "{your-api-key}";

    static async Task Main(string[] args)
    {

        HttpClient client = new HttpClient();
            using HttpRequestMessage request = new HttpRequestMessage();
            {
                request.Method = HttpMethod.Get;
                request.RequestUri = new Uri(basePath + route);
                request.Headers.Add("Ocp-Apim-Subscription-Key", key);


                HttpResponseMessage response = await client.SendAsync(request);
                string result = response.Content.ReadAsStringAsync().Result;

                Console.WriteLine($"Status code: {response.StatusCode}");
                Console.WriteLine($"Response Headers: {response.Headers}");
                Console.WriteLine();
                Console.WriteLine(result);
            }
    }
}
```

### [Node.js](#tab/javascript)

```javascript

const axios = require('axios');

let basePath = '{your-document-translation-endpoint}/translator/document/batches/{id}';
let key = '{your-api-key}';
let route = '?api-version={date}';

let config = {
  method: 'get',
  url: endpoint + route,
  headers: {
    'Ocp-Apim-Subscription-Key': key
  }
};

axios(config)
.then(function (response) {
  console.log(JSON.stringify(response.data));
})
.catch(function (error) {
  console.log(error);
});

```

### [Java](#tab/java)

```java

import java.io.*;
import java.net.*;
import java.util.*;
import com.squareup.okhttp.*;

public class GetJobStatus {

    String key = "{your-api-key}";
    String basePath = "{your-document-translation-endpoint}/translator/document/batches/{id}";
    String url = basePath + "?api-version={date}";
    OkHttpClient client = new OkHttpClient();

    public void get() throws IOException {
        Request request = new Request.Builder().url(
                url).method("GET", null).addHeader("Ocp-Apim-Subscription-Key", key).build();
        Response response = client.newCall(request).execute();
            System.out.println(response.body().string());
        }

    public static void main(String[] args) throws IOException {
        try{
            GetJobs jobs = new GetJobs();
            jobs.get();
        } catch (Exception e) {
            System.out.println(e);
        }
    }
}

```

### [Python](#tab/python)

```python

import http.client

host = '{your-document-translation-endpoint}/translator/document/batches/{id}'
parameters = '?api-version={date}'
key =  '{your-api-key}'
conn = http.client.HTTPSConnection(host)
payload = ''
headers = {
  'Ocp-Apim-Subscription-Key': key
}
conn.request("GET", parameters , payload, headers)
res = conn.getresponse()
data = res.read()
print(res.status)
print()
print(data.decode("utf-8"))
```

### [Go](#tab/go)

```go

package main

import (
  "fmt"
  "net/http"
  "io/ioutil"
)

func main() {

  basePath := "{your-document-translation-endpoint}/translator/document/batches/{id}"
  key := "{your-api-key}"
  uri := basePath + "?api-version={date}"
  method := "GET"

  client := &http.Client {
  }
  req, err := http.NewRequest(method, uri, nil)

  if err != nil {
    fmt.Println(err)
    return
  }
  req.Header.Add("Ocp-Apim-Subscription-Key", key)

  res, err := client.Do(req)
  if err != nil {
    fmt.Println(err)
    return
  }
  defer res.Body.Close()

  body, err := ioutil.ReadAll(res.Body)
  if err != nil {
    fmt.Println(err)
    return
  }
  fmt.Println(res.StatusCode)
  fmt.Println(string(body))
}
```

---

## Get status for a specific document

### Brief overview

Retrieve the status for a specific document in a Document Translation request. If successful, this method returns a `200 OK` response code.

### [C#](#tab/csharp)

```csharp

using System;
using System.Net.Http;
using System.Threading.Tasks;


class Program
{


    private static readonly string basePath = "{document-translation-endpoint}/translator/document/batches/{id}/documents/{documentId}";

    static readonly string route = "?api-version={date}";

    private static readonly string key = "{your-api-key}";

    static async Task Main(string[] args)
    {

        HttpClient client = new HttpClient();
            using HttpRequestMessage request = new HttpRequestMessage();
            {
                request.Method = HttpMethod.Get;
                request.RequestUri = new Uri(basePath + route);
                request.Headers.Add("Ocp-Apim-Subscription-Key", key);


                HttpResponseMessage response = await client.SendAsync(request);
                string result = response.Content.ReadAsStringAsync().Result;

                Console.WriteLine($"Status code: {response.StatusCode}");
                Console.WriteLine($"Response Headers: {response.Headers}");
                Console.WriteLine();
                Console.WriteLine(result);
            }
}
```

### [Node.js](#tab/javascript)

```javascript

const axios = require('axios');

let basePath = '{your-document-translation-endpoint}/translator/document/batches/{id}/documents/{documentId}';
let key = '{your-api-key}';
let route = '?api-version={date}';

let config = {
  method: 'get',
  url: basePath + route,
  headers: {
    'Ocp-Apim-Subscription-Key': key
  }
};

axios(config)
.then(function (response) {
  console.log(JSON.stringify(response.data));
})
.catch(function (error) {
  console.log(error);
});

```

### [Java](#tab/java)

```java

import java.io.*;
import java.net.*;
import java.util.*;
import com.squareup.okhttp.*;

public class GetDocumentStatus {

    String key = "{your-api-key}";
    String basePath = "{your-document-translation-endpoint}/translator/document/batches/{id}/documents/{documentId}";
    String url = endpoint + "?api-version={date}";
    OkHttpClient client = new OkHttpClient();

    public void get() throws IOException {
        Request request = new Request.Builder().url(
                url).method("GET", null).addHeader("Ocp-Apim-Subscription-Key", key).build();
        Response response = client.newCall(request).execute();
            System.out.println(response.body().string());
        }

    public static void main(String[] args) throws IOException {
        try{
            GetJobs jobs = new GetJobs();
            jobs.get();
        } catch (Exception e) {
            System.out.println(e);
        }
    }
}

```

### [Python](#tab/python)

```python

import http.client

host = '{your-document-translation-endpoint}/translator/document/batches/{id}/documents/{documentId}'
parameters = '?api-version={date}'
key =  '{your-api-key}'
conn = http.client.HTTPSConnection(host)
payload = ''
headers = {
  'Ocp-Apim-Subscription-Key': key
}
conn.request("GET", parameters , payload, headers)
res = conn.getresponse()
data = res.read()
print(res.status)
print()
print(data.decode("utf-8"))
```

### [Go](#tab/go)

```go

package main

import (
  "fmt"
  "net/http"
  "io/ioutil"
)

func main() {

  basePath := "{your-document-translation-endpoint}/translator/document/batches/{id}/documents/{documentId}"
  key := "{your-api-key}"
  uri := basePath + "?api-version={date}"
  method := "GET"

  client := &http.Client {
  }
  req, err := http.NewRequest(method, uri, nil)

  if err != nil {
    fmt.Println(err)
    return
  }
  req.Header.Add("Ocp-Apim-Subscription-Key", key)

  res, err := client.Do(req)
  if err != nil {
    fmt.Println(err)
    return
  }
  defer res.Body.Close()

  body, err := ioutil.ReadAll(res.Body)
  if err != nil {
    fmt.Println(err)
    return
  }
  fmt.Println(res.StatusCode)
  fmt.Println(string(body))
}
```

---

## Delete job

### Brief overview

Cancel currently processing or queued job. Only documents for which translation isn't started are canceled.

### [C#](#tab/csharp)

```csharp

using System;
using System.Net.Http;
using System.Threading.Tasks;


class Program
{


    private static readonly string basePath = "{your-document-translation-endpoint}/translator/document/batches/{id}";

    static readonly string route = "?api-version={date}";

    private static readonly string key = "{your-api-key}";

    static async Task Main(string[] args)
    {

        HttpClient client = new HttpClient();
            using HttpRequestMessage request = new HttpRequestMessage();
            {
                request.Method = HttpMethod.Delete;
                request.RequestUri = new Uri(basePath + route);
                request.Headers.Add("Ocp-Apim-Subscription-Key", key);


                HttpResponseMessage response = await client.SendAsync(request);
                string result = response.Content.ReadAsStringAsync().Result;

                Console.WriteLine($"Status code: {response.StatusCode}");
                Console.WriteLine($"Response Headers: {response.Headers}");
                Console.WriteLine();
                Console.WriteLine(result);
            }
}
```

### [Node.js](#tab/javascript)

```javascript

const axios = require('axios');

let basePath = '{your-document-translation-endpoint}/translator/document/batches/{id}';
let key = '{your-api-key}';
let route = '?api-version={date}';

let config = {
  method: 'delete',
  url: basePath + route,
  headers: {
    'Ocp-Apim-Subscription-Key': key
  }
};

axios(config)
.then(function (response) {
  console.log(JSON.stringify(response.data));
})
.catch(function (error) {
  console.log(error);
});

```

### [Java](#tab/java)

```java

import java.io.*;
import java.net.*;
import java.util.*;
import com.squareup.okhttp.*;

public class DeleteJob {

    String key = "{your-api-key}";
    String basePath = "{your-document-translation-endpoint}/translator/document/batches/{id}";
    String url = basePath + "?api-version={date}";
    OkHttpClient client = new OkHttpClient();

    public void get() throws IOException {
        Request request = new Request.Builder().url(
                url).method("DELETE", null).addHeader("Ocp-Apim-Subscription-Key", key).build();
        Response response = client.newCall(request).execute();
            System.out.println(response.body().string());
        }

    public static void main(String[] args) throws IOException {
        try{
            GetJobs jobs = new GetJobs();
            jobs.get();
        } catch (Exception e) {
            System.out.println(e);
        }
    }
}

```

### [Python](#tab/python)

```python

import http.client

host = '{your-document-translation-endpoint}/translator/document/batches/{id}'
parameters = '?api-version={date}'
key =  '{your-api-key}'
conn = http.client.HTTPSConnection(host)
payload = ''
headers = {
  'Ocp-Apim-Subscription-Key': key
}
conn.request("DELETE", parameters , payload, headers)
res = conn.getresponse()
data = res.read()
print(res.status)
print()
print(data.decode("utf-8"))
```

### [Go](#tab/go)

```go

package main

import (
  "fmt"
  "net/http"
  "io/ioutil"
)

func main() {

  basePath := "{your-document-translation-endpoint}/translator/document/batches/{id}"
  key := "{your-api-key}"
  uri := basePath + "?api-version={date}"
  method := "DELETE"

  client := &http.Client {
  }
  req, err := http.NewRequest(method, uri, nil)

  if err != nil {
    fmt.Println(err)
    return
  }
  req.Header.Add("Ocp-Apim-Subscription-Key", key)

  res, err := client.Do(req)
  if err != nil {
    fmt.Println(err)
    return
  }
  defer res.Body.Close()

  body, err := ioutil.ReadAll(res.Body)
  if err != nil {
    fmt.Println(err)
    return
  }
  fmt.Println(res.StatusCode)
  fmt.Println(string(body))
}
```

---

### Common HTTP status codes

| HTTP status code | Description | Possible reason |
|------------------|-------------|-----------------|
| 200 | OK | The request was successful. |
| 400 | Bad Request | A required parameter is missing, empty, or null. Or, the value passed to either a required or optional parameter is invalid. A common issue is a header that is too long. |
| 401 | Unauthorized | The request isn't authorized. Check to make sure your key or token is valid and in the correct region.
| 429 | Too Many Requests | You exceeded the quota or rate of requests allowed for your subscription. |
| 502 | Bad Gateway    | Network or server-side issue. Can also indicate invalid headers. |

## Learn more

* [Translator v3 API reference](../../reference/v3-0-reference.md)
* [Language support](../../language-support.md)

## Next steps

> [!div class="nextstepaction"]
> [Create a customized language system using Custom Translator](../../custom-translator/overview.md)
