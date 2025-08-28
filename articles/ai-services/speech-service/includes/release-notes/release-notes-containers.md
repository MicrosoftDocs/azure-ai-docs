---
author: PatrickFarley
ms.service: azure-ai-speech
ms.topic: include
ms.date: 7/1/2025
ms.author: pafarley
---

### 2025-June release

#### Neural text to speech 3.11.0

Released [neural text to speech version 3.11.0](../../speech-container-ntts.md).

- Added support for new neural voices: `de-DE-SeraphinaMultilingualNeural`, `es-ES-XimenaMultilingualNeural`, `fi-FI-SelmaNeural`, `nb-NO-FinnNeural`.
- Added support for multilingual custom lexicons.

### 2025-May release

Add support for the latest model versions:
- [Neural text to speech 3.10.0](../../speech-container-ntts.md)

For text to speech:
- Updated the text to speech backend and frontend engine to the latest versions.
- Added support for multilingual custom lexicons.
- Improved the health check functionality. The health check endpoint is now `/synthesize/health`. When the service is healthy, this endpoint returns HTTP status 200; if the service is unhealthy, it returns HTTP status 503.
- Updated the base image to AspNet 8.0.16 to address security vulnerabilities from the March/April 2025 Microsoft ASP.NET Core Security Update.

### 2025-March release

Add support for the latest model versions:
- Neural text to speech 3.9.0
- Speech to text 5.0.1 (Preview)
- Custom speech to text 5.0.1 (Preview)

For speech to text and custom speech to text, the following features are included:
- Support for new speech to text models
- Operating system change to Azure Linux 3.0
- Support for new locales: ar-dz, as-in, es-gq or-in, pa-in and ur-in
- Decoder update
- Ability to use newer custom models (2023+) in container

For text to speech, added support for new neural voices: `en-GB-OliviaNeural`, `en-US-ChristopherNeural` and `nl-NL-FennaNeural`.

### 2025-February release

Add support for the latest model versions:
- Speech language identification 1.18.0
- Neural text to speech 3.7.0
- Speech to text 4.12.0
- Custom speech to text 4.12.0

Here are the highlights of the releases:

| Feature update | Speech to text | Custom speech to text | Neural text to speech | Speech language identification |
|------|------|------|--------|------|
| Vulnerability fixes | ✅ | ✅ | ✅ | ✅ |
| Migrated OS from Ubuntu 20.04 to Ubuntu 22.04 | ✅ | ✅ | ✅ | ✅ |
| New Locales: ar-ly, fr-be, nl-be and uz-uz | ✅ | ✅ |  |  |
| Updated nuget packages, Go version | ✅ | ✅ |  |  |
| Added model download parallelization to decrease model download time | ✅ | ✅ | ✅ |  |

### 2024-October release

Add support for the latest model versions:
- Speech language identification 1.16.0
- Neural text to speech 3.5.0
    - Make `en-us-ariacpuneural` an alias to `en-us-jessacpuneural`
    - Update the text to speech backend engine version
- Speech to text 4.10.0
    - Restore support for locale `uk-UA`
    - Fix silence settings to work with long periods of silence in the audio
    - Replace deprecated models: `cs-CZ`, `da-DK`, `en-GB`, `fr-CA`, `hu-HU`, `it-CH`, `tr-TR`, `zh-CN-sichuan`
- Custom speech to text 4.10.0

### 2024-September release

Add support for the latest model versions:
- Speech language identification 1.15.0
    - Mitigate Vulnerabilities
- Neural text to speech 3.4.0
    - New voices: `en-us-andrewmultilingualneural`, `en-us-jessaneural`, `es-us-alonsoneural`, `es-us-palomaneural`, `it-it-isabellamultilingualneural`
    - Mitigate Vulnerabilities
- Speech to text 4.9.0
    - New Locales: `ar-YE`, `af-ZA`, `am-ET`, `ar-MA`, `ar-TN`, `sw-KE`, `sw-TZ`, `zu-ZA`
    - Mitigate Vulnerabilities
    - Update Deprecated Models
- Custom speech to text 4.9.0
    - Mitigate Vulnerabilities

### 2024-August release

Add support for the latest model versions:
- Speech language identification 1.14.0
    - Upgrade .NET 8.0
    - Mitigate Vulnerabilities
- Neural text to speech 3.3.0
    - Upgrade .NET 8.0
    - Mitigate Vulnerabilities
- Speech to text 4.8.0    
    - Upgrade .NET 8.0
    - Mitigate Vulnerabilities
    - Upgrade Recognition Engine
    - Fix the issue where `PropertyId.Speech_SegmentationSilenceTimeoutMs` was being ignored.
    - Update Deprecated Models
    - Remove the `uk-UA` locale

### 2024-February release

Add support for the latest model versions:
- Custom speech to text 4.6.0
- Speech to text 4.6.0
- Neural text to speech 3.1.0

Upgrade speech to text components to the latest.
Upgrade all `es` locales models to the latest.
Increase media transforming buffer for speech to text use cases.

### 2023-November release

Add support for the latest model versions:
- Custom speech to text 4.5.0
- Speech to text 4.5.0
- Neural text to speech 2.19.0


### 2023-October release

Add support for the latest model versions:
- Custom speech to text 4.4.0
- Speech to text 4.4.0
- Neural text to speech 2.18.0

Fix a bunch of high risk vulnerability issues.

Remove redundant logs in containers.

Upgrade internal media component to the latest.

Add support for voice `en-IN-NeerjaNeural`.

### 2023-September release

Add support for the latest model versions:
- Speech language identification 1.12.0
- Custom speech to text 4.3.0
- Speech to text 4.3.0
- Neural text to speech 2.17.0

Upgrade custom speech to text and speech to text to the latest framework.

Fix vulnerability issues.

Add support for voice `ar-AE-FatimaNeural`.

### 2023-July release

Add support for the latest model versions:
- Custom speech to text 4.1.0
- Speech to text 4.1.0
- Neural text to speech 2.15.0

Fix the issue of running speech to text container via `docker` mount options with local custom model files.

Fix the issue that in some cases the `RECOGNIZING` event doesn't show up in response through the Speech SDK.

Fix vulnerability issues.

### 2023-June release

Add support for the latest model versions:
- Custom speech to text 4.0.0
- Speech to text 4.0.0
- Neural text to speech 2.14.0

On-premises speech to text images are upgraded to .NET 6.0

Upgrade display models for locales including `en-us`, `ar-eg`, `ar-bh`, `ja-jp`, `ko-kr`, and more.

Upgrade the speech to text container component to address vulnerability issues.

Add support for locale voices `de-DE-AmalaNeural`,`de-AT-IngridNeural`,`de-AT-JonasNeural`, and `en-US-JennyMultilingualNeural`

### 2023-May release

Add support for the latest model versions:
- Custom speech to text 3.14.0
- Speech to text 3.14.0
- Neural text to speech 2.13.0

Fix the `he-IL` punctuation issue

Fix vulnerability issues

Add new locale voice `en-US-MichelleNeural`and `es-MX-CandelaNeural`

### 2023-April release

Security Updates

Fix vulnerability issues

### 2023-March release
	
Add support for the latest model versions:
- Custom speech to text 3.12.0
- Speech to text 3.12.0
- Speech language identification 1.11.0
- Neural text to speech 2.11.0

Fix vulnerability issues

Fix the `tr-TR` capitalization issue

Upgrade the speech to text `en-US` display models

Add support for the `ar-AE-HamdanNeural` standard voice.

### 2023-February release

#### New container versions

Add support for latest model versions:
- Custom speech to text 3.11.0
- Speech to text 3.11.0
- Neural text to speech 2.10.0

Fix vulnerability issues

Regular upgrade for speech models

Add new Abraic locales:
- ar-IL
- ar-PS

Upgrade Hebrew and Turkish display models

### 2023-January release

#### New container versions

Add support for latest model versions:
- Custom speech to text 3.10.0
- Speech to text 3.10.0
- Neural text to speech 2.9.0

Fix Hypothesis mode issue

Fix HTTP Proxy issue

Custom speech to text container disconnected mode

Add CNV Disconnected container support to TTS Frontend

Add support for these locale-voices:
- da-DK-ChristelNeural
- da-DK-JeppeNeural
- en-IN-PrabhatNeural

### 2022-December release

#### New container versions

Add support for latest model versions:
- Custom speech to text 3.9.0
- Speech to text 3.9.0
- Neural text to speech 2.8.0

Fix ipv4/ipv6 issue

Fix vulnerability issue

### 2022-November release

#### New container versions

Add support for latest model versions:
- Custom speech to text 3.8.0
- Speech to text 3.8.0
- Neural text to speech 2.7.0

### 2022-October release

#### New container versions

Add support for latest model versions:
- Custom speech to text 3.7.0
- Speech to text 3.7.0
- Neural text to speech 2.6.0

### 2022-September release

#### Speech to text 3.6.0-amd64

Add support for latest model versions.

Add support for these locales:
  * az-az
  * bn-in
  * bs-ba
  * cy-gb
  * eu-es
  * fa-ir
  * gl-es
  * he-il
  * hy-am
  * it-ch
  * ka-ge
  * kk-kz
  * mk-mk
  * mn-mn
  * ne-np
  * ps-af
  * so-so
  * sq-al
  * wuu-cn
  * yue-cn
  * zh-cn-sichuan

Regular monthly updates including security upgrades and vulnerability fixes.

#### Custom speech to text 3.6.0-amd64

Regular monthly updates including security upgrades and vulnerability fixes.

#### Neural text to speech v2.5.0

Add support for these [standard voices](../../language-support.md?tabs=tts):
   * `az-az-babekneural`
   * `az-az-banuneural`
   * `fa-ir-dilaraneural`
   * `fa-ir-faridneural`
   * `fil-ph-angeloneural`
   * `fil-ph-blessicaneural`
   * `he-il-avrineural`
   * `he-il-hilaneural`
   * `id-id-ardineural`
   * `id-id-gadisneural`
   * `ka-ge-ekaneural`
   * `ka-ge-giorgineural`

Regular monthly updates including security upgrades and vulnerability fixes.

### 2022-May release

#### Speech-language-detection Container v1.9.0-amd64-preview

Bug fixes for [speech-language-detection](~/articles/ai-services/speech-service/speech-container-howto.md).

### 2022-March release

#### Custom speech to text Container v3.1.0
Add support to [get display models](../../speech-container-cstt.md#display-model-download).

### 2022-January release

#### Speech to text Container v3.0.0
Add support for using containers in [disconnected environments](../../../containers/disconnected-containers.md).

#### Speech to text Container v2.18.0
Regular monthly updates including security upgrades and vulnerability fixes.

#### Neural-Neural text to speech Container v1.12.0
Add support for these standard voices: `am-et-amehaneural`, `am-et-mekdesneural`, `so-so-muuseneural`, and `so-so-ubaxneural`.

Regular monthly updates including security upgrades and vulnerability fixes.

