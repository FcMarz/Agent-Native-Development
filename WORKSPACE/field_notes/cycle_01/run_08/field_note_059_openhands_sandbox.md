# OpenHands: Docker-Sandboxed Developer Workspace
> Ingested on: 2026-06-08 01:41:22
> Category: field_notes
> Index: 059
> Phase: 01 | Run: 08

# Profile
- **Name**: OpenHands
- **Category**: Sandboxed Developer Agent
- **Status**: Active open-source development, standard for sandbox environments

# Agent-Native Characteristics
- **Docker-Isolated Workspace**: Spawns a dedicated Docker container to run agent code, protecting host filesystems.
- **Arbitrary Command Execution**: Runs commands, installs libraries, and spins up test servers inside the container.
- **Workspace File Syncing**: Synchronizes project directories between host and sandboxed environments seamlessly.

# Aesthetic/UX Details
- Dual-panel Web UI showing active workspace explorer, visual terminal feeds, and agent messaging interfaces.

# Key Takeaways & Market Signal
- **Signal**: Sandboxing is non-negotiable for enterprise agents. Arbitrary execution of bash scripts requires secure, containerized boundaries to prevent resource damage or security exploits.
- **Reference**: https://github.com/All-Hands-AI/OpenHands