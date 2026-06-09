# Model Context Protocol (MCP) by Anthropic
> Ingested on: 2026-06-08 00:20:16
> Category: field_notes
> Index: 001

# Profile
- **Name**: Model Context Protocol (MCP)
- **Category**: Open Standard / Tool Orchestration Protocol
- **Creator**: Anthropic (Released November 2024, standardized throughout 2025/2026)
- **Status**: Open-source specification & SDKs (Python, TypeScript)

# Agent-Native Characteristics
- **Universal Connectivity**: Solves the N×M integration bottleneck by introducing a "USB-C port for AI".
- **Client-Server Architecture**: Separates the MCP Client (e.g., Claude Desktop, IDEs like Cursor/VS Code) from the MCP Server (e.g., databases, GitHub, Slack, local terminals).
- **JSON-RPC Communication**: Allows agents to safely inspect available tools, query resources, and request prompts via a lightweight standardized protocol.

# Aesthetic/UX Details
- Exposes structured schemas that render automatically inside developer IDEs.
- Allows humans to monitor agent tool calls in real-time, providing click-to-approve interface gates for unsafe operations.

# Key Takeaways & Market Signal
- **Signal**: Walled gardens are giving way to unified APIs. Instead of building custom wrappers, startups are building MCP-compliant servers, ensuring instant compatibility with all major LLMs.
- **Reference**: https://modelcontextprotocol.io