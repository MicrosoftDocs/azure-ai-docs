---
title: Batch transcription overview - Speech service
titleSuffix: Azure AI services
description: Batch transcription is ideal if you want to transcribe a large quantity of audio in storage, such as Azure blobs. Then you can asynchronously retrieve transcriptions.
manager: nitinme
author: PatrickFarley
ms.author: pafarley
ms.service: azure-ai-speech
ms.topic: overview
ms.date: 5/25/2025
ms.devlang: csharp
ms.custom: devx-track-csharp
---

# What is batch transcription?

Batch transcription is used to transcribe a large amount of audio data in storage. Both the [Speech to text REST API](rest-speech-to-text.md#batch-transcription) and [Speech CLI](spx-basics.md) support batch transcription. 

You should provide multiple files per request or point to an Azure Blob Storage container with the audio files to transcribe. The batch transcription service can handle a large number of submitted transcriptions. The service transcribes the files concurrently, which reduces the turnaround time.

## How does it work?

With batch transcriptions, you submit the audio data, and then retrieve transcription results asynchronously. The service transcribes the audio data and stores the results in a storage container. You can then retrieve the results from the storage container.

> [!TIP]
> For a low or no-code solution, you can use the [Batch Speech to text Connector](/connectors/cognitiveservicesspe/) in Power Platform applications such as Power Automate, Power Apps, and Logic Apps. See the [Power automate batch transcription](power-automate-batch-transcription.md) guide to get started.

To use the batch transcription REST API:

1. [Locate audio files for batch transcription](batch-transcription-audio-data.md) - You can upload your own data or use existing audio files via public URI or [shared access signature (SAS)](/azure/storage/common/storage-sas-overview) URI. 
1. [Create a batch transcription](batch-transcription-create.md) - Submit the transcription job with parameters such as the audio files, the transcription language, and the transcription model.
1. [Get batch transcription results](batch-transcription-get.md) - Check transcription status and retrieve transcription results asynchronously. 

> [!IMPORTANT]
> Batch transcription jobs are scheduled on a best-effort basis. At peak hours it might take up to 30 minutes or longer for a transcription job to start processing. See how to check the current status of a batch transcription job in [this section](batch-transcription-get.md#get-transcription-status).

## Best practices for improving performance


**Request size**: Batch transcription is asynchronous, and requests are processed one at a time in each region. Submitting jobs at a higher rate does not speed up processing. For example, sending 600 or 6,000 requests per minute has no effect on throughput. We recommend submitting ~1000 files in a single `Transcription_Create` request. This way, you send fewer requests overall.

**Time distribution**: Distribute your requests over time: Submit them across several hours rather than sending them all within a few minutes. Backend processing maintains a stable performance level due to fixed bandwidth, so sending requests too quickly doesn’t improve performance.

**Job monitoring**: [When monitoring job status](./batch-transcription-get.md), polling every few seconds is unnecessary. If you submit multiple jobs, only the first job will be processed initially; subsequent jobs will wait until the first job completes. Polling all jobs frequently increases system load without benefit. Checking the status every 10 minutes is sufficient, and polling more often than once per minute is not recommended. 
- Because of the sequential processing, you can get job status by checking only a subset of the files: check the first 100 files, and if they're not completed, later batches are likely not competed either. We recommend waiting at least one minute (ideally five minutes) before checking again. 

**Avoid peak traffic for API calls**: The `ListFiles`, `Update`, and `Get` API calls behave similarly to the `Create` call and should be minimized during peak traffic times. 

**Load balancing**: To optimize throughput for large-scale batch transcription, consider distributing your jobs across multiple supported Azure regions. This approach can help balance load and reduce overall processing time, provided your data and compliance requirements allow for multi-region usage. Review [region availability](./regions.md) and ensure your storage and resources are accessible from each region you plan to use.


## Related content

- [Locate audio files for batch transcription](batch-transcription-audio-data.md)
- [Create a batch transcription](batch-transcription-create.md)
- [Get batch transcription results](batch-transcription-get.md)
- [See batch transcription code samples at GitHub](https://github.com/Azure-Samples/cognitive-services-speech-sdk/tree/master/samples/batch/)
