---
title: include file
description: include file
author: PatrickFarley
ms.author: pafarley
ms.service: azure-ai-speech
ms.topic: include
ms.date: 12/29/2025
ms.custom: include
---

When you're ready to create a custom text-to-speech voice for your application, start by gathering audio recordings and associated scripts to train the voice model. For details on recording voice samples, see [the tutorial](../../../../record-custom-voice-samples.md). The Speech service uses this data to create a unique voice tuned to match the voice in the recordings. After you train the voice, you can start synthesizing speech in your applications.

All data you upload must meet the requirements for the data type that you choose. It's important to correctly format your data before it's uploaded, which ensures the data is accurately processed by the Speech service. To confirm that your data is correctly formatted, see [Training data types](../../../../how-to-custom-voice-training-data.md).

> [!NOTE]
> - Standard subscription (S0) users can upload five data files simultaneously. If you reach the limit, wait until at least one of your data files finishes importing. Then try again.
> - The maximum number of data files that standard subscription (S0) users can import per subscription is 500 .zip files. For more details, see [Speech service quotas and limits](../../../../speech-services-quotas-and-limits.md#custom-voice---professional).

## Upload your data

> [!TIP]
> For a sample consent statement and training data, see the [GitHub repository](https://github.com/Azure-Samples/Cognitive-Speech-TTS/tree/master/CustomVoice/Sample%20Data). 

When you're ready to upload your data, go to the **Prepare training data** tab to add your first training set and upload data. A *training set* is a set of audio utterances and their mapping scripts used for training a voice model. You can use a training set to organize your training data. The service checks data readiness for each training set. You can import multiple data files to a training set.

To upload training data, follow these steps:
1. Sign in to the [Microsoft Foundry (classic) portal](https://ai.azure.com/?cid=learnDocs).
1. Select **Fine-tuning** from the left pane and then select **AI Service fine-tuning**.
1. Select the professional voice fine-tuning task (by model name) that you [started as described in the create professional voice article](/azure/ai-services/speech-service/professional-voice-create-project).
1. Select **Prepare training data** > **Upload data**. 
1. In the **Upload data** wizard, choose a [data type](../../../../how-to-custom-voice-training-data.md). If you're using the sample data, select **Individual utterances + matching transcript**. 

    :::image type="content" source="../../../../media/custom-voice/professional-voice/choose-training-data-type.png" alt-text="Screenshot of the page to select the training data type." lightbox="../../../../media/custom-voice/professional-voice/choose-training-data-type.png":::

1. Select **Next**.
1. On the **Specify the target training set** page, select **Create new**. 
1. Enter a training set name and then select **Create**.

    :::image type="content" source="../../../../media/custom-voice/professional-voice/create-new-training-set.png" alt-text="Screenshot of the page to create a new training set." lightbox="../../../../media/custom-voice/professional-voice/create-new-training-set.png":::

1. Select **Next**.
1. On the **Data upload** page, select a **Recording file** and **Script file** in the respective tiles. You can select local files from your computer or enter the Azure Blob storage URL to upload data.
1. Select **Next**.
1. Enter a name and description for your data and then select **Next**.
1. Review the upload details, and select **Upload data**.

> [!NOTE]
> Duplicate IDs aren't accepted. Utterances with the same ID are removed.
> 
> Duplicate audio names are removed from the training. Make sure the data you select don't contain the same audio names within the .zip file or across multiple .zip files. If utterance IDs (either in audio or script files) are duplicates, they're rejected.

Data files are automatically validated when you select **Upload data**. Data validation includes a series of checks on the audio files to verify their file format, size, and sampling rate. If there are any errors, fix them and submit again. 

After you upload the data, you can check the details in the training set detail view. On the detail page, you can check the pronunciation issue and the noise level for each of your data. The pronunciation score at the sentence level ranges from 0-100. A score below 70 normally indicates a speech error or script mismatch. Utterances with an overall score lower than 70 are rejected. A heavy accent can reduce your pronunciation score and affect the generated digital voice.

## Resolve data issues online

After you upload the data, you can check the data details for the training set. Before you continue to [train your voice model](../../../../professional-voice-train-voice.md), try to resolve any data problems.

### Typical data issues

The following tables describe common data problems. 

**Auto-rejected**

The training process excludes data with these problems. The import process ignores data with these problems, so you don't need to delete them. You can [fix these data problems online](#resolve-data-issues-online) or upload corrected data for training.  

| Category | Name | Description |
| --------- | ----------- | --------------------------- |
| Script | Invalid separator| You must separate the utterance ID and the script content with a Tab character.|
| Script | Invalid script ID| The script line ID must be numeric.|
| Script | Duplicated script|Each line of the script content must be unique. The line is duplicated with {}.|
| Script | Script too long| The script must be less than 1,000 characters.|
| Script | No matching audio| The ID of each utterance (each line of the script file) must match the audio ID.|
| Script | No valid script| No valid script is found in this dataset. Fix the script lines that appear in the detailed problem list.|
| Audio | No matching script| No audio files match the script ID. The name of the .wav files must match with the IDs in the script file.|
| Audio | Invalid audio format| The audio format of the .wav files is invalid. Check the .wav file format by using an audio tool like [SoX](http://sox.sourceforge.net/).|
| Audio | Low sampling rate| The sampling rate of the .wav files can't be lower than 16 KHz.|
| Audio | Too long audio| Audio duration is longer than 30 seconds. Split the long audio into multiple files. It's a good idea to make utterances shorter than 15 seconds.|
| Audio | No valid audio| No valid audio is found in this dataset. Check your audio data and upload again.|
| Mismatch | Low scored utterance| Sentence-level pronunciation score is lower than 70. Review the script and the audio content to make sure they match.|

**Auto-fixed**

The system automatically fixes the following problems, but you should review and confirm the fixes are correct.

| Category | Name | Description |
| --------- | ----------- | --------------------------- |
| Mismatch |Silence auto fixed |The start silence is detected to be shorter than 100 ms, and is extended to 100 ms automatically. Download the normalized dataset and review it. |
| Mismatch |Silence auto fixed | The end silence is detected to be shorter than 100 ms, and is extended to 100 ms automatically. Download the normalized dataset and review it.|
| Script | Text auto normalized|Text is automatically normalized for digits, symbols, and abbreviations. Review the script and audio to make sure they match.|

**Manual check required**

Unresolved problems listed in the next table affect the quality of training, but the training process doesn't exclude data with these problems. For higher-quality training, fix these problems manually. 

| Category | Name | Description |
| --------- | ----------- | --------------------------- |
| Script | Non-normalized text |This script contains symbols. Normalize the symbols to match the audio. For example, normalize */* to *slash*.|
| Script | Not enough question utterances| At least 10 percent of the total utterances should be question sentences. This helps the voice model properly express a questioning tone.|
| Script | Not enough exclamation utterances| At least 10 percent of the total utterances should be exclamation sentences. This helps the voice model properly express an excited tone.|
| Script | No valid end punctuation| Add one of the following at the end of the line: full stop (half-width '.' or full-width '。'), exclamation point (half-width '!' or full-width '！' ), or question mark (half-width '?' or full-width '？').|
| Audio| Low sampling rate for neural voice | It's recommended that the sampling rate of your .wav files be 24 KHz or higher for creating neural voices. If it's lower, the system automatically raises it to 24 KHz.|
| Volume |Overall volume too low|Volume shouldn't be lower than -18 dB (10 percent of max volume). Control the volume average level within proper range during the sample recording or data preparation.|
| Volume | Volume overflow| Overflowing volume is detected at {}s. Adjust the recording equipment to avoid the volume overflow at its peak value.|
| Volume | Start silence problem | The first 100 ms of silence isn't clean. Reduce the recording noise floor level, and leave the first 100 ms at the start silent.|
| Volume| End silence problem| The last 100 ms of silence isn't clean. Reduce the recording noise floor level, and leave the last 100 ms at the end silent.|
| Mismatch | Low scored words|Review the script and the audio content to make sure they match, and control the noise floor level. Reduce the length of long silence, or split the audio into multiple utterances if it's too long.|
| Mismatch | Start silence problem |Extra audio was heard before the first word. Review the script and the audio content to make sure they match, control the noise floor level, and make the first 100 ms silent.|
| Mismatch | End silence problem| Extra audio was heard after the last word. Review the script and the audio content to make sure they match, control the noise floor level, and make the last 100 ms silent.|
| Mismatch | Low signal-noise ratio | Audio SNR level is lower than 20 dB. At least 35 dB is recommended.|
| Mismatch | No score available |Failed to recognize speech content in this audio. Check the audio and the script content to make sure the audio is valid, and matches the script.|

## Next step

> [!div class="nextstepaction"]
> [Train the professional voice](../../../../professional-voice-train-voice.md)

