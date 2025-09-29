"""Placeholder MCP client/tool adapter.

Replace with official MCP tool integration once confirmed.
"""
from dataclasses import dataclass

@dataclass
class MCPToolPlaceholder:
    endpoint: str
    name: str = "mcp-tool"

    def describe(self):  # helper for debugging
        return {"type": "mcp_placeholder", "endpoint": self.endpoint, "name": self.name}
