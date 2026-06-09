# Profile: MCP Server Standardization

- **Category**: Communication Protocols
- **Release Status**: Draft Spec
- **Target Audience**: Tool Developers

## Agent-Native Characteristics
Model Context Protocol (MCP) defines an open standard for how foundation models connect to tools, documents, and data sources. MCP replaces custom API integrations with a unified, bi-directional JSON-RPC protocol, allowing any compliant agent client to dynamically discover and consume tools exposed by any host server.

## Aesthetic/UX Details
The protocol functions as a lightweight service running over standard transport layers like Server-Sent Events (SSE) or stdio. Developers configure client connections via simple JSON config files, and the client automatically maps available resources into the agent's context.

## Key Takeaways & Market Signal
Standardization resolves ecosystem fragmentation. By establishing a shared interface for tools and context retrieval, MCP enables developers to build reusable tool servers that work seamlessly across different models and orchestrators.

## References
- [Model Context Protocol Specification](https://modelcontextprotocol.io)
