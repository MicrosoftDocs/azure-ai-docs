Add following section to this existing doc:
<https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/rbac-azure-ai-foundry>

###  Use Entra ID Groups with Azure AI Foundry

#### What are Entra ID Groups?

Microsoft Entra ID provides several ways to manage access to resources,
applications, and tasks. With Microsoft Entra groups, you can grant
access and permissions to a group of users instead of to each individual
user. Entra groups can be created in the Azure portal for enterprise IT
admins to simplify the role assignment process for developers. By
creating an Entra group, IT admins can minimize the number of role
assignments required for new developers working on Foundry projects by
assigning the group the required role assignment on the necessary
resource.

Complete the following steps to use Entra ID groups with Azure AI
Foundry:

1)  Navigate to “Groups” in the Azure Portal.

2)  Create a new “Security” group in the Groups portal.

3)  Assign the Owner of the Entra group and add individual user
    principles in your organization to the group as Members. Save the
    group.

4)  Navigate to the resource that requires a role assignment.

    1.  **Example:** To build Agents, run traces, and more in Foundry,
        the minimum privilege ‘Azure AI User’ role must be assigned to
        your user principle. Assing the ‘Azure AI User’ role to your new
        Entra group so all users in your enterprise can build in
        Foundry.

    2.  **Example:** To use Tracing and Monitoring features in Azure AI
        Foundry, a ‘Reader’ role assignment on the connected Application
        Insights resource is required. Assign the ‘Reader’ role to your
        new Entra group so all users in your enterprise can use the
        Tracing and Monitoring feature.

5)  Navigate to Access Control (IAM).

6)  Select the role to assign.

7)  Assign access to “User, group, or service principle” and select the
    new Security group.

8)  Review and assign. Role assignment will now apply to all user
    principles assigned to the group.

To learn more about Entra ID groups, prerequisites, and limitations, see
the following documents:

- [Learn about groups, group membership, and access - Microsoft Entra \|
  Microsoft
  Learn](https://learn.microsoft.com/en-us/entra/fundamentals/concept-learn-about-groups)

- [How to manage groups - Microsoft Entra \| Microsoft
  Learn](https://learn.microsoft.com/en-us/entra/fundamentals/how-to-manage-groups)
