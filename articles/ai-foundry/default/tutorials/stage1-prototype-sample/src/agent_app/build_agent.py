"""Create a single agent with SharePoint + (placeholder) MCP tool.
[TO VERIFY] Update SDK imports, tool classes, and method signatures.
"""
from .config import settings
from .mcp_client import MCPToolPlaceholder

try:
    from azure.identity import DefaultAzureCredential  # type: ignore
    from azure.ai.projects import AIProjectClient  # [TO VERIFY import path]
    from azure.ai.agents.models import SharepointTool  # [TO VERIFY class name]
except Exception:  # pragma: no cover - keep sample resilient
    DefaultAzureCredential = object  # type: ignore
    AIProjectClient = object  # type: ignore
    SharepointTool = object  # type: ignore

SYSTEM_INSTRUCTIONS = (
    "You are an enterprise knowledge assistant. Use SharePoint grounding when user queries reference internal "
    "policies, procedures, or documents. Use MCP tools for real-time external API enrichment when needed. "
    "Answer concisely and cite document titles when grounding applies."
)


def create_agent(project_client):  # [TO VERIFY signature / API]
    sharepoint_tool = SharepointTool(connection_name=settings.sharepoint_resource)  # [TO VERIFY parameter]
    mcp_tool_placeholder = MCPToolPlaceholder(endpoint=settings.mcp_endpoint)
    # [TO VERIFY] Replace placeholder with actual MCP tool once available
    tools = [sharepoint_tool]  # append real MCP tool when integrated

    agent = project_client.agents.create(  # [TO VERIFY]
        model=settings.model_deployment,
        instructions=SYSTEM_INSTRUCTIONS,
        tools=tools,
        name="proto-stage1-agent",
    )
    return agent


def main():
    settings.validate()
    credential = DefaultAzureCredential()  # [TO VERIFY] ensure environment supports default chain
    client = AIProjectClient(endpoint=settings.project_endpoint, credential=credential)
    agent = create_agent(client)
    print(f"Created agent id: {getattr(agent, 'id', '[TO VERIFY id attr]')}")

    # Smoke test thread/run (pseudo; adjust per final SDK)
    try:
        thread = client.threads.create()  # [TO VERIFY]
        client.messages.create(thread_id=thread.id, role="user", content="Summarize remote work policy")  # [TO VERIFY]
        run = client.runs.create(thread_id=thread.id, assistant_id=agent.id)  # [TO VERIFY]
        print("Started run:", getattr(run, 'id', '[TO VERIFY run id]'))
    except Exception as e:  # noqa: BLE001
        print("[INFO] Smoke test skipped or failed (expected in placeholder mode):", e)


if __name__ == "__main__":  # pragma: no cover
    main()
