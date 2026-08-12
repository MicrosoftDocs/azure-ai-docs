---
manager: mcleans
ms.service: microsoft-foundry
ms.subservice: foundry-model-inference
ms.topic: include
ms.date: 07/31/2026
ms.author: fasantia
author: santiagxf
ai-usage: ai-assisted
---

# [Python](#tab/python)

Install the `openai` package by using pip:

```bash
pip install openai --upgrade
```

Create a client that points to the Azure OpenAI v1 endpoint, and then generate a response. The `/openai/v1/` route uses implicit versioning, so you don't pass an `api-version`. Pass your deployment name in the `model` field:

```python
import os
from openai import OpenAI

client = OpenAI(
    base_url="https://<resource>.openai.azure.com/openai/v1/",
    api_key=os.environ["AZURE_INFERENCE_CREDENTIAL"],
)

response = client.responses.create(
    model="deepseek-v3-0324",  # Replace with your model deployment name.
    input="Explain the Riemann hypothesis in one paragraph.",
)

print(response.output_text)
```

# [JavaScript](#tab/javascript)

Install the `openai` package by using npm:

```bash
npm install openai
```

Create a client that points to the Azure OpenAI v1 endpoint, and then generate a response:

```javascript
import OpenAI from "openai";

const client = new OpenAI({
    baseURL: "https://<resource>.openai.azure.com/openai/v1/",
    apiKey: process.env.AZURE_INFERENCE_CREDENTIAL,
});

const response = await client.responses.create({
    model: "deepseek-v3-0324", // Replace with your model deployment name.
    input: "Explain the Riemann hypothesis in one paragraph.",
});

console.log(response.output_text);
```

# [C#](#tab/csharp)

Install the OpenAI library:

```dotnetcli
dotnet add package OpenAI
```

Create a client that points to the Azure OpenAI v1 endpoint, and then generate a response:

```csharp
using System.ClientModel;
using OpenAI;
using OpenAI.Responses;

OpenAIClient client = new(
    new ApiKeyCredential(Environment.GetEnvironmentVariable("AZURE_INFERENCE_CREDENTIAL")),
    new OpenAIClientOptions
    {
        Endpoint = new Uri("https://<resource>.openai.azure.com/openai/v1/")
    });

OpenAIResponseClient responseClient = client.GetResponsesClient("deepseek-v3-0324");

OpenAIResponse response = responseClient.CreateResponse(
    "Explain the Riemann hypothesis in one paragraph.");

Console.WriteLine(response.GetOutputText());
```

# [Java](#tab/java)

Add the OpenAI Java SDK to your project. Check the [OpenAI Java repository](https://github.com/openai/openai-java) for the latest version.

Create a client that points to the Azure OpenAI v1 endpoint, and then generate a response:

```java
import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.models.responses.Response;
import com.openai.models.responses.ResponseCreateParams;

OpenAIClient client = OpenAIOkHttpClient.builder()
    .baseUrl("https://<resource>.openai.azure.com/openai/v1/")
    .apiKey(System.getenv("AZURE_INFERENCE_CREDENTIAL"))
    .build();

Response response = client.responses().create(
    ResponseCreateParams.builder()
        .model("deepseek-v3-0324") // Replace with your model deployment name.
        .input("Explain the Riemann hypothesis in one paragraph.")
        .build());

// The Responses API has no single output-text accessor; concatenate the output items.
response.output().stream()
    .flatMap(item -> item.message().stream())
    .flatMap(message -> message.content().stream())
    .flatMap(content -> content.outputText().stream())
    .forEach(outputText -> System.out.println(outputText.text()));
```

# [REST](#tab/rest)

Send requests directly to the v1 route. The `/openai/v1/` path uses implicit versioning, so you don't include an `api-version` query parameter. Pass your key in the `Authorization` header as a bearer token:

```bash
curl -X POST https://<resource>.openai.azure.com/openai/v1/responses \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AZURE_INFERENCE_CREDENTIAL" \
  -d '{
      "model": "deepseek-v3-0324",
      "input": "Explain the Riemann hypothesis in one paragraph."
    }'
```

---
