---
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: include
ms.date: 11/18/2025
ms.author: lajanuar
---
Use the following commands to delete the environment variables you created for this quickstart.

#### [Windows](#tab/windows)

```console
reg delete "HKCU\Environment" /v LANGUAGE_KEY /f
```

```console
reg delete "HKCU\Environment" /v LANGUAGE_ENDPOINT /f
```

#### [Linux](#tab/linux)

```bash
unset LANGUAGE_KEY
```

```bash
unset LANGUAGE_ENDPOINT
```

#### [macOS](#tab/macos)

```bash
unset LANGUAGE_KEY
```

```bash
unset LANGUAGE_ENDPOINT
```

---
