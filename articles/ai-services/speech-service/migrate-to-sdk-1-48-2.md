---
title: Azure AI Speech SDK certificate revocation list (CRL) compatibility update
description: Learn how the CRL partitioning change affects Azure AI Speech SDK on Linux and Android, and what actions to take before July 1, 2026.
ms.service: azure-ai-speech
ms.topic: how-to
ms.date: 02/26/2026
ai-usage: ai-assisted
author: PatrickFarley
ms.author: pafarley
#Customer intent: As a developer, I want to understand the Azure AI Speech SDK CRL compatibility change and take the required mitigation steps.
---

# Azure AI Speech SDK: Certificate Revocation List (CRL) Compatibility Update

> [!IMPORTANT]
> **Effective date:** July 1, 2026. Action is required before this date to avoid service disruption on Linux and Android platforms.

The certificate revocation list (CRL) caching feature in Azure AI Speech SDK versions prior to 1.48.2 can cause connection failures to the Azure Speech Service on Linux and Android platforms. All SDK language bindings that use the native OpenSSL layer on these platforms (C#, C++, Java, Python, and Go) are affected. This issue is triggered by industry-wide changes to how CRLs are structured. Action is required before July 1, 2026 to avoid service disruption.

**Affected platforms:** Linux, Android  
**Affected SDK versions:** All versions prior to 1.48.2

## Prerequisites

Before you take action, confirm whether this issue applies to you:

- **Platform:** You run the Speech SDK on Linux or Android.
- **SDK version:** You use a version prior to 1.48.2. Check the version of the Speech SDK package in your dependency manager. For example:
  - **Python:** `pip show azure-cognitiveservices-speech`
  - **C#/.NET:** `dotnet list package`
  - **Java/Maven:** `mvn dependency:tree | grep speechsdk`
  - **Go:** `go list -m all | grep speechsdk`
- **CRL checking:** CRL checking is enabled (the default in versions prior to 1.48.1).

Identify whether your application uses cloud-only, hybrid (cloud + embedded), or embedded-only speech to [determine your impact by deployment type](#determine-your-impact-by-deployment-type).

If all three conditions apply, follow the steps in [Required action](#required-action).

## Determine your impact by deployment type

The impact of the CRL partitioning change depends on whether your application connects to Azure Speech cloud endpoints. Use the following table to determine your scenario and required actions.

| Customer type | Impact | Action required |
| --- | --- | --- |
| **Embedded only** (no cloud connection) | Not impacted | No action needed |
| **Hybrid** (cloud with embedded fallback) | Cloud STT/TTS can fail after certificate renewal | See [Required action](#required-action) |
| **Cloud only** | Cloud STT/TTS can fail after certificate renewal | See [Required action](#required-action) |

Use this quick decision guide:

1. **Does your app connect to Azure Speech cloud endpoints (STT or TTS)?**
   - **No** → You use embedded-only speech. **No action needed.**
   - **Yes** → Continue to step 2.
1. **Does your app also use embedded speech as a fallback?**
   - **Yes** → You have a hybrid deployment. Cloud features can fail after certificate renewal, but embedded fallback continues to work. **Action required** for cloud features.
   - **No** → You have a cloud-only deployment. **Speech calls can fail** after certificate renewal with no fallback. **Action required.**

### Embedded-only deployments

If your application uses only embedded (on-device) speech recognition or synthesis and **never connects to Azure Speech cloud endpoints**, you aren't affected by this change. No action is needed.

### Hybrid deployments (cloud with embedded fallback)

When your application is online, it uses cloud speech-to-text (STT) or text-to-speech (TTS). These cloud connections are subject to the CRL partitioning issue. Your embedded fallback continues to work when there's no data signal, but cloud features fail unless you take action.

Determine which caching scenario applies to you:

#### CRL disk caching enabled (default)

The SDK persists CRL data to disk using the system temp directory (`$TMPDIR` or `$TMP`). A stale CRL partition entry in the disk cache can cause persistent connection failures that survive application restarts. To resolve this:

1. Follow [Option 1: Upgrade to SDK 1.48.2+](#option-1-upgrade-to-sdk-version-1482-or-later-recommended) (recommended), or
1. Follow [Option 2: Disable CRL checking](#option-2-disable-crl-checking).
1. If you can't upgrade before the deadline, use the [temporary workaround](#temporary-workaround-clear-the-crl-disk-cache) to clear the CRL disk cache and reduce the duration of impact.

#### CRL disk caching not enabled

If you use a custom configuration or the `$TMPDIR`/`$TMP` environment variables are unset, the SDK still caches CRLs in memory during the process lifetime. Restarting the application clears the in-memory cache, but the issue reoccurs on the next cross-region connection or certificate rotation. Upgrade or disable CRL checking per the [Required action](#required-action) options.

> [!TIP]
> Hybrid deployments that fall back to embedded speech when offline continue to work in embedded mode, but cloud-dependent features fail until you apply the fix.

### Cloud-only deployments

All cloud STT/TTS calls are affected. The same two scenarios (CRL disk caching enabled or not enabled) described in [Hybrid deployments](#hybrid-deployments-cloud-with-embedded-fallback) apply to cloud-only deployments.

> [!WARNING]
> Cloud-only deployments have no fallback. After certificate renewal begins using partitioned CRLs, speech recognition and synthesis calls can fail if you haven't applied the fix. The exact timing depends on when your region's TLS certificates are renewed, but you should take action before July 1, 2026 to avoid any risk of disruption.

## Background

Certificate Authorities (CAs), including Microsoft's Public Key Infrastructure (PKI), are transitioning to **partitioned CRLs** to comply with CA/Browser Forum Baseline Requirements. This is an industry-wide change affecting all publicly trusted CAs.

Previously, each certificate issuer maintained a single CRL. With partitioned CRLs, the same issuer might have multiple CRLs, each covering a subset of certificates. This improves scalability (reducing CRL sizes from 10 MB+ to ~1 KB).

## The issue

The Azure AI Speech SDK (versions prior to 1.48.2) caches CRLs on some platforms using only the certificate issuer name as the cache key. With partitioned CRLs, this causes a cache mismatch:

- When connecting to one Azure region, the SDK downloads and caches the CRL for that region's TLS certificate
- When connecting to another region (or after certificate rotation), the cached CRL may not match the new certificate's partition
- OpenSSL rejects the connection with error: `X509_V_ERR_DIFFERENT_CRL_SCOPE` (error code 44)

**This affects you if:**
- You use the Speech SDK on **Linux or Android**
- You have **CRL checking enabled** (the default in affected versions)
- You connect to **multiple Azure regions**, OR
- Your region's certificate **rotates** (which happens automatically and may assign a different partition)

**This doesn't affect:**
- Windows deployments
- iOS or Mac deployments
- SDK version 1.48.2 or later

## Required action

Take one of the following actions **before July 1, 2026**:

### Option 1: Upgrade to SDK version 1.48.2 or later (recommended)

SDK version 1.48.2 includes a fix to properly handle partitioned CRLs. Speech SDK 1.48.1 and later disable CRL checking by default, which also prevents this issue but removes the extra validation layer.

Download the latest SDK: [Azure AI Speech SDK setup](quickstarts/setup-platform.md)

After upgrading, verify the fix by monitoring your application logs for the absence of error 44 (`X509_V_ERR_DIFFERENT_CRL_SCOPE`) during connections. If you connect to multiple Azure regions, test cross-region connections to confirm the issue is resolved.

### Option 2: Disable CRL checking

If you can't upgrade immediately, disable CRL checking in your current SDK version. Set the `OPENSSL_DISABLE_CRL_CHECK` property to `"true"` on your `SpeechConfig` object:

#### [C#](#tab/csharp)

```csharp
config.SetProperty("OPENSSL_DISABLE_CRL_CHECK", "true");
```

#### [C++](#tab/cpp)

```cpp
config->SetProperty("OPENSSL_DISABLE_CRL_CHECK", "true");
```

#### [Java](#tab/java)

```java
config.setProperty("OPENSSL_DISABLE_CRL_CHECK", "true");
```

#### [Python](#tab/python)

```python
speech_config.set_property_by_name("OPENSSL_DISABLE_CRL_CHECK", "true")
```

#### [Go](#tab/go)

```go
speechConfig.properties.SetPropertyByString("OPENSSL_DISABLE_CRL_CHECK", "true")
```

---

After setting the property, verify the fix by confirming connections succeed and no CRL-related errors (error 44 or `WS_OPEN_ERROR_UNDERLYING_IO_OPEN_FAILED`) appear in SDK logs.

> [!TIP]
> If you want to keep CRL checking but tolerate download failures, set `OPENSSL_CONTINUE_ON_CRL_DOWNLOAD_FAILURE` to `"true"` instead. This property allows connections to continue when a CRL can't be retrieved, while still performing CRL validation when CRLs are available.

For more configuration options, see [How to configure OpenSSL for Linux](how-to-configure-openssl-linux.md).

## Risks of not taking action

If you don't upgrade or disable CRL checking before July 1, 2026:

- **Connection failures** can occur when certificate rotation assigns a different CRL partition, or when connecting across regions
- Failures manifest as `WS_OPEN_ERROR_UNDERLYING_IO_OPEN_FAILED` errors
- **No advance warning** — the exact timing depends on when your region's TLS certificates are renewed
- **Service disruption** continues until the SDK is upgraded, CRL checking is disabled, or the CRL cache is cleared

## How to identify if you're impacted

### Error symptoms

Connection failures with messages such as:
```
Connection failed (no connection to the remote host). Internal error: 1. 
Error details: Failed with error: WS_OPEN_ERROR_UNDERLYING_IO_OPEN_FAILED
```

### SDK log indicators

Enable SDK logging to see detailed TLS errors. Look for:

```
SPX_TRACE_ERROR: AZ_LOG_ERROR: tlsio_openssl.c:1655 Error 44 was unexpected
SPX_TRACE_ERROR: AZ_LOG_ERROR: tlsio_openssl.c:691 error:0A000086:SSL routines::certificate verify failed
SPX_TRACE_ERROR: web_socket.cpp:930 WS open operation failed with result=1(WS_OPEN_ERROR_UNDERLYING_IO_OPEN_FAILED)
```
(The line numbers in the log messages may vary by SDK version)

**Error 44** (`X509_V_ERR_DIFFERENT_CRL_SCOPE`) is the specific indicator of this CRL partition mismatch issue.

### Confirming the issue

If you see these errors and are:
- Running on Linux or Android
- Using SDK version prior to 1.48.2
- Connecting to multiple regions OR experiencing failures after a period of working connections

Then you're likely affected by this issue.

## Temporary workaround: Clear the CRL disk cache

If you can't upgrade before the deadline or disable CRL checking, you can reduce the duration of impact by **disabling the CRL disk cache**. This limits the problem to in-memory caching only, meaning:

- Impact duration = process lifetime
- **Restarting your application clears the cache** and restores connectivity (until the next cross-region connection or rotation event)

### How to disable disk caching

Remove or unset the `TMPDIR` or `TMP` environment variables before starting your application. Without these variables, the SDK doesn't persist CRLs to disk.

Alternatively, clear the CRL cache directory manually:
- Default location: System temp directory (`$TMPDIR` or `$TMP`)
- Delete cached `.crl` files and restart your application

> [!NOTE]
> This is a temporary workaround, not a solution. Upgrading to SDK 1.48.2 or later, or disabling CRL checking, is still required.

## Timeline

| Date | Event |
| --- | --- |
| Now | Review your deployment type and SDK version |
| February 2026 | SDK 1.48.2 released with fix |
| **July 1, 2026** | **Deadline: Upgrade or disable CRL checking** |
| After July 1, 2026 | Unpatched deployments can experience connection failures as certificates are renewed |

## Frequently asked questions

### Why is this happening?

Certificate Authorities are required to implement partitioned CRLs for compliance with industry standards. This isn't specific to Microsoft — all major CAs are making this change.

### Does this affect Windows?

No. Windows handles certificate validation differently and isn't affected.

### I only use one Azure region. Am I still affected?

Yes. Certificate rotation (which happens automatically) might assign your region's certificate to a different partition, triggering the same failure.

### What if I have CRL checking disabled already?

You aren't affected. No action is required, though upgrading to the latest SDK for other improvements and updates is recommended.

### Is there a security risk to disabling CRL checking?

CRL checking provides an extra layer of certificate validation. For most use cases, the security impact of disabling it is minimal, as other validation mechanisms (certificate chain, expiration) remain active. Consult your security team if you have specific compliance requirements.

### How do I enable SDK logging to diagnose the issue?

See the SDK documentation for enabling diagnostic logging: [Speech SDK logging](how-to-use-logging.md).

### I use embedded speech only, with no cloud connection. Am I affected?

No. This issue only affects connections to Azure Speech cloud endpoints. If your application never connects to cloud STT or TTS services, you aren't impacted. For more information, see [Determine your impact by deployment type](#determine-your-impact-by-deployment-type).

## Support

If you have questions or need assistance:

- **Documentation:** [Azure AI Speech Service documentation](/azure/ai-services/speech-service/)
- **Support:** Open a support ticket through the Azure portal
- **SDK issues:** [GitHub - Azure Cognitive Services Speech SDK](https://github.com/Azure-Samples/cognitive-services-speech-sdk/issues)

## Related content

- [Speech SDK release notes](releasenotes.md)
- [How to configure OpenSSL for Linux](how-to-configure-openssl-linux.md)
- [Azure AI Speech SDK setup](quickstarts/setup-platform.md)
- [Speech SDK logging](how-to-use-logging.md)
