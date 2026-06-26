---
title: "Migration guide from Azure Content Moderator to Azure AI Content Safety"
description: "Migrate from Azure Content Moderator to Azure AI Content Safety. Step-by-step guide covering text, image, and custom-terms migration with code examples."
manager: nitinme
ms.service: azure-ai-content-safety
ms.topic: how-to
ms.date: 06/04/2026
author: ssalgadodev
ms.author: ssalgado
recommendations: false
ms.custom: references_regions, azure-ai-guardrails
ai-usage: ai-assisted
# customer intent: As a developer using Azure Content Moderator, I want to migrate to Azure AI Content Safety so that I can continue content moderation after the retirement date.
---

# Migration guide from Azure Content Moderator to Azure AI Content Safety

> [!IMPORTANT]
> Azure Content Moderator is retiring soon. To avoid service disruptions, migrate your workloads to Azure AI Content Safety as soon as possible.

Azure AI Content Safety is the next-generation replacement for Azure Content Moderator. It offers advanced AI-powered detection, multiseverity scoring, and new capabilities such as prompt shielding and groundedness detection. This guide walks you through the migration process step by step.

## Migration benefits

The following table compares Azure Content Moderator and Azure AI Content Safety across key capabilities:

| Capability | Azure Content Moderator (retiring) | Azure AI Content Safety |
|---|---|---|
| Text moderation | Binary flagging (offensive/not) | Multiseverity levels (0–6) across four harm categories [(Hate, Sexual, Self-harm, Violence)](/azure/foundry/openai/concepts/content-filter-severity-levels#harm-category-descriptions) |
| Image moderation | Adult/racy detection, OCR, face detection | Multiseverity levels across four harm categories [(Hate, Sexual, Self-harm, Violence)](/azure/foundry/openai/concepts/content-filter-severity-levels#harm-category-descriptions) |
| Custom terms | Custom term lists (max five lists, 10K terms each) | Blocklists (max 10K terms per list, regex support) |
| Custom image lists | Custom image lists | [Custom categories (rapid) API](/azure/ai-services/content-safety/how-to/custom-categories-rapid) |
| Video moderation | Time-marker-based scanning | Not directly available (use frame extraction + image API) |
| PII detection | Basic PII detection in text | Use Azure AI Language PII detection |
| AI safety features | ❌ Not available | ✅ Prompt Shields, Groundedness detection, Protected material detection |
| Severity scoring | Binary | Multilevel (0, 2, 4, 6) |
| Languages | Limited | Optimized for nine languages; functional in many more |

## Prerequisites

- An Azure subscription. 
- An Azure AI Content Safety resource. [Create one](../../ai-services/content-safety/overview.md) in a supported region.
- Azure CLI or Azure portal access for resource provisioning.
- Updated SDKs. Install the latest Azure AI Content Safety SDK for your language.

### Supported regions

Azure AI Content Safety is available in multiple regions. For the most current availability, see [Region availability](../../ai-services/content-safety/overview.md).

Key regions include: East US, East US 2, West US, West Europe, Sweden Central, Japan East, Australia East, and more.

> [!NOTE]
> Government cloud (Fairfax) regions support text and image moderation.

## Step 1: Create an Azure AI Content Safety resource

# [Azure portal](#tab/portal)

1. Go to the [Azure portal](https://portal.azure.com).
1. Select **Create a resource** and search for **Content Safety**.
1. Select **Azure AI Content Safety** > **Create**.
1. Enter your subscription, resource group, region, and pricing tier (**F0** for free tier, **S0** for production).
1. Select **Review + Create** > **Create**.

# [Azure CLI](#tab/cli)

```azurecli
az cognitiveservices account create \
    --name <your-content-safety-resource> \
    --resource-group <your-resource-group> \
    --kind ContentSafety \
    --sku S0 \
    --location <region> \
    --yes
```

---

### Retrieve your credentials

```azurecli
# Get endpoint
az cognitiveservices account show \
    --name <your-content-safety-resource> \
    --resource-group <your-resource-group> \
    --query "properties.endpoint" --output tsv

# Get key
az cognitiveservices account keys list \
    --name <your-content-safety-resource> \
    --resource-group <your-resource-group> \
    --query "key1" --output tsv
```

## Step 2: Install the Content Safety SDK

# [Python](#tab/python)

```bash
pip install azure-ai-contentsafety
```

# [C#](#tab/csharp)

```dotnetcli
dotnet add package Azure.AI.ContentSafety
```

# [Java](#tab/java)

```xml
<dependency>
    <groupId>com.azure</groupId>
    <artifactId>azure-ai-contentsafety</artifactId>
    <version>1.0.0</version>
</dependency>
```

# [JavaScript/TypeScript](#tab/javascript)

```bash
npm install @azure-rest/ai-content-safety
```

---

## Step 3: Migrate your API calls

### Text moderation

#### Before (Content Moderator)

```python
from azure.cognitiveservices.vision.contentmoderator import ContentModeratorClient
from msrest.authentication import CognitiveServicesCredentials

client = ContentModeratorClient(
    endpoint="<your-content-moderator-endpoint>",
    credentials=CognitiveServicesCredentials("<your-key>")
)

# Screen text
result = client.text_moderation.screen_text(
    text_content_type="text/plain",
    text_content="<your text content>",
    language="eng",
    autocorrect=False,
    pii=True,
    classify=True
)
# Result: Classification, PII, Terms matched
```

#### After (Content Safety)

```python
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions
from azure.core.credentials import AzureKeyCredential

client = ContentSafetyClient(
    endpoint="<your-content-safety-endpoint>",
    credential=AzureKeyCredential("<your-key>")
)

# Analyze text
request = AnalyzeTextOptions(text="<your text content>")
response = client.analyze_text(request)

# Result: Severity scores for each category
for category in response.categories_analysis:
    print(f"{category.category}: severity {category.severity}")
# Categories: Hate, SelfHarm, Sexual, Violence
# Severity levels: 0 (safe), 2 (low), 4 (medium), 6 (high)
```

#### Key differences for text moderation

| Content Moderator | Content Safety | Notes |
|---|---|---|
| `screen_text()` | `analyze_text()` | New method name |
| Binary classification | Severity levels 0, 2, 4, 6 | More granular results |
| Categories: Adult, Racy, Offensive | Categories: Hate, SelfHarm, Sexual, Violence | New category taxonomy |
| Built-in PII detection | Use [Azure AI Language PII API](/azure/ai-services/language-service/personally-identifiable-information/overview) separately | PII is a separate service |
| Max text: varies | Max text: 10K characters per request | Split longer texts as needed |

### Image moderation

#### Before (Content Moderator)

```python
result = client.image_moderation.evaluate_url_input(
    content_type="application/json",
    cache_image=True,
    data_representation="URL",
    value="<image-url>"
)
# Result: IsImageAdultClassified, IsImageRacyClassified,
# AdultClassificationScore
```

#### After (Content Safety)

```python
from azure.ai.contentsafety.models import AnalyzeImageOptions, ImageData

request = AnalyzeImageOptions(
    image=ImageData(blob_url="<image-url>")
)
response = client.analyze_image(request)

for category in response.categories_analysis:
    print(f"{category.category}: severity {category.severity}")
# Categories: Hate, SelfHarm, Sexual, Violence
```

#### Key differences for image moderation

| Content Moderator | Content Safety | Notes |
|---|---|---|
| `evaluate_url_input()` / `evaluate_file_input()` | `analyze_image()` | Unified method |
| Adult/Racy scores | Severity levels across four harm categories | Broader coverage |
| OCR capability | Not included | [Use Azure AI Vision OCR](/azure/ai-services/computer-vision/concept-ocr) |
| Face detection | Not included | [Use Azure AI Face API](/azure/ai-services/face/quickstarts-sdk/identity-client-library) |
| Max image size: 4 MB | Max image size: 4 MB | Same |
| Formats: JPEG, PNG, GIF, BMP | Formats: JPEG, PNG, GIF, BMP, TIFF, WEBP | More formats supported |

### Custom term lists to blocklists

#### Before (Content Moderator)

```python
# Create a term list
custom_list = client.list_management_term_lists.create(
    content_type="application/json",
    body={"name": "My List", "description": "Custom terms"}
)

# Add a term
client.list_management_term.add_term(
    list_id=custom_list.id,
    term="blocked_term",
    language="eng"
)

# Screen text against the list
result = client.text_moderation.screen_text(
    text_content_type="text/plain",
    text_content="some text with blocked_term",
    language="eng",
    list_id=custom_list.id
)
```

#### After (Content Safety)

Create a blocklist and add items by using the REST API:

```bash
# Create a blocklist
curl -X PUT \
  "<endpoint>/contentsafety/text/blocklists/<list-name>?api-version=2024-09-01" \
  -H "Ocp-Apim-Subscription-Key: <key>" \
  -H "Content-Type: application/json" \
  -d '{"description": "Custom terms"}'

# Add items to the blocklist
curl -X POST \
  "<endpoint>/contentsafety/text/blocklists/<list-name>:addOrUpdateBlocklistItems?api-version=2024-09-01" \
  -H "Ocp-Apim-Subscription-Key: <key>" \
  -H "Content-Type: application/json" \
  -d '{"blocklistItems": [{"description": "blocked term", "text": "blocked_term"}]}'
```

Analyze text by using the blocklist:

```python
request = AnalyzeTextOptions(
    text="some text with blocked_term",
    blocklist_names=["<list-name>"],
    halt_on_blocklist_hit=False
)
response = client.analyze_text(request)

# Check blocklist matches
if response.blocklists_match:
    for match in response.blocklists_match:
        print(
            f"Blocked: '{match.blocklist_item_text}' "
            f"from list '{match.blocklist_name}'"
        )
```

### Video moderation

Content Safety doesn't provide a direct video moderation API. For video content, use the following approach:

1. Extract frames from the video at regular intervals (for example, every 1–2 seconds).
1. Analyze each frame by using the Content Safety image API.
1. Analyze audio transcription by using the Content Safety text API.

```python
# Example: Analyze extracted video frames
for frame_path in extracted_frames:
    with open(frame_path, "rb") as f:
        request = AnalyzeImageOptions(
            image=ImageData(content=f.read())
        )
        response = client.analyze_image(request)
        # Process results per frame
```

### PII detection

[PII detection](/azure/ai-services/language-service/personally-identifiable-information/overview) is no longer part of the content moderation service. Migrate to Azure AI Language for PII detection:

```python
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

text_analytics_client = TextAnalyticsClient(
    endpoint="<language-endpoint>",
    credential=AzureKeyCredential("<language-key>")
)

documents = [
    "My phone number is 555-123-4567 and my email is user@example.com"
]
response = text_analytics_client.recognize_pii_entities(documents)

for doc in response:
    for entity in doc.entities:
        print(f"  {entity.text} ({entity.category})")
```

## Step 4: Update your decision logic

### Severity score mapping

Content Safety uses a four-level severity scale. Update your business logic to handle severity scores:

| Severity | Value | Meaning | Suggested action |
|---|---|---|---|
| Safe | 0 | No harmful content detected | Allow |
| Low | 2 | Minor potentially harmful content | Review or allow based on policy |
| Medium | 4 | Moderately harmful content | Flag for review or block |
| High | 6 | Severely harmful content | Block |

### Example decision logic

```python
def should_block(response, threshold=4):
    """Block content that meets or exceeds the severity threshold."""
    for category in response.categories_analysis:
        if category.severity >= threshold:
            return True, category.category
    return False, None

# Usage
response = client.analyze_text(
    AnalyzeTextOptions(text=user_input)
)
blocked, reason = should_block(response, threshold=4)
if blocked:
    print(f"Content blocked due to: {reason}")
```

## Step 5: Adopt new capabilities (optional)

Azure AI Content Safety includes powerful features not available in Content Moderator. Consider adopting these features as part of your migration.

### Prompt Shields (for AI/LLM applications)

Detects jailbreak attacks and [prompt injection attempts](/azure/foundry/openai/concepts/content-filter-prompt-shields#examples-1) in user inputs.

```python
import requests

endpoint = "<your-content-safety-endpoint>"
key = "<your-key>"

response = requests.post(
    f"{endpoint}contentsafety/text:shieldPrompt?api-version=2024-09-01",
    headers={
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json"
    },
    json={
        "userPrompt": "<user prompt>",
        "documents": []
    }
)
result = response.json()
print(f"Jailbreak detected: {result['userPromptAnalysis']['attackDetected']}")
```

#### Additional features

* [**Protected material detection**](/azure/foundry/openai/concepts/content-filter-protected-material?tabs=text): Scans AI-generated text for known copyrighted content.
* [**Groundedness detection (preview)**](/azure/foundry/openai/concepts/content-filter-groundedness): Verifies whether LLM responses are grounded in provided source materials.
* [**Custom categories (preview)**](/azure/ai-services/content-safety/concepts/custom-categories): Create your own content categories for domain-specific moderation needs.

## Step 6: Test and validate

1. **Parallel testing**: Run both Content Moderator and Content Safety side by side in a staging environment.
1. **Compare results**: Validate that Content Safety catches the same (or more) harmful content.
1. **Tune thresholds**: Adjust severity thresholds to match your business requirements.
1. **Validate blocklists**: Ensure all custom term lists are migrated and working correctly.
1. **Performance testing**: Verify latency and throughput meet your SLAs.
1. **Monitor with Content Safety Studio**: Use the Content Safety Studio monitoring dashboard to track moderation KPIs.

### Testing checklist

- Text moderation returns expected severity scores
- Image moderation returns expected severity scores
- Custom blocklists are migrated and matching correctly
- PII detection is handled via Azure AI Language (if applicable)
- Video moderation workflow with frame extraction is functional (if applicable)
- Error handling and retry logic are updated for new API
- Authentication (key-based or Microsoft Entra ID) is configured
- Throughput is within rate limits (S0: 1,000 requests per 10 seconds)

## Step 7: Switch production traffic

1. Deploy updated code with the Content Safety SDK to production.
1. Monitor the Content Safety Studio dashboard for the first 48–72 hours.
1. Decommission your Content Moderator resource once stable.

## API mapping quick reference

| Content Moderator API | Content Safety equivalent | Notes |
|---|---|---|
| `TextModeration.ScreenText` | `AnalyzeText` | [New severity-based response](/azure/ai-services/content-safety/quickstart-text) |
| `ImageModeration.EvaluateUrlInput` | `AnalyzeImage` | [New severity-based response](/azure/ai-services/content-safety/quickstart-image) |
| `ImageModeration.EvaluateFileInput` | [`AnalyzeImage` (with `ImageData.content`)](/azure/ai-services/content-safety/quickstart-image) | Pass base64 or bytes |
| `ImageModeration.FindFaces` | [Azure AI Face API](/azure/ai-services/computer-vision/identity-api-reference) | Separate service |
| `ImageModeration.OCR` | [Azure AI Vision OCR](/azure/ai-services/computer-vision/concept-ocr) | Separate service |
| `ListManagementTermLists` | [Blocklist management API](/azure/ai-services/content-safety/quickstart-blocklist) | REST-based management |
| `ListManagementTerm` | [Blocklist item management API](/azure/ai-services/content-safety/quickstart-blocklist) | Supports regex patterns |
| `ListManagementImageLists` | [Custom categories (rapid/standard)](/azure/ai-services/content-safety/concepts/custom-categories) | Preview feature |
| `TextModeration.ScreenText` (PII) | [Azure AI Language PII API](/azure/ai-services/language-service/personally-identifiable-information/how-to/redact-text-pii) | Separate service |
| `VideoModeration` | Frame extraction + Image/Text APIs | Manual pipeline |
| Review API (human review) | Content Safety Studio | Web-based monitoring |
| — | [Prompt Shields](/azure/ai-services/content-safety/concepts/jailbreak-detection) | New — jailbreak detection |
| — | [Groundedness Detection](/azure/ai-services/content-safety/concepts/groundedness) | New — LLM verification |
| — | [Protected Material Detection](/azure/ai-services/content-safety/concepts/protected-material) | New — copyright check |

## Pricing

| Tier | Text and image moderation | Rate limit |
|---|---|---|
| F0 (Free) | 5K free transactions/month | 5 RPS |
| S0 (Standard) | Pay-as-you-go | 1,000 requests per 10 seconds |

For full details, see [Azure AI Content Safety pricing](https://azure.microsoft.com/pricing/details/cognitive-services/content-safety/).

## Support and resources

- [Azure AI Content Safety documentation](../../ai-services/content-safety/overview.md)
- [Content Safety Studio](https://contentsafety.cognitive.azure.com)
- Quickstarts: [Text](../../ai-services/content-safety/quickstart-text.md) | [Image](../../ai-services/content-safety/quickstart-image.md)
- SDK reference: [Python](/python/api/overview/azure/ai-contentsafety-readme) | [.NET](/dotnet/api/overview/azure/ai.contentsafety-readme) | [Java](/java/api/overview/azure/ai-contentsafety-readme) | [JavaScript](/javascript/api/overview/azure/ai-content-safety-rest-readme)
- [Azure Content Moderator deprecation notice](../../ai-services/content-moderator/index.yml)

## Next steps

- [Configure guardrails and controls](/azure/foundry/guardrails/how-to-create-guardrails)
- [Learn about intervention points and controls](/azure/foundry/guardrails/intervention-points)
- [Understand content filtering in Azure OpenAI](../../foundry-classic/foundry-models/concepts/content-filter.md)
- [Configure content filters for Azure OpenAI](../../foundry-classic/openai/how-to/content-filters.md)
