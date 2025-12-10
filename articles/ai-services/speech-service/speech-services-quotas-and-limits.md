---
title: Speech service quotas and limits
titleSuffix: Foundry Tools
description: Quick reference, detailed description, and best practices on the quotas and limits for the Speech service in Foundry Tools.
author: goergenj
ms.author: jagoerge
manager: nitinme
ms.service: azure-ai-speech
ms.topic: article
ms.date: 12/08/2025
ms.reviewer: jagoerge
#Customer intent: As a developer, I want to learn about the quotas and limits for the Speech service in Foundry Tools.
---

# Speech service quotas and limits

This article contains a quick reference and a detailed description of the quotas and limits for the Speech service in Foundry Tools. The information applies to all [pricing tiers](https://azure.microsoft.com/pricing/details/cognitive-services/speech-services/) of the service. It also contains some best practices to avoid request throttling.

For the free (F0) pricing tier, see also the monthly allowances at the [pricing page](https://azure.microsoft.com/pricing/details/cognitive-services/speech-services/).

## Quotas and limits reference

The following sections provide you with a quick guide to the quotas and limits that apply to the Speech service.

For information about adjustable quotas for Standard (S0) Speech resources, see [more explanations](#detailed-description-quota-adjustment-and-best-practices), [best practices](#general-best-practices-to-mitigate-throttling-during-autoscaling), and [adjustment instructions](#speech-to-text-increase-real-time-speech-to-text-concurrent-request-limit). The quotas and limits for Free (F0) Speech resources aren't adjustable. 

> [!IMPORTANT]
> If you switch a Foundry resource for Speech from Free (F0) to Standard (S0) pricing tier, the change of the corresponding quotas may take up to several hours.

### Voice live quotas and limits per resource

This section describes Voice live quotas and limits per Speech resource. For information about adjustable quotas, see [Detailed description, quota adjustment, and best practices](#detailed-description-quota-adjustment-and-best-practices).

| Quota | Free (F0) | Standard (S0) |
|-----|-----|-----|
| New connections per minute | N/A | 30  |
| Maximum connection length | N/A | <= 60 minutes per session |
| Tokens per minute | N/A | <= 120,000 |

Avatars used in Voice live follows the quota and limits described in [real-time text to speech avatar](#real-time-text-to-speech-avatar).

### LLM Speech (Preview) quotas and limits per resource

This section describes speech to text quotas and limits per Speech resource. At this time, these limits aren't adjustable.

| Quota | Free (F0) | Standard (S0) |
|-----|-----|-----|
| Maximum audio input file size | N/A | < 300 MB |
| Maximum audio length | N/A | < 120 minutes per file  |
| Maximum requests per minute | N/A | 600  |

### Speech to text quotas and limits per resource

This section describes speech to text quotas and limits per Speech resource. For information about adjustable quotas, see [Detailed description, quota adjustment, and best practices](#detailed-description-quota-adjustment-and-best-practices).

#### Real-time speech to text and speech translation

You can use real-time speech to text with the [Speech SDK](speech-sdk.md) or the [Speech to text REST API for short audio](rest-speech-to-text-short.md).

> [!IMPORTANT]
> These limits apply to concurrent real-time speech to text requests and speech translation requests combined. For example, if you have 60 concurrent speech to text requests and 40 concurrent speech translation requests, you reach the limit of 100 concurrent requests.

| Quota | Free (F0) | Standard (S0) |
|-----|-----|-----|
| Concurrent request limit - base model endpoint | 1 <br/><br/>This limit isn't adjustable. | 100 (default value)<br/><br/>The rate is adjustable for Standard (S0) resources. See [more explanations](#detailed-description-quota-adjustment-and-best-practices), [best practices](#general-best-practices-to-mitigate-throttling-during-autoscaling), and [adjustment instructions](#speech-to-text-increase-real-time-speech-to-text-concurrent-request-limit). |
| Concurrent request limit - custom endpoint | 1 <br/><br/>This limit isn't adjustable. | 100 (default value)<br/><br/>The rate is adjustable for Standard (S0) resources. See [more explanations](#detailed-description-quota-adjustment-and-best-practices), [best practices](#general-best-practices-to-mitigate-throttling-during-autoscaling), and [adjustment instructions](#speech-to-text-increase-real-time-speech-to-text-concurrent-request-limit). |
| Max audio length for [real-time diarization](./get-started-stt-diarization.md). | N/A | 240 minutes per file  |

#### Fast transcription

| Quota | Free (F0) | Standard (S0) |
|-----|-----|-----|
| Maximum audio input file size | N/A | < 300 MB |
| Maximum audio length | N/A | < 120 minutes per file  |
| Maximum requests per minute | N/A | 600  |

#### Batch transcription

| Quota | Free (F0) | Standard (S0) |
|-----|-----|-----|
| [Speech to text REST API](rest-speech-to-text.md) limit | Not available for F0 | 100 requests per 10 seconds (600 requests per minute) |
| Max audio input file size | N/A | 1 GB |
| Max number of blobs per container | N/A | 10000 |
| Max number of files per transcription request (when you're using multiple content URLs as input). | N/A | 1000  |
| Max audio length for transcriptions with diarization enabled. | N/A | 240 minutes per file  |

#### Model customization

The limits in this table apply per Speech resource when you create a custom speech model. 

| Quota | Free (F0) | Standard (S0) |
|-----|-----|-----|
| REST API limit | 100 requests per 10 seconds (600 requests per minute) | 100 requests per 10 seconds (600 requests per minute) |
| Max number of custom model deployments per Speech resource | 1 | 50 |
| Max number of speech datasets | 2 | 500 |
| Max acoustic dataset file size for data import | 2 GB | 2 GB |
| Max language dataset file size for data import | 200 MB | 1.5 GB |
| Max pronunciation dataset file size for data import | 1 KB | 1 MB |
| Max text size when you're using the `text` parameter in the [Models_Create](/rest/api/speechtotext/models/create) API request | 200 KB | 500 KB |

### Text to speech quotas and limits per resource

This section describes text to speech quotas and limits per Speech resource. For information about adjustable quotas, see [Detailed description, quota adjustment, and best practices](#detailed-description-quota-adjustment-and-best-practices).

#### Real-time text to speech

You can use real-time text to speech with the [Speech SDK](speech-sdk.md) or the [Text to speech REST API](rest-text-to-speech.md). Unless otherwise specified, the limits aren't adjustable.

| Quota | Free (F0) | Standard (S0) |
|-----|-----|-----|
| Maximum number of transactions per time period for standard voices and custom voices. | 20 transactions per 60 seconds<br/><br/>This limit isn't adjustable. | 200 transactions per second (TPS) (default value)<br/><br/>The rate is adjustable up to 1000 TPS for Standard (S0) resources. See [more explanations](#detailed-description-quota-adjustment-and-best-practices), [best practices](#general-best-practices-to-mitigate-throttling-during-autoscaling), and [adjustment instructions](#text-to-speech-increase-real-time-tps-limit). |
| Max audio length produced per request | 10 min | 10 min |
| Max total number of distinct `<voice>` and `<audio>` tags in SSML | 50 | 50 |
| Max SSML message size per turn for websocket | 64 KB | 64 KB |

> [!NOTE]
> Most HTTP 429 errors with Text-to-Speech Standard Voice are caused by limited backend service capacity for a specific voice in the selected region, not by quota limits. Increasing your quota won't resolve these errors. For best results, use the voice in its native region or select a more popular voice in your current region.

#### Batch synthesis

These limits aren't adjustable. For more information on batch synthesis latency, see [the batch synthesis latency and best practices](batch-synthesis.md#batch-synthesis-latency-and-best-practices).

| Quota | Free (F0) | Standard (S0) |
|-----|-----|-----|
|REST API limit | Not available for F0 | 100 requests per 10 seconds |
| Max JSON payload size to create a synthesis job  | N/A | 2 megabytes |
| Concurrent active synthesis jobs | N/A | No limit |
| Max number of text inputs per synthesis job | N/A | 10000 |
|Max time to live for a synthesis job since it being in the final state  | N/A | Up to 31 days (specified using properties) |

#### Custom voice - professional

The limits in this table apply per Speech resource when you create a professional voice.

| Quota | Free (F0)| Standard (S0) |
|-----|-----|-----|
| Max number of transactions per second (TPS) | Not available for F0 | 200 transactions per second (TPS) (default value) |
| Max number of datasets | N/A | 500 |
| Max number of simultaneous dataset uploads | N/A | 5 |
| Max data file size for data import per dataset | N/A | 2 GB |
| Upload of long audio or audio without script | N/A | Yes |
| Max number of simultaneous model trainings | N/A | 4 |
| Max number of custom endpoints | N/A | 50 |

#### Custom voice - personal voice

The limits in this table apply per Speech resource when you create a personal voice.

| Quota | Free (F0)| Standard (S0) |
|-----|-----|-----|
| REST API limit (not including speech synthesis) | Not available for F0 | 50 requests per 10 seconds |
| Max number of transactions per second (TPS) for speech synthesis|Not available for F0  |200 transactions per second (TPS) (default value)  |

#### Batch text to speech avatar 

| Quota | Free (F0)| Standard (S0) |
|-----|-----|-----|
| REST API limit  | Not available for F0 | 2 requests per 1 minute  |

#### Real-time text to speech avatar

| Quota | Free (F0)| Standard (S0) |
|-----|-----|-----|
| New connections per minute | Not available for F0 | 2 new connections per minute |
| Max connection duration with speaking | Not available for F0 | 30 minutes<sup>1</sup> |
| Max connection duration with idle state | Not available for F0 | 5 minutes |

<sup>1</sup> To ensure continuous operation of the real-time avatar for more than 30 minutes, you can enable auto-reconnect. For information about how to set up auto-reconnect, refer to this [sample code](https://github.com/Azure-Samples/cognitive-services-speech-sdk/blob/master/samples/js/browser/avatar/README.md) (search "auto reconnect").

#### Audio Content Creation tool

| Quota | Free (F0)| Standard (S0) |
|-----|-----|-----|
| File size (plain text in SSML)<sup>1</sup>  | 3,000 characters per file | 20,000 characters per file |
| File size (lexicon file)<sup>2</sup> | 30 KB per file | 100 KB per file|
| Billable characters in SSML| 15,000 characters per file | 100,000 characters per file |
| Export to audio library | 1 concurrent task | N/A |

<sup>1</sup> The limit only applies to plain text in SSML and doesn't include tags.

<sup>2</sup> The characters of lexicon file aren't charged. Only the lexicon elements in SSML are counted as billable characters. Refer to [billable characters](text-to-speech.md#billable-characters) to learn more.


## Detailed description, quota adjustment, and best practices

Some Speech service quotas are adjustable. This section provides more explanations, best practices, and adjustment instructions. 

The following quotas are adjustable for Standard (S0) resources. The Free (F0) request limits aren't adjustable.

- Voice live API [new connections per minute](#voice-live-quotas-and-limits-per-resource). Adjusting new connections will also adjusts the token limit.
- Speech to text [concurrent request limit](#real-time-speech-to-text-and-speech-translation) for base model endpoint and custom endpoint
- Fast Transcription [maximum number of requests per minute](#fast-transcription)
- Speech translation [concurrent request limit](#real-time-speech-to-text-and-speech-translation)
- Text to speech [maximum number of transactions per time period](#text-to-speech-quotas-and-limits-per-resource) for standard voices and custom voices
- Batch text to speech avatar [maximum requests per minute](#batch-text-to-speech-avatar)
- Real-time text to speech avatar [new connections per minute](#real-time-text-to-speech-avatar)

Before requesting a quota increase (where applicable), check your current TPS (transactions per second) or TPM (tokens per minute) and ensure that you need to increase the quota.

> [!NOTE]
> Batch transcription and Batch synthesis are asynchronous processes, and jobs are processed one-by-one in a queue. So, increasing the quota won't improve transcription performance. For performance improvements, see [Batch transcription best practices](./batch-transcription.md#best-practices-for-improving-performance) or [Batch synthesis latency and best practices](./batch-synthesis.md#batch-synthesis-latency-and-best-practices).

Speech service uses autoscaling technologies to bring the required computational resources in on-demand mode. At the same time, Speech service tries to keep your costs low by not maintaining an excessive amount of hardware capacity.

Let's look at an example. Suppose that your application receives response code 429, which indicates that there are too many requests. Your application receives this response even though your workload is within the limits defined by the [Quotas and limits reference](#quotas-and-limits-reference). The most likely explanation is that Speech service is scaling up to your demand and didn't reach the required scale yet. Therefore the service doesn't immediately have enough resources to serve the request. In such cases, increasing the quota won’t help. In most cases, the Speech service will scale up soon, and the issue causing response code 429 will be resolved.

> [!NOTE]
> As a best practice every implementation should gracefully handle 429 errors with retry logic to ensure best performance and to handle autoscaling. Please consider this before requesting additional quota. See general best practices for additional details.

### General best practices to mitigate throttling during autoscaling

To minimize issues related to throttling, it's a good idea to use the following techniques:

- Implement retry logic in your application to handle 429 errors.
- Avoid sharp changes in the workload. Increase the workload gradually. For example, let's say your application is using text to speech, and your current workload is 5 TPS. The next second, you increase the load to 20 TPS (that is, four times more). Speech service immediately starts scaling up to fulfill the new load, but is unable to scale as needed within one second. Some of the requests get response code 429 (too many requests).
- Test different load increase patterns. For more information, see the [workload pattern example](#example-of-a-workload-pattern-best-practice).
- Create more Speech service resources in *different* regions, and distribute the workload among them. (Creating multiple Speech service resources in the same region won't affect the performance, because all resources are served by the same backend cluster).

The next sections describe specific cases of adjusting quotas.

### Example of a workload pattern best practice

Here's a general example of a good approach to take. It's meant only as a template that you can adjust as necessary for your own use.

Suppose that a Speech service resource has the concurrent request limit set to 300. Start the workload from 20 concurrent connections, and increase the load by 20 concurrent connections every 90-120 seconds. Control the service responses, and implement the logic that falls back (reduces the load) if you get too many requests (response code 429). Then, retry the load increase in one minute, and if it still doesn't work, try again in two minutes. Use a pattern of 1-2-4-4 minutes for the intervals.

Generally, it's a good idea to test the workload and the workload patterns before going to production.

### Voice live: increase real-time speech to text concurrent request limit

#### Prepare the required information

Instructions on how to get the general resource information required is described in [create and submit a quota increase request](#create-and-submit-a-quota-increase-request).

> [!NOTE]
> The token per minute (TPM) limit is dependent on the new connections per minute (NCPM) limit. It will always be automatically increased with an increase of the new connections per minute.
> The formula is: TPM = NCPM * 4000 tokens. Example: 30 NCPM * 4000 tokens = 120,000 TPM.

#### Create the quota increase request

Follow the steps described in [create and submit a quota increase request](#create-and-submit-a-quota-increase-request) with the information collected to create the request.

### Speech to text: increase real-time speech to text concurrent request limit

By default, the number of concurrent real-time speech to text and speech translation [requests combined](#real-time-speech-to-text-and-speech-translation) is limited to 100 per resource in the base model, and 100 per custom endpoint in the custom model. For the standard pricing tier, you can increase this amount. Before submitting the request, ensure that you're familiar with the material discussed earlier in this article, such as the best practices to mitigate throttling.

> [!NOTE]
> Concurrent request limits for base and custom models need to be adjusted separately. You can have a Speech service resource that's associated with many custom endpoints hosting many custom model deployments. As needed, the limit adjustments per custom endpoint must be requested separately. 

Increasing the limit of concurrent requests doesn't directly affect your costs. The Speech service uses a payment model that requires that you pay only for what you use. The limit defines how high the service can scale before it starts throttle your requests.

You aren't able to see the existing value of the concurrent request limit parameter in the Azure portal, the command-line tools, or API requests. To verify the existing value, create an Azure support request.

> [!NOTE]
>[Speech containers](speech-container-howto.md) don't require increases of the concurrent request limit, because containers are constrained only by the CPUs of the hardware they're hosted on. Speech containers do, however, have their own capacity limitations that should be taken into account. For more information, see the [Speech containers FAQ](./speech-container-howto.md).

#### Prepare the required information

Instructions on how to get the general resource information required is described in [create and submit a quota increase request](#create-and-submit-a-quota-increase-request).

To create an increase request for custom speech, you need to provide the following additional information: 

- **Custom endpoint ID**

How to get information for the custom speech endpoint:

1. Go to the [Speech Studio](https://aka.ms/speechstudio/customspeech) portal.
1. Sign in if necessary, and go to **Custom speech**.
1. Select your project, and go to **Deployment**.
1. Select the required endpoint.
1. Copy and save the values of the following fields:
   - **Endpoint ID**

#### Create the quota increase request

Follow the steps described in [create and submit a quota increase request](#create-and-submit-a-quota-increase-request) with the information collected to create the request.

### Fast transcription: increase maximum requests per minute limit

#### Prepare the required information

Instructions on how to get the general resource information required is described in [create and submit a quota increase request](#create-and-submit-a-quota-increase-request).

To create an increase request for fast transcription, you need to provide the following additional information: 

- **Average Audio Length per API request**

The average audio length of each request sent to the API. Example: `5 minutes/request`. Provide an estimate based on the workload you're aiming to process.

#### Create the quota increase request

Follow the steps described in [create and submit a quota increase request](#create-and-submit-a-quota-increase-request) with the information collected to create the request.

### Text to speech: increase real-time TPS limit

For the standard pricing tier, you can increase this amount. Before submitting the request, ensure that you're familiar with the material discussed earlier in this article, such as the best practices to mitigate throttling.

#### Estimating Your Needs

- **Usage Under $10,000/month**: Typically, 32 TPS is sufficient, assuming your peak usage is within 10x of your average.
- **Default Limit**: 200 TPS is available by default, which exceeds most use cases.
 
**Example: Call Center Scenario**  
If you're building a call center with 1,000 concurrent calls:
- Assume agents speak half the time.
- Average TTS response length is 5 seconds.

**Required TPS**: 1000 calls / (2×5 seconds) = 100 TPS
 
**Information Required for TPS Increase Request**  
Please provide the following details:
- **Peak TPS**:
- **Average TPS**:
- **Average TTS Request Length (in characters)**:

With this data, you can estimate your monthly TTS usage with formula below:   
Monthly Usage=Average TPS×Request Length×3600×24×30  
Multiply the result with unit price $15 per million characters to estimate the monthly cost.

> [!NOTE]
> If your estimated usage significantly exceeds your budget, you may be overestimating your needs.
 
**Cost Considerations**  
Increasing the concurrent request limit does **not** directly affect your costs. You only pay for what you use. The limit simply defines how much the service can scale before throttling begins.

You aren't able to see the existing value of the concurrent request limit parameter in the Azure portal, the command-line tools, or API requests. To verify the existing value, create an Azure support request.

> [!NOTE]
>[Speech containers](speech-container-howto.md) don't require increases of the concurrent request limit, because containers are constrained only by the CPUs of the hardware they're hosted on.
 
#### Prepare the required information

Instructions on how to get the general resource information required is described in [create and submit a quota increase request](#create-and-submit-a-quota-increase-request).

To create an increase request for standard voice, you need to provide the following additional information:

- **Voice names you are requesting the increase for**

You can find a list of all voice names here: [Text to speech languages](./language-support.md?tabs=tts)

To create an increase request for custom voice, you need to provide the following additional information: 

- **Custom endpoint ID**

How to get information for the custom voice:

1. Go to the [Speech Studio](https://aka.ms/speechstudio/customvoice) portal.
1. Sign in if necessary, and go to **Custom voice**.
1. Select your project, and go to **Deploy model**.
1. Select the required endpoint.
1. Copy and save the values of the following fields:
   - **Endpoint ID**

#### Create the quota increase request

Follow the steps described in [create and submit a quota increase request](#create-and-submit-a-quota-increase-request) with the information collected to create the request.
   
### Text to speech avatar: increase new connections limit

#### Prepare the required information

Instructions on how to get the general resource information required is described in [create and submit a quota increase request](#create-and-submit-a-quota-increase-request).

To create an increase request for custom voice, you need to provide the following additional information: 

- **Standard avatar or custom avatar**

#### Create the quota increase request

Follow the steps described in [create and submit a quota increase request](#create-and-submit-a-quota-increase-request) with the information collected to create the request.

### Create and submit a quota increase request

To get the resource information needed for the quota increase request follow these steps:

1. Go to the [Azure portal](https://portal.azure.com/).
1. Select the resource for which you would like to increase the concurrency request limit.
1. From the **Resource Management** group, select **Properties**.
1. Copy and save the values of the following fields:
   - **Subscription ID**
   - **Resource ID**
   - **Location** (your endpoint region)

Initiate the increase of the limit for concurrent requests for your resource, or if necessary check the current limit, by submitting a support request. Here's how:

1. Ensure you have the required information listed in the previous sections.
1. Go to the [Foundry Tools Quota Increase Request](https://aka.ms/foundry-tools-quota-increase) form.
1. Provide the requestor details
    1. First Name
    1. Last Name
    1. Your Work/Organization Email Address
    > [!NOTE]
    > Applications submitted with a personal email address (for example, hotmail.com, outlook.com, gmail.com, etc.) won't be accepted.
    1. CompanyCompany/Organization Name
    > [!NOTE]
    > Note you can only request quota increases on behalf of your own organization!
1. Provide the resource information
    1. Azure Subscription ID
    1. Azure AI Service Resource ID
    1. Azure AI Service Resource Region
1. Provide the quota increase requested
    1. New Quota Limit requested (limit value you're requesting as integer only, for example, 300, 500, 1000, etc.)
    1. Justification (business justification for the limit increase)
1. Select the Foundry Tools service **Azure Speech** and click `Next`
1. On the next page, select the **Azure Speech** feature you're requesting the increase for. Options are:
    - Speech to text concurrent request limit base model endpoint
    - Speech to text concurrent request limit custom endpoint
    - Fast transcription maximum requests per minute
    - Text to speech maximum number of transactions per time period standard voices
    - Text to speech maximum number of transactions per time period custom voices
    - Speech translation concurrent request limit
    - Batch text to speech avatar maximum requests per minute
    - Real-time text to speech avatar new connections per minute
    - Voice Live API tokens per minute
1. Add the additional feature specific information requested in the form and click `Next`
1. On the final page, provide additional contact information of your account or partner contact name and e-mail address
1. Check the two confirmation questions and click `Submit`
1. Note the support request number in Azure portal notifications. You're contacted shortly about your request.

You'll receive a confirmation e-mail including your application ID. Check your spam folder in case you didn't receive the confirmation e-mail and ensure you're able to receive follow-up communication on your case.
