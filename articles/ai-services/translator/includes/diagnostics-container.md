---

titleSuffix: Foundry Tools
author:laujan
ms.service: azure-ai-services
ms.topic: include
ms.date: 11/18/2025
ms.author: lajanuar
---

If you're having trouble running a Foundry Tools container, you can try using the Microsoft diagnostics container. Use this container to diagnose common errors in your deployment environment that might prevent Azure containers from functioning as expected.

To get the container, use the following `docker pull` command:

```bash
docker pull mcr.microsoft.com/azure-cognitive-services/diagnostic
```

Then run the container. Replace `{ENDPOINT_URI}` with your endpoint, and replace `{API_KEY}` with your key to your resource:

```bash
docker run --rm mcr.microsoft.com/azure-cognitive-services/diagnostic \
eula=accept \
Billing={ENDPOINT_URI} \
ApiKey={API_KEY}
```

The container tests for network connectivity to the billing endpoint.
