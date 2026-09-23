---
title: Configure a cache for speech container diarization
titleSuffix: Foundry Tools
description: Learn how to configure a required Redis-compatible cache for real-time speech container diarization and validate speaker labels.
author: PatrickFarley
manager: mcleans
ms.service: azure-speech-foundry-tools
ms.topic: how-to
ms.date: 09/02/2026
ms.author: pafarley
ms.custom: doc-kit-assisted
ai-usage: ai-assisted
#Customer intent: As a developer, I want to configure the cache required for real-time speech-to-text container diarization and validate speaker labels.
---

# Configure a cache for speech container diarization

Only real-time speech-to-text containers need a customer-operated Redis-compatible cache for speaker diarization in connected and disconnected modes, including for audio shorter than four hours. Fast transcription containers don't need a cache for diarization. By default, the cache retains four hours of real-time diarization data. Audio can run beyond four hours, but the oldest cached data starts to be discarded, which might degrade diarization quality.

For example, if a speaker appears in hour 1 and again after hour 5, the earlier speaker information might no longer be available. Speaker association or labeling quality might then degrade. When diarization is required, segment audio into inputs of four hours or less. This article shows you how to configure the required cache and validate diarization results.

## Prerequisites

- A real-time speech to text container image, version 5.1.0 or later.
- A host that meets the [Speech container requirements](speech-container-howto.md#host-computer-requirements-and-recommendations), including the CPU, memory, and AVX2 requirements.
- For connected mode, a Speech endpoint and key for container billing.
- For disconnected mode, approval and license setup for disconnected containers, including license and output mount directories that are writable by the container's nonroot user. For more information, see [Use containers in disconnected environments](../containers/disconnected-containers.md).
- A customer-operated Redis-compatible cache that the speech to text container can reach.
- Docker for the local validation example.
- A recognition client or application that can submit audio for diarization and inspect speaker labels.

## Understand cache requirements

The Redis-compatible cache is required for proper diarization functionality at every audio length. Configure both settings when you enable diarization:

| Setting | Required value | Purpose |
| --- | --- | --- |
| `InClusterRedisCacheEnabled` | `true` | Enables the Redis-compatible cache required for diarization. |
| `InClusterRedisCacheEndpoint` | `<host-or-ip>:<port>` | Specifies the reachable Redis-compatible cache endpoint required for diarization. |

The default cache retention limit is four hours. This limit doesn't end the diarization session or prevent audio from running longer. After four hours, the oldest cached diarization data begins to be discarded, so speaker labels might become less reliable. Segment diarized audio into inputs of four hours or less.

## Test the configuration with Valkey

The following local validation example starts a speech container with the required cache and uses the public `valkey/valkey` image to test cache reachability. It creates a user-defined Docker network so the speech container can resolve the stable `diarization-cache` container name.

1. Create a Docker network for the test containers.

   ```bash
   docker network create speech-diarization-test
   ```

   ```output
   <network-id>
   ```

1. Start Valkey 8.1.10 on the network.

   ```bash
   docker run --detach --name diarization-cache \
     --network speech-diarization-test \
       valkey/valkey:8.1.10-alpine
   ```

   ```output
   <container-id>
   ```

1. From another container on the same network, verify that the cache name resolves and that Valkey responds.

    ```bash
    docker run --rm --network speech-diarization-test \
       valkey/valkey:8.1.10-alpine \
       valkey-cli -h diarization-cache PING
    ```

    ```output
    PONG
    ```

Start the real-time speech to text container on the same network. Select the tab for your container mode, and replace each placeholder with the value for your environment.

# [Connected speech to text](#tab/connected)

```bash
docker run --rm --interactive --tty \
   --name speech-to-text \
   --network speech-diarization-test \
   --publish 5000:5000 \
   --memory 8g \
   --cpus 4 \
   {SPEECH_TO_TEXT_IMAGE} \
   Eula=accept \
   Billing={ENDPOINT_URI} \
   ApiKey={API_KEY} \
   InClusterRedisCacheEnabled=true \
   InClusterRedisCacheEndpoint=diarization-cache:6379
```

```output
<container-startup-logs>
```

# [Disconnected speech to text](#tab/disconnected)

The disconnected license must already be downloaded. This service-run command mounts the existing license and an output path for usage records.

```bash
docker run --rm --interactive --tty \
   --name speech-to-text \
   --network speech-diarization-test \
   --publish 5000:5000 \
   --memory 8g \
   --cpus 4 \
   --volume {LICENSE_MOUNT} \
   --volume {OUTPUT_PATH} \
   {SPEECH_TO_TEXT_IMAGE} \
   Eula=accept \
   Mounts:License={CONTAINER_LICENSE_DIRECTORY} \
   Mounts:Output={CONTAINER_OUTPUT_DIRECTORY} \
   InClusterRedisCacheEnabled=true \
   InClusterRedisCacheEndpoint=diarization-cache:6379
```

```output
<container-startup-logs>
```

---

After the container starts without cache connection errors, use your recognition client or application to submit diarization audio and inspect the speaker labels as described in the next section. Startup messages vary by container version and environment.

Both commands are for local Docker validation and aren't production topologies. Kubernetes and Helm deployment are outside the scope of this example.

## Validate diarization results

Validate the cache connection and speaker labels before you use diarization in production:

1. Confirm that the Redis-compatible cache is reachable from the speech container network before you start the speech container.
1. Submit an input of four hours or less and confirm that the diarization result contains the expected speaker labels.
1. Inspect the speech container and cache logs for connectivity errors.
1. If you test audio longer than four hours, inspect speaker association and labels carefully because discarding the oldest cached data might degrade quality. For production workloads that require diarization, segment audio into inputs of four hours or less.

## Troubleshoot cache connectivity

If the cache validation command doesn't return `PONG`, use the following checks:

- If the command reports that it can't resolve `diarization-cache`, confirm that the cache and validation containers use the `speech-diarization-test` network.
- If the command reports that the connection is refused, confirm that the `diarization-cache` container is running and listening on port `6379`.
- If the speech container reports cache connection errors, confirm that `InClusterRedisCacheEnabled` is `true` and that `InClusterRedisCacheEndpoint` contains only the reachable `<host-or-ip>:<port>` value. Don't include a URL scheme.
- If the local Valkey test succeeds but the speech container can't connect, confirm that the speech container uses the same Docker network and the endpoint `diarization-cache:6379`.

## Prepare for production

Before production, choose and configure a Redis-compatible service that meets your organization's reliability and security requirements. Evaluate its compatibility with the two container settings in this article, and complete the following checklist:

- Network connectivity and endpoint reachability from each speech container.
- Security controls that meet your organization's requirements.
- Reliability, high availability, monitoring, and scaling.
- Failover and recovery procedures.
- Audio segmentation into inputs of four hours or less when diarization is required.
- Speaker label validation with representative audio.
- Platform-specific deployment configuration, including Kubernetes or Helm configuration when applicable.

## Related content

- [Speech to text containers with Docker](speech-container-stt.md)
- [Configure Speech containers](speech-container-configuration.md)
- [Speech to text container release notes](releasenotes.md?tabs=speech-to-text)