---
title: Configure diarization continuation for speech containers
titleSuffix: Foundry Tools
description: Configure a Redis-compatible cache to preserve diarization state across connected and disconnected real-time speech-to-text container sessions.
author: PatrickFarley
manager: mcleans
ms.service: azure-speech-foundry-tools
ms.topic: how-to
ms.date: 08/26/2026
ms.author: pafarley
ms.custom: doc-kit-assisted
ai-usage: ai-assisted
#Customer intent: As a developer, I want to configure state-backed diarization continuation for real-time speech-to-text containers.
---

# Configure diarization continuation for speech containers

Real-time speech to text containers support speaker diarization in connected and disconnected modes. Each individual diarization session has a four-hour maximum. At the boundary, the session ends. For workloads that run longer than four hours, your application starts a replacement session.

A customer-operated Redis-compatible cache preserves diarization state for the replacement session. The cache doesn't extend an individual session. This article shows you how to configure and validate the cache for state-backed continuation.

## Prerequisites

- A real-time speech to text container image, version 5.1.0 or later.
- For connected mode, a Speech endpoint and key for container billing.
- For disconnected mode, approval and license setup for disconnected containers, including the required license and output mounts. For more information, see [Use containers in disconnected environments](../containers/disconnected-containers.md).
- A customer-operated Redis-compatible cache that the speech to text container can reach.
- Docker for the local validation example.
- A recognition client or application that can start a replacement recognition session and verify diarization continuity.

## Understand session continuation

State-backed continuation uses separate diarization sessions. When the current session reaches the four-hour boundary, it ends, and your application starts a replacement session. The container retrieves the saved diarization state from the configured Redis-compatible cache for the replacement session.

Configure both of the following container settings:

| Setting | Value | Purpose |
| --- | --- | --- |
| `InClusterRedisCacheEnabled` | `true` | Enables the external cache for diarization state. |
| `InClusterRedisCacheEndpoint` | `<host-or-ip>:<port>` | Specifies the reachable Redis-compatible cache endpoint. |

Without a configured cache, the session ends with an error at the four-hour boundary. The cache preserves state between sessions; it doesn't make a single session run longer than four hours.

## Test the configuration with Valkey

The following local validation example starts a speech container and uses the public `valkey/valkey` image to test connectivity and configuration. It creates a user-defined Docker network so the speech container can resolve the stable `diarization-cache` container name.

1. Create a Docker network for the test containers.

   ```bash
   docker network create speech-diarization-test
   ```

   ```output
   <network-id>
   ```

1. Start Valkey on the network. Replace `{VALKEY_TAG}` with the tag you want to test.

   ```bash
   docker run --detach --name diarization-cache \
     --network speech-diarization-test \
     valkey/valkey:{VALKEY_TAG}
   ```

   ```output
   <container-id>
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

After the container starts, use your recognition client or application to run the validation scenarios in the next section.

Both commands are for local Docker validation. They use a single cache container without authentication or TLS and aren't production topologies. Kubernetes and Helm deployment are outside the scope of this example.

## Validate continuation behavior

Validate all three scenarios before you depend on state-backed continuation:

1. Run a diarization session for less than four hours and confirm that recognition and speaker separation work as expected.
1. Run to the four-hour boundary without a cache and confirm that the session fails at the boundary. Don't depend on exact error text.
1. Configure Valkey or Redis, run to the four-hour boundary, start a replacement session, and confirm that saved diarization state continues in the replacement session.

## Prepare for production

Before production, choose and configure a Redis-compatible service that meets your organization's reliability and security requirements. Evaluate its compatibility with the two container settings in this article, and plan for the following areas:

- Network connectivity and endpoint reachability from each speech container.
- Authentication and TLS appropriate for your environment.
- Persistence and high availability.
- Monitoring and scaling.
- Failover and recovery procedures.
- Application handling for starting replacement recognition sessions and checking diarization continuity.
- Platform-specific deployment configuration, including Kubernetes or Helm configuration when applicable.

## Related content

- [Speech to text containers with Docker](speech-container-stt.md)
- [Configure Speech containers](speech-container-configuration.md)
- [Speech to text container release notes](releasenotes.md?tabs=speech-to-text)