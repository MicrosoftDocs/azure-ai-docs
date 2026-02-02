---
title: Quotas and Limits for Azure Speech
titleSuffix: Foundry Tools
description: This article provides a quick reference, a detailed description, and best practices for the quotas and limits in Azure Speech.
author: goergenj
ms.author: jagoerge
manager: nitinme
ms.service: azure-ai-speech
ms.topic: limits-and-quotas
ms.date: 01/30/2026
ms.reviewer: jagoerge
#Customer intent: As a developer, I want to learn about the quotas and limits for Azure Speech in Foundry Tools so that I can decide how to use the features in my application.
---

# Quotas and limits for Azure Speech

This article contains a quick reference and a detailed description of the quotas and limits for Azure Speech in Foundry Tools. The information applies to all [pricing tiers](https://azure.microsoft.com/pricing/details/speech/) of Azure Speech. This article also contains some best practices to avoid request throttling.

For the Free (F0) pricing tier, see the monthly allowances on the [pricing page](https://azure.microsoft.com/pricing/details/speech/).

## Reference for quotas and limits

The following sections provide a quick guide to the quotas and limits that apply to Azure Speech.

For information about adjustable quotas for Standard (S0) Azure Speech resources, see [more explanations](#detailed-description-quota-adjustment-and-best-practices), [best practices](#general-best-practices-to-mitigate-throttling-during-autoscaling), and [adjustment instructions](#speech-to-text-increase-the-real-time-speech-to-text-concurrent-request-limit) later in this article. The quotas and limits for Free (F0) Azure Speech resources aren't adjustable.

> [!IMPORTANT]
> If you switch a Foundry resource for Azure Speech from the Free (F0) pricing tier to Standard (S0), the change of the corresponding quotas might take up to several hours.

### Voice Live quotas and limits per resource

The following table summarizes the quotas and limits for Voice Live per Azure Speech resource. For information about adjustable quotas, see [more explanations](#detailed-description-quota-adjustment-and-best-practices) later in this article.

| Quota | Free (F0) | Standard (S0) |
| ----- | --------- | ------------- |
| New connections per minute | Not applicable | 30 |
| Maximum connection length | Not applicable | <= 60 minutes per session |
| Tokens per minute | Not applicable | <= 120,000 |

Avatars used in Voice Live follow the quotas and limits described in [Real-time text-to-speech avatar](#real-time-text-to-speech-avatar) later in this article.

### LLM speech (preview) quotas and limits per resource

The following table summarizes the quotas and limits for large language model (LLM) speech per Azure Speech resource. At this time, these limits aren't adjustable.

| Quota | Free (F0) | Standard (S0) |
| ----- | --------- | ------------- |
| Maximum audio input file size | Not applicable | < 300 MB |
| Maximum audio length | Not applicable | < 120 minutes per file |
| Maximum requests per minute | Not applicable | 600 |

### Speech-to-text quotas and limits per resource

The following sections describe speech-to-text quotas and limits per Azure Speech resource. For information about adjustable quotas, see [more explanations](#detailed-description-quota-adjustment-and-best-practices) in this article.

#### Real-time speech to text and speech translation

You can use real-time speech to text with the [Speech SDK](speech-sdk.md) or the [Speech-to-text REST API for short audio](rest-speech-to-text-short.md).

These limits apply to concurrent real-time speech-to-text requests and speech translation requests *combined*. For example, if you have 60 concurrent speech-to-text requests and 40 concurrent speech translation requests, you reach the limit of 100 concurrent requests.

| Quota | Free (F0) | Standard (S0) |
| ----- | --------- | ------------- |
| Concurrent request limit for base model endpoint | 1 <br/><br/>This limit isn't adjustable. | 100 (default value)<br/><br/>The rate is adjustable for Standard (S0) resources. See [more explanations](#detailed-description-quota-adjustment-and-best-practices), [best practices](#general-best-practices-to-mitigate-throttling-during-autoscaling), and [adjustment instructions](#speech-to-text-increase-the-real-time-speech-to-text-concurrent-request-limit) later in this article. |
| Concurrent request limit for custom endpoint | 1 <br/><br/>This limit isn't adjustable. | 100 (default value)<br/><br/>The rate is adjustable for Standard (S0) resources. See [more explanations](#detailed-description-quota-adjustment-and-best-practices), [best practices](#general-best-practices-to-mitigate-throttling-during-autoscaling), and [adjustment instructions](#speech-to-text-increase-the-real-time-speech-to-text-concurrent-request-limit) later in this article. |
| Maximum audio length for [real-time diarization](./get-started-stt-diarization.md) | Not applicable | 240 minutes per file |

#### Fast transcription

| Quota | Free (F0) | Standard (S0) |
| ----- | --------- | ------------- |
| Maximum audio input file size | Not applicable | < 300 MB |
| Maximum audio length | Not applicable | < 120 minutes per file |
| Maximum requests per minute | Not applicable | 600 |

#### Batch transcription

| Quota | Free (F0) | Standard (S0) |
| ----- | --------- | ------------- |
| [Speech-to-text REST API](rest-speech-to-text.md) limit | Not available for F0 | 100 requests per 10 seconds (600 requests per minute) |
| Maximum file size for audio input | Not applicable | 1 GB |
| Maximum number of blobs per container | Not applicable | 10,000 |
| Maximum number of files per transcription request (when you're using multiple content URLs as input) | Not applicable | 1,000 |
| Maximum audio length for transcriptions with diarization enabled | Not applicable | 240 minutes per file |

#### Model customization

The limits in this table apply per Azure Speech resource when you create a custom speech model.

| Quota | Free (F0) | Standard (S0) |
| ----- | --------- | ------------- |
| REST API limit | 100 requests per 10 seconds (600 requests per minute) | 100 requests per 10 seconds (600 requests per minute) |
| Maximum number of custom model deployments per Azure Speech resource | 1 | 50 |
| Maximum number of speech datasets | 2 | 500 |
| Maximum file size for the acoustic dataset for data import | 2 GB | 2 GB |
| Maximum file size for the language dataset for data import | 200 MB | 1.5 GB |
| Maximum file size for the pronunciation dataset for data import | 1 KB | 1 MB |
| Maximum text size when you're using the `text` parameter in the [Models_Create](/rest/api/speechtotext/models/create) API request | 200 KB | 500 KB |

### Text-to-speech quotas and limits per resource

The following sections describe text-to-speech quotas and limits per Azure Speech resource. For information about adjustable quotas, see [more explanations](#detailed-description-quota-adjustment-and-best-practices) later in this article.

#### Real-time text to speech

You can use real-time text to speech with the [Speech SDK](speech-sdk.md) or the [text-to-speech REST API](rest-text-to-speech.md). Unless otherwise specified, the limits aren't adjustable.

| Quota | Free (F0) | Standard (S0) |
| ----- | --------- | ------------- |
| Maximum number of transactions per time period for standard voices and custom voices | 20 transactions per 60 seconds<br/><br/>This limit isn't adjustable. | 200 transactions per second (TPS) (default value)<br/><br/>The rate is adjustable up to 1,000 TPS for Standard (S0) resources. See [more explanations](#detailed-description-quota-adjustment-and-best-practices), [best practices](#general-best-practices-to-mitigate-throttling-during-autoscaling), and [adjustment instructions](#text-to-speech-increase-the-real-time-tps-limit) later in this article. |
| Maximum audio length produced per request | 10 minutes | 10 minutes |
| Maximum total number of distinct `<voice>` and `<audio>` tags in SSML | 50 | 50 |
| Maximum SSML message size per turn for WebSocket | 64 KB | 64 KB |

> [!NOTE]
> Most HTTP 429 errors with text-to-speech standard voice are caused by limited backend service capacity for a specific voice in the selected region, not by quota limits. Increasing your quota doesn't resolve these errors. For best results, use the voice in its native region or select a more popular voice in your current region.

#### Batch synthesis

The following limits aren't adjustable. For more information on latency in batch synthesis, see [Batch synthesis latency and best practices](batch-synthesis.md#batch-synthesis-latency-and-best-practices).

| Quota | Free (F0) | Standard (S0) |
| ----- | --------- | ------------- |
| REST API limit | Not available for F0 | 100 requests per 10 seconds |
| Maximum JSON payload size to create a synthesis job | Not applicable | 2 MB |
| Concurrent active synthesis jobs | Not applicable | No limit |
| Maximum number of text inputs per synthesis job | Not applicable | 10,000 |
| Maximum time to live for a synthesis job since it entered the final state | Not applicable | Up to 31 days (specified through properties) |

#### <a name = "custom-voice---professional"></a>Custom professional voice

The limits in this table apply per Azure Speech resource when you create a professional voice.

| Quota | Free (F0) | Standard (S0) |
| ----- | --------- | ------------- |
| Maximum number of transactions per second | Not available for F0 | 200 TPS (default value) |
| Maximum number of datasets | Not applicable | 500 |
| Maximum number of simultaneous dataset uploads | Not applicable | 5 |
| Maximum data file size for data import per dataset | Not applicable | 2 GB |
| Upload of long audio or audio without script | Not applicable | Yes |
| Maximum number of simultaneous model trainings | Not applicable | 4 |
| Maximum number of custom endpoints | Not applicable | 50 |

#### Custom personal voice

The limits in this table apply per Azure Speech resource when you create a personal voice.

| Quota | Free (F0) | Standard (S0) |
| ----- | --------- | ------------- |
| REST API limit (not including speech synthesis) | Not available for F0 | 50 requests per 10 seconds |
| Maximum number of transactions per second for speech synthesis | Not available for F0 | 200 TPS (default value) |

#### Batch text-to-speech avatar

| Quota | Free (F0) | Standard (S0) |
| ----- | --------- | ------------- |
| REST API limit | Not available for F0 | 2 requests per minute |

#### Real-time text-to-speech avatar

| Quota | Free (F0) | Standard (S0) |
| ----- | --------- | ------------- |
| New connections per minute | Not available for F0 | 2 new connections per minute |
| Maximum connection duration with speaking | Not available for F0 | 30 minutes<sup>1</sup> |
| Maximum connection duration with idle state | Not available for F0 | 5 minutes |

<sup>1</sup> To ensure continuous operation of the real-time avatar for more than 30 minutes, you can enable auto-reconnect. For information about how to set up auto-reconnect, refer to [this sample code](https://github.com/Azure-Samples/cognitive-services-speech-sdk/blob/master/samples/js/browser/avatar/README.md). Search for **auto reconnect**.

#### Audio Content Creation tool

| Quota | Free (F0) | Standard (S0) |
| ----- | --------- | ------------- |
| File size (plain text in SSML)<sup>1</sup> | 3,000 characters per file | 20,000 characters per file |
| File size (lexicon file)<sup>2</sup> | 30 KB per file | 100 KB per file |
| Billable characters in SSML | 15,000 characters per file | 100,000 characters per file |
| Export to audio library | 1 concurrent task | Not applicable |

<sup>1</sup> The limit applies only to plain text in SSML and doesn't include tags.

<sup>2</sup> The characters of the lexicon file aren't charged. Only the lexicon elements in SSML are counted as billable characters. To learn more, refer to [Billable characters](text-to-speech.md#billable-characters).

## Detailed description, quota adjustment, and best practices

Some Azure Speech quotas are adjustable. This section provides more explanations, best practices, and adjustment instructions.

The following quotas are adjustable for Standard (S0) resources. The Free (F0) request limits aren't adjustable.

- **Voice Live API**: [New connections per minute](#voice-live-quotas-and-limits-per-resource). Adjusting new connections also adjusts the token limit.
- **Speech to text**: [Concurrent request limit](#real-time-speech-to-text-and-speech-translation) for the base model endpoint and custom endpoint.
- **Fast transcription**: [Maximum number of requests per minute](#fast-transcription).
- **Speech translation**: [Concurrent request limit](#real-time-speech-to-text-and-speech-translation).
- **Text to speech**: [Maximum number of transactions per time period](#text-to-speech-quotas-and-limits-per-resource) for standard voices and custom voices.
- **Batch text-to-speech avatar**: [Maximum requests per minute](#batch-text-to-speech-avatar).
- **Real-time text-to-speech avatar**: [New connections per minute](#real-time-text-to-speech-avatar).

Before you request a quota increase (where applicable), check your current transactions per second (TPS) or tokens per minute (TPM) and ensure that you need to increase the quota.

> [!NOTE]
> Batch transcription and batch synthesis are asynchronous processes. They process jobs one by one in a queue. So, increasing the quota doesn't improve transcription performance. For performance improvements, see [Best practices for improving performance](./batch-transcription.md#best-practices-for-improving-performance) or [Batch synthesis latency and best practices](./batch-synthesis.md#batch-synthesis-latency-and-best-practices).

Azure Speech uses autoscaling technologies to bring the required computational resources in on-demand mode. At the same time, Azure Speech tries to keep your costs low by not maintaining an excessive amount of hardware capacity.

Let's look at an example. Suppose that your application receives response code 429, which indicates that there are too many requests. Your application receives this response even though your workload is within the limits defined in the earlier [Reference for quotas and limits](#reference-for-quotas-and-limits) section. The most likely explanation is that Azure Speech is scaling up to your demand and didn't reach the required scale yet. So, Azure Speech doesn't immediately have enough resources to serve the request. In such cases, increasing the quota doesn't help. In most cases, Azure Speech will scale up soon and resolve the issue that's causing response code 429.

As a best practice, every implementation should gracefully handle 429 errors with retry logic to ensure best performance and to handle autoscaling. Consider implementing this best practice before you request additional quota, as described in the next section.

### General best practices to mitigate throttling during autoscaling

To minimize issues related to throttling, it's a good idea to use the following techniques:

- Implement retry logic in your application to handle 429 errors.

- Avoid sharp changes in the workload. Increase the workload gradually.

  For example, let's say your application is using text to speech, and your current workload is 5 TPS. The next second, you increase the load to 20 TPS (that is, four times more). Azure Speech immediately starts scaling up to fulfill the new load, but it can't scale as needed within one second. Some of the requests get response code 429 (too many requests).
- Test different patterns for load increases. For more information, see the [workload pattern example](#example-of-a-best-practice-for-workload-patterns) in this article.

- Create more Azure Speech resources in *different* regions, and distribute the workload among them. Creating multiple Azure Speech resources in the same region doesn't affect the performance, because the same backend cluster serves all resources.

Later sections describe specific cases of adjusting quotas.

### <a name = "example-of-a-workload-pattern-best-practice"></a>Example of a best practice for workload patterns

Here's a general example of a good approach to take. It's meant only as a template that you can adjust as necessary for your own use.

Suppose that an Azure Speech resource has the concurrent request limit set to 300. Start the workload from 20 concurrent connections, and increase the load by 20 concurrent connections every 90 to 120 seconds. Control the Azure Speech responses, and implement the logic that falls back (reduces the load) if you get too many requests (response code 429). Then, retry the load increase in one minute. If it still doesn't work, try again in two minutes. Use a pattern of 1-2-4-4 minutes for the intervals.

Generally, it's a good idea to test the workload and the workload patterns before you go to production.

### Voice Live: Increase the real-time speech-to-text concurrent request limit

#### Prepare the required information

For instructions on how to get the general resource information that you need, see [Create and submit a quota increase request](#create-and-submit-a-quota-increase-request) later in this article.

> [!NOTE]
> The token per minute (TPM) limit is dependent on the new connections per minute (NCPM) limit. It increases automatically when the NCPM limit increases.
>
> The formula is: TPM = NCPM * 4,000 tokens. For example: 30 NCPM * 4,000 tokens = 120,000 TPM.

#### Create the quota increase request

To create the request with the collected information, follow the steps in [Create and submit a quota increase request](#create-and-submit-a-quota-increase-request) later in this article.

### Speech to text: Increase the real-time speech-to-text concurrent request limit

By default, the number of concurrent real-time speech-to-text and speech translation [requests combined](#real-time-speech-to-text-and-speech-translation) is limited to:

- 100 per resource in the base model.
- 100 per custom endpoint in the custom model.

For the Standard pricing tier, you can increase this amount. Before you submit the request, ensure that you're familiar with the material discussed earlier in this article, such as the best practices to mitigate throttling.

Concurrent request limits for base and custom models need to be adjusted separately. An Azure Speech resource can be associated with many custom endpoints that host many custom model deployments. You must separately request any limit adjustments per custom endpoint.

Increasing the limit of concurrent requests doesn't directly affect your costs. Azure Speech uses a payment model that requires that you pay for only what you use. The limit defines how high Azure Speech can scale before it starts throttle your requests.

You can't see the existing value of the parameter for the concurrent request limit in the Azure portal, the command-line tools, or API requests. To verify the existing value, create an Azure support request.

> [!NOTE]
> [Azure Speech containers](speech-container-howto.md) don't require increases of the concurrent request limit, because containers are constrained only by the CPUs of the hardware that they're hosted on. But Azure Speech containers do have their own capacity limitations that you should take into account. For more information, see [Install and run Speech containers with Docker](./speech-container-howto.md).

#### Prepare the required information

For instructions on how to get the general resource information that you need, see [Create and submit a quota increase request](#create-and-submit-a-quota-increase-request) later in this article.

To create an increase request for custom speech, you also need to provide a *custom endpoint ID*. To get this information for the custom speech endpoint:

1. Go to the [Speech Studio](https://aka.ms/speechstudio/customspeech) portal.
1. Sign in if necessary, and then go to **Custom speech**.
1. Select your project, and then go to **Deployment**.
1. Select the required endpoint.
1. Copy and save the **Endpoint ID** value.

#### Create the quota increase request

To create the request with the collected information, follow the steps in [Create and submit a quota increase request](#create-and-submit-a-quota-increase-request) later in this article.

### Fast transcription: Increase maximum requests per minute

#### Prepare the required information

For instructions on how to get the general resource information that you need, see [Create and submit a quota increase request](#create-and-submit-a-quota-increase-request) later in this article.

To create an increase request for fast transcription, you also need to provide the *average audio length per API request*.

An example length is `5 minutes/request`. Provide an estimate based on the workload that you want to process.

#### Create the quota increase request

To create the request with the collected information, follow the steps in [Create and submit a quota increase request](#create-and-submit-a-quota-increase-request) later in this article.

### Text to speech: Increase the real-time TPS limit

For the Standard pricing tier, you can increase the real-time TPS limit. Before you submit the request, ensure that you're familiar with the material discussed earlier in this article, such as the best practices to mitigate throttling.

#### Estimate your needs

- **Usage Under $10,000/month**: Typically, 32 TPS is sufficient, assuming that your peak usage is within 10 times your average.
- **Default limit**: 200 TPS is available by default. This limit exceeds most use cases.

##### Example scenario

For example, assume that you're building a call center in which:

- The number of concurrent calls is 1,000.
- You expect agents to speak half the time.
- Average TTS response length is 5 seconds.

The required TPS is: 1,000 calls / (2×5 seconds) = 100 TPS.

A TPS increase request requires the following details:

- Peak TPS
- Average TPS
- Average TTS request length (in characters)

With this data, you can estimate your monthly TTS usage by using this formula: monthly usage = average TPS × request length × 3600 × 24 × 30.

Multiply the result by the unit price of $15 per million characters to estimate the monthly cost.

> [!NOTE]
> If your estimated usage significantly exceeds your budget, you might be overestimating your needs.

##### Cost considerations

Increasing the concurrent request limit does *not* directly affect your costs. You pay for only what you use. The limit simply defines how much Azure Speech can scale before throttling begins.

You can't see the existing value of the parameter for the concurrent request limit in the Azure portal, the command-line tools, or API requests. To verify the existing value, create an Azure support request.

> [!NOTE]
> [Azure Speech containers](speech-container-howto.md) don't require increases of the concurrent request limit, because containers are constrained only by the CPUs of the hardware that they're hosted on.

#### Prepare the required information

For instructions on how to get the general resource information that you need, see [Create and submit a quota increase request](#create-and-submit-a-quota-increase-request) later in this article.

To create an increase request for standard voice, you also need to provide the *voice names that you're requesting the increase for*. You can find a list of all voice names in [Language and voice support for Azure Speech](./language-support.md?tabs=tts).

To create an increase request for custom voice, you need to provide the *custom endpoint ID*. To get this information for custom voice:

1. Go to the [Speech Studio](https://aka.ms/speechstudio/customvoice) portal.
1. Sign in if necessary, and then go to **Custom voice**.
1. Select your project, and then go to **Deploy model**.
1. Select the required endpoint.
1. Copy and save the **Endpoint ID** value.

#### Create the quota increase request

To create the request with the collected information, follow the steps in [Create and submit a quota increase request](#create-and-submit-a-quota-increase-request) later in this article.

### Text-to-speech avatar: Increase the limit of new connections

#### Prepare the required information

For instructions on how to get the general resource information that you need, see [Create and submit a quota increase request](#create-and-submit-a-quota-increase-request) later in this article.

To create an increase request for custom voice, you also need to provide the *standard avatar or custom avatar*.

#### Create the quota increase request

To create the request with the collected information, follow the steps in the next section, [Create and submit a quota increase request](#create-and-submit-a-quota-increase-request).

### Create and submit a quota increase request

To get the resource information that you need for the quota increase request, follow these steps:

1. Go to the [Azure portal](https://portal.azure.com/).

1. Select the resource for which you want to increase the concurrency request limit.

1. In the **Resource Management** group, select **Properties**.

1. Copy and save the values of the following fields:

   - **Subscription ID**
   - **Resource ID**
   - **Location** (your endpoint region)

Initiate the increase of the limit for concurrent requests for your resource by submitting a support request. You can also use a support request to check the current limit. To submit a support request:

1. Ensure that you have the required information listed in the previous sections.

1. Go to the [Foundry Tools Quota Increase Request](https://aka.ms/foundry-tools-quota-increase) form.

1. Provide the requestor details:

    1. First name
    1. Last name
    1. Your work or organization email address
        > [!NOTE]
        > Applications submitted with a personal email address (for example, hotmail.com, outlook.com, or gmail.com) aren't accepted.
    1. Company or organization name
        > [!NOTE]
        > You can request quota increases only on behalf of your own organization.

1. Provide the resource information:

    1. Azure subscription ID
    1. Foundry Tools resource ID
    1. Foundry Tools resource region
1. Provide the requested quota increase:

    1. New quota limit requested (integer only; for example, 300, 500, or 1,000)
    1. Business justification for the limit increase

1. Select the Foundry Tools product **Azure Speech**, and then select **Next**.

1. Select the Azure Speech feature that you're requesting the increase for. Options are:

    - Speech-to-text concurrent request limit for the base model endpoint
    - Speech-to-text concurrent request limit for the custom endpoint
    - Maximum requests per minute for fast transcription
    - Text-to-speech maximum number of transactions per time period for standard voices
    - Text-to-speech maximum number of transactions per time period for custom voices
    - Concurrent request limit for speech translation
    - Maximum requests per minute for batch text-to-speech avatar
    - New connections per minute for real-time text-to-speech avatar
    - Voice Live API tokens per minute

1. Add the additional feature-specific information requested in the form, and then select **Next**.

1. On the final page, provide additional contact information for your account or your partner's contact name and e-mail address.

1. Check the two confirmation questions, and then select **Submit**.

1. Note the support request number in Azure portal notifications. You're contacted shortly about your request.

You receive a confirmation e-mail that includes your application ID. Check your spam folder if you don't receive the confirmation e-mail. Ensure that you can receive follow-up communication on your case.
