---
title: Include file
description: Include file
author: ms-johnalex
ms.reviewer: dantaylo
ms.author: johalexander
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 03/20/2026
ms.custom: include
---

## Troubleshooting

### Authentication errors

If you see `DefaultAzureCredential failed to retrieve a token`:

1. **Verify Azure CLI is authenticated**:
   ```bash
   az account show
   az login  # if not logged in
   ```

2. **Check RBAC role assignment**:
   - Confirm you have at least the Azure AI User role on the Foundry project
   - See [Assign Azure roles](/azure/role-based-access-control/role-assignments-portal)

3. **For managed identity in production**:
   - Ensure the managed identity has the appropriate role assigned
   - See [Configure managed identities](../concepts/authentication-authorization-foundry.md#identity-types)

### Endpoint configuration errors

If you see `Connection refused` or `404 Not Found`:

- **Verify resource and project names** match your actual deployment
- **Check endpoint URL format**: Should be `https://<resource-name>.services.ai.azure.com/api/projects/<project-name>`
- **For custom subdomains**: Replace `<resource-name>` with your custom subdomain

### SDK version mismatches

If code samples fail with `AttributeError` or `ModuleNotFoundError`:

- **Check SDK version**:
  ```bash
  pip show azure-ai-projects  # Python
  npm list @azure/ai-projects  # JavaScript
  dotnet list package  # .NET
  ```

- **Reinstall with correct version flags**: See installation commands in each language section above
